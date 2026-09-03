<Faculty Notes — Lecture 18: IIR Cascade Realization & Pole-Zero Pairing>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY
Direct form realizations of high-order IIR filters suffer from catastrophic **coefficient quantization sensitivity**: A tiny change in high-order polynomial coefficients causes large displacements of roots, often shifting poles outside the unit circle and causing instability. **Cascade realization** factors the transfer function into a product of Second-Order Sections (SOS / biquads), isolating pole pairs and guaranteeing stability.

**Pedagogical Strategy:**
1. Demonstrate polynomial root sensitivity: Why 16-bit direct form filters fail for orders $N \ge 4$.
2. Formulate the Cascade structure: $H(z) = g \prod_{k=1}^K H_k(z)$.
3. Master **Optimal Pole-Zero Pairing Rules**: Pair complex conjugate poles with the closest transmission zeros in the $z$-plane to minimize section peak-to-average gain.
4. Master **Optimal Section Ordering Rules**: Order sections in sequence of increasing $Q$-factor (increasing pole radius $r \to 1$) to maximize dynamic range and minimize register overflow.
5. Formulate $L_2$ and $L_\infty$ scaling between sections.

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Factor** high-order IIR transfer functions into second-order biquad sections (SOS).
2. **Apply** pole-zero pairing rules to minimize frequency response peaking.
3. **Order** biquad sections to optimize signal-to-noise ratio (SNR) and prevent overflow.
4. **Draw** complete Cascade realization signal flow graphs.

---
## 2. MATHEMATICAL FOUNDATIONS

### 2.1 The Cascade Realization Formulation
$$ H(z) = g \prod_{k=1}^{K} H_k(z) = g \prod_{k=1}^{K} \frac{b_{k0} + b_{k1} z^{-1} + b_{k2} z^{-2}}{1 + a_{k1} z^{-1} + a_{k2} z^{-2}}, \quad K = \lceil N/2 \rceil $$
Each biquad $H_k(z)$ realizes one real pole pair and one real zero pair:
$$ 1 + a_{k1} z^{-1} + a_{k2} z^{-2} = (1 - p_k z^{-1})(1 - p_k^* z^{-1}) = 1 - 2r_k \cos(\theta_k) z^{-1} + r_k^2 z^{-2} $$

### 2.2 Pairing and Ordering Rules
1. **Pole-Zero Pairing:**
   * Pair the complex pole pair $p_k$ having highest $Q$ (closest to unit circle) with the zero pair $z_k$ closest to it in angle $\theta$.
   * This cancels large resonance peaks, keeping the section gain $|H_k(e^{j\omega})|$ relatively flat.
2. **Section Ordering:**
   * Arrange sections in order of **increasing pole radius $r_k$** (increasing $Q$ / peaking).
   * Low-$Q$ sections first $\to$ High-$Q$ sections last.
   * Prevents premature signal saturation in early stages.

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 18.1: 4th-Order IIR Cascade Realization
**Problem:** Realize $H(z) = \frac{(1 + z^{-1})(1 - \sqrt{2} z^{-1} + z^{-2})}{(1 - 0.9 e^{j\pi/4} z^{-1})(1 - 0.9 e^{-j\pi/4} z^{-1})(1 - 0.6 z^{-1})(1 + 0.5 z^{-1})}$ in Cascade Form with optimal pairing.

**Solution:**
1. **Poles:**
   * Complex pair: $p_{1,2} = 0.9 e^{\pm j\pi/4} \implies 1 - 2(0.9)\cos(\pi/4) z^{-1} + 0.81 z^{-2} = 1 - 1.2728 z^{-1} + 0.81 z^{-2}$. (Radius $r = 0.9$, high $Q$).
   * Real poles: $p_3 = 0.6, \; p_4 = -0.5 \implies (1 - 0.6 z^{-1})(1 + 0.5 z^{-1}) = 1 - 0.1 z^{-1} - 0.3 z^{-2}$. (Low $Q$).
2. **Zeros:**
   * Complex pair: $z_{1,2} = 1 \cdot e^{\pm j\pi/4} \implies 1 - \sqrt{2} z^{-1} + z^{-2} = 1 - 1.4142 z^{-1} + z^{-2}$ (at angle $\pi/4$).
   * Real zeros: $z_3 = -1 \implies (1 + z^{-1})$.
3. **Optimal Pairing:**
   * Pair poles at angle $\pi/4$ ($p_{1,2}$) with zeros at angle $\pi/4$ ($z_{1,2}$).
   * Section 1 (Low $Q$): $H_1(z) = \frac{1 + z^{-1}}{1 - 0.1 z^{-1} - 0.3 z^{-2}}$.
   * Section 2 (High $Q$): $H_2(z) = \frac{1 - 1.4142 z^{-1} + z^{-2}}{1 - 1.2728 z^{-1} + 0.81 z^{-2}}$.
4. **Ordering:** Section 1 followed by Section 2.

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
**(a)** Why are direct form structures not suitable for implementing high-order IIR filters? Explain coefficient quantization sensitivity. *(6 Marks)*
**(b)** Realize the transfer function in Cascade Form:
$$ H(z) = \frac{1 + \frac{1}{3} z^{-1}}{\left(1 - \frac{1}{2} z^{-1}\right)\left(1 - \frac{1}{4} z^{-1} + \frac{1}{2} z^{-2}\right)} $$
Draw the complete signal flow graph using Direct Form II biquads. *(9 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Part (a):**
  * Root sensitivity explanation: Roots of $A(z)$ depend non-linearly on polynomial coefficients. In high-order polynomials, $1\%$ coefficient perturbation can displace poles by $50\%$ or move them outside $|z|=1$ *(6 Marks)*
* **Part (b):**
  * Split into 1st-order and 2nd-order sections:
    $H_1(z) = \frac{1 + \frac{1}{3} z^{-1}}{1 - \frac{1}{2} z^{-1}}, \quad H_2(z) = \frac{1}{1 - \frac{1}{4} z^{-1} + \frac{1}{2} z^{-2}}$ *(4 Marks)*
  * Neatly drawn Cascade SFG of $H_1(z)$ cascaded into $H_2(z)$ using canonical DF-II sections *(5 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import scipy.signal as signal

b = [1, 1/3]
a = np.convolve([1, -0.5], [1, -0.25, 0.5])
sos = signal.tf2sos(b, a)
print("Computed SOS:")
print(sos)
```
