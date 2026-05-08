# CLEAR 企业 Agent 评估框架深度研究

研究对象：Sushant Mehta, **Beyond Accuracy: A Multi-Dimensional Framework for Evaluating Enterprise Agentic AI Systems**, arXiv:2511.14136

## 0. 更正说明

本文中的 CLEAR 指的是 arXiv:2511.14136 提出的企业级 Agent 多维评估框架：

```text
CLEAR = Cost + Latency + Efficacy + Assurance + Reliability
```

它不是同名的错误分析工具或代码仓。因此，本文不讨论逐样本错误聚合、KPA、工具 CLI 或 dashboard；这些内容属于另一条同名 CLEAR 工作线，不应混入本目录的企业 Agent 评估研究。

arXiv:2511.14136 的核心主张是：企业 Agent 不能只按任务完成准确率排序。真实部署还必须同时评估成本、时延、任务效能、安全合规和多次运行可靠性。论文通过系统分析 12 个主流 Agent benchmark，并对 6 类 Agent 架构在 300 个企业任务上做实验，提出 CLEAR 作为面向企业上线决策的多维评估框架。

## 1. 论文定位

| 项目 | 内容 |
|---|---|
| 论文 | Beyond Accuracy: A Multi-Dimensional Framework for Evaluating Enterprise Agentic AI Systems |
| arXiv | https://arxiv.org/abs/2511.14136 |
| 作者 | Sushant Mehta |
| 提交时间 | 2025-11-18 |
| 核心对象 | 企业级 Agentic AI 系统评估 |
| 框架 | CLEAR：Cost、Latency、Efficacy、Assurance、Reliability |
| 任务套件 | 300 个企业任务，覆盖 6 个企业域 |
| 实验对象 | 6 类 Agent 架构 |
| 验证方式 | 15 名企业 AI 部署负责人进行 expert readiness 评估 |

CLEAR 的定位不是再造一个单项能力 benchmark，而是给企业部署提供一个“多目标评估框架”。它承认准确率仍然重要，但认为准确率只是 Efficacy 的一部分；当 Agent 会调用工具、消耗 API 成本、产生延迟、触碰策略与安全边界，并且需要在大量相似请求上稳定运行时，单一 accuracy 排名会系统性误导企业选型。

## 2. 论文识别的三类评估缺口

论文先从现有 Agent benchmark 的局限出发，指出当前公开评估体系与企业上线要求之间存在三类关键错位。

### 2.1 成本没有被纳入主评分

现有 benchmark 往往只报告任务完成率，却忽略 Agent 每次任务背后的 token、API 调用、工具调用、推理轮数和基础设施消耗。论文指出，在类似精度水平下，不同 Agent 架构的成本可能出现最高 50x 差异。

这个问题在企业场景中不是边缘因素。一个 Agent 准确率提高 2 个百分点，如果每 10,000 个任务多消耗数万美元，就可能在商业上不可接受。复杂架构如反思、自我修正、多轮重试，可能带来边际准确率提升，却以指数级成本和时延为代价。

### 2.2 单次成功率掩盖可靠性脆弱

许多 benchmark 报告 pass@1 或单次成功率，但企业需要的是稳定成功。论文引用工具型 Agent 交互评估中的可靠性问题：单次运行 60% 的成功率，在要求 8 次连续成功时可能下降到 25%。

这对企业部署是本质差异。客服、合规、财务、运营自动化等场景不是“多试几次总能成”即可接受，而是每次用户请求都需要一致、可预期、低失败率的行为。一个 70% 单次成功但高度不稳定的 Agent，可能不如一个 60% 但行为更稳定的 Agent。

### 2.3 企业关键维度缺失

真实企业部署要求 Agent 满足安全、策略、合规、SLA、隐私、审计、异常恢复等约束。现有 benchmark 多数只测“任务有没有完成”，很少系统性评估：

- prompt injection 抵抗能力
- 数据泄露防护
- 是否遵守组织策略
- 是否满足时延 SLA
- 是否能优雅处理工具失败
- 是否能在多步骤任务中保持一致性

论文将这些缺口概括为实验室 benchmark 与生产部署成功之间的结构性差距。

## 3. CLEAR 五维框架

CLEAR 的五个维度分别覆盖企业部署中的经济性、交互性、任务质量、治理安全和稳定性。

| 维度 | 问题 | 代表指标 |
|---|---|---|
| Cost | 做成任务要花多少钱 | cost per task、cost per success、cost-normalized accuracy |
| Latency | 用户或业务流程要等多久 | end-to-end time、SLA compliance rate、p95/p99 latency |
| Efficacy | 任务是否真正完成且质量足够 | success rate、functional correctness、domain-specific quality |
| Assurance | 是否安全、合规、遵守策略 | policy adherence score、prompt injection resistance、data leakage rate |
| Reliability | 多次运行是否稳定 | pass@3、pass@5、pass@8、一致成功率、方差 |

### 3.1 Cost：成本维度

Cost 维度衡量 Agent 的经济效率，包括 token 成本、API 调用成本、推理成本、工具调用成本和基础设施开销。论文提出 Cost-Normalized Accuracy（CNA）和 Cost Per Success（CPS）这类指标，用于比较“昂贵但稍高准确率”的方案与“便宜但接近准确率”的方案。

对企业而言，CPS 特别重要，因为失败任务也会消耗成本。一个 Agent 即使成功率较高，如果每次失败都经历大量反思、重试和工具调用，真实单位成功成本可能很高。

### 3.2 Latency：时延维度

Latency 维度关注端到端任务完成时间，包括规划、执行、工具调用、反思、重试和最终响应。论文给出按任务域设定 SLA 阈值的思路，例如客户支持对时延要求更严格，代码生成或复杂分析可以允许更长时间。

时延不是用户体验细节，而是吞吐量、并发成本和业务可用性的组成部分。一个多轮推理 Agent 即使准确率高，如果频繁超过 SLA，在生产环境中也可能不可用。

### 3.3 Efficacy：效能维度

Efficacy 是传统 accuracy 的扩展。不同企业任务的“完成”定义不同：

- 软件工程任务看测试是否通过、补丁是否正确
- 数据分析任务看 SQL、报表、可视化和统计解释是否正确
- 客服任务看意图识别、答复质量、是否需要升级
- 合规任务看是否满足政策与监管要求

CLEAR 没有抛弃准确率，而是把准确率放回领域化任务质量中，避免用一个泛化成功率覆盖所有业务目标。

### 3.4 Assurance：保障维度

Assurance 覆盖安全、合规和策略遵循。论文提出 Policy Adherence Score（PAS），并将 prompt injection、数据泄露、领域幻觉、失败处理等纳入评估。

企业 Agent 的关键点在于：安全和策略违规往往是硬失败。一个 Agent 即使完成了功能任务，只要泄露用户数据、绕过审批、违反监管或调用越权工具，就不能被视为可部署。

### 3.5 Reliability：可靠性维度

Reliability 衡量 Agent 在多次运行中的一致性。论文强调 pass@k 作为企业部署指标，其中 pass@k 表示 k 次连续成功的概率。论文实验关注 pass@3、pass@5 和 pass@8，并指出关键任务需要较高的多次连续成功率。

这个维度直接挑战“单次 demo 成功”的评估习惯。Agent 的随机性、工具不稳定、上下文漂移和重试分支都会导致同一任务多次运行结果不同。企业需要评估方差，而不是只看一次最好表现。

## 4. 企业任务套件

论文构建了 300 个企业任务，覆盖 6 个领域。每个任务包含 5 到 15 个步骤，并带有成本、时延和策略合规注释。

| 领域 | 数量 | 任务特征 |
|---|---:|---|
| Customer Support | 60 | 多轮政策合规问题解决、知识库检索、升级处理、投诉管理 |
| Data Analysis | 50 | SQL 查询、报表生成、可视化、缺失值与异常值处理 |
| Process Automation | 50 | 表单填写、审批链路、多系统 API 编排、异常恢复 |
| Software Development | 60 | bug 修复、代码审查、测试生成、重构与性能优化 |
| Compliance | 40 | GDPR 请求、审计追踪、SOC 2 / ISO 27001 要求检查 |
| Multi-Stakeholder Workflows | 40 | 跨部门协调、冲突优先级、RBAC、截止时间和升级 |

每个任务包含自然语言描述、输入数据或上下文、预期输出、策略文档、参考成本基线、SLA 阈值、安全测试样例，以及人类专家执行得到的可靠性基线。这个设计的重点是让 Agent 不只回答问题，而是在带约束的企业流程中完成多步任务。

## 5. 实验设置与主要结果

### 5.1 被评估的 Agent 架构

论文评估了 6 类 Agent 架构：

| Agent | 说明 |
|---|---|
| ReAct-GPT4 | 基于 GPT-4 的 ReAct 风格 Agent |
| ReAct-GPT-o3 | 使用 o3 系列模型的 ReAct 风格 Agent |
| Reflexion | 带自我反思/迭代改进的 Agent |
| Plan-Execute | 分层规划后执行的 Agent |
| ToolFormer | 工具调用增强型 Agent |
| Domain-Tuned | 领域微调的 Llama 系 Agent |

每个 Agent 执行全部 300 个任务。可靠性评估选取 60 个代表性任务，每个任务执行 10 次。

### 5.2 总体表现

论文表 1 给出了六类 Agent 在 Efficacy、Cost、CNA、Latency、PAS 和 R@8 上的表现。关键结果如下：

| Agent | Efficacy | Cost | Latency | PAS | R@8 | 论文判断 |
|---|---:|---:|---:|---:|---:|---|
| ReAct-GPT4 | 72.3% | $2.87 | 8.4s | 0.89 | 58.3 | 精度较高但成本不低 |
| ReAct-GPT-o3 | 68.7% | $0.31 | 4.2s | 0.85 | 52.1 | 成本 Pareto 优 |
| Reflexion | 74.1% | $5.12 | 12.7s | 0.91 | 61.2 | 最高 Efficacy，但成本和时延高 |
| Plan-Execute | 71.9% | $1.24 | 6.8s | 0.88 | 64.5 | 均衡 Pareto 优 |
| ToolFormer | 69.5% | $1.89 | 5.9s | 0.82 | 55.7 | 工具能力有收益但策略弱 |
| Domain-Tuned | 70.3% | $0.27 | 3.8s | 0.93 | 72.8 | 可靠性和成本归一化最优 |

论文的核心发现不是 Reflexion 准确率最高，而是 Reflexion 被更均衡的方案支配。它 Efficacy 为 74.1%，但成本为 $5.12；Plan-Execute 以 71.9% 的接近效能，用约 4.1x 更低成本取得更好 R@8。Domain-Tuned 在成本、可靠性和策略遵循上表现突出，说明面向企业任务的领域化优化可能比单纯扩大模型或增加反思轮数更有效。

### 5.3 Pareto 前沿

论文识别出的 Pareto-optimal Agent 包括：

- ReAct-GPT-o3：成本最优
- Plan-Execute：平衡最优
- Domain-Tuned：可靠性和成本归一化表现最优

这说明企业选型不能只看最高 accuracy。更合理的做法是画出成本、时延、可靠性、策略合规和任务质量之间的 Pareto 前沿，选择符合业务约束的点。

### 5.4 可靠性退化

单次成功率在 68% 到 74% 之间，但 pass@8 下降到 52% 到 73%。Domain-Tuned 的 pass@8 为 72.8%，说明它在多次运行中更稳定；ReAct-GPT4 从 72.3% 单次表现降到 58.3% R@8，暴露了通用 Agent 的不稳定性。

这个结果直接支持 CLEAR 的可靠性主张：生产系统不能只测 pass@1。

### 5.5 领域差异

论文附录给出领域分解。几个趋势值得关注：

- Domain-Tuned 在 Customer Support、Compliance、Multi-Stakeholder 等需要领域策略和组织知识的任务上更强。
- ReAct-GPT4 在 Software Development 中 Efficacy 最高，但仍存在策略风险，例如不安全代码模式。
- Data Analysis 中各 Agent 表现接近，且 PAS 较高，原因是 SQL 约束本身有一定结构化边界。
- Multi-Stakeholder 是最难领域，因为它涉及跨部门协调、冲突约束、RBAC 和多步骤决策。

这说明企业评估需要按业务域拆分，而不是只给一个总分。

## 6. Expert Validation

论文招募 15 名企业 AI 部署负责人，对 40 个随机任务的部署就绪度进行 5 分制评估，并比较不同评估方式与专家判断的相关性。

| 评估方式 | Pearson | Spearman |
|---|---:|---:|
| Efficacy Only | 0.41 | 0.39 |
| Efficacy + Cost | 0.58 | 0.56 |
| CLEAR All 5 Dimensions | 0.83 | 0.81 |

这组结果是论文支持 CLEAR 的核心证据。它说明仅用任务效能预测生产就绪度较弱；加入成本后更好；使用五维 CLEAR 后，与专家部署判断的相关性显著更高。

在企业语境下，这个结论非常关键：上线评估本质上是风险决策，而不是纯能力排名。

## 7. 与现有 benchmark 的关系

CLEAR 不是要替代 SWE-bench、WebArena、AgentBench、GAIA、ToolLLM、WorkArena、OSWorld 等任务 benchmark，而是指出它们作为单项能力评估还不够。现有 benchmark 可以作为 Efficacy 的组成部分，但企业还要补齐：

- 成本和单位成功成本
- 端到端时延和 SLA 违约率
- 安全、策略与合规测试
- 多次运行可靠性
- 不同业务域下的权重差异

因此，CLEAR 更像“评估框架”和“企业任务套件设计原则”，而不是单一 leaderboard。

## 8. 对 AgentRuntimeFabric 的启示

AgentRuntimeFabric 的 benchmark 不应只回答“Agent 是否完成任务”，而应回答“这个 Agent runtime 是否让任务完成得可部署、可治理、可承受、可恢复”。

### 8.1 指标体系映射

| CLEAR 维度 | AgentRuntimeFabric 可落地指标 |
|---|---|
| Cost | token/task、tool calls/task、runtime minutes、sandbox cost、cost per success |
| Latency | end-to-end latency、step latency、tool latency、p95/p99、SLA violation rate |
| Efficacy | task success、final state correctness、test pass rate、业务字段正确率 |
| Assurance | policy violation、secret leakage、prompt injection success、unsafe tool call、audit completeness |
| Reliability | pass@3/pass@5/pass@8、flake rate、retry success、恢复后成功率 |

### 8.2 ARF benchmark 设计建议

ARF 可以把 CLEAR 转化为一套内部 benchmark harness：

1. 为每类任务定义 Efficacy oracle，例如测试通过、数据库最终状态正确、工单状态正确。
2. 在 EventLog 中记录每步 token、成本、耗时、工具调用、模型、runtime、重试次数。
3. 为每个工具调用接入 PolicyDecision，记录是否越权、是否需要审批、是否命中数据边界。
4. 对同一任务做多次 trial，计算 pass@k、方差和 flake rate。
5. 对每个业务域设置不同权重，而不是使用固定总分。
6. 输出 Pareto frontier，而不是只输出单一排行榜。
7. 对 Safety/Assurance 设置硬门禁：出现高危违规时，不允许用高 Efficacy 抵消。

### 8.3 建议的 ARF Composite Score

论文提出 composite score 支持企业按场景自定义权重。ARF 可以采用类似方式：

```text
ARF_CLEAR = wC*C_norm + wL*L_norm + wE*E + wA*A + wR*R
```

但在工程实现中，应把硬门禁和软评分分开：

- 硬门禁：secret 泄露、越权写入、审批绕过、不可逆副作用、审计缺失。
- 软评分：成本、时延、效能、普通策略遵循、可靠性。

这样可以避免“分数平均化”掩盖安全事故。

## 9. 对当前研究文档的使用边界

使用 CLEAR 时需要遵守论文边界。

第一，论文报告的是 300 个企业任务和 6 类 Agent 架构上的实验结论。它能证明多维评估的重要性，但不能直接代表所有行业、所有企业流程和所有 Agent 产品。

第二，论文提到计划释放 Enterprise Task Suite、evaluation code 和完整实验结果；在本研究写作时，应避免把这些未来计划写成已经可用的开源仓库，除非另有官方链接证据。

第三，CLEAR 的 expert validation 样本为 15 名专家、40 个随机任务。相关性结果很有价值，但仍属于初步验证，不应被写成“无条件预测生产成功”的保证。

第四，CLEAR 中的 Assurance 需要企业自身策略、权限模型、数据边界和合规要求支撑。公共任务套件只能提供参考，不能替代企业私有 policy gate。

## 10. 结论

arXiv:2511.14136 的 CLEAR 框架给企业 Agent 评估提供了一个清晰方向：准确率必要但不充分。Agent 进入生产环境后，成本、时延、安全合规和多次运行可靠性会与任务完成率同等重要，甚至在高风险业务中更重要。

对 AgentRuntimeFabric 来说，CLEAR 的价值在于把 benchmark 从“能力排名”升级为“部署决策”。ARF 如果要做企业级 Agent runtime，就需要把 CLEAR 五维指标做成运行时事实：每次执行都能记录成本、时延、工具副作用、策略决策、最终状态和多次运行稳定性；每次版本升级都能比较 Pareto 前沿和 pass@k；每个高风险任务都能通过 Assurance gate。

因此，本目录中后续所有 CLEAR 相关研究都应以 arXiv:2511.14136 为准：CLEAR 是 **Cost、Latency、Efficacy、Assurance、Reliability** 五维企业 Agent 评估框架。

## 参考资料

1. Sushant Mehta. **Beyond Accuracy: A Multi-Dimensional Framework for Evaluating Enterprise Agentic AI Systems**. arXiv:2511.14136. https://arxiv.org/abs/2511.14136
2. arXiv HTML version. https://arxiv.org/html/2511.14136v1
