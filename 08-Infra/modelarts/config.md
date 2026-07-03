# Paper Configuration Record

| Field | Value |
|---|---|
| Paper type | Technical research report / survey paper |
| Title | 华为云 ModelArts 深度研究：业务背景、技术架构、集群实践与改进路径 |
| Discipline | Cloud infrastructure / AI systems engineering |
| Structure | Survey-style: Background → Challenges → Architecture → Implementation → Cluster ops → Improvements → Discussion |
| Citation format | IEEE (numbered) |
| Output format | Markdown (single file) |
| Language | Simplified Chinese (technical terms kept in English) |
| Abstract | Bilingual (zh-CN + EN) |
| Word count target | 12000-15000 CJK chars |
| Mode | lit-review / survey (deep-research-derived) |
| Style | No AI-typical filler terms; varied paragraph rhythm; em dash ≤2/page |

## Scope locked
- Business background: Huawei Cloud AI strategy, MLaaS market positioning
- Challenges: large-model training stability, heterogeneity, communication, fault tolerance, ecosystem
- Technical architecture: 3-layer model (compute / platform / toolchain), MoXing, AutoSearch, EI-Backbone
- Concrete implementation: distributed training (DP/DDP), HCCL, checkpoint/resume, fault recovery (in-place, Job reschedule, operator re-exec)
- Cluster ops: how to actually run multi-node multi-card jobs on Atlas 800T A2 / Snt9b23, VPC/SFS/OBS/SWR, Volcano, ranktable routing, affinity groups
- Competitive landscape: vs SageMaker / Vertex AI / Azure ML
- Improvement directions: MoE communication (COMET/FlowMoE/MegaScale-MoE/Tessera), parallel folding, FP8, Ulysses CP, memory fragmentation, dynamic scheduling, ecosystem openness
- Open-source ecosystem: ModelArts-Lab, MindSpeed-LLM, MindSpeed, CANN, torch_npu, AtomGit/Gitee mirrors

## Sources verified
- huaweicloud.com productdesc / usermanual-standard / bestpractice (architecture, distributed training, fault recovery)
- InfoQ + huaweicloud blog 108339 (MoXing architecture deep-dive)
- huaweicloud news (DAWNBench 4'08" with 128×V100)
- github huaweicloud/ModelArts-Lab (1k★), huawei-clouds/modelarts-dataset-sdk
- gitee.com/ModelArts org, AtomGit/GitCode MindSpeed-LLM
- github Ascend/MindSpeed, Ascend/MindSpeed-LLM
- hiascend.com CANN/HCCL docs
- e.huawei.com Atlas 800T A2 specs (8×200GE RoCE)
- academic: arXiv Megatron-MoE Parallel Folding (2504.14960), MegaScale-MoE (2505.11432), FlowMoE (OpenReview), Tessera OSDI'26, COMET MLSys'25, X-MoE (2508.13337), SE-MoE (2205.10034)
- competitive: TechTarget, Machine Learning Authority, Medium Huawei-ModelArts-vs-SageMaker

Note: Huawei's own peer-reviewed academic papers on ModelArts internals are scarce in open indexes; the survey relies on official technical documentation, vendor blog engineering write-ups, and open-source code repos as primary, with third-party MLaaS comparisons and academic MoE/distributed-training literature as the improvement-path evidence base. This is acknowledged as a limitation.
