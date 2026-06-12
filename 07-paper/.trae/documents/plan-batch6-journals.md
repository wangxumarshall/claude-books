# Batch 6: 期刊报告 (7 份文件, ~90 篇) — 子执行计划

> **For agentic workers**: 7 份期刊报告分别处理，每份独立。TOS 报告额外需要修复 9 处"待确认"机构信息。各期刊报告格式各异，需分别适配标准格式。

**Goal**: 将 7 份期刊报告中约 90 篇论文丰富至 500-800 字标准格式，修复元数据缺陷。

**Architecture**: 7 个子任务对应 7 个期刊，每个期刊独立执行。

---

### 子任务 6a: TOS 2026 (14 篇) — 修复 + 丰富

**Target File**: `c:\Users\ubuntu\Documents\claude-books\07-paper\tos2026-report.md`

**当前状态**: 描述较详细（大部分 400-600 字），但 9 处机构为"待确认"。

- [ ] **Step 1: 修复 9 处"待确认"机构** — WebSearch 逐篇确认作者机构
  - 位置：第 117, 138, 183, 204, 225, 248, 269, 290, 311 行
- [ ] **Step 2: 检查每篇字数** — 确认 ≥ 500 字
- [ ] **Step 3: 扩充不足论文**
- [ ] **Step 4: 补充来源标注**

---

### 子任务 6b: TOSEM 2026 (~15 篇)

**Target File**: `c:\Users\ubuntu\Documents\claude-books\07-paper\tosem2026-report.md`

**当前状态**: 中等描述（~200-400 字），517 行。

- [ ] **Step 1: 逐篇搜索** — WebSearch + WebFetch
- [ ] **Step 2: 重写为标准 2 段式 500-800 字** — SearchReplace
- [ ] **Step 3: 添加来源标注**

---

### 子任务 6c: TSE 2026 (15 篇)

**Target File**: `c:\Users\ubuntu\Documents\claude-books\07-paper\tse2026-report.md`

**当前状态**: 中等描述，475 行。

- [ ] **Step 1-3: 同 6b**

---

### 子任务 6d: TPDS 2026 (18 篇)

**Target File**: `c:\Users\ubuntu\Documents\claude-books\07-paper\tpds2026-report.md`

**当前状态**: 中等描述，395 行。

- [ ] **Step 1-3: 同 6b**

---

### 子任务 6e: TSC 2026 (12 篇)

**Target File**: `c:\Users\ubuntu\Documents\claude-books\07-paper\tsc2026-report.md`

**当前状态**: 中等描述，237 行（最短）。

- [ ] **Step 1-3: 同 6b**

---

### 子任务 6f: TOCS 2026 (~10 篇)

**Target File**: `c:\Users\ubuntu\Documents\claude-books\07-paper\tocs2026-report.md`

**当前状态**: 中等描述，458 行。

- [ ] **Step 1-3: 同 6b**

---

### 子任务 6g: TOPLAS 2026 + POPL 2026 (21 篇)

**Target Files**:
- `c:\Users\ubuntu\Documents\claude-books\07-paper\toplas2026-report.md` (~10 篇, 319 行)
- `c:\Users\ubuntu\Documents\claude-books\07-paper\popl2026-report.md` (11 篇, 287 行)

- [ ] **Step 1: TOPLAS ~10 篇** — 搜索 + 丰富
- [ ] **Step 2: POPL 11 篇** — 搜索 + 丰富
- [ ] **Step 3: 添加来源标注**

### 子任务完成检查

- [ ] 7 份期刊报告全部论文为标准 2 段式 500-800 字
- [ ] TOS 0 处"待确认"机构残留
- [ ] 全部论文有来源标注