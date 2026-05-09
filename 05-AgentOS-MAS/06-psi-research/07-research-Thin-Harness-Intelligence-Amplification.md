# 模型越强，脚手架越薄：从补偿型 Harness 到智能放大型 Runtime

| 字段 | 内容 |
|---|---|
| 日期 | 2026-05-09 |
| 类型 | 研究报告 |
| 主题 | 模型能力增强后，Agent 脚手架如何从弥补模型不足转向放大模型智能 |
| 关联项目 | Project Psi、pi-book、Claude Code / Anthropic harness 研究 |

## 摘要

过去两年，Agent 工程的主流做法一直在给模型加脚手架：planner、router、multi-agent、workflow、memory、permission gate、prompt chain、reviewer、critic。这些组件的共同前提是：模型不够可靠，所以系统必须替它规划、拆解、检查、路由和约束。

但这个前提正在变化。Anthropic 近期关于 managed agents 和 long-running application development harness 的文章反复指出：harness 的每个组件都编码了一个关于“模型自己做不到什么”的假设；模型升级后，这些假设需要重新验证。一些旧模型时代必要的 harness 逻辑，在新模型上可能变成负担。

这不意味着 harness 会消失。相反，长期任务、真实工具、可恢复执行、安全边界和验证闭环仍然需要系统支持。真正发生变化的是 harness 的职责：

> 旧 harness 用控制逻辑弥补模型不足；新 harness 用环境条件放大模型智能。

对 Psi 而言，这个判断非常关键。Psi 不应该成为一个更完整的 Agent Framework，而应成为一个 intelligence-amplifying runtime：用极薄的控制面、稳定的事件/工具/状态协议、高质量反馈和可恢复执行，把强模型已有的规划、反思、工具使用和自我修正能力放大出来。

## 1. 问题背景：为什么“脚手架变薄”现在变成核心议题

### 1.1 早期 Agent 工程的默认假设

早期 Agent 系统中的 harness 通常建立在几个假设上：

- 模型不能可靠规划，所以需要 planner。
- 模型不能长期保持目标，所以需要 workflow/DAG。
- 模型不会自检，所以需要 reviewer/critic。
- 模型不能正确选择工具，所以需要 router。
- 模型无法管理上下文，所以需要 memory manager。
- 模型不能安全执行动作，所以需要固定审批流程。

这些假设在弱模型时代有工程价值。它们把不稳定的自然语言推理压进确定性流程，换来可预测性。

但它们也制造了一个长期问题：

> harness 越厚，模型越像被调度的函数；系统越“聪明”，模型越没有机会发挥智能。

当模型能力提升后，原先用于补短板的组件不再只是辅助，而可能变成智能上限。

### 1.2 Anthropic 的新判断：Harness 组件会过期

Anthropic 在 2026 年 4 月发布的 `Scaling Managed Agents` 中提出了一个重要视角：harness 会显式或隐式地编码关于模型能力的假设。文章举例说，他们曾为 Sonnet 4.5 加入自动 context reset 机制，避免模型卡住；但 Opus 4.5 更能利用长上下文后，这套机制反而变成需要移除的 dead weight。

这说明 harness 不是越多越好，而是要随模型能力重新校准。

同一篇文章还把 agent 系统虚拟化成几个稳定接口：

- `Session`：append-only log。
- `Harness`：模型调用循环和路由。
- `Sandbox`：隔离执行环境。

这个拆分背后的思想是：不要把某一代模型的短板硬编码进系统，而要把 brain、hands、state、environment 解耦。

### 1.3 Claude Code 创始人观点的含义

Sequoia 的 `Training Data` 播客在 2026 年 5 月 5 日发布了 Boris Cherny 的访谈页面，标题是 `Anthropic's Boris Cherny: Coding's Printing Press Moment`。页面摘要提到几个关键信号：

- Boris Cherny 认为 coding 正处在印刷术级别的转折。
- 他称自己 2026 年几乎不再手写代码。
- 他能从手机上通过 Claude Code 发出大量 PR。
- 他认为 `loops` 是未来。
- 页面摘要还提到一个激进说法：Claude Code 未来可能缩到约 100 行代码。

这里要谨慎：公开页面不是完整 transcript，“100 行代码”更像方向性判断，而不是架构承诺。但它和 Anthropic 官方文章的结论一致：

> 模型越强，harness 中那些为了替模型控制流程而存在的层，会越来越薄。

真正保留下来的，不是当前某个 CLI 产品的具体实现，而是让模型能持续行动的接口：工具、状态、反馈、执行环境、权限边界和验证闭环。

## 2. “薄”不是“少写代码”，而是减少补偿型控制

### 2.1 两种薄

讨论 harness 变薄时，很容易误解成“系统代码越少越好”。这不准确。

更精确的区分是：

| 类型 | 特征 | 结果 |
|---|---|---|
| 补偿型控制 | planner、router、DAG、多角色、固定审批流程、隐藏 memory | 替模型决策，压缩模型自主空间 |
| 放大型环境 | 工具 schema、事件日志、checkpoint、sandbox、verification、context builder | 让模型更好地理解、行动、观察和修正 |

未来应该变薄的是第一类：补偿型控制。  
未来仍然重要，甚至要更扎实的是第二类：放大型环境。

所以核心命题不是：

> harness 会消失。

而是：

> 控制型 harness 变薄，环境型 harness 变强。

### 2.2 为什么“环境型”能力不会消失

即使模型非常强，它仍然面对几个物理限制：

- LLM API 本身是无状态的。
- 工具调用会产生副作用。
- 长任务会跨越上下文窗口、进程生命周期和人类审批周期。
- 真实世界反馈需要被观察、压缩、记录和恢复。
- 安全边界不能只靠模型自觉。

因此，长期 Agent 仍然需要 runtime。区别在于，这个 runtime 不应该替模型思考，而应该提供：

- 清晰任务事实。
- 可理解工具。
- 高信号 observation。
- 可恢复状态。
- 可分支执行。
- 可验证完成标准。
- 明确安全边界。

这就是 intelligence-amplifying scaffold。

## 3. Anthropic/Claude Code 材料中的设计线索

### 3.1 Long-running harness：长任务需要结构化外部记忆

Anthropic 的 `Harness design for long-running application development` 展示了长周期软件任务的 harness 设计：多 agent 可以分工，任务可以被拆解，Claude 可以跨 session 工作，进度需要通过 artifacts 和 GitHub issue 等外部结构持续记录。

这篇文章说明了一点：强模型确实能完成更长任务，但长任务不应只靠“更长上下文”。它需要外部化结构：

- 任务拆分。
- 中间产物。
- 进度文件。
- 交接信息。
- 验证路径。

这些不是替模型推理，而是让模型的推理有稳定承载。

### 3.2 Effective harnesses：失败不是因为模型不会想，而是环境不给反馈

Anthropic 的 `Effective harnesses for long-running agents` 总结了他们构建长任务 harness 时遇到的失败模式：

- 模型试图 one-shot 完成太多事情。
- 上下文交接不清楚。
- 过早宣称完成。
- 缺少端到端验证。

这些失败不是简单靠 planner 能解决的。更有效的是给模型更好的工作环境：

- feature list 明确剩余任务。
- progress file 记录状态。
- git history 记录事实。
- init script 让新 session 恢复现场。
- verification 强制检查完成度。

这与 Psi 的 EventLog/Checkpoint 思路一致：真正重要的是把任务进展变成可恢复的工程事实。

### 3.3 Building effective agents：先简单，再加复杂度

Anthropic 的 `Building effective agents` 明确区分：

- workflow：LLM 和工具沿预定义路径执行。
- agent：LLM 自主决定流程和工具使用。

文章建议从简单、可组合模式开始，只有当复杂度带来可测量改善时才增加复杂度。

这对 Psi 的启发是：不要把 workflow、multi-agent、planner 预装进 core。它们可以作为外部策略存在，但 core 应保持 agent loop 原生。

### 3.4 Tool design：工具是 Agent 的 HCI

Anthropic 的 `Writing effective tools for AI agents` 把工具设计类比为人机交互设计。对 agent 来说，工具就是它和计算机世界交互的界面。

文章强调：

- 少而精的工具通常优于大量工具。
- 工具响应要高信号、低噪声。
- 工具设计要通过 evals 改进。
- 工具输出应控制上下文消耗。

这直接支持一个判断：

> 放大模型智能，第一步不是加 planner，而是设计更好的工具界面。

工具不是插件列表，而是模型的行动语义地图。

### 3.5 Claude Code docs：Agent loop 的核心是反馈驱动

Claude Code 官方文档将其描述为 agentic coding tool，核心循环可以概括为：

```text
gather context -> take action -> verify result -> repeat
```

Claude Code best practices 反复强调验证：测试、lint、build、截图、浏览器检查、期望输出。它还建议给 Claude 明确的验证方式，让模型能知道自己是否成功。

这说明一个强模型不只是需要工具，更需要 verification surface。没有验证，模型容易“看起来完成”；有验证，模型才能把行动结果转化为修正信号。

## 4. 从补偿型脚手架到放大型脚手架

### 4.1 补偿型脚手架的结构

补偿型脚手架通常长这样：

```text
User Goal
  -> Planner
  -> Router
  -> Worker Agent A/B/C
  -> Critic
  -> Memory
  -> Workflow Engine
  -> Finalizer
```

它的问题不是这些组件永远无用，而是它们经常过早进入 core。一旦进入 core，就会变成隐藏假设：

- 任务必须先规划。
- 规划必须由某个 planner 生成。
- 工具选择必须由 router 决定。
- review 必须由 critic 完成。
- memory 必须由框架维护。

模型变强后，这些假设可能不再成立。

### 4.2 放大型脚手架的结构

放大型脚手架更像这样：

```text
TaskSpec
  -> ContextBuilder
  -> Model
  -> ActionIntent
  -> SafetyBoundary
  -> Tool
  -> Observation
  -> EventLog / Checkpoint
  -> Verify / Fork / Continue
```

这里的核心差异是：模型仍然决定下一步做什么，系统只让“下一步”更可理解、更可执行、更可恢复。

### 4.3 七种智能放大机制

#### 1. 放大理解：结构化任务事实

模型不缺读懂一句话的能力，但长期任务需要稳定事实。`TaskSpec` 应提供：

- goal
- constraints
- acceptance criteria
- allowed capabilities
- workspace boundary
- risk level
- unknowns
- success evidence

这不是替模型规划，而是减少任务漂移。

#### 2. 放大行动：工具语义地图

工具描述应包含：

- 适用意图。
- 输入 schema。
- 输出 schema。
- 副作用等级。
- 幂等性。
- dry-run 能力。
- 风险等级。
- 失败后的恢复建议。

这让模型能更准确地选择和调用工具。

#### 3. 放大反馈：高信号 observation

工具返回不应只是原始 stdout 或“失败”。它应明确告诉模型：

- 发生了什么。
- 状态如何变化。
- 为什么失败。
- 有哪些证据。
- 下一步可尝试什么。

对 browser/computer use，observation 还应包括截图引用、页面状态、可见元素、坐标或 DOM 线索。

#### 4. 放大连续性：事件日志作为工作记忆

长期任务不能依赖聊天记录。需要 append-only event log：

- model request/response
- action intent
- safety decision
- tool call
- tool result
- checkpoint
- human approval/denial
- verification result

恢复时，模型看到的是“执行事实”，不是杂乱对话。

#### 5. 放大自我修正：fork/replay

强模型可以从失败中修正，但需要系统支持：

- replay：审计历史，不重复副作用。
- resume：从 checkpoint 继续。
- fork：从某个节点分支，尝试新策略。

fork 是对模型推理能力的放大：它允许模型比较路径，而不是在单一路径上补丁式前进。

#### 6. 放大边界感：安全门变成可理解反馈

SafetyGate 不应只是 `allow/deny`。好的安全门应该返回：

- 触发了哪条规则。
- 风险是什么。
- 需要什么审批。
- 有哪些替代动作。
- 人类拒绝或批准的理由。

这样安全边界成为模型可学习的环境事实，而不是外部黑箱。

#### 7. 放大自我扩展：skills/extensions

当模型反复执行某类任务，系统应允许它沉淀能力：

- skill：流程、经验、领域知识。
- extension：新工具、新 context hook、新 evaluator。
- policy：特定环境的安全规则。

但这些都应在 core 外生长。core 提供稳定接口，不吞掉生态。

## 5. 对 Psi 的具体设计建议

### 5.1 Psi 的定位应升级

现有 Psi 定义是：

> minimal durable runtime for local agent loops.

建议升级为：

> intelligence-amplifying runtime for continuous agents.

不是因为 durable execution 不重要，而是因为 durable execution 只是底座。更高层价值是：让强模型在长任务中保持连续、获得反馈、修正路径，并安全行动。

### 5.2 保持 Core 5，但重新解释职责

| 模块 | 不应做什么 | 应该放大什么 |
|---|---|---|
| TaskSpec | 不做 planner | 放大任务理解和验收清晰度 |
| ExecutionLoop | 不做 workflow/DAG | 放大反馈驱动的持续行动 |
| ToolRegistry | 不堆工具生态 | 放大行动语义和工具可靠性 |
| EventLog/Checkpoint | 不只是审计 | 放大连续性、恢复、分支比较 |
| SafetyGate | 不做业务编排 | 放大边界感和人类反馈 |

### 5.3 新增薄接口：ContextBuilder

Psi 不应内建 memory/RAG/compaction 策略，但需要提供上下文装配接口：

```text
ContextBuilder(
  TaskSpec,
  Checkpoint,
  RecentEvents,
  ToolDescriptors,
  HostContext
) -> ModelContext
```

默认实现可以很薄：

- 当前 TaskSpec。
- 最近 N 条事件。
- 最新 checkpoint。
- 可用工具摘要。
- 当前 pending approval / verification status。

领域策略放到外部：

- coding context builder：文件索引、diff、测试结果。
- browser context builder：截图、页面状态、元素摘要。
- ops context builder：告警、服务状态、变更窗口。

### 5.4 ActionIntent 应显式，但不要变成全局计划

建议让模型每轮输出一个轻量 `ActionIntent`：

```json
{
  "kind": "tool_call | ask_human | verify | fork | complete | pause",
  "goal_step": "本步推进什么",
  "tool": "read",
  "args": {},
  "expected_observation": "期望看到什么",
  "risk_note": "为什么安全或为什么需要审批",
  "fallback": "失败后如何调整"
}
```

这不是 planner。它只让当前动作的意图可记录、可审计、可恢复。

### 5.5 ToolDescriptor 应升级为执行契约

建议 ToolDescriptor 包含：

```json
{
  "name": "bash",
  "description": "Execute shell command",
  "schema": {},
  "side_effect": "none | read | write | network | destructive",
  "risk_level": "low | medium | high",
  "idempotency": "idempotent | retry_safe | non_idempotent",
  "supports_dry_run": false,
  "observation_schema": {},
  "approval_required_when": []
}
```

这能同时服务三件事：

- 模型更懂工具。
- SafetyGate 更懂风险。
- EventLog/Replay 更懂副作用。

### 5.6 Verification 应成为一等事件

Claude Code 的经验说明，验证是最高杠杆之一。Psi 应把 verification 作为事件类型，而不是普通工具输出：

- `verification_requested`
- `verification_passed`
- `verification_failed`
- `verification_skipped`

并且要求模型在 `complete` 前尽量给出 success evidence。

这能减少“看起来完成”的幻觉式结束。

### 5.7 把复杂能力放在外部增长面

Psi 不应内建：

- multi-agent。
- planner。
- workflow。
- long-term memory。
- browser agent。
- coding agent。
- UI/dashboard。
- provider router。

但 Psi 应提供：

- `SkillLoader`
- `ToolAdapter`
- `ContextHook`
- `EventHook`
- `PolicyHook`
- `EvaluatorHook`
- `StorageDriver`

判断标准很简单：

> 如果一个能力可以用 schema、event、hook、skill、extension 表达，就不要进 core。

## 6. 设计这种脚手架的检查表

每添加一个 harness 组件，都问十个问题：

1. 它是在替模型决策，还是改善模型决策条件？
2. 它对模型可见吗？模型能理解它吗？
3. 它减少 hidden state，还是增加 hidden state？
4. 它提升 observation 质量吗？
5. 它让失败更容易恢复吗？
6. 它让任务完成更可验证吗？
7. 它能被新模型能力自然替代吗？
8. 它能作为 hook/extension/skill 存在吗？
9. 它是否把某一代模型的短板硬编码进 core？
10. 模型再强一代后，这个组件是会变薄，还是继续束缚模型？

如果一个组件主要做“替模型想”，应保持外置。  
如果一个组件提供“状态、工具、反馈、边界、验证”，才有资格进入 runtime 基础层。

## 7. 反直觉结论

### 7.1 模型越强，越需要好工具，而不是更多工具

强模型不是万能 shell。工具越多，选择成本越高，上下文越重。更好的方向是少量高语义工具，加清晰 schema 和高信号 observation。

### 7.2 模型越强，越不该内建 planner

Planner 是最容易过期的 harness 组件。弱模型时代 planner 帮助稳定执行；强模型时代 planner 容易限制探索。规划能力应通过 TaskSpec、progress file、fork/replay、verification 来放大，而不是硬编码为 core planner。

### 7.3 模型越强，越需要外部事实

更强推理不等于更强事实记忆。长期任务依然需要事件日志、checkpoint、测试结果、artifact、git history。这些事实不是替代智能，而是智能的燃料。

### 7.4 模型越强，安全边界越要清晰

强模型会更主动地行动，因此边界必须更结构化。安全门不应变成审批平台，但应提供清楚的风险语义、审批记录和替代路径。

## 8. 对 Psi 的最终建议

Psi 的下一步不应是“实现一个完整 Agent Runtime”，而应是做一个可验证的最小研究 demo：

1. **崩溃恢复**：进程中断后，模型能从 checkpoint 和事件摘要中恢复任务。
2. **工具失败自修正**：工具返回结构化 observation 后，模型能自行调整策略。
3. **审批反馈学习**：高风险动作被拒绝后，模型能理解拒绝理由并提出替代路径。
4. **fork 对比**：同一 checkpoint 分叉两条策略，日志能对比结果。
5. **完成验证**：模型在 complete 前必须提供 verification evidence。

如果这五件事成立，Psi 就证明了它的核心价值：

> 不替模型变聪明，而是让模型的聪明变得可持续、可观察、可恢复、可验证。

## 9. 结论

“Harness 越来越薄”不是一句极简主义口号，而是一个架构判断：

> 随着模型变强，系统中用于弥补模型弱点的控制逻辑会不断过期；但用于放大模型智能的环境接口会越来越重要。

因此，未来 Agent runtime 的关键不是堆更多 agent、更多 planner、更多 workflow，而是设计一个模型能理解、能利用、能从中恢复和自我修正的行动环境。

Psi 应该站在这个位置上：

- 不做通用 Agent 平台。
- 不做 Claude Code/Pi 的替代品。
- 不做 workflow engine。
- 不把 planner、memory、multi-agent、UI 放进 core。
- 做一个 thin but durable、model-visible、tool-native、state-backed、feedback-rich 的执行微内核。

这就是从补偿型脚手架到智能放大型脚手架的转变。

## 参考来源

### 外部来源

- Anthropic Engineering, `Scaling Managed Agents`, 2026-04-08  
  https://www.anthropic.com/engineering/scaling-managed-agents
- Anthropic Engineering, `Harness design for long-running application development with Claude`, 2026-03-24  
  https://www.anthropic.com/engineering/harness-design-long-running-apps
- Anthropic Engineering, `Effective harnesses for long-running agents`, 2025-08-11  
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Anthropic Engineering, `Building effective agents`, 2024-12-19  
  https://www.anthropic.com/engineering/building-effective-agents
- Anthropic Engineering, `Writing effective tools for AI agents`, 2025-09-11  
  https://www.anthropic.com/engineering/writing-tools-for-agents
- Claude Code Docs, `Overview`  
  https://docs.claude.com/en/docs/claude-code/overview
- Claude Code Docs, `Common workflows`  
  https://docs.claude.com/en/docs/claude-code/common-workflows
- Claude Code Docs, `Claude Code Best Practices`  
  https://www.anthropic.com/engineering/claude-code-best-practices
- Sequoia Capital Training Data, `Anthropic's Boris Cherny: Coding's Printing Press Moment`, 2026-05-05  
  https://podcasts.apple.com/mx/podcast/anthropics-boris-cherny-codings-printing-press-moment/id1750736528?i=1000766203785&l=en-GB

### 本地来源

- `05-AgentOS-MAS/06-psi-research/psi-architecture-design-and-implementation-plan.md`
- `05-AgentOS-MAS/06-psi-research/06-insight-Psi-Intelligence-Amplifying-Scaffold.md`
- `vendor/pi-book/src/ch08-agent-loop.md`
- `vendor/pi-book/src/ch09-tool-execution.md`
- `vendor/pi-book/src/ch11-session-tree.md`
- `vendor/pi-book/src/ch12-compaction.md`
- `vendor/pi-book/src/ch15-extensions.md`
- `vendor/pi-book/src/ch16-skills.md`
- `vendor/pi-book/src/ch30-minimal-core.md`
- `vendor/pi-book/src/ch31-contrarian-choices.md`
- `vendor/pi-book/src/ch32-boundaries.md`

