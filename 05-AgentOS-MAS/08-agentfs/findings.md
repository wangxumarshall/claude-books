# Findings & Decisions

## Requirements
- User asks for a critical, deep local-report-based study of filesystems for agent scenarios.
- Must answer: real problems/challenges, necessity of changing current filesystems, what changes are needed, why, how to change, and the proposed solution.
- Must conform to scientific facts; no mutual flattery, no fantasy; every fact and reasoning step must have strict basis.
- Final deliverable: Chinese research report with top Silicon Valley programmer/researcher standard and style.

## Local Report Findings
- Existing local report: `log-structured-filesystem-research.md`.
- Strength: useful overview of log-structured filesystems, F2FS, NILFS2, ZFS, Btrfs, WAFL, LSM-tree, zoned storage, and related trends.
- Critical gap: the "Agent 时代的机会点" section asserts workload properties such as write-heavy, append-mainly, token/vector granularity, and TB-PB scale without evidence or bounded scope.
- Critical gap: it mixes layers: filesystem, LSM database engine, vector index, audit log, and multi-agent coordination. These layers have different contracts and failure models.
- Critical gap: it assumes log-structured FS is the likely answer. That may be true for some workloads, but agent file access also needs safety, provenance, replay, concurrency control, namespace isolation, and policy enforcement, which are not solved by append-only layout alone.

## Research Findings
- Agent workload evidence:
  - ReAct defines an agent pattern in which language models interleave reasoning traces with task-specific actions and receive observations from external environments. This is evidence that agent state is not just final output; it is a trajectory of thought/action/observation-like events. Source: https://arxiv.org/abs/2210.03629
  - SWE-bench tasks are created from real GitHub issues and pull requests; the task is to generate a PR that fixes the issue and passes tests. This is evidence that coding agents operate over existing repository files and test environments, not isolated prompt-answer tasks. Source: SWE-bench paper PDF, https://juanmirod.github.io/public/papers/swe-bench_2310.06770v3.pdf
  - SWE-agent found interface design materially affects performance. Its paper states compact file editing and consistent feedback are critical; naive redirection/whole-file overwrite and sed-style edits have drawbacks. This supports treating the file interface as an agent-computer interface, not a neutral POSIX detail. Source: SWE-agent NeurIPS 2024 paper PDF, https://papers.nips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf
- Existing filesystem/security evidence:
  - MCP resources are URI-addressed context objects; `file://` resources may behave like a filesystem without mapping to a physical filesystem. MCP explicitly requires URI validation, access controls for sensitive resources, binary encoding, and permission checks. Source: https://modelcontextprotocol.io/specification/2025-06-18/server/resources
  - The reference MCP filesystem server exposes read/write/list/delete/move/search/metadata operations and restricts operations to configured allowed directories or roots. This is evidence that current agent tooling already wraps the filesystem with policy, rather than giving raw ambient host access by default. Source: https://github.com/modelcontextprotocol/servers/blob/main/src/filesystem/README.md
  - OWASP MCP Top 10 v0.1 identifies security risks directly relevant to agent file access: scope creep, command injection, insufficient authz/authn, lack of audit/telemetry, and context over-sharing. This is a security-community taxonomy, not a formal theorem, but it supports the threat model. Source: https://owasp.org/www-project-mcp-top-10/
  - Linux Landlock provides unprivileged access control and recommends least-privilege directory hierarchy leaves; it reasons over allowed file hierarchies independent of underlying filesystem. Source: https://cdn.kernel.org/doc/html/latest/userspace-api/landlock.html
  - Linux `openat2` was added in Linux 5.6 and provides path-resolution constraints. Its man page documents risks from `/proc` magic links, including container escape, and detects attempts to escape with `RESOLVE_BENEATH`/`RESOLVE_IN_ROOT`. Source: https://man7.org/linux/man-pages/man2/openat2.2.html
  - Linux file locks are mostly advisory; mandatory locking was unreliable, little used, optional since Linux 4.5, and unsupported in Linux 5.15+. Advisory locks only help cooperating processes. Source: https://man7.org/linux/man-pages/man2/fcntl_locking.2.html
  - FUSE lets userspace processes provide data and metadata through the normal kernel interface and supports non-privileged mounts, but the kernel docs document permission, DoS, information leak, and deadlock concerns. Source: https://www.kernel.org/doc/html/latest/filesystems/fuse/fuse.html
  - OverlayFS is useful for copy-up workspaces, but it has backing filesystem requirements and stores origin information in xattrs for some features; it is a practical overlay mechanism, not a full provenance or transaction model. Source: https://docs.kernel.org/filesystems/overlayfs.html
  - Btrfs snapshots share a root block with a subvolume and COW makes subsequent changes private; read-only snapshots are possible. This supports fast checkpoint/rollback where the underlying FS supports it. Source: https://btrfs.readthedocs.io/en/stable/dev/dev-btrfs-design.html
- Storage layout evidence:
  - F2FS docs describe log-structured writes, the wandering-tree problem, cleaning overhead, NAT, background cleaning, hot/warm/cold multi-head logs, and adaptive logging. This supports the local report's claims that log-structured designs matter, but also shows their complexity and GC costs. Source: https://docs.kernel.org/filesystems/f2fs.html
  - USENIX 1995 and Microsoft Research summaries show LFS cleaning can seriously degrade performance in transaction workloads; LFS advantages are workload dependent. This is evidence against a blanket "agent workloads imply log-structured filesystem" conclusion. Sources: https://www.usenix.org/conference/usenix-1995-technical-conference/heuristic-cleaning-algorithms-log-structured-file and https://www.microsoft.com/en-us/research/publication/file-system-logging-versus-clustering-performance-comparison/
  - Crash-consistency research found many reported filesystem bugs reproduced with small workloads around `fsync`, and found new bugs in mature Linux filesystems. This supports requiring explicit crash/replay testing for an agent filesystem. Source: https://arxiv.org/abs/1810.02904
- Provenance/audit evidence:
  - W3C PROV defines provenance as information about entities, activities, and people involved in producing data, used to assess quality/reliability/trustworthiness. This maps directly to agent artifacts produced by model/tool/user actions. Source: https://www.w3.org/TR/prov-dm/
  - Joint CISA/NSA/FBI/partner AI Data Security guidance recommends data provenance tracking, secure storage, signatures, and integrity measures across AI system lifecycle. Source: https://www.fbi.gov/file-repository/cyber-alerts/ai-data-security-best-practices-for-securing-data-used-to-train-and-operate-ai-systems-052225.pdf
  - OpenTelemetry standardizes traces as spans with timestamped events and attributes, and semantic conventions standardize common metadata names. This supports using established observability primitives rather than inventing an opaque log format. Sources: https://opentelemetry.io/docs/concepts/signals/traces/ and https://opentelemetry.io/docs/concepts/semantic-conventions/
- Reusable design evidence:
  - Git is explicitly described in the Pro Git book as a content-addressable filesystem with a VCS interface. Its object database, refs, HEAD, and index are proven patterns for immutable content plus mutable references, though Git itself is not optimized for every agent workload. Source: https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain.html

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| Treat "agent filesystem" as a semantics/API problem first, and a physical layout problem second | The local report focuses on storage layout, but agent failures more often arise from permissions, reproducibility, provenance, race conditions, and unsafe tool effects. |
| Separate facts, engineering inferences, and design hypotheses in the final report | This directly addresses the user's requirement for rigorous evidence and avoids speculative overclaiming. |
| Avoid proposing a kernel rewrite as the default answer | Existing Linux mechanisms already provide many building blocks; the missing agent semantics can be validated faster in a userspace layer or library. |
| Treat log-structured storage as an implementation option, not the core thesis | LFS/F2FS evidence shows benefits for sequential writes, but cleaning/GC and workload sensitivity make it unsafe to generalize. |
| Define AgentFS as an agent-facing semantic layer, not necessarily a new on-disk format | Existing systems provide most low-level mechanisms; the missing pieces are policy, provenance, rollback, replay, conflict, and observability semantics. |

## Critical Analysis Conclusions
- Fact: Agents use tools and interact with external environments through action/observation loops. In file-heavy tasks, the environment includes a repository or workspace. Evidence: ReAct, SWE-bench, SWE-agent.
- Inference: Agent storage risk comes from the combination of autonomous writes, imperfect model intent, untrusted input/context, long multi-step trajectories, and external side effects. This is broader than throughput.
- Fact: Existing OS filesystems expose byte streams/directories/inodes and conventional permissions, but they do not natively encode "this write was caused by model X using prompt Y and tool Z under policy P."
- Inference: A new semantic layer is necessary if the system must support reliable rollback, audit, replay, and least-privilege action at the agent operation level. A new physical filesystem is not yet justified by evidence alone.
- Fact: Linux has building blocks: Landlock, openat2, OverlayFS, Btrfs snapshots, FUSE, advisory locks, and existing observability standards.
- Inference: First implementation should compose these pieces and expose agent-native operations; only after workload measurements show kernel/on-disk bottlenecks should a specialized FS layout be considered.
- Non-requirement: It is not scientifically defensible to claim all agent workloads are TB-PB scale, write-heavy, token/vector-granular, or necessarily best served by log-structured filesystems. Those are workload hypotheses requiring measurement.
- Non-requirement: AgentFS should not replace databases/vector databases/workflow engines. It should provide workspace semantics, provenance, safety, and commit/replay primitives that those systems can use or reference.

## Issues Encountered
| Issue | Resolution |
|-------|------------|

## Resources
- Local source report: `log-structured-filesystem-research.md`
- ReAct: https://arxiv.org/abs/2210.03629
- SWE-bench: https://juanmirod.github.io/public/papers/swe-bench_2310.06770v3.pdf
- SWE-agent: https://papers.nips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf
- MCP Resources: https://modelcontextprotocol.io/specification/2025-06-18/server/resources
- MCP filesystem server: https://github.com/modelcontextprotocol/servers/blob/main/src/filesystem/README.md
- OWASP MCP Top 10: https://owasp.org/www-project-mcp-top-10/
- Linux Landlock: https://cdn.kernel.org/doc/html/latest/userspace-api/landlock.html
- Linux openat2: https://man7.org/linux/man-pages/man2/openat2.2.html
- Linux fcntl locking: https://man7.org/linux/man-pages/man2/fcntl_locking.2.html
- Linux FUSE: https://www.kernel.org/doc/html/latest/filesystems/fuse/fuse.html
- OverlayFS: https://docs.kernel.org/filesystems/overlayfs.html
- Btrfs design: https://btrfs.readthedocs.io/en/stable/dev/dev-btrfs-design.html
- F2FS docs: https://docs.kernel.org/filesystems/f2fs.html
- W3C PROV-DM: https://www.w3.org/TR/prov-dm/
- AI Data Security guidance: https://www.fbi.gov/file-repository/cyber-alerts/ai-data-security-best-practices-for-securing-data-used-to-train-and-operate-ai-systems-052225.pdf
- OpenTelemetry traces: https://opentelemetry.io/docs/concepts/signals/traces/
- Pro Git internals: https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain.html

## Visual/Browser Findings
- Web sources support the conclusion that agent-facing filesystem design must focus on scoped authority, path safety, provenance, rollback, reproducible replay, conflict management, and observability.
