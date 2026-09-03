# Lecture 20: Lattice & Lattice-Ladder Structures & Finite Word-Length Effects
## EE3621: Digital Signal Processing | III B.Tech EEE

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Convert** FIR direct form coefficients to lattice reflection coefficients $k_m$ using the step-down algorithm.
2. **Evaluate** IIR filter stability directly from reflection coefficients.
3. **Construct** signal flow graphs for FIR lattice and IIR lattice-ladder filters.
4. **Quantify** round-off noise power and identify limit cycle conditions.

---
## 2. MATHEMATICAL FOUNDATIONS

### 2.1 FIR Lattice Recursion & Step-Down Algorithm
* **Lattice Recursion:**
  $$ A_m(z) = A_{m-1}(z) + k_m z^{-1} B_{m-1}(z) $$
  $$ B_m(z) = z^{-m} A_m(z^{-1}) \quad (\text{Reverse Polynomial}) $$
* **Step-Down Algorithm (Direct $\to$ Lattice):**
  Given $A_N(z) = 1 + \sum_{i=1}^N \alpha_N(i) z^{-i}$:
  1. Set $k_N = \alpha_N(N)$.
  2. For $m = N, N-1, \dots, 2$:
     $$ \alpha_{m-1}(i) = \frac{\alpha_m(i) - k_m \alpha_m(m - i)}{1 - k_m^2}, \quad i = 1, 2, \dots, m-1 $$
     $$ k_{m-1} = \alpha_{m-1}(m-1) $$

### 2.3 Finite Word-Length Effects Summary
1. **Coefficient Quantization:** Shifts poles in the $z$-plane; high-order direct forms are severely sensitive; lattice and cascade forms are highly robust.
2. **Round-off Noise:** Fixed-point truncation error modeled as white noise with variance $\sigma_e^2 = \frac{2^{-2B}}{12}$ for $B$-bit quantization. Output noise power:
   $$ \sigma_{y}^2 = \sigma_e^2 \sum_{n=0}^{\infty} |h[n]|^2 = \sigma_e^2 \frac{1}{2\pi j} \oint H(z) H(z^{-1}) z^{-1} dz $$
3. **Limit Cycle Oscillations:** Nonlinear oscillations in recursive filters caused by arithmetic quantization (deadbands) and two's complement overflow. Mitigated by using saturation arithmetic.

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 20.1: Step-Down Conversion to Reflection Coefficients
**Problem:** Find the reflection coefficients $k_1, k_2, k_3$ for the FIR filter:
$$ A_3(z) = 1 - 0.9 z^{-1} + 0.64 z^{-2} - 0.5 z^{-3} $$

**Solution:**
* **Stage 3:**
  $k_3 = \alpha_3(3) = -0.5$.
  $1 - k_3^2 = 1 - (-0.5)^2 = 1 - 0.25 = 0.75$.
* **Compute $\alpha_2(i)$ for $m=3$:**
  * $\alpha_2(1) = \frac{\alpha_3(1) - k_3 \alpha_3(2)}{0.75} = \frac{-0.9 - (-0.5)(0.64)}{0.75} = \frac{-0.9 + 0.32}{0.75} = \frac{-0.58}{0.75} = -0.7733$.
  * $\alpha_2(2) = \frac{\alpha_3(2) - k_3 \alpha_3(1)}{0.75} = \frac{0.64 - (-0.5)(-0.9)}{0.75} = \frac{0.64 - 0.45}{0.75} = \frac{0.19}{0.75} = 0.2533$.
  $k_2 = \alpha_2(2) = 0.2533$.
* **Stage 2:**
  $1 - k_2^2 = 1 - (0.2533)^2 = 1 - 0.0642 = 0.9358$.
* **Compute $\alpha_1(i)$ for $m=2$:**
  * $\alpha_1(1) = \frac{\alpha_2(1) - k_2 \alpha_2(1)}{0.9358} = \frac{-0.7733(1 - 0.2533)}{0.9358} = \frac{-0.7733 \times 0.7467}{0.9358} = -0.6170$.
  $k_1 = \alpha_1(1) = -0.6170$.
* **Stability Check:**
  $|k_1| = 0.6170 < 1, \; |k_2| = 0.2533 < 1, \; |k_3| = 0.5000 < 1$.
  All $|k_m| < 1 \implies$ The corresponding all-pole filter is **Stable**.

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
**(a)** State the Schur-Cohn stability criterion for digital filters. Using the step-down algorithm, determine if the system is stable:
$$ H(z) = \frac{1}{1 - 1.2 z^{-1} + 0.8 z^{-2} - 0.2 z^{-3}} $$
*(9 Marks)*
**(b)** Discuss limit cycle oscillations in recursive digital filters. Explain the difference between zero-input granular limit cycles and overflow oscillations. *(6 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Part (a):**
  * Statement of Schur-Cohn criterion: All $|k_m| < 1$ *(2 Marks)*
  * Step-down execution:
    $k_3 = -0.2 \implies 1 - k_3^2 = 0.96$
    $\alpha_2(1) = \frac{-1.2 - (-0.2)(0.8)}{0.96} = \frac{-1.04}{0.96} = -1.0833$
    $\alpha_2(2) = \frac{0.8 - (-0.2)(-1.2)}{0.96} = \frac{0.56}{0.96} = 0.5833 \implies k_2 = 0.5833$
    $1 - k_2^2 = 1 - 0.3403 = 0.6597$
    $\alpha_1(1) = \frac{-1.0833 - (0.5833)(-1.0833)}{0.6597} = \frac{-1.0833(0.4167)}{0.6597} = -0.6843 \implies k_1 = -0.6843$ *(5 Marks)*
  * Since $|k_1| = 0.6843 < 1, |k_2| = 0.5833 < 1, |k_3| = 0.2 < 1 \implies$ **Stable** *(2 Marks)*
* **Part (b):**
  * Explanation of granular limit cycles due to quantization rounding *(3 Marks)*
  * Explanation of overflow oscillations and mitigation via saturation arithmetic *(3 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import numpy as np

# Verify step-down conversion
a = np.array([1.0, -1.2, 0.8, -0.2])
roots = np.roots(a)
print("Pole Magnitudes:", np.abs(roots))
print("All inside unit circle:", np.all(np.abs(roots) < 1.0))
```
