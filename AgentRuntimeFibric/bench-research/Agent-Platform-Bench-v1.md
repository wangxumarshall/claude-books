# CLEAR 深度研究：从 LLM-as-a-Judge 打分到可审计错误分析

## 0. 结论摘要

本报告将 `Agent-Platform-Bench-v1.md` 从泛化的企业 Agent benchmark 综述，改写为对 CLEAR 的专题研究。经核对论文与代码仓，本文中的 CLEAR 指的是 IBM Research 等作者发布的 **CLEAR: Error Analysis via LLM-as-a-Judge Made Easy**，全称为 **Comprehensive LLM Error Analysis and Reporting**。它不是一个排行榜式 benchmark，也不是旧稿中误写的 `Cost / Latency / Efficacy / Assurance / Reliability` 五维企业基准，而是一套把 LLM-as-a-Judge 的逐样本评价转化为系统级、可浏览、可量化错误模式的开源错误分析工具。

CLEAR 的核心价值不是告诉开发者“哪个模型分数更高”，而是回答“模型为什么失败、失败模式出现在哪些样本上、哪些问题最常见、应该优先修哪里”。它的流程可以概括为四步：先让 judge model 对每条样本生成文本批评和数值分数；再把低分或非满分样本的批评文本送入 Key Point Analysis 或 LLM-based KPA；然后产出一组去重后的 recurring issues，并把每条样本映射回对应 issue；最后通过 dashboard 让开发者按 issue、分数、模型、样本子集做过滤、对比和下钻。

对 AgentRuntimeFabric/AgentRuntimeFibric 这类 Agent runtime 项目而言，CLEAR 最值得借鉴的不是“再做一个榜单”，而是把 trace、judge feedback、issue taxonomy、样本证据和 UI 下钻打通，形成一层“错误分析与改进优先级”能力。CLEAR 不能替代最终状态 oracle、权限审计、安全 gate 或根因分析，但它非常适合接在这些评估之后，把大量失败 trace 聚合成工程团队能行动的系统性缺陷清单。

## 1. 研究对象与更正说明

旧稿将 CLEAR 描述成企业级 Agent 的多维 benchmark，并把 CLEAR 展开为 `Cost, Latency, Efficacy, Assurance, Reliability`。这个叙述与本次用户要求的 CLEAR 论文和代码仓不一致。经核对，本文研究对象为：

| 项目 | 事实 |
|---|---|
| 论文 | `CLEAR: Error Analysis via LLM-as-a-Judge Made Easy`，arXiv:2507.18392 |
| 作者 | Asaf Yehudai、Lilach Eden、Yotam Perlitz、Roy Bar-Haim、Michal Shmueli-Scheuer |
| 机构 | IBM Research；其中 Asaf Yehudai 同时署名 The Hebrew University of Jerusalem |
| 代码仓 | `IBM/CLEAR` |
| 包名 | `clear_eval` |
| 许可证 | Apache-2.0 |
| 当前仓库版本 | `1.1.1`，要求 Python 3.10+ |
| 定位 | LLM/Agent 错误分析工具，不是 leaderboard benchmark |

因此，本文不再沿用旧稿中的“企业 Agent System 评估综述”叙述，而是围绕 CLEAR 的论文方法、实验结论、代码实现、Agentic workflow 扩展和对 AgentRuntimeFabric 的集成价值展开。

## 2. CLEAR 要解决的问题

LLM-as-a-Judge 已经成为生成式 AI 评估中的常用范式。开发者可以用强模型给回答打分、排序或做 pairwise preference，从而得到平均分、胜率、通过率等汇总指标。但这些指标的解释力有限：它们能回答“哪个系统更好”，却很难回答“系统为什么不好”。

这会在真实开发中造成三个问题。

第一，分数无法直接指导迭代。一个 RAG 系统平均分较低，可能是因为检索召回不足、答案没有引用证据、幻觉、回答过长、漏答边界条件，或者没有按任务格式输出。仅看平均分无法判断优先修 prompt、retriever、reranker、工具 schema 还是后处理。

第二，人工错误分析成本高。开发者通常需要抽样阅读失败样本，手工归类错误，再估计某类错误的频率。这个过程慢、主观、难复现，而且很难在每次模型、prompt、数据或 runtime 改动后重复执行。

第三，样本级 judge feedback 没有天然形成系统级结论。LLM judge 可以对每条样本给出一段批评文本，但几百或几千条批评本身仍然是非结构化文本。开发团队需要的是“常见问题清单 + 频率 + 证据样本 + 可过滤视图”。

CLEAR 的设计正是把“逐样本批评”加工成“系统级错误模式”。它保留 LLM-as-a-Judge 的灵活性，同时补上聚合、量化和可视化层。

## 3. 论文方法

CLEAR 的论文方法可以抽象为一个两阶段框架：先做逐样本判断，再做批评聚合。

设数据集为 `D = {x_n}`，目标系统为 `s`，系统对每个输入生成响应 `r_n = s(x_n)`。judge model `J` 对每个输入-响应对 `(x_n, r_n)` 进行评价，输出：

```text
j_n = (t_n, s_n)
```

其中 `t_n` 是自然语言批评，`s_n` 是 0 到 1 之间的质量分数。随后 CLEAR 只聚焦低分或非满分样本的文本批评，把这些批评聚合成系统级 issue 集合 `{i_m}`，并把每条样本映射到一个或多个 issue 上。

### 3.1 逐样本 judge

CLEAR 支持 reference-less 和 reference-based 两类评估。没有标准答案时，judge 仅根据输入、输出和评价准则做质量判断；有标准答案时，reference 会作为上下文进入 judge prompt。论文实验中同时覆盖数学题与 RAG 任务，代码仓中也提供 general、math、rag、agent、tool_call、external 等任务路径。

默认的普通 LLM response 评价准则包括：

| 维度 | 含义 |
|---|---|
| Adherence to Instructions and Relevance | 是否遵循输入指令，回答是否相关 |
| Accuracy & Completeness | 是否事实正确、覆盖关键细节 |
| Coherence & Clarity | 是否连贯、清晰、易懂 |

Agentic workflow 模式下，代码仓为单步 agent 输出设置了更贴近工具调用的准则：

| 维度 | 含义 |
|---|---|
| Correctness | 该步骤是否事实正确、逻辑合理；工具调用是否选对工具并给出有效参数 |
| Completeness | 该步骤是否完成它在 workflow 中的局部职责 |
| Relevance | 该步骤是否推进任务，是否避免无关内容 |
| Tool Selection | 涉及工具时，工具选择和参数是否合适 |

这里有一个重要实现细节：Agentic judge prompt 明确说明它只评价当前步骤，不应因为工具调用步骤还没有工具结果或最终答案而扣分。这对多步 Agent 评估很关键，因为工具调用本身是“委托下一步执行”，不是最终答复。

### 3.2 聚合：KPA 与 LLM-based KPA

CLEAR 的第二阶段是把逐样本批评聚合为 recurring issues。论文讨论了两种实现。

**传统 Key Point Analysis (KPA)**：CLEAR 先用 LLM 把 judge 的长批评拆成更短、更规范的句子，再用 KPA 方法聚类并生成 key points。这个路线的优点是接近已有 KPA 框架，能够把许多短句映射到少数 key points；缺点是输出可能更抽取式、更细碎，容易保留样本中的具体措辞。

**LLM-based KPA**：CLEAR 先用 LLM 总结每条批评，再让 LLM 从批评摘要中提取高层 recurring issues，之后再做去重合并，最后把每条批评映射到最终 issue 列表。论文指出这个过程大约需要 `~2N` 次 LLM 调用，但实际只对低分/非满分样本执行 issue generation，因此成本和目标系统质量相关。系统越好，低分样本越少，额外聚合成本越低。

LLM-based KPA 的工程意义更直接：它生成的 issue 更像开发团队能理解的缺陷类别，例如“遗漏关键信息”“生成无支持或推测性信息”“计算错误”“没有验证最终答案”。这比直接阅读几百条 judge feedback 更适合做迭代优先级排序。

### 3.3 三种评价模式

CLEAR 支持三类 issue discovery 模式：

| 模式 | 适用场景 | 代价 |
|---|---|---|
| General | 不知道问题会出现在哪里，希望探索模型行为 | 覆盖面广，但可能漏掉任务特定风险 |
| Task-specific | 已知任务关键风险，例如 RAG 的 faithfulness、answer completeness | 对目标风险更敏感，但可能减少意外问题发现 |
| Static / predefined issues | 已有固定错误 taxonomy，只想把样本映射到这些类别 | 可控、便于回归，但发现新问题能力较弱 |

对企业 Agent 评估而言，最实用的方式通常不是三选一，而是分层使用：探索阶段用 general，准入测试用 task-specific，回归 gate 用 predefined issues。

## 4. 论文实验与发现

论文用数学与 RAG 任务展示 CLEAR 的行为，而不是把 CLEAR 当作通用 benchmark 排名工具。

### 4.1 实验设置

论文使用的数据集包括：

| 数据集 | 类型 |
|---|---|
| GSM8K | 数学文字题 |
| TechQA | 技术问答/RAG |
| DelucionQA | RAGBench 处理后的 RAG 数据 |

被分析系统包括 Mixtral 8x7B、LLaMA-3.1 8B、Granite-3.3 8B 和 Phi-4。judge model 包括 GPT-4o 与 LLaMA-3.3 70B。KPA 模块包括 IBM watsonx KPA，以及以 GPT-4o 或 LLaMA-3.3 70B 实现的 LLM-based KPA。

### 4.2 GSM8K：分数之外的数学错误结构

在 Mixtral 8x7B + GSM8K + GPT-4o judge 的 task-specific 设置下，CLEAR 识别出最突出的失败模式是计算相关错误。论文表格中主要 issue 包括：

| Issue | 频率 |
|---|---:|
| No Issues Detected | 78.4% |
| Mathematical errors in calculations, including rounding and final steps | 13.2% |
| Incorrect understanding of problem statements leading to flawed reasoning | 11.8% |
| Failure to fully consider or correctly interpret all given information | 5.8% |
| Incomplete answers due to missing necessary steps or calculations | 5.5% |
| Logical errors despite clear reasoning | 4.3% |
| Misunderstanding or incorrect application of mathematical concepts or methods | 3.3% |
| Incorrect handling of units or conversions | 0.6% |
| Failure to verify or cross-check results | 0.2% |

这个结果的意义在于：开发者不只知道“数学题准确率不够”，还能看到失败主要集中在计算、题意理解、漏用条件和缺少校验。对应的改进动作也不同：计算错误可以接 calculator/tool use，题意理解可能需要数据增强或 prompt 结构化，缺少校验则可以在 workflow 中加 final verification step。

### 4.3 TechQA：模型差异可以转化为不同缺陷画像

论文比较了 Mixtral 8x7B 与 Phi-4 在 TechQA 上的 issue 分布。Mixtral 的 No Issues Detected 为 51.9%，Phi-4 为 76.6%，这和二者质量差异大体一致。但 CLEAR 更有价值的地方是暴露了不同模型的失败画像。

Mixtral 的主要问题包括遗漏必要细节、回答缺少具体性和完整性、遗漏相关链接或引用、提供不准确或无关信息、无法给出可执行洞察。Phi-4 的问题更少，且集中在缺少完整性、缺少上下文特定信息、技术细节不够具体、没有提到 unsupported features 或限制等方面。

这说明 CLEAR 不只是做总分比较，而是能把不同模型在同一数据集上的差异变成可操作的缺陷 taxonomy。对模型选型、prompt 改造和数据集补齐都更有用。

### 4.4 General vs Task-specific：探索和准入的取舍

论文对 Mixtral 8x7B 在 TechQA 上比较了 general 与 task-specific 模式。general 模式下，No Issues Detected 为 51.9%，主要问题包括遗漏必要细节、回答缺少具体性和完整性、遗漏链接或引用、不准确或无关信息等。task-specific 模式下，No Issues Detected 降到 18.5%，同时显著暴露 RAG 关键风险，例如：

| Task-specific issue | 频率 |
|---|---:|
| Lacks completeness and omits crucial details | 59.6% |
| Generates unsupported or speculative information | 31.8% |
| Fails to accurately incorporate document information | 22.0% |
| Provides irrelevant or extraneous information | 14.3% |
| Lacks clarity and conciseness | 14.0% |
| Fails to address the specific question | 12.4% |

这给企业落地一个直接启示：如果评估目标是“发现未知问题”，general 更合适；如果目标是上线前检查已知风险，例如 RAG 的证据忠实性、客服策略遵循、财务流程合规，则 task-specific 更合适。

### 4.5 用户研究

论文还做了一个 12 人用户研究，参与者包括 AI practitioners 和 researchers。参与者被要求使用 CLEAR 分析三个数据集，并通过 Likert 量表和开放反馈评价工具。

关键结果包括：

| 观察 | 数值 |
|---|---:|
| 当前依赖人工检查错误分析的参与者 | 75% |
| 认为工具帮助发现可能遗漏问题的平均评分 | 4.33 / 5 |
| 表示会采取或考虑采取行动的参与者 | 74% |
| time-saving 平均评分 | 4.25 / 5 |
| better than existing practices 平均评分 | 4.25 / 5 |
| 识别 common failure modes 的平均评分 | 4.16 / 5 |
| trustworthiness 相关评分 | 3.83 / 5 |

这个结果有两层含义。第一，CLEAR 确实能降低错误分析的人力成本，并把分析变成更可操作的流程。第二，用户对 trust 和 specificity 仍有保留，这与 LLM judge 和自动聚合工具的天然限制一致：它可以辅助归纳错误模式，但不能把自动结论直接当作无争议事实。

## 5. 代码仓实现深挖

`IBM/CLEAR` 仓库已经比论文主体多了一条 Agentic Workflows 路线。写文档或做集成时必须区分：论文主要论证普通 LLM response 的错误分析方法；代码仓当前实现还支持 agent trace 的 step-by-step 分析和 full trajectory evaluation。

### 5.1 包与入口

仓库的 Python 包名是 `clear_eval`，当前 `pyproject.toml` 中版本为 `1.1.1`，要求 Python 3.10+，主要依赖包括 LangChain、LangGraph、OpenAI、WatsonX、LiteLLM、Pandas、Streamlit、NiceGUI、Plotly、NetworkX、scikit-learn 等。

主要 CLI 入口如下：

| 命令 | 用途 |
|---|---|
| `run-clear-eval-analysis` | 普通 LLM response 的完整 pipeline |
| `run-clear-eval-generation` | 只生成模型响应 |
| `run-clear-eval-evaluation` | 已有响应时只跑 judge evaluation |
| `run-clear-eval-aggregation` | 已有 judge 结果时只跑 issue 聚合 |
| `run-clear-eval-dashboard` | 启动普通分析的 Streamlit dashboard |
| `run-clear-agentic-eval` | 运行 agentic step-by-step 与 full trajectory pipeline |
| `run-clear-agentic-dashboard` | 启动 Agentic workflow 的 NiceGUI dashboard |

普通 LLM 分析的最小运行方式：

```bash
run-clear-eval-analysis \
  --provider openai \
  --eval-model-name gpt-4o \
  --data-path path/to/data.csv \
  --output-dir results/my_run \
  --run-name my_run
```

Agentic workflow 分析的典型运行方式：

```bash
run-clear-agentic-eval \
  --data-dir data/my_traces \
  --results-dir results \
  --from-raw-traces true \
  --agent-framework langgraph \
  --observability-framework mlflow \
  --eval-model-name gpt-4o \
  --provider openai
```

### 5.2 普通 LLM Analysis pipeline

普通模式输入是 CSV，每行一条待评估样本。最小必需列为：

| 列名 | 含义 |
|---|---|
| `id` | 样本唯一标识 |
| `model_input` | 输入 prompt 或任务文本 |
| `response` | 已生成的模型回答；若 `perform_generation=true`，可由 pipeline 生成 |

可选列包括 `ground_truth`、`question`、`documents` 等。输出包括逐样本分数、逐样本评价文本、评价摘要、issue list、去重 issue list、样本到 issue 的映射，以及可上传 dashboard 的 ZIP。

从代码看，普通 pipeline 大致分为：

1. 读取输入数据和配置。
2. 可选执行 response generation。
3. 对每条 response 调用 judge，得到 `evaluation_text` 和 `score`。
4. 如果没有设置 `use_full_text_for_analysis`，对每条评价文本做摘要。
5. 从低分样本中合成 recurring issues。
6. 可选执行 issue 去重聚类。
7. 把每条评价文本映射到 issue list。
8. 转换为 UI 输入格式并打包 ZIP。

默认配置中值得关注的参数包括：

| 参数 | 默认/含义 |
|---|---|
| `inference_backend` | 默认 `litellm`，也支持 `langchain` 和 `endpoint` |
| `provider` | 默认 `watsonx`，可覆盖为 `openai`、`anthropic` 等 LiteLLM 支持 provider |
| `perform_generation` | 是否让 CLEAR 先生成 response |
| `high_score_threshold` | 默认 `0.91`，低于该阈值的反馈进入 issue 分析 |
| `max_shortcomings` | 默认 15 |
| `min_shortcomings` | 默认 3 |
| `max_eval_text_for_synthesis` | 默认 1000 |
| `predefined_issues` | 指定固定 issue list，跳过动态发现 |
| `external_judge_path` | 接入外部 judge 函数 |
| `issues_format` | `shortcomings` 或 `recommendations` |

### 5.3 Agentic Workflows pipeline

Agentic 模式面向多步 Agent trace。它支持两类输入：

| 输入方式 | 说明 |
|---|---|
| raw JSON traces | `--from-raw-traces true`，由内置 preprocessor 转为中间 CSV |
| preprocessed CSV | `--from-raw-traces false`，用户自己生成 CLEAR 要求的 trajectory CSV |

内置支持的框架组合：

| Agent framework | Observability platform | 状态 |
|---|---|---|
| LangGraph | MLflow | Supported |
| LangGraph | Langfuse | Supported |
| CrewAI | Langfuse | Supported |

Agentic pipeline 包含两类互补分析：

| 分析类型 | 目的 |
|---|---|
| Step-by-step CLEAR analysis | 按 agent/node/component 评估每次 LLM 调用，发现局部错误模式 |
| Full trajectory evaluation | 对完整任务轨迹做 task success、full trajectory quality、rubric evaluation，再对结果做 CLEAR aggregation |

Agentic CSV 中间表示要求每个 CSV 文件代表一条 trajectory，每行代表一次 LLM invocation。必需列包括：

| 列名 | 含义 |
|---|---|
| `Name` | agent 或 node 名称；CLEAR 会按这个字段分组分析 |
| `task_id` | trajectory 标识，同一轨迹所有行一致 |
| `step_in_trace_general` | 全局步骤顺序，1-indexed |
| `llm_call_index` | LLM 调用顺序 |
| `model_input` | 发送给 LLM 的 messages 或字符串 |
| `response` | LLM 输出；可包含 content 与 tool_calls |

可选列包括：

| 列名 | 含义 |
|---|---|
| `intent` | 用户原始目标；rubric evaluation 需要有效 intent |
| `tool_or_agent` | 标记 agent/tool |
| `api_spec` | 当前步骤可用工具定义，建议 OpenAI function-calling 格式 |
| `meta_data` | 模型、token、latency、span id 等自由元数据 |
| `traj_score` | 人工或外部 oracle 给出的轨迹级分数 |

Agentic pipeline 的输出目录通常包含：

```text
results/<run_name>/
  traces_data/
  step_by_step/
    clear_data/
    clear_results/
    clear_results.json
  full_trajectory/
    task_success/
    full_trajectory/
    rubric_generation/
    rubric/
    clear_analysis/
  unified_ui_results.zip
  pipeline_summary.json
```

`unified_ui_results.zip` 可以上传到 Agentic dashboard。该 dashboard 支持 workflow graph、node-specific CLEAR analysis、trajectory explorer、path analysis、temporal analysis 和 score prediction。

## 6. CLEAR 与 AgentRuntimeFabric 的关系

CLEAR 对 AgentRuntimeFabric 的意义应定位为“错误分析层”，而不是“完整评估底座”。它适合接在 runtime trace、task oracle、policy gate 和 safety test 之后，把大量样本级结果变成 recurring issue taxonomy。

### 6.1 能直接借鉴的设计

| CLEAR 设计 | 对 AgentRuntimeFabric 的启示 |
|---|---|
| 逐样本 judge feedback | 每个 Agent step、tool call、handoff、final answer 都应能生成可审计评价文本 |
| issue synthesis | 不要只看 pass/fail，要把失败归纳为可行动的缺陷类别 |
| issue mapping | 每个系统级 issue 必须能回链到具体 trace、step、输入、输出和工具参数 |
| dashboard filtering | 评估 UI 应支持按 issue、分数、节点、路径、工具、模型版本过滤 |
| predefined issues | 企业上线 gate 应支持固定风险 taxonomy，例如越权工具、无证据回答、审批绕过 |
| external judge | 允许接入规则引擎、确定性 oracle、人工标签或企业已有评估函数 |
| Agentic IR | runtime 应导出标准化 trace CSV/JSON，而不是只存散乱日志 |

### 6.2 建议的 ARF 数据映射

| AgentRuntimeFabric 对象 | CLEAR 字段/概念 | 集成说明 |
|---|---|---|
| `Run` / `Trajectory` | `task_id` | 每次用户任务或 benchmark case 映射为一个 trajectory |
| `Node` / `Agent` | `Name` | 用于按 planner、retriever、tool-router、executor、critic 等组件分组 |
| `EventLog` | `model_input`、`response`、`meta_data` | 保留消息、模型输出、token、latency、span id、runtime id |
| `ToolSpec` | `api_spec` | 记录当步可见工具，而不仅是实际调用的工具 |
| `ToolCall` | `response.tool_calls` | 工具名、参数、调用 id 应结构化保存 |
| `PolicyDecision` | predefined issues / evaluation criteria | 把企业策略风险转为固定评价项或 gate |
| `OutcomeOracle` | `traj_score`、full trajectory result | 最终业务状态仍应由外部 oracle 判定 |
| `EvidenceGraph` | issue mapping | issue 必须能回链到 trace、step、judge feedback 和 artifact |

### 6.3 推荐集成流程

AgentRuntimeFabric 可以按以下方式集成 CLEAR：

1. 在 benchmark runner 中统一导出 ARF trace，为每条任务生成一个 trajectory CSV 或 JSON。
2. 把 planner、retriever、tool-router、executor、critic、finalizer 等组件写入 `Name` 字段。
3. 把每次 LLM 调用的消息写入 `model_input`，把自然语言输出和 tool calls 写入 `response`。
4. 把可用工具 schema 写入 `api_spec`，把 token、latency、model、runtime、policy result 写入 `meta_data`。
5. 对私有 golden task、回归 trace、canary trace 批量运行 `run-clear-agentic-eval`。
6. 将 `clear_results.json`、`pipeline_summary.json` 和 `unified_ui_results.zip` 作为评估 artifact 保存。
7. 将高频 issue、严重 issue、指定 predefined issue 的出现率纳入 CI/CD gate。
8. 在 PR、模型升级、prompt 改动、tool schema 改动后对比 issue distribution，而不是只对比成功率。

### 6.4 建议的准入指标

CLEAR 自身不提供企业上线标准，但 ARF 可以基于 CLEAR 输出定义门禁：

| Gate | 示例规则 |
|---|---|
| 高频缺陷 | 任一 P0/P1 issue 出现率不得高于阈值 |
| 组件退化 | 某个 node 的平均 step score 较基线下降超过阈值则阻断 |
| 工具调用问题 | `Tool Selection` 相关 issue 出现率不得上升 |
| RAG 忠实性 | `unsupported/speculative information` 相关 issue 必须低于阈值 |
| 回归对比 | 新版本 issue distribution 不得显著劣于当前生产版本 |
| 人审抽样 | 对高频新 issue 自动生成样本包，进入人工复核 |

这些 gate 应与最终状态 oracle、policy engine、sandbox 审计和安全红队结果一起使用。CLEAR 负责解释“失败长什么样”，不是单独裁决“能不能上线”。

## 7. 局限与风险

CLEAR 的限制在论文和代码层面都很明确。

第一，CLEAR 依赖 judge 质量。judge 的自偏、长度偏好、风格偏好、领域知识不足和漏检都会传导到最终 issue。企业使用时应尽量做 judge 校准：抽样人工复核、跨 judge 对比、对关键场景使用 deterministic oracle 或外部 judge。

第二，LLM-based KPA 有成本。论文指出该路线约需 `~2N` 次 LLM 调用，虽然只对低分样本做 issue generation，但大规模生产 trace 仍需要预算控制。实际部署中应分层运行：PR 小样本、nightly 中样本、release 大样本。

第三，issue synthesis 可能过粗或过细。传统 KPA 可能更抽取式、碎片化；LLM-based KPA 更会综合抽象，但也可能把不同问题合并成模糊描述。代码仓提供 `max_shortcomings`、`predefined_issues`、`issues_format` 等参数，但最终 taxonomy 仍需要人工校准。

第四，CLEAR 不做因果根因证明。它能发现“答案经常缺少文档依据”，但不能单独判断根因是 retriever 召回失败、reranker 排序错误、prompt 未要求引用、模型忽略上下文，还是工具返回格式污染。根因分析需要结合 trace、检索日志、工具响应和系统实验。

第五，Agentic workflow 能力是代码仓扩展，不应反向夸大为论文主体已完整验证的 Agent benchmark。论文实验主要围绕 RAG 和数学任务；代码仓的 Agentic pipeline 很有工程价值，但其效果仍需要在 ARF 自己的 trace 和任务池上校准。

第六，隐私和安全要单独处理。CLEAR 会把输入、输出、judge feedback、工具 schema、元数据打包进结果和 dashboard artifact。企业接入前必须做脱敏、访问控制、artifact retention、secret 扫描和日志隔离。

## 8. 对 AgentRuntimeFabric 的落地建议

### P0：复现实验与最小闭环

先不用改 runtime。用现有 benchmark 的 50 到 200 条样本生成一个最小 CSV，跑普通 `run-clear-eval-analysis`，验证输出的 `analysis_results`、`shortcoming_list`、mapping 和 dashboard 是否符合团队预期。

P0 的成功标准不是得分高低，而是开发者能否回答：

- 主要失败类型是什么？
- 每类失败有多少样本？
- 每类失败能否下钻到原始输入、输出和 judge feedback？
- 这些 issue 是否能转化为 prompt、数据、工具或 runtime 改动？

### P1：导出 ARF trace 到 CLEAR Agentic IR

为 AgentRuntimeFabric 增加一个 `clear_exporter`，把每条 Agent run 导出为 CLEAR 需要的 trajectory CSV。优先覆盖：

- `task_id`
- `Name`
- `step_in_trace_general`
- `llm_call_index`
- `model_input`
- `response`
- `api_spec`
- `meta_data`
- `traj_score`

完成后跑 `run-clear-agentic-eval --from-raw-traces false`，避免一开始就绑定 MLflow/Langfuse preprocessor。

### P2：建立固定 issue taxonomy

在企业 Agent 场景中，仅靠动态 issue discovery 不够。建议沉淀一套 predefined issues，例如：

| 类别 | 示例 issue |
|---|---|
| 工具选择 | 选择了错误工具；应该调用工具但直接回答；工具参数缺字段 |
| RAG 忠实性 | 引用了不存在证据；忽略检索结果；把猜测写成事实 |
| 权限与策略 | 试图访问越权资源；绕过审批；泄露敏感字段 |
| 工作流完整性 | 未完成必要步骤；跳过确认；没有处理失败工具返回 |
| 恢复能力 | API 失败后无重试；循环调用；错误分类错误 |
| 用户交接 | 高风险/低置信任务未触发 human handoff |

这套 taxonomy 可以作为 `predefined_issues` 或 evaluation criteria 输入 CLEAR，形成稳定回归 gate。

### P3：把 CLEAR 产物接入评估证据链

每次 benchmark run 应保存：

- 原始 trace artifact
- CLEAR 输入 CSV/JSON
- judge 配置和 prompt 版本
- `pipeline_summary.json`
- `clear_results.json`
- dashboard ZIP
- issue distribution 对比报告

这些产物应该和模型版本、prompt 版本、tool schema 版本、runtime commit、数据集版本绑定。这样才能在回归发生时定位“是模型变了、prompt 变了、工具 schema 变了，还是 judge/taxonomy 变了”。

## 9. 最终判断

CLEAR 是一个很适合企业 Agent 评估体系吸收的“错误分析与可视化”组件。它把 LLM-as-a-Judge 从单纯打分扩展为“逐样本批评 -> recurring issue -> 频率量化 -> 样本证据 -> dashboard 下钻”的闭环。这对 AgentRuntimeFabric 特别有价值，因为 Agent 系统的失败通常不是单个最终答案错误，而是某个节点、工具、策略或状态转换在大量 trace 中反复出现同类问题。

但 CLEAR 不应被误用为完整 benchmark。它不替代最终业务状态验证，不替代安全策略引擎，不替代 sandbox，不替代人工复核，也不自动证明根因。最稳妥的定位是：在 ARF 的 benchmark harness 和 observability 之上，增加一层可复现、可下钻、可比较的错误模式分析层。

如果 AgentRuntimeFabric 要形成差异化，建议优先实现 CLEAR-compatible trace export、issue taxonomy 管理、judge 配置版本化、dashboard artifact 管理和 issue distribution regression gate。这样能把“Agent 是否通过测试”推进到“Agent 为什么失败、失败集中在哪些组件、下一轮应该优先修什么”。

## 参考资料

1. Asaf Yehudai, Lilach Eden, Yotam Perlitz, Roy Bar-Haim, Michal Shmueli-Scheuer. **CLEAR: Error Analysis via LLM-as-a-Judge Made Easy**. arXiv:2507.18392. https://arxiv.org/abs/2507.18392
2. IBM. **CLEAR: Comprehensive LLM Error Analysis and Reporting**. GitHub repository. https://github.com/IBM/CLEAR
3. IBM/CLEAR README. https://github.com/IBM/CLEAR/blob/main/README.md
4. IBM/CLEAR LLM Analysis Guide. https://github.com/IBM/CLEAR/blob/main/docs/ANALYSIS_README.md
5. IBM/CLEAR Agentic Workflows Guide. https://github.com/IBM/CLEAR/blob/main/src/clear_eval/agentic/README.md
6. IBM/CLEAR Agentic Intermediate Representation. https://github.com/IBM/CLEAR/blob/main/src/clear_eval/agentic/docs/INTERMEDIATE_REPR.md
7. IBM/CLEAR Agentic Dashboard Guide. https://github.com/IBM/CLEAR/blob/main/src/clear_eval/agentic/dashboard/README_DASHBOARD.md
8. IBM/CLEAR package metadata and CLI entry points. https://github.com/IBM/CLEAR/blob/main/pyproject.toml
