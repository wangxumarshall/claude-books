# Editorial Decision Letter

**Paper:** Artificial Intelligence and Machine Learning for Magnetic Confinement Fusion Plasma Control: A Comprehensive Review (2024-2026)

**Decision: MAJOR REVISION**

**Date:** 2026-05-30

---

## 1. Decision Rationale

The paper presents a comprehensive and ambitious survey of AI/ML applications in magnetic confinement fusion plasma control, covering 8 core dimensions and 6 extension topics across 117 references. The breadth of coverage, the TRL assessment framework, the failure mode catalog, and the cross-domain safety comparison represent genuine intellectual contributions to the field.

However, the panel has identified significant issues that prevent acceptance in its current form:

1. **Devil's Advocate CRITICAL findings**: Three critical issues were identified — over-claiming based on preprint evidence, DIII-D experimental centralization masking as "field maturity," and narrative framing that conflates laboratory demonstrations with deployable solutions. Per editorial policy, CRITICAL findings from the Devil's Advocate preclude an Accept decision.

2. **Methodology gaps (R1: Major Revision)**: The methodology documentation has significant gaps — missing PRISMA flow diagram, inconsistent key studies counts (33 vs 43 vs 40), and no documented search execution protocol. These gaps prevent reproducibility.

3. **Consensus issues**: Four or more reviewers identified issues with preprint reliance, missing figures, and TRL methodology. These are not individually fatal but collectively represent substantial revision work.

The paper's core strengths — its breadth, its critical analytical frameworks, and its engineering-aware perspective — are genuinely valuable. If the issues identified below are addressed, this could become an important reference work for the fusion community.

---

## 2. Review Panel Summary

| Reviewer | Recommendation | Key Concern |
|----------|---------------|-------------|
| EIC | Minor Revision | Preprint reliance, missing figures, structural imbalance |
| R1 (Methodology) | Major Revision | Missing PRISMA, inconsistent counts, no search log |
| R2 (Domain) | Minor Revision | Physics accuracy issues, missing references, uneven depth |
| R3 (Perspective) | Minor Revision | Weak cross-domain analysis, missing safety framework |
| Devil's Advocate | REVISE | 3 CRITICAL + 7 MAJOR issues |

---

## 3. Consensus Issues

### [CONSENSUS-4] Issues (All 4 non-DA reviewers agree)

**C1. Missing PRISMA-style methodology documentation**
- EIC: "Add a PRISMA-style methodology section with a literature flow diagram"
- R1: "No PRISMA Flow Diagram or Equivalent" (Severity: High)
- R2: "Literature Coverage" weakness — lack of documented screening
- R3: Noted methodology gaps
- **Action Required**: Add PRISMA-style flow diagram and document search protocol

**C2. Heavy reliance on preprints (78%)**
- EIC: "Heavy reliance on preprints undermines scholarly authority"
- R1: Preprint handling noted as concern
- R2: "Physics Accuracy" conditional — preprint claims presented with same confidence as peer-reviewed
- R3: "Broader Implications" weakness — preprint-heavy evidence base
- DA: CRITICAL — "Over-claiming based on preprint evidence"
- **Action Required**: Implement systematic evidence quality stratification throughout the paper

**C3. Missing figures**
- EIC: "Missing figures" — 5 text descriptions but no actual figures
- R3: Noted as weakness for practical impact
- **Action Required**: Convert text-based figure descriptions into actual figures

### [CONSENSUS-3] Issues (3 reviewers agree)

**C4. Inconsistent key studies table count (33 vs 43 vs 40)**
- R1: "Key Studies Table Count Inconsistency" (Severity: Medium)
- R1 verified: actual count is 40 entries
- EIC: Noted in classification table discussion
- R2: Noted in literature coverage
- **Action Required**: Standardize to 40 throughout the paper

**C5. Missing inclusion/exclusion criteria**
- R1: "Missing Inclusion/Exclusion Criteria" (Severity: High)
- EIC: "Literature search methodology lacks PRISMA-style rigor"
- R2: Noted as weakness
- **Action Required**: Add I/E criteria to the paper's appendix

**C6. TRL assessment lacks explicit methodology**
- EIC: "TRL assessment lacks explicit methodology"
- R1: TRL discrepancies with Methodology Blueprint
- R2: "Add explicit TRL methodology"
- **Action Required**: Provide rubric mapping evidence to TRL levels

**C7. DIII-D experimental centralization**
- R2: "40 key studies, only 12 (30%) experimental, 8 from DIII-D"
- DA: CRITICAL — "DIII-D centralization masking as field maturity"
- R3: Noted geographic concentration
- **Action Required**: Explicitly acknowledge DIII-D concentration and discuss portability implications

---

## 4. Devil's Advocate CRITICAL Issues

Per editorial policy, CRITICAL findings from the Devil's Advocate must be addressed. The following 3 CRITICAL issues were identified:

### DA-C1: Over-claiming based on preprint evidence
**The Problem**: The paper presents 78% preprint-sourced findings with the same confidence as peer-reviewed results. Core claims about "foundation models," digital twin maturity, and PINN applicability rest on work that has not survived peer review.

**Required Response**: Implement a systematic evidence quality framework. Options:
- (a) Color-code or symbol-code throughout the paper to distinguish peer-reviewed from preprint results
- (b) Add confidence qualifiers to preprint-sourced claims
- (c) Restructure so core analysis focuses on peer-reviewed work, with preprints as supplementary

### DA-C2: DIII-D experimental centralization
**The Problem**: Of 40 key studies, only 12 have experimental validation, and 8 of those 12 are from DIII-D. This means the "field maturity" narrative is largely a DIII-D story, not a field-wide story. Cross-device portability of AI methods remains undemonstrated at scale.

**Required Response**: 
- Add explicit discussion of DIII-D concentration in the verification level analysis
- Qualify claims about "field maturity" with the device-concentration caveat
- Discuss what would be needed to demonstrate portability (shared benchmarks, cross-device transfer protocols)

### DA-C3: Narrative framing conflates demos with deployment
**The Problem**: The paper's narrative arc — from DRL control to foundation models to digital twins — implies a progression toward deployable systems. In reality, most results are proof-of-concept demonstrations. The gap between "demonstrated in simulation" and "deployable in ITER/DEMO" is not adequately discussed.

**Required Response**:
- Add a "Deployment Readiness" discussion that honestly assesses the gap between current demonstrations and ITER/DEMO deployment requirements
- Revise the conclusion to distinguish between "research progress" and "deployment readiness"
- Consider adding a roadmap figure showing the path from current TRL to deployment

---

## 5. Revision Roadmap

### Priority 1: Must Fix (Blocks Acceptance)

| # | Issue | Source | Action |
|---|-------|--------|--------|
| R1 | Add PRISMA-style methodology section | EIC, R1, R2 | Add flow diagram documenting search process, screening, and inclusion |
| R2 | Implement evidence quality stratification | EIC, DA-C1 | Add systematic framework distinguishing peer-reviewed from preprint results throughout |
| R3 | Resolve key studies count inconsistency | R1 | Standardize to 40 in all locations (Section 1.3, Appendix A.5) |
| R4 | Add inclusion/exclusion criteria | R1, EIC | Add I1-I5, E1-E7 criteria to Appendix A |
| R5 | Address DIII-D centralization | DA-C2, R2 | Add explicit discussion of device concentration in verification analysis |
| R6 | Add deployment readiness discussion | DA-C3 | Add section assessing gap between demonstrations and ITER/DEMO deployment |
| R7 | Commit to "pre-trained framework" terminology | EIC, R2 | If Section 8.1 critiques "foundation model," use "pre-trained framework" consistently |

### Priority 2: Should Fix (Strongly Recommended)

| # | Issue | Source | Action |
|---|-------|--------|--------|
| R8 | Include actual figures | EIC, R3 | Convert 5 text descriptions to high-quality figures |
| R9 | Add TRL rubric | EIC, R1, R2 | Provide explicit evidence-to-TRL mapping |
| R10 | Deepen cross-domain comparison | R3 | Map specific AI safety challenges to analogues in aerospace/nuclear/process-control |
| R11 | Expand failure mode catalog | EIC, R2 | Add adversarial robustness, data poisoning, model degradation |
| R12 | Fix physics accuracy issues | R2 | Correct Seo et al. reward description, ELM suppression characterization |
| R13 | Add missing foundational references | R2 | Cite Kates-Harbeck et al. (2019), Rea et al. (2019) as background |
| R14 | Add search execution log | R1 | Populate database, date, query, result counts |

### Priority 3: Nice to Have

| # | Issue | Source | Action |
|---|-------|--------|--------|
| R15 | Deepen PINNs section | R2 | Add multi-scale challenges discussion |
| R16 | Expand stellarator/ICF coverage | R2 | Both topics have substantial recent AI activity |
| R17 | Add "why methods work" framework | R2 | Connect plasma physics constraints to AI architecture choices |
| R18 | Reduce length by 30-40% | EIC | Move textbook-level physics to appendix, consolidate repeated discussions |
| R19 | Add data availability statement | R1 | Offer to share search results as supplementary material |
| R20 | Add author information and COI | R1 | Complete placeholder fields, add conflict of interest statement |

---

## 6. Suggested Revision Strategy

The revision should focus on three interconnected themes:

**Theme 1: Methodology Rigor** (R1, R3, R4, R14)
- Add PRISMA flow diagram
- Add inclusion/exclusion criteria
- Add search execution log
- Fix count inconsistencies

**Theme 2: Evidence Quality** (R2, R5, R6, R7)
- Implement evidence quality stratification framework
- Address DIII-D centralization explicitly
- Add deployment readiness discussion
- Commit to consistent terminology

**Theme 3: Presentation** (R8, R9, R10, R11, R12, R13)
- Include actual figures
- Add TRL rubric
- Deepen cross-domain and failure mode analysis
- Fix physics accuracy and add missing references

The author should address all Priority 1 items before resubmission. Priority 2 items are strongly recommended. Priority 3 items are optional but would strengthen the paper.

---

## 7. Timeline

Please submit the revised manuscript within **8 weeks** of receiving this decision letter. Include a detailed response to reviewer comments addressing each point in the Revision Roadmap.

---

*Editorial Decision synthesized from 5 review reports (EIC, R1 Methodology, R2 Domain, R3 Perspective, Devil's Advocate).*

*Companion documents: Review-EIC.md, Review-R1-Methodology.md, Review-R2-Domain.md, Review-R3-Perspective.md, Review-Devils-Advocate.md*
