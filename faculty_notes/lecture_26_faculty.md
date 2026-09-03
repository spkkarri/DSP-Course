<Faculty Notes — Lecture 26: Analog Filter Approximations (Butterworth & Chebyshev)>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY
IIR digital filter design typically transforms well-established continuous-time analog filter prototypes (Butterworth, Chebyshev) into discrete transfer functions. This lecture covers continuous analog filter theory, pole placement, and order calculation equations.

**Pedagogical Strategy:**
1. Formulate the **Butterworth Approximation**: Maximally flat magnitude response in passband and stopband:
   $$ |H_a(j\Omega)|^2 = \frac{1}{1 + (\Omega / \Omega_c)^{2N}} $$
2. Derive the Butterworth order formula $N$ and 3-dB cutoff $\Omega_c$.
3. Show pole placement on a circle of radius $\Omega_c$ in the left-half $s$-plane.
4. Formulate **Chebyshev Type I (Equiripple Passband)** and **Type II (Inverse Chebyshev)** approximations using Chebyshev polynomials $C_N(x)$.
5. Contrast Butterworth and Chebyshev prototypes: Chebyshev achieves a much steeper transition roll-off for the same filter order $N$.

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Calculate** required filter order $N$ and cutoff $\Omega_c$ for Butterworth and Chebyshev analog lowpass prototypes.
2. **Determine** stable left-half $s$-plane pole locations for Butterworth and Chebyshev filters.
3. **Synthesize** continuous-time transfer functions $H_a(s)$ from given attenuation specifications.
4. **Compare** Butterworth, Chebyshev Type I, and Chebyshev Type II responses.

---
## 2. MATHEMATICAL FOUNDATIONS

### 2.1 Butterworth Filter Approximation
* **Magnitude Squared Function:**
  $$ |H_a(j\Omega)|^2 = \frac{1}{1 + \epsilon^2 (\Omega / \Omega_p)^{2N}} = \frac{1}{1 + (\Omega / \Omega_c)^{2N}} $$
* **Order Formula:**
  $$ N \ge \frac{\log_{10} \sqrt{\frac{10^{0.1 A_s} - 1}{10^{0.1 A_p} - 1}}}{\log_{10}(\Omega_s / \Omega_p)} = \frac{\log_{10}(\lambda / \epsilon)}{\log_{10}(\Omega_s / \Omega_p)} $$
* **3-dB Cutoff Frequency $\Omega_c$:**
  $$ \Omega_c = \frac{\Omega_p}{(10^{0.1 A_p} - 1)^{1/(2N)}} $$
* **Pole Locations in $s$-Plane:**
  $2N$ poles uniformly spaced on circle of radius $\Omega_c$. The $N$ stable left-half plane poles are:
  $$ s_k = \Omega_c e^{j \frac{\pi}{2} [1 + (2k-1)/N]}, \quad k = 1, 2, \dots, N $$

### 2.2 Chebyshev Type I Filter Approximation
* **Magnitude Squared Function:**
  $$ |H_a(j\Omega)|^2 = \frac{1}{1 + \epsilon^2 C_N^2(\Omega / \Omega_p)}, \quad \epsilon = \sqrt{10^{0.1 A_p} - 1} $$
* **Chebyshev Polynomials:**
  $$ C_N(x) = \begin{cases} \cos(N \arccos x), & |x| \le 1 \\ \cosh(N \text{arcosh } x), & |x| > 1 \end{cases} $$
  Recursion: $C_{N+1}(x) = 2x C_N(x) - C_{N-1}(x)$ with $C_0(x) = 1, C_1(x) = x$.
* **Order Formula:**
  $$ N \ge \frac{\text{arcosh}(\lambda / \epsilon)}{\text{arcosh}(\Omega_s / \Omega_p)} = \frac{\ln\left[ \frac{\lambda}{\epsilon} + \sqrt{\left(\frac{\lambda}{\epsilon}\right)^2 - 1} \right]}{\ln\left[ \frac{\Omega_s}{\Omega_p} + \sqrt{\left(\frac{\Omega_s}{\Omega_p}\right)^2 - 1} \right]} $$

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 26.1: Analog Butterworth Lowpass Filter Design
**Problem:** Design an analog Butterworth lowpass filter to satisfy:
* Passband loss $\le 1\text{ dB}$ at $\Omega_p = 100\text{ rad/s}$ ($A_p = 1\text{ dB}$)
* Stopband attenuation $\ge 20\text{ dB}$ at $\Omega_s = 200\text{ rad/s}$ ($A_s = 20\text{ dB}$)

**Solution:**
1. **Calculate Order $N$:**
   * $\epsilon = \sqrt{10^{0.1(1)} - 1} = \sqrt{1.2589 - 1} = \sqrt{0.2589} = 0.5088$
   * $\lambda = \sqrt{10^{0.1(20)} - 1} = \sqrt{100 - 1} = \sqrt{99} = 9.9499$
   * Ratio $\frac{\lambda}{\epsilon} = \frac{9.9499}{0.5088} = 19.555$
   * Frequency ratio $\frac{\Omega_s}{\Omega_p} = \frac{200}{100} = 2.0$
   $$ N \ge \frac{\log_{10}(19.555)}{\log_{10}(2.0)} = \frac{1.2913}{0.3010} = 4.29 \implies \mathbf{N = 5} $$
2. **Calculate Cutoff Frequency $\Omega_c$:**
   $$ \Omega_c = \frac{\Omega_p}{\epsilon^{1/N}} = \frac{100}{(0.5088)^{1/5}} = \frac{100}{0.8735} = \mathbf{114.48 \text{ rad/s}} $$
3. **Poles ($N=5$):**
   * $s_1, s_5 = 114.48 e^{j (180^\circ \pm 36^\circ)} = 114.48 (-0.8090 \pm j 0.5878) = -92.62 \pm j 67.29$
   * $s_2, s_4 = 114.48 e^{j (180^\circ \pm 72^\circ)} = 114.48 (-0.3090 \pm j 0.9511) = -35.37 \pm j 108.88$
   * $s_3 = 114.48 e^{j 180^\circ} = -114.48$
4. **Transfer Function $H_a(s)$:**
   $$ H_a(s) = \frac{\Omega_c^5}{(s + 114.48)(s^2 + 185.24s + 13106)(s^2 + 70.74s + 13106)} $$

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
**(a)** Derive the expressions for the order $N$ and cutoff frequency $\Omega_c$ of an analog Butterworth lowpass filter. *(8 Marks)*
**(b)** Design an analog Chebyshev Type I lowpass filter with $1\text{ dB}$ passband ripple up to $\Omega_p = 10\text{ rad/s}$ and stopband attenuation $\ge 30\text{ dB}$ at $\Omega_s = 25\text{ rad/s}$. Find order $N$. *(7 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Part (a):** Complete derivation from magnitude equations at $\Omega_p$ and $\Omega_s$ *(8 Marks)*
* **Part (b):**
  * $\epsilon = \sqrt{10^{0.1} - 1} = 0.5088, \; \lambda = \sqrt{10^3 - 1} = 31.607$
  * $\frac{\lambda}{\epsilon} = \frac{31.607}{0.5088} = 62.12$
  * $\frac{\Omega_s}{\Omega_p} = \frac{25}{10} = 2.5$
  * $N \ge \frac{\text{arcosh}(62.12)}{\text{arcosh}(2.5)} = \frac{\ln(62.12 + \sqrt{62.12^2 - 1})}{\ln(2.5 + \sqrt{2.5^2 - 1})} = \frac{4.822}{1.5668} = 3.078 \implies \mathbf{N = 4}$ *(7 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import scipy.signal as signal

N, Wn = signal.buttord(100, 200, 1, 20, analog=True)
print(f"Butterworth Order: {N}, Cutoff: {Wn:.2f} rad/s")
```
