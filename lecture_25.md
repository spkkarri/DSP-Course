# Lecture 25: Moving-Average Filters & Comparison of FIR vs. IIR Filters
## EE3621: Digital Signal Processing | III B.Tech EEE

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Analyze** the frequency selectivity and pole-zero placement of Moving Average and Comb filters.
2. **Compare** FIR and IIR digital filters across all architectural and algorithmic metrics.
3. **Select** the optimal filter topology for specific application constraints (latency, phase linearity, computational budget).

---
## 2. MATHEMATICAL FOUNDATIONS

### 2.1 Moving Average Filter
$$ y[n] = \frac{1}{M} \sum_{k=0}^{M-1} x[n-k] \implies H(z) = \frac{1 - z^{-M}}{M(1 - z^{-1})} $$
$$ H(e^{j\omega}) = \frac{1}{M} \frac{\sin(\omega M / 2)}{\sin(\omega / 2)} e^{-j\omega(M-1)/2} $$
* $M-1$ zeros are located on the unit circle at $z = e^{j 2\pi k / M}$ for $k = 1, 2, \dots, M-1$.
* The pole at $z=1$ exactly cancels the zero at $z=1$.

### 2.2 Comprehensive FIR vs. IIR Comparison Matrix

| Engineering Metric | FIR Filter | IIR Filter |
| :--- | :--- | :--- |
| **Phase Response** | Can guarantee **strictly linear phase** ($\tau_g = \text{const}$) | Inherently **non-linear phase** (phase distortion) |
| **Stability** | **Always BIBO stable** (All poles at origin $z=0$) | Must be tested; poles can migrate outside $|z|=1$ |
| **Filter Order** | **High order** required for sharp transition bands | **Low order** (5$\times$ to 10$\times$ lower than FIR) |
| **Computational Cost** | High MAC count per sample | Low MAC count (extremely efficient) |
| **Hardware Realization** | Non-recursive (no feedback loops); pipelineable | Recursive (feedback loops); accumulator bottlenecks |
| **Quantization Effects** | Low sensitivity; free from feedback limit cycles | High sensitivity; susceptible to limit cycles & overflow |
| **Analog Emulation** | Cannot easily emulate analog prototypes | Directly designed from analog Butterworth/Chebyshev |

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 25.1: Order Estimation Comparison (FIR vs. IIR)
**Problem:** Estimate the required filter order for an FIR filter (Kaiser) vs. an IIR filter (Butterworth) to meet:
$\omega_p = 0.4\pi, \; \omega_s = 0.5\pi, \; A_p = 0.5\text{ dB}, \; A_s = 50\text{ dB}$.

**Solution:**
* **FIR (Kaiser Formula):**
  $\Delta f = \frac{0.5\pi - 0.4\pi}{2\pi} = 0.05$.
  $N_{\text{FIR}} \approx \frac{50 - 7.95}{14.36 \times 0.05} + 1 = \frac{42.05}{0.718} + 1 = 58.56 + 1 \approx \mathbf{60 \text{ taps}}$.
* **IIR (Butterworth Order Formula):**
  Prewarping / prototype ratio: $\frac{\Omega_s}{\Omega_p} = \frac{\tan(0.25\pi)}{\tan(0.2\pi)} = \frac{1.0}{0.7265} = 1.3764$.
  $N_{\text{IIR}} = \left\lceil \frac{\log_{10}[(10^{5} - 1)/(10^{0.05} - 1)]}{2\log_{10}(1.3764)} \right\rceil = \left\lceil \frac{\log_{10}(100000 / 0.122)}{2 \times 0.1387} \right\rceil = \left\lceil \frac{5.9136}{0.2774} \right\rceil = \mathbf{22 \to 12 \text{ (BLT)}}$.
* **Takeaway:** The IIR filter requires $\approx 6$ biquad sections (12 poles), needing significantly fewer MAC operations per sample than the 60-tap FIR filter.

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
**(a)** Provide a detailed comparative analysis between FIR and IIR digital filters covering Phase Linearity, Stability, Computational Complexity, and Hardware Implementation. *(10 Marks)*
**(b)** Under what practical engineering scenarios is an FIR filter mandatory over an IIR filter? *(5 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Part (a):** Comprehensive comparison matrix covering all 7 parameters listed in Section 2.2 *(10 Marks)*
* **Part (b):** 1. Digital Communications (preventing Intersymbol Interference), 2. High-Fidelity Audio processing (preserving transient phase coherence), 3. Biomedical ECG/EEG diagnostic monitoring (preventing distortion of QRS peak morphology) *(5 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import scipy.signal as signal

# Order comparison
N_fir, beta = signal.kaiserord(50, 0.1)
N_iir, Wn = signal.buttord(0.4, 0.5, 0.5, 50)
print(f"Required FIR Order: {N_fir}")
print(f"Required IIR Order: {N_iir}")
```
