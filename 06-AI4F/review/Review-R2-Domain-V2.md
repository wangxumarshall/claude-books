# Domain Expert Review Report (R2, V2)

**Paper:** Artificial Intelligence and Machine Learning for Magnetic Confinement Fusion Plasma Control: A Comprehensive Review (2024–2026)

**Reviewer:** Peer Reviewer 2 — Domain Expert
**Specialization:** Plasma physics, tokamak control systems, 20 years experience in MCF research
**Date:** 2026-05-30

---

## Overall Assessment: Minor Revision

The paper provides an impressively comprehensive survey of AI/ML applications in magnetic confinement fusion plasma control covering the 2024-2026 window. The breadth of coverage across 8 core dimensions and 6 extension topics, spanning 121 references and 13+ devices, is among the most ambitious in this sub-field. The domain contribution is significant, particularly the TRL assessment framework, cross-domain safety comparison, and failure mode catalog. The physics accuracy issues from the previous review have been addressed. Several minor issues remain, but the overall scholarly contribution is strong.

---

## Dimension Scores

| Dimension | Score (0-100) | Notes |
|-----------|---------------|-------|
| Literature Coverage | 84 | Broad coverage; stellarator and ICF could be deeper |
| Physics Accuracy | 82 | Previous issues fixed; minor issues remain |
| Theoretical Framework | 80 | Good structure; "foundation model" terminology now consistent |
| Domain Contribution | 87 | TRL assessment and failure mode catalog are genuine contributions |
| Technical Depth | 73 | Uneven — DRL/disruption deep, PINNs/digital twins improving |
| Missing Key References | 72 | Foundational references still missing |

**Weighted Score: 80/100**

---

## Detailed Review

### 1. Literature Coverage (Score: 84)

**Strengths:**
- The 8-dimension taxonomy is well-chosen and covers major research threads
- Device coverage is commendably broad: DIII-D, KSTAR, TCV, JET, AUG, EAST, HL-2A/HL-3, MAST, ST40, ADITYA, EXL-50U, W7-X, WEST
- The inclusion of non-Western facilities (ADITYA, EXL-50U, HL-3) reduces geographic bias
- Conference proceedings from APS-DPP, IAEA FEC, SOFE, EPS, and TOFE are systematically searched
- The new references [118]-[121] strengthen the PINN and spherical tokamak sections

**Weaknesses:**
- The stellarator optimization section (11.1) is better but still could be deeper given the recent surge in AI-for-stellarator work
- The ICF section (11.4) remains thin — only 4 references for a topic with substantial AI activity
- Spherical tokamak coverage has improved with Parisi [118] but could be stronger
- No coverage of reversed field pinch (RFP) AI work

### 2. Physics Accuracy (Score: 82)

**Strengths:**
- The NTM physics description (Section 2.1) is accurate and well-contextualized
- The disruption taxonomy (Section 3.1) correctly distinguishes current quench, thermal quench, and VDE
- The ELM classification (Type I/II/III) is standard and correct
- The Grad-Shafranov equation context for equilibrium reconstruction is properly presented
- The Seo et al. reward function is now correctly described as multi-objective (Section 2.1)

**Remaining Issues:**

**Issue P1: ELM suppression characterization (Section 4.2) — Minor**
The paper states Kim et al. achieved "跨装置ELM抑制" (cross-device ELM suppression). The description is now more nuanced, noting the same control architecture was applied on DIII-D and KSTAR independently. However, the term "跨装置" could still be misread as "transfer of a trained model." Consider adding an explicit clarification that this was "same algorithm applied on two devices" rather than "cross-device transfer of a trained model."
**Severity: Low**

**Issue P2: PINN convergence claim (Section 7.5) — Minor**
The paper correctly identifies PINN convergence failures as a problem. The new Section 7.6 adds valuable depth. The discussion of multi-scale challenges is now adequate.
**Severity: Low** (addressed)

**Issue P3: TRL assessment calibration (Section 10.7) — Minor**
The TRL ratings are now well-calibrated with explicit rubric. DRL control at TRL 4-5 is appropriate given the DIII-D experimental validation. The rubric correctly identifies DIII-D as a "relevant environment" for TRL 5.
**Severity: Low** (addressed)

### 3. Theoretical Framework (Score: 80)

**Strengths:**
- The 8-dimension taxonomy provides a clear organizational framework
- The TRL assessment provides a maturity-based perspective that is actionable
- The verification level classification is well-defined and informative
- The cross-domain comparison (Section 10.9) provides valuable context
- The "foundation model" terminology is now consistent — Section 8.1 critiques the term and the rest of the paper uses "多模态预训练框架"

**Weaknesses:**
- The paper still lacks a unifying theoretical framework for understanding why certain AI methods work better than others in specific fusion contexts
- The connection between plasma physics constraints and AI architecture choices is discussed anecdotally but not systematically

### 4. Domain Contribution (Score: 87)

**Strengths:**
- The TRL assessment (Section 10.7) is a genuine intellectual contribution
- The failure mode catalog (Section 10.10) now covers 7 failure modes — significantly expanded
- The cross-domain safety comparison (Section 10.9) provides actionable insights
- The deployment readiness assessment (Section 10.11) honestly distinguishes research from deployment
- The verification level analysis revealing 27% experimental, 67% from DIII-D, is an important finding

**Weaknesses:**
- The cross-domain comparison is still somewhat superficial
- The failure mode catalog could include more discussion of mitigation strategies

### 5. Technical Depth (Score: 73)

**Strengths:**
- Sections 2 (DRL) and 3 (disruption prediction) have excellent technical depth
- The reward function design discussion (Section 2.1) is detailed and physically grounded
- The FPGA deployment discussion (Section 10.6) is practically valuable
- The new PINN section (7.6) adds depth with three 2025 papers

**Weaknesses:**
- Section 7 (PINNs) overall is still thin — Section 7.6 helps but 7.1-7.5 remain brief
- Section 9 (digital twins) reads more as a conceptual overview than a technical review
- The surrogate model section (Section 6) covers FNO well but lacks depth on DeepONet and graph neural operators
- The foundation model section (Section 8) is more descriptive than analytical

### 6. Missing Key References (Score: 72)

**Critical omissions still not addressed:**

1. **Kates-Harbeck et al. (2019)** — "Predicting disruptive instabilities in controlled fusion plasmas through deep learning." Nature 568, 526-531. This is a foundational paper for disruption prediction that should be cited as background context.

2. **Rea et al. (2019)** — "Disruption prediction investigations using machine learning tools on DIII-D and Alcator C-Mod." Plasma Physics and Controlled Fusion 61, 044001. Important cross-device disruption prediction work.

**Minor omissions:**
- DESC code papers for stellarator optimization
- Recent EUROfusion work on ML-assisted scenario development
- The growing body of work on uncertainty quantification in fusion ML models

---

## Specific Recommendations

### Must Fix (Priority 1)

1. **Add missing foundational references**: Cite Kates-Harbeck et al. (2019) and Rea et al. (2019) as background context for disruption prediction.

### Should Fix (Priority 2)

2. **Clarify ELM suppression characterization** (Section 4.2): Add explicit clarification that Kim et al. demonstrated "same algorithm applied on two devices" rather than "cross-device transfer of a trained model."

3. **Deepen the PINNs section** (Section 7): The new Section 7.6 is good, but consider adding more discussion of multi-scale challenges in 7.5.

4. **Expand the failure mode catalog** (Section 10.10): Consider adding mitigation strategies for each failure mode.

### Nice to Have (Priority 3)

5. **Add a "why methods work" framework**: Systematically connect plasma physics constraints to AI architecture choices.

6. **Expand stellarator and ICF coverage**: Both topics have seen substantial recent AI activity.

7. **Add DESC code reference** to stellarator section.

---

## Summary

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Literature Coverage | Pass (84) | Broad but some gaps in stellarator and ICF |
| Physics Accuracy | Pass (82) | Previous issues fixed; minor issues remain |
| Theoretical Framework | Conditional (80) | Good structure but lacks unifying framework |
| Domain Contribution | Pass (87) | TRL assessment and failure mode catalog are genuine contributions |
| Technical Depth | Conditional (73) | Uneven across sections |
| Missing Key References | Conditional (72) | Foundational references still missing |

**Overall: Minor Revision** — The paper makes a significant domain contribution through its TRL assessment, failure mode catalog, and deployment readiness analysis. The physics accuracy issues from the previous review have been addressed. The missing foundational references should be added. The uneven technical depth is a concern but does not prevent publication.

---

*Report generated as part of Stage 3 peer review panel (V2).*
