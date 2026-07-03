"""
示例 05: 审计日志功能 (Audit Logging)

演示 MXC 的审计和诊断能力：
  1. Debug 模式诊断日志
  2. ETW (Event Tracing for Windows) 事件追踪
  3. 应用层审计追踪（AuditLogger）
  4. 合规性报告生成

核心概念:
  - Debug Logging: --debug 标志启用详细诊断输出
    （来源: GitHub docs/diagnostics.md）
  - ETW: Windows 事件追踪，提供 OS 级别的执行遥测
    （来源: GitHub README — "Event Tracing for Windows (ETW) for troubleshooting"）
  - AuditLogger: 应用层审计日志（本模块自定义扩展）

参考来源:
  - GitHub: microsoft/mxc — docs/diagnostics.md
  - Windows Blog: Build 2026 — "observability, governance and security capabilities"
"""

import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mxc import (
    MxcClient,
    SandboxPolicy,
    FilesystemPolicy,
    NetworkPolicy,
    UIPolicy,
    ProcessConfig,
    StatefulSandbox,
    ContainmentBackend,
    AuditLogger,
    AuditEntry,
    SandboxResult,
    MXC_SCHEMA_VERSION,
)


def example_debug_mode():
    """
    Debug 模式 — 启用详细诊断日志。

    MXC 原生二进制默认静默运行（stdin/stdout/stderr 直连容器），
    使用 --debug 标志可获取详细的执行过程日志。

    来源: GitHub README — "Debug Console Mode"
    "By default, native binaries run in silent mode.
     Use --debug for verbose output."
    """
    print("=" * 60)
    print("场景 1: Debug 模式诊断日志")
    print("=" * 60)

    # 创建启用 debug 的客户端
    client = MxcClient(debug=True)

    policy = SandboxPolicy(
        version=MXC_SCHEMA_VERSION,
        filesystem=FilesystemPolicy(
            readwrite_paths=["/workspace/output"],
            readonly_paths=["/workspace/src"],
        ),
        network=NetworkPolicy(allow_outbound=False),
        timeout_ms=30000,
    )

    config = client.create_config_from_policy(policy)
    config.process = ProcessConfig(
        command_line='python -c "print(\'Debug mode execution\')"',
    )

    print("\n[Debug 模式配置]")
    print(f"  debug 标志:       True")
    print(f"  预期命令行:       wxc-exec.exe --debug config.json")
    print(f"  诊断信息包含:")
    print(f"    - 配置解析过程")
    print(f"    - 后端选择和初始化")
    print(f"    - 文件系统策略应用")
    print(f"    - 网络策略应用")
    print(f"    - 进程创建和监控")
    print(f"    - 退出码和资源清理")

    print("\n[生成的配置 JSON]")
    print(config.to_json())


def example_etw_concept():
    """
    ETW (Event Tracing for Windows) 概念演示。

    ETW 是 Windows 内核级别的高性能事件追踪机制，
    MXC 通过 ETW 提供 OS 级的执行遥测数据。

    来源: GitHub README — "Event Tracing for Windows (ETW) for troubleshooting"
    """
    print("\n" + "=" * 60)
    print("场景 2: ETW 事件追踪概念")
    print("=" * 60)

    print("""
[ETW 事件追踪架构]

  ┌─────────────────────────────────────────────────────┐
  │  MXC 沙箱执行                                        │
  │                                                     │
  │  wxc-exec.exe                                       │
  │    ├── 配置解析                                      │
  │    ├── BaseContainerRunner 启动                      │
  │    ├── CreateProcessInSandbox                       │
  │    ├── 进程监控                                      │
  │    └── 资源清理                                      │
  │         │                                           │
  │         ▼                                           │
  │  ┌────────────────────┐                             │
  │  │  ETW Provider      │                             │
  │  │  (MXC Events)      │                             │
  │  └────────┬───────────┘                             │
  │           │                                         │
  │           ▼                                         │
  │  ┌────────────────────────────────────────────┐     │
  │  │  ETW Consumer                              │     │
  │  │                                            │     │
  │  │  - Windows Event Viewer                    │     │
  │  │  - logman / xperf 收集                     │     │
  │  │  - Azure Monitor / Log Analytics 集成      │     │
  │  │  - 第三方 SIEM 工具                        │     │
  │  └────────────────────────────────────────────┘     │
  └─────────────────────────────────────────────────────┘
""")

    # 模拟 ETW 事件结构
    etw_events = [
        {
            "event": "MXC.Sandbox.Create",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "containment": "processcontainer",
            "configVersion": "0.6.0-alpha",
            "processId": 12345,
        },
        {
            "event": "MXC.Filesystem.Policy.Apply",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "readonlyPaths": 3,
            "readwritePaths": 1,
            "deniedPaths": 2,
        },
        {
            "event": "MXC.Network.Policy.Apply",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "defaultPolicy": "block",
            "enforcementMode": "firewall",
        },
        {
            "event": "MXC.Process.Start",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "commandLine": "python -c \"print('hello')\"",
            "sandboxedPid": 12400,
        },
        {
            "event": "MXC.Process.Exit",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "exitCode": 0,
            "durationMs": 234,
        },
        {
            "event": "MXC.Sandbox.Destroy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "totalDurationMs": 312,
        },
    ]

    print("[模拟 ETW 事件流]")
    for event in etw_events:
        print(f"  {event['event']:<35} {json.dumps({k: v for k, v in event.items() if k != 'event'}, ensure_ascii=False)}")


def example_audit_logger():
    """
    应用层审计日志 — 记录每次沙箱执行的完整上下文。

    AuditLogger 提供结构化的审计追踪，包括：
      - 时间戳和 Agent 身份
      - 执行的命令和策略
      - 退出码和输出统计
      - 执行耗时
    """
    print("\n" + "=" * 60)
    print("场景 3: 应用层审计日志")
    print("=" * 60)

    # 创建审计日志记录器
    log_file = "/tmp/mxc-audit.jsonl"
    audit = AuditLogger(log_file=None)  # 仅内存记录，不写文件

    client = MxcClient()
    policy = SandboxPolicy(
        version=MXC_SCHEMA_VERSION,
        filesystem=FilesystemPolicy(
            readwrite_paths=["/workspace/output"],
        ),
        network=NetworkPolicy(allow_outbound=False),
        timeout_ms=60000,
    )

    # 模拟多次执行
    executions = [
        ("agent-coder-001", 'python -c "print(\'Compiling code...\')"'),
        ("agent-coder-001", 'python -c "print(\'Running tests...\')"'),
        ("agent-reviewer-002", 'python -c "print(\'Reviewing PR...\')"'),
    ]

    print("\n[模拟审计日志记录]")
    for agent_id, command in executions:
        # 模拟执行结果
        result = SandboxResult(
            exit_code=0,
            stdout="Success",
            stderr="",
            duration_ms=234.5,
            config_json="{}",
            backend="processcontainer",
        )

        entry = audit.log_execution(
            result=result,
            command=command,
            policy_dict=policy.to_sdk_dict(),
            agent_id=agent_id,
            metadata={"task": "code-execution", "priority": "normal"},
        )
        print(f"  ✅ {entry.timestamp[:19]} | Agent: {agent_id:<20} | "
              f"Exit: {entry.exit_code} | Duration: {entry.duration_ms:.0f}ms")

    # 显示审计摘要
    print("\n[审计摘要]")
    summary = audit.summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")

    # 显示完整审计条目示例
    print("\n[审计条目示例（JSON 格式）]")
    if audit.entries:
        print(json.dumps(asdict(audit.entries[0]), indent=2, ensure_ascii=False))


def example_compliance_report():
    """
    合规性报告 — 生成面向安全团队的审计摘要。

    结合 Agent 365 的 observability 能力，
    展示如何从审计日志生成合规性报告。

    来源: Windows Blog — "observability, governance and security capabilities"
    """
    print("\n" + "=" * 60)
    print("场景 4: 合规性报告生成")
    print("=" * 60)

    audit = AuditLogger()

    # 模拟一周的执行记录
    agents = ["coding-agent-01", "data-agent-02", "review-agent-03"]
    backends = ["processcontainer", "processcontainer", "isolation_session"]

    for i in range(15):
        agent_idx = i % len(agents)
        exit_code = 0 if i % 7 != 0 else 1  # 模拟偶发失败

        result = SandboxResult(
            exit_code=exit_code,
            stdout=f"Output {i}",
            stderr="Error" if exit_code != 0 else "",
            duration_ms=100.0 + i * 50,
            config_json="{}",
            backend=backends[agent_idx],
        )
        audit.log_execution(
            result=result,
            command=f'python -c "task_{i}"',
            policy_dict={"version": MXC_SCHEMA_VERSION},
            agent_id=agents[agent_idx],
            metadata={"week": "2026-W23"},
        )

    summary = audit.summary()

    print("""
┌──────────────────────────────────────────────────────┐
│           MXC Agent 执行合规性周报                      │
│           Week: 2026-W23                              │
├──────────────────────────────────────────────────────┤""")
    print(f"│  总执行次数:    {summary['total_executions']:<40}│")
    print(f"│  成功次数:      {summary['success_count']:<40}│")
    print(f"│  失败次数:      {summary['failure_count']:<40}│")
    success_rate = (summary['success_count'] / summary['total_executions'] * 100) if summary['total_executions'] > 0 else 0
    print(f"│  成功率:        {success_rate:.1f}%{'':<36}│")
    print(f"│  总耗时:        {summary['total_duration_ms']:.0f}ms{'':<33}│")
    print(f"│  使用的后端:    {', '.join(summary['backends_used']):<40}│")
    print(f"│  活跃 Agent:    {len(summary['agents'])}{'':<38}│")
    print("""├──────────────────────────────────────────────────────┤
│  合规状态:  ✅ SOC2 审计日志要求已满足                    │
│  建议:     检查失败任务的策略配置                         │
└──────────────────────────────────────────────────────┘""")


def main():
    """运行所有审计日志示例"""
    print("MXC 审计日志功能示例")
    print("=" * 60)
    print("\n本示例演示 MXC 的审计和诊断能力：")
    print("  1. Debug 模式诊断日志")
    print("  2. ETW 事件追踪（Windows 平台）")
    print("  3. 应用层审计日志")
    print("  4. 合规性报告生成\n")

    example_debug_mode()
    example_etw_concept()
    example_audit_logger()
    example_compliance_report()

    print("\n" + "=" * 60)
    print("示例 05 完成 ✓")
    print("=" * 60)
    print("\n关键要点:")
    print("  1. --debug 标志提供详细的执行过程诊断")
    print("  2. ETW 提供 Windows 内核级执行遥测（高性能、低开销）")
    print("  3. 应用层审计日志记录完整的执行上下文和策略")
    print("  4. 结构化日志支持 SOC2/GDPR 等合规框架审计要求")
    print("  5. Agent 365 提供企业级 observability 集成")


if __name__ == "__main__":
    main()
