# 第3章：Rust —— 核心层类型不变量与状态不变量

## 3.1 所有权系统：编译时类型不变量的证明

Rust的所有权系统将类型不变量升级为**编译时可证明的内存安全**。

### Rust所有权系统图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Rust所有权系统：编译时内存安全证明                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   1. 所有权 (Ownership)                                                    │
│   ┌─────────────────────────────────────────────────────────────────────┐ │
│   │                                                                      │ │
│   │   let x = String::from("hello");                                   │ │
│   │   let y = x;                      // x 被移动(move)到y              │ │
│   │   // println!("{}", x);           // 编译错误！x已无效              │ │
│   │                                                                      │ │
│   │   ∀x, ∃!owner: Owns(owner, x)    // 同一时刻只有一个所有者         │ │
│   │                                                                      │ │
│   └─────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│   2. 借用 (Borrowing)                                                     │
│   ┌─────────────────────────────────────────────────────────────────────┐ │
│   │                                                                      │ │
│   │   let mut v = vec![1, 2, 3];                                      │ │
│   │   let first = &v[0];             // 不可变借用                      │ │
│   │   v.push(4);                    // 编译错误！                      │ │
│   │   // cannot borrow `v` as mutable because it is borrowed as immutable │ │
│   │                                                                      │ │
│   │   borrows(x) ⊆ ownership(x)        // 借用不能超过所有权范围        │ │
│   │                                                                      │ │
│   └─────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│   3. 生命周期 (Lifetime)                                                   │
│   ┌─────────────────────────────────────────────────────────────────────┐ │
│   │                                                                      │ │
│   │   fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {            │ │
│   │       if x.len() > y.len() { x } else { y }                      │ │
│   │   }                                                                 │ │
│   │                                                                      │ │
│   │   ∀x, lifetime(x) ⊆ scope(owner(x))  // 引用不能超过所有者生命周期 │ │
│   │                                                                      │ │
│   └─────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│   ─────────────────────────────────────────────────────────────────────   │
│   核心洞察：Rust编译器在编译时证明内存安全，无需GC运行时开销                │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Rust状态机状态转移图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Rust状态机状态转移图                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                       ┌──────────────┐                                     │
│                       │ Initializing │                                     │
│                       └──────┬───────┘                                     │
│                              │                                              │
│                              ▼                                              │
│                       ┌──────────────┐                                     │
│                       │   Planning   │─────────────────┐                   │
│                       └──────┬───────┘                   │                   │
│                              │                            │                   │
│              ┌───────────────┼───────────────┐          │                   │
│              ▼               │               ▼          │                   │
│       ┌──────────────┐       │        ┌──────────────┐  │                   │
│       │   Failed     │       │        │  Executing   │──┘                   │
│       └──────────────┘       │        └──────┬───────┘                     │
│                              │               │                              │
│                              │               ▼                              │
│                              │        ┌──────────────┐                      │
│                              │        │   Reviewing  │                      │
│                              │        └──────┬───────┘                      │
│                              │               │                              │
│                              │     ┌─────────┴─────────┐                    │
│                              │     ▼                   ▼                    │
│                              │ ┌──────────┐      ┌──────────┐             │
│                              │ │ Completed│      │   Failed  │             │
│                              │ └──────────┘      └──────────┘             │
│                              │                                              │
│   有效转移:                                                               │
│   Initializing → Planning                                                  │
│   Planning → Executing | Failed                                           │
│   Executing → Reviewing | Failed                                          │
│   Reviewing → Completed | Failed                                          │
│                                                                             │
│   Rust编译器确保：所有转移都经过valid_transition()验证                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 理论基础

| 概念 | 形式化定义 | Harness意义 |
|------|-----------|-------------|
| 所有权 | ∀x, ∃!owner: Owns(owner, x) | 确定性资源归属 |
| 借用 | ∀x, borrows(x) ⊆ ownership(x) | 安全的共享访问 |
| 生命周期 | ∀x, lifetime(x) ⊆ scope(owner(x)) | 编译时资源管理 |

### 数据支撑

| 指标 | 说明 | 来源 | 评级 |
|------|------|------|------|
| 内存安全 | 编译时保证，无GC | doc.rust-lang.org | **B** |
| 并发安全 | 无数据竞争 | Rustonomicon | **B** |

### 为什么AI无法绕过

```rust
// AI生成的不安全代码会被编译器拒绝
fn unsafe_code() {
    let mut v = vec![1, 2, 3];
    let first = &v[0];      // 不可变借用
    v.push(4);              // 可变借用 → 编译错误！
    // error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
}
```

编译器在编译时就能检测到这种违反所有权规则的代码，并拒绝编译。这种静态分析能力使得Rust能够在不牺牲性能的情况下提供内存安全保证。

## 学术对话：Rustine/SafeTrans

| 论文 | 数据 | 本书籍回应 | 评级 |
|------|------|----------|------|
| Rustine (arXiv:2511.20617) | 23个C程序，87%函数等价性 | 验证了Rust作为核心层的可行性 | A |
| SafeTrans (arXiv:2505.10708) | 翻译成功率54%→80%（GPT-4o + 迭代修复） | 验证了编译器驱动修复的有效性 | A |

Rustine论文展示了将C程序自动转换为Rust的可行性，达到了87%的函数等价性，证明了Rust可以作为系统编程的核心层语言。SafeTrans研究则表明，通过编译器反馈驱动的迭代修复过程，AI辅助的代码翻译成功率可以从54%提升到80%，这验证了Rust编译器在指导代码正确性方面的强大能力。

## 3.2 ts-rs：跨语言类型不变量的统一

> 问题：GRT栈中，如何保证TypeScript和Rust的类型定义一致？

### 解决方案：ts-rs实现Single Source of Truth

```rust
use serde::Serialize;
use ts_rs::TS;

// Rust中的类型定义 = 唯一真实来源
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

#[derive(Serialize, TS, Debug, Clone)]
#[ts(export, export_to = "bindings/")]
pub struct ToolCall {
    pub name: String,
    pub arguments: serde_json::Value,
}
```

自动生成的TypeScript类型：

```typescript
// bindings/AgentState.ts（自动生成）
export interface AgentState {
  phase: AgentPhase;
  tools: Array<ToolCall>;
  result: string | null;
}

export enum AgentPhase {
  Initializing = "Initializing",
  Planning = "Planning",
  Executing = "Executing",
  Reviewing = "Reviewing",
  Completed = "Completed",
  Failed = "Failed",
}
```

通过ts-rs库，我们实现了真正的单一数据源（Single Source of Truth）。Rust中的类型定义是唯一的权威来源，TypeScript类型完全由Rust代码生成，确保了跨语言类型的一致性。任何对Rust类型的修改都会自动反映到TypeScript端，消除了手动同步带来的错误风险。

## 3.3 状态机驱动的Agent Phase

> 维护状态不变量：状态转移必须满足前置/后置条件

```rust
use std::collections::VecDeque;

/// 状态不变量：Agent只能在合法状态之间转移
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AgentPhase {
    Initializing,
    Planning,
    Executing,
    Reviewing,
    Completed,
    Failed,
}

/// 状态转移错误
#[derive(Debug)]
pub enum TransitionError {
    InvalidTransition { from: AgentPhase, to: AgentPhase },
}

/// 状态不变量验证
fn valid_transition(from: AgentPhase, to: AgentPhase) -> bool {
    match (from, to) {
        (AgentPhase::Initializing, AgentPhase::Planning) => true,
        (AgentPhase::Planning, AgentPhase::Executing) => true,
        (AgentPhase::Executing, AgentPhase::Reviewing) => true,
        (AgentPhase::Reviewing, AgentPhase::Completed) => true,
        (AgentPhase::Reviewing, AgentPhase::Failed) => true,
        (AgentPhase::Executing, AgentPhase::Failed) => true,
        (AgentPhase::Planning, AgentPhase::Failed) => true,
        _ => false,
    }
}

/// Agent状态机
pub struct AgentStateMachine {
    current: AgentPhase,
    history: VecDeque<AgentPhase>,  // 用于TNR回滚
}

impl AgentStateMachine {
    pub fn new() -> Self {
        Self {
            current: AgentPhase::Initializing,
            history: VecDeque::with_capacity(16),
        }
    }

    /// 状态转移：维护状态不变量
    pub fn transition(&mut self, next: AgentPhase) -> Result<(), TransitionError> {
        if !valid_transition(self.current, next) {
            return Err(TransitionError::InvalidTransition {
                from: self.current,
                to: next,
            });
        }

        // 记录历史（用于TNR）
        self.history.push_back(self.current);
        if self.history.len() > 16 {
            self.history.pop_front();
        }

        self.current = next;
        Ok(())
    }

    /// 回滚到上一状态（TNR机制）
    pub fn rollback(&mut self) -> Option<AgentPhase> {
        self.history.pop_back().map(|prev| {
            self.current = prev;
            prev
        })
    }
}
```

这个状态机实现确保了Agent只能在预定义的合法状态之间转移。任何非法的状态转移都会被编译时类型系统捕获，并在运行时返回错误。同时，状态机维护了状态转移的历史记录，支持TNR（Try-N-Rollback）机制，允许在执行失败时回滚到之前的状态。

## 本章小结

1. Rust所有权系统在编译时证明类型不变量
2. ts-rs实现Rust→TypeScript的跨语言类型统一
3. 状态机驱动的Agent Phase维护状态不变量
4. 学术数据支撑：Rustine 87%等价性，SafeTrans 54%→80%成功率