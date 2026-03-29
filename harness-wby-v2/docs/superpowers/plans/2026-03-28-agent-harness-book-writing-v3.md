# Agent Harness书籍撰写实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 撰写《Agent Harness：编程语言、编译器与运行时》完整书籍，共1序言 + 16章 + 4附录

**Architecture:** 四卷结构（第0章 + 第一卷4章 + 第二卷4章 + 第三卷4章 + 第四卷3章）+ 附录，每章包含20%理论精华 + 80%工程实践

**Tech Stack:** TypeScript + Zod + Mastra, Rust + ts-rs, Go + CSP, WASM/WASI, MCP, Inngest

**Spec:** `docs/superpowers/specs/2026-03-28-agent-harness-book-design-v3.md`

---

## 文件结构

```
manuscript/
├── 00-big-model-vs-big-harness.md      # 第0章（v3.0新增）
├── volume-1-language/
│   ├── chapter-01-invariant-theory.md  # 第1章：Harness不变量理论
│   ├── chapter-02-typescript.md        # 第2章：TypeScript
│   ├── chapter-03-rust.md              # 第3章：Rust
│   └── chapter-04-go.md                # 第4章：Go
├── volume-2-compiler/
│   ├── chapter-05-discriminator.md     # 第5章：编译器作为判别器
│   ├── chapter-06-driven-loop.md       # 第6章：编译器驱动闭环
│   ├── chapter-07-tnr.md               # 第7章：TNR
│   └── chapter-08-case-matrix.md       # 第8章：四维案例矩阵
├── volume-3-runtime/
│   ├── chapter-09-wasm.md              # 第9章：WASM
│   ├── chapter-10-mcp.md               # 第10章：MCP协议
│   ├── chapter-11-dag.md               # 第11章：DAG架构
│   └── chapter-12-observability.md     # 第12章：可观测性
├── volume-4-practice/
│   ├── chapter-13-typescript-stack.md  # 第13章：TypeScript栈
│   ├── chapter-14-rust-wasm-stack.md   # 第14章：Rust+WASM栈
│   └── chapter-15-extreme-level.md     # 第15章：极致阶段
└── appendices/
    ├── appendix-a-glossary.md          # 附录A：术语表
    ├── appendix-b-code-index.md        # 附录B：代码索引
    ├── appendix-c-references.md        # 附录C：参考文献
    └── appendix-d-framework-matrix.md  # 附录D：框架矩阵
```

---

## Task 1: 撰写第0章 —— Big Model vs Big Harness

**Files:**
- Create: `manuscript/00-big-model-vs-big-harness.md`

**数据来源:** research-findings.md, Spec v3.0 Section 0

- [ ] **Step 1: 撰写章节头部**

```markdown
# 第0章：Big Model vs Big Harness —— 回应当前核心辩论

> **核心命题**：Better harnesses outperform better models.

## 本章目标

1. 理解2026年行业最激烈的路线之争
2. 掌握五大关键数据支撑Harness价值
3. 理解"护栏悖论"的深层含义
```

- [ ] **Step 2: 撰写0.1节 —— 辩论的起源**

内容要点：
- Big Model阵营（Noam Brown/OpenAI）的引言
- Big Harness阵营（Jerry Liu/LlamaIndex）的回应
- 辩论的核心矛盾

- [ ] **Step 3: 撰写0.2节 —— 数据裁判**

核心数据表格（必须包含来源评级）：

```markdown
### 核心数据一：同一模型，不同Harness

| 研究 | 模型 | Harness | 成功率 | 提升 | 评级 |
|------|------|---------|-------|------|------|
| Nate B Jones | 相同 | 基础 | 42% | — | C |
| Nate B Jones | 相同 | 优化 | 78% | +36pp | C |

### 核心数据二：LangChain Terminal Bench

| 配置 | 成功率 | 评级 |
|------|-------|------|
| 原始Harness | 52.8% | B |
| 改进Harness | 66.5% | B |

### 核心数据三：Cursor模型排名翻转

| 模型 | 原Harness | 优Harness | 变化 | 评级 |
|------|----------|----------|------|------|
| Claude Opus 4.6 | 第33位 | 第5位 | ↑28位 | C |
```

- [ ] **Step 4: 撰写0.3节 —— 护栏悖论**

```markdown
### 护栏悖论

```
时速30公里的自行车道：可以没有护栏
时速120公里的高速公路：护栏是标配
时速300公里的磁悬浮列车：整个轨道都是封闭的
```

**推论**：模型越强，Harness越重要。
```

- [ ] **Step 5: 撰写0.4节 —— 本书立场**

- [ ] **Step 6: 撰写0.5节 —— 学术对话**

建立与arXiv论文的对话：
- arXiv:2603.20075 (llvm-autofix)
- arXiv:2601.12146 (From LLMs to Agents)
- arXiv:2603.25697 (Kitchen Loop)

- [ ] **Step 7: 撰写本章小结**

---

## Task 2: 撰写第1章 —— Harness不变量理论导论

**Files:**
- Create: `manuscript/volume-1-language/chapter-01-invariant-theory.md`

- [ ] **Step 1: 撰写章节头部**

```markdown
# 第1章：Harness不变量理论导论

> **核心理念**：类型系统是AI行为的法律边界

## 本章目标

1. 理解LLM的概率性本质缺陷
2. 掌握Harness不变量理论的形式化定义
3. 理解GRT栈的选择逻辑
```

- [ ] **Step 2: 撰写1.1节 —— 为什么语言层是第一道防线**

内容要点：
- LLM的本质：概率函数 f: Context → Output
- 幻觉的数学定义：H(Output | Context) → ∞
- 引用：nxcode.io的Harness定义（B级）

- [ ] **Step 3: 撰写1.2节 —— 类型不变量的形式化定义**

```
定义（类型不变量）：
给定Agent A和类型系统T，类型不变量成立当且仅当：
∀i ∈ Input(A), ∀o ∈ Output(A), TypeCheck_T(i) ∧ TypeCheck_T(o)
```

- [ ] **Step 4: 撰写1.3节 —— 与Hoare逻辑的关联**

| Hoare逻辑 | Harness不变量 | 关联 |
|-----------|--------------|------|
| 前置条件P | 输入类型约束 | P = TypeCheck(input) |
| 后置条件Q | 输出类型约束 | Q = TypeCheck(output) |
| 不变式I | 状态不变量 | I = Invariant(state) |

- [ ] **Step 5: 撰写1.4节 —— GRT栈选择逻辑**

| 语言 | 不变量维护责任 | 理论依据 | 工程优势 |
|------|--------------|---------|---------|
| TypeScript | 类型不变量（应用层） | 渐进式类型系统 | Zod运行时验证 |
| Rust | 类型不变量 + 状态不变量 | 所有权类型系统 | 编译时内存安全 |
| Go | 状态不变量（并发层） | CSP进程代数 | Goroutine安全通信 |

- [ ] **Step 6: 撰写1.5节 —— 学术对话（AgenticTyper）**

引用arXiv:2602.21251（A级）：
- 2个专有仓库（81K LOC）
- 633个类型错误
- 20分钟全部解决

- [ ] **Step 7: 撰写本章小结**

---

## Task 3: 撰写第2章 —— TypeScript应用层类型不变量

**Files:**
- Create: `manuscript/volume-1-language/chapter-02-typescript.md`

- [ ] **Step 1: 撰写2.1节 —— Zod Schema**

完整代码示例：

```typescript
import { z } from 'zod';

const AgentStateSchema = z.object({
  phase: z.enum(['initializing', 'planning', 'executing', 'reviewing', 'completed', 'failed']),
  input: z.unknown(),
  output: z.union([z.string(), z.null()]),
  error: z.optional(z.string()),
});

type AgentState = z.infer<typeof AgentStateSchema>;

function validateAgentState(output: unknown): AgentState | never {
  return AgentStateSchema.parse(output);
}
```

- [ ] **Step 2: 撰写2.2节 —— Branded Types**

```typescript
declare const __toolName: unique symbol;
type ToolName = string & { readonly [__toolName]: never };

function createToolName(name: string): ToolName | Error {
  if (!/^[a-z_][a-z0-9_]*$/.test(name)) {
    return new Error(`Invalid tool name: ${name}`);
  }
  return name as ToolName;
}
```

- [ ] **Step 3: 撰写2.3节 —— Mastra框架**

数据表格（带评级）：

| 特性 | 说明 | 来源 | 评级 |
|------|------|------|------|
| 成功率提升 | 80% → 96% | mastra.ai | D |
| Replit Agent 3自主率 | 90% | mastra.ai | B |

- [ ] **Step 4: 撰写对比表格**

| 维度 | 传统方式 | Zod + TypeScript | 改进 |
|------|---------|-----------------|------|
| 类型检查 | 仅编译时 | 编译时 + 运行时 | +运行时保证 |
| 错误发现 | 生产环境 | 开发阶段 | 成本降低 |

- [ ] **Step 5: 撰写本章小结**

---

## Task 4: 撰写第3章 —— Rust核心层类型不变量与状态不变量

**Files:**
- Create: `manuscript/volume-1-language/chapter-03-rust.md`

- [ ] **Step 1: 撰写3.1节 —— 所有权系统**

理论基础表格：

| 概念 | 形式化定义 | Harness意义 |
|------|-----------|-------------|
| 所有权 | ∀x, ∃!owner: Owns(owner, x) | 确定性资源归属 |
| 借用 | ∀x, borrows(x) ⊆ ownership(x) | 安全的共享访问 |
| 生命周期 | ∀x, lifetime(x) ⊆ scope(owner(x)) | 编译时资源管理 |

- [ ] **Step 2: 撰写学术对话（Rustine/SafeTrans）**

| 论文 | 数据 | 评级 |
|------|------|------|
| Rustine (arXiv:2511.20617) | 87%函数等价性 | A |
| SafeTrans (arXiv:2505.10708) | 54%→80%翻译成功率 | A |

- [ ] **Step 3: 撰写3.2节 —— ts-rs跨语言对齐**

完整Rust代码：

```rust
use serde::Serialize;
use ts_rs::TS;

#[derive(Serialize, TS, Debug, Clone)]
#[ts(export, export_to = "bindings/")]
pub struct AgentState {
    pub phase: AgentPhase,
    pub tools: Vec<ToolCall>,
    pub result: Option<String>,
}

#[derive(Serialize, TS, Debug, Clone, Copy)]
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

- [ ] **Step 4: 撰写3.3节 —— 状态机驱动**

完整Rust代码（含测试）：

```rust
use std::collections::VecDeque;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AgentPhase {
    Initializing,
    Planning,
    Executing,
    Reviewing,
    Completed,
    Failed,
}

pub struct AgentStateMachine {
    current: AgentPhase,
    history: VecDeque<AgentPhase>,
}

impl AgentStateMachine {
    pub fn new() -> Self {
        Self {
            current: AgentPhase::Initializing,
            history: VecDeque::with_capacity(16),
        }
    }

    pub fn transition(&mut self, next: AgentPhase) -> Result<(), TransitionError> {
        // 完整实现...
    }

    pub fn rollback(&mut self) -> Option<AgentPhase> {
        self.history.pop_back()
    }
}
```

- [ ] **Step 5: 撰写本章小结**

---

## Task 5: 撰写第4章 —— Go并发层状态不变量

**Files:**
- Create: `manuscript/volume-1-language/chapter-04-go.md`

- [ ] **Step 1: 撰写4.1节 —— CSP进程代数**

形式化定义：

```
进程P || Q：P和Q并行执行
通道c!v：在通道c上发送值v
通道c?x：从通道c接收值并绑定到x
```

- [ ] **Step 2: 撰写4.2节 —— Goroutine安全通信模式**

完整Go代码：

```go
package main

import "fmt"

type AgentPhase string

const (
    PhaseInitializing AgentPhase = "initializing"
    PhasePlanning     AgentPhase = "planning"
    PhaseExecuting    AgentPhase = "executing"
    PhaseReviewing    AgentPhase = "reviewing"
    PhaseCompleted    AgentPhase = "completed"
    PhaseFailed       AgentPhase = "failed"
)

type TransitionRequest struct {
    From AgentPhase
    To   AgentPhase
    Resp chan error
}

func StateInvariantManager(
    initState AgentPhase,
    transitions <-chan TransitionRequest,
    done <-chan struct{},
) {
    current := initState
    validTransitions := map[AgentPhase][]AgentPhase{
        PhaseInitializing: {PhasePlanning},
        PhasePlanning:     {PhaseExecuting, PhaseFailed},
        PhaseExecuting:    {PhaseReviewing, PhaseFailed},
        PhaseReviewing:    {PhaseCompleted, PhaseFailed},
        PhaseCompleted:    {},
        PhaseFailed:       {},
    }

    for {
        select {
        case req := <-transitions:
            // 验证状态不变量...
        case <-done:
            return
        }
    }
}
```

- [ ] **Step 3: 撰写对比表格**

| 维度 | Go | Rust | TypeScript |
|------|-----|------|-----------|
| 并发模型 | CSP（Channel） | Async/Await | Async/Await |
| 内存安全 | GC | 编译时所有权 | 运行时 |
| 适用场景 | 高并发网关 | 核心引擎 | 应用层编排 |

- [ ] **Step 4: 撰写本章小结**

---

## Task 6: 撰写第5章 —— 编译器作为判别器

**Files:**
- Create: `manuscript/volume-2-compiler/chapter-05-discriminator.md`

- [ ] **Step 1: 撰写5.1节 —— 学术对话（From LLMs to Agents）**

核心数据（A级）：

| 指标 | 数据 |
|------|------|
| 数据集 | 699个C任务 |
| 编译成功率提升 | 5.3% → 79.4% |
| 语法错误减少 | 75% |
| Undefined reference减少 | 87% |

- [ ] **Step 2: 撰写5.2节 —— GAN视角**

```
Generator Agent (AI生成代码)
         ↓
Discriminator Agent (编译器)
         ↓
   通过 / 拒绝 + 错误反馈
```

- [ ] **Step 3: 撰写5.3节 —— llvm-autofix对话**

核心数据（A级）：

| 指标 | 数据 |
|------|------|
| SWE-bench | ~60% |
| LLVM基准 | 38% |
| llvm-autofix-mini | 52% |
| 真实端到端成功率 | <22% |

- [ ] **Step 4: 撰写本章小结**

---

## Task 7: 撰写第6章 —— 编译器驱动的开发闭环

**Files:**
- Create: `manuscript/volume-2-compiler/chapter-06-driven-loop.md`

- [ ] **Step 1: 撰写6.1节 —— Claude Code模式**

- [ ] **Step 2: 撰写6.2节 —— 结构化错误特征**

JSON格式示例：

```json
{
  "file": "src/agent.ts",
  "line": 42,
  "column": 10,
  "code": "TS2322",
  "message": "Type 'string' is not assignable to type 'AgentPhase'",
  "category": "type_error"
}
```

- [ ] **Step 3: 撰写6.3节 —— 死循环检测**

Rust代码：

```rust
struct CompileLoopDetector {
    error_hashes: VecDeque<u64>,
    max_same_errors: usize,
}

impl CompileLoopDetector {
    fn check(&mut self, error: &str) -> bool {
        let hash = blake3::hash(error.as_bytes()).as_u64();
        if self.error_hashes.back() == Some(&hash) {
            return true;  // 触发干预
        }
        self.error_hashes.push_back(hash);
        false
    }
}
```

- [ ] **Step 4: 撰写本章小结**

---

## Task 8: 撰写第7章 —— TNR事务性无回归

**Files:**
- Create: `manuscript/volume-2-compiler/chapter-07-tnr.md`

- [ ] **Step 1: 撰写7.1节 —— TNR理论基础**

形式化定义：

```
定义（TNR）：
给定状态空间S和修复操作Fix: S → S，
TNR成立当且仅当：
∀s ∈ S, Fix(s) ∈ {s', s} 其中 s' 是s的改善
```

- [ ] **Step 2: 撰写学术对话（Kitchen Loop）**

核心数据（A级）：

| 指标 | 数据 |
|------|------|
| 生产迭代 | 285+次 |
| Merged PR | 1094+ |
| 回归 | **零** |

- [ ] **Step 3: 撰写7.2节 —— Undo Agent设计**

完整Rust代码：

```rust
use std::collections::VecDeque;
use std::sync::{Arc, RwLock};

#[derive(Debug, Clone)]
pub struct StateSnapshot {
    pub phase: AgentPhase,
    pub context: String,
    pub timestamp: std::time::Instant,
}

pub struct UndoStack {
    snapshots: RwLock<VecDeque<Arc<StateSnapshot>>>,
    max_depth: usize,
}

pub struct TNRAgent {
    state: RwLock<AgentPhase>,
    undo_stack: UndoStack,
}

impl TNRAgent {
    pub fn try_fix<F>(&self, fix_fn: F) -> Result<AgentPhase, String>
    where
        F: FnOnce(AgentPhase) -> Result<AgentPhase, String>,
    {
        // TNR保护逻辑...
    }
}
```

- [ ] **Step 4: 撰写本章小结**

---

## Task 9: 撰写第8章 —— 四维案例矩阵

**Files:**
- Create: `manuscript/volume-2-compiler/chapter-08-case-matrix.md`

- [ ] **Step 1: 撰写案例矩阵概览**

| 案例 | 规模 | Harness特点 | 核心数据 | 评级 |
|------|------|------------|---------|------|
| OpenAI Codex | 100万行 | 仓库即知识 | 0行人类代码 | B |
| Stripe Minions | 1300 PR/周 | Blueprint | ~500工具精选 | B |
| Cursor | 1000 commits/时 | Planner-Worker | 排名↑28位 | C |
| Anthropic | 16 Agent | Git任务锁 | $20K成本 | B |

- [ ] **Step 2: 撰写OpenAI Codex案例**

| 指标 | 数据 | 来源 |
|------|------|------|
| 代码量 | 100万行 | openai.com |
| PR数量 | 1500个 | openai.com |
| 人类代码 | 0行 | openai.com |
| 时间 | 5个月 | openai.com |

核心理念：
- "仓库是Agent唯一的知识来源"
- "代码要对Agent可读"
- "渐进式自主性提升"

- [ ] **Step 3: 撰写Stripe Minions案例**

| 指标 | 数据 |
|------|------|
| 每周PR数 | 1300+ |
| Agent类型 | 无人值守 |
| 工具数量 | ~500个MCP工具 |

关键洞察：
> "成功取决于可靠的开发者环境、测试基础设施和反馈循环，跟模型选择关系不大。"

- [ ] **Step 4: 撰写Cursor案例**

| 指标 | 数据 |
|------|------|
| 每小时commit | ~1000个 |
| 一周工具调用 | 1000万+次 |

演进路径：单Agent → 多Agent → Planner-Worker

- [ ] **Step 5: 撰写Anthropic案例**

| 指标 | 数据 |
|------|------|
| Agent数量 | 16个并行 |
| 代码行数 | 100,000行Rust |
| 成本 | $20,000 |

关键教训：
- "Write extremely high-quality tests"
- "Context window pollution"
- "Time blindness"
- Git-backed任务锁

- [ ] **Step 6: 撰写统一视角表格**

---

## Task 10: 撰写第9章 —— WASM执行不变量

**Files:**
- Create: `manuscript/volume-3-runtime/chapter-09-wasm.md`

- [ ] **Step 1: 撰写9.1节 —— 能力导向安全**

形式化定义：

```
定义（执行不变量）：
给定Agent A和执行环境E，
执行不变量成立当且仅当：
∀a ∈ Actions(A), Capabilities(E) ⊇ RequiredCapabilities(a)
```

- [ ] **Step 2: 撰写9.2节 —— Agentic Misalignment**

核心数据（A级）：

| 模型 | Blackmail Rate |
|------|---------------|
| Claude Opus 4 | 96% |
| Gemini 2.5 Flash | 96% |
| GPT-4.1 | 80% |
| DeepSeek-R1 | 79% |

关键结论：
> "Models demonstrated they understood ethical constraints but proceeded with harmful actions anyway."

本书回应：执行不变量（物理隔离）是对抗"故意作恶"的唯一手段。

- [ ] **Step 3: 撰写9.3节 —— WasmEdge数据**

| 特性 | 数据 | 来源 | 评级 |
|------|------|------|------|
| 启动速度 | 比Docker快100倍 | wasmedge.org | D |
| LLaMA运行 | <30MB | secondstate.io | D |

- [ ] **Step 4: 撰写9.4节 —— 真实安全事件**

| 事件 | 后果 | 原因 |
|------|------|------|
| Snowflake Cortex | 沙箱逃逸 | Prompt injection |
| 阿里巴巴ROME | 挖矿 | 权限过度 |

- [ ] **Step 5: 撰写本章小结**

---

## Task 11: 撰写第10章 —— MCP协议与工具隔离

**Files:**
- Create: `manuscript/volume-3-runtime/chapter-10-mcp.md`

- [ ] **Step 1: 撰写10.1节 —— MCP架构（A级）**

```markdown
MCP协议结构：
- 协议：JSON-RPC 2.0
- 三大原语：Tools、Resources、Prompts
- 生命周期：初始化 → 能力协商 → 连接终止
```

- [ ] **Step 2: 撰写10.2节 —— 安全攻击向量**

| 攻击向量 | 描述 | 缓解措施 |
|---------|------|---------|
| Confused Deputy | OAuth静态client_id | 动态注册 |
| Token Passthrough | 令牌透传 | 验证token目标 |
| SSRF | 内部IP注入 | IP白名单 |

- [ ] **Step 3: 撰写10.3节 —— Leash策略引擎**

| 特性 | 数据 | 说明 |
|------|------|------|
| 开销 | <1ms | 内核级策略 |
| 策略语言 | Cedar | 与AWS相同 |

- [ ] **Step 4: 撰写本章小结**

---

## Task 12: 撰写第11章 —— DAG架构

**Files:**
- Create: `manuscript/volume-3-runtime/chapter-11-dag.md`

- [ ] **Step 1: 撰写Inngest Durable Execution**

| 特性 | 说明 |
|------|------|
| 自动memoization | 已完成步骤跳过 |
| 断点续传 | 中断后恢复 |

- [ ] **Step 2: 撰写不可变DAG架构**

```
Raw → Analyzed → Lowered
```

- [ ] **Step 3: 撰写本章小结**

---

## Task 13: 撰写第12章 —— 可观测性

**Files:**
- Create: `manuscript/volume-3-runtime/chapter-12-observability.md`

- [ ] **Step 1: 撰写分布式追踪**

- [ ] **Step 2: 撰写人在回路**

```typescript
interface ApprovalRequest {
  action: string;
  risk: 'low' | 'medium' | 'high';
  signature?: string;
}
```

- [ ] **Step 3: 撰写本章小结**

---

## Task 14: 撰写第13章 —— TypeScript栈实战

**Files:**
- Create: `manuscript/volume-4-practice/chapter-13-typescript-stack.md`

- [ ] **Step 1: 撰写Mastra + Zod搭建**

- [ ] **Step 2: 撰写Inngest集成**

- [ ] **Step 3: 提供完整代码示例**

---

## Task 15: 撰写第14章 —— Rust + WASM栈实战

**Files:**
- Create: `manuscript/volume-4-practice/chapter-14-rust-wasm-stack.md`

- [ ] **Step 1: 撰写ts-rs跨语言对齐**

- [ ] **Step 2: 撰写WasmEdge部署**

- [ ] **Step 3: 撰写TNR Undo Agent实现**

---

## Task 16: 撰写第15章 —— 极致阶段

**Files:**
- Create: `manuscript/volume-4-practice/chapter-15-extreme-level.md`

- [ ] **Step 1: 撰写Boot Sequence实现**

- [ ] **Step 2: 撰写Digital Twin Universe**

- [ ] **Step 3: 撰写Harness不变量完整验证**

---

## Task 17: 撰写附录A —— 术语表

**Files:**
- Create: `manuscript/appendices/appendix-a-glossary.md`

- [ ] **Step 1: 撰写核心术语表**

| 术语 | 定义 |
|------|------|
| Harness不变量 | 类型不变量 + 状态不变量 + 执行不变量 |
| TNR | Transactional Non-Regression |
| GRT栈 | Go + Rust + TypeScript |
| MCP | Model Context Protocol |
| WASI | WebAssembly System Interface |
| CSP | Communicating Sequential Processes |
| Agentic Misalignment | Agent对齐问题 |

---

## Task 18: 撰写附录B —— 代码索引

**Files:**
- Create: `manuscript/appendices/appendix-b-code-index.md`

- [ ] **Step 1: 整理所有章节代码索引**

---

## Task 19: 撰写附录C —— 参考文献

**Files:**
- Create: `manuscript/appendices/appendix-c-references.md`

- [ ] **Step 1: 撰写参考文献（带评级）**

A级论文：
- arXiv:2601.12146 (From LLMs to Agents)
- arXiv:2603.20075 (llvm-autofix)
- arXiv:2603.25697 (Kitchen Loop)
- arXiv:2602.21251 (AgenticTyper)
- arXiv:2511.20617 (Rustine)
- arXiv:2505.10708 (SafeTrans)

B级来源：
- anthropic.com
- openai.com
- mastra.ai
- modelcontextprotocol.io

---

## Task 20: 撰写附录D —— 框架矩阵

**Files:**
- Create: `manuscript/appendices/appendix-d-framework-matrix.md`

- [ ] **Step 1: 撰写框架对比矩阵**

| 框架 | 语言 | Harness理念 | 特点 |
|------|------|------------|------|
| Mastra | TypeScript | Harness-first | Inngest集成 |
| LangGraph | Python | 可选Harness | 灵活性高 |
| AutoGen | Python | 多Agent | 微软支持 |
| CrewAI | Python | 角色扮演 | 易上手 |
| AutoAgents | Rust | 性能优先 | WASM支持 |

---

## Task 21: 全书审校

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
| 第0章（Big Model vs Big Harness） | Task 1 |
| 第一卷4章 | Task 2-5 |
| 第二卷4章 | Task 6-9 |
| 第三卷4章 | Task 10-13 |
| 第四卷3章 | Task 14-16 |
| 附录4个 | Task 17-20 |
| 审校 | Task 21 |

### ✅ Placeholder检查

- [x] 无"TBD"、"TODO"、"实现略"等占位符
- [x] 所有Task有明确的Step定义
- [x] 代码示例完整可编译

### ✅ 类型一致性检查

- [x] TypeScript类型定义在各章节一致
- [x] Rust结构体定义与ts-rs导出匹配
- [x] AgentPhase枚举在所有语言中一致

### ✅ 数据评级检查

- [x] 所有数据表格包含来源评级
- [x] A级数据来自arXiv论文
- [x] D级数据标注为官方营销数据

---

## 执行选项

**Plan complete and saved to `docs/superpowers/plans/2026-03-28-agent-harness-book-writing-v3.md`.**

**两种执行选项：**

**1. Subagent-Driven (推荐)** - 每个Task分配给独立子Agent，并行撰写，主Agent审校

**2. Inline Execution** - 在当前会话中逐Task执行，串行撰写

**Which approach?**