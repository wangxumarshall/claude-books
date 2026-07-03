"""
示例 07: OpenClaw 集成 (OpenClaw Integration)

演示 OpenClaw 与 MXC 的集成模式：
  1. OpenClaw 节点 (Node) 安全执行
  2. OpenClaw 网关 (Gateway) 安全执行
  3. 多沙箱编排和通信隔离

核心概念:
  - OpenClaw 集成: "OpenClaw now runs the node and gateway securely on Windows
    leveraging MXC" （来源: Windows Blog Build 2026）
  - 多沙箱编排: 不同组件使用不同的隔离策略
  - 最小权限: 每个组件仅获得运行所需的最小权限

背景:
  OpenClaw 是一个 AI Agent 框架，其 Windows 伴侣应用使用 MXC
  来安全运行节点和网关组件。MXC 提供策略驱动的隔离，确保
  Agent 操作在企业环境中安全可控。

参考来源:
  - Windows Blog: Build 2026 — "OpenClaw now runs the node and gateway securely on Windows leveraging MXC"
  - GitHub: microsoft/mxc — 多后端支持
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mxc import (
    MxcClient,
    SandboxPolicy,
    FilesystemPolicy,
    NetworkPolicy,
    UIPolicy,
    ClipboardAccess,
    ProcessConfig,
    StatefulSandbox,
    ContainmentBackend,
    AuditLogger,
    MXC_SCHEMA_VERSION,
)


def create_node_policy() -> SandboxPolicy:
    """
    创建 OpenClaw 节点的隔离策略。

    节点 (Node) 负责执行 AI Agent 的具体任务：
      - 运行模型推理
      - 执行工具调用
      - 处理数据

    安全要求:
      - 只读访问模型文件和工具
      - 可写访问工作目录
      - 仅允许访问授权 API 端点
      - 无 UI 访问
    """
    return SandboxPolicy(
        version=MXC_SCHEMA_VERSION,
        filesystem=FilesystemPolicy(
            readwrite_paths=[
                "/openclaw/node/workspace",      # 工作目录
                "/openclaw/node/cache",           # 缓存目录
                "/tmp/openclaw-node",             # 临时文件
            ],
            readonly_paths=[
                "/openclaw/node/models",          # 模型文件（不可修改）
                "/openclaw/node/tools",           # 工具脚本
                "/openclaw/node/config",          # 配置文件
                "/usr/local/lib/python3.12",      # Python 运行时
            ],
            denied_paths=[
                "/openclaw/gateway",              # 不能访问网关目录
                "/etc",                           # 系统配置
                "/root",                          # root 目录
            ],
        ),
        network=NetworkPolicy(
            allow_outbound=True,
            allow_local_network=True,
            allowed_hosts=[
                "api.openai.com",                 # OpenAI API
                "api.anthropic.com",              # Anthropic API
                "localhost",                      # 本地网关通信
            ],
        ),
        ui=UIPolicy(
            allow_windows=False,
            clipboard=ClipboardAccess.NONE,
            allow_input_injection=False,
        ),
        timeout_ms=300000,  # 5 分钟
    )


def create_gateway_policy() -> SandboxPolicy:
    """
    创建 OpenClaw 网关的隔离策略。

    网关 (Gateway) 负责：
      - 接收外部请求
      - 路由到节点
      - 管理会话状态
      - 聚合结果

    安全要求:
      - 可读写工作目录（状态管理）
      - 受控出站网络（API 和节点通信）
      - 无 UI 访问
    """
    return SandboxPolicy(
        version=MXC_SCHEMA_VERSION,
        filesystem=FilesystemPolicy(
            readwrite_paths=[
                "/openclaw/gateway/state",        # 状态存储
                "/openclaw/gateway/sessions",     # 会话数据
                "/openclaw/gateway/logs",         # 日志
                "/tmp/openclaw-gateway",          # 临时文件
            ],
            readonly_paths=[
                "/openclaw/gateway/config",       # 网关配置
                "/openclaw/gateway/certs",        # TLS 证书
                "/usr/local/lib/python3.12",
            ],
            denied_paths=[
                "/openclaw/node",                 # 不能访问节点目录
                "/etc",
                "/root",
            ],
        ),
        network=NetworkPolicy(
            allow_outbound=True,
            allow_local_network=True,
            allowed_hosts=[
                "localhost",                      # 本地节点通信
                "auth.openclaw.io",               # OpenClaw 认证服务
                "telemetry.openclaw.io",          # 遥测数据
            ],
        ),
        ui=UIPolicy(
            allow_windows=False,
            clipboard=ClipboardAccess.NONE,
            allow_input_injection=False,
        ),
        timeout_ms=600000,  # 10 分钟（网关长运行）
    )


def example_openclaw_node():
    """
    OpenClaw 节点安全执行。

    演示节点组件在 MXC 沙箱中的启动和任务执行。
    """
    print("=" * 60)
    print("场景 1: OpenClaw 节点安全执行")
    print("=" * 60)

    policy = create_node_policy()
    client = MxcClient(debug=True)
    config = client.create_config_from_policy(policy)
    config.process = ProcessConfig(
        command_line='python -S -B -c "print(\'OpenClaw Node: Ready for tasks\')"',
        cwd="/openclaw/node",
        env=["OPENCLAW_ROLE=node", "OPENCLAW_LOG_LEVEL=info"],
    )

    print("\n[OpenClaw 节点配置]")
    print(f"  后端:     {config.containment}")
    print(f"  工作目录: /openclaw/node")
    print(f"  超时:     {policy.timeout_ms}ms")

    print("\n[文件系统权限]")
    print("  📁 可写:")
    for p in policy.filesystem.readwrite_paths:
        print(f"     → {p}")
    print("  📖 只读:")
    for p in policy.filesystem.readonly_paths:
        print(f"     → {p}")
    print("  🚫 拒绝:")
    for p in policy.filesystem.denied_paths:
        print(f"     → {p}")

    print("\n[网络访问]")
    print(f"  允许的主机:")
    for h in policy.network.allowed_hosts:
        print(f"     ✅ {h}")

    print(f"\n[配置 JSON]")
    print(config.to_json())


def example_openclaw_gateway():
    """
    OpenClaw 网关安全执行。

    演示网关组件在 MXC 沙箱中的启动和请求处理。
    """
    print("\n" + "=" * 60)
    print("场景 2: OpenClaw 网关安全执行")
    print("=" * 60)

    policy = create_gateway_policy()
    client = MxcClient()
    config = client.create_config_from_policy(policy)
    config.process = ProcessConfig(
        command_line='python -S -B -c "print(\'OpenClaw Gateway: Listening...\')"',
        cwd="/openclaw/gateway",
        env=["OPENCLAW_ROLE=gateway", "OPENCLAW_PORT=8080"],
    )

    print("\n[OpenClaw 网关配置]")
    print(f"  后端:     {config.containment}")
    print(f"  工作目录: /openclaw/gateway")
    print(f"  超时:     {policy.timeout_ms}ms")

    print("\n[文件系统权限]")
    print("  📁 可写:")
    for p in policy.filesystem.readwrite_paths:
        print(f"     → {p}")
    print("  📖 只读:")
    for p in policy.filesystem.readonly_paths:
        print(f"     → {p}")

    print("\n[网络访问]")
    print(f"  允许的主机:")
    for h in policy.network.allowed_hosts:
        print(f"     ✅ {h}")


def example_multi_sandbox_orchestration():
    """
    多沙箱编排 — 同时管理网关和多个节点。

    展示企业环境中 OpenClaw 的完整部署模式：
      - 1 个网关沙箱（长运行，处理请求路由）
      - N 个节点沙箱（按需创建，执行任务）
      - 审计日志追踪所有组件
    """
    print("\n" + "=" * 60)
    print("场景 3: 多沙箱编排")
    print("=" * 60)

    client = MxcClient()
    audit = AuditLogger()

    print("""
[OpenClaw 多沙箱编排架构]

  ┌─────────────────────────────────────────────────────────┐
  │                    外部请求                              │
  │                      │                                  │
  │                      ▼                                  │
  │  ┌───────────────────────────────────────────────┐      │
  │  │  Gateway Sandbox (MXC isolation_session)      │      │
  │  │  - 接收和路由请求                              │      │
  │  │  - 管理会话状态                                │      │
  │  │  - 聚合结果                                    │      │
  │  └──────┬──────────┬──────────┬──────────────────┘      │
  │         │          │          │                          │
  │         ▼          ▼          ▼                          │
  │  ┌──────────┐┌──────────┐┌──────────┐                   │
  │  │ Node 1   ││ Node 2   ││ Node 3   │                   │
  │  │ Sandbox  ││ Sandbox  ││ Sandbox  │                   │
  │  │ (MXC     ││ (MXC     ││ (MXC     │                   │
  │  │ process) ││ process) ││ microvm) │                   │
  │  │          ││          ││          │                   │
  │  │ 推理任务 ││ 工具调用 ││ 敏感数据 │                   │
  │  └──────────┘└──────────┘└──────────┘                   │
  └─────────────────────────────────────────────────────────┘
""")

    # 模拟网关生命周期
    gw_policy = create_gateway_policy()
    gateway = StatefulSandbox(client, gw_policy)
    gateway.provision(ContainmentBackend.PROCESS)
    gateway.start()

    gw_result = gateway.exec_async(
        'python -c "print(\'Gateway started, ready for connections\')"',
        env=["OPENCLAW_ROLE=gateway"],
    )
    audit.log_execution(
        gw_result, "gateway-start", gw_policy.to_sdk_dict(),
        agent_id="openclaw-gateway-001",
        metadata={"component": "gateway"},
    )
    print("[网关] 启动完成 — 等待请求")

    # 模拟节点任务分发
    node_tasks = [
        ("推理任务", "process", 'python -c "print(\'Running inference...\')"'),
        ("工具调用", "process", 'python -c "print(\'Executing tool...\')"'),
        ("敏感数据处理", "microvm", 'python -c "print(\'Processing sensitive data...\')"'),
    ]

    print("\n[节点任务执行]")
    for i, (task_name, backend, cmd) in enumerate(node_tasks, 1):
        node_policy = create_node_policy()
        node = StatefulSandbox(client, node_policy)

        containment = ContainmentBackend.PROCESS if backend == "process" else ContainmentBackend.MICROVM
        node.provision(containment)
        node.start()

        result = node.exec_async(cmd, env=[f"OPENCLAW_TASK={task_name}"])
        audit.log_execution(
            result, f"node-task-{i}", node_policy.to_sdk_dict(),
            agent_id=f"openclaw-node-{i:03d}",
            metadata={"component": "node", "task": task_name, "backend": backend},
        )

        print(f"  节点 {i} [{backend:<10}] {task_name}: exit_code={result.exit_code}")

        node.stop()
        node.deprovision()

    # 关闭网关
    gateway.stop()
    gateway.deprovision()

    # 审计摘要
    print(f"\n[编排审计摘要]")
    summary = audit.summary()
    print(f"  总执行:  {summary['total_executions']}")
    print(f"  成功:    {summary['success_count']}")
    print(f"  Agent:   {', '.join(summary['agents'])}")
    print(f"  后端:    {', '.join(summary['backends_used'])}")


def main():
    """运行所有 OpenClaw 集成示例"""
    print("MXC OpenClaw 集成示例")
    print("=" * 60)
    print("\n本示例演示 OpenClaw 与 MXC 的集成模式：")
    print("  1. OpenClaw 节点安全执行")
    print("  2. OpenClaw 网关安全执行")
    print("  3. 多沙箱编排和审计\n")
    print("背景: Windows Blog Build 2026 —")
    print('  "OpenClaw now runs the node and gateway securely on Windows')
    print('   leveraging MXC."\n')

    example_openclaw_node()
    example_openclaw_gateway()
    example_multi_sandbox_orchestration()

    print("\n" + "=" * 60)
    print("示例 07 完成 ✓")
    print("=" * 60)
    print("\n关键要点:")
    print("  1. OpenClaw 节点和网关各自使用独立的 MXC 策略")
    print("  2. 节点使用最小权限：只读模型、受限网络")
    print("  3. 网关负责路由和状态管理，有独立的文件系统和网络权限")
    print("  4. 多沙箱编排实现组件级隔离和审计追踪")
    print("  5. 敏感任务可使用 microvm 后端获得硬件级隔离")


if __name__ == "__main__":
    main()
