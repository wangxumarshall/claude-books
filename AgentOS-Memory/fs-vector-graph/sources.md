# Filesystem-like / Vector-Graph-like Agent Memory 来源索引

> 访问时间：2026-04-15
>
> 原则：
> - 优先保留官方仓库、官方文档、原始论文、官方项目页。
> - 次级来源只用于定位，不用于证明核心技术事实。

---

## Filesystem-like Agent Memory

### OpenViking

- 官方仓库：<https://github.com/volcengine/OpenViking>
- 官方站点：<https://www.openviking.ai/>

本轮主要使用内容：

- context database 定位
- fragmented context / flat RAG / unobservable retrieval 的问题定义
- filesystem paradigm
- L0/L1/L2 分层加载
- directory recursive retrieval
- visualized retrieval trajectory

### memsearch

- 官方仓库：<https://github.com/zilliztech/memsearch>
- 官方文档：<https://zilliztech.github.io/memsearch/>

本轮主要使用内容：

- Markdown-first / source of truth
- Milvus shadow index
- dense + BM25 + RRF
- search -> expand -> transcript
- Claude Code / OpenClaw / OpenCode / Codex CLI 插件形态

### memU

- 官方仓库：<https://github.com/NevaMind-AI/memU>
- 官方站点：<https://memu.pro/>

本轮主要使用内容：

- 24/7 proactive memory
- memory as file system
- categories / items / resources / cross-references
- proactive memory lifecycle
- smaller context / lower token pressure

### Acontext

- 官方仓库：<https://github.com/memodb-io/Acontext>
- 官方文档：<https://docs.acontext.io/>
- 官方站点：<https://acontext.io/>

本轮主要使用内容：

- skill memory layer
- task complete/failed -> distillation -> skill agent -> update skills
- no embeddings, no API lock-in
- progressive disclosure via tools

### Voyager

- 原始论文：<https://arxiv.org/abs/2305.16291>

本轮主要使用内容：

- executable code skill library
- 长时程程序性记忆与技能复用

### Memoria

- 官方仓库：<https://github.com/matrixorigin/Memoria>
- 官方站点：<https://thememoria.ai/>

本轮主要使用内容：

- Git for AI Agent Memory
- snapshot / branch / merge / rollback
- Copy-on-Write
- contradiction detection / quarantine
- audit trail / provenance chain

### XiaoClaw

- 官方站点：<https://xiaoclaw.com/>
- 安装与产品页：<https://www.xiaoclaw.xyz/>

本轮主要使用内容：

- 仅用于判断其更像 OpenClaw 的安装封装/产品壳层，而非独立 memory architecture

---

## Vector/Graph-like Agent Memory

### ContextLoom

- 官方仓库：<https://github.com/danielckv/ContextLoom>

本轮主要使用内容：

- shared brain for multi-agent systems
- decouple memory from compute
- Redis-first context state
- cold-start hydration from DB
- communication cycle / cycle hash

### eion

- 官方仓库：<https://github.com/eiondb/eion>
- 官方站点：<https://www.eiondb.com/>

本轮主要使用内容：

- shared memory storage for multi-agent systems
- unified knowledge graph
- PostgreSQL + pgvector + Neo4j
- sequential / concurrent / guest access

### honcho

- 官方仓库：<https://github.com/plastic-labs/honcho>
- 官方文档：<https://docs.honcho.dev/>
- 官方应用：<https://app.honcho.dev/>

本轮主要使用内容：

- memory library for stateful agents
- entities / peers / sessions / representations
- continual learning over changing entities

### mem0

- 官方文档：<https://docs.mem0.ai/introduction>
- 官方仓库：<https://github.com/mem0ai/mem0>
- 原始论文：<https://arxiv.org/abs/2504.19413>

本轮主要使用内容：

- universal, self-improving memory layer
- open source / platform / integrations
- extract / consolidate / retrieve 记忆工作流

### mem9

- 官方仓库：<https://github.com/mem9-ai/mem9>
- OpenClaw 入口页：<https://mem9.ai/openclaw-memory>

本轮主要使用内容：

- persistent memory for AI agents
- stateless plugins + central memory server
- TiDB hybrid vector + keyword search
- shared memory pool across sessions and machines

---

## 交叉参照来源

这些来源不单独承担两大类的核心结论，但帮助校准“程序性记忆”“治理层”“northbound memory plane”等概念。

- CoALA：<https://arxiv.org/abs/2309.02427>
- MemGPT / Letta：<https://arxiv.org/abs/2310.08560> / <https://docs.letta.com/>
- LongMemEval：<https://arxiv.org/abs/2410.10813>
- LoCoMo：<https://arxiv.org/abs/2402.17753> / <https://snap-research.github.io/locomo/>
- TiMem：<https://arxiv.org/abs/2601.02845>
- LiCoMemory：<https://arxiv.org/abs/2511.01448>
- MIRIX：<https://arxiv.org/abs/2507.07957> / <https://docs.mirix.io/>
- EverMemOS：<https://arxiv.org/abs/2601.02163>

---

## 使用说明

- 如果后续继续扩写本专题，优先补这两类缺的内容：
  - filesystem-like 路线的更细 benchmark 与治理案例
  - vector/graph-like 路线的更细 permission / provenance / temporal reasoning 证据
- 若要把 `xiaoclaw` 升级进主线，必须先拿到清晰的官方技术文档或仓库实现，而不是产品页或社区文章。
