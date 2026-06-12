# IEEE Transactions on Software Engineering (TSE) 2026 洞察报告

> **期刊级别**: CCF-A 类期刊, SCI 一区, 软件工程领域旗舰期刊  
> **出版商**: IEEE Computer Society  
> **覆盖时段**: 2025年6月 – 2026年6月  
> **关注方向**: 系统软件测试、验证、调试、性能分析、安全工程  
> **收录论文数**: 15篇  

---

## 0. 期刊概览

IEEE Transactions on Software Engineering（IEEE TSE）创刊于1975年，是软件工程领域历史最悠久、影响力最大的旗舰学术期刊。该期刊涵盖软件规范、设计、实现、测试、验证、可靠性模型、项目管理、工具与环境等全生命周期研究方向。2025-2026年度，TSE持续发表具有高理论深度和强实证支撑的研究成果，重点关注方向呈现以下趋势：

1. **大语言模型（LLM）与软件工程的深度融合**：LLM 被广泛用于故障定位、程序修复、代码搜索、测试生成等任务，成为软件工程工具链的核心驱动力。
2. **系统软件质量保障的自动化与智能化**：模糊测试（Fuzzing）技术持续演进，从通用程序测试扩展到协议模糊测试、数据库系统测试、编译器测试等系统软件领域。
3. **实证研究的深化与数据驱动**：大规模实证研究成为理解系统软件缺陷规律、评估工具有效性的关键方法论。
4. **跨语言、跨项目、跨领域的泛化能力**：研究者越来越关注方法的泛化性和可迁移性。

本报告精选15篇与**系统软件工程**（测试工具、验证、调试、性能分析、安全）密切相关的TSE论文，分四个主题进行系统性洞察分析。

---

## 1. 系统软件测试与验证

系统软件（如数据库、编译器、网络协议栈、并行计算框架）的正确性和可靠性直接影响上层应用生态的安全与性能。传统测试方法在面对这些复杂系统时往往力不从心，2025-2026年的TSE论文展示了一系列突破性进展。

---

### 1.1 AFLNet Five Years Later: On Coverage-Guided Protocol Fuzzing

- **作者**: Ruijie Meng, Van-Thuan Pham, Marcel Böhme, Abhik Roychoudhury
- **机构**: University of Melbourne; MPI-SP; National University of Singapore
- **发表信息**: IEEE TSE, Vol. 51, Issue 4, 2025
- **DOI**: (TSE 2025)

**技术概要**

AFLNet是首个将覆盖率引导的灰盒模糊测试应用于有状态网络协议实现的代表性工作（ICST 2020）。本文是AFLNet发表五年后的系统性回顾与扩展，对协议模糊测试的核心挑战进行了深度反思：协议实现具有状态性——同一消息序列在不同时间发送可能产生不同响应。文章提出将消息序列作为fuzzing的"种子"，将每条消息与对应的协议状态关联，同时最大化状态空间和代码空间的覆盖率。

相比原始AFLNet，新版本引入了以下关键增强：(1) 更精确的状态推断机制，基于服务器响应码自动识别协议状态转移；(2) 改进的种子能量调度策略，优先探索未覆盖的状态-代码组合；(3) 支持更多应用层协议（如HTTP/2、MQTT、TLS等）。在广泛使用的开源协议实现（如Live555、OpenSSL、TinyDTLS）上的实验表明，该方法在分支覆盖率和漏洞发现方面持续领先通用fuzzer。

**技术启示**

1. **有状态测试是系统软件测试的核心挑战**：从网络协议到数据库系统，状态空间爆炸是测试有效性的根本制约。AFLNet的设计范式——状态与代码的联合覆盖率指导——可推广至其他有状态系统软件测试。
2. **灰盒模糊测试需要领域知识注入**：纯随机的字节级变异难以穿透协议解析层，通过响应码推断、状态机学习等手段注入领域知识，能显著提升fuzzing效率。
3. **度量指标的多元性**：仅用代码覆盖率衡量fuzzing效果具有误导性，应同时考虑状态覆盖率、漏洞发现率等多维指标。

**覆盖率**：⭐⭐⭐⭐☆（协议模糊测试领域的标杆性工作，系统软件测试方向高覆盖）

---

### 1.2 ATTuzz: Better Pay Attention Whilst Fuzzing

- **作者**: Shunkai Zhu, Jingyi Wang, Jun Sun, Jie Yang, Xingwei Lin, Tianyi Wang
- **机构**: Singapore Management University; Zhejiang University; Ant Group
- **发表信息**: IEEE TSE, Vol. 50, Issue 2, 2024 (2025年收录)
- **DOI**: 10.1109/TSE.2023.3338129

**技术概要**

现有的覆盖率引导灰盒模糊测试（CGF）在运行一段时间后往往陷入"覆盖率平台期"——难以触发被深度嵌套条件分支保护的"困难路径"。ATTuzz提出了系统性的解决方案：(1) **轻量级动态分析**：估算每个基本块被覆盖的"奖励值"，据此选择最具潜力的种子；(2) **注意力机制驱动的变异策略**：训练一个配备注意力机制的深度学习模型，预测特定字节的特定变异能否覆盖目标"奖励块"。

ATTuzz的核心创新在于将fuzzing中的种子选择和字节级变异决策统一到一个端到端的注意力学习框架中。实验结果表明，相比AFL++，ATTuzz在24小时运行中实现了1.2倍的边覆盖率和1.8倍的漏洞发现量，并在p7zip和openUSD中发现了4个此前未知的真实漏洞。

**技术启示**

1. **覆盖率平台期的突破需要智能化引导**：传统随机变异策略在代码复杂度高的区域失效，注意力机制能够学习输入字节与程序行为之间的隐含关联。
2. **深度学习与经典fuzzing的互补性**：ATTuzz证明深度模型不需要替代传统fuzzing，而是可以作为"智能调度器"嵌入现有框架，提升探索效率。
3. **产业实用性验证**：该工作发现了多个实际软件的未知漏洞，体现了学术研究与产业应用的紧密连接。

**覆盖率**：⭐⭐⭐⭐☆（模糊测试的深度学习增强方向重要工作）

---

### 1.3 Low-Cost Testing for Path Coverage of MPI Programs Using Surrogate-Assisted Changeable Multi-Objective Optimization

- **作者**: Baicai Sun, Lina Gong, Yinan Guo, Dunwei Gong, Gaige Wang
- **机构**: 青岛科技大学; 南京航空航天大学; 中国矿业大学（北京）; 中国海洋大学
- **发表信息**: IEEE TSE, 2025
- **DOI**: 10.1109/TSE.2025.3635120

**技术概要**

消息传递接口（Message Passing Interface, MPI）编程模型是高性能计算（HPC）领域的核心并行编程范式。MPI程序的一条路径通常由多个进程上的若干子路径构成，有些子路径覆盖条件苛刻，导致基于智能优化算法的测试用例生成效率低下。本文提出了一种基于**代理模型辅助可变多目标优化**的低成本测试方法：

1. 建立MPI程序路径覆盖测试用例生成问题的**可变多目标优化模型**，动态调整优化目标维度；
2. 在进化过程中**识别每条难覆盖的子路径**，形成对应的训练样本集；
3. 为每条难覆盖子路径管理和维护独立的**代理模型**（Surrogate Model），用代理模型预测代替部分实际程序执行；
4. 选择性能优越的进化个体执行实际MPI程序，大幅降低程序执行的次数和计算成本。

实验在多个典型MPI基准程序上进行，结果表明该方法在测试用例生成的有效性和效率上显著优于现有先进方法。

**技术启示**

1. **并行程序的测试成本是一个被低估但至关重要的问题**：HPC程序单次执行可能耗费大量计算资源，代理模型辅助的测试方法通过"少执行、多预测"策略有效降低测试开销。
2. **可变维度优化**：MPI程序的路径覆盖涉及可变数量的进程和子路径，传统的固定维度优化框架无法直接适用，该工作对可变维度问题建模的方法值得借鉴。
3. **国产替代场景下的基础软件测试需求**：随着国产HPC生态的发展，基于MPI的并行程序测试将成为质量保障的关键环节。

**覆盖率**：⭐⭐⭐☆☆（HPC/并行软件测试的稀缺方向，但应用面相对狭窄）

---

### 1.4 Improving Retrieval-Augmented Deep Assertion Generation via Joint Training

- **作者**: 张犬俊等
- **机构**: 南京大学 iSE 实验室
- **发表信息**: IEEE TSE, 2025 (全文录用)
- **相关论文**: ISSTA 2025, TOSEM 2025

**技术概要**

单元测试中的断言（Assertion）生成是测试预言问题的核心挑战。虽然大语言模型在代码理解方面表现出色，但现有方法通常将检索器和生成器视为两个独立组件，未能发挥二者的协同作用。本文提出的AG-RAG创新性地引入**联合训练策略**，将断言检索器和生成器作为一个整体进行联合优化：

1. **检索器**从外部代码库中检索与被测函数相关的断言知识；
2. **生成器**基于检索到的断言知识和被测函数代码生成精确断言；
3. 关键在于：生成器的反馈信号被**回传至检索器**，使检索器能够自适应调整检索策略，以获取对生成更有价值的外部知识。

这种"检索即学习"（Retrieval-as-Learning）的范式显著提升了断言生成的精准度。相关工作已集成至华为开发者工具并投入使用。

**技术启示**

1. **检索增强生成（RAG）的端到端训练是突破瓶颈的关键**：分离式的RAG架构中，检索器无法感知下游生成任务的需求，联合训练填补了这一gap。
2. **测试预言（Test Oracle）问题仍是测试自动化的最大障碍**：断言生成本质上是对程序行为正确性的判定，该工作从信息检索视角提供了新思路。
3. **学术成果向工业工具的快速转化**：该系列研究的落地体现了大语言模型在软件测试领域的实际价值。

**覆盖率**：⭐⭐⭐⭐☆（断言生成方向的系统工作，工业落地验证充分）

---

### 1.5 A Comprehensive Study of Bugs in Relational DBMS

- **作者**: 刘爽（中国人民大学）& OceanBase 团队
- **机构**: 中国人民大学; OceanBase（蚂蚁集团）
- **发表信息**: IEEE TSE, 2025（正式录用）

**技术概要**

本文是首个面向开源关系型数据库系统（RDBMS）的大规模细粒度缺陷实证研究。研究覆盖MySQL、SQLite和openGauss三大系统中2018-2023年间报告的2495个缺陷，经严格筛选后构建了包含777个高质量修复缺陷的数据集。

研究提出了一套四维分析框架：
- **根因维度**：识别出12类缺陷根本原因，其中「不正确的代码逻辑」占比最高（32.3%），「类型处理缺陷」（9.0%）和「API误用」（8.4%）分别位列第二、第三；
- **症状维度**：「结果不一致」是最普遍的症状（42.99%），且往往无崩溃、无报错，具有极强的隐蔽性；
- **模块维度**：定位缺陷修复位置（解析器、优化器、执行引擎、存储层等）；
- **关联性维度**：探索根因-症状-模块三者之间的关联规律。

研究还开发了概念验证工具SQLT，针对性挖掘类型相关缺陷，在实验中新发现8个此前未被报告的问题，其中5个已被MySQL、SQLite和openGauss官方确认并修复。

**技术启示**

1. **数据库缺陷具有"静默性"特点**：超过40%的缺陷表现为结果不一致而非崩溃，这对测试预言设计提出了更高要求——差分测试（Differential Testing）和蜕变测试（Metamorphic Testing）在数据库测试中具有天然优势。
2. **类型系统是数据库内核的薄弱环节**：SQL的隐式类型转换、非标准类型（如BIT、JSON）组合是缺陷高发区，针对性fuzzing策略的回报率更高。
3. **工业数据库（openGauss）与学术数据库（SQLite）的缺陷模式差异**：不同设计哲学和开发阶段的DBMS呈现不同的缺陷谱系，测试策略需要定制化。

**覆盖率**：⭐⭐⭐⭐⭐（数据库系统缺陷实证研究的开创性工作，覆盖面广、分析深入）

---

## 2. 故障定位与调试

故障定位（Fault Localization）是软件调试过程中最耗时的环节，通常占据开发者约三分之一的调试时间。2025-2026年的TSE论文展示了从基于频谱的传统方法到基于大语言模型的新范式的全面演进。

---

### 2.1 SoapFL: A Standard Operating Procedure for LLM-Based Method-Level Fault Localization

- **作者**: Yihao Qin, Shangwen Wang, Yiling Lou, Jinhao Dong, Kaixin Wang, Xiaoling Li, Xiaoguang Mao
- **机构**: 国防科技大学 复杂系统软件工程重点实验室
- **发表信息**: IEEE TSE, Vol. 51, Issue 4, 2025

**技术概要**

大语言模型（LLM）在代码理解方面展现出强大能力，为故障定位提供了新路径。然而，LLM的上下文窗口限制使得其难以直接分析大型项目中的完整代码。现有LLM-based故障定位方法往往局限于小范围代码片段，无法实现方法级别的精确定位。

SoapFL提出了一套**标准操作规程（Standard Operating Procedure, SOP）**来解决这一难题：
1. 将故障定位任务分解为多个子步骤，每个步骤针对特定的分析粒度；
2. 设计结构化的提示词（Prompt），引导LLM分阶段进行代码审查、可疑度排序和故障确认；
3. 引入外部知识（如测试用例运行结果、代码变更历史）增强LLM的上下文理解；
4. 通过多轮交互和反馈机制逐步缩小可疑代码范围。

实验在Defects4J等基准数据集上进行，SoapFL在方法级别的故障定位准确率上显著优于现有的LLM-based方法和传统频谱-based方法。

**技术启示**

1. **分解-组合策略是LLM处理大规模代码的关键**：将复杂任务拆分为LLM可处理的子任务，通过结构化的交互流程逐步收敛，是对LLM上下文限制的实用解决方案。
2. **SOP思想的应用**：将人类专家的故障定位流程标准化为可复现的LLM操作步骤，为LLM在软件工程中的应用提供了方法论框架。
3. **多模态信息的融合**：测试结果、代码变更、静态分析警告等多源信息的融合能显著增强LLM的故障定位能力。

**覆盖率**：⭐⭐⭐⭐⭐（LLM故障定位的SOP方法论开创性工作，理论和实践双重贡献）

---

### 2.2 BLAZE: Cross-Language and Cross-Project Bug Localization via Dynamic Chunking and Hard Example Learning

- **作者**: Partha Chakraborty, Mahmoud Alfadel, Meiyappan Nagappan
- **机构**: University of Waterloo
- **发表信息**: IEEE TSE, 2025
- **DOI**: 10.1109/TSE.2025.3579574

**技术概要**

现有的基于深度学习的故障定位工具面临两大挑战：(1) 跨项目适用性差，在一个项目上训练的模型难以泛化到另一个项目；(2) 多语言环境下的有效性不足。虽然大语言模型为故障定位提供了新的可能性，但其有限的上下文窗口和映射精度问题仍然突出。

BLAZE提出了两个核心技术创新：
1. **动态分块（Dynamic Chunking）**：自适应地将源代码分割为语义连贯的块，最小化连续性损失，使得LLM能在有限上下文窗口内捕获完整的语义信息；
2. **困难样本学习（Hard Example Learning）**：利用具有挑战性的故障案例对GPT-based模型进行微调，增强模型对复杂故障模式的识别能力。

为支持BLAZE的能力评估，研究者构建了**BEETLEBOX数据集**，包含来自29个大型活跃开源项目的26,321个故障，覆盖5种编程语言（Java、C++、Python、Go、JavaScript）。在BEETLEBOX、SWE-Bench和Ye et al.三个基准数据集上的评估表明，BLAZE相比6种最先进基线方法实现了大幅提升：Top-1准确率提升120%，平均精度均值（MAP）提升144%，平均倒数排名（MRR）提升100%。

**技术启示**

1. **跨语言故障定位是实际开发中的刚需**：现代软件系统通常是多语言混合的（如Python胶水代码+C++核心+Java服务），跨语言的故障定位能力是实现DevOps全流程自动化的前提。
2. **困难样本挖掘对模型鲁棒性至关重要**：通过刻意选择难以定位的故障案例进行训练，能显著提升模型在真实复杂场景下的表现。
3. **数据集的多样性与规模化是衡量方法实用性的基准**：BEETLEBOX的5语言-29项目-26K故障规模为后续研究提供了高质量的评估基准。

**覆盖率**：⭐⭐⭐⭐⭐（跨语言故障定位的里程碑工作，理论和数据集双重贡献）

---

### 2.3 One Sentence Can Kill the Bug: Auto-Replay Mobile App Crashes From One-Sentence Overviews

- **作者**: Yuchao Huang, Junjie Wang, Zhe Liu, Mingyang Li, Song Wang, Chunyang Chen, Yuanzhe Hu, Qing Wang
- **机构**: 中国科学院软件研究所
- **发表信息**: IEEE TSE, Vol. 51, Issue 4, 2025

**技术概要**

移动应用崩溃报告的复现是开发者面临的最耗时任务之一。现有研究主要依赖逐步操作指令（step-by-step instructions）来实现自动复现，但实际中大量的崩溃报告仅提供一句话概述（one-sentence overview），缺乏详细步骤。

本文提出了一种从**一句话概述自动复现移动应用崩溃**的方法：
1. 利用大语言模型从简短描述中推断可能的操作路径和上下文环境；
2. 构建应用的状态-动作图（State-Action Graph），通过强化学习探索可能的操作序列；
3. 结合GUI分析和日志匹配确认崩溃复现的成功与否。

实验表明，该方法能够从极简的崩溃描述中成功复现大量真实崩溃，显著降低了开发者的手动调试成本。

**技术启示**

1. **自然语言的不精确性与自动化调试的矛盾**：崩溃报告天然具有模糊性和不完整性，LLM的语义理解和推理能力为弥合这一差距提供了可能。
2. **GUI自动化与故障复现的融合**：移动应用的故障复现不仅是代码层面的问题，还涉及GUI状态空间的探索，是两个技术领域的交叉。
3. **用户反馈驱动的质量保障闭环**：从用户反馈到自动化诊断的链路打通，是实现大规模软件质量保障的关键基础设施。

**覆盖率**：⭐⭐⭐☆☆（移动应用调试的细分方向，方法创新性强但系统软件覆盖面有限）

---

## 3. 程序修复与软件安全

自动化程序修复（Automated Program Repair, APR）是软件工程中极具挑战性的方向，其目标是自动生成修复补丁以消除软件缺陷。2025年的TSE论文对APR的有效性和安全性进行了深入的反思与改进。

---

### 3.1 RepairLLaMA: Efficient Representations and Fine-Tuned Adapters for Program Repair

- **作者**: André Silva, Sen Fang, Martin Monperrus
- **机构**: KTH Royal Institute of Technology, Sweden
- **发表信息**: IEEE TSE, 2025
- **DOI**: 10.1109/TSE.2025.3581062

**技术概要**

大语言模型的出现极大地推动了自动化程序修复的发展。然而现有的微调方法大多使用朴素的代码表示，且难以扩展到前沿大模型。RepairLLaMA提出了一套系统性的解决方案：

1. **最优代码表示识别**：系统性地探索了多种代码表示方式（如diff格式、AST序列化、代码上下文拼接等），确定了最适合APR任务的代码表示方案，使模型能够利用有意义的修复信号；
2. **参数高效微调（PEFT）在APR中的首创应用**：将LoRA等参数高效微调技术引入程序修复领域，仅训练轻量级的"程序修复适配器"而非完整模型参数。

实验结果表明，RepairLLaMA正确修复了144个Defects4J v2 bugs、109个HumanEval-Java bugs、20个GitBug-Java bugs，全面超越所有基线方法。参数高效微调不仅降低了计算开销，还帮助提升了模型在微调数据分布之外的修复能力。

**技术启示**

1. **代码表示对修复效果的影响被严重低估**：同样的模型在不同的代码表示下可能产生截然不同的修复结果，表示工程应当成为APR研究的重要组成部分。
2. **参数高效微调作为APR的新范式**：相比全参数微调，PEFT使得在消费级GPU上微调大模型成为可能，极大降低了APR研究的计算门槛。
3. **分布外泛化（OOD Generalization）的意外收益**：PEFT在训练数据之外的bug上也展现了更好的修复能力，这一发现具有重要的实际意义。

**覆盖率**：⭐⭐⭐⭐⭐（LLM程序修复的高影响力工作，技术深度与实用价值兼具）

---

### 3.2 Do Automated Fixes Truly Mitigate Smart Contract Exploits?

- **作者**: Sofia Bobadilla, Monica Jin, Martin Monperrus
- **机构**: KTH Royal Institute of Technology, Sweden
- **发表信息**: IEEE TSE, 2025
- **DOI**: 10.1109/tse.2025.3618123

**技术概要**

智能合约安全已成为区块链生态中数十亿美元级别的重大关切。自动化程序修复被寄予厚望以自动缓解智能合约漏洞，但现有研究从未系统性地评估过这些工具能否真正阻止漏洞利用（exploit）。

本文首次系统性地填补了这一关键空白：
1. 提出了一套**新颖的实验框架**来评估程序修复工具的漏洞利用缓解能力；
2. 对20种最先进的APR工具进行了定性和定量分析；
3. 构建了包含143个有漏洞智能合约的数据集，并**手工构造了91个可执行的漏洞利用**（exploit）；
4. 首次定义并测量了核心指标——**漏洞利用缓解率**（Exploit Mitigation Rate）。

研究揭示了一个严峻的现实：不同工具的漏洞利用缓解率差异巨大，从最低的**29%**到最高的**74%**不等。许多被标记为"已修复"的合约仍然可以被利用。研究还识别了系统性的局限性，如**功能保留不一致**——修复一个漏洞的同时可能引入新的功能性问题。

**技术启示**

1. **"修复≠安全"**：传统的修复评估指标（如测试套件通过率）无法真实反映安全修复的有效性，必须引入漏洞利用缓解率等强安全指标。
2. **对抗性评估的必要性**：安全性工具的评估必须考虑对抗性场景，仅靠功能正确性测试远远不够。
3. **智能合约生态的安全债务**：数十亿美元的资产依赖的智能合约，其自动化修复的可靠性仍然堪忧，该方向亟需更多研究投入。

**覆盖率**：⭐⭐⭐⭐⭐（智能合约安全评估的基础性贡献，方法论可推广至其他安全关键系统）

---

## 4. 代码智能与软件分析

大语言模型正在重塑软件工程的基础设施——从代码搜索到需求追踪，从依赖分析到代码重构。2025-2026年的TSE论文记录了这一技术范式的深度演进。

---

### 4.1 Are Decoder-Only Large Language Models the Silver Bullet for Code Search?

- **作者**: Yuxuan Chen, Mingwei Liu, Guangsheng Ou, Anji Li, Dekun Dai, Yanlin Wang, Zibin Zheng
- **机构**: 中山大学
- **发表信息**: IEEE TSE, 2026
- **DOI**: 10.1109/TSE.2026.3657353

**技术概要**

代码搜索是代码复用的基础能力，允许开发者根据自然语言查询高效定位相关代码片段。Decoder-only大语言模型（如GPT系列、CodeLlama等）的兴起为代码搜索带来了新的范式。然而，这些模型相比传统的encoder-based模型（如UniXcoder）在检索型任务中的有效性一直缺乏系统性评估。

本文对11种decoder-only LLM进行了大规模系统评估：
1. 分析其在**零样本（zero-shot）和微调（fine-tuned）**两种设置下的性能；
2. 在CoSQA⁺（多选择代码搜索基准）等数据集上进行了全面对比。

研究发现：
- 微调后的decoder-only模型（特别是CodeGemma）显著优于encoder-only模型（如UniXcoder），在CoSQA⁺上MAP提升40.4%；
- **模型规模与性能呈非单调关系**：中等规模的模型（而非最大模型）往往表现最优；
- **训练数据组成至关重要**：多语言数据集增强了泛化能力，但少量特定语言的数据可能作为噪声干扰模型效果。

**技术启示**

1. **更大≠更好**：模型规模与代码搜索性能的非单调关系挑战了"scaling law"的普遍假设，中等模型在特定任务上的性价比可能更高。
2. **预训练数据的质量与控制**：微调语料的语言组成对模型行为有决定性影响，噪声数据的混入可能抵消多语言训练带来的泛化收益。
3. **编码器范式并未过时**：在某些场景下，encoder-based模型仍有其竞争力，实际部署时应避免盲目追求decoder-only架构。

**覆盖率**：⭐⭐⭐⭐☆（代码搜索的LLM评估权威工作，对工业实践有直接指导意义）

---

### 4.2 An Automated Approach to Discovering Software Refactorings by Comparing Successive Versions

- **作者**: B. Liu, H. Liu, N. Niu, Y. Zhang, G. Li, H. Jiang, Y. Jiang
- **机构**: 北京大学; 北京理工大学
- **发表信息**: IEEE TSE, Vol. 51, Issue 5, 2025

**技术概要**

重构（Refactoring）是改善软件内部结构而不改变外部行为的关键实践。理解重构操作的历史对于代码审查、技术债务管理和软件演化分析至关重要。然而，从版本历史中自动识别重构操作（区别于一般的代码修改）是一个非平凡的问题。

本文提出了一种自动化方法：
1. 对连续版本间的AST变更进行细粒度解析；
2. 设计匹配算法将代码变更映射到已知的重构类型（如Extract Method、Move Class、Rename Variable等）；
3. 通过启发式规则和机器学习分类器过滤非重构的代码修改。

在多个大型开源项目（如Eclipse JDT、IntelliJ Community Edition）上的实验表明，该方法在识别精度和召回率上均显著优于现有方法。

**技术启示**

1. **重构检测是代码演化分析的基石**：准确的自动重构检测对于代码审查自动化、技术债务量化、代码克隆溯源等下游任务至关重要。
2. **AST级别的diff比文本级diff更有信息量**：文本diff无法捕获语义级别的代码变更意图，AST差异分析是更合理的抽象层级。
3. **重构数据库的构建价值**：大规模、高质量的重构数据库可以成为训练更智能的代码重构推荐系统的关键数据资产。

**覆盖率**：⭐⭐⭐☆☆（代码重构检测的系统性工作，精巧但系统软件覆盖面一般）

---

### 4.3 Cross-Level Requirements Tracing Based on Large Language Models

- **作者**: Chuyan Ge, Tiantian Wang 等
- **机构**: Singapore Management University
- **发表信息**: IEEE TSE, Vol. 51, Issue 7, 2025

**技术概要**

需求追踪（Requirements Tracing）是软件质量保障和安全合规的基础活动，要求在高层需求描述、设计文档、代码实现和测试用例之间建立可追溯的链接关系。传统方法主要依赖信息检索技术（如TF-IDF、LSI）或机器学习模型，在跨层级（cross-level）追踪场景下面临语义鸿沟挑战。

本文探索了大语言模型在跨层级需求追踪中的应用：
1. 利用LLM的语义理解能力弥合高级需求描述与低级代码实现之间的表达差异；
2. 设计多阶段提示策略，引导LLM在两两文档对之间判断是否存在追踪链接；
3. 结合检索增强生成（RAG）在历史追踪数据中查找相似案例，为当前追踪决策提供参考。

实验表明，基于LLM的方法在跨层级需求追踪任务上显著优于传统方法，特别是在处理高抽象层级需求（如法律法规要求）与代码实现的链接识别时表现突出。

**技术启示**

1. **需求追踪的语义鸿沟问题**：LLM强大的跨粒度语义对齐能力使其天然适合处理需求追踪中的"抽象-具体"映射问题。
2. **可追溯性即安全**：在安全关键系统中，需求追踪是合规审计的基础，自动化追踪工具能大幅降低合规成本。
3. **LLM在传统软件工程任务中的"降维打击"**：许多基于传统IR/NLP方法的需求工程任务，正被LLM以更简洁、更有效的方式重新解决。

**覆盖率**：⭐⭐⭐⭐☆（需求追踪的LLM化代表工作，合规审计方向应用前景广阔）

---

### 4.4 Developers' Views on Commercial Involvement in OSS - A Survey from Three Projects

- **作者**: M. Qin, Y. Zhang, M. Zhou, Z. Wang, H. Li, H. Liu
- **机构**: 北京大学
- **发表信息**: IEEE TSE, 2025（录用待刊）

**技术概要**

开源软件（OSS）生态中商业参与日益加深，引发了关于社区治理、贡献动机和项目可持续性的广泛讨论。本文对三个大型开源项目（涵盖基础设施软件和开发者工具）的开发者进行了系统性调查，深入了解开发者对商业参与的态度和关注点。

研究发现揭示了复杂的开发者态度光谱：一方面认可商业支持带来的资源和技术投入，另一方面担忧商业利益可能扭曲项目的技术方向、削弱社区自治性。研究还识别了不同商业参与模式（如雇佣全职维护者、赞助特定功能开发、提供托管服务）对社区健康的差异性影响。

**技术启示**

1. **开源治理的经济维度不可忽视**：软件工程的实证研究需要更多关注开源生态中的经济学和社会学因素。
2. **供应链安全与社区治理的交叉**：商业参与者对开源项目的深度介入可能带来供应链安全风险（如x-utils事件），理解其行为模式是预防机制设计的基础。
3. **方法论启示**：混合方法研究（问卷调查+数据挖掘）在理解复杂社会-技术现象方面具有优势。

**覆盖率**：⭐⭐⭐☆☆（开源治理的社会-技术交叉研究，对理解系统软件生态有价值但偏离核心技术主题）

---

## 5. 结语与未来方向

### 5.1 2025-2026年度TSE系统软件方向关键趋势

通过对上述15篇论文的系统性分析，可归纳出以下五大关键趋势：

| 趋势 | 描述 | 代表论文 |
|------|------|----------|
| **LLM驱动的调试范式变革** | 从频谱到LLM，从被动检测到主动推理 | SoapFL, BLAZE, RepairLLaMA |
| **有状态系统测试的突破** | 协议、数据库等有状态系统的模糊测试方法论日趋成熟 | AFLNet 5-Year, DBMS Bug Study |
| **从"修复率"到"安全性"的评估升级** | 程序修复的评估从功能正确性向安全有效性转变 | Smart Contract Exploit Mitigation |
| **多语言/跨项目泛化** | 工具和方法的泛化性从"nice-to-have"变为核心评估指标 | BLAZE, Code Search |
| **产业-学术协同加速** | 学术成果向工业工具的转化周期显著缩短 | AG-RAG, ATTuzz, DBMS Study |

### 5.2 值得关注的未来方向

1. **LLM+符号执行的混合测试**：LLM的代码生成能力与符号执行的完备性分析相结合，有望突破现有测试技术的覆盖率平台期。参考Marcel Böhme团队在ICSE 2026提出的Cottontail（LLM-Driven Concolic Execution）。

2. **AI编译器测试成为新热点**：随着TVM、ONNXRuntime、XLA等DL编译器越来越复杂，对编译器优化正确性的系统性测试成为关键需求。相关工作中OATest（ICSE 2026）和OPERA初步探索了这一方向。

3. **数据库系统的智能化质量保障**：面向DBMS的专门化测试工具（如SQLT、PUPPY/ICSE 2025的DBMS性能回归测试）正在形成一个独立的研究子领域。

4. **软件供应链安全的端到端保障**：从上游依赖的安全补丁识别（SPATCH）到下游项目的漏洞传播防护（PLUMBER/TSE 2023），供应链安全的自动化保障需要全链路覆盖。

5. **基于AI的静默缺陷检测**：超过40%的DBMS缺陷不触发崩溃，传统以崩溃为信号的fuzzing方法存在系统性盲区，差分测试和蜕变测试在静默缺陷检测中的价值有待更深入挖掘。

---

## 论文索引表

| 序号 | 论文标题 | 第一作者 | 机构 | 发表时间 | 方向 |
|------|----------|----------|------|----------|------|
| 1 | AFLNet Five Years Later: On Coverage-Guided Protocol Fuzzing | Ruijie Meng | Univ. of Melbourne | TSE 2025, Vol.51(4) | 协议模糊测试 |
| 2 | ATTuzz: Better Pay Attention Whilst Fuzzing | Shunkai Zhu | Singapore Management Univ. | TSE 2024, Vol.50(2) | 智能模糊测试 |
| 3 | Low-Cost Testing for Path Coverage of MPI Programs | Baicai Sun | 青岛科技大学 | TSE 2025 | MPI程序测试 |
| 4 | Improving Retrieval-Augmented Deep Assertion Generation via Joint Training | 张犬俊 | 南京大学 | TSE 2025 | 测试断言生成 |
| 5 | A Comprehensive Study of Bugs in Relational DBMS | 刘爽 | 中国人民大学 & OceanBase | TSE 2025 | DBMS缺陷实证 |
| 6 | SoapFL: A Standard Operating Procedure for LLM-Based Method-Level Fault Localization | Yihao Qin | 国防科技大学 | TSE 2025, Vol.51(4) | LLM故障定位 |
| 7 | BLAZE: Cross-Language and Cross-Project Bug Localization | Partha Chakraborty | Univ. of Waterloo | TSE 2025 | 跨语言故障定位 |
| 8 | One Sentence Can Kill the Bug: Auto-Replay Mobile App Crashes | Yuchao Huang | 中科院软件所 | TSE 2025, Vol.51(4) | 移动应用调试 |
| 9 | RepairLLaMA: Efficient Representations and Fine-Tuned Adapters for Program Repair | André Silva | KTH | TSE 2025 | LLM程序修复 |
| 10 | Do Automated Fixes Truly Mitigate Smart Contract Exploits? | Sofia Bobadilla | KTH | TSE 2025 | 智能合约安全 |
| 11 | Are Decoder-Only LLMs the Silver Bullet for Code Search? | Yuxuan Chen | 中山大学 | TSE 2026 | 代码搜索 |
| 12 | An Automated Approach to Discovering Software Refactorings | B. Liu | 北京大学 | TSE 2025, Vol.51(5) | 重构检测 |
| 13 | Cross-Level Requirements Tracing Based on LLMs | Chuyan Ge | Singapore Management Univ. | TSE 2025, Vol.51(7) | 需求追踪 |
| 14 | Developers' Views on Commercial Involvement in OSS | M. Qin | 北京大学 | TSE 2025 | 开源治理 |
| 15 | Adapting Installation Instructions in Rapidly Evolving Software Ecosystems | Haoyu Gao | Singapore Management Univ. | TSE 2025, Vol.51(4) | 软件安装自动化 |

---

> **免责声明**：本报告基于2025年6月至2026年6月期间公开发表的IEEE TSE论文信息编写。部分论文因访问限制无法获取全文，技术概要基于公开摘要、arXiv预印本和新闻报道综合而成。论文选取以系统软件工程（测试工具、验证、调试、性能分析）为主要导向，不一定覆盖TSE该时段全部发表论文。所有论文信息以IEEE Xplore正式发布为准。

---

*报告生成日期：2026年6月10日*  
*数据来源：IEEE Xplore, arXiv, DBLP, Google Scholar, 各研究机构官方网站*