"""
MXC (Microsoft Execution Containers) Python SDK — 概念验证包装器

本模块将 @microsoft/mxc-sdk (TypeScript) 的核心概念翻译为 Python API，
提供 Python 开发者友好的接口来创建、配置和管理 MXC 沙箱。

MXC 是微软在 Build 2026 发布的跨平台、策略驱动沙箱执行系统，
用于在 Windows/Linux/macOS 上安全执行不受信任的代码（模型输出、插件、工具）。

参考来源:
  - GitHub: https://github.com/microsoft/mxc
  - Windows Developer Blog: https://blogs.windows.com/windowsdeveloper/2026/06/02/windows-platform-security-for-ai-agents/
  - Schema: schemas/stable/mxc-config.schema.0.6.0-alpha.json
  - Policy Spec: docs/sandbox-policy/v1/policy.md

⚠️ 本模块为非官方概念验证，非微软官方 SDK。
MXC 当前处于 Early Preview 阶段，API 可能在 minor 版本间变化。
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# ---------------------------------------------------------------------------
# 常量与枚举
# ---------------------------------------------------------------------------

MXC_SCHEMA_VERSION = "0.6.0-alpha"
"""当前稳定的 MXC 配置 Schema 版本（来源: GitHub schemas/stable/）"""


class ContainmentBackend(str, Enum):
    """
    容器后端类型。

    来源: GitHub README — Containment Backends 表格
    """
    # 抽象意图值（由运行时按平台解析）
    PROCESS = "process"          # Windows→processcontainer, Linux→lxc, macOS→seatbelt
    VM = "vm"                    # Windows→windows_sandbox
    MICROVM = "microvm"          # Windows→NanVix via HyperV Platform

    # 具体后端
    PROCESS_CONTAINER = "processcontainer"   # Windows 默认 (AppContainer/BaseContainer)
    WINDOWS_SANDBOX = "windows_sandbox"      # VM 级隔离
    WSLC = "wslc"                            # WSL 容器
    LXC = "lxc"                              # Linux LXC 容器
    SEATBELT = "seatbelt"                    # macOS Seatbelt
    BUBBLEWRAP = "bubblewrap"                # Linux 非特权沙箱
    HYPERLIGHT = "hyperlight"                # Hyperlight microVM
    ISOLATION_SESSION = "isolation_session"  # Windows 会话隔离


class ClipboardAccess(str, Enum):
    """剪贴板访问级别（来源: Sandbox Policy Spec v1 — ui.clipboard）"""
    NONE = "none"
    READ = "read"
    WRITE = "write"
    READWRITE = "readwrite"


class TempDirMode(str, Enum):
    """临时目录模式（来源: Sandbox Policy Spec v1 — filesystem.tempDir）"""
    SHARED = "shared"        # 使用主机临时目录
    ISOLATED = "isolated"    # 使用隔离的私有临时目录


class NetworkDefaultPolicy(str, Enum):
    """网络默认策略（来源: schema.md — network.defaultPolicy）"""
    ALLOW = "allow"
    BLOCK = "block"


# ---------------------------------------------------------------------------
# 策略 Dataclass（对应 SandboxPolicy — 用户面向的安全意图）
# ---------------------------------------------------------------------------

@dataclass
class FilesystemPolicy:
    """
    文件系统策略。

    来源: Sandbox Policy Spec v1 §5 — filesystem
    ⚠️ deniedPaths 在 Windows 上尚未支持（来源: GitHub README 已知限制）
    """
    readwrite_paths: List[str] = field(default_factory=list)
    readonly_paths: List[str] = field(default_factory=list)
    denied_paths: List[str] = field(default_factory=list)
    temp_dir: Optional[TempDirMode] = None

    def to_sdk_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}
        if self.readwrite_paths:
            d["readwritePaths"] = self.readwrite_paths
        if self.readonly_paths:
            d["readonlyPaths"] = self.readonly_paths
        if self.denied_paths:
            d["deniedPaths"] = self.denied_paths
        if self.temp_dir:
            d["tempDir"] = self.temp_dir.value
        return d


@dataclass
class NetworkPolicy:
    """
    网络策略。所有标志默认为 False（无网络访问）。

    来源: Sandbox Policy Spec v1 §5 — network
    ⚠️ allowedHosts/blockedHosts 在 Windows 上尚未支持
    ⚠️ proxy 在 macOS 上不支持
    """
    allow_outbound: bool = False
    allow_local_network: bool = False
    allowed_hosts: List[str] = field(default_factory=list)
    blocked_hosts: List[str] = field(default_factory=list)
    proxy: Optional[Dict[str, Any]] = None

    def to_sdk_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}
        if self.allow_outbound:
            d["allowOutbound"] = True
        if self.allow_local_network:
            d["allowLocalNetwork"] = True
        if self.allowed_hosts:
            d["allowedHosts"] = self.allowed_hosts
        if self.blocked_hosts:
            d["blockedHosts"] = self.blocked_hosts
        if self.proxy:
            d["proxy"] = self.proxy
        return d


@dataclass
class UIPolicy:
    """
    UI 策略。所有标志默认为最限制性设置。

    来源: Sandbox Policy Spec v1 §5 — ui
    """
    allow_windows: bool = False
    clipboard: ClipboardAccess = ClipboardAccess.NONE
    allow_input_injection: bool = False

    def to_sdk_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}
        if self.allow_windows:
            d["allowWindows"] = True
        if self.clipboard != ClipboardAccess.NONE:
            d["clipboard"] = self.clipboard.value
        if self.allow_input_injection:
            d["allowInputInjection"] = True
        return d


@dataclass
class SandboxPolicy:
    """
    沙箱策略 — 用户面向的安全意图输入。

    描述调用者希望限制什么，不包含任何操作系统特定内容。
    遵循 Default-Deny 原则：省略的策略字段 = 最严格权限。

    来源: Sandbox Policy Spec v1 §5 — SandboxPolicy 完整定义
    """
    version: str = MXC_SCHEMA_VERSION
    filesystem: Optional[FilesystemPolicy] = None
    network: Optional[NetworkPolicy] = None
    ui: Optional[UIPolicy] = None
    timeout_ms: Optional[int] = None

    def to_sdk_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {"version": self.version}
        if self.filesystem:
            d["filesystem"] = self.filesystem.to_sdk_dict()
        if self.network:
            d["network"] = self.network.to_sdk_dict()
        if self.ui:
            d["ui"] = self.ui.to_sdk_dict()
        if self.timeout_ms is not None:
            d["timeoutMs"] = self.timeout_ms
        return d


# ---------------------------------------------------------------------------
# 容器配置 Dataclass（对应 ContainerConfig — 后端特定配置）
# ---------------------------------------------------------------------------

@dataclass
class ProcessConfig:
    """进程执行配置（来源: schema.md — process 节）"""
    command_line: str = ""
    cwd: Optional[str] = None
    env: List[str] = field(default_factory=list)
    timeout: int = 0  # 毫秒，0=无超时

    def to_sdk_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {"commandLine": self.command_line}
        if self.cwd:
            d["cwd"] = self.cwd
        if self.env:
            d["env"] = self.env
        if self.timeout:
            d["timeout"] = self.timeout
        return d


@dataclass
class ContainerConfig:
    """
    容器配置 — createConfigFromPolicy() 的输出，
    传递给 spawnSandboxFromConfig() 的完整后端配置。

    来源: Sandbox Policy Spec v1 §6 — ContainerConfig
    """
    version: str = MXC_SCHEMA_VERSION
    containment: str = "processcontainer"
    container_id: Optional[str] = None
    process: Optional[ProcessConfig] = None
    lifecycle: Optional[Dict[str, Any]] = None
    filesystem: Optional[Dict[str, Any]] = None
    network: Optional[Dict[str, Any]] = None
    ui: Optional[Dict[str, Any]] = None
    process_container: Optional[Dict[str, Any]] = None
    experimental: Optional[Dict[str, Any]] = None
    lxc: Optional[Dict[str, Any]] = None

    def to_json(self) -> str:
        d: Dict[str, Any] = {"version": self.version, "containment": self.containment}
        if self.container_id:
            d["containerId"] = self.container_id
        if self.process:
            d["process"] = self.process.to_sdk_dict()
        if self.lifecycle:
            d["lifecycle"] = self.lifecycle
        if self.filesystem:
            d["filesystem"] = self.filesystem
        if self.network:
            d["network"] = self.network
        if self.ui:
            d["ui"] = self.ui
        if self.process_container:
            d["processContainer"] = self.process_container
        if self.experimental:
            d["experimental"] = self.experimental
        if self.lxc:
            d["lxc"] = self.lxc
        return json.dumps(d, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# 执行结果
# ---------------------------------------------------------------------------

@dataclass
class SandboxResult:
    """沙箱执行结果"""
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: float
    config_json: str
    backend: str


# ---------------------------------------------------------------------------
# 平台支持检测
# ---------------------------------------------------------------------------

@dataclass
class PlatformSupport:
    """平台支持信息"""
    is_supported: bool
    platform: str
    default_backend: str
    available_backends: List[str]
    native_binary: Optional[str]


def get_platform_support() -> PlatformSupport:
    """
    检测当前平台的 MXC 支持情况。

    对应 TypeScript SDK: getPlatformSupport()
    来源: GitHub README — Platforms 表格
    """
    system = platform.system().lower()

    if system == "windows":
        return PlatformSupport(
            is_supported=True,
            platform="windows",
            default_backend="processcontainer",
            available_backends=[
                "processcontainer", "windows_sandbox", "wslc",
                "microvm", "hyperlight", "isolation_session"
            ],
            native_binary="wxc-exec.exe",
        )
    elif system == "linux":
        return PlatformSupport(
            is_supported=True,
            platform="linux",
            default_backend="bubblewrap",
            available_backends=["bubblewrap", "lxc", "microvm", "hyperlight"],
            native_binary="lxc-exec",
        )
    elif system == "darwin":
        return PlatformSupport(
            is_supported=True,
            platform="macos",
            default_backend="seatbelt",
            available_backends=["seatbelt"],
            native_binary="mxc-exec-mac",
        )
    else:
        return PlatformSupport(
            is_supported=False,
            platform=system,
            default_backend="",
            available_backends=[],
            native_binary=None,
        )


# ---------------------------------------------------------------------------
# 策略发现辅助函数
# ---------------------------------------------------------------------------

def get_available_tools_policy(env: Optional[Dict[str, str]] = None) -> FilesystemPolicy:
    """
    获取可用工具路径的文件系统策略。

    对应 TypeScript SDK: getAvailableToolsPolicy(process.env)
    自动发现系统中 Python、Node.js 等工具的安装路径。
    """
    env = env or dict(os.environ)
    readonly: List[str] = []

    # Python 安装路径
    python_home = os.path.dirname(os.path.dirname(sys.executable))
    if os.path.isdir(python_home):
        readonly.append(python_home)

    # Node.js 路径
    node_path = env.get("NODE_PATH", "")
    if node_path and os.path.isdir(node_path):
        readonly.append(node_path)

    return FilesystemPolicy(readonly_paths=readonly)


def get_temporary_files_policy(env: Optional[Dict[str, str]] = None) -> FilesystemPolicy:
    """
    获取临时文件目录的文件系统策略。

    对应 TypeScript SDK: getTemporaryFilesPolicy(process.env)
    """
    env = env or dict(os.environ)
    temp_dir = env.get("TEMP", env.get("TMPDIR", tempfile.gettempdir()))
    return FilesystemPolicy(readwrite_paths=[temp_dir])


def get_user_profile_policy() -> FilesystemPolicy:
    """
    获取用户配置目录的文件系统策略（只读访问）。

    对应 TypeScript SDK: getUserProfilePolicy()
    """
    user_home = Path.home()
    return FilesystemPolicy(readonly_paths=[str(user_home)])


# ---------------------------------------------------------------------------
# YAML 策略加载
# ---------------------------------------------------------------------------

def load_policy_from_yaml(yaml_path: str) -> SandboxPolicy:
    """
    从 YAML 文件加载沙箱策略。

    自定义扩展（TypeScript SDK 不包含此功能），用于 Policy-as-Code 模式。

    Args:
        yaml_path: YAML 策略文件路径

    Returns:
        SandboxPolicy 实例
    """
    try:
        import yaml
    except ImportError:
        raise ImportError("需要安装 pyyaml: pip install pyyaml")

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    policy = SandboxPolicy(
        version=data.get("version", MXC_SCHEMA_VERSION),
        timeout_ms=data.get("timeoutMs"),
    )

    # 解析文件系统策略
    fs_data = data.get("filesystem")
    if fs_data:
        temp_dir = None
        if fs_data.get("tempDir"):
            temp_dir = TempDirMode(fs_data["tempDir"])
        policy.filesystem = FilesystemPolicy(
            readwrite_paths=fs_data.get("readwritePaths", []),
            readonly_paths=fs_data.get("readonlyPaths", []),
            denied_paths=fs_data.get("deniedPaths", []),
            temp_dir=temp_dir,
        )

    # 解析网络策略
    net_data = data.get("network")
    if net_data:
        policy.network = NetworkPolicy(
            allow_outbound=net_data.get("allowOutbound", False),
            allow_local_network=net_data.get("allowLocalNetwork", False),
            allowed_hosts=net_data.get("allowedHosts", []),
            blocked_hosts=net_data.get("blockedHosts", []),
            proxy=net_data.get("proxy"),
        )

    # 解析 UI 策略
    ui_data = data.get("ui")
    if ui_data:
        clipboard = ClipboardAccess.NONE
        if ui_data.get("clipboard"):
            clipboard = ClipboardAccess(ui_data["clipboard"])
        policy.ui = UIPolicy(
            allow_windows=ui_data.get("allowWindows", False),
            clipboard=clipboard,
            allow_input_injection=ui_data.get("allowInputInjection", False),
        )

    return policy


# ---------------------------------------------------------------------------
# MXC 客户端
# ---------------------------------------------------------------------------

class MxcClient:
    """
    MXC 沙箱客户端 — 提供创建和管理沙箱的核心 API。

    对应 TypeScript SDK (@microsoft/mxc-sdk) 的主要导出函数。
    通过 subprocess 调用 MXC 原生二进制（wxc-exec / lxc-exec / mxc-exec-mac）。

    使用方式:
        client = MxcClient()
        policy = SandboxPolicy(
            filesystem=FilesystemPolicy(readonly_paths=["/workspace"]),
            network=NetworkPolicy(allow_outbound=False),
        )
        result = client.spawn_sandbox("python -c 'print(42)'", policy)
    """

    def __init__(
        self,
        binary_path: Optional[str] = None,
        debug: bool = False,
        experimental: bool = False,
    ):
        """
        初始化 MXC 客户端。

        Args:
            binary_path: MXC 原生二进制的路径。如不提供则自动检测。
            debug: 启用调试输出（对应 --debug 标志）
            experimental: 启用实验性后端（对应 --experimental 标志）
        """
        self._platform = get_platform_support()
        self._binary_path = binary_path or self._resolve_binary()
        self._debug = debug
        self._experimental = experimental

    def _resolve_binary(self) -> str:
        """解析原生二进制路径"""
        if not self._platform.is_supported or not self._platform.native_binary:
            raise RuntimeError(
                f"MXC 不支持当前平台: {self._platform.platform}"
            )
        return self._platform.native_binary

    def create_config_from_policy(
        self,
        policy: SandboxPolicy,
        containment: Union[str, ContainmentBackend] = ContainmentBackend.PROCESS,
        container_name: Optional[str] = None,
    ) -> ContainerConfig:
        """
        从策略创建容器配置。

        对应 TypeScript SDK: createConfigFromPolicy(policy, containment?, containerName?)

        Args:
            policy: 沙箱策略
            containment: 容器后端类型
            container_name: 容器名称

        Returns:
            ContainerConfig 实例
        """
        backend = containment.value if isinstance(containment, ContainmentBackend) else containment

        config = ContainerConfig(
            version=policy.version,
            containment=backend,
            container_id=container_name,
        )

        # 映射文件系统策略
        if policy.filesystem:
            config.filesystem = policy.filesystem.to_sdk_dict()

        # 映射网络策略
        if policy.network:
            net = policy.network
            config.network = {
                "defaultPolicy": "block" if not net.allow_outbound else "allow",
                "enforcementMode": "firewall",
            }
            if net.allowed_hosts:
                config.network["allowedHosts"] = net.allowed_hosts
            if net.blocked_hosts:
                config.network["blockedHosts"] = net.blocked_hosts
            if net.proxy:
                config.network["proxy"] = net.proxy

        # 映射 UI 策略
        if policy.ui:
            config.ui = {
                "disable": not policy.ui.allow_windows,
                "clipboard": policy.ui.clipboard.value,
                "injection": policy.ui.allow_input_injection,
            }

        # 生命周期
        config.lifecycle = {"destroyOnExit": True, "preservePolicy": False}

        return config

    def spawn_sandbox(
        self,
        command: str,
        policy: SandboxPolicy,
        containment: Union[str, ContainmentBackend] = ContainmentBackend.PROCESS,
        cwd: Optional[str] = None,
        env: Optional[List[str]] = None,
    ) -> SandboxResult:
        """
        创建并执行沙箱（便捷方式）。

        对应 TypeScript SDK: spawnSandbox(script, policy, ...)

        Args:
            command: 要在沙箱中执行的命令
            policy: 沙箱策略
            containment: 容器后端
            cwd: 工作目录
            env: 环境变量列表（KEY=VALUE 格式）

        Returns:
            SandboxResult 执行结果
        """
        config = self.create_config_from_policy(policy, containment)
        config.process = ProcessConfig(
            command_line=command,
            cwd=cwd,
            env=env or [],
            timeout=policy.timeout_ms or 0,
        )
        return self.spawn_sandbox_from_config(config)

    def spawn_sandbox_from_config(self, config: ContainerConfig) -> SandboxResult:
        """
        从配置创建并执行沙箱。

        对应 TypeScript SDK: spawnSandboxFromConfig(config, options?)

        Args:
            config: 容器配置

        Returns:
            SandboxResult 执行结果
        """
        config_json = config.to_json()
        start_time = time.monotonic()

        # 写入临时配置文件
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", prefix="mxc_", delete=False, encoding="utf-8"
        ) as f:
            f.write(config_json)
            config_path = f.name

        try:
            cmd = [self._binary_path]
            if self._debug:
                cmd.append("--debug")
            if self._experimental:
                cmd.append("--experimental")
            cmd.append(config_path)

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=(config.process.timeout / 1000.0) if config.process and config.process.timeout else 300,
            )

            duration = (time.monotonic() - start_time) * 1000

            return SandboxResult(
                exit_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                duration_ms=duration,
                config_json=config_json,
                backend=config.containment,
            )
        except FileNotFoundError:
            duration = (time.monotonic() - start_time) * 1000
            return SandboxResult(
                exit_code=-1,
                stdout="",
                stderr=f"MXC 原生二进制未找到: {self._binary_path}\n"
                       f"请确保已安装 MXC 并在 PATH 中可用。\n"
                       f"构建说明: https://github.com/microsoft/mxc#building",
                duration_ms=duration,
                config_json=config_json,
                backend=config.containment,
            )
        except subprocess.TimeoutExpired:
            duration = (time.monotonic() - start_time) * 1000
            return SandboxResult(
                exit_code=-2,
                stdout="",
                stderr="沙箱执行超时",
                duration_ms=duration,
                config_json=config_json,
                backend=config.containment,
            )
        finally:
            try:
                os.unlink(config_path)
            except OSError:
                pass

    def dry_run(self, config: ContainerConfig) -> str:
        """
        干运行模式 — 仅生成配置 JSON 而不实际执行。
        用于调试和策略验证。

        Args:
            config: 容器配置

        Returns:
            生成的 JSON 配置字符串
        """
        return config.to_json()


# ---------------------------------------------------------------------------
# 有状态沙箱（State-aware Lifecycle API）
# ---------------------------------------------------------------------------

class StatefulSandbox:
    """
    有状态沙箱 — 提供长生命周期沙箱的 State-aware 生命周期 API。

    对应 TypeScript SDK:
      provisionSandbox → startSandbox → execInSandboxAsync →
      stopSandbox → deprovisionSandbox

    来源: docs/state-aware-lifecycle/mxc-state-aware-sandbox-api.md

    生命周期: provision → start → exec(可多次) → stop → deprovision

    使用方式:
        sandbox = StatefulSandbox(client)
        sandbox.provision("isolation_session")
        sandbox.start()
        result = sandbox.exec_async("python -c 'print(1+1)'")
        sandbox.stop()
        sandbox.deprovision()
    """

    class State(str, Enum):
        CREATED = "created"
        PROVISIONED = "provisioned"
        STARTED = "started"
        STOPPED = "stopped"
        DEPROVISIONED = "deprovisioned"

    def __init__(self, client: MxcClient, policy: Optional[SandboxPolicy] = None):
        self._client = client
        self._policy = policy or SandboxPolicy()
        self._state = self.State.CREATED
        self._config: Optional[ContainerConfig] = None
        self._execution_count = 0

    @property
    def state(self) -> str:
        return self._state.value

    @property
    def execution_count(self) -> int:
        return self._execution_count

    def provision(
        self,
        containment: Union[str, ContainmentBackend] = ContainmentBackend.PROCESS,
    ) -> ContainerConfig:
        """
        预配沙箱 — 分配资源但不启动。

        对应 TypeScript SDK: provisionSandbox(policy, options)
        """
        if self._state != self.State.CREATED:
            raise RuntimeError(f"无法从状态 {self._state.value} 执行 provision")

        self._config = self._client.create_config_from_policy(
            self._policy, containment
        )
        self._state = self.State.PROVISIONED
        return self._config

    def start(self) -> None:
        """
        启动沙箱 — 创建隔离环境。

        对应 TypeScript SDK: startSandbox(provisionResult)
        """
        if self._state != self.State.PROVISIONED:
            raise RuntimeError(f"无法从状态 {self._state.value} 执行 start，需要先 provision")
        self._state = self.State.STARTED

    def exec_async(
        self,
        command: str,
        cwd: Optional[str] = None,
        env: Optional[List[str]] = None,
    ) -> SandboxResult:
        """
        在沙箱中执行命令。可多次调用。

        对应 TypeScript SDK: execInSandboxAsync(sandbox, command)
        """
        if self._state != self.State.STARTED:
            raise RuntimeError(f"无法从状态 {self._state.value} 执行 exec，需要先 start")

        if not self._config or not self._config.process:
            self._config = self._config or ContainerConfig()
            self._config.process = ProcessConfig()

        self._config.process.command_line = command
        if cwd:
            self._config.process.cwd = cwd
        if env:
            self._config.process.env = env

        result = self._client.spawn_sandbox_from_config(self._config)
        self._execution_count += 1
        return result

    def stop(self) -> None:
        """
        停止沙箱 — 终止所有进程。

        对应 TypeScript SDK: stopSandbox(sandbox)
        """
        if self._state != self.State.STARTED:
            raise RuntimeError(f"无法从状态 {self._state.value} 执行 stop")
        self._state = self.State.STOPPED

    def deprovision(self) -> None:
        """
        解除预配 — 释放所有资源。

        对应 TypeScript SDK: deprovisionSandbox(sandbox)
        """
        if self._state != self.State.STOPPED:
            raise RuntimeError(f"无法从状态 {self._state.value} 执行 deprovision，需要先 stop")
        self._state = self.State.DEPROVISIONED
        self._config = None

    def __enter__(self):
        """上下文管理器 — 自动 provision + start"""
        self.provision()
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器 — 自动 stop + deprovision"""
        if self._state == self.State.STARTED:
            self.stop()
        if self._state == self.State.STOPPED:
            self.deprovision()
        return False


# ---------------------------------------------------------------------------
# 审计日志支持
# ---------------------------------------------------------------------------

@dataclass
class AuditEntry:
    """审计日志条目"""
    timestamp: str
    action: str
    policy: Dict[str, Any]
    command: str
    backend: str
    exit_code: int
    stdout_length: int
    stderr_length: int
    duration_ms: float
    agent_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AuditLogger:
    """
    审计日志记录器。

    MXC 在 Windows 上通过 Event Tracing for Windows (ETW) 提供诊断日志。
    本类提供应用层审计追踪，记录每次沙箱执行的完整上下文。

    来源: GitHub docs/diagnostics.md — 诊断日志和 ETW
    """

    def __init__(self, log_file: Optional[str] = None):
        self._log_file = log_file
        self._entries: List[AuditEntry] = []

    def log_execution(
        self,
        result: SandboxResult,
        command: str,
        policy_dict: Dict[str, Any],
        agent_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AuditEntry:
        """记录一次沙箱执行"""
        from datetime import datetime, timezone

        entry = AuditEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            action="sandbox_exec",
            policy=policy_dict,
            command=command,
            backend=result.backend,
            exit_code=result.exit_code,
            stdout_length=len(result.stdout),
            stderr_length=len(result.stderr),
            duration_ms=result.duration_ms,
            agent_id=agent_id,
            metadata=metadata,
        )
        self._entries.append(entry)

        if self._log_file:
            with open(self._log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")

        return entry

    @property
    def entries(self) -> List[AuditEntry]:
        return list(self._entries)

    def summary(self) -> Dict[str, Any]:
        """生成审计摘要"""
        total = len(self._entries)
        if total == 0:
            return {"total_executions": 0}

        return {
            "total_executions": total,
            "success_count": sum(1 for e in self._entries if e.exit_code == 0),
            "failure_count": sum(1 for e in self._entries if e.exit_code != 0),
            "total_duration_ms": sum(e.duration_ms for e in self._entries),
            "backends_used": list(set(e.backend for e in self._entries)),
            "agents": list(set(e.agent_id for e in self._entries if e.agent_id)),
        }


# ---------------------------------------------------------------------------
# 便捷导出
# ---------------------------------------------------------------------------

__all__ = [
    # 常量
    "MXC_SCHEMA_VERSION",
    # 枚举
    "ContainmentBackend",
    "ClipboardAccess",
    "TempDirMode",
    "NetworkDefaultPolicy",
    # 策略
    "FilesystemPolicy",
    "NetworkPolicy",
    "UIPolicy",
    "SandboxPolicy",
    # 配置
    "ProcessConfig",
    "ContainerConfig",
    # 结果
    "SandboxResult",
    # 平台
    "PlatformSupport",
    "get_platform_support",
    # 辅助函数
    "get_available_tools_policy",
    "get_temporary_files_policy",
    "get_user_profile_policy",
    "load_policy_from_yaml",
    # 客户端
    "MxcClient",
    "StatefulSandbox",
    # 审计
    "AuditEntry",
    "AuditLogger",
]
