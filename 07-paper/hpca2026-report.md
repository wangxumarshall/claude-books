# HPCA 2026 洞察报告

> **会议全称**：The 32nd IEEE International Symposium on High-Performance Computer Architecture (HPCA-32)
> **会议等级**：CCF-A类（计算机体系结构/并行与分布计算/存储系统），体系结构四大顶会之一
> **时间地点**：2026年1月31日–2月4日，澳大利亚·悉尼国际会议中心 (ICC Sydney)
> **录用率**：119/602 = 19.8%
> **本报告覆盖论文**：约24篇（基于arXiv预印本、大学新闻公告等公开来源整理）

---

## 0. 会议概览

HPCA 2026（第32届IEEE高性能计算机体系结构国际研讨会）于2026年1月31日至2月4日在澳大利亚悉尼召开。本届会议共收到602篇投稿，接收119篇，录用率仅19.8%，延续了HPCA一贯的高选拔标准。作为与ISCA、MICRO、ASPLOS并列的「体系结构四大顶会」，HPCA是国际前沿芯片架构研究的风向标。

从本届论文分布来看，呈现出以下显著趋势：

1. **AI/LLM全面渗透体系结构**：大语言模型推理服务、AI Agent基础设施成本分析、推理模型调度等方向涌现大量工作，AI与体系结构的交叉已成为HPCA最大的投稿/录用主题之一。
2. **存内/近存计算进入工程化时代**：PIM（Processing-in-Memory）不再停留在概念验证阶段，动态内存分配器（PIM-malloc）、LUT-based PIM优化（LOCALUT）、SSD近数据处理（Conduit）等实用化成果亮相。
3. **量子计算体系结构快速成长**：量子纠错解码（Pinball）、分布式量子编译（DC-MBQC）等工作展现了量子计算从物理层向系统层的纵深推进。
4. **内存系统与预取技术持续创新**：行粒度DRAM访问（RoMe）、基于强化学习的预取协调（Athena）、多预取器管理（I-POP）等方向体现了内存子系统优化的持久生命力。
5. **HBM与新存储层次成为热点**：针对AI/LLM负载的HBM优化、固态硬盘近数据处理等方向受到高度关注。

---

## 1. AI/ML加速器架构

### 1.1 FractalCloud：面向大规模点云处理的分形启发式架构

- **作者**：Yuzhe Fu, Changchun Zhou, Hancheng Ye, Bowen Duan, Qiyu Huang, Chiyue Wei, Cong Guo, Hai "Helen" Li, Yiran Chen（杜克大学/匹兹堡大学）
- **论文地址**：[arXiv:2511.07665](https://arxiv.org/abs/2511.07665)

点云（Point Cloud）在自动驾驶、机器人和VR等领域应用日渐广泛。然而，基于点的神经网络（PNN）处理大规模点云时存在O(n²)计算复杂度，现有加速器因分区效率低和非并行架构而扩展性差。该工作提出**FractalCloud**——一种分形启发的硬件架构，核心贡献包括：

- **分形协同设计方法**：实现形状感知且硬件友好的分区（Fractal method）
- **块并行点操作**：将全部点操作分解并并行化
- 在28nm工艺流片，核心面积1.5 mm²，相较SOTA加速器实现**21.7倍加速**和**27倍能耗降低**，同时保持网络精度

> **点评**：点云加速器领域的前沿工作，28nm流片验证使其成果可信度较高。分形分区思路新颖，有望在自动驾驶芯片中落地。

### 1.2 LOCALUT：基于查找表的PIM DNN推理

- **作者**：Junguk Hong, Changmin Shin, Sukjin Kim, Si Ung Noh, Taehee Kwon, Seongyeon Park, Hanjun Kim, Youngsok Kim, Jinho Lee（延世大学等）
- **论文地址**：[arXiv:2604.04523](https://arxiv.org/abs/2604.04523)

利用查找表（LUT）替代算术逻辑执行DNN推理是近年兴起的新范式。该工作在DRAM-PIM架构上探索LUT的**容量-计算权衡（capacity-computation tradeoff）**，核心创新有三：

1. **LUT规范化（Canonicalization）**：消除LUT中大量冗余条目以减小存储开销
2. **重排序LUT（Reordering LUT）**：轻量级辅助LUT，将权重向量映射到规范形式
3. **LUT切片流式执行（Slice Streaming）**：利用DRAM-buffer层次仅流式传输相关LUT列并在多权重向量间复用

基于UPMEM真实设备的评估显示，**几何平均加速1.82倍**，支持多种数值精度。

> **点评**：乘积累加（MAC）→LUT查表是DNN计算范式的重要探索方向。在真实PIM硬件（UPMEM）上完成评估而非纯仿真，增强可信度。

### 1.3 AUM：释放共享处理器加速器单元的LLM推理效率潜力

- **作者**：Xinkai Wang, Chao Li, Yiming Zhuansun, Jinyang Guo, Xiaofeng Hou, Jing Wang, Luping Wang, Weigao Chen, Cheng Huang, Guodong Yang, Liping Zhang, Minyi Guo（上海交通大学等）
- **机构页面**：[SJTU SAIL Lab](https://wang-xinkai.github.io/chinese-about/)

该工作聚焦于数据中心中面向LLM服务的**共享处理器**场景——即多个LLM推理请求共享同一物理处理器资源。论文提出AUM方案，系统性地发掘加速器单元在共享环境下的效率潜力，优化LLM推理的资源调度与利用率。该工作反映了LLM推理服务从纯GPU向CPU+加速器异构场景延伸的趋势。

> **点评**：LLM推理服务是2025-2026年体系结构和系统的「超级热点」。该工作从加速器单元共享角度切入，与纯GPU推理优化形成互补。

### 1.4 PASCAL：面向推理型LLM的相位感知调度算法

- **作者**：Eunyeong Cho, Jehyeon Bang, Ranggi Hwang, Minsoo Rhu（KAIST）
- **论文地址**：[arXiv:2602.11530](https://arxiv.org/abs/2602.11530)

推理型LLM（如DeepSeek-R1等采用Chain-of-Thought推理的模型）引入了新的服务挑战：扩展推理阶段延迟了可见输出并膨胀了TTFT（首字延时）。现有推理框架无法区分推理阶段和回答阶段，导致GPU内存受限时性能退化。

**PASCAL**提出相位感知调度算法，优先推理以减少TTFT，同时在回答阶段使用受控抢占和令牌调速来保持用户体验质量。分层调度器结合了实例级布局与实例内执行，支持在阶段边界进行动态迁移以平衡负载。在DeepSeek-R1-Distill-Qwen-32B上，**尾部TTFT降低达72%**。

> **点评**：推理型LLM（Reasoning LLM）是2026年的绝对热点。该工作首次系统性地区分推理/回答两阶段的调度优化，具有重要实践意义。

### 1.5 The Cost of Dynamic Reasoning：AI Agent基础设施成本分析

- **作者**：Jiin Kim, Byeongjun Shin, Jinha Chung, Minsoo Rhu（KAIST）
- **论文地址**：[arXiv:2506.04301](https://arxiv.org/abs/2506.04301)

该文是**首篇对AI Agent进行系统级分析的论文**，量化了资源使用、延迟行为、能耗和数据中心级功耗需求。核心发现：

- AI Agent通过增加计算量提升精度，但**回报递减**效应显著
- 延迟方差扩大，基础设施成本不可持续
- 多种Agent设计选择（few-shot prompting、反思深度、并行推理）对accuracy-cost权衡产生深刻影响

论文揭示了AI Agent工作负载下隐藏的**可持续性危机**，呼吁从计算密集型推理转向计算高效型推理的范式转变。

> **点评**：随着AI Agent（如AutoGPT、CUA、Deep Research）的商业化部署，其基础设施成本将成为现实瓶颈。该工作填补了系统级成本建模的空白。

---

## 2. GPU与异构计算

### 2.1 HERO-Sign：面向后量子密码的GPU加速SPHINCS+签名

- **作者**：Yaoyun Zhou, Qian Wang
- **论文地址**：[arXiv:2512.23969](https://arxiv.org/abs/2512.23969)

SPHINCS+是一种无状态的基于哈希的后量子签名方案，但其签名生成因密集哈希计算而缓慢。该工作提出**HERO-Sign**——一种GPU加速的SPHINCS+实现：

- **Tree Fusion策略**：针对FORS组件（包含大量独立分支）自动搜索融合方案以适配不同GPU架构
- **自适应编译策略**：根据编译优化效果在PTX和原生代码路径间自动选择
- **Task Graph优化**：批量签名生成时通过任务图构建减少多流空闲时间和内核启动开销

在RTX 4090上相较SOTA GPU实现吞吐量提升**1.28-3.13倍**，在A100、H100和GTX 2080上同样获得加速，且内核启动延迟降低**两个数量级**。

> **点评**：后量子密码的GPU加速是实践性极强的工作。随着NIST后量子标准（SPHINCS+入选）的落地，此类优化将直接影响真实系统部署。

### 2.2 行业趋势：GPU+FPGA异构推理成为标准架构

虽然GPU+FPGA异构推理并非HPCA的直接论文，但2026年英伟达GTC将FPGA正式纳入AI推理标准架构的背景，与HPCA关注的异构计算趋势高度共振。Groq 3 LPX推理机架单机架配备32颗FPGA芯片，FPGA承担节点互连、动态调度、协议转换等任务，与GPU形成「GPU负责大规模并行计算，FPGA负责灵活调度与低延迟控制」的协同模式。

---

## 3. 内存与存储系统

### 3.1 Athena：基于在线强化学习的预取与片外预测协同

- **作者**：Rahul Bera, Zhenrong Lang, Caroline Hengartner, Konstantinos Kanellopoulos, Rakesh Kumar, Mohammad Sadrosadati, Onur Mutlu（ETH Zurich等）
- **论文地址**：[arXiv:2601.17615](https://arxiv.org/abs/2601.17615)

数据预取（Prefetching）和片外预测（Off-Chip Prediction, OCP）是掩藏长访存延迟的两大技术。该工作揭示了三项关键发现：(1) 两者往往互补；(2) 简单叠加无法发挥全部潜力；(3) 现有预取器控制策略留有显著改进空间。

**Athena**将预取器与OCP的协调建模为**强化学习（RL）问题**：Athena Agent观测多个系统级特征（预取/OCP准确度、带宽使用），在每个执行周期（epoch）后选择协调动作（启用/禁用/调整激进程度），并通过数值奖励持续学习策略。

在多样化内存密集型负载上，Athena在各种系统配置下一致超越现有SOTA协调策略，仅需**极低的存储开销**。

> **点评**：Onur Mutlu团队（ETH Zurich）在内存系统领域持续高产。RL用于预取器在线控制的思路正在形成趋势（参考同届的I-POP）。该论文代码已开源。

### 3.2 I-POP：点燃有效预取

- **作者**：林溢泉等（浙江大学计算机系统结构实验室ARClab），陈文智教授、王总辉老师指导
- **机构页面**：[ZJU ARClab](http://arc.zju.edu.cn/2025/1202/c62503a3112759/page.htm)

现代处理器集成多种硬件预取器以覆盖更多缓存缺失模式。然而，多预取器未经管理时反而可能导致**IPC下降24.3%**。现有方案存在静态死板、强化学习开销大、基于性能计数器的指标与IPC相关性弱等局限。

**I-POP**引入「**预取有效性（Prefetch Effectiveness, PE）**」新指标，统一量化预取行为的三种效应：
1. 正面效益：准确及时预取减少缺失
2. 负面代价一：缓存污染
3. 负面代价二：预取请求与常规访问竞争共享资源

硬件组件仅需**1.46 KB**存储开销，相较SOTA方案Bandit和Alecto，单核IPC提升**3.5-4.2%**，多核提升**8.4-8.6%**。

> **点评**：浙江大学ARClab已连续4年被HPCA录用（HPCA 2023-2026），在国内体系结构领域处于领先梯队。PE指标的提出是核心创新——解决了准确率/覆盖率与IPC弱相关的痛点。

### 3.3 RoMe：面向大语言模型的行粒度访问内存系统

- **作者**：Hwayong Nam, Seungmin Baek, Jumin Kim, Michael Jaemin Kim, Jung Ho Ahn（首尔大学）
- **论文地址**：[arXiv:2512.01541](https://arxiv.org/abs/2512.01541)

HBM-based内存系统虽历经多代演进，但一直保持**缓存行粒度（32B）访问**。为保留细粒度访问而引入的bank group和pseudo channel增加了时序参数和控制开销，内存控制器调度极度复杂。

LLM工作负载以连续大数据块（数KB到MB级）流式访问为主。**RoMe**提出以**行粒度访问DRAM**，从接口移除列、bank group和pseudo channel，简化调度并释放引脚。空闲引脚汇聚形成额外通道，**带宽提升12.5%**，硬件开销极小。

> **点评**：该工作抓住了关键矛盾：通用DRAM接口为通用场景设计，而LLM主导的数据中心场景需要不同的设计取向。这是「领域专用内存系统」方向的重要探索。

### 3.4 PIM-malloc：PIM架构的快速可扩展动态内存分配器

- **作者**：Dongjae Lee, Bongjoon Hyun, Youngjin Kwon, Minsoo Rhu（KAIST）
- **论文地址**：[arXiv:2505.13002](https://arxiv.org/abs/2505.13002)

动态内存分配是现代编程语言的基础功能，但当前通用PIM设备对此支持不足。该工作对PIM内存分配器进行设计空间探索，提出**PIM-malloc**：

- 在真实PIM硬件上实现**66倍**内存分配性能提升
- 进一步设计轻量级per-PIM核心硬件缓存，额外获得**31%性能提升**
- 开发代表性PIM工作负载验证可编程性增强效果

> **点评**：PIM从「能做计算」走向「能写程序」的工程化里程碑。动态内存分配的支持是PIM走向通用编程的关键一步。

### 3.5 Conduit：SSD多计算资源的程序员透明近数据处理

- **作者**：Rakesh Nadig, Vamanan Arulchelvan, Mayank Kabra, Harshita Gupta, Rahul Bera, Nika Mansouri Ghiasi, Nanditha Rao, Qingcai Jiang, Andreas Kosmas Kakolyris, Yu Liang, Mohammad Sadrosadati, Onur Mutlu（ETH Zurich等）
- **论文地址**：[arXiv:2601.17633](https://arxiv.org/abs/2601.17633)

SSD天然适合近数据处理（NDP），因为它同时支持三种NDP范式：**in-storage processing (ISP)、processing using DRAM in SSD (PuD-SSD)、in-flash processing (IFP)**。但现有技术各自孤立运行。

**Conduit**提出了通用、程序员透明的SSD NDP框架：
- **编译时**：自定义LLVM pass将应用代码SIMD向量化并与SSD页布局对齐，嵌入元数据指导运行时决策
- **运行时**：SSD内部执行**指令粒度**的offloading决策，评估6个关键特征并通过代价函数选择最优SSD资源

评估表明相较最佳现有offloading策略**加速1.8倍**，**能耗降低46%**。

> **点评**：将SSD从被动存储升级为主动计算节点的趋势加速。Conduit利用了SSD内部异构计算资源（ISP+PuD+IFP）的完整集合，指令粒度offloading是其独特之处。

### 3.6 Breaking the HBM Bit Cost Barrier：面向AI推理基础设施的领域专用ECC

- **作者**：Rui Xie, Asad Ul Haq, Yunhua Fang, Linsen Ma, Sanchari Sen, Swagath Venkataramani, Liu Liu, Tong Zhang（伦斯勒理工学院、IBM）
- **论文地址**：[arXiv:2507.02654](https://arxiv.org/abs/2507.02654)

HBM成本高企（$5-10倍于普通DRAM/GB）威胁AI基础设施的可扩展性。该工作从**系统架构视角**探索通过放松HBM原始可靠性要求来降低成本：消除片上ECC，将所有故障管理转移到内存控制器。

创新包括：
- **大码字Reed-Solomon (RS)纠错 + 细粒度CRC检测**的混合ECC
- **差分奇偶校验更新**以缓解写放大
- **基于数据重要性的可调保护**（低敏感数据如尾数可省略ECC）

即使在HBM原始误码率达**10⁻³**的极端条件下，系统仍保持**78%以上吞吐量和97%模型精度**。

> **点评**：「将可靠性视为可调系统参数而非固定硬件约束」是核心理念。该工作与RoMe论文形成互补——均在LLM负载特性下重新审视DRAM/HBM的设计假设。

---

## 4. 互连与网络架构

> 注：HPCA 2026中纯互连/网络方向的公开论文相对较少，但Chiplet/D2D互连和光学互连在行业层面是2026年的核心趋势。以下梳理行业背景并结合会议上可追踪的相关动态。

### 4.1 行业趋势：Chiplet与UCIe互连

2026年，Chiplet技术从数据中心服务器向高端移动设备、自动驾驶车载芯片渗透。UCIe（通用芯粒互连技术）标准化持续推进，AMD、英特尔、台积电共同推动。OpenAI的专利展示了使用嵌入式逻辑桥（如Intel EMIB）连接20个HBM堆栈的AI芯片设计。

### 4.2 ChipLight：面向LLM训练的光学互连Chiplet跨层优化

- **作者**：Kangbo Bai, Zhantong Zhu, Yifan Ding, Tianyu Jia
- **论文地址**：[arXiv:2604.18909](https://arxiv.org/abs/2604.18909)

虽然该工作被DATE 2026接收而非HPCA，但其主题与HPCA高度相关：Chiplet技术用于Scale-Up节点性能增强，光学互连（OI）用于Scale-Out网络的高带宽长距离通信。ChipLight提出跨层多目标设计优化方法，联合优化Chiplet架构、训练并行策略和OI网络拓扑，为未来训练集群设计提供洞见。

---

## 5. 近存/存内计算（PIM/NDP）

本节内容与第3节（内存与存储系统）有交叉。已在第3节详细介绍的PIM论文在以下仅做分类索引：

| 论文 | 核心方向 | 关键词 |
|------|---------|--------|
| [LOCALUT](#12-localut基于查找表的pim-dnn推理) | LUT-based PIM DNN推理 | DRAM-PIM, UPMEM |
| [PIM-malloc](#34-pim-mallocpim架构的快速可扩展动态内存分配器) | PIM动态内存分配器 | 通用PIM, 可编程性 |
| [Conduit](#35-conduitssd多计算资源的程序员透明近数据处理) | SSD近数据处理 | ISP, PuD, IFP |

> 注：PIM/NDP/PUD（Processing-Using-DRAM）领域是HPCA的持续热点。本届论文反映了从概念验证→工程化→系统级部署的演进路径。

---

## 6. 量子计算体系结构

### 6.1 Pinball：面向电路级噪声的量子纠错低温预解码器

- **作者**：Alexander Knapen, Guanchen Tao, Jacob Mack, Tomas Bruno, Mehdi Saligane, Dennis Sylvester, Qirui Zhang, Gokul Subramanian Ravi（密歇根大学等）
- **论文地址**：[arXiv:2512.09807](https://arxiv.org/abs/2512.09807)

可扩展容错量子计算机面临数据处理和功耗的严峻挑战。低温预解码（使用轻量级逻辑处理常见稀疏错误）是解决瓶颈的方向之一，但先前工作仅考虑部分错误源且在超导SFQ逻辑上实现受限。

**Pinball**在**低温CMOS**中实现了全面考虑电路级噪声的QEC预解码器：
- 相较SOTA低温预解码器，逻辑错误率（LER）提升**近6个数量级**
- 相较常温预解码器，LER降低**32.58倍**
- Syndrome带宽降低达**3780.72倍**
- 基于22nm FDSOI工艺，峰值功耗**<0.56 mW**
- 电压/频率缩放和体偏置使典型功耗再降**22.2倍**

在4K温度下1.5W功耗预算内，支持**2668个逻辑量子比特（距离d=21）**。

> **点评**：量子纠错解码中的系统架构探索——将低温CMOS与QEC工作负载特征协同优化。该工作不仅理论扎实，更在真实工艺参数下完成评估，是HPCA量子方向高质量的典范。

### 6.2 DC-MBQC：面向基于测量的量子计算的分布式编译框架

- **作者**：Yecheng Xue, Rui Yang, Zhiding Liang, Tongyang Li（北京大学）
- **机构解读**：[BAAI智源](https://hub.baai.ac.cn/view/51714)
- **论文地址**：[arXiv:2601.00214](https://arxiv.org/abs/2601.00214)

这是**首个**专为基于测量的量子计算（MBQC）设计的分布式编译框架。MBQC是光量子计算平台最自然的计算范式，但与量子电路模型截然不同，现有分布式编译器无法直接应用。

核心贡献：
1. **「所需光子寿命」指标**：将延迟线中光子存储需求统一量化，作为编译器性能的物理感知指标
2. **自适应图划分算法**：在保持图态结构的同时平衡QPU间负载
3. **层调度（Layer Scheduling）问题形式化**：证明其HP-hardness并提出瓶颈驱动迭代调度算法

在8个全互连QPU设置下，相较单QPU编译器所需光子寿命优化**7.46倍**，执行速度提升**6.82倍**。

> **点评**：光量子计算是量子计算的重要分支，但系统级研究极为稀缺。该工作首次跨越了光量子物理特性与分布式系统设计之间的鸿沟。

---

## 7. 处理器架构与微架构

### 7.1 预取器管理（Athena & I-POP）

已在第3节详细介绍。Athena和I-POP分别从强化学习和「预取有效性」指标两个不同角度解决多预取器的协同管理问题。I-POP以其极低的硬件开销（1.46 KB）展示了实际部署的可行性。

### 7.2 AUM：共享处理器LLM推理加速

已在第1.3节介绍。体现了LLM推理从GPU向CPU+加速器拓展的异构化趋势。

---

## 8. 数据服务与系统

### 8.1 2026年AI算力芯片行业全景

虽然不属于HPCA直接论文，但2026年的宏观行业背景为理解HPCA论文方向提供了重要参照：

- **推理算力占比超70%**：是训练算力的4.5倍，成为行业核心引擎
- **ASIC定制芯片增长率44.6%**：远超GPU的16.1%
- **Chiplet成为主流**：英伟达Rubin平台采用Chiplet架构
- **液冷成为标配**：单机柜功率突破240kW
- **HBM成本危机**：HBM成本5-10倍于普通DRAM/GB，推动HPCA上RoMe和Domain-Specific ECC等方向

---

## 9. 结语与未来方向

### 9.1 HPCA 2026的五大趋势

1. **AI从工作负载变为体系结构的「第一性原理」**：LLM推理服务、AI Agent基础设施、推理型LLM调度等方向表明，AI不再仅仅是加速器设计的目标负载，而是正在重塑整个计算栈——从内存接口（RoMe）到可靠性策略（Domain-Specific ECC）。

2. **PIM从Demo走向工程化**：PIM-malloc（动态内存分配）、LOCALUT（LUT-based DNN推理）、Conduit（SSD智能offloading）等论文的共同特征是——不在仿真器上论证概念，而是在真实硬件（UPMEM、SSD模拟器）上实现完整的系统原型。PIM正在度过「从0到1」的阶段，进入「从1到N」的工程化时期。

3. **多预取器协调成为显学**：Athena（ETH Zurich/Onur Mutlu）和I-POP（浙江大学）同时入选HPCA 2026，从RL和启发式两个角度解决相同问题。这暗示多预取器协调已成为学界共识性挑战。

4. **量子体系结构走向系统级**：Pinball（低温CMOS QEC解码器）和DC-MBQC（分布式MBQC编译）分别从物理实现和编译框架两个层面推进量子计算的系统化。HPCA作为体系结构顶会对量子方向的包容性在增强。

5. **「可持续性」从口号变为硬约束**：The Cost of Dynamic Reasoning 论文对AI Agent的能耗分析揭示：Agent推理的边际回报递减，基础设施成本不可持续。这与行业对数据中心功耗危机（2027年需额外92GW电力）的关注形成呼应。

### 9.2 中国学术力量在HPCA 2026

本届会议中，中国高校表现亮眼：

| 机构 | 论文 | 方向 |
|------|------|------|
| 浙江大学 | I-POP | 预取器管理 |
| 上海交通大学 | AUM | LLM推理服务 |
| 北京大学 | DC-MBQC | 分布式量子编译 |
| 清华大学/中科院/香港科大 | (HPCA 2025最佳论文荣誉提名延续) | 近内存计算编译工具链 |

浙江大学ARClab已连续4年（2023-2026）被HPCA录用，显示了国内体系结构方向持续性产出的能力。

### 9.3 未来方向展望

- **LLM推理的体系结构创新**：从KV-cache管理到推理阶段调度，LLM推理将成为体系结构研究未来2-3年的核心驱动力。
- **领域专用内存系统**：HBM的「领域专用化」（如RoMe的行粒度访问、领域专用ECC）将成为一个独立子方向。
- **Chiplet同构/异构集成的编译与调度**：随着Chiplet成为主流封装范式，如何在Chiplet间高效分配计算/通信资源将成为关键问题。
- **Agent基础设施的效能优化**：AI Agent的multi-turn推理带来的延迟-成本-精度三角权衡，需要系统级的解决方案。
- **量子-经典混合系统架构**：随着量子计算机逐步实用化，如何设计经典-量子混合计算系统将是一个新的体系结构前沿。

---

## 论文索引表

| 序号 | 论文简称 | 全文标题 | 机构 | 类别 | 论文地址 |
|------|---------|---------|------|------|---------|
| 1 | FractalCloud | A Fractal-Inspired Architecture for Efficient Large-Scale Point Cloud Processing | Duke/Pitt | AI加速器 | [arXiv:2511.07665](https://arxiv.org/abs/2511.07665) |
| 2 | LOCALUT | Harnessing Capacity-Computation Tradeoffs for LUT-Based Inference in DRAM-PIM | Yonsei/SNU | PIM/AI加速器 | [arXiv:2604.04523](https://arxiv.org/abs/2604.04523) |
| 3 | AUM | Unleashing the Efficiency Potential of Shared Processors with Accelerator Units for LLM Serving | SJTU | LLM推理 | (HPCA 2026) |
| 4 | PASCAL | A Phase-Aware Scheduling Algorithm for Serving Reasoning-based LLMs | KAIST | LLM推理 | [arXiv:2602.11530](https://arxiv.org/abs/2602.11530) |
| 5 | Cost of DR | The Cost of Dynamic Reasoning: Demystifying AI Agents and Test-Time Scaling | KAIST | AI Agent | [arXiv:2506.04301](https://arxiv.org/abs/2506.04301) |
| 6 | HERO-Sign | Hierarchical Tuning and Efficient Compiler-Time GPU Optimizations for SPHINCS+ | - | GPU/后量子密码 | [arXiv:2512.23969](https://arxiv.org/abs/2512.23969) |
| 7 | Athena | Synergizing Data Prefetching and Off-Chip Prediction via Online RL | ETH Zurich | 内存系统 | [arXiv:2601.17615](https://arxiv.org/abs/2601.17615) |
| 8 | I-POP | Ignite Positive Prefetchers | ZJU | 预取器管理 | (HPCA 2026, [ARClab](http://arc.zju.edu.cn/2025/1202/c62503a3112759/page.htm)) |
| 9 | RoMe | Row Granularity Access Memory System for LLMs | SNU | HBM/内存系统 | [arXiv:2512.01541](https://arxiv.org/abs/2512.01541) |
| 10 | PIM-malloc | A Fast and Scalable Dynamic Memory Allocator for PIM Architectures | KAIST | PIM | [arXiv:2505.13002](https://arxiv.org/abs/2505.13002) |
| 11 | Conduit | Programmer-Transparent Near-Data Processing Using Multiple Compute-Capable Resources in SSDs | ETH Zurich | SSD/NDP | [arXiv:2601.17633](https://arxiv.org/abs/2601.17633) |
| 12 | HBM-ECC | Breaking the HBM Bit Cost Barrier: Domain-Specific ECC for AI Inference Infrastructure | RPI/IBM | HBM/可靠性 | [arXiv:2507.02654](https://arxiv.org/abs/2507.02654) |
| 13 | Pinball | A Cryogenic Predecoder for Quantum Error Correction Decoding Under Circuit-Level Noise | UMich | 量子计算 | [arXiv:2512.09807](https://arxiv.org/abs/2512.09807) |
| 14 | DC-MBQC | A Distributed Compilation Framework for Measurement-Based Quantum Computing | PKU | 量子计算 | [arXiv:2601.00214](https://arxiv.org/abs/2601.00214) |

> **说明**：以上论文列表基于arXiv预印本、大学新闻公告、个人学术主页等公开来源整理。由于HPCA 2026官方论文集（Proceedings）在报告编写时尚未完全公开可检索，可能存在收录偏差。部分论文标注为「(HPCA 2026)」表示在机构新闻或个人主页中确认被接收，但暂未检索到arXiv版本。

---

*报告生成日期：2026年6月10日*
*作者：基于SOLO AI编程助手自动检索、阅读与整理*