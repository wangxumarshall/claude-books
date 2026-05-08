# 《Agent Harness：编程语言、编译器与运行时》写作提纲设计

## 1. 概念与愿景

**核心理念**：大模型的输出是一个"具有概率性缺陷的文本生成函数"，而Harness是驯服这个函数的确定性基座。本书揭示如何通过"语言层、编译器层、运行时层"三重牢笼，将AI的非确定性行为锁定在严格的系统边界之内。

**叙事主线**：问题驱动 × 技术架构双轨并行
> 行业真实痛点 → GRT+WASM技术方案 → 实战落地

**受众**：混合群体（AI基础设施工程师 + 框架开发者 + 高级全栈工程师），要求受众广泛可读，同时保持理论深度。

---

## 2. 核心约束

### 2.1 内容结构：三明治分层（洋葱结构）

每章采用统一的三层结构，兼顾入门读者与深度研究者：

1. **五分钟摘要**（开篇） — 用一句话 + 一张架构图讲清楚本章核心结论
2. **实践代码**（主体） — 完整的可运行代码（TS/Rust/Go），拒绝伪代码
3. **进阶理论**（收尾） — 底层原理与学术溯源，供深度读者选读

### 2.2 核心章节：螺旋上升

以下章节的概念在书中多次迭代出现，每次增加一层复杂度：

- **类型系统**：第3章（基础） → 第5章（Rust所有权） → 第6章（类型状态模式） → 第8章（跨语言对齐）
- **TNR事务性无回归**：第10章（编译器反馈回路） → 第12章（TNR形式化定义） → 第15章（WASI能力撤销）
- **Immutable DAG**：第18章（状态持久化） → 第20章（全链路观测） → 第24章（黑灯工厂）

### 2.3 反过度包装铁律

- **禁止词汇**：涌现、意识、赛博生命、智能觉醒、魔法、神奇
- **强制视角**：将LLM视为"概率性文本生成函数"
- **语调**：直白、犀利、极客风，像高级工程师做Code Review

---

## 3. 五大章节群结构

### 第一部分：范式转移（2-3章）
**主题**：从"提示词玄学"到CAR基础设施层

- 第1章：2026软件工程真相：模型是引擎，Harness是底盘
  - 大模型的工程原罪：幻觉、上下文膨胀、状态丢失
  - 为什么LangChain/LangGraph是过渡时代的玩具
  - CAR框架定义：Control / Agency / Runtime三层
  - 案例：Anthropic 16 Agent × 10万行Rust C编译器

- 第2章：终极软件栈蓝图：GRT + WASM
  - Python退场：为什么它只适合原型
  - 三层牢笼概述：语言契约 → 编译器审查 → WASM隔离
  - GRT多语言栈职责划分图

- 第*章：CAR框架学术溯源（进阶）
  - CAR ↔ 离散事件仿真理论
  - 控制论视角：Harness作为闭环反馈系统

---

### 第二部分：语言层 — 契约（8-10章）
**主题**：把AI锁死在类型系统中

- 第3章：TypeScript：动态与静态的完美防线（数据面）
  - 告别Any：Branded Types终结字符串级联编程
  - Zod + TypeChat：Schema as Code（同像性约束）
  - Tool Call路由：Vercel AI SDK类型安全管道

- 第4章：TypeScript进阶工程实践
  - Mastra框架深度：工作流编排与持久化执行
  - Zod schema `zod.infer<typeof AgentState>`实战
  - 反面教材：2023年长Prompt依赖 vs 2026年类型约束

- 第5章：Rust：Harness核心与极权内存管理（核心面）
  - 所有权与生命周期：AI无法"悄悄遗忘"Token
  - Odyssey SDK：Bundle-first架构
  - 基于Tokio的异步调度与内存印迹对比

- 第6章：Rust进阶：类型状态模式
  - `enum AgentPhase`强制状态跃迁合法性
  - `Result<T, HarnessError>`与`?`操作符
  - 错误即控制流：无法绕过的强迫性兜底

- 第7章：Go：云原生服务编排与高并发网关（控制面）
  - Goroutine与协程池：Agent路由与长时队列
  - API Gateway模式：高并发 × 低延迟
  - Go的生态位：不在Agent逻辑，而在控制平面

- 第8章：跨语言类型对齐：ts-rs / specta / Protobuf
  - Rust → TypeScript编译时100%对齐
  - Result/Option → 联合类型/条件类型映射
  - GRT栈"单点真实来源"实践

- 第*章：对比驱动：反面教材 × 正面教材
  - 2023：把所有API塞进Prompt → 模型崩溃
  - 2026：RAG-MCP动态检索Top-K契约 → 43%成功率提升

---

### 第三部分：编译器层 — 审查（6-8章）
**主题**：永不疲倦的死神Reviewer

- 第9章：编译即判别：TSC拦截流与Rustc最高法庭
  - `tsc --noEmit`：94% AI错误在类型检查阶段阻断
  - Cargo check：Rust编译通过 ≈ 内存安全大概率正确
  - 编译器作为无法贿赂的Reviewer

- 第10章：编译器反馈回路设计
  - JSON特征列表：结构化错误比Markdown更精准
  - 特征提取：剥离冗余信息，聚焦核心错误码
  - 为什么AI解析JSON远胜解析松散文本

- 第11章：TNR（事务性无回归）形式化定义与编译器层实现
  - STRATUS系统TNR理论：修复失败时状态绝不恶化
  - 事务性语义：编译单元的原子性回滚
  - 形式化定义：Precondition × Postcondition × Invariant

- 第12章：自愈循环：Critique Agent ↔ Generator Agent
  - 闭环反馈系统：编译器Error Log作为PID控制器信号
  - 多轮对抗架构：微秒级生成-评估-反思
  - 指数退避与状态快照

- 第13章：死循环检测与强制回滚
  - 同一编译错误的循环检测机制
  - Git Commit断点救援：回滚至上个通过节点
  - 人类介入触发条件

- 第*章：GAN视角：为什么编译器是最强的判别器
  - 生成器（LLM）vs 判别器（Compiler）的对抗关系
  - 类型系统作为判别损失函数

---

### 第四部分：运行时层 — 隔离（6-8章）
**主题**：WASM、MCP与零信任沙箱

- 第14章：WebAssembly：生产级Agent的数字监狱
  - Docker失败论：冷启动慢、内核面广
  - Wasmtime / WasmEdge：30MB运行时 vs 4GB Python
  - 指令级严格隔离

- 第15章：WASI与Capability-based Security
  - 剥夺默认权限：文件/Socket必须显式授予
  - 能力导向执行：消灭AI删库跑路的物理可能
  - TNR在运行时层：WASI能力撤销作为回滚原语

- 第16章：V8 Isolates / WasmEdge：毫秒级实战数据
  - Cloudflare Dynamic Workers：毫秒级冷启动
  - 内存占用是Docker的1/100
  - GPU穿透：GGML + Llama本地推理

- 第17章：MCP-SandboxScan：网络与文件系统阻断
  - 不受信MCP工具的WASM隔离
  - 毫秒级冷启动 × 网络零连通
  - 提示词注入拦截实战

- 第18章：状态持久化：Immutable DAG与内容寻址存储
  - Raw / Analyzed / Lowered三阶段AST处理
  - BLAKE3哈希 + zstd压缩的内容寻址
  - 不可变状态：分支重试无副作用污染

- 第19章：RAG-MCP：语义检索动态挂载Tool Schema
  - 向量数据库 × 工具语义检索
  - 13% → 43%成功率提升的量化支撑
  - 解决Prompt膨胀与LLM选择瘫痪

- 第20章：全链路观测：OpenTelemetry + Immutable DAG
  - 100%确定性重放（Deterministic Replay）
  - 不可变执行日志 × 分布式追踪
  - 毫秒级故障根因分析

---

### 第五部分：实战落地（4-6章）
**主题**：从零手搓2026生产就绪栈

- 第21章：起步（TypeScript篇）
  - Mastra + Zod + TypeChat强类型守卫
  - 构建AgentOutput结构体（代码 + 测试）
  - 消除JSON解析错误

- 第22章：进阶（Rust + WASM篇）
  - cargo-component：Rust核心逻辑编译为.wasm
  - WasmEdge部署：零信任环境长周期任务
  - Inngest断点续传集成

- 第23章：极致（Anthropic级全栈篇）
  - Boot Sequence全流程：Initializer → RAG-MCP → JSON List → 执行
  - Undo Agent触发条件
  - Smoke Test自愈循环

- 第24章：StrongDM黑灯工厂
  - 场景验证：端到端User Story作为Holdout Sets
  - 数字孪生宇宙：Okta/Slack高保真模拟
  - Leash零信任策略引擎：动态身份 × 微隔离

- 第*章：多Agent协作：GRT栈并发编排
  - 从单一Agent到Agent联邦
  - Goroutine × Tokio的并发模型对比

---

### 附录（理论深潜）

- 附录A：CAR框架 ↔ 离散事件仿真理论
- 附录B：TNR ↔ 软件事务内存（STM）
- 附录C：类型状态模式 ↔ 状态机可组合性
- 附录D：Capability Security ↔ 形式化安全验证（Bell-LaPadula模型）
- 附录E：WASM内存模型 ↔ 线性类型理论

---

## 4. 写作质量规范

### 4.1 代码要求

| 语言 | 必须展示的内容 |
|------|---------------|
| TypeScript | 泛型、Zod Schema `zod.infer`、Mastra工作流、Branded Types |
| Rust | 生命周期、所有权、`Result<T, HarnessError>`、`enum AgentPhase`、宏使用 |
| Go | Goroutine、Channel、Context超时控制 |
| WASM | wasm-bindgen、Rust编译为.wasm、WASI权限声明 |

### 4.2 图表规范

- 每章至少1张核心架构图（ASCII或Mermaid）
- 关键对比使用双栏表格（反面教材 vs 正面教材）
- 流程图必须标注数据流向与边界条件
- 数据支撑必须量化（冷启动毫秒数、内存占用比例、成功率%）

### 4.3 引用与来源

- Anthropic 16 Agent实验：原始论文/博客引用
- StrongDM黑灯工厂：公开演讲/技术博客引用
- 技术数据（94%错误率、V8 Isolates性能）：2026年实测数据或官方benchmark
- 避免二手引用：优先一手来源（官网、原始论文、GitHub README）

---

## 5. 成功标准

1. **可读性**：入门读者读完第1-3章能理解Harness的基本概念
2. **可动手**：读完第21-22章能在本地跑起Mastra + Zod + WasmEdge的最小可用栈
3. **可设计**：读完第9-12章能独立设计一个带TNR保证的编译器反馈回路
4. **可论证**：学术读者读完附录能理解Harness的理论根基

---

## 6. 当前状态

**输入素材**：
- `p1.md` — CAR框架、TNR、MCP-SandboxScan、RAG-MCP重构提纲
- `p2.md` — 控制论视角、类型状态模式、Capability-based Security重构提纲
- `p3.txt` — GRT+WASM全景架构深度解析（2026年版）

**待办**：
- 拆分30-40章写作任务
- 分配章节优先级与依赖关系
- 制定写作顺序与并行策略
