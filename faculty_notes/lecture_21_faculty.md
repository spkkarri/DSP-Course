</Agent System Instructions>
<Faculty Notes — Lecture 21: Quantization Effects & Finite Word-Length>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY
When teaching quantization and finite word-length effects to III B.Tech EEE students, emphasize that these are the most practical concepts for implementing DSP algorithms on actual hardware. Many students are accustomed to MATLAB/Python simulations using double-precision floating-point arithmetic and mistakenly believe that a stable theoretical filter design will automatically perform flawlessly in hardware. The shift to fixed-point reality often surprises them.

**Common student difficulties:**
1. Understanding the statistical model of quantization noise (why it is modeled as white noise when it is actually deterministic).
2. Differentiating between coefficient quantization (affects pole/zero locations) and signal round-off (adds noise to the signal).
3. Grasping the physical mechanism of limit cycles (how a linear filter exhibits non-linear oscillations).

**Suggested Demos:**
* Use MATLAB to simulate a high-Q bandpass filter (poles very close to the unit circle). Process a clean sine wave. Then, quantize the filter coefficients to 8 bits and show how the frequency response drastically shifts, perhaps even becoming unstable.
* Show an audio signal quantized to 16 bits (CD quality), 8 bits, and 4 bits. Play the audio so students can hear the harsh granular noise introduced by heavy quantization.

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Analyze** fixed-point number formats including two's complement and Q(a.b) fractional formats, evaluating their dynamic range and resolution limits.
2. **Formulate** the mathematical model for A/D quantization error and justify the statistical assumptions of uniformly distributed, white, uncorrelated noise.
3. **Derive** the 6.02 dB per bit rule for Signal-to-Quantization-Noise Ratio (SQNR) from first principles.
4. **Evaluate** the impact of coefficient quantization on filter stability by analyzing pole migration in Direct Form vs. Cascade structures.
5. **Calculate** the total output roundoff noise variance in a recursive digital filter due to finite-precision multiplications.
6. **Diagnose** granular and overflow limit cycles in IIR filters and specify scaling and saturation arithmetic strategies to suppress them.

---
## 2. PREREQUISITE KNOWLEDGE REVIEW
Students must be comfortable with the following before engaging with this topic:

* **Z-Transform and System Functions:**
  Knowledge of poles and zeros, and their relationship to filter stability (poles must lie strictly within the unit circle $|z| < 1$).
  Formula:
  $$ H(z) = \sum_{n=-\infty}^{\infty} h[n] z^{-n} $$
  
* **Random Signals and Statistics:**
  Familiarity with expected value $E[X]$, variance $\sigma_X^2$, uniform probability density functions (PDF), and wide-sense stationary (WSS) white noise.
  Formula for uniform PDF between $a$ and $b$:
  $$ f_X(x) = \frac{1}{b - a} \quad \text{for } a \leq x \leq b $$
  Formula for variance:
  $$ \sigma_X^2 = E[(X - E[X])^2] = E[X^2] - (E[X])^2 $$
  
* **Parseval's Theorem:**
  Relating time-domain energy to frequency-domain energy.
  Formula:
  $$ \sum_{n=-\infty}^{\infty} |x[n]|^2 = \frac{1}{2\pi} \int_{-\pi}^{\pi} |X(e^{j\omega})|^2 d\omega $$

---
## 3. HISTORICAL AND MOTIVATIONAL CONTEXT
The study of finite word-length effects became crucial in the 1960s and 70s as digital computers began replacing analog circuits for filtering and control. Early DSP pioneers like Alan Oppenheim and Lawrence Rabiner discovered that implementing mathematical algorithms on hardware with limited precision (e.g., 8-bit or 16-bit processors) caused bizarre, non-linear behaviors—filters would ring indefinitely with no input, or suddenly blast full-scale noise due to overflow. 

**Why does an EEE student need this?**
Electrical engineers design systems subject to strict power and cost constraints. An embedded system in a pacemaker or a low-cost IoT sensor cannot afford the silicon area or power consumption of a 64-bit floating-point unit (FPU). They must use fixed-point microcontrollers or FPGAs. If the engineer does not account for quantization noise or limit cycles, the control loop might destabilize, or the audio signal might be corrupted by unacceptable noise levels.

---
## 4. THEORETICAL FOUNDATIONS

### 4.1 Fixed-Point Number Systems
In digital hardware, continuous real values must be mapped to a finite set of discrete binary words. The most common format is fixed-point arithmetic, typically utilizing **two's complement** representation.

**Two's Complement Fractional Format (Q Format):**
A fractional number can be represented in Q(a.b) format, where $a$ is the number of integer bits (including the sign bit) and $b$ is the number of fractional bits. The total word length is $B = a + b$.

For a pure fractional two's complement number (Q1.15 format for a 16-bit word), the value is given by:
$$ X = -b_0 + \sum_{i=1}^{B-1} b_i 2^{-i} $$
where $b_0$ is the sign bit.

* **Range:** The maximum representable positive value is $1 - 2^{-(B-1)}$ and the minimum negative value is $-1$. Notice the slight asymmetry in two's complement (there is one more negative number than positive numbers).
* **Resolution (Step Size $\Delta$):** The distance between adjacent representable numbers is strictly $\Delta = 2^{-(B-1)}$. Any value that falls between these discrete steps must be mapped to the nearest step.
* **Overflow Behavior:** If an addition exceeds the maximum value, standard two's complement arithmetic wraps around (e.g., a large positive number suddenly becomes a large negative number). This introduces catastrophic, discontinuous error. In audio, this sounds like a harsh, sudden pop or screech.
* **Saturation Arithmetic:** To prevent wraparound, modern DSP processors use built-in saturation logic (often at the hardware MAC level). If a sum exceeds the maximum limit, it is clamped to the maximum positive value. If it falls below the minimum limit, it is clamped to the minimum negative value. This mimics analog overdrive (soft clipping) rather than digital wrapping.

**Physical Interpretation:**
Wraparound is like a car odometer resetting to zero after 999,999. It causes a massive mathematical discontinuity. Saturation is like a speedometer needle hitting a physical peg at 120 mph and staying there regardless of further acceleration. It distorts the signal, but bounds the error energy.

### 4.2 Quantization Model
When an analog signal $x(t)$ is sampled to $x[n]$ and then quantized to a discrete binary word $x_q[n]$, an error is inevitably introduced.

We define the quantization error (or quantization noise) $e[n]$ as the difference between the quantized signal and the true signal:
$$ e[n] = x_q[n] - x[n] $$
Thus, we can construct a powerful mathematical model: we replace the highly non-linear quantizer block with a simple linear summing junction, adding a fictitious noise source:
$$ x_q[n] = x[n] + e[n] $$

**Uniform Quantizer Types:**
A uniform quantizer has a constant step size $\Delta$ across its entire operating range.
* **Midtread:** Zero is a valid, explicit quantization level. This is crucial for DSP because it ensures that a zero-volt input yields an exactly zero digital output (silence produces silence).
* **Midriser:** Zero falls exactly halfway between two quantization levels ($\pm \Delta/2$). This is rarely used in DSP because a zero input would result in the ADC output rapidly oscillating between the positive and negative levels, creating a constant hum during silent periods.
* **Rounding:** The signal is mapped (rounded) to the nearest available level. The error range is perfectly symmetric: $-\frac{\Delta}{2} \leq e[n] < \frac{\Delta}{2}$.
* **Truncation (Floor):** The fractional bits are simply discarded (chopped off). For two's complement numbers, the error is always strictly non-positive: $-\Delta < e[n] \leq 0$. This shifts the mean of the signal downwards (DC offset).

### 4.3 Quantization Noise Model Assumptions
Quantization is fundamentally a deterministic, non-linear process. If $x[n]$ is exactly known, $e[n]$ is exactly known. There is no actual randomness. However, treating it mathematically as a deterministic non-linear process in a feedback loop is impossibly complex. 

To simplify analysis, we make the **Widrow statistical assumptions**, which treat the error as if it were a random noise source:
1. The error sequence $e[n]$ is a sample sequence of a stationary random process.
2. The error $e[n]$ is uncorrelated with the input signal $x[n]$ (i.e., the noise does not depend on the signal amplitude).
3. The random variables of the error process are mutually uncorrelated (i.e., the error is a wide-sense stationary white noise sequence with a flat power spectral density).
4. The probability distribution of the error process is completely uniform over the full range of the quantization error bounds.

For a rounding quantizer, the Probability Density Function (PDF) $f_E(e)$ is mathematically defined as:
$$ f_E(e) = \begin{cases} \frac{1}{\Delta} & \text{for } -\frac{\Delta}{2} \leq e < \frac{\Delta}{2} \\ 0 & \text{otherwise} \end{cases} $$

**When are these assumptions valid?**
These assumptions hold exceptionally well when the signal is highly complex, fluctuates rapidly, and traverses multiple quantization levels between samples (like a dense music track or a broadband sensor reading).
They fail miserably for DC signals, very low-frequency sinusoids, or signals whose amplitude is barely larger than a single $\Delta$ (where the error becomes highly correlated with the signal, forming harmonic distortion).

**Physical Interpretation:**
Imagine taking a very high-resolution photograph of a forest and then severely reducing the color palette to 16 colors. The resulting visual error looks like random granular static (noise) overlaid on the image, rather than a predictable, smooth pattern. This "randomness" allows us to use statistical noise models.

### 4.4 Signal-to-Quantization-Noise Ratio (SQNR)
We want to evaluate the quality of a quantized signal. 
The quantization noise variance (power) $\sigma_e^2$ for rounding is the second moment of the uniform PDF (since the mean is zero):
$$ \sigma_e^2 = \int_{-\Delta/2}^{\Delta/2} e^2 f_E(e) de $$
$$ \sigma_e^2 = \frac{1}{\Delta} \left[ \frac{e^3}{3} \right]_{-\Delta/2}^{\Delta/2} $$
$$ \sigma_e^2 = \frac{1}{\Delta} \left( \frac{\Delta^3}{24} - \frac{-\Delta^3}{24} \right) = \frac{\Delta^2}{12} $$

Now, consider a full-scale sinusoidal input spanning the entire range of an $N$-bit quantizer.
Range $R = 2A = 2^N \Delta \implies A = 2^{N-1} \Delta$.
The signal power for a sinusoid of amplitude $A$ is:
$$ \sigma_x^2 = \frac{A^2}{2} = \frac{(2^{N-1} \Delta)^2}{2} = \frac{2^{2N-2} \Delta^2}{2} = 2^{2N-3} \Delta^2 $$

The SQNR is the ratio of signal power to noise power:
$$ \text{SQNR} = \frac{\sigma_x^2}{\sigma_e^2} = \frac{2^{2N-3} \Delta^2}{\Delta^2 / 12} = 12 \cdot 2^{2N-3} = 1.5 \cdot 2^{2N} $$

Converting to decibels (dB):
$$ \text{SQNR}_{dB} = 10 \log_{10}(1.5 \cdot 2^{2N}) $$
$$ \text{SQNR}_{dB} = 10 \log_{10}(1.5) + 10 \log_{10}(2^{2N}) $$
$$ \text{SQNR}_{dB} = 1.76 + 20N \log_{10}(2) \approx 1.76 + 6.02N $$

**Physical Interpretation:**
Every additional bit of resolution added to an Analog-to-Digital Converter (ADC) provides an extra 6 dB of signal-to-noise ratio. A 16-bit audio CD has a theoretical dynamic range of $6.02(16) + 1.76 \approx 98$ dB, which is sufficient for human hearing.

### 4.5 Coefficient Quantization Effects
When designing a filter, poles and zeros are calculated with high precision. When implemented, these coefficients $a_k$ and $b_k$ are quantized.
$$ \hat{a}_k = a_k + \Delta a_k $$
Because the poles of the filter are the roots of the denominator polynomial, changing the polynomial coefficients perturbs the roots.

**Direct Form I / II:**
The denominator is $1 - \sum_{k=1}^{N} a_k z^{-k}$.
The roots of a high-degree polynomial are extremely sensitive to its coefficients. A small change $\Delta a_k$ can cause a pole to migrate dramatically, potentially crossing the unit circle $|z|=1$, rendering a stable filter unstable.

**Cascade Form:**
To mitigate this, high-order IIR filters are factored into second-order sections (biquads).
$$ H(z) = \prod_{k=1}^{M} \frac{b_{0k} + b_{1k}z^{-1} + b_{2k}z^{-2}}{1 - a_{1k}z^{-1} - a_{2k}z^{-2}} $$
The roots of a quadratic equation are far less sensitive to its coefficients. Thus, cascade forms are robust against coefficient quantization.

**Physical Interpretation:**
Imagine balancing 10 blocks on top of each other (Direct form). A slight breeze (quantization) knocks it over (instability). Cascade form is like having 5 separate stacks of 2 blocks—much more stable.

### 4.6 Roundoff Noise in Digital Filters
Every time two $B$-bit numbers are multiplied, the result requires $2B$ bits. To store this back in memory, it must be rounded back to $B$ bits. This rounding operation injects noise $e[n]$ into the system.

In an IIR filter, this noise is injected inside the recursive feedback loop. It gets filtered by the system itself before reaching the output.

If the transfer function from the noise injection point to the output is $H_e(z)$, then the output noise power $\sigma_o^2$ due to this single source is:
$$ \sigma_o^2 = \sigma_e^2 \sum_{n=0}^{\infty} |h_e[n]|^2 = \frac{\sigma_e^2}{2\pi} \int_{-\pi}^{\pi} |H_e(e^{j\omega})|^2 d\omega $$
where $\sigma_e^2 = \Delta^2 / 12$.

If there are $M$ multiplications, there are $M$ noise sources. Assuming they are uncorrelated, the total output noise is the sum of the individual contributions.

**Why feedback amplifies roundoff noise:**
If a pole is very close to the unit circle (e.g., $p = 0.99$), the impulse response $h_e[n] = (0.99)^n$ decays very slowly. The sum of squares $\sum |h_e[n]|^2 = \frac{1}{1 - (0.99)^2} \approx 50.25$. The noise injected by the multiplier is amplified by a factor of 50 before reaching the output!

### 4.7 Limit Cycles
Limit cycles are sustained oscillations at the output of a recursive filter when the input is zero or a constant. They are purely a consequence of non-linear fixed-point arithmetic.

**1. Granular Limit Cycles (Low-level oscillations):**
Caused by roundoff/truncation. Suppose a first-order filter $y[n] = x[n] + 0.9 y[n-1]$. Let $x[n]=0$ and $y[-1]=10$.
Ideally: $y[0]=9, y[1]=8.1, y[2]=7.29, \dots \to 0$.
With integer rounding:
$y[0] = \text{round}(0.9 \times 10) = 9$
$y[1] = \text{round}(0.9 \times 9) = \text{round}(8.1) = 8$
$y[2] = \text{round}(0.9 \times 8) = \text{round}(7.2) = 7$
...
$y[5] = \text{round}(0.9 \times 5) = \text{round}(4.5) = 5$ 
The output gets stuck at 5! This is the "deadband" effect. The signal cannot decay to zero.

**2. Overflow Limit Cycles (Large-scale oscillations):**
Caused by two's complement wraparound. If an addition exceeds the maximum value, it wraps to a huge negative number. This travels through the feedback loop, causing wild, full-scale oscillations.

**Solution:**
Using **saturation arithmetic** strictly bounds the energy in the system and definitively prevents overflow limit cycles. Granular limit cycles can be mitigated by increasing word length or injecting a tiny bit of random noise (dithering) to break the pattern.

### 4.8 Scaling to Prevent Overflow
To prevent overflow before it happens, we scale down the input signal by a factor $s$.
The signal at any internal node $v_k[n]$ must be constrained: $|v_k[n]| < 1$ (assuming fractional format).
If the transfer function from the input to node $k$ is $F_k(z)$, the bound is:
$$ |v_k[n]| = \left| \sum_{m=0}^{\infty} f_k[m] x[n-m] \right| \leq x_{max} \sum_{m=0}^{\infty} |f_k[m]| $$
To guarantee no overflow for ANY input bounded by 1, we must scale the input by:
$$ s \leq \frac{1}{\sum_{m=0}^{\infty} |f_k[m]|} $$
This is called the **L1-norm scaling rule**. It is very conservative.
A less strict rule is the **L2-norm scaling rule**, which prevents overflow for signals with bounded energy.

**Trade-off:**
Scaling down the signal prevents overflow, but it also reduces the signal power, effectively degrading the Signal-to-Noise Ratio (SQNR) due to roundoff noise.

### 4.9 Deeper Dive into Limit Cycle Mathematical Bounds
While the heuristic understanding of limit cycles is essential, advanced students should appreciate the rigorous mathematical bounds on limit cycle amplitudes.
Consider the second-order filter difference equation:
$$ y[n] = x[n] + a_1 y[n-1] + a_2 y[n-2] $$
When the input $x[n] = 0$, the unforced response in fixed-point arithmetic is subject to the quantization function $Q(\cdot)$:
$$ y[n] = Q(a_1 y[n-1] + a_2 y[n-2]) $$
The effective nonlinear error introduced at each step is $e[n]$, such that:
$$ y[n] = a_1 y[n-1] + a_2 y[n-2] + e[n] $$
where $-\frac{\Delta}{2} \leq e[n] \leq \frac{\Delta}{2}$ for rounding arithmetic.

**Jackson's Bound:**
A classic result by Jackson provides a bound on the absolute maximum amplitude of any granular limit cycle for a second-order filter with complex conjugate poles at $z = r e^{\pm j\theta}$.
The maximum amplitude $Y_{max}$ is bounded by:
$$ |y[n]| \leq Y_{max} \approx \frac{0.5 \Delta}{1 - a_2} \quad \text{for poles near the real axis} $$
and for poles with significant imaginary parts, an effective bound is:
$$ Y_{max} \approx \frac{0.5 \Delta}{1 - r} \cdot \frac{1}{\sin(\theta)} $$
This mathematical result beautifully explains why filters with poles close to the unit circle ($r \to 1$) exhibit massive limit cycles. As $r \to 1$, the denominator approaches 0, and the limit cycle amplitude approaches infinity (limited only by the dynamic range of the hardware).

**Physical Intuition of the Bound:**
A filter with $r \to 1$ is a highly resonant system. It has very little damping. When a small quantization error $e[n]$ is injected, the system cannot damp it out quickly. Over time, these small errors accumulate constructively, driving the output to a high amplitude before the non-linearity of the rounding process balances the energy out.

### 4.10 Extended Analysis of Dithering
As mentioned briefly, **dithering** is a powerful technique for breaking limit cycles and linearizing the quantization process. 
Instead of simply quantizing the signal $x[n]$:
$$ y[n] = Q(x[n]) $$
We intentionally add a small, random noise signal $d[n]$ (the dither) before quantization:
$$ y[n] = Q(x[n] + d[n]) $$

**Why Dither Works:**
By injecting noise that is statistically independent of the signal, we force the quantization error to decorrelate from the signal itself. 
Consider a very slow-moving sinusoidal signal whose amplitude is smaller than $\Delta$. Without dither, the quantizer output will be a constant zero (a massive distortion, effectively destroying the signal).
With dither, the signal pushes the random noise probabilistically across the quantization threshold. The output will bounce rapidly between 0 and $\Delta$. If we average this rapid bouncing (e.g., via the low-pass filtering inherent in human hearing or a subsequent digital filter), the original small sinusoid is recovered!

**Types of Dither:**
1. **Rectangular Probability Density Function (RPDF) Dither:** Noise is uniformly distributed between $-\Delta/2$ and $\Delta/2$. This eliminates distortion but does not eliminate noise modulation (the noise floor pumps up and down with the signal).
2. **Triangular Probability Density Function (TPDF) Dither:** Noise is generated by summing two independent RPDF noise sources. It eliminates both distortion and noise modulation, making it the industry standard for high-fidelity audio DSP.

### 4.11 Extended Note on L2 Norm Scaling
While we discussed L1 norm scaling ($S \leq 1 / \sum |h[n]|$), it is often considered too pessimistic. The L1 norm assumes the worst possible input sequence (a signal that perfectly matches the sign of the impulse response at every instant). In reality, natural signals (like voice or music) do not do this.
A more realistic bound for natural signals is the L2 norm scaling, based on Parseval's theorem.
The output energy is bounded by the input energy multiplied by the maximum power gain of the filter:
$$ \sum_{n} |y[n]|^2 \leq \left( \max_{\omega} |H(e^{j\omega})|^2 \right) \sum_{n} |x[n]|^2 $$
To prevent overflow for signals of bounded energy, we often scale using the L2 norm of the impulse response:
$$ L_2 = \sqrt{\sum_{n=0}^{\infty} |h[n]|^2} $$
Scaling by $1/L_2$ allows the signal to run 'hotter' (higher amplitude) than L1 scaling, yielding a better SQNR. However, there is a tiny statistical probability of overflow, which must be handled gracefully by saturation arithmetic.

---
## 5. COMPLETE PROOFS AND DERIVATIONS

### Proof: Quantization Noise Variance is $\Delta^2 / 12$
**Theorem:** For a uniform round-off quantizer with step size $\Delta$, assuming the error $e$ is uniformly distributed, the noise variance is $\Delta^2 / 12$.

**Proof:**
1. Let the continuous quantization error be a random variable $E$.
2. Because it is a rounding quantizer, the error is strictly bounded between $-\Delta/2$ and $+\Delta/2$.
3. The assumption of uniform distribution implies the PDF is:
   $$ f_E(e) = \frac{1}{\Delta} \quad \text{for } -\frac{\Delta}{2} \leq e \leq \frac{\Delta}{2} $$
4. The mean (expected value) of $E$ is:
   $$ \mu_e = \int_{-\infty}^{\infty} e \cdot f_E(e) de = \int_{-\Delta/2}^{\Delta/2} e \frac{1}{\Delta} de = \frac{1}{\Delta} \left[ \frac{e^2}{2} \right]_{-\Delta/2}^{\Delta/2} $$
   $$ \mu_e = \frac{1}{\Delta} \left( \frac{\Delta^2}{8} - \frac{\Delta^2}{8} \right) = 0 $$
5. The variance $\sigma_e^2$ is the second central moment:
   $$ \sigma_e^2 = \int_{-\infty}^{\infty} (e - \mu_e)^2 f_E(e) de = \int_{-\Delta/2}^{\Delta/2} e^2 \frac{1}{\Delta} de $$
6. Evaluating the integral:
   $$ \sigma_e^2 = \frac{1}{\Delta} \left[ \frac{e^3}{3} \right]_{-\Delta/2}^{\Delta/2} = \frac{1}{3\Delta} \left( \left(\frac{\Delta}{2}\right)^3 - \left(-\frac{\Delta}{2}\right)^3 \right) $$
   $$ \sigma_e^2 = \frac{1}{3\Delta} \left( \frac{\Delta^3}{8} - \left(-\frac{\Delta^3}{8}\right) \right) = \frac{1}{3\Delta} \left( \frac{2\Delta^3}{8} \right) = \frac{1}{3\Delta} \left( \frac{\Delta^3}{4} \right) $$
7. Final Result:
   $$ \sigma_e^2 = \frac{\Delta^2}{12} $$
   **Q.E.D.**

**Physical intuition:** The factor of 1/12 is fundamental to the variance of any uniform distribution. It tells us that while the maximum instantaneous error is $\Delta/2$, the average "power" of the error is significantly lower because large errors are just as likely as small errors.

---
## 6. WORKED EXAMPLES (MINIMUM 5 — fully solved)

### Example 1: ADC Resolution and Noise Power
**Problem statement:** 
An analog signal is constrained to a range of $-10$ V to $+10$ V. It is quantized using a 12-bit Analog-to-Digital Converter (ADC). Calculate the step size $\Delta$ and the quantization noise power, assuming uniform rounding.

**Solution:**
1. Determine the full-scale range $R$:
   $$ R = X_{max} - X_{min} = 10 - (-10) = 20 \text{ V} $$
2. Determine the number of quantization levels $L$ for a 12-bit ADC:
   $$ L = 2^{12} = 4096 $$
3. Calculate the step size $\Delta$:
   $$ \Delta = \frac{R}{L} = \frac{20}{4096} = 0.0048828 \text{ V} $$
4. Calculate the quantization noise power $\sigma_e^2$:
   $$ \sigma_e^2 = \frac{\Delta^2}{12} = \frac{(0.0048828)^2}{12} = \frac{2.384 \times 10^{-5}}{12} \approx 1.986 \times 10^{-6} \text{ V}^2 $$

**Physical interpretation:** The noise power is nearly 2 micro-watts (assuming 1-ohm load). This is exceptionally quiet, highlighting why 12-bit is sufficient for many industrial sensors.
**Common mistakes to avoid:** Forgetting to square $\Delta$ before dividing by 12, or using $X_{max}$ instead of the full peak-to-peak range.

### Example 2: SQNR of a Full-Scale Sinusoid
**Problem statement:**
Derive the required number of bits for an ADC to achieve a Signal-to-Quantization-Noise Ratio (SQNR) of at least 80 dB for a full-scale sinusoidal input.

**Solution:**
1. Use the derived SQNR formula for a full-scale sinusoid:
   $$ \text{SQNR}_{dB} = 6.02 B + 1.76 $$
2. Set up the inequality:
   $$ 6.02 B + 1.76 \geq 80 $$
3. Solve for B:
   $$ 6.02 B \geq 80 - 1.76 $$
   $$ 6.02 B \geq 78.24 $$
   $$ B \geq \frac{78.24}{6.02} \approx 12.996 $$
4. Since the number of bits must be an integer, we round up to the next whole number.
   $$ B = 13 \text{ bits} $$

**Physical interpretation:** To guarantee 80 dB of dynamic range, standard 12-bit ADCs (74 dB) are insufficient. A 14-bit or 16-bit ADC must be selected by the engineer.
**Common mistakes to avoid:** Rounding down to 12 bits instead of taking the ceiling, which would result in missing the 80 dB requirement.

### Example 3: Filter Scaling to Prevent Overflow
**Problem statement:**
A digital filter has the impulse response $h[n] = (0.5)^n u[n]$. The input $x[n]$ is bounded by $|x[n]| \leq 1$. Calculate the required scale factor $S$ to ensure that the filter output never overflows (i.e., $|y[n]| \leq 1$ for all $n$).

**Solution:**
1. The worst-case output magnitude occurs when the input sequence matches the sign of the impulse response perfectly (L1-norm condition).
   $$ |y[n]|_{max} = X_{max} \sum_{n=0}^{\infty} |h[n]| $$
2. Calculate the L1-norm of the impulse response:
   $$ \sum_{n=0}^{\infty} |(0.5)^n| = 1 + 0.5 + 0.25 + 0.125 + \dots $$
3. This is an infinite geometric series with $a=1$ and $r=0.5$.
   $$ \sum_{n=0}^{\infty} |h[n]| = \frac{1}{1 - 0.5} = \frac{1}{0.5} = 2 $$
4. Without scaling, the maximum output could reach $1 \times 2 = 2$, which overflows a $[-1, 1)$ fixed-point system.
5. The required scale factor $S$ must satisfy:
   $$ S \leq \frac{1}{\sum |h[n]|} $$
   $$ S \leq \frac{1}{2} = 0.5 $$
Therefore, the input must be multiplied by $0.5$ (or right-shifted by 1 bit) before entering the filter.

**Physical interpretation:** Because the filter accumulates energy over time, an input that is constantly at maximum amplitude will cause the internal state to build up to twice the input level. Scaling gives the signal enough "headroom" to grow without clipping.
**Common mistakes to avoid:** Calculating the energy (sum of squares) instead of the absolute sum.

### Example 4: Output Roundoff Noise Variance
**Problem statement:**
A first-order IIR filter is defined by $y[n] = x[n] + 0.6 y[n-1]$. The system uses 8-bit rounding arithmetic with a range of $[-1, 1)$. Assume quantization noise is injected after the multiplier. Calculate the total output noise variance.

**Solution:**
1. Determine the step size $\Delta$ for an 8-bit system spanning 2 units:
   $$ \Delta = \frac{2}{2^8} = \frac{2}{256} = 2^{-7} $$
2. Calculate the variance of the injected noise source $\sigma_e^2$:
   $$ \sigma_e^2 = \frac{\Delta^2}{12} = \frac{(2^{-7})^2}{12} = \frac{2^{-14}}{12} = \frac{1}{12 \times 16384} \approx 5.08 \times 10^{-6} $$
3. Identify the noise transfer function $H_e(z)$. The noise is injected at the same point as the input, so it passes through the same recursive path.
   $$ H_e(z) = \frac{1}{1 - 0.6 z^{-1}} $$
4. The corresponding impulse response is $h_e[n] = (0.6)^n u[n]$.
5. Calculate the noise gain (sum of squares of impulse response):
   $$ G_{noise} = \sum_{n=0}^{\infty} (h_e[n])^2 = \sum_{n=0}^{\infty} (0.6^{2})^n = \sum_{n=0}^{\infty} (0.36)^n $$
6. Sum the geometric series:
   $$ G_{noise} = \frac{1}{1 - 0.36} = \frac{1}{0.64} = 1.5625 $$
7. Calculate the total output noise variance:
   $$ \sigma_o^2 = \sigma_e^2 \times G_{noise} \approx 5.08 \times 10^{-6} \times 1.5625 = 7.94 \times 10^{-6} $$

**Physical interpretation:** The noise injected by the multiplier is magnified by roughly 56% because it circulates through the feedback loop. 
**Common mistakes to avoid:** Forgetting to square the impulse response terms before summing them. The formula requires Parseval's theorem (energy), not just the sum of the terms.

### Example 5: Deadband and Granular Limit Cycles
**Problem statement:**
Consider the recursive system $y[n] = \text{round}(0.8 y[n-1] + x[n])$. 
Assume $x[n] = 0$ for $n \geq 0$, and the initial condition is $y[-1] = 3$. The system rounds to the nearest integer. Determine the filter output for $n=0, 1, 2, 3, 4$ and identify the limit cycle.

**Solution:**
1. Compute the sequence step by step using the rounding function:
   $$ n=0: \quad y[0] = \text{round}(0.8 \times 3 + 0) = \text{round}(2.4) = 2 $$
   $$ n=1: \quad y[1] = \text{round}(0.8 \times 2 + 0) = \text{round}(1.6) = 2 $$
   $$ n=2: \quad y[2] = \text{round}(0.8 \times 2 + 0) = \text{round}(1.6) = 2 $$
   $$ n=3: \quad y[3] = \text{round}(0.8 \times 2) = 2 $$
2. The output sequence is $y[n] = \{2, 2, 2, 2, \dots\}$.
3. The theoretical response of $0.8^n \times 3$ should decay to zero. However, due to finite integer precision, it gets stuck at 2.
4. The deadband boundary can be found where the rounding error exactly balances the decay:
   $$ 0.8 y = y - 0.5 \implies 0.2 y = 0.5 \implies y = 2.5 $$
   Any value below 2.5 will get stuck.

**Physical interpretation:** This is the "deadband" effect. It sounds like a low-level persistent hum or DC offset in an audio system that remains even when the music stops playing.
**Common mistakes to avoid:** Assuming rounding behaves like theoretical math. One must explicitly apply the rounding operation at every single discrete time step.

### Example 6: Extended IIR Filter Noise Gain
**Problem statement:**
Consider a second-order IIR filter given by the transfer function:
$$ H(z) = \frac{1}{(1 - 0.5z^{-1})(1 - 0.4z^{-1})} $$
Assuming that a single noise source $e[n]$ (from fixed-point multiplication) is injected at the input of this filter, calculate the exact noise gain $G$.
**Solution:**
1. First, perform partial fraction expansion on $H(z)$:
   $$ H(z) = \frac{A}{1 - 0.5z^{-1}} + \frac{B}{1 - 0.4z^{-1}} $$
   Solving for A and B:
   For $A$: multiply by $(1 - 0.5z^{-1})$ and set $z^{-1} = 2$:
   $$ A = \frac{1}{1 - 0.4(2)} = \frac{1}{1 - 0.8} = \frac{1}{0.2} = 5 $$
   For $B$: multiply by $(1 - 0.4z^{-1})$ and set $z^{-1} = 2.5$:
   $$ B = \frac{1}{1 - 0.5(2.5)} = \frac{1}{1 - 1.25} = \frac{1}{-0.25} = -4 $$
   So, $H(z) = \frac{5}{1 - 0.5z^{-1}} - \frac{4}{1 - 0.4z^{-1}}$.
2. The impulse response is:
   $$ h[n] = (5(0.5)^n - 4(0.4)^n) u[n] $$
3. The noise gain $G$ is the sum of squares:
   $$ G = \sum_{n=0}^{\infty} (h[n])^2 = \sum_{n=0}^{\infty} (5(0.5)^n - 4(0.4)^n)^2 $$
4. Expand the squared term:
   $$ (h[n])^2 = 25(0.25)^n - 40(0.2)^n + 16(0.16)^n $$
5. Sum each geometric series separately:
   $$ \sum_{n=0}^{\infty} 25(0.25)^n = 25 \left(\frac{1}{1 - 0.25}\right) = 25 \left(\frac{1}{0.75}\right) = \frac{100}{3} \approx 33.33 $$
   $$ \sum_{n=0}^{\infty} -40(0.2)^n = -40 \left(\frac{1}{1 - 0.2}\right) = -40 \left(\frac{1}{0.8}\right) = -50 $$
   $$ \sum_{n=0}^{\infty} 16(0.16)^n = 16 \left(\frac{1}{1 - 0.16}\right) = 16 \left(\frac{1}{0.84}\right) = \frac{1600}{84} = \frac{400}{21} \approx 19.05 $$
6. Total noise gain:
   $$ G = \frac{100}{3} - 50 + \frac{400}{21} = \frac{700}{21} - \frac{1050}{21} + \frac{400}{21} = \frac{50}{21} \approx 2.38 $$
**Physical Interpretation:**
Despite having two poles, the overall noise amplification is relatively small (gain of ~2.38) because the poles are well within the unit circle (0.5 and 0.4) and the partial fractions partially cancel each other out.

### Example 7: Advanced Limit Cycle Deadband Calculation
**Problem statement:**
A first-order digital filter is given by $y[n] = \text{round}(0.95 y[n-1] + x[n])$. Find the exact range of values (the deadband) where the filter output will get stuck if the input $x[n]$ becomes zero. Assume integer rounding.
**Solution:**
1. Let the steady-state stuck value be $Y_s$.
2. In the absence of input, the difference equation becomes:
   $$ Y_s = \text{round}(0.95 Y_s) $$
3. The rounding operation implies that the argument must be within $\pm 0.5$ of the integer result:
   $$ -0.5 \leq 0.95 Y_s - Y_s < 0.5 $$
4. Simplify the inequality:
   $$ -0.5 \leq -0.05 Y_s < 0.5 $$
5. Divide by $-0.05$ (remembering to flip the inequality signs):
   $$ \frac{0.5}{0.05} > Y_s \geq \frac{-0.5}{0.05} $$
   $$ 10 > Y_s \geq -10 $$
6. Therefore, the deadband is the set of integers from $-10$ to $9$.
**Physical Interpretation:**
If the filter state ever enters this range while the input is zero, the signal will not decay any further. A pole at 0.95 is very close to 1, causing a massive deadband (20 distinct integer states). If the pole were 0.5, the deadband would only be $\pm 1$. This proves mathematically that highly resonant filters suffer from severe granular limit cycles.

---
## 7. ENGINEERING APPLICATIONS AND CASE STUDIES

**Case Study 1: Audio DSP in Active Noise Cancellation (ANC) Headphones**
ANC headphones use adaptive FIR/IIR filters to invert background noise. These run on low-power, fixed-point DSPs (e.g., 24-bit processors) to conserve battery. The engineers must carefully scale the microphone inputs to avoid overflow limit cycles. If an overflow limit cycle occurs, the user would suddenly hear a deafening, full-volume screech right next to their eardrum. Saturation arithmetic is absolutely mandatory in this application.

**Case Study 2: Engine Control Units (ECU) in Automotive**
An ECU controls fuel injection timing using PID controllers, which are mathematically IIR filters. These operate on 16-bit or 32-bit automotive-grade microcontrollers. Quantization of the control coefficients can cause the poles of the PID loop to shift, potentially causing the engine idle speed to oscillate erratically (a limit cycle). Engineers utilize Cascade (Biquad) structures for the controllers to minimize coefficient sensitivity and guarantee stable engine performance.

---
## 8. COMMON STUDENT MISCONCEPTIONS AND ERRORS
1. **Misconception:** "Quantization noise is actual, random thermal noise generated by the circuit."
   **Correction:** Quantization noise is completely deterministic. If you input the exact same sequence into an ADC twice, you get the exact same error twice. We only *model* it as random white noise because the error pattern is so complex it behaves statistically like noise. It is purely a mathematical error, not a physical thermal noise.
2. **Misconception:** "Double-precision floating-point is always better; we should never use fixed-point."
   **Correction:** Fixed-point arithmetic uses significantly less silicon area and consumes drastically less power. In mass-produced consumer electronics, IoT devices, and deeply embedded systems, fixed-point is king. The engineer's job is to make fixed-point work perfectly via proper scaling, not to default to expensive floating-point hardware just to save design effort.
3. **Misconception:** "Scaling down the input solves all overflow problems with no downsides."
   **Correction:** Scaling down the input reduces the signal power. Since the roundoff noise floor remains constant (based on $\Delta$), scaling down directly reduces the Signal-to-Noise Ratio (SQNR). It is a fundamental trade-off between overflow protection and noise performance.
4. **Misconception:** "FIR filters can suffer from limit cycles just like IIR filters."
   **Correction:** Limit cycles require feedback to sustain the oscillation. FIR filters have no recursive feedback loops. Once the input stops, an FIR filter will completely flush to zero after $N$ samples. Limit cycles are exclusively an IIR phenomenon.
5. **Misconception:** "A pole at $z=0.99$ is safe because it is inside the unit circle."
   **Correction:** In a theoretical continuous math domain, yes. But in a 16-bit fixed-point DSP, coefficient quantization might shift that pole to $z=1.002$. The filter is now unstable. Poles close to the unit circle are extremely dangerous in fixed-point implementations, and usually require cascading biquads to maintain stability.
6. **Misconception:** "Increasing the word length from 16 to 32 bits solves coefficient quantization but not signal roundoff."
   **Correction:** Increasing word length solves both. It provides more bits for representing the exact values of coefficients (preventing pole drift) and it provides a dramatically smaller $\Delta$ for signal values, which massively reduces the variance of the injected roundoff noise by 96 dB.
7. **Misconception:** "Truncation is better than rounding because it is faster to compute."
   **Correction:** While truncation just drops bits (requiring zero hardware logic), it introduces a severe DC offset into the signal because the error is strictly negative (or positive depending on sign). Rounding requires an adder (to add 0.5 LSB before truncating), but produces a zero-mean error, which is critical for avoiding DC buildup in recursive filters.

---
## 9. CONNECTIONS TO OTHER LECTURES

* **Builds upon Lecture 15 (IIR Filter Design):** You designed Butterworth and Chebyshev filters in floating-point. Today we saw how those designs break down in real hardware if not partitioned into Cascade form. The steep roll-off of a high-order Chebyshev filter often results in poles extremely close to the unit circle, making it particularly vulnerable to quantization.
* **Builds upon Lecture 7 (Z-Transform):** The concept of pole locations dictating stability was vital for understanding coefficient quantization sensitivity. The region of convergence (ROC) analysis directly explains why shifting a pole beyond $|z|=1$ destroys the system.
* **Connects to Lecture 18 (FIR Filter Implementation):** FIR filters avoid limit cycles and coefficient sensitivity issues. This lecture explains *why* engineers often prefer FIR filters despite their higher computational cost (more taps required)—they are unconditionally stable and much easier to implement in fixed-point math.
* **Sets the stage for Lecture 23 (Multirate Signal Processing):** When we learn about Decimation and Interpolation, managing word-lengths and scaling during the filtering stages will be critical to prevent overflow. Upsampling (interpolation) often involves inserting zeros and then low-pass filtering, which must be scaled carefully to avoid dynamic range issues.
* **Relates to Lecture 27 (Adaptive Filtering):** When implementing Least Mean Squares (LMS) adaptive filters in fixed point, the coefficient update equation can suffer from stalling (a type of limit cycle) due to quantization. The concepts of deadbands discussed here apply directly to adaptive weight updates.

---
## 10. EXAMINATION QUESTIONS

### 10.1 Short Answer
**Q1:** What is the fundamental difference between truncation and rounding in terms of the quantization error mean?
**Model Answer:** Rounding produces a zero-mean quantization error ($-\Delta/2$ to $\Delta/2$). Truncation always discards bits, resulting in a strictly non-zero, negative mean error ($-\Delta$ to $0$), which introduces a DC offset into the signal.

**Q2:** State the primary advantage of Saturation Arithmetic in DSP.
**Model Answer:** Saturation arithmetic clamps overflowing values to the maximum representable limit rather than wrapping around. This strictly bounds the signal energy and prevents high-amplitude overflow limit cycles in recursive filters.

**Q3:** Why are Direct Form IIR filters rarely used for orders greater than 2 in fixed-point hardware?
**Model Answer:** The roots of high-degree polynomials are hypersensitive to changes in their coefficients. Small quantization errors in the coefficients of a high-order Direct Form filter can easily push poles outside the unit circle, causing instability.

**Q4:** According to the 6-dB rule, how much does the SQNR increase if you upgrade from a 10-bit ADC to a 12-bit ADC?
**Model Answer:** Every bit adds approximately 6.02 dB. Upgrading by 2 bits yields an increase of $2 \times 6.02 = 12.04$ dB.

**Q5:** What structural condition guarantees the absolute absence of limit cycles in an IIR filter?
**Model Answer:** Limit cycles are eliminated if the filter is realized using structural topologies that are strictly passive (energy-dissipating), such as Wave Digital Filters or coupled-form state-space structures, combined with magnitude truncation arithmetic.

### 10.2 Long Answer / Numerical Problems
**Problem 1:** 
A continuous-time signal with a bandwidth of 5 kHz and a dynamic range of $\pm 5$ V is sampled and quantized. If the system requires a minimum SQNR of 65 dB for full-scale sine waves, what is the minimum required ADC bit depth? What is the resulting step size?
**Solution:**
1. $\text{SQNR}_{dB} = 6.02 B + 1.76 \geq 65$
2. $6.02 B \geq 63.24 \implies B \geq 10.5$
3. Round up to nearest integer: $B = 11$ bits.
4. Total voltage range $R = 5 - (-5) = 10$ V.
5. Number of levels $L = 2^{11} = 2048$.
6. Step size $\Delta = \frac{10}{2048} \approx 4.88$ mV.

**Problem 2:**
Consider $H(z) = \frac{1}{1 - 0.75z^{-1}}$. A white noise source with variance $\sigma_e^2 = 2 \times 10^{-6}$ is injected immediately after the multiplier. Calculate the output noise variance.
**Solution:**
1. The noise transfer function is $H_e(z) = H(z) = \frac{1}{1 - 0.75z^{-1}}$.
2. Impulse response $h_e[n] = (0.75)^n u[n]$.
3. Noise gain $G = \sum_{n=0}^{\infty} (h_e[n])^2 = \sum (0.5625)^n = \frac{1}{1 - 0.5625} = \frac{1}{0.4375} \approx 2.285$.
4. Output variance $\sigma_o^2 = \sigma_e^2 \times G = (2 \times 10^{-6}) \times 2.285 = 4.57 \times 10^{-6}$.

**Problem 3:**
For the filter $H(z) = \frac{1}{1 - 0.5z^{-1}}$, calculate the necessary scaling factor $S$ using the L1-norm scaling rule to prevent overflow for any input bounded by $\pm 1$.
**Solution:**
1. Impulse response $h[n] = (0.5)^n u[n]$.
2. $L_1 = \sum_{n=0}^{\infty} |h[n]| = \sum_{n=0}^{\infty} |(0.5)^n| = \frac{1}{1 - 0.5} = 2$.
3. The scale factor must be $S \leq \frac{1}{L_1} = 0.5$.

**Problem 4:**
Demonstrate a granular limit cycle for the system $y[n] = \text{truncate}(0.9 y[n-1] + x[n])$ for zero input $x[n]=0$ and initial condition $y[-1]=-4$. Truncation toward zero.
**Solution:**
1. $y[0] = \text{trunc}(0.9 \times -4) = \text{trunc}(-3.6) = -3$.
2. $y[1] = \text{trunc}(0.9 \times -3) = \text{trunc}(-2.7) = -2$.
3. $y[2] = \text{trunc}(0.9 \times -2) = \text{trunc}(-1.8) = -1$.
4. $y[3] = \text{trunc}(0.9 \times -1) = \text{trunc}(-0.9) = 0$.
5. $y[4] = \text{trunc}(0.9 \times 0) = 0$.
Because truncation drops the fractional part toward zero, the signal successfully decays to zero. This demonstrates that magnitude truncation is a technique used to *prevent* deadbands!

### 10.3 True/False with Justification
1. **True/False:** Overflow limit cycles can be completely eliminated by using floating-point arithmetic.
   * **True.** Floating-point hardware automatically scales the exponent, preventing hard limits and wraparound that cause overflow limit cycles.
2. **True/False:** An FIR filter is highly susceptible to granular limit cycles.
   * **False.** FIR filters have no feedback loops. Limit cycles require feedback.
3. **True/False:** The quantization noise variance for rounding is twice as large as the variance for truncation.
   * **False.** Rounding has variance $\Delta^2/12$. Truncation has error distributed from $-\Delta$ to $0$, so its variance is also $\Delta^2/12$ (though its mean is non-zero). 
4. **True/False:** Cascade form realization reduces the sensitivity of filter poles to coefficient quantization.
   * **True.** Factoring into 2nd-order sections decouples the roots, making them depend on fewer quantized coefficients.
5. **True/False:** The 6-dB rule applies exactly to all signal types, including DC.
   * **False.** The derivation assumes a full-scale sinusoid and uniform error distribution. For DC, the error is constant and deterministic.
6. **True/False:** L1 scaling is more conservative (stricter) than L2 scaling.
   * **True.** L1 scaling guarantees no overflow for *any* bounded input, whereas L2 only bounds energy, potentially allowing occasional instantaneous overflow.
7. **True/False:** Saturation arithmetic completely eliminates quantization noise in digital filters.
   * **False.** Saturation arithmetic only prevents overflow limit cycles by clipping signals that exceed the maximum range. It does not affect the small-scale quantization errors (roundoff noise) that occur within the valid signal range.
8. **True/False:** Dithering increases the total noise power in a system but improves perceptual quality.
   * **True.** Adding dither injects additional noise power into the signal prior to quantization, but it decorrelates the quantization error from the signal, turning harmonic distortion (which is highly noticeable and unpleasant) into broadband white noise (which is more tolerable and can be filtered).

### 10.4 Conceptual Essay Questions
**Question 1:**
Explain the fundamental trade-off between scaling for overflow prevention and Signal-to-Quantization-Noise Ratio (SQNR) in a fixed-point DSP system. How can an engineer optimize this trade-off?
**Model Answer:**
To prevent overflow in fixed-point filters, the input signal must be scaled down (attenuated). However, the internal roundoff noise generated by multiplications depends solely on the fixed step size $\Delta$ (i.e., the bit depth of the processor), not the signal amplitude. Therefore, when the signal is scaled down, its power decreases while the noise floor remains constant, directly degrading the SQNR. If scaled too aggressively (e.g., using strictly L1 norm), the filter is perfectly safe from overflow but the output might be buried in quantization noise. To optimize this, engineers often use the less conservative L2 norm scaling, accepting a minuscule statistical probability of overflow, and implement saturation arithmetic as a safety net to catch those rare overflow events without causing catastrophic limit cycles.

**Question 2:**
Contrast the effects of coefficient quantization with signal roundoff in digital filters. Which one affects the system's transfer function, and how?
**Model Answer:**
Coefficient quantization occurs during the design and implementation phase when the ideal infinite-precision filter tap values ($a_k, b_k$) are rounded to fit into memory. This permanently alters the transfer function of the filter, shifting the locations of poles and zeros. It can change the cutoff frequency, ripple, and in extreme cases, push poles outside the unit circle, causing instability. 
Conversely, signal roundoff occurs continuously during real-time operation every time a multiplication is performed. It does not change the filter's transfer function or pole/zero locations. Instead, it acts as an additive noise source injected into the signal path, degrading the signal quality (SQNR) and potentially causing granular limit cycles due to nonlinear feedback behavior.

---
## 11. KEY FORMULAS REFERENCE

| Concept | Formula / Equation | Description |
| :--- | :--- | :--- |
| **Quantization Step Size** | $\Delta = \frac{X_{max} - X_{min}}{2^B}$ | Resolution of a B-bit uniform quantizer |
| **Noise Variance (Rounding)** | $\sigma_e^2 = \frac{\Delta^2}{12}$ | Power of the quantization noise |
| **SQNR (Full-Scale Sine)** | $\text{SQNR}_{dB} = 6.02B + 1.76$ | Signal-to-noise ratio in decibels |
| **Filter Output Noise Gain** | $G = \sum_{n=0}^{\infty} h_e^2[n]$ | Amplification of injected noise by the filter |
| **Total Output Noise** | $\sigma_o^2 = \sigma_e^2 \times G$ | Final variance at the filter output |
| **L1 Scaling Factor** | $S \leq \frac{1}{\sum_{n=0}^{\infty} \|h[n]\|}$ | Prevents overflow for any input bounded by 1 |
| **Two's Complement Value** | $X = -b_0 + \sum_{i=1}^{B-1} b_i 2^{-i}$ | Fractional fixed-point representation |

---
## 12. FURTHER READING AND REFERENCES
1. **Proakis, J. G., & Manolakis, D. G. (2006).** *Digital Signal Processing: Principles, Algorithms, and Applications* (4th Ed.). Chapter 9: Practical Implementation of DSP Systems.
2. **Oppenheim, A. V., & Schafer, R. W. (2010).** *Discrete-Time Signal Processing* (3rd Ed.). Chapter 6: Structures for Discrete-Time Systems (focus on Finite-Precision Numerical Effects).
3. **Haykin, S. (2002).** *Adaptive Filter Theory* (4th Ed.). (For advanced discussions on limit cycles in adaptive contexts).
4. **Texas Instruments Application Notes:** "Fixed-Point DSP Arithmetic" (Focuses on hardware-level saturation and Q-format multiplication).
</Faculty Notes — Lecture 21: Quantization Effects & Finite Word-Length>


### 13. APPENDIX: ADVANCED TOPICS IN QUANTIZATION

### 13. APPENDIX: ADVANCED TOPICS IN QUANTIZATION (For Honors / Graduate Study)

**13.1 Floating-Point Arithmetic Detailed Analysis**
While fixed-point representation utilizes a single integer with a static implied decimal point, floating-point arithmetic (specifically IEEE 754) dynamically moves the radix point. A single-precision floating-point number consists of 32 bits:
* **1 sign bit ($)**
* **8 exponent bits ($)**, biased by 127
* **23 mantissa bits ($)**, representing a fractional value between 1.0 and 2.0.

The value represented is:
 X = (-1)^s 	imes (1.M) 	imes 2^{E - 127} 

**Quantization Error in Floating Point:**
Unlike fixed-point, where the absolute error [n]$ is bounded by a constant $\Delta/2$, floating-point error is proportional to the signal amplitude.
 e[n] = x_q[n] - x[n] = \epsilon[n] 	imes x[n] 
where $\epsilon[n]$ is the relative error, bounded by the mantissa precision (roughly ^{-24}$ for single precision).
This implies that the SQNR in floating-point systems remains relatively constant over an enormous dynamic range, completely solving the small-signal degradation seen in fixed-point processors.

**13.2 Error-Shaping Filters**
In advanced oversampled data converters (like Sigma-Delta ADCs), quantization noise is not just accepted as flat white noise; it is actively shaped.
By placing the quantizer inside a feedback loop with a loop filter {loop}(z)$, we can create a system where the signal transfer function (STF) is flat (all-pass), but the noise transfer function (NTF) acts as a high-pass filter.
 Y(z) = STF(z) X(z) + NTF(z) E(z) 
This pushes the quantization noise energy out of the baseband (the frequencies of interest) and into the high-frequency spectrum, where it can be easily removed by a subsequent digital low-pass decimation filter. This is the fundamental magic behind how 1-bit ADCs can achieve 24-bit audio fidelity.

**13.3 Wave Digital Filters (WDF)**
Wave Digital Filters are a specialized class of IIR digital filters derived from analog LC (inductor-capacitor) ladder networks.
Why use them? Analog LC filters matched at both ports have a property of maximum power transfer, which mathematically implies that the sensitivity of the frequency response to component variations is zero at the passband ripples.
When this topology is mapped to the digital domain using the bilinear transform and wave variables, the resulting Wave Digital Filter inherits this incredible robustness. 
Furthermore, WDFs guarantee absolute absence of limit cycles (both granular and overflow) under zero-input conditions, provided that simple magnitude truncation is used at the multipliers. They are the gold standard for bullet-proof fixed-point IIR design in mission-critical applications.

**13.4 Sub-Band Coding and Adaptive Quantization**
In audio and speech compression (like MP3 or AAC), the quantization step size $\Delta$ is not fixed. Instead, the signal is split into multiple frequency sub-bands. The quantizer for each band dynamically adjusts its step size based on psychoacoustic models. 
If a band contains a very loud tone, the quantization noise in that band will be masked by the loud tone (simultaneous masking). Thus, fewer bits (larger $\Delta$) can be allocated to that band without the human ear noticing. Conversely, bands with quiet, critical details receive more bits (smaller $\Delta$). This demonstrates how understanding quantization noise allows engineers to intelligently hide it where it cannot be perceived, drastically reducing the data rate.

**13.5 Coefficient Sensitivity in FIR Filters**
While this lecture heavily emphasized IIR filters, it is important to briefly formalize FIR coefficient sensitivity. For a linear-phase FIR filter, the roots of the polynomial occur in reciprocal pairs ($ and /z$). Coefficient quantization preserves this linear-phase property (symmetry), but it moves the zeros. Because all zeros of an FIR filter contribute only to the frequency response shape (and not stability), the only penalty is a degradation in the stopband attenuation (e.g., stopband ripple increases). In contrast to IIR filters, stability is never at risk.

**13.6 Noise Variance in Floating-Point Filters**
The variance of round-off noise in floating point implementations differs substantially from fixed point. Because floating point quantization error is a relative error:
 \sigma_{e, float}^2 pprox \sigma_x^2 \cdot rac{2^{-2B}}{3} 
where $ is the mantissa length. This means the noise floor in a floating point system is heavily dependent on the signal variance $\sigma_x^2$ itself. The output noise variance of an IIR filter implemented in floating point is derived via a complex matrix summation that tracks the variance of internal state variables at every single node, a topic covered extensively in graduate adaptive filtering courses.
