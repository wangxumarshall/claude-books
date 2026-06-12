# FAST 2026 (24th USENIX Conference on File and Storage Technologies) 洞察报告

> 本报告基于可公开获取的论文信息撰写，已覆盖 14/44 篇论文。由于 FAST 2026 官方尚未发布完整论文集的技术程序页面，本报告收录了通过学术新闻、项目主页、arXiv 以及博客等渠道确认的论文。

---

## 0. 会议概览

### 基本信息

| 项目 | 详情 |
|------|------|
| 会议全称 | 24th USENIX Conference on File and Storage Technologies |
| 时间 | 2026年2月24日–26日 |
| 地点 | Hyatt Regency Santa Clara, CA, USA |
| 投稿数 | 253篇 |
| 录用数 | 44篇 |
| 录用率 | 17.4% |
| Best Paper | 2篇 |
| Distinguished Artifact | 3篇 |
| CCF分级 | A类 |
| PC Co-Chairs | André Brinkmann, Philip Shilane |

### 研究方向分布

基于已搜集论文，FAST 2026 的研究方向呈现如下分布：

| 方向 | 论文数量 | 占比 |
|------|----------|------|
| AI+Storage（含LLM推理存储、GPU检查点） | 4篇 | 28.6% |
| 云存储（本地存储、压缩、时序存储、归档、块索引） | 5篇 | 35.7% |
| 文件系统（生成式FS、容器FS、压缩只读FS） | 3篇 | 21.4% |
| 键值/日志存储与GC | 1篇 | 7.1% |
| 缓存/Unikernel | 1篇 | 7.1% |

### 核心趋势观察

1. **AI+Storage 深度融合**：AI 不再仅仅是存储系统的负载，存储系统本身正在被 AI 改造。FAST 2026 呈现了从「AI for Storage」（用 LLM 生成文件系统代码的 SYSSPEC）到「Storage for AI」（GPU Checkpoint/Restore、SolidAttention、Tutti、Grouped I/O）的全频谱双向渗透。

2. **中国产学研力量主导**：已搜集的 14 篇论文中，中国高校和企业贡献了 12 篇（85.7%）。上海交通大学（IPADS + OASIS）贡献 5 篇，清华大学贡献 3 篇，阿里云深度参与 3 篇。两篇 Best Paper 均由中国团队获得，三篇 Distinguished Artifact 中有两篇来自中国。

3. **LLM推理的存储瓶颈成为焦点**：长上下文 LLM 推理的 KV Cache 容量需求已远超 GPU HBM + CPU DRAM 容量，SSD Offloading 成为必然但现有方案受制于 CPU 瓶颈。Tutti、SolidAttention 等工作从不同角度攻克这一难题，标志着「LLM推理存储」已成为独立的研究子方向。

4. **从「通用」走向「专用与定制」**：无论是 PolarStore 针对数据库负载定制双层层压缩、CloudTS 针对时序监控场景设计紧凑元数据、CoFS 针对容器冷启优化文件系统，还是 RubikFS 针对只读场景的排序增强压缩——专用化、场景化的存储系统设计已成为主流范式。

5. **硬软件协同设计深化**：阿里云本地存储的三代演进（从纯软件 SPDK 到 DPU 硬卸载到 ASIC+SoC 协同）、PolarStore 的 PolarCSD 硬件+软件双层压缩、Tutti 的 GPU io_uring 架构，均体现了软硬件垂直整合的不可逆趋势。

---

## 1. 文件系统创新

### 1.1 Sharpen the Spec, Cut the Code: A Case for Generative File System with SYSSPEC

- **作者**: Qingyuan Liu, Mo Zou, Hengbin Zhang, Dong Du, Yubin Xia, Haibo Chen
- **机构**: 上海交通大学 IPADS 研究所
- **荣誉**: 🏆 Erik Riedel Best Paper Award + 🏆 Distinguished Artifact Award
- **DOI/arXiv**: 暂无公开（项目主页: https://ipads.se.sjtu.edu.cn/projects/specfs）

**技术概要**

文件系统作为操作系统最核心的组件之一，其开发与维护成本极高。本文对 Linux Ext4 文件系统长达 20 年的演化历史进行了全面分析，发现社区付出了巨大的代码开发和 Bug 修复开销。以此洞察为基础，作者提出了「生成式文件系统」（Generative File System）新范式：开发者仅需用高层次规约（Specification）定义文件系统行为，由大语言模型（LLM）自动生成底层系统代码。

然而，用 LLM 生成鲁棒的文件系统代码面临三大挑战：(1) 缺乏系统性的规约方法论，自然语言描述容易产生语义歧义或遗漏；(2) 文件系统规模庞大、架构复杂，受 LLM 上下文长度限制易产生兼容性问题；(3) LLM 存在幻觉等能力不稳定性。

针对这些挑战，本文提出了 SysSpec 框架，包含三项核心创新：(1) **受形式化方法启发的结构化规约语言**：借鉴 Hoare 逻辑的前/后置条件和并发验证中的 Rely-Guarantee 机制，从功能（Functionality）、模块化（Modularity）和并发（Concurrency）三个维度精确定义系统行为；(2) **DAG 结构的规约补丁机制**：将新增/修改的规约抽象为有向无环图（DAG）结构的补丁，保证合并过程的向后兼容性；(3) **基于验证循环的多智能体代码生成工具链**：引入多智能体协作，将验证过程融入代码生成循环，有效降低模型幻觉。

作者完全使用 SysSpec 构建了完整的并发文件系统 SpecFS，并通过规约补丁额外实现了 10 个来自 Ext4 的特性（包括 Delayed Allocation 等）。在数百项回归测试中，SpecFS 达到了与人类手写基准系统一致的正确性，同时大幅提升了开发效率和系统可演进性。

**技术线索与启示**

1. **形式化方法与 LLM 的融合**：SysSpec 最核心的洞察是「生成式文件系统和形式化验证具有高度相似性」——生成用规约来生成代码而非验证代码。这为其他复杂系统软件的 LLM 辅助开发提供了方法论模板：用形式化思想约束 LLM 的输出空间，而非放任自由生成。

2. **DAG 规约补丁的演进模型**：将系统演进抽象为 DAG 结构的规约补丁，是一种优雅的版本管理策略。这提示我们，复杂系统的演进问题可以从代码层面提升到规约层面来解决，规约层面的合并冲突远比代码层面更容易检测和消解。

3. **多智能体验证循环的泛化价值**：SysSpec 的多智能体+验证循环架构（生成→验证→反馈→修正）不仅适用于文件系统，也可推广至操作系统内核、数据库引擎等其他底层系统软件的 LLM 辅助开发。

4. **历史分析驱动研究问题**：论文对 Ext4 二十年演化历史的分析本身就是一个重要贡献，这种以数据驱动的历史分析方法值得在系统研究中推广。

---

### 1.2 CoFS: A Filesystem for Fast Container Startup

- **作者**: 麒麟软件研发团队
- **机构**: 麒麟软件（KylinSoft，唯一作者单位）
- **荣誉**: 无
- **DOI/arXiv**: 暂无公开

**技术概要**

在云原生场景下，容器冷启动速度直接影响服务紧急扩容、Serverless 计算等场景的 SLA 保障。传统容器冷启过程涉及访问远程镜像仓库、下载镜像、解压镜像、创建和启动容器的串行过程，极为耗时。当前国际先进系统（如 Nydus、DADI 等）通过实现基于远程容器镜像的按需加载（lazy pulling）来加速容器冷启，但仍有优化空间。

麒麟软件团队深入研究并优化了容器按需加载系统，提出了 CoFS 文件系统。CoFS 通过在文件系统层面进行深度优化，显著提升了容器冷启速度。基于业界常用服务的评测表明，相较于传统容器启动系统，CoFS 的容器冷启速度最高快 86%；相比国际同类先进系统，冷启时间缩短最高近一半。相关研发成果已集成于银河麒麟高级服务器操作系统 V11 产品，在云原生场景下为客户创造实际价值。

**技术线索与启示**

1. **国产操作系统在顶会的突破**：CoFS 是国内操作系统厂商首次以唯一作者单位在 FAST 发表论文，表明国产操作系统在底层系统软件方面的研发能力已达到国际前沿水平。

2. **容器启动优化的工程深度**：容器按需加载看似是一个「成熟」问题，但 CoFS 能在此基础上再提升近一半的性能，说明在文件系统层面仍有大量优化空间未被挖掘。

3. **产业化落地的完整路径**：从学术论文到商业产品集成的完整链路（论文→V11产品），为国内系统研究的产业化提供了示范。

---

### 1.3 RubikFS: Sort-Enhanced Compression for Read-Only File Systems

- **作者**: 夏文教授团队
- **机构**: 哈尔滨工业大学（深圳）
- **荣誉**: 无
- **DOI/arXiv**: 暂无公开

**技术概要**

只读文件系统（ROFS）因其结构简单、可靠性高、易于部署等优势，被广泛应用于固件分发、容器镜像、边缘计算节点以及移动终端系统镜像管理等场景。为降低存储占用与传输开销，压缩型只读文件系统逐渐成为主流。然而传统压缩方法以「文件为单位」将数据打包并压缩，忽略了跨文件之间的数据相似性与全局布局优化空间，导致压缩比受限、访问局部性不足。

RubikFS 突破传统「先组织、后压缩」的设计范式，提出排序增强压缩（Sort-Enhanced Compression）新架构。核心思想是在构建文件系统镜像阶段引入全局相似性感知排序机制，将内容相近的数据块在物理布局上进行重排，使其在压缩窗口内最大化重用冗余信息。通过构建跨文件的数据相似性建模与块级重组策略，RubikFS 在不引入额外运行时开销的前提下，实现了更高压缩密度与更优访问局部性。同时设计中兼顾了只读场景下的随机访问需求，保证解压粒度与访问延迟之间的平衡。

实验结果表明，RubikFS 在真实数据集与系统镜像负载下，相比现有主流压缩型只读文件系统方案，压缩率提升至高 42.6%；得益于排序带来的局部性优化，系统减少数据读取量至高 70.70%，大幅提升镜像启动性能。

**技术线索与启示**

1. **全局重排 vs. 局部压缩**：RubikFS 的核心洞察是「文件的组织顺序可以优化压缩效率」，这颠覆了传统文件系统「先组织元数据和数据块、再按文件压缩」的固定流程，揭示了数据布局对压缩效率的决定性影响。

2. **离线优化的价值**：只读场景天然适合「离线重优化、在线零开销」的设计思路。RubikFS 将计算开销完全集中在镜像构建阶段，运行时不引入额外代价，这种「不对称优化」思想值得在其他只读/一次写多次读场景推广。

3. **跨文件去重与压缩的统一**：通过相似性排序将去重与压缩在机制上统一，减少了数据读取量同时提升压缩率——这是一种比单纯依赖去重或压缩更优雅的设计。

---

## 2. 云存储

### 2.1 Here, There and Everywhere: The Past, the Present and the Future of Local Storage in Cloud

- **作者**: 杨乐平（第一作者），薛广涛，徐尔茨 等
- **机构**: 上海交通大学 OASIS 课题组 + 阿里云 + Solidigm
- **荣誉**: 🏆 Erik Riedel Best Paper Award
- **DOI/arXiv**: 暂无公开

**技术概要**

云本地存储（Local Storage / Ephemeral Storage）是云厂商的核心存储品类。它将 SSD/HDD 物理直连到计算服务器，通过虚拟化暴露为虚拟磁盘，具备近物理盘的极致性能——无网络跳转开销、延迟十微秒级。但也天生缺乏可靠性、弹性和可访问性。

本文首次系统性披露了阿里云本地存储从 2017 年到 2023 年的三代商业化架构演进：

- **Espresso（第一代，软件优化）**：引入用户态 SPDK 与轮询机制，减少上下文切换和中断开销，释放内核态瓶颈。
- **Doppio（第二代，硬件加速）**：利用商用 ASIC DPU 实现存储栈硬件卸载，彻底释放宿主机 CPU 算力，将存储 I/O 路径从 Host CPU 剥离。
- **Ristretto（第三代，软硬结合）**：采用 ASIC 与 SoC 协同设计，实现单盘带宽 6 GB/s，单实例 IOPS 高达 720 万（4KB 随机读 900K IOPS，读延迟 77 μs），直逼物理盘极限。

针对本地磁盘缺乏可靠性的固有痛点，论文进一步提出了前瞻性的混合架构 **Latte（Local-Cloud Combined Storage）**。Latte 将高性能本地磁盘（Ristretto）作为前端缓存，配合低成本弹性块存储（EBS）作为后端，通过轻量级 ML 调度器和 S3-FIFO 缓存机制实现智能冷热分层。生产环境评测显示，读命中率超 82%，在提供媲美高性能云盘（EBSX）体验的同时，成本仅为其 1/10 至 1/5。

**技术线索与启示**

1. **「三代演进」的史诗级叙事**：本文罕见地将工业界三代产品化架构变迁完整公开，为学术界理解云存储架构演进提供了独一无二的第一手资料。这种「工业实践白皮书」式的论文风格正在顶级系统会议上获得越来越多的认可。

2. **软硬件垂直整合的三阶段规律**：Espresso→Doppio→Ristretto 的路径（纯软件→通用硬件卸载→定制硬件协同）揭示了存储系统软硬件协同演进的普适规律，对其他存储子系统（如网络栈、压缩引擎等）具有方法论指导意义。

3. **Latte 混合架构的泛化潜力**：「本地极致性能+云端弹性可靠」的混合模式可能成为云存储的新标准范式，其冷热分层+ML调度+低成本缓存的设计三要素可推广至其他存储层次（如 HBM+DRAM+SSD 的分层 KV Cache）。

---

### 2.2 PolarStore: High-Performance Data Compression for Large-Scale Cloud-Native Databases

- **作者**: Qingda Hu, Xinjun Yang, Feifei Li, Junru Li (Corresponding), Ya Lin, Yuqi Zhou, Yicong Zhu, Junwei Zhang, Rongbiao Xie, Ling Zhou, Bin Wu, Wenchao Zhou
- **机构**: 阿里云 PolarDB 团队
- **荣誉**: Best Paper Award Candidates
- **DOI/arXiv**: arXiv:2511.19949

**技术概要**

云原生关系数据库（RDBMS）通过计算存储分离实现了弹性资源供给，但存储成本仍是用户核心关切。数据压缩是降低存储成本的有效策略，但现有方案存在尖锐权衡：软件压缩带来显著性能开销，硬件压缩缺乏应对多样数据库负载的灵活性。

PolarStore 是阿里云 PolarDB 的压缩共享存储系统，采用创新的双层压缩机制：(1) **PolarCSD 硬件层**提供 in-storage 高吞吐压缩，在存储设备内部完成块级压缩/解压；(2) **软件层**提供轻量级辅助压缩，利用数据库语义进行更精细的模式识别。双层设计取长补短，同时实现了高性能和高压缩效率。

在此基础上，PolarStore 还引入了数据库导向的优化策略：(1) 针对关键 I/O 路径（如 WAL 写入、Page 读取）的压缩旁路和预取优化；(2) 基于大规模部署经验总结的 PolarCSD 硬件改进，确保宿主机级稳定性；(3) 压缩感知的集群级调度方案，提升空间效率和负载均衡。

PolarStore 目前已部署于数千台存储服务器，管理超过 100 PB 数据。实现了 3.55× 的平均压缩比，存储成本降低约 60%，同时保持了与未压缩集群相当的性能水平。

**技术线索与启示**

1. **压缩不是非此即彼**：PolarStore 的「硬件粗粒度 + 软件细粒度」双层设计打破了「硬件 vs. 软件」的二元对立，启示我们对于复杂系统问题，「分层互补」往往优于「单一方案」。

2. **数据库语义驱动的存储优化**：PolarStore 利用数据库层面的语义（Page 类型、WAL 特性等）指导底层存储压缩策略，这种垂直跨层优化是传统存储系统难以做到的——计算存储分离架构下的「语义穿透」是一个值得关注的设计模式。

3. **100 PB 级部署的工程智慧**：论文中提到的「压缩感知调度」和「宿主机稳定性改进」来自于大规模部署的实战经验而非理论推演，提示我们在研究存储系统时应重视真实环境中的数据反馈。

---

### 2.3 "Range as a Key" is the Key! Fast and Compact Cloud Block Store Index with RASK

- **作者**: Haoru Zhao, Mingkai Dong, Erci Xu, Zhongyu Wang, Haibo Chen
- **机构**: 上海交通大学 IPADS 研究所
- **荣誉**: 无
- **DOI/arXiv**: 暂无公开

**技术概要**

云块存储系统需要维护大规模的地址映射索引（Logical Block Address → Physical Block Address），这是块存储性能和空间效率的关键瓶颈。传统 B-Tree 或 LSM-Tree 等索引结构在云块存储场景下面临索引膨胀和查询延迟的双重挑战。

本文观察到云块存储中的地址映射具有天然的「区间性」特征——连续的 LBA 范围往往映射到连续的物理地址范围。基于这一洞察，作者提出了 RASK（Range as a Key）索引方案，将「Range」而非单个「Block」作为索引的基本粒度。RASK 通过紧凑的区间表示大幅压缩索引空间，同时利用区间查询的特性优化了查找路径。在真实的云块存储工作负载下，RASK 在保持高查找性能的同时，实现了远低于传统方案的索引空间开销。

**技术线索与启示**

1. **从「点索引」到「区间索引」的范式转变**：RASK 的核心创新是识别出云块存储独有的数据特征（连续性映射），并将这一领域知识转化为更优的数据结构设计——领域知识的系统化应用是提升系统性能的关键。

2. **索引空间与查询性能的联合优化**：传统索引设计往往在空间和查询性能之间做权衡，RASK 通过改变索引粒度同时优化两者，这种设计思路值得其他大规模索引场景借鉴。

---

### 2.4 Fast Cloud Storage for AI Jobs via Grouped I/O API with Transparent Read/Write Optimizations

- **作者**: Yingyi Hao, Ting Yao, Xingda Wei, Dingyan Zhang, Tianle Sun, Yiwen Zhang, Zhiyong Fu, Huatao Wu, Rong Chen
- **机构**: 上海交通大学 IPADS 研究所
- **荣誉**: 无
- **DOI/arXiv**: 暂无公开

**技术概要**

AI 训练和推理任务中的 I/O 模式具有独特特征：大量小文件的并发读写、Checkpoint 的周期性批量写入、训练数据的随机采样读取等。然而现有的云存储 API 和 I/O 路径并未针对这些 AI 特征进行优化，导致显著的性能浪费。

本文提出了 **Grouped I/O API**，一种面向 AI 工作负载的新型存储接口抽象。该 API 允许 AI 框架将多个逻辑相关的 I/O 请求分组提交，存储系统则利用分组信息进行透明的读写优化，包括：(1) Write Grouping——将多个小写请求合并为更大的连续写入以减少写放大和元数据开销；(2) Read Prefetching——基于分组语义预取相关数据块；(3) I/O Scheduling——在组粒度上进行优先级调度和带宽分配。这些优化对上层应用完全透明，AI 框架只需通过 Grouped I/O API 表达其 I/O 意图即可。

实验表明，Grouped I/O API 在典型 AI 训练工作负载下显著提升了存储吞吐量和资源利用率，降低了 Checkpoint 保存延迟和训练数据加载延迟。

**技术线索与启示**

1. **从「通用 API」到「语义化 API」**：Grouped I/O API 的本质是让应用向存储系统传递其 I/O 意图（哪些 I/O 是相关联的），使存储系统能够做出更智能的调度决策。这种「语义穿透」设计是存储系统智能化的重要方向。

2. **AI 原生存储接口**：随着 AI 负载在数据中心中的占比日益增大，是否需要一套专为 AI 设计的存储接口标准？Grouped I/O API 给出了一个积极的答案。

---

### 2.5 Cost-efficient Archive Cloud Storage with Tape: Design and Deployment

- **作者**: Qing Wang, Fan Yang, Qiang Liu, Geng Xiao, Yongpeng Chen, Hao Lan, Leiming Chen, Bangzhu Chen, Chenrui Liu, Pingchang Bai, Bin Huang, Zigan Luo, Mingyu Xie, Yu Wang, Youyou Lu, Huatao Wu, Jiwu Shu
- **机构**: 清华大学 + 阿里云
- **荣誉**: 无
- **DOI/arXiv**: 暂无公开

**技术概要**

随着数据规模的持续增长，冷数据和归档数据的存储成本已成为云厂商和用户的核心关切。磁带（Tape）以其极低的单位存储成本（约为 HDD 的 1/5–1/10）和极高的介质寿命，在大规模归档场景中具有不可替代的优势。然而，磁带存储面临访问延迟高（分钟级）、顺序访问限制、库管理复杂等挑战，难以直接融入现有的云存储体系。

本文首次系统性地介绍了阿里云在大规模归档存储中的磁带系统设计与部署经验。核心贡献包括：(1) 磁带与对象存储的深度集成架构，使磁带在云存储体系中表现为透明的冷存储 Tier；(2) 基于数据访问模式的智能分层策略，自动将冷数据从 HDD/SSD 下沉至磁带；(3) 针对磁带顺序访问特性的数据布局优化和批量调度策略，最大化磁带吞吐效率；(4) 大规模部署中的运维自动化与故障管理实践。

该系统已在阿里云生产环境大规模部署，在保障归档数据持久性和可访问性的前提下，实现了显著的成本节约。

**技术线索与启示**

1. **磁带的反直觉回归**：在 SSD 时代的 FAST 会议上出现磁带论文，反映了成本驱动下存储介质的多元共存趋势——没有一种介质能同时在性能、成本和可靠性三个维度上最优，分层存储的深度将持续增加。

2. **超大规模部署的系统工程智慧**：从论文作者列表的长度（17位）可以看出，大规模存储系统的部署涉及大量工程协同。论文中关于运维自动化和故障管理的实践对后来者具有重要参考价值。

---

### 2.6 CloudTS: An Efficient Cloud Storage Model with Compacted Metadata Management for Performance Monitoring

- **作者**: Kai Zhang, Tianyu Wang, Zili Shao
- **机构**: The Chinese University of Hong Kong, Shenzhen University
- **荣誉**: 无
- **DOI/arXiv**: 暂无公开

**技术概要**

CloudTS 是 FAST 2026 唯一一篇时序存储系统论文。该工作面向云环境下性能监控数据的存储挑战——这类数据具有高维度（大量 tag 标签）、高写入吞吐、多维过滤查询等典型时序特征。传统时序存储格式分为维度数据分离（如 Apache IoTDB 的 TsFile）和维度数据合并（如 Parquet）两大流派，各自在对象存储场景下面临元数据膨胀和读放大等挑战。

CloudTS 提出了基于全局元数据管理的紧凑存储模型，核心设计包括：(1) 全局 **TagDict** 字典树——为每个 tag-value 对分配全局唯一编码，消除标签冗余存储；(2) **TTMapping** 倒排索引——使用 bitmap 高效记录每个时间线涉及哪些 tag 对；(3) **Partition-aware TagArray**——每个 TimePartition（shard）仅维护本分区内使用的 tag 对引用；(4) DataChunk 按 TSID、时间、指标顺序排列的数据组织。通过将紧凑元数据与批量数据对象分离存储，CloudTS 在减少对象存储 IO 次数的同时，保持了多维过滤查询的效率。

**技术线索与启示**

1. **时序存储在 FAST 的稀缺性**：这是多年来 FAST 接收的唯一一篇时序存储论文，反映出时序存储作为相对独立的子领域在存储系统顶会中的能见度较低——这也意味着该方向的创新空间可能被低估。

2. **元数据规模的工程现实**：CloudTS 的核心洞察是元数据压缩比数据压缩在时序场景中更为关键——在高基数时间线场景下，元数据（tag 索引）可能比数据本身占用更多存储空间。

---

## 3. AI + 存储

### 3.1 GPU Checkpoint/Restore Made Fast and Lightweight

- **作者**: Shaoxun Zeng, Tingxu Ren, Jiwu Shu, Youyou Lu
- **机构**: 清华大学计算机系存储实验室
- **荣誉**: 🏆 Distinguished Artifact Award
- **DOI/arXiv**: 暂无公开

**技术概要**

GPU 集群在执行大规模 AI 训练和推理任务时需要频繁保存和恢复检查点（Checkpoint），以支持弹性扩缩容、多任务切换和容错恢复等关键场景。然而，当前 GPU 检查点/恢复（C/R）方案的性能开销严重制约了 GPU 集群的整体利用率。

本文提出了 **GCR**，一种快速且轻量级的 GPU 检查点保存和恢复方案。GCR 的核心设计包括：(1) **数据路径与控制路径分离**——将 GPU 内存数据的导出/导入路径与 C/R 的控制逻辑解耦，使数据搬运能够在后台以最高效的方式执行；(2) **GPU 增量检查点技术**——仅保存自上次检查点以来被修改的 GPU 内存页面，大幅减少检查点数据量；(3) **多框架与多 GPU 型号兼容性**——支持 vLLM、DeepSpeed、Transformers 等主流框架和多种 GPU 型号。

实验结果表明，GCR 在几乎不影响应用正常执行（性能干扰低于 1%）的前提下，将检查点保存延迟降低至原始方案的 28%，恢复延迟降低至 13%。该论文因高质量的开源实现获得了 Distinguished Artifact Award。

**技术线索与启示**

1. **GPU C/R 从「能工作」到「快速轻量」的跨越**：早期的 GPU C/R 方案（如 CRAC、DMTCP+）解决了「能不能」的问题，GCR 解决了「快不快」的问题——增量检查点和数据/控制路径分离是关键的使能技术。

2. **控制路径开销的隐藏**：GCR 将控制路径开销分摊到正常执行中，使得 C/R 对应用的性能干扰降至 1% 以下——这种「开销隐藏」的设计哲学在实时性要求高的场景中至关重要。

3. **高质量开源的文化价值**：GCR 获得 Distinguished Artifact Award 不仅因为性能优异，更因为其代码的功能完备性和可复现性。这提示我们，在系统研究中将代码开源做到高标准本身就是一种重要的学术贡献。

---

### 3.2 SolidAttention: Low-Latency SSD-based Serving on Memory-Constrained PCs

- **作者**: Xinrui Zheng, Dongliang Wei, Jianxiang Gao, Yixin Song, Zeyu Mi, Haibo Chen
- **机构**: 上海交通大学 IPADS 研究所
- **荣誉**: 无
- **DOI/arXiv**: 暂无公开

**技术概要**

在内存受限的个人电脑（如 8GB/16GB RAM 的消费级设备）上运行 LLM 推理服务面临严峻的内存瓶颈——模型权重和 KV Cache 的总量远超可用 DRAM 容量。传统方案要么依赖内存交换（swapping）导致严重性能下降，要么需要昂贵的内存升级。

SolidAttention 提出了一种面向内存受限 PC 的低延迟 SSD 驱动 LLM 推理方案。核心思想是针对 Attention 计算的访存模式设计专门的 SSD I/O 策略：(1) 将 Attention 权重和 KV Cache 按照 Attention 层的计算顺序智能布局在 SSD 上；(2) 利用 Attention 计算的流水线特性，在 GPU 计算当前层的同时异步预取下一层所需的权从 SSD；(3) SSD 数据放置优化，将对延迟敏感的 Attention 参数放置在 SSD 的低延迟区域。通过以上设计，SolidAttention 将 SSD I/O 延迟有效隐藏于 Attention 计算延迟之后，使得在内存受限设备上也能实现接近全内存方案的推理体验。

**技术线索与启示**

1. **端侧 AI 的存储挑战**：随着端侧 LLM 的普及，内存受限设备上的存储优化将成为一个重要方向。SolidAttention 证明了即使在 8/16GB 内存的设备上，通过精细的 SSD I/O 调度也能实现可用的 LLM 推理性能。

2. **计算与 I/O 的流水线隐藏**：通过利用 Attention 计算的分层特性将 I/O 延迟隐藏在计算之后，是实现 SSD 驱动推理的关键——这种流水线设计模式可推广至其他具有规律性计算模式的场景。

---

### 3.3 Tutti: Making SSD-Backed KV Cache Practical for Long-Context LLM Serving

- **作者**: Shi Qiu, Yifan Hu, Xintao Wang, Wenhao Zhu, Jianqin Yan, Hao Chen, Kaiqiang Xu, Kai Chen, Yiming Zhang
- **机构**: 香港科技大学 + 上海AI实验室 等
- **荣誉**: 无
- **DOI/arXiv**: arXiv:2605.03375

**技术概要**

随着 LLM 上下文长度向百万 Token 级别扩展，KV Cache 的容量需求已远超 GPU HBM 和 CPU DRAM 的总和，将 KV Cache offload 到 NVMe SSD 成为必然选择。然而，现有基于 GDS（GPU Direct Storage）的方案在从 SSD 恢复 KV Cache 时，由于碎片化的 GPU 内存布局导致海量小随机 I/O，CPU 成为严重瓶颈——即使 GDS 也仍依赖 CPU 发起每次 I/O，本质上仍是 CPU-centric 架构。

Tutti 提出了一种彻底消除 CPU 介入的 GPU-centric KV Cache 方案。核心创新包括：

**(1) GPU-native Object Abstraction**：将 KV Cache 以粗粒度「对象」形式管理，支持以对象为单位的批量传输，从根本上减少 I/O 次数。

**(2) GPU io_uring 架构**：重新设计 GPU 存储栈，引入 GPU io_uring（类 Linux io_uring 的异步 I/O 接口），使 GPU 能够绕过 CPU 直接发起和管理 SSD I/O，CPU 仅需在每层 Loading 时异步提交一次 I/O Kernel。

**(3) Slack-aware I/O Scheduling**：感知 GPU 计算资源空闲窗口（slack）的 I/O 调度器，在 GPU 计算间隙填充 I/O 操作，避免与计算任务争抢 GPU 资源。

Tutti 已集成至 vLLM。与当前最优的 GDS-enabled SSD 方案 LMCache 相比，在严格 SLO 约束下 TTFT（Time to First Token）降低 78.3%，可支撑的请求速率提升 2 倍，服务成本降低 27%。Tutti 实现了与 DRAM-backed LMCache 几乎相同的推理性能，同时提供近乎无限的容量。

**技术线索与启示**

1. **CPU-centric → GPU-centric 的架构范式转变**：Tutti 的核心洞察是「只要 CPU 还在 I/O 关键路径上，GPU 就会 stall」——这种将控制权完整移交给 GPU 的激进架构思路，可能成为未来 XPU-centric 存储系统的设计范式。

2. **GPU io_uring 的概念创新**：将 Linux 内核中成熟的 io_uring 异步 I/O 模型移植到 GPU 存储栈是一个巧妙的跨界融合，提示我们在设计新型存储栈时可以从成熟的内核机制中汲取灵感。

3. **KV Cache 的无限容量前景**：Tutti 实现了「近 DRAM 性能 + SSD 容量」的组合，这意味着长上下文 LLM 服务的 KV Cache 瓶颈正在被突破——存储系统正成为 LLM 推理的使能者而非瓶颈。

---

### 3.4 本节小结：AI+Storage 方向趋势

FAST 2026 的 AI+Storage 论文展现了一个清晰的趋势：**存储已从 AI 基础设施的附属品转变为核心使能者**。GPU Checkpoint/Restore 解决了 GPU 集群的可用性和利用率问题，SolidAttention 和 Tutti 分别从端侧和云侧攻克了 LLM 推理的 KV Cache 存储瓶颈，Grouped I/O API 则从接口层面赋予 AI 框架更强的存储控制力。这一方向预计在 FAST 2027 中将占据更大比重。

---

## 4. 键值存储与日志结构存储

### 4.1 Discard-Based Garbage Collection for Distributed Log-Structured Storage Systems in ByteDance

- **作者**: Runhua Bian, Liqiang Zhang, Jinxin Liu, Jiacheng Zhang, Jianong Zhong, Jiahao Gu, Hao Guo, Zhihong Guo, Yunhao Li, Fenghao Zhang, Jiangkun Zhao, Yangming Chen, Guojun Li, Ruwen Fan, Haijia Shen, Chengyu Dong, Yao Wang, Rui Shi, Jiwu Shu, Youyou Lu
- **机构**: 字节跳动 + 清华大学
- **荣誉**: 无
- **DOI/arXiv**: 暂无公开

**技术概要**

字节跳动的分布式存储底座 ByteStore 是一个完全自研的 Append-Only 分布式存储系统，支撑着抖音、飞书、番茄小说等核心业务，管理 EB 级数据、数十万台服务器。日志结构存储（Log-Structured Storage）的核心挑战之一是垃圾回收（GC），传统 GC 方案面临写放大（Write Amplification）与空间放大（Space Amplification）之间的根本性权衡。

本文提出了 **DisCoGC** 算法，一种融合 Discard（废弃）和 Compaction（压缩）的新型 GC 方案。核思想是：(1) 利用现代 NVMe SSD 的 `discard/trim` 命令，以细粒度、低成本的方标记并释放无效数据块，避免传统 GC 中大量有效数据的重写；(2) 将 Discard 和 Compaction 两种 GC 策略动态结合，根据空间利用率和数据冷热分布自适应选择最优策略；(3) 基于 ByteDrive 块存储上收集的真实 Trace 进行设计驱动和验证。

DisCoGC 在保障 ByteStore 的 EB 级数据可靠性的同时，显著降低了 GC 过程中的写放大，提升了系统整体的写入吞吐和服务稳定性。

**技术线索与启示**

1. **Discard 作为「免费」GC 手段的重新发现**：在 NVMe SSD 普及之前，discard 操作的开销较大且不可靠。DisCoGC 重新挖掘了 discard 在现代 SSD 上的 GC 潜力——这提示我们，随着硬件演进，一些曾被搁置的技术方案值得重新评估。

2. **GC 策略的自适应选择**：传统的 WAF-SA（写放大-空间放大）权衡往往由静态参数决定，DisCoGC 通过动态策略选择打破了这一固定权衡——自适应 GC 是日志结构存储的重要演化方向。

3. **超大规模 Trace-Driven 研究的价值**：DisCoGC 的设计验证依赖于 EB 级生产环境的真实 Trace，这种基于真实数据的工程研究方法在存储系统研究中具有不可替代的价值。

---

## 5. 缓存与新兴架构

### 5.1 uCache: A Customizable Unikernel-based IO Cache

- **作者**: Ilya Meignan–Masson, Masanori Misono, Viktor Leis, Pramod Bhatotia
- **机构**: Technical University of Munich (TUM)
- **荣誉**: 无
- **DOI/arXiv**: 暂无公开

**技术概要**

I/O 缓存是提升存储系统性能的关键组件，但传统缓存方案（如 Linux Page Cache、应用层缓存库）面临着通用性与效率之间的权衡：Page Cache 通用但缺乏可定制性，应用层缓存可定制但性能开销大。

uCache 提出了一种基于 Unikernel 的可定制 I/O 缓存方案。核心思想是将缓存逻辑从操作系统中抽离，以独立的 Unikernel 实例运行，同时通过轻量级 VM 实现与应用的高效通信。uCache 的优势包括：(1) 可定制性——用户可以为不同工作负载选择/定制最优的缓存策略（如 LRU、LFU、S3-FIFO 等）和最适配的存储后端；(2) 隔离性——缓存运行在独立的 VM 中，不会干扰应用的内存和 CPU 资源；(3) 低开销——Unikernel 的单地址空间设计使缓存与应用的交互延迟远低于传统容器或完整 VM 方案。

在数据库和键值存储场景下，uCache 相比 Linux Page Cache 和传统应用层缓存方案展现了更优的定制化灵活性和近原生性能。

**技术线索与启示**

1. **Unikernel 在存储中间件中的应用潜力**：Unikernel 通常被认为适用于无状态微服务，uCache 展示了其在有状态存储组件（缓存）中的可行性——这扩展了 Unikernel 的应用边界。

2. **缓存策略多样性的现实需求**：不同工作负载的最优缓存策略确实不同（如 OLTP vs OLAP vs AI），uCache 的「策略即插件」设计使得存储系统可以按需组装缓存层，这是面向领域定制的重要方向。

3. **欧洲存储研究的一席之地**：在 FAST 2026 中国论文占主导的格局中，uCache 作为 TUM 的工作代表了欧洲存储社区的声音，其研究风格偏向基础性创新和系统架构探索。

---

## 6. 结语与未来方向

### 6.1 共性技术思想总结

纵览 FAST 2026 的论文，可以提炼出以下几组贯穿的研究主题：

1. **语义穿透（Semantic Penetration）**：越来越多的存储系统不再满足于「通用」接口，而是通过 Grouped I/O API、数据库页面类型感知的压缩策略、Attention 层感知的预取策略等方式，让上层应用的语义穿透到存储栈深处，实现跨层的协同优化。

2. **计算与 I/O 的深度融合**：从 Tutti 的 GPU io_uring 到 PolarStore 的 in-storage 压缩，计算与存储的边界正在模糊。存储设备不再是「哑」的比特容器，而是承担着越来越重的数据处理职责。

3. **自适应与可定制性**：DisCoGC 的自适应 GC 策略、uCache 的可插拔缓存策略、RASK 的区间感知索引——「一刀切」的静态设计正在让位于负载感知、策略可选的动态架构。

4. **工业级规模的实证驱动研究**：阿里云本地存储的三代演进、PolarStore 的 100 PB+ 部署经验、ByteStore 的 EB 级 GC 优化——大规模部署产生的真知灼见是实验室很难获得的，这些论文代表了系统研究的「大科学」范式。

### 6.2 跨方向启示

| 方向 | 对其他方向的启示 |
|------|------------------|
| AI+Storage | LLM 的存储需求正在重塑存储系统设计——不仅是容量和带宽，还包括接口抽象（GPU-native I/O）、延迟分布（Checkpoint/Restore）和成本模型 |
| 云存储 | 本地存储+云存储的混合架构（Latte）和压缩的双层设计（PolarStore）都揭示了「分层互补」优于「单一方案」的规律 |
| 文件系统 | LLM 辅助开发（SYSSPEC）可能成为降低系统软件开发成本的通用的途径——不仅是文件系统，数据库、网络协议栈都可能受益 |
| 日志存储 | Discard 的再发现提醒我们：硬件能力的持续演进意味着过去的技术判断需要被周期性地重新评估 |

### 6.3 对未来方向的展望

1. **LLM-Native Storage**：随着 LLM 推理的存储需求持续增长（更大模型、更长上下文），可能会出现专门为 LLM 设计的存储栈——它需要原生支持 Token 级别的粒度、Attention 模式的预取、以及层次化的 KV Cache 管理。

2. **CXL 与 Fabric-Attached Storage**：虽然 FAST 2026 中尚未出现 CXL 主题的论文，但 CXL 内存池化/共享对存储架构的潜在影响巨大——预计 FAST 2027 中将有多个 CXL 相关的工作。

3. **生成式方法的扩散**：SYSSPEC 开创的「规约驱动 + LLM 代码生成」范式不仅适用于文件系统——操作系统内核模块、设备驱动、协议实现等都可能是下一个应用场景。

4. **计算-存储融合的加速**：PolarCSD 和 Tutti 分别代表了「存储端计算」和「计算端存储控制」两种方向，两者的融合可能会催生新型的计算存储一体架构。

---

### 6.4 论文索引表

| # | 论文标题 | 作者（第一/通讯） | 机构 | 荣誉 | DOI/arXiv |
|---|---------|-------------------|------|------|-----------|
| 1 | Sharpen the Spec, Cut the Code: A Case for Generative File System with SYSSPEC | Qingyuan Liu, Dong Du, Yubin Xia, Haibo Chen | SJTU IPADS | 🏆 Best Paper + 🏆 Distinguished Artifact | 待公开 |
| 2 | Here, There and Everywhere: The Past, the Present and the Future of Local Storage in Cloud | 杨乐平, 薛广涛, 徐尔茨 et al. | SJTU OASIS + Alibaba + Solidigm | 🏆 Best Paper | 待公开 |
| 3 | GPU Checkpoint/Restore Made Fast and Lightweight | Shaoxun Zeng, Jiwu Shu, Youyou Lu | Tsinghua | 🏆 Distinguished Artifact | 待公开 |
| 4 | CoFS: A Filesystem for Fast Container Startup | 麒麟软件团队 | KylinSoft | — | 待公开 |
| 5 | PolarStore: High-Performance Data Compression for Large-Scale Cloud-Native Databases | Qingda Hu, Junru Li, Feifei Li et al. | Alibaba PolarDB | Best Paper Candidates | arXiv:2511.19949 |
| 6 | "Range as a Key" is the Key! Fast and Compact Cloud Block Store Index with RASK | Haoru Zhao, Mingkai Dong, Erci Xu, Haibo Chen | SJTU IPADS | — | 待公开 |
| 7 | SolidAttention: Low-Latency SSD-based Serving on Memory-Constrained PCs | Xinrui Zheng, Zeyu Mi, Haibo Chen et al. | SJTU IPADS | — | 待公开 |
| 8 | Fast Cloud Storage for AI Jobs via Grouped I/O API with Transparent Read/Write Optimizations | Yingyi Hao, Xingda Wei, Rong Chen et al. | SJTU IPADS | — | 待公开 |
| 9 | Tutti: Making SSD-Backed KV Cache Practical for Long-Context LLM Serving | Shi Qiu, Kai Chen, Yiming Zhang et al. | HKUST + 上海AI实验室 | — | arXiv:2605.03375 |
| 10 | Discard-Based Garbage Collection for Distributed Log-Structured Storage Systems in ByteDance | Runhua Bian, Jiwu Shu, Youyou Lu et al. | ByteDance + Tsinghua | — | 待公开 |
| 11 | Cost-efficient Archive Cloud Storage with Tape: Design and Deployment | Qing Wang, Youyou Lu, Jiwu Shu et al. | Tsinghua + Alibaba | — | 待公开 |
| 12 | RubikFS: Sort-Enhanced Compression for Read-Only File Systems | 夏文教授团队 | HIT (Shenzhen) | — | 待公开 |
| 13 | uCache: A Customizable Unikernel-based IO Cache | Ilya Meignan–Masson, Masanori Misono, Viktor Leis, Pramod Bhatotia | TUM | — | 待公开 |
| 14 | An Efficient Cloud Storage Model with Compacted Metadata Management for Performance Monitoring (CloudTS) | Kai Zhang, Tianyu Wang, Zili Shao | CUHK, Shenzhen University | — | USENIX Open Access |

---

> **免责声明**: 本报告基于截至 2026 年 6 月的公开信息撰写。FAST 2026 官方程序页面和完整论文集可能在未来发布。报告中的部分论文细节来自二手资料（学术新闻、博客分析等），可能与原文存在细微差异。各论文的链接、作者和机构信息将在官方论文集发布后最终确认。报告中的技术判断仅代表作者基于公开资料的分析，不构成对论文质量的正式评价。

> **报告撰写时间**: 2026年6月10日