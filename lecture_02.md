# Lecture 2: LTI Systems, Convolution, Stability & Difference Equations
## EE3621: Digital Signal Processing | III B.Tech EEE

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Test** discrete systems for Linearity, Time-Invariance, Causality, Stability, and Memory.
2. **Derive** and **compute** the convolution sum $y[n] = x[n] * h[n]$ analytically, tabularly, and graphically.
3. **Determine** the duration and sample support of the convolution of two finite-length sequences.
4. **Evaluate** BIBO stability and causality directly from a system's impulse response $h[n]$.
5. **Formulate** and **solve** difference equations describing discrete-time recursive and non-recursive systems.

---
## 2. MATHEMATICAL FOUNDATIONS

### 2.1 The Convolution Sum Derivation
Any discrete-time input $x[n]$ can be represented as a weighted sum of shifted impulses:
$$ x[n] = \sum_{k=-\infty}^{\infty} x[k] \delta[n - k] $$
Let $\mathcal{T}\{\cdot\}$ represent a Linear Time-Invariant operator. Applying $\mathcal{T}$ to $x[n]$:
$$ y[n] = \mathcal{T}\{x[n]\} = \mathcal{T}\left\{ \sum_{k=-\infty}^{\infty} x[k] \delta[n - k] \right\} $$
By Linearity (Superposition principle):
$$ y[n] = \sum_{k=-\infty}^{\infty} x[k] \mathcal{T}\{\delta[n - k]\} $$
Let $h[n] = \mathcal{T}\{\delta[n]\}$ be the **impulse response**. By Time-Invariance:
$$ \mathcal{T}\{\delta[n - k]\} = h[n - k] $$
Thus, we arrive at the **Discrete Convolution Sum**:
$$ y[n] = x[n] * h[n] = \sum_{k=-\infty}^{\infty} x[k] h[n - k] = \sum_{k=-\infty}^{\infty} h[k] x[n - k] $$

### 2.2 Properties of Convolution
1. **Commutativity:** $x[n] * h[n] = h[n] * x[n]$.
2. **Associativity:** $(x[n] * h_1[n]) * h_2[n] = x[n] * (h_1[n] * h_2[n])$.
3. **Distributivity:** $x[n] * (h_1[n] + h_2[n]) = x[n] * h_1[n] + x[n] * h_2[n]$.
4. **Identity:** $x[n] * \delta[n] = x[n]$.
5. **Shift Property:** $x[n - n_1] * h[n - n_2] = y[n - n_1 - n_2]$.

### 2.3 Length of Convolved Sequences
If sequence $x[n]$ has length $L_x$ (from $n = N_1$ to $N_2$) and impulse response $h[n]$ has length $L_h$ (from $n = M_1$ to $M_2$), the convolved output $y[n] = x[n] * h[n]$ has:
* Total length: $L_y = L_x + L_h - 1$.
* Starting index: $n_{\text{start}} = N_1 + M_1$.
* Ending index: $n_{\text{end}} = N_2 + M_2$.

### 2.4 Causality and BIBO Stability Criteria
* **Causality:** An LTI system is causal if and only if its impulse response is zero for all negative time:
  $$ h[n] = 0, \quad \forall n < 0 $$
* **BIBO Stability:** An LTI system is Bounded-Input Bounded-Output (BIBO) stable if and only if its impulse response is **absolutely summable**:
  $$ S = \sum_{n=-\infty}^{\infty} |h[n]| < \infty $$
  *Proof:* Let input $|x[n]| \le M_x < \infty$ for all $n$.
  $$ |y[n]| = \left| \sum_{k=-\infty}^{\infty} h[k] x[n-k] \right| \le \sum_{k=-\infty}^{\infty} |h[k]| |x[n-k]| \le M_x \sum_{k=-\infty}^{\infty} |h[k]| = M_x \cdot S $$
  If $S < \infty$, then $|y[n]| \le M_y = M_x S < \infty$.

### 2.5 Linear Constant-Coefficient Difference Equations (LCCDE)
An $N^{\text{th}}$-order LCCDE relating input $x[n]$ to output $y[n]$ is given by:
$$ \sum_{k=0}^{N} a_k y[n-k] = \sum_{m=0}^{M} b_m x[n-m], \quad a_0 = 1 $$
$$ y[n] = \sum_{m=0}^{M} b_m x[n-m] - \sum_{k=1}^{N} a_k y[n-k] $$
The total solution consists of the Homogeneous solution $y_h[n]$ (natural response satisfying $\sum a_k y[n-k] = 0$) and the Particular solution $y_p[n]$ (forced response).

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 2.1: Analytical Convolution of Two Sequences
**Problem:** Compute the linear convolution $y[n] = x[n] * h[n]$ for:
$$ x[n] = a^n u[n], \quad h[n] = b^n u[n], \quad a \ne b, \; |a|<1, |b|<1 $$

**Solution:**
$$ y[n] = \sum_{k=-\infty}^{\infty} x[k] h[n - k] = \sum_{k=-\infty}^{\infty} (a^k u[k]) (b^{n-k} u[n - k]) $$
The step functions require:
* $u[k] = 1 \implies k \ge 0$.
* $u[n - k] = 1 \implies k \le n$.
Thus, for $n < 0$, the limits cannot be satisfied and $y[n] = 0$.
For $n \ge 0$, the summation limits are $k = 0$ to $n$:
$$ y[n] = \sum_{k=0}^{n} a^k b^{n-k} = b^n \sum_{k=0}^{n} \left( \frac{a}{b} \right)^k $$
Using the finite geometric series sum $\sum_{k=0}^n r^k = \frac{1 - r^{n+1}}{1 - r}$:
$$ y[n] = b^n \frac{1 - (a/b)^{n+1}}{1 - (a/b)} = b^n \frac{1 - a^{n+1} b^{-(n+1)}}{(b - a)/b} = \frac{b^{n+1} - a^{n+1}}{b - a} u[n] $$
$$ y[n] = \left( \frac{b^{n+1} - a^{n+1}}{b - a} \right) u[n] $$

---
### Example 2.2: Stability and Causality Testing
**Problem:** Determine if the systems with the following impulse responses are causal and BIBO stable:
(a) $h_1[n] = (0.5)^n u[n+2]$
(b) $h_2[n] = 3^n u[-n-1]$
(c) $h_3[n] = \left( \frac{1}{n} \right) u[n-1]$

**Solution:**
**(a)** Causality: $h_1[-2] = (0.5)^{-2} = 4 \ne 0 \implies$ **Non-causal**.
Stability:
$$ \sum_{n=-\infty}^{\infty} |h_1[n]| = \sum_{n=-2}^{\infty} (0.5)^n = 4 + 2 + \sum_{n=0}^{\infty} (0.5)^n = 6 + \frac{1}{1 - 0.5} = 6 + 2 = 8 < \infty \implies \textbf{BIBO Stable}. $$

**(b)** Causality: $h_2[n]$ is non-zero for $n \le -1 \implies$ **Non-causal** (anti-causal).
Stability: Let $m = -n$:
$$ \sum_{n=-\infty}^{\infty} |h_2[n]| = \sum_{n=-\infty}^{-1} 3^n = \sum_{m=1}^{\infty} 3^{-m} = \sum_{m=1}^{\infty} \left( \frac{1}{3} \right)^m = \frac{1/3}{1 - 1/3} = \frac{1/3}{2/3} = 0.5 < \infty \implies \textbf{BIBO Stable}. $$

**(c)** Causality: $h_3[n] = 0$ for $n < 1 \implies$ **Causal**.
Stability:
$$ \sum_{n=-\infty}^{\infty} |h_3[n]| = \sum_{n=1}^{\infty} \frac{1}{n} $$
This is the harmonic series, which diverges ($\sum_{n=1}^\infty \frac{1}{n} = \infty$). Therefore, the system is **Unstable**.

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
**(a)** State and prove the necessary and sufficient condition for a discrete-time LTI system to be BIBO stable. *(6 Marks)*
**(b)** Convolve the two finite sequences using the tabular method:
$$ x[n] = \{ \underset{\uparrow}{2}, 1, -1, 3 \}, \quad h[n] = \{ \underset{\uparrow}{1}, 2, 0, -2 \} $$
Verify the result using polynomial multiplication. *(9 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Part (a):**
  * Statement of condition: $\sum_{n=-\infty}^\infty |h[n]| < \infty$ *(2 Marks)*
  * Proof of sufficiency: Let $|x[n]| \le M_x$, prove $|y[n]| \le M_x \sum |h[k]| < \infty$ *(2 Marks)*
  * Proof of necessity: Construct bounded input $x[n] = \text{sgn}(h[-n])$ showing $y[0] = \sum |h[k]| = \infty$ if divergent *(2 Marks)*
* **Part (b):**
  * Tabular / Matrix setup:
    $$ \begin{array}{c|cccc} \times & 2 & 1 & -1 & 3 \\ \hline 1 & 2 & 1 & -1 & 3 \\ 2 & 4 & 2 & -2 & 6 \\ 0 & 0 & 0 & 0 & 0 \\ -2 & -4 & -2 & 2 & -6 \end{array} $$ *(3 Marks)*
  * Diagonal summation:
    * $y[0] = 2$
    * $y[1] = 1 + 4 = 5$
    * $y[2] = -1 + 2 + 0 = 1$
    * $y[3] = 3 - 2 + 0 - 4 = -3$
    * $y[4] = 6 + 0 - 2 = 4$
    * $y[5] = 0 + 2 = 2$
    * $y[6] = -6$
    $$ y[n] = \{ \underset{\uparrow}{2}, 5, 1, -3, 4, 2, -6 \}, \quad \text{Length } L_y = 4 + 4 - 1 = 7 \text{ samples} $$ *(4 Marks)*
  * Verification by polynomial multiplication:
    $(2 + z^{-1} - z^{-2} + 3z^{-3})(1 + 2z^{-1} - 2z^{-3}) = 2 + 5z^{-1} + z^{-2} - 3z^{-3} + 4z^{-4} + 2z^{-5} - 6z^{-6}$ *(2 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import numpy as np

x = np.array([2, 1, -1, 3])
h = np.array([1, 2, 0, -2])
y = np.convolve(x, h)

print(f"Convolution Output y[n] = {y}")
# Expected: [ 2,  5,  1, -3,  4,  2, -6]
```
