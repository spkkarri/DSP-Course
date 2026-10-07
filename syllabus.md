# EE3621 — Digital Signal Processing

## 26-Lecture Plan (III B.Tech EEE)

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
* **L16**: FIR filter - linear phase realization
* **L17**: IIR filter - direct form I and direct form II realization
* **L18**: IIR filter - cascade form realization
* **L19**: IIR filter - parallel form realization
* **L20**: IIR filter - Lattice form realization

---

### Unit IV — Digital Filter Design (L21–L26) &rarr; CO5
* **L21**: Linear phase FIR filter, characteristic response, location of zeros & moving average filters
* **L22**: Design of FIR filter - windowing method
* **L23**: Design of FIR filter - frequency sampling
* **L24**: Design of IIR filters from analog filters - Impulse invariance
* **L25**: Design of IIR filters - Bilinear transformation, matched z-transform & simple design example
* **L26**: Equalization, noise cancellation and adaptive FIR filter
