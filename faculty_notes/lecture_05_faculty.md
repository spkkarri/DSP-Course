<Faculty Notes — Lecture 5: Z-Transform & Region of Convergence (ROC)>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY
The Z-Transform extends continuous-frequency Fourier analysis into the complex plane $z = r e^{j\omega}$, enabling rigorous analysis of unstable systems, transient dynamics, difference equations, and system stability.

**Pedagogical Strategy:**
1. Define the two-sided (bilateral) Z-transform: $X(z) = \sum_{n=-\infty}^\infty x[n] z^{-n}$.
2. Show that the DTFT is the special case of the Z-transform evaluated on the unit circle ($r = 1 \implies z = e^{j\omega}$).
3. Emphasize that **a Z-transform is incomplete without specifying its Region of Convergence (ROC)**.
4. Establish the 6 fundamental properties of the ROC (connected ring, no poles inside ROC, right-sided $\implies |z| > r_{\max}$, left-sided $\implies |z| < r_{\min}$, two-sided $\implies r_1 < |z| < r_2$).
5. Derive standard transform pairs and properties (Linearity, Shifting, Scaling, Differentiation in z-domain, Convolution).

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Derive** the Z-transform and sketch the ROC for causal, anti-causal, and two-sided sequences.
2. **Apply** the fundamental properties of the ROC to deduce stability and causality.
3. **Utilize** Z-transform algebraic properties to transform composite discrete signals.
4. **Relate** pole-zero configurations in the complex $z$-plane to time-domain signal behaviors.

---
## 2. MATHEMATICAL FOUNDATIONS

### 2.1 The Bilateral Z-Transform
$$ X(z) = \mathcal{Z}\{x[n]\} = \sum_{n=-\infty}^{\infty} x[n] z^{-n}, \quad z = r e^{j\omega} \in \mathbb{C} $$
Substituting $z = r e^{j\omega}$:
$$ X(r e^{j\omega}) = \sum_{n=-\infty}^{\infty} (x[n] r^{-n}) e^{-j\omega n} = \mathcal{F}\{x[n] r^{-n}\} $$
The Z-transform is the DTFT of the sequence multiplied by a real exponential damping factor $r^{-n}$.

### 2.2 Region of Convergence (ROC) Properties
The ROC is the set of points in the $z$-plane for which $\sum_{n=-\infty}^\infty |x[n] r^{-n}| < \infty$:
1. The ROC is a ring or disk centered at the origin: $r_R < |z| < r_L$.
2. The ROC **cannot contain any poles**.
3. For a finite-duration sequence, the ROC is the entire $z$-plane, except possibly $z = 0$ and/or $z = \infty$.
4. For a **right-sided (causal)** sequence, the ROC extends outward from the outermost finite pole: $|z| > r_{\max}$.
5. For a **left-sided (anti-causal)** sequence, the ROC extends inward from the innermost non-zero pole: $|z| < r_{\min}$.
6. For a **two-sided** sequence, the ROC is an open annular ring bounded by poles: $r_1 < |z| < r_2$.
7. An LTI system is **BIBO stable** if and only if the ROC of its system function $H(z)$ **includes the unit circle $|z| = 1$**.

### 2.3 Common Z-Transform Pairs

| Sequence $x[n]$ | Z-Transform $X(z)$ | ROC |
| :--- | :--- | :--- |
| $\delta[n]$ | $1$ | Entire $z$-plane |
| $\delta[n - n_0]$ | $z^{-n_0}$ | All $z$, except $z=0$ ($n_0>0$) or $z=\infty$ ($n_0<0$) |
| $u[n]$ | $\frac{1}{1 - z^{-1}} = \frac{z}{z - 1}$ | $|z| > 1$ |
| $-u[-n-1]$ | $\frac{1}{1 - z^{-1}} = \frac{z}{z - 1}$ | $|z| < 1$ |
| $a^n u[n]$ | $\frac{1}{1 - a z^{-1}} = \frac{z}{z - a}$ | $|z| > |a|$ |
| $-a^n u[-n-1]$ | $\frac{1}{1 - a z^{-1}} = \frac{z}{z - a}$ | $|z| < |a|$ |
| $n a^n u[n]$ | $\frac{a z^{-1}}{(1 - a z^{-1})^2} = \frac{a z}{(z - a)^2}$ | $|z| > |a|$ |
| $\cos(\omega_0 n) u[n]$ | $\frac{1 - \cos\omega_0 z^{-1}}{1 - 2\cos\omega_0 z^{-1} + z^{-2}}$ | $|z| > 1$ |
| $\sin(\omega_0 n) u[n]$ | $\frac{\sin\omega_0 z^{-1}}{1 - 2\cos\omega_0 z^{-1} + z^{-2}}$ | $|z| > 1$ |

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 5.1: Two-Sided Sequence Z-Transform
**Problem:** Find the Z-transform and ROC of $x[n] = \left( \frac{1}{2} \right)^n u[n] + \left( -\frac{1}{3} \right)^n u[-n-1]$.

**Solution:**
Let $x_1[n] = (1/2)^n u[n]$ and $x_2[n] = -[ -(-1/3)^n u[-n-1] ]$:
* $X_1(z) = \frac{1}{1 - \frac{1}{2} z^{-1}}$ with ROC: $|z| > \frac{1}{2}$.
* $X_2(z) = \frac{1}{1 - (-\frac{1}{3}) z^{-1}} = \frac{1}{1 + \frac{1}{3} z^{-1}}$ with ROC: $|z| < \left|-\frac{1}{3}\right| = \frac{1}{3}$.
The overall ROC is the intersection: $\text{ROC} = \{|z| > 1/2\} \cap \{|z| < 1/3\} = \emptyset$ (Empty Set).
Because the two regions do not overlap, the Z-transform $X(z)$ **does not exist**.

---
### Example 5.2: Two-Sided Sequence with Valid Annular ROC
**Problem:** Find $X(z)$ and sketch ROC for $x[n] = \left( \frac{1}{3} \right)^n u[n] - 2^n u[-n-1]$.

**Solution:**
* $X_1(z) = \frac{1}{1 - \frac{1}{3}z^{-1}}$ with $\text{ROC}_1: |z| > 1/3$.
* $X_2(z) = \frac{1}{1 - 2 z^{-1}}$ with $\text{ROC}_2: |z| < 2$.
Overall ROC: $\text{ROC}_1 \cap \text{ROC}_2 = \frac{1}{3} < |z| < 2$.
$$ X(z) = \frac{1}{1 - \frac{1}{3} z^{-1}} + \frac{1}{1 - 2 z^{-1}} = \frac{(1 - 2z^{-1}) + (1 - \frac{1}{3}z^{-1})}{(1 - \frac{1}{3}z^{-1})(1 - 2z^{-1})} = \frac{2 - \frac{7}{3} z^{-1}}{(1 - \frac{1}{3}z^{-1})(1 - 2z^{-1})} $$
Poles at $z = 1/3$ and $z = 2$.
Zeros at $z = 7/6 \approx 1.167$.
Since the annular ring $\frac{1}{3} < |z| < 2$ includes the unit circle $|z|=1$, the signal possesses a valid DTFT and is stable.

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
**(a)** List the properties of the Region of Convergence (ROC) of the Z-transform. *(6 Marks)*
**(b)** Find the Z-transform and sketch the pole-zero plot and ROC of:
$$ x[n] = (0.5)^n u[n] + (0.8)^n u[n] $$
Is the system stable? Is it causal? Justify. *(9 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Part (a):**
  * Listing 6 properties with brief physical justifications *(6 Marks)*
* **Part (b):**
  * Transform of individual terms:
    $$ X(z) = \frac{1}{1 - 0.5 z^{-1}} + \frac{1}{1 - 0.8 z^{-1}}, \quad \text{ROC}_1: |z| > 0.5, \; \text{ROC}_2: |z| > 0.8 $$ *(3 Marks)*
  * Combine into rational fraction:
    $$ X(z) = \frac{(1 - 0.8 z^{-1}) + (1 - 0.5 z^{-1})}{(1 - 0.5 z^{-1})(1 - 0.8 z^{-1})} = \frac{2 - 1.3 z^{-1}}{1 - 1.3 z^{-1} + 0.4 z^{-2}} = \frac{2 z (z - 0.65)}{(z - 0.5)(z - 0.8)} $$ *(2 Marks)*
  * Poles: $z = 0.5, 0.8$. Zeros: $z = 0, 0.65$.
  * Overall ROC: $|z| > \max(0.5, 0.8) = |z| > 0.8$. *(2 Marks)*
  * Causality & Stability:
    * **Causal:** Yes, because the ROC is outside the outermost pole $|z| > 0.8$.
    * **Stable:** Yes, because the ROC $|z| > 0.8$ includes the unit circle $|z| = 1$. *(2 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import numpy as np
import scipy.signal as signal

# Pole-zero calculation
b = [2, -1.3]
a = [1, -1.3, 0.4]
zeros, poles, gain = signal.tf2zpk(b, a)
print(f"Poles: {poles}")
print(f"Zeros: {zeros}")
```
