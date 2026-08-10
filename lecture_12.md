# Lecture 12: IIR Filter Design — Analog Prototype & Bilinear Transform

**Course:** EE3621 — Digital Signal Processing  
**Target Audience:** III B.Tech EEE Students  
**Duration:** 40 Minutes  

* **Available Formats:** [LaTeX Source File](file:///C:/Users/sriph/Downloads/DSP/lecture_12.tex) | [Compiled PDF Notes](file:///C:/Users/sriph/Downloads/DSP/lecture_12.pdf)

---

## 1. Lecture Plan (40 Minutes Breakdown)

* **00:00 – 05:00 (5 mins):** **IIR Design Philosophy** — Introduction to the concept of borrowing from continuous-time analog filter theory to build digital filters.
* **05:00 – 15:00 (10 mins):** **Analog Prototypes** — Detailed exploration of Butterworth, Chebyshev (Types I & II), and Elliptic filters.
* **15:00 – 20:00 (5 mins):** **Impulse Invariance Method** — The time-domain approach to mapping continuous to discrete time.
* **20:00 – 28:00 (8 mins):** **The Bilinear Transform (BLT)** — Frequency-domain approach, derivation of the mapping, and frequency warping.
* **28:00 – 35:00 (7 mins):** **Bilinear Design Procedure & Worked Example** — Designing a 3rd-order digital Butterworth filter from scratch.
* **35:00 – 40:00 (5 mins):** **Checkpoints & Summary** — Quick questions to reinforce learning and evaluate understanding.

---

## 2. IIR Design Philosophy

The design of Infinite Impulse Response (IIR) digital filters is fundamentally different from Finite Impulse Response (FIR) design. Instead of designing directly in the discrete-time domain, we leverage decades of well-established analog filter design theory. 

The standard IIR design philosophy follows these steps:
1. **Specification:** Start with discrete-time filter specifications (passband ripple, stopband attenuation, cutoff frequencies).
2. **Pre-warping:** Convert the discrete-time frequency specifications into continuous-time (analog) specifications.
3. **Analog Design:** Design a continuous-time analog prototype filter (e.g., Butterworth, Chebyshev) that meets these analog specifications. This yields an analog transfer function $H_a(s)$.
4. **Transformation:** Map the analog transfer function $H_a(s)$ to a digital transfer function $H(z)$ using a mapping technique (such as the Bilinear Transform).

This indirect approach is used because closed-form formulas exist for analog filter poles and polynomials, making the process purely algebraic and highly robust.

---

## 3. Butterworth Analog Prototype

The Butterworth filter is known as the **maximally flat** magnitude filter. Its response is as flat as mathematically possible in the passband and rolls off monotonically in the stopband.

### 3.1 Magnitude Response
The squared magnitude response of an $N$-th order analog Butterworth lowpass filter is given by:

$$ |H_a(j\Omega)|^2 = \frac{1}{1 + \left(\frac{\Omega}{\Omega_c}\right)^{2N}} $$

where:
* $\Omega$ is the analog frequency (rad/s).
* $\Omega_c$ is the 3-dB cutoff frequency.
* $N$ is the filter order.

### 3.2 Derivation of Pole Locations
To find the poles of the transfer function, we extend the frequency variable $j\Omega$ to the complex $s$-plane by setting $s = j\Omega$, which implies $\Omega = s/j = -js$. 

Substitute this into the magnitude squared equation. Note that $|H_a(j\Omega)|^2 = H_a(j\Omega)H_a(-j\Omega)$, so:

$$ H_a(s) H_a(-s) = \frac{1}{1 + \left(\frac{s/j}{\Omega_c}\right)^{2N}} $$
$$ H_a(s) H_a(-s) = \frac{1}{1 + \frac{s^{2N}}{j^{2N} \Omega_c^{2N}}} $$

Since $j^{2N} = (j^2)^N = (-1)^N$, we have:

$$ H_a(s) H_a(-s) = \frac{1}{1 + (-1)^N \left(\frac{s}{\Omega_c}\right)^{2N}} $$

To find the poles, we set the denominator to zero:

$$ 1 + (-1)^N \left(\frac{s}{\Omega_c}\right)^{2N} = 0 $$
$$ \left(\frac{s}{\Omega_c}\right)^{2N} = -(-1)^{-N} = (-1)^{N-1} $$

We can express $(-1)^{N-1}$ in polar form as $e^{j\pi(2k + N - 1)}$ for integer $k$. Taking the $2N$-th root yields the pole locations:

$$ s_k = \Omega_c e^{j\frac{\pi(2k + N - 1)}{2N}}, \quad \text{for } k = 1, 2, \dots, 2N $$

**Physical Intuition:** 
These $2N$ poles lie exactly on a circle of radius $\Omega_c$ in the $s$-plane. For a stable, causal filter $H_a(s)$, we must select the $N$ poles that lie strictly in the left half of the $s$-plane (LHP).

Thus, the stable poles are:
$$ s_k = \Omega_c e^{j\frac{\pi}{2N}(2k + N - 1)}, \quad \text{for } k = 1, 2, \dots, N $$

### 3.3 Derivation of Order Formula
Let the filter specifications be:
* Passband maximum attenuation $A_p$ at frequency $\Omega_p$.
* Stopband minimum attenuation $A_s$ at frequency $\Omega_s$.

From the magnitude response:
$$ A_p^2 = 1 + \left(\frac{\Omega_p}{\Omega_c}\right)^{2N} \implies \left(\frac{\Omega_p}{\Omega_c}\right)^{2N} = A_p^2 - 1 $$
$$ A_s^2 = 1 + \left(\frac{\Omega_s}{\Omega_c}\right)^{2N} \implies \left(\frac{\Omega_s}{\Omega_c}\right)^{2N} = A_s^2 - 1 $$

Taking the ratio of the two equations:
$$ \left(\frac{\Omega_s}{\Omega_p}\right)^{2N} = \frac{A_s^2 - 1}{A_p^2 - 1} $$

Taking the base-10 logarithm on both sides:
$$ 2N \log_{10}\left(\frac{\Omega_s}{\Omega_p}\right) = \log_{10}\left(\frac{A_s^2 - 1}{A_p^2 - 1} \right) $$

**KEY RESULT - Order Formula:**
$$ N \geq \frac{\log_{10}\left( \frac{A_s^2 - 1}{A_p^2 - 1} \right)}{2 \log_{10}\left( \frac{\Omega_s}{\Omega_p} \right)} $$

---

## 4. Chebyshev and Elliptic Prototypes

When flat passbands are not strictly required, we can allow ripple to achieve a steeper roll-off (transition band) for a given order $N$.

### 4.1 Chebyshev Type I
Chebyshev Type I filters have an equiripple response in the passband and are monotonically decreasing in the stopband. The magnitude squared response is:

$$ |H(j\Omega)|^2 = \frac{1}{1 + \epsilon^2 C_N^2\left(\frac{\Omega}{\Omega_p}\right)} $$

Where $\epsilon$ controls the passband ripple, and $C_N(x)$ is the $N$-th order Chebyshev polynomial defined as:
$$ C_N(x) = \cos(N \cos^{-1} x), \quad \text{for } |x| \leq 1 $$
$$ C_N(x) = \cosh(N \cosh^{-1} x), \quad \text{for } |x| > 1 $$

The poles of a Chebyshev Type I filter do not lie on a circle, but rather on an **ellipse** in the left half of the $s$-plane.

### 4.2 Chebyshev Type II
Chebyshev Type II filters have a monotonic passband and an equiripple stopband. They are designed using an inverse Chebyshev polynomial. 
The magnitude squared response is:

$$ |H(j\Omega)|^2 = \frac{1}{1 + \left[ \epsilon^2 C_N^2\left(\frac{\Omega_s}{\Omega}\right) \right]^{-1}} $$

These filters contain both poles and zeros. The zeros lie directly on the $j\Omega$ axis, which creates the deep nulls (equiripple behavior) in the stopband.

### 4.3 Elliptic (Cauer) Filters
Elliptic filters provide equiripple behavior in **both** the passband and the stopband. 
For a given set of specifications, an Elliptic filter will always yield the **minimum possible order $N$**.

The magnitude response is defined using Jacobian elliptic functions $U_N(x)$:
$$ |H(j\Omega)|^2 = \frac{1}{1 + \epsilon^2 U_N^2\left(\frac{\Omega}{\Omega_p}\right)} $$
Because the math involves complex elliptic integrals, practical designs rely heavily on software (like MATLAB's `ellip` function).

---

## 5. Comparison Table of Analog Prototypes

| Filter Type | Passband Behavior | Stopband Behavior | Phase Linearity | Order $N$ Required |
| :--- | :--- | :--- | :--- | :--- |
| **Butterworth** | Maximally Flat | Monotonic | Best of the four | Highest |
| **Chebyshev I** | Equiripple | Monotonic | Moderate | Lower than Butterworth |
| **Chebyshev II** | Monotonic | Equiripple | Moderate | Lower than Butterworth |
| **Elliptic** | Equiripple | Equiripple | Very Non-linear | **Lowest** |

---

## 6. The Impulse Invariance Method

The Impulse Invariance Method (IIM) converts an analog filter to a digital filter such that the digital filter's impulse response is a directly sampled version of the analog filter's impulse response.

$$ h[n] = T_s \, h_a(nT_s) $$

### 6.1 Pole Mapping
If the analog transfer function is expanded via partial fractions:
$$ H_a(s) = \sum_{k=1}^N \frac{A_k}{s - s_k} $$
The corresponding analog impulse response is:
$$ h_a(t) = \sum_{k=1}^N A_k e^{s_k t} u(t) $$
Sampling at $t = nT_s$:
$$ h[n] = T_s \sum_{k=1}^N A_k e^{s_k n T_s} u[n] = T_s \sum_{k=1}^N A_k (e^{s_k T_s})^n u[n] $$
Taking the Z-transform yields:
$$ H(z) = \sum_{k=1}^N \frac{T_s A_k}{1 - e^{s_k T_s} z^{-1}} $$

**KEY RESULT - IIM Mapping:**
Each analog pole $s_k$ maps directly to a digital pole $z_k = e^{s_k T_s}$.

### 6.2 The Aliasing Problem
Because IIM is based on time-domain sampling, it is inherently subject to **aliasing** if the analog filter is not strictly bandlimited. Since no practical analog filter is perfectly bandlimited, there is always some aliasing.
**Engineering Intuition:** IIM is only suitable for lowpass and bandpass filters with narrow bandwidths where the high-frequency content is negligible. It is totally unsuitable for highpass or bandstop filters.

---

## 7. The Bilinear Transform (BLT)

To avoid aliasing, we need a mapping that takes the entire $j\Omega$ axis ($-\infty < \Omega < \infty$) and maps it exactly once around the unit circle ($-\pi \leq \omega \leq \pi$). The Bilinear Transform achieves this via a rational conformal mapping.

### 7.1 The Transform Definition
The BLT approximates the integration of the continuous-time differential equation using the trapezoidal rule. The resulting algebraic substitution is:
$$ s = \frac{2}{T_s} \frac{1 - z^{-1}}{1 + z^{-1}} = \frac{2}{T_s} \frac{z - 1}{z + 1} $$

Conversely, to map from $s$ to $z$:
$$ z = \frac{1 + (T_s/2)s}{1 - (T_s/2)s} $$

### 7.2 Proof of Stability Preservation
Let $s = \sigma + j\Omega$. Then:
$$ z = \frac{1 + (T_s/2)(\sigma + j\Omega)}{1 - (T_s/2)(\sigma + j\Omega)} $$
$$ |z|^2 = \frac{[1 + (T_s/2)\sigma]^2 + [(T_s/2)\Omega]^2}{[1 - (T_s/2)\sigma]^2 + [(T_s/2)\Omega]^2} $$
* If $\sigma < 0$ (LHP), then $(1 + (T_s/2)\sigma)^2 < (1 - (T_s/2)\sigma)^2$, so $|z| < 1$ (inside unit circle).
* If $\sigma = 0$ ($j\Omega$ axis), then $|z| = 1$ (on the unit circle).
* If $\sigma > 0$ (RHP), then $|z| > 1$ (outside unit circle).

Thus, a stable analog filter perfectly maps to a stable digital filter!

### 7.3 Frequency Warping
Let us map the analog frequency axis to the digital frequency axis by substituting $s = j\Omega$ and $z = e^{j\omega}$:
$$ j\Omega = \frac{2}{T_s} \frac{e^{j\omega} - 1}{e^{j\omega} + 1} $$
Factor out $e^{j\omega/2}$:
$$ j\Omega = \frac{2}{T_s} \frac{e^{j\omega/2}(e^{j\omega/2} - e^{-j\omega/2})}{e^{j\omega/2}(e^{j\omega/2} + e^{-j\omega/2})} $$
$$ j\Omega = \frac{2}{T_s} \frac{2j \sin(\omega/2)}{2 \cos(\omega/2)} = j \frac{2}{T_s} \tan\left(\frac{\omega}{2}\right) $$

**KEY RESULT - Warping Equation:**
$$ \Omega = \frac{2}{T_s} \tan\left(\frac{\omega}{2}\right) $$
Because the infinite analog frequency range maps to a finite digital frequency range $[-\pi, \pi]$, the high frequencies are highly compressed (warped). To fix this, we must **prewarp** our critical frequencies before designing the analog prototype.

---

## 8. Bilinear Design Procedure Step-by-Step

1. **Given:** Digital specifications $\omega_p$ and $\omega_s$.
2. **Prewarping:** Compute analog specifications $\Omega_p = \frac{2}{T_s} \tan(\omega_p/2)$ and $\Omega_s = \frac{2}{T_s} \tan(\omega_s/2)$. (Often, $T_s = 2$ is chosen to simplify math).
3. **Prototype Design:** Determine $N$ and $\Omega_c$, then find $H_a(s)$.
4. **BLT Conversion:** Substitute $s = \frac{2}{T_s} \frac{z-1}{z+1}$ into $H_a(s)$ to get $H(z)$.
5. **Verification:** Check that $H(z)$ meets the original digital specifications.

---

## 9. Worked Example: 3rd-Order Digital Butterworth LPF

**Problem:** Design a 3rd-order digital Butterworth lowpass filter with a 3-dB cutoff frequency $\omega_c = 0.3\pi$ using the Bilinear Transform.

**Step 1: Prewarping**
Let $T_s = 2$ for mathematical simplicity.
$$ \Omega_c = \frac{2}{2} \tan\left(\frac{0.3\pi}{2}\right) = \tan(0.15\pi) \approx 0.5095 \text{ rad/s} $$

**Step 2: Analog Prototype Design**
For a 3rd-order Butterworth ($N=3$), the stable poles are:
$$ s_k = \Omega_c e^{j\frac{\pi}{6}(2k + 2)}, \quad k = 1, 2, 3 $$
Calculating the poles:
* $k=1: \quad s_1 = \Omega_c e^{j\frac{4\pi}{6}} = \Omega_c \left(\cos(120^\circ) + j\sin(120^\circ)\right) = 0.5095 (-0.5 + j0.866) = -0.2548 + j0.4412$
* $k=2: \quad s_2 = \Omega_c e^{j\pi} = \Omega_c (-1) = -0.5095$
* $k=3: \quad s_3 = \Omega_c e^{j\frac{8\pi}{6}} = \Omega_c \left(\cos(240^\circ) + j\sin(240^\circ)\right) = 0.5095 (-0.5 - j0.866) = -0.2548 - j0.4412$

The analog transfer function is:
$$ H_a(s) = \frac{\Omega_c^3}{(s - s_1)(s - s_2)(s - s_3)} $$
Since $(s - s_1)(s - s_3) = (s - (-0.2548 + j0.4412))(s - (-0.2548 - j0.4412)) = (s + 0.2548)^2 + (0.4412)^2 = s^2 + 0.5096s + 0.2596$
And $s_2 = -0.5095$:
$$ H_a(s) = \frac{\Omega_c^3}{(s + 0.5095)(s^2 + 0.5096s + 0.2596)} $$
$$ \Omega_c^3 \approx (0.5095)^3 \approx 0.1323 $$
$$ H_a(s) = \frac{0.1323}{s^3 + 1.0191s^2 + 0.5193s + 0.1323} $$

**Step 3: Bilinear Transform**
Since $T_s = 2$, we substitute $s = \frac{z-1}{z+1}$:
$$ H(z) = \frac{0.1323}{\left(\frac{z-1}{z+1}\right)^3 + 1.0191\left(\frac{z-1}{z+1}\right)^2 + 0.5193\left(\frac{z-1}{z+1}\right) + 0.1323} $$

Multiply numerator and denominator by $(z+1)^3$:
$$ H(z) = \frac{0.1323(z+1)^3}{(z-1)^3 + 1.0191(z-1)^2(z+1) + 0.5193(z-1)(z+1)^2 + 0.1323(z+1)^3} $$

Expanding the polynomials:
* $(z-1)^3 = z^3 - 3z^2 + 3z - 1$
* $(z-1)^2(z+1) = (z^2 - 2z + 1)(z+1) = z^3 - z^2 - z + 1$
* $(z-1)(z+1)^2 = (z-1)(z^2 + 2z + 1) = z^3 + z^2 - z - 1$
* $(z+1)^3 = z^3 + 3z^2 + 3z + 1$

Substitute and group by powers of $z$:
Denominator $D(z) = (1 + 1.0191 + 0.5193 + 0.1323)z^3 + (-3 - 1.0191 + 0.5193 + 0.3969)z^2 + (3 - 1.0191 - 0.5193 + 0.3969)z + (-1 + 1.0191 - 0.5193 + 0.1323)$
$D(z) = 2.6707z^3 - 3.1029z^2 + 1.8585z - 0.3679$

Normalizing by $2.6707$ to make the leading coefficient 1:
$$ H(z) = \frac{0.1323 / 2.6707 (z^3 + 3z^2 + 3z + 1)}{z^3 - 1.1618z^2 + 0.6959z - 0.1378} $$
$$ H(z) = \frac{0.0495 (1 + 3z^{-1} + 3z^{-2} + z^{-3})}{1 - 1.1618z^{-1} + 0.6959z^{-2} - 0.1378z^{-3}} $$

This is the final digital filter transfer function.

---

## 10. Summary Table of Key Formulas

| Concept | Formula |
| :--- | :--- |
| **Butterworth Magnitude** | $\|H_a(j\Omega)\|^2 = \frac{1}{1 + (\Omega/\Omega_c)^{2N}}$ |
| **Butterworth Poles** | $s_k = \Omega_c e^{j\frac{\pi}{2N}(2k + N - 1)}$ |
| **Order Formula** | $N \geq \frac{\log_{10}((A_s^2 - 1)/(A_p^2 - 1))}{2 \log_{10}(\Omega_s/\Omega_p)}$ |
| **Impulse Invariance** | $h[n] = T_s h_a(nT_s)$, maps $s_k \to e^{s_k T_s}$ |
| **Bilinear Transform** | $s = \frac{2}{T_s} \frac{z-1}{z+1}$ |
| **Frequency Warping** | $\Omega = \frac{2}{T_s} \tan(\omega/2)$ |

---

## 11. Checkpoints & Quick Review Questions

1. **Q1: Why do we prefer the Bilinear Transform over the Impulse Invariance Method for designing highpass digital filters?**
   * *Answer:* The Impulse Invariance Method suffers from frequency aliasing because the continuous-time spectrum is copied and shifted by multiples of the sampling frequency. Highpass filters have infinite bandwidth in continuous time, so aliasing would severely distort the passband. The Bilinear Transform, however, maps the entire infinite analog frequency axis $[-\infty, \infty]$ exactly onto the finite digital frequency interval $[-\pi, \pi]$, completely eliminating aliasing, making it ideal for highpass and bandstop filters.

2. **Q2: In a Butterworth filter, what happens to the poles as the order $N$ increases?**
   * *Answer:* The $2N$ poles of the squared magnitude transfer function lie on a circle of radius $\Omega_c$ in the $s$-plane. As $N$ increases, the number of poles increases, and they become more densely packed along the circumference of the circle. The angle between adjacent poles decreases (it is $\pi/N$). The leftmost poles move closer to the $j\Omega$ axis, which results in a much sharper transition band (a steeper roll-off) in the frequency response.

3. **Q3: When using the Bilinear Transform, why is it mathematically permissible to simply choose $T_s = 2$ regardless of the actual physical sampling rate?**
   * *Answer:* $T_s$ only acts as an intermediate scaling factor. If you set $T_s = 2$, the prewarping formula becomes $\Omega = \tan(\omega/2)$. The analog cutoff frequency $\Omega_c$ scales accordingly. When you apply the BLT, $s = \frac{z-1}{z+1}$ maps it right back. The parameter $T_s$ cancels itself out perfectly between the prewarping step and the substitution step. The final digital filter coefficients in $H(z)$ remain completely independent of the $T_s$ value chosen.
