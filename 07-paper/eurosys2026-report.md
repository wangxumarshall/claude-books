# EuroSys 2026 论文综合报告

## 会议概况

- **会议**：21st European Conference on Computer Systems (EuroSys 2026)
- **地点**：Edinburgh, Scotland, UK
- **时间**：2026年4月27-30日
- **录用率**：Spring Cycle 79/404 = 19.6%, Fall Cycle 59/319 ≈ 18.5%, 合计约138篇
- **本报告覆盖**：Spring+Fall双周期约131篇论文
- **报告日期**：2026年6月

---

## 趋势概览

1. **AI系统主导**：LLM训练+推理+应用共计约30篇，占比近38%，AI系统已成为系统研究的第一大主题
2. **Serverless持续升温**：Serverless计算、资源管理、成本优化相关论文达10篇，反映云原生架构的深入演进
3. **网络与通信创新**：RDMA、负载均衡、拥塞控制等方向论文10篇，体现AI时代数据中心网络的变革需求
4. **安全与可信执行**：TEE保护LLM、安全容器、形式化验证等方向成为新焦点
5. **异构计算与硬件协同**：FPGA、DPU、SmartNIC、跨ISA二进制翻译等方向活跃

---

# Part 1: LLM Training

> 本部分涵盖16篇论文，涉及MoE训练优化、LoRA微调加速、数据管道扩展、训练调度与并行策略、运行时性能建模、多模态训练系统、训练容错以及RL后训练。

---

## 1.1 MegaScale-MoE: Large-Scale Communication-Efficient Training of Mixture-of-Experts Models in Production

**作者**：Chao Jin, Ziheng Jiang, Zhihao Bai, Zheng Zhong, Juncai Liu, Xiang Li, Ningxin Zheng, Xi Wang, Cong Xie, Qi Huang, Wen Heng, Yiyuan Ma, Wenlei Bao, Size Zheng, Yanghua Peng, Haibin Lin, Xuanzhe Liu, Xin Jin, Xin Liu
**单位**：Peking University, ByteDance Seed
**发表信息**：EuroSys 2026, arXiv:2505.11432

### 技术概要

Mixture-of-Experts（MoE）架构是当前扩展大语言模型（LLM）规模最有前景的路径之一——通过稀疏激活的专家路由机制，在保持推理计算量可控的同时将模型参数量推至数百亿乃至万亿级别。然而，MoE训练面临严峻的通信瓶颈：每个MoE层中的专家路由操作产生大量all-to-all通信（token需要在不同GPU间按专家分配进行交换），随着模型规模增长和硬件代际演进（如从A100到H100通信-计算比恶化），现有基于Megatron-LM等框架的MoE训练系统效率持续退化。具体而言，现有方案存在三个关键不足：(1) 对MoE层中的attention子层和FFN/Expert子层采用统一的并行策略，忽视了二者截然不同的通信模式——attention需要序列维度的all-reduce，而Expert需要token维度的all-to-all；(2) 通信与计算的重叠仅停留在算子间粗粒度层面，未能充分利用MoE层内部的细粒度重叠机会；(3) 通信数据始终以高精度（FP16/BF16）传输，忽视了通信场景对精度的容忍度高于计算场景这一特性。

MegaScale-MoE是面向生产环境的大规模MoE训练系统，通过三项关键通信优化设计系统性解决上述瓶颈。第一，**定制化通信高效并行策略**：针对MoE层中attention和FFN子层的不同通信特征，分别设计最优的数据并行和张量并行组合——attention子层采用序列并行减少all-reduce通信量，FFN/Expert子层采用专家并行优化all-to-all通信模式，从源头降低总通信量。第二，**多层次通信-计算重叠调度**：采用整体性（holistic）调度策略，在算子间层面（如将Expert通信与下一层的attention计算重叠）和算子内层面（如将all-to-all的分块传输与expert计算流水线化）同时挖掘重叠机会，系统性隐藏通信延迟。第三，**低精度通信压缩**：将通信数据从BF16降至FP8精度，同时调整通信模式（如改变all-to-all的数据排布）以适配低精度传输的要求，在不损失模型训练质量的前提下将通信数据量减半。在1,440块NVIDIA Hopper GPU上训练352B参数的MoE模型时，MegaScale-MoE达到1.41M tokens/s的训练吞吐量，相比Megatron-LM基线实现1.88倍效率提升，展示了通信优化在MoE训练中的决定性作用。

### 技术线索与启示

- **系统软件方向**：通信-计算重叠的多层次调度框架可泛化到其他集合通信密集场景，如分布式推理中的KV Cache传输和跨节点模型并行
- **硬件-软件协同设计**：FP8通信压缩验证了"有损通信+无损计算"范式的可行性——通信链路对精度的容忍度高于计算链路，这一洞察值得在所有分布式训练框架中推广
- **开放性问题与未来方向**：MoE模型规模持续增长（从百亿到万亿参数），all-to-all通信瓶颈将更加突出，需要探索新的网络拓扑（如rail-optimized）和通信原语（如hierarchical all-to-all）设计

> **信息来源**：arXiv:2505.11432 摘要

---

## 1.2 LoRAFusion: Efficient LoRA Fine-Tuning for LLMs

**作者**：Zhanda Zhu, Qidong Su, Yaoyao Ding, Kevin Song, Shang Wang, Gennady Pekhimenko
**单位**：University of Toronto, Vector Institute, NVIDIA
**发表信息**：EuroSys 2026, arXiv:2510.00206

### 技术概要

Low-Rank Adaptation（LoRA）已成为大语言模型（LLM）参数高效微调（PEFT）的主流方法，通过在冻结的预训练权重旁添加低秩矩阵，将可训练参数量降低数个数量级，同时保持与全量微调相当的模型质量。然而，现有LoRA微调系统存在两个关键的工程低效。第一，**内存访问冗余**：LoRA的计算流程涉及将输入激活张量与低秩矩阵相乘后再加回主路径，现有实现（如HuggingFace PEFT）在大激活张量上执行多次不必要的内存读写（如分离的矩阵乘法中间结果写回内存再读出），这些内存受限操作的开销在GPU算力持续提升的背景下日益突出。第二，**多任务并发机会错失**：在实际生产场景中（如多租户AI服务），多个独立的LoRA适配器常共享同一基座模型，但现有系统将它们串行执行，未能利用并发微调带来的通信重叠、流水线气泡减少和GPU负载均衡等性能收益。

LoRAFusion从内核和调度两个层面系统性解决上述问题。在内核层面，提出**图分裂（graph-splitting）方法**：将LoRA计算图中的内存受限操作（如LayerNorm、残差加法）与计算密集的GEMM操作分离，对前者进行融合以消除冗余内存访问，同时保持GEMM的高算力利用率——无需重计算或同步开销即可提升整体内核性能。在调度层面，引入**自适应批处理算法**用于多任务微调：先将LoRA适配器智能分组以交错执行batch（减少流水线气泡），再在每个分组内求解装箱问题生成依赖感知的均衡微批次（确保各适配器的训练进度平衡）。此外，LoRAFusion的融合内核可作为即插即用组件直接替换现有LoRA系统（如HuggingFace PEFT）中的对应模块。实验表明，系统相比Megatron-LM实现最高1.96倍（平均1.47倍）端到端加速，融合内核单独相比现有实现提升最高1.39倍（平均1.27倍），已开源。

### 技术线索与启示

- **系统软件方向**：图分裂算子融合方法可作为通用的kernel fusion策略，适用于其他存在内存受限操作的深度学习框架（如Transformer推理中的KV Cache管理）
- **Agent与LLM应用方向**：多LoRA并发微调对于Agent多任务适配场景具有直接工程价值——如同一基座模型服务多个Agent时，可并发微调各Agent的专属LoRA适配器
- **性能工程与可观测性**：将批处理调度建模为装箱问题的方法可推广到其他多任务共享GPU的场景，如多租户推理服务的请求调度

> **信息来源**：arXiv:2510.00206 摘要

---

## 1.3 Federated Fine-Tuning of Sparsely-Activated Large Language Models on Resource-Constrained Devices

**作者**：Fahao Chen, Jie Wan, Peng Li, Zhou Su, Dongxiao Yu
**单位**：Shandong University, Xi'an Jiaotong University
**发表信息**：EuroSys 2026, arXiv:2508.19078

### 技术概要

联邦学习（Federated Learning）允许多个参与方在不共享原始数据的前提下协作训练模型，是解决数据隐私和合规性问题的关键技术。当联邦学习的目标模型从传统的CNN/RNN升级到基于MoE架构的大语言模型（LLM）时，面临根本性矛盾：MoE-LLM的参数量可达数十亿甚至数百亿，单个参与方的计算资源（如消费级GPU）无法承载完整的微调过程。现有三类尝试方案均存在显著不足：(1) **模型量化**方案通过降低精度减少资源需求，但量化误差在联邦聚合中累积导致模型质量严重退化；(2) **计算卸载**方案将超出本地能力的计算卸载到云端，但引入巨大的通信开销和延迟，且依赖稳定的高带宽连接这一不切实际的假设；(3) **专家剪枝**方案仅微调部分专家以节省资源，但忽视了MoE模型中专家激活模式的动态性和层间差异性，导致微调效果不佳。

FLUX系统专门面向资源受限设备上的MoE-LLM联邦微调，以最小化time-to-accuracy为目标，通过三项创新系统性解决上述问题。第一，**量化感知本地profiling**：在微调前以极低开销（使用量化模型）在本地估计每个专家的激活模式，为后续资源分配决策提供依据——避免了在全精度模型上执行昂贵的profiling。第二，**自适应层感知专家合并**：根据不同层中专家的激活频率和重要性，将不活跃或低重要性的专家合并到相邻专家中，减少需要微调的参数量同时保持模型精度——关键创新在于"层感知"，即不同层采用不同的合并粒度。第三，**基于探索-利用策略的动态专家角色分配**：将专家分为"调优专家"和"冻结专家"两类角色，通过多臂赌博机式的探索-利用策略在训练过程中动态调整角色分配，确保所有专家都有机会被充分调优。在LLaMA-MoE和DeepSeek-MoE两个模型上的多个基准数据集上实验，FLUX实现最高4.75倍time-to-accuracy加速，显著优于现有方法。

### 技术线索与启示

- **边缘计算与端侧部署**：为资源受限设备（如消费级GPU）参与大模型协作训练提供了可行路径，对联邦学习+LLM的工程落地意义重大
- **Agent与LLM应用方向**：动态专家角色分配的探索-利用策略与Agent的tool-selection有结构相似性，可为Agent工具选择算法提供启发
- **开放性问题与未来方向**：MoE联邦微调的安全性和隐私保护仍是开放问题——专家激活模式本身可能泄露训练数据信息

> **信息来源**：arXiv:2508.19078 摘要

---

## 1.4 MegaScale-Data: Scaling DataLoader for Multi-Source Large Foundation Model Training

**作者**：Juntao Zhao, Qi Lu, Wei Jia, Borui Wan, Lei Zuo, Junda Feng, Jianyu Jiang, Yangrui Chen, Shuaishuai Cao, Jialing He, Kaihua Jiang, Yuanzhe Hu, Shibiao Nong, Yanghua Peng, Haibin Lin, Chuan Wu
**单位**：The University of Hong Kong, ByteDance Inc.
**发表信息**：EuroSys 2026, arXiv:2504.09844

### 技术概要

现代大基础模型（LFM）训练依赖数据并行框架中的多个dataloader并行处理不同数据子集。当训练数据来自多个不同源（如网页文本、代码、书籍、多模态数据）时，现有dataloader架构面临两个根本性挑战。第一，**负载失衡**：由于注意力算子的二次计算复杂度，不同样本长度导致不同dataloader的计算量严重不均——包含长文本的loader处理时间远超过短文本loader，整体训练效率受最慢的loader制约。第二，**状态冗余与内存浪费**：支持多数据源需要每个并行loader维护per-dataset文件访问状态（如当前读取位置、已访问文件列表等），这些状态在并行loader间冗余复制，不仅消耗过多CPU内存，还因动态数据混合（如课程学习中动态调整数据源比例）和混合并行（如张量并行组内多个rank重复存储相同状态）而进一步恶化。

MegaScale-Data是面向多源LFM训练的工业级分布式数据加载架构，通过三大创新系统性解决上述问题。第一，**解耦数据预处理**：引入角色特定的actor——Source Loaders负责从各数据源读取和初步处理数据，Data Constructors负责将处理后的数据组装为训练样本——消除了数据源级别和并行级别的冗余访问，确保多源可扩展性。第二，**集中式声明式数据平面**：提供统一的数据编排接口，支持加载时的多源动态混合（如长短上下文混合、多模态数据融合、课程学习中的数据比例调整），无需修改训练代码即可实现复杂的数据编排策略。第三，**多级自动分区与扩缩**：针对不同数据源预处理成本异构的特点（如图像数据增强远慢于文本tokenization），自动将高成本源的更多资源分配给Source Loaders，实现负载均衡。系统还贡献了部署和容错方面的运营经验。实验表明，MegaScale-Data实现最高4.5倍端到端训练吞吐提升和13.5倍CPU内存用量降低。

### 技术线索与启示

- **数据密集型系统**：解耦预处理+声明式数据平面的架构设计对通用ETL管道有重要借鉴意义——数据加载与数据转换的分离是提升可扩展性的关键
- **性能工程与可观测性**：多级自动分区机制可扩展到其他异构计算资源调度场景，如异构GPU集群的任务分配
- **云原生与分布式架构**：声明式数据编排的思想与Kubernetes声明式API一脉相承，可迁移到更多数据管理场景（如流处理管道编排）

> **信息来源**：arXiv:2504.09844 摘要

---

## 1.5 STAlloc: Enhancing Memory Efficiency in Large-Scale Model Training with Spatio-Temporal Planning

**作者**：Zixiao Huang, Junhao Hu, Hao Lin, Chunyang Zhu, Yueran Tang, Quanlu Zhang, Zhen Guo, Zhenhua Li, Shengen Yan, Zhenhua Zhu, Guohao Dai, Yu Wang
**单位**：Tsinghua University, Infinigence-AI, Shanghai Jiao Tong University
**发表信息**：EuroSys 2026, arXiv:2507.16274

### 技术概要

大语言模型（LLM）规模的快速增长使GPU内存压力日益严峻，而虚拟流水线（Virtual Pipeline）、重计算（Recomputation/Gradient Checkpointing）等训练优化技术进一步加剧了这一问题——这些技术通过破坏张量（tensor）的生命周期来节省内存，但副作用是引入严重的内存碎片。流行的深度学习框架如PyTorch使用在线GPU内存分配器（如CUDA caching allocator），这些分配器在运行时贪心地分配内存但完全忽视张量的生命周期信息，导致高达43%的GPU内存被浪费在碎片上，甚至触发本可避免的OOM（Out-of-Memory）错误，使得前述训练优化技术的效果大打折扣。现有内存优化方法（如内存池、紧凑化）要么无法处理动态张量生命周期，要么引入显著的运行时开销，均难以在大模型训练中实用。

STAlloc提出了一种全新的GPU内存分配范式——**离线规划与在线分配的混合架构**，核心洞察在于训练负载的内存分配行为具有高度的时空规律性（spatio-temporal regularity）。在离线阶段，STAlloc通过分析训练计算图中张量的分配模式和生命周期，利用时空规律性生成近最优的内存分配方案（包括每个张量的最优放置位置）；在在线阶段，对于MoE等动态模型（专家路由导致张量数量和大小不确定），STAlloc基于离线规划的指导进行自适应分配。作为可插拔的PyTorch内存分配器，STAlloc无需修改训练代码即可使用。实验表明，在dense模型和MoE模型上，STAlloc平均减少85.1%（最高100%）的内存碎片率，使训练吞吐性能提升最高32.5%，且开销可忽略不计。

### 技术线索与启示

- **系统软件方向**：离线规划+在线分配的混合范式可应用于其他动态资源管理场景（如内存数据库、JIT编译器、容器内存管理）
- **性能工程与可观测性**：揭示了深度学习框架内存管理器的深层问题——43%的内存浪费是令人惊讶的数字，为PyTorch等框架的内存优化提供了工程实践指导
- **硬件-软件协同设计**：GPU内存碎片问题是硬件内存管理单元设计的潜在改进方向，未来GPU硬件可考虑支持更细粒度的内存分配原语

> **信息来源**：arXiv:2507.16274 摘要

---

## 1.6 Zeppelin: Balancing Variable-length Workloads in Data Parallel Large Model Training

**作者**：Chang Chen, Tiancheng Chen, Jiangfei Duan, Qianchao Zhu, Zerui Wang, Qinghao Hu, Peng Sun, Xiuhong Li, Chao Yang, Torsten Hoefler
**单位**：Peking University, ETH Zurich, CUHK, Shanghai AI Lab, MIT
**发表信息**：EuroSys 2026, arXiv:2509.21841

### 技术概要

大语言模型（LLM）训练中的序列长度日益增长且变化大（如长文档、多轮对话、代码生成等场景），在大规模数据并行训练中引发严重的负载不均问题。不同序列长度的样本在计算和通信上的开销差异巨大——注意力算子随序列长度呈二次增长，而线性层仅为线性增长——导致同一batch内的GPU负载严重不均衡。现有框架尝试通过数据重排（将相似长度的序列分到同一batch）或混合并行策略来缓解，但忽视了计算和通信成本随序列长度的变化规律，效果不佳。Zeppelin识别了三个关键挑战：(1) 不同长度序列在分布式注意力中的计算-通信比不同，短序列的通信开销占比远高于长序列；(2) 静态NIC-GPU亲和设置与动态并行负载不匹配，某些NIC可能成为瓶颈而其他NIC闲置；(3) 二次复杂度的注意力模块和线性复杂度的FFN/Linear模块需要完全不同的最优分区策略。

Zeppelin通过三个层次的协同设计解决上述问题。第一，**层次化序列分区+分歧并行策略的注意力引擎**：对attention模块采用层次化的序列分区方法减少通信开销并均衡计算，同时支持高效的注意力引擎在同一算子内对不同部分采用不同的并行策略（如序列并行与张量并行混合）。第二，**路由层**：编排节点间的数据传输以充分利用NIC带宽，动态调整NIC-GPU亲和关系以匹配当前并行负载。第三，**重映射层**：在注意力模块和线性模块之间转换序列布局，确保两者都能在其最优分区策略下高效执行。综合评估显示，Zeppelin在多种配置下平均实现2.80倍加速，显著优于现有SOTA方法。

### 技术线索与启示

- **系统软件方向**：分歧并行策略（对同一算子不同部分采用不同并行方式）是一种可推广的优化范式，适用于其他内部计算特征不均匀的算子
- **性能工程与可观测性**：NIC-GPU亲和的动态调整思路可应用于其他网络密集型分布式系统（如分布式存储、微服务通信）
- **开放性问题与未来方向**：变长序列训练优化远未解决，特别是与动态batch size和多模态数据结合时，问题复杂度进一步提升

> **信息来源**：arXiv:2509.21841 摘要

---

## 1.7 Arena: Efficiently Training Large Models via Dynamic Scheduling and Adaptive Parallelism Co-Design

**作者**：Chunyu Xue, Weihao Cui, Quan Chen, Chen Chen, Han Zhao, Shulai Zhang, Linmei Wang, Yan Li, Limin Xiao, Weifeng Zhang, Jing Yang, Bingsheng He, Minyi Guo
**单位**：Shanghai Jiao Tong University, Lenovo Research, Microsoft, Guizhou University, NUS
**发表信息**：EuroSys 2026, arXiv:2403.16125

### 技术概要

GPU集群中大模型高效训练涉及两个层面的优化：跨任务的动态调度（决定哪些任务在哪些GPU上运行）和任务内的自适应并行（Adaptive Parallelism, AP，动态调整任务的并行策略以适应当前资源）。然而，现有动态调度器主要为静态并行（Static Parallelism, SP）模式设计，在AP执行模式下与调度决策严重失配——调度器基于静态并行配置做决策，但实际执行时AP可能将任务迁移到不同的并行策略，导致调度器的决策不再最优，引发吞吐下降和任务排队延长。此外，AP引入了额外的性能估计复杂性（需要预测不同并行配置下的性能）和搜索空间爆炸（弹性维度×异构维度×并行策略维度的联合优化）。

Arena协同设计动态调度和自适应并行，通过三项关键创新实现高集群效率。第一，**低成本解耦profiling**：将性能数据采集与调度决策解耦，以低开销获取任务在不同配置下的性能特征。第二，**AP定制的性能估计**：为AP执行模式专门设计性能预测模型，准确估计弹性并行配置下的训练吞吐。第三，**网格抽象统一优化空间**：通过网格抽象将调度决策和并行策略的联合优化空间分片，在弹性维度和异构维度上进行动态调度；执行时基于裁剪后的搜索空间进行高效AP配置选择。在异构测试床和生产负载上评估，Arena减少任务完成时间最高49.3%，集群吞吐提升最高1.60倍。

### 技术线索与启示

- **云原生与分布式架构**：解耦profiling+网格抽象的调度方法对通用集群调度系统（如Kubernetes + GPU Operator）有参考价值
- **性能工程与可观测性**：AP-tailored性能估计方法展示了如何在弹性系统中做准确性能预测，这对其他自适应系统也有借鉴意义
- **开放性问题与未来方向**：弹性训练与异构集群的联合优化是持续研究方向，特别是在多租户GPU云环境中

> **信息来源**：arXiv:2403.16125 摘要

---

## 1.8 HARP: Orchestrating Automated Parallel Training on Heterogeneous GPU Clusters

**作者**：Antian Liang, Zhigang Zhao, Kai Zhang, Xuri Shi, Chuantao Li, Chunxiao Wang, Zhenying He, Yinan Jing, X. Sean Wang
**单位**：Fudan University, Shandong Computer Science Center
**发表信息**：EuroSys 2026, arXiv:2509.24859

### 技术概要

GPU架构的快速演进（如从V100到A100到H100到H200）导致训练基础设施的异构性持续增加，许多GPU集群中同时存在多代GPU和不同型号的网络设备。在这种异构环境中高效利用所有可用加速器是分布式模型训练的关键挑战。然而，现有训练框架（如Megatron-LM、DeepSpeed）主要为同构集群设计，在异构加速器和网络上部署时表现出显著的资源利用不足——快速GPU等待慢速GPU、高带宽链路闲置在低带宽链路旁边。具体而言，异构集群面临两个核心问题：(1) 算子间并行策略空间巨大（不同GPU计算能力不同，导致数据并行、张量并行、流水线并行的最优组合完全不同），手工配置不现实；(2) 跨集群互联的网络特征与同集群内网络差异大，传统的1F1B（一个前向一个后向）流水线调度无法充分利用跨集群带宽。

HARP是专为异构集群设计的自动化并行训练框架，包含两个核心组件。第一，**细粒度规划器**：在算子间并行策略的广阔搜索空间中高效探索，综合考虑异构加速器的计算能力差异和网络带宽异构性，寻找既能缓解通信开销又能保持异构加速器负载均衡的近最优并行策略——关键创新在于搜索空间剪枝策略使得规划可以在可接受时间内完成。第二，**异构感知1F1B调度器**：根据网络特征（特别是跨集群互联的带宽和延迟特征）自适应调整微批次的执行时序和排序，最大化跨集群互联下的计算-通信重叠，同时仅引入最小内存开销。评估显示，HARP在异构集群上比现有SOTA训练框架实现1.3×-1.6×的性能提升。

### 技术线索与启示

- **硬件-软件协同设计**：异构感知调度为混合GPU集群（如A100+H100混合部署）的训练部署提供了实践指导，这对当前GPU供应紧张的环境尤为重要
- **系统软件方向**：自动化并行策略搜索可集成到PyTorch FSDP、Megatron-LM等框架中，降低用户在异构集群上配置训练的门榄
- **云原生与分布式架构**：异构集群训练是云环境弹性资源利用的常见场景，HARP的设计思路可扩展到其他异构加速器（如GPU+TPU混合集群）

> **信息来源**：arXiv:2509.24859 摘要

---

## 1.9 HetAuto: Cross-Cluster Auto-Parallelism for Heterogeneous Distributed Training

**作者**：Guicheng Qi, Junwei Su, Liqi Yang, et al.
**机构**：The University of Hong Kong, Meituan Corporation
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

随着大型语言模型参数规模突破千亿甚至万亿级别，单一计算集群的 GPU 资源已难以满足训练需求。以 GPT-4、Gemini 等模型为例，其训练需要数万张 H100 GPU 持续运行数月，这使得跨集群分布式训练成为必然选择。然而，跨集群训练面临三个根本性挑战：首先是硬件异构性——不同集群可能使用不同代际的 GPU（H100、A100、V100）、不同架构的加速器（NVIDIA GPU、AMD GPU、TPU），导致计算性能和内存容量差异巨大，静态并行策略无法有效适应这种异构性；其次是硬件兼容性问题——不同加速器的软件栈差异使统一的训练编排变得复杂；第三是跨集群通信瓶颈——集群间的网络带宽通常是集群内部互联带宽的 1/10 至 1/100，AllReduce 等集合通信操作的通信时延急剧增加。现有分布式训练框架（如 Megatron-LM、DeepSpeed）主要针对同构集群设计，其自动并行策略搜索算法（如 Alpa、FlexFlow）未考虑跨集群异构环境中的通信成本模型和硬件兼容性约束，导致在跨集群场景中负载严重不均衡。

HetAuto 提出了面向异构跨集群分布式训练的自动并行化框架，包含三项核心创新。第一，基于蒙特卡洛树搜索（MCTS）的自动并行策略搜索引擎：将并行策略搜索建模为序列决策问题，使用随机森林增强的成本模型高效评估异构设备上不同并行配置的执行时间，相比传统基于整数线性规划的方法（ILP）显著降低搜索开销。第二，Virtual-1F1B 调度策略：专门针对跨集群通信瓶颈设计，通过虚拟阶段的引入将跨集群通信与计算重叠执行，并优化重分区策略以最小化跨集群数据传输量，使得通信延迟对训练吞吐的影响被有效隐藏。第三，统一加速器 API：提供对 NVIDIA GPU、AMD GPU、TPU 等多种加速器的无缝兼容集成，通过硬件抽象层屏蔽不同加速器的软件栈差异。在 4 个异构集群、最多 736 个异构设备的大规模评估中，HetAuto 相比基线实现最高 1.57 倍的训练吞吐提升。

### 技术线索与启示

- **云原生与分布式架构**：跨集群训练是多云/混合云场景的核心需求，HetAuto 的统一 API 层和异构感知并行策略可应用于联邦学习、地理分布式训练等场景
- **性能工程与可观测性**：MCTS + 随机森林成本模型的策略搜索方法将机器学习算法融入系统优化决策，为其他组合优化问题（如编译器优化、资源调度）提供了可参考的范式
- **可扩展性与高性能计算**：Virtual-1F1B 的通信-计算重叠思想对跨数据中心、跨地域的训练和推理场景具有重要借鉴意义
- **开放性问题与未来方向**：跨集群通信优化需要结合网络拓扑感知的更深度设计，特别是在高延迟广域网环境下的容错机制

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 1.10 FlashOverlap: Efficient and Adaptable Overlapping for Computation and Communication via Signaling and Reordering

**作者**：Ke Hong, Xiuhong Li, Minxu Liu, Qiuli Mao, Tianqi Wu, Zixiao Huang, Lufang Chen, Zhong Wang, Yichong Zhang, Zhenhua Zhu, Guohao Dai, Yu Wang
**机构**：Tsinghua University, Infinigence-AI, Shanghai Jiao Tong University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK
**arXiv**：2504.19519 | **DOI**：10.1145/3767295.3769370

### 技术概要

随着生成式模型在聊天机器人、代码助手、视频生成和智能体系统等领域的广泛应用，模型参数量呈指数级增长——DeepSeek-V3 已有 671B 参数，Meta 的 Llama 4 Behemoth 更扩展至 2T 参数。单 GPU 无法容纳如此规模的模型，必须通过张量并行（TP）、流水线并行（PP）和专家并行（EP）等方式将参数切分到多设备上。这种多 GPU 计算范式不可避免地引入了 AllReduce、ReduceScatter、All-to-All 等集合通信操作带来的显著通信开销。尤其在消费级 GPU（如 NVIDIA 4090、L20）上部署时，PCIe 互联仅提供 16-64 GB/s 双向带宽，通信瓶颈更加突出。计算与通信重叠（overlapping）利用 GPU 的并发硬件执行能力，是缓解通信开销的有效技术。然而，现有重叠方案存在根本性的设计权衡困境：基于分解的方法（如将 GEMM 拆分为多 kernel）会引入额外的 kernel launch 开销和精度损失；基于融合的方法（如将通信操作嵌入计算 kernel）则需要为每种通信原语定制专用 kernel，开发负担重且缺乏通用性；基于多数据流调度的方法虽然灵活但无法保证计算性能不受干扰。

FlashOverlap 通过一种轻量级信令（signaling）与重排序（reordering）机制，同时实现了分块级重叠、无干扰计算和通信无关性三大设计目标。其核心创新在于：在 GPU 计算 kernel 执行过程中，当部分输出完成后，计算 kernel 主动发送信号触发该部分数据的通信操作，同时继续执行剩余部分的计算，从而实现已完成部分通信与剩余部分计算的天然重叠。为最大化重叠效率，FlashOverlap 设计了一套精密的信令时机机制——从传统的 tile 级演进到 wave 级再优化为 group 级，通过 group-wise tile counting 在足够的重叠窗口与最小的信令开销之间取得平衡。在此基础上，由于 GPU kernel 的 tile 执行顺序是不规则的，FlashOverlap 引入了执行顺序感知的重排序：通信前将已完成的数据重排到连续地址（便于直接调用 NCCL API），通信后再将数据恢复为正确的顺序。为进一步提升性能，FlashOverlap 还设计了预测性搜索（Predictive Search）算法，通过分解重叠延迟模型，在离线阶段预计算设计空间并在在线阶段快速调优参数。在多种模型和并行配置下的实验表明，FlashOverlap 实现了最高 1.65 倍的加速，优于 DeepSpeed、TeraPipe 等现有方案，且完全基于标准的 NCCL API 调用，无需任何定制通信原语。代码开源于 https://github.com/infinigence/FlashOverlap。

### 技术线索与启示

- **系统软件方向**：信令驱动的计算-通信重叠是一种通用范式，可集成到 NCCL 等通信库中作为标准特性，使所有框架受益而无需修改上层代码
- **软件工程与系统设计**：通信无关性设计原则极为重要——FlashOverlap 完全基于 NCCL API 构建，证明了通过巧妙的系统设计可以在不侵入通信库的前提下实现高效重叠
- **性能工程与可观测性**：预测性搜索算法将设计空间剪枝与快速在线调优结合，为大规模分布式训练中的自动化参数调优提供了可参考的实践模式
- **可扩展性与高性能计算**：group-wise tile counting 的信令粒度选择揭示了在 GPU 硬件特性约束下进行系统优化的思维方法——在重叠窗口与信令开销之间取得平衡

> **信息来源**：[arXiv:2504.19519](https://arxiv.org/abs/2504.19519) | [DOI:10.1145/3767295.3769370](https://doi.org/10.1145/3767295.3769370)

---

## 1.11 Crimson: Collaborative Parameter Updates for Efficient Pipeline Training of Large Language Models

**作者**：Yapeng Jiang, Wuhui Chen, Ganhong Huang, et al.
**机构**：Sun Yat-sen University, Hong Kong University of Science and Technology, Pengcheng Laboratory
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

训练千亿参数级大语言模型时，仅 Adam 优化器状态就需要模型参数 3 倍以上的 GPU 显存——对于一个 175B 参数的 GPT-3 级别模型，仅 FP32 参数就需约 700GB，加上 FP32 优化器状态（动量 + 方差，各 700GB）则总计超过 2TB，远超出任何单 GPU 的显存容量。现有方案主要通过 ZeRO-Offload 等方法将优化器状态和参数更新任务卸载到 CPU 内存，但 CPU 的标量计算能力远弱于 GPU，导致参数更新成为新的瓶颈——特别是在流水线并行中，每个 pipeline stage 的 GPU 在完成前向/反向传播后需等待 CPU 完成参数更新，产生严重的 GPU 空闲（pipeline bubble）。传统的 1F1B（One-Forward-One-Backward）调度虽然能部分利用 bubble 填充通信，但并未从根本上解决 CPU 卸载带来的计算瓶颈。此外，不同 pipeline stage 的计算负载和参数量天然不均衡，统一的 CPU 卸载策略导致有的 stage 参数更新快、有的慢，加剧了等待时间。

Crimson 提出协同参数更新方案，将优化器状态的存储和更新任务从单一设备分布式地扩展到多个计算资源。其核心思想是将每个 pipeline stage 的参数更新任务分散到三个层次执行：本地 GPU 负责部分高频参数的即时更新（减少 GPU-CPU 数据传输），本地 CPU 负责中等频率的参数，以及后续 pipeline stage 的空闲 GPU 协助处理计算密集型参数更新——从而形成一个跨 stage、跨设备的协同优化器网络。在此架构之上，Crimson 设计了多阶段协同优化器（Multi-Stage Collaborative Optimizer），通过精细的依赖分析和调度算法协调不同设备的计算和通信时序。在此基础上，Crimson 还引入了梯形气泡感知调度（Trapezoid-Bubble-Aware Scheduling），将参数更新过程建模为约束优化问题，根据各 pipeline stage 的 bubble 大小和参数更新延迟确定最优的任务分配策略，进一步减少 GPU 空闲时间。与 ZeRO-Offload 结合使用时，Crimson 实现了超过 1.35 倍的吞吐提升。

### 技术线索与启示

- **系统软件方向**：协同参数更新的思想——将计算任务分散到 GPU、CPU 及其他 stage 的空闲 GPU——可扩展到推理和微调场景中的所有需要 GPU-CPU 协作的流水线作业
- **性能工程与可观测性**：将参数更新调度建模为约束优化问题的方法论可应用于其他流水线气泡消除场景，如 MoE 模型中的专家负载均衡和 KV-Cache 管理中的内存调度
- **可扩展性与高性能计算**：多阶段协同优化器的设计模式为异构计算资源的协同调度提供了系统框架，可在分布式训练之外的场景中复用
- **开放性问题与未来方向**：随着模型从千亿参数向万亿参数演进，优化器状态的内存管理仍是最突出的系统挑战之一，需要通信、计算、存储三个维度的联合优化

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 1.12 Suika: Efficient and High-quality Re-scheduling of 3D-parallelized LLM Training Jobs in Shared Clusters

**作者**：Yuxuan Wang, Yanbo Wang, Chen Chen, et al.
**机构**：Shanghai Jiao Tong University, TeleAI, Huawei
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

在共享 GPU 集群中，多个大语言模型训练作业竞争有限的计算资源，集群调度器需要在作业之间进行资源重调度以优化全局指标（如平均作业完成时间 JCT）。3D 并行训练——数据并行（DP）、张量并行（TP）和流水线并行（PP）的组合——使重调度问题异常复杂：改变一个作业的 GPU 分配需要同时调整三种并行维度的配置，且不同的并行配置组合产生截然不同的训练吞吐和通信开销。现有重调度方案面临三大核心挑战：性能建模开销——每次调整并行配置后需要重新估计训练吞吐，但精确的性能模型构建成本高；决策复杂度——资源分配和并行化配置的联合搜索空间巨大，传统启发式算法（如贪心、轮询）难以找到高质量解；重部署开销——作业从旧配置迁移到新配置需要释放并重新分配 GPU、重新加载模型参数和优化器状态，这一过程可能耗时数十分钟。

Suika 利用重调度的增量性质系统性地应对这三大挑战。第一，非侵入式在线 profiling：不同于重新运行 benchmark 或在代码中植入探针的传统方法，Suika 在作业运行时通过分析 GPU kernel 执行轨迹（trace）和通信日志，在几乎不干扰训练作业的前提下构建准确的性能估计器，捕获不同并行配置下的吞吐和通信开销。第二，拓扑感知排序 + 扩展-均衡算法：将资源分配和并行化决策分解为两个阶段——首先根据集群拓扑（如 NVLink 域、节点间网络带宽）对候选 GPU 集合进行排序，然后使用扩展-均衡算法在排序后的空间中高效搜索最优并行配置，将决策复杂度从指数级降低到多项式级。第三，设备到设备重部署：利用增量重配置的交叠特性——新旧配置之间通常有大部分 GPU 重叠——仅重新分配少量新增或替换的 GPU，并通过流水线化的参数传输减少等待时间。在 64-GPU 物理集群和 1024-GPU 模拟集群的评估中，Suika 相比基线调度器实现平均 JCT 降低 1.29-1.31 倍。

### 技术线索与启示

- **云原生与分布式架构**：增量重调度的思想适用于所有需要在线调整资源配置的云系统——Kubernetes 的 Pod 重调度、数据库分片的动态调整、推理服务的弹性扩缩均可借鉴
- **系统软件方向**：非侵入式在线 profiling 方法通过分析已有 GPU trace 和通信日志进行性能建模，可应用于其他运行时性能建模的分布式系统，避免侵入性探针带来的性能扰动
- **性能工程与可观测性**：拓扑感知排序 + 扩展-均衡的两阶段搜索算法为大规模组合优化问题提供了高效且可扩展的求解范式
- **开放性问题与未来方向**：3D 并行重调度与弹性训练的深度融合——在训练过程中动态调整并行配置而不重启作业——是社区持续努力的方向

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 1.13 Maya: Optimizing Deep Learning Training Workloads using GPU Runtime Emulation

**作者**：Srihas Yarlagadda, Amey Agrawal, Elton Pinto, et al.
**机构**：Georgia Institute of Technology, NVIDIA
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK
**arXiv**：2503.20191 | **DOI**：10.1145/3767295.3769366

### 技术概要

训练大型基础模型动辄耗资数亿美元，部署优化成为影响成本的核心环节。当前实践中，机器学习工程师需要在昂贵计算集群上反复试错来手工制定训练配置方案（training recipe）。为支持高效的配置探索，研究者开发了多种性能建模系统如 Daydream、Habitat、Calipers 等，但都面临一个根本性的语义鸿沟：它们要求用户将实际工作负载翻译成各自的自定义规范语言，导致系统必须在三种不完美折衷中取舍——仅支持狭窄的工作负载集合以保持可用性，要求复杂规范编写从而限制实际采用，或采用简化的性能模型牺牲预测精度。

Maya 通过透明设备仿真（transparent device emulation）从根本上消除了语义鸿沟。其设计洞察在于：训练框架如 PyTorch 与 GPU 之间的接口本身就是一个窄而稳定的抽象层——无论何种模型架构、何种并行策略，最终都通过统一设备 API 调用（如 kernel launch、memcpy 等）与硬件交互。Maya 在这一窄接口处插入透明拦截层，直接记录未修改训练代码发出的所有设备 API 调用序列及其依赖关系，精确捕获完整工作负载行为——无需任何代码修改或翻译。基于捕获的低级操作序列，Maya 构建了高保真性能模型，能模拟不同 GPU 配置、通信拓扑和并行策略下的端到端训练时间。实验表明 Maya 在涵盖 GPT、Llama、Grok 等多种模型架构和梯度累积、混合精度、FlashAttention 等多种优化策略的测试中实现不到 5% 的预测误差，识别出的配置方案可降低高达 56% 的训练成本。

### 技术线索与启示

- **系统软件方向**：透明设备仿真通过利用框架-设备之间的已有窄接口进行零侵入拦截，是一种通用性能建模方法论，可应用于 TPU、ASIC 等其他加速器
- **软件工程与系统设计**：Maya 的关键洞察在于「使用已有接口」而非「创建新接口」，这一思想对设计零侵入系统工具有普遍启示意义
- **Agent 与 LLM 应用方向**：自动化训练配置优化可大幅减少 ML 工程师手工调优工作，结合高保真建模与自动搜索可构成闭环训练效率优化 Agent
- **可扩展性与高性能计算**：实验覆盖 8 到 512 GPU 规模，证明基于 API 级仿真的方法在不同规模下均能保持高精度

> **信息来源**：[arXiv:2503.20191](https://arxiv.org/abs/2503.20191) | [DOI:10.1145/3767295.3769366](https://doi.org/10.1145/3767295.3769366)

---

## 1.14 MegaScale-Omni: A Hyper-Scale, Workload-Resilient System for MultiModal LLM Training in Production

**作者**：Chunyu Xue, Yangrui Chen, Jianyu Jiang, et al.
**机构**：ByteDance Seed, Shanghai Jiao Tong University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK
**arXiv**：2605.08962

### 技术概要

多模态大语言模型（MLLM）通过在视觉、音频、文本等多模态数据上进行预训练，获得了强大的跨模态理解和生成能力，已广泛应用于搜索理解、内容审核和智能助手等生产场景。然而，多模态训练面临一个独特挑战：与纯文本 LLM 训练中均匀的样本长度分布不同，多模态数据集天然呈现动态的模态混合比例和高度可变的样本长度分布——一帧图像处理可能只需几十毫秒而一段长视频则需数百倍的计算时间。现有训练系统（如 Megatron-LM、DeepSpeed）针对纯文本训练优化，采用编码器和 LLM 主干之间静态耦合的资源分配和并行化策略，导致在动态负载下 GPU 空闲严重：编码器处理完一个短样本后需等待 LLM 主干完成当前批次，反之亦然。此外，现有系统缺乏对多模态数据特性的感知，无法针对变长样本和模态不平衡进行精细调度。

MegaScale-Omni 是字节跳动 Seed 团队面向数千 GPU 生产环境设计的多模态 LLM 训练系统，基于编码器-LLM 复用训练方案提出了三大核心创新。第一，解耦并行策略：编码器采用长短序列并行（Long-Short Sequence Parallelism）处理变长多模态样本，LLM 主干使用完整的 5D 并行（数据、张量、流水线、序列、专家并行），两者在通信高效的并行化布局下独立决策，消除了静态耦合带来的 GPU 空闲。第二，统一编码器-LLM 表示和编码器-LLM 联合流水线：通过统一的内存和数据结构表示实现灵活可扩展的共置（co-location），同时设计了编码器-LLM 联合流水线调度策略使两种计算在流水线阶段间无缝衔接，提供工作负载韧性。第三，去中心化分组重排序和自适应 resharding：通过去中心化的分组数据重排序应对模态比例动态变化和样本长度异构性，自适应 resharding 机制在负载变化时动态调整参数分布。生产环境数千 GPU 部署评估显示，MegaScale-Omni 相比基线实现 1.27 倍至 7.57 倍的吞吐改进。

### 技术线索与启示

- **系统软件方向**：5D 并行 + 编码器解耦的设计模式可推广到其他多组件异构模型架构（如视觉-语言-行动模型），核心思想是将异质组件之间的并行策略完全解耦
- **数据密集型系统**：去中心化分组重排序的数据加载方法适用于其他多源异构数据处理场景，特别是数据分布动态变化的生产环境
- **可扩展性与高性能计算**：编码器-LLM 联合流水线的调度策略为多阶段异构计算流水线提供了优化框架，可应用于推荐系统、视频理解等场景
- **开放性问题与未来方向**：多模态训练的模态间负载均衡和动态比例调整仍是持续挑战，特别是新模态（如触觉、3D）加入时的扩展性问题

> **信息来源**：[arXiv:2605.08962](https://arxiv.org/abs/2605.08962)

---

## 1.15 ReCCL: Handling Network Faults in Distributed AI Training: Failover is Now an Option

**作者**：Xin Zhe Khooi, Zhuo Jiang, Pan Xie, et al.
**机构**：National University of Singapore, ByteDance
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

在大规模分布式 AI 训练中，网络故障是导致训练中断的首要原因。在现代万卡集群（如训练 Llama 4 或 GPT-5 级别的模型）中，数千个 GPU 节点通过 InfiniBand 或 RoCE 高速网络互联，每个节点通常配备 8 个 NIC（网络接口卡）通过多路径连接到交换机。在这种规模下，故障不可避免——一项典型研究显示，在 16,384 张 GPU 的集群中，平均无故障时间（MTBF）可能仅 2.7 小时。网络故障（NIC 损坏、线缆松动、交换机端口故障等）在所有硬件故障中占比高达 50%。当网络故障发生时（尤其是最后一跳交换机到主机的链路故障），RDMA 连接丢失导致 NCCL 等集合通信库（CCL）中的集体操作超时，进而触发 PyTorch 等训练框架终止整个训练作业。传统应对策略是完全被动的：作业崩溃后，系统重新分配 GPU 资源，从最近的检查点恢复训练状态，并重新计算故障点之后的所有迭代——这一过程的中位恢复时间高达 68 分钟，造成巨大的算力浪费。

ReCCL 是首个面向网络容错的集合通信库，从根本上改变了分布式训练应对网络故障的范式——从「故障即崩溃」（fail-stop）转向「故障即切换」（failover）。其核心观察是：现代 GPU 服务器通常配备多个 NIC，通过 PCIe 或 NVLink 等异构链路互联，本质上提供了冗余的网络路径。ReCCL 在网络故障发生时，自动检测到故障的 NIC 连接，并将其上正在进行的集合通信操作无缝切换到同一节点上的备用 NIC 路径，整个过程对上层训练框架完全透明，训练进度不受影响。在故障切换期间，ReCCL 通过三个关键机制保持通信效率和状态同步：动态通道负载均衡——在降级网络拓扑下重新分配通信负载以适应带宽减少；主机内 GPU 路由——利用 NVLink 或 PCIe 交换机在本地 GPU 之间转发数据以绕过失效 NIC；以及通信状态同步——确保所有参与节点在切换后保持一致的通信状态。实验评估表明 ReCCL 可以以最小的性能损失（与无故障情况相比）实现无缝故障切换。大规模仿真进一步证实，相比传统 fail-stop + 重启方案，ReCCL 的故障切换策略可显著节省 GPU 时间。

### 技术线索与启示

- **安全与可信计算**：通信层的容错设计为分布式系统韧性提供了新维度——不同于传统的检查点容错（计算层）和冗余计算（应用层），通信层容错在更底层、更高效的位置拦截故障
- **系统软件方向**：容错 CCL 的设计范式可直接集成到 NCCL、RCCL 等主流通信库中，使所有基于这些通信库的框架（PyTorch、JAX 等）自动获得故障切换能力
- **开放性问题与未来方向**：训练容错从检查点恢复到通信层故障切换的范式转变值得关注——将两种容错机制互补（细粒度故障用切换、粗粒度故障用检查点）可能是最优策略
- **可扩展性与高性能计算**：随着集群规模从万卡向十万卡演进，网络故障频率线性增长，ReCCL 的故障切换机制在大规模集群中的价值更加显著

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 1.16 Laminar: A Scalable Asynchronous RL Post-Training Framework

**作者**：Guangming Sheng, Yuxuan Tong, Borui Wan, et al.
**机构**：The University of Hong Kong, ByteDance
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

强化学习后训练（RL Post-Training）已成为提升大语言模型推理能力、指令遵循能力和安全性的事实标准——OpenAI 的 o 系列模型、DeepSeek-R1、Kimi K1.5 等前沿模型均采用了 RL 后训练管线（通常使用 PPO 或 GRPO 算法）。RL 训练采用经典的 actor-learner 架构：多个 actor 通过 rollout 生成推理轨迹（chain-of-thought），learner 收集这些轨迹计算优势函数并更新模型权重。然而在大规模集群上运行时，RL 训练面临一个独特而严重的挑战——轨迹生成的长尾延迟（straggler tail）：不同推理轨迹的长度差异巨大（从几十个 token 到数万个 token 不等），导致 rollout 的完成时间呈现极端长尾分布，而现有同步 RL 系统要求所有 rollout 完成后才能进行全局权重同步，这使得大量 GPU 处于空闲等待状态。此外，异步 RL 系统（如 IMPALA）虽然允许部分同步，但依赖 actor 和所有 rollout 之间的全局权重同步机制（如定期广播模型参数），创建了刚性的模型更新调度，在高度倾斜的轨迹生成延迟分布下仍然效率低下。

Laminar 通过轨迹级异步（trajectory-level asynchrony）彻底打破了传统 actor-learner 架构中的锁步（lock-step）限制。其核心设计包含三个层次。第一，中继 worker 层：替代全局权重同步，引入一层中继 worker（relay workers）作为分布式参数服务，每个 relay worker 维护模型参数的最新版本，actor 在完成单个轨迹（而非整个 batch）后立即向 relay worker 拉取最新权重并开始新轨迹生成，实现异步细粒度权重同步。第二，动态 repack 机制：实时监测各 rollout 的轨迹生成进度，将多个短轨迹合并到少数专用 rollout worker 上集中处理，而将长尾的单个长轨迹分配到独立的 rollout worker 上持续执行，最大化生成吞吐。第三，完全解耦设计：将 actor rollout、relay worker 和 learner 三个组件之间的故障域完全隔离——任何一个组件的故障（如 actor 节点宕机）不会级联到其他组件，确保长时间运行（数周至数月）的训练任务具有鲁棒性。在 1024-GPU 集群上的评估显示，Laminar 实现了最高 5.48 倍的训练吞吐加速。

### 技术线索与启示

- **Agent 与 LLM 应用方向**：RL 后训练是 Agent 能力提升的核心手段，Laminar 的异步框架可直接服务于 Agent 的大规模 RL 训练——轨迹级异步特别契合 Agent 轨迹长度高度可变的特性
- **系统软件方向**：中继 worker 层 + 轨迹级异步的设计模式可推广到其他 actor-learner 架构（如推荐系统中的在线学习、游戏 AI 中的 self-play 训练），分布式参数服务的细粒度同步是关键
- **云原生与分布式架构**：完全解耦设计带来的故障隔离能力对长时运行（数周至数月）的云原生训练任务至关重要——不因局部故障而损失全局进度
- **可扩展性与高性能计算**：动态 repack 机制通过在 rollout worker 之间重新分配轨迹负载来消除长尾延迟，这一思想可应用于其他存在 straggler 问题的分布式计算框架

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

# Part 2: LLM Inference

> 本部分涵盖14篇论文，涉及投机解码、请求调度、KV Cache管理、模型家族服务、多模态服务、稀疏注意力、端侧推理、端-云协同推理、可信执行以及推理流水线优化。

---

## 2.1 AdaServe: Accelerating Multi-SLO LLM Serving with SLO-Customized Speculative Decoding

**作者**：Zikun Li, Zhuofu Chen, Remi Delacourt, et al.
**机构**：Carnegie Mellon University, Princeton University, EPFL, Amazon Web Services, Purdue University
**发表信息**：EuroSys 2026

> **信息来源**：EuroSys 2026 会议论文集

### 技术概要

现代LLM应用呈现日益多样化的服务等级目标（SLO）需求——从交互编程助手要求的亚秒级响应延迟，到实时对话Agent的数百毫秒级端到端延迟，再到数据整理和批量处理任务可容忍的数十秒宽松约束。这种异构SLO需求源于LLM应用的广泛渗透：ChatGPT类对话产品要求TTFT（Time To First Token）在200-500ms内以保证自然对话体验；代码补全工具（如GitHub Copilot）要求解码延迟极低以实现实时补全；而文档摘要、数据标注等离线任务则更关注吞吐量而非单次延迟。然而，现有LLM推理服务系统（如vLLM、TensorRT-LLM、SGLang）主要采用统一批处理调度策略，对所有请求施加相同的服务水平，无法同时高效满足异构SLO。核心矛盾在于：当快速SLO请求与慢速SLO请求混在同一个batch中时，快请求完成decode后需等待慢请求，造成head-of-line阻塞；反之，若快慢分离调度，慢请求可能长期得不到GPU时间片而饿死。这种"一刀切"的服务方式迫使服务提供商为最严格的SLO过度配置资源，或在SLO较宽松时浪费GPU算力。

AdaServe是首个支持多SLO并发服务的LLM推理系统，核心创新在于将投机解码（Speculative Decoding）重新定位为SLO定制的可控调节机制。投机解码最初由Google Leviathan等人和Chen等人提出，利用小型draft模型预测未来token，再由大型target模型并行验证，通过计算换延迟的方式加速自回归生成。AdaServe的关键洞察是：投机解码的"激进程度"（投机树的分支因子和深度）形成了一个连续的延迟-计算代价谱系——更激进的投机产生更低延迟但消耗更多计算，更保守的投机延迟略高但计算开销更小。因此，投机策略可以按每个请求的SLO需求进行定制：对严格SLO的请求采用激进投机以达到目标延迟，对宽松SLO的请求采用保守投机以节省计算资源。

系统将多SLO服务形式化为约束优化问题：在满足每个请求延迟SLO的前提下，最小化总计算资源消耗。为此，AdaServe引入了硬件感知算法，为每个请求动态构建适配其延迟目标的投机树。硬件感知体现在：不同GPU架构（如A100 vs H100）的SM数量、内存带宽、Tensor Core吞吐各异，导致同一投机树在不同硬件上的实际延迟特征不同。算法结合硬件性能模型，在线搜索最优投机树拓扑（分支宽度、树深度、token候选数量），使每个请求恰好达到其SLO——不过度也不不足。系统设计了speculate-select-verify三段式流水线：draft模型执行投机预测生成候选token序列；select引擎基于大模型的KV Cache状态和注意力模式选择最有希望的候选路径；verify阶段由大模型并行验证所有候选，接受最长匹配前缀。通过流水线化这三个阶段，AdaServe实现了细粒度解码速度控制的同时最大化系统整体吞吐。

系统具备动态自适应能力：运行时持续监控请求到达模式、长度分布变化以及GPU利用率，当检测到工作负载漂移（如从短对话请求切换为长文档请求，或请求突发）时，自动调整全局投机参数和各请求级别的投机配置。评估显示AdaServe减少SLO违规最高4.3倍，goodput提升最高1.9倍。这项工作是LLM服务从"尽力而为"走向"SLO保证"的重要一步，其将投机解码从纯性能加速技术重新定位为QoS控制机制的思想，为未来多租户、差异化SLA的LLM云服务奠定了理论基础。

### 技术线索与启示

- **Agent与LLM应用方向**：多SLO服务是Agent系统的核心需求——实时对话Agent要求低延迟交互，推理型Agent可容忍较高延迟以换取深度思考，而监控类Agent关注持续吞吐而非单次响应。AdaServe的SLO定制化设计可直接适配多Agent并行服务的差异化需求，使得同一GPU集群可以高效地同时服务多种类型的Agent工作负载。
- **系统软件方向**：SLO定制投机解码的约束优化方法可推广到其他需要差异化服务的场景，如差异化视频编码（高SLO→高码率低延迟，低SLO→低码率）、数据库查询的差异化执行计划等。硬件感知参数搜索的方法论也为自适应系统调优提供了范式参考。
- **性能工程与可观测性**：硬件感知投机参数调整展示了运行时自适应优化的工程实践，关键在于建立准确的硬件性能代理模型以指导在线搜索，同时保证搜索开销远小于推理开销本身。这种在线性能建模+实时决策的架构是构建智能化推理系统的关键技术路径。

---

## 2.2 FlexPipe: Adapting Dynamic LLM Serving Through Inflight Pipeline Refactoring in Fragmented Serverless Clusters

**作者**：Yanying Lin, Shijie Peng, Chengzhi Lu, Chengzhong Xu, Kejiang Ye
**机构**：SIAT CAS, UCAS, UCSD, University of Macau
**发表信息**：EuroSys 2026

> **信息来源**：EuroSys 2026 会议论文集

### 技术概要

生产环境LLM推理服务面临双重系统性挑战：高度可变的请求模式和Serverless集群中严重的GPU资源碎片化。一方面，LLM服务的请求到达率呈现显著的时变特征——日间峰值时段请求密集、夜间稀疏，同时请求的输入/输出长度分布也随时间漂移（短对话→长文档生成→代码补全等模式切换）。另一方面，Serverless计算平台（如AWS Lambda GPU、Modal、BentoCloud等）虽然提供了弹性GPU分配能力，但由于GPU实例按需创建和销毁，集群中剩余的GPU资源散布在不同物理节点上，形成碎片化的拓扑格局——可用GPU之间可能缺乏NVLink等高速互联，甚至分布在不同的网络域中。传统的静态流水线并行（Pipeline Parallelism）配置——在部署时固定模型分区点、每个pipeline stage分配固定数量的GPU——在这种动态且碎片化的环境中表现出严重的适应性不足：当负载下降时，固定分区导致部分GPU闲置（"气泡"效应），GPU预留率高；当负载上升或GPU碎片化加剧时，固定分区无法利用分散的GPU碎片。

FlexPipe提出了运行时飞行中流水线重构（Inflight Pipeline Refactoring）的新范式，使LLM推理流水线能够动态适应负载变化和GPU拓扑变化。其设计基于三个核心创新。第一，细粒度模型分区：FlexPipe将LLM模型以比传统流水线并行更细的粒度分解为众多小型计算阶段（micro-stages），远多于实际GPU数量。每个micro-stage包含若干连续的Transformer层，并在分区时严格遵守计算图约束（如残差连接的边界约束），确保任何阶段的组合都不会破坏模型的前向传播语义。这种过度分区为后续的动态重组合提供了充分的灵活性。

第二，飞行中流水线重构配合一致的缓存转换（Cache-Consistent Transition）。这是FlexPipe最具挑战性的创新：当运行时决定改变流水线配置时（如调整stage数量、重新分配stage到不同GPU），系统中仍有正在处理的请求，其KV Cache与当前流水线布局绑定。FlexPipe通过两阶段转换协议解决：(1) 快照阶段：对当前KV Cache进行快照，按新旧流水线布局的映射关系重新分片；(2) 切换阶段：在流水线"气泡"（pipe bubble，即流水线天然的等待间隙）中完成KV Cache迁移和流水线配置切换，最小化对正在处理请求的干扰。转换过程保证KV Cache一致性——请求不会因流水线重构而丢失上下文或产生错误输出。

第三，拓扑感知资源分配。在碎片化的Serverless GPU集群中，可用GPU可能来自不同物理服务器，网络拓扑（NVLink域内、InfiniBand跨节点、以太网跨机架）差异巨大。FlexPipe的GPU分配器不仅考虑GPU可用性，还综合考虑：GPU间的通信带宽和延迟、流水线stage间的通信模式（前一层输出传递到下一层，通信模式为P2P单向数据流）、以及KV Cache迁移所需的额外带宽。分配策略的目标是最小化流水线关键路径上的通信代价，同时在碎片化约束下找到可行的GPU组合。

在82-GPU集群上的全面评估表明，FlexPipe实现了资源效率提升最高8.5倍（通过按需使用GPU而非按峰值预留），延迟降低38.3%（通过拓扑优化减少通信开销），GPU预留需求从传统的75%降至30%（通过飞行中缩容）。FlexPipe代表了Serverless环境下LLM服务从"静态部署"向"弹性编排"转变的关键技术，其飞行中重构的思想也为其他有状态分布式服务的弹性伸缩提供了参考。

### 技术线索与启示

- **云原生与分布式架构**：飞行中流水线重构是Serverless环境自适应部署的创新实践。FlexPipe解决了有状态服务（KV Cache绑定流水线布局）动态伸缩的核心难题——状态迁移与一致性保证。这一方法论可推广到其他需要维护会话状态的Serverless应用（如流处理管道、在线学习系统）。
- **系统软件方向**：细粒度模型分区+动态重构的思想可应用于其他需要弹性部署的深度学习推理任务。过度分区提供灵活性、动态合并提供效率——这种"分区-合并"的动态调整范式本质上是一种online graph optimization技术，可被集成到PyTorch、JAX等框架的编译器中。
- **开放性问题与未来方向**：Serverless环境中的GPU碎片化问题随着多租户增加将更加严重。FlexPipe目前假设同一模型的多副本服务，未来需要扩展到跨不同模型的GPU共享场景——不同模型的pipeline stage混在同一GPU上，问题将从"流水线重构"演变为"多流水线协同调度"，复杂度显著提升。

---

## 2.3 TokenFlow: Responsive LLM Text Streaming Serving under Request Burst via Preemptive Scheduling

**作者**：Junyi Chen, Chuheng Du, Renyuan Liu, et al.
**机构**：Shanghai Jiao Tong University, George Mason University, China Telecom Shanghai
**发表信息**：EuroSys 2026

> **信息来源**：EuroSys 2026 会议论文集

### 技术概要

实时LLM交互应用（如对话助手、AI搜索、代码辅助）依赖流式token生成来提供即时反馈——模型逐token生成输出，服务端通过SSE（Server-Sent Events）或WebSocket将每个token增量推送到客户端，用户在首个token到达后即可开始阅读，无需等待完整响应。这种流式服务需要同时满足两个质量指标：低TTFT（Time To First Token，用户感知的响应速度）和稳定TBT（Time Between Tokens，生成过程中的流畅度）。然而，在请求突发场景下（如热门话题引发用户集中提问、工作时间高峰），标准LLM服务系统的非抢占式调度策略表现出严重的僵化缺陷：一旦某个batch的decode循环开始，新到达的请求只能在队列中等待当前batch完成，导致TTFT随队列长度线性恶化。同时，被动式内存管理——仅在OOM风险时才触发KV Cache eviction——无法在突发场景下提前为即将到来的请求腾出空间，进一步加剧了处理并行度的下降。

TokenFlow通过两大机制解决上述问题。第一，抢占式请求调度：核心创新在于基于实时token缓冲区占用的动态优先级决策。每个活跃客户端维护一个token消耗缓冲区（display buffer），TokenFlow实时监控每个客户端的缓冲区水位和消耗速率。当某客户端的缓冲区接近耗尽（用户将感知到"卡顿"），其请求获得高优先级；当缓冲区充足时，优先级降低。在高优先级请求到达时，TokenFlow可抢占正在执行的batch——将当前batch的中间状态（KV Cache和partial output）保存，立即插入高优先级请求，完成后恢复原batch。这种基于"用户体验"而非"先来先服务"的调度策略直接优化了用户感知质量。

第二，主动KV Cache管理：TokenFlow从仅响应OOM信号的被动模式转变为基于预测的主动模式。系统持续追踪每个请求的KV Cache使用趋势和GPU内存水位，在剩余内存低于预警阈值时，前瞻性地将低优先级、低活跃度请求的KV Cache从昂贵的GPU HBM迁移到CPU内存（通过PCIe），将高优先级请求的KV Cache反向预取到GPU。关键是TokenFlow将KV Cache迁移的I/O与GPU计算进行流水线重叠：在GPU执行当前batch的attention计算时，后台DMA引擎并发执行KV Cache的PCIe传输，几乎完全隐藏迁移延迟。

在RTX 4090（消费级）、A6000（专业可视化）和H200（数据中心旗舰）三种不同定位的GPU上评估，覆盖了从边缘到云的部署场景。结果显示有效吞吐（满足SLO约束的有用token输出速率）提升最高82.5%，P99 TTFT降低最高80.2%。TokenFlow证明，在LLM流式服务中，调度策略的"抢占灵活性"和内存管理的"主动性"是应对突发负载的关键能力。

### 技术线索与启示

- **Agent与LLM应用方向**：流式体验优化直接影响Agent的交互质量。基于token缓冲区的用户体验驱动调度，启发了Agent系统中以"用户可感知延迟"而非"系统延迟"为优化目标的调度设计理念。尤其在多Agent协作场景中，可据此设计Agent间通信的差异化流控策略。
- **性能工程与可观测性**：基于token缓冲区状态的动态优先级调度是一种通用的流式系统优化方法，其将业务层指标（用户缓冲区水位）映射到系统层决策（调度优先级）的架构模式值得推广。主动式KV Cache管理的理念也适用于其他预取敏感的存储层次。
- **系统软件方向**：主动KV Cache管理（GPU-CPU间迁移）的设计可直接集成到vLLM、SGLang等推理框架中。抢占式调度+流水线I/O的技术组合也可应用于其他需要细粒度时间共享的GPU计算场景。

---

## 2.4 AdaGen: Workload-Adaptive Cluster Scheduler for Latency-Optimal LLM Inference Serving

**作者**：Sudipta Saha Shubha, Ayush Goel, Diman Zad Tootaghaj, et al.
**机构**：University of Virginia, HPE Labs, UC Riverside
**发表信息**：EuroSys 2026

> **信息来源**：EuroSys 2026 会议论文集

### 技术概要

LLM推理服务的延迟和成本挑战源于模型规模的指数增长与实时响应需求之间的根本矛盾。在多实例LLM集群部署中，请求被分发到多个GPU实例上并行处理，调度器的任务是在满足延迟SLO的前提下最大化集群吞吐和资源利用。现有集群调度器（如vLLM的前端router、Ray Serve的调度层）主要采用基于内存使用率的负载均衡策略——将请求路由到GPU内存余量最大的实例，隐含假设"内存越充足，处理越快"。然而，这一假设忽略了推理延迟的另一关键因素：计算布局（computational layout），即不同长度请求的prefill和decode阶段在同一个batch中如何排列组合。

计算布局之所以重要，是因为LLM推理的两个阶段具有截然不同的计算特性。Prefill阶段（处理输入prompt）是计算密集型，对输入token并行执行attention，GPU利用率高；Decode阶段（逐token生成输出）是内存带宽密集型，每个step处理batch中所有请求的下一个token，计算密度低。当长短请求混批时，长prefill请求会阻塞短请求的decode，而短prefill请求则会在decode阶段"搭便车"一起执行——batch的计算布局直接决定了GPU的SM占用率和内存带宽利用率，进而影响延迟。

AdaGen是工作负载自适应的集群调度器，其核心创新在于将计算布局作为首要优化目标。系统采用多步调度策略：第一步按请求的prefill和decode长度进行分类（short-prefill-short-decode、long-prefill-long-decode等类别）；第二步在每个类别内基于内存使用率进行负载均衡，同时考虑各实例已排队的计算布局；第三步跨实例选择性分布式执行——对于计算布局高度相似的请求，调度到同一实例以提高batch效率；对于计算布局冲突的请求，分散到不同实例以避免相互拖慢。每一步基于前一步的计算布局状态逐步优化。为避免实际执行生成布局的昂贵开销，AdaGen引入模拟估计器（simulation estimator），通过轻量级性能模型快速预测不同布局组合的延迟，使调度决策的开销远小于推理本身。

在生产负载trace上的评估表明，AdaGen实现3.6倍更高SLO达标率和2倍更好成本效率。该工作揭示了LLM集群调度中计算布局感知的重要性，为突破简单负载均衡的传统范式提供了新方向。

### 技术线索与启示

- **云原生与分布式架构**：计算布局感知的调度策略可推广到其他需要细粒度GPU资源管理的云服务，如批处理与在线服务混部的GPU集群。多步逐步优化+模拟估计的架构模式也适用于其他搜索空间大且评估昂贵的调度问题。
- **性能工程与可观测性**：模拟估计器替代实际执行的方法论值得在其他调度系统中借鉴——关键是要在估计精度和估计开销之间找到平衡。AdaGen的轻量级性能模型设计思路（基于计算布局而非完整模拟）是可推广的折中策略。
- **Agent与LLM应用方向**：按请求特征分类+差异化调度的思想对Agent的多优先级请求处理有参考价值。Agent系统中不同任务的推理需求特征（简单查询vs复杂推理）差异显著，可借鉴AdaGen的分类调度策略。

---

## 2.5 SkyWalker: A Locality-Aware Cross-Region Load Balancer for LLM Inference

**作者**：Tian Xia, Ziming Mao, Jamison Kerney, et al.
**机构**：UC Berkeley, Renmin University of China, Rice University
**发表信息**：EuroSys 2026

> **信息来源**：EuroSys 2026 会议论文集

### 技术概要

全球化的LLM推理服务部署面临成本与GPU可用性之间的尖锐矛盾。云提供商（如AWS、GCP、Azure）在各区域提供GPU实例，但由于全球GPU供应链紧张和区域需求差异，提供商通常采用长期承诺实例（预留实例或自建数据中心）来确保GPU供给，而非依赖随时可能缺货的按需实例。这种模式导致了一个根本性的资源利用问题：每个区域的服务容量必须基于该区域的峰值需求来规划（如东亚用户的工作时间高峰、北美用户的晚间高峰），但由于各区域的日变化模式（diurnal pattern）在时间上错开——当东亚处于高峰时北美可能在低谷，反之亦然——如果各区域独立服务本地流量，整体GPU池的峰值利用率仅在少数时段达标，大部分时间GPU资源严重闲置。

SkyWalker是多区域负载均衡器，其核心思想是利用地球自转带来的时区差异，通过跨区域流量聚合来平滑全球GPU使用曲线。当东亚区域处于午夜低谷时，SkyWalker将该区域的空闲GPU容量用于服务北美白天的峰值流量，反之亦然。这一设计使LLM服务提供商可以基于全球总需求的聚合峰值（而非各区域峰值之和）来规划GPU容量，从根本上减少过度配置。

然而，简单的跨区域流量转发会破坏KV-Cache的局部性——如果同一用户的连续请求被路由到不同区域的不同GPU实例，每次都需要重新计算prefill阶段的KV Cache，导致延迟增加和计算资源浪费。SkyWalker通过两个关键机制解决这个问题。第一，cache-aware跨区域流量处理器：系统维护全局请求亲和性表，追踪每个用户会话最近服务的区域和GPU实例。在路由决策时，优先将同一会话的后续请求发送到持有其KV Cache的GPU，仅在区域间负载严重不均衡时才进行跨区域迁移，且迁移时附带KV Cache状态信息以减少冷启动开销。第二，基于选择性推送的负载均衡机制：不同于传统pull模式（实例拉取请求），SkyWalker采用push-select模式——全局调度器根据各区域的实时负载和KV-Cache局部性分布，主动将请求选择性推送到目标区域，被推送区域只需评估本地GPU是否可以高效处理该请求（基于KV Cache命中率和当前队列长度）。

评估结果显示，SkyWalker实现1.12-2.06倍更高吞吐和1.74-6.30倍更低延迟，同时总服务成本降低25%。这项工作展示了地理分布式LLM服务中"时间维度"和"空间维度"协同优化的潜力。

### 技术线索与启示

- **云原生与分布式架构**：跨区域负载均衡利用时区差异提高资源利用率的思想可推广到其他全球化云服务——任何具有明显日变化模式的在线服务（视频流、游戏、社交网络）都可以通过跨区域流量调度来平滑资源需求曲线。选择性push模式也为传统的pull-based负载均衡提供了替代方案。
- **性能工程与可观测性**：KV-Cache局部性保持与跨区域路由的权衡设计是实用的工程范例。SkyWalker通过在全局调度层引入会话亲和性概念，将应用层状态（KV Cache）与网络层路由联动，这种"状态感知路由"模式值得推广。
- **绿色计算与可持续性**：降低25%服务成本意味着无需为峰值需求额外部署和运行GPU，直接带来约25%的能源消耗和碳排放减少。在全球AI能耗快速增长的背景下，跨区域负载均衡可作为一种重要的碳效率优化手段。

---

## 2.6 PiLLM: Resource-Efficient LLM Inference Using Workload Prediction

**作者**：Yunqian Fan, Shihao Bai, Ruihao Gong, Zaijun Wang, Rui Fan
**机构**：ShanghaiTech University, SenseTime, Beihang University
**发表信息**：EuroSys 2026

> **信息来源**：EuroSys 2026 会议论文集

### 技术概要

LLM推理服务面临的根本效率挑战源于工作负载的高可变性与资源分配的安全冗余之间的矛盾。这种效率损失在"跨GPU"和"GPU内"两个层面同时发生，且相互叠加。在跨GPU层面，为满足延迟SLO，服务运营商通常按峰值负载配置GPU数量——假设工作日高峰期需要8块GPU来保证P99延迟达标，那么这8块GPU必须持续在线，即使在夜间或周末的低谷期（可能仅需2块GPU）。这种峰值定向的资源规划导致GPU平均利用率极低，大量算力资源在非高峰时段白白浪费。在GPU内层面，为防止OOM（Out of Memory），现有推理引擎对每个请求的KV Cache内存分配采用最坏情况预留策略——按模型最大context length预分配内存，而实际请求的输入/输出长度通常远小于此上限。这种过度预留严重限制了GPU可同时服务的请求数量（batch size），降低了GPU的SM利用率和吞吐。

PiLLM的核心思想是：如果能够准确预测未来工作负载的计算和内存需求，就可以从被动的安全冗余模式切换为主动的精准分配模式，从而在两个层面消除资源浪费。系统的技术基础是工作负载预测算法，其通过对历史请求trace的深入统计分析——不仅关注输入/输出序列长度的均值，更关注长度分布的形状（方差、偏度、尾部特征）和请求到达的时间模式（日周期、周周期、突发频率）——建立高精度的计算需求（FLOPs）和内存需求（KV Cache字节数）预测模型。

基于工作负载预测，PiLLM实现两个互补优化。第一，弹性跨GPU调度：不同于传统基于当前负载的被动伸缩（如HPA基于CPU/内存阈值触发），PiLLM基于预测的未来负载趋势（如30秒后、2分钟后、10分钟后的GPU需求）进行前瞻性伸缩决策。系统构建了一个带预测窗口的优化模型：在未来T分钟内，在保证SLO达标率≥99%的约束下，最小化GPU·时间（GPU租赁成本）。关键创新在于伸缩决策考虑了GPU冷启动延迟——新GPU从无模型到可服务需要加载模型权重（数十GB），这一过程本身耗时数十秒。PiLLM将预测窗口与冷启动时间对齐，确保GPU在负载到达前已完成预热。

第二，GPU内精确内存分配调度器：在单个GPU实例内部，传统的KV Cache管理器（如vLLM的PagedAttention）虽然已经实现了块级分配，但分配逻辑仍是"请求一说'我可能需要4096个token的context'，就预留4096个token的KV Cache空间"。PiLLM基于预测模型为每个请求估计其实际最可能需要的输出长度，仅在最初分配"几乎确定需要"的基础KV Cache空间，后续根据请求生成进度的实时观察和剩余长度预测动态追加分配。这种方法类似于操作系统的内存过量分配（memory overcommit），但在风险控制上更为精细：通过对请求群体的统计预测，保证整体eviction概率低于0.1%，而非单个请求的绝对安全。

评估结果显示出显著的两个层面改进：跨GPU调度将平均GPU使用量减少1.6-3.1倍（取决于工作负载的可预测性），GPU内调度在KV Cache eviction率<0.1%的约束下持续提升有效吞吐。PiLLM代表了LLM推理资源管理从"被动冗余"到"预测驱动精准分配"的范式转变。

### 技术线索与启示

- **性能工程与可观测性**：工作负载预测驱动的弹性资源分配是通用的成本优化方法。PiLLM的核心价值在于将预测这一经典技术应用到LLM推理的两层资源分配中，且预测粒度不是粗粒度的"多少QPS"，而是深入到"每个请求的内存需求和计算需求"的粒度。这种细粒度预测+精准分配的模式可推广到数据库查询优化、CDN缓存预加载等场景。
- **云原生与分布式架构**：基于预测的GPU伸缩可集成到Kubernetes HPA、KEDA等自动伸缩机制中，为现有的基于阈值触发的伸缩策略补充前瞻性维度。关键是要将模型加载冷启动延迟纳入伸缩决策模型，避免"缩容后再扩容时的服务抖动"。
- **绿色计算与可持续性**：减少1.6-3.1倍GPU使用量直接降低能源消耗。考虑到LLM推理GPU的典型功耗（A100约400W，H100约700W），即使保守按2倍节省计算，大规模部署下的年度碳排放减少可达数百至数千吨CO₂当量。

---

## 2.7 FineMoE: Taming Latency-Memory Trade-Off in MoE-Based LLM Serving via Fine-Grained Expert Offloading

**作者**：Hanfei Yu, Xingqi Cui, Hong Zhang, Hao Wang
**机构**：Stevens Institute of Technology, Rice University, University of Waterloo, Rutgers University
**发表信息**：EuroSys 2026

> **信息来源**：EuroSys 2026 会议论文集

### 技术概要

Mixture-of-Experts（MoE）架构已成为大规模LLM的主流设计路线——从Google的Switch Transformer到Mistral的Mixtral 8x7B再到DeepSeek-V2/V3——通过稀疏激活（每个token仅路由到少数"专家"子网络）实现参数规模扩展而不等比增加计算量。然而，MoE架构也给推理服务带来了独特的内存挑战：虽然每个token仅激活少量专家（如8个专家中的2个），但所有专家参数都必须加载到GPU显存中以确保任意输入token都能路由到正确的专家。以Mixtral 8x7B为例，8个专家的总参数量约为7B×8=56B（不含共享层），但推理时每次前向只使用约14B参数的计算量——导致GPU显存中有75%的专家参数在任意时刻处于闲置状态，造成严重的内存低效。

现有方案通过将不活跃专家从昂贵的GPU HBM卸载到CPU DRAM来缓解内存压力，在专家被激活时再按需加载回GPU。但粗粒度的专家卸载策略（以整个专家FFN层为单位卸载/加载）面临根本性的延迟-内存权衡困境：若激进卸载（大量专家在CPU），推理延迟因频繁的PCIe传输而飙升；若保守卸载（尽量保留专家在GPU），GPU内存占用高、batch size受限。FineMoE提出了细粒度专家卸载来解决这个困境。其核心创新有两方面：第一，在专家选择层面，不同于简单的"最近使用"或"频率计数"策略，FineMoE提取MoE模型中路由器的细粒度专家选择模式（哪些专家经常被同一类型输入共同激活），以及输入提示的语义提示（通过分析prompt embedding的聚类特征推断后续token可能的路由分布），来精确预测未来需要哪些专家。第二，基于这些预测，系统实施分层缓存和预取策略：高概率即将激活的专家提前从CPU异步预取到GPU显存的"热区"（warm buffer），低概率专家延迟加载，极低概率专家保留在CPU，在GPU显存的"冷区"中也可能保留专家参数压缩版本以备不测。

细粒度的另一个维度体现在卸载粒度上：不同于以整个专家为单位，FineMoE将每个专家的参数进一步分解为更小的"微块"（如按FFN的中间维度分片），允许部分卸载——一个专家的部分参数在GPU，部分在CPU。这使得内存使用曲线更加平滑，避免了"全部加载或全部卸载"的阈值效应。

在六GPU测试床上的评估表明，FineMoE将推理延迟降低47%，专家命中率（在GPU上找到所需专家的概率）比SOTA提升39%。该工作展示了在MoE推理中，语义感知和细粒度管理是突破原有延迟-内存权衡的关键路径。

### 技术线索与启示

- **系统软件方向**：语义提示驱动的预取策略可应用于其他具有可预测访问模式的缓存系统。FineMoE将应用层语义（输入内容的embedding特征）融入系统层缓存决策的方法，为构建"应用感知"系统软件提供了范式——类似的思路可应用于图数据库的查询缓存、推荐系统的特征缓存等场景。
- **Agent与LLM应用方向**：MoE专家的细粒度管理对Agent多工具调用场景的资源管理有启发。Agent在调用不同工具时往往涉及不同的专家组合，可基于FineMoE的语义预测思想预测Agent的工具链使用模式，提前加载相关专家参数。
- **硬件-软件协同设计**：GPU-CPU间专家迁移的性能模型可指导内存带宽规划。FineMoE的微块粒度和分层缓存设计也为未来支持更细粒度内存管理的GPU架构（如支持HBM-CXL-DRAM多级存储层次）提供了软件侧的参考。

---

## 2.8 KUNSERVE: Parameter-centric Memory Management for Efficient Memory Overloading Handling in LLM Serving

**作者**：Rongxin Cheng, Yuxin Lai, Xingda Wei, Rong Chen, Haibo Chen
**机构**：Shanghai Jiao Tong University
**发表信息**：EuroSys 2026

> **信息来源**：EuroSys 2026 会议论文集

### 技术概要

LLM推理服务中GPU内存过载是一个极具破坏性的故障模式。在正常运行时，GPU HBM被模型权重和KV Cache占用，剩余空间用于batch处理。当负载尖峰（如突发流量、长上下文请求涌入）导致KV Cache需求超出剩余空间时，系统被迫进入"过载模式"：新到达的请求无法被立即调度到batch中，只能在请求队列中等待已有请求完成并释放KV Cache空间。由于LLM decode阶段每个token生成需要数十毫秒，一个正在处理的请求可能需要数十秒甚至数分钟才能完成，导致队列中的请求经历数个数量级的延迟飙升——原本100ms的TTFT可能变为10秒以上。

现有系统应对GPU内存过载的策略是"以KV Cache为中心"的，方法包括：(1) KV Cache丢弃（eviction）——从GPU内存中移除部分已完成请求的KV Cache；(2) KV Cache迁移（swapping）——将KV Cache通过PCIe传输到CPU内存，需要时再取回；(3) KV Cache卸载（offloading）——将不活跃请求的KV Cache暂存到CPU。这些方法的共同缺陷是释放内存的速度受限于KV Cache本身的大小和PCIe带宽——一个长请求的KV Cache可达数GB，通过PCIe传输需要数十到数百毫秒，在高负载尖峰时，释放速度赶不上新请求的到达速度，导致排队持续恶化。

KUNSERVE提出了一个范式转变的解决方案：以参数为中心（parameter-centric）的内存管理。其核心洞察是一个常被忽视的事实——在多GPU LLM推理部署中（典型的数据并行或混合并行配置），模型参数在多个GPU上被完整复制。例如，在一个4 GPU数据并行部署中，每个GPU都持有完整的模型权重（数十GB），这些重复副本的总和占据了大量GPU内存。KUNSERVE的关键创新是：在GPU内存过载时，不是丢弃或交换KV Cache（以数据为中心的思路），而是选择性丢弃模型参数的部分复制副本（以参数为中心的思路），瞬间释放大量GPU内存。

具体机制如下。当检测到内存过载时，KUNSERVE在各GPU上选择性地从显存中释放（unload）模型参数的不同子集——例如，4 GPU集群中，GPU 0释放Layer 1-10的参数，GPU 1释放Layer 11-20，GPU 2释放Layer 21-30，GPU 3释放Layer 31-40。释放后每个GPU上腾出大量KV Cache可用空间，请求可以大批量地立即开始执行。关键机制在于协作执行：被"丢弃"的参数通过流水线并行（Pipeline Parallelism）协作完成推理——一个请求在GPU 0上执行Layer 1-10的计算后，将中间激活传递到GPU 1执行Layer 11-20，依此类推。这样，虽然每个GPU不再拥有完整模型，但4个GPU作为整体仍持有完整参数副本，所有请求都能高效执行。

KUNSERVE推导了无冗余协作丢弃方案（redundancy-free cooperative offloading scheme）：确保每一层参数至少在集群中的某一个GPU上保留，且丢弃方案最小化流水线协作的通信开销。系统在检测到内存压力时自动触发参数丢弃，当负载下降后自动恢复参数（从CPU内存或SSD重新加载被丢弃的参数副本，或从其他GPU的保留副本中通过NVLink/PCIe复制）。

评估结果具有变革性：尾TTFT（即P99首token延迟）比Llumnix和vLLM等SOTA系统降低最高72.2倍。KUNSERVE的核心贡献在于重新定义了LLM服务中的"可丢弃资源"——从传统的"数据可丢弃（KV Cache）"转向"参数可丢弃（模型权重副本）"，开辟了LLM推理内存管理的新维度。

### 技术线索与启示

- **系统软件方向**：参数中心vs数据中心的管理思路是一种范式转变，对分布式系统资源管理有深远启发。传统分布式系统倾向于保护静态资源（配置、代码、模型参数）而牺牲动态数据（中间结果、缓存）。KUNSERVE颠倒了这一假设——在特定场景下，丢弃静态资源（模型参数副本）比丢弃动态数据（KV Cache）更高效。这一思想可推广到其他复制冗余很重的分布式系统，如分布式数据库索引缓存、流处理算子的有状态备份等。
- **性能工程与可观测性**：揭示了LLM服务中参数复制的隐藏资源浪费，为内存优化提供了全新视角。KUNSERVE的成功表明，当前LLM服务系统中存在着显著的结构性浪费，发现并利用这些浪费可以产生数量级的性能提升。建议系统设计者在优化前，应仔细审视系统的"隐藏冗余"——那些被视为理所当然但实际可以被动态调整的资源分配。
- **开放性问题与未来方向**：参数丢弃后的模型一致性恢复是需要继续深入的问题。KUNSERVE当前依赖从CPU或SSD重新加载参数来恢复，未来可探索增量恢复（仅恢复被修改的参数）、热备份（保留一个GPU不丢弃作为备份）、以及与投机解码的结合（丢弃参数后的流水线协作可能引入额外延迟，投机解码可补偿）。此外，参数丢弃+KV Cache eviction的联合优化（何时丢弃参数、何时丢弃KV Cache）也是一个值得研究的混合策略方向。

---

## 2.9 eLLM: High Throughput and Low Latency LLM Serving via Adaptive KV Caching

**作者**：Wenyan Chen, Chengzhi Lu, Huanle Xu, Kejiang Ye, Chengzhong Xu
**机构**：University of Macau, SIAT CAS, Nanyang Technological University
**发表信息**：EuroSys 2026

> **信息来源**：EuroSys 2026 会议论文集

### 技术概要

LLM推理服务的核心内存瓶颈源于模型权重和KV Cache对GPU HBM的巨大需求——以Llama2-70B在A100-80G上服务为例，模型权重（FP16）本身占用约140GB，需要至少2张A100（共160GB HBM）才能容纳，剩余空间几乎全部被KV Cache占据。为缓解这一瓶颈，现有系统（如FlexGen、Infinite-LLM）将KV Cache卸载到CPU内存，在需要时按需恢复到GPU。但这种"全或无"的粗粒度策略存在根本性缺陷：要么在GPU内存充足时缓存所有KV Cache（浪费GPU计算能力因batch size受内存限制），要么内存紧张时将过多KV Cache卸载到CPU（浪费GPU计算能力因频繁等待PCIe传输）。

eLLM的核心创新在于将KV缓存管理视为一个"缓存-重计算"的连续权衡问题，而非简单的"缓存或不缓存"的二元选择。系统引入了自适应KV缓存策略：在GPU内存不足时，不是粗暴地卸载整个请求的KV Cache，而是对每个请求选择性缓存部分token的Key-Value向量（如每隔K个token缓存一个），对未缓存的token在需要时通过动态并行重计算（recomputation）恢复。这个设计的精妙之处在于：重计算虽然消耗GPU算力，但其延迟可能远低于从CPU通过PCIe恢复KV Cache的延迟——特别是在GPU计算能力相对充裕（内存带宽是瓶颈）的场景下，用富裕的算力（TFLOPs）换取稀缺的内存带宽（GB/s）是一种有利的交换。

系统在两个层面实现自适应。在请求层面，token级缓存自适应器根据GPU当前内存水位和请求的上下文长度，实时优化每个请求的缓存密度（caching density）——哪些token缓存、哪些token重计算。优化目标是：在batch中所有请求的KV Cache总大小不超过GPU剩余内存的前提下，最小化重计算开销。这本质上是一个背包问题变种——每个请求可选不同的缓存密度（对应不同的内存占用和重计算开销），选择使总重计算开销最小的组合。eLLM使用贪心启发式算法在线近似求解。

在系统层面，eLLM利用通信-计算重叠和kernel融合技术进一步增强吞吐。当需要重计算未缓存token时，系统将重计算的GEMM运算与PCIe上同步进行的KV Cache预取重叠；同时将多个连续的重计算操作融合为单个CUDA kernel以减少kernel启动开销和寄存器溢出。

评估结果显示，eLLM实现3.03倍更高吞吐和2.63倍首token延迟降低。其技术核心价值在于打破了"KV Cache要么全缓存要么全卸载"的传统思维，将缓存密度作为一个可优化的连续变量引入系统设计空间。

### 技术线索与启示

- **系统软件方向**：缓存+重计算的混合策略（trading compute for memory）可应用于其他内存受限的计算密集场景，如图神经网络推理的特征缓存、科学计算的checkpointing策略等。连续化的缓存密度控制（而非二元的缓存/不缓存）是eLLM方法论的核心贡献。
- **性能工程与可观测性**：层级（请求级+系统级）双重优化的方法论对多层级系统设计有借鉴意义。eLLM展示了如何将单请求级别的优化（选择哪个token缓存）与系统级别的优化（通信-计算重叠）有机结合，形成协同效应。
- **硬件-软件协同设计**：通信-计算重叠在KV Cache管理中的应用展示了系统级优化的价值。未来GPU若能提供更灵活的显存层次（如HBM与L3 Cache间的可编程迁移），这种缓存密度自适应策略可进一步延伸到硬件层面。

---

## 2.10 MFS: An Efficient Model Family Serving System for LLMs

**作者**：Yunxuan Zhang, Hao Wang, Han Tian, et al.
**机构**：HKUST, USTC, Inspur
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

> **信息来源**：EuroSys 2026 会议论文集

### 技术概要

LLM服务提供商通常以"模型家族"的形式向用户提供选择——同一基础架构的不同规模变体（如Llama2的7B、13B、70B，Qwen的7B、14B、72B），用户根据任务复杂度和延迟预算选择合适规模。然而，当前的部署方式是将家族中每个模型独立部署，各模型的GPU实例相互隔离，无法共享计算资源。这种"独立部署"模式造成了显著的资源浪费：首先，家族内模型共享相同的网络架构，大模型的前几层与小模型的对应层在语义功能上高度相似——例如Llama2-70B的前16层和Llama2-7B的对应层都在学习基础语言特征（词法、浅层句法），但70B的实例必须从零开始计算这些浅层特征；其次，当用户在不同规模模型间切换时（如简单问题用7B，复杂问题用70B），两个模型实例的KV Cache和中间特征无法共享，每次切换都需完全重新计算。

MFS通过知识沉淀（Knowledge Precipitation）这一微调技术，将同一家族的最大模型重构为"在自身架构中封装小模型"的结构。具体而言，通过对大模型进行特殊的蒸馏微调，使其前若干层（称为base layers）的输出与小模型对应层的输出对齐，同时中间若干层的特征表示与小模型的完整推理结果对齐。这样，大模型在执行推理时，其内部就同时包含了小模型的完整推理路径——大模型的前向传播过程中，早期层的输出即可作为小模型的等效推理结果使用。

基于这种重构，MFS构建了统一多层服务流水线。流水线分为三个层级：Layer 1（base tier）执行大模型的早期层计算，产生API向量（中间特征表示），这些向量被缓存后可供所有下游任务复用；Layer 2（small-model equivalent tier）基于Layer 1的输出，经过少量额外计算即可得到等价于小模型的完整推理结果——用户请求的小模型推理可在Layer 2完成而无需单独部署小模型GPU实例；Layer 3（full-model tier）对需要大模型完整能力的请求，继续执行大模型的剩余层计算。三层流水线支持高度并行的层级批处理：Layer 1的输出可同时被Layer 2（多个小模型等效请求）和Layer 3（大模型完整请求）消费，实现"一次计算，多次使用"。

系统还实现了模型间的中间特征共享和KV-Cache共享——当用户的连续请求在不同规模模型间切换时，已计算的中间层特征和KV Cache可被新请求的对应层直接复用。评估结果：端到端token生成延迟降低56.1%，GPU内存占用减少47.8%。MFS指出了一条极具前景的技术路线：用模型内部的层级结构替代外部多模型独立部署，从根本上消除模型家族服务的资源冗余。

### 技术线索与启示

- **Agent与LLM应用方向**：模型家族共享服务对Agent根据任务复杂度动态选择模型规模有直接实用价值。Agent框架（如AutoGen、CrewAI）中的router agent可基于MFS无缝地在不同"能力层级"间切换（简单工具调用→小模型等效层，复杂推理→大模型完整层），而无需启动不同的推理实例。
- **系统软件方向**：知识沉淀的模型重构方法是一种新颖的模型压缩/共享范式，介于传统的知识蒸馏和模型剪枝之间。其核心思想"让小模型成为大模型的子路径"可推广到多模态模型的家族服务——如让CLIP-Large的早期层同时服务CLIP-Base的推理请求。
- **数据密集型系统**：多层级特征和KV-Cache共享的设计思想可应用于其他多模型推理场景，如模型集成（ensemble）推理——多个模型的推理路径在早期层共享计算，减少重复的前向传播。

---

## 2.11 Eevee: Efficient Multimodal Serving via Module Multiplexing

**作者**：Zicong Hong, Yuyan Chen, Haoyue Zhang, et al.
**机构**：HKUST, Sun Yat-sen University, Xi'an Jiaotong University, MetaX
**发表信息**：EuroSys 2026

> **信息来源**：EuroSys 2026 会议论文集

### 技术概要

多模态大模型（如CLIP、BLIP-2、LLaVA、InternVL、GPT-4V）已成为AI服务的重要组成部分，其架构本质上是模块化的：一个视觉编码器（如ViT）提取图像特征，一个投影/对齐模块将视觉特征映射到语言空间，一个语言解码器（LLM）基于视觉+文本特征生成输出。这种模块化架构对现有LLM服务系统构成了深刻挑战——标准系统将多模态模型视为单一整体（monolithic），按统一的batch size顺序执行所有模块，忽视了不同模块之间的异构计算特性。

这种"整体编排"方式造成严重的GPU利用不足。视觉编码器（如ViT-Large）的输入为固定分辨率的图像patch序列，批处理时图像数量而非patch数量决定batch size——但图像数量通常远小于文本token数（一次请求1张图 vs 数百个文本token），导致视觉编码器阶段的batch size很小，GPU利用率低。更严重的是，当batch中某些请求仅需文本处理（无图像输入）时，视觉编码器在整个batch期间必须空转等待——因为系统无法在batch内对不同请求选择性地执行不同模块。反过来，语言解码器阶段可能出现相反的问题：文本token数量远多于图像patch，但GPU时间被视觉编码器拖慢的请求"搭便车"，长文本请求被短视觉请求的decode限制。

Eevee提出了模块复用（module multiplexing）这一新调度范式来彻底解决上述问题。其核心思想是不再按统一batch size顺序执行所有模块，而是在同一GPU上并发调度不同的模态特定模块，独立调整每个模块的批处理大小和资源分配。具体设计包括三个关键机制：(1) 模块级调度器：将多模态模型拆解为独立的可调度模块（视觉编码器、投影层、语言解码器等），每个模块拥有独立的请求队列，调度器根据模块各自的负载和数据特征独立决定batch size；(2) 细粒度GPU共享：利用CUDA MPS（Multi-Process Service）或CUDA Streams实现模块在GPU上的时间片共享和空间分区，不同模块的计算kernel在同一GPU上交错执行；(3) 跨模块流水线：当一个请求的视觉编码器完成后，其结果立即进入投影层队列，投影层完成后立即进入语言解码器队列，各模块之间以流水线方式并行处理不同阶段的请求，最大化GPU内的并行度和整体请求级吞吐。

在CLIP、BLIP、LLaVA、InternVL等多个主流多模态模型上的评估显示，Eevee的吞吐和GPU利用率均显著优于SOTA系统。Eevee的意义在于揭示了模块化AI服务的通用调度问题——任何由异构组件组成的AI模型（多模态、Mixture-of-Experts、模型集成）都面临类似的"统一batch效率低下"问题，模块复用提供了一种通用的解决方案。

### 技术线索与启示

- **Agent与LLM应用方向**：多模态Agent（视觉感知+语言推理+工具调用）的推理效率可通过模块复用显著提升。Agent系统中的多个处理模块（视觉理解、代码执行、工具响应解析）可借鉴Eevee的模块级独立调度思路，实现异构模块在有限GPU资源上的高效时分复用。
- **系统软件方向**：模块复用作为一种新调度范式可推广到其他多组件异构推理场景，如语音+语言的多模态服务、结构化数据查询+自然语言生成的混合服务等。其核心方法论——将异构计算模块的调度从"整体同步"变为"各自独立"——是通用的设计原则。
- **硬件-软件协同设计**：细粒度GPU共享的调度方法需要与GPU硬件的并行执行能力协同优化。Eevee需要细致考虑CUDA Stream间的资源共享冲突（如L2 Cache竞争、DRAM带宽争抢），未来GPU微架构若能提供模块级的计算/缓存隔离，将进一步提升模块复用的效率。

---

## 2.12 SAS: Sparse Attention Synthesizer for Efficient Language Model Inference

**作者**：Yuan Zhou, Shaojie Xiang, Lingfan Yu, et al.
**机构**：Amazon
**发表信息**：EuroSys 2026

> **信息来源**：EuroSys 2026 会议论文集

### 技术概要

Attention机制的计算复杂度随序列长度平方增长（O(n²)），是长上下文LLM推理（如处理128K token文档）的主要性能瓶颈。稀疏注意力（Sparse Attention）通过仅关注输入序列中的重要token子集来降低计算和内存需求，是缓解这一瓶颈的关键技术方向。近年来，学术界和工业界提出了多样化的稀疏注意力模式：静态模式（如滑动窗口Sliding Window、空洞窗口Dilated Window、全局+局部混合）基于固定的结构化规则选择关注token，实现简单但灵活性差；动态模式（如基于注意力分数的Top-K选择、基于聚类的Hash Attention）根据输入内容自适应选择关注token，准确度高但实现复杂、运行时开销大。实际应用中往往需要组合多种稀疏模式——例如前半层用静态滑动窗口捕获局部依赖，后半层用动态Top-K选择捕获长程关键信息——但实现这种组合需要手动编写复杂的CUDA kernel，且优化KV Cache管理（不同稀疏模式的缓存需求不同）极为繁琐。

SAS是稀疏注意力合成器（Sparse Attention Synthesizer），其核心思想是让用户以声明式方式描述稀疏注意力模式，系统自动生成优化的执行代码。SAS引入一组原语（primitives）来封装静态和动态稀疏注意力机制的基本操作——如window_mask（滑动窗口遮罩）、topk_select（按分数选择Top-K）、hash_bucket（哈希分桶）、global_token（全局token锚点）。用户通过逻辑运算符（AND、OR、NOT）和声明式函数组合这些原语，简洁表达复杂的复合注意力模式。例如，"前10层用滑动窗口+全局token，后10层用Top-128动态选择"可以表达为 `(layer < 10) → window(4096) OR global(4) | (layer >= 10) → topk(128)`。

SAS的另一关键创新是基于几何的模式分析器。不同稀疏模式对应不同的KV Cache需求：滑动窗口仅需最近K个token的Cache，Top-K选择需要存储所有token但仅访问部分，全局token的Cache永不淘汰。SAS的分析器从用户声明的模式中自动推导最小KV Cache大小（基于模式的空间覆盖范围的最紧上界），并自动生成对应的缓存管理函数（包括分配、淘汰、查找逻辑），消除了手动管理KV Cache的复杂性和出错可能。

系统支持NVIDIA GPU（CUDA）和AWS Trainium（Neuron SDK）两种后端。在NVIDIA GPU上，通过自动tuning的kernel合成实现token生成加速2.68-2.80倍；在AWS Trainium上，利用其脉动阵列架构的特性，加速1.39-10.87倍（长序列场景受益更大）。SAS展示了"声明式规范→自动代码生成"这一编译器/代码生成范式在深度学习系统优化中的强大潜力。

### 技术线索与启示

- **系统软件方向**：自动内核合成方法（从声明式规范生成优化内核）是编译器/代码生成的新范式，类似于Halide/TVM在图像处理和张量计算领域的成功。SAS将这一思想推广到注意力模式的组合优化，其"原语+组合子"的DSL设计方法可应用于其他需要灵活组合计算模式的领域。
- **Agent与LLM应用方向**：稀疏注意力可显著降低Agent长上下文推理的成本。Agent在处理多轮对话历史、知识库检索结果等长上下文时，不同对话轮次和信息源需要不同的注意力模式，SAS的声明式组合能力使Agent开发者可以方便地定制和实验不同的稀疏策略。
- **硬件-软件协同设计**：同一框架支持GPU和Trainium两种架构展示了硬件抽象层设计的重要性。SAS的pattern-compiler后端架构使得添加新硬件支持只需实现一组原语的硬件特化kernel，而无需修改上层的模式组合逻辑。

---

## 2.13 Scaling LLM Test-Time Compute with Mobile NPU on Smartphones

**作者**：Zixu Hao, Jianyu Wei, Tuowei Wang, et al.
**机构**：Tsinghua University, USTC, Microsoft Research, AIR Tsinghua
**发表信息**：EuroSys 2026

> **信息来源**：EuroSys 2026 会议论文集

### 技术概要

移动设备上的LLM部署面临着尖锐的"质量-成本"矛盾：小模型（如1-3B参数量）可以在手机NPU上流畅运行，但回答质量有限；大模型（7B+）质量高但内存和计算需求超出移动设备的资源预算。Apple Intelligence和Google Gemini Nano等商用方案选择了前者（设备端小模型+云端大模型fallback），但许多场景下用户期望纯端侧推理（隐私敏感、离线、低延迟要求）。OpenAI的o1/o3等推理模型展示了test-time compute scaling（测试时计算缩放）的巨大潜力——通过让模型在推理时进行更多计算（如链式思考、多路径采样、自洽性投票），小模型的回答质量可以大幅提升甚至匹配大模型。

本论文发现了一个被忽视的事实：移动NPU（如Qualcomm Hexagon、Apple Neural Engine）在典型LLM推理中存在着大量未利用的计算资源——特别是矩阵乘法单元的利用率远未达到峰值。这是因为标准LLM推理中的GEMM操作受内存带宽限制（memory-bound）而非计算限制（compute-bound）——权重从DRAM加载的速度跟不上矩阵乘法单元的计算速度，导致NPU的MAC阵列大量空闲等待。该论文的创新在于：将这些空闲的NPU计算能力用于test-time compute scaling，在不增加延迟感知的前提下提升小模型的回答质量。

系统实现需要克服两个关键技术挑战。第一，硬件感知分块量化：移动NPU的内存访问模式不同于GPU——通常支持通道量化（per-channel quantization）或张量量化（per-tensor quantization），但标准LLM的组量化（group quantization，如每128个权重共享一个缩放因子）与NPU的固定硬件数据通路不匹配。论文设计了硬件感知分块量化方案，将组量化的分组边界与NPU内存访问的对齐边界对齐，同时引入高效的混合精度GEMM内核在NPU上实现量化矩阵乘法，加速最高19.0倍。第二，基于查找表的Softmax和反量化：Softmax中的exp操作和量化中的反量化操作在NPU上缺乏原生硬件支持，论文使用预先计算的查找表（LUT）高效近似，Softmax加速2.2倍。

在Qualcomm Snapdragon平台上实现了完整的端到端推理系统。通过将空闲NPU算力用于并行执行test-time scaling策略（如生成多个候选回答并进行自洽性投票、扩展思考链长度），小模型可在不显著增加用户感知延迟的情况下匹配甚至超越更大模型的精度。

### 技术线索与启示

- **边缘计算与端侧部署**：利用NPU冗余计算能力做测试时缩放是端侧推理的新范式，本质上是一种"资源分时复用"策略——在推理的间隙（memory stall期间）利用NPU空闲算力进行额外的质量增强计算。这种"用空闲算力换质量"的思路可推广到端侧模型的动态量化、在线微调等场景。
- **硬件-软件协同设计**：硬件感知量化方案需要深入理解NPU内存层次，展示了端侧硬件优化的深度。移动NPU的设计目标通常偏向卷积运算而非Transformer，这使得LLM部署需要大量的软件适配工作。论文的分块量化对齐方法为解决类似的硬件-算法不匹配问题提供了方法论参考。
- **开放性问题与未来方向**：测试时缩放的精度-计算-延迟权衡在移动端有独特约束。移动端还需考虑功耗和散热限制——test-time scaling虽然可利用空闲NPU周期，但持续高负载可能导致芯片降频。未来的研究需要建立包含功耗约束的端侧test-time scaling优化模型。

---

## 2.14 TailorLLM: Collaborative End-Cloud Inference of Large and Small Language Models Based on Low-Rank Adaptation

**作者**：Zian Wang, Ziyi Wang, Haonan Jin, Jie Xing, Lanshan Zhang
**机构**：Beijing University of Posts and Telecommunications
**发表信息**：EuroSys 2026

> **信息来源**：EuroSys 2026 会议论文集

### 技术概要

LLM推理服务的规模化部署使云计算资源成本成为核心运营挑战。当数以百万计的用户同时使用AI助手时，将所有推理请求发送到云端大模型不仅增加延迟（网络往返），还产生巨大的GPU租赁成本。端-云协同推理（collaborative end-cloud inference）是业界关注的降低成本的方案：简单任务在设备端用小模型处理，复杂任务上传到云端大模型处理。但这一方案面临两个关键的技术难题：一是如何高效地在端侧维护个性化/任务特定的模型适配能力（LoRA矩阵），避免每次任务切换都需要从云端下载新的适配参数；二是如何决定哪些任务应该在端侧处理、哪些应该在云端处理——决策错误将导致要么延迟过高（复杂任务被发送到端侧小模型但结果不可用，需要二次云端推理），要么成本过高（简单任务被发送到云端浪费资源）。

TailorLLM是基于LoRA的任务级端-云协同推理方案。第一项核心创新是RFLoRA（Reconstruction-Free LoRA），将预训练参数解耦为"冷模块"（cold modules）和"热模块"（hot modules）：冷模块是预训练权重中与任务无关的通用语言知识（语法、常识等），在端侧和云端共享，仅需传输一次；热模块是任务特定的参数适配（如医疗问答的领域知识、代码生成的编程范式），以LoRA低秩矩阵的形式存储在端侧。通过这种解耦，将需要通过网络传输的可训练参数量降到最低，同时保持模型在各项任务上的性能。冷热模块的划分基于Fisher信息矩阵分析——预训练参数中Fisher信息值较低的维度（对任务损失不敏感）标记为冷模块，Fisher信息值高的维度标记为热模块。

第二项核心创新是AdapterMgr（Adapter Manager），基于模仿学习的LoRA矩阵动态替换策略。端侧设备上维护着一个有限的LoRA矩阵库（受设备存储容量限制），当用户的任务需求超出库的覆盖范围时，需要从云端加载新的LoRA矩阵。AdapterMgr使用模仿学习训练一个替换决策策略：以任务历史记录、LoRA库当前内容、设备状态（电量、网络、存储）为状态，以"替换哪个LoRA"或"发送到云端"为动作，通过模拟专家的最优决策（基于完整任务信息的事后分析）来训练策略。持续优化使得设备端LoRA库的内容始终覆盖用户最常见和最重要的任务。

相比基线方案，TailorLLM减少最高69.8%云资源消耗和62%推理延迟，同时保持高精度。该工作为端-云协同推理中的"任务路由"和"模型适配"两个关键问题提供了系统性的解决框架。

### 技术线索与启示

- **边缘计算与端侧部署**：端-云协同推理通过LoRA矩阵动态管理实现了计算卸载的新范式——不同于传统的"任务卸载"（task offloading），TailorLLM实现的是"能力卸载"（capability offloading）：只需传输小型LoRA矩阵即可赋予端侧模型特定任务能力，计算完全在端侧完成。这一思路对边缘计算有深远的架构启示。
- **Agent与LLM应用方向**：设备端LoRA库动态管理使Agent可根据任务类型本地化执行。Agent在处理用户请求时，可基于AdapterMgr的模仿学习策略自主决定：当前任务是否匹配本地LoRA能力（端侧执行，低延迟低成本）、是否需要加载新LoRA（端侧执行，但有加载延迟）、还是应该直接路由到云端（高延迟高成本但最可靠）。
- **云原生与分布式架构**：冷热模块解耦的思想可应用于云端的模型版本管理——将模型更新分解为不变的"冷基础"和可变的"热适配"，大幅减少模型更新的网络传输和存储开销。

---

## 2.15 TZ-LLM: Protecting On-Device Large Language Models with Arm TrustZone

**作者**：Xunjie Wang, Jiacheng Shi, Zihan Zhao, Yang Yu, Zhichao Hua, Jinyu Gu
**机构**：Shanghai Jiao Tong University
**发表信息**：EuroSys 2026

> **信息来源**：EuroSys 2026 会议论文集

### 技术概要

随着LLM向移动端部署的趋势加速（Apple Intelligence、Samsung Galaxy AI、端侧模型如Gemma 2B、Phi-3），一个紧迫的安全问题浮出水面：专有模型的权重参数存储在设备上，终端用户可能通过逆向工程、内存dump等手段窃取模型知识产权。与云端SaaS模型的API访问不同，设备端模型的所有参数都暴露给了拥有物理访问权限的攻击者。Arm TrustZone作为移动设备上广泛部署的TEE（Trusted Execution Environment），提供了硬件隔离的"安全世界"（Secure World），理论上可以保护模型参数不被"普通世界"（Normal World / REE）的攻击者访问。然而，在TrustZone中运行完整的LLM推理面临两个根本性挑战。

第一个挑战是TEE内存效率与推理速度困境。TrustZone的安全世界内存（Secure DRAM）通常非常有限（数MB到数十MB），远不足以容纳一个数十亿参数的LLM及其KV Cache。简单的解决方案是将模型参数全部加密存储在REE侧内存中，推理时按需解密加载到TEE内存——但这会导致每次推理都要通过REE进行大规模数据传输和解密，延迟极高。如果激进地将参数缓存在TEE内存中以加速后续推理，则内存不足；如果保守地不缓存、每次从REE侧解密加载，则推理速度无法接受。TZ-LLM的解决方案是流水线恢复（Pipeline Recovery）：利用LLM推理的确定性内存访问模式——注意力层按序列顺序访问KV Cache、FFN层按固定顺序访问权重矩阵——前瞻性地从REE侧预取即将需要的参数到TEE内存。通过将参数I/O、解密和TEE内存分配操作与GPU/NPU上的计算流水线化重叠，几乎完全隐藏了安全内存与REE内存之间的额外延迟。

第二个挑战是REE与TEE之间NPU的高效安全分时。现代移动NPU（如Qualcomm Hexagon）通常不具备完整的IOMMU/SMMU stage-2隔离能力，无法直接将NPU配置为仅由TEE使用。如果整个NPU在REE和TEE间切换（world switch），每次切换都需要保存/恢复NPU全部状态和重新初始化控制平面，开销巨大。TZ-LLM的协同驱动设计解决这一问题：在TEE中创建最小的数据平面NPU驱动（仅包含推理所需的DMA描述符提交和中断处理），而将复杂的控制平面（调度、电源管理、固件更新）留在REE侧。TEE侧驱动仅需在推理时提交数据平面任务到NPU，REE侧驱动继续正常管理NPU的控制平面——两个"世界"的驱动共享同一个NPU硬件但操作不同的功能层面。这一设计大幅减少了TEE的TCB（Trusted Computing Base），同时消除了NPU世界切换时的控制平面重初始化，因为控制平面从未被TEE接管。

在OpenHarmony OS和MLC-LLM框架上的实现评估显示，TTFT降低最高90.9%，解码速度提升23.2%。TZ-LLM为端侧LLM的TEE保护提供了实用的系统方案，其核心方法论——利用推理的确定性访问模式实现安全前提下的高效预取——对TEE内运行其他计算密集任务有普遍参考价值。

### 技术线索与启示

- **安全与可信计算**：TEE内LLM保护是端侧AI安全的重要方向。TZ-LLM的协同驱动设计通过"数据平面在TEE、控制平面在REE"的功能分离，在保证安全的前提下最大化了性能，同时减少了TCB。这种"功能分离+分层设计"的安全架构模式对任何需要在TEE中运行性能敏感应用的场景都有指导意义。
- **边缘计算与端侧部署**：NPU分时的安全设计为端侧多租户AI推理提供了安全基础——未来的手机可能需要同时运行多个AI服务（如Apple Intelligence的多个模型），不同模型有不同的安全需求和隔离要求，TZ-LLM的NPU分时方案展示了如何在单体NPU上实现安全的多租户共享。
- **系统软件方向**：流水线恢复+确定性访问预取的模式可应用于其他TEE内的计算密集任务。任何具有可预测内存访问模式的应用（如加密数据库的查询执行、安全视频转码的前后帧处理）都可以利用这种"预测-预取-流水线重叠"技术来克服TEE内存限制。

---

## 2.16 PARD: Enhancing Goodput for Inference Pipeline via Proactive Request Dropping

**作者**：Zhixin Zhao, Yitao Hu, Simin Chen, et al.
**机构**：Tianjin University, University of Texas at Dallas, Stevens Institute of Technology
**发表信息**：EuroSys 2026

> **信息来源**：EuroSys 2026 会议论文集

### 技术概要

DNN推理流水线（Inference Pipeline）是许多实时AI应用的核心架构——多个DNN模型串联（有时也包含分支和循环）形成处理管道，典型的例子包括视频分析流水线（目标检测→人体跟踪→行为识别→事件报告）、自动驾驶感知流水线（目标检测→深度估计→轨迹预测→碰撞预警）、以及多模态LLM流水线（语音识别→语义理解→知识检索→文本生成）。这些流水线具有严格的端到端延迟约束：自动驾驶的端到端延迟要求在100-200ms以内，实时视频分析要求在30fps帧间隔内完成。当系统负载超过流水线容量时（请求突发、复杂场景导致个别阶段耗时增加），部分请求不可避免地会超时——在截止时间之前无法完成所有阶段的处理。

现有系统采用被动丢弃策略（reactive dropping）应对超时：只有当请求在流水线中途已经超时（如在跟踪阶段检测到从开始到当前已超过总时间预算），才丢弃该请求并释放其占用的资源。这种"事后清理"模式存在致命的效率问题：在请求被正式判定为超时之前，它已经消耗了大量GPU/CPU计算资源和内存——前期阶段的推理工作全部浪费了。这些被浪费的资源本可以用于处理那些最终能够按时完成的有效请求，从而提升goodput（有效吞吐，即成功按时完成的请求吞吐量）。在高负载下，被动丢弃导致大量计算资源被"注定超时"的请求消耗，形成恶性循环：浪费资源→goodput下降→为维持SLO需要更多资源→更多请求高斯延→更多浪费。

PARD（Proactive Request Dropping）提出主动丢弃策略来打破这一恶性循环。其核心思想是：在请求实际超时之前，基于运行时信息预测其能否按时完成，对预测必将超时的请求提前丢弃，将节省的资源用于服务其他更有希望按时完成的请求。实现主动丢弃需要解决两个核心子问题。

第一，何时丢弃（when to drop）：PARD维护每个请求的"进度-时间"模型，追踪请求已完成的流水线阶段及各自耗时、当前剩余阶段及预估耗时、以及总剩余时间预算。当剩余预算不足以覆盖预估的剩余处理时间时（考虑安全边际），PARD触发主动丢弃。预估模型基于各流水线阶段的历史延迟分布和当前队列深度（排队请求数×平均每请求处理时间），并自适应更新以响应负载变化。关键在于平衡"过早丢弃"（丢弃了本可能按时完成的请求，false positive）和"过晚丢弃"（丢弃太迟节约不了多少资源，false negative）两种错误。PARD引入风险预算概念——越接近截止时间的请求，丢弃决策的false positive容忍度越低（即宁愿保留可能超时的请求，也不错过可能成功的请求）。

第二，丢弃哪些请求（which to drop）：当多个请求都面临超时风险时，需要决定优先保留哪些。PARD的自适应请求优先级机制综合考虑：(1) 剩余延迟预算——预算越紧的请求优先级越高（接近deadline的请求不应被丢弃）；(2) 已完成进度——已完成阶段越多、投入资源越多的请求优先级越高（保护已投入的计算）；(3) 负载强度——在高负载下，优先丢弃"重"请求（长序列、大分辨率图像），保留"轻"请求以维持goodput。

在64-GPU集群上的全面评估显示，PARD的goodput比SOTA被动丢弃方案高16%-176%，丢弃率（被丢弃请求占总请求比例）减少1.6-17倍，浪费计算资源（被丢弃请求消耗的GPU·时间）减少1.5-62倍。PARD展示了过载控制中"主动vs被动"的范式优势——与其等坏事发生再清理，不如提前预测并阻止坏事的发生。

### 技术线索与启示

- **系统软件方向**：主动丢弃策略是一种通用的过载保护机制，可应用于任何有延迟SLO的服务系统——不仅是推理流水线，还包括微服务链路、消息队列、流处理管道。PARD的核心贡献在于将过载控制从"事后清理"（reactive garbage collection）升级为"事前预防"（proactive admission control+early termination），这一方法论具有广泛的适用性。
- **性能工程与可观测性**：运行时信息驱动的丢弃决策需要准确的延迟预测能力。PARD的进度-时间模型本质上是一个轻量级的在线延迟预测器，其设计理念——用请求级别的剩余预算和阶段级别的历史延迟分布做预测——可推广到其他需要在线延迟保障的系统。
- **云原生与分布式架构**：自适应请求优先级对微服务链路中的过载保护有直接参考价值。在微服务架构中，一个请求穿越多个服务的处理类似于PARD的流水线模型，可在每个服务入口处植入主动丢弃逻辑：当判定请求剩余预算不足以完成剩余服务调用时，提前返回降级响应而非在全链路浪费资源。

---

# Part 3: LLM Applications & Agent

> 本部分涵盖2篇论文，涉及LLM Agent的云-边协同部署和操作系统接口革新。

---

## 3.1 AIMS: Cost-Efficient LLM-Based Agent Deployment in Hybrid Cloud-Edge Environments

**作者**：Shiyi Liu, Haiying Shen, Shuai Che, Mahdi Ghandi, Mingqin Li
**机构**：University of Virginia, Microsoft
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

基于大语言模型（LLM）的自主Agent正在成为AI应用的新范式——Agent通过"感知-推理-行动"循环，自主调用外部工具、检索知识和执行操作来完成复杂任务。然而，Agent的部署架构面临着尖锐的成本-性能矛盾：Agent工作流包含多样化计算需求——从简单的文本解析、工具API调用到复杂的多步推理和代码生成——这些子任务的计算复杂度、延迟敏感度和资源需求差异巨大。将所有Agent子任务统一部署到云端大模型虽然保证质量，但产生高昂的GPU成本，且网络往返延迟对交互式Agent应用（如实时对话助手、代码补全Agent）极为不利。反之，将所有子任务部署到边缘设备（如本地服务器、Workspace）虽然消除网络延迟，但边缘设备无法承载大模型的高内存和计算需求，复杂推理任务的回答质量大幅下降。

AIMS是一个面向混合云-边环境的成本高效LLM Agent部署框架。其核心设计是任务感知的分层调度架构：将Agent执行流程分解为多个可独立调度的子任务（reasoning tasks、tool-use tasks、response-generation tasks），对每个子任务进行计算需求分析（估算token长度、模型规模需求、延迟预算），然后动态决定子任务的执行位置。计算密集的深度推理子任务（如多跳逻辑推理、长文档分析）被调度到云端大模型以确保回答质量；轻量级子任务（如JSON解析、函数签名生成、简单文本格式化）直接在边缘设备上用小模型完成。框架维护一个端-云模型能力矩阵，记录不同模型在各类型子任务上的精度-延迟-成本特征，调度器基于此矩阵和当前系统负载（云GPU队列深度、边缘设备可用内存、网络延迟）做出联合调度决策。当边缘模型的输出置信度低于阈值时，框架自动将子任务升级（escalate）到云端大模型，通过这种fallback机制在成本和质量间取得平衡。AIMS还实现了跨子任务的状态共享——先序子任务的中间推理结果（如检索到的上下文摘要、工具调用返回的结构化数据）在云端和边缘之间高效传递，避免重复计算。

### 技术线索与启示

- **Agent与LLM应用方向**：Agent云-边分层部署是生产中的核心架构问题。AIMS的分层调度方法使Agent可根据子任务特征动态选择执行位置，为Agent框架（如LangGraph、AutoGen、CrewAI）提供系统级部署方案参考。
- **边缘计算与端侧部署**：Agent组件的边缘化部署减少网络往返延迟，显著提升交互体验。子任务级别（而非请求级别）的云-边划分使边缘设备承担更多有效工作，减少对持续云连接的依赖。
- **云原生与分布式架构**：任务感知的混合部署策略可推广到其他云-边协同AI应用场景，如视频分析流水线中的轻量目标检测在边缘、复杂场景理解在云端的分级处理模式。
- **性能工程与可观测性**：模型能力矩阵和子任务置信度评估为Agent系统的可观测性提供了新维度——开发者可追踪每个子任务的执行位置、置信度和升级次数，为系统调优提供数据支持。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 3.2 From Imperative to Declarative: Towards LLM-friendly OS Interfaces for Boosted Computer-Use Agents

**作者**：Yuan Wang, Mingyu Li, Haibo Chen
**机构**：Institute of Software CAS, Shanghai Jiao Tong University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

计算机使用Agent（Computer-Use Agents，如Claude Computer Use、OpenAI Operator、UI-TARS等）代表了AI系统从"理解世界"到"操作世界"的跨越——它们通过模拟人类的输入输出操作（移动鼠标、点击按钮、键盘输入、截屏理解）与图形用户界面和操作系统交互，完成文件管理、网页浏览、文档处理等复杂任务。然而，当前所有Computer-Use Agent都受困于一个根本性的界面不匹配问题：操作系统的接口是为了人类的手指和眼睛设计的（命令式、逐步式、视觉导向），而非为LLM的符号推理能力设计的。Agent必须通过多轮"观察屏幕→推断界面状态→模拟操作→观察结果"循环来完成任务，每一步都伴随OCR解析误差、界面布局歧义和操作粒度不匹配。一个人类只需说"把这份文档转成PDF发给团队"即可利用系统服务和自动化工作流，但Agent却需要逐一模拟点击菜单、选择选项、确认对话框等数十步操作，不仅效率低下还极易因界面微小变化而失败。

本文提出了根本性的范式转变：从命令式OS接口到声明式OS接口。核心贡献是声明式机器接口（Declarative Machine Interface，DMI）——一组专门为LLM Agent设计的操作系统API抽象层，让Agent可以直接以声明式意图而非逐步操作来表达需求。DMI涵盖多个系统能力域：文件操作（"将目录下所有Word文件转为PDF并归档"）、进程管理（"启动一个Python环境并安装依赖"）、网络配置（"在当前网络下开放一个HTTPS服务"）、系统信息查询（"列出当前所有GPU使用率"）。每个声明式API都包含输入约束规范（schema）、预期副作用说明（effects）和执行状态反馈（progress tracking），Agent通过自然语言描述意图，DMI的意图解析器将声明式描述映射到可执行的OS系统调用序列，同时利用OS自身的优化能力（如I/O调度、并行执行、错误恢复）高效完成执行计划。由于DMI的API语义是文件/进程/网络的系统级抽象而非GUI的像素级抽象，Agent可以跳过"观察→操作"的低效循环，将数十步的GUI模拟操作压缩到一次声明式API调用。评估显示，声明式接口显著减少Agent与OS的交互轮次，将复杂任务的完成时间降低了数倍，同时任务成功率因其对界面变化的不敏感性而大幅提升。

### 技术线索与启示

- **Agent与LLM应用方向**：OS接口设计应适配LLM的声明式推理能力，而非要求Agent模拟人类操作，这是基础性的设计哲学洞察。声明式接口使Agent的"计算机使用"从像素级GUI交互跨越到模型到系统调用的高效通道，为下一代Computer-Use Agent的架构设计指明了方向。
- **系统软件方向**：操作系统提供声明式API是一次范式革命。DMI的设计模式（意图解析-计划生成-执行监控）可扩展为操作系统的标准抽象层，类似POSIX定义了进程/文件API，DMI有望定义面向AI Agent的系统接口标准。
- **安全与可信计算**：声明式OS接口的安全性、权限管理和向后兼容是落地核心挑战。DMI需要在Agent意图的灵活表达和OS资源的安全访问之间建立精细的权限模型——Agent可以声明"读取哪些文件"但不能绕过文件系统权限检查。
- **开放性问题与未来方向**：DMI的意图解析需要处理模糊性和歧义性（"把文档发给大家"中的"大家"是谁？），需要结合上下文（Agent当前会话历史、用户的身份和权限、文件系统的当前状态）进行消歧。这一挑战将推动LLM+符号推理的混合系统设计。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

# Part 4: Model Serving & Diffusion

> 本部分涵盖3篇论文，涉及图像编辑服务加速、端到端模型服务自动化以及LLM常量折叠优化。

---

## 4.1 InstGenIE (FlashPS): Efficient Generative Image Editing with Mask-aware Caching and Scheduling

**作者**：Xiaoxiao Jiang, Suyi Li, Lingyun Yang, et al.
**机构**：Hong Kong University of Science and Technology, Alibaba Group
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

扩散模型（Diffusion Models）驱动的生成式图像编辑——用户通过文本描述指定编辑需求并用mask（掩码）划定编辑区域——已成为创意工具和视觉内容生产的关键技术。然而，这种基于扩散模型的图像编辑面临一个特殊的性能瓶颈：编辑任务天然具有空间稀疏性，即用户仅希望修改图像中的特定区域（mask内），而非mask区域的内容应当保持原样不变。现有的扩散模型推理服务系统忽视了这一稀疏性——它们将整张图像的所有像素区域等量齐观地送入扩散模型的每个去噪步骤，为mask外边不需要修改的像素浪费了大量计算。在批处理场景中这一问题更加严重：不同请求的mask位置和大小各不相同（有的mask覆盖人脸区域、有的覆盖背景区域、有的覆盖整个前景），但传统批处理要求所有请求以同一batch同步完成所有去噪步骤，mask小的请求被迫等待mask大的请求完成——就像短请求在长请求后面排队。

InstGenIE（又名FlashPS）利用mask引入的推理稀疏性实现了高效生成式图像编辑服务。系统的核心洞察是：扩散模型的去噪过程具有空间局部性——每个像素的去噪计算主要依赖其空间邻域的中间特征激活（activation），mask外像素的激活值在编辑前后保持不变，因此可以被安全地缓存和复用。基于这一洞察，InstGenIE设计了三项关键机制：(1) mask感知的激活缓存：在首次编辑时为非mask区域的中间层激活建立缓存（类似KV Cache但针对图像特征图），后续编辑步骤中直接复用这些缓存值，跳过非mask区域的前向传播计算；(2) 无气泡流水线：将缓存数据的加载操作（从GPU显存或NVMe SSD读取）与mask区域的去噪计算在CUDA stream级别进行重叠流水线化，确保计算单元不会因等待缓存加载而空闲；(3) 面向扩散模型的连续批处理（continuous batching）：不同于传统推理服务中batch内所有请求必须同步完成所有去噪步骤，InstGenIE允许mask小的请求提前完成并退出batch、新请求动态插入，保持GPU持续满负荷。评估结果显示，吞吐量提升最高3倍，请求延迟降低最高14.7倍，展示了利用任务稀疏性进行服务优化的巨大潜力。

### 技术线索与启示

- **系统软件方向**：mask感知的稀疏计算重用可推广到其他具有空间局部性的生成模型推理场景，如视频编辑中的时间-空间mask缓存、3D内容生成的体素区域稀疏处理等。
- **Agent与LLM应用方向**：高效图像编辑服务是视觉Agent的关键后端能力。Agent执行"修改这张图片中的背景颜色"等任务时，InstGenIE可大幅降低编辑延迟，提升Agent交互的实时性。
- **性能工程与可观测性**：扩散模型的连续批处理突破了传统batch需等待全部完成的限制，其"动态插入+提前退出"的调度模式可推广到其他变长推理工作负载（如变长序列的Transformer推理）。
- **硬件-软件协同设计**：激活缓存对GPU显存容量提出额外需求——缓存所有中间层激活可能消耗数GB显存。InstGenIE的NVMe SSD分层缓存策略暗示了未来AI服务系统中存储-计算协同设计的必要性。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 4.2 Automated End-to-End Model Serving with Cooperative Compilation and Scheduling

**作者**：Yikang Zhang, Junlong Chen, Wei Wang, Jia Liu, Nan Hu, Haipeng Dai
**机构**：Nanjing University, Hunan University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

深度学习模型从训练完成到部署为生产级推理服务需要经过两个高度耦合但传统上独立优化的阶段：编译优化（图优化、算子融合、内存规划、量化方案选择）和运行时调度（批处理策略、流水线并行度、GPU实例分配）。这两个阶段的决策存在深刻的相互依赖关系——编译阶段选择的图融合策略会改变算子的执行时间和内存占用模式，从而影响运行时批处理的最优batch size；反之，运行时调度中预期的请求到达率模式和SLO要求也应当指导编译阶段选择偏延迟优化还是偏吞吐优化的算子实现。当前业界实践中，编译优化（通常由TVM、Triton、TensorRT等工具链完成）和运行时调度（通常由Triton Inference Server、Ray Serve等完成）是由不同团队、使用不同工具独立进行的，缺乏协同优化——编译器在优化时不知道模型将面临怎样的运行时负载，调度器在选择策略时也无法利用编译器的内部性能模型信息。

本文提出了编译与调度的端到端协同优化框架，将两个阶段的决策空间联合搜索以实现全局最优的模型服务配置。框架的核心是分层联合搜索策略：第一层，在固定编译配置（算子融合方案、内存布局、量化精度）的前提下，使用贝叶斯优化探索运行时调度空间（batch size、GPU实例数、流水线深度），快速收敛到该编译配置下的最优调度参数；第二层，将第一层得到的最优调度性能作为该编译配置的评估分数反馈给编译级搜索器，驱动编译器探索图的替代优化策略；两个层级交替迭代，逐步逼近联合最优解。框架的一个关键工程创新是编译-运行时性能模型的桥接——编译器在生成优化图的同时导出细粒度的算子级性能模型（每个算子的延迟、内存占用、并行度特征），调度器基于这些模型进行精确的吞吐-延迟建模，无需在线profile即可预测不同调度参数的端到端性能。评估显示，协同优化相比独立优化（先编译后调度，或先调度后编译）提升10-30%吞吐量，并显著降低了工程师手动调参的工作量。

### 技术线索与启示

- **系统软件方向**：编译-调度协同优化框架可集成到TVM、Triton等主流编译框架和Triton Inference Server等推理服务引擎中，作为自动化部署的标准化组件。其分层搜索方法论同样适用于训练系统的编译-并行策略联合优化。
- **性能工程与可观测性**：编译导出的算子级性能模型为运行时调度提供了精确的先验信息，这种"编译时profil + 运行时决策"的二阶段范式可推广到其他需要编译-运行时协同的系统优化场景。
- **Agent与LLM应用方向**：Agent系统通常涉及多个不同模型（推理模型、工具调用模型、嵌入模型）的pipeline式调用，联合优化多个模型的编译和调度参数对端到端Agent延迟至关重要。
- **开放性问题与未来方向**：编译-调度协同的在线自适应是更进一步的挑战——当运行时负载模式发生漂移时，如何在不中断服务的情况下动态调整编译配置（如重新融合算子）仍是一个开放问题。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 4.3 LLMFolder: Revisiting Constant Folding in Large Language Models

**作者**：Gansen Hu, Zhaoguo Wang, Wei Huang, Jinglin Wei, Haibo Chen
**机构**：Shanghai Jiao Tong University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

常量折叠（Constant Folding）是传统编译器中一项基础优化技术——编译时识别并将常量表达式替换为其计算结果，从而消除运行时的冗余计算。例如，表达式 `3.14 * 2` 在编译时即可替换为 `6.28`，无需在运行时执行乘法。LLM推理的计算图中实际上存在大量类似的"准常量"机会：权重矩阵的元素在推理期间固定不变，许多基于权重的组合表达式在给定输入序列下可被静态确定。然而，现有LLM推理框架（如vLLM、TensorRT-LLM）将整个模型视为统一的计算图，未系统性地识别和折叠这些可预计算的子图——每次推理都重新计算相同的权重组合，浪费了宝贵的GPU算力和内存带宽。

LLMFolder将常量折叠这一经典编译器优化技术系统性地应用于LLM推理场景。其核心贡献是将常量折叠从传统的"常量表达式消除"扩展为"参数精简"（parameter reduction）——不仅消除冗余的运行时计算，更重要的是消除冗余的参数存储。LLMFolder的工作流程分为三个阶段：(1) 静态模式识别：通过对LLM计算图进行符号分析，识别出哪些算子（如LayerNorm的仿射变换参数、Attention的投射矩阵组合、FFN的门控-升维-降维三联矩阵）在给定模型权重后完全由常量参数构成；(2) 等价图变换：将被标识为常量的子图折叠为单一操作的预计算矩阵——例如，Attention层中QKV投影矩阵的串接操作可以在加载前折叠为一个大矩阵，LayerNorm的缩放和偏移可与前一层的线性变换合并为等效的单步变换；(3) 内存布局优化：折叠后的参数不再需要以原始多维张量的形式存储，可以采用更紧凑的线性存储格式，消除原始格式中的padding和对齐开销，进一步减少GPU显存占用。在保持模型输出tensor精度（浮点数值逐位一致）的前提下，LLMFolder显著减少了模型参数的GPU显存占用，并由于减少了访存次数和kernel调用次数而提升了推理吞吐。

### 技术线索与启示

- **系统软件方向**：将传统编译器优化应用到深度学习推理是回归基础的优化思路，展示了经典编译技术与现代AI系统的深度结合空间。LLMFolder的静态图分析方法可集成到MLIR、XLA等深度学习编译器框架中。
- **性能工程与可观测性**：识别LLM推理中的静态模式需要深入的算子级分析——哪些算子组合在数学上等价、哪些参数可以预合并、哪些内存布局可以简化。这种分析需要同时具备编译原理和深度学习计算图的知识。
- **硬件-软件协同设计**：参数精简不仅节省GPU显存，还由于减少了对HBM的访问次数而降低了显存带宽压力。在HBM带宽成为LLM推理瓶颈的背景下，这种"以计算换带宽"的优化方向与量化、稀疏化等技术互补。
- **开放性问题与未来方向**：更多传统编译器优化（如公共子表达式消除CSE、死代码消除DCE、循环展开、强度削弱）在LLM推理中的应用潜力尚未被充分挖掘。LLM计算图的特殊结构（长序列自回归、动态shape）对这些传统优化提出了新的适应需求。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---


---

# Part 5: Resource Management & Serverless

> 本部分涵盖11篇论文，涉及Serverless工作流管理、GPU资源调度、容器内存管理、成本分析以及跨云存储复制。

---

## 5.1 iRoute: Local Routing Table-based Workflow Management in Serverless Computing

**作者**：Yiming Li, Laiping Zhao, Zhiyuan Su, et al.
**机构**：Tianjin University, Tsinghua University, IEIT Systems, Inspur
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

Serverless计算平台（如AWS Step Functions、Azure Durable Functions）将复杂应用编排为函数工作流——一个有向无环图（DAG），节点是独立函数，边表示数据依赖和控制流。传统的Serverless工作流编排依赖中心化调度器：调度器维护完整的DAG状态，接收每个函数执行完成的信号，查找下游依赖已满足的函数，触发其执行，并管理函数间的数据传输。这种中心化架构在规模化部署中暴露出三个固有缺陷：(1) 中心化状态管理开销随工作流规模和并发数线性增长，调度器成为吞吐瓶颈；(2) 每次函数间数据传递需要经过中心存储（如S3/DynamoDB）中转，引入显著的序列化-网络传输-反序列化延迟；(3) 调度器故障或网络分区会导致整个工作流挂起，单点故障风险难以消除。

iRoute提出了一套基于本地路由表的去中心化工作流管理方案，完全消除中心化调度器的瓶颈。其核心设计是：每个函数实例在启动时从全局DAG描述中提取自身的本地路由表——一个紧凑的数据结构指定"当本函数执行完成后，输出应该发送到哪些下游函数"——类似于IP路由表中"目标地址→下一跳"的映射关系。函数执行完毕后，不向中心调度器报告，而是直接根据本地路由表将输出数据和执行状态推送到下游函数的输入队列。系统通过三个机制保证去中心化架构的正确性和效率：(1) 路由表预取与更新：函数实例在冷启动阶段从持久化存储（如DynamoDB）加载路由表，运行时通过轻量级gossip协议同步DAG拓扑变更（如动态分支、条件跳转）；(2) 状态本地化：每个函数实例维护仅与其直接相关的工作流局部状态（上游依赖计数、输出目标地址），而非全局DAG状态，将状态管理复杂度从O(|V|²)降到O(degree)；(3) 轻量级协调：对于需要汇聚多个上游输出的Join节点，使用分布式计数器而非中心化锁实现依赖跟踪，消除协调瓶颈。通过将路由功能从中心下沉到边缘，iRoute将工作流编排的吞吐限制从单个调度器实例扩展到整个函数集群的总容量。

### 技术线索与启示

- **云原生与分布式架构**：去中心化路由表思想可迁移到微服务编排场景——Service Mesh的sidecar代理可内嵌本地路由表，将微服务间的调用路由从中心化API Gateway下沉到每个sidecar，减少网络跳数和单点瓶颈。
- **系统软件方向**：本地状态+预取路由的设计模式适用于所有DAG执行引擎的性能优化，包括数据管道系统（如Spark/Dask的DAG调度器）和CI/CD流水线引擎。
- **Agent与LLM应用方向**：Agent多步骤工作流（如ReAct模式的"思考→行动→观察→思考"循环）可建模为动态DAG，每个Agent步骤作为函数节点，iRoute的去中心化路由可降低多Agent协作的编排延迟。
- **性能工程与可观测性**：去中心化架构下，分布式调试和可观测性（如追踪一个请求穿越多个函数实例的完整路径）比中心化架构更复杂，需要分布式追踪基础设施（如OpenTelemetry）的有力支持。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

---

## 5.2 Efficient Data Passing for Serverless Inference Workflows: A GPU-Centric Approach

**作者**：Hao Wu, Yaochen Liu, Minchen Yu, et al.
**机构**：HUST, CUHK-Shenzhen, TeleAI, HKUST
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

Serverless推理工作流将多个AI模型组织为流水线式函数图——例如，一个视觉问答流水线可能包括图像预处理函数 → ViT编码函数 → 文本嵌入函数 → LLM推理函数 → 结果后处理函数。当前主流Serverless平台（AWS Lambda、Google Cloud Functions）中，函数间的数据传递遵循"生产者写入外部存储 → 消费者从外部存储读取"的模式：前一个函数将中间结果（如图像特征tensor、KV Cache）序列化后写入S3或共享文件系统，后一个函数启动后从存储中加载并反序列化。然而在GPU推理场景下，这种CPU-存储中介的传递模式造成了严重的性能开销：GPU上计算出的中间数据（tensor）必须先拷贝到CPU内存再进行序列化和网络传输，接收端需要从CPU内存重新拷贝回GPU——两次CPU-GPU跨PCIe总线拷贝本身就消耗大量时间和带宽，对于KV Cache这类巨型中间数据（数百MB至数GB）这种开销更是成倍恶化。

本文提出了GPU中心的数据传递方案，从根本上消除CPU-GPU跨总线拷贝。核心设计是GPU内存池化与零拷贝共享：在多个Serverless函数之间维护一个统一的GPU显存池，函数产生的中间tensor直接保留在池中，不拷贝到CPU内存——下游函数直接以引用（指针）方式访问池中的tensor数据进行后续计算。系统通过三个关键机制实现高效流转：(1) GPU显存池管理器：将GPU显存划分为逻辑分区，为每个活跃的工作流分配专属的显存区域，函数执行完毕后显存区域不立即释放，而是标记为"待消费"等待下游函数读取；(2) 零拷贝跨函数引用传递：函数间传输的不再是数据本身，而是一个轻量级的描述符（tensor shape、dtype、显存偏移地址、引用计数），下游函数根据描述符直接在GPU上访问数据；(3) 显存感知的函数调度器：调度器在决定将下游函数调度到哪块GPU上时，优先选择已经持有上游数据的GPU实例，实现数据本地化计算——当上游函数的输出tensor恰好在下游函数被调度的GPU上时，数据传递延迟从毫秒级（跨GPU/NVLink/CPU）降为零。评估表明这一方案在推理工作流场景中显著降低了端到端延迟并提升了吞吐。

### 技术线索与启示

- **系统软件方向**：GPU内存池化和零拷贝共享可集成到Ray Serve、Triton Inference Server等推理服务框架中，作为标准的数据传递机制替代现有的protobuf序列化方案。
- **Agent与LLM应用方向**：多模型Agent pipeline（视觉理解→工具选择→推理→代码生成）的数据传递可直接受益于GPU内直接流转，消除KV Cache在不同Agent模块间的序列化开销。
- **硬件-软件协同设计**：GPU显存管理需与CUDA内存分配器（cudaMallocAsync、CUDA Virtual Memory Management API）深度协同，确保显存池化不会引入碎片化和额外管理开销。
- **云原生与分布式架构**：GPU中心的Serverless架构代表了Serverless从CPU中心到加速器中心的演进方向——未来Serverless平台需要原生支持GPU/TPU/NPU等加速器间的直接数据传递。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 5.3 DROPS: Managing Serverless Resource Pools in Microsoft Azure Functions

**作者**：Ahmed Alquraan, Abdelrahman Baba, Rafael Mendes, et al.
**机构**：University of Waterloo, Microsoft Research, Microsoft
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

冷启动延迟是Serverless计算自诞生以来最顽固的问题之一——当函数被调用时如果不存在"热"实例，平台需要分配VM/容器、加载运行时、初始化函数代码，这一过程可能需要数百毫秒甚至数秒，对延迟敏感应用（如API后端、实时数据处理）是致命的。几乎所有主流Serverless平台（AWS Lambda、Azure Functions、Google Cloud Functions）都采用预热池（warm pool）策略来缓解冷启动：维护一组预初始化的空闲容器，随时准备接收请求。然而，预热池管理面临经典的供需两难：预热池过小，请求高峰时冷启动率飙升；预热池过大，大量空闲容器白白占用内存和CPU，造成严重的资源浪费——在Azure Functions的生产规模下，哪怕仅仅过度预热5%的容器，累积的资源浪费也十分惊人。

DROPS是一套面向Azure Functions生产环境的智能预热池管理系统。核心贡献是三管齐下的资源管理策略：(1) 预测性扩缩（Predictive Scaling）：基于历史函数调用数据（调用频率的时间序列、每周周期性模式、突发性特征）训练轻量级预测模型，提前扩充或收缩预热池——例如，在工作日上午9点（历史高峰前30分钟）开始扩充预热池，在凌晨3点收缩到最低水位；(2) 容器复用与分级池：对预热池进行热度分级——hot tier（毫秒级就绪）存放最近使用过的高频函数容器，warm tier（秒级就绪）存放中等频率函数容器，cold storage（仅保留容器镜像）存放低频函数——根据函数的实际调用热度在不同级别间自动迁移，最大化池内每个容器的"被命中概率"；(3) 细粒度资源分配：不同于传统的"一个容器一个函数"固定映射，DROPS允许同一容器在函数空闲期间被轻度复用于其他同runtime的函数初始化（通过容器内函数代码热替换），进一步提升资源利用率。通过在生产数据的trace-driven模拟中验证，DROPS在保持低冷启动率的同时显著减少了预热池的资源浪费。

### 技术线索与启示

- **云原生与分布式架构**：预热池管理是Serverless平台的核心工程问题，DROPS的分级池和预测扩缩策略可集成到Knative、OpenFaaS等开源Serverless框架中。
- **性能工程与可观测性**：预热池的实时监控和自动调优需要细粒度的容器生命周期可观测性——包括容器创建/销毁时间、函数冷启动耗时、池命中率、资源利用率等关键指标。
- **绿色计算与可持续性**：减少过度预热的资源浪费直接降低数据中心能耗。DROPS通过将"用后即焚"的Serverless模型与智能池化结合，在按需付费和资源效率之间找到了更好的平衡点。
- **Agent与LLM应用方向**：Agent平台的函数/工具调用也面临类似的冷启动问题——如按需加载工具定义、初始化代码解释器等。DROPS的分级池策略可应用于Agent工具的懒加载和预热管理。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 5.4 Squeezy: Rapid VM Memory Reclamation for Serverless Functions

**作者**：Orestis Lagkas Nikolos, Chloe Alverti, et al.
**机构**：National Technical University of Athens, UIUC
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

Serverless函数的典型生命周期是"执行→完成→释放"，但在VM/容器层面，函数执行完毕后内存并不立即归还操作系统——Linux的内存回收（memory reclamation）依赖惰性的页面回收守护进程（kswapd）和直接回收（direct reclaim），这两个机制的触发时机粗糙且回收速度慢（以秒为单位），与被Hundred毫秒级调度的Serverless函数完全不匹配。当一台物理服务器上运行着数百个Serverless函数实例时，已完成的函数白白占用大量内存，导致活跃函数因内存不足而触发频繁的页面换入/换出（swap）甚至OOM Killer，严重影响整体性能和吞吐。这种"僵尸内存"问题已成为Serverless平台GPU/CPU密度提升的关键瓶颈。

Squeezy提出了面向Serverless场景的快速VM/容器内存回收方案，将内存回收从操作系统的惰性被动回收转变为函数生命周期驱动的主动快速回收。核心设计包括三个层面：(1) 主动内存压缩（proactive compression）：利用Linux内核的zswap/zram框架，在函数执行完毕后立即将其内存页压缩到内存压缩池，而非等待换出到慢速的SSD/HDD swap空间——内存压缩/解压缩延迟在微秒量级，远低于磁盘I/O的毫秒级延迟；(2) 页面级精准回收：通过跟踪每个函数实例的页表映射关系，精确识别哪些物理页面完全属于已完成的函数（而非与其他活跃函数共享的页面），对这些"孤儿页面"进行定向回收，避免误伤活跃函数的页面；(3) 内存使用模式在线学习：训练轻量级时间序列模型预测每个函数的下次调用时间和峰值内存需求，基于预测结果决定回收时机和回收激进程度——如果预测函数将在200ms内被再次调用，则保留其内存；如果预测间隔超过5秒，则激进回收。Squeezy在函数执行完毕后的亚毫秒时间内即可启动回收，回收速度提升一个数量级以上，使Serverless平台可以在同一物理服务器上安全地容纳更多函数实例。

### 技术线索与启示

- **系统软件方向**：快速内存回收机制可直接应用于容器运行时（containerd、CRI-O等）和轻量级VM（Firecracker、gVisor等）的内存管理，提升容器密度。主动压缩+预测回收的组合策略对Kubernetes集群中的burstable workload同样有效。
- **云原生与分布式架构**：Serverless平台内存超卖（oversubscription）策略可借助快速回收实现更激进的资源复用——回收越快，超卖比例可以越高，单位硬件成本越低。
- **性能工程与可观测性**：内存使用模式的在线预测为资源管理提供了数据驱动决策基础。函数的内存行为通常具有高度可预测性（同一函数每次调用的内存峰值相近），这使得轻量级模型就能达到很好的预测精度。
- **绿色计算与可持续性**：更高的内存密度意味着用更少的物理服务器服务更多的函数实例，直接减少数据中心硬件规模和能耗。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 5.5 Demystifying Serverless Costs on Public Platforms

**作者**：Changyuan Lin, Yuanzhi Ma, Mohammad Shahrad
**机构**：University of British Columbia, Johns Hopkins University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

公有云Serverless平台的计费模型看似简单透明——AWS Lambda按请求次数和执行时长（GB-秒）计费，Azure Functions按执行时间和内存分配计费——但在实际运营中，用户发现"纸面计费"和"实际成本"之间存在显著差距。这种差距的来源是什么？不同云平台之间是否存在系统性差异？底层架构（如VM vs 容器、不同hypervisor、不同OS调度器）是否通过隐藏的机制放大了用户感知成本？这些问题直接关系到企业的云支出优化决策，但在学术文献中缺乏系统性的实证研究和量化分析。

本文通过大规模测量研究对主流公有云Serverless平台（AWS Lambda、Azure Functions、Google Cloud Functions）的成本构成进行了系统性的解剖。研究方法论涵盖三个维度：(1) 计费时间 vs. 实际资源消耗：通过精确定时测量（利用函数内部的高精度时钟和外部监控）量化计费时长与实际计算时长的偏差——揭示了初始化开销（冷启动时不计费但消耗实际资源）、计费粒度的四舍五入效应（AWS Lambda按1ms粒度计费但实际向上取整）、以及"计费wall clock"与"CPU wall clock"的差异；(2) 架构层隐藏开销：通过对不同平台的事件触发延迟、网络接入延迟、存储I/O延迟的解构量化，揭示了哪些开销被隐藏在了看似统一的"执行时长"计费模型中——例如，一次看似100ms的函数调用可能实际包含了20ms的API Gateway路由延迟（用户感知但不计费）、80ms的函数执行（计费），而80ms中又有15ms是平台内部的数据序列化/反序列化开销；(3) OS调度对执行时间的放大效应：通过在同一平台上比较相同代码在不同负载密度下的执行时间分布，量化了CPU时间窃取（steal time）、NUMA远端内存访问以及并发函数间资源竞争对计费时长的实际放大比例。研究揭示了令人深思的成本结构——计费时间与实际资源消耗之间存在系统性的不一致，提示行业需要更加精细透明的计费模型。

### 技术线索与启示

- **云原生与分布式架构**：成本透明化是用户选型和架构决策的关键。该研究提供的成本解构方法论可帮助企业在多云策略中做出更精确的TCO分析。
- **性能工程与可观测性**：OS调度对Serverless执行时间的放大效应（特别是CPU steal time和cache竞争）提示开发者和平台方都需关注底层调度行为，而非仅关注应用层优化。
- **开放性问题与未来方向**：Serverless计费模型精细化是行业演进方向——从粗糙的"GB-秒"模式走向"按实际CPU周期+实际内存占用+实际I/O操作"的多维计费，将更公平地反映资源消耗，但也需要平台提供更细粒度的资源度量基础设施。
- **绿色计算与可持续性**：计费模型的设计会反向塑造用户行为——如果计费模型过度鼓励短函数（按请求次数计费），用户可能将任务拆分成过于细碎的函数调用，反而增加整体资源开销。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 5.6 Fix: Externalizing Network I/O in Serverless Computing

**作者**：Yuhan Deng, Akshay Srivatsan, Sebastian Ingino, et al.
**机构**：Stanford University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

Serverless函数的"按执行时长计费"模型在遇到网络I/O时暴露出一处根本性的经济不合理：当函数调用外部API、查询数据库或下载文件时，函数线程被阻塞等待网络响应，但这段时间被完整计入计费时长——用户实际上在为"等待网络"付费。以一个典型的AI Agent函数为例：函数调用OpenAI API处理用户请求，API响应平均耗时2秒，函数实际计算时间仅200ms——但用户被收取了2.2秒的执行费用，其中90%的时间是在空闲等待。更糟的是，阻塞等待期间函数实例的CPU和内存被空闲占用但不能服务其他请求，整个平台的资源利用率和吞吐也受到拖累。传统的异步编程模型（async/await、callback）在语言层面解决了并发问题，但在Serverless平台上仍需一个运行的函数实例来"await"——不能将等待成本降为零。

Fix提出了一个根本性的解决方案：将网络I/O从Serverless函数的执行上下文中完全外置（externalize）到独立的I/O Worker进程。其工作流程如下：函数执行到网络I/O调用点时，不发起阻塞或异步等待，而是将I/O请求（HTTP URL、请求参数、回调函数标识）提交给同主机的I/O Worker守护进程，然后自身立即结束执行并释放所有资源（CPU、内存）——计费时钟在此刻停止。I/O Worker在后台异步完成网络请求，获得响应后将结果连同回调信息发送到Serverless平台的事件总线（如AWS EventBridge），平台触发一个新的函数实例（或复用热实例）从断点继续执行——这个过程类似于操作系统层面的"I/O线程让出CPU→I/O完成中断→唤醒线程"，但粒度是函数级而非线程级。这要求平台运行时支持检查点/恢复（checkpoint/restore）或者函数被设计为可分段执行（将"请求API→处理结果"拆分为两个独立函数，由Fix自动编排），Fix为开发者透明地管理这种分段。评估显示，这一方案显著缩短了函数的实际计费时长，降低了用户成本的同时提升了平台的整体函数吞吐量。

### 技术线索与启示

- **系统软件方向**：I/O外置+异步回调的模式可集成到AWS Lambda、Azure Functions等主流平台的运行时中，作为对现有async/await模型的平台级升级——将"语言级异步"升级为"平台级异步"。
- **Agent与LLM应用方向**：Agent调用外部工具（搜索引擎、代码解释器、API）时的等待可借鉴I/O外置思想：Agent发起工具调用后释放LLM推理资源，工具返回结果后再恢复Agent执行，避免昂贵的GPU实例在工具调用期间空闲等待。
- **云原生与分布式架构**：I/O外置与Serverless按需计费模型天然契合——按实际计算时间而非等待时间付费，使得Serverless的成本优势扩展到了I/O密集型工作负载。
- **安全与可信计算**：I/O Worker需要处理函数的敏感网络请求（包括API密钥、用户数据），其安全隔离和审计是生产化的重要前提。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 5.7 Bridging the GPU Utilization Gap: Predictive Multi-Dimensional Resource Scheduling

**作者**：Yilei Lu, Dongbiao He, Teng Ma, et al.
**机构**：Tsinghua University, Alibaba Group, Shanghai Jiao Tong University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

GPU集群的调度器（如Kubernetes GPU scheduler、YARN GPU extension）通常采用单维度资源模型——仅将GPU视为一个不可分割的"整卡"资源，通过简单的计数（每个节点有N张GPU卡、每张卡分配给一个作业）进行调度。然而，这种粗糙模型严重低估了GPU资源的多维耦合特征：一个GPU作业的实际资源占用不仅包括SM（流多处理器）计算能力，还包括显存容量、PCIe带宽（用于与CPU/存储传输数据）、NVLink/NVSwitch带宽（用于多GPU间通信）、以及L2 Cache共享——这些资源维度之间存在复杂的耦合和竞争关系。例如，一个仅占用30% SM计算的推理作业可能因为大batch size消耗了90%的显存，导致同GPU上虽然SM还有70%空闲却无法调度另一个作业；一个通信密集的分布式训练作业可能不消耗太多SM，但独占NVLink带宽导致共置的推理作业的KV Cache跨GPU访问延迟飙升。这种多维资源的隐式耦合导致实际GPU利用率远低于理论上限。

本文提出了预测性多维GPU资源调度框架，将调度决策从单维度GPU计数升级为多维资源联合匹配。核心设计包括两个模块：(1) 工作负载特征预测器：在作业提交时通过分析其计算图或少量profiling运行，预测该作业在各资源维度的消耗模式——包括SM利用率曲线、显存占用峰值、PCIe带宽需求（如KV Cache加载模式）、NVLink通信模式（如all-reduce频率和数据量）——生成一个多维资源需求向量；(2) 多维拓扑感知调度器：维护集群中每个GPU节点的多维资源状态图谱（包括各资源维度的当前占用量、剩余容量、拓扑亲和性），将作业的多维需求向量与节点状态图谱进行匹配，寻找使所有维度资源利用率均衡且无竞争冲突的节点-作业配对。调度器还内置了干扰模型——基于历史共置数据的回归分析，预测特定作业组合在共置时各维度的性能干扰程度，主动避免"有毒组合"（如两个NVLink密集作业不应共置在同一NVSwitch域内）。在生产GPU集群的trace驱动评估中，该调度方案显著提升了GPU的综合利用率和作业吞吐。

### 技术线索与启示

- **云原生与分布式架构**：多维资源调度可直接集成到Kubernetes GPU调度器（如GPU device plugin + extended resources）、Volcano等批调度框架中，替代现有的一维GPU计数模型。
- **性能工程与可观测性**：GPU多维资源的实时监控（SM利用率、显存带宽、NVLink吞吐、PCIe吞吐）和干扰检测是实现多维调度的数据基础——需要与DCGM、Prometheus GPU exporter等监控工具深度集成。
- **硬件-软件协同设计**：NVLink拓扑感知调度需要精确理解GPU集群的物理互联拓扑（如DGX节点的NVSwitch全互联 vs. PCIe-based的多GPU节点），这要求调度器与硬件拓扑信息的标准化接口。
- **Agent与LLM应用方向**：Agent的多模型混合调用（推理模型、嵌入模型、重排序模型）具有不同的多维资源特征——预测性调度可优化这种异构模型的GPU资源分配。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 5.8 Untangling GPU Power Consumption: Job-Level Inference in Cloud Shared Settings

**作者**：Pierre Jacquet, Maxime Agusti, Eddy Caron, et al.
**机构**：École de technologie supérieure, Inria, OVHcloud, CNRS
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

随着AI工作负载成为数据中心能耗的主要增长驱动力，GPU功耗管理已成为云运营商和用户的共同关切。然而，当前GPU功耗监控存在一个关键的粒度缺陷：数据中心仅能在节点级别（整台GPU服务器的总功耗）或GPU整卡级别（通过nvidia-smi读取）测量功耗，当一台GPU上同时运行多个作业时（MIG多实例GPU、MPS多进程服务、或vGPU），无法区分每个作业分别消耗了多少电量。这在共享GPU环境下——如多个推理服务共置在同一GPU上、一个训练作业和多个推理作业共享GPU——造成了"功耗归因困境"：云运营商无法准确核算各租户的碳排放责任，也无法识别和消除"功耗热点"作业；同时研究人员缺乏作业级数据来理解和优化GPU共享的能效特征。

本文提出了从节点级功耗到作业级功耗的解耦推断方法。核心思路是利用GPU硬件性能计数器（Performance Counters）——这些计数器存在于所有现代GPU中，记录着SM活动周期数、DRAM读写字节数、PCIe传输字节数、L2 Cache命中率等底层硬件事件——这些事件与功耗存在物理因果关系但关系复杂且非线形（如DRAM access的功耗系数与频率、温度、电压相关）。论文的训练方法是：首先在独占GPU场景下（仅运行单一作业，已知其功耗=整卡功耗），采集大量作业的性能计数器特征和对应的整卡功耗数据，训练一个轻量级ML模型（如梯度提升树或小型神经网络）学习从性能计数器到功耗的映射函数；然后在共享GPU场景下，对每个共置作业分别采集其性能计数器数据，通过训练好的模型推断每个作业对总功耗的贡献比例。由于GPU的功耗管理硬件（如动态电压频率调整DVFS）对整卡统一生效，功耗在不同作业间的分配是近似线性的——使用基于性能计数器活动比例的线性分解即可获得足够准确的功耗归属。评估显示推断误差低于10%，并发现了一个有启发性的结果：GPU共享对小AI工作负载（推理服务、小模型训练）的综合能效高于独占GPU。这一发现为"共享GPU以提高能效"提供了数据支撑。

### 技术线索与启示

- **绿色计算与可持续性**：作业级功耗归因是实现精细化能耗管理和碳排放核算（如Scope 2和Scope 3碳排放分配）的基础。云运营商可基于此向租户提供"碳账单"，推动AI产业向绿色计算转型。
- **性能工程与可观测性**：基于性能计数器的轻量级功耗推断方法论可推广到其他加速器（TPU、NPU、FPGA），只要这些硬件提供等效的性能事件计数器。
- **云原生与分布式架构**：功耗感知调度器可基于作业级功耗数据做能效优化调度——将功耗密集的作业分布到不同GPU以避免局部热累积，将对功耗敏感但计算轻的作业与功耗不敏感的作业共置。
- **经济与市场机制**：作业级功耗数据为建立GPU碳排放交易市场或内部碳定价提供了计量基础，使得"用AI的碳成本"从隐性变为显性。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 5.9 In-Production Characterization of an Open Source Serverless Platform

**作者**：Nima Nasiri, Nalin Munshi, Simon D Moser, et al.
**机构**：University of British Columbia, IBM
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

开源Serverless平台（如基于Knative+Serving的开源方案、OpenFaaS、Apache OpenWhisk）被视为避免云厂商锁定的关键替代方案，越来越多的企业和研究机构将开源Serverless部署到私有数据中心和混合云环境。但关于开源Serverless平台在生产环境中的真实表现，现有文献几乎完全空白——学术界已有的Serverless特征研究（如Serverless in the Wild、Azure Functions traces等）无一例外地聚焦于商业公有云平台，其结论（如冷启动延迟的分布、函数执行时间模式、内存使用行为）是否适用于开源平台的私有化部署？开源平台在哪些方面优于商业平台、在哪些方面存在差距？这些问题对于规划开源Serverless生产和指导平台改进至关重要。

本文对生产环境中部署的开源Serverless平台进行了系统性的长期（持续数月）特征分析，涵盖多个维度的量化指标：(1) 函数级分析：函数执行时间的分布特征（P50/P95/P99、短函数vs长函数的比例）、调用频率的模式（每日周期性和突发性模式）、函数间调用链的长度分布；(2) 平台级分析：冷启动延迟的分位数分布和触发原因（容器创建、镜像拉取、运行时初始化各阶段贡献多少）、预热池命中率的时序变化、自动扩缩器（如Knative的KPA/HPA）的响应延迟和过度扩缩比例；(3) 资源效率分析：CPU/内存的实际利用率 vs. 配置值（用户倾向于为函数分配过多的"安全余量"内存导致严重浪费）、节点级别的函数密度和资源碎片化程度。通过与已知的公有云Serverless特征数据进行对比，论文揭示了开源平台与商业平台的关键差异——例如，开源平台的冷启动延迟在某些场景下可优于商业平台（无多租户干扰），但在自动扩缩的响应速度上落后于商业平台的专有基础设施。基于这些发现，论文提出了一组针对性优化建议，涵盖Knative配置参数调优、容器镜像分层策略和预热池热度预测等方向。

### 技术线索与启示

- **云原生与分布式架构**：开源Serverless平台的特征分析可指导Knative、OpenFaaS等平台的默认配置和最佳实践（如revision保留策略、minScale/maxScale参数设定），降低生产部署的试错成本。
- **性能工程与可观测性**：生产环境长期测量是系统优化的基础方法论。该论文提供的特征分析方法论（需要长时间窗口、多维度指标、跨平台比较）可作为其他系统性能审计的参考模板。
- **开放性问题与未来方向**：开源Serverless在多租户隔离（一个恶意函数不应影响同节点其他函数）、自动扩缩的预测精度和成本效益方面仍有较大的提升空间，这些是学术研究和工业改进的活跃方向。
- **数据密集型系统**：函数调用链分析揭示了Serverless工作流在开源平台上的实际拓扑特征，这一数据对工作流调度器（如iRoute）的设计有直接参考价值。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 5.10 Serverless Replication of Object Storage across Multi-Vendor Clouds and Regions

**作者**：Junyi Shu, Xiaolong Huang, Gang Huang, et al.
**机构**：Peking University, UCLA
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

多云架构（Multi-Cloud）正在成为企业IT战略的主流选择——将数据和应用分布到多个云厂商（AWS+Azure+GCP）可以避免单一厂商锁定、降低区域性故障风险并利用各厂商的差异化优势（如某厂商在特定区域的价格更低或延迟更优）。然而，多云架构的一个基本挑战是跨云数据复制：如何将某个云厂商的对象存储（如AWS S3）中的数据低延迟、低成本地复制到另一个厂商的对象存储（如Azure Blob Storage）？传统方案依赖专用数据传输通道（如AWS DataSync、跨云专线）或自建复制中间件服务器——前者的成本高且灵活性差，后者需要管理和维护持续运行的服务器集群，违背了Serverless"按需使用"的哲学。

本文提出利用各云厂商的Serverless函数作为跨云对象存储复制的执行单元，实现完全按需的、事件驱动的跨云数据复制方案。其架构设计的关键洞察是：跨云数据复制天然匹配Serverless的事件触发和按需付费模型——数据复制是偶发的（当新对象写入时触发）、计算轻量的（主要是数据搬运而非重计算）、且复制量高度可变（突发的数据写入vs长时间的静默），这些都是Serverless最适合的工作负载特征。系统工作流程如下：(1) 源云的对象存储配置事件通知（如S3 Event Notification），当有新对象写入时自动触发该云上的复制函数（一个轻量级Serverless函数）；(2) 复制函数计算对象的增量变化（通过对比元数据版本或checksum），仅传输变化的字节而非全量对象；(3) 复制函数通过各云厂商的对象存储API将增量数据写入目标云的对象存储；(4) 冲突解决机制处理多写场景——当同一对象在多个云上被同时修改时，采用最后写入者胜出策略+应用层冲突标记（保留冲突版本的元数据供上层逻辑裁决）。通过利用Serverless函数的全球分布（在各云的区域就近部署），数据复制的网络路径最优；通过按需触发，完全消除了空闲服务器的成本。系统还实现了自适应传输优化：根据对象大小动态选择传输策略（小对象直接HTTP PUT，大对象通过分段并行上传），以及跨云传输的压缩和去重以进一步降低网络成本。

### 技术线索与启示

- **云原生与分布式架构**：Serverless驱动的跨云复制是多云数据管理的一项创新实践，其"事件驱动+按需执行"的设计模式可推广到其他跨云操作——如跨云数据库同步、跨云日志聚合、跨云模型权重分发等。
- **数据密集型系统**：增量同步和冲突解决机制对分布式数据库的多活复制（multi-active replication）有直接借鉴意义。特别是在弱一致性模型下如何用Serverless函数实现最终一致性复制。
- **开放性问题与未来方向**：跨云环境下的强一致性保证（如线性一致性复制）和Serverless函数执行的可靠性（确保复制函数至少执行一次）仍是核心挑战——这需要Serverless平台的exactly-once语义支持或应用层的幂等设计。
- **经济与市场机制**：利用Serverless做跨云复制的成本模型需要仔细分析——虽然省去了常驻服务器的费用，但跨云数据传输的出口流量费（egress cost）可能成为主要成本项，需要在数据放置策略中综合考虑。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 5.11 NADINO: Unleashing RDMA-capable DPUs in Multi-Tenant Serverless Clouds

**作者**：Shixiong Qi, Songyu Zhang, K. K. Ramakrishnan, et al.
**机构**：University of Kentucky, UC Riverside, HPE Labs
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

DPU（Data Processing Unit，如NVIDIA BlueField、Intel IPU）是近年来数据中心架构最重要的硬件创新之一——它将网络、存储和安全等基础设施任务从主机CPU卸载到专用的智能网卡上，使主机CPU可以专注于应用计算。在Serverless云场景中，DPU的潜力尤为突出：Serverless函数通常是短小且I/O密集的（频繁读写对象存储、调用其他服务、收发网络请求），将I/O处理卸载到DPU可以显著减少函数执行时间（因为减少了host CPU等待I/O的时间）。然而，当前Serverless平台对DPU的使用极度受限——通常仅将DPU当作普通的加速网卡使用，未发挥其可编程性和RDMA能力的真正价值，更未解决多租户环境下DPU资源的安全隔离和弹性分配问题。

NADINO释放了RDMA-capable DPU在Serverless多租户场景下的全部潜力。系统设计围绕三个核心创新：(1) DPU Native Data PlaNe Offloading（NDPNO）：将Serverless函数的关键数据平面操作——网络I/O（TCP/IP协议栈处理）、存储I/O（NVMe-oF initiator）、安全加密/解密——完全卸载到DPU的ARM核心和硬件加速器上，函数自身仅需通过轻量级API提交I/O请求到DPU，DPU通过RDMA直接访问远端存储和网络，绕过host CPU和host网络栈，实现接近裸金属的网络和存储性能；(2) 多租户DPU资源隔离：在DPU上实现多租户资源划分——每个租户的Serverless函数获得DPU上独立的网络命名空间、独立的加密密钥槽（避免密钥泄露）、独立的RDMA保护域（Protection Domain，防止跨租户内存访问），同时利用DPU的硬件QoS（Quality of Service）机制确保一个租户的大量I/O不会饿死其他租户；(3) 弹性DPU资源伸缩：Serverless平台可以根据函数实例的启动和销毁动态地在DPU上分配和回收资源槽——当一个新函数实例启动时，平台为该实例在DPU上创建一组虚拟I/O端点（Network Queue Pair + Storage Namespace + Crypto Session），函数实例销毁时立即回收，使DPU资源利用率与Serverless的弹性模型匹配。评估表明NADINO使Serverless函数获得与裸金属部署相当的网络吞吐和存储IOPS，同时保持了Serverless的多租户安全隔离。

### 技术线索与启示

- **硬件-软件协同设计**：DPU的真正价值在于多租户环境下的基础设施全卸载——不仅是网络加速，而是将网络、存储、安全三类I/O同时从host CPU卸载到DPU，使Serverless函数的计算效率和密度达到新水平。
- **云原生与分布式架构**：DPU+RDMA为Serverless提供了高性能网络和存储基础设施，使有状态Serverless函数（如需要低延迟访问共享数据或状态存储的函数）成为可能，扩展了Serverless的适用场景。
- **系统软件方向**：DPU上的多租户隔离和弹性资源管理需要一个全新的系统软件栈——类似于hypervisor之于VM，DPU需要"多租户DPU抽象层"来管理各个租户的虚拟I/O端点、密钥槽、QoS策略。
- **安全与可信计算**：DPU作为独立的安全域可以执行与host OS隔离的安全操作（如密钥管理、数据加密），这为Serverless的零信任安全架构提供了硬件基石——即使host OS被攻破，DPU上保护的密钥和加密通道仍然安全。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

# Part 6: Networking

> 本部分涵盖10篇论文，涉及负载均衡、拥塞控制、网络配置、可编程网络、RDMA优化以及跨数据中心路由。

---

## 6.1 REPS: Recycled Entropy Packet Spraying for Adaptive Load Balancing and Failure Mitigation

**作者**：Tommaso Bonato, Abdul Kabbani, et al.
**机构**：ETH Zürich, Microsoft, Sapienza University of Rome
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

数据中心网络的负载均衡策略长期在两种极端间摇摆：包级负载均衡（packet spraying）将同一流的每个数据包独立选择路径，能最优利用所有可用的网络路径但在接收端产生严重的乱序（out-of-order），乱序被TCP/RDMA误判为丢包而触发不必要的重传和拥塞控制回退；流级负载均衡（flow-level ECMP）将同一流的所有包固定到同一条路径，避免了乱序但哈希冲突导致某些路径过载而其他路径空闲——即"哈希极化"现象。在AI训练集群这样的高带宽低延迟环境中，这两个问题都极其致命：乱序导致RDMA的Go-Back-N重传浪费链路上大量带宽，而哈希极化使得某些链路在all-reduce关键时刻成为瓶颈。

REPS（Recycled Entropy Packet Spraying）提出了一种精巧的包级负载均衡方案，通过在网络边缘（源ToR交换机或NIC/FPGA）实施智能的路径选择和故障恢复，同时实现最优链路利用和受控乱序。其核心机制包括：(1) 回收熵（Recycled Entropy）：从数据包已有的头部字段（如IP ID、TCP序列号、RDMA PSN等）中提取随机熵，无需引入额外的per-packet状态，以此哈希选择路径，保证同一流的不同包在多数情况下均匀分布到所有可用路径；(2) 路径缓存与自适应：在FPGA/NIC上维护一个紧凑的路径状态表（per-connection <25字节），记录"当前表现良好的路径集合"，仅将包喷洒到这些高质量路径上，检测到某路径开始丢包或延迟飙升时立即从缓存中移除，避免了向拥塞路径继续发送数据；(3) 亚100微秒级故障恢复：当链路或交换机故障导致路径中断时，REPS在发送端检测到连续NACK（RDMA场景）或超时（TCP场景）后，仅需一次RTT即可切换到备用路径，无需等待路由协议收敛（通常需要数十到数百毫秒）。与传统的静态ECMP或纯随机包喷洒相比，REPS在最大化吞吐和最小化乱序之间找到了精巧的平衡点，并通过FPGA原型验证了线速实现的可行性。

### 技术线索与启示

- **系统软件方向**：去中心化逐包负载均衡适配下一代Ultra Ethernet标准（面向AI/HPC的下一代以太网协议），其核心思想"利用已有头部字段的熵+紧凑路径缓存"为无损RDMA网络的负载均衡提供了工程上可行的方案。
- **硬件-软件协同设计**：FPGA NIC实现验证了硬件加速复杂负载均衡逻辑的可行性——25字节per-connection的状态量在硬件上是可承受的，但CPU软件实现可能因频繁的查找开销而性能不足。
- **安全与可信计算**：100微秒级故障恢复为AI训练网络的韧性提供了关键保障——在大规模训练中，单链路故障若不能快速恢复，所有GPU的all-reduce将在几百毫秒内累积大量梯度不同步，可能导致训练需要回退数步甚至完全重启。
- **Agent与LLM应用方向**：在分布式LLM推理的KV Cache跨节点传输场景中，包级负载均衡可优化多路径网络中的Cache数据分发延迟。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 6.2 Learn-to-Probe: Signal Distinguishability in Congestion Control

**作者**：Han Tian, Wenbo Li, Junxue Zhang, et al.
**机构**：USTC, HKUST, Huawei
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

基于强化学习（RL）的拥塞控制算法（如Aurora、Orca、Gemini）近年来展现出超越传统启发式算法（如BBR、CUBIC）的潜力——RL Agent通过与环境交互自适应学习最优速率调节策略。然而，一个被长期忽视的根本性问题正在限制学习型CC的进一步发展：信号可区分性（Signal Distinguishability）。具体而言，拥塞控制Agent通过探测行为（如增加发送速率）来观察网络反馈信号（延迟变化、丢包、ECN标记），从中推断网络状态（可用带宽、缓冲队列深度）并做出决策。但当网络状态复杂（多个瓶颈链路、竞争流交错）或信号噪声高（延迟抖动大）时，不同网络状态可能产生几乎无法区分的信号模式——Agent无法确定当前的延迟上升是因为自己发送太快，还是因为其他流的突发流量，导致学习到的策略在一种状态下有效但在另一种不可区分的状态下失败。这种"信号混淆"是学习型CC在生产环境中表现不稳定的深层原因。

Learn-to-Probe（LTP）提出了信号可区分性导向的探测-学习框架，从根本上解决信号混淆问题。其设计包含两个关键创新：(1) 贝叶斯滤波状态估计：对抗噪声的首选武器——LTP维护网络状态的贝叶斯后验分布（而非点估计），每次收到新信号后用粒子滤波更新后验，将状态从"未知数"变为"概率分布"，Agent基于后验分布而非点估计做决策，天然对抗观测噪声；(2) 内在RL奖励鼓励区分布性探测：标准RL的奖励函数仅奖励性能目标（高吞吐+低延迟），LTP加入了一个"信号可区分性"内在奖励——当Agent采取的行动产生的信号序列具有高区分度时（即不同网络状态的后验分布间距离大），额外给予正向内在奖励。这个内在奖励驱动Agent主动生成"富含信息量"的探测行为——例如，在当前不确定性高的状态下，Agent会主动制造短时速率脉冲以暴露瓶颈容量——而非被动等待网络状态信号自然到达。通过将探测从"学习的附带品"升级为"学习的目标之一"，LTP的压缩决策在多种竞争场景下都更准确。

### 技术线索与启示

- **Agent与LLM应用方向**：贝叶斯滤波+内在奖励探测策略可迁移到Agent的环境探索和学习——Agent在不确定的环境中应主动生成信息丰富的行动，而非被动观察。这一思想对RL-based Agent的主动学习有启发价值。
- **系统软件方向**：信号可区分性分析方法论可应用于其他在线学习系统——如自适应视频流（网络带宽估计的信号混淆）、负载均衡器（后端延迟信号的混淆）、自动扩缩器（负载信号的混淆）等。
- **性能工程与可观测性**：主动探测为网络可观测性提供了一种"按需诊断"的新范式——在不确定性高时主动注入探测流量以澄清网络状态，在确定时减少探测开销。
- **开放性问题与未来方向**：内在奖励的权重如何在线自适应调整——在某些场景下过度追求信号可区分性可能造成不必要的带宽浪费，需要在"探索的信息价值"和"探索的带宽成本"间动态平衡。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 6.3 Canopy: Property-Driven Learning for Congestion Control

**作者**：Chenxi Yang, Divyanshu Saxena, et al.
**机构**：UT Austin, Google DeepMind
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

学习型系统的"可解释性"和"正确性保证"是阻碍其从学术原型走向生产部署的核心障碍，拥塞控制（CC）领域尤为突出。传统CC算法（如TCP Cubic、BBR）虽然性能非最优，但其行为可被形式化分析——在数学模型上可以证明它们在特定条件下"不会导致网络崩溃""不会饿死其他流""最终收敛到公平分配"。这些保证对运行在数十亿设备上的CC算法至关重要：一个偶尔行为异常的CC算法在互联网尺度上可能酿成大面积的网络灾难。然而，基于强化学习或神经网络的CC算法是完全的黑箱——没有形式化保证来说明它在worst-case输入（如极端竞争、恶意流量模式）下会做出什么决策，这也是为什么尽管学习型CC在受控实验中表现出色，但在实际互联网中几乎未见部署。

Canopy提出了属性驱动学习（Property-Driven Learning）来填补这一鸿沟：在训练拥塞控制RL Agent时，不仅优化传统的性能奖励（吞吐+延迟+丢包），还强制Agent满足一组形式化定义的"安全属性"。具体方法是将CC行为的关键安全属性——如"收敛性：最终所有竞争流获得公平速率分配""无饥饿：任何流的速率不会长期为零""稳定性：在网络稳定状态下发送速率不会持续振荡"——以时序逻辑（如Signal Temporal Logic, STL）形式化表达。训练过程中引入一个"定量认证器"（Quantitative Certifier）和一个"抽象解释器"（Abstract Interpreter）：定量认证器评估当前策略在满足各安全属性上的"满意度分数"（而非布尔值——0表示完全违反，1表示完全满足），使RL可以使用连续梯度优化；抽象解释器将连续的网络状态空间离散化为有限抽象状态并验证属性在抽象状态上的保持性——类似于经典的形式化验证中模型检查的思路但针对RL策略。RL训练时的损失函数由三部分组成：性能损失（传统RL目标）、安全属性违反损失（来自定量认证器的负奖励）、worst-case鲁棒性损失（基于抽象解释器的worst-case输入模拟）。最终的Controller在保持自适应性能优势的同时，具有worst-case可靠性保证——即无论网络环境如何变化，它都不会违反预设的安全属性。

### 技术线索与启示

- **安全与可信计算**：属性驱动学习为学习型系统提供了形式化安全保证的通用方法论——将安全需求写为形式化规范，在训练中强制满足而非事后验证。这一方法论可推广到自动驾驶、电网控制、医疗AI等所有对安全有严格要求的RL应用领域。
- **Agent与LLM应用方向**：形式化保证可应用于Agent行为约束和安全策略验证——例如，确保Agent在执行文件操作时不会删除系统关键文件（安全性属性），或确保Agent的API调用频率不超过速率限制（合规性属性）。
- **系统软件方向**：抽象解释器+定量认证器的架构可集成到RL训练框架（如RLlib、Stable-Baselines3）中作为安全层，为学习型系统组件（调度器、资源管理器、缓存策略等）提供正确性保证。
- **开放性问题与未来方向**：定量认证目前能处理的安全属性范围有限——复杂属性如"在多流动态加入/退出的场景下保持公平收敛"的状态空间太大，现有抽象解释技术难以在合理时间内完成验证。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 6.4 Concord: Learning Network Configuration Contracts

**作者**：Ryan Beckett, Francis Y. Yan, et al.
**机构**：Microsoft Research, UIUC
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

网络配置错误是公共云和大型企业网络服务中断的首要原因——一项经典研究表明，超过60%的网络故障是由配置变更直接或间接引发的。在一个拥有数十万网络设备的大型云网络中，配置工程师每天需要进行数百次BGP路由策略更新、ACL规则修改、VLAN/VXLAN变更——在如此复杂的配置空间中，即使经验丰富的工程师也可能在不经意间引入规则冲突、遗漏必要的route-map或错误配置AS Path过滤器。更致命的是，配置错误的影响往往是"沉默"的——网络在操作上仍然"正常工作"，直到特定流量模式触发隐藏的配置漏洞——而此时可能已过去数天，定位和回滚变得极为困难。

Concord引入了一种全新的配置防御范式：从历史正确配置中自动学习配置合约（Configuration Contracts），在新配置部署前自动进行合规检查。其核心思想是借鉴程序的"类型检查"——为网络配置定义一个"类型系统"。Concord离线分析数千份已被验证正确的历史配置快照，利用频繁模式挖掘和关联规则学习技术提取配置合约——形式化的约束规则，例如"每个BGP peer定义必须包含至少一个route-map引用""所有VLAN ID必须在已声明的范围内""ACL规则的deny语句只能出现在permit语句之后"等。这些合约定义了"什么是一个合法配置"的边界。在线阶段，任何新的配置变更提案在进入部署流水线之前，Concord自动解析配置语法树并检查所有合约规则的满足情况——如果发现违反，系统不仅报错，还给出修复建议（基于历史配置中类似情境下如何处理）。Concord还支持增量验证：对于大型配置变更，仅验证被修改的配置段所影响到的合约，而非全量重新检查所有合约。这一思想不仅适用于网络配置，对同样以YAML/JSON为主要配置语言的Kubernetes、Terraform等云原生工具链有直接的推广价值。

### 技术线索与启示

- **安全与可信计算**：自动学习配置合约提供了一种轻量级的"形式化验证替代方案"——虽然不能证明配置在所有场景下正确，但可以高效地阻止已知类型的错误配置。这种"经验驱动验证"的思想可推广到Kubernetes配置、Terraform IaC、CloudFormation模板等所有声明式配置系统。
- **云原生与分布式架构**：Kubernetes的YAML配置同样极易出错——错误配置RBAC权限可能导致安全漏洞、错误配置resource limits可能导致Pod OOM。Concord的学习合约机制可直接应用于Kubernetes admission webhook，在配置apply之前拦截错误。
- **性能工程与可观测性**：配置变更增量验证需要与CI/CD流水线深度集成——在Git PR合并之前自动运行Concord检查作为pre-merge gate，将配置错误拦截在代码审查阶段而非部署后的线上故障阶段。
- **Agent与LLM应用方向**：LLM Agent生成的配置（如Terraform脚本、K8s YAML）缺乏正确性保证，Concord可作为Agent配置输出的自动验证层，过滤LLM的幻觉性错误配置。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 6.5 PatternSketch: General and Runtime Reconfigurable Traffic Pattern Detection

**作者**：Yang Du, Dan Wang, He Huang, et al.
**机构**：Soochow University, NJUPT
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

网络流量模式检测（如DDoS攻击的前兆流量突增模式、端口扫描的固定间隔模式、C&C通信的信标模式）是网络安全和运维的基础能力。当前方案面临一个尖锐的灵活性-效率矛盾：基于软件的IDS/IPS方案灵活可编程但处理速率受限（Gbps级别），无法跟上数据中心Tbps级别的流量速率；基于硬件（可编程交换机如Tofino）的方案可达线速但受到交换机极有限的片上SRAM（数十KB至数MB）和简化指令集的严格约束，通常每种检测模式需要独占一个硬件sketch，且修改检测模式需要重新编译和部署交换机固件——这意味着网络安全团队无法快速响应新型攻击模式。

PatternSketch打破了这一矛盾，在单个轻量级硬件sketch中同时实现通用性（支持多种时序模式）、线速处理（Tofino全线速）、和运行时动态重配置（无需下线交换机）。核心技术是Pattern Automaton——一种统一的模式描述自动机，可以将多种时序流量模式（周期性、突增、渐变、多阶段等）统一编码为有限状态机的状态转移图，每个状态定义了时间窗口内的流量统计特征期望。在Tofino交换机上，Pattern Automaton被编译为数个流水线stage——每个stage在固定数量的SRAM表条目中存储部分自动机状态和中间匹配结果——通过流水线级联实现任意复杂度的模式匹配。评估显示仅需数十KB SRAM即可同时检测6种不同的时序模式，F1分数超过90%，且管理员可以在运行时通过控制平面API动态切换或更新检测模式，无需重启交换机或中断转发。PatternSketch展示了在严格硬件约束下，通过算法-架构协同设计实现"通用+高效+灵活"三者兼得的可能性。

### 技术线索与启示

- **系统软件方向**：单sketch多模式检测的架构思想可推广到日志分析、时序指标监控、APM异常检测等软件系统——用一个统一的数据结构替代多个专用检测器，降低维护复杂度。
- **Agent与LLM应用方向**：Agent行为异常检测（如异常频繁的工具调用、异常模式的文件访问）可借鉴PatternSketch的轻量级在线模式检测框架，在Agent运行时以低开销实时监控行为模式。
- **硬件-软件协同设计**：可编程交换机资源约束下的算法设计是软硬协同设计的典型案例——Pattern Automaton的流水线分解策略展示了如何将理论上不受限的自动机映射到物理上受限的流水线stage。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 6.6 Solar-NP: Rearchitecting Programmable Networks For In-Network Computing

**作者**：Haifeng Sun, Bing Liu, et al.
**机构**：Peking University, Huawei Cloud, Huawei, ICT CAS
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

网内计算（In-Network Computing）——在数据包穿越网络时由交换机或网卡对数据进行就地处理（如聚合、过滤、变换）——被视为突破分布式系统性能瓶颈的变革性技术。传统架构中，中间件（如消息队列、缓存、负载均衡器）是集中式瓶颈，而网内计算将这些功能分布到每个交换机的数据平面。然而，当前可编程网络的三大组件——芯片架构、编程语言、开发工具链——是各自独立演化的，缺乏全栈协同设计。这导致程序员需要用低层次的P4语言编写交换机逻辑，手动管理极其有限的硬件资源（表条目、ALU、寄存器），编程效率极低且极易引入资源耗尽或流水线冲突的错误。

Solar-NP提供了网内计算的全栈可编程方案，以系统性协同设计覆盖芯片-语言-工具链三个层面：(1) 芯片层：Solar-NP芯片采用RTC（Run-To-Completion）架构——与传统交换机的固定流水线不同，RTC允许数据包在片上灵活循环处理，数据平面表管理支持动态分配和回收表条目，层次化内存池（寄存器文件→SRAM→TCAM→HBM）提供不同延迟-容量梯度的存储选择，原子访问数据结构（如原子计数器、compare-and-swap队列）为分布式共识等高级网内计算原语提供硬件支持；(2) 语言层：NPC编程语言引入OAT（Operator Abstraction Tree）抽象——程序员以声明式方式描述数据处理的逻辑树（如filter→transform→aggregate→forward），编译器自动将OAT映射到RTC芯片的循环调度序列，隐藏硬件细节；(3) 工具链层：XuanWu工具链提供完整的开发-模拟-调试-部署工作流，包括周期精确的芯片模拟器、资源消耗预估器和性能分析器。Solar-NP的设计哲学是"让网内计算程序员像编写Spark/Flink作业一样编写交换机逻辑"，大幅降低开发门槛的同时系统性消除资源相关的编程错误。

### 技术线索与启示

- **硬件-软件协同设计**：全栈可编程网络是软硬协同设计的典范——从芯片微架构到编程模型再到工具链的一体化设计，每个层面都为"网内计算"这一核心场景优化，而非将通用芯片/语言/工具强行适配网络场景。
- **云原生与分布式架构**：网内计算可加速微服务间的数据聚合和过滤——在API Gateway或Service Mesh的sidecar代理处完成请求合并和响应缓存，消除集中式中间件的瓶颈。
- **系统软件方向**：高层网络编程语言（NPC+OAT）通过提高抽象层次降低了网络功能开发门槛，类似于CUDA将GPU编程从汇编级提升到C++级——这种"语言定义生态"的策略对任何新硬件平台都有借鉴意义。
- **Agent与LLM应用方向**：Agent间的大量数据交换（如多Agent共享知识库的分布式查询）可从网内计算中受益——数据在传输路径上的交换机节点处完成聚合和过滤，减少每个Agent的数据处理负担。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 6.7 Themis: Enabling Packet Spraying over Commodity RNICs

**作者**：Xiangzhou Liu, Wenxue Li, Zihao Wang, Kai Chen
**机构**：Hong Kong University of Science and Technology
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

大规模AI训练集群中的集合通信操作（如all-reduce、all-to-all）对网络的带宽利用率和延迟极为敏感——在数百至数千块GPU同步梯度时，任何一个通信bottleneck都会放大为全局wait时间。然而，RDMA over Converged Ethernet（RoCEv2）的ECMP（等价多路径）哈希路由与AI训练的通信模式存在根本性不匹配：ECMP基于五元组哈希将同一QP（Queue Pair）的所有数据包固定到同一路径上，而AI训练中少数大QP（如all-reduce的数据通道）占据了绝大多数带宽，导致哈希均匀但流量极度不均——承载大QP的路径拥塞而其他路径空闲。最直接的修复方案是包级喷洒（Packet Spraying）——将同一QP的包均匀喷洒到所有可用路径上以充分利用多路径带宽。然而，现有商品化RDMA网卡（RNIC）无法正确处理包喷洒引入的乱序：RNIC将乱序包误判为丢包，触发Go-Back-N重传和拥塞控制回退（DCQCN降速），反而严重劣化了性能。

Themis在可编程交换机层面以无侵入的方式解决这一问题，无需修改任何RNIC硬件或固件。其设计精巧地利用了RDMA协议的PSN（Packet Sequence Number）字段：(1) 源ToR交换机拦截来自发送端GPU的所有RDMA包，将每个包的PSN替换为精心计算的新PSN——按照包喷洒到不同路径的顺序分配连续的PSN值——使得目标ToR交换机接收到的包无论来自哪条物理路径，在PSN空间上都是有序的；(2) 目标ToR交换机在包到达时分析PSN连续性，对于确认真实丢失的包（基于超时而非乱序判断），才生成NACK回传给发送端；(3) 目标ToR过滤掉由乱序触发的"假NACK"——这些NACK是由于包通过不同路径到达的时延差异导致的，但数据包本身并未真正丢失，阻止无效NACK向发送端传播即可避免不必要的Go-Back-N重传和DCQCN降速。整个方案对发送端和接收端的RNIC完全透明——它们看到的仍是"正常"的RDMA流量。在真实测试床上，Allreduce和Alltoall完成时间分别减少15.6-75.3%和11.5-40.7%，展示了在商用硬件约束下以中间件实现高级网络功能的工程价值。

### 技术线索与启示

- **系统软件方向**：无需修改RNIC即可包喷洒的"交换机中间件"方案大幅降低部署门槛——没有硬件依赖性，可在现有数据中心交换机上通过固件升级部署，这是一种实用主义驱动的系统设计范式。
- **性能工程与可观测性**：AI训练通信优化对大规模训练效率有直接影响——对于千卡以上集群，Themis节省的通信时间可累积为显著的训练加速。
- **硬件-软件协同设计**：商用硬件约束下的系统设计是重要的工程方法论——Themis不假设"下一代RNIC会支持包喷洒"，而是在现有硬件的限制下通过可编程交换机的智能找到突破口。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 6.8 Practical and Scalable RDMA Connection Sharing for HPC Workload

**作者**：Yuejie Wang, Tuo Fang, et al.
**机构**：Peking University, Huawei
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

RDMA的可靠连接（RC）模式提供了最高的带宽利用率和最低的延迟——数据直接绕过OS内核在两台机器的用户态内存间DMA传输，是HPC和AI训练集群的事实通信标准。然而，RC模式要求通信双方在数据传输前建立专用的Queue Pair（QP）连接，每个连接在RNIC（RDMA网卡）内消耗宝贵的硬件资源：包括QP上下文Cache、内存翻译表（MTT）条目、完成队列（CQ）条目等。在大规模HPC系统中——如果有数百个节点，每个节点上的每个进程需要与所有其他进程通信——所需QP连接数量按O(N²)爆炸式增长，远超商品RNIC的硬件资源上限。当QP数量超过RNIC硬件容量时，RNIC被迫将QP上下文换入/换出（QP context thrashing），性能急剧下降。

本文提出了一套连接共享框架来从根本上解决QP爆炸问题。核心设计是双平面架构：(1) 零开销硬件辅助数据平面：利用RNIC的SRQ（Shared Receive Queue）和DCT（Dynamically Connected Transport）等高级特性，将一个物理QP在多个逻辑连接间时分复用——数据路径上的连接复用完全由RNIC硬件完成，不引入软件处理开销，保持高速数据通道的线速性能；(2) 轻量级细粒度控制平面：一个用户态守护进程根据通信模式（如MPI rank间的通信图、集合操作的通信拓扑）动态管理QP的分配和回收——将QP分配给当前最活跃的通信对、在通信模式变化时无感迁移QP的使用权。通过这种"硬件做数据路径、软件做控制决策"的分层设计，框架在不牺牲数据平面性能的前提下将可支持的逻辑连接数提升了多个数量级。

### 技术线索与启示

- **系统软件方向**：硬件辅助数据平面消除软件开销是RDMA优化的新范式——将性能关键的路径全部交由RNIC硬件处理，软件仅负责粗粒度的控制决策。这一范式对NVMe-oF、CXL等新兴互联技术同样适用。
- **云原生与分布式架构**：连接共享策略对Kubernetes集群中的大规模微服务RDMA通信同样有效，可降低Pod间通信的连接管理开销。
- **硬件-软件协同设计**：利用RDMA硬件特性（SRQ、DCT）做连接共享需要深入理解NIC固件行为——错误的复用策略可能触发固件的非预期降级模式。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 6.9 SmartNS: Enabling Line-rate and Flexible Network Stack with SmartNIC

**作者**：Xuzheng Chen, Jie Zhang, et al.
**机构**：Zhejiang University, Alibaba Cloud, Alibaba Group
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

现代数据中心正在将关键网络功能从主机CPU卸载到SmartNIC（如NVIDIA BlueField、Intel IPU、Marvell Octeon），以释放CPU资源给更有价值的工作负载。然而，SmartNIC卸载面临一个深层的架构矛盾：要实现线速（100Gbps/200Gbps）处理，网络栈路径上的每条指令都必须极度精简——这要求将网络功能固化为硬件加速的固定流水线（如DPDK+固定函数卸载）；要支持灵活的功能扩展（如自定义包头处理、动态协议解析、应用层路由），则需要可编程的软件实现——但通用CPU核心（即使是SmartNIC上的ARM核心）在网络数据路径上远无法达到线速。现有方案要么选择线速牺牲灵活性（硬件卸载），要么选择灵活性牺牲线速（软件DPDK），无法两全。

SmartNS在BlueField-3 SmartNIC上提出了一套精巧的混合网络栈架构，同时实现线速和灵活性。其设计哲学是"仅将数据路径中真正需要线速的部分卸载到硬件，其余保留在灵活的软件中"：(1) TX路径的头部卸载：SmartNS仅卸载发送路径的包头部构建（MAC/IP/UDP/RDMA头部封装）——这部分工作具有固定模式但极其高频，硬件处理可以轻松线速——而payload的处理（如加密、压缩）保留在软件中按需执行；(2) RX路径的无限工作集缓存内处理：SmartNS利用SmartNIC的板载DDR缓存了一个"无限"大小的工作集（如连接状态、流表、路由表），使得RX路径的查表操作全部在低延迟的板载内存中完成，避免访问慢速的host内存；(3) 纯DMA通知管道：SmartNIC与host CPU之间的控制和通知使用纯粹的DMA ring buffer，消除了中断和系统调用的开销——host CPU通过轮询ring获取完成通知；(4) 可编程卸载引擎：提供一个可编程的匹配-动作（match-action）引擎，允许用户定义自定义的包处理逻辑（如特定五元组的负载均衡规则），在硬件加速路径上执行。评估显示块存储解聚合（disaggregated block storage）吞吐提升2.2倍，分布式LLM推理中的KV Cache传输吞吐提升1.3倍。

### 技术线索与启示

- **硬件-软件协同设计**：SmartNIC中心网络栈是AI基础设施的重要方向——将网络处理从GPU host CPU卸载到SmartNIC，释放host的PCIe带宽和CPU周期给GPU训练/推理工作负载。
- **系统软件方向**：线速+灵活性的组合突破了传统SmartNIC卸载的设计限制——SmartNS证明不必要在"线速"和"灵活性"间做全有或全无的选择，而是可以对每个数据路径阶段做精细的权衡决策。
- **Agent与LLM应用方向**：高效网络栈直接提升分布式LLM推理中KV Cache跨节点传输的性能——在disaggregated inference（prefill和decode分离）架构中，KV Cache的传输带宽是端到端延迟的关键因子。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 6.10 LCMP: Distributed Long-Haul Cost-Aware Multi-Path Routing for Inter-DC RDMA

**作者**：Dong-Yang Yu, Yuchao Zhang, et al.
**机构**：BUPT, Peking University, Tsinghua University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

跨数据中心（Inter-DC）的RDMA将高性能远程内存访问从单个数据中心内部延伸到地理分布的数据中心之间，是构建全球分布式AI基础设施（如跨区域训练数据同步、全球模型副本一致性更新、多DC KV Cache池）的关键使能技术。然而，跨DC RDMA面临三个数据中心内RDMA不曾有过的独特挑战：(1) 路径不对称：由于ISP的BGP路由策略，从DC-A到DC-B和从DC-B到DC-A的广域网路径可能穿越完全不同的光纤和路由器，延迟和带宽严重不对称——NACK包可能走一条比数据包慢得多的路径；(2) 延迟拥塞信号：在数百毫秒的广域网延迟下，传统的拥塞信号（ECN标记）传回发送端已经过时——发送端基于200ms前的拥塞信息做出的速率调整在当前网络状态下大概率是错误的；(3) 路由碰撞：分布式路由选择（每个发送端独立选择路径）在多发送端场景下可能产生"羊群效应"——探测到某条路径空闲的多个发送端同时涌向该路径，瞬间将其塞满。

LCMP提出了一套分布式长距成本感知多路径路由方案来解决上述挑战。核心设计包含四个机制：(1) 路径质量评分：每个发送端维护所有可用路径的实时质量评分——综合考量延迟、丢包率、可用带宽、以及路径的每GB传输成本（不同ISP的广域网链路收费不同），基于评分选择路径而非简单轮询；(2) 交换机紧凑拥塞信号：利用沿途交换机在数据包头中嵌入紧凑的拥塞信息（几字节的队列深度编码），接收端收到后立即通过ACK反射回发送端，提供比端到端ECN更低延迟的拥塞反馈；(3) 过滤高成本候选：路由选择时主动排除成本过高或质量不稳定的路径（如丢包率超过阈值的路径），缩小候选集以提高决策质量；(4) 多样性保持哈希：在路径选择哈希中引入随机因子，防止多个发送端因独立评分趋同而选择相同的"最优"路径——即主动注入受控的多样性以分散流量，避免路由碰撞。在8数据中心测试床上，中位和尾部流完成时间（FCT）减慢分别降低76%和64%，展示了跨DC RDMA的性能可行性和成本效率。

### 技术线索与启示

- **系统软件方向**：跨DC RDMA路由是多云AI基础设施的关键组件——随着AI模型规模和数据规模的增长，单一数据中心的GPU容量和电力预算无法满足需求，跨DC分布式训练和推理将变得更加普遍。
- **云原生与分布式架构**：成本感知路由可集成到云网络管理平台（如跨云的SD-WAN控制器），使应用可以在性能、可靠性和成本三个维度间进行动态权衡。
- **开放性问题与未来方向**：长距RDMA的拥塞控制和可靠性保证仍有许多未解问题——在数百毫秒延迟下，传统的基于窗口或速率的拥塞控制算法在收敛速度和稳定性方面表现不佳，需要设计专门的"延迟鲁棒"拥塞控制算法。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

# Part 7: Storage & File Systems

> 本部分涵盖7篇论文，涉及分布式文件系统元数据、功耗自适应存储、TCO配置、存储压缩以及冷数据编码。

---

## 7.1 SwitchFS: Asynchronous Metadata Updates with In-Network Coordination

**作者**：Jingwei Xu, Mingkai Dong, et al.
**机构**：Shanghai Jiao Tong University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

分布式文件系统的元数据操作（如创建文件、重命名、修改权限）在提供强一致性保证时，通常需要同步写入：当多个客户端并发操作同一目录或文件时，元数据服务器必须串行化这些操作——通过锁和日志（WAL）确保操作的全序性和崩溃后可恢复性——再将结果同步写入持久化存储。这种同步写入模式造成了严重的写放大和延迟：一次简单的文件创建涉及WAL写入、元数据页面更新、索引更新至少三次独立的SSD写入，而锁竞争导致并发操作的吞吐受限。在AI训练场景中，大规模数据加载阶段可能触发每秒数百万次的文件打开/读取/关闭操作，元数据服务器的同步写入瓶颈会直接导致GPU因等待数据而处于饥饿状态。

SwitchFS提出了一种激进的架构创新：将元数据的协调逻辑从运行在CPU上的元数据服务器卸载到可编程交换机中，实现异步元数据更新。其关键洞察是：元数据冲突的检测和排序本质上是一种数据平面操作——可以表示为对键值对的匹配-动作规则——这与可编程交换机的硬件能力天然匹配。在SwitchFS中，文件系统的元数据操作被翻译为网络包中的键值操作请求，发送到可编程交换机（如Tofino）；交换机在数据平面（线速、超低延迟）完成冲突检测（检查同一路径上是否存在并发操作）和全局排序（为并发操作分配确定的序号），然后将排序结果通过包头部返回给节点。节点收到排序确认后，可以异步地将元数据变更追加到本地日志中——知道这些日志最终可以按交换机分配的序号合并为一致的状态——无需等待远程服务器的同步确认。元数据操作吞吐提升13.34倍，同时保持了线性一致性（linearizability）保证。SwitchFS的架构展示了"将分布式协调从软件层下沉到网络层"的巨大性能潜力。

### 技术线索与启示

- **系统软件方向**：网内协调思想可推广到分布式数据库的事务管理（将2PC协调卸载到交换机）、分布式锁服务（锁的申请-授予-释放由交换机数据平面完成）等依赖分布式协调的所有系统。
- **硬件-软件协同设计**：可编程交换机作为无状态的"协调层"展示了网内计算在系统基础设施中的工程价值——交换机不存储元数据（数据仍在节点上），仅负责协调（排序+冲突检测），这种"控制逻辑下推、数据留在边缘"的模式降低了交换机的存储需求。
- **性能工程与可观测性**：异步元数据更新的一致性验证需要细粒度的冲突检测——交换机上的冲突检测规则需要覆盖文件系统命名空间的所有并发操作类型（create-create、create-delete、rename-rename等），规则的完备性验证是一个开放挑战。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 7.2 MesaFS: An I/O-Efficient Metadata Service for Distributed File Systems

**作者**：Hao Guo, Jiwu Shu, Youyou Lu
**机构**：Tsinghua University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

分布式文件系统的元数据服务是影响整体性能的关键路径——几乎每次文件访问都以元数据查询或更新开始。当前元数据服务的持久化更新采用数据库风格的写前日志（WAL：Write-Ahead Logging）模式：先将操作记录追加写入日志文件（WAL），然后将修改反映到元数据页面（如inode table、dentry cache），再更新相关索引（如B-tree或LSM-tree的internal pages）。这种多阶段写入在SSD上造成严重的写放大（Write Amplification）——一次逻辑上的元数据更新可能触发三次物理SSD写入，严重消耗SSD的有限P/E周期（Program/Erase cycles）并降低元数据吞吐。在AI数据预处理和模型checkpoint等元数据密集的场景中，这一问题尤为严重。

MesaFS通过日志结构化存储（Log-Structured Storage）的重新设计实现了元数据更新的"单次SSD写入"——即一次元数据操作仅触发一次物理SSD写入。核心创新在于三个层面的协同设计：(1) 日志结构化存储：所有元数据更新以追加（append-only）方式写入日志段（log segment），日志段在内存中积累多个操作后批量写入SSD——一次物理写入承载多个逻辑操作——消除WAL+数据+索引的三阶段写入；(2) 批量合并：相邻或有因果关系的元数据操作在内存中被合并为等效的复合操作——例如，先创建文件再删除该文件的连续操作可以合并为无操作（no-op），三次连续的文件扩展可以合并为一次最终大小的扩展——减少实际需要持久化的操作数量；(3) 轻量级索引：用一个紧凑的内存跳表索引（Skip-List）维护日志段到元数据键的映射，避免传统LSM-tree的多级索引写入。崩溃一致性通过日志段的顺序写入和原子写入（Atomic Write Unit）特性保证：当日志段的写入在SSD的原子写入单元内完成时，要么全部持久化（成功），要么全部不持久化（崩溃后回滚），无需额外的校验和恢复逻辑。MesaFS在元数据密集负载下实现了接近设备物理极限的元数据吞吐量。

### 技术线索与启示

- **系统软件方向**：单次写入元数据更新的思想可推广到分布式数据库的元数据管理和键值存储引擎——用日志结构化+批量合并替代WAL+Data+Index三阶段写入是降低写放大的通用策略。
- **数据密集型系统**：元数据服务的I/O效率直接影响大规模文件系统的整体性能——在AI训练管道的I/O路径上，元数据操作可能成为hidden bottleneck（被数据读取的巨大时间掩盖，但在高并发场景下突然暴露）。
- **硬件-软件协同设计**：利用SSD的原子写入单元（Atomic Write Unit）特性来实现轻量级崩溃一致性，而非使用昂贵的校验和+fsync，是存储系统设计中利用硬件特性简化软件逻辑的典范。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 7.3 PASS: A Power Adaptive Storage Server

**作者**：Dedong Xie, Theano Stavrinos, et al.
**机构**：University of Washington, Databricks
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

数据中心存储服务器的一个被长期忽视的能耗问题是：存储设备（SSD、HDD）被设计为始终运行在最大功耗状态——HDD的主轴电机持续全速旋转、SSD的控制器始终全频率运行——无论实际负载如何。但在典型的生产工作负载中，存储服务器的平均利用率远低于峰值：根据大规模数据中心trace分析，平均IOPS利用率仅在15-30%之间，大部分时间存储设备处于"低负载等待"状态，但仍消耗着接近满载的电能。随着AI训练数据集的EB级增长和数据中心电力预算的日益紧张，存储功耗占数据中心总功耗的比例正在上升，存储功耗优化成为绿色数据中心的重要议题。

PASS（Power Adaptive Storage Server）提出了基于实时负载的自适应存储功耗管理方案。核心设计包含三个层面：(1) 功耗状态动态调整：根据实时I/O负载自动切换存储设备的功耗状态——当检测到负载进入低谷期（如预测到未来N秒内无密集I/O请求）时，将HDD置于spin-down模式（主轴停转）、将SSD置于低功耗ALPM（Active Link Power Management）模式；当负载回升时提前唤醒设备以避免首请求的高延迟惩罚；(2) 请求调度补偿：在设备处于低功耗状态期间，将到达的读请求通过缓存层（使用少量NVMe SSD作为热缓存）服务——如果命中则零延迟返回，如果未命中则唤醒设备并合并多个pending请求批量处理，将唤醒惩罚平摊到多个请求；(3) 缓存策略协同：根据工作负载的时序模式动态调整缓存策略——在可预测的低谷期间激进地预取可能被访问的数据到缓存，延长设备可保持低功耗状态的窗口。PASS实现了功耗-性能的动态平衡——在低负载场景下功耗节省显著，而在高负载高峰期间性能不受影响。

### 技术线索与启示

- **绿色计算与可持续性**：存储功耗自适应直接降低数据中心碳排放——在EB级数据中心的规模下，即使节省5%的存储功耗，其碳减排量也相当于数千家庭的年用电量。
- **系统软件方向**：功耗自适应调度可集成到Linux块设备层和文件系统层——作为I/O调度器的一个功耗感知扩展，类似于现有的cpuidle/cpufreq框架对CPU功耗的管理。
- **性能工程与可观测性**：功耗-性能平衡需要实时负载监控和准确功耗预测——过于激进的降功耗策略可能导致频繁的设备状态切换带来的延迟抖动。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 7.4 TCO-driven Storage Provisioning for Exascale Data Centers

**作者**：Timothy Kim, Saurabh Kadekodi, et al.
**机构**：Carnegie Mellon University, Google, Microsoft
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

EB级（Exabyte）数据中心存储配置（如何将总存储容量分配到不同性能和成本的存储层级上——如NVMe SSD热层、QLC SSD温层、HDD冷层、磁带归档层）是影响数据中心总拥有成本（TCO）的核心决策之一。当前行业实践严重依赖经验法则（rules of thumb）——如"20%热数据用SSD，80%冷数据用HDD"——这种粗糙的经验比例在不同工作负载（如AI训练数据访问、视频流媒体、数据库OLTP、冷备份）之间产生巨大的配置偏差：过度provisioning SSD造成成本浪费，SSD配备不足导致性能瓶颈。随着存储介质技术的快速多样化（SLC/MLC/TLC/QLC/PLC NAND、SMR/CMR HDD、磁带、光学存储等），手动制定最优存储层级配置的任务复杂度已超出人类专家能力。

本文提出了基于TCO驱动的存储配置模型，将存储配置决策建模为带约束的多目标优化问题。模型的输入包括：(1) 工作负载特征——访问频率分布（hot/warm/cold数据比例）、读写比率、I/O大小分布、延迟SLO要求；(2) 各存储介质的成本参数——每TB采购成本、每TB年化能耗成本、故障率和对应的维护成本（备件+人工）、数据迁移成本（层级间数据移动的带宽和时间开销）；(3) 组织约束——最小冗余度要求（3副本 vs EC编码）、增长速度预测（未来12个月的数据净增量）。模型输出最优的容量-层级分配方案，使在满足性能SLO的前提下总TCO（3-5年总成本净现值）最小化。这一模型验证了在Google和Microsoft生产trace上的有效性，显示可将存储总成本降低20-40%——相比经验法则的配置方案。更重要的是，该研究揭示了不同工作负载类型的最优配置呈现出截然不同的结构特征。

### 技术线索与启示

- **数据密集型系统**：TCO驱动存储配置是大规模数据管理的核心工程决策——不仅是技术决策，更是财务决策。该模型可作为数据中心规划的标准工具。
- **绿色计算与可持续性**：TCO优化推动冷数据向低能耗存储（HDD/磁带）迁移——能耗成本占TCO的比重随电力涨价而不断上升，TCO优化本身就具有减碳效应。
- **云原生与分布式架构**：TCO模型可扩展到云存储的自动分层策略优化——云存储服务（AWS S3 Intelligent-Tiering等）的自动分层策略可基于类似的成本模型进行优化。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 7.5 ASIC-based Compression Accelerators for Storage Systems

**作者**：Tao Lu, Jiapin Wang, et al.
**机构**：DapuStor Corporation
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

数据压缩是存储系统中平衡容量、性能和成本的关键技术——现代存储系统几乎在所有层级都依赖压缩：从SSD控制器内的透明压缩（transparent compression）到文件系统级的在线压缩（如ZFS compression）、再到数据仓库的列式压缩。当前压缩主要依赖CPU软件实现（如LZ4、ZSTD）或集成在SSD控制器内的小型硬件加速块——前者消耗大量CPU周期且延迟较高，后者受限于SSD控制器的有限硅面积仅支持轻量级算法。随着NVMe SSD的吞吐从GB/s迈向10+ GB/s，CPU端压缩已成为新的性能瓶颈——CPU花在压缩/解压缩上的时间甚至超过了实际数据传输时间。

本文对ASIC压缩加速器在存储系统中的应用进行了系统性的三维度研究：(1) ASIC设计：对比多种压缩算法（LZ4、ZSTD、Snappy、gzip）在ASIC实现中的面积-吞吐-功耗特征，揭示不同算法在硬件实现中的优劣——例如ZSTD在软件中最优但ASIC面积显著大于LZ4；(2) 放置策略：评估三种放置位置的性能-成本权衡——作为PCIe外围加速卡（最高灵活性但引入PCIe往返延迟）、作为SSD控制器片上块（最低延迟但面积受限需与FTL/NAND管理共享芯片面积）、作为存储内（in-storage）计算单元（接近NAND但需要处理NAND的异步特性）；(3) 性能profiling方法论：建立一套标准化的工作负载benchmark来评估压缩加速器在不同真实负载（数据库OLTP、对象存储、日志分析、AI数据管道）下的实际增益。研究揭示了ASIC压缩在不同放置策略下对不同工作负载的性能特征差异——这些洞察为存储系统设计者选择"是否需要ASIC压缩"以及"放在哪里"提供了系统性的决策框架。

### 技术线索与启示

- **硬件-软件协同设计**：ASIC压缩加速器的设计和放置策略需要软硬协同优化——硬件架构师需要软件侧的I/O路径分析来理解延迟约束，软件架构师需要理解硬件约束来设计合理的压缩卸载接口。
- **系统软件方向**：压缩加速器的集成需要与文件系统和块设备层的I/O路径深度协同——在I/O栈的哪一层插入压缩/解压缩操作对延迟有决定性影响（块设备层 vs 文件系统层 vs 应用层）。
- **性能工程与可观测性**：ASIC压缩profiling方法论可推广到其他硬件加速器（加密、纠错码、哈希）的性能评估，为数据中心基础设施的硬件投资决策提供数据基础。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 7.6 ColdCode: Cold Data Encoding for Enhanced Reliability and Lifetime in 3D NAND Flash

**作者**：Qiao Li, Shangyu Wu, et al.
**机构**：MBZUAI, Xiamen University, McGill University, Peking University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

3D NAND Flash的存储可靠性问题随着堆叠层数的增加（从64层到300+层）而不断恶化。其中，数据保持（Data Retention）问题——存储在浮动栅极（floating gate）或电荷陷阱（charge trap）中的电荷随时间缓慢泄漏，导致存储单元的阈值电压漂移和读取位错误——是影响Flash寿命和可靠性的首要因素。对于冷数据（写入后长时间不被访问或重写的数据），电荷泄漏的影响尤为严重：冷数据可能数月甚至数年不被刷新，泄漏累积的位错误逐渐逼近甚至超出标准ECC（Error Correction Code）的纠正能力。现有的ECC方案（如LDPC、BCH）设计为最坏情况——假设所有数据都经历最大强度的电荷泄漏——对所有数据页施加同等强度的错误保护，这导致两个问题：首先，热数据（频繁更新的数据）被"过度保护"——浪费了宝贵的ECC冗余位和编解码延迟；其次，冷数据的ECC保护强度可能在超长时间尺度下仍然不足。

ColdCode提出了"数据温度感知编码"——根据数据的访问/更新温度（hot/warm/cold）和Flash物理退化特性，为不同类型的数据设计不同的编码策略。核心设计包含三个层面：(1) 温度分级：基于数据的最后访问时间戳和更新频率，将数据分为Hot（<1小时）、Warm（1天-1周）、Cold（>1周）三级，每段使用不同强度的编码——Hot数据使用轻量级但低延迟的BCH编码（因为很快会被重写，电荷泄漏效应可忽略），Cold数据使用更强力的LDPC编码或RAID-like跨页奇偶校验；(2) Flash物理特性感知：编码设计考虑了3D NAND中不同层（layer）的物理差异——顶部和底部的存储单元因蚀刻工艺差异而具有不同的电荷泄漏速率——编码强度根据物理层位进行微调，而非一刀切；(3) 轻量级在线迁移：当数据从Hot降级为Warm或Cold时，系统在后台执行低优先级的重编码（从弱编码升级为强编码），迁移的CPU和I/O开销通过使用空闲时间片摊平。ColdCode在保持足够可靠性的同时，相比统一的强ECC方案，提高了编码效率（可用冗余位更多的用于存储用户数据）和有效存储容量。

### 技术线索与启示

- **系统软件方向**：数据温度感知编码的思想可推广到分布式存储系统的数据分层和编码选择——将温度维度的信息加入数据管理决策中，在冗余度、性能、容量之间做更精细的权衡。
- **硬件-软件协同设计**：Flash物理特性感知编码是存储介质与编码算法协同优化的典范——软件编码策略不能脱离硬件的物理退化模型，必须基于实测的层间泄漏速率差异进行校准。
- **绿色计算与可持续性**：提升Flash有效容量和寿命直接减少存储硬件更换频率——每延长一年SSD的服役寿命，就减少了一次制造新SSD的碳排放和原材料消耗。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 7.7 Omar: Scheduling Cloud Block Storage Proactively and Reactively

**作者**：Xinqi Chen, Weidong Zhang, et al.
**机构**：Shanghai Jiao Tong University, Alibaba Group, CUHK
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

云块存储（Cloud Block Storage，如AWS EBS、阿里云Disk）是虚拟机/容器持久化存储的基础设施，其I/O调度器负责在多个租户/磁盘间分配存储设备的带宽和IOPS资源。调度策略在"proactive"（预测式：根据预测的工作负载模式提前预留资源）和"reactive"（响应式：根据实时负载反馈动态调整资源分配）之间存在根本性的权衡：proactive调度能提前规划资源避免临时性的资源竞争，但预测错误时会导致严重的资源浪费（预留了资源却未被使用）和饥饿（未预留的资源需求被拒绝）；reactive调度能紧密跟随实时负载变化，但对突发负载的响应存在固有延迟——当检测到某租户的IOPS飙升时，调度器需要数十毫秒到数百毫秒来调整资源分配，调整完成前该租户的所有请求都在排队等待。在云块存储的多租户生产环境中（阿里云单集群服务数十万磁盘、数千租户），调度器的这两种模式的权衡被极度放大——尾延迟直接影响着关键业务（如数据库事务提交）的用户体验。

Omar提出了proactive-reactive混合调度方案，结合两者的优势同时规避各自的短板。核心设计是双引擎协同架构：(1) Proactive引擎：对每个租户的I/O负载进行在线时间序列预测（基于历史多日的周期模式+近期趋势），提前为预测的高负载时段预留存储带宽和IOPS——预测模型使用轻量级指数平滑+周期分解以保持低计算开销；(2) Reactive引擎：实时监控每个租户的实际负载与预测值的偏差，当偏差超过阈值时（如突发流量使实际IOPS超过预测值的2倍），触发快速响应机制——从系统预留的弹性资源池中临时调配额外资源给该租户；(3) 协同仲裁器：当proactive预留和reactive调配产生资源冲突时（即proactive已为租户A预留了带宽，reactive同时想为租户B调配更多带宽），仲裁器基于租户优先级、资源短缺度和历史公平性指标（max-min fairness）做出最终分配决策。在阿里云生产环境中的部署评估显示，尾延迟（P99.9）降低64%，同时资源利用率也有所提升（因为proactive预留减少了因竞争导致的空转等待）。

### 技术线索与启示

- **云原生与分布式架构**：proactive+reactive混合调度模式可广泛应用于Kubernetes存储卷调度、网络带宽分配、CPU时间片调度等所有需要对"预测规划"和"实时响应"进行平衡的资源管理场景。
- **性能工程与可观测性**：尾延迟优化需要准确的工作负载预测和实时的延迟监控——缺少任一维度，混合调度就会退化为纯proactive或纯reactive。
- **系统软件方向**：预测-响应协同框架可推广到其他需要同时利用历史知识和实时反馈的系统——如CDN的缓存预热策略、自动扩缩器的扩缩决策、负载均衡器的流量分发等。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

# Part 8: Security & Trusted Execution

> 本部分涵盖4篇论文，涉及安全容器架构、多租户Kubernetes、LLM完整性度量以及形式化方法工业实践。

---

## 8.1 SKernel: An Elastic and Efficient Secure Container System at Scale with a Split-Kernel Architecture

**作者**：Xiaohu Chai, Keyang Hu, Jianfeng Tan, et al.
**机构**：Tsinghua University, Ant Group, Shanghai Jiao Tong University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

安全容器技术在云计算中扮演着越来越重要的角色，但其在隔离性与弹性之间始终存在根本性矛盾。传统的安全容器方案（如Kata Containers、gVisor等）为了提供强隔离，往往需要为每个容器实例启动独立的轻量级虚拟机或独立内核，这导致启动延迟高、内存占用大，难以应对大规模集群中频繁的容器创建与销毁需求。此外，当容器需要弹性扩缩容时，传统架构中的内核资源无法在容器间动态共享，进一步加剧了资源浪费和弹性响应延迟。如何在保证安全隔离不低于虚拟机级别的前提下，同时实现接近原生容器的弹性扩展能力和资源利用效率，是大规模生产环境中安全容器落地的核心挑战。

SKernel提出了一种创新的分裂内核架构来解决上述困境。其核心设计思想是将传统单体内核拆分为两个协同运行的组件：可信微内核负责处理安全关键操作（如内存隔离、进程间通信、安全策略执行等），运行在最高特权级的可信执行环境中；功能内核则承载丰富的系统服务（如文件系统、网络协议栈等），运行在独立的隔离域内。两个内核组件通过经过严格形式化验证的通信接口进行交互，确保安全关键操作不会被非可信模块污染或绕过。该架构在蚂蚁集团的生产环境中进行了大规模部署验证，结果表明分裂内核设计在保持与虚拟机相当的安全隔离强度的同时，支持毫秒级的容器弹性扩展，且性能开销显著低于传统安全容器方案，为金融级安全容器提供了可工程化的参考架构。

### 技术线索与启示

- **安全与可信计算**：分裂内核架构是安全容器领域的创新设计范式，通过将安全关键功能与非关键功能进行物理隔离，为TEE和机密计算容器的设计提供了全新的思路——未来机密计算容器可借鉴分裂内核思想，将TPM、加密引擎等可信硬件驱动运行在微内核侧，通用服务运行在功能内核侧
- **系统软件方向**：微内核+功能内核的双核协作设计具有广泛的适用性，可应用于浏览器沙箱（将渲染引擎隔离在功能内核侧）、IoT边缘OS（将硬件控制逻辑运行在微内核侧）、以及自动驾驶中间件等需要高安全性与功能丰富性并存的应用场景
- **云原生与分布式架构**：弹性安全容器运行时可直接集成到Kubernetes生态中，作为新的容器运行时类别（如"split-kernel runtime"），为金融、政务等对安全隔离要求极高的多租户场景提供生产级解决方案
- **工业实践与组织考量**：论文提供了在蚂蚁集团大规模生产环境中部署分裂内核架构的实践经验，包括安全审计流程调整、运维监控体系适配以及开发者工具链改造等方面的经验教训，对计划在自身环境中引入安全容器技术的工程团队具有重要参考价值

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 8.2 Pyramid: A Secure, Resource-Efficient, and Pluggable Kubernetes for Multi-Tenancy

**作者**：Xiang Li, Weijie Liu, Fabing Li, et al.
**机构**：Tsinghua University, China Telecom eSurfing Cloud, Nankai University, Ant Group
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

Kubernetes已经成为云原生生态的事实标准编排平台，但在多租户场景下，如何在安全隔离与资源效率之间取得平衡是一个长期悬而未决的挑战。一方面，在公有云或企业内部共享集群中，不同租户的工作负载必须严格隔离以防止信息泄露和侧信道攻击，理想的安全方案是将每个租户的工作负载部署在独立TEE（可信执行环境）中；另一方面，TEE的引入带来了显著的资源开销——每个TEE实例需要独享加密内存、产生额外的加解密和完整性检查开销，导致集群资源利用率大幅下降。传统Kubernetes调度器对TEE的资源特性一无所知，使得TEE保护下的多租户集群往往面临资源严重碎片化的困境，CPU和内存的实际利用率远低于非安全场景。

Pyramid针对上述挑战提出了一套系统性的多租户Kubernetes安全增强方案。其核心创新包括三个层面：首先，TEE资源感知调度器能够精确感知每个节点上TEE可用内存、加密引擎吞吐等安全资源的状态，将需要安全隔离的Pod智能调度到最有空闲安全资源的节点上；其次，匿名化资源视图通过中间代理层隔离各租户对集群物理拓扑的感知，防止基于调度信息的侧信道推断攻击；第三，调度信息约束机制限制跨租户的调度元数据泄露面。在真实测试中，Pyramid的数据平面吞吐相比基线提升了1.4倍，展示了安全与效率兼得的可行性。此外，Pyramid采用可插拔架构设计，可通过适配器对接不同厂商的TEE实现（如Intel SGX、AMD SEV等），具有良好的硬件生态兼容性。

### 技术线索与启示

- **安全与可信计算**：TEE资源感知调度开创了安全-效率联合优化的新范式，突破了传统观念中"安全必然牺牲效率"的二元对立——这一思想可以推广到机密计算GPU调度、加密数据库资源管理等更广泛的安全敏感资源调度场景
- **云原生与分布式架构**：匿名化资源视图和调度信息约束机制可应用于所有多租户云平台（不仅限于Kubernetes），为多云管理平台、Serverless多租户平台等提供了通用的安全隔离设计模式
- **Agent与LLM应用方向**：随着Agent即服务（AaaS）模式的兴起，多租户Agent平台需要确保不同用户的Agent执行环境严格隔离——Pyramid的安全隔离架构可直接借鉴，为Agent托管平台提供租户级安全保障
- **工业实践与生态建设**：可插拔架构设计降低了不同TEE硬件厂商的适配门槛，有助于推动TEE在云原生场景中的大规模商业化落地，论文中与中国电信天翼云的合作验证了方案在运营商级多租户云平台中的实际可行性

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 8.3 TrustWeave: Integrity Measurement and Attestation For Multi-Cloud LLMs

**作者**：Jianchang Su, Wenhui Zhang, et al.
**机构**：University of Connecticut, Tsinghua University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

随着大型语言模型（LLM）在各行业关键业务中的广泛应用，越来越多的企业选择在多云环境中部署LLM推理服务以获取弹性、成本优化和供应商多样性。然而，多云部署模型引入了前所未有的安全挑战：模型文件（通常高达数十GB甚至上百GB）在不同云提供商之间传输和部署时，如何确保模型的完整性和真实性？推理代码是否被恶意篡改或植入后门？传统云计算中依赖硬件TEE（如Intel SGX）的完整性证明方案面临两大困境：一是TEE的加密内存大小远远不足以容纳完整的LLM模型参数，二是不同云提供商采用的TEE方案互不兼容，无法跨云建立统一的信任链。这使得多云LLM部署场景中存在一个安全真空地带——模型提供方和使用方都无法确信推理过程中模型和代码的完整性。

TrustWeave针对这一独特的安全挑战，扩展了Linux内核中的IMA（Integrity Measurement Architecture）框架，将其重新设计为面向LLM推理工作负载的完整性度量和远程证明系统。该框架的核心思路是在LLM推理管线的关键节点（模型加载、权重初始化、token生成等）植入完整性度量钩子，实时计算并记录模型文件、推理代码和运行时内存页的哈希值，形成一条不可篡改的度量日志链。通过远程证明协议，任何依赖方（模型提供方、最终用户、合规审计方）都可以验证多云环境中运行的LLM推理实例的完整性状态。TrustWeave的设计不需要依赖任何特定硬件TEE，因而可以在不同云提供商之间无缝运行，为跨不信任云提供商的LLM部署建立了统一的信任锚点。

### 技术线索与启示

- **安全与可信计算**：多云LLM完整性验证填补了AI基础设施安全的一个关键空白——在TEE受限于内存容量的情况下，TrustWeave展示了基于IMA扩展的软件级完整性证明方案的可行性，这一思路可推广到多模态大模型、联邦学习聚合器等更大规模AI组件的安全验证
- **Agent与LLM应用方向**：Agent系统在调用多云LLM服务时需要建立端到端的信任链，确保每个调用环节的模型完整性——TrustWeave的运行时证明协议可直接嵌入Agent的LLM调用中间件层，为Agent决策的可信性提供安全基础
- **云原生与分布式架构**：跨云信任建立是多云AI部署架构中当前最薄弱的环节之一，TrustWeave提供的统一度量框架为构建多云AI服务的安全服务等级协议（SLA）提供了技术基础，有助于推动"AI信任即服务"概念的工程化实现
- **开放性问题与未来方向**：随着MoE（混合专家）架构在多云场景中的部署，模型分片后的跨分片完整性验证将成为更具挑战性的开放问题——如何在保证证明效率的同时追踪模型分片间的依赖关系，需要社区继续探索

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 8.4 Lessons Learned from Incorporating Formal Methods in Huawei Cloud Reliability

**作者**：Claudia Cauli, Timo Lang, Shuo Chen, et al.
**机构**：Huawei Technologies Co., Ltd (Ireland & Shenzhen)
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

形式化方法长期以来被视为软件系统可靠性保障的"黄金标准"——通过数学证明确保系统在给定规范下不会出错。然而，尽管学术界在形式化验证技术上取得了长足进步（从模型检测到定理证明再到SMT求解），形式化方法在工业级云系统中的大规模采用仍然极其有限。其根本原因在于，云系统具有前所未有的复杂性：分布式共识协议的状态空间爆炸、硬件故障模型的多样性、持续演进导致的规范变更、以及大规模运维团队中形式化方法专业知识匮乏，都使得学术界的验证工具难以直接应用于工业生产环境。此外，形式化验证的投资回报率难以量化——在资源受限的项目周期内，投入大量人力进行形式化验证是否真的比传统测试方法带来更大的可靠性提升？

华为云团队的这篇经验论文通过三个真实的工业项目案例，系统性地分析了形式化方法在云可靠性保障中的不同应用策略及其投资-保证权衡。第一个项目采用轻量级形式化规格（TLA+模型检测），以最小投入快速发现分布式协议设计中的逻辑漏洞；第二个项目采用中等投入的交互式定理证明，对关键安全不变量进行机器验证；第三个项目则采用了高投入的全形式化验证流水线，从需求规格到代码实现建立了完整的证明链。论文深入剖析了每个项目中的实践挑战——包括形式化规范与实现代码的同步维护、形式化验证结果向非形式化背景工程师的传达、以及组织层面如何建立形式化方法的文化认同。基于这些经验，论文提出了一套面向工业云系统的形式化方法应用决策框架，帮助组织根据系统关键度和资源约束选择合适的形式化策略。

### 技术线索与启示

- **安全与可信计算**：形式化方法在工业云系统的落地经验对国内云厂商（阿里云、腾讯云等）具有直接参考价值——论文提供的投资-保证权衡框架可指导企业在核心基础设施组件（如分布式锁、分布式事务协调器等）中采用级别匹配的形式化验证策略，而非盲目追求"全证明"
- **系统软件方向**：形式化验证的投入产出比需要在项目初期仔细评估——论文提出的三层分层策略（轻量规格→交互式证明→全验证流水线）为工程团队提供了渐进式引入形式化方法的可操作路径，降低了组织变革的风险
- **开放性问题与未来方向**：降低形式化方法对领域专家的依赖是实现工业推广的关键瓶颈——自动化规范推导、LLM辅助的不变量生成、以及验证结果的自然语言解释等方向有望在未来5-10年内显著降低形式化方法的人力门槛
- **教育与人才培养**：论文隐含地揭示了一个重要问题——工业界缺乏兼具形式化方法技能和分布式系统工程经验的"复合型"人才，这提示高校在系统方向的研究生培养中应加强形式化方法训练

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

# Part 9: OS & Virtualization

> 本部分涵盖6篇论文，涉及用Rust强化OS级虚拟化安全、自动化OS特化、嵌套虚拟化Fuzzing、RISC-V上x86-64仿真、异构处理器间VM迁移以及跨ISA异构计算二进制重写。

---

## 9.1 CofferOS: Hardening OS-level Virtualization with Rust

**作者**：Minkyu Jung, Chanshin Kwak, Junho Ahn, Sunho Park, Changjun Lee, Jongyul Kim, Jeehoon Kang, Youngjin Kwon
**机构**：KAIST, UIUC, FuriosaAI
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

OS级虚拟化（以Linux容器为代表）是云原生基础设施的基石，但在提供强隔离和多租户安全保障方面长期面临一个根本性困境：现有内核几乎全部以C语言编写，内存安全漏洞（Use-After-Free、缓冲区溢出、Double-Free等）层出不穷，每年持续贡献大量高危CVE。尽管内核社区投入了大量资源进行代码审查和静态分析，但在数百万行C代码的海量攻击面面前，人为发现和修复漏洞的速度远远落后于攻击者的探索进度。与此同时，Rust语言凭借其所有权模型、借用检查器和类型系统，已经在用户态系统软件中证明了从编译期消除整类内存安全漏洞的能力。然而，将Rust应用于内核级虚拟化面临巨大的工程挑战：内核中广泛存在的自引用数据结构、复杂的并发同步原语、以及大量依赖指针运算的性能敏感路径，都难以直接映射到Rust的安全编程模型中。

CofferOS是首个用Rust从零重新设计的OS级虚拟化内核。论文的核心贡献在于展示了一种系统化的内核数据结构安全建模方法：通过精心设计的抽象层（包括基于生命周期的资源管理、类型状态模式（typestate）编码的安全状态机、以及受限unsafe块的精确定义边界），将内核中原本隐含的安全约束显式化为编译期可检查的类型规则。研究团队在保证隔离强度的同时维持了定制化灵活性——每个虚拟化实例可以根据工作负载需求配置不同的内核功能子集，而不牺牲安全性。评估结果表明，CofferOS从设计层面消除了Use-After-Free、缓冲区溢出、未初始化内存访问等多个漏洞类别，同时通过零成本抽象的Rust特性保持了接近原生C内核的性能水平。这证明了在操作系统内核中全面采用Rust不仅是可行的高度安全的替代方案，而且不会带来性能上的妥协。

### 技术线索与启示

- **安全与可信计算**：Rust内核为容器安全提供了从语言层面而非运行时检查层面的内存安全保障——CofferOS的成功证明了在虚拟化内核中全面使用Rust是完全可行的，为减少内核CVE这一长期困扰行业的安全难题提供了根本性解决方案
- **系统软件方向**：CofferOS中的Rust安全建模方法论（生命周期资源管理、typestate安全状态机、unsafe边界收缩）具有高度可迁移性——可以指导文件系统、网络栈、设备驱动等其他内核子系统的Rust重写工作，推动整个操作系统内核从"打补丁式"安全演进转向"设计即安全"的方法论
- **开放性问题与未来方向**：Rust内核与现有C内核模块的互操作性仍是工程实践中的重大挑战——C与Rust之间的FFI边界可能成为新的安全薄弱点，如何在保持Rust安全保证的前提下与海量现有C驱动程序共存，需要社区持续探索ABI安全规范
- **工业实践与生态建设**：FuriosaAI等AI芯片公司的参与表明，新一代AI加速器厂商倾向于从零开始构建Rust原生驱动栈而非继承C历史包袱——这可能催生一个全新的、以安全语言为核心的加速器驱动生态

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 9.2 Wayfinder: Automated Operating System Specialization

**作者**：Alexander Jung, Cezar Crăciunoiu, Nikolaos Karaolidis, Hugo Lefeuvre, Daniel Oñoro Rubio, Felipe Huici, Charalampos Rotsos, Pierre Olivier
**机构**：Lancaster University, Politehnica Bucharest, U Manchester, UBC, NEC Labs, Unikraft
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

操作系统特化——即根据特定应用场景裁剪不必要的内核功能以优化性能、减少内存占用和降低攻击面——已被证明是在特定领域（如Serverless、边缘计算、IoT等）中提升系统效率的有效手段。Unikraft等Unikernel项目已经展示了操作系统特化的巨大潜力。然而，手工探索操作系统的庞大配置空间是极其困难甚至不可能的：现代操作系统提供了数量惊人的编译时选项、启动时参数和运行时调优变量，这些参数之间存在复杂的非线性交互效应。以Linux内核为例，其Kconfig系统包含超过15000个编译选项，其中很多选项之间存在依赖和互斥关系。在这种规模下，即使是经验丰富的系统工程师也难以找到针对特定工作负载的最优配置组合。此外，配置搜索还面临冷启动问题——每次配置更改都需要重新编译和部署操作系统，导致单次尝试的成本极高。

Wayfinder创新性地将操作系统配置搜索建模为神经网络驱动的自动化优化问题。该系统由两个协同工作的核心组件构成：一个自动化基准测试平台负责精确、可重复地测量任意配置下的系统性能指标（启动时间、内存占用、吞吐量、攻击面大小等），一个神经网络搜索算法则学习配置参数与性能之间的映射关系，从而高效导航搜索空间。与传统暴力搜索或随机搜索相比，Wayfinder的关键优势在于其利用神经网络学习到的潜在函数空间来预测未尝试配置的预期性能，从而优先探索最有潜力的配置区域。论文在Unikraft上进行的实验表明，Wayfinder实现平均24%的性能提升，同时显著减少内存占用和攻击面。该方法论具有广泛的适用性，不仅限于Unikernel，也可推广至传统操作系统和数据库系统的配置优化。

### 技术线索与启示

- **系统软件方向**：神经网络驱动的OS配置搜索为操作系统自动化运维提供了新的技术范式——这一方法论可直接集成到Unikraft等Unikernel框架中，也可扩展至eBPF程序优化、内核模块选择等领域，使OS特化从少数专家的手艺活变为普通开发者亦可使用的自动化工具
- **性能工程与可观测性**：将配置空间建模为神经网络优化问题的方法具有高度的跨领域可迁移性——数据库参数调优（如PostgreSQL的数百个GUC参数）、JVM垃圾回收器选择、以及分布式系统的超参数优化都可以借鉴Wayfinder的搜索策略
- **云原生与分布式架构**：Serverless场景下每个函数的执行模式各不相同（CPU密集型、IO密集型、内存密集型等），Wayfinder可以为每个函数自动生成定制化的OS配置，从而在函数冷启动延迟、执行性能和资源开销之间达到最优平衡
- **开放性问题与未来方向**：配置搜索中的迁移学习是一个有前景的方向——在不同工作负载之间如何复用已学到的配置-性能映射知识，以减少新场景下的搜索成本，是降低Wayfinder实际部署门槛的关键

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 9.3 NecoFuzz: Effective Fuzzing of Nested Virtualization via Fuzz-Harness VMs

**作者**：Reima Ishii, Takaaki Fukai, Takahiro Shinagawa
**机构**：The University of Tokyo, AIST
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

嵌套虚拟化——即在虚拟机内部再运行虚拟机——是云计算基础设施中广泛应用的技术，支撑着CI/CD流水线中的隔离构建环境、安全研究中的恶意软件分析沙箱、以及GPU虚拟化中的直接设备分配等关键场景。然而，嵌套虚拟化引入了一层额外的抽象复杂性：hypervisor需要管理VMCS（虚拟机控制结构）的影子副本、维护嵌套页表（嵌套EPT/NPT）的多级地址转换、以及处理从客户hypervisor到物理hypervisor的VM-entry/exit事件链。这些复杂逻辑在传统Fuzzing方法中几乎不可测试，因为标准Fuzzer以用户态程序或内核模块为目标，缺乏对VMX根模式和非根模式之间复杂交互的有效覆盖手段。更棘手的是，嵌套虚拟化中的漏洞往往涉及跨特权级和跨VM边界的异常状态转换——这些状态转换路径极难通过人工测试用例穷举覆盖。

NecoFuzz是首个系统性针对嵌套虚拟化进行Fuzzing的测试框架，其核心创新在于"Fuzz-Harness VM"概念。与传统的将Fuzzer直接连接到被测试软件不同，NecoFuzz合成特制的客户虚拟机作为测试驱动——这些VM被精心设计以生成覆盖VM-entry/exit路径、嵌套EPT异常处理、中断注入与拦截边界等关键代码路径的输入序列。Fuzz-Harness VM在物理hypervisor（如KVM）上运行，通过编排内层VM和外层VM的交互来曝露状态转换异常。在KVM/QEMU上的测试中，NecoFuzz发现了6个先前未知的安全漏洞，其中2个获得了CVE编号，充分证明了嵌套虚拟化在安全方面的脆弱性以及NecoFuzz方法的有效性。这一成果表明，将测试目标封装为VM是一种新颖且高效的安全测试范式。

### 技术线索与启示

- **安全与可信计算**：嵌套虚拟化长期以来是云安全的一个薄弱但被忽视的环节——NecoFuzz的6个新发现漏洞（其中2个获CVE）强烈表明，随着嵌套虚拟化在GPU虚拟化、机密计算等安全敏感场景中的广泛使用，其安全审计需求将急剧增长
- **系统软件方向**：Fuzz-Harness VM这一测试方法论具有高度可扩展性——可以推广到TrustZone安全监控器、AMD SEV-SNP嵌套证明、以及Hyper-V嵌套虚拟化等其他虚拟化/安全扩展的Fuzzing测试中
- **云原生与分布式架构**：嵌套虚拟化在CI/CD（如GitHub Actions的虚拟机执行环境）、Kubernetes虚拟化节点、以及GPU直通（GPU Pass-through）等云原生场景中广泛使用，这些场景的安全性直接影响所有托管服务的客户数据安全
- **开放性问题与未来方向**：当前NecoFuzz主要覆盖Intel VMX架构下的嵌套虚拟化路径，扩展到AMD SVM架构、ARM VHE扩展以及新兴的RISC-V H扩展将是增强覆盖面的重要工作

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 9.4 Practical and Efficient x86-64 Emulation on RISC-V

**作者**：Xiongchuan Tan, Yang Liu, Sebastien Chevalier, Yangyu Chen, Xiaoyi Liu, Haohuan Fu
**机构**：Tsinghua University, ISCAS, Chongqing University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

RISC-V作为开放指令集架构（ISA）正在全球范围内快速崛起，从嵌入式IoT设备到高性能服务器芯片，越来越多的硬件厂商正在推出基于RISC-V的处理器产品。然而，RISC-V生态系统面临一个严峻的现实挑战：数十年来积累的海量x86-64应用软件（包括商业软件、闭源驱动、游戏、企业应用等）无法在RISC-V平台上运行。现有的跨ISA仿真方案（如QEMU的用户态仿真和系统级仿真）虽然功能完备，但性能表现极其糟糕——对计算密集型应用，QEMU的纯软件指令翻译可能带来10倍甚至更高的性能开销，使得实际的复杂应用（如3D游戏、视频处理等）在RISC-V硬件上几乎无法使用。这一软件生态鸿沟严重阻碍了RISC-V在桌面和服务器市场的渗透，形成了"没有软件就没有用户，没有用户就没有软件"的恶性循环。

本文提出了一种融合RISC-V向量扩展（RVV 1.0）和动态二进制翻译（DBT）的高效x86-64仿真方案。其核心洞见在于：x86-64的SSE/AVX指令集在语义上与RISC-V的RVV向量指令高度相似，可以通过直接向量化映射而非逐条标量仿真来实现高性能翻译。论文详细描述了将SSE打包整数/浮点操作、内存对齐加载/存储以及数据重排指令映射到RVV等价操作的系统化方法。对于无法通过RVV直接映射的复杂x86控制流指令，系统回退到优化的动态二进制翻译引擎。研究团队在真实的RISC-V硬件平台上进行了验证，成功运行了包括3D游戏在内的复杂闭源x86-64应用，其性能显著优于QEMU的纯软件仿真方案。这项工作为RISC-V平台构建实用的x86-64兼容层奠定了技术基础，有望加速RISC-V在更广泛计算场景中的采纳进程。

### 技术线索与启示

- **硬件-软件协同设计**：利用RVV向量扩展做SSE/AVX仿真充分展示了指令集协同设计的威力——这一思路提示芯片设计者，在新ISA的设计阶段就应该前瞻性地考虑为流行ISA的指令提供语义兼容支持，而非将跨ISA兼容的负担完全留给软件层
- **系统软件方向**：动态二进制翻译+向量化仿真的混合方案可推广到其他ISA对之间的高性能兼容层构建——例如利用ARM SVE/SVE2向量扩展加速x86 SSE/AVX仿真，或者利用RISC-V向量加密扩展加速ARM NEON仿真
- **开放性问题与未来方向**：RISC-V在服务器领域的渗透在很大程度上取决于能否提供高性能的x86-64兼容层——随着RISC-V高性能处理器（如算能SG2042等）的持续迭代，x86兼容层的性能每提升10%，RISC-V在数据中心的市场潜力就会显著扩大，这方面的学术投入具有高度战略价值
- **生态建设与标准化**：高效的x86仿真不仅仅是指令翻译问题，还涉及系统调用ABI兼容、动态链接器适配、信号处理语义一致等大量系统工程细节——社区需要建立一套标准化的兼容性测试套件和认证体系

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 9.5 Everything You Need to Know About VM Live Migration Between Heterogeneous Processors

**作者**：Kenta Ishiguro, Fonyuy-Asheri Caleb, Elouan Barraud, Renaud Lachaize, Yérom-David Bromberg, Alain Tchana
**机构**：Université Grenoble Alpes, INRIA, University of Rennes
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

虚拟机热迁移（Live Migration）是云计算基础设施中最核心的能力之一——它支持零停机维护、动态负载均衡和节能调度。数十年来，学术界和工业界在VM热迁移方面积累了大量的研究和工程经验，但这些工作几乎全部假设源和目标服务器具有相同的处理器型号或至少在ISA层面完全一致。然而，随着云计算数据中心从均质化向异质化转型（同一集群中同时部署不同型号、不同代际甚至不同厂商的CPU），半异构处理器之间的VM热迁移正成为一项日益迫切但技术准备严重不足的需求。所谓"半异构"指的是同ISA但微架构不同的处理器——例如Intel的Sapphire Rapids和Emerald Rapids之间、或者AMD的Milan和Genoa之间——它们虽然运行相同的x86-64指令集，但CPU特性集（如AVX-512子集、缓存预取策略、功耗管理特性等）存在差异。

这篇法国研究团队的论文首次对半异构处理器间VM热迁移进行了全面、系统化的分析，揭示了多个此前未被充分认识的迁移陷阱。研究发现，即使处理器属于同一ISA家族，微架构差异也会导致三类严重问题：CPU特性不兼容（目标CPU不支持源CPU的某些扩展指令，导致迁移后应用崩溃或静默降级）、性能退化（迁移后由于缓存拓扑、TLB行为或NUMA布局差异导致应用性能突然下降）、以及一致性问题（CPUID等架构状态的迁移语义模糊导致应用行为不确定）。论文通过实验揭示了这些陷阱在实际系统中的触发条件和影响程度，并基于分析结果提出了一套系统化的迁移解决方案指南，涵盖预迁移兼容性检查、特性协商协议、以及迁移后性能验证等工程最佳实践。该工作为正在经历处理器异质化转型的云数据中心提供了关键的技术参考。

### 技术线索与启示

- **云原生与分布式架构**：异构CPU集群已成为现代数据中心的常态而非例外——无论是采购新一代服务器时造成的代际混合，还是出于供应链安全考量的多厂商策略，都意味VM热迁移必须面对处理器异质性，该论文的实验分析和工程指南对AWS Nitro、阿里云神龙等虚拟化平台有直接的工程价值
- **性能工程与可观测性**：迁移后的性能退化检测是论文揭示的一个关键但易被忽视的问题——将性能退化检测集成到云平台的迁移决策引擎中，可以在迁移前评估风险并推荐最优目标主机，避免"迁移成功但性能崩溃"的尴尬局面
- **开放性问题与未来方向**：ARM服务器CPU的多样化趋势（Ampere、Graviton、倚天等各行其道）将使得ARM VM热迁移面临比x86更严峻的半异构挑战——ARM生态缺乏统一的CPUID等价机制和特性发现协议，社区需要建立标准化的ARM处理器能力描述框架
- **工程实践与标准化**：论文提出的预迁移兼容性检查框架有望推动虚拟化管理器（如QEMU/KVM、Firecracker等）标准化其迁移兼容性描述格式，使跨厂商的迁移成为可能

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 9.6 Chimera: Transparent ISAX Heterogeneous Computing via Binary Rewriting

**作者**：Jiatai He, Qinglin Pan, Ruilin Zhao, et al.
**机构**：ISCAS, UCAS, Hohai University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

跨ISA异构计算——即在同一个系统中同时利用不同指令集架构的处理器（例如x86-64 CPU+RISC-V协处理器，或ARM CPU+x86加速器）——正成为提升数据中心能效和特定负载性能的重要趋势。然而，实现跨ISA的透明异构计算面临一个核心矛盾：应用二进制文件是针对单一ISA编译的，无法直接在不同ISA处理器上执行。传统的解决方案依赖动态二进制翻译（如QEMU）在运行时逐块翻译并执行跨ISA代码，这种方法虽然实现了完全的透明性，但持续性的翻译开销极为显著——每一个执行过的基本块都需要翻译，即使是被频繁调用的热路径也每次都要经过翻译管道。此外，动态翻译还引入了额外的内存开销（翻译缓存）和控制流间接性（每次间接跳转都需要查找翻译缓存），使得性能进一步恶化。

Chimera提出了一种"静态重写为主、动态翻译为辅"的创新混合方案来大幅降低跨ISA异构计算的性能开销。其核心策略是先通过静态二进制重写技术（Static Binary Rewriting）在部署前尽可能多地翻译目标ISA指令——包括函数入口点、间接调用目标的保守分析、以及符号化地址的静态解析等。对于那些在静态分析阶段无法确定的指令（如通过函数指针进行的间接调用、动态生成的代码、以及自修改代码等），Chimera采用被动触发故障处理机制：当程序执行到未翻译指令时触发一个轻量级故障，系统随即进行按需翻译并修补对应位置，后续执行即可直接命中已翻译代码。这种"乐观静态翻译+回退动态翻译"的策略使得Chimera与原生ISA执行的性能差距被压缩到平均仅3.2%，相比纯动态翻译方案获得了数量级的性能改善。该方案实现了完全的透明性——应用程序无需任何代码修改或重编译即可在异构ISA环境中运行。

### 技术线索与启示

- **系统软件方向**：静态重写+按需动态翻译的混合方法是一种通用范式，可推广到WebAssembly到原生代码编译（WASM AOT+JIT分层编译）、跨ISA的Android应用兼容层（如Intel的ARM-to-x86翻译），甚至可应用于Python JIT编译中的字节码到机器码的分层翻译策略
- **硬件-软件协同设计**：高效跨ISA异构计算需要深入理解两种ISA在ABI、内存模型和调用约定层面的差异——Chimera中处理跨ISA函数调用和内存映射的具体工程方法（如寄存器映射、栈帧转换、原子操作模拟等）为其他跨ISA系统提供了可复用的设计模式
- **云原生与分布式架构**：透明的跨ISA迁移方案为数据中心部署异构ISA集群降低了技术门槛——云提供商可以在不影响用户应用的前提下引入ARM或RISC-V节点以实现成本优化或能效提升，Chimera的静态预翻译+动态回退策略恰好契合了云环境的部署模型
- **开放性问题与未来方向**：跨ISA的间接控制流（特别是C++虚函数调用和JIT代码）仍是静态重写的阿喀琉斯之踵——需要更精确的静态分析技术与更高效的JIT回退路径的进一步协同优化

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

# Part 10: Distributed Systems & Blockchain

> 本部分涵盖5篇论文，涉及拜占庭共识角色分配优化、账户区块链状态精简、DAG BFT共识吞吐提升、纠删码加速区块链传播以及企业级区块链模糊测试。

---

## 10.1 OptiLog: Assigning Roles in Byzantine Consensus

**作者**：Hanish Gogada, Christian Berger, Leander Jehl, Hans P. Reiser, Hein Meling
**机构**：U Stavanger, FAU Erlangen-Nürnberg, Reykjavik University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

拜占庭容错（BFT）共识协议是区块链和分布式账本技术的核心支柱，能够保证在存在任意恶意行为（Byzantine faults）的分布式系统中仍然达成一致。然而，BFT协议在设计上假设所有副本具有同等角色和同等通信成本，这一假设在局域网环境中成立——节点之间延迟差异小、带宽充足。但在广域网（WAN）部署中（如跨越不同大洲的区块链节点），这一假设彻底失效：节点间网络延迟存在显著差异，部分节点可能由于地理距离、网络拥塞或ISP策略而表现异常。传统BFT协议缺乏对节点行为差异的感知能力，导致整个共识过程被最慢节点拖累——这在分布式系统理论中被称为"straggler effect"。更糟糕的是，恶意节点可能故意制造行为异常（延迟响应、部分丢弃消息等）来破坏共识的活性（liveness）而不一定被传统超时机制检测到。

OptiLog提出了一种动态角色分配机制来应对广域BFT面临的挑战。其核心思想是：将副本分为优化节点和普通节点两类角色，优化节点承担共识协议中的关键路径（如leader提案和commit消息聚合），普通节点仅参与投票。系统持续监测每个副本的响应延迟、消息丢包率和行为一致性等指标，基于统计异常检测算法识别并排除行为异常的副本（无论是由于恶意行为还是网络故障），自动将它们降级为普通节点角色。这种动态角色重分配使系统可以在大部分时间以优化低延迟模式运行——仅由稳定、低延迟的少数节点承担核心责任。论文将OptiLog的设计灵活应用于Aware和Kauri两种不同的BFT协议架构，证明了该方法的通用性。实验表明角色分配机制能显著降低广域网环境下的共识延迟并提升系统吞吐量。

### 技术线索与启示

- **云原生与分布式架构**：动态角色分配对跨越多个地理区域部署的区块链网络和分布式数据库具有直接工程价值——例如多区域的etcd集群、跨AZ的ZooKeeper部署等都可以利用角色分配来降低跨区域协调延迟
- **安全与可信计算**：基于行为检测的拜占庭副本识别和排除机制提供了一种自适应安全策略——不依赖静态的拜占庭假设（如f=⌊(n-1)/3⌋），而是根据实际观测动态调整安全策略，增强了系统在非均匀威胁模型下的韧性
- **开放性问题与未来方向**：角色分配与网络拓扑感知结合可进一步优化广域BFT——如果能够感知到节点间网络拓扑和AS路径，将优化节点优先部署在网络密集区域，有望获得额外的延迟增益
- **工程实践与应用方向**：OptiLog的角色分配框架可以集成到Hyperledger Fabric、Tendermint等联盟链框架中，为不同信任假设下的联盟成员提供差异化的参与角色，在安全性和效率之间提供更灵活的配置空间

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 10.2 Ethane: Debloating State Data using Compact Trie for Account-based Blockchain

**作者**：Junmo Lee, Jaehun Kim, Jiyong Youn, Soo-Mook Moon
**机构**：Seoul National University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

账户型区块链（以以太坊及其兼容链为代表）正面临日益严重的状态膨胀危机。随着时间的推移，历史账户状态数据持续累积——已销毁的合约、废弃的地址、历史存储槽等"僵尸数据"在全局状态Trie中永久留存而无法被清除。以太坊的全局状态数据已经膨胀到令普通节点难以承受的规模——全节点需要TB级别的SSD存储来维护完整的状态数据，这严重违背了区块链去中心化的核心理念。更令人担忧的是，状态膨胀形成了一种恶性循环：更大的状态意味着更慢的同步速度和更高的硬件门槛，这导致参与网络的节点数量减少；而更少的节点反过来增加了网络的中心化风险。学术界和社区虽然提出过状态过期（State Expiry）、无状态客户端（Stateless Clients）等多种方案，但这些方案要么需要硬分叉来改变共识协议，要么引入了额外的网络带宽开销或信任假设。

Ethane提出了一种无需协议级变更的精巧状态精简方案。其核心创新在于利用区块头中已有的元数据构建紧凑Trie（Compact Trie）数据结构——由于每个区块头中已经包含了状态根哈希和交易Trie根，Ethane可以通过追溯和重构区块头中的已有信息来推导哪些状态条目是当前活跃的、哪些是已废弃的"膨胀"数据。通过这种方式，Ethane无需下载或依赖任何额外数据集，仅利用区块链本身的区块头即可完成状态精简。更重要的是，Ethane的紧凑Trie数据结构支持部分验证——轻客户端或资源受限节点可以选择只验证自己关心的状态子集，而不需要遍历全部状态数据。实验表明Ethane能显著减少状态数据的存储体积和验证时间，为解决以太坊等账户型区块链的状态膨胀问题提供了一条不需要硬分叉的务实路径。

### 技术线索与启示

- **数据密集型系统**：利用已有元数据构建紧凑数据结构的策略是一种通用的空间优化范式——可应用于日志压缩（利用索引元数据去重）、LSM-Tree的SSTable元数据优化、以及文件系统的元数据驱动的重复数据删除等跨领域场景
- **系统软件方向**：紧凑Trie设计对分布式状态管理和备份系统有直接参考价值——例如分布式KV存储的状态快照机制、Git-like版本控制系统的packfile优化等都可以借鉴Ethane的元数据驱动的状态精简思想
- **开放性问题与未来方向**：状态膨胀是一个系统工程问题，需要多层次协同解决——Ethane的精简方案应该与分片（将状态分片到不同子链）、Layer2 Rollup（将大部分状态迁移到L2）以及Verkle Tree（降低见证数据大小）等技术协同配合，形成多管齐下的解决方案
- **生态与标准化**：Ethane的方案不需要硬分叉这一特性极具实用价值——这意味着它可以作为客户端级别的优化被不同的以太坊客户端（如Geth、Nethermind等）独立实现和渐进式部署

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 10.3 Towards Improving Throughput and Scalability of DAG-based BFT SMR

**作者**：Nibesh Shrestha, Aniket Kate
**机构**：Supra Research, Purdue University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

基于有向无环图（DAG）的拜占庭容错状态机复制（BFT SMR）协议是近年来区块链共识领域最重要的架构演进之一。与传统的轮转式leader BFT协议（如PBFT、HotStuff等）不同，DAG-based BFT允许所有副本并行提案和传播交易，通过DAG结构的因果排序而非严格轮转来实现共识排序，理论上可以获得更高的吞吐量和更好的网络利用率。然而，在实际大规模部署中，DAG-based BFT面临两个关键的扩展性瓶颈：第一，带宽密集型的投票传播模式——每个副本需要向所有其他副本广播投票消息，导致O(n²)的消息复杂度，大量低效的冗余通信占据了宝贵的广域网带宽；第二，DAG结构的提交延迟——虽然并行提案提升了吞吐量，但由于DAG中交易的因果依赖链可能很长，从交易被提出到被最终确认的延迟可能显著高于传统BFT协议。

这篇由Purdue大学与Supra Research合作的论文提出了三项系统性的改进来突破DAG BFT的扩展性瓶颈。第一项改进是Tribe辅助广播——将副本分组为"Tribe"（部落），组内使用高效的全广播协议，跨组之间通过代表节点进行通信，将消息复杂度从O(n²)降低到O(k²+n)，其中k为组数。第二项改进是优化DAG结构本身——通过引入更紧凑的引用策略和更高效的因果编码，减少了DAG中冗余引用导致的消息膨胀和验证开销。第三项改进是改进提交规则——提出了更积极的提交条件，允许在较弱假设下提前确认交易，从而降低端到端确认延迟。基于这三项改进的Shoal++系统在吞吐量和延迟两个维度上均显著优于现有的DAG BFT协议（如Narwhal+Tusk、Bullshark等），为DAG BFT在实际生产环境中的大规模部署扫除了关键的性能障碍。

### 技术线索与启示

- **云原生与分布式架构**：基于Tribe的分组通信降低消息复杂度是一种通用的分布式系统优化策略——可应用于大规模的一致性协议优化（如基于Raft的多Raft组设计）、分布式发布-订阅系统、以及P2P网络的Gossip协议优化
- **数据密集型系统**：DAG消息优化和提交规则改进对高频交易和金融清算系统具有直接参考价值——这类场景对低延迟确定性确认有极高要求，Shoal++的积极提交规则可以在不牺牲安全性的前提下提供更快的交易最终性
- **开放性问题与未来方向**：DAG BFT的吞吐量理论极限和异步安全性边界仍是开放性问题——在完全异步模型（FLP不可能性下）中DAG BFT可以达到的最大吞吐量是多少？能否在不引入随机性预言机的前提下实现异步终局性？
- **工程实践与应用集成**：Shoal++的模块化改进设计使其可以独立应用于不同的DAG BFT实现中——Tribe广播可以集成到Narwhal等现有DAG层，提交规则优化可以单独插入Tusk等共识层，为工业级BFT系统的渐进式升级提供了友好的路径

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 10.4 ECCB: Boosting Block Propagation with Erasure-Coded Compact Block

**作者**：Bingyi Cai, Shenggang Wan, Hong Jiang
**机构**：HUST, UT Arlington
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

区块链的可扩展性瓶颈不仅在于共识协议本身，更在于底层P2P网络的区块传播效率。当矿工或验证者成功产出新区块后，需要尽快将整个区块广播至网络中所有其他全节点，以便它们开始验证和推进共识。然而，随着区块链吞吐量的提升和区块大小的增长，区块传播延迟已经成为制约整个系统扩展的关键因素。在比特币中，区块传播延迟直接导致分叉率上升——延迟越大，两个矿工同时发现有效区块并各自广播的概率越高；在以太坊等支持智能合约的链中，大区块传播还会延迟交易确认和增加重组风险。现有的优化方案主要依赖紧凑区块（Compact Block）技术——通过发送交易的短哈希（而非完整交易内容）让接收方从本地的mempool中重建区块。但这要求接收方mempool中已包含绝大多数交易，在网络拥塞或交易传播不均衡时效果大打折扣。

ECCB创新性地将纠删码（Erasure Coding）引入区块传播协议。其核心设计是：发送方将区块数据分割为k个数据块，通过纠删码编码为n个编码块（n>k），然后向不同邻居发送不同的编码块子集。接收方只需接收到任意足够数量（至少k个）的编码块即可完整重建原始区块——无需依赖本地mempool状态，也无需等待所有片段到达。这种"以编码冗余换取传播鲁棒性"的策略从根本上解决了紧凑区块面临的mempool同步依赖问题：即使接收方的mempool状态与发送方存在显著差异，只要收到足够的编码块就能完整恢复区块。纠删码的冗余可控特性还允许系统根据网络条件动态调整冗余度——在网络质量好的情况下使用较少冗余以节省带宽，在网络不稳定时增加冗余以确保可靠传播。ECCB在显著降低区块传播延迟的同时，提升了对网络丢包和节点异构性的鲁棒性。

### 技术线索与启示

- **云原生与分布式架构**：纠删码加速数据传播的方法具有广泛的适用性——可应用于CDN内容分发（替代或补充传统多播）、分布式存储在去中心化环境下的快速数据恢复、以及边缘计算中的模型分发，本质上任何需要在非可靠P2P环境中高效传播大数据的场景都可能受益
- **性能工程与可观测性**：纠删码与传统短哈希压缩（Compact Block）之间的对比为区块链协议设计者提供了量化的选型依据——在节点mempool同步率作为变量的情况下，两种方案的性能交叉点决定了最佳传播策略
- **系统软件方向**：纠删码可靠传播可以集成到P2P网络协议栈（如libp2p的发布-订阅模块）和分布式数据库的WAL复制协议中——为那些需要在不可靠网络上进行高效、可靠数据复制的基础设施提供通用的优化原语
- **理论探索与工程权衡**：纠删码的参数选择（k和n的比例）直接影响传播延迟与编码计算开销之间的权衡——动态自适应选择编码参数以适应实时网络条件是一个有价值的研究方向

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 10.5 Fuzzing Enterprise-Grade Blockchain Systems: Industrial Practice and Solutions

**作者**：Fuchen Ma, Yuanliang Chen, Zhen Yan, Yuanhang Zhou, Yu Jiang, Mingchao Wan
**机构**：Tsinghua University, Beijing Academy of Blockchain and Edge Computing
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

企业级区块链系统（如Hyperledger Fabric、FISCO BCOS、ChainMaker等）已被广泛应用于供应链金融、政务数据共享、跨境贸易等关键业务场景，承载着数十亿级别的资产和核心业务流程。然而，这些系统的安全性保障长期严重依赖于有限的单元测试和集成测试，缺乏系统性的Fuzzing实践。与公链不同，企业级区块链具有独特的架构特征——权限管理（CA证书体系）、多通道隔离、智能合约与共识协议的紧耦合、以及复杂的插件化模块——这些特征使得通用的Fuzzing工具（如AFL、LibFuzzer等）难以直接应用。此外，企业级区块链的部署配置多种多样，不同组织可能使用不同的共识算法（Raft、PBFT、HotStuff）、不同的状态数据库（LevelDB、CouchDB）和不同的加密套件，组合爆炸式的配置空间使得人工安全审计更加不可行。

清华大学的这项工作是首次系统性地对企业级区块链进行大规模Fuzzing测试的实践研究。研究团队开发了一套专门针对企业级区块链架构特征的Fuzzing框架，涵盖共识协议消息的变异生成、智能合约交易序列的编排模糊化、证书和权限边界条件的边界值测试、以及跨通道交互的并发模糊化等多个测试维度。通过在9个主流企业级区块链系统上的全面测试，研究团队发现了87个严重漏洞，包括共识协议死锁、状态数据库不一致、权限绕过、未处理异常导致的节点崩溃等多种类型。论文不仅呈现了测试结果，更重要的是总结了从这一大规模工业实践中提炼出的通用方法论和工程最佳实践——包括如何构建区块链Fuzzing的测试oracle、如何设计能够触发深层逻辑漏洞的种子语料库、以及如何与开发者团队高效协作完成漏洞的定位于修复。这项工作为企业级区块链的安全质量保障提供了系统性的方法论和基准。

### 技术线索与启示

- **安全与可信计算**：87个严重漏洞的发现是一个令人警醒的数字——它强烈表明当前企业级区块链的安全性成熟度远低于行业预期，安全测试的投入与这些系统所承载的资产价值严重不匹配，亟需建立持续性的安全验证机制
- **系统软件方向**：与开发者协作的Fuzzing模式（包括建立标准化的漏洞报告流程、提供可复现的最小化测试用例、以及协助进行根因分析）是一种可推广的工业安全实践——这种模式同样适用于数据库系统、消息队列等企业级基础设施的安全测试
- **开放性问题与未来方向**：智能合约与共识协议的交互漏洞是比单一层面漏洞更深刻的安全挑战——例如，恶意构造的智能合约交易可能利用共识协议的重排序机制来控制交易最终排序，这类跨层攻击向量尚未被充分研究
- **工业实践与标准化**：论文提出的测试方法论有潜力推动企业级区块链的安全测试标准建立——包括Fuzzing覆盖度的最低要求、漏洞严重性分级标准、以及持续集成中的Fuzzing门禁策略，类似AFL在用户态软件安全中扮演的角色

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

# Part 11: Heterogeneous Computing & Binary Translation

> 本部分涵盖4篇论文，涉及异构FPGA虚拟化、混合DPU架构编译框架、Chiplet异构感知运行时映射以及GPU-FPGA间数据中心级P2P DMA。

---

## 11.1 Proteus: Heterogeneous FPGA Virtualization

**作者**：Felix Gust, Shu Anzai, Charalampos Mainas, Atsushi Koshiba, Pramod Bhatotia
**机构**：TUM, UCLA, Tokyo University of Science
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

现场可编程门阵列（FPGA）已成为数据中心加速器生态中不可或缺的组成部分，凭借其可重配置的硬件结构和极高的能效比，在机器学习推理、金融风控、网络包处理等场景中发挥着关键作用。然而，数据中心在采购FPGA时通常出于供应链多样性和成本优化的考量，会同时引入不同厂商（如AMD/Xilinx、Intel/Altera）的异构FPGA产品。这带来一个尖锐的软件工程问题：每个FPGA厂商都有自己专有的开发工具链、IP核生态、位流格式和运行时API——针对一种FPGA开发和优化的应用无法在另一种FPGA上运行。例如，为AMD Alveo U50编写的OpenCL加速应用无法直接部署到Intel Stratix 10上。这种锁定效应使得数据中心运维团队需要在异构FPGA集群上维护多套不同的软件栈，大幅增加了开发、测试和运维的复杂性，也阻碍了FPGA作为通用加速器资源池进行弹性分配的愿景。

Proteus是首个面向异构FPGA的虚拟化系统，旨在为数据中心提供跨厂商的FPGA加速统一抽象。其核心架构包含四个关键层次：首先是硬件抽象层，为不同厂商的FPGA提供统一的底层接口封装；其次是跨厂商位流转换层，通过分析和重映射FPGA配置位流中的逻辑单元映射、布线资源和时钟域配置，实现位流在不同FPGA之间的可移植转换；第三是统一API层，提供与厂商无关的高级编程接口，使开发者只需编写一份加速器代码即可部署到任意支持的FPGA上；最后是资源调度器，负责跨异构FPGA池的负载分发和资源分配。该团队在AMD Alveo U50/U280和Intel Stratix 10三种FPGA上进行了跨厂商部署验证，证明了Proteus能够实现应用的无缝跨平台部署。这项工作为构建厂商无关的FPGA-as-a-Service云服务奠定了关键的技术基础，有望打破FPGA加速领域的厂商锁定困局。

### 技术线索与启示

- **硬件-软件协同设计**：跨厂商FPGA虚拟化是异构加速器统一管理的一个重要里程碑——它标志着学术界开始正视硬件多样性带来的系统性软件挑战，而非回避或接受硬件锁定的现状，这一思路可以扩展到GPU、NPU、TPU等其他异构加速器的统一管理中
- **系统软件方向**：Proteus的虚拟化层设计（抽象层→转换层→API层→调度层）为异构加速器管理提供了一种通用的分层架构模式——可以迁移到异构GPU集群管理、混合AI芯片池的调度，以及新兴的Chiplet生态中的跨芯粒资源抽象
- **云原生与分布式架构**：统一的FPGA虚拟化抽象为FPGA-as-a-Service（FaaS）云服务提供了关键的技术基础——类似于Kubernetes将CPU和GPU统一为可调度资源的方式，Proteus使FPGA也可以作为一类标准化的可池化加速器资源被Kubernetes编排
- **生态与标准化**：跨厂商位流转换的核心技术挑战（逻辑单元映射、时序收敛、IP硬核兼容等）是FPGA虚拟化能否在工业界大规模采纳的关键——需要在FPGA厂商之间建立开放的标准化的位流中间表示

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 11.2 NutCracker: A Compilation Framework for Hybrid DPU Architectures

**作者**：Yihan Yang, Haifeng Sun, Antoine Kaufmann, Jialin Li
**机构**：NUS, MPI-SWS
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

数据处理单元（DPU）正在成为现代云数据中心基础设施的新支柱——从AWS Nitro到NVIDIA BlueField再到Intel IPU，各大云厂商和芯片厂商纷纷推出自己的DPU产品，将网络、存储和安全等基础设施功能从主机CPU卸载到专用处理器上。然而，现代DPU的架构并非单一同构处理器，而是典型的混合异构系统：通常包含多个通用ARM/RISC-V CPU核心与若干专用加速器（DSA），如正则表达式匹配引擎、加密/压缩引擎、流表匹配器等。这种异构架构给开发者带来了极大的编程挑战——他们需要手动分析每个计算任务的性质，判断其适合在通用CPU上运行还是在某个DSA上执行，并手写两种完全不同编程模型下的代码。更糟糕的是，不同DPU厂商的DSA集合和编程接口互不兼容，导致代码几乎无法跨DPU移植。这种极高的编程复杂度严重阻碍了DPU生态的繁荣——大多数云厂商虽然有DPU硬件，但实际利用效率远低于其理论能力。

NutCracker提出了一种面向混合DPU架构的编译框架，从根本上降低DPU编程的复杂度。其核心设计理念是"目标无关编程"：开发者只需用高级语言描述数据平面处理逻辑（包括包解析、流表匹配、数据变换等），无需关心底层是CPU核心还是特定的DSA在执行。NutCracker的编译器后端负责自动将高级描述分解为计算图，然后通过基于代价模型的划分算法，将计算图中的算子智能映射到最合适的执行单元上——流表匹配操作自动映射到流表DSA，加密操作自动映射到加密引擎，通用控制逻辑映射到CPU核心。编译器还自动生成CPU-DSA之间的数据传输和同步代码，处理异构单元间的共享内存和缓存一致性问题。实验表明NutCracker生成的代码性能接近手工深度优化的实现，同时将开发复杂度降低了数量级。这项工作填补了DPU编程模型的一个重要空白。

### 技术线索与启示

- **系统软件方向**：NutCracker填补了DPU编程模型的长期空白——类似于CUDA降低了GPU编程门槛、TensorFlow/PyTorch降低了深度学习编程门槛，NutCracker的目标是为DPU混合架构提供类似的高层抽象，可以集成到DPDK、SPDK等数据平面开发框架中
- **硬件-软件协同设计**：可扩展的DSA架构描述语言是NutCracker的一个重要设计决策——允许芯片厂商通过配置文件描述其DSA的能力和约束，而不需要修改编译器内核，从而促进了DPU软硬件生态的协同演进
- **云原生与分布式架构**：DPU卸载是云基础设施的重要趋势——随着更多功能（网络虚拟化、存储虚拟化、安全策略执行）被卸载到DPU，NutCracker提供的自动化编程能力将成为DPU大规模部署的关键使能技术
- **开放性挑战与标准化**：不同DPU厂商的DSA在能力、精度和性能特征上存在本质差异——编译框架需要在"自动生成最优代码"和"跨平台可移植性"之间做出设计权衡，过度优化会导致代码碎片化

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 11.3 CHARM: Chiplet Heterogeneity-Aware Runtime Mapping System

**作者**：Alessandro Fogli, Bo Zhao, Peter Pietzuch, Jana Giceva
**机构**：Imperial College London, Aalto University, TU Munich
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

后摩尔时代的CPU设计正在经历从单一大芯片向Chiplet架构的根本性转变。Chiplet通过将多个小尺寸的半导体芯粒（die）通过先进封装（如台积电CoWoS、Intel EMIB等）互连在一起，组成一颗逻辑上的完整处理器。这种设计带来了成本、良率和灵活性的巨大优势——AMD的EPYC和Ryzen系列、Intel的Meteor Lake以及Apple的M系列芯片都已经广泛采用了Chiplet架构。然而，Chiplet架构引入了一个传统操作系统完全无法感知的新层次的异构性：不同芯粒之间虽然运行相同的指令集，但在计算能力、缓存大小、内存带宽和互连延迟方面可能存在显著差异。例如，一个芯粒可能靠近内存控制器因而具有更低的访存延迟，另一个芯粒可能拥有更大的L3缓存但距离PCIe总线更近。现代操作系统的调度器完全无视这些芯粒间的物理差异，将工作负载盲目地分布在不同芯粒的核心上，导致严重的性能不均匀和资源利用不均衡。

CHARM（Chiplet Heterogeneity-Aware Runtime Mapping）是一个面向Chiplet架构的运行时任务映射系统。其核心理念是将Chiplet的物理拓扑特征（芯粒间延迟矩阵、带宽拓扑图、缓存容量分布等）显式引入任务调度决策中。CHARM包含两个紧密协作的组件：离线分析器通过微基准测试自动构建目标Chiplet CPU的精确性能模型，量化每个芯粒在各种访存模式下的延迟和带宽特征；在线运行时调度器则在任务启动和迁移时，结合任务的访存特征（从硬件性能计数器实时获取）和当前各芯粒的负载情况，做出Chiplet感知的调度决策——例如将访存密集型任务调度到靠近内存控制器的芯粒上，将缓存敏感型任务调度到大缓存芯粒上，将IO密集型任务调度到靠近PCIe总线的芯粒上。在真实Chiplet CPU上的实验评估表明，CHARM能带来显著的性能提升和更好的能耗效率，证明了Chiplet感知调度是充分发挥Chiplet CPU潜力的关键技术。

### 技术线索与启示

- **硬件-软件协同设计**：Chiplet是后摩尔时代芯片设计的主流趋势——AMD、Intel、Apple、NVIDIA等都已全面转向Chiplet架构，CHARM为这一新兴的硬件范式提供了急需的系统软件配套，有望成为Chiplet生态中的标准调度参考实现
- **系统软件方向**：Chiplet拓扑感知调度是一个全新的操作系统研究领域——传统Linux调度器以"所有核心等价"为基础假设，这一假设在Chiplet时代已彻底过时，需要将其集成到CFS（完全公平调度器）和EAS（能耗感知调度器）等主线调度器中
- **性能工程与可观测性**：CHARM的轻量级运行时调度在精度和开销之间的平衡设计值得借鉴——通过离线构建性能模型+在线轻量级监控的组合策略，避免了纯在线学习的高开销问题，这种混合方法可推广至NUMA调度、异构内存管理等场景
- **开放性问题与未来方向**：未来Chiplet将不限于同构芯粒拼接——可能会出现异构ISA芯粒（如x86+RISC-V）、异构工艺节点芯粒（3nm+7nm）甚至包含专用领域加速器芯粒的极度异构系统，调度复杂度将呈指数级增长

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 11.4 RoPeerTo: Datacenter-Scale P2P DMA between GPUs and FPGAs

**作者**：Marco Venere, Giuseppe Sorrentino, Benjamin Ramhorst, et al.
**机构**：Politecnico di Milano, ETH Zurich, AMD Research
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

现代数据中心越来越多地采用异构加速器组合（如GPU+FPGA）来构建高性能数据处理流水线。一个典型的场景是：FPGA负责低延迟的网络包预处理和过滤，GPU负责批量化的深度学习推理或大规模并行计算处理。然而，当前数据中心中GPU和FPGA之间的数据传输存在一个严重的架构瓶颈：数据必须经过CPU和系统内存中转。具体来说，FPGA处理完的数据需要通过PCIe写入主机DRAM，CPU启动DMA传输将数据从DRAM搬移到GPU显存，GPU处理完的结果又需要经过同样的逆向路径返回。这种"FPGA→DRAM→GPU"的中转模式带来了三重代价：额外的PCIe带宽消耗、CPU核心参与数据传输导致的计算资源浪费、以及端到端流水线延迟的显著增加。随着GPU和FPGA各自性能的持续提升，两者之间的数据传输带宽正成为整个异构计算流水线的性能天花板。

RoPeerTo提出了一个开源的、适用于数据中心规模的GPU-FPGA点对点（P2P）DMA架构，彻底消除了CPU和系统内存的中转瓶颈。其核心设计基于PCIe的点对点传输能力——现代PCIe交换芯片支持两个PCIe端点设备之间绕过根复合体（Root Complex）直接进行DMA数据传输。RoPeerTo在包括FPGA的PCIe DMA引擎驱动程序、GPU的RDMA栈、PCIe拓扑发现服务以及用户态零拷贝API等多个层面进行了系统级的工程实现和优化。论文团队成功在真实数据中心环境中验证了GPU-FPGA P2P DMA的可行性，实现了接近PCIe理论峰值带宽的直接数据传输，同时显著降低了端到端流水线延迟。RoPeerTo以开源方式发布，可以被集成到ROCm、OpenCL等异构计算平台中，为构建高性能GPU-FPGA异构数据处理系统提供了关键的基础设施。

### 技术线索与启示

- **硬件-软件协同设计**：PCIe P2P DMA绕过CPU的架构思想对不同加速器对组合具有普遍适用性——GPU-NPU之间的模型参数同步、GPU-DPU之间的网络数据直通、甚至GPU-SSD之间的存储数据直接加载都可以利用相同的P2P DMA原理来消除CPU中转开销
- **系统软件方向**：RoPeerTo作为开源框架可以集成到ROCm（AMD GPU计算平台）、OpenCL等主流异构计算框架中——类似于NVIDIA的GPUDirect RDMA已经成为GPU集群通信的事实标准，RoPeerTo有潜力成为GPU-FPGA直接通信的标准化方案
- **数据密集型系统**：绕过CPU的直接P2P传输对大规模数据处理流水线的端到端延迟至关重要——在实时视频分析（FPGA解码+GPU AI推理）、高频交易（FPGA行情解析+GPU策略计算）、基因组分析（FPGA序列比对+GPU变异检测）等场景中，每微秒的中转延迟节省都直接转化为业务竞争力
- **开放性与生态建设**：开源策略是RoPeerTo的重要优势——相比NVIDIA GPUDirect等闭源方案，RoPeerTo的开源特性允许社区贡献对新型FPGA或新兴互连标准（如CXL）的支持，有望催生更丰富的GPU-FPGA异构计算生态

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings




---

# Part 12: Embedded, IoT & Edge ML / Other Papers

> 本部分涵盖EuroSys 2026中未归入Part 1-11的其余论文。

---

## 12.1 Neuro-C: Neural Inference Shaped by Hardware Limits

**作者**：Diletta Romano, Luca Mottola, Thiemo Voigt
**机构**：Uppsala University, RISE, Politecnico di Milano
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

嵌入式设备（如ARM Cortex-M0微控制器）运行神经网络推理时面临极低计算能力和有限内存的严苛约束，传统MAC（乘累加）操作在这些平台上代价高昂——单次MAC可能需要数百个时钟周期且占用大量寄存器资源，使得标准神经网络架构在KB级内存和MHz级频率的微控制器上完全不可行。现有方案要么过度压缩模型导致精度大幅下降，要么无法从根本上解决MAC操作与硬件能力之间的本质不匹配。

Neuro-C提出从硬件原语出发的反向设计范式：完全消除MAC操作，仅使用硬件原生高效操作（位运算、查表、加法）构建完整推理流水线。具体而言，该系统将神经网络中的权重映射为移位操作序列，将激活函数替换为基于查找表的非线性近似，利用硬件ALU直接支持的位级操作实现卷积和全连接层的等效计算。与传统8位量化相比，Neuro-C在Cortex-M0上实现了推理延迟减少一个数量级和内存占用降低数倍的效果，同时通过精心设计的训练方法保持了接近量化模型的精度水平。该方法为超低功耗嵌入式AI开辟了全新的架构-算法协同设计范式，从根本上重新思考了神经网络在极端受限硬件上的可行性。

### 技术线索与启示

- **边缘计算与端侧部署**：消除MAC操作为超低功耗嵌入式AI提供了突破性新范式，使得关键词唤醒、振动模式识别、传感器异常检测等任务可直接在功耗预算毫瓦级的设备上运行，无需升级到更高规格MCU，这对于大规模部署的IoT节点具有重大成本意义。
- **硬件-软件协同设计**：从硬件原生操作为起点反向设计网络架构，而非从标准卷积网络出发进行压缩，代表了一种根本不同的设计哲学——传统方法试图让网络适应硬件，Neuro-C则让网络与硬件同构。这一思想可推广到其他特定硬件平台（如FPGA、ASIC、RISC-V定制指令集）。
- **开放性问题与未来方向**：无MAC网络在处理高维数据（如图像分类、语音识别）时的精度上限仍不明确，如何自动搜索最优的无MAC架构、如何与混合精度方案结合（关键层保留少量MAC）是需要持续探索的方向。此外，将Neuro-C思想扩展到Transformer架构和多模态输入也是潜在挑战。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.2 viNPU: Optimizing Vision Transformer Inference on Mobile NPUs

**作者**：Jeho Lee, Gunjoong Kim, Chanyoung Jung, Jaehee Kim, Seonghoon Park, Hojung Cha
**机构**：Yonsei University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

Vision Transformer（ViT）和CLIP等视觉基础模型（VFM）在移动端部署面临严重的架构-硬件不匹配问题：自注意力机制中的Softmax、LayerNorm和矩阵乘法等核心算子不被移动NPU直接支持，导致大量计算回退到CPU上执行，严重损害推理效率；同时ViT参数量远大于传统CNN，移动NPU的片上内存和带宽难以支撑完整模型加载。

viNPU系统性地解决这一挑战：首先识别并消除NPU不支持算子，将Softmax替换为NPU友好的近似归一化方案，将不规则的内存访问模式重组为NPU高效的规则访问模式；其次设计NPU本地的注意力模式替代方案，利用NPU的卷积加速器模拟部分注意力计算；最后优化权重内存布局、算子融合和流水线调度以最大化NPU利用率。在三星Galaxy设备上完成端到端部署验证，使ViT和CLIP等视觉基础模型首次在移动NPU上实现实时推理。该方法为移动端Transformer推理建立了系统性的算子适配框架，对日益增长的移动视觉AI应用具有直接工程价值。

### 技术线索与启示

- **边缘计算与端侧部署**：移动NPU上ViT优化的核心方法论——识别不支持算子→设计NPU友好替代→优化调度——可直接推广到其他Transformer模型（如移动端BERT、端侧LLM），为移动AI推理引擎（如TensorFlow Lite、MNN、ncnn）提供NPU后端优化参考。
- **硬件-软件协同设计**：viNPU展示的算子替换策略对编译器中间表示（IR）设计有重要参考价值——下游编译器可通过自动识别不兼容算子并查找替代实现来降低开发者手动适配负担。该技术与MLIR的硬件抽象方言结合潜力巨大。
- **性能工程与可观测性**：移动NPU瓶颈分析方法（逐层延迟分析、内存带宽剖析、算子支持矩阵检测）是移动端AI推理性能调优的通用工具箱，可应用于其他移动端推理场景的瓶颈定位和优化决策。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.3 E-Cube: Event Enhanced Efficient Video Streaming for Drones

**作者**：Jingao Xu, Longfei Shangguan, Danyang Li, Yunhao Liu, Zheng Yang
**机构**：HKU, U Pittsburgh, Tsinghua University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

无人机在搜救、巡检、农业等场景中需实时传输高清视频以支持远程决策，但面临双重约束：无线带宽受限（尤其在远距离或遮挡环境下）且无人机电池容量有限，持续高清视频传输会快速耗尽电量。传统帧相机方案在高帧率下产生巨量数据，而降低帧率则导致快速运动场景出现运动模糊和信息丢失，无法满足感知质量和传输效率的兼顾要求。

E-Cube创新性地将事件相机（event camera）与帧相机融合：事件相机以微秒级时间分辨率异步感知像素亮度变化，天然适合捕捉快速运动和边缘信息；低帧率帧相机提供色彩和纹理细节。系统在发送端将事件流与帧数据联合编码——事件流提供运动补偿和时序结构信息，帧数据填充纹理和颜色——在接收端通过事件引导的超分辨率重建恢复高质量视频。相比纯帧相机方案，E-Cube在保持同等感知质量的前提下显著降低传输数据量，且事件流对带宽波动具有内在鲁棒性。该方案为无人机感知领域引入了事件-帧融合的通信范式，对自动驾驶和工业检测等带宽敏感场景具有直接迁移价值。

### 技术线索与启示

- **边缘计算与端侧部署**：事件+帧相机融合是无人机感知的高效数据传输方案，事件相机的异步稀疏特性天然与低功耗边缘设备匹配，未来可探索将融合编码推向更极端的嵌入式平台（如ESP32-CAM），并与端侧SLAM和避障系统集成。
- **系统软件方向**：异构传感器融合传输框架的设计模式——不同模态数据差异化编码、联合重建——可推广到其他多传感器系统，如自动驾驶中的LiDAR+相机融合传输、工业检测中的热成像+可见光融合，其核心思想是让高时间分辨率传感器补偿低帧率传感器的时序盲区。
- **性能工程与可观测性**：带宽-质量动态权衡优化对实时视频流有普遍参考价值，事件流作为辅助通道的引入为自适应比特率（ABR）算法提供了新的优化维度——在带宽骤降时优先保证事件流传输以维持运动连贯性，而非传统方案的均匀降质。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.4 Efficient ML Model Updates for Deeply Embedded Microcontrollers

**作者**：Shishir G. Patil, Sam Kumar, Prabal Dutta, Joseph Gonzalez
**机构**：UC Berkeley, UCLA
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

物联网场景中部署在微控制器（如ARM Cortex-M系列）上的ML模型需要持续更新以适应数据漂移和概念漂移，但面临三重严苛约束：Flash写入寿命有限（约10万次擦写循环后单元失效）、无线传输带宽极低（BLE吞吐量通常在几十KB/s量级）、更新过程中设备不能完全停止感知任务。传统全量OTA更新方式每次需要擦除并重写整个固件分区，在频繁更新场景下会快速耗尽Flash寿命。

本文提出面向深度嵌入式设备的增量模型更新方案，核心思路是仅传输和写入发生变化的权重子集而非完整模型。系统在训练服务器端计算新旧模型之间的权重差异，利用差异编码压缩变化信息；在设备端通过片上微调机制将变化权重精确写入Flash的目标位置，避免全量擦写。更新数据量相比全量传输降低数个数量级，Flash擦写次数大幅减少。该方案还考虑了断电恢复和写失败的安全回退机制，确保在不可靠的无线环境中更新过程不会导致设备变砖。该方法将设备端ML的可持续运维从理论可能变为工程可行，对大规模IoT部署的TCO具有重大影响。

### 技术线索与启示

- **边缘计算与端侧部署**：Flash写入寿命是嵌入式ML的核心约束，且这一问题随着模型复杂度增长变得更加突出——每次更新不仅消耗写入次数，写入过程中的功耗峰值还可能影响电池供电设备。增量更新方案将Flash从"消耗品"变为"可续用资源"，是嵌入式AI可持续部署的前提条件。
- **系统软件方向**：差异编码+增量传输的框架可推广到所有嵌入式OTA场景（不仅仅是ML模型），包括固件更新、配置变更、特征库升级等，为实现细粒度的设备持续交付（Continuous Delivery）提供了底层机制支持。
- **绿色计算与可持续性**：减少Flash写入和无线传输不仅延长硬件寿命、降低维护成本，还直接减少了因设备提前报废产生的电子废弃物，以及对电池的过度消耗。在大规模IoT网络中，每设备微小的寿命延长汇总为显著的可持续性收益。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.5 SwiftFL: Speculative Training for On-Device Federated Deep Learning

**作者**：Yuhui Zhang, Guang Yan, Xin Zhang, Zimu Guo, Lutan Zhao, Jiangfeng Cao, Dan Meng, Rui Hou
**机构**：CAS IIE, Peking University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

设备端联邦学习（Federated Learning）面临通信开销大和设备计算异构双重挑战——慢设备（straggler）成为全局训练瓶颈，传统同步联邦学习必须等待最慢设备完成本地训练才能聚合更新，快设备的大量计算能力被浪费在等待上。随着模型规模增长（从ResNet到ViT再到小型LLM），设备计算能力差距进一步放大这一问题。

SwiftFL引入投机训练机制打破这一瓶颈：快设备基于预测的全局模型提前启动下一轮本地训练，服务器聚合时验证投机方向是否正确。若投机方向与真实聚合方向一致，则训练直接加速一步；若方向偏差，则代价仅为回退并重新训练一轮。具体设计中，SwiftFL采用轻量级模型预测器根据历史更新轨迹推断当前轮次的全局模型变化方向，并通过置信度阈值控制投机风险。在多种FL基准和异构设备配置下实现2-4倍端到端训练加速，且在非IID数据分布下仍保持收敛精度。该方案将投机执行从单机优化推广到分布式学习场景，为异构设备联邦学习提供了一条实用的加速路径。

### 技术线索与启示

- **边缘计算与端侧部署**：投机训练充分利用设备计算异构性——将"快设备等待慢设备"的浪费转化为"快设备预计算未来"的收益，这一思想可推广到其他异构分布式系统（如分层FL、去中心化FL），也可与异步联邦学习结合实现更大加速。
- **系统软件方向**：投机执行+验证回退的通用模式从处理器微架构（分支预测）延伸到分布式训练（模型聚合预测），表明计算机系统中"预测-验证-回退"是一种跨层次的通用优化范式。SwiftFL的验证机制和回退代价管理对其他分布式投机系统有直接参考价值。
- **Agent与LLM应用方向**：联邦学习是LLM分布式微调的重要手段，尤其当数据分散在用户设备且受隐私法规保护时。SwiftFL的投机加速机制可降低设备端LLM微调的等待延迟，使大型模型的联邦学习更加实用。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.6 PointShuffler: Accelerating Point Cloud Neural Networks on GPUs

**作者**：Yangfan Li, Zhengjie Jin, Yue Tian, Mengquan Li, Fengxiao Tang, Ming Zhao, Cen Chen
**机构**：Central South University, Hunan University, SCUT
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

3D点云神经网络（如PointNet++、DGCNN、PointConv）在自动驾驶、AR/VR和机器人感知中广泛应用，但点云数据的稀疏性和不规则性导致GPU利用率严重低下。核心瓶颈在于：点云邻域查询（如k近邻搜索、球查询）产生的内存访问模式高度不规则，不同线程访问的数据地址随空间分布而剧烈变化，导致GPU warp内线程发散（thread divergence）和共享内存bank conflict，大量计算单元处于空闲状态。

PointShuffler通过数据重排从根本上解决这一问题：在预处理阶段分析点云的空间分布特征，将空间邻近的点重新组织到连续内存区域，使邻域查询时的内存访问从随机跳转变为规则的连续访问模式。同时引入GPU友好的索引结构替代传统KD树和八叉树，减少指针追踪开销并提升缓存命中率。在主流GPU上（覆盖NVIDIA RTX 30/40系列和A100），PointShuffler实现平均6.15倍推理加速和5.30倍内存带宽效率提升，且重排开销在预处理阶段一次性摊销。该方法展示了结构化数据布局对不规则计算性能的决定性影响，其核心思路——通过数据重组将稀疏不规则访问转化为密集规则访问——是GPU优化的通用策略。

### 技术线索与启示

- **性能工程与可观测性**：数据重排策略可推广到图神经网络（GNN节点邻域采样）、稀疏矩阵运算（SpMM）、分子动力学模拟（邻域列表构建）等具有不规则数据访问模式的计算场景，核心原则是"宁可预处理时多做一次排序，不让运行时线程发散"。
- **系统软件方向**：点云布局转换可作为通用点云处理库（如Open3D、Pytorch3D）的底层优化后端，通过自动检测点云分布模式选择最优重排策略，对上层应用完全透明。该技术与TVM、Triton等编译器框架的自动调度结合潜力显著。
- **数据密集型系统**：自动驾驶点云处理是实时性要求极高的任务（通常要求100ms以内的端到端延迟），PointShuffler的6倍加速对满足实时性约束至关重要。在机器人和无人机感知中，更低的推理延迟意味着更高的安全裕度。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.7 TAO: Tolerance-Aware Optimistic Verification for FP Neural Networks

**作者**：Jianzhu Yao, Hongxu Su, Taobo Liao, Zerui Cheng, Huan Zhang, Xuechao Wang, Pramod Viswanath
**机构**：Princeton University, HKUST(GZ), UIUC
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

深度神经网络在不可控硬件（如第三方云GPU、边缘设备、TEE环境）上推理时面临浮点非确定性问题：同一模型在不同GPU型号、不同CUDA版本或不同数学库下可能产生微小差异的输出，这种浮点不确定性对模型可复现性和安全性验证构成严重威胁。传统严格位精确比对方案需要在TEE中对整个推理过程进行验证，开销极高（通常10倍以上推理延迟），在实际部署中难以接受。

TAO提出容差感知乐观验证框架，其核心洞察是：神经网络输出对单算子级别的小误差具有天然容错性，不必逐位验证每个运算。具体而言，TAO接受每算子在预设容差范围内的输出偏差，乐观执行完整推理后再进行轻量级验证——验证时仅检查输出偏离是否在容许范围之内，而非验证每个中间结果。该方案将验证从计算密集型转变为检查轻量型，在保持可验证安全性（即输出不会偏离可信结果超过预设容差）的同时，显著降低传统严格验证的极高开销。在ResNet、ViT等多种DNN模型上验证了容差验证的有效性和效率优势，为不可信硬件上的安全AI推理提供了实用的中间道路。

### 技术线索与启示

- **安全与可信计算**：不可信硬件上的推理验证是可信计算的新前沿——当AI推理被外包到第三方基础设施时，用户需要确保返回结果未被篡改且精度可信。TAO的容差验证模式为"可验证推理即服务"（Verifiable Inference as a Service）奠定了理论基础。
- **Agent与LLM应用方向**：当AI Agent调用第三方推理API获取决策支持时，可直接应用乐观验证机制——Agent提交输入、获取输出后运行轻量级验证，确保推理结果在可接受偏差范围内。这对金融风控、医疗诊断等高风险Agent应用尤为关键。
- **开放性问题与未来方向**：容差阈值的自动确定（不同任务、不同层可能需要不同阈值）、大规模LLM推理验证的可行性（LLM输出是文本而非向量，容差定义更复杂）、以及形式化验证与经验容差的结合，都是需要持续探索的开放问题。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.8 GeDES: GPU-Driven Discrete Event Network Simulator

**作者**：Qinyong Li, Zhiwei Zhao, Geyong Min, Zi Wang, Luwei Fu
**机构**：UESTC, University of Exeter
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

大规模网络仿真（如数据中心网络拓扑评估、5G核心网协议验证、卫星互联网路由测试）需要处理海量离散事件——每个数据包的发送、接收、排队、丢弃都是一个事件，复杂拓扑下事件数量可达每秒数十亿量级。传统CPU驱动仿真器（如ns-3、OMNeT++）受限于单线程事件处理吞吐，即使并行化后仍面临内存带宽和缓存一致性开销的瓶颈，无法在合理时间内完成大规模场景仿真。

GeDES将离散事件仿真引擎完整移植到GPU上执行，核心创新在于设计了GPU友好的优先级事件队列和并行仿真引擎。传统堆结构的事件队列在GPU上并行性极差，GeDES改用分层桶排序结构，将事件按时间戳分配到不同桶中，同一桶内事件可完全并行处理。同时设计稀疏事件聚合和warp级同步机制，利用GPU数千个核心并行处理独立事件，实现数量级吞吐提升。该方案使此前需要数天甚至数周的大规模网络评估（如百万节点数据中心全网仿真）可在数小时内完成，大幅缩短网络架构设计和协议验证的迭代周期。

### 技术线索与启示

- **性能工程与可观测性**：GPU加速离散事件仿真的方法论——将串行事件队列重构为可并行桶结构——可推广到交通流仿真、金融交易回测、流行病传播建模等具有离散事件特性的领域，是一种通用的"离散事件→并行桶"加速模式。
- **系统软件方向**：GPU上高效事件队列管理代表了一种新的并行计算模式，不同于传统的SPMD（单程序多数据）模式。GeDES的桶结构事件管理对其他需要GPU上优先级调度的系统（如GPU加速数据库、GPU任务调度器）具有直接参考价值。
- **数据密集型系统**：大规模网络仿真GPU加速使更复杂的"what-if"评估成为可能——网络架构师可以快速迭代评估不同拓扑、路由协议和故障场景下的网络行为，这对云提供商和数据中心运营商具有显著的工程价值。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.9 Effective On-Hardware Fuzzing of Embedded Operating Systems

**作者**：Yuheng Shen, Jianzhong Liu, Qiming Guo, Yifei Chu, Qiang Zhang, Heyuan Shi, Yu Jiang
**机构**：Tsinghua University, Shandong University, Beihang University, Hunan University, Central South University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

嵌入式操作系统（如Zephyr、FreeRTOS、RIOT）广泛应用于IoT设备、工控系统和汽车电子，其安全性直接影响数十亿联网设备的可信基础。然而，传统嵌入式OS安全测试主要依赖仿真器（QEMU/Unicorn）上的Fuzzing，这类方法无法覆盖硬件相关漏洞——包括外设寄存器映射错误、DMA传输竞态、中断嵌套异常、电源管理状态转换bug等。这些漏洞仅在真实硬件-OS-外设三方交互中触发，仿真器无法精确模拟。

本文提出硬件在环Fuzzing框架，在真实开发板上运行目标嵌入式OS并通过调试接口（SWD/JTAG）实现覆盖率反馈和外设状态监控。核心挑战在于：真实硬件上每次Fuzzing迭代后需将系统恢复到干净状态，但嵌入式设备缺乏快照/恢复原语。框架设计了轻量级硬件状态恢复策略——通过外设寄存器复位序列和内存区域选择性回写实现快速状态恢复，避免每次完整重启的数秒级延迟。结合硬件感知输入变异——根据外设内存映射和寄存器布局生成语义有效的测试输入——在Zephyr和FreeRTOS等多个RTOS上发现数十个此前未知漏洞，覆盖外设驱动、网络协议栈和文件系统等关键组件。

### 技术线索与启示

- **安全与可信计算**：嵌入式OS安全性是IoT和工控安全的基石——一个RTOS内核漏洞可能影响同一OS生态中数百万设备。硬件在环Fuzzing填补了仿真Fuzzing的覆盖盲区，对汽车功能安全（ISO 26262）和工业安全（IEC 62443）认证具有支撑价值。
- **系统软件方向**：硬件Fuzzing的覆盖率反馈和状态恢复机制可推广到其他需要真实硬件的测试场景——如固件安全测试、硬件安全模块（HSM）验证、TrustZone切换逻辑测试，其核心挑战都是在缺乏虚拟化支持的裸金属环境中实现可重复的快速状态管理。
- **边缘计算与端侧部署**：边缘设备OS安全直接关系边缘AI安全——如果运行ML推理的RTOS被攻破，攻击者既可窃取模型参数也可篡改推理结果。硬件Fuzzing提供的底层安全保证是边缘AI可信部署的前提。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.10 TierScape: Harnessing Multiple Compressed Tiers for Server Memory TCO

**作者**：Sandeep Kumar, Aravinda Prasad, Sreenivas Subramoney
**机构**：Intel Labs
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

数据中心服务器内存成本占总TCO比例高达40%，且物理内存需求增长速度持续快于DRAM密度提升速度（受制于工艺微缩放缓），内存成本正成为云服务提供商利润率的主要压力来源。现有内存压缩方案（如Linux zswap、zram）仅提供单一压缩层，无法平衡压缩率与访问延迟——高压缩率算法（如zstd）虽然节省空间但解压延迟高，低延迟算法（如lz4）则压缩率不足。

TierScape创建多级不同压缩率和延迟的压缩内存层：从近CPU缓存的最热数据层（无压缩或轻量压缩）到远端内存池的冷数据层（高压缩率），形成一个从低延迟低压缩到高延迟高压缩的连续谱系。系统设计智能数据放置和迁移策略——基于页面访问频率和重用距离预测，动态将冷页面下沉到高压缩层、将热页面提升到低延迟层，确保应用性能影响最小化。在不显著影响应用延迟的前提下，TierScape将服务器内存TCO降低30-50%，为云数据中心内存层级管理提供了精细化的成本-性能调控手段。

### 技术线索与启示

- **数据密集型系统**：多级压缩内存的设计思想可应用于数据库缓冲池管理——热页面保持在未压缩缓冲池中，温页面使用轻量压缩，冷页面使用高压缩率存储。分布式缓存系统（如Redis、Memcached）也可采用类似分层策略降低总内存占用。
- **系统软件方向**：TierScape的多级压缩架构与CXL（Compute Express Link）内存扩展天然互补——CXL提供物理上的远近内存层级，TierScape在此基础上叠加压缩层级，形成物理距离×压缩率的二维内存管理空间，将进一步提升内存成本效率。
- **绿色计算与可持续性**：降低内存TCO意味着每台服务器可使用更少DRAM或更长时间不升级，直接减少DRAM制造相关的碳排放和资源消耗。内存压缩还间接降低了内存刷新功耗，对数据中心PUE改善有正面贡献。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.11 MTTM: Dynamic Fast Memory Partitioning for Multi-tenant Cloud

**作者**：Changjun Lee, Sangjin Choi, Youngjin Kwon
**机构**：KAIST
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

多租户云环境中，不同租户的工作负载共享同一物理服务器的内存带宽，带宽密集型任务（如ML推理、大数据扫描）可能挤占延迟敏感型任务（如Web服务、数据库查询）的内存带宽，导致严重的性能干扰和尾延迟飙升。现有解决方案要么通过静态分区隔离（浪费带宽）、要么依赖软件限流（响应滞后），无法在保证QoS的同时最大化整体利用率。

MTTM（Multi-Tenant memory partitioning）设计低开销内存带宽监控机制——利用硬件性能计数器（PMC）实时感知各租户的带宽使用和延迟敏感度，采样开销控制在1%以内。基于实时监控数据，MTTM动态调整内存控制器的分区边界和配额：对延迟敏感租户分配保证带宽分区，对批量处理租户使用尽力而为带宽池，同时分区边界可根据负载变化在亚秒级重新配置。在多种云工作负载混合场景（如Memcached+Spark、NGINX+ML推理）下验证了分区策略的有效性——延迟敏感型服务尾延迟降低，批量任务吞吐保持，整体带宽利用率提升。该方案为多租户内存QoS管理提供了实用且低侵入的系统级解决方案。

### 技术线索与启示

- **云原生与分布式架构**：内存带宽隔离是多租户QoS的关键能力——CPU隔离（cgroup）和网络隔离（tc）已相对成熟，但内存带宽隔离仍处于早期阶段。MTTM补上了多租户性能隔离拼图中缺失的重要一块，可与Kubernetes资源管理集成。
- **性能工程与可观测性**：低开销PMC监控为性能归因和计费提供细粒度数据——云提供商可以精确知道每个租户的实际内存带宽消耗，进而实现基于实际使用量而非分配量的计费模型（fine-grained billing）。
- **系统软件方向**：动态内存分区策略可应用于NUMA系统和CXL共享内存环境——当多个主机通过CXL共享同一内存池时，内存带宽分区和隔离的需求更加突出，MTTM的分区框架可直接迁移。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.12 BASK: Batch And SmartNIC-offloaded KSM

**作者**：Chanshin Kwak, Jaehyeon Lee, Minkyu Jung, Changjun Lee, Youngjin Kwon
**机构**：KAIST
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

Linux KSM（Kernel Same-page Merging）是云环境内存去重的核心机制——通过扫描物理页面内容，发现相同内容的页面并合并为单一写时复制（CoW）页面，可节省大量物理内存。然而KSM的内容扫描和哈希比较消耗大量主机CPU资源，在典型云配置下可达单核100%利用率，与租户工作负载竞争CPU资源，限制了KSM的实际部署范围。

BASK通过软硬件协同设计将KSM卸载到SmartNIC上执行：首先将页面内容扫描批量化——累积一批待比较页面后统一发送到SmartNIC，避免逐页DMA传输的高开销；其次利用SmartNIC的可编程流水线和硬件哈希引擎高效完成页面哈希计算和内容比对，SmartNIC上的并行处理能力天然适合这类计算密集但逻辑简单的任务。BASK还扩展了KSM的扫描范围至跨主机——不同物理服务器上运行相同OS或应用的虚拟机常有大量相同页面，跨主机去重可进一步放大节省效果。在真实云工作负载下，BASK实现与CPU端KSM相近的去重率，同时几乎消除主机CPU开销，使内存去重从"有代价的优化"变为"几乎免费的能力"。

### 技术线索与启示

- **系统软件方向**：SmartNIC卸载内核功能的范式——将计算密集但逻辑规律的系统任务从通用CPU迁移到专用硬件——可推广到其他内核子系统：内存压缩/解压、加密/解密、CRC校验、数据复制（如sendfile的零拷贝路径中的校验和计算）都是SmartNIC卸载的候选目标。
- **云原生与分布式架构**：跨主机内存去重为云环境的成本优化提供了新的维度——在同一物理集群内，不同租户运行相同基础镜像和中间件的概率很高，跨主机KSM可大幅降低集群总内存占用。该技术与容器镜像分层存储理念一脉相承，但工作在线上的内存层面。
- **硬件-软件协同设计**：SmartNIC的DMA能力是内存操作的理想卸载目标——DMA可以绕过主机CPU直接访问主机内存，避免了内存复制和CPU缓存污染。BASK的设计模式展示了如何利用DMA+硬件加速器构建高效的卸载流水线。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.13 PaCaR: Page Cache Replication for NUMA I/O Locality

**作者**：Jérôme Coquisart, Julien Sopena, Redha Gouicem
**机构**：RWTH Aachen University, LIP6 - Inria
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

NUMA（非一致性内存访问）系统中，I/O密集型应用频繁面临跨NUMA节点的页面缓存访问——当应用运行在节点A而文件页面缓存在节点B的本地内存中时，每次I/O操作都需跨越NUMA互联网络，引入额外的延迟（通常50-150ns以上）并消耗宝贵的互联带宽。在配备高速NVMe SSD的现代服务器上，存储设备延迟已降至微秒级，跨NUMA访问的开销在I/O关键路径中变得不可忽视，严重削弱了高速存储设备的性能收益。

PaCaR通过在多个NUMA节点维护页面缓存副本来解决这一问题：当页面被I/O操作首次读入节点A的页面缓存时，同时将副本复制到节点B（预期将有本地访问需求的节点）。系统设计轻量级一致性协议——基于写无效（write-invalidate）策略，写操作时使远程副本失效而非同步更新，利用文件系统大多为读密集的特性（读写比通常7:3以上）将一致性维护开销降至最低。在配备NVMe SSD和多核服务器上的评估表明，PaCaR显著提升读密集型工作负载的文件系统IOPS，且对写密集负载影响可控。该方案的核心洞察是：在I/O路径中，复制页面缓存所消耗的额外内存和复制带宽远小于跨越NUMA边界进行远程内存访问的累积延迟损失。

### 技术线索与启示

- **系统软件方向**：NUMA感知的缓存复制可集成到Linux页面缓存管理层——作为VFS（虚拟文件系统）的一个可配置策略，类似当前内核中的reclaim策略。考虑到现代服务器NUMA节点数量持续增长（AMD EPYC可达8-12个NUMA域），此类优化的收益将随节点数增加而放大。
- **性能工程与可观测性**：跨NUMA延迟量化对系统性能调优具有普遍参考价值——许多看似"CPU密集"的工作负载实际上被跨NUMA内存访问所拖慢。PaCaR的分析方法论（识别I/O路径中的远程访问比例、量化远程访问的实际延迟代价）可推广到其他内核子系统的NUMA优化。
- **数据密集型系统**：数据库管理系统（DBMS）的缓冲池管理是页面缓存复制的典型受益者——MySQL/PostgreSQL的缓冲池本质上是一个应用层页面缓存，在多NUMA服务器上采用类似PaCaR的复制策略可避免跨NUMA缓冲池访问的性能损失。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.14 FUR: Fast and Unlimited Reads on Persistent Memory Transactions

**作者**：João Barreto, Daniel Castro, Paolo Romano, Alexandro Baldassin
**机构**：INESC-ID, IST Lisbon, Unesp
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

持久内存（PM，如Intel Optane）事务需要保证崩溃一致性——即系统崩溃后事务状态要么完全持久化、要么完全回滚。传统方案在每次读取事务数据时引入版本检查和拷贝开销：读取方必须记录"读过哪些数据"（维护读集），并在提交时验证这些数据未被并发事务修改。读集大小随事务读取的操作数线性增长，在读密集型事务中（如数据分析扫描），维护和验证读集的开销可能超过实际数据处理的成本。

FUR通过创新的数据版本管理彻底消除读集开销。核心设计是：每个数据项维护一个全局可见的版本号，事务提交时原子更新版本号；读操作不再记录读集，而是通过运行时版本比对检测冲突——如果在读取数据后版本号发生变化，说明存在并发冲突，事务回退重试。由于版本检查操作极轻量（通常仅为一次内存读取和比较），FUR实现接近零开销的读路径，且不受并发写事务数量的限制（传统方案中更多写事务意味着更多读集验证开销）。在读密集型负载上实现显著性能提升，尤其对大规模数据分析型事务效果突出。该方案展示了"不跟踪读集而通过版本优化检测冲突"这一设计模式在PM事务领域的有效性。

### 技术线索与启示

- **数据密集型系统**：PM事务读优化对内存数据库（如基于PM的Redis、Memcached变体）有直接价值——这些系统以读为主，事务读集开销是主要瓶颈。FUR的无读集方案可使内存数据库在PM上的事务吞吐接近DRAM纯内存性能。
- **系统软件方向**：无读集冲突检测的范式——"不记录读什么，只检测是否被改过"——可推广到其他事务系统，如HTAP数据库中的混合读写事务、分布式事务中的乐观并发控制。其本质是用极轻量级的版本检查替代重量级的读集维护。
- **性能工程与可观测性**：读写不对称优化在读多写少场景中普遍适用——大多数OLTP工作负载（如电商、社交）的读写比在10:1以上，FUR展示的不对称优化策略（读路径极致轻量、写路径保留适度开销）是此类场景下高性能事务系统的设计原则。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.15 Reducing GPU Memory Bottleneck with Lossless Compression for ML

**作者**：Aditya Kamath, Arvind Krishnamurthy, Marco Canini, Simon Peter
**机构**：University of Washington, Google, KAUST
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

ML工作负载的GPU HBM（高带宽内存）需求持续膨胀——大语言模型、扩散模型和高分辨率视觉模型的参数量和中间激活值常超过HBM物理容量（即使是80GB的H100也常不敷使用），导致频繁的HBM-DRAM换页（swapping）或重计算，严重损害训练和推理性能。现有方案要么依赖手工梯度检查点（engineering effort大）、要么使用有损压缩（精度损失不可控），尚缺乏自动化的无损内存压缩方案。

本文识别ML张量中的可压缩模式：权重张量因训练收敛后趋于平滑而具有高空间冗余性，激活张量因ReLU/GELU等激活函数的稀疏化效应而含有大量零值，梯度张量在训练后期通常具有低秩结构。基于这些模式，系统设计了GPU友好的透明压缩/解压内核——压缩和解压操作完全在GPU上执行（避免PCIe传输），解压延迟通过流水线与计算重叠以最小化对关键路径的影响。内核利用GPU的SIMT并行性实现高吞吐压缩，并针对不同张量类型（fp32/fp16/bf16）优化编码格式。在多种ML模型（涵盖NLP、视觉和生成式）上实现显著内存节省，同时训练和推理性能几乎不受影响。该方案为GPU内存扩展提供了可透明集成到PyTorch/CUDA的低侵入路径。

### 技术线索与启示

- **系统软件方向**：GPU内存透明压缩为深度学习框架提供了新的内存管理维度——可设计类似操作系统虚拟内存的"GPU虚拟内存"层，在HBM和压缩后的HBM之间自动迁移张量。该技术可集成到PyTorch的allocator和CUDA的显存管理接口中，对上层模型代码完全透明。
- **Agent与LLM应用方向**：内存压缩直接降低LLM部署成本——在消费者级GPU（如RTX 4090 24GB）上部署70B模型时，即使4-bit量化仍需要约40GB，内存压缩可进一步将内存需求拉低到消费级硬件可承受范围，推动LLM推理的民主化。
- **硬件-软件协同设计**：GPU硬件压缩加速器（类似NVIDIA的nvcomp但面向ML张量）可与软件方案协同——未来GPU可能集成专用的张量压缩/解压硬件单元，软件的压缩模式识别和调度策略将引导硬件的压缩管线选择。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.16 Carbon-Aware Continuous Learning for Sustainable Real-Time ML

**作者**：Gwanjong Park, Osama Khan, Dongho Ha, Myeongjae Jeon, Euiseong Seo
**机构**：Sungkyunkwan University, POSTECH
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

持续ML模型更新（Continuous Learning）是保持模型时效性的必要手段——推荐系统需适应变化的用户偏好、异常检测需应对新型攻击模式、时序预测需跟踪概念漂移。然而持续训练消耗大量能源，且电力碳排放强度随电网能源结构实时波动（如夜间高比例煤电、午间高比例光伏），固定时刻的训练可能恰好落在电网碳强度峰值。

本文提出碳感知（Carbon-Aware）持续学习框架：实时监控电网碳排放强度数据（通过公开API如Electricity Maps获取），在低碳窗口（如可再生能源充沛时段）调度训练任务；同时结合精度预测模型评估延迟训练对模型质量的影响——当延迟过久可能导致精度显著退化时，即使碳强度较高也触发训练以保证服务质量。框架在精度退化和碳足迹之间进行动态权衡，使用多目标优化控制器在保持模型精度的同时显著降低碳足迹。实验覆盖推荐系统和异常检测等典型持续学习场景，展示了在精度损失可忽略的约束下实现碳排放降低的实际可行性。该方案为AI系统的可持续发展提供了将外部环境信号纳入调度决策的实用框架，其碳感知调度模式可推广到批处理训练、模型评估等更广泛的AI运维任务。

### 技术线索与启示

- **绿色计算与可持续性**：碳感知调度是AI可持续发展的重要方向——不仅是学术概念，在欧盟碳边境调节机制（CBAM）和科技企业碳中和承诺的压力下，碳感知调度正从"锦上添花"变为"合规刚需"，对AI服务提供商的ESG报告有直接价值。
- **系统软件方向**：碳感知调度器可集成到Kubernetes的自定义调度扩展（scheduler extender）中，与现有的资源感知调度（CPU/内存/GPU）并列为一个新的调度维度。更远期看，碳强度可成为云原生调度器的第一公民属性，类似当前的资源请求和亲和性。
- **Agent与LLM应用方向**：LLM训练和推理的碳足迹日益受关注——单次GPT-4级别模型训练碳排放可达数百吨CO₂，持续微调和在线学习进一步放大碳足迹。碳感知训练调度可将大模型更新安排在低碳时段，大幅降低AI碳足迹而不影响模型服务质量。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.17 FlexiQ: Adaptive Mixed-Precision Quantization

**作者**：Jaemin Kim, Hongjun Um, Sungkyun Kim, Yongjun Park, Jiwon Seo
**机构**：SNU, Hanyang University, Yonsei University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

DNN量化通过降低权重和激活值位宽来压缩模型，但不同层对量化的敏感度差异巨大——注意力层通常对精度高度敏感需要保持较高位宽，而FFN（前馈网络）层和嵌入层可以容忍更激进的量化。传统统一位宽量化要么过度压缩敏感层导致精度不达标（如INT4对注意力层造成显著精度下降），要么保守压缩非敏感层导致延迟和内存浪费（如INT8统一量化未充分利用压缩潜力）。

FlexiQ设计敏感度驱动的自适应混合精度量化框架：首先通过逐层敏感度分析（基于Hessian矩阵或梯度幅值）量化各层对精度损失的容忍度；然后求解带约束优化问题——在给定端到端延迟约束下最大化模型精度，或在给定精度下限约束下最小化延迟——自动为每层分配最优位宽（范围从INT2到INT8）。框架支持运行时动态调整：当设备负载变化（如后台任务启动）或电池状态改变时，可在不重新加载模型的情况下切换精度配置。在Vision Transformer、BERT和CNN等模型上验证了混合精度策略相比统一位宽量化的优越性——在相同延迟预算下精度更高，或在相同精度要求下延迟更低。该方案将模型量化从"一刀切"的粗粒度优化提升为"逐层定制"的细粒度优化。

### 技术线索与启示

- **边缘计算与端侧部署**：混合精度量化对移动端和嵌入式部署至关重要——设备端的延迟和功耗预算随时变化（充电/放电、性能模式切换），FlexiQ的运行时动态精度切换使模型能自适应设备状态，是端侧AI工程化部署的刚需能力。
- **性能工程与可观测性**：敏感度驱动的位宽分配是一种通用的精度-效率权衡方法论——不仅适用于量化，可扩展到剪枝比率分配、知识蒸馏的层权重、混合专家（MoE）模型的专家激活策略等场景，其本质是通过测量各组件对输出质量的边际贡献来指导资源分配。
- **Agent与LLM应用方向**：LLM量化中不同层的重要性差异更大——注意力层和第一个/最后一个Transformer层通常对精度影响最大，FlexiQ的敏感度分析可直接指导LLM的混合精度量化方案，避免对关键层过度压缩导致的性能退化。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.18 Million-Scale Text-to-Video Retrieval with Hyperdimensional Computing

**作者**：Hyunsei Lee, Jaewoo Gwak, Shinhyoung Jang, Junyoung Lee, Yeseong Kim
**机构**：DGIST
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

百万级文本到视频检索（如视频搜索引擎、内容审核、数字资产管理）面临严峻的计算和存储挑战：传统向量搜索方案需存储每视频的高维浮点特征向量（通常512-1024维），内存占用随视频库规模线性增长（百万视频×512维×4字节≈2GB），且检索延迟随数据量增加快速上升。近似最近邻（ANN）索引虽可加速搜索但引入精度损失和额外内存开销。

本文利用超维计算（Hyperdimensional Computing, HDC）的独特性质解决这一瓶颈：HDC使用超高维（通常10000维）二值（+1/-1）向量作为信息表示，文本和视频特征分别编码为HDC超向量后，通过绑定（binding）、捆绑（bundling）和联想记忆等代数操作实现高效相似度检索。HDC的核心优势在于：二值运算天然适合硬件加速（XOR和popcount替代浮点乘加）、超向量维度对噪声和量化极其鲁棒、联想记忆支持单次前向检索无需建索引。在百万规模数据集上的评估表明，HDC方案在检索效率和精度上均优于传统浮点向量+ANN方案，且二值超向量的内存占用仅为浮点向量的1/32。该工作为大规模多模态检索引入了全新的计算范式，将类脑计算的超维表示从理论推向实用的工程系统。

### 技术线索与启示

- **数据密集型系统**：HDC为大规模多模态检索提供了全新的计算范式——不同于传统的"高维浮点→降维→ANN索引"管线，HDC用"超高维二值→绑定捆绑→联想检索"的管道，其底层数学基础（高维随机向量的准正交性）保证了检索质量。该范式对跨模态检索（文本-图像、文本-音频）具有普遍适用性。
- **硬件-软件协同设计**：HDC二值运算天然适合FPGA和ASIC加速——XOR和popcount是数字电路中最基础的操作，HDC加速器可以用极小的硅面积和功耗实现极高的吞吐。并且HDC计算具有大规模并行性（所有维度独立运算），与存内计算（Processing-in-Memory）架构高度契合。
- **Agent与LLM应用方向**：AI Agent的多模态检索（如检索相关图片/视频后作为LLM的上下文）可利用HDC高效搜索——Agent的检索请求通常要求低延迟，而HDC的单次联想检索无需ANN索引的图遍历开销，可将端到端响应延迟控制在毫秒级。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.19 Matrix-PIC: Matrix Outer-product for Particle-in-Cell Simulations

**作者**：Yizhuo Rao, Xingjian Cui, Jiabin Xie, Shangzhi Pang, Guangnan Feng, Jinhui Wei, Zhiguang Chen, Yutong Lu
**机构**：Sun Yat-sen University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

PIC（Particle-in-Cell）方法是等离子体物理、空间物理和加速器物理中的核心模拟技术，其计算模式是将连续场离散化到网格上、再将粒子与网格交互求解运动方程。然而PIC模拟中粒子-网格交互步骤（粒子属性插值到网格、网格力插值回粒子）产生大量不规则内存访问和标量计算，传统GPU实现中这些操作无法充分利用GPU的大规模并行性和Tensor Core。

Matrix-PIC提出将核心粒子-网格交互计算重构为矩阵外积操作以利用GPU Tensor Core的极高吞吐。具体而言：将粒子属性向量和网格权重向量组织为矩阵形式，粒子到网格的插值映射为外积稀疏矩阵×向量操作，网格到粒子的力插值映射为对应的转置矩阵乘法。这种重构将传统PIC中的逐粒子标量循环转化为Tensor Core原生的矩阵运算，大幅提升GPU计算单元利用率。在多种PIC模拟场景（静电、电磁、相对论）上实现显著性能提升，展示了科学计算与AI硬件协同的巨大潜力——许多传统科学计算中的稀疏交互模式可以通过巧妙的线性代数重构转化为密集矩阵运算，释放AI加速器的算力。

### 技术线索与启示

- **性能工程与可观测性**：科学计算重构为矩阵操作以利用Tensor Core是一种通用GPU优化策略——分子动力学中的邻域力计算、有限元中的刚度矩阵组装、N体问题中的引力计算等都可以通过类似的外积重构受益。核心原则是"找到计算中的隐式矩阵结构并将其显式化"。
- **硬件-软件协同设计**：Tensor Core不仅是AI加速器也是通用科学计算加速器——当前许多HPC应用仅使用CUDA Core而忽略Tensor Core，Matrix-PIC展示了一条挖掘Tensor Core算力的实用路径。这为科学计算社区提供了一种新的性能优化思维：与其等待专用硬件，不如将计算模式适配已有AI硬件。
- **系统软件方向**：矩阵化重构的思想可推广到其他粒子/网格耦合仿真——如流体力学中的SPH（光滑粒子流体动力学）、材料科学中的相场模拟。构建通用的"稀疏交互→密集矩阵"编译器或代码生成工具可自动完成这一转换，降低科学计算代码的优化门槛。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.20 Elastic QEC Decoders

**作者**：Satvik Maurya, Abtin Molavi, Aws Albarghouthi, Swamit Tannu
**机构**：University of Wisconsin-Madison
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

量子纠错（Quantum Error Correction, QEC）是容错量子计算的基础——通过编码逻辑量子比特到多个物理量子比特并持续解码错误模式来维持量子态的完整性。传统QEC解码器按最坏情况错误率设计：假设所有物理量子比特都处于高噪声状态，部署最强的纠错算法（如最小权重完美匹配或最大似然解码），导致解码延迟和功耗固定在高位，即使在量子芯片噪声较低的运行窗口也不例外。

本文提出弹性QEC解码器：根据实时物理错误率动态调整解码精度和资源分配。当错误率低时（如低温环境、新鲜校准后），使用轻量级解码器快速纠正稀疏错误，降低解码延迟和系统功耗；当错误率上升时（如温度漂移、退相干加剧），无缝切换到高精度解码器以保证逻辑量子比特保真度。弹性切换基于运行时错误症状（syndrome）的统计特征——例如错误症状的密度和关联模式——自动判断当前噪声水平并选择适配的解码策略。在多种量子设备和噪声模型上验证了弹性策略的优势：与固定最强解码器相比，在低噪声窗口实现延迟和功耗的大幅降低，同时在高噪声窗口保持等价纠错能力。该方案将经典计算系统中"按需分配资源"的思想引入量子计算栈，对即将到来的含噪中等规模量子（NISQ）时代的系统效率有重要意义。

### 技术线索与启示

- **系统软件方向**：弹性纠错思想——根据实际错误率而非设计最坏情况分配计算资源——可推广到经典容错系统，如纠删码存储系统的自适应冗余度调整、网络传输的自适应FEC（前向纠错）编码率调整、内存ECC的自适应校验粒度等，核心原则是"为实际发生的错误付费，不为可能的错误预留"。
- **绿色计算与可持续性**：动态调整纠错精度直接降低量子计算系统的功耗——高精度QEC解码的计算复杂度通常随码距指数增长，在低噪声时避免不必要的高精度解码可大幅降低经典控制电子学的功耗，这对量子计算机的总功耗预算（其中经典控制占比远高于量子芯片本身）具有显著影响。
- **开放性问题与未来方向**：量子-经典混合系统的纠错策略协同设计是重要开放领域——弹性QEC需要在量子比特保真度、经典解码延迟和系统功耗之间做三方权衡，且该权衡与量子算法对错误率的容忍度相关（如变分算法比质因数分解容忍度更高），构建跨量子-经典边界的统一调度框架是下一代量子操作系统的核心挑战。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.21 Prediction-Informed Power Management for Compute Servers

**作者**：Jonggyu Park, Simon Peter, Thomas E. Anderson
**机构**：University of Washington
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

现有服务器功耗管理基于简单启发式规则（如Linux的P-state governor——根据过去一段时间CPU利用率选取DVFS频率），核心缺陷在于：启发式规则只能响应过去的负载，无法预测即将到来的负载变化，导致响应滞后和功耗-性能权衡次优。例如，当CPU利用率突然升高时，频率提升发生在性能已经受损之后；当负载即将结束时，频率降低又过于保守。

本文利用轻量级ML模型预测即将到来的功耗特征，提前调整CPU频率和电压以匹配预期需求。系统的核心设计包括：（1）训练硬件性能计数器（PMC）信号到未来短期功耗的映射模型，利用PMC的细粒度时序信息（如缓存未命中率、指令退休率、分支预测失败率）捕捉负载变化的早期信号；（2）预测模型集成到内核的调度和DVFS路径中，在每次调度决策点查询预测结果并据此设置频率；（3）预测置信度阈值控制机制——当预测不确定性高时回退到保守的启发式策略，避免误预测导致的过度降频。在多种服务器工作负载（Web服务、数据库、批处理）上验证了预测驱动策略相比传统on-demand和conservative governor的优势：在保持应用尾延迟和吞吐量的同时，实现更精细的功耗控制和更低的平均功耗。该方案将服务器的功耗管理从"被动的观察-反应"循环升级为"主动的预测-调整"闭环。

### 技术线索与启示

- **绿色计算与可持续性**：预测驱动功耗管理是数据中心碳减排的有效手段——全球数据中心年耗电约300TWh，其中CPU功耗占服务器总功耗的30-50%。预测驱动的精细DVFS可降低CPU平均功耗10-20%，汇总到数据中心级别即为显著的碳排放和电费节省。
- **性能工程与可观测性**：硬件性能计数器的预测价值远超传统使用场景——PMC通常仅用于性能分析和调试，本文展示了PMC作为"负载变化预警信号"的潜力。该思想可推广到内存带宽预测、I/O压力预测、网络流量预测等资源管理场景，将PMC从诊断工具升级为控制系统的传感器。
- **系统软件方向**：OS级功耗预测可替代启发现有的启发式DVFS governor——Linux内核社区的cpufreq子系统架构允许插入自定义governor，预测驱动governor可以作为新的governor类型（类似现有的performance/powersave/ondemand）合入主线，为更广泛的用户提供开箱即用的功耗优化。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.22 On-device Semantic Selection: Monolithic Forwarding

**作者**：Jiahao Zhou, Chengliang Lin, Dingji Li, Mingkai Dong, Haibo Chen
**机构**：Shanghai Jiao Tong University, Huawei
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

设备端语义选择（On-device Semantic Selection）是移动AI应用的关键能力——例如相机应用需同时执行场景分类（决定拍摄模式）、目标检测（定位人脸/物体）和语义分割（识别前景/背景），每个任务通常由独立模型完成。依次执行多个模型导致总延迟叠加，并行执行则内存占用叠加，对资源受限的移动设备构成严峻挑战。

本文提出单体转发（Monolithic Forwarding）技术：将多个语义任务的模型融合为统一的推理路径。其核心设计是共享中间层计算——多个任务模型的底层特征提取（边缘检测、纹理分析、形状编码）高度重叠，通过设计共享的骨干网络提取通用视觉特征，仅在最顶层按任务需求分叉出轻量级任务头（task-specific heads）。单体转发在一次前向传播中同时产生所有任务的输出，消除了多模型推理的重复计算和多次内存访问，显著降低总延迟和内存占用。在移动设备上验证了场景分类+目标检测+语义分割等多任务组合的加速效果，为设备端多任务AI推理提供了"一次推理、多任务输出"的高效执行模型。

### 技术线索与启示

- **边缘计算与端侧部署**：多任务融合推理是设备端AI的关键优化方向——移动设备的AI负载正从单一任务向多任务组合演化（如AR应用同时需要手势识别+场景理解+深度估计），单体转发模式为这种趋势提供了可扩展的架构基础。
- **Agent与LLM应用方向**：AI Agent的语义路由可利用单体转发降低决策延迟——Agent需要同时判断用户意图（分类）、提取关键实体（NER）、评估风险（异常检测），这些语义选择任务可通过共享编码器+独立任务头的方式融合，减少Agent决策链的端到端延迟。
- **系统软件方向**：模型融合推理的设计模式可集成到端侧推理引擎（如TensorFlow Lite、MediaPipe、ncnn）中，以"多任务模型图"的形式提供给开发者，自动进行共享层的识别和融合，降低开发者手动设计多任务模型的门槛。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.23 LightDSA: Efficient DSA Through Hardware-Aware Transparent Optimization

**作者**：Yuansen Wang, Teng Ma, Yuanhui Luo, Dongbiao He, Zheng Liu, Yunpeng Chai
**机构**：Renmin University of China, Alibaba Group, CNIC CAS
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

数字签名算法（DSA）是现代互联网安全的基石——TLS握手、代码签名、DNS安全扩展（DNSSEC）等关键安全协议均依赖DSA进行身份验证和完整性保护。然而DSA中的模幂运算和椭圆曲线点乘是计算密集操作，在高吞吐网络场景中（如CDN边缘节点的百万级TLS握手/秒、API网关的请求签名验证）DSA计算成为系统瓶颈，占用大量CPU资源。

LightDSA的核心理念是"透明优化"——在不修改上层应用代码的前提下，通过硬件感知的执行调度提升DSA性能。系统分析DSA计算中的多种并行可能性：数据级并行（多个签名/验证操作独立可并行）、指令级并行（模乘和模加可在不同执行单元同时进行）、算法级并行（批量验证中的多标量乘法）。LightDSA自动识别当前硬件平台的能力（SIMD指令集版本、专用加密加速器是否可用、乱序执行窗口大小），并选择最优执行策略——例如在有AVX-512的平台使用向量化的蒙哥马利乘法、在有ARM Crypto Extensions的平台卸载到硬件指令、在通用平台上使用SIMD软件实现。在多种硬件平台（x86、ARM、RISC-V）上实现DSA计算的显著加速，且对上层应用完全透明。该方案将密码学加速从"应用感知的手工优化"转变为"运行时自适应的自动优化"。

### 技术线索与启示

- **安全与可信计算**：高性能DSA对TLS性能至关重要——CDN和云服务提供商每秒处理数百万TLS握手，DSA计算可能占总CPU时间20-30%。LightDSA的透明加速可直接提升TLS吞吐、降低TLS握手延迟，对互联网基础设施的安全-性能平衡具有工程价值。
- **系统软件方向**：硬件感知密码学加速的方法论可推广到其他密码学原语——对称加密（AES-GCM）、哈希（SHA-3）、后量子密码（Kyber/Dilithium）的软件实现都可以受益于类似的自适应执行策略。特别是后量子密码的计算开销远高于传统密码，硬件感知优化对其实际部署尤为关键。
- **性能工程与可观测性**：透明优化是理想的系统优化目标——在不改变API接口的前提下通过运行时自适应提升性能，降低应用开发者的认知负担。LightDSA展示的"探针-选择-执行"模式（探测硬件能力→选择最优策略→执行）是一种通用的透明优化框架，可应用于压缩、编码、序列化等场景。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.24 GPU Kernel Idempotency Validation

**作者**：Mingcong Han, Weihang Shen, Rong Chen, Haibo Chen
**机构**：Shanghai Jiao Tong University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

GPU内核幂等性（idempotency）——即同一内核在相同输入下重复执行产生一致的输出且无副作用——是故障恢复和容错计算（如检查点/重启、推测执行、精确异常处理）的基础性质。然而判定一个GPU内核是否幂等极具挑战：GPU内核常包含原子操作（atomicAdd、atomicCAS）和全局内存写入，这些操作的执行顺序和中间状态受线程调度影响，不同执行实例可能产生不同但都正确的输出。

本文提出在GPU内核启动时通过静态分析和轻量级运行时检查快速判定幂等性的方法。静态分析阶段扫描PTX/SASS指令序列，识别可能破坏幂等性的操作模式（如非原子写后读、未初始化的输出缓冲区、依赖于warp执行顺序的行为）；运行时检查在首次内核启动时监控全局内存访问模式，通过影子内存跟踪写入位置和顺序。两者结合在微秒级内完成幂等性判定，且分析开销在后续重复启动时完全消除（结果缓存）。在CUDA SDK样本、深度学习内核和科学计算内核上的评估验证了检测的高准确性和极低的启动延迟开销。该方案为GPU容错系统提供了轻量级的幂等性保证机制，使编译器和运行时系统可以安全地应用基于幂等性的优化（如自动检查点插入、失败重试）。

### 技术线索与启示

- **系统软件方向**：幂等性验证可集成到CUDA编程模型和编译器工具链——类似于Rust编译器的借用检查确保内存安全，幂等性检查器可以在编译时和启动时确保内核的安全性，为GPU运行时系统（如CUDA Graph、CUDA Stream）的自动容错优化奠定基础。
- **性能工程与可观测性**：启动时低开销验证的设计模式——将昂贵的程序分析拆分为"一次性的启动时分析+结果缓存+后续零开销"——对其他GPU安全检查（如内存越界检测、数据竞争检测）具有直接借鉴意义。GPU内核的重复启动特性使得任何一次性分析开销都可以被充分摊销。
- **安全与可信计算**：幂等性保证是GPU故障恢复和可信计算的基础——在不可靠硬件（如消费级GPU）上进行长时间训练时，幂等性允许训练框架安全地重试失败的内核启动而不产生副作用。在机密计算场景中，幂等性也是远程验证GPU计算完整性的前提。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.25 swKokkos: Athread Backend for Sunway

**作者**：Junlin Wei, Jinrong Jiang, Wu Wang, Chen Li, et al.
**机构**：CNIC CAS, Pengcheng Laboratory, Laoshan Laboratory
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

神威（Sunway）系列超算采用独特的主从核异构架构——每个计算节点包含管理核心（MPE）和大量从核（CPE）组成的加速阵列，从核阵列通过Athread编程模型暴露。这一架构在提供极高理论算力的同时，也给应用移植带来巨大挑战：现有高性能计算应用大多基于CUDA、OpenMP或Kokkos等通用编程框架开发，无法直接运行在神威从核阵列上，手工移植每个应用到Athread模型工作量大、可维护性差且容易出错。

swKokkos通过为神威从核阵列实现Kokkos并行编程框架的完整后端来解决这一可移植性鸿沟。Kokkos是面向高性能计算的C++并行编程框架，通过Execution Space和Memory Space抽象将应用算法与硬件后端解耦。swKokkos将Kokkos的并行原语（parallel_for、parallel_reduce、parallel_scan）映射到Athread的从核线程模型，优化数据搬运（DMA）策略以利用从核的本地内存带宽优势——包括自动识别频繁访问的数据并预加载到从核的SPM（Scratchpad Memory）、采用双缓冲策略隐藏DMA传输延迟、以及设计NUMA感知的数据分布以最小化跨从核阵列的数据移动。使现有大量Kokkos应用无需修改即可高效运行在神威平台上，大幅降低了国产超算平台的软件移植成本和生态建设门槛。

### 技术线索与启示

- **系统软件方向**：为标准框架实现国产超算后端是降低平台迁移成本的关键策略——通过在一个广泛使用的框架中实现单一后端，即可解锁该框架生态中的大量现有应用。这一策略对曙光（HIP/CUDA兼容）、华为昇腾（CANN）、寒武纪（BangLang）等国产加速器均有借鉴价值。
- **硬件-软件协同设计**：Kokkos适配经验为其他国产硬件的软件生态建设提供了可复制的方法论：识别框架的抽象层次（Execution Space/Memory Space）→映射到硬件的执行模型（Athread/线程块）→优化数据移动（DMA/SPM）→验证性能可移植性。这一流程可标准化为国产硬件软件栈的"框架适配模板"。
- **性能工程与可观测性**：Athread后端优化中数据搬运和SPM管理的策略对使用类似架构的其他异构加速器（如Intel GPU的共享本地内存、AMD APU的scratchpad）有借鉴意义——核心挑战都是如何在透明编程模型中自动做出最优的数据局部性决策。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.26 MinatoLoader: Accelerating ML Training Through Data Preprocessing

**作者**：Rahma Nouaji, Stella Bitchebe, Ricardo Macedo, Oana Balmau
**机构**：McGill University, INESC TEC & U Minho
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

ML训练管道中数据预处理——包括图像解码、随机裁剪、翻转增强、归一化、文本tokenization、视频帧提取——已日益成为GPU等待的主要瓶颈。随着GPU计算能力持续翻倍（从V100到H100的4年间单卡算力增长超5倍），而CPU和存储I/O增速相对滞后，数据预处理环节的"供给不足"导致昂贵的GPU频繁处于空闲状态（stall），训练吞吐远低于硬件理论峰值。

MinatoLoader识别并消除数据预处理中的三大冗余来源：（1）跨epoch重复计算——相同原始数据在每个epoch中被重复解码和增强，MinatoLoader引入预处理结果缓存，跨epoch复用确定性变换的输出；（2）同batch内相似样本的冗余变换——同一batch中样本常共享相同的增强参数（如同步随机翻转），MinatoLoader通过批量变换消除逐样本重复的元操作；（3）I/O与计算的不平衡——CPU预处理和GPU训练构成生产者-消费者流水线，MinatoLoader自适应调整CPU线程数、预取深度和内存缓冲大小以匹配GPU消费速率。在图像分类（ImageNet）、目标检测（COCO）和文本训练（C4）等多种任务上显著提升GPU利用率和端到端训练吞吐。该方案将数据预处理从训练的"黑盒附属环节"升级为"可优化的一等组件"。

### 技术线索与启示

- **数据密集型系统**：数据预处理是ML训练的隐藏瓶颈——许多团队投入大量资源优化模型架构和训练超参数，却忽视了训练耗时中30-50%可能消耗在GPU等待数据上。MinatoLoader揭示了预处理优化的巨大杠杆效应：预处理吞吐的每百分比提升直接转化为GPU利用率的提升和训练时间的缩短。
- **性能工程与可观测性**：预处理去冗余和自适应资源分配可集成到PyTorch DataLoader和TensorFlow tf.data中——当前DataLoader的配置（num_workers、prefetch_factor）依赖手动调参且静态不变，MinatoLoader的自适应调整为数据加载管道的自动调优提供了路线图。
- **系统软件方向**：预处理去冗余的思想可推广到其他数据密集型计算管道——ETL（提取-转换-加载）管道、流数据处理、科学工作流等场景中普遍存在跨运行和批内的重复计算，类似MinatoLoader的缓存+批量变换策略可普遍降低这些场景的计算开销。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.27 Multipath Collective Communication in GPU Clouds

**作者**：Yuchen Xu, Jianglong Nie, Baojia Li, et al.
**机构**：Peking University, Tencent
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

GPU云中大规模分布式训练依赖高效的集合通信（collective communication）原语——AllReduce、AllGather、ReduceScatter等——在数百至数千GPU间同步梯度和模型参数。然而，GPU云的网络拓扑具有层次化特征：同一节点内的GPU通过超高带宽的NVSwitch/NVLink互联（scale-up），跨节点GPU通过RDMA网络互联（scale-out）。这种拓扑不对称导致跨scale-up域（即跨NVSwitch域）的集合通信成为瓶颈：单条物理链路带宽被多个GPU共享，集合通信吞吐受限于域间链路聚合带宽。

本文利用多条网络路径同时传输以突破单路径带宽限制。系统设计了多路径感知的集合通信调度和数据分割策略：（1）拓扑发现——自动探测GPU集群的层次化网络拓扑（NVSwitch域、RDMA路径、交换机层级）并识别可用的并行路径；（2）多路径数据分割——根据各路径的可用带宽和延迟动态分配数据分片，带宽高的路径分配更多数据，同时确保所有路径的数据同时到达以最小化同步等待；（3）拥塞感知路径选择——实时监控各路径的拥塞状态，避开拥塞链路动态调整路径集合。在腾讯GPU云生产环境中（千卡级别集群）验证了多路径集合通信相比单路径NCCL的显著吞吐提升，直接转化为大规模模型（如GPT类、推荐模型）训练的迭代时间缩短。该方案将传统多路径路由的思想引入GPU集合通信领域，解决了scale-up/scale-out拓扑不对称下的带宽利用率问题。

### 技术线索与启示

- **云原生与分布式架构**：多路径集合通信对大规模分布式训练至关重要——随着模型规模增长（万亿参数模型需要数千甚至上万GPU协同训练），集合通信的开销占总训练时间的比例持续上升（可达30-50%），多路径优化是维持训练可扩展性的必要条件。
- **系统软件方向**：多路径感知NCCL扩展可集成到主流训练框架（PyTorch Distributed、DeepSpeed、Megatron-LM）中——在NCCL的通信plan生成阶段加入多路径拓扑感知，使上层框架无需修改即可受益于多路径带宽聚合。该技术与SHARP（交换机内聚合）和网内计算结合可进一步放大收益。
- **性能工程与可观测性**：网络拓扑感知调度对其他分布式计算（如分布式推理、分布式数据处理）有参考价值——任何需要在层次化网络中传输大量数据的分布式系统都可以通过拓扑感知的数据分割和路径选择提升带宽利用率。

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.28 Gopher: Dynamic Graph Pattern Mining via DAG-Driven Execution

**作者**：Yi Zhang, Yu Huang, Chaoqiang Liu, et al.
**机构**：HUST, Michigan Tech, UNSW
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

动态图模式挖掘是图计算领域的核心挑战，涵盖子图计数、模式匹配和图同构判断等关键任务。这类计算在高动态变化的图上运行时，面临两大核心问题：一是中间结果的重复计算导致大量资源浪费，二是图拓扑持续演化使得状态管理极其困难。传统方法通常在每次图更新时重新执行完整的模式发现流程，忽略了更新操作之间的大量计算可复用性，导致吞吐和延迟均不理想。

Gopher提出了一套基于DAG驱动的执行框架来解决上述问题。其核心思想是将动态图模式挖掘的计算逻辑组织为有向无环图（DAG），通过拓扑级别的依赖分析识别并消除跨时间步的冗余计算。具体而言，Gopher在每次图更新时仅重新计算DAG中受影响的节点，而非执行全量重算。在此之上，系统基于拓扑顺序实施并行调度——将无依赖关系的DAG节点分配到多个执行单元上同步推进，并结合内存管理策略优化中间结果的缓存和淘汰，在提升计算吞吐的同时控制内存占用。该设计在多类图挖掘基准测试上取得了显著加速效果，证明了DAG驱动的去冗余策略在动态图分析场景中的有效性。

### 技术线索与启示

- **数据密集型系统**：DAG驱动的计算去冗余思想不仅适用于图模式挖掘，还可推广到其他增量图分析任务（如社区发现、链接预测），为实时图计算引擎的设计提供了新范式
- **系统软件方向**：动态图的增量计算机制对实时图数据库（如Neo4j、TigerGraph）的快照更新和流式查询优化有直接参考价值，可融合到现有图查询引擎中提升更新吞吐
- **性能工程与可观测性**：DAG拓扑感知调度策略对不规则计算密集型工作负载（如稀疏矩阵运算、分子动力学模拟）的资源分配和负载均衡有普遍借鉴意义

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.29 AEP: Hierarchical Fault Tolerance in DSM

**作者**：Zixuan Wang, Qi Wu, Hang Huang, Jia Rao, Hui Lu, Hao Fan, Zhuo Huang, Song Wu, Hai Jin
**机构**：HUST, UT Arlington
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

分布式共享内存（DSM）系统在多节点场景下面临节点故障的双重挑战：既要保证数据一致性又要维持高可用性。传统容错方案通常采用全局检查点机制——每次故障后所有节点回滚到统一快照，带来显著的性能和空间开销。随着DSM系统规模扩大和内存容量增长，全局回滚的代价变得难以承受，特别是在细粒度共享内存访问模式下，一次局部故障就可能导致大量无关操作的无效回滚。

AEP提出了一套层次化原子执行保护框架来解决这一困境。其核心设计是将DSM中的共享内存操作分解为可独立原子回滚的执行单元，每个单元对应一个逻辑上的保护域。当某节点发生故障时，系统仅回滚与该故障节点直接相关的执行单元，而非回滚全局状态，其他未受影响节点可继续推进。在此基础上，AEP提供不同层次的差异化容错策略——对关键元数据和一致性状态采用强一致性保护，对普通数据页采用更轻量的最终一致性保障，从而在可靠性和性能开销之间实现精细化的按需配置。该方案在多种DSM系统原型上验证了层次化容错在降低恢复开销和提升系统整体可用性方面的显著优势。

### 技术线索与启示

- **云原生与分布式架构**：层次化容错思想可直接应用于分布式数据库的事务管理（如CockroachDB、TiDB），通过按数据粒度或事务类型实施差异化恢复策略，在保证ACID的同时降低事务回滚开销
- **系统软件方向**：原子执行保护单元的概念对分布式内存系统、分布式缓存（如Redis Cluster）和分布式文件系统的故障恢复有普遍参考价值，可扩展到远程直接内存访问（RDMA）场景
- **性能工程与可观测性**：差异化容错策略体现了在可靠性和开销之间进行动态权衡的系统设计范式——按需配置保护级别，而非采用一刀切的全局强保证，这对大规模云服务的SLO驱动架构设计有借鉴意义
- **边缘计算与端侧部署**：该方法在资源受限的边缘DSM场景中尤为适用，局部化故障恢复避免了全量回滚对边缘节点计算和带宽资源的冲击

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.30 PARD

已在Part 2 (2.16)中涵盖。

---

## 12.31 Laminar

已在Part 1 (1.16)中涵盖。

---

## 12.32 EMVOD: Elastic Multi-Path QUIC Scheduling for CDN VoD

**作者**：ZiQi Wei, Qing Li, TianYun Zhao, Cheng Luo, ChangKui OuYang, XiaoFei Yu, DaYi Zhao, Yong Jiang
**机构**：Tsinghua SIGS, Peng Cheng Laboratory, Tencent
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

CDN视频点播（VoD）场景中，用户期望高质量、零卡顿的观看体验，但网络环境具有高度动态性和不可预测性。多路径传输协议（如MP-QUIC）为提升传输可靠性提供了可能，然而在多条异构路径（如WiFi+蜂窝网络）之间进行最优的流量分配和路径选择是极具挑战性的决策问题。固定比例或静态策略无法适应实时网络波动，容易出现部分路径拥塞而其他路径闲置的不均衡现象，导致视频缓冲和卡顿，损害用户体验。

EMVOD针对CDN VoD场景设计了一套弹性多路径调度策略，运行于QUIC多路径传输协议之上。系统实时监测每条路径的带宽、延迟和丢包率等网络指标，结合视频播放缓冲区的当前状态，动态调整各路径上的数据分配比例。核心创新在于将视频内容的优先级属性与路径质量进行匹配：对即将播放的高优先级数据块，优先选择低延迟、高可靠路径传输；对可预取的未来数据块，则利用剩余路径带宽进行后台传输。该弹性调度策略在腾讯CDN生产环境中进行了验证，在多变的网络条件下明显提升了平均视频质量和启动速度，同时有效降低了卡顿事件的发生频率，证明了多路径智能调度在大规模VoD服务中的实际价值。

### 技术线索与启示

- **系统软件方向**：基于QUIC的多路径弹性调度机制可集成到新一代视频传输协议栈中，为CDN边缘节点和客户端之间的传输层提供智能化的路径管理能力
- **性能工程与可观测性**：实时网络感知与内容优先级匹配的联合优化框架对任何需要区分服务质量等级的多路径传输场景（如实时会议、云游戏）都有参考价值
- **边缘计算与端侧部署**：移动设备的多网络接口（WiFi+蜂窝）利用是提升移动视频体验的关键手段，EMVOD的调度策略可融入移动端视频播放SDK，直接惠及终端用户

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.33 Mitigating CDN Cache Misses: Origin Shield for Billion-QPS

**作者**：Zixuan Yang, Yimeng Xu, Jiaqi Zheng, Boxi Liu, Guihai Chen, Quan Xia, He Lin, Zhihai Huang, Shangce Yuan
**机构**：Nanjing University, Central China Normal University, Tencent
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

十亿QPS规模的社交平台CDN系统面临极端缓存压力：高频热点内容的缓存未命中会瞬间将海量请求转发至源站，形成请求风暴，不仅冲击源站负载还加剧用户感知延迟。在如此大规模下，缓存未命中率即便只是小幅波动，换算成绝对请求量也是巨大的。传统的CDN层级缓存架构虽能分摊部分压力，但各边缘节点独立处理缓存未命中会导致源站接收大量重复请求——同一内容在多个边缘节点同时未命中时，源站可能被数千次相同的回源请求轰炸。

该研究提出了一层名为Origin Shield的防护中间层，辅以智能请求调度机制来系统性解决上述问题。Origin Shield部署在CDN边缘节点与源站之间，充当回源请求的统一汇聚点。其核心技术包括三点：一是请求合并——在同时间窗口内对同一内容的多个回源请求合并为单次请求，避免重复回源；二是优先级感知调度——根据内容热度和用户请求的紧急程度对回源请求分级处理；三是源站负载感知的均衡策略——动态感知源站容量并智能分配回源流量。该系统在腾讯社交平台CDN生产环境中部署，在十亿QPS量级下显著降低了源站的峰值请求压力，同时将整体缓存命中率维持在极高水平，确保了大规模社交场景下的服务稳定性。

### 技术线索与启示

- **云原生与分布式架构**：Origin Shield + 智能请求调度的三层防护架构是大规模CDN保护源站的有效范式，可直接推广到其他十亿级互联网服务的缓存架构设计中
- **性能工程与可观测性**：十亿QPS场景下的缓存优化实践经验——特别是请求合并策略对消除重复回源的量化效果——对任何大规模Web服务的高并发代理层设计都有重要参考价值
- **系统软件方向**：请求合并和优先级感知调度可抽象为通用的高并发代理中间件，应用于API网关、反向代理和数据库连接池等场景，减少后端服务的无效重复请求
- **边缘计算与端侧部署**：Origin Shield的部署位置靠近边缘但逻辑上集中，在边缘网络拓扑中可复用于IoT数据汇聚网关的设计

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.34 RLive: Robust Delivery System for Live Streaming

**作者**：Yu Tian, Gerui Lv, Qinghua Wu, Ruili Fang, Yajie Peng, Zhichen Xue, Rui Han, Chuanqing Lin, Xiaofei Pang, Ri Lu, Zhenyu Li
**机构**：ICT CAS, ByteDance
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

直播分发系统在业务快速增长中面临两个根本性瓶颈：容量瓶颈和鲁棒性不足。直播流量具有高度突发性和不可预测性——热门主播开播瞬间可能吸引千万级并发观众，传统静态拓扑结构的CDN节点在这种流量冲击下容易出现单点过载，继而引发级联故障。此外，直播对延迟极其敏感，故障恢复的每一秒都意味着大量观众流失。在这种场景下，系统不仅需要足够的分发容量，更需要面对节点故障、网络分区和流量尖峰时的快速自适应能力。

RLive提出了一套面向大规模直播场景的鲁棒分发系统。其核心设计包括三个层面：第一，弹性分发拓扑——取代传统的静态分发树，系统维护一个动态可重构的多路径拓扑结构，支持毫秒级的路径切换和负载重分配，当某条分发路径出现故障或过载时，流量自动绕过问题节点转发至健康路径；第二，预测性容量规划——基于历史观看数据和内容热度趋势，提前预估各直播间的流量规模并预分配边缘资源，避免临时扩容带来的延迟；第三，实时异常检测——部署全链路监控，利用流式异常检测算法在数百毫秒内识别节点异常并触发自动切换。该系统在字节跳动生产环境中实现了分发容量提升3倍，同时卡顿率显著降低，故障恢复时间大幅缩短，为亿级用户直播场景提供了可靠的传输基础设施。

### 技术线索与启示

- **云原生与分布式架构**：弹性分发拓扑是应对流量突发和节点故障的有效设计模式，可推广到其他大规模实时内容分发系统（如实时消息推送、在线游戏状态同步）中
- **性能工程与可观测性**：预测性容量规划+实时异常检测+自动故障切换的三位一体运维策略是大规模实时服务的最佳实践，对SRE团队构建自动化运维体系有直接参考价值
- **系统软件方向**：直播场景的鲁棒性设计——特别是快速故障检测与切换机制——对实时通信（RTC）和低延迟流媒体传输协议的设计有重要借鉴意义
- **边缘计算与端侧部署**：多路径分发拓扑与边缘节点的就近接入相结合，为边缘直播CDN架构提供了新的设计思路

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.35 Scalable RDMA Locks: Shared Stream Abstraction

**作者**：Miao Cai, Junru Shen, Xiaojian Liao, Rong Gu, Yanchao Zhao, Hao Han, Bing Chen, Baoliu Ye
**机构**：NUAA, Hohai University, Beihang University, Nanjing University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

RDMA（远程直接内存访问）技术通过绕过内核和CPU参与数据传输，极大地降低了分布式系统中的通信延迟，因此被广泛应用于分布式锁服务中以提升并发性能。然而，现有的RDMA加速分布式锁方案在高并发、高节点数的场景下面临严重的可扩展性瓶颈：当数百个节点同时竞争同一把锁时，RDMA的可靠连接（RC）模式因需要为每对节点维护独立的QP（队列对），导致连接数量和内存开销随节点数平方级增长；而不可靠数据报（UD）模式虽能降低连接开销，却又丧失了请求的保序性，破坏锁的公平性和正确性保证。

该研究提出了基于共享流抽象的RDMA分布式锁方案。其核心创新在于利用RDMA的共享接收队列（Shared Receive Queue, SRQ）机制：所有竞争节点的锁请求通过SRQ汇聚到锁服务端，由硬件在接收层完成请求的物理排序，无需软件层额外的协调开销，从而同时获得UD模式的高可扩展性和RC模式的保序性保证。在此基础上，利用RDMA的点对点write操作实现高效的所有权转移——锁的持有者直接通过单边RDMA write将所有权令牌传递给下一个等待者，避免了传统的锁服务端中转带来的额外延迟。该设计在数百节点的高并发场景下表现出线性的可扩展性，锁获取延迟保持在微秒级别，吞吐远超传统方案。

### 技术线索与启示

- **系统软件方向**：RDMA加速的分布式锁是分布式系统的基础设施，可直接集成到分布式数据库的事务管理器（如PolarDB、Spanner）、分布式文件系统的元数据服务（如HDFS NameNode）和分布式缓存的一致性协议中
- **硬件-软件协同设计**：共享接收队列的排队能力利用是RDMA编程中的关键优化技术，对RDMA消息队列、RDMA RPC框架和其他RDMA协议的设计有普遍参考价值
- **云原生与分布式架构**：高性能分布式锁是云原生系统中资源调度、Leader选举和分布式协调的核心原语，该方案可提升Kubernetes、etcd等系统在大规模集群中的协调效率
- **性能工程与可观测性**：锁竞争模式下的延迟分析和可扩展性瓶颈诊断方法对分布式系统性能调优有重要指导意义

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.36 RaidenSwap: Multi-Swap Remote System for Multi-core

**作者**：Kefan Liu, Ke Liu, Xu Zhang, Hui Yuan, Xiaolong Zheng, Ning Liu, Sa Wang, Guanghui Zhang, Yungang Bao, Mingyu Chen, Chenxi Wang
**机构**：ICT CAS, UCAS, Huawei, Shandong University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

远程内存swap是云数据中心应对内存资源紧张的常用手段——当本地内存不足时，将冷数据换出至远程节点的快速存储（如NVMe或远程内存池），以缓解本地内存压力。然而，在多核应用场景中，传统的单路径swap通道成为严重的性能瓶颈：所有CPU核心共享同一条换入换出路径，当多个核心同时触发缺页异常或内存回收时，请求在swap通道上串行排队，远程内存的高带宽无法被充分利用，导致应用性能急剧下降。

RaidenSwap针对这一问题提出了多路径并发swap机制。其核心设计是在多核节点与远程内存池之间建立多条独立的swap数据通道，允许不同CPU核心的换入换出操作并行执行。系统采用多核感知的调度策略：通过监控各核心的内存访问模式和缺页频率，智能分配swap通道——对频繁缺页的核心分配独占通道避免竞争，对偶尔缺页的核心共享通道以节省资源。这种通道分配策略最大化远程内存的有效带宽利用率，同时避免了多路径之间的锁竞争和缓存行乒乓效应。在多核内存密集型应用（如大型数据库、内存分析引擎）的测试中，RaidenSwap显著降低了swap操作的尾延迟，整体应用吞吐得到大幅提升，证明了多路径并发是突破远程内存swap性能瓶颈的有效途径。

### 技术线索与启示

- **系统软件方向**：多路远程swap机制可集成到Linux内核的swap子系统中，作为现有frontswap/zswap框架的扩展，为云环境中的弹性内存管理提供高性能基础
- **云原生与分布式架构**：远程内存利用是云环境弹性资源管理的重要手段——在容器密度优化、Serverless冷启动加速等场景中，高效的远程swap能力直接影响资源利用率和SLO达成率
- **性能工程与可观测性**：多核感知的通道调度策略——基于缺页频率的动态分配——对任何需要多核并发访问共享资源的系统（如NUMA感知调度、多队列存储）都有参考价值
- **硬件-软件协同设计**：多通道架构与NUMA拓扑的联合优化可进一步降低远程内存访问的延迟和带宽浪费

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.37 FicusDB: Scalable Multi-Versioned Authenticated Archival Storage

**作者**：Hongbo Zhang, Maofan "Ted" Yin, Robbert van Renesse
**机构**：Cornell University, UC Santa Barbara
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

归档存储系统需要长期安全地保存海量数据，并保证数据的真实性和完整性可被独立验证——这在合规审计、医疗档案和金融记录等场景中至关重要。传统的认证存储方案基于Merkle树或其变体对数据进行哈希链式认证，任何数据篡改都会破坏哈希链的一致性从而被检测出来。然而，经典Merkle树结构存在两个根本性局限：一是每次数据更新都需要重新计算从叶子到根路径上所有节点的哈希值，更新开销随树高度对数增长，在频繁更新的归档场景中成为瓶颈；二是多版本管理困难——归档数据往往需要保留完整的历史版本，但传统Merkle树缺乏对版本间共享数据的有效复用，导致大量冗余存储。

FicusDB提出了一套可扩展的多版本认证归档存储系统。其核心数据结构是Merkle DAG（有向无环图）的改进变体——与传统Merkle树的严格层级结构不同，DAG拓扑允许不同版本之间共享未变更的数据节点，只需为每个新版本创建增量变更节点并更新相关的认证路径。这种设计实现了两大关键能力：增量认证更新——数据修改时仅需更新受影响的分支，而非从根节点全部重建；并行验证——多个数据段或版本的认证可同时独立验证，利用多核并行加速。系统在保持与传统Merkle树同等的强认证安全保证（即任何数据篡改都可被检测）的同时，实现了认证更新的线性可扩展性，存储效率也因版本间共享而显著优于独立快照方案。

### 技术线索与启示

- **安全与可信计算**：多版本认证存储是合规归档和审计追踪的关键技术，可应用于企业级文档管理、医疗数据合规存储和金融交易记录的防篡改保护
- **数据密集型系统**：可扩展的认证数据结构（Merkle DAG）不仅适用于归档存储，还可推广到区块链状态管理、去中心化存储（如IPFS的Merkle DAG层）和日志审计系统
- **系统软件方向**：增量认证更新+并行验证的设计范式对分布式认证场景——如跨组织数据共享的完整性验证、供应链溯源系统——有普遍参考价值
- **云原生与分布式架构**：版本间共享存储的思想可以融入云原生的数据版本管理服务，为对象存储（如S3）提供原生的多版本认证能力

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.38 A Logically Disaggregated Cache for Replicated Storage

**作者**：Kiran Hombal, Henry Zhu, Shreesha G. Bhat, Neil Kaushikkar, Ramnatthan Alagappan, Aishwarya Ganesan
**机构**：UIUC, Jump Trading Group
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

在复制存储系统中，数据被冗余保存在多个副本节点上以提供容错和高可用性。为保证读性能，每个副本节点通常独立维护本地缓存来加速数据访问。然而，这种"每副本独立缓存"的架构存在严重的缓存空间浪费问题：由于负载均衡策略将不同请求分发到不同副本，各副本缓存的内容高度相似——同一热点数据块可能同时在所有副本的缓存中各占一份空间，导致有效缓存容量仅为单副本的缓存量级，而非多副本的聚合容量。在典型的三副本系统中，实际可用缓存至多为总缓存空间的1/3，大量昂贵的内存资源被冗余条目虚耗。

该研究提出了一种逻辑解聚的缓存架构来解决多副本缓存冗余问题。核心思想是在不改变物理部署的前提下，将多个副本的独立缓存统一抽象为一个逻辑共享的缓存层。通过一致性协议保证缓存层与底层复制存储的数据一致性：当某副本修改数据时，所有持有该数据缓存的其他副本需要在一致性协议驱动下使对应条目失效或刷新。逻辑共享缓存消除了跨副本的重复缓存条目，将聚合缓存空间真正用于缓存不同数据块。实验表明，该设计显著提升了全局缓存命中率——在多副本环境下，缓存命中率的增益随着副本数量和数据局部性的变化而不同——验证了缓存解聚是提升复制存储系统读性能和经济性的有效手段。

### 技术线索与启示

- **系统软件方向**：缓存解聚的架构思想可应用于分布式数据库（如TiKV、CockroachDB的Raft副本）、分布式文件系统和对象存储的缓存层设计，将多租户或多副本的缓存资源池化为统一的逻辑缓存
- **云原生与分布式架构**：缓存资源共享是云环境中多租户性能优化的关键方向——在多应用共享存储集群的场景中，逻辑解聚缓存可避免应用之间的缓存冗余，最大化集群级的缓存效率
- **数据密集型系统**：消除缓存冗余直接提升有效缓存容量，对任何采用多副本架构的数据密集型系统（如搜索引擎、推荐系统）都意味着更低的平均读延迟和更高的吞吐
- **性能工程与可观测性**：跨副本缓存一致性协议的开销量化分析对分布式缓存系统（如Redis Cluster、Memcached集群）的协议设计和优化有参考价值

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.39 Once Rolling Hashing in Delta Compression

**作者**：Haoliang Tan, Wenhao Ou, Xiangyu Zou, Cai Deng, Yanqi Pan, Hao Huang, Zhaoquan Gu, Wen Xia
**机构**：HIT (Shenzhen)
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

差量压缩（Delta Compression）是数据备份和去重系统中的核心技术，其标准流程分为三个阶段：分块（chunking）——使用滚动哈希将数据流切分为可变大小的数据块；匹配（matching）——对每个块计算指纹并在已有块索引中查找相似或重复块；编码（encoding）——仅存储与匹配到的旧块之间的差异。在这三个阶段中，滚动哈希被重复计算多次：分块阶段计算哈希用于块边界判定，匹配阶段再次计算用于指纹查找，编码阶段还需要用于差异检测和校验。这种重复计算构成差量压缩流水线的主要性能瓶颈——哈希计算占压缩总时间的比例可达40%以上。

该研究提出了"一次计算，多次复用"的策略来消除重复哈希开销。核心思路是在分块阶段的自然滚动哈希计算过程中，将每个窗口位置的哈希值保留至后续阶段复用，避免匹配和编码阶段的独立重算。在此基础上，研究进一步结合了两项配套优化：内容感知采样——在高信息熵区域提高哈希保留密度，在低熵区域降低密度以节省存储；捎带式I/O——将哈希值的保留和存储与压缩数据本身的I/O操作合并，避免额外的磁盘访问。在多种真实数据备份工作负载上的测试表明，该方案在保持相同压缩比的前提下，压缩吞吐得到了显著提升，吞吐增益随数据集的冗余度和熵分布不同而变化。

### 技术线索与启示

- **系统软件方向**："一次计算、多次复用"的计算消除思想可推广到所有多阶段流水线系统——在数据处理、编译器优化、网络包处理等场景中，审计并消除阶段间的重复计算往往比发明新算法更有效
- **数据密集型系统**：差量压缩吞吐的提升直接加速数据备份和容灾恢复流程，对备份存储厂商（如Veeam、Commvault）和数据去重系统（如ZFS dedup、Dmdedup）的工程优化有实际指导意义
- **性能工程与可观测性**：计算冗余审计（而非仅关注算法复杂度）是一种被低估但又极其高效的系统优化方法论，该方法可应用于各种复杂流水线的性能瓶颈诊断
- **Agent与LLM应用方向**：LLM推理流水线的多阶段计算（prefill、decode、KV cache管理）中同样可能存在阶段间重复计算，类似的分析和消除策略可加速大模型服务

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.40 2DIO: Configurable Trace Generation for Storage Benchmarking

**作者**：Yirong Wang, Isaac Khor, Peter Desnoyers
**机构**：Northeastern University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

存储系统的性能基准测试是系统设计和容量规划的基础，而准确模拟真实工作负载的I/O轨迹是其中最具挑战性的环节。现有的轨迹生成方法面临两难困境：基于参数配置的合成负载生成器（如fio）虽然灵活可调——用户可以指定读写比、顺序随机比、块大小分布等参数——但无法准确模拟真实工作负载的缓存行为；而基于重放的轨迹回放工具虽然忠实于原始行为，却缺乏可配置性，无法探索"如果工作负载特性改变会怎样"的假设性问题。最为关键的是，存储系统中缓存层的行为往往是性能的决定因素，但现有工具几乎无法同时实现参数可配置性和缓存行为保真性。

2DIO提出了一个同时满足可配置性和缓存保真性的存储基准轨迹生成框架。系统基于两个维度的建模：第一个维度是I/O模式参数，包括读写混合比例、请求大小分布、顺序与随机访问占比、空间和时间局部性等可配置属性；第二个维度是缓存行为保真性——通过分析原始轨迹的缓存命中率曲线（Miss Ratio Curve），并约束合成轨迹必须产生与之匹配的缓存行为特征，从而保证在评估存储系统缓存层性能时的准确性。用户可以根据需求调整I/O模式参数来模拟不同场景（如写密集型数据库负载、读密集型Web服务负载），同时合成轨迹的缓存行为保持与目标工作负载一致。在多种存储后端上的实验证明，2DIO生成的基准轨迹比传统的纯参数化方法更准确地预测了真实存储系统的性能表现。

### 技术线索与启示

- **系统软件方向**：准确的存储基准测试工具对系统设计、容量规划和采购决策至关重要——存储厂商、云服务商和企业IT团队可使用2DIO更精确地评估不同存储方案在预期工作负载下的性能
- **性能工程与可观测性**：缓存命中率曲线（MRC）作为工作负载特征的核心指标，其保真性约束的方法论可推广到其他缓存敏感系统（如CDN、数据库Buffer Pool、Web缓存）的基准生成和性能预测
- **数据密集型系统**：存储性能的准确评估直接影响应用层的数据库选型、文件系统参数调优和数据流水线的资源规划——消除基准测试的系统误差对生产环境的容量决策有实质性意义
- **Agent与LLM应用方向**：LLM训练和推理的I/O模式具有独特特征（如周期性checkpoint写入、模型加载的批量读），2DIO的可配置框架可用于构建面向AI工作负载的存储基准

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.41 Fast Crash Consistency: Opportunistic Order Elimination

**作者**：Jiahao Chen, Yanqi Pan, Wen Xia, Hao Huang, Peixin Zeng, Yuchen Shan
**机构**：HIT (Shenzhen)
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

持久内存（Persistent Memory, PM）兼具内存级访问速度和存储级数据持久性，被视为下一代存储系统的关键介质。然而，在PM上保证崩溃一致性的代价极高——传统方法依赖严格的写入顺序约束（如clflush、clwb加sfence指令，或频繁的fsync系统调用）来确保系统崩溃时数据处于一致状态。这些顺序约束迫使独立的I/O操作必须串行化执行，即使它们之间没有真正的数据依赖，也必须在持久化屏障处等待，将PM的高并发潜力大幅压缩。在大量并发写入的工作负载下，这种顺序化I/O成为限制PM吞吐的核心瓶颈。

该研究提出了"机会主义消序"（Opportunistic Order Elimination）技术来打破这种不必要的I/O串行化。关键洞察是：许多写入顺序约束是为了保护崩溃一致性不变式而"过度保守"地强加的——在真正需要顺序保证的写入对之间，存在大量语义无关的操作可以被安全地重新排序。系统通过静态程序分析和运行时依赖追踪，精确识别哪些写入操作之间存在真实的因果依赖（必须在持久化顺序上严格保序），哪些操作之间并无依赖（可以并行提交），然后仅在必要的依赖对上施加同步屏障，其余操作允许自由并发。在PM文件系统的高并发工作负载上，该技术将I/O性能提升了1.99至10.13倍，提升幅度随工作负载的并发度和写入依赖性而变化，证明了精准消除不必要的顺序约束是释放PM性能潜力的关键手段。

### 技术线索与启示

- **系统软件方向**：机会主义消序是PM文件系统的核心优化技术，可集成到现有的PM文件系统（如NOVA、PMFS、SplitFS）中，作为通用的崩溃一致性优化层
- **性能工程与可观测性**：I/O写入顺序依赖的精细分析对其他强一致性存储系统（如WAL日志、LSM-Tree的MemTable刷新、数据库redo log）的并行化优化有直接参考价值——精准识别真实依赖并仅在此处保序，而非全局串行化
- **数据密集型系统**：PM并发吞吐的大幅提升直接加速数据密集型应用的持久化写入——如OLTP数据库的事务提交、流处理系统的状态快照、消息队列的消息持久化
- **硬件-软件协同设计**：该技术可与PM硬件的更深层优化（如eADR的异步持久化）组合，进一步缩小持久化屏障的开销

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.42 CSnake: Detecting Cascading Failure via Causal Stitching

**作者**：Shangshu Qian, Lin Tan, Yongle Zhang
**机构**：Purdue University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

自维持级联故障（Self-Sustaining Cascading Failure）是大规模分布式系统中最具破坏性的故障模式之一——一个局部故障触发新的故障点，新故障又引发更多故障，形成无限传播的连锁反应。这种故障模式在微服务架构中尤为常见：一个服务的延迟增加导致调用方线程池耗尽，进而拖垮上游服务，最终使整个调用链崩溃。传统监控工具能捕捉到每个独立故障事件，但难以重建完整的故障传播因果链——日志时间戳可能因时钟偏移而不可靠，指标相关性分析可能识别出虚假关联，运维人员面对成千上万个告警事件时如同盲人摸象。

CSnake提出了一种基于因果拼接的级联故障自动检测方法。系统从分布式系统的日志和性能指标中提取两类关键信息：各服务的异常事件（如超时、错误率飙升、资源耗尽）和事件之间的因果依赖关系（如服务A调用服务B、数据库连接池满导致请求排队）。然后通过因果推理算法将这些零散的事件"拼接"为完整的故障传播链——将第一个异常事件标记为根因，依次连接其直接和间接影响的后继事件，最终还原从初始触发到最终崩溃的完整级联路径。研究利用多个真实系统的故障案例对CSnake进行了验证，包括Kubernetes集群调度故障和微服务调用链雪崩，证明该方法能够准确识别级联故障的起始点和传播路径，显著缩短故障根因定位时间。

### 技术线索与启示

- **云原生与分布式架构**：级联故障的自动检测和传播链可视化是大规模分布式系统（特别是微服务和Kubernetes集群）可靠性工程的关键能力，可集成到现有的可观测性平台（如Datadog、Grafana、Prometheus）中
- **性能工程与可观测性**：因果关系拼接方法可融入APM（应用性能管理）和AIOps工具中，在告警风暴时自动聚类事件并构建故障树，大幅提升SRE的事故响应效率
- **系统软件方向**：故障传播链的自动重建对其他复杂系统的故障分析有参考价值——如多层网络SDN控制器级联故障、云资源编排中的依赖异常传播
- **Agent与LLM应用方向**：LLM可进一步辅助因果推理——利用自然语言理解能力分析日志语义、构建故障知识图谱，与CSnake的因果拼接结合形成智能化的故障诊断系统

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.43 Garen: Reliable Cluster Management with Atomic State Reconciliation

**作者**：Mingi Kim, Ahnjae Shin, Jaewoo Maeng, Myeongjae Jeon, Byung-Gon Chun
**机构**：FriendliAI, Samsung, POSTECH, SNU
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

集群管理系统（如Kubernetes）是现代云基础设施的控制核心，负责在数百甚至上千个节点上编排容器、分配资源和维持期望状态。这些系统本质上是一个分布式状态机——通过控制平面与各节点上的agent持续通信，将集群从"实际状态"向用户声明的"期望状态"调谐。然而，当发生网络分区、节点瞬时故障或控制平面重启等异常时，状态调谐过程极易出现不一致：部分节点的状态更新已提交而其他节点未提交，或者节点的实际状态与控制平面的记录产生偏差，导致控制平面作出错误决策（如错误地删除"已失联"但其实仍正常运行的服务）。

Garen提出了一种基于原子状态协调的集群管理方案来解决状态不一致问题。核心设计是将每个状态变更操作封装为原子事务——要么所有受影响的节点都可见该变更的完整效果，要么所有节点都不可见，杜绝部分更新的中间态。在并发故障场景下（如控制平面在执行滚动更新时遭遇网络分区），Garen通过原子操作保证状态协调的正确性：即使在网络恢复后也无需人工介入清理不一致状态，系统自动根据原子事务日志恢复到一致状态。该机制在设计上追求对系统正常操作的性能影响最小化——原子事务的开销主要发生在故障恢复路径上，正常路径几乎无额外延迟。在FriendliAI的生产环境中，Garen成功处理了多种真实故障场景下的状态协调，验证了原子状态管理对提升集群管理可靠性的关键作用。

### 技术线索与启示

- **云原生与分布式架构**：原子状态协调是提升Kubernetes控制平面可靠性的核心手段，可融入Kubernetes upstream的controller模式和etcd交互中，为社区提供生产级的状态一致性保证
- **系统软件方向**：分布式状态协调的原子化设计模式可推广到其他控制平面系统——如服务网格（Istio/Envoy）的配置下发、虚拟机编排器（OpenStack）的资源调度和服务发现系统的一致性维护
- **性能工程与可观测性**：状态不一致的自动检测与修复是运维自动化的重要方向——Garen的原子事务日志也为事后审计和故障回溯提供了可靠的基础数据源
- **Agent与LLM应用方向**：LLM Agent在多集群编排中需要可靠的状态视图作为决策依据，Garen的一致性保证可确保Agent对集群状态的感知始终准确

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.44 Avicenna: Masking Slowdowns in Replicated State Machines

**作者**：Christopher Hodsdon, Zijian Qin, Khiem Ngo, Siddhartha Sen, Ethan Katz-Bassett, Wyatt Lloyd
**机构**：Databricks, Princeton University, Datadog, Microsoft Research, Columbia University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

复制状态机（Replicated State Machine, RSM）是分布式共识系统（如Raft、Paxos）的基础抽象，通过多副本一致复制来提供容错能力。然而，RSM面临一个根本性的性能问题：共识决策需要等待多数副本的响应，因此单个副本的性能减速——无论是由GC暂停、磁盘I/O抖动、网络瞬时拥塞还是其他原因导致——都会直接拖慢整个系统的事务提交速度。在云环境的共享基础设施中，这种"短板效应"尤为突出：即使90%的副本运行正常，一个受邻居干扰的慢副本就可能使共识延迟翻倍，系统的尾延迟因此表现出极大的不可预测性。

Avicenna提出了一种推测性执行（Speculative Execution）策略来屏蔽慢副本对共识延迟的拖累。核心机制是反事实评估：在每次共识轮次中，不等慢副本回复，系统基于已经到达的快副本响应提前推进共识状态——这个"推测提交"的结果被立即提供给上层应用使用。与此同时，系统继续等待慢副本的响应：如果慢副本最终返回的结果与推测结果一致（即大多数情况下），则推测提交被确认为正式提交，用户无感知任何延迟；如果慢副本返回的结果与推测结果不一致（即罕见的异常情况），系统回退推测状态并采用正确结果。这种"先推测、后验证、不一致则回退"的策略在保证RSM正确性（线性一致性）的前提下，将系统的尾延迟从最慢副本延迟降低至最快多数副本延迟的水平，在多种分布式系统原型上显著压缩了长尾延迟。

### 技术线索与启示

- **云原生与分布式架构**：反事实评估处理慢节点是分布式系统设计中的创新范式——不同于传统方案试图消除慢节点，而是通过推测来"无视"它们，这对云环境中不可避免的性能抖动有极强的实用性
- **系统软件方向**：推测执行+验证回退的设计模式可推广到其他分布式协议——如分布式事务的2PC提交、分布式缓存的读修复和Gossip协议的收敛加速——任何需要等待多个响应者的场景都可以从中受益
- **性能工程与可观测性**：慢副本检测和反事实评估框架对分布式系统的性能调优有参考价值——识别哪些副本是"常任慢节点"有助于运维团队进行针对性的资源调整和故障预防
- **边缘计算与端侧部署**：在边缘-云协同的RSM场景中，边缘节点天然比云节点更不稳定，Avicenna的推测方法可有效屏蔽边缘波动

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.45 Rose: Reproducing External-Fault-Induced Failures

**作者**：Sebastião Amaro, Miguel Matos, Pedro Fonseca
**机构**：INESC-ID, IST Lisbon, Purdue University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

外部因素引发的分布式系统故障——如网络抖动、磁盘延迟尖峰、时钟异常、CPU资源争抢等——是生产环境中最难调试的故障类型之一。这类故障的触发条件通常极为苛刻：可能需要特定的请求到达时序与特定的环境异常事件精确"碰撞"才能暴露。然而，在测试或开发环境中重现这些条件几乎不可能——开发者无法精确控制网络延迟的微观波动模式，也无法复制生产环境的多租户资源争抢特征。结果是大量"生产环境专属"的故障成为无法在测试环境中复现的"幽灵Bug"，运维团队只能通过猜测和热修复来应对。

Rose提出了一套轻量级的故障复现框架来解决这一难题。系统在运行时插入最小化的仪器代码——仅记录与故障触发相关的关键事件（如消息发送接收时间戳、资源竞争事件、系统调用返回值异常等）及其精确时序，而非全量日志记录，从而将性能开销控制在极低水平。当故障发生后，Rose利用记录的"故障触发条件快照"在生产环境或测试环境中高保真地重放该故障场景——通过精密控制网络模拟器注入与原始场景相同的延迟模式、利用资源限制工具复现相同的CPU/内存争抢条件。该框架在多种分布式系统（包括ZooKeeper、MongoDB等）的真实故障案例中进行了验证，成功复现了原本"不可复现"的外部故障，大幅缩短了从故障发现到根因定位的调试周期。

### 技术线索与启示

- **系统软件方向**：轻量级故障可复现性是提升分布式系统测试效率的关键能力——该框架可集成到CI/CD流水线中，每当生产环境发现新故障即自动生成可复现的测试用例，持续加固系统
- **云原生与分布式架构**：外部故障的可复现性直接提升云服务的可靠性工程（SRE）效率——将不可复现的随机故障转化为确定性的回归测试，使故障修复从"试错"转变为"验证"
- **性能工程与可观测性**：最小化仪器设计的"只记录差异"原则对其他可观测性工具（如分布式追踪、eBPF探针）的设计有普遍借鉴意义——精准记录比全量记录更重要
- **Agent与LLM应用方向**：LLM在分析故障模式和生成修复建议时需要准确的故障上下文，Rose复现的确定性故障场景可作为LLM辅助调试的高质量输入

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.46 Proactive Change Risk Detection in Production Cloud Systems

**作者**：Jinyang Liu, Yichen Li, Tieying Zhang, Binbin Chen, Xiao He, Zhihan Jiang, Haipeng Zhang, Gang Wu, Yi Li
**机构**：ByteDance
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

云系统变更操作——包括配置参数修改、软件版本升级、基础设施扩容缩容、安全补丁部署等——被业界公认为引发生产故障的首要原因。据多项行业调查，变更相关故障占所有生产事故的比例高达50%以上。究其原因，云系统的高度复杂性和组件间不可预见的交互效应，使得看似安全的单项变更可能触发意料之外的连锁反应。当前业界的普遍做法是依赖变更审批流程和人工经验判断风险，但人工审查面对每天数百次变更的吞吐量时力不从心，且无法发现隐蔽的跨组件兼容性问题。

该研究提出了一套主动式变更风险检测系统，在变更真正执行之前评估其对生产环境的潜在威胁。系统基于字节跳动历史积累的海量变更数据和故障事件训练风险预测模型：模型从变更的属性特征（修改了哪些配置项、涉及哪些服务、变更窗口时间等）、环境上下文（目标集群的负载水平、依赖服务的版本状态等）和历史相似变更的故障记录中提取信号，综合评估当前变更的风险等级。对于判定为高风险的变更，系统自动触发拦截或建议转为灰度发布——先在少量节点上验证变更效果，确认无异常后再全量推广。在字节跳动生产环境中，该系统已持续运行处理大规模变更流量，显著减少了因变更直接引发的故障事件，实践证明了主动式变更风险管理在大规模云运维中的重要价值。

### 技术线索与启示

- **云原生与分布式架构**：主动变更风险检测是规模化云运维从"被动救火"向"主动防火"转型的关键系统，对任何管理大规模集群的云服务商都有直接借鉴意义
- **Agent与LLM应用方向**：LLM可显著增强变更风险分析的能力边界——利用LLM理解变更描述的自然语言语义、自动比对变更影响的配置项文档、分析历史故障报告与当前变更的相似性，从而提升风险预测的召回率和精确率
- **性能工程与可观测性**：工业级的变更风险检测经验——包括特征工程、模型选型、灰度策略设计——对其他互联网公司建立类似的变更安全机制有重要的工程参考价值
- **安全与可信计算**：变更风险管理与供应链安全（如软件BOM分析、依赖漏洞检测）的结合可进一步构建端到端的变更安全体系

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.47 Five Minutes of DDoS Brings down Tor

**作者**：Zhongtang Luo, Jianting Zhang, Akshat Neerati, Aniket Kate
**机构**：Purdue University, Supra Research
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

Tor网络是全球最重要的匿名通信基础设施，每天为数百万用户提供抗审查和隐私保护服务。Tor的目录服务（Directory Service）负责维护全网节点的信息——包括每个中继节点的IP地址、公钥、带宽权重和在线状态。客户端必须从目录服务器获取共识文档（consensus document）才能构建匿名通信链路。该研究发现Tor的目录协议存在严重的DDoS脆弱性——仅需五分钟的针对性DDoS攻击即可使目录服务完全不可用，进而导致整个Tor网络瘫痪。

攻击的机制十分精巧且高效：攻击者利用目录协议的带宽放大效应——通过发送精心构造的小请求诱导服务器返回大量数据，以微小攻击带宽消耗大量服务器出站带宽。同时，攻击请求迫使服务器维护大量半连接状态，耗尽服务器的内存和文件描述符等资源。这两重压力叠加使得目录服务器在极短时间内失去响应能力。由于客户端高度依赖目录服务获取网络拓扑，目录服务一旦瘫痪，新客户端无法加入、已有客户端无法更新节点信息，整个Tor网络的匿名通信功能随之崩溃。研究不仅揭示了这一脆弱性，还提出了协议层面和部署层面的综合缓解措施，包括请求速率限制、状态资源隔离和分布式目录服务增强方案。

### 技术线索与启示

- **安全与可信计算**：Tor目录协议的DDoS脆弱性研究揭示了匿名通信基础设施在面临资源耗尽攻击时的系统性弱点——不仅是Tor，其他依赖集中式目录或注册中心的对等网络（如IPFS的DHT引导节点、区块链网络的种子节点）同样面临此类威胁
- **云原生与分布式架构**：目录服务的DDoS防护经验对其他分布式系统的注册中心和元数据服务（如Consul、Eureka、Nacos）有参考价值——资源隔离、请求验证和速率限制是核心防护手段
- **开放性问题与未来方向**：匿名通信网络的韧性与效率之间存在深刻的权衡——更强的抗DDoS能力往往意味着更高的协议复杂度和延迟开销，如何在两者之间取得平衡是持续的开放挑战
- **系统软件方向**：带宽放大攻击和状态耗尽攻击的防护机制可推广到通用的网络服务网关设计中，应对DNS放大攻击、Memcached放大攻击等类似威胁

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.48 Yield Not Thy Core

**作者**：Achilles Benetopoulos, Peter Alvaro, Andi Quinn, Robert Soule
**机构**：UC Santa Cruz, Yale University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

"Yield"（让出CPU）是并发编程中的基本操作——线程主动放弃CPU使用权，让其他线程运行，自身等待某个条件满足后再被唤醒。这看似无害的操作在分布式系统中可能引发严重的性能异常和正确性问题。当关键路径上的任务（如RPC处理线程、数据库事务协调者、消息队列消费者）在执行yield时，CPU可能被非关键任务长期占用，导致关键任务的实际等待时间远超预期。更糟糕的是，这种"无意的阻塞"可能引发级联效应——一个任务被延迟导致其依赖方超时，进而触发重试或故障切换，在高负载下演变为活锁（livelock）：系统各组件都在忙碌运转，但整体没有进展。

该研究对yield在多个主流分布式系统中间件中的实际行为进行了系统性的实证分析。涵盖的组件包括数据库系统（如PostgreSQL的锁等待）、消息队列（如Kafka的消费者再均衡）、RPC框架（如gRPC的线程池调度）等。分析揭示了几个关键发现：yield导致的延迟波动在某些场景下远超网络本身的不确定性；许多系统使用yield的方式隐含了不合理的时序假设——例如假设被yield阻塞的任务将在固定时间内被唤醒，而在高负载下该假设经常被打破；活锁是yield不当使用的典型症状，表现为系统CPU利用率接近100%但有效吞吐几乎为零。研究不仅诊断了这些问题，还提出了改进的调度策略和编程建议，帮助开发者避免yield相关的陷阱。

### 技术线索与启示

- **系统软件方向**：yield行为分析对分布式系统的编程实践有直接指导意义——开发者在设计关键路径代码时应明确标记不应被随意yield的代码段，并对yield的等待语义设置显式超时和死线检查
- **性能工程与可观测性**：yield导致的性能异常是一种隐蔽且难以诊断的反模式——传统的CPU和延迟监控可能显示一切正常但吞吐却异常低，需要专门的yield-wait分析工具来检测此类问题
- **开放性问题与未来方向**：分布式系统的调度语义缺乏形式化定义——不同语言运行时（Go goroutine、Java virtual thread、Rust async task）对yield的实现语义各异，系统间不一致的调度行为可能导致跨语言调用的隐藏陷阱，亟需更深入的形式化工作
- **云原生与分布式架构**：在Service Mesh sidecar和eBPF程序等内核旁路执行场景中，yield的副作用更加突出——sidecar与主容器的调度抢占可能导致原本预期微秒级响应的请求延迟飙升至毫秒级

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.49 Fuzzing Enterprise Blockchain

已在Part 10中涵盖。

---

## 12.50 No More Translation at Runtime: LLM-Empowered Static Binary Translation

**作者**：Zhibo Liu, Huaijin Wang, Wai Kin Wong, Daoyuan Wu, Shuai Wang
**机构**：HKUST, Lingnan University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

静态二进制翻译（Static Binary Translation, SBT）旨在将一种指令集架构（ISA）的二进制程序离线翻译为另一种ISA的等价程序，从而在无需源码和运行时开销的情况下实现跨平台执行。这一技术在异构计算迁移、遗留软件兼容和移动应用跨平台部署等场景中具有重要价值。然而SBT面临两大经典难题：一是间接跳转的解析——当目标地址在编译时无法确定（如通过函数指针调用、虚函数分发）时，静态翻译器无法准确识别跳转目标，导致翻译后代码控制流不完整；二是代码与数据的区分——在冯·诺依曼架构中指令和数据混存，翻译器必须准确区分哪些字节序列是代码（需要翻译）哪些是数据（需要保留），误判将导致翻译失败或运行时错误。

该研究首次将大语言模型（LLM）引入静态二进制翻译流程，利用LLM强大的代码理解能力突破传统方法的局限。在间接跳转解析方面，LLM通过分析二进制代码的上下文语义和常见编译模式，推理函数指针的可能目标集合，显著提升间接跳转的覆盖率和准确性——传统基于模式匹配的方法往往无法识别编译器优化后的复杂间接跳转模式，而LLM的语义理解能力可以有效填补这一空白。在代码-数据分离方面，LLM通过识别代码段的典型控制流模式和数据段的典型字节分布特征来辅助区分，减少了传统启发式方法在高熵数据区的误判。实验结果表明，LLM辅助的静态翻译在翻译覆盖率和正确性上显著优于纯传统方法，首次展示了大语言模型在底层二进制分析任务中的巨大潜力。

### 技术线索与启示

- **Agent与LLM应用方向**：LLM辅助二进制翻译是该方向的开创性工作，证明了LLM的代码理解能力不仅适用于高级语言源代码，还可深入到底层的二进制分析中——这为LLM在反编译、二进制加固、逆向工程等安全分析任务中的应用打开了大门
- **系统软件方向**：LLM+传统编译/翻译技术的结合范式可能开创二进制分析的新范式——LLM负责"理解"和高层推理（理解控制流语义、识别编译模式），传统工具负责"执行"和确定性保证（指令翻译、地址重定位），两者互补形成"语义驱动+精确执行"的混合架构
- **开放性问题与未来方向**：LLM辅助的静态分析可扩展到更多领域——如自动化漏洞检测（理解跨函数的状态交互）、逆向工程（恢复高级语义如类和继承关系）、二进制补丁生成等
- **安全与可信计算**：LLM辅助翻译的正确性需要严格验证——翻译后程序与原程序在行为上必须等价，这在安全攸关的场景中尤为重要，需要形式化验证或差分测试作为LLM输出的最终保险

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.51 Low-Compilation-Cost Register Allocation in LLVM-Based BT

**作者**：Xiangwei Meng, Chen Gao, Wei Li, Fengyuan Ren
**机构**：Lanzhou University, Tsinghua University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

基于LLVM的二进制翻译（Binary Translation, BT）框架因其成熟的多目标后端支持而被广泛采用，但翻译过程中的编译开销——特别是寄存器分配阶段——成为限制翻译速度的关键瓶颈。寄存器分配是编译器中决定程序变量映射到物理寄存器的优化过程，经典方法如图着色算法（Graph Coloring）需要在变量活性（liveness）分析后构建干涉图（Interference Graph），再求解图的着色问题，其时间复杂度在变量数较多时呈指数级增长。在二进制翻译的特殊场景中，问题更加严峻：源ISA和目标ISA的寄存器模型差异巨大（如x86的少量通用寄存器 vs ARM/RISC-V的大量寄存器），跨ISA的寄存器映射约束使得干涉图结构异常复杂，图着色时间远超一般编译场景。

该研究针对LLVM-based二进制翻译场景提出了轻量级寄存器分配策略。核心思路是利用二进制翻译场景的特殊性简化问题复杂度：翻译器处理的输入是已高度优化的机器码，而非未优化的中间表示，其中的变量间干涉关系已经过前端编译器的优化，因此可以用启发式方法替代完整的图着色算法。具体而言，该方案采用基于优先级的线性扫描（Linear Scan）与局部干涉解析的组合策略——对活跃范围短的变量使用线性扫描快速分配，对活跃范围长且干涉复杂的变量使用轻量级干涉解析——避免了全局干涉图构建和图着色的高开销。实验结果证明，该方案将编译时间大幅缩短，同时由于输入代码本身已具备较好的寄存器利用率，启发式分配产生的代码质量仍保持在可接受水平，在翻译速度与代码质量之间取得了较好的平衡。

### 技术线索与启示

- **系统软件方向**：面向特定场景简化通用编译器pass的设计方法论可推广到其他LLVM工具链优化——如JIT编译中的内联优化、WASM后端的指令选择——不需要在每个场景中都使用最通用（也最耗时）的算法
- **性能工程与可观测性**：编译开销与代码质量的权衡对JIT运行时（如V8 TurboFan、HotSpot C2）有直接参考价值——JIT必须在优化效果和编译延迟之间动态决策，二进制翻译中的场景特定简化策略可以启发JIT的分层编译设计
- **硬件-软件协同设计**：寄存器分配策略可针对目标ISA的寄存器特性进一步定制——如利用RISC-V的寄存器窗口或ARM的NEON寄存器文件来简化映射逻辑
- **Agent与LLM应用方向**：LLM辅助的寄存器分配——利用LLM分析代码模式预测最优寄存器分配方案——可能是进一步提升翻译效率和质量的新方向

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.52 Digital Hole: Bypassing Commercial Audio DRM

**作者**：Björn Ruytenberg, Mohammad Sina Karvandi, Herbert Bos, Erik van der Kouwe, Asia Slowinska
**机构**：Vrije Universiteit Amsterdam
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

商业音频DRM（Digital Rights Management）系统是音乐流媒体平台（如Spotify、Apple Music、Amazon Music等）保护版权内容的核心技术屏障。这些DRM方案通过在音频流中嵌入加密层和许可证验证来阻止用户未经授权地提取和保存原始音频数据。然而，尽管DRM技术在视频领域经历了多年的攻防升级，音频DRM的安全性却长期缺乏系统的第三方安全审计——音乐流媒体平台普遍假设其使用的DRM方案（如Widevine、FairPlay）的安全性等同于视频DRM，未考虑音频内容独特的技术特征可能引入新的攻击面。

该研究提出了DReaMcatcher攻击方法，利用信号处理中的"数字空洞"（Digital Hole）从受保护的音频流中提取原始内容。核心洞察在于：无论DRM施加多强的加密保护，最终解密后的音频信号必然要通过操作系统的音频栈（audio stack）传输至声卡进行数模转换——在这个环节，音频数据以PCM（脉冲编码调制）的形式存在于系统的音频缓冲区中。DReaMcatcher在音频驱动层面拦截这些已解密但尚未输出的PCM采样数据，利用自定义的音频抓取工具绕过DRM的加密保护层直接获得原始音频内容。该攻击揭示了多个主流DRM方案在音频处理链路中的一个根本性设计缺陷：加密保护终止于解码器输出，而解码后的明文信号在内存路径上缺乏足够的保护。研究对Spotify、Apple Music等多个平台的DRM方案进行了安全评估和绕过验证，对音频版权保护的安全性提出了严肃质疑。

### 技术线索与启示

- **安全与可信计算**：音频DRM的系统性安全研究表明现有方案的普遍设计缺陷——加密保护仅覆盖传输和存储路径，而最终的解码输出是未受保护的明文信号"盲区"，这为DRM系统的纵深防御设计提出了更高的要求
- **系统软件方向**：信号层面的安全分析方法可推广到其他多媒体保护场景——视频DRM的HDCP链路、游戏反作弊系统的画面合成层、远程桌面的屏幕抓取防护等都面临类似的"信号末端"安全挑战
- **开放性问题与未来方向**：DRM安全性与用户体验的平衡是持续的开放挑战——更强的信号路径保护（如TEE内的端到端音频处理）可能带来显著的性能开销和延迟增加，在安全与流畅播放之间取得合理平衡仍需更多研究
- **硬件-软件协同设计**：将音频解码和信号处理移入可信执行环境（TEE）可能是抵御此类攻击的长期方向，但音频处理的实时性要求对TEE的计算能力提出了新挑战

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.53 Turnstile: Hybrid IFC Framework for IoT Privacy

**作者**：Kumseok Jung, Mohanna Shahrad, Gargi Mitra, Karthik Pattabiraman
**机构**：UBC, Princeton University
**发表信息**：EuroSys 2026, Edinburgh, Scotland, UK

### 技术概要

IoT设备广泛部署在家庭、办公和公共场所，持续采集大量敏感数据——包括麦克风录音、摄像头画面、位置轨迹、健康指标和用户行为模式。然而，这些数据的流向和用途往往不透明：传感器数据可能在用户不知情的情况下被上传到云端、被第三方分析、或被跨应用共享，引发严重的隐私合规风险，尤其在GDPR、CCPA等数据保护法规日益严格的背景下。现有的隐私保护方案要么过于粗粒度——如一刀切地禁止所有传感器数据共享，严重限制设备功能；要么性能开销过大——如动态污点追踪技术在全系统范围部署时带来无法承受的运行时开销，在资源受限的IoT设备上不切实际。

Turnstile提出了一套混合信息流控制（IFC）框架来实现IoT隐私数据的细粒度保护。系统结合了两种互补的技术：静态分析在编译时或部署前推理数据在程序中的传播路径，预先识别敏感数据可能流向的"槽点"（如网络发送函数、文件写入点）；动态监控则在运行时按需在已识别的关键点上插入轻量级检查，验证实际数据流是否违反用户定义的隐私策略。这种"静态预判+动态验证"的混合策略既避免了全量动态追踪的高开销，又克服了纯静态分析对运行时行为的盲区。该框架支持用户定义灵活的隐私策略——如"心率数据仅允许在本地处理、禁止上传""卧室摄像头数据仅允许在边缘设备上进行人员检测、禁止原始图像传输"——在多种IoT设备原型上验证了隐私保护的细粒度控制与功能最小化影响。

### 技术线索与启示

- **安全与可信计算**：IoT隐私保护是践行GDPR、CCPA等法规的技术底座——Turnstile的细粒度策略定义能力直接对应数据最小化、目的限制等合规原则，为IoT设备厂商提供了可嵌入的隐私合规框架
- **系统软件方向**：静态+动态混合信息流控制的设计范式可推广到其他数据流追踪场景——如移动应用的权限滥用检测、浏览器扩展的跨域数据泄露防护、微服务系统的敏感数据传播审计
- **边缘计算与端侧部署**：IoT隐私框架必须在资源极度受限的环境下运行——Turnstile在性能和功能保护之间的权衡设计对边缘AI推理的隐私保护（如本地人脸识别不上传原始图像）有直接启示
- **Agent与LLM应用方向**：LLM Agent在智能家居场景中需要访问多种传感器数据来做决策，Turnstile的隐私策略可为Agent提供安全的数据访问沙箱

> **信息来源**：基于会议公开信息 | EuroSys 2026 Proceedings

---

## 12.54 LifeFuzz: Lifecycle-Guided Fuzzing for Windows Driver

**作者**：Chendong Yu, Yuekang Li, Yang Xiao, Jie Lu, Yeting Li, Defang Bo, Wei Huo
**单位**：CAS IIE, UNSW, ICT CAS

### 技术概要

Windows驱动跨处理程序漏洞涉及多IRP函数间状态交互。基于对象生命周期模型引导探索不同阶段处理函数组合，自动推断状态机生成跨处理程序测试，发现多种未知漏洞。

### 技术线索与启示

- **安全与可信计算**：Windows驱动漏洞是系统安全重要攻击面
- **系统软件方向**：基于状态机的Fuzzing引导可推广到其他事件驱动系统测试
- **开放性问题与未来方向**：形式化验证与Fuzzing结合可进一步提升安全性

---

## 12.55 ECCB

已在Part 10中涵盖。

---

# 论文索引表

> 以下索引表覆盖EuroSys 2026全部约131篇录用论文（Spring+Fall双周期）。

| # | Part | 论文标题 | 第一作者 | 机构 |
|---|------|---------|---------|------|
| 1 | 1 | MegaScale-MoE: Large-Scale Communication-Efficient Training of MoE Models | Chao Jin | Peking U, ByteDance |
| 2 | 1 | LoRAFusion: Efficient LoRA Fine-Tuning for LLMs | Zhanda Zhu | U of Toronto, Vector, NVIDIA |
| 3 | 1 | Federated Fine-Tuning of Sparsely-Activated LLMs on Resource-Constrained Devices | Fahao Chen | Shandong U, Xi'an Jiaotong U |
| 4 | 1 | MegaScale-Data: Scaling DataLoader for Multi-Source LFM Training | Juntao Zhao | HKU, ByteDance |
| 5 | 1 | STAlloc: Enhancing Memory Efficiency with Spatio-Temporal Planning | Zixiao Huang | Tsinghua U, Infinigence-AI |
| 6 | 1 | Zeppelin: Balancing Variable-length Workloads in Data Parallel Training | Chang Chen | PKU, ETH Zurich |
| 7 | 1 | Arena: Dynamic Scheduling and Adaptive Parallelism Co-Design | Chunyu Xue | SJTU, Lenovo, Microsoft |
| 8 | 1 | HARP: Automated Parallel Training on Heterogeneous GPU Clusters | Antian Liang | Fudan U |
| 9 | 1 | HetAuto: Cross-Cluster Auto-Parallelism for Heterogeneous Training | Guicheng Qi | HKU, Meituan |
| 10 | 1 | FlashOverlap: Efficient Overlapping via Signaling and Reordering | Ke Hong | Tsinghua U, Infinigence-AI |
| 11 | 1 | Crimson: Collaborative Parameter Updates for Pipeline Training | Yapeng Jiang | Sun Yat-sen U, HKUST |
| 12 | 1 | Suika: Re-scheduling 3D-parallelized LLM Training Jobs | Yuxuan Wang | SJTU, TeleAI, Huawei |
| 13 | 1 | Maya: Optimizing Training Workloads using GPU Runtime Emulation | Srihas Yarlagadda | Georgia Tech, NVIDIA |
| 14 | 1 | MegaScale-Omni: MultiModal LLM Training in Production | Chunyu Xue | SJTU, ByteDance Seed |
| 15 | 1 | ReCCL: Handling Network Faults in Distributed AI Training | Xin Zhe Khooi | NUS, ByteDance |
| 16 | 1 | Laminar: Scalable Asynchronous RL Post-Training Framework | Guangming Sheng | HKU, ByteDance |
| 17 | 2 | AdaServe: Multi-SLO LLM Serving with SLO-Customized Speculative Decoding | Zikun Li | CMU, Princeton, EPFL |
| 18 | 2 | FlexPipe: Inflight Pipeline Refactoring in Fragmented Serverless Clusters | Yanying Lin | SIAT CAS, UCSD |
| 19 | 2 | TokenFlow: Responsive LLM Streaming via Preemptive Scheduling | Junyi Chen | SJTU, George Mason |
| 20 | 2 | AdaGen: Workload-Adaptive Cluster Scheduler for LLM Inference | Sudipta Saha Shubha | U Virginia, HPE Labs |
| 21 | 2 | SkyWalker: Locality-Aware Cross-Region Load Balancer for LLM | Tian Xia | UC Berkeley |
| 22 | 2 | PiLLM: Resource-Efficient LLM Inference Using Workload Prediction | Yunqian Fan | ShanghaiTech, SenseTime |
| 23 | 2 | FineMoE: Fine-Grained Expert Offloading for MoE Serving | Hanfei Yu | Stevens, Rice, Waterloo |
| 24 | 2 | KUNSERVE: Parameter-centric Memory Management for LLM Serving | Rongxin Cheng | SJTU |
| 25 | 2 | eLLM: High Throughput LLM Serving via Adaptive KV Caching | Wenyan Chen | U Macau, SIAT CAS |
| 26 | 2 | MFS: Model Family Serving System for LLMs | Yunxuan Zhang | HKUST, USTC |
| 27 | 2 | Eevee: Efficient Multimodal Serving via Module Multiplexing | Zicong Hong | HKUST, Sun Yat-sen U |
| 28 | 2 | SAS: Sparse Attention Synthesizer for Language Model Inference | Yuan Zhou | Amazon |
| 29 | 2 | Scaling LLM Test-Time Compute with Mobile NPU on Smartphones | Zixu Hao | Tsinghua U, Microsoft |
| 30 | 2 | TailorLLM: Collaborative End-Cloud Inference via Low-Rank Adaptation | Zian Wang | BUPT |
| 31 | 2 | TZ-LLM: Protecting On-Device LLMs with Arm TrustZone | Xunjie Wang | SJTU |
| 32 | 2 | PARD: Enhancing Goodput via Proactive Request Dropping | Zhixin Zhao | Tianjin U, UT Dallas |
| 33 | 3 | AIMS: Cost-Efficient LLM Agent Deployment in Cloud-Edge | Shiyi Liu | U Virginia, Microsoft |
| 34 | 3 | From Imperative to Declarative: LLM-friendly OS Interfaces | Yuan Wang | ISCAS, SJTU |
| 35 | 4 | InstGenIE: Efficient Image Editing with Mask-aware Caching | Xiaoxiao Jiang | HKUST, Alibaba |
| 36 | 4 | Automated End-to-End Model Serving with Cooperative Compilation | Yikang Zhang | Nanjing U |
| 37 | 4 | LLMFolder: Revisiting Constant Folding in LLMs | Gansen Hu | SJTU |
| 38 | 5 | iRoute: Local Routing Table Workflow Management | Yiming Li | Tianjin U, Tsinghua U |
| 39 | 5 | Efficient Data Passing for Serverless Inference: GPU-Centric | Hao Wu | HUST, CUHK-Shenzhen |
| 40 | 5 | DROPS: Managing Serverless Resource Pools in Azure Functions | Ahmed Alquraan | U Waterloo, Microsoft |
| 41 | 5 | Squeezy: Rapid VM Memory Reclamation for Serverless | Orestis Lagkas Nikolos | NTUA, UIUC |
| 42 | 5 | Demystifying Serverless Costs on Public Platforms | Changyuan Lin | UBC, Johns Hopkins |
| 43 | 5 | Fix: Externalizing Network I/O in Serverless Computing | Yuhan Deng | Stanford U |
| 44 | 5 | Bridging GPU Utilization Gap: Predictive Multi-Dimensional Scheduling | Yilei Lu | Tsinghua U, Alibaba |
| 45 | 5 | Untangling GPU Power Consumption: Job-Level Inference | Pierre Jacquet | ETS, Inria, OVHcloud |
| 46 | 5 | In-Production Characterization of Open Source Serverless Platform | Nima Nasiri | UBC, IBM |
| 47 | 5 | Serverless Replication of Object Storage across Multi-Vendor Clouds | Junyi Shu | PKU, UCLA |
| 48 | 5 | NADINO: RDMA-capable DPUs in Multi-Tenant Serverless Clouds | Shixiong Qi | U Kentucky, UC Riverside |
| 49 | 6 | REPS: Recycled Entropy Packet Spraying for Load Balancing | Tommaso Bonato | ETH Zurich, Microsoft |
| 50 | 6 | Learn-to-Probe: Signal Distinguishability in Congestion Control | Han Tian | USTC, HKUST |
| 51 | 6 | Canopy: Property-Driven Learning for Congestion Control | Chenxi Yang | UT Austin, Google DeepMind |
| 52 | 6 | Concord: Learning Network Configuration Contracts | Ryan Beckett | Microsoft Research, UIUC |
| 53 | 6 | PatternSketch: Runtime Reconfigurable Traffic Pattern Detection | Yang Du | Soochow U |
| 54 | 6 | Solar-NP: Rearchitecting Programmable Networks for In-Network Computing | Haifeng Sun | PKU, Huawei |
| 55 | 6 | Themis: Packet Spraying over Commodity RNICs | Xiangzhou Liu | HKUST |
| 56 | 6 | Practical RDMA Connection Sharing for HPC Workload | Yuejie Wang | PKU, Huawei |
| 57 | 6 | SmartNS: Line-rate Network Stack with SmartNIC | Xuzheng Chen | Zhejiang U, Alibaba |
| 58 | 6 | LCMP: Long-Haul Cost-Aware Multi-Path Routing for Inter-DC RDMA | Dong-Yang Yu | BUPT, PKU |
| 59 | 7 | SwitchFS: Async Metadata Updates with In-Network Coordination | Jingwei Xu | SJTU |
| 60 | 7 | MesaFS: I/O-Efficient Metadata Service for Distributed FS | Hao Guo | Tsinghua U |
| 61 | 7 | PASS: Power Adaptive Storage Server | Dedong Xie | U Washington, Databricks |
| 62 | 7 | TCO-driven Storage Provisioning for Exascale Data Centers | Timothy Kim | CMU, Google |
| 63 | 7 | ASIC-based Compression Accelerators for Storage Systems | Tao Lu | DapuStor |
| 64 | 7 | ColdCode: Cold Data Encoding for 3D NAND Flash Reliability | Qiao Li | MBZUAI, Xiamen U |
| 65 | 7 | Omar: Scheduling Cloud Block Storage Proactively and Reactively | Xinqi Chen | SJTU, Alibaba |
| 66 | 8 | SKernel: Elastic Secure Container with Split-Kernel Architecture | Xiaohu Chai | Tsinghua U, Ant Group |
| 67 | 8 | Pyramid: Secure, Resource-Efficient Kubernetes for Multi-Tenancy | Xiang Li | Tsinghua U, China Telecom |
| 68 | 8 | TrustWeave: Integrity Measurement for Multi-Cloud LLMs | Jianchang Su | UConn, Tsinghua U |
| 69 | 8 | Lessons Learned from Formal Methods in Huawei Cloud | Claudia Cauli | Huawei Ireland |
| 70 | 9 | CofferOS: Hardening OS-level Virtualization with Rust | Minkyu Jung | KAIST, UIUC |
| 71 | 9 | Wayfinder: Automated Operating System Specialization | Alexander Jung | Lancaster U, Unikraft |
| 72 | 9 | NecoFuzz: Fuzzing Nested Virtualization via Fuzz-Harness VMs | Reima Ishii | U Tokyo, AIST |
| 73 | 9 | Practical x86-64 Emulation on RISC-V | Xiongchuan Tan | Tsinghua U |
| 74 | 9 | VM Live Migration Between Heterogeneous Processors | Kenta Ishiguro | UGA, INRIA |
| 75 | 9 | Chimera: Transparent ISAX Heterogeneous Computing via Binary Rewriting | Jiatai He | ISCAS |
| 76 | 10 | OptiLog: Assigning Roles in Byzantine Consensus | Hanish Gogada | U Stavanger |
| 77 | 10 | Ethane: Debloating State Data using Compact Trie for Blockchain | Junmo Lee | Seoul National U |
| 78 | 10 | Improving Throughput of DAG-based BFT SMR | Nibesh Shrestha | Supra, Purdue |
| 79 | 10 | ECCB: Boosting Block Propagation with Erasure-Coded Compact Block | Bingyi Cai | HUST, UT Arlington |
| 80 | 10 | Fuzzing Enterprise-Grade Blockchain Systems | Fuchen Ma | Tsinghua U |
| 81 | 11 | Proteus: Heterogeneous FPGA Virtualization | Felix Gust | TUM, UCLA |
| 82 | 11 | NutCracker: Compilation Framework for Hybrid DPU Architectures | Yihan Yang | NUS, MPI-SWS |
| 83 | 11 | CHARM: Chiplet Heterogeneity-Aware Runtime Mapping | Alessandro Fogli | Imperial College |
| 84 | 11 | RoPeerTo: Datacenter-Scale P2P DMA between GPUs and FPGAs | Marco Venere | Polimi, ETH Zurich |
| 85 | 12 | Neuro-C: Neural Inference Shaped by Hardware Limits | Diletta Romano | Uppsala U |
| 86 | 12 | viNPU: Optimizing ViT Inference on Mobile NPUs | Jeho Lee | Yonsei U |
| 87 | 12 | E-Cube: Event Enhanced Video Streaming for Drones | Jingao Xu | HKU, U Pittsburgh |
| 88 | 12 | Efficient ML Model Updates for Embedded Microcontrollers | Shishir G. Patil | UC Berkeley |
| 89 | 12 | SwiftFL: Speculative Training for On-Device Federated DL | Yuhui Zhang | CAS IIE, PKU |
| 90 | 12 | PointShuffler: Accelerating Point Cloud NNs on GPUs | Yangfan Li | Central South U |
| 91 | 12 | TAO: Tolerance-Aware Optimistic Verification for FP NNs | Jianzhu Yao | Princeton, HKUST(GZ) |
| 92 | 12 | GeDES: GPU-Driven Discrete Event Network Simulator | Qinyong Li | UESTC |
| 93 | 12 | Effective On-Hardware Fuzzing of Embedded OS | Yuheng Shen | Tsinghua U |
| 94 | 12 | TierScape: Multiple Compressed Tiers for Server Memory TCO | Sandeep Kumar | Intel Labs |
| 95 | 12 | MTTM: Dynamic Fast Memory Partitioning for Multi-tenant Cloud | Changjun Lee | KAIST |
| 96 | 12 | BASK: Batch And SmartNIC-offloaded KSM | Chanshin Kwak | KAIST |
| 97 | 12 | PaCaR: Page Cache Replication for NUMA I/O Locality | Jerome Coquisart | RWTH Aachen |
| 98 | 12 | FUR: Fast and Unlimited Reads on Persistent Memory Transactions | Joao Barreto | INESC-ID |
| 99 | 12 | Reducing GPU Memory Bottleneck with Lossless Compression for ML | Aditya Kamath | U Washington, Google |
| 100 | 12 | Carbon-Aware Continuous Learning for Sustainable Real-Time ML | Gwanjong Park | Sungkyunkwan U |
| 101 | 12 | FlexiQ: Adaptive Mixed-Precision Quantization | Jaemin Kim | SNU |
| 102 | 12 | Million-Scale Text-to-Video Retrieval with Hyperdimensional Computing | Hyunsei Lee | DGIST |
| 103 | 12 | Matrix-PIC: Matrix Outer-product for Particle-in-Cell Simulations | Yizhuo Rao | Sun Yat-sen U |
| 104 | 12 | Elastic QEC Decoders | Satvik Maurya | UW-Madison |
| 105 | 12 | Prediction-Informed Power Management for Compute Servers | Jonggyu Park | U Washington |
| 106 | 12 | On-device Semantic Selection: Monolithic Forwarding | Jiahao Zhou | SJTU, Huawei |
| 107 | 12 | LightDSA: Efficient DSA Through Hardware-Aware Optimization | Yuansen Wang | RUC, Alibaba |
| 108 | 12 | GPU Kernel Idempotency Validation | Mingcong Han | SJTU |
| 109 | 12 | swKokkos: Athread Backend for Sunway | Junlin Wei | CNIC CAS |
| 110 | 12 | MinatoLoader: Accelerating ML Training Through Data Preprocessing | Rahma Nouaji | McGill U |
| 111 | 12 | Multipath Collective Communication in GPU Clouds | Yuchen Xu | PKU, Tencent |
| 112 | 12 | Gopher: Dynamic Graph Pattern Mining via DAG-Driven Execution | Yi Zhang | HUST |
| 113 | 12 | AEP: Hierarchical Fault Tolerance in DSM | Zixuan Wang | HUST, UT Arlington |
| 114 | 12 | EMVOD: Elastic Multi-Path QUIC Scheduling for CDN VoD | ZiQi Wei | Tsinghua SIGS |
| 115 | 12 | Mitigating CDN Cache Misses: Origin Shield for Billion-QPS | Zixuan Yang | Nanjing U, Tencent |
| 116 | 12 | RLive: Robust Delivery System for Live Streaming | Yu Tian | ICT CAS, ByteDance |
| 117 | 12 | Scalable RDMA Locks: Shared Stream Abstraction | Miao Cai | NUAA |
| 118 | 12 | RaidenSwap: Multi-Swap Remote System for Multi-core | Kefan Liu | ICT CAS |
| 119 | 12 | FicusDB: Scalable Multi-Versioned Authenticated Archival Storage | Hongbo Zhang | Cornell U |
| 120 | 12 | Logically Disaggregated Cache for Replicated Storage | Kiran Hombal | UIUC |
| 121 | 12 | Once Rolling Hashing in Delta Compression | Haoliang Tan | HIT (Shenzhen) |
| 122 | 12 | 2DIO: Configurable Trace Generation for Storage Benchmarking | Yirong Wang | Northeastern U |
| 123 | 12 | Fast Crash Consistency: Opportunistic Order Elimination | Jiahao Chen | HIT (Shenzhen) |
| 124 | 12 | CSnake: Detecting Cascading Failure via Causal Stitching | Shangshu Qian | Purdue U |
| 125 | 12 | Garen: Reliable Cluster Management with Atomic State Reconciliation | Mingi Kim | FriendliAI, SNU |
| 126 | 12 | Avicenna: Masking Slowdowns in Replicated State Machines | Christopher Hodsdon | Databricks, Princeton |
| 127 | 12 | Rose: Reproducing External-Fault-Induced Failures | Sebastiao Amaro | INESC-ID, Purdue |
| 128 | 12 | Proactive Change Risk Detection in Production Cloud Systems | Jinyang Liu | ByteDance |
| 129 | 12 | Five Minutes of DDoS Brings down Tor | Zhongtang Luo | Purdue U |
| 130 | 12 | Yield Not Thy Core | Achilles Benetopoulos | UC Santa Cruz |
| 131 | 12 | No More Translation at Runtime: LLM-Empowered Static Binary Translation | Zhibo Liu | HKUST |
| 132 | 12 | Low-Compilation-Cost Register Allocation in LLVM-Based BT | Xiangwei Meng | Lanzhou U |
| 133 | 12 | Digital Hole: Bypassing Commercial Audio DRM | Bjorn Ruytenberg | VU Amsterdam |
| 134 | 12 | Turnstile: Hybrid IFC Framework for IoT Privacy | Kumseok Jung | UBC, Princeton |
| 135 | 12 | LifeFuzz: Lifecycle-Guided Fuzzing for Windows Driver | Chendong Yu | CAS IIE |

> 注：#130 PARD同Part 2(2.16)，#131 Laminar同Part 1(1.16)，#149 Fuzzing Enterprise Blockchain同Part 10(10.5)，#155 ECCB同Part 10(10.4)，已在前文相应Part中详细覆盖。

---

# 全局综述与跨领域技术线索

## 会议趋势分析

### 1. AI系统主导地位（~38%）
LLM训练、推理、应用相关论文共约30篇，占录用总数的38%。AI系统已从EuroSys的“新兴方向”转变为绝对主流。这反映了：
- 大模型训练和推理的系统级优化已成为核心研究问题
- 从单机优化到集群级优化，再到跨集群和多云优化的演进
- Agent作为LLM的应用层正在催生新的系统需求

### 2. Serverless持续演进（~13%）
Serverless相关论文10篇，涵盖从资源池管理到跨云复制的全栈问题。趋势包括：
- 从函数级优化到工作流级优化的转变
- GPU Serverless作为新兴方向出现（GPU-centric数据传递、DPU卸载）
- 成本透明化和能效优化成为关注焦点

### 3. 网络与通信创新（~13%）
10篇网络论文反映了AI时代数据中心网络的变革需求：
- RDMA优化和跨DC路由成为核心问题
- 可编程交换机和SmartNIC正在重塑网络架构
- 学习型网络控制与形式化保证的结合成为新趋势

### 4. 安全与可信执行成为新焦点
- TEE保护LLM模型和推理的安全问题被提出（TZ-LLM、TrustWeave）
- 安全容器架构创新（SKernel分裂内核、Pyramid多租户K8s）
- 形式化方法在工业云系统中的落地经验（华为云）

## 跨领域技术线索汇总

### Agent方向启示
1. **声明式OS接口**（3.2 From Imperative to Declarative）：Agent的交互范式应转向声明式，直接表达意图而非模拟人类操作
2. **云-边协同部署**（3.1 AIMS）：Agent组件的分层部署是降低延迟和成本的关键架构
3. **多SLO服务**（2.1 AdaServe）：Agent的多优先级请求处理需要SLO定制的推理服务
4. **多LoRA并发微调**（1.2 LoRAFusion）：Agent多任务适配的高效训练方法
5. **多模态服务**（2.11 Eevee）：视觉+语言Agent的模块复用推理优化

### 系统软件方向启示
1. **通信-计算重叠**（1.10 FlashOverlap）：信令机制作为通用计算-通信重叠范式
2. **内存分配器优化**（1.5 STAlloc）：离线规划+在线分配的混合范式可应用于通用内存管理
3. **网内协调**（7.1 SwitchFS）：可编程交换机作为分布式协调层
4. **声明式网络编程**（6.6 Solar-NP）：OAT抽象为数据平面有状态操作提供新模型
5. **分裂内核架构**（8.1 SKernel）：安全与功能分离的内核设计模式

### 云原生与分布式架构启示
1. **飞行中流水线重构**（2.2 FlexPipe）：Serverless环境的自适应部署创新
2. **跨区域负载均衡**（2.5 SkyWalker）：利用时区差异提高全球资源利用率
3. **多维资源调度**（5.7）：GPU计算、显存、网络等多维资源的联合调度
4. **DPU基础设施卸载**（5.11 NADINO）：多租户环境下DPU的真正价值释放
5. **Serverless跨云编排**（5.10）：Serverless函数驱动的多云数据同步

### 安全与可信计算启示
1. **形式化保证+学习型系统**（6.3 Canopy）：属性驱动学习为AI系统提供可证明的安全保证
2. **TEE保护端侧LLM**（2.15 TZ-LLM）：流水线恢复+协同驱动实现高效TEE内推理
3. **配置合约自动学习**（6.4 Concord）：从历史配置学习规则预防配置错误
4. **多云信任链**（8.3 TrustWeave）：跨不信任云提供商的LLM完整性验证

### 硬件-软件协同设计启示
1. **SmartNIC线速网络栈**（6.9 SmartNS）：BlueField-3验证SmartNIC中心网络栈可行性
2. **DPU多租户卸载**（5.11 NADINO）：DPU从概念到实际多租户场景的落地
3. **移动NPU测试时缩放**（2.13）：利用NPU冗余计算做并行推理增强
4. **全栈可编程网络**（6.6 Solar-NP）：从芯片到语言到工具链的端到端设计

### 绿色计算与可持续性启示
1. **GPU功耗作业级归因**（5.8）：精细化能耗管理的基础
2. **碳感知持续学习**（12.16）：将碳排放目标纳入在线学习决策
3. **功耗自适应存储**（7.3 PASS）：存储服务器的功耗-性能动态平衡
4. **TCO驱动存储配置**（7.4）：成本优化自然推动能效优化

### 边缘计算与端侧部署启示
1. **端-云协同推理**（2.14 TailorLLM）：LoRA矩阵库动态管理实现高效协同
2. **端侧测试时缩放**（2.13）：小模型+并行推理在NPU上匹配大模型精度
3. **TEE保护设备端LLM**（2.15 TZ-LLM）：在OpenHarmony上实现安全的端侧推理
4. **联邦MoE微调**（1.3 FLUX）：消费级GPU参与大模型协作训练

## 开放性问题与未来研究方向

1. **Agent系统基础设施**：随着Agent从原型走向生产，需要专用的系统基础设施支持（调度、安全、可观测性）
2. **异构集群训练**：A100+H100+H200混合集群的自动化并行策略和负载均衡
3. **跨云AI基础设施**：多云训练和推理的网络、存储、调度全栈优化
4. **可信AI系统**：形式化保证+学习型系统的结合将推动AI系统在关键领域的部署
5. **绿色AI基础设施**：从碳感知调度到功耗自适应存储的全栈能效优化
6. **端-云-边协同**：三层协同的AI服务架构将成为下一个系统研究热点
---

> **数据来源声明**: 本报告的论文信息来自EuroSys 2026官网、arXiv、ACM Digital Library等公开渠道。论文技术概要基于已公开的摘要、作者声明撰写。
>
> **撰写日期**: 2026年6月10日
