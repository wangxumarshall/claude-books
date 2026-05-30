# Phase 5: Devil's Advocate Report

**Paper:** AI for Fusion V2 -- Artificial Intelligence and Machine Learning for Magnetic Confinement Fusion Plasma Control: A Comprehensive Review (2024-2026)

**Reviewer Role:** Devil's Advocate

**Date:** 2026-05-30

**Pipeline Stage:** Phase 5 -- Full Devil's Adversarial Review of Final Manuscript

---

## Verdict: REVISE

The V2 manuscript substantially improves upon the earlier draft: it now correctly reports the preprint ratio (78%), adds a verification-level summary table (Appendix A.5), expands cross-domain comparison with specific regulatory references (IEC 61508, DO-178C, 10 CFR 50), and introduces honest discussion of failure modes and negative results (Section 10.10). The TRL assessments are now internally consistent with the verification-level table. However, three structural problems persist that would undermine the paper's credibility with the target audience of plasma physicists and fusion engineers who are rightly skeptical of AI hype: (1) the paper systematically conflates "demonstrated in simulation" with "validated for deployment," (2) the preprint-heavy evidence base creates an authority-laundering risk that the paper acknowledges but does not mitigate, and (3) the "milestone breakthrough" framing in the abstract overstates the field's actual readiness for engineering application. These issues require revision before the paper is suitable for publication in a top-tier fusion journal.

---

## Strongest Counter-Argument (against the paper's central thesis)

The paper's central thesis is that 2024-2026 represents a period of "milestone breakthroughs" in which AI/ML for fusion plasma control is "transitioning from proof-of-concept toward engineering application exploration." This framing is misleading. The paper's own evidence, when read critically, tells a different story: the field remains overwhelmingly at the proof-of-concept stage, with a single genuinely experimentally validated breakthrough (Seo et al. 2024 on DIII-D) surrounded by a large body of simulation-only or single-device results.

The verification-level table in Appendix A.5 is the most honest part of the paper. Of the 43 key studies listed, only 12 (28%) are classified as "experimental verification," and of those, 8 are from DIII-D. The remaining 31 studies (72%) are either simulation-only (20 studies, 47%) or simulation+partial experiment (11 studies, 26%). The paper's abstract claims "multiple milestone breakthroughs," but the actual evidence base shows one breakthrough (Seo et al., Nature 2024) and a collection of promising but unvalidated demonstrations.

The "transitioning toward engineering application" claim is further undermined by the paper's own TRL assessments. The highest TRL assigned to any sub-domain is 5-6 (ML disruption prediction and balance reconstruction), and the paper itself notes that ML disruption prediction models exhibit 20-30% false positive rates in real deployments -- hardly consistent with engineering readiness. The median TRL across all eight sub-domains is 3.5, which corresponds to "proof of concept in laboratory environment," not "transitioning toward engineering application."

The most damaging counter-argument is this: if we remove the single Seo et al. result from the evidence base, the paper's narrative collapses. Without that Nature paper, the field's strongest claim to experimental validation would be Kim et al.'s ELM suppression on DIII-D and KSTAR (conference abstract, not yet a full peer-reviewed paper) and a handful of balance reconstruction deployments on smaller devices. The paper is, in essence, a review of a field that has produced one genuine breakthrough and a large volume of preliminary work. That is not a criticism of the field -- it is an honest assessment of where things stand. But the paper's framing as a period of "multiple milestone breakthroughs" is not supported by its own evidence.

---

## Issue List

### CRITICAL

**C1. Simulation-only results are consistently presented as if they validate real-world applicability**

The paper's abstract and introduction claim "DRL successfully avoided tearing mode instability on DIII-D (Nature, 2024)" and "ML adaptive controllers demonstrated cross-device ELM suppression on DIII-D and KSTAR (APS-DPP 2024)." These are genuine experimental results. But the abstract also claims "Transformer-based foundation models began to be used for tokamak plasma dynamics modeling" and "digital twin frameworks opened new pathways for intelligent fusion power plant operations" -- these are simulation-only results presented in the same breath as experimental breakthroughs, creating a false equivalence.

Throughout the paper, simulation-only results are described using the same language as experimental validations. For example:
- Section 2.4: "Zero-shot generative RL" is described as achieving "zero-shot generalization" on an HL-3 simulator, not on the actual HL-3 device.
- Section 6.2: FNO is described as achieving "six orders of magnitude speedup" but this is benchmarked against JOREK simulation data, not experimental measurements.
- Section 9.1: The digital twin framework is described as "opening new pathways" but is a conceptual framework using NVIDIA Omniverse, not a validated system.

The paper does include an Appendix A.5 table that distinguishes verification levels, but this distinction is not carried into the main text. A reader who only reads the abstract and conclusions would come away with a significantly inflated impression of the field's maturity.

**C2. The 78% preprint ratio creates an authority-laundering risk that the paper acknowledges but does not mitigate**

The paper now correctly reports that 78% of its references are preprints (91 out of 117). It even notes that "readers should be aware of the limitations of preprint conclusions when citing them." However, this caveat is buried in the appendix methodology section and does not appear in the abstract, introduction, or conclusions -- the sections that most readers will actually read.

More importantly, the paper does not distinguish between preprints that have since been published in peer-reviewed venues and those that remain unpublished. Some preprints cited (e.g., Seo et al. was originally a preprint that became a Nature paper) are now peer-reviewed, while others (e.g., many of the arXiv preprints from 2025-2026) have not yet undergone any review. Treating all preprints as equivalent evidence is methodologically unsound.

The TRL assessments are particularly vulnerable to this problem. When the paper assigns "Foundation models: TRL 3" based on TokaMind and PanoMHD, both of which are preprints, it is making an authoritative-sounding maturity assessment based on unreviewed work. A funding agency program manager reading this table would have no way to know that the underlying evidence has not been independently verified.

**C3. The "cross-device portability" claim rests on a single cross-device experimental result**

The paper repeatedly emphasizes cross-device portability as a key achievement. Section 4.2 describes Kim et al.'s ELM suppression as demonstrating that "the same control architecture successfully achieved ELM suppression on both DIII-D and KSTAR." This is presented as proof that ML control strategies are portable across devices.

However, DIII-D and KSTAR are both mid-size, conventional aspect ratio tokamaks with similar physics parameters. The claim of "cross-device portability" would be far more compelling if it included results from devices with fundamentally different characteristics (e.g., a spherical tokamak like MAST or a superconducting device like EAST or a stellarator like W7-X). The paper's own Section 10.4 acknowledges that "the performance on devices with different scales and different magnetic field configurations still needs systematic verification," but this caveat does not appear in the abstract or conclusions, where the cross-device claim is presented without qualification.

The cross-device disruption prediction results (Shen et al., Zheng et al.) are simulation-only, using historical data from JTEXT and EAST. These are important contributions but do not constitute experimental validation of cross-device portability.

---

### MAJOR

**M1. The paper conflates "computational speedup" with "practical utility"**

Sections 6 and 11 repeatedly claim "orders of magnitude" speedups for surrogate models (FNO: 10^6x, TorbeamNN: 10^3x, GyroSwin: 10^3x). These numbers are technically correct but misleading in context. The speedups are measured relative to full-physics simulation codes, not relative to the simplified models that are actually used in real-time control systems. For example, EFIT balance reconstruction is already fast (tens of milliseconds); the claim that ML methods can do it faster is useful but not the paradigm shift implied by "orders of magnitude speedup."

More importantly, the paper does not adequately discuss the accuracy-speed tradeoff. A surrogate model that is 10^6 times faster but 10% less accurate may not be useful for safety-critical applications. The paper mentions this concern briefly in Section 6.2 (FNO limitations) but does not systematically address it across all surrogate model results.

**M2. The DIII-D dominance in the evidence base is under-discussed**

The paper's own verification table (Appendix A.5) shows that 8 of 12 experimentally validated results come from DIII-D. The paper lists 13+ devices in Section 10.11, but the experimental evidence is overwhelmingly from one device. DIII-D is a mid-size, highly flexible, heavily diagnosed device with strong US DOE investment in AI/ML research. It is not representative of ITER, SPARC, or DEMO.

The paper acknowledges this bias in Section 10.4 ("cross-device portability") but treats it as a future challenge rather than a current limitation. A more honest framing would be: "The experimental validation of AI/ML for fusion plasma control is currently limited to a small number of devices, with DIII-D accounting for the majority of results. The applicability of these results to next-generation devices remains an open question."

**M3. The "foundation model" terminology creates confusion despite the paper's own critique**

Section 8.1 contains an excellent critical analysis of why "foundation model" is an overstatement for TokaMind and PanoMHD. The paper correctly notes that fusion data is "orders of magnitude smaller than NLP/CV fields" and that current models are "more accurately described as multi-modal pre-training frameworks."

However, the paper then continues to use "foundation model" (and its Chinese translation) throughout the rest of the paper, including in the abstract ("Transformer-based foundation models began to be used"), the conclusions ("foundation models are expected to become core enabling technology"), and Section 10.12 ("develop foundation models for the fusion domain"). This is intellectually inconsistent: the paper simultaneously critiques and promotes the same terminology. If the paper believes "foundation model" is misleading, it should use the more accurate term consistently.

**M4. The failure modes section (10.10) is valuable but incomplete**

Section 10.10 is one of the paper's strongest contributions, honestly documenting failure modes including high false positive rates, sim-to-real transfer failures, and overfitting to specific devices. However, the section is incomplete in two important ways:

First, it does not discuss the failure modes of the most cited result -- Seo et al. 2024. What are the limitations of the DRL tearing mode avoidance system? Under what conditions does it fail? How does it perform when the plasma enters regimes not seen during training? The paper presents this result as an unqualified success without discussing its boundaries.

Second, the section does not discuss the failure modes of surrogate models and neural operators. FNO models assume periodic boundary conditions (the paper notes this in Section 6.2), but the implications for real plasma control are not explored. If an FNO-based control model encounters a non-periodic boundary condition in real-time operation, what happens? Does it degrade gracefully, or does it produce physically nonsensical outputs?

**M5. The safety certification discussion (Section 10.3) is thorough but lacks a concrete roadmap**

The paper provides an excellent discussion of safety certification challenges, referencing IEC 61508, IEC 61511, and DO-178C. The potential compliance pathways (ML as "additional protection layer," V-model development, in-service monitoring) are well-chosen. However, the discussion remains at the level of "what should be done" without specifying "how to do it." No existing fusion AI system has undergone any of these certification processes. The paper would be stronger if it included a concrete example of how even a simple ML model (e.g., a disruption predictor) could be certified under these frameworks.

**M6. The paper overstates the novelty of several contributions**

Several results are described as "first" or "breakthrough" when they are incremental advances:

- Section 2.1: "DRL successfully avoided tearing mode instability" is described as a "milestone breakthrough." While this is indeed a landmark result, the paper does not note that DRL for plasma control was demonstrated on TCV two years earlier (Degrave et al. 2022). The Seo et al. result is better characterized as "the first experimental demonstration of DRL for instability avoidance" rather than a general breakthrough in DRL for plasma control.

- Section 8.1: TokaMind is described as "the first multi-modal transformer foundation model for fusion." This may be technically true, but the paper does not compare it with other multi-modal approaches in adjacent fields (e.g., weather forecasting, materials science) to contextualize its actual novelty.

- Section 11.4: XiHeFusion is described as "the first large language model specifically for nuclear fusion." This is true but the paper does not discuss whether a domain-specific LLM is actually needed, or whether a general-purpose LLM with appropriate prompting would achieve similar results.

---

### MINOR

**m1. The 2024-2026 window includes too many pre-window references**

The paper claims to focus on 2024-2026 literature but includes numerous references from 2022-2023:
- Mathews 2022 [47,101] (edge plasma turbulence)
- Zhu et al. 2022 [54] (divertor detachment)
- Kube et al. 2021 [68] (streaming analysis)
- Gopakumar et al. 2023 [40,41] (FNO)
- Arnold et al. 2023 [23] (continuous CNN)
- Shen et al. 2023 [24,26] (cross-tokamak disruption prediction)
- Zheng et al. 2022 [25] (cross-tokamak disruption prediction)

These are labeled as "contextual" but having ~15% of references outside the stated window weakens the "2024-2026" claim. The paper would be stronger if it either tightened the window or explicitly acknowledged that some foundational works are included for context.

**m2. The paper does not discuss computational costs of training foundation models**

Section 10.6 includes a useful table of training costs for different ML approaches. However, the foundation model row ("64 GPU x 200+ hours") is a rough estimate, not based on actual reported costs from TokaMind or PanoMHD papers. The environmental and financial costs of training large models are increasingly important considerations in ML research, and the paper would benefit from a more honest discussion of whether these costs are justified given the limited training data available.

**m3. The cross-domain comparison (Section 10.9) is improved but still superficial**

The V2 version adds specific regulatory references (IEC 61508, DO-178C, 10 CFR 50) and discusses V-model development and in-service monitoring. This is a significant improvement over the V1 version. However, the comparison still lacks concrete case studies. The paper would be stronger if it included a specific example of how an ML system was certified in aerospace or nuclear fission, and what lessons could be applied to fusion.

**m4. The paper does not discuss the opportunity cost of AI research in fusion**

The paper presents AI/ML as an enabling technology for fusion, but does not discuss whether the same resources (researcher time, funding, computational resources) might be better spent on other approaches to fusion's core challenges. For example, could the effort spent on DRL control be better spent on improving conventional control systems or on understanding the underlying physics better? This is a legitimate question that a comprehensive review should address.

**m5. Chinese-language literature is likely underrepresented**

The paper's search strategy is English-language and arXiv-centric. China operates several of the world's most advanced tokamaks (EAST, HL-2A/HL-3) and has significant AI/ML investment. It is likely that important Chinese-language publications in journals like Nuclear Fusion and Plasma Physics (Chinese editions) or in Chinese conference proceedings are not captured. The paper's coverage of Chinese devices is thin compared to DIII-D and KSTAR.

**m6. The TRL assessment does not distinguish between "demonstrated" and "deployed"**

The TRL framework distinguishes between "demonstrated in relevant environment" (TRL 5-6) and "system prototype demonstrated in operational environment" (TRL 7-8). The paper assigns TRL 5-6 to ML disruption prediction, but the actual deployments are limited to a few devices with significant performance limitations (20-30% FPR). A more nuanced assessment would distinguish between "demonstrated on one device" and "deployed as operational system on multiple devices."

---

## Ignored Alternative Explanations

**AE1. The success of DRL on DIII-D may reflect DIII-D's exceptional diagnostic coverage, not DRL's general capability**

DIII-D has approximately 50 independent diagnostic systems, far more than most other devices. The Seo et al. DRL system uses multi-modal sensing (magnetic diagnostics, Thomson scattering, ECE) to build a real-time state estimate. On a device with fewer diagnostics, the same DRL approach might fail due to insufficient observability. The paper does not discuss whether the DRL approach is fundamentally dependent on DIII-D's exceptional diagnostic infrastructure.

**AE2. The "cross-device" ELM suppression result may reflect the similarity of DIII-D and KSTAR, not the generality of the approach**

DIII-D and KSTAR are both conventional aspect ratio tokamaks with similar plasma parameters. The successful transfer of the ELM suppression controller between them may reflect their physical similarity rather than the generalizability of the ML approach. A more stringent test would be transfer between devices with fundamentally different characteristics (e.g., conventional vs. spherical tokamak, or tokamak vs. stellarator).

**AE3. The high AUC scores for disruption prediction models may not translate to operational utility**

The paper reports AUC improvements of ~5% for Transformer-based disruption predictors (Section 3.2). However, AUC is a metric that can be misleading in highly imbalanced datasets. When the base rate of disruptions is very low (e.g., 1-5% of discharges), even a model with AUC > 0.95 can have an unacceptably high false positive rate. The paper's own Section 10.10 acknowledges 20-30% FPR in real deployments, but the AUC-focused presentation in Section 3 creates an overly optimistic impression.

**AE4. The "orders of magnitude" speedup claims for surrogate models may not be operationally relevant**

If the real-time control system already operates within the required latency budget using conventional methods, a 10^6x speedup is operationally irrelevant. The paper does not discuss what latency improvements are actually needed for specific control tasks, making it impossible to assess whether the surrogate model speedups are solving real problems or are solutions in search of problems.

**AE5. The paper's positive framing may reflect publication bias in the underlying literature, not actual progress**

The paper's own Section 10.10 acknowledges "significant positive-results bias" in the field. But the paper does not apply this insight to its own analysis: by presenting the literature's positive results as evidence of progress, the paper inherits the same bias. The true state of the field may be less advanced than the paper suggests, because failed AI/ML experiments are not published.

---

## Observations (Non-Defects)

**O1. The paper's structure is well-organized and comprehensive**

The eight-dimension structure (DRL control, disruption prediction, ELM detection, equilibrium reconstruction, surrogate models, PINNs, foundation models, digital twins) provides a clear and logical framework for organizing the literature. The extended topics (stellarators, HTS magnets, LLMs, ICF, data infrastructure, gyrokinetic surrogates) add breadth without overwhelming the core analysis.

**O2. The verification-level summary table (Appendix A.5) is a major strength**

The table that classifies 43 key studies by verification level (simulation, simulation+experiment, experiment) is the most valuable contribution of the paper. It provides readers with a clear, honest assessment of the evidence base that is not available in any other review. This table should be promoted to the main text and referenced prominently in the abstract and conclusions.

**O3. The failure modes section (10.10) is a valuable and unusual contribution**

Most reviews in this field focus exclusively on positive results. The paper's honest discussion of failure modes (high FPR, sim-to-real failures, overfitting, PINN convergence issues) is a significant contribution that will help the field learn from its mistakes. This section should be expanded and made more prominent.

**O4. The TRL assessment, while imperfect, is a useful framework**

The TRL framework provides a common language for discussing the maturity of different AI/ML approaches. While the specific TRL assignments may be debatable, the framework itself is valuable for helping researchers and funding agencies understand where each sub-field stands.

**O5. The safety certification discussion (Section 10.3) is thorough and well-referenced**

The discussion of IEC 61508, IEC 61511, and DO-178C, and the potential compliance pathways (ML as additional protection layer, V-model development, in-service monitoring) is well-researched and provides practical guidance for researchers planning to deploy ML systems in fusion environments.

**O6. The paper's honesty about the preprint-heavy evidence base is commendable**

The paper correctly reports the 78% preprint ratio and explicitly warns readers about the limitations of preprint conclusions. While this caveat should be more prominent, the fact that it is included at all is unusual and commendable.

---

## Summary Table

| Issue ID | Severity | Topic | Action Required |
|----------|----------|-------|-----------------|
| C1 | CRITICAL | Simulation-only results presented as real-world validation | Distinguish simulation vs. experimental results in abstract, conclusions, and throughout main text |
| C2 | CRITICAL | 78% preprint ratio creates authority-laundering risk | Add prominent caveat in abstract and conclusions; distinguish published vs. unpublished preprints |
| C3 | CRITICAL | Cross-device portability claim rests on single result | Qualify cross-device claims; discuss DIII-D/KSTAR similarity |
| M1 | MAJOR | "Computational speedup" conflated with "practical utility" | Discuss accuracy-speed tradeoff; contextualize speedups relative to existing real-time systems |
| M2 | MAJOR | DIII-D dominance under-discussed | Add explicit discussion of device bias and its implications |
| M3 | MAJOR | "Foundation model" terminology inconsistent | Either use consistently or replace with accurate term throughout |
| M4 | MAJOR | Failure modes section incomplete | Add failure modes for Seo et al. and surrogate models |
| M5 | MAJOR | Safety certification lacks concrete roadmap | Add example of how an ML model could be certified |
| M6 | MAJOR | Novelty overstated for several contributions | Contextualize "first" claims; compare with adjacent fields |
| m1 | MINOR | Too many pre-window references (~15%) | Tighten window or relabel as contextual |
| m2 | MINOR | Training cost discussion incomplete | Add honest discussion of computational costs for foundation models |
| m3 | MINOR | Cross-domain comparison still lacks case studies | Add specific certification examples from aerospace/nuclear |
| m4 | MINOR | Opportunity cost of AI research not discussed | Acknowledge that resources spent on AI could be spent elsewhere |
| m5 | MINOR | Chinese-language literature underrepresented | Acknowledge search limitations; consider Chinese-language sources |
| m6 | MINOR | TRL "demonstrated" vs. "deployed" not distinguished | Add nuance to TRL assessments |

---

## Recommendations for Revision

1. **Promote the verification-level table to the main text.** This is the paper's most valuable contribution and should be prominently featured, not buried in an appendix.

2. **Add a "Limitations of This Review" section** that explicitly discusses: (a) the preprint-heavy evidence base, (b) the DIII-D dominance in experimental results, (c) the difficulty of distinguishing simulation-only from experimentally validated results in the current literature.

3. **Reframe the abstract and conclusions** to accurately reflect the field's actual maturity. Instead of "multiple milestone breakthroughs," use language like "one landmark experimental demonstration (Seo et al. 2024) accompanied by a growing body of simulation-validated work."

4. **Standardize terminology.** Either commit to "foundation model" with appropriate caveats in every usage, or replace it with "multi-modal pre-trained model" throughout.

5. **Expand the failure modes section** to cover the most cited results (Seo et al., Kim et al.) and to discuss failure modes of surrogate models in real-time control contexts.

6. **Add a concrete safety certification example** showing how a specific ML model (e.g., a disruption predictor) could be certified under IEC 61508 or DO-178C.

---

*Report prepared per Phase 5 Devil's Advocate protocol.*
*Full adversarial review of AI-for-Fusion-V2.md.*
