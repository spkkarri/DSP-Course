# Lecture 21: Quantization Effects in DSP Systems

**Course:** EE3621 — Digital Signal Processing  
**Target Audience:** III B.Tech EEE Students  
**Duration:** 40 Minutes  

* **Available Formats:** [LaTeX Source File](file:///C:/Users/sriph/Downloads/DSP/lecture_21.tex) | [Compiled PDF Notes](file:///C:/Users/sriph/Downloads/DSP/lecture_21.pdf)

---

## 1. Lecture Plan (40 Minutes Breakdown)
* **00:00 – 05:00 (5 mins):** Why Quantization Matters (ADC limitations, fixed-point vs floating-point).
* **05:00 – 12:00 (7 mins):** Uniform Quantization & Error Model (step size, representation levels, white noise assumption).
* **12:00 – 18:00 (6 mins):** SQNR Derivation ($6.02b + 1.76$ dB).
* **18:00 – 25:00 (7 mins):** Coefficient Quantization (FIR/IIR, sensitivity, direct vs cascade forms).
* **25:00 – 30:00 (5 mins):** Round-off Noise in Fixed-Point IIR (additive noise model, PSD, noise power).
* **30:00 – 35:00 (5 mins):** Limit Cycles & Overflow (granular, overflow, saturation vs two's complement).
* **35:00 – 40:00 (5 mins):** Checkpoints & Full Derivations.

---

## 2. Why Quantization Matters

In any practical Digital Signal Processing (DSP) system, we cannot represent continuous values with infinite precision. We face **finite word-length effects** due to hardware limitations.

### ADC Limitations
An Analog-to-Digital Converter (ADC) must map an infinite set of continuous amplitude values into a finite set of discrete digital levels. This process, known as quantization, inherently discards information.

### Fixed-Point Arithmetic in DSPs
Most cost-effective microcontrollers and DSP chips use fixed-point arithmetic. Unlike floating-point systems, which dynamically adjust the radix point to maintain precision across a huge dynamic range, fixed-point systems assign a strict number of bits to the integer and fractional parts. 
* Whenever two $b$-bit numbers are multiplied, the result requires $2b$ bits.
* To store the result back into a $b$-bit register, the lower bits must be discarded.
* We discard bits via either **truncation** (simply chopping off the lower bits) or **rounding** (choosing the nearest representable value). Rounding is more computationally expensive but yields zero-mean error.

---

## 3. Uniform Quantization

A uniform quantizer divides the input signal range into equal intervals.
Let the input signal range be from $x_{min}$ to $x_{max}$.
For a quantizer with $b$ bits, the number of representation levels is:
$$ L = 2^b $$
The **step size** $\Delta$ (the distance between adjacent quantization levels) is:
$$ \Delta = \frac{x_{max} - x_{min}}{2^b} $$

### Quantization Range
* **Granular Noise Region:** When the signal stays within $[x_{min}, x_{max}]$, the quantization error is bounded by $\Delta$.
* **Overload Region:** When the signal exceeds $x_{max}$ or falls below $x_{min}$, the error grows proportionally to the input (clipping occurs), which is highly non-linear and causes severe distortion.

---

## 4. Quantization Error Model

The quantized signal $x_Q[n]$ can be modeled as the original signal $x[n]$ plus an additive noise term $e[n]$:
$$ x_Q[n] = x[n] + e[n] $$
$$ e[n] = x_Q[n] - x[n] $$

### White Noise Model Assumption
For complex, rapidly varying signals, $e[n]$ is well-approximated by the **Widrow model** (white noise assumption):
1. $e[n]$ is a stationary random process.
2. $e[n]$ is uniformly distributed over the interval $[-\Delta/2, \Delta/2]$ (assuming rounding).
3. $e[n]$ is an uncorrelated white noise sequence (flat power spectral density).
4. $e[n]$ is uncorrelated with the input signal $x[n]$.

### Variance of the Quantization Error
The probability density function (PDF) of $e[n]$ is $p(e) = 1/\Delta$ for $-\Delta/2 \leq e < \Delta/2$, and 0 otherwise.
Since rounding is symmetric, the mean is $\mu_e = 0$.
The variance (noise power) $\sigma_e^2$ is calculated as:
$$ \sigma_e^2 = E[e^2] $$
$$ \sigma_e^2 = \int_{-\Delta/2}^{\Delta/2} e^2 p(e) de $$
$$ \sigma_e^2 = \int_{-\Delta/2}^{\Delta/2} e^2 \frac{1}{\Delta} de $$
$$ \sigma_e^2 = \frac{1}{\Delta} \left[ \frac{e^3}{3} \right]_{-\Delta/2}^{\Delta/2} $$
$$ \sigma_e^2 = \frac{1}{3\Delta} \left( \left(\frac{\Delta}{2}\right)^3 - \left(-\frac{\Delta}{2}\right)^3 \right) $$
$$ \sigma_e^2 = \frac{1}{3\Delta} \left( \frac{\Delta^3}{8} + \frac{\Delta^3}{8} \right) $$
$$ \sigma_e^2 = \frac{1}{3\Delta} \left( \frac{2\Delta^3}{8} \right) $$
$$ \sigma_e^2 = \frac{\Delta^2}{12} $$
**KEY RESULT:** The quantization noise power is proportional to the square of the step size.

---

## 5. Signal-to-Quantization-Noise Ratio (SQNR)

Let the input be a full-scale sinusoidal signal:
$$ x[n] = A \cos(\omega n) $$
The peak-to-peak range is $2A$. If this spans the full quantizer range, then $x_{max} - x_{min} = 2A$.
Thus, the step size is:
$$ \Delta = \frac{2A}{2^b} $$
The signal power $P_x$ for a sine wave of amplitude $A$ is:
$$ P_x = \frac{A^2}{2} $$
The noise power $P_e$ is:
$$ P_e = \sigma_e^2 = \frac{\Delta^2}{12} $$
Substitute $\Delta$:
$$ P_e = \frac{1}{12} \left( \frac{2A}{2^b} \right)^2 $$
$$ P_e = \frac{1}{12} \left( \frac{4A^2}{2^{2b}} \right) $$
$$ P_e = \frac{A^2}{3 \cdot 2^{2b}} $$
Now, compute the SQNR as the ratio of signal power to noise power:
$$ \text{SQNR} = \frac{P_x}{P_e} $$
$$ \text{SQNR} = \frac{A^2 / 2}{A^2 / (3 \cdot 2^{2b})} $$
$$ \text{SQNR} = \frac{3}{2} \cdot 2^{2b} $$
In decibels (dB):
$$ \text{SQNR (dB)} = 10 \log_{10} \left( \frac{3}{2} \cdot 2^{2b} \right) $$
$$ \text{SQNR (dB)} = 10 \log_{10}(1.5) + 10 \log_{10}(2^{2b}) $$
$$ \text{SQNR (dB)} = 1.76 + 20b \log_{10}(2) $$
$$ \text{SQNR (dB)} = 1.76 + 20b (0.301) $$
$$ \text{SQNR (dB)} = 6.02b + 1.76 $$
**KEY RESULT:** Every additional bit of precision increases the SQNR by approximately 6 dB.

---

## 6. Coefficient Quantization in FIR/IIR

When implementing a digital filter, the ideal coefficients $h_k$ (which may require infinite precision) are quantized to fixed-point values $\hat{h}_k$. This perturbs the locations of the poles and zeros of the transfer function $H(z)$.

### Sensitivity Analysis
The change in the frequency response $\Delta H(e^{j\omega})$ due to coefficient errors $\Delta h_k$ is approximated by:
$$ \Delta H(e^{j\omega}) \approx \sum_k \frac{\partial H(e^{j\omega})}{\partial h_k} \Delta h_k $$
If poles move outside the unit circle, an IIR filter becomes unstable. 

### Direct Form vs. Cascade Form
* **High-order Direct Form IIR:** The roots of a high-degree polynomial are extremely sensitive to small changes in its coefficients. A high-order direct form structure is generally avoided in fixed-point implementations.
* **Cascade Form:** We factor $H(z)$ into a product of second-order sections (biquads). The roots of a quadratic equation are far less sensitive to coefficient quantization.
For example, if a 10th-order filter is implemented directly, the roots depend on 11 coefficients interactively. In cascade form, each pair of poles only depends on 3 coefficients, decoupling the sensitivity.

---

## 7. Round-off Noise in Fixed-Point IIR

In fixed-point arithmetic, multiplying a $b$-bit number by a $b$-bit coefficient yields a $2b$-bit product, which must be rounded back to $b$ bits before the next addition.
We model this by inserting an additive white noise source $e[n]$ immediately after every multiplier.
If multiple noise sources exist, we can use superposition (assuming they are uncorrelated) to find the total output noise.

For a specific noise source $e_i[n]$ which passes through a sub-filter with transfer function $H_{noise,i}(z)$ to reach the output, the power spectral density (PSD) of the output noise contribution is:
$$ S_{ee}^{out}(e^{j\omega}) = \frac{\sigma_e^2}{2\pi} |H_{noise,i}(e^{j\omega})|^2 $$
The total output noise power (variance) from this source is found using Parseval's theorem:
$$ \sigma_{out,i}^2 = \frac{\sigma_e^2}{2\pi} \int_{-\pi}^{\pi} |H_{noise,i}(e^{j\omega})|^2 d\omega $$
$$ \sigma_{out,i}^2 = \sigma_e^2 \sum_{n=0}^{\infty} h_{noise,i}^2[n] $$

---

## 8. Limit Cycles

Even when the input $x[n]$ is zero, a fixed-point IIR filter may exhibit sustained oscillations at its output. These are nonlinear phenomena called **limit cycles**.

### Granular Limit Cycles
Arise from quantization (rounding/truncation) inside the recursive feedback loop. Small values bounce back and forth between adjacent quantization levels, unable to settle precisely at zero. 
Condition for absolute absence of limit cycles is when the impulse response satisfies an L1-norm condition, or utilizing structures that strictly reduce signal energy (like coupled-form or wave digital filters).

### Overflow Limit Cycles
Arise from addition overflow. When a sum exceeds the maximum representable value, the behavior depends on the arithmetic:
* **Two's Complement Wraparound:** A large positive number overflows and becomes a large negative number. This severe nonlinearity can cause massive, high-amplitude oscillations.
* **Saturation Arithmetic:** The value is clipped to $x_{max}$ or $x_{min}$. While this distorts the signal, it strictly limits the energy in the loop, generally preventing overflow limit cycles.

To prevent overflow, we apply **scaling**. We typically require that the sum of absolute values of the impulse response (L1-norm) satisfies:
$$ \sum_{n=0}^{\infty} |h[n]| \leq 1 $$
This ensures the output magnitude never exceeds the maximum input magnitude.

---

## 9. Floating-Point vs Fixed-Point

### Dynamic Range and Error
* **Fixed-Point:** Constant absolute error (step size $\Delta$ is fixed). SQNR degrades significantly for small-amplitude signals.
* **Floating-Point (IEEE 754):** The number is represented as a mantissa and an exponent ($x = M \cdot 2^E$). The relative error is bounded, meaning the SQNR remains relatively constant across a vast dynamic range.

### When is Floating-Point Preferred?
Floating-point DSPs (like the TI TMS320C67x) are preferred when:
* Algorithm development time must be minimized (no manual scaling required).
* The application involves matrix inversions (e.g., Kalman filtering, MIMO communication) where dynamic range fluctuates wildly.
* Power and cost constraints are relaxed.

---

## 10. Key Formulas Summary

| Concept | Formula |
| :--- | :--- |
| Step Size | $\Delta = \frac{x_{max} - x_{min}}{2^b}$ |
| Quantization Noise Variance | $\sigma_e^2 = \frac{\Delta^2}{12}$ |
| SQNR for Full-Scale Sine | $\text{SQNR (dB)} = 6.02b + 1.76$ |
| Output Noise Power | $\sigma_{out}^2 = \sigma_e^2 \sum_{n} h^2[n]$ |

---

## 11. Checkpoint Questions

**Q1: A continuous-time sine wave $x(t) = 5 \cos(2\pi \cdot 1000 t)$ is sampled and uniformly quantized using an 8-bit ADC. The ADC range is $-5$ V to $+5$ V. Calculate the step size $\Delta$ and the quantization noise power.**
* **Answer:**
  * The full range is $x_{max} - x_{min} = 5 - (-5) = 10$ V.
  * Number of bits $b = 8$.
  * Step size:
    $$ \Delta = \frac{10}{2^8} $$
    $$ \Delta = \frac{10}{256} $$
    $$ \Delta \approx 0.0390625 \text{ V} $$
  * Quantization noise power $\sigma_e^2$:
    $$ \sigma_e^2 = \frac{\Delta^2}{12} $$
    $$ \sigma_e^2 = \frac{(0.0390625)^2}{12} $$
    $$ \sigma_e^2 = \frac{0.0015258789}{12} $$
    $$ \sigma_e^2 \approx 1.27 \times 10^{-4} \text{ W} $$

**Q2: Derive the maximum amplitude $A$ of a sinusoidal input that can be applied to a 12-bit ADC (range $\pm 2.5$ V) to achieve an SQNR of exactly 70 dB, assuming quantization noise power remains constant at the full-scale level.**
* **Answer:**
  * For full scale, $\Delta = 5 / 2^{12} = 5 / 4096 = 0.00122$ V.
  * Noise power $P_e = \Delta^2 / 12 = (0.00122)^2 / 12 \approx 1.24 \times 10^{-7}$ W.
  * We require $10 \log_{10}(P_x / P_e) = 70$.
  * Therefore, $P_x / P_e = 10^7$.
  * Signal power $P_x = 10^7 \times P_e = 10^7 \times 1.24 \times 10^{-7} = 1.24$ W.
  * For a sine wave, $P_x = A^2 / 2$.
  * $A^2 = 2 \times P_x = 2.48$.
  * $A = \sqrt{2.48} \approx 1.57$ V.
  * (Note: Since $1.57 \text{ V} \leq 2.5 \text{ V}$, clipping does not occur).

**Q3: A first-order IIR filter has the difference equation $y[n] = x[n] + 0.8 y[n-1]$. The multiplications are performed using fixed-point arithmetic with rounding, introducing a noise source $e[n]$ with variance $\sigma_e^2$. What is the total output noise power?**
* **Answer:**
  * The noise source $e[n]$ is injected after the multiplication by 0.8, meaning it passes through the same recursive loop as the signal.
  * The noise transfer function is $H_{noise}(z) = \frac{1}{1 - 0.8z^{-1}}$.
  * The corresponding impulse response is $h_{noise}[n] = (0.8)^n u[n]$.
  * The output noise power is $\sigma_{out}^2 = \sigma_e^2 \sum_{n=0}^{\infty} h_{noise}^2[n]$.
  * Substituting $h_{noise}[n]$:
    $$ \sigma_{out}^2 = \sigma_e^2 \sum_{n=0}^{\infty} ((0.8)^n)^2 $$
    $$ \sigma_{out}^2 = \sigma_e^2 \sum_{n=0}^{\infty} (0.64)^n $$
  * Using the infinite geometric series sum formula $S = \frac{1}{1 - r}$ for $|r| < 1$:
    $$ \sigma_{out}^2 = \sigma_e^2 \left( \frac{1}{1 - 0.64} \right) $$
    $$ \sigma_{out}^2 = \sigma_e^2 \left( \frac{1}{0.36} \right) $$
    $$ \sigma_{out}^2 \approx 2.78 \sigma_e^2 $$
  * The recursive structure amplifies the injection noise by a factor of roughly 2.78.

*(End of Notes)*
