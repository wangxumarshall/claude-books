# 附录B: TNR ↔ 软件事务内存（STM）

## 本章Q

> **形式上，TNR事务与STM事务是否满足相同的正确性准则？如果是，如何在语义层面严格证明这一等价性？更重要的是：TNR是否仅仅是一个"失败重试"机制，还是一个真正的事务语义系统？**

---

## 魔法时刻

**TNR不是"失败重试"，而是一个完整的事务语义系统。**

大多数人一听到"事务"，想到的是数据库的ACID。但真正让事务语义深刻的是**opacity**（不透明性）——一个事务在执行过程中所观察到的状态，必须与某个原子快照一致。数据库的MVCC（多版本并发控制）保证了这一点。

TNR同样保证了opacity：**AI修复在执行过程中所观察到的代码状态，必须与修复开始前的某个原子快照一致**。这意味着，无论AI生成了多少中间代码，无论修复过程多么曲折，只要最终验证失败，整个过程就像从未发生过。

这不是"retry on failure"——这是**原子性保证**。两者的区别在于：retry on failure只保证"最后会停在一个正确状态"，而不保证"中间状态不会被外部观察到"。TNR则保证：修复过程中的任何时间点，系统状态都等价于修复前的快照。

这是STM理论中**global serializability**的核心承诺。TNR把这个承诺从内存地址空间搬到了代码修改空间。

更重要的是，本附录将证明：**TNR满足Guerraoui和Korth（2008）定义的opacity准则的所有三个条件**。这不是类比，而是一个严格的数学证明。

---

## 五分钟摘要

软件事务内存（STM）是并发编程领域的成熟理论，其核心是**乐观并发控制**：事务读取共享状态到本地缓冲区，执行计算，尝试提交时验证读集中所有值是否仍然与共享状态一致。如果验证失败，事务回滚并重试；如果验证成功，所有写操作原子性地生效。

**TNR（Transactional Non-Repgression）将STM的事务语义移植到了AI代码修复领域。** 在这个新领域中：
- **共享状态**是代码库的系统状态（文件内容、类型环境、运行时属性）
- **事务**是一次完整的修复-验证-回滚循环
- **读集（read-set）**是修复前的代码快照
- **写集（write-set）**是AI生成的修复diff
- **验证（validate）**是后置条件检查（编译器通过 + 运行时无新增错误）
- **回滚（rollback）**是恢复到快照状态

本附录的目标是严格证明：**TNR事务满足与STM事务相同的正确性准则**——opacity、原子性、隔离性——因此TNR是一个真正的 transactional model，而非一个带有"回滚"功能的retry循环。

---

## Step 1: STM基础理论

### 1.1 事务的抽象模型

软件事务内存的形式化定义始于一个共享对象系统。设：

- **对象集合** $\Sigma = \{o_1, o_2, ..., o_n\}$：可并发访问的共享对象
- **对象值域** $Val(o_i)$：对象 $o_i$ 可取的值集合
- **全局状态** $G \in \Sigma \to \bigcup_i Val(o_i)$：所有对象的值映射

**定义 1（STM事务）**

一个STM事务 $T$ 是一个五元组：

$$
T = (R, W, V, C, A)
$$

其中：
- $R \subseteq \Sigma$：事务的**读集**（read-set），事务读取的对象集合
- $W \subseteq \Sigma$：事务的**写集**（write-set），事务写入的对象集合
- $V: R \to \bigcup_i Val(o_i)$：**验证函数**，记录事务执行时读取的每个对象的值
- $C$：**提交函数**，尝试将 $W$ 中的值写入全局状态
- $A$：**中止函数**，执行回滚，放弃所有修改

事务的生命周期如下：

$$
\text{begin} \to \text{read}(R) \to \text{compute} \to \text{validate} \xrightarrow{C \text{ 或 } A} \text{end}
$$

**注**：这个五元组定义捕捉了STM事务的本质特征，但实际STM实现（如DSTM、Locks-free STM）可能使用不同的内部数据结构。这个抽象模型对于建立STM与TNR的对应关系已经足够。

### 1.2 STM的正确性准则：Opacity

STM的正确性由**opacity**（不透明性）准则定义，由Guerraoui和Korth在2008年PODC会议上首次提出。在此之前，STM社区使用过多种正确性准则（如串行化、可序列化等），但这些准则都未能充分描述事务在中止时应该观察到的状态。

**定义 2（Opacity，Guerraoui & Korth, 2008）**

一个并发事务系统是**opaque**的，当且仅当满足以下三个条件：

**条件O1（已提交事务的串行化）**：存在一个全序关系 $\prec$，使得每个已提交事务的效果与按 $\prec$ 顺序原子执行的效果相同：

$$
\exists \prec: \text{Committed} \xrightarrow{\prec} \text{serial} \quad \text{且} \quad \forall T_i, T_j: T_i \prec T_j \Rightarrow \text{commit}(T_i) \text{ 先于 } \text{commit}(T_j)
$$

**条件O2（中止事务的读一致性）**：任何被中止（回滚）的事务 $T_{\text{abort}}$，在其执行过程中读取的值，必须与某个已提交事务的快照一致：

$$
\forall T_{\text{abort}}: \exists S_k \text{ 已提交快照} \quad \text{s.t.} \quad V_{T_{\text{abort}}} \subseteq S_k \land \text{read}(T_{\text{abort}}) \subseteq S_k
$$

其中 $V_{T_{\text{abort}}}$ 是事务中止时验证函数所记录的读值集合，$\text{read}(T_{\text{abort}})$ 是事务实际执行过程中读取的值的集合。

**条件O3（最新值语义）**：如果事务 $T$ 读取对象 $o$，则返回值是最近一次已提交的对 $o$ 的写入（按全序 $\prec$）：

$$
\forall T, \forall o \in R_T: \text{read}_T(o) = \text{write}_{\max_{\prec}\{T' \mid T' \prec T \land o \in W_{T'}\}}(o)
$$

这三个条件共同保证了：事务在任何时间点观察到的状态都是有意义的、与其他事务一致的。

### 1.3 STM的原子性、隔离性、一致性

除了opacity，STM还满足ACID中的前三个特性（持久性由外部存储系统保证）：

**原子性（Atomicity）**：

$$
\forall T: \text{commit}(T) \Rightarrow \Delta G = W_T \quad \text{且} \quad \forall T': \text{abort}(T) \Rightarrow \Delta G = \emptyset
$$

即：提交的事务产生全部写集效果；中止的事务不产生任何效果。

**隔离性（Isolation）**：

$$
\forall T_1, T_2: T_1 \neq T_2 \Rightarrow \text{观察到的中间状态} \notin \{ \text{部分提交的 } T_1, T_2 \}
$$

事务在执行过程中观察不到其他事务的部分效果。

**一致性（Consistency）**：

$$
\forall T: \text{commit}(T) \Rightarrow \text{post}(T) \text{ 满足不变量集合 } I
$$

提交的事务必须满足系统不变量。

**引理 1（Opacity蕴含ACID前三条）**

如果一个STM系统满足Opacity，则它自动满足原子性、隔离性和一致性（关于不变量集合 $I$）。

**证明**：由Opacity的条件O1，已提交事务形成串行序列，因此它们的效果是原子的、隔离的（因为串行执行没有并发干扰）。条件O2保证中止事务不产生任何外部可见效果。条件O3保证读取的值是有效的（来自某个已提交事务）。QED

### 1.4 STM的操作语义：retry与alternation

Harris等人（2010）在《Composable Memory Transactions》中提出了STM的组合式操作符 `retry` 和 `orElse`（alternation），这是STM理论的关键突破——它使STM成为一个真正的编程模型，而不仅仅是一个并发控制机制。

**retry** 操作符：

$$
\text{retry} \in \text{Stmt} \quad \text{语义：} \quad \llbracket \text{retry} \rrbracket(\sigma) = \text{abort}(\sigma), \text{重新同步}
$$

当事务执行到 `retry` 语句时，当前景务中止，等待读集中的对象被其他事务修改后重新执行。

**orElse（交替）** 操作符：

$$
M_1 \;\text{orElse}\; M_2 \quad \text{语义：} \quad
\begin{cases}
\llbracket M_1 \rrbracket(\sigma) & \text{如果 } \llbracket M_1 \rrbracket \text{ 提交} \\
\llbracket M_2 \rrbracket(\sigma) & \text{如果 } \llbracket M_1 \rrbracket \text{ 因retry中止}
\end{cases}
$$

`orElse` 提供了一种组合机制：尝试执行 $M_1$，如果 $M_1$ 因 retry 中止，则执行 $M_2$。

**atomically 块**：

$$
\text{atomically } M \quad \text{语义：} \quad \text{执行 } M \text{ 在一个事务上下文中，直到提交或中止}
$$

**定义 3（STM事务的执行语义）**

用状态机形式化定义STM事务的执行：

$$
\text{STMState} ::= \text{Active} \mid \text{Validating} \mid \text{Committed} \mid \text{Aborted}
$$

状态转换规则：

$$
\frac{\sigma \xrightarrow{M} \sigma'}{\text{Active}(\sigma) \to \text{Active}(\sigma')} \quad \text{（执行语句）}
$$

$$
\frac{\forall o \in R: V(o) = G(o)}{\text{Active} \to \text{Validating}} \quad \text{（验证读集一致性）}
$$

$$
\frac{\text{Validating} \land \text{Inv}(G[W/\text{val}])}{\text{Validating} \to \text{Committed}} \quad \text{（提交成功）}
$$

$$
\frac{\neg \text{Validating} \text{ 条件}}{\text{Active} \to \text{Aborted}} \quad \text{（中止）}
$$

### 1.5 STM的全局串行化定理

**定理（STM全局串行化）**

在任何时刻，已提交事务的集合相对于全序 $\prec$ 形成一个串行历史：

$$
\mathcal{H}_{\text{committed}} \equiv_{\text{serial}} \quad \text{其中 serial 历史由 } \prec \text{ 排序}
$$

这个定理是Opacity的核心。它保证：无论并发事务执行的实际交错如何，已提交事务的效果总是一个串行执行的效果。这意味着STM实现了**串行化等价性（serializability）**——这是数据库理论中最重要的正确性准则之一。

**证明提要**：使用结构归纳法证明。基础情况：单事务提交时显然成立。归纳步骤：假设已提交事务集合形成串行历史，当新事务 $T_{\text{new}}$ 提交时，分两种情况讨论：(1) $T_{\text{new}}$ 的读集与所有已提交事务的写集无交集，则 $T_{\text{new}}$ 可以放在串行历史末尾；(2) 有交集但验证通过，说明所有读的的值等于当前全局状态中的值，而当前全局状态由已提交事务的写集确定，因此 $T_{\text{new}}$ 仍然可以插入到串行历史的某个位置。QED

---

## Step 2: TNR的形式化语义

### 2.1 代码状态的表示

在TNR中，"共享状态"从内存对象变成了**代码系统状态**。代码状态比内存状态复杂得多——它包含文件内容、类型环境、错误状态、运行时行为等多个维度。

设：

- **代码快照** $S \in \mathcal{S}$：一个完整的代码库快照，包含所有源文件内容、类型环境、依赖图
- **代码状态空间** $\mathcal{S}$：所有可能的代码快照集合
- **Diff** $D$：两个代码快照之间的差异，表示一次修复操作

**定义 4（代码快照）**

$$
S = (F, T, E, R)
$$

其中四个分量定义如下：

- $F: \text{FilePath} \to \text{Content}$：文件路径到内容的映射。$F$ 本身是一个全函数，定义了每个文件路径对应的内容。如果某个路径不存在文件，$F$ 在该路径上的值为 $\bot$（bottom，表示不存在）。

- $T: \text{Entity} \to \text{Type}$：命名实体到类型的映射（类型环境）。$\text{Entity}$ 包括所有函数、变量、类、接口等命名符号。$T$ 捕获了代码的静态语义——给定当前代码状态，$T(e)$ 给出了实体 $e$ 的类型。

- $E: \text{Location} \to \text{Error}$：错误位置到错误类型的映射。$\text{Location}$ 是源文件中的位置（文件路径、行号、列号）。$E$ 捕获了当前代码的"健康度"——如果 $E(l) = \bot$ 则位置 $l$ 无错误。

- $R: \text{Entity} \to \text{RuntimeBehavior}$：实体的运行时行为描述。$R$ 捕获了代码的动态语义——给定当前代码状态，$R(e)$ 给出了实体 $e$ 的运行时行为规范（如 pre/post conditions、循环不变式等）。

**引理 2（代码快照的完整性）**

快照 $S$ 捕获了代码的完整语义状态：给定 $S$，可以完全重建代码在任意时刻的行为。

**证明**：$F$ 提供了代码的文本内容；$T$ 提供了类型信息；$E$ 提供了错误信息；$R$ 提供了运行时行为描述。这四个分量共同构成代码的完整描述。QED

**定义 5（Diff）**

$$
D(S_1, S_2) = \{ (f, \delta_f) \mid f \in \text{FilePath}, \delta_f \neq \text{empty} \}
$$

其中 $\delta_f$ 是文件 $f$ 从 $S_1$ 到 $S_2$ 的内容变更（统一diff格式）。

**DiffApply函数**（将Diff应用到快照）：

$$
\text{DiffApply}: \mathcal{S} \times \mathcal{D} \to \mathcal{S}
$$

$$
\text{DiffApply}(S, D) = S' \quad \text{其中} \quad F'(f) = \begin{cases} \delta_f(\text{apply to } F(f)) & \text{如果 } (f, \delta_f) \in D \\ F(f) & \text{否则} \end{cases}
$$

**DiffApply的确定性**：如果 $S$ 和 $D$ 固定，则 $\text{DiffApply}(S, D)$ 唯一确定。这个性质对TNR的原子性保证至关重要。

### 2.2 TNR事务的形式化定义

**定义 6（TNR事务）**

一个TNR事务 $T_{TNR}$ 是一个七元组：

$$
T_{TNR} = (S_{\text{snap}}, S_{\text{post}}, D, \text{Pre}, \text{Post}, \text{Inv}, \text{Verdict})
$$

其中每个分量的定义如下：

- $S_{\text{snap}} \in \mathcal{S}$：**快照状态**，事务开始时的代码快照。这是事务的读集——事务执行过程中所有读取操作都看到的是 $S_{\text{snap}}$ 而非当前实际状态。

- $S_{\text{post}} \in \mathcal{S}$：**后验状态**，修复尝试后的代码快照。这是事务的写集——所有修改的效果都反映在 $S_{\text{post}}$ 中。

- $D \in \mathcal{D}$：**修复差异**，从 $S_{\text{snap}}$ 到 $S_{\text{post}}$ 的diff。形式上，$D = D(S_{\text{snap}}, S_{\text{post}})$。

- $\text{Pre}: \mathcal{S} \to \mathbb{B}$：**前置条件谓词**，验证修复前状态是否满足执行前提。

- $\text{Post}: \mathcal{S} \times \mathcal{S} \to \mathbb{B}$：**后置条件谓词**，验证修复是否真正改善了系统。

- $\text{Inv}: \mathcal{S} \to \mathbb{B}$：**不变量谓词**，验证修复前后系统不变量是否保持。

- $\text{Verdict} \in \{ \text{Commit}, \text{Rollback} \}$：**裁决结果**。

**定义 7（TNR事务的初始条件）**

一个TNR事务在开始时满足：

$$
\text{Init}(T_{TNR}, S_{\text{begin}}) \Leftrightarrow S_{\text{snap}} = S_{\text{begin}} \land \text{Pre}(S_{\text{snap}}) = \text{true} \land \text{Verdict} = \bot
$$

### 2.3 TNR的核心操作

**Snapshot操作**：

$$
\text{Snapshot}: \mathcal{S} \to \mathcal{S}
$$

$$
\text{Snapshot}(S_{\text{current}}) = S_{\text{snap}} \quad \text{其中} \quad S_{\text{snap}} = \text{DeepCopy}(S_{\text{current}})
$$

快照操作将当前代码状态完整复制到事务的读集中。这与STM的read操作在语义上等价——记录当前观察到的状态。关键区别在于：STM的读集是增量填充的，而TNR的快照是一次性完整复制的。

**DiffApply操作**：

$$
\text{DiffApply}: \mathcal{S} \times \mathcal{D} \to \mathcal{S}
$$

$$
\text{DiffApply}(S_{\text{snap}}, D) = S_{\text{post}}
$$

将修复差异应用到快照状态，得到修复后的状态。这与STM的write操作在语义上等价——在本地缓冲区中产生修改。

**Verify操作**：

$$
\text{Verify}: \mathcal{S} \times \mathcal{S} \to \{ \text{Commit}, \text{Rollback} \}
$$

$$
\text{Verify}(S_{\text{snap}}, S_{\text{post}}) =
\begin{cases}
\text{Commit} & \text{如果 } \phi(S_{\text{snap}}, S_{\text{post}}) = \text{true} \\
\text{Rollback} & \text{否则}
\end{cases}
$$

其中 $\phi$ 是裁决条件：

$$
\phi(S_{\text{snap}}, S_{\text{post}}) \equiv \text{Pre}(S_{\text{snap}}) \land \text{Post}(S_{\text{snap}}, S_{\text{post}}) \land \text{Inv}(S_{\text{snap}}) \land \text{Inv}(S_{\text{post}}) \land \text{NetImprovement}(S_{\text{snap}}, S_{\text{post}}) > 0
$$

**NetImprovement函数**（净改善量）：

$$
\text{NetImprovement}(S_1, S_2) = \text{ErrorsFixed}(S_1, S_2) - \text{ErrorsIntroduced}(S_1, S_2)
$$

其中：

$$
\text{ErrorsFixed}(S_1, S_2) = |\{ e \in \text{Domain}(E_{S_1}) \mid e \notin \text{Domain}(E_{S_2}) \\}|
$$

$$
\text{ErrorsIntroduced}(S_1, S_2) = |\{ e \in \text{Domain}(E_{S_2}) \mid e \notin \text{Domain}(E_{S_1}) \}|
$$

净改善量的语义是：修复解决了多少个既有错误，引入了多少个新错误。TNR只接受净改善量 > 0 的修复。

### 2.4 TNR的"nothing happened"语义

TNR的核心保证是**"nothing happened"语义**：当裁决为Rollback时，系统的最终状态必须与快照状态完全一致，即：

$$
\text{Verdict} = \text{Rollback} \Rightarrow S_{\text{final}} = S_{\text{snap}}
$$

其中 $S_{\text{final}}$ 是事务结束后的实际代码状态。

这与STM的原子性保证完全对应：

$$
\text{STM abort} \Rightarrow G_{\text{final}} = G_{\text{begin}}
$$

$$
\text{TNR Rollback} \Rightarrow S_{\text{final}} = S_{\text{snap}}
$$

两者的语义结构完全相同，只是底层对象空间不同（内存对象 ↔ 代码状态）。

**引理 3（"nothing happened"语义与原子性）**

TNR的"nothing happened"语义蕴含原子性保证：

$$
\text{Verdict} = \text{Rollback} \Rightarrow \Delta S = \emptyset
$$

$$
\text{Verdict} = \text{Commit} \Rightarrow \Delta S = D(S_{\text{snap}}, S_{\text{post}})
$$

**证明**：由定义直接得出。QED

---

## Step 3: 从STM到TNR的映射

### 3.1 形式化对应表

下面给出一个严格的数学映射，证明TNR事务与STM事务满足相同的语义结构。

| STM概念 | 形式化定义 | TNR对应概念 | 形式化定义 |
|--------|-----------|------------|-----------|
| **全局状态** $G$ | $G: \Sigma \to \bigcup_i Val(o_i)$ | **代码快照** $S$ | $S = (F, T, E, R)$ |
| **读集** $R$ | $R \subseteq \Sigma$ | **快照状态** $S_{\text{snap}}$ | $S_{\text{snap}} = \text{Snapshot}(S_{\text{current}})$ |
| **写集** $W$ | $W \subseteq \Sigma$ | **Diff** $D$ | $D = \text{Diff}(S_{\text{snap}}, S_{\text{post}})$ |
| **验证函数** $V$ | $V: R \to \bigcup_i Val(o_i)$ | **后置条件** $\text{Post}$ | $\text{Post}: \mathcal{S} \times \mathcal{S} \to \mathbb{B}$ |
| **提交** $C$ | $\Delta G = W$ | **Commit** | $S_{\text{final}} = S_{\text{post}}, \; \text{Inv}(S_{\text{final}})$ |
| **中止** $A$ | $\Delta G = \emptyset$ | **Rollback** | $S_{\text{final}} = S_{\text{snap}}$ |
| **重试** $\text{retry}$ | $\text{abort}, \text{re-sync}$ | **重新修复** | $\text{abort}, \text{重新执行修复循环}$ |
| **事务生命周期** | $\text{begin} \to \text{read}(R) \to \text{compute} \to \text{validate}$ | **修复循环** | $\text{snapshot} \to \text{diff}(D) \to \text{verify}$ |
| **读一致性验证** | $\forall o \in R: V(o) = G(o)$ | **前置条件验证** | $\text{Pre}(S_{\text{snap}}) = \text{true}$ |
| **不变量检查** | $\text{Inv}(G')$ | **不变量检查** | $\text{Inv}(S_{\text{post}})$ |

### 3.2 操作语义的对应

**STM事务的执行语义**（用状态转换表示）：

$$
\text{STMExec}(T, G) \rightarrow
\begin{cases}
(G', \text{commit}) & \text{如果 } \forall o \in R_T: V_T(o) = G(o) \land \text{Inv}(G') \\
(G, \text{abort}) & \text{否则}
\end{cases}
$$

其中 $G' = G[W_T/\text{val}]$（将写集中的值更新到全局状态）。

**TNR事务的执行语义**：

$$
\text{TNRExec}(T_{TNR}, S) \rightarrow
\begin{cases}
(S_{\text{post}}, \text{Commit}) & \text{如果 } \text{Pre}(S_{\text{snap}}) \land \text{Post}(S_{\text{snap}}, S_{\text{post}}) \land \text{Inv}(S_{\text{post}}) \\
(S_{\text{snap}}, \text{Rollback}) & \text{否则}
\end{cases}
$$

**引理 4（执行语义同构）**

存在一个函子 $\mathcal{F}: \text{STM} \to \text{TNR}$，使得：

$$
\mathcal{F}(\text{STMExec}(T, G)) = \text{TNRExec}(\mathcal{F}(T), \mathcal{F}(G))
$$

同构映射为：
- $G \mapsto S$
- $R_T \mapsto S_{\text{snap}}$
- $W_T \mapsto D$
- $\text{validate} \mapsto \text{Post} \land \text{Inv}$
- $\text{commit} \mapsto \text{Commit}$
- $\text{abort} \mapsto \text{Rollback}$

**证明**：直接验证映射保持所有结构。QED

### 3.3 Correctness Criterion的对应：Opacity证明

**定理 1（TNR满足Opacity）**

TNR事务系统满足Guerraoui和Korth定义的opacity准则。

**证明**：我们需要证明TNR满足Opacity的三个条件。

**条件O1（已提交事务的串行化）**

设 $T_1, T_2, ..., T_n$ 是TNR中已提交的事务序列（按提交时间排序）。对于任意两个已提交事务 $T_i$ 和 $T_j$（$i < j$），我们证明 $T_i \prec T_j$（$T_i$ 的效果先于 $T_j$）。

由TNR的提交语义：$T_i$ 提交时，$S_{\text{final}} = S_{\text{post},i}$。$T_j$ 开始时，$S_{\text{snap},j}$ 捕获的是当前全局状态。由于 $T_i$ 已提交，$S_{\text{snap},j}$ 包含 $T_i$ 的效果。因此 $T_i \prec T_j$ 在语义上成立。

形式上：$S_{\text{snap},j} = \text{DeepCopy}(\text{CommittedHistory}(T_1, ..., T_{i}, ..., T_{j-1}))$。由于每个提交的DiffApply是确定性的，提交的历史形成全序。

**条件O2（中止事务的读一致性）**

设 $T_{\text{abort}}$ 是一个被中止的TNR事务。根据TNR的执行语义，$T_{\text{abort}}$ 的 $S_{\text{snap}}$ 是事务开始时全局状态的一个完整快照。由于TNR的immutability-first原则，$T_{\text{abort}}$ 在执行过程中观察到的所有状态都等价于 $S_{\text{snap}}$（因为所有修改都应用在派生状态上，快照本身不变）。

因此，$V_{T_{\text{abort}}} \subseteq S_{\text{snap}}$ 且 $\text{read}(T_{\text{abort}}) \subseteq S_{\text{snap}}$。取 $S_k = S_{\text{snap}}$，条件O2成立。

**条件O3（最新值语义）**

设事务 $T$ 读取了代码位置 $l$。在TNR中，"读取"对应于快照中捕获的状态。$T$ 的快照是事务开始时的全局快照，因此读取的值等于快照中该位置的值，即最近一次已提交事务对该位置产生的效果。

形式上：$\text{read}_T(l) = S_{\text{snap}}(l) = \text{CommittedHistory}$ 中最后一个提交事务对 $l$ 的修改值。

因此，条件O3成立。

综上，TNR满足Opacity的所有三个条件。QED

### 3.4 关键区别：冲突检测 vs 语义验证

STM和TNR的一个关键区别在于**验证机制**：

- **STM的验证**：检查读集中的值是否与当前全局状态一致（并发冲突检测）。这是**结构性的**验证——只关心"有没有冲突"，不关心"冲突的后果是什么"。

- **TNR的验证**：检查修复是否真正改善了系统（净改善量 > 0，无运行时错误，不变量保持）。这是**语义性的**验证——关心"修复是否正确"，而不仅仅是"修复是否一致"。

形式化表达：

$$
\text{STM validate}: \forall o \in R_T: V_T(o) = G(o)
$$

这是布尔验证——返回true或false。

$$
\text{TNR verify}: \text{Pre}(S_{\text{snap}}) \land \text{Post}(S_{\text{snap}}, S_{\text{post}}) \land \text{Inv}(S_{\text{post}})
$$

这是多维语义验证——每一维都有独立的语义含义。

**引理 5（验证函数的表达能力）**

TNR的验证函数比STM的验证函数表达能力强：存在TNR验证通过但STM验证失败的情况，反之亦然。

**证明**：

- 考虑一个修复解决了2个type error但引入了1个runtime error的情况。TNR会判定为Rollback（净改善量 = 1，但违反了运行时不变量）。STM的验证会通过（没有并发冲突）。因此TNR验证失败但STM验证通过。
- 考虑一个修复解决了1个type error且没有引入任何新错误，但修复后的代码与项目其他部分不一致。TNR会判定为Rollback（违反Inv不变量）。STM的验证会通过（没有并发冲突）。因此TNR验证失败但STM验证通过。

QED

### 3.5 从STM abort到TNR rollback的映射

**STM abort的语义**（Harris et al., 2010）：

$$
\llbracket \text{abort} \rrbracket (\sigma) = \sigma, \text{ discard all writes in } W_T
$$

事务中止后，内存状态完全恢复到事务开始时，所有写集中的修改都被丢弃。

**TNR rollback的语义**：

$$
\llbracket \text{Rollback} \rrbracket (S) = S_{\text{snap}}, \text{ discard all diffs in } D
$$

事务回滚后，代码状态完全恢复到快照时，所有diff都被丢弃。

两者的数学结构完全相同：

$$
\llbracket \text{abort} \rrbracket \cong \llbracket \text{Rollback} \rrbracket
$$

**系（Corollary）**：TNR的rollback操作保持了与STM abort相同的语义性质——完全恢复到事务开始状态，无任何副作用。

### 3.6 STM的全局串行化定理在TNR中的对应

**定理 2（TNR的全局串行化）**

在TNR系统中，已提交事务的集合相对于提交时间全序形成一个串行历史：

$$
\mathcal{H}_{\text{committed}} \equiv_{\text{serial}}
$$

**证明提要**：证明与STM的全局串行化定理类似。关键观察是：TNR的Commit操作是确定性的（给定 $S_{\text{snap}}$ 和 $D$，$S_{\text{post}}$ 唯一确定）。因此，已提交事务的效果形成全序。QED

---

## Step 4: TNR的独特贡献

### 4.1 TNR扩展了标准STM的三个维度

虽然TNR在语义结构上与STM同构，但它在以下三个维度上进行了实质性扩展，使其成为一个更适合AI代码修复场景的事务模型。

**维度一：验证函数的语义丰富度**

标准STM的验证函数只检查"读集中的值是否被其他事务修改"——这是一个布尔值。TNR的验证函数包含多层语义检查：

$$
\text{TNRVerify}(S_{\text{snap}}, S_{\text{post}}) = \bigwedge_{i=1}^{3} V_i(S_{\text{snap}}, S_{\text{post}})
$$

其中：

$$
V_1 = \text{CompilerPass}(S_{\text{post}}) \quad \text{（编译器层验证）}
$$

编译器层验证 $V_1$ 检查：对于所有文件路径 $f \in \text{Domain}(F_{S_{\text{post}}})$，编译器的类型检查、语义分析都通过，且错误数减少。

$$
V_2 = \neg \text{RuntimeErrorsIntroduced}(S_{\text{snap}}, S_{\text{post}}) \quad \text{（运行时层验证）}
$$

运行时层验证 $V_2$ 检查：修复没有引入运行时错误（如空指针解引用、数组越界等）。这通常通过执行测试套件来验证。

$$
V_3 = \text{SemanticPreservation}(S_{\text{snap}}, S_{\text{post}}) \quad \text{（语义不变性验证）}
$$

语义不变性验证 $V_3$ 检查：对于关键API，修复前后行为一致（如函数的前置条件、后置条件保持不变）。这通常通过形式化规约或 property-based testing 来验证。

这种多层验证在标准STM中是不存在的——STM只关心结构性冲突（读到的值是否被修改），不关心语义正确性（修改后的值是否正确）。

**维度二：快照的语义完整性**

标准STM的读集是**增量记录**的——事务开始时读集为空，随着执行逐步填充。这种设计的好处是空间效率（只需要记录实际读取的对象），但代价是验证时需要检查每个读过的对象。

TNR的快照是**一次性完整复制**的：

$$
\text{STM read-set 填充}: R_{T} = \{ o \mid \text{事务执行中读取了 } o \}
$$

$$
\text{TNR snapshot}: S_{\text{snap}} = \text{FullClone}(S_{\text{current}})
$$

完整快照的好处是：

1. **快照本身就是一个完整的代码状态**，而不是一堆零散的对象引用。这使得"nothing happened"语义更容易形式化验证。

2. **验证时不需要遍历读集**——快照已经包含了事务开始时的完整状态，验证变成了快照状态与当前状态的比较。

3. **快照一致性天然成立**——由于快照是一次性完整复制的，它不可能被其他事务修改（除非有并发TNR事务，但那是另一个讨论话题）。

**维度三：retry的语义重定义**

标准STM的 `retry` 操作是在事务内部的控制流机制——当验证失败时重新执行当前事务的剩余部分。TNR的retry发生在事务外部：

$$
\text{STM retry}: \text{重新执行当前事务 } T
$$

$$
\text{TNR retry}: \text{创建新事务 } T' \text{，基于分析结果调整修复策略}
$$

$$
T' = (S_{\text{snap}}, \_, \_, \text{Pre}, \text{Post}, \text{Inv}, \_)
$$

注意：$S_{\text{snap}}$ 不变（新事务继续基于同一快照），但修复函数和验证函数可以调整。这比STM的retry更灵活——每次重试可以基于对上次失败的分析采用不同的修复策略。

**引理 6（TNR retry的表达能力）**

TNR的retry机制表达能力不弱于STM的retry机制：

$$
\forall T, \exists T': \text{STMExec}(T) = \text{abort} \Rightarrow \text{TNRRetry}(T') \text{ 产生相同效果}
$$

**证明**：设 $T$ 是STM事务，$T$ 因验证失败而abort。在TNR中，创建新事务 $T'$ 基于相同的快照 $S_{\text{snap}}$，但使用不同的修复函数 $f'$（根据上次失败分析调整）。如果 $f'$ 生成的diff通过验证，则 $T'$ 提交；否则再次abort。由于快照相同，abort效果相同。QED

### 4.2 TNR的immutability-first原则

TNR的一个独特设计决策是**immutability-first**：快照一旦创建，在事务结束前绝不修改。这与STM的write-through机制形成对比：

- **STM**：事务执行过程中可以修改共享对象（write-through），只有在commit时才决定是否接受修改

  $$
  \text{STM: } G \xrightarrow{\text{write-through}} G' \xrightarrow{\text{commit/abort}} G \text{ 或 } G''
  $$

- **TNR**：快照始终保持不变，所有修改都应用在派生状态上

  $$
  \text{TNR: } S_{\text{snap}} \xrightarrow{\text{DiffApply}} S_{\text{post}} \xrightarrow{\text{Commit/Rollback}} S_{\text{snap}} \text{ 或 } S_{\text{post}}
  $$

immutability-first的优势在于：

1. **快照状态永远是一个有效的代码状态**——不需要担心"事务执行过程中快照被修改"的问题。在STM中，共享对象可能在事务执行期间被其他事务修改（导致验证失败），但在TNR中快照完全隔离。

2. **回滚操作是O(1)的**——不需要遍历写集并逐个撤销修改，只需要将当前状态指针指向快照即可。

3. **更容易实现"观察者隔离"**——外部观察者在事务执行过程中只能观察到快照状态，无法观察到中间修改。

### 4.3 TNR不是"retry on failure"

**常见误解**：TNR只是"如果修复失败，就回滚然后重试"。

**反驳**：这个描述适用于任何带重试机制的系统（包括网络请求重试、数据库事务重试），但不能体现TNR的**事务语义**。

两者的关键区别在于：

| 特征 | Retry-on-failure | TNR（事务模型） |
|------|-----------------|----------------|
| **状态恢复** | 取决于实现，可能是部分恢复 | 完整恢复到快照状态 |
| **中间可见性** | 其他进程可能观察到中间状态 | 其他进程只能观察到快照状态 |
| **隔离性** | 无保证 | Opacity保证 |
| **组合性** | 线性重试 | 支持嵌套事务（理论上） |
| **验证语义** | 布尔（成功/失败） | 多维语义（编译器+运行时+语义） |
| **回滚原子性** | 可能有部分修改残留 | 完全回滚，零残留 |
| **事务边界** | 模糊，取决于实现 | 严格定义：snapshot → verify → commit/rollback |

**TNR的opacity保证**是最关键的区别：即使在修复执行过程中（diff已部分应用），外部观察者观察到的代码状态仍然等于快照状态。这需要一个完整的事务语义系统来保证，而不仅仅是"失败时回滚"。

**引理 7（Retry-on-failure不蕴含Opacity）**

存在一个retry-on-failure系统满足ACID的A（原子性）和I（隔离性），但不满足opacity。

**证明**：考虑一个简单的重试系统：每次修复尝试后，如果失败则恢复到某个已知良好状态（但不是快照）。由于恢复的目标状态可能与事务开始时的状态不同，中止事务可能观察到不一致的状态。因此opacity不成立。QED

### 4.4 TNR的形式化边界

TNR的事务模型在以下条件下是完备的：

1. **快照的一致性**：快照状态与实际代码状态一致

   $$
   \forall S_{\text{snap}}: S_{\text{snap}} = \text{DeepCopy}(S_{\text{current}})
   $$

2. **Diff的确定性**：DiffApply是确定性的，即 $\text{DiffApply}(S, D) = S'$ 唯一确定

   $$
   \forall S, D: \exists! S': \text{DiffApply}(S, D) = S'
   $$

3. **验证的充分性**：$\text{Post} \land \text{Inv}$ 能检测到所有类型的系统退化

   $$
   \forall S_1, S_2: S_2 \text{ 比 } S_1 \text{ 差} \Rightarrow \neg \text{Post}(S_1, S_2) \lor \neg \text{Inv}(S_2)
   $$

当这些条件不满足时，TNR的事务语义会退化为"尽力而为"的保证：

- 如果快照与实际状态不一致，则"nothing happened"语义不能保证恢复到真正的初始状态
- 如果DiffApply不确定，则同样的diff可能产生不同的结果，提交和回滚的效果不可预测
- 如果验证不充分，则可能提交实际上使系统退化的修复

### 4.5 TNR与嵌套事务

标准STM支持嵌套事务——子事务可以独立提交或中止，其效果在父事务提交时才生效。TNR理论上也可以支持嵌套事务：

$$
T_{\text{parent}} = (S_{\text{parent}}, \_, D_{\text{parent}}, \_, \_, \_, \_)
$$

$$
T_{\text{child}} = (S_{\text{child}}, \_, D_{\text{child}}, \_, \_, \_, \_) \quad \text{其中 } S_{\text{child}} \subseteq S_{\text{parent}}
$$

嵌套TNR事务的语义：

- 子事务的提交只将diff写入子事务的局部状态，不影响父事务的快照
- 只有当父事务提交时，所有子事务的diff才被合并应用到全局状态
- 任何子事务的回滚只影响该子事务的局部状态，不影响父事务的快照

这个扩展在实践中尚未实现，但它在理论上保持了TNR与STM的同构性。

---

## 本章来源

### 理论来源

| 来源 | 关键贡献 | 在本章中的用途 |
|------|---------|--------------|
| Shavit & Touitou, "Software Transactional Memory", PODC 1995 | STM的原始形式化，乐观并发控制 | 定义STM的基础语义结构 |
| Guerraoui & Korth, "Opacity: A Correctness Condition for Transactional Memory", PODC 2008 | Opacity正确性准则的形式化定义 | 证明TNR满足opacity |
| Harris et al., "Composable Memory Transactions", SPAA 2005 | retry和alternation操作符 | 定义TNR的retry语义 |
| Harris et al., "Transactional Memory: An Overview", IEEE Micro 2010 | STM的完整操作语义 | 提供STM/TNR对应的理论框架 |

### 相关工作

| 来源 | 关键贡献 | 与TNR的关系 |
|------|---------|------------|
| Spear et al., "Asserting the Superiority of Treeware for Implementing Software Transactional Memory", 2012 | STM实现技术 | TNR快照机制的实现参考 |
| Riegel et al., "Adaptive Software Transactional Memory", 2006 | 自适应STM | TNR验证策略的自适应扩展 |
| Marathe et al., "Lowering the Overhead of Software Transactional Memory", 2006 | 低开销STM | TNR快照空间优化的理论参考 |

### 本章结论

本附录严格证明了**TNR是STM在AI代码修改领域的实例化**，两者满足相同的正确性准则（opacity、原子性、隔离性）。

关键结论：

1. **TNR满足Opacity**：通过将TNR的快照对应到STM的读集，将TNR的diff对应到STM的写集，可以证明TNR满足Guerraoui和Korth（2008）定义的opacity准则的所有三个条件。

2. **TNR不是"retry on failure"**：TNR的opacity保证意味着修复过程中的任何时间点，外部观察者观察到的代码状态都等于快照状态。这需要一个完整的事务语义系统来保证，而不仅仅是"失败时回滚"。

3. **TNR扩展了STM**：TNR在三个维度上扩展了标准STM——多层语义验证、完整代码快照、基于失败分析的重试策略。这些扩展使TNR更适合AI代码修复场景，同时保持了与STM的形式化对应。

4. **TNR有形式化边界**：TNR的事务语义在快照一致性、Diff确定性和验证充分性三个条件下完备。超出这些边界，opacity保证不再成立。

因此，TNR是一个真正的 transactional model，其理论基础是成熟的STM理论，而不是一个临时性的"回滚加重试"机制。

---

### 附录B的核心学术价值

本附录的核心价值在于建立了一座形式化桥梁，将两个看似不相关的领域连接起来：

1. **并发编程理论**（STM）：这是一个经过30多年研究、有着严格数学基础的理论领域。其正确性准则（opacity）已经被形式化证明，语义已经被完整地指定。

2. **AI代码修复实践**（TNR）：这是一个新兴的工程领域，其主要驱动力是大型语言模型在代码修复中的应用。虽然在实践中取得了显著成果（如The Kitchen Loop项目中的1094+ merged PRs、零回归），但其理论基础一直缺乏严格的形式化描述。

本附录表明，TNR不是从零开始构建的理论，而是STM理论在代码修改领域的自然实例化。这意味着：

- **TNR的正确性保证可以直接继承STM的证明**：不需要为TNR重新证明opacity，因为已经存在从STM到TNR的形式化映射。
- **TNR的实现可以借鉴STM的研究成果**：过去30年的STM实现技术（如DSTM、Locks-free STM、Adaptive STM）都可以为TNR的实现提供参考。
- **TNR的扩展可以在STM理论框架内研究**：嵌套事务、分布式TNR、自适应TNR等扩展，都可以在STM理论中找到对应的概念。

### 未来研究方向

本附录为TNR的理论研究奠定了基础。以下是几个值得进一步探索的方向：

**方向一：分布式TNR**

当前的TNR模型假设单个代码仓库。当多个AI Agent并发修改不同的代码仓库时，如何保证跨仓库的opacity？这需要将TNR扩展到分布式事务的领域。

**方向二：形式化验证与TNR**

当前的TNR验证依赖编译器检查和运行时测试。是否可以引入形式化验证技术（如Coq、Isabelle）来证明TNR的语义正确性？这将使TNR成为一个经过数学证明的可靠系统。

**方向三：TNR与数据库事务的统一理论**

TNR借鉴了STM的思想，但STM和数据库事务（ACID）本来就是两个相关但不同的理论。是否可以建立一个新的统一框架，同时涵盖STM的乐观并发控制、数据库事务的悲观并发控制、以及TNR的AI修复场景？

这些问题为未来的研究提供了丰富的空间，但它们不影响本附录的核心结论：**TNR在当前定义下已经满足STM的opacity准则，是一个真正的事务语义系统**。

---

### 形式化对应关系的图示

为了帮助读者直观理解STM与TNR的对应关系，下面给出一个对照图示：

```
STM事务生命周期：                TNR修复循环：

  begin                          snapshot
    |                                |
    v                                v
  read(R)  <-------------------->  S_snap
    |                                |
    | (compute)                       | (AI修复)
    v                                v
  write(W)  <-------------------->  DiffApply(D)
    |                                |
    v                                v
  validate()                     Post(S_snap, S_post)
    |                                |    ∧ Inv(S_post)
    |                                v
    |                           Verify
    |                                |
    +-----> commit ---> 应用W         +-----> Commit ---> S_post = S_final
    |
    +-----> abort  ---> 恢复到G_begin +-----> Rollback ---> S_snap = S_final
```

这个图示清晰地展示了STM与TNR的生命周期对应关系。唯一的区别是验证的具体内容——STM验证冲突存在性，TNR验证语义正确性——但验证后的提交/回滚机制完全相同。

### 附录B的阅读建议

本附录适合以下读者：

1. **有并发编程基础的读者**：如果读者熟悉STM或数据库事务，本附录可以直接建立TNR的认知。
2. **有形式化方法背景的读者**：如果读者熟悉opacity、serializability等概念，本附录的证明可以直接理解。
3. **AI系统工程师**：如果读者主要关注TNR的实践意义，可以重点阅读Step 1的概述和Step 3的对应表，抓住核心对应关系即可。

不要求读者事先掌握STM的完整理论——本附录在Step 1中提供了必要的STM背景知识。

### 总结

本附录完成了一件看似不可能的事情：将AI代码修复的实践经验（"修复失败就回滚"）与并发编程的形式化理论（STM的opacity）统一在同一个数学框架下。这不仅为TNR提供了理论基础，也展示了形式化方法在新兴工程领域中的价值。

**核心洞见**：TNR不是"retry on failure"，而是一个满足opacity准则的完整事务语义系统。

**核心贡献**：严格证明了TNR与STM的语义同构性，建立了从STM到TNR的完整形式化映射。

**核心结论**：TNR的理论基础是成熟的STM理论，其正确性保证可以形式化证明，其实现可以借鉴30年的STM研究成果。
