# OpenAI Agents SDK + Codex CLI 深度研究报告

> **一句话核心价值**：OpenAI Agents SDK + Codex 为开发者提供了一个**轻量级、provider-agnostic 的多Agent编排框架 + 沙箱化终端编码Agent**，通过 Handoff 原语和平台原生沙箱将"LLM→工具→多Agent协调"的复杂度压缩到极简 Python/TS API中，让任何团队都能在几十行代码内构建可观测、可防护、可交接的自主Agent工作流，同时 Codex CLI 证明了"终端优先+沙箱安全"的编码Agent范式可以在开发者日常工作中安全地自主运行。

---

## 0. 核心架构与设计哲学

### 设计理念：「够用的抽象」
OpenAI Agents SDK 的设计哲学可以用一个词概括：**"Minimal but sufficient"**（最小但足够）。它不试图成为一个全栈Agent平台（如AWS AgentCore），而是提供刚好够用的抽象层，让开发者用最少的代码完成多Agent编排。

### 核心架构原语

| 原语 | 作用 | 类比 |
|------|------|------|
| **Agent** | 配置了instructions、tools、guardrails、handoffs的LLM | 一个"有角色定义的员工" |
| **Sandbox Agent** | 预配置了容器环境的Agent（v0.14.0+） | "带办公室的员工" |
| **Handoff** | Agent间的任务委托机制 | "转接电话" |
| **Guardrail** | 输入/输出/工具调用的安全校验层 | "门卫检查" |
| **Runner** | 执行Agent的运行时循环 | "流水线控制器" |
| **Session** | 跨run的对话历史管理 | "对话记忆" |
| **Tracing** | 内建的运行追踪系统 | "黑匣子记录仪" |
| **Realtime Agent** | 实时语音Agent（基于gpt-realtime-2） | "语音座席" |
| **Voice Agent** | 语音管道Agent | "语音助手" |

### 架构分层

```
┌──────────────────────────────────────────────┐
│              Developer API Layer              │
│  Agent() / Runner.run() / handoff() / trace()│
├──────────────────────────────────────────────┤
│           Orchestration Engine                │
│  Agent Loop (ReAct) / Handoff Router /       │
│  Guardrail Pipeline / Session Manager        │
├──────────────────────────────────────────────┤
│              Model Provider Layer             │
│  OpenAI Responses API / Chat Completions /   │
│  LiteLLM (100+ LLMs) / any-llm             │
├──────────────────────────────────────────────┤
│              Tool Integration Layer           │
│  Function Tools / MCP Servers / Hosted Tools │
│  (Code Interpreter, File Search, Web Search) │
├──────────────────────────────────────────────┤
│            Sandbox & Execution Layer          │
│  UnixLocalSandboxClient / Container Sandbox  │
│  Codex CLI (Seatbelt/Bubblewrap/Windows)     │
└──────────────────────────────────────────────┘
```

### 为什么这么设计？

1. **Provider-Agnostic**：不绑死 OpenAI 模型，支持 100+ LLM，降低vendor lock-in
2. **组合优于继承**：Agent、Tool、Guardrail 都是独立原语，自由组合
3. **渐进复杂度**：单Agent → Handoff → Agents-as-Tools → Sandbox Agent，按需升级
4. **可观测性内建**：Tracing 默认开启，不需要额外集成

---

## 1. 实现原理和实现细节

### Agent 执行循环（核心Loop）

```python
# 简化版 Runner 核心逻辑
async def run(agent, input, context):
    current_agent = agent
    messages = [{"role": "user", "content": input}]
    
    while True:
        # 1. 并行执行 Input Guardrails（首个Agent才执行）
        await run_input_guardrails(current_agent, messages)
        
        # 2. 调用 LLM
        response = await current_agent.model.generate(
            instructions=current_agent.instructions,
            tools=current_agent.tools + current_agent.handoffs,
            messages=messages
        )
        
        # 3. 检查是否有 Handoff
        if response.has_handoff:
            handoff_target = resolve_handoff(response.handoff_call)
            current_agent = handoff_target
            messages = transfer_context(messages, handoff_target)
            continue  # 重新进入循环
        
        # 4. 检查是否有 Tool Call
        if response.has_tool_calls:
            for tool_call in response.tool_calls:
                # 执行 Tool Guardrails
                await run_tool_guardrails(tool_call)
                result = await execute_tool(tool_call)
                messages.append(tool_result(result))
            continue  # 重新进入循环
        
        # 5. 执行 Output Guardrails
        await run_output_guardrails(current_agent, response)
        
        # 6. 返回结果
        return RunResult(final_output=response.text)
```

### Handoff 内部实现

Handoff 本质上是一个**伪装成 Tool 的 Agent 引用**：

```python
# Handoff 被序列化为工具定义
{
    "type": "function",
    "name": "transfer_to_spanish_agent",
    "description": "Handoff to the Spanish-speaking agent",
    "parameters": {"type": "object", "properties": {}}
}
```

当 LLM 调用 `transfer_to_spanish_agent` 时：
1. Runner 识别这是 Handoff 而非普通 Tool
2. 将当前对话历史传递给目标 Agent
3. 目标 Agent 接管后续循环
4. **关键**：Handoff 是**替换式**的，当前 Agent 退出循环

### Agents-as-Tools vs Handoff

| 特征 | Handoff | Agents-as-Tools |
|------|---------|-----------------|
| 控制权 | 完全转移 | 保留在调用方 |
| 返回值 | 目标Agent继续运行 | 返回结果给调用方 |
| 适用场景 | 多语言路由、专家转接 | 子任务委托、信息查询 |
| 对话历史 | 继承全部 | 隔离的子对话 |

### Guardrail 三层防护体系

```
Input Guardrails ────→ [仅首个Agent]
    │
    ▼
Agent 执行循环
    │
    ├─→ Tool Guardrails ────→ [每次工具调用前后]
    │       ├─ Pre-tool check (输入校验)
    │       └─ Post-tool check (输出校验)
    │
    ▼
Output Guardrails ────→ [最终输出校验]
```

- **并行模式**（默认）：Guardrail 与 Agent 执行并行运行，低延迟但可能浪费token
- **阻塞模式**：Guardrail 先执行完毕才让 Agent 继续
- **Tripwire 机制**：检测到违规时抛出异常，开发者捕获后返回安全回复

### Sandbox Agent（v0.14.0+，核心创新）

```python
from agents.sandbox import Manifest, SandboxAgent, SandboxRunConfig
from agents.sandbox.entries import GitRepo

agent = SandboxAgent(
    name="Workspace Assistant",
    instructions="Inspect the sandbox workspace before answering.",
    default_manifest=Manifest(
        entries={
            "repo": GitRepo(repo="openai/openai-agents-python", ref="main"),
        }
    ),
)
```

Sandbox Agent 的创新在于：
- **Manifest 声明式环境配置**：用声明式方式定义沙箱中的文件系统
- **与 Codex CLI 共享沙箱基础设施**：复用 Seatbelt/Bubblewrap 隔离
- **长时任务支持**：容器状态跨 turn 持久化

### Tracing 实现

```python
# 自动追踪（默认）
with trace("customer_support_workflow", group_id="session_123"):
    result = await Runner.run(triage_agent, user_input)

# Span 层级
# Trace
#   └─ agent_span("triage_agent")
#        ├─ generation_span(model="gpt-4.1")
#        ├─ guardrail_span("toxicity_check")
#        ├─ handoff_span("→ billing_agent")
#        └─ agent_span("billing_agent")
#             ├─ generation_span(model="gpt-4.1-mini")
#             └─ function_span("lookup_invoice")
```

---

## 2. 开发者使用方式与上手路径（SDK 完全指南）

### 2.1 安装与环境配置

```bash
# 基础安装
pip install openai-agents            # 核心包
pip install 'openai-agents[voice]'   # 语音支持
pip install 'openai-agents[redis]'   # Redis Session
pip install 'openai-agents[litellm]' # 100+ LLM Provider

# 或使用 uv
uv add openai-agents
uv add 'openai-agents[voice]'

# 环境变量
export OPENAI_API_KEY=sk-...
```

### 2.2 完整 SDK API 模块目录（官方 API Reference）

```
agents/                          # 核心包
├── Agent                        # 主类：LLM Agent 定义
├── Runner                       # 运行器：run() / run_sync() / run_streamed()
├── RunConfig                    # 运行配置：模型/温度/并行度
├── RunState                     # 运行状态机
├── Result / RunResult           # 运行结果
├── Items                        # 对话项（消息/工具调用/输出）
├── RunContext / ToolContext      # 运行/工具上下文
├── Usage                        # Token 用量统计
├── Exceptions                   # 异常体系
│
├── tools/                       # 工具系统
│   ├── function_tool()          # 装饰器：Python函数 → Agent工具
│   ├── FunctionTool             # 显式工具类
│   ├── agent_as_tool()          # 将 Agent 作为工具使用
│   ├── HostedTool               # 托管工具（web_search/file_search/code_interpreter）
│   ├── ToolGuardrails           # 工具调用防护
│   └── ToolOutputTrimmer        # 工具输出截断器
│
├── handoffs/                    # 切换系统
│   ├── Handoff                  # 切换定义
│   ├── handoff()                # 自定义切换函数
│   ├── HandoffInputFilter       # 输入过滤器
│   └── HandoffPrompt            # 切换提示词模板
│
├── guardrails/                  # 防护系统
│   ├── InputGuardrail           # 输入防护
│   ├── OutputGuardrail          # 输出防护
│   └── GuardrailFunctionOutput  # 防护结果
│
├── sessions/                    # 会话持久化
│   ├── SQLAlchemySession        # 默认：SQLite/PostgreSQL
│   ├── AdvancedSQLiteSession    # 高级 SQLite
│   ├── EncryptedSession         # 加密存储
│   ├── RedisSession             # 分布式
│   ├── MongoDBSession           # MongoDB
│   └── DaprSession              # Dapr 集成
│
├── mcp/                         # MCP 集成
│   ├── MCPServerStdio           # stdio 连接
│   ├── MCPServerSse             # SSE 连接
│   └── MCPServerStreamableHttp  # HTTP 连接
│
├── sandbox/                     # 沙箱系统
│   ├── SandboxAgent             # 沙箱 Agent
│   ├── Manifest                 # 环境声明
│   ├── GitRepo / Directory / File  # 工作区条目
│   ├── Permissions              # 权限控制
│   ├── SnapshotSpec             # 快照
│   ├── Capabilities             # 能力集
│   │   ├── Filesystem           # 文件系统能力
│   │   ├── Shell                # Shell 能力
│   │   ├── Memory               # 记忆能力
│   │   ├── Skills               # 技能能力
│   │   └── Compaction           # 压缩能力
│   └── clients/
│       ├── UnixLocalSandboxClient  # 本地沙箱
│       └── DockerSandboxClient     # Docker 沙箱
│
├── realtime/                    # 实时 Agent
│   ├── RealtimeAgent            # 实时 Agent 定义
│   ├── RealtimeRunner           # 实时运行器
│   ├── RealtimeSession          # 实时会话
│   └── RealtimeConfig           # 配置
│
├── voice/                       # 语音 Agent
│   ├── VoicePipeline            # 语音管道
│   ├── VoiceWorkflow            # 语音工作流
│   ├── PipelineConfig           # 管道配置
│   ├── OpenAISTT                # 语音转文字
│   └── OpenAITTS                # 文字转语音
│
├── tracing/                     # 追踪系统
│   ├── trace()                  # 创建追踪
│   ├── Trace / Span             # 追踪/跨度
│   ├── TracingProcessor         # 处理器接口
│   └── SpanData                 # 跨度数据
│
├── models/                      # 模型适配
│   ├── OpenAIResponsesModel     # Responses API（默认）
│   ├── OpenAIChatCompletionsModel  # Chat Completions API
│   ├── OpenAIProvider           # OpenAI Provider
│   ├── MultiProvider            # 多 Provider
│   ├── LiteLLMModel             # LiteLLM 100+ LLMs
│   └── AnyLLMModel             # Any-LLM 适配
│
├── prompts/                     # 提示词系统
│   └── PromptTemplate           # 模板化指令
│
├── visualization/               # 可视化
│   └── draw_graph()             # Agent 图形可视化
│
└── repl/                        # 交互式 REPL
    └── run_demo_loop()          # 调试工具
```

### 2.3 核心类 API 签名

#### Agent 类（核心）

```python
class Agent:
    name: str                              # Agent 名称（必填）
    instructions: str | Callable           # 系统指令（支持动态）
    model: str | Model = "gpt-4.1"         # 使用的模型
    tools: list[Tool] = []                 # 工具列表
    handoffs: list[Agent | Handoff] = []   # 可切换的 Agent
    input_guardrails: list[InputGuardrail] = []   # 输入防护
    output_guardrails: list[OutputGuardrail] = [] # 输出防护
    output_type: type | None = None        # 结构化输出类型（Pydantic）
    hooks: AgentHooks | None = None        # 生命周期钩子
    model_settings: ModelSettings = ModelSettings()  # 模型参数
    tool_use_behavior: ToolUseBehavior = "run_llm_again"  # 工具后行为

    def clone(self, **kwargs) -> Agent:    # 克隆并覆盖参数
```

#### Runner 类（执行器）

```python
class Runner:
    @staticmethod
    async def run(
        agent: Agent,
        input: str | list[dict],           # 用户输入
        *,
        context: Any = None,               # 自定义上下文
        session: Session | None = None,    # 会话持久化
        max_turns: int = 10,               # 最大轮次
        run_config: RunConfig | None = None,
    ) -> RunResult: ...

    @staticmethod
    def run_sync(agent, input, **kwargs) -> RunResult: ...  # 同步版本

    @staticmethod
    async def run_streamed(agent, input, **kwargs) -> RunResultStreaming: ...  # 流式版本
```

#### RunResult 结果

```python
class RunResult:
    final_output: str | T       # 最终输出（可为结构化类型）
    last_agent: Agent           # 最后执行的 Agent
    new_items: list[RunItem]    # 本次运行产生的所有项
    input: str | list[dict]     # 原始输入
    raw_responses: list         # 原始 API 响应
    guardrail_results: list     # 防护结果
    context_wrapper: RunContextWrapper
```

### 2.4 八层渐进式完整 Demo

#### Level 1：单 Agent + 自定义工具

```python
from agents import Agent, Runner, function_tool

@function_tool
def get_weather(city: str) -> str:
    """获取城市天气"""
    return f"{city}: 晴天, 25°C"

@function_tool
def search_flights(origin: str, destination: str, date: str) -> str:
    """搜索航班"""
    return f"{origin}→{destination} on {date}: ¥1200起"

agent = Agent(
    name="Travel Assistant",
    instructions="你是旅行助手。使用工具帮助用户规划旅行。",
    model="gpt-4.1-mini",
    tools=[get_weather, search_flights],
)

result = Runner.run_sync(agent, "我想下周去东京旅行，帮我查一下天气和航班")
print(result.final_output)
```

#### Level 2：多 Agent Handoff（路由分发）

```python
from agents import Agent, Runner

chinese_agent = Agent(
    name="Chinese Support",
    instructions="你是中文客服。用中文回答所有问题。",
    model="gpt-4.1-mini",
)

english_agent = Agent(
    name="English Support",
    instructions="You are English support. Answer in English.",
    model="gpt-4.1-mini",
)

triage_agent = Agent(
    name="Triage",
    instructions="""你是客服路由。根据用户使用的语言：
    - 中文 → 转给 Chinese Support
    - 英文 → 转给 English Support""",
    handoffs=[chinese_agent, english_agent],
)

result = Runner.run_sync(triage_agent, "请问你们的退货政策是什么？")
print(f"最终由 {result.last_agent.name} 处理")
print(result.final_output)
```

#### Level 3：Agents-as-Tools（层级委托）

```python
from agents import Agent, Runner

researcher = Agent(
    name="Researcher",
    instructions="深入研究给定主题，返回详细的研究报告。",
    model="gpt-4.1",
)

writer = Agent(
    name="Writer",
    instructions="将研究报告改写为通俗易懂的博客文章。",
    model="gpt-4.1",
)

# Manager 将 researcher 和 writer 作为工具使用
manager = Agent(
    name="Project Manager",
    instructions="""你是项目经理。对于用户请求：
    1. 先让 Researcher 做深度研究
    2. 再让 Writer 将研究成果写成文章""",
    tools=[
        researcher.as_tool(
            tool_name="deep_research",
            tool_description="进行深度主题研究",
        ),
        writer.as_tool(
            tool_name="write_article",
            tool_description="将内容改写为博客文章",
        ),
    ],
)

result = Runner.run_sync(manager, "写一篇关于量子计算最新进展的博客")
```

#### Level 4：Guardrails + 结构化输出

```python
from pydantic import BaseModel
from agents import Agent, Runner, InputGuardrail, GuardrailFunctionOutput

class ReviewOutput(BaseModel):
    """结构化输出"""
    summary: str
    sentiment: str  # positive / negative / neutral
    score: float    # 0.0 - 1.0
    key_points: list[str]

async def check_for_pii(ctx, agent, input) -> GuardrailFunctionOutput:
    """防护：检测个人信息"""
    pii_keywords = ["身份证", "银行卡", "密码"]
    has_pii = any(k in str(input) for k in pii_keywords)
    return GuardrailFunctionOutput(
        output_info={"has_pii": has_pii},
        tripwire_triggered=has_pii,
    )

review_agent = Agent(
    name="Review Analyzer",
    instructions="分析产品评论，返回结构化分析结果。",
    output_type=ReviewOutput,           # 结构化输出
    input_guardrails=[
        InputGuardrail(guardrail_function=check_for_pii),
    ],
)

result = Runner.run_sync(review_agent, "这款手机拍照效果很好，但电池续航不行")
review: ReviewOutput = result.final_output_as(ReviewOutput)
print(f"情感: {review.sentiment}, 评分: {review.score}")
```

#### Level 5：Session 持久化 + 多轮对话

```python
from agents import Agent, Runner
from agents.extensions.memory import SQLAlchemySession

# 创建持久化 Session
session = SQLAlchemySession(
    "sqlite:///my_agent.db",  # 也支持 PostgreSQL
    session_id="user_12345",
)

agent = Agent(
    name="Memory Bot",
    instructions="你是有记忆的助手。记住用户之前告诉你的信息。",
)

# 第一轮对话
result1 = await Runner.run(agent, "我叫王小明，我喜欢Python", session=session)

# 第二轮对话（自动恢复历史）
result2 = await Runner.run(agent, "我叫什么名字？", session=session)
print(result2.final_output)  # "你叫王小明"
```

#### Level 6：MCP 工具集成

```python
from agents import Agent, Runner
from agents.mcp import MCPServerStdio, MCPServerSse

# stdio 方式连接 MCP Server
filesystem_server = MCPServerStdio(
    name="filesystem",
    params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp/workspace"],
    },
)

# SSE 方式连接远程 MCP Server
github_server = MCPServerSse(
    name="github",
    params={"url": "http://localhost:3001/sse"},
)

agent = Agent(
    name="MCP Agent",
    instructions="使用文件系统和 GitHub 工具完成任务。",
    mcp_servers=[filesystem_server, github_server],
)

# MCP Server 的工具会自动注册到 Agent
async with filesystem_server, github_server:
    result = await Runner.run(agent, "列出 /tmp/workspace 下的所有文件")
```

#### Level 7：Streaming 流式输出

```python
from agents import Agent, Runner

agent = Agent(name="Storyteller", instructions="你是故事讲述者。")

# 流式运行
result = Runner.run_streamed(agent, "讲一个关于AI的故事")
async for event in result.stream_events():
    if event.type == "raw_response_event":
        # 实时输出每个 token
        if hasattr(event.data, 'delta'):
            print(event.data.delta, end="", flush=True)
    elif event.type == "agent_updated_stream_event":
        print(f"\n[Agent切换到: {event.new_agent.name}]")
    elif event.type == "run_item_stream_event":
        if event.item.type == "tool_call_item":
            print(f"\n[调用工具: {event.item.raw_item.name}]")
```

#### Level 8：Sandbox Agent + 长时编码任务

```python
from agents import Runner
from agents.run import RunConfig
from agents.sandbox import Manifest, SandboxAgent, SandboxRunConfig
from agents.sandbox.entries import GitRepo, Directory

agent = SandboxAgent(
    name="Code Assistant",
    instructions="""你是高级编码助手。
    在沙箱中检查代码、运行测试、修复bug。
    完成后提交一个清晰的 commit。""",
    default_manifest=Manifest(
        entries={
            "project": GitRepo(repo="user/my-project", ref="main"),
            "docs": Directory(path="/shared/docs"),
        }
    ),
)

result = await Runner.run(
    agent,
    "检查项目中的所有测试，修复失败的测试，然后提交修改",
    run_config=RunConfig(
        sandbox=SandboxRunConfig(
            client=UnixLocalSandboxClient(),  # 或 DockerSandboxClient()
        ),
    ),
)
```

### 2.5 生命周期钩子（Lifecycle Hooks）

```python
from agents import Agent, AgentHooks

class MyHooks(AgentHooks):
    async def on_start(self, context, agent):
        print(f"Agent {agent.name} 开始执行")

    async def on_end(self, context, agent, output):
        print(f"Agent {agent.name} 完成，输出: {output[:50]}")

    async def on_handoff(self, context, agent, source):
        print(f"从 {source.name} 切换到 {agent.name}")

    async def on_tool_start(self, context, agent, tool):
        print(f"调用工具: {tool.name}")

    async def on_tool_end(self, context, agent, tool, result):
        print(f"工具 {tool.name} 返回: {result[:50]}")

agent = Agent(
    name="Observable Agent",
    instructions="...",
    hooks=MyHooks(),
)
```

### 2.6 动态指令（Dynamic Instructions）

```python
from agents import Agent, RunContextWrapper

def dynamic_instructions(
    context: RunContextWrapper[MyContext],
    agent: Agent,
) -> str:
    user = context.context.user_name
    role = context.context.user_role
    return f"""你是 {user} 的专属助手。
    用户角色: {role}
    当前时间: {context.context.current_time}
    请根据用户角色调整你的回答风格。"""

agent = Agent(
    name="Personalized Agent",
    instructions=dynamic_instructions,  # 每次运行动态生成
)
```

### 2.7 Human-in-the-Loop

```python
from agents import Agent, Runner

agent = Agent(
    name="Careful Agent",
    instructions="执行前确认用户意图。",
    tools=[delete_file],  # 危险操作
)

# 拦截工具调用，要求人工确认
result = await Runner.run(
    agent,
    "删除 /tmp/important.txt",
    run_config=RunConfig(
        tool_approval_function=my_approval_callback,  # 人工审批回调
    ),
)
```

### 2.8 多 Provider（使用非 OpenAI 模型）

```python
from agents import Agent, Runner
from agents.extensions.models.litellm_model import LiteLLMModel

# 使用 Anthropic Claude
agent = Agent(
    name="Claude Agent",
    instructions="...",
    model=LiteLLMModel(model="anthropic/claude-sonnet-4-20250514"),
)

# 使用 Google Gemini
agent2 = Agent(
    name="Gemini Agent",
    instructions="...",
    model=LiteLLMModel(model="gemini/gemini-2.5-flash"),
)

# 混合使用：不同 Agent 用不同模型
result = Runner.run_sync(agent, "Compare yourself with GPT-4")
```

### 2.9 Agent 可视化 & REPL 调试

```python
# 可视化 Agent 图
from agents import draw_graph
draw_graph(triage_agent)  # 输出 Mermaid 图

# 交互式 REPL 调试
from agents import run_demo_loop
await run_demo_loop(agent)  # 启动命令行交互
```

---


## 3. 多Agent协调与Orchestration

### 支持的编排模式

| 模式 | 实现方式 | 适用场景 |
|------|----------|----------|
| **路由分发** | Handoff（triage agent → specialist agents） | 客服系统、多语言路由 |
| **层级委托** | Agents-as-Tools（manager → workers） | 研究报告、代码审查 |
| **流水线** | 串联 Runner.run（output_a → input_b） | 数据处理管道 |
| **并行执行** | 开发者自行 asyncio.gather | 信息收集、多源搜索 |

### 关键设计决策：去中心化 Handoff

Agents SDK 选择了**去中心化的 Handoff 模式**而非中心化的 Orchestrator 模式。每个 Agent 自行决定是否 handoff，没有全局的"导演"Agent。这使得系统更灵活，但也意味着**没有内建的 DAG/工作流引擎**。

---

## 4. 执行环境与工具集成（Hands层）

### 工具类型

| 类型 | 描述 | 示例 |
|------|------|------|
| **Function Tool** | 普通 Python 函数 | `@function_tool` 装饰器 |
| **MCP Server** | Model Context Protocol 服务器 | `MCPServerStdio(...)` |
| **Hosted Tools** | OpenAI 平台托管工具 | Code Interpreter, File Search |
| **Agent-as-Tool** | 将 Agent 包装为工具 | `agent.as_tool(...)` |

### Codex CLI 沙箱策略

> **安装**: `npm i -g @openai/codex` 或 `brew install --cask codex`

| 平台 | 沙箱技术 | 隔离级别 |
|------|----------|----------|
| macOS | Seatbelt 框架 | 系统调用级 |
| Linux/WSL2 | Bubblewrap | 容器级 |
| Windows | PowerShell 沙箱 | 进程级 |

### Codex CLI 审批模式

| 模式 | 文件读取 | 文件写入 | 命令执行 | 网络 |
|------|----------|----------|----------|------|
| `read-only` | ✅ | 需审批 | 需审批 | ❌ |
| `workspace-write`（默认） | ✅ | ✅(工作区) | ✅(常规) | ❌ |
| `danger-full-access` | ✅ | ✅ | ✅ | ✅ |

---

## 5. 记忆、状态与持久化

### Sessions（v0.13.0+）

- **SQLAlchemy Session**（默认）：支持 SQLite/PostgreSQL 等多数据库
- **Advanced SQLite Session**：高级本地存储
- **Encrypted Session**：加密存储
- **Redis Session**：分布式共享（需安装 `openai-agents[redis]`）
- **自定义 Session Store**：实现 `SessionStore` 接口

### 核心局限

- ⚠️ Sandbox Agent 新增了 **Agent Memory**（文件系统级持久记忆），但非语义记忆
- ❌ 无内建长期语义记忆（跨 session 知识提取）
- ❌ 无向量搜索（语义检索历史）
- ❌ 无 Context Compaction（上下文窗口管理需自行处理）

---

## 6. 安全、治理与企业特性

| 能力 | 状态 | 说明 |
|------|------|------|
| Input/Output/Tool Guardrails | ✅ | 三层防护 |
| Sandbox 隔离 | ✅ | Sandbox Agent + Codex |
| Human-in-the-Loop | ✅ | 内建审批 |
| Tracing | ✅ | OpenAI Dashboard |
| OAuth/身份管理 | ❌ | 不提供 |
| RBAC | ❌ | 不提供 |
| 合规审计 | ❌ | 无SOC2平台支持 |

---

## 7. 性能、成本与生产就绪度

| 维度 | 评分 | 说明 |
|------|------|------|
| 稳定性 | ⭐⭐⭐⭐ | v0.16.1，96个Release |
| 文档质量 | ⭐⭐⭐⭐ | MkDocs 完善 |
| 社区活跃度 | ⭐⭐⭐⭐⭐ | 26k Stars |
| 企业支持 | ⭐⭐ | 无专门企业版 |
| 可观测性 | ⭐⭐⭐⭐ | 内建 Tracing |

- **SDK免费**（MIT License）
- **成本 = 模型API费用 + Hosted Tools费用**

---

## 8. 集成与生态

- **模型**：OpenAI / Anthropic / Google / Mistral（via LiteLLM 100+）
- **工具**：MCP 生态 / Function Tools / Hosted Tools
- **观测**：OpenAI Dashboard / Langfuse / Braintrust
- **存储**：SQLite / Redis / SQLAlchemy
- **语言**：Python + JS/TS
- **沙箱**：本地Unix / 容器 / Codex CLI

---

## 9. 适用场景（优势）与局限性

### ✅ 最佳场景
- 客服路由/多Agent分诊（Handoff 天然适合）
- 快速原型验证（极简API）
- 多Provider对比测试（LiteLLM 100+ LLM）
- 编码助手（Codex CLI + Sandbox Agent）

### ❌ 核心局限
- 无内建工作流引擎（复杂DAG需自行实现）
- 无托管运行时（需自己管理部署/伸缩）
- 无长期记忆（跨session知识丢失）
- 无内建并行Agent执行
- Handoff 单向性（不支持"完成后返回"）

---

## 10. 演进路线与未来

```
v0.1.0 (2025-03)  → 核心 Agent + Handoff + Runner
v0.6.0 (2025-06)  → MCP 集成 + 多Provider支持
v0.10.0 (2025-09) → Sessions + Human-in-the-Loop
v0.13.0 (2025-12) → Guardrails 三层体系
v0.14.0 (2026-01) → Sandbox Agent (重大创新)
v0.15.0 (2026-03) → Realtime Voice Agent
v0.16.1 (2026-05) → 当前最新版
```

**未来方向**：Sandbox成熟化 → A2A协议支持 → 内建工作流原语 → 企业安全层 → Hosted Agent Runtime

---

## 参考引用

1. **OpenAI Agents SDK GitHub 仓库** — `openai/openai-agents-python`, https://github.com/openai/openai-agents-python （v0.16.1, 26k+ Stars, MIT License）
2. **OpenAI Agents SDK 官方文档** — https://openai.github.io/openai-agents-python/ （MkDocs 站点，覆盖 Agent/Handoff/Guardrail/Tracing/Session/MCP 等全部模块）
3. **OpenAI Codex CLI GitHub 仓库** — `openai/codex`, https://github.com/openai/codex （Rust 实现, Apache 2.0 License）
4. **OpenAI 官方博客: "Introducing the Agents SDK"** — https://openai.com/index/new-tools-for-building-agents/ （2025-03, Agents SDK 发布公告）
5. **Handoff 机制文档** — https://openai.github.io/openai-agents-python/handoffs/ （Handoff 原语的设计原理与 `transfer_to_<agent>` 内部实现）
6. **Guardrails 文档** — https://openai.github.io/openai-agents-python/guardrails/ （三层防护体系：Input/Output/Tool Guardrails, Tripwire 机制, 并行/阻塞模式）
7. **Tracing 文档** — https://openai.github.io/openai-agents-python/tracing/ （内建 trace/span 体系, Langfuse/Braintrust 第三方集成）
8. **Sandbox Agents 文档** — https://openai.github.io/openai-agents-python/sandbox-agents/ （v0.14.0+, Manifest 声明式环境, UnixLocalSandboxClient）
9. **Sessions 文档** — https://openai.github.io/openai-agents-python/sessions/ （SQLite/Redis Session Store, v0.13.0+）
10. **LiteLLM 多 Provider 集成** — https://openai.github.io/openai-agents-python/models/litellm/ （支持 100+ LLM Providers）
11. **Codex CLI Seatbelt/Bubblewrap 沙箱设计** — https://github.com/openai/codex/blob/main/codex-rs/README.md （macOS Seatbelt, Linux Bubblewrap, Windows PowerShell 沙箱策略）
12. **UI Bakery: "OpenAI Agents SDK Tutorial"** — https://uibakery.io/blog/openai-agents-sdk （SDK 架构概览与使用教程）
13. **CodeSignal: "Multi-Agent Handoffs"** — https://codesignal.com/blog/multi-agent-handoffs-openai （Handoff 模式深度解析）
14. **Towards Data Science: "Guardrails in OpenAI Agents SDK"** — https://towardsdatascience.com/ （Tripwire 机制与安全最佳实践分析）
15. **Analytics Vidhya: "Building AI Agents with OpenAI"** — https://analyticsvidhya.com/ （Agent 构建实践指南）
16. **Aurelio AI: "Tracing and Observability"** — https://aurelio.ai/ （OpenAI Agents SDK Tracing 深度教程）
17. **Langfuse: "OpenAI Agents SDK Integration"** — https://langfuse.com/ （第三方观测平台与 OpenAI SDK 的 OpenTelemetry 集成方案）
18. **Sid Bharath Blog: "Agent Frameworks Compared"** — https://sidbharath.com/ （多 Agent 框架横向对比分析）
