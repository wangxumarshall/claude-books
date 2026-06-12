# 学术论文洞察报告全面校正与质量提升 — 主架构计划

> **For agentic workers**: 按 Batch 子计划分别执行。每个 Batch 子计划包含独立的任务清单，可跨对话轮次执行。步骤使用 checkbox (`- [ ]`) 语法追踪。

**Goal**: 将工作区 16 份报告文件中约 400 篇论文的每篇描述丰富到 500-800 字（2段式标准格式），修复元数据缺陷，更新跨分析报告。

**Architecture**: 7 个独立 Batch 按顺序执行。每个 Batch 包含若干子任务（5-15 篇论文），每个子任务是一个独立执行单元。所有子任务遵循统一的论文处理操作流程（SOP）。Batch 7 在全部论文更新完成后执行跨分析一致性更新。

**Tech Stack**: WebSearch + WebFetch (arXiv/会议官网), SearchReplace (更新报告文件), agent-browser (PDF 下载场景)

---

## 总体目标分解

| 优先级 | 目标 | 描述 |
|--------|------|------|
| P0 | 每篇论文描述 500-800 字 | 2 段式标准格式：场景与问题 + 方案与效果 |
| P0 | 每篇论文 3-5 条技术启示 | 覆盖系统软件/Agent/性能工程等方向 |
| P1 | 修复元数据缺陷 | 索引表缺失、"待确认"机构信息、格式不一致 |
| P2 | 更新跨分析报告 | ASPLOS 覆盖数据、EuroSys 覆盖数据、全局一致性 |

## 标准输出格式 (每篇论文)

```markdown
## X.Y 论文标题（英文原标题）

**作者**：第一作者, 通讯作者 等
**机构**：机构全称
**发表信息**：会议/期刊名, 年份

### 技术概要

[第1段：场景与问题 - 500-800字] 描述应用场景背景，指出核心问题和挑战，
分析现有技术方案（1-3个代表性工作）的不足之处。

[第2段：方案与效果] 介绍本文解决方案和关键创新技术（2-4项），
说明核心设计思路和实现效果（量化数据），总结贡献价值。

### 技术线索与启示
- 启示1
- 启示2
- 启示3

> **信息来源**：[arXiv链接 / 会议官网 / 基于摘要信息]
```

## 每篇论文操作 SOP

```
Step 1: WebSearch "论文标题 会议/期刊 2026 arXiv" → 确认 arXiv ID / DOI
Step 2: WebFetch arXiv abstract 页面 → 提取摘要、作者、机构
Step 3: (可选) WebFetch Introduction + Conclusion → 提取场景、问题、方案、效果
Step 4: 撰写 500-800 字技术概要（2段式）
Step 5: 撰写 3-5 条技术启示
Step 6: 验证作者/机构信息（与原文一致）
Step 7: SearchReplace 更新报告文件中的对应章节
```

## 质量红线

- **禁止编造**：无法获取全文时标注 `> **信息来源**：基于摘要信息`
- **准确性 > 完整性**：优先保证已确认信息的准确，不强求覆盖所有细节
- **量化数据优先**：优先引用论文中报告的量化性能数据
- **作者机构一致性**：以论文原文标注为准，不与旧版本冲突

## 文件状态总览

| 文件 | 行数 | 论文数 | 当前描述质量 | 主要问题 |
|------|------|--------|-------------|---------|
| eurosys2026-report.md | 2547 | ~131 | ★★★★☆ 已有详细描述 | 缺少论文索引表(2543行) |
| ppopp2026-report.md | 648 | 51 | ★★☆☆☆ 150-200字 | 全量需丰富至标准格式 |
| icse2026-report.md | 352 | ~30 | ★★☆☆☆ 简短描述 | 全量需丰富至标准格式 |
| hpca2026-report.md | 360 | ~24 | ★★☆☆☆ 简短+点评 | 全量需丰富至标准格式 |
| nsdi2026-report.md | 441 | 22 | ★★★☆☆ 中等描述 | 丰富描述+修复索引表 |
| fast2026-report.md | 472 | 14 | ★★★★☆ 较详细 | 修复2处"待确认" |
| asplos2026-report.md | 358 | 14 | ★★★☆☆ 中等描述 | 丰富现有14篇 |
| tos2026-report.md | 376 | 14 | ★★★★☆ 较详细 | 修复9篇"待确认"机构 |
| tosem2026-report.md | 517 | ~15 | ★★★☆☆ 中等描述 | 丰富描述 |
| tse2026-report.md | 475 | 15 | ★★★☆☆ 中等描述 | 丰富描述 |
| tpds2026-report.md | 395 | 18 | ★★★☆☆ 中等描述 | 丰富描述 |
| tsc2026-report.md | 237 | 12 | ★★★☆☆ 中等描述 | 丰富描述 |
| tocs2026-report.md | 458 | ~10 | ★★★☆☆ 中等描述 | 丰富描述 |
| toplas2026-report.md | 319 | ~10 | ★★★☆☆ 中等描述 | 丰富描述 |
| popl2026-report.md | 287 | 11 | ★★★☆☆ 中等描述 | 丰富描述 |
| 2026-system-cross-analysis.md | 309 | N/A | N/A | 更新ASPLOS/EuroSys覆盖数据 |

## 执行顺序

```
Batch 1 (EuroSys) → Batch 2 (PPoPP) → Batch 3 (ICSE) → Batch 4 (HPCA+NSDI)
  → Batch 5 (FAST+ASPLOS) → Batch 6 (Journal) → Batch 7 (Cross-Analysis)
```

---

## 子计划文件清单

| Batch | 文件 | 说明 |
|-------|------|------|
| Batch 1 | `plan-batch1-eurosys.md` | EuroSys 2026, ~131篇 |
| Batch 2 | `plan-batch2-ppopp.md` | PPoPP 2026, 51篇 |
| Batch 3 | `plan-batch3-icse.md` | ICSE 2026, ~30篇 |
| Batch 4 | `plan-batch4-hpca-nsdi.md` | HPCA + NSDI 2026, ~46篇 |
| Batch 5 | `plan-batch5-fast-asplos.md` | FAST + ASPLOS 2026, 28篇 |
| Batch 6 | `plan-batch6-journals.md` | 7份期刊报告, ~90篇 |
| Batch 7 | `plan-batch7-cross-analysis.md` | 跨分析报告更新 |