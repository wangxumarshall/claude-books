# POPL 2026 洞察报告（系统软件相关论文）

> **会议信息**：POPL 2026 (ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages)，CCF-A 类会议，2026 年 1 月举办。
> **报告定位**：聚焦与系统软件（编译器、操作系统、运行时、并发系统）直接相关的 PL 研究，覆盖编译器验证、类型系统、分离逻辑、程序综合、概率程序分析等方向，遴选 11 篇代表性论文进行深度解读。

---

## 0. 会议概览

POPL（Principles of Programming Languages）是编程语言领域历史最悠久、学术地位最高的国际会议，与 PLDI、OOPSLA 并称 PL 三大顶会。POPL 2026 延续了其对编程语言理论基础与形式化方法的高度关注，同时呈现出以下几个显著趋势：

1. **Rust 成为系统编程语言形式化验证的核心载体**。今年有两篇直接与 Rust 相关的论文（Miri UB 检测、TypeDis 中关于 MaPLe/Rust 风格并行编程的类型系统），以及多篇关于 ownership/substructural type systems 的论文可间接服务于 Rust 验证。
2. **分离逻辑的泛化与下沉**。从传统的内存分离逻辑扩展到概率分离逻辑（BaSL）、并行确定性分离逻辑（Musketeer/Angelic），表明分离逻辑正成为通用程序验证的基础设施。
3. **并发与并行验证进入精细化阶段**。不再满足于"正确与否"，而是关注内部确定性、disentanglement、message-passing 复杂度等更细粒度的性质。
4. **概率程序分析与验证全面开花**。概率程序的定量分析（piecewise bounds via k-induction）和定性验证（BaSL）均有突破。
5. **类型系统的跨界创新**。linear types 进入惰性语言（Linear Core for GHC）、strictness 类型化、incorrectness typing 的类型补操作——类型理论持续向新的应用领域渗透。

以下按主题分类，逐一解读各论文的核心贡献与系统相关性。

---

## 1. 系统代码安全与未定义行为检测

### 1.1 Miri: Practical Undefined Behavior Detection for Rust

> **作者**：Ralf Jung (ETH Zurich) 等
> **论文页**：https://plf.inf.ethz.ch/research/popl26-miri.html
> **关键词**：Rust, Undefined Behavior, MIR Interpreter, Stacked Borrows, Tree Borrows

**核心贡献**：Miri 是 Rust 生态中最核心的未定义行为（UB）检测工具，该论文总结了 Miri 在过去三年中的重大进展，标志着其在学术和实践上的双重里程碑。

**技术亮点**：
- **系统调用模拟（Shims）**：大幅扩展了对 Windows、Linux、macOS、Android 等平台的 API 支持，使得 Miri 可以在解释器中模拟完整的系统调用路径，而不仅限于纯 Rust 代码。
- **硬件指令集模拟**：新增 Intel AVX-512 等 SIMD 指令集的模拟支持，使得使用 SIMD intrinsics 的 unsafe 代码也能接受 UB 检测。
- **别名模型演进**：从 Stacked Borrows 到 Tree Borrows 的别名分析模型，Tree Borrows 在许多真实场景下更宽松、误报更少。
- **C++20 并发语义**：引入全非确定性调度器，实验性集成 GenMC 模型检查器，支持穷举并发程序的执行状态。
- **诊断增强**：精准追踪数据竞争、Use-After-Free、借用违规的根源，提供可操作的错误报告。

**系统相关性**：Miri 是 Rust for Linux、Bun runtime、zlib-rs 等重大系统项目的核心安全网。随着 Linux 内核正式接纳 Rust（2025 年底移除"实验性"标签），Miri 作为 unsafe Rust 的事实标准验证工具，其重要性将进一步提升。

---

### 1.2 Lazy Linearity for a Core Functional Language

> **作者**：Rodrigo Mesquita, Bernardo Toninho (Universidade Nova de Lisboa)
> **arXiv**：2511.10361
> **DOI**：10.1145/3776702
> **关键词**：Linear Types, Lazy Evaluation, GHC Core, Compiler Optimization

**核心贡献**：提出 **Linear Core**——一种适用于惰性函数式语言的新型线性类型系统，突破了传统线性类型中"语法出现即消费"的假设，在语义层面定义线性资源的使用。

**技术亮点**：
- **惰性语义中的线性**：在非严格求值（lazy evaluation）下，变量的语法出现并不必然意味着运行时使用。Linear Core 接受这一语义差异，在静态层面仍保证线性资源使用。
- **GHC 优化兼容性**：证明了 GHC 的多个优化变换（如内联、let-floating）在 Linear Core 中保持线性，而这些优化在 GHC 原有的 Core 语言中会破坏线性。
- **编译器插件实现**：将 Linear Core 实现为 GHC 编译器插件，在 `linear-base` 等重度使用 linear types 的库上验证了系统的有效性。

**系统相关性**：GHC 是 Haskell 的主力编译器，也是许多工业系统（如 Facebook 的 Sigma/Haxl）的底层基础设施。Linear Core 使得 linear types 在 GHC 的优化管道中不再被破坏，对于在 Haskell 中安全使用线性资源（文件句柄、socket、内存缓冲区等）至关重要。

---

### 1.3 A Complementary Approach to Incorrectness Typing

> **作者**：Celia Mengyue Li, Sophie Pull, Steven Ramsay (University of Bristol)
> **arXiv**：2510.13725
> **关键词**：Incorrectness Logic, Type System, Complement Types, Erlang

**核心贡献**：提出一种新型的**双向（two-sided）类型系统**，可同时验证程序的正确性（correctness）和错误性（incorrectness）。关键创新是引入了**类型的补操作（complement）**，充当类型公式的否定。

**技术亮点**：
- **Normal Form Typing**：类型基于范式集（sets of normal forms）而非值集，这使得补操作在类型层面自然成立。
- **补操作公理化**：通过子类型（subtyping）对补操作进行表达性公理化，证明该公理化是可判定的（decidable）。
- **Erlang 风格程序验证**：使用该系统验证了多个 Erlang 风格的并发程序中确实会"出错"（go wrong），包括模式匹配失败等典型错误。
- **完备性**：不仅证明了类型系统的可靠性（soundness），还证明了对范式是完备的（complete）。

**系统相关性**：Erlang/Elixir 是电信系统和分布式系统中的主流语言。能够在类型层面同时表达"程序应做什么"和"程序不应做什么"，对于容错系统、监控系统的行为规约具有直接应用价值。

---

## 2. 并发与并行程序的形式化验证

### 2.1 All for One and One for All: Program Logics for Exploiting Internal Determinism in Parallel Programs

> **作者**：Alexandre Moine, Sam Westrick, Joseph Tassarotti (New York University)
> **arXiv**：2511.23283
> **DOI**：10.1145/3776668
> **关键词**：Internal Determinism, Separation Logic, Parallel Programs, Iris, Rocq

**核心贡献**：首次为**内部确定性并行程序（internally deterministic parallel programs）**建立了完整的验证框架，包含两个新逻辑：**Musketeer** 和 **Angelic**。

**技术亮点**：
- **Schedule-Independent Safety**：定义了一个核心性质——如果一个并行程序在一次终止执行中是安全的，那么它在所有调度下都是安全的。
- **Musketeer 逻辑**：用于证明程序满足 schedule-independent safety，基于 Iris 分离逻辑框架，所有证明在 Rocq 中机械化。
- **Angelic 逻辑**：一旦 Musketeer 证明程序满足 schedule-independent safety，Angelic 允许验证者**动态选择一个顺序执行路径**进行验证，大幅降低验证工作量。
- **MiniDet 类型系统**：基于 Musketeer 证明了一个仿射类型系统（affine type system）的可靠性。任何语法上类型正确的 MiniDet 程序自动满足 schedule-independent safety，可直接使用 Angelic 验证。
- **并发哈希集案例**：展示了并行确定性版本的并发哈希集等原语的验证。

**系统相关性**：Fork-join 并行是高性能计算和系统编程的基本范式（如 Cilk、Rayon）。该工作为这类系统的形式化验证提供了理论基础，使得验证并行程序不再需要穷举所有交错。

---

### 2.2 TypeDis: A Type System for Disentanglement

> **作者**：Alexandre Moine (NYU), Stephanie Balzer (CMU), Alex Xu (CMU), Sam Westrick (NYU)
> **arXiv**：2511.23358
> **DOI**：10.1145/3776655
> **关键词**：Disentanglement, Parallelism, Type System, Region Types, Memory Management

**核心贡献**：提出 **TypeDis**——首个自动验证并行程序**解缠性（disentanglement）**的类型系统。Disentanglement 是保证并行任务可独立、无同步地进行垃圾回收的关键性质。

**技术亮点**：
- **时间戳标注类型**：每个类型被标注一个时间戳（timestamp），标识分配该对象的并行任务。时间戳在 join 点和通过"子时序化（subtiming）"子类型关系可变化。
- **Iso-Recursive Types & Polymorphism**：支持 iso-recursive 类型以及类型和时间戳上的多态。
- **Subtiming 子类型**：允许时间戳在类型检查时变化，这是一个关键创新，使得 join 点的时间戳合并变得简洁。
- **全机械化证明**：在 Rocq 中使用改进版 DisLog2 对所有结果进行了形式化证明。
- **MaPLe 编译器基础**：TypeDis 为 MaPLe 编译器中任务局部（task-local）内存管理提供静态保证。

**系统相关性**：并行垃圾回收的同步开销是高性能系统的关键瓶颈。Disentanglement 使得 GC 完全并行化、无需全局同步，这在 MaPLe 中已获得实际性能收益。TypeDis 将该性质的证明从手动的、专家级别的分离逻辑证明降低为自动类型检查，极大降低了使用门槛。

---

### 2.3 The Complexity of Testing Message-Passing Concurrency

> **作者**：Zheng Shi, Lasse Møldrup, Umang Mathur, Andreas Pavlogiannis
> **arXiv**：2505.05162
> **关键词**：Message-Passing, Channel, Concurrency Testing, Complexity, Go, Rust, Kotlin

**核心贡献**：首次系统性地研究了基于**通道（channel）的消息传递并发**的测试复杂度，建立了完整的复杂度图谱。

**技术亮点**：
- **Channel Consistency Problem**：定义了通道一致性问题的形式化框架——给定部分执行历史，是否存在一个一致的程序完成方式？
- **完整复杂度图谱**：考虑了线程数、通道数、通道容量等因素，给出了多项式上界和 NP-hard 下界的完整刻画。
- **固定参数多项式算法**：当某些参数固定时（如通道容量为 1 或有界），给出多项式时间算法。
- **最优性证明**：证明了所给算法在特定参数下是（近）最优的。

**系统相关性**：Go、Rust (Tokio)、Kotlin (coroutines) 等现代系统编程语言广泛采用通道作为并发原语。该工作为通道并发程序的自动化测试和验证工具的设计提供了理论基础和复杂度下界，对构建 Channel Fuzzer 或 Concurrency Bug Finder 具有直接指导意义。

---

## 3. 概率程序分析与验证

### 3.1 Bayesian Separation Logic (BaSL)

> **作者**：Shing Hin Ho, Nicolas Wu, Azalea Raad (Imperial College London)
> **arXiv**：2507.15530
> **关键词**：Bayesian Programming, Separation Logic, Probabilistic Independence, Measure Theory

**核心贡献**：提出 **BaSL**——首个能够处理贝叶斯更新（Bayesian updating）的概率分离逻辑，为贝叶斯概率编程语言（BPPL）提供模块化程序逻辑。

**技术亮点**：
- **内部贝叶斯定理**：利用测度论中的 Rokhlin-Simmons 分解定理，在分离逻辑内部证明了贝叶斯定理，使得 Bayesian updating 可直接在 Hoare 三元组中推理。
- **Kripke 资源幺半群**：基于 Hilbert 立方体上的 σ-有限测度空间，给出新颖的 Kripke 语义模型。
- **分离合取 = 概率独立**：延续 PSL 和 Lilac 的传统，将分离合取解释为随机变量的概率独立性，同时将 frame rule 扩展至贝叶斯更新场景。
- **建模能力**：支持 unnormalised distribution、conditional distribution、soft constraint、conjugate prior、improper prior 等高级概率编程概念。
- **案例验证**：使用 BaSL 证明了 Bayesian coin flip 期望值、collider Bayesian network 中随机变量的相关性、burglar alarm 模型的后验分布、参数估计算法、Gaussian mixture model 等统计模型的正确性。

**系统相关性**：概率编程正日益应用于推荐系统、量化金融、机器人感知等实际系统。BaSL 为这些系统的正确性推理提供了模块化的理论基础，使得可以局部地推理概率模型的各组成部分，而非需要全局分析。

---

### 3.2 Piecewise Analysis of Probabilistic Programs via k-Induction

> **作者**：Tengshun Yang (ISCAS), Shenghua Feng (ISCAS), Hongfei Fu (SJTU), Naijun Zhan (PKU), Jingyu Ke (SJTU), Shiyang Wu (SJTU)
> **arXiv**：2403.17567v2
> **关键词**：Probabilistic Program Analysis, k-Induction, Piecewise Bounds, Semidefinite Programming

**核心贡献**：提出一种**分段定量分析（piecewise quantitative analysis）**方法，通过格化的 k-归纳（latticed k-induction）自动推导概率程序的分段数值界。

**技术亮点**：
- **分段界 vs. 整体界**：传统的概率程序定量分析只推导全局/整体界（monolithic bounds），要么太保守、要么不够简洁。分段界更精确且更简洁。
- **Optional Stopping Theorem 的巧妙应用**：将分段信息与 Optional Stopping Theorem 结合，为概率程序的分段期望值/概率界推导提供了一般性框架。
- **双线性规划化简**：在线性情况下将分段多项式界的合成归约为双线性规划（bilinear programming）；在多项式情况下松弛为半定规划（semidefinite programming）。
- **实验验证**：在多种 benchmark 上生成比现有方法更紧的分段界。

**系统相关性**：概率程序广泛用于随机算法（如 randomized quicksort）、机器学习推理管线、可靠性工程等系统场景。自动推导紧的定量界对于这些系统的资源规划（如内存、延迟的尾部界）和 SLA 保障至关重要。

---

## 4. 类型系统理论与实现

### 4.1 Typing Strictness

> **作者**：Daniel Sainati, Joseph W. Cutler, Benjamin C. Pierce, Stephanie Weirich (University of Pennsylvania)
> **arXiv**：2510.16133
> **关键词**：Strictness Analysis, Type Systems, Call-by-Name, Call-by-Push-Value, Logical Relations

**核心贡献**：重新定义严格性（strictness）概念，建立了基于类型理论的严格性分析框架，同时适用于 call-by-name 和 call-by-push-value。

**技术亮点**：
- **精化严格性定义**：不同于传统"函数是否求值其参数"的二元定义，新定义更精确地描述变量的使用方式。
- **双语言设置**：在 call-by-name 和 call-by-push-value 两种求值策略下分别给出类型系统，并提供保持严格性标注的 CBN→CBPV 翻译。
- **逻辑关系证明**：通过逻辑关系（logical relations）证明类型系统计算的严格性属性准确描述了运行时的变量使用。
- **全 Rocq 机械化**：所有结果在 Rocq 中完全机械化。

**系统相关性**：严格性分析是惰性函数式语言（如 Haskell）编译器中关键的性能优化手段，直接影响程序的空间和时间效率。该工作为将严格性分析建立于坚实的类型理论基础之上，对编译器优化通道的设计具有长远影响。

---

### 4.2 The Relative Monadic Metalanguage

> **作者**：Jack Liell-Cock, Zev Shirazi, Sam Staton (University of Oxford)
> **arXiv**：2512.11762
> **DOI**：10.1145/3776702
> **关键词**：Relative Monads, Graded Monads, Arrow Calculus, Category Theory, Semantics

**核心贡献**：将单子元语言（monadic metalanguage）推广到相对单子（relative monads）设定，统一了 graded monads 和 arrow calculus 的语义框架。

**技术亮点**：
- **相对单子元语言**：将 Moggi 的经典 monadic metalanguage 推广到相对单子，给出完整语义。
- **LNL-RMM**：提出用于 graded monads 的线性-非线性语言，证明它是 graded monadic metalanguage 的保守扩展。
- **ARMM**：提出用于 arrows 的计算 λ-calculus 风格语言，证明它是 arrow calculus 的保守扩展。
- **统一框架**：展示了 graded monads 和 arrows 是相对单子元语言的特例。

**系统相关性**：Graded monads 用于追踪效应的细粒度信息（如追踪 IO 操作的安全级别），arrows 是 Haskell 中结构化计算的核心抽象（如 stream processing libraries）。该工作为这些实践中广泛使用的抽象提供了更坚实的语义基础。

---

### 4.3 Handling Higher-Order Effectful Operations with Judgemental Monadic Laws

> **作者**：Zhixuan Yang, Nicolas Wu (Imperial College London)
> **arXiv**：2511.05739
> **关键词**：Algebraic Effects, Handlers, Higher-Order Effects, Judgemental Equality, Realizability

**核心贡献**：提出一个新的核心演算，处理高阶效应操作（higher-order effectful operations），其中处理器（handlers）由无法律的原始单子（lawless raw monads）承载，但计算判断在判断层面仍满足单子律。

**技术亮点**：
- **高阶效应操作**：支持以计算为参数/返回值的效应操作（如 `catch`、`callCC` 等）。
- **判断式单子律**：核心设计选择——处理器由原始单子承载（无需满足单子律），但计算判断层面 judgementally 满足单子律。
- **可实现性语义**：使用 realizability semantics 给出指标模型。
- **Closed-Term Canonicity & Parametricity**：对于无递归片段的语言，证明了闭项规范性和参数性。

**系统相关性**：代数效应与处理器是结构化并发（如 structured concurrency with `async`/`await`）、异常处理、非确定性等系统编程模式的通用抽象。该工作为这些系统特性提供了更灵活的类型理论基础——处理器可以在内部使用不满足单子律的表示，但对程序员暴露的接口保持良行为。

---

## 5. 结语与未来方向

### 5.1 趋势总结

POPL 2026 的系统相关论文展现了以下关键趋势：

| 趋势 | 代表性论文 | 对系统领域的影响 |
|------|-----------|----------------|
| **Rust/unsafe 的形式化保障** | Miri | 为 Rust for Linux 等底层系统项目提供 UB 检测基础设施 |
| **线性/子结构类型进入惰性语言** | Linear Core | GHC 编译器中 linear types 的优化安全 |
| **并行验证的降维打击** | Musketeer/Angelic, TypeDis | 将并行程序验证从状态空间爆炸中解放 |
| **通道并发的复杂度奠基** | Channel Complexity | 为 Go/Rust 并发测试工具提供理论界限 |
| **概率编程的模块化推理** | BaSL, k-Induction | 统计模型在系统中的可信部署 |
| **类型系统的跨界创新** | Strictness Typing, Incorrectness Typing, Relative Monads | 编译器优化、错误检测、效应追踪的理论基础 |

### 5.2 未来值得关注的方向

1. **Rust 验证的工业化**：Miri 的成功表明，形式化工具可以进入主流系统开发工作流。下一个目标是降低证明负担——将 Iris/Coq 级别的证明能力下沉到自动化为类型检查（TypeDis 已迈出重要一步）。
2. **概率编程与系统可靠性工程的融合**：BaSL 和 piecewise analysis 为在概率系统中进行模块化正确性推理铺平了道路。随着自动驾驶、量化交易等系统的可靠性需求增长，这些技术的工程化将加速。
3. **编译器中间表示的类型安全保障**：Linear Core 和 Typing Strictness 都展示了在编译器 IR 层面嵌入强类型安全性的价值。这一方向有望在更多编译器（如 MLIR、Cranelift）中得到应用。
4. **通道/消息传递并发理论到工具的转化**：The Complexity of Testing Message-Passing Concurrency 给出了理论复杂度边界，接下来需要的是将这些理论转化为实际可用的 Go/Rust 并发测试工具。

### 5.3 中国力量

值得注意的是，今年 POPL 有多篇来自中国研究机构的论文：
- 上海交通大学的 **Hongfei Fu** 团队（Piecewise Analysis via k-Induction）
- 中国科学院软件研究所的 **Tengshun Yang、Shenghua Feng** 以及北京大学的 **Naijun Zhan** 均参与了上述工作
- 上海交通大学的 **Yuting Wang** 团队虽未在本届正式发表（RustCompCert 已投稿至 Rust Verify 2026），但持续在 verified compilation 方向深耕

这表明中国在编程语言理论前沿的研究影响力持续增强。

---

## 论文索引表

| # | 论文标题 | 作者 | arXiv/DOI | 主题分类 |
|---|---------|------|-----------|---------|
| 1 | Miri: Practical Undefined Behavior Detection for Rust | Ralf Jung et al. | [plf.inf.ethz.ch](https://plf.inf.ethz.ch/research/popl26-miri.html) | Rust UB 检测 |
| 2 | Lazy Linearity for a Core Functional Language | Mesquita, Toninho | [2511.10361](https://arxiv.org/abs/2511.10361) | 线性类型 / GHC |
| 3 | A Complementary Approach to Incorrectness Typing | Li, Pull, Ramsay | [2510.13725](https://arxiv.org/abs/2510.13725) | 类型系统 / 错误检测 |
| 4 | All for One and One for All (Musketeer/Angelic) | Moine, Westrick, Tassarotti | [2511.23283](https://arxiv.org/abs/2511.23283) | 并行验证 / 分离逻辑 |
| 5 | TypeDis: A Type System for Disentanglement | Moine, Balzer, Xu, Westrick | [2511.23358](https://arxiv.org/abs/2511.23358) | 并行类型系统 |
| 6 | The Complexity of Testing Message-Passing Concurrency | Shi, Møldrup, Mathur, Pavlogiannis | [2505.05162](https://arxiv.org/abs/2505.05162) | 通道并发 / 测试复杂度 |
| 7 | Bayesian Separation Logic (BaSL) | Ho, Wu, Raad | [2507.15530](https://arxiv.org/abs/2507.15530) | 概率分离逻辑 |
| 8 | Piecewise Analysis of Probabilistic Programs via k-Induction | Yang, Feng, Fu, Zhan, Ke, Wu | [2403.17567](https://arxiv.org/abs/2403.17567) | 概率程序分析 |
| 9 | Typing Strictness | Sainati, Cutler, Pierce, Weirich | [2510.16133](https://arxiv.org/abs/2510.16133) | 严格性类型系统 |
| 10 | The Relative Monadic Metalanguage | Liell-Cock, Shirazi, Staton | [2512.11762](https://arxiv.org/abs/2512.11762) | 单子 / 箭头语义 |
| 11 | Handling Higher-Order Effectful Operations with Judgemental Monadic Laws | Yang, Wu | [2511.05739](https://arxiv.org/abs/2511.05739) | 代数效应 / 处理器 |

---

*报告生成日期：2026-06-10*
*本报告由自动文献调研系统生成，论文信息基于 arXiv 和 POPL 2026 官方网站公开数据。*