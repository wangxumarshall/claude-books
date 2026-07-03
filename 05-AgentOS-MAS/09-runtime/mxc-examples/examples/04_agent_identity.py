"""
示例 04: Agent 身份管理 (Agent Identity)

演示 MXC 的 Agent 身份管理和会话隔离机制：
  1. StatefulSandbox 的完整生命周期
  2. 会话隔离（isolation_session）概念
  3. Agent 独立身份（独立用户帐户）
  4. 多次执行复用沙箱

核心概念:
  - State-aware Lifecycle: provision → start → exec → stop → deprovision
    （来源: docs/state-aware-lifecycle/mxc-state-aware-sandbox-api.md）
  - Session Isolation: 独立用户帐户，分离桌面/剪贴板/输入
    （来源: Windows Blog Build 2026 — Session Isolation 章节）
  - Entra ID 集成: 云身份管理、Intune 策略控制
    （来源: Windows Blog — "Windows assigns a local ID or a cloud provisioned identity backed by Entra"）

参考来源:
  - GitHub: microsoft/mxc — State-aware Sandbox API 文档
  - Windows Blog: Build 2026 — Session Isolation
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
    ClipboardAccess,
    ProcessConfig,
    StatefulSandbox,
    ContainmentBackend,
    AuditLogger,
    MXC_SCHEMA_VERSION,
)


def example_stateful_lifecycle():
    """
    演示 StatefulSandbox 的完整生命周期。

    五步流程:
      1. provision — 分配资源，选择隔离后端
      2. start — 创建隔离环境
      3. exec (可多次) — 在沙箱中执行命令
      4. stop — 终止所有进程
      5. deprovision — 释放资源

    对应 TypeScript SDK:
      const sandbox = await provisionSandbox(policy, options);
      await startSandbox(sandbox);
      const result = await execInSandboxAsync(sandbox, command);
      await stopSandbox(sandbox);
      await deprovisionSandbox(sandbox);
    """
    print("=" * 60)
    print("场景 1: StatefulSandbox 完整生命周期")
    print("=" * 60)

    client = MxcClient(debug=True)

    policy = SandboxPolicy(
        version=MXC_SCHEMA_VERSION,
        filesystem=FilesystemPolicy(
            readwrite_paths=["/workspace/output"],
            readonly_paths=["/workspace/src"],
        ),
        network=NetworkPolicy(allow_outbound=False),
        timeout_ms=60000,
    )

    sandbox = StatefulSandbox(client, policy)

    # 步骤 1: Provision
    print(f"\n[步骤 1] provision — 当前状态: {sandbox.state}")
    config = sandbox.provision(ContainmentBackend.PROCESS)
    print(f"  状态: {sandbox.state}")
    print(f"  后端: {config.containment}")

    # 步骤 2: Start
    print(f"\n[步骤 2] start — 当前状态: {sandbox.state}")
    sandbox.start()
    print(f"  状态: {sandbox.state}")

    # 步骤 3: 多次执行
    commands = [
        'python -c "print(\'Execution 1: Hello from sandbox!\')"',
        'python -c "import os; print(f\'Execution 2: PID={os.getpid()}\')"',
        'python -c "print(\'Execution 3: Computation result: \', 42 * 73)"',
    ]

    for i, cmd in enumerate(commands, 1):
        print(f"\n[步骤 3.{i}] exec — 执行命令 #{i}")
        result = sandbox.exec_async(cmd)
        print(f"  退出码: {result.exit_code}")
        print(f"  输出:   {result.stdout.strip() or '(dry-run: 无实际输出)'}")
        print(f"  耗时:   {result.duration_ms:.1f}ms")

    print(f"\n  总执行次数: {sandbox.execution_count}")

    # 步骤 4: Stop
    print(f"\n[步骤 4] stop — 当前状态: {sandbox.state}")
    sandbox.stop()
    print(f"  状态: {sandbox.state}")

    # 步骤 5: Deprovision
    print(f"\n[步骤 5] deprovision — 当前状态: {sandbox.state}")
    sandbox.deprovision()
    print(f"  状态: {sandbox.state}")


def example_context_manager():
    """
    使用上下文管理器简化生命周期管理。

    StatefulSandbox 支持 Python with 语句，
    自动管理 provision/start 和 stop/deprovision。
    """
    print("\n" + "=" * 60)
    print("场景 2: 上下文管理器（with 语句）")
    print("=" * 60)

    client = MxcClient()
    policy = SandboxPolicy(
        version=MXC_SCHEMA_VERSION,
        filesystem=FilesystemPolicy(
            readwrite_paths=["/workspace/output"],
        ),
        network=NetworkPolicy(allow_outbound=False),
        timeout_ms=30000,
    )

    print("\n[使用 with 语句自动管理生命周期]")
    print("  with StatefulSandbox(client, policy) as sandbox:")
    print("      result = sandbox.exec_async(command)")

    with StatefulSandbox(client, policy) as sandbox:
        print(f"\n  进入 with 块 — 状态: {sandbox.state}")

        result = sandbox.exec_async(
            'python -c "print(\'Context manager sandbox!\')"'
        )
        print(f"  执行结果: exit_code={result.exit_code}")

    print(f"  退出 with 块 — 自动 stop + deprovision")
    print(f"  最终状态: {sandbox.state}")


def example_session_isolation_concept():
    """
    会话隔离概念演示。

    Session Isolation 是 MXC 的高级隔离模式：
      - Agent 运行在独立的用户会话中
      - 与人类用户的桌面/剪贴板/输入设备完全分离
      - 独立身份（本地 ID 或 Entra 云身份）
      - 防止 UI 欺骗、输入注入、跨会话数据泄露

    来源: Windows Blog Build 2026 — Session Isolation 章节:
    "Sessions in Windows separate the agent's execution from the human user's
     environment, such as the interactive desktop, clipboard, UI, input devices
     and active sessions."
    """
    print("\n" + "=" * 60)
    print("场景 3: 会话隔离概念")
    print("=" * 60)

    print("""
[会话隔离架构]

  ┌─────────────────────────────────────────────────┐
  │  Windows Session                                │
  │                                                 │
  │  ┌──────────────────┐  ┌──────────────────────┐ │
  │  │  用户会话         │  │  Agent 会话           │ │
  │  │  (Human Session)  │  │  (Agent Session)     │ │
  │  │                   │  │                      │ │
  │  │  - 交互式桌面     │  │  - 独立桌面          │ │
  │  │  - 剪贴板         │  │  - 独立剪贴板        │ │
  │  │  - 输入设备       │  │  - 无输入注入        │ │
  │  │  - 用户身份       │  │  - Agent 独立身份    │ │
  │  │  (Entra ID)      │  │  (Local ID / Entra)  │ │
  │  └──────────────────┘  └──────────────────────┘ │
  │                                                 │
  │  ──── 会话间隔离边界 ────                        │
  │  防止: UI 欺骗、输入注入、跨会话数据泄露         │
  └─────────────────────────────────────────────────┘
""")

    # 演示隔离会话的策略配置
    policy = SandboxPolicy(
        version=MXC_SCHEMA_VERSION,
        filesystem=FilesystemPolicy(
            readwrite_paths=["/agent-workspace/output"],
            readonly_paths=["/agent-workspace/tools"],
        ),
        network=NetworkPolicy(
            allow_outbound=True,
            allowed_hosts=["api.internal.corp"],
        ),
        ui=UIPolicy(
            allow_windows=False,         # 非交互式
            clipboard=ClipboardAccess.NONE,  # 无剪贴板
            allow_input_injection=False,  # 无输入注入
        ),
        timeout_ms=600000,  # 10 分钟（长时间运行的任务）
    )

    client = MxcClient()
    config = client.create_config_from_policy(
        policy,
        containment=ContainmentBackend.ISOLATION_SESSION,
    )

    print("[会话隔离策略]")
    print(f"  后端:        {config.containment}")
    print(f"  UI 隔离:     完全分离")
    print(f"  剪贴板:      {policy.ui.clipboard.value}")
    print(f"  输入注入:    {policy.ui.allow_input_injection}")
    print(f"  超时:        {policy.timeout_ms}ms")
    print(f"\n[身份管理（来源: Windows Blog）]")
    print(f"  - Windows 为容器分配本地 ID")
    print(f"  - 或使用 Entra 云身份")
    print(f"  - 所有活动归因于 Agent 身份")
    print(f"  - 人类 vs Agent 清晰区分")
    print(f"  - Intune 策略可强制 MXC 隔离要求")


def main():
    """运行所有 Agent 身份管理示例"""
    print("MXC Agent 身份管理示例")
    print("=" * 60)
    print("\n本示例演示 MXC 的 Agent 身份和隔离机制：")
    print("  1. StatefulSandbox 生命周期管理")
    print("  2. 上下文管理器简化用法")
    print("  3. 会话隔离和独立身份\n")

    example_stateful_lifecycle()
    example_context_manager()
    example_session_isolation_concept()

    print("\n" + "=" * 60)
    print("示例 04 完成 ✓")
    print("=" * 60)
    print("\n关键要点:")
    print("  1. StatefulSandbox 提供 provision→start→exec→stop→deprovision 生命周期")
    print("  2. 多次 exec 复用同一沙箱，避免重复创建开销")
    print("  3. 会话隔离（isolation_session）提供独立用户会话和身份")
    print("  4. Entra ID + Intune 实现企业级 Agent 身份治理")
    print("  5. 会话隔离防止 UI 欺骗和跨会话数据泄露")


if __name__ == "__main__":
    main()
