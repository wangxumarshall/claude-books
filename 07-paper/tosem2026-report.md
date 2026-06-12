# ACM Transactions on Software Engineering and Methodology (TOSEM) 2026 洞察报告

> **覆盖时段**：2025年6月 – 2026年6月
> **期刊定位**：CCF-A类，ACM旗舰期刊，软件工程方法学领域顶级刊物
> **年度卷数**：每年1卷，2024年起每卷8期（1月、2月、3月、5月、6月、7月、9月、11月）
> **2024影响因子**：6.604

---

## 0. 期刊概览

ACM Transactions on Software Engineering and Methodology（TOSEM）由美国计算机学会（ACM）主办，创刊于1992年，与IEEE Transactions on Software Engineering（TSE）并称为软件工程领域两大旗舰期刊。TOSEM被中国计算机学会（CCF）认定为A类期刊，位列中科院一区，年发文量控制在50篇左右，录用率极低，代表了软件工程方法学、软件分析与质量保障方向的最高学术水平。

### 0.1 本报告关注焦点

本报告聚焦2025年6月至2026年6月期间TOSEM发表的与**系统软件**高度相关的论文，涵盖三大核心方向：

- **软件测试与分析**：模糊测试（Fuzzing）、变异测试（Mutation Testing）、漏洞检测、符号执行、GUI测试迁移
- **自动化程序修复（APR）**：基于大语言模型的程序修复、多智能体协同修复、补丁生成与验证
- **软件工程方法学**：AI辅助开发实践、软件安全路线图、量子软件工程、实时系统形式化验证

### 0.2 年度主题词云

> **LLM/大模型 · 程序修复 · 漏洞检测 · 模糊测试 · 变异测试 · 多智能体 · 软件安全 · 代码审查 · 实证研究**

2025-2026年度TOSEM的最显著特征是**大语言模型（LLM）全面渗透软件工程全生命周期**。从测试生成到程序修复，从漏洞检测到代码审查，LLM已成为方法论创新的核心驱动力。与此同时，传统软件工程方法（符号执行、形式化验证、模糊测试）通过与LLM的深度融合焕发新生。

---

## 1. 软件测试与分析方法

### 1.1 Fuzzing: On Benchmarking Outcome as a Function of Benchmark Properties

- **作者**：Dylan Wolff, Marcel Böhme, Abhik Roychoudhury
- **机构**：MPI-SP (Max Planck Institute for Security and Privacy), National University of Singapore
- **发表时间**：TOSEM 2025

#### 技术概要

模糊测试（Fuzzing）作为现代软件安全测试的核心技术，其基准评测结果直接影响研究方向和工具选择。然而，现有模糊测试基准研究存在根本性问题：**基准评估结果在多大程度上取决于基准程序本身的属性？** 本文首次系统性地回答了这一问题。

研究团队提出了一个理论框架，将模糊测试器的评测结果形式化为基准属性的函数。具体而言，研究探讨了如果基准程序的规模更大、初始种子的覆盖率更高，模糊测试器的排名将如何变化。通过大规模实验，作者揭示了当前模糊测试基准的**随机性**问题：测试结果高度依赖于基准程序的选择，而不同的基准集合可能导致截然相反的排名结论。

论文进一步提出了评估基准方法"一致性"（concordance）的指标，用于量化基准评测结果的可重复性和可信度。这一工作对模糊测试社区具有深远的方法论意义——它提醒研究者，工具排名不应当被视为绝对真理，而应在统计意义上被解读。

#### 技术启示

1. **基准敏感性**：模糊测试器的相对性能排名对基准程序集合高度敏感，单一的基准评测结论不可盲目推广。
2. **统计严谨性**：模糊测试评测应当报告效应量（effect size）和置信区间，而非仅给出排名。
3. **基准设计原则**：基准程序需要在规模、复杂度和覆盖特性上具有足够多样性，才能产生可信的对比结果。
4. **外推风险**：从小规模基准程序外推到大规模真实程序的结论需要谨慎对待。

---

### 1.2 Vital: Vulnerability-Oriented Symbolic Execution via Type-Unsafe Pointer-Guided Monte Carlo Tree Search

- **作者**：Haoxin Tu, Lingxiao Jiang, Marcel Böhme
- **机构**：MPI-SP, Singapore Management University
- **发表时间**：TOSEM 2025

#### 技术概要

符号执行是漏洞发现的强有力技术，但在面对大规模真实程序时，其面临的根本挑战是**路径爆炸**——执行树的分支数量随程序规模指数增长。现有的启发式搜索策略（如深度优先、广度优先、覆盖率引导）往往无法将有限的计算资源聚焦于最可能存在漏洞的执行路径。

本文提出了**Vital**，一个面向漏洞发现的符号执行框架，其核心创新在于利用**类型不安全指针引导的蒙特卡洛树搜索（MCTS）**来智能导航执行树。具体而言，Vital首先进行轻量级静态分析，识别程序中涉及类型不安全指针操作（如类型转换、直接内存访问）的代码位置——这些位置历史上是漏洞的高发区域。然后，Vital将MCTS应用于符号执行，将"到达类型不安全指针操作"作为搜索的奖励信号，从而将探索资源集中在最可能包含漏洞的执行路径上。

实验结果表明，Vital在多个真实C/C++程序上显著优于现有符号执行工具，在相同时间预算内发现了更多真实漏洞。该方法的关键优势在于将**领域知识**（类型不安全指针 ≈ 漏洞风险）编码为搜索引导信号，实现了符号执行从"盲目探索"到"目标导向探索"的范式转变。

#### 技术启示

1. **领域知识引导搜索**：将软件安全领域知识编码为搜索启发式，是缓解符号执行路径爆炸问题的有效策略。
2. **MCTS与程序分析融合**：蒙特卡洛树搜索在程序分析中的潜力尚未被充分挖掘，尤其适合需要长期规划的场景。
3. **类型系统作为漏洞指示器**：类型不安全操作是强有力的漏洞风险信号，可作为多种分析技术的优先级依据。
4. **漏洞导向 vs. 覆盖率导向**：以漏洞为目标的分析策略可能比以覆盖率为目标的策略更高效。

---

### 1.3 VulDeNoise: Outlier Detection to Reduce Label Noises for Effective Vulnerability Detection

- **作者**：Yutao Hu, Suyuan Wang, Yu Ji, Yueming Wu, Deqing Zou
- **机构**：华中科技大学 网络空间安全学院
- **发表时间**：TOSEM 2026 (2026-02-07)
- **DOI**：10.1145/3787972

#### 技术概要

基于深度学习的漏洞检测近年来取得了显著进展，但其性能严重依赖于训练数据的质量。一个关键但常被忽视的问题是**标签噪声**（label noise）——在漏洞数据集中，由于人工标注的主观性、漏洞定义的模糊性以及代码语义的复杂性，相当比例的样本可能被错误标注。标签噪声直接导致模型学习到错误的决策边界，降低检测精度和泛化能力。

本文提出了**VulDeNoise**，一个通过离群点检测消除标签噪声以提升漏洞检测效果的框架。VulDeNoise的核心思想是：在嵌入空间中，被错误标注的样本往往表现为离群点——它们与同类标签样本的表示距离较远，而与异类标签样本的表示距离较近。研究团队设计了多层次离群点检测策略，从函数级、切片级和语句级三个粒度识别可疑标注，并通过主动学习与人工审核相结合的方式进行校正。

实验覆盖了多个主流漏洞数据集（如SARD、NVD、FFMPeg+Qemu），结果表明VulDeNoise能够有效识别并纠正平均12-18%的标注错误。经VulDeNoise清洗后的数据集训练的模型，在漏洞检测F1分数上提升了5-12个百分点。更重要的是，VulDeNoise揭示了一个深层问题：当前漏洞检测数据集的标注质量可能被系统性高估，社区亟需建立更严格的标注质量控制标准。

#### 技术启示

1. **数据质量优先于模型复杂度**：在漏洞检测任务中，改善训练数据质量带来的收益可能超过设计更复杂的模型架构。
2. **嵌入空间离群检测**：利用深度表示学习中的嵌入空间分布特性识别标注错误，是一种通用且有效的策略。
3. **多粒度去噪**：从不同语义粒度（函数、切片、语句）进行去噪，可以互补地捕获不同类型的标注错误。
4. **标注质量评估生态**：漏洞检测社区需要建立标准化的标注质量评估基准和工具链。
5. **主动学习降低成本**：结合离群检测和主动学习，可以在最小化人工审核成本的前提下提升数据质量。

---

### 1.4 A Comprehensive Study on Large Language Models for Mutation Testing

- **作者**：Bo Wang, Mingda Chen, Ming Deng, Youfang Lin, Mark Harman, Mike Papadakis, Jie M. Zhang
- **机构**：北京交通大学, University College London, University of Luxembourg, King's College London
- **发表时间**：TOSEM 2026

#### 技术概要

变异测试（Mutation Testing）是衡量测试套件质量的金标准方法，其通过向程序中注入人工缺陷（变异体）并检查测试套件是否能够检测到这些缺陷，来评估测试的充分性。然而，变异测试面临两个根本性挑战：（1）**变异体生成**——如何生成语义上有意义且能有效评估测试质量的变异体；（2）**等效变异体检测**——如何高效识别那些在语义上与原始程序等价的变异体。

本文对**大语言模型在变异测试中的应用**进行了全面的实证研究，是第一篇系统探讨LLM能否以及如何改进变异测试的TOSEM论文。研究覆盖了三个关键维度：

- **变异体生成**：评估LLM生成语法正确、语义有意义且能有效测试差异化的变异体的能力。研究发现GPT-4等模型可以生成传统变异算子无法产生的新型变异体，但也存在生成无效变异体的问题。
- **等效变异体检测**：考察LLM判断一个变异体是否与原始程序语义等价的能力。实验显示LLM在此任务上表现出色，可以显著减少需要人工审查的变异体数量。
- **变异体优化**：探索LLM在减少冗余变异体、选择最有区分力的变异体子集方面的能力。

实验在多个大型Java和Python项目上进行，结果表明LLM在变异测试的多个环节展现了超越传统方法的潜力，但当前的性能离完全自动化仍有相当距离。

#### 技术启示

1. **LLM生成新型变异体**：LLM可以突破预定义变异算子的限制，生成更接近真实缺陷的语义变异体。
2. **等效变异体检测是LLM的强项**：由于等效性判断本质上是语义理解任务，LLM在此方面具有天然优势。
3. **人机协作范式**：当前最优实践是LLM辅助+人工确认的混合范式，而非完全自动化。
4. **变异测试的智能化转型**：LLM为变异测试这一经典技术注入了新的活力，使其在实际工业场景中更加实用。
5. **跨语言泛化**：LLM在多语言变异测试中的泛化能力值得进一步挖掘。

---

### 1.5 GUI Test Migration via Abstraction and Concretization (MACdroid)

- **作者**：Yakun Zhang, Chen Liu, Xiaofei Xie, Yun Lin, Jin Song Dong, Dan Hao, Lu Zhang
- **机构**：北京大学, Singapore Management University, 新加坡国立大学
- **发表时间**：TOSEM 2025
- **DOI**：10.1145/3726525

#### 技术概要

GUI测试迁移旨在将一个应用的测试用例迁移到实现相同功能的另一个目标应用上。现有方法主要采用**控件映射范式**（widget-mapping paradigm）——将源应用中的GUI控件直接映射到目标应用的对应控件。然而，不同应用即使实现相同的功能，其UI设计和交互逻辑也可能截然不同，导致控件映射方法产生不完整甚至错误的测试用例。

本文提出了**MACdroid**，首次引入了**抽象-具体化范式**（abstraction-concretization paradigm）用于GUI测试迁移。该范式的核心创新在于两阶段设计：

1. **抽象阶段**：从多个实现相同功能的源应用的测试用例中，提取出通用的功能级测试逻辑。该逻辑独立于具体UI实现，描述了"需要完成什么操作来测试该功能"。
2. **具体化阶段**：利用LLM将抽象的测试逻辑具体化为目标应用的GUI测试用例，包括具体的点击事件、输入内容和验证断言。

实验在FrUITeR和Lin两个广泛使用的数据集上（覆盖31个应用、34个功能和123个测试用例）进行评测。MACdroid在FrUITeR数据集上成功测试了64%的目标功能，比基线方法提升191%；在Lin数据集上成功测试了75%的目标功能，超越基线42%。

#### 技术启示

1. **抽象层次的分离**：将"测试什么"（功能逻辑）与"如何测试"（UI交互）分离，是GUI测试迁移的关键设计原则。
2. **LLM作为具体化引擎**：LLM在将抽象描述转化为具体实现方面表现出色，尤其适合跨UI平台的具体化任务。
3. **多源融合**：从多个源测试中提取共识性的测试逻辑，可以提高迁移后测试的鲁棒性。
4. **功能语义迁移 vs. 表面映射**：基于功能语义理解的迁移方法从根本上优于基于表面控件对应的映射方法。

---

### 1.6 Software Security Analysis in 2030 and Beyond: A Research Roadmap

- **作者**：Marcel Böhme, Eric Bodden, Tevfik Bultan, Cristian Cadar, Yang Liu, Giuseppe Scanniello
- **机构**：MPI-SP, Paderborn University, UC Santa Barbara, Imperial College London, Nanyang Technological University, University of Salerno
- **发表时间**：TOSEM 2025 (Special Section: 2030 Software Engineering Roadmap)

#### 技术概要

这是一篇受邀发表的路线图论文，属于TOSEM "2030软件工程路线图"特刊。六位软件安全领域的国际权威学者联合撰文，审视了当前软件安全分析面临的根本性挑战，并勾勒出面向2030年的研究蓝图。

论文首先识别了三大挑战：

1. **规模挑战**：现代软件系统的规模（数百万行代码、数千个依赖项、分布式微服务架构）使得全程序精确分析几乎不可能。
2. **语义挑战**：编程语言和框架的语义复杂性持续增长（异步编程、反射、动态加载、JIT编译），精确建模程序行为变得愈发困难。
3. **生态挑战**：软件供应链的复杂化（第三方库、容器、云服务）使得安全问题跨越传统程序边界，需要系统级的分析视角。

针对这些挑战，论文提出了六个方向的研究路线图：
- **统计程序分析**：将统计推断与程序分析结合，在不确定条件下做出合理的安全保障声明。
- **神经符号分析**：融合深度学习与符号推理，利用神经网络处理模糊性和规模，利用符号方法保证精确性。
- **持续安全分析**：安全分析从"一次性审计"转变为"持续监控"，适应快速迭代的DevOps实践。
- **供应链安全分析**：跨越组件边界进行端到端的安全分析，追踪漏洞从引入到触发的完整路径。
- **AI系统安全分析**：针对AI/ML组件（模型、数据管道、推理引擎）的专门安全分析方法。
- **人机协作安全分析**：将人类安全专家的领域洞察与自动化工具的计算能力有机结合。

#### 技术启示

1. **从精确到概率**：未来的软件安全分析可能需要接受不确定性，转向统计保证而非绝对保证。
2. **神经+符号融合**：深度学习与符号推理的互补性尚未被充分利用，是重要的交叉创新方向。
3. **供应链视角**：安全分析必须从单组件分析扩展到全供应链分析。
4. **AI系统自身安全**：随着AI系统的普及，其自身的安全性（模型投毒、对抗攻击、数据泄露）需要专门的软件工程方法。
5. **持续性 > 一次性**：安全分析的未来在于持续集成，而非单次审计。

---

## 2. 系统软件工程方法

### 2.1 SGAgent: Suggestion-Guided LLM-Based Multi-Agent Framework for Repository-Level Software Repair

- **作者**：Quanjun Zhang, Chengyu Gao, Yu Han, Ye Shang, Chunrong Fang, Zhenyu Chen, Liang Xiao
- **机构**：南京大学
- **发表时间**：TOSEM 2026
- **论文链接**：[arXiv:2602.23647](https://arxiv.org/abs/2602.23647)

#### 技术概要

基于大语言模型的智能体（LLM-based Agent）在仓库级软件修复（repository-level repair）领域取得了突破性进展，SWE-Bench等基准上的性能持续刷新。然而，现有方法普遍采用**"先定位后修复"范式**（localize-then-fix），直接从"漏洞在哪里"跳到"如何修复"，其间存在一个根本性的推理断层——定位到代码位置后，如何从对漏洞的理解推导出正确的修复方案？

本文提出了**SGAgent**，引入了**"定位-建议-修复"范式**（localize-suggest-fix），在定位和修复之间插入关键的"建议"阶段。SGAgent由三个专业化子智能体协同工作：

1. **Localizer（定位器）**：利用仓库级知识图谱定位漏洞相关的文件和函数。
2. **Suggester（建议器）**：从漏洞位置出发，增量式检索相关上下文（调用关系、数据流、历史变更），逐步构建对漏洞的完整理解，并生成可操作的修复建议。
3. **Fixer（修复器）**：基于建议器的输出生成具体补丁。

SGAgent还构建了目标仓库的**知识图谱（KG）**，将代码实体（函数、类、文件）及其关系（调用、继承、导入）结构化为可查询的图，增强了Agent的全局上下文感知能力。

在SWE-Bench-Lite上，SGAgent搭配Claude-3.5实现了51.3%的修复准确率，文件级和函数级定位准确率分别达到81.2%和52.4%，平均每次修复成本仅$1.48。当使用Claude-4时，修复率进一步提升至60.7%。在漏洞修复任务（VUL4J和VJBench）上，修复率达到48.0%，展示了跨任务和跨语言的强泛化能力。

#### 技术启示

1. **推理链完整性**：在复杂任务中显式建模中间推理阶段（建议），可显著提升终端输出质量。
2. **知识图谱增强Agent**：结构化知识图谱为LLM Agent提供了可靠的"世界模型"，减少了幻觉。
3. **经济可行性**：每次修复$1.48的成本意味着LLM辅助修复已具备工业部署的经济可行性。
4. **跨任务泛化**：location-suggest-fix范式不仅在通用程序修复上有效，在漏洞修复等特定任务上同样高效。

---

### 2.2 GiantRepair: Hybrid Automated Program Repair by Combining Large Language Models and Program Analysis

- **作者**：Li Fengjie, Jiang Jiajun, Sun Jiajun, Zhang Hongyu
- **机构**：天津大学, 重庆大学
- **发表时间**：TOSEM 2025

#### 技术概要

现有基于大语言模型的自动化程序修复（APR）方法通常直接使用LLM生成的补丁，但由于LLM缺乏程序特定知识（如局部变量名、领域特有API、类型约束），生成的补丁往往无法通过测试。如何有效利用这些"接近正确但不完全正确"的补丁，是一个尚未被充分探索的问题。

本文提出了**GiantRepair**，一种将LLM与程序分析深度融合的混合APR方法。其核心洞察是：**LLM生成的补丁即使不正确，也能为补丁搜索提供有价值的骨架信息**。

GiantRepair的工作流程分为两个阶段：

1. **补丁框架构建**：从LLM生成的多个候选补丁中提取共性结构，构建"补丁框架"（patch skeleton）——一个保留了关键修改模式但留有空位（hole）的模板。例如，框架可以明确"需要在第X行后插入一个条件判断"但不确定具体的判断条件。
2. **框架实例化**：利用基于程序分析的搜索技术（包括约束求解、类型检查、数据流分析），在补丁框架限定的搜索空间内寻找最优的具体化方案。

在Defects4J v1.2和v2.0上的大规模实验表明，GiantRepair相比直接使用LLM生成的补丁，平均修复率分别提升了27.78%和23.40%。在"完美故障定位"和"自动故障定位"两种场景下，分别比现有最优APR方法多修复了至少42个和7个漏洞。

#### 技术启示

1. **补丁框架的引导价值**：LLM提供"大致方向"，程序分析负责"精确落地"，是混合APR的杀手级范式。
2. **搜索空间剪枝**：补丁框架将无限的补丁搜索空间缩减为有限的"填空"问题，使得精确分析方法变得可行。
3. **知识互补**：LLM的语义理解能力和程序分析的精确推理能力高度互补。
4. **实用定位假设**：在"自动故障定位"场景下的评估更贴近工业实际，应成为APR评测的标准。

---

### 2.3 A-ProS: Towards Reliable Autonomous Programming Through Multi-Model Feedback

- **作者**：Anika Tabassum, Md Sifat Hossain, Md. Fahim Arefin, Tariqul Islam, Tarannum Shaila Zaman
- **机构**：美方学术机构
- **发表时间**：TOSEM 2026
- **论文链接**：[arXiv:2605.18073](https://arxiv.org/abs/2605.18073)

#### 技术概要

大型语言模型在代码生成方面展现了强大潜力，但其在**基于执行反馈迭代改进解决方案**方面的能力尚未被充分探索。竞赛编程（competitive programming）为研究这一问题提供了理想的实验场——它要求端到端的算法推理、精确实现、严格约束下运行和完全功能正确性。

本文提出了**A-ProS**，一个自主AI Agent，通过**混合多模型反馈框架**（hybrid multi-model feedback framework）解决竞赛编程问题。A-ProS的核心设计理念是将**方案生成**与**专用化调试**分离：

- **生成器**：使用ChatGPT系列（GPT-4和GPT-5）生成初步解决方案。
- **调试评论家**：使用三个不同的模型作为调试评论家——Codestral-2508、Llama-3.3-70B和DeepSeek-R1。当生成的方案未通过测试时，评论家分析错误输出并提供针对性的调试反馈。

实验采用2×3因子设计（2个生成器×3个调试评论家），在ICPC World Finals（2011-2024）和Codeforces（1200-1800难度）的367个问题上评估了6种工作流。结果表明：

- GPT-5工作流从初始39个正确解答提升至三轮反馈后的85-90个（提升约2.3倍）。
- GPT-4工作流从15个提升至31-38个。
- 有状态反馈（保留完整对话历史）显著优于无状态反馈（每次独立生成）：正确率提升8.5-10.6个百分点，重复失败减少至1/3.5。
- 相比基线Agent循环，A-ProS的增益超过2倍。

#### 技术启示

1. **多模型互补**：不同LLM在代码生成和调试推理上的能力差异可以被系统化利用——生成用强模型，调试用专门模型。
2. **反馈持续性**：保持反馈历史（有状态）对于迭代代码改进至关重要，无状态重置会丢失大量上下文。
3. **专业化分工**：将生成和调试分离为不同角色，比单一模型包揽所有任务更高效。
4. **竞赛编程的迁移价值**：竞赛编程场景下验证的代码生成和迭代改进能力，可以迁移到更广泛的软件工程任务。

---

### 2.4 DEVLoRe: Integrating Various Software Artifacts for Better LLM-based Bug Localization and Program Repair

- **作者**：Qiong Feng, Xiaotian Ma, Jiayi Sheng, Ziyuan Feng, Wei Song, Peng Liang
- **机构**：武汉大学
- **发表时间**：TOSEM 2025
- **论文链接**：[arXiv:2412.03905](https://arxiv.org/abs/2412.03905)

#### 技术概要

大多数基于LLM的程序修复方法仅依赖单一类型的软件信息（如代码本身），而没有充分利用多样化的软件制品（software artifacts）——包括问题描述（issue content）、堆栈错误跟踪（stack error trace）、调试信息（debug information）等。不同类型的软件制品包含互补的信息：问题描述提供高层语义上下文，堆栈跟踪指示错误传播路径，调试信息揭示运行时状态。

本文提出了**DEVLoRe**，系统性地探索了不同软件制品在漏洞定位和程序修复中的作用。DEVLoRe的工作流程如下：

1. **方法级定位**：利用问题描述和堆栈错误跟踪定位漏洞所在的方法。
2. **行级定位与补丁生成**：利用漏洞方法内的调试信息、问题描述和堆栈跟踪，精确定位漏洞代码行并生成可修复的补丁。

核心发现包括：
- **问题描述是最有效的单一信息源**：在辅助LLM进行故障定位和程序修复方面表现最佳。
- **软件制品互补性**：不同类型的软件制品相互补充，组合使用效果显著优于单一信息源。
- 在Defects4J v2.0上，DEVLoRe成功定位了49.3%的单漏洞方法和47.6%的多漏洞方法，分别生成了56.0%和14.5%的可信补丁。
- 在SWE-bench上的跨语言实验表明，DEVLoRe解决了9个现有方法无法修复的独特问题。

#### 技术启示

1. **多源信息融合**：软件调试中不同类型信息的互补价值巨大，系统化融合方法论值得深入研究。
2. **问题描述的价值被低估**：自然语言的问题描述比通常认为的更有信息量，应作为修复流程的一等公民。
3. **跨语言迁移的挑战**：一个语言上的最佳实践不能直接应用于另一种语言，需要适配。
4. **定位与修复的耦合**：精确的定位是高质量修复的前提，二者应从系统工程角度协同设计。

---

### 2.5 Assessing the Latent Automated Program Repair Capabilities of Large Language Models using Round-Trip Translation

- **作者**：Fernando Vallecillos Ruiz, Anastasiia Grishina, Max Hort, Leon Moonen
- **机构**：Simula Research Laboratory (Norway)
- **发表时间**：TOSEM 2025
- **DOI**：10.1145/3771922
- **论文链接**：[arXiv:2401.07994](https://arxiv.org/abs/2401.07994)

#### 技术概要

自然语言处理研究表明，通过将文本翻译到另一种语言再翻译回来（round-trip translation，往返翻译），语言模型可以修正其中的错误。这种现象的机制被解释为**均值回归**（regression toward the mean）——模型倾向于输出训练语料中最常见的模式，从而在往返翻译过程中将低频的错误模式替换为高频的正确模式。

本文探索了这一潜在的修复能力在**自动化程序修复（APR）**中的延伸：将包含漏洞的代码从一种编程语言翻译为另一种编程语言或自然语言，再翻译回来。研究假设往返翻译能够恢复LLM训练语料中最常见的代码模式，将不常见的错误替换为更常见、更自然的无错代码。

研究使用了9个LLM和4个主流Java APR基准（包括Defects4J、HumanEval-Java等），进行了详细的定量和定性分析：

- 通过英文进行往返翻译，GPT-4在HumanEval-Java的164个漏洞中生成了100个可信补丁，其中97个经人工确认正确。
- 往返翻译独特地为46个漏洞生成了可信补丁——这些漏洞是专门为APR微调的模型也未能修复的。
- 然而，往返翻译的整体修复率仍低于最先进的专用APR方法。
- 局限性包括：代码风格的稀释（修复后的代码可能偏离原项目的编码风格）、以及某些漏洞类型（如需要深层语义理解的逻辑错误）难以通过简单的翻译范式修复。

#### 技术启示

1. **零样本修复能力**：LLM即使在未专门为APR微调的情况下，也具有可观的潜在程序修复能力。
2. **往返翻译的机制价值**：作为APR的补充组件而非替代方案，往返翻译在捕捉"统计常见错误"方面独具优势。
3. **代码风格保持**：程序修复不仅需要功能正确性，还需要保持原始代码风格——后者是当前方法的薄弱环节。
4. **语言作为正则化器**：自然语言（英语）作为中间表示，对代码起到了隐式的正则化和去噪作用。

---

### 2.6 Unveiling the Role of ChatGPT in Software Development: Insights from Developer-ChatGPT Interactions on GitHub

- **作者**：Ruiyin Li, Peng Liang, Yifei Wang, Yangxiao Cai, Weisong Sun, Zengyang Li
- **机构**：武汉大学, Nanyang Technological University, 华中师范大学
- **发表时间**：TOSEM 2026
- **论文链接**：[arXiv:2505.03901](https://arxiv.org/abs/2505.03901)

#### 技术概要

ChatGPT等生成式AI工具已被开发者广泛采用，但对于开发者**如何在实际工作中实际使用**LLM辅助，目前仍缺乏大规模的实证证据。本文通过对GitHub上公开分享的ChatGPT对话链接进行大规模实证分析，填补了这一空白。

研究团队构建了**DevChat**数据集——包含从2023年5月至2024年6月期间GitHub上收集的2,547个公开分享的ChatGPT对话链接。通过对DevChat的全面分析，研究揭示了以下关键发现：

- **交互模式**：开发者与ChatGPT的交互通常是简短的（大多数为1-3轮对话）且任务聚焦的，表明ChatGPT更多被用于"即时问答"而非"长程协作"。
- **分享目的**：开发者分享ChatGPT对话的主要目的分为五类——任务委托、问题解决、知识获取、观点确认和方案验证。
- **开发活动分布**：ChatGPT最常被用于**软件实现**和**维护与演化**活动，其次是代码审查、测试和调试。
- **细粒度任务分类**：研究识别出39种由ChatGPT支持的细粒度软件工程任务，其中**代码生成与补全**和**代码修改与优化**最为突出。
- **数据源-活动-任务映射框架**：提出了一套将GitHub数据源（issues、PRs、commits、discussions）与开发活动和SE任务关联起来的映射框架。

这一研究首次提供了LLM在真实软件开发场景中应用的全景图，为理解AI辅助开发的当前状态和未来方向奠定了实证基础。

#### 技术启示

1. **开发者更偏好快捷交互**：短对话模式表明，工具设计应针对即时任务优化，而非假设长程协作。
2. **分享即知识传播**：开发者公开分享对话的行为本身就是一种新型的知识传播形式，可被系统化利用。
3. **任务粒度决定工具适配**：39种细粒度任务的识别为设计专用化AI辅助工具提供了需求图谱。
4. **实证数据驱动工具设计**：基于真实使用数据而非假设需求来设计AI开发工具，将更有针对性。
5. **维护与演化是主场景**：AI辅助在软件维护（而非新建项目）中具有最大的应用潜力。

---

### 2.7 Fine-Tuning Large Language Models to Improve Accuracy and Comprehensibility of Automated Code Review

- **作者**：Yongda Yu, Guoping Rong, Haifeng Shen, He Zhang, Dong Shao, Min Wang, Zhao Wei, Yong Xu, Juhong Wang
- **机构**：南京大学
- **发表时间**：TOSEM 2025

#### 技术概要

自动化代码审查通过AI技术协助开发者发现代码中的缺陷、风格问题和改进机会，有望大幅降低人工代码审查的成本。然而，现有方法面临两大核心挑战：**准确性不足**——生成的审查意见可能遗漏真实问题或包含虚假警报；**可理解性不足**——审查意见的表述可能不够清晰、缺乏足够的上下文或解释。

本文探索了通过**微调大语言模型**来同时提升自动化代码审查的准确性和可理解性。研究团队从GitHub上收集了大规模的代码审查数据（包括审查评论及其对应的代码变更），并设计了一套微调策略，使LLM学习生成既准确又易于理解的审查意见。

关键技术贡献包括：
- **审查意见质量的多维度评估框架**：从准确性、完整性、可理解性和可操作性四个维度衡量审查意见质量。
- **微调数据构造策略**：如何从原始代码审查数据中筛选高质量样本并构造适合监督微调的输入-输出对。
- **基线与微调模型的系统对比**：在多个模型和多个项目上评估微调前后的性能差异。

实验结果表明，微调后的模型在审查意见的准确性和可理解性上均有显著提升。特别地，微调使模型学会了生成更具上下文针对性、更符合项目编码规范的审查建议。

#### 技术启示

1. **可理解性与准确性同等重要**：代码审查自动化不应仅追求准确性——不可理解的审查意见不会被开发者采纳。
2. **项目特定微调的价值**：通用模型经项目特定数据微调后，可学习项目的编码规范和审查风格。
3. **数据筛选是关键**：代码审查数据的质量参差不齐，高质量微调数据的筛选策略至少与模型架构同等重要。
4. **人机协作审查**：自动审查的定位应是辅助而非替代人工审查，可理解的意见有助于开发者快速判断建议是否采纳。

---

### 2.8 C2|Q>: A Robust Framework for Bridging Classical and Quantum Software Development

- **作者**：Boshuai Ye, Arif Ali Khan, Teemu Pihkakoski, Peng Liang, Muhammad Azeem Akbar, Matti Silveri, Lauri Malmi
- **机构**：University of Oulu (Finland), 武汉大学, LUT University
- **发表时间**：TOSEM 2026
- **论文链接**：[arXiv:2510.02854](https://arxiv.org/abs/2510.02854)

#### 技术概要

量子软件工程（Quantum Software Engineering, QSE）正在成为使量子计算对更广泛开发者社区可及的关键学科。然而，当前的量子开发环境仍然要求开发者处理跨软件栈的低层细节——包括问题编码、电路构建、算法配置、硬件选择和结果解释——这对于经典软件工程师而言构成了极高的使用门槛。

本文提出了**C2|Q>**（读作"C to Q"），一个硬件无关的量子软件开发框架，将特定类型的经典规范自动翻译为量子可执行程序。C2|Q>应用模块化软件工程原则，将工作流划分为三个核心模块：

1. **编码器（Encoder）**：对输入问题进行分类，生成量子兼容格式（Quantum-Compatible Formats），并构建量子电路。在评测中，编码器模块实现了93.8%的完成率。
2. **部署模块（Deployment Module）**：根据保真度（fidelity）、运行时间和成本推荐最优的量子硬件。在扩展到56量子比特的工作负载上，硬件推荐模块能够持续选择适当的量子设备。
3. **解码器（Decoder）**：将量子计算结果解释回经典解决方案。

端到端实验覆盖了434个Python程序和100个JSON问题实例，在模拟器和真实量子硬件（限于当前NISQ能力的小到中等规模实例）上均成功执行。C2|Q>的开源实现可通过GitHub获取，并作为Python包发布。

#### 技术启示

1. **经典-量子桥接的软件工程方法**：将软件工程的模块化、抽象化原则应用于量子计算，可大幅降低使用门槛。
2. **硬件无关设计**：屏蔽底层量子硬件的差异，使得同一套程序可以在不同的量子处理器上运行。
3. **NISQ时代的实用主义**：在当前中等规模含噪量子（NISQ）时代，务实的设计应同时支持模拟器和真实硬件。
4. **量子的软件工程化**：量子计算正在从物理实验走向软件工程实践，需要配套的方法论和工具链。

---

### 2.9 Fault-Tolerant Design and Multi-Objective Model Checking for Real-Time Deep Reinforcement Learning Systems

- **作者**：Guoxin Su, Thomas Robinson, Hoa Khanh Dam, Li Liu, David S. Rosenblum
- **机构**：University of Wollongong (Australia), National University of Singapore
- **发表时间**：TOSEM 2026
- **论文链接**：[arXiv:2603.23113](https://arxiv.org/abs/2603.23113)

#### 技术概要

深度强化学习（DRL）已成为解决复杂决策问题的强大范式，但DRL系统在实际部署中面临严峻的可依赖性挑战——仿真到现实的差距（sim-to-real gap）、分布外观察（out-of-distribution observations）以及延迟的严重影响。特别是延迟诱导的故障（latency-induced faults）可能导致不安全或不稳定的行为。然而，现有的DRL容错方法缺乏能够同时严格分析和优化性能与安全性的形式化方法。

本文提出了一个用于设计和分析**实时DRL系统切换机制**的形式化框架。该框架的核心思想是：当DRL Agent面临不确定性（如延迟过高、遇到分布外状态）时，系统应能够切换到备用的安全控制器。

技术贡献包括：

1. **时间自动机（Timed Automata）建模**：使用TA对DRL与备用控制器之间的切换逻辑进行显式设计。
2. **MDP转换与分析**：将TA语法转换为马尔可夫决策过程（MDP），使用概率模型检验进行形式化分析。
3. **凸查询技术（Convex Query Technique）**：提出新型的多目标模型检验方法，在满足硬安全约束的前提下优化软性能目标。
4. **MOPMC工具**：实现了GPU加速的多目标概率模型检验工具，在模型规模和目标数量上展现了优越的可扩展性。

该框架使得系统设计者能够在部署前形式化地验证：在给定的延迟和不确定性条件下，DRL系统的切换策略是否同时满足性能需求和安全保证。

#### 技术启示

1. **形式化方法用于AI系统**：将模型检验这一传统形式化技术应用于DRL系统，填补了AI系统工程化验证的空白。
2. **切换机制的形式化设计**：DRL与安全控制器之间的切换策略应经过严格分析，而非仅凭经验设定。
3. **多目标权衡的形式化**：性能与安全之间的权衡可以且应该通过形式化方法进行精确量化。
4. **GPU加速的可扩展性**：GPU加速使得概率模型检验能够应用于实际规模的DRL系统。
5. **软硬约束分离**：将安全建模为硬约束、性能建模为软目标，是在不确定环境下进行系统设计的有效方法论。

---

## 3. 结语与未来方向

### 3.1 年度关键趋势总结

纵观2025年6月至2026年6月的TOSEM论文，可以总结出以下五大关键趋势：

**趋势一：LLM从工具到基础设施的转变。** 大语言模型不再仅仅是软件工程研究中的一个"方法选项"，而是正在成为软件工程方法学的底层基础设施。从程序修复到漏洞检测、从代码审查到测试生成，LLM渗透率接近100%。

**趋势二：混合方法的兴起。** "LLM + X"成为主流范式——LLM与符号执行（Vital）、与程序分析（GiantRepair）、与知识图谱（SGAgent）、与搜索算法（MACdroid）的深度融合，表明学界已认识到LLM不能单独解决所有问题。

**趋势三：多智能体协同。** SGAgent的定位-建议-修复三Agent架构、A-ProS的生成-调试多模型分工、iReDev的六Agent需求开发——多智能体系统的工程化设计成为新的研究热点。

**趋势四：从模型到数据的关注转移。** VulDeNoise关注标签噪声、DEVLoRe关注多源信息融合——研究者开始将注意力从模型架构创新转向数据和信息的质量管理，这是领域成熟度提升的标志。

**趋势五：安全与可靠性的系统性审视。** "2030路线图"从宏观视角审视了软件安全分析的未来，DRL系统的形式化验证则为AI系统的可靠性保障提供了新的方法论框架。

### 3.2 未来研究方向

基于对本期TOSEM论文的分析，以下是值得关注的未来研究方向：

1. **LLM辅助测试生成的规模化**：如何将LLM从单元测试生成扩展到系统级和集成测试生成？
2. **仓库级智能体的上下文管理**：当代码仓库达到数百万行时，如何高效管理和检索Agent所需的上下文？
3. **混合分析的自动化编排**：在"LLM+符号执行+模糊测试+程序分析"的混合范式中，如何自动决策哪种方法应用于哪个子问题？
4. **AI系统的软件工程**：随着AI系统成为基础设施，如何将软件工程方法论应用于AI系统本身的开发和维护？
5. **安全分析的持续化与自动化**：如何将安全分析从离线审计转变为在线持续监控？
6. **量子软件工程的成熟化**：随着量子计算硬件的进步，量子软件工程方法论需要同步发展。

---

## 论文索引表

| 序号 | 论文标题 | 作者 | 机构 | 发表时间 | 主题标签 |
|------|---------|------|------|---------|---------|
| 1 | Fuzzing: On Benchmarking Outcome as a Function of Benchmark Properties | Dylan Wolff, Marcel Böhme, Abhik Roychoudhury | MPI-SP, NUS | TOSEM 2025 | 模糊测试、基准评测、统计方法 |
| 2 | Vital: Vulnerability-Oriented Symbolic Execution via Type-Unsafe Pointer-Guided MCTS | Haoxin Tu, Lingxiao Jiang, Marcel Böhme | MPI-SP, SMU | TOSEM 2025 | 符号执行、漏洞检测、蒙特卡洛树搜索 |
| 3 | VulDeNoise: Outlier Detection to Reduce Label Noises for Effective Vulnerability Detection | Yutao Hu, Suyuan Wang, Yu Ji, Yueming Wu, Deqing Zou | 华中科技大学 | TOSEM 2026 | 漏洞检测、标签噪声、数据质量 |
| 4 | A Comprehensive Study on Large Language Models for Mutation Testing | Bo Wang, Mingda Chen, Ming Deng, et al. | 北京交通大学, UCL, KCL | TOSEM 2026 | 变异测试、大语言模型、实证研究 |
| 5 | GUI Test Migration via Abstraction and Concretization (MACdroid) | Yakun Zhang, Chen Liu, Xiaofei Xie, et al. | 北京大学, SMU, NUS | TOSEM 2025 | GUI测试迁移、抽象-具体化、LLM |
| 6 | Software Security Analysis in 2030 and Beyond: A Research Roadmap | Marcel Böhme, Eric Bodden, Tevfik Bultan, et al. | MPI-SP, Paderborn, UCSB, ICL, NTU, Salerno | TOSEM 2025 | 软件安全、路线图、未来方向 |
| 7 | SGAgent: Suggestion-Guided LLM-Based Multi-Agent Framework for Repository-Level Software Repair | Quanjun Zhang, Chengyu Gao, Yu Han, et al. | 南京大学 | TOSEM 2026 | 多智能体、程序修复、知识图谱 |
| 8 | GiantRepair: Hybrid Automated Program Repair Combining LLMs and Program Analysis | Li Fengjie, Jiang Jiajun, Sun Jiajun, Zhang Hongyu | 天津大学, 重庆大学 | TOSEM 2025 | 程序修复、LLM+程序分析、混合方法 |
| 9 | A-ProS: Towards Reliable Autonomous Programming Through Multi-Model Feedback | Anika Tabassum, Md Sifat Hossain, et al. | 美方学术机构 | TOSEM 2026 | 自主编程、多模型反馈、竞赛编程 |
| 10 | DEVLoRe: Integrating Various Software Artifacts for Better LLM-based Bug Localization and Program Repair | Qiong Feng, Xiaotian Ma, Jiayi Sheng, et al. | 武汉大学 | TOSEM 2025 | 程序修复、多源信息融合、故障定位 |
| 11 | Assessing the Latent APR Capabilities of LLMs using Round-Trip Translation | Fernando Vallecillos Ruiz, et al. | Simula Research Lab | TOSEM 2025 | 程序修复、往返翻译、零样本 |
| 12 | Unveiling the Role of ChatGPT in Software Development (DevChat) | Ruiyin Li, Peng Liang, et al. | 武汉大学, NTU, 华中师范大学 | TOSEM 2026 | 实证研究、ChatGPT、开发实践 |
| 13 | Fine-Tuning LLMs to Improve Accuracy and Comprehensibility of Automated Code Review | Yongda Yu, Guoping Rong, He Zhang, et al. | 南京大学 | TOSEM 2025 | 代码审查、LLM微调、质量评估 |
| 14 | C2\|Q>: A Robust Framework for Bridging Classical and Quantum Software Development | Boshuai Ye, Arif Ali Khan, et al. | University of Oulu, 武汉大学 | TOSEM 2026 | 量子软件工程、经典-量子桥接 |
| 15 | Fault-Tolerant Design and Multi-Objective Model Checking for Real-Time DRL Systems | Guoxin Su, Thomas Robinson, et al. | UoW, NUS | TOSEM 2026 | 形式化验证、DRL、容错设计 |

---

> **报告作者声明**：本报告基于公开可获取的论文摘要、arXiv预印本及机构新闻稿撰写，力求准确反映原论文的核心贡献。由于部分论文在撰写时尚未正式出版或仅提供预印本，具体细节可能以最终出版版本为准。论文索引中的URL超链接指向arXiv预印本或ACM Digital Library页面。

> **报告日期**：2026年6月