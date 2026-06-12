# 2026年系统软件CCF-A类顶会综合对比分析

> **分析范围**: EuroSys 2026、FAST 2026、NSDI 2026、ASPLOS 2026、ICSE 2026、HPCA 2026、PPoPP 2026、POPL 2026
> **数据来源**: 各会议洞察报告
> **分析日期**: 2026年6月10日

> ⚠️ **注意**: ICSE 2026 聚焦软件工程（系统软件相关 Track），POPL 2026 聚焦编程语言理论（系统软件相关论文），二者非纯粹系统会议，对比数据侧重与系统方向的交叉部分。

---

## 一、各会议概览对比

| 维度 | EuroSys 2026 | FAST 2026 | ASPLOS 2026 | NSDI 2026 | ICSE 2026 | HPCA 2026 | PPoPP 2026 | POPL 2026 |
|------|-------------|-----------|-------------|-----------|-----------|-----------|------------|-----------|
| **全称** | European Conf. on Computer Systems | USENIX Conf. on File and Storage Technologies | Int'l Conf. on Architectural Support for PL and OS | USENIX Symp. on Networked Systems Design and Impl. | Int'l Conf. on Software Engineering | Int'l Symp. on High-Performance Computer Architecture | Symp. on Principles and Practice of Parallel Programming | Symp. on Principles of Programming Languages |
| **届次** | 第21届 | 第24届 | - | 第23届 | 第48届 | 第32届 | 第31届 | - |
| **投稿数** | ~404（两轮合计） | 253 | ~1048（两轮合计） | ~608（Spring 207 + Fall ~401） | 1,469 | 602 | 280 | 未公开 |
| **录用数** | 79 | 44 | ~152 | ~105（Spring 50 + Fall ~55） | 321 | 119 | 51 | 未公开 |
| **录用率** | ~19.6% | 17.4% | ~14.5% | Spring 24.2% / Fall ~13.7% / 综合~17% | ~21.85% | 19.8% | 18.2% | 未公开 |
| **举办时间** | 2026年4月27日–30日 | 2026年2月24日–26日 | 2026年3月22日–26日 | 2026年5月4日–6日 | 2026年4月12日–18日 | 2026年1月31日–2月4日 | 2026年1月31日–2月4日 | 2026年1月 |
| **举办地点** | 英国·爱丁堡 | 美国·圣克拉拉 | 美国·匹兹堡 | 美国·华盛顿州 Renton | 巴西·里约热内卢 | 澳大利亚·悉尼 | 澳大利亚·悉尼 | - |
| **核心方向** | 通用系统（OS/存储/网络/分布式/安全） | 存储系统（文件系统/云存储/键值存储） | 体系结构/OS/编程语言交叉 | 网络系统（数据中心网络/AI网络/高性能网络） | 软件工程（测试/分析/安全/AI+SE） | 体系结构（AI加速器/内存系统/量子计算） | 并行编程（并发/GPU/ML训练/ML推理） | 编程语言理论（类型系统/形式化验证/分离逻辑） |
| **论文覆盖** | ~131篇全量解读 | 14/44篇详细解读 | 14/152篇详细解读 | 22篇详细解读 | ~30篇系统相关论文解读 | ~24篇解读 | 51篇全量解读 | 11篇系统相关论文解读 |
| **审稿机制** | 双轮审稿（秋轮+春轮） | 单轮 | 双轮审稿（春轮+夏轮） | 双轮审稿（Spring+Fall） | 双轮（Research Track） | 单轮 | 单轮 | 单轮 |
| **Best Paper / 杰出论文** | 2篇 Best Paper（含候选） | 2篇 Best Paper + 3篇 Distinguished Artifact | 未获取 | 3篇 Outstanding Paper + 1项 Community Award | 22篇 ACM SIGSOFT 杰出论文（6.9%） | 未获取 | 1篇 Best Paper + 1篇 Best Artifact + 5篇提名 | 未获取 |

### 关键观察

1. **录用率梯度明显**: ASPLOS（~14.5%）< FAST（17.4%）< NSDI（~17%）< PPoPP（18.2%）< EuroSys（~19.6%）< HPCA（19.8%）< ICSE（~21.85%）。ASPLOS 因投稿基数最大，竞争最为激烈；ICSE 虽投稿量最大（1,469篇），但录用率最高。

2. **时间线分布**: 八个会议在2026年1-5月密集举办。HPCA/PPoPP/POPL集中在1月底-2月初的悉尼（联合举办），形成"春节档超级周"；FAST（2月）→ ASPLOS（3月）→ ICSE/EuroSys（4月）→ NSDI（5月）几乎每月一会。

3. **双轮审稿成为主流**: EuroSys、ASPLOS、NSDI、ICSE 均采用双轮审稿机制，FAST、HPCA、PPoPP、POPL 保持单轮。

4. **论文规模差异显著**: ICSE（321篇）规模最大，ASPLOS（~152篇）次之，FAST（44篇）最为精简。

5. **HPCA/PPoPP/POPL联合举办效应**: 三个会议同在悉尼ICC举办，参会者可一站式覆盖体系结构、并行编程和编程语言三大领域。

---

## 二、研究方向侧重对比

### 2.1 各会议主题热力图

| 研究方向 | EuroSys | FAST | NSDI | ICSE | HPCA | PPoPP | POPL |
|----------|:-------:|:----:|:----:|:----:|:----:|:-----:|:----:|
| **AI/LLM 系统基础设施** | 趋势级 | ★★★★★ | ★★★★★ | — | ★★★★★ | ★★★★ | — |
| **存储系统** | ★★★★ | ★★★★★ | ★★ | — | ★★★ | ★ | — |
| **文件系统** | ★★★ | ★★★ | — | — | — | — | — |
| **网络系统（数据中心/传输）** | ★★★ | — | ★★★★ | — | ★★ | — | — |
| **分布式系统/并发控制** | ★★★ | ★ | ★ | — | — | ★★★★ | — |
| **RDMA/高性能网络** | ★★★ | — | ★★★ | — | — | — | — |
| **安全/机密计算/隔离** | ★★★ | — | ★★ | ★★★ | — | — | — |
| **硬件-软件协同设计** | ★★★★ | ★★★★ | ★★★ | — | ★★★★★ | ★★★ | — |
| **LLM 辅助系统开发（AI for Systems）** | — | ★★★ | ★★ | ★★★★★ | — | — | — |
| **软件测试/Fuzzing** | — | — | — | ★★★★★ | — | — | — |
| **程序分析与形式化验证** | — | — | — | ★★★★ | — | — | ★★★★★ |
| **并发与并行编程** | — | — | — | — | — | ★★★★★ | ★★★★ |
| **GPU/加速器计算** | — | — | — | — | ★★★★★ | ★★★★★ | — |
| **PIM/NDP 存内计算** | ★★ | — | — | — | ★★★★ | ★★ | — |
| **量子计算体系结构** | — | — | — | — | ★★★ | — | — |
| **混合精度/量化** | — | — | — | — | — | ★★★★ | — |
| **类型系统/编程语言理论** | — | — | — | — | — | — | ★★★★★ |

### 2.2 各会议独特标签

**EuroSys 2026 —「系统设计哲学」**
体现清晰的工程哲学："消除冗余"（FastDelta）、"机会主义消序"（ChimeraFS）、"安全与性能双高"（Pyramid）。EuroSys 偏爱有方法论深度的系统工作。

**FAST 2026 —「AI + Storage 深度融合」**
从「AI for Storage」（SYSSPEC）到「Storage for AI」（Tutti、GCR、SolidAttention），形成完整的双向闭环。

**NSDI 2026 —「AI 定义网络」**
约35%论文围绕AI/ML训练推理的网络系统问题，AI工作负载特征正在重新定义网络系统设计范式。

**ICSE 2026 —「LLM 重塑软件工程」**
LLM与程序分析、形式化验证、符号执行的深度融合成为最有效路径。智能体化测试与修复全面爆发。

**HPCA 2026 —「AI 成为体系结构第一性原理」**
AI不再仅是加速器目标负载，而是重塑整个计算栈——从内存接口（RoMe）到可靠性策略（领域专用ECC）到Agent成本分析。

**PPoPP 2026 —「从 HPC 到 AI Infra 的重心转移」**
约40%论文与AI/ML直接相关，同时坚守并发数据结构、任务调度等传统优势方向。

**POPL 2026 —「形式化方法下沉至系统代码」**
Miri对Rust unsafe UB检测已成Rust for Linux核心安全网；Musketeer/Angelic将并行验证从状态爆炸中解放；TypeDis将disentanglement保证降为自动类型检查。

### 2.3 交叉覆盖对比

**AI/LLM 推理存储** - 同时出现在 FAST、NSDI 和 PPoPP：
- FAST: Tutti（GPU io_uring KV Cache）、SolidAttention（端侧 SSD 推理）
- NSDI: DroidSpeak（跨微调模型 KV Cache 共享）、ServeGen（推理负载建模）
- PPoPP: Laser（层级调度LLM Serving）、JanusQuant（2-bit KV Cache量化）、FlashAttention-T（Tensor化Attention）
- **差异**: FAST侧重存储层I/O路径，NSDI侧重网络层Cache共享，PPoPP侧重并行计算优化。三者互补。

**并发编程与形式化验证** - 同时出现在 PPoPP 和 POPL：
- PPoPP: Binary Compatible Critical Section Delegation（Best Paper）、Waste-Efficient Work Stealing
- POPL: Musketeer/Angelic（内部确定性并行验证）、TypeDis（解缠性类型系统）、Channel Complexity
- **差异**: PPoPP侧重工程实现，POPL侧重理论基础。

**LLM 辅助系统开发（AI for Systems）**:
- FAST: SYSSPEC（Best Paper）
- NSDI: Eywa
- ICSE: SAINT、CodeCureAgent、OScope、USEagent 等大量工作

**硬件-软件协同** - 同时出现在 EuroSys、FAST、HPCA 和 PPoPP：
- EuroSys: ChimeraFS、RDMA分布式锁
- FAST: PolarStore、阿里云本地存储三代演进
- HPCA: FractalCloud、LOCALUT、Conduit
- PPoPP: MetaAttention（跨硬件后端统一Attention）

---

## 三、跨会议共性技术趋势（2026年系统软件五大趋势）

### 趋势一：AI 工作负载重塑底层系统设计——从"适配"到"原生"

| 会议 | AI-Native 系统工作 | 核心思想 |
|------|-------------------|---------|
| FAST | Tutti（GPU io_uring KV Cache）、GCR、SolidAttention、Grouped I/O API | 存储栈从 CPU-centric 转向 GPU-centric |
| NSDI | HeteCCL、ForestColl、EROICA、DroidSpeak、ServeGen | 网络栈原生支持 AllReduce 通信、异构GPU拓扑 |
| HPCA | RoMe（行粒度DRAM）、PASCAL（推理型LLM调度）、Domain-Specific ECC | 内存接口围绕LLM负载重新设计 |
| PPoPP | Elastor（弹性容错训练）、COCCL（压缩通信库）、FlashAttention-T | 并行编程范式为LLM训练/推理重塑 |
| EuroSys | Agent/LLM 系统启示 | 面向AI Agent的系统设计原则 |

### 趋势二：异构性从"例外"变为"默认假设"

| 会议 | 相关论文 | 异构维度 |
|------|---------|---------|
| NSDI | HeteCCL、ForestColl、BURST | GPU型号异构、网络异构、网卡异构 |
| FAST | PolarStore | 压缩硬件异构 |
| HPCA | GPU+FPGA异构推理 | 计算硬件异构 |
| PPoPP | MetaAttention | GPU后端异构（NVIDIA/AMD/寒武纪） |

### 趋势三：硬软件协同设计从"优化手段"升级为"核心方法论"

| 会议 | 代表工作 | 协同模式 |
|------|---------|---------|
| EuroSys | ChimeraFS | 文件系统感知PM硬件拓扑 |
| FAST | 阿里云本地存储、PolarStore | 纯软件→DPU→ASIC+SoC演进 |
| NSDI | Octopus、SONiC DASH | CXL稀疏直连拓扑、SmartSwitch流水线 |
| HPCA | Conduit | SSD内部ISP+PuD+IFP指令粒度offloading |
| PPoPP | FlashAttention-T | Tensor-Vector并行性适配国产AI芯片 |

### 趋势四："语义穿透"——让上层应用意图直达系统底层

| 会议 | 论文 | 语义穿透方式 |
|------|------|------------|
| FAST | Grouped I/O API | AI框架向存储传递"I/O分组意图" |
| FAST | PolarStore | 数据库页面类型语义指导压缩策略 |
| NSDI | OSCAR、DroidSpeak | 延迟梯度信号近似INT、微调知识复用KV Cache |
| ICSE | OScope、R-Log | 运维SOP编码为LLM诊断链、13套推理模板 |

### 趋势五：工业级实证研究成为系统顶会的"硬通货"

| 会议 | 代表性工业论文 | 部署规模 | 获得荣誉 |
|------|--------------|---------|---------|
| FAST | 阿里云本地存储三代演进 | 三代商业化产品、生产集群 | 🏆 Best Paper |
| FAST | PolarStore（阿里云） | 数千台存储服务器、100+ PB | Best Paper Candidates |
| NSDI | EROICA（阿里云） | 覆盖全部训练集群、1.5年生产运行 | — |
| NSDI | SONiC DASH（Microsoft） | Azure生产环境 | 🏆 Community Award |
| EuroSys | Pyramid（蚂蚁/清华/南开） | 支付宝生产集群 | — |
| ICSE | OScope（南开/阿里/清华） | 阿里生产环境3个月+、诊断67个故障 | 🏆 杰出论文 |
| PPoPP | CCL-D（中科院计算所/蚂蚁） | 4000 GPU集群部署一年 | 🏆 Best Paper Nominee |
| PPoPP | Cacheman（阿里云） | 阿里云多租户云环境 | — |

---

## 四、中国团队表现对比

### 4.1 整体统计

| 维度 | EuroSys 2026 | FAST 2026 | NSDI 2026 | ICSE 2026 | HPCA 2026 | PPoPP 2026 | POPL 2026 |
|------|:-----------:|:---------:|:---------:|:---------:|:---------:|:----------:|:---------:|
| **中国团队参与论文比例** | 6篇中5篇为中国主导 | 14篇中12篇（85.7%） | 22篇中~10篇（~45%） | 多篇获奖 | ~4篇 | 51篇中~30+篇 | ~2篇 |
| **Best Paper / 杰出论文** | 1篇候选（ChimeraFS） | 2篇 Best Paper + 2篇 Distinguished Artifact | 1篇 Outstanding Paper（OSCAR） | 多个杰出论文（北大×2、浙大、北理工、扬州大学） | 未获取 | 1篇 Best Paper（复旦/阿里）、1篇 Best Artifact（清华）、多篇提名 | — |
| **企业深度参与** | 华为、蚂蚁/支付宝 | 阿里云（3篇）、字节跳动（1篇）、麒麟软件（1篇） | 阿里云（6篇）、字节跳动（1篇） | 阿里（OScope）、华为（R-Log） | — | 阿里云（2篇）、蚂蚁（2篇）、寒武纪 | — |
| **高校表现突出** | 哈工大深圳（2篇）、南航/北航/南大/南开/清华/苏大 | 上海交大（5篇）、清华（3篇）、哈工大深圳（1篇） | 南京大学（Outstanding）、东北大学（首中NSDI）、湖南大学、浙大 | 北大（2篇杰出论文）、浙大（1篇）、南开（3篇SEIP）、华中科大 | 浙大（I-POP）、上海交大（AUM）、北大（DC-MBQC） | 中科院计算所（陶鼎文3篇）、清华（翟季冬3篇+甘霖等）、北大（崔斌）、上海交大（陈海波）、北航（杨海龙3篇） | 上海交大（Fu团队）、中科院软件所 |

### 4.2 高校/机构表现亮点

**上海交通大学** — 2026年系统顶会的最大赢家
- FAST 2026: 5篇（IPADS 4篇 + OASIS 1篇），含 1 篇 Best Paper + Distinguished Artifact、1 篇 Best Paper、1 篇 Distinguished Artifact
- PPoPP 2026: MetaAttention（IPADS陈海波团队）
- HPCA 2026: AUM（LLM推理服务）
- ICSE 2026: EvoC2Rust
- 跨FAST、PPoPP、HPCA、ICSE四大顶会的统治性表现

**中科院计算所** — PPoPP 2026最大赢家
- 陶鼎文团队包揽2篇 Best Paper Nominee（PRISM + CCL-D）+ COCCL通信库
- 陈云霁/郭琦团队 FlashAttention-T（国产AI芯片Attention加速）

**清华大学** — 多会议全面覆盖
- FAST 2026: 3篇（GPU C/R 获 Distinguished Artifact、磁带归档、DisCoGC）
- PPoPP 2026: 翟季冬团队3篇 + 甘霖团队 HierCut（Best Artifact）+ 张悠慧团队3篇GPU论文
- NSDI 2026: 参与 ForestColl

**北京大学** — ICSE + HPCA + PPoPP 三开花
- ICSE 2026: 2篇 SIGSOFT 杰出论文奖（HoarePrompt、SEAlign）+ 多篇入选
- HPCA 2026: DC-MBQC（分布式量子编译）
- PPoPP 2026: Elastor（崔斌团队弹性容错训练）

**阿里云** — 企业研究能力的标杆
- FAST 2026: 3篇、NSDI 2026: 6篇、ICSE 2026: OScope、PPoPP 2026: Cacheman + zBuffer
- **10+篇顶会论文**的规模在单一企业中极为罕见

### 4.3 值得关注的新势力

| 团队 | 会议 | 意义 |
|------|------|------|
| 东北大学（HeteCCL） | NSDI 2026 | 首篇 NSDI 主会论文 |
| 麒麟软件（CoFS） | FAST 2026 | 国产OS厂商首次在FAST发表论文 |
| 扬州大学（LoopRepair） | ICSE 2026 | 获 ACM SIGSOFT 杰出论文奖 |
| 电子科技大学（HQB-Mixed SVD） | PPoPP 2026 | GPU SVD算法数千倍加速 |
| 中国石油大学-北京（Trojan Horse） | PPoPP 2026 | Best Paper Nominee |

### 4.4 中国团队的整体特征

1. **产学研协同成为主流**: 阿里云、字节跳动、蚂蚁、华为、寒武纪与高校联合署名论文占据相当比例。
2. **"去中心化"趋势明显**: 上交IPADS异军突起，中科院计算所、哈工大深圳、东北大学、湖南大学、电子科技大学等新力量加入。
3. **工业界论文质量追平学术界**: 阿里云的FAST Best Paper、蚂蚁CCL-D（PPoPP提名）证明中国企业系统研究能力已达世界一流。
4. **存储方向优势突出**: FAST 2026中85.7%为中国团队。
5. **软件工程与并行编程全面崛起**: ICSE 2026多个杰出论文奖、PPoPP 2026约60%中国论文参与。

---

## 五、投稿策略建议

### 5.1 按研究方向选择会议

| 你的研究方向 | 首选会议 | 备选会议 | 理由 |
|------------|---------|---------|------|
| **存储系统 / 文件系统** | FAST | EuroSys | FAST是存储领域第一旗帜 |
| **网络系统 / RDMA / SDN** | NSDI | EuroSys | NSDI是网络系统第一选择 |
| **AI 训练/推理基础设施** | NSDI / FAST / PPoPP | EuroSys | 推理存储偏FAST、通信调度偏NSDI、并行训练偏PPoPP |
| **操作系统 / 内核 / 虚拟化** | EuroSys | ASPLOS | EuroSys是OS核心阵地 |
| **体系结构 / 硬软件协同** | ASPLOS / HPCA | EuroSys | ASPLOS/HPCA是体系结构旗舰 |
| **分布式系统 / 并发控制** | EuroSys | PPoPP | EuroSys接收分布式；PPoPP偏好并发 |
| **并行编程 / 并发数据结构 / GPU计算** | PPoPP | HPCA | PPoPP是并行编程核心阵地 |
| **软件测试 / Fuzzing / 程序分析** | ICSE | — | ICSE是软件工程旗舰 |
| **形式化验证 / 类型系统** | POPL | — | POPL是PL领域最高级别 |
| **LLM 辅助系统开发（AI for Systems）** | ICSE / FAST | NSDI | SYSSPEC在FAST获Best Paper；ICSE有大量AI+SE工作 |

### 5.2 按论文特征选择会议

| 论文特征 | 推荐会议 | 原因 |
|---------|---------|------|
| **有大规模工业部署验证** | FAST、NSDI | 工业论文获高度认可 |
| **有硬件原型 / 芯片 / FPGA** | ASPLOS、HPCA | 偏好硬件实现 |
| **有开源系统 / 高质量 Artifact** | FAST、PPoPP | 有专门Artifact奖项 |
| **理论优雅性 + 可证最优** | NSDI、POPL | 偏好理论深度 |
| **新方法论 / 新设计范式** | EuroSys、POPL | 偏好方法论/理论创新 |
| **小团队 / 单作者单位** | EuroSys、NSDI、ICSE | 独立团队仍有空间 |
| **跨领域交叉** | ASPLOS、EuroSys | 专门偏好交叉创新 |

### 5.3 时间线策略

基于2026年已举办会议的时间线，2027年投稿节奏建议：

```
2026年6月  → 准备 SOSP 2027
2026年7月  → 准备 FAST 2027（预计9月截稿）
2026年8月  → 准备 EuroSys 2027 秋轮 / ICSE 2027 第一轮
2026年9月  → 准备 NSDI 2027 Spring 轮
2026年10月 → 准备 ASPLOS 2027 夏轮
2026年11月 → 准备 HPCA 2027 / PPoPP 2027 / POPL 2027
```

---

## 六、2026年系统软件领域总体评述

### 6.1 "系统软件的黄金时代"正在到来

2026年是系统软件领域极具标志性的一年。八个CCF-A顶会在1-5月密集举办，呈现出前所未有的繁荣景象。

**1. AI革命正在重新定义系统软件的价值。** 当LLM推理的KV Cache需要TB级存储管理（Tutti）、当异构GPU集群需要近最优通信调度（HeteCCL、ForestColl）、当文件系统可被LLM自动生成（SYSSPEC）、当并行训练需要弹性容错（Elastor）——系统软件不再是被动的"基础设施"，而是主动的"使能者"。

**2. 硬件多样性开启了系统软件的设计空间。** PM、CXL内存池、SmartNIC/SmartSwitch、定制ASIC、量子计算芯片、PIM设备——每一种新硬件都创造了一类新的系统设计问题。

**3. 工业界与学术界的边界正在模糊。** 阿里云三代存储架构演进、字节跳动EB级GC实践、Azure SmartSwitch大规模部署、蚂蚁4000 GPU集群诊断——为系统研究提供了前所未有的实证基础。

**4. 跨会议交叉融合加速。** HPCA/PPoPP/POPL在悉尼联合举办。LLM推理存储（FAST+NSDI+PPoPP）、并发形式化验证（PPoPP+POPL）、AI for Systems（FAST+NSDI+ICSE）等方向在多个会议上同时开花。

### 6.2 值得关注的三大潜在变革

**变革一：从"CPU-centric"到"XPU-centric"的系统架构。** Tutti的GPU io_uring、FlashAttention-T的国产AI芯片适配、MetaAttention的跨硬件统一Attention框架——"XPU-native"的系统软件正成为新设计类别。

**变革二：LLM辅助系统软件开发从"玩具"走向"生产"。** SYSSPEC获FAST Best Paper、ICSE 2026大量AI+SE论文获奖——AI for Systems进入实用化阶段。

**变革三：安全从"附加层"变为"系统设计的一等公民"。** Pyramid（EuroSys）、SrFTL（TOS）、Miri（POPL）等从TEE编排、存储层勒索检测、Rust UB检测等维度展现"安全原生"设计。

### 6.3 对中国系统研究社区的观察

2026年是中国系统研究社区的丰收年。FAST 2026 85.7%中国论文占比、ICSE多个杰出论文奖、PPoPP约60%中国团队参与——中国已成为全球系统研究的重要一极。

值得思考的问题：研究方向集中度高（上交/清华/阿里云），工业论文占比突出提示高校独立产出需持续关注，"后发优势"明显（东北大学、麒麟软件、扬州大学等首次突破），SE和并行编程方向已达世界一流水平。

### 6.4 总结

2026年的系统软件CCF-A顶会共同描绘了一幅清晰的图景：**AI正在重塑系统软件的每个层次，硬件多样性正在创造前所未有的设计空间，工业实证正在赋予系统研究更强的说服力，学科交叉融合正在催生新的研究范式，中国正在成为全球系统软件创新的核心力量。**

对于系统软件研究者而言，这是一个充满机遇的时代。最好的论文不是"发明一个更快的算法"，而是"在理解AI工作负载、理解新硬件能力、理解大规模部署约束的前提下，重新设计一个层次栈"。八个顶会的论文一再证明：**系统软件的创新本质，从来都是跨层的重新思考。**

---

> **数据说明**: 本报告基于 EuroSys 2026、FAST 2026、NSDI 2026、ASPLOS 2026、ICSE 2026、HPCA 2026、PPoPP 2026、POPL 2026 八份洞察报告撰写。ASPLOS 2026 的详细论文数据暂未获取。ICSE 2026 数据侧重系统软件相关 Track，POPL 2026 数据侧重与系统软件直接相关的 PL 研究。所有论文数据来源于可公开获取的学术信息，具体以各会议官方论文集为准。中国团队的界定以论文第一完成单位为准。
>
> **报告撰写时间**: 2026年6月10日