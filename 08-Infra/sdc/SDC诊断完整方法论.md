# SDC诊断方法论：ARM64鲲鹏处理器（操作版）

> **基于论文**：[ASPLOS 2025] HWSentinel / [HPCA 2026] PinDrop / [SOSP 2023] Alibaba / [IEEE TC 2021] Bodmann / [ASPLOS 2026] SEVI / [MICRO 2024] DelayAVF / [SOSP 2025] Orthrus / [ISCA 2024] Harpocrates / [HPCA 2025] Veritas / [HPCA 2024] Gem5-MARVEL / [arXiv 2026] ITHICA
> **目标架构**：ARM64 (AArch64) — 鲲鹏 (Kunpeng) 920/930 系列处理器
> **用途**：直接指导AI Agent进行ARM64鲲鹏平台SDC诊断

---

## 第一章：SDC定义与诊断范畴

### 1.1 SDC本质定义

**Silent Data Corruption (SDC)** 是指处理器硬件层在没有任何即时错误信号的情况下，产生错误的计算结果，该错误结果被上层软件正常使用并在系统中传播，最终导致数据丢失、一致性破坏或服务异常。

核心特征"三无"：
- **无错误信号**：CPU不产生SError、SEA、ECC等硬件级错误报告
- **无日志记录**：SEL / RAS Error Records中无对应硬件故障条目
- **无即时崩溃**：应用不会立即crash，而是静默产生错误结果

**关键发现**：SDC发生率由微架构决定，而非ISA。ARM64的条件标志（NZCV）和更大的寄存器文件是独有的脆弱点。来源：[IEEE 2023] Cross-ISA SDC

### 1.2 与其他故障类型的区别

| 故障类型 | 错误信号 | 应用表现 | ARM64典型例子 |
|---------|---------|---------|-------------|
| **SDC（静默数据损坏）** | 无 | 错误结果静默传播 | 1+1=3, NEON向量计算单元素bit-flip |
| **响亮硬件故障（Loud Fault）** | 有（SError/RAS/ECC） | 崩溃/重启/宕机 | SError + 有效RAS Error Record |
| **软件Bug** | 取决于实现 | 可复现崩溃/异常 | 空指针解引用（Data Abort from null pointer） |
| **软错误/瞬态故障** | 通常无 | 单次bit-flip | 宇宙射线导致NZCV标志翻转 |
| **永久故障/老化** | 可能延迟出现 | 随时间恶化 | 晶体管BTI/HCI导致时序违例 |

**SDC静默性判定原则**（来源：[ASPLOS 2025]）：仅当RAS Error Records / SError条目中不存在指示CPU硬件故障的记录时，服务器才被视为SDC检测候选。

### 1.3 真实发生率

**关键结论**：真实SDC发生率比传统软错误模型高3个数量级。

### 1.4 SDC的根因来源

SDC根因涵盖以下六类：

1. **硅设计缺陷（Design Escapes）**：芯片设计阶段未被验证覆盖的边际情况
2. **制造缺陷（Manufacturing Defects）**：量产过程中未被ATE检测的缺陷
3. **环境条件（Environmental）**：温度、电压、频率波动导致的计算错误
4. **老化过程（Aging/Wear-out）**：NBTI、HCI、TDDB等效应随使用时间积累。ARM低功耗设计频繁DVFS切换会加速老化
5. **数据依赖性（Data Randomization）**：特定比特模式触发错误（如NEON VFM指令仅在特定向量元素上出错）
6. **电学变异（Electrical Variations）**：不同V/f操作点的计算正确性差异

### 1.5 ARM64架构SDC脆弱性排序

| 优先级 | 结构 | 原理 | 来源 |
|--------|------|------|------|
| **最高** | NEON/SVE向量寄存器 | 向量宽度128-2048 bits，攻击面更大 | [ASPLOS 2026] SEVI |
| **最高** | FP/向量功能单元 | VFM/VFMA指令故障率最高 | [HPCA 2026] PinDrop, [ASPLOS 2026] SEVI |
| **高** | 条件标志 (NZCV) | ARM64独有脆弱点，条件标志bit-flip导致控制流静默偏离 | [IEEE 2023] Differential FI |
| **高** | L1指令缓存 | 损坏时几乎总是导致崩溃 | [IEEE 2023] CHAOS |
| **高** | 物理寄存器文件 | ARM RISC风格拥有大量寄存器，攻击面广 | [IEEE 2023] Cross-ISA |
| **中** | Load/Store队列 | ARM load-store架构导致更多数据移动 | [IEEE 2023] Differential FI |
| **中** | ALU时序路径 | 高翻转率单元中延迟故障更可能 | [MICRO 2024] DelayAVF |
| **中** | 分支预测器 | 控制流异常 | [IEEE 2023] 微架构透视 |

### 1.6 诊断输入与输出

**输入模式1：日志包（tar/zip）**
- 包含：kernel日志、dmesg、SEL/RAS Error Records、应用日志、crash dump
- AI Agent通过解压和自动识别日志类型进行离线分析

**输入模式2：机器IP + SSH/iBMC凭证**
- AI Agent通过远程命令实时采集数据
- SSH命令序列采集：CPU信息、温度、RAS、PMU、kernel日志、核心浓度数据、向量检测结果
- iBMC命令序列采集：SEL/RAS、温度、电压

**输出：结构化诊断报告**
- 判定结论（SDC/排除/观察）
- SDC概率（0-100%）
- 置信区间（如80%±10%）
- 命中规则列表（P规则命中、N规则检查结果）
- 处置建议（隔离/观察/排除）

---

## 第二章：数据源与采集协议

### 2.1 六大数据源

| 数据源 | 关键字段 | 采集命令 |
|--------|---------|---------|
| **结构化Kernel异常日志** | 异常类型、EC代码、CPU core ID、EL层级、时间戳、backtrace、应用名称、ESR_ELx值 | `dmesg`、`/var/log/messages`、`journalctl -k` |
| **重启数据库** | 重启时间戳、重启类型（计划/非计划）、crash dump、PSCI/SMC reset cause | `last reboot`、`/var/log/kdump`、`journalctl --list-boots` |
| **SEL/RAS Error Records** | ERR\<n\>STATUS、ERR\<n\>ADDR、ERR\<n\>MISC、CE/UE计数、SError记录、PCIe AER、温度/电压事件 | `ipmitool sel list`、`/sys/devices/system/edac/mc/mc*/ce_count`、`dmesg \| grep -iE "ras\|serror\|sea"` |
| **SDC测试结果数据库** | 测试时间戳、测试类型（Fleetscanner/Ripple/PinDrop）、测试结果、失败用例ID、CPU核心ID、向量指令测试结果、VL | PinDrop/Fleetscanner/Ripple测试框架 |
| **维修数据库** | 维修时间戳、维修类型、诊断结果（正确诊断/误诊/未诊）、替换组件、修复后复发 | 数据中心维修工单系统 |
| **核心浓度元数据** | 每核心异常数量及比例、兄弟核聚合、cluster分布、唯一应用数量、backtrace签名频率 | 从结构化kernel异常日志聚合计算 |

**SEL/RAS判定逻辑**（本方法论中唯一的RAS决策逻辑版本）：
- SEL中有SError/SEA且附带有效RAS Error Record → **排除**（响亮故障）
- SEL中有ECC多比特错误 → **排除**（内存故障，非CPU SDC）
- SEL中无任何硬件故障条目但应用在特定核心上崩溃 → **SDC候选**
- SError但无有效RAS Error Record → **SDC候选**（硬件自身不知何故出错）

### 2.2 日志包分析协议

**2.2.1 tar/zip解压流程**
```
1. 解压日志包到临时目录
2. 扫描所有文件，按文件名和内容模式识别日志类型
3. 按日志类型应用对应的字段提取规则
4. 聚合提取结果到统一数据结构
```

**2.2.2 日志类型自动识别规则**

| 文件名模式 | 内容模式 | 日志类型 |
|-----------|---------|---------|
| `dmesg*`、`messages*`、`syslog*` | 包含kernel时间戳 | Kernel日志 |
| `sel*`、`ipmi*` | 包含IPMI SEL条目 | SEL/RAS |
| `crash*`、`vmcore*`、`dmesg.*.log` | 包含crash dump信息 | Crash dump |
| `app*.log`、`*.out` | 应用级日志 | 应用日志 |
| `thermal*`、`temp*` | 包含温度数据 | 温度日志 |

**2.2.3 字段提取规则**

**Kernel异常日志提取字段**：
- 异常类型：Data Abort / Undefined Instruction / SError / SEA / PC alignment fault / SP alignment fault / Permission Fault / BRK/BKPT
- EC代码：0x00 (Undefined), 0x20/0x21 (Permission), 0x24/0x25 (Data Abort), 0x26 (Alignment), 0x2F (SError), 0x3C (BRK)
- CPU core ID、EL层级（EL0/EL1/EL2/EL3）、时间戳、backtrace、应用名称
- ESR_ELx (Exception Syndrome Register) 值

**RAS Error Record提取字段**：
- ERR\<n\>STATUS：错误类型（CE/DE/UE）、严重程度、syndrome
- ERR\<n\>ADDR：故障地址
- ERR\<n\>MISC：L1/L2 cache way、寄存器索引
- CE/UE计数、SError记录

**核心浓度计算方法**：
```
1. 遍历所有kernel异常日志条目
2. 按CPU core ID分组统计异常数量
3. 兄弟核（SMT）聚合：将同一物理核的逻辑核异常数合并
4. 计算每核心异常占比 = 单核异常数 / 服务器总异常数
5. 按cluster分组（异构架构）：big cluster和little cluster分别统计
6. 统计每核心上失败的唯一应用数量
```

### 2.3 机器IP诊断协议

**2.3.1 SSH命令序列**

```bash
# 1. CPU信息
lscpu | grep -E "Model name|Architecture|CPU\(s\)|Thread|Core|Socket"
cat /proc/cpuinfo | grep -E "CPU part|CPU implementer|Features"

# 2. 温度
cat /sys/class/thermal/thermal_zone*/temp
cat /sys/class/thermal/thermal_zone*/type

# 3. RAS错误
cat /sys/devices/system/edac/mc/mc*/ce_count
cat /sys/devices/system/edac/mc/mc*/ue_count
grep -i "serror\|SError" /proc/interrupts
dmesg | grep -iE "arm64|ras|error|serror|sea|data.abort"

# 4. PMU事件基线
perf stat -e armv8_pmuv3_0/sve_inst_retired/,\
armv8_pmuv3_0/br_mis_pred/,\
armv8_pmuv3_0/l1d_cache_refill/,\
armv8_pmuv3_0/cpu_cycles/ -- sleep 10

# 5. Kernel日志
journalctl -k --since "30 days ago" | grep -iE "serror|sea|data.abort|undefined|permission|alignment|brk"
dmesg -T | tail -500

# 6. 核心浓度数据（从kernel日志聚合）
journalctl -k | grep -iE "data.abort|undefined|serror|permission|alignment|brk" | \
  awk '{print $0}' | grep -oP "CPU: \K[0-9]+"

# 7. 向量检测（跨核对比）
for core in 0 1 2 3; do
  taskset -c $core ./neon_stress_test > /tmp/neon_out_$core &
done
wait
diff /tmp/neon_out_0 /tmp/neon_out_1
```

**2.3.2 iBMC命令序列**

```bash
# SEL/RAS
ipmitool -H <iBMC_IP> -U <user> -P <pass> sel list
ipmitool -H <iBMC_IP> -U <user> -P <pass> sel elist

# 温度/电压
ipmitool -H <iBMC_IP> -U <user> -P <pass> sdr type temperature
ipmitool -H <iBMC_IP> -U <user> -P <pass> sdr type voltage

# Redfish API（替代方案）
curl -s -u <user>:<pass> https://<iBMC_IP>/redfish/v1/Systems/system/LogServices/SEL/Entries
curl -s -u <user>:<pass> https://<iBMC_IP>/redfish/v1/Chassis/1/Thermal
```

**2.3.3 数据采集完成后的自动分析流程**
```
1. 解析SSH采集的kernel日志，提取异常类型和EC代码
2. 解析iBMC采集的SEL，提取RAS Error Records
3. 按核心浓度计算方法聚合异常分布
4. 应用RAS判定逻辑判断静默性
5. 执行七步诊断工作流（见第三章）
6. 生成结构化诊断报告（见第七章）
```

---

## 第三章：AI Agent诊断工作流

### 3.1 工作流总览

```
┌─────────────────────────────────────────────────────────┐
│  阶段1: 输入接收                                          │
│  ├─ 模式1: 日志包解压 → 自动识别日志类型                    │
│  └─ 模式2: SSH/iBMC远程采集 → 统一数据结构                  │
├─────────────────────────────────────────────────────────┤
│  阶段2: 数据预处理                                        │
│  ├─ Kernel异常日志结构化（EC代码/core ID/backtrace）        │
│  ├─ RAS Error Records提取（ERR_STATUS/ERR_ADDR/CE/UE）     │
│  ├─ 核心浓度计算（兄弟核聚合/cluster分布）                   │
│  └─ 重启历史/维修历史/测试结果提取                           │
├─────────────────────────────────────────────────────────┤
│  阶段3: 规则分析                                          │
│  ├─ 负向规则N1-N13检查（命中任一即排除）                     │
│  ├─ 正向规则P1-P14匹配                                    │
│  └─ 向量指令SDC专项检测 + PMU偏差检测                       │
├─────────────────────────────────────────────────────────┤
│  阶段4: 量化评分                                          │
│  ├─ P_score = Σ(命中的P规则分值)                           │
│  ├─ N_score = Σ(命中的N规则分值)                           │
│  ├─ 净分 = P_score + N_score                              │
│  └─ SDC概率 = f(净分)                                     │
├─────────────────────────────────────────────────────────┤
│  阶段5: 报告生成                                          │
│  ├─ Markdown格式诊断报告（人读）                           │
│  └─ JSON格式诊断报告（机读）                               │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Step 1: 候选筛选

**操作**：按异常总数对所有服务器降序排序，选取Top-N进入后续流程。

**ARM64注意**：鲲鹏920同构64核设计，核心浓度分析相对简单；DynamIQ异构集群需按cluster分别Top-N排序。

### 3.3 Step 2: 重启异常检测

| 参数 | 通用服务器 | AI服务器 |
|------|-----------|---------|
| 回溯窗口 | 30天 | 30天 |
| 重启阈值 | ≥6次 | ≥3次 |

- 超过阈值 → 进入下一步
- 低于阈值 → 可能健康，标记观察

**ARM64注意**：鲲鹏使用UEFI + ACPI启动，重启原因通过PSCI接口查询。异常重启伴随的SError可能进入EL3固件处理流程。

### 3.4 Step 3: RAS静默性验证

**决策树**（唯一的RAS决策逻辑版本）：

```
IF RAS Error Records中有CPU相关条目:
    IF SError + 有效ERR<n>STATUS记录 → 排除（响亮故障）
    IF SEA + 有效syndrome → 排除（响亮故障）
    IF ECC多比特错误（UE计数增加）→ 排除（内存故障）
    IF CE频率上升 → 不排除（SDC前兆，持续监控）
ELSE IF SError但无有效RAS Error Record:
    → SDC候选（硬件自身不知何故出错）
ELSE IF 无任何RAS记录但应用层存在异常:
    → SDC候选（经典静默损坏）
```

### 3.5 Step 4: 核心浓度分析

| 参数 | 配置值 | 说明 |
|------|--------|------|
| 异常回溯窗口 | 1周 | 平衡精度与粒度 |
| 单核异常集中度阈值（同构/big cluster） | **60%** | 鲲鹏920同构64核使用60% |
| 单核异常集中度阈值（little cluster） | **40%** | 小核执行更简单，信号更分散 |
| 兄弟核（SMT）聚合 | 启用 | SMT逻辑核聚合到物理核 |
| 应用数量阈值 | ≥2 | 至少2个不同应用在同一核心上失败 |
| Cluster级别分析 | 启用 | 按big/little cluster分别分析 |

**判定逻辑**：
```
IF 单核(或兄弟核聚合)异常占比 > 60% (同构/big)
   AND 在该核心上失败的不同应用数 ≥ 2
   THEN → 强SDC信号，进入Step 5
ELSE IF 单核异常占比 > 60% AND 仅1个应用
   THEN → 低置信度，可能是软件缺陷，需持续观察
ELSE IF 异常均匀分布在所有核心上
   THEN → 软件问题，排除SDC（命中N1）
ELSE IF 所有big核心受影响但little核心正常
   THEN → 共享组件问题（DSU L3缓存、互联总线）
ELSE IF 一个big核心+一个little核心同时异常
   THEN → 可能的cluster级问题
```

### 3.6 Step 5: 异常类型加权

**ARM64异常权重矩阵**：

| ARM64异常类型 | EC代码 | 相对比率 | 权重 |
|-------------|--------|---------|------|
| **嵌套SError / 递归异常** | — | 59.35x | ★★★★★ |
| **Data Abort (SP-relative)** | 0x24/0x25 | 20.77x | ★★★★ |
| **PXN/UXN Permission Fault** | 0x20/0x21 | 20.03x | ★★★★ |
| **Undefined Instruction** | 0x00 | 17.80x | ★★★★ |
| **BKPT/BRK** | 0x3C | 6.92x | ★★★ |
| **SError无有效RAS Record** | 0x2F | — | ★★★★ |
| Data Abort（通用） | 0x24/0x25 | ~1x | ★★ |
| Alignment Fault | 0x26 | ~1x | ★ |
| Lockups / Oops | — | ~1x | ★ |

**注意**：有有效RAS Error Record的SError/SEA应排除在SDC得分计算之外（OS层面检测到的异常是DUE信号而非SDC信号）。来源：[IEEE TC 2021] Bodmann

### 3.7 Step 6: 维修历史交叉验证

| 维修类别 | 定义 | SDC相关性 |
|---------|------|----------|
| 正确诊断 | 准确定位问题组件并正确修复 | 低 |
| **误诊** | 定位到错误组件或应用错误修复 | **高** |
| **未诊** | 无法诊断故障根因，需人工介入 | **高** |

**时间窗口**：30天内维修记录中出现误诊或未诊且问题持续复发 → 强SDC信号。

### 3.8 Step 7: FA确认

第三方硅片故障分析（FA）复现SDC行为 = 金标准。目标复现率：≥70%（行业基准15-30%）。来源：[ASPLOS 2025]

### 3.9 向量指令SDC专项检测

**3.9.1 NEON/SVE/SVE2风险矩阵**

| 指令类型 | 风险等级 | 已知故障模式 | 鲲鹏支持 |
|---------|---------|-------------|---------|
| **VFM/VFMA (向量熔合乘加)** | **关键** | 单/双精度vfm故障率最高 | 920 NEON / 930 SVE |
| **SDOT/UDOT (向量点积)** | **高** | 多比特翻转比单比特更常见 | 930 SVE2 |
| **FSQRT (向量平方根)** | **高** | 精度依赖的故障模式 | 920 NEON / 930 SVE |
| **FADDA/FADDV (向量归约)** | **中** | 跨lane归约故障 | 930 SVE |
| **谓词操作 (whilelt, ptrue)** | **中** | ARM64独有mask寄存器损坏 | 930 SVE |
| **LD1/ST1 (向量load/store)** | **中** | 数据移动损坏 | 通用NEON |

**3.9.2 SVE可变向量长度（VL）诊断**

```
1. 查询实际VL: cat /proc/cpuinfo | grep "Features" | grep sve
2. 在每个VL倍数下测试: 128, 256, 512, 1024, 2048 bits
3. 使用prctl(PR_SVE_SET_VL)设置VL进行测试
4. 对比不同VL下的故障模式——同一指令可能在某一VL下失败但另一VL下通过
```

**鲲鹏适配**：920不支持SVE（仅NEON 128-bit固定宽度）；930支持SVE/SVE2，需确认实际VL。

**3.9.3 Bit-Flip模式分析**

来源：[HPCA 2026] PinDrop对500M+测试执行分析
1. **多比特翻转 > 单比特翻转**（向量指令中）——单比特翻转模型不足以推理SDC
2. **~90%仅影响单个向量元素**——故障局部化于特定pipeline阶段
3. **无元素位置偏差**：首/中/末元素同等可能被影响
4. **无0→1或1→0方向偏差**
5. 浮点数据：bit翻转集中在尾数部分；整数数据：40.2%案例有>100%精度损失
6. **检测延迟**：针对性向量测试在10秒内即可检测到错误

**3.9.4 向量SDC检测命令**

```bash
# NEON向量压力测试（跨核对比）
for core in 0 1 2 3; do
  taskset -c $core ./neon_stress_test > /tmp/neon_out_$core &
done
wait
diff /tmp/neon_out_0 /tmp/neon_out_1  # 任何差异 = SDC

# SVE指令退役监控
perf stat -e armv8_pmuv3_0/sve_inst_retired/,\
armv8_pmuv3_0/sve_inst_spec/,\
armv8_pmuv3_0/fp_hp_spec/,\
armv8_pmuv3_0/cpu_cycles/ \
-C 0-3 -- ./sve_stress_test
# 高SVE_INST_SPEC但低SVE_INST_RETIRED = 可能的SDC导致的pipeline停顿
```

### 3.10 PMU偏差检测

**3.10.1 PMU事件分类表**

| 类别 | 关键ARM64 PMU事件 | 诊断价值 |
|------|-------------------|---------|
| **向量** | `ASE_SPEC`, `SVE_INST_SPEC`, `SVE_INST_RETIRED` | 向量指令执行异常 |
| **浮点** | `FP_HP_SPEC`, `FP_SP_SPEC`, `FP_DP_SPEC` | 浮点计算异常 |
| **缓存** | `L1D_CACHE_REFILL`, `L1I_CACHE_REFILL`, `L2D_CACHE_REFILL` | 缓存行为异常（L1I_REFILL尖峰=指令缓存损坏） |
| **分支** | `BR_MIS_PRED`, `BR_PRED`, `BR_RETIRED` | 控制流异常（BR_MIS_PRED/BR_PRED尖峰=分支预测器或NZCV损坏） |
| **内存** | `LD_SPEC`, `ST_SPEC`, `LDST_SPEC` | 数据移动异常 |
| **TLB** | `L1D_TLB_REFILL`, `L1I_TLB_REFILL` | 地址转换异常 |
| **指令** | `INST_RETIRED`, `INST_SPEC`, `CPU_CYCLES` | IPC异常检测 |

**3.10.2 监控场景**

```bash
# 场景1: 向量SDC监控
perf stat -e armv8_pmuv3_0/sve_inst_spec/,\
armv8_pmuv3_0/sve_inst_retired/,\
armv8_pmuv3_0/fp_hp_spec/ -C 0-7 -- your_workload

# 场景2: 缓存相关SDC监控
perf stat -e armv8_pmuv3_0/l1d_cache_refill/,\
armv8_pmuv3_0/l1i_cache_refill/,\
armv8_pmuv3_0/l2d_cache_refill/ -- your_workload

# 场景3: 控制流SDC监控
perf stat -e armv8_pmuv3_0/br_mis_pred/,\
armv8_pmuv3_0/br_pred/,\
armv8_pmuv3_0/inst_retired/ -- your_workload
```

**3.10.3 HPC偏差协议（CHAOS方法）**

```
1. 在目标CPU上运行工作负载，捕获PMU基线
2. 与已知良好兄弟核或历史数据的预期基线对比
3. 计算每个PMU事件的MAPD（Mean Absolute Percentage Deviation）
4. 标记MAPD > 阈值的事件（即使程序输出看似正确）
5. 将标记事件与ARM64脆弱性排名交叉引用
```

**关键洞察**：即使程序输出表现为"Masked"（无可见错误），HPC偏差可能达到83,000%。始终检查HPC偏差，即使输出看似正确。来源：[IEEE 2023] CHAOS

---

## 第四章：正向判定规则P1-P14

当服务器满足以下条件时，判定为SDC正向候选。

### 规则P1: 单核异常集中度 — IRON RULE

- **条件**：1周回溯窗口内，单个CPU核心（或兄弟核聚合）异常数占该服务器总异常数比例 >60%（同构鲲鹏/big cluster）或 >40%（little cluster）
- **判定**：强SDC信号，硬件缺陷通常只影响特定物理核心
- **权重**：+15分
- **置信度**：高
- **来源**：[ASPLOS 2025] HWSentinel §4.2.3

**ARM64适配**：鲲鹏920同构64核使用60%阈值；鲲鹏930 DynamIQ big cluster 60% / little cluster 40%；兄弟核（SMT）必须聚合。

### 规则P2: 多应用共现

- **条件**：至少2个不同应用在同一CPU核心或兄弟核对上产生异常
- **判定**：多个独立应用在同一核心上失败，根因大概率是硬件而非软件
- **权重**：+8分
- **置信度**：高
- **来源**：[ASPLOS 2025] HWSentinel §4.2.3

**注意**：需排除ARM弱内存模型下DMB/DSB屏障缺失导致的软件异常。

### 规则P3: 非计划重启频率异常

- **条件**：通用服务器30天内非计划重启 ≥6次；AI服务器 ≥3次
- **判定**：系统频繁中断，可能因SDC导致不可恢复的内核异常
- **权重**：+10分
- **置信度**：中
- **来源**：[ASPLOS 2025] HWSentinel §4.2.1, §4.2.7

### 规则P4: 高SDC相关ARM64异常类型出现在同一核心

- **条件**：以下任一异常类型在单核上出现：Undefined Instruction (EC=0x00)、PXN/UXN Permission Fault (EC=0x20/0x21)、Data Abort SP-relative (EC=0x24/0x25)、BKPT/BRK (EC=0x3C)、嵌套SError (59.35x)、SError无有效RAS Record
- **判定**：这些异常类型在舰队中罕见但在SDC诱导CPU上高度集中
- **权重**：+12分
- **置信度**：高
- **来源**：[ASPLOS 2025] HWSentinel §5.3

### 规则P5: RAS静默

- **条件**：异常发生相近时间戳，RAS Error Records / SEL中无CPU相关硬件故障条目
- **判定**：SDC"静默"特性的核心判定条件
- **权重**：+12分
- **置信度**：高
- **来源**：[ASPLOS 2025] HWSentinel §4.2.2

**ARM64判定**：无有效RAS Error Record的SError → 仍视为SDC候选；有有效RAS Error Record的SError → 响亮故障，排除。

### 规则P6: 维修历史中反复误诊或未诊

- **条件**：30天内维修记录中出现误诊或未诊，且问题持续复发
- **判定**：SDC的隐蔽性导致传统诊断手段无法定位根因
- **权重**：+10分
- **置信度**：中
- **来源**：[ASPLOS 2025] HWSentinel §4.2.5

### 规则P7: 独立FA可复现（金标准）

- **条件**：第三方硅片故障分析能够复现SDC行为
- **判定**：最终确认SDC，目标复现率≥70%
- **权重**：+20分
- **置信度**：高（金标准）
- **来源**：[ASPLOS 2025] HWSentinel §5.7

### 规则P8: 向量指令SDC信号

- **条件**：以下任一出现：NEON/SVE VFM/VFMA指令计算结果偏差（跨核对比不一致）；SVE指令在不同VL下表现不一致；向量谓词寄存器异常；向量load/store (LD1/ST1) 数据损坏
- **判定**：向量指令是SDC最高风险区域
- **权重**：+12分
- **置信度**：高
- **来源**：[ASPLOS 2026] SEVI, [HPCA 2026] PinDrop

### 规则P9: NZCV条件标志异常

- **条件**：条件分支（B.cond, CSEL, CCMP）执行路径与预期不符，且排除编译器优化和内存模型问题
- **判定**：NZCV是ARM64独有脆弱点，条件标志bit-flip导致控制流静默偏离
- **权重**：+8分
- **置信度**：中
- **来源**：[IEEE 2023] Differential FI

### 规则P10: 失败持续性

- **条件**：已确认至少一次SDC测试失败的机器，在持续测试中保持失败状态（>71%故障机器持续失败至少2年，失败率保持恒定）
- **判定**：一旦确认SDC，机器极大概率会持续产生错误结果
- **权重**：+8分
- **置信度**：中
- **来源**：[HPCA 2026] PinDrop §V-B Observation 6

### 规则P11: 兄弟核共失效

- **条件**：同一次测试中，同一物理核心的两个兄弟逻辑核（SMT线程）同时报告失败
- **判定**：兄弟核共享相同物理硬件（ALU、FPU、NEON、L1缓存），硬件缺陷同时影响两个逻辑线程
- **权重**：+10分
- **置信度**：中
- **来源**：[HPCA 2026] PinDrop §VI-A Observation 8

**注意**：需区分真正的硬件共失效和软件副作用——一个逻辑核的静默错误值可能导致非故障逻辑核的软件级异常。

### 规则P12: 不一致错误检测 — IRON RULE

- **条件**：同一条指令，在相同架构输入下，在同一线程内的不同执行上下文中产生不同的架构输出
- **判定**：最隐蔽的缺陷（最可能逃逸制造测试的缺陷）导致不一致错误。传统功能测试隐式假设缺陷导致一致错误，因此遗漏了大量有缺陷的芯片
- **权重**：+15分
- **置信度**：高（有形式化理论基础+3000+真实硬件验证）
- **来源**：[arXiv 2026] ITHICA §3, §7.1, Finding 1

**检测方法**：使用ITHICA的Arith/Mem/MemDiv/Br变换对程序进行指令级插桩，比较原始指令和验证指令的输出。任何不匹配即为SDC检测。

**执行上下文驱动**：指令是否表现出缺陷诱导的错误，取决于其执行时的序列驱动执行上下文，而非指令的动态执行频率或特定输入值。测试程序选择至关重要——应使用多样化程序作为测试。来源：[arXiv 2026] ITHICA Finding 5, 7

**多指令类型共受影响**：同一缺陷导致多种指令类型（算术、浮点、向量、内存）出现错误，差异可达六个数量级。44%的被检测服务器在多种指令类型上出现错误。不能仅依赖向量测试进行硬件定位。来源：[arXiv 2026] ITHICA §7.5, Finding 10

### 规则P13: FI预测准确性验证

- **条件**：候选服务器在Gem5 FI模拟中，微架构级故障注入产生的SDC率与舰队观测的SDC率在1个数量级内一致
- **判定**：FI验证为SDC归因提供独立于物理测试的佐证
- **权重**：+8分
- **置信度**：中
- **来源**：[IEEE TC 2021] Bodmann §V, §VI

**ARM64适配**：使用Gem5-MARVEL框架，配置TaiShan核心参数化模型。注意：FI产生的DUE率仅为下界估计，DUE相关信号不应作为主要SDC判定依据。

### 规则P14: SoC/OS隔离效应规则

- **条件**：SDC信号仅限于CPU核心内部（指令执行、寄存器、ALU、NEON/SVE），且SoC外围组件（DSU L3缓存、Hydra互联、内存控制器）的RAS记录正常
- **判定**：SDC仅由CPU核心贡献，SoC集成和OS增加的是DUE而非SDC
- **权重**：+8分
- **置信度**：中
- **来源**：[IEEE TC 2021] Bodmann §IV, §V

**ARM64适配**：鲲鹏920确认Hydra互联、L3共享缓存（64MB）、DDR4控制器的RAS记录无异常；鲲鹏930确认DSU-110 L3、互联总线、DDR5控制器的RAS记录无异常。

---

## 第五章：负向否定规则N1-N13

以下规则用于排除SDC可能性。**命中任何一条即排除SDC**。

### 规则N1: 异常均匀分布 → 软件问题

- **条件**：异常在服务器所有CPU核心上均匀分布，无单核集中现象
- **排除**：多核同时以相同水平出现异常，更可能是应用导致的而非硬件
- **正确做法**：排查应用软件缺陷
- **排除权重**：-20分
- **来源**：[ASPLOS 2025] HWSentinel §4.3.1

### 规则N2: 单应用+相同回溯 → 软件缺陷

- **条件**：只有1个应用在特定核心上失败，且该应用在舰队中大量服务器上以相同backtrace失败
- **排除**：单一工作负载在大量服务器上以相同backtrace失败，是软件故障特征
- **正确做法**：修复应用软件Bug
- **排除权重**：-15分
- **来源**：[ASPLOS 2025] HWSentinel §4.1.6

### 规则N3: RAS Error Records中有明确CPU硬件故障 → 响亮故障

- **条件**：RAS Error Records / SEL中在异常相近时间戳存在CPU相关硬件故障条目（SError+有效ERR\<n\>STATUS、SEA+有效syndrome、ECC多比特UE）
- **排除**：已检测到的"响亮"硬件故障，非静默损坏
- **正确做法**：按硬件故障处理流程修复
- **排除权重**：-30分
- **来源**：[ASPLOS 2025] HWSentinel §4.2.2

### 规则N4: Fuzzer/测试工具等有意引发崩溃的工作负载 → 排除

- **条件**：异常由fuzzer、压力测试工具、故障注入工具等有意引发系统崩溃的工作负载产生
- **排除**：应用设计为有意崩溃系统，非SDC
- **正确做法**：从分析中排除fuzzer工作负载
- **排除权重**：-15分
- **来源**：[ASPLOS 2025] HWSentinel §4.4

### 规则N5: 重启伴随完整crash dump且有明确硬件诊断 → 非静默

- **条件**：非计划重启伴随完整crash dump，且crash dump中包含明确硬件故障诊断信息
- **排除**：已有足够遥测信息进行硬件健康检查和修复
- **正确做法**：按crash dump诊断结果处理
- **排除权重**：-15分
- **来源**：[ASPLOS 2025] HWSentinel

### 规则N6: 已知软件Bug/CVE导致的异常模式 → 软件根因

- **条件**：异常模式匹配已知软件Bug或CVE特征（特定kernel版本+特定backtrace）
- **排除**：软件根因，非硬件SDC
- **正确做法**：升级kernel或应用补丁
- **排除权重**：-20分
- **来源**：[ASPLOS 2025] HWSentinel

### 规则N7: 大规模同步异常 → 软件/配置变更

- **条件**：短时间内（数小时）大量服务器（数百台）同时出现相同异常模式
- **排除**：SDC是硬件个体问题，不会短时间内大规模同步出现
- **正确做法**：排查软件部署、配置变更或kernel rollback
- **排除权重**：-30分
- **来源**：[ASPLOS 2025] HWSentinel

### 规则N8: 缺少内存屏障导致的并发异常 → 软件问题

- **条件**：异常仅出现在多线程并发场景，且代码中缺少DMB/DSB屏障
- **排除**：ARM弱内存模型下软件移植问题，非SDC
- **正确做法**：添加正确的内存屏障指令
- **排除权重**：-20分
- **来源**：ARM架构规范

### 规则N9: 非确定性环境因素导致的瞬态异常

- **条件**：SDC-like行为与瞬态环境异常（温度尖峰、电压骤降、电源事件）完全相关，且恢复正常后不再出现
- **排除**：环境瞬态异常，非硬件缺陷
- **正确做法**：改善环境条件，在固定频率下测试
- **排除权重**：-15分
- **来源**：[SOSP 2023] Alibaba

**注意**：ARM64的DVFS激进频率调节可能掩盖温度效应，诊断时应在固定频率下测试。

### 规则N10: 单次测试阴性不可靠 — IRON RULE

- **条件**：机器在单次或少数几次SDC测试中通过（未检测到故障），即被判定为"健康"
- **排除**：PinDrop连续测试分析表明机器可能在测试数年后才开始出现首次SDC失败。单次测试通过不代表机器健康
- **正确做法**：建立连续测试机制，测试重访周期≤30天（PinDrop最优实践平均15天）
- **排除权重**：-30分
- **来源**：[HPCA 2026] PinDrop §V-B Observation 4, 5

### 规则N11: DUE优先排除规则 — IRON RULE

- **条件**：候选服务器异常信号主要来自OS层面检测到的SError/SEA（有有效RAS Error Record），而非应用层静默数据损坏
- **排除**：OS检测到的SError/SEA是DUE信号——内核panic handler、MMU、异常处理框架将CPU核心错误转化为可检测的DUE。这些错误已被检测到，不是SDC
- **正确做法**：按DUE故障处理流程排查和修复。频繁DUE可能指示CPU核心存在问题，但属于"响亮"故障而非"静默"故障
- **排除权重**：-30分
- **来源**：[IEEE TC 2021] Bodmann §IV-B, [ASPLOS 2025] HWSentinel §4.2.2

**ARM64适配**：有有效ERR\<n\>STATUS的SError → DUE，排除SDC；有有效syndrome的SEA → DUE，排除SDC；仅当SError无有效RAS Error Record时 → 仍为SDC候选。

### 规则N12: 微架构复杂度误判规则 — IRON RULE

- **条件**：将Kunpeng 920（TaiShan v110）的诊断规则直接应用于Kunpeng 930（TaiShan v200），未考虑微架构差异（流水线深度、发射宽度、SVE/SVE2引入、ROB/加载队列/存储队列大小、推测执行激进程度、缓存层次和替换策略变化）
- **排除**：不同微架构复杂度的核心具有不同的故障传播路径和掩蔽概率。跨代际直接复用诊断规则会导致误判
- **正确做法**：1.新架构部署初期使用保守阈值（核心浓度40%而非60%）；2.通过舰队数据重新校准异常类型-权重矩阵；3.进行Gem5 FI预评估；4.建立鲲鹏代际SDC特征数据库
- **排除权重**：-25分
- **来源**：[IEEE TC 2021] Bodmann §V-C, §VI-A

### 规则N13: ITHICA检测可靠性综合规则

- **条件**：基于指令使用压力（动态执行频率）作为缺陷检测预测因子；或使用单指令/基本块级别短测试进行缺陷检测且结果为阴性；或基于ISA级观察将缺陷归因于特定硬件单元
- **排除**：
  - 指令使用压力不可靠：59%案例中检测到故障的测试并非执行失败操作码频率最高的测试。来源：[arXiv 2026] ITHICA Finding 7
  - 短测试不可靠：除极少数例外（1/14服务器），单指令测试和基本块测试无法复现缺陷诱导的错误。短测试阴性结果不能作为硬件健康的证据
  - ISA级硬件定位不可靠：67%向量指令错误服务器也在其他指令类型上出错。仅基于指令类型做出硬件定位结论不可靠
- **正确做法**：使用多样化程序覆盖不同执行上下文；使用长程序或多指令序列测试建立必要执行上下文；使用覆盖多种指令类型（算术、浮点、向量、内存、控制流）的测试
- **排除权重**：-20分
- **来源**：[arXiv 2026] ITHICA §7.4, §7.5, Finding 7, 8, 10

---

## 第六章：量化SDC概率评分模型

### 6.1 评分公式

```
正向分 P_score = Σ(命中的P规则分值)
负向分 N_score = Σ(命中的N规则分值)    // N规则分值为负数
净分 = P_score + N_score
SDC概率 = f(净分)
```

**P规则分值表**：

| 规则 | 分值 | 规则 | 分值 |
|------|------|------|------|
| P1 (IRON RULE) | +15 | P8 | +12 |
| P2 | +8 | P9 | +8 |
| P3 | +10 | P10 | +8 |
| P4 | +12 | P11 | +10 |
| P5 | +12 | P12 (IRON RULE) | +15 |
| P6 | +10 | P13 | +8 |
| P7（金标准） | +20 | P14 | +8 |

**N规则排除权重表**：

| 规则 | 权重 | 规则 | 权重 |
|------|------|------|------|
| N1 | -20 | N8 | -20 |
| N2 | -15 | N9 | -15 |
| N3 | -30 | N10 (IRON RULE) | -30 |
| N4 | -15 | N11 (IRON RULE) | -30 |
| N5 | -15 | N12 (IRON RULE) | -25 |
| N6 | -20 | N13 | -20 |
| N7 | -30 | | |

### 6.2 概率映射函数

**线性映射公式**：
```
SDC概率 = min(99, max(0, 净分 × 2))%
```

**映射表**：

| 净分 | SDC概率 | 置信度等级 |
|------|---------|-----------|
| ≥40 | ≥80% | 高置信度 |
| 25-39 | 50-79% | 中置信度 |
| 10-24 | 20-49% | 低置信度 |
| <10 | <20% | 排除 |

**示例**：
- 净分=45 → 概率=90%（高置信度）
- 净分=30 → 概率=60%（中置信度）
- 净分=15 → 概率=30%（低置信度）
- 净分=5 → 概率=10%（排除）

### 6.3 四级置信度标准

| 等级 | 条件 | 处理建议 |
|------|------|---------|
| **高置信度** | 概率 ≥ 80%（净分 ≥ 40）且无N规则命中 | 立即移入隔离池，安排FA分析 |
| **中置信度** | 概率 50%-79%（净分 25-39）且无N规则命中 | 标记观察，下次维护窗口深度测试，增加向量测试和PMU偏差检测 |
| **低置信度** | 概率 20%-49%（净分 10-24）且无N规则命中 | 维持生产运行，增加监控频率，监控CE计数器趋势和PMU事件偏差 |
| **排除** | 概率 < 20%（净分 < 10）或任一N规则命中 | 非SDC，按其他故障类型处理 |

### 6.4 置信区间计算方法

基于规则命中数和数据完整度计算置信区间宽度：

| 条件 | 置信区间宽度 |
|------|------------|
| ≥5条P规则命中 且 数据完整度 ≥ 80% | ±5% |
| 3-4条P规则命中 或 数据完整度 50-79% | ±10% |
| ≤2条P规则命中 或 数据完整度 < 50% | ±20% |

**数据完整度评分**：
- Kernel异常日志可用：+25%
- RAS Error Records可用：+25%
- 重启历史可用：+20%
- 维修历史可用：+15%
- SDC测试结果可用：+15%

**示例**：净分=50 → 概率=99%，命中5条P规则，数据完整度85% → 置信区间 [94%, 100%]

### 6.5 可程序化决策树

```python
def diagnose_sdc(p_rules_hit, n_rules_hit, data_completeness):
    """
    P规则命中列表: p_rules_hit = ["P1", "P2", "P5", ...]
    N规则命中列表: n_rules_hit = ["N3", ...]
    数据完整度: data_completeness = 0-100
    """
    
    # Step 1: 检查N规则（任一命中即排除）
    if len(n_rules_hit) > 0:
        return {
            "conclusion": "EXCLUDED",
            "probability": 0,
            "confidence_level": "EXCLUDED",
            "reason": f"N规则命中: {n_rules_hit}"
        }
    
    # Step 2: 计算P_score
    p_weights = {
        "P1": 15, "P2": 8, "P3": 10, "P4": 12, "P5": 12,
        "P6": 10, "P7": 20, "P8": 12, "P9": 8, "P10": 8,
        "P11": 10, "P12": 15, "P13": 8, "P14": 8
    }
    p_score = sum(p_weights[r] for r in p_rules_hit)
    
    # Step 3: 计算净分（无N规则命中，N_score=0）
    net_score = p_score
    
    # Step 4: 映射概率
    probability = min(99, max(0, net_score * 2))
    
    # Step 5: 确定置信度等级
    if probability >= 80:
        confidence_level = "HIGH"
        conclusion = "SDC"
    elif probability >= 50:
        confidence_level = "MEDIUM"
        conclusion = "SDC_CANDIDATE"
    elif probability >= 20:
        confidence_level = "LOW"
        conclusion = "OBSERVE"
    else:
        confidence_level = "EXCLUDED"
        conclusion = "EXCLUDED"
    
    # Step 6: 计算置信区间
    num_p_hits = len(p_rules_hit)
    if num_p_hits >= 5 and data_completeness >= 80:
        ci_width = 5
    elif num_p_hits >= 3 or data_completeness >= 50:
        ci_width = 10
    else:
        ci_width = 20
    
    ci_lower = max(0, probability - ci_width)
    ci_upper = min(100, probability + ci_width)
    
    return {
        "conclusion": conclusion,
        "probability": probability,
        "confidence_level": confidence_level,
        "confidence_interval": [ci_lower, ci_upper],
        "p_score": p_score,
        "net_score": net_score,
        "rules_hit": p_rules_hit
    }
```

---

## 第七章：AI Agent诊断报告规范

### 7.1 Markdown格式诊断报告模板（人读）

```markdown
# SDC诊断报告

## 服务器信息
- **主机名**：[hostname]
- **IP地址**：[ip]
- **CPU型号**：[cpu_model]
- **CPU架构**：[architecture]
- **核心数**：[core_count]
- **SMT状态**：[smt_enabled]
- **诊断时间**：[timestamp]
- **诊断ID**：[diagnosis_id]

## 判定结论
- **结论**：[SDC / SDC候选 / 观察 / 排除]
- **SDC概率**：[X]%
- **置信区间**：[lower]% - [upper]%
- **置信度等级**：[HIGH / MEDIUM / LOW / EXCLUDED]

## 命中规则详情

### 正向规则命中（P规则）
| 规则ID | 规则名称 | 权重 | 证据 |
|--------|---------|------|------|
| [PX] | [名称] | [+X分] | [证据描述] |
| ... | ... | ... | ... |

**P_score合计**：[X]分

### 负向规则检查结果（N规则）
| 规则ID | 规则名称 | 结果 | 说明 |
|--------|---------|------|------|
| [NX] | [名称] | 未命中 | — |
| ... | ... | ... | ... |

**N规则命中数**：0（无排除）

## 数据证据摘要
- **RAS记录**：[无CPU相关故障条目 / 有SError+有效RAS Record / ...]
- **核心浓度**：[核心X占比Y%，应用数Z]
- **异常类型**：[Undefined Instruction × N次 / Data Abort × M次 / ...]
- **重启历史**：[30天内N次非计划重启]
- **维修历史**：[误诊N次 / 未诊M次 / 无记录]
- **PMU偏差**：[事件X偏差Y% / 无显著偏差]

## 处置建议
1. [立即移入隔离池 / 标记观察 / 维持生产运行 / 排除SDC]
2. [安排FA分析 / 下次维护窗口深度测试 / 增加监控频率]
3. [具体测试建议：向量测试 / PMU监控 / 连续测试]
```

### 7.2 JSON格式诊断报告Schema（机读）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SDC诊断报告",
  "type": "object",
  "required": ["diagnosis_id", "timestamp", "server_info", "verdict", "rules_hit", "scoring", "evidence_summary", "recommendations"],
  "properties": {
    "diagnosis_id": {
      "type": "string",
      "description": "诊断唯一标识符"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "诊断时间（ISO8601格式）"
    },
    "server_info": {
      "type": "object",
      "required": ["hostname", "ip", "cpu_model", "architecture", "core_count", "smt_enabled"],
      "properties": {
        "hostname": {"type": "string", "description": "主机名"},
        "ip": {"type": "string", "description": "IP地址"},
        "cpu_model": {"type": "string", "description": "CPU型号"},
        "architecture": {"type": "string", "description": "CPU架构（如ARM64）"},
        "core_count": {"type": "integer", "description": "CPU核心数"},
        "smt_enabled": {"type": "boolean", "description": "SMT是否启用"},
        "kunpeng_model": {"type": "string", "enum": ["920", "930", "unknown"], "description": "鲲鹏型号"}
      }
    },
    "verdict": {
      "type": "object",
      "required": ["conclusion", "sdc_probability", "confidence_level", "confidence_interval"],
      "properties": {
        "conclusion": {
          "type": "string",
          "enum": ["SDC", "SDC_CANDIDATE", "OBSERVE", "EXCLUDED"],
          "description": "判定结论"
        },
        "sdc_probability": {
          "type": "number",
          "minimum": 0,
          "maximum": 100,
          "description": "SDC概率（0-100）"
        },
        "confidence_level": {
          "type": "string",
          "enum": ["HIGH", "MEDIUM", "LOW", "EXCLUDED"],
          "description": "置信度等级"
        },
        "confidence_interval": {
          "type": "object",
          "required": ["lower", "upper"],
          "properties": {
            "lower": {"type": "number", "minimum": 0, "maximum": 100, "description": "置信区间下界"},
            "upper": {"type": "number", "minimum": 0, "maximum": 100, "description": "置信区间上界"}
          }
        }
      }
    },
    "rules_hit": {
      "type": "object",
      "required": ["positive_rules", "negative_rules"],
      "properties": {
        "positive_rules": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["rule_id", "rule_name", "weight", "evidence"],
            "properties": {
              "rule_id": {"type": "string", "description": "规则ID（如P1）"},
              "rule_name": {"type": "string", "description": "规则名称"},
              "weight": {"type": "integer", "description": "规则权重分值"},
              "is_iron_rule": {"type": "boolean", "description": "是否为IRON RULE"},
              "evidence": {"type": "string", "description": "命中证据描述"}
            }
          }
        },
        "negative_rules": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["rule_id", "rule_name", "weight", "evidence"],
            "properties": {
              "rule_id": {"type": "string", "description": "规则ID（如N1）"},
              "rule_name": {"type": "string", "description": "规则名称"},
              "weight": {"type": "integer", "description": "排除权重分值（负数）"},
              "is_iron_rule": {"type": "boolean", "description": "是否为IRON RULE"},
              "evidence": {"type": "string", "description": "命中证据描述"}
            }
          }
        }
      }
    },
    "scoring": {
      "type": "object",
      "required": ["p_score", "n_score", "net_score"],
      "properties": {
        "p_score": {"type": "integer", "description": "正向分（P规则分值之和）"},
        "n_score": {"type": "integer", "description": "负向分（N规则分值之和，负数或0）"},
        "net_score": {"type": "integer", "description": "净分 = P_score + N_score"},
        "data_completeness": {"type": "number", "minimum": 0, "maximum": 100, "description": "数据完整度（0-100）"}
      }
    },
    "evidence_summary": {
      "type": "object",
      "required": ["ras_records", "core_concentration", "exception_types", "reboot_history", "repair_history"],
      "properties": {
        "ras_records": {"type": "string", "description": "RAS记录摘要"},
        "core_concentration": {"type": "string", "description": "核心浓度分析摘要"},
        "exception_types": {"type": "string", "description": "异常类型分布摘要"},
        "reboot_history": {"type": "string", "description": "重启历史摘要"},
        "repair_history": {"type": "string", "description": "维修历史摘要"},
        "pmu_deviation": {"type": "string", "description": "PMU偏差检测摘要"},
        "vector_test_results": {"type": "string", "description": "向量测试结果摘要"}
      }
    },
    "recommendations": {
      "type": "array",
      "items": {"type": "string"},
      "description": "处置建议列表"
    }
  }
}
```

### 7.3 报告必填字段定义

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| diagnosis_id | string | 是 | 诊断唯一标识符 |
| timestamp | string | 是 | 诊断时间（ISO8601） |
| server_info.hostname | string | 是 | 主机名 |
| server_info.ip | string | 是 | IP地址 |
| server_info.cpu_model | string | 是 | CPU型号 |
| server_info.core_count | integer | 是 | CPU核心数 |
| verdict.conclusion | string | 是 | 判定结论 |
| verdict.sdc_probability | number | 是 | SDC概率（0-100） |
| verdict.confidence_level | string | 是 | 置信度等级 |
| verdict.confidence_interval | object | 是 | 置信区间 |
| rules_hit.positive_rules | array | 是 | 命中的P规则列表 |
| rules_hit.negative_rules | array | 是 | 命中的N规则列表 |
| scoring.p_score | integer | 是 | 正向分 |
| scoring.n_score | integer | 是 | 负向分 |
| scoring.net_score | integer | 是 | 净分 |
| evidence_summary | object | 是 | 数据证据摘要 |
| recommendations | array | 是 | 处置建议列表 |

---

## 第八章：鲲鹏处理器专项适配

### 8.1 鲲鹏920/930架构特征表

| 特征 | Kunpeng 920 | Kunpeng 930 | SDC诊断意义 |
|------|------------|------------|-----------|
| **ISA** | ARMv8.2-A | ARMv9-A | 920仅NEON；930支持SVE2 |
| **核心数** | 64核 (TaiShan v110) | TaiShan v200系列 | 同构分析，60%浓度阈值 |
| **向量** | NEON 128-bit | SVE/SVE2 | 920向量诊断仅NEON；930需SVE VL测试 |
| **RAS** | ARMv8.2 RAS | ARMv9完整RAS | 920基础RAS；930全功能RAS |
| **SMT** | 支持 | 支持 | 兄弟核聚合分析 |
| **缓存** | L1: 64KB I/D, L2: 512KB, L3: 64MB共享 | 待确认 | 大L3共享缓存，共享组件故障影响多核 |
| **互联** | 华为自研Hydra互联 | 待确认 | 互联总线SDC影响跨socket通信 |
| **内存** | 8通道DDR4 | DDR5 | ECC标准配置 |
| **BMC** | 华为iBMC (兼容IPMI/Redfish) | 华为iBMC | SEL访问通过iBMC |

### 8.2 鲲鹏诊断命令

```bash
# CPU信息
lscpu | grep -E "Model name|Architecture|CPU\(s\)|Thread|Core|Socket"
cat /proc/cpuinfo | grep -E "CPU part|CPU implementer|Features"

# Kernel日志
dmesg | grep -iE "ras|serror|sea|data.abort|hisilicon|kunpeng"
journalctl -k --since "30 days ago" | grep -iE "serror|sea|data.abort|undefined|permission|alignment|brk"

# iBMC SEL访问
ipmitool -H <iBMC_IP> -U <user> -P <pass> sel list
ipmitool -H <iBMC_IP> -U <user> -P <pass> sel elist

# 温度监控
cat /sys/class/thermal/thermal_zone*/temp
cat /sys/class/thermal/thermal_zone*/type

# RAS
cat /sys/devices/system/edac/mc/mc*/ce_count
cat /sys/devices/system/edac/mc/mc*/ue_count
grep -i "serror\|SError" /proc/interrupts

# PMU
perf stat -e armv8_pmuv3_0/sve_inst_retired/,\
armv8_pmuv3_0/br_mis_pred/,\
armv8_pmuv3_0/l1d_cache_refill/ -- sleep 10
```

### 8.3 big.LITTLE/DynamIQ差异化阈值

| 参数 | big cluster / 同构 | little cluster | 说明 |
|------|-------------------|---------------|------|
| 核心浓度阈值 | 60% | 40% | 小核执行更简单，异常信号更分散 |
| SMT兄弟核聚合 | 启用 | 启用 | 共享物理硬件 |
| Cluster级分析 | 启用 | 启用 | 按cluster分别分析 |

**异构诊断逻辑**：
- 所有big核心受影响但little核心正常 → 共享组件问题（DSU L3缓存、互联）
- 一个big核心+一个little核心同时异常 → 可能的cluster级问题
- SMT兄弟核应聚合分析

**异构诊断命令**：
```bash
# 识别CPU拓扑
lscpu | grep -E "Cluster|Core|Thread|Model"
cat /sys/devices/system/cpu/cpu*/topology/physical_package_id
cat /sys/devices/system/cpu/cpu*/topology/core_id

# big vs little识别
cat /sys/devices/system/cpu/cpu*/cpu_capacity  # 更高 = big核心
cat /sys/devices/system/cpu/cpu*/cpufreq/cpuinfo_max_freq

# Per-cluster PMU监控
perf stat -e armv8_pmuv3_0/inst_retired/ -C 0-3  # big cluster
perf stat -e armv8_pmuv3_0/inst_retired/ -C 4-7  # little cluster
```

### 8.4 配置参数表

| 参数 | 默认值 | 调优方向 |
|------|--------|---------|
| 重启回溯窗口 | 30天 | 增加→提高置信度，但可能遗漏短期SDC |
| 重启阈值（通用） | 6次 | 降低→更敏感，增加→减少误报 |
| 重启阈值（AI） | 3次 | 更严格，因AI训练中断影响大 |
| 核心浓度阈值（同构/big） | 60% | 鲲鹏920/930同构使用60% |
| 核心浓度阈值（little） | 40% | 仅异构集群使用 |
| 应用数量阈值 | 2 | 增加→减少误报但可能遗漏真实SDC |
| 异常回溯窗口 | 1周 | 缩短→更快响应，延长→更稳定信号 |
| 向量/FP负载权重 | 1.2 | 向量密集型工作负载更高权重 |
| NZCV异常权重 | 1.0 | ARM独有脆弱点 |
| SVE VL测试范围 | 128-2048 | 根据实际硬件VL范围调整 |
| 测试重访周期（PinDrop） | ≤30天 | 新架构首季度≤15天，稳定后≤30天 |
| 测试种子记录（PinDrop） | 启用 | 失败时记录种子，用于复现和诊断 |
| 连续测试最小观察期（PinDrop） | 2季度 | 单次测试阴性不可靠，需持续观察 |

### 8.5 温度-SDC管理

**关键发现**：SDC频率与温度呈指数关系（log10频率 vs 温度线性，Pearson r > 0.75）。来源：[SOSP 2023] Alibaba

**管理策略**：
1. 每个ARM64 CPU存在最低触发温度
2. 监控CPU温度趋势；温度尖峰超过阈值 = SDC风险
3. 实现工作负载回退当温度接近阈值
4. ARM64的DVFS激进频率调节可能掩盖温度效应——诊断时应在固定频率下测试

**温度监控命令**：
```bash
while true; do
  temp=$(cat /sys/class/thermal/thermal_zone0/temp)
  if [ $temp -gt $THRESHOLD ]; then
    echo $MAX_QUOTA > /sys/fs/cgroup/cpu/group/cpu.max
  fi
  sleep 1
done
```

### 8.6 鲲鹏可用工具列表

| 工具 | 用途 | 鲲鹏支持 |
|------|------|---------|
| **perf** | PMU分析 | 原生支持ARM PMUv3 |
| **gem5** | 周期精确模拟 | 需TaiShan核心模型（可能需定制） |
| **GeFIN** | gem5故障注入 | 需ARM64 gem5配置 |
| **Gem5-MARVEL** | 异构SoC弹性分析 | 原生ARM64 big.LITTLE |
| **CHAOS** | gem5可控硬件故障注入 | ARM64 via gem5 |
| **Valgrind** | 内存调试 | ARM64移植版本 |
| **LLVM** | 编译器（ITHICA变换） | 原生ARM64后端 |
| **华为iBMC** | BMC遥测 | 原生支持 |

### 8.7 场景推荐表

| 场景 | 推荐方法 | 理由 |
|------|---------|------|
| 高频维护工作负载 | Fleetscanner | 维护窗口多，测试机会充足 |
| 性能敏感工作负载 | HWSentinel | 无性能开销 |
| 新架构早期部署（鲲鹏930） | HWSentinel + PinDrop连续测试 | 测试程序尚未成熟，HWSentinel架构无关；PinDrop捕获延迟发作 |
| 向量密集型工作负载 | HWSentinel + PinDrop向量测试 | 向量指令SDC风险最高 |
| AI训练工作负载 | HWSentinel (阈值3) + PinDrop GEMM测试 | 重启影响大，矩阵乘法故障率高 |
| 已知SDC热点区域 | 多方法联合 | 最大化覆盖 |
| 鲲鹏异构集群 | HWSentinel (cluster感知) + PinDrop核心亲和性 | 按cluster分析，兄弟核共失效检测 |
| 长期稳定性评估 | PinDrop连续测试 | 唯一能捕获数年后首次失败的方法 |

---

## 第九章：核心研究发现摘要

### 9.1 Bodmann 2021五项核心发现

| 发现 | Kunpeng启示 |
|------|------------|
| **发现1**: SDC率仅由CPU核心决定（Cortex-A5裸机与Cortex-A9 SoC+Linux的SDC率统计无显著差异） | SDC诊断应聚焦TaiShan核心本身，而非SoC外围组件。当SoC外围RAS正常但核心内存在异常时，SDC信号可信度最高 |
| **发现2**: SoC集成增加DUE率但不影响SDC率（看门狗定时器、共享资源冲突检测、外设错误传播将部分静默错误转化为DUE） | 鲲鹏Hydra互联、L3共享缓存、DDR4/5内存控制器故障导致DUE增加而非SDC增加。频繁DUE时应优先排查SoC共享组件 |
| **发现3**: OS增加DUE率但不影响SDC率（内核panic handler、MMU、调度器/中断处理将CPU核心错误转化为DUE） | Linux内核异常信号（SError、Oops、Data Abort）是DUE信号而非SDC信号。内核异常日志应作为核心浓度分析的数据源，而非直接SDC判定依据 |
| **发现4**: 早期FI可准确预测SDC率，DUE率仅为下界（Gem5 FI的SDC率与束流实验在1个数量级内一致） | 鲲鹏新架构部署前可通过Gem5 FI预评估SDC脆弱性，指导测试优先级。FI的DUE下界可用于保守估计 |
| **发现5**: 微架构复杂度影响SDC敏感性（Cortex-A5简单顺序与Cortex-A9复杂乱序具有不同SDC特征） | TaiShan v110 (920) vs TaiShan v200 (930)需差异化诊断。鲲鹏920的诊断规则不能直接应用于930。建议建立鲲鹏代际SDC特征数据库 |

### 9.2 ITHICA核心发现

| 发现 | 诊断启示 |
|------|---------|
| **发现1**: 最隐蔽的缺陷导致不一致错误（同一指令、相同输入、不同执行上下文产生不同输出） | 线程内指令复制+输出比较是高效检测手段。传统"一致错误假设"不必要地限制了检测能力 |
| **发现5**: 指令是否暴露错误取决于执行上下文而非指令使用频率（PC Sensitivity常<1%） | 测试程序选择至关重要——不同程序即使执行相同操作码，检测效果可截然不同。应使用多样化程序 |
| **发现7**: 指令使用压力不能可靠预测哪些测试能检测到有缺陷的服务器（59%案例中检测测试并非执行频率最高者） | 不能基于指令执行频率进行缺陷检测预测或故障指令定位。应使用多样化程序覆盖不同执行上下文 |
| **发现8**: 单指令/基本块测试几乎无法复现缺陷诱导的错误（13/14服务器无法复现） | 短测试阴性结果不能作为硬件健康证据。必须使用长程序或多指令序列测试建立必要执行上下文 |
| **发现10**: 67%向量错误服务器也在其他指令类型上出错（44%被检测服务器在多种指令类型上出现错误） | 不能仅依赖向量测试进行硬件定位。ISA级硬件定位存在固有限制 |

### 9.3 PinDrop核心发现

| 发现 | 操作要点 |
|------|---------|
| **连续测试优于快照测试**: 机器可能在测试数年后才首次失败；稳态每季度0.0024%已测试机器开始新失败 | 必须建立连续测试机制，重访周期≤30天（最优15天）。新部署鲲鹏服务器（尤其930）应提高测试频率 |
| **91.4%测试至少检测到一次失败；31%测试是某台机器唯一失败的测试** | 需要多样化测试集，单一测试不够。不能仅依赖一种测试类型 |
| **62%故障机器仅单物理核心失败；14%有2-9个；24%有≥10个** | 单物理核心故障是最常见模式，但大规模多核故障（24%）不应被忽视 |
| **>71%故障机器持续失败至少2年，失败率保持恒定** | 一旦确认SDC，机器极大概率持续产生错误。FA确认前建议至少2个季度持续测试 |
| **多比特翻转 > 单比特翻转（向量指令中）** | 单比特翻转模型不足以推理SDC。检测算法需考虑多比特翻转模式 |
| **~90%仅影响单个向量元素；无元素位置偏差；无方向偏差** | 故障局部化于特定pipeline阶段。检测算法应针对单元素异常 |
| **新引入指令在首代故障率最高，后续代际显著降低** | 鲲鹏930 SVE2新向量指令应作为最高优先级测试目标。建立跨代际向量指令故障率追踪 |
| **兄弟核共失效（Observation 8）**: 同时出现的两个逻辑核失败绝大多数位于同一物理核心 | 检测到兄弟核同时失败时，应在核心浓度分析中将兄弟核聚合计数 |

### 9.4 对立研究挑战表

ITHICA对先前研究核心结论的挑战：

| 先前研究结论 | ITHICA挑战 | 依据 |
|------------|-----------|------|
| **[SOSP 2023] Alibaba**: 指令使用压力是检测预测因子 | 59%案例中检测测试并非执行频率最高者 | Finding 7 |
| **[SOSP 2023] Alibaba**: 基于指令使用压力进行指令定位 | 执行频率不可靠预测，不能用于定位 | Finding 7 |
| **[ASPLOS 2026] SEVI**: 向量指令错误归因于向量单元 | 67%向量错误服务器也在其他指令类型上出错 | Finding 10 |
| **[ASPLOS 2026] SEVI**: 短测试用于指令定位 | 单指令/基本块测试几乎无法复现错误 | Finding 8 |
| **传统假设**: 缺陷导致一致错误 | 几乎所有缺陷导致不一致错误 | Finding 1 |

---

## 第十章：附录

### 10.1 参考文献

| 论文标题 | 会议 | 核心结论 |
|---------|------|---------|
| Hardware Sentinel: Protecting Software Applications from Hardware Silent Data Corruptions | ASPLOS 2025 | 应用层异常分析（top-down）检测SDC，70% FA复现率 |
| PinDrop: Breaking the Silence on SDCs in a Large-Scale Fleet | HPCA 2026 | 连续测试优于快照测试，500M+测试执行，12年数据 |
| Understanding Silent Data Corruptions in a Large Production CPU Population | SOSP 2023 | 100万+ CPU SDC研究，温度-频率指数关系 |
| Soft Error Effects on Arm Microprocessors: Early Estimations versus Chip Measurements | IEEE TC 2021 | ARM A5/A9双路径验证，SDC仅由CPU核心决定 |
| SEVI: Silent Data Corruption in Vector Instructions | ASPLOS 2026 | 超大规模数据中心向量指令SDC模式 |
| DelayAVF: Architectural Vulnerability Factor for Delay Faults | MICRO 2024 | 延迟故障的架构脆弱性 |
| Orthrus: Low-Overhead Online Computation Validation | SOSP 2025 | 低开销在线计算验证 |
| Harpocrates: Automated Test Program Generation for CPU Faults | ISCA 2024 | 自动化CPU故障测试程序生成 |
| Veritas: Demystifying Silent Data Corruptions | HPCA 2025 | 门级SDC建模+舰队数据 |
| Gem5-MARVEL: Microarchitecture-Level Resilience Analysis of Heterogeneous SoC | HPCA 2024 | 异构SoC弹性分析，支持x86/Arm/RISC-V+加速器 |
| ITHICA: Intra-Thread Instruction Checking Approach for Defect-Induced SDC | arXiv 2026 | 线程内指令检查，不一致错误理论，3000+硬件验证 |
| Cross-ISA SDC Rate Comparison | IEEE 2023 | SDC率跨ISA比较，ARM64独有脆弱点 |
| Differential Fault Injection: Cross-Simulator, Cross-ISA Comparison | IEEE 2023 | 跨模拟器、跨ISA故障注入比较 |
| CHAOS: Controlled Hardware Fault Injector for gem5 | IEEE 2023 | gem5可控硬件故障注入器 |
| Cores that Don't Count | HotOS 2021 | Google SDC报告，mercurial cores |
| Fleetscanner/Ripple | arXiv 2022 | 离线/在线SDC测试方法 |

### 10.2 ARM64异常类代码（EC）速查表

| EC代码 | 异常类型 | SDC相关性 | 权重 |
|--------|---------|-----------|------|
| 0x00 | Undefined Instruction | 17.80x | ★★★★ |
| 0x20 | Instruction Abort from EL1 (PXN) | 20.03x | ★★★★ |
| 0x21 | Instruction Abort from EL0 (UXN) | 20.03x | ★★★★ |
| 0x24 | Data Abort from EL1 | 20.77x (SP-relative) | ★★★★ |
| 0x25 | Data Abort from EL0 | 20.77x (SP-relative) | ★★★★ |
| 0x26 | Alignment Fault | ~1x | ★ |
| 0x2F | SError | — (无有效RAS Record时为SDC候选) | ★★★★ |
| 0x3C | BRK (Breakpoint) | 6.92x | ★★★ |
| — | 嵌套SError / 递归异常 | 59.35x | ★★★★★ |

**ESR_ELx寄存器**：提供详细的异常分类信息，EC位于ESR_ELx[31:26]。

### 10.3 诊断命令速查卡

**数据采集**：
```bash
# Kernel日志
dmesg -T | tail -500
journalctl -k --since "30 days ago" | grep -iE "serror|sea|data.abort|undefined|permission|alignment|brk"

# RAS
cat /sys/devices/system/edac/mc/mc*/ce_count
cat /sys/devices/system/edac/mc/mc*/ue_count
grep -i "serror" /proc/interrupts

# iBMC SEL
ipmitool -H <iBMC_IP> -U <user> -P <pass> sel list

# CPU信息
lscpu | grep -E "Model name|Architecture|CPU\(s\)|Thread|Core|Socket"

# 温度
cat /sys/class/thermal/thermal_zone*/temp

# CPU拓扑
cat /sys/devices/system/cpu/cpu*/topology/core_id
cat /sys/devices/system/cpu/cpu*/cpu_capacity
```

**SDC检测**：
```bash
# 向量跨核对比
for core in 0 1 2 3; do
  taskset -c $core ./neon_stress_test > /tmp/neon_out_$core &
done
wait
diff /tmp/neon_out_0 /tmp/neon_out_1

# PMU监控
perf stat -e armv8_pmuv3_0/sve_inst_retired/,\
armv8_pmuv3_0/sve_inst_spec/,\
armv8_pmuv3_0/br_mis_pred/,\
armv8_pmuv3_0/l1d_cache_refill/,\
armv8_pmuv3_0/cpu_cycles/ -C 0-7 -- sleep 10

# 重启历史
last reboot | head -20
journalctl --list-boots | head -20
```

**核心浓度分析**：
```bash
# 从kernel日志提取异常并按core分组
journalctl -k | grep -iE "data.abort|undefined|serror|permission|alignment|brk" | \
  grep -oP "CPU: \K[0-9]+" | sort | uniq -c | sort -rn

# 识别SMT兄弟核
cat /sys/devices/system/cpu/cpu*/topology/thread_siblings_list
```
