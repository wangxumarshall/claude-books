# Methodology Reviewer Report (R1, V2)

**Paper:** Artificial Intelligence and Machine Learning for Magnetic Confinement Fusion Plasma Control: A Comprehensive Review (2024–2026)

**Reviewer:** Peer Reviewer 1 — Methodology Expert
**Specialization:** Systematic review methodology, ML validation frameworks, research design
**Date:** 2026-05-30

---

## Overall Assessment: Minor Revision

The paper presents a comprehensive survey with significant methodological improvements over its previous version. The addition of an evidence quality framework (Level A-D), inclusion/exclusion criteria, TRL rubric with evidence mapping, and deployment readiness assessment addresses many of the prior methodological concerns. The key studies count is now consistently 44 throughout. However, the absence of a PRISMA flow diagram and incomplete search execution log remain gaps that should be addressed.

---

## Dimension Scores

| Dimension | Score (0-100) | Notes |
|-----------|---------------|-------|
| Research Design | 78 | Good taxonomy but PRISMA diagram missing |
| Data Collection | 75 | Search strategy described but log incomplete |
| Analysis Framework | 82 | Evidence quality framework is a strength |
| Reproducibility | 70 | I/E criteria present; search log lacks detail |
| Statistical Validity | 80 | TRL assessment well-calibrated |
| Transparency | 72 | Preprint labeling is good; some methodological choices undocumented |

**Weighted Score: 76/100**

---

## Detailed Review

### 1. Research Design (Score: 78)

**Strengths:**
- The 8-dimension taxonomy is well-chosen and covers major research threads
- The inclusion/exclusion criteria (Section A.3.1, I1-I5, E1-E7) are now documented
- The evidence quality framework (Level A-D) provides a systematic way to assess claim maturity
- The TRL rubric with explicit evidence mapping is a genuine methodological contribution

**Weaknesses:**
- **No PRISMA flow diagram**: The methodology section describes the search process but lacks a visual flow diagram showing records identified, screened, excluded, and included. This is a standard requirement for systematic reviews and was identified as a Priority 1 issue in the previous review round.
- The paper does not specify who conducted the screening (single reviewer vs. dual screening) — this affects reproducibility

### 2. Data Collection (Score: 75)

**Strengths:**
- The search strategy covers 5 journals and 5 conferences — appropriate scope
- The keyword list is comprehensive (Section 1.2)
- Citation tracking and snowball searching are documented (Section A.3)
- The inclusion of arXiv preprints is explicitly acknowledged and justified

**Weaknesses:**
- **Search execution log incomplete**: Section A.4 mentions database counts but lacks specific dates, database-specific result counts, and number of records at each screening stage
- No documentation of how conference abstracts were screened (E4 criterion says "unless the only evidence" but no process for determining this)
- The search period (2024-2026) is clear but the cutoff date within 2026 is not specified

### 3. Analysis Framework (Score: 82)

**Strengths:**
- The evidence quality framework (Level A-D) is well-defined with clear criteria
- The reading guide explicitly warns about preprint limitations
- The TRL assessment provides a maturity-based perspective
- The verification level classification (仿真验证/仿真+实验/实验验证) is informative

**Weaknesses:**
- The selection criteria for "key studies" (44 entries) vs. other references is not explicit — what makes a study "key"?
- The evidence quality percentages are reported but not validated (e.g., no inter-rater reliability for classification)

### 4. Reproducibility (Score: 70)

**Strengths:**
- Inclusion/exclusion criteria are documented
- The TRL rubric is explicit and could be applied by other reviewers
- The search strategy is described in sufficient detail to replicate

**Weaknesses:**
- No PRISMA flow diagram — critical for reproducibility
- Search execution log lacks specificity
- No documentation of data extraction process (how were key findings extracted from each paper?)
- The paper does not specify the software/tools used for literature management

### 5. Statistical Validity (Score: 80)

**Strengths:**
- The TRL assessment is well-calibrated with explicit rubric
- The verification level analysis (27% experimental, 67% from DIII-D) is informative
- The evidence quality percentages sum correctly (17% + 2% + 79% + 2% = 100%)
- The key studies count (44) is consistent throughout the paper

**Weaknesses:**
- No confidence intervals or uncertainty estimates for the evidence quality percentages
- The TRL ratings are somewhat subjective — different reviewers might assign different ratings

### 6. Transparency (Score: 72)

**Strengths:**
- Preprint labeling is consistent throughout the paper
- The evidence quality reading guide is prominently placed
- The DIII-D centralization is honestly acknowledged

**Weaknesses:**
- Some methodological choices are undocumented (e.g., how were Mermaid diagram types selected?)
- The author information fields are still placeholders — this affects transparency
- No conflict of interest statement

---

## Specific Recommendations

### Must Fix (Priority 1)

1. **Add PRISMA flow diagram**: Create a visual flow diagram showing:
   - Records identified from each database
   - Records after duplicate removal
   - Records screened (title/abstract)
   - Records excluded with reasons
   - Full-text articles assessed
   - Articles included in final review

### Should Fix (Priority 2)

2. **Complete search execution log**: Add specific information to Section A.4:
   - Database search dates
   - Number of results per database
   - Number of records at each screening stage
   - Software used for literature management

3. **Document key study selection criteria**: Explain what distinguishes a "key study" (44 entries) from other references (77 entries).

4. **Add data extraction documentation**: Describe how key findings were extracted from each paper.

### Nice to Have (Priority 3)

5. **Add inter-rater reliability**: If possible, document how evidence quality classifications were validated.

6. **Specify search cutoff date**: The paper covers 2024-2026 but the exact cutoff date is not specified.

---

## Summary

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Research Design | Conditional (78) | Good taxonomy, PRISMA diagram missing |
| Data Collection | Conditional (75) | Search strategy good, log incomplete |
| Analysis Framework | Pass (82) | Evidence quality framework is a strength |
| Reproducibility | Conditional (70) | I/E criteria present, search log lacks detail |
| Statistical Validity | Pass (80) | TRL assessment well-calibrated |
| Transparency | Conditional (72) | Preprint labeling good, some gaps |

**Overall: Minor Revision** — The paper has made significant methodological improvements. The evidence quality framework, TRL rubric, and inclusion/exclusion criteria address prior concerns. The remaining gap (PRISMA diagram) is addressable and does not prevent publication if the paper is otherwise ready.

---

*Report generated as part of Stage 3 peer review panel (V2).*
