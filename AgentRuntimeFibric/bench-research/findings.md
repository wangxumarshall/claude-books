# 研究发现

## Phase 1: 核心文献
（待填充）

## Phase 2: 二级文献
（待填充）

## Phase 3: 三级文献
（待填充）

## Session 2 - 正式稿校验结论

- 最终报告采用 A/B 级证据优先：官方文档、官方工程博客、正式 API 文档、arXiv/OpenReview/会议论文、官方 benchmark 与开源仓库为主要来源。
- 核心结论收敛为“结果必要但不充分”：企业级 Agent 上线评估必须同时检查最终业务状态、执行轨迹、权限策略、安全门禁、恢复能力、成本时延和审计证据。
- CLEAR 与 HAL 被定位为重要研究框架和评估基础设施，不再写成唯一权威或生产成功率保证。
- 平台比较按对象分层：OpenAI Agents SDK/Codex、Claude Managed Agents、Google Gemini Enterprise Agent Platform、AWS Bedrock AgentCore、Kimi K2.6 Agent Swarm 不再混作同类平台。
- AgentRuntimeFabric 的建议定位更新为开源、自托管、模型和运行时中立的 Agent 证据与治理控制面，核心对象为 EventLog、EvidenceGraph、PolicyDecision、ExecutionLease、WorkspaceLineage、RuntimeAdapter 与 Artifact。

## Session 3 - CLEAR 研究对象校正

- 用户明确要求当前目录下所有 CLEAR 评估研究均以 arXiv:2511.14136 为准，不使用同名错误分析工具或代码仓。
- 本目录中的 CLEAR 指 **Beyond Accuracy: A Multi-Dimensional Framework for Evaluating Enterprise Agentic AI Systems**，即 `Cost, Latency, Efficacy, Assurance, Reliability` 五维企业 Agent 评估框架。
- CLEAR 论文通过分析 12 个主流 Agent benchmark，指出现有评估缺少成本、可靠性和企业安全/策略维度；并构建 300 个企业任务，覆盖 Customer Support、Data Analysis、Process Automation、Software Development、Compliance、Multi-Stakeholder Workflows 六个领域。
- CLEAR 实验比较 6 类 Agent 架构：ReAct-GPT4、ReAct-GPT-o3、Reflexion、Plan-Execute、ToolFormer、Domain-Tuned。核心发现是最高 Efficacy 不等于最佳部署选择；成本、时延、Assurance 和 Reliability 会改变 Pareto 前沿。
- 15 名企业 AI 部署负责人对 40 个随机任务做 expert readiness 评估；CLEAR 五维评分与专家判断的相关性显著高于 Efficacy-only。
