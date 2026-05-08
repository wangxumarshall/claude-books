# AWS Bedrock AgentCore 深度研究报告

> **一句话核心价值**：AWS Bedrock AgentCore 为企业提供了一个**框架无关、模型无关的Agent运行时基础设施**，通过 Runtime(Serverless容器) + Memory(短期/长期分层) + Gateway(MCP/A2A统一接入) + Identity(IAM级Agent身份) + Observability(OTEL链路追踪) 五大模块化服务，让企业用**任何框架(LangGraph/CrewAI/Strands/OpenAI SDK)构建的Agent**都能获得AWS级别的安全、伸缩和治理能力——它是**Agent的"AWS Lambda"**，不造Agent框架，只造Agent运行的基础设施。

---

## 0. 核心架构与设计哲学

### 设计理念：「框架无关的Agent基础设施」

AWS 的设计哲学体现了其一贯的**基础设施即服务(IaaS)**思维：不提供Agent开发框架，而是提供让**任何Agent**都能安全运行的基础设施层。

### 九大模块化服务（官方产品页 2026-05 确认）

> **一句话定位**：不造Agent框架，只造Agent运行的基础设施——以模块化、可组合服务套件加速Agent从原型到生产。

```
┌──────────────────────────────────────────────────────────┐
│                  AWS Bedrock AgentCore                     │
│                                                            │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐            │
│  │  Runtime   │ │  Gateway   │ │  Policy    │            │
│  │            │ │            │ │            │            │
│  │ Serverless │ │ API/Lambda │ │ 自然语言→  │            │
│  │ Container  │ │ →MCP转换   │ │ Cedar策略  │            │
│  │ 会话隔离   │ │ 语义发现   │ │ 实时拦截   │            │
│  └────────────┘ └────────────┘ └────────────┘            │
│                                                            │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐            │
│  │  Memory    │ │  Identity  │ │ Evaluations│            │
│  │            │ │            │ │            │            │
│  │ 跨会话上下 │ │ Agent ID   │ │ 实时采样   │            │
│  │ 文+知识积  │ │ IAM/OAuth  │ │ 质量评分   │            │
│  │ 累         │ │ SigV4      │ │ 自定义评估 │            │
│  └────────────┘ └────────────┘ └────────────┘            │
│                                                            │
│  ┌────────────┐ ┌──────────────────────────────────┐     │
│  │ Observ.    │ │     Specialized Tools              │     │
│  │            │ │                                    │     │
│  │ OTEL       │ │ Code Interpreter  Browser          │     │
│  │ CloudWatch │ │ (多语言沙箱)     (无服务器浏览器)  │     │
│  │ Traces     │ │ Knowledge Bases                    │     │
│  └────────────┘ └──────────────────────────────────┘     │
└──────────────────────────────────────────────────────────┘
```

### 核心设计原则

| 原则 | 实现 | 对比 |
|------|------|------|
| **Framework-Agnostic** | 支持任何框架 | vs Google ADK（自有框架） |
| **Model-Agnostic** | 支持任何FM | vs Claude（仅Claude模型） |
| **Modular Services** | 可选组合各服务 | vs Claude（全托管bundled） |
| **Security-First** | IAM/VPC/PrivateLink 原生 | AWS安全基因 |
| **Serverless** | 零运维，自动伸缩 | Lambda模式 |

---

## 1. 实现原理和实现细节

### AgentCore Runtime

```python
# 框架无关：你的Agent可以用任何框架
# Runtime 只关心如何安全地运行你的容器

# 使用 Strands 框架的例子
from strands import Agent
from strands.tools import tool

@tool
def search_inventory(product_id: str) -> dict:
    """Search product inventory"""
    return {"product_id": product_id, "stock": 42}

agent = Agent(
    model="us.anthropic.claude-sonnet-4-20250514-v1:0",
    tools=[search_inventory],
    system_prompt="You are an inventory management assistant."
)

# 部署到 AgentCore Runtime
# → 自动获得 microVM 隔离、会话管理、自动伸缩
```

**Runtime 实现细节**：
- 基于 **Firecracker microVM**（与Lambda相同的底层技术）
- 每个 Session 独立的 microVM 实例
- 支持**实时**（同步请求-响应）和**长时运行**（最长8小时）
- 自动伸缩，Serverless模式

### AgentCore Memory

```python
# Memory 分两层

# 短期记忆 - Session Events
short_term = {
    "session_id": "sess_123",
    "events": [
        {"role": "user", "content": "What's my order status?"},
        {"role": "assistant", "content": "Let me check..."},
        {"role": "tool_result", "content": "Order #456 shipped"}
    ],
    "ttl": 3600  # 1小时后过期
}

# 长期记忆 - Extracted Knowledge
long_term = {
    "namespace": "user/john_doe",
    "memories": [
        {
            "fact": "Prefers expedited shipping",
            "source": "session_abc",
            "confidence": 0.95,
            "created_at": "2026-01-15"
        },
        {
            "fact": "Usually orders on weekends",
            "source": "pattern_analysis",
            "confidence": 0.87
        }
    ]
}
```

**Memory 实现细节**：
- **短期记忆**：Session内的原始对话记录，TTL过期
- **长期记忆**：自动从对话中提取事实/偏好/摘要
- **语义搜索**：向量化存储 + 混合检索
- **层级命名空间**：`org/team/user` 级别的隔离

### AgentCore Gateway

```
┌─────────────────────────────────────────┐
│           AgentCore Gateway              │
│                                          │
│  External APIs/Services                  │
│       │                                  │
│       ▼                                  │
│  ┌─────────────┐  ┌─────────────┐       │
│  │ API → MCP   │  │ Lambda→MCP  │       │
│  │ Translator  │  │ Translator  │       │
│  └──────┬──────┘  └──────┬──────┘       │
│         │                │               │
│         ▼                ▼               │
│  ┌──────────────────────────────┐       │
│  │     Unified MCP Interface    │       │
│  │  (Tool Discovery + Auth +    │       │
│  │   Rate Limiting + Logging)   │       │
│  └──────────────┬───────────────┘       │
│                 │                        │
│                 ▼                        │
│         Agent Runtime                    │
└─────────────────────────────────────────┘
```

**Gateway 实现细节**：
- 将传统 REST API / Lambda / 外部服务**自动转换为MCP兼容工具**
- 统一的认证层（SigV4 / OAuth 2.0 / API Key）
- 内建速率限制和配额管理
- 工具发现注册表

### AgentCore Identity

```python
# Agent 身份管理
agent_identity = {
    "agent_id": "arn:aws:bedrock:us-east-1:123456:agent/my-agent",
    "authentication": {
        "inbound": "sigv4",          # 验证调用者身份
        "outbound": {
            "type": "oauth2",
            "provider": "cognito",    # 使用 Cognito 获取token
            "scopes": ["read:data"]   # 最小权限
        }
    },
    "iam_role": "arn:aws:iam::123456:role/AgentExecutionRole",
    "permissions": {
        "s3": ["GetObject"],          # 只读S3
        "dynamodb": ["Query"],        # 只查DynamoDB
        "bedrock": ["InvokeModel"]    # 可调用模型
    }
}
```

**Identity 实现细节**：
- 每个 Agent 有独立的 **IAM Role**
- 支持与 Cognito / Okta / Entra ID 集成
- **最小权限原则**：Agent只能访问明确授权的资源
- 跨Agent通信（A2A）也需要认证

### AgentCore Observability

```python
# OTEL 兼容的遥测数据

# 自动捕获：
# 1. Agent 调用链路 (Traces)
trace = {
    "trace_id": "abc123",
    "spans": [
        {"name": "agent_invocation", "duration_ms": 2500},
        {"name": "model_inference", "duration_ms": 1800, 
         "attributes": {"model": "claude-sonnet", "tokens": 1500}},
        {"name": "tool_execution", "duration_ms": 200,
         "attributes": {"tool": "search_inventory"}}
    ]
}

# 2. 指标 (Metrics)
metrics = {
    "invocation_count": 1000,
    "avg_latency_ms": 2500,
    "error_rate": 0.02,
    "token_usage": {"input": 50000, "output": 30000},
    "cost_usd": 1.25
}

# 3. 日志 → CloudWatch
# 4. Dashboard → 自动生成
```

---

## 2. 开发者使用方式与上手路径（SDK 完全指南）

### 2.1 安装与环境配置

```bash
# AWS SDK（核心）
pip install boto3
pip install awscli

# AgentCore Toolkit（专用 CLI）
pip install bedrock-agentcore-toolkit

# Strands Agents（AWS 原生框架，推荐）
pip install strands-agents
pip install 'strands-agents[bedrock]'

# 或使用其他框架
pip install langgraph crewai openai-agents

# 环境配置
aws configure  # 设置 Access Key / Secret / Region
export AWS_REGION=us-west-2
```

### 2.2 AgentCore 九大服务 API 概览

```
bedrock-agentcore/                    # AgentCore 服务族
│
├── Runtime/                           # 无服务器部署
│   ├── deploy_agent()                 # 部署 Agent（代码上传 / 容器）
│   ├── invoke_agent()                 # 调用 Agent
│   ├── create_session()               # 创建会话
│   └── config: 会话隔离 + 8h 异步支持
│
├── Gateway/                           # 工具接入网关
│   ├── register_api_tool()            # 注册 API 工具
│   ├── register_lambda_tool()         # 注册 Lambda 工具
│   ├── connect_mcp_server()           # 连接 MCP Server
│   └── semantic_search_tools()        # 语义工具发现
│
├── Policy/                            # 策略执行引擎
│   ├── create_policy()                # 创建策略（自然语言→Cedar）
│   ├── evaluate_policy()              # 评估策略
│   └── config: 实时拦截 + Gateway 集成
│
├── Memory/                            # 智能记忆
│   ├── store_memory()                 # 存储记忆
│   ├── retrieve_memory()              # 检索记忆
│   ├── semantic_search()              # 语义搜索
│   └── config: 短期/长期/语义分层
│
├── Identity/                          # 身份治理
│   ├── create_agent_identity()        # 创建 Agent 身份
│   ├── configure_oauth()              # 配置 OAuth
│   └── config: IAM/Cognito/Okta 集成
│
├── Evaluations/                       # 持续质量评估
│   ├── create_evaluator()             # 创建评估器
│   ├── sample_interactions()          # 采样交互
│   └── metrics: 正确性/安全性/目标达成率
│
├── Observability/                     # 可观测性
│   ├── config: CloudWatch + OTEL
│   ├── traces                         # 分布式追踪
│   ├── metrics                        # 运行指标
│   └── dashboards                     # 自动仪表盘
│
├── Code Interpreter/                  # 代码执行
│   ├── execute_code()                 # 沙箱执行代码
│   └── config: 多语言支持
│
└── Browser/                           # 浏览器运行时
    ├── create_browser_session()        # 创建浏览器会话
    └── config: 自动缩放 + CAPTCHA 处理
```

### 2.3 两种核心开发路径

#### 路径 A：Bedrock Agents（全托管，低代码）

```python
import boto3

client = boto3.client('bedrock-agent-runtime', region_name='us-west-2')

# 调用已创建的 Agent
response = client.invoke_agent(
    agentId='YOUR_AGENT_ID',
    agentAliasId='YOUR_AGENT_ALIAS_ID',
    sessionId='unique-session-id',
    inputText="What is the status of my order?",
    enableTrace=True,
)

# 流式接收响应
for event in response.get('completion'):
    if 'chunk' in event:
        print(event['chunk']['bytes'].decode('utf-8'), end='')
    elif 'trace' in event:
        # 追踪信息：推理过程、工具调用
        print(f"\n[Trace] {event['trace']}")
```

#### 路径 B：AgentCore + Strands Agents（BYOF 推荐）

```python
from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.tools import tool

# 定义工具
@tool
def search_inventory(product_name: str) -> dict:
    """搜索产品库存信息"""
    return {"product": product_name, "stock": 42, "warehouse": "上海"}

@tool
def create_order(product_name: str, quantity: int) -> dict:
    """创建订单"""
    return {"order_id": "ORD-12345", "product": product_name, "quantity": quantity}

# 创建 Agent（Strands 的极简 API）
agent = Agent(
    model=BedrockModel(
        model_id="anthropic.claude-sonnet-4-20250514-v1:0",
        region_name="us-west-2",
    ),
    system_prompt="""你是电商助手。帮助用户：
    1. 查询库存
    2. 创建订单
    3. 跟踪物流""",
    tools=[search_inventory, create_order],
)

# 运行
response = agent("帮我查一下 MacBook Pro 的库存，如果有就下单两台")
print(response)
```

### 2.4 AgentCore 各服务集成 Demo

#### Gateway — 工具注册与发现

```python
import boto3

gateway = boto3.client('bedrock-agentcore-gateway')

# 注册 API 作为工具
gateway.register_api_tool(
    name="crm_lookup",
    description="查询客户 CRM 信息",
    api_spec={
        "method": "GET",
        "url": "https://api.internal.com/crm/customers/{customer_id}",
        "auth": {"type": "sigv4"},
    },
)

# 注册 Lambda 作为工具
gateway.register_lambda_tool(
    name="invoice_processor",
    description="处理发票",
    function_arn="arn:aws:lambda:us-west-2:123456:function:invoice-processor",
)

# 连接 MCP Server
gateway.connect_mcp_server(
    name="github_tools",
    server_url="https://mcp.internal.com/github",
    transport="sse",
)

# 语义工具发现（Agent 可以搜索可用工具）
tools = gateway.semantic_search_tools(
    query="查找与客户关系管理相关的工具",
    max_results=5,
)
```

#### Memory — 分层记忆

```python
memory = boto3.client('bedrock-agentcore-memory')

# 存储短期记忆（会话内）
memory.store_memory(
    session_id="session_123",
    memory_type="short_term",
    content={"user_preference": "偏好中文回复", "context": "正在处理退款"},
)

# 存储长期记忆（跨会话）
memory.store_memory(
    user_id="user_456",
    memory_type="long_term",
    content={"name": "王小明", "vip_level": "gold", "last_issue": "退款"},
)

# 语义搜索记忆
results = memory.semantic_search(
    user_id="user_456",
    query="用户之前遇到过什么问题？",
    memory_types=["long_term"],
    max_results=5,
)
```

#### Policy — 自然语言策略

```python
policy = boto3.client('bedrock-agentcore-policy')

# 用自然语言定义策略（自动转换为 Cedar 语言）
policy.create_policy(
    name="refund_limit",
    description="Agent 单次退款不能超过 1000 元",
    natural_language_rule="Agent 执行退款工具时，金额不得超过 1000 人民币。超过时需要人工审批。",
    # 自动生成 Cedar 策略并与 Gateway 集成
)

# 策略自动与 Gateway 集成
# 当 Agent 尝试调用退款工具且金额 > 1000 时：
# → Gateway 实时拦截 → 返回 "需要人工审批" → Agent 通知用户
```

#### Identity — Agent 身份配置

```python
identity = boto3.client('bedrock-agentcore-identity')

# 创建 Agent 身份
identity.create_agent_identity(
    agent_name="customer_service_agent",
    iam_role="arn:aws:iam::123456:role/AgentServiceRole",
    oauth_config={
        "provider": "cognito",
        "user_pool_id": "us-west-2_xxx",
        "client_id": "xxx",
        "scopes": ["read:orders", "write:refunds"],
    },
    # Agent 代表用户访问资源时使用 OAuth
    # Agent 自主访问 AWS 资源时使用 IAM Role
)
```

#### Runtime — 部署到生产

```bash
# 使用 AgentCore Toolkit CLI 部署

# 方式1：代码上传部署
agentcore deploy \
  --name my-agent \
  --entry main.py \
  --requirements requirements.txt \
  --region us-west-2

# 方式2：容器化部署
agentcore deploy \
  --name my-agent \
  --image 123456.dkr.ecr.us-west-2.amazonaws.com/my-agent:latest \
  --region us-west-2

# 配置选项
agentcore configure \
  --name my-agent \
  --memory-enabled \
  --gateway-enabled \
  --identity-role arn:aws:iam::123456:role/AgentRole \
  --vpc-config subnet-xxx,sg-xxx \
  --max-session-duration 8h
```

### 2.5 上手路径总结

```
Level 1: Bedrock Agents (控制台创建，快速启动)
    └─ 零代码，可视化配置 → invoke_agent()

Level 2: AgentCore + Strands Agents (AWS原生框架)
    └─ from strands import Agent → 极简 Python

Level 3: AgentCore + BYOF (自选框架)
    └─ LangGraph / CrewAI / OpenAI SDK → agentcore deploy

Level 4: Gateway + Policy (工具接入 + 策略执行)
    └─ API/Lambda/MCP → Cedar 策略实时拦截

Level 5: Memory + Identity (分层记忆 + 身份治理)
    └─ 短期/长期/语义记忆 + IAM/OAuth

Level 6: Evaluations + Observability (质量保证)
    └─ 实时采样评分 + OTEL + CloudWatch

Level 7: 全栈生产部署 (VPC + 会话隔离 + 8h异步)
    └─ 企业级安全合规
```

---


## 3. 多Agent协调与Orchestration

### 支持的多Agent模式

| 模式 | 描述 | 实现方式 |
|------|------|----------|
| **Agents-as-Tools** | 主Agent调用子Agent作为工具 | 框架层面实现 |
| **A2A Protocol** | 平等Agent间的标准化通信 | JSON-RPC 2.0 over HTTPS |
| **Supervisor** | 监督Agent协调多个专家Agent | AgentCore + Strands |
| **Multi-Agent Collaboration** | 层级式任务委托 | 多Runtime实例 |

### A2A 协议在 AgentCore 中的实现

```
Agent A (Runtime 1)                Agent B (Runtime 2)
┌──────────────────┐              ┌──────────────────┐
│ Sales Agent      │    A2A       │ Inventory Agent  │
│ (LangGraph)      │←──────────→ │ (Strands)        │
│                  │  JSON-RPC   │                  │
│ "Check stock    │  HTTPS      │ "Product X has   │
│  for product X" │             │  42 units"       │
└──────────────────┘              └──────────────────┘
        │                                │
        └─── AgentCore Identity ─────────┘
             (SigV4 认证)
```

---

## 4. 执行环境与工具集成（Hands层）

### 特殊执行环境

| 工具 | 描述 | 用途 |
|------|------|------|
| **Code Interpreter** | 安全沙箱Python执行 | 数据分析、计算 |
| **Browser** | 云端浏览器实例 | 网页交互自动化 |
| **Knowledge Bases** | 向量+关键词混合检索 | RAG |

### Gateway 工具集成

```
                AgentCore Gateway
                      │
        ┌─────────────┼─────────────┐
        │             │             │
    REST API     Lambda Fn    MCP Server
    → MCP Tool   → MCP Tool   (原生)
        │             │             │
        └─────────────┼─────────────┘
                      │
              Agent Runtime
```

---

## 5. 记忆、状态与持久化

### 最完善的记忆系统

AgentCore 拥有五个平台中**最完善的记忆系统**：

| 维度 | AgentCore | OpenAI SDK | Claude | Google ADK | Kimi |
|------|-----------|------------|--------|------------|------|
| 短期对话记忆 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 长期知识提取 | ✅ | ❌ | ❌ | ✅(Engine) | ❌ |
| 语义搜索 | ✅ | ❌ | ❌ | ✅(Engine) | ❌ |
| 命名空间隔离 | ✅ | ❌ | ❌ | 部分 | ❌ |
| 自动提取策略 | ✅ | ❌ | ❌ | ✅ | ❌ |
| 跨Session持久 | ✅ | ✅(Redis) | ✅ | ✅ | ❌ |

---

## 6. 安全、治理与企业特性

### AWS 安全生态深度整合

| 能力 | AWS 服务 | 状态 |
|------|----------|------|
| 身份认证 | IAM + Cognito + SigV4 | ✅ |
| 网络隔离 | VPC + PrivateLink | ✅ |
| 数据加密 | KMS (CMEK) | ✅ |
| 审计日志 | CloudTrail | ✅ |
| 访问控制 | IAM Policies (细粒度) | ✅ |
| 合规 | SOC1/2/3, ISO, HIPAA, FedRAMP | ✅ |
| DLP | Macie 集成 | ✅ |
| 威胁检测 | GuardDuty | ✅ |
| 资源标签 | Resource Tagging | ✅ |

**安全优势**：AgentCore 继承了 AWS 20+ 年的企业安全积累，这是其他平台难以复制的。

---

## 7. 性能、成本与生产就绪度

### Serverless 定价模型

| 计费项 | 方式 |
|--------|------|
| Runtime（计算） | 按microVM活跃时间 + 内存用量 |
| Memory | 按存储量 + 查询次数 |
| Gateway | 按API调用次数 |
| Model Inference | 按Token用量（独立计费） |
| Storage (S3) | 标准S3定价 |
| Observability | CloudWatch 定价 |

### 性能特征

| 指标 | 表现 |
|------|------|
| 冷启动 | 数秒（microVM） |
| 长时运行 | 最长 8 小时 |
| 会话隔离 | 100%（独立microVM） |
| 自动伸缩 | Serverless，无需配置 |

### 生产就绪度

| 维度 | 评分 | 说明 |
|------|------|------|
| 稳定性 | ⭐⭐⭐⭐⭐ | GA (2025-10) |
| 企业安全 | ⭐⭐⭐⭐⭐ | AWS安全全家桶 |
| 可观测性 | ⭐⭐⭐⭐⭐ | OTEL + CloudWatch |
| 文档质量 | ⭐⭐⭐⭐ | AWS标准文档 |
| 学习曲线 | ⭐⭐ | AWS概念多，上手复杂 |
| 开发体验 | ⭐⭐⭐ | 不如OpenAI SDK简洁 |

---

## 8. 集成与生态

```
AWS Bedrock AgentCore 生态
  ├─ 模型：Bedrock FM (Claude/Llama/Mistral/Titan)
  ├─ 框架：LangGraph / CrewAI / Strands / OpenAI SDK / Google ADK
  ├─ 协议：MCP + A2A
  ├─ 存储：S3 / DynamoDB / RDS / OpenSearch
  ├─ 计算：Lambda / ECS / EKS
  ├─ 安全：IAM / KMS / VPC / Cognito
  ├─ 观测：CloudWatch / CloudTrail / X-Ray
  ├─ AI：SageMaker / Bedrock Knowledge Bases
  └─ 企业：QuickSight / Connect / Lex
```

---

## 9. 适用场景（优势）与局限性

### ✅ 最佳场景

| 场景 | 为什么合适 |
|------|-----------|
| **已有AWS基础设施的企业** | 原生IAM/VPC/CloudWatch集成 |
| **需要多框架共存** | Framework-agnostic设计 |
| **安全合规要求严格** | FedRAMP/HIPAA/SOC认证 |
| **需要长期记忆** | 最完善的Memory系统 |
| **多Agent协作** | A2A协议 + MCP Gateway |
| **Serverless需求** | 零运维自动伸缩 |

### ❌ 核心局限

| 局限 | 影响 | 替代方案 |
|------|------|----------|
| **无自有Agent框架** | 需搭配第三方框架 | 用Strands或LangGraph |
| **学习曲线陡峭** | AWS概念/服务多 | 从Bedrock Agents开始 |
| **开发体验不如SDK** | 不如OpenAI SDK简洁 | 优先用SDK开发，部署用AgentCore |
| **区域限制** | 部分服务限特定区域 | 检查最新区域支持 |
| **成本复杂** | 多组件分别计费 | 使用Cost Explorer监控 |
| **无内建工作流引擎** | 复杂DAG需框架实现 | 用LangGraph或Step Functions |
| **冷启动延迟** | microVM需要数秒 | 使用预热策略 |

---

## 10. 演进路线与未来

### 演进历程

```
2023-09  Amazon Bedrock GA
2024-01  Agents for Bedrock GA
2024-06  Knowledge Bases 增强
2025-04  AgentCore 预览
2025-10  AgentCore GA (重大里程碑)
2026-01  AgentCore Memory GA
2026-03  AgentCore Gateway + A2A 支持
2026-05  当前状态
```

### 未来方向

1. **AgentCore 2.0**：更强的多Agent编排原语
2. **Strands 框架成熟化**：AWS原生Agent SDK
3. **Agent Marketplace**：预构建Agent模板
4. **Edge Agent**：IoT/边缘设备上的Agent运行时
5. **与Step Functions深度整合**：声明式长时工作流

---

## 核心价值总结

> **AWS Bedrock AgentCore** 不造Agent框架，只造Agent运行的基础设施——通过Runtime(无服务器部署)+Gateway(工具接入)+Policy(策略执行)+Memory(智能记忆)+Identity(IAM身份)+Evaluations(质量监控)+Observability(OTEL链路追踪)+Code Interpreter(代码执行)+Browser(浏览器运行时)九大模块化服务，让企业用**任何框架、任何模型**构建的Agent都能获得AWS级别的安全隔离、自动伸缩和合规治理，是将AI Agent从"玩具"推向"企业生产"的**基础设施决定性答案**。

---

## 参考引用

1. **AWS 官方文档: "Amazon Bedrock AgentCore"** — https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore.html （AgentCore Runtime/Memory/Gateway/Identity/Observability 五大模块完整文档）
2. **AWS Blog: "Introducing Amazon Bedrock AgentCore"** — https://aws.amazon.com/blogs/aws/introducing-amazon-bedrock-agentcore/ （AgentCore 发布公告，Framework-agnostic 设计哲学与五大服务详解）
3. **AWS re:Invent 2025: AgentCore Architecture** — https://aws.amazon.com/events/reinvent/ （AgentCore GA 发布, microVM 隔离架构, 长时运行支持）
4. **Amazon Bedrock AgentCore Runtime GitHub** — https://github.com/awslabs/amazon-bedrock-agentcore-runtime （开源 Runtime 客户端与部署示例）
5. **AWS Bedrock AgentCore Pricing** — https://aws.amazon.com/bedrock/agentcore/pricing/ （Serverless 按用量计费模型：Runtime/Memory/Gateway/Model 分别计费）
6. **Amazon Bedrock 定价概览** — https://aws.amazon.com/bedrock/pricing/ （模型推理 Token 计费, 按需/预留吞吐量选项）
7. **AWS Blog: "Multi-Agent Collaboration with A2A"** — https://aws.amazon.com/blogs/machine-learning/multi-agent-collaboration/ （A2A 协议在 AgentCore 中的实现, JSON-RPC 2.0, SigV4 认证）
8. **AWS: "MCP Server Hosting"** — https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-gateway.html （AgentCore Gateway: REST API/Lambda → MCP 自动转换, 统一认证/速率限制）
9. **Dev.to: "Building Production Agents with AgentCore"** — https://dev.to/aws （AgentCore 实战指南：BYOF 部署, 实时与长时运行模式, 8小时执行上限）
10. **InfoQ: "AWS AgentCore vs Google ADK"** — https://www.infoq.com/ （AgentCore Framework-agnostic vs ADK Code-first 设计对比分析）
11. **TrueFoundry: "Bedrock AgentCore Cost Analysis"** — https://www.truefoundry.com/ （AgentCore 多组件成本结构分析与优化建议）
12. **CloudChipr: "Bedrock Pricing Deep Dive"** — https://www.cloudchipr.com/ （Bedrock 模型推理成本详细对比）
13. **CloudKeeper: "MCP and A2A in AWS"** — https://www.cloudkeeper.com/ （MCP Agent-to-Tool vs A2A Agent-to-Agent 协议在 AWS 中的角色定位）
14. **OpenSearch.org: "Vector Search for AgentCore"** — https://opensearch.org/ （OpenSearch Serverless 在 AgentCore Knowledge Bases 和 Memory 中的向量检索应用）
15. **AWS IAM 文档** — https://docs.aws.amazon.com/IAM/latest/UserGuide/ （Agent Identity 的 IAM Role, SigV4 认证, 最小权限原则实现）
16. **AWS CloudTrail 文档** — https://docs.aws.amazon.com/cloudtrail/ （AgentCore 审计日志与合规追踪）
17. **AWS Strands SDK** — https://github.com/awslabs/strands （AWS 原生 Agent 开发框架，与 AgentCore Runtime 深度集成）
18. **Go-Cloud.io: "Bedrock Enterprise Cost"** — https://go-cloud.io/ （企业级 Bedrock 部署的总体拥有成本分析）
