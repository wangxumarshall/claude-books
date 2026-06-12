# Batch 2: PPoPP 2026 — 子执行计划

> **For agentic workers**: PPoPP 报告当前为 150-200 字的简短描述 + 技术启示格式，需全量重构为标准 2 段式 500-800 字格式。51 篇论文按主题拆分为 6 个子任务。

**Goal**: 将 ppopp2026-report.md 中全部 51 篇论文从简短描述重构为标准 2 段式 500-800 字格式，补充 arXiv 链接和来源标注。

**Architecture**: 6 个子任务按用户指定主题分组执行。51 篇论文每篇都需 WebSearch + WebFetch + 重写。

**Target File**: `c:\Users\ubuntu\Documents\claude-books\07-paper\ppopp2026-report.md`

**当前状态**:
- 每篇论文当前为 150-200 字简短描述 + 3-4 条技术启示
- 已有论文全索引（Section 12:634行），但可能需更新
- 格式非标准 2 段式，需全量重构
- 已有会议概览和趋势方向章节

---

### 子任务 2a: 并发控制与内存管理 (4+4=8 篇)

**Files to modify**: `ppopp2026-report.md:41-154`

**Papers**:
- Section 1 (并发控制): Binary Compatible Critical Section Delegation (Best Paper), SCOT, Hapax Locks, Multiverse — 4 篇
- Section 2 (任务调度): Rethinking Thread Scheduling, Waste-Efficient Work Stealing, 图搜索负载均衡, SpMV负载均衡 — 4 篇

- [ ] **Step 1: 逐篇 WebSearch** — "论文标题 PPoPP 2026 arXiv"
- [ ] **Step 2: WebFetch 摘要/Introduction** — 提取场景/问题/方案/效果
- [ ] **Step 3: 重写为 500-800 字标准格式** — 使用 SearchReplace 逐篇更新
- [ ] **Step 4: 添加来源标注**

---

### 子任务 2b: GPU 计算与稀疏矩阵 (10 篇)

**Files to modify**: `ppopp2026-report.md:155-270`

**Papers**: Section 3 (并发数据结构, 4篇) + Section 4 (GPU计算, 6篇)

- [ ] **Step 1-4: 同 2a**

---

### 子任务 2c: LLM 训练 (8 篇)

**Files to modify**: `ppopp2026-report.md:271-392`

**Papers**: Section 5 (混合精度与量化, 4篇) + Section 6 (集群与云计算, ~4篇) + Section 7 (ML训练分布式优化, 约8篇, 取前部分)

- [ ] **Step 1-4: 同 2a**

---

### 子任务 2d: LLM 推理 (8 篇)

**Files to modify**: `ppopp2026-report.md:393-547`

**Papers**: Section 8 (并行算法) + Section 9 (ML推理与Transformer优化)

- [ ] **Step 1-4: 同 2a**

---

### 子任务 2e: 分布式 + 科学计算 (10 篇)

**Files to modify**: `ppopp2026-report.md:548-633`

**Papers**: Section 10 (线性代数与矩阵计算) + Section 11 (研究趋势, 含补充论文)

- [ ] **Step 1-4: 同 2a**

---

### 子任务 2f: 其余论文 + 索引表更新 (11 篇)

**Files to modify**: `ppopp2026-report.md:634-648`

- [ ] **Step 1: 补充剩余未覆盖论文**
- [ ] **Step 2: 更新 Section 12 论文全索引表** — 确保与重写后的论文元数据一致
- [ ] **Step 3: 更新 Section 13 报告总结** — 如有必要

### 子任务完成检查

- [ ] 全部 51 篇论文为标准 2 段式 500-800 字格式
- [ ] 全部论文有 `> **信息来源**：` 标注
- [ ] 论文全索引表已更新
- [ ] 无旧格式残留