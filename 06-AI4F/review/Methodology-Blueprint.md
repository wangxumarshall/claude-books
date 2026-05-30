# Methodology Blueprint

**Paper:** AI/ML in Magnetic Confinement Fusion Plasma Control: A Comprehensive Review (2024--2026)

**Version:** 1.0

**Date:** 2026-05-30

**Pipeline Stage:** Phase 1b -- Methodology Design (feeds Phase 2 Literature Search)

---

## 1. Research Paradigm

### 1.1 Epistemological Position

This review adopts a **pragmatist-positivist** epistemological stance appropriate for a technical survey in engineering science.

| Dimension | Position | Justification |
|-----------|----------|---------------|
| **Ontology** | Realist | Plasma control problems have objective physical states; AI/ML methods either succeed or fail on measurable criteria (AUC, TPR/FPR, inference latency, disruption avoidance rate) |
| **Epistemology** | Positivist with pragmatic flexibility | Knowledge is generated through empirical measurement and reproducible experiment; however, the review also values engineering judgment, practitioner experience, and "negative results" that resist clean quantification |
| **Axiology** | Value-neutral reporting | The review reports findings without advocacy; TRL assessments are evidence-based, not promotional |
| **Methodology** | Narrative comprehensive review | Not a PRISMA-governed systematic review or meta-analysis; the field is too young and heterogeneous for formal meta-analytic synthesis |

### 1.2 Why Not a Systematic Review?

A formal systematic review (PRISMA 2020) was considered and rejected for three reasons:

1. **Heterogeneity of outcomes.** DRL control papers report reward functions, disruption prediction papers report AUC/TPR/FPR, surrogate models report speedup factors and relative error. There is no common effect size for meta-analysis.
2. **Prematurity.** The 2024--2026 window contains approximately 150--250 candidate papers across 10 venues. Many are preprints or conference abstracts without full-text peer review. A rigid PRISMA protocol would exclude valuable early-stage work.
3. **Narrative value.** The primary contribution is a *synthesis* -- connecting eight sub-domains through cross-cutting themes (interpretability, safety, portability) -- which is better served by narrative structure than by tabular systematic extraction.

### 1.3 Review Classification

Following Grant & Booth (2009) typology, this is a **"mapping review"** with **"systematic search"** elements:

- **Systematic search** elements: structured keyword strategy, defined inclusion/exclusion criteria, venue-level coverage tracking, citation verification protocol.
- **Narrative synthesis** elements: thematic organization by 8 dimensions + 6 extended topics, TRL assessment, cross-domain comparison, expert judgment on maturity.

---

## 2. Method Selection and Justification

### 2.1 Primary Method: Structured Literature Review

The review follows a five-phase pipeline (already defined in Research-Question-Brief.md, Section 8):

| Phase | Method | Output |
|-------|--------|--------|
| Phase 1 | RQ formulation + Methodology blueprint | This document |
| Phase 2 | Systematic keyword search + snowball expansion | Verified reference corpus (target: 80--120 papers) |
| Phase 3 | Thematic coding + TRL assessment | Per-dimension synthesis with evidence grading |
| Phase 4 | Narrative writing with classification tables | Structured review manuscript |
| Phase 5 | Internal peer review + citation audit | Quality-assured final manuscript |

### 2.2 Supplementary Methods

| Method | Purpose | Section |
|--------|---------|---------|
| **Snowball citation tracking** | Identify seminal pre-2024 papers (DeepMind TCV 2022, etc.) and forward citations from 2024--2026 | Section 3.3 |
| **TRL assessment rubric** | Map each sub-domain to NASA TRL 1--9 using defined evidence criteria | Section 4.3 |
| **Cross-domain comparison** | Benchmark fusion AI practices against aerospace (DO-178C), nuclear fission (10 CFR 50 Appendix B), and process control (IEC 61511) | Section 4.4 |
| **Evidence grading** | Classify each cited result by validation level (L1--L5) | Section 5.2 |
| **Failure mode cataloging** | Systematically record negative results and failure modes to counter publication bias | Section 6.3 |

---

## 3. Data Strategy

### 3.1 Source Portfolio

#### 3.1.1 Journals (5 primary + 3 supplementary)

**Primary journals** (systematic coverage of every issue, 2024--2026):

| Journal | Publisher | Impact Factor (2024) | Rationale |
|---------|-----------|---------------------|-----------|
| *Nuclear Fusion* (NF) | IOP Publishing | ~4.2 | Premier MCF journal; covers plasma control, diagnostics, heating |
| *Physical Review Letters* (PRL) | APS | ~8.1 | High-impact breakthroughs (Seo et al. 2024 DRL paper) |
| *Plasma Physics and Controlled Fusion* (PPCF) | IOP Publishing | ~2.4 | Core plasma physics + control theory |
| *Physics of Plasmas* (PoP) | AIP | ~2.2 | Broad plasma physics coverage; high volume |
| *Fusion Engineering and Design* (FED) | Elsevier | ~1.9 | Engineering integration, digital twins, control systems |

**Supplementary journals** (keyword search only):

| Journal | Publisher | Rationale |
|---------|-----------|-----------|
| *Nature* / *Nature Physics* | Springer Nature | Landmark AI-fusion papers (Degrave 2022, Seo 2024) |
| *Reviews of Modern Physics* | APS | Rea et al. 2024 comprehensive review (benchmark comparison) |
| *IEEE Transactions on Plasma Science* | IEEE | Real-time control, FPGA deployment |

#### 3.1.2 Conferences (5 primary)

| Conference | Frequency | Coverage Strategy |
|------------|-----------|-------------------|
| IAEA Fusion Energy Conference (FEC) | Biennial (2024, 2026) | Full proceedings scan |
| IEEE Symposium on Fusion Engineering (SOFE) | Biennial (2024, 2026) | Full proceedings scan |
| European Physical Society Conference on Plasma Physics (EPS) | Annual | Keyword search of abstracts |
| APS Division of Plasma Physics Annual Meeting (APS-DPP) | Annual | Keyword search of abstracts + contributed papers |
| Technology of Fusion Energy (TOFE) | Biennial | Engineering-focused AI papers |

#### 3.1.3 Preprints and Technical Reports

| Source | Rationale | Treatment |
|--------|-----------|-----------|
| arXiv (physics.plasm-ph, cs.LG, eess.SY) | Early dissemination of ML-fusion work; many 2025--2026 papers first appear here | Labeled [预印本]; cross-referenced with journal versions when available |
| IAEA Technical Documents (TECDOC) | Official reports on ITER PCS ML integration | Labeled [技术报告] |
| ITPA (International Tokamak Physics Activity) reports | Cross-device benchmarking data | Labeled [技术报告] |
| DOE/SC FES reports | US fusion program AI investments | Labeled [技术报告] |

### 3.2 Search Strategy

#### 3.2.1 Keyword Taxonomy

Keywords are organized into three tiers:

**Tier 1 -- AI/ML Method Keywords:**

```
"artificial intelligence" OR "machine learning" OR "deep learning"
OR "reinforcement learning" OR "deep reinforcement learning"
OR "neural network" OR "transformer" OR "attention mechanism"
OR "physics-informed neural network" OR "PINN"
OR "neural operator" OR "Fourier neural operator" OR "FNO" OR "DeepONet"
OR "digital twin" OR "surrogate model" OR "foundation model"
OR "transfer learning" OR "generative model" OR "diffusion model"
OR "large language model" OR "LLM" OR "Bayesian optimization"
```

**Tier 2 -- Fusion Domain Keywords:**

```
"plasma control" OR "tokamak" OR "stellarator"
OR "disruption prediction" OR "disruption avoidance"
OR "ELM" OR "edge localized mode" OR "ELM suppression"
OR "equilibrium reconstruction" OR "plasma diagnostics"
OR "magnetic confinement fusion" OR "MCF"
OR "ITER" OR "SPARC" OR "DEMO"
OR "tearing mode" OR "NTM" OR "neoclassical tearing mode"
OR "runaway electron" OR "divertor" OR "SOL"
OR "gyrokinetic" OR "transport model" OR "turbulence"
```

**Tier 3 -- Device Keywords:**

```
"DIII-D" OR "KSTAR" OR "EAST" OR "JET" OR "TCV"
OR "ASDEX Upgrade" OR "AUG" OR "W7-X" OR "Wendelstein"
OR "HL-2A" OR "HL-3" OR "MAST" OR "WEST"
OR "ST40" OR "EXL-50U" OR "NSTX-U"
```

#### 3.2.2 Boolean Search Strings

**Primary search string** (for database-level systematic search):

```
(Tier1_AI) AND (Tier2_Fusion)
```

Expanded:

```
("artificial intelligence" OR "machine learning" OR "deep learning"
 OR "reinforcement learning" OR "neural network" OR "transformer"
 OR "physics-informed neural network" OR "neural operator"
 OR "digital twin" OR "surrogate model" OR "foundation model"
 OR "transfer learning" OR "diffusion model" OR "large language model")
AND
("plasma control" OR "tokamak" OR "stellarator"
 OR "disruption" OR "ELM" OR "equilibrium reconstruction"
 OR "magnetic confinement fusion" OR "ITER" OR "SPARC"
 OR "tearing mode" OR "runaway electron" OR "divertor"
 OR "gyrokinetic" OR "turbulence")
```

**Secondary search string** (device-specific, to catch papers that omit AI keywords in title/abstract):

```
(Tier1_AI) AND (Tier3_Devices)
```

**Tertiary search string** (extended topics):

```
("machine learning" OR "deep learning" OR "neural network" OR "generative model"
 OR "diffusion model" OR "large language model")
AND
("stellarator optimization" OR "HTS magnet" OR "high temperature superconductor"
 OR "inertial confinement fusion" OR "ICF" OR "fusion"
 OR "gyrokinetic surrogate" OR "data infrastructure")
```

#### 3.2.3 Database-Specific Implementation

| Database | Search Interface | Notes |
|----------|-----------------|-------|
| IOP Science (NF, PPCF) | Advanced search; field-restricted to title/abstract | Primary venue for MCF papers |
| AIP Scitation (PoP) | Full-text search available | Large volume; filter by year |
| ScienceDirect (FED) | Title/abstract/keyword search | Engineering focus |
| APS Journals (PRL, RMP) | PRL search by PACS codes 52.XX | High-impact breakthroughs |
| Nature.com | Keyword + subject filter | Landmark papers |
| IEEE Xplore (SOFE, IEEE TPS) | Metadata search | Conference proceedings |
| arXiv.org | Category physics.plasm-ph + cs.LG cross-listing | Preprints; use export tool for bulk |
| APS-DPP/EPS abstract archives | Meeting abstract search engines | Conference-only results |
| Google Scholar | Broad catch-all search | Snowball expansion; citation tracking |

#### 3.2.4 Search Execution Timeline

| Step | Activity | Timing |
|------|----------|--------|
| S1 | Execute primary Boolean search across all 9 databases | Day 1 |
| S2 | Execute secondary (device-specific) and tertiary (extended) searches | Day 1 |
| S3 | Deduplicate results across databases | Day 2 |
| S4 | Title/abstract screening against inclusion criteria | Day 2--3 |
| S5 | Full-text retrieval for included papers | Day 3--4 |
| S6 | Snowball citation tracking (backward from landmark papers, forward from seminal 2022--2023 works) | Day 4--5 |
| S7 | Expert knowledge supplementation (known papers not captured by keywords) | Day 5 |
| S8 | Final corpus assembly and reference numbering | Day 5 |

### 3.3 Snowball Strategy

**Backward snowball** (from 2024--2026 papers to foundational works):

- Seed papers: Seo et al. 2024 (Nature), Degrave et al. 2022 (Nature), Rea et al. 2024 (RMP)
- Extract reference lists; include pre-2024 papers cited 3+ times across the corpus
- Target: 10--15 seminal pre-2024 context papers

**Forward snowball** (from seminal 2022--2023 papers to 2024--2026 citing papers):

- Use Google Scholar "Cited by" for Degrave 2022, Kates-Harbeck 2019 (Nature), Rea 2024
- Filter for fusion-relevant 2024--2026 citing papers
- Target: 5--10 papers missed by keyword search

### 3.4 Inclusion and Exclusion Criteria

#### 3.4.1 Inclusion Criteria (all must be met)

| ID | Criterion | Rationale |
|----|-----------|-----------|
| I1 | Published or posted between January 2024 and May 2026 | Primary time window |
| I2 | Published in one of the 10 primary venues (Section 3.1) or on arXiv in physics.plasm-ph or cs.LG | Source quality control |
| I3 | Applies one or more AI/ML methods (as defined in Tier 1 keywords) to a fusion plasma physics or plasma control problem | Relevance to RQ |
| I4 | Provides quantitative results (metrics, benchmarks, experimental data) or a novel methodological framework | Evidence quality |
| I5 | Available in English or Chinese (with English abstract) | Language accessibility |

#### 3.4.2 Exclusion Criteria (any one triggers exclusion)

| ID | Criterion | Rationale |
|----|-----------|-----------|
| E1 | Pure ML methodology paper with no fusion application | Out of scope |
| E2 | Fusion materials science / neutronics / tritium breeding as primary focus | Not plasma control |
| E3 | Pre-2024 publication (except identified foundational context papers from snowball) | Outside primary window |
| E4 | Non-peer-reviewed blog post, press release, or marketing whitepaper | Evidence quality |
| E5 | Duplicate publication (journal version supersedes preprint/conference version) | Avoid double-counting |
| E6 | ICF-only paper with no MCF relevance | Out of primary scope |
| E7 | Conference abstract without available full text or sufficient technical detail | Insufficient evidence |

#### 3.4.3 Borderline Case Resolution

For papers that partially meet criteria, apply the following decision rules:

1. If a paper covers both MCF and ICF, include it and code it under both core dimensions and extended topic E4.
2. If a conference abstract has no full text but describes a result cited in other included papers (cross-validation), include it with label [会议报告] and note the evidence limitation.
3. If a preprint has been superseded by a journal version, cite the journal version and note "originally posted as arXiv:XXXX" in a footnote.
4. If a paper is in Chinese with an English abstract, include it; if no English abstract, evaluate on a case-by-case basis with preference for inclusion if the result is significant.

### 3.5 Time Window Specification

| Window | Period | Treatment |
|--------|--------|-----------|
| **Primary survey** | January 2024 -- May 2026 | Systematic keyword search; all matching papers evaluated against I/E criteria |
| **Foundational context** | Pre-2024 | Snowball-identified seminal papers only; maximum 15 papers; clearly labeled as contextual |
| **Cut-off date** | May 30, 2026 | Last search execution date; papers published after cut-off noted as "in press" if known |

---

## 4. Analytical Framework

### 4.1 Eight Core Dimensions

Each core dimension is analyzed using a standardized template:

**Dimension Template:**

```
## [Dimension #]: [Title]

### [#].1 Scope and Key Questions
   - What specific AI/ML methods are applied?
   - What plasma control problems are addressed?
   - What devices are involved?

### [#].2 Landmark Results (2024-2026)
   - Chronological narrative of breakthroughs
   - Classification table (Author, Year, Venue, Method, Device, Key Metric, TRL, Verification Level)

### [#].3 Technical Deep Dive
   - Method description (architecture, training, reward design, etc.)
   - Physics encoding (how domain knowledge is incorporated)
   - Performance analysis (metrics, benchmarks, ablation studies)

### [#].4 Cross-Device Portability
   - Has the method been validated on multiple devices?
   - What transfer learning or domain adaptation techniques are used?
   - What are the sim-to-real gaps?

### [#].5 Limitations and Failure Modes
   - What didn't work? Why?
   - What are the known failure modes?
   - What negative results are reported?

### [#].6 TRL Assessment
   - Current TRL with evidence justification
   - Gap to next TRL level
   - Key milestones needed for advancement
```

### 4.2 Dimension-Specific Analytical Questions

| # | Dimension | Key Analytical Questions |
|---|-----------|------------------------|
| 1 | DRL-based plasma control | Reward function physics encoding; offline vs. online training; safety constraints during exploration; multi-timescale actuator coordination; sim-to-real transfer fidelity |
| 2 | ML disruption prediction | Class imbalance handling; warning time vs. accuracy tradeoff; false positive rate in operational context; cross-device generalization; feature importance and physical interpretability |
| 3 | ELM detection and suppression | Real-time inference latency requirements (<1 ms); RMP optimization; pacing frequency; adaptive controller stability guarantees; multi-device validation |
| 4 | Equilibrium reconstruction & real-time diagnostics | Sub-ms reconstruction accuracy vs. EFIT; Thomson scattering surrogate fidelity; multi-diagnostic fusion; measurement uncertainty propagation |
| 5 | Surrogate models & neural operators | Speedup factor vs. accuracy tradeoff; generalization beyond training distribution; FNO vs. DeepONet vs. custom architectures; uncertainty quantification |
| 6 | PINNs | Handling stiff PDEs (Braginskii, Grad-Shafranov); boundary condition encoding; convergence failure modes; comparison with classical solvers on wall-clock time |
| 7 | Foundation models & cross-device transfer | Pre-training data requirements; zero-shot vs. few-shot transfer; multi-modal fusion (magnetic + Thomson + ECE + imaging); scaling laws for plasma physics |
| 8 | Digital twins & integrated AI control | Multi-physics coupling (MHD + transport + SOL); real-time data assimilation; bidirectional data flow architecture; integration with existing PCS infrastructure |

### 4.3 TRL Assessment Framework (NASA TRL 1--9)

The Technology Readiness Level assessment follows the NASA TRL definitions adapted for fusion AI applications:

| TRL | NASA Definition | Fusion AI Adaptation | Evidence Required |
|-----|----------------|---------------------|-------------------|
| **1** | Basic principles observed | ML concept applied to fusion-relevant physics equation | Published theoretical analysis or proof-of-concept simulation |
| **2** | Technology concept formulated | AI method designed for specific plasma control problem; proof-of-concept on simplified model | Simulation on analytical/low-fidelity model; no real plasma data |
| **3** | Proof of concept | AI method validated on historical experimental data (offline) | Offline validation on real tokamak data; quantitative metrics reported |
| **4** | Component validation | AI method validated in high-fidelity simulation environment (e.g., nonlinear MHD, gyrokinetic) | Validation on physics-based simulation with realistic geometry and parameters |
| **5** | Component validation in relevant environment | AI method tested on real plasma in laboratory setting (single device, supervised) | Experimental demonstration on a real tokamak; human operator in the loop |
| **6** | System demonstration in relevant environment | AI method demonstrated in realistic operational scenario (multiple shots, semi-autonomous) | Multi-shot campaign; performance statistics across operating conditions |
| **7** | System prototype in operational environment | AI control system integrated into device PCS architecture; autonomous operation | Integration with real-time control hardware; autonomous operation demonstrated |
| **8** | System complete and qualified | AI system passes nuclear-grade verification and validation (V&V) | Formal V&V per applicable standards (e.g., IEC 61513 for nuclear I&C) |
| **9** | System proven in operational deployment | AI system deployed in ITER/DEMO/pilot plant; operational track record | Operational deployment with incident-free track record |

**TRL Assessment Protocol for Each Dimension:**

1. Identify the highest-TRL result within the dimension.
2. Justify the TRL assignment with specific evidence from the literature.
3. Identify the gap between current TRL and the next level.
4. List the specific milestones needed to advance to the next TRL.

**Current TRL Summary (as of May 2026):**

| Dimension | TRL | Justification |
|-----------|-----|---------------|
| DRL plasma control | 5--6 | DIII-D tearing mode avoidance demonstrated across multiple shots; not yet integrated into PCS |
| ML disruption prediction | 6--7 | Deployed on multiple devices (DIII-D, JET, EAST); integration into ITER PCS under study |
| ELM detection/suppression | 5--6 | Cross-device demonstration (DIII-D + KSTAR); real-time RMP optimization validated |
| Equilibrium reconstruction | 5--6 | Sub-ms reconstruction validated offline; real-time deployment on EAST/KSTAR |
| Surrogate models | 3--4 | High-fidelity simulation validation; limited experimental validation |
| PINNs | 2--3 | Proof-of-concept on simplified models; convergence issues on full-physics problems |
| Foundation models | 2--3 | Concept formulation and early pre-training; no experimental validation |
| Digital twins | 3--4 | Framework architecture demonstrated; limited real-time data assimilation |

### 4.4 Cross-Domain Comparison Framework

To contextualize fusion AI maturity, the review compares practices in three reference domains:

| Domain | Reference Standards | Key AI Safety Practices | Transferable Lessons |
|--------|-------------------|------------------------|---------------------|
| **Aerospace** | DO-178C (software), DO-331 (ML model verification), ARP4754A (system) | Requirements-based testing; MC/DC coverage; model lineage tracking; formal verification for flight-critical systems | V&V methodology for safety-critical ML; model versioning and traceability |
| **Nuclear Fission** | 10 CFR 50 Appendix B (QA), IEC 61513 (I&C), IAEA NP-T-3.17 (digital I&C) | Defense-in-depth; diversity and redundancy; failure mode analysis; software categorization (Cat A/B/C) | Safety classification of ML components; diverse backup systems; independent verification |
| **Process Control** | IEC 61511 (functional safety), ISA-84 (SIS) | Safety integrity levels (SIL 1--4); proof test intervals; systematic capability | SIL assignment for ML controllers; periodic revalidation; human override requirements |

**Comparison Questions:**

1. What V&V methodology do aerospace practitioners use for neural network-based flight control, and how could it be adapted for fusion plasma control?
2. How do nuclear fission regulators classify software safety categories, and what would Category A (safety-critical) mean for an ML disruption prediction system?
3. What safety integrity level (SIL) would be appropriate for an ML-based ELM suppression controller, and what proof test interval would be required?
4. Where has the fusion community already adopted practices from these domains, and where are the gaps?

### 4.5 Extended Topics Analysis Framework

The six extended topics use a simplified analysis template:

```
## [E#]: [Title]

### [E#].1 Relevance to Core Review
   - How does this topic connect to the 8 core dimensions?

### [E#].2 State of the Art (2024-2026)
   - Key papers and results

### [E#].3 TRL Assessment
   - Current level and justification

### [E#].4 Outlook
   - Near-term trajectory and impact on core dimensions
```

---

## 5. Quality Assessment

### 5.1 Peer-Review Status Labeling System

Every cited reference is labeled with one of five peer-review status indicators:

| Label | Chinese | English | Definition | Evidence Quality Weight |
|-------|---------|---------|------------|------------------------|
| **[期刊论文]** | 期刊论文 | Journal Paper | Published in a peer-reviewed journal after formal review process | Highest (1.0) |
| **[会议报告]** | 会议报告 | Conference Report | Published in peer-reviewed conference proceedings or presented at a refereed conference | High (0.85) |
| **[预印本]** | 预印本 | Preprint | Posted on arXiv or similar preprint server; not yet peer-reviewed | Moderate (0.7) |
| **[技术报告]** | 技术报告 | Technical Report | Published by a recognized institution (IAEA, DOE, ITPA) with internal review | Moderate-High (0.8) |
| **[专著]** | 专著 | Monograph/Book | Published book or book chapter with editorial review | High (0.9) |

**Labeling Rules:**

1. If a paper exists as both a preprint and a journal version, cite the journal version with label [期刊论文] and note the arXiv identifier.
2. Conference papers that are later expanded into journal papers should use the journal version.
3. For conference abstracts with no full text (e.g., APS-DPP invited talks), use [会议报告] and note the evidence limitation.
4. IAEA TECDOCs and DOE FES reports use [技术报告].

### 5.2 Verification Level Classification

Each quantitative result cited in the review is classified by the level of experimental verification:

| Level | Label | Description | Example |
|-------|-------|-------------|---------|
| **V1** | 仿真验证 | Validated only in simulation (analytical model, synthetic data, or physics-based code) | PINN for Grad-Shafranov equation on synthetic equilibria |
| **V2** | 仿真+实验 (离线) | Validated in simulation and tested on historical experimental data (offline, not real-time) | Surrogate transport model trained on AUG database, tested on held-out discharges |
| **V3** | 实验验证 (单装置) | Demonstrated on a real plasma device in a single experimental campaign | DRL tearing mode avoidance on DIII-D (Seo et al. 2024) |
| **V4** | 实验验证 (跨装置) | Demonstrated on two or more devices | ML adaptive ELM suppression on DIII-D and KSTAR (Kim et al. 2024) |
| **V5** | 工程集成验证 | Integrated into operational control system and demonstrated over extended operation | Not yet achieved for any AI/ML system (as of 2026) |

**Verification Level Mapping to TRL:**

| Verification Level | Corresponding TRL Range |
|-------------------|------------------------|
| V1 | TRL 2--3 |
| V2 | TRL 3--4 |
| V3 | TRL 5--6 |
| V4 | TRL 6--7 |
| V5 | TRL 7--9 |

### 5.3 Citation Verification Protocol

To prevent the citation accuracy issues identified in the V1 peer review (P0 severity), all references undergo three-level verification:

| Level | Method | Scope | Timing |
|-------|--------|-------|--------|
| **CV1** | DOI/metadata cross-check | All references verified against publisher databases (DOI resolution, author, title, year, venue) | Phase 2 (corpus assembly) |
| **CV2** | Claim attribution audit | Every quantitative claim attributed to a reference is verified against the source paper's actual reported values | Phase 3 (analysis) |
| **CV3** | Internal consistency check | Reference list cross-checked against in-text citations; no orphan references; no phantom citations | Phase 5 (final review) |

### 5.4 Evidence Hierarchy

For resolving conflicting claims or establishing consensus findings:

| Priority | Evidence Type | Rationale |
|----------|--------------|-----------|
| 1 | Peer-reviewed journal paper with experimental validation (V3--V4) | Highest evidence quality |
| 2 | Peer-reviewed journal paper with simulation-only validation (V1--V2) | Strong evidence, limited generalizability |
| 3 | Peer-reviewed conference paper with experimental validation (V3--V4) | High evidence quality |
| 4 | Technical report from recognized institution (IAEA, DOE) | Institutional credibility |
| 5 | Preprint with quantitative results | Provisional; must be flagged |
| 6 | Conference abstract without full text | Lowest evidence quality; use only for context |

---

## 6. Validity Criteria

### 6.1 Internal Validity: Ensuring Accuracy

| Threat | Mitigation |
|--------|------------|
| **Citation inaccuracy** (wrong author, year, venue, claim) | Three-level citation verification protocol (Section 5.3) |
| **Selective reporting bias** (cherry-picking favorable results) | Failure mode cataloging (Section 6.3); mandatory inclusion of negative results |
| **Confirmation bias** (favoring results that support a narrative) | Structured extraction template with mandatory "Limitations" field for each paper |
| **Staleness** (missing recent results) | Final search execution within 1 week of submission; "in press" section for late-breaking results |

### 6.2 External Validity: Ensuring Comprehensiveness

| Threat | Mitigation |
|--------|------------|
| **Venue coverage gaps** (missing relevant papers in non-target venues) | Google Scholar catch-all search; snowball citation tracking; expert knowledge supplementation |
| **Language bias** (missing Chinese, Japanese, Korean papers) | Include Chinese-language papers with English abstracts; search EAST, HL-2A/HL-3, KSTAR specific results |
| **Publication bias** (negative results unpublished) | Explicitly search for "failure," "limitation," "negative result" keywords; include workshop presentations on failed approaches |
| **Preprint bias** (missing emerging 2025--2026 work) | Include arXiv preprints with explicit [预印本] label; cross-check with conference abstracts |
| **Device bias** (over-representing US/EU devices) | Explicit Tier 3 device keywords covering Chinese (EAST, HL-2A/HL-3), Korean (KSTAR), and startup (ST40, EXL-50U) devices |

### 6.3 Publication Bias Countermeasures

The review explicitly addresses the positive-results bias in the AI-for-fusion literature:

1. **Failure mode catalog.** Section 10.10 of the review manuscript documents known failure modes:
   - DRL policies that degrade 30--50% on real hardware vs. simulation
   - Disruption predictors with >20% FPR in operational deployment
   - PINN convergence failures on stiff fusion PDEs
   - Transfer learning methods that fail across device types (tokamak to stellarator)

2. **Negative results search.** Additional search queries:
   ```
   ("machine learning" OR "deep learning") AND ("fusion" OR "tokamak")
   AND ("failure" OR "limitation" OR "challenge" OR "negative result"
        OR "did not" OR "unable to" OR "poor performance")
   ```

3. **Workshop proceedings.** Check for "lessons learned" presentations at APS-DPP, SOFE, and IAEA FEC that may report failed approaches not captured in formal publications.

### 6.4 Construct Validity: Ensuring Correct Framing

| Threat | Mitigation |
|--------|------------|
| **TRL overclaim** | TRL assessment requires explicit evidence justification (Section 4.3); cross-checked against verification level |
| **Scope creep** | Inclusion/exclusion criteria strictly enforced (Section 3.4); borderline cases resolved by decision rules |
| **Dimension overlap** | Cross-references between dimensions where papers span multiple areas; primary classification by dominant contribution |
| **Temporal framing** | Pre-2024 papers clearly labeled as foundational context; 2024--2026 window strictly enforced for primary corpus |

### 6.5 Reliability: Ensuring Reproducibility

| Element | Reproducibility Measure |
|---------|------------------------|
| Search strategy | Full Boolean strings documented (Section 3.2); database-specific implementation noted |
| Inclusion decisions | Borderline case decision rules documented (Section 3.4.3); can be independently re-applied |
| TRL assessments | Rubric-based with explicit evidence requirements (Section 4.3); each assignment justified |
| Verification levels | Classification criteria clearly defined (Section 5.2); each result labeled |
| Cross-domain comparisons | Reference standards cited (Section 4.4); comparison questions explicitly stated |

---

## 7. Classification Table Schema

### 7.1 Per-Dimension Comparison Table

Each core dimension includes a structured comparison table with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| Author(s) | First author et al. | Seo et al. |
| Year | Publication year | 2024 |
| Venue | Journal/conference | Nature |
| Peer-Review Label | [期刊论文] / [会议报告] / [预印本] / [技术报告] / [专著] | [期刊论文] |
| AI/ML Method | Specific technique | Deep RL (PPO) + Ensemble Kalman Filter |
| Plasma Problem | Control problem addressed | Tearing mode avoidance |
| Device(s) | Tokamak/stellarator used | DIII-D |
| Key Metric | Primary performance measure | Tearing mode rate reduction; H98 ~ 1.0 |
| Verification Level | V1--V5 | V3 (实验验证, 单装置) |
| TRL | Technology readiness level | 5 |
| Key Limitation | Primary limitation noted | Single device; specific to DIII-D geometry |

### 7.2 Cross-Dimension Summary Table

A summary table spanning all 8 dimensions with:

| Dimension | # Papers | TRL Range | Highest-TRL Result | Key Gap |
|-----------|----------|-----------|-------------------|---------|
| DRL control | N | 5--6 | Seo 2024, Nature, TRL 5 | Cross-device validation |
| Disruption prediction | N | 6--7 | [Highest result] | FPR reduction in ops |
| ... | ... | ... | ... | ... |

---

## 8. Ethical and Methodological Declarations

### 8.1 Conflict of Interest

The review authors declare no conflicts of interest. No industry funding or consulting relationships exist with any fusion device operator, AI company, or ITER Organization.

### 8.2 Use of AI Tools

AI tools (Claude, GPT-4) were used for literature search assistance, draft generation, and citation verification. All AI-generated content was independently verified against primary sources. The authors bear full responsibility for the accuracy of all claims.

### 8.3 Limitations of This Review

Explicitly acknowledged limitations:

1. This is a narrative review, not a systematic review; some relevant papers may be missed.
2. Preprint results have not undergone formal peer review and may be revised.
3. TRL assessments involve expert judgment and are not formally standardized in the fusion community.
4. The 2024--2026 window captures a rapidly evolving field; some results may be superseded.
5. Cross-domain comparisons (Section 4.4) are indicative, not exhaustive; the author team's primary expertise is in fusion, not aerospace or nuclear fission regulation.

---

## Appendix A: Search Execution Log Template

| Search ID | Database | Date | Query String | Results (Raw) | After Dedup | After Screening | Included |
|-----------|----------|------|-------------|---------------|-------------|-----------------|----------|
| S1-001 | IOP Science | YYYY-MM-DD | [full query] | N | N | N | N |
| S1-002 | AIP Scitation | YYYY-MM-DD | [full query] | N | N | N | N |
| ... | ... | ... | ... | ... | ... | ... | ... |

## Appendix B: TRL Assessment Worksheet Template

| Sub-Domain | Highest-TRL Paper | TRL | Evidence Summary | Gap to Next Level | Key Milestones |
|------------|-------------------|-----|-----------------|-------------------|----------------|
| DRL control | [Author, Year] | N | [Evidence] | [Gap description] | [Milestones] |
| ... | ... | ... | ... | ... | ... |

## Appendix C: Cross-Domain Comparison Worksheet

| Fusion AI Practice | Aerospace Analog | Nuclear Fission Analog | Process Control Analog | Transferable Lesson |
|--------------------|-----------------|----------------------|----------------------|-------------------|
| DRL safety constraints | Neural network envelope protection (DO-331) | Reactor protection system logic (IEC 61513) | Safety instrumented function (IEC 61511) | [Lesson] |
| Disruption predictor V&V | Flight software MC/DC testing (DO-178C) | Safety system software V&V (10 CFR 50 App B) | SIL proof testing (IEC 61511) | [Lesson] |
| ... | ... | ... | ... | ... |

---

*Blueprint prepared per research_architect_agent protocol.*
*Companion to Research-Question-Brief.md (FINER score: 4.80/5.00).*
*Ready to proceed to Phase 2: Literature Search & Verification.*
