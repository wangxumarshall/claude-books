"""
示例 03: 网络限制配置 (Network Restrictions)

演示 MXC 网络策略的四种配置场景：
  1. 完全无网络 — 代码执行最安全
  2. 仅允许特定主机 — API 调用受限
  3. 阻止特定主机 — 黑名单模式
  4. 代理路由 — 企业级流量控制

核心概念:
  - NetworkPolicy: 网络访问控制（来源: Sandbox Policy Spec v1 §5 — network）
  - Default-Deny: 省略 = 无网络访问（所有标志默认 false）
  - enforcementMode: 防火墙或能力限制（来源: schema.md — network.enforcementMode）

⚠️ 已知平台限制:
  - allowedHosts/blockedHosts 在 Windows processcontainer 上尚未支持
    （来源: GitHub README — "allow/block outbound and host filtering not yet supported on Windows"）
  - proxy 在 macOS seatbelt 后端上不支持
    （来源: GitHub README — "Proxy support not supported on macOS"）

参考来源:
  - GitHub: microsoft/mxc — docs/schema.md §Network Policy
  - GitHub: microsoft/mxc — Sandbox Policy Spec v1 §5
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mxc import (
    MxcClient,
    SandboxPolicy,
    FilesystemPolicy,
    NetworkPolicy,
    UIPolicy,
    ProcessConfig,
    ContainmentBackend,
    MXC_SCHEMA_VERSION,
)


def scenario_1_no_network():
    """
    场景 1: 完全无网络 — 最安全的代码执行环境。

    适用于: 代码生成/执行、单元测试、本地计算任务
    对应 TypeScript SDK:
      network: { allowOutbound: false }
    """
    print("=" * 60)
    print("场景 1: 完全无网络")
    print("=" * 60)

    policy = SandboxPolicy(
        version=MXC_SCHEMA_VERSION,
        filesystem=FilesystemPolicy(
            readwrite_paths=["/workspace/output"],
            readonly_paths=["/workspace/src"],
        ),
        network=NetworkPolicy(
            allow_outbound=False,       # 禁止所有出站连接
            allow_local_network=False,  # 禁止本地网络
        ),
        ui=UIPolicy(allow_windows=False),
        timeout_ms=60000,
    )

    client = MxcClient()
    config = client.create_config_from_policy(policy)
    config.process = ProcessConfig(
        command_line='python -c "result = sum(range(1000)); print(f\'Result: {result}\')"',
    )

    print("\n[网络策略]")
    print(f"  allowOutbound:    {policy.network.allow_outbound}")
    print(f"  allowLocalNetwork: {policy.network.allow_local_network}")
    print(f"  → 完全隔离，无任何网络访问能力")

    print("\n[生成的网络配置]")
    print(f"  defaultPolicy: block")
    print(f"  enforcementMode: firewall")
    print(f"\n  {config.to_json()}")


def scenario_2_allowlisted_hosts():
    """
    场景 2: 仅允许特定主机 — 白名单模式。

    适用于: 需要调用外部 API 的 Agent（如天气查询、代码搜索）
    ⚠️ allowedHosts 在 Windows 上尚未支持

    对应 TypeScript SDK:
      network: { allowOutbound: true, allowedHosts: ["api.github.com"] }
    """
    print("\n" + "=" * 60)
    print("场景 2: 仅允许特定主机（白名单）")
    print("=" * 60)

    policy = SandboxPolicy(
        version=MXC_SCHEMA_VERSION,
        filesystem=FilesystemPolicy(
            readwrite_paths=["/workspace/output"],
            readonly_paths=["/workspace/src"],
        ),
        network=NetworkPolicy(
            allow_outbound=True,
            allow_local_network=False,
            allowed_hosts=[
                "api.github.com",           # GitHub API（代码搜索）
                "registry.npmjs.org",       # npm 包注册表
                "pypi.org",                 # PyPI 包索引
                "files.pythonhosted.org",   # PyPI 文件下载
            ],
        ),
        timeout_ms=120000,
    )

    client = MxcClient()
    config = client.create_config_from_policy(policy)
    config.process = ProcessConfig(
        command_line='python -c "print(\'Fetching from allowed hosts...\')"',
    )

    print("\n[网络策略]")
    print(f"  allowOutbound: {policy.network.allow_outbound}")
    print(f"  允许的主机:")
    for host in policy.network.allowed_hosts:
        print(f"    ✅ {host}")
    print(f"\n  ⚠️ 注意: allowedHosts 在 Windows processcontainer 上尚未支持")
    print(f"     此功能在 Linux (bubblewrap/lxc) 上可用")


def scenario_3_blocked_hosts():
    """
    场景 3: 阻止特定主机 — 黑名单模式。

    适用于: 一般允许网络但需阻止危险域名的场景
    ⚠️ blockedHosts 在 Windows 上尚未支持

    对应 TypeScript SDK:
      network: { allowOutbound: true, blockedHosts: ["evil.com"] }
    """
    print("\n" + "=" * 60)
    print("场景 3: 阻止特定主机（黑名单）")
    print("=" * 60)

    policy = SandboxPolicy(
        version=MXC_SCHEMA_VERSION,
        filesystem=FilesystemPolicy(
            readwrite_paths=["/workspace/output"],
            readonly_paths=["/workspace/src"],
        ),
        network=NetworkPolicy(
            allow_outbound=True,
            allow_local_network=True,
            blocked_hosts=[
                "*.malware-domain.com",     # 恶意软件域名
                "*.cryptominer.net",        # 加密货币挖矿
                "paste.ee",                 # 代码粘贴板（数据泄露风险）
                "pastebin.com",             # 代码粘贴板
                "*.ngrok.io",               # 隧道服务（安全审计绕过）
            ],
        ),
        timeout_ms=120000,
    )

    client = MxcClient()
    config = client.create_config_from_policy(policy)
    config.process = ProcessConfig(
        command_line='python -c "print(\'Network with blocklist...\')"',
    )

    print("\n[网络策略]")
    print(f"  allowOutbound: {policy.network.allow_outbound}")
    print(f"  阻止的主机:")
    for host in policy.network.blocked_hosts:
        print(f"    🚫 {host}")
    print(f"\n  ⚠️ blockedHosts 在 Windows 上尚未支持")


def scenario_4_proxy_routing():
    """
    场景 4: 代理路由 — 所有流量通过企业代理。

    适用于: 企业环境中需要集中流量控制和审计的场景
    ⚠️ proxy 在 macOS 上不支持

    对应 TypeScript SDK:
      network: { proxy: { url: "http://proxy:8080" } }
    """
    print("\n" + "=" * 60)
    print("场景 4: 企业代理路由")
    print("=" * 60)

    policy = SandboxPolicy(
        version=MXC_SCHEMA_VERSION,
        filesystem=FilesystemPolicy(
            readwrite_paths=["/workspace/output"],
            readonly_paths=["/workspace/src", "/opt/corp-tools"],
        ),
        network=NetworkPolicy(
            allow_outbound=True,
            allow_local_network=True,
            proxy={"url": "http://corp-proxy.internal:8080"},
        ),
        timeout_ms=180000,
    )

    client = MxcClient()
    config = client.create_config_from_policy(policy)
    config.process = ProcessConfig(
        command_line='python -c "print(\'Routed through corporate proxy...\')"',
    )

    print("\n[网络策略]")
    print(f"  allowOutbound:    {policy.network.allow_outbound}")
    print(f"  allowLocalNetwork: {policy.network.allow_local_network}")
    print(f"  代理地址:          {policy.network.proxy}")
    print(f"\n  所有出站流量将通过企业代理路由，")
    print(f"  代理服务器可执行：")
    print(f"    - TLS 检查和审计日志")
    print(f"    - URL 过滤和恶意软件扫描")
    print(f"    - 带宽控制和速率限制")
    print(f"\n  ⚠️ proxy 在 macOS seatbelt 后端上不支持")


def main():
    """运行所有网络限制示例"""
    print("MXC 网络限制配置示例")
    print("=" * 60)
    print("\n本示例演示 MXC 的四种网络策略模式：")
    print("  1. 完全无网络    — Default-Deny 最安全")
    print("  2. 白名单模式    — 仅允许指定主机")
    print("  3. 黑名单模式    — 阻止危险域名")
    print("  4. 代理路由      — 企业级流量控制\n")

    scenario_1_no_network()
    scenario_2_allowlisted_hosts()
    scenario_3_blocked_hosts()
    scenario_4_proxy_routing()

    print("\n" + "=" * 60)
    print("示例 03 完成 ✓")
    print("=" * 60)
    print("\n关键要点:")
    print("  1. 默认情况下沙箱无任何网络访问能力（Default-Deny）")
    print("  2. allowedHosts 实现精确的白名单控制（⚠️ Windows 暂不支持）")
    print("  3. blockedHosts 实现黑名单过滤（⚠️ Windows 暂不支持）")
    print("  4. proxy 支持企业级流量路由（⚠️ macOS 暂不支持）")
    print("  5. 平台限制需在部署时考虑 — 建议 Linux 环境获得完整网络控制")


if __name__ == "__main__":
    main()
