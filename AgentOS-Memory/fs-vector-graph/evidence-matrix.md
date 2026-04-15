# Filesystem-like / Vector-Graph-like Agent Memory 证据矩阵

> 说明：
> - `类别` 按本专题报告的主导接口归类。
> - `证据等级` 含义见主报告。
> - `主线结论` 表示该项目是否被用于支撑核心结论。

| 系统 | 类别 | 一手来源 | 已核验的核心事实 | 公开量化 | 证据等级 | 主线结论 | 备注 |
|------|------|----------|------------------|----------|----------|----------|------|
| OpenViking | Filesystem-like | 官方 GitHub README / 官方站点 | 用 filesystem paradigm 统一 memory/resource/skill；支持层级加载、目录递归检索、retrieval trajectory、session 自迭代；README 明确给出相对 OpenClaw / LanceDB 的项目自报 benchmark | `43%-49%` improvement；`83%-91%` input-token reduction；LoCoMo10 `1,540` cases | A | 是 | 主项目 AGPLv3，部分子组件 Apache 2.0；不能把局部许可误读为整体许可 |
| memsearch | Filesystem-like | 官方 GitHub README / 文档 | Markdown 是 source of truth；Milvus 是 shadow index；支持 dense + BM25 + RRF 与三段式 recall | `4` 平台；`3` 层 recall；默认模型约 `558 MB`；Milvus Lite 单文件 | A | 是 | 对 coding agent 场景最清晰；无公开统一 benchmark |
| memU | Filesystem-like | 官方 GitHub README | 面向 24/7 proactive agents；memory as file system；后台 bot 监控与长期主动记忆；强调小上下文成本 | one-click install `<3 min`；官方自报 comparable usage 约 `~1/10` | A | 是 | 主动式记忆路线很鲜明，量化指标主要为官方口径 |
| Acontext | Filesystem-like | 官方 GitHub README / 官方 docs | Skill memory layer；任务完成/失败后蒸馏为 skill files；用工具逐层拉取，不走 embedding top-k | `2` SDK；学习延迟 `10-30s`；默认 task/SOP agent 最大迭代均为 `4` | A | 是 | 对“技能即记忆”定义非常清晰；更像 context+skills 平台 |
| Voyager | Filesystem-like / Procedural | 原始论文 | 通过 executable code skill library 做长期程序性记忆与复用 | `3.3x` 更多独特物品；`15.3x` 更快里程碑 | A | 是 | 不是通用 memory product，但程序性记忆价值很强 |
| Memoria | Filesystem-like / Governance | 官方 GitHub README | Git for AI agent memory；snapshot/branch/merge/rollback；CoW；hybrid retrieval；audit trail | `2` 种部署；`6` 类 agent/client 图标；`4` 类版本操作主语义 | A | 是 | 更偏治理层/基础设施层 |
| XiaoClaw | 生态弱证据 | 官方站点 / 安装页 | 本质更像 OpenClaw 的一键安装与运行时封装，不是独立 memory architecture | 无可靠官方 benchmark | X | 否 | 仅用于说明生态包装层，不用于技术主结论 |
| ContextLoom | Vector/Graph-like | 官方 GitHub README | Redis-first shared context state；memory from compute decoupling；cold start hydration；cycle hash 检测循环 | `4` 个框架 wrapper；官方宣称 sub-millisecond retrieval | B | 是 | 项目较早期，但设计目标明确 |
| eion | Vector/Graph-like | 官方 GitHub README | shared memory storage + unified knowledge graph；Postgres+pgvector+Neo4j；支持 multi-agent sequential/concurrent/guest access | `4` 个 memory tools + `4` 个 knowledge tools；`384` 维 embeddings | B | 是 | 多 Agent 与权限模型表达清晰，生态尚早期 |
| honcho | Vector/Graph-like | 官方 GitHub README / 官方 docs / 官方 blog | stateful agents memory library；围绕 entities/peers/session/context/representation 持续建模 | 官方自报 `90.4%` LongMem S、`89.9%` LoCoMo、约 `60%` cost reduction；`10_000` token context 示例 | B | 是 | 更偏 entity-aware state modeling；benchmark 主要来自官方自报 |
| mem0 | Vector/Graph-like | 官方 docs / 官方 repo / 原始论文 | universal self-improving memory layer；抽取、整合、召回；产品化与集成成熟 | `+26%`、`91%` faster、`90%` fewer tokens；GitHub `53.1k` stars | A | 是 | 典型通用 memory layer |
| mem9 | Vector/Graph-like | 官方 GitHub README / 官方站点 | 以 stateless plugins + central memory server 共享 memory pool；TiDB Cloud Starter 混合检索；视觉面板；集中控制 | `3` 原生插件 + HTTP；`5` tools；`25 GiB / 250M RU` 免费层 | B | 是 | 适合 coding agent 协作，更多效果是项目自报或产品口径 |

## 旁系参照（用于完善判断，不作为本专题主清单）

| 系统 | 角色 | 一手来源 | 吸收的合理结论 | 证据等级 | 备注 |
|------|------|----------|----------------|----------|------|
| TiMem | 时间层次化参照 | 原始论文 | 时间层次化 consolidation 与 complexity-aware recall 值得借鉴 | B | 用于补强 northbound memory 的时间尺度设计 |
| LiCoMemory | 轻量图索引参照 | 原始论文 | 图更适合作为检索导航层，而非总是做重型 KG | B | 用于补强轻量结构化索引观点 |
| MIRIX | 多类型记忆参照 | 原始论文 / 官方 docs | memory types orchestration 与 active retrieval 值得借鉴 | B | 用于补强“多类型北向记忆”观点 |
| EverMemOS | 反面教训参照 | 原始论文 | engram lifecycle 概念有启发，但复现与可信度必须谨慎 | C | 只保留方法论启发，不将其高分结果写入主结论 |
| xiaoclaw-memory | 弱证据条目 | 未找到稳定官方一手技术链条 | 旧稿中的极简 Markdown 架构有启发，但本轮无法将其作为可靠项目纳入 | X | 不进入主线结论 |
| lossless-claw | 弱证据条目 | 未找到足够稳定的官方一手技术链条 | append-only 原始记录 + 分层摘要是合理模式，但不依赖该项目来证明 | X | 只保留概念，不保留项目级结论 |

## 证据使用原则

### 可以作为强支撑的结论

- Filesystem-like 路线强调可读、可编辑、渐进式披露、skill memory 与治理能力
- Vector/graph-like 路线强调 northbound API、共享状态、关系化与多 Agent 协作
- Cortex-Mem 适合做混合架构，而不是单路线押注

### 不能作为强支撑的结论

- 统一 benchmark 总排名
- 各系统之间跨口径的绝对性能优劣
- XiaoClaw 作为独立 memory technology 的代表性结论

## 本轮最重要的证据判断

1. `memsearch`、`Acontext`、`Memoria` 证明 filesystem-like 路线不是“没有检索能力”，而是把检索置于文件真相层之下。
2. `ContextLoom`、`eion`、`honcho`、`mem0`、`mem9` 证明 northbound memory plane 已经从“向量库调用”演进到“共享状态 / 表示层 / 图层”。
3. `XiaoClaw` 更像 OpenClaw 的封装产品，而不是本研究要重点分析的 memory core。
4. 旧稿里关于 TiMem、LiCoMemory、MIRIX 的判断，在“时间层次化”“轻量图索引”“多类型编排”三个方向上是有保留价值的，但它们更适合做旁系参照，而不是替代本专题主清单。
