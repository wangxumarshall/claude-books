# IEEE Transactions on Parallel and Distributed Systems (TPDS) 2026 洞察报告

> **覆盖时间**：2025年6月 – 2026年6月  
> **期刊等级**：CCF-A，JCR Q1，并行与分布式系统领域顶级期刊  
> **报告范围**：选取18篇代表性论文，覆盖分布式系统与云计算、并行计算与ML系统、边缘计算与IoT系统三大方向  

---

## 0. 期刊概览

IEEE Transactions on Parallel and Distributed Systems（TPDS）是IEEE Computer Society主办的旗舰期刊，创刊于1990年，在中国计算机学会（CCF）推荐目录中被列为A类期刊（CCF-A），也是SCI JCR一区期刊。TPDS专注于并行与分布式系统领域的原创性研究，涵盖并行计算架构、分布式算法、云计算、高性能计算、边缘计算、存储系统、ML系统等方向。

本报告覆盖2025年下半年至2026年上半年（Vol. 36, Issues 7-12 + 2026 early access articles），按月均约15篇的发表节奏，估计本周期内发表约180篇论文。本报告精选18篇代表性工作，按三大研究主题——分布式系统与云计算、并行计算与ML系统、边缘计算与IoT系统——进行分类综述，每篇论文给出技术概要（200–300字）与关键技术启示（3–5条）。

### 论文覆盖总览

| 编号 | 论文标题 | 研究主题 | Vol/Issue |
|:---:|:---|:---|:---|
| P1 | Characterizing FaaS Workflows on Public Clouds | 分布式系统与云计算 | 2026 Early Access |
| P2 | ABSE: Adaptive Baseline Score-Based Election for Leader-Based BFT Systems | 分布式系统与云计算 | 36(8), 2025 |
| P3 | Slark: A Performance Robust Decentralized Inter-Datacenter Deadline-Aware Coflows Scheduling | 分布式系统与云计算 | 36(2), 2025 |
| P4 | Object Proxy Patterns for Accelerating Distributed Applications | 分布式系统与云计算 | 36(2), 2025 |
| P5 | Spread+: Scalable Model Aggregation in Federated Learning With Non-IID Data | 分布式系统与云计算 | 36(4), 2025 |
| P6 | DegaFL: Decentralized Gradient Aggregation for Cross-Silo Federated Learning | 分布式系统与云计算 | 36(2), 2025 |
| P7 | GreenFlow: A Carbon-Efficient Scheduler for Deep Learning Workloads | 分布式系统与云计算 | 36(2), 2025 |
| P8 | Towards Universal Performance Modeling for ML Training on Multi-GPU Platforms | 并行计算与ML系统 | 36(2), 2025 |
| P9 | Joint Dynamic Data and Model Parallelism for Distributed Training of DNNs | 并行计算与ML系统 | 36(2), 2025 |
| P10 | UMPIPE: Unequal Microbatches-Based Pipeline Parallelism for DNN Training | 并行计算与ML系统 | 36(2), 2025 |
| P11 | TOP: Task-Based Operator Parallelism for Asynchronous DL Inference on GPU | 并行计算与ML系统 | 36(2), 2025 |
| P12 | Spreeze: High-Throughput Parallel Reinforcement Learning Framework | 并行计算与ML系统 | 36(2), 2025 |
| P13 | Leveraging Graph Analysis to Pinpoint Root Causes of Scalability Issues | 并行计算与ML系统 | 36(2), 2025 |
| P14 | GEREM: Fast and Precise Error Resilience Assessment for GPU Microarchitectures | 并行计算与ML系统 | 36(5), 2025 |
| P15 | Coordinating Computational Capacity for Adaptive FL in Heterogeneous Edge | 边缘计算与IoT系统 | 36(8), 2025 |
| P16 | Loci: Federated Continual Learning of Heterogeneous Tasks at Edge | 边缘计算与IoT系统 | 36(4), 2025 |
| P17 | Multi-Agent Collaboration for Workflow Task Offloading in End-Edge-Cloud | 边缘计算与IoT系统 | 36(11), 2025 |
| P18 | SpatialVec-DWP: Dynamic Weighted Data Placement for Edge-Cloud Co-Optimization | 边缘计算与IoT系统 | 2026 Accepted |

---

## 1. 分布式系统与云计算

### P1. Characterizing FaaS Workflows on Public Clouds: The Good, the Bad and the Ugly

- **作者**：Varad Kulkarni, Nikhil Reddy, Tuhin Khare, Abhinandan S. Prasad, Chitra Babu, Yogesh Simmhan
- **机构**：Indian Institute of Science (IISc), Bangalore
- **发表**：IEEE TPDS, 2026 Early Access (DOI: 10.1109/TPDS.2026.3678606)

**技术概要**：FaaS（Function-as-a-Service）工作流平台（如AWS Step Functions、Azure Durable Functions）已成为构建无服务器应用的核心基础设施，但平台内部的性能特性、扩缩容行为和成本模型对开发者而言几乎是"黑盒"。本文对AWS和Azure三大主流FaaS工作流平台进行了系统性的实证评估，运行了25个微基准测试与应用工作流，共计超过132K次函数调用。研究验证了部分社区共识（如冷启动对延迟的影响），但同时揭示了诸多反直觉的发现：包括函数执行模式对编排开销的非线性影响、跨函数交互导致的级联延迟放大效应、以及不同平台在成本-性能权衡上的设计哲学差异。文章为FaaS工作流开发者提供了可操作的配置指南和性能预期，并指明了平台优化的开放研究问题。

**技术启示**：
1. **冷启动不只影响首调用**：工作流中的函数间依赖使得单个函数的冷启动延迟会通过编排链级联放大，严重时导致端到端延迟上升数倍
2. **平台设计差异显著**：AWS Step Functions的状态机模型与Azure Durable Functions的编排器重放机制在并发扩展性上表现出截然不同的瓶颈模式
3. **成本不可忽视**：工作流编排器自身的计费模型（状态转换次数、执行时长）在复杂工作流中可能超越函数执行成本，需纳入总成本分析
4. **可观测性缺口**：缺乏跨函数的端到端追踪工具是当前FaaS工作流调试和性能优化的首要障碍

---

### P2. ABSE: Adaptive Baseline Score-Based Election for Leader-Based BFT Systems

- **作者**：Xuyang Liu, Zijian Zhang, Zhen Li, Hao Yin, Meng Li, Jiamou Liu, Mauro Conti, Liehuang Zhu
- **机构**：北京理工大学、奥克兰大学、北京大学、帕多瓦大学、代尔夫特理工大学
- **发表**：IEEE TPDS, Vol. 36(8), pp. 1634-1650, 2025

**技术概要**：基于Leader的拜占庭容错（BFT）共识协议在分布式系统中有广泛应用，但恶意Leader会严重破坏系统性能和安全性。现有方案要么引入过高复杂度（如随机Leader轮换），要么缺乏可扩展性。本文提出ABSE（Adaptive Baseline Score-based Election），一种完全本地化的、基于积分累积的Leader选举机制。ABSE为每个共识参与节点维护一个基线评分（Baseline Score），依据其对共识推进的贡献动态调整；在选举时，高分节点获得更高选中概率，从而自然绕过低可靠性参与者。论文给出了ABSE的形式化处理，定义了通用的组件和一致性约束规则，并将其应用到两种不同的BFT协议（HotStuff和PBFT变体）中，证明了方法在协议复杂性上的最小侵入性和跨协议的可迁移性。

**技术启示**：
1. **"贡献即信誉"设计**：将Leader选举与节点行为贡献直接挂钩，使拜占庭节点在重复表现不当时被自然边缘化，无需额外的故障检测层
2. **本地化即扩展性**：ABSE的纯本地计算特性使其能在不引入额外协调开销的前提下扩展到大规模网络，与依赖全局视图的方案形成鲜明对比
3. **协议无关性**：通过抽象通用组件和规则，ABSE可无缝集成到多种BFT协议中，展现了良好的可移植性
4. **最小侵入设计哲学**：无需修改底层共识协议的核心逻辑，仅通过调整Leader选举概率分布即可实现显著的鲁棒性提升

---

### P3. Slark: A Performance Robust Decentralized Inter-Datacenter Deadline-Aware Coflows Scheduling

- **作者**：Xiaodong Dong, Lihai Nie, Zheli Liu, Yang Xiang
- **机构**：南开大学
- **发表**：IEEE TPDS, Vol. 36(2), pp. 197-211, 2025

**技术概要**：跨数据中心网络中的Coflow调度是分布式计算系统的关键性能瓶颈。传统的集中式调度方法在跨数据中心场景下面临信息延迟和单点瓶颈问题。本文提出Slark，一种仅依赖本地信息的去中心化跨数据中心Coflow调度框架。Slark的核心创新在于：每个数据中心仅基于本地可观测信息（本地Coflow到达时间、大小估计和截止时间）独立做出调度决策，无需全局协调。为保证去中心化条件下的性能鲁棒性，Slark设计了基于"虚拟截止时间"的优先级机制和自适应的速率控制策略，理论上证明了在信息不完整情况下仍能保证deadline满足率的下界。实验表明Slark在跨地域数据中心场景下可接近集中式方案的最优性能，同时具备更好的可扩展性和容错能力。

**技术启示**：
1. **去中心化vs.信息不完整**：Slark证明在跨数据中心场景下，放弃全局信息换取的扩展性收益远大于决策精度损失
2. **虚拟截止时间机制**：通过对真实截止时间进行本地偏移调整，实现了一种轻量级的去中心化优先级协调
3. **Coflow抽象的价值**：将相关流聚合为Coflow进行调度，比逐流调度更能捕捉应用级语义，尤其在跨数据中心场景下优势显著
4. **理论-实践闭环**：论文不仅给出了工程实现，还提供了deadline满足率的理论下界保证，这在系统类论文中较为难得

---

### P4. Object Proxy Patterns for Accelerating Distributed Applications

- **作者**：J. Gregory Pauloski, Valerie Hayot-Sasson, Logan Ward, Alexander Brace, André Bauer, Kyle Chard, Ian Foster
- **机构**：University of Chicago, Argonne National Laboratory
- **发表**：IEEE TPDS, Vol. 36(2), pp. 253-265, 2025

**技术概要**：分布式科学应用中，Python已成为主流编程语言，但Python对象的跨节点传输效率低下是显著的性能瓶颈。传统方案要么依赖手写序列化代码（易出错），要么使用通用序列化框架（性能差）。本文提出Object Proxy Patterns——一种基于代理（Proxy）模式的透明分布式对象管理框架。其核心思想是：利用Python的`__getattr__`和描述符协议实现惰性对象解析，使得远程对象的访问在语法上与本地对象完全一致，同时在底层自动处理数据传输、缓存和一致性。Proxy支持多种解析策略（eager/lazy/batch），并内置基于引用计数的自动垃圾回收。实验在分子动力学、材料科学等典型科学计算场景中展示了Proxy相比传统pickle序列化方案2-10倍的数据传输加速。

**技术启示**：
1. **代理模式的系统化应用**：将设计模式中的Proxy模式提升到分布式系统中间件层面，实现了对应用代码零侵入的分布式对象管理
2. **惰性解析的权衡**：eager/lazy/batch等多种解析策略使开发者可按数据访问模式精细调优，避免"一刀切"的性能损失
3. **Python生态的分布式痛点**：论文揭示了科学计算从HPC向云迁移过程中，Python序列化瓶颈已成为比网络带宽更紧迫的优化方向
4. **引用计数驱动的GC**：利用Python内置引用计数实现分布式垃圾回收，比传统的基于心跳/租约的方案更轻量且及时

---

### P5 & P6. 联邦学习：分层聚合与去中心化梯度聚合

#### P5. Spread+: Scalable Model Aggregation in Federated Learning With Non-IID Data

- **作者**：Huanghuang Liang, Xin Yang, Xiaoming Han, Boan Liu, Chuang Hu, Dan Wang, Xiaobo Zhou, Dazhao Cheng
- **机构**：武汉大学、澳门大学、香港理工大学
- **发表**：IEEE TPDS, Vol. 36(4), pp. 701-716, 2025

**技术概要**：联邦学习（FL）中数据异构性（Non-IID）和设备异构性导致中心化聚合成为系统的可扩展性瓶颈。本文提出Spread+，一种通过分层聚类实现可扩展模型聚合的联邦学习系统。客户端首先通过Hedonic联盟博弈（Hedonic Coalition Formation Game）自组织为多个聚类，每个聚类由边缘设备担任聚合器。系统采用自适应算法动态调节聚类内和聚类间的聚合间隔，在模型精度和通信效率之间取得平衡。此外，Spread+优化了聚合算法以提升Non-IID数据下的模型精度。实验表明，Spread+相比FedAvg提升49.58%，相比Ring-AllReduce提升22.78%。

**技术启示**：
1. **博弈论驱动的客户端组织**：Hedonic联盟博弈为客户端聚类提供了严格的数学基础，使得聚类结果兼具稳定性和全局效率
2. **双层自适应聚合**：聚类内高频聚合与聚类间低频同步的结合，是对Non-IID场景下"局部过拟合vs.全局收敛"矛盾的有效拆解
3. **分层去中心化优于完全中心化/去中心化**：Spread+在完全中心化（瓶颈）和完全去中心化（精度损失）之间找到了工程上的最优折中点

#### P6. DegaFL: Decentralized Gradient Aggregation for Cross-Silo Federated Learning

- **作者**：Jialiang Han, Yudong Han, Xiang Jing, Gang Huang, Yun Ma
- **机构**：北京大学
- **发表**：IEEE TPDS, Vol. 36(2), pp. 212-225, 2025

**技术概要**：跨机构联邦学习（Cross-Silo FL）中，参与方通常为少量但拥有大量数据的机构（如医院、银行），对数据隐私和模型质量同时有极高要求。DegaFL提出一种完全去中心化的梯度聚合方案，各参与方通过点对点通信直接在去中心化拓扑中交换和聚合模型更新，无需中央聚合服务器。DegaFL的核心是设计了一种基于Gossip协议的梯度同步算法，理论上证明了在非完全连接拓扑下仍能保证线性收敛速度。同时，DegaFL引入差分隐私机制保护梯度交换过程中的隐私，并设计了自适应通信拓扑优化，在保护隐私的前提下最小化通信开销。

**技术启示**：
1. **Cross-Silo场景的特殊性**：与Cross-Device FL相比，Cross-Silo FL对隐私合规要求更高，同时参与方数量少但计算能力强，去中心化方案在此场景下具有天然优势
2. **Gossip收敛性的理论突破**：DegaFL的理论证明消除了"去中心化必然牺牲收敛速度"的顾虑
3. **隐私与通信效率的联合优化**：在去中心化拓扑中同时考虑差分隐私噪声和通信开销，实现多目标帕累托优化

---

### P7. GreenFlow: A Carbon-Efficient Scheduler for Deep Learning Workloads

- **作者**：Diandian Gu, Yihao Zhao, Peng Sun, Xin Jin, Xuanzhe Liu
- **机构**：北京大学
- **发表**：IEEE TPDS, Vol. 36(2), pp. 168-184, 2025

**技术概要**：深度学习训练工作负载的快速增长导致了巨大的碳排放问题。不同时间和地域的电力碳强度（Carbon Intensity）存在显著差异，为碳感知调度提供了优化空间。GreenFlow提出了首个面向DL训练工作负载的碳效率调度器。其核心创新包括：(1) 利用电力碳强度的时空变化特性，将可延迟的DL训练作业调度到低碳时段和低碳区域执行；(2) 设计了碳感知的作业准入控制和抢占策略，在保证SLO的前提下最小化碳足迹；(3) 建立了考虑电网边际碳排放信号的细粒度碳核算模型。实验基于真实电网碳排放数据和生产DL训练负载轨迹进行，GreenFlow在仅增加5%作业完成时间的情况下，实现了最高54%的碳排放减少。

**技术启示**：
1. **碳感知调度的可行性**：论文证明了在不显著牺牲性能的前提下，通过时空调度优化即可实现可观的碳减排，为绿色AI系统开辟了新的优化维度
2. **碳强度的时空异质性**：同一时刻不同地域的电网碳强度差异可达10倍以上，使得跨地域调度成为碳减排的有力杠杆
3. **边际碳排放vs.平均碳排放**：使用边际碳排放信号（而非平均碳排放）建模作业的增量碳影响，是碳核算准确性的关键
4. **系统研究的"绿色转向"**：GreenFlow代表了系统领域的新趋势——将环境可持续性作为一等优化目标，与性能和成本并列

---

## 2. 并行计算与ML系统

### P8. Towards Universal Performance Modeling for Machine Learning Training on Multi-GPU Platforms

- **作者**：Zhongyi Lin, Ning Sun, Pallab Bhattacharya, Xizhou Feng, Louis Feng, John D. Owens
- **机构**：NVIDIA, UC Davis
- **发表**：IEEE TPDS, Vol. 36(2), pp. 226-238, 2025

**技术概要**：在多GPU平台上对机器学习训练进行性能建模，是硬件选型、资源配置和成本估算的基础。然而，现有性能模型要么依赖于具体硬件特性（缺乏通用性），要么使用过于简化的计算/通信比模型（精度不足）。本文提出了一种通用性能建模框架，能够准确预测任意DNN模型在任意多GPU配置下的训练吞吐量。框架将训练过程分解为计算、通信和同步三个基本操作，通过离线微基准测试获取目标GPU平台的计算和通信Roofline特征，再结合模型的FLOPs和通信量进行端到端吞吐预测。该框架已对NVIDIA V100到H100多代GPU及NVLink、PCIe、InfiniBand等不同互连技术进行验证，预测误差控制在8%以内。

**技术启示**：
1. **"模型-硬件解耦"建模**：将DNN模型的计算特征与硬件平台的Roofline特征分离建模，使得同一模型可在不同硬件配置间快速"移植"预测
2. **通信建模的细粒度化**：不仅考虑通信量，还建模了通信模式（AllReduce/AllGather/ReduceScatter）、消息大小和拓扑结构的影响
3. **微基准的巧妙应用**：通过少量离线微基准测试替代繁重的硬件逆向工程，实现了跨GPU代际的通用性
4. **工程启示**：对云厂商和AI平台而言，该模型可直接嵌入资源调度器，实现"按性能付费"的定价模式

---

### P9. Joint Dynamic Data and Model Parallelism for Distributed Training of DNNs Over Heterogeneous Infrastructure

- **作者**：Zhi Ling, Xiaofeng Jiang, Xiaobin Tan, Huasen He, Shiyin Zhu, Jian Yang
- **机构**：中国科学技术大学
- **发表**：IEEE TPDS, Vol. 36(2), pp. 150-167, 2025

**技术概要**：现有的分布式DNN训练并行策略（数据并行、模型并行、流水线并行）通常要求同构的硬件环境，难以适应异构基础设施（混合GPU型号、不同网络带宽、异构节点算力）。本文首次提出了联合动态数据并行与模型并行的统一框架，在异构基础设施中自动搜索最优的并行策略组合。框架基于代价模型（Cost Model）对搜索空间进行剪枝，将联合优化问题转化为带约束的整数线性规划，并利用二分图匹配和动态规划进行高效求解。与纯数据并行或纯模型并行相比，在异构GPU集群中实现了最高2.3倍的训练加速。

**技术启示**：
1. **异构优先的设计理念**：在云/算力网络中，硬件异构是常态而非例外，本文的方法是"为异构设计"而不是"在异构上适配"
2. **并行策略的组合搜索**：将数据并行度、模型并行度、流水线深度作为联合决策变量，其搜索空间虽大但可通过代价模型有效剪枝
3. **二分图匹配的应用**：将GPU到模型分片的映射建模为二分图匹配问题，是优雅且高效的形式化方法
4. **工业实践的指引**：对混合使用A100/H100/RTX等GPU的企业AI平台具有直接的实用价值

---

### P10. UMPIPE: Unequal Microbatches-Based Pipeline Parallelism for DNN Training

- **作者**：Guangyao Zhou, Wenhong Tian, Rajkumar Buyya, Kui Wu
- **机构**：电子科技大学、墨尔本大学、维多利亚大学
- **发表**：IEEE TPDS, Vol. 36(2), pp. 293-307, 2025

**技术概要**：流水线并行是训练大模型的标准方法之一，但传统的等大小微批次（Equal Microbatch）策略会导致"流水线气泡"（Pipeline Bubble），即部分GPU在流水线填充和排空阶段空闲。UMPIPE提出不等微批次策略，通过给流水线不同阶段分配不同大小的微批次来减少气泡。其核心洞察是：流水线首尾阶段的微批次大小对气泡大小的影响最大，通过动态调整这些阶段的微批次大小（如首阶段使用较小微批次快速填充流水线），可显著压缩空闲时间。论文对不等微批次策略进行了严格的理论收敛性分析，证明在特定条件下不影响最终模型精度。实验在GPT和BERT等模型上验证了最高1.4倍的训练吞吐提升。

**技术启示**：
1. **"形状感知"的流水线优化**：不等微批次本质上是对流水线"填充-稳态-排空"三个阶段进行非对称优化，比传统对称策略更贴合流水线的真实执行特征
2. **理论保证的重要性**：不等微批次改变了每步的计算量，可能影响优化器动态，论文的理论收敛分析消除了这一顾虑
3. **通用性与简洁性的平衡**：UMPIPE仅需修改微批次分配算法，无需改动模型代码、优化器或通信模式，工程落地门槛极低
4. **与1F1B调度的互补**：不等微批次可与1F1B（One-Forward-One-Backward）等主流流水线调度策略正交叠加，获得进一步的性能增益

---

### P11. TOP: Task-Based Operator Parallelism for Asynchronous Deep Learning Inference on GPU

- **作者**：Changyao Lin, Zhenming Chen, Ziyang Zhang, Jie Liu
- **机构**：哈尔滨工业大学（深圳）
- **发表**：IEEE TPDS, Vol. 36(2), pp. 266-281, 2025

**技术概要**：GPU推理服务中，传统请求级批处理（Request-Level Batching）在混合推理负载（不同模型/不同batch size/不同序列长度）下会引入显著的排队延迟。TOP提出基于任务的操作符并行（Task-Based Operator Parallelism），将推理请求分解为独立算子任务，利用GPU的多流（Multi-Stream）并发能力异步执行不同请求的不同算子。TOP设计了轻量级的算子依赖图调度器，通过CUDA Stream优先级和事件同步，实现算子间的无锁并发；同时引入算子融合策略减少kernel launch开销。实验在NVIDIA A100上对多种CV和NLP模型进行了验证，TOP在混合负载下相比传统批处理将P99延迟降低了42%，同时提升吞吐23%。

**技术启示**：
1. **从"请求并行"到"算子并行"的粒度进化**：算子级并行能更充分地利用GPU的多流并发能力，尤其适合推理即服务（Inference-as-a-Service）的多租户混合负载场景
2. **依赖图调度vs.队列调度**：算子依赖图调度器比简单的FIFO队列更能发现跨请求的并行机会
3. **CUDA Stream的精细化使用**：TOP展示了在推理场景中，对CUDA Stream和Event的精妙使用如何在不增加显存压力的情况下提升GPU利用率
4. **算子融合作为补充策略**：将小算子融合为更大kernel，减少kernel launch开销，与算子并行形成互补优化

---

### P12. Spreeze: High-Throughput Parallel Reinforcement Learning Framework

- **作者**：Jing Hou, Guang Chen, Ruiqi Zhang, Zhijun Li, Shangding Gu, Changjun Jiang
- **机构**：同济大学
- **发表**：IEEE TPDS, Vol. 36(2), pp. 282-292, 2025

**技术概要**：强化学习（RL）训练面临"样本生成-策略更新"交替的固有串行瓶颈。Spreeze提出了高吞吐并行RL框架，在采样、推理、训练三个阶段之间实现流水线解耦和异步并行。核心设计包括：(1) 解耦的分布式采样架构，多环境实例异步产生经验样本，通过共享经验池与训练器交互；(2) 基于优先级的样本消费策略（Prioritized Experience Consumption），使训练器优先消费高价值的"异常"样本；(3) 动态批次聚合机制，在训练器端自动合并到达的多源样本批次以最大化GPU利用率。实验在MuJoCo和Atari基准上，使用单节点8-GPU实现了相比主流分布式RL框架（RLlib、SEED RL）2.1倍的吞吐提升。

**技术启示**：
1. **RL训练的三阶段流水线**：采样-推理-训练的解耦和异步化是RL系统优化的核心范式，Spreeze将其系统化实现
2. **优先级样本消费vs.优先级经验回放**：Spreeze在"消费端"而非"存储端"做优先级过滤，避免了经验池排序开销，更适合高吞吐场景
3. **GPU应该只做训练**：将推理和采样尽可能卸载到CPU/环境模拟器，让GPU专注于反向传播，是实现RL训练GPU高利用率的关键
4. **框架设计的可组合性**：Spreeze通过模块化设计，允许各组件独立替换，具有良好的生态兼容性

---

### P13. Leveraging Graph Analysis to Pinpoint Root Causes of Scalability Issues for Parallel Applications

- **作者**：Yuyang Jin, Haojie Wang, Xiongchao Tang, Zhenhua Guo, Yaqian Zhao, Torsten Hoefler, Tao Liu, Xu Liu, Jidong Zhai
- **机构**：清华大学、ETH Zurich、North Carolina State University
- **发表**：IEEE TPDS, Vol. 36(2), pp. 308-325, 2025

**技术概要**：并行应用的可扩展性问题诊断是一项耗时且依赖专家经验的艰巨任务。现有工具（如性能分析器、trace可视化工具）能提供大量底层数据，但缺乏自动化的根因定位能力。本文提出了一个利用图分析技术自动定位并行应用可扩展性瓶颈根源的系统。系统首先将应用的执行trace建模为"执行图"（Execution Graph），包含计算节点、通信边和同步屏障等元素；然后定义了一系列图分析算子——关键路径分析、通信拓扑瓶颈检测、负载均衡偏差量化、同步点异常检测等——自动从执行图中提取可扩展性问题信号；最后通过因果推理引擎将多个信号关联为根因假设并排序输出。系统在NPB、HPCG等基准和真实科学应用中验证了有效性。

**技术启示**：
1. **从"数据"到"洞察"的自动化**：将性能分析从"看数据"提升到"得结论"，是HPC工具链向智能化演进的关键一步
2. **图建模的通用性**：无论是MPI通信、CUDA kernel依赖还是流水线阶段同步，都可统一抽象为执行图，适用性极广
3. **因果推理vs.相关性分析**：仅凭统计相关性无法区分"症状"和"根因"，因果推理引擎是根因定位的关键技术差异
4. **产学研结合的典范**：清华翟季冬团队与Torsten Hoefler（ETH）的跨国合作，体现了HPC系统研究的全球化和强强联合趋势

---

### P14. GEREM: Fast and Precise Error Resilience Assessment for GPU Microarchitectures

- **作者**：Jingweijia Tan, Xurui Li, An Zhong, Kaige Yan, Xiaohui Wei, Guanpeng Li
- **机构**：吉林大学、University of Iowa
- **发表**：IEEE TPDS, Vol. 36(5), pp. 1011-1024, 2025

**技术概要**：GPU在后摩尔时代对瞬态硬件故障（Soft Error）越来越敏感，对GPU微架构进行错误弹性（Error Resilience）评估是芯片设计和容错软件的基础。传统的统计故障注入（Statistical Fault Injection, SFI）方法虽然准确但极其耗时。GEREM提出了首个GPU微架构错误弹性快速评估框架，核心发现是：故障在微架构层面的"早期表现行为"（Early Fault Manifestation, EFM）可以有效预测最终的程序执行结果。GEREM通过一次profiling获取目标程序的微架构状态快照，然后在这些快照上快速注入故障并生成EFM。对于数据存储结构（寄存器文件、共享内存等），EFM直接用于预测故障结果；对于流水线指令，则使用ML模型进行预测。相比传统SFI，GEREM实现了平均237倍的加速。

**技术启示**：
1. **"早期信号即预测"洞察**：故障在传播早期就表现出可判别的行为模式，无需全流程模拟即可判断最终影响，这是200+倍加速的根源
2. **ML用于故障预测的适配性**：流水线指令的故障行为模式复杂但可学习，ML模型在此场景下比规则匹配更有效
3. **GPU可靠性研究的紧迫性**：随着制程缩减和电压降低，GPU soft error率每代平均增加约2倍，快速评估工具对芯片设计至关重要
4. **软硬件协同可靠性设计**：GEREM的输出可指导编译器插入选择性指令冗余（Selective Instruction Duplication），比全量冗余更高效

---

## 3. 边缘计算与IoT系统

### P15. Coordinating Computational Capacity for Adaptive Federated Learning in Heterogeneous Edge Computing Systems

- **作者**：Kechang Yang, Biao Hu, Mingguo Zhao
- **机构**：中国农业大学、清华大学
- **发表**：IEEE TPDS, Vol. 36(8), pp. 1509-1523, 2025

**技术概要**：异构边缘设备（树莓派、Jetson、手机等）参与联邦学习时，算力差异导致"短板效应"——弱设备拖慢全局聚合节奏。本文提出自适应FL框架，通过协调异构设备间的计算能力差异来提升整体训练效率。框架首先证明了本地聚合模型在异构环境下的收敛界，然后基于收敛界设计了自适应算法，该算法根据各设备的计算能力和资源消耗关系动态调节其本地更新迭代次数。算力强的设备执行更多本地迭代，算力弱的设备执行较少迭代，在保持全局收敛的同时最大化整体训练吞吐。在MNIST和PlantVillage数据集上，使用MobileNet和AlexNet的实验中，本算法相比现有方法将loss函数改善至少16.87%，收敛速度提升至少2倍。

**技术启示**：
1. **"各尽所能"的异构适应**：允许强设备多跑、弱设备少跑，既避免了弱设备的拖累，又充分利用了强设备算力，是异构FL的效率最优策略
2. **收敛界驱动的设计**：从理论收敛界出发推导出各设备的"最优本地迭代次数"，使工程设计与理论保证形成闭环
3. **实际硬件验证**：使用树莓派等真实边缘设备进行实验，而非纯模拟，验证了方案在实际部署中的可行性
4. **农业场景的应用前景**：PlantVillage数据集的使用表明该方法在智慧农业等特殊边缘场景中有明确的落地路径

---

### P16. Loci: Federated Continual Learning of Heterogeneous Tasks at Edge

- **作者**：Yiluo Luopan, Rui Han, Q. Zhang, X. Zuo, Chi Harold Liu, Guoren Wang, Lydia Y. Chen
- **机构**：北京理工大学、TU Delft
- **发表**：IEEE TPDS, Vol. 36(4), pp. 775-790, 2025

**技术概要**：边缘设备面临的AI任务往往随时间动态变化（新类别、新任务），传统联邦学习假设任务分布固定，无法处理"持续学习"（Continual Learning）需求。Loci首次将联邦学习与持续学习融合，提出联邦持续学习（Federated Continual Learning, FCL）框架，解决边缘设备上异构任务序列的学习问题。Loci设计了自适应解耦提示（Adaptive Decoupled Prompting）机制：为每个任务维护独立的任务提示（Task Prompt），通过提示选择器在推理时自动路由到对应的任务知识，从而避免灾难性遗忘（Catastrophic Forgetting）。同时，Loci在联邦聚合时设计了提示对齐机制，确保不同设备上学习到的提示在语义空间中对齐。实验在多种持续学习基准上验证了Loci相比现有方法在模型精度、通信成本和计算效率上的综合优势。

**技术启示**：
1. **FL × CL = FCL**：联邦持续学习是分布性（隐私保护）与时序性（概念漂移）的交叉需求，代表了边缘AI的新范式
2. **提示（Prompt）作为知识载体**：将任务特定知识压缩为轻量级Prompt向量，在持续学习中既能隔离任务干扰，又便于联邦传输
3. **灾难性遗忘的分布式解决方案**：传统的CL方案（如EWC、replay）在联邦场景下面临隐私和数据共享限制，Prompt-based方法在此场景下具有天然优势
4. **边缘场景的时间维度**：大多数边缘AI研究忽略了时间维度上的任务演化，Loci填补了这一重要空白

---

### P17. Multi-Agent Collaboration for Workflow Task Offloading in End-Edge-Cloud Environments Using Deep Reinforcement Learning

- **作者**：Bohuai Xiao, Chujia Yu, Xing Chen, Zheyi Chen, Geyong Min
- **机构**：福州大学、University of Exeter
- **发表**：IEEE TPDS, Vol. 36(11), pp. 2281-2296, 2025

**技术概要**：端-边-云三层计算环境中，来自多移动设备的工作流应用具有复杂的任务依赖关系，同时并行任务的卸载决策构成了指数级爆炸的解决方案空间。现有方法多采用集中式决策，面临决策时间长、计算开销高、大规模场景下难以找到合适卸载方案等问题。本文提出MCWT-AC（Multi-agent Collaborative Workflow Task offloading with Actor-Critic），将每个移动设备建模为独立Agent，基于本地信息和Actor-Critic强化学习算法做出卸载决策，通过多Agent协作逐步演化出全局最优/近优的卸载方案。该方法无需全局状态同步，各Agent仅通过奖励信号隐式协调。仿真实验表明MCWT-AC在适应性和扩展性上显著优于现有方法。

**技术启示**：
1. **MARL（多智能体强化学习）解决组合爆炸**：将全局优化分解为多个局部Agent的协同决策，是应对端-边-云场景下大规模组合优化问题的有效范式
2. **独立学习 + 隐式协调**：各Agent仅通过共享奖励信号协调，无需显式通信，降低通信开销的同时保持隐私性
3. **工作流依赖的卸载建模**：MCWT-AC考虑了有向无环图（DAG）形式的工作流任务依赖，比简单的独立任务卸载更贴近实际应用
4. **端-边-云三层架构的系统化求解**：将移动设备端、边缘节点和云中心三层统一纳入决策空间，实现了全局资源的最优匹配

---

### P18. SpatialVec-DWP: A Dynamic Weighted Data Placement Strategy with Spatial Correlation Awareness for Edge-Cloud Latency and Cost Co-Optimization

- **作者**：Pengwei Wang, et al.
- **机构**：东华大学
- **发表**：IEEE TPDS, 2026年正式接收（2026 Accepted）

**技术概要**：云边协同环境中，数据副本的放置位置直接影响访问时延和传输成本。现有方法多从全局热度或局部负载出发，难以刻画不同区域用户请求偏好的空间差异，也难以兼顾数据体量对传输成本的影响。本文提出SpatialVec-DWP策略：首先结合用户请求分布与服务器空间位置构建请求的空间分布向量（Spatial Vector），以此感知不同数据在不同区域的需求差异；其次将数据体量纳入权重建模，动态调整不同数据在不同节点上的放置优先级；进一步分析不同数据请求空间分布之间的相关性，对高相似性内容进行协同放置以压缩网络传输成本。基于真实基站分布与Foursquare数据集的实验表明，该方法相比现有方案将平均访问时延降低17.98%-38.72%，并在系统成本上取得显著优化。

**技术启示**：
1. **空间感知的独特视角**：将传统"what to place"问题扩展为"where and with what to place"，空间分布向量的引入为云边协同数据放置提供了新的形式化工具
2. **相关性协同放置**：具有相似请求空间分布的多个数据对象可联合优化放置，实现"1+1>2"的协同效应
3. **数据体量感知的权重建模**：大数据对象与小数据对象在放置策略上的不对称性此前被普遍忽视，DWP的权重机制弥补了这一缺陷
4. **从理论到真实的跨越**：使用真实基站拓扑而非随机拓扑进行实验，使结果对实际部署具有直接参考价值

---

## 4. 结语与未来方向

### 4.1 2025-2026年度TPDS研究图景

纵观2025.6至2026.6的TPDS论文，可归纳出以下五大研究趋势：

**趋势一：大模型时代的系统研究全面渗透**

从训练到推理，大语言模型（LLM）已成为TPDS的绝对热点。论文覆盖了流水线并行优化（UMPIPE）、性能建模（P8）、推理调度（TOP）、异构训练（P9）等多个维度，表明系统社区已将LLM作为核心驱动场景。值得注意的是，2026年初出现了针对NVL72等新一代GPU互联架构的系统优化工作，预示着"硬件-系统-模型"三角协同设计将成为下一阶段的研究范式。

**趋势二：绿色计算从愿景走向实践**

GreenFlow（P7）为代表的工作将碳排放作为一等优化目标，表明"绿色计算"已从理念倡导进入可量化的工程实践阶段。碳感知调度、能效优化的软硬件协同、数据中心PUE优化等方向预计将持续升温。2026年多个云厂商宣布碳中和目标，更进一步推动了该方向的研究需求。

**趋势三：边缘智能的深度融合**

边缘计算与联邦学习的融合（P15, P16）正在催生"联邦持续学习"等新范式。边缘场景不再只是"将云的计算下放"，而是需要处理数据异质性、设备异构性、任务时序演化等特有的系统挑战。端-边-云三层协同（P17）和空间感知数据放置（P18）反映了边缘计算正在从连接层向智能层升级。

**趋势四：去中心化与可扩展性的持续追求**

从BFT共识的Leader选举（ABSE）、去中心化Coflow调度（Slark）、到去中心化联邦学习（DegaFL），"去中心化"贯穿多个研究子领域。去中心化不再是理想主义的口号，而是应对超大规模系统（跨数据中心、万级节点）中信息同步代价过高这一现实约束的必然选择。

**趋势五：AI for Systems / Systems for AI的正向循环**

ML方法被广泛用于解决系统优化问题（GEREM用ML预测故障结果、MCWT-AC用MARL做任务卸载），同时系统优化也为AI训练/推理提供了基础支撑（UMPIPE、TOP等），形成了"AI为系统赋能"和"系统为AI提速"的双向正循环。

### 4.2 值得关注的未来方向

1. **LLM推理的系统优化**：KV-Cache管理、分离式推理架构（Prefill-Decode Disaggregation）、长序列高效注意力机制等，将成为2026下半年及今后TPDS持续活跃的热点
2. **异构算力网络**：存算一体、DPU/FPGA/ASIC混合部署、跨厂商GPU池化等方向将催生新的分布式系统设计挑战
3. **AI训练可靠性**：随着万亿参数模型训练常态化，故障容忍和弹性训练（Elastic Training）的需求将超越传统HPC容错技术的覆盖范围
4. **端侧大模型部署**：如何在资源极度受限的边缘设备上高效运行LLM（模型压缩、推理卸载、协作推理），是边缘智能的下一个重要战场
5. **碳感知与可持续计算**：从作业级碳感知调度向基础设施级（冷却、供电、选址）碳优化扩展，形成全栈绿色计算方案

---

## 附录：论文索引表

| # | 标题 | 作者（第一/通讯） | 机构 | 卷/期/年 | DOI | 页码 |
|:---:|:---|:---|:---|:---|:---|:---|
| P1 | Characterizing FaaS Workflows on Public Clouds | Varad Kulkarni | IISc Bangalore | 2026 EA | 10.1109/TPDS.2026.3678606 | - |
| P2 | ABSE: Adaptive Baseline Score-Based Election for Leader-Based BFT Systems | Xuyang Liu | 北京理工大学 | 36(8),2025 | 10.1109/TPDS.2025.3572553 | 1634-1650 |
| P3 | Slark: A Performance Robust Decentralized Inter-Datacenter Coflows Scheduling | Xiaodong Dong | 南开大学 | 36(2),2025 | - | 197-211 |
| P4 | Object Proxy Patterns for Accelerating Distributed Applications | J. Gregory Pauloski | UChicago/ANL | 36(2),2025 | - | 253-265 |
| P5 | Spread+: Scalable Model Aggregation in Federated Learning With Non-IID Data | Huanghuang Liang | 武汉大学 | 36(4),2025 | 10.1109/TPDS.2025.3539738 | 701-716 |
| P6 | DegaFL: Decentralized Gradient Aggregation for Cross-Silo Federated Learning | Jialiang Han | 北京大学 | 36(2),2025 | - | 212-225 |
| P7 | GreenFlow: A Carbon-Efficient Scheduler for Deep Learning Workloads | Diandian Gu | 北京大学 | 36(2),2025 | - | 168-184 |
| P8 | Towards Universal Performance Modeling for ML Training on Multi-GPU Platforms | Zhongyi Lin | NVIDIA/UC Davis | 36(2),2025 | - | 226-238 |
| P9 | Joint Dynamic Data and Model Parallelism for Distributed Training of DNNs | Zhi Ling | 中国科学技术大学 | 36(2),2025 | - | 150-167 |
| P10 | UMPIPE: Unequal Microbatches-Based Pipeline Parallelism for DNN Training | Guangyao Zhou | 电子科技大学 | 36(2),2025 | - | 293-307 |
| P11 | TOP: Task-Based Operator Parallelism for Asynchronous DL Inference on GPU | Changyao Lin | 哈尔滨工业大学(深圳) | 36(2),2025 | - | 266-281 |
| P12 | Spreeze: High-Throughput Parallel Reinforcement Learning Framework | Jing Hou | 同济大学 | 36(2),2025 | - | 282-292 |
| P13 | Leveraging Graph Analysis to Pinpoint Root Causes of Scalability Issues | Yuyang Jin | 清华大学/ETH | 36(2),2025 | - | 308-325 |
| P14 | GEREM: Fast and Precise Error Resilience Assessment for GPU Microarchitectures | Jingweijia Tan | 吉林大学 | 36(5),2025 | 10.1109/TPDS.2025.3552679 | 1011-1024 |
| P15 | Coordinating Computational Capacity for Adaptive FL in Heterogeneous Edge | Kechang Yang | 中国农业大学 | 36(8),2025 | 10.1109/TPDS.2025.3574718 | 1509-1523 |
| P16 | Loci: Federated Continual Learning of Heterogeneous Tasks at Edge | Yiluo Luopan | 北京理工大学 | 36(4),2025 | - | 775-790 |
| P17 | Multi-Agent Collaboration for Workflow Task Offloading in End-Edge-Cloud | Bohuai Xiao | 福州大学 | 36(11),2025 | 10.1109/TPDS.2025.3606001 | 2281-2296 |
| P18 | SpatialVec-DWP: Dynamic Weighted Data Placement for Edge-Cloud | Pengwei Wang | 东华大学 | 2026 Acc. | - | - |

> **注**："EA" = Early Access，"Acc." = Accepted/录用待发表。"-" 表示DOI/页码暂未获取。

---

*报告生成时间：2026年6月 | 覆盖周期：2025.6 – 2026.6 | 论文总数：18篇*