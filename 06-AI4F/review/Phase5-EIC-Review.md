# EIC Review Report: AI and ML for Magnetic Confinement Fusion Plasma Control (2024-2026)

**Paper Title:** Artificial Intelligence and Machine Learning for Magnetic Confinement Fusion Plasma Control: A Comprehensive Review (2024-2026)

**Reviewer Role:** Editor-in-Chief

**Date:** 2026-05-30

---

## Overall Assessment: Major Revision

The paper presents a broad and ambitious survey of AI/ML applications in magnetic confinement fusion plasma control covering the 2024-2026 window. While the scope is impressive and several analytical contributions (TRL assessment, cross-domain comparison, failure mode catalog) go beyond a standard literature survey, the manuscript suffers from significant structural, methodological, and evidentiary weaknesses that must be addressed before it is suitable for publication in a top-tier venue.

---

## Strengths

1. **Exceptional breadth of coverage.** The paper spans eight core dimensions (DRL control, disruption prediction, ELM suppression, equilibrium reconstruction, surrogate models, PINNs, foundation models, digital twins) plus six extension topics (stellarator optimization, HTS magnets, LLMs, ICF, data infrastructure, 5D gyrokinetic surrogates), covering 117 references across 13+ devices. This is among the most comprehensive surveys attempted in this specific sub-field.

2. **Novel analytical frameworks beyond literature survey.** The TRL assessment (Section 10.7), cross-domain safety comparison with aerospace/nuclear-fission/process-control (Section 10.9), failure mode catalog (Section 10.10), and the verification-level classification table (Appendix A.5) represent genuine intellectual contributions that provide actionable insights for the community, not merely a reorganization of existing abstracts.

3. **Honest and critical assessment of limitations.** The paper does not shy away from discussing the 78% preprint ratio, the gap between "foundation model" rhetoric and data reality (Section 8.1 critical assessment), PINNs convergence failures (Section 7.5), and sim-to-real transfer failures (Section 10.10). This intellectual honesty strengthens credibility.

4. **Practical engineering perspective.** The inclusion of hardware deployment trade-offs (GPU vs. FPGA vs. ASIC, Section 10.6), real-time OS considerations (VxWorks), functional safety standards (IEC 61508, DO-178C), and computation cost tables bridges the gap between ML research and fusion engineering practice -- a perspective often missing in ML-centric reviews.

5. **Well-structured bilingual presentation.** The dual Chinese-English abstract and consistent bilingual section headers make the paper accessible to both Chinese and international fusion communities, which is strategically valuable given the geographic distribution of major tokamak facilities.

---

## Weaknesses

1. **Heavy reliance on preprints undermines scholarly authority.** With 78% of references being arXiv preprints (91 out of 117), many core claims rest on work that has not undergone peer review. The paper acknowledges this but does not adequately address it: several sections present preprint findings with the same confidence as published journal results. For a review paper intended to guide the field, this is a significant epistemological problem. The paper needs a more systematic framework for distinguishing the confidence level assigned to peer-reviewed vs. preprint results.

2. **Lack of quantitative comparative analysis.** Despite the breadth of coverage, the paper rarely provides head-to-head quantitative comparisons of methods. The classification table in Appendix A.5 lists key metrics but does not normalize them across devices or tasks. There is no systematic meta-analysis of (for example) disruption prediction AUC scores across methods, or DRL reward convergence across algorithms. The reader is left with a collection of individual results rather than a synthesized understanding of which approaches work best under what conditions.

3. **Structural imbalance and redundancy.** Sections 2 (DRL) and 3 (disruption prediction) are heavily detailed, while Section 7 (PINNs) and parts of Section 9 (digital twins) are comparatively thin. The "NTM physics and DRL reward function design" subsection (2.1) reads more like a textbook introduction than a review analysis. Several points are repeated across sections (e.g., cross-device portability challenges appear in Sections 3.5, 8.2, 10.4, and 10.11 with overlapping content).

4. **Missing figures.** The paper contains five detailed figure descriptions (Figures 1-5) embedded as text, but no actual figures are included. For a review of this scope, visual summaries (taxonomy diagrams, timeline charts, TRL radar plots, method comparison scatter plots) are essential for reader comprehension. The current text-based figure descriptions are insufficient substitutes.

5. **Insufficient engagement with pre-2024 foundational context.** While the paper focuses on 2024-2026, many of the surveyed methods have roots in earlier work that is not adequately contextualized. The paper would benefit from a concise "state of the field as of 2023" section that establishes the baseline from which 2024-2026 advances depart, enabling readers to assess the actual incremental progress.

---

## Specific Issues

1. **[Section 1.2 / Appendix A.3] Literature search methodology lacks PRISMA-style rigor.** The paper describes keyword searches and snowball sampling but provides no quantitative flow diagram (records identified, screened, excluded with reasons, included). For a systematic review, this is a minimum requirement. The claim of "systematic" retrieval cannot be verified without such documentation.

2. **[Section 2.1] Over-representation of a single result.** The Seo et al. Nature 2024 paper receives approximately 1,500 words of dedicated analysis including physics background, reward function design, and experimental details. While this is a landmark result, the level of detail is disproportionate compared to other contributions of similar significance. This creates an impression of advocacy rather than balanced review.

3. **[Section 8.1] "Foundation model" terminology is contested but inconsistently applied.** The paper correctly critiques the use of "foundation model" in the fusion context and proposes "multi-modal pretrained framework" as more accurate. However, the paper itself continues to use "foundation model" throughout (in the abstract, section titles, conclusion) without consistent qualification. This undermines the critical argument.

4. **[Section 10.7] TRL assessment lacks explicit methodology.** The TRL ratings are presented as a table without showing the evidence basis for each rating. How was "TRL 4-5" for DRL control determined versus "TRL 2-3" for PINNs? What specific criteria were met or not met at each level? The assessment reads as subjective opinion rather than structured evaluation. A rubric mapping specific evidence items to TRL levels would substantially strengthen this contribution.

5. **[Section 10.9] Cross-domain comparison is superficial.** The comparison with aerospace, nuclear fission, and process control covers only one page each and relies on general statements rather than structured analysis. A more rigorous approach would map specific AI safety challenges in fusion to their analogues in other domains, with explicit discussion of which solutions transfer and which do not.

6. **[Section 10.10] Failure mode catalog is incomplete.** While the inclusion of negative results is commendable, the catalog covers only four failure modes (high false positive rate, sim-to-real transfer failure, device overfitting, PINN convergence). Missing are: adversarial robustness failures, data poisoning risks, model degradation over time in deployed systems, and catastrophic forgetting in continual learning scenarios. The section also lacks quantitative data on failure frequencies.

7. **[Section 11] Extension topics feel disconnected.** The six topics in Section 11 (stellarator optimization, HTS magnets, LLMs, ICF, data infrastructure, 5D gyrokinetics) are each given 1-2 pages of superficial coverage. The connection to the paper's core theme (plasma control) is weak for some topics (e.g., HTS magnet design, ICF). These topics would be better served as a brief outlook section rather than a full chapter that dilutes the paper's focus.

8. **[Section A.5] Classification table lacks standardized metrics.** The 43-row table uses heterogeneous metrics (AUC, accuracy, speedup factor, success rate) without normalization or cross-method comparison. A column indicating the baseline comparator for each metric would enable meaningful comparison. Additionally, several entries list "simulation" as the verification level without specifying the fidelity of the simulation model used.

9. **[References] Inconsistent reference quality.** Some references lack DOIs (e.g., [55], [60], [65], [72], [76], [78], [80], [81], [90], [95]). Reference [55] cites an entire conference rather than a specific paper. Several arXiv preprints have no DOI and some may not survive peer review. The reference list needs quality control and standardization.

10. **[Sections 2-12] Excessive length without clear reader guidance.** At approximately 30,000 words (including references), the paper is significantly longer than typical review articles in Nuclear Fusion (~15,000 words) or Reviews of Modern Physics (which allows longer reviews but demands commensurate depth). The paper would benefit from a structured "key takeaways" box at the start of each section and a condensed main text with detailed material moved to supplementary information.

11. **[Section 10.6] Real-time deployment discussion lacks specificity.** The computation cost table provides useful order-of-magnitude estimates but does not cite specific benchmarking studies. The claim of "sub-millisecond" FPGA inference needs supporting data. The discussion of RTOS integration (VxWorks) is based on general knowledge rather than specific reported implementations.

12. **[Section 4.2] Single conference abstract as primary evidence.** The ELM suppression breakthrough (Kim et al., APS-DPP 2024) is referenced only as a conference abstract [28]. For a claim of this significance ("cross-device ELM suppression"), the lack of a peer-reviewed publication at the time of writing should be explicitly acknowledged as a limitation, and the evidence level should be clearly distinguished from results published in archival journals.

---

## Recommendation to Authors

**Decision: Major Revision required before the paper can be considered for publication.**

The following revisions are mandatory:

1. **Add a PRISMA-style methodology section** with a literature flow diagram documenting the systematic search process, inclusion/exclusion criteria, and quantitative results of the screening process.

2. **Reduce preprint reliance or stratify evidence quality.** Implement a consistent system (e.g., color-coded or symbol-coded) throughout the paper to distinguish peer-reviewed results from preprint findings. Consider limiting the core analysis to peer-reviewed work and treating preprints as supplementary evidence.

3. **Include actual figures.** Convert the five text-based figure descriptions into high-quality figures. At minimum: (a) a taxonomy/timeline diagram, (b) a TRL radar chart, (c) a method comparison visualization, (d) a device coverage map, and (e) a research landscape bubble chart.

4. **Add quantitative comparative analysis.** For each major topic (disruption prediction, DRL control, surrogate models), provide a normalized comparison table with standardized metrics, baselines, and statistical significance where available.

5. **Strengthen the TRL assessment** by providing an explicit rubric and evidence mapping for each rating. Consider involving domain experts to validate the ratings through a Delphi-style process.

6. **Reduce length by 30-40%** by: (a) moving detailed textbook-level physics introductions (e.g., NTM mechanism in 2.1, ELM mechanism in 4.5) to an appendix or removing them; (b) consolidating repeated cross-device portability discussions into a single dedicated section; (c) condensing Section 11 extension topics into a brief outlook subsection.

7. **Add a "state of the field as of 2023" baseline section** to enable readers to assess the incremental progress made during 2024-2026.

8. **Standardize the reference list**: add DOIs where available, fix the generic conference citation [55], and add a note distinguishing peer-reviewed from non-peer-reviewed sources.

The paper's core strengths -- its breadth, its critical analytical frameworks, and its engineering-aware perspective -- are genuinely valuable to the fusion community. If the above issues are addressed, this could become an important reference work. However, in its current form, the heavy reliance on preprints, lack of quantitative synthesis, missing figures, and structural imbalances prevent it from meeting the standards of a top-tier journal.

---

*End of EIC Review Report*
