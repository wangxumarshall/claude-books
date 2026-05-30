# Research Question Brief

**Paper:** AI for Fusion — Artificial Intelligence and Machine Learning for Magnetic Confinement Fusion Plasma Control: A Comprehensive Review (2024–2026)

**Brief Version:** 1.0

**Date:** 2026-05-30

**Pipeline Stage:** Phase 1 — RQ Formulation & Methodology Blueprint

---

## 1. Primary Research Question

> **RQ1:** During 2024–2026, how have artificial intelligence and machine learning techniques — spanning deep reinforcement learning, transformer-based foundation models, physics-informed neural networks, and digital twin frameworks — advanced the state-of-the-art in magnetic confinement fusion plasma control, and what is the current technology readiness level (TRL 1–9) of each major sub-domain as the field transitions from proof-of-concept demonstrations toward engineering deployment in next-step devices such as ITER, SPARC, and DEMO?

### RQ1 Characteristics

| Attribute     | Assessment                                                                                                                                   |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Specific**  | Targets a defined 3-year window (2024–2026), a specific application domain (MCF plasma control), and eight identifiable AI/ML sub-domains    |
| **Measurable** | Can be answered through systematic literature survey, TRL assessment, and classification comparison tables with quantifiable metrics (AUC, TPR/FPR, inference latency, speedup factors) |
| **Achievable** | Builds on existing V1/V2 drafts with 70+ verified references; leverages systematic search across 10 target venues; no laboratory access required |
| **Relevant**  | Directly addresses the critical gap between AI research demonstrations and ITER/DEMO engineering deployment requirements                     |
| **Time-bound** | Focused on the 2024–2026 window, capturing the acceleration from DeepMind TCV (2022) through DIII-D DRL (Nature 2024) to foundation models (2025–2026) |

---

## 2. Sub-Questions

### SQ1: Milestone Analysis

> What are the key milestone breakthroughs in AI/ML for MCF plasma control during 2024–2026, and how do they collectively advance the field's maturity from TRL 2–3 (research) toward TRL 5–6 (lab-validated)?

**Answerable via:** Systematic survey of Nature, PRL, NF, PoP, PPCF, FED publications plus APS-DPP, IAEA FEC, IEEE SOFE proceedings; classification of each result by TRL level; identification of the 10–15 highest-impact papers.

**Key milestones to track:**

| Milestone                                          | Year | Venue        | TRL | Significance                                          |
| -------------------------------------------------- | ---- | ------------ | --- | ----------------------------------------------------- |
| Seo et al. DRL tearing mode avoidance on DIII-D    | 2024 | *Nature*     | 5   | First DRL control avoiding MHD instability on a real tokamak |
| Kim et al. ML adaptive ELM suppression (DIII-D + KSTAR) | 2024 | APS-DPP     | 5   | Cross-device validation of ML control portability     |
| TokaMind multi-modal Transformer foundation model  | 2025 | Preprint     | 2–3 | First plasma dynamics foundation model                |
| NVIDIA digital twin framework for tokamaks         | 2025 | Conference   | 3–4 | Industry-grade digital twin for fusion                |
| DeepMind TCV autonomous plasma control (context)   | 2022 | *Nature*     | 5   | Catalyst for the 2024–2026 wave                       |
| GyroSwin 5D gyrokinetic surrogate (billion-param)  | 2025 | Preprint     | 3–4 | First billion-parameter fusion ML model               |
| DivControlNN ML divertor detachment control on KSTAR | 2025 | Preprint   | 4–5 | First ML-driven divertor control on real device       |
| XiHeFusion domain-specific LLM                     | 2025 | Preprint     | 2   | First fusion-domain large language model              |
| Padidar et al. conditional diffusion for stellarator design | 2025 | Preprint | 3 | Generative AI for stellarator configuration          |
| EAST 1,066 s steady-state H-mode (AI-assisted)     | 2025 | Conference   | 6   | Long-pulse record with ML-assisted control            |

### SQ2: Cross-Cutting Challenges

> What are the persistent cross-cutting challenges — specifically interpretability, rare-event handling, safety certification, cross-device portability, and uncertainty quantification — that impede the transition of AI/ML plasma control systems from laboratory demonstrations to deployment in ITER-class and pilot-plant-class devices?

**Answerable via:** Thematic synthesis across all eight review dimensions; comparison with safety-critical AI practices in aerospace (DO-178C), nuclear fission (10 CFR 50), and process control (IEC 61511); identification of failure modes and negative results.

**Challenge taxonomy:**

| Challenge Category            | Current Status (2026)                                  | Gap to Deployment                                                |
| ----------------------------- | ------------------------------------------------------ | ---------------------------------------------------------------- |
| Interpretability              | Post-hoc attention maps, SHAP values applied sporadically | No standard for physics-validated explanation in control decisions |
| Rare-event handling           | Class imbalance (10:1 to 100:1) in disruption data    | FPR 20–30% in some real deployments; operator alert fatigue      |
| Safety certification          | Framework proposals only (TRL 2–3)                     | No ML control system has passed nuclear-grade V&V                |
| Cross-device portability      | Demonstrated on 2 devices (DIII-D + KSTAR) for ELM     | ITER/SPARC parameters far outside training distribution          |
| Uncertainty quantification    | Ensemble methods (implicit); BNN/MC-Dropout (limited)  | No standardized UQ metrics; no operational UQ-decision mapping   |
| Sim-to-real transfer          | Domain randomization + fine-tuning; partial success     | DRL policies degrade 30–50% on real hardware in some cases       |
| Data infrastructure           | dFL, TokaMark, TORAX emerging                          | No unified cross-device dataset; data ownership barriers         |

### SQ3: Technical Readiness Roadmap

> Based on the TRL assessment of each AI/ML sub-domain, what is the prioritized research and engineering roadmap — distinguishing short-term (2026–2028), medium-term (2028–2032), and long-term (2032+) milestones — for deploying trustworthy AI plasma control in ITER, SPARC, and DEMO?

**Answerable via:** TRL gap analysis for each sub-domain; dependency mapping between sub-domains (e.g., foundation models require data infrastructure first); alignment with ITER/SPARC/DEMO construction and operation timelines.

**Roadmap framework:**

| Timeframe    | Priority Milestones                                                                                  | Target TRL |
| ------------ | ----------------------------------------------------------------------------------------------------- | ---------- |
| Short (2026–2028) | Standardized cross-device benchmarks; UQ integration in disruption predictors; FPGA-deployed DRL demos | 4–5 → 6    |
| Medium (2028–2032) | Foundation model pre-training on multi-device data; safety certification frameworks; ITER ML control pilot | 5 → 7      |
| Long (2032+)      | Autonomous multi-agent control; digital twin closed-loop operation; DEMO-integrated AI systems         | 7 → 8–9    |

---

## 3. Scope Boundaries

### 3.1 In-Scope

| Category                              | Specific Topics                                                                                                                                                                                                                      |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Core AI/ML Methods**                | Deep reinforcement learning (DRL), supervised/deep learning for prediction, transformer architectures, neural operators (FNO, DeepONet), physics-informed neural networks (PINNs), Bayesian optimization, diffusion models, LLMs       |
| **Plasma Control Applications**       | Tearing mode avoidance, ELM suppression, disruption prediction and mitigation, equilibrium reconstruction, profile control (current, density, rotation, temperature), divertor detachment control, magnetic control                    |
| **Simulation & Modeling**             | Surrogate models for gyrokinetic codes (GENE, CGYRO, GS2, QuaLiKiz), transport models (TGLF, TRANSP), MHD stability, SOLPS/EDGE2D, TORAX                                                                                            |
| **Devices**                           | DIII-D, KSTAR, EAST, JET, TCV, ASDEX Upgrade (AUG), W7-X, HL-2A/HL-3, MAST/MAST-U, WEST, ST40, EXL-50U, ITER (design phase), SPARC (construction)                                                                                  |
| **Engineering Integration**           | Digital twin frameworks, real-time inference systems (FPGA, embedded), integrated AI control systems, data infrastructure (dFL, TokaMark, TORAX), open-source tools (Gym-TORAX)                                                        |
| **Extended Topics**                   | Stellarator optimization (generative design), HTS magnet AI design, LLMs for fusion (XiHeFusion), ICF AI applications, 5D gyrokinetic surrogates (GyroSwin), non-tokamak MCF devices (magnetic mirrors, FRC)                         |
| **Publication Venues**                | *Nuclear Fusion*, *Physical Review Letters*, *Plasma Physics and Controlled Fusion*, *Physics of Plasmas*, *Fusion Engineering and Design*, IAEA FEC, IEEE SOFE, EPS, APS-DPP, TOFE, *Nature*, *Nature Physics*, *Reviews of Modern Physics* |
| **Time Window**                       | January 2024 – May 2026, with seminal pre-2024 papers (DeepMind TCV 2022, etc.) included for context                                                                                                                                 |

### 3.2 Out-of-Scope

| Category                                        | Reason for Exclusion                                                                                              |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Inertial confinement fusion (ICF) as primary focus** | ICF AI applications are included as an extended topic only; the primary focus is MCF plasma control                |
| **General ML methodology without fusion application** | Pure ML papers (e.g., new optimizer architectures) without a direct fusion use case are excluded                   |
| **Fusion materials science as primary focus**    | ML interatomic potentials and radiation damage prediction are mentioned in the engineering section, not as a core dimension |
| **Pre-2024 literature (except context)**         | The primary survey window is 2024–2026; earlier papers are included only as foundational context                    |
| **Non-peer-reviewed blog posts, press releases** | Only peer-reviewed journal papers, official conference proceedings, and recognized preprint servers (arXiv) are included |
| **Magnetic confinement devices outside the listed set** | Devices not in the in-scope list are excluded unless they provide unique methodological insights                  |
| **Fusion neutronics, tritium breeding, remote handling AI** | These engineering domains are outside the plasma control focus                                                    |
| **Pure economic/LCOE modeling with AI**          | Cost optimization AI is out of scope unless directly coupled with plasma control or plant design                   |

---

## 4. FINER Criteria Scoring

### Scoring Rubric

Each criterion is scored on a 1–5 scale:

| Score | Meaning                             |
| ----- | ----------------------------------- |
| 1     | Does not meet criterion             |
| 2     | Marginally meets criterion          |
| 3     | Adequately meets criterion          |
| 4     | Strongly meets criterion            |
| 5     | Exemplary fit with criterion        |

### Detailed Scoring

#### F — Feasible: **5/5**

| Factor                         | Assessment                                                                                                                                   |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Data availability              | 70+ references already identified and partially verified across 10 target venues; V1 and V2 drafts provide a substantive starting corpus       |
| Research infrastructure        | Systematic search methodology defined; access to all target venue databases (IOP Science, AIP, ScienceDirect, Nature, conference proceedings) |
| Computational requirements     | No computational resources required — this is a literature review, not an empirical study                                                    |
| Time feasibility               | 3-year window (2024–2026) is well-bounded; field is active but not overwhelming in volume (~350 candidate papers)                             |
| Skill requirements             | Domain knowledge in both plasma physics and ML is required; the existing V2 draft demonstrates this expertise is available                    |
| **Evidence from existing work** | The V1 (MCF-review-V11.md, 151 KB) and V2 (AI-for-Fusion-V2.md, 110 KB) drafts already cover all 8 core dimensions + 6 extended topics       |

#### I — Interesting: **5/5**

| Factor                              | Assessment                                                                                                                                                  |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Scientific significance             | The 2024–2026 period represents a paradigm shift: DRL moved from simulation to real-device control; foundation models entered plasma physics; digital twins matured |
| Broad audience appeal               | Relevant to plasma physicists, ML researchers, fusion engineers, ITER/SPARC/DEMO project managers, and science policy analysts                               |
| Timeliness                          | The DIII-D Nature 2024 result and the foundation model wave (2025) create a "moment of acceleration" that warrants a comprehensive stocktaking               |
| Practical implications              | Directly informs ITER control system design, SPARC commissioning strategy, and private fusion company technology roadmaps                                    |
| Interdisciplinary appeal            | Bridges AI/ML, plasma physics, nuclear engineering, and control theory — a genuinely interdisciplinary synthesis                                              |
| **Key narrative hook**              | "From proof-of-concept to engineering exploration" — the field is at an inflection point comparable to deep learning's breakthrough moment in computer vision (2012–2015) |

#### N — Novel: **4/5**

| Factor                                   | Assessment                                                                                                                                      |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Gap in existing reviews                  | Rea et al. (2024, *Reviews of Modern Physics*) covers ML for fusion but focuses on pre-2024 work and excludes engineering/materials domains      |
| Unique contribution of this review       | (1) 2024–2026 temporal focus captures the acceleration; (2) 8+6 dimensional structure is more comprehensive; (3) TRL assessment framework is novel |
| Differentiation from Rea et al. 2024    | Rea: "ML for fusion energy" — broad physics focus. This review: "AI for fusion plasma control 2024–2026" — engineering/deployment focus with TRL    |
| Differentiation from Brunton et al. 2020 | Brunton: "ML for fluid mechanics" — general. This review: fusion-specific, deployment-oriented                                                    |
| Potential overclaim                      | The "first comprehensive review" claim is partially mitigated by Rea et al.; should position as "first review focused on the 2024–2026 acceleration" |
| **Novelty score rationale**              | Scored 4 (not 5) because Rea et al. 2024 partially overlaps; the novelty lies in temporal scope, TRL framework, and engineering emphasis          |

#### E — Ethical: **5/5**

| Factor                            | Assessment                                                                                                                                      |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Human subjects                    | No human subjects involved; this is a literature review of published scientific research                                                         |
| Data privacy                      | No personal or sensitive data collected; all data sources are published peer-reviewed literature                                                 |
| Dual-use concerns                 | AI for fusion plasma control has no weapons-of-mass-destruction dual-use concern; fusion technology is inherently civilian                        |
| Conflicts of interest             | No industry funding or consulting relationships to declare                                                                                      |
| Responsible AI narrative          | The review explicitly addresses safety certification, failure modes, and negative results — promoting responsible AI deployment in fusion          |
| Environmental impact              | The review supports the development of clean fusion energy — a net positive environmental contribution                                           |
| Citation ethics                   | All references will be verified against publisher databases before submission (addressing the P0 issue identified in the V1 peer review)          |
| **Bonus: Failure mode reporting** | Section 10.10 of V2 explicitly documents negative results and failure modes, countering the positive-results bias in the field                    |

#### R — Relevant: **5/5**

| Factor                                    | Assessment                                                                                                                                           |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Alignment with field priorities           | ITER Organization has identified AI/ML as a key enabling technology for plasma control; SPARC is actively commissioning ML-based control systems       |
| Policy relevance                          | Multiple national fusion strategies (US, EU, China, Japan, Korea) explicitly mention AI/ML integration as a priority                                  |
| Industry relevance                        | Private fusion companies (CFS, Helion, TAE, Tokamak Energy) are actively hiring ML engineers and deploying AI control systems                         |
| Scientific community demand               | The 2024–2026 period has seen exponential growth in AI-for-fusion publications; a synthesis is urgently needed                                        |
| Training/education relevance              | The review serves as a comprehensive entry point for researchers crossing from ML to fusion or vice versa                                             |
| **ITER/SPARC deployment pathway**         | Directly informs the design of ITER's plasma control system (PCS) ML components and SPARC's commissioning strategy                                    |
| **Cross-device portability question**     | The central engineering challenge — can AI trained on DIII-D work on ITER? — is directly addressed by this review's scope                              |

### FINER Summary Scorecard

| Criterion   | Score | Weight | Weighted Score |
| ----------- | ----- | ------ | -------------- |
| **F**easible   | 5/5   | 0.20   | 1.00           |
| **I**nteresting | 5/5   | 0.25   | 1.25           |
| **N**ovel       | 4/5   | 0.20   | 0.80           |
| **E**thical     | 5/5   | 0.15   | 0.75           |
| **R**elevant    | 5/5   | 0.20   | 1.00           |
| **Total**       |       | 1.00   | **4.80 / 5.00** |

**Assessment: EXCELLENT.** The research question is feasible (existing corpus), interesting (paradigm shift moment), novel (temporal scope + TRL framework), ethical (no concerns), and highly relevant (ITER/SPARC deployment pathway). The only deduction is for novelty (4/5) due to partial overlap with Rea et al. 2024.

---

## 5. Research Dimensions to Cover

### 5.1 Core Dimensions (8)

| #  | Dimension                                    | Key Questions                                                                                                   | Representative Papers                                    | TRL |
| -- | -------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- | --- |
| 1  | **DRL-based plasma control**                 | Can DRL avoid MHD instabilities in real-time on real devices? What reward function designs encode physics?       | Seo 2024 (Nature), Degrave 2022 (Nature), Wu 2025       | 5–6 |
| 2  | **ML disruption prediction**                 | Can ML achieve >95% TPR with <1% FPR and sufficient warning time? How does it generalize across devices?         | Spangher 2024, Chayapathy 2024, Arnold 2024             | 6–7 |
| 3  | **ELM detection and suppression**            | Can ML adaptive controllers maintain ELM suppression across devices? How is RMP optimized in real-time?          | Kim 2024 (APS-DPP), Shousha 2024                        | 5–6 |
| 4  | **Equilibrium reconstruction & real-time diagnostics** | Can NN achieve sub-ms equilibrium reconstruction? How accurate are NN diagnostic surrogates?          | Matsumori 2024, Zheng 2024, Wang 2024                    | 5–6 |
| 5  | **Surrogate models and neural operators**    | Can FNO/DeepONet achieve 10,000x speedup for gyrokinetic/turbulence simulations?                                | Gopakumar 2024, Ho 2024, Mathews 2024                   | 3–5 |
| 6  | **Physics-informed neural networks**         | Can PINNs handle stiff fusion PDEs (Braginskii, Grad-Shafranov)? What physics constraints improve convergence?   | Meneghini 2024, Luo 2024                                | 2–3 |
| 7  | **Foundation models & cross-device transfer** | Can Transformer foundation models learn general plasma dynamics? Does transfer learning reduce data needs by 60–80%? | TokaMind 2025, Reinke 2024                              | 2–3 |
| 8  | **Digital twins & integrated AI control**    | Can digital twins close the "sense-predict-decide-act" loop? What multi-physics coupling is needed?              | NVIDIA 2025, Rothstein 2024, UK STEP                     | 3–4 |

### 5.2 Extended Topics (6)

| #  | Extended Topic                             | Key Questions                                                                                    | Representative Papers                        | TRL |
| -- | ------------------------------------------ | ------------------------------------------------------------------------------------------------ | -------------------------------------------- | --- |
| E1 | **Stellarator optimization**               | Can generative AI (diffusion models) design novel stellarator configurations?                    | Padidar 2025, Cadena 2025 (ConStellaration)  | 3   |
| E2 | **HTS magnet AI design**                   | Can NN surrogates replace FEM for HTS magnet modeling? Can ML potentials model YBCO defects?     | Xiao 2025, Di Eugenio 2025, Nunn 2025        | 4–5 |
| E3 | **LLM for fusion**                         | Can domain-specific LLMs (XiHeFusion) assist literature review, code generation, experiment design? | XiHeFusion 2025, Chen 2025 (LPI-LLM)        | 2   |
| E4 | **ICF AI applications**                    | How do AI methods transfer between MCF and ICF? What are the key differences in data and control? | Gutierrez 2025 (HL-MBO), Ejaz 2025 (KAN)    | 3–4 |
| E5 | **Data infrastructure**                    | What standardized datasets, benchmarks, and tools are needed? How to break data silos?           | Michoski 2025 (dFL), TokaMark 2025, TORAX   | 3–4 |
| E6 | **5D gyrokinetic surrogate models**        | Can billion-parameter models learn 5D phase-space turbulence? What is the accuracy-cost tradeoff? | GyroSwin 2025                                | 3–4 |

---

## 6. Key Milestones to Track

### 6.1 Landmark Papers (Must-Cite)

| Year | Paper                                     | Venue          | Impact                                      |
| ---- | ----------------------------------------- | -------------- | ------------------------------------------- |
| 2022 | Degrave et al. — DRL on TCV               | *Nature*       | Catalyst for the 2024–2026 AI-fusion wave   |
| 2024 | Seo et al. — DRL tearing mode avoidance   | *Nature*       | First DRL avoiding MHD instability on real tokamak |
| 2024 | Kim et al. — ML adaptive ELM suppression  | APS-DPP        | Cross-device ML control validation          |
| 2024 | Spangher et al. — Transformer disruption prediction | Preprint | Transformer architecture for disruption forecasting |
| 2025 | TokaMind — multi-modal Transformer        | Preprint       | First plasma dynamics foundation model       |
| 2025 | GyroSwin — 5D gyrokinetic surrogate       | Preprint       | Billion-parameter fusion ML model            |
| 2025 | Padidar et al. — diffusion for stellarators | Preprint      | Generative AI for stellarator design         |
| 2025 | XiHeFusion — fusion-domain LLM            | Preprint       | First fusion-specific large language model   |
| 2025 | DivControlNN — ML divertor control        | Preprint       | First ML-driven detachment control on KSTAR  |

### 6.2 Device Performance Records (Context)

| Year | Record                                                     | Device  |
| ---- | ---------------------------------------------------------- | ------- |
| 2024 | 48 s at 100 million K; H-mode >100 s                      | KSTAR   |
| 2025 | 1,066 s steady-state H-mode                                | EAST    |
| 2025 | 1,320 s plasma sustainment (tungsten divertor)             | WEST    |
| 2025 | 43 s triple product record                                 | W7-X    |
| 2023 | 69.26 MJ fusion energy (final D-T experiment)              | JET     |
| 2024 | 20 T HTS magnet validated                                  | MIT-CFS |
| 2026 | SPARC construction ~80% complete                           | CFS     |

### 6.3 Technology Milestones (AI-specific)

| Milestone                                          | Status (2026)   | Next Step                                |
| -------------------------------------------------- | --------------- | ---------------------------------------- |
| DRL on real tokamak (single device)                | Achieved (DIII-D) | DRL on ITER-class device (TRL 6→7)       |
| Cross-device ML control (2+ devices)               | Achieved (DIII-D + KSTAR) | 3+ devices including superconducting (TRL 5→6) |
| Real-time ML disruption prediction (<10 ms)        | Demonstrated    | Integration into ITER PCS architecture    |
| Foundation model for plasma dynamics                | Early research  | Multi-device pre-training; zero-shot transfer |
| Digital twin closed-loop control                   | Framework stage | Online data assimilation; bidirectional data flow |
| Safety-certified ML control system                 | Not yet achieved | Develop V&V methodology with nuclear regulators |
| Standardized cross-device benchmark dataset        | TokaMark (single device) | Multi-device ITPA database integration   |

---

## 7. Methodological Notes

### 7.1 Review Type

This is a **narrative comprehensive review** with systematic search elements, not a formal systematic review/meta-analysis. A PRISMA diagram is not required, but a transparent search process summary (already in V2 Section 1.3) is provided.

### 7.2 Evidence Grading

Each cited result should be graded by validation level:

| Level | Description                                       | Example                                    |
| ----- | ------------------------------------------------- | ------------------------------------------ |
| L1    | Mathematical proof / analytic result               | PINN convergence theorems                  |
| L2    | High-fidelity simulation validation                | Gyrokinetic surrogate on GENE benchmarks   |
| L3    | Experimental validation on a single device         | DRL tearing mode avoidance on DIII-D       |
| L4    | Cross-device validation (2+ devices)               | ML ELM suppression on DIII-D + KSTAR       |
| L5    | Deployment in operational / ITER-class environment | Not yet achieved for any AI/ML system      |

### 7.3 TRL Framework

| TRL | Definition                                                     | Fusion AI Example                           |
| --- | -------------------------------------------------------------- | ------------------------------------------- |
| 1–2 | Basic research; concept formulation                            | PINN for Grad-Shafranov (early stage)       |
| 3–4 | Proof-of-concept; simulation-validated                         | GyroSwin 5D surrogate; foundation models    |
| 5–6 | Lab-validated on real devices                                  | DIII-D DRL; KSTAR ELM suppression           |
| 7   | System prototype in operating environment                      | Not yet achieved                            |
| 8–9 | Qualified system; proven in operational deployment             | ITER PCS ML components (future)             |

---

## 8. Deliverable Mapping

The RQ Brief feeds into the deep-research pipeline as follows:

| Pipeline Phase       | RQ Brief Component Used                           | Output                                    |
| -------------------- | ------------------------------------------------- | ----------------------------------------- |
| Phase 2: Literature Search | In-scope venues, keywords, milestones table   | Verified reference corpus (target: 70–100 papers) |
| Phase 3: Analysis    | 8 core dimensions + 6 extended topics, TRL framework | Thematic synthesis per dimension           |
| Phase 4: Writing     | Primary RQ, sub-questions, scope boundaries      | Structured review manuscript               |
| Phase 5: Review      | FINER scoring, evidence grading, failure modes    | Peer review and revision                   |

---

*Brief prepared per research_question_agent protocol.*
*FINER score: 4.80/5.00 — EXCELLENT.*
*Ready to proceed to Phase 2: Literature Search & Verification.*
