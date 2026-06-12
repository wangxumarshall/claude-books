# ACM Transactions on Storage (TOS) 2026 洞察报告

> **覆盖时间范围**：2025年6月 – 2026年6月
> **报告生成日期**：2026年6月10日
> **期刊级别**：CCF-A类期刊，JCR Q2（2025 IF: 2.6），中科院分区计算机科学3区
> **报告性质**：本文基于公开可获取的论文摘要、作者主页、arXiv预印本及新闻报道进行综合分析。部分论文在撰写时处于"Just Accepted"阶段，完整版本以ACM Digital Library最终出版为准。

---

## 0. 期刊概览

ACM Transactions on Storage（TOS）是存储系统领域最权威的同行评审期刊之一。作为CCF推荐的A类期刊，TOS聚焦于存储系统体系结构、文件系统、固态存储、分布式存储、存储安全、数据编码理论等核心方向。期刊为季刊，年发文量约34篇，审稿周期约12周，国人论文占比约27%。

2025–2026年度，TOS呈现出几个鲜明的趋势性特征：

1. **ZNS SSD与主机控制存储成为主流**：分区命名空间（Zoned Namespace）SSD的相关研究已从早期的接口适配走向深度系统优化，涵盖RAID、文件系统、键值存储等多个层次。
2. **混合内存/存储在AI时代的重构**：CXL互联、持久内存（PM）、HBM等新型存储层级正在重塑系统架构，存储研究越来越多地与AI推理、大模型KV缓存等场景交叉。
3. **存储安全从被动防御走向主动检测**：在SSD固件层嵌入勒索软件检测能力，代表存储安全正从"加密+备份"向"检测+恢复"一体化演进。
4. **可持续存储与新型介质崭露头角**：微软Project Silica玻璃存储、HDD重估等研究体现了学术界和工业界对存储可持续性的高度关注。
5. **数据缩减技术持续深化**：重复数据删除、Delta压缩、透明压缩等技术在HDD、SSD等不同介质上持续优化。

本报告精选14篇代表性论文，按三大主题领域进行分类综述。

---

## 1. 文件系统与新型存储

### 1.1 SSD存储抽象演进综述

**论文标题**：Storage Abstractions for SSDs: The Past, Present, and Future
**作者**：Xiangqun Zhang, Janki Bhimani, Shuyi Pei, Eunji Lee, Sungjin Lee, Yoon Jae Seong, Eui Jin Kim, Changho Choi, Eyee Hyun Nam, Jongmoo Choi, Bryan S. Kim
**发表信息**：ACM Transactions on Storage, Vol. 21, No. 1, 2025（共44页）
**机构**：多所韩国大学联合（Sungkyunkwan University, Seoul National University等）

**技术概要**：

这是一篇极具参考价值的综述论文，系统追溯了SSD接口从继承HDD块存储范式到闪存专用标准的完整演化历程。论文将SSD存储抽象的发展划分为四个并行演进的支线：(1) 通过主机-SSD提示/指令扩展块抽象（如Multi-Stream SSD）；(2) 增强主机对SSD的控制能力（如Open-Channel SSD、ZNS SSD）；(3) 将主机级管理卸载到SSD（如计算存储Computational Storage）；(4) 使SSD支持字节寻址（如CXL SSD）。论文深入分析了闪存转换层（FTL）在其中的角色演变：早期SSD通过FTL模拟块接口以保证向后兼容，但FTL引入的设备级垃圾回收（GC）导致了不可预测的I/O性能。ZNS通过将FTL管理责任上移至主机端，消除了设备级GC，实现了接近1的写放大因子。论文还讨论了Flexible Data Placement（FDP）、计算存储、字节寻址SSD等前沿方向，为SSD技术发展提供了清晰的路线图。

**技术启示**：
- SSD接口演进的核心矛盾在于"主机控制粒度"与"设备管理复杂度"之间的权衡——ZNS将FTL提升至主机端代表了当前最优解，而CXL SSD则可能通过字节寻址彻底消除块抽象。
- Multi-Stream和FDP（Flexible Data Placement）作为块抽象的扩展方案仍具有实用价值，尤其在企业级SSD部署中。
- 计算存储（Computational Storage）代表了存储近数据处理的新范式，但面临编程复杂性、生态系统碎片化和散热功耗三大挑战。
- 该综述可作为存储系统研究者快速建立SSD技术全貌的入门读物。

**论文覆盖率说明**：基于论文摘要和期刊目录信息进行概括。

---

### 1.2 ZapRAID：面向ZNS SSD的高性能日志结构RAID系统

**论文标题**：The Design and Implementation of a High-Performance Log-Structured RAID System for ZNS SSDs
**作者**：Jinhong Li, Qiuping Wang, Shujie Han, Patrick P. C. Lee
**发表信息**：ACM Transactions on Storage, 2025（arXiv: 2402.17963, 41页, FAST'24扩展版）
**机构**：The Chinese University of Hong Kong（香港中文大学）, Peking University（北京大学）

**技术概要**：

ZNS SSD的Zone Append原语通过将地址管理卸载到设备端，释放了分区内写入并行度，显著提升了写入性能。然而在构建多盘RAID阵列时，Zone Append带来了严峻挑战：主机无法直接指定写入地址，也无法控制并发Zone Append命令之间的写入顺序，这与传统RAID需要静态分配条带地址的需求直接冲突。ZapRAID提出了三项核心技术：(1) 基于分组的数据布局（Group-based Data Layout），以粗粒度顺序跨多个条带组组织数据，使用小型元数据实现逐组条带管理；(2) 混合数据管理策略，巧妙结合Zone Write和Zone Append两种原语，同时利用分区内和分区间并行度；(3) 轻量级条带元数据设计，通过组级管理而非逐条带管理降低了元数据开销。ZapRAID以用户态块设备形式实现，实验表明在正常读、降级读、崩溃恢复和全盘恢复等场景下均保持高性能。

**技术启示**：
- Zone Append虽然释放了设备内并行写能力，但地址管理的不确定性对上层RAID设计构成根本性挑战，需要在"并行度"和"确定性"之间做精巧权衡。
- 分组粗粒度数据布局是应对Zone Append不确定性的关键设计模式——以牺牲少量空间效率换取极大的元数据简化和条带管理便利性。
- ZNS SSD的RAID方案需要同时考虑正常路径和恢复路径的性能，ZapRAID在降级读和全盘恢复上的性能保持证明了其设计的完备性。
- 该工作展示了传统RAID概念在新型存储接口下的适应性重构，对ZNS SSD在企业级存储中的部署有直接指导意义。

**论文覆盖率说明**：基于arXiv预印本全文（v2, 2025年2月）进行详细分析。

---

### 1.3 HLN-Tree：面向大叶节点的内存高效B+树

**论文标题**：HLN-Tree: A Memory-efficient B+-Tree with Huge Leaf Nodes and Locality Predictors
**作者**：Reza Salkhordeh, Andre Brinkmann
**发表信息**：ACM Transactions on Storage, Vol. 21, No. 2, 2025（共27页）
**机构**：Institute of Computer Science, Johannes Gutenberg University Mainz（德国美因茨大学）

**技术概要**：

B+树作为数据库和文件系统的核心索引结构，其节点大小直接影响I/O效率和缓存性能。传统B+树通常采用4KB-64KB的节点大小以匹配存储设备的块/页粒度。然而随着SSD顺序访问带宽的持续增长和NVMe协议延迟的降低，更大节点（MB级别）可能通过更好的顺序访问局部性获得性能优势。HLN-Tree提出了一种支持超大叶节点（Huge Leaf Nodes, HLN）的内存高效B+树设计。核心创新包括：(1) 局部性预测器（Locality Predictors），利用机器学习技术预测键值访问模式，指导数据在超大叶节点内的布局优化；(2) 内存高效的分层节点内索引结构，避免将完整叶节点加载到内存中；(3) 自适应节点分裂与合并策略，根据访问模式动态调整节点粒度。实验表明HLN-Tree在扫描密集型工作负载下性能显著优于传统B+树。

**技术启示**：
- SSD顺序带宽的持续增长正在改变传统索引结构的优化方向——从"减少I/O次数"转向"利用大规模顺序I/O带宽"。
- 将机器学习用于索引结构的访问预测是一种值得关注的设计范式，可降低传统启发式策略的不确定性。
- 大叶节点的核心挑战不在于存储层面，而在于内存缓存效率——如何在有限内存中高效管理超大节点是设计关键。
- 该工作暗示了存储硬件演进对经典数据结构设计的反哺作用。

**论文覆盖率说明**：基于NSTL收录信息和作者主页进行概括。

---

### 1.4 WALSH：面向混合内存的写聚合日志结构哈希索引

**论文标题**：WALSH: Write-Aggregating Log-Structured Hashing for Hybrid Memory
**作者**：Yubo Liu, Yongfeng Wang, Zhiguang Chen, Yutong Lu, Ming Zhao
**发表信息**：ACM Transactions on Storage, Vol. 21, No. 2, Article 13, 2025（共26页）
**机构**：Sun Yat-sen University（中山大学）/ Huawei OS Kernel Lab / Arizona State University

**技术概要**：

持久内存（PM）与DRAM的混合内存架构为构建高性能持久化索引提供了新机遇。然而现有PM哈希索引面临双重挑战：(1) PM的写延迟虽低于SSD但仍显著高于DRAM，高频随机小写入造成性能瓶颈；(2) PM的读写不对称性（读快写慢）使得传统针对DRAM优化的哈希结构不再最优。WALSH提出了一种写聚合日志结构哈希索引，核心设计包括：在DRAM中维护写缓冲区，聚合多个小写入为批量日志追加操作写入PM；采用日志结构布局以匹配PM的顺序写偏好；通过精心设计的一致性协议确保崩溃后DRAM缓冲数据的可恢复性。WALSH在混合DRAM-PM平台上实现了接近纯DRAM哈希的读性能，同时将写放大降低了3-5倍。

**技术启示**：
- 混合内存架构下，"写聚合+批量持久化"是弥合DRAM和PM性能差距的有效策略。
- 日志结构布局天然适合PM的访问特性（偏好顺序写、避免就地更新），值得在更多持久化数据结构中推广。
- 混合内存索引的正确性依赖于DRAM写缓冲和PM持久化之间的崩溃一致性协议设计，这是系统的正确性基石。
- PM正在从独立设备（如Optane DC PMM）向CXL附加内存演进，WALSH的混合内存设计理念可直接迁移至CXL内存场景。

**论文覆盖率说明**：基于作者主页、中山大学教师页面和期刊目录信息进行分析。

---

### 1.5 非易失性内存写干扰问题的重新思考

**论文标题**：From In-Place Updates to Out-of-Place Selections: Reconsidering Write Disturbance in Non-Volatile Memory
**作者**：Shuyue Zhou, Ronglong Wu, Hao Li 等
**发表信息**：ACM Transactions on Storage, Just Accepted, 2025（DOI: 10.1145/3767319）
**机构**：Shanghai Jiao Tong University (SJTU)

**技术概要**：

写干扰（Write Disturbance, WD）是非易失性内存（NVM）扩展主内存容量的关键阻碍之一。WD问题指在写入目标NVM单元时，相邻单元的存储值可能被错误翻转，导致数据损坏。传统方法通过就地更新（In-Place Updates）加错误纠正码来缓解WD，但这导致显著的性能和空间开销。本文从一个全新视角重新审视WD问题，提出"异地选择"（Out-of-Place Selections）策略：与其在写入时修复WD引起的错误，不如在写入目标单元之前，主动选择那些写干扰效应最小的物理位置进行数据放置。论文通过系统刻画不同NVM单元间的写干扰模式，建立了干扰预测模型，并据此设计了干扰感知的数据放置算法。实验表明该策略在几乎不引入额外硬件开销的情况下显著降低了WD引发的数据错误率。

**技术启示**：
- "从修复到规避"的范式转换是本文最大的创新——不再被动修复WD错误，而是主动选择不受干扰的位置写入。
- 该思路可类比SSD中的磨损均衡，但WD的物理机制不同（电磁耦合 vs. 氧化层退化），需要不同的建模和优化方法。
- 干扰预测模型的准确性是方案有效性的关键，其泛化到不同NVM技术（PCM、STT-RAM、ReRAM等）的能力值得关注。
- WD问题彰显了新型存储介质在物理层面引入的新约束，需要跨层次（器件-架构-系统）的协同优化。

**论文覆盖率说明**：基于ACM DL的Just Accepted摘要信息进行概括。

---

### 1.6 HyTorC：支持压缩的混合地址转换SSD

**论文标题**：HyTorC: Hybrid Address Translation for SSDs supporting Compression
**作者**：Yu Zhang, Renhai Chen, Gong Zhang 等
**发表信息**：ACM Transactions on Storage, Just Accepted, 2025（Open Access, DOI: 10.1145/3767335）
**机构**：Tianjin University, Huawei Technologies, Tsinghua University

**技术概要**：

高容量SSD（预期达1PB及以上）将进入此前由磁盘主导的云存储和归档环境。这些应用场景对数据压缩需求强烈，然而传统SSD的FTL基于固定大小的逻辑-物理地址映射，无法高效支持变长的压缩数据管理。HyTorC提出了一种混合地址转换方案，同时支持压缩和非压缩数据的统一管理。核心设计包括：(1) 混合页表结构，为压缩数据和非压缩数据分别维护不同粒度的地址映射；(2) 压缩感知的垃圾回收策略，在回收过程中保留压缩增益；(3) I/O路径上的在线压缩/解压流水线，最小化压缩引入的延迟开销。HyTorC在高压缩率工作负载上将有效存储容量提升了2-3倍，同时保持了与传统SSD相当的读写性能。

**技术启示**：
- SSD内置压缩是提升容量成本比的关键技术路径，但FTL必须从固定块映射升级为变长映射才能高效支持。
- 压缩引入的变长数据块对垃圾回收和磨损均衡提出了新挑战，需要压缩感知的系统设计。
- 随着QLC/PLC闪存的普及，SSD的原始容量与有效容量之间的差距可以通过透明压缩弥补。
- 该方向与计算存储（Computational Storage）存在自然交集——压缩/解压的硬件加速可与近存储计算结合。

**论文覆盖率说明**：基于ACM DL的Just Accepted摘要信息进行概括。

---

## 2. 分布式与云存储

### 2.1 Project Silica：面向可持续云归档存储的玻璃介质系统

**论文标题**：Project Silica: Towards Sustainable Cloud Archival Storage in Glass
**作者**：Patrick Anderson, Erika Aranas 等（Microsoft Research Cambridge团队）
**发表信息**：ACM Transactions on Storage, Vol. 21, No. 1, 2025（共31页）
**机构**：Microsoft Research Cambridge（微软剑桥研究院）

**技术概要**：

Project Silica是微软研究院历时多年的颠覆性存储项目，旨在用石英玻璃代替磁带和硬盘作为长期归档存储介质。该系统利用飞秒激光在石英玻璃内部以三维体素（voxel）形式写入数据，通过多层多级编码方案实现极高存储密度。每片DVD大小（12cm×12cm×2mm）的玻璃可存储超7TB数据，密度约为每平方英寸1.75TB。读取采用偏振显微镜结合卷积神经网络进行图像处理和解码，纠错使用类似5G网络的LDPC码。2026年2月发表在Nature的更新论文已将单块容量提升至4.84TB，室温下数据稳定保存超1万年。当前瓶颈在于写入速度较低（约8.25 MB/s），使其仅适用于WORM（写一次读多次）场景。Silica系统采用机器人库架构，玻璃片存储无需受控环境（不像磁带需要恒温恒湿），且无需定期介质迁移，具有显著的环境可持续性优势。

**技术启示**：
- Project Silica代表了存储技术从"容量密度"到"时间密度"的范式转移——追求千年级数据保存而非单纯的每TB最低成本。
- 写入速率是制约玻璃存储从归档走向通用存储的关键瓶颈，但飞秒激光技术的进步和并行写入可能逐步缓解。
- 该技术在文化遗产保护、科学数据归档、法规遵从等场景具有独特的价值主张，其TCO优势随存储时间增长而扩大。
- 微软将该技术与Azure云存储结合的战略意图明确——玻璃存储可能成为超大规模云归档层的终极方案。
- 从存储系统研究角度看，Project Silica示范了"介质-硬件-软件-服务"全栈协同设计的必要性。

**论文覆盖率说明**：基于TOS期刊摘要、Nature论文公开报道和微软官方技术博客综合分析。

---

### 2.2 基于分离式持久内存的非对称文件系统

**论文标题**：Achieving Both Performance and Reliability in An Asymmetric File System on Disaggregated Persistent Memory
**作者**：Miao Cai, Junru Shen, Baoliu Ye
**发表信息**：ACM Transactions on Storage, Just Accepted, August 2025（DOI: 10.1145/3760403）
**机构**：Nanjing University of Aeronautics and Astronautics (NUAA)

**技术概要**：

分离式（Disaggregated）持久内存是数据中心资源池化的重要趋势——计算节点通过网络访问独立的PM池，实现内存资源的弹性分配。然而，本文揭示了一个此前被忽视的级联问题：在分离式PM环境中，现有的PM文件系统设计同时面临性能和可靠性退化。性能方面，网络延迟使得PM的低延迟优势被稀释；可靠性方面，网络分区和节点故障使得传统的PM一致性协议失效。本文提出了一种非对称文件系统架构，通过在客户端和PM服务端之间进行非对称的功能分布——将性能关键的元数据操作下沉至PM端本地执行，将数据路径优化放到客户端——同时在两端维护互补的一致性状态。实验表明该设计在分离式PM环境中恢复了接近本地PM的读写性能，并在网络故障下保证了数据可靠性。

**技术启示**：
- 分离式PM文件系统的核心矛盾在于：PM的低延迟优势在跨越网络后是否仍能保持。本文证明了通过合理的功能分布可以达到"鱼与熊掌兼得"。
- "非对称"设计是分布式存储系统的通用模式——计算密集与I/O密集操作需要不同的优化策略和部署位置。
- 随着CXL 3.0支持跨机架内存共享，分离式PM的研究将从实验室走向生产环境，可靠性和可恢复性成为首要问题。
- 该方向与当前CXL内存池化的产业趋势高度契合，具有显著的实践指导意义。

**论文覆盖率说明**：基于ACM DL的Just Accepted摘要信息进行概括。

---

### 2.3 eBPF驱动的半虚拟化存储I/O优化

**论文标题**：A Tale of Two Paths: Optimizing Paravirtualized Storage I/O with eBPF
**作者**：Li Wang, Shi Qiu 等
**发表信息**：ACM Transactions on Storage, Just Accepted, August 2025（DOI: 10.1145/3760404）
**机构**：Shanghai Jiao Tong University (SJTU)

**技术概要**：

KVM是Linux上主导的虚拟机管理程序，依赖QEMU实现virtio-blk等半虚拟化设备后端。然而KVM/QEMU架构拖长了客户机I/O路径——I/O请求需要经过"客户机内核→QEMU用户态→宿主机内核→物理设备"的长链路，引入了显著的上下文切换和数据拷贝开销。本文提出利用eBPF技术优化virtio-blk的I/O路径，核心思想是将关键路径上的I/O处理逻辑下沉到宿主机内核的eBPF程序中执行，从而绕过QEMU用户态的多次上下文切换。论文设计了双路径架构：快速路径通过eBPF直接在内核中处理简单I/O请求（如顺序读写），慢速路径回退到QEMU处理复杂操作（如TRIM/DISCARD）。实验表明eBPF加速路径将虚拟机I/O延迟降低了40-60%，吞吐量提升了2-3倍。

**技术启示**：
- eBPF正在从网络/安全领域向存储I/O栈渗透，其"安全地将用户逻辑注入内核"的能力正在改变传统的内核旁路策略（如SPDK）。
- KVM/QEMU的I/O路径冗长是业界公认的性能瓶颈，eBPF方案的优势在于无需修改虚拟机内核或更换hypervisor。
- 双路径设计体现了系统优化的务实原则——不求在所有场景下最优，而是为常见场景提供极大加速，为异常场景保持兼容。
- 该技术对未来CXL下的虚拟化I/O栈设计有潜在影响——eBPF可能成为统一内核可编程I/O加速的通用框架。

**论文覆盖率说明**：基于ACM DL的Just Accepted摘要信息进行概括。

---

### 2.4 应用引导的OS页面缓存管理

**论文标题**：P2Cache: Enhancing Data-Centric Applications via Application-Guided Management of OS Page Caches
**作者**：Dusol Lee, Inhyuk Choi 等
**发表信息**：ACM Transactions on Storage, Just Accepted, June 2025（Open Access, DOI: 10.1145/3736586）
**机构**：Seoul National University

**技术概要**：

以数据为中心的应用（如数据库、大数据分析框架）执行需要密集数据处理和大量内存资源的任务。这些任务具有差异化的I/O访问模式，而OS页面缓存的"一刀切"管理策略（LRU或LRU变体）常常与应用的实际需求错配——应用比OS更清楚哪些数据将被重用、哪些是一次性扫描。P2Cache提出了一种应用引导的OS页面缓存管理框架，通过暴露给应用的缓存提示（cache hint）接口，允许应用显式标注数据页的预期重用模式。OS内核基于这些提示动态调整缓存替换策略——例如，数据库的WAL页面可被标记为"尽快淘汰"，而索引页面可被标记为"长期保留"。实验表明P2Cache在典型数据库和大数据工作负载上将缓存命中率提升了15-30%。

**技术启示**：
- "应用知道但内核不知道"是经典的信息不对称问题，P2Cache通过轻量级API弥合了这一语义鸿沟。
- 应用引导的缓存管理与Multi-Stream SSD、FDP等SSD端的提示机制形成互补——两者分别在OS层和设备层实现感知优化。
- 该思路可扩展到更多OS资源管理场景（预取、I/O调度），形成以应用为中心的OS资源管理范式。
- 安全隔离是需要关注的问题——应用提供的缓存提示不能被恶意利用来干扰其他应用的缓存空间。

**论文覆盖率说明**：基于ACM DL的Just Accepted摘要信息进行概括。

---

## 3. 存储安全与可靠性

### 3.1 SrFTL：利用存储语义的闪存勒索软件防御

**论文标题**：SrFTL: Leveraging Storage Semantics for Effective Ransomware Defense in Flash-based SSDs
**作者**：Weidong Zhu, Grant Hernandez 等
**发表信息**：ACM Transactions on Storage, Just Accepted, 2025（DOI: 10.1145/3767322）
**机构**：Florida International University

**技术概要**：

勒索软件攻击日益频繁，每年造成数十亿美元的数据和运营损失。现有防御机制主要部署在操作系统层，但一旦OS被攻破，这些防御也随即失效。在存储设备（SSD）中实施防御可以避开OS漏洞，但现有FTL级方案（如MimosaFTL）因无法访问文件系统语义（如文件名、目录结构、文件类型）而导致检测准确性低下。SrFTL通过在SSD的FTL层嵌入可信执行环境（TEE），建立从FTL到文件系统元数据的安全语义通道，使SSD能在获取文件级语义的同时保持防御组件的完整性和真实性。SrFTL在TEE中部署了勒索软件分类器和数据恢复引擎，实现了零误报/漏报的检测准确率。更关键的是，SrFTL利用FTL对闪存物理页的管理能力实现了高效的文件级数据恢复——平均恢复时间仅9.3秒，远优于传统备份恢复方案。性能开销仅为1.5%。

**技术启示**：
- "从OS层下沉到存储层"是勒索软件防御的重要范式迁移——存储设备具有独立于OS的信任根，天然抗OS级攻击。
- 弥合"FTL块级语义"与"文件系统文件级语义"之间的差距是实现精准检测的关键——SrFTL的安全语义通道设计值得关注。
- 该工作展示了存储安全从"静态防护"（加密、访问控制）向"动态检测与恢复"演进的大趋势。
- 9.3秒的文件级恢复时间具有极高的实用价值，有望推动SSD内置安全防御能力的产业化。

**论文覆盖率说明**：基于中文新闻媒体的详细论文报道和ACM DL摘要信息综合分析。

---

### 3.2 HBM错误揭秘：回顾历史以预测未来故障

**论文标题**：Looking Back to Move Forward: Unveiling the Mysteries of HBM Errors to Predict Future Failures
**作者**：Shuyue Zhou, Xinbin Hu, Ronglong Wu 等
**发表信息**：ACM Transactions on Storage, Just Accepted, 2025（DOI: 10.1145/3767333）
**机构**：Shanghai Jiao Tong University (SJTU)

**技术概要**：

高带宽内存（HBM）通过垂直堆叠多层DRAM芯片大幅提升了内存访问带宽，被视为突破"内存墙"的关键技术。然而HBM独特的3D堆叠结构和更高的热密度引入了新的故障模式，其错误特征与传统的DDR DRAM有本质不同。本文首次对HBM的错误模式进行了大规模实证研究，分析了来自生产环境的HBM错误日志。关键发现包括：(1) HBM错误呈现出强烈的空间和时间局部性，相邻堆叠层之间的错误高度相关；(2) 温度是HBM错误率的最主要影响因素，其影响超过电压波动和访问模式；(3) HBM的"软错误"和"硬错误"边界模糊，许多初始表现为软错误的故障最终发展为永久性硬件故障。基于这些发现，论文构建了HBM故障预测模型，可以提前数小时至数天预警HBM的即将失效。

**技术启示**：
- HBM的错误特征与DDR DRAM存在根本性不同，不能简单复用传统的DRAM错误模型和容错机制。
- 3D堆叠结构引入了独特的层间依赖故障模式——一层失效可能预示相邻层的高风险，这为预测性维护提供了物理基础。
- 温度作为第一影响力的发现对数据中心冷却设计和HBM部署策略有直接指导意义。
- 该研究填补了HBM可靠性领域的关键实证空白，对AI训练集群（HBM的最大消费场景）的可靠性工程具有重要参考价值。

**论文覆盖率说明**：基于ACM DL的Just Accepted摘要信息进行概括。

---

### 3.3 Argus：面向后去重Delta压缩的精确相似性检测

**论文标题**：Argus: A Precise and Efficient Resemblance Detection for Post-Deduplication Delta Compression
**作者**：Han Xu, Xiangyu Zou 等
**发表信息**：ACM Transactions on Storage, Just Accepted, July 2025（Open Access, DOI: 10.1145/3747839）
**机构**：Harbin Institute of Technology (HIT)

**技术概要**：

数据缩减是存储系统的核心优化技术。在实际部署中，Delta压缩通常在去重之后执行——首先通过去重消除完全相同的块，然后通过Delta压缩发现和压缩高度相似但不完全相同的块。然而，现有Delta压缩的相似性检测技术（如基于特征指纹的近似匹配）在去重后的数据上表现不佳——因为去重已经消除了完全相同的数据块，剩余数据块之间的相似性更加微妙和隐蔽。Argus提出了一种精确且高效的相似性检测方法，专为去重后的Delta压缩场景设计。核心创新包括：(1) 多粒度特征提取，从多个粒度级别捕捉数据块的结构相似性；(2) 基于局部敏感哈希（LSH）的相似性快速筛选机制，减少不必要的精确比较；(3) 压缩收益感知的Delta对选择策略，避免对压缩收益不足以覆盖计算开销的块对进行Delta压缩。Argus在后去重场景中实现了比现有方案高2-3倍的压缩率。

**技术启示**：
- "去重+Delta压缩"的组合在备份和归档存储中广泛部署，但两者之间的协同优化尚不充分，Argus填补了这一空白。
- 相似性检测是Delta压缩的计算瓶颈，LSH和Bloom Filter等概率数据结构的融合是加速该过程的有效手段。
- 压缩收益感知的选择策略体现了"实用性优先"的设计哲学——不是所有可压缩的数据都值得压缩。
- 随着AI训练数据的爆炸式增长（多个版本的数据集通常高度相似），Delta压缩在ML数据管理中的应用前景广阔。

**论文覆盖率说明**：基于ACM DL的Just Accepted摘要信息进行概括。

---

### 3.4 边缘设备不可纠正闪存错误下的CNN模型优雅降级

**论文标题**：Graceful CNN Model Degradation in Uncorrected Flash Storage for Embedded Edge Devices
**作者**：Hung-Yi Chen, Jin-Wei Chang 等
**发表信息**：ACM Transactions on Storage, Just Accepted, July 2025（DOI: 10.1145/3747298）
**机构**：National Yang Ming Chiao Tung University (NYCU)

**技术概要**：

边缘智能设备（如IoT传感器、无人机、嵌入式视觉系统）依赖本地闪存存储CNN模型参数。然而边缘设备的闪存因成本限制通常缺乏企业级的纠错能力（如LDPC），导致不可纠正的比特错误（Uncorrectable Bit Errors）率较高。传统方法将比特错误视为灾难性故障，要求模型重新加载或设备返修。本文提出了一个反直觉的思路：CNN模型天然具有一定的容错性，与其在存储层面追求完美纠错，不如让CNN推理引擎"优雅地容忍"存储错误。论文首先对CNN模型参数中比特错误的影响进行了系统表征——发现不同层、不同位置的参数对错误的敏感度差异达数个数量级。基于这一发现，论文设计了错误感知的模型部署策略：将关键参数存储在更可靠的闪存页中，将容错参数放置在普通页中，并在推理时引入轻量级错误检测机制。实验表明该方案在不增加硬件纠错成本的前提下，将CNN推理精度从随机错误下的严重退化恢复到接近无错误水平。

**技术启示**：
- "应用容错"与"存储纠错"的跨层次协同是边缘计算场景下的有效优化策略。
- CNN模型的参数重要性存在极大的非均匀分布——利用这一特性进行差异化存储管理是本文的核心洞察。
- 该研究体现了"近似计算"（Approximate Computing）思想在存储系统中的延伸应用。
- 对于其他在边缘设备上运行的DNN模型类型（Transformers、RNNs），该方法的迁移性值得进一步探索。

**论文覆盖率说明**：基于ACM DL的Just Accepted摘要信息进行概括。

---

## 4. 结语与未来方向

### 4.1 年度关键趋势总结

2025–2026年度的ACM TOS论文呈现出以下五大核心趋势：

**趋势一：存储接口从"黑盒"走向"白盒"**。ZNS SSD、FDP、计算存储等技术的成熟标志着存储设备正在从"隐藏内部细节的块设备"转变为"向主机暴露内部并行性和可管理性的协作设备"。ZapRAID、WALSH等工作展示了应用如何利用这些新接口实现性能突破。

**趋势二：存储层次结构在AI时代加速重构**。HBM的错误特征研究、混合内存哈希索引、分离式PM文件系统等工作都反映了内存/存储层次正在经历深刻变革。CXL作为统一互连协议，将成为连接DRAM、PM、SSD等异构存储层的关键基础设施。

**趋势三：存储安全进入"主动检测+快速恢复"时代**。SrFTL在SSD固件中嵌入勒索软件检测代表了存储安全的重要进化方向——存储不再仅仅是加密和备份的目标，而是成为安全防御的主动参与者。

**趋势四：可持续性成为存储系统设计的新维度**。Project Silica玻璃存储以"千年保存"为设计目标，重新定义了存储可持续性的内涵。从碳足迹到介质寿命，可持续性正成为与性能、成本并列的存储系统评价维度。

**趋势五：AI既是存储的消费者也是存储的优化者**。一方面，大模型训练和推理的KV缓存成为新的存储瓶颈；另一方面，CNN模型容错部署、数据缩减中的ML辅助等方法展示了AI技术反哺存储系统优化的潜力。

### 4.2 未来研究展望

基于对论文的分析，以下方向值得中国存储研究者关注：

1. **CXL原生存储系统**：CXL 3.0支持跨机架内存共享和池化，围绕CXL构建原生存储系统（文件系统、KV存储、数据库）将是重要方向。
2. **面向AI推理的存储优化**：LLM推理中的KV缓存管理已成为存储系统的新前沿，如何在容量、带宽、延迟之间取得最优平衡是有价值的研究问题。
3. **存储与安全的深度融合**：在设备层、固件层实现安全能力的嵌入，构建从介质到应用的全栈存储安全体系。
4. **新型存储介质的系统适配**：玻璃存储、DNA存储等新型介质从实验室走向工程化部署的过程中，需要大量系统层面的创新。
5. **数据缩减与计算的协同**：在数据压缩/去重的基础上与近存储计算结合，实现"先压缩再计算"或"边压缩边计算"的新范式。

---

## 论文索引表

| 编号 | 论文标题 | 作者（代表） | 发表信息 | 核心主题 |
|------|----------|-------------|----------|----------|
| 1 | Storage Abstractions for SSDs: The Past, Present, and Future | Xiangqun Zhang, Janki Bhimani 等 | TOS Vol.21(1), 2025 | SSD接口演进综述 |
| 2 | ZapRAID: A High-Performance Log-Structured RAID System for ZNS SSDs | Jinhong Li, Qiuping Wang, Shujie Han, Patrick P. C. Lee | TOS 2025 (arXiv:2402.17963) | ZNS SSD RAID系统 |
| 3 | HLN-Tree: A Memory-efficient B+-Tree with Huge Leaf Nodes and Locality Predictors | Reza Salkhordeh, Andre Brinkmann | TOS Vol.21(2), 2025 | 大叶节点B+树 |
| 4 | WALSH: Write-Aggregating Log-Structured Hashing for Hybrid Memory | Yubo Liu, Yongfeng Wang, Zhiguang Chen, Yutong Lu, Ming Zhao | TOS Vol.21(2), Art.13, 2025 | 混合内存哈希索引 |
| 5 | From In-Place Updates to Out-of-Place Selections: Reconsidering Write Disturbance in NVM | Shuyue Zhou, Ronglong Wu, Hao Li 等 | TOS Just Accepted, 2025 | NVM写干扰缓解 |
| 6 | HyTorC: Hybrid Address Translation for SSDs supporting Compression | Yu Zhang, Renhai Chen, Gong Zhang 等 | TOS Just Accepted, 2025 | SSD透明压缩 |
| 7 | Project Silica: Towards Sustainable Cloud Archival Storage in Glass | Patrick Anderson, Erika Aranas 等 (Microsoft) | TOS Vol.21(1), 2025 | 玻璃介质归档存储 |
| 8 | Achieving Both Performance and Reliability in An Asymmetric File System on Disaggregated PM | Miao Cai, Junru Shen, Baoliu Ye | TOS Just Accepted, Aug 2025 | 分离式PM文件系统 |
| 9 | A Tale of Two Paths: Optimizing Paravirtualized Storage I/O with eBPF | Li Wang, Shi Qiu 等 | TOS Just Accepted, Aug 2025 | eBPF虚拟化I/O优化 |
| 10 | P2Cache: Enhancing Data-Centric Applications via Application-Guided Management of OS Page Caches | Dusol Lee, Inhyuk Choi 等 | TOS Just Accepted, Jun 2025 | 应用引导页面缓存 |
| 11 | SrFTL: Leveraging Storage Semantics for Effective Ransomware Defense in Flash-based SSDs | Weidong Zhu, Grant Hernandez 等 | TOS Just Accepted, 2025 | SSD勒索软件防御 |
| 12 | Looking Back to Move Forward: Unveiling the Mysteries of HBM Errors to Predict Future Failures | Shuyue Zhou, Xinbin Hu, Ronglong Wu 等 | TOS Just Accepted, 2025 | HBM错误预测 |
| 13 | Argus: A Precise and Efficient Resemblance Detection for Post-Deduplication Delta Compression | Han Xu, Xiangyu Zou 等 | TOS Just Accepted, Jul 2025 | 数据缩减优化 |
| 14 | Graceful CNN Model Degradation in Uncorrected Flash Storage for Embedded Edge Devices | Hung-Yi Chen, Jin-Wei Chang 等 | TOS Just Accepted, Jul 2025 | 边缘CNN容错存储 |

---

*注：标记为"Just Accepted"的论文在报告撰写时尚未正式分配卷号。部分论文的作者机构和详细技术参数以最终出版的Version of Record为准。本报告基于公开可获取的信息进行学术性综述，如有纰漏请以ACM Digital Library原文为准。*