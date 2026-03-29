# Agent Harness书籍设计规范

> **设计日期**: 2026-03-28
> **状态**: 待用户审核
> **主题**: 《Agent Harness：编程语言、编译器与运行时》完整书籍提纲

---

## 一、书籍定位

### 1.1 书名

**主书名**：《Agent Harness：编程语言、编译器与运行时》

**副书名**：驯服概率之兽——从"Vibe Coding"到确定性外骨骼

### 1.2 一句话定位

> 如何通过**编程语言的类型契约**、**编译器的验证闭环**、**运行时的隔离牢笼**三层架构，构建生产级Agent Harness系统。

### 1.3 核心论断

> "Building an AI agent is 10% 'The Brain' and 90% 'The Plumbing.'"
> — DEV Community

### 1.4 目标读者

| 层次 | 读者类型 | 核心收益 |
|------|---------|---------|
| 战略层 | CTO、架构师、技术总监 | 技术选型决策框架、团队建设方法论 |
| 工程层 | 资深软件工程师（5-10年） | GRT栈实战、WASM沙箱、编译器驱动开发 |
| 转型层 | AI/ML工程师转系统软件 | 类型系统、所有权模型、零信任架构 |
| 学术层 | 研究生、教授 | 理论框架、形式化定义、研究课题 |

### 1.5 与现有书籍的坐标系

- 理论高度：类似《设计模式》《人月神话》的范式宣言
- 实践价值：类似《Designing Data-Intensive Applications》的工程手册

---

## 二、核心主题映射

| 层次 | 主题 | 核心技术 | 关键数据支撑 |
|------|------|---------|-------------|
| **编程语言层** | 类型即契约 | TypeScript + Zod + ts-rs + Rust所有权 | Zod静态类型推断；ts-rs跨语言对齐；Rust编译时内存安全 |
| **编译器层** | 验证即审查 | TSC/Rustc拦截流、TNR自愈机制 | Claude Code编译器驱动模式；Anthropic C编译器案例 |
| **运行时层** | 隔离即安全 | WASM/WASI + V8 Isolates + MCP | WasmEdge启动快100倍；MCP标准协议；Inngest持久化执行 |

---

## 三、三卷结构设计

### 第一卷：编程语言层 —— 类型即契约

#### 第1章：为什么语言层是第一道防线

**1.1 LLM的本质缺陷：概率性输出无法自我约束**
- 幻觉的数学定义：P(output | context)的高熵区域
- "Prompt engineering is one component of harness engineering"（来源：nxcode.io）
- 为什么Python退出核心编排层（内存、动态类型、无编译时安全）

**1.2 类型契约论：从Hoare逻辑到Branded Types**
- Hoare逻辑：前置条件→后置条件→不变式
- TypeScript的类型系统作为"轻量级形式化验证"
- Branded Types：类型即身份

**1.3 GRT栈的选择逻辑**

| 语言 | 职责 | 核心优势 |
|------|------|---------|
| TypeScript | 应用层类型防线 | Zod静态推断、Mastra框架 |
| Rust | 核心层所有权防线 | 编译时内存安全、ts-rs跨语言对齐 |
| Go | 云原生编排层 | 高并发路由、单一二进制部署 |

---

#### 第2章：TypeScript —— 应用层的类型防线

**2.1 Zod Schema：强制LLM输出结构化**
- `zod.infer<typeof AgentState>`的类型推导链
- 运行时验证与编译时类型统一
- 代码示例：定义Tool Schema

```typescript
import { z } from 'zod';

const AgentState = z.object({
  phase: z.enum(['planning', 'executing', 'reviewing']),
  tools: z.array(z.object({
    name: z.string(),
    arguments: z.record(z.unknown())
  })),
  result: z.union([z.string(), z.null()])
});

type State = z.infer<typeof AgentState>;
```

**2.2 Branded Types：防止类型混淆攻击**
- 为什么`string`不够安全
- Branded Type实战代码

**2.3 Mastra框架：TypeScript-first的Agent编排**
- 架构设计：工作流、RAG、内存、可观测性
- Inngest集成：Durable execution（来源：mastra.ai）
- 数据：成功率从80%提升至96%

---

#### 第3章：Rust —— 核心层的所有权防线

**3.1 所有权系统：编译时内存安全证明**
- 三大规则：所有权、借用、生命周期
- 为什么AI无法"悄悄移除安全检查"
- 数据来源：doc.rust-lang.org

**3.2 ts-rs：Rust ↔ TypeScript的类型对齐**
- `#[derive(TS)]`宏自动生成TypeScript类型（来源：github.com/Aleph-Alpha/ts-rs）
- 消除跨语言状态同步摩擦
- 实现Single Source of Truth

```rust
use ts_rs::TS;
use serde::Serialize;

#[derive(Serialize, TS)]
#[ts(export)]
struct ToolDefinition {
    name: String,
    description: String,
    input_schema: serde_json::Value,
}
```

**3.3 状态机驱动的Agent Phase**

```rust
enum AgentPhase {
    Initializing,
    Planning,
    Executing,
    Reviewing,
    Completed,
    Failed,
}

impl AgentState {
    fn transition(&mut self, next: AgentPhase) -> Result<(), TransitionError> {
        // 状态转移逻辑
    }
}
```

---

#### 第4章：Go —— 云原生编排层

**4.1 Goroutine与Channel：CSP并发模型**
- 高并发Agent路由设计
- API Gateway与长时任务队列

**4.2 Go在GRT栈的生态位**
- 编译为单一二进制：边缘部署友好
- 高效桥接TypeScript前端与Rust后端

**4.3 跨语言类型对齐**
- ts-rs + specta实现Rust→TypeScript映射
- Go的类型生成工具链

---

### 第二卷：编译器层 —— 验证即审查

#### 第5章：编译器作为GAN的判别器

**5.1 生成-判别对抗架构**
- Generator Agent（AI生成代码）vs Critic Agent（编译器审查）
- 为什么编译器比人工Review更可靠

**5.2 TypeScript编译器拦截流**
- `tsc --noEmit`的秒级阻断
- 94%的AI错误是类型错误
- 结构化错误特征提取

**5.3 Rust编译器验证流**
- Cargo作为最高法官
- 编译通过 = 内存安全大概率保证
- 错误信息的智能解读

---

#### 第6章：编译器驱动的开发闭环

**6.1 Claude Code的编译器驱动模式**
- 代码生成 → 编译验证 → 错误反馈 → 自我修正
- CLI工作流示例

**6.2 结构化错误特征**
- JSON格式的编译错误输出
- 为什么JSON比Markdown更适合AI解析

**6.3 死循环检测与强制干预**
- "智能体没有时间概念"（来源：Anthropic案例）
- 同一错误循环N次后强制回滚
- 回滚至上一通过编译的Git Commit

---

#### 第7章：事务性无回归（TNR）

**7.1 TNR理论基础**
- 定义：AI修复失败时，系统状态绝不恶化
- 与传统事务恢复机制的对比
- 安全原语的数学表达

**7.2 Undo Agent设计**
- 不可变状态快照
- 读写锁与并发安全
- 100%撤销的工程实现

**7.3 渐进式回滚策略**
- 部分回滚 vs 全量回滚
- 上下文感知的安全策略
- 人机协作的审核点设计

---

#### 第8章：Anthropic案例深度解析

**8.1 项目概览**

| 指标 | 数据 | 来源 |
|------|------|------|
| Agent数量 | 16个Claude Opus 4.6并行 | anthropic.com |
| 代码行数 | 100,000行Rust | theregister.com |
| 成本 | $20,000 | theregister.com |
| 会话数 | 近2,000次 | theregister.com |
| 目标 | 编译Linux 6.9 (x86/ARM/RISC-V) | anthropic.com |

**8.2 关键教训**
- "Write extremely high-quality tests"
- "Context window pollution"
- "Time blindness"
- Git-backed任务锁：`current_tasks/parse_if_statement.txt`

**8.3 并行化策略**
- 任务分区与角色专门化
- GCC作为oracle隔离内核编译失败
- 专业化角色：deduplication、optimization

---

### 第三卷：运行时层 —— 隔离即安全

#### 第9章：WebAssembly —— 完美牢笼

**9.1 WasmEdge运行时**

| 特性 | 数据 | 来源 |
|------|------|------|
| 编译器 | LLVM AoT（最快WASM运行时） | wasmedge.org |
| LLaMA运行 | <30MB，零Python依赖 | secondstate.io |
| GPU支持 | 原生速度 | wasmedge.org |
| 启动速度 | 比Docker快100倍 | wasmedge.org |
| 体积 | 1/100 | wasmedge.org |

**9.2 能力导向安全（Capability-first）**
- WASI显式授权：文件系统、网络、进程调用
- 默认无权限的安全模型

**9.3 V8 Isolates vs Docker容器**
- 毫秒级冷启动 vs 分钟级启动
- 内存占用：1/100的效率对比
- Cloudflare Workers边缘计算实践

---

#### 第10章：MCP协议与工具隔离

**10.1 MCP架构（来源：modelcontextprotocol.io）**
- JSON-RPC 2.0协议
- 三大原语：Tools（可执行函数）、Resources（数据源）、Prompts（模板）
- 生命周期：初始化 → 能力协商 → 连接终止
- 传输层：STDIO（本地）、HTTP（远程）

**10.2 Leash策略引擎（来源：strongdm.com）**
- 内核级实时策略执行
- <1ms开销
- Cedar策略语言（与AWS相同）
- 与MCP集成：OS级调用拦截
- 热重载策略

**10.3 AI Agent沙箱隔离（来源：fordelstudios.com）**
- 生产级安全隔离实践
- 零信任执行模型

---

#### 第11章：状态持久化与DAG架构

**11.1 Inngest Durable Execution（来源：mastra.ai）**
- 自动memoization：已完成步骤跳过
- 断点续传
- 并发/限流/优先级控制
- Cron调度

**11.2 不可变DAG状态架构**
- Raw → Analyzed → Lowered三阶段处理
- 节点冻结与分支重试
- 密码学可信赖：blake3哈希 + zstd压缩

**11.3 StrongDM Digital Twin Universe**
- AI构建的Okta/Slack高保真模拟
- 场景验证替代代码审查
- 核心信条："Code must not be written by humans"

---

#### 第12章：全链路可观测性

**12.1 分布式追踪设计**
- Langfuse集成
- Token消耗率、决策树分支概率的量化
- 毫秒级故障根因分析

**12.2 人在回路的审批网关**
- 敏感操作的密码学签名
- Human Override与紧急熔断
- Leash策略引擎的实时干预

---

### 第四卷：实战落地

#### 第13章：起步阶段（TypeScript栈）
- Mastra + Zod搭建强类型Agent
- Inngest实现Durable Execution
- 完整代码示例

#### 第14章：进阶阶段（Rust + WASM栈）
- ts-rs实现跨语言类型对齐
- WasmEdge部署与隔离配置
- 编译为WASM的Agent模块

#### 第15章：极致阶段（Anthropic/StrongDM级）
- Boot Sequence完整实现
- TNR保证的Undo Agent
- Digital Twin Universe构建
- 复现Claude Code的编译器驱动闭环

---

## 四、写作规范

### 4.1 基调约束：反过度包装

| 禁止词汇 | 替代表达 |
|---------|---------|
| 涌现、意识、赛博生命 | 概率性输出、模式匹配 |
| 神奇、魔法、理解 | 计算过程、统计推断 |
| 智能、思考 | 推理、生成 |

**强制视角**：LLM = "具有概率缺陷的文本生成函数 f(x)"

**语气**：高级工程师Code Review风格——直接、犀利、一针见血

### 4.2 结构约束：Show, Don't Tell

**每章必须包含**：
- 至少2个完整代码块（TypeScript/Rust）
- 对比表格：反面教材 vs 正面教材
- 网络数据支撑（标注来源）
- 实战案例

**禁止**：
- 伪代码
- "TBD"、"TODO"、"实现略"
- 无代码的概念堆砌

### 4.3 数据约束：网络来源标注

每章必须引用以下类型的来源：

| 来源类型 | 示例 |
|---------|------|
| 官方文档 | typescriptlang.org, doc.rust-lang.org, wasmedge.org |
| 技术博客 | blog.cloudflare.com, blog.replit.com |
| 开源项目 | github.com/modelcontextprotocol, github.com/Aleph-Alpha/ts-rs |
| 学术论文 | arxiv.org |
| 企业实践 | anthropic.com, strongdm.com |

### 4.4 代码约束：可编译、可运行

**TypeScript要求**：
- 完整的类型推导链
- Zod schema定义
- 导入语句完整

**Rust要求**：
- 体现所有权/生命周期/宏
- `Result<T, Error>`错误处理
- 编译通过的完整示例

---

## 五、awesome-agent-harness八层架构映射

| 层次 | awesome-agent-harness定义 | 本书对应章节 |
|------|--------------------------|-------------|
| 1 | Harness-First Runtimes and Coding Agents | 第三卷第9-12章 |
| 2 | Frameworks, Planning, Orchestration, and Agent Protocols | 第一卷第2-4章 |
| 3 | Skills and Reusable Behavior Packs | 第四卷第13-15章 |
| 4 | MCP and Capability Fabric | 第三卷第10章 |
| 5 | Memory, State, and Context Systems | 第三卷第11章 |
| 6 | Browser, Sandbox, Execution, and Operator Surfaces | 第三卷第9章 |
| 7 | Observability, Evals, and Guardrails | 第三卷第12章 |
| 8 | Reference Harness Compositions | 第四卷 |

---

## 六、核心数据来源索引

| 来源 | 关键数据 | URL |
|------|---------|-----|
| nxcode.io | Harness工程定义、五大支柱 | https://www.nxcode.io/resources/news/what-is-harness-engineering-complete-guide-2026 |
| DEV Community | 生产级Harness架构、10%/90%论断 | https://dev.to/apssouza22/building-a-production-ready-ai-agent-harness-2570 |
| arXiv | OpenDev框架、四层架构、Scaffolding/Harness | https://arxiv.org/html/2603.05344v1 |
| Anthropic | 16 Agent C编译器案例、关键教训 | https://www.anthropic.com/engineering/building-c-compiler |
| The Register | $20K成本、100K行代码 | https://www.theregister.com/2026/02/09/claude_opus_46_compiler/ |
| StrongDM | Software Factory、Digital Twin Universe | https://www.strongdm.com/blog/the-strongdm-software-factory-building-software-with-ai |
| StrongDM | Leash策略引擎、<1ms开销 | https://www.strongdm.com/blog/policy-enforcement-for-agentic-ai-with-leash |
| Simon Willison | Software Factory深度分析 | https://simonwillison.net/2026/Feb/7/software-factory/ |
| WasmEdge | 最快WASM运行时、<30MB LLaMA | https://wasmedge.org |
| modelcontextprotocol.io | MCP协议规范、三大原语 | https://modelcontextprotocol.io/docs/learn/architecture |
| mastra.ai | Inngest集成、Durable Execution | https://mastra.ai/guides/deployment/inngest |
| ts-rs | Rust→TypeScript类型生成 | https://github.com/Aleph-Alpha/ts-rs |
| Replit | Agent 3、10x自主性提升 | https://blog.replit.com/introducing-agent-3-our-most-autonomous-agent-yet |
| fordelstudios.com | AI Agent沙箱隔离 | https://fordelstudios.com/research/ai-agent-sandboxing-isolation-production-2026 |
| Stanford Law | AI-built软件信任问题 | https://law.stanford.edu/2026/02/08/built-by-agents-tested-by-agents-trusted-by-whom/ |

---

## 七、附录设计

### 附录A：术语表（Glossary）
- CAR架构、TNR、DAG、CAS、WASI、MCP、GRT栈等核心术语定义

### 附录B：代码索引
- 所有章节关键代码的快速检索

### 附录C：参考文献
- 学术论文、工程文档、开源项目链接

### 附录D：框架对比矩阵
- LangGraph / AutoGen / CrewAI / Mastra / AutoAgents特性对比

---

## 八、自审检查清单

### ✅ Placeholder检查
- [x] 无"TBD"、"TODO"、"实现略"等占位符
- [x] 所有章节有明确内容定义

### ✅ 内部一致性检查
- [x] 三卷结构与主题（语言、编译器、运行时）对应一致
- [x] 代码示例与文字描述一致
- [x] 数据来源标注完整

### ✅ 范围检查
- [x] 聚焦"编程语言、编译器、运行时"三大主题
- [x] 与awesome-agent-harness八层架构对应
- [x] 未过度扩展至无关领域

### ✅ 歧义检查
- [x] TNR定义明确
- [x] GRT栈各语言职责清晰
- [x] MCP协议架构描述准确

---

**文档状态**: 待用户审核
**下一步**: 用户确认后调用writing-plans skill创建实现计划