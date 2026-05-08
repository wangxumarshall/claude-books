Psi和 [Pi](https://pi.dev?utm_source=chatgpt.com) 的理念，其实是高度同源的。

甚至可以说：

> 你现在收敛后的“薄 Runtime”方向，本质上已经非常接近 Pi 的核心哲学了。

但两者仍有几个关键差异。

我下面会从：

1. Pi 到底是什么
2. 它真正的架构哲学
3. 它和你方案的重合点
4. 它对你的核心借鉴
5. 它不适合你的地方
6. 最关键的启发

六部分展开。

---

# 一、Pi 到底是什么

Pi 不是传统意义上的：

* Agent Platform
* Workflow Engine
* Multi-Agent System
* DAG 编排框架

它本质上是：

> 一个“极简 Agent Harness”。

官方自己强调：

> “There are many agent harnesses, but this one is yours.” ([Pi][1])

核心思想：

```text id="q98c2x"
不要构建复杂 agent 系统
而是给模型一个最小执行环境
```

这是 Pi 最重要的东西。

---

# 二、Pi 的真正哲学（非常重要）

Pi 的核心哲学其实只有三条：

---

## 1. 模型优先，而不是 Harness 优先

Pi 认为：

```text id="z8cfu2"
随着模型增强
大部分 harness complexity 都会变成负资产
```

所以它极度反对：

* 复杂 Planner
* DAG workflow
* 固定 agent role
* 巨型 tool abstraction
* 大量 orchestration

---

## 2. Tool 越少越好

Pi 最著名的是：

```text id="h4x9g8"
只有四个核心工具：

read
write
edit
bash
```

([LLM Reference][2])

甚至：

* 不做 grep
* 不做 git tool
* 不做 search tool

原因是：

> 模型已经被 RL 在 bash 上训练过。

这是一个非常 radical 的观点。 ([Reddit][3])

---

## 3. Harness 必须“可生长”

Pi 不内建很多功能。

而是：

```text id="9nxzic"
让 agent 自己生成 extension
```

包括：

* subagent
* status bar
* workflow
* UI

都不是核心内建。

而是：

```text id="oxts2x"
agent 自己写 extension
```

这点极其关键。 ([Reddit][3])

---

# 三、Pi 与你方案的吻合度

我认为：

```text id="0d0w6q"
理念吻合度：90%
架构吻合度：70%
```

---

# 四、和你方案最重合的地方

---

# 1. “Loop-first” 完全一致

你现在的核心：

```text id="qjvx7s"
ExecutionLoop
```

而 Pi 的核心也是：

```text id="uz74h4"
极简 loop
```

Pi 本质上就是：

```text id="a2lzxq"
state
→ think
→ tool call
→ observation
→ continue
```

这和你现在的：

```text id="r6eh5f"
ReadState
→ DecideNextAction
→ CallTool
→ Observe
→ UpdateState
```

几乎一致。

---

# 2. “薄壳” 完全一致

Pi 明确反对：

* 大 orchestration
* 大 workflow
* 重型 planner
* 大 control plane

这和你现在的：

```text id="v8n8lp"
只保留：
Task
Loop
Tool
State
```

几乎完全一致。

---

# 3. “Tool-native” 完全一致

Pi 的核心：

```text id="0q6k6x"
everything is tool
```

甚至：

```text id="xw6k1n"
bash is enough
```

你现在的：

```text id="w6v6p2"
ToolRegistry
```

和 Pi 的方向高度一致。

---

# 4. “让模型自己长能力” 完全一致

这是你和 Pi 最接近的地方。

你现在的理念：

```text id="tjlwmf"
不要提前做复杂系统
让模型以后自然长出来
```

而 Pi：

甚至已经在实践：

```text id="rm7i4e"
让 agent 自己生成 extension
```

([Reddit][3])

这是高度一致的。

---

# 五、Pi 对你最大的借鉴（核心）

这里才是真正重要的。

---

# 借鉴 1：系统应该“小到能被模型理解”

这是 Pi 最厉害的地方。

Pi 的整个系统：

```text id="zmx8h4"
小到模型自己能理解自己的 runtime
```

这非常关键。

很多 Agent 平台的问题：

```text id="w7qcdh"
系统复杂度已经超过模型理解能力
```

导致：

* agent 不知道 runtime 怎么工作
* tool semantics 太复杂
* orchestration 太复杂
* hidden state 太多

而 Pi：

```text id="8gq9r3"
runtime complexity 极低
```

所以模型：

* 更稳定
* 更容易 self-debug
* 更容易 self-extension

---

# 借鉴 2：不要过早抽象

Pi 非常克制。

它几乎不做：

* planner abstraction
* orchestration abstraction
* agent hierarchy abstraction

这是非常值得你学的。

因为很多 Agent Framework：

死于：

```text id="msdyx8"
过早抽象
```

---

# 借鉴 3：让“extension”成为核心，而不是 feature

这是 Pi 最先进的地方之一。

Pi 本质上：

不是：

```text id="2o8ljo"
build features
```

而是：

```text id="y8quhu"
build extension surface
```

这意味着：

未来：

* subagents
* workflows
* memory
* UI
* dashboards

都可以：

```text id="7lmjlwm"
后生长
```

而不是：

```text id="g9bz0x"
内建
```

这和你“薄 runtime”方向极其一致。

---

# 六、Pi 不适合你的地方

这里也很重要。

---

# 1. Pi 太“coding-centric”

Pi 本质还是：

```text id="u6jjlwm"
coding harness
```

它的：

* read
* write
* edit
* bash

本质都围绕：

```text id="md8n1g"
code workspace
```

而你未来想做的是：

```text id="lzjlwm"
general task runtime
```

包括：

* computer use
* browser
* desktop
* real-world workflows

所以：

你不能完全照搬 Pi。

---

# 2. Pi 的状态层其实偏弱

Pi 目前：

* 更偏 session
* 更偏 conversational state
* replay/recovery 不算特别强

而你现在强调：

```text id="jjlwmf"
durable execution
```

这是你比 Pi 更进一步的地方。

---

# 3. Pi 对长期 runtime 还不够重视

Pi 更像：

```text id="0mjlwm"
interactive coding session
```

而不是：

```text id="yjlwmr"
long-running execution runtime
```

你未来如果真做：

* async execution
* long-running tasks
* resumable agents

你会更接近：

```text id="3jlwm7"
Temporal + Agent
```

而不仅是 Pi。

---

# 七、最关键结论（非常重要）

你现在这个方向：

其实已经非常接近：

```text id="jlwm6f"
Pi 的下一阶段
```

也就是：

> “把 Pi 从 coding harness，推进到 general execution runtime。”

---

# Pi 真正验证了什么？

Pi 最重要的不是功能。

而是它证明了：

> 强模型 + 极小 runtime
> 真的可以工作。

([Agentlas][4])

这是整个 Agent 行业非常关键的一个方向。

---

# 八、你现在最该借鉴 Pi 的部分（最终建议）

如果你继续推进你的 Minimal Runtime：

我最建议你直接借鉴 Pi 的：

---

## （1）极小核心

真正做到：

```text id="aqjlwm"
Loop
Tool
State
```

就够。

---

## （2）Tool 极简主义

不要搞：

* 50 个工具
* 复杂 tool taxonomy
* 巨型 capability graph

Pi 已经证明：

```text id="jlwmjt"
4 tools 都能非常强
```

---

## （3）系统可被模型理解

这是最重要的。

你未来所有设计都应该问：

> “模型自己能理解这个 runtime 吗？”

如果不能：

那系统已经太复杂了。

---

# 九、一句话总结

Pi 和你方案最本质的共同点是：

> 都认为未来 Agent 的核心不是“更复杂的 orchestration”，而是“更薄、更通用、更可生长的执行 runtime”。

[1]: https://pi.dev/?utm_source=chatgpt.com "Pi Coding Agent"
[2]: https://www.llmreference.com/agent/pi?utm_source=chatgpt.com "Pi (Pi Harness) — CLI for AI Coding | LLMReference"
[3]: https://www.reddit.com/r/Agent_AI/comments/1t62mu2/i_tried_pi_opensource_coding_agent_after_watching/?utm_source=chatgpt.com "I tried Pi open-source coding agent after watching Mario Zechner's talk"
[4]: https://agentlas.pro/frameworks/pi/?utm_source=chatgpt.com "Pi (The Framework Behind OpenClaw) — AI Agent Framework Review 2026 | Agentlas"

