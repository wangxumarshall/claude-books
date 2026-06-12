# ICSE 2026 洞察报告（系统软件相关Track）

> **会议全称**：IEEE/ACM 48th International Conference on Software Engineering (ICSE 2026)
>
> **时间地点**：2026年4月12日–18日，巴西里约热内卢（Rio de Janeiro, Brazil）
>
> **级别**：CCF-A类，软件工程领域旗舰会议

---

## 0. 会议概览

### 0.1 基本信息

ICSE（International Conference on Software Engineering）是软件工程领域历史最悠久、影响力最大的国际学术会议，自1975年创办以来已成功举办48届。ICSE 2026于2026年4月12日至18日在巴西里约热内卢召开，是该会议首次在南美洲举办。

### 0.2 关键数据

| 指标 | 数值 |
|------|------|
| 有效投稿数 | 1,469篇 |
| 接收论文数 | 321篇 |
| **录用率** | **~21.85%** |
| ACM SIGSOFT杰出论文奖 | 22篇（占录用论文6.9%，占投稿1.5%） |
| 主要Track | Technical Track, SEIP (Software Engineering in Practice), NIER, Doctoral Symposium |

其中第二轮投稿809篇，直接录用72篇，直接录用率约为8.9%，竞争极其激烈。

### 0.3 主要议题（系统软件视角）

ICSE 2026的官方大会议题包括：
- **Testing and Analysis**（测试与分析）
- **Dependability and Security**（可靠性与安全）
- **AI for Software Engineering**（AI赋能软件工程）
- **Software Engineering for AI**（面向AI的软件工程）
- **Architecture and Design**（架构与设计）
- **Evolution**（演化与维护）

本报告聚焦于系统软件相关的Track，精选约30篇论文，从**软件测试与Fuzzing**、**程序分析与验证**、**调试与性能工程**、**AI+SE交叉**四个维度展开深入解读。

### 0.4 中国高校表现

2026年中国高校在ICSE上表现亮眼，获多个ACM SIGSOFT杰出论文奖：
- **北京大学**：HoarePrompt（杰出论文奖）、SEAlign（杰出论文奖）、Argus、Attention Distance
- **浙江大学**：TypeUp（杰出论文奖）
- **北京理工大学**：Evaluating Generated Commit Messages with LLMs（杰出论文奖）
- **扬州大学**：LoopRepair（杰出论文奖）
- **南开大学**：3篇SEIP Track（OScope、R-Log等）
- **华中科技大学/重庆大学**：InterFuzz（Java编译器Fuzzing）
- **上海交通大学**：EvoC2Rust（C-to-Rust翻译）
- **复旦大学**：WarpL（WebAssembly性能调试）

---

## 1. 软件测试与Fuzzing

### 1.1 Fuzzing技术创新

#### InterFuzz：面向复杂类间结构的Java编译器模糊测试
- **作者**：邱士煜、文明、谢子凡、金海（华中科技大学 / 重庆大学）
- **Track**：Technical Track
- **核心贡献**：提出了首个面向Java优化编译器中复杂类间结构的Fuzzing框架InterFuzz。引入**异构程序图（Heterogeneous Program Graph, HPG）**概念抽象与操纵类间关系，设计了**类间变异器（Inter-Class Mutators）**系统性地构造复杂类间交互，使用**图复杂度（Graph Complexity）**作为生成指导指标。在HotSpot、ART、R8等生产级编译器中发现24个新漏洞，其中20个已被开发者确认，16个与复杂类间结构直接相关。
- **启示**：编译器测试正从方法内、类内测试向跨类、跨模块的复杂结构测试演进，图结构抽象在此发挥关键作用。

#### On Interaction Effects in Greybox Fuzzing
- **作者**：Konstantinos Kitsios, Marcel Böhme, Alberto Bacchelli（MPI-SP / University of Zurich）
- **Track**：Technical Track
- **核心贡献**：首次识别并利用灰盒Fuzzing中变异算子之间的**交互效应（Interaction Effects）**。现有Fuzzer将各变异算子视为独立操作，但该研究发现不同变异算子之间存在显著的协同/拮抗关系，合理利用这些交互效应可以显著提升Fuzzing效率。
- **启示**：Fuzzing的变异策略设计需要从"原子操作"思维转变为"交互组合"思维。

#### Scaling Security Testing by Addressing the Reachability Gap
- **作者**：Gaetano Sapia, Marcel Böhme（MPI-SP）
- **Track**：Technical Track
- **核心贡献**：研究如何配置并与任意软件系统交互，以执行特定目标功能并运行in-vivo fuzzing。核心解决"可达性差距"（Reachability Gap）——即Fuzzer难以使目标代码被实际执行的问题。
- **启示**：Fuzzing的前沿从"如何生成好的输入"延伸到了"如何让程序到达目标位置"。

#### Attention Distance：基于大语言模型的定向Fuzzing距离度量
- **作者**：Bin Wang等（北京大学 李辉教授团队）
- **Track**：Technical Track
- **核心贡献**：提出**Attention Distance**——一种新的定向Fuzzing距离度量，将LLM对代码语义关系的理解能力引入定向灰盒Fuzzing。通过为代码语句赋予上下文感知的注意力分数，生成更具区分度的路径引导信号。在38个真实漏洞复现实验中，仅替换AFLGo的距离度量即实现平均**3.43倍**效率提升，相比DAFL和WindRanger分别提升**2.89倍**和**7.13倍**。
- **启示**：LLM的语义理解能力可以作为传统程序分析方法的"增强外挂"，而非替代品。

#### LSC-Fuzz：基于贝叶斯优化的FPGA逻辑综合编译器Fuzzing
- **作者**：Zhihao Xu, Shikai Guo等（大连海事大学）
- **Track**：Technical Track（推测）
- **核心贡献**：面向FPGA逻辑综合编译器的引导式变异Fuzzing方法。通过**代码差分引导（Code Difference Guided）**策略与**贝叶斯优化（Bayesian Optimization）**选择多样性种子，结合等价性检查检测编译器缺陷。3个月内发现16个Bug，12个已被官方确认。
- **启示**：硬件编译器的测试正成为Fuzzing的新战场，等价性检查是关键的测试预言（Test Oracle）。

### 1.2 测试生成技术

#### TestWeaver：基于执行感知反馈的LLM回归测试生成
- **作者**：Cuong Chi Le, Cuong Duc Van等（University of Texas at Dallas）
- **Track**：Technical Track
- **核心贡献**：提出TestWeaver，将轻量级程序分析集成到LLM测试生成流程中，通过三种机制克服LLM在复杂执行推理上的局限：（1）向后切片替代完整程序上下文以减少幻觉；（2）识别具有控制流相似性的近邻测试用例以提供聚焦执行上下文；（3）以内联注释编码变量状态以增强执行推理。在代码覆盖增长速度和测试有效性上显著优于SOTA。
- **启示**：测试生成的瓶颈不在于LLM"是否会写代码"，而在于"是否理解程序如何执行"。

#### SAINT：面向企业Java应用的白盒测试方法
- **作者**：ICSE 2026 Research Track论文
- **核心贡献**：结合静态分析 + LLM + LLM智能体，自动生成端点和场景级测试用例。构建端点模型（捕获语义信息）和操作依赖图（捕获调用约束），通过智能体的规划-行动-反思循环将代码逐步精炼为可执行测试。开发者调研给予强烈认可。
- **启示**：多智能体协同测试正成为新一代测试自动化的核心范式。

### 1.3 软件供应链与安全测试

#### Six Million (Suspected) Fake Stars on GitHub
- **作者**：CMU、NC State、Socket Inc.联合团队
- **Track**：Technical Track
- **核心贡献**：通过StarScout工具分析2019-2024年20TB GitHub元数据（67亿事件、3.26亿次Star），发现约**600万颗疑似假Star**、18,617个涉事仓库、30.1万个参与账号。2024年7月峰值时，50+ Star仓库中16.66%涉及假Star活动。AI/LLM项目成为最大非恶意假Star接收方（17.7万颗），78个涉假仓库曾登上GitHub Trending。被标记仓库中90.42%已被GitHub删除。论文公开了StarScout源码和数据集。
- **启示**：开源生态的"信任指标"正在被系统性操纵，亟需新的可信度评估机制。

---

## 2. 程序分析与验证

### 2.1 形式化验证与程序等价性

#### Heimdall：eBPF程序到Rust的形式化验证自动迁移
- **作者**：Vishnu Asutosh Dasu, Gang Tan等（Penn State / UIC）
- **Track**：Technical Track
- **核心贡献**：提出Heimdall，使用LLM将legacy libbpf C程序翻译为Aya Rust程序，并通过**符号执行（angr）**和**Z3等价性验证**证明翻译后程序与原始程序行为等价。在102个eBPF程序上实现94.1%的形式化等价翻译率。同时首次系统性地记录了6类通过内核验证器但仍可导致信息泄露的eBPF源码级缺陷。
- **启示**：将LLM代码翻译与形式化验证结合，为安全关键系统软件的迁移提供了可行性路径。

#### HoarePrompt：用自然语言进行程序正确性结构化推理
- **作者**：Dimitris Bouras, Sergey Mechtaev（北京大学）
- **Track**：Technical Track，**ACM SIGSOFT杰出论文奖**
- **核心贡献**：研究LLM是否能够判断一个程序是否符合自然语言规范。直接让LLM判断程序正确性效果较差，因为模型难以准确推理程序语义。HoarePrompt通过传播可达程序状态的自然语言描述，构建类似**Hoare逻辑的非形式化推理轨迹**来总结程序行为。实验表明这种结构化推理方式显著提升程序正确性分类能力。
- **启示**：程序验证中的"形式化"与"自然语言"可以互补——用自然语言模拟形式化推理框架。

### 2.2 静态分析与缺陷检测

#### CodeCureAgent：静态分析告警的自动分类与修复
- **作者**：Pascal Joos, Islem Bouzenia, Michael Pradel（CISPA）
- **Track**：Technical Track（推测）
- **核心贡献**：提出基于LLM智能体的静态分析告警处理框架CodeCureAgent。与以往局限于特定分析规则的方法不同，该框架采用**智能体框架（Agentic Framework）**迭代调用工具收集代码库信息并编辑代码。在1,000个SonarQube告警、106个Java项目、291条规则上达到96.8%的可信修复率（Plausible Fix Rate），正确修复率为86.3%。每次修复成本仅2.9美分，端到端处理时间约4分钟。
- **启示**：AI驱动的静态分析告警修复已接近实用化门槛。

#### Dependency-aware Residual Risk Analysis
- **作者**：Seongmin Lee, Marcel Böhme（MPI-SP）
- **Track**：Technical Track
- **核心贡献**：首次在残余风险估计中考虑覆盖元素之间的**依赖性（Dependencies）**。传统方法将代码覆盖元素视为独立，但这忽略了执行路径间的依赖结构，导致风险估计偏差。
- **启示**：程序分析的"独立性假设"是需要被挑战的——代码元素之间的依赖关系蕴含着关键信息。

#### Argus：基于多智能体的敏感信息泄露检测框架
- **作者**：Bin Wang等（北京大学 李辉教授团队）
- **Track**：Technical Track
- **核心贡献**：提出Argus协同多智能体检测框架，在三个层次上进行联合分析：敏感信息内容本身、文件级上下文语义、项目级引用关系。通过多智能体任务分工与协作，有效降低误报率。论文同时引入两个面向真实仓库场景的基准数据集。
- **启示**：层次化多智能体架构是解决代码安全检测中高误报率问题的有效路径。

---

## 3. 调试与性能工程

### 3.1 操作系统与运行时调试

#### OScope：基于LLM的操作系统故障诊断
- **作者**：赵咏欣、张圣林等（南开大学 / 阿里巴巴 / 清华大学）
- **Track**：SEIP Track
- **核心贡献**：提出OScope——基于LLM的自动化可解释操作系统故障诊断框架。四大核心模块：（1）预处理与特征提取模块；（2）**知识对齐与检索模块**（领域微调的"知识对齐器"）；（3）**SOP指导的诊断模块**（思维链推理 + 报告验证）；（4）**交互式解释与优化模块**（人机协同）。在阿里巴巴生产环境中，AC@5达到90.1%，较最优基线提升约20%。已部署运行超过三个月，成功诊断67个关键故障，平均诊断耗时从人工的112分钟降至**1.5分钟**。
- **启示**：LLM+领域知识库+人机协同是工业级故障诊断的可行路径，"人在环路"（Human-in-the-Loop）机制是增强信任的关键。

#### R-Log：基于推理强化学习的日志分析
- **作者**：刘逸伦、陈子昂等（南开大学 / 华为）
- **Track**：Technical Track
- **核心贡献**：提出R-Log——基于推理的强化学习日志分析范式。从运维实践中提炼**13套推理模板**覆盖五类日志分析任务（日志解析、异常检测、日志解释、根因分析、解决方案推荐）。采用**双阶段训练架构**：监督微调冷启动 + GRPO强化学习优化。在五项任务上超越DeepSeek-V3.1、Qwen3-235B等最优基线，**未见场景中提升高达228.05%**。同时设计了速度提升5倍、保留93%效果的R-Log-fast工业版。
- **启示**：模仿人类"先思考、后回答"的结构化推理是缓解LLM日志分析"幻觉"的有效策略。

#### TAAF：融合知识图谱与LLM的Trace分析框架
- **作者**：Alireza Ezaz等（Brock University）
- **Track**：Technical Track
- **核心贡献**：提出TAAF（Trace Abstraction and Analysis Framework），结合时间索引、**知识图谱（KG）**和**LLM**将原始Trace数据转化为可操作的洞察。构建时间索引知识图谱捕获线程、CPU、系统资源等实体关系，LLM解释查询特定子图以回答自然语言问题。引入TraceQA-100基准（100个基于真实内核Trace的问题），相较于纯LLM提升准确率最高31.2%，特别在多跳推理和因果推理任务中效果显著。
- **启示**：KG+LLM的混合架构是处理大规模系统Trace的分析新范式。

### 3.2 性能分析与调试

#### WarpL：基于变异的WebAssembly运行时性能调试
- **作者**：Ruiying Zeng, Shuyao Jiang等（复旦大学 / 香港中文大学）
- **Track**：Technical Track
- **核心贡献**：提出WarpL——面向Wasm运行时性能问题的变异推断方法。通过**细粒度Wasm字节码变异**获得功能等价但不表现性能问题的变异体，比较原始程序与变异体的机器码来**隔离次优指令序列**。在3个主流Wasm运行时的12个真实性能问题中成功定位10个根因，并诊断出Wasmtime中的6个此前未知性能问题。
- **启示**：变异测试的思想可以迁移到性能调试领域，等价变异体对比是精确定位性能缺陷的有效手段。

#### LQPR：自动化性能需求量化
- **作者**：Shihai Wang, Tao Chen（University of Birmingham）
- **Track**：Technical Track
- **核心贡献**：提出LQPR——一种高效的自动化性能需求量化方法。观察到性能需求具有强模式且通常短小精悍，设计了一种**轻量级语言诱导匹配机制**（Lightweight Linguistically Induced Matching），将量化问题转化为分类问题。与9种SOTA方法对比，在75%以上的案例中排第一，且成本低两个数量级。
- **启示**：专精方法在特定任务上可以超越通用LLM——"Heavy is not always better"。

---

## 4. AI+SE交叉

### 4.1 AI软件工程智能体

#### USEagent：统一软件工程智能体
- **作者**：Leonhard Applis, Yuntong Zhang等（NUS / Purdue）
- **Track**：Technical Track
- **核心贡献**：提出USEagent——第一个面向通用软件工程任务的统一智能体。与现有面向特定任务（测试、调试、修复）的专业化智能体不同，USEagent能够编排多种能力处理软件开发中的复杂场景。构建USEbench基准（1,271个仓库级软件工程任务），在问题修复方面与AutoCodeRover等专业智能体相当，同时适用更广泛的任务。
- **启示**：从"专才智能体"到"通才智能体"是AI软件工程师进化的关键转折。

#### SEAlign：面向软件工程智能体的对齐训练
- **作者**：北京大学团队
- **Track**：Technical Track，**ACM SIGSOFT杰出论文奖**
- **核心贡献**：提出SEAlign对齐框架，核心洞察：软件工程智能体的成败取决于一系列中间决策，训练目标不应只关注最终代码是否正确，而应显式优化模型在关键步骤上的行为选择。识别出三类行为失配：指令跟随不足、工具调用错误、重复循环。经过SEAlign优化后的14B参数开源模型在SWE-bench上显著领先同体量模型甚至媲美顶级闭源模型。
- **启示**：软件工程智能体的后训练需要从"代码生成对齐"转向"决策过程对齐"。

#### EmbedAgent：评估LLM在嵌入式系统开发中的能力
- **作者**：Ruiyang Xu, Jialun Cao等（中国科学院软件所 / 港科大 / 鹏城实验室）
- **Track**：Technical Track
- **核心贡献**：提出EmbedAgent范式，模拟嵌入式系统开发中的真实角色（Embedded System Programmer、Architect、Integrator），构建EmbedBench——首个面向嵌入式系统编程、电路设计和跨平台迁移的综合基准（126个案例、9种电子元器件、3个硬件平台）。在10个主流LLM上实验发现：即使案例简单，DeepSeek-R1在有电路图信息时pass@1仅55.6%，自设计电路时仅50.0%。跨平台迁移任务中，MicroPython表现较好（73.8%），ESP-IDF最差（仅29.4%）。通用对话LLM往往无法利用相关预训练知识，而推理LLM倾向于"过度思考"。
- **启示**：嵌入式系统是当前LLM能力的显著短板，RAG和编译器反馈是有效的增强策略。

### 4.2 自动程序修复（APR）与调试

#### LoopRepair：位置感知与轨迹引导的迭代式漏洞修复
- **作者**：叶振雷等（扬州大学）
- **Track**：Technical Track，**ACM SIGSOFT杰出论文奖**
- **核心贡献**：提出LoopRepair，创新性地采用**先预测修复位置、后预测修复内容**的迭代式修复策略，并提供基于测试失败补丁质量评估的迭代优化机制。相比SOTA，在41个真实漏洞数据集中多修复8-13个额外漏洞。
- **启示**："先定位后修复"的分解策略符合人类调试思维，显著优于"一步到位"的直接生成。

#### DebugRepair：基于自主调试的LLM程序修复增强
- **作者**：Linhao Wu, Yifei Pei等（北京大学 / 清华大学等）
- **Track**：Technical Track（推测）
- **核心贡献**：提出DebugRepair——自主调试驱动的程序修复框架，通过三组件（测试语义纯化、模拟插桩、调试驱动对话式修复）利用**中间运行时状态证据**增强补丁精化。在Defects4J上，GPT-3.5配合DebugRepair正确修复224个Bug（超越SOTA 26.2%），DeepSeek-V3配合修复295个Bug，通用提升51.3%。
- **启示**：运行时中间状态信息是LLM程序修复的关键缺失拼图。

#### DynaFix：执行级动态信息驱动的迭代APR
- **作者**：Zhili Huang, Ling Xu等（重庆大学等）
- **核心贡献**：提出DynaFix，在每个修复轮次中捕获**变量状态、控制流路径和调用栈**等执行级动态信息，转化为结构化提示引导LLM生成候选补丁。若验证失败则重新执行修改后程序收集新信息。在Defects4J v1.2和v2.0上修复186个单函数Bug（提升10%），包括38个此前未修复的Bug。
- **启示**：迭代式动态反馈循环正在成为LLM程序修复的标准范式。

#### EvolRepair：基于种群的语义进化APR框架
- **作者**：Cuong Chi Le等（UT Dallas）
- **核心贡献**：将LLM-based APR重新表述为**语义进化算法**，用LLM驱动的语义感知组件替代传统遗传算法的语法操作符。候选修复被组织为行为一致的组，算法可以保留多样性、推理修复家族、并通过重组互补修复洞察合成更强候选。
- **启示**：进化算法与LLM的深度融合为APR开辟了新的搜索范式。

#### SpecTune：基于规约引导的调试框架
- **作者**：Minh Le-Anh, Cuong Chi Le等（UT Dallas）
- **核心贡献**：提出SpecTune，将修复任务分解为由执行检查点连接的可疑区域，并推导局部后置条件表示预期程序行为。引入两个互补信号：规约验证信号（α）估计生成后置条件的一致性，判别信号（β）检测已验证后置条件在执行中的违规。
- **启示**：自动生成的中间规约即使不完美，也能为APR提供有价值的调试信号。

#### What's in a Benchmark? The Case of SWE-Bench in APR
- **作者**：Matias Martinez, Xavier Franch（UPC）
- **Track**：SEIP Track
- **核心贡献**：首次全面研究SWE-Bench Lite和Verified两个排行榜，分析79个Lite提交和133个Verified提交。发现大多数提交来自工业界（尤其是小型公司和大型上市公司），学术界多为开源贡献。Claude系列模型占主导地位，Claude 4 Sonnet取得了顶级成绩。
- **启示**：评测基准本身的生态正在深刻影响APR研究的方向和方法。

### 4.3 AI+SE工具与应用

#### TypeUp：即时Python类型注解更新
- **作者**：薛志鹏、高志鹏、夏鑫等（浙江大学）
- **Track**：Technical Track，**ACM SIGSOFT杰出论文奖**
- **核心贡献**：提出基于大模型的即时（Just-In-Time）类型注解更新方法TypeUp，在代码变更时自动生成新的类型注解。性能优于SOTA类型推断方法41.9%，在真实开源项目中25条更新中20条已被开发者采纳。这是浙大团队继ICSE 2024、FSE/ISSTA 2025后连续第三年获得软件工程顶会杰出论文奖。
- **启示**：Python类型系统的演进为AI辅助代码维护提供了实际的应用场景。

#### Evaluating Generated Commit Messages with LLMs
- **作者**：曾群鸿、张宇霞、刘辉等（北京理工大学）
- **Track**：Technical Track，**ACM SIGSOFT杰出论文奖**
- **核心贡献**：首次系统验证了利用LLM直接评估提交信息质量的可行性。"变更内容（What）"维度Spearman相关系数达0.65，"变更原因（Why）"维度达0.78，接近人类一致性水平。相比BLEU、ROUGE-L、METEOR等传统指标在两个维度上均显著更优。
- **启示**：LLM作为一种"语义评估器"的价值可能不亚于其作为"内容生成器"的价值。

#### EvoC2Rust：项目级C到Rust翻译框架
- **作者**：Chaofan Wang, Xiaodong Gu等（上海交通大学）
- **Track**：SEIP Track
- **核心贡献**：提出EvoC2Rust——基于骨架引导的项目级C到Rust翻译框架。针对大型C项目向Rust迁移的实际工业需求，利用骨架引导策略确保翻译过程的结构一致性和功能完整性。
- **启示**：系统软件语言的现代化迁移（C→Rust）正在成为重要的SE研究课题。

#### FaultLine：基于LLM智能体的PoV测试生成
- **作者**：Vikram Nitin等（Columbia University / Microsoft）
- **Track**：Technical Track
- **核心贡献**：提出FaultLine——LLM智能体工作流，通过精心设计的推理步骤（数据流推理、控制流推理、测试生成与修复循环），自动生成漏洞证明（PoV）测试用例。在100个跨语言（Java/C/C++）已知漏洞数据集上比CodeAct 2.1提升了77%。
- **启示**：层次化推理（Hierarchical Reasoning）是增强LLM智能体在复杂安全任务上表现的有效策略。

### 4.4 新兴方向

#### 软件工程公平性鲁棒性评估
- **作者**：Verya Monjezi等（UIC / Penn State / CU Boulder）
- **Track**：Technical Track
- **核心贡献**：基于因果理论的ML软件公平性实践鲁棒性评估框架。将公平性实践规范为一阶逻辑属性，利用因果图表示和搜索算法探索等价因果图，识别在噪声、错误标注和人口统计偏移等因素下保持鲁棒性的最佳实践。
- **启示**：软件公平性正从"设计时保证"走向"系统性鲁棒性测试"。

#### On the Robustness of Fairness Practices
- 结合前述公平性研究，ICSE 2026展现出对AI系统非功能性属性（公平性、可解释性、鲁棒性）的深入关注。

---

## 5. 结语与未来方向

### 5.1 ICSE 2026系统软件领域关键趋势

1. **LLM从"替代工具"到"增强外挂"**：大量工作表明，LLM与程序分析、形式化验证、符号执行的深度融合是当前最有效路径，而非简单的端到端替代。HoarePrompt、Attention Distance、Heimdall等工作都体现了这一理念。

2. **智能体化测试与修复**：从单一LLM调用到多智能体协同（Argus、SAINT、USEagent），从一次性生成到迭代反馈循环（DebugRepair、DynaFix、TestWeaver），测试与修复正在变得更加"自主化"。

3. **系统软件的AI融合**：操作系统故障诊断（OScope）、嵌入式系统开发（EmbedAgent）、WebAssembly运行时优化（WarpL）、eBPF程序迁移（Heimdall）——AI正在深入系统软件栈的各个层面。

4. **可靠性与可信度再定义**：GitHub假星研究揭示了开源生态系统的信任危机，LQPR证明了轻量方法的优越性，CodeCureAgent展示了告警修复的实用化——都在呼唤新的可信度评估机制。

5. **从"覆盖"到"语义"的范式转移**：Attention Distance用语义距离替代物理距离指导Fuzzing，HoarePrompt用自然语言模拟形式化推理——语义理解正在成为测试与分析的核心驱动力。

6. **中国高校全面崛起**：22个杰出论文奖中中国高校获得多个，且在系统软件相关的Fuzzing、日志分析、故障诊断、程序修复、类型系统等方向均有高质量产出。

### 5.2 值得关注的开放方向

- **LLM+符号执行的深度耦合**：目前多停留在"LLM辅助生成输入"层面，如何让LLM直接参与约束求解和路径探索仍待突破。
- **多语言/跨平台系统测试**：EmbedAgent已揭示LLM在跨平台嵌入式迁移中的显著不足，有待进一步提升。
- **工业级部署的验证闭环**：OScope和R-Log的成功表明，"冷启动→部署→反馈→迭代"的闭环是工业级AI落地的关键。
- **开源生态的可信度量**：假星问题暴露了开源评价体系的脆弱性，需要新的多维可信度评估框架。
- **AI编译器的系统化测试**：Qingchao Shen的博士论坛工作已发现266个AI编译器新Bug，该方向仍有巨大空间。

---

## 论文索引表

| 编号 | 论文标题 | 作者（第一/通讯单位） | Track | 获奖/备注 |
|------|----------|----------------------|-------|-----------|
| 1 | InterFuzz: Fuzzing Java Optimizing Compilers with Complex Inter-Class Structures | 邱士煜/文明 (华中科技大学) | Technical | — |
| 2 | On Interaction Effects in Greybox Fuzzing | Kitsios/Böhme (MPI-SP) | Technical | — |
| 3 | Scaling Security Testing by Addressing the Reachability Gap | Sapia/Böhme (MPI-SP) | Technical | — |
| 4 | Attention Distance: A Novel Metric for Directed Fuzzing with LLMs | Wang/李辉 (北京大学) | Technical | — |
| 5 | LSC-Fuzz: Code Difference Guided Fuzzing for FPGA Logic Synthesis Compilers | Xu/Guo (大连海事大学) | Technical | — |
| 6 | TestWeaver: Execution-aware, Feedback-driven Regression Testing with LLMs | Le/Nguyen (UT Dallas) | Technical | — |
| 7 | Six Million (Suspected) Fake Stars on GitHub | CMU/NC State/Socket | Technical | 引发广泛关注 |
| 8 | Heimdall: Formally Verified Migration of eBPF Programs to Rust | Dasu/Tan (Penn State) | Technical | — |
| 9 | HoarePrompt: Structural Reasoning About Program Correctness | Bouras/Mechtaev (北京大学) | Technical | 🏆 杰出论文奖 |
| 10 | CodeCureAgent: Automatic Classification and Repair of Static Analysis Warnings | Joos/Pradel (CISPA) | Technical | — |
| 11 | Dependency-aware Residual Risk Analysis | Lee/Böhme (MPI-SP) | Technical | — |
| 12 | Argus: Multi-Agent Sensitive Information Leakage Detection | Wang/李辉 (北京大学) | Technical | — |
| 13 | OScope: When LLMs Listen to Experts — Failure Diagnosis in OS | 赵咏欣/张圣林 (南开大学/阿里/清华) | SEIP | 工业部署 |
| 14 | R-Log: Incentivizing Log Analysis in LLMs via Reasoning-based RL | 刘逸伦/张圣林 (南开大学/华为) | Technical | — |
| 15 | TAAF: Trace Abstraction and Analysis Framework with KG and LLMs | Ezaz (Brock University) | Technical | — |
| 16 | WarpL: Debugging Performance Issues in WebAssembly Runtimes | Zeng/Zhou (复旦大学/CUHK) | Technical | — |
| 17 | LQPR: Light over Heavy — Automated Performance Requirements Quantification | Wang/Chen (U. Birmingham) | Technical | — |
| 18 | USEagent: Unified Software Engineering Agent | Applis/Roychoudhury (NUS/Purdue) | Technical | — |
| 19 | SEAlign: Alignment Training for Software Engineering Agent | 北京大学 | Technical | 🏆 杰出论文奖 |
| 20 | EmbedAgent: Benchmarking LLMs in Embedded System Development | Xu/Sun (中科院软件所/港科大) | Technical | — |
| 21 | LoopRepair: Location-Aware and Trace-Guided Iterative Vulnerability Repair | 叶振雷 (扬州大学) | Technical | 🏆 杰出论文奖 |
| 22 | DebugRepair: Enhancing LLM-Based APR via Self-Directed Debugging | Wu/Hao (北京大学) | Technical | — |
| 23 | DynaFix: Iterative APR Driven by Execution-Level Dynamic Information | Huang/Zhang (重庆大学) | Technical | — |
| 24 | EvolRepair: Semantic Evolution over Populations for LLM-Guided APR | Le/Nguyen (UT Dallas) | Technical | — |
| 25 | SpecTune: Enhancing Program Repair with Specification Guidance | Le-Anh/Nguyen (UT Dallas) | Technical | — |
| 26 | TypeUp: Automating Just-In-Time Python Type Annotation Updating | 薛志鹏/夏鑫 (浙江大学) | Technical | 🏆 杰出论文奖 |
| 27 | Evaluating Generated Commit Messages with LLMs | 曾群鸿/张宇霞/刘辉 (北理工) | Technical | 🏆 杰出论文奖 |
| 28 | What's in a Benchmark? The Case of SWE-Bench in APR | Martinez/Franch (UPC) | SEIP | — |
| 29 | EvoC2Rust: Skeleton-guided Framework for Project-Level C-to-Rust | Wang/Gu (上海交通大学) | SEIP | — |
| 30 | FaultLine: Automated Proof-of-Vulnerability Generation using LLM Agents | Nitin/Ray (Columbia/Microsoft) | Technical | — |
| 31 | On the Robustness of Fairness Practices: A Causal Framework | Monjezi/Tizpaz-Niari (UIC) | Technical | — |
| 32 | Data-driven Test Generation for Fuzzing AI Compiler | Shen (中科院) | Doctoral Symposium | 266个新Bug |

> **注**：部分论文的Track信息基于公开资料的合理推断。CS = Technical Track (Research Track, 主会研究论文)。

---

*报告撰写日期：2026年6月10日*
*数据来源：公开学术论文（arXiv）、高校新闻稿、ACM Digital Library、会议官方网站*