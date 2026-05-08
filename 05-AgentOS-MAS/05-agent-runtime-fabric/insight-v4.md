# 《技术对标与借鉴分析》

这部分的核心结论很明确：你要做的 **Agent Runtime Fabric**，并不是把 Agent “放进沙箱”，而是把 Agent 运行时升级成一套**可恢复、可审计、可治理、可并发协作**的基础设施。当前主流技术路线已经非常一致：**控制面负责编排、审批、路由、记忆和观测；执行面负责在隔离 workspace/sandbox/microVM/container 中跑代码、装依赖、开端口、执行长任务；状态面负责事件、快照和产物持久化**。OpenAI 的 Agents SDK、Codex、Sandbox，Google 的 Gemini Enterprise Agent Platform，AWS 的 Bedrock AgentCore，E2B、Modal、Daytona、OpenHands、AutoGen、Open Agents 都在不同维度上推动这个收敛。([OpenAI Developers][1])

## 1. 对标结论：这条赛道已经从“会调用工具”走向“会运行工作流”

OpenAI 的 Agents SDK 明确把职责边界写成：当应用自己负责 orchestration、tool execution、approvals 和 state 时，就该用 Agents SDK；它的 sandbox 指南进一步说明，sandbox 是为了承载依赖 workspace 内工作成果的任务，而不是单次问答。Codex 则把这种模式继续推向后台化、并行化和项目级执行。这个信号很重要：Agent 的单位已经从“对话轮次”变成“可持续运行的任务/会话”。([OpenAI Developers][1])

Google 和 AWS 则把这件事平台化了。Google 的 Agent Runtime 直接定位为部署、管理、扩展 AI agents 的生产服务，Agent Gateway 负责身份、访问策略、协议中介和网络层观测；AWS AgentCore 则把 Runtime、Memory、Gateway、Identity、Policy、Observability 作为完整平台能力，并提供 Browser runtime 等内建执行环境。换句话说，业界已经默认：Agent 基础设施不能只靠“模型 + 工具”拼起来，必须有独立的治理和运行平台。([Google Cloud Documentation][2])

## 2. 分技术对标：每一类技术分别补了哪一块短板

### 2.1 OpenAI Agents SDK + Codex：把“应用拥有控制权”这件事说清楚了

OpenAI Agents SDK 的价值，不在于多了一个 agent 框架，而在于它把系统分工定死：**编排、执行、审批、状态由应用拥有**，模型只是其中一个可替换组件。Codex 则进一步把 sandbox、approvals、remote connections、worktrees、后台执行、并行任务这些能力组合进项目级工作流里。对你的方案来说，这意味着控制面不能只是“planner”，而要真正持有 Session/Task 的生命周期控制权。([OpenAI Developers][1])

### 2.2 OpenAI sandbox：把执行边界和审批边界拆开了

OpenAI 对 sandbox 的定义很关键：当答案依赖 workspace 里的实际工作结果时，就该用 sandbox；它特别强调目录、文件、命令、artifact、端口和暂停后恢复这些场景。它还明确表示，sandbox boundary 和 approval policy 是两件事：前者定义“在哪里执行”，后者定义“何时允许越界”。这对你的 Policy Plane 设计非常直接。([OpenAI Developers][3])

### 2.3 E2B：把 pause/resume 做成了真正的状态原语

E2B 最有借鉴价值的是它把 persistence 做到“连 memory 一起恢复”，并且 snapshot/恢复不会改变 sandbox ID；它还提供生命周期事件，能追踪 sandbox 被创建、暂停、恢复、快照、销毁等状态变化。对 Agent Runtime Fabric 来说，这说明 **Snapshot 不是备份功能，而是运行时状态机的一部分**。([E2B][4])

### 2.4 Modal Sandboxes：把 snapshot 做成了差分与复用

Modal 的 sandbox 文档强调，它是执行不可信代码的安全容器；filesystem snapshots 是某一时刻文件系统的副本，可以直接拿去创建新的 sandbox。它还支持 volume 复用和目录级快照，这说明 Modal 走的是**delta-first / reusable state** 路线，而不是全量复制路线。对你来说，这正好支持 Workspace-first 与增量 Snapshot 的设计。([Modal][5])

### 2.5 Daytona：把“快、态、并发、REST 化”做成产品特征

Daytona 强调 fast、scalable、stateful，官网直接给出 sub-90ms sandbox creation，并把 process execution、file system operations、git integration、并行环境下的 state persistence 作为核心能力。它的产品方向说明：Agent runtime 需要兼顾低延迟拉起、长时持久、并行执行和可恢复状态。对你的方案而言，Runtime Pool 的目标不应只是高隔离，还应包括**快速创建、稳定驻留、并发扩展和快照复用**。([Daytona][6])

### 2.6 OpenHands Runtime / Conversation：把生命周期、状态和 workspace 绑定在一起

OpenHands 的 Conversation 体系把四个责任写得非常清楚：agent 生命周期管理、状态编排、workspace 协调、runtime services。它的 persistence 也明确记录 message history、agent configuration、execution state、tool outputs 和 statistics。这说明 OpenHands 的思路不是“agent 工具调用层”，而是“agent 运行系统”。对你的方案，这几乎可以直接映射成 Session/Task/Workspace/Artifact/EventLog 的对象模型。([OpenHands Docs][7])

### 2.7 AutoGen：补上了事件驱动与 actor/runtime 的多 Agent 协作视角

AutoGen Core 明确采用 actor model，并把系统定位成 event-driven、distributed、scalable、resilient；它的 MCP adapter 又把远程 MCP 服务、云工具、Web API 统一成可接入的工具层。对你的方案，这个启发很重要：多 Agent 协作不应该靠 prompt 中的角色扮演，而应该靠**actor identity、异步消息、事件流和显式生命周期**。([Microsoft GitHub][8])

[1]: https://developers.openai.com/api/docs/guides/agents "Agents SDK | OpenAI API"
[2]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime "Agent Runtime  |  Gemini Enterprise Agent Platform  |  Google Cloud Documentation"
[3]: https://developers.openai.com/api/docs/guides/agents/sandboxes "Sandbox Agents | OpenAI API"
[4]: https://e2b.dev/docs/sandbox/persistence "Documentation - E2B"
[5]: https://modal.com/docs/guide/sandboxes?utm_source=chatgpt.com "Sandboxes | Modal Docs"
[6]: https://www.daytona.io/ "Daytona - Secure Infrastructure for Running AI-Generated Code"
[7]: https://docs.openhands.dev/sdk/arch/conversation "Conversation - OpenHands Docs"
[8]: https://microsoft.github.io/autogen/stable//reference/python/autogen_ext.tools.mcp.html?utm_source=chatgpt.com "autogen_ext.tools.mcp — AutoGen"
