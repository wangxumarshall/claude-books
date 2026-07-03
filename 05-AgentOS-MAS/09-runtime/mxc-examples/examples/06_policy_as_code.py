"""
示例 06: 策略即代码 (Policy-as-Code)

演示从 YAML 策略文件加载并执行策略的模式：
  1. 从 YAML 加载策略
  2. 策略验证和合规检查
  3. 多角色策略选择
  4. 策略版本控制

核心概念:
  - Policy-as-Code: 将安全策略存储为版本化的代码文件
    （来源: 业界最佳实践 + MXC 策略设计原则）
  - load_policy_from_yaml: 自定义扩展函数（mxc.py）
  - Intent, Not Mechanism: 策略描述 "what"，不描述 "how"
    （来源: Sandbox Policy Spec v1 §3 — Principle 1）

参考来源:
  - GitHub: microsoft/mxc — Sandbox Policy Spec v1
  - AgentBound (arXiv:2510.21236) — 声明式策略机制
  - Windows Blog: Build 2026 — "policy-based controls"
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mxc import (
    MxcClient,
    SandboxPolicy,
    ProcessConfig,
    ContainmentBackend,
    AuditLogger,
    load_policy_from_yaml,
    MXC_SCHEMA_VERSION,
)


POLICIES_DIR = Path(__file__).parent.parent / "policies"


def example_load_yaml_policy():
    """
    从 YAML 文件加载策略。

    演示 load_policy_from_yaml() 函数的使用：
      - 解析 YAML 中的 filesystem/network/ui 策略
      - 转换为 SandboxPolicy dataclass
      - 创建 ContainerConfig 并执行

    对应 Policy-as-Code 工作流：
      1. 安全团队编写 YAML 策略文件
      2. 策略文件进入 Git 版本控制
      3. CI/CD 验证策略语法和合规性
      4. 运行时从 YAML 加载并执行
    """
    print("=" * 60)
    print("场景 1: 从 YAML 加载代码执行策略")
    print("=" * 60)

    policy_file = POLICIES_DIR / "code_execution_policy.yaml"
    print(f"\n[策略文件] {policy_file}")

    # 加载策略
    policy = load_policy_from_yaml(str(policy_file))

    print(f"\n[加载的策略摘要]")
    print(f"  Schema 版本: {policy.version}")
    print(f"  超时:        {policy.timeout_ms}ms")

    if policy.filesystem:
        print(f"\n  文件系统策略:")
        print(f"    可写路径: {policy.filesystem.readwrite_paths}")
        print(f"    只读路径: {policy.filesystem.readonly_paths}")
        print(f"    拒绝路径: {policy.filesystem.denied_paths}")

    if policy.network:
        print(f"\n  网络策略:")
        print(f"    出站:     {policy.network.allow_outbound}")
        print(f"    本地网络: {policy.network.allow_local_network}")

    if policy.ui:
        print(f"\n  UI 策略:")
        print(f"    窗口:     {policy.ui.allow_windows}")
        print(f"    剪贴板:   {policy.ui.clipboard.value}")

    # 创建配置
    client = MxcClient()
    config = client.create_config_from_policy(policy)
    config.process = ProcessConfig(
        command_line='python -c "print(\'Code execution under YAML policy\')"',
        cwd="/workspace",
    )

    print(f"\n[生成的配置 JSON]")
    print(config.to_json())


def example_enterprise_multi_role():
    """
    企业多角色策略 — 根据 Agent 角色选择不同策略配置。

    企业策略文件（enterprise_policy.yaml）定义了多个 Agent 角色，
    每个角色有差异化的隔离配置。

    对应 Windows Blog 中:
    "Agent 365's policy-based controls with Microsoft Entra and Intune
     will be used to apply those MXC constraints to a specific agent."
    """
    print("\n" + "=" * 60)
    print("场景 2: 企业多角色策略选择")
    print("=" * 60)

    try:
        import yaml
    except ImportError:
        print("  ⚠️ 需要 pyyaml: pip install pyyaml")
        return

    policy_file = POLICIES_DIR / "enterprise_policy.yaml"
    with open(policy_file, "r", encoding="utf-8") as f:
        enterprise_data = yaml.safe_load(f)

    print(f"\n[企业策略] {enterprise_data.get('name', 'unknown')}")
    print(f"  描述: {enterprise_data.get('description', '')[:60]}...")

    # 列出所有 Agent 角色
    profiles = enterprise_data.get("profiles", [])
    print(f"\n[Agent 角色列表]")
    for profile in profiles:
        name = profile.get("name", "unknown")
        desc = profile.get("description", "")
        containment = profile.get("containment", "process")
        timeout = profile.get("timeoutMs", "default")
        print(f"  📋 {name:<25} | 后端: {containment:<20} | 超时: {timeout}ms")
        print(f"     {desc}")

    # 选择特定角色执行
    print(f"\n[选择 'coding-agent' 角色执行]")
    coding_profile = next(
        (p for p in profiles if p["name"] == "coding-agent"), None
    )

    if coding_profile:
        from mxc import FilesystemPolicy, NetworkPolicy, UIPolicy, ClipboardAccess

        fs = coding_profile.get("filesystem", {})
        net = coding_profile.get("network", {})
        ui = coding_profile.get("ui", {})

        policy = SandboxPolicy(
            version=enterprise_data.get("version", MXC_SCHEMA_VERSION),
            filesystem=FilesystemPolicy(
                readwrite_paths=fs.get("readwritePaths", []),
                readonly_paths=fs.get("readonlyPaths", []),
                denied_paths=fs.get("deniedPaths", []),
            ),
            network=NetworkPolicy(
                allow_outbound=net.get("allowOutbound", False),
                allow_local_network=net.get("allowLocalNetwork", False),
            ),
            ui=UIPolicy(
                allow_windows=ui.get("allowWindows", False),
                clipboard=ClipboardAccess(ui.get("clipboard", "none")),
                allow_input_injection=ui.get("allowInputInjection", False),
            ),
            timeout_ms=coding_profile.get("timeoutMs"),
        )

        client = MxcClient()
        config = client.create_config_from_policy(policy)
        config.process = ProcessConfig(
            command_line='python -c "print(\'Coding agent execution\')"',
        )

        print(f"\n  生成的配置:")
        print(f"    后端:     {config.containment}")
        print(f"    可写路径: {policy.filesystem.readwrite_paths}")
        print(f"    只读路径: {policy.filesystem.readonly_paths}")
        print(f"    网络:     {policy.network.allow_outbound}")


def example_policy_validation():
    """
    策略验证 — 在部署前检查策略的合规性。

    验证规则:
      - Schema 版本兼容性
      - 路径冲突检测
      - 网络策略一致性
      - 超时范围检查
    """
    print("\n" + "=" * 60)
    print("场景 3: 策略验证")
    print("=" * 60)

    policy_files = [
        "code_execution_policy.yaml",
        "data_access_policy.yaml",
        "enterprise_policy.yaml",
    ]

    print("\n[策略验证报告]")
    print(f"  {'文件':<40} {'版本':<15} {'状态':<10}")
    print(f"  {'─' * 40} {'─' * 15} {'─' * 10}")

    for filename in policy_files:
        filepath = POLICIES_DIR / filename
        try:
            policy = load_policy_from_yaml(str(filepath))

            # 版本检查
            version_ok = policy.version == MXC_SCHEMA_VERSION

            # 路径冲突检查
            path_conflicts = []
            if policy.filesystem:
                rw = set(policy.filesystem.readwrite_paths)
                ro = set(policy.filesystem.readonly_paths)
                denied = set(policy.filesystem.denied_paths)
                if rw & ro:
                    path_conflicts.append("readwrite ∩ readonly")
                if rw & denied:
                    path_conflicts.append("readwrite ∩ denied")

            # 网络一致性检查
            net_ok = True
            if policy.network:
                if policy.network.allowed_hosts and not policy.network.allow_outbound:
                    net_ok = False

            status = "✅ 通过" if (version_ok and not path_conflicts and net_ok) else "⚠️ 警告"
            print(f"  {filename:<40} {policy.version:<15} {status:<10}")

            if path_conflicts:
                print(f"    ⚠️ 路径冲突: {', '.join(path_conflicts)}")
            if not net_ok:
                print(f"    ⚠️ 网络策略不一致: allowedHosts 需要 allowOutbound=true")

        except Exception as e:
            print(f"  {filename:<40} {'N/A':<15} ❌ 错误: {e}")


def example_policy_versioning():
    """
    策略版本控制 — 展示 Schema 版本演进策略。

    来源: GitHub — docs/versioning.md
    "While in 0.x (initial development), any release may include
     breaking changes per semver §4."
    """
    print("\n" + "=" * 60)
    print("场景 4: 策略版本控制")
    print("=" * 60)

    print("""
[MXC Schema 版本演进]

  0.3.0-alpha  ──→  0.4.0-alpha  ──→  0.5.0-alpha  ──→  0.6.0-alpha  ──→  0.7.0-dev
  (初始)            (移除遗留字段)     (稳定)            (当前稳定)          (实验性)

[版本兼容性规则（来源: docs/schema.md）]

  | 配置版本       | 解析器支持     | 结果          |
  |---------------|---------------|--------------|
  | 0.3.0-alpha   | >=0.4, <=0.5  | ❌ 过旧       |
  | 0.4.0-alpha   | >=0.4, <=0.5  | ✅ 兼容       |
  | 0.5.0-alpha   | >=0.4, <=0.5  | ✅ 兼容       |
  | 0.6.0         | >=0.4, <=0.5  | ❌ 过新       |

[最佳实践]
  1. 策略文件始终显式声明 version 字段
  2. 使用当前稳定版本（0.6.0-alpha）创建新策略
  3. 升级时进行兼容性测试
  4. 在 CI/CD 中验证策略版本兼容性
""")


def main():
    """运行所有策略即代码示例"""
    print("MXC 策略即代码 (Policy-as-Code) 示例")
    print("=" * 60)
    print("\n本示例演示 MXC 的 Policy-as-Code 模式：")
    print("  1. 从 YAML 加载策略")
    print("  2. 企业多角色策略选择")
    print("  3. 策略验证和合规检查")
    print("  4. 策略版本控制\n")

    example_load_yaml_policy()
    example_enterprise_multi_role()
    example_policy_validation()
    example_policy_versioning()

    print("\n" + "=" * 60)
    print("示例 06 完成 ✓")
    print("=" * 60)
    print("\n关键要点:")
    print("  1. YAML 策略文件实现策略的版本化和可审查性")
    print("  2. 企业策略支持多角色差异化配置")
    print("  3. 部署前验证策略的语法和合规性")
    print("  4. Schema 版本遵循 semver，当前稳定版为 0.6.0-alpha")
    print("  5. Policy-as-Code 使安全策略成为可测试的代码资产")


if __name__ == "__main__":
    main()
