# R1 Methodology Review Report

**Reviewer:** R1 -- Methodology Expert
**Paper:** "Artificial Intelligence and Machine Learning for Magnetic Confinement Fusion Plasma Control: A Comprehensive Review (2024--2026)"
**Date:** 2026-05-30

---

## Overall Assessment: Major Revision

The paper presents an ambitious and timely review of AI/ML applications in magnetic confinement fusion plasma control. While the topical coverage is broad and the critical commentary on evidence quality is commendable, the methodology suffers from several significant deficiencies that undermine the claim of a "systematic" review. The most critical issues are: (1) the search strategy, though described, lacks key elements of reproducibility and transparency mandated by systematic review standards; (2) the screening process is inadequately documented; (3) the quantitative synthesis relies on a convenience sample of 40 studies without clear selection criteria; and (4) the statistical claims are imprecise and inconsistently reported. These issues must be addressed before the paper can be considered a rigorous systematic review.

---

## Dimension Scores

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Search Strategy | 55 | Keywords and databases listed (Section 1.2, Appendix A.3); search execution table provided (A.4.1). However, no PRISMA flow diagram, no date-stamped search records, no Boolean operator specification for all databases, and the search table shows implausibly precise filtering counts without documenting the screening process. |
| Inclusion/Exclusion Criteria | 62 | Criteria I1-I5 and E1-E7 are explicitly listed (A.3.1) and are generally sensible. However, criteria lack operational definitions (e.g., "highly overlapping" in E3 is subjective), the 15-paper exception for 2022-2023 works is arbitrary and undocumented, and no inter-rater reliability is reported for screening decisions. |
| Statistical Reporting | 48 | Several numerical claims lack proper sourcing or are imprecise. The "78% preprints" claim and "30% experimentally validated" claim are presented without confidence intervals or formal meta-analytic treatment. Percentages in the abstract (78%, 30%, 67%) are stated as exact figures without acknowledging rounding or calculation methodology. Some statistics (e.g., "50% success rate, 117% improvement" in Section 2.3) are reported without baseline definitions. |
| Reproducibility | 45 | The search strategy is partially reproducible (databases, keywords, dates listed), but critical details are missing: no PRISMA registration, no screening protocol published a priori, no full list of excluded studies with exclusion reasons, no inter-rater agreement metrics, and the 40-study verification analysis lacks selection methodology. Another researcher could not fully reproduce this review. |
| Evidence Quality | 70 | The paper explicitly acknowledges the 78% preprint rate and the concentration of experimental validation on DIII-D. The TRL framework provides a structured quality assessment. The verification-level classification table (Section A.5) distinguishes simulation, simulation+experimental, and experimental validation. However, no formal risk-of-bias assessment is conducted, and the TRL assignments lack detailed justification methodology. |
| Quantitative Synthesis | 52 | The paper provides useful summary tables (A.5 classification table, TRL table, computational cost table in 10.6) but these constitute a narrative-quantitative hybrid rather than a formal quantitative synthesis. No forest plots, no effect size comparisons, no formal meta-analysis of performance metrics across studies. The claim of "AUC improved by ~5%" (Section 3.2) is stated without specifying baseline or statistical significance. |

---

## Strengths

- **Transparent evidence quality reporting.** The paper proactively discloses that 78% of citations are preprints and that experimental validation is heavily concentrated on DIII-D. This level of methodological self-awareness is unusual and commendable for a review in this rapidly evolving field.

- **Structured verification-level classification.** The 40-study classification table (Section A.5) explicitly distinguishes between simulation-only, simulation+experimental, and full experimental validation, providing readers with a clear framework for evaluating evidence maturity. This tripartite classification is more informative than a simple binary peer-reviewed/not-peer-reviewed distinction.

- **Technology Readiness Level (TRL) framework.** The adoption of the NASA TRL framework (Section 10.7) for assessing maturity across eight sub-domains provides a standardized, domain-agnostic language for communicating the state of the field. The TRL assessments are generally reasonable and appropriately conservative.

- **Explicit inclusion/exclusion criteria.** The paper lists seven inclusion and seven exclusion criteria (A.3.1), which is more than many narrative reviews provide. The criteria cover content relevance, time window, venue, methodological completeness, and language.

- **Honest treatment of negative results and failure modes.** Section 10.10 systematically documents failure patterns (high false-positive rates in disruption prediction, sim-to-real transfer failures, overfitting to specific devices, PINN convergence difficulties). This is a valuable contribution to the field's methodological maturity.

---

## Weaknesses

- **No PRISMA compliance or equivalent reporting standard.** The paper claims to be a "systematic review" but does not reference or follow PRISMA 2020 guidelines, PRISMA-ScR (for scoping reviews), or any other recognized systematic review reporting standard. No PRISMA flow diagram is provided. The screening process described in A.4.1 ("title/abstract screening then full-text screening") is mentioned but not documented with the number of studies excluded at each stage with reasons.

- **Undocumented 40-study selection for verification analysis.** The central quantitative claim -- that "only 30% of 40 key studies have been experimentally validated" -- rests on a convenience sample whose selection methodology is never described. Why 40 studies? How were they chosen from the 117 included papers? Was there a systematic ranking criterion? Without this, the verification-level analysis cannot be independently reproduced or validated.

- **Imprecise and inconsistently reported statistics.** Several numerical claims lack precision: (a) the abstract states "AUC improved by about 5%" without specifying the baseline AUC, the dataset, or the statistical test; (b) "50% success rate, 117% improvement" (Section 2.3) lacks a clearly defined baseline and denominator; (c) the search execution table (A.4.1) reports exact screening counts (e.g., 342 to 298 to 18 for Web of Science) without explaining how 280 records were screened or what criteria drove each exclusion, making the funnel implausibly precise.

- **No inter-rater reliability for screening or classification.** A single reviewer appears to have conducted all screening, classification, and TRL assessment decisions. Systematic review standards require at minimum dual independent screening with reported inter-rater agreement (e.g., Cohen's kappa). The TRL assignments (Section 10.7) and verification-level classifications (A.5) are subjective assessments that would particularly benefit from multi-reviewer consensus.

- **Absence of formal meta-analytic synthesis.** While the field may not lend itself to full meta-analysis given heterogeneity, the paper could at minimum report standardized performance metrics (e.g., AUC ranges, false-positive rates with confidence intervals) grouped by method category. The computational cost table (10.6) provides indicative ranges but without source attribution for each row. The paper instead relies entirely on narrative synthesis, missing an opportunity for quantitative comparison across studies that report compatible metrics.

---

## Specific Issues

**1. Missing PRISMA flow diagram (Appendix A.4.1).** The search execution table reports 1,758 records identified and 117 included, but does not provide the number excluded at each screening stage (title/abstract screening, full-text screening) with exclusion reasons. The note "1,451 records screened by title/abstract (excluding E1-E3), then full-text screened (excluding E4-E7)" is insufficient. A PRISMA 2020 flow diagram with exact counts at each stage is required for a systematic review.

**2. Search date inconsistency (Appendix A.4.1).** The search execution table shows different search dates for different databases: Web of Science and Scopus on 2026-05-15, arXiv on 2026-05-20, and conference proceedings on 2026-05-22. While this is not inherently problematic, the paper does not explain the rationale for the staggered search dates or whether a final update search was conducted to capture papers published between the earliest and latest search dates.

**3. Boolean logic not fully specified (Appendix A.3).** The search strategy describes keyword combinations but does not provide the exact Boolean queries used for each database. The Web of Science query shown in A.4.1 uses AND/OR but does not include field tags (e.g., TS=, TI=) or database-specific syntax. The arXiv search uses only "plasma" OR "tokamak" OR "fusion" without AI/ML terms, which would retrieve a very broad set of non-AI plasma physics papers.

**4. Arbitrary 15-paper exception (A.3.1, criterion I2).** The inclusion criteria state that "some 2022-2023 foundational works" are included as background context, "not exceeding 15 papers." This cap is arbitrary and undocumented. How were these ~15 papers selected? What qualifies as "foundational"? This exception introduces unmeasurable selection bias.

**5. Undefined "highly overlapping" exclusion (A.3.1, criterion E3).** Exclusion criterion E3 states that "repeated publications or literature with highly overlapping content" will be excluded, retaining "the most complete version." The term "highly overlapping" is not operationally defined (e.g., by text similarity threshold or shared author analysis), making this criterion subjective and non-reproducible.

**6. Verification table selection methodology missing (Section A.5).** The paper states the classification table covers "40 key studies" but never explains how these 40 were selected from the 117 included papers. Were they selected to represent all eight sub-domains? Were they the most-cited? The most methodologically significant? This selection must be justified and ideally conducted by a systematic ranking procedure.

**7. TRL assessment methodology (Section 10.7).** The TRL assignments (e.g., "DRL plasma control: TRL 4-5") are presented as single-point estimates without detailed justification criteria for each assignment. The paper describes the TRL scale but does not provide a scoring rubric or checklist that would enable another assessor to independently arrive at the same TRL rating. Was each TRL assessed by a single reviewer or by consensus?

**8. "AUC improved by ~5%" claim (Section 3.2).** The claim that Spangher et al.'s Transformer model improved AUC "by approximately 5%" over existing methods lacks critical context: (a) which baseline methods were compared? (b) on which datasets? (c) was this difference statistically significant? (d) was the comparison conducted on held-out test data? A 5% AUC improvement could be meaningful or trivial depending on the baseline and dataset.

**9. Computational cost table lacks source attribution (Section 10.6).** The table reporting typical training costs (e.g., "8 GPU x 72 hours" for DRL control) does not attribute each row to a specific source. Only the DRL row references Seo et al. The remaining rows appear to be the authors' estimates without documented methodology.

**10. Statistical claims in abstract vs. body inconsistency.** The abstract states "78% of cited works are preprints" while Section A.4 reports "preprints 91 (78%)" out of 117 references. The math checks out (91/117 = 77.8%, rounded to 78%), but the paper should explicitly state the rounding convention used throughout.

**11. Missing sensitivity analysis.** The paper does not discuss how results might change if the search were extended to additional databases (e.g., IEEE Xplore, INSPEC), additional keywords (e.g., "neural operator," "PINN," "surrogate model" are used in the text but not listed as search terms in A.3), or a broader time window.

**12. No protocol registration.** The review was not prospectively registered on PROSPERO, OSF, or any other systematic review protocol registry. While not strictly required for all reviews, registration would strengthen the claim of systematic methodology and protect against post-hoc analytical choices.

---

## Recommendation to Authors

**Major revision is required.** The paper's topical contribution is valuable and the critical perspective on evidence quality is a genuine strength. However, to credibly claim "systematic review" status, the following revisions are mandatory:

1. **Add a PRISMA 2020 flow diagram** with exact counts at each screening stage and documented exclusion reasons. If the review is better characterized as a scoping review, adopt PRISMA-ScR instead and reframe the claims accordingly.

2. **Document the 40-study selection methodology.** Either (a) provide explicit, reproducible selection criteria for the verification-level analysis, or (b) expand the analysis to all 117 included papers with a clear classification rubric.

3. **Conduct dual independent screening** for at least a random subset of records, and report inter-rater agreement (Cohen's kappa). At minimum, have a second reviewer independently classify the 40 key studies by verification level and TRL.

4. **Standardize statistical reporting.** For every quantitative claim (AUC, false-positive rate, computational speedup), report: the specific study, the dataset, the baseline comparator, the metric with confidence interval or error bar, and the statistical significance test if applicable.

5. **Provide a detailed TRL scoring rubric** with explicit criteria for each TRL level, enabling independent reproducibility of the TRL assignments.

6. **Register the review protocol** retrospectively on OSF and provide the registration link, or explicitly reframe the paper as a narrative/scope review rather than a systematic review.

7. **Add a limitations section** that explicitly addresses the risks introduced by the 78% preprint rate, the single-reviewer screening process, and the potential for publication bias in a field where negative results are rarely reported.

The paper is publishable after these revisions, as the underlying content and critical analysis are strong. The methodology simply needs to be brought up to the standard claimed by the paper's own framing as a "systematic review."
