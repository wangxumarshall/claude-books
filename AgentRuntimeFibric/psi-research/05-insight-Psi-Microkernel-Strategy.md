# Project Psi：微内核战略下的架构重塑与演进指南

> **文档目的**：在 `04-feasibility-Psi-Project-Assessment.md` 的悲观评估（将 Psi 视为应用层产品）基础上，进行视角转换。本文档将 Psi 严格定位为 **Agent 时代的极简基础设施（Microkernel）**，并提供完整的论述、架构设计、方案设计与落地方向。

---

## 一、战略论述：从“造车”到“造发动机”

在 04 号报告中，我们将 Psi 与 Pi、OpenCode、Aider 等项目放在同一赛道进行对比，得出了“红海竞争、爆火概率低”的结论。这个评估是客观的，但前提是**假设 Psi 是一个直接面向终端用户的应用**。

然而，基于 `00-insight-why-project-Psi.md` 和 `01-insight-what-is-project-Psi.md` 的核心定义，Psi 的真正形态应该是：**一个极简的任务执行内核（Minimal Agent Runtime）**。

### 1.1 行业目前的真空地带

现在的开发者在构建 Agent 时，面临两难的“断层”：
- **底层太简陋**：OpenAI/Anthropic 的原生 API 只提供“无状态的单轮 `tool_call`”，没有持久化，没有循环机制，宕机即丢失上下文。
- **上层太笨重**：LangChain、CrewAI、AutoGen 强加了“多角色、DAG 路由、复杂反思链”等重度编排逻辑。在“模型越来越聪明”的今天，这些重型框架往往限制了模型的原生推理能力。

### 1.2 Psi 的生态位：Agent 界的 Zustand / Express.js

天下苦重型框架久矣。开发者迫切需要一个干净、纯粹、抗中断（Durable）的 Loop 引擎。
Psi 的定位必须是**底层中间件（Library / SDK）**。
它不带任何 UI，不预设任何场景（如写代码、查网页）。它只负责一件事：**将大模型的单轮对话，转化为安全、可中断、可恢复的持久化执行（Durable Execution）。**

---

## 二、架构设计：微内核（Microkernel）架构

为了实现“模型变强，系统变薄”的终极理念，Psi 必须采用极端解耦的**微内核架构**。内核只保留维系任务存活的最少状态，其他一切皆为插件。

### 2.1 核心理念
- **Loop-first**：系统的主动脉是循环（观察-思考-调用-更新），而不是流程图。
- **Plugin-everything**：工具、安全规则、UI 交互，全部以插件或回调形式接入。
- **State-is-Truth**：内存中的对象随时可以被销毁，真正的状态是落盘的增量日志（Event Log）。

### 2.2 核心五模块（The Core 5）

1. **TaskSpec（任务规约）**：
   - 系统的唯一输入入口。结构化定义目标、约束、验收标准。
   - 拒绝大段的模糊 prompt，要求显式声明所需的 `Capabilities` 和 `Risk Level`。

2. **StateStore & Log（状态与轨迹存储）**：
   - 这是 Psi 区别于简单 While 循环的灵魂。
   - **Event Log**：Append-only 的执行轨迹，记录所有的 Tool Call、Observation 和 State Delta。
   - **Checkpoint**：提供微秒级的状态快照，支持任务的 Suspend（挂起）和 Resume（恢复）。

3. **ToolRegistry（工具注册表）**：
   - 统一的能力边界定义。
   - 拥抱 **MCP (Model Context Protocol)** 协议，Psi 内核本身不写任何具体的工具逻辑，只做协议的解析与调用转发。

4. **Minimal Safety Gate（极简安全门）**：
   - 独立于业务逻辑的拦截层。
   - 不做复杂的多级审批，只做“底线拦截”（如：禁止脱离特定目录的写操作、阻断未授权的出站网络请求、高危动作要求 HITL 人类在环确认）。

5. **ExecutionLoop（执行引擎）**：
   - 驱动上述 4 个模块的齿轮。
   - 负责：加载状态 -> 触发模型推理 -> 过安全门 -> 执行工具 -> 记录日志 -> 写入快照 -> 进入下一循环。

---

## 三、方案设计：技术选型与实现细节

### 3.1 语言与技术栈选型

既然定位是微内核，那么应该追求极致的轻量、无依赖、高性能。
- **推荐方案 A（Go 语言）**：编译为单一二进制文件，无依赖，极低的并发开销，非常适合做底层 Runtime 和系统级工具。
- **推荐方案 B（TypeScript / Node.js）**：目前 AI 轮子最多、受众最广的语言。如果选 TS，核心库必须做到 `0 dependencies`（除了跨平台必要的少量底层库），提供极佳的类型提示（DX）。

### 3.2 持久化执行（Durable Execution）的设计

实现“抗中断”无需引入 Temporal 这样沉重的外壳。Psi 可以采用基于文件系统的轻量级 Checkpoint 树：
- 每次 ExecutionLoop 结束时，计算当前状态的 Delta（包含模型上下文的摘要、变量状态），追加写入 JSONL 格式的 Session 日志中。
- 当进程被意外 Kill，下次启动时只需指定 `session_id`，Psi 即可从最后一行合法的 Checkpoint 瞬间重水化（Rehydrate）恢复执行。

### 3.3 拥抱 MCP（Model Context Protocol）

不要自己发明工具规范。
- `ToolRegistry` 应直接实现为 MCP Client。
- 让开发者通过 MCP 提供 `computer_use`、`filesystem_edit` 或 `github_api`。
- Psi 就能将所有的精力集中在如何让 Loop 跑得更稳、更安全。

### 3.4 代码接口示例（DX 体验设计）

开发者使用 Psi 的体验应该是极其“爽快”的：

```typescript
import { PsiKernel, MemoryStore, McpToolRegistry, SafetyGate } from '@psi/core';

// 1. 初始化底座
const registry = new McpToolRegistry();
await registry.connectServer('sqlite-mcp-server');

// 2. 配置安全门
const safety = new SafetyGate({
  rules: [{ action: 'DROP TABLE', decision: 'require_human_approval' }]
});

// 3. 实例化内核
const kernel = new PsiKernel({
  store: new MemoryStore(),
  tools: registry,
  safety: safety,
});

// 4. 提交任务，持久化执行
const execution = await kernel.submit({
  title: "清理无效日志并生成报表",
  goal: "查询 log 表，删除30天前的数据，生成 summary.md",
  riskLevel: "medium"
});

// 监听事件以驱动宿主的 UI
execution.on('tool_call', (e) => console.log(e));
execution.on('suspended', (e) => promptUser(e.reason));

await execution.start();
```

---

## 四、行动建议：如何让 Psi 取得成功？

如果将 Psi 定位为上述的微内核，其 GitHub 爆火（>5k stars）或取得行业影响力的概率将大幅上升。为了实现这一目标，建议采取以下行动：

### 4.1 核心原则：保持克制
**千万不要在内核代码里写业务逻辑！**
坚决抵制在核心库中内置诸如 `BashTool`、`WebBrowser` 或 `CodeEditor` 的冲动。内核只管调度、存储和安全。将具体能力留给 MCP 和外部插件。

### 4.2 打造杀手级 Demo（展示内核的 Anywhere 属性）

发布时，用 3 个极简 Demo 证明 Psi 作为“基础设施”的通用性：
1. **Terminal Coding Agent**：用 100 行代码 + Psi + Filesystem MCP，复刻一个极简版 Pi。
2. **Durable Backend Agent**：用 Psi 嵌入 Express/Gin 路由，展示一个因为网络断开而挂起，3天后随着回调接口触发而瞬间无损恢复的“财务对账 Agent”。
3. **Browser Automation**：结合 Playwright，展示系统自动应对弹窗、报错重试，并在高危操作前暂停等待人类终端指令。

### 4.3 营销定位：反叛者的口号
在 README 的开头，打出极具煽动性且切中当前开发者痛点的口号：

> **"As the model gets smarter, the framework must get thinner."**
> 
> 厌倦了 LangChain 和 AutoGen 的沉重黑盒？
> Psi 是一个不到 2000 行代码、零外部依赖的 Agent 执行微内核。
> 它不教模型怎么思考，它只为大模型提供抗宕机的持久化循环（Durable Loop）、可插拔的工具边界（MCP）和绝对坚固的安全底线（Safety Gate）。

### 4.4 个人产出与 ROI
即便最终未能成为顶级开源项目，这套**从 0 到 1 构建微内核**、**深度解耦状态机**、**融合 MCP 协议**的工程经验，将是你无可替代的技术资产。它可以直接沉淀为你的 Multica 产品底层的核心引擎（AgentOS 的基石）。

---
**结论**：
转换视角后，Psi 不再是一个去红海厮杀的应用，而是一台轻巧、强劲、普适的发动机。这是一条技术品味更高、更有长远价值的造轮子之路。
