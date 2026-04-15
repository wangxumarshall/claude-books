# Filesystem-like 与 Vector/Graph-like Agent Memory 深度研究报告

> 目录定位：`AgentOS-Memory/fs-vector-graph/`
>
> 研究目标：围绕两类 Agent Memory 技术路线做专题研究：
> 1. `filesystem like agent memory`
> 2. `vector/graph like agent memory`
>
> 研究要求：不仅比较“怎么做”，还要回答“为什么会出现”“解决了什么真实问题”“效果和边界在哪里”“Cortex-Mem 可以借鉴什么”。

---

## 0. 研究方法与分类边界

### 0.1 为什么单独研究这两类

在当前 Agent Memory 生态里，很多项目都被粗糙地放进“长期记忆”一个大桶里，但它们解决的问题层级并不一样。

本报告采用一个更贴近工程实现的切分：

- **Filesystem-like agent memory**
  把记忆首先看作“文件、目录、Markdown、技能文件、版本化对象”，强调人类可读、可编辑、可迁移、可审计。
- **Vector/Graph-like agent memory**
  把记忆首先看作“北向可调用的语义存储/关系存储/共享状态平面”，强调语义召回、图关系、多 Agent 共享、服务化。

这个切分不是说两类系统互斥，而是为了回答一个更具体的问题：

> 当 Agent Memory 进入生产后，系统到底更像“人类可读的知识工作区”，还是更像“供多个 Agent 复用的共享语义基础设施”？

### 0.2 本报告采用的判定规则

如果一个系统同时具备文件层和向量层，本报告按**主导接口**归类：

- 如果它强调“Markdown/文件树/技能文件/目录导航/版本控制”是主体验面，则归为 **filesystem-like**。
- 如果它强调“memory API / vector retrieval / graph reasoning / shared context bus / managed service”是主体验面，则归为 **vector/graph-like**。

因此：

- `memsearch` 虽然内部有 Milvus 向量索引，但因为它明确把 Markdown 作为 source of truth，所以归 filesystem-like。
- `mem9` 虽然服务于 coding agent，但因为它把共享 memory pool、TiDB 混合检索、stateless plugin 作为主导接口，所以归 vector/graph-like。

### 0.3 证据等级

| 等级 | 含义 |
|------|------|
| **A** | 官方文档、官方仓库、论文/技术说明能够相互印证 |
| **B** | 有官方仓库或文档，但很多效果仍是项目自报 |
| **C** | 有官方入口，但技术实现、产品包装、评测口径不完全稳定 |
| **X** | 本轮未找到足够稳定的一手技术材料，只能作弱证据处理 |

### 0.4 核心结论先行

本轮研究后，可以先给出六个高层判断：

1. **Filesystem-like memory 的根本价值不是“替代向量检索”，而是把记忆重新拉回可读、可控、可迁移的工程对象。**
2. **Vector/graph-like memory 的根本价值不是“存更多 embedding”，而是为多 Agent 和复杂检索提供共享语义平面。**
3. **两类系统分别擅长不同问题：前者擅长可观测性与技能沉淀，后者擅长共享、规模化与关系建模。**
4. **两类系统都在逐步走向混合：filesystem-like 系统开始引入 shadow index、hybrid retrieval；vector/graph-like 系统开始补充 provenance、治理和可视化。**
5. **Cortex-Mem 不应在两类路线中二选一，而应做“文件表面 + 语义索引 + 图关系 + 版本治理”的混合架构。**
6. **旧稿里最值得保留的，不是那些激进分数，而是更严格的批判性判断。**
   例如 OpenViking 的 benchmark 提升、memU 的 `92%+ LoCoMo`、MemBrain 的 `93.25% LoCoMo` 这类数字都不能直接拿来支撑主结论；真正应该吸收的是对证据等级、治理能力、遗忘缺位和评测口径的警惕。

---

## 1. Filesystem-like Agent Memory

### 1.1 问题背景：为什么这类系统会出现

这类系统的出现，不是因为大家突然喜欢 Markdown，而是因为传统 memory/RAG 方案在 Agent 场景里暴露了四类真实问题。

#### 案例一：Coding Agent 跨会话“失忆”，而且记忆不可读

`memsearch` 的官方定位非常直接：它是面向 AI coding agents 的跨平台语义记忆系统。它在 Claude Code、OpenClaw、OpenCode、Codex CLI 上统一写入日级 Markdown 记忆文件，再通过 Milvus 做 shadow index。其官方示例问题非常工程化，例如“我们之前讨论过 Redis 的 TTL 方案是什么”“之前定过 batch size limit 是多少”。这说明它要解决的不是泛化聊天，而是**coding session 的跨会话延续性**。

这里的真实痛点不是“检索不到文本”，而是：

- 过去的讨论没有稳定落盘；
- 落盘后人类也看不懂；
- 不同 Agent 各写各的本地状态，互不相通；
- 一旦 memory 出错，工程师很难修。

#### 案例二：24/7 proactive agent 必须持续在线，但 token 成本不能线性爆炸

`memU` 的官方定位是面向 24/7 proactive agents 的 memory framework。它明确强调：

- 长时间运行；
- 持续捕捉用户意图；
- 即便没有显式命令，也能基于长期记忆主动行动；
- 通过更小上下文把成本压到可接受范围。

这类产品的真实案例不是单轮问答，而是：

- 持续监控与提醒；
- 长期个人助理；
- 始终在线的 work assistant；
- 一边观察、一边积累偏好、一边主动触发动作。

在这种场景里，如果记忆只是扁平向量块，系统很快会遇到两个问题：

- 无法把“长期结构”表达清楚；
- 记忆虽然存在，但不适合主动浏览和逐层展开。

#### 案例三：Agent 的上下文散落在代码、资源、技能、工具结果里，RAG 很黑箱

`OpenViking` 在 README 里把这一痛点说得很透：

- memory 在代码里；
- resources 在向量库里；
- skills 散落在别处；
- 传统 RAG 是扁平存储；
- 检索链条不透明；
- 出问题时工程师看不到根因。

这其实是大量复杂 Agent 的共同症状：系统在“能调通”之后，会迅速进入“调不动”的状态。文件系统式记忆之所以重新出现，本质上是在用更熟悉的工程抽象对抗黑箱检索。

#### 案例四：真正可复用的长期能力，常常不是一句总结，而是一段可执行技能

`Acontext` 和 `Voyager` 都直指同一个问题：

- Agent 完成一次任务后，真正高价值的长期资产不是原始对话本身；
- 而是“什么做法有效、什么做法失败、下次应该怎么做”。

`Acontext` 选择把这种资产沉淀为 skill files；
`Voyager` 则更进一步，把技能沉淀为 executable code skill library。

这类系统的背景不是“用户画像”，而是**经验能不能变成可执行资产**。

#### 案例五：长期记忆不仅要能写，还要能安全地修改、回滚和审计

`Memoria` 提出的不是普通的 memory store，而是“Git for AI agent memory”。它之所以有吸引力，是因为长期记忆一旦进入生产系统，问题就从“存不存得住”升级为：

- 写错了怎么办；
- 被脏信息污染怎么办；
- 想实验一套新记忆策略怎么办；
- 多个记忆分支如何合并；
- 哪次变更导致了坏行为。

这已经不是纯检索问题，而是**记忆治理问题**。

### 1.2 这类系统的共同技术路线

Filesystem-like agent memory 虽然具体实现不同，但在技术上有五个共性。

#### 共性一：把“人类可读文件”视为源头真相

在这类系统里：

- Markdown 不是导出格式，而是主存格式；
- 技能文件不是附属物，而是核心记忆单元；
- 文件树不是 UI 皮肤，而是信息组织方式。

这带来三个后果：

- 便于审计；
- 便于 git/version control；
- 便于跨 Agent、跨模型迁移。

#### 共性二：向量检索经常仍然存在，但只是缓存、影子索引或辅助手段

这类系统并不反向量检索，而是改变了向量检索的地位。

典型形态包括：

- `memsearch`：Markdown 是 source of truth，Milvus 是可重建的 shadow index；
- `OpenViking`：目录定位 + 语义搜索 + 递归获取，而不是纯 top-k；
- `Memoria`：vector + full-text hybrid retrieval，但版本化对象才是核心。

换句话说，vector retrieval 退居为**加速层**，而不是**真相层**。

#### 共性三：渐进式披露比“一次性 top-k 拼上下文”更重要

Filesystem-like memory 天然适合做 progressive disclosure：

- 先看目录；
- 再看概览；
- 再按需拉取细节；
- 或先拿 skill metadata，再按需拿具体 skill file。

这类设计在 coding agent、research agent、proactive agent 上都非常有用，因为它更符合人类与 Agent 协同的实际工作方式。

#### 共性四：程序性记忆是一等公民

这类系统往往更容易把：

- 操作套路；
- 工作流模板；
- 调试经验；
- 工具调用策略；
- 失败后修复策略

沉淀成 skill 或 code artifact，而不只是文字摘要。

#### 共性五：治理与版本化更容易落地

当记忆是文件、目录、版本对象时，很多治理能力更自然：

- diff
- branch
- rollback
- quarantine
- provenance
- 规则化组织

这也是 `Memoria` 之类系统最值得注意的点。

#### 共性六：append-only 原始记录 + 分层摘要，是 filesystem-like 路线里反复出现的合理结构

旧稿里提到的若干社区实现，虽然证据强弱不一，但共同暴露出一个很稳定的设计模式：

- 原始 episode / transcript 不应轻易覆写；
- 面向召回的摘要层可以逐步压缩和重组；
- 人类可读的索引层应当独立于原始记录存在。

这类设计并不等于某个具体项目一定成熟，但它作为架构模式是成立的。Cortex-Mem 的 `L0 Raw Episodes + 上层 consolidation` 就应当吸收这一点，而不是把所有信息直接压成单层 Markdown 或单层向量块。

### 1.3 关键系统深度研究

#### 1.3.1 OpenViking

**定位**

OpenViking 是一个面向 AI Agents 的开源 context database，核心叙事不是“更大的向量库”，而是“用文件系统范式统一 memory、resource、skill”。

**问题背景**

它解决的是复杂 Agent 的 context 工程问题，而不是单纯问答召回问题。官方明确点名的痛点包括：上下文碎片化、长任务上下文激增、扁平 RAG 全局视角不足、检索过程黑箱、记忆无法围绕任务自我迭代。

**技术方案**

- 用文件系统范式统一管理 memory、resource、skill
- 使用层次化上下文交付，典型是 `L0/L1/L2` 逐层加载
- 结合目录定位、语义搜索与递归检索
- 提供可视化 retrieval trajectory
- 自动压缩 session 内容，提取长期记忆，形成自迭代回路

**技术效果**

OpenViking 的强点不是公开 benchmark 数字，而是它把 Agent context management 从“检索黑箱”改成了“有结构、可追踪、可递归探索”的工作流。

同时，官方 README 的确给出了两组 OpenClaw 对比口径：

- 开启 native memory 时，声称相对原始 OpenClaw 有 `43% improvement` 与 `91% reduction in input token cost`
- 关闭 native memory 时，声称有 `49% improvement` 与 `83% reduction in input token cost`

这些数字说明其工程方向值得重视，但它们仍然属于**项目自报结果**，比较对象也主要是 OpenClaw 原始配置或 LanceDB 对照组，不能被当成跨系统总榜证据。

**优势**

- 统一 memory / resource / skill
- 可观测性强
- 适合层次化按需加载
- 对 coding/research/workflow agent 的复杂上下文组织更自然

**劣势**

- 系统复杂度高于纯插件型记忆层
- 学习曲线高于单一向量库方案
- 生态中很多效果仍偏项目自报
- 许可结构比看上去复杂：主项目是 AGPLv3，但部分子组件如 `ov_cli` 与 `examples` 使用 Apache 2.0；商用团队不能把“局部 Apache”误读成“整体 Apache”

**应用场景**

- 复杂 coding agent
- 长时程 research agent
- 需要多类 context 协调的 workflow agent

**对 Cortex-Mem 的借鉴**

- 采用“文件表面 + 层次披露”而不是扁平 top-k
- 将 memory、resource、skill 作为统一上下文对象
- 引入 retrieval trace 作为调试能力，而不是仅输出结果

#### 1.3.2 memsearch

**定位**

memsearch 是面向 AI coding agents 的 Markdown-first memory system。

**问题背景**

它瞄准的是最典型的工程痛点：Claude Code、OpenClaw、OpenCode、Codex CLI 等工具之间，记忆互不共享；会话结束后上下文蒸发；即使记录下来了，人类也很难确认 Agent 究竟记住了什么。

**技术方案**

- Markdown 作为 source of truth
- 日级记忆文件落盘
- Milvus 只作为 shadow index
- dense vector + BM25 + RRF 混合检索
- 3 层 recall：`search -> expand -> transcript`
- 内容 hash 去重
- file watcher 实时同步
- 本地嵌入模型可用，降低云依赖

**技术效果**

memsearch 的效果不是“把一切都语义化”，而是提供一种兼顾：

- 人类可读
- 跨平台共享
- 混合检索
- 渐进式展开

的 memory layer。

**优势**

- 对 coding agent 非常贴合
- 可读可写，适合 git 管理
- 影子索引可重建，不易被底层向量库绑死
- 跨 CLI/插件平台共享体验好

**劣势**

- 主要优化的是 coding/workspace 场景
- 仍依赖额外向量索引组件
- 图关系和复杂多实体推理能力有限

**应用场景**

- Claude Code / Codex CLI / OpenClaw 等 coding agents
- 个人与团队级工程知识沉淀
- 本地优先、低摩擦接入的记忆层

**对 Cortex-Mem 的借鉴**

- “Markdown 是真相，向量索引是缓存”应成为 Cortex-Mem 的基本原则之一
- 采用 progressive recall 而不是直接回填全文
- 将 coding memory 设计成自然可审阅的 artifact

#### 1.3.3 memU

**定位**

memU 的核心不是“会记住对话”，而是“支撑 24/7 proactive agents 的长期、低成本、主动记忆框架”。

**问题背景**

如果 Agent 要持续在线，仅靠当前对话和最近上下文是不够的。系统必须既能持续记录，也能在没有显式命令时推断用户意图并主动行动。

**技术方案**

- 把 memory 建模为文件系统：categories / items / resources / cross-references
- 用层次结构组织 preferences、relationships、knowledge、context
- 把 conversation/document/image 等视为可挂载资源
- 通过后台 bot 或辅助 agent 监控输入输出并持续沉淀记忆
- 强调更小上下文和持续运行

**技术效果**

官方材料强调的两个关键效果是：

- 将 always-on memory 的 token 成本压到更低；
- 让 Agent 从“被动问答”走向“主动理解和行动”。

旧稿中的 `92%+ LoCoMo` 和“token 成本降到 1/10”这类说法，本轮没有获得足够稳定的一手技术链条支撑，因此**不纳入本报告的事实层结论**。对 memU 更合理的评价是：它在产品方向上非常明确，但公开量化效果目前仍应谨慎对待。

**优势**

- 极适合 proactive / always-on agent
- 文件系统模型天然适合组织长期结构
- 对个人助理和连续工作流很贴合

**劣势**

- 需要后台监控或 memory bot，系统形态比普通插件更重
- 主动推断带来误触发和治理成本
- 复杂部署下的数据流与隐私边界更难处理

**应用场景**

- 24/7 assistant
- 持续监控型 agent
- 长期 personal AI companion

**对 Cortex-Mem 的借鉴**

- 引入“在线 Agent + 后台 memory worker”双通道结构
- 将主动记忆与被动检索分开治理
- 用文件树表达长期偏好、关系、待办与上下文资源

#### 1.3.4 Acontext

**定位**

Acontext 把 Agent Memory 重新定义成“skill memory layer”。

**问题背景**

Acontext 的判断很激进：很多所谓 agent memory 越做越复杂、越黑箱、越难调试；如果 skill 已经能代表 agent 所需知识，那么 memory 也可以直接落成 skill files。

**技术方案**

- 自动从 agent run 中提取 learnings
- 在任务完成或失败时触发 distillation
- 由 skill agent 决定更新已有 skill 还是创建新 skill
- 用 `SKILL.md` 定义结构
- 召回不依赖 embedding top-k，而是依赖 `list_skills / get_skill / get_skill_file` 等逐层获取
- 明确强调 plain files、跨框架、无 vendor lock-in、可 ZIP 导出

**技术效果**

Acontext 的重要价值不在 benchmark，而在于它把“经验沉淀”这件事从向量块抽象回了技能资产管理。

**优势**

- 对 skill reuse 场景极强
- 文件可读可调试
- 框架无关
- 减少 embedding 依赖

**劣势**

- 对开放语义检索不如向量/图系统灵活
- 强依赖 agent 自己做工具调用与逐层展开
- 如果 skill schema 设计不好，记忆会变成碎片文件堆

**应用场景**

- coding agent 的 repair/ops/playbook 沉淀
- workflow agent 的 SOP 复用
- 希望把经验变成长期资产的 agent 平台

**对 Cortex-Mem 的借鉴**

- 程序性记忆应该独立于语义记忆存在
- Cortex-Mem 需要内建 `skill schema + skill distillation + skill recall`
- 不应把所有长期经验都压成 embedding

#### 1.3.5 Voyager

**定位**

Voyager 是程序性/技能记忆的经典样本。它证明：在开放世界任务里，长期记忆最稳的形态常常不是摘要，而是可执行代码技能。

**问题背景**

如果 Agent 要在长时程环境里不断成长，仅靠文字总结无法稳定复用行为。必须把经验沉淀成可执行、可组合、可验证的技能单元。

**技术方案**

- 自动课程生成
- 环境交互后总结成功/失败经验
- 将技能沉淀为 executable code library
- 下次任务优先复用已有 skill，而不是从零生成

**技术效果**

Voyager 的关键贡献是证明了“长期能力积累”可以通过 skill library 持续增长，而不是只能依赖即时 prompting。

**优势**

- 对 embodied / tool-using agent 的长期成长非常有效
- 记忆直接可执行
- 技能可复用、可组合

**劣势**

- 更适合明确工具环境，不适合所有 conversational agent
- 技能库维护会逐步变复杂
- 对一般业务问答场景不如语义记忆直接

**应用场景**

- 游戏/仿真 agent
- 可编程工具链 agent
- 自动化 workflow agent

**对 Cortex-Mem 的借鉴**

- 程序性记忆层应该与事实记忆层分离
- 长期高价值资产要优先沉淀为“可执行技能”而不是长文本总结

#### 1.3.6 Memoria

**定位**

Memoria 不是传统意义上的“更强召回”，而是“更安全地修改长期记忆”。

**问题背景**

长期记忆进入生产后，会出现三个高阶问题：

- 记忆变更需要追踪；
- 错误记忆需要回滚；
- 实验性记忆策略需要隔离。

Memoria 直接把这些问题映射成 Git 的操作模型。

**技术方案**

- snapshot / branch / merge / rollback
- Copy-on-Write 驱动的 memory mutation 管理
- vector + full-text hybrid retrieval
- contradiction detection
- low-confidence memory quarantine
- provenance chain + full audit trail

**技术效果**

Memoria 的价值不是把记忆做得更“聪明”，而是把记忆做得更“可治理”。这一点对生产系统尤其关键。

**优势**

- 版本治理概念清晰
- 特别适合审计、安全、回滚需求
- 对长时程 memory pollution 风险有直接应对能力

**劣势**

- 更像治理层与基础设施层，不是轻量插件
- 系统与运维复杂度更高
- 目前仍是较新的路线，生态成熟度待观察

**应用场景**

- 企业级 agent memory
- 需要 audit / rollback / branch experiment 的团队
- 安全敏感或合规敏感场景

**对 Cortex-Mem 的借鉴**

- Cortex-Mem 必须内建版本治理和 provenance ledger
- 记忆更新不应只有 overwrite，要有 branch / merge / rollback 语义
- 安全治理不是附属功能，而是 memory system 的一等公民

#### 1.3.7 XiaoClaw：为什么本轮只把它当作弱证据

本轮检索到的 `XiaoClaw` 官方入口，主要呈现为：

- OpenClaw 的一键安装与桌面封装；
- 浏览器自动化；
- 预装 Skills；
- 对中国网络和模型接入做优化。

它与 memory 生态有关，但**不是一个有足够清晰公开技术材料的独立 memory architecture**。因此本报告只把它当作生态包装层看待，而不把它作为 filesystem-like memory 的核心技术代表。

### 1.4 Filesystem-like 路线的整体优劣

#### 核心优势

- 人类可读、可审计、可修正
- 便于 git/version control
- 适合沉淀 skill / SOP / code artifact
- 更贴近 coding agent 和本地工作区
- 更容易做渐进式披露和层次浏览

#### 核心短板

- 大规模共享与服务化不如 northbound memory plane 顺手
- 多实体关系推理天然弱于图结构
- 一旦 schema/file layout 设计不好，目录会变脏
- 在多 Agent 并发写入时，需要更强治理机制

#### 最适合的场景

- coding agent
- local-first assistant
- research / workflow agent
- 对可观测性要求很高的团队
- 程序性记忆沉淀

---

## 2. Vector/Graph-like Agent Memory

### 2.1 问题背景：为什么这类系统会出现

如果 filesystem-like 路线主要解决“可读可控”，那么 vector/graph-like 路线主要解决的是**可共享、可扩展、可关系化**。

#### 案例一：多 Agent 框架各有状态，但彼此失忆

`ContextLoom` 直接把问题定义为 multi-agent systems 的“shared brain”。它指出：

- 一个 CrewAI agent 不知道 DSPy 模块刚刚学到了什么；
- 新 session 从数据库拉冷启动数据很脆弱；
- 长流程对话一旦超时或换框架，状态就断了。

这类痛点不是单个 agent 的个人记忆，而是**跨框架、跨进程、跨 agent 的共享状态问题**。

#### 案例二：多个 Agent 串行或并行协作时，缺少统一 memory/knowledge graph

`eion` 的设计就是为 multi-agent systems 提供 shared memory storage，并明确给出：

- sequential agency
- concurrent live agency
- external guest agent access

这类系统不是围绕单个 user profile，而是围绕**agent 间的上下文协同与受控共享**。

#### 案例三：个性化 agent 不只是记住消息，还要持续建模“实体”

`honcho` 的切入点很有代表性：它不是把记忆看成 message chunks，而是看成关于 users, agents, groups, ideas 等实体的持续状态建模。其官方示例中，math tutor chatbot 会利用系统推断的 learning styles 来调整行为。

这说明 vector/graph-like 系统开始从“检索历史消息”转向“持续建模实体和关系”。

#### 案例四：生产级 AI 应用需要通用 memory layer，而不是每个团队重造一遍

`mem0` 的官方定位是 universal, self-improving memory layer。这里的关键词不是 file，也不是 branch，而是：

- 通用层；
- 生产接入；
- memory as infrastructure；
- 多框架集成。

这类系统出现的背景，是企业与产品团队不想为每个 agent 重写一套 memory stack。

#### 案例五：多个 coding agent 需要共享云端长期记忆，而不是各自绑在一台电脑上

`mem9` 公开强调的痛点非常具体：

- session 结束即失忆；
- 一个 agent 学到的内容，另一个 agent 用不到；
- 本地 memory file 绑死在单机；
- 团队里不同人的 agent 无法共享发现。

因此它选择的是 stateless plugin + cloud memory pool。

### 2.2 这类系统的共同技术路线

#### 共性一：把 memory 做成 northbound service / API / shared plane

这类系统的主接口通常不是文件树，而是：

- SDK
- REST API
- managed service
- shared Redis/DB context plane
- MCP / framework integration

它们更像“上层 Agent 可以统一调用的北向记忆层”。

#### 共性二：语义召回和结构化召回共同出现

这类系统很少只做纯向量检索，而是引入：

- vector + keyword hybrid search
- entity representation
- session context
- graph traversal
- knowledge graph / temporal graph

因此它们更适合处理：

- 多实体关系；
- 跨会话归纳；
- 多 Agent 共享；
- 大规模服务化检索。

#### 共性三：共享命名空间与隔离机制变得重要

一旦是 northbound memory plane，问题就变成：

- 哪些 agent 共享同一 memory pool；
- 哪些只读；
- 哪些 tenant 隔离；
- 哪些 guest access；
- 哪些 workspace/scopes。

Filesystem-like 系统也会遇到这个问题，但 vector/graph-like 系统更常把它做成一等配置项。

#### 共性四：后台 consolidation / representation 更常见

这类系统比 filesystem-like 更倾向于在后台生成：

- representation
- summary
- entity state
- relation edge
- session context

从而让检索结果不仅是文档片段，而是“关于某个对象的结构化认识”。

#### 共性五：规模化与多 Agent 协作优先于人类直接编辑

这类系统通常更擅长：

- 共享
- 并发
- 服务治理
- 大规模接入

但代价是：

- 人类直接编辑不如文件型直观；
- 黑箱风险更高；
- provenance 若设计不够强，会更难调试。

#### 共性六：这一路线正在吸收“时间层次化、轻量图导航、多类型协同”三种研究增量

旧稿里有三类旁系参照是值得保留的：

- **TiMem**
  提供时间层次化 consolidation 与 complexity-aware recall；
- **LiCoMemory**
  证明图不一定要做成重型知识图谱，也可以是轻量认知索引层；
- **MIRIX**
  强调多记忆类型与 active retrieval 的协同。

这些工作不属于本专题要求的核心项目清单，但它们说明 vector/graph-like memory 的“下一步”并不只是继续堆向量，而是：

- 引入时间层次；
- 引入轻量结构；
- 引入类型分工；
- 引入更主动的检索编排。

### 2.3 关键系统深度研究

#### 2.3.1 ContextLoom

**定位**

ContextLoom 是 multi-agent systems 的 shared brain，用 Redis 作为 persistent context state，并支持从传统数据库做 cold start hydration。

**问题背景**

它解决的是框架级 amnesia 和 context fragmentation：

- 不同 agent framework 各自持有局部状态；
- 新 session 需要人工把数据库历史塞回 prompt；
- 长流程循环容易重复和断裂。

**技术方案**

- Redis-first memory backend
- decouple memory from compute
- 从 PostgreSQL / MySQL / MongoDB 拉冷启动数据
- communication cycle + cycle hash
- 检测 loop/repetition 并推动 agent pivot
- 为 DSPy、CrewAI、Agno、Google ADK 提供 wrapper

**技术效果**

ContextLoom 的重点不是高阶图推理，而是把“跨框架共享上下文状态”做成轻量可落地中间层。

**优势**

- 框架无关性强
- 适合多 Agent 协作
- Redis 路线简单直接
- 冷启动数据接入清晰

**劣势**

- 关系建模能力有限，更多是 state bus 而非知识图谱
- 证据主要来自 README 和项目说明
- 生态成熟度相对较早期

**应用场景**

- 多框架协作系统
- 需要共享全局上下文状态的 orchestrator
- 订单、客服、流程编排等需要 cold start 数据注入的场景

**对 Cortex-Mem 的借鉴**

- Cortex-Mem 需要 northbound shared context bus
- cold start hydration 应作为独立能力存在
- 循环检测可以成为 agent state management 的一部分

#### 2.3.2 eion

**定位**

eion 是面向 multi-agent systems 的 shared memory storage，强调 unified knowledge graph。

**问题背景**

一旦系统从单 Agent 走向 agency，问题会从“单体记忆检索”变成：

- 多 Agent 如何共享上下文；
- 串行链路如何持续继承状态；
- 外部 guest agent 如何受控访问；
- 如何同时支持 conversation history 和 temporal knowledge。

**技术方案**

- PostgreSQL + pgvector 负责 memory storage 与 semantic search
- Neo4j 负责 knowledge graph
- unified API
- register console 管理 agents、permissions、resource snippets
- 支持 sequential agency、live agency、guest access

**技术效果**

eion 的价值在于把 shared memory 与 graph capabilities 统一在一个 northbound memory service 里，而不是让每个团队自己拼。

**优势**

- 多 Agent 共享能力明确
- 图关系表达能力强于纯向量层
- 权限与注册机制较清晰

**劣势**

- 部署复杂度明显高于 Redis-only 或单向量库方案
- 项目仍然早期
- 主要证据来自仓库和架构说明

**应用场景**

- 多 Agent 协同系统
- 需要知识图谱和权限控制的 memory platform
- 企业级 orchestration 场景

**对 Cortex-Mem 的借鉴**

- Cortex-Mem 的 northbound API 应支持 tenant、agent、permission、guest scope
- 图层适合承载关系和时序，而不是替代所有原始记忆

#### 2.3.3 honcho

**定位**

honcho 是一个 open source memory library with managed service，用于构建 stateful agents。

**问题背景**

它试图解决的不是“下一轮怎么找历史消息”，而是“agent 如何逐步理解用户、群体、其他 agent 和抽象实体，并随着时间持续更新”。

**技术方案**

- workspace / peer / session 抽象
- 持续维护实体状态
- `chat` 直接对实体提问
- `search` 查找相似消息
- `context` 生成 session-scoped context
- `representation` 获取某个 peer 在特定 session 下的状态表示

**技术效果**

honcho 的独特点是把“记忆”从 conversation chunk 提升成 entity-aware state modeling。

**优势**

- 适合个性化和 social cognition
- 对 stateful chatbot 很自然
- 支持开放式实体建模，而不只限 user profile

**劣势**

- 人类可读性不如文件型方案
- 背后 reasoning 更黑箱
- 对开发团队提出更高抽象理解要求

**应用场景**

- 个性化聊天机器人
- tutor / coach / companion agent
- 需要持续理解用户偏好与风格的产品

**对 Cortex-Mem 的借鉴**

- Cortex-Mem 的 graph/vector 层不应只服务检索，也要服务 representation
- “关于实体的状态”应独立于“原始消息记录”

#### 2.3.4 mem0

**定位**

mem0 是通用型、可自改进的 memory layer，面向 LLM apps 与 agents。

**问题背景**

产品团队需要的并不是一套研究型 memory demo，而是一层：

- 好接入；
- 可托管；
- 可自托管；
- 能覆盖多框架与多产品形态；
- 能持续从交互中抽取长期记忆。

**技术方案**

- 作为 universal memory layer 暴露
- 支持平台托管、开源自托管、CLI、插件、REST/API
- 从交互中抽取 salient information
- 做 consolidate / retrieve
- 继续扩展到 graph memory 和多集成生态

**技术效果**

mem0 的最大价值是把“长期记忆”产品化成一层中间件，而不是要求应用团队自己构建一套 memory backend。

**优势**

- 易集成
- 产品化成熟度高
- 生态集成丰富
- 适合作为通用 memory SDK

**劣势**

- 对人类可读性和直接审计不如 filesystem-like
- 很多性能口径仍依赖论文和项目自报
- 若没有额外治理层，长期写入风险仍在

**应用场景**

- 通用 AI assistant
- 客服、个性化、Agent workflow
- 需要快速集成 persistent memory 的产品团队

**对 Cortex-Mem 的借鉴**

- Cortex-Mem 需要 northbound SDK/API，而不只是本地文件层
- 通用 memory layer 必须有足够好的接入体验，否则很难进入实际产品

#### 2.3.5 mem9

**定位**

mem9 是面向 AI coding agents 的 persistent cloud memory。

**问题背景**

mem9 明确针对 coding agent 的四类问题：

- session 结束即失忆；
- 各 agent 之间形成 silo；
- 本地文件绑死在单机；
- 团队间无法共享发现。

**技术方案**

- stateless plugin + central memory server
- same tenant 共享 memory pool
- TiDB 支撑 hybrid vector + keyword search
- visual dashboard
- 统一的 memory CRUD tools
- 中央化的限流、审计和控制

**技术效果**

它把 coding agent 的长期记忆从“本地文件习惯”升级为“多客户端共享的云记忆池”。

**优势**

- 跨机器、跨 agent、跨团队共享
- 适合 coding agent 协作
- 插件无状态，运维边界更清晰
- 混合检索实用

**劣势**

- 可读性和本地可编辑性弱于 memsearch
- 更依赖服务端与外部存储
- 对隐私和治理提出更高要求

**应用场景**

- 团队协同 coding agents
- 跨终端使用同一记忆池
- 中心化记忆平台

**对 Cortex-Mem 的借鉴**

- northbound cloud memory pool 很重要，尤其在多人协作场景
- 插件无状态、后端有状态是很有价值的边界划分

### 2.4 Vector/Graph-like 路线的整体优劣

#### 核心优势

- 多 Agent 共享更自然
- 更适合 northbound service 化
- 语义召回与关系推理能力更强
- 易于做多租户、权限、tenant、workspace
- 更适合规模化生产接入

#### 核心短板

- 人类可读和直接编辑能力通常较差
- provenance 若设计不足，会形成更深黑箱
- 图/向量基础设施会提高部署复杂度
- 容易把“记忆”退化成难以审计的 embedding 池

#### 最适合的场景

- stateful chatbot
- personalized assistant
- 多 Agent orchestration
- 企业级 memory-as-a-service
- 需要关系建模或共享状态的系统

### 2.5 旁系参照：为什么 TiMem、LiCoMemory、MIRIX 值得作为“北向结构化记忆”的补充样本

虽然它们不在本专题两大类的主清单里，但旧稿中这三类工作提供了很有价值的旁系信息：

#### TiMem

TiMem 的价值不在于“分数更高”，而在于它把**时间层次化记忆树**讲清楚了：

- 细节记忆与稳定画像不应混在同一层；
- 查询复杂度不同，召回层级也应不同；
- consolidation 不只是压缩，而是抽象层级上移。

这对 Cortex-Mem 最大的启示不是照搬 5 层树，而是明确：northbound memory plane 不能只有 top-k recall，还要有时间尺度感知。

#### LiCoMemory

LiCoMemory 的价值在于提出“**图即检索索引**”而不是“图即全量推理引擎”。这对工程很重要，因为它说明：

- 结构化层不一定要上重型 KG；
- 图的主要职责可以是导航和候选缩减；
- 轻量图能在表达力和运维复杂度之间找到更好的平衡。

#### MIRIX

MIRIX 的关键贡献是让“多类型记忆”变得更具体：

- semantic
- episodic
- procedural
- resource
- core
- vault

它提醒我们，vector/graph-like memory 真正走向成熟时，通常不会只剩一个统一 embedding 池，而会出现更明确的 memory type orchestration。

---

## 3. 两类路线的对比分析

### 3.1 能力对比表

| 维度 | Filesystem-like | Vector/Graph-like |
|------|-----------------|-------------------|
| **主导接口** | 文件、目录、Markdown、skill file、版本对象 | SDK、API、shared context plane、vector/graph store |
| **源头真相** | 人类可读文件/技能资产 | 服务端状态、向量索引、图结构、entity representation |
| **典型检索** | 目录浏览、渐进式披露、文件读取、语义辅助 | top-k/混合检索、graph traversal、representation lookup |
| **可观测性** | 强 | 中到弱，取决于产品化程度 |
| **直接可编辑性** | 强 | 弱到中 |
| **多 Agent 共享** | 可做，但不是天然强项 | 天然强项 |
| **关系推理** | 中，依赖额外设计 | 强于文件型，尤其图/知识图谱路线 |
| **程序性记忆** | 强 | 中，常需外挂 skill layer |
| **治理/版本化** | 容易自然落地 | 需要额外层补齐 |
| **规模化服务化** | 中 | 强 |
| **典型成本** | 文件组织简单，但 schema 设计关键 | 基础设施更重，但共享收益更高 |

### 3.2 不是替代关系，而是分工关系

两类路线最容易被误解的地方是：大家常把它们看成互斥方案。

其实更合理的理解是：

- **filesystem-like**
  更像 southbound 的人类可读 memory surface。
- **vector/graph-like**
  更像 northbound 的共享语义/关系 memory plane。

也就是说：

- 前者擅长让人和 agent 一起看懂、修正和沉淀记忆；
- 后者擅长让多个 agent 和产品系统在统一平面上调用记忆。

### 3.3 选型建议

#### 如果你做的是 coding agent

优先级通常是：

1. 可读可审阅
2. 技能复用
3. 跨会话 recall
4. 必要时再上共享 memory pool

因此 filesystem-like 更适合作为第一层；若团队协作强，再叠一层 vector/graph service。

#### 如果你做的是 24/7 proactive assistant

需要同时具备：

- 文件树式长期结构；
- 后台 memory worker；
- 更轻的长期上下文成本；
- northbound 语义/关系索引。

因此往往天然走向混合架构。

#### 如果你做的是企业级多 Agent 系统

优先级会变成：

1. northbound shared memory plane
2. tenant / workspace / permission
3. graph / relation / temporal model
4. 审计和可观测补齐

这时 vector/graph-like 是基础层，但仍需要 filesystem-like 的审计界面或导出表面。

### 3.4 两类路线的共同盲区与方法论风险

旧稿最值得保留的一部分，是它对“大家都在忽略什么”给出了更锋利的判断。整理后，当前两类路线至少共有四个共同盲区。

#### 盲区一：遗忘与记忆治理仍然普遍缺位

无论是 filesystem-like 还是 vector/graph-like，真正把以下能力做完整的系统都很少：

- 过期判定
- 冲突解决
- 低置信内容隔离
- 回滚
- 清理策略

大多数系统擅长“写入”和“召回”，但不擅长“治理”。

#### 盲区二：安全治理远落后于记忆能力

旧稿里关于 Memoria 的判断是合理的：它的重要性并不在于检索更强，而在于它真正把 rollback、branch、audit、quarantine 提到了 memory core。

这同时暴露出行业共性：大多数系统还没有把长期记忆当作高风险面来设计，而只是当作增强 recall 的功能模块。

#### 盲区三：benchmark 经常衡量不了真正的工程价值

这是旧稿里最值得保留的批判性结论之一。

比如：

- Filesystem-like 系统的核心价值往往是可读、可审计、可迁移、可技能化；
- Vector/graph-like 系统的核心价值往往是共享、关系化和 northbound service 化；

但 LoCoMo、LongMemEval 之类 benchmark 更多测的是长期召回与问答正确率，并不直接衡量：

- 工程师能否修 memory；
- 团队能否共享 memory；
- memory 被污染后能否回滚；
- 程序性经验能否稳定复用。

因此，benchmark 对 memory system 很重要，但不能替代工程判断。

#### 盲区四：很多“强结论”其实建立在不可比口径上

旧稿中有不少激进数字，本次保留的合理结论不是这些数字本身，而是其背后的方法论警示：

- 同一系统的论文口径、项目 README 口径、独立复现实验，可能完全不同；
- 不同系统使用的 benchmark、judge model、上下文预算和基座模型也经常不同；
- 因此“统一总榜”在当前阶段通常不可靠。

这也是为什么本专题最终选择：

- 保留结构与方法论上的结论；
- 弱化跨系统数值总排名；
- 强化证据等级与适用场景判断。

---

## 4. Cortex-Mem 创新方案的借鉴

本节不是产品宣传，而是基于上述两类路线推导 Cortex-Mem 的合理演进方向。

### 4.1 Cortex-Mem 不应二选一，而应做“五层混合”

#### L0 原始事件层

- 保存对话、工具调用、网页观察、文档片段、附件摘要
- append-only
- 每条记录都有 provenance

#### L1 Filesystem-like 记忆表面

- 用 Markdown / resource file / skill file / versioned object 承载人类可读记忆
- 支持目录组织、按需展开、局部编辑、导出迁移

#### L2 Vector/Graph-like 语义索引层

- 为 L1 的记忆对象构建 shadow index
- 既支持 dense retrieval，也支持 full-text / metadata / relation lookup
- 不把向量层当真相层

#### L3 程序性/技能层

- 将成功策略、操作套路、playbook、代码片段沉淀为 skill memory
- 与事实记忆分离治理

#### L4 治理与版本层

- snapshot / branch / merge / rollback
- contradiction detection
- trust / namespace / quarantine
- audit trail

### 4.2 Cortex-Mem 应明确借鉴 filesystem-like 路线的五点

1. **Markdown/skill file 作为可审阅对象**
2. **progressive disclosure 作为默认召回范式**
3. **resource、memory、skill 统一放进一个上下文对象模型**
4. **程序性记忆与语义记忆分层**
5. **把版本治理和 rollback 做成原生能力**
6. **append-only raw episodes + layered summaries**
   这不是某个单点项目的专利，而是 filesystem-like 路线里反复出现的合理结构，应成为 Cortex-Mem 的默认底座。

### 4.3 Cortex-Mem 应明确借鉴 vector/graph-like 路线的五点

1. **northbound memory API/SDK**
2. **tenant/workspace/agent scope**
3. **hybrid retrieval 与 entity representation**
4. **graph/temporal layer 承载复杂关系**
5. **多 Agent 共享与后台 consolidation**

### 4.4 一个更具体的 Cortex-Mem 混合架构

| 层 | 借鉴来源 | 目标 |
|----|---------|------|
| 文件表面层 | OpenViking / memsearch / Acontext | 可读、可调试、可迁移 |
| 技能层 | Acontext / Voyager | 经验复用、程序性记忆 |
| 主动记忆层 | memU | 后台监控、意图捕捉、长期连续性 |
| 北向语义层 | mem0 / mem9 / ContextLoom | 通用 API、共享 memory pool、跨框架接入 |
| 图关系层 | eion / honcho | 实体关系、时序、表示层 |
| 治理层 | Memoria | 审计、分支、回滚、隔离 |

### 4.5 Cortex-Mem 应避免的三类错误

1. **把向量库直接当记忆真相层**
   这样会快速失去审计性和可修正性。

2. **只做文件表面，不做 northbound 共享语义层**
   这样很难支撑多 Agent、跨终端、跨产品。

3. **只谈 recall，不谈治理**
   长期记忆最难的问题往往不是找不到，而是找错、写错、污染后无法回滚。

---

## 5. 最终结论

如果用一句话总结这次研究：

> **Filesystem-like agent memory 解决的是“让记忆成为可读、可控、可沉淀的工程资产”；vector/graph-like agent memory 解决的是“让记忆成为可共享、可语义化、可关系化的北向基础设施”。**

因此，Cortex-Mem 最合理的方向不是站队，而是融合：

- 以 filesystem-like 路线保证可读、可审计、可技能化；
- 以 vector/graph-like 路线保证共享、关系化、服务化；
- 以 Memoria 式治理层保证长期安全演进。

这比单纯做“更大的记忆库”更接近真正可用的 Agent Memory System。
