# 第8章：四维案例矩阵 —— 工程实践全景

> **核心理念**：LLM作为概率性文本生成函数，其产出质量高度依赖于外部Harness架构的质量。本章通过四个真实案例，揭示Harness成熟度与自动化程度之间的因果关系。

## 案例矩阵概览

| 案例 | 规模 | Harness特点 | 核心数据 | 来源评级 |
|------|------|------------|---------|---------|
| **OpenAI Codex** | 100万行代码 | 仓库即知识 | 0行人类代码 | B |
| **Stripe Minions** | 1300 PR/周（⚠️待核实） | Blueprint混合编排 | ~500工具（⚠️待核实） | B（⚠️待核实） |
| **Cursor** | 1000 commits/时 | 递归Planner-Worker | — | B |
| **Anthropic** | 16 Agent并行 | Git任务锁 + GCC Oracle | $20K成本 | B |

## OpenAI Codex团队案例

> 来源：openai.com/index/harness-engineering/，**B级**

| 指标 | 数据 |
|------|------|
| 代码量 | 100万行 |
| PR数量 | 1500个 |
| 人类代码 | 0行 |
| 时间 | 5个月 |
| 团队规模 | 3人 → 7人 |
| 工程师人均产出 | 每天3.5个PR |
| 估算效率提升 | 10倍（vs传统方式） |

**核心理念**：
- "仓库是Agent唯一的知识来源"——代码、markdown、schema、可执行计划全都版本化存在仓库
- "代码要对Agent可读，不是对人类可读"——Application Legibility
- "渐进式自主性提升"——从简单任务开始，逐步提升Agent权限
- "合并哲学"——审查，而非修改；发现需要大量修改→反思Harness哪里出错

## Stripe Minions案例

> 来源：stripe.dev/blog/minions，**B级**（⚠️原URL返回404，待核实）

| 指标 | 数据 |
|------|------|
| 每周PR数 | 1300+（⚠️待核实） |
| Agent类型 | 无人值守，完全自主 |
| 架构 | Blueprint编排（确定性+Agentic节点混合） |
| 工具数量 | ~500个MCP工具（⚠️待核实），每个Agent仅见筛选子集 |
| CI限制 | 最多两轮，第一轮失败→自动修复再跑，还失败→转交人类 |

**关键洞察**：

> "成功取决于可靠的开发者环境、测试基础设施和反馈循环，跟模型选择关系不大。"

**Blueprint模式**：确定性节点（配置、模板）+ Agentic节点（AI决策）的混合编排。

## Cursor Self-Driving案例

> 来源：cursor.com/blog/self-driving-codebases，**C级**

| 指标 | 数据 |
|------|------|
| 每小时commit | ~1000个 |
| 一周工具调用 | 1000万+次 |
| 演进路径 | 单Agent → 多Agent共享状态（锁竞争）→ 角色分工（过载）→ 递归Planner-Worker模型 |

**递归Planner-Worker模型**：
1. Planner Agent：分解任务
2. Worker Agent：执行具体工作
3. 递归：Worker内部可再包含Planner

**关键洞察**：单一模型在超大规模下遇到瓶颈，递归结构是解决方案。

## Anthropic 16 Agent案例

> 来源：anthropic.com/engineering/building-c-compiler，**B级**

| 指标 | 数据 |
|------|------|
| Agent数量 | 16个Claude Opus 4.6并行 |
| 代码行数 | ~100,000行Rust |
| 成本 | ~$20,000 |
| 会话数 | 近2,000次 |
| Token消耗 | 2B输入 + 140M输出 |
| 目标 | 编译Linux 6.9 (x86/ARM/RISC-V) |
| GCC torture test通过率 | 99% |

**关键教训**：

| 教训 | Harness意义 | 对应不变量 |
|------|-------------|-----------|
| "Write extremely high-quality tests" | 测试即验证 | 状态不变量 |
| "Context window pollution" | 上下文管理 | 需DAG状态架构 |
| "Time blindness" | 死循环检测 | TNR强制干预 |
| Git-backed任务锁 | 任务分区 | 并行安全 |

**方法论**：

```bash
# Agent循环：简单的bash while true循环
while true; do
  COMMIT=$(git rev-parse --short=6 HEAD)
  claude -p "$(cat AGENT_PROMPT.md)" --model claude-opus-X-Y &> "agent_${COMMIT}.log"
done
```

## 四案例的统一视角

| 维度 | OpenAI | Stripe | Cursor | Anthropic |
|------|--------|--------|--------|-----------|
| Harness成熟度 | 最高 | 高 | 中 | 高 |
| 人类介入 | 仅审查 | 仅CI失败 | 仅Prompt | 任务分配 |
| 核心机制 | 仓库即知识 | Blueprint | Planner-Worker | 任务锁 |
| 适用规模 | 巨型 | 中型 | 中型 | 巨型 |
| 类型不变量 | ✅ TypeScript | ✅ TypeScript | ✅ TypeScript | ✅ Rust |
| 状态不变量 | ✅ Git | ✅ Blueprint | ✅ Planner-Worker | ✅ 任务锁 |
| 执行不变量 | ✅ 容器 | ✅ 沙箱 | ✅ 本地 | ✅ Docker |

## 本书框架与替代方案对比

| 维度 | 本书（Harness不变量） | LangChain | AutoGen | CrewAI |
|------|---------------------|-----------|---------|--------|
| **理论深度** | 公理+引理+定理体系 | 无形式化理论 | 无形式化理论 | 无形式化理论 |
| **类型不变量** | TypeScript+Zod+Rust类型系统 | 弱类型检查 | 动态Python | 动态Python |
| **状态不变量** | 状态机+DAG持久化 | LangGraph状态 | 会话状态 | Task状态 |
| **执行不变量** | WASM沙箱+能力导向安全 | 无物理隔离 | 无物理隔离 | 无物理隔离 |
| **TNR支持** | 完整Undo Stack实现 | 无 | 无 | 无 |
| **编译器集成** | 编译时验证+死循环检测 | 无 | 无 | 无 |
| **适用场景** | 企业级高可靠性系统 | 快速原型 | 多Agent对话 | 流程编排 |

**本书的独特贡献**：

1. **形式化理论体系**：唯一提供公理-引理-定理结构的AI Harness理论
2. **三层不变量完备性证明**：类型+状态+执行不变量缺一不可
3. **TNR不可能性定理**：诚实声明开放世界假设下的理论边界
4. **GRT栈工程实践**：Go+Rust+TypeScript的完整多语言架构

## 本章小结

1. OpenAI：100万行代码，0行人类手写，仓库即知识
2. Stripe：1300 PR/周，Blueprint混合编排，与模型选择无关
3. Cursor：1000 commits/时，递归Planner-Worker模型
4. Anthropic：16 Agent并行，Git任务锁，$20K成本
5. 共同特点： Harness成熟度决定自动化程度