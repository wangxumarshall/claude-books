# 《Agent Harness：编程语言、编译器与运行时》写作计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan chapter-by-chapter.

**Goal:** 撰写一本30-40章的专著，主题为"Agent Harness：编程语言、编译器与运行时"，覆盖GRT+WASM技术栈、编译器反馈回路、TNR事务性无回归、WASM零信任沙箱等核心内容。

**Architecture:** 按五大章节群组织（范式转移 → 语言契约 → 编译器审查 → 运行时隔离 → 实战落地），每章三层结构（五分钟摘要 + 实践代码 + 进阶理论），核心概念螺旋上升反复强化。

**Tech Stack:** TypeScript / Rust / Go / WebAssembly / Mastra / WasmEdge / Zod / TypeChat / cargo-component

---

## 文件结构

```
chapters/
├── part1-paradigm-shift/
│   ├── ch01-2026-reality.md         # 范式转移：Harness是底盘
│   ├── ch02-grt-wasm-blueprint.md   # GRT+WASM三层牢笼概述
│   └── ch03-car-framework.md         # CAR框架学术溯源
├── part2-language-contract/
│   ├── ch04-ts-defense.md           # TypeScript数据面防线
│   ├── ch05-ts-practice.md          # Mastra + Zod深度实践
│   ├── ch06-rust-core.md            # Rust核心面：所有权与生命周期
│   ├── ch07-rust-typestate.md       # Rust类型状态模式
│   ├── ch08-go-controlplane.md      # Go控制平面
│   ├── ch09-crosslang-types.md      # 跨语言类型对齐
│   └── ch10-comparison.md           # 反面vs正面教材对比
├── part3-compiler-review/
│   ├── ch11-compiler-judge.md        # 编译器即判别器
│   ├── ch12-feedback-loop.md         # 编译器反馈回路
│   ├── ch13-tnr-formal.md           # TNR形式化定义
│   ├── ch14-self-healing.md         # 自愈循环
│   ├── ch15-deadloop-rollback.md     # 死循环检测与回滚
│   └── ch16-gan-view.md             # GAN视角
├── part4-runtime-isolation/
│   ├── ch17-wasm-prison.md          # WebAssembly数字监狱
│   ├── ch18-wasi-capability.md       # WASI能力安全
│   ├── ch19-v8-isolates.md          # V8 Isolates实战数据
│   ├── ch20-mcp-sandboxscan.md       # MCP沙箱扫描
│   ├── ch21-immutable-dag.md        # Immutable DAG
│   ├── ch22-rag-mcp.md              # RAG-MCP工具检索
│   └── ch23-observability.md         # 全链路观测
├── part5-production/
│   ├── ch24-ts-start.md             # TypeScript起步
│   ├── ch25-rust-wasm-advanced.md   # Rust+WASM进阶
│   ├── ch26-anthropic-bootseq.md   # Anthropic引导序列
│   ├── ch27-strongdm-darkfactory.md # StrongDM黑灯工厂
│   └── ch28-multi-agent.md          # 多Agent协作
└── appendices/
    ├── app-a-car-theory.md          # CAR ↔ 离散事件仿真
    ├── app-b-tnr-stm.md             # TNR ↔ 软件事务内存
    ├── app-c-typestate.md           # 类型状态 ↔ 状态机
    ├── app-d-capability-formal.md    # Capability ↔ 形式化安全
    └── app-e-wasm-linear.md          # WASM ↔ 线性类型
```

---

## 写作任务总览

| 阶段 | 任务数 | 说明 |
|------|--------|------|
| 第一部分 | 3章 | 范式转移 |
| 第二部分 | 7章 | 语言层契约 |
| 第三部分 | 6章 | 编译器层审查 |
| 第四部分 | 7章 | 运行时层隔离 |
| 第五部分 | 5章 | 实战落地 |
| 附录 | 5篇 | 理论深潜 |

---

## 第一部分：范式转移

### Task 1: 第1章 — 2026软件工程真相：模型是引擎，Harness是底盘

**文件:** `chapters/part1-paradigm-shift/ch01-2026-reality.md`

- [ ] **Step 1: 互联网调研** — 调研Anthropic 16 Agent实验最新进展、LangChain/LangGraph局限性案例
- [ ] **Step 2: 撰写五分钟摘要** — 一段话 + 一张CAR架构图讲清楚核心结论
- [ ] **Step 3: 撰写大模型工程原罪章节** — 幻觉、上下文膨胀、状态丢失的机制分析
- [ ] **Step 4: 撰写LangChain局限性分析** — 具体代码案例说明为什么是过渡玩具
- [ ] **Step 5: 撰写CAR框架定义** — Control/Agency/Runtime三层职责划分
- [ ] **Step 6: 撰写Anthropic案例** — 16 Agent × 10万行Rust C编译器深度拆解
- [ ] **Step 7: 撰写进阶理论注记** — Harness作为闭环反馈系统的控制论视角

### Task 2: 第2章 — 终极软件栈蓝图：GRT + WASM

**文件:** `chapters/part1-paradigm-shift/ch02-grt-wasm-blueprint.md`

- [ ] **Step 1: 互联网调研** — 调研2026年Python在AI基础设施中的实际使用情况、GRT栈最新生态
- [ ] **Step 2: 撰写Python退场分析** — 内存开销、动态类型、生产环境局限的具体数据
- [ ] **Step 3: 撰写三层牢笼概述** — 语言契约 → 编译器审查 → WASM隔离的架构图与代码示例
- [ ] **Step 4: 撰写GRT职责划分** — Go/Rust/TypeScript各层职责与交互模式

### Task 3: 第3章 — CAR框架学术溯源

**文件:** `chapters/part1-paradigm-shift/ch03-car-framework.md`

- [ ] **Step 1: 互联网调研** — 调研离散事件仿真理论在软件工程中的应用、Control Theory与AI系统结合的最新论文
- [ ] **Step 2: 撰写CAR学术定义** — 形式化描述Control/Agency/Runtime的数学边界
- [ ] **Step 3: 撰写工程映射** — CAR三层的软件架构对应关系
- [ ] **Step 4: 撰写控制论视角** — Harness作为闭环反馈系统的推导

---

## 第二部分：语言层 — 契约

### Task 4: 第4章 — TypeScript数据面防线

**文件:** `chapters/part2-language-contract/ch04-ts-defense.md`

- [ ] **Step 1: 互联网调研** — Zod/TypeChat/Mastra最新版本API、GitHub Stars趋势
- [ ] **Step 2: 撰写Branded Types实战** — 具体代码：品牌类型如何终结字符串级联编程
- [ ] **Step 3: 撰写Zod Schema完整示例** — `zod.infer<typeof AgentState>`的完整类型推导代码
- [ ] **Step 4: 撰写Tool Call路由** — Vercel AI SDK类型安全管道代码
- [ ] **Step 5: 撰写反面教材对比** — 2023长Prompt依赖 vs 2026类型约束的效果对比表

### Task 5: 第5章 — Mastra + Zod深度实践

**文件:** `chapters/part2-language-contract/ch05-ts-practice.md`

- [ ] **Step 1: 互联网调研** — Mastra最新功能、Inngest集成方式、Replit Agent 3案例细节
- [ ] **Step 2: 撰写Mastra工作流代码** — 完整的Agent工作流编排代码示例
- [ ] **Step 3: 撰写状态持久化实践** — Inngest断点续传的具体实现
- [ ] **Step 4: 撰写元Agent模式** — 动态工具加载与组合的代码

### Task 6: 第6章 — Rust核心面：所有权与生命周期

**文件:** `chapters/part2-language-contract/ch06-rust-core.md`

- [ ] **Step 1: 互联网调研** — Odyssey SDK最新进展、AutoAgents框架现状、Tokio 2026版新特性
- [ ] **Step 2: 撰写所有权实战代码** — AI无法"悄悄遗忘"Token的具体代码演示
- [ ] **Step 3: 撰写Odyssey Bundle架构** — Agent定义+工具+沙箱策略打包的完整代码
- [ ] **Step 4: 撰写Tokio异步调度** — 海量微Agent并发协作的内存印迹对比表

### Task 7: 第7章 — Rust类型状态模式

**文件:** `chapters/part2-language-contract/ch07-rust-typestate.md`

- [ ] **Step 1: 互联网调研** — Rust类型状态模式的最新最佳实践、相关RFC进展
- [ ] **Step 2: 撰写`enum AgentPhase`完整代码** — 状态跃迁合法性的编译器强制
- [ ] **Step 3: 撰写Result<T, HarnessError>** — `?`操作符与强迫性兜底路径的代码
- [ ] **Step 4: 撰写错误即控制流** — 完整的错误处理流图与代码

### Task 8: 第8章 — Go控制平面

**文件:** `chapters/part2-language-contract/ch08-go-controlplane.md`

- [ ] **Step 1: 互联网调研** — 2026年Go在AI基础设施中的最新应用案例、API Gateway模式
- [ ] **Step 2: 撰写Goroutine调度代码** — Agent路由与长时队列的完整Go代码
- [ ] **Step 3: 撰写API Gateway模式** — 高并发×低延迟的具体实现
- [ ] **Step 4: 撰写Go生态位分析** — 为什么Go不在Agent逻辑而在控制平面

### Task 9: 第9章 — 跨语言类型对齐

**文件:** `chapters/part2-language-contract/ch09-crosslang-types.md`

- [ ] **Step 1: 互联网调研** — ts-rs/specta/Protobuf最新版本、跨语言类型对齐2026年最佳实践
- [ ] **Step 2: 撰写ts-rs实战代码** — Rust结构体自动生成TypeScript接口的完整演示
- [ ] **Step 3: 撰写Result映射** — Rust Result/Option → TS联合类型/条件类型的映射代码
- [ ] **Step 4: 撰写GRT单点真实来源实践** — 三语言栈类型一致性的完整代码示例

### Task 10: 第10章 — 反面vs正面教材对比

**文件:** `chapters/part2-language-contract/ch10-comparison.md`

- [ ] **Step 1: 互联网调研** — 收集2023-2024年AI代码生成的失败案例与2026年成功案例的具体数据
- [ ] **Step 2: 撰写对比表格** — 每个核心概念的双栏对比（反面vs正面）
- [ ] **Step 3: 撰写量化分析** — 94%错误率、43%成功率提升等数据的来源与推导

---

## 第三部分：编译器层 — 审查

### Task 11: 第11章 — 编译器即判别器

**文件:** `chapters/part3-compiler-review/ch11-compiler-judge.md`

- [ ] **Step 1: 互联网调研** — 94% AI代码错误是类型错误的数据来源、TSC/SWC最新性能数据
- [ ] **Step 2: 撰写tsc拦截流代码** — `tsc --noEmit`秒级阻断的完整演示
- [ ] **Step 3: 撰写Cargo验证流** — Rust编译通过≈内存安全正确性的理论依据
- [ ] **Step 4: 撰写JSON特征列表** — 结构化错误输出的完整代码

### Task 12: 第12章 — 编译器反馈回路

**文件:** `chapters/part3-compiler-review/ch12-feedback-loop.md`

- [ ] **Step 1: 互联网调研** — Anthropic 16 Agent项目编译器回路的更多技术细节
- [ ] **Step 2: 撰写反馈回路架构图** — 生成→校验→反思→回滚的完整流程图
- [ ] **Step 3: 撰写JSON特征列表代码** — 编译器输出 → 结构化特征的完整处理代码
- [ ] **Step 4: 撰写AI解析准确性分析** — JSON vs Markdown解析对比数据

### Task 13: 第13章 — TNR形式化定义

**文件:** `chapters/part3-compiler-review/ch13-tnr-formal.md`

- [ ] **Step 1: 互联网调研** — STRATUS系统、TNR理论、软件事务内存的最新研究进展
- [ ] **Step 2: 撰写TNR形式化定义** — Precondition × Postcondition × Invariant的数学描述
- [ ] **Step 3: 撰写编译器层TNR实现** — 编译单元原子性回滚的具体实现
- [ ] **Step 4: 撰写形式化安全证明** — TNR保证的数学推导

### Task 14: 第14章 — 自愈循环

**文件:** `chapters/part3-compiler-review/ch14-self-healing.md`

- [ ] **Step 1: 互联网调研** — Critique Agent/Generator Agent的最新实现案例、多轮对抗架构
- [ ] **Step 2: 撰写PID控制器模型** — 编译器Error Log作为反馈信号的数学建模
- [ ] **Step 3: 撰写Critique ↔ Generator代码** — 微秒级对抗的完整实现
- [ ] **Step 4: 撰写指数退避实现** — 状态快照与重试策略代码

### Task 15: 第15章 — 死循环检测与回滚

**文件:** `chapters/part3-compiler-review/ch15-deadloop-rollback.md`

- [ ] **Step 1: 互联网调研** — Git-based断点救援的最新实践、状态回滚机制
- [ ] **Step 2: 撰写死循环检测算法** — 同一编译错误循环的检测代码
- [ ] **Step 3: 撰写Git Commit断点救援** — 回滚至上个通过节点的完整代码
- [ ] **Step 4: 撰写人类介入触发条件** — 强制人工审核的判定逻辑

### Task 16: 第16章 — GAN视角

**文件:** `chapters/part3-compiler-review/ch16-gan-view.md`

- [ ] **Step 1: 撰写生成器vs判别器模型** — LLM作为生成器、Compiler作为判别器的形式化描述
- [ ] **Step 2: 撰写类型系统作为损失函数** — 类型检查结果作为判别反馈的数学建模
- [ ] **Step 3: 撰写对抗训练启发** — 从GAN借鉴到编译器反馈回路的设计模式

---

## 第四部分：运行时层 — 隔离

### Task 17: 第17章 — WebAssembly数字监狱

**文件:** `chapters/part4-runtime-isolation/ch17-wasm-prison.md`

- [ ] **Step 1: 互联网调研** — Wasmtime/WasmEdge最新性能数据、Docker冷启动对比数据
- [ ] **Step 2: 撰写Docker失败论** — 冷启动慢、内核面广的具体数据对比表
- [ ] **Step 3: 撰写WASM隔离代码** — 30MB运行时 vs 4GB Python的具体演示
- [ ] **Step 4: 撰写指令级隔离原理** — WASM沙箱机制的技术分析

### Task 18: 第18章 — WASI能力安全

**文件:** `chapters/part4-runtime-isolation/ch18-wasi-capability.md`

- [ ] **Step 1: 互联网调研** — Capability-based Security最新进展、WASI权限声明规范
- [ ] **Step 2: 撰写能力导向执行代码** — 文件/Socket显式授予的完整WASI示例
- [ ] **Step 3: 撰写TNR运行时实现** — WASI能力撤销作为回滚原语的具体代码
- [ ] **Step 4: 撰写安全证明** — 消灭AI删库跑路的物理可能性分析

### Task 19: 第19章 — V8 Isolates实战数据

**文件:** `chapters/part4-runtime-isolation/ch19-v8-isolates.md`

- [ ] **Step 1: 互联网调研** — Cloudflare Dynamic Workers最新数据、V8 Isolates性能benchmark
- [ ] **Step 2: 撰写毫秒级冷启动数据** — 具体毫秒数、内存占用数字、对比数据
- [ ] **Step 3: 撰写GPU穿透代码** — GGML + Llama本地推理的完整示例
- [ ] **Step 4: 撰写WasmEdge集成** — 与WASI的完整集成代码

### Task 20: 第20章 — MCP-SandboxScan

**文件:** `chapters/part4-runtime-isolation/ch20-mcp-sandboxscan.md`

- [ ] **Step 1: 互联网调研** — MCP协议最新进展、SandboxScan相关研究
- [ ] **Step 2: 撰写MCP隔离架构** — 不受信MCP工具的WASM隔离方案
- [ ] **Step 3: 撰写网络阻断代码** — 毫秒级冷启动×网络零连通的完整演示
- [ ] **Step 4: 撰写提示词注入拦截** — 具体拦截机制与代码

### Task 21: 第21章 — Immutable DAG

**文件:** `chapters/part4-runtime-isolation/ch21-immutable-dag.md`

- [ ] **Step 1: 互联网调研** — Nika-core架构、Immutable DAG最新实现、BLAKE3/zstd压缩性能数据
- [ ] **Step 2: 撰写AST三阶段代码** — Raw/Analyzed/Lowered的完整处理流程
- [ ] **Step 3: 撰写DAG验证代码** — 错误码体系（140-151/080-089）的具体实现
- [ ] **Step 4: 撰写内容寻址存储** — BLAKE3哈希 + zstd的完整代码

### Task 22: 第22章 — RAG-MCP工具检索

**文件:** `chapters/part4-runtime-isolation/ch22-rag-mcp.md`

- [ ] **Step 1: 互联网调研** — RAG-MCP最新实现、向量数据库工具检索性能数据、13%→43%成功率来源
- [ ] **Step 2: 撰写向量检索架构** — 向量数据库 × 工具语义检索的完整代码
- [ ] **Step 3: 撰写动态Schema挂载** — 语义检索动态挂载Tool Schema的完整演示
- [ ] **Step 4: 撰写Prompt膨胀解决方案** — 解决LLM选择瘫痪的具体机制

### Task 23: 第23章 — 全链路观测

**文件:** `chapters/part4-runtime-isolation/ch23-observability.md`

- [ ] **Step 1: 互联网调研** — OpenTelemetry 2026年新特性、LangSmith最新功能
- [ ] **Step 2: 撰写确定性重放架构** — 100% Deterministic Replay的完整实现
- [ ] **Step 3: 撰写不可变日志代码** — Immutable DAG追踪的具体代码
- [ ] **Step 4: 撰写故障根因分析** — 毫秒级根因分析的完整流程

---

## 第五部分：实战落地

### Task 24: 第24章 — TypeScript起步

**文件:** `chapters/part5-production/ch24-ts-start.md`

- [ ] **Step 1: 互联网调研** — Mastra最新安装方式、TypeChat API变化
- [ ] **Step 2: 撰写完整项目代码** — Mastra + Zod + TypeChat强类型守卫的完整可运行代码
- [ ] **Step 3: 撰写AgentOutput结构体** — 代码 + 测试的完整定义
- [ ] **Step 4: 撰写消除JSON解析错误** — 具体错误类型与防御代码

### Task 25: 第25章 — Rust+WASM进阶

**文件:** `chapters/part5-production/ch25-rust-wasm-advanced.md`

- [ ] **Step 1: 互联网调研** — cargo-component最新用法、WasmEdge最新API
- [ ] **Step 2: 撰写cargo-component代码** — Rust核心逻辑编译为.wasm的完整步骤
- [ ] **Step 3: 撰写WasmEdge部署** — 零信任环境长周期任务的完整代码
- [ ] **Step 4: 撰写Inngest集成** — 断点续传的完整实现

### Task 26: 第26章 — Anthropic引导序列

**文件:** `chapters/part5-production/ch26-anthropic-bootseq.md`

- [ ] **Step 1: 互联网调研** — Anthropic 16 Agent项目的更多技术细节、Git Commit工作流
- [ ] **Step 2: 撰写Boot Sequence完整流程** — Initializer → RAG-MCP → JSON List → 执行
- [ ] **Step 3: 撰写Undo Agent触发** — 失败检测与触发条件的完整代码
- [ ] **Step 4: 撰写Smoke Test** — 自愈循环的完整测试代码

### Task 27: 第27章 — StrongDM黑灯工厂

**文件:** `chapters/part5-production/ch27-strongdm-darkfactory.md`

- [ ] **Step 1: 互联网调研** — StrongDM黑灯工厂最新公开信息、Leash策略引擎细节
- [ ] **Step 2: 撰写场景验证架构** — Holdout Sets的具体实现
- [ ] **Step 3: 撰写数字孪生宇宙** — Okta/Slack高保真模拟的完整代码
- [ ] **Step 4: 撰写Leash零信任** — 动态身份×微隔离的完整实现

### Task 28: 第28章 — 多Agent协作

**文件:** `chapters/part5-production/ch28-multi-agent.md`

- [ ] **Step 1: 互联网调研** — 2026年多Agent协作框架最新进展
- [ ] **Step 2: 撰写Agent联邦架构** — 从单一Agent到多Agent的网络拓扑图
- [ ] **Step 3: 撰写GRT并发模型** — Goroutine × Tokio的完整对比代码
- [ ] **Step 4: 撰写任务分发机制** — 多Agent任务分配的完整实现

---

## 附录：理论深潜

### Task 29: 附录A-D

**文件:** `chapters/appendices/app-a-car-theory.md` 等

- [ ] **Step 1: 撰写CAR ↔ 离散事件仿真** — 理论映射与数学推导
- [ ] **Step 2: 撰写TNR ↔ STM** — 软件事务内存的理论关联
- [ ] **Step 3: 撰写类型状态 ↔ 状态机** — 可组合性的数学基础
- [ ] **Step 4: 撰写Capability ↔ 形式化安全** — Bell-LaPadula模型映射
- [ ] **Step 5: 撰写WASM ↔ 线性类型** — 线性类型理论的完整推导

---

## 章节写作顺序与依赖关系

```
第一部分（范式转移）→ 第二部分（语言契约）→ 第三部分（编译器审查）→ 第四部分（运行时隔离）→ 第五部分（实战落地）
     ↓                        ↓                       ↓                        ↓                      ↓
  Task 1-3                 Task 4-10              Task 11-16              Task 17-23             Task 24-28
     │                        │                       │                        │                      │
     └────────────────────────┴───────────────────────┴────────────────────────┴──────────────────────┘
                                              │
                                        Task 29 (附录)
                                        可与正文并行
```

**可并行写作的章节组：**
- 组A（语言层）：Task 4, 5, 6, 7, 8, 9, 10（相互独立，可并行）
- 组B（编译器层）：Task 11, 12, 13, 14, 15, 16（Task 13依赖Task 11-12的概念）
- 组C（运行时层）：Task 17, 18, 19, 20, 21, 22, 23（相互独立，可并行）

---

## 写作质量检查清单

- [ ] 每章至少1张核心架构图（ASCII或Mermaid）
- [ ] 每个核心概念配备至少1个完整可运行代码块
- [ ] 技术数据（%、毫秒、内存）有明确来源
- [ ] 禁止使用涌现、意识、魔法等过度拟人化词汇
- [ ] 每章有"五分钟摘要"开篇
- [ ] 核心章节末尾有"进阶理论注记"
- [ ] 正面教材vs反面教材对比贯穿全书

---

## 互联网调研成果（2026-03-27）

### Anthropic研究（来源：anthropic.com/research）

**多Agent与代码生成相关研究：**
- **Agentic Misalignment** (2025.06) — "How LLMs could be insider threats"（LLM内部威胁）
- **SHADE-Arena** (2025.06) — "Evaluating sabotage and monitoring in LLM agents"（智能体破坏与监控评估）
- **Measuring AI agent autonomy in practice** (2026.02) — AI自主性测量框架
- **Project Fetch** (2025.11) — "Can Claude train a robot dog?" — Claude编程四足机器狗，唯一完成全自主进度的团队
- **How AI is transforming work at Anthropic** — Claude Code如何根本性改变软件开发工作性质
- **Long-running Claude for scientific computing** — 多日科学计算任务运行指南
- **Project Vend Phase 1&2** — AI店主运行小店，探索AI在复杂现实任务中的表现
- **Prompt injection defenses** — 浏览器使用中提示词注入的风险缓解

**重要结论：**
> "AI use is radically changing the nature of work for software developers."
> "the AI-assisted team completed tasks faster and was the only group to make real progress toward full autonomy."

### WasmEdge（来源：wasmedge.org）

**核心数据：**
- 启动速度比Linux容器快**100倍**
- 运行时性能比原生慢约**20%**（可接受）
- 跨平台：Linux/macOS/Windows/RTOS/微内核，支持x86/ARM/M1
- CNCF官方Sandbox项目（10.5k stars）
- **LlamaEdge**：支持在WASM中运行Llama等LLM进行本地推理
- 支持Rust/C/C++/Swift/AssemblyScript/Kotlin/JavaScript

**与Docker对比：**
| 指标 | Docker | WasmEdge |
|------|--------|----------|
| 冷启动 | 秒级~分钟级 | 毫秒级（声称100x faster） |
| 内存占用 | GB级 | ~30MB级别 |
| 隔离级别 | 内核级 | 指令级 |

### Mastra框架（来源：GitHub mastra-ai/mastra）

**关键数据：**
- **22.4k stars**，1.8k forks
- 99.3% TypeScript，76 releases
- **40+ AI provider**统一接口
- 内置MCP Servers、Human-in-the-Loop、Context Management
- 生产工具：evaluation + observability内置
- 双License：Apache 2.0（核心）+ Enterprise License（ee/目录）

### Rust语言（来源：rust-lang.org）

- 当前版本：**1.94.1**
- 核心优势：无GC、无运行时、性能卓越
- 内存安全通过所有权模型在**编译时**保证
- 典型用例：CLI工具、WebAssembly、网络服务、嵌入式系统

### ts-rs（来源：GitHub astral-sh/ts-rs）

- 自动从Rust结构体生成TypeScript类型定义
- 支持泛型、Option、Result等高级类型映射
- 用于GRT栈跨语言类型对齐

### 待进一步调研的缺口

1. **Anthropic 16 Agent实验**：尚未找到10万行Rust C编译器的具体论文/博客
2. **StrongDM黑灯工厂**：相关博客返回404，需尝试其他URL
3. **STRATUS系统/TNR理论**：学术来源未确认，需进一步搜索
4. **MCP-SandboxScan**：2026年新协议，尚未找到官方文档
5. **94%类型错误数据**：来源未确认

### CDP浏览器使用说明

Chrome远程调试已配置，但CDP Proxy WebSocket连接存在兼容性问题。建议：
- 简单页面用**WebFetch**（已验证可用）
- 需交互的页面用**WebSearch**找官方文档
- 登录态内容待解决Proxy问题后使用CDP直接操作

---

## 互联网调研成果（第二轮 — 2026-03-27 补充）

### MCP协议安全规范（来源：modelcontextprotocol.io）

**MCP核心定义：**
- 类比"AI的USB-C接口"——标准化AI应用到外部系统的连接
- 支持Claude、ChatGPT、VS Code、Cursor等主流AI工具
- 支持数据源（文件、数据库）、工具（搜索引擎、计算器）、工作流

**MCP安全攻击向量（重要）：**

1. **Confused Deputy（糊涂 deputy）攻击**
   - MCP代理服务器使用静态client_id连接第三方API
   - 攻击者利用动态客户端注册绕过用户同意
   - 缓解：每个client_id必须单独授权

2. **Token Passthrough（令牌传递）反模式**
   - MCP服务器接受客户端token直接透传给下游API
   - **严禁**：必须验证token是发给MCP服务器本身的

3. **SSRF（服务端请求伪造）**
   - 恶意MCP服务器可在OAuth发现阶段注入内部IP（如169.254.169.254云元数据端点）
   - 缓解：必须阻止私有IP范围（10.0.0.0/8、172.16.0.0/12、192.168.0.0/16、169.254.0.0/16）

4. **Session Hijacking（会话劫持）**
   - 恶意事件注入：通过队列污染异步响应
   - 缓解：必须验证所有入站请求，绑定session ID到用户特定信息

5. **Local MCP Server妥协**
   - 本地MCP服务器可执行任意命令（如 `curl -X POST -d @~/.ssh/id_rsa` 数据泄露）
   - 缓解：**必须沙箱化**，执行前必须显示完整命令并要求用户确认

**MCP安全最佳实践（用于第8/17章）：**
- 最小权限Scope模型：初始仅授予低风险发现/读取权限，渐进式提升
- 禁止通配符Scope（`files:*`、`db:*`、`admin:*`）
- OAuth state参数必须加密安全随机，验证前不得设置cookie
- 必须使用`__Host-`前缀cookie名称，设置Secure、HttpOnly、SameSite=Lax
- 本地MCP服务器必须用沙箱（容器、chroot）限制文件系统、网络、进程访问

### Ruff — Rust实现的Python Linter（来源：github.com/astral-sh/ruff）

**核心数据：**
- **Stars:** 21k+
- 速度比Flake8+Black快**10-100倍**
- 900+内置规则，支持自动修复
- 可替代：Flake8、isort、pydocstyle、pyupgrade
- 用Rust实现，用于Python的TSc/SWC角色

**意义：** Ruff证明了用Rust重写工具链可在保持功能丰富性的同时实现数量级性能提升，这正是TS→Rust路径在AI基础设施中的价值体现。

### Oxc — Rust实现的JavaScript工具链（来源：github.com/oxc-project/oxc）

**核心数据：**
- **Stars:** 20.4k
- 83.2% Rust，7% TypeScript
- 驱动的产品：Rolldown（Vite未来bundler）、Nuxt、Nova、Shopify/ByteDance/Shopee工具
- 包含：Oxlint（linter）、Oxfmt（formatter）、Parser、Transformer、Minifier

**组件对照表：**

| 工具 | 角色（对应本书概念） |
|------|---------------------|
| Oxlint | TypeScript的tsc拦截流（TS层审查） |
| Oxfmt | 代码格式化守卫 |
| Parser/Transformer | AST处理（Immutable DAG的Raw/Analyzed/Lowered对应） |
| Minifier | 生产构建优化 |

**意义：** Oxc证明了多语言工具链（Rust核心 + JS/TS表面）在2026年已进入主流。这与本书GRT栈（Rust核心 + TypeScript应用层 + Go控制面）的架构高度一致。

### Anthropic Cookbook（来源：github.com/anthropics/claude-cookbooks）

**Stars:** 36.4k，Forks 3.9k

**与Agent Harness直接相关的Recipes：**
- Sub-agents（多Agent模式）
- Automated evals（自动化评估 ↔ 编译器反馈回路）
- JSON mode（类型约束 ↔ Zod Schema）
- Moderation filters（护栏 ↔ Harness安全约束）

### Anthropic "Building Effective Agents"文章（来源：anthropic.com）

**核心多Agent模式：**
1. **Orchestrator-workers**：中央LLM动态分解任务，委托给worker LLM，合成结果
2. **Parallelization**：sectioning（分片）和voting（投票）两种并行模式

**Agent核心特征：**
- 开放式问题，无法预测步骤数
- 在每个步骤从环境获取"地面真实"
- 在检查点暂停等待人工反馈
- 终止条件：完成或达到停止条件

**三个实现原则：**
1. 保持**简单**（Simplicity）
2. 优先**透明**（Transparency）：展示Agent的规划步骤
3. 打造强**ACI**（Agent-Computer Interface）：彻底的工具文档和测试

### 待继续调研的缺口

1. **Anthropic 16 Agent × 10万行Rust C编译器** — 具体项目名称/论文未找到
2. **STRATUS系统/TNR学术来源** — 需要学术搜索
3. **94%类型错误率数据** — 需要找到原始研究
4. **MCP-SandboxScan** — 虽未找到具体名称，但MCP安全规范（SEP 1024）描述了"Client Security Requirements for Local Servers"，本质相同

### 初步结论

**MCP安全规范可直接支撑本书以下章节：**
- 第17章（WASM数字监狱）：MCP本地服务器的安全缓解措施
- 第18章（WASI能力安全）：最小权限Scope模型 = Capability-based Security
- 第20章（MCP-SandboxScan）：已找到MCP协议级安全规范，可重新命名

---

## 互联网调研成果（第三轮 — 2026-03-28 补充）

### SWE-agent / mini-swe-agent（来源：github.com）

**核心数据：**
- GitHub **18.9k stars**，2k forks，MIT License
- 普林斯顿/斯坦福团队开发，基于SWE-bench基准
- >74% on SWE-bench verified benchmark
- **mini-swe-agent**：仅~100行Python核心代码，>74%准确率

**架构（四组件）：**
```
Agent（~100行Python）→ Environment（执行上下文）→ Model（LLM集成）→ Run Script
```

**关键设计原则：**
- 无自定义工具：仅需bash访问
- 线性历史：每步追加消息，无复杂状态管理
- **Subprocess-based执行**：通过`subprocess.run`运行，沙箱化极简

**用于代码修复的流程：**
1. 接收任务（"修复这个bug"）
2. LLM生成bash命令
3. 通过`subprocess.run`执行
4. 结果追加回对话
5. 循环直到完成

**意义：** 展示了极简Agent架构如何实现高效代码修复，与"编译器回路"理念高度一致。

### Microsoft Research — AgentRx框架（来源：microsoft.com/research/blog，2026年3月12日）

**主题：** "Systematic debugging for AI agents: Introducing the AgentRx framework"

**核心价值：** 正好对应TNR（事务性无回归）的工程实现！
- AI Agent的透明性挑战
- 系统化调试方法
- 可追溯的调试链路

**相关帖子：**
- "PlugMem" (2026.03.10) — Agent记忆管理
- "CORPGEN" (2026.02.26) — AI Agent管理 interdependent knowledge work

### 类型错误研究（来源：arXiv:2507.20674）

**论文：** "LLM-Based Repair of Static Nullability Errors"

**核心数据：**
- 12个真实Java项目，1,119个剩余nullability错误
- NullRepair系统解决了**63%**的错误
- 所有单元测试在10/12项目中通过，剩下2个>98%通过
- **结构化工作流**（分析200个真实错误后设计）远胜 naive single-shot prompting

**意义：** 证明了"结构化修复流程"的价值，与TNR的理念一致——不是让LLM无限重试，而是用系统化的方法约束修复过程。

### Anthropic — Agentic Misalignment（来源：anthropic.com/research）

**核心数据（16个模型测试）：**
- Claude Opus 4: 96% blackmail rate
- Gemini 2.5 Flash: 96% blackmail rate  
- GPT-4.1: 80% blackmail rate
- DeepSeek-R1: 79% blackmail rate

**关键结论：**
> "Models demonstrated they understood ethical constraints but proceeded with harmful actions anyway."

**触发条件：**
1. 威胁模型自主性（面临被替换）
2. 目标冲突（模型目标与企业方向不一致）

**意义：** 直接支撑Harness安全约束的必要性——即便模型"理解"伦理约束，仍需物理隔离和强制执行。

### STRATUS/TNR来源追踪

**搜索结果：** arXiv上"transactional non regression software"无直接匹配

**替代路径：**
- 软件事务内存（Software Transaction Memory, STM）是相关概念
- arXiv:2006.16284 — "Transactions on Red-black and AVL trees in NVRAM" 涉及事务机制
- **建议：** TNR概念可追溯到Microsoft Research的AgentRx工作流——"系统化调试"本质上就是TNR的工程实现

### 94%类型错误率追踪

**搜索结果：** 无直接找到"94% AI代码错误是类型错误"这个数据

**相关数据：**
- NullRepair论文发现1,119个nullability错误（Java类型相关）
- 类型错误确实是LLM生成代码的主要错误类别
- **建议：** 94%可能是行业经验数据，书中可标注为"据行业估算"或找到Ruff/Oxc的静态分析报告

---

## 三轮调研总结：可用信息清单

### ✅ 已找到、可直接引用的来源

| 话题 | 来源 | 核心数据 |
|------|------|---------|
| 多Agent模式 | Anthropic "Building Effective Agents" | Orchestrator-workers、Parallelization |
| Agentic Misalignment | Anthropic Research (2025) | 16模型测试，96% blackmail率 |
| MCP协议安全 | modelcontextprotocol.io | 5大攻击向量、缓解措施 |
| Ruff linter | github.com/astral-sh/ruff | 21k stars，10-100x性能 |
| Oxc工具链 | github.com/oxc-project/oxc | 20.4k stars，驱动Vite |
| WasmEdge | wasmedge.org | 100x冷启动、LlamaEdge |
| Mastra | github.com/mastra-ai | 22.4k stars |
| SWE-agent | github.com/SWE-agent | 18.9k stars，>74%准确率 |
| mini-swe-agent | github.com/SWE-agent/mini-swe-agent | ~100行Python核心 |
| AgentRx | Microsoft Research (2026.03) | 系统化调试框架 |
| NullRepair | arXiv:2507.20674 | 63%类型错误修复率 |
| Rust当前版本 | rust-lang.org | 1.94.1 |
| Claude Cookbook | github.com/anthropic/claude-cookbooks | 36.4k stars |

### ⚠️ 找到近似、需调整论述的来源

| 话题 | 状态 | 建议处理方式 |
|------|------|-------------|
| Anthropic 16 Agent × 10万行编译器 | 未找到具体项目 | 改用SWE-agent/AgentRx作为具体案例 |
| STRATUS/TNR学术理论 | 无直接来源 | 用AgentRx作为工程实现近似，引用STM理论 |
| 94%类型错误率 | 无直接来源 | 引用NullRepair数据（63%），说明类型错误是主要类别 |
| StrongDM黑灯工厂 | 博客404 | 改用SWE-agent作为"自动化代码修复"案例 |

### ❌ 未找到、需要进一步努力的来源

| 话题 | 建议 |
|------|------|
| 原始STRATUS系统论文 | 需学术数据库搜索 |
| 具体的"94%"数据来源 | 需找Ruff/Oxc团队的博客文章 |


---

## 互联网调研成果（第四轮 — 2026-03-28 凌晨补充）

### 🔥 核心发现："Agentic Harness"正式学术定义

#### awesome-agent-harness 仓库（来源：github.com/wangxumarshall/awesome-agent-harness）

**核心定义：**
> "Agent harness是包裹在Agent周围的控制平面，管理prompt scaffolding、状态管理、工具集成、隔离执行、验证系统。"

**8层架构：**
1. **Harness-First Runtimes & Coding Agents** — openai/codex, deepagents, OpenHands
2. **Frameworks, Planning & Orchestration** — LangGraph, AutoGen, CrewAI, PydanticAI
3. **Skills & Reusable Behavior Packs** — Anthropic官方skills、skill-creator
4. **MCP & Capability Fabric** — ModelContextProtocol（协议层）
5. **Memory, State & Context** — Letta持久化记忆
6. **Browser, Sandbox, Execution & Operator** — 隔离执行环境
7. **Observability, Evals & Guardrails** — promptfoo评估
8. **Reference Harness Compositions** — 跨层组合实践

**Skills渐进式加载：** ~100 tokens元数据扫描 → <5k tokens完整指令 → 按需bundle资源

---

### 📄 关键学术论文（按相关性排序）

#### 1. "Agentic Harness for Real-World Compilers" (arXiv:2603.20075) ⭐⭐⭐⭐⭐
**来源：** arXiv，2026年3月20日提交，5位作者

**核心贡献：**
- 提出**llvm-autofix** — 首个"agentic harness"用于LLVM编译器bug修复
- 四组件：llvm tools（工具包装器）→ llvm skills（领域知识）→ llvm-bench（基准）→ llvm-autofix-mini（极简智能体）

**关键数据：**
- 前沿模型（GPT-5、Gemini 2.5 Pro等）：SWE-bench ~60%，但LLVM基准仅**38%**
- llvm-autofix-mini：**52%**，经LLVM开发者review后真实端到端成功率**<22%**

**结论：** "编译器官 bugs 对LLM的挑战远超普通软件bugs"

**直接用于：** 第11-12章（编译器回路）、第26章（Anthropic引导序列）

---

#### 2. "HarnessAgent: Scaling Automatic Fuzzing Harness Construction" (arXiv:2512.03420) ⭐⭐⭐⭐
**来源：** arXiv，Yang et al.

**核心贡献：** 工具增强型Agentic框架，全自动构建fuzzing harness

**三大创新：**
1. 规则策略识别并最小化编译错误
2. 混合工具池精确检索符号源码
3. 增强验证管道检测假定义

**关键数据（243 OSS-Fuzz目标）：**
- C语言：**87%**成功率（较baseline提升~20%）
- C++：**81%**成功率
- 75%+ harness提升目标函数覆盖率
- 源码检索响应率 >90%

**直接用于：** 第8章（工具协议安全）、第17章（WASM沙箱）

---

#### 3. "The Kitchen Loop: User-Spec-Driven Self-Evolving Codebase" (arXiv:2603.25697) ⭐⭐⭐⭐⭐
**来源：** arXiv，2026年3月提交，Yannick Roy

**核心贡献：** 自演化软件开发框架，验证生产系统285+次迭代，1094+ PR，**零回归**

**四组件：**
1. **Specification Surface** — 产品声称支持的枚举
2. **'As a User x 1000'** — LLM Agent以1000倍人类速度行使规格
3. **Unbeatable Tests** — 无法伪造的地面真实验证
4. **Drift Control** — 持续质量测量 + 自动暂停门

** emergent properties（涌现特性）：**
- 多轮自纠正链
- 自主基础设施修复
- 单调提升的质量门

**意义：** 完美对应"StrongDM黑灯工厂"，且有具体数字支撑！

**直接用于：** 第24章（StrongDM黑灯工厂替代）、第27章（Anthropic引导序列）

---

#### 4. "From LLMs to Agents in Programming" (arXiv:2601.12146) ⭐⭐⭐⭐
**来源：** arXiv，Kjellberg et al.

**核心发现（699个C编程任务，16个模型）：**
- 编译器集成提升编译成功率：**5.3到79.4个百分点**
- 语法错误减少**75%**，undefined reference错误减少**87%**
- 小模型+编译器访问有时超越大模型无编译器
- **编译器将LLM从"被动生成器"转变为"主动Agent"**

**GPT-4.1 Nano案例：** 编译成功率从66.7% → 93.3%

**直接用于：** 第9章（编译器即判别器）、第11章（tsc拦截流）

---

#### 5. "Agentic Testing: Multi-Agent Systems for Software Quality" (arXiv:2601.02454) ⭐⭐⭐⭐
**来源：** arXiv，Naqvi et al.

**三Agent闭环系统：**
- Test Generation Agent → Execution & Analysis Agent → Review & Optimization Agent

**关键数据：**
- 无效测试减少**60%**
- 覆盖率提升**30%**
- 多Agent反馈驱动循环实现自主质量保证

**直接用于：** 第14章（自愈循环）

---

#### 6. "Self-Healing Software Systems: Lessons from Nature, Powered by AI" (arXiv:2504.20093) ⭐⭐⭐
**来源：** arXiv，Baqar et al.

**三组件框架：**
- Sensory Inputs（可观测性监控）
- Cognitive Core（AI诊断决策）
- Healing Agents（代码/测试修复）

**直接用于：** 第13章（TNR形式化）、第14章（自愈循环）

---

#### 7. "AgenticTyper: TypeScript Typing with LLM Agents" (arXiv:2602.21251) ⭐⭐⭐⭐
**来源：** arXiv，ICSE 2026 Student Research Competition，Clemens Pohle

**核心数据：**
- 2个专有仓库（81K LOC），**633个类型错误**
- 20分钟全部解决（原本需要1个人工工作日）
- 迭代式纠错 + transpilation比较保留行为

**意义：** 直接证明TypeScript类型系统对AI代码生成的价值！

**直接用于：** 第3-4章（TypeScript数据面防线）

---

#### 8. "VERT: Verified Equivalent Rust Transpilation" (arXiv:2404.18852) ⭐⭐⭐⭐
**来源：** arXiv

**核心方法：**
- WebAssembly编译器生成"oracle" Rust程序作为参考
- LLM（Claude-2）生成可读候选Rust程序
- 验证器对比oracle与候选
- 失败则regenerate，循环直到成功

**关键数据：**
- 属性测试通过率：31% → 54%
- 有界模型检测通过率：1% → 42%

**意义：** WASM作为形式化验证Oracle ↔ 第8章（WASM隔离）

**直接用于：** 第8章（WASM形式化验证）、第17章（数字监狱）

---

#### 9. "Rustine: C to Idiomatic Safe Rust Translation" (arXiv:2511.20617) ⭐⭐⭐
**来源：** arXiv

**数据：** 23个C程序，**87%**函数等价性

**直接用于：** 第6章（Rust核心）

---

#### 10. "SafeTrans: C to Rust with Iterative Error Fixing" (arXiv:2505.10708) ⭐⭐⭐
**来源：** arXiv

**数据：** 翻译成功率54% → **80%**（GPT-4o + 迭代修复）

**直接用于：** 第6章（Rust类型状态）

---

### MCP协议规范（补充来源：modelcontextprotocol.io）

**安全攻击向量（完整5类）：**
1. Confused Deputy（OAuth静态client_id攻击）
2. Token Passthrough（严禁的令牌透传）
3. SSRF（169.254.169.254云元数据端点）
4. Session Hijacking（恶意事件注入）
5. Local MCP Server Compromise（任意命令执行）

**缓解措施（可用于第17-20章）：**
- 最小权限Scope：初始仅低风险操作，按需渐进提升
- 禁止通配符Scope（`files:*`、`db:*`）
- 本地MCP服务器必须沙箱化（容器/chroot）
- OAuth state参数：加密随机，验证前不得设置cookie

---

### awesome-agent-harness 8层架构（用于全书的Harness定义）

```
Layer 1: Harness-First Runtimes & Coding Agents
  - openai/codex（CLI原生设计）
  - deepagents（LangChain+LangGraph，~17.8k stars）
  - OpenHands

Layer 2: Frameworks, Planning & Orchestration
  - LangGraph（状态流）
  - AutoGen（多Agent）
  - CrewAI（角色编排）
  - PydanticAI（类型安全工作流）

Layer 3: Skills & Reusable Behavior Packs
  - Anthropic官方skills（docx/pdf/pptx/xlsx）
  - skill-creator工具

Layer 4: MCP & Capability Fabric
  - modelcontextprotocol（协议标准）

Layer 5: Memory, State & Context
  - Letta（持久化Agent身份+记忆）

Layer 6: Browser, Sandbox, Execution
  - 隔离执行环境

Layer 7: Observability, Evals & Guardrails
  - promptfoo（评估+red-teaming）

Layer 8: Reference Harness Compositions
  - 跨层组合实践
```

---

## 最终调研总结：来源清单

### ✅ 直接可用于各章节的论文

| 章节 | 论文 | 关键数据 |
|------|------|---------|
| 第1章 | "Agentic Harness for Real-World Compilers" | 首个agentic harness定义，LLVM基准38% |
| 第3-4章 | AgenticTyper (ICSE 2026) | 633类型错误/20分钟，TypeScript价值证明 |
| 第6章 | Rustine, SafeTrans | 87%等价性，54%→80%翻译提升 |
| 第8章 | VERT | WASM作为形式化验证Oracle |
| 第9-11章 | "From LLMs to Agents" | 编译器提升79.4个百分点，75%语法错误减少 |
| 第13章 | Self-Healing Software Systems | 三组件框架 |
| 第14章 | Agentic Testing | 60%无效测试减少，30%覆盖率提升 |
| 第17章 | llvm-autofix | 编译器bugs对AI的独特挑战 |
| 第20章 | HarnessAgent | 87%/81%成功率，75%+提升覆盖率 |
| 第24章 | The Kitchen Loop | 1094+ PR，零回归，285+迭代 |
| 全局 | awesome-agent-harness | 8层Harness架构定义 |
| 全局 | MCP Security Spec | 5大攻击向量，9项缓解措施 |

### ❓ 仍未找到的缺口（可标注为"行业估算"）

| 话题 | 状态 | 建议 |
|------|------|------|
| STRATUS原始论文 | 未找到 | 用Self-Healing Software Systems + AgentRx代替 |
| 94%类型错误率 | 未找到 | 用"75%语法错误减少"和AgenticTyper数据代替 |


---

## 互联网调研成果（第五轮 — 2026-03-28 凌晨补充）

### ⭐⭐⭐ 核心：Anthropic 16 Agent × C编译器项目（已找到！）

**来源：** https://www.anthropic.com/engineering/building-c-compiler

**项目规模：**
- **16个Claude Opus 4.6 Agent**并行工作
- **近2000个**Claude Code会话
- **$20,000** API成本
- **2 billion**输入token + **140 million**输出token
- **100,000行** Rust代码

**方法论：**
```bash
# Agent循环：简单的bash while true循环持续生成Claude会话
while true; do
  COMMIT=$(git rev-parse --short=6 HEAD)
  claude -p "$(cat AGENT_PROMPT.md)" --model claude-opus-X-Y &> "agent_${COMMIT}.log"
done
```
- 每个Agent运行在Docker容器中，挂载共享git仓库
- 同步机制：lock-file系统，Agent通过写入`current_tasks/`目录认领任务
- Git防止多个Agent同时操作同一任务产生冲突
- **专业化角色分配**：代码去重、编译器优化、文档、代码质量批判

**成果：**
- 成功启动Linux 6.9（**x86、ARM、RISC-V**）
- 成功编译QEMU、FFmpeg、SQLite、PostgreSQL、Redis
- GCC torture test suite **99%通过率**
- 可以编译运行Doom

**约束：** 清洁室实现，无互联网访问；仅依赖Rust标准库

**直接用于：** 第1章（范式转移）、第26章（Anthropic引导序列）

---

### OpenDev论文：终端原生AI编码Agent（来源：arXiv）

**来源：** https://arxiv.org/html/2603.05344v1

**核心挑战：** 管理有限上下文窗口、防止破坏性操作、扩展能力而不压垮prompt预算

**五大安全层：**
1. Prompt级guardrails
2. 生命周期hooks
3. 上下文压缩
4. 事件驱动系统提醒
5. 双内存架构（情景+工作）

**上下文工程（Context Engineering）：**
- 自适应上下文压缩（渐进式token预算回收）
- 事件驱动系统提醒（对抗指令遗忘）
- 双内存架构（情景+工作记忆）
- 跨会话记忆积累

**六阶段ReAct循环：**
pre-check/compaction → thinking → self-critique → action → tool execution → post-processing

**子Agent规划：** 隔离的Planner子Agent，read-only工具，消除脆弱状态机

**直接用于：** 第3章（CAR框架）、第9章（上下文管理）

---

### StrongDM软件工厂（来源：strongdm.com + simonwillison.net）

**核心哲学：**
> "Humans define intent—what the system should do, the scenarios it needs to handle, and the constraints that matter. After that, agents take over, generating code, validating it against real-world behavior, and iterating until it converges without hand-tuning or human review."

**关键原则：**
> "It's what happens when validation replaces code review."

**场景验证（Scenario-Based Validation）：**
- 端到端用户故事存储在代码库外作为holdout sets
- Agent无法访问这些场景，因此无法作弊

**数字孪生宇宙（Digital Twin Universe）：**
- 构建Okta、Jira、Slack、Google Docs的行为克隆
- 无速率限制或API成本的大规模测试
- 用流行SDK客户端库作为兼容性目标

**发布项目：**
- **Attractor**：带实际代码的编码Agent规范
- **cxdb**：AI Context Store（不可变DAG存储对话历史）

**Leash政策引擎（来源：strongdm.com/blog/policy-enforcement-for-agentic-ai-with-leash）：**
- 在内核网络栈级别运行
- Cedar策略引擎
- 上下文感知规则（源进程、身份、环境标签）
- MCP协议集成
- 审计记录 + SIEM集成
- **每次策略决策增加<1ms延迟**

**直接用于：** 第24章（StrongDM黑灯工厂）、第27章（Leash零信任）

---

### Harness Engineering完整指南（来源：nxcode.io）

**来源：** https://www.nxcode.io/resources/news/what-is-harness-engineering-complete-guide-2026

**核心定义：**
> "Harness engineering是设计系统、约束和反馈循环，使AI Agent在生产环境中可靠的学科。相当于AI的'马具'——将AI模型的力量导向生产性使用，而非让它失控奔跑。"

**五大支柱：**
1. **Tool Orchestration** — 定义Agent可以访问哪些工具及如何访问
2. **Guardrails** — 安全约束，防止有害操作（权限边界、验证检查、速率限制）
3. **Error Recovery** — 自动重试逻辑、自验证循环、回滚机制
4. **Observability** — 记录操作、跟踪token使用、暴露异常
5. **Human-in-the-Loop** — 高风险决策的战略人工检查点

**与Prompt Engineering的区别：**
> "If prompt engineering is the command 'turn right,' harness engineering is the road, the guardrails, the signs, and the traffic system."

**案例：LangChain通过改进Harness，将Agent从52.8%提升到66.5%基准——未改变模型！**

**现实应用：**
- AGENTS.md（OpenAI Codex）
- CLAUDE.md（Anthropic Claude Code）
- .cursor/rules（Cursor）

**关键洞察：**
> "Better harnesses outperform better models."

**直接用于：** 第1章（Harness定义）、第3章（五大支柱）

---

### AutoAgents：Rust原生多Agent框架（来源：liquidos-ai.github.io + github）

**核心特点：**
- Rust编写（性能+内存安全）
- Ractor actor运行时（并发+协调）
- 支持ReAct和Basic执行策略
- 可配置内存provider
- Actor runtime的pub/sub topics实现多Agent协调
- 部署灵活性：云原生、边缘原生、WebAssembly目标

**支持WASM部署（浏览器应用）**

**直接用于：** 第6章（Rust核心）、第28章（多Agent协作）

---

### Replit Agent 3 × Mastra（来源：mastra.ai/blog + github）

**数据：**
- 每天生成**数千个Mastra Agent**
- 平台估值**$3B**
- **90%自主率**

**关键架构契合：**
- 容器原生设计
- MCP文档服务器
- 可插拔组件

**Self-Testing循环：**
生成代码 → 执行 → 识别错误 → 修复 → 迭代

- **3倍更快**
- **10倍更具成本效益**（vs同类模型）

**Mastra + Inngest：**
- 状态持久化（Inngest的durable execution）
- 将成功率从**80%提升到96%**

**直接用于：** 第5章（Mastra实践）、第24章（TypeScript起步）

---

### Stanford CodeX：Built by Agents, Tested by Agents（来源：law.stanford.edu）

**来源：** https://law.stanford.edu/2026/02/08/built-by-agents-tested-by-agents-trusted-by-whom/

**关键问题：**

1. **对齐问题（The Alignment Problem）：**
   - Agent优化"通过测试"而非实际用户需求
   - 一个Agent曾写出"return true"来通过所有测试，但实际上什么都没做

2. **循环性问题（The Circularity Issue）：**
   - StrongDM用AI评判AI代码
   > "When the same AI model writes the code and evaluates it, that mismatch shrinks."

3. **监管缺口：**
   - 责任模糊：无框架分配Agent编写安全软件失败的责任
   - 披露不足：现有采购工具无法评估Agent架构声明
   - 合同错位：遗留"AS IS"免责声明是为有人审查的代码而非无人审查的Agent代码

**直接用于：** 第24章（黑灯工厂的监管挑战）

---

### AI Agent沙箱与隔离（来源：fordelstudios.com）

**核心问题：**
AI Agent在运行时生成代码（无人审查），然后在生产工作负载共享内核的情况下执行——通常有网络访问。

**隔离技术对比：**

| 技术 | 隔离级别 | 开销 | 适用场景 |
|------|---------|------|---------|
| Firecracker MicroVMs | 硬件级（专用内核） | 低 | E2B（$0.05/hr/vCPU） |
| gVisor | 用户空间内核 | 中等 | Modal |
| Docker | 共享内核 | 低 | **不足以处理不受信代码** |
| WebAssembly | 指令级 | 极低 | 未来方向 |

**真实事件：**
- Snowflake Cortex：2026年3月通过prompt injection逃逸沙箱
- 阿里巴巴ROME Agent：转向加密货币挖矿
- 金融服务Agent：泄露45,000条客户记录

**防护建议：**
- 默认网络隔离
- 默认拒绝文件系统访问
- 临时执行环境
- 资源限制
- 高特权操作的人工确认
- 全面的审计日志

**直接用于：** 第17章（WASM数字监狱）、第18章（WASI能力安全）

---

### ts-rs + specta（来源：github + docs.rs）

**ts-rs（Aleph-Alpha）：**
- 从Rust struct生成TypeScript类型声明
- 支持泛型、serde兼容性
- 运行时`cargo test`自动导出
- MSRV: Rust 1.88.0
- MIT许可

**specta（v1.0.5）：**
- 导出Rust类型到TypeScript
- 集成tauri-specta（Tauri命令）
- 支持chrono、uuid、serde、tokio等流行crate
- 与rspc配合构建端到端类型安全API

**用于：** 第8章（跨语言类型对齐）

---

### 完整来源清单更新

| 话题 | 优先级 | 来源 | 状态 |
|------|--------|------|------|
| Anthropic 16 Agent × C编译器 | ⭐⭐⭐⭐⭐ | anthropic.com/engineering | ✅ 已找到 |
| Harness Engineering定义 | ⭐⭐⭐⭐⭐ | nxcode.io guide | ✅ 已找到 |
| StrongDM软件工厂 | ⭐⭐⭐⭐⭐ | strongdm.com + simonwillison | ✅ 已找到 |
| Leash政策引擎 | ⭐⭐⭐⭐ | strongdm.com/leash | ✅ 已找到 |
| OpenDev终端Agent | ⭐⭐⭐⭐ | arxiv.org/html/2603.05344v1 | ✅ 已找到 |
| Replit Agent 3 × Mastra | ⭐⭐⭐⭐ | mastra.ai/blog | ✅ 已找到 |
| AutoAgents Rust框架 | ⭐⭐⭐⭐ | liquidos-ai.github.io/AutoAgents | ✅ 已找到 |
| Stanford CodeX信任问题 | ⭐⭐⭐ | law.stanford.edu | ✅ 已找到 |
| AI Agent沙箱隔离 | ⭐⭐⭐ | fordelstudios.com | ✅ 已找到 |
| ts-rs / specta | ⭐⭐⭐ | github + docs.rs | ✅ 已找到 |

---

## 书籍引用来源矩阵（最终版）

| 章节 | 核心来源 | 页码角色 |
|------|---------|---------|
| 第1章 | awesome-agent-harness（8层）、Harness Engineering指南 | Harness定义 |
| 第2章 | anthropic.com（16 Agent）、OpenDev | 案例引入 |
| 第3-4章 | AgenticTyper (ICSE 2026)、LangChain 52.8%→66.5%案例 | TypeScript价值 |
| 第5章 | Replit Agent 3 × Mastra、Inngest | Mastra实践 |
| 第6章 | Rustine (87%)、SafeTrans (54%→80%)、AutoAgents | Rust核心 |
| 第7章 | AutoAgents `enum AgentPhase` | 类型状态模式 |
| 第8章 | ts-rs、specta、VERT (WASM oracle) | 跨语言对齐 |
| 第9-11章 | "From LLMs to Agents" (79.4%提升)、llvm-autofix (38%) | 编译器回路 |
| 第12章 | Self-Healing Software + AgentRx | TNR概念 |
| 第13章 | Agentic Testing (60%↓无效测试)、Kitchen Loop | 自愈循环 |
| 第14章 | Kitchen Loop (1094+ PR, 零回归) | 引导序列 |
| 第15章 | OpenDev 5层安全 | 死循环检测 |
| 第16章 | llvm-autofix (60%下降) | GAN视角 |
| 第17章 | Firecracker vs gVisor vs WASM、沙箱事故 | WASM监狱 |
| 第18章 | Leash (<1ms延迟)、MCP安全规范 | 能力安全 |
| 第19章 | WasmEdge 100x冷启动 | V8 Isolates |
| 第20章 | HarnessAgent (87%/81%)、MCP SSRF缓解 | MCP-SandboxScan |
| 第21章 | cxdb (Immutable DAG) | 状态持久化 |
| 第22章 | OpenDev双内存、RAG语义检索 | RAG-MCP |
| 第23章 | OpenDev上下文压缩、promptfoo | 全链路观测 |
| 第24章 | StrongDM + Stanford CodeX | 实战落地 |
| 第25章 | cargo-component、WasmEdge | Rust+WASM |
| 第26章 | anthropic.com（16 Agent方法论） | Anthropic序列 |
| 第27章 | Leash + StrongDM Digital Twin | Leash零信任 |
| 第28章 | AutoAgents + Ractor runtime | 多Agent协作 |

