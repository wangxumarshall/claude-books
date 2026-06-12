# Batch 4: HPCA 2026 + NSDI 2026 — 子执行计划

> **For agentic workers**: HPCA 报告 (~24 篇) 和 NSDI 报告 (22 篇) 并行处理。HPCA 当前为简短点评格式（约 150 字 + 点评），NSDI 当前为中等描述格式。NSDI 还需修复索引表格式（添加作者列、展开机构缩写）。

**Goal**: (1) HPCA 24篇全量丰富到标准格式；(2) NSDI 22篇丰富描述 + 修复索引表。

**Architecture**: 2 个报告独立处理，HPCA 5 个子任务、NSDI 3 个子任务。

**Target Files**: 
- `c:\Users\ubuntu\Documents\claude-books\07-paper\hpca2026-report.md`
- `c:\Users\ubuntu\Documents\claude-books\07-paper\nsdi2026-report.md`

---

## Part A: HPCA 2026 (~24 篇)

**当前状态**: 每篇为简短点评格式，含摘要式描述（~100-150字）+ 点评段落。需全量重构。

### 子任务 4a1: AI/ML 加速器 (5 篇)

**Files to modify**: `hpca2026-report.md:25-92`

**Papers**: FractalCloud, LOCALUT, AUM, PASCAL, The Cost of Dynamic Reasoning

- [ ] **Step 1: 逐篇 WebSearch + WebFetch** — "论文标题 HPCA 2026 arXiv"
- [ ] **Step 2: 重写为 500-800 字标准 2 段式** — SearchReplace
- [ ] **Step 3: 添加来源标注**

### 子任务 4a2: 量子 + GPU 安全 (5 篇)

**Files to modify**: `hpca2026-report.md:94-143`

**Papers**: HERO-Sign, GPU+FPGA异构, Athena, I-POP, RoMe

- [ ] **Step 1-3: 同 4a1**

### 子任务 4a3: PIM + HBM + Chiplet (6 篇)

**Files to modify**: `hpca2026-report.md:145-233`

**Papers**: PIM-malloc, Conduit, Domain-Specific ECC, ChipLight 等

- [ ] **Step 1-3: 同 4a1**

### 子任务 4a4: 量子计算 (4 篇)

**Files to modify**: `hpca2026-report.md:235-273`

- [ ] **Step 1-3: 同 4a1**

### 子任务 4a5: 其余 + 趋势章节 (4 篇)

**Files to modify**: `hpca2026-report.md:275-360`

- [ ] **Step 1-3: 同 4a1**
- [ ] **Step 4: 更新趋势章节** — 如有新发现

---

## Part B: NSDI 2026 (22 篇)

**当前状态**: 已有中等长度描述（~200-400字），格式较规范，但需扩充至 500-800 字。索引表（Section 7）需添加作者列并展开机构缩写。

### 子任务 4b1: 数据中心网络 + 部分 AI/ML (10 篇)

**Files to modify**: `nsdi2026-report.md:49-175`

**Papers**: OSCAR (Outstanding Paper), HEDGE, 以及 Section 2 中约 7 篇 AI/ML 论文

- [ ] **Step 1: 逐篇 WebSearch + WebFetch** — "论文标题 NSDI 2026" (arXiv/USENIX)
- [ ] **Step 2: 扩充描述至 500-800 字** — SearchReplace 更新
- [ ] **Step 3: 添加来源标注**

### 子任务 4b2: 剩余 AI/ML + RDMA + 视频 (12 篇)

**Files to modify**: `nsdi2026-report.md:175-310`

- [ ] **Step 1-3: 同 4b1**

### 子任务 4b3: 修复索引表 + 其余章节

**Files to modify**: `nsdi2026-report.md:311-441`

- [ ] **Step 1: 修复 Section 7 索引表** — 添加作者列、展开机构缩写
- [ ] **Step 2: 扩充网络验证/诊断/安全章节论文** (~8篇)
- [ ] **Step 3: 更新 Section 8 结语**

### 子任务完成检查

- [ ] HPCA: 全部 ~24 篇论文为标准 2 段式 500-800 字
- [ ] NSDI: 全部 22 篇论文为标准 2 段式 500-800 字
- [ ] NSDI: 索引表已添加作者列、机构缩写已展开
- [ ] 两报告全部论文有来源标注