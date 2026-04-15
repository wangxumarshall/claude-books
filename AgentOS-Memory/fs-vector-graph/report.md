# Filesystem-like 与 Vector/Graph-like Agent Memory研究

> 目录定位：`AgentOS-Memory/fs-vector-graph/`
>
> 更新时间：2026-04-15
>
> 研究主题：Agent 外部记忆增强中的两条主路线
> 1. `filesystem-like agent memory`
> 2. `vector/graph-like agent memory`
>
> 研究目标：回答
> - 这些 memory 方案解决了哪些关键问题，当前解决到什么程度，业界 SOTA 是什么，还有哪些空间
> - 核心实现机制和原理是什么
> - 分别面向哪些关键场景
> - 对 CortexMem 的能力建设有什么直接启发

---

## 0. 研究范围、方法与结论先行

### 0.1 研究范围

报告聚焦 **external memory augmentation**，即模型外的持久化记忆系统，不把 Transformer 原生记忆、参数编辑、KV-cache 机制本身当作主线。

纳入主研究对象的标准是同时具备三点：

1. **跨会话持久化**
2. **可检索 / 可复用**
3. **可更新 / 可巩固**

因此：

- `Voyager` 虽然不是通用聊天 memory 产品，但其可执行技能库满足"长期可复用程序性记忆"，纳入主研究。
- `MemGPT/Letta` 更接近虚拟上下文管理框架，作为重要学术参照。
- `UltraContext` 属于重要邻接基础设施：它解决跨 agent 上下文同步和版本化，但还不是典型的长期记忆抽取/巩固系统。
- `XiaoClaw` 仍不作为独立 memory architecture 处理，它更像 OpenClaw 的安装封装与生态包装层。

### 0.2 为什么单独研究 filesystem-like 与 vector/graph-like

"Agent Memory"经常被笼统地说成"长期记忆"，但实际至少有两套不同的工程目标：

- **Filesystem-like memory**
  重点是把记忆重新变成可读、可调试、可迁移、可治理的工程对象。
- **Vector/graph-like memory**
  重点是把记忆做成共享语义平面、关系平面和服务平面，支撑多 agent、跨产品、跨终端协同。

这个切分更接近真实工程问题：

> 生产里的 agent memory，到底更像"可审阅的知识工作区"，还是更像"可编排的共享语义基础设施"？

答案不是二选一，但两类系统的第一性设计目标明显不同。

### 0.3 主导接口判定规则

同一系统可能同时有文件层、向量层和图层，本报告按**主导接口**归类：

- 主导接口是文件树、Markdown、skill file、目录导航、版本对象：归 `filesystem-like`
- 主导接口是 API、SDK、共享状态、向量检索、图检索、managed service：归 `vector/graph-like`

例子：

- `memsearch` 内部有 Milvus 向量索引，但 Markdown 是 source of truth，仍归 filesystem-like。
- `mem9` 服务 coding agents，但主导接口是中心化 memory server、共享 memory pool、混合检索和可视控制，归 vector/graph-like。
- `lossless-claw` 以 SQLite + DAG 摘要和 recall tools 管理 OpenClaw 上下文，主导接口仍更接近 filesystem/context-engine，因此归 filesystem-like 的"上下文压缩子类型"。

### 0.4 证据等级

| 等级 | 含义 |
|------|------|
| A | 官方仓库 / 官方文档 / 原始论文相互印证，关键机制可核验 |
| B | 以官方仓库或官方文档为主，机制较清晰，但效果主要依赖项目自报 |
| C | 官方入口存在，但口径偏产品化、实现细节或评测链条不够稳 |
| X | 本轮未拿到足够稳定的一手技术链条，只能弱引用或不纳入主线 |

### 0.5 六个高层结论

1. **Filesystem-like memory 的价值不是"反向量库"，而是把记忆重新拉回可读、可控、可迁移的工程对象。**
2. **Vector/graph-like memory 的价值不是"多存 embedding"，而是为多 agent、跨会话、跨系统协作提供共享语义与关系平面。**
3. **两类路线解决的是不同层次的问题：前者先解决可观测性、程序性沉淀和治理；后者先解决共享、规模化、关系化和异步基础设施。**
4. **行业正在走向混合架构：filesystem-like 正引入 shadow index / hybrid retrieval，vector/graph-like 正补 provenance / versioning / observability。**
5. **公开 benchmark 很重要，但不能被滥用。LoCoMo、LongMem、LongMemEval、DMR、BEAM 测的是不同能力，不能做单一总冠军表。**
6. **CortexMem 最合理的方向不是押单一路线，而是"文件表面 + 语义索引 + 图关系 + 程序性记忆 + 治理层"的混合架构。**

---

## 1. 解决了哪些关键问题，当前解决到什么程度

### 1.1 问题总览

| 关键问题 | 主要路线 | 当前解决程度 | 2026-04 公开强信号 / SOTA | 仍有空间 |
|----------|---------|-------------|---------------------------|---------|
| **跨会话失忆，记忆不可读** | 两类都有 | 已较成熟，但对时间演化与冲突仍脆弱 | Honcho 90.4% LongMem S、89.9% LoCoMo（官方 blog 自报）；mem0 在官方研究页持续强化 LongMemEval/LoCoMo 结果；TiMem 75.30% LoCoMo / 76.88% LongMemEval-S（论文） | 需要更强时间结构、知识更新和可解释性 |
| **有限上下文中的注意力质量与 token 成本** | 两类都有 | 已有明显工程收益 | mem0 论文/研究页持续强调 latency 与 token 节省（91% faster、90% fewer tokens vs full-context）；OpenViking 输入 token 降低 83%-91%；memU 自报约 1/10 comparable usage | 仍缺真实生产成本基准和跨系统可比性 |
| **多 agent 协作时没有共享脑** | Vector/graph-like 更强 | 真实需求明确，但无统一 benchmark | ContextLoom、eion、mem9、UltraContext 都给出可运行 shared context/memory plane | 权限模型、冲突解决、共享一致性仍未标准化 |
| **高价值长期资产（技能/策略）沉淀** | Filesystem-like 更强 | 已证明可行，但仍未成为行业默认 | Voyager 的 executable skill library 是学术代表；Acontext 是产业化代表 | 技能验证、失效检测、版本升级仍弱 |
| **记忆写错/被污染/过时后的治理** | Filesystem-like 当前更强 | 仍是行业短板，但方向清晰 | Memoria 在 snapshot / branch / rollback / quarantine / provenance 上最完整 | 需要成为行业默认能力，而不是少数系统特性 |
| **记忆遗忘/过期/知识更新** | Vector/graph-like 略强 | 远未解决 | LongMemEval 已把 knowledge update / abstention 纳入 benchmark；Graphiti、TiMem、Honcho 有方向性优势 | 缺安全遗忘、置信度衰减和策略化淘汰机制 |

### 1.2 已解决/解决部分的问题

#### 问题一：跨会话失忆，记忆不可读

在 coding agent、research agent、personal assistant 场景里，真正困扰用户的不是模型"不会检索"，而是：

- 上一轮有效讨论没有稳定落盘
- 即使落盘，人也无法读懂、改正、迁移
- 换一个 agent、换一个终端、换一个模型后上下文断掉

`memsearch`、`OpenViking`、`Acontext` 的兴起，都是在回答这个问题。

**当前状态**：跨会话事实 recall 已经"能用"，但还没"可信"。今天大多数成熟系统已经能在跨会话事实 recall 上给出明显收益，但真正难点不再是"能否找到一句旧话"，而是：

- 这句话现在还对不对
- 它的时间边界是什么
- 这一结论是用户明确说的，还是系统推断的
- 多条记忆冲突时如何处理

因此，当前更像是"高可用的 recall 层"而不是"高可信的长期认知层"。

#### 问题二：有限上下文中的注意力质量与 token 成本

长上下文并不等于好记忆。MemGPT 把问题定义为"有限上下文窗口下的虚拟内存管理"；memU、OpenViking、mem0、Honcho 都在强调：

- 需要比"每轮都全塞进去"更便宜
- 需要比"扁平 top-k chunk"更稳定
- 需要主动做 consolidation，而不是只堆历史

**当前状态**：业界逐渐意识到"塞满 1M Token Context"在工程上并不经济且不稳定。SOTA 方案正在从单纯的 Dense Vector Retrieval 转向 GraphRAG（如微软的研究）。GraphRAG 通过构建知识图谱并在不同层级（社区）生成摘要，解决了全局认知问题。但这依然属于 Vector/Graph 范式，对人类并不友好。

#### 问题三：多 agent 协作时没有共享脑

单 agent 还能靠本地文件或对话摘要勉强维持；多 agent 一旦串行或并行协作，就会遇到：

- 状态共享断裂
- 权限边界不清
- 关系信息难以表达
- 不同 agent 对同一实体的认知无法汇合

ContextLoom、eion、mem9、UltraContext、Honcho 都是在解决这个问题。

**当前状态**：多agent共享脑是真需求，但industry还没统一范式。ContextLoom、mem9、eion、UltraContext 都表明多agent系统无法只靠每个agent各自的本地 session 状态运行，必须有共享状态或共享上下文层。但这个方向目前仍缺权限与命名空间标准、冲突与并发写策略、标准 benchmark。

### 1.3 待解决的问题

#### 待解决问题一：记忆资产化——从记"事实"到记"技能/策略"

记住"用户喜欢咖啡"当然有价值，但在大量 agent 工作流中，更高价值的是：

- 哪种调试步骤有效
- 哪个工具组合最稳
- 什么 workflow 在这个环境里能跑通
- 什么失败模式出现后该怎么修

Voyager、Acontext 和 filesystem-like 路线的"skill memory"本质上在回答：

> 经验能不能被沉淀成可执行资产，而不只是变成一段文字摘要？

**当前状态**：目前的记忆多为"陈述性记忆"（Declarative Memory，例如"用户是程序员"）。但在复杂系统中，更高价值的是"程序性记忆"（Procedural Memory）。例如一个 Coding Agent 经过反复调试解决了一个环境配置问题，它应该能生成一个 `.md` 或 `.yaml` 格式的 SOP 文件持久化下来，下次遇到类似环境直接加载执行。Acontext 是产业化代表，Voyager 是学术代表，但技能验证、失效检测、版本升级仍弱。

#### 待解决问题二：记忆治理/回滚/审计

长期记忆进入生产后，问题从"能不能记住"升级为：

- 写错了怎么办
- 记忆冲突怎么办
- 不同实验分支怎么办
- 哪次 mutation 导致坏行为
- 低置信信息如何隔离

Memoria 之所以重要，不在于它又加了一个向量库，而在于它把"Git for memory"做成了一等公民。

**当前状态**：当前的 RAG 极度脆弱，一旦向量库中混入了幻觉或错误结论，Agent 就会反复"中毒"。业界急需引入数据库级别的事务（Transaction）或代码级别的版本控制（Version Control）来管理记忆。治理是下一阶段 memory 的真正分水岭——今天很多系统"能记住"，但并不能可控地试验新记忆策略、在记忆污染时恢复、明确追踪 mutation provenance。从生产视角看，这比再多 3-5 个 benchmark 分数更关键。

#### 待解决问题三：记忆遗忘/过期/知识更新

**当前状态**：大多数系统会写入、会召回，但不太会安全地忘。缺安全遗忘、置信度衰减和策略化淘汰机制。无限制堆砌的记忆最终会拖垮系统。AgentPoison（arXiv:2407.12784）表明记忆投毒攻击 ASR >80%，eTAMP（arXiv:2604.02623）表明环境观察污染可实现跨站投毒 ASR 最高 32.5%。没有 provenance、隔离、回滚、写入审计的 memory system，在生产中并不完整。

---

## 2. 核心实现机制和原理

### 2.1 机制总览

| 机制 | 核心原理 | 代表方案 | 价值 | 代价 / 边界 |
|------|----------|---------|------|------------|
| **文件真相层** | 记忆对象以 Markdown / file / skill 落盘，便于人审阅 | memsearch, Acontext | 可读、可改、可迁移 | 共享与关系表达弱于服务层 |
| **Shadow Index（影子索引）** | 向量/全文索引从真相层重建，文件为 Source of Truth，向量库只作为检索路由和加速的"影子" | memsearch | 检索快且不失真相层 | 需要同步和 rebuild 机制 |
| **分层加载（L0-L2）** | Agent 先用 `ls` 看目录，再用 `cat` 或 `less` 读内容。按需递归披露上下文 | OpenViking, memsearch, Acontext | 降 token，提解释性 | 需要更复杂的 agent tool-use |
| **Consolidation（固化）** | 定期后台运行大模型，将短对话压缩提取为高浓度的语义片段存入库中 | mem0, Honcho, Graphiti | 让记忆自更新 | 成本高，且受 judge/抽取质量影响 |
| **Hybrid Retrieval** | 向量 + BM25 + 图遍历。纯 Vector 在处理"逻辑否定"和"精确关系"时效果极差，SOTA 必然是 Hybrid | mem0, mem9, Graphiti | 平衡精确与语义 | 检索链路更复杂 |
| **LLM Reconciliation** | 新事实与旧记忆比对，做 ADD/UPDATE/DELETE/NOOP | mem0, mem9 | 让记忆自更新 | 成本高，且受 judge/抽取质量影响 |
| **Representation Modeling** | 围绕实体形成持续状态表示 | Honcho | 更适合个体/实体长期理解 | 黑箱程度更高 |
| **Temporal Graph** | 关系带时间、历史与有效窗 | Graphiti | 更贴近真实业务状态 | 图维护和查询复杂 |
| **Multi-type Orchestration** | 核心、语义、程序、资源等记忆协同 | MIRIX | 更接近真实 agent memory | 系统复杂度高 |
| **Append-only + DAG Compaction** | 原始消息不丢，摘要 DAG 支撑恢复和扩展 | lossless-claw | 可压缩又可追溯 | 主要解决上下文管理，不等于全功能 memory |
| **Branch / Rollback / Quarantine** | 把记忆 mutation 纳入版本治理 | Memoria | 可实验、可恢复、可审计 | 需要更重的基础设施和流程 |

### 2.2 Filesystem-like 范式：将记忆映射为文件系统目录与文件

#### 核心机制一：Shadow Index（影子索引）

文件作为真相，向量作为加速。这是本轮研究里最稳定、最值得继承的设计原则之一：

- 真相层应便于人检查
- 检索层应便于机器加速
- 两者不要混成一个黑盒

memsearch 是最清晰的产业化样本：Markdown 是 source of truth，Milvus 是 rebuildable shadow index。影子索引被触发后，不要把完整的文本丢给大模型，而是返回一个包含 URI 的摘要，例如 `[相关度95%: 数据库调优指南 -> file://knowledge/db_tune.md]`。只有当 Agent 判断需要详细信息时，才通过特定的 Tool (`read_file`) 获取内容。

#### 核心机制二：分层加载（L0-L2）

这是极其巧妙的设计。L0 是核心摘要（~100 tokens，始终加载）；L1 是结构化摘要（~2k tokens，按需加载）；L2 是完整原始内容（精确查询时加载）。这本质上是用空间换取了 LLM 注意力的聚焦。

OpenViking 的 L0/L1/L2 tiered context loading、memsearch 的三段 recall（search → expand → transcript）、Acontext 的 `get_skill` / `get_skill_file` 都在说明同一件事：

- 真正稳定的 retrieval 往往不是"一步命中"
- 而是"先缩小空间，再按需向下钻"

### 2.3 Vector-like 范式：将记忆抽象为中央化的语义/关系平面向量库

#### 核心机制一：Consolidation（固化）

从对话中提取 Salient Information，定期后台运行大模型，将短对话压缩提取为高浓度的语义片段存入库中。

mem0 的两阶段处理是最典型的实现：

```
Extraction Phase（记忆提取）
    ↓
接收对话消息 + 检索历史摘要上下文
    ↓
LLM (GPT-4o-mini) 提取原子事实
    ↓
Update Phase（记忆决策）
    ↓
候选记忆 vs 已有记忆 → LLM 决策：
    - ADD: 新信息直接添加
    - UPDATE: 补充/更新现有记忆
    - DELETE: 删除矛盾记忆
    - NOOP: 重复信息不操作
```

mem9 的两段式提取流水线类似：Step 1 事实提取（只提取用户说的，不提取 AI 回复）→ Step 2 记忆调和（新事实 vs 已有记忆，带"年龄"标签，冲突时老记忆优先被判定过时）。

#### 核心机制二：Hybrid Retrieval

稠密向量 + 关键词 + 图遍历混合检索。纯 Vector 在处理"逻辑否定"和"精确关系"时效果极差，因此当前 SOTA 必然是 Hybrid。不仅是 Vector + 关键词，更加入了 Graph 遍历（找到节点后，把相邻的一度/二度关系节点一起召回）。

Graphiti 的三路检索（semantic + keyword + graph traversal）、memsearch 的 BM25 + Dense Vector + RRF Reranking、eion 的 PostgreSQL + pgvector + Neo4j 都是这一思路的体现。

### 2.4 代表系统源码级关键模块

#### OpenViking：虚拟文件系统范式

```
viking://
├── memory/
│   ├── session/     # 会话记忆
│   ├── task/       # 任务记忆
│   └── long_term/  # 长期记忆
├── resources/
│   ├── docs/       # 文档资源
│   ├── code/       # 代码资源
│   └── knowledge/  # 知识库
└── skills/
    ├── tools/      # 工具能力
    └── workflows/  # 工作流
```

| 层级 | 内容 | Token 占比 | 加载时机 |
|------|------|-----------|----------|
| L0 | 核心摘要 ~100 tokens | ~5% | 始终加载 |
| L1 | 结构化摘要 ~2k tokens | ~25% | 按需加载 |
| L2 | 完整原始内容 | 100% | 精确查询时 |

关键模块：目录递归检索 + 语义预滤、可视化 retrieval trajectory、自动压缩 session 内容形成自迭代回路。

#### memsearch：Markdown-first + Shadow Index

```
memory/
├── MEMORY.md              # 手写的长期记忆
├── 2026-02-09.md          # 今天的工作日志
└── .memsearch/            # 向量索引缓存（可重建）
```

三层渐进检索：L1 Search → L2 Expand → L3 Transcript。混合搜索：BM25 + Dense Vector + RRF Reranking。SHA-256 内容去重，文件监听器实时同步 Milvus shadow index，本地 ONNX 嵌入模型 bge-m3 约 558 MB。

#### mem0：LLM 驱动的智能记忆管理系统

双重存储：向量数据库（VectorStoreFactory 支持 15+ 种）+ 图数据库（GraphStoreFactory）。核心存储机制：图内存，将记忆表示为有向标记图 G = (V, E, L)。关键创新：使用 LLM 作为"记忆决策机"，而非简单的向量相似度匹配。

#### mem9：两段式提取流水线

单次最多提取 50 条事实，检索 60 条已有记忆比对。记忆带"年龄"标签，冲突时老记忆优先被判定过时。防幻觉设计：真实 UUID 替换为整数 ID 供给 LLM。5 个核心工具：`memory_store / memory_search / memory_get / memory_update / memory_delete`。

#### Acontext：Skill Memory Layer

自动从 agent run 中提取 learnings，任务完成/失败后异步蒸馏为 skill files。召回不依赖 embedding top-k，而是依赖 `list_skills / get_skill / get_skill_file` 等逐层获取。后台异步过程，常见延迟约 10-30s。

#### lossless-claw：DAG 摘要系统

```
SQLite DB
├── messages/           # 原始消息（永不丢失）
├── leaf_summaries/    # 叶子层摘要
├── d1_summaries/      # 一级摘要
└── d2_summaries/      # 二级摘要
```

Fresh Tail（最近 64 条原始消息）+ Summary DAG + 动态展开（`lcm_expand`）。如果原始消息被过早压碎或覆盖，后续很多问题都无法修复——这是 L0 append-only 的工程实证。

#### Memoria：Git for AI Agent Memory

snapshot / branch / merge / rollback + Copy-on-Write + contradiction detection + low-confidence quarantine + provenance chain + full audit trail。把分支、回滚、隔离、审计从"运维附加项"变成 memory 的原生语义，很像代码系统从"文件备份"走向 Git 的跃迁。

#### Honcho：Entity-Aware State Modeling

workspace / peer / session 抽象。存储消息后，后台推理形成 representations——关于 users / agents / groups / ideas 的持续状态。API 不是简单 chunk recall，而是围绕 richer state 组织：`chat` 直接对实体提问、`search` 查找相似消息、`context` 生成 session-scoped context、`representation` 获取实体状态表示。

#### Graphiti/Zep：时序知识图谱

temporal knowledge graph + 动态构建 evolving graph + 保留 changing relationships 和 historical context。检索可融合时间、全文、语义和图算法。事实有效期（Validity Window）+ Source Provenance。

#### eion：统一知识图谱共享存储

PostgreSQL + pgvector + Neo4j。统一 knowledge graph + register console 管理 agents、permissions、resource snippets。支持 sequential agency、live agency、guest access。384 维 embedding（all-MiniLM-L6-v2），4 个 memory MCP tools + 4 个 knowledge MCP tools。

#### ContextLoom：Redis-First 共享上下文

Redis-first memory backend + decouple memory from compute + 从 PostgreSQL/MySQL/MongoDB 拉冷启动数据 + communication cycle + cycle hash 检测 loop/repetition。

### 2.5 学术论文核心机制

#### TiMem（arXiv:2601.02845）：时间层次化记忆树

5 层时序记忆树：L1 事实层 → L2 会话层 → L3 日模式层 → L4 周趋势层 → L5 人格画像层。Complexity-Aware Recall：简单问题只检索浅层，复杂问题才往深层找，**无需 LLM 决策即可实现分层路由**。理论基础来自互补学习系统理论（CLS）：海马体到新皮层转移的系统巩固机制。

#### LiCoMemory（arXiv:2511.01448）：轻量认知图谱

CogniGraph：lightweight hierarchical graph。图不一定要做成重型知识图谱，也可以是轻量认知索引层。图的主要职责可以是导航和候选缩减，而不是全量推理引擎。很多场景并不需要全量知识图推理，而只需要把"谁、何时、与什么相关"组织清楚。

#### MIRIX（arXiv:2507.07957）：多类型记忆编排

6 类记忆类型：Core、Episodic、Semantic、Procedural、Resource、Knowledge Vault。Active Retrieval：Agent 不被动等待查询，主动关联所有记忆类型，减少 87% 的 API 调用。多 Agent 协调：由 controller 编排不同 memory types 的读写与协调。

#### CoALA（arXiv:2309.02427）：认知架构奠基

语言 agent 应被理解为带有模块化记忆组件、结构化动作空间、广义决策过程的认知架构。定义了 Observe → Think → Act → Learn 循环，工作记忆/长期记忆二分，语义/情景/程序性三分。记忆不是单表存储而是多模块协作；记忆、行动、外部环境访问是统一闭环。

---

## 3. 面向的关键场景

### 3.1 场景总览

| 场景 | 为什么需要 memory | 更优路线 | 合理混合形态 |
|------|------------------|---------|-------------|
| **Coding Agent** | 需要跨会话记住决策、代码约定、调试过程、失败经验 | Filesystem-like 起手 | 文件真相层 + shadow index + skill layer |
| **Proactive Assistant** | 需要长期偏好、关系、待办、提醒和主动行为 | 两类混合 | 文件偏好表面 + entity/temporal memory |
| **Multi-Agent Workflow** | 多 agent 必须共享状态与任务上下文 | Vector/graph-like 起手 | shared memory plane + namespaces + file artifacts |
| **Enterprise Copilot** | 需要把动态业务数据、用户历史和知识库统一进 agent | Vector/graph-like 更强 | graph/temporal layer + governed file truth |
| **Research / Analysis Agent** | 需要可追踪笔记、资源索引、可复查结论 | Filesystem-like 更强 | resource filesystem + retrieval trajectory + provenance |
| **Long-running Autonomous Process** | 需要持续压缩、巩固、更新和回滚 | 两类都需要 | append-only log + consolidation + governance |

### 3.2 Filesystem-like 范式适用场景

#### 场景一：高复杂度编程（Coding Agents）

代码库本身就是文件系统。Agent 维护一个 `.agent_memory` 目录，里面记录 `architecture.md`、`decisions_log.md`。开发者可以直接打开这些文件查看 Agent 的思路甚至帮它纠错。

这个场景下最关键的不是"人格画像"，而是：项目事实、决策历史、调试策略、skill / playbook。因此 filesystem-like 路线先天占优。

memsearch、OpenViking、lossless-claw 是强工程样本。memsearch 支持 Claude Code、OpenClaw、OpenCode、Codex CLI 四个主要 coding-agent 平台；OpenViking 在官方 LoCoMo10 插件评测中给出 completion/token 强信号。

#### 场景二：长程研究（Research Agents）

输出目标本身就是综述报告。Agent 的工作过程就是不断在不同目录下创建草稿、收集 Reference、合并章节的过程。需要将海量信息整理成结构化文档，供人和 Agent 多次迭代。

### 3.3 Vector-like 范式适用场景

#### 场景一：全天候个性化助手（Proactive Assistants）

需要跨手机、电脑多端同步用户画像，自动更新偏好。比如基于手机端侧的 AI，需要不断吸收用户的碎片化信息（喜好、行程）。这些信息不需要人工去阅读一个"用户配置.md"，直接通过向量库在后台潜移默化地影响模型输出。

memU 的定位很明确：memory for 24/7 proactive agents。它把 memory 明确比喻为文件系统（folders → categories, files → memory items, symlinks → cross references, mount points → resources），但主动式 agent 不能只等 query 再检索，它需要更持久的结构化 memory space 和更小的默认上下文。

#### 场景二：多 Agent 协同系统（Multi-Agent Workflow）

多个 Agent（如 Planner, Executor, Reviewer）实时共享同一个状态池，避免抢占同一文件或读取超长文档而卡死，通常采用 Vector-like memory。当 5 个 Agent 在解决一个复杂问题时，它们通过高频地向一个统一的 Vector 数据库读写状态来保持同步，避免了文件系统的并发锁死（File Locking）问题。

只做本地 Markdown 不够，因为多个 agent 之间需要：共享命名空间、并发控制、统一视图、跨终端和跨 runtime 的统一访问。因此需要 northbound memory plane。

---

## 4. 对 CortexMem 的启示

### 4.1 CortexMem"表里"混合架构

采用"文件为表，语义为里"的设计。南向保留人类可读的 Markdown 文件和 Skill 配置（作为 Source of Truth），北向构建影子向量索引作为加速平面。

| 层 | 目标 | 应借鉴的代表 |
|----|------|-------------|
| L0 原始事件层 | append-only 保存原始 observation / tool trace / transcript / artifact refs | lossless-claw, OpenViking |
| L1 文件记忆表面 | 人类可读、可局部编辑、可迁移的记忆对象 | memsearch, Acontext |
| L2 语义索引与图层 | dense + sparse + metadata + entity + temporal retrieval | mem0, Graphiti, Honcho |
| L3 程序性记忆层 | playbook / skill / executable workflow | Acontext, Voyager |
| L4 治理层 | snapshot / branch / rollback / provenance / quarantine | Memoria |

### 4.2 五条关键启示

#### 启示一：程序性记忆（Procedural Memory）治理

目前多偏向语义记忆（记事），应加强对"技能文件"管理。让 Agent 自动总结确定性的"任务执行 SOP"。

在软件工程中，复用性是降低成本的关键。不要让 Agent 每次都从头推理。当 Agent 成功完成一次复杂任务后，强制触发一个 Reviewer Agent，将刚刚成功的执行轨迹（Trajectory）提炼为一个标准的 YAML/Markdown SOP 文件存入文件系统，并打上向量标签。下次执行类似任务，Agent 直接读取 SOP 按照步骤执行。

高价值长期资产应优先以程序性/技能性对象存在，而不是先压成抽象文本再寄希望于检索。

#### 启示二：分层递归检索和向量索引增强

在 Context Window 依然昂贵的今天，应支持类似 URI 的层次化加载逻辑和索引增强。先提供目录和摘要，长路径支持向量索引增强，由 Agent 发起 `read_file` 指令后再加载详情，大幅压低输入 Token 成本。此能力可外挂到传统 FS，或内嵌到传统 FS。

建议四阶段读路径：
1. trust / namespace filter
2. entity / type / time pre-filter
3. dense + sparse + metadata retrieval + graph expansion + rerank
4. minimal-context assembly

#### 启示三：引入"检索轨迹"可视化

记忆系统不应只输出结果，需提供 Trace 能力，向开发者/用户展示 Agent 究竟是基于哪一条"过去的文件"或"关系"做出决策，解决记忆透明度问题。

每次回答必须附带类似 APM（应用性能管理）的 Trace Log。用户（或开发者）可以清晰地看到：Agent 识别了意图 A → 查询了影子向量库 → 命中了文件 B 和节点 C → 提取了段落 D → 生成了当前回答。这不仅解决了透明度，更是后续做数据飞轮（反馈优化）的基础。

#### 启示四：记忆治理/回滚/审计

像脚本/程序一样被版本化管理、回滚和共享，实现记忆可修复。

引入基于时间轴或 Commit 的记忆管理。所有 Filesystem 中的记忆文件修改，必须保留 Diff。如果发现 Agent 最近的行为变差，人类可以执行 Memory Rollback，将特定目录的记忆回退到三天前。同时，对于外部输入提取的记忆，应赋予"置信度（Confidence Score）"，低置信度的记忆只作为参考，不作为执行依据。

治理是内生能力，不是后补 feature。长期 memory 系统迟早会遇到污染、冲突、实验分支和恢复问题。branch、rollback、audit、quarantine 不应后补。

#### 启示五：记忆遗忘

研究记忆的安全遗忘、置信度衰减和策略化淘汰机制。

结合缓存淘汰算法（如 LRU）和时间衰减曲线（Ebbinghaus）。对于 Vector 平面的实体，如果长时间未被访问且置信度未被强化，其权重自动降低；对于 Filesystem 平面的文件，定期由一个后台 Agent 进行"碎片整理（Defragmentation）"，将过时文件归档（Archive）或打上 `[DEPRECATED]` 标签，防止其污染新的决策。

### 4.3 优先能力方向

| 优先级 | 方向 | 为什么值得先做 |
|--------|------|---------------|
| P0 | L0 + L1 + 基础检索 | 先让记忆可落盘、可读、可查、可扩展 |
| P0 | progressive disclosure | 立刻改善 token 成本和检索噪声 |
| P1 | entity / temporal indexing | 解决跨 session 与时间演化问题 |
| P1 | skill memory | 把真正高价值经验沉淀出来 |
| P1 | governance primitives | 为长期安全演化打底 |
| P2 | shared memory plane + MCP/API | 支撑多 agent 和跨产品 |

### 4.4 建议的最小演进顺序

| 阶段 | 重点能力 | 目标 |
|------|---------|------|
| Phase 1 | L0/L1 + hybrid retrieval + progressive disclosure | 跑通可读、可查、可扩 |
| Phase 2 | entity / temporal indexing + skill memory | 提升跨 session 和记忆复用质量 |
| Phase 3 | governance primitives + MCP/API plane | 进入多 agent / 产品级形态 |
| Phase 4 | active retrieval + adaptive forgetting + benchmark suite | 进入前沿能力竞争 |

---

## 5. 两类路线的比较与融合判断

### 5.1 能力对比

| 维度 | Filesystem-like | Vector/Graph-like |
|------|-----------------|-------------------|
| 人类可读性 | 强 | 中到弱 |
| 手动可修正性 | 强 | 弱于文件层 |
| 多 agent 共享 | 中 | 强 |
| 关系 / 时序建模 | 中 | 强 |
| 程序性记忆沉淀 | 强 | 中 |
| 版本治理自然度 | 强 | 取决于系统设计 |
| northbound API | 弱到中 | 强 |
| 大规模服务化 | 中 | 强 |
| 黑箱风险 | 低到中 | 中到高 |

### 5.2 不是替代关系，而是分工关系

- Filesystem-like 更像 **southbound memory surface**
  - 让人和 agent 看懂记忆
  - 沉淀技能
  - 做局部修正和治理
- Vector/graph-like 更像 **northbound memory plane**
  - 支撑共享
  - 管理关系和时序
  - 为多个 agent / runtime 提供统一调用

### 5.3 当前真正的前沿在哪里

前沿已经不再是"谁又把向量检索调好了一点"，而是：

1. **时间结构**：Graphiti、TiMem、LongMemEval、BEAM 指向了时间维度和超长时程 recall。
2. **实体持续建模**：Honcho、Graphiti 把 memory 从 chunks 提升到 entity state。
3. **程序性记忆**：Voyager、Acontext 把技能层推成一等公民。
4. **治理**：Memoria 把版本、回滚、审计、隔离拉进主舞台。
5. **跨 agent context plane**：mem9、ContextLoom、UltraContext 解决"记忆怎么共享和同步"。

### 5.4 两类路线的共同盲区

- **遗忘与过期策略仍弱**：大多数系统会写入、会召回，但不太会安全地忘。
- **benchmark 与真实工程目标错位**：benchmark 不直接测"工程师能不能修 memory""团队能不能共享""记忆污染后能不能恢复"。
- **跨系统可比性差**：各家用不同模型、不同 judge、不同 cutoff、不同上下文预算。
- **provenance 与 trust 仍未成为行业默认项**：除少数系统外，很多 memory 仍难回答"这条结论从哪来、置信度如何、能否回滚"。

---

## 6. 最终判断

如果只用一句话总结本轮研究：

> **Filesystem-like 路线解决的是"让记忆成为可读、可控、可沉淀的工程资产"；vector/graph-like 路线解决的是"让记忆成为可共享、可关系化、可服务化的语义基础设施"。**

如果再进一步收敛成对 CortexMem 的一句话建议：

> **不要做"更大的记忆库"，而要做"可读的真相层 + 可编排的语义层 + 可演化的技能层 + 可恢复的治理层"。**

---

## 附录 A：Benchmark 数据汇总与正确解读

| 系统 | LoCoMo | LongMemEval | 证据等级 | 正确解读 |
|------|--------|-------------|---------|---------|
| mem0 | +26% vs OpenAI Memory | - | B | LLM-as-a-Judge 指标，非 exact-match |
| TiMem | 75.30% | 76.88%(S) | B | 论文自报，但口径清晰 |
| MIRIX | 85.4% | - | A | 自定义任务胜出，跨系统不可比 |
| Zep/Graphiti | 85.22% | 63.80% | A | 证据较强 |
| EverMemOS | 93.05% | 83.00% | C | 独立复现失败(38.38%)，严重存疑 |
| Honcho | 89.9% | 90.4%(LongMem S) | B | 官方博客自报 |
| OpenViking | +43%-49% improvement | - | A | 项目 README 自报，相对 OpenClaw |

**方法论警示**：
1. 不同 benchmark（LoCoMo、LongMemEval、LongMemEval-S、DMR、BEAM）测的是不同能力，不能直接混排
2. 不同 metric（accuracy、F1、BLEU-1、LLM-as-a-Judge）不能直接并列排名
3. 不同论文使用不同基础模型、embedding、judge model、context budget
4. 产品版本与论文版本可能漂移

## 附录 B：核心参考来源

### 产业系统
- OpenViking: https://github.com/volcengine/OpenViking
- memsearch: https://github.com/zilliztech/memsearch
- memU: https://github.com/NevaMind-AI/memU
- Acontext: https://github.com/memodb-io/Acontext
- Memoria: https://github.com/matrixorigin/Memoria
- mem0: https://github.com/mem0ai/mem0
- mem9: https://github.com/mem9-ai/mem9
- ContextLoom: https://github.com/danielckv/ContextLoom
- eion: https://github.com/eiondb/eion
- Honcho: https://github.com/plastic-labs/honcho
- lossless-claw: https://github.com/Martian-Engineering/lossless-claw

### 核心论文
- CoALA: arXiv:2309.02427
- MemGPT: arXiv:2310.08560
- Voyager: arXiv:2305.16291
- LoCoMo: arXiv:2402.17753
- LongMemEval: arXiv:2410.10813
- mem0: arXiv:2504.19413
- Zep/Graphiti: arXiv:2501.13956
- TiMem: arXiv:2601.02845
- LiCoMemory: arXiv:2511.01448
- MIRIX: arXiv:2507.07957
- EverMemOS: arXiv:2601.02163
- AgentPoison: arXiv:2407.12784
- eTAMP: arXiv:2604.02623
