# 华为云 ModelArts 深度研究：业务背景、技术架构、集群实践与改进路径

**作者：** AtomCode 研究整理
**日期：** 2026-07-03
**版本：** V1.0
**文档类型：** 技术研究报告 / Survey

---

## 摘要（中文）

华为云 ModelArts（魔坊）是面向 AI 开发者的一站式模型训推平台，定位为全栈全生命周期的 AI 工程化基座。本研究系统梳理 ModelArts 的业务背景、问题挑战、三层技术架构（算力层 / AI 平台层 / AI 开发工具链层）、关键技术实现（MoXing 分布式加速框架、AutoSearch 自动超参搜索、EI-Backbone 骨干模型、联邦学习）、以及在昇腾集群上跑通多机多卡大模型训练作业的具体工程实践，包括 VPC/SFS/OBS/SWR 资源准备、专属资源池、Volcano 调度、ranktable 动态路由、超节点亲和组、HCCL 通信与故障恢复（原地恢复 / Job 级重调度 / 算子重执行）等。研究进一步将其与 AWS SageMaker、Google Vertex AI、Azure ML 进行横向对比，并基于 2025–2026 年学术前沿（Megatron MoE Parallel Folding、MegaScale-MoE、FlowMoE、Tessera OSDI'26、COMET MLSys'25、X-MoE）提出深入改进路径：MoE 通信-计算细粒度重叠、Attention 与 MoE 解耦的并行映射、FP8 低精度训练、Ulysses 长序列并行、内存碎片与自适应重计算、运行时动态气泡填充，以及生态开放性建设。研究指出，当前 ModelArts 在"粗放可用"层面已具备万卡级训练与 0.5% 以下作业失败率，但向"高效精打"演进仍需在 MoE 系统软件、跨平台内核、生态中立性与可复现性基线四个方向持续投入。

**关键词：** ModelArts；昇腾；分布式训练；MLaaS；MoE；HCCL；超节点；MLOps

---

## Abstract (English)

Huawei Cloud ModelArts is a one-stop model training-and-inference platform positioned as a full-stack, full-lifecycle AI engineering substrate. This study systematically surveys ModelArts along five axes: business background, problem challenges, the three-layer technical architecture (compute / AI platform / AI development toolchain), key technologies (the MoXing distributed acceleration framework, AutoSearch hyperparameter optimization, the EI-Backbone foundation model, and federated learning), and concrete engineering practice for running multi-node multi-card large-model training jobs on Ascend clusters — covering VPC/SFS/OBS/SWR provisioning, dedicated resource pools, Volcano scheduling, ranktable dynamic routing, super-node affinity groups, HCCL collective communication, and multi-strategy fault recovery (in-place recovery, job-level rescheduling, operator re-execution). The report then benchmarks ModelArts against AWS SageMaker, Google Vertex AI, and Azure ML, and, grounded in 2025–2026 academic frontiers (Megatron MoE Parallel Folding, MegaScale-MoE, FlowMoE, Tessera OSDI'26, COMET MLSys'25, X-MoE), proposes concrete improvement paths: fine-grained MoE compute-communication overlap, decoupled Attention/MoE parallelism mapping, FP8 low-precision training, Ulysses long-context parallelism, memory-fragmentation and adaptive recomputation, runtime dynamic bubble filling, and ecosystem openness. We argue that ModelArts has reached the "coarsely usable" tier — 10K-card training with sub-0.5% job failure rates — but the transition to "efficiently refined" requires sustained investment in four directions: MoE system software, cross-platform kernels, ecosystem neutrality, and reproducibility baselines.

**Keywords:** ModelArts; Ascend; distributed training; MLaaS; MoE; HCCL; super-node; MLOps

---

## 1. 业务背景与市场定位

### 1.1 MLaaS 范式与产业驱动力

机器学习即服务（Machine Learning as a Service, MLaaS）指涵盖数据预处理、模型训练、模型评估与预测的全自动或半自动云平台的总称 [1]。对于多数企业而言，自建机器学习栈既昂贵又困难，且需要稀缺的高科技人才储备。一切皆服务（everything-as-a-service）的趋势使得企业可以用一个小团队、无需大量前期投资即开始构建模型并从预测中获得价值。在这一产业背景下，主流云厂商陆续推出端到端 ML 平台：AWS SageMaker（2017 年发布，市场占有率约 34% [2]）、Microsoft Azure ML（约 29% [2]）、Google Vertex AI（约 22% [2]），以及华为云 ModelArts。

ModelArts 最初从华为内部衍生：华为内部有大量算法工程师与 AI 开发者，他们在数据准备、模型训练慢、环境配置繁杂等痛点上的解决方案被沉淀积累，最终在华为云上对外开放前已经过内部众多 AI 工程师锤炼 [3]。这一"内部孵化→外溢商业化"的路径与 SageMaker 起源于 Amazon 内部机器学习需求高度相似，是理解 ModelArts 工程取向的关键背景。

### 1.2 全栈全场景 AI 战略

ModelArts 是华为"全栈全场景 AI 解决方案"面向开发者与用户的门户 [3]。所谓"全栈"指从最底层的昇腾 AI 芯片（Ascend 910/310 系列）、异构计算架构 CANN、到上层框架 MindSpore、再到应用使能 MindSpeed/ModelArts 工具链的垂直整合；"全场景"指端、边、云协同部署能力。这一垂直整合战略与 Google 的"TPU + TensorFlow + Vertex AI"路线同构，但与 AWS、Azure 主要依赖 NVIDIA GPU 加速器、对自研芯片采取补强而非全栈主导的策略形成鲜明对比。其优势在于软硬协同优化空间大、单位算力成本可控；代价是生态封闭性、跨平台可移植性受限。

### 1.3 产品形态演进

ModelArts 的产品定位经历了从"通用一站式 AI 开发平台"到"大模型训推一体化平台"的演进。早期 ModelArts 强调数据标注、自动学习（AutoLearning）、MoXing 加速框架与端-边-云部署；ModelArts 3.0（2020 年）引入四大新特性：EI-Backbone 骨骨模型、联邦学习、可视化评估与智能诊断、Turbo 与经济双模式、以及集群规模/任务数量/分布式训练的针对性优化 [4]。当前最新版本（2025–2026 文档记为"魔坊（ModelArts）模型训推平台"）已明确以大模型为核心，宣称支持万亿参数模型训练、单作业百 PB 级数据、万卡集群 30 天不中断、作业失败率低于 0.5% [5]。这一演进反映了整个行业从"通用 ML 工作流"向"大模型基础设施"的重心迁移。

### 1.4 目标用户与典型场景

平台面向三类用户：(1) 入门级业务开发者，通过自动学习与 Workflow 低代码 DAG 工具实现零代码模型定制；(2) 算法工程师与数据科学家，通过 Notebook（云上 JupyterLab 或本地 IDE + ModelArts 插件远程开发）、预置镜像、SDK 进行代码优先开发；(3) 大规模训练用户，通过专属资源池、Lite Server/Cluster 进行千卡至万卡级大模型预训练与微调。典型落地场景覆盖工业质检、智慧交通、自动驾驶标注、医疗影像、遥感、零售安防、金融风控、运营商智算中心等 [3][5]。

---

## 2. 问题挑战

ModelArts 面临的工程挑战既来自 AI 训练系统的一般性难题，也来自其"全栈自研 + 昇腾硬件"路线特有的约束。可归纳为六类。

### 2.1 大规模分布式训练的加速比瓶颈

当训练从单卡扩展到千卡、万卡时，通信开销逐渐主导收敛时间。斯坦福 DAWNBench 的 ResNet50-on-ImageNet 基准上，单块 P100 GPU 训练需约一周 [3]；华为云 ModelArts 用 128 块 V100 GPU 在 4 分 08 秒内完成训练，比 fast.ai 在 AWS 上的成绩快 4 倍 [6]。即便如此，千级资源规格下 ResNet50 加速比仅能做到 >0.8 [3]，距离理想线性扩展仍有显著差距。当模型规模跃迁至万亿参数 MoE 架构、序列长度延伸至百万 token，通信-计算比急剧恶化，all-to-all 与 all-reduce 成为关键瓶颈。

### 2.2 万卡集群的稳定性与故障恢复

大模型训练周期以周乃至月计，硬件故障不再是小概率事件。在万卡集群上，单卡日均故障率即使仅 0.01%，30 天训练周期内遇到至少一次故障的概率也接近 1。ModelArts 官方目标为"作业失败率低于 0.5%、万亿参数模型训练 30 天不中断" [5]，这对故障检测、隔离、恢复提出了极高要求。昇腾新一代超节点硬件 Snt9b23 的"超平面"网络由两层交换机实现 NPU 互联，光模块故障率偏高，链路闪断会直接导致通信算子报错 [7]，成为稳定性短板。

### 2.3 异构算力与跨平台生态

ModelArts 同时承载 GPU（早期主流，如 V100）与昇腾 NPU（910A/B/C 系列）两类异构算力，且不同昇腾型号（910B1/B2/B3/B4、910C、超节点 Snt9b/Snt9b23）在显存容量、算力、互联带宽上差异显著 [8]。这给预置镜像、框架适配、性能调优带来复杂度。CANN 与 HCCL 作为昇腾专属软件栈，与 NVIDIA CUDA/NCCL 生态不互通；当前主流开源 MoE 训练框架（Megatron-Core、Tutel、FasterMoE、ScheMoE）几乎只针对 NVIDIA GPU 优化，在昇腾 NPU 上"表现欠佳"是已被学术工作明确指出的问题 [9]。

### 2.4 生态封闭性与可移植性

垂直整合战略带来软硬协同优势的同时，也带来了生态封闭代价。ModelArts SDK 仅提供 Python、且不支持在训练作业与推理在线服务内调用 [10]；MoXing 框架构建于 TensorFlow/MXNet/PyTorch/MindSpore 之上但属自研抽象 [11]；CANN/torch_npu/MindSpeed 与 CUDA/NCCL/Megatron-LM 原生路径存在割裂。相比之下，SageMaker、Vertex AI、Azure ML 三家均原生支持 MLflow 跟踪，pipeline 编排虽各有 SDK 但生态相对开放 [1][2]。跨平台可移植性是华为云 AI 业务出海与吸引第三方开发者必须正视的硬约束。

### 2.5 数据工程与全生命周期管理

AI 开发中数据准备与标注往往耗费整体开发一半以上时间 [3]。ModelArts 需要管理从原始数据、标注数据、训练作业、算法、模型到推理服务的全生命周期溯源，官方基于华为 EYWA 图计算引擎支持千万级模型/数据集/服务对象管理 [3]。在 PB 至百 PB 级训练数据规模下，OBS 对象存储与 SFS Turbo 文件存储的协同、数据加速下载（moxing.file.copy_parallel）、数据集版本管理与可复现性，构成另一组工程难题。

### 2.6 从"通用 ML"到"大模型"的范式迁移压力

ModelArts 早期设计的自动学习、AutoSearch 超参搜索（贝叶斯 SMAC、TPE、模拟退火 [12]）主要面向传统机器学习与中小规模深度学习模型；当模型规模跃迁至千亿、万亿参数，AutoML 的搜索空间维度爆炸，传统黑盒超参搜索算法不再适用，需要与分布式训练系统、并行策略搜索、显存优化深度耦合的"系统级 AutoML"。这是平台当前最根本的范式迁移压力。

---

## 3. 技术架构

ModelArts 采用清晰的三层架构（见图 1 概念图），自底向上为算力层、AI 平台层、AI 开发工具链层 [5][13]。

### 3.1 算力层

算力层提供全系列昇腾硬件与万卡级大规模集群管理能力，兼容业界主流 AI 开发调试、训练推理框架 [13]。核心硬件包括：

- **Atlas 800T A2 训练服务器**：4U 形态，4×鲲鹏 920 CPU，搭载 8 颗 Ascend 910B 系列 NPU，提供 8×200GE QSFP 接口直出（RoCE 协议），4×2.6kW 冗余电源，N+1 风扇冗余，5–35℃ 风冷工作环境 [14]。
- **Ascend 910B 系列**：按算力升序分为 B1/B2/B3/B4 四款，FP16 算力 280–414 TFLOPS，显存 32–64GB HBM2e，对应不同整机型号与场景定位 [8]。
- **Ascend 910C 与超节点**：双芯合封，FP16 算力达 780–800 TFLOPS，内存带宽 3.2 TB/s；CloudMatrix 384 超节点由 384 张 910C 组成，算力达 300 PFlops [8]。
- **超节点 Snt9b23**：使用 HCCS 总线将多个计算节点的 NPU 互联组成超节点，超节点内全互联组网形态称为"超平面"，可极大提升 AI 任务通信效率 [15]。

集群组网层面，昇腾训练解决方案提供 Atlas 900 A2 PoDc、Atlas 900 A2 PoD、Atlas 200T A2 Box16 等多种集群形态 [16]，采用 Spine-Leaf 两层交换机架构。三种平面的职责分工需要明确区分，这是理解后续通信优化与故障恢复的前提：

| 平面 | 协议 | 承载业务 | 关键约束 |
|---|---|---|---|
| 参数面（业务面） | RoCE / RoH over 200GE | 训练梯度同步、HCCL all-reduce/all-to-all | 带宽主导，光模块闪断高发 |
| 存储面 | NFS over TCP | SFS Turbo 共享挂载、OBS 加速下载 | IO 吞吐与训练数据加载并行度耦合 |
| VPC 平面（管理面） | TCP | 通信域状态协商、Pod 调度、健康检查 | HCCL 算子重执行依赖 VPC 平面协商 |

超节点 Snt9b23 的"超平面"组网是关键创新：HCCS 总线将多个计算节点的 NPU 全互联，形成单层超大通信域；而传统 Spine-Leaf 两层架构下，跨节点通信需经 Leaf→Spine→Leaf 两跳，超平面将其压缩为单跳，all-reduce 与 MoE all-to-all 的有效带宽因此显著提升 [15]。但这一架构也带来新故障模式——L1-L2 链路光模块闪断会直接中断整个通信域业务，HCCL 算子重执行机制正是为此设计 [7]。

### 3.2 AI 平台层

AI 平台层提供端到端 AI 开发工具链，支持开发者一站式完成模型开发和上线，并提供高效资源管理能力与自动化故障恢复 [13]。其功能模块包括：

| 模块 | 职责 |
|---|---|
| 数据管理 | 多源数据连接、数据集创建、标注（图片分类/物体检测/分割/语音/文本）、版本管理、自动预标注与辅助标注 |
| 开发环境 | 云上 JupyterLab Notebook、本地 IDE + ModelArts 插件远程开发、预置镜像（PyTorch/MindSpore/CANN） |
| 模型训练 | 企业级分布式训练平台，支持一键发起超大规模分布式任务、超参搜索、增量训练、断点续训 |
| 推理部署 | 新一代分布式弹性推理平台，深度集成自研优化 vLLM，支持在线/批量/边缘多形态部署、PD 弹性伸缩、Token 级快恢 |
| 资源管理 | 公共资源池与专属资源池、Lite Server（裸金属）、Lite Cluster（原生 Kubernetes API）、逻辑子池配额 |
| 运维运营 | 性能分析诊断、故障诊断、AOM 监控、LTS 日志、EYWA 溯源图 |

资源池是平台的调度与隔离单元。专属资源池提供独立计算集群与网络，不同用户物理隔离，可接入用户自有 VPC 访问 SFS 等存储 [17]；可进一步切分逻辑子池并设置保留配额与上限。Lite Cluster 面向 Kubernetes 资源用户，提供原生 K8s API 直接管理节点与集群，训练任务以 Volcano job 模式下发 [18]。

调度链路需要进一步拆解才能看清"训练作业如何从控制台请求落到具体 NPU 上"。完整链路为：控制台创建作业 → ModelArts 训练服务 API → Volcano scheduler（按亲和组约束 + 资源配额过滤候选节点）→ kubelet 拉起 Pod → CCE/Ascend device plugin 分配 NPU 设备 → 注入 `RANK_TABLE_FILE` 环境变量 → 容器启动用户启动命令 [18][26]。其中三个关键调度决策点决定作业能否高效运行：

1. **亲和组约束**：超节点亲和组要求同组实例必须调度到同一超节点内，Volcano 通过 `cce.kubectl.kubernetes.io/ascend-rank-table` 注解感知超节点拓扑 [15][18]。
2. **资源配额过滤**：逻辑子池的保留配额与上限决定多租户场景下的资源争抢结果，未配置保留配额的子池在峰值时可能被高优作业挤占 [17]。
3. **设备分配**：Ascend device plugin 按 `DEVICE_NUM` 与 `RANK_SIZE` 环境变量分配 NPU 卡，单节点 8 卡全部占用即为"占满节点"，是亲和组生效的前提 [34]。

数据流层面，训练作业涉及三类数据移动，其性能特征差异显著：

| 数据流 | 路径 | 典型瓶颈 | 加速手段 |
|---|---|---|---|
| 训练数据加载 | OBS → 训练容器本地 / SFS Turbo → DataLoader | 小文件海量 IO、首启延迟 | `mox.file.copy_parallel` 多线程下载、SFS Turbo 本地缓存、多级并发输入流水线 [23][3] |
| Checkpoint 持久化 | 训练容器 → SFS Turbo / OBS | 大文件写带宽、万卡并发写 | 异步保存、增量 CKPT、存储挂载避免 OBS PUT 延迟 [29] |
| 梯度同步 | NPU HBM ↔ HCCS/RoCE 互联 ↔ 对端 NPU HBM | all-reduce/all-to-all 通信量、跨节点带宽 | HCCL 拓扑感知、ranktable 动态路由、算子-通信重叠 [7][18] |

### 3.3 AI 开发工具链层

AI 开发工具链层提供端到端大模型开发工具链，支持主流优质开源大模型"开箱即用"，提供大模型开发套件 [13]。这一层向上对接 AI Gallery（开发者生态社区，提供模型、API、数据集、竞赛案例共享与交易 [3]），向下集成昇腾生态的开源组件：

- **MindSpeed-LLM**（原 ModelLink）：基于昇腾生态的大语言模型分布式训练套件，内置百余个业界常用 LLM 的预训练与微调支持 [19]。
- **MindSpeed**：针对昇腾设备的大模型加速库，使能客户大模型业务快速迁移至昇腾，支持 Megatron 数据/张量/流水/虚拟流水/序列并行、分布式优化器、异步 DDP，以及昇腾亲和的 TP 重计算通信优化、内存碎片优化、自适应重计算、计算通信并行、Ulysses 长序列并行等特性 [20]。
- **CANN**（Compute Architecture for Neural Networks）：异构计算架构，向上支持 MindSpore/PyTorch/TensorFlow，向下服务 AI 处理器；提供 HCCL 集合通信库、HIXL 单边通信库、ATB（Ascend Transformer Boost）加速库 [21]。
- **torch_npu**：PyTorch 的昇腾扩展，将 PyTorch 训练脚本一键式迁移至昇腾 NPU [21]。

### 3.4 架构总览

```
┌─────────────────────────────────────────────────────────────┐
│  AI Gallery / 开发者社区（模型/API/数据集/案例共享与交易）       │
├─────────────────────────────────────────────────────────────┤
│  AI 开发工具链层                                              │
│  MindSpeed-LLM · MindSpeed · CANN · torch_npu · ATB · HCCL    │
├─────────────────────────────────────────────────────────────┤
│  AI 平台层                                                    │
│  数据管理│开发环境│模型训练│推理部署│资源管理│运维运营           │
│  (公共/专属资源池 · Lite Server/Cluster · Volcano · EYWA)      │
├─────────────────────────────────────────────────────────────┤
│  算力层                                                       │
│  Atlas 800T A2 · Ascend 910B/C · 超节点 Snt9b23 · RoCE 200GE │
│  Atlas 900 A2 PoD/PoDc · CloudMatrix 384 超节点              │
└─────────────────────────────────────────────────────────────┘
```

*图 1. ModelArts 三层架构概念图（据 [5][13][14][19][20] 整理；可运行 matplotlib 脚本见 `figures/generate_figures.py` → `fig1_architecture()`）*

---

## 4. 关键技术实现

### 4.1 MoXing 分布式训练加速框架

MoXing（"模型"拼音）是华为云 ModelArts 团队自研的分布式训练加速框架，构建于 TensorFlow、MXNet、PyTorch、Keras 之上 [11][22]。其设计哲学是"一切优化都围绕模型展开"，让开发者只需关心 `input_fn`（数据输入）与 `model_fn`（模型构建），即可实现任意模型在多 GPU 与分布式下的高性能运行。

MoXing 的全栈优化链路包括 [3][22]：

1. **数据读取与预处理**：多级并发输入流水线使数据 IO 不成为瓶颈；`mox.file.copy_parallel` 提供数据下载加速，适用于 100w–1000w 文件数或单文件 >20GB 场景 [23]。
2. **模型计算**：半精度与单精度组成的混合精度计算，通过自适应尺度缩放减小精度损失。
3. **超参调优**：动态超参策略（momentum、batch size、image size 等）使模型收敛所需 epoch 数降到最低；LARS 优化器支持 batch_size=32k 的 ResNet-50 分布式训练；深度梯度压缩 DGC 将通信量降低至原 0.1% 而精度不降 [22]。
4. **底层优化**：与底层华为服务器和通信计算库（nstack、HCCL）相结合，实现分布式数据-模型混合并行、梯度自动融合拆分、基于 BP bubble 自适应的计算-通信算子调度。

性能层面，MoXing 在斯坦福 DAWNBench 上用 128 块 V100 GPU 训练 ResNet50-on-ImageNet 至 93% 以上精度仅需 4 分 08 秒，比 fast.ai 在 AWS 上的成绩快 4 倍，推理速度是第二名厂商的 1.7 倍 [6]。

需要指出的是，MoXing 是面向"传统深度学习模型 + GPU 集群"时代的产物，在大模型与昇腾 NPU 主导的当前阶段，其角色已被 MindSpeed-LLM 与 MindSpeed 加速库所承接。MoXing 框架的 `mox.file` 文件操作接口仍作为 OBS 访问的便捷封装在 Notebook 与训练脚本中广泛使用 [23]。

### 4.2 AutoSearch 自动超参搜索

AutoSearch 提供 0 代码修改基础上的超参搜索能力 [12][24]，内置三种算法：

- **贝叶斯优化（SMAC）**：基于高斯过程回归估计目标函数均值与方差，构造采集函数选择下一搜索点；利用历史评估结果降低迭代次数，但不易找到全局最优。
- **TPE（Tree-structured Parzen Estimator）**：为每个超参维护两个高斯混合模型 l(x) 与 g(x)，选择 l(x)/g(x) 最大化的超参作为下一组搜索值。
- **模拟退火（Anneal）**：从先前采样点出发，从密度集中在试验点周围的分布中采样，随时间倾向于从越来越接近最佳点处采样，以一定概率跳出局部最优。

AutoSearch 通过指标正则表达式从训练日志提取搜索指标（loss/accuracy），朝指定优化方向收敛。其局限在于：仅支持 float 类型超参、仅支持 pytorch_1.8.0/tensorflow_2.1.0 两款预置镜像 [24]，无法直接服务于大模型时代的并行策略搜索与系统级 AutoML。

### 4.3 EI-Backbone 与自动学习

ModelArts 3.0 引入华为云骨干模型 EI-Backbone，集模型高效、数据高效、算力高效、知识高效为一体，在 10 余个行业获得验证，发表相关顶级论文 100 余篇 [4]。自动学习（AutoLearning）面向零 AI 基础的业务开发者，根据标注数据自动设计模型、自动调参、自动训练、自动压缩与部署，支持图像分类、物体检测、预测分析、声音分类、文本分类五类项目 [25]。其关键技术包括基于信息熵上限近似模型的树搜索最优特征变换、贝叶斯优化自动调参、迁移学习（少数据生成高质量模型）、多维度模型架构自动搜索（NAS）。在新版本中，自动学习流程由 Workflow 低代码 DAG 工具承载 [25]。

华为与雨林保护组织合作项目中，ModelArts 自动学习声音分类对电锯与卡车噪音的识别精度超过许多博士手工调参结果 [3]，是自动学习实战能力的代表性案例。

### 4.4 联邦学习与数据安全

针对企业"数据不出户"的联合建模诉求，ModelArts 3.0 提供联邦学习特性：用户各自利用本地数据训练，不交换数据本身，只用加密方式交换更新的模型参数，实现协同训练 [4]。这一特性在大模型时代的隐私计算与跨机构数据协作场景中持续具有战略价值。

### 4.5 高性能通信库 HCCL

HCCL（Huawei Collective Communication Library）是华为专为昇腾 AI 处理器设计的分布式通信库，协调多个昇腾处理器之间的数据同步（梯度聚合、参数更新），减少通信开销，提升训练效率 [7]。HCCL 通过 `Ascend HCCL RANK_TABLE_FILE`（`jobstart_hccl.json`）描述集群拓扑，被 HCCL 解析用于分布式训练通信 [26]。

HCCL 提供的集合通信原语与典型用途需要明确，这是评估通信开销与优化空间的基础：

| 原语 | 通信量（N 卡） | 典型用途 | 优化要点 |
|---|---|---|---|
| AllReduce | O(N) 数据量 | 数据并行梯度聚合 | Ring/Tree 算法、梯度融合、计算-通信重叠 |
| AllGather | O(N) 数据量 | 张量并行前向/反向、ZeRO-3 参数收集 | 拓扑感知分桶、流水化 |
| ReduceScatter | O(N) 数据量 | ZeRO-2/3 梯度分片 | 与 AllGather 配对、通信压缩 |
| AllToAll | O(N²) 数据量 | MoE 专家路由、序列并行 | 稀疏 token 路由、padding-free 内核 |
| Broadcast | O(N) 数据量 | 初始权重分发、MoE gate 同步 | 树形拓扑、与首步 AllReduce 合并 |

超节点 Snt9b23 的"超平面"全互联组网对 AllReduce 与 AllToAll 收益最大——传统 Spine-Leaf 两跳通信压缩为单跳，有效带宽提升可达数倍 [15]。但 AllToAll 在 MoE 场景下仍是首要瓶颈：其通信量随专家数与卡数平方增长，且 token 路由的不均衡性引入运行时停顿，这是 §7.1 改进方向的根因。在超节点场景中，HCCL 引入算子级重执行机制以应对光模块闪断：当通信算子报 SDMA 或 RDMA CQE 错误时，HCCL 尝试重新执行该通信算子，成功率约 95%，有效降低回退至 checkpoint 断点续训的概率 [7]。重执行依赖通信域内所有卡停在同一通信算子处，这一前提在异步训练或流水并行场景下不成立，是其已知约束。

### 4.6 故障恢复与高可靠

ModelArts 的训练高可靠采用多级故障恢复策略 [27][28]：

| 策略 | 触发场景 | 机制 | 资源调度 |
|---|---|---|---|
| 原地恢复 | NPU 芯片可自愈故障（次要/重要级别故障码） | 强制停止用户进程，保留容器，尝试芯片自愈后重新运行启动命令 | 不涉及 |
| 作业卡死重启 | 训练作业卡死 | 强制停止用户进程，保留容器，重新运行启动命令 | 不涉及 |
| 隔离式 Job 级重调度 | 自愈失败、24h 内同节点同芯片 3 次相同故障码 | 终止所有 Pod，隔离故障节点，Job 实例完全重建 | 涉及 |
| 无条件 Job 重调度 | 作业异常退出码非 0 | 终止所有 Pod，Job 实例完全重建 | 涉及 |
| 算子重执行 | 通信链路闪断（HCCS/RoH/RoCE 平面） | HCCL 算子级重执行，借轨通信 | 不涉及 |

启用方式为创建训练作业时设置 `fault-tolerance/job-retry-num`（1–128）开启自动重启，设置 `fault-tolerance/hccl_op_retry=true` 开启算子重执行 [27][28]。原地恢复要求作业脚本可重入，需跳过数据下载/预处理步骤、删除与重建同名共享内存，可通过环境变量 `MA_PROC_START_CNT` 判断是否发生过原地恢复 [27]。

故障检测到恢复的时序是评估可用性的关键。一次典型 NPU 芯片可自愈故障的端到端时序（**以下数值为基于公开文档描述的工程估算，未经实测验证**）为：硬件健康检查守护进程检测到故障码（秒级）→ 上报训练服务（<1s）→ 强制停止用户进程并保留容器（数秒）→ 触发 NPU 芯片复位自愈（10–60s，取决于故障级别）→ 自愈成功后重新执行启动命令（容器重启 + 数据加载 + checkpoint 加载，数分钟）[27][28]。若自愈失败，降级路径为隔离式 Job 重调度：终止所有 Pod → Volcano 重新调度到健康节点 → 镜像重新拉取 → 容器重建 → 训练恢复，全程估算可达 10–30 分钟，万卡作业下影响显著。决策树如下：

```
故障发生
  ├─ 通信链路闪断 → 算子重执行（秒级，成功率~95%）→ 成功则继续
  │                                          └─ 失败 → 回退 checkpoint 续训
  ├─ NPU 芯片可自愈故障 → 原地恢复（分钟级，不占重启次数）
  │                          ├─ 自愈成功 → 继续
  │                          └─ 自愈失败 / 24h 内 3 次同故障码 → 隔离式 Job 重调度
  ├─ 作业卡死 → 卡死重启（保留容器）
  └─ 作业异常退出码非 0 → 无条件 Job 重调度（重建所有 Pod）
```

*图 3. ModelArts 多级故障恢复决策树（据 [27][28][7] 整理）*

配合上述策略，断点续训通过 checkpoint 机制实现：训练过程持续保存 EPOCH、模型权重、优化器状态、调度器状态至 OBS 或挂载存储路径，故障恢复后加载最新 checkpoint 接续训练 [29]。ModelArts 提供"训练输出"功能与存储挂载功能两种 CKPT 持久化路径，前者支持"预下载至本地目录"在训练启动前自动拉取 checkpoint [29]。万卡场景下 checkpoint 写带宽成为新瓶颈：千亿参数模型单份 CKPT 可达 TB 级，万卡并发写 SFS 易触发元数据服务限速，工程上需配合增量 CKPT、异步保存、分层存储（本地 SSD 缓存 → SFS → OBS 冷备）缓解。

### 4.7 推理部署侧深化

ModelArts 新一代分布式弹性推理平台深度集成自研优化的 vLLM 推理框架，支持一键部署主流开源模型 [5][13]。其核心能力需要展开，因为推理侧是大模型商业落地的"最后一公里"：

- **PD 弹性伸缩**：Prefill（首 token 计算）与 Decode（后续 token 生成）分离部署，Prefill 为计算密集型适合高算力节点、Decode 为内存带宽密集型适合高显存节点，分离后可分别按负载弹性扩缩容，提升资源利用率 [5]。
- **超密部署**：单节点部署多模型实例共享 GPU/NPU，通过细粒度资源切分提升单卡吞吐，适合多租户低 QPS 场景。
- **Token 级快恢**：推理服务故障时，未完成请求的 KV 缓存可迁移至健康实例，从最后一个完成的 token 续推，而非整请求重算，降低长上下文场景的故障恢复成本 [5]。
- **多级流控**：按租户、模型、API key 维度的令牌桶限流与优先级调度，防止突发流量击穿服务。
- **多形态部署**：在线推理（HTTP/gRPC API）、批量推理（异步任务）、边缘推理（IEF 边缘节点下发模型）三形态统一管理 [13]。

推理侧相对训练侧的工程成熟度更高（vLLM 社区生态成熟、P/D 分离已是业界共识），但 ModelArts 推理平台在昇腾 NPU 上的优化深度、与训练侧 MindSpeed-LLM 的训推一体化（权重格式互通、量化一致性）、以及与第三方推理框架（SGLang、TensorRT-LLM）的互操作性，是后续值得跟踪的方向。

---

## 5. 在集群上跑起来：端到端工程实践

本章回答"如何在 ModelArts 集群上实际跑通一个多机多卡大模型训练作业"。综合官方最佳实践 [30][31][32][33] 与昇腾训练镜像制作指南 [34]，完整链路可归纳为七步。

### 5.1 资源准备（VPC / SFS / OBS / SWR / 资源池）

1. **购买服务资源**：创建 VPC 与子网、SFS Turbo 文件系统、OBS 桶、SWR 组织、ECS 调试机 [30]。
2. **分配权限**：为 ModelArts 用户授予 OBS/SFS/SWR 的读写权限。
3. **创建专属资源池**并接入 VPC，选择昇腾规格（如 Atlas 800T A2 8 卡节点、或超节点 Snt9b23 节点）[17]。
4. **挂载 SFS Turbo** 至 ECS，授予 ModelArts 用户读权限；安装配置 obsutil（OBS CLI）[30]。

资源池选择直接决定后续作业形态：公共资源池即开即用但资源争抢；专属资源池物理隔离且可接入用户 VPC 访问 SFS；Lite Cluster 面向需要原生 K8s API 的用户。

### 5.2 镜像构建与上传

ModelArts 提供丰富的 ARM+Ascend 预置镜像，覆盖 PyTorch、MindSpore、MindSpeed-LLM 等场景，命名形如 `pytorch_2.7.1-cann_8.3.rc1-py_3.11-hce_2.0.2509-aarch64-snt9b` [35]。当预置镜像不满足需求时，需基于预置镜像制作自定义镜像：

1. 在能访问 SWR 且联网的 ECS-ARM 机器上拉取基础镜像。
2. 安装额外依赖（如 `pip install -r requirements.txt`）。
3. 升级 CANN 包至与硬件驱动兼容版本（如 cann-toolkit_8.0.run）[34]。
4. `docker push` 至 SWR 组织。

镜像规范须满足自定义镜像规范要求 [31]，否则训练作业可能因环境变量缺失而启动失败。

### 5.3 数据与算法上传

- **数据**：通过 obsutil 上传至 OBS 桶（如 ImageNet21k 数据集上传至 `obs://bucket/imagenet21k_whole/`）[31]。
- **算法**：上传至 SFS Turbo 挂载目录（如 `/home/ma-user/work/`），多机共享同一目录 [31]。

OBS 与 SFS 的取舍：OBS 是对象存储，多机训练时各节点输入通道不共用，需在代码中适配；SFS 是共享文件系统，多机挂载同一目录，编程模型更简单但 IO 性能受网络制约 [34]。

### 5.4 Notebook 代码调试

创建 Notebook 实例（选择与训练目标一致的预置镜像与规格），在 JupyterLab 或通过 VS Code/PyCharm ModelArts 插件远程连接调试训练脚本 [32]。推荐先跑通单机单卡脚本，再切到多机多卡脚本 [31]。Notebook 也支持分布式调测：SDK 会创建一个附属 Notebook 与当前 Notebook 组成 2 节点分布式调试环境 [36]。

### 5.5 创建多机多卡训练作业

控制台创建训练作业时关键配置 [30][31]：

- **创建方式**：自定义算法
- **启动方式**：自定义镜像
- **镜像**：选择上传至 SWR 的自定义镜像
- **资源池**：专属资源池，选择 GPU/NPU 规格
- **计算节点个数**：≥2 即为分布式作业
- **SFS Turbo 挂载**：云上挂载路径 `/home/ma-user/work`
- **自动重启**：开启并设置重启次数（推荐 ≥28，配合断点续训）
- **超节点亲和组实例数**：Snt9b23 场景填写，实例数须为亲和组实例数整数倍 [15]
- **算子重执行**：超节点大模型场景开启 [7]
- **环境变量**：设置 `HCCL_CONNECT_TIMEOUT=7200`、`HCCL_EXEC_TIMEOUT=7200`、`HCCL_IF_BASE_PORT=64321`、`GLOO_SOCKET_IFNAME=eth0`、`HCCL_SOCKET_IFNAME=eth0` 等 [34]

多机多卡启动脚本 `run.sh` 中使用 ModelArts 训练容器预置环境变量 `VC_WORKER_HOSTS`、`VC_WORKER_NUM`、`VC_TASK_INDEX`、`MA_NUM_GPUS` [31]。

### 5.6 分布式训练模式选择

ModelArts 支持两种分布式模式 [37][38]：

| 模式 | 适用 | 优点 | 缺点 |
|---|---|---|---|
| DataParallel (DP) | 单机多卡 | 代码简单，仅改一行 | 通信瓶颈、GPU 负载不均衡 |
| DistributedDataParallel (DDP) | 多机多卡 | 通信更快、负载均衡、运行速度快 | 代码改造点多 |

昇腾 NPU 场景下，Ascend-Powered-Engine 框架提供三种启动方式：基于 `RANK_TABLE_FILE` 默认启动、`MA_RUN_METHOD=torchrun`、`MA_RUN_METHOD=msrun` [26]。系统自动生成 `jobstart_hccl.json` 描述集群拓扑，预设镜像自动解析，自定义镜像需训练代码自行读取解析 [26]。

### 5.7 ranktable 动态路由加速

ranktable 路由规划是面向大模型分布式并行训练的通信优化能力，根据实际交换机拓扑为节点间通信路径进行网络路由亲和规划，提升节点间通信速度 [18]。使用约束：

- Volcano 插件 1.10.12 或以上版本。
- 训练作业至少 3 个任务节点，否则 ranktable 路由被跳过。
- 大模型场景（512 卡以上）加速效果更显著。
- 必须使用 `torch.distributed.launch/run` 启动脚本。
- 训练脚本须将 `NODE_RANK` 设为环境变量 `RANK_AFTER_ACC`。

### 5.8 超节点亲和组

超节点亲和特性是一种调度策略，通过对 AI 训练任务编排分组匹配计算资源的硬件组网形态，充分利用超节点的高带宽低延迟特性 [15]。核心思想是将训练过程中对带宽要求高的卡放到同一亲和组内：模型并行中的 allreduce 通信与 MoE 专家并行中的 all-to-all 通信对卡间互联带宽要求极高，受限于硬件组网，这些通信开销往往成为瓶颈；超平面全互联组网可极大提升通信效率，从而允许更大范围调整模型并行或 MoE 专家并行参数。配置时填写"超节点亲和组实例数"=2 即可，"实例数"必须设为亲和组实例数整数倍 [15]。

### 5.9 故障恢复与断点续训实战

实战配置要点 [27][28][29]：

1. 训练脚本中实现 checkpoint 保存与 reload 逻辑，定期保存网络权重、优化器状态、epoch。
2. 创建作业时开启"自动重启"，设置重启次数（如 28 次）。
3. 超节点场景额外开启"算子重执行"。
4. 使用"训练输出"功能或存储挂载持久化 checkpoint 至 OBS/SFS。
5. 训练脚本支持可重入：通过 `MA_PROC_START_CNT` 判断是否原地恢复，跳过数据下载/预处理、删除重建共享内存。
6. 故障恢复后通过作业详情页"故障恢复详情"页签查看启停记录。

LLaMa-Factory 等框架通过 `resume_from_checkpoint` 参数显式指定恢复点，与 ModelArts 训练输出功能协同实现断点续训 [29]。

### 5.10 端到端流程图

```
[1] VPC/SFS/OBS/SWR/资源池准备
        ↓
[2] 自定义镜像构建（基于预置 ARM+Ascend 镜像）
        ↓
[3] 数据上传 OBS + 算法上传 SFS
        ↓
[4] Notebook 单机单卡调试 → 多机多卡脚本适配
        ↓
[5] 创建训练作业（专属资源池 + N 节点 + 自动重启 + 算子重执行 + 亲和组）
        ↓
[6] DDP 启动（RANK_TABLE_FILE / torchrun / msrun）
        ↓
[7] ranktable 动态路由 + 超节点亲和组调度
        ↓
[8] 训练运行（HCCL 通信 + checkpoint 持久化）
        ↓
[9] 故障检测 → 原地恢复 / Job 重调度 / 算子重执行 → 断点续训
        ↓
[10] 训练输出 → 模型注册 → 推理部署（vLLM / 在线/批量/边缘）
```

*图 2. ModelArts 多机多卡训练作业端到端流程（据 [30][31][34] 整理）*

---

## 6. 竞品横向对比

将 ModelArts 置于 MLaaS 主流平台谱系中对比，可厘清其差异定位与改进空间。综合 [1][2][39][40][41] 整理如下。

### 6.1 平台哲学对比

| 维度 | AWS SageMaker | Azure ML | Google Vertex AI | Huawei ModelArts |
|---|---|---|---|---|
| 核心哲学 | All-in-One 工具箱，最广功能面 | 企业治理与混合云，合规优先 | AI-Native 创新，数据到 AI 一体 | 全栈自研软硬协同，昇腾主导 |
| 目标用户 | 工程师，AWS 原生企业 | 大型企业、受监管行业 | 数据原生公司、研究型团队 | 国内政企、智算中心、昇腾生态伙伴 |
| 自研加速器 | Trainium（训练）、Inferentia（推理） | ND A100 v4 VM（NVIDIA） | TPU v5p | Ascend 910B/C、超节点 Snt9b23 |
| 框架支持 | 全主流 + 自研 | 全主流 | 全主流 + JAX | MindSpore/PyTorch/MXNet + torch_npu |
| AutoML | Autopilot（≤250 候选，仅表格） | AutoML（表格/图像/NLP） | AutoML Tables/Image/Text | AutoSearch（SMAC/TPE/Anneal）+ AutoLearning |
| Feature Store | SageMaker Feature Store | Azure ML Feature Store | Vertex AI Feature Store | 无独立产品，数据管理内嵌 |
| Model Registry | SageMaker Model Registry | Azure ML Model Registry | Vertex AI Model Registry | 模型管理（版本/溯源/转换/精度追踪） |
| Pipeline | SageMaker Pipelines | Azure ML Pipelines | Vertex AI Pipelines (Kubeflow) | Workflow（低代码 DAG） |
| MLflow | 原生跟踪服务器 | 原生集成 | Vertex AI Experiments | 无原生支持 |
| 部署形态 | 云/边/端，serverless 推理 | 云/边/端，Arc 混合，机密计算 | 云/边/端 | 云/边/端，vLLM 推理，Token 级快恢 |
| 计费 | 实例小时，Savings Plan 最高 64% off | 仅 VM 费，Reserved 最高 72% off | 节点小时 + TPU 小时，$300 免费额度 | 按需/包年包月，昇腾性价比优势 |
| 市场份额 | 约 34% [2] | 约 29% [2] | 约 22% [2] | 国内市场领先，全球份额有限 |

### 6.2 差异化优势

ModelArts 相对三家美国厂商的差异化优势集中在三点。其一，**软硬全栈协同**：从 Ascend 芯片、CANN、HCCL、MindSpeed 到 ModelArts 平台垂直整合，可在通信库、调度、镜像层面做深度联合优化（如超节点亲和组、ranktable 动态路由、HCCL 算子重执行），这是依赖通用 NVIDIA GPU + NCCL 的 SageMaker/Vertex AI 难以复刻的。其二，**昇腾单位算力成本**：910C 双芯合封 FP16 算力达 780–800 TFLOPS、内存带宽 3.2 TB/s，单位算力成本相较 910B 进一步下降 [8]，配合智算中心集约部署形成价格竞争力。其三，**大模型训练稳定性工程**：多级故障恢复（原地恢复/Job 重调度/算子重执行）+ 0.5% 以下作业失败率 + 万卡 30 天不中断的工程指标 [5]，在长稳训练场景下构成可用性护城河。

### 6.3 差距与短板

差距同样清晰。其一，**生态开放性与可移植性**：ModelArts SDK 仅 Python 且不支持在训练/推理服务内调用 [10]，无原生 MLflow 支持，MoXing/CANN/MindSpeed 与 CUDA/NCCL/Megatron 原生路径割裂；而 SageMaker/Vertex AI/Azure ML 三家均原生支持 MLflow、pipeline 编排虽各 SDK 但相对开放 [1]。其二，**全球可达性与合规覆盖**：SageMaker 与 Azure ML 拥有 FedRAMP High、HITRUST 等 93+ 合规认证 [40]，ModelArts 主要服务国内与部分国际站，合规认证广度受限。其三，**MoE 系统软件成熟度**：当前主流开源 MoE 训练框架（Megatron-Core MoE、Tutel、FasterMoE、ScheMoE）几乎只针对 NVIDIA GPU 优化，在昇腾 NPU 上"表现欠佳"已被学术工作明确指出 [9]；MindSpeed 虽提供昇腾亲和的 MoE 支持，但与 Megatron-Core 生态的互操作与社区贡献广度仍有差距。其四，**开发者体验与文档**：Vertex AI 被指"文档欠缺"[2]，但 SageMaker 与 Azure ML 的文档完备度与社区活跃度仍高于 ModelArts。

### 6.4 选型建议

| 场景 | 推荐平台 | 理由 |
|---|---|---|
| AWS 原生企业、复杂企业 ML 大规模 | SageMaker | 功能最广、MLOps 最成熟、Inferentia3 性价比 |
| Microsoft 生态、受监管行业、混合云 | Azure ML | 治理最强、Arc 边缘、机密计算 |
| Google Cloud、数据原生、研究型、TPU | Vertex AI | BigQuery 一体化、AutoML 最易用、TPU v5p |
| 国内政企、智算中心、昇腾生态、长稳训练 | ModelArts | 软硬协同、单位算力成本、稳定性工程 |

---

## 7. 深入改进路径

用户原始诉求中"当前做的比较粗，如何深入改进"是本研究的核心命题。"粗"体现在：传统深度学习时代的 MoXing/AutoSearch 范式向大模型迁移的过渡未完成、MoE 系统软件在昇腾上的成熟度不足、生态封闭性限制开发者基数、可复现性基线缺失。基于 2025–2026 年学术前沿，提出七个改进方向。

七个方向并非等权投入，需按"预期收益 × 技术可行性 × 战略必要性"排序，避免工程资源错配。改进优先级矩阵如下（**注：预期吞吐收益为借用 NVIDIA 生态学术前沿的迁移估算，未经昇腾 NPU 实测验证；工程投入经 §7.8 接口可用性评估修正**）：

| 方向 | 预期吞吐收益 | 工程投入 | 战略必要性 | 综合优先级 |
|---|---|---|---|---|
| §7.1 MoE 通信-计算细粒度重叠 | 1.5–2×（COMET 实测 [42]） | 高 | 高（MoE 是主流） | P0 |
| §7.2 Attention/MoE 解耦并行映射 | 1.2–1.5×（Parallel Folding [43]） | 中 | 高 | P0 |
| §7.3 异构流水并行 + 动态气泡填充 | 1.2–1.33×（Tessera [44]） | 高 | 中（万卡场景才显著） | P1 |
| §7.4 FP8 + 跨平台内核 | 1.5–2×（依赖 910D 量产 [8]） | 高（受硬件制约） | 高 | P1（受 910D 节奏约束） |
| §7.5 Ulysses 长序列 + 内存优化 | 1.3–1.88×（MegaScale-MoE [46]） | 中 | 中（长上下文场景） | P1 |
| §7.6 系统级 AutoML | 难量化（降人力成本） | 中 | 高（范式迁移） | P2 |
| §7.7 生态开放性 + 可复现基线 | 间接（扩大开发者基数） | 低 | 高（全球化的硬约束） | P0（投入产出比最高） |

排序逻辑：P0 三项（§7.1、§7.2、§7.7）中，前两项是大模型训练效率的即时杠杆且学术证据充分，第三项投入产出比最高且是全球化硬约束；P1 三项收益明确但受硬件节奏或场景普适性制约；P2 一项收益间接但关乎范式迁移。

### 7.1 MoE 通信-计算细粒度重叠

MoE 架构是当前扩展模型规模的主流方向，但 all-to-all 通信开销严重制约训练效率。字节跳动豆包大模型团队提出的 COMET 通信优化系统通过更精准、细粒度的计算-通信重叠技术，在大规模 MoE 模型上达到单层 1.96× 加速、端到端平均 1.71× 效率提升，已应用于万卡级生产集群累计节省数百万 GPU 小时，获 MLSys 2025 高分评审（5/5/5/4）[42]。其关键技术包括：

- **细粒度重叠**：将 MoE 层的前向/反向拆分为独立的计算算子与通信算子，重排序实现通信隐藏于独立计算之内。
- **计算重调度**：动态调整数据块计算顺序，优先计算本地数据块同时异步拉取远程 Token，消除等待延迟。
- **动态负载平衡**：根据 Token 长度 M、并行策略（EP/TP 比例）实时调整线程块分配，预编译多版本计算-通信融合算子实现运行时零开销切换。

ModelArts 改进建议：将 COMET 风格的细粒度重叠下沉到 MindSpeed 与 HCCL 协同层，针对昇腾超平面组网优化 all-toall 调度；MindSpeed 已具备"计算通信并行优化"特性 [20]，但与 COMET 的细粒度算子级重叠仍有距离，可作为下一代特性重点投入。

### 7.2 Attention 与 MoE 解耦的并行映射

Megatron MoE Parallel Folding [43] 提出关键洞察：强制 MoE 层沿用与 Attention 层相同的并行映射是次优的，因为两者计算特征截然不同。该框架提出 5-D 混合并行（TP/EP/CP/DP/PP），核心创新是 MoE Parallel Folding——解耦 Attention 与 MoE 组件的并行映射，配合高效的 token 级 dispatcher（同时支持 token-dropping 与 token-dropless、消除序列长度依赖、允许动态 tensor 形状）。在 Mixtral-8x22B 上达到 49.3% MFU、Qwen2-57B-A14B 上 39.0% MFU（H100 GPU），1024 GPU 仍保持强扩展效率 [43]。

ModelArts 改进建议：MindSpeed-LLM 当前支持 Megatron 全套并行 [20]，但"解耦并行映射"作为高级特性尚未在文档中明确暴露；可将其作为推荐配置项暴露给大模型用户，配合昇腾超节点亲和组实现 Attention 走 TP + MoE 走 EP+TP 的混合策略。

### 7.3 异构流水并行与运行时动态气泡填充

阿里巴巴 Qwen3/Qwen3-Next 生产集群上的 Tessera 框架（OSDI 2026）[44] 解决万亿参数异构 MoE 训练的流水并行难题：现代架构从均匀 Transformer 块演化为 MoE + 不同 attention 变体的异构组合，破坏了现有流水系统的均匀性假设——串行层成本选择的分区在通信与计算重叠后变得不均衡，且 10K+ GPU 规模下 MoE 路由变化引入运行时停顿。Tessera 引入：(1) 为每种层组合合成细粒度交错的 overlap 调度器；(2) 用 profiled post-overlap 成本选择并行执行均衡分区的 overlap-aware 分区器；(3) 用可移动任务填充路由引发空闲槽的动态气泡优化器。在 4096–12288 GPU 上比生产基线提升吞吐 20%–33%，万亿参数模型达 39% MFU [44]。

ModelArts 改进建议：当前 ModelArts 的流水并行主要依赖 MindSpeed 承接的 Megatron 静态调度 [20]，缺乏运行时动态气泡填充能力。可借鉴 Tessera 思路，在 MindSpeed 中引入 overlap-aware 分区器与动态气泡优化器，特别是针对超节点 Snt9b23 的"超平面"网络拓扑定制化。

### 7.4 FP8 低精度训练与跨平台内核

低精度训练是提升算力利用率的关键路径。Megatron Core 已支持 FP8 与 NVFP4 训练 [45]，在 NVIDIA GB300/GB200 上 DeepSeek-V3-685B 达到 1233/1048 TFLOPS/GPU。然而当前昇腾 910B/C 对 FP8 支持有限（910D 预计 2026 年量产才补齐 FP8 [8]），这是相对 NVIDIA Hopper/Blackwell 的硬性差距。

X-MoE [9] 提出面向非 NVIDIA 平台的另一条路径：在 AMD MI250X 上用 padding-free 跨平台内核、redundancy-bypassing dispatch、sequence-sharded MoE block (SSMB) 混合并行，将 DeepSeek 风格 MoE 扩展至 545B 参数 1024 GPU——比现有方法在同硬件预算下可训练模型大 10×。其 SSMB 策略利用 MoE block 所有操作 token-wise 无 inter-token 依赖的特性，将 MoE block 输入序列在 EP ranks 间分片，减少 dispatch/combine 激活显存占用 TP group size 倍 [9]。

ModelArts 改进建议：(1) 加速 910D FP8 量产与 CANN/ATB 的 FP8 算子完备度；(2) 在过渡期借鉴 X-MoE 的跨平台内核思路，针对昇腾 910B/C 开发 padding-free MoE 内核与 SSMB 混合并行，弥补 FP8 缺失下的效率损失；(3) 将 ATB（Ascend Transformer Boost）加速库 [21] 的 FP8 路线图公开化以稳定生态预期。

### 7.5 Ulysses 长序列并行与内存优化

长上下文（128K–1M token）是 2025–2026 年大模型的核心能力方向。MindSpeed 已提供 Prototype 阶段的 Ulysses 长序列并行 [20]，但尚未商用。配合长序列的内存优化方面，MegaScale-MoE [46] 采用选择性激活重物质化（仅在前向保留部分激活、反向重算或重通信获取所需激活），在 holistic 调度下有效隐藏重物质化开销，仅存储一半激活即达到可比性能。在 1440 NVIDIA Hopper GPU 上训练 352B MoE 模型达 1.41M tokens/s，比 Megatron-LM 提升 1.88× [46]。

ModelArts 改进建议：(1) 将 Ulysses 从 Prototype 推向商用，与超节点亲和组协同优化长序列 all-to-all；(2) 在 MindSpeed 中引入选择性激活重物质化与 holistic 调度，MindSpeed 已有"自适应选择重计算"与"内存碎片优化"特性 [20]，需进一步将其整合到端到端 MoE 训练流水线。

### 7.6 系统级 AutoML 与并行策略搜索

当前 ModelArts 的 AutoSearch 仅支持 float 超参的黑盒搜索 [12][24]，无法服务大模型时代的并行策略搜索（TP/EP/CP/DP/PP 维度组合 + 重计算/Offload/FP8 开关）。学术上，MoE Parallel Folding [43] 与 Tessera [44] 已展示"并行策略搜索 + overlap-aware 成本建模"的可行路径：用 profiled post-overlap 成本驱动分区器搜索，而非黑盒采样。

ModelArts 改进建议：将 AutoSearch 从黑盒超参搜索升级为"系统级 AutoML"，集成：(1) 并行策略搜索器（基于小规模 profile 成本预测大规模分区）；(2) overlap-aware 调度器合成；(3) 与 MindSpeed-LLM 的 5-D 并行配置深度耦合。这是从"通用 ML AutoML"到"大模型系统级 AutoML"范式迁移的关键投资。

### 7.7 生态开放性与可复现性基线

生态层面改进虽非纯技术，却是 ModelArts 从"国内可用"走向"全球可选"的硬约束。四项具体建议：

1. **MLflow 原生集成**：SageMaker/Vertex AI/Azure ML 三家均原生支持 MLflow 跟踪 [1]，ModelArts 应提供原生 MLflow tracking server，降低跨平台迁移成本。
2. **SDK 跨环境可用**：当前 ModelArts SDK 不支持在训练作业与推理服务内调用 [10]，应解除这一限制，使训练脚本可直接调用 SDK 管理作业生命周期。
3. **可复现性基线公开**：定期发布 ModelArts 在 MLPerf Training [47] 等公开基准上的成绩与复现脚本，对标 SageMaker HyperPod、Vertex AI 公开基准。当前公开性能数据仍停留在 2019 年 DAWNBench [6]，缺乏大模型时代可复现基线。
4. **开源贡献双向化**：MindSpeed-LLM 与 MindSpeed 已在 GitHub/Gitee/AtomGit 开源 [19][20]，应进一步将 MoE 优化特性（如 COMET 风格细粒度重叠）作为开源贡献回流社区，吸引第三方开发者参与，缓解"昇腾专属"标签带来的封闭印象。

### 7.8 改进路径的昇腾接口可用性前置评估（CRITICAL 边界条件）

上述七方向均借用 NVIDIA 生态学术前沿并主张迁移到昇腾。必须正视的边界条件是：COMET/Tessera/Parallel Folding 等优化的工程实现深度依赖 CUDA/NCCL 的特定语义（COMET 细粒度算子拆分依赖 CUDA Graph、Tessera overlap 调度依赖 NCCL 异步语义、Parallel Folding 的 token-level dispatcher 依赖动态形状内核）。迁移到昇腾并非算法思想平移，而是需在 HCCL/CANN/ATB 上重新发明等价语义。下表对每方向标注昇腾侧接口现状与迁移成本性质，区分"可采纳的算法思想"（低成本）与"需重新发明的系统语义"（高成本）：

| 方向 | 依赖的 NVIDIA 侧语义 | 昇腾侧接口现状 | 迁移性质 | 工程投入修正 |
|---|---|---|---|---|
| §7.1 COMET 细粒度重叠 | CUDA Graph 算子级控制、NCCL 异步通信句柄 | MindSpeed 有"计算通信并行优化"[20] 但未公开 CUDA Graph 等价粒度 | 需重新发明 HCCL 异步语义 | 投入 ×2（原"高"→"极高"） |
| §7.2 Parallel Folding | 动态形状内核、token-level dispatcher | torch_npu 支持动态形状有限，MindSpeed MoE dispatcher 未公开 | 部分需重新发明 | 投入 ×1.5 |
| §7.3 Tessera 动态气泡 | NCCL 异步 overlap、运行时任务迁移 | HCCL overlap 调度未公开运行时任务迁移接口 | 需重新发明 | 投入 ×2 |
| §7.4 FP8 + 跨平台内核 | FP8 Tensor Core、NVFP4 | 910B/C 无 FP8，910D 2026 量产 [8] | 受硬件制约，非软件可解 | 投入不变（等硬件） |
| §7.5 Ulysses + 内存优化 | 长序列 all-toall、选择性重物质化 | MindSpeed Ulysses 已 Prototype [20]、自适应重计算已有 | 算法思想可采纳 | 投入不变 |
| §7.6 系统级 AutoML | profile 成本建模 | 与硬件无关，纯软件 | 算法思想可采纳 | 投入不变 |
| §7.7 生态开放性 | 无硬件依赖 | N/A | 直接可做 | 投入不变 |

**修正结论:** §7.1、§7.3 的工程投入在 V1.0 被低估约 2 倍，因依赖 HCCL 异步语义与运行时任务迁移接口的可用性，而这些接口的公开程度不足。在华为云公开 HCCL/CANN 的细粒度算子控制与异步 overlap 接口文档之前，§7.1、§7.3 应视为"研究阶段"而非"可立即投入"。§7.5、§7.6、§7.7 为低风险可优先推进项。这一边界条件不改变改进方向本身，但改变优先级与投入估算——F1 修复后，§7 优先级矩阵的工程投入列应在 V1.1 修正（见矩阵脚注）。

> **优先级矩阵修正（F1）：** §7.1 工程投入"高"→"极高"，§7.3"高"→"极高"，并标注"依赖 HCCL/CANN 接口公开度"。综合优先级：§7.7、§7.5、§7.6 上调为 P0（低接口依赖），§7.1、§7.3 下调为 P1（接口可用性未验证）。

---

## 8. 讨论

### 8.1 "粗放可用"到"高效精打"的范式跃迁

综合前述分析，ModelArts 当前处于"粗放可用"阶段：万卡集群管理、0.5% 以下作业失败率、30 天不中断训练、万亿参数训练能力 [5] 等指标证明了基础设施层面的工程成熟度。然而向"高效精打"演进——即在 MoE 系统软件成熟度、并行策略搜索自动化、跨平台内核、生态开放性四个维度达到与 SageMaker HyperPod、Megatron-Core 生产部署可比的水平——仍需显著投入。这一跃迁的核心不是再增加一个功能模块，而是范式转换：从"硬件垂直整合驱动"转向"系统软件与生态驱动"，软硬协同的红利在大模型时代更多取决于系统软件对 MoE/长序列/低精度等新工作负载的适配速度，而非单纯的芯片算力指标。

### 8.2 全栈战略的收益与代价再平衡

ModelArts 的全栈自研战略在"卡脖子"背景下具有战略必要性，且在软硬协同优化（HCCL 算子重执行、超节点亲和组、ranktable 动态路由）上已产生独特价值。但学术前沿（COMET [42]、Tessera [44]、MegaScale-MoE [46]、X-MoE [9]）显示，最先进的 MoE 训练系统优化主要诞生于 NVIDIA + Megatron-Core 生态，且越来越多以开源形式回流社区。这意味着"全栈自研"的代价不仅是生态封闭，更是"重复造轮子"的研发效率损失——MindSpeed 需要独立实现 COMET 风格细粒度重叠、Tessera 风格动态气泡填充，而 NVIDIA 生态可直接采纳社区成果。战略再平衡的可行路径是：硬件层（Ascend/CANN/HCCL）保持自研主导，系统软件层（MindSpeed/MoE 优化）采取"自研核心 + 积极采纳社区 + 回流贡献"的混合模式，应用层（MindSpeed-LLM 模型适配）尽量与 Megatron-Core/HF 生态保持接口兼容。

### 8.3 与 AtomGit/Gitee 开源生态的协同

> **利益冲突就近披露：** 本研究的审稿与写作工具 AtomCode 由 AtomGit 出品，本节推荐 AtomGit 作为开源生态主阵地存在潜在正向偏见。读者应独立评估此结论的中立性，并参考文末"利益冲突声明"完整披露。

AtomGit/GitCode 作为开放原子开源基金会主导的"开源+AI"一体化基础设施，提供从云端到本地的多样化算力支持，覆盖 GPU/NPU 及异构算力，面向大模型研发提供 1TB 起步可扩展模型仓库与 Notebook/Space 每月 1000 核时免费算力 [48]。MindSpeed-LLM 已在 AtomGit/GitCode 设立镜像 [49]。这一协同对 ModelArts 生态开放性建设具有战略意义：(1) AtomGit 的中立公益属性可缓解"昇腾专属"封闭印象；(2) 模型仓库与算力调度一体化降低第三方开发者试用门槛；(3) 与 CSDN 等生态伙伴协同的人才培养通道（算力入校、课程进校园）可扩大昇腾开发者基数。建议华为云进一步将 ModelArts 的预置镜像、MindSpeed 训练样例、可复现基线脚本以 AtomGit 为主阵地开放，形成"ModelArts 商用平台 + AtomGit 开源生态"的双轮驱动。**鉴于上述利益冲突，本节结论应被视为建议而非定论，替代方案（如 Gitee 主导、或 Gitee+AtomGit 双平台）的可行性需独立评估。**

### 8.4 风险与不确定性

本研究提出的改进路径存在三方面不确定性。其一，910D FP8 量产时间表与良率（910C 当前良率仅 35%–36% [8]）直接影响 §7.4 改进路径的可行性。其二，MoE 系统软件优化的工程投入规模巨大，COMET/Tessera 等成果背后是字节/阿里万卡级生产集群的工程团队长期投入，华为云能否在 MindSpeed 中等价投入并保持与社区同步是组织层面的挑战。其三，国内智算中心建设节奏与"东数西算"政策导向影响 ModelArts 的市场窗口，改进路径的优先级排序需随政策与市场动态调整。

---

## 9. 局限与未来工作

### 9.1 研究局限

1. **一手学术文献不足**：华为云关于 ModelArts 内部实现的同行评审学术论文在公开索引中稀缺，本研究主要依赖官方技术文档、厂商博客工程文章与开源代码仓库作为一手材料，第三方 MLaaS 对比与学术 MoE/分布式训练文献作为改进路径证据。这一材料结构可能低估了未公开的内部工程实践深度。
2. **性能数据时效性**：公开性能数据最新仅至 2019 年 DAWNBench [6]，缺乏 2024–2026 年大模型时代 ModelArts 在 MLPerf Training [47] 等公开基准上的可复现成绩，§6 与 §7 的定量对比因此受限。
3. **未涵盖推理侧深度**：本研究聚焦训练侧，对 ModelArts 新一代分布式弹性推理平台（vLLM 集成、PD 弹性伸缩、Token 级快恢 [5]）仅作架构性描述，未深入推理侧的连续批处理、KV 缓存管理、投机解码等前沿。
4. **未实测验证**：研究基于文档与代码审阅，未在真实 ModelArts 集群上实测跑通万卡训练作业，§5 工程实践链路的可行性依赖官方文档准确性。

### 9.2 未来工作

1. 在 ModelArts 专属资源池上实测 MindSpeed-LLM 训练 Qwen2-57B-A14B 等 MoE 模型，采集 MFU、通信开销、故障恢复时延等一手指标，与 Megatron-Core + H100 基线对照。
2. 跟踪 910D FP8 量产进度，评估 FP8 训练对 ModelArts 大模型吞吐的定量提升。
3. 深入研究 ModelArts 推理侧（vLLM 集成、PD 弹性伸缩、Token 级快恢）的工程实现与改进路径。
4. 调研 ModelArts 在国内智算中心（北京中关村、上海松江、深圳鹏城、武汉光谷等 [8]）的实际部署案例，补充行业落地一手证据。

---

## 10. 结论

本研究系统梳理了华为云 ModelArts 的业务背景、问题挑战、三层技术架构、关键技术实现、集群端到端工程实践、竞品横向对比与深入改进路径。主要结论如下：

1. ModelArts 采用算力层/AI 平台层/AI 开发工具链层三层架构，全栈自研软硬协同是其核心差异化优势，体现于 HCCL 算子重执行、超节点亲和组、ranktable 动态路由等深度联合优化。
2. 在集群实践层面，ModelArts 已形成从 VPC/SFS/OBS/SWR 资源准备到多机多卡训练作业创建、ranktable 动态路由、超节点亲和组调度、多级故障恢复与断点续训的完整工程链路，支撑万卡级训练与 0.5% 以下作业失败率。
3. 横向对比 SageMaker/Vertex AI/Azure ML，ModelArts 在软硬协同、单位算力成本、长稳训练工程上具备优势，但在生态开放性、全球合规覆盖、MoE 系统软件成熟度、开发者体验上存在差距。
4. 基于 2025–2026 学术前沿（COMET、MoE Parallel Folding、Tessera、MegaScale-MoE、X-MoE、Ulysses），提出七个改进方向：MoE 通信-计算细粒度重叠、Attention/MoE 解耦并行映射、异构流水并行与动态气泡填充、FP8 与跨平台内核、Ulysses 长序列并行与内存优化、系统级 AutoML、生态开放性与可复现性基线。
5. ModelArts 当前处于"粗放可用"阶段，向"高效精打"演进的核心是从"硬件垂直整合驱动"转向"系统软件与生态驱动"的范式转换，全栈战略需在系统软件层采取"自研核心 + 积极采纳社区 + 回流贡献"的混合模式，并以 AtomGit/Gitee 开源生态为开放性建设主阵地。

本研究的价值在于将分散于官方文档、厂商博客、开源仓库、学术前沿的信息整合为一份可操作的技术研究报告，为 ModelArts 的工程实践者、昇腾生态合作伙伴、MLaaS 选型决策者提供参考。研究局限主要来自一手学术文献与可复现基线的缺乏，这正是 §7.7 建议华为云公开可复现性基线的反面印证。

---

## 参考文献

[1] G. Lawton, "Compare Google Vertex AI vs. Amazon SageMaker vs. Azure ML," TechTarget, 2025-03. [Online]. Available: https://www.techtarget.com/searchenterpriseai/tip/Compare-Google-Vertex-AI-vs-Amazon-SageMaker-vs-Azure-ML

[2] Ankur A. Patel, "Azure ML vs Vertex AI vs SageMaker: A Comparison," 2025-02. [Online]. Available: https://www.ankursnewsletter.com/p/azure-ml-vs-vertex-ai-vs-sagemaker

[3] 陈亮, "深度解读华为云 AI 开发平台 ModelArts 技术架构," 华为云社区博客 108339, 2019-07. [Online]. Available: https://bbs.huaweicloud.cn/blogs/108339

[4] 华为, "ModelArts 3.0使能平台，助力AI赋能千行百业," Huawei Tech Publication 87. [Online]. Available: https://www.huawei.com/cn/huaweitech/publication/87/ai-adoption-modelarts

[5] 华为云, "魔坊（ModelArts）模型训推平台 产品介绍," 2026. [Online]. Available: https://support.huaweicloud.com/productdesc-modelarts/modelarts_01_0001.html

[6] 华为云, "斯坦福DAWNBench深度学习训练及推理榜单：华为云ModelArts拿下双料冠军," 2019-03. [Online]. Available: https://www.huaweicloud.com/news/2019/20190322094534931.html

[7] 华为云, "开启超节点HCCL通信算子级重执行机制," ModelArts 用户指南（轻量算力节点）. [Online]. Available: https://support.huaweicloud.com/usermanual-server-modelarts/usermanual-server-0037.html

[8] AI柠檬, "面向AI的华为昇腾NPU参数汇总整理," 2025-05. [Online]. Available: https://blog.ailemon.net/2025/05/24/huawei-ascend-npu-params-for-ai/

[9] X-MoE 团队, "X-MoE: Enabling Scalable Training for Emerging Mixture-of-Experts Architectures on HPC Platforms," arXiv:2508.13337, 2025. [Online]. Available: https://arxiv.org/html/2508.13337v1

[10] 华为云, "SDK简介," ModelArts SDK 参考. [Online]. Available: https://support.huaweicloud.com/sdkreference-modelarts/modelarts_04_0002.html

[11] 华为云, "MoXing Framework功能介绍," ModelArts 开发环境文档. [Online]. Available: https://support.huaweicloud.com/intl/zh-cn/devtool-modelarts/modelarts_11_0001.html

[12] 华为云, "自动模型优化介绍," ModelArts AutoSearch. [Online]. Available: https://support.huaweicloud.com/develop-modelarts/develop-modelarts-0031.html

[13] 华为云, "什么是ModelArts," 产品介绍. [Online]. Available: https://support.huaweicloud.com/intl/zh-cn/productdesc-modelarts/modelarts_01_0001.html

[14] 华为, "Atlas 800T A2 训练服务器," 企业业务产品页. [Online]. Available: https://e.huawei.com/cn/products/computing/ascend/atlas-800t-a2

[15] 华为云, "超节点亲和组实例数配置," ModelArts 用户指南. [Online]. Available: https://support.huaweicloud.com/intl/zh-cn/usermanual-standard-modelarts/develop-modelarts-0011.html

[16] 华为, "Ascend Training Solution 25.3.x 组网指南（Atlas A2训练产品）02," EDOC1100543548, 2026-04. [Online]. Available: https://support.huawei.com/enterprise/zh/doc/EDOC1100543548

[17] 华为, "ModelArts Resource Management," ModelArts 7.2.1-HCS Usage Guide. [Online]. Available: https://support.huawei.com/enterprise/en/doc/EDOC1100521426/814b5f8/modelarts-resource-management

[18] 华为云, "Performing PyTorch NPU Distributed Training In a ModelArts Lite Resource Pool Using Ranktable-based Route Planning," ModelArts User Guide (Lite Cluster). [Online]. Available: https://support.huaweicloud.com/intl/en-us/usermanual-cluster-modelarts/umn-cluster-modelarts-0015.html

[19] Ascend, "MindSpeed-LLM: 基于昇腾生态的大语言模型分布式训练套件," GitHub 仓库. [Online]. Available: https://github.com/Ascend/MindSpeed-LLM

[20] Ascend, "MindSpeed: 针对华为昇腾设备的大模型加速库," GitHub 仓库. [Online]. Available: https://github.com/Ascend/MindSpeed

[21] 昇腾社区, "使用导读 - CANN 商用版 9.0.0 开发文档," 2026. [Online]. Available: https://www.hiascend.com/document/detail/zh/canncommercial/900/index/index.html

[22] 华为云, "走近深度学习，认识MoXing：初识华为云ModelArts的王牌利器," 华为云技术分享, 博客园. [Online]. Available: https://www.cnblogs.com/huaweicloud/p/12016887.html

[23] 华为云, "ModelArts-Lab/docs/moxing_api_doc," GitHub 仓库. [Online]. Available: https://github.com/huaweicloud/ModelArts-Lab/tree/master/docs/moxing_api_doc

[24] 华为云, "创建自动模型优化的训练作业," ModelArts AutoSearch. [Online]. Available: https://support.huaweicloud.com/develop-modelarts/develop-modelarts-0036.html

[25] 华为云, "自动学习简介," ModelArts 用户指南. [Online]. Available: https://support.huaweicloud.com/usermanual-standard-modelarts/exeml-modelarts_0001.html

[26] 华为云, "Model Training - Distributed Model Training," ModelArts 6.7.1-HCS Usage Guide. [Online]. Available: https://support.huaweicloud.com/intl/en-us/develop-modelarts/ModelArts%20Model%20Training-pdf.pdf

[27] 华为云, "训练作业故障恢复," ModelArts 用户指南（控制台）. [Online]. Available: https://support.huaweicloud.com/intl/zh-cn/usermanual-standard-modelarts/develop-modelarts-0019.html

[28] 华为云, "训练作业容错检查," ModelArts 用户指南. [Online]. Available: https://support.huaweicloud.com/usermanual-standard-modelarts/modelarts_trouble_0003.html

[29] 华为云, "设置断点续训练," ModelArts 用户指南. [Online]. Available: https://support.huaweicloud.com/intl/zh-cn/usermanual-standard-modelarts/develop-modelarts-0023.html

[30] 华为云, "Running a Multi-Node Multi-PU Training Job on ModelArts Standard," Best Practices. [Online]. Available: https://support.huaweicloud.com/intl/en-us/bestpractice-modelarts/modelarts_20_2040.html

[31] 华为云, "在ModelArts上运行多机多卡训练作业," 最佳实践. [Online]. Available: https://support.huaweicloud.com/bestpractice-modelarts/modelarts_20_2040.html

[32] 华为云, "分布式训练功能介绍," ModelArts 用户指南. [Online]. Available: https://support.huaweicloud.com/usermanual-standard-modelarts/modelarts-distributed-0001.html

[33] 华为云, "Overview - Distributed Model Training," ModelArts User Guide (Standard). [Online]. Available: https://support.huaweicloud.com/intl/en-us/usermanual-standard-modelarts/modelarts-distributed-0001.html

[34] 华为, "大模型训练镜像制作及上云迁移（OBS）," ModelArts 6.7.1-HCS 使用指南. [Online]. Available: https://support.huawei.com/enterprise/zh/doc/EDOC1100439086/4344b6f1

[35] 华为云, "ModelArts统一镜像列表," ModelArts 用户指南, 2026-06. [Online]. Available: https://support.huaweicloud.com/usermanual-standard-modelarts/docker-modelarts_6022.html

[36] 华为云, "使用SDK调测多机分布式训练作业," ModelArts SDK 参考. [Online]. Available: https://support.huaweicloud.com/sdkreference-modelarts/modelarts-distributed-0005.html

[37] 华为云, "配置算子重执行," ModelArts 用户指南. [Online]. Available: https://support.huaweicloud.com/usermanual-standard-modelarts/develop-modelarts-14191.html

[38] 华为云, "ModelArts分布式训练," 专题. [Online]. Available: https://www.huaweicloud.com/special/info-modelarts-distributedtraining.html

[39] baris_kaplan, "Cloud AI Smackdown: Huawei Cloud ModelArts vs AWS SageMaker," Medium Huawei Developers, 2025-06. [Online]. Available: https://medium.com/huawei-developers/cloud-ai-smackdown-huawei-cloud-modelarts-vs-aws-sagemaker-67e30dcab14a

[40] Articsledge, "AWS SageMaker vs Azure ML vs Google Vertex AI," 2025-11. [Online]. Available: https://www.articsledge.com/post/machine-learning-platforms-comparison-azure-ai-vs-aws-sagemaker-vs-google-vertex-ai

[41] beneficial.cloud, "MLOps Platform Comparison 2026: AWS vs Vertex vs Azure," 2025-12. [Online]. Available: https://beneficial.cloud/mlops-platform-comparison-2026

[42] 字节跳动 Seed, "COMET: MoE 通信优化技术开源，已部署万卡级集群节省数百万 GPU 小时," 2025. [Online]. Available: https://seed.bytedance.com/zh/blog/comet-has-been-deployed-in-large-scale-clusters-saving-millions-of-gpu-hours-moe-communication-optimization-technology-comet-is-now-open-source

[43] MoE Parallel Folding 团队, "MoE Parallel Folding: Heterogeneous Parallelism Mappings for Efficient Large-Scale MoE Model Training with Megatron Core," arXiv:2504.14960, 2025. [Online]. Available: https://arxiv.org/html/2504.14960v2

[44] W. Hu et al., "Tessera: A Holistic Pipeline Parallelism Framework for Trillion-Parameter Heterogeneous MoE Training," USENIX OSDI 2026. [Online]. Available: https://www.usenix.org/conference/osdi26/presentation/hu-weifang

[45] Z. Yan et al., "Scalable Training of Mixture-of-Experts Models with Megatron Core," arXiv:2603.07685, 2026. [Online]. Available: https://arxiv.org/html/2603.07685

[46] MegaScale-MoE 团队, "MegaScale-MoE: Large-Scale Communication-Efficient Training of Mixture-of-Experts Models in Production," arXiv:2505.11432, 2025. [Online]. Available: https://arxiv.org/html/2505.11432v1

[47] MLCommons, "MLPerf Training Benchmark," 2024. [Online]. Available: https://mlcommons.org/benchmarks/training/

[48] 开放原子开源基金会, "新一代AtomGit平台正式上线，打造'开源+AI'一体化基础设施," 2025-11. [Online]. Available: https://www.openatom.org/journalism/detail/Q5U5ZPm9veBs

[49] Ascend, "MindSpeed-LLM/docs/pytorch/install_guide.md," AtomGit/GitCode 镜像. [Online]. Available: https://gitcode.com/Ascend/MindSpeed-LLM/blob/2.3.0/docs/pytorch/install_guide.md

---

## AI 使用声明

本报告由 AtomCode（GLM-5.2 模型，AtomGit 出品）作为研究助手协助完成。AI 工具的具体使用方式与边界如下：

- **文献检索**：通过 web_search / web_fetch 工具检索华为云官方文档、InfoQ/华为云社区博客、GitHub/Gitee/AtomGit 开源仓库、arXiv/USENIX/OpenReview 学术论文、第三方 MLaaS 对比文章，作为研究素材来源。
- **内容撰写**：由 AI 在用户给定研究框架（业务背景、问题挑战、技术方案、技术架构、具体实现、集群实践、改进路径）下撰写全文初稿，并完成章节组织、表格整理、流程图绘制。
- **引用核实**：所有参考文献均来自实际检索到的公开网页，URL 已列出；但 AI 未通过 DOI 系统逐一交叉验证每条引用的元数据准确性，读者引用时建议复核。
- **未参与事项**：AI 未在真实 ModelArts 集群上执行任何训练作业或性能测试；§5 工程实践链路与 §7 改进路径的可行性基于文档审阅与学术前沿类比，未经实测验证（详见 §9.1 局限 4）。
- **潜在偏差**：一手材料中华为云官方文档与博客占比较高，可能存在对平台能力的乐观描述；改进路径证据主要来自 NVIDIA 生态学术前沿，迁移到昇腾生态的可行性与定量收益需进一步工程验证。

本报告遵循"AI 辅助研究、人类主导判断"的原则，所有结论与改进建议的最终责任由研究报告署名方承担。读者在据此进行工程决策或学术引用时，应结合自身环境实测验证。

---

## 数据可用性声明

本研究为基于公开网络资料的文献综述与技术分析，未生成原始实验数据。所有引用来源已在参考文献部分完整列出 URL，可通过公开网络访问复核。研究过程中产生的配置记录文件（`config.md`）与本报告 Markdown 源文件（`modelarts-research-report.md`）保存在工作目录 `C:\Users\ubuntu\Documents\claude-books\08-Infra\modelarts\`。

## 伦理声明

本研究不涉及人类受试者、敏感个人数据或动物实验。所引用的华为云、昇腾、MindSpeed 等产品名称与商标版权归各自所有者所有，本研究仅作技术分析与学术讨论用途，不构成商业宣传或产品担保。

## 作者贡献（CRediT）

本报告由 AtomCode（GLM-5.2）作为单一研究助手完成，无人类合作作者。CRediT 角色对应：

- Conceptualization（概念化）：AI 根据用户给定框架完成
- Methodology（方法论）：AI 设计研究流程与章节结构
- Investigation（调查）：AI 通过 web 检索工具完成文献收集
- Writing – original draft（初稿撰写）：AI 完成
- Writing – review & editing（审阅编辑）：AI 自审，未经人类编辑
- Visualization（可视化）：AI 绘制架构图与流程图（ASCII 形式）

## 利益冲突声明

AtomCode 由 AtomGit 出品，AtomGit/GitCode 是本研究 §8.3 讨论的 ModelArts 开源生态协同对象之一。这一关联可能在 §8.3 的讨论中存在潜在正向偏见。读者在参考该节结论时应知晓此利益关联，并独立评估 AtomGit 作为 ModelArts 开源生态主阵地的中立性。

## 资金致谢

本研究未获得任何外部资金支持。研究工具（AtomCode AI 助手）由 AtomGit 提供。

---

*报告版本：V1.0 | 完成日期：2026-07-03 | 字数：约 14000 CJK 字符*

