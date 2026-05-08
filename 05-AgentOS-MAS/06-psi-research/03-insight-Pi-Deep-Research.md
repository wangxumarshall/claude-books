# Pi 开源项目深度研究报告

> 基于官方文档（pi.dev）、GitHub 仓库（earendil-works/pi）、创始人博客（mariozechner.at）等一手信息源

---

## 一、项目概览

| 维度 | 内容 |
|------|------|
| 项目名称 | Pi（pi.dev） |
| 定位 | 极简终端编码代理工具（Minimal Terminal Coding Harness） |
| 创始人 | Mario Zechner |
| 组织 | Earendil Inc.（earendil-works） |
| 开源协议 | MIT |
| 语言 | TypeScript（96.2%） |
| GitHub Stars | 46.3k |
| 版本 | v0.74.0（截至 2026-05-07，214 个 release） |
| 核心理念 | "Adapt Pi to your workflows, not the other way around." |
| Slogan | "There are many agent harnesses, but this one is yours." |

---

## 二、设计理念（Philosophy）

### 2.1 激进极简主义（Radical Minimalism）

Pi 的核心哲学来自创始人 Mario Zechner 一句话：

> "If I don't need it, it won't be built."

这种极简主义体现在：

- **极简系统提示**：整个 system prompt 不到 1000 tokens，仅描述 4 个工具和基本行为准则
- **极简工具集**：仅 `read`、`write`、`edit`、`bash` 四个核心工具
- **极简架构**：核心本质就是一个 `while` 循环
- **极简依赖**：不依赖 Vercel AI SDK 等第三方统一 API，直接对接四大底层协议

### 2.2 模型优先（Model-First）

Pi 的设计基于一个核心判断：

> 随着模型能力增强，大部分 harness complexity 都会变成负资产。

因此 Pi 极度反对：
- 复杂 Planner / DAG workflow
- 固定 agent role
- 巨型 tool abstraction
- 大量 orchestration
- 过度安全审批链

### 2.3 可扩展性优先于功能（Extensibility over Features）

Pi 明确**不内建**以下功能，而是提供 extension surface 让用户自行构建：

| 不内建的功能 | Pi 的替代方案 |
|---|---|
| Sub-agents | 通过 tmux 或 extension 自行实现 |
| Plan mode | 写 PLAN.md 文件，或用 extension 实现 |
| MCP 支持 | CLI 工具 + README（Skills），或用 extension 添加 |
| Permission popups | 容器化运行，或用 extension 实现确认流 |
| Built-in to-dos | 使用 TODO.md 文件 |
| Background bash | 使用 tmux |

### 2.4 YOLO 安全哲学

Pi 默认完全开放（无权限弹窗、无命令预检查、无文件保护）。理由：

> 当 agent 可以写代码并执行代码时，安全限制本质是安全剧场（security theater）。唯一真正有效的安全措施是切断网络访问或在容器中运行。

---

## 三、架构设计（Architecture）

### 3.1 Monorepo 分层架构

Pi 采用 TypeScript monorepo，严格单向依赖图：

```
Foundation → Core → Applications

packages/
├── ai/              # @earendil-works/pi-ai         — 统一 LLM API 层
├── agent/           # @earendil-works/pi-agent-core  — Agent 运行时核心
├── tui/             # @earendil-works/pi-tui         — 终端 UI 框架
├── web-ui/          # @earendil-works/pi-web-ui      — Web UI 组件库
└── coding-agent/    # @earendil-works/pi-coding-agent — CLI 编码代理
```

### 3.2 pi-ai：统一 LLM API 层

**核心职责**：将 4 大 LLM 协议统一为一个抽象。

| 协议 | 提供者 |
|------|--------|
| OpenAI Completions API | OpenAI、xAI、Groq、Cerebras、Mistral、Ollama、vLLM、LM Studio 等 |
| OpenAI Responses API | OpenAI |
| Anthropic Messages API | Anthropic |
| Google Generative AI API | Google |

**关键设计决策**：

1. **跨提供者上下文交接（Context Handoff）**：支持会话中途切换模型/提供者，自动转换 thinking traces 等格式
2. **类型安全的模型注册表**：从 OpenRouter 和 models.dev 自动生成 `models.generated.ts`，包含 token 成本和能力矩阵
3. **全链路中止支持（Abort Support）**：基于 `AbortController`，支持管道中任意点中止，并返回部分结果
4. **分离的工具结果**：工具返回分为 LLM 内容和 UI 展示内容两部分
5. **流式部分 JSON 解析**：工具调用参数流式传入时，渐进式解析以实现实时 UI

```typescript
// 跨提供者切换示例
const claude = getModel('anthropic', 'claude-sonnet-4-5');
const gpt = getModel('openai', 'gpt-5.1-codex');
const gemini = getModel('google', 'gemini-2.5-flash');

// 序列化上下文 → 反序列化 → 继续用任意模型
const serialized = JSON.stringify(context);
const restored: Context = JSON.parse(serialized);
```

### 3.3 pi-agent-core：Agent 运行时

核心循环极为简洁：

```
用户消息 → LLM 决策 → 工具调用 → 结果观测 → 状态更新 → 继续/停止
```

**Agent 类提供**：
- 状态管理（AgentState）
- 事件流订阅
- 消息队列（steer / followUp 两种模式）
- 附件处理（图片、文档）
- 传输抽象（直接运行 / 代理模式）

**核心特点**：
- 没有 max_steps 或类似限制——循环直到 agent 认为完成
- 工具参数通过 TypeBox + AJV 自动验证

### 3.4 pi-tui：终端 UI 框架

**设计选择**：追加式 TUI（非全屏），保留原生终端滚动和搜索。

**关键技术**：
- **保留模式 UI（Retained Mode）**：组件树 + 缓存渲染结果
- **差分渲染（Differential Rendering）**：找到第一个变化行，从该行重新渲染到末尾
- **同步输出**：使用 `CSI ?2026h/l` 转义序列实现原子化显示，消除闪烁

### 3.5 pi-coding-agent：CLI 编码代理

作为顶层应用，负责串联一切：
- 会话管理（树结构 JSONL）
- 配置（settings.json、models.json）
- 扩展加载（TypeScript 热重载）
- 上下文工程（AGENTS.md、SYSTEM.md、Skills）
- 四种运行模式（Interactive、Print/JSON、RPC、SDK）

---

## 四、方案设计详解

### 4.1 四个核心工具的设计

```
read   — 读取文件内容（支持文本和图片），默认前 2000 行，支持 offset/limit
write  — 写入文件，自动创建父目录
edit   — 精确文本替换（oldText 必须完全匹配）
bash   — 执行 bash 命令，可选超时
```

**为什么只需 4 个工具？**
- 现代 LLM 已经通过 RL 在 bash 上充分训练
- `bash` 可以覆盖 grep、git、find、curl 等所有命令行操作
- 极少的工具意味着极少的 context 消耗和极高的可靠性
- Terminal-Bench 2.0 基准测试验证：极简工具集的效果不逊于复杂工具集

### 4.2 扩展系统（Extension System）

扩展是 TypeScript 模块，通过默认导出函数接收 `ExtensionAPI`：

```typescript
export default function (pi: ExtensionAPI) {
  // 事件订阅
  pi.on("tool_call", async (event, ctx) => { ... });
  // 注册工具
  pi.registerTool({ name: "greet", ... });
  // 注册命令
  pi.registerCommand("hello", { ... });
  // 注册快捷键
  pi.registerShortcut("ctrl+x", { ... });
}
```

**扩展能力矩阵**：

| 能力 | API |
|------|-----|
| 事件拦截/修改 | `pi.on(event, handler)` — 可 block、modify、inject |
| 自定义工具 | `pi.registerTool()` |
| 自定义命令 | `pi.registerCommand()` |
| 自定义快捷键 | `pi.registerShortcut()` |
| 状态持久化 | `pi.appendEntry()` — 自定义条目存入 session |
| 自定义 UI | `ctx.ui.custom()` — 完整 TUI 组件 |
| 自定义渲染 | `pi.registerMessageRenderer()` |
| 模型/提供者管理 | `pi.setModel()`、`pi.registerProvider()` |

**扩展生命周期事件**：

```
pi starts
├─► session_start
└─► resources_discover
    ↓
user prompt
├─► input (可拦截/转换)
├─► before_agent_start (可注入消息/修改系统提示)
├─► agent_start
│   ├─► turn_start
│   │   ├─► context (可修改消息)
│   │   ├─► before_provider_request
│   │   ├─► tool_call (可 block)
│   │   ├─► tool_result (可 modify)
│   │   └─► turn_end
│   └─► agent_end
```

**热重载**：放入 `~/.pi/agent/extensions/` 或 `.pi/extensions/`，用 `/reload` 即时生效。

### 4.3 Skills 系统

Skills 是按需加载的能力包，遵循 [Agent Skills 标准](https://agentskills.io)：

**渐进式披露（Progressive Disclosure）**：
1. 启动时只扫描 name + description（极少 token）
2. 系统提示以 XML 格式列出可用 skills
3. 模型按需用 `read` 加载完整 `SKILL.md`
4. 技能内的脚本和资源通过相对路径引用

```
my-skill/
├── SKILL.md          # 必需：frontmatter + 指令
├── scripts/          # 辅助脚本
├── references/       # 按需加载的详细文档
└── assets/           # 模板和资源
```

**vs MCP 的优势**：
- MCP 服务器（如 Playwright MCP 21 工具 13.7k tokens）会一次性注入所有工具描述
- Skills 只在需要时加载，token 成本按需支付
- CLI 工具 + README 可组合、可管道、易扩展

### 4.4 会话管理（Session Management）

**树结构会话**：每条消息有 `id` 和 `parentId`，形成树而非线性链。

```
├─ user: "Hello..."
│  └─ assistant: "Of course..."
│     ├─ user: "Approach A..."        ← 分支 1
│     │  └─ assistant: "For A..."
│     └─ user: "Approach B..."        ← 分支 2
│        └─ assistant: "For B..."
```

**核心操作**：
- `/tree` — 可视化导航到任意历史节点，从该点继续
- `/fork` — 从当前位置创建新会话文件
- `/clone` — 克隆完整会话到新文件
- 分支摘要 — 切换分支时可选择是否生成上下文摘要

**存储格式**：JSONL 文件，包含消息、模型变更、thinking level、标签、压缩、分支摘要、扩展自定义条目。

### 4.5 SDK 与编程式使用

Pi 提供完整的 SDK 用于嵌入式集成：

```typescript
const { session } = await createAgentSession({
  sessionManager: SessionManager.inMemory(),
  authStorage,
  modelRegistry,
});

session.subscribe((event) => { /* 事件流处理 */ });
await session.prompt("What files are in the current directory?");
```

**四种运行模式**：

| 模式 | 用途 |
|------|------|
| Interactive | 完整 TUI 体验 |
| Print/JSON | `pi -p "query"` 脚本集成 |
| RPC | stdin/stdout JSONL 协议，非 Node 集成 |
| SDK | 嵌入 Node.js 应用，如 OpenClaw |

### 4.6 上下文工程（Context Engineering）

Pi 的上下文管理策略：

| 机制 | 说明 |
|------|------|
| AGENTS.md | 项目指令，启动时从 `~/.pi/agent/`、父目录、当前目录层级加载 |
| SYSTEM.md | 替换或追加默认系统提示 |
| Compaction | 接近上下文限制时自动摘要旧消息，可通过 extension 完全自定义 |
| Skills | 按需加载的能力包，渐进式披露 |
| Prompt Templates | 可复用提示模板，`/name` 展开 |
| Dynamic Context | Extension 可在每轮前注入消息、过滤历史、实现 RAG 或长期记忆 |

---

## 五、关键实现细节

### 5.1 跨提供者兼容性处理

Pi 在 `openai-completions.ts` 中处理各提供者差异：
- Cerebras/xAI/Mistral 不支持 `store` 字段
- Mistral 用 `max_tokens` 而非 `max_completion_tokens`
- 不同提供者的推理内容在不同字段（`reasoning_content` vs `reasoning`）
- Google 至今不支持工具调用流式传输

### 5.2 Steering 与 Follow-up

Pi 支持在 agent 工作时提交消息：
- **Enter**（Steering）：当前工具完成后立即插入，中断后续工具调用
- **Alt+Enter**（Follow-up）：等待 agent 完成后再处理

### 5.3 Benchmark 验证

在 Terminal-Bench 2.0 上，Pi + Claude Opus 4.5 的表现：
- 与使用复杂工具集的 Codex、Cursor、Windsurf 持平甚至超越
- 证明了"强模型 + 极简 runtime"的可行性
- 值得注意：Terminus 2（只给模型一个 tmux 会话）也表现不俗

---

## 六、对 Psi 项目的核心借鉴

### 6.1 高度吻合的部分

| 维度 | Pi | Psi | 吻合度 |
|------|-----|-----|--------|
| Loop-first | 极简 agent loop | ExecutionLoop | ★★★★★ |
| 薄壳哲学 | 反对大编排/大 workflow | 只保留 Task/Loop/Tool/State | ★★★★★ |
| Tool-native | Everything is tool | ToolRegistry 统一接口 | ★★★★★ |
| 可生长性 | Extension surface | 薄壳演进 | ★★★★☆ |

### 6.2 Pi 验证了的关键假设

1. **强模型 + 极简 runtime 确实可以工作** — Terminal-Bench 已证明
2. **4 个工具足够** — bash 覆盖一切命令行操作
3. **不到 1000 tokens 的 system prompt 足够** — 模型已被 RL 训练理解编码 agent
4. **树结构会话** 比线性会话更有价值
5. **渐进式披露**（Skills）比一次性注入（MCP）更 token 高效

### 6.3 Psi 应从 Pi 直接借鉴的设计

#### （1）系统应"小到能被模型理解"

Pi 最厉害的地方：runtime complexity 极低，模型自己能理解自己的运行环境。Psi 的每个设计决策都应问：

> "模型自己能理解这个 runtime 吗？"

#### （2）Extension Surface 而非 Feature

不做 features，做 extension surface。未来的 subagents、workflows、memory、UI 都应该是"后生长"出来的，而非内建的。

**具体参考 Pi 的扩展 API 设计**：
- 事件驱动（on/emit 模式）
- 工具注册（registerTool）
- 状态持久化（appendEntry）
- 生命周期钩子（before_agent_start、tool_call、tool_result 等）
- 热重载（/reload）

#### （3）渐进式上下文加载

借鉴 Pi 的 Skills 模式：
- 启动时只注入 name + description（极小 token 开销）
- 按需读取完整指令
- 远优于 MCP 的全量注入

#### （4）树结构状态管理

Psi 的 StateStore 应参考 Pi 的树结构会话：
- 每个状态节点有 `id` + `parentId`
- 支持分支、回溯、从任意点恢复
- JSONL append-only 存储，天然支持回放

#### （5）跨模型上下文交接

Psi 的 LLM 抽象层应参考 `pi-ai` 的设计：
- 统一多提供者协议
- 支持会话中途切换模型
- thinking traces 自动转换
- 上下文可序列化/反序列化

### 6.4 Psi 应超越 Pi 的部分

| 维度 | Pi 的局限 | Psi 的方向 |
|------|-----------|-----------|
| 场景 | Coding-centric（read/write/edit/bash 围绕 code workspace） | General task runtime（computer use、browser、desktop） |
| 状态持久化 | 偏 session/conversational | Durable execution（checkpoint/resume/retry） |
| 长期运行 | Interactive coding session | Long-running execution runtime |
| 安全 | YOLO（无安全边界） | Minimal Safety Gate（拦截底线风险） |
| 并行 | 无内建（靠 tmux） | 轻量子 Loop 并行 |
| 结构化 | 自由文本为主 | 结构化优先（TaskSpec、验收标准） |

### 6.5 风险提醒

| 风险 | Pi 的教训 | Psi 的对策 |
|------|-----------|-----------|
| 系统逐渐变厚 | Pi 坚持"不需要就不做" | 每个新增模块都问"模型能理解吗？" |
| 过早抽象 | Pi 几乎不做 planner/orchestration/hierarchy 抽象 | 先跑通 MVP，再决定抽象 |
| Extension 成为新的复杂度来源 | Pi 的 extension API 极其丰富但核心仍简单 | Extension 只做加法，不改核心 Loop |

---

## 七、Pi 代码仓关键文件索引

| 路径 | 说明 |
|------|------|
| `packages/ai/src/providers/` | 各 LLM 提供者的适配实现 |
| `packages/ai/src/agent/agent-loop.ts` | Agent 核心循环 |
| `packages/ai/src/models.generated.ts` | 自动生成的模型注册表 |
| `packages/agent/` | Agent 类、状态管理、传输抽象 |
| `packages/coding-agent/src/core/system-prompt.ts` | 系统提示定义 |
| `packages/coding-agent/examples/extensions/` | 50+ 扩展示例 |
| `packages/coding-agent/examples/sdk/` | SDK 使用示例 |
| `packages/coding-agent/docs/` | 完整文档源 |

---

## 八、一手信息源索引

| 来源 | URL |
|------|-----|
| 官方网站 | https://pi.dev |
| GitHub 仓库 | https://github.com/earendil-works/pi |
| 官方文档 | https://pi.dev/docs/latest |
| 创始人博客 | https://mariozechner.at/posts/2025-11-30-pi-coding-agent/ |
| OpenClaw 集成 | https://github.com/OpenClaw/OpenClaw |
| Agent Skills 标准 | https://agentskills.io |
| Terminal-Bench 结果 | https://github.com/laude-institute/terminal-bench |
| Pi Skills 仓库 | https://github.com/badlogic/pi-skills |

---

## 九、结论

Pi 和 Psi 最本质的共同点是：

> **都认为未来 Agent 的核心不是"更复杂的 orchestration"，而是"更薄、更通用、更可生长的执行 runtime"。**

Pi 已经用 46k stars、214 个 release 和 Terminal-Bench 基准验证了这个方向的可行性。Psi 的定位是 Pi 的**下一阶段演进**——把极简 runtime 从 coding harness 推进到 general execution runtime，增加 durable execution、minimal safety gate 和 computer use 等维度，同时坚守"模型变强后系统变薄"的核心哲学。
