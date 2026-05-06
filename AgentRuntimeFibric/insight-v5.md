# Agent Runtime Fabric 详细设计（用于研发实现）

## 0. 文档目标

本文档把 **Agent Runtime Fabric** 从概念方案落到可研发、可拆分、可实现的系统设计。其核心判断是：当前主流 agent 基础设施已经从“聊天式函数调用”演进到“**控制面与执行面分离的持久化工作流**”。OpenAI 明确将 orchestration、tool execution、approvals、state 交给应用层；sandbox 用来承载文件、命令、产物、端口和暂停后恢复；Codex cloud 则把任务后台化、并行化、worktree 化。E2B、Modal 强化 snapshot / pause-resume；OpenHands、Open Agents 强化 workspace / event / remote execution；Google 与 AWS 则把 identity、policy、governance、observability 平台化；AutoGen 则补齐 actor model 与 event-driven 协作。([developers.openai.com](https://developers.openai.com/api/docs/guides/agents), [developers.openai.com](https://developers.openai.com/api/docs/guides/agents/sandboxes), [e2b.dev](https://e2b.dev/docs/sandbox/persistence), [modal.com](https://modal.com/docs/guide/sandboxes), [docs.openhands.dev](https://docs.openhands.dev/sdk/arch/conversation), [docs.cloud.google.com](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime), [docs.aws.amazon.com](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html), [microsoft.github.io](https://microsoft.github.io/autogen/stable//user-guide/core-user-guide/index.html), [github.com](https://github.com/vercel-labs/open-agents))

---

## 1. 设计原则

### 1.1 控制面与执行面彻底分离

Control Plane 只做规划、拆解、路由、审批、恢复、回放，不直接承载危险执行。Execution Plane 只提供隔离执行能力：shell、filesystem、network、browser、GPU、ports。这样做的直接收益是：Runtime 可销毁、可重建、可迁移，Agent 不再绑定某个容器进程。

### 1.2 Workspace-first

所有长时任务的本体都应落在 Workspace，而不是落在对话上下文。Workspace 至少包含：仓库、依赖缓存、环境变量、运行端口、浏览器状态、构建产物、日志索引、快照链、分支信息。

### 1.3 Snapshot-first

Snapshot 不是备份，而是运行时语义的一部分。它必须支持：

* 增量化；
* 可恢复；
* 可分叉；
* 可回放；
* 与事件日志可互相定位。

E2B 的 persistence / snapshots 与 Modal 的 filesystem snapshots 都是这个方向的直接验证。([e2b.dev](https://e2b.dev/docs/sandbox/snapshots), [e2b.dev](https://e2b.dev/docs/sandbox/lifecycle-events-api), [modal.com](https://modal.com/docs/guide/sandbox-snapshots))

### 1.4 Policy is first-class

sandbox 只定义技术边界，approval policy 定义何时越界；Google 和 AWS 的平台也都把 identity、gateway、policy、observability 做成独立原语。你的系统里，Policy 不能散落在 agent prompt 或工具代码中，必须是可组合、可审计、可下发、可版本化的对象。([developers.openai.com](https://developers.openai.com/codex/concepts/sandboxing), [docs.cloud.google.com](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/agent-identity-overview), [docs.aws.amazon.com](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html))

### 1.5 Event-driven & replayable

系统默认事件驱动：Task、Runtime、Workspace、Snapshot、Approval、Artifact 都通过事件推进状态。OpenHands 的 Conversation / Agent Server 体系、AutoGen 的 actor model，都说明 agent 运行系统最终会收敛到 message/event + state management。([docs.openhands.dev](https://docs.openhands.dev/sdk/arch/conversation), [docs.openhands.dev](https://docs.openhands.dev/sdk/arch/overview), [microsoft.github.io](https://microsoft.github.io/autogen/stable//user-guide/core-user-guide/index.html))

---

## 2. 总体架构

### 2.1 逻辑分层

```text
User / IDE / API
        |
        v
+-------------------+
| Control Plane     |
| planner/router    |
| memory/reviewer   |
| policy/approvals  |
+-------------------+
        |
        v
+-------------------+
| Execution Plane   |
| runtime pool      |
| sandbox/microVM   |
| browser/GPU/etc.  |
+-------------------+
        |
        v
+-------------------+
| State Plane       |
| event log         |
| snapshots         |
| artifacts         |
| metadata/index    |
+-------------------+
        |
        v
+-------------------+
| Observability     |
| trace/replay      |
| timeline/debug    |
| audit/provenance  |
+-------------------+
```

### 2.2 物理服务划分

建议拆成 7 个服务域：

1. **orchestrator-service**：Session/Task 生命周期、调度、恢复；
2. **policy-service**：权限、审批、网络规则、secret scope；
3. **workspace-service**：Workspace 创建、挂载、分支、快照；
4. **runtime-fleet**：容器 / microVM / browser / GPU runtime；
5. **event-bus**：命令、状态、审批、快照事件总线；
6. **artifact-store**：日志、patch、build output、test report；
7. **observability-service**：trace、replay、timeline、diff UI。

---

## 3. 核心对象模型

## 3.1 Session

**Session** 表示用户的宏观目标，例如“完成一个 Chrome 插件”“修复某仓库 CI”。Session 是控制对象，不是执行对象。

建议字段：

```json
{
  "session_id": "uuid",
  "tenant_id": "uuid",
  "owner_id": "uuid",
  "goal": "string",
  "status": "ACTIVE|PAUSED|DONE|FAILED|ABORTED",
  "policy_bundle_id": "uuid",
  "root_task_id": "uuid",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

## 3.2 Task

**Task** 是可执行工作单元，支持递归分解与合并。Task 必须可恢复、可重试、可挂起。

建议字段：

```json
{
  "task_id": "uuid",
  "session_id": "uuid",
  "parent_task_id": "uuid|null",
  "title": "string",
  "status": "QUEUED|PROVISIONING|RUNNING|WAITING_APPROVAL|SNAPSHOTTING|SUSPENDED|RECOVERING|SUCCEEDED|FAILED|ABORTED|EVICTED",
  "plan": { "steps": [] },
  "workspace_id": "uuid",
  "runtime_id": "uuid|null",
  "policy_id": "uuid",
  "last_snapshot_id": "uuid|null",
  "retry_count": 0
}
```

## 3.3 Workspace

**Workspace** 是 Agent 的“身体”。它承载代码、依赖、缓存、端口、浏览器状态和 branch。

建议字段：

```json
{
  "workspace_id": "uuid",
  "tenant_id": "uuid",
  "base_image": "string",
  "repo_ref": "git_url_or_snapshot_ref",
  "branch_id": "uuid|null",
  "mounts": [],
  "env": {},
  "open_ports": [],
  "cache_policy": "HOT|WARM|COLD",
  "snapshot_head_id": "uuid|null",
  "lock_state": "UNLOCKED|LOCKED",
  "created_at": "timestamp"
}
```

## 3.4 Snapshot

**Snapshot** 是增量检查点，包含 filesystem diff、必要的进程态 / memory 状态、以及恢复所需元数据。

建议字段：

```json
{
  "snapshot_id": "uuid",
  "workspace_id": "uuid",
  "parent_snapshot_id": "uuid|null",
  "kind": "FS_DELTA|FS+MEMORY|FS+MEMORY+PROCESS",
  "delta_ref": "blob_uri",
  "metadata": {
    "runtime_type": "container|microvm|browser|gpu",
    "reason": "manual|auto|approval|preemption|failure",
    "command_cursor": "event_id"
  },
  "created_at": "timestamp"
}
```

## 3.5 Policy

**Policy** 需要拆成五类：

* Tool policy：允许哪些工具；
* Path policy：允许写哪些目录；
* Network policy：允许哪些域名 / 端口；
* Approval policy：哪些动作必须审批；
* Secret policy：哪些 secret 可见。

建议字段：

```json
{
  "policy_id": "uuid",
  "allowed_tools": ["bash", "git", "npm", "python"],
  "allowed_paths": ["/workspace", "/tmp"],
  "egress_rules": [{"host":"*.github.com","ports":[443]}],
  "approval_rules": [{"action":"git push","risk":"high"}],
  "secret_scope": ["repo_read", "ci_token"]
}
```

## 3.6 Artifact

**Artifact** 是交付物、证据和后续输入。包括 patch、日志、测试结果、二进制、截图、页面录屏等。

建议字段：

```json
{
  "artifact_id": "uuid",
  "task_id": "uuid",
  "snapshot_id": "uuid|null",
  "type": "log|patch|binary|report|screenshot|trace",
  "uri": "blob_uri",
  "checksum": "sha256",
  "created_at": "timestamp"
}
```

---

## 4. Runtime 设计

## 4.1 Runtime 类型

Runtime 是可插拔执行后端，不是系统主体。

建议最少支持：

* `container`：低风险任务、快速迭代；
* `microvm`：不可信代码、强隔离；
* `browser`：网页自动化、UI 测试；
* `gpu`：模型推理、训练、编译加速；
* `wasm`：超轻量工具执行。

OpenAI、OpenHands、Open Agents 的分层方式都说明：执行环境应该与控制面解耦，并可替换为不同隔离形态。([developers.openai.com](https://developers.openai.com/api/docs/guides/agents/sandboxes), [docs.openhands.dev](https://docs.openhands.dev/sdk/arch/agent-server), [github.com](https://github.com/vercel-labs/open-agents))

## 4.2 Runtime 状态机

```text
DRAFTED -> QUEUED -> PROVISIONING -> MOUNTED -> PRIMING -> RUNNING
RUNNING -> WAITING_APPROVAL -> RUNNING
RUNNING -> SNAPSHOTTING -> RUNNING
RUNNING -> SUSPENDED -> RECOVERING -> RUNNING
RUNNING -> SUCCEEDED|FAILED|ABORTED|EVICTED
```

### 状态解释

* **PROVISIONING**：拉起 runtime、注入策略、挂载 workspace；
* **MOUNTED**：workspace 已可用，但未进入稳定执行；
* **PRIMING**：安装依赖、warm cache、启动服务；
* **WAITING_APPROVAL**：高风险动作被策略拦截；
* **SNAPSHOTTING**：生成快照；
* **SUSPENDED**：可恢复挂起；
* **RECOVERING**：从 snapshot / suspend 恢复。

E2B 的 pause/resume、snapshot 生命周期，以及 Modal 的 snapshot 复用，都是这里的实现参考。([e2b.dev](https://e2b.dev/docs/sandbox/persistence), [e2b.dev](https://e2b.dev/docs/sandbox/lifecycle-events-api), [modal.com](https://modal.com/docs/guide/sandboxes))

---

## 5. 执行与恢复流程

### 5.1 正常执行

1. Control Plane 创建 Session 与 Root Task。
2. Policy Service 绑定 policy bundle。
3. Workspace Service 创建 workspace，挂载 repo / cache。
4. Runtime Fleet 分配 sandbox / microVM。
5. Priming 阶段完成依赖安装与服务启动。
6. Task 进入 RUNNING，开始执行步骤。
7. 命令、文件变化、stdout/stderr、artifact 都写入 Event Log / Artifact Store。
8. 任务完成后生成 final snapshot、patch、report。

### 5.2 失败恢复

1. Runtime 崩溃或超时，事件总线收到失败事件。
2. Observability Service 从最后可用 snapshot、事件尾部和 stderr 中提取恢复上下文。
3. Control Plane 决定：

   * 原 runtime 恢复；
   * 新 runtime 接管；
   * 提升资源规格；
   * 回滚到前一快照；
   * 请求人工审批。
4. Workspace 以 snapshot 为基点恢复。
5. Task 继续执行，同一 Task ID 不变。

这个恢复模型与 OpenAI 的 resumable state、E2B 的 pause/resume、OpenHands 的 conversation state orchestration 方向一致。([developers.openai.com](https://developers.openai.com/api/docs/guides/agents/results), [e2b.dev](https://e2b.dev/docs/sandbox/persistence), [docs.openhands.dev](https://docs.openhands.dev/sdk/arch/conversation))

---

## 6. 多 Agent 协作

### 6.1 协作模式

建议支持三种模式：

**串行接力**：Planner -> Coder -> Tester -> Reviewer。
**并行分支**：多个 agent 在 branch workspace 上并行工作。
**仲裁合并**：Reviewer 合并分支并解决冲突。

### 6.2 Workspace 分支

Workspace 分支本质上是 git-like branch + snapshot lineage。每个分支有自己的 snapshot head 和 lock state。合并时优先以 patch / diff 为单位，不直接合并 runtime 内存态。

### 6.3 Actor / Message 机制

多 Agent 通信建议采用消息驱动而不是同步 RPC。AutoGen 的 actor model 提示了正确方向：agent 之间通过异步消息、事件、mailbox 协同，系统更适合分布式、弹性和故障恢复。([microsoft.github.io](https://microsoft.github.io/autogen/stable//user-guide/core-user-guide/index.html))

---

## 7. 事件模型

## 7.1 事件总线原则

所有状态变化都以事件进入 Event Bus，Event Log 采用 append-only。OpenHands 的 Conversation / Agent Server 都强调事件、状态、workspace、runtime services 的分离；OpenHands 还提供 WebSocket 流式事件接口。([docs.openhands.dev](https://docs.openhands.dev/sdk/arch/conversation), [docs.openhands.dev](https://docs.openhands.dev/sdk/arch/agent-server), [docs.openhands.dev](https://docs.openhands.dev/openhands/usage/developers/websocket-connection))

## 7.2 统一事件格式

```json
{
  "event_id": "uuid",
  "event_type": "CommandStarted|CommandFinished|SnapshotCreated|ApprovalRequested|ApprovalGranted|ArtifactEmitted|RuntimeSuspended|RuntimeRecovered",
  "tenant_id": "uuid",
  "session_id": "uuid",
  "task_id": "uuid",
  "workspace_id": "uuid",
  "runtime_id": "uuid|null",
  "timestamp": "iso8601",
  "payload": {}
}
```

## 7.3 关键事件

* TaskCreated
* RuntimeProvisioned
* WorkspaceMounted
* CommandStarted / CommandFinished
* FileChanged
* ArtifactEmitted
* ApprovalRequested / ApprovalGranted / ApprovalDenied
* SnapshotCreated
* RuntimeSuspended / RuntimeRecovered
* TaskSucceeded / TaskFailed / TaskAborted

---

## 8. 存储设计

### 8.1 元数据存储

建议使用关系型数据库保存：

* Session / Task / Workspace / Snapshot / Policy / Artifact 的主数据；
* 状态机当前态；
* 关联关系；
* 幂等键；
* 事件游标。

### 8.2 事件存储

建议使用 Kafka / Pulsar / NATS JetStream 之一承载高吞吐事件流，Topic 按 tenant/session 分区。

### 8.3 Artifact Store

建议用对象存储保存：

* patch；
* 代码快照；
* stdout/stderr；
* 测试报告；
* 截图 / 录屏；
* trace 导出。

### 8.4 Snapshot Store

Snapshot 采用 delta-first：

* base image 只存一次；
* snapshot 存相对 base / parent 的差分；
* 恢复时按 lineage 回放或合成。

Modal 的 filesystem snapshots 和 E2B 的 snapshot 语义都支持这种“差分 + 复用”思路。([modal.com](https://modal.com/docs/guide/sandbox-snapshots), [e2b.dev](https://e2b.dev/docs/sandbox/snapshots))

---

## 9. API 设计

### 9.1 Session API

```http
POST /v1/sessions
GET  /v1/sessions/{session_id}
POST /v1/sessions/{session_id}/pause
POST /v1/sessions/{session_id}/resume
POST /v1/sessions/{session_id}/abort
```

### 9.2 Task API

```http
POST /v1/tasks
POST /v1/tasks/{task_id}/run
POST /v1/tasks/{task_id}/retry
POST /v1/tasks/{task_id}/approve
POST /v1/tasks/{task_id}/split
POST /v1/tasks/{task_id}/merge
```

### 9.3 Workspace API

```http
POST /v1/workspaces
POST /v1/workspaces/{workspace_id}/mount
POST /v1/workspaces/{workspace_id}/snapshot
POST /v1/workspaces/{workspace_id}/restore
POST /v1/workspaces/{workspace_id}/branch
POST /v1/workspaces/{workspace_id}/lock
POST /v1/workspaces/{workspace_id}/unlock
```

### 9.4 Runtime API

```http
POST /v1/runtimes/allocate
POST /v1/runtimes/{runtime_id}/execute
POST /v1/runtimes/{runtime_id}/pause
POST /v1/runtimes/{runtime_id}/resume
POST /v1/runtimes/{runtime_id}/destroy
```

### 9.5 Event API

```http
GET /v1/events?session_id=...
GET /v1/events?task_id=...
GET /v1/replay/{session_id}
```

---

## 10. 安全与治理

### 10.1 权限模型

建议采用三层权限：

* **Identity**：谁在执行；
* **Policy**：能做什么；
* **Approval**：什么时候允许做。

Google 的 Agent Identity / Gateway、AWS AgentCore Identity / Policy / Gateway 都说明，Agent 平台必须把身份与策略做成平台能力，而不是业务代码中的临时逻辑。([docs.cloud.google.com](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/agent-identity-overview), [docs.cloud.google.com](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/gateways/agent-gateway-overview), [docs.aws.amazon.com](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html), [docs.aws.amazon.com](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html))

### 10.2 默认策略

* 默认关闭公网 egress；
* 默认限制写路径；
* 默认限制 shell 命令；
* 默认隐藏敏感 secret；
* 高风险动作必须审批；
* 所有越权事件必须审计。

### 10.3 安全边界

建议在 Runtime 层实现：

* 网络 ACL；
* 文件系统 ACL；
* secret broker；
* prompt injection 防护；
* artifact 输出过滤；
* 任务级审计日志。

---

## 11. 可观测性与回放

### 11.1 观测目标

不是“看见系统在跑”，而是“能证明为什么这样跑”。因此 observability 的目标是：

* 每个 Task 可回放；
* 每个 Snapshot 可追溯；
* 每个 Artifact 可证明来源；
* 每次审批可审计。

### 11.2 观测维度

* trace：Session / Task / Runtime / Command 链路；
* logs：stdout / stderr / system log；
* metrics：启动时延、恢复时延、成功率、重试率；
* timeline：快照点、命令点、审批点；
* diff view：文件变化、patch 变化、依赖变化。

AWS 和 Google 的 Agent 平台都把 runtime、memory、gateway、identity、observability 做成统一监控面，这种做法可以直接借鉴到你的 observability plane。([docs.aws.amazon.com](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-service-provided.html), [docs.aws.amazon.com](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html), [docs.cloud.google.com](https://docs.cloud.google.com/gemini-enterprise-agent-platform/optimize/observability/overview))

---

## 12. 部署建议

### 12.1 推荐拓扑

* Control Plane：K8s 微服务；
* Runtime Fleet：容器池 + microVM 池 + browser 池；
* State Plane：PostgreSQL + Object Storage + Event Bus；
* Observability：OpenTelemetry + 查询后端；
* Policy Service：独立微服务，支持规则版本化。

### 12.2 扩容策略

* Runtime 按队列长度和任务风险分级扩容；
* Snapshot Store 按冷热分层；
* Event Bus 按 tenant/session 分区；
* Workspace 以“任务级孤岛”方式调度。

### 12.3 资源策略

* 短任务优先 container；
* 不可信任务优先 microVM；
* 长时任务必须支持 suspend/resume；
* UI 自动化任务走 browser runtime；
* GPU 任务独立资源池。

Open Agents 的 “Web -> Agent workflow -> Sandbox VM” 与 OpenHands 的 remote workspace / agent server 架构，正好支持这种分层部署。([github.com](https://github.com/vercel-labs/open-agents), [docs.openhands.dev](https://docs.openhands.dev/sdk/arch/agent-server))

---

## 13. MVP 落地范围

### Phase 1：能跑

* Session / Task / Workspace / Snapshot / Policy / Artifact 六对象落库；
* 单 runtime 后端（container）；
* 基础 event log；
* 手动审批；
* snapshot 恢复。

### Phase 2：能稳

* 增加 microVM；
* 网络 / 路径 / secret 规则；
* 自动恢复；
* replay UI；
* artifact provenance。

### Phase 3：能协作

* workspace branching；
* 多 agent 并行；
* reviewer merge；
* actor-driven event bus；
* semantic context 压缩层。

---

## 14. 研发实现上的关键约束

1. **Task 不能依赖 runtime 存活**，只能依赖 session/task id + event log + snapshot head。
2. **Workspace 不能等价于容器文件系统**，否则无法做稳定恢复与分支。
3. **Snapshot 必须是增量对象**，否则成本不可控。
4. **审批必须可恢复**，不能让 pending approval 丢失。
5. **Event Log 必须可重放**，否则无法 debug 长时任务。
6. **Policy 必须版本化**，否则无法审计与回滚。

---

## 15. 结论

Agent Runtime Fabric 的研发实现，可以被概括为：

> **把 Agent 从“单次执行的聊天程序”，改造成“以 Session/Task 为控制对象、以 Workspace/Snapshot 为持久对象、以 Policy/Identity 为治理对象、以 Event/Trace 为观测对象的持久化执行织网”。**

这条路线不是概念化堆砌，而是已经被 OpenAI、Google、AWS、E2B、Modal、OpenHands、AutoGen、Open Agents 等不同方向的实现逐步验证的共同收敛点。([developers.openai.com](https://developers.openai.com/api/docs/guides/agents), [docs.cloud.google.com](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime), [docs.aws.amazon.com](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html), [e2b.dev](https://e2b.dev/docs/sandbox/persistence), [modal.com](https://modal.com/docs/guide/sandboxes), [docs.openhands.dev](https://docs.openhands.dev/sdk/arch/conversation), [microsoft.github.io](https://microsoft.github.io/autogen/stable//user-guide/core-user-guide/index.html), [github.com](https://github.com/vercel-labs/open-agents))

如果你要继续，我下一步可以把这份详细设计直接拆成研发可执行的三份交付物：**数据库 DDL、事件 Schema、以及服务接口 OpenAPI 草案**。

