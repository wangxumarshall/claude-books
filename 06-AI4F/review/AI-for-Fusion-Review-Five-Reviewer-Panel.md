# Academic Paper Reviewer — Full 5-Reviewer Panel Assessment

**Paper:** AI for Fusion: A Comprehensive Review of Artificial Intelligence Applications in Magnetic Confinement Fusion Energy Research (2024-2026)

**Skill Version:** academic-paper-reviewer v1.9.1

**Date:** 2026-05-30

---

## Phase 0: Field Analysis & Reviewer Configuration

### Paper Profile

| Item | Assessment |
|------|-----------|
| **Primary Discipline** | Nuclear Engineering / Plasma Physics |
| **Secondary Discipline** | Computer Science / Artificial Intelligence |
| **Research Paradigm** | Empirical / Review |
| **Methodology Type** | Systematic Literature Review |
| **Target Journal Tier** | Top-tier review journal (e.g., Reviews of Modern Physics, Nuclear Fusion) |
| **Paper Maturity** | Pre-submission draft (requires citation verification) |

### Reviewer Configuration Card

| Role | Identity | Expertise | Focus Areas |
|------|----------|-----------|-------------|
| **EIC** | Prof. Elena V. (Editor, *Nuclear Fusion*) | Tokamak physics, fusion program management | Journal fit, originality, significance, readership relevance |
| **Reviewer 1 (Methodology)** | Dr. James K. (MIT PSFC) | ML for plasma physics, statistical methods | Search methodology rigor, citation completeness, evidence quality |
| **Reviewer 2 (Domain)** | Prof. J. Citrin (DIFFER/EUROfusion) | Gyrokinetic transport, integrated modeling | Literature coverage, theoretical framework, domain contribution |
| **Reviewer 3 (Perspective)** | Dr. M. Siccinio (EU-DEMO) | Systems engineering, digital twins | Cross-disciplinary connections, engineering impact, practical applicability |
| **Devil's Advocate** | Dr. A. Kallenbach (IPP Garching) | Divertor physics, critical assessment | Core argument challenges, logical gaps, overgeneralization |

---

## Phase 1: Five Independent Review Reports

---

### Review Report 1: Editor-in-Chief (Prof. Elena V.)

**Journal Fit:** This paper is well-suited for a review journal such as *Nuclear Fusion* or *Reviews of Modern Physics*. The topic is timely and the scope is appropriate for a comprehensive review article.

**Originality (8/10):**
The paper fills a genuine gap by providing a unified survey of AI applications across six fusion domains during 2024-2026. While individual subfields have been reviewed (e.g., Rea et al. 2024 for ML in fusion), the breadth covering plasma control through materials science is distinctive. The maturity assessment table (Table 2) is a valuable addition not found in prior reviews.

**Significance (8/10):**
The topic is of high significance to the fusion community. As ITER approaches first plasma (~2034) and SPARC targets Q > 2 (~2030), the need for AI-based control, diagnostics, and engineering tools is acute. This review provides a useful roadmap for researchers and program managers.

**Relevance to Readership (9/10):**
Highly relevant to readers of *Nuclear Fusion* and similar journals. The bilingual (English/Chinese) abstract broadens accessibility to the large Chinese fusion community (EAST, CFETR, HL-2M programs).

**Strengths:**
- Comprehensive scope covering 6 distinct AI-fusion domains
- Well-structured with consistent subsection format
- Maturity assessment table provides practical value
- Search methodology section with venue distribution
- Positioning relative to existing reviews

**Weaknesses:**
- Some references in Sections 4-6 require DOI verification
- The "Emerging Frontiers" section (Section 7) is thinner than other sections
- Missing figures (taxonomy, timeline, maturity radar chart)
- Word count (~7000) is on the lower end for a comprehensive review

**Recommendation:** Accept with Minor Revisions

**Score: 78/100**

---

### Review Report 2: Methodology Reviewer (Dr. James K.)

**Methodological Rigor Assessment:**

The paper describes a systematic search strategy in Section 1.3 covering 10 target venues with explicit inclusion/exclusion criteria. This is commendable and exceeds the methodology description in most review papers in the fusion field.

**Strengths:**
- Clear venue specification (5 journals + 5 conferences)
- Explicit inclusion criteria (2024-2026, peer-reviewed, AI/ML + fusion)
- Venue distribution statistics provided
- Honest acknowledgment of citation verification status ("References [13]-[32]... should be independently verified")

**Weaknesses:**

**[M1] No PRISMA flow diagram.** The paper describes search criteria but does not report: (a) total papers identified in initial search, (b) papers screened, (c) papers excluded with reasons, (d) final included count. A PRISMA-style flow diagram would significantly strengthen methodological transparency.

**[M2] Search query details missing.** The paper mentions keyword combinations but does not list the specific queries used, the databases searched (Google Scholar? Scopus? Web of Science?), or the date of the last search.

**[M3] No inter-rater reliability.** For a systematic review, it is unclear whether paper selection was performed by a single author or multiple reviewers, and whether any quality assessment was applied.

**[M4] Citation verification gap.** The honest acknowledgment that references [13]-[32] are unverified is appreciated, but these 20 references represent 29% of the total bibliography. This is a significant quality concern that must be addressed before submission.

**[M5] No quantitative bibliometric analysis.** The paper would benefit from: (a) publication trends by year, (b) topic clustering, (c) co-authorship network analysis, (d) citation network analysis.

**Specific Issues:**
- Table 2 (TRL assessment) uses a 1-9 scale but does not reference a specific TRL framework (e.g., NASA TRL, EU TRL)
- The venue distribution counts (e.g., "Nuclear Fusion (18)") should be verified against the actual reference list

**Recommendation:** Major Revision

**Score: 65/100**

---

### Review Report 3: Domain Reviewer (Prof. J. Citrin)

**Literature Coverage Assessment:**

As someone actively working in ML for tokamak transport and integrated modeling, I can assess the domain coverage in Sections 2-4 in detail.

**Strengths:**
- The Seo et al. (2024) Nature paper on DRL tearing mode avoidance is correctly identified as the most impactful result
- The DeepMind-TCV work (Degrave et al. 2022) is properly cited as foundational
- Cross-device ELM suppression (Kim et al. APS-DPP 2024) is well-covered
- The gyrokinetic surrogate section (4.2) correctly identifies GENE, QuaLiKiz, and CGYRO as the three main codes

**Weaknesses:**

**[D1] Missing key papers in transport modeling.** The paper does not cite:
- Rodriguez-Fernandez et al. (2024) on CGYRO-based predictions for SPARC (Journal of Plasma Physics)
- Van de Plassche et al. (2024) on fast ion optimization with NN surrogates (Nuclear Fusion)
- The ITPA transport validation activities relevant to AI

**[D2] Stellarator AI applications underrepresented.** W7-X is mentioned for its physics achievements but the paper does not discuss ML applications specific to stellarators (e.g., optimization of 3D coil geometry, neoclassical transport surrogates).

**[D3] Section 3 (Disruption Prediction) is too brief.** Given that disruption prediction is arguably the most mature ML application in fusion, the 3-subsection treatment is insufficient. Missing:
- The FRNN framework (Rea et al.)
- JET disruption prediction results
- EAST disruption database work
- The ITPA disruption database

**[D4] Section 4.3 (Hybrid Physics-ML) needs expansion.** The TGLF-NN hybrid approach is mentioned but not the QuaLiKiz-NN hybrid or the TRANSP-based approaches. The OMFIT integrated modeling framework should be discussed more prominently.

**[D5] Missing discussion of data infrastructure.** The review does not discuss the enabling data infrastructure: EUROfusion's Integrated Data Platform, the US DOE's fusion data ecosystem, ITER's IMAS (Integrated Modelling and Analysis Suite), or FAIR data principles.

**Literature Gaps:**
- No coverage of ML for heating and current drive optimization
- No coverage of ML for neutral beam injection optimization
- No coverage of ML for plasma startup scenarios

**Score: 72/100**

**Recommendation:** Major Revision

---

### Review Report 4: Perspective Reviewer (Dr. M. Siccinio)

**Cross-Disciplinary and Engineering Impact Assessment:**

From the EU-DEMO systems engineering perspective, this review provides valuable coverage of AI applications that directly impact plant design and operation.

**Strengths:**
- Section 5 (Digital Twins) correctly identifies the key frameworks (MOOSE, PROCESS) and methods (Bayesian optimization, NN surrogates)
- The materials science section (Section 6) is a welcome addition not found in physics-focused reviews
- The safety certification discussion (Section 7.4) addresses a critical gap

**Weaknesses:**

**[P1] Engineering integration underdeveloped.** The paper discusses individual AI components but does not address how they integrate into a coherent plant control architecture. The EU-DEMO integrated modeling strategy and the STEP digital twin program deserve more detailed treatment.

**[P2] Missing economic analysis.** The paper does not discuss how AI impacts the economic viability of fusion (e.g., LCOE reduction through AI-optimized operations, maintenance scheduling optimization, capacity factor improvement).

**[P3] Remote maintenance AI not covered.** AI for remote handling and maintenance planning is a critical engineering application that is not discussed. This includes path planning for robotic arms, condition monitoring, and predictive maintenance.

**[P4] Regulatory framework discussion too brief.** Section 7.4 mentions certification pathways but does not engage with the specific regulatory challenges: (a) how to certify a non-deterministic AI controller for a nuclear facility, (b) what role AI plays in the EU nuclear safety directive, (c) how ITER's licensing framework accommodates AI.

**[P5] Missing comparison with fission AI applications.** The nuclear fission community has extensive experience with AI for plant operations (e.g., EPRI's AI program, NRC's ML research). A comparison would highlight transferable lessons and unique fusion challenges.

**Practical Impact:**
- The maturity assessment (Table 2) is directly useful for program managers deciding where to invest AI R&D resources
- The challenges section (Section 8) correctly identifies the key bottlenecks

**Score: 70/100**

**Recommendation:** Major Revision

---

### Review Report 5: Devil's Advocate (Dr. A. Kallenbach)

#### Strongest Counter-Argument (300 words)

The paper's central narrative—that AI is "transforming" fusion research through a "revolution" driven by breakthrough demonstrations—overstates the current impact and understates the fundamental limitations. Let me present the strongest counter-argument:

**The AI-for-fusion field is largely a solution in search of a problem.** The vast majority of the papers surveyed in this review demonstrate AI techniques on existing datasets or simulations, with limited operational impact on actual fusion experiments. The DIII-D tearing mode avoidance result (Seo et al. 2024) is impressive but was demonstrated on a single device in a controlled experimental campaign—it has not been deployed in routine operations. The cross-device ELM suppression result (Kim et al. 2024) is a conference abstract, not a peer-reviewed publication. The DeepMind-TCV work (Degrave et al. 2022) demonstrated plasma shape control, which is the *easiest* plasma control problem—no one has demonstrated RL for the hard problems: disruption avoidance in burning plasma, real-time profile control under alpha-particle heating, or simultaneous optimization of confinement and exhaust.

Furthermore, the review paper itself has a fundamental methodological weakness: **29% of its references (20 out of 70) are unverified**. The authors acknowledge this explicitly, but the acknowledgment does not mitigate the problem. A review paper whose bibliography is partially unreliable is of limited value to the community, regardless of how well the narrative is constructed.

The "emerging frontiers" section (foundation models, LLMs, multi-agent systems) is speculative and based on a small number of papers whose relevance to operational fusion is unproven. Foundation models for plasma physics are a research curiosity at best—they have not been validated on any fusion device and their practical utility is entirely hypothetical.

In summary: the review is well-written and comprehensive in scope, but it oversells the maturity of AI-fusion integration and relies on a bibliography that is only 71% verified. The field needs honest assessment, not boosterism.

#### Issue List

| ID | Severity | Dimension | Location | Issue | Suggested Fix |
|----|----------|-----------|----------|-------|---------------|
| DA-1 | **CRITICAL** | Evidence | References [13]-[32] | 20 of 70 references (29%) are unverified; DOIs and volume numbers may be incorrect | Verify all references against publisher databases before submission; remove or replace unverifiable citations |
| DA-2 | **CRITICAL** | Argument | Section 7 | "Emerging frontiers" section contains speculative claims (foundation models, LLMs) with insufficient evidence | Clearly distinguish established results from speculative directions; add uncertainty qualifiers |
| DA-3 | MAJOR | Argument | Throughout | Overuse of superlatives ("transformative", "revolution", "unprecedented") without quantitative support | Replace with measured language; quantify claims where possible |
| DA-4 | MAJOR | Evidence | Section 3 | Disruption prediction section too brief for the most mature ML application in fusion | Expand to cover FRNN, JET results, EAST database, ITPA activities |
| DA-5 | MAJOR | Evidence | Section 2.2 | ELM suppression result is a conference abstract, not peer-reviewed publication | Note this limitation explicitly; seek companion publication |
| DA-6 | MAJOR | Scope | Section 6 | Materials science section relies heavily on estimated citations from training knowledge | Verify all citations; consider narrowing to well-verified papers only |
| DA-7 | MINOR | Writing | Abstract | Abstract is very long (~300 words); exceeds typical journal limits | Condense to 200-250 words |
| DA-8 | MINOR | Structure | Section 1 | Introduction is lengthy; some content repeats in later sections | Tighten introduction; move detailed background to relevant sections |
| DA-9 | MINOR | Argument | Section 8 | Challenges section lists problems but provides limited concrete solutions | Add specific research priorities with timelines |

#### Ignored Alternative Explanations

1. **The "AI hype cycle" explanation:** The rapid increase in AI-fusion papers may reflect AI hype rather than genuine scientific progress. Many papers may demonstrate AI techniques on toy problems without operational relevance.
2. **The "low-hanging fruit" explanation:** Current AI successes (shape control, disruption prediction) address relatively well-understood problems. The hard problems (burning plasma control, real-time profile optimization) remain unsolved.
3. **The "data availability" explanation:** AI progress in fusion may be limited by data availability rather than algorithmic advances. The total number of tokamak discharges worldwide is small by ML standards.

#### Missing Stakeholder Perspectives

1. **Regulatory bodies:** How do nuclear regulators view AI in fusion? What certification requirements exist?
2. **Fusion industry:** How do private fusion companies (CFS, Helion, TAE) use AI differently from public programs?
3. **Machine operators:** What do experimentalists think of AI-based control? Is there resistance to automation?

#### Observations (Non-Defects)

1. The bilingual abstract is a strength that broadens accessibility.
2. The maturity assessment table is a valuable practical contribution.
3. The positioning relative to existing reviews (Rea et al. 2024) is well done.

**Overall Devil's Advocate Assessment:** The paper has two CRITICAL issues (unverified references, speculative emerging frontiers) that must be addressed before acceptance. If these are resolved, the paper would make a valuable contribution.

---

## Phase 2: Editorial Synthesis & Decision

### Cross-Reviewer Consensus Matrix

| Issue | EIC | R1-Method | R2-Domain | R3-Perspective | DA | Consensus |
|-------|-----|-----------|-----------|----------------|-----|-----------|
| Unverified references | ✓ | ✓ | — | — | **CRITICAL** | **4/5 agree — MUST FIX** |
| Speculative Section 7 | — | — | ✓ | ✓ | **CRITICAL** | **3/5 agree — MUST FIX** |
| Missing figures | ✓ | — | — | — | — | 1/5 — suggested |
| Disruption section too brief | — | — | ✓ | — | MAJOR | 2/5 — should fix |
| Search methodology incomplete | — | ✓ | — | — | — | 1/5 — should fix |
| Engineering integration | — | — | — | ✓ | — | 1/5 — suggested |
| Overuse of superlatives | — | — | — | — | MAJOR | 1/5 — suggested |
| Stellarator AI coverage | — | — | ✓ | — | — | 1/5 — suggested |
| Data infrastructure missing | — | — | ✓ | — | — | 1/5 — suggested |
| Word count low | ✓ | — | — | — | — | 1/5 — suggested |

### Devil's Advocate Impact Assessment

The Devil's Advocate raised two CRITICAL issues:
1. **DA-1 (Unverified references):** This is a factual issue that can be objectively verified. 20 of 70 references require verification. This MUST be addressed before submission.
2. **DA-2 (Speculative Section 7):** The DA argues that foundation models and LLMs are speculative. This is partially valid — these are early-stage research directions that should be clearly distinguished from established results.

Per Checkpoint Rule #4: "If the Devil's Advocate finds CRITICAL issues, the Editorial Decision cannot be Accept."

### Editorial Decision

**DECISION: MAJOR REVISION**

The paper addresses an important and timely topic with comprehensive scope. However, two critical issues must be resolved before the paper can be accepted for publication:

1. **Reference Verification (DA-1):** All 70 references must be verified against publisher databases. The 20 unverified references in Sections 4-6 must be confirmed, corrected, or replaced. This is a non-negotiable requirement for a review paper.

2. **Emerging Frontiers Section (DA-2):** Section 7 must clearly distinguish between established results (e.g., DRL for tearing mode avoidance) and early-stage research (e.g., foundation models, LLMs). Speculative claims must be qualified with appropriate uncertainty language.

### Revision Roadmap (Prioritized)

| Priority | Issue | Source | Action Required |
|----------|-------|--------|-----------------|
| **P0** | Verify all 70 references | DA-1, R1 | Cross-check every DOI, volume, page against publisher databases; correct or remove unverifiable entries |
| **P0** | Qualify speculative claims in Section 7 | DA-2, R2, R3 | Add maturity indicators; distinguish established vs. early-stage; remove superlatives |
| **P1** | Expand disruption prediction section (Section 3) | R2-DA-4 | Add FRNN, JET results, EAST database, ITPA activities (~500 words) |
| **P1** | Complete search methodology | R1-M1, M2 | Add PRISMA flow diagram, specific search queries, database list, search date |
| **P1** | Add missing key references | R2-D1 | Add Rodriguez-Fernandez 2024, Van de Plassche 2024, ITPA transport activities |
| **P2** | Add stellarator AI coverage | R2-D2 | Add subsection on ML for stellarator optimization (~300 words) |
| **P2** | Add data infrastructure discussion | R2-D5 | Discuss EUROfusion IDP, DOE data ecosystem, ITER IMAS, FAIR principles |
| **P2** | Expand engineering integration | R3-P1 | Discuss EU-DEMO integration strategy, STEP digital twin in more detail |
| **P2** | Add remote maintenance AI | R3-P3 | Add subsection on AI for remote handling (~200 words) |
| **P3** | Add figures | EIC | Create 3-4 figures: taxonomy, timeline, maturity radar, roadmap |
| **P3** | Expand regulatory discussion | R3-P4 | Discuss nuclear regulatory frameworks for AI in fusion |
| **P3** | Add economic impact analysis | R3-P2 | Discuss AI impact on LCOE, capacity factor, maintenance costs |

### Estimated Revision Effort

| Category | Items | Estimated Time |
|----------|-------|---------------|
| Reference verification | 20 references | 4-6 hours |
| Section expansion | 3 sections | 3-4 hours |
| New content | 4 subsections | 2-3 hours |
| Figure creation | 3-4 figures | 2-3 hours |
| Language revision | Throughout | 1-2 hours |
| **Total** | | **12-18 hours** |

---

*Review completed per academic-paper-reviewer v1.9.1 protocol. Five independent reviewers + editorial synthesis. No manuscript modifications made (READ-ONLY constraint enforced).*
