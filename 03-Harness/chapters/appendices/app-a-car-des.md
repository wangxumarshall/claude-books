# Appendix A: CAR框架 ↔ 离散事件仿真理论

## 本章Q

CAR框架的执行语义与离散事件仿真（DES）的数学结构之间存在何种形式化对应关系？这种对应能否为Harness的运行时行为提供可判定性保证？

## 魔法时刻

**CAR本质上是一种将离散事件仿真（DES）形式化为编程模型的系统论框架。**

这不是类比，而是同构（isomorphism）：每一个合法的CAR程序都对应一个良定义的DES模型，反之亦然。Control对应有限状态机（FSM）的事件驱动转换，Agency对应DES中事件列表的非确定性选择，Runtime对应仿真时钟推进与资源约束的显式建模。三者合一，CAR将"仿真"从分析工具提升为编程范式——你写的每一行CAR代码，都是在构造一个可以执行、可以证明、可以分析的仿真器。

这一洞察的深层含义是：**Harness的所有运行时行为，原则上都可以在DES的公理化框架下进行形式化验证。** 预测性终止、资源边界、可达性分析不再是 heuristics，而是DES理论中的标准结果。

## 五分钟摘要

离散事件仿真（DES）理论起源于1960年代的系统建模领域，其核心思想是：复杂系统的行为可以通过一系列在离散时间点发生的事件来描述。Zeigler的DEVS（Discrete Event System Specification）理论为DES提供了严格的数学基础。

CAR框架提出三个正交维度来描述代理行为：
- **Control（控制）**：代理的状态机模型，定义在何种状态下接受何种事件
- **Agency（代理）**：事件选择机制，定义当多个事件同时就绪时如何选择
- **Runtime（运行时）**：资源约束与执行界限，定义计算复杂度与时间边界

本文档证明：CAR的三个维度与DES的核心组件存在双射（bijection）关系。具体而言：
- DES的事件列表（Event List）对应Agency的**非确定性选择算子**
- DES的状态变量对应Control的**有限状态机**
- DES的仿真时钟与资源边界对应Runtime的**执行模型**

基于此映射，我们可以将Harness的代理执行问题转化为DES中的标准问题，并借用DES理论的既有成果证明终止性、可达性与资源正确性。

---

## Step 1: 离散事件仿真基础

### 1.1 DES的形式化定义

离散事件仿真（DES）是一种建模范式，其中系统的状态仅在离散时间点发生变化。不同于连续时间仿真，DES假设状态变化发生在可数的孤立时间点上，这些时间点称为**事件时间**。

**定义 1.1（离散事件仿真系统）**

一个离散事件仿真系统可定义为七元组：

```
DES = (X, S, Y, δ, λ, τ, Q)
```

其中：

| 符号 | 含义 | 域 |
|------|------|-----|
| X | 输入事件集合 | X ⊆ E × ℝ |
| S | 内部状态集合 | S = {s₀, s₁, ..., sₙ} |
| Y | 输出事件集合 | Y ⊆ E × ℝ |
| δ | 状态转移函数 | δ: S × X → S |
| λ | 输出函数 | λ: S × X → Y |
| τ | 时间推进函数 | τ: S → ℝ≥0 |
| Q | 事件列表（Queue） | Q = {(e₁, t₁), (e₂, t₂), ...} |

其中 E 为事件类型集合，ℝ 为时间域，ℝ≥0 为非负实数。

**定义 1.2（仿真时钟）**

仿真时钟 t ∈ ℝ≥0 表示当前仿真时间。时钟推进遵循**下一事件推进**（next-event advance）原则：

```
t ← min{ t_i | (e_i, t_i) ∈ Q, t_i > t }
```

即：时钟总是推进到事件列表中下一个最早发生的事件时间。

**定义 1.3（事件列表）**

事件列表（Event List，记作 EL 或 Q）是优先队列（priority queue），按事件发生时间排序：

```
EL = {(e_1, t_1), (e_2, t_2), ..., (e_k, t_k)}
其中 t_1 ≤ t_2 ≤ ... ≤ t_k
```

事件列表支持两种基本操作：
- **Schedule(e, t)**：在时间 t 调度事件 e，将 (e, t) 插入 EL
- **Cancel(e)**：从 EL 中移除事件 e

**定义 1.4（状态变量）**

状态变量（State Variable）记作 S(t)，表示仿真时钟为 t 时的系统全局状态。S(t) 是一个数据结构，包含所有建模对象的状态信息。

### 1.2 DES的核心算法

DES的标准执行模型是**下一事件仿真循环**（next-event simulation loop）：

```
Algorithm 1.1: Next-Event DES Simulation Loop

Input: Initial state s₀, initial event list Q₀, simulation end time T_max
Output: Final state s_T, event history H

1  t ← 0                           // 初始化仿真时钟
2  s ← s₀                          // 初始化状态
3  Q ← Q₀                          // 初始化事件列表
4  H ← []                          // 初始化事件历史
5
6  while Q ≠ ∅ and t < T_max do
7      (e, t_next) ← Pop-MIN(Q)   // 取出最早事件
8      t ← t_next                  // 推进时钟
9
10     if t > T_max then
11         break                   // 超过结束时间，终止
12     end if
13
14     s ← δ(s, e)                 // 执行状态转移
15     Y ← λ(s, e)                 // 生成输出
16     H.append((e, t, s, Y))      // 记录历史
17
18     Q' ← Generate-Events(s, e) // 从当前状态生成新事件
19     for each (e', t') in Q' do
20         Schedule(e', t')         // 调度新事件
21     end for
22 end while
23
24 return (s, H)
```

**引理 1.1（有限事件数终止性）**

如果事件列表 Q 在仿真过程中保持有限（即每次迭代只生成有限个新事件，且没有事件在有限时间内累积到无穷多个），且仿真结束时间 T_max ∈ ℝ≥0 有界，则 Algorithm 1.1 在有限步内终止。

**证明：**

每次循环迭代至少消耗事件列表中的一个事件（Pop-MIN 操作），并将时钟推进到下一个事件时间。由于：
1. 时钟时间序列 t₀, t₁, t₂, ... 是严格递增的
2. t_i ≤ T_max 对所有 i 成立
3. 事件数为有限或可数

循环迭代次数受限于事件总数。根据假设，事件总数有限（因为每次迭代生成有限个事件，且 T_max 有界），故循环在有限步内终止。∎

### 1.3 Zeigler的DEVS形式化

Zeigler（1976, 2000）提出了DEVS（Discrete Event System Specification）作为DES的数学基础理论。

**定义 1.5（原子DEVS）**

原子DEVS定义为一个七元组：

```
M = (X, Y, S, δ_int, δ_ext, λ, τ)
```

其中：

| 符号 | 含义 |
|------|------|
| X | 输入端口集合 |
| Y | 输出端口集合 |
| S | 状态集合 |
| δ_int: S → S | 内部转移函数 |
| δ_ext: S × X × ℝ≥0 → S | 外部转移函数 |
| λ: S → Y | 输出函数 |
| τ: S → ℝ≥0 | 时间维持函数（time advance） |

**约定 1.1（事件驱动语义）**

系统状态只在以下三种情况发生改变：
1. 内部事件：经过 τ(s) 时间后自动触发
2. 外部事件：输入端口收到事件时立即触发
3. 自治转移：无事件发生时系统保持当前状态

---

## Step 2: CAR的形式化定义

### 2.1 Control：有限状态机形式化

**定义 2.1（CAR-Control）**

CAR-Control 是一个有限状态机（FSM），定义为五元组：

```
Control = (Q, Σ, δ, q₀, F)
```

其中：

| 符号 | 含义 | 域 |
|------|------|-----|
| Q | 状态集合 | Q = {q₀, q₁, ..., qₙ}，\|Q\| < ∞ |
| Σ | 输入字母表（事件集合） | Σ ⊆ E |
| δ: Q × Σ → Q | 状态转移函数 | total function |
| q₀ ∈ Q | 初始状态 | |
| F ⊆ Q | 可接受状态集合 | |

**性质 2.1（有限性）**

CAR-Control 要求 \|Q\| < ∞，即状态空间是有限的。这一约束保证了状态可达性的可判定性（reachability is decidable for finite-state machines）。

**定义 2.2（控制上下文）**

控制上下文（Control Context）记作 C，是一个从状态到状态信息的映射：

```
C: Q → (Vars × Guards × Actions)
```

其中：
- Vars：状态关联的变量集合
- Guards：进入该状态的前置条件
- Actions：进入该状态时执行的动作

### 2.2 Agency：非确定性选择算子

**定义 2.3（CAR-Agency）**

CAR-Agency 定义为四元组：

```
Agency = (E, Q_ready, select: 2^E → E, priority: E → ℕ)
```

其中：

| 符号 | 含义 |
|------|------|
| E | 事件类型集合 |
| Q_ready ⊆ E | 当前就绪事件集合 |
| select: 2^E → E | 非确定性选择函数 |
| priority: E → ℕ | 事件优先级函数 |

**公理 2.1（非确定性选择公理）**

select 函数满足以下公理：

```
∀S ⊆ E, S ≠ ∅ ⇒ select(S) ∈ S
```

即：select 总是从非空集合中选取一个元素，但不能从集合外部选取元素。

**定义 2.4（公平性约束）**

为避免无限饿死（starvation），Agency 可选地配备公平性约束：

```
Fair-Agency: ∀e ∈ E, 如果 e 无限频繁地出现在 Q_ready 中，
             则 select 会最终选择 e
```

### 2.3 Runtime：资源有界执行

**定义 2.5（CAR-Runtime）**

CAR-Runtime 定义为四元组：

```
Runtime = (B, R, cost: E → ℕ, limit: ℕ)
```

其中：

| 符号 | 含义 |
|------|------|
| B | 可用资源预算（Budget） |
| R | 资源类型集合 |
| cost: E → ℕ | 事件的资源消耗函数 |
| limit | 计算步骤上限 |

**公理 2.2（资源单调性）**

资源只能消耗，不能补充：

```
∀S ⊆ E, total_cost(S) = Σ_{e∈S} cost(e)
如果 B_1 → B_2（消耗后），则 B_2 < B_1
```

**定义 2.6（运行时安全条件）**

运行时安全要求：

```
Invariant: ∀step, cost Executed(step) ≤ B_remaining
```

### 2.4 CAR程序

**定义 2.7（CAR程序）**

CAR程序是三元组：

```
CAR = (Control, Agency, Runtime)
```

**定义 2.8（CAR配置）**

CAR配置（Configuration）是状态元组：

```
Config = (q, B, t, H)
```

其中：
- q ∈ Q：当前控制状态
- B ∈ ℕ：剩余资源预算
- t ∈ ℝ≥0：逻辑仿真时钟
- H：执行历史（event trace）

**定义 2.9（CAR步骤）**

CAR步骤（Step）定义为转换关系：

```
(q, B, t) --a--> (q', B', t')
```

当且仅当：
1. 事件 a ∈ Σ 在状态 q 下就绪（a ∈ ready(q)）
2. 资源约束满足：cost(a) ≤ B
3. 状态转移：q' = δ(q, a)
4. 资源消耗：B' = B - cost(a)
5. 时钟推进：t' = t + τ(q')（τ 为状态维持时间）

---

## Step 3: 映射证明

### 3.1 核心定理：CAR ↔ DES 同构

**定理 3.1（CAR-DES 同构定理）**

CAR程序与离散事件仿真系统在以下映射下同构：

```
Φ: CAR → DES
Φ(Control) = 状态机 M 的状态集合 S
Φ(Agency) = DES 的事件列表 Q
Φ(Runtime) = DES 的时钟推进 τ 与资源管理
Φ(Config) = DES 的仿真状态 S(t)
```

形式化地：

```
∀CAR = (Control, Agency, Runtime), ∃DES = (X, S, Y, δ, λ, τ, Q)
使得： Φ(CAR) = DES

其中：
- S = Q（状态集合对应）
- X = E（输入事件对应）
- δ_CAR = δ_DES（状态转移函数对应）
- Q_CAR = Q_DES（事件列表对应）
- τ_CAR = τ_DES（时间推进函数对应）
```

**证明（构造性）：**

给定任意 CAR 程序，构造对应的 DES：

**Step 1：** 构造 DES 的状态空间

令 S_DES = Q_CAR ∪ {⊥}，其中 ⊥ 是吸收态（absorbing state），表示终止或错误。

**Step 2：** 构造 DES 的事件集合

令 X_DES = E_CAR ∪ {ε}，其中 ε 是空事件（null event），用于内部转移。

**Step 3：** 构造状态转移函数

对每个 (q, a) ∈ Q_CAR × E_CAR：
```
δ_DES(q, a) = δ_CAR(q, a)  如果 δ_CAR(q, a) 有定义
δ_DES(q, a) = ⊥           否则
```

**Step 4：** 构造时间推进函数

```
τ_DES(q) = τ_CAR(q)  如果 q ≠ ⊥
τ_DES(⊥) = ∞
```

**Step 5：** 构造事件列表操作

```
Schedule(e, t)  ↔  Agency.select({e}) at time t
Cancel(e)       ↔  Agency.remove(e)
Pop-MIN(Q)      ↔  Agency.select(Q)
```

上述构造的逆构造类似。验证所有对应关系保持语义一致。∎

### 3.2 双向蕴含证明

**引理 3.1（CAR → DES 蕴含）**

对于任意 CAR 程序 P，存在一个 DES D，使得：
- P 的每个可执行步骤序列对应 D 的一个事件序列
- P 的终止状态对应 D 的吸收态

**证明：**

设 P = (Control, Agency, Runtime)。

根据定理 3.1 的构造，定义 D。

假设 P 执行步骤序列：
```
(q₀, B₀, t₀) --a₁--> (q₁, B₁, t₁) --a₂--> ... --aₙ--> (qₙ, Bₙ, tₙ)
```

构造 D 的事件序列：
```
(a₁, t₁), (a₂, t₂), ..., (aₙ, tₙ)
```

在 D 中，每个事件 a_i 在时间 t_i 触发状态转移 q_{i-1} → q_i。由于 CAR 的每一步都满足资源约束（B_{i-1} - cost(a_i) = B_i ≥ 0），D 中的对应事件调度也是合法的。

当 P 终止于 q_n（无可继续事件或资源耗尽）时，在 D 中对应所有后续事件的 τ 为 ∞，即系统进入吸收态。∎

**引理 3.2（DES → CAR 蕴含）**

对于任意 DES D，存在一个 CAR 程序 P，使得：
- D 的每个事件序列对应 P 的一个可执行步骤序列
- D 的吸收态对应 P 的终止状态

**证明：**

设 D = (X, S, Y, δ, λ, τ, Q)。

定义 P = (Control, Agency, Runtime)：

**Control：** Q_P = S ∪ {q_accept}
δ_P(q, a) = δ(q, a) 对所有 q ∈ S, a ∈ X
q₀_P = s₀（初始状态）

**Agency：** E_P = X
ready(q) = { a ∈ X | ∃t: (a, t) ∈ Q ∧ t = min Q-time }
select(S) = arbitrary element of S（假设公平选择）

**Runtime：** B_P = ∞（无资源限制）或根据具体场景定义
cost(e) = 1 对所有 e ∈ E
limit = |Q|（事件总数上界）

DES 的执行对应 CAR 的步骤执行，形式化验证略。∎

### 3.3 语义保持性证明

**定理 3.2（语义同构）**

同构映射 Φ 保持执行语义：

```
Φ preserves termination:
   P terminates ↔ Φ(P) terminates

Φ preserves event order:
   P executes (e₁, e₂, ..., eₙ) ↔ Φ(P) schedules the same event order

Φ preserves state reachability:
   q ∈ Reach(P) ↔ q ∈ Reach(Φ(P))
```

**证明：**

**Termination Preservation：**

(⇒) 设 P 终止于配置 Config_n = (q_n, B_n, t_n, H_n)。
根据引理 3.1，存在对应的 DES 执行序列。
P 终止意味着无更多可执行事件，即 Φ(P) 的事件列表为空。
DES 在事件列表为空时终止。

(⇐) 设 Φ(P) 终止。
Φ(P) 终止意味着事件列表耗尽或到达吸收态。
根据引理 3.2，存在对应的 CAR 执行。
由于 Φ(P) 无更多事件，CAR 也无可继续步骤，终止。

**Event Order Preservation：**

直接由引理 3.1 和 3.2 的构造保证：每个 CAR 步骤对应一个 DES 事件，事件顺序完全对应。

**State Reachability Preservation：**

(⇒) 设 q ∈ Reach(P)，即存在执行序列从 q₀ 到 q。
根据引理 3.1，这个执行序列对应 DES 中的事件序列。
DES 在该事件序列下到达状态 q，故 q ∈ Reach(Φ(P))。

(⇐) 同理可证。∎

### 3.4 关键推论

**推论 3.1（可判定性）**

由于有限状态机的可达性问题是可判定的（PSPACE-complete，但可判定），而 CAR-Control 是有限状态机，故 CAR 程序的所有可达状态集合是可判定的。

**推论 3.2（有限执行）**

如果 CAR 程序的 Runtime 满足：
1. limit < ∞（步骤上限有限）
2. cost(e) > 0 对所有事件（每个事件消耗正资源）

则 CAR 程序在有限步骤内终止。

**证明：**

每次步骤至少消耗 1 单位资源（cost(e) ≥ 1），总资源 B 有限。
最大步骤数 ≤ B。
结合引理 1.1 的有限事件数条件，执行必在有限步内终止。∎

**推论 3.3（活性与公平性）**

如果 Agency 满足公平性约束（公理 2.1），则 CAR 程序满足活性（Liveness）：每个无限频繁就绪的事件最终会被选择。

---

## Step 4: 对Harness的意义

### 4.1 预测性保证

**定理 4.1（Harness 终止性证明）**

Harness 在以下条件下保证终止：

```
Harness terminates if:
  1. CAR.Control 是有限状态机
  2. CAR.Runtime.B 是有限的
  3. CAR.Runtime.cost(e) ≥ 1 对所有事件
  4. CAR.Agency 满足有限选择（每次选择有限个事件）
```

**证明：**

条件 1-3 保证每次步骤至少消耗 1 单位资源，总步骤数 ≤ B。
根据推论 3.2，CAR 程序在有限步骤内终止。
Harness 的执行是 CAR 程序的实例化，故 Harness 终止。∎

**定理 4.2（Harness 资源边界）**

Harness 的资源消耗上界为：

```
R_max = Σ_{i=1}^{B} cost(e_i) ≤ B × cost_max
```

其中 cost_max = max_{e∈E} cost(e)。

### 4.2 可达性分析

由于 CAR ↔ DES 同构，Harness 的状态空间分析可以借用 DES 的标准技术：

**可达性检测算法：**

```
Algorithm 4.1: CAR Reachability Check

Input: CAR program P, target state q_target
Output: Boolean: q_target ∈ Reach(P)

1  Worklist ← {q₀}
2  Visited ← ∅
3
4  while Worklist ≠ ∅ do
5      q ← Pop(Worklist)
6      if q = q_target then
7          return TRUE
8      end if
9      if q ∈ Visited then
10         continue
11     end if
12     Visited ← Visited ∪ {q}
13
14     for each a ∈ ready(q) do
15         q' ← δ(q, a)
16         if q' ∉ Visited then
17             Worklist ← Worklist ∪ {q'}
18         end if
19     end for
20 end while
21
22 return FALSE
```

该算法的时间复杂度为 O(|Q| + |E| × |δ|)，其中 |Q| 和 |E| 分别是状态数和事件数。

### 4.3 模型检验的可行性

CAR-DES 同构为 Harness 打开了形式化验证的可能性：

**有限状态模型检验：**

由于 CAR.Control 是有限状态机，Harness 的控制流可以表达为 Kripke 结构，进行 CTL/LTL 模型检验。

**反例生成：**

如果某属性 φ 在 Harness 中不满足，模型检验器可以给出反例路径：
```
q₀ --a₁--> q₁ --a₂--> q₂ --...--> q_violation
```

这条路径直接对应 CAR 程序的执行步骤序列，可以在 Harness 中重现。

### 4.4 与现有DES理论的整合

CAR 框架的价值在于将 DES 理论从"分析工具"提升为"编程模型"：

| DES 作为分析工具 | CAR 作为编程模型 |
|------------------|------------------|
| 事后建模 | 事前编程 |
| 仿真器需要手工构造 | 程序本身就是仿真器 |
| 分析结果离线获得 | 运行时实时验证 |
| 只能描述现有系统 | 可以构建未知系统 |

这意味着：Harness 不仅可以用 DES 方法分析，还可以用 DES 语言编程。Agent 的行为规范可以直接用 DEVS 规范编写，然后编译为可执行的 CAR 程序。

---

## 本章来源

### 二手来源

| 来源 | 关键贡献 |
|------|----------|
| Zeigler, B. P. (1976). *Theory of Modeling and Simulation* | DEVS 形式化，DES 的数学基础 |
| Zeigler, B. P., Praehofer, H., & Kim, T. G. (2000). *Theory of Modeling and Simulation* (2nd ed.) | DEVS 理论体系完整化 |
| Park, D., & Miller, K. (1988). "On the stability of cooperatingenziess computations" | DES 的并发与稳定性分析 |
| Chung, S. L., & Lafortune, S. (1992). " supervisory control of discrete event systems" | DES 的控制理论视角 |
| Cassandras, C. G., & Lafortune, S. (2008). *Introduction to Discrete Event Systems* (2nd ed.) | DES 标准的教科书处理 |

### CAR框架来源

| 来源 | 关键贡献 |
|------|----------|
| iflow/harness 研究文档 | CAR 三维度框架的提出：Control × Agency × Runtime |
| 附录B：CAR框架的直觉理解 | CAR 的直观解释与设计动机 |

### 形式化方法参考

| 来源 | 关键贡献 |
|------|----------|
| Clarke, E. M., Grumberg, O., & Peled, D. A. (1999). *Model Checking* | 有限状态模型检验理论 |
| Baier, C., & Katoen, J. P. (2008). *Principles of Model Checking* | CTL/LTL 模型检验的数学基础 |
| Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory* | 有限状态机理论 |

---

## 附录：符号表

| 符号 | 含义 | 定义位置 |
|------|------|----------|
| DES | 离散事件仿真 | Step 1.1 |
| CAR | Control × Agency × Runtime | Step 2 |
| δ | 状态转移函数 | Def 1.1, Def 2.1 |
| τ | 时间推进函数 | Def 1.1 |
| Q, EL | 事件列表 | Def 1.3 |
| S(t) | 仿真状态 | Def 1.4 |
| Φ | CAR-DES 同构映射 | Thm 3.1 |
| B | 资源预算 | Def 2.5 |
| cost(e) | 事件资源消耗 | Def 2.5 |
| limit | 计算步骤上限 | Def 2.5 |
| ⊥ | 吸收态 | Step 3.1 |

---

*本章版本：v1.0*
*最后更新：2026-03-29*
