"""
示例 02: 只读访问配置 (Read-Only Access)

演示 MXC 文件系统策略的精细化权限控制：
  1. readonlyPaths — Agent 可读取源码但不能修改
  2. readwritePaths — 仅允许写入指定输出目录
  3. deniedPaths — 完全禁止访问敏感目录
  4. tempDir — 隔离的临时文件空间

核心概念:
  - FilesystemPolicy: 三级路径访问控制（来源: Sandbox Policy Spec v1 §5 — filesystem）
  - Default-Deny: 未声明的路径完全不可访问
  - 路径策略由 SDK 翻译为后端特定的 OS 级强制（如 AppContainer/Bubblewrap bind mount）

⚠️ 已知限制:
  - deniedPaths 在 Windows processcontainer 后端上尚未支持
    （来源: GitHub README — "denied paths not yet supported on Windows"）

参考来源:
  - GitHub: microsoft/mxc — docs/schema.md §Filesystem Policy
  - GitHub: microsoft/mxc — docs/sandbox-policy/v1/policy.md §5
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
    TempDirMode,
    ProcessConfig,
    ContainmentBackend,
    MXC_SCHEMA_VERSION,
)


def example_readonly_source_code():
    """
    场景 1: 代码审查 Agent — 只读访问项目源码。

    Agent 需要读取代码进行审查，但绝不能修改源文件。
    审查结果写入独立的 output 目录。
    """
    print("=" * 60)
    print("场景 1: 代码审查 Agent — 只读源码访问")
    print("=" * 60)

    policy = SandboxPolicy(
        version=MXC_SCHEMA_VERSION,
        filesystem=FilesystemPolicy(
            # 可写: 仅审查报告输出目录
            readwrite_paths=["/workspace/reviews/output"],
            # 只读: 项目源码和依赖
            readonly_paths=[
                "/workspace/project/src",       # 源代码
                "/workspace/project/tests",      # 测试代码
                "/workspace/project/docs",       # 文档
                "/usr/local/lib/python3.12",     # Python 运行时
            ],
            # 拒绝: 敏感配置和密钥
            denied_paths=[
                "/workspace/project/.env",       # 环境变量
                "/workspace/project/secrets",    # 密钥目录
                "/workspace/project/.git",       # Git 仓库（防止篡改历史）
            ],
            temp_dir=TempDirMode.ISOLATED,
        ),
        network=NetworkPolicy(allow_outbound=False),
        ui=UIPolicy(allow_windows=False),
        timeout_ms=120000,  # 2 分钟（代码审查可能较慢）
    )

    client = MxcClient()
    config = client.create_config_from_policy(policy)
    config.process = ProcessConfig(
        command_line='python -c "import os; print(\'Reading source files...\')"',
        cwd="/workspace/project",
    )

    print("\n[文件系统权限映射]")
    print("  📁 可写 (readwrite):")
    for p in policy.filesystem.readwrite_paths:
        print(f"     → {p}")
    print("  📖 只读 (readonly):")
    for p in policy.filesystem.readonly_paths:
        print(f"     → {p}")
    print("  🚫 拒绝 (denied):")
    for p in policy.filesystem.denied_paths:
        print(f"     → {p}")
    print(f"  📦 临时目录: {policy.filesystem.temp_dir.value}")

    print("\n[配置 JSON]")
    print(config.to_json())


def example_data_analysis_readonly():
    """
    场景 2: 数据分析 Agent — 只读访问数据集。

    Agent 需要读取大型数据集进行分析，
    分析结果写入暂存区，原始数据不可修改。
    """
    print("\n" + "=" * 60)
    print("场景 2: 数据分析 Agent — 只读数据集访问")
    print("=" * 60)

    policy = SandboxPolicy(
        version=MXC_SCHEMA_VERSION,
        filesystem=FilesystemPolicy(
            readwrite_paths=[
                "/data/output/reports",          # 分析报告输出
                "/data/output/visualizations",    # 可视化图表
            ],
            readonly_paths=[
                "/data/datasets/sales_2025",      # 销售数据集
                "/data/datasets/customer_stats",   # 客户统计
                "/data/reference/lookup_tables",   # 参考查找表
                "/opt/analytics",                  # 分析工具
            ],
            denied_paths=[
                "/data/datasets/pii_records",      # PII 记录
                "/data/datasets/financial_raw",    # 原始财务数据
                "/data/admin",                      # 管理目录
            ],
            temp_dir=TempDirMode.ISOLATED,
        ),
        network=NetworkPolicy(allow_outbound=False),
        timeout_ms=300000,  # 5 分钟
    )

    client = MxcClient()
    config = client.create_config_from_policy(policy)
    config.process = ProcessConfig(
        command_line='python -c "print(\'Analyzing datasets...\')"',
        cwd="/data",
    )

    print("\n[访问控制矩阵]")
    print(f"  {'路径':<40} {'权限':<10}")
    print(f"  {'─' * 40} {'─' * 10}")
    for p in policy.filesystem.readwrite_paths:
        print(f"  {p:<40} {'读写':<10}")
    for p in policy.filesystem.readonly_paths:
        print(f"  {p:<40} {'只读':<10}")
    for p in policy.filesystem.denied_paths:
        print(f"  {p:<40} {'拒绝':<10}")


def example_minimal_write_access():
    """
    场景 3: 最小写入权限 — 仅临时输出目录。

    展示最小权限原则（Principle of Least Privilege）：
    Agent 仅在隔离的临时目录中有写入权限，
    所有其他路径要么只读、要么拒绝、要么不可访问。
    """
    print("\n" + "=" * 60)
    print("场景 3: 最小写入权限")
    print("=" * 60)

    policy = SandboxPolicy(
        version=MXC_SCHEMA_VERSION,
        filesystem=FilesystemPolicy(
            readwrite_paths=["/tmp/agent-output"],  # 唯一可写路径
            readonly_paths=["/opt/tools"],            # 仅工具目录
            # deniedPaths 省略 — Default-Deny 使所有未声明路径不可访问
        ),
        network=NetworkPolicy(allow_outbound=False),
        ui=UIPolicy(allow_windows=False),
        timeout_ms=30000,
    )

    client = MxcClient()
    config = client.create_config_from_policy(policy)
    config.process = ProcessConfig(
        command_line='python -c "print(\'Minimal write access sandbox\')"',
    )

    print("\n[权限分析]")
    print("  ✅ 可写:  /tmp/agent-output（唯一写入目标）")
    print("  📖 只读:  /opt/tools（工具可执行文件）")
    print("  🚫 不可访问: 所有其他路径（Default-Deny 生效）")
    print("\n  这是 MXC 安全模型的核心：")
    print("  未声明的路径不是 '默认允许'，而是 '默认禁止'。")

    print("\n[配置 JSON]")
    print(config.to_json())


def main():
    """运行所有只读访问示例"""
    print("MXC 只读访问配置示例")
    print("=" * 60)
    print("\n本示例演示 MXC 的三级文件系统权限控制：")
    print("  readwritePaths — 可读可写")
    print("  readonlyPaths  — 只读不可写")
    print("  deniedPaths    — 完全禁止访问")
    print("  (未声明)       — Default-Deny，不可访问\n")

    example_readonly_source_code()
    example_data_analysis_readonly()
    example_minimal_write_access()

    print("\n" + "=" * 60)
    print("示例 02 完成 ✓")
    print("=" * 60)
    print("\n关键要点:")
    print("  1. readonlyPaths 让 Agent 读取源码/数据但不修改")
    print("  2. readwritePaths 应限制为最小输出目录")
    print("  3. deniedPaths 显式阻止敏感路径（⚠️ Windows 上暂不支持）")
    print("  4. tempDir=isolated 提供私有临时空间，避免主机临时文件泄露")
    print("  5. 未声明的路径遵循 Default-Deny，完全不可访问")


if __name__ == "__main__":
    main()
