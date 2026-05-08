# Project Psi：极简智能体微内核（Microkernel）架构研究与演进策略

> **文档版本**：v1.0  
> **文档类型**：架构与战略研究报告  
> **核心命题**：在复杂编排框架与底层 API 的夹缝中，论证并设计一个基于“持久化执行（Durable Execution）”和“微内核（Microkernel）”理念的极简 Agent 运行时。

---

## 摘要 (Executive Summary)

随着大语言模型（LLM）推理能力的指数级提升，2026年的智能体（Agent）工程生态正经历一次范式转移。Anthropic 在其架构指南中明确指出：“随着模型变得越来越聪明，框架必须变得越来越薄”[1]。过度复杂的工作流编排逐渐成为阻碍模型原生能力的“抽象债务”。

本报告正式提出 **Project Psi** 的架构战略。Psi 并非一个开箱即用的终端应用（如 Coding Agent），也不是一个全能的编排平台，而是一个**智能体微内核（Agent Microkernel）**。它致力于解决当前生态中的核心痛点：将底层大模型的无状态、单轮 API 调用，转化为具备“抗中断恢复（Durable）”、“边界安全（Safety Gate）”与“通用工具插拔（MCP 协议）”能力的持久化执行循环。

---

## 一、 行业背景与架构断层分析

### 1.1 “框架疲劳”与编排逻辑的退化
在早期的 Agent 开发中，由于模型推理能力较弱，开发者被迫使用如 LangChain、AutoGen 等重型框架，通过多角色（Multi-agent）、固定提示词链与有向无环图（DAG）来进行死板的流程控制[2]。然而，随着具备深度反思能力（如 OpenAI o-series、Claude 3.5+）的模型的普及，业界普遍出现了“框架疲劳（Framework Fatigue）”现象。资深工程师倾向于回归原生 SDK，用最简的 `While` 循环让模型自主决定执行路径，而不是被框架的硬编码逻辑所束缚[3]。

### 1.2 持久化执行（Durable Execution）的刚需
原生 LLM API 的致命弱点在于**无状态（Stateless）**。当 Agent 执行长周期任务（如持续数小时的代码重构或网页抓取）时，网络超时、API 限流或人为暂停（HITL，人类在环审批）都会导致进程崩溃和上下文彻底丢失[4]。虽然 Temporal 等企业级工作流引擎可以解决此类问题，但其对普通开发者而言过于沉重。行业急需一种轻量级的、原生服务于 Agent 循环的持久化状态机[5]。

### 1.3 协议标准化：Brain 与 Hands 的解耦
Model Context Protocol (MCP) 的广泛采用标志着智能体能力的彻底解耦[6]。系统设计不再需要将文件系统、浏览器或数据库 API 硬编码在框架内部。标准的微内核应当只关注“控制平面（Control Plane）”，而将所有具体的动作执行下放给外部的 MCP Servers。

---

## 二、 Psi 微内核架构设计 (Microkernel Architecture)

基于上述行业共识，Psi 的核心设计哲学被定义为：**Loop-first（循环优先）、Plugin-everything（一切皆插件）、State-is-Truth（状态即真理）**。

其整体架构由且仅由五个高度解耦的模块组成（The Core 5）：

### 2.1 TaskSpec（任务规约）
抛弃模糊的系统提示词，使用强类型的结构化数据定义目标。
* **职责**：定义任务的最终目标（Goal）、边界约束（Constraints）、所需的外部能力集合（Required Capabilities）以及风险定级（Risk Level）。

### 2.2 ToolRegistry（工具注册表）
内核不实现任何业务工具，而是作为一个协议路由器。
* **职责**：全面拥抱 **MCP (Model Context Protocol)**[6]。将外部注入的 MCP Servers（如 GitHub API、本地终端、数据库读写）统一解析为大模型可理解的 JSON Schema，并负责路由调用请求。

### 2.3 StateStore & Event Log（状态机与事件日志）
Psi 区别于简单循环的灵魂模块，引入“事件溯源（Event Sourcing）”模式[4]。
* **职责**：采用 Append-only（仅追加）的方式记录所有状态变更，包括大模型决策记录、工具执行结果和上下文快照。这确保了任务的每一步都是可追溯、可审计的。

### 2.4 Minimal Safety Gate（极简安全门）
应对 Agent 越权操作和提示词注入（Prompt Injection）的最后防线。
* **职责**：独立于模型推理的拦截层。基于 `TaskSpec` 的风险评级，对高危工具调用（如 `rm -rf`、执行未经审核的 SQL）进行拦截，并触发挂起（Suspend），等待人类审查（Human-in-the-loop）[1]。

### 2.5 ExecutionLoop（执行引擎）
微内核的心脏。
* **职责**：一个极度健壮的循环引擎。流程为：`读取 State` -> `向模型发起推理请求` -> `过 Safety Gate` -> `路由执行 Tool` -> `记录 Event Log` -> `更新 State` -> `进入下一循环`。

---

## 三、 关键方案设计与实现路径

为了确保微内核的灵活性与健壮性，Psi 在技术实现上需要遵循以下策略：

### 3.1 轻量级重水化（Rehydration）机制
为了实现持久化执行，Psi 将放弃依赖外部数据库，转而采用类似文件系统快照的设计：
* 每次循环结束，状态引擎生成一个包含当前变量和上下文差异（Delta）的 `JSONL` 记录。
* 当系统因断网或人类审批被挂起时，Psi 的进程可以被安全终止（释放内存）。
* 恢复执行时，内核通过读取指定的 `session_id` 日志文件，能在毫秒级进行**重水化（Rehydrate）**，无缝接续前置状态继续向 LLM 发起请求。

### 3.2 零业务逻辑污染（Zero Business Logic）
在代码库管理上，内核（`psi-core`）必须做到零外部业务依赖。例如，处理浏览器 DOM 树或编译代码的逻辑，绝对不允许进入内核代码。内核的职责边界极其清晰：只处理调度、网络容错、日志落盘和安全拦截。

### 3.3 语言与运行时选择
为保证底层中间件的高性能与泛用性：
* **首选（Go 或 Rust）**：具备无 GC 延迟或极低并发开销特性，可编译为单文件二进制，非常适合作为跨平台的底层引擎嵌入到不同的系统应用中。
* **次选（TypeScript）**：若为了快速验证并复用现有的 MCP 生态，可采用纯 TypeScript 构建。但需严格遵循 `0 dependencies`（除跨平台标准库外）的原则，确保极简的开发者体验（DX）。

---

## 四、 战略定位与行动建议

将 Psi 打造为成功的开源基础设施，需要明确的营销与推广路线：

### 4.1 定位差异化：“反框架”的中间件
Psi 的目标用户不是想要一键生成代码的最终用户，而是**需要构建可靠 Agent 系统的开发者**。它的竞品不是 Pi 或 Cline 等终端产品，而是 LangChain 或复杂的自研编排代码。
* **宣传核心**：提供“抗宕机的持久化循环”与“绝对的安全底线”，将复杂性降低 90%。

### 4.2 杀手级特性展示（Killer Demos）
通过提供三个极简的场景 Demo，证明其作为“内核”的 Anywhere 属性：
1. **Durable Backend Agent**：在后端服务中，展示一个因等待外部 API 回调而被挂起 3 天，随后随着 Webhook 触发而瞬间无损恢复的对账 Agent。
2. **Safe Coding Agent**：结合本地 Filesystem MCP，展示由于触发修改核心配置文件的规则，Agent 自动挂起并向终端推送审批请求，确认后继续执行。
3. **Browser Automation**：演示在遇到复杂的验证码弹窗时，Agent 如何优雅地处理错误日志并进行有限度的重试循环，而非导致整个系统崩溃。

### 4.3 结论
Agent 工程生态正在从“拼装全家桶”向“高度定制化的解耦基建”回归。Project Psi 通过拥抱微内核（Microkernel）与持久化（Durable Execution）的设计理念，不仅准确踩中了“框架变薄”的业界演进趋势，更为开发者构建稳定、安全的下一代自主智能体提供了一个坚实而纯粹的技术底座。

---

## 参考文献

* [1] Anthropic. (2025). *Building Effective Agents*. Anthropic Research. 明确提出了“框架应随模型能力增强而变薄”的设计哲学。
* [2] 开发者社区观察. (2026). *The Rise of Framework Fatigue*. 行业讨论表明，过度复杂的 DAG 和多角色编排正被原生循环取代。
* [3] OpenAI. (2025). *Introducing the Agents SDK*. 强调了基于原生代码控制流程与模型解耦的必要性。
* [4] Temporal Technologies. (2025). *Durable Execution in the Age of AI*. 详细论述了事件溯源（Event Sourcing）在长周期 Agent 任务容错中的关键作用。
* [5] LangChain. (2026). *LangGraph Checkpointing Architecture*. 证明了在有状态工作流中，中断与可恢复机制的普遍需求。
* [6] Anthropic & 社区. (2025). *Model Context Protocol (MCP) Specification*. 定义了 LLM 与外部数据及工具环境交互的标准化接口。
