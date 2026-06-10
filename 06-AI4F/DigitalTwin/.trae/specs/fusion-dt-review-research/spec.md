# 核聚变数字孪生前沿深度研究 — 评审、修正与补充 Spec

## Why
现有核聚变装置数字孪生技术方案研究报告已基于2025年以来的公开信息完成初稿（12章，约15,000+字），但存在以下待改进项：部分引用为推测性描述（"可能""极有可能"），缺少2026年6月最新发展动态，部分章节数据密度不足，以及与日本、韩国、欧盟等非美国地区最新进展的覆盖缺口。需通过全面网络实证研究（WebSearch/WebFetch/agent-browser）对报告进行系统性评审、修正和补充。

## What Changes
- 评审现有报告（中文版 + 英文版），标注问题点：
  - 推测性表述需替换为实证引用或标注为分析判断
  - 事实错误需修正
  - 数据缺失需补充
- 通过 WebSearch 和 WebFetch 进行全面的聚变数字孪生前沿研究，覆盖：
  - Thea Energy / Helios 最新进展（2026年6月后）
  - CFS / SPARC 最新进展（2026年6月后）
  - DIII-D 数字孪生最新进展
  - NVIDIA 聚变数字孪生产品更新
  - Synopsys/Ansys 2026 R1/R2 聚变相关功能
  - ITER AI 与数字孪生进展
  - UKAEA STEP 最新动态
  - 日本（LHD, JT-60SA）、韩国（KSTAR）、欧盟（W7-X）数字孪生相关进展
  - 惯性约束聚变（NIF, Xcimer, Marvel Fusion 等）数字孪生
  - 聚变数字孪生相关的学术论文（arXiv, Nature, Nuclear Fusion, IEEE TPS）
  - 国际原子能机构（IAEA）聚变数字孪生倡议
  - DOE 创世纪使命 / 里程碑计划最新进展
  - 聚变数字孪生标准与认证（ISO, ASME, 新增标准）
  - 聚变AI初创公司最新融资与进展
- 基于研究成果修正报告：
  - 修正事实错误
  - 替换推测性表述
  - 补充新发现的数据和引用
  - 更新参考资料列表
  - 覆盖非美国地区进展
- 输出修正后的完整报告（中文版 + 英文版）

## Impact
- Affected specs: 核聚变数字孪生技术方案体系深度研究（12章）
- Affected code: `fusion-digital-twin-research-report-part1.md`, `fusion-digital-twin-research-report-part2.md`, `核聚变装置数字孪生技术方案体系深度研究.md`
- New files: 修正版报告文件

## ADDED Requirements

### Requirement: 报告质量评审
系统 SHALL 对现有报告全文进行逐章评审，标注所有需要修正的问题点。
- 推测性表述（"可能""极有可能""基于推测"等）
- 事实性错误
- 数据缺失位置
- 格式不一致

### Requirement: 前沿网络实证研究
系统 SHALL 通过 WebSearch 和 WebFetch 对聚变数字孪生的全领域进行最新信息采集，覆盖：
- 美国（Thea Energy, CFS, GA, ANL, PPPL, LLNL）
- 欧洲（UKAEA, ITER, W7-X, Renaissance Fusion）
- 亚洲（LHD/日本, KSTAR/韩国, 中国聚变数字孪生）
- 全球学术论文（arXiv, Nature, NF, IEEE TPS）
- 行业报告与融资动态
- 标准与政策进展

### Requirement: 报告修正
基于网络实证研究结果，系统 SHALL 修正报告中的所有已标注问题，并补充新的技术数据和引用引用。

### Requirement: 最终质量验证
修正后的报告 SHALL 满足：
- 每章引用 ≥ 5 个独立来源
- 推测性表述全部替换或明确标注
- 所有URL可访问
- 覆盖美国/欧洲/亚洲三大区域
- 参考资料 ≥ 30 条