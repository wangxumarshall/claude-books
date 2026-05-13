# Agent 场景文件系统研究

---

## 结论

**现有文件系统需要改造，但改造对象是 agent 接触文件系统的语义层（AgentFS），而非底层磁盘布局（ext4/XFS/Btrfs/ZFS）。**

---

## 一、现有文件系统在哪些方面无法满足Agent诉求？缺口不在"能不能存文件"，而在"能不能解释和约束 agent 的文件操作"。

### 事实依据

1. **ReAct 论文**（Yao et al., 2022）证明 agent 的状态不是最终输出，而是推理-动作-观察交错的**轨迹**。普通文件系统只保存最终文件树，不保存轨迹。

2. **SWE-agent 论文**（Yang et al., NeurIPS 2024）证明 agent-computer interface 的设计会显著影响 agent 在软件工程任务中的表现——文件编辑接口不是中性的实现细节。

3. **MCP filesystem server** 的参考实现已经默认要求配置允许访问的目录，把 read/write/list/delete 等能力限制在 allowed directories 内。这说明当前 agent 工具层已经在用策略包裹文件系统，而非直接暴露裸 POSIX 接口。

4. **OWASP MCP Top 10** 把 scope creep、command injection、context over-sharing、缺少审计遥测列为 agent 工具环境的重要安全风险。

### 推理

普通文件系统能保存字节流、目录、权限位和 inode 元数据，但它不表达"**哪个模型、基于什么上下文、通过哪个工具、在什么策略下、为什么写了这个文件**"。Agent 场景恰好需要这些语义。

---

## 二、需要改造哪些点？为什么？

### 问题一：Ambient authority 与路径逃逸

**事实**：Agent 根据上下文、模型输出和工具反馈动态决定读写什么。如果 agent 拥有宿主目录的宽权限，错误推理、提示注入或恶意文件内容都可能诱导它读取 secret、覆盖无关文件。

**依据**：Linux `openat2(2)` 手册页明确记录了 `/proc` magic link 的容器逃逸风险，并提供了 `RESOLVE_BENEATH`/`RESOLVE_IN_ROOT` 约束。Linux Landlock 文档建议采用最小权限目录边界。这些机制的存在本身就证明了路径逃逸是真实威胁。

**改造点**：AgentFS 必须默认是 capability-scoped filesystem——路径字符串不能直接等于权限；权限应绑定到**工作区、动作类型、路径前缀、数据等级和任务目的**。

### 问题二：多文件修改缺少 agent 级事务

**事实**：Coding agent 一次任务常修改多个文件（源码、测试、配置、lockfile）。POSIX 提供单文件 rename 的原子替换语义，但不提供跨文件、跨目录的 agent 级事务。

**依据**：崩溃一致性研究（Mohan et al., 2018）显示，很多成熟文件系统中的 bug 可以用很小的、围绕 `fsync` 的 workload 复现，并发现了新的文件系统 bug。这说明"写文件后程序没报错"不等于"agent 的多步修改具备可恢复提交语义"。

**改造点**：需要 `begin_transaction → propose changes → validate preconditions → commit/abort`。崩溃后只能看到 commit 前或 commit 后状态，不能看到半套 agent 修改。

### 问题三：缺少因果 provenance

**事实**：普通文件系统记录 owner、mode、mtime、ctime，但不能回答：哪个 agent 写了这个文件？使用了哪个模型、工具版本、系统提示？写入前看过哪些文件？

**依据**：W3C PROV-DM 将 provenance 定义为关于**实体、活动和参与者**的信息，用于评估数据质量、可靠性和可信度。CISA/NSA/FBI 联合发布的 AI 数据安全指南建议跟踪数据 provenance、使用安全存储、签名和完整性措施。

**改造点**：每次 agent 写入应建模为 provenance graph 的一部分。**文件内容、工具动作、模型调用、测试结果和人工批准**都应有可关联的 ID。

### 问题四：长轨迹难以回放和调试

**事实**：ReAct 类 agent 的状态是 action/observation 轨迹。失败后仅靠最终 diff 和 shell history 很难回答：哪一步误读了上下文？哪个工具输出被截断？

**依据**：OpenTelemetry 已把 trace 建模为 span、event、attribute 等结构。AgentFS 不需要重新发明观测模型，但需要把文件操作纳入这种 trace。

**改造点**：operation log 应同时服务于**审计、调试、回放和安全检测**。单纯保存最终文件树不够。

### 问题五：并发 agent 的冲突不是 advisory lock 能解决的

**事实**：Linux 文件锁主要是 advisory。手册页说明 mandatory locking 在 Linux 上长期不可靠，已在 Linux 5.15+ 移除支持。

**依据**：多 agent 协作时，冲突常是语义冲突（一个 agent 修改 API，另一个修改调用点），而非简单的同 inode 并发写。

**改造点**：需要版本向量或 MVCC 风格的 read-set/write-set 检测，提交时做 optimistic concurrency control。

### 问题六：快照、回滚和隔离需成为日常路径

**事实**：Agent 的典型工作流包括探索、试错、运行测试、回滚、重试。

**依据**：Btrfs 的 subvolume/snapshot 使用 COW 共享 root block，支持只读快照。OverlayFS 可组合 lower/upper/workdir 成叠加视图。这些机制已存在但 agent 工具层未统一使用。

**改造点**：**snapshot/branch/rollback** 应作为一等操作，而非要求上层每次手写 `cp -r` 或 `git stash`。

---

## 三、为什么不需要立即替换底层文件系统？

**严格推理链**：

1. **前提一**：Agent 的底层存储需求（快照、限权、安全路径解析、用户态文件系统、内容寻址）已有成熟机制——Btrfs/ZFS snapshot、Landlock、`openat2`、FUSE、Git object model。

2. **前提二**：没有公开的 agent workload benchmark 证明 ext4/XFS/Btrfs/ZFS 在延迟、写放大、快照成本、审计吞吐或并发提交上无法满足 agent 场景的目标。

3. **前提三**：写一个新内核文件系统是把风险集中在最难验证、最难部署、最容易产生数据损坏的层。F2FS 文档明确说明 log-structured 设计要处理 cleaning、wandering tree、冷热数据布局等复杂问题——在没有 workload 测量的情况下设计新 LFS 是高风险工程。

4. **结论**：第一阶段不应写新内核文件系统。应先改造 agent-facing 语义层，复用成熟底层，用真实 agent trace 和 benchmark 验证后，再决定是否需要专用 on-disk layout。

---

## 四、AgentFS 方案

### 定义

> AgentFS 是一个在现有文件系统之上的 agent-facing 事务化工作区层，它把文件操作从裸路径读写提升为带 capability、版本、provenance、audit、rollback 和 replay 语义的受控操作。

### 分层架构

```
Agent runtime / IDE / CI / MCP client
        ↓
AgentFS API（workspace, read, patch, transaction, commit, rollback, search, diff, merge, provenance, replay, export trace）
        ↓
Policy & Capability Layer（allowed roots, path policy, data classification, operation permissions, approval gates, retention rules）
        ↓
Transaction & Version Layer（read-set/write-set, CAS, MVCC, snapshot refs, atomic multi-file commits, branch/merge）
        ↓
Provenance & Audit Layer（W3C PROV entities/activities/agents, OpenTelemetry spans/events, hash-chained operation log, optional signatures）
        ↓
Storage Adapter Layer（POSIX fs, OverlayFS, Btrfs/ZFS snapshot, FUSE, content-addressed object store, append-only log）
```

关键点：AgentFS API 是 agent 唯一接触文件的入口。底层 POSIX 路径、shell command 和裸文件描述符不应直接暴露给模型驱动的决策层。

### 核心对象模型

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

### API 草案

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

### 最小可行系统应具备的 10 项能力

1. **能力化命名空间**：每个 agent 任务只获得显式授权的路径和操作
2. **安全路径解析**：所有路径基于授权 root 解析，防止 symlink/magic-link/path traversal 逃逸
3. **事务化提交**：多文件修改以 commit 发布，支持 abort 和 rollback
4. **内容寻址和版本引用**：文件版本可哈希定位；workspace tree 可 diff/merge
5. **Provenance by default**：每次写入记录 agent、模型、工具、输入、证据和 policy
6. **Append-only audit log**：操作日志 hash-chained，可导出、压缩、签名
7. **Trace integration**：文件操作映射到 OpenTelemetry 类 trace
8. **冲突检测**：commit 使用 base_version/read-set/write-set 做 optimistic concurrency control
9. **后端可替换**：普通 FS 起步；按需接入 OverlayFS、Btrfs/ZFS snapshot、FUSE、object store
10. **实验证据驱动演进**：任何内核改造、专用 LFS 或硬件协同都必须由 benchmark 支撑

### 安全模型

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

### 实现路线图

| 阶段 | 内容 |
|---|---|
| Phase 0 | 收集真实 agent 文件操作 trace，标注敏感路径、危险操作、回滚需求 |
| Phase 1 | AgentFS library + MCP server：capability-scoped read/write/search/diff/commit，hash-chained operation log |
| Phase 2 | 事务和版本层：content-addressed blob store，tree refs，branch/merge/rollback，crash recovery tests |
| Phase 3 | 强隔离 backend：Landlock + namespace/container + optional FUSE，snapshot backend |
| Phase 4 | Benchmark 和 workload-driven storage：用真实 agent trace 回放，与 plain FS/Git/OverlayFS/Btrfs 对比，数据驱动决定是否需要专用存储布局 |

---

## 五、对本地 log-structured 报告的批判性评估

本地报告正确指出 log-structured 思想已广泛影响文件系统和数据库，但其"Agent 时代的机会点"部分存在以下不严谨之处：

| 原推断 | 问题 |
|---|---|
| Agent workload 写密集、追加为主 | 无 workload 测量；不同 agent 任务差异巨大 |
| Agent 数据粒度是向量/embedding/token | 向量库和 token cache 属于数据库/模型运行时，不是文件系统的核心抽象 |
| TB-PB 是 Agent 的典型规模 | 对个人 coding agent、移动端 agent 不成立 |
| LSM + log-structured FS 是自然答案 | LFS cleaning 和 LSM compaction 都有写放大、尾延迟和空间放大问题 |

**严格结论**：log-structured 方向可保留为 trajectory 和 audit log 的后端选项，但不能作为 AgentFS 的核心答案。AgentFS 的第一性问题是语义和安全，不是磁盘布局。

---

## 六、总结

Agent 场景确实暴露了当前文件系统的不足，但不足不在"传统文件系统不会顺序追加写"这么简单。真正的问题是：普通文件系统不知道 agent 的意图、权限、轨迹、来源、验证证据和协作边界。它们能保存文件，却不能解释和约束一个半自治系统为什么、如何、在什么权限下改变了世界。

因此，当前文件系统需要改造，但正确的改造顺序是：

1. 先改 agent-facing 语义层：capability、transaction、provenance、audit、replay、rollback、conflict；
2. 复用成熟底层：Landlock、openat2、OverlayFS、Btrfs/ZFS snapshot、FUSE、content-addressed store；
3. 用真实 agent trace 和 crash/security benchmark 验证；
4. 最后才讨论专用 on-disk layout、log-structured backend 或 kernel integration。

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
