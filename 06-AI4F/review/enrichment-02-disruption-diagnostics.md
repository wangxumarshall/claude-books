# Enrichment Content: Disruption + Diagnostics

## 1. Kates-Harbeck et al. (2019) Nature — FRNN
Kates-Harbeck et al. developed the Fusion Recurrent Neural Network (FRNN), combining LSTMs for temporal pattern recognition with CNNs for spatial feature extraction, trained on combined databases from DIII-D, JET, and EAST. The system achieved >95% true positive rates with <1% false positive rates, providing disruption warnings tens of milliseconds before onset. A landmark result was the demonstration of cross-machine generalization, wherein models trained on one tokamak successfully predicted disruptions on a different device, establishing that disruption precursors encode device-independent physics. The FRNN framework set the benchmark against which all subsequent ML-based disruption predictors are measured.

## 2. Poels et al. (2025) Nuclear Fusion — VAE Disruptivity
Poels et al. introduced a multimodal VAE for plasma state monitoring with a Fourier Neural Operator encoder and Gaussian mixture prior (K=8). Trained on ~1,600 TCV discharges, the model learns a 2D latent representation from which a calibrated disruption risk variable D_risk emerges, deviating from actual disruption rates by only ~3% on training data. Despite using no confinement labels during training, the latent space naturally separates L-mode and H-mode states (83.9% vs. 15.0%). The method provides interpretable, continuous indicators of disruption proximity rather than binary predictions.

## 3. Bandyopadhyay et al. (2025) Nuclear Fusion — ITPA Review
Bandyopadhyay et al. produced the comprehensive ITPA review on MHD stability, disruptions, and control, synthesizing over 1.5 decades of progress with contributions from over 60 co-authors spanning ~15 countries. The review documents advances in sawtooth control, NTM suppression via ECCD, RWM stabilization, and the transition toward shattered pellet injection. Critically, the review formally elevates AI/ML-based disruption prediction to a major subfield, establishing that disruption management "remains probably the most active field of R&D globally." With over 9,500 downloads, this serves as the definitive physics basis for ITER and DEMO operations.

## 4. Arnaud et al. (2025) Nuclear Fusion — Runaway Electron Surrogate
Arnaud et al. developed a PINN surrogate that predicts the exponential avalanche growth rate of runaway electrons for plasmas containing partially ionized impurities — the first such surrogate to incorporate partial screening effects. The PINN solves the adjoint of the relativistic Fokker-Planck equation and embeds steady-state power balance with atomic physics data, reducing the parameter space from five to three dimensions. Loss decreased by ~9 orders of magnitude for fixed-parameter cases. A novel closure using an exponentially decaying avalanche distribution substantially improves growth rate predictions near marginality compared to the standard Rosenbluth-Putvinski approach.

## 5. Zheng et al. (2025) Nuclear Fusion — EFIT-mini
Zheng et al. developed EFIT-mini, strategically integrating neural networks with physical simulation rather than replacing the entire pipeline. The architecture uses neural networks only for the most numerically challenging steps while retaining parallelizable operations. Trained on 355 shots and 206,543 time slices from EXL-50U, EFIT-mini achieves >98% overlap ratio in LCFS reconstruction at 129×129 resolution in only 0.36 ms — ~1000× faster than offline EFIT. It successfully drove PID feedback control on shots far outside the training distribution.

## 6. Carey et al. (2025) Nuclear Fusion — Neural Operators for Edge
Carey et al. investigated FNOs as surrogate models for JOREK MHD and STORM turbulence. Key finding: error spikes during long rollouts were non-monotonic and correlated with specific physical transitions such as blob-wall collisions. Transfer learning from low- to high-fidelity datasets achieved ~1 order of magnitude error reduction for small datasets. Heat flux predictions showed strong correlation (Pearson 0.95) but systematically underestimated high-flux events.

## 7. Davies et al. (2025) PRL — Universal Plasma Representation
Davies et al. developed a self-supervised learning framework to create universal plasma state representations from multi-machine tokamak data, enabling zero-shot transfer between devices without device-specific calibration. The learned representation captures device-independent physics features that generalize across different experimental setups, providing a foundation for transfer learning, anomaly detection, and cross-machine benchmarking.

## 8. Dasbach et al. (2026) — SOLPS-NN
Dasbach et al. developed SOLPS-NN trained on several thousand SOLPS-ITER simulations. Key finding: simple fully connected neural networks outperformed more complex alternatives, and independent models for different observables yielded higher accuracy than predicting the whole spatial domain simultaneously.

## 9. Zhu et al. (2025) Phys. Plasmas — Latent-Space Detachment
Zhu et al. developed latent-space mapping models trained on UEDGE databases for real-time divertor detachment prediction, achieving orders-of-magnitude speedup over full 2D edge transport simulations. The approach uses autoencoder-based dimensionality reduction to compress the high-dimensional divertor plasma state into a compact latent representation.
