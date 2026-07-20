# openYuanrong（元戎）Serverless 分布式计算引擎：架构、原理与上下层诉求
---

## 摘要（中文）

openYuanrong（元戎）是 openEuler 社区孵化的 Serverless 分布式计算引擎，以"函数"为核心概念抽象，将传统 Serverless 函数概念泛化为可表达任意分布式应用运行实例的通用编程单元，起到类似单机操作系统中进程的作用。本文以 openYuanrong 为案例，系统剖析其三层子系统架构：多语言函数运行时提供 Python/Java/C++ 分布式编程接口与类单机编程体验；函数系统提供大规模分布式动态调度、极速弹性扩缩与跨节点迁移；数据系统提供基于 HBM/DRAM/SSD 的异构分布式多级缓存，支撑函数间高性能数据共享与传递。文章进一步论述 openYuanrong 向上对 Serverless/FaaS/BaaS 范式的支撑价值：通过将函数间数据传递从外部存储介质转移到近计算共享内存与异构对象直通通道，消解传统 Serverless 的数据传输瓶颈与冷启动开销；向下分析其对设备（昇腾 NPU、HBM、HCCS/RoCE）和操作系统（openEuler、共享内存、RDMA、Kubernetes）的诉求。最后讨论系统当前局限与演进方向。

**关键词：** Serverless, FaaS, 分布式计算, 多级缓存, 异构对象, openEuler, 元戎

---

## 1 引言

### 1.1 问题背景与研究动机

Serverless 计算范式自 AWS Lambda 问世以来，以"按需付费、零运维、自动弹性"的承诺改变了云原生应用的构建方式。然而，传统 FaaS 平台在实践中暴露了三个结构性瓶颈：

1. **冷启动延迟**。函数实例从零到可用需要经历容器拉起、运行时初始化、代码加载等阶段，延迟可达数百毫秒至数秒，对延迟敏感型应用构成障碍 [1]。
2. **数据传输瓶颈**。函数间数据传递依赖外部对象存储（如 S3）或消息队列，引入"存储税"：每次数据经过外部介质均产生 I/O 延迟与吞吐折损。这一瓶颈在分布式函数链、流式处理、大模型参数分发等场景中尤为突出 [2]。
3. **编程体验割裂**。FaaS 平台要求开发者显式处理分布式逻辑（事件触发、状态外部化、异步编排），与单机编程模型差距显著，增加了心智负担与出错概率 [3]。

openYuanrong 的设计动机正是回应这三重瓶颈。它不是又一个 FaaS 平台，而是一个将 Serverless 理念延伸到分布式计算底层的引擎：以"函数"为统一抽象，让开发者用单机编程的方式构建分布式应用，同时在引擎层解决数据传递和弹性调度问题。

### 1.2 案例选择与研究问题

openYuanrong 作为案例具有两个独特价值：其一，它是 openEuler 社区孵化项目（Apache 2.0 许可证），源码完全开放，可供深入剖析实现细节；其二，它的架构设计同时对齐了 Serverless 上层需求和异构硬件下层诉求，为理解"从应用范式到设备特性"的纵向穿透关系提供了完整标本。

本文聚焦两个研究问题：

- **RQ1**：openYuanrong 的整体架构、核心原理与关键功能实现是什么？
- **RQ2**：openYuanrong 向上如何支撑 Serverless 范式的价值诉求，向下对设备和操作系统提出了哪些诉求？

### 1.3 论文结构

第 2 节建立 Serverless/FaaS/BaaS 的理论框架。第 3 节描述 openYuanrong 的整体架构与关键概念。第 4 节逐层剖析三个子系统的原理与实现。第 5 节论述向上对 Serverless 的支撑。第 6 节分析向下对设备与操作系统的诉求。第 7 节讨论局限与未来方向。第 8 节总结全文。

---

## 2 文献脉络：Serverless、FaaS 与 BaaS

### 2.1 Serverless 计算的定义与演进

UC Berkeley RISELab 的综述论文将 Serverless 计算定义为："云编程简化——开发者只需关注业务逻辑，而不必关心集群管理、调度、扩缩容等运维问题" [3]。这一定义揭示了 Serverless 的本质不是"无服务器"，而是将服务器管理责任从用户转移到平台。

Serverless 的发展经历了两个阶段。第一阶段以 AWS Lambda 为代表，聚焦事件驱动的短期函数执行（FaaS），函数无状态、短暂存活、按调用计费。第二阶段涌现了 Dask [4]、SAND [5]、SEED [6] 等工作，试图将 Serverless 扩展到有状态、长时运行的分布式计算场景，但普遍面临数据传递效率和编程模型复杂度的挑战。

### 2.2 FaaS 的瓶颈与突破方向

FaaS 平台的核心瓶颈可归纳为三类：

- **冷启动**。AWS Lambda 的冷启动延迟在 2019 年的测量中可达 1-8 秒（取决于运行时与包大小）[7]。后续的 Firecracker MicroVM 快照恢复 [8]、保持存活（keep-alive）策略、预热并发（provisioned concurrency）等缓解措施各有代价：快照恢复需要内核协作，保持存活浪费资源，预热并发需要用户预估流量。
- **数据传输**。函数间数据必须经由外部存储中转，Berkeley 论文称之为"存储税" [3]。SAND [5] 提出在同一节点内通过共享内存传输数据，但仅限于单节点场景；SEED [6] 引入本地缓存层，但缓存容量受限于单节点 DRAM。openYuanrong 的数据系统则将缓存延伸到集群级多级层次（HBM/DRAM/SSD），且支持异构对象（NPU HBM）的跨卡直通传输。
- **编程模型**。传统 FaaS 要求开发者以事件处理函数的方式编写代码，状态外部化到 DynamoDB 等 BaaS 服务，函数间通过 Step Functions 或消息队列编排。这种模型与单机编程的直觉相去甚远。openYuanrong 试图通过"有状态函数"和"数据对象/数据流"抽象，让开发者用类/函数的方式编程，运行时自动处理分布式语义。

### 2.3 BaaS 的角色与局限

BaaS（Backend as a Service）为 Serverless 应用提供数据库、存储、认证等后端能力，是 FaaS 的必要补充。然而，BaaS 服务本质上是独立的外部系统，每次调用仍涉及网络 I/O。openYuanrong 的数据系统将部分 BaaS 功能（分布式缓存、KV 存储、发布订阅）内置于引擎，以共享内存和近计算缓存的方式提供，避免了外部 I/O 的延迟代价。这并非取代所有 BaaS，而是在高频数据共享场景中提供更近的替代。

---

## 3 openYuanrong 整体架构与关键概念

### 3.1 系统定位

openYuanrong 定位为"Serverless 分布式计算引擎"，其核心目标是：以一套统一的 Serverless 架构支持 AI、大数据、微服务等各类分布式应用。它由三个子系统组成，可灵活单独或组合使用：

| 子系统 | 代码仓 | 核心职责 |
|--------|--------|----------|
| 多语言函数运行时 | `yuanrong` | 函数分布式编程，支持 Python/Java/C++，类单机编程体验 |
| 函数系统 | `yuanrong-functionsystem` | 大规模分布式动态调度，极速弹性扩缩与跨节点迁移 |
| 数据系统 | `yuanrong-datasystem` | 异构分布式多级缓存（HBM/DRAM/SSD），Object/Stream 语义 |

系统版本为 0.8.0.dev，以 Apache 2.0 许可证发布在 openEuler 社区（AtomGit/GitCode `openeuler` 组织），支持 x86_64 与 aarch64 两种架构。

### 3.2 核心概念抽象：函数

openYuanrong 最关键的概念创新是"函数"（openYuanrong Function）的泛化定义。根据官方词汇表：

> "openYuanrong 函数是分布式调度运行的基本单位。相比传统 Serverless 函数概念，openYuanrong 函数更加通用，支持运行中动态创建、长时运行、相互间异步调用、有状态等，可以表达任意分布式应用的运行实例，起到类似单机 OS 中进程的作用。" [9]

这一泛化在三个维度突破了传统 FaaS 函数的限制：

1. **有状态 vs 无状态**。传统 FaaS 函数强制无状态；openYuanrong 同时支持无状态函数（`@yr.invoke`）和有状态函数（`@yr.instance`）。有状态函数保持进程内私有变量（如静态变量、成员变量），方法调用按顺序执行，支持运行中状态读写。
2. **动态创建与长时运行**。传统 FaaS 函数生命周期由事件触发决定；openYuanrong 函数可在运行中通过 `invoke()` 动态创建，支持长时运行直到显式 `terminate()`。
3. **天然相互调用**。传统 FaaS 函数间调用需要外部编排；openYuanrong 函数可直接相互调用，调用返回数据对象引用，支持 Future 语义和引用传递。

从编程模型看，有状态函数映射为"类"（class），无状态函数映射为"函数"（function），开发者用单机编程方式编写类或函数，SDK 自动将其转换为分布式运行单元。Python 示例：

```python
@yr.instance
class Counter:
    def __init__(self):
        self.value = 0
    def increment(self, n):
        self.value += n
        return self.value

counter = Counter.invoke()  # 远端创建实例
ref = counter.increment.invoke(1)  # 异步调用
print(yr.get(ref))  # 获取结果
counter.terminate()  # 终止实例
```

### 3.3 数据抽象：数据对象与数据流

除函数抽象外，openYuanrong 还定义了两种数据原语，作为函数间数据传递的载体：

**数据对象（Object）**：跨节点分布式共享的内存数据。支持基于共享内存的高性能 `put/get` 访问。可作为函数调用参数和返回值自动分布式传递，并支持异步 Future 语义。openYuanrong 在运行中自动解析引用，通过分布式引用计数管理数据对象生命周期。

**数据流（Stream）**：跨节点分布式传递共享的有序无界内存数据集。支持基于共享内存的 `pub/sub` 访问，支持一对一、一对多、多对一等发布订阅模式。通过数据流可解耦多个函数间异步流式数据传递。

这两种数据原语将函数间通信从"经由外部存储中转"变为"经由引擎内置共享内存直传"，是 openYuanrong 消解 Serverless 数据传输瓶颈的核心机制。

### 3.4 集群角色模型

openYuanrong 集群分为两种节点角色：

- **主节点（Master）**：包含控制面和数据面。控制面组件包括 `function_master`（全局调度、实例管理、Traefik 路由注册）；数据面组件包括 `function_proxy`（本地调度）、`function_agent`（实例生命周期管理）、`runtime_manager`（运行时环境管理）和 `data_worker`（分布式缓存）。
- **从节点（Agent）**：只包含数据面。一台主机可部署多个从节点。

控制面组件通过 etcd 实现集群发现、健康检测、故障恢复和在线扩缩容。

---

## 4 子系统原理与关键实现

### 4.1 多语言函数运行时

#### 4.1.1 编程接口与 SDK

运行时 SDK 是用户与 openYuanrong 交互的入口。Python SDK 提供 `yr.init()`、`@yr.invoke`、`@yr.instance`、`yr.get()`、`yr.put()`、`yr.finalize()` 等接口。C++ SDK 提供 `RuntimeHandler` 抽象基类（用户实现 `HandleRequest`、`Initializer`、`PreStop` 方法）、`ObjectRef`（Future 式异步结果引用）和 `Context`（包含 trace ID、request ID、函数名、内存/CPU 配额等调用上下文）。Java SDK 通过 `faas-function-sdk` jar 包提供类似接口。

SDK 的关键设计是 `yr.init()` 的自动集群发现机制（源码 `src/libruntime/auto_init.cpp`）。当用户在非集群节点上调用 `yr.init()`，SDK 按以下优先级寻找集群：(1) 用户配置参数；(2) 环境变量 `YR_SERVER_ADDRESS` 和 `YR_DS_ADDRESS`；(3) 读取 `/tmp/yr_sessions/yr_current_master_info` 文件；(4) 执行 `yr start --master` 启动临时集群。临时集群在进程退出时自动销毁。这一机制使得开发者无需预先部署集群即可使用 openYuanrong。

#### 4.1.2 函数调用链路

函数调用涉及 SDK → `function_proxy` → runtime 实例的 RPC 链路。核心协议是 `RuntimeRPC` gRPC 双向流式 RPC（定义在 `src/libruntime/fsclient/protobuf/runtime_rpc.proto`），支持 `MessageStream` 和 `BatchMessageStream` 两种模式。消息类型覆盖 `CreateReq/InvokeReq/KillReq/CallResultReq/StateSaveReq/StateLoadReq/CheckpointReq/SignalReq/EventReq` 等，覆盖函数实例的完整生命周期。

在集群内（`in_cluster=true`），SDK 通过 `FSClient`（gRPC 客户端，源码 `src/libruntime/fsclient/fs_client.h`）连接同节点 `function_proxy`，proxy 路由到目标实例的 runtime 进程。在集群外（`in_cluster=false`），SDK 通过 `GwClient`（HTTP/WebSocket 客户端，源码 `src/libruntime/gwclient/gw_client.h`）连接 frontend 网关（端口 8888），走 `/serverless/v1/posix/instance/create|invoke|kill` RESTful 路径。

#### 4.1.3 并发模型

runtime 实例内部的并发使用 **boost::fibers**（M:N 用户级线程），而非传统 OS 线程（源码 `src/libruntime/fiber.h`）。`FiberPool` 在单个 OS 线程中调度多个 fiber：每个 fiber 任务通过 `unbuffered_channel` 入队，以 `fixedsize_stack` 分配栈空间，以 `FiberSemaphore` 控制并发上限。这一设计在单实例内实现了高并发处理能力，同时避免了 OS 线程创建和上下文切换的开销。

#### 4.1.4 沙箱隔离

openYuanrong 提供了沙箱（Sandbox）机制用于隔离的远端执行环境。沙箱不是独立的运行时实现，而是跨三个仓库协作的端到端能力：

- `yuanrong` 侧：SDK 提供 `yr.sandbox.create()` 高层封装，基于 `@yr.instance` 创建远端实例，支持 `exec()` 命令执行、端口转发和 reverse tunnel。
- `functionsystem` 侧：负责实例创建、runtime 环境变量注入（`YR_SERVER_ADDRESS`、`YR_DS_ADDRESS`、`INSTANCE_ID`）、端口映射和 Traefik 路由注册。
- `frontend` 侧：提供浏览器 WebTerminal 入口。

此外，openYuanrong 还提供 Rust sandbox runtime（`rrt`），作为轻量级隔离运行时。在 `deploy/sandbox/docker/services.yaml` 中，`rrt` 运行时槽位通过 `openyuanrong_rrt.runtime_path()` 获取可执行文件路径。

#### 4.1.5 函数服务模式

openYuanrong 函数可运行于两种模式：任务模式（一次性作业）和 Serverless 服务模式（长期运行、自动弹性）。`ApiType` 枚举（proto 定义）包含 `Function=0`（任务模式）、`Faas=1`（FaaS 服务模式）、`Posix=2`（POSIX 调用模式）和 `Serve=3`（服务模式）。SpringBoot 微服务可通过适配器 SDK 以接近零改动的方式迁移为 openYuanrong 函数服务运行，享受 Serverless 弹性与免运维优势（见 `docs/source_zh_cn/use_cases/microservice-serverless.md`）。

### 4.2 函数系统

#### 4.2.1 架构概述

函数系统是 openYuanrong 的控制平面，由以下组件构成：

- **function_master**：全局调度器，管理集群资源表、实例生命周期、Traefik 路由注册。提供 RESTful 接口：`/global-scheduler/resources`（资源查询）、`/instance-manager/named-ins`（命名实例查询）、`/global-scheduler/scheduling_queue`（调度队列）、`/global-scheduler/node/localschedulingstatus`（节点调度开关）。
- **function_proxy**：本地调度器，以 DaemonSet 方式部署在每个节点（`hostNetwork: true`），负责本地实例创建、路由转发、健康检测。支持与 function_agent 合并进程模式（`function_proxy_merge_process_enable`）以减少进程间通信开销。
- **function_agent**：实例管理器，与 runtime_manager 协同工作，负责函数实例进程的创建与销毁。
- **runtime_manager**：运行时环境管理器，负责拉取函数代码、构建运行时环境、注入环境变量（`INSTANCE_ID`、`YR_SERVER_ADDRESS`、`YR_DS_ADDRESS` 等）、启动 runtime 实例进程。
- **runtime_launcher**：容器启动器，支持 Docker 和 K8s 两种后端，通过 Unix domain socket 接收 runtime_manager 的容器创建请求。
- **frontend**：API 网关（Go 实现），提供 HTTP/WebSocket 接入，端口 8888。承担函数调用、认证（JWT/OAuth2 via Casdoor/Keycloak）、沙箱创建入口等职责。
- **meta_service**：元数据服务，管理函数注册、资源池配置。
- **function_scheduler**：调度策略服务，支持多副本部署实现高可用。
- **iam_server**：身份认证服务，支持 Casdoor 和 Keycloak 两种外部 IdP。

#### 4.2.2 调度与弹性

函数系统实现了两级调度架构：

- **全局调度**（function_master）：维护集群资源表，决定实例的节点分配。提供调度队列查询接口，可观测等待调度的实例及其资源需求和等待时长。
- **本地调度**（function_proxy）：在节点内执行实例创建和路由。支持通过 `/global-scheduler/node/localschedulingstatus` 接口将节点切换为 `evicting` 状态（停止接收新实例）或恢复为 `normal`。

弹性扩缩通过多种机制实现：(1) 函数实例的极速创建与销毁；(2) 通过 HTTP 接口触发实例扩缩（如推理实例扩容的 `/scaleout` 接口）；(3) 节点级调度开关控制流量疏散；(4) 运行时快照恢复（checkpoint `StateSaveReq/StateLoadReq`）加速实例启动。

#### 4.2.3 Traefik 路由集成

函数系统使用 Traefik 作为反向代理，为函数实例暴露 HTTP 服务端口。路由信息通过 HTTP Provider 方案提供：Traefik 定期轮询 `GET /global-scheduler/traefik/config` 端点拉取完整路由表。每个实例通过 `portForward` 扩展字段声明端口映射（`protocol:hostPort:containerPort` 格式），function_master 清洗实例 ID 后生成 `{safeID}-{sandboxPort}` 路由名称，注册到 Traefik。这一方案比 etcd provider 方案减少了 etcd 写放大和 TTL 续约开销。

### 4.3 数据系统

#### 4.3.1 架构概述

数据系统是 openYuanrong 的数据平面，由三个部分构成：

- **多语言 SDK**：提供 Python/C++ 接口，封装 heterogeneous object（异构对象）、KV、object 三类接口。
- **worker**：核心组件，分配管理 DRAM/SSD 资源和元数据，提供分布式多级缓存能力。
- **集群管理**：依赖 etcd，实现节点发现/健康检测、故障恢复及在线扩缩容。

部署视图中，每个节点部署一个 worker 进程并注册到 etcd，SDK 集成到用户进程中与同节点 worker 通过共享内存通信。worker 间通过 TCP/RDMA 传输数据（当前版本仅支持 TCP，RDMA/UB 即将支持）。异构对象 HBM 间通过 HCCS/RoCE 卡间直通传输。

#### 4.3.2 三类数据接口

数据系统提供三类接口，分别服务于不同场景：

**KV 接口**：基于共享内存的免拷贝 KV 操作，支持 `KVWrite/KVRead/KVDel/KVMSetTx/KVExist`。适用于微服务状态数据的内存级读写，Checkpoint 快速保存和加载。支持 `write_through`（写穿）、`write_back`（写回）和 `none`（无持久化）三种持久化策略，满足不同场景的数据可靠性需求。

**object 接口**：基于共享内存的近计算本地对象缓存，支持 `Put/Get/IncreGlobalReference/DecreGlobalReference`。实现函数间高效数据流转，支撑 Distributed Futures 编程模型。数据对象作为函数调用参数和返回值自动传递，运行时自动解析 Future 引用并管理分布式引用计数。

**heterogeneous object 接口**：基于 NPU 卡 HBM 内存抽象的异构对象接口。这是数据系统最具创新性的部分，提供以下能力：

- **H2D/D2H**：数据在 DRAM 与 HBM 之间的高速迁移。`MSetD2H` 将设备数据写回主机，`MGetH2D` 将主机数据加载到设备。
- **D2D（DevPublish/DevSubscribe）**：NPU 卡间数据直通传输。发布者通过 `DevPublish` 将 HBM 内存注册为异构对象，订阅者通过 `DevSubscribe` 获取数据，数据通过 HCCS/RoCE 卡间链路直接传输。传输完成后数据系统自动删除异构对象。
- **DevMSet/DevMGet**：D2D 模式的非自动删除版本，适用于需要多次访问的场景。
- **P2P 负载均衡**：跨节点 NPU 间传输支持 P2P 策略，充分利用卡间链路带宽。

#### 4.3.3 一致性模型与可靠性

数据系统支持两种数据一致性模型：

- **Causal 一致性**：保证因果顺序的可见性，适合需要因果推理的场景（如分布式训练中的参数更新顺序）。
- **PRAM（Pipeline Random Access Memory）一致性**：单进程写入顺序对所有进程可见，但不同进程的写入顺序不保证全局一致。适合对一致性要求较低、对性能要求较高的场景。

数据可靠性方面，热点数据跨节点读取时自动在本地保存副本（`enable_data_replication` 参数，默认开启），本地副本使用 LRU 策略自动淘汰。这一机制支撑热点数据高效访问，但不保障数据可靠性或可用性（文档明确标注其仅为性能优化机制）。

分布式元数据管理基于 etcd，支持系统水平线性扩展。动态资源伸缩时自动迁移数据，实现系统高可用。

#### 4.3.4 应用场景与实测效果

数据系统文档列出的应用场景覆盖 AI 推理、训练和微服务三大领域：

- **LLM 长序列推理 KVCache**：基于异构对象构建分布式 KVCache，实现 Prefill 阶段 KVCache 缓存和 Prefill/Decode 实例间 KVCache 快速传递。
- **模型推理实例 M→N 快速弹性**：利用异构对象卡间直通和 P2P 数据分发能力实现模型参数快速复制。实测在 Qwen2.5-7B 推理实例扩容场景中，首次冷加载模型约 15.8 秒，扩容实例通过 `dev_mget` 从已有实例 HBM 中同步模型参数仅约 1.5 秒，加速约 **10 倍** [10]。
- **强化学习模型参数重排**：卡间直通传输训练侧模型参数到推理侧。
- **训练场景 Checkpoint 快速保存及加载**：KV 接口快速写 Checkpoint 到二级缓存保证可靠性；恢复时各节点将 Checkpoint 分片加载到异构对象，利用 D2D 直通快速传递到各节点 HBM。
- **微服务状态数据快速读写**：KV 接口实现内存级读写微服务状态数据，支持持久化到二级缓存。

---

## 5 向上：对 Serverless 范式的支撑

### 5.1 消解数据传输瓶颈

传统 Serverless 的核心性能瓶颈在于函数间数据必须经过外部存储中转。openYuanrong 通过数据系统的三种机制直接消解这一瓶颈：

**近计算共享内存**。数据对象和 KV 接口基于共享内存实现免拷贝读写，函数实例与同节点 worker 之间通过共享内存传输数据，消除了网络 I/O 和序列化开销。这与 SAND [5] 的共享内存思路类似，但 openYuanrong 将其扩展到集群级：跨节点数据通过 worker 间 TCP/RDMA 传输后，在本地保存副本供后续访问，减少了重复跨节点传输。

**异构对象直通传输**。对于 AI 场景中大模型参数、KVCache 等数据，openYuanrong 通过 D2D 直通将数据从源 NPU HBM 直接传输到目标 NPU HBM，不经过主机 DRAM 中转。这一机制将模型弹性扩容的数据传输延迟从"从磁盘加载全部参数"的分钟级降至"HBM 直通复制"的秒级，实测 10 倍加速。

**数据流解耦**。数据流 pub/sub 模式解耦了数据生产者与消费者，实现异步流式传递。与传统 Serverless 中依赖 SQS/Kafka 等外部消息队列不同，数据流基于共享内存实现，延迟和吞吐显著优于网络消息队列。

### 5.2 减轻冷启动开销

openYuanrong 从两个层面减轻冷启动：

**运行时层面**。函数实例的 runtime 进程通过 `runtime_launcher` 拉起，支持 Docker 容器方式。runtime 实例进程启动后通过 gRPC `RuntimeRPC.MessageStream` 注册到 `function_proxy`，后续调用直接路由到已注册实例，无需再次创建。有状态函数的 `Initializer` 方法在实例启动时执行一次，后续调用直接执行 `HandleRequest`，避免了传统 FaaS 每次调用均需初始化的开销。

**数据层面**。对于 AI 推理等数据密集型场景，冷启动最耗时的环节是模型参数加载。openYuanrong 的异构对象机制实现了"一次冷加载，多次热复制"：首个实例冷加载模型参数后发布到数据系统，后续实例通过 `dev_mget` 从已有实例 HBM 直接获取参数，将模型加载时间从约 15.8 秒降至约 1.5 秒。

### 5.3 简化分布式编程体验

openYuanrong 的编程接口设计使分布式应用开发接近单机编程体验：

- **类即有状态函数**：Python 的 class 通过 `@yr.instance` 装饰后自动转为分布式有状态函数，成员变量保持状态，方法调用按顺序执行。
- **函数即无状态函数**：Python 的 function 通过 `@yr.invoke` 装饰后自动转为分布式无状态函数，支持并行异步调用。
- **数据对象引用传递**：函数调用返回数据对象引用（Future），引用可直接作为其他函数调用参数传递，引擎自动解析引用并管理生命周期，避免了显式序列化和数据传输代码。
- **零改动微服务迁移**：SpringBoot 微服务通过适配器 SDK 以接近零改动的方式迁移为 openYuanrong 函数服务，享受 Serverless 弹性与免运维。

这一编程体验与传统 FaaS 的"事件触发、状态外部化、编排链式调用"模型形成鲜明对比。开发者不再需要显式处理分布式语义，引擎层自动完成。

### 5.4 统一 Serverless 底座

openYuanrong 的"函数"泛化抽象使其可同时支撑三类分布式应用：

- **AI 应用**：大模型推理的弹性扩缩、强化学习的参数重排、训练的 Checkpoint 管理。
- **大数据应用**：数据流 pub/sub 实现流式处理，无状态函数并行化实现批处理。
- **微服务应用**：SpringBoot 迁移为函数服务，享受 Serverless 弹性。

这种"一套架构支撑三类场景"的定位，比传统 FaaS 平台（主要面向事件驱动微服务）或分布式计算框架（如 Spark，主要面向批处理）的单一场景定位更具通用性。

---

## 6 向下：对设备与操作系统的诉求

### 6.1 异构计算设备诉求

openYuanrong 数据系统的异构对象能力直接依赖昇腾 NPU 的以下硬件特性：

- **HBM（High Bandwidth Memory）**：NPU 卡内高带宽内存，作为异构对象的存储介质。openYuanrong 将 HBM 抽象为可编程对象，通过 `DevPublish/DevSubscribe` 在卡间共享。当前案例中 Qwen2.5-7B 推理实例的单卡 HBM 需求为 20GB（`vLLM_MODEL_MEMORY_USE_GB=20`）。
- **HCCS（Huawei Cache Coherence System）/ RoCE（RDMA over Converged Ethernet）**：NPU 卡间互联协议。同节点内多卡通过 HCCS 互联，跨节点通过 RoCE 互联。openYuanrong 的 D2D 直通传输利用这些协议实现 NPU 间数据高速传递。
- **HCCL（Huawei Collective Communication Library）**：华为集合通信库，openYuanrong 的异构对象传输自动协调 HCCL 收发顺序，实现卡间异步并发传输。P2P 传输负载均衡策略充分利用卡间链路带宽。

在部署层面，容器需要映射 `/dev/davinci*`（NPU 设备）、`/dev/davinci_manager`、`/dev/devmm_svm`、`/dev/hisi_hdc` 等设备文件，并挂载 `/usr/local/dcmi`、`/usr/local/Ascend/driver/lib64/` 等驱动路径。这些要求意味着 openYuanrong 的异构对象能力只能在昇腾 NPU 环境中使用。

当前版本未直接支持 GPU（CUDA/NVIDIA）的异构对象抽象，但架构设计（`HeteroClient` 的设备抽象层）预留了扩展空间。

### 6.2 操作系统诉求

openYuanrong 对操作系统的诉求体现在三个层面：

**Linux 内核能力**：
- **共享内存**：数据系统的 KV/object 接口基于共享内存（`shm`）实现免拷贝读写，依赖 POSIX 共享内存 API 和 `/dev/shm` 文件系统。K8s 部署中 Pod 需要挂载 `/dev/shm` 并配置足够的共享内存大小（如推理场景需 `--shm-size=64g`）。
- **RDMA/UB**：数据系统文档标注"RDMA/UB 即将支持"，当前版本仅使用 TCP。RDMA 支持将依赖 `rdma-core` 库和内核 RDMA 子模块，是高性能跨节点传输的关键。
- **进程管理**：`runtime_manager` 和 `function_agent` 需要创建和管理子进程，依赖 `fork/exec`、信号处理（`SIGTERM/SIGKILL`）、进程组管理等标准 POSIX 进程管理能力。

**openEuler 发行版**：
- openYuanrong 作为 openEuler 社区孵化的项目，其编译镜像基于 openEuler 22.03（`ci/openeuler/Dockerfile.x86_64`），运行时镜像基于 Ubuntu 22.04。openEuler 提供的昇腾驱动、HCCL 库和内核优化（如 eBPF、io_uring 等现代内核特性）是 openYuanrong 高性能运行的基础环境。
- glibc 版本要求 2.34+（datasystem pip 安装前置条件），对应 openEuler 22.03 SP3+ 或 Ubuntu 22.04+。

**Kubernetes 容器编排**：
- openYuanrong 的生产部署依赖 K8s（Helm chart），核心组件分布为：function-master Deployment、function-proxy DaemonSet（`hostNetwork: true`）、function-agent+runtime-manager Deployment、frontend Deployment。
- 关键 K8s 特性需求：`hostNetwork`（function-proxy 需要直接使用主机网络以减少 NAT 开销）、`hostPort`（数据系统 worker 和 function-proxy 的端口需要直接暴露）、`privileged`（sandbox 和 runtime_launcher 需要 Docker-in-Docker 能力）、Linux capabilities（`cap_net_admin/cap_net_raw` 用于 function-agent 的 iptables 操作，`cap_dac_override/cap_sys_admin/cap_kill/cap_setgid/cap_setuid` 用于 runtime_manager）。
- etcd 作为集群管理的核心依赖，提供节点发现、健康检测、故障恢复和在线扩缩容。

### 6.3 部署模型与资源诉求

openYuanrong 提供三种部署模型，对底层环境的诉求递增：

| 部署模型 | 最低环境 | 适用场景 |
|----------|----------|----------|
| 进程部署（`yr start`） | 单台 Linux 主机，etcd | 本地验证、轻量级场景 |
| K8s Helm 部署 | K8s 集群 + etcd + Helm | 生产部署，完整控制面 |
| Sandbox AIO | Docker + privileged | 开发测试、单机体验 |

端口分配方面，控制面端口范围 10000-20000（function-master 22770/22668、ds-master 12123、etcd 32379），数据面端口范围 20000-40000（function-proxy 22772/22423、function-agent 58866、ds-worker 31501、frontend 8888）。

---

## 7 讨论：局限与演进

### 7.1 当前局限

openYuanrong 仍处于 0.8.0.dev 版本，存在若干局限：

**异构对象仅支持昇腾 NPU**。当前 D2D 直通传输依赖 HCCL 和昇腾 HBM 抽象，不支持 NVIDIA GPU/CUDA。跨硬件平台的异构对象抽象需要额外的适配层。

**RDMA/UB 尾未闭环**。数据系统跨节点传输当前仅支持 TCP，RDMA 和 UB（Unified Bus）标注为"即将支持"。跨节点数据传输的延迟和吞吐仍有优化空间。

**数据可靠性有限**。热点数据副本机制仅为性能优化（LRU 淘汰、不保障可靠性），真正的数据可靠性依赖 `write_through/write_back` 持久化策略和 etcd 元数据管理。在极端故障场景下（如节点同时故障），数据可能丢失。

**安全与多租户**。当前支持 Casdoor/Keycloak 认证和 JWT/OAuth2 授权，但文档未详细描述网络隔离、资源硬隔离（如 cgroup 配额强制）等安全机制。多租户场景下的资源竞争和安全边界需要进一步强化。

### 7.2 演进方向

基于源码和文档的分析，openYuanrong 的演进方向包括：

**跨硬件异构对象扩展**。`HeteroClient` 的设备抽象层预留了多硬件支持空间。CUDA GPU 的 HBM（如 NVIDIA H100 的 80GB HBM3）可作为下一个异构对象目标，需要适配 NCCL 集合通信库和 CUDA IPC 机制。

**RDMA/UB 闭环**。数据系统的 worker 间 RDMA 传输将显著提升跨节点数据传输吞吐，对于大规模分布式训练和推理场景尤为关键。

**Serverless 自动弹性**。当前弹性扩缩主要通过手动触发（如 `/scaleout` 接口），完整的 Serverless 体验需要基于负载指标的自动弹性策略（如基于 QPS 的自动扩缩、基于空闲时间的自动缩容）。

**更完善的 BaaS 服务层**。数据系统的 KV 接口已覆盖部分 BaaS 能力（状态存储、发布订阅），但完整的 BaaS 还需要数据库服务、对象存储服务、认证服务等。openYuanrong 可通过数据系统扩展更多内置 BaaS 能力，减少对外部服务的依赖。

---

## 8 结论

openYuanrong 以"函数"泛化抽象为核心，构建了一个三层子系统协同的 Serverless 分布式计算引擎。其架构原理的关键在于：(1) 将传统 Serverless 函数扩展为可表达任意分布式应用实例的通用编程单元；(2) 通过近计算共享内存和异构对象直通消解函数间数据传输瓶颈；(3) 通过两级调度和 runtime 快照恢复减轻冷启动开销；(4) 通过数据对象 Future 引用和数据流 pub/sub 简化分布式编程体验。

向上，openYuanrong 对 Serverless 范式的支撑价值体现在三个维度：消解数据传输瓶颈（10 倍加速实测）、减轻冷启动开销（有状态函数避免重复初始化 + 异构对象热复制）、简化编程体验（类单机编程接口）。向下，其对昇腾 NPU（HBM/HCCS/RoCE/HCCL）的依赖使异构对象能力只能在特定硬件上实现，对操作系统（共享内存、RDMA、K8s hostNetwork/privileged）的诉求使部署环境有明确门槛。

openYuanrong 仍处于早期阶段，异构对象跨硬件支持、RDMA 闭环、自动弹性策略等演进方向将决定其能否从"openEuler 社区项目"成长为"通用 Serverless 分布式底座"。

---

## 参考文献

[1] J. M. Hellerstein et al., "Serverless Computing: One Step Forward, Two Steps Back," *arXiv preprint arXiv:1812.03697*, 2018.

[2] V. Shankar et al., "Serverless Data Processing," *CIDR 2023*, 2023.

[3] E. Jonas et al., "Cloud Programming Simplified: A Berkeley View on Serverless Computing," *arXiv preprint arXiv:1902.05862*, 2019.

[4] M. Rocklin, "Dask: Parallel Computation with Blocked Algorithms and Task Scheduling," *Proceedings of the 14th Python in Science Conference*, 2015.

[5] I. E. Akkus et al., "SAND: Towards High-Performance Serverless Computing," *USENIX ATC 2018*, 2018.

[6] A. Klimovic et al., "SEED: Accelerating Serverless Applications with Heterogeneous Storage," *IEEE Micro*, vol. 40, no. 4, pp. 42–49, 2020.

[7] S. Wang et al., "Characterizing and Optimizing Serverless Cold Starts at Major Cloud Providers," *arXiv preprint arXiv:2006.09206*, 2020.

[8] A. Agache et al., "Firecracker Lightweight Virtualization for Serverless Applications," *NSDI 2020*, 2020.

[9] openYuanrong 项目, "词汇表 — openYuanrong 函数," https://docs.openyuanrong.org/zh-cn/latest/reference/glossary.html, 2025.

[10] openYuanrong 项目, "推理实例模型加载速度 10 倍提升," https://docs.openyuanrong.org/zh-cn/latest/use_cases/accelerate_llm_instance_scaling.html, 2025.

[11] openYuanrong 项目, "openYuanrong datasystem README," https://atomgit.com/openeuler/yuanrong-datasystem, 2025.

[12] openYuanrong 项目, "Function-master 扩缩容运维接口," https://atomgit.com/openeuler/yuanrong-functionsystem, 2025.

[13] openYuanrong 项目, "Sandbox 实现综述," yuanrong/docs/features/sandbox-implementation.md, 2025.

[14] openYuanrong 项目, "Traefik HTTP Provider 设计," yuanrong-functionsystem/docs/traefik-http-provider-design.md, 2025.

[15] openYuanrong 项目, "auto_init.cpp — SDK 自动集群发现," yuanrong/src/libruntime/auto_init.cpp, 2025.

[16] openYuanrong 项目, "libruntime.proto — RuntimeRPC 定义," yuanrong/src/proto/libruntime.proto, 2025.

[17] openYuanrong 项目, "fiber.h — FiberPool 并发模型," yuanrong/src/libruntime/fiber.h, 2025.

[18] openYuanrong 项目, "gw_client.h — GwClient 网关客户端," yuanrong/src/libruntime/gwclient/gw_client.h, 2025.

[19] openYuanrong 项目, "fm_client.h — FMClient Function Master 客户端," yuanrong/src/libruntime/fmclient/fm_client.h, 2025.

[20] openYuanrong 项目, "MGetH2D/MSetD2H Multi-Buffer Python API 设计," yuanrong-datasystem/docs/design/mget_mset_multi_buffer_python_api.md, 2025.
