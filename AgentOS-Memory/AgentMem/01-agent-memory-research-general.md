# Agent Memory System 全面研究报告（v2）

> 研究范围：Filesystem-like、Vector/Graph-like、框架集成、模型原生 四大范式全景
>
> 研究方法：C.A.P.E 框架（Architecture / Cognition / Production / Ecosystem）
>
> 数据规模：25+ 产业系统、57+ 篇学术论文（2025-2026）、7 篇综述、3 个 Benchmark
>
> 证据等级：A（论文+代码可验证）/ B（论文或代码其一）/ C（官方自报）/ X（未找到材料）

---

## 序章：研究范围、方法与演进全景

### 0.1 研究范围

本报告研究 **Agent Memory System（智能体记忆系统）**——定义为同时具备以下三种能力的系统：
1. **跨会话持久化**：记忆在不同会话间保持
2. **可检索/可复用**：记忆可被后续任务检索和应用
3. **可更新/可巩固**：记忆可被修改、遗忘或提炼为更高阶知识

### 0.2 方法论：C.A.P.E 框架

| 维度 | 核心问题 |
|------|---------|
| **A**rchitecture & Paradigm | 技术分类、存储范式、系统定位 |
| **C**ognition & Evolution | 自我进化、结构化推理、遗忘治理 |
| **P**roduction & Engineering | Token 效率、可观测性、运维复杂度 |
| **E**cosystem & Business | 适用场景、生态成熟度、选型指南 |

### 0.3 新增数据规模

本轮研究相比 report.md 新增：
- **产业系统**：13+ 个（Cognee、CrewAI、MetaGPT、LangMem、CAMEL-AI、Swarms、MindForge、MineContext、Ori-Mnemos、MemOS 等）
- **学术论文**：57+ 篇（2026 年 1-4 月占 ~40 篇），涵盖巩固、图结构、遗忘、安全、上下文管理、自进化
- **综述论文**：7 篇
- **Benchmark 论文**：3 篇

### 0.4 证据等级

| 等级 | 含义 |
|------|------|
| **A** | 论文 + 独立复现 / 开源代码可验证 |
| **B** | peer-reviewed paper 或 README 可验证 |
| **C** | 官方自报（博客、README、营销页） |
| **X** | 未找到足够稳定的一手技术材料 |

### 0.5 六个高层结论

1. **文件系统范式正在吸收向量/图能力**：OpenViking 引入语义预滤，memsearch 实现 Dense+BM25+RRF 三路召回——纯文件路线已不再是"纯文件"
2. **框架内置记忆能力正在吞噬独立产品**：CrewAI(49.7k)、MetaGPT(67.4k) 的 star 数远超独立 memory 系统，它们的内置记忆能力对独立 Memory-as-a-Service 构成竞争
3. **遗忘机制从"缺位"到"爆发"**：2026 年 1-4 月涌现 5+ 篇遗忘机制论文（FSFM、Oblivion 等），标志着遗忘从研究盲区变为热点
4. **安全研究从单点攻击到全景治理**：从 AgentPoison(2024) → MINJA(2026) → Memory Security Survey(2026-04)，安全研究已形成完整体系
5. **"记忆+技能+规则"正在统一为经验压缩谱系**：Experience Compression Spectrum(arXiv:2604.15877) 提出记忆/技能/规则沿压缩轴统一，为程序性记忆治理提供理论基础
6. **多 Agent 记忆共享从概念走向协议**：Mesh Memory Protocol(arXiv:2604.19540) 和 Prism(arXiv:2604.19795) 标志着多 Agent 语义互操作正在成为基础设施

---

## 第一部分：C.A.P.E-A 架构与底层范式层

---

## 第1章 Filesystem-like Agent Memory 路线

### 1.1 路线定义与核心问题

Filesystem-like 路线的根本价值：**把记忆重新拉回可读、可控、可迁移的工程对象**。

这类系统的出现不是因为大家突然喜欢 Markdown，而是因为传统 memory/RAG 方案在 Agent 场景里暴露了四类真实问题：

1. **Coding Agent 跨会话"失忆"且记忆不可读**：memsearch 直接瞄准此痛点
2. **24/7 proactive agent 必须持续在线但 token 成本不能线性爆炸**：memU 明确强调
3. **Agent 上下文散落在代码、资源、技能、工具结果里，RAG 很黑箱**：OpenViking 把这一痛点说透
4. **真正可复用的长期能力常常不是一句总结，而是一段可执行技能**：Acontext 和 Voyager 直指同一问题

### 1.2 内部子类型

| 子类型 | 核心目标 | 代表系统 | 新增(本轮) |
|--------|---------|---------|-----------|
| 虚拟文件系统 | 统一虚拟协议管理所有记忆 | OpenViking | - |
| Markdown-first + Shadow Index | 文件为真相，向量为加速缓存 | memsearch | - |
| 类文件系统架构 | 分层目录 + 类型标签 | memU | - |
| 技能即记忆 | Skill file 作为一等公民 | Acontext、Voyager | - |
| 版本控制记忆 | Git-for-Memory | Memoria | - |
| 自动记忆构建 | Self-updating + automatic graph | - | **MemMachine** |
| 递归记忆 | Local-first recursive harness | - | **Ori-Mnemos** |
| DAG 摘要 | 原始消息不丢失，逐层压缩 | lossless-claw | - |
| 上下文工程 | Proactive context-aware | - | **MineContext** |

### 1.3 代表系统深度分析

#### 1.3.1 OpenViking（volcengine/OpenViking）

- **GitHub**：22,900 stars（截至 2026-04） | **License**：AGPL-3.0 | **证据等级**：A
- **核心架构**：`viking://` 虚拟文件系统协议 + L0/L1/L2 分层加载
- **检索**：意图分析 + 向量预滤 + 目录递归探索 + 可视化轨迹
- **自进化**：自动压缩 session → 提取长期记忆 → 更新 User/Agent 目录
- **Benchmark**：LoCoMo10 数据集 1,540 测试用例，43%-49% 完成率提升，83%-91% Token 成本降低 [B]
- **局限**：AGPL-3.0 对商用有约束；依赖 VLM/Embedding 模型
- **对 AgentMem 的启示**：`viking://` 协议范式是 L1 文件系统真相层的直接先例；L0/L1/L2 分层加载为 AgentMem 的 L2a-L2c 渐进式加载提供了产业验证

#### 1.3.2 memsearch（zilliztech/memsearch）

- **GitHub**：1,300 stars（截至 2026-04） | **License**：MIT | **证据等级**：A
- **核心架构**：Markdown-first + Milvus 影子索引
- **检索**：Dense + BM25 + RRF 三路混合召回 + 3 层渐进披露（search → expand → transcript）
- **去重**：SHA-256 内容去重，只对变化内容重新嵌入
- **本地部署**：ONNX bge-m3 模型（~558 MB），降低云依赖
- **对 AgentMem 的启示**：Markdown 为 source of truth、向量为可重建 shadow index 的原则应成为 AgentMem 的设计基本原则；SHA-256 去重方案可直接采用

#### 1.3.3 memU（NevaMind-AI/memU）

- **GitHub**：13,400 stars（截至 2026-04） | **License**：Apache-2.0 | **证据等级**：A
- **核心架构**：Category/Item/Resource + 符号链接 + RAG/LLM 双模式
- **五种记忆标签**：[P] Profile、[E] Event、[K] Knowledge、[B] Behavior、[S] Skill
- **主动式**：自动分类、模式检测、上下文预测
- **集成**：openclaw 生态、PostgreSQL/pgvector
- **对 AgentMem 的启示**：五种记忆标签体系为 AgentMem 的 type 枚举提供了扩展参考；主动式检索为 AgentMem 的"被动→主动"趋势提供验证

#### 1.3.4 Acontext（memodb-io/Acontext）

- **核心架构**：Skill Memory Layer + list_skills → get_skill → get_skill_file 逐层获取
- **蒸馏**：任务完成/失败时自动提取 learnings → skill agent 决定更新或创建
- **延迟**：skill 学习后台异步，约 10-30s
- **对 AgentMem 的启示**：SKILL.md 规范（主指令 + reference + scripts）已被 Acontext 验证可行；不依赖 embedding top-k 而依赖逐层获取的召回策略与 AgentMem 的 L2a-L2c 理念一致

#### 1.3.5 Memoria（matrixorigin/Memoria）

- **GitHub**：206 stars（截至 2026-04） | **License**：Apache-2.0 | **证据等级**：A
- **核心架构**：Git for Memory + Copy-on-Write + snapshot/branch/merge/rollback
- **能力**：版本化对象 + vector + full-text hybrid + contradiction detection + quarantine
- **对 AgentMem 的启示**：Memoria 证明了"版本控制 + 回滚"在 Agent 记忆场景的可行性；但 CoW 依赖 MatrixOne（分布式 HTAP 数据库），运维复杂度高——AgentMem 的 MVP 应用层快照方案更轻量

#### 1.3.6 MemMachine（新增）

- **论文**：arXiv:2604.04853 | **证据等级**：B
- **核心创新**：Ground-Truth-Preserving Memory System，集成短期、情景、画像三级记忆
- **差异化**：批评现有系统过度依赖摘要导致上下文失真，坚持保留原始事实
- **对 AgentMem 的启示**：Ground-truth preservation 原则验证了 AgentMem L1 文件系统真相层的设计选择——原始内容不应被摘要覆盖

#### 1.3.7 Ori-Mnemos（新增）

- **GitHub**：aayoawoyemi/Ori-Mnemos | **License**：开源
- **核心架构**：Local-first + Recursive Memory Harness (RMH)
- **差异化**：完全本地优先，不依赖云端服务
- **对 AgentMem 的启示**：Local-first 范式为 AgentMem 的"个人开发者"场景提供了参考路径

#### 1.3.8 MineContext（新增）

- **GitHub**：volcengine/MineContext | **证据等级**：B
- **核心架构**：Context-Engineering + ChatGPT Pulse，proactive context-aware
- **差异化**：从被动检索转向主动捕捉意图
- **对 AgentMem 的启示**：proactive 能力为 AgentMem 的"被动→主动"演进趋势提供了产业先例

#### 1.3.9 其他新增系统速览

| 系统 | Stars | 核心特征 | 证据等级 |
|------|-------|---------|---------|
| **Hermes Agent**（nousresearch/hermes-agent） | - | Markdown 持久记忆 + 闭环学习循环 + FTS5 + Honcho 用户画像 | B |
| **memos**（MemTensor/MemOS） | - | Memory OS + 图结构 + MemScheduler + 多 Cube 知识库 | B |
| **claude-mem**（thedotmack/claude-mem） | - | Claude Code 插件，自动捕获 + AI 压缩 + 上下文注入 | B |
| **MindOS**（GeminiLight/MindOS） | - | 人机协作心智系统 + 全局同步心智 | C |
| **MindForge**（aiopsforce/mindforge） | - | Vector + concept graphs + 多级记忆结构 | C |

### 1.4 共同机制总结表

| 机制 | 具备的系统 | 说明 |
|------|-----------|------|
| 人类可读文件为真相 | 全部 | Markdown 是主存格式 |
| 向量检索降级为加速层 | OpenViking、memsearch、Memoria | 影子索引可重建 |
| 渐进式披露 | OpenViking(L0-L2)、memsearch(search-expand-transcript)、Acontext | 目录→概览→详情 |
| 程序性记忆是一等公民 | Acontext、Voyager、Hermes Agent、memos | Skill file / SKILL.md |
| 版本控制/回滚 | Memoria、lossless-claw | Git-like 快照 |
| 自动记忆构建 | MemMachine | Self-updating + automatic graph |
| 主动式上下文 | MineContext、memU | 意图预测 + 模式检测 |

### 1.5 优势、边界与当前状态

**核心优势**：人类可读、可审计、可修正、便于 git/version control、适合沉淀 skill/SOP、贴近 coding agent 工作区。

**核心短板**：大规模共享与服务化不如 northbound memory plane；多实体关系推理天然弱于图结构；目录 schema 设计不当会变脏；多 Agent 并发写入需更强治理。

> **对 AgentMem 的启示**：AgentMem 的 L1 层应直接继承 Filesystem-like 路线的最佳实践——Markdown 为真相、SKILL.md 管理程序性记忆、渐进式披露控制 token 消耗。新增系统（MemMachine 的 ground-truth preservation、MineContext 的 proactive 能力）为 L1 的扩展方向提供了新参考。

---

## 第2章 Vector/Graph-like Agent Memory 路线

### 2.1 路线定义与核心问题

Vector/Graph-like 路线的根本价值：**为多 Agent 和复杂检索提供共享语义平面**。

这类系统解决的核心问题是**可共享、可扩展、可关系化**：
1. 多 Agent 框架各有状态但彼此失忆（ContextLoom）
2. 多个 Agent 协作缺少统一 knowledge graph（eion）
3. 持续建模用户/实体状态（Honcho）
4. 生产级通用 memory layer（mem0）

### 2.2 内部子类型

| 子类型 | 核心目标 | 代表系统 | 新增(本轮) |
|--------|---------|---------|-----------|
| Universal Memory Layer | 通用 memory API/服务 | mem0 | - |
| Shared Memory Plane | 多 Agent 共享上下文 | ContextLoom、mem9 | - |
| Graph/Entity Memory | 实体/关系/时序追踪 | Honcho、Graphiti、eion | - |
| Knowledge Engine | 多后端 graph + vector | - | **Cognee** |
| Temporal-Hierarchical | 时间层次化 | TiMem | - |
| Multi-type Orchestration | 多类型协同检索 | MIRIX | - |

### 2.3 代表系统深度分析

#### 2.3.1 mem0（mem0ai/mem0）

- **GitHub**：53,900 stars（截至 2026-04） | **License**：Apache-2.0 (core) | **证据等级**：A
- **核心架构**：Universal memory layer + 多级记忆（User/Session/Agent scope）
- **存储**：向量数据库（15+ 种支持）+ 图数据库（entity linking，非完整图 DB）
- **更新**：LLM 作为"记忆决策机"（ADD/UPDATE/DELETE/NOOP 四路决策）
- **Benchmark**：LoCoMo 91.6、LongMemEval 93.4 [C，README 自报]
- **局限**：依赖外部 LLM/向量库；"graph-enhanced"仅体现为 entity linking
- **对 AgentMem 的启示**：mem0 的高 star 数证明"通用记忆层"定位有市场需求；LLM 决策式更新为 AgentMem L2.5 受控回写提供了参考；但 mem0 的 entity linking 不等于完整图数据库——AgentMem 的 L3 层用 SQLite 邻接表 + CTE 是多跳推理的轻量替代

#### 2.3.2 Graphiti/Zep（getzep/graphiti + getzep/zep）

- **GitHub**：Graphiti 25,300 stars + Zep 4,483 stars（截至 2026-04） | **证据等级**：A
- **核心架构**：时序上下文图（Temporal Context Graph）+ 双时态模型（Bi-temporal Model）
- **三层结构**：Entities（节点，随时变化）、Facts（边，带有效性窗口）、Episodes（原始数据，血统溯源）
- **检索**：semantic + keyword + graph traversal 三路混合 + 异步 NLP 流水线
- **论文**：arXiv:2501.13956（2025 年 1 月提交） [A]
- **对 AgentMem 的启示**：双时态模型（Event Time vs Ingestion Time）是 AgentMem L3 图谱层的核心设计参考——每条关系边必须有 valid_at/invalid_at 时间窗口；Episodes 作为原始数据血统溯源的原则验证了 AgentMem L0/L1 分离的设计

#### 2.3.3 Honcho（plastic-labs/honcho）

- **核心架构**：Entity-Aware State Modeling（workspace/peer/session 抽象）
- **能力**：chat（对实体提问）、search（相似消息）、context（session-scoped）、representation（peer 状态表示）
- **对 AgentMem 的启示**：Honcho 证明了"持续维护实体状态"在用户画像场景的价值，为 AgentMem 的用户画像层提供了参考

#### 2.3.4 eion（eiondb/eion）

- **核心架构**：PostgreSQL + pgvector + Neo4j + unified API + register console
- **能力**：memory MCP tools + knowledge MCP tools + sequential/live agency + guest access
- **差异化**：完整的 PostgreSQL + Neo4j 双后端，统一知识图谱共享存储
- **对 AgentMem 的启示**：eion 验证了 PostgreSQL + Neo4j 作为生产级共享记忆栈的可行性，但运维成本高——AgentMem 的 MVP SQLite 全栈方案在数据量 < 10K 时可替代

#### 2.3.5 ContextLoom（danielckv/ContextLoom）

- **核心架构**：Redis-first shared context + decouple memory from compute
- **能力**：从 PostgreSQL/MySQL/MongoDB 拉冷启动数据 + cycle hash 检测 loop/repetition
- **对 AgentMem 的启示**：Redis-first 模式为 AgentMem 的 Phase 3 多 Agent 场景提供了参考

#### 2.3.6 Cognee（topoteretes/cognee）【新增】

- **GitHub**：16,700 stars（截至 2026-04） | **证据等级**：A
- **核心架构**：Knowledge Engine for AI Agent Memory，多后端（Neo4j/NetworkX/PostgreSQL）graph + vector
- **差异化**：自动知识图谱构建 + 混合检索 + 多模态支持 + 图剪枝
- **与 mem0 对比**：graph-first vs vector-first
- **对 AgentMem 的启示**：Cognee 的高 star 数(16.7k)证明"Knowledge Engine"定位有独立市场价值；图剪枝和多跳推理为 AgentMem L3 层的升级路径提供了参考

#### 2.3.7 LangMem（langchain-ai/langmem）【新增】

- **GitHub**：1,413 stars（截至 2026-04） | **License**：MIT | **证据等级**：A
- **核心架构**：LangChain 专为 LangGraph agent 设计的 memory utilities
- **存储**：LangGraph checkpointers（Postgres/SQLite/Redis/in-memory）
- **差异化**：不是独立服务，直接集成到 LangGraph 状态管理和 checkpointing
- **对 AgentMem 的启示**：LangMem 代表"框架绑定型 memory"路线——与 AgentMem 作为独立库的定位不同，但证明了对 agent framework 深度集成的市场需求

### 2.4 共同机制总结表

| 机制 | 具备的系统 | 说明 |
|------|-----------|------|
| LLM 决策式更新 | mem0、mem9 | ADD/UPDATE/DELETE/NOOP |
| 时序事实追踪 | Graphiti、Honcho | 双时态模型 + 有效性窗口 |
| 多路混合检索 | mem0、Graphiti、eion | semantic + keyword + graph |
| 命名空间隔离 | mem0、mem9、eion、ContextLoom | user/agent/session scope |
| 后台 consolidation | mem0、Graphiti、Honcho | 异步实体提取 + 状态合成 |
| Knowledge Engine | Cognee | 自动图谱构建 + 多后端 |

### 2.5 优势、边界与当前状态

**核心优势**：多 Agent 共享更自然、语义召回与关系推理更强、易于做多租户/权限/workspace、适合规模化生产接入。

**核心短板**：人类可读和直接编辑能力差、provenance 不足时形成更深黑箱、向量/图基础设施提高部署复杂度、容易退化为难以审计的 embedding 池。

> **对 AgentMem 的启示**：AgentMem 的 L2/L3 层应吸收 Vector/Graph-like 路线的多路检索和时序追踪能力，但用 SQLite 全栈降低部署成本。Cognee 的 Knowledge Engine 定位验证了"图谱+向量"组合的工程价值，但 AgentMem 应坚持"文件为真相"原则，向量/图仅为加速层。

---

## 第3章 框架集成路线

### 3.1 为什么需要独立章节

CrewAI(49.7k)、MetaGPT(67.4k)、CAMEL-AI(16.8k) 的 star 数远超独立 memory 系统（mem0 53.9k 除外）。它们的主导接口不是 memory API，而是 agent framework，memory 是"内置能力"而非"独立产品"。但它们的用户规模和生态影响力不可忽视。

### 3.2 代表系统分析

| 系统 | Stars | Memory 架构 | 特点 | 证据等级 |
|------|-------|------------|------|---------|
| **CrewAI** | 49,700 | short-term + long-term + entity memory | 框架内置三级记忆，零配置，ChromaDB 存储 | A |
| **MetaGPT** | 67,400 | shared message pool | 多 agent 消息总线，role-based memory context | A |
| **CAMEL-AI** | 16,800 | role-playing memory | 角色扮演的记忆管理，message history tracking | A |
| **Swarms** | - | collective memory across swarms | 群体记忆共享，知识传递 | C |

### 3.3 框架内置 vs 独立 Memory Layer 权衡

| 维度 | 框架内置（CrewAI/MetaGPT） | 独立 Layer（mem0/AgentMem） |
|------|--------------------------|---------------------------|
| 集成复杂度 | 零配置，开箱即用 | 需编写集成代码 |
| 跨框架 | 锁定单一框架 | 可在不同框架间迁移 |
| 记忆持久性 | 随框架生命周期 | 独立于框架存在 |
| 可调试性 | 依赖框架提供的工具 | 可用外部工具直接查看 |
| 社区生态 | 依赖框架社区 | 独立社区和文档 |
| 适用团队 | 小团队/快速原型 | 需要灵活性和控制力的团队 |

> **对 AgentMem 的启示**：AgentMem 作为独立 memory library，必须提供足够好的接入体验（SDK/API/CLI）以对抗框架内置的"零配置"优势。同时，AgentMem 应提供对主流框架（LangGraph、CrewAI）的适配层，降低集成门槛。

---

## 第4章 模型原生与混合路线

### 4.1 模型原生记忆三大范式

| 维度 | KV 缓存检索（推理前） | MSA 稀疏注意力（推理中） | 参数内化（预训练/后训练） |
|------|---------------------|------------------------|--------------------------|
| 记忆时机 | 推理前压缩/选择 | 推理中实时检索 | 写入参数 |
| 持久性 | 无状态(单次推理) | 无状态(单次推理) | 永久(跨会话) |
| 可解释性 | 中 | 中 | 无(隐式参数编码) |
| 容量 | 受 GPU 显存限制 | 百万-亿级 tokens | 受参数预算限制 |
| 代表 | Memorizing Transformers | - | MemoryLLM |

### 4.2 新增：DeepSeek Engram 与 ICLR STEM

| 系统 | 状态 | 核心技术 | 对 AgentMem 的意义 |
|------|------|---------|-------------------|
| **DeepSeek Engram** | 传闻中，论文待确认 | MoE 中嵌入条件记忆模块，O(1) 确定性知识查找 | 可能挑战"记忆必须是外部系统"假设 |
| **ICLR STEM** | ICLR 2026 论文 | FFN up-projection 替换为 token-indexed embedding 表，即插即用知识编辑 | 证明模型原生记忆可从感知层扩展到知识层 |

### 4.3 混合路线：完整栈

完整栈通常是：**参数记忆/架构记忆 + 推理期上下文机制 + 外部持久用户记忆**。模型原生记忆与外部 agent memory 不是互斥关系，而是不同层级的互补。

### 4.4 新增系统

| 系统 | 核心架构 | 差异化 | 证据等级 |
|------|---------|-------|---------|
| **MemOS**（BUPT+腾讯） | 三层记忆 + 热度驱动更新 + 语义感知检索 | 热度驱动直观有效，LoCoMo F1 +49.11% | B |
| **MineContext** | Context-Engineering + ChatGPT Pulse | 从被动检索到主动意图捕捉 | C |

> **对 AgentMem 的启示**：模型原生记忆目前仅适用于事实性知识的存储和编辑，不适用于情景记忆或程序性记忆——这与 AgentMem 的外部记忆定位不冲突。MemOS 的热度驱动更新机制可被 AgentMem 的调度器借鉴。

---

## 第5章 跨范式对比与融合矩阵

### 5.1 全系统能力对比表

| 系统 | 人类可读 | 多Agent共享 | 关系建模 | 程序性记忆 | 版本治理 | 遗忘机制 | 安全能力 | 部署成本 | Star/引用 |
|------|---------|------------|---------|-----------|---------|---------|---------|---------|-----------|
| OpenViking | ★★★★★ | ★★☆ | ★★☆ | ★★★★ | ★★☆ | ★★☆ | ★★★ | ★★★ | 22.9k |
| memsearch | ★★★★★ | ★★★ | ★★☆ | ★★☆ | ★★☆ | ★★☆ | ★★☆ | ★★★★ | 1.3k |
| memU | ★★★★★ | ★★★ | ★★☆ | ★★★★ | ★★☆ | ★★★ | ★★★ | ★★★ | 13.4k |
| Acontext | ★★★★★ | ★★★ | ★★☆ | ★★★★★ | ★★☆ | ★★☆ | ★★☆ | ★★★★ | - |
| Memoria | ★★★★★ | ★★★ | ★★★ | ★★☆ | ★★★★★ | ★★☆ | ★★★★ | ★★☆ | 206 |
| mem0 | ★★☆ | ★★★★★ | ★★★ | ★★☆ | ★★☆ | ★★★ | ★★★ | ★★☆ | 53.9k |
| Graphiti | ★★★ | ★★★★ | ★★★★★ | ★★☆ | ★★★ | ★★★ | ★★★★ | ★★☆ | 25.3k |
| Honcho | ★★★ | ★★★★ | ★★★★ | ★★☆ | ★★★ | ★★★ | ★★★ | ★★★ | - |
| eion | ★★☆ | ★★★★★ | ★★★★★ | ★★☆ | ★★★ | ★★☆ | ★★★★ | ★☆ | - |
| Cognee | ★★★ | ★★★★ | ★★★★★ | ★★☆ | ★★★ | ★★☆ | ★★★ | ★★☆ | 16.7k |
| CrewAI | ★★★ | ★★★ | ★★☆ | ★★☆ | ★★☆ | ★★☆ | ★★☆ | ★★★★★ | 49.7k |
| MetaGPT | ★★★ | ★★★★ | ★★★ | ★★☆ | ★★☆ | ★★☆ | ★★☆ | ★★★★★ | 67.4k |
| LangMem | ★★☆ | ★★★ | ★★☆ | ★★☆ | ★★★ | ★★☆ | ★★★ | ★★★★ | 1.4k |
| ContextLoom | ★★☆ | ★★★★★ | ★★★ | ★★☆ | ★★☆ | ★★☆ | ★★★ | ★★★ | - |
| **AgentMem** | **★★★★★** | **★★★★** | **★★★★** | **★★★★★** | **★★★★** | **★★★★★** | **★★★★** | **★★★★** | **概念** |

> 注：AgentMem 为设计目标评分，尚未实现

### 5.2 范式融合趋势

| 趋势 | 具体表现 |
|------|---------|
| Filesystem-like 引入向量/图 | OpenViking 语义预滤、memsearch Dense+BM25+RRF |
| Vector/Graph-like 补充可读性 | mem0 entity linking 可解释、Graphiti provenance 链 |
| 框架集成吸收两者 | CrewAI 内置 short/long/entity 三级记忆 |
| 模型原生 + 外部互补 | Engram(模型内知识) + AgentMem(外部情景记忆) |

### 5.3 技术路线演进时间线（2023-2026）

```
2023-Q2: Generative Agents (记忆流) → MemoryBank
2023-Q3: MemGPT/Letta (虚拟上下文管理)
2023-Q4: Voyager (程序性记忆)
2024-Q1: AgentPoison (安全研究起点)
2024-Q2: mem0 开源 → mem0 成为最广泛采用的独立 memory 系统
2024-Q3: Graphiti 开源 → 时序知识图谱记忆
2024-Q4: OpenViking 开源 → 虚拟文件系统范式
2025-Q1: memsearch 开源 → Markdown-first + Shadow Index
2025-Q2: MIRIX (多类型记忆编排)
2025-Q3: MUSE (经验驱动自进化)
2025-Q4: Cognee 获得高关注 → Knowledge Engine 定位
2026-Q1: TiMem (时序层次记忆) / EverMemOS (自组织记忆) / FadeMem (生物遗忘)
2026-Q2: 遗忘机制爆发(FSFM/Oblivion) + 安全全景(Security Survey) + 经验压缩谱系
```

> **对 AgentMem 的启示**：跨范式融合是 AgentMem 的核心价值主张——不是"每个组件首创"，而是"文件可读 + 语义加速 + 图谱推理 + 版本治理"的组合效果优于各组件单独运行。第5章的全系统对比表为 AgentMem 的差异化定位提供了量化支撑。

---

## 第二部分：C.A.P.E-C 认知与演进能力层

---

## 第6章 记忆巩固与提炼机制

### 6.1 巩固机制分类学

| 机制类型 | 触发时机 | 代表系统/论文 | LLM 依赖 |
|---------|---------|--------------|---------|
| 后台蒸馏 | 异步闲时 | Acontext、TSUBASA | 高 |
| LLM 调和 | 写入时 | mem0、mem9 | 高 |
| 时间层次巩固 | 周期性 | TiMem (L1→L2→L3→L4→L5) | 中 |
| 语义引导巩固 | 周期性 | EverMemOS (engram lifecycle) | 高 |
| 主动提取 | 对话中 | MemReader | 高 |
| 上下文蒸馏 | 任务完成 | TSUBASA | 高 |
| 双轨编码 | 写入时 | Dual-Trace Encoding | 中 |

### 6.2 新增论文解读

| 论文 | arXiv | 核心贡献 | 工程启示 |
|------|-------|---------|---------|
| **HeLa-Mem** | 2604.16839 | Hebbian learning 联想记忆，关系记忆网络 | 跨模态关联记忆的生物学启发 |
| **APEX-MEM** | 2604.14362 | 半结构化 + 时序推理 + agentic 管理 | 介于纯向量和纯图之间的中间态 |
| **GAM** | 2604.12285 | 层次化图记忆，平衡获取与保留 | 解决流式系统中瞬态噪声干扰 |
| **HiGMem** | 2604.18349 | LLM 引导的分层记忆，避免纯向量膨胀 | 用 LLM 引导替代纯相似度召回 |
| **MemReader** | 2604.07877 | 主动提取 vs 被动接收 | 处理噪声对话、缺失引用、跨轮依赖 |
| **TSUBASA** | 2604.07894 | 演化记忆 + 上下文蒸馏 | 个人化 LLM 的用户历史跟踪 |
| **AnchorMem** | 2604.17377 | 锚定事实 + 关联上下文 | 批评 Mem0/A-Mem 过度摘要稀释上下文 |
| **Experience Compression Spectrum** | 2604.15877 | 记忆/技能/规则沿压缩轴统一（5-20x → 50-500x → 1000x+） | 为 AgentMem 的程序性记忆治理提供理论框架 |
| **Thought-Retriever** | 2604.12231 | 检索"思维"而非原始数据 | 思维级可解释性，提升检索语义质量 |
| **Dual-Trace Encoding** | 2604.12948 | 事实 + 场景轨迹双编码 | 认知心理学"绘画效应"在记忆中的应用 |

### 6.3 巩固机制对比

| 维度 | 后台蒸馏 | LLM 调和 | 时间层次巩固 | 上下文蒸馏 |
|------|---------|---------|-------------|-----------|
| 触发时机 | 闲时异步 | 写入时 | 周期性 | 任务完成时 |
| LLM 依赖 | 高 | 高 | 中 | 高 |
| 信息保真度 | 中 | 高 | 中 | 高 |
| 计算成本 | 冷路径（不增延迟） | 热路径（增加延迟） | 冷路径 | 冷路径 |
| 适用场景 | 长期记忆提炼 | 即时事实提取 | 个人画像 | 经验沉淀 |

> **对 AgentMem 的启示**：Experience Compression Spectrum 为 AgentMem 的记忆分类提供了理论框架——战略记忆（低压缩）、程序性记忆（中压缩）、工具记忆（高压缩）。AgentMem 的冷/热路径分账原则要求巩固机制必须在冷路径（闲时后台）执行，不影响前台检索延迟。

---

## 第7章 结构化与推理能力

### 7.1 图记忆的结构化层次

| 层次 | 表达力 | 部署成本 | 代表 |
|------|-------|---------|------|
| 轻量认知索引 | 低：仅"谁-何时-相关" | 低 | LiCoMemory CogniGraph |
| 时序知识图谱 | 中：实体+关系+时间窗口 | 中 | Graphiti |
| 多图架构 | 高：语义/时间/因果/实体正交 | 高 | MAGMA (ACL 2026) |
| 层次化图 | 高：知识获取与保留平衡 | 中高 | GAM、HiGMem |
| 世界图 | 极高：本体感知 + 矛盾处理 | 极高 | WorldDB |

### 7.2 新增论文解读

| 论文 | arXiv | 核心贡献 |
|------|-------|---------|
| **MAGMA** | 2601.03236 (ACL 2026 Main) | 多图架构，查询自适应图选择，超越 SOTA |
| **WorldDB** | 2604.18478 | Vector graph-of-worlds + 本体感知写入时调和 + 矛盾处理一等公民 |
| **SCG-MEM** | 2604.20117 | 模式约束的记忆生成，防止结构幻觉，LoCoMo 验证 |
| **Mesh Memory Protocol** | 2604.19540 | 多 Agent 语义互操作协议，跨天/周认知状态共享 |
| **Prism** | 2604.19795 | 全栈分层：文件持久 + 向量语义 + 图关系 + 多 Agent 演化 |

### 7.3 上下文管理与预算

| 论文 | arXiv | 方法 | 关键发现 |
|------|-------|------|---------|
| **ContextBudget** | 2604.01664 | Token 预算约束下的最优检索 | 在有限上下文预算下最大化过去信息保留 |
| **GenericAgent** | 2604.17091 | 上下文信息密度最大化 | 信息密度比窗口长度更重要 |
| **MemCoT** | 2604.08216 | 记忆驱动的 chain-of-thought | 减少因果推理中的幻觉和灾难性遗忘 |
| **Cooperative Memory Paging** | 2604.12376 | 淘汰段替换为关键词书签(~8-24 tokens) | 低成本的记忆召回机制 |
| **Oblivion** | 2604.00131 | 衰减驱动的激活控制 | 解决"always-on"检索导致的干扰和延迟 |

> **对 AgentMem 的启示**：WorldDB 的本体感知写入时调和与矛盾处理为 AgentMem L2.5 受控回写协议提供了高级参考——当机器推理产出与人类记忆冲突时，需要有系统的矛盾解决机制。Cooperative Memory Paging 的关键词书签机制可应用于 AgentMem 的记忆驱逐策略——被淘汰的记忆保留 ~10 token 书签而非完全删除。

---

## 第8章 遗忘与记忆治理

### 8.1 遗忘机制分类学

| 策略 | 触发条件 | 代表 | 核心机制 |
|------|---------|------|---------|
| 被动衰减 | 时间推移 | AgentMem 设计、ACT-R | 指数衰减 S(t) = S₀ × e^(-λt) |
| 主动删除 | 重要性评分低于阈值 | FSFM | 生物启发的选择性遗忘 |
| 安全触发 | 检测到投毒/异常 | Memory Security Survey | 隔离 + 回滚 |
| 合作分页 | 上下文预算不足 | Cooperative Memory Paging | 淘汰段 + 关键词书签 |
| 自适应预算 | 系统资源约束 | Novel Memory Forgetting (arXiv:2604.02280) | 预算控制的遗忘 |

### 8.2 新增论文解读

| 论文 | arXiv | 核心贡献 | 关键数据 |
|------|-------|---------|---------|
| **FSFM** | 2604.20300 | 海马体巩固理论 + Ebbinghaus 曲线的生物启发遗忘 | +8.49% 访问效率, +29.2% 信噪比, 100% 消除安全风险 |
| **Oblivion** | 2604.00131 | 衰减驱动的激活控制 | 解决"always-on"检索的干扰和延迟 |
| **Agent Drift** | 2601.04170 | 行为退化量化，记忆与行为退化关联 | 长时间交互中的渐进式行为退化 |
| **When to Forget** | 2604.12007 | "Memory Worth"指标决定信任/抑制/弃用 | 任务分布偏移时的记忆治理 |
| **Novel Memory Forgetting** | 2604.02280 | 自适应预算遗忘 | LoCoMo 性能从 0.455 降至 0.05 |

### 8.3 安全治理

| 论文 | arXiv | 安全维度 | 关键发现 |
|------|-------|---------|---------|
| **Memory Security Survey** | 2604.16548 | 跨会话投毒、未授权访问、组织状态传播 | 首次全景式 Agent 记忆安全综述 |
| **Opal** | 2604.02522 | 隐私记忆 via Oblivious RAM | 保护检索访问模式隐私 |
| **Governing Evolving Memory** | 2603.11768 | 语义漂移 + 隐私漏洞 | SSGM 框架治理演化记忆 |
| **Safety Risks in Self-Evolving** | 2604.16968 | 经验积累对安全的影响 | 自进化 agent 在 web/具身环境中的安全风险 |

### 8.4 治理机制对比

| 维度 | FSFM | Oblivion | AgentMem 设计 |
|------|------|---------|--------------|
| 遗忘触发 | 生物模型（海马体） | 衰减激活 | 指数衰减 + 类型差异化 λ |
| 可恢复性 | 是（潜伏非删除） | 是（降级非删除） | 是（inactive 标记非删除） |
| 计算开销 | 中 | 低 | 低（冷路径异步） |
| 对检索精度影响 | +8.49% | 改善信噪比 | 目标保持 Top-K 精度 |

> **对 AgentMem 的启示**：FSFM 的"遗忘不是删除而是降权"理念已被纳入 AgentMem 的设计（inactive 标记策略）。Memory Security Survey(2604.16548) 是 AgentMem 安全栈的最新参考——AgentMem 的三级防御应以该综述中的攻击分类为基线。Opal 的 ORAM 方案为 AgentMem 的隐私保护场景提供了可选增强。

---

## 第三部分：C.A.P.E-P 工程与生产力层

---

## 第9章 Token 效率与检索工程

### 9.1 Token 效率方法汇总

| 方法 | 代表系统 | 效果 | 指标定义 |
|------|---------|------|---------|
| 分层加载(L0/L1/L2) | OpenViking | 输入 token 降低 83%-91% | 相对全量上下文注入 [B] |
| 稀疏读写 | mem0 | token 节省 90%+ | README 自报 [C] |
| 渐进式披露 | memsearch、Acontext | 按需加载 | 无需 LLM 的路径 [A] |
| 复杂度感知召回 | TiMem | 召回记忆长度减少 52.20% | 召回冗余减少 [B] |
| DAG 压缩 | lossless-claw | 保留原始但压缩上下文 | 无损压缩 [B] |
| 上下文蒸馏 | TSUBASA | 持续个人化压缩 | 蒸馏后 token 减少 [B] |

### 9.2 方法论警示

**不同指标不可直接比较**：
- TiMem 的 52.2% 是"召回记忆长度减少" ≠ "Token 节省率"
- OpenViking 的 83-91% 是相对"全量上下文注入"基线
- 没有任何系统完整报告"净 Token 效率"（扣除记忆系统自身 LLM 消耗后的真实节省）

**AgentMem 的净 Token 效率公式**：
`净 Token 节省 = (全量基线 - 注入窗口) - 记忆系统自身LLM消耗`

### 9.3 检索延迟分析

| 系统 | 热路径延迟 | 说明 |
|------|-----------|------|
| ContextLoom | sub-millisecond | Redis-first [C] |
| memsearch | <500ms | BM25 + Dense 本地模型 [B] |
| Graphiti | 异步 NLP 流水线 | 前台查询快，后台提取延迟 [A] |
| AgentMem 目标 | 热路径 <350ms | 规则引擎 + SQLite [D，推测] |

> **对 AgentMem 的启示**：AgentMem 的 SQLite 全栈 MVP 方案在数据量 < 10K 时可达到与 memsearch 相当的延迟水平（<500ms）。入口校验必须使用纯规则引擎（非 LLM）才能满足 <150ms 延迟目标。

---

## 第10章 可观测性、安全与运维

### 10.1 可观测性与透明度

| 系统 | 可观测机制 | 人类可读 | 检索轨迹 | 版本历史 |
|------|-----------|---------|---------|---------|
| OpenViking | 可视化 retrieval trajectory | ★★★★★ | ✅ | ❌ |
| memsearch | Markdown 直接查看 + git | ★★★★★ | ❌ | ✅ (via git) |
| Graphiti | provenance chain | ★★★ | ❌ | ✅ |
| Memoria | full audit trail | ★★★★★ | ❌ | ✅✅ |
| AgentMem 设计 | AgentTrace 三层日志 + 快照 | ★★★★★ | ✅ | ✅ |

### 10.2 安全分析全景

#### 攻击类型

| 攻击 | 论文 | 原理 | 成功率 | 年份 |
|------|------|------|--------|------|
| **AgentPoison** | arXiv:2407.12784 | 污染长期记忆/RAG 知识库 | ASR >80% (poison rate <0.1%) | 2024 |
| **MINJA** | arXiv:2601.05504 | 长程记忆注入 | 理想 95% 注入/70% 攻击，真实大幅下降 | 2026 |
| **eTAMP** | arXiv:2604.02623 | 环境观察污染 | ASR 32.5%，frustration exploit 可 ×8 | 2026 |
| **Cross-session poisoning** | arXiv:2604.16548 | 跨会话投毒综述 | 综述覆盖 | 2026 |

#### 防御矩阵

| 防御层 | 安全措施 | 覆盖攻击 | 延迟 |
|--------|---------|---------|------|
| 入口校验 | 纯规则引擎 + 来源可信度 | AgentPoison 直接注入 | <150ms |
| 记忆免疫 | 已有记忆一致性检查 | MINJA 多 Agent 传播 | <200ms |
| 版本回滚 | 快照 + 异常检测 | eTAMP 未知攻击 | ~0ms 异步 |
| 隔离 | 低置信隔离 + 沙箱 | 逃逸检测 | 冷路径 |

### 10.3 运维复杂度评估

| 系统 | 存储后端数 | 后端类型 | 运维复杂度 |
|------|-----------|---------|-----------|
| mem0 | 1-2 | Vector DB + LLM API | ★★☆ |
| memsearch | 2 | Markdown + Milvus | ★★☆ |
| Graphiti | 2 | Neo4j + Vector | ★★★ |
| eion | 3 | PostgreSQL + pgvector + Neo4j | ★★★★ |
| ContextLoom | 2-3 | Redis + SQL DB | ★★★ |
| Cognee | 2-3 | Neo4j/NetworkX + Vector | ★★★ |
| **AgentMem MVP** | **2** | **Filesystem + SQLite** | **★☆** |
| AgentMem Phase 3 | 4 | FS + Milvus + Neo4j + MatrixOne | ★★★★★ |

> **对 AgentMem 的启示**：运维复杂度是 AgentMem SQLite 全栈 MVP 的核心差异化优势——2 个后端 vs 竞品 2-4 个。但随着规模增长到 Phase 3，运维复杂度将超过 eion。因此 AgentMem 的每个阶段必须有明确的升级触发条件（数据量阈值、推理复杂度阈值），避免过早引入重量级依赖。

---

## 第11章 Benchmark 与评测体系

### 11.1 已有 Benchmark 回顾

| Benchmark | 测试维度 | 说明 |
|-----------|---------|------|
| **LoCoMo** | 300+ 回合长程因果时序一致性 | 非核心场景（对话），但行业通用名片 |
| **LongMemEval** | 知识更新 + 拒答机制 | 含 S/Full 两个版本 |
| **BEAM** | 1M token 级长程基准 | mem0 README 数据 |
| **DMR** | 对话记忆检索 | Graphiti 论文使用 |

### 11.2 新增 Benchmark

| 论文 | arXiv | 基准 | 独特价值 |
|------|-------|------|---------|
| **From Recall to Forgetting** | 2604.20006 | 记忆巩固 + 知识更新处理 | 首个关注"遗忘"能力的基准 |
| **SkillLearnBench** | 2604.20087 | 持续技能学习（20 任务 / 15 子领域） | 程序性记忆的持续学习基准 |
| **AgenticAI-DialogGen** | 2604.12179 | 主题引导对话生成 | 短/长期记忆联合评估 |

### 11.3 全系统 Benchmark 数据汇总表

| 系统 | LoCoMo | LongMemEval | BEAM(1M) | 证据等级 |
|------|--------|-------------|----------|---------|
| mem0 | 91.6 | 93.4 | 64.1 | C (README 自报) |
| TiMem | 75.30% | 76.88%(S) | - | B (论文自报) |
| Graphiti | 85.22% | 63.80% | - | A (论文) |
| MIRIX | 85.4% | - | - | A (自定义任务) |
| EverMemOS | 93.05% | 83.00% | - | C (独立复现失败 38.38%) |
| Honcho | 89.9% | 90.4%(S) | - | C (博客自报) |
| OpenViking | +43%-49% improvement | - | - | B (README) |
| Omni-SimpleMem | F1 0.117→0.598 | - | - | B (论文) |
| FadeMem | superior (无数值) | - | - | B (论文) |
| **AgentMem MVP 目标** | **>65%** | **待测** | - | - |

### 11.4 7 篇综述论文的核心发现

| 综述 | arXiv | 核心发现 |
|------|-------|---------|
| Memory for Autonomous LLM Agents | 2603.07670 | 自主 LLM agent 记忆机制的分类与评估协议 |
| Anatomy of Agentic Memory | 2602.19320 | 现有 benchmark 规模不足、指标与语义效用错位 |
| Graph-based Agent Memory Survey | 2602.05665 | 图记忆的分类、技术和应用全景 |
| Rethinking Memory Mechanisms | 2602.06052 | 基础 agent 记忆的真实效用 vs 上下文爆炸 |
| The AI Hippocampus | 2601.09113 | 现代 LLM 记忆机制与人类记忆架构的对比差距 |
| Memory in the Age of AI Agents | 2512.13564 | 记忆研究的碎片化问题和分类 |
| Security of Long-Term Memory | 2604.16548 | 跨会话投毒、未授权访问、共享状态传播的全景 |

### 11.5 评测方法论建议

1. **拒绝单一 SOTA 排名表**：先问比较的是不是同一类系统，再问 benchmark/metric/模型底座是否一致
2. **场景化评测优先**：MVP 核心指标应为"跨会话代码约束回忆率 >90%"而非 LoCoMo
3. **热/冷路径成本分账**：所有效率指标分别报告热路径和冷路径
4. **组合增效验证**：证明 L1+L2+L3 组合效果优于各单独系统

> **对 AgentMem 的启示**：SkillLearnBench 是 AgentMem 程序性记忆治理方向的直接评测基准。From Recall to Forgetting 验证了 AgentMem 遗忘机制设计的合理性——记忆系统不仅要能"记住"，还要能"遗忘"。AgentMem 的评测体系应建立自定义场景 benchmark（编码约束回忆、SOP 蒸馏、投毒回滚），而非仅依赖学术 benchmark。

---

## 第四部分：C.A.P.E-E 业务与生态层

---

## 第12章 场景映射与选型指南

### 12.1 场景-系统匹配矩阵

| 场景 | 推荐路线 | 首选系统 | 备选系统 | 关键考量 |
|------|---------|---------|---------|---------|
| Coding Agent | Filesystem-like | memsearch + AgentMem | OpenViking | 可读性 + 版本控制 |
| Personal Assistant | 混合 | mem0 + TiMem | Honcho | 实体建模 + 个性化 |
| Multi-Agent | Vector/Graph | eion + ContextLoom | CrewAI built-in | 共享命名空间 |
| Enterprise Copilot | 混合 | Graphiti + Memoria | AgentMem | 安全 + 审计 |
| Research Agent | Filesystem | OpenViking | memU | 资源管理 |
| Swarm/Collective | 框架集成 | Swarms + MetaGPT | CAMEL-AI | 群体记忆 |

### 12.2 不同规模团队推荐栈

| 团队规模 | 推荐栈 | 理由 |
|---------|-------|------|
| 个人开发者 | MemMachine / Ori-Mnemos / xiaoclaw-memory | 零运维成本，本地优先 |
| 小团队（2-10人） | mem0 / memsearch / CrewAI | 低配置，快速启动 |
| 中团队（10-50人） | Graphiti / Cognee / AgentMem MVP | 可控复杂度，组合增效 |
| 大企业（50+人） | eion / Memoria / AgentMem Phase 3 | 安全 + 审计 + 多 Agent |

### 12.3 选型决策树

```
是否需要人类直接读写记忆？
  ├── 是 → 是否需要向量/图加速？
  │       ├── 是 → Filesystem-like + Shadow Index (memsearch, AgentMem)
  │       └── 否 → 纯文件系统 (Ori-Mnemos)
  └── 否 → 是否需要多 Agent 共享？
          ├── 是 → Vector/Graph-like (eion, ContextLoom, Cognee)
          └── 否 → 框架内置 (CrewAI, MetaGPT) 或独立层 (mem0)
```

> **对 AgentMem 的启示**：AgentMem 的核心目标场景是"Coding Agent + Enterprise Copilot"交叉区域——既需要文件可读性（Coding），又需要安全审计和版本回滚（Enterprise）。在这个交叉区域，AgentMem 的主要竞品是 memsearch（有 L1+L2 但无回滚）和 Memoria（有回滚但无索引同步）。

---

## 第13章 趋势、空白与 AgentMem 定位

### 13.1 六大演进趋势

| 趋势 | 方向 | 证据 |
|------|------|------|
| 静态 → 动态 | 从 CRUD 到自适应巩固 | TiMem, EverMemOS, TSUBASA, 自进化论文群 |
| 被动 → 主动 | Active Retrieval + 预测性上下文 | MIRIX, MineContext, memU, MemReader |
| 单体 → 集体 | 跨 agent 语义互操作 | Mesh Memory Protocol, Prism, Swarms, eion |
| 扁平 → 分层 | 从单一向量池到多级架构 | TiMem, AgentMem, MemOS, GAM, HiGMem |
| 黑盒 → 透明 | 检索轨迹 + 版本治理 | AgentTrace, Memoria, MemMachine |
| 仅记忆 → 记忆+技能+规则 | 经验压缩谱系 | Acontext, Voyager, Experience Compression Spectrum |

### 13.2 行业空白与 AgentMem 机会

| 空白领域 | 现状 | AgentMem 方案 |
|---------|------|--------------|
| 程序性记忆治理 | 仅 Voyager/Acontext 有学术验证 | SKILL.md + SOP 蒸馏 |
| 知识回涌 | 无系统解决 | L2.5 受控回写协议（confidence 分级） |
| 安全遗忘 | 学术界有(FSFM/Oblivion)，工程缺 | 分层衰减策略（fact/procedure/profile 差异化 λ） |
| 版本回滚 + 索引同步 | Memoria 有回滚但无索引同步 | 快照回滚 + 索引自动重建 |
| 多后端运维简化 | 竞品 3-4 个后端 | SQLite 全栈 MVP（2 个后端） |
| 组合增效验证 | 未被独立验证 | L1+L2+L3 协同测试 |

### 13.3 AgentMem 差异化定位更新

基于本轮 25+ 系统的对比，AgentMem 的 6 个差异化定位更新如下：

1. **L1+L2+L3 三层主路径 + SQLite 全栈 MVP**：运维成本较竞品降低 60%-70%（2 个后端 vs 3-4 个），但保留明确升级路径
2. **程序性记忆治理**：SKILL.md 规范 + SOP 自动蒸馏，参照 Voyager/MUSE/PlugMem/Memp
3. **L2.5 受控回写协议**：唯一无产业先例的技术方向，confidence 分级回写
4. **版本回滚 + 索引同步**：Memoria 有回滚但 L2 索引不会自动同步——这是 AgentMem 的独特能力
5. **安全遗忘分层衰减**：不同类型记忆差异化 λ（fact=0.05, procedure=0.001, profile=0.005），基于 FSFM 理念
6. **热/冷路径成本分账**：所有效率指标分别报告，禁止合并为单一"节省率"

### 13.4 风险矩阵更新

| 风险 | 等级 | 缓解措施 |
|------|------|---------|
| 学术引用不完整 | 中 | critical-analysis.md 已核实 32 条数据声明 |
| L2.5 零先例 | 高 | 标为"实验性"，Phase 2 PoC 验证 |
| 安全栈延迟 | 高 | 入口校验纯规则引擎 <150ms |
| 存储后端复杂度 | 高 | MVP 仅 2 个后端，明确升级触发条件 |
| 框架集成竞争 | 中 | 提供 LangGraph/CrewAI 适配层 |

> **对 AgentMem 的启示**：AgentMem 的核心价值主张是"组合增效"——不是每个组件首创，而是组合后的整体效果优于各组件单独运行的总和。L1+L2+L3 的组合必须证明比 memsearch(L1+L2) 或 Graphiti(L2+L3) 单独运行有更好的检索精度和治理能力。这是 AgentMem 必须在 MVP 阶段验证的核心假设。

---

## 附录

### A. 新增产业系统速查表

| 系统 | Stars | 架构类型 | 一句话描述 | 链接 |
|------|-------|---------|-----------|------|
| Cognee | 16,700 | Knowledge Engine | 自动知识图谱构建 + 混合检索 | github.com/topoteretes/cognee |
| CrewAI | 49,700 | 框架集成 | 内置三级记忆的 multi-agent 框架 | github.com/crewAIInc/crewAI |
| MetaGPT | 67,400 | 框架集成 | 共享消息池的多 agent 软件工程 | github.com/FoundationAgents/MetaGPT |
| LangMem | 1,413 | 框架集成 | LangGraph agent 的 memory utilities | github.com/langchain-ai/langmem |
| CAMEL-AI | 16,800 | 框架集成 | 角色扮演 agent 的记忆管理 | github.com/camel-ai/camel |
| MemMachine | - | 自动记忆构建 | Ground-truth preserving 记忆系统 | arXiv:2604.04853 |
| Ori-Mnemos | - | 递归记忆 | Local-first recursive memory harness | github.com/aayoawoyemi/Ori-Mnemos |
| MineContext | - | 上下文工程 | Proactive context-aware AI partner | github.com/volcengine/MineContext |
| MemOS | - | 记忆 OS | 三层记忆 + 热度驱动更新 | arXiv + molbit |
| MindForge | - | 混合记忆 | Vector + concept graphs + multi-level | github.com/aiopsforce/mindforge |
| Hermes Agent | - | 自我进化 | Markdown 持久记忆 + 闭环学习 | github.com/nousresearch/hermes-agent |
| Swarms | - | 集体记忆 | Agent 群体共享记忆池 | swarms.ai |
| MindOS | - | 心智系统 | 人机协作心智系统 + 全局同步 | github.com/GeminiLight/MindOS |

### B. 新增学术论文速查表

#### 巩固与提炼
| 论文 | arXiv | 核心贡献 |
|------|-------|---------|
| HeLa-Mem | 2604.16839 | Hebbian 学习联想记忆网络 |
| APEX-MEM | 2604.14362 | 半结构化 + 时序推理记忆 |
| GAM | 2604.12285 | 层次化图 agent 记忆 |
| HiGMem | 2604.18349 | LLM 引导分层记忆系统 |
| MemReader | 2604.07877 | 主动提取长期记忆 |
| TSUBASA | 2604.07894 | 演化记忆 + 上下文蒸馏 |
| AnchorMem | 2604.17377 | 锚定事实 + 关联上下文 |
| Experience Compression Spectrum | 2604.15877 | 记忆/技能/规则统一压缩谱 |
| Thought-Retriever | 2604.12231 | 检索思维非原始数据 |
| Dual-Trace Encoding | 2604.12948 | 事实 + 场景轨迹双编码 |

#### 图结构与上下文
| 论文 | arXiv | 核心贡献 |
|------|-------|---------|
| WorldDB | 2604.18478 | Vector graph-of-worlds + 本体感知调和 |
| SCG-MEM | 2604.20117 | 模式约束的记忆生成 |
| Mesh Memory Protocol | 2604.19540 | 多 Agent 语义互操作协议 |
| Prism | 2604.19795 | 全栈分层记忆架构 |
| ContextBudget | 2604.01664 | Token 预算约束最优检索 |
| GenericAgent | 2604.17091 | 上下文信息密度 > 窗口长度 |
| MemCoT | 2604.08216 | 记忆驱动 chain-of-thought |
| Cooperative Memory Paging | 2604.12376 | 淘汰段关键词书签 |
| Oblivion | 2604.00131 | 衰减驱动激活控制 |

#### 遗忘与安全
| 论文 | arXiv | 核心贡献 |
|------|-------|---------|
| FSFM | 2604.20300 | 生物启发选择性遗忘 |
| When to Forget | 2604.12007 | Memory Worth 治理原语 |
| Agent Drift | 2601.04170 | 行为退化量化 |
| Memory Security Survey | 2604.16548 | Agent 记忆安全全景综述 |
| Opal | 2604.02522 | 隐私记忆 via Oblivious RAM |
| Governing Evolving Memory | 2603.11768 | 语义漂移 + 隐私 SSGM 框架 |
| Safety Risks in Self-Evolving | 2604.16968 | 自进化 agent 安全风险 |
| Novel Memory Forgetting | 2604.02280 | 自适应预算遗忘 |

### C. 综述论文摘要

| 综述 | arXiv | 核心发现 |
|------|-------|---------|
| Memory for Autonomous LLM Agents | 2603.07670 | 自主 LLM agent 的记忆机制、评估协议、新兴方向的结构化综述 |
| Anatomy of Agentic Memory | 2602.19320 | 发现现有 benchmark 规模不足、指标与语义效用错位，需要更贴近真实场景的评估 |
| Graph-based Agent Memory | 2602.05665 | 图记忆从轻量索引到重型 KG 的梯度，及其在各领域的应用 |
| Rethinking Memory Mechanisms | 2602.06052 | 基础 agent 记忆的真实效用 vs 上下文爆炸的矛盾，呼吁回归场景化评估 |
| The AI Hippocampus | 2601.09113 | 现代 LLM 记忆机制与人类海马体/新皮层记忆架构的系统性对比 |
| Memory in the Age of AI Agents | 2512.13564 | Agent 记忆研究的碎片化问题，动机/实现/评估协议的分类与统一框架 |
| Security of Long-Term Memory | 2604.16548 | 首次全景式 Agent 记忆安全综述，覆盖跨会话投毒、未授权访问、共享状态传播 |

### D. Benchmark 论文摘要

| Benchmark | arXiv | 测试维度 |
|-----------|-------|---------|
| From Recall to Forgetting | 2604.20006 | 记忆巩固 + 频繁知识更新处理，超越简单事实检索 |
| SkillLearnBench | 2604.20087 | 20 任务 / 15 子领域的持续技能学习基准 |
| AgenticAI-DialogGen | 2604.12179 | 主题引导对话生成，短/长期记忆联合评估 |

### E. 全系统存储后端对比表

| 系统 | 后端数 | 后端类型 |
|------|-------|---------|
| mem0 | 1-2 | Vector DB (Qdrant/Pinecone) + LLM API |
| memsearch | 2 | Markdown (FS) + Milvus (Lite) |
| Graphiti | 2 | Neo4j + Vector embedding |
| Zep | 3 | PostgreSQL + Weaviate/Qdrant + Neo4j |
| eion | 3 | PostgreSQL + pgvector + Neo4j |
| Cognee | 2-3 | Neo4j/NetworkX + Vector DB |
| ContextLoom | 2-3 | Redis + PostgreSQL/MySQL/MongoDB |
| LangMem | 1 | LangGraph checkpointer (SQLite/Postgres/Redis) |
| Memoria | 2 | MatrixOne (CoW) + Vector |
| OpenViking | 1-2 | FS + embedded vector |
| **AgentMem MVP** | **2** | **Filesystem (MD) + SQLite (FTS5+adjacency)** |

### F. 来源索引

- OpenViking: https://github.com/volcengine/OpenViking
- memsearch: https://github.com/zilliztech/memsearch
- memU: https://github.com/NevaMind-AI/memU
- Acontext: https://github.com/memodb-io/Acontext
- Memoria: https://github.com/matrixorigin/Memoria
- mem0: https://github.com/mem0ai/mem0
- Graphiti: https://github.com/getzep/graphiti
- Zep: https://github.com/getzep/zep
- Honcho: https://github.com/plastic-labs/honcho
- eion: https://github.com/eiondb/eion
- ContextLoom: https://github.com/danielckv/ContextLoom
- Cognee: https://github.com/topoteretes/cognee
- CrewAI: https://github.com/crewAIInc/crewAI
- MetaGPT: https://github.com/FoundationAgents/MetaGPT
- CAMEL-AI: https://github.com/camel-ai/camel
- LangMem: https://github.com/langchain-ai/langmem
- Ori-Mnemos: https://github.com/aayoawoyemi/Ori-Mnemos
- MindForge: https://github.com/aiopsforce/mindforge
- MineContext: https://github.com/volcengine/MineContext
- Hermes: https://github.com/nousresearch/hermes-agent
- MindOS: https://github.com/GeminiLight/MindOS
- MemOS/memos: https://github.com/MemTensor/MemOS
- MemMachine: arXiv:2604.04853
- claude-mem: https://github.com/thedotmack/claude-mem
- Swarms: https://swarms.ai

---

*报告完成。所有数据截至 2026-04-23。*
