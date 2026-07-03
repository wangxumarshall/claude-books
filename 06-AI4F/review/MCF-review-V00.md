# 《磁约束核聚变及商用发电研究（2024–2026）》

## 摘要
2024–2026 年，磁约束核聚变研究已从“物理可达性验证”进入“工程可交付性验证”阶段。托卡马克方向在先导电站（Fusion Pilot Plant, FPP）参数收敛、负三角形运行窗口、破裂与逃逸电子（RE）缓解方面持续推进；仿星器方向在新型磁构型优化与湍流控制方面取得关键突破。与此同时，氚自持、高热流部件寿命、破裂后果控制、全厂系统集成与经济可融资性，仍是商业发电落地的主障碍。本文基于 2024–2026 年 NF、PRL、PPCF、PoP、FED 及 FEC、SOFE、EPS、APS-DPP、TOFE 的代表性成果，系统梳理研究进展。结论是：聚变已具备进入示范电站工程化攻关的条件，但要实现可复制商业部署，必须优先打通“燃料循环闭合 + 高可用运行 + 许可合规”三条主线。

## 引言
磁约束聚变的评价重心正在改变：过去关注“单次高性能放电”，现在更关注“电站级持续可发电能力”。这意味着研究对象从等离子体本体，扩展为“等离子体—材料—包层—燃料循环—运维—监管—经济”的耦合系统。

2024–2026 年的文献显示，国际路线并未收敛为单一技术，而是形成“托卡马克近期主线 + 仿星器中长期对冲”的并行结构 [1-10]。在该结构下，真正决定商用节奏的不是某一项峰值物理指标，而是系统瓶颈的消减速度。

## 相关工作
- **NF/PoP**：聚焦破裂、RE、DEMO 包层与燃料循环可行性 [1,6,7]。
- **PRL**：在仿星器湍流与磁构型理论上给出高价值新结果 [2,3]。
- **PPCF**：围绕 MANTA 等 FPP 设计，强调功率排出与可运行性并重 [4,5]。
- **FED**：面向包层、结构与受限空间工程实现 [8]。
- **FEC/SOFE/EPS/APS-DPP/TOFE**：推动从单学科研究转向工程集成与产业部署讨论 [9-15]。

## 关键进展（2024–2026）

### 1. 仿星器可反应堆化路径增强
PRL 结果证明杂质可用于调控湍流热输运，且存在优化窗口 [2]；piecewise omnigenous 构型放宽了传统几何约束，提升工程可制造性潜力 [3]。

### 2. 托卡马克 FPP 从概念进入参数闭环
MANTA 等工作将“辐射主导功率排出、ELM-free 倾向、系统级约束”纳入统一优化框架 [4,5]；APS-DPP/EPS 展示了“系统码扫描 + 高保真校核”的共性流程 [13,14]。

### 3. 破裂与 RE 风险认知趋于现实化
PoP 与 NF 结果提示：RE 放大机制高度依赖碰撞性、杂质冷却与场景细节，通用缓解方案尚不成立 [1,6]。

### 4. 包层与氚自持成为主系统问题
NF（JA DEMO）与 FED 的结果显示，包层已不再是“中子学子课题”，而是与结构完整性、维护策略、燃料循环效率共同决定商用可行性 [7,8]。

## 挑战：问题、技术思路与路线
下面按“挑战问题 -> 技术思路 -> 可能路线（近/中期）”展开。

### 挑战 1：氚自持与燃料循环闭合不足
**问题挑战**
- D-T 路线必须实现足够 TBR 裕量；
- 包层增殖、提氚效率、系统滞留库存、再注入链路耦合强；
- 小型高场装置（尤其球形托卡马克）空间受限导致包层设计余度不足 [7,8,10]。

**技术思路**
- 将“包层中子学最优”转为“全燃料循环最优”；
- 采用数字孪生驱动的动态库存管理（而非静态 TBR 指标）；
- 提升在线提氚与过程安全监测能力。

**实施路线**
- **近端（~3年）**：建设包层-提氚-燃料回注联试平台；统一 TBR 与燃料循环评价口径。
- **中端（~5年）**：在示范级装置上完成连续运行工况的闭环验证（含异常工况）。
- **远端（并网前）**：形成可审查的安全壳边界内氚库存与排放控制标准。

### 挑战 2：高热流排出与部件寿命矛盾
**问题挑战**
- 偏滤器和第一壁承受高热流、粒子负荷和热疲劳；
- “高增益”常伴随“高局部热负荷”，影响可用率与检修周期；
- 现有方案在长脉冲/高占空比场景下证据不足 [4,5,11]。

**技术思路**
- 以“热流可管理性”作为反应堆设计第一约束；
- 采用辐射主导边界层、几何扩展偏滤器、主动控制协同；
- 运行策略与材料策略并行优化（不是二选一）。

**实施路线**
- **近端**：建立“热流-寿命-维护周期”统一指标，优先筛选可维护构型。
- **中端**：开展接近电站热负荷的长时试验与失效模式统计。
- **远端**：形成可替换模块化 PFC 体系，匹配计划停堆维护窗口。

### 挑战 3：材料辐照与结构完整性数据不足
**问题挑战**
- 第一壁/包层结构材料在中子辐照下性能退化路径复杂；
- 关键连接工艺、涂层与功能梯度材料寿命数据库不足；
- 影响安全裕度、备件策略与成本预测 [8,10,12,15]。

**技术思路**
- “材料样品数据”升级为“构件级可用寿命模型”；
- 通过多尺度模型 + 加速辐照实验建立可外推数据库；
- 工艺验证与质量控制标准同步建设。

**实施路线**
- **近端**：补齐关键材料/连接工艺数据库。
- **中端**：开展原型构件辐照后性能与失效机理联合评估。
- **远端**：形成面向采购与监管的材料标准与验收规范。

### 挑战 4：破裂与逃逸电子（RE）高后果风险
**问题挑战**
- 破裂阶段 RE 可能造成壁面局部高损伤；
- 缓解手段对不同装置参数敏感，通用经验外推失效风险高 [1,6]。

**技术思路**
- 从“事后缓解”转向“事前可避免 + 事中可终止 + 事后可容错”；
- 建立 RE 风险概率化评估（PRA）与多屏障设计；
- 将破裂风险作为许可前置指标。

**实施路线**
- **近端**：统一破裂数据库、开展跨装置基准验证。
- **中端**：部署实时预警 + 主动干预系统（注入/线圈/场景降级协同）。
- **远端**：把 RE 缓解系统纳入“安全级”功能分级与监管审查框架。

### 挑战 5：系统集成复杂度与控制可靠性
**问题挑战**
- 核心等离子体、边界层、磁体、包层、燃料循环、热工系统强耦合；
- 控制系统需在高不确定性下长期稳定运行；
- “单系统优化”可能导致全厂次优。

**技术思路**
- 采用模型分层（系统码—中保真—高保真）闭环迭代；
- 推进控制算法可验证化与故障安全设计；
- 构建“从设计到运行”的统一数字主线。

**实施路线**
- **近端**：建立统一接口标准与跨团队模型互认流程。
- **中端**：在集成试验平台验证多系统联动控制。
- **远端**：实现电站级数字孪生运维与预测性检修。

### 挑战 6：许可、标准与商业可融资性
**问题挑战**
- 聚变监管框架仍在形成中，不同地区要求差异大；
- FOAK 项目 CAPEX 与停堆损失不确定性高，融资风险偏大。

**技术思路**
- 早期嵌入许可工程（licensing-by-design）；
- 采用阶段性可交付里程碑，降低融资与技术风险；
- 推动标准化部件与供应链质量体系。

**实施路线**
- **近端**：明确安全案例边界与关键审查指标。
- **中端**：以示范项目验证“技术—监管—商业”联动机制。
- **远端**：形成可复制的 EPC 与运维商业模型。

## 展望
未来 5–10 年的成败，不在于再刷新单次物理纪录，而在于能否完成以下三项工程闭环：
1. **燃料循环闭环**（可持续氚自持）；
2. **运行闭环**（高可用、可维护、可预测停堆）；
3. **许可闭环**（可审查、可证明、可复制）。

路线判断上，托卡马克仍将主导近期示范发电节点；仿星器凭借稳态与潜在运维优势，可能在中长期形成有竞争力的商业分支。两条路线并行推进将是降低系统性技术风险的优选策略。

## 参考文献（含期刊/会议来源）
[1] Arnaud P, McDevitt C J. *The impact of collisionality on the runaway electron avalanche during a tokamak disruption*. **Physics of Plasmas (PoP)**, 2024, 31(6).  
[2] García-Regaña J M, Calvo I, Parra F I, Thienpondt H. *Reduction or Enhancement of Stellarator Turbulence by Impurities*. **Physical Review Letters (PRL)**, 2024, 133:105101. DOI: 10.1103/PhysRevLett.133.105101.  
[3] Velasco J L, Calvo I, Escoto F J, et al. *Piecewise omnigenous stellarators*. **Physical Review Letters (PRL)**, 2024, 133:185101. DOI: 10.1103/PhysRevLett.133.185101.  
[4] The MANTA Collaboration. *MANTA: A Negative-Triangularity NASEM-compliant fusion pilot plant*. **Plasma Physics and Controlled Fusion (PPCF)**, 2024, 66:105006.  
[5] Miller M A, Arnold D, Wigram M, et al. *Power handling in a highly-radiative negative triangularity pilot plant*. **Plasma Physics and Controlled Fusion (PPCF)**, 2024, 66:125004.  
[6] Fil A, et al. *Disruption runaway electron generation and mitigation in the Spherical Tokamak for Energy Production (STEP)*. **Nuclear Fusion (NF)**, 2024, 64:106049. DOI: 10.1088/1741-4326/ad73e9.  
[7] Someya Y, et al. *Development of water-cooled cylindrical blanket in JA DEMO*. **Nuclear Fusion (NF)**, 2024, 64:046025. DOI: 10.1088/1741-4326/ad2950.  
[8] Anderton M D, et al. *Novel high temperature tritium blanket designs for confined spaces in spherical tokamak fusion reactors*. **Fusion Engineering and Design (FED)**, 2025, 210:114732.  
[9] Lopez N. *Tokamak Energy’s high temperature superconducting magnet spherical tokamak fusion pilot plant concept*. **IAEA Fusion Energy Conference (FEC 2025)**, 2025.  
[10] American Nuclear Society. *26th Topical Meeting on the Technology of Fusion Energy (TOFE 2024)*. **TOFE**, 2024.  
[11] Salazar E, Sorbom B, Adams J, et al. *Overview of magnet testing and development for SPARC*. **IEEE Symposium on Fusion Engineering (SOFE 2025)**, 2025.  
[12] Serikov A (ed.). *Special Issue Featuring Papers from TOFE 2024*. **Fusion Science and Technology (TOFE Special Issue)**, 2026, 82(1–2): vii–viii.  
[13] Brown T G, Menard J E, et al. *Physics design of a Spherical Tokamak Advanced Reactor (STAR)*. **APS Division of Plasma Physics (APS-DPP 2024)**, Abstract JP12.00083, 2024.  
[14] Tholerus E. *Integrated scenario design for the STEP prototype power plant*. **EPS Conference on Plasma Physics (EPS 2024)**, Contribution P4.078, 2024.  
[15] SOFE 2025 Organizing Committee. *Technical program: blankets, magnets, power plants and commercialization*. **IEEE SOFE**, 2025.  
