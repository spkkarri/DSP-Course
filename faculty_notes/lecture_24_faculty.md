<Faculty Notes — Lecture 24: FIR Design: Frequency-Sampling Method>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY
The Frequency-Sampling Method designs an FIR filter by directly sampling the desired continuous frequency response $H_d(e^{j\omega})$ at $N$ uniform frequency points $\omega_k = \frac{2\pi k}{N}$ and computing the filter coefficients $h[n]$ via Inverse DFT.

**Pedagogical Strategy:**
1. Formulate the Frequency-Sampling equations: $H[k] = |H_d(e^{j 2\pi k / N})| e^{-j \frac{N-1}{2} \frac{2\pi k}{N}}$.
2. Apply the IDFT synthesis formula to calculate real impulse response coefficients $h[n]$.
3. Explain the primary drawback of basic frequency sampling: Between sampled points, the frequency response ripples significantly, yielding poor stopband attenuation ($\approx -16\text{ dB}$).
4. Demonstrate **Transition Band Optimization**: By placing one or two unconstrained optimization variables $T_1, T_2 \in (0, 1)$ in the transition band, stopband attenuation is dramatically increased to over $-45\text{ dB}$ (1 transition sample) or $-75\text{ dB}$ (2 transition samples).

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Sample** desired frequency responses $H_d(e^{j\omega})$ with proper linear-phase phase assignments.
2. **Compute** FIR filter coefficients $h[n]$ via IDFT formulation.
3. **Optimize** transition band samples to maximize stopband attenuation.
4. **Compare** the Frequency-Sampling method with the Windowing method.

---
## 2. MATHEMATICAL FOUNDATIONS

### 2.1 Frequency-Sampling Design Equations
Let $H[k] = H_d(e^{j \frac{2\pi k}{N}})$. For a linear-phase FIR filter of length $N$:
$$ H[k] = |H[k]| e^{j \angle H[k]}, \quad \angle H[k] = -\left( \frac{N-1}{2} \right) \frac{2\pi k}{N} $$
The impulse response is computed by the IDFT:
$$ h[n] = \frac{1}{N} \sum_{k=0}^{N-1} H[k] e^{j \frac{2\pi k n}{N}} $$
Exploiting Hermitian symmetry ($H[N-k] = H^*[k]$):
* **For $N$ Odd:**
  $$ h[n] = \frac{H[0]}{N} + \frac{2}{N} \sum_{k=1}^{(N-1)/2} |H[k]| \cos\left[ \frac{2\pi k}{N} \left( n - \frac{N-1}{2} \right) \right] $$
* **For $N$ Even:**
  $$ h[n] = \frac{H[0]}{N} + \frac{2}{N} \sum_{k=1}^{N/2 - 1} |H[k]| \cos\left[ \frac{2\pi k}{N} \left( n - \frac{N-1}{2} \right) \right] + \frac{H[N/2]}{N} (-1)^n $$

### 2.2 Transition Sample Optimization Values

| Number of Transition Samples | Optimized Sample Values | Resulting Stopband Attenuation $A_s$ |
| :---: | :---: | :---: |
| **0 (No transition band)** | None ($H[k] \in \{0, 1\}$) | $-16$ dB |
| **1 Transition Sample** | $T_1 \approx 0.38$ | $-45$ dB |
| **2 Transition Samples** | $T_1 \approx 0.59, \; T_2 \approx 0.11$ | $-75$ dB |
| **3 Transition Samples** | $T_1 \approx 0.70, \; T_2 \approx 0.25, \; T_3 \approx 0.02$ | $-95$ dB |

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 24.1: Frequency-Sampling Lowpass Filter Design
**Problem:** Design a 7-point ($N=7$) linear-phase FIR lowpass filter with frequency samples:
$$ |H[k]| = \{ 1, 1, 0, 0, 0, 0, 1 \} \quad \text{for } k = 0, 1, 2, 3, 4, 5, 6 $$

**Solution:**
* Length $N = 7$ (Odd), $\tau = \frac{7-1}{2} = 3$.
* Non-zero samples: $|H[0]| = 1, \; |H[1]| = |H[6]| = 1$.
* Using the real summation formula:
  $$ h[n] = \frac{H[0]}{7} + \frac{2}{7} |H[1]| \cos\left[ \frac{2\pi (1)}{7} (n - 3) \right] = \frac{1}{7} + \frac{2}{7} \cos\left[ \frac{2\pi}{7} (n - 3) \right] $$
  * $h[3] = \frac{1}{7} + \frac{2}{7} \cos(0) = \frac{3}{7} \approx 0.4286$
  * $h[2] = h[4] = \frac{1}{7} + \frac{2}{7} \cos\left( \frac{2\pi}{7} \right) = \frac{1 + 2(0.6235)}{7} = \frac{2.2470}{7} \approx 0.3210$
  * $h[1] = h[5] = \frac{1}{7} + \frac{2}{7} \cos\left( \frac{4\pi}{7} \right) = \frac{1 + 2(-0.2225)}{7} = \frac{0.5550}{7} \approx 0.0793$
  * $h[0] = h[6] = \frac{1}{7} + \frac{2}{7} \cos\left( \frac{6\pi}{7} \right) = \frac{1 + 2(-0.9010)}{7} = \frac{-0.8019}{7} \approx -0.1146$
$$ h[n] = \{ \underset{\uparrow}{-0.1146}, 0.0793, 0.3210, 0.4286, 0.3210, 0.0793, -0.1146 \} $$

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
**(a)** Derive the Frequency-Sampling design formula for an odd-length linear-phase FIR filter. *(8 Marks)*
**(b)** Explain why transition band samples are introduced in the Frequency-Sampling method. How do they affect the passband ripple and stopband attenuation? *(7 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Part (a):**
  * Mathematical derivation using IDFT and Euler's formula *(8 Marks)*
* **Part (b):**
  * Explanation of interpolation ripple between sharp 1-to-0 transitions *(3 Marks)*
  * Role of transition samples $T_1, T_2$ in smoothing frequency gradient and boosting $A_s$ from $16\text{ dB}$ to $>45\text{ dB}$ *(4 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import numpy as np

N = 7
H = np.array([1, 1, 0, 0, 0, 0, 1], dtype=complex)
# Apply linear phase
k = np.arange(N)
H_phase = H * np.exp(-1j * ((N - 1) / 2) * 2 * np.pi * k / N)
h = np.fft.ifft(H_phase).real
print("Frequency Sampling Coefficients h[n]:", np.round(h, 4))
```
