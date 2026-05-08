# 五大 AI Agent 平台横向对比总结

> 本报告对 **OpenAI Agents SDK + Codex**、**Claude Managed Agents**、**Google Gemini Enterprise Agent Platform**、**AWS Bedrock AgentCore**、**Kimi Swarm** 进行系统性横向对比。

---

## 一、平台定位光谱

```
轻量框架 ◄──────────────────────────────────────────► 全栈平台

OpenAI SDK   Kimi Swarm   Claude Managed   AWS AgentCore   Google Platform
(框架层)     (模型层)      (运行时层)        (基础设施层)      (全生命周期)
   │            │              │                │                │
 "Express.js" "超级引擎"   "Agent OS"      "Agent Lambda"   "Agent GCP"
```

---

## 二、一句话核心价值

| 平台 | 一句话核心价值 |
|------|---------------|
| **OpenAI Agents SDK** | 用最简API（Agent+Handoff+Guardrail+Tracing）让开发者10分钟构建可观测的多Agent工作流，provider-agnostic设计消除vendor lock-in——**多Agent编排的Express.js** |
| **Claude Managed Agents** | 通过Brain-Hands-Session三层解耦将Agent运行时完全托管，开发者只定义逻辑不管基础设施——**Agent的操作系统层** |
| **Google Gemini Platform** | ADK（开源）+Agent Engine（托管）+A2A（互操作）全栈覆盖，内建Sequential/Parallel/Loop编排原语+Workspace集成——**Agent时代的GCP** |
| **AWS Bedrock AgentCore** | 框架无关的五模块Agent基础设施（Runtime+Memory+Gateway+Identity+Observability），让任何Agent获得AWS级安全——**Agent的Lambda** |
| **Kimi Swarm** | PARL训练将编排能力植入模型权重，实现300+子Agent并行4000+步骤、3-4.5x加速——**模型即编排器** |

---

## 三、11维度多维对比矩阵

### 维度0：核心架构与设计哲学

| 维度 | OpenAI SDK | Claude Managed | Google Platform | AWS AgentCore | Kimi Swarm |
|------|-----------|----------------|-----------------|---------------|------------|
| **定位** | 轻量SDK | 托管运行时 | 全栈平台 | 基础设施服务 | 模型能力 |
| **开源** | ✅ MIT | ❌ 托管 | ✅ ADK (Apache) | ❌ 托管 | ✅ 模型权重 |
| **Provider-Agnostic** | ✅ 100+ LLM | ❌ 仅Claude | ✅ Model Garden | ✅ 任何FM | ❌ 仅Kimi |
| **Framework-Agnostic** | N/A (是框架) | ❌ 绑定API | N/A (是框架) | ✅ 任何框架 | N/A (是模型) |

### 维度1：实现原理

| 维度 | OpenAI SDK | Claude Managed | Google Platform | AWS AgentCore | Kimi Swarm |
|------|-----------|----------------|-----------------|---------------|------------|
| **Agent Loop** | ReAct Loop | while(tool_call) | BaseAgent.run() | 框架决定 | PARL训练的编排 |
| **编排实现** | 代码(Handoff) | 平台(Sub-agent) | 代码(Workflow Agents) | 协议(A2A/MCP) | 模型权重 |
| **确定性** | 高 | 中 | 高(工作流Agent) | 取决于框架 | 低 |

### 维度2：开发者体验

| 维度 | OpenAI SDK | Claude Managed | Google Platform | AWS AgentCore | Kimi Swarm |
|------|-----------|----------------|-----------------|---------------|------------|
| **上手时间** | ⭐⭐⭐⭐⭐ 5分钟 | ⭐⭐⭐⭐ 15分钟 | ⭐⭐⭐ 30分钟 | ⭐⭐ 1小时+ | ⭐⭐⭐⭐ 10分钟 |
| **语言支持** | Python/TS | Python/TS | Py/Java/Go/TS | 任何语言 | Python(API兼容) |
| **调试工具** | Tracing Dashboard | Event Log | ADK Web UI | CloudWatch | 基础API日志 |
| **文档质量** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

### 维度3：多Agent编排

| 维度 | OpenAI SDK | Claude Managed | Google Platform | AWS AgentCore | Kimi Swarm |
|------|-----------|----------------|-----------------|---------------|------------|
| **内建Sequential** | ❌ | ❌ | ✅ | ❌ | ❌ |
| **内建Parallel** | ❌ | 部分 | ✅ | ❌ | ✅ 模型原生 |
| **内建Loop** | ❌ | ❌ | ✅ | ❌ | ❌ |
| **DAG组合** | ❌ | ❌ | ✅ | ❌ | ❌ |
| **Handoff/路由** | ✅ | ✅ | ✅ | ✅(A2A) | ✅ 模型决策 |
| **Agent数量上限** | 开发者控制 | 数个 | 开发者控制 | 开发者控制 | 300+ |

### 维度4：执行环境与工具

| 维度 | OpenAI SDK | Claude Managed | Google Platform | AWS AgentCore | Kimi Swarm |
|------|-----------|----------------|-----------------|---------------|------------|
| **沙箱执行** | Sandbox Agent | 托管容器 | Agent Engine | microVM | 云端沙箱 |
| **MCP支持** | ✅ | ✅ 原生 | ✅ | ✅ | ❌ |
| **A2A支持** | ❌ | ❌ | ✅ 主导 | ✅ | ❌ |
| **Code Interpreter** | ✅ Hosted | ✅ Bash | ✅ | ✅ | ✅ |
| **浏览器** | ❌ | ❌ | ❌ | ✅ | ✅(内建搜索) |

### 维度5：记忆与状态

| 维度 | OpenAI SDK | Claude Managed | Google Platform | AWS AgentCore | Kimi Swarm |
|------|-----------|----------------|-----------------|---------------|------------|
| **短期对话记忆** | ✅ Session | ✅ Session | ✅ Session | ✅ Memory | ✅ 上下文 |
| **长期知识提取** | ❌ | ❌ | ✅ Memory Bank | ✅ Long-term | ❌ |
| **语义搜索** | ❌ | ❌ | ✅ | ✅ | ❌ |
| **故障恢复** | ❌ | ✅ Event Log | ✅ | ✅ | ❌ |
| **上下文窗口** | 模型决定 | 模型决定 | 模型决定 | 模型决定 | 256K |

### 维度6：安全与治理

| 维度 | OpenAI SDK | Claude Managed | Google Platform | AWS AgentCore | Kimi Swarm |
|------|-----------|----------------|-----------------|---------------|------------|
| **IAM/RBAC** | ❌ | 部分 | ✅ | ✅ | ❌ |
| **网络隔离** | ❌ | ✅ 域名白名单 | ✅ VPC | ✅ VPC+PrivateLink | ❌ |
| **合规认证** | ❌ | ✅ SOC2 | ✅ SOC/ISO/FedRAMP | ✅ 最全 | ❌ |
| **审计日志** | ✅ Tracing | ✅ Event Log | ✅ Cloud Audit | ✅ CloudTrail | ❌ |
| **Agent身份** | ❌ | ❌ | ✅ | ✅ | ❌ |

### 维度7：性能与成本

| 维度 | OpenAI SDK | Claude Managed | Google Platform | AWS AgentCore | Kimi Swarm |
|------|-----------|----------------|-----------------|---------------|------------|
| **冷启动** | 无(SDK) | 5-15s | 数秒 | 数秒(microVM) | 无(API) |
| **长时运行** | 有限 | ✅ 数小时 | ✅ | ✅ 8小时 | ✅ |
| **成本模型** | Token+工具 | Token+环境 | 多组件 | Serverless | Token |
| **自托管选项** | ✅ (SDK) | ❌ | ✅ (ADK) | ❌ | ✅ (开放权重) |

### 维度8：生态集成

| 维度 | OpenAI SDK | Claude Managed | Google Platform | AWS AgentCore | Kimi Swarm |
|------|-----------|----------------|-----------------|---------------|------------|
| **企业连接器** | ❌ | MCP生态 | ✅ Workspace/Salesforce等 | ✅ AWS全家桶 | ❌ |
| **第三方框架** | N/A | ❌ | LangChain/LlamaIndex | 全部支持 | OpenAI兼容 |
| **社区规模** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

### 维度9：适用场景

| 场景 | 最佳选择 | 原因 |
|------|----------|------|
| **快速原型/POC** | OpenAI SDK | 5分钟上手，极简API |
| **安全合规严格的企业** | AWS AgentCore | AWS安全全家桶+合规认证 |
| **已有Google Cloud** | Google Platform | 原生Workspace/IAM集成 |
| **长时编码任务** | Claude Managed | Brain-Hands-Session故障恢复 |
| **大规模并行研究** | Kimi Swarm | 300+ Agent 3-4.5x加速 |
| **复杂确定性工作流** | Google ADK | Sequential/Parallel/Loop原语 |
| **多框架共存** | AWS AgentCore | Framework-agnostic |
| **成本敏感/自托管** | Kimi Swarm | 开放权重 + INT4量化 |
| **MCP生态优先** | Claude Managed | MCP协议发起者 |
| **跨平台互操作** | Google / AWS | A2A协议支持 |

### 维度10：演进路线

| 平台 | 当前阶段 | 下一步 |
|------|----------|--------|
| OpenAI SDK | v0.16 快速迭代 | Sandbox成熟化 + A2A |
| Claude Managed | Public Beta | GA + 长期记忆 + A2A |
| Google Platform | GA | ADK 2.0 + Workspace深度集成 |
| AWS AgentCore | GA | 更强编排 + Agent Marketplace |
| Kimi Swarm | K2.6 | PARL 2.0 + MCP/A2A + 企业安全 |

---

## 四、场景选型决策树

```
你是什么样的团队？
│
├─→ "我想5分钟跑起来一个多Agent原型"
│     → OpenAI Agents SDK
│
├─→ "我有严格的安全合规要求（金融/医疗/政府）"
│     → AWS Bedrock AgentCore
│
├─→ "我已经用Google Cloud，想深度集成Workspace"
│     → Google Gemini Enterprise Agent Platform
│
├─→ "我需要Agent长时运行编码任务，不想管运维"
│     → Claude Managed Agents
│
├─→ "我的任务可以大规模并行分解，需要速度"
│     → Kimi Swarm (Agent Swarm模式)
│
├─→ "我想用LangGraph/CrewAI，但需要企业级运行时"
│     → AWS Bedrock AgentCore (BYOF)
│
├─→ "我需要确定性的工作流编排（不是LLM随机决定）"
│     → Google ADK (Sequential/Parallel/Loop)
│
├─→ "我的预算有限，想自托管所有东西"
│     → Kimi Swarm (开放权重) + OpenAI SDK (MIT)
│
└─→ "我不确定，想低风险尝试"
      → OpenAI Agents SDK (最低入门门槛)
        → 然后根据需求迁移到其他平台
```

---

## 五、架构演进趋势

### 趋势1：Brain-Hands-Session 解耦成为共识

所有平台都在向"认知(Brain)、执行(Hands)、状态(Session)分离"演进：
- Claude Managed 最先明确提出
- AWS AgentCore 通过模块化服务实现
- Google Agent Engine 内建此分层

### 趋势2：协议标准化（MCP + A2A）

```
2024                    2025                    2026
MCP发布(Anthropic)  →  主流采用(5家都支持) →  事实标准
                    →  A2A发布(Google)     →  跨平台互操作
```

### 趋势3：编排从代码走向模型

| 阶段 | 代表 | 特点 |
|------|------|------|
| **阶段1** | 硬编码编排 | if-else / DAG配置 |
| **阶段2** | LLM辅助编排 | LLM决定路由(Handoff) |
| **阶段3** | 框架编排原语 | Sequential/Parallel/Loop |
| **阶段4** | 模型原生编排 | PARL训练(Kimi Swarm) |

### 趋势4：企业Agent = 基础设施 + 治理

Agent从"酷炫的demo"走向企业生产，**基础设施层(Security/Observability/Memory)**的重要性超过Agent逻辑本身。

---

## 六、结论与建议

### 对技术决策者

1. **不要过早选型**：从OpenAI Agents SDK开始原型验证，再根据需求迁移
2. **安全是第一天的事**：选择有企业安全能力的平台（AWS/Google），不要事后补
3. **MCP先行**：无论选哪个平台，用MCP定义工具接口，保留互操作性
4. **单Agent优先**：不要为了"酷"而用多Agent，大多数场景单Agent+好的上下文工程更可靠

### 对架构师

1. **分层设计**：Brain(选模型) / Hands(选执行环境) / Session(选持久化) 独立选型
2. **确定性为先**：复杂工作流用ADK的确定性原语，不要依赖LLM的随机编排
3. **观测性必建**：Tracing/Logging/Metrics 从第一天就要有
4. **记忆要分层**：短期(Session) + 长期(知识提取) + 语义搜索，按需建设

### 对开发者

1. **掌握OpenAI SDK**：门槛最低，概念最清晰，是理解Agent编程的最佳入门
2. **理解MCP**：这是Agent时代的"HTTP"，会成为必备技能
3. **实验Kimi Swarm**：理解"模型即编排器"的新范式，开拓思维
4. **关注ADK**：它的工作流原语设计最成熟，值得学习

---

## 参考引用

> 本报告的详细引用分布于各平台独立研究报告中，以下为综合引用汇总。

### 官方文档与仓库
1. **OpenAI Agents SDK** — https://github.com/openai/openai-agents-python / https://openai.github.io/openai-agents-python/
2. **OpenAI Codex CLI** — https://github.com/openai/codex
3. **Anthropic Managed Agents** — https://docs.anthropic.com/en/docs/agents/managed-agents
4. **Anthropic Claude Code** — https://github.com/anthropic-ai/claude-code
5. **Google ADK** — https://github.com/google/adk-python / https://google.github.io/adk-docs/
6. **Google A2A Protocol** — https://github.com/google/A2A
7. **Google Agent Engine** — https://cloud.google.com/vertex-ai/docs/agents/agent-engine
8. **AWS Bedrock AgentCore** — https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore.html
9. **AWS Strands SDK** — https://github.com/awslabs/strands
10. **MoonshotAI Kimi K2** — https://github.com/MoonshotAI/Kimi-K2

### 协议与标准
11. **MCP (Model Context Protocol)** — https://modelcontextprotocol.io/ （Anthropic 发起, Agent-to-Tool 通信标准）
12. **A2A (Agent-to-Agent Protocol)** — https://github.com/google/A2A （Google 发起, 跨框架 Agent 互操作标准）

### 架构与设计哲学
13. **Anthropic: "Building Effective Agents"** — https://www.anthropic.com/research/building-effective-agents
14. **Anthropic: "How We Built Claude Code"** — https://www.anthropic.com/engineering/claude-code-architecture
15. **OpenAI: "Introducing the Agents SDK"** — https://openai.com/index/new-tools-for-building-agents/
16. **Google Cloud: "Introducing ADK"** — https://cloud.google.com/blog/products/ai-machine-learning/agent-development-kit
17. **AWS: "Introducing Bedrock AgentCore"** — https://aws.amazon.com/blogs/aws/introducing-amazon-bedrock-agentcore/
18. **Moonshot AI: "Kimi K2.5 Agent Swarm"** — https://www.moonshot.ai/blog/k2.5-agent-swarm

### 分析与对比研究
19. **Sid Bharath: "Agent Frameworks Compared"** — https://sidbharath.com/
20. **InfoQ: "AWS AgentCore vs Google ADK"** — https://www.infoq.com/
21. **Galileo AI: "Multi-Agent System Failure Modes"** — https://galileo.ai/
22. **Towards Data Science: "Error Propagation in Agent Swarms"** — https://towardsdatascience.com/
23. **Kimi K2 技术报告** — arXiv

### 各平台详细引用
- **OpenAI 报告完整引用**（18条）→ 见 `01-openai-agents-sdk-codex.md`
- **Claude 报告完整引用**（15条）→ 见 `02-claude-managed-agents.md`
- **Google 报告完整引用**（17条）→ 见 `03-google-gemini-agent-platform.md`
- **AWS 报告完整引用**（18条）→ 见 `04-aws-bedrock-agentcore.md`
- **Kimi 报告完整引用**（17条）→ 见 `05-kimi-swarm.md`
