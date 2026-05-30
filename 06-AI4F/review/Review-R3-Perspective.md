## R3 Perspective Review Report

**Reviewer:** Peer Reviewer 3 -- Cross-Disciplinary Perspective (Safety-Critical AI Systems, Aerospace/Functional Safety)

---

### Overall Assessment: Minor Revision

This paper represents a commendable and unusually thorough survey of AI/ML for magnetic confinement fusion plasma control. From a cross-disciplinary standpoint, the paper makes several genuine attempts to connect fusion AI to other safety-critical domains (Section 10.9), discusses safety certification frameworks (Section 10.3), and identifies transferable lessons. However, the treatment of cross-domain connections remains largely superficial -- a comparative table and a few paragraphs rather than a deep analysis of what fusion can actually learn from (and contribute to) aerospace, nuclear fission, and process control safety engineering. The safety certification discussion, while mentioning the right standards (IEC 61508, DO-178C), lacks the specificity needed to be actionable for practitioners. Several fundamental assumptions about the transferability of ML methods across domains are left unchallenged. With targeted revisions to deepen the cross-disciplinary analysis, this paper would be a strong contribution.

---

### Dimension Scores

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Cross-Domain Connections | 58 | Section 10.9 provides a comparative table of aerospace, nuclear fission, and process control, but the analysis remains at the level of bullet-point summaries. The paper mentions DO-178C and IEC 61508 (Section 10.3) but does not explain how their specific certification artifacts (e.g., traceability matrices, modified condition/decision coverage, tool qualification under DO-330) would apply to ML systems in fusion. No discussion of adjacent domains where similar ML-for-control challenges have been solved (e.g., autonomous vehicles' ISO 21448 SOTIF, medical devices' IEC 62304, or railway's EN 50129). The TokEye cross-domain transfer (Section 5.4, ref [38]) from fusion to bioacoustics is mentioned but not analyzed for what it implies about feature universality. |
| Practical Impact | 65 | The paper honestly states 78% of cited works are preprints and only 30% of key studies have experimental validation. The TRL assessment (Section 10.7) is valuable. However, the practical implications section lacks quantified deployment scenarios -- e.g., what would it cost to retrofit an existing tokamak control system with ML? What is the operational downtime risk during integration testing? The calculation cost table (Section 10.6) is helpful but lacks comparison to the cost of NOT deploying AI (e.g., lost plasma time due to conservative operational limits). |
| Safety Certification | 52 | Section 10.3 mentions IEC 61508, IEC 61511, DO-178C, and 10 CFR 50, which is the correct vocabulary. However, the treatment is declarative rather than prescriptive. The paper states ML systems face certification obstacles but does not propose a concrete certification pathway. Missing: discussion of IEC 61508 Part 7 (application of specific techniques), the concept of "proven in use" arguments for ML, the role of runtime monitoring architectures (e.g., safety cage/watchdog patterns), and the critical distinction between ML as a "recommendation system" (lower SIL) versus ML as the "final element" (higher SIL) in a safety function. The mention of "extra protective layer" (Section 10.3) is the right idea but underdeveloped. |
| Transferable Insights | 55 | The paper identifies several transferable insights (physics-informed approaches, sim-to-real, human-on-the-loop) but treats them as bullet points rather than analyzing their mechanisms. No discussion of what fusion's unique challenges (millisecond timescales, extreme environments, limited data) could CONTRIBUTE to other fields. For example, the one-shot learning approach via ensemble Kalman filtering (Section 2.1) has direct implications for any domain with expensive, scarce training data. The FPGA deployment pattern (Section 4.3) is directly relevant to edge AI in aerospace. |
| Broader Implications | 50 | Policy and ethical considerations are almost entirely absent. No discussion of: dual-use concerns (plasma control AI and weapons-relevant physics), workforce displacement implications, environmental justice in fusion energy deployment, the geopolitics of AI-for-fusion data sharing, or the ethical implications of autonomous plasma control decisions. The paper briefly mentions data access restrictions (Section 10.6) but frames them only as technical barriers, not as governance challenges. |
| Fundamental Assumptions | 45 | Several unchallenged assumptions: (1) The paper assumes that scaling laws from NLP/CV will eventually apply to fusion foundation models, but provides no analysis of why physics-constrained systems might have fundamentally different scaling behavior. (2) The paper assumes cross-device transfer is primarily a data/domain adaptation problem, ignoring that the underlying control architectures differ significantly between devices. (3) The TRL framework is borrowed from NASA's hardware-centric context without discussing its limitations for software/ML systems. (4) The paper assumes that "more data" will solve the generalization problem, without considering that the relevant physics may be fundamentally underrepresented in existing datasets. |

---

### Strengths

- **Exceptional transparency about evidence quality.** The explicit disclosure that 78% of cited works are preprints, combined with the verification-level analysis showing only 30% experimental validation and 67% of those from a single device (DIII-D), sets a high standard for intellectual honesty in a rapidly moving field. This is exactly the kind of rigor that safety-critical domains demand.

- **Genuine attempt at cross-domain comparison.** Section 10.9 explicitly compares fusion AI with aerospace, nuclear fission, and process control, identifying concrete lessons. The observation that "ML typically gains regulatory acceptance more easily as an operator assistance tool rather than a fully autonomous controller" (Section 10.9) is a critical insight borrowed correctly from aviation practice.

- **Failure mode documentation.** Section 10.10 on failure modes and negative results is rare in survey papers and extremely valuable from a safety engineering perspective. The documentation of high false-positive rates (20-30%), sim-to-real transfer failures, and PINN convergence difficulties provides the "negative evidence base" that safety assessors need.

- **Computation cost and deployment analysis.** The table in Section 10.6 quantifying training costs, inference latency requirements, and hardware options, combined with the FPGA/GPU/CPU hybrid deployment discussion, shows engineering maturity beyond typical ML survey papers.

- **Critical assessment of "foundation model" claims.** The paper's careful demarcation between "multi-modal pre-training frameworks" and true foundation models (Section 8.1), with explicit comparison to meteorology and materials science data scales, demonstrates the analytical discipline needed to prevent hype-driven technology transfer.

---

### Weaknesses

- **Safety certification treatment is superficial.** The paper mentions the right standards but does not engage with their specific requirements. For a paper that identifies safety certification as a "key challenge," the treatment should be substantially deeper. A fusion engineer reading Section 10.3 would know the standards exist but would not know how to begin a certification campaign.

- **Cross-domain connections are listed, not analyzed.** Section 10.9 reads as a comparative summary rather than a deep analysis. The paper does not identify specific technical mechanisms by which aerospace or nuclear safety practices could be adapted for fusion, nor does it identify what fusion's unique constraints would require that is genuinely novel.

- **No discussion of runtime safety architectures.** The paper focuses on model-level properties (accuracy, latency, interpretability) but almost entirely ignores system-level safety architectures -- the watchdog monitors, safety cages, graceful degradation pathways, and voting architectures that are standard in aerospace and nuclear control systems. These are arguably more important for safety certification than model-level properties.

- **Missing policy and governance analysis.** The paper has virtually no discussion of the policy, ethical, or governance dimensions of deploying AI in fusion facilities. This is a significant gap for a paper that aims to be "comprehensive" and that claims to discuss "broader implications."

- **Unchallenged assumptions about data-driven scaling.** The paper implicitly assumes that the path forward is "more data, bigger models" without seriously considering that physics-constrained systems may require fundamentally different approaches. The discussion of PINN limitations (Section 7.5) hints at this but does not develop the argument.

---

### Specific Issues

1. **Section 10.3 (Safety Certification):** The paper states "ML-based control systems in fusion devices need to reference the industrial functional safety standard system" but does not explain how IEC 61508's concept of "systematic capability" applies to ML systems whose behavior is not fully specified by design. The paper should discuss the emerging consensus (from ISO/IEC JTC 1/SC 42 and the EU AI Act's high-risk AI requirements) that ML systems in safety-critical applications require a "safety case" that addresses both systematic failures and the inherent non-determinism of learned behavior. The mention of "layer of protection analysis" (LOPA) as a framework for positioning ML relative to traditional SIS would strengthen this section.

2. **Section 10.3 (Safety Certification):** The statement "The 'black-box' characteristics of ML models make FMEA and FTA difficult to implement completely" is correct but incomplete. The paper should discuss specific mitigation strategies that have been developed in aerospace: (a) input-output behavioral testing at boundary conditions (DO-178C's requirements-based testing), (b) back-to-back testing against a physics baseline, (c) statistical testing with confidence bounds (as in DO-254 for hardware), and (d) the emerging concept of "assurance cases" for ML (see the EASA concept paper on AI in aviation, or the UK's AMLAS framework).

3. **Section 10.9 (Cross-Domain Comparison):** The comparison with aerospace mentions that "the Boeing 787 and Airbus A350 flight control systems have integrated data-driven adaptive control algorithms" but does not discuss the fundamental architectural difference: these systems use data-driven algorithms WITHIN a deterministic envelope protection framework. The outer loop ensures the aircraft never exceeds structural/aerodynamic limits regardless of what the inner adaptive algorithm does. This "safety envelope" pattern is directly applicable to fusion and should be analyzed in detail.

4. **Section 10.9 (Cross-Domain Comparison):** The discussion of nuclear fission mentions "10 CFR 50's strict requirements for deterministic behavior" but does not discuss the NRC's recent regulatory guidance on "digital instrumentation and control" (NUREG-0800, Standard Review Plan Chapter 7), which provides a concrete framework for qualifying digital systems in nuclear facilities. This framework could be adapted for ML in fusion.

5. **Section 10.7 (TRL Assessment):** The NASA TRL framework was designed for hardware systems and has known limitations when applied to software and ML systems. The paper should acknowledge this and discuss alternative maturity frameworks more suited to ML, such as the MLTRL (Machine Learning Technology Readiness Levels) framework or the SEI's AI/ML maturity model. The current TRL assignments are reasonable but would carry more weight with this methodological caveat.

6. **Section 10.6 (Real-time and Reliability):** The discussion of RTOS integration (VxWorks on DIII-D PCS) is valuable but missing a critical point: deterministic execution time for ML inference. Neural network inference time is input-dependent (data-dependent control flow in activation functions), which challenges the worst-case execution time (WCET) analysis required for real-time safety-critical systems. The paper should discuss techniques for bounding ML inference time: fixed-iteration architectures, early-exit networks, and hardware-guaranteed timing (FPGA).

7. **Section 10.1 (Interpretability):** The discussion of XAI is generic. For safety-critical applications, interpretability serves a specific function: enabling safety assessors to construct arguments about system behavior. The paper should distinguish between (a) "interpretability for physicists" (understanding the physics learned by the model), (b) "interpretability for operators" (understanding why a specific control action was taken), and (c) "interpretability for regulators" (demonstrating that failure modes are bounded and detectable). These three audiences require different XAI techniques.

8. **Section 10.8 (Uncertainty Quantification):** The UQ discussion is technically sound but does not connect UQ to safety decision-making. The critical question is not "can we estimate uncertainty?" but "how should the control system respond to different uncertainty levels?" The paper should discuss the concept of "uncertainty-aware control" where model uncertainty directly triggers safety responses (e.g., switching to a conservative physics-based controller when ML uncertainty exceeds a threshold). This connects directly to the "safety cage" architecture pattern.

9. **Missing section: System-level safety architecture.** The paper discusses component-level ML properties (accuracy, latency, interpretability) but never addresses the system-level architecture for safe ML deployment. Key patterns from aerospace that should be discussed: (a) the "safety cage" or "shield" pattern where a verified physics-based controller monitors and overrides the ML controller; (b) the "voting" pattern where multiple diverse ML models must agree before a control action is taken; (c) the "graceful degradation" pattern where ML failure triggers automatic fallback to conservative operation modes; (d) the "runtime assurance" pattern from the DARPA Assured Autonomy program.

10. **Section 11.3 (LLMs for Fusion):** The paper discusses LLM applications for fusion but does not address the safety implications of LLM "hallucinations" in a nuclear facility context. Even for non-safety-critical applications like knowledge retrieval, LLM-generated misinformation about plasma physics or operational procedures could have safety consequences. The paper should discuss mitigation strategies: retrieval-augmented generation with verified knowledge bases, human-in-the-loop verification, and the distinction between LLM-as-tool (acceptable) and LLM-as-advisor (requires higher assurance).

11. **Missing cross-domain analysis of federated learning.** Section 10.12 mentions federated learning as a future direction but does not connect it to the extensive literature on federated learning in healthcare (where patient data privacy constraints are analogous to fusion data access restrictions). The healthcare domain has developed concrete federated learning frameworks (e.g., NVIDIA Clara, Intel OpenFL) with privacy guarantees (differential privacy, secure aggregation) that could be directly adapted for fusion.

12. **Section 10.9: Missing comparison with autonomous vehicle safety frameworks.** ISO 21448 (Safety of the Intended Functionality, SOTIF) addresses the exact problem fusion faces: ensuring that an ML-based system is safe not only when it malfunctions (traditional functional safety) but also when it encounters scenarios it was not designed to handle (distribution shift, novel plasma states). SOTIF's concept of "known unsafe scenarios" and "unknown unsafe scenarios" maps directly to the fusion problem of "in-distribution" and "out-of-distribution" plasma states.

---

### Transferable Insights from Other Domains

**Insights FROM other domains TO fusion:**

1. **Aerospace safety cage architecture.** Aviation's fly-by-wire systems use envelope protection -- an outer loop of verified safety constraints that cannot be overridden by inner-loop adaptive algorithms. Fusion should adopt this pattern: a verified physics-based controller as the outer safety envelope, with ML controllers operating within those bounds. This is more practical than trying to certify the ML controller itself.

2. **Automotive SOTIF framework.** ISO 21448's systematic approach to identifying scenarios where perception/control systems may fail due to functional insufficiency (not hardware/software faults) directly applies to ML plasma controllers encountering novel plasma states.

3. **Medical device software lifecycle (IEC 62304).** The medical device industry's risk-based classification of software (Class A/B/C based on potential harm) provides a template for classifying fusion ML applications by safety criticality and applying proportionate development rigor.

4. **Nuclear LOPA methodology.** Layer of Protection Analysis from the process industry provides a systematic framework for positioning ML as one layer in a multi-layer safety architecture, rather than requiring ML to be the sole safety barrier.

5. **Railway safety cases (EN 50129).** The railway industry's structured safety case argumentation -- combining design assurance, verification evidence, and operational experience -- provides a template for building safety arguments for ML-based fusion control systems.

**Insights FROM fusion TO other domains:**

1. **One-shot learning via ensemble Kalman filtering.** The approach demonstrated by Seo et al. (Section 2.1) for learning from extremely scarce, expensive data has direct implications for any domain where data acquisition is costly (e.g., clinical trials, rare disease diagnosis, space systems).

2. **Physics-informed reward shaping for RL.** The NTM-aware reward function design (Section 2.1) demonstrates a general pattern for incorporating domain physics into RL reward structures, applicable to any physical system control (chemical processes, power grids, structural systems).

3. **FPGA deployment of ML for ultra-low-latency control.** The DIII-D FPGA deployment pattern (Section 4.3) for sub-millisecond ML inference is directly applicable to aerospace (flight control), automotive (collision avoidance), and industrial robotics.

4. **Cross-device transfer learning for scarce-data domains.** The tokamak cross-device transfer methods (Section 8.2) address the same fundamental challenge faced in medical AI (transferring models across hospitals with different equipment) and manufacturing (transferring across production lines).

5. **Surrogate models for extreme-computation physics.** The FNO and neural operator approaches (Section 6) achieving 10^6x speedup over full-physics simulations are directly applicable to climate modeling, materials design, and aerodynamic simulation.

---

### Recommendation to Authors

I recommend **Minor Revision** with the following priority actions:

1. **Expand Section 10.3 (Safety Certification)** by at least 1000 words to include: (a) a concrete safety certification pathway for ML in fusion, distinguishing between ML-as-recommendation and ML-as-final-element; (b) discussion of the safety cage / runtime assurance architecture pattern; (c) reference to emerging ML assurance frameworks (AMLAS, EASA AI roadmap, ISO/IEC 23894). This is the single most important revision for the paper's credibility with safety-critical systems practitioners.

2. **Deepen Section 10.9 (Cross-Domain Comparison)** by adding: (a) a systematic analysis of the safety envelope pattern from aviation; (b) SOTIF (ISO 21448) as a framework for addressing "unknown unknown" plasma states; (c) specific examples of how nuclear LOPA methodology could position ML in fusion safety architectures. Consider adding a comparison table that maps specific safety engineering artifacts (safety requirements, FMEA, verification test cases, safety case arguments) from aerospace/nuclear to their fusion equivalents.

3. **Add a brief subsection on system-level safety architecture** (could be Section 10.13 or integrated into 10.6) discussing watchdog monitors, voting architectures, graceful degradation, and safety cage patterns. This is the gap most likely to be noticed by reviewers from safety-critical industries.

4. **Add a brief policy and governance discussion** (could be a new Section 10.14) addressing: dual-use considerations, data governance frameworks, workforce implications, and the regulatory landscape for AI in nuclear facilities.

5. **Challenge the implicit data-scaling assumption** by adding a paragraph in Section 10.12 or Section 8.1 discussing whether physics-constrained systems may exhibit fundamentally different scaling behavior than language/vision models, and what this implies for the "foundation model" research direction.

These revisions would elevate the paper from a good fusion-domain survey to a genuinely cross-disciplinary contribution that safety-critical AI practitioners from other fields would find valuable and actionable.
