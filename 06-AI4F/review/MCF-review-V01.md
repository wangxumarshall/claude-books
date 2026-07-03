# 磁约束核聚变及商用发电研究

**——基于 2024–2025 年顶会顶刊证据链的综合评述**

---

**摘要：** 磁约束核聚变（magnetic confinement fusion, MCF）在 2024–2025 年呈现由“高性能等离子体验证”向“商用发电系统集成设计”加速过渡的显著特征。本文以 Nuclear Fusion（NF）、Physical Review Letters（PRL）、Plasma Physics and Controlled Fusion（PPCF）、Physics of Plasmas（PoP）、Fusion Engineering and Design（FED）、IAEA Fusion Energy Conference（FEC）、IEEE Symposium on Fusion Engineering（SOFE）、EPS Conference on Plasma Physics（EPS）、APS Division of Plasma Physics（APS-DPP）及 Topical Meeting on the Technology of Fusion Energy（TOFE）为主要文献来源，采用“同行评议优先、会议官方文献补充、非可核验来源剔除”的证据分级策略，系统梳理约束与输运、偏滤器排热、氚燃料循环、FPP/DEMO 系统集成及工程放大等方面的最新进展。研究表明：先进偏滤器辐射排热机制、第一性原理输运预测框架与高场紧凑 FPP 架构设计，显著提升了从物理可行到工程可部署的连通性；但氚自持闭环、高热流部件寿命、全厂可用率与成本—监管—供应链协同仍是商业化核心瓶颈。本文提出面向示范电站阶段的优先攻关路径：以排热—燃料循环—可维护性为联立约束，建立可审计的跨学科指标体系和统一数据披露规范。

**关键词：** 磁约束核聚变；商用发电；聚变示范电站；偏滤器排热；氚自持；系统集成

---

## 1 引言

实现安全、清洁、可规模化的聚变能发电，是应对全球能源转型与气候治理的长期战略选项之一。在各类聚变路线中，磁约束方案（托卡马克、仿星器、磁镜等）因具备相对成熟的装置基础、持续的国际协作网络以及向 DEMO/FPP 演进的明确技术路线图，仍是当前最接近“电站化验证”的主路径。

过去数十年，磁约束聚变研究长期以三乘积（\(n_i T_i \tau_E\)）、聚变增益 \(Q\)、能量约束因子 \(H\) 等等离子体物理指标为核心评价标准。然而，近两年国际主流期刊与顶级会议的研究叙事发生结构性转变：评价重心由“能否在实验室实现燃烧等离子体相关条件”扩展为“能否在可接受的成本、风险与监管框架下实现长期并网发电”[1–10]。这一转变在以下三方面尤为突出：

1. **物理层**：边界与偏滤器排热、湍流输运外推、集成运行场景成为与核心约束同等重要的议题；
2. **工程层**：包层与氚循环、材料与远程维护、磁体与系统可靠性被纳入设计闭环；
3. **经济层**：资本开支（CAPEX）、净电输出、可用率与燃料闭环安全裕度开始与物理参数并列优化[1,5,7]。

本文聚焦 2024–2025 年文献，回答三个问题：（1）哪些进展对商用发电可行性具有实质贡献；（2）哪些结论仍属前沿假设、尚需工程验证；（3）下一阶段研发与产业资源应如何排序。全文坚持“去粗存精、去伪存真”：优先采用可核验 DOI 的同行评议论文；会议层面采用官方摘要、预印本或特刊论文；不将媒体转述或未标注来源的材料作为论证主证据。

---

## 2 研究方法与文献纳入标准

### 2.1 时间与来源范围

- **时间窗口**：2024 年 1 月至 2025 年 12 月（部分 TOFE 2024 论文于 2026 年特刊正式出版，仍纳入“近两年研究脉络”）。
- **必含来源**：NF、PRL、PPCF、PoP、FED、IAEA-FEC、IEEE-SOFE、EPS、APS-DPP、TOFE，每个来源至少 1 篇代表性文献。
- **研究边界**：以磁约束路线为主；惯性约束成果仅作背景对照，不作为本文主证据链。

### 2.2 证据分级

| 级别 | 类型 | 用途 |
|------|------|------|
| A | 同行评议期刊正式论文 | 论证核心科学结论 |
| B | 会议官方预印本/特刊论文 | 补充前沿方向与集成设计 |
| C | 会议官方摘要集 | 描述议题结构与产业趋势 |

### 2.3 关键指标口径

本文涉及指标包括：聚变增益 \(Q\)、聚变功率 \(P_{\mathrm{fus}}\)、净电功率 \(P_{\mathrm{net}}\)、氚增殖比 TBR、偏滤器峰值热流 \(q_{\parallel,\mathrm{peak}}\)、能量约束时间 \(\tau_E\)、容量因子（可用率）。跨文献比较时需注意各研究团队对“净电”“目标增益”定义的差异，避免简单数值对标。

---

## 3 相关工作

### 3.1 约束、输运与燃烧等离子体集成场景

NF 在 2024–2025 年持续发表 ITER/JET 燃烧等离子体集成运行、同位素效应外推及新型磁约束构型（如磁镜 Novatron）相关研究[1,11,12]。其中，面向托卡马克燃烧等离子体运行路径的专题工作系统讨论了从非燃烧到燃烧工况的集成场景开发，为 ITER 及后续 DEMO 运行提供了情景库基础[11]。

PoP 2025 年发表的多项工作表明，基于 GENE/GENE-3D 与 KNOSOS、Tango 耦合的第一性原理框架，已能在 W7-X 等装置尺度上再现稳态剖面及湍流趋势，为仿星器与混合构型的反应堆性能预测提供了比纯经验标度更可信的工具链[4,13]。

### 3.2 偏滤器、排热与边界物理

PRL 2025 年报道的 X 点目标辐射器（XPTR）工况，通过次级 X 点几何与强辐射区组织，显著改善偏滤器去附着可达性并降低辐射前沿位置敏感性，为反应堆级功率排散提供了新的物理机制[2]。

PPCF 2024 年关于高辐射负三角 FPP（MANTA）排热的研究表明，在合理杂质（如 Ne）份额下，可将靶板峰值热流控制在可接受范围，并讨论 FLiBe 等介质在靶板冷却中的复用潜力[3]。

### 3.3 反应堆系统工程与商用化设计

FED 2025 年发表的 STAR（Spherical Tokamak Advanced Reactor）概念强调“物理—工程—成本”联合优化，而非孤立追求峰值 \(Q\)[5]。NF 2025 年关于 FPP 贝叶斯网络元模型的研究，将不确定性显式纳入设计决策，可在资本成本、产热/产电与工程约束之间进行双向推理[1]。

SOFE、TOFE 的技术议程显示，氚提取、燃料循环、材料辐照、系统建模与公私合作机制已成为与等离子体物理并列的核心议题[7,10,14]。

### 3.4 国际会议与路线协同

- **IAEA FEC 2025**：聚焦磁约束、惯性约束及创新概念，强调从 R&D 向示范与部署准备过渡[6]；
- **EPS 2024/2025**：“Visions for Fusion” 圆桌及 PPCF 特刊反映学界对部署路径、燃料循环与监管协同的关注[8]；
- **APS-DPP 2024**：邀请报告与海报大量涉及 FPP 运行点、ELM 抑制、负三角构型及数据驱动控制[9]。

---

## 4 关键进展

### 4.1 偏滤器排热：从经验调参走向机制化设计

托卡马克商用化的“硬约束”之一是偏滤器热负荷。ITER 类装置在满功率工况下面临的平行热流密度可达数十 MW·m⁻² 量级，需通过几何扩展（如 Super-X）、杂质辐射与去附着协同实现目标壁负荷[2,3,15]。

Bernert 等（PRL, 2025）在瑞士 TCV 等装置上验证的 XPTR 工况表明：将强辐射区锚定在远离主等离子体的次级 X 点附近，可在保持芯部性能的同时，显著拓宽可运行空间[2]。该结果的意义在于——排热优化不再仅依赖“增加杂质、增加辐射”的单变量策略，而是进入“磁几何—辐射区—靶板热负荷”协同设计阶段。

Miller 等（PPCF, 2024）在 MANTA 负三角 FPP 概念中给出定量边界：在 \(P_{\mathrm{SOL}} \approx 25\) MW 工况下，约 0.1% 的 Ne 杂质即可将靶板热流降至安全阈值以下，峰值约 7.8 MW·m⁻² 时靶板温度可控制在约 1550 °C 以内[3]。尽管该结果基于模拟与概念设计，但为“紧凑高功率堆型是否具备排热可行性”提供了可计算证据。

### 4.2 输运预测：第一性原理框架的可验证性增强

传统反应堆设计大量依赖 \( \tau_E \propto I_{\mathrm{p}}^{\alpha} B_{\mathrm{t}}^{\beta} P_{\mathrm{loss}}^{-\gamma} \) 等经验标度律。其局限在于：当装置尺度、磁场、同位素质量或磁场构型显著变化时，外推误差可能系统性放大。

Bañón Navarro 等（PoP, 2025, 32, 073904）对 GENE-KNOSOS-Tango 框架的验证显示：在 W7-X OP1.2b 的四个工况中，该耦合框架可较好再现密度、温度剖面及湍流热扩散率趋势，并揭示电子尺度湍流与新经典径向电场剪切等关键效应[4]。这标志着“以边界条件为输入、预测芯部性能”的仿星器设计路径正在从方法学走向可检验工程工具。

需要审慎的是：第一性原理框架的计算成本、边界条件不确定性和多物理耦合（如快离子、辐射损失）仍限制其在大规模参数扫描中的实时应用。因此，近期合理的技术路线是“系统码 + 高保真局部校核”的分层架构，而非完全替代经验设计流程[1,5,6]。

### 4.3 FPP/DEMO 设计：物理目标与电站指标联立优化

商用发电要求设计团队同时满足：

- **物理目标**：足够高的 \(P_{\mathrm{fus}}\) 与 \(Q\)，可控的 MHD 与快粒子稳定性；
- **工程目标**：TBR ≥ 1.05（考虑闭环损失）、可维护部件、合理的中子辐照剂量；
- **经济目标**：可接受的 CAPEX、容量因子与度电成本（LCOE）区间[1,5,7]。

Griffiths 等（NF, 2025）针对 Tokamak Energy FPP 的贝叶斯网络元模型研究表明：在 DOE 里程碑计划约束下，可在“最小资本开支”与“最大产热/产电”之间识别可行参数域，并支持反向推理——即由经济约束反推允许的等离子体与工程参数窗口[1]。

Jain 等（FED, 2025）提出的 STAR 概念进一步强调架构级设计：在球形托卡马克路线中，通过 HTS 磁体、紧凑几何与系统级成本约束的协同，探索“中间示范堆—商业堆”的过渡路径[5]。

### 4.4 燃料循环与氚工程：从“能否增殖”到“能否闭环”

D-T 聚变商用堆必须实现氚自持。名义 TBR > 1 仅是必要条件；充分条件还包括：提氚效率、系统滞留、库存安全、启停堆瞬态行为及监管许可[10,14]。

TOFE 2024 的“Tritium Extraction”专题集中讨论了 PbLi 渗透提氚、FLiBe 渗透反对真空（PAV）、MELCOR-TMAP 系统建模等路径[10]。这些研究共同指向一个工程共识：**燃料循环不是包层附属模块，而是决定电站可用率与许可边界的主系统**。

### 4.5 会议生态：产业化和部署导向显著增强

SOFE 2025 摘要集与 ITER 相关报道显示，全球聚变投资与私营公司数量持续增长，会议议题中“商业化、供应链、公私合作”占比上升[7]。EPS 2024 的 “Visions for Fusion” 及后续 PPCF 述评指出，学界正在将“科学突破之后的系统集成与监管路径”纳入主流讨论[8]。

APS-DPP 2024 邀请报告（如 DIII-D/KSTAR 的 ELM 抑制与机器学习控制）表明，高性能工况维持越来越依赖实时优化与跨装置验证的控制策略[9]。这对 FPP 意味着：控制系统复杂度与认证成本将构成不亚于物理极限的工程挑战。

---

## 5 挑战与风险分析

### 5.1 氚自持与燃料循环闭环

主要风险包括：

1. **提氚与滞留**：固态增殖剂、液态金属和熔盐路线在提氚动力学、腐蚀与材料相容性方面差异显著；
2. **库存与许可**：场内氚库存上限、事故源项评估和监管要求可能压缩设计裕度；
3. **动态工况**：启停、扰动与维护期间的燃料循环稳定性尚未形成充分运行统计[10]。

### 5.2 高热流部件寿命与可用率

先进排热方案改善了稳态与瞬态热负荷窗口，但钨靶板溅射、再沉积、裂纹与辐照脆化等问题仍需辐照装置（如 IFMIF/DONES 类设施）与 DEMO 运行数据验证[2,3,7]。

可用率（容量因子）是 LCOE 的敏感参数。若年停机维护时间超预期，即使 \(Q\) 较高，商业回报仍可能不达标[5,7]。

### 5.3 控制、运行场景与数字孪生可信度

FPP 运行场景涉及启动、电流爬升、燃烧维持、排热调节与异常缓解的多阶段耦合。机器学习控制虽可提升性能，但其可解释性、失效模式覆盖与安全认证路径仍需建立行业规范[6,9]。

### 5.4 经济可行性与供应链

当前多数 FPP 处于预概念/概念设计阶段，成本模型对 HTS 磁体良率、包层制造周期、土建与融资成本高度敏感[1,5]。此外，关键材料（如低活化钢、钨、锂陶瓷）的工业供给能力尚未形成聚变专用供应链[7,10]。

### 5.5 证据链风险：会议前沿与工程现实之间的“梯度差”

部分前沿结论首先出现在会议摘要或预印本，尚未完成跨装置复现或同行评议。对此应坚持：

- **A 级证据**用于核心判断；
- **B/C 级证据**用于趋势判断；
- 对“时间表”“成本区间”等前瞻性表述保持区间估计，避免单点承诺[6–10]。

---

## 6 展望与建议

### 6.1 短期（3–5 年）：打通“排热—氚循环—维护”联立验证链

建议设立跨机构联合平台，统一以下工况库：

- 满功率/长脉冲排热工况（含杂质播种与去附着边界）；
- 氚闭环动态工况（启停、扰动、维护）；
- 远程维护与部件更换节拍验证。

并将台架试验结果反馈至系统码与 FPP 数字样机，形成“实验—模拟—设计”闭环[1,2,5,10]。

### 6.2 中期（5–10 年）：以电站指标验收示范机

示范机验收建议从“最高 \(Q\)”转向“可审计电站指标”：

| 指标类别 | 建议核心量 |
|----------|------------|
| 能量 | \(P_{\mathrm{fus}}\)、\(P_{\mathrm{net}}\)、\(Q_{\mathrm{plant}}\) |
| 燃料 | TBR、闭环时间常数、场内氚库存 |
| 可靠性 | 容量因子、MTBF、计划外停机 |
| 经济 | CAPEX 区间、LCOE 敏感性 |

### 6.3 长期：建立全球可比的数据披露与认证框架

建议推动：

1. 统一 \(Q\)、净电、TBR、热流、可用率定义；
2. 公开关键设计假设与不确定性区间；
3. 形成“物理认证—工程认证—监管认证”分层体系，降低重复试错成本[8,10]。

---

## 7 结论

2024–2025 年的磁约束核聚变研究正在完成从“物理突破叙事”向“商用发电系统叙事”的转型。偏滤器排热机制创新、第一性原理输运预测、FPP 贝叶斯/系统优化设计以及燃料循环工程化，是最具实质意义的进展方向[1–5,10]。同时，氚闭环、部件寿命、可用率、控制认证与供应链成熟度仍是决定商业化节奏的关键约束[7,9,10]。

可以判断：磁约束聚变已具备迈向示范电站的技术趋势，但“商用发电”的成功不取决于单一物理里程碑，而取决于多约束耦合下的系统收敛速度。未来领先路线将是能够同时在物理性能、工程可靠性与经济可竞争性上提供可验证证据链的路线。

---

## 参考文献

[1] Griffiths T, et al. Decision support for engineering and design in a fusion pilot-plant concept using Bayesian networks as meta-models. **Nuclear Fusion**, 2025, 65(6): 066019. DOI: 10.1088/1741-4326/add549. **（期刊：Nuclear Fusion）**

[2] Bernert M, et al. X-Point Target Radiator Regime in Tokamak Divertor Plasmas. **Physical Review Letters**, 2025, 134(18): 185102. DOI: 10.1103/PhysRevLett.134.185102. **（期刊：Physical Review Letters）**

[3] Miller M A, et al. Power handling in a highly-radiative negative triangularity pilot plant. **Plasma Physics and Controlled Fusion**, 2024, 66(12): 125004. DOI: 10.1088/1361-6587/ad867a. **（期刊：Plasma Physics and Controlled Fusion）**

[4] Bañón Navarro A, et al. Validation of a comprehensive first-principles-based framework for predicting the performance of future stellarators. **Physics of Plasmas**, 2025, 32(7): 073904. DOI: 10.1063/5.0267879. **（期刊：Physics of Plasmas）**

[5] Jain P, et al. The spherical tokamak advanced reactor (STAR) fusion power plant design. **Fusion Engineering and Design**, 2025, 222. **（期刊：Fusion Engineering and Design）**

[6] Bannmann S, et al. Attaining tokamak level performance through plasma density profile shaping at Wendelstein 7-X. In: **30th IAEA Fusion Energy Conference (FEC 2025)**, Chengdu, China, 2025 (conference manuscript/preprint). **（会议：IAEA Fusion Energy Conference）**

[7] Wallace G M (ed.). Book of Abstracts, **31st IEEE Symposium on Fusion Engineering (SOFE 2025)**, MIT, Cambridge, MA, USA, June 23–26, 2025. **（会议：IEEE Symposium on Fusion Engineering）**

[8] Dinklage A, et al. Visions for fusion. **Plasma Physics and Controlled Fusion**, 2025, 67(6): 063701. DOI: 10.1088/1361-6587/add621. (Special Issue from the **50th EPS Conference on Plasma Physics**, Salamanca, Spain, July 8–12, 2024). **（会议关联：EPS Conference on Plasma Physics）**

[9] Kim S. Achieving ELM-suppressed operation with the highest performance in DIII-D and KSTAR via adaptive and machine learning controls. Invited Talk, **66th APS Division of Plasma Physics Annual Meeting (APS-DPP 2024)**, Atlanta, GA, USA, Abstract TI02.00003, October 10, 2024. **（会议：APS Division of Plasma Physics）**

[10] American Nuclear Society. Tritium Extraction (Technical Session), **26th Topical Meeting on the Technology of Fusion Energy (TOFE 2024)**, Madison, WI, USA, July 24, 2024. Related special issue: **Fusion Science and Technology**, 2026, 82(1–2). **（会议：Topical Meeting on the Technology of Fusion Energy）**

[11] Na Y-S, et al. Integrated operation scenarios: Chapter 6 of the special issue on the path to tokamak burning plasma operation. **Nuclear Fusion**, 2025, 65(9): 093001. DOI: 10.1088/1741-4326/ade79f. **（期刊：Nuclear Fusion）**

[12] Qi L, et al. Reversal of the isotopic dependence of energy confinement in system size scans. **Nuclear Fusion**, 2025, 65(9): 096031. DOI: 10.1088/1741-4326/adfaf3. **（期刊：Nuclear Fusion，补充）**

[13] Wilms F, et al. Global gyrokinetic simulations of kinetic-ballooning-mode turbulence in Wendelstein 7-X. **Physics of Plasmas**, 2025, 32(7): 072505. DOI: 10.1063/5.0261004. **（期刊：Physics of Plasmas，补充）**

[14] Chapman R. Developing integrated cost models for fusion power plants. *Journal of Fusion Energy*, 2025, 44: 43. DOI: 10.1007/s10894-025-00515-1. **（补充：成本建模，非指定会刊）**

[15] Pitts R A, et al. The operational space for divertor power exhaust in DEMO with a super-X divertor. **Nuclear Fusion**, 2020, 60(6): 066054. DOI: 10.1088/1741-4326/abf9df. **（期刊：Nuclear Fusion，背景参考）**

---

**作者说明：** 本文为基于公开文献的综述性研究稿，指标与时间表引用均来自对应期刊/会议原文或官方摘要；若用于正式投稿，建议根据目标期刊格式（GB/T 7714、IEEE 或 APA）重排参考文献，并补充图表（技术路线图、证据分级表、FPP 指标对照表）。

**字数：** 约 7200 字（中文正文，不含参考文献格式化重复项）。
