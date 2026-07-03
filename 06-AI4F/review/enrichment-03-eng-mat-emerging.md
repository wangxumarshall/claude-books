# Enrichment Content: Engineering + Materials + Emerging

## 1. Griffiths et al. (2025) — Bayesian Networks for FPP
Griffiths et al. developed a Bayesian network meta-model (BNM) for techno-economic assessment of a fusion pilot plant based on Tokamak Energy's spherical tokamak concept. The methodology employs a seven-step framework: a deterministic whole-plant systems code (PyTOK) generates 10,420 quasi-random samples across four input parameters (major radius, aspect ratio, effective ion charge, toroidal field), which are discretized into conditional probability tables using the PyBBN library, enabling bi-directional probabilistic inference rather than deterministic point estimates. The approach is significant as the first application of a BNM for decision support in a real-world fusion case study. Reverse inference reveals that major radius is the dominant economic driver: increasing R by roughly 1 m could potentially double capital cost from 4.7 to 8.4 billion USD, with the posterior concentrating between R = 3.02-3.30 m at the target cost range.

## 2. Muraca et al. (2025) — SPARC H-mode Modeling
Muraca et al. constructed an extensive database of SPARC H-mode confinement predictions using the ASTRA transport solver coupled with TGLF SAT2 and a neural network ensemble trained on over 11,000 EPED simulations. For the PRD at 11 MW auxiliary power, 74% of simulations converged and all converged points achieved Q > 2, with nearly all reaching burning plasma conditions (Q > 5). The study underscores that tungsten concentration and H-mode sustainment are the most critical uncertainties.

## 3. Morosohk et al. (2025) — Real-time Te Profile Control
Morosohk et al. reported the first experimental demonstration of real-time electron temperature profile feedback control on DIII-D, integrating neural network surrogates (NubeamNet for NBI and MMMnet for anomalous thermal diffusivity, each executing in ~1 ms) into the Plasma Control System alongside an extended Kalman filter. The controller achieved observer-to-Thomson agreement with r-squared values exceeding 0.89.

## 4. Byggmastar et al. (2024) — MLIP for Tungsten
Byggmastar et al. developed MLIPs for tungsten trained on DFT data including high-energy collision cascades and point defect configurations. Moment tensor potentials reproduced DFT-quality defect formation energies within 0.1 eV, a significant advance over traditional empirical potentials.

## 5. Roy et al. (2026) — MLIP Benchmarking
Roy et al. conducted a systematic comparison of six MLIP frameworks (DeePMD, MTP, GAP, ACE, MACE) for radiation-damage simulations in fusion-relevant ceramics, providing the first comprehensive user-perspective benchmark for this critical materials class.

## 6. Zhu et al. (2025) — Foundation Models
Zhu et al. developed transformer-based foundation models pre-trained on diverse plasma physics simulation data spanning gyrokinetic, MHD, and transport domains, demonstrating transfer learning to multiple downstream tasks including disruption prediction and turbulence classification.

## 7. Boschi et al. (2026) — TokaMind
Boschi et al. proposed TokaMind, the first dedicated multi-modal transformer foundation model for tokamak plasma dynamics, trained on MAST diagnostics. The model handles multiple data modalities including time-series signals, 2D radial profiles, and video data, incorporating missing-signal handling and a training-free DCT3D embedding.

## 8. Joglekar et al. (2026) — Differentiable Programming
Joglekar et al. demonstrated that differentiable programming provides a unified framework for gradient-based optimization spanning discovery, multi-scale modeling, diagnostics, and inverse design. Applied across four domains: discovering superadditive wavepacket interactions, learning hidden variables for fluid-kinetic bridging, accelerating Thomson scattering by 140x, and designing spatiotemporal laser pulses with 15x improvement.

## 9. Gahle & Barbarino (2026) — IAEA Fusion Data Lake
The IAEA Fusion Data Lake involves 24 institutions across 11 countries, comprising an international data catalogue, centralized storage, and a data federation connecting fusion platforms worldwide, aligned with FAIR principles.

## 10. Citrin et al. (2024) — TORAX
Citrin et al. presented TORAX, an open-source differentiable tokamak core transport simulator in JAX, solving coupled PDEs for ion/electron heat transport, particle transport, and current diffusion. JIT compilation provides fast runtimes and automatic differentiation enables gradient-based optimization.
