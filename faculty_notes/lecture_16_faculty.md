<Faculty Notes — Lecture 16: Linear-Phase FIR & Frequency-Sampling Realization>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY
Linear-phase FIR filters possess coefficient symmetry that allows hardware multipliers to be reduced by approximately 50%. In addition, the **Frequency-Sampling Realization** provides a recursive implementation of FIR filters using an all-zero comb filter and a bank of all-pole discrete resonators.

**Pedagogical Strategy:**
1. Prove how symmetry $h[n] = h[M-1-n]$ allows input samples to be pre-added before multiplication, cutting hardware multipliers from $M$ to $\lfloor M/2 \rfloor + 1$.
2. Formulate the Linear-Phase Direct Form structure for both even and odd filter lengths.
3. Derive the Frequency-Sampling Transfer Function:
   $$ H(z) = \frac{1 - z^{-M}}{M} \sum_{k=0}^{M-1} \frac{H[k]}{1 - W_M^{-k} z^{-1}} $$
4. Explain the physical mechanism: The comb filter $(1 - z^{-M})$ places $M$ zeros on the unit circle at $z = e^{j 2\pi k / M}$, while the resonator poles cancel the zeros at specific bin locations.
5. Address practical engineering issues: Pole-zero cancellation sensitivity on $|z|=1$ and stability under coefficient quantization (damping factor $r = 0.999 \approx 1$).

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Design** Linear-Phase FIR structures with 50% reduced multiplier count.
2. **Derive** the Frequency-Sampling filter realization equations from the IDFT formulation.
3. **Construct** signal flow graphs for frequency-sampling FIR filters.
4. **Evaluate** computational efficiency for narrowband filters with few non-zero DFT bins.

---
## 2. MATHEMATICAL FOUNDATIONS

### 2.1 Linear-Phase Multiplier Reduction
For a symmetric FIR filter of length $M$ ($h[n] = h[M-1-n]$):
* **Odd Length $M$ (Order $N = M-1$ Even):**
  $$ y[n] = \sum_{k=0}^{(M-3)/2} h[k] (x[n-k] + x[n - M + 1 + k]) + h\left[\frac{M-1}{2}\right] x\left[n - \frac{M-1}{2}\right] $$
  Total multipliers: $\frac{M+1}{2}$.
* **Even Length $M$ (Order $N = M-1$ Odd):**
  $$ y[n] = \sum_{k=0}^{M/2 - 1} h[k] (x[n-k] + x[n - M + 1 + k]) $$
  Total multipliers: $\frac{M}{2}$.

### 2.2 Frequency-Sampling Structure Derivation
Express the FIR transfer function in terms of its $M$-point DFT samples $H[k]$:
$$ h[n] = \frac{1}{M} \sum_{k=0}^{M-1} H[k] W_M^{-nk} $$
$$ H(z) = \sum_{n=0}^{M-1} h[n] z^{-n} = \sum_{n=0}^{M-1} \left( \frac{1}{M} \sum_{k=0}^{M-1} H[k] W_M^{-nk} \right) z^{-n} = \frac{1}{M} \sum_{k=0}^{M-1} H[k] \sum_{n=0}^{M-1} (W_M^{-k} z^{-1})^n $$
Using the finite geometric sum $\sum_{n=0}^{M-1} u^n = \frac{1 - u^M}{1 - u}$, and since $(W_M^{-k} z^{-1})^M = W_M^{-kM} z^{-M} = 1 \cdot z^{-M} = z^{-M}$:
$$ H(z) = \frac{1 - z^{-M}}{M} \sum_{k=0}^{M-1} \frac{H[k]}{1 - W_M^{-k} z^{-1}} $$
* **Comb Filter:** $H_{\text{comb}}(z) = \frac{1 - z^{-M}}{M}$ (FIR, zeros at $z = e^{j 2\pi k / M}$).
* **Resonator Bank:** $H_k(z) = \frac{H[k]}{1 - W_M^{-k} z^{-1}}$ (All-pole, pole at $z = e^{j 2\pi k / M}$).

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 16.1: Linear-Phase FIR Structure
**Problem:** Draw the linear-phase direct form structure for an FIR filter with impulse response $h[n] = \{ \underset{\uparrow}{1}, 2, 3, 2, 1 \}$ ($M=5$).

**Solution:**
* Length $M = 5$ (Odd).
* Symmetry: $h[0] = h[4] = 1, \; h[1] = h[3] = 2, \; h[2] = 3$.
* Output equation:
  $$ y[n] = 1 \cdot (x[n] + x[n-4]) + 2 \cdot (x[n-1] + x[n-3]) + 3 \cdot x[n-2] $$
* **Hardware Count:**
  * Multipliers: $\frac{5+1}{2} = 3$ (compared to 5 in standard direct form).
  * Adders: $2 \text{ (pre-additions)} + 2 \text{ (accumulation)} = 4$.
  * Delays: 4 registers $z^{-1}$.

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
**(a)** Derive the Frequency-Sampling structure for an FIR filter. Explain how pole-zero cancellation is achieved. *(8 Marks)*
**(b)** Draw the linear-phase realization for an FIR filter of length $M=6$ with $h[n] = \{ \underset{\uparrow}{-1}, 2, 4, 4, 2, -1 \}$. *(7 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Part (a):**
  * Complete IDFT substitution and geometric series derivation *(5 Marks)*
  * Explanation of comb zeros cancelling resonator poles on $|z|=1$, and damping factor $r \lesssim 1$ for numerical stability *(3 Marks)*
* **Part (b):**
  * $M=6$ (Even length, symmetric):
    $y[n] = -1(x[n] + x[n-5]) + 2(x[n-1] + x[n-4]) + 4(x[n-2] + x[n-3])$ *(3 Marks)*
  * Multipliers required: $6/2 = 3$.
  * Neatly drawn SFG with 5 delay elements, 3 pre-adders, 3 multipliers, and accumulator bus *(4 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import numpy as np

# Verify linear-phase convolution equivalence
h = np.array([1, 2, 3, 2, 1])
x = np.array([1, 1, 1, 1, 1])
y = np.convolve(x, h)
print("Convolution Output:", y)
```
