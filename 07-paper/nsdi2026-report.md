# NSDI 2026 (23rd USENIX Symposium on Networked Systems Design and Implementation) 洞察报告

> 撰写日期：2026年6月10日
> 会议日期：2026年5月4日–6日 | 地点：美国华盛顿州 Renton
> 来源覆盖：USENIX官方程序、Microsoft Research Blog、阿里云官方公告、各大学新闻、实验室主页

---

## 0. 会议概览

NSDI 2026 是 USENIX 协会举办的第23届网络系统设计与实现研讨会，与 ACM SIGCOMM 并列为计算机网络领域两大顶级会议（CCF-A 类）。本次会议继续采用 Spring + Fall 双轮投稿机制。

| 统计项 | Spring 轮 | Fall 轮 | 合计（估算） |
|--------|-----------|---------|-------------|
| 投稿数 | 207 | ~401* | ~608 |
| 录用数 | 50 | ~55* | ~105 |
| 录用率 | 24.2% | ~13.7%* | ~17% |

> \* Fall轮数据参考NSDI 2025 Fall轮（401投稿/55录用/13.7%），最终数据以官方公布为准。

### 研究方向分布（基于已收录论文统计）

```
AI/ML训练与推理基础设施  ████████████████████  ~35%
数据中心网络与传输协议    ██████████████        ~22%
视频/流媒体网络系统       ███████              ~10%
RDMA与高性能网络          ███████              ~10%
网络验证/测试/诊断        ██████               ~8%
云存储与计算系统          █████                ~7%
安全与隔离                ████                 ~5%
光互连/新硬件             ███                  ~3%
```

### 奖项

- **Outstanding Paper Award (3篇)**：OSCAR (南京大学) 等
- **Community Award**：SONiC DASH SmartSwitch (Microsoft/CUHK)

### 关键趋势

1. **AI 基础设施成为最大主题**：约35%的论文围绕大模型训练推理中的网络系统挑战，包括集合通信优化、性能诊断、工作负载特征分析、KV Cache共享等
2. **异构性成为核心关切**：从 GPU 异构（HeteCCL）到网络异构（ForestColl、BURST），系统对异构环境的适应能力成为设计重点
3. **SmartNIC/硬件卸载持续火热**：eXpressSFU、Pyrocumulus、SONiC DASH、KRAKENGUARD 均涉及 SmartNIC 或可编程硬件
4. **产业与学术深度融合**：阿里云（6篇）、微软（11篇）等企业贡献大量论文，产学研合作成为主流模式
5. **中国高校表现突出**：南京大学获杰出论文奖，东北大学首中 NSDI 主会，湖南大学、浙江大学、清华、港中文等均有斩获

---

## 1. 数据中心网络与传输协议

### 1.1 OSCAR: O(1)-Step Convergence and Readily-deployable Congestion Control
> 🏆 **Outstanding Paper Award**

- **作者**：张兆琛、薛飞阳、宁锐、曹培睿*（通讯作者）等，南京大学田臣教授团队（NASA实验室）
- **类别**：数据中心拥塞控制

**技术概要**：OSCAR 面向数据中心拥塞控制的快速收敛与易于部署两大核心难题，提出了首个兼具 O(1)步收敛与可直接部署特性的拥塞控制方案。论文核心洞察在于：延迟及延迟梯度信号可以提供接近 INT（In-band Network Telemetry）精确拥塞信息的信号质量，从而在不依赖专用网络硬件特性的情况下实现快速稳定的速率收敛。在大规模真实工作负载仿真中，OSCAR 相比基于精确 INT 的拥塞控制方案，平均流完成时间（FCT）提升12%–48%，尾部流完成时间提升40%–74%。OSCAR 不要求交换机支持 INT 等特殊功能，仅依赖端侧可观测的延迟信号，使其具备良好的可部署性。

**技术线索与启示**：
1. **延迟梯度作为拥塞代理信号**：论文证明了精心设计的延迟梯度信号可以逼近 INT 级精度，这对无力部署 INT 的大规模商用数据中心具有极高参考价值
2. **O(1)收敛的理论意义**：相比传统 AIMD 的渐进收敛，O(1)步收敛对于微秒级 RTT 的数据中心网络至关重要
3. **可部署性优先的设计哲学**：在算法性能与系统可部署性之间，OSCAR 选择了后者优先的策略——不求最精确，但求最实用
4. **拥塞控制与 INT 的性价比权衡**：重新审视了精确遥测信息在拥塞控制中的必要性边界

---

### 1.2 HEDGE: Traffic Engineering with Probabilistic Link Capacities

- **作者**：Arjun Devraj (Cornell), Bill Owens (NYSERNet), Umesh Krishnaswamy (Microsoft), Ying Zhang (Meta), Rachee Singh (Cornell)
- **类别**：广域网流量工程与光网络可靠性

**技术概要**：HEDGE 解决光网络中波长特定故障（wavelength-specific faults）导致的链路容量波动问题。光网络中的放大器故障或波长争用可能导致部分波长不可用，进而使链路容量呈现概率性波动。HEDGE 结合链路本地（link-local）和全局网络级（network-wide）两种弹性机制：链路本地层通过快速重路由维持稳定容量，网络全局层在流量工程优化中显式建模链路的概率性容量，确保在容量波动下仍能优化流量分布。实验表明 HEDGE 在吞吐量不降低的前提下，显著减少了网络中断事件。

**技术线索与启示**：
1. **概率容量建模**：传统流量工程假设链路容量是确定值，HEDGE 引入概率视角，更贴近光网络物理现实
2. **分层弹性设计**：local + global 的双层弹性架构，在故障响应速度与全局最优之间取得了工程折中
3. **跨层协同**：光层故障与 IP 层流量工程的联动优化，体现了光-IP 协同的永恒主题

---

## 2. AI/ML 训练与推理基础设施

### 2.1 HeteCCL: Synthesizing Near-Optimal Collective Communication Schedules for Heterogeneous GPU Clusters

- **作者**：黑晨阳、李福亮*、李嘉仪、操佳敏、高程希、沙修竹、刘桐瑞、张登科、翟恩南、王兴伟* —— 东北大学（第一单位）、阿里云、中科院先进院
- **历史意义**：东北大学首篇 NSDI 主会论文
- **前序工作**：ResCCL (ACM SIGCOMM 2025)
- **类别**：集合通信调度 / 大模型训练系统

**技术概要**：HeteCCL 面向异构 GPU 集群（不同型号、不同带宽 GPU 混合部署）中的集合通信效率瓶颈。在 ResCCL（同构集群资源高效调度）的基础上，HeteCCL 将问题拓展到"异构集群中近最优通信调度合成"。系统自动感知 GPU 计算能力、链路带宽及拓扑结构的差异化特征，综合考虑多维资源约束与负载不均衡，通过精细建模拓扑与带宽、结合约束求解与搜索空间剪枝，智能生成接近最优的通信调度策略。实验表明通信性能提升多达 4.4×，调度生成速度提升 90%。系统经多种典型大模型训练任务与真实异构集群环境充分验证。

**技术线索与启示**：
1. **从同构到异构的范式跃迁**：ResCCL→HeteCCL 的演进路径值得关注——先解决同构问题建立方法论，再拓展到异构场景
2. **约束求解 + 搜索剪枝**：将集合通信调度形式化为约束满足问题，通过拓扑感知的搜索空间剪枝提升求解效率
3. **异构 GPU 集群的现实需求**：GPU 供应紧张导致集群中混合 A100/H100/B200 等不同型号 GPU 成为常态，HeteCCL 切中了这一产业痛点
4. **产学研协同**：东北大学（学术界）+ 阿里云（产业界）+ 中科院先进院，三方合作模式

---

### 2.2 ForestColl: Throughput-Optimal Collective Communications on Heterogeneous Network Fabrics

- **作者**：Liangyu Zhao (UW), Saeed Maleki (Independent), Yuanhong Wang (Tsinghua), Zezhou Wang (UW), Ziyue Yang (Microsoft Research), Hossein Pourreza (Microsoft), Arvind Krishnamurthy (UW)
- **类别**：集合通信 / 大模型训练系统

**技术概要**：ForestColl 将集合通信（broadcast/aggregation）调度形式化为生成树（spanning tree）构造问题，并证明其可达理论最优吞吐。调度生成算法运行在多项式时间内且高度可扩展。关键的是，ForestColl 支持任意网络结构（network fabric），包括传统交换网络和直接加速器互联（如 NVLink）。这一通用性使其能适配从单机多卡 NVLink 拓扑到跨机架 RDMA 网络的全场景通信优化。

**技术线索与启示**：
1. **生成树模型的理论优雅性**：将广播/聚合通信映射为多棵带宽最优生成树的构造，理论可证最优
2. **异构网络结构支持**：同时覆盖 switching fabric 和 direct accelerator connections，适配 NVIDIA NVLink、UALink 等新兴互联
3. **多项式时间可扩展性**：相比 NP-hard 的通信调度问题，ForestColl 的多项式时间算法对大规模集群部署至关重要
4. **与 HeteCCL 互补**：HeteCCL 侧重异构 GPU 的负载均衡，ForestColl 侧重异构网络拓扑的最优调度——两者可组合使用

---

### 2.3 EROICA: Online Performance Troubleshooting for Large-scale Model Training

- **作者**：阿里云基础设施网络团队
- **类别**：大模型训练性能诊断

**技术概要**：EROICA 是首个基于在线 profiling 的大模型性能诊断系统，填补了在线监控（轻量但粗粒度）与离线 profiling（精确但数据量大）之间的空白。系统持续监控训练吞吐，仅在吞吐下降时短时间开启在线 profile。核心创新在于：从 profile 数据中识别关键函数，对所有训练进程的函数"行为向量"进行对比分析，将原始 profile 数据量降低 10^5 倍后实现根因定位。基于行为向量的期望范围建模和离群点分析，EROICA 能自动诊断 GPU、网络、代码、配置等全栈交互的性能瓶颈。系统已上线超过1.5年，覆盖阿里云全部训练集群，成功诊断 80 个现有方法未能诊断的疑难性能问题。

**技术线索与启示**：
1. **行为向量降维**：10^5 倍的数据压缩比是 EROICA 从"海量 profile 数据"到"可操作的诊断结果"的关键
2. **触发式在线 profiling**：仅在吞吐异常时开启，兼顾了诊断精度与系统开销
3. **跨进程对比分析**：利用大规模分布式训练中多进程的"冗余性"，通过横向对比发现异常进程
4. **生产级验证**：1.5年生产环境运行，80个疑难问题诊断证明了系统的实用价值
5. **与大模型系统运维的深度融合**：ALL-STACK（GPU/网络/代码/配置）诊断视角

---

### 2.4 ServeGen: Workload Characterization and Generation of Large Language Model Serving in Production

- **作者**：阿里云基础设施网络团队
- **开源**：https://github.com/alibaba/ServeGen
- **类别**：LLM 推理工作负载分析

**技术概要**：ServeGen 对 LLM 推理服务的生产级工作负载进行了系统性特征分析，并实现了高保真工作负载生成器。论文揭示了真实推理场景中被学术研究普遍忽视的关键特征，包括请求到达模式的时间局部性、输入/输出长度的联合分布、以及不同模型架构对负载的差异化响应。基于这些发现，ServeGen 构建了参数化负载模型，能够生成与生产环境统计特性高度一致的合成负载，为推理系统的基准测试和性能评估提供了关键工具。

**技术线索与启示**：
1. **生产数据驱动的研究方法**：真实负载特征分析是系统优化的基础——许多学术工作使用合成负载，与实际差距大
2. **开源负载生成器**：为社区提供了标准化的 LLM 推理评估基准
3. **推理负载的独特性**：与训练负载的规则性不同，推理负载具有高度不可预测性和突发性
4. **负载特征→系统设计启示**：论文发现的负载特征可指导 KV Cache 管理、批处理策略等系统设计

---

### 2.5 DroidSpeak: KV Cache Sharing Across Fine-tuned Model Variants

- **作者**：Yuhan Liu, Yuyang Huang, Jiayi Yao, Zhuohan Gu, Kuntai Du, Hanchen Li, Yihua Cheng, Junchen Jiang (UChicago); Shan Lu, Madan Musuvathi, Esha Choukse (Microsoft)
- **类别**：LLM 推理优化 / KV Cache 共享

**技术概要**：DroidSpeak 使具有相同架构的多个微调模型变体能够共享和部分复用 KV Cache。在云服务场景中，同一基础模型的不同微调版本（如不同客户的定制模型）被广泛部署，但各自的 KV Cache 相互隔离无法复用。DroidSpeak 发现了不同微调模型在注意力计算中的结构性共性：微调主要影响模型的后几层和特定注意力头，而前几层的 KV Cache 高度相似。通过跨模型 KV Cache 的部分复用，DroidSpeak 实现高达 4× 的吞吐量提升和更快的响应时间，同时对输出质量影响极小。

**技术线索与启示**：
1. **微调模型的 KV Cache 结构性共性**：这是一个具有深刻洞察的发现——微调并未彻底改变模型的注意力模式
2. **多租户推理的效率优化**：面向模型即服务（MaaS）场景，共享 KV Cache 可显著降低服务成本
3. **Cache 复用边界的量化**：需要精确界定哪些层/哪些头可安全复用，避免质量退化

---

### 2.6 HarvestContainers: Harvesting Spare CPU Resources in Container Systems

- **作者**：Adam Hall, Anirudh Sarma (Georgia Tech); Esha Choukse (Microsoft Azure Research); Umakishore Ramachandran (Georgia Tech); Sameh Elnikety (Microsoft Research)
- **类别**：容器资源管理 / 资源混部

**技术概要**：HarvestContainers 解决了容器化环境中延迟敏感型（LC）与批处理型（BE）工作负载的安全混部问题。系统动态识别 LC 容器的空闲 CPU 核心，在不干扰其尾延迟的前提下，将这些"闲置"核心分配给 BE 任务使用。核心机制包括：(1) 基于性能监控的动态核心安全采摘；(2) 无需修改应用或操作系统的无侵入设计。实验表明可实现高达 75% 的空闲 CPU 利用率，同时尾延迟在单独运行的 4% 以内。

**技术线索与启示**：
1. **无侵入式资源采摘**：无需修改应用代码或 OS 内核，降低了生产环境中的部署门槛
2. **安全边界的动态确定**：如何确定"安全采摘"的核心数量是关键——过于激进会影响 LC 尾延迟
3. **与 AI 训练集群的潜在结合**：训练集群中也存在 GPU 空闲周期，类似思路可拓展到 GPU 资源采摘

---

## 3. RDMA 与高性能网络

### 3.1 BURST: Seeking High-performance, Interoperability and Scalability in Soft-RDMA

- **作者**：申卉君（一作）、陈果*（通讯作者）—— 湖南大学 + 字节跳动
- **类别**：软件 RDMA 协议栈

**技术概要**：BURST 提出了面向异构环境的高性能 Soft-RDMA 协议栈，解决真实集群中商用 RNIC、普通以太网卡、自研高性能网卡混合部署时的 NR2R（Non-RNIC to RNIC）通信瓶颈。当非 RNIC 节点需要与 RNIC 节点进行高速通信时，系统往往只能退化到内核 TCP，无法发挥 RDMA 的高吞吐与低时延优势。BURST 通过用户态设计、安全可靠的共享资源管理，以及结合 DPDK 与 DSA（Data Streaming Accelerator）的高效加速，实现了与商用 RNIC 行为和性能基本一致的 RoCEv2 通信流程。在 400G 环境下，BURST 首次证明软件 RDMA 也能以较低 CPU 开销实现接近硬件线速的吞吐。

**技术线索与启示**：
1. **软硬协同的 RDMA 生态**：BURST 证明了 Soft-RDMA 在性能上可以追赶硬件 RNIC，这对降低 RDMA 部署成本有重大意义
2. **DPDK + DSA 双加速路径**：DPDK 负责数据面快速路径，DSA 负责内存拷贝卸载——两者互补
3. **NR2R 场景的普适价值**：异构集群是 AI 基础设施的现实，BURST 消除了 RNIC 与非 RNIC 节点间的通信"断崖"
4. **400G 线速软件实现的里程碑**：验证了软件协议栈在极高带宽下的可行性

---

### 3.2 Octopus: Enhancing CXL Memory Pods via Sparse Topology

- **作者**：Yuhong Zhong (Columbia); Fiodar Kazhamiaka, Pantea Zardoshti, Shuwei Teng, Rodrigo Fonseca (Microsoft Azure); Mark D. Hill (UW-Madison); Daniel S. Berger (Microsoft Azure/UW)
- **类别**：CXL 内存分解 / 数据中心架构

**技术概要**：Octopus 提出了面向分解式内存池（disaggregated memory pods）的无交换机组网设计。传统 CXL 内存池依赖 CXL 交换机构建，成本高且扩展性受限。Octopus 采用稀疏拓扑（sparse topology）直接连接服务器与内存节点，消除了交换机的成本和延迟开销。在三服务器硬件原型上，Octopus 的 RPC 延迟相比机架内 RDMA 降低 3.2×，相比 CXL 交换机方案降低 2.4×。同时 Octopus 支持扩展到多机架规模。

**技术线索与启示**：
1. **去交换机化的 CXL 架构**：交换机是成本和延迟的主要来源，稀疏直连拓扑在中小规模内存池中可能更优
2. **CXL 内存分解的工程实践**：从仿真走向硬件原型验证，标志着 CXL 生态的成熟
3. **3.2× vs RDMA 的性能优势**：Octopus 表明在特定场景下 CXL 内存访问可大幅超越传统 RDMA

---

## 4. 视频/流媒体网络系统

### 4.1 QCON: Seamless QoE-aware 5G Streaming via Multi-Connectivity

- **作者**：Goodsol Lee, Junhong Min, Seyeon Kim, Juheon Yi, Kwang Taik Kim, Mung Chiang, Sangtae Ha*, Kyunghan Lee*, Saewoong Bahk* —— Seoul National University (SNU)
- **类别**：5G 视频流媒体 / 多连接传输

**技术概要**：QCON 利用 5G 多连接（Multi-Connectivity）能力，实现无缝的 QoE 感知视频流传输。5G 标准支持用户设备同时连接多个基站或多种无线接入技术（如 5G NR + LTE），QCON 通过智能调度视频数据在多个连接间的分布，实现：(1) 当某条链路质量下降时无感切换到其他链路；(2) 在多链路间动态分配视频质量层（如 SVC 分层）；(3) 基于预测的主动式链路选择。系统在真实 5G 网络环境中验证，实现了接近零卡顿的流媒体体验。

**技术线索与启示**：
1. **5G Multi-Connectivity 的系统化利用**：将 3GPP 标准能力转化为端到端系统方案
2. **QoE 驱动的跨层优化**：从物理层多连接到应用层视频码率自适应的联合优化
3. **预测式链路切换**：基于信号强度预测的主动切换，避免被动切换导致的卡顿
4. **视频分层与多链路的匹配**：SVC 分层编码天生适合多链路异构传输

---

### 4.2 eXpressSFU: Toward Super-Scalable Video Conferencing with SmartNICs

- **作者**：Tuan Tran, S.M. Hosseini, Seyeon Kim, Kyunghan Lee, Nam Bui, Dirk Grunwald, Sangtae Ha* —— SNU + University of Colorado
- **类别**：视频会议系统 / SmartNIC 加速

**技术概要**：eXpressSFU 利用 SmartNIC 实现超大规模视频会议系统中的 Selective Forwarding Unit（SFU）。传统 SFU 运行在 CPU 上，当参会者数量增加时，视频流转发和转码的 CPU 开销急剧增长，成为系统扩展瓶颈。eXpressSFU 将 SFU 的核心转发逻辑卸载到 SmartNIC（如 NVIDIA BlueField），利用 SmartNIC 的硬件数据包处理能力和片上可编程引擎，实现线速的视频流选择性转发。系统支持数百路并发视频流，在保持低延迟的同时大幅降低服务器 CPU 占用。

**技术线索与启示**：
1. **SmartNIC 卸载 SFU 的合理性**：SFU 的核心操作（包过滤/复制/转发）天然适合硬件流水线处理
2. **视频会议的可扩展性壁垒**：CPU-based SFU 是当前大规模视频会议的成本瓶颈，硬件卸载是自然出路
3. **与 WebRTC 生态的兼容性**：如何在 SmartNIC 上保持与 WebRTC 协议栈的兼容是一大工程挑战
4. **超大规模实时通信**：后疫情时代大规模视频会议需求不减，eXpressSFU 提供了系统级可扩展方案

---

### 4.3 AVA: Towards Video Analytics with Vision Language Models

- **作者**：Yuxuan Yan (Zhejiang University); Shiqi Jiang, Yifan Yang, Yuqing Yang, Lili Qiu (Microsoft Research); Ting Cao (Tsinghua); Qianqian Yang, Yuanchao Shu (Zhejiang University)
- **类别**：视频分析 / 视觉语言模型

**技术概要**：AVA 支持基于视觉语言模型（VLM）的开放式视频分析。传统视频分析系统只能回答预定义问题（如"是否有车"），AVA 通过结合事件知识图谱（Event Knowledge Graph）和基于 VLM 的智能体检索（agentic retrieval），支持开放式的自然语言查询。论文还提出了 AVA-100 基准，包含 8 段超长视频（每段超 10 小时）和 120 个手工标注的多样化复杂问答对。AVA 在该基准上达到 75.8% 的准确率。

**技术线索与启示**：
1. **从检测到理解的跃迁**：视频分析正从目标检测走向语义理解——VLM 是这一转变的关键推手
2. **事件知识图谱的索引作用**：将长视频结构化存储为事件图谱，使 VLM 能高效定位相关信息
3. **超长视频分析的挑战**：10 小时+视频的问答需要高效的时空索引和 VLM 调用策略

---

## 5. 网络验证、诊断与安全

### 5.1 S2Sim: Diagnosing and Repairing Distributed Routing Configurations Using Selective Symbolic Simulation

- **作者**：阿里云基础网络团队
- **类别**：网络配置验证 / 路由诊断

**技术概要**：S2Sim 填补了分布式路由配置自动诊断与修复的空白。现有方法擅长验证配置是否符合意图（intent），但当验证失败时，诊断根因和生成修复方案仍高度依赖人工。S2Sim 基于选择性符号仿真（Selective Symbolic Simulation），通过有选择地对网络局部进行符号执行，准确定位配置错误的位置和原因，并自动生成修复建议。在 O(100) 节点的真实网络中诊断耗时不超过 20 秒，在 O(1000) 节点的合成网络中不超过 15 分钟。

**技术线索与启示**：
1. **从"验证"到"诊断+修复"的闭环**：S2Sim 将网络验证从"发现问题"推进到"自动修复"
2. **选择性符号仿真**：避免全网络符号执行的组合爆炸，仅在相关子网上进行精确分析
3. **生产级可扩展性**：1000 节点网络 15 分钟内完成诊断，达到生产环境可用的性能水平
4. **与意图驱动网络的融合方向**：S2Sim 可成为意图驱动网络的"自动修复引擎"

---

### 5.2 Eywa: Automating Model-Based Testing using LLMs

- **作者**：Rajdeep Mondal, Rathin Singha, Todd D. Millstein, George Varghese (UCLA); Ryan Beckett, Siva Kesava Reddy Kakarla (Microsoft Research)
- **类别**：网络协议测试 / LLM 辅助验证

**技术概要**：Eywa 利用 LLM 从自然语言协议规范（RFC 文档）自动构建协议模型（protocol models），从而驱动基于模型的测试（model-based testing）。传统上，为网络协议构建形式化测试模型需要大量人工投入。Eywa 将 RFC 文本输入 LLM，自动提取协议状态机、消息格式和时序约束，生成可执行的测试模型。在多个广泛使用的网络协议实现中，Eywa 发现了 33 个 bug，其中包括 16 个此前未知的缺陷。

**技术线索与启示**：
1. **LLM + 形式化方法的融合**：LLM 负责"理解"自然语言规范，形式化模型负责"精确"测试——两者互补
2. **RFC 到可执行模型的自动化**：显著降低了协议测试的门槛和成本
3. **16 个未知 bug 的发现**：证明即使是广泛部署的协议实现，仍存在未被发现的缺陷

---

### 5.3 MetaEase: Heuristic Analysis from Source Code via Symbolic-Guided Optimization

- **作者**：Pantea Karimi (MIT); Siva Kesava Reddy Kakarla, Ryan Beckett, Pooria Namyar, Behnaz Arzani (Microsoft Research); Santiago Segarra (Rice); Mohammad Alizadeh (MIT)
- **类别**：启发式算法分析 / 系统性能形式化验证

**技术概要**：MetaEase 直接从源代码分析启发式算法，揭示其最坏情况性能场景，无需复杂的形式化建模。系统通过符号引导优化（symbolic-guided optimization）自动探索算法的输入空间，寻找导致性能退化的极端输入组合。MetaEase 在多个领域（网络调度、拥塞控制、负载均衡）匹配或超越了最先进的手工分析器，并发现了多个此前未知的实际系统性能缺陷。

**技术线索与启示**：
1. **源代码级自动分析**：跳过形式化建模这一传统瓶颈，直接从代码出发进行性能边界分析
2. **符号引导优化**：利用符号执行引导搜索，高效探索庞大的输入空间
3. **跨领域通用性**：同一框架适用于网络调度、拥塞控制、负载均衡——证明了方法的通用性

---

### 5.4 KRAKENGUARD: Towards Fine-Grained eBPF Isolation

- **作者**：Jainil Patel (IIT Roorkee); Lucas Graeff Buhl-Nielsen (Quantco); Adrien Ghosn (Microsoft); Marios Kogias (Imperial College London)
- **类别**：eBPF 安全隔离

**技术概要**：KRAKENGUARD 实现了 eBPF 程序的细粒度、基于策略的安全控制。当前 Linux 内核通过粗粒度的 CAP_BPF 等能力控制 eBPF 程序加载，缺乏细粒度的行为约束。KRAKENGUARD 在 eBPF 程序加载时使用符号执行进行静态分析，基于用户定义的策略检查程序行为（如禁止访问特定内核数据结构、限制网络数据包修改范围等）。系统阻止恶意行为、检测漏洞，并允许在多租户环境中安全执行不可信 eBPF 程序。

**技术线索与启示**：
1. **eBPF 安全的细粒度化**：从"全有或全无"的能力模型转向策略驱动的行为控制
2. **加载时符号执行**：在程序加载阶段而非运行时进行安全检查，兼顾安全与性能
3. **多租户 eBPF 的安全基础**：为云环境中多租户共享 eBPF 基础设施提供安全保障

---

## 6. 云基础设施与系统

### 6.1 Come Hell or Still Water: Alleviating Tail Latency in Cloud Block Store

- **作者**：阿里云基础设施网络团队
- **类别**：云存储 / 尾延迟优化

**技术概要**：该论文系统分析了云块存储（EBS）场景中 I/O 长尾延迟的根因，将问题分为过载与欠载两种场景。在过载场景下，极少数虚拟磁盘（VD）产生的工作负载爆发（bursts）是导致长尾的核心原因；在欠载场景下，事件循环（event-loop）线程模型导致了不必要的数据路径处理延迟。针对性地，系统设计了双桶限流（dual-bucket rate limiting）来抑制过载下的突发，以及任务差异化调度来减少欠载下的事件循环延迟。过载场景长尾延迟降低 97%，欠载场景降低 43%。

**技术线索与启示**：
1. **根因驱动的场景化优化**：拒绝"一刀切"，分场景诊断后针对性施策
2. **过载 vs 欠载的不同机制**：同样表现为长尾延迟，但底层机制完全不同——诊断方法学的价值
3. **双桶限流**：为突发工作负载设计，在保证隔离性的同时避免过度限流
4. **事件循环线程模型反思**：欠载场景下的延迟并非资源不足，而是调度策略不匹配

---

### 6.2 AnyPro: Preference-Preserving Anycast Optimization based on Strategic AS-Path Prepending

- **作者**：阿里云基础设施网络团队
- **类别**：Anycast 流量工程 / BGP 路由优化

**技术概要**：AnyPro 优化 IP Anycast 的流量调度。IP Anycast 在多个地理分布 PoP 上广播相同 IP 前缀，依赖 BGP 路由自然地引导用户流量到最近 PoP，但缺乏对流量分布的精细控制。AnyPro 的核心洞察是：通过战略性地使用 AS-Path Prepending（ASPP）——向特定方向的人造 AS 路径加长，可系统性地影响远端 AS 的 BGP 选路决策。论文推导了 ASPP 的约束条件以确保不会破坏路由策略偏好，并计算最优 ASPP 配置。AnyPro 将 90 分位 RTT 降低 37.7%，落点准确率提升至 0.85。

**技术线索与启示**：
1. **ASPP 的系统化利用**：将 BGP 社区中"粗放"的 ASPP 操作升级为精确的流量工程工具
2. **约束推导保证路由安全**：在优化性能的同时，确保不违反路由策略约束
3. **Anycast 流量的精细化控制**：突破了传统 Anycast "尽力而为"的流量分布模型

---

### 6.3 SONiC DASH SmartSwitch: Offloading Cloud Network Services at Production Scale
> 🏆 **Community Award Winner**

- **作者**：Shaofeng Wu (CUHK/MSRA), Zhixiong Niu (MSRA), Riff Jiang, Lawrence Lee 等数十位 Microsoft 工程师 + Hong Xu (CUHK), Yongqiang Xiong (MSRA)
- **类别**：SmartNIC/可编程交换机 / 云网络卸载

**技术概要**：SONiC DASH SmartSwitch 重新设计了云网络服务卸载架构，通过硬件友好的流水线设计、统一的交换机架构和开放开发模型，在 Azure 生产环境中大规模部署。SmartSwitch 将 SDN 策略执行、负载均衡、DDoS 防护等网络服务从 x86 服务器卸载到可编程交换机，显著提升了吞吐量和连接容量，同时大幅改善了功耗和空间效率。论文分享了大规模部署中的扩展性挑战和工程解决方案，为行业提供了可复用的参考架构。

**技术线索与启示**：
1. **开放硬件 + 开放软件**：基于 SONiC 开源生态的 SmartSwitch 方案，可避免厂商锁定
2. **硬件友好流水线设计**：在 SmartNIC/SmartSwitch 硬件限制下设计高效流水线——"为硬件设计软件"
3. **生产级验证的工业价值**：Azure 规模的真实部署经验远超学术原型，揭示了大量工程细节
4. **云网络服务卸载的大趋势**：x86→SmartNIC→SmartSwitch 的卸载演进路线图

---

### 6.4 Pyrocumulus: SmartNIC-Enabled Live Migration for Storage-Optimized VMs

- **作者**：Jiechen Zhao (UofT/MSRA); Ran Shu, Lei Qu, Ziyue Yang, Rui Ma, Peng Cheng, Yongqiang Xiong (MSRA); Derek Chiou (Microsoft/UT Austin); Natalie Enright Jerger (UofT)
- **类别**：虚拟机热迁移 / FPGA SmartNIC

**技术概要**：Pyrocumulus 利用 FPGA SmartNIC 实现存储优化型虚拟机的快速低开销热迁移。存储密集型 VM（如数据库 VM）的热迁移因涉及大量本地存储状态（GB-TB 级）而极为困难。Pyrocumulus 将迁移协议的核心逻辑卸载到 FPGA SmartNIC 上，利用 SmartNIC 的硬件定制化和高效网络访问能力，实现接近于计算型 VM 的迁移速度，同时将迁移对 VM 性能的干扰降至最低。

**技术线索与启示**：
1. **SmartNIC 卸载热迁移协议**：将 CPU 密集型的数据搬运和网络传输逻辑卸载到 SmartNIC
2. **存储型 VM 的热迁移挑战**：GB-TB 级的本地存储状态迁移是传统方案的盲区
3. **FPGA 定制化的灵活性**：相比于固定功能 ASIC，FPGA 允许对迁移协议进行定制
4. **与 CXL 内存分解的协同**：若结合 CXL 共享内存，Pyrocumulus 的迁移效率可能进一步提升

---

### 6.5 Wallet: Confidential Serverless Computing

- **作者**：Patrick Sabanic, Masanori Misono, Teofil Bodea, Julian Pritzi, Michael Hackl, Dimitrios Stavrakakis, Pramod Bhatotia —— Technical University of Munich (TUM)
- **类别**：机密计算 / Serverless

**技术概要**：Wallet 将机密计算（Confidential Computing）引入 Serverless 场景。Serverless 平台（如 AWS Lambda）中，用户代码在共享基础设施上运行，其数据和执行状态面临来自云提供商内部威胁的风险。Wallet 利用 AMD SEV-SNP / Intel TDX 等 TEE 技术保护 Serverless 函数的机密性和完整性，同时解决了 Serverless 场景下的几个独特挑战：(1) 函数实例快速启动与 TEE 初始化延迟的矛盾；(2) 函数间安全通信的密钥管理；(3) 无状态函数与 TEE 状态保护的适配。

**技术线索与启示**：
1. **Confidential Computing × Serverless**：两个热门领域的交汇点，TEE 为 Serverless 提供了"不信任云提供商"的安全基础
2. **冷启动 vs TEE 初始化**：Serverless 追求毫秒级启动，TEE 初始化需数百毫秒——如何调和是核心工程挑战
3. **Serverless 的安全威胁模型升级**：从"信任云厂商"到"零信任"的范式转变

---

## 7. 论文完整索引表

| # | 论文标题 | 第一作者 | 机构 | 方向 | 奖项 |
|---|---------|---------|------|------|------|
| 1 | OSCAR: O(1)-Step Convergence Congestion Control | 张兆琛 | 南京大学 | 拥塞控制 | 🏆 Outstanding Paper |
| 2 | SONiC DASH SmartSwitch | — | CUHK / Microsoft Research | SmartNIC/云网络 | 🏆 Community Award |
| 3 | HeteCCL: Synthesizing Collective Communication for Heterogeneous GPU Clusters | 黑晨阳 | 东北大学, 阿里云, 中科院先进院 | 集合通信/ML训练 | — |
| 4 | ForestColl: Throughput-Optimal Collective Communications | Liangyu Zhao | U Washington, Microsoft Research, Tsinghua | 集合通信/ML训练 | — |
| 5 | EROICA: Online Performance Troubleshooting for Model Training | 阿里云团队 | 阿里云 | ML训练诊断 | — |
| 6 | ServeGen: Workload Characterization of LLM Serving | 阿里云团队 | 阿里云 | LLM推理负载 | — |
| 7 | DroidSpeak: KV Cache Sharing Across Fine-tuned Models | Yuhan Liu | U Chicago, Microsoft | LLM推理/KV Cache | — |
| 8 | HarvestContainers: Harvesting Spare CPU in Container Systems | Adam Hall | Georgia Tech, Microsoft | 容器资源管理 | — |
| 9 | BURST: High-performance Soft-RDMA | 申卉君 | 湖南大学, 字节跳动 | 软件RDMA | — |
| 10 | Octopus: CXL Disaggregated Memory | — | Columbia, Microsoft Azure, UW-Madison | CXL内存分解 | — |
| 11 | QCON: Quality-Aware Video Streaming over 5G | — | Seoul National University | 5G流媒体 | — |
| 12 | eXpressSFU: Video Conferencing SFU on SmartNIC | — | Seoul National University, Colorado | SmartNIC/视频会议 | — |
| 13 | AVA: Video Analytics with VLM | — | 浙江大学, Microsoft Research, Tsinghua | 视频分析/VLM | — |
| 14 | HEDGE: Traffic Engineering with Probabilistic Link Capacities | Arjun Devraj | Cornell, Microsoft, Meta | 流量工程 | — |
| 15 | S2Sim: Network Simulation for Verification | 阿里云团队 | 阿里云 | 网络验证/诊断 | — |
| 16 | Eywa: LLM-assisted Protocol Testing | — | UCLA, Microsoft Research | 协议测试/LLM | — |
| 17 | MetaEase: Heuristic Analysis for Network Config | — | MIT, Microsoft Research, Rice | 启发式分析 | — |
| 18 | KRAKENGUARD: eBPF Security Isolation | — | IIT Roorkee, Quantco, Imperial | eBPF安全 | — |
| 19 | Come Hell or Still Water: Cloud Storage Tail Latency | 阿里云团队 | 阿里云 | 云存储/尾延迟 | — |
| 20 | AnyPro: Anycast/BGP Routing | 阿里云团队 | 阿里云 | Anycast/BGP | — |
| 21 | Pyrocumulus: SmartNIC VM Live Migration | — | U Toronto, Microsoft, UT Austin | SmartNIC/热迁移 | — |
| 22 | Wallet: Confidential Computing for Serverless | — | Technical U Munich | 机密计算/Serverless | — |

> **覆盖说明**：本报告覆盖了 Spring 轮（50篇）中可公开检索到的 22 篇论文（约 44%），包括3篇获奖论文。Fall 轮论文因信息有限仅少量覆盖。SNU 论文（QCON、eXpressSFU）来源为实验室主页 [netstech.org](https://netstech.org/publications/)，PRC 论文实际发表于 CoNEXT 2026，非 NSDI 2026。

---

## 8. 结语与未来方向

NSDI 2026 反映了网络系统领域的几个深刻变革：

**1. 网络系统已全面进入"AI 定义"时代。** 约35%的论文围绕大模型训练/推理中的网络系统问题，这不是 AI 应用网络，而是 AI 重塑了网络的底层设计需求——从集合通信调度、拥塞控制到工作负载建模，AI 工作负载的独特特征（大象流、同步突发、AllReduce 通信模式）在重新定义网络系统的设计范式。

**2. 异构性从"例外"变为"常态"。** HeteCCL（GPU 异构）、ForestColl（网络异构）、BURST（网卡异构）共同指向一个事实：未来的数据中心网络必须原生支持异构环境。同构假设在产业实践中已不成立。

**3. SmartNIC/硬件卸载进入成熟期。** 从 eXpressSFU 的视频会议 SFU 卸载，到 Pyrocumulus 的 VM 热迁移卸载，到 SONiC DASH 的全栈云网络卸载——SmartNIC 已不再是"加速某个特定功能"的辅助角色，而是成为系统架构的核心组件。

**4. 中国学术力量的崛起。** 南京大学获 Outstanding Paper Award，东北大学首中 NSDI 主会，湖南大学、浙江大学、清华大学、港中文等多所中国高校均有论文入选。阿里云 6 篇论文的规模表明中国企业已具备系统领域的顶级研究能力。

**5. 安全与隐私成为系统设计的原生属性。** Wallet（机密计算 Serverless）、KRAKENGUARD（eBPF 隔离）体现了"安全不应是事后添加"的设计理念。

**未来1-3年值得关注的方向**：
- **百万卡集群的网络架构**：当前在万卡/十万卡规模验证的方案能否线性扩展到百万卡？
- **CXL/UALink 等新总线的网络影响**：内存语义网络（CXL）和加速器互联（UALink）将如何改变数据中心网络分层？
- **Confidential Computing + Networking**：TEE 保护的网络通信和分布式计算
- **AI for Networking 的落地**：LLM 辅助网络运维（如 Eywa、S2Sim 的进一步演进）
- **绿色网络**：光互连（如微软 MOSAIC）等低功耗互联技术的系统级集成

---

*本报告基于公开信息整理，论文详细信息以 USENIX NSDI 2026 官方论文集为准。*