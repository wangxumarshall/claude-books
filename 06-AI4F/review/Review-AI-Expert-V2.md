# AI/LLM/Agent Systems Expert Review Report

**Paper:** Artificial Intelligence and Machine Learning for Magnetic Confinement Fusion Plasma Control: A Comprehensive Review (2024–2026)

**Reviewer:** AI/LLM/Agent Systems Expert
**Specialization:** Large language models, multi-agent systems, foundation models for scientific computing, AI safety, reinforcement learning
**Date:** 2026-05-30

---

## Overall Assessment: Minor Revision

The paper provides a comprehensive survey of AI/ML applications in fusion plasma control. From an AI methodology perspective, the paper correctly identifies the major trends (DRL, transformers, neural operators, PINNs) and critically assesses the "foundation model" terminology. However, several AI methodology gaps need to be addressed: missing uncertainty quantification methods (conformal prediction, calibrated UQ), incomplete treatment of safe RL, underdeveloped LLM/agent systems coverage, and missing PDE foundation model literature. The paper's AI methodology rigor can be significantly strengthened.

---

## Dimension Scores

| Dimension | Score (0-100) | Notes |
|-----------|---------------|-------|
| AI Methodology Rigor | 72 | Good coverage of methods but missing key AI advances |
| LLM/Agent Systems Coverage | 65 | LLM section too thin; no agent systems discussion |
| Foundation Model Assessment | 80 | Critical assessment is strong; missing PDE foundation models |
| RL Methodology | 78 | DRL well-covered; safe RL and MARL missing |
| UQ & Safety | 68 | UQ section exists but methods are thin |
| Evaluation Methodology | 75 | TRL framework is good; benchmarking discussion weak |

**Weighted Score: 73/100**

---

## Detailed Review

### 1. AI Methodology Rigor (Score: 72)

**Strengths:**
- The paper correctly identifies the major AI paradigms (DRL, transformers, neural operators, PINNs)
- The critical assessment of "foundation model" terminology is well-argued
- The evidence quality framework is a genuine contribution
- The TRL assessment provides a maturity-based perspective

**Weaknesses:**

**Issue A1: Missing conformal prediction for UQ (Section 10.8)**
The UQ section mentions Bayesian methods, ensembles, and conformal prediction in passing, but does not cite the actual conformal prediction work in fusion. Gopakumar et al. (arXiv:2408.09881, 2024) specifically applied conformal prediction to fusion surrogate models, providing prediction intervals with statistical guarantees. This is the most practical UQ approach for fusion applications and should be discussed in detail.
**Severity: Medium**

**Issue A2: Missing calibrated physics-informed UQ (Section 10.8)**
Gopakumar et al. (arXiv:2502.04406, 2025) proposed calibrated physics-informed UQ that combines physics constraints with uncertainty estimation. This directly addresses the paper's concern about UQ in safety-critical fusion applications.
**Severity: Medium**

**Issue A3: Missing UQ for confinement state classification**
Poels et al. (arXiv:2502.17397, 2025) demonstrated robust confinement state classification with uncertainty quantification using ensembled data-driven methods. This is directly relevant to the disruption prediction section.
**Severity: Low**

**Issue A4: Missing interpretable plasma monitoring with VAEs**
Poels et al. (arXiv:2504.17710, 2025) used multimodal VAEs for plasma state monitoring and disruption characterization at TCV. This provides a new interpretable approach that should be discussed in the disruption prediction or explainability sections.
**Severity: Low**

### 2. LLM/Agent Systems Coverage (Score: 65)

**Strengths:**
- XiHeFusion [77] and LPI-LLM [78] are correctly identified
- The "hallucination risk" warning for LLMs is appropriate

**Weaknesses:**

**Issue A5: No discussion of AI agents for scientific discovery (Section 11.3)**
The LLM section (11.3) focuses on domain-specific LLMs but does not discuss the rapidly growing field of AI agents for scientific discovery. Key developments include:
- Multi-agent systems for autonomous scientific experimentation (AutoLabs, arXiv:2509.25651)
- LLM-powered scientific discovery in experimental fluid mechanics (arXiv:2512.04716)
- Agentic AI for scientific discovery surveys (arXiv:2503.08979)
These agent-based approaches could revolutionize how fusion experiments are designed and analyzed.
**Severity: Medium**

**Issue A6: No discussion of multi-agent RL for plasma control**
The paper discusses single-agent DRL but does not address multi-agent RL (MARL) approaches. In principle, tokamak control can be decomposed into multiple agents handling different actuator groups (magnetic coils, heating, gas injection). While no fusion-specific MARL papers were found, the concept should be discussed as a future direction.
**Severity: Low**

### 3. Foundation Model Assessment (Score: 80)

**Strengths:**
- The critical assessment of "foundation model" terminology (Section 8.1) is rigorous
- The comparison with meteorology (GenCast) and materials science (MACE-MP-0) is appropriate
- The data scarcity argument is well-developed

**Weaknesses:**

**Issue A7: Missing PDE foundation models (Section 8.1)**
The paper does not discuss the emerging field of PDE foundation models, which are directly relevant to fusion:
- PDEformer-2 (arXiv:2507.15409, 2025): A versatile foundation model for 2D PDEs
- Soares et al. (arXiv:2511.21861, 2025): "Towards a Foundation Model for PDEs Across Physics Domains" (PDE-FM)
- Negrini et al. (arXiv:2502.06026, 2025): "A Multimodal PDE Foundation Model"
- Tripura & Chakraborty (arXiv:2310.18885, 2023): Foundational neural operator with continual learning
These models represent a more achievable path toward "foundation models" in physics than domain-specific pre-training.
**Severity: Medium**

**Issue A8: Missing negative transfer in multi-physics models**
Sharma & Sharma (arXiv:2605.15179, 2026) addressed negative transfer in multi-physics foundation models using sparse mixture-of-experts routing. This is directly relevant to the cross-device transfer learning discussion.
**Severity: Low**

### 4. RL Methodology (Score: 78)

**Strengths:**
- DRL for tearing avoidance is well-covered
- Offline RL and sim-to-real transfer are discussed
- The reward function design discussion is detailed

**Weaknesses:**

**Issue A9: No discussion of safe RL or constrained RL**
The paper discusses DRL for plasma control but does not address safe RL or constrained RL approaches. In safety-critical fusion applications, RL agents must satisfy hard safety constraints (e.g., never exceed certain plasma parameters). Recent work on constrained RL for physical systems (e.g., PD-TD3 for energy systems, arXiv:2402.05412) provides relevant methodology.
**Severity: Medium**

**Issue A10: No discussion of offline RL challenges**
The paper mentions offline RL (Section 2.3) but does not discuss the fundamental challenges: distributional shift, extrapolation error, and the need for conservatism. These challenges are particularly relevant for fusion where online exploration is dangerous.
**Severity: Low**

### 5. UQ & Safety (Score: 68)

**Strengths:**
- The UQ section (10.8) correctly identifies the need for uncertainty estimation
- The safety certification discussion (10.3) is comprehensive
- The failure mode catalog (10.10) is valuable

**Weaknesses:**

**Issue A11: UQ methods are described abstractly, not concretely**
Section 10.8 describes UQ methods (Bayesian, ensemble, conformal) in general terms but does not cite the actual fusion-specific UQ work. The section should be updated with concrete references to conformal prediction (Gopakumar et al. 2408.09881) and calibrated physics-informed UQ (Gopakumar et al. 2502.04406).
**Severity: Medium**

### 6. Evaluation Methodology (Score: 75)

**Strengths:**
- The TRL framework is well-designed
- The verification level analysis is informative
- The deployment readiness assessment is honest

**Weaknesses:**

**Issue A12: No discussion of benchmarking standards**
The paper mentions TokaMark [60] but does not discuss the broader need for standardized benchmarks in AI-for-fusion. The AI community has established benchmarks (ImageNet, GLUE, etc.) that enable fair comparison of methods. Fusion needs similar benchmarks.
**Severity: Low**

---

## Specific Recommendations

### Must Fix (Priority 1)

1. **Add UQ references to Section 10.8**: Cite Gopakumar et al. (2408.09881, 2502.04406) and Poels et al. (2502.17397) as concrete examples of UQ in fusion ML.

2. **Add PDE foundation model discussion to Section 8.1**: Discuss PDEformer-2, PDE-FM, and multimodal PDE foundation models as a more achievable path toward foundation models in physics.

### Should Fix (Priority 2)

3. **Add AI agents discussion to Section 11.3**: Briefly discuss the emerging field of AI agents for scientific discovery and its potential application to fusion.

4. **Add safe RL discussion to Section 2**: Briefly discuss constrained RL approaches and their relevance to fusion control safety.

5. **Add interpretable monitoring reference**: Cite Poels et al. (2504.17710) on multimodal VAEs for plasma state monitoring.

### Nice to Have (Priority 3)

6. **Add benchmarking discussion**: Discuss the need for standardized benchmarks in AI-for-fusion.

7. **Add negative transfer reference**: Cite Sharma & Sharma on negative transfer in multi-physics models.

8. **Discuss offline RL challenges**: Add brief discussion of distributional shift and conservatism in offline RL.

---

## Summary

| Criterion | Rating | Notes |
|-----------|--------|-------|
| AI Methodology Rigor | Conditional (72) | Missing key UQ methods and conformal prediction |
| LLM/Agent Systems Coverage | Conditional (65) | LLM section thin; no agent systems |
| Foundation Model Assessment | Pass (80) | Critical assessment strong; missing PDE foundation models |
| RL Methodology | Conditional (78) | Safe RL and offline RL challenges missing |
| UQ & Safety | Conditional (68) | UQ methods described abstractly |
| Evaluation Methodology | Pass (75) | TRL framework good; benchmarking weak |

**Overall: Minor Revision** — The paper's AI methodology can be significantly strengthened by adding concrete UQ references, PDE foundation model discussion, and AI agents coverage. The critical assessment of "foundation model" terminology is a strength.

---

*Report generated from AI/LLM/Agent Systems expert perspective.*
