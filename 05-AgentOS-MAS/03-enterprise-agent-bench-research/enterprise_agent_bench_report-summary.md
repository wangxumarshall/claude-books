# 企业级 Agent 系统评估研究报告

公开资料截至：2026-05-08
研究对象：企业级 AI Agent 的评估理论、基准体系、工程方法、平台能力与 AgentRuntimeFabric 设计启示

## 摘要

企业级 Agent 不是单次问答模型，而是由模型、编排框架、工具、运行时、状态、权限、记忆、人工协作和业务系统共同构成的执行系统。公开研究与产业文档显示，Agent 评估已经从“最终文本是否正确”扩展为“最终业务状态、执行轨迹、工具副作用、安全治理、可靠性、成本与可观测性”的系统工程问题；AgentBench、SWE-bench、WebArena、OSWorld、WorkArena、tau-bench、HAL 与 CLEAR 等基准共同推动了这种转向。[R1][R2][R3][R4][R5][R6][R7][R8][R9][R10]

本报告的核心结论是：企业级 Agent 的最终结果仍然是必要底线，但不能作为充分证据。上线级评估必须同时验证结果是否正确、路径是否合法、权限是否受控、状态是否一致、失败是否可恢复、成本是否可承受、审计证据是否完整。Anthropic、OpenAI 与 Google Cloud 的评估文档均把任务、试次、评分器、轨迹或最终响应/轨迹评估纳入 Agent 评估流程，说明轨迹评估已经成为产业级方法的一部分，而非单纯的研究概念。[R11][R12][R13][R14]

面向 AgentRuntimeFabric，本报告建议将其定位为开源、自托管、模型中立、运行时中立的 Agent 证据与治理控制面。它的核心差异不应是再造一个 Agent SDK，而应是把 EventLog、EvidenceGraph、PolicyDecision、ExecutionLease、WorkspaceLineage、RuntimeAdapter 与 Artifact 作为一等对象，支撑可恢复、可审计、可复现、可治理的企业级 Agent 执行。[R11][R12][R15][R16][R17][R18]

**关键词**：AI Agent；企业级评估；轨迹审计；工具调用；运行时隔离；安全治理；可观测性；AgentRuntimeFabric

## 1. 研究问题与方法

### 1.1 研究问题

本报告回答五个问题：

1. 企业级 Agent 为什么不能只用传统模型 benchmark 或最终答案准确率评估？
2. 当前学术界和产业界的代表性 Agent 基准分别解决了什么问题，又不能解决什么问题？
3. 一个生产级企业 Agent 评估体系应包含哪些指标、任务集、评分器和上线门禁？
4. OpenAI、Anthropic、Google Cloud、AWS 与 Kimi 等平台能力应如何放入同一评估口径，而不是混为同类对象？
5. AgentRuntimeFabric 应如何吸收这些研究结论，形成可验证的开源控制面能力？

这些问题的共同前提是：Agent 会调用工具、改变外部状态、消耗真实资源，并可能触发不可逆副作用；因此评估对象必须从“模型输出”扩展到“系统行为”。AgentBench 把 LLM 放入多种交互环境中测试，WebArena 和 OSWorld 分别强调 Web 与桌面环境状态，SWE-bench 以真实代码库测试补丁结果，tau-bench 用数据库最终状态和多轮用户交互评估工具型 Agent，这些基准共同证明了评估对象的系统化扩展。[R1][R3][R4][R5][R7]

### 1.2 研究方法

本报告采用文献综述、证据分层、平台能力归类与工程推演四种方法。文献综述覆盖公开学术论文、官方 benchmark、云厂商文档和官方工程博客；证据分层用于区分论文结论、官方产品能力与分析性推断；平台能力归类用于避免把 SDK、托管运行时、企业控制面和业务系统混为同一对象；工程推演用于提出 AgentRuntimeFabric 的可实现对象模型与评估门禁。[R8][R10][R11][R12][R15][R16][R17][R18]

本报告只将 A/B 级来源作为主要证据：A 级为官方文档、官方工程博客、正式 API 文档和官方帮助中心；B 级为 arXiv、OpenReview、会议论文、官方 benchmark 网站和开源仓库。云厂商博客、技术媒体和社区文章只作为趋势说明；未能被 A/B 级来源支持的强断言不进入正文结论。NIST AI RMF 与 OWASP LLM Top 10 被用作治理和安全风险框架，而不是 Agent 性能 benchmark。[R19][R20]

## 2. 研究结论

### 2.1 结果必要，但不足以证明可信

企业级 Agent 评估不能抛弃结果。最终数据库、文件、工单、PR、报表、消息、审批记录是否正确，是业务验收的第一门槛。SWE-bench 以测试是否通过验证代码修改，WebArena 强调后端状态和页面状态，tau-bench 将最终数据库状态纳入评分，这些做法说明“最终状态”仍然是客观评估的基础。[R3][R4][R7]

同时，最终结果不足以证明 Agent 可信。一个 Agent 可能输出正确答案，却使用了错误数据源、跳过审批、读取未授权数据、误解工具返回值、重复执行不可逆操作，或在工具失败后伪造完成。OpenAI 的 trace grading 将 trace 定义为端到端决策、工具调用和推理步骤日志，用于定位 workflow 层面的正确性、质量和合规问题；Google 的 Agent evaluation 明确区分 final response evaluation 与 trajectory evaluation；Anthropic 的 Agent eval 方法把 transcript/trajectory 作为一次 trial 的完整记录。[R11][R12][R13][R14]

因此，企业级 Agent 的可信性应由三层证据共同支持：结果证据证明任务是否完成，轨迹证据证明完成路径是否合规，恢复证据证明异常中断后能否保持状态、权限链和副作用一致。没有轨迹证据的“成功”不可审计；没有结果证据的“合规路径”不能证明业务完成；没有恢复证据的长任务不能进入生产级自动化。[R11][R12][R15][R16]

### 2.2 Agent 评估对象必须分层

Agent 评估常见错误是把模型、Agent scaffold、运行时、工具网关、企业平台和业务系统放进同一个排行榜。模型层主要回答推理、代码、视觉、工具调用格式是否足够；scaffold 层回答规划、重试、handoff、停止条件是否合理；运行时层回答 shell、browser、code interpreter、sandbox 是否隔离和可恢复；工具网关层回答身份、策略、审计、限流和参数校验是否强制执行；企业平台层回答 registry、memory、observability、evaluation、identity 是否被统一治理；业务系统层回答 Agent 是否产生可接受的业务价值。[R12][R15][R16][R17][R18]

不同层级必须使用不同指标。模型层可以使用 pass@1、准确率和工具调用格式；scaffold 层需要轨迹正确率、工具选择、错误分类和重规划能力；运行时层需要隔离边界、生命周期、文件系统持久化、网络策略和恢复能力；工具网关层需要策略命中率、越权拦截、参数 schema 校验和审计完整性；业务系统层需要最终状态正确率、人工返工率、事故率、SLA 和 ROI。[R11][R12][R16][R17][R19][R20]

### 2.3 公开 benchmark 只能提供基线，不能替代企业私有评估

AgentBench、GAIA、SWE-bench、WebArena、OSWorld、WorkArena、tau-bench、TheAgentCompany、CLEAR 与 HAL 为 Agent 研究提供了重要基线，但没有任何单个公开 benchmark 能代表企业生产就绪度。公开 benchmark 的价值在于暴露能力边界、比较模型和框架、沉淀评分方法；企业上线仍需私有黄金任务、脱敏生产 trace、对抗样本、异常恢复实验和人工校准。[R1][R2][R3][R4][R5][R6][R7][R8][R9][R10][R11]

原因有三点。第一，企业任务依赖私有权限、流程、数据模型、审批制度和不可逆副作用，公共基准无法覆盖。第二，Agent 的非确定性导致单次运行不能代表可靠性，Anthropic 建议用多次 trial 并区分 pass@k 与 pass^k；tau-bench 也强调一致成功概率对面向客户的 Agent 更重要。[R7][R11] 第三，评估环境本身可能成为攻击面，Berkeley RDI 对基准环境的安全分析提醒研究者必须审计 benchmark harness、oracle 和沙箱边界。[R21]

## 3. 文献与基准体系

### 3.1 综合性研究

LLM-based Agent evaluation 综述系统梳理了 Agent 评估中的任务设计、环境交互、工具使用、记忆、规划、安全和长期可靠性问题，为本报告的指标框架提供了总览。[R22] “AI Agents That Matter”指出 Agent 评估容易受成本、脚手架差异、实现细节和不可复现实验影响，强调必须报告成本、运行设置和可复现证据；HAL 也以此为动机构建成本可见的统一评估平台。[R23][R10]

### 3.2 代表性基准

| 基准 | 主要评估对象 | 关键贡献 | 企业评估启示 |
| --- | --- | --- | --- |
| AgentBench | LLM-as-Agent | 将 Agent 放入 Web、数据库、操作系统、游戏等交互环境中测试 | Agent 能力必须在环境内评估，而不是只测静态文本输出。[R1] |
| GAIA | 通用 AI 助手 | 面向真实世界问题的信息检索、工具使用和多步推理 | 知识工作评估应包含外部信息整合，但仍需企业权限和状态模型补充。[R2] |
| SWE-bench | 代码 Agent | 以真实 GitHub issue 和仓库级补丁作为任务，使用测试验证修复 | 软件工程 Agent 评估必须包含真实代码库、测试、回归和 diff 审查。[R3] |
| WebArena | Web Agent | 构建高保真网站环境，验证浏览器导航和状态变更 | 浏览器 Agent 不能只看页面文本，必须验证后端和页面状态。[R4] |
| OSWorld | Computer-use Agent | 在真实桌面/操作系统任务中评估多模态 Agent | GUI Agent 需要检查文件、应用配置、数据库和 UI 状态。[R5] |
| WorkArena | 企业工作流 Agent | 基于企业 SaaS 工作流测试知识工作自动化 | 企业任务必须纳入票据、角色、流程和系统状态。[R6] |
| tau-bench | 工具-用户交互 Agent | 用多轮用户模拟、工具调用和最终数据库状态评估策略遵循 | 客服和运营 Agent 应关注 pass^k，即多次都成功的可靠性。[R7] |
| TheAgentCompany | 数字员工 Agent | 在模拟公司环境中测试多类工作任务 | 数字员工评估应关注跨系统任务链，而不是孤立能力点。[R9] |
| CLEAR | 企业多维评估 | 将 Cost、Latency、Efficacy、Assurance、Reliability 纳入统一框架 | 企业不能只看 accuracy，必须把成本、时延、安全和可靠性放入主评分。[R8] |
| HAL | 评估基础设施 | 提供标准 harness、成本报告、并行执行、trace/token 日志和跨 benchmark 比较 | 评估本身需要可复现、可比较、可审计。[R10] |

### 3.3 CLEAR：多维评估框架的价值与边界

CLEAR 的价值在于把企业 Agent 评估从单点准确率推进到 Cost、Latency、Efficacy、Assurance、Reliability 五个维度。该框架适合纠正“只看成功率”的倾向，尤其适用于评估成本可承受性、时延是否满足业务 SLA、策略遵循和多次运行可靠性。[R8]

使用 CLEAR 时必须遵守论文边界。CLEAR 是重要研究框架，不是所有行业、所有任务、所有平台的唯一标准；其任务集、行业覆盖、专家评估和相关性结论只能在论文报告范围内使用。企业采用 CLEAR 的正确方式是把五维框架转化为自身业务指标，而不是直接把论文得分当作上线结论。[R8][R19]

### 3.4 HAL：评估基础设施的可复现方向

HAL 的核心贡献不是再提出一个单项任务集，而是提供标准化评估 harness、成本控制、token/trace 记录、并行执行和跨 benchmark 比较。HAL 论文报告了 21,730 次 Agent rollout，覆盖 9 个模型与 9 个 benchmark，并公开强调成本、trace 和复现性对理解 Agent 行为的重要性。[R10] HAL 官方说明也指出，Agent 评估若只关注 accuracy 而忽略成本，会让下游开发者难以判断真实价值。[R24]

HAL 对企业的启示是：评估平台必须同时记录模型、scaffold、工具、参数、成本、轨迹和日志；模型榜单不能替代系统榜单；同一模型在不同 scaffold 和工具边界下可能呈现完全不同的可靠性和成本曲线。[R10][R23][R24]

### 3.5 安全基准与评估环境安全

Agent Security Bench 将 LLM Agent 的攻击和防御形式化，覆盖多类应用场景、工具与攻防方法，说明 Agent 安全必须独立成为评估维度，而不是被普通任务成功率吸收。[R25] OWASP LLM Top 10 将 Prompt Injection、Sensitive Information Disclosure、Excessive Agency 等列为 LLM 应用风险，进一步说明具有工具权限的 Agent 需要最小权限、隔离、审批和对抗性测试。[R20]

安全评估还必须覆盖 benchmark 自身。Berkeley RDI 关于可信 benchmark 的研究指出，Agent 可以攻击或利用评估环境、测试框架、配置和本地文件边界；因此企业内部评估需要把 Agent 执行环境、评分 oracle、测试密钥、参考答案和日志保留系统隔离开来。[R21]

## 4. 企业级 Agent 指标体系

### 4.1 一级指标

| 一级指标 | 核心问题 | 示例度量 | 主要证据 |
| --- | --- | --- | --- |
| 任务效能 | Agent 是否完成真实业务目标 | task success、最终状态正确率、partial credit、人工验收率 | SWE-bench、WebArena、tau-bench 均使用状态或测试验证任务完成。[R3][R4][R7] |
| 轨迹正确性 | Agent 是否以合规路径完成任务 | 工具序列、参数正确率、证据引用完整率、策略路径合规率 | OpenAI trace grading、Google trajectory evaluation、Anthropic transcript 方法均支持轨迹评估。[R12][R13][R14] |
| 工具与执行 | Agent 是否稳定调用外部系统 | tool call success、schema violation、retry rate、timeout rate | Agents SDK、AgentCore Runtime、Google Agent Platform 都将工具与运行环境作为 Agent 生产能力组成部分。[R15][R16][R17] |
| 状态与记忆 | Agent 是否维护正确上下文 | session consistency、memory retrieval precision、workspace checksum、memory revision audit | Google Memory Bank 与 Anthropic session log 均强调跨会话状态与可恢复上下文。[R17][R18][R26] |
| 安全与治理 | Agent 是否遵守权限、审批和数据边界 | policy violation、approval bypass、secret leak、egress violation、prompt injection success rate | NIST AI RMF、OWASP LLM Top 10、ASB 和 AWS AgentCore Policy 支持风险治理评估。[R19][R20][R25][R27] |
| 可靠性 | 多次运行是否稳定 | pass@1、pass@k、pass^k、方差、flake rate、恢复成功率 | Anthropic 对 pass@k/pass^k 的区分与 tau-bench 的一致性评估为可靠性提供方法依据。[R7][R11] |
| 成本与时延 | Agent 是否具备商业可行性 | token/task、tool calls/task、runtime minutes、p50/p95/p99 latency、idle cost | CLEAR 和 HAL 都把成本与性能共同纳入评估。[R8][R10][R24] |
| 人机协作 | Agent 是否知道何时升级给人 | handoff precision、handoff latency、handoff context completeness、approval coverage | OpenAI Agents SDK 支持 handoff 与 human-in-the-loop，NIST AI RMF 强调治理和风险管理。[R15][R19] |
| 可观测审计 | 行为是否可解释、可追责、可复现 | trace completeness、event coverage、artifact lineage、replayable ratio | OpenAI tracing、HAL trace/token 日志、AgentCore observability 均指向可观测性要求。[R10][R12][R16][R24] |

### 4.2 结果、轨迹与恢复的三层校验

结果校验回答“业务状态是否正确”。在代码场景中，它对应测试通过、回归不破坏和 diff 合理；在 Web 场景中，它对应页面状态与后端状态；在客服或运营场景中，它对应数据库记录、工单状态、退款记录、通知状态和用户目标是否一致。[R3][R4][R7]

轨迹校验回答“完成路径是否可信”。它检查 Agent 是否先读取必要信息再写入、是否选择授权工具、是否传递正确参数、是否正确解析结构化返回、是否在高风险动作前触发审批、是否保留引用与证据。OpenAI、Google 与 Anthropic 的评估文档均把 trace、trajectory 或 transcript 放入 Agent 评估流程，为轨迹校验提供了产业依据。[R11][R12][R13][R14]

恢复校验回答“异常后是否仍然安全”。长任务 Agent 可能经历网络中断、工具超时、runtime 停止、上下文压缩、人工纠错和多 Agent 合并冲突。AWS AgentCore Runtime 文档说明了隔离 session、microVM、最长运行时间、stop/resume 和持久文件系统等能力；Anthropic Managed Agents 的工程文章说明了 session、harness、sandbox 解耦的恢复思路。这些能力表明恢复能力已成为生产运行时设计的一部分，也应成为评估门禁。[R16][R18][R28][R29]

### 4.3 门禁规则

企业上线不应使用“单一总分抵消所有失败”的规则。高准确率不能抵消越权访问、审批绕过、敏感数据泄露、不可逆副作用重复执行、审计证据缺失或无法恢复的长任务。NIST AI RMF 的 Govern、Map、Measure、Manage 思路要求组织把风险容忍度、测量和治理动作制度化；OWASP LLM Top 10 则提示 Agent 场景需要特别关注 prompt injection、敏感信息披露和过度代理权。[R19][R20]

建议采用硬门禁与维度评分组合：Outcome Score、Trajectory Score、Safety Score、Reliability Score、Economic Score、Operability Score 可以用于比较候选方案；但只要 Safety、Auditability、Irreversible Side Effect 或 Recovery 任一门禁失败，高风险自动化任务不得进入无人值守生产路径。[R11][R19][R20][R25]

## 5. 评估方法论

### 5.1 任务集构建

企业 Agent 评估应构建四层任务池。第一层是公共基准池，用于横向比较模型与 scaffold，例如 SWE-bench、WebArena、OSWorld、tau-bench 和 HAL 支持的多 benchmark 评估。[R3][R4][R5][R7][R10] 第二层是私有黄金任务池，用于覆盖企业自己的客服、CRM、财务、研发、合规、运营和数据流程；Anthropic 建议从真实失败、手动测试和明确成功标准开始构建任务。[R11] 第三层是对抗与异常池，用于测试 prompt injection、越权工具、脏数据、网络失败、工具超时、secret 泄漏和审批绕过；ASB 与 OWASP 为此提供安全风险分类。[R20][R25] 第四层是回归与影子池，用脱敏生产 trace 进行固定重放，防止模型、prompt、工具或运行时升级后发生回退。[R11][R12]

每个任务必须明确初始状态、可用工具、权限边界、成功标准、禁止行为、风险等级、评分器和可复现实验环境。Anthropic 强调任务应无歧义，两个领域专家应能独立得到相同判定；Google 的 Agent evaluation 支持 final response 与 trajectory 指标；OpenAI 的 trace grading 支持按 trace 进行可复现评分。[R11][R12][R13]

### 5.2 评分器组合

程序化 oracle 是高风险任务的第一选择。它适合检查数据库状态、文件内容、API 返回、测试结果、配置变更、工单状态和账务记录，具有确定性、低成本和可复现优势。[R3][R7][R11]

LLM-as-a-Judge 适合评估开放式文本质量、摘要完整性、引用覆盖、对话语气、解释质量和部分轨迹语义，但不应单独裁决法律、金融、医疗、财务或不可逆业务状态。Anthropic 明确区分代码评分器、模型评分器和人类评分器，并强调模型评分器需要人工校准；OpenAI 和 Google 的评估工具也应与确定性状态检查组合使用。[R11][R12][R13]

人工专家评审应集中在高风险、主观性强或 LLM judge 尚未校准的任务上。它不适合替代自动化回归套件，但适合校准评分器、审查边界样本、定义合规 rubrics 和抽检线上 shadow mode。[R11][R19]

### 5.3 多次运行与统计报告

Agent 的非确定性要求关键任务进行多次 trial。pass@k 衡量 k 次尝试中至少一次成功的概率，适合“找到一个可用补丁”这类场景；pass^k 衡量 k 次尝试全部成功的概率，适合客服、财务、合规和运营等每次都必须可靠的场景。Anthropic 用 75% 单次成功率在 3 次试验中只有约 42% 全部成功的例子说明 pass^k 的严苛性，tau-bench 也采用类似可靠性视角。[R7][R11]

企业报告至少应包含 pass@1、pass@k、pass^k、均值、方差、置信区间、失败类型分布、成本分布、p50/p95/p99 时延和恢复成功率。只有成功率而没有方差、成本和失败类型的评估报告，不足以支撑上线决策。[R8][R10][R11]

### 5.4 kill-and-recover 实验

长任务 Agent 必须接受 kill-and-recover 实验。实验流程是：启动 Agent 执行任务并产生文件、工具调用、审批和中间 artifact；在随机步骤终止 harness、worker、runtime 或网络连接；从 event cursor、checkpoint、snapshot、session log 或持久文件系统恢复；验证 workspace checksum、artifact、diff、policy decision、approval 和外部系统状态是否一致；最后检查是否重复执行不可逆工具调用。[R16][R18][R28][R29]

通过标准不是“最终回复看起来完整”，而是“业务状态、证据链、权限链、文件系统和工具副作用一致”。AWS AgentCore 的隔离 session、stop/resume、持久文件系统和长生命周期能力，Anthropic Managed Agents 的 session/harness/sandbox 解耦，为这类实验提供了工程参照。[R16][R18][R28][R29]

### 5.5 多 Agent fan-out 实验

多 Agent 系统不能只报告吞吐提升，还必须评估任务分解、上下文最小化、预算控制、deadline、ack、retry、backpressure、冲突合并、结果裁决和成本放大。Kimi K2.6 Agent Swarm 官方帮助中心把该产品定位为 Beta 水平扩展架构，宣称可协调最多 300 个子 Agent、单任务超过 4,000 次 tool call，并报告约 4.5 倍速度提升；这些数据可以作为 fan-out 产品能力事实，但不能自动推出企业 IAM、policy、audit、runtime isolation 已经完备。[R30]

企业对 swarm 或多 Agent 系统的评估应额外检查：子 Agent 是否获得最小必要上下文，是否重复搜索和写入，是否能追踪每个子任务的证据，是否能回滚局部失败，orchestrator 是否会制造无意义并行，以及并行收益是否超过 token、工具、运行时和人工审核成本。[R8][R10][R30]

### 5.6 安全红队实验

安全红队至少覆盖六类攻击：隐藏在网页、邮件、文档、工单和工具返回中的间接 prompt injection；工具参数注入与 schema 绕过；敏感字段泄漏和数据外发；测试、oracle、缓存和依赖的篡改；诱导 Agent 绕过审批或伪造授权；记忆投毒和过期记忆召回。ASB、OWASP LLM Top 10、OWASP MCP Top 10 与 Berkeley RDI 的 benchmark 安全分析共同支持这些测试方向。[R20][R21][R25][R31]

红队评估必须在工具网关和运行时层强制执行，而不是只依赖提示词。最小权限、审批、隔离、egress policy、secret broker、审计日志和评分 oracle 隔离应成为基础设施能力；这与 NIST AI RMF 的治理思路和 AWS AgentCore Policy 的策略执行方向一致。[R19][R27]

## 6. 产业平台能力比较

### 6.1 比较口径

平台比较必须先定义对象。OpenAI Agents SDK 是代码优先的 Agent 应用 SDK，OpenAI Codex 是面向软件工程任务的 coding agent 产品；Claude Managed Agents 是 Anthropic 托管 harness、session 与 sandbox 的 Claude Agent 运行方式；Google Gemini Enterprise Agent Platform 是包含构建、部署、管理、优化和企业治理的控制面；AWS Bedrock AgentCore 是模型/框架中立的 Agent runtime、memory、gateway、identity、policy、observability、evaluation、registry 等模块化底座；Kimi K2.6 Agent Swarm 是 Beta 产品/模型层 fan-out 能力。[R15][R16][R17][R18][R30][R32]

这些对象不能用“谁最强”直接排序。正确比较方式是看它们分别覆盖了模型接入、编排、运行时、工具、身份、策略、记忆、观测、评估、成本治理和人工协作的哪些部分，以及哪些部分仍需企业自建或外接。[R15][R16][R17][R18][R19]

### 6.2 平台能力矩阵

| 维度 | OpenAI Agents SDK / Codex | Claude Managed Agents | Google Gemini Enterprise Agent Platform | AWS Bedrock AgentCore | Kimi K2.6 Agent Swarm |
| --- | --- | --- | --- | --- | --- |
| 正确定位 | SDK 与 coding agent 产品组合；SDK 提供 agents、tools、handoffs、guardrails、sessions、tracing，Codex 面向代码读写运行和 PR 工作流。[R15][R32] | 托管 Agent 结构，强调 session、harness、sandbox 解耦。[R18] | 企业 Agent 平台，覆盖构建、扩展、管理、优化、Memory Bank、Agent Gateway、Agent Identity、Evaluation 等。[R17][R33] | 框架/模型中立的托管 Agent runtime 与治理底座，包含 Runtime、Memory、Gateway、Identity、Policy、Observability、Evaluation 等能力。[R16][R27] | Beta 水平扩展产品，强调 orchestrator 协调大量子 Agent 并行完成搜索、写作、编程和 Office 任务。[R30] |
| 编排 | handoff、agents-as-tools、AgentKit/Agent Builder、Codex 代码任务流程。[R12][R15][R32] | harness 调用 Claude 并路由工具调用，session 记录事件。[R18] | ADK、Agent Runtime、A2A、Agent Gateway 与企业平台能力组合。[R17][R33] | Runtime 支持多框架，协议支持 MCP/A2A，Gateway 暴露工具。[R16] | orchestrator 指挥子 Agent，强调 PARL 训练和 context sharding。[R30] |
| 执行环境 | Agents SDK 支持 sandbox agents；Codex cloud task 在独立 sandbox/container 中处理代码任务。[R15][R32] | sandbox 作为 Claude 可运行代码和编辑文件的执行环境。[R18] | Agent Runtime、code execution、computer use、Cloud Trace/Logging/Monitoring。[R17] | 每个 session 可运行在独立 microVM，支持长任务、命令执行和持久文件系统。[R16][R28][R29] | 产品内工具、网页、文件、文档、表格、代码和并行子任务能力。[R30] |
| 状态与记忆 | SDK sessions 维护 agent loop 内工作上下文；Codex 以任务 workspace 和 sandbox 为中心。[R15][R32] | session 是 append-only log，承担可恢复上下文存储。[R18] | Sessions 与 Memory Bank 维护会话状态和长期记忆，Memory Bank 支持跨 session 记忆与修订检查。[R17][R26] | Runtime session 保存会话上下文，AgentCore Memory 用于长期上下文；session storage 支持 stop/resume 后文件存续。[R16][R28][R29] | 子 Agent notebook/context sharding，由 orchestrator 汇总结论。[R30] |
| 治理与安全 | guardrails、tool approvals、trace grading、agent safety 指南；企业强权限仍需外部 IAM、网关和审批系统配合。[R12][R15][R34] | auth 可放在 vault 或 sandbox 外部资源边界，具体企业权限需按 Anthropic 文档和集成设计验证。[R18] | Agent Identity、Agent Gateway、IAM Conditions、Semantic Governance、Model Armor 等能力组成治理面。[R17][R33] | Identity、Gateway、Cedar policy、IAM/IdP、isolated sessions 与 observability 形成治理底座。[R16][R27] | 官方帮助中心主要说明 fan-out 与产品使用；企业 IAM、policy、审计和 runtime 隔离不能从 swarm 能力自动推出。[R30] |
| 观测与评估 | trace grading、agent evals、tracing、datasets 和 evals 工具链。[R12][R13][R14][R15] | session log 和 event stream 思路有利于追踪长任务行为。[R18] | Final response evaluation、trajectory evaluation、Cloud Trace、Logging、Monitoring。[R13][R17] | OpenTelemetry/OpenInference/CloudWatch 方向的 Agent observability 与 AgentCore Evaluations。[R16] | 产品进度可视化较强，但企业可复现 trace、policy decision 与 artifact lineage 需外部体系补齐。[R30] |

### 6.3 选型原则

如果目标是快速构建代码优先 Agent 应用，OpenAI Agents SDK、Codex、LangGraph、Temporal、OpenHands 或自建 runtime 的组合更容易贴合研发流程，但企业仍需自建权限、审计、审批和证据保留边界。[R15][R32] 如果目标是降低自建 harness、sandbox 和 session 的工程成本，Claude Managed Agents 的 session/harness/sandbox 解耦提供了直接参考，但它绑定 Anthropic 生态。[R18] 如果企业已经深度使用 Google Cloud 和 Workspace，Gemini Enterprise Agent Platform 的 Agent Identity、Gateway、Memory Bank、Evaluation 与 Observability 更容易接入既有治理面。[R17][R33] 如果企业在 AWS 上追求模型/框架中立、隔离运行和策略治理，Bedrock AgentCore 的 Runtime、Identity、Gateway、Policy 与 Observability 更接近生产底座。[R16][R27] 如果任务主要是大规模搜索、批量资料处理和并行产出，Kimi Agent Swarm 的 fan-out 能力值得实验，但高风险业务自动化仍需外接强治理和审计。[R30]

## 7. AgentRuntimeFabric 的设计启示

### 7.1 定位

AgentRuntimeFabric 不应被定位为另一个 Agent SDK，也不应仅复制单一云厂商平台。更合理的定位是：开源、自托管、模型中立、运行时中立的 Agent 证据与治理控制面，专门处理代码变更、长任务、工具副作用、多 Agent 协作、策略执行、恢复和审计问题。[R10][R12][R16][R18][R19]

这个定位的核心依据是：公开平台已经证明 session、sandbox、gateway、identity、memory、eval 和 observability 是生产级 Agent 的必要方向；开源替代的价值在于把这些能力抽象为可检查 schema、可替换 runtime、可复现实验和不依赖单一云厂商的 EvidenceGraph。[R15][R16][R17][R18]

### 7.2 核心对象模型

| 对象 | 作用 | 必要字段 |
| --- | --- | --- |
| EventLog | 执行事实源，记录所有 task、tool、runtime、approval、artifact、policy decision | event_id、task_id、agent_id、runtime_id、timestamp、input_hash、output_hash、parent_event_id |
| EvidenceGraph | 连接事件、工具调用、diff、snapshot、artifact、审批、身份和 secret grant | node、edge、artifact_hash、policy_version、identity_binding |
| PolicyDecision | 每个高风险动作的版本化授权结果 | subject、action、resource、scope、decision、reason、policy_version、expiry |
| ExecutionLease | 短期执行授权，绑定 agent、tool、runtime、scope 和 deadline | lease_id、allowed_tools、network_scope、filesystem_scope、deadline、revocation_state |
| WorkspaceLineage | 记录 workspace branch、snapshot、merge、rollback 和测试产物 | workspace_id、base_snapshot、current_snapshot、diff_hash、test_artifacts、merge_state |
| RuntimeAdapter | 屏蔽 Docker、gVisor、OpenHands、E2B、Modal、Daytona、AgentCore 或自建 runtime 差异 | runtime_type、capabilities、isolation_level、filesystem_mode、network_policy |
| Artifact | 报告、代码、日志、截图、测试结果和证据包 | artifact_id、type、hash、producer_event、retention_policy、access_policy |

这些对象不是为了形式化而形式化。EventLog 对应 Anthropic transcript/session 与 OpenAI trace 的可审计记录；EvidenceGraph 对应 HAL 对 trace/token 日志与可复现分析的要求；PolicyDecision 和 ExecutionLease 对应 NIST/OWASP/AWS Policy 的治理要求；WorkspaceLineage 对应 SWE-bench、Codex 和 coding agent 对真实代码变更、测试与回滚的需要；RuntimeAdapter 对应 AWS、Anthropic、OpenAI 和 Google 对 sandbox/runtime/session 的生产化方向。[R3][R10][R12][R15][R16][R18][R19][R20][R27]

### 7.3 ARF 评估门禁

AgentRuntimeFabric 的 benchmark 不应只测 Agent 是否完成任务，而应测控制面是否让任务完成得可治理。建议设置七类门禁：

1. **结果门禁**：最终业务状态必须由程序化 oracle 或人工专家验收通过，不能只依据 Agent 自述。[R3][R7][R11]
2. **轨迹门禁**：所有高风险工具调用必须能追溯到输入、参数、身份、权限、审批、工具返回和后续 artifact。[R12][R13][R14]
3. **策略门禁**：越权 shell、MCP、network、secret、Git、PR 和外部通信必须在 policy 层阻断，不能依赖模型自律。[R20][R27][R31]
4. **恢复门禁**：runtime、worker 或 harness 被杀后，必须从 checkpoint、snapshot、session log 或 event cursor 恢复，且不得重复不可逆副作用。[R16][R18][R28][R29]
5. **证据门禁**：报告、代码、日志、截图、测试结果和审批记录必须连接到 EvidenceGraph，满足可复现和可审计要求。[R10][R12][R24]
6. **多 Agent 门禁**：fan-out 必须有预算、deadline、ack、retry、backpressure、冲突合并和子任务证据去重。[R8][R10][R30]
7. **经济门禁**：token、工具调用、runtime minutes、人工审核和失败重试成本必须与 SLA 一起报告。[R8][R10][R24]

### 7.4 开源差异化

闭源平台的优势是托管集成、云原生治理和厂商生态；开源控制面的优势应是透明 schema、自托管部署、跨模型、跨云、跨 runtime 和可检查证据链。AgentRuntimeFabric 如果要形成差异化，应优先实现开放事件协议、policy-bound execution、workspace lineage、runtime adapter contract、benchmark harness、replay runner 和 artifact evidence pack，而不是优先追求更复杂的 Agent 编排语法。[R10][R15][R16][R18][R19]

## 8. 生产级实验方案

### 8.1 四级门禁流程

| 阶段 | 目标 | 必测内容 | 通过条件 |
| --- | --- | --- | --- |
| P0 离线基线 | 验证基本能力 | 公共 benchmark、私有黄金任务、基础工具调用、成本与时延 | 能完成任务，失败可解释，成本可记录。[R8][R10][R11] |
| P1 安全沙箱 | 验证受控执行 | prompt injection、越权工具、secret、网络外发、文件写入、审批绕过 | 高风险动作不能绕过 policy、approval 和隔离边界。[R20][R25][R27] |
| P2 可靠性压测 | 验证生产稳定性 | 多次 trial、并发、长任务、kill-and-recover、重试、恢复、p95/p99 | pass^k、恢复成功率、成本和时延满足 SLA。[R7][R11][R16] |
| P3 影子发布 | 验证真实流量适配 | 脱敏生产 trace 重放、人工对照、线上 shadow mode、A/B 与监控 | 不产生不可逆副作用，人工验收和线上监控达标。[R11][R19] |

### 8.2 最小可行评估套件

最小可行套件应包含 20-50 个真实任务作为起点，覆盖成功场景、拒绝场景、异常场景和高风险场景。Anthropic 指出，早期 Agent 评估不必等待数百个任务才启动；小而清晰的任务集可以快速发现回归与产品需求歧义。[R11]

每个任务至少应包含：任务描述、初始状态、可用工具、权限范围、参考解、成功 oracle、禁止行为、风险等级、预期成本上限、预期时延上限和所需人工校准方式。这个格式与 OpenAI trace grading、Google Agent evaluation 和 Anthropic task/trial/grader/transcript 术语兼容，也方便后续接入 HAL 式 harness。[R10][R11][R12][R13]

### 8.3 报告模板

生产级评估报告应至少输出以下字段：

| 报告字段 | 内容 |
| --- | --- |
| Capability | 每类任务 pass@1、pass@k、partial credit、失败类型 |
| Consistency | pass^k、trial 方差、flake rate、随机种子/温度设置 |
| Trajectory | 工具调用数、工具序列、参数错误、重试、违规路径 |
| Safety | prompt injection 成功率、越权拦截率、secret/PII 泄漏、egress 违规 |
| Recovery | kill-and-recover 成功率、重复副作用、workspace checksum、一致性检查 |
| Economics | token/task、tool calls/task、runtime minutes、人工审核成本、p50/p95/p99 |
| Auditability | trace completeness、artifact lineage、policy decision coverage、replayable ratio |

## 9. 讨论与限制

公开文献提供的是共同方法，而不是企业上线的充分条件。AgentBench、SWE-bench、WebArena、tau-bench、CLEAR 和 HAL 证明了交互环境、状态验证、工具轨迹、成本与可靠性的重要性；但企业仍必须用自身数据、流程、权限、审批和风险容忍度重建私有评估体系。[R1][R3][R4][R7][R8][R10]

平台官方文档提供的是能力边界，而不是业务结果保证。OpenAI、Anthropic、Google、AWS 和 Kimi 的能力各有定位，不能把 SDK 能力等同于企业治理平台，也不能把 fan-out 能力等同于可审计运行时。平台选型必须以任务风险、云生态、团队能力、合规要求和可替换性为约束。[R15][R16][R17][R18][R30][R32]

LLM-as-a-Judge 是必要工具，但不是最终裁判。它能扩展开放式任务评估能力，却必须由程序化 oracle、人工校准和安全门禁约束；否则可能把主观偏好、模型同源偏见和错误解释引入高风险决策。[R11][R12][R13]

## 10. 结论

企业级 Agent 评估的核心不是选择一个更漂亮的排行榜，而是建立一套能够证明“任务完成、路径合规、权限受控、状态一致、失败可恢复、成本可承受、证据可审计”的工程制度。最终结果是底线，轨迹是解释，安全是门禁，可靠性是上线条件，成本是规模化约束，可观测性是持续改进的基础。[R8][R10][R11][R12][R19][R20]

AgentRuntimeFabric 的机会在于把这些原则落实为开放控制面。它应服务于多模型、多框架、多运行时和多工具网关的异构现实，以 EventLog 与 EvidenceGraph 统一证据，以 PolicyDecision 与 ExecutionLease 约束动作，以 WorkspaceLineage 与 RuntimeAdapter 支撑恢复，以 benchmark harness 和 replay runner 实现可复现实验。只有这样，AgentRuntimeFabric 才能从“运行 Agent”提升为“治理 Agent 的运行”。[R10][R12][R16][R18][R27]

## 参考文献

[R1] AgentBench: Evaluating LLMs as Agents. https://arxiv.org/abs/2308.03688
[R2] GAIA: A Benchmark for General AI Assistants. https://arxiv.org/abs/2311.12983
[R3] SWE-bench: Can Language Models Resolve Real-World GitHub Issues? https://arxiv.org/abs/2310.06770 and https://www.swebench.com/SWE-bench/
[R4] WebArena: A Realistic Web Environment for Building Autonomous Agents. https://openreview.net/forum?id=oKn9c6ytLx and https://webarena.dev/
[R5] OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments. https://arxiv.org/abs/2404.07972
[R6] WorkArena: Benchmarking Agents for Enterprise Workflow Automation. https://arxiv.org/abs/2403.07718
[R7] tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains. https://arxiv.org/abs/2406.12045
[R8] Beyond Accuracy: A Multi-Dimensional Framework for Evaluating Enterprise Agentic AI Systems / CLEAR. https://arxiv.org/abs/2511.14136
[R9] TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks. https://arxiv.org/abs/2412.14161
[R10] Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation. https://arxiv.org/abs/2510.11977
[R11] Anthropic, Demystifying evals for AI agents. https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
[R12] OpenAI, Trace grading. https://developers.openai.com/api/docs/guides/trace-grading
[R13] Google Cloud, Evaluate Gen AI agents. https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-agents
[R14] OpenAI, Evaluate agent workflows. https://developers.openai.com/api/docs/guides/agent-evals
[R15] OpenAI Agents SDK. https://openai.github.io/openai-agents-python/
[R16] AWS, Host agent or tools with Amazon Bedrock AgentCore Runtime. https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html
[R17] Google Cloud, Gemini Enterprise Agent Platform overview and scale documentation. https://docs.cloud.google.com/gemini-enterprise-agent-platform/overview and https://docs.cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview
[R18] Anthropic, Scaling Managed Agents: Decoupling the brain from the hands. https://www.anthropic.com/engineering/managed-agents
[R19] NIST AI Risk Management Framework. https://www.nist.gov/itl/ai-risk-management-framework
[R20] OWASP Top 10 for Large Language Model Applications. https://owasp.org/www-project-top-10-for-large-language-model-applications/
[R21] Berkeley RDI, How We Broke Top AI Agent Benchmarks: And What Comes Next. https://rdi.berkeley.edu/blog/trustworthy-benchmarks-cont/
[R22] Survey on Evaluation of LLM-based Agents. https://arxiv.org/abs/2503.16416
[R23] AI Agents That Matter. https://arxiv.org/abs/2407.01502
[R24] HAL official site. https://hal.cs.princeton.edu/about
[R25] Agent Security Bench: Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents. https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf
[R26] Google Cloud, Vertex AI Agent Engine Memory Bank. https://docs.cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/memory-bank/overview
[R27] AWS, Amazon Bedrock AgentCore Policy. https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html
[R28] AWS, Use isolated sessions for agents. https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-sessions.html
[R29] AWS, File system configurations for AgentCore Runtime. https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-filesystem-configurations.html
[R30] Kimi Help Center, K2.6 Agent Swarm [Beta]. https://www.kimi.com/help/agent/agent-swarm
[R31] OWASP MCP Top 10. https://owasp.org/www-project-mcp-top-10/
[R32] OpenAI Codex documentation. https://developers.openai.com/codex/cloud
[R33] Google Cloud, Gemini Enterprise Agent Gateway overview. https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/gateways/agent-gateway-overview
[R34] OpenAI, Safety in building agents. https://developers.openai.com/api/docs/guides/agent-builder-safety
