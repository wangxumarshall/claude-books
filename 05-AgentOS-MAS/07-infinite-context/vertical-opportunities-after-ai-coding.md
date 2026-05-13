# AI Coding 之后：强模型与无限上下文假设下的垂直场景创业机会

日期：2026-05-13  
假设窗口：未来 4 个月，即 2026-05-13 至 2026-09-13

## 核心判断

AI coding 是过去一年最成功的 AI 落地场景，不是因为“代码只是文本”，而是因为软件工程天然具备 agent 落地所需的完整闭环：

- 上下文：repo、issue、docs、PR 历史、CI 日志
- 执行环境：terminal、sandbox、browser、test runner
- 可验证工件：diff、unit test、E2E test、build result
- 人类 review：PR review、code owner、CI gate
- 版本控制：Git、branch、commit、rollback
- 高价值任务：bug fix、feature、migration、security remediation

因此，未来 4 个月如果模型能力持续增强，甚至出现近似无限上下文，下一个被攻克的不是所有白领工作，而是一批能被改造成 “GitHub-like workflow” 的垂直场景。

更具体地说，机会在于这些流程：

```text
业务上下文输入 -> agent 生成工件 -> 自动验证 -> 人类 review -> 合入业务系统
```

创业机会也不在于“给某行业套一个 ChatGPT”，而在于为某个高价值行业补齐 coding 已经拥有的基础设施：上下文、执行、验收、审计、回滚和协作。

## 模型与产品趋势

当前公开信号已经非常明确：

- GitHub Copilot 从补全工具进入 coding agent 阶段，支持从 issue 到 PR 的工作流。
- OpenAI Codex 把 coding agent 放入云端 sandbox，并强调安全执行和可审计轨迹。
- Anthropic Managed Agents 提出把 brain、hands、session 解耦，强调 sandbox、session log 和工具执行。
- Anthropic context engineering 指出，agent 成败不仅取决于模型，而取决于上下文如何被选择、组织、压缩和反馈。
- OpenAI GDPval 开始直接评估模型在真实专业工作上的表现。
- Microsoft Work Trend Index 把未来企业描述为由人类管理 agent 的 Frontier Firm。

如果未来 4 个月模型继续增强、上下文窗口继续扩大，瓶颈会从“模型会不会做”转移到：

- 是否有完整业务上下文
- 是否有安全执行环境
- 是否有可执行验收标准
- 是否有版本、审计与责任链
- 是否能自然嵌入现有业务系统

## 为什么 AI Coding 能先成功

| 要素 | Coding 里对应什么 | 外溢到其他行业时需要什么 |
|---|---|---|
| 长上下文 | repo、issue、docs、PR 历史 | 全量业务文档、历史案例、客户记录、系统日志 |
| 可执行环境 | terminal、tests、CI | sandbox、模拟器、业务系统测试环境 |
| 可验证工件 | diff、unit test、E2E test | 报告、合同、表格、配置、流程变更的验收器 |
| 人类 review | PR review | 审批流、审计流、专家签字 |
| 版本控制 | Git | 业务对象版本、证据链、回滚 |
| 高价值任务 | bug、feature、迁移、安全修复 | 专业服务、合规、财务、运营、销售工程 |

所以，判断一个垂直场景是否会被 AI 攻克，关键不是看它是否“文字很多”，而是看它是否能形成类似软件工程的闭环。

## 最可能被攻克的垂直场景

| 优先级 | 场景 | 为什么会被攻克 | 具体创业机会 |
|---:|---|---|---|
| 1 | QA、测试、验收 | 和 coding 最接近，有代码、需求、浏览器、CI，可自动验证 | `spec-to-test agent`：从 PRD、issue、Figma、API docs 自动生成 Playwright、API、unit 测试并维护 |
| 2 | AppSec、安全修复 | 漏洞报告结构化，修复可 PR 化，验证可用 SAST、DAST、PoC | `security remediation agent`：接 CodeQL、Snyk、Semgrep，自动复现、修复、开 PR、生成审计证据 |
| 3 | DevOps、SRE、云运维 | 有日志、metrics、runbook、Terraform、K8s 配置，可沙箱演练 | `incident-to-patch agent`：从告警到根因分析、临时缓解、配置 PR、复盘报告 |
| 4 | 数据工程、BI | SQL、dbt、Airflow、dashboard 都是代码化资产，验证可跑查询 | `analytics engineer agent`：自动修 pipeline、补 dbt tests、生成指标口径和 dashboard diff |
| 5 | 技术支持到工程闭环 | support ticket、日志、复现步骤、代码修复天然串联 | `support-to-PR agent`：从 Zendesk、Intercom ticket 定位 bug，复现，开修复 PR，回写客户回复 |
| 6 | 企业 SaaS 配置运维 | Salesforce、ServiceNow、NetSuite、Workday 配置复杂但可版本化 | `SaaS admin agent`：字段、流程、权限、报表、审批流自动配置，并生成变更审计 |
| 7 | 合规与审计 | SOC2、ISO、HIPAA、金融审计高度文档化、证据化 | `compliance evidence agent`：自动收集 GitHub、AWS、HRIS、Jira 证据，映射控制项，生成 auditor-ready package |
| 8 | 财务 FP&A、月结 | Excel、ERP、合同、发票、预算、variance analysis 长上下文密集 | `month-end close agent`：自动对账、异常解释、生成 CFO pack 和审计 trail |
| 9 | 法务合同、尽调 | 长文档、多版本、playbook、风险条款，长上下文提升明显 | `contract diligence agent`：批量 redline、风险矩阵、条款偏离、引用证据，不替代律师签字 |
| 10 | RFP、售前、安全问卷 | 公司知识库、产品文档、历史回答、客户需求都可检索和复用 | `RFP engineer agent`：自动回答安全问卷、生成 proposal、标注引用、发现缺失材料 |

## 最看好的 5 个创业切口

### 1. `SpecBench for Enterprise`

定位：从需求、设计稿、API 文档、历史 bug 自动生成验收测试。

这是 AI coding 之后最刚需的一层。模型越会写代码，企业越需要证明它真的完成了需求。

MVP：

```bash
specbench from github-issue 42
specbench add figma <url>
specbench generate --playwright --api --unit
specbench run --against ./candidate-branch
specbench report --github-pr
```

核心功能：

- 从 issue、PRD、Figma、API docs 抽取验收标准
- 自动生成 Playwright、API、unit 测试
- 对比实现和需求差距
- 把报告贴回 GitHub PR
- 随需求变化维护测试

商业价值：

- 降低 QA 成本
- 提高 agent coding 的可用性
- 适合按 repo、seat 或 CI usage 收费

### 2. `Support-to-PR`

定位：把客服系统、日志系统、GitHub/GitLab 接起来，让高频技术问题自动进入工程闭环。

目标不是替代客服，而是把客户问题转成：

- 复现步骤
- 相关日志
- 根因定位
- 修复 PR
- 回归测试
- 客户回复草稿

MVP：

```bash
support-pr ingest zendesk-ticket 123
support-pr reproduce
support-pr patch
support-pr open-pr
support-pr reply-draft
```

适合客户：

- API 公司
- DevTools 公司
- B2B SaaS
- 有大量技术支持 ticket 的平台型公司

商业价值：

- 缩短 ticket resolution time
- 把 support 数据反哺 engineering
- 减少重复 bug 的人工排查

### 3. `AI AppSec Remediator`

定位：安全扫描器很多，但企业真正缺的是可信修复。

典型流程：

```text
漏洞报告 -> 复现 -> 定位代码 -> 修复 -> 跑测试 -> 安全说明 -> PR -> 审计证据
```

MVP：

```bash
appsec-agent import codeql.sarif
appsec-agent reproduce
appsec-agent patch
appsec-agent verify
appsec-agent pr
```

核心能力：

- 接入 CodeQL、Snyk、Semgrep、Dependabot
- 自动理解漏洞和调用链
- 尝试生成 exploit 或验证脚本
- 修复代码并补测试
- 生成安全审计说明

商业价值：

- 安全团队预算明确
- 漏洞修复 backlog 长期存在
- 和 GitHub Advanced Security、Snyk、Wiz、Semgrep 生态兼容

### 4. `SaaS ConfigOps Agent`

定位：把 Salesforce、ServiceNow、NetSuite、Workday 等企业 SaaS 的配置变成可版本化、可 review、可回滚的工程流程。

这些系统的配置复杂度已经接近代码，但大多数企业还在用人工管理员和顾问。

MVP：

```bash
configops snapshot salesforce
configops plan "add approval flow for enterprise discount"
configops simulate
configops apply --approval
configops rollback
```

核心能力：

- 配置快照
- 自然语言到配置计划
- 变更 diff
- 权限影响分析
- 沙箱模拟
- 审批和回滚

商业价值：

- 企业愿意为减少顾问费用付费
- 配置错误会直接影响收入、权限和合规
- 可以从 Salesforce 这类单一生态切入

### 5. `Finance Close Agent`

定位：帮助财务团队完成月结、对账、预算差异分析和管理层报告。

这类工作长上下文密集，涉及：

- ERP
- 发票
- 合同
- 银行流水
- 预算模型
- Excel
- 历史解释
- 审计证据

MVP：

```bash
close-agent ingest erp
close-agent reconcile
close-agent explain-variance
close-agent generate-cfo-pack
close-agent export-audit-trail
```

关键边界：

- agent 起草和解释
- 人类财务负责人审批
- 不自动承担最终财务责任
- 强审计 trail

商业价值：

- 月结周期缩短
- FP&A 人力昂贵
- CFO 和 controller 对可靠自动化有明确需求

## 判断垂直场景是否适合创业的 7 个信号

| 信号 | 越强越适合创业 |
|---|---|
| 工件是否数字化 | 文档、表格、代码、配置、报告优先 |
| 是否有验收器 | test、lint、规则引擎、审计 checklist、模拟环境 |
| 是否有版本和回滚 | Git、配置版本、审批记录、变更日志 |
| 上下文是否分散且昂贵 | repo、CRM、ERP、Slack、合同、日志越多越适合 |
| 专家是否昂贵 | 工程、安全、法务、财务、合规、售前 |
| 风险能否人审 | agent 起草，人类批准 |
| 结果是否能直接进入系统 | PR、ticket、dashboard、contract、ERP entry |

## 不建议押的方向

以下方向在强模型和无限上下文假设下风险较高：

- 泛泛的“行业 ChatGPT”
- prompt marketplace
- 普通 RAG 知识库
- 通用 autonomous agent
- 只做聊天 UI 的垂直 SaaS
- 没有写回系统能力的 copilot
- 没有验收、审计、权限和回滚的自动化工具

原因是：如果无限上下文真的出现，单纯“能读很多文档”的产品会快速贬值。真正值钱的是上下文编排、工具执行、验收、审计和工作流闭环。

## 与 AI Coding 的类比

| AI Coding | 下一个垂直场景应该具备的对应物 |
|---|---|
| repo | 业务系统、文档库、历史案例、数据仓库 |
| issue | ticket、case、request、audit finding、alert |
| PR | 变更请求、配置 diff、报告草稿、合同 redline |
| CI | 规则引擎、测试环境、审计 checklist、财务校验 |
| code review | 专家审批、法务审批、财务审批、安全审批 |
| merge | 写回业务系统 |
| rollback | 版本恢复、配置回退、报告修订 |

这也是为什么最好的创业项目会像“某行业的 GitHub Actions + Copilot + PR workflow”，而不是像“某行业的聊天机器人”。

## 最终排序

未来 4 个月最可能出现创业爆点的不是纯法律、纯医疗、纯咨询，而是这些半软件、半业务的场景：

1. QA、验收测试
2. AppSec 修复
3. 技术支持到 PR
4. DevOps、SRE
5. 数据工程、BI
6. 企业 SaaS 配置
7. 合规审计证据
8. 财务月结、FP&A
9. 合同审查、尽调
10. RFP、售前工程

## 参考来源

- GitHub Copilot coding agent: https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/
- GitHub Octoverse 2025: https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typeScript-to-1/
- OpenAI Codex: https://openai.com/index/introducing-codex/
- OpenAI Codex app: https://openai.com/index/introducing-the-codex-app/
- OpenAI Running Codex safely: https://openai.com/index/running-codex-safely/
- OpenAI GDPval: https://openai.com/index/gdpval/
- Anthropic Managed Agents: https://www.anthropic.com/engineering/managed-agents
- Anthropic Context Engineering: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Microsoft Work Trend Index 2026: https://blogs.microsoft.com/blog/2026/05/05/how-frontier-firms-are-rebuilding-the-operating-model-for-the-age-of-ai/
- McKinsey State of AI 2025: https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai
