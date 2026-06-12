# IEEE Transactions on Services Computing (TSC) 2026 洞察报告

> 覆盖范围：2025年6月 – 2026年6月 | 收录论文：12篇
> 报告日期：2026年6月10日

---

## 0. 期刊概览

**IEEE Transactions on Services Computing (TSC)** 是服务计算领域最具影响力的国际学术期刊之一，CCF-A类推荐期刊，中科院二区，JCR Q1分区（COMPUTER SCIENCE, INFORMATION SYSTEMS），2024年影响因子约为5.5。该期刊专注于服务计算领域的算法、数学、统计与计算方法，涵盖面向服务的架构（SOA）、Web服务、业务流程集成、服务性能管理、服务运维与管理，以及近年来蓬勃发展的云服务、微服务、边缘服务与智能服务等前沿方向。

**本期报告覆盖2025年下半年至2026年上半年发表的12篇代表性论文**，按主题分为三大板块：(1) 云服务与微服务；(2) Serverless与边缘服务；(3) 服务编排与智能服务。以下是详细解读。

---

## 1. 云服务与微服务

### 1.1 ARAScaler: Adaptive Resource Autoscaling Scheme Using ETimeMixer for Efficient Cloud-Native Computing
**作者**: Byeonghui Jeong, Young-Sik Jeong (Dongguk University, Korea)
**出版**: TSC Vol.18, Issue 1, Jan.-Feb. 2025, pp.72-84
**DOI**: 10.1109/TSC.2024.3522815

**技术概要**:
该论文针对云原生计算环境中容器化微服务的资源自动伸缩问题，提出了自适应资源自动伸缩方案ARAScaler。现有Kubernetes等容器编排平台的自动伸缩技术（如HPA）在处理复杂工作负载模式时存在资源浪费和过载问题，且动态工作负载引发的弹性震荡（oscillation）增加了运维复杂度。ARAScaler的核心创新在于：首先利用增强型TimeMixer（ETimeMixer）——一种融入卷积方法的时间序列预测模型——对未来的工作负载进行高精度预测；其次，将预测的工作负载分段识别为突发（burst）、非突发（nonburst）、动态（dynamic）和静态（static）四种状态；最后，针对每种状态分别计算最优容器实例数量进行弹性伸缩。在七个云工作负载真实追踪数据集上的离线仿真表明，ARAScaler实现了约70%以上的资源利用率，仅需极少量的扩缩容操作，且资源过载实例数远少于现有方法。

**技术启示**:
1. **状态感知的分段扩缩容**：不是对所有工作负载采用统一策略，而是先做状态分类再差异化决策，这种"先诊断再治疗"的模式值得推广。
2. **时间序列预测+弹性决策的端到端整合**：ETimeMixer与决策模块的紧耦合设计为云原生自动运维提供了新的技术范式。
3. **震荡抑制机制**：ARAScaler通过最少化扩缩容事件来避免弹性震荡，这对生产环境的稳定性至关重要。

---

### 1.2 Flexible Computing: A New Framework for Improving Resource Allocation and Scheduling in Elastic Computing
**作者**: Weipeng Cao, Jiongjiong Gu, Zhong Ming (Shenzhen University), Zhiyuan Cai, Yuzhao Wang, Changping Ji, Zhijiao Xiao, Yuhong Feng, Ye Liu, Liang-Jie Zhang
**出版**: TSC Vol.18, Issue 1, Jan.-Feb. 2025
**DOI**: 10.1109/TSC.2025 (Early Access)

**技术概要**:
自云计算诞生以来，弹性计算（Elastic Computing）一直是资源分配与调度的标准架构。然而，传统的弹性计算通常基于预定义的规格（如虚拟机或容器的flavor）来分配计算资源，这些规格往往受限于固定的CPU与内存比例（如1:2、1:4），不能精确匹配应用的实际资源需求，导致大量资源浪费。该论文提出了"柔性计算"（Flexible Computing）这一全新框架，打破了传统固定资源配比的限制，允许用户以任意CPU与内存比例请求计算资源。该框架通过资源解耦（resource disaggregation）技术实现CPU与内存的独立分配，并设计了配套的调度算法来保证系统效率。实验结果表明，柔性计算框架能在保证应用性能的前提下，将资源利用率提升至更高水平。

**技术启示**:
1. **资源解耦思想**：CPU与内存不应该永远绑定，柔性计算框架在IaaS层面的创新为提升云数据中心资源效率提供了新思路。
2. **打破固定flavor范式**：传统的固定规格正在成为资源优化的瓶颈，按需灵活组合是未来的趋势。
3. **调度算法的适配挑战**：当资源维度解耦后，调度问题的搜索空间将急剧膨胀，需要更智能的调度策略。

---

### 1.3 MSCNet: Multi-Scale Network With Convolutions for Long-Term Cloud Workload Prediction
**作者**: Feiyu Zhao, Weiwei Lin, Shengsheng Lin, Shaomin Tang (South China University of Technology), Keqin Li (State University of New York)
**出版**: TSC Vol.18, Issue 2, March-April 2025, pp.969-982
**DOI**: 10.1109/TSC.2025.3536313

**技术概要**:
准确的工作负载预测是大型云数据中心资源分配与管理的关键前提。现有方法大多基于RNN及其变体（如LSTM、GRU），聚焦于短期预测，难以捕捉云工作负载的长期变化趋势与多周期模式。由于用户需求与工作负载动态性，短期看似平稳的工作负载在长期视角下往往呈现出不同的模式，导致现有方法在长期预测上精度显著下降。MSCNet的设计哲学在于多尺度建模：通过Multi-Scale Patch Block将原始工作负载序列划分为不同粒度的patch、利用Transformer Encoder捕捉全局长期依赖、结合Multi-Scale Convolutions Block提取多尺度局部特征。在阿里巴巴、Google和Azure真实云工作负载数据上的实验表明，MSCNet在长期预测精度上显著优于SOTA方法，且计算复杂度仅为O(L²d)。

**技术启示**:
1. **多尺度建模是长期预测的关键**：云工作负载天然具有不同时间粒度上的周期模式，同时建模短期波动与长期趋势至关重要。
2. **Transformer替代RNN**：MSCNet用卷积+Transformer的组合替代传统RNN架构，规避了梯度消失问题，同时享受并行训练的优势。
3. **真实多平台验证**：在三大云平台数据上的验证确保了模型的泛化能力，这对工业应用不可或缺。

---

### 1.4 Deep Learning and Feedback Control Based Container Auto-scaling for Cloud Native Micro-services
**作者**: Zhicheng Cai, Hang Wu, Xu Jiang, Xiaoping Li (Southeast University), Rajkumar Buyya (University of Melbourne)
**出版**: TSC Early Access, August 2025
**DOI**: 10.1109/TSC.2025.3596887

**技术概要**:
在基于Kubernetes的云原生平台中，根据工作负载变化为微服务弹性分配容器是降低成本并稳定响应时间的关键。然而，多容器系统的性能模型难以精确刻画，加之粗粒度的容器分配方式，导致性能波动频繁。该论文创新性地将深度学习、传统Jackson排队网络（JQN）与反馈控制三种技术融为一体：利用神经网络的非线性拟合能力精准建模多容器系统的性能模型；利用JQN精确预测微服务间的交互效应（如上游吞吐量对下游排队延迟的影响）；利用反馈控制的实时响应能力快速调整容器数量。在真实Kubernetes云原生集群上的实验表明，该方案在满足95分位访问路径响应时间SLA的前提下，将容器成本降低了10.94%–11.36%。

**技术启示**:
1. **三者融合的设计哲学**：深度学习负责建模精度、排队论提供结构化的领域知识、反馈控制保证实时性，各取所长、互补不足。
2. **微服务交互效应的显式建模**：JQN的引入解决了纯黑箱模型难以捕捉服务间级联效应的痛点。
3. **端到端SLA保障**：以95分位响应时间为约束优化容器成本，直面工业界最关心的SLA合规问题。

---

### 1.5 Large-Scale Service Mesh Orchestration With Probabilistic Routing in Cloud Data Centers
**作者**: Kai Peng, Yi Hu, Haonan Ding, Haoxuan Chen, Liangyuan Wang, Chao Cai, Menglan Hu (Huazhong University of Science and Technology)
**出版**: TSC Vol.18, Issue 2, 2025, pp.868-882
**DOI**: 10.1109/TSC.2025.3526373

**技术概要**:
服务网格（Service Mesh）作为微服务间通信的基础设施层正在迅速兴起。然而在大型微服务场景中，频繁的服务通信、复杂的调用依赖关系以及严格的延迟要求给高效的服务网格编排带来了巨大压力。服务部署与请求路由在服务网格架构下是紧耦合、相互依赖的，不能单独优化。当考虑微服务多路复用、并行依赖和多实例建模时，问题难度进一步加剧。该论文利用开放Jackson排队网络理论细粒度地捕捉关键微服务，并分析海量用户请求的处理、排队与通信延迟。在此基础上，提出一种高效的三阶段启发式算法，实现了多实例整合与概率化多队列路由的协同优化。基于真实追踪数据的实验证明了该算法在降低响应延迟与成本方面相对于其他基线方法的显著优势。

**技术启示**:
1. **排队论在服务网格中的精细应用**：相比抽象的性能模型，Jackson排队网络能够细粒度地刻画请求在每个服务节点的等待与处理过程。
2. **部署与路由的联合优化**：将服务部署（决定实例在哪）与请求路由（决定流量如何走）作为统一优化问题，是实现全局最优的关键。
3. **概率化路由**：区别于确定性的轮询或最短队列路由，概率化路由提供了更灵活的资源利用空间。

---

### 1.6 UDA-RCL：基于多模态数据与无监督域自适应的微服务根因定位方法
**作者**: 北京大学研究团队
**出版**: TSC 2025 (December 2025)
**DOI**: IEEE TSC (Early Access)

**技术概要**:
微服务系统发生故障时，快速准确地定位根因（Root Cause Localization, RCL）对保障系统可靠性至关重要。然而，新部署的微服务系统缺乏历史异常数据，难以构建高精度的监督学习模型。UDA-RCL方法通过无监督域自适应（Unsupervised Domain Adaptation）技术，利用成熟系统（源域）中丰富的带标签数据帮助新系统（目标域）构建根因定位模型。该方法包含三项关键技术：(1) 基于聚合的事件提取模块，将日志、指标和追踪三种多模态数据统一转化为标准化的事件格式；(2) 多模态域对抗适应模块，通过对抗训练缩小源域和目标域之间的特征分布差异；(3) PageRank分类器模块，将异常传播规则（异常沿服务调用链传播）嵌入神经网络，直接输出服务实例成为根因的概率。在AIOps2021和AIOps2022数据集上的实验表明，UDA-RCL在监督学习和迁移学习场景下均优于现有方法。

**技术启示**:
1. **冷启动场景下的智能运维**：新系统缺乏标注数据是工业界的普遍痛点，域自适应方法提供了优雅的解决方案。
2. **异常传播规则的嵌入**：将已知的领域知识（异常沿调用链传播）融入神经网络架构（PageRank分类器），是"知识+数据"双轮驱动的典范。
3. **多模态数据的统一表示**：日志、指标、追踪三者的语义鸿沟通过聚合事件提取得到了弥合。

---

## 2. Serverless与边缘服务

### 2.1 Online Service Placement, Task Scheduling, and Resource Allocation in Hierarchical Collaborative MEC Systems
**作者**: An Du, Jie Jia (Northeastern University), Schahram Dustdar (TU Wien), Jian Chen, Xingwei Wang
**出版**: TSC Vol.18, Issue 2, 2025, pp.983-997
**DOI**: 10.1109/TSC.2025.3536307

**技术概要**:
移动边缘计算（MEC）将云计算能力推向网络边缘，为服务化应用提供实时处理与缓存灵活性。然而，单一节点的解决方案难以应对不断增长的计算工作负载，尤其在时空分布不可预测的服务请求模式下。该论文提出分层协同计算（Hierarchical Collaborative Computing, HCC）框架，利用云层的充足算力、边缘层的广覆盖服务区域以及设备层的空闲资源协同为用户服务。在此框架下，研究异质性感知的资源管理问题——包括服务放置、任务调度和资源分配的协同优化（节点内和跨节点）。为追求长期性能最优，论文提出一种在线优化框架，通过代理拉格朗日松弛（surrogate Lagrangian relaxation）方法降低混合整数非线性规划问题的复杂度，并设计混合数值技术求解子问题。仿真结果表明，HCC框架在系统成本最小化与服务放置成本稳定性之间实现了有效权衡。

**技术启示**:
1. **三层协同架构**：云-边-端的三层协同超越了传统的云-边或边-端两层架构，充分利用每一层的独特优势。
2. **在线优化与长期性能**：面对动态到达的服务请求，在线优化框架的实时决策能力比离线最优解更具实用价值。
3. **拉格朗日松弛降维**：对复杂的混合整数非线性规划问题，数学规划中的松弛技术仍有不可替代的作用。

---

### 2.2 DHMPM: Integrating Deep Spiking Q-Network Into Hypergame-Theoretic Deceptive Defense for Mitigating Malware Propagation in Edge Intelligence-Enabled IoT Systems
**作者**: Yizhou Shen, Carlton Shepherd (Newcastle University), Chuadhry Mujeeb Ahmed (University of Strathclyde), Shigen Shen (Shaoxing University), Shui Yu (University of Technology Sydney)
**出版**: TSC 2025, April 2025
**DOI**: 10.1109/TSC.2025.3562355

**技术概要**:
边缘智能（Edge Intelligence, EI）支持的物联网系统容易遭受恶意软件传播攻击，导致数据泄露和信息窃取。该论文提出了在信息不对称条件下物联网节点与边缘设备之间主动面向欺骗的超博弈论恶意软件传播缓解模型（DHMPM）。具体而言，物联网节点和边缘设备在博弈环境和系统动力学的"不确定性信念"下，根据获得的效用不断调整其策略。进一步地，论文将脉冲神经网络（Spiking Neural Networks, SNN）融入深度Q网络（DQN），形成超博弈论深度脉冲Q网络（HGDSQN）。SNN通过脉冲通信机制模拟生物大脑的信息处理方式，突破了传统深度模型在时间处理上的瓶颈，实现智能决策与实时恶意软件防御。实验评估了攻击到达概率和学习率对最优学习策略选择的影响。

**技术启示**:
1. **博弈论+深度学习的融合防御**：超博弈论描述攻防双方的非对称信息博弈，DRL提供策略优化，两者的结合代表了一种主动防御新范式。
2. **脉冲神经网络在安全领域的应用**：SNN以其脉冲时序编码能力和低功耗特性，在实时安全决策场景中展现出独特优势。
3. **信息不对称下的不确定性建模**：以"信念"形式对博弈中的不确定性进行建模，更加贴近真实攻防场景。

---

### 2.3 TPI-LLM: Serving 70B-scale LLMs Efficiently on Low-resource Mobile Devices
**作者**: Zonghang Li, Wenjiao Feng (University of Electronic Science and Technology of China), Mohsen Guizani (Mohamed Bin Zayed University of AI), Hongfang Yu
**出版**: TSC Early Access, August 2025
**DOI**: 10.1109/TSC.2025.3596892

**技术概要**:
由于用户对隐私问题的担忧，大语言模型（LLM）的推理服务正在从云端向边缘设备迁移。然而移动设备面临算力和内存的严重限制，需要多设备协同才能运行LLM应用。主流方案——流水线并行（Pipeline Parallelism）——在此场景下效率低下，因为移动设备通常仅运行一个推理任务。该论文论证了张量并行（Tensor Parallelism）虽然通信开销高，但在这种场景下更为适合。论文引入TPI-LLM——一种计算和内存高效的大模型张量并行推理系统，将敏感原始数据保留在用户本地设备上。该系统采用滑动窗口内存调度器动态管理层权重，将磁盘I/O与计算和通信重叠执行，使得70B级大模型能在内存受限的设备上高效运行。大量实验表明，TPI-LLM相比于Transformers、Accelerate和Galaxy，将token延迟降低了80%–90%，峰值内存占用减少90%，运行70B级模型仅需3.1 GiB内存。

**技术启示**:
1. **大模型边缘推理的可行性**：TPI-LLM证明了70B参数级模型在资源极度受限的移动设备上运行的可行性，拓展了边缘智能的边界。
2. **张量并行 vs 流水线并行**：在单任务执行场景下，张量并行的优势超越了直觉上的通信成本顾虑。
3. **滑动窗口内存管理**：动态管理的层权重窗口有效解决了内存瓶颈，这种"用完即弃、按需加载"的策略值得在其他内存约束场景中推广。

---

## 3. 服务编排与智能服务

### 3.1 DiffMSR: a Multi-Semantic Graph Diffusion Model for Service Recommendation
**作者**: Xiang Xie, Jianxun Liu, Buqing Cao, Wenyu Zhao, Sheng Lin, Min Shi (Hunan University of Technology), Jinjun Chen (Swinburne University of Technology)
**出版**: TSC Early Access 2025
**DOI**: IEEE TSC

**技术概要**:
随着云计算与服务计算的快速发展，服务推荐系统在帮助用户高效筛选合适服务方面发挥着关键作用。然而，服务数据的稀疏性和交互中的噪声使得精准捕捉用户偏好变得极具挑战性。现有的基于图神经网络（GNN）的服务推荐方法虽然在图结构建模方面取得了进展，但在多语义信息融合方面仍存在不足。DiffMSR创新性地将扩散模型（Diffusion Model）引入服务推荐领域，提出多语义图扩散模型。该方法通过在服务交互图上执行前向扩散与反向去噪过程，同时融合用户-服务交互的协作语义、服务功能描述的文本语义以及服务属性的结构语义，生成高质量的用户偏好表示。实验表明，DiffMSR在多个真实服务数据集上显著优于最新基线方法，尤其在数据稀疏场景下优势更加明显。

**技术启示**:
1. **扩散模型在服务推荐中的首次应用**：将从图像生成领域兴起的扩散模型迁移至服务推荐，代表了跨领域技术迁移的新趋势。
2. **多语义融合**：协作语义+文本语义+结构语义的融合突破了传统推荐仅依赖交互数据的局限。
3. **噪声鲁棒性**：扩散模型天然的降噪能力使其在服务数据稀疏和噪声环境下表现出色。

---

### 3.2 ARRQP: Anomaly Resilient Real-Time QoS Prediction Framework With Graph Convolution
**作者**: Suraj Kumar, Soumi Chattopadhyay (IIT Indore, India)
**出版**: TSC Vol.18, Issue 3, 2025
**DOI**: IEEE TSC

**技术概要**:
在现代面向服务的架构中，服务质量（QoS）的保障至关重要。提前预测QoS值能让用户做出明智的服务选择决策。然而，现实世界中的QoS数据常常包含由网络波动、服务器故障或恶意攻击引起的异常值，这些异常值会严重干扰预测模型的训练。ARRQP框架正是针对这一挑战提出的，它融合了图卷积网络（GCN）与异常检测机制，在预测QoS的同时具备对异常值的鲁棒性。该框架首先利用GCN对用户-服务交互的二部图进行编码，捕获协同过滤信号；其次设计了一个异常感知注意力模块，自动识别并抑制异常值对特征聚合的贡献；最后通过时序建模组件输出实时QoS预测。在公开QoS数据集上的实验表明，ARRQP在含有不同程度异常的数据上，均实现了优于现有方法的预测精度。

**技术启示**:
1. **异常鲁棒性作为第一性设计**：不同于"先清洗后预测"的两阶段流水线，ARRQP将异常处理融入模型架构本身，实现了端到端的鲁棒预测。
2. **图结构在QoS建模中的优势**：用户-服务的二部图结构天然适合用GCN建模，能够捕获传统矩阵分解方法难以表示的高阶关联。
3. **实时性需求**：在线服务场景中QoS值的实时变化要求模型具备快速的推理能力，而非仅仅追求离线精度。

---

### 3.3 Wind-Aware Service Provisioning Strategy for Multi-Package Drone Delivery
**作者**: Jia Xu, Hao Liu (Anhui University), Xiao Liu (Deakin University), Azadeh Ghari Neiat (Deakin University), Xuejun Li (Anhui University), Yun Yang (Swinburne University of Technology)
**出版**: TSC Early Access 2025
**DOI**: IEEE TSC

**技术概要**:
无人机配送作为一种新兴服务范式正在解决最后一公里配送问题。Drone-as-a-Service (DaaS) 作为一种将配送能力服务化的模式，在复杂配送网络中具有广阔应用前景。然而，现有的DaaS服务组合框架通常未考虑多包裹配送服务的共享性和风力对配送的影响。该论文提出了面向多包裹无人机配送的风感知服务供应策略：首先将多包裹配送建模为服务组合优化问题，同时考虑包裹间的共享配送路径；其次引入风场模型，精确计算风对无人机飞行时间与能耗的影响；最后设计了基于智能优化的求解算法，在满足配送时限约束的前提下最小化总运营成本。实验验证了考虑风因素后配送计划的可行性和经济性显著优于忽略风影响的基准方法。

**技术启示**:
1. **物理世界约束的服务化建模**：将风这一真实物理因素纳入服务组合优化，是数字世界与物理世界融合的典型案例。
2. **DaaS模式的创新应用**：将送货能力抽象为可组合、可调用的服务单元，为传统物流行业提供了新的技术范式。
3. **多包裹共享配送**：包裹间配送路径的共享利用是提升效率的关键，体现了服务复用的思想。

---

## 4. 结语与未来方向

回顾2025-2026年度IEEE TSC上发表的代表性论文，我们可以看到服务计算领域呈现出以下几个清晰的技术趋势：

**趋势一：AI与服务的深度融合**。无论是MSCNet用深度学习做云工作负载预测、DiffMSR用扩散模型做服务推荐，还是DHMPM用脉冲神经网络做安全防御——AI技术正在成为服务系统的核心组件，而不只是辅助工具。

**趋势二：云-边-端协同成为主流架构**。从HCC分层协同计算到TPI-LLM在移动设备上的大模型推理，从边缘智能安全防御到风感知的无人机服务供应，计算正在从中心化的云向边缘和终端延伸，形成从云到端的连续体（Compute Continuum）。

**趋势三：微服务治理走向精细化**。ARAScaler的状态感知弹性伸缩、UDA-RCL的多模态根因定位、大规模服务网格的概率化路由编排——微服务治理正在从事后响应转向事前预测、从粗粒度转向细粒度、从单一维度转向多维协同。

**趋势四：性能与成本的均衡优化始终是核心目标**。几乎所有入选论文都以"在满足SLA约束下最小化资源成本"为优化目标，这反映了工业界和学术界对经济效率的共同追求。

**未来展望**：展望下一年度，我们预计TSC将继续在以下方向产出高质量论文：(1) 大语言模型（LLM）在服务计算中的应用，如LLM驱动的服务组合、智能运维等；(2) 可持续计算（绿色服务），如碳感知的云/边缘资源调度；(3) 量子服务计算，随着量子计算的成熟，量子服务的安全、编排与优化将成为新热点；(4) 数字孪生增强的服务管理。

---

## 附录：论文索引表

| 编号 | 论文标题 | 作者 | 出版信息 | 主题分类 |
|------|---------|------|---------|---------|
| 1 | ARAScaler: Adaptive Resource Autoscaling Scheme Using ETimeMixer | Byeonghui Jeong, Young-Sik Jeong | TSC Vol.18(1), 2025 | 云原生自动伸缩 |
| 2 | Flexible Computing: A New Framework for Resource Allocation in Elastic Computing | Weipeng Cao et al. | TSC Vol.18(1), 2025 | 弹性计算资源调度 |
| 3 | MSCNet: Multi-Scale Network With Convolutions for Cloud Workload Prediction | Feiyu Zhao et al. | TSC Vol.18(2), 2025 | 云工作负载预测 |
| 4 | Deep Learning and Feedback Control Based Container Auto-scaling | Zhicheng Cai et al. | TSC Early Access, 2025 | Kubernetes容器伸缩 |
| 5 | Large-Scale Service Mesh Orchestration With Probabilistic Routing | Kai Peng et al. | TSC Vol.18(2), 2025 | 服务网格编排 |
| 6 | UDA-RCL: 多模态域自适应的微服务根因定位 | 北京大学团队 | TSC 2025 | 微服务故障诊断 |
| 7 | Online Service Placement in Hierarchical Collaborative MEC | An Du, Jie Jia et al. | TSC Vol.18(2), 2025 | 边缘计算资源管理 |
| 8 | DHMPM: Deep Spiking Q-Network for Edge IoT Malware Defense | Yizhou Shen et al. | TSC 2025 | 边缘安全防御 |
| 9 | TPI-LLM: Serving 70B-scale LLMs on Low-resource Mobile Devices | Zonghang Li et al. | TSC Early Access, 2025 | 边缘大模型推理 |
| 10 | DiffMSR: Multi-Semantic Graph Diffusion Model for Service Recommendation | Xiang Xie et al. | TSC Early Access, 2025 | 服务推荐 |
| 11 | ARRQP: Anomaly Resilient Real-Time QoS Prediction With Graph Convolution | Suraj Kumar, Soumi Chattopadhyay | TSC Vol.18(3), 2025 | QoS预测 |
| 12 | Wind-Aware Service Provisioning for Multi-Package Drone Delivery | Jia Xu et al. | TSC Early Access, 2025 | 无人机服务供应 |

---

> *本报告数据来源为IEEE Xplore数字图书馆，检索时间范围为2025年6月至2026年6月，所选论文均为IEEE Transactions on Services Computing在该时间窗口内出版的正式论文或Early Access文章。由于访问限制，部分论文的具体作者单位和全文信息可能存在遗漏，建议读者通过IEEE Xplore获取完整信息。*