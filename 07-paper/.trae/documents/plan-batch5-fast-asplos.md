# Batch 5: FAST 2026 + ASPLOS 2026 — 子执行计划

> **For agentic workers**: FAST 报告已有较详细描述，主要修复元数据缺陷。ASPLOS 报告 14 篇中等描述需丰富。两个报告独立处理。

**Goal**: (1) FAST 14篇检查扩充 + 修复 2 处"待确认"；(2) ASPLOS 14篇丰富至 500-800 字标准格式。

**Architecture**: FAST 3 个子任务、ASPLOS 3 个子任务。

**Target Files**:
- `c:\Users\ubuntu\Documents\claude-books\07-paper\fast2026-report.md`
- `c:\Users\ubuntu\Documents\claude-books\07-paper\asplos2026-report.md`

---

## Part A: FAST 2026 (14 篇)

**当前状态**: 已有较好描述（大部分 400-600 字），2 处"待确认"需修复。

### 子任务 5a1: 文件系统 + AI+Storage (6 篇)

**Files to modify**: `fast2026-report.md:50-~250`

**Papers**: 
- Section 1 (文件系统): SYSSPEC (Best Paper), CoFS, RubikFS — 3 篇
- Section 2 (AI+Storage): Tutti, SolidAttention, GCR — 3 篇

- [ ] **Step 1: 检查每篇字数** — 确认 ≥ 500 字
- [ ] **Step 2: 修复"待确认"** — WebSearch "论文标题 FAST 2026" 确认 CoFS 机构信息（第257行）
- [ ] **Step 3: 扩充不足 500 字的论文** — SearchReplace
- [ ] **Step 4: 补充来源标注** — 标注 arXiv 链接或"基于公开信息"

### 子任务 5a2: 云存储 + 键值存储 (6 篇)

**Files to modify**: `fast2026-report.md:~250-~400`

**Papers**: PolarStore, 阿里云本地存储, CloudTS, Grouped I/O, 以及其他云存储/键值存储论文

- [ ] **Step 1: 检查并扩充**
- [ ] **Step 4: 补充来源标注**

### 子任务 5a3: 其余 + 修复索引表 (2 篇)

**Files to modify**: `fast2026-report.md:~400-472`

- [ ] **Step 1: 修复索引表第 466 行 "待确认"** — 确认 CloudTS 作者/机构信息
- [ ] **Step 2: 补充剩余论文**

---

## Part B: ASPLOS 2026 (14 篇)

**当前状态**: 14 篇已有中等描述（~200-400 字），部分带点评。已有论文索引表（333行）。

### 子任务 5b1: 体系结构 + LLM/ML (8 篇)

**Files to modify**: `asplos2026-report.md:35-168`

**Papers**:
- Section 1 (体系结构): ISAMORE (Best Paper), PF-LLM (Best Paper), DARTH-PUM, CounterPoint, ASDR — 5 篇
- Section 2 (LLM/ML): SNIP, CREATE, RedFuser, SpecSA — 4 篇 (与 Section 1 合并)

- [ ] **Step 1: 逐篇 WebSearch + WebFetch** — "论文标题 ASPLOS 2026 arXiv"
- [ ] **Step 2: 丰富至 500-800 字标准 2 段式** — SearchReplace
- [ ] **Step 3: 添加来源标注**

### 子任务 5b2: OS + 编译 + 安全 (6 篇)

**Files to modify**: `asplos2026-report.md:168-261`

**Papers**:
- Section 3 (OS/虚拟化): LAIKA, Nemo — 2 篇
- Section 4 (编译/PL): LPO, MLIR Stencil — 2 篇
- Section 5 (安全): Maverick, AMD SEV-SNP 破解 — 2 篇

- [ ] **Step 1-3: 同 5b1**

### 子任务 5b3: 存储网络 + 结语 (2+ 篇)

**Files to modify**: `asplos2026-report.md:263-358`

**Papers**: Section 6 (存储/网络): Nemo (备注:已覆盖), Zebra — 2 篇

- [ ] **Step 1-3: 同 5b1**
- [ ] **Step 4: 更新 Section 7 结语与趋势**
- [ ] **Step 5: 更新论文索引表** — 确保与丰富后的论文数据一致
- [ ] **Step 6: 更新跨分析中 ASPLOS 状态** — (在 Batch 7 中执行)

### 子任务完成检查

- [ ] FAST: 全部 14 篇论文 ≥ 500 字，0 "待确认"残留
- [ ] ASPLOS: 全部 14 篇论文为标准 2 段式 500-800 字
- [ ] 两报告全部论文有来源标注