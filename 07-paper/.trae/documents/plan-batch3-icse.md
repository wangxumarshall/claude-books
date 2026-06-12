# Batch 3: ICSE 2026 — 子执行计划

> **For agentic workers**: ICSE 报告当前为简短摘要格式（每篇约 100-200 字 + 核心贡献 + 启示），需全量重构为标准 2 段式 500-800 字格式。约 30 篇论文按主题拆分为 4 个子任务。

**Goal**: 将 icse2026-report.md 中约 30 篇论文从简短摘要重构为标准格式，补充 arXiv/DOI 链接。

**Architecture**: 4 个子任务按 SE 主题分组。ICSE 论文可能不易在 arXiv 找到（部分 IEEE 出版），WebSearch 时也需尝试 ACM/IEEE DL。

**Target File**: `c:\Users\ubuntu\Documents\claude-books\07-paper\icse2026-report.md`

**当前状态**:
- 每篇论文当前为简短摘要格式（100-200字），含核心贡献 + 启示
- 部分论文有量化数据但非 2 段式
- 会议概览（Section 0）已较完善

---

### 子任务 3a: 测试与 Fuzzing (~10 篇)

**Files to modify**: `icse2026-report.md:55-110`

**Papers**: InterFuzz, On Interaction Effects in Greybox Fuzzing, Scaling Security Testing, Attention Distance, LSC-Fuzz, TestWeaver, SAINT, Six Million Fake Stars on GitHub 等

- [ ] **Step 1: 逐篇 WebSearch** — "论文标题 ICSE 2026" (arXiv 或 IEEE Xplore)
- [ ] **Step 2: WebFetch 摘要/Introduction**
- [ ] **Step 3: 重写为 500-800 字标准 2 段式** — SearchReplace
- [ ] **Step 4: 添加来源标注**

---

### 子任务 3b: 程序分析与验证 (~8 篇)

**Files to modify**: `icse2026-report.md:112-148`

**Papers**: Heimdall, HoarePrompt (杰出论文), CodeCureAgent, Dependency-aware Risk Analysis, Argus 等

- [ ] **Step 1-4: 同 3a**

---

### 子任务 3c: AI+SE (~8 篇)

**Files to modify**: `icse2026-report.md:188-281`

**Papers**: USEagent, SEAlign, EmbedAgent, LoopRepair, DebugRepair, DynaFix, EvolRepair, SpecTune, TypeUp, SWE-Bench, Generated Commit Messages, EvoC2Rust, FaultLine, 公平性 等

- [ ] **Step 1-4: 同 3a**

---

### 子任务 3d: 调试与性能 (~4 篇)

**Files to modify**: `icse2026-report.md:150-186`

**Papers**: OScope, R-Log, TAAF, WarpL, LQPR

- [ ] **Step 1-4: 同 3a**
- [ ] **Step 5: 更新 Section 5 结语** — 如有必要

### 子任务完成检查

- [ ] 全部 ~30 篇论文为标准 2 段式 500-800 字格式
- [ ] 全部论文有 `> **信息来源**：` 标注
- [ ] 结语与趋势已更新