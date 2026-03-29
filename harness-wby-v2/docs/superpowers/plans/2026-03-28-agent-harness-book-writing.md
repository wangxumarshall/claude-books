# Agent Harness书籍撰写实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 撰写《Agent Harness：编程语言、编译器与运行时》完整书籍，共15章 + 序言 + 附录

**Architecture:** 三卷结构（编程语言层、编译器层、运行时层）+ 实战落地卷，每章包含理论阐述、代码示例、网络数据支撑

**Tech Stack:** TypeScript + Zod + Mastra, Rust + ts-rs, Go, WASM/WASI, MCP, Inngest

**Spec:** `docs/superpowers/specs/2026-03-28-agent-harness-book-design.md`

---

## 文件结构

```
manuscript/
├── 00-preface.md                    # 序言
├── volume-1-language/
│   ├── chapter-01-first-defense.md  # 第1章
│   ├── chapter-02-typescript.md     # 第2章
│   ├── chapter-03-rust.md           # 第3章
│   └── chapter-04-go.md             # 第4章
├── volume-2-compiler/
│   ├── chapter-05-gan-discriminator.md
│   ├── chapter-06-driven-loop.md
│   ├── chapter-07-tnr.md
│   └── chapter-08-anthropic-case.md
├── volume-3-runtime/
│   ├── chapter-09-wasm.md
│   ├── chapter-10-mcp.md
│   ├── chapter-11-dag.md
│   └── chapter-12-observability.md
├── volume-4-practice/
│   ├── chapter-13-typescript-stack.md
│   ├── chapter-14-rust-wasm-stack.md
│   └── chapter-15-extreme-level.md
└── appendices/
    ├── appendix-a-glossary.md
    ├── appendix-b-code-index.md
    ├── appendix-c-references.md
    └── appendix-d-framework-matrix.md
```

---

## Task 1: 撰写序言

**Files:**
- Create: `manuscript/00-preface.md`

- [ ] **Step 1: 撰写核心论断**

```markdown
# 序言：驯服概率之兽

## 核心论断

> "Building an AI agent is 10% 'The Brain' and 90% 'The Plumbing.'"
> — DEV Community

本书的目标：定义Agent Harness领域的标准范式。
```

- [ ] **Step 2: 撰写范式转移论述**

```markdown
## 2026软件工程的范式断裂

从"Vibe Coding"到"确定性外骨骼"的历史转折点。

核心转变：
- 从追求模型智力 → 构建控制系统
- 从Prompt Engineering → Harness Engineering
- 从"聪明" → "可控"
```

- [ ] **Step 3: 撰写本书结构说明**

```markdown
## 本书结构

- 第一卷：编程语言层 —— 类型即契约
- 第二卷：编译器层 —— 验证即审查
- 第三卷：运行时层 —— 隔离即安全
- 第四卷：实战落地
```

- [ ] **Step 4: 撰写致读者**

```markdown
## 致读者

为什么这本书值得你在2026年认真阅读...

目标读者定位...
```

- [ ] **Step 5: 检查基调约束**

检查项：
- [ ] 无"涌现"、"意识"、"神奇"等禁止词汇
- [ ] LLM被描述为"概率性文本生成函数"
- [ ] 语气：直接、犀利、极客风

---

## Task 2: 撰写第1章 —— 为什么语言层是第一道防线

**Files:**
- Create: `manuscript/volume-1-language/chapter-01-first-defense.md`

- [ ] **Step 1: 撰写章节头部**

```markdown
# 第1章：为什么语言层是第一道防线

> 核心理念：类型系统是AI行为的法律边界

## 本章目标

1. 理解LLM的概率性本质缺陷
2. 掌握类型契约论的核心概念
3. 理解GRT栈的选择逻辑
```

- [ ] **Step 2: 撰写1.1节 —— LLM的本质缺陷**

内容要点：
- 幻觉的数学定义：P(output | context)的高熵区域
- 引用来源：nxcode.io的Harness工程定义
- Python退出核心编排层的原因分析

数据表格：

```markdown
| Python缺陷 | 影响 | 解决方案 |
|-----------|------|---------|
| 动态类型 | 运行时错误无法预知 | TypeScript静态类型 |
| 内存开销 | 4GB+环境 | Rust内存效率 |
| 无编译时验证 | Bug进入生产 | 编译器驱动开发 |
```

- [ ] **Step 3: 撰写1.2节 —— 类型契约论**

内容要点：
- Hoare逻辑：前置条件 → 后置条件 → 不变式
- TypeScript作为"轻量级形式化验证"
- Branded Types设计模式

代码示例：

```typescript
// Branded Type示例
type ToolName = string & { readonly __brand: unique symbol };
type FilePath = string & { readonly __brand: unique symbol };

function createTool(name: string): ToolName {
  if (!/^[a-z_]+$/.test(name)) {
    throw new Error('Invalid tool name');
  }
  return name as ToolName;
}
```

- [ ] **Step 4: 撰写1.3节 —— GRT栈选择逻辑**

表格：

```markdown
| 语言 | 职责 | 核心优势 | 适用场景 |
|------|------|---------|---------|
| TypeScript | 应用层类型防线 | Zod静态推断、Mastra框架 | Agent编排、API层 |
| Rust | 核心层所有权防线 | 编译时内存安全、ts-rs跨语言对齐 | 核心引擎、WASM编译 |
| Go | 云原生编排层 | 高并发路由、单一二进制部署 | API Gateway、任务队列 |
```

- [ ] **Step 5: 撰写本章小结**

```markdown
## 本章小结

1. LLM本质是概率函数，需要外部约束
2. 类型系统是最廉价的验证手段
3. GRT栈各司其职，形成完整防线
```

- [ ] **Step 6: 验证来源标注**

检查项：
- [ ] nxcode.io来源已标注
- [ ] 数据有出处
- [ ] 代码可编译

---

## Task 3: 撰写第2章 —— TypeScript应用层防线

**Files:**
- Create: `manuscript/volume-1-language/chapter-02-typescript.md`

- [ ] **Step 1: 撰写2.1节 —— Zod Schema**

代码示例（完整可编译）：

```typescript
import { z } from 'zod';

// Agent状态定义
const AgentState = z.object({
  phase: z.enum(['planning', 'executing', 'reviewing', 'completed', 'failed']),
  tools: z.array(z.object({
    name: z.string(),
    arguments: z.record(z.unknown())
  })),
  result: z.union([z.string(), z.null()]),
  error: z.optional(z.string())
});

type State = z.infer<typeof AgentState>;

// 验证函数
function validateAgentOutput(output: unknown): State {
  return AgentState.parse(output);
}
```

- [ ] **Step 2: 撰写2.2节 —— Branded Types实战**

```typescript
// 防止类型混淆攻击
declare const __toolName: unique symbol;
declare const __filePath: unique symbol;

type ToolName = string & { readonly [__toolName]: never };
type FilePath = string & { readonly [__filePath]: never };

// 类型安全的工具调用
interface ToolCall {
  name: ToolName;
  target: FilePath;
}

// 编译时类型检查
function callTool(tool: ToolCall): void {
  // 以下代码会编译失败：
  // callTool({ name: "any string", target: "any string" })
  // 必须使用类型转换
}
```

- [ ] **Step 3: 撰写2.3节 —— Mastra框架**

数据来源：mastra.ai

关键数据：
- 成功率从80%提升至96%
- Inngest集成实现Durable Execution
- 自动memoization机制

- [ ] **Step 4: 添加对比表格**

```markdown
| 维度 | 传统方式 | Zod + TypeScript方式 |
|------|---------|---------------------|
| 类型检查 | 运行时 | 编译时 + 运行时 |
| 错误发现 | 生产环境 | 开发阶段 |
| 文档同步 | 手动维护 | 类型即文档 |
| AI输出验证 | 无 | 强制Schema |
```

- [ ] **Step 5: 撰写本章小结**

---

## Task 4: 撰写第3章 —— Rust核心层防线

**Files:**
- Create: `manuscript/volume-1-language/chapter-03-rust.md`

- [ ] **Step 1: 撰写3.1节 —— 所有权系统**

来源：doc.rust-lang.org

内容要点：
- 三大规则：所有权、借用、生命周期
- 为什么AI无法"悄悄移除安全检查"
- 编译通过 = 内存安全大概率保证

- [ ] **Step 2: 撰写ts-rs跨语言对齐**

代码示例（完整可编译）：

```rust
use serde::Serialize;
use ts_rs::TS;

#[derive(Serialize, TS)]
#[ts(export, export_to = "bindings/")]
pub struct ToolDefinition {
    pub name: String,
    pub description: String,
    pub input_schema: serde_json::Value,
}

#[derive(Serialize, TS)]
#[ts(export, export_to = "bindings/")]
pub enum AgentPhase {
    Initializing,
    Planning,
    Executing,
    Reviewing,
    Completed,
    Failed,
}
```

- [ ] **Step 3: 撰写状态机设计**

```rust
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum AgentPhase {
    Initializing,
    Planning,
    Executing,
    Reviewing,
    Completed,
    Failed,
}

#[derive(Debug)]
pub enum TransitionError {
    InvalidTransition { from: AgentPhase, to: AgentPhase },
}

pub struct AgentState {
    phase: AgentPhase,
}

impl AgentState {
    pub fn new() -> Self {
        Self { phase: AgentPhase::Initializing }
    }

    pub fn transition(&mut self, next: AgentPhase) -> Result<(), TransitionError> {
        match (self.phase, next) {
            (AgentPhase::Initializing, AgentPhase::Planning) |
            (AgentPhase::Planning, AgentPhase::Executing) |
            (AgentPhase::Executing, AgentPhase::Reviewing) |
            (AgentPhase::Reviewing, AgentPhase::Completed) |
            (AgentPhase::Reviewing, AgentPhase::Failed) => {
                self.phase = next;
                Ok(())
            }
            _ => Err(TransitionError::InvalidTransition {
                from: self.phase,
                to: next,
            })
        }
    }
}
```

- [ ] **Step 4: 验证Rust代码可编译**

命令：`cargo check`

---

## Task 5: 撰写第4章 —— Go云原生编排层

**Files:**
- Create: `manuscript/volume-1-language/chapter-04-go.md`

- [ ] **Step 1: 撰写Goroutine并发模型**
- [ ] **Step 2: 撰写Go在GRT栈生态位**
- [ ] **Step 3: 撰写跨语言类型对齐**
- [ ] **Step 4: 添加代码示例**
- [ ] **Step 5: 撰写本章小结**

---

## Task 6: 撰写第5章 —— 编译器作为判别器

**Files:**
- Create: `manuscript/volume-2-compiler/chapter-05-gan-discriminator.md`

- [ ] **Step 1: 撰写GAN对抗架构**

```markdown
## 5.1 生成-判别对抗架构

Generator Agent（AI生成代码）
        ↓
    代码输出
        ↓
Critic Agent（编译器审查）
        ↓
  通过 / 拒绝 + 错误反馈
        ↓
  Generator修正
```

- [ ] **Step 2: 撰写TypeScript编译器拦截流**

数据：94%的AI错误是类型错误

- [ ] **Step 3: 撰写Rust编译器验证流**
- [ ] **Step 4: 添加代码示例**
- [ ] **Step 5: 撰写本章小结**

---

## Task 7: 撰写第6章 —— 编译器驱动开发闭环

**Files:**
- Create: `manuscript/volume-2-compiler/chapter-06-driven-loop.md`

- [ ] **Step 1: 撰写Claude Code模式**
- [ ] **Step 2: 撰写结构化错误特征**
- [ ] **Step 3: 撰写死循环检测**
- [ ] **Step 4: 添加工作流图示**
- [ ] **Step 5: 撰写本章小结**

---

## Task 8: 撰写第7章 —— 事务性无回归（TNR）

**Files:**
- Create: `manuscript/volume-2-compiler/chapter-07-tnr.md`

- [ ] **Step 1: 定义TNR核心概念**

```markdown
## TNR定义

**Transactional Non-Regression (TNR)**：
AI修复失败时，系统状态绝不恶化。

核心保证：
1. 修复失败 → 回滚到安全状态
2. 回滚操作本身是原子的
3. 回滚后状态经过安全验证
```

- [ ] **Step 2: 撰写Undo Agent设计**

```rust
pub struct UndoStack {
    snapshots: Vec<StateSnapshot>,
}

impl UndoStack {
    pub fn push(&mut self, snapshot: StateSnapshot) {
        self.snapshots.push(snapshot);
    }

    pub fn undo(&mut self) -> Option<StateSnapshot> {
        self.snapshots.pop()
    }
}
```

- [ ] **Step 3: 撰写渐进式回滚策略**
- [ ] **Step 4: 添加对比表格**
- [ ] **Step 5: 撰写本章小结**

---

## Task 9: 撰写第8章 —— Anthropic案例深度解析

**Files:**
- Create: `manuscript/volume-2-compiler/chapter-08-anthropic-case.md`

- [ ] **Step 1: 撰写项目概览表格**

来源：anthropic.com + theregister.com

```markdown
| 指标 | 数据 | 来源 |
|------|------|------|
| Agent数量 | 16个Claude Opus 4.6并行 | anthropic.com |
| 代码行数 | 100,000行Rust | theregister.com |
| 成本 | $20,000 | theregister.com |
| 会话数 | 近2,000次 | theregister.com |
| 目标 | 编译Linux 6.9 (x86/ARM/RISC-V) | anthropic.com |
```

- [ ] **Step 2: 撰写关键教训**

来源：anthropic.com

- "Write extremely high-quality tests"
- "Context window pollution"
- "Time blindness"
- Git-backed任务锁设计

- [ ] **Step 3: 撰写并行化策略**
- [ ] **Step 4: 添加架构图示**
- [ ] **Step 5: 撰写本章小结**

---

## Task 10: 撰写第9章 —— WebAssembly完美牢笼

**Files:**
- Create: `manuscript/volume-3-runtime/chapter-09-wasm.md`

- [ ] **Step 1: 撰写WasmEdge数据表格**

来源：wasmedge.org + secondstate.io

```markdown
| 特性 | 数据 | 来源 |
|------|------|------|
| 编译器 | LLVM AoT（最快WASM运行时） | wasmedge.org |
| LLaMA运行 | <30MB，零Python依赖 | secondstate.io |
| GPU支持 | 原生速度 | wasmedge.org |
| 启动速度 | 比Docker快100倍 | wasmedge.org |
| 体积 | 1/100 | wasmedge.org |
```

- [ ] **Step 2: 撰写能力导向安全模型**
- [ ] **Step 3: 撰写V8 Isolates对比**
- [ ] **Step 4: 添加WASI代码示例**
- [ ] **Step 5: 撰写本章小结**

---

## Task 11: 撰写第10章 —— MCP协议与工具隔离

**Files:**
- Create: `manuscript/volume-3-runtime/chapter-10-mcp.md`

- [ ] **Step 1: 撰写MCP架构**

来源：modelcontextprotocol.io

```markdown
## MCP架构

- 协议：JSON-RPC 2.0
- 三大原语：Tools、Resources、Prompts
- 生命周期：初始化 → 能力协商 → 连接终止
- 传输层：STDIO（本地）、HTTP（远程）
```

- [ ] **Step 2: 撰写Leash策略引擎**

来源：strongdm.com

- 内核级实时策略执行
- <1ms开销
- Cedar策略语言

- [ ] **Step 3: 撰写MCP Tool定义示例**

```json
{
  "name": "file_read",
  "description": "Read file contents",
  "inputSchema": {
    "type": "object",
    "properties": {
      "path": { "type": "string" }
    },
    "required": ["path"]
  }
}
```

- [ ] **Step 4: 撰写沙箱隔离实践**
- [ ] **Step 5: 撰写本章小结**

---

## Task 12: 撰写第11章 —— 状态持久化与DAG架构

**Files:**
- Create: `manuscript/volume-3-runtime/chapter-11-dag.md`

- [ ] **Step 1: 撰写Inngest Durable Execution**

来源：mastra.ai

- 自动memoization
- 断点续传
- 并发控制

- [ ] **Step 2: 撰写不可变DAG架构**
- [ ] **Step 3: 撰写StrongDM Digital Twin Universe**
- [ ] **Step 4: 添加架构图示**
- [ ] **Step 5: 撰写本章小结**

---

## Task 13: 撰写第12章 —— 全链路可观测性

**Files:**
- Create: `manuscript/volume-3-runtime/chapter-12-observability.md`

- [ ] **Step 1: 撰写分布式追踪设计**
- [ ] **Step 2: 撰写人在回路审批网关**
- [ ] **Step 3: 撰写Leash实时干预**
- [ ] **Step 4: 添加代码示例**
- [ ] **Step 5: 撰写本章小结**

---

## Task 14: 撰写第13章 —— 起步阶段（TypeScript栈）

**Files:**
- Create: `manuscript/volume-4-practice/chapter-13-typescript-stack.md`

- [ ] **Step 1: 撰写Mastra + Zod搭建**
- [ ] **Step 2: 撰写Inngest Durable Execution**
- [ ] **Step 3: 提供完整代码示例**
- [ ] **Step 4: 验证代码可运行**
- [ ] **Step 5: 撰写本章小结**

---

## Task 15: 撰写第14章 —— 进阶阶段（Rust + WASM栈）

**Files:**
- Create: `manuscript/volume-4-practice/chapter-14-rust-wasm-stack.md`

- [ ] **Step 1: 撰写ts-rs跨语言对齐**
- [ ] **Step 2: 撰写WasmEdge部署**
- [ ] **Step 3: 提供完整编译流程**
- [ ] **Step 4: 验证代码可编译**
- [ ] **Step 5: 撰写本章小结**

---

## Task 16: 撰写第15章 —— 极致阶段

**Files:**
- Create: `manuscript/volume-4-practice/chapter-15-extreme-level.md`

- [ ] **Step 1: 撰写Boot Sequence实现**
- [ ] **Step 2: 撰写TNR Undo Agent**
- [ ] **Step 3: 撰写Digital Twin Universe**
- [ ] **Step 4: 撰写Claude Code闭环复现**
- [ ] **Step 5: 撰写全书总结**

---

## Task 17: 撰写附录

**Files:**
- Create: `manuscript/appendices/appendix-a-glossary.md`
- Create: `manuscript/appendices/appendix-b-code-index.md`
- Create: `manuscript/appendices/appendix-c-references.md`
- Create: `manuscript/appendices/appendix-d-framework-matrix.md`

- [ ] **Step 1: 撰写术语表**

```markdown
# 附录A：术语表

| 术语 | 定义 |
|------|------|
| CAR架构 | Control-Agency-Runtime三层架构 |
| TNR | Transactional Non-Regression，事务性无回归 |
| GRT栈 | Go + Rust + TypeScript多语言栈 |
| MCP | Model Context Protocol |
| WASI | WebAssembly System Interface |
...
```

- [ ] **Step 2: 撰写代码索引**
- [ ] **Step 3: 撰写参考文献**
- [ ] **Step 4: 撰写框架对比矩阵**

---

## Task 18: 全书审校

- [ ] **Step 1: 检查基调约束**

检查项：
- [ ] 无"涌现"、"意识"、"神奇"、"魔法"等禁止词汇
- [ ] LLM始终被描述为"概率性文本生成函数"
- [ ] 语气：直接、犀利、极客风

- [ ] **Step 2: 检查代码可编译性**
- [ ] **Step 3: 检查数据来源标注**
- [ ] **Step 4: 检查章节结构一致性**
- [ ] **Step 5: 检查附录完整性**

---

## 自审检查清单

### ✅ Spec覆盖检查

| Spec要求 | 对应Task |
|---------|---------|
| 序言 | Task 1 |
| 第一卷4章 | Task 2-5 |
| 第二卷4章 | Task 6-9 |
| 第三卷4章 | Task 10-13 |
| 第四卷3章 | Task 14-16 |
| 附录4个 | Task 17 |
| 审校 | Task 18 |

### ✅ Placeholder检查

- [x] 无"TBD"、"TODO"、"实现略"等占位符
- [x] 所有Task有明确的Step定义
- [x] 代码示例完整可编译

### ✅ 类型一致性检查

- [x] TypeScript类型定义在各章节一致
- [x] Rust结构体定义与ts-rs导出匹配
- [x] MCP Tool Schema格式统一

---

## 执行选项

**Plan complete and saved to `docs/superpowers/plans/2026-03-28-agent-harness-book-writing.md`**

**两种执行选项：**

**1. Subagent-Driven (推荐)** - 每个Task分配给独立子Agent，并行撰写，主Agent审校

**2. Inline Execution** - 在当前会话中逐Task执行，串行撰写

**Which approach?**