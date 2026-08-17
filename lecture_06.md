# Lecture 6: Inverse Z-Transform \& Stability Analysis

**Course:** EE3621 — Digital Signal Processing  
**Target Audience:** III B.Tech EEE Students  
**Duration:** 40 Minutes  

* **Available Formats:** [LaTeX Source File](file:///C:/Users/sriph/Downloads/DSP/lecture_06.tex) | [Compiled PDF Notes](file:///C:/Users/sriph/Downloads/DSP/lecture_06.pdf)

---

## 1. Lecture Plan (40 Minutes Breakdown)
* **00:00 – 05:00 (5 mins):** Motivation: Why do we need the Inverse Z-transform? Uniqueness of ROC.
* **05:00 – 18:00 (13 mins):** Method 1: Partial Fraction Expansion (Distinct and Repeated Poles).
* **18:00 – 25:00 (7 mins):** Method 2: Power Series Expansion (Long Division for causal vs. anti-causal).
* **25:00 – 30:00 (5 mins):** Method 3: Contour Integration (Residue Theorem).
* **30:00 – 38:00 (8 mins):** Stability \& Causality Analysis of LTI Systems based on poles.
* **38:00 – 40:00 (2 mins):** Checkpoint & Summary.

---

## 2. Overview of the Inverse Z-Transform

The Z-transform maps a sequence $x[n]$ to $X(z)$. The **Inverse Z-Transform** recovers the discrete-time sequence $x[n]$ from $X(z)$ and its associated Region of Convergence (ROC):

$$x[n] = \mathcal{Z}^{-1}\{X(z)\}$$

Without the ROC, the inverse Z-transform is **not unique**. For example, the algebraic expression $X(z) = \frac{z}{z-a}$ corresponds to:
* $x[n] = a^n u[n]$ if the ROC is $|z| > |a|$ (causal).
* $x[n] = -a^n u[-n-1]$ if the ROC is $|z| < |a|$ (anti-causal).

Therefore, **always specify the ROC** when performing inverse Z-transforms.

---

## 3. Method 1: Partial Fraction Expansion

This is the most common method for rational system functions. We expand $X(z)/z$ into a sum of simpler terms whose inverse transforms are known.

### A. Case 1: Distinct Poles
If $\frac{X(z)}{z}$ has distinct poles $p_1, p_2, \dots, p_N$:
$$\frac{X(z)}{z} = \frac{A_1}{z-p_1} + \frac{A_2}{z-p_2} + \dots + \frac{A_N}{z-p_N}$$
where the residues $A_i$ are found using the cover-up method:
$$A_i = \left[ (z - p_i) \frac{X(z)}{z} \right]_{z = p_i}$$

### B. Case 2: Repeated Poles
If $\frac{X(z)}{z}$ contains a pole $p_1$ repeated $m$ times:
$$\frac{X(z)}{z} = \frac{A_{11}}{z-p_1} + \frac{A_{12}}{(z-p_1)^2} + \dots + \frac{A_{1m}}{(z-p_1)^m} + \sum_{k=2}^{N} \frac{A_k}{z-p_k}$$
The coefficients for the repeated poles are computed using derivatives:
$$A_{1k} = \frac{1}{(m-k)!} \left[ \frac{d^{m-k}}{dz^{m-k}} \left( (z - p_1)^m \frac{X(z)}{z} \right) \right]_{z = p_1}$$
Once all residues are computed, we multiply back by $z$ to form terms like $\frac{A_j z}{z-p_j} \longleftrightarrow A_j p_j^n u[n]$ or $\frac{A z}{(z-p)^2} \longleftrightarrow A n p^{n-1} u[n]$.

---

## 4. Method 2: Power Series Expansion (Long Division)

This method is useful when only the first few values of $x[n]$ are required or when $X(z)$ is difficult to factor. We expand $X(z)$ directly as a power series:

$$X(z) = \sum_{n=-\infty}^{\infty} x[n] z^{-n} = \dots + x[-1]z^1 + x[0] + x[1]z^{-1} + x[2]z^{-2} + \dots$$

The coefficients of $z^{-n}$ are the time samples $x[n]$.
* **For a causal sequence ($|z| > |a|$):** Arrange numerator and denominator in descending powers of $z$ (or ascending powers of $z^{-1}$) and perform division to get a series of the form $x[0] + x[1]z^{-1} + x[2]z^{-2} + \dots$.
* **For an anti-causal sequence ($|z| < |a|$):** Arrange numerator and denominator in ascending powers of $z$ (or descending powers of $z^{-1}$) and perform division to get a series of the form $x[-1]z^1 + x[-2]z^2 + \dots$.

---

## 5. Method 3: Contour Integration (Residue Method)

The formal definition of the inverse Z-transform is a contour integral in the complex plane:

$$x[n] = \frac{1}{2\pi j} \oint_{C} X(z) z^{n-1} dz$$

where $C$ is a counterclockwise closed path in the ROC of $X(z)$ circling the origin.
Using Cauchy's Residue Theorem, the integral is computed as:
$$x[n] = \sum \text{Residues of } \left[ X(z) z^{n-1} \right] \text{ at the poles inside } C$$
The residue of a pole $z = p$ of order $m$ is found using:
$$\text{Res}\left\{ X(z) z^{n-1} \right\}_{z=p} = \frac{1}{(m-1)!} \lim_{z \to p} \frac{d^{m-1}}{dz^{m-1}} \left[ (z-p)^m X(z) z^{n-1} \right]$$

---

## 6. Stability, Causality \& Pole Locations

For a discrete LTI system, the transfer function is $H(z) = \frac{Y(z)}{X(z)}$, which is the Z-transform of the impulse response $h[n]$.

### A. Causality
A system is causal if $h[n] = 0$ for $n < 0$. This requires the ROC of $H(z)$ to be the exterior of the outermost pole:
$$|z| > p_{max}$$

### B. BIBO Stability
A system is stable if and only if the ROC of $H(z)$ contains the unit circle ($|z| = 1$).

### C. Pole-Zero Stability Criterion
For a causal LTI system to be stable, the ROC $|z| > p_{max}$ must contain the unit circle. This is satisfied if and only if **all poles of $H(z)$ lie strictly inside the unit circle**:
$$|p_i| < 1 \quad \forall i$$

Below are the pole location stability regions in the complex z-plane:

![Stability Regions](images/pole_zero_stability_l6.png)

Below are the four possible impulse response profiles based on pole location and ROC causality choice:

* **Left panel (Green)**: Causal stable ($|p| < 1$, decaying) and anti-causal stable ($|p| > 1$, decaying for $n \to -\infty$).
* **Right panel (Red)**: Causal unstable ($|p| > 1$, expanding) and anti-causal unstable ($|p| < 1$, expanding for $n \to -\infty$).

---

## 7. Checkpoint \& Quick Review Questions

1. **Q1:** Find the inverse Z-transform of $H(z) = \frac{z^2}{(z - 0.5)(z - 2)}$ for the stable ROC: $0.5 < |z| < 2$.
   * *Answer:*
     1. Divide by $z$:
        $$\frac{H(z)}{z} = \frac{z}{(z-0.5)(z-2)} = \frac{A}{z-0.5} + \frac{B}{z-2}$$
     2. Calculate residues:
        $$A = \left[ \frac{z}{z-2} \right]_{z=0.5} = \frac{0.5}{0.5-2} = -\frac{1}{3}$$
        $$B = \left[ \frac{z}{z-0.5} \right]_{z=2} = \frac{2}{2-0.5} = \frac{4}{3}$$
     3. Reconstruct $H(z)$:
        $$H(z) = -\frac{1}{3} \frac{z}{z-0.5} + \frac{4}{3} \frac{z}{z-2}$$
     4. Find $h[n]$ using the ROC $0.5 < |z| < 2$:
        * For the pole at $z = 0.5$, the ROC $|z| > 0.5$ implies a **causal** sequence: $-\frac{1}{3} (0.5)^n u[n]$.
        * For the pole at $z = 2$, the ROC $|z| < 2$ implies an **anti-causal** sequence: $-\frac{4}{3} (2)^n u[-n-1]$.
     5. Combining them:
        $$h[n] = -\frac{1}{3} (0.5)^n u[n] - \frac{4}{3} (2)^n u[-n-1]$$

2. **Q2:** Find the first three terms of the causal sequence corresponding to $X(z) = \frac{1}{1 - 0.5 z^{-1}}$ using long division.
   * *Answer:*
     Perform long division of $1$ by $1 - 0.5 z^{-1}$:
     * Step 1: $1 / (1 - 0.5 z^{-1}) \implies$ quotient is $1$, remainder is $0.5 z^{-1}$.
     * Step 2: $0.5 z^{-1} / (1 - 0.5 z^{-1}) \implies$ quotient is $0.5 z^{-1}$, remainder is $0.25 z^{-2}$.
     * Step 3: $0.25 z^{-2} / (1 - 0.5 z^{-1}) \implies$ quotient is $0.25 z^{-2}$, remainder is $0.125 z^{-3}$.
     * Result: $X(z) = 1 + 0.5 z^{-1} + 0.25 z^{-2} + \dots$
     * Thus, $x[0] = 1$, $x[1] = 0.5$, and $x[2] = 0.25$.


---

### Visual Illustration: Z-Plane Stability Regions & Pole Dynamics

* **Physical Insight:** 
  - **Inside Unit Circle ($|z| < 1$):** Poles generate decaying modes ($|p|^n 	o 0$ as $n 	o \infty$), guaranteeing bounded-input bounded-output (BIBO) stability.
  - **On Unit Circle ($|z| = 1$):** Poles generate sustained oscillations or step functions without decaying (Marginal Stability / Oscillators).
  - **Outside Unit Circle ($|z| > 1$):** Poles produce exponentially explosive modes ($|p|^n 	o \infty$), causing immediate system saturation/overflow.

---

### Visual Illustration: Impulse Response Modes Across the Z-Plane

* **Waveform Characteristics:**
  - **Positive Real Pole ($z=0.7$):** Smooth monotonic exponential decay.
  - **Negative Real Pole ($z=-0.7$):** Alternating sign ($\pm$) decaying oscillation with frequency $\omega = \pi$.
  - **Complex Conjugate Pair ($0.8 e^{\pm j\pi/4}$):** Damped sinusoidal oscillation with envelope decay $0.8^n$.
  - **Unit Circle Conjugate Pair ($e^{\pm j\pi/4}$):** Pure undamped sinusoidal oscillation with permanent energy.

---

### Visual Illustration: Partial Fraction Expansion Decomposition

![Partial Fraction Expansion Mode Decomposition](images/pfe_decomposition_modes.png)

* **Linear Superposition:** The overall system impulse response $h[n] = 2(0.8)^n u[n] - (0.4)^n u[n]$ is the exact linear superposition of its individual first-order pole modes.
