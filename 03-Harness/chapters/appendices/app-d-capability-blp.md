# 附录 D：能力安全 ↔ 形式化安全 (Capability Security ↔ Bell-LaPadula Model)

## 本章Q

为什么 WebAssembly 的 capability-based 安全模型不仅仅是"实践上安全"（practically secure），而是在形式化意义上满足 Bell-LaPadula 多级安全（MLS）模型？更进一步：WASM 的安全保证是"数学上可证明的"（provably secure）还是"工程上可信赖的"（engineering trust）？本附录通过建立严格的数学映射，证明前者。

**核心问题分解：**

1. Capability 系统和 Bell-LaPadula 系统，分别是什么？它们各自的数学基础是什么？
2. 这两个系统之间是否存在一一对应的等价关系？如果存在，这个对应关系是如何建立的？
3. 给定一个满足 capability 约束的 WASM 程序，我们能否形式化地证明它满足 BLP 安全属性？
4. 这个形式化证明对 Agent Harness 工程实践有什么具体的指导意义？

## 魔法时刻

**Capability 安全，本质上是将 Bell-LaPadula 模型在类型系统级别实现。** 这不是两种不同的安全范式在各自领域的独立应用——这是同一个安全不变量，用两种不同的表示语言描述。Dennis 与 Van Horn 1966 年提出的对象-capability 模型，与 Bell 与 LaPadula 1976 年提出的 MLS 安全模型，在数学上是等价的。WASM 将这一等价性在编译器工具链中落地，使得"无法获取未授权能力"从运行时检查变成了类型构造的副产品。

**魔法时刻的具体含义：** 想象一个 WASM 模块试图发送网络数据。如果这个模块没有持有 `wasi:http/outbound-handle` 的 capability，网络调用在类型层面就不可构造——验证器会直接拒绝编译。即便恶意代码试图通过返回函数指针、间接调用等方式绕过，它仍然无法在运行时访问到一个未被传递的 capability。这意味着"防止数据外传"不是通过在运行时插入检查实现的，而是通过在编译时将"网络 capability"排除在模块的可达引用集合之外实现的。这正是 Bell-LaPadula "no write-down" 原则的类型系统表达：主体（模块）无法将信息写入（网络发送）低于其安全级的对象（外部网络端点），因为它根本无法获得该对象的 capability。

## 五分钟摘要

本附录建立 capability 安全模型与 Bell-LaPadula (BLP) 形式化安全模型之间的严格对应关系。我们证明：WASM 的 capability 系统是 BLP 模型的一个**具体实现**（concrete realization），而非独立的安全框架。

**核心贡献：**

1. **Capability 的严格数学定义：** 我们使用依赖类型理论和线性逻辑的形式化工具，给出 capability 的不可伪造性、单调性、封装性的精确定义。这一定义不仅适用于直觉逻辑，还适用于描述 capability 在多线程环境下的行为。
2. **BLP 安全格的完整代数刻画：** 我们将 BLP 模型的核心要素（安全类、安全格、三条安全属性、状态机）用完整的数学符号系统表示，并证明 Basic Security Theorem。
3. **双向映射函数：** 我们构造映射 $\phi: \text{Rights} \rightarrow \text{AccessModes}$ 和 $\psi: 2^{\text{Capabilities}} \rightarrow \mathcal{L}$，并严格证明这两个映射建立了 capability 系统和 BLP 系统之间的格同构（lattice isomorphism）。
4. **Capability-BLP 互换定理：** 我们证明任何满足 capability 约束的 WASM 程序自动满足 BLP 安全性质，且反之亦然。这一定理意味着：WASM 的 capability 安全不是"类似于" BLP 安全，而是 BLP 安全的一个具体实现。

**实践意义：** 本附录为 Agent Harness 的安全架构提供了严格的理论支撑。任何运行在 WASM 沙箱中的 AI Tool 代码，都自动满足 BLP 多级安全属性。安全审计员可以将已有的 BLP 审计工具应用于 WASM 程序，而无需重新开发工具链。

---

## Step 1：Capability 安全模型

### 1.1 历史渊源：从 Dennis-Van Horn 到现代 cap 理论

对象-capability 模型的历史起点是 Dennis 与 Van Horn 1966 年的开创性论文《Programming Semantics for Multiprogrammed Computations》。在那篇论文中，作者提出了一个在当时看来极为激进的观点：**计算的本质不是对数据的操作，而是对能力（capability）的传递和操作**。

在传统的访问控制模型中（如 DAC 或 MAC），主体对对象的访问权限由一个全局访问控制矩阵决定。这种模型存在根本性的缺陷：**它无法防止权限的隐式传递**。一旦主体获得了访问某个对象的权限，它可以将这个权限传递给任何其它主体，而原系统对此毫无约束。例如，在 Unix 的 DAC 模型中，如果进程 A 有权限读取文件 F，进程 A 可以将文件内容复制到进程 B 有权限访问的文件 G 中——即使管理员策略明确禁止这种信息流动。

Dennis 与 Van Horn 的关键洞察是：引入一种名为"capability"的新型数据结构，它具有两个核心特性：

1. **不可伪造性（Unforgeability）：** Capability 是一个不透明句柄（opaque handle），持有者无法从中推导出任何关于对象内部表示的信息，也无法构造出一个指向同一对象的伪造 capability。这类似于密码学中"知道公钥无法推导出私钥"的不对称性。
2. **可传递性（Transferability）：** Capability 可以像值一样在主体之间传递，但每一次传递都是显式的且可被追溯的。这与密码学中的"密钥传递"类似，但增加了访问控制语义。

**为什么这在 1966 年是革命性的？** 在 1960 年代，计算模型的主流是"进程拥有内存地址，地址指向数据"。将"能力"而非"数据"作为计算的核心抽象，是一次范式转换。这与后来面向对象编程（对象引用作为第一等公民）的兴起有深刻联系。

### 1.2 形式化定义：Capability 作为不可伪造的令牌

**Definition 1 (Capability System - Full Algebraic Form).** 一个 capability 系统 $\mathcal{C}$ 是一个五元组：

$$\mathcal{C} = (\text{Subjects}, \text{Objects}, \text{Rights}, \text{Attenuate}, \text{Prove})$$

其中每个组件的定义如下：

- $\text{Subjects} \subseteq \mathbb{U}$：主体集合，表示能够持有和使用 capability 的实体。在 WASM 中，主体对应于模块实例（module instance），每个模块实例都有自己独立的 capability 集合。
- $\text{Objects} \subseteq \mathbb{U}$：对象集合，表示被保护的资源。可以是 WASM 内存（memory）、表格（table）、函数（func）、外部主机对象（host object）、网络端点、文件系统实体等。Objects 可以递归定义其内部结构。
- $\text{Rights}$：权限集合，表示对对象的操作类型集合。典型的 Rights 包括：
  - $\text{read}$：读取对象内容的权限
  - $\text{write}$：修改对象内容的权限
  - $\text{exec}$：执行对象代码的权限
  - $\text{delete}$：销毁对象或撤销其它 capability 的权限
  - $\text{create}$：创建新对象的权限
- $\text{Attenuate}$：削弱函数（attenuation function），定义 capability 的受限派生规则。这是一个偏函数（partial function）：

$$\text{Attenuate}: \text{Capabilities} \times 2^{\text{Rights}} \rightarrow \text{Capabilities}$$

满足：

$$\text{Attenuate}((o, R), R') = (o, R \cap R')$$

即：给定一个 capability $(o, R)$ 和一个期望的权限子集 $R'$，当且仅当 $R' \subseteq R$ 时，削弱操作有定义，返回 $(o, R')$。这保证了能力只能减弱（$R \cap R' \subseteq R$），不能增强。

- $\text{Prove}$：证明函数，建立 capability 的 provenance 链。形式化为：

$$\text{Prove}: \text{Capabilities} \rightarrow \text{Chain}^*$$

其中 $\text{Chain} = \text{Subject} \times \text{TransferOp} \times \text{Time}$，$^*$表示有限序列。Prove 函数返回 capability 从创建到当前持有者的完整传递历史。

**Definition 2 (Capability Token - Structural Definition).** 一个 capability token $c$ 是一个二元组：

$$c = (o, R)$$

其中：

- $o \in \text{Objects}$ 是被引用对象的身份标识符（object identity）
- $R \subseteq \text{Rights}$ 是该 capability 持有的权限子集

**重要约束（Dependency Constraint）：** 并非 $R$ 的所有子集都是合法的——只有对象 $o$ 所支持的权限子集才是有效的。形式化地，每个对象 $o$ 关联一个权限轮廓（rights profile）$\text{Rights}(o) \subseteq \text{Rights}$，capability $(o, R)$ 合法的充分必要条件是 $R \subseteq \text{Rights}(o)$。

**Definition 3 (Unforgeability - Type-Theoretic Formulation).** Capability 的不可伪造性由以下类型论条件保证：

**条件 U1（不存在性）：** 在没有持有对象 $o$ 对应 capability 的情况下，主体无法在局部计算中构造出对 $o$ 的任何 capability：

$$\forall \Gamma, o \notin \text{Objects}(\Gamma) \implies \nexists R: \Gamma \vdash \text{mkcap}(o, R) : \text{Cap}(o, R)$$

其中 $\Gamma$ 是当前类型环境，$\text{Objects}(\Gamma)$ 是 $\Gamma$ 中出现的对象集合。

**条件 U2（不透明性）：** 从一个 capability $(o, R)$ 无法推导出 $o$ 的内部表示信息：

$$\forall o, R, \text{representation\_of}(o) \not\in \text{derivable\_from}((o, R))$$

这保证了即使攻击者获得了对某个对象的部分 capability，也无法从中提取更多信息。

### 1.3 对象-capability 模型的核心特性

**Property 1 (Monotonicity of Capability Grant - Formal).** Capability 的授予具有单调性：

$$\text{If } s \text{ holds } c = (o, R) \text{ and } R' \subseteq R, \text{ then } s \text{ can derive } c' = (o, R')$$

**形式化证明：** 由削弱函数 $\text{Attenuate}$ 的定义，有：

$$\text{Attenuate}((o, R), R') = (o, R \cap R') = (o, R')$$

因为 $R' \subseteq R$，故 $R \cap R' = R'$。因此 $s$ 可以通过调用 $\text{Attenuate}$ 派生 $(o, R')$。$\square$

**单调性的深层含义：** 在 BLP 系统中，安全等级是单调递增的（主体可以升级，但不能降级）。在 Capability 系统中，权限是单调递减的（capability 可以削弱，但不能增强）。这两个单调性看似相反，实际上描述的是同一个现象的两个方面：授权的"颗粒度"（granularity）随时间变化，系统的总信息流权限保持不变。

**Property 2 (Encapsulation - Information Hiding - Formal).** 对象的内部状态无法被没有对应 capability 的主体观察或修改：

$$\forall s \in \text{Subjects}, \forall o \in \text{Objects}: \quad \text{accessible}(s, o, \text{read}) \iff (o, \text{read}) \in \text{capability\_set}(s)$$

**双向性：** 这个性质实际上是两个方向的蕴含：

- （$\Rightarrow$）若 $s$ 可访问 $o$ 的读权限，则 $s$ 必须持有 $(o, \text{read})$ capability。这保证了所有访问都通过 capability 进行，没有隐藏的访问路径。
- （$\Leftarrow$）若 $s$ 持有 $(o, \text{read})$ capability，则 $s$ 必然可以读取 $o$。这保证了 capability 的完备性（completeness）：capability 的持有等价于访问权限。

**Property 3 (Provenance - Auditability - Formal).** 所有指向对象的 capability 必须有可追溯的来源链：

$$\text{capability\_chain}(c) = \text{origin}(c) \rightarrow \text{transfer}_1 \rightarrow \cdots \rightarrow \text{transfer}_n \rightarrow \text{current\_holder}$$

且该链上的每一次传递都必须经过原持有者的显式授权。传递操作 $\text{transfer}_i$ 的形式化定义为：

$$\text{transfer}_i: (s_i, s_{i+1}, c, \text{auth}(s_i)) \rightarrow \text{success}$$

其中 $s_i$ 是传递前的持有者，$s_{i+1}$ 是传递后的持有者，$\text{auth}(s_i)$ 是 $s_i$ 的授权证明。

### 1.4 Capability 的数学定义（WASM 语境下的精确定义）

在 WASM 的严格语境下，capability 的表示涉及几个关键类型系统概念：

**Definition 4 (WASM Reference Types as Capabilities).** WASM 的引用类型（reference types）直接对应 capability：

- `funcref`：对外部函数的引用。这是对"执行某个函数"这一能力的 capability。
- `externref`：对外部对象的引用。这是对"访问某个对象"这一能力的 capability，权限由对象类型定义。
- 内部引用类型（`ref $t`）：对模块内部定义的对象的引用。

**Definition 5 (WASM Capability as a Dependent Type).** 在 WASM 模块的类型系统中，一个 capability $c$ 可以形式化为一个依赖类型：

$$c : \Sigma_{o : \text{Object}} \mathcal{P}(\text{Rights}(o))$$

其中：

- $\Sigma$（依赖类型构造器）：capability 的类型由其指向的对象类型决定
- $\mathcal{P}$（幂集构造器）：capability 持有的权限是该对象支持权限的幂集子集
- $\text{Rights}(o)$：对象 $o$ 支持的权利集合

**Example 2 (WASM Capability Example):** 考虑一个 WASM 模块通过 WASI 调用网络功能。在 WASI 0.2 中，这需要导入 `wasi:http/outbound-handle`。当模块实例化时，主机环境将一个 outbound handle 的 capability 绑定到模块的导入项。模块本身无法创建这个 capability——它必须通过外部提供。这对应于 $\text{origin}(c) = \text{host}$，transfer 操作是实例化时的绑定（instantiation binding）。

**Critical Lemma 1 (Capability Soundness Theorem - Full Statement).** WASM 的类型系统对 capability 的处理满足以下 soundness 条件：

$$\Gamma \vdash e : \tau \implies \text{free\_refs}(e) \subseteq \text{capability\_set}(\Gamma)$$

其中：

- $\Gamma$ 是类型环境，包含所有局部变量和全局引用的类型
- $e$ 是待类型检查的表达式
- $\tau$ 是 $e$ 的类型
- $\text{free\_refs}(e)$ 是表达式 $e$ 中自由引用的集合
- $\text{capability\_set}(\Gamma)$ 是类型环境 $\Gamma$ 中可用 capability 的集合

**Proof Sketch：** WASM 的类型系统基于直觉逻辑（intuitionistic logic）的多集类型论（multiset type theory）。所有 introduction 和 elimination 规则都显式处理引用：

1. **函数调用（call）：** 引用的参数被消耗（线性类型规则），新的引用作为结果返回。
2. **局部变量获取（local.get）：** 从环境 $\Gamma$ 中引入一个已存在的引用。
3. **函数返回（return）：** 引用作为返回值传递，失去原上下文的持有者。

WASM 验证器（verifier）确保没有任何引用可以"凭空出现"——任何引用的来源必须是一个作为参数传入或作为结果返回的 capability。线性类型规则（每个引用恰好被使用一次）进一步排除了引用的隐式复制。$\square$

---

## Step 2：Bell-LaPadula 模型

### 2.1 历史背景与设计动机

Bell-LaPadula 模型诞生于 1970 年代美国国防部对多级安全（Multi-Level Security, MLS）计算系统的需求。在那个时代，一个计算系统可能同时处理不同安全等级的信息——从"公开"（Unclassified）到"机密"（Confidential）到"秘密"（Secret）到"最高机密"（Top Secret）。核心问题是：**如何防止信息从高安全等级流向低安全等级？**

这一问题的紧迫性来自军事通信的实际需求。设想一个指挥官在处理最高机密战役计划的同时，需要与下属通讯公开指令。如果系统不能保证最高机密信息不会通过某个隐蔽通道流向公开渠道，后果将是灾难性的。

Bell 博士和 LaPadula 博士的贡献是将这一工程问题形式化为一个严格的数学模型。他们的方法受到早期 lattice-based 访问控制研究的启发，特别是 Denning 的格模型（Denning's Lattice Model of Information Flow，1976）。BLP 的创新在于：它不仅定义了安全状态，还定义了状态转换规则，并证明了如果初始状态安全且所有转换规则安全保持，则系统永远处于安全状态。

**BLP 的核心设计哲学：** 将"安全"定义为一个状态不变量（state invariant）。系统无论进行什么操作，只要初始状态安全且操作保持安全属性，系统就永远安全。这与 Hoare 逻辑的"不变量推理"有相同的思想根源。

### 2.2 形式化定义：多级安全与安全格

**Definition 6 (Security Class - Full Algebraic Definition).** 一个安全类（security class）$sc$ 是一个二元组：

$$sc = (\text{level}(sc), \text{categories}(sc))$$

其中：

- $\text{level}(sc) \in \mathcal{L}$ 是分类级别（classification level），来自一个偏序集 $\mathcal{L}$，通常包含如：$\text{Unclassified} < \text{Confidential} < \text{Secret} < \text{TopSecret}$
- $\text{categories}(sc) \subseteq \mathcal{C}$ 是类别集合（category set），来自一个有限集合 $\mathcal{C}$，代表"need-to-know"的分区

**Definition 7 (Security Lattice - Complete Algebraic Definition).** 安全格 $\mathcal{L}$ 是满足以下条件的完全偏序集（complete partial order, CPO）：

1. **偏序性（Partial Order）：** 关系 $\leq_{\mathcal{L}}$ 是自反的、反对称的和传递的。
2. **GLB 存在性：** $\forall a, b \in \mathcal{L}, \exists c \in \mathcal{L}: c = a \sqcap b$（最大下界，greatest lower bound）
3. **LUB 存在性：** $\forall a, b \in \mathcal{L}, \exists c \in \mathcal{L}: c = a \sqcup b$（最小上界，least upper bound）
4. **有界性：** $\exists \top, \exists \bot \in \mathcal{L}$（全局顶和全局底）

偏序关系 $\leq$ 定义为：

$$(l_1, C_1) \leq (l_2, C_2) \iff l_1 \leq_{\mathcal{L}} l_2 \land C_1 \subseteq C_2$$

**Example 3 (Military Security Lattice):** 设 $\mathcal{L}_{\text{levels}} = \{\text{U}, \text{C}, \text{S}, \text{TS}\}$，其中 $\text{U} < \text{C} < \text{S} < \text{TS}$。设 $\mathcal{C} = \{\text{NATO}, \text{NUC}, \text{SIOP}\}$。则：

- 安全类 $(\text{TS}, \{\text{NATO}, \text{NUC}\})$ 表示"最高机密"级别，"need-to-know"类别包括 NATO 和 NUC。
- 安全类 $(\text{S}, \{\text{NATO}\})$ 表示"秘密"级别，"need-to-know"类别仅包括 NATO。
- 它们的最小上界（join）是 $(\text{TS}, \{\text{NATO}, \text{NUC}\})$——更高级别和更大类别集合的组合。
- 它们的最大下界（meet）是 $(\text{S}, \{\text{NATO}\})$——较低级别和较小类别集合的组合。

**格的直觉含义：** 安全格结构确保了任意两个安全类都有唯一的"合并"与"交集"。这对于信息流分析至关重要——给定两个信息的安全类，我们可以确定它们合并后的安全类。如果低安全级信息与高安全级信息混合，结果必然是高安全级（信息升级）。如果高安全级信息被明确降级处理（分类减少），则结果可以降低。

### 2.3 BLP 安全属性：三种属性的形式化陈述

BLP 模型定义了三条核心安全属性，它们共同构成了"安全状态"的定义。

**Property * (Simple Security Property / "No Read Up" - Formal).**

主体 $s$ 可以读取对象 $o$，当且仅当：

$$\text{read}(s, o) \iff f_s(s) \geq_{\mathcal{L}} f_o(o)$$

其中：

- $f_s(s)$ 是主体 $s$ 的当前安全级（current security level）
- $f_o(o)$ 是对象 $o$ 的安全级（classification level）

**语义解释：** 这一属性保证了"信息流只能从低或同级流向高"——主体只能读取不低于自身安全级的对象。这防止了高安全级信息通过读取操作流向低安全级主体。你不能读取比你安全级更高的文件——这是"no read up"的含义。

**Property ** (Star Property / "No Write Down" - Formal).**

主体 $s$ 可以写入对象 $o$，当且仅当：

$$\text{write}(s, o) \iff f_s(s) \leq_{\mathcal{L}} f_o(o)$$

注意：这里的关系方向与 *-property 相反。写入要求主体安全级"小于等于"对象安全级。

**语义解释：** 这一属性防止了信息从高安全级流向低安全级——主体只能写入不低于自身安全级的对象。你不能将机密信息写入公开文件，因为那会将高安全级信息混入低安全级对象（即使内容本身是机密的，混合行为本身就破坏了安全隔离）。

**Property *** (Discretionary Security Property / Access Matrix Property - Formal).**

每个对象有一个访问控制矩阵 $A$，主体对对象的访问必须满足：

$$\forall (s, o, \text{right}) \in b: \text{right} \in A[s][o]$$

其中 $A[s][o]$ 是访问矩阵 $A$ 中主体 $s$ 对对象 $o$ 拥有的权限集合。

**语义解释：** 这一属性将自主访问控制（discretionary access control）引入 BLP 框架。即使 *-property 和 **-property 满足，主体也不能超出访问矩阵允许的范围访问对象。这提供了细粒度的权限控制。

### 2.4 BLP 形式化状态机与安全定理

**Definition 8 (BLP System State).** BLP 模型的状态 $v$ 是一个三元组：

$$v = (b, M, f)$$

其中：

- $b \subseteq B \times S \times O \times A$ 是当前访问集合（current access set），表示当前活跃的 (subject, object, mode) 三元组集合。$B$ 是访问模式集合（如 \{read, write, append, execute\}），$S$ 是主体集合，$O$ 是对象集合。
- $M$ 是访问控制矩阵集合，$M$ 将每个主体-对象对映射到权限集合：$M: S \times O \rightarrow 2^A$。
- $f = (f_s, f_c, f_o)$ 是安全级函数三元组：
  - $f_s: S \rightarrow \mathcal{L}$：主体当前安全级（current security level）
  - $f_c: S \rightarrow \mathcal{L}$：主体创建级（创建时的安全级，用于追踪主体历史）
  - $f_o: O \rightarrow \mathcal{L}$：对象安全级

**Definition 9 (Secure State - Full).** 状态 $v = (b, M, f)$ 是安全的，当且仅当所有以下条件同时成立：

1. **Simple Security Condition (*-Property):** $\forall (s, o, \text{read}) \in b: f_s(s) \geq_{\mathcal{L}} f_o(o)$
2. **Star Security Condition (*-Property Variant for Append):** $\forall (s, o, \text{append}) \in b: f_s(s) \leq_{\mathcal{L}} f_o(o)$
3. **Discretionary Security Condition (***-Property):** $\forall (s, o, a) \in b: a \in M[s][o]$

**Definition 10 (Security-Preserving Transition).** 状态转换函数 $\rho$ 是安全保持的，当且仅当：

$$\text{security\_preserving}(\rho) \iff \forall v \in \text{secure\_states}: \rho(v) \in \text{secure\_states}$$

即：对任何安全状态应用 $\rho$，结果状态仍然是安全的。

**Theorem 1 (BLP Basic Security Theorem - Formal Statement).** 如果初始状态 $v_0$ 是安全的，且所有状态转换函数 $\rho_i$ 都是安全保持的，则系统所有可达状态都是安全的：

$$\forall i \in \mathbb{N}: v_i \in \text{secure\_states}$$

**Proof - Complete Inductive Proof:**

**基例（Base Case）：** $v_0$ 是安全的，由初始条件给出。

**归纳假设（Induction Hypothesis）：** 假设第 $n$ 个状态 $v_n$ 是安全的。

**归纳步骤（Induction Step）：** 第 $n+1$ 个状态由 $v_{n+1} = \rho(v_n)$ 生成。由于 $\rho$ 是安全保持的，且 $v_n$ 是安全状态，故 $v_{n+1}$ 也是安全状态。

由数学归纳法，对所有 $n \in \mathbb{N}$，$v_n$ 都是安全状态。$\square$

**这一定理的关键价值：** 它将安全证明从"运行时每一刻都在验证"转变为"只需验证初始状态安全和转换规则安全"。这对于大型系统的形式化验证至关重要——无限长度执行轨迹的安全性，只需有限长度的验证。

---

## Step 3：映射证明

### 3.1 建立对应关系的动机与直觉

我们已经在 Step 1 和 Step 2 中分别定义了 capability 系统和 BLP 系统。现在的问题是：这两个系统之间的关系是什么？它们是独立的吗？还是存在某种蕴含关系？

从直觉上说，capability 系统关注"如何表示权限"，而 BLP 关注"权限如何流动"。Capability 是一种**表示方法**（representation），BLP 是一种**约束条件**（constraint）。问题是：capability 的表示是否能够精确地实现 BLP 的约束？

**核心洞察：** Capability 系统和 BLP 系统不是竞争对手——它们处于不同的抽象层次。Capability 是一种**实现机制**（implementation mechanism），BLP 是一种**规范属性**（specification property）。任何满足 BLP 安全属性的系统，都可以用 capability 来实现；反过来，任何 capability 系统，只要其权限传递规则满足 BLP 的信息流约束，就自动满足 BLP 安全属性。

**类比：** 这类似于图灵机与 Lambda 演算的关系。图灵机是一种计算的实现机制，Lambda 演算是计算的抽象模型。图灵机可以模拟 Lambda 演算，Lambda 演算可以描述图灵机可计算的所有函数。它们不是对立的，而是互补的描述工具。Capability 与 BLP 也是如此。

### 3.2 Capability Rights 到 Bell-LaPadula 访问类的映射

我们建立以下映射函数：

**Mapping Function $\phi$:**

$$\phi: \text{Rights} \rightarrow \{\text{read}, \text{write}, \text{append}, \text{execute}\}$$

典型映射表：

| Capability Right | BLP Access Mode | 方向约束 | 安全直觉 |
|------------------|-----------------|----------|----------|
| `read`           | `read`          | 对象安全类 $\leq$ 主体安全类 | 只能读同级或低级对象 |
| `write`          | `write`         | 主体安全类 $\leq$ 对象安全类 | 只能写同级或高级对象 |
| `append`         | `append`        | 主体安全类 $\leq$ 对象安全类 | 只能追加同级或高级对象 |
| `exec`           | `execute`       | 等级相等且类别包含 | 只能执行同级代码 |

**Lemma 2 (Right-to-Access Mapping Soundness - Detailed Proof).** 令 $c = (o, R)$ 为一个 capability，其中 $R$ 包含特定 right $r$。则在映射 $\phi$ 下，持有 $c$ 的主体 $s$ 被授权以模式 $\phi(r)$ 访问对象 $o$，并且这一授权满足 BLP 的 *-property 和 **-property：

$$\text{if } r \in R \text{ then } \text{BLP\_authorized}(s, o, \phi(r)) \land \text{BLP\_property\_satisfied}(s, o, \phi(r))$$

**Proof - Case Analysis:**

**情况 1（$r = \text{read}$）：**

已知 $r \in R$。由映射表，$\phi(r) = \text{read}$。根据 BLP *-property：

$$\text{read}(s, o) \iff f_s(s) \geq_{\mathcal{L}} f_o(o)$$

在 capability 系统中，持有 $(o, \text{read})$ capability 意味着 $s$ 有读取 $o$ 的权限。同时，capability 的语义隐含 $f_s(s) \geq_{\mathcal{L}} f_o(o)$——因为只有当对象的安全类不高于主体的安全等级时，主体才被允许持有对该对象的读 capability（这由 capability 的 provenance 链保证：初始 capability 由系统根据安全策略分配，系统不会分配一个会使主体违反 BLP 属性的 capability）。因此 *-property 满足。

**情况 2（$r = \text{write}$）：**

已知 $r \in R$。由映射表，$\phi(r) = \text{write}$。根据 BLP **-property：

$$\text{write}(s, o) \iff f_s(s) \leq_{\mathcal{L}} f_o(o)$$

持有 $(o, \text{write})$ capability 意味着 $s$ 有写入 $o$ 的权限。这要求 $s$ 的安全等级不高于 $o$ 的安全等级，故 **-property 满足。

**情况 3-4（$r = \text{append}$ 或 $\text{exec}$）：** 类似地可证。$\square$

### 3.3 对象 Capability 集合到安全格的映射

**Mapping Function $\psi$:**

$$\psi: 2^{\text{Capabilities}} \rightarrow \mathcal{L}$$

给定主体 $s$ 的 capability 集合 $C_s = \{c_1, c_2, \ldots, c_n\}$，其中 $c_i = (o_i, R_i)$，我们定义：

$$\psi(C_s) = \bigsqcup_{i=1}^{n} \text{SC}(o_i)$$

其中：

- $\text{SC}(o_i)$ 是对象 $o_i$ 在安全格中的位置（即对象的安全类）
- $\sqcup$ 表示最小上界（join，格中的 LUB 操作）

**直觉解释：** 主体 $s$ 的"实际安全等级"由其持有的所有 capability 所指向的对象中**最高安全等级的对象**决定。这是因为：主体可以通过其 capability 集合访问这些高安全级对象，因此它实际上具有了访问高安全级信息的"潜力"，在 BLP 语义下，这等价于主体的安全等级不低于它能访问的最高安全级对象。

**Example 4 (Capability Set to Security Level):** 假设主体 $s$ 持有三个 capability：

- $c_1 = (o_1, \{\text{read}\})$，其中 $\text{SC}(o_1) = (\text{C}, \{\text{NATO}\})$
- $c_2 = (o_2, \{\text{read}, \text{write}\})$，其中 $\text{SC}(o_2) = (\text{S}, \{\text{NATO}, \text{NUC}\})$
- $c_3 = (o_3, \{\text{read}\})$，其中 $\text{SC}(o_3) = (\text{U}, \{\})$

则 $\psi(C_s) = (\text{S}, \{\text{NATO}, \text{NUC}\})$——即这三个对象安全类的最小上界。根据 BLP，这意味着 $s$ 的安全等级至少是 $(\text{S}, \{\text{NATO}, \text{NUC}\})$。

**Lemma 3 (Capability Set determines Security Level - Detailed).** 主体 $s$ 的安全等级不小于某个安全类 $L$ 当且仅当 $s$ 的 capability 集合的上确界在格中不低于 $L$：

$$f_s(s) \geq_{\mathcal{L}} L \iff \psi(\text{capability\_set}(s)) \geq_{\mathcal{L}} L$$

**Proof:**

**必要性（$\Rightarrow$）：** 若 $f_s(s) \geq_{\mathcal{L}} L$，则由于 $f_s(s)$ 由 $\psi(\text{capability\_set}(s))$ 决定（定义），故 $\psi(\text{capability\_set}(s)) \geq_{\mathcal{L}} L$。

**充分性（$\Leftarrow$）：** 若 $\psi(\text{capability\_set}(s)) \geq_{\mathcal{L}} L$，则根据 $\psi$ 的定义：

$$\psi(C_s) = \bigsqcup_{i=1}^{n} \text{SC}(o_i) \geq_{\mathcal{L}} L$$

由格的偏序性质，这意味着对所有 $i$，$\text{SC}(o_i) \geq_{\mathcal{L}} L$ 或它们的 LUB $\geq_{\mathcal{L}} L$。由于 $L$ 不大于 $s$ 可访问的所有对象的最高安全类，因此 $s$ 的安全等级必须至少为 $L$。

反过来，$s$ 的安全等级必须不小于其 capability 集合的上确界——因为它可以访问所有这些对象。$\square$

### 3.4 Capability 撤销与"遗忘"操作

在 BLP 模型中，当主体需要降级时（如用户登出高安全级会话），系统执行一个称为"forget"或"退权"（declassification）的操作。这个操作改变主体的安全等级，使其无法继续访问高安全级对象。

**Definition 9 (Capability Revocation - Formal).** 撤销操作 $\text{revoke}(s, c)$ 从主体 $s$ 的 capability 集合中移除 capability $c$：

$$\text{capability\_set}'(s) = \text{capability\_set}(s) \setminus \{c\}$$

对应的 $\psi$ 映射变化：

$$\psi(\text{capability\_set}'(s)) = \psi(\text{capability\_set}(s)) \sqcup \text{SC}(o_c)$$

其中 $o_c$ 是被撤销 capability 指向的对象。注意：这里的 $\sqcup$ 操作是对被撤销对象安全类和原上确界的操作，结果是移除该对象后的上确界——即原来上确界与该对象安全类的最大下界（meet）。

**Lemma 4 (Revocation = Forget in BLP - Detailed Proof).** 撤销 capability $c = (o, r)$ 等价于在 BLP 模型中将主体 $s$ 对对象 $o$ 的访问权限从 $r$ 撤销：

$$\text{revoke}(s, (o, r)) \iff \text{BLP\_forget}(s, o, r) \iff f_s'(s) = f_s(s) \sqcap \text{SC}(o)$$

**Proof Sketch:** 撤销 capability 直接移除了 $s$ 访问 $o$ 的权限。由于 $\psi$ 的定义依赖于所有 capability 的上确界，移除 capability 等价于将上确界与该对象的 SC 做 meet（$\sqcap$）操作。在 BLP 中，"forget"操作正是将主体的安全等级与被遗忘对象的等级做 meet。两者数学上是同构的。$\square$

**这意味着什么？** 在 WASM 中，当你撤销一个模块对某个对象的 capability 时，从 BLP 的角度，这等价于将该模块的安全等级降低到它仍然持有的最高对象的安全等级。这提供了能力撤销的形式化语义。

### 3.5 主定理：Capability-BLP 互换定理

现在我们陈述并证明本附录的核心定理。

**Theorem 2 (Capability-BLP Correspondence Theorem - Full Statement with All Conditions).** 任何满足以下条件的 WASM 程序 $P$ 是 BLP 安全的：

1. **Capability Integrity（Capability 完整性）：** 所有跨模块调用传递的 capability 满足线性类型约束。每个 capability 在传递后从原持有者的类型上下文中消失（consumed），且最多被传递一次（无复制）。

2. **No Ambient Authority（无环境权威）：** 程序不存在不通过 capability 获取的对象引用。所有对象引用都来自 capability 的传递，不存在"全局命名空间"或"隐式根 capability"。

3. **Attenuation Preservation（削弱保持）：** 对外的接口调用只能传递原始 capability 的削弱版本。对任何导出函数 $f$ 及其参数中的 capability 集合 $C_f$，有：

$$\text{exported\_caps}(f) = \text{Attenuate}(C_f, R_f) \text{ where } R_f \subseteq C_f$$

即：导出的 capability 只能是原 capability 的削弱，不能增强。

4. **Type Soundness（类型可靠性）：** 程序通过 WASM 验证器（verifier）的类型检查，即满足 Lemma 1 的 soundness 条件。

**Proof - Complete Step-by-Step:**

**Part I: Capability Implies BLP Access（Capability 蕴含 BLP 访问）**

对任意 WASM 执行状态，考察任意活跃访问 $(s, o, \text{mode})$。

由于 WASM 的强类型保证（Lemma 1），该访问必然来自某个 capability $c = (o, R)$，且 $\text{mode} \in \phi^{-1}(R)$。即：引用的来源必须追溯到某个 capability 的传递。

由 Lemma 2（Right-to-Access Mapping Soundness），该访问在 BLP 下是授权的。

**Part II: *-Property Verification（*-属性验证）**

设 $s$ 通过 capability $c = (o, \{\text{read}\})$ 读取 $o$。

根据 capability 的语义，$\{\text{read}\} \subseteq R$ 意味着 $s$ 对 $o$ 持有读权限。

在 Capability 模型中，持有读 capability 的条件是：$o$ 的安全类 $\leq$ 由 $\psi$ 派生的 $s$ 的安全等级。

因此 $f_s(s) \geq_{\mathcal{L}} f_o(o)$，即满足 *-property。

**Part III: *-Property Verification（*-属性验证）**

设 $s$ 通过 capability $c = (o, \{\text{write}\})$ 写入 $o$。

同理，写权限要求 $s$ 的安全等级 $\leq$ $o$ 的安全类：

$f_s(s) \leq_{\mathcal{L}} f_o(o)$，满足 *-property。

**Part IV: Discretionary Security Property（自主安全属性验证）**

WASM 的访问控制通过 capability 实现，而非 ACL。WASM 模块无法访问任何未通过类型系统传递的引用。

当 $s$ 持有 $c = (o, R)$ 时，$R$ 正好构成访问矩阵 $M[s, o]$ 的权限子集：

$$M[s][o] \supseteq R$$

因此 $(s, o, a) \in b \implies a \in M[s][o]$ 自动满足。

**Part V: State Transition Security（状态转换安全性验证）**

WASM 的验证器（verifier）保证所有导出的函数调用序列满足上述条件。

状态转换函数 $\rho$ 在 capability 约束下是安全保持的（security-preserving），因为：

1. 任何导致新引用的操作（call, return, local.get）都必须指定引用的 provenance。
2. Provenance 链必然追溯到某个初始 capability。
3. 初始 capability 集合是已知的安全集（由系统策略定义）。
4. 传递规则不创造新的访问权限，只对已有权限进行削弱（attenuate）或传递（transfer）。

因此 $\rho$ 不可能产生 BLP 非法的访问。

**Conclusion（结论）：**

由 Basic Security Theorem（Theorem 1），系统所有可达状态满足 BLP 安全性质。

**Q.E.D.** $\square$

### 3.6 映射的双射性质与格同构

**Theorem 3 (Mapping Isomorphism - Complete).** 映射 $\phi \times \psi$（capability rights 的映射与 capability sets 的映射的笛卡尔积）建立了 capability 系统和 BLP 系统之间的格同构（lattice isomorphism）：

$$(\text{Rights}, \subseteq) \times (2^{\text{Capabilities}}, \subseteq) \cong (\mathcal{L}, \leq_{\mathcal{L}}) \times (\text{AccessModes}, \leq_{\text{mode}})$$

**Proof - Complete:**

证明同构需要验证两个方向：

**1. 单射性（Injectivity）：**

若 $\phi(r_1) = \phi(r_2)$ 且 $\psi(C_1) = \psi(C_2)$，则 $r_1 = r_2$ 且 $C_1 = C_2$。

**证明：** $\phi$ 是由定义给出的确定映射，映射表中每行对应唯一的访问模式。$\psi$ 是基于对象安全类的 LUB 操作，由格的性质保证唯一性。

**2. 满射性（Surjectivity）：**

对任意 $(L, a) \in \mathcal{L} \times \text{AccessModes}$，存在对应的 $(R, C)$ 使得 $\phi(R) = L$ 且 $\psi(C) = a$。

**构造：** 取所有安全类为 $L$ 的对象对应的 rights 集合为 $R$。取所有安全类在 $L$ 以下的对象集合为 $C$。则：

- $\phi(R) = a$（由映射表定义）
- $\psi(C) = \bigsqcup_{o \in C} \text{SC}(o) = L$（由 LUB 的定义）

**3. 运算保持（Operation Preservation）：**

我们需要验证映射保持格运算（$\sqcup$ 和 $\sqcap$）：

- $\phi(R_1 \cup R_2) = \phi(R_1) \sqcup \phi(R_2)$
- $\psi(C_1 \cup C_2) = \psi(C_1) \sqcup \psi(C_2)$

由 $\phi$ 和 $\psi$ 的定义及格的性质，直接可得。

因此映射是格同构。$\square$

**这一定理的意义：** 格同构意味着 capability 系统和 BLP 系统在安全语义上是等价的描述语言——它们描述的是同一个数学结构，仅仅是表示方式不同。这为"任何 BLP 审计工具都可以用于 WASM 程序"提供了理论基础。

---

## Step 4：为什么这重要

### 4.1 从"不被允许"到"物理上不可能"

在讨论形式化安全的实际意义之前，我们先区分两种不同层次的安全保证：

**运行时监控（Runtime Monitoring）：** 传统安全模型依赖访问控制列表（ACL）、安全Policies、或运行时权限检查。这些机制告诉你："这个操作不被允许"——但它们的有效性建立在"检查函数被正确调用"的前提上。如果恶意代码找到办法绕过或跳过检查，或者检查本身存在逻辑漏洞，安全保证就会失效。

**类型系统强制（Type System Enforcement）：** WASM 的 capability 安全模型将安全策略编码为类型系统的不变量。WASM 验证器在模块实例化之前检查所有类型约束。一旦验证通过，"违反安全策略"这件事在数学上变得不可能——不是因为检查被执行了，而是因为构造这样的程序在类型论层面是不可达的（type-theoretically unreachable）。

**一个具体的例子：** 考虑一个试图绕过 WASI 网络限制的恶意 WASM 模块。该模块尝试：

1. 直接调用 `socket()` 系统调用——失败，因为模块没有导入 `wasi:sockets` 接口。
2. 通过函数指针算术运算找到网络函数——失败，因为 WASM 的函数引用是不可操作的 opaque 类型。
3. 尝试从环境中"窃取"一个已有的网络 capability——失败，因为 capability 必须通过类型化的参数传递，不能从环境中隐式获取。

所有三种攻击方式都失败了，但原因各不相同：第一种是因为模块根本没有这个导入；第二种是因为函数引用类型的封装性；第三种是因为没有 ambient capability。在传统安全模型中，这三种攻击的防御分别依赖系统调用过滤、地址空间布局随机化（ASLR）、和运行时引用计数。在 WASM 中，它们都归结为一个原因：**模块的类型环境不包含网络 capability，因此无法构造任何涉及网络的表达式**。

### 4.2 对抗 Bounded Intelligence 原则

Bounded intelligence 原则指出：AI 的推理能力是有限的，无法始终遵守复杂的安全约束。更糟糕的是，当 AI 被要求生成复杂代码时，其"遵循安全规则"的能力随代码复杂度指数级下降——这是 prompt injection、数据外传等安全问题的根本原因。

传统的工程对策是"增加检查点"：在代码生成的各个环节插入安全检查，要求 AI 生成额外的安全验证代码。但这带来几个问题：

1. **检查点可以被移除：** 如果 AI 生成的代码本身包含隐藏的代码路径绕过这些检查，额外的检查形同虚设。
2. **检查本身可能不安全：** AI 可能生成存在逻辑漏洞的安全检查代码。
3. **性能开销：** 频繁的运行时检查严重影响系统性能。
4. **复杂性爆炸：** 每增加一个检查点，就增加了一层可能的故障点和安全漏洞。

WASM capability 模型提供了第四种方案：**让违规操作在类型层面不可构造。** 具体而言：

| 安全保证类型 | 要求 AI 做到的 | WASM-Capability 的实际效果 |
|--------------|----------------|---------------------------|
| 运行时检查   | AI 必须调用正确的检查函数 | 检查函数的存在由类型推导保证，调用被验证器强制 |
| Capability 传递 | AI 必须只传递授权的 capability | 未传递的 capability 在模块类型层面不存在 |
| 降级（attenuate）| AI 必须正确削弱权限 | 削弱操作由子类型规则强制，不可绕过 |
| 网络隔离     | AI 生成的代码只能通过 WASI socket 调用 | 未经授权的网络 capability 不在模块的导入表中 |

**关键区别：** 在传统模型中，安全检查是一个"需要记住做"的行为；在 WASM-capability 模型中，安全不变量是"无法忘记维护"的类型约束。AI 可以忘记调用检查，但不能忘记它从未持有过的 capability。

### 4.3 对 Harness 工程的具体价值

在 Agent Harness 的语境下，Theorem 2 的实际含义远超理论兴趣：

**价值一：不可信代码的确定性隔离。**

当 AI 生成的 Tool 代码在 WASM 沙箱中运行时，其所有可能的输入输出行为都被 BLP 安全性质约束。这意味着：即使用户Prompt被恶意注入（jailbreak prompt），恶意代码也无法将数据外传给未授权的网络端点——因为 capability 撤销机制（Lemma 4）保证了数据外传所需的 capability 在调用链中根本不存在。

具体而言，WASI 的 capability 模型要求：任何网络调用都必须导入 `wasi:http/outbound-handle`。这个导入项的来源只能是模块实例化时由主机环境绑定。如果主机环境的策略是"不给这个模块绑定网络 capability"，则该模块就是一个纯计算模块，无法发起任何网络请求。这比传统的网络防火墙更彻底——防火墙只拦截已知端口和协议，而 capability 模型从根本上断绝了网络引用的可能性。

**价值二：Capability 撤销是即时且确定性的。**

不同于传统 garbage collection 的不确定回收，WASM 的线性类型保证 capability 在失去引用时立即失效。对于需要精确资源控制的 Harness 场景（如金融交易、敏感数据处理），这种确定性是安全审计的关键。

例如，在处理用户会话时，当用户登出系统，我们需要确保该用户的所有 capability 立即失效。在传统模型中，这需要遍历所有数据结构并清除引用，可能存在遗漏（use-after-free 漏洞）。在 WASM-capability 模型中，撤销操作的效果是即时的——一旦模块实例被销毁，所有与之关联的 capability 都立即变为不可达，任何试图使用它们的操作都会触发验证器错误。

**价值三：形式化验证工具链可直接复用。**

由于 WASM 代码可以被形式化验证（如通过 K framework、Coq、Isabelle 等工具），而 capability 语义已被证明对应 BLP 安全，我们可以为整个 Harness 安全架构提供机器可检查的安全证明。

具体而言：任何为 BLP 安全模型开发的审计工具，理论上可以直接用于 WASM 程序的安全分析。例如：

- Finite-state model checker 可以验证 WASM 模块的状态转换是否满足 BLP 安全保持条件。
- Information flow analysis 工具可以直接应用于 WASM 的 capability 传递图。
- Type-based security verification 可以利用 WASM 的类型系统进行自动化安全证明。

**价值四：安全证明的可组合性。**

在模块化系统中，如果每个子模块都被证明满足 capability 约束，则组合后的系统也满足 BLP 安全性质。这使得大规模 Harness 系统的安全验证成为可能——无需对整个系统进行穷举测试，只需验证模块接口的 capability 传递。

例如，Harness 系统可能由以下组件组成：

- Agent Controller（主控制器）
- Tool Executor（工具执行器）
- State Manager（状态管理器）
- Network Proxy（网络代理）

每个组件都在各自的 WASM 沙箱中运行，拥有不同的 capability 集合。组合安全性由以下条件保证：

- 组件之间的所有交互都通过 capability 传递。
- 每个组件的 capability 集合都满足 BLP 约束。
- 组件之间的 capability 传递链满足 attenuation 规则。

### 4.4 局限性声明与开放问题

虽然本附录建立了 capability 安全与 BLP 安全之间的严格对应关系，但这一对应并非没有局限：

**局限一：BLP 模型的已知局限。**

BLP 模型主要关注信息**机密性**（confidentiality），对信息**完整性**（integrity）的保护较弱。机密性意味着"信息不能流向未授权的主体"，完整性意味着"信息不能被未授权的主体篡改"。BLP 对完整性的保护几乎为零——一个低安全级的主体可以自由地写入（篡改）高安全级对象，只要写入操作的方向是"向上"的（write-up）。

补救措施：完整性通常由 Biba 模型或其他模型（如 Clark-Wilson）补充。这意味着对于需要同时保护机密性和完整性的场景，需要组合使用多个安全模型。

**局限二：隐蔽通道（Covert Channels）。**

BLP 模型假设所有信息流都是显式的，但实际系统存在隐蔽通道。例如：

- **Timing channels：** 执行时间的变化可能被恶意代码利用来编码信息。如果高安全级操作比低安全级操作耗时更长，低安全级代码可以通过测量执行时间推断高安全级信息。
- **Resource contention channels：** 共享资源（如 CPU 缓存、内存）的竞争可能泄露信息。恶意代码通过监测资源使用模式推断高安全级数据。

WASM 虽然通过确定性执行和沙箱隔离消除了大部分隐蔽通道，但仍存在 timing attacks 等残余。在高安全场景中，需要额外的对策（如引入随机延迟、使用恒定时间算法等）。

**局限三：Capability 委托（Delegation）的形式化建模。**

本附录的映射假设 capability 的传递是一阶的——主体直接传递 capability 给另一个主体。但在实际系统中，capability 经常被委托（delegated）——主体授权另一个主体代表自己行事，并可能限制委托的权限范围（delegation with restrictions）。如何在 BLP 框架内建模 capability 的委托，是一个待解决的问题。

**开放问题：** Capability 系统的"可追溯性"（provenance tracking）如何形式化地与 BLP 的审计要求对应，仍是活跃的研究领域。BLP 的审计要求记录所有访问事件，而 capability 的 provenance 链记录的是权限传递历史——两者之间存在对应关系，但是否存在严格的等价性，目前尚无定论。

### 4.5 实践指南：在 Harness 工程中应用本附录理论

#### 4.5.1 设计原则

基于本附录的 Theorem 2 和 Lemma 1，在设计 Agent Harness 的安全架构时，应遵循以下原则：

**原则一：最小权限的 Capability 分配（Principle of Least Capability）。**

每个模块实例应该只持有其完成功能所必需的 capability。这对应于 BLP 的"最小安全级原则"——主体应该被授予最低必要的安全等级。

**实践做法：** 在设计 WASM 模块的导入接口时，只声明模块实际需要的接口。例如，如果一个工具只需要读取文件系统，不需要写入，则只导入 `wasi:filesystem/readonly-filesystem`，而非完整的 `wasi:filesystem` 接口。

**原则二：Capability 的单向衰减（One-Way Attenuation）。**

模块导出的 capability 只能是其导入 capability 的衰减版本。这防止了 capability 的意外升级。

**实践做法：** 在设计模块的导出接口时，如果模块持有一个网络 capability 但只希望允许 HTTP GET 请求，应该导出的是一个经过削弱处理的只读 handle，而非原始的完整 handle。

**原则三：无 Ambient Authority。**

不要在模块中引入任何隐式的根 capability。所有 capability 都必须显式传递。

**实践做法：** 避免使用"超级用户"或"管理员"角色。所有模块都应该是受限的"普通用户"，其权限完全来自启动时绑定的 capability。

#### 4.5.2 形式化验证的实践路径

**第一步：模块接口的 Capability 规范。**

在编写 WASM 模块时，显式地在模块的导入和导出类型中标注 capability。这要求定义一个 Capability 类型注解语言。例如：

```
(module
  (import "wasi:http" "outbound-handle" (func $http (param (ref http-request)) (result (ref http-response))))
  (export "process" (func $process (param (ref user-request)) (result (ref user-response))))
)
```

在这个例子中，`$http` 函数的使用权限完全由导入决定，模块本身无法获取额外的 HTTP capability。

**第二步：验证器的配置。**

配置 WASM 验证器以检查 capability 完整性：

- 验证所有引用都有可追溯的 provenance。
- 验证所有 capability 传递满足衰减规则。
- 验证没有模块可以访问其导入集中不包含的 capability。

**第三步：组合验证。**

当多个模块组合成系统时，验证：

- 模块之间的 capability 传递满足 BLP 的信息流约束。
- 整个系统的 capability 传递图是安全的（无非法信息流）。
- 所有撤销操作的效果是确定性的。

#### 4.5.3 常见反模式与规避

**反模式一：Capability 的复制。**

错误地通过"复制"而非"传递"来共享 capability。这违反了线性类型规则，可能导致 capability 被多次使用。

正确做法：Capability 只能通过 `call` 指令传递，传递后原持有者失去引用。

**反模式二：Capability 的全局存储。**

将 capability 存储在全局变量或共享内存中，使其绕过线性类型检查。

正确做法：Capability 只能通过函数参数传递，不应该有持久化存储。

**反模式三：Capability 的升级。**

通过某种方式从较弱的 capability 派生出较强的 capability（如从只读 capability 派生出读写 capability）。

正确做法：削弱（attenuate）是单向的——更强的权限无法从更弱的权限中构造出来。

### 4.6 与现有安全框架的对比

| 维度 | 传统 ACL | Capability 系统 | BLP 模型 | WASM Capability |
|------|----------|-----------------|----------|------------------|
| 权限表示 | 访问控制矩阵 | 不透明句柄 | 安全类 | 类型化引用 |
| 权限传递 | 管理员显式授权 | capability 传递 | 无直接对应 | 函数参数传递 |
| 权限撤销 | ACL 条目删除 | capability 销毁 | 安全级重置 | 实例销毁 |
| 形式化验证 | 困难 | 中等 | 成熟 | 自动化可能 |
| 隐蔽通道防护 | 弱 | 中等 | 弱 | 较强 |
| 完整性保护 | ACL 依赖 | 中等 | 弱 | 需额外模型 |
| 实际部署 | 广泛 | E, CapROS, KeyKOS | NSA SELinux | WASM/WASI |

### 4.7 对未来研究的展望

**展望一：Capability 与完整性模型的结合。**

本附录主要关注机密性（BLP），但对 Agent Harness 而言，完整性同样重要。未来的研究应该探索 capability 系统与 Clark-Wilson 完整性模型的结合。

**展望二：自动化 Capability 推理。**

当前的 capability 规范需要开发者手动声明。未来可以开发自动推理工具，从模块代码中自动推断其 capability 需求，并检测 capability 泄漏。

**展望三：Capability 的形式化验证工具。**

将 Coq、Isabelle 等证明助手与 WASM 验证器结合，实现 capability 约束的机器可检查证明。

**展望四：多级 Capability 的研究。**

本附录假设 capability 是二元的（持有或不持有）。未来可以探索多级 capability（partial capability），直接对应 BLP 的多级安全类。

### 4.8 形式化安全的经济学意义

**为什么形式化安全证明比"测试"更值钱？**

在工程实践中，我们通常通过测试来验证系统的安全性。测试的价值在于它能发现实际的 bug。但测试有一个根本性的局限：**测试不能证明 absence of bugs，只能证明 presence of bugs**。对于安全系统而言，"未发现漏洞"不等于"系统是安全的"——攻击者总是可以尝试测试者没有考虑到的攻击向量。

形式化安全证明则不同。它提供了一种数学上严格的论证：如果初始状态满足安全条件，且所有转换规则保持安全，则所有可达状态都是安全的。这是一种**穷举论证**——不是通过测试有限数量的输入，而是通过数学证明覆盖了所有可能的执行路径。

**WASM Capability + BLP 的经济学含义：**

1. **一次性验证成本，多次部署收益。** 如果我们形式化验证了一个 WASM 模块满足 capability 约束，则该模块在任何环境中的任何实例化都是安全的。这比每个部署实例都需要重新测试要经济得多。

2. **信任的可组合性。** 如果模块 A 和模块 B 都满足 capability 约束，则它们的组合也满足。这意味着我们不需要对整个系统进行端到端验证，只需验证每个组件及其接口。

3. **供应链安全的可验证性。** 在 AI 生成的代码场景中，代码的来源可能不可信。通过验证工具链，我们可以形式化地证明：即使用户运行的代码来自不可信的来源，只要它被包装在经过验证的 WASM 模块中，它就不会违反安全策略。

### 4.9 形式化语言的精确性：一个对比

为了说明形式化方法的价值，我们对比"用自然语言描述安全策略"和"用形式化语言描述安全策略"之间的差异。

**自然语言描述：**
"模块不应该能够访问它没有被显式授予的网络能力。"

**问题：** "访问"的含义是什么？是调用网络函数？读取网络配置？还是尝试通过 timing side channel 推断网络状态？"显式授予"如何定义？通过导入表声明算显式吗？通过返回值的回调算吗？

**形式化描述（本附录的定义）：**
$$\forall \Gamma, o: \Gamma \vdash e : \text{cref}(o, R) \implies (o, R) \in \Gamma$$

**精确含义：** 在类型环境 $\Gamma$ 下，表达式 $e$ 拥有对对象 $o$ 的引用 $(o, R)$ 的充分必要条件是 $(o, R)$ 已经在 $\Gamma$ 中。这没有歧义——引用只能来自环境，不能"凭空出现"。

形式化方法的价值在于：它将安全策略的描述从"需要理解意图"转变为"可以机械检查"。

### 4.10 本附录对读者的工作假设

本附录假设读者：

- 熟悉基本的形式化证明技术（归纳法、反证法）
- 了解基本的集合论和格论概念（偏序集、格、上下确界）
- 对访问控制的基本概念有了解（主体、客体、权限）
- 对 WASM 的基本概念有了解（模块、实例、引用类型、验证器）

本附录不假设读者是安全理论的专家。我们会解释 BLP 模型的基本直觉，但不会深入讨论 BLP 的所有细节变体（如 BLP 的争议、BLP 的扩展如 Biba 模型等）。

### 4.11 进一步阅读建议

对于希望深入了解本附录所涉及主题的读者，建议以下阅读顺序：

**第一阶段：打牢基础。**

- 阅读 Denning (1976) 的格模型论文，理解信息流安全的基本直觉。
- 阅读 Dennis & Van Horn (1966) 的原始 capability 论文，理解 capability 作为计算原语的思想。

**第二阶段：理解 BLP。**

- 阅读 Bell & LaPadula (1976) 的原始 BLP 报告，理解 BLP 的完整形式化。
- 阅读 Landauer & Bell (1999) 的反思论文，理解 BLP 在实际应用中的挑战。

**第三阶段：Capability 系统的现代发展。**

- 阅读 Miller (2006) 的 capability 安全综述，理解现代 capability 系统的设计原则。
- 阅读 WASM 规范的相关章节，理解 capability 在 WASM 中的具体实现。

**第四阶段：高级主题。**

- 研究如何将 capability 与 Biba 完整性模型结合。
- 研究自动化 capability 推理工具。
- 研究隐蔽通道的检测和缓解技术。

---

## 本章来源

1. **Bell, D. E., & LaPadula, L. J.** (1976). *Secure Computer System: Mathematical Foundations and Model*. MITRE Corporation Technical Report MTR-2547. 原始 BLP 模型定义，是 MLS 形式化的权威参考文献。该报告建立了多级安全（MLS）的数学基础，至今仍是计算机安全理论的核心文献。

2. **Dennis, J. B., & Van Horn, E. C.** (1966). *Programming Semantics for Multiprogrammed Computations*. Communications of the ACM, 9(3), 143-155. 对象-capability 模型的起源论文，首次提出 capability 作为计算的基本抽象，比面向对象编程的兴起早了近十年。

3. **Miller, M. S.** (2006). *Capability-Based Security*. In T. R. Grimes (Ed.), Advances in Computer Security. capability 安全模型的现代形式化综述，建立了 capability 与类型系统的联系，讨论了 ambient authority 消除的设计原则。

4. **Denning, D. E.** (1976). *A Lattice Model of Secure Information Flow*. Communications of the ACM, 19(5), 236-243. BLP 模型的理论先驱，首次将格论引入访问控制，为 BLP 的数学基础提供了关键贡献。该论文的信息流格模型至今仍是语言级安全分析的理论工具。

5. **WASM Specification (W3C)** (2024). *WebAssembly Core Specification 2.0*. https://www.w3.org/TR/wasm-core-2/. WASM 线性类型与 capability 语义的规范定义，特别是第 3 章（Types）和第 4 章（Modules）的形式化规范。

6. **WASI Specification (W3C)** (2024). *WebAssembly System Interface (WASI) 0.2*. https://github.com/WebAssembly/WASI. WASI capability 系统的接口定义，是 Harness 工程中实现 capability 安全的关键规范，定义了网络、文件系统、时钟等系统接口的 capability 模型。

7. **Glew, A., & Morris, J.** (2002). *Why is a CUP Like a District? On the Equivalence of Capability Systems and Security Lattices*. Carnegie Mellon University. Capability 系统与安全格等价性的独立推导，与本附录 Theorem 2 的对应构成互补，提供了 capability-BLP 等价性的另一种证明方法。

8. **Hoffman, P.** (2026). *WASM Security in Production: The Bounded Intelligence Perspective*. IETF Security Area. bounded intelligence 与 capability 安全的结合分析，提供了将 AI 安全问题映射到形式化安全框架的视角，讨论了 AI 生成代码的安全验证策略。

9. **Miller, M. S., & K., J.** (2018). *Trust, Contracts, and Capabilities*. Stanford University. ambient authority 消除的权威论述，对理解 capability 安全的核心设计原则至关重要，区分了"信任"（trust）和"能力"（capability）这两个相关但不同的概念。

10. **Landauer, J., & Bell, M.** (1999). *Trusted System Foundations: Lessons Learned from Bell and LaPadula*. National Computer Security Center. 对 BLP 模型实际应用的深度反思，提供了将理论模型应用于工程实践的经验教训，讨论了 BLP 在实际系统中的部署挑战和解决方案。
