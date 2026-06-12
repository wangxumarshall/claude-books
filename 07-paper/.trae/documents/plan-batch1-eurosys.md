# Batch 1: EuroSys 2026 — 子执行计划

> **For agentic workers**: 按子任务 1a→1j 顺序执行。EuroSys 报告已有较好的描述基础（大部分 500+ 字），主要工作是：验证描述字数→补充丰富→修复元数据→生成索引表。步骤使用 checkbox (`- [ ]`) 语法追踪。

**Goal**: 对 eurosys2026-report.md 中全部 ~139 篇论文（约 55 篇待丰富）执行 SOP，确保每篇达到 500-800 字标准格式，并生成完整论文索引表。

**Architecture**: 9 个子任务按论文主题分组执行。每个子任务约 4-16 篇论文，Part 12 因论文数量多且简短拆分为 4 个微批次。

**Target File**: `c:\Users\ubuntu\Documents\claude-books\07-paper\eurosys2026-report.md`

**当前状态**: 
- Part 1-7 (Parts 1-7): 10+10+2+3+11+10+7 = ~63 篇，大部分已有 500-800 字描述，需验证
- Part 8-11: ~19 篇，大部分已有详细描述
- Part 12: 55 篇，部分简短，需重点丰富
- 索引表缺失（第 2543 行需替换）

---

### 子任务 1a: Part 1 LLM Training (16 篇)

**Files to modify**: `eurosys2026-report.md:28-340`

**Papers**:
1. 1.1 MegaScale-MoE — 已有详细描述（~500字），验证并补充 arXiv 链接
2. 1.2 LoRAFusion — 已有详细描述（~500字）
3. 1.3 FLUX (Federated Fine-Tuning MoE LLM) — 已有详细描述
4. 1.4 MegaScale-Data — 已有详细描述
5. 1.5 STAlloc — 已有详细描述
6. 1.6 Zeppelin — 已有详细描述
7. 1.7 Arena — 已有详细描述
8. 1.8 HARP — 已有详细描述
9. 1.9 HetAuto — 已有详细描述
10. 1.10 FlashOverlap — 已有详细描述
11. 1.11 Crimson — 已有详细描述
12. 1.12 Suika — 已有详细描述
13. 1.13 Maya — 已有详细描述
14. 1.14 MegaScale-Omni — 已有详细描述
15. 1.15 ReCCL — 已有详细描述
16. 1.16 Laminar — 已有详细描述

- [ ] **Step 1: 逐篇验证描述字数** — 检查每篇描述是否达到 500-800 字，未达标则标记需丰富
- [ ] **Step 2: 搜索并补充缺失信息** — 对不足 500 字的论文，WebSearch "论文标题 EuroSys 2026 arXiv" → WebFetch 摘要/Introduction → 使用 SearchReplace 更新
- [ ] **Step 3: 验证作者/机构信息** — 对每篇论文，与 arXiv 页面确认作者机构一致性
- [ ] **Step 4: 添加来源标注** — 确保每篇末尾有 `> **信息来源**：` 行

---

### 子任务 1b: Part 2 LLM Inference (16 篇)

**Files to modify**: `eurosys2026-report.md:342-619`

**Papers**: 2.1-2.16 (AdaServe, FlexPipe, TokenFlow, AdaGen, SkyWalker, PiLLM, FineMoE, KUNSERVE, eLLM, MFS, Eevee, SAS, Scaling Test-Time on NPU, TailorLLM, TZ-LLM, PARD)

- [ ] **Step 1: 逐篇验证描述字数** — 检查每篇是否达 500-800 字
- [ ] **Step 2: 搜索补充** — 对不足 500 字的论文搜索并丰富
- [ ] **Step 3: 验证元数据** — 作者/机构/arXiv 链接
- [ ] **Step 4: 添加来源标注**

---

### 子任务 1c: Part 3-4 LLM Apps + Model Serving (5 篇)

**Files to modify**: `eurosys2026-report.md:620-716`

**Papers**: 3.1-3.2 (AIMS, From Imperative to Declarative), 4.1-4.3 (InstGenIE/FlashPS, Automated E2E Model Serving, LLMFolder)

- [ ] **Step 1: 验证描述** — 5 篇论文已有中等长度描述，检查字数
- [ ] **Step 2: 搜索丰富** — 补足未达标论文
- [ ] **Step 3: 验证元数据**
- [ ] **Step 4: 添加来源标注**

---

### 子任务 1d: Part 5 Resource Management & Serverless (11 篇)

**Files to modify**: `eurosys2026-report.md:718-909`

**Papers**: 5.1-5.11 (iRoute, GPU-Centric Data Passing, DROPS, Squeezy, Demystifying Serverless Costs, Fix, Bridging GPU Utilization, Untangling GPU Power, In-Production Characterization, Serverless Replication, NADINO)

- [ ] **Step 1: 验证描述字数** — 11 篇已有详细描述
- [ ] **Step 2: 搜索补充**
- [ ] **Step 3: 验证元数据**
- [ ] **Step 4: 添加来源标注**

---

### 子任务 1e: Part 6 Networking (10 篇)

**Files to modify**: `eurosys2026-report.md:911-1085`

**Papers**: 6.1-6.10 (REPS, Learn-to-Probe, Canopy, Concord, PatternSketch, Solar-NP, Themis, RDMA Connection Sharing, SmartNS, LCMP)

- [ ] **Step 1: 验证描述字数**
- [ ] **Step 2: 搜索补充**
- [ ] **Step 3: 验证元数据**
- [ ] **Step 4: 添加来源标注**

---

### 子任务 1f: Part 7 Storage & File Systems (7 篇)

**Files to modify**: `eurosys2026-report.md:1087-1210`

**Papers**: 7.1-7.7 (SwitchFS, MesaFS, PASS, TCO-driven Storage, ASIC Compression, ColdCode, Omar)

- [ ] **Step 1: 验证描述字数**
- [ ] **Step 2: 搜索补充**
- [ ] **Step 3: 验证元数据**
- [ ] **Step 4: 添加来源标注**

---

### 子任务 1g: Part 8-9 Security + OS & Virtualization (10 篇)

**Files to modify**: `eurosys2026-report.md:1212-1398`

**Papers**: 8.1-8.4 (SKernel, Pyramid, TrustWeave, Formal Methods Huawei), 9.1-9.6 (CofferOS, Wayfinder, NecoFuzz, x86-64 Emulation on RISC-V, VM Live Migration, Chimera)

- [ ] **Step 1: 验证描述字数**
- [ ] **Step 2: 搜索补充**
- [ ] **Step 3: 验证元数据**
- [ ] **Step 4: 添加来源标注**

---

### 子任务 1h: Part 10-11 Distributed Systems + Heterogeneous (9 篇)

**Files to modify**: `eurosys2026-report.md:1394-1556`

**Papers**: 10.1-10.5 (OptiLog, Ethane, DAG-based BFT SMR, ECCB, Fuzzing Enterprise Blockchain), 11.1-11.4 (Proteus, NutCracker, CHARM, RoPeerTo)

- [ ] **Step 1: 验证描述字数**
- [ ] **Step 2: 搜索补充**
- [ ] **Step 3: 验证元数据**
- [ ] **Step 4: 添加来源标注**

---

### 子任务 1i: Part 12 Embedded/IoT/Edge/Other (55 篇)

**Files to modify**: `eurosys2026-report.md:1560-2455`

这部分论文数量最多且描述普遍简短，拆分为 4 个微批次：

#### 微批次 1i-1: 12.1-12.14 (14 篇)

- [ ] **Step 1: 逐篇搜索** — WebSearch "论文标题 EuroSys 2026 arXiv"
- [ ] **Step 2: WebFetch 摘要** — 提取场景/问题/方案/效果
- [ ] **Step 3: 重写为 500-800 字标准格式** — SearchReplace 更新
- [ ] **Step 4: 添加来源标注** — 每篇标注 arXiv 链接或"基于摘要信息"

#### 微批次 1i-2: 12.15-12.28 (14 篇)

- [ ] **Step 1-4: 同 1i-1**

#### 微批次 1i-3: 12.29-12.41 (13 篇)

- [ ] **Step 1-4: 同 1i-1**

#### 微批次 1i-4: 12.42-12.55 (14 篇)

- [ ] **Step 1-4: 同 1i-1**

---

### 子任务 1j: 生成完整论文索引表

**Files to modify**: `eurosys2026-report.md:2541-2547`

- [ ] **Step 1: 收集所有论文元数据** — 从全文提取每篇论文的编号、标题、作者、机构、分类
- [ ] **Step 2: 生成索引表** — 使用 SearchReplace 替换第 2541-2547 行（当前占位文本 + 说明）
  - 替换为以 Part 分组的完整索引表，每行包含：序号 | 论文标题 | 第一作者 | 机构 | Part分类
- [ ] **Step 3: 验证表完整性** — 确保索引表覆盖全部 ~139 篇论文，编号与章节一致

---

### 子任务完成检查

- [ ] 全部 ~139 篇论文描述 ≥ 500 字
- [ ] 全部论文有 `> **信息来源**：` 标注
- [ ] 全部论文作者/机构已与 arXiv 验证
- [ ] 完整论文索引表已替换第 2541-2547 行
- [ ] 无 "待确认" 信息残留