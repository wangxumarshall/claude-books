# Agent 场景文件系统：改造“文件系统语义层”和“工具访问接口”

---

## 0. 摘要

1. Agent 的真实文件系统问题不是单纯吞吐量问题，而是“可执行写入 + 不可信上下文 + 长轨迹 + 外部副作用 + 多主体协作”叠加后的安全性、可回放性、可审计性、回滚性和冲突控制问题。
2. 当前 POSIX 风格文件系统适合存储字节流、目录、权限位和 inode 元数据，但它不表达“哪个模型、基于什么上下文、通过哪个工具、在什么策略下，为什么写了这个文件”。Agent 场景恰好需要这些语义。
3. 因此，需要改造的是 agent-facing filesystem layer：受限命名空间、能力权限、事务化工作区、版本化提交、来源证明、操作轨迹、可回放审计和冲突检测。底层可以先复用 ext4/XFS/Btrfs/ZFS/F2FS/OverlayFS/FUSE 等成熟机制。
4. 只有当真实 agent 工作负载测量显示现有组合方案在延迟、写放大、快照成本、审计吞吐或并发提交上无法满足目标时，才应考虑内核文件系统或专用布局。

 **AgentFS**不“替代 Linux 文件系统”，而是一个面向 agent runtime、MCP server、IDE agent、CI agent 和多 agent 协作环境的文件系统语义层。最低目标是：让 agent 的文件读写变成可约束、可解释、可回滚、可审计、可合并、可重放的操作序列。

---

## 1. 研究边界与方法

### 1.1 本文所说的 Agent 场景

本文中的 agent 指满足以下条件的软件主体：

- 由 LLM 或类似模型驱动，能够根据上下文选择动作；
- 能调用工具，例如读写文件、执行命令、搜索代码、运行测试、调用 API；
- 会形成多步轨迹，而不是一次性输入输出；
- 可能在共享仓库、沙箱、CI、生产辅助环境或多 agent 工作区内运行。

这个定义有事实基础。ReAct 论文把推理和动作交错建模，agent 通过动作与外部环境交互并接收观察结果 [ReAct](https://arxiv.org/abs/2210.03629)。SWE-bench 将真实 GitHub issue / pull request 转化为需要修改代码并通过测试的任务，说明代码 agent 的典型环境是已有文件树和测试系统，而不是孤立文本问答 [SWE-bench](https://juanmirod.github.io/public/papers/swe-bench_2310.06770v3.pdf)。SWE-agent 进一步提供证据表明 agent-computer interface 会显著影响 agent 在软件工程任务中的表现，文件编辑接口不是中性的实现细节 [SWE-agent](https://papers.nips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf)。

### 1.2 本文所说的文件系统

本文把“文件系统”分成三层：

| 层级 | 例子 | Agent 相关性 |
|---|---|---|
| 物理布局层 | ext4、XFS、Btrfs、ZFS、F2FS、NILFS2 | 决定耐久性、快照、写放大、GC、崩溃恢复成本 |
| OS 语义层 | POSIX path、fd、rename、fsync、权限、锁、namespace | 决定工具如何读写、隔离、并发和恢复 |
| Agent 语义层 | workspace、trajectory、policy、provenance、commit、rollback、replay | 当前缺失最多，也是本文重点 |

本地报告主要讨论第一层。Agent 场景真正紧迫的问题主要在第二层和第三层。

### 1.3 证据分级

本文区分三类陈述：

- **事实**：来自论文、官方文档、标准或手册页。
- **工程推理**：由事实推出的可辩护设计判断。
- **假设**：需要真实 workload benchmark 验证，不能当作事实。

例如，“F2FS 使用 log-structured 思想、NAT、多头日志和 cleaning”是事实，依据 Linux kernel 文档 [F2FS](https://docs.kernel.org/filesystems/f2fs.html)。“AgentFS 可以把 trajectory log 放在 append-only backend 上”是工程推理。“所有 agent workload 都是写密集且适合 F2FS/LSM”是假设，目前证据不足。

---

## 2. 对本地报告的批判性评估

### 2.1 本地报告成立的部分

本地报告正确指出：log-structured 思想已经广泛影响文件系统、数据库和存储硬件。F2FS 是面向闪存的 log-structured 文件系统，ZFS/Btrfs/WAFL 使用 copy-on-write 思想，LSM-tree 在数据库层通过顺序写入和 compaction 提高写入效率。Linux F2FS 文档也明确讨论了 wandering tree、NAT、cleaning、多头日志和冷热数据分离 [F2FS](https://docs.kernel.org/filesystems/f2fs.html)。

这些事实对 AgentFS 有帮助，但它们不能直接推出“Agent 场景需要一个 log-structured filesystem”。

### 2.2 本地报告不够严格的部分

| 原推断 | 问题 | 更严格的表述 |
|---|---|---|
| Agent workload 写密集、追加为主 | 没有给出 workload 测量；不同 agent 任务差异巨大 | 某些轨迹、审计、事件日志是追加型；代码编辑、搜索、测试产物和依赖缓存不一定是 |
| Agent 数据粒度是向量/embedding/token | 向量库和 token cache 多数属于数据库/模型运行时，不是普通文件系统的核心抽象 | AgentFS 应能引用这些对象，但不应把 vector DB 伪装成 filesystem |
| TB-PB 是 Agent 的典型规模 | 对个人 coding agent、企业自动化 agent、移动端 agent 都不成立 | 规模需要按场景测量：本地 IDE、CI agent、企业平台、多租户训练/推理日志分别建模 |
| LSM + log-structured FS 是自然答案 | LFS cleaning 和 LSM compaction 都有写放大、尾延迟和空间放大 | Append-only 适合轨迹和审计，但 workspace mutation 需要事务、diff、merge 和快照 |
| 文件系统层提供多 agent 共享日志 | 共享日志是分布式系统问题，涉及一致性、租约、复制、故障检测 | 单机 FS 可提供本地 append log；跨机器多 agent 需要数据库/日志系统或共识协议 |

严格结论：本地报告适合作为“存储布局背景材料”，但不能作为 AgentFS 设计的直接论证。AgentFS 的第一性问题是语义和安全，不是磁盘布局。

---

## 3. Agent 面临的真实文件系统问题

### 3.1 问题一：Ambient authority 与路径逃逸

传统程序通常由开发者明确写出文件路径和权限边界。Agent 不同：它会根据上下文、模型输出和工具反馈动态决定要读写什么。如果 agent 拥有宿主目录的宽权限，错误推理、提示注入或恶意文件内容都可能诱导它读取 secret、覆盖无关文件或执行危险命令。

这不是理论风险。MCP filesystem server 的参考实现默认要求配置允许访问的目录，并把 read/write/list/delete/move/search 等能力限制在 allowed directories / roots 内 [MCP filesystem server](https://github.com/modelcontextprotocol/servers/blob/main/src/filesystem/README.md)。MCP 资源规范也要求 URI 验证、访问控制和权限检查，`file://` 资源即使表现得像文件系统，也不必映射到原始物理文件系统 [MCP Resources](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)。OWASP MCP Top 10 把 scope creep、command injection、context over-sharing、缺少审计遥测列为重要风险 [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/)。

Linux 已有底层工具，但不是 agent-native。Landlock 可以让非特权进程限制自身对文件层级的访问，并建议采用最小权限目录边界 [Landlock](https://cdn.kernel.org/doc/html/latest/userspace-api/landlock.html)。`openat2` 提供路径解析约束，例如限制路径不能逃出目录、处理 magic links 和 symlink 风险 [openat2](https://man7.org/linux/man-pages/man2/openat2.2.html)。这些机制说明问题真实存在，也说明 AgentFS 不必从零实现所有安全机制。

**推理结论**：AgentFS 必须默认是 capability-scoped filesystem。路径字符串不能直接等于权限；权限应绑定到工作区、动作类型、路径前缀、数据等级和任务目的。

### 3.2 问题二：多文件修改缺少 agent 级事务

Coding agent 常常一次任务修改多个文件：源码、测试、配置、文档、lockfile。POSIX 提供单个文件 rename 的原子替换语义，但不提供跨文件、跨目录、带 read-set/write-set 的 agent 级事务。程序可以自己用临时文件、rename、fsync 和 journal 实现，但每个 agent 工具都重复实现，会留下崩溃一致性和部分提交风险。

崩溃一致性不是小问题。文件系统 crash-consistency 研究显示，很多成熟文件系统中的 bug 可以用很小的、围绕 `fsync` 的 workload 复现，并且研究还发现了新的文件系统 bug [Crash consistency study](https://arxiv.org/abs/1810.02904)。这说明“写文件后程序没报错”不等于“agent 的多步修改具备可恢复提交语义”。

**推理结论**：AgentFS 需要 `begin_transaction -> propose changes -> validate preconditions -> commit/abort`。提交应生成一个可审计 commit object；崩溃后只能看到 commit 前或 commit 后状态，不能看到半套 agent 修改。

### 3.3 问题三：缺少因果 provenance

普通文件系统记录 owner、mode、mtime、ctime、size、xattr 等元数据，但这些元数据不能回答 agent 场景的核心问题：

- 哪个 agent 写了这个文件？
- 使用了哪个模型、工具版本、系统提示、用户请求和检索上下文？
- 写入前看过哪些文件？
- 哪个测试或审查结论支持这个变更？
- 这个产物能不能用于训练、复制、外发或生产？

W3C PROV 把 provenance 定义为关于实体、活动和参与者的信息，用于评估数据质量、可靠性和可信度 [W3C PROV-DM](https://www.w3.org/TR/prov-dm/)。CISA/NSA/FBI 等机构发布的 AI 数据安全指南也建议跟踪数据 provenance、使用安全存储、签名和完整性措施来保护 AI 系统生命周期中的数据 [AI Data Security Guidance](https://www.fbi.gov/file-repository/cyber-alerts/ai-data-security-best-practices-for-securing-data-used-to-train-and-operate-ai-systems-052225.pdf)。

**推理结论**：AgentFS 应把每次 agent 写入建模为 provenance graph 的一部分。文件内容、工具动作、模型调用、测试结果和人工批准都应有可关联的 ID。

### 3.4 问题四：长轨迹难以回放和调试

ReAct 类 agent 的状态不是一个 final answer，而是 action/observation 轨迹 [ReAct](https://arxiv.org/abs/2210.03629)。SWE-agent 类 coding agent 还会读文件、编辑文件、运行命令、观察测试失败、再次修改。失败发生后，仅靠最终 diff 和 shell history 很难回答：哪一步误读了上下文？哪个工具输出被截断？哪个文件版本被用于推理？

OpenTelemetry 已经把 trace 建模为 span、event、attribute 等结构，用来观察分布式系统行为 [OpenTelemetry Traces](https://opentelemetry.io/docs/concepts/signals/traces/)。AgentFS 不需要重新发明观测模型，但需要把文件操作纳入这种 trace：每次 read、write、patch、rename、delete、commit、rollback、test result 都应可挂接到同一条 agent trace。

**推理结论**：AgentFS 的 operation log 应同时服务于审计、调试、回放和安全检测。单纯保存最终文件树不够。

### 3.5 问题五：并发 agent 的冲突不是 advisory lock 能解决的

Linux 文件锁主要是 advisory。手册页说明，普通 advisory lock 只有在协作进程遵守协议时才有效；mandatory locking 在 Linux 上长期不可靠、使用少，并且已被移除支持 [fcntl locking](https://man7.org/linux/man-pages/man2/fcntl_locking.2.html)。多 agent 协作时，冲突常常不是“两个进程同时写同一 inode”这么简单，而是语义冲突：一个 agent 修改 API，另一个 agent 修改调用点；两个 agent 都改 package lock；一个 agent 删除了另一个 agent 刚引用的测试 fixture。

**推理结论**：AgentFS 需要版本向量或 MVCC 风格的 read-set/write-set 检测，提交时按内容版本和路径版本做 optimistic concurrency control。锁只能作为性能优化或短临界区工具，不能作为核心一致性模型。

### 3.6 问题六：快照、回滚和隔离成为日常路径

Agent 的典型工作流包括探索、试错、运行测试、回滚、重试。底层已有机制可以支持这类需求：Btrfs 的 subvolume/snapshot 使用 COW 共享 root block，之后的变更私有化，并支持只读快照 [Btrfs design](https://btrfs.readthedocs.io/en/stable/dev/dev-btrfs-design.html)。OverlayFS 可以把 lower/upper/workdir 组合成叠加视图，适合创建临时可写工作区，但它有 backing filesystem 要求和 xattr 限制，不是完整 provenance 系统 [OverlayFS](https://docs.kernel.org/filesystems/overlayfs.html)。FUSE 可以让用户态进程实现文件系统接口，但内核文档同时提醒权限、拒绝服务、信息泄漏和死锁风险 [FUSE](https://www.kernel.org/doc/html/latest/filesystems/fuse/fuse.html)。

**推理结论**：AgentFS 应把 snapshot/branch/rollback 作为一等操作，而不是要求上层每次手写 `cp -r`、`git stash` 或临时目录管理。实现上可优先复用 Btrfs/ZFS snapshot、OverlayFS 或 content-addressed store。

### 3.7 问题七：log-structured 有价值，但不是唯一答案

本地报告强调 log-structured filesystem。这个方向在轨迹、审计、事件日志上合理，因为这些数据通常呈 append-only 形态。但将它扩展为 AgentFS 的总答案并不严谨。

F2FS 文档明确说明 log-structured 设计要处理 cleaning、wandering tree 和冷热数据布局等复杂问题 [F2FS](https://docs.kernel.org/filesystems/f2fs.html)。早期 LFS 研究和后续性能对比也显示，cleaning 策略和事务 workload 会显著影响性能，LFS 优势依赖 workload [USENIX LFS cleaning](https://www.usenix.org/conference/usenix-1995-technical-conference/heuristic-cleaning-algorithms-log-structured-file)、[File system logging vs clustering](https://www.microsoft.com/en-us/research/publication/file-system-logging-versus-clustering-performance-comparison/)。

**推理结论**：AgentFS 可以内部使用 append-only log 和 content-addressed objects，但不应承诺所有 workload 都使用单一 log-structured on-disk layout。轨迹和审计适合日志；工作区文件树适合 snapshot + diff + content addressing；高频查询可能适合数据库索引；大对象适合 object store。

---

## 4. 当前文件系统是否必须改造？

### 4.1 不需要立即替换底层文件系统

没有足够证据说明 ext4/XFS/Btrfs/ZFS/F2FS 这类底层文件系统整体不适合 agent。Agent 的许多底层需求已有成熟机制：

- 快照：Btrfs/ZFS/NILFS2/OverlayFS 可提供不同粒度的 checkpoint；
- 限权：Landlock、namespace、容器、chroot、seccomp、ACL 可组合；
- 安全路径解析：`openat2` 可减少 symlink / magic-link / path traversal 风险；
- 用户态文件系统：FUSE 可快速实验新语义；
- 内容寻址：Git 为 immutable object + mutable ref 提供了成熟工程证据 [Pro Git](https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain.html)。

因此，第一阶段不应写一个新内核文件系统。这会把风险集中在最难验证、最难部署、最容易产生数据损坏的层。

### 4.2 必须改造 agent 接触文件系统的语义层

当前缺口不是“能不能存文件”，而是：

| 必要语义 | 当前 POSIX/普通 FS 状态 | AgentFS 目标 |
|---|---|---|
| 最小权限 | 依赖进程权限、路径约定、容器配置 | 每个任务授予显式 capability |
| 安全路径解析 | 应用自己处理，容易遗漏 symlink/magic link | 默认 `dirfd` + constrained resolution |
| 多文件事务 | 应用自己实现，语义不统一 | 原子 commit/abort |
| 工作区分支 | Git/临时目录/容器各做各的 | 一等 workspace branch |
| provenance | mtime/owner 不足 | W3C PROV 风格因果图 |
| 审计 | shell log / app log 分散 | hash-chained operation log |
| replay | 依赖临时日志，常不可重现 | snapshot + tool/model/env manifest |
| 并发冲突 | advisory lock 不够 | read-set/write-set + CAS |
| 数据治理 | 靠外部流程 | classification / retention / export policy |

**结论**：当前文件系统需要改造，但改造对象应是 agent-facing interface 和 metadata/control plane，不是优先替换所有存储引擎。

---

## 5. AgentFS 的设计目标

### 5.1 非目标

先明确不做什么：

1. 不把 AgentFS 设计成“另一个通用 ext4/ZFS 替代品”。
2. 不把 vector database、workflow engine、message queue、object store 都塞进 filesystem。
3. 不假设所有 agent workload 都写密集、追加型、TB-PB 规模。
4. 不把 prompt、token、embedding 当成普通文件系统必须理解的基本块。
5. 不依赖模型“自觉遵守路径约束”；权限必须由系统强制。

### 5.2 目标

AgentFS 至少要满足以下目标：

| 目标 | 严格含义 |
|---|---|
| Scoped authority | agent 只能看到和修改任务授予的资源 |
| Transactional workspace | 多文件修改可作为一个提交单位 |
| Versioned state | 每次提交可定位、可比较、可回滚 |
| Provenance by construction | 写入默认携带来源、活动、参与者、策略和证据 |
| Replayable trajectory | 能重建 agent 看到的文件版本、工具输出和提交序列 |
| Conflict-aware collaboration | 多 agent 提交前检测 read/write 冲突 |
| Observable operations | 文件操作可映射到 trace/span/event |
| Backend neutrality | 可运行在普通 FS、snapshot FS、FUSE、object store 或日志后端上 |

---

## 6. 推荐架构

### 6.1 分层架构

```text
┌──────────────────────────────────────────────────────────┐
│ Agent runtime / IDE / CI / MCP client                     │
├──────────────────────────────────────────────────────────┤
│ AgentFS API                                               │
│ - workspace, read, patch, transaction, commit, rollback   │
│ - search, diff, merge, provenance, replay, export trace   │
├──────────────────────────────────────────────────────────┤
│ Policy & Capability Layer                                 │
│ - allowed roots, path policy, data classification          │
│ - operation permissions, approval gates, retention rules   │
├──────────────────────────────────────────────────────────┤
│ Transaction & Version Layer                               │
│ - read-set/write-set, CAS, MVCC, snapshot refs             │
│ - atomic multi-file commits, branch/merge                  │
├──────────────────────────────────────────────────────────┤
│ Provenance & Audit Layer                                  │
│ - W3C PROV entities/activities/agents                     │
│ - OpenTelemetry-compatible spans/events                   │
│ - hash-chained operation log, optional signatures          │
├──────────────────────────────────────────────────────────┤
│ Storage Adapter Layer                                     │
│ - POSIX fs, OverlayFS, Btrfs/ZFS snapshot, FUSE            │
│ - content-addressed object store, append-only log          │
└──────────────────────────────────────────────────────────┘
```

关键点：AgentFS API 是 agent 唯一接触文件的入口。底层 POSIX 路径、shell command 和裸文件描述符不应直接暴露给模型驱动的决策层。

### 6.2 核心对象模型

AgentFS 的最小对象模型：

| 对象 | 含义 |
|---|---|
| `Workspace` | 一个 agent 任务的隔离文件视图，基于某个 parent snapshot |
| `Capability` | 对路径集合和操作集合的授权，例如 read-only、patch-only、test-output-write |
| `Blob` | 内容寻址的不可变文件内容 |
| `Tree` | 路径到 blob / directory / metadata 的映射 |
| `Transaction` | 包含 read-set、write-set、delete-set、rename-set 和 preconditions |
| `Commit` | 原子发布的 tree 更新，带 provenance 和 validation result |
| `Trace` | agent 动作、工具调用、文件操作和观察结果的时间线 |
| `Policy` | 数据分类、保留、外发、审批和命令执行约束 |

Git 的 object database 和 refs 为 content-addressed object + mutable reference 提供了成熟工程证据 [Pro Git](https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain.html)，但 AgentFS 不能直接等同于 Git：Git 不记录完整模型上下文、工具权限、shell side effect 和运行时 trace，也不适合所有二进制大对象或高频临时产物。

### 6.3 API 草案

```text
create_workspace(parent_ref, policy_id, capabilities) -> workspace_id
read(workspace_id, path, options) -> {content, version, provenance}
search(workspace_id, query, scope) -> results
begin_transaction(workspace_id) -> tx_id
patch(tx_id, path, base_version, diff, intent) -> patch_result
write_artifact(tx_id, path, content_ref, classification) -> result
delete(tx_id, path, base_version, intent) -> result
commit(tx_id, message, validation_refs, approval_refs) -> commit_ref
rollback(workspace_id, target_ref) -> workspace_ref
diff(ref_a, ref_b, scope) -> diff
merge(target_workspace, source_commit, strategy) -> merge_result
export_trace(workspace_id, format = otel|prov|jsonl) -> trace_ref
```

设计原则：

- 所有 mutating operation 必须带 `intent`，用于审计和后续 review。
- 所有写入必须绑定 `base_version` 或显式声明 blind write。
- 默认拒绝路径逃逸、symlink surprise、magic-link surprise 和未经授权的 absolute path。
- `commit` 是唯一发布可见状态的操作。
- 每次 commit 必须持久化 operation log、manifest 和 tree ref。

### 6.4 Provenance schema

建议映射到 W3C PROV：

| W3C PROV 概念 | AgentFS 映射 |
|---|---|
| Entity | 文件版本、blob、测试结果、工具输出、用户请求、上下文片段 |
| Activity | read、patch、test、build、commit、rollback、approval |
| Agent | LLM 模型实例、human reviewer、tool server、CI runner |

每个 commit 至少记录：

- parent commit / parent snapshot；
- agent runtime、模型标识、工具版本、policy id；
- 用户请求 hash 和系统提示 hash；
- read-set、write-set、delete-set、rename-set；
- validation evidence，例如测试命令、退出码、日志 hash；
- approval evidence，如果需要人工批准；
- data classification 和 retention policy；
- wall-clock timestamp 和 monotonic sequence number；
- operation log hash chain head。

模型输出本身可能非确定，因此 AgentFS 不承诺“同样输入一定得到同样输出”。它承诺的是：可以恢复 agent 当时看到的文件版本、工具输入输出、策略、模型标识和提交证据，从而支持调试、审计和近似复现实验。

---

## 7. 实现路径

### 7.1 MVP：用户态语义层

第一版不写内核模块。建议实现为一个 library + daemon + MCP server：

- library 提供 workspace/transaction/provenance API；
- daemon 维护 content store、metadata DB、operation log 和 policy；
- MCP server 暴露受限 read/write/search/diff/commit 工具；
- 执行命令时在 workspace mount 或临时 checkout 中运行；
- Linux 上用 `openat2` 做安全路径解析，用 Landlock 限制进程文件访问；
- workspace 用 OverlayFS、临时目录、Git worktree 或 Btrfs snapshot 作为 backend；
- operation log 使用 append-only JSONL/CBOR + hash chain，后续可替换为专用日志。

这个路径的优势是可测试、可部署、可回滚。FUSE 可作为第二阶段选择：它能把新语义挂到普通文件接口上，但其权限和死锁风险需要额外验证 [FUSE](https://www.kernel.org/doc/html/latest/filesystems/fuse/fuse.html)。

### 7.2 第二阶段：可选 FUSE / snapshot backend

当 library/MCP 方案验证 API 有价值后，再提供 FUSE mount：

- 让 legacy tools 看到普通目录；
- 在 open/write/rename/unlink 上拦截并生成 transaction；
- 对 forbidden path、symlink escape、secret path 做强制拒绝；
- 将 `.agentfs/` 暴露为只读 control plane，例如 commits、trace、policy、locks；
- 对高风险操作要求显式 approval token。

底层 backend 可以选择：

- 普通 POSIX 目录：最简单，适合小项目；
- OverlayFS：适合临时 agent workspace；
- Btrfs/ZFS：适合快速 snapshot/rollback；
- content-addressed store：适合去重、审计和跨 workspace 共享；
- append-only log：适合 trajectory 和 audit。

### 7.3 第三阶段：基于测量决定是否进入内核或专用布局

只有在以下条件成立时，才有理由研发专用 kernel filesystem 或 on-disk layout：

- agent trajectory / audit log 的写入吞吐、fsync 频率或 tail latency 成为瓶颈；
- snapshot/rollback 的空间放大或延迟无法接受；
- 多 agent commit 冲突检测需要更低层的索引支持；
- 大规模文件观察和增量索引导致普通 FS + metadata DB 成本过高；
- zoned storage / flash endurance 约束明确要求顺序写入布局。

即使进入这一阶段，也不应“一刀切 log-structured”。更合理的是混合布局：

- append-only log：trajectory、audit、commit manifest；
- content-addressed blob store：文件内容和工具输出；
- B-tree/LSM metadata index：路径、版本、provenance、policy 查询；
- snapshot-friendly tree：workspace state；
- optional hot/cold separation：缓存、测试产物、大对象、长期审计记录分层。

---

## 8. 安全模型

### 8.1 威胁模型

AgentFS 至少假设以下威胁存在：

- 用户提供的文件、README、issue、网页或测试输出可能包含提示注入；
- agent 可能误解任务，尝试访问无关路径；
- 工具 server 可能暴露过宽能力；
- 多 agent 可能互相覆盖或读取不该共享的数据；
- shell command 可能产生文件系统 side effect；
- 日志和上下文可能泄露 secret；
- 审计日志可能被篡改或删除；
- 崩溃可能发生在任意写入点。

OWASP MCP Top 10 对 MCP 和 agent tool 环境中的 scope creep、context over-sharing、command injection、缺少 audit/telemetry 等风险给出了安全分类 [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/)。

### 8.2 安全控制

| 风险 | 控制 |
|---|---|
| 路径逃逸 | `openat2` constrained resolution；禁止未授权 symlink/magic link；路径 canonicalization 不作为唯一安全边界 |
| 过宽权限 | per-task capability；默认 deny；read/write/delete/execute 分离 |
| 提示注入诱导读 secret | secret path 分类；context budget policy；敏感文件需要显式 approval |
| 命令副作用 | 命令在 workspace sandbox 内运行；Landlock/seccomp/container 组合 |
| 审计篡改 | hash chain；append-only backend；可选签名和远端 notarization |
| 数据外发 | export policy；classification；redaction；egress approval |
| 并发覆盖 | base_version + read-set/write-set 检测；commit CAS |
| 崩溃半提交 | manifest-first 或 log-first commit protocol；crash recovery test |

---

## 9. 性能与存储策略

AgentFS 不应把性能目标写成空泛的“高吞吐”。应按 workload 分类：

| Workload | 访问模式 | 推荐策略 |
|---|---|---|
| agent trajectory | append-only、小事件、多索引查询 | append log + trace index |
| coding workspace | 读多、局部多文件修改、频繁 diff/test | snapshot + content addressing + path index |
| build/test output | 大量临时文件、可丢弃 | separate scratch area；短 TTL |
| dependency/cache | 大对象、重复读、跨 workspace 共享 | shared content store；quota |
| provenance/audit | 小记录、强耐久、长期保留 | append-only hash chain；压缩归档 |
| vector/embedding | 高维近邻查询 | vector DB，不放进核心 FS |

Log-structured backend 可用于 trajectory/audit，但 workspace 不必强制 log-structured。F2FS 的复杂设计说明，日志布局需要冷热分离、cleaning 和映射表才能控制写放大 [F2FS](https://docs.kernel.org/filesystems/f2fs.html)。如果没有 workload 测量，直接设计新 LFS 是高风险工程。

---

## 10. 评估标准

一个符合科学标准的 AgentFS 研究项目必须有可复现实验，而不是只画架构图。

### 10.1 正确性

- 多文件 commit 在随机崩溃后是否只出现 old 或 new 状态；
- rollback 是否恢复文件内容、metadata、policy 和 provenance；
- read-set/write-set 是否检测到并发冲突；
- symlink、hardlink、mount point、magic link、rename race 是否无法逃逸 policy；
- operation log 是否能完整重建提交序列。

### 10.2 安全性

- 使用恶意 README / issue / test output 诱导 agent 读取 secret，系统是否拒绝；
- 未授权 write/delete/execute 是否被强制阻断；
- context over-sharing 是否可由 policy 检测和阻止；
- 审计日志是否能防止或检测篡改；
- allowed directory 变化后旧 capability 是否失效或按版本解释。

### 10.3 可用性

- 在 SWE-bench / SWE-agent 类任务上，AgentFS 是否降低文件编辑错误率；
- agent 是否更少需要 whole-file overwrite；
- 人类 reviewer 是否能更快定位 agent 修改原因；
- 失败任务是否能从 trace 中定位关键误读或错误工具输出。

### 10.4 性能

- read/write/patch/commit/rollback 延迟；
- p95/p99 commit latency；
- snapshot 创建和删除成本；
- audit log fsync 成本；
- metadata index 空间放大；
- 与 plain POSIX workspace、Git worktree、OverlayFS、Btrfs snapshot 的对比；
- 长时间运行后的 GC/compaction/cleanup 成本。

### 10.5 可移植性

- Linux 原生 backend；
- macOS/Windows 降级 backend；
- 容器 / CI runner 适配；
- remote workspace 和 object store 适配；
- MCP server 集成。

---

## 11. 推荐路线图

### Phase 0：测量和威胁建模

- 收集真实 agent 文件操作 trace：读路径、写路径、文件大小、diff 大小、命令 side effect、测试产物、失败原因；
- 标注敏感路径、危险操作、回滚需求；
- 区分 coding agent、research agent、ops agent、data agent、mobile agent。

### Phase 1：AgentFS library + MCP server

- 实现 capability-scoped read/write/search/diff/commit；
- 所有路径操作走 safe path resolver；
- 所有写入生成 provenance 和 audit event；
- workspace 先用普通目录或 OverlayFS；
- 引入 hash-chained operation log。

### Phase 2：事务和版本层

- content-addressed blob store；
- tree refs、commit refs、read-set/write-set；
- branch/merge/rollback；
- crash recovery tests；
- OpenTelemetry trace export 和 W3C PROV export。

### Phase 3：强隔离 backend

- Linux：Landlock + namespace/container + optional FUSE；
- snapshot backend：Btrfs/ZFS/OverlayFS；
- per-agent scratch/cache/audit 分区；
- policy-driven secret redaction 和 egress gates。

### Phase 4：benchmark 和 workload-driven storage

- 用真实 agent trace 回放；
- 和 plain FS/Git/OverlayFS/Btrfs 对比；
- 只有当数据表明确有需要时，再评估专用 log-structured 或 zoned-storage backend。

---

## 12. 最终方案：AgentFS 的最小可行定义

一句话定义：

> AgentFS 是一个在现有文件系统之上的 agent-facing 事务化工作区层，它把文件操作从裸路径读写提升为带 capability、版本、provenance、audit、rollback 和 replay 语义的受控操作。

最小可行系统应具备：

1. **能力化命名空间**：每个 agent 任务只获得显式授权的路径和操作。
2. **安全路径解析**：所有路径基于授权 root 解析，防止 symlink/magic-link/path traversal 逃逸。
3. **事务化提交**：多文件修改以 commit 发布，支持 abort 和 rollback。
4. **内容寻址和版本引用**：文件版本可哈希定位；workspace tree 可 diff/merge。
5. **Provenance by default**：每次写入记录 agent、模型、工具、输入、证据和 policy。
6. **Append-only audit log**：操作日志 hash-chained，可导出、压缩、签名。
7. **Trace integration**：文件操作映射到 OpenTelemetry 类 trace，便于调试和观测。
8. **冲突检测**：commit 使用 base_version/read-set/write-set 做 optimistic concurrency control。
9. **后端可替换**：普通 FS 起步；按需接入 OverlayFS、Btrfs/ZFS snapshot、FUSE、object store 或 log backend。
10. **实验证据驱动演进**：任何内核改造、专用 LFS 或硬件协同都必须由 benchmark 支撑。

---

## 13. 结论

Agent 场景确实暴露了当前文件系统的不足，但不足不在“传统文件系统不会顺序追加写”这么简单。真正的问题是：普通文件系统不知道 agent 的意图、权限、轨迹、来源、验证证据和协作边界。它们能保存文件，却不能解释和约束一个半自治系统为什么、如何、在什么权限下改变了世界。

因此，当前文件系统需要改造，但正确的改造顺序是：

1. 先改 agent-facing 语义层：capability、transaction、provenance、audit、replay、rollback、conflict；
2. 复用成熟底层：Landlock、openat2、OverlayFS、Btrfs/ZFS snapshot、FUSE、content-addressed store；
3. 用真实 agent trace 和 crash/security benchmark 验证；
4. 最后才讨论专用 on-disk layout、log-structured backend 或 kernel integration。

本地报告的 log-structured 方向可以保留为一个后端选项，尤其适合 trajectory 和 audit log。但如果把它作为 AgentFS 的核心答案，会漏掉 agent 场景最真实、最危险、也最需要工程严肃性的部分：安全边界、因果记录、可恢复提交和可解释协作。

---

## 参考资料

1. ReAct: Synergizing Reasoning and Acting in Language Models — https://arxiv.org/abs/2210.03629
2. SWE-bench: Can Language Models Resolve Real-World GitHub Issues? — https://juanmirod.github.io/public/papers/swe-bench_2310.06770v3.pdf
3. SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering — https://papers.nips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf
4. Model Context Protocol Resources Specification — https://modelcontextprotocol.io/specification/2025-06-18/server/resources
5. MCP filesystem server README — https://github.com/modelcontextprotocol/servers/blob/main/src/filesystem/README.md
6. OWASP MCP Top 10 — https://owasp.org/www-project-mcp-top-10/
7. Linux Landlock documentation — https://cdn.kernel.org/doc/html/latest/userspace-api/landlock.html
8. Linux `openat2(2)` man page — https://man7.org/linux/man-pages/man2/openat2.2.html
9. Linux `fcntl` locking man page — https://man7.org/linux/man-pages/man2/fcntl_locking.2.html
10. Linux FUSE documentation — https://www.kernel.org/doc/html/latest/filesystems/fuse/fuse.html
11. Linux OverlayFS documentation — https://docs.kernel.org/filesystems/overlayfs.html
12. Btrfs design documentation — https://btrfs.readthedocs.io/en/stable/dev/dev-btrfs-design.html
13. Linux F2FS documentation — https://docs.kernel.org/filesystems/f2fs.html
14. Finding Crash-Consistency Bugs with Bounded Black-Box Crash Testing — https://arxiv.org/abs/1810.02904
15. Heuristic Cleaning Algorithms in Log-Structured File Systems — https://www.usenix.org/conference/usenix-1995-technical-conference/heuristic-cleaning-algorithms-log-structured-file
16. File System Logging Versus Clustering: A Performance Comparison — https://www.microsoft.com/en-us/research/publication/file-system-logging-versus-clustering-performance-comparison/
17. W3C PROV-DM: The PROV Data Model — https://www.w3.org/TR/prov-dm/
18. AI Data Security: Best Practices for Securing Data Used to Train and Operate AI Systems — https://www.fbi.gov/file-repository/cyber-alerts/ai-data-security-best-practices-for-securing-data-used-to-train-and-operate-ai-systems-052225.pdf
19. OpenTelemetry Traces — https://opentelemetry.io/docs/concepts/signals/traces/
20. Pro Git, Git Internals — https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain.html
