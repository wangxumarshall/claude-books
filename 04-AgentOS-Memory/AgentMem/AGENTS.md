
## 第1章：深度研究并洞察如下产业界 agent memory system，撰写《agent memory system洞察》研究报告，要求进行技术方案的深度对比，可以参考以下四个层次的模型（C.A.P.E 框架）：

	1. 架构与底层范式层 (Architecture & Paradigm)
		- 技术分类 (Tech Taxonomy)：是基于 RAG 的外挂检索、基于 OS 的内存页置换，还是修改 Transformer 注意力机制的模型原生记忆？
		- 存储范式 (Storage Paradigm)：扁平向量（Flat Vector）、会话时序（Time-Series）、图数据库（GraphDB）、还是文件目录树（File System）？
		- 系统定位 (System Positioning)：是作为中间件插件、独立 Memory-as-a-Service 服务，还是直接内置于大模型底座？
		- XXX
		
	2. 认知与演进能力层 (Cognition & Evolution)
		- 自我进化 (Self-Evolution)：记忆是“死”的还是“活”的？系统是否具备后台反思（Reflection）、记忆融合（Fusion）、以及主动淘汰脏数据（Forgetting）的机制？
		- 结构化与推理能力 (Structural Reasoning)：能否处理复杂实体关系（如 A 隶属于 B，B 昨天被 C 修改）？
		- XXX
		
	3. 工程与生产力层 (Production & Engineering)
		- Token 节省效能 (Token Efficiency)：通过精准的上下文压缩和路由，能在多大程度上降低基础模型的推理成本（API 费用）？
		- 可观测性与可读性 (Observability & Readability)：当 Agent 出现幻觉或行为异常时，人类工程师能否直观地打开面板，查看 Agent “当时脑子里在想什么”（Traceability）？记忆数据对人类是否可读可写？
		- XXX

	4. 业务与生态层 (Business & Ecosystem)
		- 适用场景 (Use Cases)：适合 C 端闲聊陪伴、B 端复杂系统运维，还是多 Agent 仿真？
		- XXX
	5. 主要局限与短板 (Limitations)：
		- 部署成本、延迟瓶颈、生态锁死风险。
		- XXX
	
	6. Agent Memory System 的演进方向趋势
		- 如静态 -> 动态
		- 被动 -> 主动
		- 单体 -> 集体意识总线
		- XXX

### OpenViking（volcengine/OpenViking） + VikingBot
OpenViking is an open-source context database designed specifically for AI Agents(such as openclaw). OpenViking unifies the management of context (memory, resources, and skills) that Agents need through a file system paradigm, enabling hierarchical context delivery and self-evolving.
**问题背景**：传统 Agent 记忆分散（记忆在代码、资源在向量库、技能散落），检索黑箱、上下文不可分层、无法自我迭代，导致 token 成本高、调试难、长期记忆弱。

**技术方案**：采用**虚拟文件系统范式（viking:// 协议）**统一管理记忆、资源、技能。层次结构：
- `viking://user/memories/`、`agent/memories/`、`resources/` 等。
- 每项支持 **L0（摘要 ~100 tokens）→ L1（概览 ~2k tokens）→ L2（完整内容）** 分层加载。
- 检索：意图分析 + 向量预滤 + 目录递归探索 + 可视化轨迹。
- Session 管理：自动压缩对话、工具调用，异步提取长期记忆并更新 User/Agent 目录，实现**自进化循环**。
- VikingBot 是其上层 Agent 框架，提供 7 个专用工具（memory_commit 等）。

**优劣势**：
- **优势**：统一管理、可观测、可分层节省 token（基准显示 OpenClaw + OpenViking 节省 83-91% token，完成率提升 43-49%）；自我迭代让 Agent “越用越聪明”。
- **劣势**：依赖 VLM/Embedding 模型；AGPL-3.0 许可对商用有一定限制；早期项目需编译环境。

**演进趋势**：从 RAG 平面存储 → 层次化上下文工程；未来向 Rust 重写（RAGFS）、本地模型（vLLM/Ollama）演进，已集成 OpenClaw 等框架。
https://github.com/volcengine/OpenViking
https://openviking.ai/blog


### memsearch（zilliztech/memsearch）
**问题背景**：编码 Agent（Claude Code、OpenClaw 等）跨会话遗忘，记忆不可读、不可编辑、跨平台不共享，传统 RAG 缺乏渐进式检索和去重。

**技术方案**：**Markdown-first**（源头真相），每日日志 `memory/YYYY-MM-DD.md` + Milvus 向量影子索引。插件（Claude/OpenClaw 等）自动捕获并追加 haiku 摘要。检索采用**混合搜索（dense + BM25 + RRF）+ 3 层渐进披露**（search → expand → transcript）。支持 CLI/Python API、实时 watch、LLM 压缩。

**优劣势**：
- **优势**：人类可读、可 git 版本控制、跨 Agent 零配置共享、去重高效、token 节省显著。
- **劣势**：依赖 Milvus（即使 Lite 模式）；首次需下载嵌入模型。

**演进趋势**：从 OpenClaw 提取的记忆子系统 → 独立库，支持更多 IDE 插件、混合检索升级，体现“人类可读 + 向量加速”的混合趋势。

### Hermes Agent（nousresearch/hermes-agent）
**问题背景**：传统 Agent 缺乏跨会话学习、技能自动生成、用户画像建模，导致每次会话“从零开始”。

**技术方案**：**Markdown 持久记忆层**（MEMORY.md、USER.md、skills/ 目录）+ 闭环学习循环。Agent 自主在复杂任务后创建/迭代技能；FTS5 + LLM 摘要实现跨会话搜索；Honcho 建模用户行为。支持 MCP、Telegram/CLI 多表面，内置压缩工具。

**优劣势**：
- **优势**：真正“自我成长”Agent（技能自进化 + 用户画像）；低成本部署（$5 VPS）；可迁移 OpenClaw 记忆。
- **劣势**：Windows 支持需 WSL；大上下文需手动压缩。

**演进趋势**：向 RL 训练（Atropos）、批量轨迹生成演进，强调“Agent 即研究员”的研究级记忆系统。

### Letta(memGPT)
Letta is the platform for building stateful agents: AI with advanced memory that can learn and self-improve over time.
https://github.com/letta-ai/letta
https://docs.letta.com/letta-code/

### mem0：
Universal memory layer for AI Agents
**问题背景**：LLM 应用缺乏持久个性化记忆，导致重复解释偏好、高 token 消耗。

**技术方案**：**多级记忆（User/Session/Agent）** + 向量语义检索 + 自适应更新。Python/JS SDK 一行集成，支持插件（Claude/Cursor）、CLI、LangGraph 等框架。使用向量库（Valkey 等）存储，支持托管/自托管。

**优劣势**：
- **优势**：基准领先（+26% 准确率、90% 少 token）；通用层，易集成；自改进。
- **劣势**：依赖外部 LLM/向量库；自托管需运维。

**演进趋势**：v1.0 大升级（API 现代化 + 新向量支持），从单一 RAG → 通用记忆层，未来向企业分析/安全扩展。
https://github.com/mem0ai/mem0
https://mem0.ai/

### memos
AI memory OS for LLM and Agent systems(moltbot,clawdbot,openclaw), enabling persistent Skill memory for cross-task skill reuse and evolution.
**问题背景**：技能无法跨任务复用、记忆缺乏统一调度和反馈。

**技术方案**：**Memory OS** 概念，将记忆视为一等资源。统一 API + 图结构存储 + MemScheduler（Redis 异步）+ 多 Cube 知识库 + 反馈修正 + 多模态/工具记忆。支持本地 SQLite / 云部署。

**优劣势**：
- **优势**：技能持久进化、43%+ 准确率提升、72% token 节省、多代理隔离共享。
- **劣势**：需 Neo4j/Qdrant 等外部组件。

**演进趋势**：v2.0 重大升级（多模态 + 调度器 + Helm），向 MAG（Memory-Augmented Generation）完整 OS 演进。

https://github.com/MemTensor/MemOS
https://memos.openmem.net/


### EverOS/EverMemOS
Build, evaluate, and integrate long-term memory for self-evolving agents.
https://github.com/EverMind-AI/EverOS
https://arxiv.org/pdf/2601.02163
https://mp.weixin.qq.com/s/SrARqbLyNGBkwz059e1TcA
HyperMem 超图：给结构化记忆加关联（比如「足球→运动→周末」）
EverCore 记忆 OS：自动删无用记忆、高频记忆优先读取
基准测试：用标准答案对比，算记忆准确率
@article{hu2026evermemos,
  title   = {EverMemOS: A Self-Organizing Memory Operating System for Structured Long-Horizon Reasoning},
  author  = {Chuanrui Hu and Xingze Gao and Zuyi Zhou and Dannong Xu and Yi Bai and Xintong Li and Hui Zhang and Tong Li and Chong Zhang and Lidong Bing and Yafeng Deng},
  journal = {arXiv preprint arXiv:2601.02163},
  year    = {2026}
}

@article{yue2026hypermem,
  title   = {HyperMem: Hypergraph Memory for Long-Term Conversations},
  author  = {Juwei Yue and Chuanrui Hu and Jiawei Sheng and Zuyi Zhou and Wenyuan Zhang and Tingwen Liu and Li Guo and Yafeng Deng},
  journal = {arXiv preprint arXiv:2604.08256},
  year    = {2026}
}

@article{hu2026evaluating,
  title   = {Evaluating Long-Horizon Memory for Multi-Party Collaborative Dialogues},
  author  = {Chuanrui Hu and Tong Li and Xingze Gao and Hongda Chen and Yi Bai and Dannong Xu and Tianwei Lin and Xiaohong Li and Yunyun Han and Jian Pei and Yafeng Deng},
  journal = {arXiv preprint arXiv:2602.01313},
  year    = {2026}
}

### claude-mem
A Claude Code plugin that automatically captures everything Claude does during your coding sessions, compresses it with AI (using Claude's agent-sdk), and injects relevant context back into future sessions.
https://github.com/thedotmack/claude-mem
https://claude-mem.ai/


### mem9
Unlimited memory for OpenClaw
https://github.com/mem9-ai/mem9

### lossless-claw
Lossless Claw — LCM (Lossless Context Management) plugin for OpenClaw
https://github.com/Martian-Engineering/lossless-claw

### memU
Memory for 24/7 proactive agents like openclaw (moltbot, clawdbot).
- 为openclaw/moltbot等24/7 proactive agents设计
- 结合多个社区扩展：memu-cowork、memu-sillytavern-extension
- **技术栈**: Python + OpenClaw集成
- **演进**: 已有3代社区实现（memov.ai、memovyn等）
**问题背景**：24/7 主动 Agent 需要低成本长期上下文，但传统方案 token 爆炸、无法主动捕捉意图。

**技术方案**：**文件系统式分层记忆**（Category/Item/Resource + 符号链接），支持 RAG + LLM 双模式检索。主动式：自动分类、模式检测、上下文预测。集成 openclaw 等，支持 PostgreSQL/pgvector，多模态输入。

**优劣势**：
- **优势**：token 成本降至 1/10；92%+ Locomo 准确率；真正 24/7 主动。
- **劣势**：文档中未明确提及局限，但依赖 LLM/嵌入模型。

**演进趋势**：从 openclaw 生态衍生，v1.x 迭代强调多代理协作、多模态、云托管（memu.so）。

https://github.com/NevaMind-AI/memU
https://memu.pro/

### Ori-Mnemos
Local-first persistent agentic memory powered by Recursive Memory Harness (RMH). Open source must win.
https://github.com/aayoawoyemi/Ori-Mnemos
https://orimnemos.com/

### langmen
https://github.com/langchain-ai/langmem
https://langchain-ai.github.io/langmem/

### honcho
Memory library for building stateful agents
https://github.com/plastic-labs/honcho
https://docs.honcho.dev/

### ContextLoom
ContextLoom is the shared "brain" for multi-agent systems. It weaves together memory threads from frameworks like DSPy and CrewAI into a unified, persistent context, powered by Redis and hydrated from your existing databases.
https://github.com/danielckv/ContextLoom
https://danielckv.dev/

### eion
Shared Memory Storage for Multi-Agent Systems
https://github.com/eiondb/eion
https://www.eiondb.com/

### mindforge
MindForge is a Python library designed to provide sophisticated memory management capabilities for AI agents and models. It combines vector-based similarity search, concept graphs, and multi-level memory structures (short-term, long-term, user-specific, session-specific, and agent-specific) to enable more context-aware and adaptive AI responses.
https://github.com/aiopsforce/mindforge

### minecontext
MineContext is your proactive context-aware AI partner（Context-Engineering+ChatGPT Pulse）
https://github.com/volcengine/MineContext

### Memorizing Transformers
https://arxiv.org/abs/2203.08913

### memoryllm
https://github.com/wangyu-ustc/MemoryLLM
https://arxiv.org/abs/2402.04624

### acontext
Agent Skills as a Memory Layer
https://github.com/memodb-io/Acontext

### ultraContext
Open Source Context infrastructure for AI agents. Auto-capture and share your agents' context everywhere.
https://github.com/ultracontext/ultracontext
https://ultracontext.com/

### MemaryAI
This is an open-source project that provides an efficient memory layer for autonomous AI agents, helping AI agents better manage and utilize information by simulating how human memory works
https://github.com/MemaryAI/MemaryAI


### MindOS - 人机协作心智系统
  - 全局同步心智
  - 透明可控的Agent行为
  - 共生演进逻辑
https://github.com/GeminiLight/MindOS  

### 知识图谱
查看完整知识图表系统列表: [160+ Graph Memory Systems](https://github.com/search?q=knowledge+graph+memory+system&sort=stars)

### 向量数据库
向量数据库详细对比: [67+ Vector Database Implementations](https://github.com/search?q=vector+database+memory+embedding&sort=stars)


## 第2章： 网络上（google scholar、arXiv）全文检索“Agent Memory+ (Episodic / Semantic / Working)+ (Formation / Retrieval / Evolution)+ (Vector DB / Graph Memory / RAG)+ (Reflection / Self-evolving / Continual Learning)+ 
(Multi-agent / Shared Memory)+ (Evaluation / MemBench / LongMemEval)”，并研究检索到的所有论文，按照业务场景、问题挑战、技术方案或创新技术或解决方案、效果、优劣势、演进趋势

### 记忆：kvcache复用（感知记忆的更新，上文感知语义管理） ：降低记忆长度（信息熵）、承载更有价值的记忆

### [Awesome-Agent-Memory](https://github.com/TeleAI-UAGI/Awesome-Agent-Memory)



## 第3章：基于《agent memory system洞察》研究报告，借鉴如上agent memory system研究，参考如下方向，面向构建通用agent的memory系统，撰写技术解决方案，要求从业务场景、问题挑战、技术方案或创新技术或解决方案、差异化竞争优势、测评标准benchmark、预期效果维度：

### entire.io
非纯 GitHub 记忆仓库，而是 AI 编码/Agent 平台。其 Dispatch 更新重点优化**大仓库记忆、检查点、Agent 更新**，体现商业产品中“内存改进 + 远程仓库支持”的实践应用。非独立开源记忆层，但验证了分层记忆在实际编码 Agent 中的价值。

### User as Code（用代码表示用户记忆）
GitHub 未发现独立仓库，此为**前沿概念**：将用户信息/偏好编码为**可执行代码**（如 Python 函数、脚本、规则引擎），而非文本/结构化数据。Agent 可直接“执行”用户记忆，实现动态行为适配（如自动调用特定工具、应用自定义逻辑）。优势在于**可编程性、动态更新**；挑战是安全性、解释性、可维护性。未来可能与技能自进化结合，成为 Agent 记忆的“可执行层”。

### xiaoclaw-memory
Zero-cost layered memory system for 24/7 AI Agents. Inspired by memU, powered by pure Markdown.
https://github.com/huafenchi/xiaoclaw-memory

### MemBrain 1.0（Feeling AI）
MemBrain 1.0 is a dynamic memory system that breaks linear memory workflows by enabling sub-agents to coordinate autonomously, letting LLMs directly participate in memory reasoning rather than having graph algorithms compute results and then feed them to the model.
**问题背景**：传统记忆系统采用线性流程（提取→存储→检索→注入），图算法与大语言模型之间存在范式差异——图算法在算的时候，LLM只能站在旁边看着，导致记忆处理与模型推理脱节。

**技术方案**：**LLM亲和记忆架构** + 子Agent自主协调 + 时间戳标准化。
- 打破线性流程：记忆提取、存储、检索由子Agent自主协调，非固定流水线
- LLM直接参与记忆推理：让模型在记忆空间中直接推理，而非图算法算完再喂给LLM
- 严控时间戳：所有记忆附加精确时间信息，支持时序推理
- "中庸"遗忘：重要的事保留，细节模糊，旧经历融入新反应——模拟人类的"活人感"

**优劣势**：
- **优势**：LoCoMo 93.25%（SOTA）、LongMemEval 84.6%、PersonaMem-v2 51.50%、KnowMeBench Level III 提升300%+；"活人感"记忆比规则式更自然。
- **劣势**：子Agent协调增加系统复杂度；LLM直接参与记忆推理增加token成本；数据均为自报，无独立验证。

**演进趋势**：从"图算法驱动"→"LLM亲和记忆"，代表记忆系统与模型推理范式融合的趋势。
https://feeling.ai/membrain

### Memoria（矩阵起源，GTC 2026 发布）
Memoria is "Git for Memory" — a version-controlled memory system for AI agents, providing Copy-on-Write snapshots, branching, merging, and rollback capabilities.
**问题背景**：Agent记忆一旦被投毒或损坏，无法回退到安全状态；记忆变更不可追溯、不可回滚；多人协作时记忆冲突无法解决。

**技术方案**：**Git式版本控制**应用于Agent记忆。
- Copy-on-Write：每次记忆变更创建新版本，不覆盖旧版本
- 快照/分支/合并：支持记忆的分支实验和合并
- 回滚：发现记忆被投毒时，可回退到已知安全版本
- 明确批评Markdown的"静态、单向、无结构、无法回滚"四大局限

**优劣势**：
- **优势**：版本回滚是防御记忆投毒的实用手段；支持多人协作记忆管理；与Git生态天然兼容。
- **劣势**：Copy-on-Write增加存储开销；分支合并的冲突解决策略待完善；GTC 2026刚发布，工程成熟度待验证。

**演进趋势**：从"不可变记忆"→"版本控制记忆"，为Agent记忆引入软件工程最佳实践。版本回滚作为投毒防御手段，与CortexMem的防火墙+溯源+沙箱形成互补。
https://github.com/matrixorigin/Memoria

### TiMem（中科院自动化所）
TiMem: Temporal Hierarchical Memory for Long-Term Conversations, inspired by Complementary Learning Systems (CLS) theory from cognitive neuroscience.
**问题背景**：现有记忆系统缺乏时间层次结构，无法区分事实、会话、日、周、画像等不同时间尺度的记忆；检索时无法根据问题复杂度自适应调整检索深度。

**技术方案**：**5层时序记忆树（TMT）** + 复杂度感知召回，源自互补学习系统理论（CLS）。
- L1事实层：原始事实片段
- L2会话层：会话摘要
- L3日层：日模式归纳
- L4周层：周趋势
- L5画像层：稳定人格画像
- 复杂度感知召回：简单问题只检索L1/L2，复杂问题才往L3/L4/L5找，无需LLM决策
- CLS系统巩固：模拟海马体→新皮层转移，L1事实→L3模式的巩固过程
- Token节省52.2%（LoCoMo实测），无需微调，纯指令引导

**优劣势**：
- **优势**：LoCoMo 75.30%、LongMemEval 76.88%（论文自报）；CLS理论提供比Ebbinghaus遗忘曲线更完整的认知科学框架；复杂度感知召回无需LLM决策即可分层路由；部署成本低。
- **劣势**：5层归纳仍需LLM调用；时序树的层级划分可能不适用于所有场景；论文预印本未经peer review。

**演进趋势**：从"Ebbinghaus遗忘曲线"→"CLS互补学习系统理论"，代表认知科学驱动的记忆分层趋势。复杂度感知召回为"零成本路由"提供了新思路。
arXiv:2601.02845

### OmniMem / Omni-SimpleMem（UNC-Chapel Hill）
OmniMem is a multimodal lifelong memory system discovered through AI autonomous research. Omni-SimpleMem uses a 23-stage autonomous research pipeline where AI discovers optimal memory architectures through 50 experiments.
**问题背景**：人类设计的记忆架构可能存在盲区；多模态Agent需要跨模态的统一记忆；现有系统缺乏终身学习能力。

**技术方案**：**AI自主研究管道** + 多模态原子单元（MAU）。
- 23阶段自主研究管道：AI在50次实验中自主发现最优架构
- 关键发现：Bug修复贡献+175% > 超参数调优——AI发现了人类研究者忽略的架构Bug
- 多模态原子单元（MAU）：统一文本、图像、音频的记忆表示
- 热/冷存储分层 + 渐进式检索
- LoCoMo F1从0.117→0.598（+411%）

**优劣势**：
- **优势**：证明AI自主优化记忆架构可行；多模态终身记忆；Bug修复比超参数调优更有效。
- **劣势**：自主研究管道计算成本高；多模态MAU的表示能力受限；F1=0.598仍低于SOTA。

**演进趋势**：从"人工设计记忆架构"→"AI自主优化"，引入全新方法论维度。多模态终身记忆是Agent记忆的必要扩展方向。
arXiv:2604.01007

### DeepSeek Engram
DeepSeek Engram introduces conditional memory modules into Mixture-of-Experts (MoE) architecture, enabling O(1) deterministic knowledge lookup.
**问题背景**：MoE模型的知识存储分散在专家参数中，检索需要全量计算；知识更新需要重新训练；无法实现确定性的知识查找。

**技术方案**：**条件记忆模块（Engram）** 嵌入MoE架构。
- Engram作为与MoE并行的条件记忆分支
- O(1)确定性知识查找：通过条件路由直接定位知识
- 20-25%稀疏参数预算分配给Engram时验证集loss最低
- MoE+Engram呈现U形scaling law：随参数增长先降后升

**优劣势**：
- **优势**：确定性知识查找（非概率检索）；与MoE架构无缝集成；知识更新无需重训。
- **劣势**：Engram容量仍有限；仅适用于知识记忆，不适用于情景/程序性记忆；需要模型架构修改。

**演进趋势**：从"参数微调式模型原生记忆"（MemoryLLM）→"架构级记忆原语"（Engram/STEM），重新定义模型原生记忆。Engram证明模型原生记忆可从感知层扩展到知识层。

### ICLR STEM
STEM (Scalable Token-efficient Memory) replaces FFN up-projection with a token-indexed embedding lookup table, enabling plug-and-play knowledge editing.
**问题背景**：LLM的知识编码在FFN参数中，修改特定知识（如"西班牙首都是马德里"→"巴塞罗那"）需要精确编辑FFN权重，但权重交织导致编辑困难。

**技术方案**：**查表式记忆**。
- 将FFN的up-projection替换为token索引embedding表
- 即插即用的知识编辑：互换Spain/Germany的向量即可改变模型输出
- 无需重训或微调即可更新特定知识

**优劣势**：
- **优势**：即插即用知识编辑；无需重训；精确控制知识更新范围。
- **劣势**：仅适用于事实性知识；embedding表的容量限制；ICLR 2026论文，工程成熟度待验证。

**演进趋势**：与Engram共同代表"架构级记忆原语"方向，将模型原生记忆从"参数微调"推进到"查表式知识管理"。

### LiCoMemory（HKUST+华为+WeBank）
LiCoMemory introduces CogniGraph — a lightweight hierarchical cognitive graph for long-term conversation memory with temporal and hierarchy-aware search.
**问题背景**：知识图谱构建成本高、更新延迟大；扁平向量检索缺乏结构化推理能力；需要在图谱表达力和轻量部署之间取得平衡。

**技术方案**：**CogniGraph轻量认知图谱** + 时序层次感知搜索 + 集成重排序。
- CogniGraph：轻量层次图，实体和关系作为语义索引层
- 时序+层次感知搜索：结合时间衰减和层级权重的检索策略
- 集成重排序：多路检索结果融合排序

**优劣势**：
- **优势**：在LoCoMo/LongMemEval上超越baselines；显著降低更新延迟；轻量部署。
- **劣势**：CogniGraph的表达力弱于完整知识图谱/超图；论文预印本未经peer review。

**演进趋势**：从"重型知识图谱"→"轻量认知图谱"，在表达力和部署成本之间寻找平衡点。
arXiv:2511.01448

### MIRIX
MIRIX is a multi-intelligent memory system with 6 memory types and Active Retrieval for multi-agent collaboration.
**问题背景**：单一记忆类型无法覆盖Agent的多样化需求；被动检索导致Agent重复查询相同信息；多Agent协作缺乏统一的记忆协调机制。

**技术方案**：**6类记忆** + Active Retrieval + 多智能体协同。
- 6种记忆类型：核心记忆、情景记忆、语义记忆、程序性记忆、资源记忆、知识库
- Active Retrieval：Agent不被动等待查询，主动关联所有记忆类型
- 用户输入自动触发跨类型检索
- 减少87%的API调用

**优劣势**：
- **优势**：6类记忆覆盖更全面；Active Retrieval减少重复查询；多智能体协同记忆管理。
- **劣势**：6类记忆的分类和维护成本高；Active Retrieval可能引入噪声；工程成熟度待验证。

**演进趋势**：从"被动检索"→"Active Retrieval"，从"3类记忆"→"6类记忆精细化"，代表记忆类型细分和主动化趋势。

### MemoryOS（BUPT+腾讯）
MemoryOS is a three-layer memory system with heat-driven updates and semantic-aware retrieval for long-term conversation.
**问题背景**：现有记忆系统缺乏热度驱动的更新机制；记忆检索缺乏语义感知；跨会话记忆一致性难以保证。

**技术方案**：**三层记忆** + 热度驱动更新 + 语义感知检索。
- 三层记忆架构：短期→中期→长期
- 热度驱动更新：高频访问记忆自动晋升，低频记忆自动降级
- 语义感知检索：结合语义相似度和时间衰减的检索策略
- LoCoMo F1 +49.11%（相对baseline提升）

**优劣势**：
- **优势**：热度驱动更新机制直观有效；语义感知检索提升准确率；BUPT+腾讯背书。
- **劣势**：三层架构表达力有限；热度驱动的"热门偏见"可能忽略重要但低频的记忆；论文自报数据。

**演进趋势**：热度驱动更新与TiMem的CLS分层、EverMemOS的EverCore调度共同代表"记忆动力学"方向的探索。
arXiv:2506.06326
