# Lecture 27: Impulse Invariance Method for IIR Filter Design
## EE3621: Digital Signal Processing | III B.Tech EEE

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Derive** the Impulse Invariance mapping formula for simple and repeated poles.
2. **Transform** continuous transfer functions $H_a(s)$ into discrete transfer functions $H(z)$.
3. **Analyze** the mechanism and severity of spectral aliasing.
4. **Determine** when Impulse Invariance is applicable in practical filter design.

---
## 2. MATHEMATICAL FOUNDATIONS

### 2.1 Pole Mapping Derivation
Given analog transfer function in partial fraction form:
$$ H_a(s) = \sum_{k=1}^{N} \frac{A_k}{s - p_k} $$
The continuous impulse response is:
$$ h_a(t) = \sum_{k=1}^{N} A_k e^{p_k t} u(t) $$
Sampling at $t = n T_d$ with gain scaling $T_d$:
$$ h[n] = T_d h_a(n T_d) = T_d \sum_{k=1}^{N} A_k e^{p_k n T_d} u[n] = T_d \sum_{k=1}^{N} A_k (e^{p_k T_d})^n u[n] $$
Taking the Z-Transform of $h[n]$:
$$ H(z) = T_d \sum_{k=1}^{N} \frac{A_k}{1 - e^{p_k T_d} z^{-1}} $$

### 2.2 Pole-Mapping Properties
* Let $p_k = \sigma_k + j\Omega_k$.
* Discrete pole: $z_k = e^{p_k T_d} = e^{\sigma_k T_d} e^{j\Omega_k T_d}$.
* **Magnitude:** $|z_k| = e^{\sigma_k T_d}$.
  * If $\sigma_k < 0$ (Left-half $s$-plane) $\implies |z_k| < 1$ (Inside unit circle $\implies$ **Stable**).
  * If $\sigma_k = 0$ ($j\Omega$ axis) $\implies |z_k| = 1$ (On unit circle).
  * If $\sigma_k > 0$ (Right-half $s$-plane) $\implies |z_k| > 1$ (Outside unit circle $\implies$ **Unstable**).

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 27.1: Impulse Invariance Transformation
**Problem:** Apply the Impulse Invariance method to design a digital filter from:
$$ H_a(s) = \frac{s + 1}{(s + 1)^2 + 9} = \frac{s + 1}{(s + 1 - 3j)(s + 1 + 3j)} $$
with sampling interval $T_d = 0.1\text{ s}$.

**Solution:**
1. **Partial Fraction Expansion:**
   $$ H_a(s) = \frac{0.5}{s + 1 - 3j} + \frac{0.5}{s + 1 + 3j} $$
   Poles: $p_1 = -1 + 3j, \; p_2 = -1 - 3j$.
2. **Apply Impulse Invariance Mapping:**
   $$ z_1 = e^{p_1 T_d} = e^{(-1 + 3j)(0.1)} = e^{-0.1} e^{j 0.3} = 0.9048 e^{j 0.3} = 0.9048(\cos 0.3 + j \sin 0.3) = 0.8644 + 0.2674j $$
   $$ H(z) = T_d \left[ \frac{0.5}{1 - e^{p_1 T_d} z^{-1}} + \frac{0.5}{1 - e^{p_2 T_d} z^{-1}} \right] = 0.1 \left[ \frac{1 - e^{-0.1} \cos(0.3) z^{-1}}{1 - 2 e^{-0.1} \cos(0.3) z^{-1} + e^{-0.2} z^{-2}} \right] $$
   $$ H(z) = \frac{0.1 - 0.08644 z^{-1}}{1 - 1.7288 z^{-1} + 0.8187 z^{-2}} $$

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
**(a)** Derive the Impulse Invariance mapping equation. Explain why highpass filters cannot be designed using this method. *(8 Marks)*
**(b)** Convert $H_a(s) = \frac{2}{(s+1)(s+2)}$ into a digital filter $H(z)$ using Impulse Invariance with $T_d = 1\text{ s}$. *(7 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Part (a):**
  * Mathematical derivation from $h_a(t) \to h[n] \to H(z)$ *(5 Marks)*
  * Explanation of periodic aliasing $\sum H_a(j(\omega + 2\pi k)/T_d)$ corrupting high frequencies *(3 Marks)*
* **Part (b):**
  * PFE: $H_a(s) = \frac{2}{s+1} - \frac{2}{s+2}$ *(2 Marks)*
  * Apply mapping with $T_d = 1$:
    $H(z) = 1 \cdot \left[ \frac{2}{1 - e^{-1} z^{-1}} - \frac{2}{1 - e^{-2} z^{-1}} \right] = \frac{2}{1 - 0.3679 z^{-1}} - \frac{2}{1 - 0.1353 z^{-1}}$ *(3 Marks)*
  * Combine:
    $H(z) = \frac{2(1 - 0.1353 z^{-1}) - 2(1 - 0.3679 z^{-1})}{(1 - 0.3679 z^{-1})(1 - 0.1353 z^{-1})} = \frac{0.4652 z^{-1}}{1 - 0.5032 z^{-1} + 0.0498 z^{-2}}$ *(2 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import scipy.signal as signal

b = [2]
a = [1, 3, 2]
bz, az = signal.impinvar(b, a, fs=1.0)
print("Impulse Invariance Numerator:", np.round(bz, 4))
print("Impulse Invariance Denominator:", np.round(az, 4))
```
