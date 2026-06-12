# Batch 7: 跨分析报告更新 + 全局一致性检查

> **For agentic workers**: 在全部 6 个 Batch 完成后执行。更新跨分析报告中的过时数据，执行全局一致性检查。

**Goal**: 更新 `2026-system-cross-analysis.md` 中的 ASPLOS 和 EuroSys 覆盖数据，执行全局一致性检查。

**Architecture**: 2 个子任务，一次性完成。

**Target File**: `c:\Users\ubuntu\Documents\claude-books\07-paper\2026-system-cross-analysis.md`

---

### 子任务 7a: 更新跨分析报告数据

**Files to modify**: `2026-system-cross-analysis.md`

- [ ] **Step 1: 更新 ASPLOS 状态** — 将第 23 行 `数据暂缺` 替换为 `已覆盖 14/152 篇`
  - 当前: `ASPLOS 2026 | 数据暂缺`
  - 更新为: `ASPLOS 2026 | 14篇详细解读（含2篇Best Paper）`

- [ ] **Step 2: 更新 EuroSys 覆盖数据** — 将第 23 行 `6篇代表性论文深度解读` 替换为 `~139篇全量解读`
  - 当前: `EuroSys | 6篇代表性论文深度解读`
  - 更新为: `EuroSys | ~139篇全量解读（Spring+Fall双周期）`

- [ ] **Step 3: 更新 Attention Notice** — 更新第 7 行的 ASPLOS 警告:
  - 当前: `ASPLOS 2026 的详细论文洞察报告暂未完成`
  - 如果 ASPLOS 报告已更新，移除或减弱此警告

- [ ] **Step 4: 验证交叉覆盖章节** — 确认 Section 2.3（交叉覆盖对比）中的论文引用与更新后的各报告一致

---

### 子任务 7b: 全局一致性检查

- [ ] **Step 1: 索引表检查** — 验证 EuroSys/PPoPP/ASPLOS 的索引表覆盖全部论文
- [ ] **Step 2: 格式一致性** — 抽查各报告论文格式是否统一（2段式、作者标注、来源标注）
- [ ] **Step 3: "待确认"清零** — 全工作区搜索 `待确认`，确保已全部修复
- [ ] **Step 4: 数据一致性** — 验证跨分析报告中引用的论文数据与源报告一致
- [ ] **Step 5: 来源标注完整性** — 抽查各报告论文末尾是否有 `> **信息来源**：` 行

```bash
# 搜索残留的"待确认"
grep -rn "待确认" c:\Users\ubuntu\Documents\claude-books\07-paper\*.md

# 检查来源标注覆盖
grep -c "信息来源" c:\Users\ubuntu\Documents\claude-books\07-paper\*.md
```

### 子任务完成检查

- [ ] 跨分析报告中 ASPLOS 数据已更新（不为"数据暂缺"）
- [ ] 跨分析报告中 EuroSys 覆盖数据已更新（不为"6篇"）
- [ ] 全工作区 0 处"待确认"残留
- [ ] 索引表与论文章节编号一致