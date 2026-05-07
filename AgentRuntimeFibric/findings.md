# AgentRuntimeFabric Findings

## File Inventory

- `insight-v1.md`: 企业架构文档雏形，覆盖背景、目标、非目标、五平面、六对象、runtime 状态机、API、事件、安全、观测、部署、roadmap。
- `insight-v2.md`: 对五平面职责和对象语义的精炼版，强调 control/execution/state/policy/observability 解耦，runtime 可插拔，workspace/snapshot 是恢复与协作基础。
- `insight-v3.md`: 偏概念与行业类比，补充 Semantic Context Plane、分支/锁、多智能体协同、可插拔 compute pool、HITL、Semantic Firewall、标准协议边界。
- `insight-v4.md`: 技术对标分析，强调行业从“会调用工具”走向“会运行工作流”；OpenAI/Google/AWS/E2B/Modal/Daytona/OpenHands/AutoGen 分别验证编排、治理、pause/resume、snapshot、低延迟 stateful sandbox、workspace lifecycle、actor event model 等能力。
- `insight-v5.md`: 面向研发实现的详细设计，提出 7 个物理服务域、六对象字段、runtime 类型、正常执行/失败恢复流程、多 Agent 协作、事件模型、存储设计、API、默认安全策略、部署建议和三阶段 MVP。
- `AgentRuntimeFabric-v2.md`: 当前最强目标架构，升级为 durable workflow kernel + runtime adapter contract + workspace lineage + governance fabric；拆分 WorkflowRun / Task / ExecutionLease / RuntimeInstance 生命周期；定义 RuntimeAdapter、RuntimeCapabilities、PolicyDecision、A2AEnvelope、Semantic Context Plane、Replayable Event Fabric、Phase 0-5 演进路线。
- `AgentRuntimeFabric-Solution.md`: 综合方案，补齐业务场景、问题挑战、AgentOps Layer、KnowledgeBase、Skill Registry、关键技术、部署拓扑、Phase 1-4 MVP，以及风险缓解矩阵。相对 v2 更重产品与场景表达，但生命周期模型仍偏早期，需要以 v2 的四层生命周期拆分修正。

## Extracted Concepts

- 已有材料共同收敛到：Control Plane / Execution Plane / State Plane / Policy Plane / Observability Plane。
- 核心对象稳定为：Session、Task、Workspace、Snapshot、Policy、Artifact。
- `Workspace` 是长期状态与协作边界；`Runtime` 是短生命周期、可替换的执行资源。
- `Snapshot` 是恢复、分支、回放的原语，应优先支持增量、可恢复、可分叉。
- `Event Log` 是可观测、审计、回放和恢复编排的事实源。
- `Policy` 必须外置且声明式，覆盖命令、路径、网络、密钥和审批。
- `Semantic Context Plane` 在 insight-v3 中被引入，用于把长日志、错误和产物压缩为可用于 LLM 决策的高信息上下文。
- v2 新增稳定对象：AgentSpec、AgentActor、EnvironmentSpec、WorkflowRun、ExecutionLease、RuntimeInstance、WorkspaceBranch、PolicyDecision、Approval、SecretGrant、ToolCall、A2AEnvelope、Event。
- v2 新增稳定边界：Workflow Boundary、Computer Boundary、Governance Boundary、Protocol Boundary、Collaboration Boundary、Context Boundary、Evidence Boundary。
- RuntimeAdapter 必须提供能力声明、allocate/connect/reconnect/mount/execute/stream/open_port/snapshot/restore/pause/resume/teardown，并返回结构化事件。
- Governance Fabric 明确 UserIdentity、AgentIdentity、ToolIdentity、RuntimeIdentity、SecretIdentity 分层；高风险动作默认审批；SecretBroker 和 EgressGateway 为平台能力。
- Workflow Kernel 负责 durable state machine、Task DAG、checkpoint、retry、timeout、approval wait、runtime lost、compensation、handoff/review/merge。
- Solution 文件新增业务需求：复杂软件工程、长时后台任务、多 Agent 并发协作、浏览器/UI 自动化、数据/GPU 任务、高安全执行环境、AgentOps 团队协作、知识库与技能复用。
- Solution 文件新增产品入口：AgentOps Layer 只通过 Session/Task/Approval/Comment/Blocker API 影响执行，不能直接调用 Runtime。
- Solution 文件新增复用闭环：KnowledgeBase 是上下文来源，Skill/Playbook 是成功任务沉淀，但二者都不能绕过 Policy。

## Requirements and Gaps

- 早期文档把 Runtime 与 Task 状态机混在一起；最终设计需要拆成 WorkflowRun/TaskRun、ExecutionLease、RuntimeInstance、WorkspaceSnapshot 等不同生命周期。
- 已有 API 示例较粗，需要补输入输出契约、幂等键、错误码、状态转移前置条件和稳定版本边界。
- 已有路线给出 Phase，但缺少每阶段交付件、使用者、成功标准和明确不做事项。
- 需要明确哪些模块是核心必建，哪些是可复用库/适配器，哪些依赖外部系统。
- `AgentRuntimeFabric-v2.md` 的 Phase 0-5 可作为阶段基础，但用户要求更清楚“谁使用、解决什么问题、成功标准、哪些不做”，需扩展成交付矩阵。
- `AgentRuntimeFabric-Solution.md` 的 Phase 1-4 与 v2 Phase 0-5 命名不完全一致；最终文档应统一为 Foundation -> Lease/Daemon -> Governance -> Collaboration -> Multi-backend -> Knowledge/Replay 的阶段序列。

## Architecture Synthesis Notes

- 文档应采用“需求可验证 -> 模块边界 -> 对象模型 -> 协议契约 -> 状态机 -> 实现阶段”的顺序，便于后续 Codex 按任务拆解开发。
- 最终文档应明确“事实源”和“投影”的区别：EventLog / Workspace / Snapshot / Artifact / PolicyDecision 是事实；日志摘要、ContextIndex、Skill 建议是投影。
- 保留六平面 + AgentOps，但把 Durable Workflow Kernel 放在 Control Plane 与 State Plane 之间作为内核；把 Policy Plane 升级为 Governance Fabric。
- 针对“基于现有开源项目的堆加和重构”，最终设计应采用防腐层：OpenHands/Vercel Open Agents/AutoGen/Temporal/MCP/OPA/Vault/OpenTelemetry 等可以复用能力，但不能把其内部对象泄漏为 AgentRuntimeFabric 核心对象。
- 每个外部项目接入都应通过 contract tests 和 mapping ADR，稳定输出 Event、RuntimeAdapter、ToolCall、A2AEnvelope、PolicyDecision、SecretGrant 等内部契约。

## 2026-05-06 Re-synthesis Addendum

- Re-read all local source files and confirmed the main consolidated document already covered most requested sections, but needed stronger traceability from source documents to final decisions.
- Added a source-material distillation table to distinguish adopted concepts, corrected assumptions, and deliberately delayed product capabilities.
- Added a requirements traceability matrix mapping R1-R14 to owner modules, stable objects/interfaces, required tests, and first delivery phase.
- Added a reusable requirement decomposition template so future Codex issues have explicit inputs, outputs, state transitions, events, policy checks, errors, idempotency, tests, non-goals, and reusable artifacts.
- Added module interaction chains for normal execution, runtime recovery, high-risk approval, multi-agent branch collaboration, and Knowledge/Skill use.
- Added module write-boundary ownership to prevent hidden coupling through shared state.
- Verified current official/reference docs for the open-source stacking direction at a high level; refined the implementation route by separating directly embeddable open-source components, adapter backends, implementation references, hosted replacements, and industry references.

## 2026-05-06 GitHub/Open-source Selection Addendum

- GitHub and official docs research indicates no single open-source project should become the ARF base. The strongest implementation route is a composable core with stable ARF contracts and multiple adapters.
- P1 influences for the first implementation slice: OpenAI Agents SDK concepts, Codex CLI as an external coding-agent adapter, Vercel Open Agents as product/workflow reference, OpenHands Runtime as sandbox/action executor reference, MCP SDK as ToolGateway protocol, Docker/gVisor as the local runtime backend.
- P2 adapter candidates after MVP: E2B, Modal Sandboxes, Daytona, and gVisor hardening. These are useful for snapshot, pause/resume, workspace lifecycle, port, and remote execution capability comparison.
- P3/P4 references: AutoGen/Microsoft Agent Framework, A2A, AgentPool, AG-UI, Warp, Firecracker, Google ADK/Gemini Enterprise, and AWS Bedrock AgentCore samples. These should not block the MVP and should enter only through mapping ADRs, protocol bridges, or UX/security references.
- The updated ARF base choice is: self-built minimal Harness, DB outbox workflow kernel, Docker/gVisor runtime adapter, self-built sandbox-daemon, Git worktree + fs snapshot manifest, MCP gateway, internal A2AEnvelope, YAML policy/fake broker, and EventLog-first observability.
- Added dependency admission standards: license review, schema anti-corruption, contract tests, security checks, operability, maintenance, and cost. Any project that leaks external schema into ARF public API or requires cloud credentials for the minimal recovery demo should be blocked from the MVP path.
- Codex implementation should begin with contract tests and fake adapters, then Docker/gVisor, sandbox-daemon lease enforcement, read-only MCP gateway, Codex adapter, and only then OpenHands/E2B/Modal/Daytona/A2A/AgentPool spikes.

## 2026-05-07 Industry Differentiation Research Addendum

- Re-read `AgentRuntimeFabric-Architecture-Implementation.md` and `AgentRuntimeFabric-Architecture-Implementation-v2.md`. Both documents already cover durable workflow, workspace lineage, execution leases, runtime adapters, policy decisions, replay, and open-source stacking. The weakness is not missing architecture vocabulary; the weakness is that many named capabilities already exist in mainstream/frontier systems, so ARF cannot claim differentiation merely by listing them.
- User clarified that the goal is to build an open-source alternative. Closed-source/proprietary platforms may already implement these capabilities; the gap can still be valid if no corresponding open-source project exposes the same control plane, schemas, and self-hosted deployment path. This changes the positioning from "globally unique capability" to "open-source replacement for validated closed-source agent runtime fabrics plus missing open-source glue across existing components."
- OpenAI Agents SDK positions itself as code-first orchestration where the application owns tools, MCP, runtime behavior, state, approvals, and traces. Its docs also call out sandbox agents for files, commands, packages, snapshots, mounts, and provider links. ARF should not compete as another agent SDK; it should integrate SDKs as Harness/AgentActor frontends and own the execution evidence/governance layer underneath.
- OpenAI Codex is a mature terminal coding agent that reads, modifies, and runs code locally. ARF should not fork or replace Codex; the stronger route is to treat Codex-like agents as external AgentActors that must execute through ARF's lease, workspace, event, and artifact contracts.
- LangGraph already offers persistence, checkpoints, durable execution, human-in-the-loop, time travel, and fault tolerance. Temporal already offers durable execution through event history and deterministic replay. Therefore durable workflow alone is not ARF differentiation. ARF must add code-workspace semantics, sandbox lifecycle, policy lease, artifact lineage, and cross-backend adapter contracts.
- Vercel Workflow and Vercel Open Agents already combine durable agent workflows with sandbox VM execution and GitHub coding flow. They validate ARF's direction but reduce ARF's uniqueness. ARF must be more portable/self-hosted, vendor-neutral, and stricter about event evidence, policy decisions, and runtime backend anti-corruption.
- AWS Bedrock AgentCore now exposes a broad managed platform: Runtime, Memory, Gateway, Identity, Code Interpreter, Browser, Observability, Evaluations, Policy, and Registry. This is the strongest enterprise counterexample. ARF's differentiator cannot be "enterprise agent platform"; it must be "open, self-hostable change-control runtime fabric for code-changing agents, with inspectable schemas and replaceable backends."
- E2B, Modal, Daytona, and Vercel Sandbox already provide strong sandbox/workspace primitives, including filesystem and in some cases memory snapshots or pause/resume. ARF should not overclaim snapshot technology. It should normalize capabilities through `RuntimeCapabilities`, record exact `SnapshotClass`, and build recovery/provenance semantics above those providers.
- OpenHands already has a practical Docker runtime/action executor with shell, file, browser, Jupyter/plugins, event stream, remote/Modal/Runloop runtime variants, and image tagging. ARF should reuse it as an implementation reference or adapter, but not expose its action/event schema as ARF public schema.
- MCP is the mainstream tool integration protocol, but the spec explicitly leaves security enforcement to implementors and treats tools as arbitrary execution surfaces requiring consent. ARF's opportunity is to make every MCP call pass through `ToolCall + PolicyDecision + SecretGrant + Artifact provenance` rather than treating MCP authorization as solved.
- A2A is the emerging agent interoperability protocol with AgentCard, Task, Message, Artifact, streaming, push notifications, and opaque agent collaboration. ARF should bridge A2A externally but keep an internal replayable mailbox with ack, deadline, retry, policy, branch, and snapshot references.
- AG-UI standardizes event-based agent-to-user interaction. ARF should map EventLog projections to AG-UI for UI, but UI event streams must not become execution facts.
- The reconstructed ARF differentiators should be explicit and testable:
  1. `EvidenceGraph`: a typed graph linking events, actions, diffs, snapshots, artifacts, policy decisions, approvals, identities, secret grants, tool calls, and runtime instances.
  2. `PolicyBoundExecution`: every shell/MCP/network/secret/Git/PR action requires a short-lived lease backed by a versioned policy decision, and sandbox daemon/tool gateway reject bypasses.
  3. `WorkspaceLineageForAgents`: branches, locks, snapshots, merge decisions, test artifacts, and review decisions form a portable workspace history independent of Git branch or sandbox id.
  4. `RuntimeAntiCorruption`: Docker/gVisor/OpenHands/E2B/Modal/Daytona/Firecracker capabilities enter only through `RuntimeAdapter` and `RuntimeCapabilities`, with contract tests and schema lint.
  5. `AgentChangeControl`: optimized first use case for code-changing agents: kill-and-recover, approval without runtime occupancy, audit timeline, and reproducible debug restore.
  6. `OpenControlPlane`: self-hostable local demo and open schemas; cloud platforms can be adapters, not mandatory control planes.
