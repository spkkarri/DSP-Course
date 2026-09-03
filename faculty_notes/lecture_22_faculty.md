<Faculty Notes — Lecture 22: FIR Design: Windowing (Rect, Bartlett, Hann)>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY
The Window Method is the classical analytical approach to FIR filter design. Starting from an ideal brick-wall frequency response $H_d(e^{j\omega})$, its infinite non-causal impulse response $h_d[n]$ is truncated and smoothed using a finite window function $w[n]$.

**Pedagogical Strategy:**
1. Derive the ideal lowpass impulse response: $h_d[n] = \frac{\sin(\omega_c (n - \tau))}{\pi (n - \tau)}$ where $\tau = \frac{N-1}{2}$.
2. Explain the **Gibbs Phenomenon**: Truncating with a rectangular window causes 8.95% peak overshoot at band edges, which does not vanish even as $N \to \infty$.
3. Analyze the fundamental trade-off: **Mainlobe width (transition bandwidth) vs. Sidelobe level (stopband attenuation)**.
4. Define and analyze Rectangular, Bartlett (triangular), and Hann (Hanning) windows.
5. Complete step-by-step filter design numericals.

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Derive** ideal impulse responses $h_d[n]$ for Lowpass, Highpass, Bandpass, and Bandstop filters.
2. **Explain** the origins and mathematical properties of the Gibbs phenomenon.
3. **Design** linear-phase FIR filters using Rectangular, Bartlett, and Hann windows to meet transition bandwidth and attenuation specs.
4. **Evaluate** the frequency spectrum of window functions.

---
## 2. MATHEMATICAL FOUNDATIONS

### 2.1 Ideal Filter Impulse Responses ($\tau = \frac{N-1}{2}$)
* **Lowpass ($\omega_c$):**
  $$ h_{d,\text{LP}}[n] = \frac{\sin(\omega_c(n - \tau))}{\pi(n - \tau)} $$
* **Highpass ($\omega_c$):**
  $$ h_{d,\text{HP}}[n] = \delta[n - \tau] - \frac{\sin(\omega_c(n - \tau))}{\pi(n - \tau)} $$
* **Bandpass ($\omega_{c1}, \omega_{c2}$):**
  $$ h_{d,\text{BP}}[n] = \frac{\sin(\omega_{c2}(n - \tau))}{\pi(n - \tau)} - \frac{\sin(\omega_{c1}(n - \tau))}{\pi(n - \tau)} $$

### 2.2 Window Functions Formulation ($0 \le n \le N-1$)
1. **Rectangular Window:**
   $$ w[n] = 1, \quad \Delta\omega = \frac{4\pi}{N}, \quad \text{Peak Sidelobe: } -13 \text{ dB}, \quad A_s = 21 \text{ dB} $$
2. **Bartlett (Triangular) Window:**
   $$ w[n] = 1 - \frac{2|n - \tau|}{N-1}, \quad \Delta\omega = \frac{8\pi}{N}, \quad \text{Peak Sidelobe: } -25 \text{ dB}, \quad A_s = 25 \text{ dB} $$
3. **Hann (Hanning) Window:**
   $$ w[n] = 0.5 - 0.5\cos\left( \frac{2\pi n}{N-1} \right), \quad \Delta\omega = \frac{8\pi}{N}, \quad \text{Peak Sidelobe: } -31 \text{ dB}, \quad A_s = 44 \text{ dB} $$

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 22.1: FIR Lowpass Filter Design using Hann Window
**Problem:** Design a causal FIR lowpass filter with cutoff $\omega_c = \frac{\pi}{4} \text{ rad/sample}$ and length $N = 7$ using a Hann window.

**Solution:**
* Length $N = 7 \implies \tau = \frac{7-1}{2} = 3$.
* Ideal impulse response:
  $$ h_d[n] = \frac{\sin(\frac{\pi}{4}(n - 3))}{\pi(n - 3)} $$
  * $h_d[3] = \frac{\omega_c}{\pi} = \frac{\pi/4}{\pi} = 0.2500$
  * $h_d[2] = h_d[4] = \frac{\sin(-\pi/4)}{-\pi} = \frac{\sqrt{2}/2}{\pi} = \frac{0.7071}{\pi} = 0.2251$
  * $h_d[1] = h_d[5] = \frac{\sin(-2\pi/4)}{-2\pi} = \frac{1}{2\pi} = 0.1592$
  * $h_d[0] = h_d[6] = \frac{\sin(-3\pi/4)}{-3\pi} = \frac{0.7071}{3\pi} = 0.0750$
* **Hann Window Values ($w[n] = 0.5 - 0.5\cos(\frac{2\pi n}{6})$):**
  * $w[3] = 0.5 - 0.5\cos(\pi) = 1.0000$
  * $w[2] = w[4] = 0.5 - 0.5\cos(2\pi/3) = 0.5 - 0.5(-0.5) = 0.7500$
  * $w[1] = w[5] = 0.5 - 0.5\cos(\pi/3) = 0.5 - 0.5(0.5) = 0.2500$
  * $w[0] = w[6] = 0.5 - 0.5\cos(0) = 0.0000$
* **Final FIR Filter Coefficients ($h[n] = h_d[n] \cdot w[n]$):**
  * $h[0] = h[6] = 0.0750 \times 0.0000 = 0.0000$
  * $h[1] = h[5] = 0.1592 \times 0.2500 = 0.0398$
  * $h[2] = h[4] = 0.2251 \times 0.7500 = 0.1688$
  * $h[3] = 0.2500 \times 1.0000 = 0.2500$
$$ h[n] = \{ \underset{\uparrow}{0.0000}, 0.0398, 0.1688, 0.2500, 0.1688, 0.0398, 0.0000 \} $$

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
**(a)** What is the Gibbs phenomenon? Explain how window functions reduce Gibbs ringing at the expense of transition bandwidth. *(6 Marks)*
**(b)** Design a 9-tap FIR Highpass filter with cutoff $\omega_c = \frac{\pi}{3}$ using a Bartlett window. *(9 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Part (a):**
  * Explanation of 8.95% overshoot at step discontinuities and Fourier truncation *(3 Marks)*
  * Tapering effect of windows: Smooth boundary transitions suppress high-frequency sidelobes but widen mainlobe transition band *(3 Marks)*
* **Part (b):**
  * $N=9, \tau=4$.
  * $h_d[n] = \delta[n-4] - \frac{\sin(\pi(n-4)/3)}{\pi(n-4)}$ *(3 Marks)*
  * Bartlett window: $w[n] = 1 - \frac{|n-4|}{4}$ for $n=0,\dots,8$ *(2 Marks)*
  * Evaluation of all 9 coefficients $h[n] = h_d[n] w[n]$ with symmetry *(4 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import numpy as np

N = 7
tau = 3
wc = np.pi / 4
n = np.arange(N)

# Ideal LPF
hd = np.zeros(N)
hd[n != tau] = np.sin(wc * (n[n != tau] - tau)) / (np.pi * (n[n != tau] - tau))
hd[tau] = wc / np.pi

# Hann window
w = 0.5 - 0.5 * np.cos(2 * np.pi * n / (N - 1))
h = hd * w

print("Designed FIR Filter Coefficients h[n]:")
print(np.round(h, 4))
```
