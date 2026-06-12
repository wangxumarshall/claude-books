# PPoPP 2026 洞察报告

> **会议全称**：ACM SIGPLAN Symposium on Principles and Practice of Parallel Programming  
> **会议简称**：PPoPP 2026（第31届）  
> **CCF等级**：A类（计算机体系结构/并行与分布计算/存储系统）  
> **时间地点**：2026年1月31日–2月4日，澳大利亚悉尼  
> **投稿/录用**：280篇投稿，51篇录用，录用率 **18.2%**  
> **联合举办**：与 HPCA / CGO / CC 2026 联合在悉尼国际会议中心 (ICC Sydney) 举办

---

## 0. 会议概览

### 0.1 会议定位

PPoPP 是并行编程与高性能计算领域公认的顶级会议（CCF-A类），涵盖并行编程理论基础、语言设计、编译器优化、运行时系统、调试与性能分析工具、并行算法、并发数据结构、GPU与加速器计算、分布式与集群系统等核心方向。近年来，随着大语言模型（LLM）训练的爆发式增长，PPoPP 日益成为 AI 系统/Infra 研究的核心发表阵地之一。

### 0.2 PPoPP 2026 概览

PPoPP 2026 共收到 280 篇投稿，最终录用 51 篇，录用率 18.2%，延续了该会一贯的高选择标准。会议在悉尼与 HPCA、CGO、CC 三大会议共同举办，为期5天（含2天 Workshop & Tutorial），主会论文报告集中在周一至周三。

本届会议设有三场 **Plenary Keynote**：
- **Saman Amarasinghe (MIT)**：*"Compiler 2.0: Building the Next Generation Compilers with Machine Learning"*
- **Cristina Cifuentes (Oracle)**：*"Oracle Parfait – Scaling Vulnerability Detection from Enterprise Systems to Cloud-Scale Systems and Beyond"*
- **Sudhanva Gurumurthi (AMD)**：*"Architecting Resilience at Scale: From Research to Practice"*

### 0.3 奖项一览

| 奖项 | 论文标题 | 作者机构 |
|------|---------|---------|
| **Best Paper Award** | Binary Compatible Critical Section Delegation | Junyao Zhang, Zhuo Wang (Alibaba), Zhe Zhou (Fudan) |
| **Best Artifact Award** | HierCut: Enabling 16-bit Format Mixed Precision for Molecular Dynamics through Hierarchical Cutoff | Zeyu Song, Lin Gan et al. (Tsinghua) |
| **Best Paper Nominee** | Rethinking Thread Scheduling under Oversubscription | Aleix Roca, Vicenç Beltran (BSC) |
| **Best Paper Nominee** | UFO Trees: Practical and Provably-Efficient Parallel Batch-Dynamic Trees | Quinten De Man et al. (UMD) |
| **Best Paper Nominee** | Trojan Horse: Aggregate-and-Batch for Scaling Up Sparse Direct Solvers on GPU Clusters | Yida Li et al. (CUPB) |
| **Best Paper Nominee** | PRISM: An Efficient GPU-Based Lossy Compression Framework | Bing Lu, Zedong Liu, Dingwen Tao et al. (ICT CAS) |
| **Best Paper Nominee** | CCL-D: A High-Precision Diagnostic System for Slow and Hang Anomalies in Large-Scale Model Training | Yida Gu, Dingwen Tao et al. (ICT CAS) |

---

## 1. 并发控制与内存管理

### 1.1 概况

并发控制是 PPoPP 的传统核心议题。本届会议该方向包含 4 篇论文，涵盖临界区委托、互斥锁、无阻塞数据结构的 SMR 兼容性、事务内存等技术点。

### 1.2 重点论文

#### ★ Binary Compatible Critical Section Delegation（最佳论文奖）

- **作者**：Junyao Zhang (Fudan University), Zhuo Wang (Alibaba Group), Zhe Zhou (Fudan University)
- **关键词**：Critical Section Delegation, Binary Compatibility, Lock Optimization
- **发表信息**：PPoPP 2026, ACM SIGPLAN | DOI: 10.1145/3694906.3743347

### 技术概要

临界区（Critical Section）是多线程程序中保护共享数据一致性的核心同步机制，但传统的锁实现在高竞争场景下会成为严重的性能瓶颈——多个线程争抢同一把锁时，大量CPU时间被浪费在自旋等待或上下文切换上。现有的高性能锁优化方案（如锁委托、锁消除、事务内存等）通常需要修改应用程序源码或依赖编译器支持，这在阿里巴巴等大规模生产环境中不可接受——数十亿行遗留代码无法逐一修改。此外，锁委托机制还需要修改二进制文件的ABI（Application Binary Interface），与现有部署流水线不兼容。

本文提出二进制兼容的临界区委托（Binary Compatible Critical Section Delegation）机制，其核心创新在于无需修改应用程序二进制文件即可将临界区执行委托给专用核心。技术方案包括：(1) 通过动态二进制插桩（DBI）在运行时识别热点临界区，将其执行重定向到专用的delegate core上；(2) 设计高效的跨核通信机制，利用共享内存和轻量级信号实现委托请求的快速提交和结果返回；(3) 提出自适应的委托决策算法，根据运行时竞争强度动态决定是否启用委托。论文在阿里巴巴的生产环境中进行了完整实现与评估，在多个高竞争工作负载上实现了显著的性能提升，展示了工业级并发优化的前沿水准。该工作获得PPoPP 2026最佳论文奖。

> **信息来源**：PPoPP 2026 官方程序 | conference-publishing.com

#### Fixing Non-blocking Data Structures for Better Compatibility with Memory Reclamation Schemes

- **作者**：Md Amit Hasan Arovi, Ruslan Nikolaev (Pennsylvania State University)
- **关键词**：Safe Memory Reclamation, SCOT, Optimistic Traversal, Hazard Pointers
- **发表信息**：PPoPP 2026, ACM SIGPLAN | arXiv:2504.06254

### 技术概要

无锁（Non-blocking）并发数据结构通过乐观遍历（optimistic traversals）实现高吞吐的并发访问——线程在遍历时不加锁，仅在修改时通过CAS操作检测冲突。然而，这种乐观遍历与安全内存回收（Safe Memory Reclamation, SMR）方案之间存在根本性兼容问题：当一个线程正在遍历某个节点时，另一个线程可能已经释放了该节点的内存，导致悬挂指针（dangling pointer）。现有的健壮SMR方案——如Hazard Pointers (HP)、Hazard Eras (HE)、Interval-Based Reclamation (IBR)、Hyaline——能够防止停滞线程（stalled threads）引发的ABA问题，但它们与经典的乐观遍历数据结构（如Harris链表、Natarajan-Mittal树）不兼容，或者需要修改数据结构导致性能下降。而Epoch-Based Reclamation (EBR)虽然兼容性好但无法防护停滞线程，在生产环境中存在安全隐患。

本文提出SCOT（Safe Concurrent Optimistic Traversals）技术，在不修改现有SMR方案的前提下解决了乐观遍历与健壮SMR方案的兼容性问题。SCOT的核心思路是修改数据结构本身而非SMR方案：通过在节点中嵌入额外的元数据（如版本号），使得乐观遍历能够在不依赖SMR保护的情况下安全地检测到已被回收的节点。SCOT保持了原有SMR方案的完整性，同时保留了原始数据结构的性能优势。实验表明，SCOT使Harris链表和NM树在HP/HE/IBR/Hyaline等健壮SMR方案下实现了与此前仅EBR用户可享的同等性能加速，NM树的吞吐量达到了EBR级别的实用上界。

> **信息来源**：arXiv:2504.06254 摘要

#### Hapax Locks: Scalable Value-Based Mutual Exclusion

- **作者**：Dave Dice (Independent), Alex Kogan (Oracle Labs)
- **关键词**：Value-Based Mutual Exclusion, Scalable Locks
- **发表信息**：PPoPP 2026, ACM SIGPLAN, pp.13-25 | arXiv:2511.14608

### 技术概要

互斥锁是多线程编程中最基本的同步原语，但现有锁算法在高竞争场景下面临两难困境：基于MCS/Ticket的队列锁保证了FIFO公平性但unlock路径需要O(N)时间遍历等待队列；基于Malthian/Array的锁实现了常数时间操作但牺牲了公平性或引入了大量缓存一致性流量。此外，许多高性能锁方案需要在锁结构和等待节点之间传递指针或转移所有权，对运行时环境提出了特定要求（如GC兼容性、线程本地存储等），限制了其在现有系统中的可集成性。

Hapax Locks提出了一种新型的基于值（Value-Based）的互斥锁算法，同时实现了简单性、常数时间到达和解锁路径、FIFO准入顺序以及空间效率。核心创新在于：不使用传统的指针链表或数组结构，而是通过值传递（而非指针传递）实现等待队列的管理——等待线程将自己的标识值写入共享结构，而非传递指向本地节点的指针。这意味着没有指针在进程间移动或逃逸所有权，大幅减少了缓存一致性协议（MESI等）下的缓存行失效风暴。在常见竞争情况下，Hapax Locks产生的一致性流量显著少于MCS等经典方案。实验表明其性能（延迟和可扩展性）可与最佳SOTA锁媲美，同时对运行时环境的约束和依赖更少，特别适合集成或改造到现有系统中。

> **信息来源**：arXiv:2511.14608 摘要

#### Multiverse: Transactional Memory with Dynamic Multiversioning

- **作者**：Gaetano Coccimiglio, Trevor Brown (University of Waterloo), Srivatsan Ravi (USC)
- **关键词**：Transactional Memory, Dynamic Multiversioning
- **发表信息**：PPoPP 2026, ACM SIGPLAN, pp.40-52

### 技术概要

事务内存（Transactional Memory, TM）是替代锁的乐观并发控制机制，允许多个线程原子地执行一组读写操作。然而现有TM系统在高并发读写混合场景下性能严重退化：写者频繁中止读者（因读者观察到的数据版本被写者修改），或读者阻止写者提交（因需等待所有读者完成）。多版本事务内存（MV-TM）通过维护数据的多个历史版本来缓解读写冲突，但现有MV-TM方案要么在编译时静态确定版本数量（无法适应运行时工作负载变化），要么引入高昂的版本管理开销（垃圾回收、版本链遍历等）。

Multiverse提出了动态多版本管理（Dynamic Multiversioning）技术，其核心创新在于运行时根据工作负载特征动态调整每个数据对象维护的版本数量。当检测到某个对象的读写冲突频繁时，自动增加该对象的版本数（允许更多读者并发访问不同版本）；当冲突减少时，回收多余版本以降低内存和遍历开销。Multiverse通过精心设计的版本链数据结构和无锁的版本回收算法，在保证事务正确性（序列化一致性）的前提下实现了高效的动态调整。在高并发读写混合场景下，Multiverse实现了比现有TM方案（如NOrec、TL2等）更优的性能，为事务内存在实际系统中的采用提供了新的技术路径。

> **信息来源**：PPoPP 2026 官方程序 | dblp.org

---

## 2. 任务调度与负载均衡

### 2.1 概况

包含 4 篇论文，覆盖线程过订阅调度、工作窃取、GPU 上的图搜索负载均衡、SpMV 负载均衡等方向。

### 2.2 重点论文

#### ★ Rethinking Thread Scheduling under Oversubscription（最佳论文提名）

- **作者**：Aleix Roca, Vicenç Beltran (Barcelona Supercomputing Center)
- **关键词**：Oversubscription, Thread Scheduling, Multi-runtime Coordination
- **发表信息**：PPoPP 2026, ACM SIGPLAN | arXiv:2601.20435

### 技术概要

高性能计算（HPC）与人工智能（AI）的融合正在推动日益复杂的并行应用和工作负载出现。这些工作负载通常在同一个应用中组合多个并行运行时（如OpenMP + CUDA + MPI），或在同一个节点上共存多个作业，导致就绪线程数远超物理核心数的“过订阅”（oversubscription）场景成为常态。在这种情况下，OS调度器依赖周期性抢占（如Linux CFS的10ms时间片）来多路复用核心，引入了严重的干扰问题：锁持有者抢占（LHP，持有锁的线程被抢占导致所有等待者阻塞）、锁等待者抢占（LWP，等待锁的线程被抢占导致释放锁后无法及时唤醒）、以及可扩展性崩溃（多个运行时各自为战导致全局性能急剧下降）。

本文提出了用户态调度框架（USF, User-space Scheduling Framework），完全在用户态实现无缝的进程调度，无需特殊权限。USF的核心设计包括：(1) 通过扩展GNU C库的nOS-V运行时，实现跨运行时（如OpenMP、StarSs等）的无缝协调——无需侵入式修改应用代码；(2) 默认协作策略SCHED_COOP：仅在线程阻塞时（如等待锁、等待I/O）才切换线程，从根本上消除LHP和LWP问题——因为线程不会在持锁期间被强制抢占；(3) 支持用户自定义调度算法，使应用开发者可以根据工作负载特征定制调度策略。评估显示，在过订阅多进程场景下获得最高2.4倍的性能提升，测试场景包括嵌套BLAS工作负载、多进程PyTorch推理（使用LLaMA-3模型）和分子动力学（MD）模拟。

> **信息来源**：arXiv:2601.20435 摘要

#### Waste-Efficient Work Stealing

- **作者**：Kyle Singer (MIT), Kunal Agrawal (WUSTL), Tao B. Schardl (MIT)
- **关键词**：Work Stealing, Waste Efficiency
- **发表信息**：PPoPP 2026, ACM SIGPLAN, pp.68-80

### 技术概要

工作窃取（work stealing）是并行任务调度的经典算法——空闲线程从其他线程的任务队列尾部窃取任务来执行。然而在实际运行中，工作窃取引入了大量的“浪费”操作：窃取尝试失败（队列已空）、窃取到的任务过小（执行时间低于窃取开销）、以及级联窃取（一个窃取触发更多窃取）等。这些浪费操作在高核数、不规则并行场景下尤为严重，可能占总执行时间的30%以上。现有的优化方案（如指数退避、批量窃取）虽然能减少部分浪费，但缺乏系统的理论指导，往往以牺牲负载均衡质量为代价。

本文对经典工作窃取算法进行了重新审视，提出了“浪费效率”（waste-efficient）的新概念和理论框架。核心贡献包括：(1) 形式化定义了工作窃取中的“浪费”度量——包括空窃取率、任务粒度过细率和级联窃取深度，并证明这些度量与总体效率之间的理论关系；(2) 设计了浪费效率感知的窃取策略，在窃取前评估目标队列的预期浪费，仅当预期收益超过阈值时才执行窃取；(3) 给出了在保持工作窃取简洁性（无需全局知识、去中心化）的同时显著降低无用窃取开销的理论保证。实验表明新策略在多种不规则并行工作负载上显著优于经典工作窃取和现有优化方案。

> **信息来源**：PPoPP 2026 官方程序 | dblp.org

#### DiggerBees: Depth First Search Leveraging Hierarchical Block-Level Stealing on GPUs

- **作者**：Yuyao Niu (BSC), Yuechen Lu, Weifeng Liu (CUPB), Marc Casas (BSC)
- **关键词**：GPU DFS, Hierarchical Block-Level Stealing, Graph Algorithms
- **发表信息**：PPoPP 2026, ACM SIGPLAN | DOI: 10.1145/3774934.3786457

### 技术概要

深度优先搜索（DFS）是图算法的基础原语，广泛应用于连通分量检测、拓扑排序、强连通分量识别等任务。与广度优先搜索（BFS）不同，DFS的探索路径具有高度不规则性——不同分支的深度差异可达数个数量级，导致GPU上的线程级并行效率极低。现有GPU DFS方案主要通过将未探索的邻居节点放入工作队列、由空闲warp窃取来实现负载均衡，但这种扁平化的窃取策略忽视了GPU的层级并行结构（thread-warp-block-grid），在高直径图中仍然出现严重的负载不均和同步开销。

DiggerBees提出了GPU上的层次化block级别窃取策略，核心创新在于利用GPU的三级并行结构（warp-block-grid）设计了多层窃取机制：(1) **warp内窃取**：同一warp内的线程间共享探索状态，快速平衡warp内负载；(2) **block内窃取**：同一block内的多个warp之间窃取未完成的DFS子树，利用共享内存实现低延迟窃取；(3) **grid级窃取**：不同block之间通过全局工作队列窃取大规模DFS子树。这种层次化设计确保窃取操作始终在最近的可用并行层次上执行，最小化窃取延迟和数据传输开销。在多种图基准（社交网络、Web图、道路网络）上的实验表明，DiggerBees显著优于现有GPU DFS方案。

> **信息来源**：PPoPP 2026 官方程序 | ssslab.cn PDF

#### PANA: A Fine-Grained Runtime-Adaptive Load Balancing for Parallel SpMV on Multicore CPUs

- **作者**：Haodong Bian, Youhui Zhang et al. (Tsinghua University)
- **关键词**：SpMV, Load Balancing, Runtime Adaptation, Multicore CPU
- **发表信息**：PPoPP 2026, ACM SIGPLAN

### 技术概要

稀疏矩阵-向量乘法（SpMV）是科学计算和机器学习中最基础且最频繁调用的内核之一，其性能直接影响上层应用的效率。SpMV的核心挑战在于稀疏矩阵的非零元素分布极不均匀——某些行的非零元素数量可能是其他行的数百倍——导致静态任务划分（如按行均分）产生严重的负载不均。现有动态负载均衡方案（如OpenMP dynamic scheduling）虽然能缓解不均，但引入了高昂的调度开销（每次获取任务都需原子操作），在细粒度任务场景下反而降低性能。

PANA提出了一种运行时自适应的细粒度负载均衡策略。核心创新包括：(1) 在运行时分析矩阵的非零元素分布特征（如行长度分布、block结构），自动选择最优的任务划分粒度——对于规则部分使用粗粒度静态划分（减少调度开销），对于不规则部分使用细粒度动态划分（保证负载均衡）；(2) 设计了轻量级的运行时监控机制，在SpMV执行过程中实时检测负载不均并动态调整任务分配；(3) 针对多核CPU的缓存层次结构进行了缓存感知优化，减少因任务迁移导致的缓存失效。在多种稀疏矩阵基准（SuiteSparse矩阵集合）上的实验表明，PANA在多种矩阵结构和多核配置下均优于现有方案。

> **信息来源**：PPoPP 2026 官方程序

---

## 3. 并发数据结构

### 3.1 概况

4 篇论文，涵盖动态树、并发栈、平衡增强树、空间索引等核心数据结构。

### 3.2 重点论文

#### ★ UFO Trees: Practical and Provably-Efficient Parallel Batch-Dynamic Trees（最佳论文提名）

- **作者**：Quinten De Man, Atharva Sharma, Kishen N Gowda, Laxman Dhulipala (University of Maryland)
- **关键词**：Batch-Dynamic Trees, Parallel Data Structures, Link-Cut Trees
- **发表信息**：PPoPP 2026, ACM SIGPLAN, pp.109-122 | arXiv:2601.10706

### 技术概要

动态树问题（dynamic trees problem）要求在支持边更新（插入/删除）的同时维护树的连通性、路径查询等功能，是动态图算法的核心构建块。自从40年前Sleator和Tarjan发明Link-Cut树以来，这一经典数据结构在串行场景下仍是最快的动态树方案。然而Link-Cut树存在两个关键限制：(1) 不支持并行批量动态更新——当需要同时插入/删除多条边时，只能串行执行，无法利用多核并行性；(2) 支持的查询功能有限——某些高级查询（如子树聚合、路径统计）需要额外的数据结构辅助。现有的并行批量动态树方案（如Parallel Euler Tour Trees）虽然支持批量更新，但在查询功能范围或实际性能上不如Link-Cut树。

UFO Trees设计了一种新的并行批量动态树数据结构，同时实现了三大目标：(1) **广泛的查询功能**——支持连通性、路径查询、子树聚合等多种查询；(2) **工作高效的并行批量更新**——批量插入/删除k条边的工作复杂度为O(k log n)，可利用多核并行执行；(3) **串行竞争力**——单线程执行时性能可与Link-Cut树媲美。论文证明了一个关键洞察：UFO Trees和Link-Cut树都能在低直径树上实现次对数（sub-logarithmic）时间的更新和查询，这一理论结果为两者的实际性能提供了统一解释。作者对UFO Trees进行了广泛的实验研究，与十种其他动态树实现（包括新设计的方案）在合成和真实树基准上进行了对比。实验表明UFO Trees在串行和并行场景下都是支持广泛查询功能的最快动态树数据结构，且空间使用低，可扩展至十亿级输入规模。

> **信息来源**：arXiv:2601.10706 摘要

#### Sharded Elimination and Combining for Highly-Efficient Concurrent Stacks

- **作者**：Ajay Singh, Nikos Metaxakis, Panagiota Fatourou (FORTH ICS / University of Crete)
- **关键词**：Concurrent Stack, Sharding, Elimination, Combining
- **发表信息**：PPoPP 2026, ACM SIGPLAN

### 技术概要

并发栈是多线程编程中的基础数据结构，但在高竞争场景下性能严重退化：多个线程同时争抢栈顶指针导致大量CAS冲突和缓存行失效。现有的高性能并发栈方案主要通过两种策略缓解竞争——消除（elimination，配对的push/pop操作直接交换数据而不访问栈）和合并（combining，一个线程代表多个等待线程执行操作），但这两种策略在高线程数下各自面临瓶颈：消除需要配对的push/pop在时间上重合，而合并的代表线程成为新瓶颈。

本文提出将分片（sharding）、消除和合并三种机制高度协同的新型并发栈实现。核心创新在于：将栈分为多个分片（shard），每个分片独立维护以减少争用；在每个分片上同时部署消除层和合并层，使push和pop操作可以在消除层直接配对，未配对的请求进入合并层由代表线程批量执行。分片数量的动态调整机制根据运行时竞争强度自动优化分片粒度。实验表明，在高线程数（128+线程）和高竞争场景下，该栈比所有现有并发栈实现快最多2倍，且保证可线性化（linearizable）正确性。

> **信息来源**：PPoPP 2026 官方程序

#### Concurrent Balanced Augmented Trees

- **作者**：Evan Wrench (UBC), Ajay Singh, Younghun Roh, Panagiota Fatourou, Siddhartha Jayanti (Google Research), Eric Ruppert, Yuanhao Wei
- **关键词**：Concurrent Balanced Trees, Augmented Trees
- **发表信息**：PPoPP 2026, ACM SIGPLAN

### 技术概要

增强树（augmented trees）是在每个节点维护额外聚合信息（如子树大小、求和、最大值等）的平衡搜索树，广泛应用于数据库索引、区间查询和顺序统计等场景。在并发环境下，增强树面临双重挑战：(1) 树的结构修改（旋转、分裂、合并）必须保持平衡性；(2) 增强值必须在结构变更时被一致更新——一个节点的增强值依赖其子树中所有节点的信息，结构变更可能导致增强值级联失效。现有并发树方案要么仅支持基本搜索树操作而不支持增强值，要么在更新增强值时引入严重的全局锁定开销。

本文设计了首个支持高效并发更新的平衡增强树数据结构。核心技术包括：(1) 局部化增强值更新协议——通过精心设计的更新顺序，将增强值的修正限制在受影响的子树路径上，避免全局重新计算；(2) 与平衡操作（如AVL旋转或红黑树重新着色）的原子组合——确保结构变更和增强值更新在同一个原子操作中完成，其他线程不会观察到中间状态；(3) 基于细粒度锁的并发控制，允许不重叠子树上的操作完全并行执行。实验表明在多种增强类型（求和、计数、最值）和工作负载下均实现了良好的可扩展性。

> **信息来源**：PPoPP 2026 官方程序

#### Parallel Dynamic Spatial Indexes

- **作者**：Ziyang Men, Bo Huang, Yan Gu, Yihan Sun (UC Riverside)
- **关键词**：Spatial Index, Parallel Dynamic Data Structure
- **发表信息**：PPoPP 2026, ACM SIGPLAN

### 技术概要

空间索引（如R-tree、kd-tree）是地理信息系统、数据库和计算机图形学中的核心数据结构，支持范围查询、最近邻搜索等操作。在多线程环境中，现有并发空间索引方案面临两难：基于锁的方案在高竞争下性能退化，基于无锁的方案难以支持复杂的空间查询操作。更重要的是，当需要批量插入/删除时（如实时追踪系统中数千个移动对象同时更新位置），现有方案只能串行执行，无法利用多核并行性。

本文提出首个支持并行批量更新的动态空间索引数据结构。核心技术包括：(1) 基于批量并行构建的R-tree重构算法，允许多个线程同时插入/删除对象而保持树的平衡性和空间索引的正确性；(2) 高效的范围查询和k-NN查询算法，与批量更新操作可并行执行；(3) 理论工作复杂度分析，证明批量操作的工作复杂度接近最优串行算法。实验表明在大规模地理空间数据集上实现了良好的并行加速比。

> **信息来源**：PPoPP 2026 官方程序

---

## 4. GPU 计算与稀疏矩阵

### 4.1 GPU 与异构计算

#### 4.1.1 概况

4 篇论文，覆盖有损压缩、OpenMP 数据映射诊断、GPU 上的最大团枚举与全对最短路径。

#### 4.1.2 重点论文

#### ★ PRISM: An Efficient GPU-Based Lossy Compression Framework for Progressive Data Retrieval with Multi-Level Interpolation（最佳论文提名）

- **作者**：Bing Lu, Zedong Liu, Hairui Zhao, Dejun Luo, Wenjing Huang, Yida Gu, Jinyang Liu, Guangming Tan, **Dingwen Tao** (中科院计算所 / 中国科学院大学)
- **关键词**：GPU Lossy Compression, Progressive Data Retrieval, Multi-Level Interpolation, Scientific Data
- **发表信息**：PPoPP 2026, ACM SIGPLAN (Best Paper Nominee)

### 技术概要

高性能计算（HPC）模拟产生的科学数据规模已达EB级别，存储和I/O成为严重瓶颈。有损压缩通过在可控误差范围内减少数据精度来大幅降低存储需求，但现有GPU有损压缩框架（如cuSZ、MGARD）仅支持“全有或全无”的解压模式——用户需要访问数据的一小部分时也必须解压整个数据集。这在渐进式数据检索场景（如可视化、探索性分析）中效率极低，用户通常需要先查看低分辨率概览，再逐步细化感兴趣的区域。

PRISM提出了首个支持渐进式数据检索的GPU有损压缩框架。核心创新包括：(1) 多级插值架构——将数据按多个分辨率层级组织，每个层级可以独立解压，用户从最低分辨率开始，逐步解压更高分辨率的细节；(2) GPU高效的多级插值内核——充分利用GPU的大规模并行性和内存层次结构，实现高压缩比的同时保持快速解压速度；(3) 误差控制机制——确保每一级的解压数据都在用户指定的误差界限内。PRISM在多种科学数据集（气候模拟、粒子物理、天文学）上的评估显示，在保持相同压缩比的情况下，渐进式检索速度比全量解压快5-20倍。该工作获得PPoPP 2026最佳论文提名。

> **信息来源**：PPoPP 2026 官方程序 | 中科院计算所陶鼎文团队

#### Dynamic Detection of Inefficient Data Mapping Patterns in Heterogeneous OpenMP Applications (OMPDataPerf)

- **作者**：Luke Marzen, Junhyung Shim, Ali Jannesari (Iowa State University)
- **关键词**：OpenMP, Heterogeneous Computing, Data Mapping, Dynamic Analysis
- **发表信息**：PPoPP 2026, ACM SIGPLAN

### 技术概要

OpenMP的target offload模型允许将计算和数据显示卸载到GPU等异构设备，但数据映射（data mapping）的效率直接决定应用性能。低效的数据映射模式——如不必要的数据拷贝、过度的数据分配、缺失的映射子句导致的隐式拷贝——是异构OpenMP应用中最常见且最难发现的性能问题。现有的静态分析工具难以处理动态的数据映射行为，而profiling工具仅提供底层事件日志，需要专家手动解读。

OMPDataPerf是基于OMPT（OpenMP Tools Interface）的动态分析工具，自动检测异构OpenMP应用中的低效数据映射模式。核心技术包括：(1) 定义了一组常见的低效数据映射模式分类（如冗余拷贝、过度分配、隐式映射等）；(2) 基于OMPT回调机制实现轻量级运行时监控，动态识别这些模式并生成可读的诊断报告；(3) 提供具体的优化建议（如添加map子句、使用data region等）。实验表明OMPDataPerf仅引入5%的几何平均运行时开销，在多个真实OpenMP应用中成功检测到了可显著改善性能的数据映射问题。

> **信息来源**：PPoPP 2026 官方程序

#### Root-Down Exposure for Maximal Clique Enumeration on GPUs

- **作者**：Zhe Pan, Peng Qu, Youhui Zhang (Tsinghua University)
- **关键词**：Maximal Clique, GPU Enumeration, Root-Down Exposure
- **发表信息**：PPoPP 2026, ACM SIGPLAN

### 技术概要

最大团枚举（Maximal Clique Enumeration）是图挖掘中的基础问题，在社交网络分析、生物信息学和推荐系统中有广泛应用。该问题的计算复杂度为指数级，对大规模图来说极具挑战性。GPU的大规模并行性理论上可以加速枚举过程，但现有的GPU移植方案面临根本性困难：传统的Bron-Kerbosch等回溯算法本质上是深度优先搜索，其不规则的分支结构和动态的候选集管理难以有效映射到GPU的SIMT执行模型上，导致线程发散和负载不均。

本文提出Root-Down Exposure策略，从根节点开始自顶向下地暴露搜索树，将搜索空间的探索重组为GPU友好的层次化批次。核心创新包括：(1) 将搜索树的前几层展开为独立的并行任务，每个GPU线程处理一个子搜索空间；(2) 设计了高效的候选集管理数据结构，支持GPU线程的快速访问和更新；(3) 动态负载均衡机制，根据各子搜索空间的实际工作量重新分配GPU资源。在多种大规模图基准上的实验表明，该方案显著优于现有GPU最大团枚举方案。

> **信息来源**：PPoPP 2026 官方程序

#### ROME: Maximizing GPU Efficiency for All-Pairs Shortest Path via Taming Fine-Grained Irregularities

- **作者**：Weile Luo, Yuhan Chen, Xiangrui Yu, Ruibo Fan (HKUST-GZ), Qiang Wang (HIT-Shenzhen), Hongyuan Liu (Stevens), Xiaowen Chu (HKUST-GZ)
- **关键词**：All-Pairs Shortest Path, GPU Irregularity, Fine-Grained Optimization
- **发表信息**：PPoPP 2026, ACM SIGPLAN

### 技术概要

全对最短路径（APSP）是图算法中的经典问题，计算复杂度为O(n³)，在大规模图上计算量巨大。GPU的大规模并行性理论上可以加速APSP，但实际移植面临多层次的细粒度不规则性：不同源点的最短路径搜索树深度不同导致线程发散；不同图区域的密度差异导致计算量不均；稀疏图的邻居列表长度不一导致内存访问不规则。现有GPU APSP方案主要关注粗粒度的并行策略（如将不同源点分配到不同GPU），而忽视了这些细粒度不规则性对GPU效率的严重影响。

ROME提出了一套系统的优化策略来“删服”这些细粒度不规则性。核心技术包括：(1) 自适应的工作分配策略，根据每个源点的搜索树特征动态调整GPU资源分配；(2) 规整化的内存访问模式，将不规则的邻居列表重组为GPU友好的连续内存布局；(3) 混合精度计算策略，在保证最短路径正确性的前提下利用低精度算术加速计算。实验表明ROME在多种图基准上实现了接近GPU理论峰值的计算效率。

> **信息来源**：PPoPP 2026 官方程序

---

### 4.2 模板计算与稀疏矩阵

#### 4.2.1 概况

4 篇论文，聚焦稀疏矩阵在 Tensor Core、Arm SME 等新硬件上的高效计算。

#### 4.2.2 重点论文

#### SPIDER: Unleashing Sparse Tensor Cores for Stencil Computation via Strided Swapping

- **作者**：Qiqi Gu, Chenpeng Wu, Heng Shi, Jianguo Yao (SJTU / Shanghai Enflame Technology)
- **关键词**：Stencil Computation, Sparse Tensor Cores, Strided Swapping
- **发表信息**：PPoPP 2026, ACM SIGPLAN

### 技术概要

模板计算（stencil computation）是科学计算中的核心内核，广泛用于PDE求解、流体模拟、图像处理等领域。其计算模式为对多维网格上的每个点，根据相邻点的值更新当前点的值。NVIDIA GPU的Tensor Core为矩阵乘法提供了极高的算力，但stencil计算的访存模式（滑动窗口式邻居访问）与Tensor Core期望的矩阵块访问模式严重不匹配，导致Tensor Core利用率极低。现有方案将stencil转换为矩阵形式时引入大量数据重组开销，且无法处理稀疏网格场景。

SPIDER提出利用稀疏Tensor Core加速stencil计算的新方法。核心创新在于跨步交换（strided swapping）策略：将stencil计算的邻居访问模式重新排列为Tensor Core可直接处理的跨步矩阵块，无需显式的数据重组。对于稀疏网格，SPIDER利用NVIDIA Ampere及以后架构的稀疏Tensor Core（2:4结构化稀疏），将stencil的稀疏性直接映射到硬件稀疏格式，进一步减少计算和访存开销。实验表明SPIDER在多种stencil类型（7点、27点、高阶）上实现了显著的性能提升。

> **信息来源**：PPoPP 2026 官方程序

#### ASM-SpMM: Unleashing the Potential of Arm SME for Sparse Matrix Multiplication Acceleration

- **作者**：Jiazhi Jiang, Xijia Yao, Jiayu Chen, Jinhui Wei, Dan Huang, Yutong Lu (Sun Yat-sen University)
- **关键词**：Arm SME, SpMM, Sparse Matrix Multiplication, Matrix Engine
- **发表信息**：PPoPP 2026, ACM SIGPLAN

### 技术概要

稀疏矩阵-密集矩阵乘法（SpMM）是图神经网络、推荐系统和科学计算的核心操作。NVIDIA GPU的Tensor Core已有成熟的SpMM加速方案，但ARM生态中的高性能稀疏计算方案仍然缺乏。ARM的可扩展矩阵扩展（SME, Scalable Matrix Extension）是ARMv9架构引入的新一代矩阵加速硬件，包含Streaming SVE模式和ZA tile寄存器，理论上可提供强大的矩阵计算能力。然而，SME的编程模型与NVIDIA Tensor Core差异巨大，如何有效利用SME加速SpMM是一个未被探索的问题。

ASM-SpMM首次系统性探索了ARM SME在SpMM上的加速潜力。核心技术包括：(1) 将SpMM的稀疏行访问模式映射到SME的Streaming SVE模式，利用其可伸缩的向量长度适应不同稀疏度；(2) 利用ZA tile寄存器缓存中间结果，减少对主存的访问；(3) 针对SME的outer-product执行模式优化数据布局。在ARM A64FX等支持SME的处理器上的实验表明，ASM-SpMM显著优于现有的ARM稀疏计算库。

> **信息来源**：PPoPP 2026 官方程序

#### Exploiting Efficient Mapping and Pipelined Execution for Accelerating SpMV on Tensor Cores

- **作者**：Kaige Zhang, Hailong Yang et al. (Beihang University)
- **关键词**：SpMV, Tensor Cores, Mapping, Pipelined Execution
- **发表信息**：PPoPP 2026, ACM SIGPLAN

### 技术概要

稀疏矩阵-向量乘法（SpMV）是科学计算和迭代求解器中最基础的内核之一，但其不规则的内存访问模式使其难以利用GPU Tensor Core的高算力。Tensor Core设计用于密集矩阵乘法（16x16或8x8块），而SpMV中每行的非零元素数量和分布差异巨大，导致难以形成规则的矩阵块。现有方案（如cuSPARSE）主要通过将稀疏矩阵转换为规则格式（如BSR、ELLPACK）来适配Tensor Core，但转换开销大且对不规则稀疏矩阵效果差。

本文提出通过高效映射和流水线执行在Tensor Core上加速SpMV。核心创新包括：(1) 自适应映射策略——根据矩阵行的非零元素分布自动选择最优的Tensor Core块大小和填充策略；(2) 流水线执行框架——将SpMV的计算分解为多个流水线阶段（数据加载、格式转换、Tensor Core计算、结果累加），各阶段重叠执行以隐藏延迟；(3) 智能填充策略——最小化将不规则行填充为规则Tensor Core块所需的额外计算。在SuiteSparse矩阵集合上的实验表明显著优于cuSPARSE。

> **信息来源**：PPoPP 2026 官方程序

#### VDHA: Vector-Driven Hash Aggregation for Sparse Matrix-Sparse Vector Multiplication on GPUs

- **作者**：Yuchen Li, Zhe Pan, Peng Qu, Youhui Zhang (Tsinghua University)
- **关键词**：SpM-SpV, Hash Aggregation, GPU
- **发表信息**：PPoPP 2026, ACM SIGPLAN

### 技术概要

稀疏矩阵-稀疏向量乘法（SpM-SpV）是图分析、推荐系统和信息检索中的核心操作。与更常见的SpMV（稀疏矩阵-密集向量）不同，SpM-SpV的输入向量也是稀疏的，这意味着结果向量的大多数元素为零。这种双稀疏性使得传统的基于数组的结果累加方案极度低效（大量无效的零元素操作），而基于哈希表的方案又面临GPU上的哈希冲突和原子操作开销问题。

VDHA提出了向量驱动的哈希聚合方法来解决GPU上SpM-SpV的效率问题。核心创新在于：(1) 以输入向量的非零元素为驱动（而非以矩阵行为驱动），仅计算对结果有贡献的元素，完全跳过零元素的无效计算；(2) 设计GPU友好的哈希聚合结构，利用共享内存作为一级哈希表减少全局内存原子操作；(3) 自适应的哈希表大小调整策略，根据输入向量稀疏度动态确定最优的哈希表容量。在多种稀疏图数据集上的实验表明，VDHA显著优于现有GPU SpM-SpV方案，特别是在输入向量极度稀疏的场景下。

> **信息来源**：PPoPP 2026 官方程序

---

## 5. 混合精度与量化

### 5.1 概况

4 篇论文，覆盖 LLM 量化推理、KV Cache 压缩、分子动力学混合精度等热点应用。

### 5.2 重点论文

#### RoMeo: Mitigating Dual-dimensional Outliers with Rotated Mixed Precision Quantization

- **作者**：Qihao Zhang, MingLiang Tang, Mingshu Zhai, Kinman Lei, **Jidong Zhai** (Tsinghua University)
- **关键词**：Mixed Precision Quantization, Outlier Mitigation, LLM
- **发表信息**：PPoPP 2026, ACM SIGPLAN

### 技术概要

LLM量化推理面临的核心挑战是离群值（outlier）问题：激活值和权重中都存在少量极端值，如果统一使用低精度量化会导致严重的精度损失。现有方案主要通过混合精度策略（对离群值通道保留高精度，其余使用低精度）来缓解，但仅单独处理激活值或权重的离群值。当两者同时存在离群值时（“双维度离群值”），现有方法的交互效应导致精度退化严重，无法同时降低两个维度的位宽。

RoMeo提出旋转混合精度量化方法，核心创新在于通过数学旋转变换同时缓解激活值和权重的双维度离群值。技术方案包括：(1) 旋转矩阵设计——找到一个正交变换，使变换后的激活值和权重分布更加均匀，离群值被“旋转”分散到多个维度上；(2) 双维度混合精度分配——在旋转后的空间中，为激活值和权重分别分配最优的精度方案，两者协同优化而非独立决策；(3) 硬件友好的实现——旋转变换可融合到矩阵乘法前的预处理中，不增加推理时的计算开销。实验表明RoMeo在Llama、OPT等模型上实现了更低的位宽和更高的推理吞吐。

> **信息来源**：PPoPP 2026 官方程序 | 清华大学翟季冬团队

#### JanusQuant: Accurate and Efficient 2-bit KV Cache Quantization for Long-Context Inference

- **作者**：Chengyu Sun, Yaqi Xia (Wuhan University), Donglin Yang (Nvidia), Dazhao Cheng (Wuhan University)
- **关键词**：KV Cache Quantization, 2-bit, Long-Context Inference
- **发表信息**：PPoPP 2026, ACM SIGPLAN

### 技术概要

长上下文LLM推理中，KV Cache的内存占用随序列长度线性增长，成为推理服务的主要瓶颈。例如128K上下文窗口的Llama-70B模型，单个请求的KV Cache可达数十GB。量化是减少KV Cache内存的有效手段，但将其压缩到2-bit时面临严重的精度挑战：KV Cache中的Key和Value分布高度非均匀，且不同层、不同头的敏感度差异巨大。现有4-bit/8-bit量化方案（如KIVI、GEAR）在2-bit下精度崩溃，而专用2-bit方案（如KVQuant）的量化/反量化开销过高，抵消了内存节省带来的推理加速。

JanusQuant实现了精确且高效的2-bit KV Cache量化。核心创新包括：(1) “双面神”（Janus）策略——对Key和Value采用不同的量化策略，Key侧重保持注意力分数的相对排序，Value侧重保持数值精度；(2) 通道感知的非均匀量化——为每个注意力头学习最优的量化分箱点，适应不同头的分布特征；(3) 高效的2-bit量化/反量化内核——利用位操作实现无乘法器的快速转换，开销低于5%。在128K上下文的Llama和Mistral模型上，JanusQuant在困惑度损失<1%的情况下将KV Cache内存降低4倍。

> **信息来源**：PPoPP 2026 官方程序

#### ★ HierCut: Enabling 16-bit Format Mixed Precision for Molecular Dynamics through Hierarchical Cutoff（最佳 Artifact 奖）

- **作者**：Zeyu Song, **Lin Gan**, Xiaohui Duan et al. (Tsinghua University)
- **关键词**：Molecular Dynamics, Mixed Precision, Hierarchical Cutoff, 16-bit
- **发表信息**：PPoPP 2026, ACM SIGPLAN (Best Artifact Award)

### 技术概要

分子动力学（MD）模拟通过数值求解牛顿运动方程模拟原子/分子的运动，是材料科学、药物设计和生物物理的核心计算工具。MD的计算瓶颈在于短程力（如Lennard-Jones势、库仑力）的粒子对计算，其复杂度为O(N²)。将计算从FP64/FP32降低到FP16/BF16可大幅提升GPU算力利用率，但MD对数值精度极为敏感——微小的力计算误差在长期积分中累积导致能量漂移和轨迹发散。现有混合精度MD方案（如MixedSPME）仅在最内层力计算使用FP16，外层求和仍需FP32，限制了性能提升。

HierCut通过分层截断（Hierarchical Cutoff）技术首次在MD中实现了完整的16-bit混合精度计算。核心创新在于：(1) 将粒子对按距离分层，近距离对使用FP32保证精度，中距离对使用BF16，远距离对使用FP16——不同距离的力贡献量级不同，远距离力的数值本身就小，FP16精度已足够；(2) 分层累加策略——各层的力分别在对应精度下累加，最后以FP32合并，避免跨精度累加的舍入误差；(3) 动态精度调整——根据模拟过程中的粒子分布动态优化分层阈值。在LAMMPS上的实现显示，HierCut在保持能量守恒和轨迹精度的同时实现了显著的GPU性能提升。该工作获得PPoPP 2026最佳Artifact奖。

> **信息来源**：PPoPP 2026 官方程序 | 清华大学甘霖团队

#### High-Throughput Non-Uniformly Quantized 3-bit LLM Inference

- **作者**：YuAng Chen, Wenqi Zeng, Jeffrey Xu Yu (CUHK / HKUST)
- **关键词**：3-bit LLM Inference, Non-uniform Quantization
- **发表信息**：PPoPP 2026, ACM SIGPLAN

### 技术概要

LLM推理的内存带宽瓶颈使得低比特量化成为提升吞吐的关键技术。4-bit均匀量化（如GPTQ、AWQ）已较为成熟，但进一步压缩到3-bit时精度损失急剧增加。非均匀量化（NUQ）通过使用不等间距的量化级别可以更好地拟合权重分布，理论上比均匀量化在相同比特数下精度更高。然而NUQ的致命缺陷是反量化开销——均匀量化仅需一次乘法和加法，而非均匀量化需要查表（LUT），而LUT操作在GPU上极不友好（随机内存访问、无向量化），导致推理吞吐反而低于4-bit均匀量化。

本文设计了高吞吐的非均匀3-bit量化LLM推理方案。核心创新在于解决NUQ的吞吐瓶颈：(1) 将LUT操作重组为GPU友好的内存布局，使32个权重共享一个小型LUT，利用共享内存实现快速查表；(2) 利用位打包技术将3-bit权重紧密存储，减少内存访问量；(3) 设计了与NUQ兼容的kernel融合策略，将查表、反量化和矩阵乘法融合为单个GPU kernel。在Llama和OPT等模型上的实验表明，该方案在3-bit精度下实现了接近4-bit均匀量化的推理吞吐，同时 perplexity 损失显著小于均匀3-bit方案。

> **信息来源**：PPoPP 2026 官方程序

---

## 6. 集群与云计算

### 6.1 概况

4 篇论文，覆盖云缓存管理、零拷贝序列化、GPU-to-CPU 迁移、GPU 集群稀疏求解器。

### 6.2 重点论文

#### Cacheman: A Comprehensive Last-Level Cache Management System for Multi-tenant Clouds

- **作者**：Xiaokang Hu et al. (Alibaba Cloud Computing)
- **关键词**：LLC Management, Multi-tenant Cloud, Cache Partitioning
- **发表信息**：PPoPP 2026, ACM SIGPLAN

### 技术概要

多租户云环境中，多个VM共享物理服务器的Last-Level Cache (LLC)，导致严重的缓存干扰问题——一个租户的大量缓存访问会抢占其他租户的缓存空间，导致尾延迟飙升。现有LLC管理方案（如Intel CAT）仅提供粗粒度的缓存分区，无法根据运行时负载动态调整，且缺乏对租户性能目标的感知。Linux内核的缓存回收策略（如CLOX）则完全无视租户边界，导致缓存污染。

Cacheman是阿里云提出的综合LLC管理系统，核心创新包括：(1) 细粒度缓存分区——以cache way为基本单位，在租户间动态分配LLC空间，并支持优先级策略；(2) 性能感知的缓存分配——根据每个租户的miss rate和IPC变化动态调整其缓存配额，确保关键租户的尾延迟SLO；(3) 与内存管理协同——将LLC分区决策与NUMA内存分配联动优化。在阿里云生产环境中的评估表明，Cacheman显著降低了多租户场景下的尾延迟变异。

> **信息来源**：PPoPP 2026 官方程序 | 阿里云

#### zBuffer: Zero-Copy and Metadata-Free Serialization for Fast RPC with Scatter-Gather Reflection

- **作者**：Xiangyu Liu (Xiamen University), Huiba Li, Shun Gai (Alibaba), Youmin Chen (SJTU), Yiming Zhang (Xiamen University)
- **关键词**：Zero-Copy Serialization, RPC, Scatter-Gather
- **发表信息**：PPoPP 2026, ACM SIGPLAN

### 技术概要

RPC序列化/反序列化是微服务架构中不可忽视的性能开销——在高吞吐场景下可占总请求延迟的20-40%。现有零拷贝序列化方案（如FlatBuffers、Cap'n Proto）虽避免了拷贝，但引入了复杂的元数据管理开销（偏移量计算、边界检查）；而Protobuf等经典方案虽然简单但需要多次内存拷贝。如何在零拷贝的同时消除元数据开销是一个长期未解决的问题。

zBuffer提出了基于scatter-gather reflection的零拷贝、无元数据序列化方案。核心创新在于：(1) 利用C++ reflection机制在编译时生成消息的内存布局描述，运行时直接利用该描述进行scatter（序列化）和gather（反序列化），无需额外元数据；(2) 零拷贝设计——序列化时直接引用应用内存中的数据，gather时通过writev-like系统调用直接发送到网络，全程无数据拷贝；(3) 与阿里云RPC框架深度集成，在实际生产负载下序列化延迟降低60%以上。

> **信息来源**：PPoPP 2026 官方程序 | 厦门大学/阿里云

#### Scaling GPU-to-CPU Migration for Efficient Distributed Execution on CPU Clusters

- **作者**：Ruobing Han, Hyesoon Kim (Georgia Tech)
- **关键词**：GPU-to-CPU Migration, Distributed Execution, CPU Cluster
- **发表信息**：PPoPP 2026, ACM SIGPLAN

### 技术概要

GPU计算的快速增长催生了大量GPU专属软件，但许多组织仍然主要拥有CPU集群。将GPU程序移植到CPU集群执行面临两个挑战：(1) GPU程序的并行模型（SIMT、共享内存）与CPU集群（MIMD、分布式内存）差异巨大，直接移植性能极差；(2) 现有GPU-to-CPU迁移工具（如HIP-to-OpenMP）仅支持单机转换，无法扩展到分布式CPU集群。

本文探索了将GPU计算任务高效迁移至CPU集群执行的系统化方法。核心技术包括：(1) 自动将GPU kernel转换为CPU多线程代码，并将共享内存操作映射到分布式共享内存或消息传递；(2) 智能的任务划分策略，根据CPU集群的网络拓扑和计算能力分配GPU block的工作负载；(3) 通信优化，将GPU的同步模式转换为CPU集群高效的异步通信模式。在多种GPU benchmark上的实验表明，迁移后的程序在CPU集群上可以达到接近手动优化版本的性能。

> **信息来源**：PPoPP 2026 官方程序

#### ★ Trojan Horse: Aggregate-and-Batch for Scaling Up Sparse Direct Solvers on GPU Clusters（最佳论文提名）

- **作者**：Yida Li, Siwei Zhang, Yiduo Niu, Yang Du, Qingxiao Sun, Zhou Jin, **Weifeng Liu** (China University of Petroleum-Beijing)
- **关键词**：Sparse Direct Solvers, GPU Clusters, Aggregate-and-Batch
- **发表信息**：PPoPP 2026, ACM SIGPLAN (Best Paper Nominee)

### 技术概要

稀疏直接求解器（sparse direct solvers）是求解大规模稀疏线性系统Ax=b的核心工具，广泛应用于有限元分析、电路模拟、流体力学等科学计算领域。其计算过程（如Cholesky/LU分解）涉及大量的稀疏矩阵操作，计算复杂度为O(n^{1.5})到O(n²)。GPU的高算力理论上可以加速求解过程，但稀疏直接求解器的核心操作（如稀疏三角求解、超节点分解）具有高度不规则的计算模式和严重的数据依赖，使其难以高效映射到GPU集群上。现有GPU稀疏求解器（如cuSOLVER）主要优化单GPU性能，在多GPU集群上的可扩展性极差。

Trojan Horse提出了“特洛伊木马”聚合批处理策略，核心创新在于将稀疏直接求解器中的多个小型、不规则的子任务“聚合”成GPU友好的大型批处理任务——就像将士兵藏在木马里一样，将不规则计算包装在规则的计算外壳中。具体包括：(1) 超节点聚合——将多个小的稀疏超节点合并为一个大型密集块，利用GPU的密集矩阵计算能力；(2) 流水线批处理——将求解过程中的依赖链重组为可并行的批次；(3) 多GPU负载均衡——根据各GPU的计算能力和子任务分布动态分配工作。在多种大规模稀疏矩阵上的实验表明，Trojan Horse在多GPU集群上实现了显著优于现有方案的加速比。

> **信息来源**：PPoPP 2026 官方程序 | 中国石油大学(北京)

---

## 7. ML 训练分布式优化

### 7.1 概况

4 篇论文，聚焦 LLM 分布式训练中的通信压缩、弹性容错、长序列训练流水线和故障诊断。

### 7.2 重点论文

#### COCCL: A Collective Communication Library Supporting Easy Integration and Configuration of Customized Compression for Scalable LLM Training

- **作者**：Xingchen Liu, Hairui Zhao, Shengkai Lyu, Guangming Tan, **Dingwen Tao** 等 (ICT CAS / CUHK-Shenzhen / Ant Group)
- **关键词**：Collective Communication, Compression, LLM Training, Communication Library

中科院计算所陶鼎文团队提出了 **COCCL**——新一代高性能通信库。分布式LLM训练中，AllReduce/AllGather等集合通信是主要瓶颈，现有通信库（如NCCL）仅支持有限的内置压缩算法，用户自定义压缩算法需要修改库源码，集成门槛极高。COCCL的核心创新在于：(1) 插件式压缩架构——用户仅需实现压缩/解压函数即可自动集成到集合通信流程中，无需修改通信库内部逻辑；(2) 通信-压缩流水线——将数据分块后在通信和压缩之间流水线化执行，隐藏压缩开销；(3) 异构设备支持——压缩可在GPU、CPU或专用加速器上执行，根据设备可用性自动选择最优路径。COCCL已在国产超算平台部署，通信成本降低最高70%。

> **信息来源**：PPoPP 2026 官方程序 | 中科院计算所陶鼎文团队

#### ★ Elastor: Elastic and Efficient Model Partitioning and Checkpointing for Fault-Tolerant Distributed Training

- **作者**：Xuanyu Wang, Fangcheng Fu, Haoyang Li, Hao Ge, Sheng Lin, Jiawen Niu, **Bin Cui** (Peking University / SJTU)
- **关键词**：Fault-Tolerant Training, Elastic Model Partitioning, Checkpointing, Heterogeneous Parallelism
- **开源代码**：https://github.com/PKU-DAIR/Hetu

北大崔斌教授团队（PKU-DAIR）提出 **Elastor**，解决大模型训练中GPU故障导致的训练中断问题。现有方案依赖定期全局检查点+重启，但在大规模集群上故障频率高（MTBF仅数小时），重启和恢复开销巨大。Elastor的核心创新：(1) **异构模型并行（HMP）**——允许不同DP rank内的TP组大小不一致，GPU部分失效时仍能用剩余GPU自适应训练；(2) **快速策略搜索**——GPU数量变化后数秒内自动搜索最优并行策略；(3) **细粒度分片检查点**——参数张量统一划分为全局split，恢复时每张GPU仅加载自己负责的部分，避免冗余I/O；(4) **训练与保存重叠**——通过共享内存和多进程解耦参数搬运、序列化与写盘。在32张A100集群上，LLaMA2-7B/13B等模型验证了有效性。

> **信息来源**：PPoPP 2026 官方程序 | 北大PKU-DAIR | [开源代码](https://github.com/PKU-DAIR/Hetu)

#### HelixPipe: Efficient Distributed Training of Long Sequence Transformers with Attention Parallel Pipeline Parallelism

- **作者**：Geng Zhang, Shenggan Cheng, Xuanlei Zhao, Ziming Liu, **Yang You** (National University of Singapore)
- **关键词**：Long Sequence Training, Attention Parallelism, Pipeline Parallelism

新加坡国立大学尤洋团队提出HelixPipe，解决长序列Transformer训练的内存和效率瓶颈。当序列长度超过64K时，注意力计算的内存需求为O(n²)，单GPU无法容纳。现有方案要么使用序列并行（SP）将序列切分到多GPU但引入通信开销，要么使用流水线并行（PP）将层切分但产生气泡。HelixPipe将注意力并行（AP）与PP协同：AP将长序列切分到多个PP stage中并行处理注意力，PP则在不同层之间流水线化执行。核心挑战在于AP和PP的内存访问模式冲突以及通信模式的叠加，HelixPipe通过精心设计的调度策略解决这些冲突。

> **信息来源**：PPoPP 2026 官方程序 | NUS尤洋团队

#### ★ CCL-D: A High-Precision Diagnostic System for Slow and Hang Anomalies in Large-Scale Model Training（最佳论文提名）

- **作者**：Yida Gu, Fakang Wang, Jianhao Fu, Zhenhang Sun, Guangming Tan, **Dingwen Tao** 等 (ICT CAS / Ant Group)
- **关键词**：Anomaly Diagnosis, Communication Hang, Large-Scale Training, Diagnostic System

中科院计算所与蚂蚁集团联合提出**CCL-D**，解决大规模分布式训练中的“慢”和“挂”异常诊断难题。“慢”异常指某个GPU rank的计算或通信速度显著下降，“挂”异常指某个rank完全停止响应。这两种异常都会导致所有rank等待最慢者，严重拖慢整体训练。现有监控工具仅提供节点级指标，无法定位到rank级的具体故障。CCL-D集成了rank级实时探针和智能决策分析器：(1) 轻量级分布式追踪框架监测每个rank的通信流量模式；(2) 基于统计异常检测算法自动识别偏离正常模式的rank；(3) 决策树分析器根据异常特征定位根因（GPU硬件故障、网络拥塞、代码bug等）。在4000 GPU集群部署一年，实现近乎全覆盖检测，**6分钟内**精确定位故障rank。

> **信息来源**：PPoPP 2026 官方程序 | 中科院计算所/蚂蚁集团

---

## 8. 并行算法

### 8.1 概况

4 篇论文，覆盖零知识证明 GPU 加速、自动微分并行化、序列比对优化、PIM（存内计算）索引结构。

### 8.2 重点论文

#### Pipelonk: Accelerating End-to-End Zero-Knowledge Proof Generation on GPUs for PLONK-Based Protocols

- **作者**：Zhiyuan Zhang, Yanxin Cai, Wenhao Yin (Shandong University), Xueyu Wu (HKU), Yi Wang (SZU), Lei Ju, Zhuoran Ji (Shandong University)
- **关键词**：Zero-Knowledge Proof, GPU Acceleration, PLONK, Pipeline

提出GPU加速PLONK零知识证明生成的端到端流水线方案。PLONK是当前最通用的ZKP协议之一，但其证明生成涉及多项式承诺、FFT、MSM等计算密集型操作，在CPU上耗时数分钟。核心创新：(1) 将PLONK各阶段操作流水线化，利用GPU的大规模并行能力加速FFT和MSM；(2) 设计了GPU友好的多项式承诺算法，减少CPU-GPU数据传输；(3) 内存管理优化，避免GPU内存溢出。实验表明端到端证明生成速度提升10-50倍。

> **信息来源**：PPoPP 2026 官方程序

#### ParDiff: Efficiently Parallelizing Reverse-Mode Automatic Differentiation with Direct Indexing

- **作者**：Shuhong Huang, Shizhi Tang, Huanqi Cao, Ruibai Tang, Jiping Yu, Yang Li, Chao Jiang, Limin Xiao, **Jidong Zhai** (Tsinghua / Lenovo Research / Qingcheng.AI)
- **关键词**：AutoDiff, Reverse-Mode, Direct Indexing, Parallelization

提出基于直接索引的反向模式自动微分并行化方案ParDiff。反向模式自动微分（reverse-mode AD）是深度学习框架计算梯度的核心机制，其本质是构建计算图并反向传播梯度。现有AD实现（如PyTorch autograd）中的梯度计算存在大量顺序依赖，难以并行化。ParDiff通过直接索引技术重新组织计算图的反向传播顺序，将独立的梯度计算任务分配到不同线程并行执行，同时保证梯度累加的正确性。在多种深度学习模型上的实验表明显著提升了梯度计算的并行效率。

> **信息来源**：PPoPP 2026 官方程序 | 清华大学翟季冬团队

#### Faster and Cheaper: Pushing the Sequence Alignment Throughput with Commercial CPUs

- **作者**：Zhonghai Zhang, Yewen Li, Ke Meng, Chunming Zhang, Guangming Tan (ICT CAS)
- **关键词**：Sequence Alignment, CPU Throughput, Bioinformatics

通过精细的CPU级优化将生物信息学中的序列比对通量推向新高。序列比对（如Smith-Waterman、Needleman-Wunsch）是基因组学的核心操作，现有方案主要依赖GPU加速，但GPU的购置和运维成本极高。本文展示了在商用CPU上通过SIMD向量化、缓存优化、多线程调度和NUMA感知等系统级优化，可以达到接近GPU的序列比对通量，同时成本仅为GPU方案的1/10。这项工作证明在特定计算密集型任务上，CPU经过精心优化仍具有强大的竞争力。

> **信息来源**：PPoPP 2026 官方程序 | 中科院计算所

#### PIM-zd-tree: A Fast Space-Partitioning Index Leveraging Processing-in-Memory

- **作者**：Yiwei Zhao, Hongbo Kang, Ziyang Men, Yan Gu, Guy E. Blelloch, Laxman Dhulipala, Charles McGuffey, **Phil Gibbons** (CMU / Tsinghua / UCR / UMD / Reed College)
- **关键词**：Processing-in-Memory, Spatial Index, PIM

提出利用存内计算（PIM）加速空间分区索引的PIM-zd-tree。空间索引（如kd-tree、quad-tree）的查询操作涉及大量不规则的内存访问和比较操作，CPU缓存效率低。PIM将计算移动到内存附近，可以大幅减少数据移动开销。PIM-zd-tree将zd-tree（一种支持并行批量更新的动态空间索引）的查询操作映射到PIM设备上执行，充分利用近数据计算降低查询延迟。核心挑战在于将树形结构的递归遍历转换为PIM友好的顺序执行模式。

> **信息来源**：PPoPP 2026 官方程序 | CMU Phil Gibbons团队

---

## 9. ML 推理与 Transformer 优化

### 9.1 ML 推理服务

#### 9.1.1 概况

4 篇论文，覆盖机器视觉、LLM 多 SLO 推理调度、扩散模型并行推理等方向。

#### 9.1.2 重点论文

#### Laser: Unlocking Layer-Level Scheduling for Efficient Multi-SLO LLM Serving

- **作者**：Jianxiong Liao, Quanxing Dong, Yunkai Liang, Zhi Zhou, Xu Chen (Sun Yat-sen University)
- **关键词**：LLM Serving, Layer-Level Scheduling, Multi-SLO

提出层级调度策略解决LLM推理中的多SLO服务问题。当不同请求有不同延迟要求时（如实时对话要求低延迟，批量处理可容忍高延迟），现有的请求级调度无法同时满足异构SLO。Laser的核心创新在于将调度粒度从请求级细化到层（layer）级：在LLM逐层解码过程中，根据各请求的剩余延迟预算动态调整每层的执行优先级和批处理策略，实现更细粒度的资源分配。实验表明多SLO达标率和goodput均显著提升。

> **信息来源**：PPoPP 2026 官方程序 | 中山大学

#### MixFusion: A Patch-Level Parallel Serving System for Mixed-Resolution Diffusion Models

- **作者**：Desen Sun (Waterloo), Zepeng Zhao (CMU), Yuke Wang (Rice)
- **关键词**：Diffusion Models, Patch-Level Parallelism, Mixed Resolution

设计Patch级并行推理系统解决混合分辨率扩散模型的服务难题。扩散模型在生成过程中需要处理不同分辨率的特征图，高分辨率阶段的计算量大但并行度高，低分辨率阶段计算量小但并行度低。MixFusion在Patch级别将不同分辨率的特征图分解为统一的并行任务，使GPU可以在同一批次中同时处理不同分辨率的patch，消除分辨率切换带来的GPU空闲。

> **信息来源**：PPoPP 2026 官方程序

#### ChituDiffusion: A Data-Characteristic-Aware Serving System for Diffusion Models

- **作者**：Chengzhang Wu, Liyan Zheng, Haojie Wang, Kezhao Huang, Zixuan Ma, Dong Dong, Jidong Zhai (Tsinghua)
- **关键词**：Diffusion Model Serving, Data-Characteristic-Aware

提出数据特征感知的扩散模型推理服务系统。不同输入数据（如简单场景 vs 复杂场景）对扩散模型的去噪步数和计算量需求差异巨大。ChituDiffusion在推理前分析输入数据特征，动态调整去噪步数、采样策略和计算精度，为简单数据分配更少资源，为复杂数据保留充足计算。这种数据驱动的自适应策略在保持生成质量的同时显著提升了推理吞吐。

> **信息来源**：PPoPP 2026 官方程序 | 清华大学翟季冬团队

#### BEEMS: Boosting Machine Vision Efficiency via Computation Graph-Based Memory Smoothing

- **作者**：Hanjing Shen, Fangxin Liu, Jian Liu, Li Jiang, Haibing Guan (SJTU / BUAA)
- **关键词**：Machine Vision, Memory Smoothing, Computation Graph

通过计算图级内存平滑优化提升机器视觉pipeline效率。视觉pipeline包含多个串联模型（检测、分割、跟踪等），各模型的内存峰值差异巨大，导致GPU内存碎片和频繁的分配/释放开销。BEEMS分析计算图中各算子的内存生命周期，通过算子重排序和内存复用策略“平滑”内存峰值，使整体内存占用更加均匀，减少碎片和分配开销。

> **信息来源**：PPoPP 2026 官方程序 | 上海交大/北航

---

### 9.2 图与图神经网络

#### 9.2.1 概况

4 篇论文，覆盖弹性 GNN 训练、时序图网络推理、十亿级 GNN 缓存优化、时序模体挖掘。

#### 9.2.2 重点论文

#### ElasGNN: An Elastic Training Framework for Distributed GNN Training

- **作者**：Siqi Wang, Hailong Yang et al. (Beihang University)
- **关键词**：GNN Training, Elastic Framework, Distributed

提出弹性分布式GNN训练框架。GNN训练的邻居采样导致各mini-batch计算量差异巨大，加上GPU故障或资源波动，静态训练策略效率低下。ElasGNN的核心创新：(1) 弹性数据并行——根据各GPU的实际负载动态调整mini-batch大小和采样深度；(2) 自适应模型并行——当GPU数量变化时自动切换最优并行策略；(3) 故障容错——GPU失效后自动重分区继续训练。在多种GNN模型和动态集群环境下验证了有效性。

> **信息来源**：PPoPP 2026 官方程序 | 北航

#### APERTURE: Algorithm-System Co-optimization for Temporal Graph Network Inference

- **作者**：Yiqing Wang, Hailong Yang et al. (Beihang University)
- **关键词**：Temporal Graph Network, Algorithm-System Co-optimization

从算法-系统协同优化角度对时序图网络（TGN）推理进行全栈优化。TGN需要在动态图上维护节点的时间嵌入，推理时的邻居查询和嵌入更新是主要瓶颈。APERTURE的协同优化包括：算法层面设计近似邻居采样减少查询量，系统层面优化时序数据的内存布局和缓存策略，两者联合优化在不损失精度的情况下显著提升了TGN推理吞吐。

> **信息来源**：PPoPP 2026 官方程序 | 北航

#### TAC: Cache-Based System for Accelerating Billion-Scale GNN Training on Multi-GPU Platform

- **作者**：Zhiqiang Liang, Hongyu Gao, Jue Wang, Peng Di (Ant Group & UNSW) 等 (CNIC CAS / UCAS)
- **关键词**：Billion-Scale GNN, Multi-GPU Training, Cache System

设计基于缓存的系统TAC解决十亿级GNN训练的内存和效率瓶颈。十亿级图的节点嵌入和邻居特征无法完全放入GPU内存，频繁的主机-设备数据传输成为主要瓶颈。TAC在GPU上构建多层次缓存：热点节点嵌入常驻GPU，冷节点按需从主存加载，并利用图结构的空间局部性预测未来访问模式进行预取。在蚂蚁集团的多GPU平台上实现了十亿级GNN的高效训练。

> **信息来源**：PPoPP 2026 官方程序 | 蚂蚁集团/中科院

#### DTMiner: A Data-Centric System for Efficient Temporal Motif Mining

- **作者**：Hou Yinbo, Hao Qi, Ligang He, Jin Zhao, Hai Jin 等 (HUST / University of Warwick / HKUST)
- **关键词**：Temporal Motif Mining, Data-Centric System

提出以数据为中心的时序模体挖掘系统。时序模体（如“A→B→C在Δt内”）是时序图分析的基本原语，现有算法在大规模时序图上效率低下。DTMiner通过数据中心的优化策略——预计算部分结果、缓存中间状态、利用时序局部性剪枝搜索空间——在保持精确挖掘的同时大幅提升了大规模时序图上的模式发现效率。

> **信息来源**：PPoPP 2026 官方程序 | 华中科大/Warwick/HKUST

---

### 9.3 Transformer 优化

#### 9.3.1 概况

3 篇论文，聚焦 Attention 机制的硬件加速与跨平台统一。

#### 9.3.2 重点论文

#### FlashAttention-T: Towards Fully Tensorized Attention by Exploiting Tensor-Vector Parallelism

- **作者**：Jianxing Xu (USTC), Yuanbo Wen, Jun Bi, Ruibai Xu, Rui Zhang, Wei Li, Ling Li, Tianshi Chen, Qi Guo, Yunji Chen (CAS / Cambricon)
- **关键词**：Tensorized Attention, Tensor-Vector Parallelism, FlashAttention

中科院计算所陈云叆/郭崎团队提出FlashAttention-T，在国产AI芯片上实现超越传统方案的Attention性能。现有FlashAttention主要为NVIDIA GPU的Tensor Core设计，而国产AI芯片（如寒武纪）的矩阵计算单元架构不同，无法直接复用。FlashAttention-T的核心创新在于挖掘Tensor-Vector并行性——将Attention的softmax和矩阵乘法分解为可在国产芯片向量单元上高效执行的子操作，通过Tensor化重组使计算充分匹配硬件的计算-内存层次。在寒武纪芯片上实现了超越NVIDIA GPU上FlashAttention的每瓦性能。

> **信息来源**：PPoPP 2026 官方程序 | 中科院/寒武纪

#### Accelerating Sparse Transformer Inference on GPU

- **作者**：Wenhao Dai, Haodong Deng (CUPB), Fangxin Liu (SJTU), Hailong Yang (Beihang) 等
- **关键词**：Sparse Transformer, GPU Inference, Acceleration

针对稀疏Transformer模型推理的GPU高效实现进行系统优化。稀疏Attention（如Longformer、BigBird）通过限制注意力范围降低计算复杂度，但其不规则的稀疏模式与GPU的密集计算单元不匹配。本文通过稀疏模式感知的kernel融合、内存布局优化和warp级负载均衡，在保持稀疏性的同时充分利用GPU算力，在长序列推理场景下显著优于dense Attention。

> **信息来源**：PPoPP 2026 官方程序 | 中国石油大学/北航/上海交大

#### MetaAttention: A Unified and Performant Attention Framework Across Hardware Backends

- **作者**：Feiyang Chen (SJTU), Yu Cheng, Lei Wang (PKU), Ziming Miao, Lingxiao Ma, Fan Yang, Jilong Xue, Mao Yang (Microsoft Research), Xingda Wei, **Haibo Chen** (SJTU)
- **关键词**：Attention Framework, Unified Backend, Cross-Hardware

上海交大IPADS陈海波团队与微软研究院合作提出MetaAttention——跨硬件后端的统一Attention框架。不同AI芯片（NVIDIA GPU、AMD GPU、寒武纪、华为昇腾）的矩阵计算单元差异巨大，为每种硬件单独优化Attention成本极高。MetaAttention通过统一抽象层描述各硬件的计算原语和内存层次，自动生成硬件最优的Attention实现。核心创新在于将Attention计算分解为硬件无关的“算子模板”+硬件特定的“后端实现”，通过编译时优化自动选择最优配置。在多种硬件后端上均实现了接近或超越手工优化版本的性能。

> **信息来源**：PPoPP 2026 官方程序 | 上海交大IPADS/微软研究院

---

## 10. 线性代数与矩阵计算

### 10.1 概况

4 篇论文，覆盖 GPU SVD、多项式预处理器、分布式矩阵运算、矩阵乘法单元表征等。

### 10.2 重点论文

#### ★ Towards Singular Value Decomposition for Rank-Deficient Matrices: An Efficient and Accurate Algorithm on GPU Architectures (HQB-Mixed SVD)

- **作者**：Lu Shi (UESTC), WeiWei Xu (NUIST), **Shaoshuai Zhang** (UESTC)
- **关键词**：Rank-Deficient SVD, GPU, QB Decomposition, Mixed Precision

电子科技大学张少帅团队与南京信息工程大学徐玮玮教授合作，提出了面向秩亏（rank-deficient）矩阵的 GPU 高效精确 SVD 算法 **HQB-Mixed SVD**：

- 利用 Householder QB 分解降低低秩 SVD 的算法复杂度
- 引入混合精度计算（FP32 低精度 + 高精度 EVD），在 GPU 架构上实现高度并行化
- 在秩为 32 时，相比英伟达 cuSOLVER 官方库加速达 6798 倍；秩 4096 时近 100 倍加速；满秩时仍有 5 倍加速
- 算法自动揭示矩阵秩，无需预设秩信息
- 精度（O(1e-07)）优于英伟达 SGESVD（O(1e-06)）

该算法在图像压缩等实际应用中验证了兼具高压缩率与高性能的潜力。

#### A Diagonal Block Memory-Aware Polynomial Preconditioner for Linear and Eigenvalue Solvers

- **作者**：Xiaojian Yang, Yuhui Ni, Fan Yuan, Shengguo Li, Dezun Dong, Xuchuan Fu, Haipeng Jia, Jie Liu (NUDT)
- **关键词**：Polynomial Preconditioner, Memory-Aware, Eigenvalue Solver

提出内存感知的对角块多项式预处理器。迭代求解器（如CG、GMRES）的收敛速度取决于矩阵的条件数，预处理器通过改善条件数加速收敛。多项式预处理器通过矩阵多项式近似逆矩阵，但其计算涉及大量矩阵-矩阵乘法，内存带宽成为瓶颈。本文利用对角块结构设计内存高效的预处理器，通过缓存感知的计算顺序和分块策略减少内存访问量，在线性和特征值求解中显著提升了收敛速度。

> **信息来源**：PPoPP 2026 官方程序 | 国防科技大学

#### A Distributed Matrix-Block-Vector Multiplication in Presence of System Performance Variability

- **作者**：Yuchen Ma, Bin Ren, Andreas Stathopoulos (College of William & Mary)
- **关键词**：Distributed Matrix Multiplication, Performance Variability

设计系统性能波动下的分布式矩阵分块-向量乘法算法。在异构集群或云环境中，各节点的实际计算性能存在波动（如CPU降频、网络拥塞、VM抢占），静态的矩阵分块策略导致快节点等待慢节点。本文提出性能变异感知的动态分块策略：运行时监测各节点的实际性能，动态调整矩阵分块大小，使各节点的计算时间趋于均衡。在存在显著性能变异的环境中实现了接近无变异环境的计算效率。

> **信息来源**：PPoPP 2026 官方程序 | William & Mary

#### Characterizing Matrix Multiplication Units across General Parallel Patterns in Scientific Computing

- **作者**：Yuechen Lu, Hongwei Zeng, Marc Casas (BSC), Weifeng Liu (CUPB)
- **关键词**：Matrix Multiplication Units, Parallel Patterns, Scientific Computing

首次系统性表征GPU矩阵乘法单元在科学计算通用并行模式下的性能特征。Tensor Core不仅可用于深度学习，还可加速科学计算中的矩阵运算（如Krylov子空间方法、预条件子计算）。本文通过微基准测试和性能建模，全面表征了Tensor Core在不同矩阵大小、数据类型、并行模式下的性能特征，包括吞吐、延迟、内存带宽利用等。这些表征结果为未来数值算法在AI加速器上的移植提供了理论基础和设计指导。

> **信息来源**：PPoPP 2026 官方程序 | 中国石油大学/BSC

---

## 11. 研究趋势与未来方向

### 11.1 AI Infra 全面占据舞台中心

PPoPP 2026 的 51 篇论文中，与 AI/ML 训练/推理直接相关的论文超过 20 篇（约占 40%），涵盖大模型训练通信优化、弹性容错、KV Cache 量化、Attention 加速、扩散模型推理、图神经网络等热点。这显著反映了 PPoPP 已从传统并行编程会议转变为 **AI 基础设施系统研究的核心发表场所**。

### 11.2 中国团队表现突出

本届 PPoPP 中，中国学术机构和工业界贡献了大量高质量论文。中科院计算所（陶鼎文团队包揽 2 篇最佳论文提名 + 1 篇入选）、清华大学（翟季冬团队 3 篇、杨广文/甘霖团队等）、北京大学（崔斌团队）、上海交通大学（陈海波团队）、北京航空航天大学（杨海龙团队 3 篇）、中国石油大学（刘伟峰团队 2 篇）等均有多篇论文被录用。电子科技大学张少帅团队的 GPU SVD 论文也取得了数千倍的性能提升。

### 11.3 GPU 仍为核心计算平台

GPU 计算持续是研究热点。Tensor Cores 的稀疏计算、稀疏 Transformer 推理、GPU 上的图算法和矩阵计算等方向均有大量高质量工作。新的硬件趋势包括 Arm SME、存内计算（PIM）、国产 AI 加速器（寒武纪）也开始出现在论文中。

### 11.4 混合精度与量化成标配

从 LLM 推理的 2-bit/3-bit 量化、KV Cache 的 2-bit 压缩到分子动力学模拟的 16-bit 混合精度，混合精度计算已在各类场景中广泛渗透，成为提升计算效率的核心手段。

### 11.5 系统+算法协同设计趋势明显

越来越多的论文采用**算法-系统协同设计**（Algorithm-System Co-design）的研究范式：不仅关注算子层的优化，更是从分布式策略搜索（Elastor）、通信-计算重叠（MetaAttention）、异常诊断全链路（CCL-D）等全局视角进行系统设计。

### 11.6 可扩展性与容错成刚需

随着训练集群规模增长至数千 GPU，训练过程中的故障诊断（CCL-D）、弹性容错恢复（Elastor）成为生产级系统不可或缺的能力。4000 GPU 集群上的部署验证成为论文的亮点。

---

## 12. 论文全索引

| # | 论文标题 | 作者 | 机构 | 关键词 | 奖项 |
|---|---------|------|------|--------|------|
| 1 | Binary Compatible Critical Section Delegation | Junyao Zhang, Zhuo Wang, Zhe Zhou | Alibaba, Fudan | Critical Section, Delegation | **Best Paper** |
| 2 | Hapax Locks: Scalable Value-Based Mutual Exclusion | Dave Dice, Alex Kogan | Independent, Oracle Labs | Value-Based Locking | |
| 3 | Fixing Non-blocking Data Structures for Better Compatibility with Memory Reclamation Schemes | Md Amit Hasan Arovi, Ruslan Nikolaev | Penn State | SMR, SCOT, Optimistic Traversal | |
| 4 | Multiverse: Transactional Memory with Dynamic Multiversioning | Gaetano Coccimiglio, Trevor Brown, Srivatsan Ravi | Waterloo, USC | TM, Multiversioning | |
| 5 | Rethinking Thread Scheduling under Oversubscription | Aleix Roca, Vicenç Beltran | BSC | Oversubscription, Multi-runtime | **Nominee** |
| 6 | Waste-Efficient Work Stealing | Kyle Singer, Kunal Agrawal, TB Schardl | MIT, WUSTL | Work Stealing | |
| 7 | DiggerBees: DFS Leveraging Hierarchical Block-Level Stealing on GPUs | Yuyao Niu, Yuechen Lu, Weifeng Liu, Marc Casas | BSC, CUPB | GPU DFS | |
| 8 | PANA: Fine-Grained Runtime-Adaptive Load Balancing for SpMV | Haodong Bian, Youhui Zhang et al. | Tsinghua | SpMV, Load Balancing | |
| 9 | UFO Trees: Practical and Provably-Efficient Parallel Batch-Dynamic Trees | Quinten De Man, Atharva Sharma, Kishen N Gowda, Laxman Dhulipala | UMD | Batch-Dynamic Trees | **Nominee** |
| 10 | Sharded Elimination and Combining for Highly-Efficient Concurrent Stacks | Ajay Singh, Nikos Metaxakis, Panagiota Fatourou | FORTH ICS, UoC | Concurrent Stack | |
| 11 | Concurrent Balanced Augmented Trees | Evan Wrench et al. | UBC, FORTH, Google | Balanced Augmented Trees | |
| 12 | Parallel Dynamic Spatial Indexes | Ziyang Men, Bo Huang, Yan Gu, Yihan Sun | UC Riverside | Spatial Index | |
| 13 | PRISM: GPU-Based Lossy Compression for Progressive Data Retrieval | Bing Lu, Zedong Liu, Dingwen Tao et al. | ICT CAS | GPU Compression | **Nominee** |
| 14 | Dynamic Detection of Inefficient Data Mapping in OpenMP (OMPDataPerf) | Luke Marzen, Junhyung Shim, Ali Jannesari | Iowa State | OpenMP, Dynamic Analysis | |
| 15 | Root-Down Exposure for Maximal Clique Enumeration on GPUs | Zhe Pan, Peng Qu, Youhui Zhang | Tsinghua | MCE, GPU | |
| 16 | ROME: Maximizing GPU Efficiency for All-Pairs Shortest Path | Weile Luo, Xiaowen Chu et al. | HKUST-GZ, HIT-SZ | APSP, GPU | |
| 17 | SPIDER: Sparse Tensor Cores for Stencil via Strided Swapping | Qiqi Gu, Jianguo Yao et al. | SJTU, Enflame | Stencil, Tensor Core | |
| 18 | ASM-SpMM: Arm SME for Sparse Matrix Multiplication | Jiazhi Jiang, Yutong Lu et al. | SYSU | Arm SME, SpMM | |
| 19 | Efficient Mapping and Pipelined Execution for SpMV on Tensor Cores | Kaige Zhang, Hailong Yang et al. | Beihang | SpMV, Tensor Core | |
| 20 | VDHA: Vector-Driven Hash Aggregation for SpM-SpV on GPUs | Yuchen Li, Zhe Pan, Youhui Zhang | Tsinghua | SpM-SpV, GPU | |
| 21 | RoMeo: Rotated Mixed Precision Quantization | Qihao Zhang, Jidong Zhai et al. | Tsinghua | Mixed Precision, Quantization | |
| 22 | High-Throughput Non-Uniformly Quantized 3-bit LLM Inference | YuAng Chen, Jeffrey Xu Yu et al. | CUHK, HKUST | 3-bit, LLM Inference | |
| 23 | JanusQuant: 2-bit KV Cache Quantization for Long-Context Inference | Chengyu Sun, Dazhao Cheng et al. | Wuhan U, Nvidia, U Macau | KV Cache, 2-bit | |
| 24 | HierCut: 16-bit Mixed Precision for Molecular Dynamics | Zeyu Song, Lin Gan et al. | Tsinghua | MD, Mixed Precision | **Best Artifact** |
| 25 | Cacheman: LLC Management for Multi-tenant Clouds | Xiaokang Hu et al. | Alibaba Cloud | LLC, Cloud | |
| 26 | zBuffer: Zero-Copy Serialization for Fast RPC | Xiangyu Liu, Huiba Li et al. | XMU, Alibaba, SJTU | Zero-Copy, RPC | |
| 27 | Scaling GPU-to-CPU Migration for CPU Clusters | Ruobing Han, Hyesoon Kim | Georgia Tech | GPU-to-CPU Migration | |
| 28 | Trojan Horse: Aggregate-and-Batch for Sparse Direct Solvers on GPU Clusters | Yida Li, Weifeng Liu et al. | CUPB | Sparse Solver, GPU Cluster | **Nominee** |
| 29 | COCCL: Compression-Aware Collective Communication for LLM Training | Xingchen Liu, Dingwen Tao et al. | ICT CAS, Ant | Communication, Compression | |
| 30 | Elastor: Elastic Model Partitioning and Checkpointing | Xuanyu Wang, Bin Cui et al. | PKU, SJTU | Fault Tolerance, Checkpoint | |
| 31 | HelixPipe: Attention Parallel Pipeline for Long Sequence Training | Geng Zhang, Yang You et al. | NUS | Long Sequence, Pipeline | |
| 32 | CCL-D: Diagnostic System for Slow/Hang Anomalies in Large-Scale Training | Yida Gu, Dingwen Tao et al. | ICT CAS, Ant | Anomaly Diagnosis | **Nominee** |
| 33 | Pipelonk: ZKP Generation on GPUs for PLONK Protocols | Zhiyuan Zhang, Lei Ju et al. | SDU, HKU, SZU | ZKP, GPU | |
| 34 | ParDiff: Parallelizing Reverse-Mode AutoDiff with Direct Indexing | Shuhong Huang, Jidong Zhai et al. | Tsinghua, Lenovo | AutoDiff, Parallel | |
| 35 | Faster and Cheaper: Sequence Alignment with Commercial CPUs | Zhonghai Zhang, Guangming Tan et al. | ICT CAS | Sequence Alignment, CPU | |
| 36 | PIM-zd-tree: Space-Partitioning Index with Processing-in-Memory | Yiwei Zhao, Phil Gibbons et al. | CMU, UCR, UMD | PIM, Spatial Index | |
| 37 | BEEMS: Machine Vision Efficiency via Computation Graph Memory Smoothing | Hanjing Shen, Li Jiang et al. | SJTU, BUAA | Machine Vision | |
| 38 | Laser: Layer-Level Scheduling for Multi-SLO LLM Serving | Jianxiong Liao, Xu Chen et al. | SYSU | LLM Serving, Scheduling | |
| 39 | MixFusion: Patch-Level Parallel Serving for Mixed-Resolution Diffusion | Desen Sun, Zepeng Zhao, Yuke Wang | Waterloo, CMU, Rice | Diffusion, Parallel Serving | |
| 40 | ChituDiffusion: Data-Characteristic-Aware Diffusion Model Serving | Chengzhang Wu, Jidong Zhai et al. | Tsinghua | Diffusion Serving | |
| 41 | ElasGNN: Elastic Training Framework for Distributed GNN | Siqi Wang, Hailong Yang et al. | Beihang | GNN Training, Elastic | |
| 42 | APERTURE: Algorithm-System Co-optimization for TGN Inference | Yiqing Wang, Hailong Yang et al. | Beihang | TGN, Co-optimization | |
| 43 | TAC: Cache-Based System for Billion-Scale GNN Training | Zhiqiang Liang et al. | CNIC CAS, Ant | GNN, Cache | |
| 44 | DTMiner: Data-Centric System for Temporal Motif Mining | Hou Yinbo, Hai Jin et al. | HUST, Warwick, HKUST | Motif Mining | |
| 45 | FlashAttention-T: Fully Tensorized Attention | Jianxing Xu, Yunji Chen et al. | USTC, CAS, Cambricon | Tensorized Attention | |
| 46 | Accelerating Sparse Transformer Inference on GPU | Wenhao Dai, Hailong Yang et al. | CUPB, Beihang, SJTU | Sparse Transformer, GPU | |
| 47 | MetaAttention: Unified Attention Framework Across Hardware Backends | Feiyang Chen, Haibo Chen et al. | SJTU, PKU, MSR | Attention, Cross-Hardware | |
| 48 | Towards SVD for Rank-Deficient Matrices on GPU (HQB-Mixed SVD) | Lu Shi, WeiWei Xu, Shaoshuai Zhang | UESTC, NUIST | SVD, GPU, Mixed Precision | |
| 49 | Diagonal Block Memory-Aware Polynomial Preconditioner | Xiaojian Yang, Jie Liu et al. | NUDT | Preconditioner, Memory-Aware | |
| 50 | Distributed Matrix-Block-Vector Multiplication under Performance Variability | Yuchen Ma, Bin Ren, Andreas Stathopoulos | William & Mary | Distributed MatMul | |
| 51 | Characterizing Matrix Multiplication Units across Parallel Patterns | Yuechen Lu, Marc Casas, Weifeng Liu | CUPB, BSC | MatMul Units, Scientific | |

---

## 13. 报告总结

PPoPP 2026 展示了并行编程与高性能计算领域的**三大范式转变**：

1. **从 HPC 到 AI Infra 的重心转移**：大模型训练和推理已成为并行编程研究的第一驱动力，通信压缩、弹性容错、KV Cache 量化、Attention 加速等方向取代了传统的科学计算优化成为新的主战场。

2. **从单点优化到系统级协同设计**：单纯的算子优化（「kernel 手工调优」）已不足以解决 AI 时代的并行挑战。研究者们开始从分布式策略搜索、通信-计算重叠调度、故障诊断全链路、跨硬件统一抽象等**全局视角**进行体系化设计。

3. **从「能用」到「好用」的工程化升级**：COCCL 通信库的「易于集成自定义压缩」、CCL-D 的「6 分钟定位故障」、Elastor 的「自适应 GPU 数量变化」等特征表明，PPoPP 的研究成果正越来越注重工程可用性和生产级部署，工业界（Alibaba、Ant Group、Microsoft Research、寒武纪等）的深度参与加速了这一趋势。

面向未来，随着 AI 模型规模的持续增长和硬件生态的不断多元化（NVIDIA/AMD/Arm/国产芯片），并行编程的系统性挑战将进一步加剧，PPoPP 作为连接**算法、系统、硬件**的核心桥梁平台，其重要性将愈加凸显。

---

*本报告由 AI 辅助生成，基于公开可获取的 PPoPP 2026 官方网站程序信息、arXiv 论文摘要、各大学/实验室官方新闻及第三方学术资讯整理而成。所有论文信息以 PPoPP 2026 官方网站 [ppopp26.sigplan.org](https://ppopp26.sigplan.org/) 为准。*