# PSI Research Findings

## Source Inventory

- `00-insight-why-project-Psi.md`
- `01-insight-what-is-project-Psi.md`
- `02-insight-Psi-vs-Pi.md`
- `03-insight-Pi-Deep-Research.md`
- `04-feasibility-Psi-Project-Assessment.md`
- `05-insight-Psi-Microkernel-Strategy.md`
- `06-insight-Psi-Intelligence-Amplifying-Scaffold.md`

## Article Notes

### `00-insight-why-project-Psi.md`

- PSI 被命名为 Pi 的 runtime 演进态，强调 cognition、state、dynamics、system evolution。
- 目标气质：极简、高级、AI-native、不像框架、更像系统内核。
- 候选 slogan：`A minimal runtime for continuous agents.` / `Thin runtime. Persistent execution.`

### `01-insight-what-is-project-Psi.md`

- 已有正式架构草案将 PSI 定位为“极简任务执行型 Agent Runtime”，目标是持续执行、可恢复、可审计、工具原生、薄壳演进。
- 核心链路：`TaskSpec -> ExecutionLoop -> ToolRegistry -> Observation -> StateStore -> ExecutionLoop`。
- 核心模块：TaskSpec、ExecutionLoop、ToolRegistry、StateStore/Log、Minimal Safety Gate。
- 重要原则：薄壳优先、单主链路、结构化优先、可恢复/可回放/可追责。
- 对 computer use 的处理方式是作为 ToolRegistry 的一类工具，而非独立平台；设计阶段和并行能力也应保持为 loop 内自然行为，而不是中心化平台模块。

### `02-insight-Psi-vs-Pi.md`

- 文章判断 PSI 与 Pi 理念同源：模型优先、薄 harness、tool-native、让模型自己长能力。
- PSI 与 Pi 的区别：Pi 更偏 coding harness，PSI 想成为 general task runtime；Pi 状态层偏 session，PSI 强调 durable execution；Pi 更像 interactive coding session，PSI 面向 long-running/resumable runtime。
- 对 PSI 的关键启发：系统应该小到模型能理解，不要过早抽象，把 extension surface 作为核心能力而不是内建大量 feature。

### `03-insight-Pi-Deep-Research.md`

- Pi 被描述为极简终端编码代理工具，强调 radical minimalism、model-first、extensibility over features，以及默认开放的 YOLO 安全哲学。
- Pi 架构包括 `pi-ai`、`pi-agent-core`、`pi-tui`、`pi-web-ui`、`pi-coding-agent`，其核心 agent loop 极简。
- Pi 的四工具设计是 `read/write/edit/bash`，论点是极少工具降低上下文消耗并提升可靠性，bash 覆盖大量命令行能力。
- 重点借鉴：系统应小到模型能理解；extension surface 比内建 feature 更重要；渐进式上下文加载优于一次性注入；树结构会话和 JSONL append-only 对 PSI 的 StateStore 有直接启发。
- PSI 应超越 Pi 的方向：general task runtime、durable execution、minimal safety gate、轻量子 loop 并行、结构化 TaskSpec/验收标准。

### `04-feasibility-Psi-Project-Assessment.md`

- 文章给出克制结论：技术方向正确但市场拥挤；不建议以“爆款开源”或替代 Pi 为目标；建议以个人研究、内部基础设施或垂直扩展为目标推进。
- 必要性判断：真实需求存在，但窗口正在收窄。框架太厚和 durable execution 缺口成立；general-purpose runtime 只部分成立，因为行业更常见的是专用 agent。
- 差异化空白：轻量级本地 durable execution、跨场景统一 loop、开发者可控安全边界、Go/Rust 极简 runtime。
- 明确不建议：替代 Pi、泛化“Minimal Agent Runtime”、以 GitHub 爆火为唯一目标、同时做重型 AgentRuntimeFabric 与 PSI、重写成熟 LLM 抽象层。
- 可行路线：极窄定位为 `Durable Local Agent Loop with Safety Gate`；SDK/library 优先；核心只做 append-only log + checkpoint/resume、安全门、跨场景工具适配。

### `05-insight-Psi-Microkernel-Strategy.md`

- 将 PSI 进一步收敛为 Agent Microkernel，而非终端应用或全能平台。
- 三个设计哲学：Loop-first、Plugin-everything、State-is-Truth。
- The Core 5：TaskSpec、ToolRegistry、StateStore & Event Log、Minimal Safety Gate、ExecutionLoop。
- 关键实现策略：JSONL append-only 重水化，零业务逻辑污染，Go/Rust 优先，TypeScript 仅作为快速验证选项。
- 战略定位：反框架中间件，竞品不是 Pi/Cline 终端产品，而是复杂自研编排代码和重型框架。
- 建议 killer demos：Durable Backend Agent、Safe Coding Agent、Browser Automation。

### `06-insight-Psi-Intelligence-Amplifying-Scaffold.md`

- 进一步提出 PSI 的叙事应从 `durable execution runtime` 升级为 `intelligence-amplifying runtime for continuous agents`。
- 区分补偿型脚手架与智能放大型脚手架：前者替弱模型规划/路由/编排，后者改善强模型的目标、状态、工具、反馈、记忆、分支和边界。
- 提出智能放大的七个面向：理解、行动、反馈、记忆、自我修正、边界感、自我扩展。
- 建议 PSI 保持 Core 5，但将其重新解释为智能放大模块：TaskSpec 是任务事实，ToolRegistry 是行动语义地图，EventLog 是工作记忆，SafetyGate 是清晰边界。
- 建议新增薄接口 `ContextBuilder`，只定义上下文装配契约，不把 memory/RAG/summary 策略做进 core。
- 给出新增功能的检查表：是否对模型可见、是否减少 hidden state、是否提升 observation、是否让失败可恢复、是否可通过 schema/event/hook/skill/extension 外置。

## Cross-Cutting Findings

- PSI 的核心方向不是“另一个 agent framework”，而是“可持续执行的薄 runtime”。
- 最主要张力：越薄越符合模型优先和可生长哲学，但 durable execution、审计、安全和 general task 能力会自然推高系统复杂度。
- 初步判断：PSI 的价值不在于替代 Pi，而在于把 Pi 的薄 harness 思想推进到更长期、更通用、更可恢复的执行场景。
- 公平结论：PSI 有必要性，但不是“通用 Agent 平台”的必要性，而是“本地、可嵌入、可恢复、可审计、具备底线安全的 agent loop 内核”的必要性。
- 成功约束：必须极窄切入，避免 UI/LLM provider/复杂编排/完整工具生态；否则会与 Pi、Codex、LangGraph、Temporal、云厂商 runtime 同时竞争。
- 架构红线：任何业务工具、planner、workflow、memory、UI、dashboard、subagent 都应首先作为插件/适配器，而不是进入内核。
- 技术判断：MVP 应以文件系统 JSONL + snapshot/checkpoint 开始，而非数据库/Temporal；等证明价值后再提供 pluggable storage。
- 产品判断：首个用户不是终端用户，而是 agent/tool builder；首个 demo 应证明“进程死掉、等待人类、跨工具失败后仍能继续”。
- 新增判断：PSI 的脚手架价值不在于替模型做更多决定，而在于把模型已有的规划、反思、修正和工具使用能力放进一个能长期运转的工程环境。

## External Verification

- Anthropic `Building effective agents` 明确建议优先寻找最简单方案，复杂度只在需要时增加；并区分预定义路径的 workflows 与由 LLM 动态决定流程和工具使用的 agents。
- MCP 官方规范说明其用于标准化 LLM 与外部数据/工具集成，工具具备 schema，并强调数据访问、代码执行、用户授权与工具安全。
- MCP 工具规范说明工具可由模型发现和调用，但应用应让用户看到暴露的工具、工具调用，并对操作提供确认。
- LangGraph 官方文档显示 checkpoint/persistence 已支撑 human-in-the-loop、memory、time travel、fault-tolerant execution。
- Temporal 官方将 durable execution 定义为故障后可从中断处继续，强调 workflow state、replay、pause、retry 和 long-running workflows。
- 2026-05-08 当前核验：GitHub 上 Pi 约 46.3k stars、Codex 约 80.8k stars、LangGraph 约 31.5k stars，Agent/runtime 相关赛道竞争确实拥挤。

## Open Questions

- PSI 第一版是 Go 还是 Rust？Go 更利于实现速度和跨平台分发；Rust 更利于系统感和安全叙事，但实现成本更高。
- 是否要兼容 MCP 作为一等 ToolAdapter？倾向是兼容，但 PSI 内部需要自己的安全元数据和执行记录，不把 MCP schema 直接等同于可信能力。
- 是否内建 LLM provider 抽象？倾向是不重做成熟抽象，MVP 只定义 `ModelClient` 接口并提供一个最小 OpenAI-compatible adapter。
