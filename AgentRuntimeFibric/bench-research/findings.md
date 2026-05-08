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

## Session 3 - CLEAR 深度研究事实

- 本次用户要求中的 CLEAR 指向 arXiv:2507.18392《CLEAR: Error Analysis via LLM-as-a-Judge Made Easy》，对应开源仓库为 `IBM/CLEAR`，不是旧文档中误写的 `Cost/Latency/Efficacy/Assurance/Reliability` 企业 benchmark。
- CLEAR 全称为 `Comprehensive LLM Error Analysis and Reporting`，定位是 LLM/Agent 错误分析工具，而不是排行榜 benchmark。它用 LLM-as-a-Judge 生成逐样本评分和文本批评，再用 Key Point Analysis 或 LLM-based KPA 聚合为系统级 recurring issues，并用 dashboard 支持过滤、对比和下钻到样本。
- 论文主体实验覆盖 GSM8K、TechQA、DelucionQA/RAGBench，系统包括 Mixtral 8x7B、LLaMA-3.1 8B、Granite-3.3 8B、Phi-4；judge 包括 GPT-4o 与 LLaMA-3.3 70B；KPA 包括 IBM watsonx KPA 与 LLM-based KPA。用户研究有 12 名 AI 从业者/研究者。
- 论文限制：依赖 judge 质量，继承 judge 的自偏、长度/风格偏好和漏检；LLM-based KPA 约需 2N 次 LLM 调用，但只对低分样本做 issue generation；CLEAR 能识别 recurring patterns，但不自动证明根因。
- 代码仓当前版本 `clear_eval` 1.1.1，Apache-2.0，Python 3.10+。支持普通 LLM response 分析和 Agentic Workflows 两条 pipeline。普通分析输入 CSV 至少含 `id`、`model_input`、`response`，可选 `ground_truth`。Agentic 分析支持 LangGraph/CrewAI + MLflow/Langfuse raw traces 或预处理 CSV。
- Agentic pipeline 提供 step-by-step CLEAR analysis、full trajectory evaluation、rubric evaluation、issues/root_cause CLEAR aggregation 和 NiceGUI dashboard；CSV IR 的必需列包括 `Name`、`task_id`、`step_in_trace_general`、`llm_call_index`、`model_input`、`response`，可选 `intent`、`api_spec`、`meta_data`、`traj_score`。
