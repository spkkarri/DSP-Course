<Faculty Notes — Lecture 6: Inverse Z-Transform & System Analysis>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY
Inversion of the Z-Transform is central to solving difference equations, deriving impulse responses, and synthesizing digital filter structures. This lecture provides a comprehensive treatment of all three inversion techniques: **Partial Fraction Expansion (PFE)**, **Power Series Expansion (Long Division)**, and the **Contour Inversion Integral / Cauchy Residue Theorem**.

**Pedagogical Strategy:**
1. Master Partial Fraction Expansion for distinct real poles, repeated poles, and complex conjugate pole pairs.
2. Teach the Long Division method for obtaining the first $N$ samples of non-rational or high-order transfer functions.
3. Review the Cauchy Residue Theorem for complex contour integration along a closed counterclockwise path in the ROC: $x[n] = \frac{1}{2\pi j} \oint_C X(z) z^{n-1} dz = \sum \text{Res}[X(z) z^{n-1}]$.
4. Link the pole locations of the rational transfer function $H(z) = \frac{B(z)}{A(z)}$ directly to transient decay rates and sinusoidal oscillation modes.
5. System stability and causality criteria from pole-zero diagrams.

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Apply** Partial Fraction Expansion to compute $x[n]$ for distinct, repeated, and complex poles under different ROC constraints.
2. **Execute** polynomial long division to extract sample values for causal ($|z|>r_0$) and anti-causal ($|z|<r_0$) sequences.
3. **Evaluate** inverse transforms using the Cauchy Residue Theorem.
4. **Solve** Linear Constant-Coefficient Difference Equations (LCCDE) with non-zero initial conditions using the One-Sided (Unilateral) Z-Transform.
5. **Determine** stability, causality, and frequency selectivity from pole-zero plots.

---
## 2. MATHEMATICAL FOUNDATIONS

### 2.1 Inversion Methods Overview
1. **Partial Fraction Expansion (PFE):** Most practical for rational $X(z) = \frac{B(z)}{A(z)}$.
2. **Power Series (Long Division):** Expands $X(z) = \sum x[n] z^{-n}$ directly.
3. **Contour Inversion Integral (Cauchy Residue Theorem):**
   $$ x[n] = \frac{1}{2\pi j} \oint_{C} X(z) z^{n-1} dz = \sum_{\text{poles inside } C} \text{Res} \left[ X(z) z^{n-1} \right] $$
   Where the residue at a simple pole $p_k$ is:
   $$ \text{Res}[X(z) z^{n-1}]_{z = p_k} = \lim_{z \to p_k} (z - p_k) X(z) z^{n-1} $$

### 2.2 Partial Fraction Expansion Formulation
Given $X(z) = \frac{b_0 + b_1 z^{-1} + \dots + b_M z^{-M}}{1 + a_1 z^{-1} + \dots + a_N z^{-N}}$.
It is mathematically cleanest to expand $\frac{X(z)}{z}$ in terms of $z$:
$$ \frac{X(z)}{z} = \frac{A_1}{z - p_1} + \frac{A_2}{z - p_2} + \dots + \frac{A_N}{z - p_N} $$
Where residue $A_k = \left. (z - p_k) \frac{X(z)}{z} \right|_{z = p_k}$.
Then:
$$ X(z) = \sum_{k=1}^{N} A_k \frac{z}{z - p_k} = \sum_{k=1}^{N} A_k \frac{1}{1 - p_k z^{-1}} $$
Inversion depends on the ROC for each pole $p_k$:
* If ROC is outside pole ($|z| > |p_k|$): $A_k (p_k)^n u[n]$ (Causal).
* If ROC is inside pole ($|z| < |p_k|$): $-A_k (p_k)^n u[-n-1]$ (Anti-causal).

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 6.1: Inversion under Different ROC Constraints
**Problem:** Find $x[n]$ for $X(z) = \frac{1}{(1 - 0.5 z^{-1})(1 - 2 z^{-1})}$ for:
(a) ROC: $|z| > 2$ (Causal).
(b) ROC: $|z| < 0.5$ (Anti-causal).
(c) ROC: $0.5 < |z| < 2$ (Two-sided).

**Solution:**
Partial fraction expansion in $z^{-1}$:
$$ X(z) = \frac{A}{1 - 0.5 z^{-1}} + \frac{B}{1 - 2 z^{-1}} $$
$$ A = \left. (1 - 0.5 z^{-1}) X(z) \right|_{z^{-1} = 2} = \frac{1}{1 - 2(2)} = -\frac{1}{3} $$
$$ B = \left. (1 - 2 z^{-1}) X(z) \right|_{z^{-1} = 0.5} = \frac{1}{1 - 0.5(0.5)} = \frac{4}{3} $$
$$ X(z) = -\frac{1/3}{1 - 0.5 z^{-1}} + \frac{4/3}{1 - 2 z^{-1}} $$

* **(a) ROC: $|z| > 2$:** Both poles are inside ROC $\implies$ Both terms causal:
  $$ x[n] = -\frac{1}{3} (0.5)^n u[n] + \frac{4}{3} (2)^n u[n] $$
* **(b) ROC: $|z| < 0.5$:** Both poles are outside ROC $\implies$ Both terms anti-causal:
  $$ x[n] = \frac{1}{3} (0.5)^n u[-n-1] - \frac{4}{3} (2)^n u[-n-1] $$
* **(c) ROC: $0.5 < |z| < 2$:** $|z| > 0.5$ (causal for $p=0.5$) and $|z| < 2$ (anti-causal for $p=2$):
  $$ x[n] = -\frac{1}{3} (0.5)^n u[n] - \frac{4}{3} (2)^n u[-n-1] $$

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
Solve the difference equation with initial conditions using the unilateral Z-transform:
$$ y[n] - 0.7 y[n-1] + 0.1 y[n-2] = x[n], \quad n \ge 0 $$
Given $x[n] = u[n]$ and initial conditions $y[-1] = 1, \; y[-2] = 2$. *(15 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Unilateral Z-transform property:**
  $\mathcal{Z}\{y[n-1]\} = z^{-1} Y(z) + y[-1]$
  $\mathcal{Z}\{y[n-2]\} = z^{-2} Y(z) + z^{-1} y[-1] + y[-2]$ *(3 Marks)*
* **Transform difference equation:**
  $[Y(z)] - 0.7 [z^{-1} Y(z) + 1] + 0.1 [z^{-2} Y(z) + z^{-1}(1) + 2] = \frac{1}{1 - z^{-1}}$
  $Y(z) [1 - 0.7 z^{-1} + 0.1 z^{-2}] - 0.7 + 0.1 z^{-1} + 0.2 = \frac{1}{1 - z^{-1}}$
  $Y(z) [1 - 0.7 z^{-1} + 0.1 z^{-2}] = 0.5 - 0.1 z^{-1} + \frac{1}{1 - z^{-1}} = \frac{(0.5 - 0.1 z^{-1})(1 - z^{-1}) + 1}{1 - z^{-1}} = \frac{1.5 - 0.6 z^{-1} + 0.1 z^{-2}}{1 - z^{-1}}$ *(4 Marks)*
* **Factor denominator:**
  $1 - 0.7 z^{-1} + 0.1 z^{-2} = (1 - 0.5 z^{-1})(1 - 0.2 z^{-1})$.
  $$ Y(z) = \frac{1.5 - 0.6 z^{-1} + 0.1 z^{-2}}{(1 - z^{-1})(1 - 0.5 z^{-1})(1 - 0.2 z^{-1})} $$ *(3 Marks)*
* **Partial Fraction Expansion:**
  $$ Y(z) = \frac{A}{1 - z^{-1}} + \frac{B}{1 - 0.5 z^{-1}} + \frac{C}{1 - 0.2 z^{-1}} $$
  * $A = \left. \frac{1.5 - 0.6(1) + 0.1(1)}{(1 - 0.5)(1 - 0.2)} \right|_{z^{-1}=1} = \frac{1.0}{0.5 \times 0.8} = \frac{1.0}{0.4} = 2.5$.
  * $B = \left. \frac{1.5 - 0.6(2) + 0.1(4)}{(1 - 2)(1 - 0.4)} \right|_{z^{-1}=2} = \frac{1.5 - 1.2 + 0.4}{(-1)(0.6)} = \frac{0.7}{-0.6} = -1.1667 = -\frac{7}{6}$.
  * $C = \left. \frac{1.5 - 0.6(5) + 0.1(25)}{(1 - 5)(1 - 2.5)} \right|_{z^{-1}=5} = \frac{1.5 - 3.0 + 2.5}{(-4)(-1.5)} = \frac{1.0}{6.0} = \frac{1}{6}$. *(3 Marks)*
* **Inverse Transform:**
  $$ y[n] = \left[ 2.5 - \frac{7}{6} (0.5)^n + \frac{1}{6} (0.2)^n \right] u[n] $$ *(2 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import numpy as np

# Simulate LCCDE iteratively
N = 10
y = np.zeros(N + 2)
y[0] = 2  # y[-2]
y[1] = 1  # y[-1]

for n in range(2, N + 2):
    y[n] = 0.7 * y[n-1] - 0.1 * y[n-2] + 1.0

n_idx = np.arange(0, N)
y_sim = y[2:]
y_analytic = 2.5 - (7/6)*(0.5**n_idx) + (1/6)*(0.2**n_idx)

print("Simulated y[n]:", np.round(y_sim[:5], 4))
print("Analytic y[n]: ", np.round(y_analytic[:5], 4))
```
