# Paper Configuration Record

| Field | Value |
|---|---|
| Paper type | Technical research report / survey paper |
| Title | 华为云 ModelArts V2.0 深度研究：业务背景、技术架构、集群实践与改进路径 |
| Version | V2.0 |
| Date | 2026-07-03 |
| Discipline | Cloud infrastructure / AI systems engineering |
| Structure | Survey-style: Background → Challenges → Architecture → Key Technologies → Cluster ops → Competitive → Improvements → Discussion → Limitations → Conclusion → Code Examples → Troubleshooting |
| Citation format | IEEE (numbered, [n] superscript) |
| Output format | Markdown (single file) |
| Language | Simplified Chinese (technical terms kept in English) |
| Abstract | Bilingual (zh-CN + EN) |
| Word count target | ~28000 CJK characters |
| References | 68 entries (IEEE format) |
| Chapters | 12 chapters + references + appendix (6 sections) |
| Mode | lit-review / survey (deep-research-derived) with engineering handbook |
| Style | No AI-typical filler terms; varied paragraph rhythm; em dash ≤2/page |

## Chapter List (V2.0)

1. 业务背景（4子节：市场格局/全栈AI战略/芯片演进/研究定位）
2. 六大问题挑战（每类含子问题+工程案例）
3. 三层技术架构（算力层/平台层/工具链层，含服务器/网络/调度/device plugin/EYWA/MindSpeed vs Megatron/CANN演进/torch_npu劫持）
4. 关键技术深度剖析（MoXing API/HCCL算法与ranktable/故障码与五级自愈/checkpoint格式）
5. 集群端到端实践（10步流程）
6. 竞品对比分析（全球三巨头对比+国内竞品对比）
7. 七条改进路径（含§7.8昇腾接口可用性前置评估）
8. 讨论（工程哲学/全栈优劣势/MFU之外/超节点影响）
9. 局限与未来工作
10. 结论
11. 代码与配置示例集（6节：训练脚本/Volcano YAML/run.sh/ranktable/Dockerfile/异步CKPT）
12. 常见问题排查手册（7节：5镜像问题/5通信问题/5调度问题/4性能问题/6故障码/工具位置表/上报checklist）

## Scope locked
- Business background: IDC/Gartner 2025-2026 MLaaS data (AWS 31%, Azure 28%, GCP 21%, HWC 27% domestic), Huawei full-stack AI strategy, Ascend 910B→910C→910D evolution
- Challenges: heterogeneous scheduling, communication bottleneck, fault frequency, parallel strategy combinatorial explosion, ecosystem lock-in, observability
- Technical architecture: 3-layer model (compute: RoCE v2 leaf-spine + HCCS 50GB/s + Snt9b23 8-card mesh; platform: Volcano Gang/DRF/preempt + Ascend device plugin + EYWA DAG; toolchain: MindSpeed-LLM vs Megatron-Core, CANN 5.x→8.x, torch_npu Aten hijacking)
- Key technologies: MoXing API (mox.run/copy_parallel), HCCL Ring/Tree/Hybrid algorithms, ranktable fields, fault code classification (AICORE/HCCL/OOM/Driver), 5-level self-healing state machine, checkpoint format (TP sharded weights/optimizer/RNG/metadata)
- Cluster ops: 10-step end-to-end workflow (resource prep → image → data upload → Notebook debug → job create → DDP launch → ranktable routing → training → fault recovery → model deployment)
- Competitive landscape: AWS SageMaker / Azure ML / GCP Vertex AI vs domestic Alibaba PAI / Baidu BMLC / Tencent TI
- Improvement paths: 7 paths (MoE overlap, Attention/MoE decoupling, bubble filling, FP8, Ulysses CP, AutoML, ecosystem openness) each with pseudocode, code changes, difficulty rating, risks, rollback; §7.8 interface availability pre-assessment
- New in V2.0: Chapter 11 (6 code examples), Chapter 12 (7-section troubleshooting handbook), Snt9b23 mesh topology detail, CANN 8.x, 910D specs, expanded references to 68
- Open-source ecosystem: ModelArts-Lab, MindSpeed-LLM, MindSpeed, CANN, torch_npu, Volcano, AtomGit/Gitee mirrors

## Sources verified
- huaweicloud.com productdesc / usermanual-standard / bestpractice (architecture, distributed training, fault recovery)
- InfoQ + huaweicloud blog (MoXing architecture deep-dive)
- github huaweicloud/ModelArts-Lab
- gitee.com/ModelArts org, AtomGit/GitCode MindSpeed-LLM
- github Ascend/MindSpeed, Ascend/MindSpeed-LLM
- hiascend.com CANN/HCCL docs
- e.huawei.com Atlas 800T A2 / Snt9b23 specs
- IDC 2025 H2 MLaaS tracker; Gartner 2026 Magic Quadrant
- academic: arXiv COMET MLSys'25, MegaScale-MoE, Tessera OSDI'26, Ulysses (2406.12583), Ring-Attention (2310.01889), Megatron-LM, Alpa OSDI'22, ZeRO SC'20, FP8 (2209.05433), FlashAttention-2
- competitive: AWS/Azure/GCP/alibaba/baidu/tencent public docs

## Figures (7)
- fig1: 三层架构图
- fig2: 端到端10步流程图
- fig3: 故障恢复状态机决策树
- fig4: 改进优先级矩阵（气泡图）
- fig5: Volcano调度器工作链路
- fig6: Snt9b23超节点NPU拓扑+HCCL算法
- fig7: MindSpeed-LLM vs Megatron-Core对比柱状图

Note: Huawei's own peer-reviewed academic papers on ModelArts internals are scarce in open indexes; the survey relies on official technical documentation, vendor blog engineering write-ups, and open-source code repos as primary, with third-party MLaaS comparisons and academic MoE/distributed-training literature as the improvement-path evidence base. This is acknowledged as a limitation (Chapter 9).
