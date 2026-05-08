# Psi：从补偿型脚手架到智能放大型脚手架

| 字段 | 内容 |
|---|---|
| 日期 | 2026-05-09 |
| 输入 | 当前 Psi 研究方案、`vendor/pi-book` |
| 主题 | 如何让脚手架从弥补模型不足，转向放大模型本身的智能 |

## 1. 核心判断

当前 Psi 的正确方向不是继续发明一个更完整的 Agent Framework，而是把自己收敛为：

> 一个让强模型更稳定、更可持续、更可审计地行动的最小执行环境。

这意味着 Psi 的脚手架不应该替模型做复杂规划、替模型编排角色、替模型规定流程。它应该做的是让模型面对一个更清晰、更可操作、更可恢复、更有反馈的世界。

一句话：

> 旧脚手架把模型当成能力不足的执行器，所以用流程补它；新脚手架把模型当成正在变强的智能体，所以用环境放大它。

## 2. Pi-book 给 Psi 的关键启发

`pi-book` 反复强调一个设计纪律：核心越薄，模型和上层产品越自由。

对 Psi 最重要的启发有六点：

1. **Loop 应该知道尽可能少的东西**  
   Pi 的 agent loop 只做模型调用、工具执行、消息注入和事件发射。会话、压缩、权限、UI、重试都在外层。Psi 的 `ExecutionLoop` 也不应变成 planner 或 workflow engine。

2. **协议比框架更重要**  
   Pi 的核心价值不是内建功能，而是事件流、回调、工具 schema、消息格式这些协议面。Psi 也应该优先定义稳定协议，而不是堆 feature。

3. **工具是模型的行动界面，不只是插件调用**  
   Pi 的工具执行是 `prepare -> execute -> finalize`：参数验证、执行前拦截、执行后处理、流式观察。Psi 的 `ToolRegistry` 应继承这个思想，并增加风险、幂等、副作用、恢复语义。

4. **状态不是聊天记录，而是可分支、可回放的执行事实**  
   Pi 的 session tree、JSONL、parentId、compaction entry 说明：长期 Agent 需要的不只是历史，而是可导航的执行轨迹。Psi 的 `EventLog/Checkpoint/Fork` 正是这一点的 general runtime 版本。

5. **上下文管理应该是可替换策略，不是 core 行为**  
   Pi 把 compaction 放在产品层，通过 `transformContext` 接入。Psi 也不应内建某一种 memory/summary/RAG 策略，而应提供 Context Builder/Hook 接口。

6. **能力应该外置成 extension surface 和 skill surface**  
   Pi 的 extension 让产品长出新器官，skill 用文档替代代码。Psi 的 subagent、memory、workflow、UI、browser automation、domain policy 都应先作为外置能力出现。

## 3. “补偿型脚手架”的问题

早期 Agent Framework 的脚手架大多是补偿型的。它们隐含假设是：

> 模型不会规划、不会自检、不会正确调用工具、不会保持目标，所以系统必须替它拆任务、定流程、分角色、做路由。

于是系统会引入：

- 固定 planner/executor/reviewer 角色。
- DAG/workflow 编排。
- 复杂 multi-agent 拓扑。
- 内建 memory、router、policy、retriever。
- 大量隐藏状态和隐式流程。
- 一次性注入大量工具和说明。

这些设计在弱模型时代有必要，但在强模型时代会逐渐变成负资产：

- 模型已经能自主规划，但流程把它锁死。
- 模型能根据上下文选择工具，但框架提前路由。
- 模型能从反馈中修正，但系统只给低质量 observation。
- 模型能理解简单 runtime，但复杂抽象让它无法自我调试。
- 模型变强后，脚手架没有变薄，反而成为智能上限。

补偿型脚手架的典型坏味道是：

> 系统越聪明，模型越笨；系统越厚，模型越像被调度的函数。

## 4. 智能放大型脚手架的定义

智能放大型脚手架不是替模型思考，而是改善模型思考和行动的条件。

它放大的不是模型参数本身，而是模型每一轮推理可接触到的：

- 目标清晰度。
- 状态真实性。
- 工具可理解性。
- 反馈密度。
- 记忆连续性。
- 分支比较能力。
- 风险边界。
- 自我扩展空间。

可以定义为：

> 一种 model-visible、tool-native、state-backed、feedback-rich 的执行环境，使模型能更好地理解任务、选择行动、观察结果、修正路径并持续推进。

关键不是“多加一层智能”，而是让已有智能获得更高质量的输入、动作和反馈。

## 5. 如何放大模型本身的智能

### 5.1 放大理解：把任务变成模型可操作的事实

强模型不缺自然语言理解，但缺稳定的任务边界。Psi 的 `TaskSpec` 应成为模型的任务操作台，而不是普通 prompt。

`TaskSpec` 至少应包含：

- `goal`：最终目标。
- `acceptance_criteria`：验收标准。
- `constraints`：硬约束。
- `capabilities`：允许使用的能力。
- `workspace_boundary`：可触达资源。
- `risk_level`：默认风险等级。
- `unknowns`：当前未知点。
- `success_evidence`：什么证据说明任务完成。

放大点在于：模型每一轮都能回到同一个结构化任务事实，而不是依赖长对话里的模糊记忆。

### 5.2 放大行动：给模型更少但更清晰的工具

工具越多不等于能力越强。真正的放大来自高质量 tool affordance。

Psi 的工具描述不应只有 name/schema，还应包含：

- 这个工具适合什么意图。
- 输入参数的强 schema。
- 输出 observation 的结构。
- 是否有副作用。
- 是否幂等。
- 是否可 dry-run。
- 风险等级。
- 失败后模型应如何恢复。

也就是说，`ToolRegistry` 不只是工具列表，而是模型的行动语义地图。

### 5.3 放大反馈：让 observation 成为高信号学习材料

模型能从反馈中变聪明，但前提是反馈足够清楚。

Psi 的工具结果应分成两层：

- `model_observation`：给模型看的高信号摘要，包含事实、状态变化、错误原因、下一步提示。
- `ui_details` / `artifact_ref`：给人或系统看的完整输出、日志、截图、文件引用。

例如 browser/computer use 不应只返回“点击失败”，而应返回：

- 当前页面状态。
- 目标元素是否存在。
- 失败动作。
- 可替代动作。
- 截图引用。
- DOM/坐标/可见性线索。

反馈越结构化，模型越能自我修正。

### 5.4 放大记忆：把执行轨迹变成可恢复的工作记忆

单纯长上下文不是可靠记忆。可靠记忆来自事件事实。

Psi 的 `EventLog` 应记录：

- 模型看到的上下文摘要。
- 模型声明的动作意图。
- 工具调用参数。
- safety 决策。
- observation。
- checkpoint。
- 人类审批与拒绝原因。
- 分支来源。

这样模型恢复时看到的不是“聊天历史”，而是“我在什么状态下做过什么，结果如何，现在还差什么”。

这会显著放大模型的连续任务能力。

### 5.5 放大自我修正：让 replay/fork 成为推理工具

强模型可以比较方案，但需要系统支持分支。

Psi 的 `Fork` 不只是工程调试能力，也是一种智能放大机制：

- 从失败 checkpoint 分叉，让模型换策略。
- 从人类拒绝点分叉，让模型解释并修正。
- 从关键决策点分叉，比较两条路径。
- 把失败路径摘要注入新分支，避免重复犯错。

这比内建一个固定 reviewer agent 更薄，也更符合模型优先。

### 5.6 放大边界感：安全门应该让世界更清晰，而不是替模型决策

`SafetyGate` 的目标不是让模型“更不自由”，而是让模型知道行动边界。

好的安全门应：

- 在执行前暴露风险原因。
- 拒绝时返回明确、可行动的解释。
- 审批后记录人类意图。
- 允许模型提出替代动作。
- 不把业务流程写死进安全策略。

安全边界越清楚，模型越能在边界内自主规划。

### 5.7 放大自我扩展：把新能力做成 skill/extension，而不是 core feature

如果模型发现自己反复执行某类任务，理想脚手架应允许它沉淀能力：

- 写一个 skill，总结流程和注意事项。
- 写一个 extension，封装重复工具链。
- 写一个 context packer，优化某类任务的上下文。
- 写一个 evaluator，判断某类任务是否完成。

但这些都应走审批和版本化，不应让 core 自动变厚。

这就是从“系统提供能力”转向“系统提供生长能力”。

## 6. 对 Psi 架构的具体修订建议

### 6.1 保持 Core 5，但重新解释它们

现有 Core 5 是对的，但每个模块应承担“智能放大”的职责：

| 模块 | 原职责 | 智能放大后的职责 |
|---|---|---|
| TaskSpec | 任务入口 | 把目标、约束、验收、未知点变成模型可操作事实 |
| ExecutionLoop | 持续循环 | 保持模型自主决策，同时提供稳定的 observe-act-feedback 节奏 |
| ToolRegistry | 工具注册/路由 | 提供行动语义地图：schema、风险、副作用、幂等、observation 规范 |
| EventLog/Checkpoint | 恢复与审计 | 把执行轨迹变成可回放、可分支、可压缩的工作记忆 |
| SafetyGate | 底线拦截 | 给模型清晰边界、审批反馈和替代行动空间 |

### 6.2 增加一个薄接口：Context Builder

不要把 memory 做进 core，但需要一个模型上下文装配接口。

建议把它定义为接口，而不是模块：

```text
ContextBuilder(
  TaskSpec,
  Checkpoint,
  RecentEvents,
  ToolDescriptors,
  HostContext
) -> ModelContext
```

它的作用是把状态、事件、工具、约束装配成模型可理解的上下文。

Core 只定义输入输出契约，具体策略外置：

- 默认策略：最近事件 + checkpoint + task spec。
- coding 策略：加入文件操作索引、测试状态、diff 摘要。
- browser 策略：加入页面状态、截图引用、可见元素。
- ops 策略：加入服务状态、告警、变更窗口。

这继承了 Pi 的 `transformContext` 思想。

### 6.3 ActionIntent 不要变成 planner

Psi 可以要求模型输出结构化 `ActionIntent`，但不要要求它先生成完整计划。

建议结构：

```json
{
  "kind": "tool_call | ask_human | complete | pause | fork",
  "goal_step": "本步想推进什么",
  "tool": "read",
  "args": {},
  "expected_observation": "期望看到什么",
  "risk_note": "为什么这一步安全或需要审批",
  "fallback": "失败后下一步怎么处理"
}
```

这不是 planner，而是让模型把当前行动意图显式化，方便恢复、审计和自我修正。

### 6.4 ToolDescriptor 应包含执行语义

建议 `ToolDescriptor` 至少扩展以下字段：

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

这会让模型更理解工具，也让 SafetyGate 和 replay/resume 有基础语义。

### 6.5 EventLog 应记录“为什么”，但不强迫模型暴露完整思维链

Psi 不需要保存完整 hidden reasoning。它需要保存的是可审计的行动理由：

- 本步目标。
- 选择该工具的原因摘要。
- 预期观察。
- 风险判断。
- 失败后的修正路径。

这足以支持调试、恢复、分支和人类 review。

### 6.6 Skill 与 Extension 应成为 Psi 的增长面

Psi 不应内建：

- planner。
- memory。
- browser agent。
- code agent。
- multi-agent。
- dashboard。
- domain workflows。

但 Psi 应提供足够稳定的外置入口：

- `SkillLoader`：按需加载流程性知识。
- `ToolAdapter`：接 MCP、HTTP、shell、本地函数。
- `ContextHook`：自定义上下文装配。
- `EventHook`：订阅执行轨迹。
- `PolicyHook`：扩展安全策略。
- `EvaluatorHook`：判断验收标准是否满足。

这就是“可生长”，而不是“预装很多功能”。

## 7. 判断一个设计是否放大智能的检查表

每加一个功能，都问八个问题：

1. 这个功能是让模型更好地理解/行动/反馈/恢复，还是替模型决策？
2. 它是否对模型可见？模型能否理解它的存在和作用？
3. 它是否能用 schema、event、hook、skill 或 extension 表达，而不是进入 core？
4. 它是否减少 hidden state？
5. 它是否提升 observation 质量？
6. 它是否让失败更可恢复？
7. 它是否让人类反馈变成可用状态？
8. 模型变强后，这个功能会自然变薄，还是会继续束缚模型？

如果答案偏向“替模型做决定”“隐藏在框架内部”“模型无法理解”，就不是智能放大，而是补偿型复杂度。

## 8. Psi 的下一步路线

建议把 Psi 的下一阶段目标从“实现完整 runtime”改成：

> 证明一个薄 runtime 如何让强模型在长任务中更聪明。

最小 demo 应证明四件事：

1. **崩溃恢复**：任务中途进程死亡，恢复后模型知道自己做过什么、现在差什么。
2. **高信号反馈**：工具失败后，模型能基于结构化 observation 自行修正。
3. **审批分支**：高风险动作被拒绝后，模型能理解拒绝原因并提出替代路径。
4. **fork 对比**：同一 checkpoint 分叉两条策略，事件日志能对比结果。

如果这四件事成立，Psi 的价值就不是“又一个 agent runtime”，而是：

> 把模型已有的规划、反思、修正和工具使用能力，放进一个能长期运转的工程环境里。

## 9. 最终结论

Psi 应坚持当前微内核方向，但需要把叙事从“durable execution runtime”进一步提升为：

> Intelligence-amplifying runtime for continuous agents.

它的核心不是给弱模型补腿，而是给强模型铺设：

- 清晰目标。
- 可靠状态。
- 可理解工具。
- 高信号反馈。
- 可恢复轨迹。
- 可分支探索。
- 明确边界。
- 可外置生长面。

这样的脚手架会随着模型变强而变薄，因为它不把智能写死在框架里，而是把智能需要的环境条件做扎实。

