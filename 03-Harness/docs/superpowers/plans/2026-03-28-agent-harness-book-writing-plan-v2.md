# 《Agent Harness：构建生产级AI Agent的确定性基座》写作计划（修订版）

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan chapter-by-chapter.
>
> **SPEC版本：** v2（2026-03-28）
> **核心变更：** 修复7个问题（书名/核心洞察/Python立场/指标/桥接/脚手架/开放问题）

**Goal:** 撰写22章专著，建立生产级AI Agent的Harness工程方法论，配套代码脚手架和量化指标体系。

**Architecture:** 五部分结构（问题与原理 → 语言层 → 编译器层 → 运行时层 → 生产落地），每章含"魔法时刻"、增量代码开发、标准桥接语。

**Code Scaffolding:**
```
Part I 结束时：AgentBasic（最简有状态Agent）
Part II 结束时：TypeSafeAgent（类型化+跨语言）
Part III 结束时：CompiledAgent（编译检查+TNR+自愈）
Part IV 结束时：IsolatedAgent（WASM沙箱+MCP隔离）
Part V 结束时：MultiAgentSystem（完整GRT栈）
```

---

## 文件结构

```
chapters/
├── part0-preface/           # 序言（不在22章内）
│   └── preface.md            # 本书适合谁/不适合谁
├── part1-problem/           # 第一部分：问题与原理
│   ├── ch01-why-wrong.md    # 为什么现有的AI编程方法论都是错的
│   └── ch02-first-principles.md  # Harness工程学第一性原理
├── part2-language/          # 第二部分：语言层
│   ├── ch03-ts-contract.md   # TypeScript类型系统作为契约层
│   ├── ch04-rust-ownership.md    # Rust所有权模型
│   ├── ch05-rust-typestate.md   # Rust类型状态模式
│   ├── ch06-go-controlplane.md   # Go控制平面
│   └── ch07-crosslang-types.md   # 跨语言类型对齐
├── part3-compiler/          # 第三部分：编译器层
│   ├── ch08-compiler-judge.md    # 编译器作为判别器
│   ├── ch09-feedback-loop.md     # 编译器反馈回路
│   ├── ch10-tnr-formal.md       # TNR形式化定义
│   ├── ch11-self-healing.md     # 自愈循环
│   └── ch12-deadloop-rollback.md # 死循环检测与回滚
├── part4-runtime/           # 第四部分：运行时层
│   ├── ch13-wasm-prison.md   # WebAssembly数字监狱
│   ├── ch14-wasi-capability.md  # WASI能力安全
│   ├── ch15-v8-isolates.md   # V8 Isolates
│   ├── ch16-mcp-sandbox.md   # MCP沙箱扫描
│   ├── ch17-immutable-dag.md # Immutable DAG
│   └── ch18-rag-mcp.md       # RAG-MCP动态检索
├── part5-production/         # 第五部分：生产落地
│   ├── ch19-min-stack.md     # 最小可用栈
│   ├── ch20-production-deploy.md  # 生产部署
│   ├── ch21-boot-sequence.md # 引导序列
│   └── ch22-multi-agent.md   # 多Agent协作
└── appendices/
    ├── app-a-car-theory.md
    ├── app-b-tnr-stm.md
    ├── app-c-typestate.md
    ├── app-d-capability-formal.md
    └── app-e-wasm-linear.md
```

---

## 写作任务总览

| 阶段 | 任务数 | 说明 |
|------|--------|------|
| 第一部分 | 2章 | 问题定义，定调 |
| 第二部分 | 5章 | 语言层契约 |
| 第三部分 | 5章 | 编译器层审查 |
| 第四部分 | 6章 | 运行时层隔离 |
| 第五部分 | 4章 | 实战落地 |
| 附录 | 5篇 | 理论深潜 |
| **总计** | **22章正文 + 5附录** | |

---

## 章节任务模板

**每章必须包含以下结构：**

```markdown
## 本章Q
[一个具体的、读者会问的问题]

## 魔法时刻
[本章的核心洞察（逆向洞察/统一揭示/边界划定之一）]

## 五分钟摘要
[用2-3句话讲清楚本章核心结论]

## 实践代码
[完整的可运行代码块]

## 进阶理论（可选）
[底层原理与学术溯源]

## 桥接语
- 承上：[不超过2句话]
- 启下：[下章要回答的问题]
- 认知缺口：[为什么必须知道]

## 本章来源
- [一手来源列表]
```

---

## 第一部分：问题与原理

### Task 1: 第1章 — 为什么现有的AI编程方法论都是错的

**文件:** `chapters/part1-problem/ch01-why-wrong.md`

**本章Q:** 既然AI能写代码，为什么还需要Harness？

**魔法时刻:** LangChain的脆弱性不是bug，而是设计缺陷——它试图用提示词管理弥补架构问题

- [ ] **Step 1: 撰写开篇失败案例** — 用一个真实失败案例开场（基于调研成果）
- [ ] **Step 2: 撰写LangChain局限性分析** — 具体代码案例说明架构缺陷
- [ ] **Step 3: 撰写核心论点** — 提示词管理是外科手术，Harness是建筑工程
- [ ] **Step 4: 撰写魔法时刻段落** — LangChain设计缺陷的深层原因
- [ ] **Step 5: 设计桥接语** — 承上（问题）→ 启下（三层边界如何过滤概率性）
- [ ] **Step 6: 列出本章一手来源**

### Task 2: 第2章 — Harness工程学的第一性原理

**文件:** `chapters/part1-problem/ch02-first-principles.md`

**本章Q:** Harness的设计哲学根源是什么？

**魔法时刻:** 三层边界不是三重保险，而是三层过滤器，每层过滤不同类型的概率性

- [ ] **Step 1: 撰写Bounded Intelligence原理** — 概率性输入，确定性输出
- [ ] **Step 2: 撰写CAR框架定义** — Control × Agency × Runtime
- [ ] **Step 3: 撰写三层牢笼架构图** — 语言契约 → 编译器审查 → WASM隔离
- [ ] **Step 4: 撰写Python立场修正** — 训练推理层 vs 编排控制层（非"Python退场"）
- [ ] **Step 5: 撰写开放问题** — AI生成代码的可重复性问题
- [ ] **Step 6: 设计桥接语** — 承上 → 启下（TypeScript类型防线）

---

## 第二部分：语言层 — 契约

### Task 3: 第3章 — TypeScript类型系统作为契约层

**文件:** `chapters/part2-language/ch03-ts-contract.md`

**本章Q:** 如何用类型系统消灭AI生成的JSON解析错误？

**魔法时刻:** TypeScript的type是编译时约束，Zod的schema是运行时约束，二者合一是完整的概率性边界

**代码脚手架:** TypeSafeAgent增量开发（继承自AgentBasic）

- [ ] **Step 1: 撰写Branded Types实战** — 品牌类型终结字符串级联编程
- [ ] **Step 2: 撰写Zod Schema完整示例** — `zod.infer<typeof AgentState>`
- [ ] **Step 3: 撰写TypeChat示例** — Schema as Code同像性约束
- [ ] **Step 4: 撰写对比表格** — 2023年长Prompt依赖 vs 2026年类型约束
- [ ] **Step 5: 撰写魔法时刻段落** — type+schema=完整概率性边界
- [ ] **Step 6: 设计桥接语** — 承上 → 启下（为什么Rust比TypeScript更"硬"）
- [ ] **Step 7: 列出本章一手来源**

### Task 4: 第4章 — Rust所有权模型

**文件:** `chapters/part2-language/ch04-rust-ownership.md`

**本章Q:** 为什么Rust是Harness核心语言？

**魔法时刻:** Rust所有权是AI无法逃脱的监狱——不是因为强制，而是因为它是编译时事实

**代码脚手架:** Rust核心类型定义

- [ ] **Step 1: 撰写所有权实战代码** — AI无法"悄悄遗忘"Token的具体演示
- [ ] **Step 2: 撰写生命周期标注** — 借用检查器的AI行为约束
- [ ] **Step 3: 撰写Odyssey Bundle架构** — Agent定义+工具+沙箱策略打包
- [ ] **Step 4: 撰写魔法时刻段落** — 所有权作为编译时事实的意义
- [ ] **Step 5: 设计桥接语** — 承上 → 启下（所有权约束了状态泄漏，状态跃迁怎么办）
- [ ] **Step 6: 列出本章一手来源**

### Task 5: 第5章 — Rust类型状态模式

**文件:** `chapters/part2-language/ch05-rust-typestate.md`

**本章Q:** 如何让AI的状态机无法进入非法状态？

**魔法时刻:** 状态机的非法状态不是设计失误，而是未被发现的设计意图

**代码脚手架:** AgentPhase状态机实现

- [ ] **Step 1: 撰写`enum AgentPhase`完整代码** — 状态跃迁合法性的编译器强制
- [ ] **Step 2: 撰写Result<T, HarnessError>** — `?`操作符与强迫性兜底
- [ ] **Step 3: 撰写错误即控制流** — 完整的错误处理流图
- [ ] **Step 4: 撰写魔法时刻段落** — 非法状态是未发现的设计意图
- [ ] **Step 5: 设计桥接语** — 承上 → 启下（单Agent状态约束了，多Agent怎么办）
- [ ] **Step 6: 列出本章一手来源**

### Task 6: 第6章 — Go控制平面与高并发网关

**文件:** `chapters/part2-language/ch06-go-controlplane.md`

**本章Q:** 为什么Go适合控制平面而非Agent逻辑？

**魔法时刻:** Go的Goroutine不是为AI设计的，但是为AI的控制平面而生的

**代码脚手架:** Agent路由网关实现

- [ ] **Step 1: 撰写Goroutine调度代码** — Agent路由与长时队列的完整Go代码
- [ ] **Step 2: 撰写API Gateway模式** — 高并发×低延迟的具体实现
- [ ] **Step 3: 撰写Go生态位分析** — 为什么Go不在Agent逻辑而在控制平面
- [ ] **Step 4: 撰写魔法时刻段落** — Goroutine为控制平面而生
- [ ] **Step 5: 设计桥接语** — 承上 → 启下（三个语言层的类型如何跨服务边界保持一致）
- [ ] **Step 6: 列出本章一手来源**

### Task 7: 第7章 — 跨语言类型对齐

**文件:** `chapters/part2-language/ch07-crosslang-types.md`

**本章Q:** 如何保证Rust→TypeScript编译时100%类型一致？

**魔法时刻:** 跨语言类型对齐的难点不是技术，而是谁是新真实来源（SSOT）

**代码脚手架:** GRT栈类型对齐完整实现

- [ ] **Step 1: 撰写ts-rs/specta实战代码** — Rust结构体自动生成TS接口
- [ ] **Step 2: 撰写Result映射** — Rust Result/Option → TS联合类型映射
- [ ] **Step 3: 撰写SSOT实践** — GRT栈单点真实来源的完整代码
- [ ] **Step 4: 撰写魔法时刻段落** — SSOT问题是政治问题，不是技术问题
- [ ] **Step 5: 撰写开放问题** — Bootstrap问题——谁验证验证者？
- [ ] **Step 6: 设计桥接语** — 承上 → 启下（编译器如何做判别）
- [ ] **Step 7: 列出本章一手来源**

---

## 第三部分：编译器层 — 审查

### Task 8: 第8章 — 编译器作为无法贿赂的代码审查者

**文件:** `chapters/part3-compiler/ch08-compiler-judge.md`

**本章Q:** 编译器如何做到比人类reviewer更可靠？

**魔法时刻:** 编译器是唯一一个不会说"差不多"的reviewer

**代码脚手架:** CompilerJudge实现

- [ ] **Step 1: 撰写tsc拦截流代码** — `tsc --noEmit`秒级阻断演示
- [ ] **Step 2: 撰写Cargo验证流** — Rust编译通过≈内存安全正确性
- [ ] **Step 3: 撰写JSON特征列表** — 结构化错误输出的完整代码
- [ ] **Step 4: 撰写魔法时刻段落** — 不会说"差不多"的reviewer
- [ ] **Step 5: 设计桥接语** — 承上 → 启下（编译器反馈如何驱动AI自愈）
- [ ] **Step 6: 列出本章一手来源**

### Task 9: 第9章 — 编译器反馈回路设计

**文件:** `chapters/part3-compiler/ch09-feedback-loop.md`

**本章Q:** 如何让编译器错误驱动AI自愈？

**魔法时刻:** 编译器反馈回路的本质是：一个损失函数，其梯度由类型检查结果定义

**代码脚手架:** FeedbackLoop完整实现

- [ ] **Step 1: 撰写反馈回路架构图** — 生成→校验→反思→回滚流程
- [ ] **Step 2: 撰写JSON特征列表代码** — 编译器输出 → 结构化特征
- [ ] **Step 3: 撰写PID控制器模型** — 编译器Error Log作为反馈信号
- [ ] **Step 4: 撰写魔法时刻段落** — 损失函数与梯度下降的类比
- [ ] **Step 5: 设计桥接语** — 承上 → 启下（如果AI修复引入新bug怎么办）
- [ ] **Step 6: 列出本章一手来源**

### Task 10: 第10章 — TNR事务性无回归的形式化定义

**文件:** `chapters/part3-compiler/ch10-tnr-formal.md`

**本章Q:** 当AI修复引入新bug时，如何保证状态不恶化？

**魔法时刻:** TNR的核心洞察：修复失败时，系统状态应该等价于"从未尝试修复"

**代码脚手架:** TNR事务边界实现

- [ ] **Step 1: 撰写TNR形式化定义** — Precondition × Postcondition × Invariant
- [ ] **Step 2: 撰写编译器层TNR实现** — 编译单元原子性回滚
- [ ] **Step 3: 撰写软件事务内存理论关联** — TNR ↔ STM
- [ ] **Step 4: 撰写魔法时刻段落** — 等价于"从未尝试修复"
- [ ] **Step 5: 设计桥接语** — 承上 → 启下（TNR在编译层实现了，运行时呢）
- [ ] **Step 6: 列出本章一手来源**

### Task 11: 第11章 — 自愈循环

**文件:** `chapters/part3-compiler/ch11-self-healing.md`

**本章Q:** AI如何通过自我对抗实现自愈？

**魔法时刻:** 自愈不是AI在修复，而是系统在强制AI进行梯度下降

**代码脚手架:** CritiqueAgent实现

- [ ] **Step 1: 撰写Critique ↔ Generator代码** — 微秒级对抗的完整实现
- [ ] **Step 2: 撰写指数退避实现** — 状态快照与重试策略
- [ ] **Step 3: 撰写PID控制器模型** — 编译器Error Log作为反馈信号
- [ ] **Step 4: 撰写魔法时刻段落** — 梯度下降的类比
- [ ] **Step 5: 设计桥接语** — 承上 → 启下（如果对抗循环本身陷入死循环怎么办）
- [ ] **Step 6: 列出本章一手来源**

### Task 12: 第12章 — 死循环检测与强制回滚

**文件:** `chapters/part3-compiler/ch12-deadloop-rollback.md`

**本章Q:** 如何防止AI在错误中无限循环？

**魔法时刻:** 死循环的真正问题不是AI停不下来，而是系统如何在AI停不下来时保持可用

**代码脚手架:** DeadLoopDetector实现

- [ ] **Step 1: 撰写死循环检测算法** — 同一编译错误循环的检测
- [ ] **Step 2: 撰写Git Commit断点救援** — 回滚至上个通过节点
- [ ] **Step 3: 撰写人类介入触发条件** — 强制人工审核的判定逻辑
- [ ] **Step 4: 撰写魔法时刻段落** — 停不下来的可用性保证
- [ ] **Step 5: 撰写开放问题** — Harness的自身脆弱性
- [ ] **Step 6: 设计桥接语** — 承上 → 启下（编译时检查有了，运行时呢）
- [ ] **Step 7: 列出本章一手来源**

---

## 第四部分：运行时层 — 隔离

### Task 13: 第13章 — WebAssembly数字监狱

**文件:** `chapters/part4-runtime/ch13-wasm-prison.md`

**本章Q:** 为什么Docker无法满足Agent隔离需求？

**魔法时刻:** Docker的隔离是进程级的，WASM的隔离是指令级的——这不是程度差异，是性质差异

**代码脚手架:** WASM Agent骨架

- [ ] **Step 1: 撰写Docker vs WASM对比** — 冷启动、内核面、内存占用数据表
- [ ] **Step 2: 撰写WASM隔离代码** — 30MB运行时 vs 4GB Python演示
- [ ] **Step 3: 撰写指令级隔离原理** — WASM沙箱机制技术分析
- [ ] **Step 4: 撰写魔法时刻段落** — 进程级 vs 指令级的性质差异
- [ ] **Step 5: 设计桥接语** — 承上 → 启下（WASM隔离了执行，但代码能访问什么资源）
- [ ] **Step 6: 列出本章一手来源**

### Task 14: 第14章 — WASI能力安全与TNR运行时实现

**文件:** `chapters/part4-runtime/ch14-wasi-capability.md`

**本章Q:** 如何从物理上消灭"AI删库跑路"的可能性？

**魔法时刻:** WASI能力撤销的物理意义：不是"不允许"，而是"物理上不可能"

**代码脚手架:** WASI Capability实现

- [ ] **Step 1: 撰写能力导向执行代码** — 文件/Socket显式授予的完整WASI示例
- [ ] **Step 2: 撰写TNR运行时实现** — WASI能力撤销作为回滚原语
- [ ] **Step 3: 撰写安全证明** — 消灭AI删库跑路的物理可能性分析
- [ ] **Step 4: 撰写魔法时刻段落** — "不允许" vs "物理上不可能"
- [ ] **Step 5: 设计桥接语** — 承上 → 启下（V8 Isolates与WASM有何不同）
- [ ] **Step 6: 列出本章一手来源**

### Task 15: 第15章 — V8 Isolates与毫秒级冷启动

**文件:** `chapters/part4-runtime/ch15-v8-isolates.md`

**本章Q:** 如何实现真正的无服务器Agent执行？

**魔法时刻:** V8 Isolates的毫秒级冷启动不是性能优化，而是架构选择——它改变了可能的系统设计

**代码脚手架:** V8 Isolate Worker实现

- [ ] **Step 1: 撰写毫秒级冷启动数据** — Cloudflare Dynamic Workers具体数字
- [ ] **Step 2: 撰写GPU穿透代码** — GGML + Llama本地推理
- [ ] **Step 3: 撰写WasmEdge集成** — 与WASI的完整集成
- [ ] **Step 4: 撰写魔法时刻段落** — 架构选择 vs 性能优化
- [ ] **Step 5: 设计桥接语** — 承上 → 启下（隔离了执行环境，Agent如何调用外部工具）
- [ ] **Step 6: 列出本章一手来源**

### Task 16: 第16章 — MCP沙箱扫描与提示词注入拦截

**文件:** `chapters/part4-runtime/ch16-mcp-sandbox.md`

**本章Q:** 不受信的MCP工具如何安全调用？

**魔法时刻:** 工具是可信的，但工具的输出是不可信的

**代码脚手架:** MCP Sandboxing实现

- [ ] **Step 1: 撰写MCP隔离架构** — 不受信MCP工具的WASM隔离方案
- [ ] **Step 2: 撰写网络阻断代码** — 毫秒级冷启动×网络零连通
- [ ] **Step 3: 撰写提示词注入拦截** — 具体拦截机制与代码
- [ ] **Step 4: 撰写魔法时刻段落** — 工具可信 vs 输出不可信
- [ ] **Step 5: 设计桥接语** — 承上 → 启下（隔离了工具调用，状态如何持久化）
- [ ] **Step 6: 列出本章一手来源**

### Task 17: 第17章 — Immutable DAG状态持久化

**文件:** `chapters/part4-runtime/ch17-immutable-dag.md`

**本章Q:** 如何实现100%确定性重放？

**魔法时刻:** 状态的历史比状态本身更重要

**代码脚手架:** ImmutableDAG实现

- [ ] **Step 1: 撰写AST三阶段代码** — Raw/Analyzed/Lowered的完整处理
- [ ] **Step 2: 撰写DAG验证代码** — 错误码体系的具体实现
- [ ] **Step 3: 撰写内容寻址存储** — BLAKE3哈希 + zstd压缩
- [ ] **Step 4: 撰写魔法时刻段落** — 状态的历史比状态本身更重要
- [ ] **Step 5: 设计桥接语** — 承上 → 启下（有了状态持久化，如何选择正确的工具执行）
- [ ] **Step 6: 列出本章一手来源**

### Task 18: 第18章 — RAG-MCP动态工具检索

**文件:** `chapters/part4-runtime/ch18-rag-mcp.md`

**本章Q:** 如何解决Prompt膨胀与LLM选择瘫痪？

**魔法时刻:** RAG-MCP解决的不仅是"不知道用什么工具"，而是"在错误的时间知道错误的工具"

**代码脚手架:** RAG-MCP集成

- [ ] **Step 1: 撰写向量检索架构** — 向量数据库 × 工具语义检索
- [ ] **Step 2: 撰写动态Schema挂载** — 语义检索动态挂载Tool Schema
- [ ] **Step 3: 撰写Prompt膨胀解决方案** — 解决LLM选择瘫痪
- [ ] **Step 4: 撰写魔法时刻段落** — 错误的时间知道错误的工具
- [ ] **Step 5: 撰写开放问题** — Agent间通信的形式化验证
- [ ] **Step 6: 设计桥接语** — 承上 → 启下（有了所有基础设施，如何构建最小可用栈）
- [ ] **Step 7: 列出本章一手来源**

---

## 第五部分：生产落地

### Task 19: 第19章 — 从零构建Harness最小可用栈

**文件:** `chapters/part5-production/ch19-min-stack.md`

**本章Q:** 如何在本地跑起第一个Harness栈？

**魔法时刻:** 最小可用栈的价值不是"能用"，而是"可验证"

**代码脚手架:** Complete Stack实现（整合前四部分的代码）

- [ ] **Step 1: 撰写完整项目代码** — Mastra + Zod + WasmEdge强类型守卫
- [ ] **Step 2: 撰写AgentOutput结构体** — 代码 + 测试的完整定义
- [ ] **Step 3: 撰写消除JSON解析错误** — 具体错误类型与防御代码
- [ ] **Step 4: 撰写魔法时刻段落** — 可验证性的价值
- [ ] **Step 5: 设计桥接语** — 承上 → 启下（本地栈如何扩展为生产部署）
- [ ] **Step 6: 列出本章一手来源**

### Task 20: 第20章 — GRT+WASM生产部署实战

**文件:** `chapters/part5-production/ch20-production-deploy.md`

**本章Q:** 如何将Rust核心编译为.wasm并部署？

**魔法时刻:** 从TS到Rust到WASM，不是在构建不同功能，而是在构建不同的确定性保证

**代码脚手架:** Production Deployment

- [ ] **Step 1: 撰写cargo-component代码** — Rust核心逻辑编译为.wasm
- [ ] **Step 2: 撰写WasmEdge部署** — 零信任环境长周期任务
- [ ] **Step 3: 撰写Inngest集成** — 断点续传的完整实现
- [ ] **Step 4: 撰写魔法时刻段落** — 不同的确定性保证层级
- [ ] **Step 5: 设计桥接语** — 承上 → 启下（单一Agent如何扩展为多Agent协作）
- [ ] **Step 6: 列出本章一手来源**

### Task 21: 第21章 — Anthropic级全栈案例：引导序列设计

**文件:** `chapters/part5-production/ch21-boot-sequence.md`

**本章Q:** 如何设计一个永不崩溃的Agent Boot Sequence？

**魔法时刻:** Boot Sequence的失败不是技术失败，而是系统在告诉你"你的假设错了"

**代码脚手架:** Boot Sequence实现

- [ ] **Step 1: 撰写Boot Sequence完整流程** — Initializer → RAG-MCP → JSON List → 执行
- [ ] **Step 2: 撰写Undo Agent触发** — 失败检测与触发条件的完整代码
- [ ] **Step 3: 撰写Smoke Test** — 自愈循环的完整测试
- [ ] **Step 4: 撰写魔法时刻段落** — 失败是系统的信息
- [ ] **Step 5: 设计桥接语** — 承上 → 启下（多Agent协作时，谁对最终状态负责）
- [ ] **Step 6: 列出本章一手来源**

### Task 22: 第22章 — 多Agent协作与编排

**文件:** `chapters/part5-production/ch22-multi-agent.md`

**本章Q:** 如何从单一Agent扩展到Agent联邦？

**魔法时刻:** 多Agent协作的终极问题：谁对最终状态负责？

**代码脚手架:** MultiAgent Orchestration

- [ ] **Step 1: 撰写Agent联邦架构** — 从单一Agent到多Agent的网络拓扑图
- [ ] **Step 2: 撰写Blueprint编排** — 确定性节点 + Agentic节点的组合
- [ ] **Step 3: 撰写GRT并发模型** — Goroutine × Tokio的完整对比
- [ ] **Step 4: 撰写任务分发机制** — 多Agent任务分配的完整实现
- [ ] **Step 5: 撰写魔法时刻段落** — 谁对最终状态负责
- [ ] **Step 6: 撰写开放问题** — AI推理不确定性与业务确定性的矛盾
- [ ] **Step 7: 列出本章一手来源**

---

## 附录任务（与正文并行）

### Task 23: 附录A-E

**文件:** `chapters/appendices/app-*.md`

- [ ] **Step 1: 撰写CAR ↔ 离散事件仿真** — 理论映射与数学推导
- [ ] **Step 2: 撰写TNR ↔ STM** — 软件事务内存的理论关联
- [ ] **Step 3: 撰写类型状态 ↔ 状态机** — 可组合性的数学基础
- [ ] **Step 4: 撰写Capability ↔ 形式化安全** — Bell-LaPadula模型映射
- [ ] **Step 5: 撰写WASM ↔ 线性类型** — 线性类型理论的完整推导

---

## 章节写作顺序与依赖关系

```
第一部分（问题与原理）
     ↓
第二部分（语言层契约）← Task 3-7 可并行
     ↓
第三部分（编译器审查）← Task 8-12 可并行（Task 10依赖Task 8-9的概念）
     ↓
第四部分（运行时隔离）← Task 13-18 可并行
     ↓
第五部分（实战落地）← Task 19-22 可并行
     ↑
附录A-E（理论深潜）→ 可与正文并行
```

---

## 并行写作组

| 组别 | 任务 | 可开始条件 |
|------|------|-----------|
| 组A（第一部分） | Task 1, 2 | 无依赖 |
| 组B（第二部分） | Task 3, 4, 5, 6, 7 | 组A完成 |
| 组C（第三部分） | Task 8, 9, 11, 12 | 组B完成，Task 10在Task 8-9后 |
| 组D（第四部分） | Task 13, 14, 15, 16, 17, 18 | 组C完成 |
| 组E（第五部分） | Task 19, 20, 21, 22 | 组D完成 |
| 组F（附录） | Task 23 | 无依赖，可与任意组并行 |

---

## 写作质量检查清单

### 每章必须满足

- [ ] 本章Q已明确回答
- [ ] 魔法时刻已设计并撰写
- [ ] 五分钟摘要（2-3句话）已撰写
- [ ] 完整可运行代码块已提供
- [ ] 桥接语三要素（承上/启下/认知缺口）已设计
- [ ] 本章一手来源清单已列出
- [ ] Harness有效性矩阵相关维度已标注
- [ ] 代码脚手架增量已实现

### 整体检查

- [ ] 每章至少1张核心架构图
- [ ] 关键对比使用双栏表格
- [ ] 无"涌现"、"意识"、"魔法"等过度包装词汇
- [ ] 数据来源已验证，无未标注的二手引用
- [ ] 开放问题已在相关章节末尾直面

---

## 调研成果复用说明

**research-findings.md 中已覆盖的主题，task 中不再设置"Step 1: 互联网调研"。**

直接复用的一手来源：

| 主题 | 来源 | 所在章节 |
|------|------|---------|
| Anthropic 16 Agent | anthropic.com/engineering | ch01, ch21 |
| Stripe Minions | stripe.dev/blog | ch06 |
| Cursor Self-Driving | cursor.com/blog | ch22 |
| Peter Steinberger案例 | 公开资料 | ch22 |
| Nate B Jones Harness研究 | 研究论文 | ch01, ch09 |
| Rust+AI Agent+WASM | ITNEXT (p4.txt) | ch04, ch20 |
| GRT+WASM架构 | p3.txt | ch02, ch20 |
| Mitchell Hashimoto六阶段 | mitchellh.com | ch01, ch14 |
| OpenAI Harness | openai.com/index | ch01, ch02 |

---

## 当前状态

- [x] SPEC v2 完成
- [x] PLAN v2 完成
- [ ] 调研成果已整合至各task
- [ ] 写作执行待启动

**下一步：选择执行选项开始逐章节写作**
