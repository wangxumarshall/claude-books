# EIC Review Report

**Paper Title:** Artificial Intelligence and Machine Learning for Magnetic Confinement Fusion Plasma Control: A Comprehensive Review (2024-2026)

**Journal:** Nuclear Fusion

**Reviewer Role:** Editor-in-Chief

**Date:** 2026-05-30

**Manuscript Version:** V2 (revised incorporating prior review feedback)

---

## Overall Assessment: Minor Revision

This V2 manuscript represents a substantial improvement over the prior version. The authors have addressed the majority of critical issues raised in the initial EIC review and Devil's Advocate report: the preprint percentage is now correctly and transparently reported (78%), the verification-level analysis of 40 key studies adds genuine analytical depth, the critical assessment of "foundation model" terminology is intellectually rigorous, and the methodology appendix now documents search strategy with reproducible detail. The paper's core strengths -- its breadth across 8 core dimensions and 6 extension topics, its novel TRL framework, its cross-domain safety comparison, and its honest treatment of failure modes -- remain intact and are strengthened in this revision.

However, several issues persist that prevent outright acceptance: the absence of actual figures (only text descriptions remain), the lack of a quantitative meta-analysis that synthesizes results across methods, residual structural redundancy, and the fact that 78% preprint reliance -- now honestly reported -- still weakens the evidence base for a review intended to guide the field's direction. These are addressable in a single focused revision cycle.

---

## Dimension Scores

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Originality | 78/100 | The TRL assessment framework (Section 10.7), cross-domain safety comparison with aerospace/fission/process-control (Section 10.9), systematic failure mode catalog (Section 10.10), verification-level classification of 40 key studies (Appendix A.5), and the critical evaluation of "foundation model" applicability to fusion (Section 8.1) all represent genuine analytical contributions beyond a standard literature survey. However, the majority of the paper (Sections 2-9, 11) remains structured as an annotated literature review rather than an analytical synthesis. The cross-domain comparison, while novel in conception, remains at a high level of generality -- specific regulatory pathways (e.g., how DO-178C DAL levels map to fusion control functions) are not worked through. |
| Significance | 82/100 | The paper addresses a field undergoing rapid growth with direct implications for ITER operations and future fusion power plants. The TRL assessment (median 3.5 across sub-domains, ranging from TRL 2-3 for PINNs to TRL 5-6 for disruption prediction and equilibrium reconstruction) provides the community with a realistic calibration of where AI/ML for fusion actually stands -- a valuable corrective to the hype cycle. The 78% preprint ratio disclosure and the 30% experimental validation statistic (with 67% from DIII-D alone) are important findings that should shape how the community evaluates claims in this space. The functional safety discussion (IEC 61508, DO-178C reference) in Section 10.3 is practically significant for ITER planning. |
| Rigor | 71/100 | The literature search methodology (Appendix A.3) now documents keyword strategies, databases, date ranges, and inclusion/exclusion criteria with quantitative screening records (1758 initial records, 1451 after deduplication, 117 included). This represents meaningful methodological improvement. The verification-level analysis is a genuine rigor contribution. However, several weaknesses persist: (1) the TRL assessments remain subjective without a formal rubric mapping evidence to levels; (2) the search lacks PRISMA flow documentation; (3) no quantitative meta-analysis is attempted despite heterogeneous metrics being available for disruption prediction (AUC values across multiple studies) and surrogate models (speedup factors); (4) some specific claims lack supporting data (e.g., "sub-millisecond FPGA inference" in Section 4.3 cites the Dave et al. preprints but provides no measured latency numbers). |
| Clarity | 85/100 | The paper is exceptionally well-organized across 12 sections with consistent bilingual (Chinese/English) abstracts and section headers. Tables are informative and well-formatted (computation cost table in Section 10.6, TRL table in Section 10.7, verification-level table in Appendix A.5). The progression from core methods (Sections 2-5) through enabling technologies (Sections 6-8) to system integration (Section 9) and critical analysis (Section 10) is logical. Figure descriptions are detailed and would produce informative visualizations. However: (1) the paper is approximately 30,000 words, substantially exceeding typical Nuclear Fusion review length (~15,000 words); (2) several cross-device portability discussions appear with overlapping content in Sections 3.5, 8.2, 10.4, and 10.11; (3) the NTM physics tutorial in Section 2.1 reads as textbook material rather than review analysis. |
| Relevance | 88/100 | Directly relevant to the Nuclear Fusion readership. The paper covers topics at the intersection of plasma physics and AI/ML -- precisely where the field is moving. The engineering deployment perspective (hardware trade-offs, RTOS integration, safety certification) bridges the ML research and fusion engineering communities. The device coverage (DIII-D, KSTAR, TCV, JET, EAST, W7-X, HL-3, MAST, WEST, ST40, EXL-50U, ADITYA, plus non-tokamak devices) is broad. The practical implications for ITER preparation (disruption prediction, ELM control, burning plasma dynamics) are clearly articulated. The inclusion of Chinese devices (EAST, HL-3, HL-2A, EXL-50U) is strategically important given the geographic distribution of major fusion programs. |
| Completeness | 76/100 | Strong coverage of 8 core dimensions with 117 references across 13+ devices. The 6 extension topics (stellarator optimization, HTS magnets, LLMs, ICF, data infrastructure, 5D gyrokinetics) add breadth. However: (1) no dedicated "state of the field as of 2023" baseline section exists, making it difficult to assess incremental progress; (2) radiation effects on AI hardware for in-vessel deployment are not discussed; (3) adversarial robustness of ML models in safety-critical fusion applications is absent; (4) the IAEA's developing regulatory framework for AI in nuclear facilities receives only passing mention; (5) some emerging topics could benefit from deeper coverage -- federated learning (mentioned only in Section 10.12 outlook), edge computing architectures, and the role of synthetic data generation are underdeveloped; (6) EU/UK fusion programs (JET decommissioning data, STEP planning) are underrepresented relative to US and Asian programs. |

---

## Strengths

1. **Intellectual honesty about evidence quality.** The transparent reporting of the 78% preprint ratio, the 30% experimental validation rate, and the DIII-D concentration (67% of experimental results from one device) is commendable and sets a standard for reviews in this fast-moving field. This honesty, rather than undermining the paper, strengthens its credibility as a guide for researchers and program managers.

2. **Novel analytical frameworks that go beyond survey.** The TRL assessment (Section 10.7), cross-domain safety comparison (Section 10.9), failure mode catalog (Section 10.10), verification-level classification (Appendix A.5), and critical "foundation model" evaluation (Section 8.1) represent genuine intellectual contributions. These are not merely reorganized abstracts but structured analytical tools that provide actionable insights for the community.

3. **Engineering-aware perspective that bridges communities.** The inclusion of hardware deployment trade-offs (GPU/FPGA/ASIC, Section 10.6), computation cost tables, real-time OS considerations, functional safety standards (IEC 61508, DO-178C), and model quantization/knowledge distillation discussion provides practical value that pure ML reviews lack. The mixed deployment architecture recommendation (FPGA for ELM detection, GPU for disruption prediction, CPU for preprocessing) reflects engineering realism.

4. **Comprehensive device and method coverage.** The paper surveys AI/ML work across 13+ devices spanning the US, EU, China, South Korea, India, and Switzerland, covering tokamaks (conventional and spherical), stellarators, and non-tokamak magnetic confinement devices. This breadth enables the cross-device portability analysis that is central to the field's future.

5. **Improved methodology documentation.** The Appendix A.3-A.4 sections now provide reproducible search methodology with database records, keyword strategies, screening statistics, and explicit inclusion/exclusion criteria. The Appendix A.5 verification-level table with 40 classified studies is a significant analytical contribution that enables readers to independently assess evidence quality.

---

## Weaknesses

1. **Absence of actual figures.** Five detailed figure descriptions are embedded in the text (Figures 1-5), but no actual figures are included. For a review of this scope and length, visual summaries are essential for reader comprehension and retention. The TRL radar chart, method comparison scatter plot, device coverage map, and research landscape bubble chart described in the text would substantially improve the paper's utility. This was flagged in the prior review and remains unaddressed.

2. **No quantitative meta-analysis despite available data.** Multiple sub-fields have sufficient published results for quantitative synthesis: disruption prediction (AUC values from Spangher et al., Shen et al., Zheng et al., Peng et al. across multiple devices), surrogate models (speedup factors from Gopakumar et al., GyroSwin, TorbeamNN, SOLPS-NN), and DRL control (reward convergence and performance metrics from Seo et al., Wang et al., Sonker et al.). A forest plot or systematic comparison table with normalized metrics would transform the paper from a narrative survey into a quantitative reference.

3. **Structural redundancy and excessive length.** Cross-device portability challenges are discussed in Sections 3.5, 8.2, 10.4, and 10.11 with overlapping content. The NTM physics tutorial in Section 2.1 (~500 words) and ELM physics tutorial in Section 4.5 (~300 words) read as textbook material. At ~30,000 words, the paper substantially exceeds typical Nuclear Fusion review length. These issues were also raised in the prior review and remain partially unaddressed.

4. **TRL assessment lacks formal rubric.** While the TRL framework is a valuable contribution, the ratings are presented without showing the evidence-to-level mapping. The text provides post-hoc justification for each rating but does not define, ex ante, what specific criteria must be met for each TRL level in the fusion AI context. This makes the assessments appear subjective. For example, what precisely distinguishes TRL 4 from TRL 5 for DRL control? The paper assigns "TRL 4-5" but does not specify which sub-criteria are met at each level.

5. **Cross-domain comparison remains high-level.** Section 10.9 mentions DO-178C, IEC 61508, and 10 CFR 50 but does not map specific fusion AI challenges to specific regulatory requirements. How would a DRL tearing mode avoidance controller be classified under IEC 61508 SIL levels? What specific DAL level under DO-178C would a disruption prediction system require? Without this level of specificity, the comparison provides orientation but not actionable guidance.

---

## Specific Issues

1. **[Section 1.1] The four bottleneck claims need citations.** The four challenges listed (multi-variable coupling, fast transients, cross-device generalization, burning plasma physics) are well-known but each claim should cite specific references. The current notation "[journal paper][1,2]" etc. is placeholder-style and should be verified against the actual reference list.

2. **[Section 2.1] Excessive detail on a single result.** The Seo et al. Nature 2024 analysis receives approximately 1,500 words including NTM physics background, reward function design, and ensemble Kalman filter explanation. While this is a landmark result, the level of detail is disproportionate. The NTM physics subsection (2.1, paragraphs on beta_N threshold and bootstrap current) reads as a textbook introduction. Consider condensing to 800 words and moving physics background to an appendix.

3. **[Section 3.2] Transformer disruption prediction AUC claim lacks precision.** The paper states the Transformer model achieved "AUC improvement of approximately 5% over existing methods." This should specify: 5 percentage points or 5% relative? Over which baseline methods? On which datasets? The vagueness weakens what should be a quantitative comparison.

4. **[Section 4.2] Conference abstract as primary evidence for a "breakthrough."** The ELM suppression result (Kim et al., APS-DPP 2024) is cited only as a conference abstract [28]. For a claim described as "breakthrough" ("突破性成果"), the lack of a peer-reviewed publication should be more explicitly acknowledged. The paper does note it as "[conference report]" but the narrative tone ("breakthrough") overstates the evidence level.

5. **[Section 7.5] PINNs limitations section is strong but unbalanced.** The section provides an honest assessment of PINNs' convergence difficulties and TRL 2-3 status. However, it reads as predominantly negative without adequately discussing recent advances that partially address these issues (e.g., curriculum learning for stiff PDEs, domain decomposition PINNs). The section would benefit from a more balanced "challenges and partial solutions" framing.

6. **[Section 8.1] "Foundation model" critique is excellent but terminology remains inconsistent.** The critical assessment paragraph (approximately 400 words) analyzing data scarcity, comparison with meteorology and materials science, and the proposal to use "multi-modal pretrained framework" instead is one of the paper's strongest analytical contributions. However, the term "foundation model" continues to appear in the abstract ("Transformer-based foundation models"), section titles, and conclusion without consistent qualification. This inconsistency undermines the critical argument. Either apply the corrected terminology throughout or add an explicit footnote at each remaining usage.

7. **[Section 10.7] TRL table needs methodology column.** The TRL assessment table assigns ratings (e.g., "DRL control: TRL 4-5") with brief explanations. A methodology column showing: (a) number of peer-reviewed studies supporting the rating, (b) number of devices validated on, (c) highest validation level achieved (simulation / single-device experiment / multi-device experiment / ITER-relevant conditions) would make the assessment reproducible and auditable.

8. **[Section 10.9] Cross-domain comparison needs specificity.** The comparison with aerospace, fission, and process control provides orientation but lacks actionable detail. Recommendation: For each domain, identify one specific case study of ML certification (e.g., how Airbus certified A350 fly-by-wire adaptive elements; how Kairos Power obtained NRC approval for ML-assisted control) and map the certification pathway to a specific fusion AI application.

9. **[Section 10.10] Failure mode catalog is valuable but incomplete.** Missing failure modes include: (a) adversarial robustness (can diagnostic noise patterns fool ML classifiers?); (b) model degradation in deployed systems (concept drift as wall conditions change over a campaign); (c) catastrophic forgetting when fine-tuning on new data; (d) data poisoning risks in shared datasets. The section would benefit from a "failure taxonomy" table organizing failures by type (data, model, deployment, system integration).

10. **[Section 11] Extension topics lack connection to core theme.** Section 11 covers 6 topics across approximately 4,000 words. Some topics (stellarator optimization, HTS magnets) are only loosely connected to "plasma control." The LLM subsection (11.3) discusses XiHeFusion and LPI-LLM but does not address how LLMs could be integrated into control systems -- which would be the natural connection to the paper's theme. Consider either strengthening the connections to plasma control or condensing Section 11 into a brief outlook.

11. **[Appendix A.5] Classification table needs baseline column.** The 40-row verification table lists key metrics (AUC, speedup, success rate) but does not specify baseline comparators. A "baseline" column would enable meaningful cross-study comparison. For example, Seo et al.'s ">90% tearing mode avoidance" -- compared to what baseline rate? Gopakumar et al.'s "10^6x speedup" -- compared to which solver and at what accuracy loss?

12. **[Section 10.12] Future directions section lacks prioritization.** Six future directions are listed without prioritization or timeline estimates. Which are most critical? Which are most tractable in the near term? A prioritized roadmap with estimated timelines (e.g., "federated learning: 3-5 years to first cross-device demonstration") would increase the section's utility for program managers and funding agencies.

13. **[General] The paper does not discuss AI model governance for fusion.** As fusion devices become more complex and AI plays larger roles in control, questions of model versioning, change control, audit trails, and accountability become important. The paper touches on model update strategies (Section 3.8) but does not address the broader governance framework. This is a gap that Nuclear Fusion readers planning AI deployment would find relevant.

14. **[Section 10.6] Hardware deployment discussion is strong but lacks benchmarking references.** The computation cost table provides useful order-of-magnitude estimates, but the claim that "DRL training requires 8 NVIDIA A100 GPUs for approximately 72 hours" for Seo et al. should be verified -- this specific hardware configuration is not stated in the cited Nature paper. If this is an estimate, it should be labeled as such.

---

## Recommendation to Authors

**Decision: Minor Revision**

This V2 manuscript has addressed the majority of issues from the prior review round and represents a substantial analytical contribution to the AI for Fusion field. The remaining issues are focused and addressable in a single revision cycle. The following revisions are required:

**Mandatory revisions:**

1. **Include actual figures.** Convert the five text-based figure descriptions into high-quality figures. This is the single most impactful improvement available. At minimum: (a) a TRL radar chart (Figure 4), (b) a verification-level summary visualization (derived from Appendix A.5), (c) a research landscape overview (Figure 5), and (d) a method taxonomy diagram (Figure 1 or 2).

2. **Add a quantitative comparison table** for at least one sub-field where sufficient data exists. Disruption prediction is the strongest candidate: compile AUC, false positive rate, prediction horizon, and device for each published method into a normalized comparison table with baseline references.

3. **Eliminate structural redundancy.** Consolidate cross-device portability discussions (currently in Sections 3.5, 8.2, 10.4, 10.11) into a single dedicated subsection. Remove or condense textbook-level physics tutorials (NTM in 2.1, ELM in 4.5). Target a total length reduction of approximately 20% (to ~24,000 words).

4. **Standardize "foundation model" terminology.** Either replace all occurrences with "multi-modal pretrained framework" (as the critical assessment in Section 8.1 recommends) or add a consistent footnote qualification at every usage. The current inconsistency between the critical argument and the continued use of the term undermines intellectual credibility.

5. **Strengthen TRL assessment with explicit rubric.** Add a methodology subsection defining what specific evidence is required for each TRL level in the fusion AI context. Add columns to the TRL table showing: number of peer-reviewed supporting studies, number of devices validated, and highest validation level achieved.

**Recommended (non-mandatory) revisions:**

6. Add a brief "state of the field as of 2023" subsection (500 words) to establish the baseline from which 2024-2026 advances depart.

7. Strengthen the cross-domain comparison (Section 10.9) with at least one specific regulatory case study per domain.

8. Expand the failure mode catalog (Section 10.10) to include adversarial robustness, model degradation, and catastrophic forgetting.

9. Add a "prioritized roadmap" to the future directions section (10.12) with estimated timelines.

10. Verify all specific quantitative claims against cited sources (e.g., A100 GPU configuration for Seo et al. training, FPGA latency numbers).

The paper's core contributions -- the TRL framework, the verification-level analysis, the cross-domain comparison, and the honest assessment of the field's maturity -- are genuinely valuable and represent a meaningful advance over prior reviews in this space. With the mandatory revisions completed, this manuscript will be a strong contribution to Nuclear Fusion and an important reference for the AI for Fusion community.

---

*End of EIC Review Report*
