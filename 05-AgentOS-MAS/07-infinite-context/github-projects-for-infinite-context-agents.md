# 强模型、无限上下文与超薄 Harness 下的 GitHub 爆款项目机会

日期：2026-05-13  
假设窗口：未来 4 个月，即 2026-05-13 至 2026-09-13

## 核心判断

如果未来 4 个月真的出现“超级强模型 + 近似无限上下文 + harness 极薄”，那么不应该再做一个 AutoGPT、LangGraph、CrewAI、OpenHands 式的通用 agent 框架。

这层会被模型厂商、IDE、云平台和模型本身快速吞掉。真正值得提前布局的是 agent 时代的操作系统周边能力：

- 上下文治理
- 安全沙箱
- 审计回放
- 权限与凭证隔离
- 自动验收与评测
- 多 agent 协作
- 可复现交付
- MCP、skills、工具供应链

一句话：未来最值钱的开源项目不是“更聪明的 agent”，而是让超级 agent 可控、可查、可复现、可交付的基础设施。

## 观点依据

近期一线趋势基本指向同一个方向：

- Sam Altman 已把 agent 进入劳动力作为明确方向。
- Google 从 Gemini 1.5 的百万 token 长上下文推进到 Gemini 2.0 的 agentic era。
- OpenAI Codex 和 Agents SDK 正在把 sandbox、文件、工具、追踪能力产品化。
- Anthropic Managed Agents 明确提出把 brain、hands、session 解耦，并强调 session log、sandbox、安全边界。
- Anthropic context engineering 进一步说明，agent 成败关键不是单纯 prompt，而是上下文的选择、组织、压缩和工具反馈。
- Andrej Karpathy 的 Software 3.0 观点说明，LLM 更像一种新操作系统，而不是普通 API。

参考来源：

- Sam Altman, Reflections: https://blog.samaltman.com/reflections
- Google Gemini 1.5: https://blog.google/innovation-and-ai/products/google-gemini-next-generation-model-february-2024/
- Google Gemini 2.0: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/google-gemini-ai-update-december-2024/
- OpenAI Codex: https://openai.com/index/introducing-codex/
- OpenAI Agents SDK 2026: https://openai.com/index/the-next-evolution-of-the-agents-sdk/
- Anthropic Managed Agents: https://www.anthropic.com/engineering/managed-agents
- Anthropic context engineering: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Andrej Karpathy, Software Is Changing Again: https://rosetta.to/u/ycombinator/andrej-karpathy-software-is-changing-again

## 值得提前布局的 GitHub 爆款项目

| 项目方向 | 爆款理由 | 技术难度 | 商业价值 | 相对现有 agent 项目的差异化 |
|---|---|---:|---:|---|
| `agent-blackbox`：agent 飞行记录仪 | 记录每次 LLM 调用、工具调用、shell、diff、截图、审批、测试结果，可回放、脱敏、导出 | 中高 | 很高 | 不是 agent 框架，而是所有 Claude Code、Codex、OpenHands、Cursor 的审计层 |
| `contextfs`：无限上下文文件系统 | repo、docs、issue、Slack、PR、运行轨迹统一成可查询、可引用、可恢复的上下文对象 | 高 | 很高 | 无限上下文后，RAG 不再是核心，核心变成 provenance、权限、相关性、上下文治理 |
| `hands-kernel`：agent sandbox/权限内核 | 标准化 `execute(name,input)->string`，支持容器、浏览器、手机、远程机器、MCP、凭证隔离 | 高 | 很高 | harness 变薄，但 hands 会变厚，安全执行层不会消失 |
| `agent-ci`：多模型 PR/issue 工厂 | 同一 issue 交给 Claude、Codex、Gemini、OpenHands 并行修复，跑测试，比较 patch，自动生成 PR | 中高 | 高 | 不是单 agent，而是 agent 作为 CI worker |
| `specbench`：规格到验收测试生成器 | 从 PRD、Figma、issue、API docs 生成 Playwright、API、unit、security 验收套件 | 中 | 很高 | 当前 agent 最大短板不是写代码，而是不知道 done 是什么 |
| `agent-patch-auditor`：AI PR 风险检测 | 检查 agent 生成代码的假测试、过度工程、破坏兼容、隐藏安全风险 | 中高 | 高 | 专门针对 agent failure modes，不是普通 code review |
| `mcp-skill-registry`：可信 MCP/Skills 注册表 | 给 MCP server 和 skills 做 manifest、安全扫描、权限说明、eval 分数、可复现实例 | 中 | 中高 | MCP/Skills 会爆炸，真正稀缺的是可信供应链 |
| `llm-native-docs`：面向 agent 的文档/仓库适配器 | 自动生成 `AGENTS.md`、`llms.txt`、命令式 docs、repo map、可复制 context pack | 中低 | 中 | Karpathy 说要重写基础设施让 LLM 可读，这是最低成本爆款入口 |
| `refactor-factory`：长程迁移/重构流水线 | React、Rails、Django、Python、Java 大版本迁移，自动拆任务、跑测试、分 PR | 高 | 很高 | 模型越强，越能处理大规模机械但脆弱的企业迁移 |

## 最推荐的 3 个方向

### 1. `agent-blackbox`

这是最容易做出 GitHub 爆款、也最容易商业化的方向。

强模型会让 agent 执行更多真实工作，但企业和开发者马上会问：

- 它到底看了什么？
- 它到底执行了什么？
- 它有没有泄露密钥？
- 它改了哪些文件？
- 它为什么选择这个方案？
- 它的输出能否回放？
- 它的行为能否作为审计证据？

可做成：

- 本地 CLI
- GitHub Action
- VS Code/Cursor/Claude Code wrapper
- OpenTelemetry exporter
- 企业审计 dashboard

MVP 形态：

```bash
agent-blackbox run -- claude "fix issue #42"
agent-blackbox open latest
agent-blackbox export --format sarif,jsonl,html
```

核心产物：

- `trace.jsonl`
- `tool-calls.json`
- `patch.diff`
- `screenshots/`
- `approval-log.json`
- `redaction-report.json`
- `replay.html`

### 2. `specbench`

这是 agent 编程真正落地的关键瓶颈。

当模型越来越会写代码，稀缺点会从“能不能生成代码”转向“怎么知道它真的完成了需求”。企业环境里，需求往往来自：

- GitHub issue
- Linear ticket
- PRD
- API 文档
- Figma
- Slack 讨论
- 老代码行为

`specbench` 的价值是把这些模糊需求转成验收标准和可执行测试。

MVP 形态：

```bash
specbench from issue 42
specbench generate --playwright --api --unit
specbench run --against ./candidate-branch
specbench report
```

核心能力：

- 需求抽取
- 验收标准生成
- 测试生成
- 测试覆盖差距说明
- 和 agent PR 绑定
- 报告可贴回 GitHub PR

### 3. `contextfs`

这是长期天花板最高的方向，但技术难度也最高。

如果上下文真的接近无限，传统 RAG 的价值会下降，但上下文治理的价值会上升。无限上下文不等于无限有效上下文，真正的问题会变成：

- 哪些上下文可信？
- 哪些上下文过期？
- 哪些上下文和当前任务相关？
- 哪些上下文来自敏感来源？
- agent 引用的上下文能不能追溯？
- 长任务中上下文状态如何恢复？

`contextfs` 可以把上下文变成一个文件系统或版本化对象存储。

MVP 形态：

```bash
contextfs mount ./repo
contextfs add github://org/repo/issues/42
contextfs add slack://team/channel/thread
contextfs pack --task "migrate auth to oauth"
contextfs cite --from trace.jsonl
```

核心对象：

- `ContextObject`
- `SourceRef`
- `PermissionPolicy`
- `Freshness`
- `Citation`
- `TaskPack`
- `SessionSnapshot`

## 这些项目的共同特征

1. **agent-neutral**  
   不绑定 Claude、OpenAI、Gemini 或某个 IDE。模型越强，项目越强。

2. **不和模型抢智能**  
   不再卖“我有更聪明的 agent loop”，而是卖执行、审计、验证、上下文和权限。

3. **GitHub 一眼可见 demo**  
   爆款项目必须能在 README 第一屏展示结果，例如：

   ```bash
   npx agent-blackbox run "fix issue #12"
   ```

   然后生成 trace、diff、测试报告。

4. **默认本地优先**  
   开发者先信本地 CLI，再接受 hosted 版。

5. **产物标准化**  
   例如 JSONL trace、sandbox manifest、context pack、eval report、`AGENTS.md`。

6. **商业化自然**  
   开源 CLI + GitHub App + 企业版审计、SSO、VPC、数据保留策略。

## 与现有 agent 项目的核心差异

当前爆款项目如 AutoGPT、OpenHands、AutoGen、LangGraph，主要围绕“如何编排 agent”。

但如果 harness 真的薄到十几行，编排层会快速商品化。新的机会不是再造大脑，而是构建 agent 时代的底层配套：

- `context substrate`：agent 到底看了什么、引用了什么、遗漏了什么。
- `execution substrate`：agent 在哪里安全运行、如何隔离凭证、如何恢复。
- `verification substrate`：agent 做完后怎么证明真的对。
- `collaboration substrate`：人如何审批、复盘、回放、接管。
- `supply-chain substrate`：工具、MCP、skills 如何可信安装和评分。

## 商业化排序

| 排名 | 项目 | 开源吸引力 | 企业付费意愿 | 实现速度 | 综合判断 |
|---:|---|---:|---:|---:|---|
| 1 | `agent-blackbox` | 高 | 很高 | 快 | 最值得先做 |
| 2 | `specbench` | 高 | 很高 | 中 | 最贴近真实 ROI |
| 3 | `contextfs` | 中高 | 很高 | 慢 | 长期天花板最高 |
| 4 | `agent-ci` | 高 | 高 | 中 | 适合 GitHub App 商业化 |
| 5 | `hands-kernel` | 中 | 很高 | 慢 | 偏基础设施，技术门槛高 |
| 6 | `mcp-skill-registry` | 高 | 中高 | 中 | 取决于 MCP 生态爆发速度 |
| 7 | `llm-native-docs` | 很高 | 中 | 快 | 最适合快速涨星 |
| 8 | `agent-patch-auditor` | 中高 | 高 | 中 | 可作为 `agent-blackbox` 子产品 |
| 9 | `refactor-factory` | 中 | 很高 | 慢 | 垂直场景商业价值高 |

## 建议路线

如果目标是 GitHub 爆款，建议先做：

1. `llm-native-docs` 或 `agent-blackbox` 的极简 MVP。
2. 用 Claude Code、Codex、OpenHands 作为第一批适配对象。
3. README 第一屏展示 before/after、trace 回放、生成报告。
4. 一周内做出可运行 demo。
5. 两周内接 GitHub Action。
6. 四周内做 hosted dashboard 或 GitHub App。

如果目标是长期公司化，建议先做：

1. `agent-blackbox`
2. 向 `specbench` 扩展
3. 再向 `contextfs` 扩展

这三者可以形成闭环：

- `contextfs` 决定 agent 看什么
- `agent-blackbox` 记录 agent 做什么
- `specbench` 验证 agent 做得对不对

## 最终结论

如果未来 4 个月模型能力真的快速跃迁，agent 框架本身会贬值，agent 基础设施会升值。

值得提前布局的不是“下一个 AutoGPT”，而是：

- agent 的黑盒记录仪
- agent 的上下文文件系统
- agent 的验收测试生成器
- agent 的安全执行内核
- agent 的可信工具供应链

优先级最高的是 `agent-blackbox`，因为它同时具备 GitHub 传播性、开发者刚需、企业合规价值和较短 MVP 路径。
