# 企业级 Agent 系统评估研究报告

截至日期：2026-05-08

## 修订说明

本报告用于合并并重写两份企业级 Agent 评估草稿：`enterprise_agent_bench_report_ch1.md` 与 `enterprise_agent_bench_report_ch2.md`。参考基线为 `Agent-Platform-Bench-v1.md` 中的评估文献清单，并结合当前仓库中的平台研究材料与公开官方/学术资料进行事实校验。

修订原则如下：

1. 保留“Agent 评估必须从最终答案扩展到轨迹、状态、工具、成本、安全、可靠性”的核心判断。
2. 修正“抛弃结果”这类过度表述：最终结果仍是必要指标，但不能作为唯一指标。
3. 区分模型、Agent scaffold、运行时、工具网关、企业平台和完整业务系统，避免把不同抽象层混为一类。
4. 删除无关引用和未证实断言；对官方文档、论文、产品帮助、媒体文章和推断性分析分层标注。
5. 把平台横向比较纳入评估方法论，而不是把平台介绍与评估框架平行堆叠。

## 结论先行

企业级 Agent 系统的评估对象不是一个静态模型，而是一个会规划、调用工具、读写状态、承担外部副作用、与人和其他系统协作的运行系统。因此，传统只看单次最终答案或单一成功率的评估方式不够用。更合理的结论不是“抛弃结果”，而是：

> 企业级 Agent 评估必须以最终业务状态为底线，以执行轨迹为解释，以成本和时延为约束，以安全治理为门禁，以多次运行可靠性和恢复能力为上线条件。

从学术界看，AgentBench、WebArena、SWE-bench、OSWorld、WorkArena、tau-bench、TheAgentCompany、CLEAR 和 HAL 等基准共同推动了评估范式变化：从静态答题转向交互式环境、真实工具、状态变更、可复现执行、成本可见和轨迹分析。从产业界看，Anthropic、OpenAI、Google Cloud、AWS、Kimi 等平台都在把 trace、session、sandbox、gateway、identity、policy、memory、eval 等能力产品化。但这些平台不是同一类对象，不能直接用“谁是最强企业 Agent 平台”一类笼统结论覆盖。

企业落地时最重要的不是排行榜总分，而是回答五个问题：

1. 这个 Agent 是否把真实业务状态改对了？
2. 它是否用合规、可解释、可审计的路径完成？
3. 它在多次运行、异常、重试、恢复和环境变化下是否稳定？
4. 它的成本、时延和运维复杂度是否落在业务 SLA 内？
5. 当它不确定、越权或高风险时，是否能停止、升级给人并保留完整上下文？

## 1. 研究范围与证据等级

### 1.1 评估对象分层

企业级 Agent 评估首先要界定对象。不同对象对应不同指标，混用会导致错误结论。

| 层级 | 评估对象 | 典型问题 | 主要指标 |
| --- | --- | --- | --- |
| 模型层 | LLM/VLM 本身 | 能否推理、编码、理解指令、调用工具格式 | pass@1、准确率、工具调用格式、推理质量、幻觉率 |
| Agent scaffold 层 | ReAct、Plan-Execute、LangGraph、Agents SDK 等 | 能否组织多步动作和工具循环 | 轨迹正确性、重规划、停止条件、工具选择、错误处理 |
| 运行时层 | sandbox、browser、shell、code interpreter、microVM | 能否安全执行外部动作 | 隔离强度、冷启动、执行时延、文件/网络边界、快照/恢复 |
| 工具网关层 | MCP、OpenAPI gateway、AgentCore Gateway、内部 API gateway | 能否把工具安全暴露给 Agent | 参数校验、身份传递、策略执行、审计、限流、重试 |
| 企业平台层 | Gemini Enterprise、Bedrock AgentCore、Claude Managed Agents 等 | 能否统一部署、身份、策略、观测、评测、注册 | lifecycle、registry、policy、memory、trace、eval、成本治理 |
| 业务系统层 | 完整客服、研发、财务、合规、运营流程 | 是否产生真实业务价值且风险可控 | 业务状态正确率、人工返工率、事故率、SLA、ROI |

### 1.2 证据等级

| 等级 | 来源类型 | 使用方式 |
| --- | --- | --- |
| A | 官方文档、官方工程博客、官方帮助中心、正式 API 文档 | 可作为平台能力事实，但仍要区分 GA/Beta/Preview |
| B | arXiv/OpenReview/会议论文、官方 benchmark 网站、开源仓库 | 可作为研究事实和方法论依据，但需说明是否经过同行评审 |
| C | 云厂商博客、技术媒体、社区实践、第三方报告 | 可作为补充案例，不能单独支撑强结论 |
| D | 推断、架构类比、经验总结 | 必须明确标注为分析判断，不能写成产品事实 |

本报告采用 A/B 级来源作为主证据。C/D 级内容只用于解释趋势或提出实验建议。

## 2. 为什么传统评估不够用

### 2.1 最终答案不能解释执行风险

LLM 时代的静态评估通常面对的是“输入问题，输出答案”。Agent 系统面对的是“目标、环境、工具、状态、权限和人机协作”。一个 Agent 可能最终给出看似正确的回复，但中间步骤存在严重问题：

- 调用了错误数据源，只是碰巧得到同样结果。
- 用了过期报表、缓存数据或未授权 API。
- 漏掉了必要审批，却在最终回复中声称任务完成。
- 在多 Agent 协作中重复执行、覆盖他人修改或合并冲突。
- 在工具失败后伪造成功，而不是分类错误并恢复。

因此，最终结果是必要但不充分的。企业评估必须把最终状态、执行轨迹和副作用一起看。

### 2.2 Agent 评估必须处理非确定性

同一模型、同一任务、同一 scaffold 在不同试次中可能产生不同计划、工具序列和中间状态。单次运行不能代表可靠性。Anthropic 的 agent eval 指南把 task、trial、grader、transcript/trajectory 明确拆开，强调对 Agent 需要多任务、多试次、带工具和环境状态的评估。OpenAI 的 trace grading 也将 trace 定义为端到端决策、工具调用和推理步骤日志，用于定位 workflow 级错误。

因此，企业评估至少要报告：

- pass@1、pass@k 和多次运行方差。
- 平均工具调用次数、失败率、重试率。
- token、工具、运行时和人工审核成本。
- p50/p95/p99 任务耗时。
- 失败类型分布和恢复成功率。

### 2.3 轨迹评估不是替代结果评估

源稿中“抛弃结果，追踪轨迹，溯源决策”的说法方向正确但措辞过强。更准确的框架是三层校验：

1. **结果校验**：最终业务状态是否正确，例如订单是否创建、补丁是否通过测试、工单是否被正确流转。
2. **轨迹校验**：是否用了正确工具、正确参数、正确权限、正确顺序，是否遵守审批和业务规则。
3. **恢复校验**：工具报错、网络中断、runtime 死亡、上下文过长、用户纠错后能否恢复并保留审计证据。

结果决定是否完成任务；轨迹解释为什么可信；恢复能力决定能否生产化。

## 3. 学术界与基准研究基线

### 3.1 代表性基准

| 基准/论文 | 主要对象 | 贡献 | 企业评估启示 |
| --- | --- | --- | --- |
| AgentBench | LLM-as-Agent | 多环境交互式评估，覆盖 web、游戏、数据库、操作系统等 | Agent 要放进环境中测，不只测文本 |
| GAIA | 通用助手 | 真实世界信息整合、工具使用、多步任务 | 更接近知识工作任务，但仍需企业权限和状态建模 |
| WebArena | Web Agent | 高保真网站环境，评估网页导航和状态变更 | 浏览器 Agent 要验证后端状态，不只看页面文本 |
| SWE-bench | Coding Agent | 真实 GitHub issue、仓库级修复、测试验证 | 软件工程评估必须包含真实代码库、测试和回归风险 |
| OSWorld | Computer-use Agent | 真实桌面/操作系统任务 | GUI Agent 要检查文件、应用配置和系统状态 |
| WorkArena | 企业 SaaS 工作流 | 基于 ServiceNow 的知识工作任务 | 企业任务需要流程、票据、角色和系统状态 |
| tau-bench | 工具-用户交互 | 多轮用户模拟、工具调用和规则遵循 | API Agent 应用最终数据库状态和 policy compliance 评分 |
| TheAgentCompany | 数字员工 | 模拟真实公司工作环境中的多类任务 | 衡量 Agent 对企业工作流的端到端参与能力 |
| CLEAR | 企业多维评估 | Cost、Latency、Efficacy、Assurance、Reliability | 成本、安全、可靠性必须进入主评分 |
| HAL | 评估基础设施 | 标准 harness、成本控制、跨 benchmark、日志共享 | 评估本身要可复现、可比较、可审计 |

这些基准的共同趋势是：Agent 评估从“模型答题”转向“系统行为”。但是任何单个公开基准都不能直接代表企业生产就绪度。企业必须把公共基准、私有任务集、红队攻击、长任务恢复和上线门禁组合起来。

### 3.2 CLEAR 的正确使用方式

CLEAR 论文提出 Cost、Latency、Efficacy、Assurance、Reliability 五维框架，适合纠正企业只看准确率的倾向。源稿中把 CLEAR 描述为“权威标准”并直接绑定生产成功率，这种表达应收敛为：

- CLEAR 是一个有价值的多维评估框架，不是所有行业的唯一标准。
- 其 300 任务企业套件和相关性结论应按论文边界理解，不能泛化到所有企业、所有行业和所有平台。
- CLEAR 的核心价值在于提醒企业同时看成本、时延、效能、保障和可靠性，而不是追求单点 accuracy。

### 3.3 HAL 的正确使用方式

HAL 关注 Agent 评估基础设施：统一 harness、成本控制、跨 benchmark 比较、trace/token 日志和可复现性。源稿中关于 HAL 的方向基本成立，但应避免“全链路基础设施革命”这类宣传化措辞。

HAL 对企业最重要的启发是：

- 同一模型在不同 scaffold 下表现差异很大，模型榜单不能替代系统评估。
- 成本必须与性能一起报告，否则 1 个百分点的提升可能隐藏不可接受的成本放大。
- trace 和 token 日志是失败归因、污染分析和复现实验的基础。
- 评估 harness 不能强制所有 Agent 采用同一框架，但必须捕获可比较的行为证据。

### 3.4 SWE-bench、WebArena 与安全边界

SWE-bench 对代码 Agent 很重要，但不能被解释为“真实企业软件工程能力”的完整代理。它主要衡量 issue 修复和测试通过，不能覆盖需求澄清、架构评审、变更审批、部署回滚、数据迁移、供应链安全和长期维护。

WebArena、OSWorld 等交互环境揭示了 Agent 在真实界面中的能力限制，但它们不是企业治理基准。企业必须额外评估身份、权限、敏感数据、不可逆副作用和审计。

源稿中“SWE-bench 容器 100% 可被利用”的表述应删除。更严谨的说法是：已有研究和安全实践表明，代码评测环境可能被对抗性补丁、测试篡改、依赖注入、配置覆盖等方式攻击，因此代码 Agent benchmark 需要加入评测沙箱加固、测试完整性校验和补丁审查。

## 4. 企业级 Agent 指标体系

### 4.1 一级指标

| 一级指标 | 核心问题 | 示例度量 |
| --- | --- | --- |
| 任务效能 | 是否完成业务目标 | task success、partial credit、最终状态正确率、人工验收率 |
| 轨迹正确性 | 是否以正确方式完成 | 工具序列匹配、参数正确率、状态读取正确率、证据引用完整率 |
| 工具与执行 | 是否能稳定使用外部系统 | tool call success、schema violation、retry rate、timeout rate |
| 状态与记忆 | 是否维护正确上下文 | session consistency、memory retrieval precision、workspace checksum |
| 安全与治理 | 是否遵守权限和策略 | policy violation、approval bypass、secret leak、egress violation |
| 可靠性 | 多次运行是否稳定 | pass@k、variance、flake rate、恢复成功率 |
| 成本与时延 | 是否可规模化运行 | token/task、tool calls/task、runtime minutes、p95 latency、idle cost |
| 人机协作 | 是否知道何时升级 | handoff precision、handoff latency、handoff context completeness |
| 可观测审计 | 是否可解释和追责 | trace completeness、event coverage、artifact lineage、replayable ratio |

### 4.2 二级指标设计

**任务效能**

- 最终数据库、文件、工单、PR、报表等业务状态是否正确。
- 输出是否满足格式、引用、完整性和业务约束。
- 是否破坏无关状态，例如误改不相关文件或错误关闭工单。

**轨迹正确性**

- 是否在需要澄清时主动询问，而不是猜测。
- 是否先读取必要信息再执行写操作。
- 是否使用了授权工具和正确参数。
- 是否正确解析工具返回的结构化数据。
- 是否在失败时分类错误并选择合理恢复策略。

**治理与安全**

- 高风险动作是否触发审批。
- secret 是否只在 broker/proxy 边界使用，未进入模型上下文、日志和工作区。
- 数据外发是否经过 egress policy。
- 权限是否绑定 user/agent/tool/runtime 身份，而不是依赖提示词。

**生产可靠性**

- runtime 被杀后是否能从 event cursor、checkpoint 和 filesystem snapshot 恢复。
- 长任务是否能 pause/resume，不占用不必要计算资源。
- 多 Agent fan-out 是否有预算上限、deadline、ack、retry、backpressure。
- 失败后是否产生可操作的诊断证据。

## 5. 评估方法论

### 5.1 任务集构建

企业任务集不应只从公开 benchmark 复制。推荐四层任务池：

| 任务池 | 用途 | 示例 |
| --- | --- | --- |
| 公共基准池 | 横向比较模型/scaffold 基线 | SWE-bench、WebArena、OSWorld、tau-bench |
| 私有黄金任务池 | 对齐自身业务流程 | 客服退款、CRM 更新、财务报表、代码迁移、工单流转 |
| 对抗与异常池 | 暴露安全和恢复问题 | prompt injection、越权工具、网络失败、脏数据、权限冲突 |
| 回归与线上影子池 | 防止版本回退 | 从生产 trace 脱敏抽样，固定重放 |

每个任务应明确：

- 初始状态：数据库、文件、账号、权限、外部系统模拟。
- 可用工具：名称、schema、权限、速率限制。
- 成功标准：最终状态、轨迹要求、禁止行为。
- 风险等级：只读、可逆写、不可逆写、外部通信、财务/合规。
- 评分器：程序化检查、人工审核、LLM judge、状态 oracle。

### 5.2 评分方式

推荐采用多维评分，而不是单一总分：

| 分数 | 说明 |
| --- | --- |
| Outcome Score | 最终业务状态正确性 |
| Trajectory Score | 工具、顺序、参数、证据和策略路径正确性 |
| Safety Score | 权限、审批、数据边界、注入防护和拒绝能力 |
| Reliability Score | 多次运行方差、恢复、重试和长任务稳定性 |
| Economic Score | 成本、时延、资源占用与 SLA 符合度 |
| Operability Score | trace、日志、artifact、诊断和人工修复能力 |

总分只能用于粗略排序，不能替代维度分解。上线决策应采用门禁式规则：任何高风险安全或审计失败都不能被高准确率抵消。

### 5.3 LLM-as-a-Judge 的边界

LLM judge 适合评估开放式文本质量、覆盖度、语气、部分轨迹解释，但不应单独裁决高风险业务状态。更稳妥的组合是：

- 程序化 oracle 检查数据库、文件、API 状态。
- 静态分析检查代码、配置、安全策略。
- LLM judge 辅助总结失败原因和主观质量。
- 人工抽检校准 LLM judge，尤其是合规、法律、财务和医疗场景。

### 5.4 多次运行与统计

每个关键任务至少运行多次，报告：

- pass@1 与 pass@k。
- 均值、方差和置信区间。
- 失败类型分布。
- 成功路径多样性。
- 成本和时延分布。

如果一个 Agent 单次成功率高但方差大，企业上线风险仍然很高。

## 6. 产业平台横向比较

### 6.1 平台不是同一类对象

| 对象 | 正确定位 | 不应误解为 |
| --- | --- | --- |
| OpenAI Agents SDK | 代码优先 Agent 应用 SDK，提供 agent、tools、handoffs、guardrails、sessions、tracing | 完整企业 Agent PaaS |
| OpenAI Codex | 面向代码任务的 coding agent 产品和工作流 | 通用企业治理平台 |
| Claude Managed Agents | Anthropic 托管 harness、environment、session、events、tools 的 Claude Agent API | 多云模型中立平台 |
| Google Gemini Enterprise / ADK / Agent Runtime | 企业 Agent 开发、部署、身份、网关、记忆、观测、评估体系；ADK 是开发框架 | 单一 SDK 或完全云无关平台 |
| AWS Bedrock AgentCore | 模型/框架中立的托管 runtime、memory、gateway、identity、policy、observability、evaluation、registry | Agent 编排框架本身 |
| Kimi K2.6 Agent Swarm | 产品/模型层并行 Agent 模式，强调大规模 fan-out | 企业 IAM/policy/audit/runtime 治理平台 |

### 6.2 平台能力矩阵

| 维度 | OpenAI Agents SDK/Codex | Claude Managed Agents | Google Gemini Enterprise/ADK | AWS Bedrock AgentCore | Kimi Agent Swarm |
| --- | --- | --- | --- | --- | --- |
| 编排 | SDK handoff、agents-as-tools、Agent Builder/Codex 工作流 | 托管 harness，支持多 agent session | ADK + Agent Runtime + A2A/Agent Platform | 框架中立 runtime，可承载多框架 | 模型/产品内置 orchestrator |
| 执行环境 | Codex/sandbox agents、代码和文件工作区 | 托管环境、sandbox、MCP/custom tools | Agent Engine code execution、connectors、runtime | microVM、Code Interpreter、Browser、Gateway | 产品内工具、文件、网页、代码、Office |
| 状态/记忆 | SDK sessions、Codex 会话/工作区 | session event log、filesystem/environment | Sessions、Memory Bank、RAG/Example Store | Runtime session、Memory、persistent filesystem | 子 Agent notebook/context sharding |
| 治理 | guardrails、approval/sandbox 需结合产品与外部系统 | permission policies、vault/proxy 思路 | IAM、Agent Identity、Gateway、Model Armor、Semantic Governance | Identity、Cedar Policy、Gateway、Registry、IAM/IdP | 产品权限和配额为主 |
| 观测/评估 | tracing、trace grading、evals | Console trace/usage、event stream | Cloud Trace/Logging/Monitoring、Evaluation | OTEL/OpenInference/CloudWatch、Evaluations | 产品任务可视化，企业审计较弱 |
| 最适合 | 自建可控 Agent 应用、代码自动化 | Claude 长任务、免自建 harness/sandbox | Google Cloud/Workspace 企业控制面 | AWS 合规环境、框架中立生产化 | 广域搜索、批量处理、并行产出 |
| 主要限制 | 企业治理需自建或外接 | 绑定 Claude/API 生态，Beta 边界需关注 | 云生态绑定和平台复杂度 | AWS/IAM/网络配置复杂 | 黑盒 fan-out、治理能力不足 |

## 7. 各平台评估口径修正

### 7.1 OpenAI Agents SDK + Codex

OpenAI Agents SDK 可作为 Agent 应用开发框架评估，不应写成完整企业 PaaS。官方文档支持的核心事实包括：工具、handoff、guardrail、session 和 tracing。OpenAI 的 trace grading 文档明确把 trace 作为端到端决策和工具调用日志来评分，这与企业轨迹评估方向一致。

需要修正的源稿问题：

- 删除“SDK 内部守护进程捕获内存变量二进制快照”等未证实实现细节。
- 不把 tracing 等同于完整审计。审计还需要身份、权限、审批、artifact lineage、不可抵赖事件和保留策略。
- 不把 guardrails 写成强制权限控制。工具前后的 guardrail 是重要钩子，但企业权限应在 tool gateway、runtime、lease 和 policy 边界强制执行。

评估重点：

- handoff 是否保留必要上下文并避免重复/丢失。
- tool guardrail 是否覆盖每次高风险工具调用。
- session 是否只是对话记忆，还是与业务状态一致。
- Codex 生成的 diff 是否可测试、可回滚、可审计。

### 7.2 Claude Managed Agents

Anthropic 官方工程文章明确提出 brain、hands、session 解耦：harness、sandbox/tools、session log 可独立失败和替换；session 作为上下文窗口外的持久事件日志；凭证通过 vault/proxy 等方式避免进入 sandbox。这些事实可以保留。

需要修正的源稿问题：

- “毫秒级拉起”不应作为事实写入，除非有明确来源。
- p50/p95 TTFT 降低可引用 Anthropic 官方工程文章中的相对改善，但不要扩展为所有场景性能承诺。
- 定价、会话小时费用、Beta 状态必须以官方文档为准，并标注时间。
- 不把 Managed Agents 写成多云、模型中立、通用治理平台。

评估重点：

- session event log 是否能支持中断恢复和审计。
- sandbox 与 credential vault/proxy 的边界是否能通过红队测试。
- permission policy 是否覆盖 shell、network、file、MCP/custom tools。
- 长任务是否能在 harness 和 hand 失败后恢复。

### 7.3 Google Gemini Enterprise / ADK / Agent Runtime

Google 的相关能力应分层描述：ADK 是开发框架；Agent Engine/Agent Runtime 是运行与生产承载；Gemini Enterprise 是企业入口和控制面；Agent Gateway、Agent Identity、Memory Bank、Evaluation、Observability 是平台能力。不要把这些写成一个单一 SDK。

需要修正的源稿问题：

- “成百上千微型智能体全连接通信”属于推断，不应写成官方事实。
- A2A 是互操作协议和协作边界，不等于天然正确的多 Agent 协同。
- 低代码 Agent Studio、ADK、Agent Runtime、Gemini Enterprise 的目标用户和部署边界需要分开。

评估重点：

- Agent Identity 是否能覆盖 agent、tool、service account 和用户委托。
- Agent Gateway 是否能统一 MCP/A2A/REST/gRPC 出入站策略。
- Memory Bank 是否可撤销、纠错、隔离和版本化。
- Evaluation 是否支持 final response 和 trajectory 两类评估。

### 7.4 AWS Bedrock AgentCore

AWS AgentCore 更接近企业生产底座：Runtime、Memory、Gateway、Identity、Policy、Observability、Evaluations、Registry、Browser、Code Interpreter 等是模块化能力。官方文档支持 microVM session isolation、最多 8 小时生命周期、MCP/A2A 支持、persistent filesystem、Cedar policy 等事实。

需要修正的源稿问题：

- 不把 AgentCore 写成 Agent 框架本身。
- “唯一正规解法”“坚不可摧”“不损耗执行性能”等营销化表述应删除。
- VPC/PrivateLink/ENI 能力要按具体 Gateway/Runtime 文档描述，不泛化到所有部署模式。

评估重点：

- policy 是否默认 deny、forbid wins，并覆盖每次 tool invocation。
- microVM session stop/resume 后文件系统、上下文和身份是否一致。
- Gateway 是否把内部 API 安全转换为 MCP 工具并保留审计。
- OTEL/OpenInference/CloudWatch trace 是否能连接到业务 artifact 和审批记录。

### 7.5 Kimi K2.6 Agent Swarm

Kimi 官方帮助中心支持以下表述：K2.6 Agent Swarm 是 Beta，面向水平扩展，可协调最多 300 个子 Agent，单任务超过 4,000 次 tool calls，官方宣称相对单 Agent 顺序执行约 4.5 倍速度提升，并使用 PARL 训练 orchestrator。它适合广域搜索、批量处理、长文档、长文写作、复杂编程和 Office 自动化。

需要修正的源稿问题：

- 不把 Kimi Swarm 写成企业运行时治理平台。
- 不把官方产品帮助中的 fan-out 能力扩展为 IAM、policy、audit、runtime isolation 能力。
- 删除“1500 次并发工具调用”等未证实数字。
- K2.5/K2.6 参数、视觉编码器、内部实现等强断言必须只按官方模型卡或帮助文档写。

评估重点：

- 大规模 fan-out 是否真的降低关键路径，还是只放大成本和重复劳动。
- 子 Agent 任务是否可审计、可去重、可合并、可回滚。
- orchestrator 是否会产生无意义并行或串行退化。
- Beta 产品的可用性、配额、失败率和数据边界是否满足企业要求。

## 8. 生产级评估实验设计

### 8.1 从 PoC 到上线的四级门禁

| 阶段 | 目标 | 必测内容 | 通过条件 |
| --- | --- | --- | --- |
| P0 离线基线 | 验证基本可行 | 公共 benchmark、私有黄金任务、基础工具调用 | 任务可完成，失败可解释 |
| P1 安全沙箱 | 验证受控执行 | prompt injection、越权工具、secret、网络外发、文件写入 | 高风险动作不能绕过 policy/approval |
| P2 可靠性压测 | 验证生产稳定性 | 多次运行、并发、长任务、kill-and-recover、重试、恢复 | 可靠性、成本、p95 时延满足 SLA |
| P3 影子发布 | 验证真实流量适配 | 脱敏生产 trace 重放、人工对照、线上 shadow mode | 不产生不可逆副作用，人工验收达标 |

### 8.2 必须增加的 kill-and-recover 实验

企业级 Agent 与普通聊天机器人的关键差别是长任务和外部状态。上线前必须做真实恢复实验：

1. Agent 开始执行任务并产生文件、工具调用和中间 artifact。
2. 在随机步骤杀掉 harness、worker 或 runtime。
3. 从 event cursor、checkpoint、snapshot 或 session log 恢复。
4. 验证 workspace checksum、artifact、diff、policy decision、approval 关系是否完整。
5. 检查恢复后是否重复执行不可逆工具调用。

通过条件不是“Agent 最终答复看起来完整”，而是“状态、证据和权限链一致，且没有重复副作用”。

### 8.3 多 Agent fan-out 实验

对多 Agent 系统不能只看吞吐提升，还要测：

- 子任务划分是否覆盖目标且不重复。
- 子 Agent 是否拿到最小必要上下文。
- 预算、deadline、ack、retry 是否可控。
- 冲突合并和裁决是否正确。
- 失败的子 Agent 是否影响全局结果。
- 并行带来的成本放大是否小于业务收益。

### 8.4 安全红队实验

至少覆盖：

- 隐藏在网页、文档、邮件、工单里的 prompt injection。
- 工具参数注入和 schema 绕过。
- 数据外发与敏感字段泄漏。
- 修改测试、篡改评估 oracle、污染缓存。
- 诱导 Agent 绕过审批或伪造已获批准。
- 记忆投毒和过期记忆召回。

## 9. 企业选型建议

### 9.1 按场景选型

| 场景 | 更合适的路线 | 原因 |
| --- | --- | --- |
| 内部工程自动化、代码修改、CI 辅助 | OpenAI Agents SDK/Codex、自建 runtime、OpenHands/Temporal/LangGraph 组合 | 控制度高，便于集成现有研发流程 |
| Claude 长任务和文档/代码异步处理 | Claude Managed Agents | 少建 harness/sandbox/session 基础设施 |
| 已深度使用 Google Cloud/Workspace 的企业 | Gemini Enterprise/ADK/Agent Runtime | 与 IAM、数据、办公套件和 Google Cloud 观测治理集成 |
| 高合规 AWS 企业、需要模型/框架中立 | AWS Bedrock AgentCore | runtime、identity、gateway、policy、observability 模块完整 |
| 大规模搜索、批量资料处理、并行产出 | Kimi Agent Swarm | fan-out 效率强，但需外接治理和审计 |
| 自建开源替代/强可控平台 | AgentRuntimeFabric 类开放控制面 | 需要统一证据、策略、workspace lineage 和多后端 runtime |

### 9.2 按组织能力选型

- 如果团队缺少平台工程能力，应优先使用托管平台，但接受供应商绑定和可审计边界限制。
- 如果团队有强 DevOps/SRE/安全能力，可以自建 Agent control plane，换取模型/云/运行时中立。
- 如果业务涉及不可逆写操作，必须选择能在工具网关和 runtime 层强制 policy 的方案。
- 如果任务主要是批量研究和文档产出，可以接受更黑盒的 swarm 产品，但不要把它用于高风险自动审批流程。

## 10. 对 AgentRuntimeFabric 的启发

AgentRuntimeFabric 不应把自己定位成另一个 agent SDK，也不应只复制某个云平台。更清晰的定位是：

> 一个开源、自托管、模型和运行时中立的 Agent 证据与治理控制面，专门解决代码变更、长任务、工具副作用、多 Agent 协作和恢复审计问题。

### 10.1 必须沉淀的核心对象

| 对象 | 作用 |
| --- | --- |
| EventLog | 执行事实源，记录 task、tool、runtime、approval、artifact、policy decision |
| EvidenceGraph | 连接事件、工具调用、diff、snapshot、artifact、审批、身份、secret grant |
| PolicyDecision | 每个高风险动作的版本化授权结果 |
| ExecutionLease | 短期执行授权，绑定 agent、tool、runtime、scope、deadline |
| WorkspaceLineage | 记录 workspace branch、snapshot、merge、rollback 和测试产物 |
| RuntimeAdapter | 隔离 Docker/gVisor/OpenHands/E2B/Modal/Daytona/AWS/自建 runtime 的差异 |
| Artifact | 报告、代码、日志、截图、测试结果和证据包 |

### 10.2 ARF 评估门禁

ARF 的 benchmark 不应只测“Agent 会不会做任务”，而要测：

- sandbox 被杀后能否恢复。
- policy 是否能阻止越权 shell/MCP/network/secret/Git/PR 操作。
- 所有 artifact 是否能追溯到 tool call、runtime、身份和审批。
- 多 Agent 分支是否能合并、冲突检测和回滚。
- trace 是否只是观测数据，还是能与 EventLog/EvidenceGraph 对齐。
- 同一任务在不同 runtime backend 下是否保持语义一致。

### 10.3 开源替代的差异化

闭源平台已经验证了 session、sandbox、gateway、identity、memory、eval 的方向。开源替代的价值不在于声称“独有能力”，而在于提供：

- 开放 schema 和可检查事件。
- 可自托管的控制面。
- 可替换 runtime 和模型。
- 不依赖单一云厂商的 EvidenceGraph。
- 面向代码变更和企业副作用的 policy-bound execution。
- 可复现实验和 contract tests。

## 11. 源稿主要修正清单

| 源稿问题 | 修正方式 |
| --- | --- |
| “抛弃结果，追踪轨迹” | 改为“结果必要但不充分，必须叠加轨迹、状态、安全、成本和恢复评估” |
| CLEAR/HAL 被写成唯一权威 | 改为“重要研究框架/基础设施，按论文边界使用” |
| 平台能力与评估方法混杂 | 改为“先定义评估对象和指标，再横向比较平台支持度” |
| OpenAI Agents SDK 被写成完整 PaaS | 改为“开发框架 + Codex coding agent 产品组合” |
| Claude Managed Agents 被泛化为多云治理平台 | 改为“Anthropic 托管 Claude Agent harness/environment/session API” |
| Google ADK/Gemini/Agent Runtime 混写 | 改为分层描述开发框架、运行时、企业控制面 |
| AWS AgentCore 被写成 Agent 框架 | 改为“模型/框架中立的托管运行和治理底座” |
| Kimi Swarm 被写成企业治理平台 | 改为“Beta 产品/模型层 fan-out 能力，治理需另建” |
| SWE-bench “100% 可利用” | 改为“已有研究提示评测环境存在对抗风险，需要沙箱和 oracle 加固” |
| 无关 Google Patent 引用 | 删除 |
| “唯一正规解法”“坚不可摧”“降维打击”等话术 | 删除或改为证据边界内的中性表述 |

## 12. 参考来源

### 12.1 Agent 评估与基准

- Survey on Evaluation of LLM-based Agents: https://arxiv.org/abs/2503.16416
- AI Agents That Matter: https://arxiv.org/abs/2407.01502
- AgentBench: https://arxiv.org/abs/2308.03688
- GAIA: https://arxiv.org/abs/2311.12983
- WebArena: https://openreview.net/forum?id=oKn9c6ytLx
- SWE-bench: https://www.swebench.com/SWE-bench/
- OSWorld: https://arxiv.org/abs/2404.07972
- WorkArena: https://arxiv.org/abs/2403.07718
- tau-bench: https://arxiv.org/abs/2406.12045
- TheAgentCompany: https://arxiv.org/abs/2412.14161
- CLEAR / Beyond Accuracy: https://arxiv.org/abs/2511.14136
- HAL: https://arxiv.org/abs/2510.11977
- HAL official site: https://hal.cs.princeton.edu/about

### 12.2 产业评估方法

- Anthropic, Demystifying evals for AI agents: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Google Cloud, A methodical approach to agent evaluation: https://cloud.google.com/blog/topics/developers-practitioners/a-methodical-approach-to-agent-evaluation/
- OpenAI, Trace grading: https://platform.openai.com/docs/guides/trace-grading
- OpenAI, Agent evals: https://platform.openai.com/docs/guides/agent-evals

### 12.3 平台与运行时

- OpenAI Agents SDK: https://developers.openai.com/api/docs/guides/agents
- OpenAI Agents SDK tracing: https://openai.github.io/openai-agents-python/tracing/
- OpenAI Agents SDK guardrails: https://openai.github.io/openai-agents-python/guardrails/
- OpenAI Agents SDK sessions: https://openai.github.io/openai-agents-python/sessions/
- Anthropic, Scaling Managed Agents: https://www.anthropic.com/engineering/managed-agents
- Claude Managed Agents docs: https://platform.claude.com/docs/en/managed-agents/overview
- Google Gemini Enterprise Agent Platform scale docs: https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale
- Google Agent Platform Memory Bank: https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/memory-bank
- Google Agent Gateway overview: https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/gateways/agent-gateway-overview
- AWS Bedrock AgentCore Runtime: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html
- AWS AgentCore isolated sessions: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-sessions.html
- AWS AgentCore Policy: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html
- Kimi K2.6 Agent Swarm Help: https://www.kimi.com/help/agent/agent-swarm
- Kimi K2.6 Agent Overview: https://www.kimi.com/help/agent/agent-overview
