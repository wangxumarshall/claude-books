# MXC (Microsoft Execution Containers) Python 示例集

> **⚠️ 声明**：本仓库为非官方概念验证示例，非微软官方 SDK。
> MXC 当前处于 Early Preview 阶段（Schema 0.6.0-alpha），API 可能在未来版本中变化。

## 项目概述

[Microsoft Execution Containers (MXC)](https://github.com/microsoft/mxc) 是微软在 Build 2026 发布的跨平台、策略驱动沙箱执行系统，用于在 Windows、Linux 和 macOS 上安全执行不受信任的代码（AI 模型输出、插件、工具）。

本仓库提供 Python 示例代码，演示 MXC 的核心概念和 API 用法，包括：

- 基础沙箱创建和代码执行
- 文件系统只读/读写/拒绝访问控制
- 网络访问限制（出站/入站/代理）
- Agent 身份管理和会话隔离
- 审计日志和合规追踪
- 策略即代码（Policy-as-Code）模式
- OpenClaw 集成示例

## 前置要求

| 依赖项 | 版本要求 | 说明 |
|--------|----------|------|
| Python | ≥ 3.10 | 示例代码使用 dataclass 和类型注解 |
| Node.js | ≥ 18 | MXC TypeScript SDK 运行时依赖 |
| MXC 原生二进制 | 最新 | `wxc-exec.exe` (Windows) / `lxc-exec` (Linux) / `mxc-exec-mac` (macOS) |
| pip | 最新 | Python 包管理器 |

### 安装 MXC

```bash
# Windows
build.bat                    # Release 构建
# Linux
./build.sh                   # Release 构建
# macOS
./build-mac.sh               # Release 构建
```

详见 [MXC 构建说明](https://github.com/microsoft/mxc#building)。

### 安装 Python 依赖

```bash
pip install -r requirements.txt
```

## 目录结构

```
mxc-examples/
├── mxc.py                              # 核心 Python 包装器模块
├── requirements.txt                    # Python 依赖
├── README.md                           # 本文件
├── examples/
│   ├── 01_basic_sandbox.py             # 基础沙箱使用
│   ├── 02_read_only_access.py          # 只读文件系统访问
│   ├── 03_network_restrictions.py      # 网络限制配置
│   ├── 04_agent_identity.py            # Agent 身份管理
│   ├── 05_audit_logging.py             # 审计日志功能
│   ├── 06_policy_as_code.py            # 策略即代码模式
│   └── 07_openclaw_integration.py      # OpenClaw 集成
└── policies/
    ├── code_execution_policy.yaml      # 代码执行策略
    ├── data_access_policy.yaml         # 数据访问策略
    └── enterprise_policy.yaml          # 企业级综合策略
```

## 快速开始

```python
from mxc import MxcClient, SandboxPolicy, FilesystemPolicy, NetworkPolicy

client = MxcClient()

# 创建策略：只读访问工作目录，禁止网络
policy = SandboxPolicy(
    filesystem=FilesystemPolicy(readonly_paths=["./workspace"]),
    network=NetworkPolicy(allow_outbound=False),
    timeout_ms=30000,
)

# 执行代码
result = client.spawn_sandbox('python -c "print(\'Hello MXC!\')"', policy)
print(f"退出码: {result.exit_code}")
print(f"输出: {result.stdout}")
```

## 示例说明

| # | 文件 | 描述 | MXC 核心概念 |
|---|------|------|--------------|
| 1 | `01_basic_sandbox.py` | 最基础的沙箱创建 | SandboxPolicy, Default-Deny |
| 2 | `02_read_only_access.py` | 文件系统权限控制 | readonlyPaths, readwritePaths, deniedPaths |
| 3 | `03_network_restrictions.py` | 网络访问限制（4 种场景） | allowOutbound, allowedHosts, proxy |
| 4 | `04_agent_identity.py` | Agent 身份和会话隔离 | StatefulSandbox, isolation_session |
| 5 | `05_audit_logging.py` | 审计日志和诊断 | AuditLogger, ETW |
| 6 | `06_policy_as_code.py` | YAML 策略加载和执行 | load_policy_from_yaml |
| 7 | `07_openclaw_integration.py` | OpenClaw 集成模式 | 多沙箱编排 |

## 策略文件说明

| 文件 | 用途 | 适用场景 |
|------|------|----------|
| `code_execution_policy.yaml` | 编程 Agent 标准隔离 | 代码生成和执行 |
| `data_access_policy.yaml` | 数据处理 Agent 受控访问 | 数据分析和处理 |
| `enterprise_policy.yaml` | 企业级多角色综合策略 | 企业 Agent 平台 |

## mxc.py 模块 API

### 核心类

| 类名 | 说明 | 对应 SDK |
|------|------|----------|
| `SandboxPolicy` | 安全意图策略 | `SandboxPolicy` type |
| `FilesystemPolicy` | 文件系统策略 | `filesystem` 字段 |
| `NetworkPolicy` | 网络策略 | `network` 字段 |
| `UIPolicy` | UI 策略 | `ui` 字段 |
| `ContainerConfig` | 后端特定配置 | `ContainerConfig` |
| `MxcClient` | 客户端主入口 | SDK 导出函数集合 |
| `StatefulSandbox` | 有状态沙箱生命周期 | State-aware API |
| `AuditLogger` | 审计日志记录器 | ETW 诊断扩展 |

### 辅助函数

| 函数 | 说明 |
|------|------|
| `get_platform_support()` | 检测平台 MXC 支持情况 |
| `get_available_tools_policy()` | 自动发现工具路径 |
| `get_temporary_files_policy()` | 获取临时目录策略 |
| `get_user_profile_policy()` | 获取用户配置目录策略 |
| `load_policy_from_yaml()` | 从 YAML 加载策略 |

## 参考链接

- **GitHub 仓库**: https://github.com/microsoft/mxc
- **Windows Developer Blog**: https://blogs.windows.com/windowsdeveloper/2026/06/02/windows-platform-security-for-ai-agents/
- **Schema 文档**: https://github.com/microsoft/mxc/blob/main/docs/schema.md
- **策略规范**: https://github.com/microsoft/mxc/blob/main/docs/sandbox-policy/v1/policy.md
- **SDK 文档**: https://github.com/microsoft/mxc/tree/main/sdk

### 学术论文

- **AgentBound** (arXiv:2510.21236): MCP 服务器访问控制框架
- **Parallax** (arXiv:2604.12986): AI Agent 执行安全的架构分析
- **AgentBay** (arXiv:2512.04367): 混合交互沙箱系统

## 许可证

本示例代码遵循与 MXC 主仓库相同的许可协议。详见 [MXC LICENSE](https://github.com/microsoft/mxc/blob/main/LICENSE.md)。
