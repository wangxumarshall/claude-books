# Phase 5: Methodology Review Report

**Paper:** AI and Machine Learning for Magnetic Confinement Fusion Plasma Control: A Comprehensive Review (2024-2026)
**File:** AI-for-Fusion-V2.md
**Reviewer:** Ethics and Methodology Reviewer
**Date:** 2026-05-30

---

## Overall Assessment: CONDITIONAL PASS

The review paper demonstrates substantial scholarly effort and provides valuable synthesis of a rapidly evolving field. However, the methodology documentation has significant gaps that prevent full reproducibility. The paper would benefit from explicit inclusion of the search protocol details, resolution of internal statistical inconsistencies, and addition of standard systematic review elements.

---

## 1. Methodology Strengths

### 1.1 Well-Defined Source Portfolio
The paper clearly identifies 5 primary journals and 5 primary conferences (Section 1.2, Appendix A.1-A.2), with impact factors and publishers documented. This provides a defensible scope for a domain-specific review.

### 1.2 Transparent Peer-Review Status Labeling
Every reference is labeled with its peer-review status ([期刊论文], [会议报告], [预印本], [技术报告], [专著]), and the paper explicitly acknowledges the high preprint ratio (78%) with appropriate caveats about the limitations of unreviewed work. This is commendable transparency.

### 1.3 Verification Level Classification
The A.5 table classifies each key study by verification level (仿真验证 / 仿真+实验 / 实验验证), which provides readers with crucial context about the maturity of cited claims.

### 1.4 Critical Self-Assessment
The paper includes several sections of genuine critical analysis:
- Section 8.1 critically evaluates the applicability of "foundation models" to fusion, noting data scarcity constraints
- Section 10.10 documents failure modes and negative results, counteracting publication bias
- Section 10.7 provides TRL assessments with explicit justification
- Section 10.5 discusses data quality and sharing challenges honestly

### 1.5 Cross-Domain Benchmarking
Section 10.9 provides valuable context by comparing fusion AI practices with aerospace, nuclear fission, and process control domains, referencing specific standards (DO-178C, IEC 61508, IEC 61511).

### 1.6 Comprehensive Device Coverage
The review covers 13+ tokamak devices and stellarators (Section 10.11), including non-Western facilities (EAST, HL-3, ADITYA, EXL-50U), reducing geographic bias.

---

## 2. Methodology Weaknesses

### 2.1 No PRISMA Flow Diagram or Equivalent
The paper does not provide a flow diagram showing the number of records identified, screened, excluded (with reasons), and included. This is a standard element even for narrative reviews that claim "systematic search" elements. The Methodology Blueprint (Methodology-Blueprint.md) specifies a search execution log template (Appendix A), but this log is not populated in the final paper.

### 2.2 Inclusion/Exclusion Criteria Not in Paper
The Methodology-Blueprint.md defines detailed inclusion criteria (I1-I5) and exclusion criteria (E1-E7), including borderline case resolution rules. However, these criteria are **not included** in the review paper itself (AI-for-Fusion-V2.md). A reader cannot assess whether the paper selection was systematic or ad hoc.

### 2.3 No Search Execution Documentation
The paper does not report:
- Exact dates when searches were conducted
- Number of results retrieved from each database
- Number of records after deduplication
- Number of records excluded at each screening stage with reasons
- Which databases yielded which references

### 2.4 Internal Statistical Inconsistencies
Several numerical claims are inconsistent within the paper (detailed in Section 3 below).

### 2.5 Scope Boundary Ambiguity
The paper claims to focus on "2024-2026" literature but includes approximately 20 references from 2018-2023 as core content (not merely background). While some foundational references are expected, the boundary between "background context" and "within scope" is not clearly delineated in the paper text.

### 2.6 Single-Author Review Process
The review appears to be conducted by a single author (or a single AI agent). No dual-screening, inter-rater reliability, or independent verification process is documented. The Methodology-Blueprint.md mentions a "five-phase pipeline" with peer review, but the actual execution of these quality controls is not evidenced.

---

## 3. Specific Issues

### Issue 1: Key Studies Table Count Inconsistency
**Severity: Medium**

The paper makes conflicting claims about the number of key studies in the classification table:
- Section 1.3 states: "建立了包含**33项**关键研究的分类比较表" (33 key studies)
- Appendix A.5 introduction states: "该表格共收录**43项**关键研究" (43 key studies)
- Actual count of table rows: **40 entries**

All three numbers are different. This undermines confidence in the statistical reporting.

**Recommendation:** Recount and correct to the actual number (40). Use a consistent number throughout the paper.

### Issue 2: Missing Inclusion/Exclusion Criteria
**Severity: High**

The Methodology-Blueprint.md defines explicit criteria (I1-I5, E1-E7) and borderline case resolution rules, but none of these appear in the review paper. A reader has no way to determine why specific papers were included or excluded.

**Recommendation:** Add a subsection to Appendix A documenting the inclusion/exclusion criteria used.

### Issue 3: No Search Execution Log
**Severity: High**

The Methodology-Blueprint.md includes a search execution log template (Appendix A) with columns for database, date, query string, raw results, post-dedup results, post-screening results, and included count. This log is not populated in the paper.

**Recommendation:** Populate the search execution log with actual data and include it as an appendix.

### Issue 4: Pre-2024 References Used as Core Content
**Severity: Medium**

Approximately 18-20 references from 2018-2023 are cited as core content (not just background), including:
- [11] Tracey et al. 2023 - cited as DRL practical application
- [23] Arnold et al. 2023 - cited as disruption prediction method
- [24] Shen et al. 2023 - cited as cross-device prediction
- [25] Zheng et al. 2022 - cited as transferable prediction
- [26] Shen et al. 2022 - cited as physics-guided prediction
- [40] Gopakumar et al. 2023 - cited as FNO surrogate model
- [41] Gopakumar et al. 2023 - cited as FNO plasma modelling
- [47] Mathews 2022 - cited as PINN edge turbulence
- [54] Zhu et al. 2022 - cited as divertor detachment model
- [59] Wan et al. 2022 - cited as LCFS reconstruction
- [63] Ai et al. 2023 - cited as disruption precursor
- [101] Mathews et al. 2022 - cited as deep electric field prediction
- [102] Fujii et al. 2018 - cited as robust regression

The Methodology Blueprint allows "maximum 15 papers" for "foundational context" from pre-2024, but these are not labeled as foundational context in the paper -- they are integrated into the main narrative as if they are within scope.

**Recommendation:** Either (a) explicitly label pre-2024 core references as "foundational context" with a note explaining their inclusion, or (b) expand the stated scope to "2022-2026" with justification.

### Issue 5: Placeholder Author Information
**Severity: Medium**

The author field contains: "[作者姓名]", "[所在机构]", "[邮箱地址]". While this may be intentional for a draft, it means:
- Conflicts of interest cannot be assessed
- Author expertise cannot be evaluated
- Institutional affiliations (which may indicate bias toward specific devices or approaches) are unknown

**Recommendation:** Complete author information before any submission or circulation.

### Issue 6: No Conflict of Interest Statement
**Severity: Medium**

The paper contains no conflict of interest declaration. The Methodology-Blueprint.md includes a template COI statement (Section 8.1), but it is not included in the review paper.

**Recommendation:** Add a conflict of interest statement, even if it declares no conflicts.

### Issue 7: No Funding Acknowledgment
**Severity: Low**

No funding source is disclosed. If the review was conducted as part of funded research, this should be disclosed per standard academic practice.

**Recommendation:** Add funding acknowledgment section or declare no funding.

### Issue 8: TRL Assessment Discrepancies with Blueprint
**Severity: Low**

The TRL assessments in the paper (Section 10.7) differ slightly from those in the Methodology-Blueprint.md (Section 4.3):

| Sub-Domain | Blueprint TRL | Paper TRL |
|------------|---------------|-----------|
| DRL control | 5-6 | 4-5 |
| Disruption prediction | 6-7 | 5-6 |
| ELM detection | 5-6 | 4-5 |
| Equilibrium reconstruction | 5-6 | 5-6 |
| Surrogate models | 3-4 | 4 |
| PINNs | 2-3 | 2-3 |
| Foundation models | 2-3 | 3 |
| Digital twins | 3-4 | 3-4 |

The paper consistently rates technologies lower than the blueprint. This is not necessarily wrong (the paper may have better evidence), but the discrepancy should be acknowledged or explained.

**Recommendation:** Document the rationale for TRL assignments that differ from the methodology blueprint, or reconcile the two.

### Issue 9: Reference Type Count Verification
**Severity: Low (Verified Correct)**

The paper claims: 21 journal papers (18%), 2 conference reports (2%), 91 preprints (78%), 1 technical report (1%), 2 monographs (2%). Manual verification against the reference list confirms these counts are correct (21+2+91+1+2 = 117).

### Issue 10: Topic Distribution Verification
**Severity: Low (Verified Correct)**

The paper claims topic distribution: DRL (19), Disruption (13), ELM (10), Equilibrium (11), Surrogates (18), PINN (8), Foundation (11), Digital Twin (9), Engineering (18). Sum = 117. This is internally consistent.

### Issue 11: No Data Availability Statement
**Severity: Low**

The review does not include a data availability statement. While review papers do not generate primary data, the search results and screening decisions constitute data that could be made available for reproducibility.

**Recommendation:** Consider making the search results and screening decisions available as supplementary material.

### Issue 12: Conference Abstract Evidence Limitations
**Severity: Low**

Reference [28] (Kim et al. APS-DPP 2024) is cited extensively as a key result (cross-device ELM suppression) but is a conference abstract/report without full peer review. The paper appropriately labels it [会议报告] but does not discuss the evidence limitations of relying on conference abstracts for major claims.

**Recommendation:** Add a note in Section 4.2 acknowledging that the Kim et al. result is based on a conference presentation and noting the evidence limitation.

---

## 4. Reproducibility Assessment

### 4.1 What Could Be Reproduced
- The source portfolio (10 venues) is clearly defined
- The keyword strategy is documented (Section 1.2)
- The peer-review status labeling system is consistent
- The verification level classification is defined
- The TRL framework is referenced (NASA TRL 1-9)

### 4.2 What Could NOT Be Reproduced
- The exact search queries used in each database
- The screening process and decisions
- The rationale for including specific borderline papers
- The rationale for excluding papers not in the corpus
- The snowball citation tracking process and decisions
- The date of search execution

### 4.3 Reproducibility Rating: MODERATE
An independent researcher could identify many of the same papers using the documented keywords and venues, but could not reproduce the exact corpus or verify that no relevant papers were missed.

---

## 5. Bias Assessment

### 5.1 Publication Bias (Acknowledged)
The paper appropriately acknowledges the 78% preprint ratio and its implications. Section 10.10 on failure modes partially addresses positive-results bias.

### 5.2 Selection Bias (Partially Mitigated)
The multi-venue search strategy and snowball tracking reduce selection bias. However, without documented screening criteria, the potential for unconscious selection bias remains.

### 5.3 Geographic/Device Bias (Well Mitigated)
The review covers devices from the US (DIII-D), South Korea (KSTAR), EU (JET, AUG, TCV, WEST, W7-X), China (EAST, HL-2A, HL-3, EXL-50U), UK (MAST, ST40), India (ADITYA), and Switzerland (TCV). This is commendably broad.

### 5.4 Temporal Bias (Partially Addressed)
The 2024-2026 window is appropriate for a rapidly evolving field, but the inclusion of ~20 pre-2024 references as core content creates ambiguity about the actual temporal scope.

### 5.5 Method Bias (Unclear)
Without documented inclusion criteria, it is unclear whether certain AI methods were preferentially covered. The paper does cover a wide range of methods (DRL, CNN, Transformer, FNO, PINN, GAN, diffusion models, LLMs), suggesting reasonable method diversity.

---

## 6. Ethical Considerations

### 6.1 Disclosure Issues
- No conflict of interest statement
- No funding disclosure
- No author information
- AI tool usage not disclosed in the paper (though documented in the Methodology Blueprint)

### 6.2 Citation Ethics
- All references include author, title, venue, and year (appropriate)
- DOIs are provided for journal papers (appropriate)
- arXiv identifiers are provided for preprints (appropriate)
- No evidence of citation manipulation or coercive citation

### 6.3 Preprint Handling
- Preprints are clearly labeled (appropriate)
- The high preprint ratio is acknowledged with caveats (appropriate)
- However, preprint conclusions are sometimes presented with the same confidence as peer-reviewed results

### 6.4 AI-Generated Content Disclosure
The Methodology-Blueprint.md states: "AI tools (Claude, GPT-4) were used for literature search assistance, draft generation, and citation verification." This disclosure is not present in the review paper itself. Many journals now require AI tool usage disclosure.

**Recommendation:** Add an AI tool usage statement to the paper.

---

## 7. Recommendations

### Priority 1 (Must Fix Before Submission)
1. **Add inclusion/exclusion criteria** from the Methodology Blueprint to the paper's appendix
2. **Resolve the key studies table count** (33 vs 43 vs 40) -- use the actual count consistently
3. **Complete author information** and add conflict of interest statement
4. **Add a search execution log** or at minimum document the search dates and result counts

### Priority 2 (Should Fix)
5. **Clearly delineate pre-2024 references** as "foundational context" in the paper text, or expand the stated scope
6. **Add AI tool usage disclosure** to the paper
7. **Reconcile TRL assessments** between the blueprint and the paper, or document the rationale for differences
8. **Add a brief PRISMA-style flow diagram** or equivalent showing the literature screening process

### Priority 3 (Nice to Have)
9. **Add data availability statement** offering to share search results
10. **Add funding acknowledgment** section
11. **Strengthen caveats** around conference abstract evidence (particularly [28])
12. **Consider adding a "Limitations" section** to the paper itself (currently only in the Methodology Blueprint)

---

## 8. Summary

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Methodology Rigor | Conditional | Good framework exists (Blueprint) but not fully documented in paper |
| Statistical Reporting | Conditional | Reference counts verified correct; key studies table count inconsistent |
| Bias Assessment | Pass | Good geographic and method diversity; preprint bias acknowledged |
| Reproducibility | Conditional | Venues and keywords documented; screening process undocumented |
| Ethical Considerations | Conditional | Preprint labeling excellent; COI and AI disclosure missing |

**Overall: CONDITIONAL PASS** -- The paper provides valuable scholarly synthesis with commendable transparency on preprint limitations and failure modes. However, the methodology documentation gaps (missing I/E criteria, no search log, statistical inconsistencies, missing disclosures) must be addressed before the paper meets the standards expected of a comprehensive review in a peer-reviewed journal.

---

*Report generated as part of Phase 5 review pipeline.*
*Companion documents: Methodology-Blueprint.md, Research-Question-Brief.md*
