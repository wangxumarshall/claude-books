# Filesystem-like 与 Vector/Graph-like Agent Memory 深度研究报告

> 目录：`AgentOS-Memory/fs-vector-graph/`
>
> 更新时间：2026-04-16
>
> 融合来源：`report.md`、`report_v2.md`、`report_v3.md`、`report_v4.md`
>
> 补充核验：截至 `2026-04-16` 的公开一手材料，仅用于校正“业界 SOTA / 公开前沿”判断

---

## 0. 研究范围、方法与先给结论

### 0.1 研究范围

本报告聚焦 **external memory augmentation**，即模型外的持久化记忆系统，不把 Transformer 原生记忆、参数编辑、KV cache 机制本身当作主线。

纳入主研究对象的标准是同时具备三点：

1. **跨会话持久化**
2. **可检索 / 可复用**
3. **可更新 / 可巩固**

因此，本报告的主线对象仍以已有研究材料中的系统为主：

- `Filesystem-like`：`OpenViking`、`memsearch`、`memU`、`Acontext`、`Voyager`、`lossless-claw`、`Memoria`
- `Vector/Graph-like`：`mem0`、`Honcho`、`Graphiti/Zep`、`eion`、`ContextLoom`、`mem9`、`UltraContext`

为回答“业界 SOTA 是什么”，本轮额外补查了截至 `2026-04-16` 的官方 benchmark / research 页面，例如 `Hindsight`、`Mem0`、`Honcho`。这些补充材料只用于界定**公开分数前沿**，不把所有新项目都扩写成完整架构剖析。

### 0.2 为什么把“vector-like”扩展写成“vector/graph-like”

用户问题里使用了 `vector-like`。但到 2025-2026 年，很多所谓 vector memory 已经不再是“纯 embedding 池”，而是演化成：

- 语义检索
- 关键词检索
- 图遍历
- 实体状态表示
- 时间有效窗
- 共享命名空间

所以本报告统一使用 **`vector/graph-like`**，强调它们的主导接口是**中央化语义 / 关系 / 服务平面**，而不再只是传统向量库。

### 0.3 分类规则与证据等级

#### 分类规则

同一系统可能同时有文件层、向量层和图层。本报告按 **主导接口** 归类：

- 主导接口是 `Markdown / 文件树 / URI / skill file / 版本对象`：归为 `filesystem-like`
- 主导接口是 `API / SDK / shared memory pool / vector retrieval / graph retrieval / managed service`：归为 `vector/graph-like`

#### 证据等级

| 等级 | 含义 |
|------|------|
| A | 官方仓库 / 官方文档 / 原始论文相互印证，关键机制可核验 |
| B | 官方仓库或官方文档较清晰，但效果主要依赖项目自报 |
| C | 官方入口存在，但实现细节或评测链条不够稳 |
| X | 本轮未拿到足够稳定的一手技术材料，只作弱引用 |

### 0.4 如何正确理解“SOTA”

“SOTA”在 agent memory 里不能被理解成一个总冠军数字。更合理的读法是：

| 信号类型 | 能说明什么 | 不能说明什么 |
|----------|------------|-------------|
| 同行评审论文 / 官方 benchmark | 方法在某个测试集上有效 | 一定最适合生产，也不一定可迁移到别的场景 |
| 官方 research / benchmark 页面 | 当前公开前沿和产品方向 | 独立复核、可重复性、跨系统公平性 |
| README / Docs 工程数据 | 架构形态、接入方式、成本和产品成熟度 | 通用记忆质量冠军 |

因此，后文不会写“唯一 SOTA”，而会写：

- **哪类问题已经被较好解决**
- **哪类切片上谁更强**
- **哪些还是 vendor self-report**
- **还有哪些空间**

### 0.5 七个高层结论

1. **Filesystem-like memory 的价值，不是“反向量库”，而是把记忆重新变成可读、可改、可迁移、可治理的工程对象。**
2. **Vector/graph-like memory 的价值，不是“多存 embedding”，而是构建共享语义平面、关系平面和服务平面。**
3. **当前已经被证明能解决的问题，主要是跨会话 recall、按需压缩上下文成本、以及一定程度的多 agent 状态共享。**
4. **当前还没有成为行业默认能力的问题，主要是程序性记忆治理、记忆回滚/审计、以及安全遗忘与知识更新。**
5. **公开 benchmark 前沿在 2026 年变得更碎片化，很多高分来自厂商官方页面；这恰恰说明不能把 agent memory 写成单一排行榜。**
6. **Filesystem-like 与 vector/graph-like 已经开始相互收敛：前者引入 shadow index 与 hybrid retrieval，后者补 provenance、temporal modeling、trace 与治理。**
7. **`CortexMem` 最合理的方向不是二选一，而是“文件真相层 + 语义/图检索层 + 程序性记忆层 + 治理/遗忘层”的混合架构。**

---

## 1. 解决了哪些关键问题，当前解决到什么程度，业界 SOTA 是什么，还有哪些空间

### 1.1 总表

| 关键问题 | 当前解决程度 | 当前公开强信号 / SOTA 切片（截至 2026-04-16） | 主要代表 | 仍有空间 |
|----------|-------------|-----------------------------------------------|---------|---------|
| **跨会话失忆，记忆不可读** | 事实 recall 已较成熟；“可读可改”主要由 filesystem-like 解 | 长对话 recall 的公开高分前沿已进入 vendor self-report 阶段，例如 `Hindsight` 官方页给出 `94.6% LongMemEvalS / 92.0% LoCoMo10`，`Mem0` 官方研究页给出 `92.0% LongMemEval`，`Honcho` 官方 blog 给出 `90.4% LongMem S / 89.9% LoCoMo`；但“人能读懂、纠正、迁移”的强信号仍主要来自 `memsearch`、`Acontext`、`OpenViking` | Hindsight, Mem0, Honcho, memsearch, Acontext, OpenViking | 时间边界、来源溯源、冲突处理、人类纠错与跨系统迁移一致性 |
| **有限上下文窗口中的注意力质量与 token 成本** | 工程收益已经很明确 | `Mem0` 官方研究页报告相对 full-context 的 `91%` 延迟下降与 `90%` token 节省；`OpenViking` README 报告相对 OpenClaw 的 `83%-91%` 输入 token 降低；`BEAM` 等新 benchmark 开始逼迫系统在 1M-10M 级历史上工作 | Mem0, OpenViking, Hindsight, Honcho, Graphiti | 缺统一的成本-质量-延迟联合基准，很多结果仍不便横向公平比较 |
| **多 agent 协作时没有共享脑** | 架构需求明确，工程样本已出现，但没有统一 benchmark | 这一维没有公认分数冠军；更强的是架构信号：`mem9` 的中心化 memory pool、`eion` 的 shared knowledge graph、`ContextLoom` 的 Redis-first shared brain、`UltraContext` 的 context plane、`Honcho` 的 entity-aware shared state | mem9, eion, ContextLoom, UltraContext, Honcho | 权限边界、并发冲突、命名空间、事务语义、共享一致性仍未标准化 |
| **高价值长期资产：技能 / 策略 / SOP** | 已被证明可行，但远未成为行业默认 | `Voyager` 用 executable skill library 证明程序性记忆有效；`Acontext` 把 “skill is memory” 做成产品接口；但主流 memory 系统仍偏向“记事实”而不是“记做法” | Voyager, Acontext | 技能验证、失效检测、版本升级、与语义记忆联动仍弱 |
| **记忆治理 / 回滚 / 审计** | 仍是行业短板，只有少数系统做成一等能力 | 这条线没有 benchmark 型 SOTA，**架构 SOTA** 更接近 `Memoria`：snapshot / branch / merge / rollback / quarantine / audit trail | Memoria | 需要从“少数系统特性”变成“行业默认能力” |
| **记忆遗忘 / 过期 / 知识更新** | 最弱的一环 | `Graphiti/Zep` 在 temporal validity 和 fact invalidation 上最有代表性；`LongMemEval` 已把 knowledge update / abstention 纳入 benchmark；但“安全遗忘、置信度衰减、策略淘汰”仍基本缺位 | Graphiti/Zep, TiMem, LongMemEval | 缺安全遗忘策略、衰减函数、过期治理和低置信隔离机制 |

### 1.2 已经被基本证明的三件事

#### 1.2.1 跨会话失忆可以被解决，但“可信记忆”还没完成

在 coding agent、research agent、personal assistant 场景里，用户真正痛的往往不是“模型不会检索”，而是：

- 上一轮有效讨论没有稳定落盘
- 落盘后人又看不懂、改不动
- 换模型、换 agent、换终端后上下文断掉

这一点已经被两类路线分别证明：

- `Filesystem-like` 证明了**可读、可改、可迁移**是刚需，而不是附属功能
- `Vector/graph-like` 证明了**事实 recall** 和 **跨会话复用** 可以工程化做出来

但“已能 recall”不等于“已可信”。当前系统仍普遍缺三样东西：

1. 这条记忆是**谁说的、何时说的、是否推断得出**
2. 这条记忆**现在是否仍然有效**
3. 新旧记忆冲突时，**应如何更新、保留还是隔离**

换句话说，今天的主流水平更像“高可用 recall 层”，还不是“高可信认知层”。

#### 1.2.2 “长上下文不等于好记忆”已经成为行业共识

旧式做法往往是：

- 要么把所有历史直接塞进 context
- 要么做一次扁平 top-k chunk retrieval

这两者都不稳：

- 全塞进 context 会导致 token 成本高、注意力分散、时延上涨
- 扁平 top-k 容易召回噪声块，缺层次感，也缺时间结构

当前更成熟的方案已经走向三种能力的组合：

1. **主动 consolidation**
   不是存原话堆历史，而是抽取高浓度事实、摘要、实体状态或 skill
2. **按需披露**
   先给目录、摘要、短 context，再逐层下钻
3. **混合检索**
   semantic + keyword + metadata + graph traversal，而不是单纯 dense vector

这也是为什么：

- `Mem0` 强调 extract / update / selective retrieval
- `OpenViking` 强调 `L0/L1/L2` tiered loading
- `Hindsight` 和 `Honcho` 都开始强调长程 benchmark 尤其是 `BEAM 10M`

今天真正要优化的，不再是“能否记住所有文本”，而是：

> 在有限上下文里，把最值得被关注的东西，以最低 token 成本、最高注意力质量，稳定地送到模型面前。

#### 1.2.3 多 agent 确实需要共享脑，但还没有标准答案

单 agent 还能靠对话摘要、本地文件或者 session memory 勉强维持；多 agent 一旦并行，就会暴露出一组新的系统问题：

- agent A 的状态，agent B 看不到
- 多个 agent 同时写入，冲突无人处理
- “谁对什么有读写权限”边界不清
- 同一实体被多 agent 以不同方式理解，无法汇合

这一点已经被多个系统从不同角度证明：

- `ContextLoom`：shared brain / decoupled memory from compute
- `eion`：shared knowledge graph + guest access
- `mem9`：stateless plugins + central memory pool
- `UltraContext`：same context, everywhere
- `Honcho`：围绕 entities / sessions / representations 组织共享状态

但这条路线目前仍然更像“工程必要性被证明”，而不是“行业已有标准栈”。最薄弱的部分不是检索本身，而是：

- 权限和命名空间
- 并发和事务
- 冲突解决
- provenance 和审计

### 1.3 仍未被行业默认解决的三件事

#### 1.3.1 记忆资产化：从“记事实”到“记技能 / 策略 / SOP”

大量系统今天仍偏向**陈述性记忆**：

- 用户喜欢什么
- 过去说过什么
- 某个事实是否出现过

但对 agent 真正更值钱的长期资产，往往是**程序性记忆**：

- 哪套 debug 步骤最稳
- 哪个工具组合在这个环境里能跑通
- 哪类失败模式出现后应该怎么修
- 哪个 workflow 是该团队的默认 SOP

这一点已经有两个强样本：

- `Voyager`：把能力沉淀为 executable skill library
- `Acontext`：把 skill memory layer 做成产品接口，直接以 `SKILL.md` 等文件形式治理

它们说明方向成立，但还没成为默认范式。主要短板是：

- skill 是否真的有效，缺自动验证
- 环境变了后，skill 是否过时，缺失效检测
- skill 版本升级和兼容性治理不成熟

#### 1.3.2 一旦记错、被污染或被投毒，怎么治理

长期记忆一旦进入真实生产，问题就从“能不能写进去”变成：

- 写错了怎么办
- 记忆互相矛盾怎么办
- 哪次 mutation 引入了坏行为
- 低置信信息是否应该被隔离
- 不同实验分支如何并存

这条线上最清晰的代表是 `Memoria`。它的重要性不在于“又用了向量库”，而在于它把下面这些能力做成了一等对象：

- snapshot
- branch
- merge
- rollback
- contradiction detection
- low-confidence quarantine
- audit trail

这说明治理不是附属功能，而是 memory system 的必经阶段。今天很多系统“能记住”，但还不“可治理”。

#### 1.3.3 记忆如何安全遗忘、过期和更新，仍然没有好答案

绝大多数系统今天都会：

- 写入
- 检索
- 或多或少做 consolidation

但不太会：

- 安全地忘掉不再可信的信息
- 给低置信信息降权
- 在新旧事实冲突时做可靠的时间治理
- 把过期知识从检索主路径里策略化移除

当前最有方向性的工作是：

- `Graphiti/Zep`：用 temporal graph、fact invalidation、valid/invalid 时间戳处理事实变化
- `LongMemEval`：把 knowledge update、abstention 纳入评测
- `TiMem`：从时间层次上看待 consolidation 和 recall

但这些离“生产默认遗忘机制”还有明显距离。安全遗忘、置信度衰减、策略淘汰、归档与隔离，会是下一阶段真正的分水岭。

---

## 2. 核心实现机制和原理

### 2.1 机制总表

| 机制 | 范式 | 核心原理 | 代表系统 | 价值 | 主要边界 |
|------|------|----------|---------|------|---------|
| **文件真相层** | Filesystem-like | 记忆对象以 Markdown / skill / 版本对象落盘，文件为 source of truth | memsearch, Acontext, Memoria | 人类可读、可审阅、可迁移 | 服务化共享不如 northbound plane 自然 |
| **Shadow Index** | Filesystem-like | 向量 / FTS 从文件真相层重建，负责加速而不负责真相 | memsearch | 快速检索且不牺牲可读性 | 需要同步与 rebuild 策略 |
| **分层加载（L0-L2）** | Filesystem-like | 先给目录/摘要，再按需递归披露细节 | OpenViking, memsearch, Acontext | 降 token、提注意力质量、提可解释性 | 要求 agent 有更强 tool-use 能力 |
| **Append-only + Layered Summary** | Filesystem-like | 原始 episode 不丢失，上层摘要可压缩可展开 | lossless-claw, OpenViking | 可追溯、可压缩、可恢复 | 主要解决上下文管理，不等于完整 memory 栈 |
| **Consolidation / Reconciliation** | Vector/Graph-like | 从对话里提取 salient info，并做 ADD / UPDATE / DELETE / NOOP | mem0, mem9 | 避免只堆历史，让记忆自更新 | 成本高，受抽取质量影响 |
| **Hybrid Retrieval** | Vector/Graph-like | dense + keyword + metadata + graph traversal 组合检索 | mem0, mem9, Graphiti, Hindsight | 平衡语义召回与精确关系 | 链路更复杂，调参更重 |
| **Representation Modeling** | Vector/Graph-like | 围绕实体形成持续状态表示，而不只是 chunk recall | Honcho | 更适合长期个体/实体理解 | 黑箱程度更高 |
| **Temporal Graph** | Vector/Graph-like | 关系携带时间边界与有效窗，支持 point-in-time 查询 | Graphiti/Zep | 更贴近真实业务状态演化 | 图维护和查询复杂 |
| **Shared Memory Plane** | Vector/Graph-like | 以中心化服务 / pool / namespace 供多 agent 共享 | mem9, ContextLoom, eion, UltraContext | 多 agent 协作和跨端同步更强 | ACL、并发、事务仍难 |
| **Branch / Rollback / Quarantine** | 治理层 | 把记忆 mutation 纳入版本和安全治理 | Memoria | 可审计、可修复、可实验 | 基础设施和流程成本更高 |

### 2.2 Filesystem-like 范式：记忆首先是文件、目录和技能对象

#### 2.2.1 Shadow Index：文件为真相，向量为加速

Filesystem-like 路线最值得保留的原则之一是：

> 文件作为真相，向量作为加速。

这意味着：

- 记忆对象应当是人能打开的 `Markdown / YAML / skill file`
- 向量库或全文索引只是可重建的检索缓存
- 检索命中后，真正被引用和修正的仍是文件本身

`memsearch` 是这一原则最清晰的工程样本：

- `Markdown` 是 source of truth
- `Milvus` 是 shadow index
- 检索链路是 `search -> expand -> transcript`

这一机制的重要意义在于：

1. 记忆不会被底层向量库绑死
2. 人工修正的对象是显式文件，而不是黑箱 embedding
3. 检索层坏掉时，真相层仍在

#### 2.2.2 分层加载（L0-L2）：按需递归披露，而不是一次塞满

Filesystem-like 路线在上下文管理上的核心发明，不是“存成文件”，而是**层级披露**：

- `L0`：最小核心摘要，默认带入
- `L1`：结构化摘要、目录、索引，按需展开
- `L2`：完整原文、完整 skill、完整资源，只在确实需要时加载

这本质上是在做一种“记忆分页”：

- 先把问题缩到足够小
- 再决定是否继续读更深的层级

`OpenViking` 的 `L0/L1/L2`、`memsearch` 的三级 recall、`Acontext` 的 `list_skills -> get_skill -> get_skill_file`，都在说明同一件事：

> 稳定的 retrieval 往往不是一步命中，而是先缩小空间，再向下钻取。

#### 2.2.3 程序性记忆：skill file 比抽象摘要更接近高价值资产

Filesystem-like 系统天然更容易把记忆沉淀成：

- `skill`
- `playbook`
- `workflow`
- `SOP`
- `可执行代码`

这比“把所有经验都抽成一段自然语言摘要”更稳，原因有三点：

1. 可验证
2. 可组合
3. 可版本化

`Acontext` 和 `Voyager` 分别给出了产业化和学术化的强样本。它们共同说明：

> 对复杂 agent 而言，长期最值钱的记忆，常常不是“知道过什么”，而是“会怎么做”。

#### 2.2.4 Append-only 原始记录 + 分层摘要 + 可恢复展开

`lossless-claw` 这类系统之所以值得保留，不是因为它代表了通用 user memory 的最强路线，而是因为它揭示了一个很合理的底层结构：

- 原始消息要保留
- 摘要可以分层压缩
- 命中摘要后，仍能恢复原始上下文

这条思路非常适合：

- coding session
- 长研究过程
- 多轮工具调用轨迹

因为这些场景里，很多关键细节是不能在早期就丢弃的。

### 2.3 Vector/Graph-like 范式：记忆首先是共享语义 / 关系平面

#### 2.3.1 Consolidation：从原始对话抽取高浓度记忆

Vector/graph-like 路线的主流做法，不是保存全部原话，而是保存**抽取后的记忆单位**。

最典型的是两阶段流程：

1. **Extraction**
   从最近消息、滚动摘要、上下文中提取候选事实 / 实体 / 关系
2. **Update / Reconciliation**
   将新候选与已有记忆比较，决定：
   - `ADD`
   - `UPDATE`
   - `DELETE`
   - `NOOP`

`mem0`、`mem9` 都属于这一类。这个机制的价值在于：

- 避免重复存原文
- 让记忆能演化
- 把“更新”变成一等能力，而不是只会追加

但代价也很清楚：

- 要跑 LLM 判断
- 容易受抽取质量影响
- 错误提炼会持续污染后续决策

#### 2.3.2 Hybrid Retrieval：纯向量检索已经不够

当前较成熟的 memory system，几乎都在走向 hybrid retrieval：

- dense vector
- keyword / BM25
- metadata / entity filters
- graph traversal
- reranking

原因很直接：

- 纯语义检索对精确关系和否定信息不稳
- 纯关键词对近义表达和抽象偏好不稳
- 没有结构化关系时，多会话和跨实体推理很弱

因此，今天更合理的判断是：

> 真正可用的 SOTA 不是“最强向量库”，而是“多信号检索 + 更好的路由与重排”。

#### 2.3.3 Representation Modeling 与 Temporal Graph：从“找句子”走向“建状态”

这是 vector/graph-like 路线与传统 RAG 最大的分野。

`Honcho` 的重点不是更多 chunks，而是：

- entities
- sessions
- representations
- dreaming / background reasoning

`Graphiti/Zep` 的重点则是：

- temporal knowledge graph
- facts with `valid_at / invalid_at`
- point-in-time reasoning
- source provenance

这两类设计共同说明：长期记忆的核心问题，不只是“找到一句旧话”，而是：

- 某个实体当前处于什么状态
- 这个状态是如何演化来的
- 旧事实是失效了，还是仍应保留为历史事实

#### 2.3.4 Shared Memory Plane：多 agent 需要中央化语义/状态平面

Vector/graph-like 路线在多 agent 场景更强，核心原因不是“检索更快”，而是它更容易变成一个：

- northbound API
- shared pool
- multi-tenant memory service
- context / state plane

典型代表：

- `mem9`：central server + stateless plugin
- `eion`：shared memory storage + knowledge graph + guest access
- `ContextLoom`：Redis-first shared brain
- `UltraContext`：history / fork / clone / same context everywhere

这条路线适合做：

- 跨终端同步
- 多 agent 协作
- 企业多应用共享同一认知层

但同时必须补上：

- namespace
- ACL
- transaction
- conflict resolution

否则共享脑只会把单 agent 的错误放大成系统性错误。

### 2.4 行业真实趋势：两类路线正在收敛成混合架构

这轮研究最重要的判断之一是：

- `Filesystem-like` 已经不再排斥向量检索，而是把它降成 shadow index
- `Vector/graph-like` 也不再只强调 recall，而开始补 temporal modeling、trace、governance 和 provenance

因此，未来真正稳定的 memory stack 更可能是：

1. **文件真相层**
2. **语义 / 图索引层**
3. **共享 memory plane**
4. **程序性记忆层**
5. **治理 / 审计 / 遗忘层**

---

## 3. 面向的关键场景

### 3.1 场景总表

| 场景 | 更适合的主导范式 | 原因 | 代表系统 |
|------|------------------|------|---------|
| **高复杂度编程（Coding Agents）** | Filesystem-like 优先，必要时加 shadow index | 代码库本身就是文件系统；需要记录架构决策、版本依赖、调试经验；必须支持人工审核和记忆修正 | memsearch, OpenViking, Acontext, Memoria |
| **长程研究（Research Agents）** | Filesystem-like 优先 | 输出物本身是结构化文档；需要多轮整理、改写、引用和人工干预 | OpenViking, memsearch, lossless-claw |
| **全天候个性化助手（Proactive Assistants）** | Vector/graph-like 优先 | 需要跨设备同步、后台更新偏好、围绕人和关系持续建模 | mem0, Honcho, Graphiti/Zep, memU |
| **多 agent 协同系统（Planner / Executor / Reviewer）** | Vector/graph-like 优先 | 多个 agent 需要共享状态池、共享实体关系和中心化权限边界，不能都盯着同一个大文件读写 | mem9, eion, ContextLoom, UltraContext |

### 3.2 Filesystem-like 为什么更适合 coding / research

这类任务有两个共同点：

1. **任务对象本来就天然是文件和文档**
2. **人类工程师必须能看懂 agent 在记什么**

所以在这些场景里，最关键的不是“极致 recall 分数”，而是：

- 记忆能不能被 review
- 技术决策能不能被纠正
- SOP 能不能沉淀成 skill
- 历史过程能不能被追溯

这也是为什么 `memsearch`、`Acontext`、`OpenViking` 这类系统对 coding / research 特别贴合。

### 3.3 Vector/Graph-like 为什么更适合 proactive / multi-agent

这类场景的共同特征是：

- 多端同步
- 高并发
- 长期在线
- 多实体关系
- 中央化服务治理

这时候单纯靠文件表面不够，因为系统需要：

- 更像服务，而不是像目录
- 更像共享状态池，而不是单机工作区
- 更强的实体建模、时间建模和权限边界

所以 `mem0`、`Honcho`、`Graphiti/Zep`、`mem9`、`eion`、`ContextLoom` 更适合成为这一层的主体。

---

## 4. 对 CortexMem 的直接启示

### 4.1 总体架构判断：文件为表，语义为里，治理为底

这轮研究给 `CortexMem` 最直接的结论不是“该选 filesystem-like 还是 vector-like”，而是：

> `CortexMem` 应采用“文件为表，语义为里，治理为底，程序性记忆为增长引擎”的混合架构。

可以把它理解为：

```
L4 治理 / 审计 / 回滚 / 遗忘
L3 程序性记忆 / Skill / SOP
L2 语义索引 / 图关系 / Shared Memory Plane
L1 文件真相层（Markdown / Resource / Skill Files）
L0 Append-only 原始事件与轨迹
```

### 4.2 六个优先建设方向

#### 4.2.1 程序性记忆治理：把成功做法沉淀成 skill，而不是只记事实

目前大多数系统仍然偏“记事”，但对 agent 最有复利价值的常常是：

- 调试步骤
- 工具组合
- 环境 workaround
- 失败模式与修复 SOP

`CortexMem` 应把这些对象单独建模成 `skill / playbook / SOP`，并支持：

- 自动 distill
- 版本化
- 失效检测
- 人工 review

#### 4.2.2 分层递归检索 + 向量增强：先缩小空间，再向下钻

`CortexMem` 不应该默认把完整记忆全文塞给模型，而应支持类似 URI 的层次化加载：

- 先给目录和摘要
- 再给命中文件路径和原因
- 仅在需要时读取正文

而 shadow index / hybrid retrieval 的职责是：

- 缩小检索空间
- 提供候选
- 支持更快命中

不是直接取代文件真相层。

#### 4.2.3 检索轨迹可视化：让记忆成为可观测系统

记忆系统不应只返回结果，还应给出 trace：

- 为什么命中了这条记忆
- 经过了哪一层检索
- 用到了哪些过去的文件、实体或关系
- 哪条证据最终影响了回答

这对开发者和用户都重要，因为：

- 它能解释错误是如何产生的
- 它是后续调参与治理的基础

#### 4.2.4 记忆治理 / 回滚 / 审计：像代码一样管理记忆

`CortexMem` 若想进入生产，必须内建：

- snapshot
- branch
- rollback
- diff
- provenance
- low-confidence quarantine

否则记忆一旦写错，只能靠下一次写入“碰运气地覆盖”，这在工程上不成立。

#### 4.2.5 安全遗忘与置信度衰减：不只是会写，还要会忘

应把遗忘设计成一等策略，而不是垃圾回收的副产物。至少应考虑：

- 时间衰减
- 访问频次衰减
- 置信度衰减
- 过期归档
- 低置信隔离
- 新旧事实冲突时的时间治理

真正成熟的 memory system，不是无限堆积，而是能**安全地压缩、淘汰、归档和忘记**。

#### 4.2.6 面向多 agent 的共享脑：共享记忆必须带权限与命名空间

如果 `CortexMem` 未来要服务 planner / executor / reviewer 这类多 agent 编排，就不能只停留在单机文件记忆。它还需要：

- shared memory plane
- workspace / tenant / agent scopes
- 读写权限
- 冲突和事务语义

否则所谓“共享脑”只会变成“共享污染”。

---

## 5. 最终判断

1. **Filesystem-like 与 vector/graph-like 解决的是不同层级的问题，不是简单替代关系。**
2. **Filesystem-like 更适合把记忆做成可读、可控、可迁移、可治理的工程对象，尤其适合 coding 和 research。**
3. **Vector/graph-like 更适合把记忆做成共享语义 / 关系 / 服务平面，尤其适合 proactive assistant 和 multi-agent workflow。**
4. **截至 2026-04-16，公开 benchmark 前沿已经高度碎片化；因此“业界 SOTA”应该按问题切片理解，而不能写成单一冠军榜。**
5. **对 `CortexMem` 来说，最有价值的不是押注单一路线，而是做“文件真相层 + 语义/图索引层 + 程序性记忆层 + 治理/遗忘层”的混合栈。**

---

## 附录 A：Benchmark / SOTA 的正确读法（截至 2026-04-16）

| 切片 | 更该看什么 | 当前公开强信号 | 如何使用 |
|------|-----------|---------------|---------|
| **标准长对话 recall** | `LongMemEval / LoCoMo` | `Hindsight` 官方 benchmark 页给出 `94.6% LongMemEvalS / 92.0% LoCoMo10`；`Mem0` 官方 research-2 页给出 `92.0% LongMemEval`；`Honcho` 官方 blog 给出 `90.4% LongMem S / 89.9% LoCoMo` | 可判断公开 recall 前沿，但多为厂商自报，不宜直接当统一总榜 |
| **超长历史真正需要 memory 架构的切片** | `BEAM 1M / 10M` | `Hindsight` 官方 blog 报告 `64.1% BEAM 10M`；`Mem0` 官方页展示 `45.0% BEAM 10M`；`Honcho` 官方 blog 报告 `0.406 BEAM 10M` | 更接近“context stuffing 已经失效”的 frontier，但仍需注意评测配置差异 |
| **时间变化与知识更新** | `LongMemEval` 的 knowledge update、temporal reasoning；`Graphiti/Zep` 的 temporal graph | `Graphiti/Zep` 明确支持 validity / invalidation / historical context | 这里更应看架构是否真建模时间，而不是只看总分 |
| **多 agent 共享脑** | 架构能力 | `mem9`、`eion`、`ContextLoom`、`UltraContext` 提供强架构信号，但无统一 benchmark | 这是“缺 benchmark 但工程需求真实”的典型领域 |
| **可读性 / 可治理性** | 文件真相层、trace、rollback、audit | `memsearch`、`Acontext`、`OpenViking`、`Memoria` | 这条线目前更该看机制和可操作性，而不是分数 |

### 附录 A 的核心结论

- `LoCoMo / LongMemEval` 仍有价值，但在更大 context window 时代，已经不够单独代表“真实 memory frontier”。
- `BEAM 10M` 更能测试“无法靠塞上下文取巧”的能力，因此更接近真正的长期 memory frontier。
- 但即便如此，agent memory 也不能只看 benchmark；生产上同样重要的是：
  - 可读
  - 可调试
  - 可治理
  - 可共享
  - 可遗忘

## 附录 B：本轮补充核验的一手来源

- `Mem0` 官方 research page：<https://mem0.ai/research>
- `Mem0` 官方 research-2 page：<https://mem0.ai/research-2>
- `Honcho` 官方 benchmark blog（`2025-12-19`）：<https://blog.plasticlabs.ai/research/Benchmarking-Honcho>
- `Hindsight` 官方 benchmark 页：<https://benchmarks.hindsight.vectorize.io/>
- `Hindsight` 官方 BEAM 文章（`2026-04-02`）：<https://hindsight.vectorize.io/blog/2026/04/02/beam-sota>
- `Graphiti/Zep` 官方文档：<https://help.getzep.com/graphiti/graphiti/overview>

如需进一步追溯各系统的仓库、论文和细节材料，可继续参考同目录下的 `sources.md` 与 `evidence-matrix.md`。
