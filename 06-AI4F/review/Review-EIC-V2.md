# Editor-in-Chief Review Report (V2)

**Paper:** Artificial Intelligence and Machine Learning for Magnetic Confinement Fusion Plasma Control: A Comprehensive Review (2024–2026)

**Reviewer:** Editor-in-Chief — Prof. of Computational Physics, AI for Physical Sciences
**Specialization:** AI/ML applications in physics and engineering, editorial experience in high-impact computational journals
**Date:** 2026-05-30

---

## Overall Assessment: Minor Revision

This is an ambitious and comprehensive survey of AI/ML applications in magnetic confinement fusion plasma control covering the 2024–2026 window. The paper demonstrates significant improvements over its previous version: the addition of an evidence quality framework, explicit TRL rubric, deployment readiness assessment, expanded failure mode catalog, and Mermaid-based figures. The breadth of coverage across 8 core dimensions and 6 extension topics, spanning 121 references and 13+ devices, is commendable. The critical self-assessment of the "foundation model" terminology and the honest acknowledgment of 79% preprint reliance are notable scholarly contributions. Several issues remain, but the paper is close to submission-ready.

---

## Dimension Scores

| Dimension | Score (0-100) | Notes |
|-----------|---------------|-------|
| Originality & Significance | 85 | TRL framework and deployment readiness assessment are genuine contributions |
| Technical Quality | 78 | Generally strong but uneven across sections |
| Presentation & Clarity | 75 | Good structure but some redundancy; Mermaid figures are effective |
| Literature Coverage | 82 | Broad but some key gaps remain |
| Rigor & Reproducibility | 72 | Evidence framework is good; methodology still has gaps |
| Relevance to Readership | 88 | Highly relevant to both fusion and AI communities |

**Weighted Score: 80/100**

---

## Detailed Review

### 1. Originality & Significance (Score: 85)

**Strengths:**
- The TRL assessment (Section 10.7) with explicit rubric and evidence mapping is a genuine intellectual contribution — no prior review has systematically assessed maturity of AI-for-fusion technologies
- The deployment readiness assessment (Section 10.11) honestly distinguishes "research progress" from "deployment readiness," which is rare and valuable in review papers
- The failure mode catalog (Section 10.10) now covers 7 failure modes (up from 4 in the previous version), including adversarial robustness, data poisoning, and catastrophic forgetting
- The critical assessment of "foundation model" terminology (Section 8.1) is well-argued and consistent throughout the paper
- The evidence quality framework (Level A-D) with explicit reading guide is a practical contribution

**Weaknesses:**
- The cross-domain comparison (Section 10.9) remains somewhat superficial — one paragraph per domain is insufficient for meaningful analysis
- The "why methods work" framework suggested by R2 is still absent — the paper describes what works but not systematically why

### 2. Technical Quality (Score: 78)

**Strengths:**
- Sections 2 (DRL) and 3 (disruption prediction) have excellent technical depth
- The multi-objective reward function description for Seo et al. (Section 2.1) is now correctly described
- The new PINN section (7.6) adds valuable depth with three 2025 papers
- The Mermaid figures are well-designed and technically informative

**Weaknesses:**
- Section 7 (PINNs) overall is still thin for a topic with substantial literature — Section 7.6 helps but the core sections 7.1-7.5 remain brief
- Section 9 (digital twins) reads more as a conceptual overview than a technical review
- The surrogate model section (Section 6) covers FNO well but lacks depth on DeepONet and graph neural operators

### 3. Presentation & Clarity (Score: 75)

**Strengths:**
- The bilingual abstract (Chinese + English) is well-written and informative
- The paper structure (8 dimensions + 6 extensions) is logical and easy to navigate
- The Mermaid diagrams are effective — particularly Figure 1 (DRL architecture) and Figure 4 (TRL chart)
- Evidence quality labels throughout the text help readers assess claim maturity

**Weaknesses:**
- Some redundancy exists between sections (e.g., DIII-D centralization is discussed in multiple places)
- The conclusion is long (13 points) — could be consolidated
- Figure 2 (timeline) is informative but the Mermaid timeline syntax limits visual clarity
- The paper could benefit from a summary table at the beginning listing all 8 dimensions with key findings

### 4. Literature Coverage (Score: 82)

**Strengths:**
- 121 references covering 13+ devices is commendable
- The inclusion of non-Western facilities (ADITYA, EXL-50U, HL-3) reduces geographic bias
- Conference proceedings from APS-DPP, IAEA FEC, SOFE, EPS, and TOFE are systematically searched
- The new references [118]-[121] strengthen the PINN and spherical tokamak sections

**Weaknesses:**
- Stellarator optimization section (11.1) could be deeper given the recent surge in AI-for-stellarator work
- ICF section (11.4) remains thin — only 4 references for a topic with substantial AI activity
- No coverage of reversed field pinch (RFP) AI work
- Missing foundational references: Kates-Harbeck et al. (2019) and Rea et al. (2019) should be cited as background context

### 5. Rigor & Reproducibility (Score: 72)

**Strengths:**
- The evidence quality framework (Level A-D) is well-defined
- The TRL rubric with explicit evidence mapping is now provided
- Inclusion/exclusion criteria are documented (Section A.3.1)
- Search execution methodology is described (Section A.3)

**Weaknesses:**
- No PRISMA flow diagram — the methodology section describes the process but lacks a visual flow diagram
- The search execution log (Section A.4) lacks specific dates and database-specific result counts
- The key studies table (44 entries) is valuable but the selection criteria for "key studies" vs. other references is not explicit

### 6. Relevance to Readership (Score: 88)

**Strengths:**
- The paper is highly relevant to both the fusion community (practical AI applications) and the AI community (real-world safety-critical applications)
- The deployment readiness assessment and cross-domain comparison provide actionable insights
- The failure mode catalog is valuable for researchers entering the field
- The TRL assessment helps funding agencies and program managers prioritize investments

---

## Specific Recommendations

### Must Fix (Priority 1)

1. **Add PRISMA flow diagram**: The methodology section (A.3-A.4) describes the search process but lacks a visual PRISMA-style flow diagram showing the number of records identified, screened, excluded, and included. This is a standard requirement for systematic reviews.

2. **Add missing foundational references**: Cite Kates-Harbeck et al. (2019, Nature 568) and Rea et al. (2019, PPCF 61) as background context for disruption prediction. These are foundational papers that established the CNN/LSTM approach many 2024-2026 papers build upon.

### Should Fix (Priority 2)

3. **Deepen the cross-domain comparison** (Section 10.9): Map specific AI safety challenges in fusion to their analogues in other domains. Currently one paragraph per domain — consider adding a comparison table.

4. **Add a summary table**: At the beginning of the paper (after the abstract), add a table summarizing all 8 dimensions with key findings, TRL levels, and representative references.

5. **Strengthen ICF section** (Section 11.4): The section has only 4 references. Consider adding more ICF AI work or explicitly marking this as "brief overview."

6. **Consolidate conclusion**: The 13-point conclusion is long. Consider grouping into 3-4 themes (control, prediction, infrastructure, outlook).

### Nice to Have (Priority 3)

7. **Add "why methods work" framework**: Systematically connect plasma physics constraints to AI architecture choices (e.g., why Transformers outperform LSTMs for disruption prediction).

8. **Add search execution log details**: Include specific dates, database-specific result counts, and number of records at each screening stage.

9. **Consider adding a glossary**: The paper uses many acronyms (DRL, PINN, FNO, TRL, etc.) — a glossary would help non-specialist readers.

---

## Summary

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Originality & Significance | Pass (85) | TRL framework and deployment assessment are genuine contributions |
| Technical Quality | Conditional (78) | Strong in DRL/disruption, thin in PINNs/digital twins |
| Presentation & Clarity | Conditional (75) | Good structure, some redundancy |
| Literature Coverage | Pass (82) | Broad but some gaps |
| Rigor & Reproducibility | Conditional (72) | Evidence framework good; PRISMA diagram missing |
| Relevance to Readership | Pass (88) | Highly relevant to both communities |

**Overall: Minor Revision** — The paper has significantly improved since the previous version. The evidence quality framework, TRL rubric, deployment readiness assessment, and Mermaid figures all address prior concerns. The remaining issues (PRISMA diagram, missing foundational references, cross-domain depth) are addressable. The paper's core strengths — its breadth, critical analytical frameworks, and engineering-aware perspective — make it a valuable contribution to the field.

---

*Report generated as part of Stage 3 peer review panel (V2).*
