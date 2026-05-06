撰写《Agent Runtime Fabric（智能体执行织网）》方案，包括总体架构图、核心对象模型（Task / Session / Workspace / Snapshot / Policy / Artifact）、以及Runtime生命周期状态机等等。

# Agent Runtime Fabric（智能体执行织网）：一个以控制面为大脑、以可恢复工作区为身体、以快照和策略为记忆边界、以事件流为神经系统的 Agent 执行基础设施。这比“Agent inside Sandbox”更准确，也比“单纯 remote shell”更能支撑复杂软件工程、长时任务、并发协作和安全治理。([OpenAI Developers][2])

控制面负责思考与编排，执行面负责无状态/弱状态执行（计算），持久化状态、快照、权限和观测都外置为独立基础设施”。OpenAI、Anthropic、OpenHands、Modal、E2B 等主流实现共同收敛出来的方向：编排与执行分离、workspace 独立化、快照可恢复、网络与权限可控、任务可后台并行运行。([OpenAI Developers][1])

> Agent Runtime Fabric 的候选名称： Adaptive Agent Operating System (自适应智能体操作系统)。
> Agent底层设施，本质上是一个以 LLM 为 CPU，以 Prompt 为指令集，以 MCP/ACI 为系统调用，以带有时间旅行能力的 Snapshot Workspace 为硬盘的分布式操作系统.


## 核心对象模型 (Core Object Model)
- Session: 用户的宏观目标（如“开发一个 Chrome 插件”）。
- Task/Sub-task: 拆解后的具体任务流。
- Workspace (W-Volume): 分布式、带版本控制的持久化工作区（不仅是文件，含依赖缓存和环境变量）。
- Snapshot (Delta): 秒级的增量执行点（内存+文件系统 diff）。


## **Agent Runtime Fabric（智能体执行织网）核心是五个彼此解耦的平面：

### **1）Control Plane：Agent Brain / Orchestrator**
负责规划、分解任务、选择模型、决定是否需要新Runtime、是否要回滚、是否要人工审批；它只保留对话态、任务态和策略态，不直接承载危险执行。OpenAI 的 Agents SDK 把“应用拥有编排、工具执行、审批和状态”作为职责边界，Codex 的云模式支持在自己的云环境里后台并行处理任务。([OpenAI Developers][2])

- 任务级生命周期管理：Agent不再绑定某个容器的存活，而是绑定一个 task/session ID；Runtime死了，Agent 还能从事件日志和快照恢复，甚至换模型接管同一工作区。E2B 的 pause/resume、Firecracker snapshot restore、OpenAI 的 background cloud tasks 都说明这条路线已经成立。([e2b.dev][8])

- Router & Planner: 将大任务拆解为小 Task，路由给最适合的异构大模型（如复杂的架构设计给 GPT-4o/Claude-3.5-Sonnet，简单的代码重构给 Qwen-Coder 等）。
- Context Manager: 负责记忆管理、Token 截断、长文本日志的自动摘要压缩，确保送入 LLM 的 Prompt 永远保持高信息熵。


### **2）Execution Plane：Workspace / Sandbox Fleet**
Runtime只提供文件系统、shell、网络、端口、依赖安装、测试运行等能力；它应该是可丢弃、可重建、可暂停、可克隆的工作区。OpenHands 的 runtime / agent server、Modal Sandboxes、E2B 的 pause/resume，都在朝这个方向做：workspace 独立、执行隔离、状态可恢复。([docs.openhands.dev][3])

- Pluggable Compute Pool:
	- 信任任务/轻量代码 -> Wasm Sandbox / 极轻量级 gVisor 容器。
	- 重度编译/不可信代码 -> Firecracker MicroVM (毫秒级拉起)。
	- UI 交互任务 -> Headless Browser Sandbox。
	- 深度学习任务 -> Serverless GPU 实例。
- 动态挂载: 计算资源本身是极其“无脑”和短暂的，启动时秒级挂载下方的 W-Volume。


#### **2.1） Runtime随时可销毁，但 Workspace 作为独立的分布式文件系统（如类似高性能缓存盘）被动态挂载。快照不应该全量备份，采用写时复制类的增量快照，解决真实任务海量产物数据、频繁拉起Runtime、控制面之间搬运文件状态导致的网络I/O延迟和成本灾难问题。**

#### **2.2) workspace-first
真正决定 SWE-bench 这类任务成功率的，不是对话多长，而是 workspace 是否完整：仓库、依赖、构建缓存、测试产物、日志、端口、浏览器状态、快照历史都在同一个可恢复工作区里。OpenAI 的 sandbox 指南已经把“目录、文件、命令、产物、端口、暂停后恢复”列为核心适用场景。([OpenAI Developers][1])**

#### **2.3） “Runtime”是可插拔执行后端**。
比如低风险任务用docker或gVisor，脏活累活、第三方依赖、编译不稳定、可能跑恶意代码的任务用 microVM；需要浏览器操作则挂 browser sandbox；需要 GPU 则挂 GPU execution pool。 Modal 和 Firecracker 的路线说明：高隔离、快启动、快快照、强观测，才是面向 Agent 的基础设施形态。([Modal][7])


### **3）State Plane：Event Log + Snapshot + Artifact Store**【分水岭】
“状态外置”：任务事件日志、文件/内存快照、产物与diff等。Firecracker 的 snapshot 机制可以序列化运行中的 microVM 并在之后恢复到同一时刻，E2B 支持连同内存一起 pause/resume，Modal 则把 memory/filesystem snapshots 作为核心原语。([GitHub][4])

#### 3.1）在控制面与状态面之间，增加Semantic Context Plane（语义上下文层）。当日志过长时，自动使用小模型（如本地模型）对 stdout 报错进行提炼总结，将G级别的系统日志压缩成KB级别的关键上下文，再喂给大模型。

#### 3.2）多智能体并发协同：引入 Workspace 状态锁 (Stateful Locks) 和 分支机制 (Git-like Branching for Workspaces)。不同 Agent 在克隆的 Workspace 副本（Branch）中工作，最终由 Reviewer Agent 合并状态。

#### 3.3）Workspace Volumes (W-Volume): 采用类似 ZFS 或 Btrfs 的底层技术，天然支持写时复制（CoW）。Agent 执行的每一步自动打上一个极低成本的 Delta-Snapshot。
#### 3.4）Event & Artifact Broker: 类似 Kafka 的事件总线，记录每一个 CLI 命令、API 调用结果和编译产物。




**4）Policy Plane：Least-Privilege + Approval + Egress Control**
Runtime不只是隔离，更要“可声明权限”。默认拒绝网络、限制写路径、限制命令白名单、限制密钥暴露、对高风险动作走审批流。OpenAI 明确把 sandbox boundary 和 approval policy 分开；Anthropic 也把工具分成 client tools 和 server tools，强调“哪里执行”是安全模型的一部分；Modal 则把 granular outbound networking control 作为Runtime能力。([OpenAI Developers][5])

Egress Control: 极细粒度的沙箱网络出口管控（仅白名单域名可通信）。
Semantic Firewall (LLM防火墙 ): 拦截沙箱执行结果中潜在的 Prompt 注入（防止 Agent 读取带有恶意指令的 Readme 后叛变）。
Human-in-the-Loop (HITL) 审批卡点: 对于如 git push、npm publish 或涉及生产数据库的动作，自动挂起状态机，等待控制面回调人类授权。


**5）Observability Plane：Replayable Execution**
真正能把复杂项目跑稳的，不是“多聪明”，而是“可追踪、可回放、可复盘”。每条命令、stdout/stderr、文件变更、失败原因、快照点都应该结构化记录。OpenHands 的 agent server 会通过 WebSocket 流事件，Codex 也把 sandbox 边界、审批和命令行为明确化；这意味着未来的 Agent Runtime 必须像分布式系统一样可观测。([docs.openhands.dev][6])

Time-Travel Debugging (时间旅行调试): 既然所有状态都外置且快照化，开发者可以随时在 UI 界面上拖动时间轴，瞬间恢复到 10 分钟前 Agent 报错的那个 VM 现场，由人类直接进入 Web Terminal 进行人工修复，修复后 Agent 再次接管接力棒。


**6) 控制面与执行面等之间的交互协议、标准化工具协议**
未来控制面与执行面的边界，不会只靠“内部SDK调用”，而会越来越像 MCP / tool-use / ACI 这样的标准协议：模型发出结构化工具调用，宿主或远端服务执行，再把结果回传。OpenAI 已经把 remote MCP 和 connectors 做成正式能力，Anthropic 也明确区分了由应用执行的 client tools 与由平台执行的 server tools。([OpenAI Developers][9])



## 从架构形态上的图：

```text
User / IDE / API
      |
      v
Control Plane
(planner, memory, policy, router, reviewer)
      |
      v
Runtime/Execution Fabric
[microVM sandbox] [container sandbox] [browser sandbox] [GPU job sandbox]
      |
      v
State Services
(event log, snapshots, artifacts, git patches, secrets broker, audit)
```

示例：
** 执行中： 控制面发令，MicroVM (执行面) 挂载 Workspace 执行 npm run build。
** 崩溃发生： 依赖冲突导致进程死锁，内存溢出，MicroVM 宕机。
** 秒级恢复：
	State Plane 捕获心跳丢失事件。
	Observability Plane 提取死锁前最后 100 行报错，Context Manager 提炼为 200 个 Token 的总结。
	控制面大脑收到总结，反思：“内存不足或配置错误”。
	控制面下发新策略：要求拉起一台内存翻倍的 MicroVM，从崩溃前的 Snapshot 瞬间恢复 Workspace，并附带修复命令 npm cache clean --force，任务继续。




[1]: https://developers.openai.com/api/docs/guides/agents/sandboxes "Sandbox Agents | OpenAI API"
[2]: https://developers.openai.com/api/docs/guides/agents "Agents SDK | OpenAI API"
[3]: https://docs.openhands.dev/openhands/usage/architecture/runtime "Runtime Architecture - OpenHands Docs"
[4]: https://github.com/firecracker-microvm/firecracker/blob/main/docs/snapshotting/snapshot-support.md "firecracker/docs/snapshotting/snapshot-support.md at main · firecracker-microvm/firecracker · GitHub"
[5]: https://developers.openai.com/codex/concepts/sandboxing "Sandbox – Codex | OpenAI Developers"
[6]: https://docs.openhands.dev/sdk/guides/agent-server/overview "Overview - OpenHands Docs"
[7]: https://modal.com/solutions/coding-agents "Solutions - Coding agents | Modal"
[8]: https://e2b.dev/docs/sandbox/persistence "Documentation - E2B"
[9]: https://developers.openai.com/api/docs/guides/tools-connectors-mcp "MCP and Connectors | OpenAI API"
