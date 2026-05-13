# 《Psi - Minimal Agent Runtime》架构设计文档
> Intelligence-amplifying runtime for continuous agents
## 1. 文档信息

| 字段   | 内容                                    |
| ---- | ------------------------------------- |
| 文档名称 | Minimal Agent Runtime Architecture    |
| 文档版本 | v0.1                                  |
| 文档类型 | 架构设计文档                                |
| 系统定位 | 极简任务执行型 Agent Runtime                 |
| 核心目标 | 持续执行、可恢复、可审计、薄壳演进                     |
| 适用范围 | 软件开发、自动化运维、跨应用任务执行、桌面/网页操作            |
| 设计风格 | Loop-first / Thin-shell / Tool-native |

---

## 2. 背景与问题定义

当前许多 Agent 系统存在一个共性问题：系统层做得过厚，过早将模型能力不足固化为复杂编排、固定角色、重型审批与大而全的工作流。短期看，这些设计能提升稳定性；长期看，它们会成为模型能力增强后的结构性负担。

本方案希望解决的，不是“如何把 Agent 做得更像一个平台”，而是：

> **如何构建一个足够薄、足够稳定、足够可恢复的执行内核，让模型在其中持续完成真实任务。**

该内核的核心职责只有一件事：
**把“目标”转化为可持续推进的执行过程。**

---

## 3. 系统目标

### 3.1 核心目标

系统必须支持以下能力：

1. **持续执行**：任务不是单轮问答，而是多步推进的执行过程。
2. **可恢复**：任务可中断、可恢复、可重试。
3. **可审计**：所有关键动作都能追溯。
4. **工具原生**：真实能力通过统一工具接口暴露。
5. **薄壳演进**：模型能力增强后，系统不需要重构，只需更换模型或减少控制逻辑。

### 3.2 设计意图

本系统不是 Agent OS，也不是复杂 workflow 平台，而是一个：

> **以循环执行为核心的最小任务运行时。**

---

## 4. 设计原则

### 4.1 薄壳优先

系统只保留模型当前无法稳定替代的底座能力。
不把“今天模型还不够强”写进产品结构里。

必须保留的底座包括：

* 任务表达
* 执行循环
* 工具调用
* 状态持久化
* 最小安全边界
* 日志审计

### 4.2 单主链路

所有任务统一走一条链路：

```text
TaskSpec → ExecutionLoop → Tool Call → Observation → State Update → Loop
```

不为不同场景设计多套执行框架。

### 4.3 结构化优先

关键数据必须结构化：

* 任务定义
* 执行状态
* 工具调用
* 观测结果
* 验收结果

自然语言可用于解释，但不能作为系统状态本身。

### 4.4 可恢复、可回放、可追责

* 任一步失败都能恢复
* 任一次执行都能回放
* 任一个高风险动作都能追溯

---

## 5. 方案总览

系统仅保留 4 个核心模块，加 1 个最小安全边界：

```text
TaskSpec
   ↓
ExecutionLoop
   ↓
ToolRegistry
   ↓
StateStore / Log
   ↓
Minimal Safety Gate
```

### 5.1 TaskSpec

定义任务目标、约束、验收标准和能力边界。

### 5.2 ExecutionLoop

负责推进任务执行，驱动模型决策，调用工具，更新状态。

### 5.3 ToolRegistry

负责统一暴露外部能力。

### 5.4 StateStore / Log

负责状态持久化、checkpoint、轨迹记录和回放。

### 5.5 Minimal Safety Gate

只拦截真正危险的动作，不做复杂审批链。

---

## 6. 模块设计

---

### 6.1 TaskSpec

#### 6.1.1 定义

`TaskSpec` 是系统唯一任务入口。

#### 6.1.2 职责

* 表达用户目标
* 描述任务约束
* 定义验收标准
* 标记风险等级
* 声明可用能力

#### 6.1.3 数据结构

```json
{
  "task_id": "string",
  "title": "string",
  "goal": "string",
  "constraints": ["string"],
  "acceptance_criteria": ["string"],
  "risk_level": "low | medium | high",
  "available_capabilities": ["code", "browser", "computer_use", "filesystem", "api"],
  "context_refs": ["string"],
  "deadline": "string"
}
```

#### 6.1.4 设计要求

* 任务必须可验证
* 风险等级必须显式声明
* 不允许将自由文本直接作为执行依据

---

### 6.2 ExecutionLoop

#### 6.2.1 定义

`ExecutionLoop` 是系统核心运行时。

#### 6.2.2 职责

* 读取当前状态
* 触发模型决策
* 调用工具
* 接收观测结果
* 更新状态
* 决定继续、暂停、重试或结束

#### 6.2.3 标准循环

```text
ReadState
→ DecideNextAction
→ CallTool
→ ObserveResult
→ UpdateState
→ Continue / Stop / Replan
```

#### 6.2.4 必须支持的能力

* 单步执行
* checkpoint
* resume
* retry
* timeout
* 人工插入
* 轻量 replan

#### 6.2.5 最小状态结构

```json
{
  "task_id": "string",
  "execution_id": "string",
  "status": "running | paused | failed | completed",
  "current_step": "string",
  "checkpoint_id": "string",
  "last_observation": {},
  "pending_actions": [],
  "retry_count": 0
}
```

#### 6.2.6 设计要求

* Loop 内不放复杂业务逻辑
* 状态变更必须落盘
* 执行过程必须可回放

---

### 6.3 ToolRegistry

#### 6.3.1 定义

`ToolRegistry` 是系统连接外部世界的统一接口。

#### 6.3.2 职责

* 工具注册
* 能力描述
* 输入输出 schema 定义
* 权限标记
* 副作用标记
* 统一调用入口

#### 6.3.3 Tool Descriptor

```json
{
  "tool_id": "string",
  "name": "string",
  "category": "code | browser | computer_use | filesystem | api",
  "input_schema": {},
  "output_schema": {},
  "permission_level": "read | write | admin",
  "side_effect_level": "none | low | medium | high",
  "rollback_supported": true
}
```

#### 6.3.4 设计要求

* 工具必须先注册再使用
* 工具调用必须可审计
* 高风险动作必须经过安全检查

---

### 6.4 StateStore / Log

#### 6.4.1 定义

StateStore 保存当前状态，Log 保存执行轨迹。

#### 6.4.2 职责

* 保存 checkpoint
* 保存执行状态
* 保存工具调用记录
* 保存观测结果
* 支持回放与复盘

#### 6.4.3 日志结构

```json
{
  "execution_id": "string",
  "step_id": "string",
  "timestamp": "string",
  "action": {},
  "observation": {},
  "state_delta": {},
  "errors": [],
  "artifacts": []
}
```

#### 6.4.4 设计要求

* append-only
* 每一步都可回放
* 支持后续评测与优化
* 不丢弃失败轨迹

---

### 6.5 Minimal Safety Gate

#### 6.5.1 定义

`Minimal Safety Gate` 是系统最小安全边界。

#### 6.5.2 职责

* 拦截高风险动作
* 控制权限边界
* 处理人工确认
* 执行最小安全策略

#### 6.5.3 拦截对象

* 越权访问
* 不可逆破坏动作
* 高风险写操作
* 超额资源消耗
* 违反显式约束的动作

#### 6.5.4 决策结果

```json
{
  "request_id": "string",
  "risk_level": "low | medium | high",
  "decision": "allow | deny | require_human_approval",
  "reason": "string"
}
```

#### 6.5.5 设计要求

* 只挡底线，不挡正常执行
* 规则少而硬
* 不把安全层做成新的编排层

---

## 7. 执行数据流

### 7.1 主流程

```text
TaskSpec
→ ExecutionLoop
→ ToolRegistry
→ Observation
→ StateStore
→ ExecutionLoop
```

### 7.2 任务开始流程

1. 用户提交 `TaskSpec`
2. 系统生成 `execution_id`
3. 初始化状态
4. 进入首轮 Loop

### 7.3 单轮循环流程

1. 读取当前状态
2. 模型决定下一步动作
3. 先过 Safety Gate
4. 再调用工具
5. 收集 Observation
6. 写入 Log
7. 更新 State
8. 决定是否继续

### 7.4 结束条件

* 达成验收标准
* 用户显式终止
* 不可恢复错误
* 人工接管终止

---

## 8. computer use 处理方式

computer use 不作为单独平台能力建设，而是 ToolRegistry 中的一类工具。

### 8.1 最小原语

* click
* type
* scroll
* hotkey
* open
* save
* screenshot
* read_ui

### 8.2 设计原则

* 每个动作都有反馈
* 每次动作都有记录
* 出错可重试
* 高风险操作可拦截

### 8.3 目标

先把原语打通，再让模型在 loop 中自然决定何时调用。

---

## 9. 设计阶段与并行能力的处理方式

本方案不将其作为独立平台模块建设，而是作为 Loop 内的自然行为。

### 9.1 设计阶段

模型在执行前可先输出一个轻量 `Plan`，例如：

```json
{
  "goal": "...",
  "approach": "...",
  "steps": ["..."],
  "risks": ["..."]
}
```

该结构仅作为中间状态，不作为独立设计系统。

### 9.2 并行能力

仅支持“子任务触发子 loop”，不建设中心化调度平台。

```text
主 Loop
→ 发现可并行子任务
→ 启动子 Loop
→ 子 Loop 独立执行
→ 汇总结果
```

这样可以保留并行能力，同时避免系统变厚。

---

## 10. 接口定义

### 10.1 TaskSpec 接口

```json
{
  "task_id": "string",
  "title": "string",
  "goal": "string",
  "constraints": ["string"],
  "acceptance_criteria": ["string"],
  "risk_level": "low | medium | high",
  "available_capabilities": ["code", "browser", "computer_use", "filesystem", "api"],
  "context_refs": ["string"],
  "deadline": "string"
}
```

### 10.2 ExecutionState 接口

```json
{
  "task_id": "string",
  "execution_id": "string",
  "status": "running | paused | failed | completed",
  "current_step": "string",
  "checkpoint_id": "string",
  "last_observation": {},
  "pending_actions": [],
  "retry_count": 0
}
```

### 10.3 Tool Descriptor 接口

```json
{
  "tool_id": "string",
  "name": "string",
  "category": "code | browser | computer_use | filesystem | api",
  "input_schema": {},
  "output_schema": {},
  "permission_level": "read | write | admin",
  "side_effect_level": "none | low | medium | high",
  "rollback_supported": true
}
```

### 10.4 Observation 接口

```json
{
  "execution_id": "string",
  "step_id": "string",
  "timestamp": "string",
  "action": {},
  "observation": {},
  "state_delta": {},
  "errors": [],
  "artifacts": []
}
```

### 10.5 Safety Decision 接口

```json
{
  "request_id": "string",
  "risk_level": "low | medium | high",
  "decision": "allow | deny | require_human_approval",
  "reason": "string"
}
```

---

## 11. MVP 范围

### 11.1 必做

* TaskSpec
* ExecutionLoop
* ToolRegistry
* StateStore / Log
* Minimal Safety Gate
* 最小 computer use 工具集
* checkpoint / resume

### 11.2 暂不做

* 复杂 Planner
* 独立 Orchestrator
* 重型多 Agent 中控
* 完整设计平台
* 学习闭环系统
* 复杂审批工作流

---

## 12. 里程碑计划

### Phase 0：最小内核

目标：打通执行底座。

交付物：

* TaskSpec
* StateStore
* Log
* ToolRegistry
* Safety Gate

验收标准：

* 任务可进入统一结构
* 工具可统一调用
* 所有操作可记录

---

### Phase 1：单 Loop 跑通

目标：形成持续执行闭环。

交付物：

* ExecutionLoop
* checkpoint / resume
* retry
* timeout

验收标准：

* 任务可多步执行
* 中断可恢复
* 错误可重试

---

### Phase 2：接入 computer use

目标：操作真实界面。

交付物：

* 基础 UI 动作
* screenshot
* read_ui
* 失败回退

验收标准：

* 能完成简单跨应用任务
* 每次动作都有反馈

---

### Phase 3：轻量并行

目标：支持子任务子 loop。

交付物：

* 子任务触发机制
* 子 loop 执行
* 简单结果汇总

验收标准：

* 能并行处理可拆任务
* 不引入重型调度系统

---

## 13. 非目标

本方案明确不做以下事情：

* 不做完整 Agent OS
* 不做复杂 DAG 编排平台
* 不做重型多 Agent 管控中心
* 不做固定角色体系
* 不做大而全设计平台
* 不做过早学习系统

原因是：这些能力会把系统做厚，背离“模型变强后系统变薄”的方向。

---

## 14. 风险与对策

### 风险 1：系统逐渐变厚

**对策**：坚持只保留最小控制面、最小状态面和最小工具面。

### 风险 2：模型能力提升后系统反而束缚模型

**对策**：把策略与执行解耦，把能力描述写成 schema，不写死流程。

### 风险 3：computer use 不稳定

**对策**：动作回执、截图反馈、失败重试、人工接管。

### 风险 4：状态与日志量增长过快

**对策**：append-only + 分层归档 + checkpoint 精简。

---

## 15. 最终定义

本系统不是 AI 编程工具，也不是完整 Agent 平台，而是：

> **一个以 Loop 为核心、以 Tool 为边界、以 State 为记忆、以 Safety 为底线的极简任务执行内核。**

其本质是：

* 给模型一个最小但完整的行动环境
* 让模型从“回答问题”转向“持续完成任务”
* 让系统随着模型变强而自动变薄，而不是越来越重

---

如果你愿意，我下一步可以直接把这份文档继续补成研发团队更常用的版本，拆成三份：

1. **架构设计图 + 模块职责图**
2. **接口定义（JSON Schema / TypeScript Interface）**
3. **MVP 研发排期与任务拆解**

