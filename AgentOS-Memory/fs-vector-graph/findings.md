# Findings

## High-Signal Findings

### 2026-04-16
- 现有 `report.md` 已具备较成熟的主线：研究范围、主导接口、证据等级、问题总览、机制总览和 CortexMem 混合架构判断都可保留。
- `report_v2.md` 的价值在于补充了更细的架构拆解与源代码级机制说明，但篇幅偏长、重复较多，适合提炼机制与子类型，不适合整段复用。
- `report_v3.md` 对“为什么会分化成 filesystem-like 与 vector/graph-like”阐述更扎实，也更强调 benchmark 不能滥排总榜，适合做主结构基础。
- `report_v4.md` 是高层摘要版，表述更贴近用户要求中的四个模块：关键问题、机制原理、关键场景、对 CortexMem 的启示；适合用于压缩和收束。
- `sources.md` 与 `evidence-matrix.md` 已经给出较稳定的证据边界：`memsearch`、`Acontext`、`Memoria`、`lossless-claw` 支撑 filesystem-like 主线；`mem0`、`Honcho`、`Graphiti`、`eion`、`mem9`、`ContextLoom` 支撑 vector/graph-like 主线。
- 现有材料已经明确一个核心判断：行业趋势不是“文件系统 vs 向量库”二选一，而是“文件真相层 + 语义索引/图关系 + 治理层”的混合架构。
- 截至 `2026-04-16`，公开 benchmark 前沿比旧稿更碎片化，`Hindsight`、`Mem0`、`Honcho` 等官方页面都在给出高分信号；这进一步说明 SOTA 只能按问题切片理解，不能写成单一冠军榜。
- 重写后的主报告采用了更贴近用户要求的五段结构：研究边界、关键问题与 SOTA、核心机制、关键场景、CortexMem 启示，并保留了附录用于解释 benchmark 的正确读法。

## Rewrite Principles
- 保留强结论，压缩重复案例堆叠。
- 把“已解决问题”和“待解决问题”并置呈现，避免报告只写优点。
- 在 SOTA 一节里明确区分“论文结果”“官方研究页自报”“README 工程信号”。
- CortexMem 启示部分聚焦可执行方向：程序性记忆、分层递归检索、trace、治理、遗忘。
