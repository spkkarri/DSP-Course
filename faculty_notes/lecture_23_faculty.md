<Faculty Notes — Lecture 23: Hamming, Blackman & Kaiser Windows>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY
While basic windows (Hann, Bartlett) provide moderate stopband attenuation, high-performance applications (audio equalization, communications, radar pulse compression) demand deep stopband rejection ($>50\text{ dB}$). The **Hamming**, **Blackman**, and **Kaiser** windows provide superior stopband suppression.

**Pedagogical Strategy:**
1. Formulate the **Hamming Window**: $w[n] = 0.54 - 0.46\cos(\frac{2\pi n}{N-1})$, showing how the $0.54/0.46$ coefficient choice places a spectral zero directly on the first sidelobe peak, yielding $-43\text{ dB}$ peak sidelobe.
2. Formulate the **Blackman Window**: Adding a 2nd harmonic cosine achieves $-58\text{ dB}$ peak sidelobe and $74\text{ dB}$ attenuation.
3. Master the **Kaiser Window Family**: Parameterized by shape factor $\beta$ and zeroth-order modified Bessel function $I_0(\cdot)$.
4. Teach empirical design formulas (Bellanger / Kaiser formulas) to calculate exact filter length $N$ from transition width $\Delta f$ and stopband attenuation $A_s$.
5. Complete comprehensive filter design examples.

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Design** high-rejection FIR filters using Hamming, Blackman, and Kaiser windows.
2. **Compute** required filter length $N$ using Kaiser empirical design equations.
3. **Tune** the shape parameter $\beta$ to trade off transition bandwidth and stopband ripple.
4. **Compare** performance trade-offs across all standard window families.

---
## 2. MATHEMATICAL FOUNDATIONS

### 2.1 Standard Window Performance Summary

| Window | Time Formula $w[n], \; 0 \le n \le N-1$ | Mainlobe Width $\Delta\omega$ | Peak Sidelobe | Min Stopband Attenuation $A_s$ | Transition Width Formula |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Rectangular** | $1$ | $4\pi / N$ | $-13$ dB | $21$ dB | $\Delta f \approx 0.9 / N$ |
| **Hann** | $0.5 - 0.5\cos\left(\frac{2\pi n}{N-1}\right)$ | $8\pi / N$ | $-31$ dB | $44$ dB | $\Delta f \approx 3.1 / N$ |
| **Hamming** | $0.54 - 0.46\cos\left(\frac{2\pi n}{N-1}\right)$ | $8\pi / N$ | $-41$ dB | $53$ dB | $\Delta f \approx 3.3 / N$ |
| **Blackman** | $0.42 - 0.5\cos\left(\frac{2\pi n}{N-1}\right) + 0.08\cos\left(\frac{4\pi n}{N-1}\right)$ | $12\pi / N$ | $-57$ dB | $74$ dB | $\Delta f \approx 5.5 / N$ |

### 2.2 The Kaiser Window Design Equations
$$ w[n] = \frac{I_0\left( \beta \sqrt{1 - \left(\frac{n - \tau}{\tau}\right)^2} \right)}{I_0(\beta)}, \quad \tau = \frac{N-1}{2} $$
Where $I_0(x) = \sum_{k=0}^{\infty} \left[ \frac{(x/2)^k}{k!} \right]^2$.
* **Shape Parameter $\beta$ Calculation:**
  $$ \beta = \begin{cases} 0.1102(A_s - 8.7), & A_s > 50 \\ 0.5842(A_s - 21)^{0.4} + 0.07886(A_s - 21), & 21 \le A_s \le 50 \\ 0, & A_s < 21 \end{cases} $$
* **Filter Length $N$ Calculation:**
  $$ N \ge \frac{A_s - 7.95}{14.36 \cdot \Delta f} + 1, \quad \Delta f = \frac{\omega_s - \omega_p}{2\pi} $$

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 23.1: Complete FIR Filter Design via Kaiser Window
**Problem:** Design a linear-phase FIR Lowpass filter meeting the following specifications:
* Passband edge: $\omega_p = 0.2\pi \text{ rad}$
* Stopband edge: $\omega_s = 0.3\pi \text{ rad}$
* Passband ripple: $\delta_p = 0.01$ (Peak passband ripple $\approx 0.086\text{ dB}$)
* Stopband ripple: $\delta_s = 0.001$ (Stopband attenuation $A_s = -20\log_{10}(0.001) = 60\text{ dB}$)

**Solution:**
1. **Determine Design Attenuation:**
   $A_s = -20\log_{10}(\min(\delta_p, \delta_s)) = -20\log_{10}(0.001) = 60\text{ dB}$.
2. **Compute Normalized Transition Bandwidth:**
   $$ \Delta f = \frac{\omega_s - \omega_p}{2\pi} = \frac{0.3\pi - 0.2\pi}{2\pi} = \frac{0.1\pi}{2\pi} = 0.05 $$
3. **Calculate Filter Order & Length $N$:**
   $$ N \ge \frac{60 - 7.95}{14.36 \times 0.05} + 1 = \frac{52.05}{0.718} + 1 = 72.49 + 1 = 73.49 \implies \mathbf{N = 75} \quad (\text{Select odd length } N) $$
4. **Calculate Kaiser Parameter $\beta$ ($A_s > 50$):**
   $$ \beta = 0.1102(60 - 8.7) = 0.1102(51.3) = \mathbf{5.6533} $$
5. **Cutoff Frequency:**
   $$ \omega_c = \frac{\omega_p + \omega_s}{2} = \frac{0.2\pi + 0.3\pi}{2} = 0.25\pi \text{ rad/sample} $$

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
**(a)** Explain why the Hamming window achieves $-43\text{ dB}$ peak sidelobe level compared to $-31\text{ dB}$ for the Hann window. *(5 Marks)*
**(b)** Design an FIR bandpass filter using a Hamming window to pass frequencies between $0.3\pi$ and $0.6\pi$ with transition widths of $0.05\pi$. Find $N$ and the expression for $h[n]$. *(10 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Part (a):**
  * Mathematical cancellation: The pedestal $0.54 - 0.46\cos$ places a transmission zero at the first sidelobe peak of the Dirichlet sinc kernel *(5 Marks)*
* **Part (b):**
  * Transition width $\Delta\omega = 0.05\pi \implies \Delta f = 0.025$.
  * For Hamming: $\Delta\omega = \frac{6.6\pi}{N} \implies N \ge \frac{6.6}{0.05} = 132 \implies N = 133$ (odd length) *(4 Marks)*
  * Ideal Bandpass: $h_d[n] = \frac{\sin(0.6\pi(n-\tau))}{\pi(n-\tau)} - \frac{\sin(0.3\pi(n-\tau))}{\pi(n-\tau)}, \quad \tau = 66$ *(3 Marks)*
  * Final coefficients $h[n] = h_d[n] \cdot [0.54 - 0.46\cos(2\pi n / 132)]$ *(3 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import scipy.signal as signal

# Kaiser filter design verification
N, beta = signal.kaiserord(60, 0.1)  # 60 dB, dw = 0.1*pi (df = 0.05)
print(f"Kaiser length N = {N}, beta = {beta:.4f}")
```
