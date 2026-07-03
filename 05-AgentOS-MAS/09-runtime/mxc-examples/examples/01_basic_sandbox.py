"""
示例 01: 基础沙箱使用 (Basic Sandbox)

演示 MXC 最基本的沙箱创建和代码执行流程：
  1. 检测平台支持
  2. 创建 Default-Deny 策略
  3. 在沙箱中执行 Python 代码
  4. 获取执行结果

核心概念:
  - SandboxPolicy: 声明安全意图（来源: Sandbox Policy Spec v1 §5）
  - Default-Deny: 省略的策略字段 = 最严格权限（来源: Policy Spec §3 Principle 2）
  - spawnSandbox: 一步式沙箱创建（来源: @microsoft/mxc-sdk 导出）

参考来源:
  - GitHub: microsoft/mxc — SDK 快速开始
  - Windows Blog: Build 2026 — Process Isolation 章节
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from mxc import (
    MxcClient,
    SandboxPolicy,
    FilesystemPolicy,
    NetworkPolicy,
    UIPolicy,
    ClipboardAccess,
    ContainmentBackend,
    get_platform_support,
    get_available_tools_policy,
    get_temporary_files_policy,
    MXC_SCHEMA_VERSION,
)


def example_01_minimal_sandbox():
    """
    最小化沙箱 — 完全 Default-Deny。

    空策略 = 无文件系统访问 + 无网络 + 无 UI + 无输入注入。
    这是 MXC 安全模型的基石：一切默认禁止，仅显式授权。

    对应 TypeScript SDK:
      spawnSandbox("script.sh", { version: "0.6.0-alpha" });
    """
    print("=" * 60)
    print("示例 1a: 最小化沙箱（Default-Deny）")
    print("=" * 60)

    # 创建空策略 — 一切默认禁止
    policy = SandboxPolicy(version=MXC_SCHEMA_VERSION)

    # 创建客户端并生成配置
    client = MxcClient(debug=True)
    config = client.create_config_from_policy(policy)

    # 设置要执行的命令
    config.process = type(config.process)(
        command_line='python -c "print(\'Hello from MXC sandbox!\')"'
    ) if config.process else None

    # 干运行模式 — 查看生成的 JSON 配置
    print("\n[生成的容器配置 JSON]")
    print(client.dry_run(config))
    print("\n[说明] 空策略生成的配置中：")
    print("  - 无 filesystem 节（无文件访问）")
    print("  - 无 network 节（无网络访问）")
    print("  - ui.disable=true（无 UI）")
    print("  - lifecycle.destroyOnExit=true（执行后销毁）")


def example_02_basic_with_tools():
    """
    带工具发现的基础沙箱。

    使用 SDK 辅助函数自动发现主机环境：
      - getAvailableToolsPolicy() → 发现 Python/Node 安装路径
      - getTemporaryFilesPolicy() → 获取临时目录

    对应 TypeScript SDK:
      const tools = getAvailableToolsPolicy(process.env);
      const temp  = getTemporaryFilesPolicy();
    """
    print("\n" + "=" * 60)
    print("示例 1b: 带工具发现的基础沙箱")
    print("=" * 60)

    # 自动发现主机工具路径
    tools_policy = get_available_tools_policy()
    temp_policy = get_temporary_files_policy()

    print(f"\n[发现的工具路径（只读）]")
    for path in tools_policy.readonly_paths:
        print(f"  - {path}")

    print(f"\n[临时目录（可写）]")
    for path in temp_policy.readwrite_paths:
        print(f"  - {path}")

    # 组合策略
    policy = SandboxPolicy(
        version=MXC_SCHEMA_VERSION,
        filesystem=FilesystemPolicy(
            readonly_paths=tools_policy.readonly_paths,
            readwrite_paths=temp_policy.readwrite_paths,
        ),
        network=NetworkPolicy(allow_outbound=False),
        timeout_ms=30000,
    )

    # 创建沙箱配置
    client = MxcClient()
    config = client.create_config_from_policy(
        policy,
        containment=ContainmentBackend.PROCESS,
    )
    config.process = type(config.process)(
        command_line='python -S -B -c "import sys; print(f\'Python {sys.version} in sandbox\')"'
    ) if config.process else None

    print("\n[生成的容器配置 JSON]")
    print(client.dry_run(config))


def example_03_explicit_policy():
    """
    显式策略配置 — 精确控制每个安全维度。

    展示 SandboxPolicy 的完整字段：
      - filesystem: 读写/只读/拒绝路径
      - network: 出站控制
      - ui: 窗口/剪贴板/输入注入
      - timeoutMs: 执行超时
    """
    print("\n" + "=" * 60)
    print("示例 1c: 显式策略配置")
    print("=" * 60)

    policy = SandboxPolicy(
        version=MXC_SCHEMA_VERSION,
        filesystem=FilesystemPolicy(
            readwrite_paths=["/workspace/output"],
            readonly_paths=["/workspace/src", "/usr/local/lib/python3.12"],
            denied_paths=["/etc/shadow", "/root/.ssh"],
            temp_dir=None,
        ),
        network=NetworkPolicy(
            allow_outbound=False,
            allow_local_network=False,
        ),
        ui=UIPolicy(
            allow_windows=False,
            clipboard=ClipboardAccess.NONE,
            allow_input_injection=False,
        ),
        timeout_ms=60000,
    )

    client = MxcClient()
    config = client.create_config_from_policy(policy)

    # 设置执行命令
    from mxc import ProcessConfig
    config.process = ProcessConfig(
        command_line='python -c "result = sum(range(100)); print(f\'Sum: {result}\')"',
        cwd="/workspace",
        timeout=60000,
    )

    print("\n[策略摘要]")
    print(f"  Schema 版本: {policy.version}")
    print(f"  容器后端:    {config.containment}")
    print(f"  可写路径:    {policy.filesystem.readwrite_paths}")
    print(f"  只读路径:    {policy.filesystem.readonly_paths}")
    print(f"  拒绝路径:    {policy.filesystem.denied_paths}")
    print(f"  网络出站:    {policy.network.allow_outbound}")
    print(f"  UI 窗口:     {policy.ui.allow_windows}")
    print(f"  剪贴板:      {policy.ui.clipboard.value}")
    print(f"  超时:        {policy.timeout_ms}ms")

    print("\n[完整配置 JSON]")
    print(config.to_json())


def main():
    """运行所有基础沙箱示例"""

    # 首先检测平台支持
    print("MXC 基础沙箱示例")
    print("=" * 60)

    platform_info = get_platform_support()
    print(f"\n[平台检测结果]")
    print(f"  操作系统:       {platform_info.platform}")
    print(f"  MXC 支持:       {'是' if platform_info.is_supported else '否'}")
    print(f"  默认后端:       {platform_info.default_backend}")
    print(f"  可用后端:       {', '.join(platform_info.available_backends)}")
    print(f"  原生二进制:     {platform_info.native_binary or 'N/A'}")
    print(f"  Schema 版本:    {MXC_SCHEMA_VERSION}")

    if not platform_info.is_supported:
        print("\n⚠️ 当前平台不支持 MXC，示例将以 dry-run 模式运行。")

    # 运行示例
    example_01_minimal_sandbox()
    example_02_basic_with_tools()
    example_03_explicit_policy()

    print("\n" + "=" * 60)
    print("示例 01 完成 ✓")
    print("=" * 60)
    print("\n关键要点:")
    print("  1. MXC 遵循 Default-Deny 原则 — 空策略 = 完全锁定")
    print("  2. 使用辅助函数自动发现主机环境（工具路径、临时目录）")
    print("  3. SandboxPolicy 描述安全意图，ContainerConfig 描述后端实现")
    print("  4. 进程级隔离（processcontainer）是最快速的隔离方式")


if __name__ == "__main__":
    main()
