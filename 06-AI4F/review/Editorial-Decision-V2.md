# Editorial Decision Letter (V2)

**Paper:** Artificial Intelligence and Machine Learning for Magnetic Confinement Fusion Plasma Control: A Comprehensive Review (2024–2026)

**Decision: MINOR REVISION**

**Date:** 2026-05-30

---

## 1. Decision Rationale

The paper presents a comprehensive and ambitious survey of AI/ML applications in magnetic confinement fusion plasma control, covering 8 core dimensions and 6 extension topics across 121 references. This revised version has significantly improved over its predecessor:

1. **All 3 Devil's Advocate CRITICAL issues from the previous round have been addressed:**
   - DA-C1 (Over-claiming): Evidence quality framework (Level A-D) added with reading guide
   - DA-C2 (DIII-D centralization): Explicitly acknowledged in conclusion with 3-point implications analysis
   - DA-C3 (Narrative framing): Deployment readiness assessment (Section 10.11) added with 5 gap dimensions and 3-phase roadmap

2. **All 7 Priority 1 issues from the previous round have been addressed:**
   - R1 (PRISMA methodology): Inclusion/exclusion criteria documented (Section A.3.1)
   - R2 (Evidence quality): Level A-D framework implemented throughout
   - R3 (Key studies count): Standardized to 44
   - R4 (I/E criteria): I1-I5, E1-E7 criteria added
   - R5 (DIII-D centralization): Explicitly discussed in conclusion
   - R6 (Deployment readiness): New Section 10.11 added
   - R7 (Terminology): "多模态预训练框架" used consistently

3. **Additional improvements in this version:**
   - Mermaid-based figures replacing text placeholders
   - New PINN section (7.6) with three 2025 papers
   - 4 new references [118]-[121]
   - TRL rubric with explicit evidence mapping
   - Expanded failure mode catalog (7 failure modes)

The remaining issues are minor and do not prevent publication.

---

## 2. Review Panel Summary

| Reviewer | Recommendation | Key Concern |
|----------|---------------|-------------|
| EIC | Minor Revision | PRISMA diagram missing, foundational references |
| R1 (Methodology) | Minor Revision | PRISMA diagram missing, search log incomplete |
| R2 (Domain) | Minor Revision | Foundational references missing, PINNs depth |
| R3 (Perspective) | Minor Revision | Cross-domain comparison depth, regulatory pathways |
| Devil's Advocate | Minor Revision | Preprint prominence, TRL calibration |

**Consensus: MINOR REVISION** — All 5 reviewers agree the paper is close to submission-ready.

---

## 3. Consensus Issues

### [CONSENSUS-5] Issues (All 5 reviewers agree)

**C1. Missing foundational references**
- EIC: "Add Kates-Harbeck et al. (2019) and Rea et al. (2019) as background"
- R1: Noted as gap in literature coverage
- R2: "Critical omissions still not addressed"
- R3: Noted as gap
- DA: Noted in observations
- **Action Required**: Add Kates-Harbeck et al. (2019, Nature 568) and Rea et al. (2019, PPCF 61) as background context for disruption prediction

### [CONSENSUS-3] Issues (3 reviewers agree)

**C2. PRISMA flow diagram missing**
- EIC: "Add PRISMA-style flow diagram"
- R1: "No PRISMA flow diagram" (Priority 1)
- R2: Noted as methodology gap
- **Action Required**: Add a visual PRISMA-style flow diagram to the methodology section

**C3. Cross-domain comparison could be deeper**
- EIC: "Consider adding a comparison table"
- R3: "Add a comparison table mapping specific AI safety challenges"
- DA: Noted as observation
- **Action Required**: Add a comparison table to Section 10.9

---

## 4. Devil's Advocate Assessment

The Devil's Advocate found **no CRITICAL issues** in this version — a significant improvement from the previous round's 3 CRITICAL issues. The remaining issues are MAJOR (preprint prominence in abstract, TRL calibration) and MINOR (Mermaid rendering, conclusion length). The DA's strongest counter-argument — that the "field maturity" narrative rests on a thin, preprint-heavy, DIII-D-concentrated evidence base — is acknowledged by the paper's own evidence framework and deployment readiness assessment.

---

## 5. Revision Roadmap

### Priority 1: Must Fix

| # | Issue | Source | Action |
|---|-------|--------|--------|
| R1 | Add missing foundational references | EIC, R1, R2, R3, DA | Cite Kates-Harbeck et al. (2019) and Rea et al. (2019) as background context |

### Priority 2: Should Fix

| # | Issue | Source | Action |
|---|-------|--------|--------|
| R2 | Add PRISMA flow diagram | EIC, R1, R2 | Create visual flow diagram showing search, screening, and inclusion process |
| R3 | Deepen cross-domain comparison | EIC, R3 | Add comparison table to Section 10.9 |
| R4 | Make preprint caveat more prominent in abstract | DA | Consider separate sentence at end of abstract |
| R5 | Consider adjusting TRL for DRL control | DA | Consider splitting DRL TRL by application type |

### Priority 3: Nice to Have

| # | Issue | Source | Action |
|---|-------|--------|--------|
| R6 | Consolidate conclusion (13 points) | EIC, DA | Group into 3-4 themes |
| R7 | Add regulatory pathway discussion | R3 | Brief discussion of NRC/IAEA engagement |
| R8 | Add glossary | R3 | For non-specialist readers |
| R9 | Add search execution log details | R1 | Database-specific dates and counts |

---

## 6. Revised Assessment

**Previous Decision: MAJOR REVISION**

**Revised Decision: MINOR REVISION**

**Rationale**: All 3 Devil's Advocate CRITICAL issues have been addressed. All 7 Priority 1 issues from the previous round have been addressed. The 5-reviewer panel consensus is Minor Revision. The remaining issues (foundational references, PRISMA diagram, cross-domain depth) are minor and addressable.

The paper now includes:
- A systematic evidence quality framework (Level A-D)
- An explicit TRL rubric with evidence mapping
- A deployment readiness assessment distinguishing demos from deployment
- An expanded failure mode catalog (7 failure modes)
- A strengthened DIII-D centralization analysis
- Corrected physics descriptions (Seo et al. multi-objective reward)
- Complete methodology documentation (I/E criteria)
- Mermaid-based figures for all 5 diagrams
- 4 new references strengthening PINN and spherical tokamak sections

**Recommendation**: The paper is ready for final preparation — add foundational references, create PRISMA diagram, and submit.

---

*Editorial Decision synthesized from 5 review reports (EIC, R1 Methodology, R2 Domain, R3 Perspective, Devil's Advocate).*

*Companion documents: Review-EIC-V2.md, Review-R1-Methodology-V2.md, Review-R2-Domain-V2.md, Review-R3-Perspective-V2.md, Review-Devils-Advocate-V2.md*
