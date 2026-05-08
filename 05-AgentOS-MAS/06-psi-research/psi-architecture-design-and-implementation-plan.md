# Project PSI 架构设计与实现方案

| 字段 | 内容 |
|---|---|
| 文档版本 | v1.0 |
| 日期 | 2026-05-08 |
| 文档类型 | 研究结论 + 架构设计 + 实施计划 + 对抗性 Review |
| 目标读者 | Agent runtime / agent tool builder / 内部基础设施研发者 |
| 核心定位 | Durable Local Agent Microkernel |

## 1. 结论摘要

PSI 值得做，但只在一个很窄的定义下值得做：

> PSI 不是通用 Agent 平台，不是终端编码 Agent，不是 Pi 的替代品，也不是 workflow/DAG 框架。PSI 应被定义为一个可嵌入的、本地优先的、可恢复的 Agent 执行微内核。

它真正要解决的问题是：

> 把一次性的、无状态的 LLM 工具调用循环，变成一个可中断、可恢复、可审计、可加安全底线的持久化执行过程。

公平评估后，PSI 的价值成立，但市场野心必须收缩：

| 维度 | 判断 |
|---|---|
| 技术必要性 | 成立。durable execution、audit log、HITL、tool safety 是真实缺口。 |
| 市场独特性 | 部分成立。泛化 runtime 已红海，轻量本地 durable loop 仍有空间。 |
| 开源爆火概率 | 低。不应以替代 Pi 或追求 stars 为目标。 |
| 内部基础设施价值 | 高。可作为 Clawteam 或其他 agent 产品的执行底座。 |
| 个人/团队技术价值 | 高。能沉淀 agent runtime 的核心工程能力。 |

最终建议：

> 做 PSI，但必须做成“SQLite-like agent runtime library”，而不是“又一个 agent app”。

## 2. 依据与公正评估

### 2.1 支持 PSI 的证据

1. 本地 `01` 和 `05` 均指向同一核心：Agent 系统需要一个 loop-first、state-first、tool-native 的最小执行内核。
2. Anthropic 的 agent 工程建议强调简单、可组合模式优先，复杂度只在必要时增加；这支持 PSI 的薄内核方向。
3. Temporal、LangGraph 的成熟说明 durable execution/checkpoint/HITL/replay 已是长期任务系统的基础需求。
4. MCP 的普及说明工具与模型解耦正在标准化，PSI 无需内建大量业务工具，只需做好工具注册、路由、安全和审计。
5. Pi 的成功说明“强模型 + 极简 harness”确实能工作；PSI 可以继承这个哲学，并补足 Pi 不强调的 durable execution 与安全底线。

### 2.2 反对 PSI 的证据

1. 赛道拥挤。Pi、Codex、OpenCode、Cline、Aider、LangGraph、Temporal、各云厂商 Agent Runtime 已覆盖大量相邻空间。
2. “Minimal Agent Runtime”这个口号过泛，开发者不会因为抽象理念而采用新项目。
3. General-purpose agent runtime 容易陷入“什么都做、什么都不强”的陷阱。
4. Durable execution 并不新鲜，Temporal 和 LangGraph 已证明并占据心智。
5. Safety Gate 如果设计过强会变成新编排层；如果设计过弱又会沦为安全剧场。

### 2.3 公正判定

PSI 的必要性不是“行业缺一个通用 agent runtime”，而是：

> 缺一个足够小、可嵌入、本地优先、agent-loop 原生的 durable execution 内核。

因此 PSI 的成功标准不应是与 Pi、Codex、LangGraph 正面竞争，而应是：

1. 任何 agent app 都能把 PSI 嵌入为执行底座。
2. 进程崩溃、人工审批、工具失败、模型中断后，任务仍可恢复。
3. 每一步模型决策、工具调用、状态变化都可回放和审计。
4. 安全边界清晰可配置，只挡底线风险，不变成重型审批平台。

## 3. 产品定位

### 3.1 一句话定义

> PSI is a minimal durable runtime for local agent loops.

中文定义：

> PSI 是一个面向 Agent Loop 的极简持久化执行微内核。

### 3.2 PSI 是什么

PSI 是：

- 一个 SDK/library 优先的 runtime core。
- 一个 append-only event log + checkpoint/resume 引擎。
- 一个工具调用路由与审计层。
- 一个最小安全门。
- 一个可被 Pi、OpenCode、自研 TUI、后端服务或桌面应用嵌入的执行底座。

### 3.3 PSI 不是什么

PSI 不是：

- 终端编码 Agent。
- 完整 Agent OS。
- 多 Agent 编排平台。
- DAG/workflow 平台。
- LLM provider 大统一抽象层。
- UI/TUI 产品。
- MCP server 大集合。
- 自动记忆、自动规划、自动学习系统。

### 3.4 PSI 应该干什么

PSI 第一性任务只有一个：

> 让 Agent 的执行过程从“临时会话”升级为“可恢复的工程事实”。

具体来说，PSI 应该干：

1. 接收结构化任务目标、约束和验收标准。
2. 驱动模型在统一 loop 中持续决定下一步动作。
3. 把所有工具调用转成可审计事件。
4. 在每轮后写入 checkpoint，使任务可以恢复。
5. 在高风险动作前挂起并等待人类批准。
6. 提供 replay/fork 能力，让失败可复盘、路径可比较。

PSI 不应该干：

1. 不替用户设计业务流程。
2. 不替模型做复杂 planner。
3. 不争夺终端 agent 的交互体验。
4. 不内建大而全工具生态。
5. 不承诺替代 sandbox、容器和系统权限。

## 4. 理念、本质与原则

### 4.1 核心理念

PSI 的理念是：

> 模型负责智能决策，内核负责可靠执行。

进一步拆开：

- 模型决定下一步做什么。
- 工具负责真实世界动作。
- 状态日志记录事实。
- 安全门守住底线。
- Runtime 只保证循环、恢复、审计和边界。

### 4.2 本质

PSI 的本质不是 framework，而是 runtime microkernel：

```text
Goal
  -> Loop
  -> Model decision
  -> Safety check
  -> Tool call
  -> Observation
  -> Event log
  -> Checkpoint
  -> Resume / Continue / Stop
```

PSI 的关键资产不是工具数量，而是执行轨迹：

> State is truth. Event log is memory. Checkpoint is continuity.

### 4.3 架构原则

1. **Thin Core**：核心只放无法由模型或插件可靠替代的能力。
2. **Loop First**：所有任务统一进入同一执行循环，不按场景创建多套 runtime。
3. **State Is Truth**：自然语言可以解释状态，但不能作为唯一状态。
4. **Plugin Everything**：工具、模型、存储、安全策略、UI 都在核心外扩展。
5. **Safety As Boundary**：安全门只做边界控制，不做任务编排。
6. **Replay Before Intelligence**：先让执行可回放，再谈优化模型行为。
7. **Local First**：MVP 使用本地文件和单二进制，降低试用和集成成本。
8. **Model Understandable**：系统复杂度必须低到模型能够理解自己的运行环境。

## 5. 总体架构

### 5.1 架构图

```text
Host App / CLI / Service
        |
        v
    TaskSpec
        |
        v
+------------------- PSI Core -------------------+
|                                                 |
|  ExecutionLoop                                  |
|    |                                            |
|    +--> ModelClient                             |
|    |       |                                    |
|    |       v                                    |
|    |   ActionIntent                             |
|    |                                            |
|    +--> Minimal Safety Gate                     |
|    |       |                                    |
|    |       v                                    |
|    +--> ToolRegistry -> ToolAdapter/MCP Adapter |
|    |       |                                    |
|    |       v                                    |
|    +--> Observation                             |
|            |                                    |
|            v                                    |
|      EventStore + CheckpointStore               |
|            |                                    |
|            v                                    |
|      Rehydration / Replay / Fork                |
|                                                 |
+-------------------------------------------------+
```

### 5.2 核心模块

PSI Core 只包含五个核心模块：

1. `TaskSpec`
2. `ExecutionLoop`
3. `ToolRegistry`
4. `StateStore & EventLog`
5. `Minimal Safety Gate`

为了工程可用，还需要三个薄接口，但它们不是策略中心：

1. `ModelClient`
2. `StorageDriver`
3. `ObserverHook`

## 6. 模块设计

### 6.1 TaskSpec

`TaskSpec` 是 PSI 的唯一任务入口。它把用户目标变成可验证、可约束、可恢复的执行单元。

```json
{
  "task_id": "task_01H...",
  "title": "Refactor billing module safely",
  "goal": "Refactor billing module and keep all tests passing",
  "constraints": [
    "Do not modify database migrations",
    "Do not delete user data",
    "Ask before changing CI configuration"
  ],
  "acceptance_criteria": [
    "Unit tests pass",
    "No public API regression",
    "Execution log includes all file writes"
  ],
  "risk_level": "medium",
  "capabilities": ["filesystem", "shell", "git"],
  "workspace": {
    "root": "/repo",
    "allow_paths": ["src", "tests"],
    "deny_paths": [".env", "secrets", "prod"]
  }
}
```

设计要求：

- 任务必须有验收标准。
- 任务必须声明工具能力边界。
- 任务必须有风险等级。
- 不允许只有一句自由文本就进入高风险执行。

### 6.2 ExecutionLoop

`ExecutionLoop` 是 PSI 的心脏，但它不包含业务策略。

标准循环：

```text
LoadState
  -> BuildModelContext
  -> AskModel
  -> ParseActionIntent
  -> SafetyCheck
  -> ExecuteTool
  -> RecordObservation
  -> CommitEvent
  -> UpdateCheckpoint
  -> DecideContinue
```

状态机：

```text
created
  -> running
  -> suspended
  -> running
  -> completed

running
  -> failed
  -> resumable
  -> running

running
  -> cancelled
```

必须支持：

- 单步执行。
- 连续执行。
- timeout。
- retry。
- suspend。
- resume。
- replay。
- fork。
- human approval。

### 6.3 StateStore & EventLog

这是 PSI 区别于简单 while loop 的核心。

事件日志采用 append-only JSONL：

```json
{
  "event_id": "evt_01H...",
  "task_id": "task_01H...",
  "execution_id": "exec_01H...",
  "parent_event_id": "evt_01H_prev",
  "type": "tool_result",
  "timestamp": "2026-05-08T12:00:00Z",
  "payload": {},
  "hash": "sha256:...",
  "prev_hash": "sha256:..."
}
```

核心事件类型：

| Event | 说明 |
|---|---|
| `task_created` | 任务创建 |
| `loop_started` | 执行循环开始 |
| `model_requested` | 向模型发起请求 |
| `model_responded` | 模型输出 |
| `action_intent_created` | 解析出的动作意图 |
| `safety_decided` | 安全门决策 |
| `tool_called` | 工具调用请求 |
| `tool_result` | 工具执行结果 |
| `checkpoint_written` | checkpoint 生成 |
| `suspended` | 挂起等待 |
| `approved` | 人工批准 |
| `denied` | 人工拒绝 |
| `resumed` | 恢复执行 |
| `completed` | 任务完成 |
| `failed` | 任务失败 |

Checkpoint 不是日志的替代品，而是日志的加速索引：

```json
{
  "checkpoint_id": "ckpt_01H...",
  "task_id": "task_01H...",
  "execution_id": "exec_01H...",
  "last_event_id": "evt_01H...",
  "status": "running",
  "model_context_ref": "ctx_01H...",
  "current_plan": [],
  "pending_action": null,
  "retry_state": {},
  "artifact_refs": []
}
```

### 6.4 Rehydration / Replay / Fork

PSI 必须明确区分三种恢复能力：

| 能力 | 含义 |
|---|---|
| Rehydrate | 从日志和 checkpoint 恢复当前执行状态，继续跑。 |
| Replay | 不重新调用外部工具，按历史事件重放，用于审计和调试。 |
| Fork | 从某个 checkpoint 创建新分支，允许修改上下文或策略后继续。 |

由于 LLM 调用本身非确定性，PSI 不承诺“重新调用模型得到同样输出”。正确做法是：

- replay 模式使用历史 `model_responded` 和 `tool_result`。
- resume 模式从最后可信 checkpoint 继续调用模型。
- fork 模式显式生成新的 execution branch。

### 6.5 ToolRegistry

`ToolRegistry` 统一工具描述、权限、路由、调用和审计。

工具描述：

```json
{
  "tool_id": "shell.exec",
  "name": "Shell Exec",
  "description": "Run a shell command in the workspace",
  "input_schema": {},
  "output_schema": {},
  "capability": "shell",
  "permission_level": "write",
  "side_effect_level": "high",
  "risk_annotations": {
    "read_only": false,
    "destructive": true,
    "external_network": false,
    "secrets_access": false
  },
  "idempotency": "caller_key_required",
  "rollback_supported": false
}
```

MVP 工具适配器：

- `filesystem.read`
- `filesystem.write`
- `filesystem.patch`
- `shell.exec`
- `http.request`
- `mcp.call`

完整版工具适配器：

- Browser adapter。
- Computer-use adapter。
- Git adapter。
- Database read-only adapter。
- Queue/webhook adapter。
- Custom local tool adapter。

MCP 应作为一等适配器，但不是内核本身。PSI 必须在 MCP 工具元数据之外增加自己的风险注解、权限策略、审计事件和 idempotency 约束。

### 6.6 Minimal Safety Gate

Safety Gate 的职责是边界控制，而不是替模型规划任务。

输入：

```json
{
  "task_id": "task_01H...",
  "action_intent": {},
  "tool_descriptor": {},
  "task_constraints": [],
  "workspace_policy": {},
  "history_summary": {}
}
```

输出：

```json
{
  "decision": "allow",
  "risk_level": "low",
  "reason": "Read-only file access under allow_paths",
  "required_approval": false
}
```

决策类型：

| Decision | 含义 |
|---|---|
| `allow` | 允许执行 |
| `deny` | 拒绝执行，不可继续该动作 |
| `require_approval` | 挂起等待人工批准 |
| `require_replan` | 要求模型重新规划 |

MVP 内置规则：

- 禁止访问 deny_paths。
- 高风险 shell 命令需要 approval。
- 删除、覆盖、迁移、发布、转账等不可逆动作需要 approval。
- 外部网络请求可按域名 allow/deny。
- secrets 文件默认不可读。
- 超出 TaskSpec capability 的工具不可调用。

重要边界：

> Safety Gate 不是完整安全沙箱。真正的隔离仍应依赖容器、系统权限、网络策略和最小凭证。

### 6.7 ModelClient

PSI 不应重写完整 LLM 抽象层。

MVP 只定义极薄接口：

```go
type ModelClient interface {
    Complete(ctx context.Context, req ModelRequest) (ModelResponse, error)
}
```

MVP 提供：

- OpenAI-compatible adapter。
- Anthropic adapter 可选。
- Fake model adapter 用于测试。

不做：

- 模型市场。
- 成本矩阵。
- provider 路由优化。
- thinking trace 跨 provider 转换。

这些以后可以作为插件，不进入 core。

## 7. 执行流程

### 7.1 正常执行

```text
1. Host 提交 TaskSpec
2. PSI 写入 task_created
3. ExecutionLoop 读取当前 checkpoint
4. ModelClient 生成下一步 ActionIntent
5. Safety Gate 检查动作
6. ToolRegistry 路由到具体 ToolAdapter
7. ToolAdapter 返回 Observation
8. PSI 记录所有事件
9. PSI 写入 checkpoint
10. Loop 判断继续或完成
```

### 7.2 挂起与恢复

```text
1. Safety Gate 返回 require_approval
2. PSI 写入 suspended 事件
3. 进程可以退出
4. 用户或外部系统写入 approved/denied
5. psi resume 读取 checkpoint 与 approval event
6. ExecutionLoop 从挂起点继续
```

### 7.3 崩溃恢复

```text
1. 进程崩溃或网络中断
2. 用户执行 psi resume <task_id>
3. PSI 校验 event chain
4. PSI 读取最后 checkpoint
5. 对未完成 tool call 做幂等检查
6. 继续执行或要求人工确认
```

## 8. 实现方案

### 8.1 技术选型

MVP 建议使用 Go。

理由：

- 单文件二进制，安装和嵌入简单。
- 并发、文件 IO、CLI、HTTP、JSON 生态成熟。
- 比 Rust 更快形成 MVP。
- 比 TypeScript 更符合“底层 runtime”心智，且避开 Pi/Claude Code/Codex CLI 的 TypeScript 直接竞争。

Rust 可作为后续选项，尤其用于更强沙箱、WASM plugin 或嵌入式安全场景。

### 8.2 仓库结构

```text
psi/
  cmd/psi/                  # CLI: run/status/resume/replay/approve
  core/
    task/                   # TaskSpec
    loop/                   # ExecutionLoop
    state/                  # EventLog + Checkpoint
    safety/                 # Safety Gate
    tools/                  # ToolRegistry interfaces
    model/                  # ModelClient interfaces
  adapters/
    model/openai/
    tools/filesystem/
    tools/shell/
    tools/http/
    tools/mcp/
    storage/file/
  examples/
    safe-coding-agent/
    durable-backend-agent/
    browser-automation/
  docs/
```

### 8.3 CLI 形态

MVP 需要 CLI，但 CLI 只是调试和演示入口，不是产品主形态。

```bash
psi run task.yaml
psi status <task_id>
psi resume <task_id>
psi approve <task_id> <approval_id>
psi deny <task_id> <approval_id>
psi replay <task_id>
psi fork <task_id> --from <checkpoint_id>
```

### 8.4 文件存储布局

```text
.psi/
  tasks/
    task_01H/
      task.json
      events.jsonl
      checkpoints/
        ckpt_0001.json
        ckpt_0002.json
      artifacts/
      approvals/
```

### 8.5 测试策略

必须优先测试 runtime 语义，而不是模型表现。

MVP 测试：

- Event append 顺序与 hash chain。
- checkpoint 写入和读取。
- crash 后 resume。
- safety allow/deny/approval。
- tool call idempotency。
- replay 不重复执行外部副作用。
- fake model 驱动完整 loop。

验收测试：

- 人为 kill 进程后可恢复。
- approval 后可继续。
- deny 后模型可 replan。
- 文件写操作均可审计。
- shell 高危命令被拦截。

## 9. 短期 MVP 计划

目标：

> 在 4 到 6 周内证明 PSI 的核心价值：一个本地 agent loop 可以在进程中断、人工审批和工具失败后继续执行，并留下完整审计轨迹。

### Week 1：内核骨架

交付：

- Go module 初始化。
- TaskSpec schema。
- EventLog append-only JSONL。
- CheckpointStore。
- Fake ModelClient。
- 单步 loop。

验收：

- `psi run task.yaml --fake-model` 可产生完整事件日志。

### Week 2：工具与安全门

交付：

- ToolRegistry。
- filesystem read/write/patch。
- shell.exec。
- Minimal Safety Gate 规则引擎。
- approval event。

验收：

- 读操作自动允许。
- 写操作落日志。
- 高危 shell 命令挂起等待批准。

### Week 3：恢复与回放

交付：

- `psi resume`。
- `psi replay`。
- checkpoint rehydration。
- tool idempotency key。
- crash simulation tests。

验收：

- kill 进程后可从最后 checkpoint 继续。
- replay 不重复执行 shell/write 副作用。

### Week 4：真实模型与第一个 Demo

交付：

- OpenAI-compatible ModelClient。
- safe coding demo。
- README。
- 最小 SDK API。

验收：

- Agent 修改一个小项目，测试失败后修复，所有写入可审计。
- 修改危险文件触发 approval，批准后继续。

### Week 5-6：MVP 打磨

交付：

- MCP adapter 最小版。
- http.request adapter。
- status 命令。
- 文档和架构图。
- 三个端到端用例中的至少两个。

验收：

- 外部 MCP tool 可被注册和调用。
- tool 风险元数据进入 Safety Gate。
- 可演示 30 秒核心价值。

## 10. 完整功能计划

### v0.1：Durable Local Loop

范围：

- 本地文件存储。
- TaskSpec。
- EventLog。
- Checkpoint/resume/replay。
- ToolRegistry。
- Minimal Safety Gate。
- filesystem/shell/http tools。
- OpenAI-compatible model adapter。

目标：

- 验证“轻量本地 durable loop”成立。

### v0.2：Tool Adapter Ecosystem

范围：

- MCP adapter 完整化。
- Browser adapter。
- Git adapter。
- Approval webhook。
- Secret redaction。
- Policy file。
- SDK examples。

目标：

- 让 PSI 能被真实 agent app 嵌入。

### v0.3：Forkable Execution

范围：

- Tree-structured execution。
- checkpoint fork。
- branch compare。
- time travel debugging。
- artifact index。
- observer hooks。

目标：

- 把 PSI 变成可调试、可审计、可实验的 agent execution ledger。

### v0.4：Production Storage

范围：

- SQLite storage driver。
- Postgres storage driver。
- encrypted local store。
- multi-process lock。
- remote worker protocol。

目标：

- 支持小团队和内部服务落地。

### v1.0：Stable Microkernel

范围：

- 稳定 core API。
- 插件接口。
- storage/tool/model/safety 扩展点。
- 完整文档。
- benchmark 和可靠性测试。

目标：

- 成为 agent runtime 的嵌入式基础设施。

## 11. 预期效果与衡量指标

### 11.1 预期效果

1. Agent 任务不再因进程退出、网络错误、人工等待而丢失进度。
2. 每一步模型和工具行为都可审计。
3. 开发者能在不引入 Temporal/LangGraph 的情况下获得轻量 durable execution。
4. 高风险动作有明确、可配置、可追踪的安全边界。
5. 上层 agent app 可以保持很薄，把可靠性委托给 PSI。

### 11.2 关键指标

| 指标 | MVP 目标 |
|---|---|
| 崩溃恢复成功率 | 本地测试场景 100% |
| Replay 副作用重复率 | 0 |
| 高风险动作漏拦截率 | 内置规则场景 0 |
| checkpoint 恢复时间 | 小任务 < 1s |
| 端到端 demo 时间 | 30 秒能看懂核心价值 |
| 核心代码规模 | 尽量控制在 3k-5k LOC 内 |

## 12. Killer Demos

### 12.1 Safe Coding Agent

场景：

- Agent 修改代码。
- 写入普通源码文件被允许。
- 尝试修改 `.env` 或 CI 发布配置时挂起。
- 用户批准后继续，拒绝后 replan。
- 最后展示完整事件日志和 diff。

证明：

- Safety Gate 有价值。
- 执行可恢复。
- PSI 可嵌入编码 agent。

### 12.2 Durable Backend Agent

场景：

- Agent 执行对账任务。
- 中途等待外部 webhook。
- 进程退出 1 小时。
- webhook 到达后 resume。

证明：

- PSI 能处理 long-running task。
- PSI 不只是 coding harness。

### 12.3 Browser Automation

场景：

- Agent 使用 browser adapter 操作网页。
- 遇到失败或弹窗。
- 记录 screenshot/observation。
- retry 后失败则挂起人工接管。

证明：

- PSI 的 loop 能容纳 computer/browser use。
- Observation 和 checkpoint 对不稳定 UI 操作有价值。

## 13. 风险与对策

| 风险 | 影响 | 对策 |
|---|---|---|
| 定位重新变泛 | 失去差异化 | 所有文档固定为 Durable Local Agent Microkernel。 |
| 核心变厚 | 复制 LangGraph/Temporal 复杂度 | UI、planner、memory、subagent 全部外置。 |
| Safety Gate 变安全剧场 | 误导用户 | 明确只做底线策略，隔离交给 sandbox。 |
| MCP 工具不可信 | 数据泄露或越权 | MCP adapter 必须增加 PSI 风险注解与 approval。 |
| LLM 非确定性破坏 replay | 审计不可信 | replay 使用历史响应；resume/fork 明确产生新分支。 |
| 工具副作用重复 | 造成破坏 | idempotency key、pending action、人工确认。 |
| 日志泄露敏感信息 | 安全风险 | redaction、deny secrets、可选加密存储。 |
| 开发者不理解价值 | 采用困难 | 用 crash/resume/approval 的 demo 展示价值。 |

## 14. 对抗性 Review

### 攻击 1：PSI 没有市场，赛道已经满了

这个批评成立一半。作为独立 agent app 或通用 runtime，PSI 不值得做。但作为可嵌入 durable local loop，PSI 避开了终端 agent、云 runtime、重型 workflow 的主战场。

修订：

- 不做 app。
- 不做通用平台。
- 不以 GitHub 爆火为目标。
- 定位为 SDK/library。

### 攻击 2：PSI 只是 Temporal/LangGraph 的弱化版

如果 PSI 做 workflow、graph、distributed orchestration，这个批评成立。PSI 的边界必须更窄：只解决 agent loop 的本地持久化、审计、安全和恢复。

修订：

- 不实现 DAG。
- 不实现 distributed scheduler。
- 不引入中心化 orchestrator。
- 保持文件存储 MVP。

### 攻击 3：LLM 非确定性导致 durable execution 不可靠

这个批评很重要。传统 durable execution 依赖确定性 replay，但 LLM 调用天然不确定。PSI 不能假装重新执行会得到同样结果。

修订：

- 明确区分 replay、resume、fork。
- replay 使用历史模型响应和工具结果。
- resume 从 checkpoint 继续，不承诺历史重算一致。
- fork 显式创建新分支。

### 攻击 4：Safety Gate 不是安全，只是心理安慰

如果 Safety Gate 声称能解决所有安全问题，这个批评成立。PSI 的 Safety Gate 只做策略边界、审批与审计，不能替代 sandbox、权限、容器和网络隔离。

修订：

- 文档明确 Safety Gate 的能力边界。
- 高风险工具建议默认 sandbox。
- 内核记录 exact command、input、approval、result。

### 攻击 5：MCP 已经标准化工具了，PSI 的 ToolRegistry 多余

MCP 解决连接协议，不解决 PSI 所需的完整执行语义：checkpoint、idempotency、risk annotation、event sourcing、resume/replay。PSI 应拥抱 MCP，但不能把 MCP 直接等同为可信执行层。

修订：

- MCP 是 adapter，不是 core。
- ToolRegistry 负责 PSI 内部风险和审计语义。

### 攻击 6：没有 UI 就没有用户

这对消费级工具成立，但 PSI 的第一用户是 builder。早期 UI 会拉高复杂度并把项目拖向 Pi/OpenCode/Codex 的竞争区。

修订：

- CLI 只做调试入口。
- 优先 SDK 和 demo。
- 后续可让 Pi/OpenCode/自研 TUI 嵌入 PSI。

### 攻击 7：Go 生态不如 TypeScript/Python 适合 Agent

Agent 工具生态确实偏 TypeScript/Python，但 PSI 的职责不是写工具，而是做 runtime。Go 的单二进制、本地 IO、并发和部署体验更符合 PSI 的底层定位。MCP adapter 可以连接外部生态。

修订：

- Go 做 core。
- MCP/HTTP/shell 连接生态。
- 不重写工具生态。

### 攻击 8：核心 5 模块仍然可能越做越厚

这个风险最大。PSI 必须有架构红线。

修订：

- planner 不进 core。
- memory 不进 core。
- UI 不进 core。
- multi-agent 不进 core。
- workflow 不进 core。
- provider routing 不进 core。

## 15. 最终修订版方案

经过对抗性 review 后，最终 PSI 方案收敛为：

> 一个用 Go 实现的、本地文件存储优先的、SDK/library 形态的 durable agent loop 微内核。

核心只做：

1. `TaskSpec`：结构化任务、约束、验收标准、能力边界。
2. `ExecutionLoop`：模型-工具-观测-状态的持续循环。
3. `EventLog/Checkpoint`：append-only 事件溯源、恢复、回放、分支。
4. `ToolRegistry`：工具 schema、路由、风险注解、幂等语义。
5. `SafetyGate`：最小底线拦截、人工审批、审计。

第一阶段只证明三件事：

1. 进程死了能恢复。
2. 高风险动作能挂起审批。
3. replay 不重复执行副作用。

这三件事如果做不扎实，PSI 就没有价值。做扎实之后，再扩展 MCP、browser、computer use、storage driver 和生态集成。

## 16. 参考来源

本地来源：

- `00-insight-why-project-Psi.md`
- `01-insight-what-is-project-Psi.md`
- `02-insight-Psi-vs-Pi.md`
- `03-insight-Pi-Deep-Research.md`
- `04-feasibility-Psi-Project-Assessment.md`
- `05-insight-Psi-Microkernel-Strategy.md`

外部核验：

- Anthropic, Building effective agents: https://www.anthropic.com/engineering/building-effective-agents
- Model Context Protocol overview: https://modelcontextprotocol.io/docs/getting-started/intro
- MCP tools specification: https://modelcontextprotocol.io/specification/2024-11-05/server/tools
- MCP security best practices: https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices
- LangGraph persistence docs: https://docs.langchain.com/oss/python/langgraph/persistence
- Temporal durable execution docs: https://docs.temporal.io/
- Pi GitHub repository: https://github.com/earendil-works/pi
- Codex GitHub repository: https://github.com/openai/codex
- LangGraph GitHub repository: https://github.com/langchain-ai/langgraph
