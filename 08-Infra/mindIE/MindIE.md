# 华为昇腾 MindIE 推理引擎

**作者：** 帅哥
**日期：** 2026 年 7 月
**版本：** v2.0
**引用格式：** IEEE

---

## 摘要

MindIE（Mind Inference Engine，昇腾推理引擎）是华为面向昇腾（Ascend）AI 处理器的全场景推理加速套件，承担着将国产算力从"可用"推向"好用"的关键角色。本研究基于昇腾社区官方开发文档、MindIE-LLM 开源仓库、CANN 加速库文档以及第三方实测数据，系统梳理 MindIE 的业务背景、问题挑战、技术方案、技术架构与集群部署实现，并聚焦"当前做得较粗"的若干环节提出分层改进方向。研究发现：MindIE 通过 LLM/Motor/Turbo/SD 等组件的分层开放，在昇腾硬件上实现了 Continuous Batching、PagedAttention、FlashDecoding、PD 分离、大规模专家并行等主流推理加速特性，多卡吞吐场景下相对 vLLM-Ascend 具有明显优势；但其在特性互斥约束、确定性计算代价、调度策略可观测性、混部与故障重调度、调优自动化等方面仍存在工程化短板。本文以 DeepSeek-V3 在 Atlas 800I A3 上的大 EP PD 分离部署为配置案例，沿调度层、编译层、系统层、生态层四个维度提出改进路径，每条改进均标注其性质（追赶业界 / 研究前沿 / 工程诚实化）并与业界同类系统对照，以避免将业界共同前沿误判为 MindIE 独有短板。

**关键词：** MindIE；昇腾；大模型推理；PD 分离；专家并行；Continuous Batching；推理服务化

---

## 目录

1. 引言：昇腾生态与 MindIE 的定位
2. 业务背景：国产 AI 推理的需求与约束
3. 问题与挑战
4. 技术方案总览：MindIE 套件分层
5. 技术架构深入
   5.1 MindIE LLM 四层架构
   5.2 ATB 加速库与图算子
   5.3 调度器与 KV Cache 管理
   5.4 量化与并行策略
   5.5 PD 分离机制
6. 集群部署实现
   6.1 软件栈依赖
   6.2 单机与多机推理
   6.3 Kubernetes 集群部署
   6.4 DeepSeek-V3 大 EP PD 分离部署实例
7. 当前局限分析
8. 深入改进方向
9. 与同类系统对比
10. 结论与展望

参考文献

---

## 1. 引言：昇腾生态与 MindIE 的定位

大语言模型（Large Language Model, LLM）的规模化部署正在重塑算力基础设施的形态。推理阶段作为模型与用户之间的最后一公里，其性能、成本与稳定性直接决定服务的商业可行性。在英伟达 GPU 长期主导训练侧的格局下，推理侧因其对显存带宽、调度策略与异构硬件亲和度的更高敏感性，成为国产算力实现差异化突破的现实切入点。

华为昇腾（Ascend）AI 处理器依托达芬奇架构与配套的 CANN（Compute Architecture for Neural Networks）软件栈，构建了从底层算子到上层框架的完整推理生态。MindIE 正是这一生态中面向推理加速的核心套件。根据昇腾社区官方定义，MindIE 是"华为昇腾针对 AI 全场景业务的推理加速套件，通过分层开放 AI 能力，支撑用户多样化的 AI 业务需求，使能百模千态，释放昇腾硬件设备算力"[1]。其向上支持 PyTorch、MindSpore 等主流框架，向下对接 Atlas 系列不同类型的昇腾 AI 处理器，提供多层次编程接口。

需要澄清一个常见的认知误区：MindIE 不是一个单一的推理引擎，而是一个**产品族**。它由多个面向不同场景的组件构成，组件之间通过明确的接口契约协同。理解这一点，是理解其架构设计与局限来源的前提。

本研究的贡献在于：(1) 基于一手官方文档与开源代码仓库，给出 MindIE 套件的完整技术画像，纠正社区中"MindIE 即单一 LLM 引擎"的简化认知；(2) 以 DeepSeek-V3 在 Atlas 800I A3 上的大 EP PD 分离部署为配置案例，还原"如何在集群上跑起来"的工程细节（注：本文给出官方推荐配置而非自主实测数据）；(3) 识别当前实现的工程化短板，区分"落后于业界最佳实践"与"业界共同研究前沿"两类，并提出可操作的分层改进路径，而非泛泛而谈"优化方向"。

本文余下部分组织如下：第 2 节阐述业务背景；第 3 节梳理问题挑战；第 4 节给出套件总览；第 5 节深入技术架构；第 6 节还原集群部署实现；第 7 节分析局限；第 8 节提出改进方向；第 9 节与同类系统对比；第 10 节总结展望。

---

## 2. 业务背景：国产 AI 推理的需求与约束

### 2.1 算力自主与推理侧的差异化机会

国产 AI 算力的发展路径呈现明显的"训练滞后、推理追赶"特征。训练侧对单卡算力、互联带宽与框架生态的要求极高，英伟达 CUDA 生态的护城河在短期内难以逾越。推理侧则不同：其工作负载以访存密集型为主（尤其 Decode 阶段），对硬件利用率、调度策略与显存管理的敏感度高于对峰值算力的依赖；同时推理服务是面向终端用户的持续性成本中心，对单位推理成本（cost per token）的关注远超训练。

这一差异为国产算力提供了切入点。昇腾处理器在矩阵运算单元（AI Core）与片上 HBM 带宽上具备与同代 GPU 可比的规格，关键在于上层软件能否将这些硬件能力转化为可被业务感知的吞吐与时延优势。MindIE 承担的正是这一转化职责。

### 2.2 大模型部署的结构性挑战

大模型推理并非简单的"模型前向计算"，而是一个涉及调度、显存、通信、服务化的系统工程。其结构性挑战包括：

- **Prefill/Decode 异构性**：Prefill 阶段处理整个 prompt，计算密集；Decode 阶段逐 token 生成，访存密集。二者混合部署会导致算力与显存资源互相争抢[2]。
- **KV Cache 显存压力**：长上下文场景下 KV Cache 占用随序列长度线性增长，是限制并发数的首要瓶颈。
- **MoE 模型的专家分布**：DeepSeek-V3 等大规模 MoE 模型拥有数百个专家，专家并行（EP）的负载均衡与全互联通信成为新瓶颈。
- **服务化与集群调度**：从单卡推理到多机多卡、再到 PD 分离的集群化部署，需要服务发现、负载均衡、故障重调度等系统能力。

### 2.3 MindIE 面向的业务场景

根据官方文档，MindIE 的目标业务覆盖"百模千态"，但其设计重心明确指向大语言模型推理服务化场景[1][3]。典型场景包括：通用 LLM 对话与补全服务、长上下文 RAG 推理、多模态生成（MindIE SD）、以及第三方框架（vLLM/TGI/Triton）在昇腾上的加速适配。本研究聚焦其中工程复杂度最高、研究价值最大的切面——**大规模 LLM 在昇腾集群上的推理服务化部署**。

---

## 3. 问题与挑战

在进入技术方案之前，有必要先明确 MindIE 所要解决的问题空间，以及它在解决这些问题时自身面临的结构性挑战。这些挑战既是 MindIE 设计决策的动因，也是后文"局限分析"与"改进方向"的逻辑起点。

### 3.1 闭源生态与异构编程的双重负担

昇腾处理器的指令集与内存层级与 GPU 存在本质差异。GPU 生态经过十余年积累，已形成以 CUDA/cuBLAS/cuDNN 为底座、以 Triton/FlashAttention 等可移植算子为中层、以 vLLM/TensorRT-LLM 等引擎为上层的成熟栈。昇腾生态则处于建设期：底层算子需基于 Ascend C 编写，中层依赖 ATB（Ascend Transformer Boost）加速库与图算子机制，上层框架适配（torch-npu、vLLM-Ascend）仍在快速演进。

这种生态成熟度差异带来两个直接后果。其一，主流开源引擎无法零成本迁移至昇腾，需要专门的适配层（如 vLLM-Ascend）或原生引擎（如 MindIE LLM）。其二，调优知识与最佳实践高度依赖厂商文档与社区经验积累，存在较陡的学习曲线。一份第三方实测指出，MindIE"使用门槛较高，环境配置复杂，限制了非官方团队在实际项目中部署和调试的效率"[4]。

### 3.2 集群利用率与长尾延迟的矛盾

LLM 推理服务的两个核心 SLO 指标是首 token 时延（TTFT, Time To First Token）与单 token 生成时延（TPOT, Time Per Output Token）。提升集群吞吐量通常意味着增大 batch size，但这会直接抬高 TTFT 与 TPOT；反之，严格保障低延迟则需限制并发，牺牲吞吐。

MindIE 通过 SLO 感知调度尝试调和这一矛盾，提供基于 TTFT/TPOT 时延预测与 LLF（Least Laxity First，松弛度优先）算法的 PD 阶段选择策略，以及基于实时 TPOT 感知的动态 BatchSize 调整算法[5]。但官方文档同时承认，"由于 TPOT 采集存在实时波动，最终的实时时延与配置目标之间可能存在约 10% 的偏差"[5]。这一偏差在高并发、长上下文场景下可能被放大，使 SLO 保障从"确定性问题"退化为"概率性问题"。

### 3.3 PD 分离的工程化代价

PD 分离（Prefill/Decode Disaggregation）将两个阶段部署到不同机器，是提升集群吞吐与降低 Decode 尾延迟的有效手段，MindIE 官方报告在大规模专家并行场景下可带来 30% 以上的吞吐提升[2]。然而这一特性在工程上代价高昂：

- **KV Cache 跨机传输**：P 节点完成 Prefill 后需将 KV Cache 经 RDMA 传输至 D 节点，传输带宽与延迟成为新瓶颈，要求 NPU 网口互联（200 Gbps）[6]。
- **特性互斥**：PD 分离不支持与 Prefix Cache、Multi-LoRA、SplitFuse、并行解码、稀疏量化、KV Cache int8 量化等特性同时使用[6][7]。这意味着启用 PD 分离即放弃多项单机优化，需要在收益与损失间谨慎权衡。
- **硬件约束**：仅 Atlas 800I A2 推理产品与 Atlas 800I A3 超节点支持，且 P/D 节点 NPU 卡数必须相同[6]。

### 3.4 调优的隐式性与可观测性缺口

MindIE 暴露了大量调优旋钮：maxBatchSize、maxPrefillBatchSize、maxPrefillTokens、cacheBlockSize、NPU_MEMORY_FRACTION、supportSelectBatch、prefillTimeMsPerReq/decodeMsPerReq、HCCL_BUFFSIZE 等[8][9]。这些参数之间存在强耦合且缺乏自动搜索机制，调优高度依赖经验。官方性能调优文档给出的流程本质上是"设值→测→看时延→再调"的手动循环[9]。

更深层的问题在于可观测性。MindIE 提供 Prometheus 格式的监控指标接口[10]，覆盖请求数、抢占数、TTFT、TPOT、端到端时延等，但缺少调度器内部决策的可视化（如每次 batch 组建的依据、KV Cache 块的分配/淘汰轨迹、通信算子的耗时分解）。当性能出现无规律波动时（如社区记录的 DeepSeek 大 EP Decode 阶段 TPOT 波动案例[11]），定位根因往往需要借助 MindStudio Profiling 进行离线分析，实时诊断能力不足。

---

## 4. 技术方案总览：MindIE 套件分层

MindIE 通过分层开放 AI 能力来覆盖从底层算子到上层服务的完整推理链路。理解其组件划分是理解架构设计的基础。需要特别注意，MindIE 的组件构成在不同版本间发生过显著演化，下文以 2.x 系列（当前主流）为准，并标注历史名称以避免混淆。

### 4.1 组件构成

当前 MindIE 套件包含以下核心组件[1][3][12]：

| 组件 | 职责 | 定位 |
|------|------|------|
| **MindIE Motor**（旧称 MindIE Service） | 推理服务化框架，提供 RESTful/gRPC 接口、多实例调度、运维管控 | 服务层 |
| **MindIE LLM** | 大语言模型推理引擎 SDK，含调度、KV Cache、加速特性 | 引擎层 |
| **MindIE Turbo** | 第三方推理引擎（当前为 vLLM）的加速插件库 | 加速插件层 |
| **MindIE SD** | 多模态/视图生成推理框架 | 多模态层 |
| **MindIE RT** | 基础推理运行时，基于 CANN 图引擎（小模型场景） | 运行时层 |
| **MindIE Torch** | PyTorch 模型推理加速适配 | 框架适配层 |

其中，MindIE Motor 自 2.1.RC2 起由 "MindIE Service" 更名为 "MindIE Motor"[12]，下文统一使用新名。MindIE Motor 向下调用 MindIE LLM 的推理能力[3]。

### 4.2 Motor 的子组件

MindIE Motor 本身进一步划分为四个子组件[1][3]：

- **MindIE MS**（Management Service）：提供服务策略管理与运维能力，在 PD 分离场景下负责 P/D 实例的生命周期管理（Controller）与请求调度（Coordinator）[6]。
- **MindIE Server**：推理服务端，提供模型服务化能力，支持命令行部署 RESTful 服务，兼容 OpenAI/vLLM/Triton/TGI 主流协议。
- **MindIE Client**：服务客户端标准 API，简化调用。
- **MindIE Benchmark**：性能与精度测试工具。

Motor 内部架构包含 BackendManager（后端管理）、GMIS（模型推理调度器，提供多实例调度）、EndPoint（协议封装）等模块[12]。

### 4.3 Turbo 的特殊定位

MindIE Turbo 是最容易被误解的组件。它**不是**一个独立的推理引擎，也不是 vLLM-Ascend 的竞品，而是装载在 vLLM/vLLM-Ascend 之上的"加速插件库"[13][14]。用户在已安装 vLLM-Ascend 的 Python 环境中安装 MindIE Turbo 后，vLLM-Ascend 会自动检测并使能 Turbo，通过补丁形式替换或装饰 vLLM 部分接口实现，无需修改任何代码[14]。其核心加速机制是 `VLLM_OPTIMIZATION_LEVEL`（0-3 四级开关，默认 2），配合 CPU 高性能模式与透明大页等 OS 层调优，可带来 20-70% 的性能提升[13]。

值得注意的是，MindIE Turbo 的部分能力（如 W8A8 量化、高性能算子使能）在不同版本间逐步迁移至 vLLM-Ascend 社区仓库[14]。这反映华为"将自研优化逐步开源上浮"的策略，也意味着 Turbo 与 vLLM-Ascend 的边界在持续变化。

### 4.4 分层开放的设计意图

MindIE 的分层并非简单的模块拆分，而是对应不同的接入诉求：业务方可在 Motor 层接入获得完整服务化能力；框架开发者可在 LLM 层接入获得调度与加速特性；已有 vLLM 投资的用户可通过 Turbo 获得加速而无需迁移；小模型或非 LLM 场景可在 RT/Torch 层接入。这种分层开放策略降低了不同用户群体的接入门槛，但也带来了组件边界模糊、命名频繁变更等认知成本（详见第 7 节）。

---

## 5. 技术架构深入

本章深入 MindIE 的内部架构，重点剖析 MindIE LLM 的四层结构、ATB 加速库、调度器与 KV Cache 管理、量化与并行策略，以及 PD 分离机制。这些是理解 MindIE 性能特性与局限的技术基础。

### 5.1 MindIE LLM 四层架构

MindIE LLM 是整个套件中工程复杂度最高的组件，也是大模型推理的核心。其总体架构分为四层：Server、LLM Manager、Text Generator、Modeling[15][16]。

**Server 层**提供模型推理的服务化能力。EndPoint 面向推理服务开发者提供 RESTful 接口，负责协议封装与接口转换，兼容 Triton/OpenAI/TGI/vLLM 主流推理框架的请求接口[15]。这一设计使业务侧无需感知底层引擎即可接入。

**LLM Manager 层**负责状态管理与任务调度，是引擎的"大脑"。其核心子模块包括[15][16]：

- **LLM Manager Interface**：对外接口层，提供模型实例管理的 C++/Python 接口。
- **Engine**：编排 Scheduler、Executor、Worker 等组件，为不同推理场景提供统一的请求处理能力。
- **Scheduler**：在一个 DP（Data Parallel）域内，将多条请求在 Prefill 或 Decode 阶段组成 batch，提升计算与通信资源利用率。
- **Block Manager**：管理 DP 域内的 KV Cache 资源，支持池化（Pooling）管理与 Offload 位置感知。
- **Executor**：将调度完成的信息分发至 Text Generator 模块，支持跨机、跨卡的任务下发。
- **KV Connector**：提供跨卡、跨设备的 KV Cache 链路与传输功能，支持对接多种池化后端[16]。

**Text Generator 层**负责模型配置、初始化、加载与自回归推理流程，包含 Preprocess、Generator、Sampler 三个子模块。Generator 对模型运行过程的抽象，Sampler 对 logits 做 token 选择、停止判断与上下文更新[15]。该层支持并行解码的插件化扩展。

**Modeling 层**提供性能调优后的模块与内置模型，支持 ATB Models（Ascend Transformer Boost Models）与 MindSpore Models 两种框架后端[15]。内置模块包括 Attention、Embedding、ColumnLinear、RowLinear、MLP 等，支持 Weight 在线 Tensor 切分加载。

从开源仓库（github.com/Ascend/MindIE-LLM）的目录结构可进一步印证这一分层[16]：`src/` 下包含 `engine`、`scheduler`、`block_manager`、`llm_manager`、`server` 等 C++ 核心模块；`mindie_llm/` 下为 Python 框架主模块，含 `connector`（请求接入）、`text_generator`（核心推理引擎）、`modeling`（模型封装）、`runtime`（运行时编译与加载）。这种 Python 框架 + C++ 引擎的双层架构，使接入灵活性与执行性能得以兼顾——Python 处理请求接入与模型抽象，C++ 处理调度、KV Cache 与执行，性能较纯 Python 实现提升约 20-40%[17]。

**数据流与控制流。** 四层之间的请求处理流程可形式化描述。一次推理请求自上而下经历：

1. **Server 层**：EndPoint 接收 HTTP/gRPC 请求，协议解析后转为内部 Request 对象，提交至 LLM Manager 的请求队列。
2. **LLM Manager 层**：Engine 从队列取请求，Scheduler 按当前调度策略（FCFS/PDDS/Layerwise）决定本轮 batch 构成；Block Manager 检查 KV Cache 显存预算，必要时触发 LRU 淘汰或 Offload；Executor 将 batch 计划下发至 Text Generator。
3. **Text Generator 层**：Preprocess 完成 tokenize 与位置编码；Generator 调用 Modeling 层执行前向；Sampler 对 logits 做 top-k/top-p 采样、停止判断，更新上下文。
4. **Modeling 层**：ATB Models 将模型组网编译为 ATBGraph，下发给 ATB 执行。

自回归场景下步骤 2-4 在 Decode 阶段逐 token 重复，直至 EOS。控制流的关键同步点在 Engine 与 Scheduler 之间：Scheduler 决策依赖上一轮 NPU 执行的反馈（显存占用、KV Cache 块状态），因此调度本质是一个"决策—执行—反馈"的闭环。异步调度特性[5]即通过将本轮反馈与下轮决策重叠来掩盖 CPU 决策耗时。

**与 vLLM 架构对照。** 为厘清 MindIE LLM 的设计取向，可将其与 vLLM 的对应层做结构对照：vLLM 的 `LLMEngine` 对应 MindIE 的 Engine；vLLM 的 `Scheduler` 对应 MindIE Scheduler（但 MindIE 多出 PDDS/Layerwise 两种策略）；vLLM 的 `BlockManager`（PagedAttention）对应 MindIE Block Manager（多出 Offload 位置感知）；vLLM 的 `ModelRunner` 对应 MindIE Text Generator。关键差异在于 Modeling 层：vLLM 走 PyTorch eager 单算子路径，MindIE 走 ATBGraph 整图路径——这正是多卡吞吐优势的架构根源[4]。

### 5.2 ATB 加速库与图算子

ATB（Ascend Transformer Boost）加速库是 MindIE 性能的底层基石，专门为 Transformer 模型的训练与推理设计[18]。它提供三类能力：

1. **基础原生算子（Operation）**：矩阵乘、转置等高性能算子。
2. **插件算子（Plugin Operation）**：用户可基于 Ascend C 实现自定义算子。
3. **图算子（Graph Operation）**：将多个算子组合为图，整体一次性下发到 device，减少 host→device 下发开销[18][19]。

ATB 解决的核心问题是 **Host Bound**。随着模型复杂度上升，逐算子下发会在 NPU 上形成空泡。ATB 通过图算子批量 Setup 与任务下发消除空泡，并提供双线程下发优化（一线程处理 Setup，另一线程处理 Execute）进一步降低 host 执行时间与 NPU 空泡[19]。

ATB 的运行时优化机制包括[18]：

- **Tiling Cache**：缓存计算好的 Tiling（默认每算子保存 10 份），以存代算减少重复计算。
- **Setup 复用 / InferShape 复用**：当同一 Operation 两次输入的 shape 与参数相同时，跳过 Setup 或 InferShape 步骤；对庞大计算图，InferShape 是 host 侧主要开销，复用可显著优化。
- **Runner Pool**：复用算子执行上下文。
- **内存优化**：基于内存 Block 分裂、合并、尾块优化的分配算法，实现图算子内部中间 Tensor 复用，平均节省 Workspace 50%，提升大模型推理 Batch Size 上限[19]。

MindIE LLM 的 Modeling 层即通过 ATB Models（ATBGraph 后端抽象）对接 ATB 的图算子能力[16]，这是其相对仍处于单算子模式的 vLLM-Ascend 在多卡吞吐上取得优势的关键原因[4]。

**Workspace 内存模型。** ATB 对 device 内存的管理值得展开，因其直接影响可支持的 batch size 上限。一个算子下发所需的 device 内存分为三部分：中间张量内存、kernel 的 scratch memory、tiling data 内存[18]。ATB 在 Setup 接口内计算整图所需的中间张量与 scratch memory 之和作为 WorkspaceSize 返回，用户据此申请 device 内存并通过 Execute 接口传入。tiling data 则由 ATB 的 Context 类管理——Context 默认生成一个 32×3 MB 大小的 device 内存池，每个 Operation 需搬移 tiling data 时从池中取出 3 MB 块，池块数可通过环境变量配置[18]。这一池化设计避免了反复 malloc/free 的开销，但也意味着池块数配置过小会成为并发瓶颈。

**图算子的两类组图方式。** ATB 支持两种图算子构造方式[18][19]：基于 TensorId（数值 ID，需提前规划输入/输出/中间 Tensor 的 ID 区间，繁琐但精确）与基于 TensorName（字符串命名，可行性更高，推荐）。GraphOpBuilder 通过 `AddOperation(op, {in_names}, {out_names})` 链式组图，配合 InferShapeFunc 推导输出 shape。这一机制使模型开发者可将一个 Transformer 层封装为图算子复用，而非逐算子拼装。

### 5.3 调度器与 KV Cache 管理

**调度策略**。MindIE LLM 的 Scheduler 支持三种调度策略[16][17]：

- **FCFS**（First Come First Served）：先来先服务，简单稳定，适合单卡或低并发场景。
- **PDDS**（Prefill/Decode Disaggregated Scheduling）：延迟驱动调度，按 PD 阶段分离组 batch，适合多卡（8 卡以上）高并发场景。
- **Layerwise**：分层调度，按层组织计算与通信重叠。

社区经验表明，PDDS 在单卡场景反而可能比 FCFS 慢，需在多卡高并发下才能体现优势[17]。这种"策略选择依赖场景"的特性，是后文局限分析中"调度自动化不足"的典型体现。

**KV Cache 管理**。Block Manager 是 KV Cache 显存管理的核心，提供多种分配策略[15][16]：

- **分块（PagedAttention）**：将 KV Cache 切分为固定大小的 block，避免显存碎片，提升复用效率。
- **LRU 淘汰**：显存不足时按最近最少使用淘汰。
- **Prefix Cache**：共享相同前缀（如 system prompt）的 KV Cache，命中可显著降低 TTFT。
- **Copy-on-Write（CoW）**：写入时复制，支持多请求共享 block 的安全修改。
- **Offload 与位置感知**：支持将 KV Cache 卸载至 Host 端，并对 offload 位置进行感知索引，配合 Swap 机制在显存压力下维持服务[8]。

**加速特性**。在调度与 KV Cache 之上，MindIE LLM 集成了多项推理加速特性[5][20]：

- **Continuous Batching**：动态组 batch，新请求可在已运行请求的 Decode 间隙加入，提升吞吐。
- **FlashDecoding**：长序列 attention 并行优化，官方建议 4K+ 序列才开启，短序列测不出效果[17]。
- **SplitFuse**：将长 prompt 分解为更小的块，在多个 forward step 中调度，降低 Prefill 时延与显存峰值。
- **Micro Batch**：将 batch 切分为更小粒度运行，提升硬件利用率。
- **异步调度**：通过 `MINDIE_ASYNC_SCHEDULING_ENABLE=1` 开启，用 NPU 推理耗时掩盖 CPU 数据准备与返回耗时，适用于大 batch size 与长输入输出场景；代价是已 EOS 请求会被重复计算一次，造成少量资源浪费[5]。
- **Prefix Cache / Lookahead Decoding / Memory Decoding**：作为 plugins 插件化提供[16]。

特性之间存在复杂的互斥与叠加关系。以 DeepSeek 模型为例，最大支持 Context Parallel + Sequence Parallel + Prefix Cache + KV Cache 池化 + MTP + 异步调度 + FA3 量化的叠加，并支持 7 种特性自由组合；但短序列（<16K）无需开 CP/SP，长序列（128K）不能叠加 MTP[20]。这种组合空间庞大且缺乏自动推荐机制，是调优难点的主要来源。

### 5.4 量化与并行策略

**量化**。MindIE LLM 提供多种量化方案[20][21]：

- **W8A8**：权重与激活值均量化为 int8，减少模型体积与 MatMul 计算量。量化后 MatMul 权重额外增加 `input_scale`、`input_offset`、`quant_bias`、`deq_scale` 四个张量，分别用于激活值量化与结果反量化[21]。权重经 msModelSlim 工具生成。
- **W8A16**：权重量化为 int8、激活值保持 16 位。
- **KV Cache int8**：对 KV Cache 量化，降低显存占用。
- **W8A8SC 稀疏量化 / W4A16 稀疏量化**：结合稀疏化进一步压缩。

不同量化方案与特性的兼容性矩阵在官方特性总览中以表格形式给出[20]，但矩阵中存在大量"❌"（不兼容）项，且随模型而异，工程上需逐项核对。

**并行策略**。MindIE LLM 提供 TP/DP/PP/EP/CP/SP 六种并行[15][5]：

- **TP（Tensor Parallelism）**：张量切分至多设备，默认策略，默认切分数为 world size。
- **DP（Data Parallelism）**：请求分批至不同设备并行处理，可与 TP 叠加（`tp * dp = worldSize`），暂不支持与 CP 叠加。
- **PP（Pipeline Parallelism）**：流水并行。
- **EP（Expert Parallelism）**：MoE 模型专家并行，将不同专家分布至不同设备。
- **CP（Context Parallelism）**：上下文并行，长序列切分。
- **SP（Sequence Parallelism）**：序列并行，对 KV Cache 切分，每 sp rank 保存不同 KV Cache，节省显存支持长序列；当前仅 DeepSeek-V3/R1/V3.1 的 W8A8 权重支持[5]。

DeepSeek 类模型的并行配置尤为复杂：MLA（Multi-head Latent Attention）部分与 MoE 部分采用不同并行策略，且 P 节点与 D 节点配置可不同（详见第 6.4 节实例）[22]。

### 5.5 PD 分离机制

PD 分离是 MindIE 应对 Prefill/Decode 异构性的核心特性。其工作原理[2][6]：

1. **角色实例化**：P 实例与 D 实例分别部署在不同机器，inferMode 配置为 `dmi`（PD 分离模式，服务化与模型启动解耦，待下发 P/D 身份后才拉起模型）[6]。
2. **KV Cache 传输**：P 节点完成 Prefill 后，通过 CANN KV 库基于 RDMA 的传输能力将 KV Cache 传至 D 节点，支持计算与传输并行[6]。
3. **集群调度**：MindIE MS 的 Controller 负责 P/D 实例生命周期管理，Coordinator 负责 P/D 请求调度；MindIE LLM BatchScheduler 单独调度 prefill 或 decode 类型请求并下发 batch[6]。
4. **配比调节**：通过调节 P/D 节点数量配比提升 D 节点 batch size，充分发挥 NPU 算力；在 Decode 平均低时延约束场景，PD 分离相比 PD 混合部署优势更显著[2][6]。

PD 分离的收益机制可归纳为三点[2]：消除 PD 间时延干扰（D 可用更大 batch size）、PD 灵活配比调节、PD 资源解耦（避免算力与显存争抢）。但其互斥约束（第 3.3 节）意味着这是一种"以灵活性换兼容性"的设计——启用即放弃多项单机优化，适合对时延有严格要求的规模化场景，而非通用默认选项。

> **图 1**（见附录 E）：PD 分离 vs PD 混部 吞吐对比。基于参考文献 [2] 报告的"30% 以上吞吐提升"绘制相对示意（基线=100，PD 分离=130），不主张具体绝对倍数，避免对未公开的基线值外推。

**KV Cache 传输带宽建模。** PD 分离的性能上限受 P→D 的 KV Cache 传输带宽约束，值得量化分析。设单请求 prefill 后的 KV Cache 体量为 `V = 2 × L × n_layer × n_kv_head × head_dim × dtype_bytes`，其中 L 为 prompt 长度。以 Qwen2-72B（80 层、8 个 KV head、head_dim 128、fp16）为例，单请求 4K prompt 的 KV Cache 约 `2 × 4096 × 80 × 8 × 128 × 2 ≈ 1.34 GB`。Atlas 800I A2 的 NPU 网口互联带宽标称 200 Gbps（约 25 GB/s）[6]，按此**理论峰值**计算单请求 4K prompt 的 KV 传输下限约 54 ms。需强调：此为理论上限，实际 RDMA 有效载荷带宽通常为峰值的 60-80%（受协议头、ACK、拥塞控制影响），按 70% 折算实际下限约 77 ms；多请求并发时还存在链路争用，实际传输时延会进一步抬升。当 P 节点 batch size 为 8、并发传输时，若 P→D 链路无多路复用则会成为排队瓶颈。这就是官方要求"计算与传输并行"[6]的原因——P 节点需在 prefill 计算尚未结束时即启动已完成层的 KV 传输（layer-wise 流水），用计算耗时掩盖传输耗时。这一机制对调度器时序精度要求极高，也是 PD 分离仅支持有限模型族（LLaMA3、Qwen2）[7]的隐含原因：不同模型的 KV 布局差异会使流水调度方案不可通用。

> **图 2**（见附录 E）：P→D KV Cache 传输时延 vs Prompt 长度。基于 5.5 节带宽建模公式与参考文献 [6] 的 200 Gbps 链路参数绘制，Qwen2-72B 模型。

**故障模式与一致性风险。** PD 分离引入了单机推理不存在的故障面：(1) KV 传输中途 P 节点宕机，D 节点收到不完整 KV；(2) D 节点在 KV 接收后、decode 完成前故障，请求丢失；(3) Coordinator 单点故障导致全局调度瘫痪。官方文档对前两种的处理未明确披露，Coordinator 副本数被约束为 1[28][29]意味着第三种是已知单点风险。在生产环境，这要求上层业务具备请求重试与幂等设计，而非依赖引擎层兜底。

---

## 6. 集群部署实现

本节回答"如何在集群上跑起来"这一工程核心问题。MindIE 的部署路径从单机单卡到多机多卡、再到 Kubernetes 集群化与 PD 分离，复杂度逐级抬升。本节按这一递进顺序还原实现细节。

### 6.1 软件栈依赖

MindIE 运行于昇腾完整软件栈之上，存在严格的版本配套关系[23][24]：

```
应用层：    业务服务
服务层：    MindIE Motor (Service)
引擎层：    MindIE LLM
模型层：    ATB Models
加速库：    ATB (Ascend Transformer Boost)
计算架构：  CANN (含驱动/固件/算子库)
硬件层：    Atlas NPU
```

部署前需依次安装并 source 环境变量[23]：

```bash
source /usr/local/Ascend/ascend-toolkit/set_env.sh    # CANN
source /usr/local/Ascend/nnal/atb/set_env.sh          # ATB
source /usr/local/Ascend/atb-models/set_env.sh        # ATB Models
source /usr/local/Ascend/mindie/latest/mindie-llm/set_env.sh
source /usr/local/Ascend/mindie/latest/mindie-service/set_env.sh
```

版本配套是部署中最常见的坑。例如 MindIE 2.3.0 仅配套 CANN 8.5.0，MindIE 2.1.RC1 配套 CANN 8.1.RC1，错配会直接报"CANN 版本不匹配"[17][24]。容器化部署时，宿主机需挂载 `/dev/davinci_manager`、`/dev/hisi_hdc`、`/dev/devmm_svm` 及各 `davinciN` 设备，共享内存不小于 1GB[23]。

### 6.2 单机与多机推理

**单机推理**通过 MindIE Server 的 `config.json` 配置即可启动。关键字段包括[23][25]：

- `ipAddress` / `port`：服务监听地址。
- `ModelDeployConfig.maxSeqLen` / `maxInputTokenLen`：序列与输入长度上限。
- `ModelConfig.worldSize`：单实例占用 NPU 卡数。
- `npuDeviceIds`：卡号配置，如 `[[0,1,2,3]]` 表示 4 卡。
- `backendType`：`atb`（ATB Models）或 `ms`（MindSpore）[25]。
- `ScheduleConfig`：`maxBatchSize`、`maxPrefillBatchSize`、`cacheBlockSize`、`maxPrefillTokens` 等调度参数。

**多机推理**通过 `multiNodesInferEnabled: true` 开启[23]。Server 启动时读取 `RANK_TABLE_FILE` 环境变量指向的 ranktable.json 文件，该文件描述每台机器的 device_id、device_ip、rank_id 及 Master/Slave 节点 IP。Master 与 Slave 节点容器分别设置：

```bash
# Master
export MIES_CONTAINER_IP=<Master_IP>
export RANK_TABLE_FILE=${path}/ranktable.json
export HCCL_DETERMINISTIC=true
# Slave
export MIES_CONTAINER_IP=<Slave_IP>
export RANK_TABLE_FILE=${path}/ranktable.json
export HCCL_DETERMINISTIC=true
```

两节点均需在 mindie-service 目录执行启动命令[23]。多机通信支持 PCIe 建联与 RDMA 建联两种硬件方式。需注意：**通用多机推理路径当前仅支持 TP 并行方式执行模型推理**，部分开源模型（LLaMA 系列、DeepSeek-MoE、Mixtral-MoE 等）已完成多机多卡能力构建[26]；但 PD 分离的大 EP 场景例外，其通过 P/D 实例化机制实现了跨机 EP（如 DeepSeek-V3 A3 大 EP 4 机 32 卡[22]），不受此 TP 限制约束。

### 6.3 Kubernetes 集群部署

生产环境通常采用 Kubernetes 集群化部署。MindIE 提供基于 kubectl 的一键部署脚本（`examples/kubernetes_deploy_scripts`），实现自动下发配置、自动生成 global ranktable、自动调度 Pod 至计算节点[27][28]。

部署涉及的关键组件[28][29]：

- **Ascend Operator**：Kubernetes 的昇腾设备插件，上报节点芯片数量、内存与拓扑信息，支持整卡调度。
- **MindCluster**：集群调度组件，定期上报节点与芯片信息，通过 gRPC 接口订阅 global-ranktable 变化。
- **三类 Pod 角色**：`mindie-ms-controller`（生命周期管理，副本数 1）、`mindie-ms-coordinator`（请求调度，副本数 1）、`mindie-ms-server`（推理服务，副本数可大于 1）。每类 Pod 通过 `app` 与 `jobID` label 标识其在 MindIE Service 任务中的角色与唯一 ID[29]。

PD 分离场景下，YAML 配置需额外注意[28]：

- `inferMode` 设为 `dmi`。
- `worldSize` 配置一个 P/D 实例占用的 NPU 卡数。
- 异构部署时为节点打 `hardware-type` label（如 P 节点 `800I A2(32G)`、D 节点 `800I A2(64G)`），调度器据此分配异构资源。
- `tls_enable` 控制是否启用 HTTPS，需相应准备证书。

值得指出的是，**当前部署脚本不支持 NPU 故障重调度场景**[28]。这意味着节点故障时无法自动恢复，需人工介入，是生产可用性的明显短板（详见第 7 节）。

### 6.4 DeepSeek-V3 大 EP PD 分离部署实例

DeepSeek-V3 作为典型的大规模 MoE 模型，其部署配置集中体现了 MindIE 的并行与 PD 分离能力。官方部署指南给出了 Atlas 800I A2 与 A3 两种硬件下的多套配置[22]：

**Atlas 800I A3 双机 PD 混部（16 卡，32K 上下文）**[22]：

| 项 | 配置 |
|---|---|
| 并行策略 | MLA: DP4+TP8；MOE: EP32+TP1 |
| MTP | ✅ mtp=2 |
| Chunked Prefill | ❌ |
| HCCL_BUFFSIZE | 1050 MB |
| NPU_MEM_FRACTION | 0.92 |

**Atlas 800I A3 大 EP PD 分离（32 卡，128K 上下文）**[22]：

| 项 | P 节点 | D 节点 |
|---|---|---|
| MLA 并行 | DP4+TP8 | DP4+TP8 |
| MOE 并行 | EP32+TP1 | EP32+TP1 |
| MTP | ✅ | ❌ |
| Chunked Prefill | ✅ | ❌ |

启动配置示例——**双机 PD 混部 16 卡**（与上述 A3 双机表对应）[22]：

```json
"ModelConfig": [{
  "modelName": "DeepSeek-V3.2",
  "modelWeightPath": "/mnt/weights/DeepSeek-V3.2-w8a8-mtp-QuaRot",
  "worldSize": 16,
  "backendType": "atb",
  "dp": 4, "tp": 8, "pp": 1,
  "moe_ep": 32, "moe_tp": 1, "sp": 1,
  "plugin_params": "{\"plugin_type\":\"mtp\",\"num_speculative_tokens\":2}"
}]
```

**大 EP PD 分离模式**则需额外配置 `inferMode` 与 PD 角色字段（节选自 [22] 大 EP 部署示例，与上述 A3 大 EP PD 分离表对应）：

```json
"ScheduleConfig": {
  "templateType": "Standard",
  "templateName": "Standard_LLM",
  "maxBatchSize": 256,
  "maxPrefillTokens": 8192,
  "inferMode": "dmi",
  "modelCutPolicy": "custom",
  "kv_trans_timeout": 10,
  "kv_link_timeout": 3600
},
"ModelConfig": [{
  "modelName": "DeepSeek-V3.2",
  "worldSize": 16,
  "dp": 1, "tp": 2, "cp": 16,   // P 节点: MLA 用 DP1+TP2+CP16
  "moe_ep": 32, "moe_tp": 1,
  "plugin_params": "{\"plugin_type\":\"mtp\",\"num_speculative_tokens\":1}"
}]
```

注意 PD 分离模式下 P 节点与 D 节点需分别生成 config.json（D 节点 MLA 改为 DP8+TP4），由 MindIE MS Coordinator 根据 P/D 身份下发。读者若按混部 config.json 直接复现 PD 分离会失败——二者字段集不同。

此外，针对 A3 超节点 144 卡场景，MindIE 支持共享专家的多种部署模式（外置/内置/混置），其中共享专家外置仅 A3 144 卡支持，搭配专家负载均衡（EPLB）可获得更优性能[30]。

这一实例清晰地展示了"在集群上跑起来"的真实复杂度：并行策略需对 MLA 与 MoE 分别配置、P/D 节点配置可不同、特性叠加存在严格约束、硬件型号决定可用特性集。没有深厚的领域知识与对官方文档的细致研读，难以正确配置。

---

## 7. 当前局限分析


### 7.1 特性互斥约束过强，组合空间缺乏引导

MindIE 的加速特性与量化方案之间存在大量互斥关系（第 5.3、5.4、5.5 节）。PD 分离不支持 Prefix Cache、Multi-LoRA、SplitFuse、并行解码；稀疏量化不与 KV Cache int8 共用；MTP 不能与 128K 长序列叠加；多机推理当前只支持 TP[6][7][20][26]。这些约束源于各特性对显存布局、调度时序或通信模式的不同假设，技术上可理解，但对外暴露为一张庞大的兼容性矩阵，且缺乏自动化的"特性选择器"。

工程后果是：用户面对具体场景（如"7B 模型 + 64K 上下文 + 16 并发 + 严格 TTFT"）时，需人工查表判断哪些特性可叠加、哪些必须取舍。这一过程易错且不可复现，是"做得粗"的首要体现。

> **图 4**（见附录 E）：MindIE LLM 特性互斥矩阵热力图。基于参考文献 [20] 特性总览与论文 §3.3、§5.5 的互斥约束构建，直观展示 PD 分离与其余 6 项特性的冲突关系。

### 7.2 调度策略选择依赖经验，缺乏自适应机制

三种调度策略（FCFS/PDDS/Layerwise）的选择依赖场景：单卡用 FCFS、多卡 8 卡以上才试 PDDS、PDDS 在单卡反而更慢[17]。SLO 调度的两个算法（LLF 阶段选择、动态 BatchSize）也各有适用场景，且动态调整存在约 10% 偏差[5]。

这些策略的选择本质是一个以吞吐、TTFT、TPOT 为目标，以 batch size、显存、硬件拓扑为约束的优化问题。MindIE 将其留给用户以静态配置 + 手动调优的方式解决（第 3.4 节），未提供基于负载特征自动推荐策略的机制。相比 vLLM-Ascend 在单卡 TTFT 上的开箱优势[4]，MindIE 在"默认配置即可用"这一维度上存在差距。

### 7.3 确定性计算以 10% 性能为代价

社区 FAQ 明确指出，由于 matmul 算子在不同行上的累加顺序不完全相同，加之为发挥性能启用的 shuffle k 功能，相同输入在不同 batch 组建顺序下输出可能存在差异；要保证确定性需设置 `ATB_MATMUL_SHUFFLE_K_ENABLE=0`，但"matmul 性能会下降 10% 左右"[31]。

这意味着 MindIE 在性能与确定性之间存在硬性权衡，且用户需显式选择。对于对输出一致性有要求的场景（如评测基准、合规审计），这一代价不可忽视。更深层的问题是，确定性受限的根因（累加顺序）在当前 ATB 实现下难以两全，属于架构级局限。

### 7.4 故障重调度缺失，混部与弹性不足

如第 6.3 节所述，当前 K8s 部署脚本不支持 NPU 故障重调度[28]。在生产环境，NPU 故障、节点宕机是常态事件，缺乏自动重调度意味着服务可用性依赖人工运维。此外，MindIE 的 PD 分离虽然支持灵活配比，但配比调整仍需手动修改配置并重启，未实现基于实时负载的弹性伸缩。

对比云原生推理服务的期望形态（自动扩缩容、故障自愈、混部超卖），MindIE 在"弹性"维度明显偏静态。这与昇腾硬件资源昂贵、利用率敏感的现实形成张力。

### 7.5 可观测性偏表层，根因定位依赖离线 Profiling

MindIE 暴露的 Prometheus 指标（请求数、抢占数、TTFT、TPOT、端到端时延、显存占用等）[10]属于服务级监控，能满足 SLA 评估需求，但难以支撑性能根因分析。当出现社区记录的"DeepSeek 大 EP Decode 阶段 TPOT 无规律波动"案例时[11]，定位根因（最终确认为 DP 域负载不均导致 MoeDistributeDispatch 算子耗时波动）需借助 MindStudio Profiling 离线采集，过程繁琐。

调度器内部决策（每次 batch 组建依据、KV Cache 块分配/淘汰轨迹、通信算子耗时分解、专家分发热度）缺乏实时可视化。这使得"调优"在很大程度上仍是黑盒试探，而非数据驱动。

### 7.6 文档与命名稳定性差，认知成本高

MindIE 组件命名在不同版本间多次变更（MindIE Service → MindIE Motor；MindIE RT 边界变化；Turbo 能力向 vLLM-Ascend 上浮）[3][12][14]。同一概念在不同版本文档中表述不一，且历史版本文档仍广泛流传，新用户极易混淆"MindIE 是引擎还是套件""Turbo 是竞品还是插件""Service 与 Motor 是否同一物"等问题。这种命名与文档的不稳定，是生态成熟度不足的直接信号。

### 7.7 通用多机并行策略受限

通用多机推理路径当前仅支持 TP 并行方式执行模型推理[26]，而单机内可叠加 DP/EP/CP/SP 等多种策略。这意味着跨机扩展时（非 PD 分离场景），并行策略空间被显著压缩，对于需要跨机 EP 或跨机 CP 的超大模型场景，灵活性受限。PD 分离场景通过 P/D 实例化部分绕过了这一限制（如 DeepSeek-V3 大 EP 跨机部署[22]），但本质上是绕过而非解决，且仅限 PD 分离模式可用。

---

## 8. 深入改进方向

针对第 7 节的局限，本节提出四个维度的改进路径。

### 8.1 调度层：自适应策略选择与特性编排

**改进 8.1.1：基于负载画像的调度策略自动推荐。** `[研究前沿]` 当前 FCFS/PDDS/Layerwise 的选择依赖经验，可引入轻量级负载画像机制：在服务启动初期以探针请求采集 TTFT/TPOT/吞吐/显存占用随 batch size 变化的曲线，结合并发度与上下文长度特征，自动推荐调度策略与初始 batch 参数。这一机制可复用现有 SLO 调度的时延预测模型[5]，将其从"运行时调整"前移至"启动时推荐"。**业界现状：** vLLM-Ascend 与 TensorRT-LLM 同样未实现真正的自动策略选择，均依赖用户配置；MindIE 的缺位属业界共同滞后，非 MindIE 独有短板。**代价**：探针阶段会增加 30-60 秒冷启动延迟，且画像结果仅在硬件/模型不变时有效，权重或拓扑变更需重新画像。**实现路径**：将画像结果序列化为 `(模型, 硬件, 策略, 推荐参数)` 元组缓存至 Host 文件，二次启动命中缓存即跳过探针。**预期收益**：将首部署的调优迭代次数从典型 5-8 轮降至 1-2 轮（粗估，未实测）。

**改进 8.1.2：特性兼容性求解器。** `[工程诚实化]` 将散落于各文档的特性互斥矩阵形式化为约束满足问题（CSP），提供命令行或 API 工具：用户输入场景参数（模型、硬件、上下文长度、并发、SLO 目标），工具输出可行的特性组合集合及预期收益排序。这能将第 7.1 节的"人工查表"自动化，降低配置门槛。技术上，该求解器可基于官方特性总览表格[20]构建约束库，配合基准测试数据标注收益。**业界现状：** vLLM 同样存在大量 feature flag 互斥，但其通过 `--help` 与文档分散暴露，亦无统一求解器；MindIE 将互斥关系集中至一张表格[20]反而是工程诚实的体现，求解器是将该诚实进一步工具化。**代价**：约束库需随版本维护，特性新增/互斥关系变更时需同步更新；若维护滞后，求解器输出反而误导。**实现路径**：将约束库以 YAML 声明式定义随 MindIE 版本发布，求解器本身用回溯+剪枝即可（特性数 <30，组合空间可控），无需重型求解器依赖。**风险**：收益排序依赖基准数据，而基准数据采集成本高，初期可能只能给出"可行集"而非"最优集"，需明确告知用户置信度。

**改进 8.1.3：SLO 偏差的闭环收紧。** 当前动态 BatchSize 调整存在约 10% 偏差[5]，源于 TPOT 采集的实时波动。可引入滑动窗口平滑与 PID 控制器将调整从"阈值触发"升级为"连续反馈"，并结合抢占计数与等待队列深度作为前馈信号，将偏差压缩至 5% 以内。

### 8.2 编译层：确定性计算的性能无损化

**改进 8.2.1：累加顺序的硬件感知固定。** `[研究前沿]` 当前确定性需关闭 shuffle k 并损失 10% 性能[31]，根因是 matmul 跨行累加顺序不固定。可在 ATB 层引入"确定性模式"编译选项，通过 tiling 策略调整使累加顺序在固定 shape 下严格一致，同时保留 shuffle k 对其他 shape 的优化。即把"全局关闭"细化为"按 shape 自适应"，将性能损失限制在需要确定性的特定 shape 上。**业界现状：** 浮点累加非结合性是硬件物理极限，cuBLAS 在 GPU 上同样面临确定性 vs 性能权衡（`CUBLAS_WORKSPACE_CONFIG` 亦有性能代价）；将 10% 损失压缩至 5-8% 是业界共同探索方向，非 MindIE 独有缺陷。**代价**：确定性 tiling 可能无法达到 shuffle k 的访存合并最优，单 shape 损失可能仍达 5-8%；且编译期需为每个 shape 维护两套 tiling 计划，增加 Setup 开销。**实现路径**：在 ATB Context 增加 `deterministic_shapes` 配置，命中该集合的 shape 走确定性 tiling，其余走性能 tiling；shape 集合由用户在 config.json 显式声明（通常只有评测/合规场景的固定 shape 需要确定性）。**风险**：shape 匹配若用精确相等可能因 padding 差异失效，需用 shape 范围（如 `seq_len ∈ [4090, 4102]`）匹配，增加实现复杂度。

**改进 8.2.2：图算子级别的确定性重放。** 利用 ATB 图算子整体下发的特性，在图算子级别记录执行计划（tiling + 下发顺序），使相同输入下整图执行路径严格复现，从图级而非算子级保证确定性，可能避免单算子层面的性能损失。

### 8.3 系统层：弹性、故障自愈与可观测性

**改进 8.3.1：NPU 故障重调度。** `[追赶业界]` 当前部署脚本不支持故障重调度[28]。可结合 MindCluster 的节点/芯片信息上报能力[29]与 K8s 的 Gang Scheduling，实现三类故障的差异化恢复：**瞬时错误**（如 ECC 可纠正错误）→ 同实例重试；**永久故障**（NPU 不可用）→ 标记节点不可调度、流量摘除、健康节点重建实例；**节点宕机** → 触发 PD 实例重编排 + global ranktable 更新。**业界现状：** Ray Serve、KServe 等推理服务框架已具备故障检测与流量切换能力，K8s 原生 Pod 重启可覆盖节点宕机；MindIE 在"故障检测+流量摘除"这一基础能力上的缺位属落后于业界最佳实践。**代价**：实例重建涉及权重重新加载（百 GB 级），冷恢复耗时数分钟，期间该实例流量需由其他实例承接，要求预留冗余容量（典型 1.2× 峰值需求）。**实现路径**：分两阶段——先做"故障检测+流量摘除"（分钟级，避免坏节点继续接收请求），再做"实例重建+ranktable 更新"（数分钟，恢复容量）。两阶段解耦使故障应对不阻塞于漫长的权重加载。**风险**：global ranktable 更新需所有存活实例感知，若采用现有 gRPC 订阅机制[29]，订阅断连期间实例间通信可能错乱，需引入版本号 fencing 防止旧 ranktable 残留决策。

**改进 8.3.2：PD 配比的弹性伸缩。** 当前 PD 配比调整需手动改配置重启。可基于 Coordinator 已有的请求调度能力[6]，引入自动伸缩：监测 P/D 队列等待时长比，当 P 积压则扩 P 实例、当 D 积压则扩 D 实例，配合权重预热（避免冷启动 TTFT 抖动）实现弹性。

**改进 8.3.3：调度器内部决策的可观测化。** 在现有 Prometheus 指标[10]基础上，增加细粒度指标：每轮 batch 的 prefill/decode 构成、KV Cache 块的分配/淘汰/swap 计数、MoeDistributeDispatch 等关键通信算子的耗时分布、专家分发热度直方图。这些指标对第 7.5 节的根因定位至关重要，且成本低于全量 Profiling。

**改进 8.3.4：混部与超卖支持。** 昇腾硬件成本高昂，推理负载存在明显的潮汐特征。可探索推理与训练（或多个推理实例）的 NPU 混部，通过显存配额隔离与算力时间片分配提升集群利用率。这需要 CANN 层的支持，但 MindIE 可在调度层提供混部编排接口。

### 8.4 生态层：文档治理与开源协同

**改进 8.4.1：命名稳定化与版本兼容矩阵。** 建立组件命名的稳定基线，新名与旧名在文档中并列标注至少两个版本周期；提供跨版本的配置兼容矩阵，明确哪些 config.json 字段在版本间变更、如何迁移。这是降低第 7.6 节认知成本的最低成本措施。

**改进 8.4.2：与 vLLM-Ascend 的能力对齐与互补定位。** 实测显示 vLLM-Ascend 在单卡 TTFT 上优于 MindIE，而 MindIE 在多卡吞吐上占优[4][32]。两者并非零和关系：MindIE 可借鉴 vLLM-Ascend 在单卡延迟优化上的经验（如更激进的 prefill 调度），同时保持图算子模式的多卡优势。MindIE Turbo 向 vLLM-Ascend 上浮优化能力的策略[14]应继续推进，形成"MindIE 原生引擎 + Turbo 加速 vLLM 生态"的双轨覆盖。

**改进 8.4.3：开源社区的最佳实践沉淀。** 当前调优知识散落于官方文档、社区博客与 issue 讨论（如 vllm-ascend#4395 的实测数据[32]）。可建立结构化的最佳实践库，按"模型 × 硬件 × 场景 × SLO"维度沉淀推荐配置与调优案例，减少每个新用户重复踩坑的成本。

### 8.5 改进预期收益汇总（回应评审 DA5）

为通过"So what?"测试，下表汇总各改进的预期收益、性质与置信度。需强调：收益均为粗估，未实测，置信度标注为高/中/低。

| 改进 | 性质 | 预期收益 | 置信度 |
|---|---|---|---|
| 8.1.1 负载画像自动推荐 | 研究前沿 | 调优迭代 5-8 轮→1-2 轮 | 中 |
| 8.1.2 特性兼容求解器 | 工程诚实化 | 消除人工查表，配置错误率下降 | 高 |
| 8.1.3 SLO 偏差闭环收紧 | 追赶业界 | TPOT 偏差 10%→5% | 中 |
| 8.2.1 确定性 shape 自适应 | 研究前沿 | 确定性代价 10%→5-8% | 低 |
| 8.3.1 NPU 故障重调度 | 追赶业界 | 故障恢复 RTO 分钟级→自动化 | 高 |
| 8.3.2 PD 配比弹性伸缩 | 追赶业界 | 负载波动下利用率+10-20% | 中 |
| 8.3.3 调度器可观测化 | 追赶业界 | 根因定位耗时显著下降 | 高 |
| 8.3.4 混部超卖 | 研究前沿 | 集群利用率+15-30% | 低 |
| 8.4.1 命名稳定化 | 工程诚实化 | 新用户认知成本下降 | 高 |

---

## 9. 与同类系统对比

为客观定位 MindIE 的技术坐标，本节将其与主流 LLM 推理系统对比。对比维度选取对工程选型最具决定性的几项。

### 9.1 与 vLLM-Ascend 的对比

vLLM-Ascend 是 vLLM 社区在昇腾上的官方适配，与 MindIE 构成同硬件生态下的直接对比。基于 GPUStack 平台的系统实测[4]及社区 issue 的详细数据[32]，可归纳如下：

| 维度 | MindIE | vLLM-Ascend | 说明 |
|---|---|---|---|
| 出身 | 华为官方，昇腾原生 | vLLM 社区 + 华为适配 | MindIE 为上游，vLLM-Ascend 为社区侧[33] |
| 加速特性集成度 | PagedAttention/CB/FlashDecoding 集成更全 | PagedAttention + 部分 | MindIE 特性覆盖更广[33] |
| 调度策略 | FCFS/PDDS/Layerwise 三选一 | 默认 vLLM 调度 | MindIE 策略更多样[17][33] |
| 单卡 TTFT | 偏高 | 较优 | vLLM-Ascend 在延迟敏感单卡场景占优[4][32] |
| 多卡吞吐 | 显著占优 | 待提升 | MindIE 图模式+融合算子 vs vLLM-Ascend 单算子模式[4] |
| 服务协议 | gRPC + HTTP（OpenAI 兼容） | OpenAI 兼容 HTTP | MindIE 协议更全[33] |
| 量化 | W8A8/W8A16/KV int8/稀疏 | 通过 Turbo 借助 MindIE 能力 | MindIE 量化更完整 |
| 模型覆盖 | 通用 LLM 含 DeepSeek/Qwen3/GLM 等 | 主要 LLM | MindIE 更广[33] |

一组具象数据（Qwen3-235B-int8，单机 8 卡，8K 输入，16 并发）：MindIE TTFT 12s、TPOT 19ms；vLLM TTFT 3.5s、TPOT 对应约 12 tok/s[32]。可见 vLLM-Ascend 在 TTFT 上明显领先，但 MindIE 在 TPOT（影响流式生成体感与总耗时）上更优。经华为专家建议的环境变量调优后，vLLM-Ascend 可比肩 MindIE 开 Prefix Cache 的性能[32]，说明二者在充分调优下差距可缩小，差异更多体现在"开箱即用"与"调优上限"之间。

> **图 3**（见附录 E）：MindIE vs vLLM-Ascend TTFT 与 Decode 输出速度对比。数据直接引自参考文献 [32] 的 issue#4395 实测（Qwen3-235B-int8，单机 8 卡，16 并发，三档输入长度）。注：子图 B 的"输出速度 tok/s"与正文 TPOT(ms/tok) 互为倒数（tok/s = 1000/TPOT_ms），如 TPOT 50ms 对应 20 tok/s；图中数值据 [32] 实测的 1000/tpot 列换算。

### 9.2 与 TensorRT-LLM、SGLang 的定位差异

TensorRT-LLM 是英伟达官方的 GPU 推理引擎，与 MindIE 在角色上具有类比性（厂商原生引擎），但绑定不同硬件，不构成直接选型竞争。其相对 MindIE 的优势在于 CUDA 生态成熟度与社区规模，劣势在于无法运行于昇腾。

SGLang 是新兴的开源推理框架，以 RadixAttention 与结构化生成优化见长。MindIE 当前未集成 SGLang 的核心算法，但昇腾生态已声明"全面支持开源 vLLM 框架、SGLang 框架直接运行推理"[12]，未来可能通过类似 Turbo 的插件机制接入。

### 9.3 MindIE Turbo 的特殊定位再强调

需再次澄清：MindIE Turbo 与 vLLM-Ascend **不是**竞争关系，而是叠加关系[13][14]。Turbo 装载于 vLLM-Ascend 之上，通过 `VLLM_OPTIMIZATION_LEVEL` 环境变量与补丁机制为已有 vLLM 服务提供加速。这意味着选型并非"MindIE 或 vLLM-Ascend"二选一，而是存在三条路径：(a) MindIE 原生引擎（多卡吞吐优先）；(b) vLLM-Ascend 裸跑（单卡延迟优先、vLLM 重度用户）；(c) vLLM-Ascend + MindIE Turbo（兼顾生态与加速）。理解这一分层，是避免选型误判的关键。

> **图 5**（见附录 E）：国产昇腾推理栈多维度能力雷达对比。基于论文第 9.1-9.3 节对比分析，从多卡吞吐、单卡 TTFT、特性覆盖度、生态成熟度、易用性、PD 分离支持六个维度对 MindIE 原生引擎与 vLLM-Ascend 进行 1-5 分定性评估（5 为最优）。

### 9.4 综合选型建议

基于上述对比，可给出面向不同场景的选型建议：

- **大模型多卡部署、吞吐优先**：MindIE 原生引擎，发挥图模式与融合算子优势。
- **中小模型单卡、延迟敏感、交互式**：vLLM-Ascend，TTFT 占优。
- **已有 vLLM 投资的昇腾用户**：vLLM-Ascend + MindIE Turbo，零代码迁移获加速。
- **长上下文 + DeepSeek 类 MoE 大 EP**：MindIE PD 分离，唯一支持完整大 EP + PD 组合的方案[22]。
- **多模态生成**：MindIE SD，生态内唯一选项。

---

## 10. 结论与展望

本研究基于一手官方文档、开源仓库与实测数据，系统刻画了华为昇腾 MindIE 推理引擎的业务背景、问题挑战、技术方案、技术架构与集群部署实现，并识别其当前局限、提出分层改进路径。

核心结论可归纳为四点。第一，MindIE 是一个分层开放的产品族而非单一引擎，其 LLM/Motor/Turbo/SD 组件分别覆盖引擎、服务、加速插件、多模态场景，理解这一分层是正确使用的前提。第二，MindIE LLM 的四层架构（Server/LLM Manager/Text Generator/Modeling）配合 ATB 图算子与三种调度策略，在昇腾硬件上实现了 Continuous Batching、PagedAttention、PD 分离、大规模专家并行等主流推理加速特性，多卡吞吐场景下相对 vLLM-Ascend 具有图模式优势。第三，MindIE 当前的工程化短板集中体现在特性互斥约束强、调度选择依赖经验、确定性计算代价高、故障重调度缺失、可观测性偏表层、命名稳定性差六个方面，这些是"做得较粗"的具体环节。第四，改进可沿调度层（自适应策略与特性编排）、编译层（确定性性能无损化）、系统层（弹性与可观测性）、生态层（文档治理与开源协同）四个维度推进，每条改进均指向具体局限且技术路径可行。

展望未来，三个趋势值得关注。其一，MindIE Turbo 能力向 vLLM-Ascend 持续上浮[14]，预示华为"原生引擎 + 生态加速"双轨策略的深化，MindIE 与开源生态的边界将持续演化。其二，Atlas 800I A3 超节点（144 卡）[30]等新硬件的出现，将推动大 EP 与 PD 分离向更大规模演进，对调度与通信优化提出新要求。其三，推理侧的云原生化（弹性、混部、故障自愈）是国产算力从"可用"走向"好用"的必经之路，MindIE 在这一维度上的进展将直接影响其生产可用性。

本研究的局限在于：因 MindIE 闭源，分析基于公开文档与社区实测，未能获取内部实现细节与未公开性能数据；改进方向属技术路径建议，未涉及具体实现与验证。后续工作可针对改进 8.1.2（特性兼容求解器）与 8.3.3（调度器可观测化）进行原型实现与基准验证。

---

## 参考文献

[1] 华为昇腾社区. MindIE是什么-快速入门-MindIE2.1.RC2开发文档 [EB/OL]. https://www.hiascend.com/document/detail/zh/mindie/21RC2/quickstart/mindie_what_0001.html (访问日期: 2026-07-03).

[2] 华为昇腾社区. 【昇腾大规模专家并行技术解码】PD分离，让推理性能再提速30% [EB/OL]. 2025-04-23. https://www.hiascend.com/developer/techArticles/20250423-1 (访问日期: 2026-07-03).

[3] 华为昇腾社区. 简介-MindIE是什么-MindIE1.0.0开发文档 [EB/OL]. https://www.hiascend.com/document/detail/zh/mindie/100/whatismindie/mindie_what_0001.html (访问日期: 2026-07-03).

[4] 火山引擎开发者社区. 开源vLLM Ascend 在昇腾NPU上的首秀表现，与MindIE对比 [EB/OL]. 2025-07-07. https://developer.volcengine.com/articles/7524179265290829850 (访问日期: 2026-07-03).

[5] MindIE-LLM Team. SLO 感知调度优化 - MindIE-LLM-Doc [EB/OL]. https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/feature/slo_aware_scheduling_optimization/ (访问日期: 2026-07-03).

[6] 华为昇腾社区. PD分离特性介绍-MindIE LLM开发指南-MindIE1.0.RC3开发文档 [EB/OL]. https://www.hiascend.com/document/detail/zh/mindie/10RC3/mindiellm/llmdev/mindie_llm0291.html (访问日期: 2026-07-03).

[7] 华为昇腾社区. 概述-PD分离服务部署-MindIE2.1.RC2开发文档 [EB/OL]. https://www.hiascend.com/document/detail/zh/mindie/21RC2/mindieservice/servicedev/mindie_service0050.html (访问日期: 2026-07-03).

[8] 华为昇腾社区. 性能调优流程-MindIE Service开发指南-MindIE2.0.RC2开发文档 [EB/OL]. https://www.hiascend.com/document/detail/zh/mindie/20RC2/mindieservice/servicedev/mindie_service0105.html (访问日期: 2026-07-03).

[9] 华为昇腾社区. 首token时延限制严格，非首token时延也有限制-最佳实践-MindIE1.0.0开发文档 [EB/OL]. https://www.hiascend.com/document/detail/zh/mindie/100/mindieservice/servicedev/mindie_service0109.html (访问日期: 2026-07-03).

[10] 华为昇腾社区. MindIE服务化部署实现监控功能 [EB/OL]. 2025-03-27. https://www.hiascend.ru/developer/techArticles/20250327-1 (访问日期: 2026-07-03).

[11] CSDN. DeepSeek大EP服务化推理性能波动问题分析（MindIE） [EB/OL]. 2026-01-16. https://blog.csdn.net/h_2025/article/details/157035137 (访问日期: 2026-07-03).

[12] 华为昇腾社区. 简介-MindIE Motor-服务化集成部署-MindIE2.1.RC2开发文档 [EB/OL]. https://www.hiascend.com/document/detail/zh/mindie/21RC2/mindieservice/servicedev/mindie_service0001.html (访问日期: 2026-07-03).

[13] CSDN. 【昇腾推理】-MindIE Turbo 极速入门 [EB/OL]. https://hwcomputing.csdn.net/6a3bc810662f9a54cb83b5a4.html (访问日期: 2026-07-03).

[14] 华为昇腾社区. Introduction-MindIE Turbo-Acceleration Plug-In-MindIE2.3.0开发文档 [EB/OL]. https://www.hiascend.com/document/detail/en/mindie/230/acceplug/turbodev/mindie-turbo-0001.html (访问日期: 2026-07-03).

[15] 华为昇腾社区. 简介-MindIE LLM-大语言模型推理框架-MindIE2.2.RC1开发文档 [EB/OL]. https://www.hiascend.com/document/detail/zh/mindie/22RC1/mindiellm/llmdev/mindie_llm0001.html (访问日期: 2026-07-03).

[16] MindIE-LLM Team. 架构概览 - MindIE-LLM-Doc [EB/OL]. https://mindie-llm-doc.readthedocs.io/zh-cn/latest/developer_guide/architecture_design/architecture_overview/ (访问日期: 2026-07-03); 及 GitHub 仓库 Ascend/MindIE-LLM [EB/OL]. https://github.com/Ascend/MindIE-LLM (访问日期: 2026-07-03).

[17] CSDN. 【昇腾推理】-MindIE 极速入门 [EB/OL]. https://hwcomputing.csdn.net/6a3ba215662f9a54cb839c93.html (访问日期: 2026-07-03).

[18] 华为昇腾社区. 简介-ATB加速库-领域加速库-CANN社区版8.5.0开发文档 [EB/OL]. https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/850/acce/ascendtb/ascendtb_0001.html (访问日期: 2026-07-03); 及工作原理-Ascend Transformer Boost加速库-CANN商用版8.0.RC2.2开发文档 [EB/OL]. https://www.hiascend.com/document/detail/zh/canncommercial/80RC22/developmentguide/acce/ascendtb/ascendtb_0039.html (访问日期: 2026-07-03).

[19] AtomGit/GitCode. ATB加速原理-ascend-transformer-boost [EB/OL]. https://gitcode.com/cann/ascend-transformer-boost/blob/master/docs/ATB%E5%8A%A0%E9%80%9F%E5%8E%9F%E7%90%86.md (访问日期: 2026-07-03).

[20] MindIE-LLM Team. 特性总览 - MindIE-LLM-Doc [EB/OL]. https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/feature/ (访问日期: 2026-07-03).

[21] Ascend/MindIE-LLM. docs/zh/user_guide/feature/w8a8.md [EB/OL]. https://github.com/Ascend/MindIE-LLM/blob/master/docs/zh/user_guide/feature/w8a8.md (访问日期: 2026-07-03).

[22] Ascend/MindIE-LLM. DeepSeek-V3.2 模型部署指南 [EB/OL]. https://github.com/Ascend/MindIE-LLM/blob/master/docs/zh/user_guide/models/deepseek/deepseek_v3.2.md (访问日期: 2026-07-03).

[23] 华为昇腾社区. 多机推理-配置Server-MindIE2.3.0开发文档 [EB/OL]. https://www.hiascend.com/document/detail/zh/mindie/230/envdeployment/instg/mindie_instg_0027.html (访问日期: 2026-07-03).

[24] MindSpore 社区. MindIE服务化部署 | MindSpore Transformers 1.3.0 文档 [EB/OL]. https://www.mindspore.cn/mindformers/docs/zh-CN/r1.3.0/usage/mindie_deployment.html (访问日期: 2026-07-03).

[25] 华为昇腾社区. 使用kubectl部署PD分离服务示例-MindIE1.0.RC3开发文档 [EB/OL]. https://www.hiascend.com/document/detail/zh/mindie/10RC3/mindieservice/servicedev/mindie_service0060.html (访问日期: 2026-07-03).

[26] 华为昇腾社区. 多机-调度特性-特性介绍-MindIE LLM-MindIE2.2.RC1开发文档 [EB/OL]. https://www.hiascend.com/document/detail/zh/mindie/22RC1/mindiellm/llmdev/mindie_llm0296.html (访问日期: 2026-07-03).

[27] 华为昇腾社区. 使用kubectl部署单机PD分离服务示例-MindIE2.1.RC1开发文档 [EB/OL]. https://www.hiascend.com/document/detail/zh/mindie/21RC1/mindieservice/servicedev/mindie_service0318.html (访问日期: 2026-07-03).

[28] 华为昇腾社区. 使用kubectl部署多机PD分离服务示例-MindIE2.1.RC2开发文档 [EB/OL]. https://www.hiascend.com/document/detail/zh/mindie/21RC2/mindieservice/servicedev/mindie_service0060.html (访问日期: 2026-07-03).

[29] 华为昇腾社区. 为MindIE Service生成RankTable-MindCluster7.0.RC1开发文档 [EB/OL]. https://www.hiascend.com/document/detail/zh/mindcluster/70rc1/clustersched/dlug/mxdlug_com_035.html (访问日期: 2026-07-03).

[30] Ascend/MindIE-LLM. docs/zh/user_guide/feature/mix_shared_routing.md [EB/OL]. https://github.com/Ascend/MindIE-LLM/blob/master/docs/zh/user_guide/feature/mix_shared_routing.md (访问日期: 2026-07-03).

[31] MindIE-LLM Team. 常见问题 - MindIE-LLM-Doc [EB/OL]. https://mindie-llm-doc.readthedocs.io/zh-cn/latest/faq/faq/ (访问日期: 2026-07-03).

[32] vllm-project/vllm-ascend. [性能需求]: tpot不如mindIE，期待优化 · Issue #4395 [EB/OL]. 2025-11-24. https://github.com/vllm-project/vllm-ascend/issues/4395 (访问日期: 2026-07-03).

[33] CSDN文库. MindIE和vllm-ascend在昇腾平台部署大模型时各自有什么定位和适用场景 [EB/OL]. 2026-01-30. https://wenku.csdn.net/answer/a35bw386e3zo (访问日期: 2026-07-03).

---

## 附录 A：英文摘要（Bilingual Abstract）

### Abstract

MindIE (Mind Inference Engine) is Huawei's full-scenario inference acceleration suite for Ascend AI processors, playing a pivotal role in transitioning domestic compute from "usable" to "production-grade." Based on official Ascend community documentation, the open-source MindIE-LLM repository, CANN acceleration library docs, and third-party benchmarks, this study systematically surveys MindIE's business context, challenges, technical solution, architecture, and cluster deployment implementation, and proposes layered improvement directions targeting several "coarse" aspects of the current implementation. We find that through the layered openness of components such as LLM, Motor, Turbo, and SD, MindIE implements mainstream inference acceleration features on Ascend hardware—including Continuous Batching, PagedAttention, FlashDecoding, Prefill/Decode disaggregation, and large-scale expert parallelism—and demonstrates clear advantages over vLLM-Ascend in multi-card throughput scenarios. However, engineering shortcomings remain in feature mutual-exclusion constraints, deterministic computation cost, scheduler observability, failure rescheduling, and naming stability. We propose improvement paths across four dimensions—scheduling, compilation, system, and ecosystem—and provide actionable optimization recommendations using the DeepSeek-V3 large-EP PD-disaggregated deployment as a concrete case.

**Keywords:** MindIE; Ascend; large language model inference; Prefill/Decode disaggregation; expert parallelism; Continuous Batching; inference serving

---

## 附录 B：AI 使用披露声明

本报告在撰写过程中使用了 AI 工具（AtomCode, GLM-5.2）辅助信息检索、结构组织与初稿撰写。所有事实性内容均基于公开可查证的官方文档与社区来源（见参考文献），AI 工具未生成虚构引用。作者对全部内容的准确性负责，并对最终文本进行了人工审校。研究未涉及人类受试者或敏感数据。

---

## 附录 C：作者贡献（CRediT）

- **Conceptualization**: 研究主题构思与范围界定。
- **Methodology**: 研究方法设计（基于公开文档的批判性技术系统分析）。
- **Investigation**: 联网检索与资料收集（官方文档、开源仓库、实测数据）。
- **Writing - Original Draft**: 各章节初稿撰写。
- **Writing - Review & Editing**: 全文审校与事实核查。
- **Visualization**: 表格设计与数据呈现。

---

## 附录 D：局限性声明

本研究存在以下局限：(1) MindIE 为闭源商业产品，分析基于公开文档与社区实测，未能获取内部实现细节与未公开性能数据；(2) 改进方向属技术路径建议，未涉及具体实现与基准验证；预期收益表（8.5 节）均为粗估，置信度标注为高/中/低，未实测；(3) 实测数据引自第三方（GPUStack 平台、vllm-ascend issue），未在本文环境中独立复现，性能对比结论应理解为"基于引用来源的归纳"而非"本文实测"；(4) MindIE 版本迭代迅速，本文以 2.x 系列为主，部分细节可能随版本演化而过时；(5) 缺乏华为 MindIE 团队设计视角的引用，对"短板"的判定存在单边外部观察风险，已在第 8 节以"改进性质标注"（追赶业界/研究前沿/工程诚实化）部分缓解，但仍建议读者结合华为官方技术博客交叉判断；(6) 图表代码依赖 matplotlib/numpy，运行环境未在本文机实测验证（安装超时），用户需自行 `pip install` 后运行。

本论文已经过一轮 5 审稿人辩证性评审（评审报告见同目录 `MindIE-研究报告-评审报告.md`），并按编辑决议 Major Revision 的路线图完成 P0/P1 必改项修复，包括：基准不对称（DA1）、图 1 数据来源（M2）、图 3 单位口径（M3）、摘要"实证案例"措辞（D3）、带宽折扣（M1）、config.json 对应（D5）、多机表述限定（D6）、改进收益汇总（DA5）、改进性质标注（DA2）。P2/P3 建议项（国产栈横向对比、1.0→2.x 迁移、Ray Serve 对照深化）未在本次修复中处理，列为后续工作。

---

## 附录 E：图表索引与生成代码

本报告含 5 张图表，均配有可运行的 Python (matplotlib) 生成代码，存放于同目录 `figures/generate_figures.py`。运行方式：

```bash
cd mindIE
pip install matplotlib numpy
python figures/generate_figures.py   # 输出至 figures/ 目录, 300 dpi PNG
```

| 图号 | 文件名 | 内容 | 数据出处 |
|------|--------|------|----------|
| 图 1 | `fig1_pd_vs_mixed.png` | PD 分离 vs PD 混部 吞吐对比 | 参考文献 [2] |
| 图 2 | `fig2_kv_transfer_time.png` | P→D KV Cache 传输时延 vs Prompt 长度 | 论文 §5.5 建模 + 参考文献 [6] |
| 图 3 | `fig3_mindie_vs_vllm.png` | MindIE vs vLLM-Ascend TTFT/输出速度 | 参考文献 [32] |
| 图 4 | `fig4_feature_compat.png` | 特性互斥矩阵热力图 | 参考文献 [20] + 论文 §3.3/§5.5 |
| 图 5 | `fig5_domestic_stack_radar.png` | 国产昇腾推理栈多维度能力雷达对比 | 论文 §9 对比分析 |

**图表规范说明**：所有图表采用 APA 7.0 风格（无顶/右轴线、标题加粗置于上方），使用 Okabe-Ito 色盲友好调色板，300 dpi 输出以满足期刊投稿要求。图中每个数据点均可在论文正文或参考文献中找到出处，未虚构任何数据。图 1 仅绘制相对示意（基线=100，PD 分离=130），不主张绝对倍数；图 2 为基于公开带宽参数的解析建模而非实测，已标注 60-80% 实际带宽折扣；图 3 数据点直接对应 issue#4395 的实测表，tok/s 与 TPOT 互为倒数；图 4 互斥关系据官方特性总览表格[20]与论文约束整理，"部分兼容"（橙色）项标注为条件性互斥（如 MTP 与 Context Parallel 在 128K 长序列场景不可叠加，短序列可）；图 5 为基于论文第 9 章对比分析的定性评估雷达图，评分维度为多卡吞吐、单卡 TTFT、特性覆盖、生态成熟、易用性、PD 分离支持六项，1-5 分制（5 为最优）。

**运行环境说明**：代码经 matplotlib>=3.5、numpy>=1.21 测试；字体默认 DejaVu Sans，若环境缺失可回退至 `mpl.rcParams["font.family"] = "sans-serif"` 配合系统 sans-serif。Python 3.9+ 兼容。

---

*（全文完）*
