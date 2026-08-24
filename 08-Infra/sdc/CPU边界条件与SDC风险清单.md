# CPU 边界条件与 SDC（静默数据损坏）风险清单

> 面向芯片设计与制造视角：除乱序执行 + 寄存器重命名、load-use 前递之外，
> 还有哪些 CPU 边界条件可能导致 SDC，以及芯片厂商如何预检。

---

## 一、一个统一的判据：什么样的边界条件才会"静默"

乱序执行+寄存器重命名、load-use前递这两个例子本质属于同一类。SDC故障是三个条件同时成立：

1. **激活稀有** —— 该路径的 toggle 率极低（长逻辑锥、罕见操作数组合、罕见状态交叉），ATPG 向量和功能仿真都难覆盖；
2. **检错真空** —— 结果路径上没有 parity / ECC / residue / 重放校验，出错后无人喊叫；
3. **余量脆弱** —— 该路径本身贴近 setup/hold 边界，或所在电路对 V/T/老化敏感。

厂商的"预检"分别攻击这三条。
---

## 二、执行单元与数据通路（最经典的"数据相关型" SDC）

Meta 论文里著名的 `Int(1.1^53) = 0` 就是纯数据相关缺陷——同一个核上 `1.1^52` 正确、`1.1^53` 错误，说明失效落在浮点单元一条特定的长路径上。

| 边界条件 | 为什么危险 |
|---|---|
| **加法器进位链全传播**（`0xFFFF...F + 1`） | 前缀树（Kogge-Stone / Ladner-Fischer）最长路径，只有全 propagate 的操作数才激活 |
| **乘法器 Booth 编码 + Wallace/Dadda 压缩树最坏部分积** | 压缩树深度最大的操作数组合极其罕见 |
| **除法/开方 SRT 商位选择重叠区** | Pentium FDIV 的现代变体；商位查找表在重叠区边界的选择错误 |
| **FMA 对阶移位器 + sticky 位 OR 树** | 指数差极端（如 ±2^k 附近）时移位量最大，sticky 归约树是超长组合路径 |
| **LZA（前导零预测）与实际 LZC 的 ±1 修正路径** | 修正路径只在特定尾数模式激活 |
| **单次舍入（single rounding）与 tie-to-even 边界** | 恰好落在半个 ULP 上的操作数 |
| **非规格化数 / FP assist 微码路径** | 极少执行，验证覆盖率天然低 |
| **FP→INT 饱和、NaN 传播、-0 / ±Inf 边界** | 特殊值路径与主路径共用旁路 |
| **向量跨 lane 操作**：reduction、permute/shuffle crossbar、gather/scatter 部分完成、SVE predicate tail | lane 间 skew + crossbar 长走线；tail 元素掩码是罕见状态 |
| **矩阵/AI 单元的累加链与低精度格式**（BF16/FP8 的次正规、累加顺序） | 累加树深、又常常无任何校验 |

**厂商预检手段**：数据通路专用 corner-operand 向量库、随机指令生成器（RIS）对参考模型逐条比对、把这些向量嵌进 SLT 并在 Vmin/Fmax shmoo 上跑。设计侧的对策是 **residue check（模 3 / 模 15 余数校验）** 加在乘加单元上——这是把"检错真空"堵上的最有效手段。

---

## 三、访存与一致性（与 load-use 前递同族，风险最高的一片）

- **Store-to-load forwarding 的部分重叠**：store 8B / load 4B 偏移、非对齐、跨 cache line、**跨 4K 页的地址别名**（只比较低 12 位时的假匹配）。字节使能的合并逻辑是典型的稀有激活 + 无校验。
- **内存消歧预测器（memory dependence predictor）误预测恢复**：预测器说"无依赖"而实际有依赖时的 flush/replay 窗口。
- **推测唤醒 + L1 miss 的 replay 取消窗口**：调度器假设 L1 命中提前唤醒消费者，miss 后要在极窄窗口内取消；取消信号漏一拍就是错数据被消费。replay storm 场景下这个窗口被反复压榨。
- **LSQ / ROB / free list 同时满、以及指针回绕（wrap-around）**：多个队列同时到达满/空是罕见状态交叉。
- **原子操作**：跨 cache line 的 unaligned atomic、ARM LSE 的 CAS/SWP 与 LL/SC exclusive monitor 的竞态、monitor 被 snoop 清除的边界。
- **一致性协议竞态**：snoop 与 eviction 同拍到达、silent eviction、部分行数据转发、写回与 probe 交叉、独占权获取与 store buffer drain 的顺序。
- **TLB / 页表**：ARM 的 **break-before-make** 违例、`TLBI` + `DSB` 完成边界、**ASID/VMID 回绕**、page table walker 对 A/D 位的原子更新与并发 walker 的竞态、以及硬件 walker 与推测 walk 的中止路径。
- **自修改 / 跨修改代码（SMC/XMC）** 的 I-cache 一致性窗口。
- **预取器**：越界预取污染、与 device memory / 非缓存区域的交互。
- **内存序屏障**：弱序模型下 store buffer drain 与 barrier 完成的握手边界（这类更多是设计 bug，但同样完全静默）。

---

## 四、没有检错覆盖的存储与关联结构

这是"检错真空"的重灾区。要点是**清点哪些结构裸奔**：

- **寄存器堆**：同周期同地址读写的 write-through 旁路、多端口写冲突仲裁。很多设计的 RF 只有 parity 甚至没有。
- **SRAM 位单元级**：half-select 干扰、write recovery 不足、read disturb、bitcell Vmin 分布尾部。
- **CAM 类结构的 multi-hit**：TLB、STLF 比较网络、snoop filter、BTB。wired-OR 输出在多匹配时给出的是"或"出来的垃圾值，且通常无检测。
- **典型裸奔清单**：调度器 wakeup 矩阵、旁路/转发网络、rename map 与 free list、store buffer 数据体、fill buffer、write-combining buffer。

**预检**：MBIST（March C- / March SS 等算法）+ 冗余修复、SRAM Vmin/retention shmoo，以及设计侧给关键 CAM 加 parity、给 RF 加 parity + replay。

---

## 五、时序与电气边界（"厂商预检"最核心的对象）

- **Hold / min-delay 违例**：最阴险的一类。它**与频率无关**，降频不缓解，也不会因降载消失，因此表现为长期低概率静默错误。而且 FinFET 工艺存在**温度反转**，低温反而更快，最坏角在低温高压，很多厂商的老测试流程角覆盖不全。
- **半周期路径 / 时钟 duty cycle 失真**：高频下对占空比敏感的路径。
- **CDC 亚稳态**：core ↔ uncore ↔ mesh ↔ 内存控制器之间的异步桥、同步器 MTBF 余量、异步 FIFO 格雷码指针在满/空边界的跨位翻转。
- **复位 recovery/removal 与时钟门控使能窄脉冲**：唤醒后第一拍的 glitch。
- **di/dt 与电压跌落谐振**：从 idle 突然进入全宽 SIMD/矩阵满载是最坏用例；一阶（die，ns 级）、二阶（package，~50–150 MHz）、三阶（board，~1 MHz）三个 droop。厂商用 power virus + adaptive / droop-detector 校准 + per-core Vmin shmoo 来预检。
- **DVFS / 频率许可切换窗口**：PLL relock、glitch-free clock mux 切换、电压与频率握手的顺序。
- **电源门控进出**：retention 电压保持余量（Vret shmoo）、隔离单元使能时序、上电浪涌导致邻域 droop、core online/offline 时的状态恢复。
- **IR drop 热点**：sign-off 用的向量与真实 workload 功耗分布不匹配，导致某些 workload 下局部压降超预期。
- **老化（BTI / HCI / EM）**：出厂 pass、部署 6–18 个月后 fail，这正是 SDC 在现役机群里"突然出现"的主要机理。

---

## 六、制造缺陷侧：为什么是"静默"而不是"崩溃"

半导体业界数据：数据中心 CPU 的 SDE 率大致在 **100–1000 PPM** 量级，且主因是**制造缺陷而非设计缺陷**。

- **弱开路（resistive open）/ 桥接（bridging）** → 表现为 small delay defect，只在特定跳变方向 + 特定温度下才超时。
- **FinFET 多鳍中单鳍缺陷** → 参数化行为，随测试条件漂移。
- **IDDQ 在先进工艺基本失效**（漏电本底太高），传统 stuck-at 覆盖率高但抓不到延迟型缺陷。

**预检手段的递进链**：

```
stuck-at ATPG
  → transition delay fault (TDF)
    → cell-aware / bridging ATPG
      → small delay defect / path-delay
        → MBIST + LBIST
          → 多角 Vmin / Fmax / 温度 shmoo
            → burn-in / HTOL
              → SLT（系统级测试，40–60 分钟功能向量，温压控制比客户环境更严）
                → 现场周期性扫描
```

现场扫描是过去几年最重要的补充：Intel 的 **In-Field Scan (IFS / SAF)** 把扫描测试内容像微码一样以固件包分发（`/lib/firmware/intel/ifs_<n>/`），由驱动同步核内所有线程后写 `ACTIVATE_SCAN` MSR 触发，单次最长约 200 ms，期间该核所有线程离线。它明确定位为"检测 parity 和 ECC 抓不到的问题"。ARM 阵营有对应的 in-field BIST / functional safety scan IP，鲲鹏平台上等价能力通常由 BMC + 厂商诊断工具承载。

**已知覆盖缺口**（这点在 SLT 讨论里被反复强调）：

- 功能向量无法做故障分级——你没法说"我启动了 OS，因此覆盖了哪些故障模型"；
- SLT 需要的随机性与测试时间预算直接冲突；
- 这类缺陷**跨测试轮次可重复性很低**。

这就是为什么筛完仍有漏网。

---

## 七、容易被忽略的系统 / 接口层

- **Chiplet D2D 链路**（UCIe / 厂商私有 IFOP）：训练余量随温度漂移、重训练窗口，以及 CRC 覆盖的盲区（有 CRC 一般不静默，但重训练边界和 lane 修复切换瞬间是缺口）。
- **DDR 子系统**：读写训练余量随温度/老化漂移、refresh 与 ZQ 校准边界、**DRAM on-die ECC 的多比特盲区**（ODECC 会把 2-bit 错"洗"成看似正常的数据）、Row Hammer。
- **PCIe / CXL**：未启用 ECRC 时端到端存在静默通路；CXL.mem 的 poison 传播策略。
- **微码 / patch RAM 更新窗口**、性能计数器与调试逻辑对功能路径的耦合。

---

## 八、落到 ARM64 / 鲲鹏场景的排查优先级

如果目标是"哪些边界最值得针对性构造探测负载"，建议顺序：

| 优先级 | 目标 | 可行性 |
|---|---|---|
| 1 | **FP/向量数据通路 corner operand**（FMA 极端指数差、SRT 除法边界、NEON/SVE 跨 lane reduction） | 数据相关、纯静默、易构造自校验 |
| 2 | **STLF 部分重叠 + 4K 别名 + 非对齐跨行** | 用户态可构造 |
| 3 | **原子与 exclusive monitor 竞态**（LSE CAS/SWP 高并发） | 用户态可构造 |
| 4 | **TLB break-before-make / ASID 回绕** | 需内核态 |
| 5 | **di/dt：idle → 全宽 SIMD 突变的 Vmin 边缘**，配合温度扫描（勿忘低温角，因温度反转） | 需控 V/F/T |
| 6 | **裸奔结构的 Vmin shmoo**（RF、STLF CAM、调度器唤醒阵列） | 需厂商侧或 BMC 调压能力 |

前四项用"双跑比对 + 参考模型"即可在现役机器上做；后两项通常只能在厂商侧或有 BMC 调压能力的平台上做。

---

## 参考资料

- [Silent Data Corruptions at Scale (Dixit et al., Meta)](https://arxiv.org/pdf/2102.11245)
- [Why Silent Data Errors Are So Hard To Find — Semiconductor Engineering](https://semiengineering.com/why-silent-data-errors-are-so-hard-to-find/)
- [In-Field Scan — The Linux Kernel documentation](https://docs.kernel.org/arch/x86/ifs.html)
- [Revisiting CPU Silent Data Corruptions in Modern Datacenters — CACM](https://cacm.acm.org/research/revisiting-cpu-silent-data-corruptions-in-modern-datacenters/)
- [Silent Data Corruptions: Microarchitectural Perspectives — IEEE TC](https://dl.acm.org/doi/abs/10.1109/TC.2023.3285094)
- [Understanding Silent Data Corruption in Processors for Mitigating its Effects — ACM TACO](https://dl.acm.org/doi/10.1145/3690825)
