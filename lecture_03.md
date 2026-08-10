# Lecture 3: The Discrete-Time Fourier Transform (DTFT)

**Course:** EE3621 — Digital Signal Processing  
**Target Audience:** III B.Tech EEE Students  
**Duration:** 40 Minutes  

* **Available Formats:** [LaTeX Source File](file:///C:/Users/sriph/Downloads/DSP/lecture_03.tex) | [Compiled PDF Notes](file:///C:/Users/sriph/Downloads/DSP/lecture_03.pdf)

---

## 1. Lecture Plan (40 Minutes Breakdown)
* **00:00 – 05:00 (5 mins):** Motivation: Time-domain limitations, continuous spectrum for discrete signals, and periodicity.
* **05:00 – 12:00 (7 mins):** DTFT & IDTFT Mathematical Definitions, Convergence Criteria (Absolute vs. Mean-Square).
* **12:00 – 22:00 (10 mins):** DTFT of Common Signals: Rectangular Pulse (Dirichlet Kernel), Single/Double Decaying Exponentials, Impulse, and DC.
* **22:00 – 35:00 (13 mins):** Key Properties of the DTFT (Linearity, Shifting, Modulation, Symmetry, Differentiation, Convolution, Parseval) with complete proofs.
* **35:00 – 40:00 (5 mins):** Time-Frequency Duality, the Uncertainty Principle, and Checkpoints.

---

## 2. Mathematical Definition of the DTFT

The **Discrete-Time Fourier Transform (DTFT)** maps a discrete-time sequence $x[n]$ to a continuous, periodic complex frequency function $X(e^{j\omega})$, where $\omega$ is the digital frequency in radians per sample.

### Analysis Equation (Forward DTFT)
$$X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n}$$

* **Periodicity Proof:** The DTFT is always periodic in $\omega$ with a period of $2\pi$:
  $$X(e^{j(\omega + 2\pi)}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j(\omega + 2\pi)n} = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n} e^{-j 2\pi n}$$
  Since $e^{-j 2\pi n} = \cos(2\pi n) - j\sin(2\pi n) = 1$ for any integer $n$, the expression simplifies to:
  $$X(e^{j(\omega + 2\pi)}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n} = X(e^{j\omega})$$
  Because of this periodicity, we only need to analyze $X(e^{j\omega})$ over a single interval of length $2\pi$, typically $[-\pi, \pi]$ or $[0, 2\pi]$.

### Synthesis Equation (Inverse DTFT / IDTFT)
Given the frequency spectrum $X(e^{j\omega})$, we can reconstruct the original discrete sequence $x[n]$ using:
$$x[n] = \frac{1}{2\pi} \int_{-\pi}^{\pi} X(e^{j\omega}) e^{j\omega n} d\omega$$

### Convergence Conditions
The infinite summation in the forward DTFT does not always converge.
1. **Absolute Summability (Sufficient for Uniform Convergence):**
   A sequence $x[n]$ has a uniformly convergent DTFT if it is absolutely summable:
   $$\sum_{n=-\infty}^{\infty} |x[n]| < \infty$$
   * **Proof:**
     $$|X(e^{j\omega})| = \left| \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n} \right| \le \sum_{n=-\infty}^{\infty} |x[n] e^{-j\omega n}| = \sum_{n=-\infty}^{\infty} |x[n]| < \infty$$
     If this condition is met, $X(e^{j\omega})$ is a continuous function of $\omega$.
2. **Square Summability (Mean-Square Convergence):**
   If a sequence has finite energy but is not absolutely summable (e.g., $x[n] = \frac{\sin(\omega_c n)}{\pi n}$):
   $$\sum_{n=-\infty}^{\infty} |x[n]|^2 < \infty$$
   In this case, the DTFT converges in the mean-square error sense, though it may contain discontinuities (such as Gibbs phenomenon ripples at band edges).

---

## 3. DTFT of Common Signals

### A. Finite Rectangular Pulse
Let $x[n] = 1$ for $0 \le n \le M-1$, and $0$ otherwise.
$$X(e^{j\omega}) = \sum_{n=0}^{M-1} e^{-j\omega n} = \frac{1 - e^{-j\omega M}}{1 - e^{-j\omega}}$$
Factoring out the half-angle terms:
$$X(e^{j\omega}) = \frac{e^{-j\omega M/2} \left( e^{j\omega M/2} - e^{-j\omega M/2} \right)}{e^{-j\omega/2} \left( e^{j\omega/2} - e^{-j\omega/2} \right)} = e^{-j\omega(M-1)/2} \frac{\sin\left(\frac{\omega M}{2}\right)}{\sin\left(\frac{\omega}{2}\right)}$$
* This is the **Dirichlet kernel** (often called the periodic sinc function). 
* The magnitude $\left|\frac{\sin(\omega M/2)}{\sin(\omega/2)}\right|$ represents the amplitude spectrum, and the linear phase term $e^{-j\omega(M-1)/2}$ represents the time delay of $(M-1)/2$ samples.

### B. Single-Sided Decaying Exponential
Let $x[n] = a^n u[n]$ with $|a| < 1$.
$$X(e^{j\omega}) = \sum_{n=0}^{\infty} \left( a e^{-j\omega} \right)^n = \frac{1}{1 - a e^{-j\omega}}$$
* **Magnitude:**
  $$|X(e^{j\omega})| = \frac{1}{\sqrt{(1 - a\cos\omega)^2 + (a\sin\omega)^2}} = \frac{1}{\sqrt{1 + a^2 - 2a\cos\omega}}$$
* **Phase:**
  $$\angle X(e^{j\omega}) = -\arctan\left( \frac{a\sin\omega}{1 - a\cos\omega} \right)$$

### C. Double-Sided Decaying Exponential
Let $x[n] = a^{|n|}$ with $|a| < 1$.
$$X(e^{j\omega}) = \sum_{n=-\infty}^{-1} a^{-n} e^{-j\omega n} + \sum_{n=0}^{\infty} a^n e^{-j\omega n} = \sum_{m=1}^{\infty} (a e^{j\omega})^m + \sum_{n=0}^{\infty} (a e^{-j\omega})^n$$
$$X(e^{j\omega}) = \frac{a e^{j\omega}}{1 - a e^{j\omega}} + \frac{1}{1 - a e^{-j\omega}} = \frac{1 - a^2}{1 + a^2 - 2a\cos\omega}$$
This result is purely real because the input sequence is even-symmetric ($x[n] = x[-n]$).

### D. Unit Impulse
Let $x[n] = \delta[n]$.
$$X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} \delta[n] e^{-j\omega n} = e^{-j\omega (0)} = 1$$
An impulse in the time domain contains all frequencies at equal amplitude.

### E. Constant DC Signal
Let $x[n] = 1$ for all $n$. This signal is not absolutely summable, but its DTFT can be defined using Dirac delta functions:
$$X(e^{j\omega}) = 2\pi \sum_{k=-\infty}^{\infty} \delta(\omega - 2\pi k)$$
Within the fundamental interval $[-\pi, \pi]$, this represents a single impulse at $\omega = 0$.

---

## 4. Key Properties of the DTFT (with Proofs)

Let $x[n] \leftrightarrow X(e^{j\omega})$ and $y[n] \leftrightarrow Y(e^{j\omega})$.

### A. Linearity
$$a \cdot x[n] + b \cdot y[n] \longleftrightarrow a \cdot X(e^{j\omega}) + b \cdot Y(e^{j\omega})$$

### B. Time Shifting
$$x[n - n_0] \longleftrightarrow X(e^{j\omega}) e^{-j\omega n_0}$$
* **Proof:**
  $$\text{DTFT}\{x[n-n_0]\} = \sum_{n=-\infty}^{\infty} x[n-n_0] e^{-j\omega n}$$
  Let $m = n - n_0 \Rightarrow n = m + n_0$:
  $$\sum_{m=-\infty}^{\infty} x[m] e^{-j\omega (m+n_0)} = e^{-j\omega n_0} \sum_{m=-\infty}^{\infty} x[m] e^{-j\omega m} = X(e^{j\omega}) e^{-j\omega n_0}$$

### C. Frequency Shifting (Modulation)
$$x[n] e^{j\omega_0 n} \longleftrightarrow X(e^{j(\omega - \omega_0)})$$
* **Proof:**
  $$\text{DTFT}\{x[n] e^{j\omega_0 n}\} = \sum_{n=-\infty}^{\infty} x[n] e^{j\omega_0 n} e^{-j\omega n} = \sum_{n=-\infty}^{\infty} x[n] e^{-j(\omega - \omega_0)n} = X(e^{j(\omega - \omega_0)})$$

### D. Differentiation in Frequency
$$n \cdot x[n] \longleftrightarrow j \frac{d X(e^{j\omega})}{d\omega}$$
* **Proof:** Differentiate the analysis equation with respect to $\omega$:
  $$\frac{d X(e^{j\omega})}{d\omega} = \frac{d}{d\omega} \left[ \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n} \right] = \sum_{n=-\infty}^{\infty} x[n] (-jn) e^{-j\omega n} = -j \sum_{n=-\infty}^{\infty} (n \cdot x[n]) e^{-j\omega n}$$
  Multiply both sides by $j$ (since $j \cdot -j = 1$):
  $$j \frac{d X(e^{j\omega})}{d\omega} = \sum_{n=-\infty}^{\infty} (n \cdot x[n]) e^{-j\omega n} = \text{DTFT}\{n \cdot x[n]\}$$

### E. Convolution Theorem (Time Convolution)
$$x[n] * y[n] \longleftrightarrow X(e^{j\omega}) \cdot Y(e^{j\omega})$$
* **Proof:**
  $$\text{DTFT}\{x[n] * y[n]\} = \sum_{n=-\infty}^{\infty} \left[ \sum_{k=-\infty}^{\infty} x[k] y[n-k] \right] e^{-j\omega n}$$
  Interchange the order of summation:
  $$\sum_{k=-\infty}^{\infty} x[k] \left[ \sum_{n=-\infty}^{\infty} y[n-k] e^{-j\omega n} \right]$$
  Apply the time-shifting property to the inner sum:
  $$\sum_{k=-\infty}^{\infty} x[k] \left[ Y(e^{j\omega}) e^{-j\omega k} \right] = Y(e^{j\omega}) \sum_{k=-\infty}^{\infty} x[k] e^{-j\omega k} = Y(e^{j\omega}) X(e^{j\omega})$$

### F. Parseval's Theorem (Energy Conservation)
$$\sum_{n=-\infty}^{\infty} |x[n]|^2 = \frac{1}{2\pi} \int_{-\pi}^{\pi} |X(e^{j\omega})|^2 d\omega$$
* **Proof:**
  $$\sum_{n=-\infty}^{\infty} x[n] x^*[n] = \sum_{n=-\infty}^{\infty} x[n] \left[ \frac{1}{2\pi} \int_{-\pi}^{\pi} X^*(e^{j\omega}) e^{-j\omega n} d\omega \right]$$
  Interchange the summation and integration:
  $$\frac{1}{2\pi} \int_{-\pi}^{\pi} X^*(e^{j\omega}) \left[ \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n} \right] d\omega = \frac{1}{2\pi} \int_{-\pi}^{\pi} X^*(e^{j\omega}) X(e^{j\omega}) d\omega = \frac{1}{2\pi} \int_{-\pi}^{\pi} |X(e^{j\omega})|^2 d\omega$$

---

## 5. Time-Frequency Duality & The Uncertainty Principle

* **Duality:** A narrow signal in the time domain (e.g., an impulse) results in a wide response in the frequency domain (constant flat spectrum). Conversely, a wide signal in the time domain (e.g., a constant DC line) results in a narrow response in the frequency domain (a single impulse at $\omega = 0$).
* **Heisenberg Uncertainty Principle:** You cannot simultaneously localize a signal in both time and frequency. The product of the time-duration variance $\Delta_t^2$ and the frequency-bandwidth variance $\Delta_\omega^2$ is bounded from below:
  $$\Delta_t \cdot \Delta_\omega \ge \frac{1}{2}$$

---

## 6. Detailed Worked Examples

### Example 1: DTFT of a Shifted Impulse
**Problem:** Find the DTFT of $x[n] = \delta[n] - \delta[n-1]$ and compute its magnitude and phase.

**Solution:**
1. Apply the definition:
   $$X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} (\delta[n] - \delta[n-1]) e^{-j\omega n} = e^{-j\omega(0)} - e^{-j\omega(1)} = 1 - e^{-j\omega}$$
2. Simplify using half-angle factoring:
   $$X(e^{j\omega}) = e^{-j\omega/2} \left( e^{j\omega/2} - e^{-j\omega/2} \right) = e^{-j\omega/2} \left( 2j \sin(\omega/2) \right)$$
   Since $j = e^{j\pi/2}$:
   $$X(e^{j\omega}) = 2 \sin(\omega/2) e^{j(\pi/2 - \omega/2)}$$
3. **Magnitude:**
   $$|X(e^{j\omega})| = 2 \left| \sin(\omega/2) \right|$$
4. **Phase:**
   $$\angle X(e^{j\omega}) = \frac{\pi - \omega}{2} \quad (\text{for } \sin(\omega/2) > 0)$$

---

### Example 2: DTFT of a Sum of Exponentials
**Problem:** Find the DTFT of $x[n] = \left[(0.5)^n + (0.3)^n\right] u[n]$.

**Solution:**
Using the linearity property, the DTFT is the sum of the individual transforms:
$$X(e^{j\omega}) = \text{DTFT}\left\{(0.5)^n u[n]\right\} + \text{DTFT}\left\{(0.3)^n u[n]\right\}$$
Using the decaying exponential pair:
$$X(e^{j\omega}) = \frac{1}{1 - 0.5 e^{-j\omega}} + \frac{1}{1 - 0.3 e^{-j\omega}}$$
Combine over a common denominator:
$$X(e^{j\omega}) = \frac{(1 - 0.3 e^{-j\omega}) + (1 - 0.5 e^{-j\omega})}{(1 - 0.5 e^{-j\omega})(1 - 0.3 e^{-j\omega})} = \frac{2 - 0.8 e^{-j\omega}}{1 - 0.8 e^{-j\omega} + 0.15 e^{-2j\omega}}$$

---

### Example 3: DTFT of a Modulated Causal Exponential
**Problem:** Find the DTFT of $x[n] = a^n \cos(\omega_0 n) u[n]$ for $|a| < 1$.

**Solution:**
1. Using Euler's formula, write the cosine as complex exponentials:
   $$x[n] = a^n \left( \frac{e^{j\omega_0 n} + e^{-j\omega_0 n}}{2} \right) u[n] = \frac{1}{2} \left( a e^{j\omega_0} \right)^n u[n] + \frac{1}{2} \left( a e^{-j\omega_0} \right)^n u[n]$$
2. Apply the decaying exponential transform formula to each term:
   $$X(e^{j\omega}) = \frac{1}{2} \left[ \frac{1}{1 - a e^{j\omega_0}e^{-j\omega}} + \frac{1}{1 - a e^{-j\omega_0}e^{-j\omega}} \right] = \frac{1}{2} \left[ \frac{1}{1 - a e^{-j(\omega - \omega_0)}} + \frac{1}{1 - a e^{-j(\omega + \omega_0)}} \right]$$
3. Combine the fractions:
   $$X(e^{j\omega}) = \frac{1 - a\cos\omega_0 e^{-j\omega}}{1 - 2a\cos\omega_0 e^{-j\omega} + a^2 e^{-2j\omega}}$$

---

### Example 4: Energy Calculation using Parseval's Theorem
**Problem:** Given $x[n] = a^n u[n]$ for $|a| < 1$, find the total energy of the signal in both the time and frequency domains.

**Solution:**
1. **Time Domain:**
   $$E = \sum_{n=-\infty}^{\infty} |x[n]|^2 = \sum_{n=0}^{\infty} (a^2)^n = \frac{1}{1 - a^2}$$
2. **Frequency Domain (Parseval's):**
   $$E = \frac{1}{2\pi} \int_{-\pi}^{\pi} |X(e^{j\omega})|^2 d\omega = \frac{1}{2\pi} \int_{-\pi}^{\pi} \frac{1}{1 + a^2 - 2a\cos\omega} d\omega$$
   Using the standard integration formula $\int \frac{1}{A - B\cos\omega} d\omega = \frac{2\pi}{\sqrt{A^2 - B^2}}$:
   Here, $A = 1 + a^2$ and $B = 2a$.
   $$\sqrt{A^2 - B^2} = \sqrt{(1+a^2)^2 - (2a)^2} = \sqrt{1 + 2a^2 + a^4 - 4a^2} = \sqrt{1 - 2a^2 + a^4} = \sqrt{(1-a^2)^2} = 1 - a^2$$
   Thus:
   $$E = \frac{1}{2\pi} \cdot \frac{2\pi}{1 - a^2} = \frac{1}{1 - a^2}$$
   Both domains yield the exact same energy.

---

### Example 5: Finding Inverse DTFT
**Problem:** Find the inverse DTFT $x[n]$ of $X(e^{j\omega}) = e^{-j\omega n_0}$ for $\omega \in [-\pi, \pi]$.

**Solution:**
Apply the synthesis equation:
$$x[n] = \frac{1}{2\pi} \int_{-\pi}^{\pi} X(e^{j\omega}) e^{j\omega n} d\omega = \frac{1}{2\pi} \int_{-\pi}^{\pi} e^{-j\omega n_0} e^{j\omega n} d\omega = \frac{1}{2\pi} \int_{-\pi}^{\pi} e^{j\omega (n - n_0)} d\omega$$
* **If $n = n_0$:**
  $$x[n_0] = \frac{1}{2\pi} \int_{-\pi}^{\pi} 1 \cdot d\omega = \frac{2\pi}{2\pi} = 1$$
* **If $n \neq n_0$:**
  $$x[n] = \frac{1}{2\pi} \left[ \frac{e^{j\omega(n-n_0)}}{j(n-n_0)} \right]_{-\pi}^{\pi} = \frac{\sin(\pi(n-n_0))}{\pi(n-n_0)} = 0$$
  *(Since $\sin(\pi k) = 0$ for any non-zero integer $k$).*

Thus, $x[n] = \delta[n - n_0]$.

---

### Example 6: DTFT of $x[n] = n a^n u[n]$ using Differentiation
**Problem:** Compute the DTFT of $x[n] = n a^n u[n]$ for $|a| < 1$.

**Solution:**
1. Let $v[n] = a^n u[n] \longleftrightarrow V(e^{j\omega}) = \frac{1}{1 - a e^{-j\omega}}$.
2. Using the differentiation property, $x[n] = n v[n] \longleftrightarrow X(e^{j\omega}) = j \frac{d V(e^{j\omega})}{d\omega}$.
3. Calculate the derivative:
   $$\frac{d}{d\omega} \left[ (1 - a e^{-j\omega})^{-1} \right] = -(1 - a e^{-j\omega})^{-2} \cdot \left( -a \cdot (-j) e^{-j\omega} \right) = \frac{-j a e^{-j\omega}}{(1 - a e^{-j\omega})^2}$$
4. Multiply by $j$:
   $$X(e^{j\omega}) = j \cdot \left( \frac{-j a e^{-j\omega}}{(1 - a e^{-j\omega})^2} \right) = \frac{a e^{-j\omega}}{(1 - a e^{-j\omega})^2}$$

---

## 8. Interactive Lecture Checkpoints

* **Checkpoint 1: Why is the DTFT always periodic with period $2\pi$, whereas the continuous Fourier transform is not periodic?**
  * **Answer:** The time-domain index $n$ is restricted to integers. When we calculate the exponential term $e^{-j(\omega + 2\pi)n} = e^{-j\omega n} e^{-j2\pi n}$, the term $e^{-j2\pi n}$ is always equal to $1$ because $n$ is an integer. For continuous signals, $t$ can be any real number, so $e^{-j2\pi t} \neq 1$, preventing periodicity.

* **Checkpoint 2: What is the physical meaning of the DTFT phase spectrum?**
  * **Answer:** The phase spectrum $\angle X(e^{j\omega})$ describes the relative time alignment (delay) of the different frequency components in the signal. A linear phase shift $\angle X(e^{j\omega}) = -\omega n_0$ represents a uniform time delay of $n_0$ samples for all frequencies, preserving the shape of the signal envelope.

* **Checkpoint 3: Explain why a DC signal $x[n]=1$ requires Dirac delta functions in its DTFT.**
  * **Answer:** A constant DC signal contains only one frequency ($\omega = 0$) and exists from $-\infty$ to $\infty$. It is not absolutely summable, meaning its standard summation diverges. To represent its infinite spectral density at exactly $\omega = 0$ while maintaining consistency with the inverse transform, we use the Dirac delta function $2\pi \delta(\omega)$.

* **Checkpoint 4: How does the window length $M$ of a rectangular pulse affect its DTFT mainlobe width and sidelobe height?**
  * **Answer:** The DTFT of an $M$-length rectangular pulse is the Dirichlet kernel. The width of the mainlobe is $4\pi/M$, which decreases as $M$ increases (narrower spectrum, higher resolution). However, the peak sidelobe level relative to the mainlobe peak remains approximately $-13$ dB regardless of $M$.
