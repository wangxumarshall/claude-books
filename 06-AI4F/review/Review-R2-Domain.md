# Domain Expert Review Report (R2)

**Paper:** Artificial Intelligence and Machine Learning for Magnetic Confinement Fusion Plasma Control: A Comprehensive Review (2024-2026)

**Reviewer:** Peer Reviewer 2 — Domain Expert
**Specialization:** Plasma physics, tokamak control systems, 20 years experience in MCF research
**Date:** 2026-05-30

---

## Overall Assessment: Minor Revision

The paper provides an impressively comprehensive survey of AI/ML applications in magnetic confinement fusion plasma control covering the 2024-2026 window. The breadth of coverage across 8 core dimensions and 6 extension topics, spanning 117 references and 13+ devices, is among the most ambitious in this sub-field. The domain contribution is significant, particularly the TRL assessment framework, cross-domain safety comparison, and failure mode catalog. Several physics accuracy issues and missing key references need to be addressed, but the overall scholarly contribution is strong.

---

## Dimension Scores

| Dimension | Score (0-100) | Notes |
|-----------|---------------|-------|
| Literature Coverage | 82 | Broad coverage but some key gaps in stellarator AI and IFE |
| Physics Accuracy | 75 | Generally accurate but several physics claims need verification |
| Theoretical Framework | 78 | Good structure but "foundation model" terminology inconsistent |
| Domain Contribution | 85 | TRL assessment and failure mode catalog are genuine contributions |
| Technical Depth | 70 | Uneven — DRL/disruption deep, PINNs/digital twins thin |
| Missing Key References | 68 | Several important recent works omitted |

**Weighted Score: 76/100**

---

## Detailed Review

### 1. Literature Coverage (Score: 82)

**Strengths:**
- The 8-dimension taxonomy (DRL, disruption, ELM, equilibrium, surrogates, PINNs, foundation models, digital twins) is well-chosen and covers the major research threads
- Device coverage is commendably broad: DIII-D, KSTAR, TCV, JET, AUG, EAST, HL-2A/HL-3, MAST, ST40, ADITYA, EXL-50U, W7-X, WEST
- The inclusion of non-Western facilities (ADITYA, EXL-50U, HL-3) reduces geographic bias
- Conference proceedings from APS-DPP, IAEA FEC, SOFE, EPS, and TOFE are systematically searched

**Weaknesses:**
- The stellarator optimization section (11.1) is underdeveloped given the recent surge in AI-for-stellarator work. Key omissions include:
  - Recent NCSX/HSX optimization work using ML
  - Gradient-based stellarator optimization with automatic differentiation (e.g., DESC code family)
  - The growing body of work on quasi-isodynamic optimization beyond [117]
- The ICF section (11.4) is too thin — only 3 references for a topic that has seen substantial AI activity (NIF shot prediction, implosion symmetry optimization, hohlraum design)
- Spherical tokamak coverage is limited despite MAST-U and ST40 being active platforms
- No coverage of reversed field pinch (RFP) or stellarator AI work beyond W7-X

### 2. Physics Accuracy (Score: 75)

**Strengths:**
- The NTM physics description (Section 2.1) is accurate and well-contextualized
- The disruption taxonomy (Section 3.1) correctly distinguishes current quench, thermal quench, and VDE
- The ELM classification (Type I/II/III) is standard and correct
- The Grad-Shafranov equation context for equilibrium reconstruction is properly presented

**Issues:**

**Issue P1: Seo et al. reward function over-simplification (Section 2.1)**
The paper states the reward function uses "β_N - β_N,crit" as the primary signal. While this is correct, the paper does not mention that the actual Nature 2024 paper uses a multi-objective reward including density limit proximity (greenwald fraction), rotation constraints, and shape error — not just the tearing stability parameter. This over-simplification could mislead readers about what made the DRL controller successful.
**Severity: Medium**

**Issue P2: ELM suppression mechanism claim (Section 4.2)**
The paper states that Kim et al. [28] achieved "cross-device ELM suppression" via adaptive ML. However, the APS-DPP abstract [28] describes applying similar control strategies on DIII-D and KSTAR independently, not a truly cross-device transfer of a trained model. The distinction between "same algorithm applied on two devices" and "cross-device transfer" is important for the field.
**Severity: Medium**

**Issue P3: PINN convergence claim (Section 7.5)**
The paper correctly identifies PINN convergence failures as a problem but attributes them primarily to "spectral bias." The more fundamental issue in fusion PINNs is the multi-scale nature of the PDEs (transport timescales ~100ms vs. MHD timescales ~μs), which creates stiff optimization landscapes. Spectral bias is one manifestation but not the root cause.
**Severity: Low**

**Issue P4: TRL assessment calibration (Section 10.7)**
The paper rates DRL control at TRL 4-5. Given that Seo et al. demonstrated closed-loop control on DIII-D (a real tokamak), this should be at least TRL 5 ("component validation in relevant environment"). The DIII-D experiment was conducted in a relevant plasma environment with real actuators. The paper's own criteria state TRL 5 requires "relevant environment" — DIII-D is exactly that for tokamak control.
**Severity: Medium**

**Issue P5: "Foundation model" terminology (Section 8.1)**
The paper correctly critiques the use of "foundation model" in fusion but then inconsistently uses it throughout. The proposed alternative "multi-modal pretrained framework" is more accurate but the paper should commit to one terminology consistently. The current state — critiquing the term in Section 8.1 but using it in abstracts and conclusions — undermines the critical argument.
**Severity: Low** (already noted by EIC)

### 3. Theoretical Framework (Score: 78)

**Strengths:**
- The 8-dimension taxonomy provides a clear organizational framework
- The TRL assessment provides a maturity-based perspective that is actionable for engineers
- The verification level classification (仿真验证/仿真+实验/实验验证) is well-defined and informative
- The cross-domain comparison (Section 10.9) with aerospace/nuclear-fission/process-control provides valuable context

**Weaknesses:**
- The paper lacks a unifying theoretical framework for understanding *why* certain AI methods work better than others in specific fusion contexts. For example:
  - Why do Transformers outperform LSTMs for disruption prediction? (Answer: attention mechanisms capture long-range temporal dependencies in slowly-evolving plasma instabilities)
  - Why do neural operators outperform standard NNs for surrogate modeling? (Answer: mesh-independent architectures respect the PDE structure)
  - Why does DRL work for plasma control but not for disruption avoidance? (Answer: the reward landscape for control is smoother than for avoidance)
- The connection between plasma physics constraints and AI architecture choices is discussed anecdotally but not systematically

### 4. Domain Contribution (Score: 85)

**Strengths:**
- The TRL assessment (Section 10.7) is a genuine intellectual contribution — no prior review has systematically assessed the maturity of AI-for-fusion technologies
- The failure mode catalog (Section 10.10) is extremely valuable and counteracts the publication bias in the field
- The cross-domain safety comparison (Section 10.9) provides actionable insights for fusion engineers considering AI deployment
- The verification level analysis revealing that only 30% of key studies have experimental validation, with 67% from DIII-D, is an important finding

**Weaknesses:**
- The TRL assessment lacks explicit methodology — how were the ratings determined? What evidence was weighted?
- The failure mode catalog covers only 4 modes; adversarial robustness, data poisoning, and catastrophic forgetting are missing
- The cross-domain comparison is too superficial — one page per domain is insufficient for meaningful analysis

### 5. Technical Depth (Score: 70)

**Strengths:**
- Sections 2 (DRL) and 3 (disruption prediction) have excellent technical depth
- The reward function design discussion (Section 2.1) is detailed and physically grounded
- The FPGA deployment discussion (Section 10.6) is practically valuable

**Weaknesses:**
- Section 7 (PINNs) is too thin for a topic that has generated substantial literature
- Section 9 (digital twins) reads more as a conceptual overview than a technical review
- The surrogate model section (Section 5) covers FNO well but lacks depth on other neural operator architectures (DeepONet, graph neural operators)
- The foundation model section (Section 8) is more descriptive than analytical

### 6. Missing Key References (Score: 68)

The following important recent works are not cited:

**Critical omissions:**

1. **Kates-Harbeck et al. (2019)** — "Predicting disruptive instabilities in controlled fusion plasmas through deep learning." Nature 568, 526-531. This is a foundational paper for disruption prediction that should be cited as background context. It established the CNN/LSTM approach that many 2024-2026 papers build upon.

2. **Rea et al. (2019)** — "Disruption prediction investigations using machine learning tools on DIII-D and Alcator C-Mod." Plasma Physics and Controlled Fusion 61, 044001. Important cross-device disruption prediction work.

3. **Felici & De Tommasi (2024)** — Recent TCV control work that directly complements the Degrave et al. line of research.

4. **Zanisi et al. (2024)** — "Data-driven surrogate modelling of tokamak plasma dynamics using neural operators." Nuclear Fusion. Important FNO/surrogate work from the same group as [40,41].

5. **Park et al. (2024)** — Recent KSTAR disruption prediction work using physics-informed features.

6. **Pavone et al. (2024)** — Recent work on ML-based real-time control at AUG.

7. **Logan et al. (2024)** — "The HTS magnet design optimization using ML" — important for the HTS section (11.2).

8. **DESC code papers** — The DESC stellarator optimization code represents a major advance in gradient-based stellarator design using automatic differentiation, relevant to Section 11.1.

**Minor omissions:**
- Several 2024-2025 IAEA FEC papers on AI for ITER diagnostics
- Recent EUROfusion work on ML-assisted scenario development
- The growing body of work on uncertainty quantification in fusion ML models

---

## Specific Recommendations

### Must Fix (Priority 1)

1. **Fix the Seo et al. reward function description** (Section 2.1): Include the multi-objective nature of the reward (β_N, density limit, rotation, shape error), not just the tearing stability term.

2. **Correct the ELM suppression characterization** (Section 4.2): Distinguish between "same algorithm applied on two devices" and true "cross-device transfer." Kim et al. demonstrated the former, not the latter.

3. **Add missing foundational references**: At minimum, cite Kates-Harbeck et al. (2019) and Rea et al. (2019) as background context for disruption prediction.

4. **Commit to "pre-trained framework" terminology**: If Section 8.1 critiques "foundation model," then the abstract, section titles, and conclusion should use "pre-trained framework" consistently.

### Should Fix (Priority 2)

5. **Deepen the PINNs section** (Section 7): Add discussion of multi-scale challenges, stiff optimization landscapes, and the trade-off between physics constraints and data fitting.

6. **Expand the failure mode catalog** (Section 10.10): Add adversarial robustness, data poisoning, model degradation over time, and catastrophic forgetting.

7. **Add explicit TRL methodology**: Provide a rubric showing which evidence items map to which TRL levels.

8. **Deepen the cross-domain comparison** (Section 10.9): Map specific AI safety challenges in fusion to their analogues in other domains.

### Nice to Have (Priority 3)

9. **Add a "why methods work" framework**: Systematically connect plasma physics constraints to AI architecture choices.

10. **Expand stellarator and ICF coverage**: Both topics have seen substantial recent AI activity that deserves more than 1-2 pages each.

11. **Add DESC code reference** to stellarator section.

12. **Strengthen spherical tokamak coverage**: MAST-U and ST40 are producing important AI results.

---

## Summary

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Literature Coverage | Pass (82) | Broad but some key gaps in stellarator and ICF |
| Physics Accuracy | Conditional (75) | Generally correct but several claims need verification |
| Theoretical Framework | Conditional (78) | Good structure but lacks unifying framework |
| Domain Contribution | Pass (85) | TRL assessment and failure mode catalog are genuine contributions |
| Technical Depth | Conditional (70) | Uneven across sections |
| Missing Key References | Conditional (68) | Several important omissions |

**Overall: Minor Revision** — The paper makes a significant domain contribution through its TRL assessment, failure mode catalog, and verification level analysis. The physics accuracy issues and missing references are addressable. The uneven technical depth is a concern but does not prevent publication if the stronger sections are maintained and weaker sections are either deepened or explicitly marked as "brief overview."

---

*Report generated as part of Stage 3 peer review panel.*
