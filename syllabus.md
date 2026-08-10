# EE3621 — Digital Signal Processing

## 30-Lecture Plan (III B.Tech EEE)

### Unit I — Basic Elements of DSP (L1–L7) &rarr; CO1, CO2
* **L1**: Course intro, DSP vs analog processing; review of DT signals, classification, elementary sequences
* **L2**: LTI systems, convolution sum, causality/stability; difference equations
* **L3**: DTFT — definition, existence, properties (linearity, shifting, convolution)
* **L4**: Frequency response of LTI systems; magnitude/phase response, group delay
* **L5**: Z-transform — definition, ROC, properties; common transform pairs
* **L6**: Inverse Z-transform (partial fraction, power series); poles/zeros, stability from ROC; system function $H(z)$
* **L7**: DFT — definition, relation to DTFT/DFS, matrix formulation

---

### Unit II — Fast Fourier Transforms (L8–L14) &rarr; CO2, CO3
* **L8**: DFT properties — periodicity, symmetry, circular shift, circular convolution
* **L9**: Linear vs circular convolution; computational cost of direct DFT — motivation for FFT
* **L10**: Radix-2 DIT-FFT — signal flow graph, butterfly, bit reversal
* **L11**: Radix-2 DIF-FFT — derivation, comparison with DIT; in-place computation
* **L12**: Radix-4 FFT; comparison of computational complexity
* **L13**: FFT in linear filtering — overlap-add method
* **L14**: Overlap-save method; reconstruction and aliasing in time and frequency domains

---

### Unit III — Digital Filter Synthesis / Structures (L15–L20) &rarr; CO4
* **L15**: Filter realization basics; FIR direct form and cascade form
* **L16**: Linear-phase FIR realization; frequency-sampling structure
* **L17**: IIR — direct form I and direct form II (and transposed forms)
* **L18**: IIR cascade realization; pole-zero pairing and ordering
* **L19**: IIR parallel realization
* **L20**: Lattice and lattice-ladder structures; finite word-length effects (brief)

---

### Unit IV — Digital Filter Design (L21–L30) &rarr; CO5
* **L21**: FIR specifications; linear phase conditions, four types, location of zeros
* **L22**: Windowing method — rectangular, Bartlett, Hann; Gibbs phenomenon
* **L23**: Hamming, Blackman, Kaiser windows; design examples (LPF/HPF)
* **L24**: Frequency-sampling method for FIR design
* **L25**: Moving-average filters and other simple FIR filters; comparison FIR vs IIR
* **L26**: Analog filter review (Butterworth/Chebyshev prototypes) for IIR design
* **L27**: Impulse-invariance method — derivation, aliasing limitation, example
* **L28**: Bilinear transformation — frequency warping, prewarping, design example
* **L29**: Matched z-transform; complete IIR design example (LPF &rarr; BPF via transformation)
* **L30**: Applications: channel equalization, adaptive noise cancellation, adaptive FIR (LMS); revision and CO mapping
