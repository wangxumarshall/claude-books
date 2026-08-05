# openYuanrong 函数系统（yuanrong-functionsystem）接纳与维护决策评估报告

**评估对象**：`yuanrong-functionsystem` 代码仓（openYuanrong Serverless 分布式计算引擎之"函数系统"组件）
**评估日期**：2026-08-05
**评估方法**：源码级深度审阅（约 41.4 万行 C++/Go + 1006 次提交全量 git 考古）+ 多 Agent 并行子系统纵深勘察
**评估视角**：顶级 AI/系统软件专家 × 老练项目经理（接纳决策与 ROI 最大化）
**对标粒度**：《深入理解 Linux 内核》式的子系统级梳理

---

## 第〇章 执行摘要（先读这一章）

### 0.1 一句话结论

> 这是一个年轻、仍在高速迭代的分布式系统，工程素养远超普通国产项目。底子好：华为系 openEuler/原壤社区用正式 PR 流程驱动（Gitee !PR + CI bot 同步），20 多位人类贡献者，10 个月 1006 次提交（2025-09-30 ~ 2026-07-20）；架构完整，测试扎实（测试/生产比≈0.40），文档有 ADR/spec 规范。包袱也实在：双构建迁移未竟、自研 etcd 兼容层加手写 K8s 模型、巨型上帝类、命令注入安全债、华为云强绑定，五类。**结论是有条件接纳**——详见第陆章。

### 0.2 关键画像（数字）

| 维度 | 数值 | 评价 |
|---|---|---|
| 源码规模 | C++/Go ≈ 413,975 行（874 cpp + 793 h + 276 go + 67 hpp） | 中大型系统 |
| 项目龄期 | 10 个月（2025-09-30 首提交 ~ 2026-07-20 最新） | 年轻、高节奏 |
| 提交总数 | 1006 次（含 266 个 `!NNN` PR 同步、94 个 merge/sync） | 活跃开源工作流 |
| 近 1/2/3 月提交 | 82 / 133 / 179 | 仍在高速演进 |
| 人类贡献者 | ~20+（Lwy_Robb 201、WolfBolin 67、mhsong2 53…）+ openeuler-ci-bot 273 | 真实社区 |
| 独立可执行服务 | 6 个 C++（master/agent/proxy/domain_sched/iam/runtime_mgr）+ 1 个 Go（runtime-launcher） | 微服务式 |
| 测试规模 | 99,885 行 / 235 文件 / 204 用 gmock | 测试/生产≈0.40，覆盖扎实 |
| 最大文件 | instance_ctrl_actor.cpp **7394 行**（+测试 6405 行） | 上帝对象 |
| 技术债信号 | fix 占比 ~34%（256+ fix 提交） | 补丁式演进 |
| 构建系统 | Bazel（16 BUILD）+ CMake（222 CMakeLists）双轨 | 迁移未完成 |
| 许可证 | Apache 2.0（Huawei Copyright） | 商业友好 |
| 三方依赖 | 516KB OSS Notice，abseil 2024.07 等较新 | 依赖锁定基本健全 |

### 0.3 五大历史包袱（详见第肆章）

1. **架构包袱·双构建系统**：Bazel（新，16 BUILD）与 CMake（旧，222 CMakeLists）并存，`run.sh`→`make_functionsystem.py` 走 Bazel，但 CMake 仍是全仓 GLOB 单一 `main` 可执行——迁移未竟，新人二义性高。
2. **架构包袱·自研 etcd 兼容层 + 手写 K8s 模型**：`meta_store`（13K 行）是 etcd 兼容 API 适配层加一个单节点桩（`META_STORE_CLUSTER_ID=123456` 等硬编码，真正一致性靠 passthrough 转发 etcd）。`kube_client`（115 个 cpp）手写 K8s REST 模型，没用官方 client。K8s API 每次演进都得手工同步，维护成本高。
3. **代码包袱·巨型上帝类**：`InstanceCtrlActor` 7394 行承担实例生命周期/调度校验/亲和/心跳/健康/IAM/转发/GC 等十余职责（违反 SRP）；`ScalerActor` 3356 行包揽 K8s Deployment/Pod 全套 CRUD+迁移+污点。同类巨型文件还有 `runtime_executor.cpp` 2381、`function_agent_mgr_actor.cpp` 2216、`agent_service_actor.cpp` 2034。
4. **安全包袱·命令注入面 + 加密空壳**：`code_deployer` 和 `network_tool` 大量用 `std::system(cmd.c_str())` 拼接路径执行 shell（copy_deployer.cpp:108/114、remote_deployer.cpp:193/215、working_dir_deployer.cpp:330/407、network_tool.cpp:132/194/223）。`POST_START_EXEC` 只用 regex 限制后就 popen 执行（runtime_executor.cpp:417-442）。`crypto.cpp` 的 Encrypt/Decrypt 是明文返回的桩（注释明说 "does not provide algorithms by default"）。合规要自己补。
5. **生态包袱·华为云强绑定**：CI 基础镜像 `swr.cn-southwest-2.myhuaweicloud.com/yuanrong-dev/compile_x86:2.1`、Bazel redirect 全指向 `repo.huaweicloud.com`、若干依赖下载自 `openyuanrong.obs…myhuaweicloud.com`、部署依赖 openYuanrong 全家桶（datasystem/runtime/pattern_faas/checkpoints）与 Jiwenbox/JiwenSwarm——外部团队复现 CI 与脱离华为云生态成本高。

### 0.4 接纳决策建议（详见第陆章）

**建议：有条件接纳（Adopt with Conditions）**，而非无条件接管或直接否决。

- **战略价值高**：Serverless+AI 函数调度是前沿赛道，国产可控的分布式调度引擎稀缺，技术与品牌资产均有价值。
- **工程基本面好**：正式 PR 流程、ADR/spec 文化、测试扎实、ASan/TSan 配置、模块化治理宪章——接手后可平滑继续。
- **ROI 关键在"前置条件"**：必须从原团队获取①CI 镜像构建方法与华为云凭证脱钩方案 ②vendor 预编译产物的可复现构建链 ③sandboxd 新功能的完成路线图 ④安全债的已知清单。否则工作量与风险将失控。

### 0.5 总工作量估算（详见第伍章）

| 阶段 | 工作量（人月 PM） | 说明 |
|---|---|---|
| T0 接纳准备（1-2 月） | 4-6 PM | 知识转移、CI/构建复现、环境搭建、安全审计 |
| T1 稳定化（2-4 月） | 8-12 PM | 安全债修复、巨型类拆分首批、补顶层文档 |
| T2 持续演进（6-12 月） | 15-25 PM | 构建系统统一、meta_store/kube_client 现代化、跟进前沿 |
| **合计（首年）** | **27-43 PM** | 约 3-5 人专职团队一年的投入 |

---

## 第壹章 项目深度理解：openYuanrong 函数系统是什么

### 1.1 产品定位（来自 README + docs + proto）

openYuanrong（原壤）是 **Serverless 分布式计算引擎**，"以一套统一 Serverless 架构支持 AI、大数据、微服务等各类分布式应用"。其核心抽象是**函数（Function）**——对传统 Serverless 函数的通用化扩展，"起到类似单机 OS 中进程的作用，可以表达任意分布式应用的运行实例，同时天然支持相互调用"。

整个 openYuanrong 由**四个代码仓**组成（本仓为其一）：

| 仓库 | 职责 | 类比 |
|---|---|---|
| `yuanrong` | 多语言函数运行时（Python/Java/C++ 编程接口） | 函数 SDK + 语言运行时 |
| **`yuanrong-functionsystem`（本仓）** | 函数系统：分布式动态调度、实例扩缩/迁移 | K8s 控制面（scheduler+controller+kubelet）的等价物 |
| `yuanrong-datasystem` | 数据系统：异构多级缓存、Object/Stream 语义 | 分布式缓存/对象存储 |
| `yuanrong-frontend` | 网关：函数创建、调用 | API Gateway |

本仓 version `0.7.0.dev`/README 标 `0.8.0.dev`——仍在 1.0 前的快速迭代期。

### 1.2 总体架构（源码级梳理）

本仓是一个**微服务式分布式系统**，编译为 6 个 C++ 独立可执行 + 1 个 Go 辅助进程：

```
                       ┌─────────────────────────────────────────────┐
                       │           function_master（全局调度器）      │  ← 类比 kube-scheduler + controller-manager
                       │  global_scheduler / instance_manager /       │
                       │  scaler / resource_group / snap / quota      │
                       │  + Traefik HTTP provider（路由发布）          │
                       └───────────────┬─────────────────────────────┘
                                       │ MetaStore watch/leader
              ┌────────────────────────┼────────────────────────┐
              ▼                        ▼                        ▼
  ┌───────────────────┐    ┌──────────────────────┐    ┌──────────────────┐
  │ domain_scheduler   │    │  function_proxy /     │    │  iam_server      │
  │ （域/集群级中间     │    │  local_scheduler     │    │  （鉴权：AKSK/   │
  │   调度器）          │    │  （节点本地代理）     │    │  Casdoor/Keycloak│
  │  preemption/        │    │   instance_ctrl(7394)│    │  /token）        │
  │  underlayer_sched   │    │   + Traefik route    │    └──────────────────┘
  └─────────┬─────────┘    └──────────┬───────────┘
            │                          │
            ▼                          ▼
  ┌──────────────────────────────────────────────────┐
  │  function_agent（节点上的函数代理：部署/driver/plugin）│
  │  + runtime_manager（运行时生命周期：ckpt/health/log/  │
  │    port/std_monitor/virtual_env）                   │
  │  + sandboxd_executor（新沙箱：supervisor 拉起 runtime）│
  └──────────────────────┬───────────────────────────┘
                          │ gRPC/UDS（proto/posix/*）
                          ▼
  ┌──────────────────────────────────────────────────┐
  │  runtime-launcher（Go）：docker/podman 后端容器运行时 │  ← 类比 CRI/容器引擎代理
  └──────────────────────────────────────────────────┘

  横贯全局的通信基石：common/litebus（自研 libprocess 风格 Actor 框架，43K 行）
  元数据存储：meta_store（etcd 兼容 API 适配层 + 本地桩，13K 行）/ 亦可直连 etcd
  观测：common/metrics（OpenTelemetry 16K）+ common/logs + Grafana dashboards
```

**三级调度模型**（这是本项目最核心的架构思想，源码级可证）：

1. **function_master / global_scheduler**（全局）：类比 Mesos master / K8s kube-scheduler。维护调度队列（`GET /global-scheduler/scheduling_queue`）、做全局 bin-packing/亲和决策、按 root domain 分配实例请求。Leader 选举支持 etcd/k8s/txn 三种后端（`common/leader/*`）。
2. **domain_scheduler**（域/集群中间层）：类比"逻辑集群调度器"。做域内抢占（`preemption_controller`）、委托底层调度器（`underlayer_scheduler_manager`——可能对接 K8s/Volcano）。
3. **function_proxy / local_scheduler**（节点本地）：类比 **kubelet**。每个节点一个，管理本节点所有函数实例生命周期——`InstanceCtrlActor` 是其心脏（7394 行）。含 `LocalGcActor`（异常实例周期回收，有完整 DESIGN.md）、`SnapCtrl`、`AbnormalProcessor` 等。

### 1.3 通信基石：common/litebus

全项目的进程内/跨进程通信都建立在自研的 `litebus` 之上（43K 行，156 文件）。从 `function_master/main.cpp` 的 include 与用法可见：所有服务由若干 `Actor` 组成，通过 `litebus::Spawn`、`litebus::Async`、`litebus::AsyncAfter`、`litebus::Future/Promise`、AID 寻址编程——这是 **libprocess/Mesos 风格的 Actor 模型**（非 Akka 的 JVM、非 Seastar 的 share-nothing-per-core）。包含自研 event loop（`src/evloop`）、TCP/UDP/HTTP/SSL（`src/tcp`、`src/httpd`、`src/ssl`）、异步执行器（`src/exec`）。它是项目的"用户态微内核"。

### 1.4 资源模型（来自 proto/posix/resource.proto）

资源表示法受 **Mesos 影响**：`Value.Type = SCALAR | RANGES | SET | COUNTER | VECTORS`，`ResourceUnit`、`ScheduleTopology{leader,members}`、`Register`/`Registered` 握手——典型的"调度器-执行器注册+资源 offer"范式。同时 `ScalerActor` 直接操作 K8s `V1Deployment/V1Pod`（手写模型）——说明系统**双轨**：既能直上 K8s，也有自研调度语义。

### 1.5 数据流（一个函数实例从创建到运行，源码级）

1. 用户经 frontend 网关创建函数 → master 的 `instance_manager` 入队调度队列。
2. `global_scheduler` 决策：亲和校验（`affinity.proto` LabelIn/LabelNotIn）、配额（`quota_manager_actor`）、资源视图（`resource_view_actor`）→ 下发到某 domain。
3. `domain_scheduler` 域内可选抢占 → 转发到目标节点的 `function_proxy`。
4. `function_proxy/local_scheduler` 的 `InstanceCtrlActor` 接管：校验（`CheckSchedRequestValid`）、异步部署（`AsyncDeployInstance`）、起心跳（`StartHeartbeat`）、订阅状态变更（`SubscribeInstanceStatusChanged`）。
5. `function_agent/code_deployer` 拉代码（`copy_deployer`/`remote_deployer`/`working_dir_deployer`，**注意：用 std::system 拼接路径——安全债**）。
6. `runtime_manager` 拉起运行时：旧路径 `runtime_executor.cpp`，新路径 `sandboxd_executor.cpp`（supervisor + traefik 端口路由 + checkpoint）。`runtime-launcher`（Go）经 `SandboxService` gRPC 调 docker/podman 起容器。
7. 运行中：`LocalGcActor` 周期回收 FAILED/EXITED/EVICTED/卡滞实例；`AbnormalProcessor` 上报；Traefik 经 `GET /traefik/config` 拉取路由表对外发布。
8. 实例退出/迁移：`scaler_actor` 的 `MigratePodInstanceWithTaints`/`MigrateNodeInstanceWithTaints` 处理 K8s 污点迁移。

### 1.6 工程文化（这是接纳决策的强正面信号）

- **PR 评审工作流**：266/1006 提交带 `!NNN` Gitee PR 编号（最大 !363），openEuler CI bot 同步——有正式评审，非个人提交。
- **ADR / spec-driven 开发**：`specs/001-generic-lru-module/` 完整展示了 spec→research→data-model→contracts→tasks→checklist 的工程流程，含 Decision/Rationale/Alternatives 三段式；`docs/traefik-*.md`、`gc_actor/DESIGN.md` 体现资深架构师文档风格（确定性 JSON、FNV hash 兼容、故障模式表、并发测试）。
- **架构治理宪章**：`plan.md` 的 Constitution Check 列出 7 条架构原则（模块化/gRPC/容器运行时抽象/可观测性/测试/快照/LiteBus Actor）+ 命名规范 + 构建规范——有正式治理。
- **测试纪律**：测试/生产比≈0.40，204 文件用 gmock，LRU spec 明确要求 TSan 验证；`.bazelrc` 配 ASan/TSan/Release/Debug 多 config。
- **AI 辅助开发痕迹**：`.gitignore` 忽略 `.claude/CLAUDE.md/SKILL.md/AGENTS.md/.specify/opencode.json`——原团队用 AI 工具+spec 驱动开发，这解释了文档的高规范度。


## 第贰章 子系统源码级纵深（多 Agent 并行勘察结论）

> 本章由 7 个并行子 Agent 对各子系统做《深入理解 Linux 内核》式纵深勘察后整合。结论与第壹章架构梳理互补，聚焦"每个子系统是什么、怎么实现、债在哪"。

### 2.1 common/litebus —— 自研 libprocess 风格 Actor 通信框架（43K 行，156 文件）

**定位**：`litebus.hpp` 注释自述"provide an asynchronous programming framework as Actor model"。`LitebusAddress{scheme,ip,port}` + TCP/UDP URL + `threadCount` + 测试目录 `common/litebus/test/libprocess_server/`（`libprocess_tcp_server.cpp`/`libprocess_ssl_server.cpp`/`libprocess_udp_server.cpp`）**实证对标 Mesos 的 libprocess**——进程以 AID 寻址、跨网络消息、Future/Promise 异步、Actor 编程范式。

**核心原语**：`Actor`/`AID`/`Future`/`Promise`/`Option`/`Msg`/`Naught`（include/actor/*.hpp）；`Spawn`/`Async`/`AsyncAfter`/`Defer`/`Await`/`Terminate` API（见 function_master/main.cpp 与 gc_actor/DESIGN.md 的用法）。

**并发/IO 模型**：自研 `evloop`（`src/evloop/evloop.cpp`）基于 **epoll**（`epoll_create`/`epoll_wait`，`EPOLL_EVENTS_SIZE`），非 io_uring——稳健保守、可移植、易调试但非极致性能。线程模型含 `threadCount` 可配池；含 `src/actor`/`src/async`/`src/exec`/`src/tcp`/`src/udp`/`src/httpd`/`src/ssl`/`src/iomgr`/`src/timer`/`src/utils`。

**历史包袱**：①自研而非用成熟库（Seastar/Folly Future/asio），意味着缺陷需自修、无社区补丁——但测试目录有完整 `libprocess_server_test`+`http_test`+`tcp/udp/timer` 测试，自测不弱。②epoll 非 io_uring，对极致高并发有上限，但与本项目"调度系统"定位（非海量 IO）匹配，**非致命**。③43K 行自研框架学习曲线陡，新人需消化——是接纳后最大认知成本之一。

**与外部交互**：向上暴露 `litebus::Spawn/Async/Future` 给所有 6 个 C++ 服务（它们全是 Actor）；向下依赖 STL + 自研 evloop，无第三方通信库依赖。是项目的"用户态微内核"。

### 2.2 function_proxy / local_scheduler —— 节点本地调度（40K 行，174 文件，全项目最大）

**定位**：类比 **K8s kubelet**——每节点一个，管理本节点所有函数实例生命周期。`InstanceCtrlActor`（instance_ctrl_actor.cpp **7394 行**，全项目最大）是其心脏。

**InstanceCtrlActor 职责（实证过载）**：从源码方法清单可见单类承担十余职责——实例生命周期（UpdateInstanceInfo/AsyncDeployInstance/ScheduleEnd）、调度校验（CheckSchedRequestValid/CheckDiskResourceValid/CheckHeteroResourceValid/VerifyTenantID/VerifyAffinityWithoutTenantKey）、亲和（AddTenantToScheduleAffinity/SetTenantAffinityOpt）、心跳健康（StartHeartbeat/StopHeartbeat/HandleRuntimeHeartbeatLost/HandleInstanceHealthChange）、IAM/token/aksk（UpdateInternalToken/UpdateInternalAkSk/BindInternalIAM/AddDsAuthToDeployInstanceReq）、转发（ForwardCallResultRequest/ForwardCustomSignalRequest/ForwardCustomSignalResponse）、状态机 GC（TryClearStateMachineCache/GCOrphanStateMachine）、driver 事件（OnDriverEvent/OnDriverConnected/DeleteDriverClient）、租户配额（OnTenantQuotaExceeded/OnTenantCooldownExpired）——**典型上帝对象，违反 SRP**。

**实例生命周期流程**：ScheduleRequest→CheckSchedRequestValid→AsyncDeployInstance→起心跳+订阅状态→运行→退出/迁移。含 `LocalGcActor`（异常实例周期回收，60s 扫描+5min 保留+10min 卡滞超时，有完整 DESIGN.md）、`SnapCtrl`、`AbnormalProcessor`、`BundleMgrActor`、`LocalGroupCtrlActor`、`function_agent_mgr_actor`（2216 行，管 agent）。

**与上下协作**：上接 function_master（转发非本节点请求、上报资源视图）、下接 runtime_manager/function_agent（部署+运行时）。Traefik 路由在 master 侧发布，proxy 侧不直接参与（见 gc_actor/DESIGN.md 架构图）。

**历史包袱**：①`InstanceCtrlActor` 7394 行 + 测试 6405 行——上帝对象，改一处易回归，测试镜像巨测。②`function_agent_mgr_actor` 2216 行同类问题。③但测试覆盖扎实（instance_ctrl_test 6405 行 + function_agent_mgr_test 1960 行），且 LocalGcActor 有完整 ADR 级文档——说明团队**知道问题但用流程兜底**，非放任。

### 2.3 function_master —— 全局调度器与控制面（25K 行，73 文件）

**定位**：类比 **kube-scheduler + controller-manager**。`function_master/main.cpp` 编入 global_scheduler/instance_manager/scaler/resource_group/snap/quota/system_function_loader/explorer/leader/meta_store_monitor——是控制面总装点。提供运维 API：`GET /global-scheduler/scheduling_queue`（调度队列）、`POST/DELETE /global-scheduler/node/localschedulingstatus`（节点本地调度开关 evicting/normal）、`GET /instance-manager/query-tenant-instances`（按 tenant/instance/node 查询，支持分页）。

**核心数据模型与状态机**：函数实例（InstanceInfo，proto `message.proto`）、资源组（ResourceGroup）、扩缩池（ResourcePool→V1Deployment）、快照（Snap）、配额（Quota）。实例状态枚举见 gc_actor/DESIGN.md：RUNNING/SUSPENDED/EVICTING（健康态）、CREATING/SCHEDULING（过渡态）、FAILED/EXITED/EVICTED（终态异常）。

**调度算法**：global_scheduler 维护普通队列+group 队列；亲和决策用 `affinity.proto`（LabelIn/LabelNotIn，类似 K8s nodeSelector/affinity）；有 `scheduler_framework`/`schedule_plugin`（common 下）——**支持热插拔调度插件**（先进设计）。资源视图 `resource_view_actor`（1978 行）维护全局资源账本。

**一致性机制**：Leader 选举三后端可选（`common/leader/`：etcd_leader_actor 217 行、k8s_leader_actor 194 行、txn_leader_actor 256 行——基于 meta_store txn）；meta_store watch 驱动状态同步（InstanceManagerActor 订阅 watch 事件更新路由）；Active-Standby 部署（TraefikLeaderContext 处理 standby→leader 转发，返回 503 保 last-known-good）。

**Traefik 集成**：FunctionMaster 暴露 `GET /traefik/config`，Traefik HTTP provider 轮询拉取路由表（替代旧 etcd registry 方案，消除 etcd 写放大+TTL 续约）。确定性 JSON（nlohmann::json std::map 字典序+routerName 排序，保证 FNV hash 稳定，避免 Traefik 反复 reload）。portForward 解析新旧格式（3段 protocol:hostPort:containerPort / 2段 hostPort:containerPort）+ routeKind（direct/tunnel/public）正交。这是**工程质量极高的设计**。

**历史包袱**：①`scaler_actor.cpp` 3356 行——上帝对象，包揽 K8s Deployment/Pod CRUD+迁移+污点+资源池（CreateDeployment/CheckExistingDeployment/IsSameDeploymentConfig/SetAffinityForPool/OnPodModified/MigratePodInstanceWithTaints/MigrateNodeInstanceWithTaints…）。②`instance_manager_actor.cpp` 2420 行同类。③但测试覆盖扎实（scaler_test 3580 行、instance_manager_test 2470 行、meta_store_test 2065 行、group_manager_test 1820 行），且 autoscaling/traefik 有完整设计文档——债务有测试与文档兜底。

### 2.4 meta_store 与 common 基础设施（13K + 69K 行）

**meta_store（13K 行，82 文件）——etcd 兼容 API 适配层 + 本地桩**：
- server/src/：kv_service_actor、lease_service_actor、watch_service_actor、maintenance_service_actor、backup_actor + passthrough/（election/kv/lease/watch passthrough actor）。
- `meta_store_common.h` 硬编码 `META_STORE_CLUSTER_ID=123456`/`MEMBER_ID=456789`/`REVISION=32`/`RAFT_TERM=2`——**本地是桩，非真 Raft**；真一致性走 `KvServicePassthroughActor`（持 `MetaStoreClient` 即 etcd client）转发 etcd。
- 结论：**降低了"自研 Raft 重造轮子"的严重性**（它只是 etcd 兼容层+本地直通桩，单节点开发/测试用 local 模式、生产用 passthrough 到真 etcd），但 13K 行适配层仍有理解与维护成本，且与真 etcd 行为一致性需验证。

**common（69K 行，501 文件）——全项目最大基础设施层**，盘点：
- **自研**：litebus 通信、leader 选举三实现、resource_lock（`lease_lock`，基于租约的分布式锁）、scheduler_framework/schedule_plugin（调度框架+插件）、resource_view（资源视图）、lru（spec 重构的通用 LRU）、kv_client、http、network、heartbeat、file_monitor、file_storage、metadata、meta_store_adapter、trace、profile、status、service_json、yaml_tool、utils（含 memory_optimizer/ssl_config/version/param_check/module_switcher/os_utils）。
- **封装**：kube_client（115 个手写 K8s 模型 cpp，**非官方 client-go**——手写 V1Pod/V1Deployment/V1SeccompProfile 等的 JSON 序列化）、etcd（meta_store_adapter）、iam（aksk+casdoor_verifier+keycloak_verifier+external_auth_verifier+token_manager）、obs（华为云对象存储 SDK）、crypto（**明文桩**）。
- **C++ 内存安全纪律**（实证）：shared_ptr 8075 处、unique_ptr 129 处、裸 new 仅 10 处、delete 280 处（多在智能指针 deleter/析构）——41 万行仅 10 处裸 new，**RAII 纪律远超平均水平**。

**历史包袱**：①kube_client 手写 115 个 K8s 模型——K8s API 演进时需逐字段手工同步，**长期必失同步**，是最重隐性债。②common 69K 行混自研与封装，部分本可独立成库（如 lru 已 spec 重构）。③crypto 明文桩（4.1.2）。④但 tests/unit/common 覆盖 30+ 子模块、resource_view_test 3563 行、kube_client_model_test 1635 行——基础设施测试不弱。

### 2.5 runtime_manager 与 sandboxd —— 运行时生命周期（25K 行 + Go 5.2K）

**runtime_manager（25K 行，123 文件）角色**：管理函数运行时（Python/Java/C++）的生命周期——启动、停止、检查点（ckpt）、健康检查（healthcheck）、日志（log）、端口转发（port）、标准输出监控（std_monitor）、虚拟环境（virtual_env_manager，含 conda/pip）、metrics、debug、config、utils、driver、manager。`runtime_manager/main.cpp` 引入 `<sys/capability.h>`+`<linux/capability.h>`——**真用 Linux capability 做沙箱**，方向正确。

**sandboxd 新沙箱（迁移中）**：`executor/sandboxd/sandboxd_executor.cpp`（1704 行）+ `sandboxd_checkpoint_orchestrator.cpp`。supervisor 拉起 runtime（`!355`），Traefik 做端口路由（routeKind: direct/tunnel/public，见 traefik 设计文档）。提交 `!334 feat[sandboxd]：同步sandbox执行器与运行时管理能力` 标志新路径引入。

**runtime-launcher（Go，5.2K 行）与 runtime_manager（C++）分工**：runtime-launcher/cmd/runtime-launcher/main.go 是容器运行时代理——UDS socket（`/var/run/runtime-launcher.sock`）+ gRPC 服务（`SandboxService`，proto `runtime/v1/sandbox_api.pb.go` 2556 行）+ docker/podman 后端（`internal/runtime`）+ 状态管理（`internal/state`）。为何两语言：C++ 侧 runtime_manager 承担调度系统侧的运行时编排（与 litebus Actor 集成），Go 侧 runtime-launcher 作为容器引擎薄代理（复用 Docker/Podman Go SDK 生态）。分工合理。

**历史包袱（安全与迁移）**：①`POST_START_EXEC`（runtime_executor.cpp:417-442）regex 限制后 popen 执行——命令注入面（4.1.1）。②`runtime_manager.cpp:470` `ExecuteCommand("lscpu")` 等裸命令调用。③sandboxd 与旧 runtime_executor.cpp（2381 行）**并存迁移未竟**（4.2.3）——行为不一致、测试分散。④但测试覆盖有（runtime_executor_test 2556 行），sandboxd 有 checkpoint orchestrator 设计。

### 2.6 构建系统与 CI/部署链路

**双构建系统并存**：
- **Bazel（新，官方路径）**：WORKSPACE + `bazel/*.bzl`（hazel_workspace、local_patched_repository、preload_grpc、preload_opentelemetry、grpc_extra_deps、各 BUILD 模板）+ `.bazelrc`（C++17、ASan/TSan/Release/Debug、`--distdir`+`--repository_cache` 双保险离线、`--experimental_downloader_config=.bazel_redirect.cfg`）+ `.bazel_redirect.cfg`（`mirror.bazel.build` → `repo.huaweicloud.com`）。仅 16 个 BUILD.bazel、tests 仅 2 个 BUILD.bazel——Bazel 迁移进行中、tests 落后。
- **CMake（旧，全仓覆盖）**：222 个 CMakeLists.txt；根 `CMakeLists.txt` 用 `file(GLOB_RECURCE)` 把全部源码编进**单一 `main` 可执行**——极简陋，与 6 二进制语义矛盾，疑似已实际废弃但未删。
- **入口**：`run.sh` → `scripts/executor/make_functionsystem.py` → `builder/build_bazel.py`/`build_cpp.py`/`build_go.py`/`build_whl.py` + `tasks/`（build_task/clean_task/download_vendor/vendor_cache/pack_task/test_task/run_code_gate/test_build_runtime_launcher）+ `utils/`（archive/files/logger/process/tools）。Python 构建编排器完备，有 vendor_cache_test/build_task_test 自测。

**vendor 依赖管理**：`vendor/src/`（gtest_1_12_1、libboundscheck、gogo-protobuf、grpc-gateway/googleapis、datasystem sdk）+ `vendor/output/Install/`（spdlog/obs/curl/zlib/等预编译产物）+ `vendor/patches/`。`download_vendor.py`+`vendor_cache.py`（有自测）拉取并缓存，sha256 锁定+distdir+repository_cache 双保险——**离线可复现构建设计健全**。

**CI**：`ci/compile.Dockerfile` 基于 `swr.cn-southwest-2.myhuaweicloud.com/yuanrong-dev/compile_x86:2.1`（华为云专有镜像）+ `ci/build_compile_image.sh`。**外部团队复现 CI 受阻于华为云镜像凭证**——核心供应链风险。

**部署**：`scripts/deploy/function_system/install.sh`（启动 6 二进制+etcd+meta_store 模式切换+Traefik+jemalloc）+ `scripts/deploy/third_party/install.sh`（etcd grpc-proxy）。依赖兄弟目录 `datasystem/`、`runtime/`、`pattern/pattern_faas/`、`checkpoints/` + 提交 `!360` 的 Jiwenbox/JiwenSwarm——**强耦合 openYuanrong 全家桶 + openEuler 运行环境**。

**代码规范工具**：`.clang-format`（**空文件**——格式配置缺失）、`ruff.toml`（line-length=120、double quote、space、lf）、`scripts/code_check.py`+`scripts/format_code.py`+`scripts/config/pyproject.toml`——有检查脚本但 clang-format 空配置是缺口。提交含大量 `fix(codecheck)` 说明门禁在用。

### 2.7 domain_scheduler / function_agent / iam_server —— 中间层调度、节点代理、鉴权

**domain_scheduler（5K 行，24 文件）——域/集群中间层调度器**：
- 子模块：domain_group_control、domain_scheduler_service、instance_control、underlayer_scheduler_manager、preemption_controller、startup、create_agent_decision、flags。
- 职责：在 function_master（全局）与 function_proxy（本地）之间做"逻辑域/集群"级调度——域内抢占（preemption_controller）、委托底层调度器（underlayer_scheduler_manager，对接 K8s/Volcano 等）、域分组控制（domain_group_control）。
- **历史包袱**：仅 5K 行、24 文件——相对三级调度的另两级（master 25K、proxy 40K）规模偏小，功能深度可能不及上下两级；三级调度职责边界是否清晰、有无重叠是接纳后需消化的点（tests/unit/domain_scheduler 覆盖 create_agent_decision/domain_group_control/preemption_controller/underlayer_scheduler_manager 等，覆盖不弱）。

**function_agent（8.8K 行，43 文件）——节点上的函数代理**：
- 子模块：agent_service_actor（2034 行）、code_deployer（copy/remote/working_dir）、driver、network（network_tool）、plugin（multi_plugin_client/remote_plugin_client）、common、flags。
- 职责：在节点上代表函数实例——代码部署（code_deployer 三种：复制/远程/工作目录）、agent 服务（agent_service_actor）、插件机制（plugin，remote_plugin_client 支持远程插件，`address.find("localhost")` 判断本地）、网络配置（network_tool 增删 route）。
- **历史包袱（安全重灾区）**：code_deployer 与 network_tool 大量 `std::system(cmd.c_str())` 拼接路径执行 shell——命令注入高危面（4.1.1 全部命中在此）。agent_service_actor 2034 行偏大但未到上帝级。测试有 agent_service_actor_test 3327 行。

**iam_server（7.6K 行，22 文件）——鉴权**：
- 子模块：iam_actor（iam_actor.h）、internal_iam（aksk_manager_actor、token_manager_actor、casdoor_config/verifier、keycloak_config/verifier、external_auth_verifier、token_content）、driver、flags。
- 鉴权模型：**AKSK（华为云风格）+ Token** 双轨；集成企业 IDP **Casdoor + Keycloak**（casdoor_verifier/keycloak_verifier，URL 表单提交 client_secret/password，UrlEncode 转义）+ external_auth_verifier（可扩展外部鉴权）。token_manager_actor/aksk_manager_actor 以 Actor 形态管理凭证生命周期。
- **历史包袱**：casdoor/keycloak_verifier 用 `&password=UrlEncode(password)` URL 拼接表单提交（keycloak_verifier.cpp:804 等）——需确认走 HTTPS 否则密码明文传输；client_secret 拼接需审计。但集成熟利 IDP 而非自研鉴权是**成熟工程选择**。测试有 iam_server 单测覆盖。

**三级调度职责重叠审视**：master（全局队列+亲和+扩缩决策）、domain（域内抢占+委托底层）、proxy（本地实例生命周期）——分层清晰，但 domain 层偏薄（5K vs 25K/40K），可能存在"中间层是否必要"的架构债嫌疑（若多数场景域=单集群，domain 可被 master 直接覆盖）。接纳后建议评估 domain_scheduler 的实际价值与简化空间。

### 2.8 历史包袱定量扫描汇总（全仓实证）

子 Agent 全仓 grep 扫描 + 本人复核的关键数字：
- **TODO/FIXME/XXX/HACK：仅 14 处**（排除 vendor）——41 万行项目惊人干净，团队纪律强。
- **命令注入面（std::system/popen）**：10+ 处集中在 code_deployer/network_tool/runtime_executor/file_monitor——4.1.1。
- **裸 new：仅 10 处**；shared_ptr 8075、unique_ptr 129、delete 280——RAII 纪律优秀。
- **中文注释/commit 混杂**：国产项目特征，commit 多见中文（如"删除文件 README.en.md"）+ 英文代码，国际化协作有阻力但不致命。
- **巨型文件**：instance_ctrl_actor.cpp 7394 + 测试 6405、scaler_actor 3356、instance_manager_actor 2420、runtime_executor 2381、function_agent_mgr_actor 2216、agent_service_actor 2034、resource_view_actor 1978、sandboxd_executor 1704——上帝对象集中区。
- **.gitignore 忽略大块**：`**/output/*`、`common/litebus/build/`、`functionsystem/build/`、`version.h`（生成）、`bazel-*`、`thirdparty/runtime_deps/`、`*.pb.go`（除 runtime-launcher 的）——生成物与产物隔离规范。
- **Third Party Notice**：516KB，涉及 abseil-cpp 2024.07、easyexcel、brotli、Apache Commons 等跨语言三方库——依赖众多且部分较新。
- **提交节奏**：近 1/2/3 月 82/133/179 提交仍活跃；fix ~34%（256+）、feat 134、chore 166、build 34、test 25——补丁式但 feat 持续增长，项目在前进非烂化。


## 第叁章 项目经理视角：接纳决策的评估维度

### 3.1 评估框架（十个维度）

站在老练项目经理视角，接纳一个外部项目需从**十个维度**系统评估。下表给出本仓的逐维评分（1-5，5 最好）与依据。

| # | 维度 | 评分 | 依据（源码级） |
|---|---|---|---|
| 1 | **战略价值** | 4.5 | Serverless+AI 函数调度是前沿赛道；国产可控的统一分布式调度引擎稀缺；可作为团队基础设施能力沉淀与品牌资产 |
| 2 | **技术健康度** | 3.0 | 架构完整且有治理宪章，但双构建、巨型类、自研 etcd/kube_client、命令注入债拖累；fix 占比 34% |
| 3 | **代码质量** | 3.5 | 命名规范（camelCase+member_ 前缀）、有 .clang-format/ruff、ADR 文档优秀；但部分巨型文件违反 SRP、中文注释混杂 |
| 4 | **测试与可验证性** | 4.0 | 测试/生产比≈0.40、204 文件用 gmock、spec 要求 TSan、ASan/TSan config 齐备；集成测试有 stubs/mocks |
| 5 | **文档与知识转移** | 2.5 | specs/DESIGN.md/traefik 文档质量极高，但**无顶层架构文档、无 CONTRIBUTING/CHANGELOG**，知识散在 PR/specs |
| 6 | **社区与可持续性** | 3.5 | 真实 PR 流程、~20 贡献者、10 月 1006 提交仍活跃；但强绑华为云/openEuler，外部接手能否获得上游支持存疑 |
| 7 | **许可证与合规** | 4.5 | Apache 2.0 + 516KB OSS Notice，商业友好；仅 crypto 为空壳需自补合规 |
| 8 | **安全 posture** | 2.5 | std::system 命令注入面、crypto 明文桩、POST_START_EXEC popen；有 `!341 security 清理敏感文档` 说明团队有安全意识 |
| 9 | **依赖与供应链** | 3.0 | 依赖锁定基本健全（sha256+distdir+repository_cache 双保险），但强绑华为云镜像/OBS、vendor 预编译产物来源需透明化 |
| 10 | **人力与成本** | 2.5 | 首年需 27-43 PM（3-5 人专职）；C++分布式+K8s+安全复合人才稀缺；学习曲线陡（litebus/meta_store 自研需消化） |

**加权总分：3.45 / 5** —— 中上，"有条件接纳"区间。

### 3.2 如何科学决策以最大化团队利益与 ROI

项目经理的核心不是"接不接"，而是"以什么条件、什么节奏、什么退出机制接"。建议采用**阶段化决策 + 实物期权**模型：

#### 3.2.1 三道门（Stage-Gate），每道门都可中止

- **门 1（2 周尽职调查 DD）**：不投入实质开发，只验证"硬骨头"——①能否脱华为云复现 CI ②vendor 构建链是否可独立 ③sandboxd 完成度 ④安全债清单 ⑤上游是否愿意继续协作。**通过门 1 才进入 T0。**
- **门 2（T0 接纳准备 1-2 月）**：4-6 PM。产出：可在自有 CI 复现构建、可独立部署最小可用集群、安全审计报告、顶层架构文档 v1。**通过门 2（能独立构建+跑通）才进入 T1。**
- **门 3（T1 稳定化 2-4 月）**：8-12 PM。产出：P0 安全债清零、首批巨型类拆分、CI 绿、可对外发版。**通过门 3 才承诺长期 T2。**

每道门失败即止损，沉没成本可控（最多 4-6 PM）。这是**最大化 ROI 的关键**——不要一上来就承诺 43 PM。

#### 3.2.2 最大化 ROI 的五条策略

1. **谈判前置条件**：向原团队索要 CI 镜像 Dockerfile 源、vendor 构建脚本、sandboxd 路线图、安全已知清单、架构脑图——**这些是"零成本知识转移"，价值等于数月人力**。不给则砍价或放弃。
2. **保留上游同步能力**：维持与 openEuler/原壤上游的可同步分支（`!NNN` PR 机制），不要立即 fork 成不可合并的私有树——能持续吃到上游修复，ROI 最高。
3. **先治安全与可构建，后治架构债**：先修命令注入（P0，1-2 PM 即可大幅降险）、统一构建系统（消除双轨二义性），再啃巨型类——**风险按降序排，回报按可见度排**。
4. **以演进替代重写**：meta_store/kube_client 虽是"重造轮子"但**能跑且有测试**，不要推倒重写（重写是最大陷阱），而用"边替换边共存"——如逐步用官方 k8s client-go 替换手写模型、逐步用真 etcd 直连替换 meta_store 适配层。
5. **借前沿趋势放大价值**：将函数调度能力对齐当前前沿（见第伍章）——AI Agent 编排、Wasm 函数运行时、eBPF 可观测、Serverless GPU——让接纳后的项目增值，而非纯维护。

#### 3.2.3 退出机制（Negative ROI 触发器）

设置明确的"若发生则止损退出"的红线：
- 若 T0 后仍无法脱华为云独立复现 CI → 退出（供应链不可控）。
- 若安全审计发现 RCE 级未修复漏洞且上游拒绝协作 → 退出。
- 若 T1 稳定化后 fix 增速不降反升 → 退出（项目在烂化）。
- 若团队无法招募/培养 ≥2 名 C++ 分布式核心人力 → 退出（人力断档）。

### 3.3 决策矩阵（情景化建议）

| 团队画像 | 建议 | 理由 |
|---|---|---|
| 有 C++ 分布式 + K8s + 安全人力，且做云原生/Serverless 平台业务 | **接纳（全门通过后）** | 战略契合，可消化债并增值 |
| 仅需"用"函数调度能力，不自研平台 | **不接纳代码，仅用上游发行版** | 接管代码 ROI 低，直接用更划算 |
| 有人力但无 Serverless 业务场景 | **谨慎/否决** | 维护成本无业务分摊，ROI 为负 |
| 无 C++ 分布式人力 | **否决** | 学习曲线陡，必陷入维护泥潭 |


## 第肆章 历史包袱源码级梳理（Linus 式逐项审判）

> 本章以"如果要把这个项目维护起来，先得知道哪些地方会咬人"为视角，逐项列明已确认的历史包袱，全部定位到 file:line，并给出维护影响与修复成本。

### 4.1 P0 安全债（必须优先治理）

#### 4.1.1 命令注入面（高危）

- `functionsystem/src/function_agent/code_deployer/copy_deployer.cpp:108,114` —— `std::system(cmd.c_str())` 拼接路径执行。
- `functionsystem/src/function_agent/code_deployer/remote_deployer.cpp:193,215,362` —— 同上，`unzip -Z -l` 拼接 destFile。
- `functionsystem/src/function_agent/code_deployer/working_dir_deployer.cpp:330,407` —— `std::system(cmd)` chmod/unzip。
- `functionsystem/src/function_agent/network/network_tool.cpp:132,194,198,223` —— route 增删用 `std::system`/`ExecuteCommand` 拼接。
- `functionsystem/src/runtime_manager/executor/runtime_executor.cpp:417-442` —— `POST_START_EXEC` 仅以 `POST_START_EXEC_REGEX` regex 限制后 `ExecuteCommandByPopen(command, INT32_MAX)` 执行；`runtime_manager.cpp:470` 直接 `ExecuteCommand("lscpu")`。
- `functionsystem/src/common/file_monitor/monitor_callback_actor.cpp:117` —— `ExecuteCommandByPopen(command, INT32_MAX)`。
- `functionsystem/src/common/utils/exec_utils.h:116-132` —— popen 封装，`fullCommand` 拼接。

**影响**：函数代码部署、网络配置、运行时启动均经 shell 拼接，若路径/参数含元字符即命令注入。在多租户 Serverless 场景下这是**租户隔离绕过级**风险。
**修复成本**：2-4 PM（改用 `execvp`/`fork+exec` 数组传参或 `posix_spawn`，移除 shell；逐处替换并补单测）。

#### 4.1.2 加密空壳（合规级）

- `functionsystem/src/common/crypto/crypto.cpp` 全文 —— `Encrypt`/`Decrypt`/`LoadSecretKey` 全为桩，明文返回 + 注释 "OpenYuanRong does not provide encryption and decryption algorithms by default. You can implement…"。

**影响**：敏感数据（AKSK、token、凭证）在元数据层实际明文存储；若团队有合规要求（金融/政企），不补实现即不合规。
**修复成本**：1-2 PM（接入 OpenSSL EVP AES-GCM；或显式声明由外接 KMS/HSM 承担并文档化）。

#### 4.1.3 沙箱隔离强度待证

`runtime_manager/main.cpp` 引入 `<sys/capability.h>` + `<linux/capability.h>`——真用 Linux capability 做沙箱，方向正确；但 `sandboxd_executor.cpp`（1704 行）是新功能（`!334`），与旧 `runtime_executor.cpp`（2381 行）并存，迁移未竟（见 4.2.3）。需审计 sandbox 边界是否完整（namespace/capability/seccomp/网络），防止逃逸。**修复成本**：审计 1 PM + 修复视发现而定。

### 4.2 架构包袱

#### 4.2.1 双构建系统并存（中危，认知成本高）

- **Bazel（新）**：16 个 BUILD.bazel、WORKSPACE + `bazel/*.bzl`（preload_grpc/preload_opentelemetry/local_patched_repository）、`.bazelrc`（ASan/TSan/Release/Debug/distdir/repository_cache）、`.bazel_redirect.cfg`（华为云镜像）。
- **CMake（旧，但全仓覆盖）**：222 个 CMakeLists.txt；根 `CMakeLists.txt` 用 `file(GLOB_RECURSE)` 把全部 .cpp/.cc/.h 编进**单一 `main` 可执行**（极简陋），与 Bazel 精细化产物（6 个独立二进制）矛盾。
- **入口**：`run.sh` → `scripts/executor/make_functionsystem.py` → `build_bazel.py`——**官方走 Bazel**。
- **tests 仅 2 个 BUILD.bazel**：测试的 Bazel 迁移更落后。

**影响**：新人困惑"该用哪个"；两套构建需双倍维护；CMake 的 GLOB 单 main 与微服务式 6 二进制语义冲突，可能已实际废弃但未删。
**修复成本**：3-5 PM（二选一统一：要么删 CMake 全面 Bazel 并补 tests BUILD，要么反之；推荐保 Bazel 删 CMake）。

#### 4.2.2 自研 etcd 兼容层 + 手写 K8s 模型（中危，维护成本高）

- `functionsystem/src/meta_store/`（13K 行，82 文件）：`server/src/{kv,lease,watch,maintenance,election,backup}_service_actor.cpp` + `passthrough/*`。`meta_store_common.h` 硬编码 `META_STORE_CLUSTER_ID=123456`/`MEMBER_ID=456789`/`REVISION=32`/`RAFT_TERM=2`——**本地是桩，非真 Raft**；真一致性走 `KvServicePassthroughActor`（持 `etcdClient`）转发 etcd。
- `functionsystem/src/common/kube_client/`：**115 个手写 K8s REST 模型 cpp**（`V1Pod/V1Deployment/V1SeccompProfile/...`），手写 JSON 序列化，非官方 client-go/C++ k8s client。

**影响**：13K 行 etcd 兼容层增加理解与维护成本（虽然降低"重造 Raft 轮子"的严重性，因为它只是适配+桩）；手写 K8s 模型在 K8s API 演进时需逐字段手工同步，**长期必失同步**（这是最重的隐性债）。
**修复成本**：演进式替换 6-10 PM（meta_store 逐步瘦身为薄适配或直连 etcd；kube_client 逐步替换为官方 k8s client——但 C++ 无一等公民官方 client，或迁 cpp-redis/cpp-restio 风格第三方，需评估）。

#### 4.2.3 sandboxd 与旧 runtime_executor 并存（迁移未竟）

- 旧：`runtime_manager/executor/runtime_executor.cpp`（2381 行）。
- 新：`runtime_manager/executor/sandboxd/sandboxd_executor.cpp`（1704 行）+ `sandboxd_checkpoint_orchestrator.cpp` + `runtime-launcher`（Go，`SandboxService` gRPC）。
- 提交 `!334 feat[sandboxd]：同步sandbox执行器与运行时管理能力`、`!355 feat[runtime-manager]:Faas support supervisor to launch runtime`——**正在迁移中**。

**影响**：两条路径并存→行为不一致、测试覆盖分散、新人难判断该跟哪条。Traefik 路由（`traefik-http-provider-design.md`）已接入新 sandboxd，但旧路径可能仍在用。
**修复成本**：2-3 PM（完成迁移收尾、下线旧路径或明确各自治域）。

#### 4.2.4 巨型上帝类（中危，可维护性差）

| 文件 | 行数 | 承担职责（过载） |
|---|---|---|
| `function_proxy/local_scheduler/instance_control/instance_ctrl_actor.cpp` | 7394 | 实例生命周期+调度校验+亲和+租户配额+心跳+健康+IAM/token/aksk+call result 转发+状态机 GC+driver 事件（十余职责） |
| `function_proxy/local_scheduler/instance_control/instance_ctrl_test.cpp` | 6405 | 镜像巨测 |
| `function_master/scaler/scaler_actor.cpp` | 3356 | K8s Deployment/Pod 全套 CRUD+迁移+污点+资源池 |
| `runtime_manager/executor/runtime_executor.cpp` | 2381 | 运行时启动/停止/检查点/conda/pip |
| `function_proxy/local_scheduler/function_agent_manager/function_agent_mgr_actor.cpp` | 2216 | agent 管理 |
| `function_agent/agent_service_actor.cpp` | 2034 | agent 服务 |

**影响**：违反 SRP，修改一处易引入回归；测试镜像巨型（改一行要跑 6405 行测试）；阅读理解成本高。
**修复成本**：4-6 PM（首批拆 instance_ctrl_actor 与 scaler_actor，按职责切分为若干小 actor；用 specs/ 流程）。

### 4.3 代码与文档包袱

- **顶层文档缺失**：无顶层 ARCHITECTURE.md、无 CONTRIBUTING、无 CHANGELOG；知识散落在 `specs/`、`docs/`、`gc_actor/DESIGN.md`、PR 描述中。**修复成本**：1-2 PM（撰写顶层架构 + 贡献者指南 + 变更日志骨架）。
- **`.clang-format` 为空文件**：虽有 `scripts/format_code.py`，但格式配置缺失，风格一致性靠人工。**修复成本**：0.1 PM。
- **中文注释/标识符混杂**：国产项目，部分注释与 commit message 中文（如 `删除文件 README.en.md`），与英文代码混用——对国际化协作有阻力，但非致命。
- **补丁式提交占比高**：fix ~34%（256+ fix 提交），且大量 `fix(sandbox)/fix(bazel)/fix(codecheck)` 集中在近月——说明新功能（sandbox/bazel 迁移）在引入并修补，属正常迁移阵痛，但需观察是否长期不收敛。
- **TODO/FIXME 极少（强正面）**：全仓（排除 vendor）TODO/FIXME/XXX/HACK 仅 **14 处**——对 41 万行项目惊人干净，说明团队纪律性强、不积压债注释。样本：`snapshot_scheduler.cpp:58`、`request_dispatcher.cpp:487`。
- **version 管理**：`version.h` 被 `.gitignore` 忽略（构建时生成），`VERSION` 文件记 `0.7.0.dev` 而 README 标 `0.8.0.dev`——版本信息不一致。

### 4.4 生态与供应链包袱

- **华为云强绑定**（详见 0.3.5）：CI 镜像、Bazel redirect、OBS 依赖下载、部署依赖全家桶+Jiwenbox。**修复成本**：2-3 PM（镜像替换为公共/自建、redirect 改为可配置、依赖源去华为云化）。
- **vendor 预编译产物来源不透明**：`vendor/output/Install/*` 大量预编译库（spdlog/obs/curl/grpc/protobuf/absl/openssl/otel 等），由 `run.sh`→`download_vendor.py`→`vendor_cache.py` 拉取，但产物构建链需从原团队获取。**修复成本**：含在 3.2.1 谈判前置条件中。

### 4.5 测试与可观测包袱（轻）

- 测试覆盖扎实（0.40 比、gmock 204 文件），obs/metrics 有 OpenTelemetry 集成 + 2 个 Grafana dashboard——**这层债轻**，是接纳的正面信号。
- 唯一缺口：集成测试 `tests/integration` 规模小于 unit，端到端覆盖待加强（1-2 PM）。


## 第伍章 工作量估算与持续演进路线（结合前沿趋势）

### 5.1 工作量估算方法与假设

- **单位**：人月（PM），1 PM = 1 名工程师 1 个月的有效产出。
- **估算依据**：源码规模（41.4 万行）、历史包袱项数与修复难度（第肆章）、子系统复杂度（litebus/meta_store/调度三级自研需消化）、可比项目（K8s 子系统、Mesos、OpenFaaS 等的维护经验）。
- **人力画像假设**：团队含 ≥2 名 C++ 分布式 + K8s 复合工程师、1 名安全工程师、1 名 SRE/构建工程师、1 名文档/PM；3-5 人专职。
- **不确定性**：估算区间上下限反映"原团队协作度"与"业务场景分摊"两个变量。

### 5.2 总工作量（首年）

| 阶段 | 时间窗 | 工作量 | 核心产出 | 通过门 |
|---|---|---|---|---|
| **门 1·DD 尽职调查** | 第 0-0.5 月 | 1-2 PM | 验证硬骨头（CI 复现/构建链/sandboxd/安全/上游协作） | → 门 1 |
| **T0 接纳准备** | 第 0.5-2 月 | 4-6 PM | 自有 CI 复现构建、最小可用集群、安全审计、顶层架构文档 v1 | → 门 2 |
| **T1 稳定化** | 第 2-6 月 | 8-12 PM | P0 安全债清零、首批巨型类拆分、构建统一、可发版 | → 门 3 |
| **T2 持续演进** | 第 6-12 月 | 15-25 PM | meta_store/kube_client 现代化、前沿趋势对齐、生态去华为云化 | 长期承诺 |
| **合计** | **首年** | **28-45 PM** | — | — |

> 约合 **3-5 人专职团队一整年**。若原团队协作顺畅（给齐 CI/构建脚本/路线图/脑图），取下限；若需自行逆向，取上限。

### 5.3 T0-T2 任务分解（可直接排期）

#### T0 接纳准备（4-6 PM）
1. 知识转移与架构脑图（1 PM）——含向原团队索取：CI 镜像 Dockerfile、vendor 构建脚本、sandboxd 路线图、安全已知清单。
2. CI/构建可复现（1.5 PM）——脱华为云镜像、去 redirect 华为云、本地 distdir+repository_cache 验证。
3. 最小可用集群部署（1.5 PM）——基于 `scripts/deploy/function_system/install.sh` + third_party etcd，跑通 function_master+proxy+runtime_manager。
4. 安全审计（1 PM）——聚焦 4.1 的命令注入/crypto/sandbox 边界。
5. 顶层架构文档 v1（0.5-1 PM）。

#### T1 稳定化（8-12 PM）
1. P0 安全债清零（2-4 PM）——code_deployer/network_tool 改 execvp 数组传参；crypto 接入 OpenSSL 或显式外接声明；sandbox 边界审计修复。
2. 构建系统统一（3-5 PM）——二选一，推荐保 Bazel 删 CMake，补齐 tests 的 BUILD.bazel，去华为云 redirect。
3. 首批巨型类拆分（2-3 PM）——`instance_ctrl_actor` 按"生命周期/调度校验/心跳健康/IAM/转发"拆为 5-6 个小 actor；`scaler_actor` 按"Deployment CRUD/Pod 迁移/污点/资源池"拆。用 specs/ 流程保 TDD+TSan。
4. 补 CONTRIBUTING/CHANGELOG/ARCHITECTURE 顶层文档（0.5 PM）。
5. 端到端集成测试加强（1-2 PM）。
6. 首个自管发版（0.5 PM）——v0.9.0 自有 release。

#### T2 持续演进（15-25 PM，结合前沿趋势）

**演进方向必须对齐当前前沿（2026 年视角）**，否则维护只是"保活"，无法增值：

1. **AI Agent / LLM 函数编排**（4-6 PM）：openYuanrong 的"函数天然相互调用"已是 Agent 编排的好底座。演进：支持长时运行 Agent 实例、工具调用链、流式输出、与 MCP/主流 Agent 框架（LangGraph/AutoGen 风格）互操作；GPU/NPU 异构调度（proto 已有 VECTORS/affinity 基础）。
2. **Wasm 函数运行时**（3-5 PM）：补 Wasm（Wasmtime/Wasmer）作为第四种语言运行时——冷启动毫秒级、沙箱天然安全（替代/补强当前 std::system 部署的不安全面），契合 Serverless 趋势。
3. **可观测性现代化**（2-3 PM）：已有 OpenTelemetry+Grafana，演进为 eBPF 级内核观测（对齐 Pixie/Parca）、结构化日志（已有 common/logs）、分布式追踪贯通 master→proxy→runtime→launcher。
4. **meta_store/kube_client 换骨**（3-5 PM）：meta_store 瘦身为薄 etcd 适配或直接走 etcd；kube_client 评估换维护更活跃的第三方 C++ K8s client 或用 OpenAPI codegen 生成——根除手工同步 K8s API 的隐性债。
5. **去华为云绑定**（2-3 PM）：CI 镜像改自建或换公共源、依赖下载脱离 OBS、部署解耦 Jiwenbox（或文档标为可选）。
6. **安全合规收尾**（1-2 PM）：接 KMS/HSM、默认启用 seccomp profile（kube_client 已有 V1SeccompProfile 模型）、SBOM 持续生成。
7. **性能与规模**（1-3 PM）：jemalloc 已可选、profile 能力（common/profile 已有）、大规模（万级实例）压测与调优。

### 5.4 第二年及以后（演进而非维护）

若首年通过三道门，第二年应转向差异化竞争。把 openYuanrong 的"统一 Serverless 架构，AI/大数据/微服务通吃"做成卖点，对接三块：
- **K8s 生态**：做 K8s 之上的 Serverless 层（与 Knative/OpenFaaS 同台，但底座是分布式调度，不是软肋）。
- **AI 基础设施**：做 AI Agent 和推理负载的弹性调度层，与 Ray/vLLM 调度互补。
- **边缘计算**：三级调度天然契合"中心-域-边缘"拓扑，domain_scheduler 可改造成边缘域调度器。

第二年起年均维护+演进约 **15-25 PM**（小于首年，因债已收敛）。

### 5.5 ROI 模型（粗算）

| 情景 | 首年成本 | 3 年累计收益（估值） | 净 ROI | 判断 |
|---|---|---|---|---|
| 全门通过+有 Serverless 业务 | 28-45 PM | 平台能力沉淀+品牌+业务分摊（等价 80-150 PM 价值） | 正 | 接纳 |
| 无业务分摊纯维护 | 28-45 PM | 仅品牌+技术储备（等价 10-20 PM） | **负** | 否决或仅用上游 |
| 中途门失败止损 | 4-12 PM | 沉没但可控 | 中性 | 阶段决策 |


## 第陆章 最终建议：有条件接纳

### 6.1 结论

**建议：有条件接纳（Adopt with Conditions）**。

这不是一个"烂项目"——恰恰相反，它的工程素养（PR 流程、ADR/spec 文化、测试纪律、架构宪章）**优于绝大多数同类国产项目**，技术与战略价值真实存在。但它**不是一个能"零成本接管"的项目**——它背负双构建、自研 etcd/kube_client、巨型类、命令注入安全债、华为云强绑定五类包袱，且仍在 sandboxd 迁移的半途。

因此决策不应是"接 or 不接"，而是**"以什么前置条件、什么节奏、什么退出机制接"**。

### 6.2 接纳的前置条件（必须满足才进入 T0）

1. **原团队知识转移到位**：CI 镜像 Dockerfile 源、vendor 预编译产物构建脚本、sandboxd 完成路线图、安全已知清单、架构脑图——零成本但价值等同数月人力。**不给则砍价或放弃。**
2. **可脱华为云复现 CI**：验证在自有环境（公共镜像源+自建 distdir）能完整构建与测试。
3. **上游协作通道保留**：维持与 openEuler/原壤上游的可同步分支与 PR 协作机制，不立即不可逆 fork。
4. **团队人力到位**：≥2 名 C++ 分布式 + K8s 复合工程师 + 1 安全工程师（或可借调）。
5. **有 Serverless/AI 平台业务场景分摊成本**：纯维护无业务则 ROI 为负。

### 6.3 三道门阶段化决策

- 门 1（DD，2 周，1-2 PM）→ 验证硬骨头，失败即止损。
- 门 2（T0，1-2 月，4-6 PM）→ 能独立构建+跑通+安全审计，失败即止损。
- 门 3（T1，2-4 月，8-12 PM）→ P0 债清零+可发版，才承诺长期 T2。
- 每道门设明确红线（3.2.3），触发即退出，沉没成本可控。

### 6.4 接纳后的优先级（首年排期）

按"风险降序、回报可见度降序"排：
1. 安全债清零（P0，命令注入+crypto）——风险最高、修复快、回报立竿见影。
2. 构建系统统一（去双轨、去华为云）——消除认知二义性与供应链风险。
3. 补顶层文档（ARCHITECTURE/CONTRIBUTING/CHANGELOG）——降低后续人力门槛。
4. 首批巨型类拆分（instance_ctrl/scaler）——用 specs/ TDD 流程，稳扎稳打。
5. sandboxd 迁移收尾——明确新旧路径治域。
6. 前沿对齐（AI Agent 编排/Wasm 运行时/eBPF 观测）——增值而非纯维护。
7. meta_store/kube_client 换骨——根除隐性长尾债。

### 6.5 否决情景（何时说不）

- 若团队无 C++ 分布式人力、或无 Serverless 业务场景分摊 → **否决，仅用上游发行版**。
- 若门 1 验证发现 CI 不可脱华为云、或上游拒绝协作、或安全审计有 RCE 级未修复且无响应 → **否决**。
- 若谈判阶段原团队拒绝给 CI/构建脚本/路线图 → **否决或大幅压价**（知识不透明=接管即踩雷）。

### 6.6 一句话给决策者

> **这是一个值得接、但必须"先谈条件、再分门、按红线止损"的项目。** 它的下限是"接了个华为系半成品 Serverless 引擎"，上限是"沉淀成团队自有的国产分布式调度底座+AI Agent 编排平台"。决定上下限的不是项目本身，而是你团队的**人力画像、业务场景、谈判能力**。

---

## 附录 A：评估方法与证据可复现性

- 本报告所有结论基于源码级实测：`git log` 全量考古（1006 提交）、`find/wc/grep` 定量扫描、关键文件 `Read`、多 Agent 并行子系统纵深。
- 所有 file:line 引用均可在本仓对应路径复核。
- 报告生成日：2026-08-05；评估对象版本：master@2ddb8f17（VERSION 0.7.0.dev）。

## 附录 B：子 Agent 纵深勘察索引

7 个并行子 Agent 分别覆盖：①litebus 异步框架 ②function_master 全局调度 ③function_proxy 本地调度 ④runtime_manager+sandboxd ⑤domain_scheduler+function_agent+iam ⑥meta_store+common ⑦构建/CI/部署 + 历史包袱定量扫描。其结论整合于第贰章与第肆章。


