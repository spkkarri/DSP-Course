<Faculty Notes — Lecture 23: Digital Oscillators & NCO>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY

Teaching digital oscillators bridges the gap between abstract z-domain theory and highly practical, real-world digital synthesis. Students often struggle with the transition from continuous-time analog oscillators (which rely on feedback and active components) to discrete-time difference equations. 

The concept of marginal stability, which in continuous time is achieved via poles strictly on the $j\omega$-axis, translates to poles strictly on the unit circle in the z-domain. A common difficulty is understanding why exact placement of poles on the unit circle is impossible in fixed-point arithmetic due to coefficient quantization, leading to amplitude drift.

**How to teach this lecture:**

Start with a comprehensive review of complex exponentials and how they form the basis of all signals. Emphasize that digital oscillators are essentially autonomous IIR filters. Then, pivot to the practical challenges of fixed-point math, showing that theoretical perfection breaks down. 

Introduce the NCO as the industry-standard solution to this problem, highlighting the paradigm shift from recursive calculation to phase accumulation.

**Prerequisite Checks:**

Ensure students are comfortable with the z-transform, finding poles from second-order difference equations, and Euler's formula. 
A quick review of phase accumulators in digital logic is also highly recommended before discussing NCOs. The students must recall that an ideal oscillator requires energy to be strictly conserved, which maps to poles on the unit circle in DSP.

**Suggested Demos:**

1. A MATLAB/Python script showing the output of a recursive oscillator with floating-point vs. 8-bit fixed-point coefficients to visually demonstrate amplitude drift (either decay to zero or unbounded growth).
2. An audio demo of an NCO generating a sine wave, followed by a chirp signal, to connect mathematical concepts to audible frequencies.
3. A real-time spectral analysis of a truncated phase accumulator, demonstrating the exact locations of spurs and how dithering flattens the noise floor.
4. A Simulink model comparing the computational complexity of the direct form oscillator versus the coupled Gold-Rader oscillator.
5. Hardware demonstration using an FPGA evaluation board, showing the output of a DDS core on an oscilloscope, emphasizing phase continuity during frequency hopping.

---
## 1. LEARNING OBJECTIVES

By the end of this highly detailed lecture, students will be able to:

1. **Derive** the recursive difference equation for a digital sinusoidal oscillator from the complex exponential sequence without omitting any algebraic steps.
2. **Analyze** the transfer function of the recursive oscillator to determine its pole locations and explain its marginal stability mathematically using the z-domain.
3. **Evaluate** the impact of finite-precision arithmetic (coefficient quantization) on the marginal stability and quantify the resulting amplitude drift of the oscillator in practical hardware.
4. **Formulate** the coupled oscillator equations to generate quadrature signals (sine and cosine) and explain how this structure mitigates some stability issues while using a rotation matrix.
5. **Design** a Numerically Controlled Oscillator (NCO) by calculating the exact tuning word for a desired output frequency given a system clock and phase accumulator bit-width.
6. **Quantify** the Spurious-Free Dynamic Range (SFDR) of an NCO due to phase truncation and explain how phase dithering fundamentally improves performance by spreading concentrated spur energy.
7. **Synthesize** linear frequency modulated (LFM) chirp signals using modified NCO architectures with dual cascaded accumulators.
8. **Compare** and contrast the architectural benefits of recursive IIR oscillators versus lookup-table-based Direct Digital Synthesis techniques in terms of memory usage, logic complexity, and spectral purity.

---
## 2. PREREQUISITE KNOWLEDGE REVIEW

Before engaging with this material, students must possess a firm grasp of the following concepts:

**1. The Z-Transform and Difference Equations:**

The relationship between a linear constant-coefficient difference equation and its transfer function $H(z)$. Students must recall the definition of the two-sided z-transform and its application to solving difference equations with zero initial conditions.

$$Y(z) = H(z)X(z)$$

The general form of a causal, rational transfer function is given by:

$$H(z) = \frac{\sum_{k=0}^{M} b_k z^{-k}}{1 + \sum_{k=1}^{N} a_k z^{-k}}$$

where $b_k$ are the feedforward coefficients and $a_k$ are the feedback coefficients. 
This formulation is critical because our oscillators will rely heavily on the denominator coefficients $a_k$.

**2. Pole-Zero Plots and System Stability:**

A causal LTI system is Bounded-Input Bounded-Output (BIBO) stable if and only if all poles of its transfer function $H(z)$ lie strictly inside the unit circle ($|p_i| < 1$). 

If any single pole is strictly on the unit circle ($|p_i| = 1$), and it is a simple (non-repeated) pole, the system is marginally stable. This means its impulse response will oscillate indefinitely with a constant amplitude, never decaying to zero nor growing to infinity. 

If there are repeated poles on the unit circle, the system becomes strictly unstable, and its output will grow linearly with time (e.g., a ramp multiplied by a sinusoid).

**3. Euler's Identities and Complex Variables:**

The foundation of connecting complex exponentials to real sinusoids. Students must be perfectly fluent in converting between polar and rectangular forms.

$$e^{j\theta} = \cos(\theta) + j\sin(\theta)$$

$$\cos(\theta) = \frac{e^{j\theta} + e^{-j\theta}}{2}$$

$$\sin(\theta) = \frac{e^{j\theta} - e^{-j\theta}}{2j}$$

These identities are paramount because our digital oscillators will be derived by observing the behavior of $e^{j\omega_0 n}$ in discrete time. Without Euler's formula, transitioning from the complex exponential to the real-valued recursive equation is impossible.

---
## 3. HISTORICAL AND MOTIVATIONAL CONTEXT

**Who discovered this?**

The shift from analog to digital signal processing in the late 20th century revolutionized waveform generation. Traditionally, Voltage-Controlled Oscillators (VCOs) and analog Phase-Locked Loops (PLLs) were used to generate carrier frequencies. However, analog oscillators are susceptible to component aging, thermal drift, and supply voltage variations. 

The concept of recursive digital oscillators arose early in the development of digital filters in the 1960s, primarily by pioneers such as Gold and Rader. The advent of Direct Digital Synthesis (DDS), however, is widely credited to Joseph Tierney, Charles Rader, and Bernard Gold at MIT Lincoln Laboratory in 1971. Their seminal paper provided a completely deterministic, digital method for frequency synthesis that circumvented the stability issues of recursive IIR filters entirely.

**Why does EEE need this? Real Engineering Applications:**

1. **Software-Defined Radios (SDR):** Modern transceivers use digital down-converters (DDC) and up-converters (DUC) that require precise local oscillators generated via NCOs. Without digital oscillators, an SDR cannot flexibly tune to arbitrary frequencies without swapping physical hardware crystals.
2. **Telecommunications:** Modems generating QAM, PSK, or FSK signals rely heavily on quadrature digital oscillators. Perfect orthogonality (exact 90-degree phase shift) is guaranteed in the digital domain, unlike analog circuits where phase imbalances severely degrade Error Vector Magnitude (EVM).
3. **RADAR and Sonar Systems:** Generating chirp signals (Linear Frequency Modulation) for pulse compression. The NCO architecture allows for perfectly linear sweeps that are impossible to guarantee with analog VCOs due to non-linear tuning curves.
4. **Test & Measurement Equipment:** Arbitrary Waveform Generators (AWGs) and vector network analyzers use DDS cores to produce low-phase-noise, highly stable signals with micro-Hertz resolution.
5. **Acoustic Engineering and Synthesizers:** Generating precise polyphonic notes in digital instruments without the detuning effects found in vintage analog synthesizers.

---
## 4. THEORETICAL FOUNDATIONS

### 4.1 Recursive Digital Sinusoidal Oscillator

We desire a discrete-time system that generates a sinusoidal sequence $y[n] = \sin(\omega_0 n)$ or $y[n] = \cos(\omega_0 n)$ autonomously, i.e., as its natural response to an impulse. Instead of computing the sine function directly using a Taylor series (which is computationally expensive and requires branching), we use a recursive filter structure.

Let us start with the complex exponential sequence, which elegantly contains both sine and cosine terms:

$$ y_c[n] = e^{j\omega_0 n} $$

To find a recursive relationship, we evaluate the sequence at adjacent time steps $n+1$ and $n-1$:

$$ y_c[n+1] = e^{j\omega_0 (n+1)} = e^{j\omega_0 n} \cdot e^{j\omega_0} $$

$$ y_c[n-1] = e^{j\omega_0 (n-1)} = e^{j\omega_0 n} \cdot e^{-j\omega_0} $$

Summing these two adjacent samples to eliminate the phase shift term and combine the complex exponents:

$$ y_c[n+1] + y_c[n-1] = e^{j\omega_0 n} \cdot e^{j\omega_0} + e^{j\omega_0 n} \cdot e^{-j\omega_0} $$

Factoring out the common term $e^{j\omega_0 n}$:

$$ y_c[n+1] + y_c[n-1] = e^{j\omega_0 n} (e^{j\omega_0} + e^{-j\omega_0}) $$

Recognizing that $e^{j\omega_0 n} = y_c[n]$ and applying Euler's formula for cosine:
$e^{j\omega_0} + e^{-j\omega_0} = 2\cos(\omega_0)$

Substituting this back into the equation:

$$ y_c[n+1] + y_c[n-1] = y_c[n] \cdot 2\cos(\omega_0) $$

Rearranging for the next sample $y_c[n+1]$ to make the system causal and computable from past states:

$$ y_c[n+1] = 2\cos(\omega_0)y_c[n] - y_c[n-1] $$

Shifting the time index by $-1$ yields the standard causal difference equation:

$$ y_c[n] = 2\cos(\omega_0)y_c[n-1] - y_c[n-2] $$

Because this equation is entirely real and linear, it holds for both the real part $\cos(\omega_0 n)$ and the imaginary part $\sin(\omega_0 n)$ independently. Therefore, the general real sinusoidal sequence $y[n]$ satisfies exactly the same difference equation:

$$ y[n] = 2\cos(\omega_0)y[n-1] - y[n-2] $$

**Physical Intuition:** 
This second-order infinite impulse response (IIR) system acts like an undamped pendulum. The term $2\cos(\omega_0)y[n-1]$ represents the restoring force that pulls the pendulum back toward equilibrium, while $-y[n-2]$ represents the inertia from the previous state. Once excited by an initial condition (like an impulse), it swings back and forth indefinitely without energy loss because there is no damping term ($r < 1$).

### 4.2 Transfer Function Analysis

To fully understand the frequency domain behavior of this oscillator, we take the Z-transform of the difference equation. Assuming zero initial conditions and an arbitrary excitation input $X(z)$ to start the oscillation:

$$ y[n] = 2\cos(\omega_0)y[n-1] - y[n-2] + x[n] $$

Taking the Z-transform of both sides:

$$ Y(z) = 2\cos(\omega_0)z^{-1}Y(z) - z^{-2}Y(z) + X(z) $$

Group all $Y(z)$ terms on the left side of the equation:

$$ Y(z) - 2\cos(\omega_0)z^{-1}Y(z) + z^{-2}Y(z) = X(z) $$

Factor out $Y(z)$:

$$ Y(z)(1 - 2\cos(\omega_0)z^{-1} + z^{-2}) = X(z) $$

The transfer function $H(z)$ is defined as the ratio of the output to the input:

$$ H(z) = \frac{Y(z)}{X(z)} = \frac{1}{1 - 2\cos(\omega_0)z^{-1} + z^{-2}} $$

Multiplying the numerator and the denominator by $z^2$ to write the function in terms of positive powers of $z$:

$$ H(z) = \frac{z^2}{z^2 - 2\cos(\omega_0)z + 1} $$

To find the poles of the system, we solve the characteristic equation (the denominator polynomial set to zero):

$$ z^2 - 2\cos(\omega_0)z + 1 = 0 $$

Using the quadratic formula for finding roots of $az^2 + bz + c = 0$:

$$ z = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a} $$

Substituting the coefficients $a=1, b=-2\cos(\omega_0), c=1$:

$$ z_{1,2} = \frac{2\cos(\omega_0) \pm \sqrt{4\cos^2(\omega_0) - 4(1)(1)}}{2} $$

Simplify the expression under the square root by factoring out the 4:

$$ z_{1,2} = \frac{2\cos(\omega_0) \pm 2\sqrt{\cos^2(\omega_0) - 1}}{2} $$

Divide out the 2:

$$ z_{1,2} = \cos(\omega_0) \pm \sqrt{\cos^2(\omega_0) - 1} $$

Since we know from standard trigonometry that $\cos^2(\omega_0) + \sin^2(\omega_0) = 1$, it follows that $\cos^2(\omega_0) - 1 = -\sin^2(\omega_0)$:

$$ z_{1,2} = \cos(\omega_0) \pm \sqrt{-\sin^2(\omega_0)} $$

The square root of a negative number introduces the imaginary unit $j$:

$$ z_{1,2} = \cos(\omega_0) \pm j\sin(\omega_0) $$

Using Euler's identity backward, we can express these roots in polar form:

$$ z_{1,2} = e^{\pm j\omega_0} $$

**Pole-Zero Plot Interpretation:**
The system has two complex conjugate poles located at angles $\pm \omega_0$ on the complex plane. 
The magnitude of these poles is $|z_{1,2}| = \sqrt{\cos^2(\omega_0) + \sin^2(\omega_0)} = 1$. 
Because the poles lie strictly on the unit circle, the system is marginally stable. This mathematical property is what guarantees a continuous, non-decaying oscillation. There are also two zeros located exactly at the origin ($z=0$), which affect the phase response but not the stability.

### 4.3 Amplitude Drift Problem and Solutions

In theoretical continuous math, the oscillator functions perfectly. However, in practical hardware (such as FPGAs, ASICs, or fixed-point DSP processors), numbers are represented with finite precision (fixed-point arithmetic). 

**The Impact of Coefficient Quantization:**

The coefficient $a_1 = 2\cos(\omega_0)$ cannot be represented exactly in binary unless $\omega_0$ corresponds to trivial angles (like $0, \pi/2, \pi$, where the cosine is exactly $0, 1,$ or $-1$).
Let the quantized coefficient be $\hat{a}_1$. The actual implemented characteristic equation is:

$$ z^2 - \hat{a}_1 z + 1 = 0 $$

The roots of this new equation are:

$$ z = \frac{\hat{a}_1 \pm \sqrt{\hat{a}_1^2 - 4}}{2} $$

As long as $|\hat{a}_1| < 2$, the roots remain complex conjugates. Notice that the constant term in the polynomial is still exactly 1 (which comes from the $-y[n-2]$ term). Because the product of the roots must equal the constant term ($z_1 \cdot z_2 = 1$), the magnitude of the poles remains exactly 1. 

Therefore, quantization of $a_1$ merely shifts the frequency of oscillation slightly, but does not move the poles off the unit circle. 

**The Real Issue: Round-Off Noise:**

While the poles remain on the unit circle, a much more insidious problem exists. At each time step, the multiplication $\hat{a}_1 \cdot y[n-1]$ produces a product with more bits than the original word length. This product must be rounded or truncated before being stored back into memory. 

This rounding operation injects a small quantization noise $e[n]$ at every step:

$$ y[n] = \hat{a}_1 y[n-1] - y[n-2] + e[n] $$

Because the poles of the system are exactly on the unit circle, the system acts as an infinite-Q resonator (an ideal integrator for signals at frequency $\omega_0$). If the noise spectrum has any energy at $\omega_0$, that energy is integrated indefinitely.

The injected quantization noise is accumulated without any damping, causing the amplitude of the oscillation to drift over time. It essentially performs a random walk, leading to an unbounded amplitude (overflowing the registers) or decaying to zero depending on the specific sequence of round-off errors.

**Solution: Periodic Renormalization**
To combat this, we must periodically force the amplitude back to 1. If we are generating quadrature signals, we compute the instantaneous amplitude:
$$ A = \sqrt{x_c[n]^2 + x_s[n]^2} $$
If $A$ deviates from 1, we divide the state variables by $A$. This requires a square root and division, which are computationally expensive, defeating the purpose of a fast recursive equation.

### 4.4 Coupled Oscillator Form (Quadrature Generation)

Many modern applications (e.g., QAM modulation) require both sine and cosine waveforms simultaneously (in-phase and quadrature signals). While we could run two independent recursive oscillators, a more robust architecture is the Coupled Oscillator (or Gold-Rader oscillator).

Consider the generation of the complex exponential directly. We define a complex state vector:

$$ x[n] = x_c[n] + jx_s[n] = e^{j\omega_0 n} $$

The fundamental recursive relationship for a complex exponential is a simple multiplication by $e^{j\omega_0}$:

$$ x[n] = e^{j\omega_0} x[n-1] $$

Substitute the rectangular forms for both the state and the exponential multiplier:

$$ x_c[n] + jx_s[n] = (\cos(\omega_0) + j\sin(\omega_0))(x_c[n-1] + jx_s[n-1]) $$

Expand the complex product on the right side of the equation:

$$ x_c[n] + jx_s[n] = \cos(\omega_0)x_c[n-1] + j\cos(\omega_0)x_s[n-1] + j\sin(\omega_0)x_c[n-1] + j^2\sin(\omega_0)x_s[n-1] $$

Since $j^2 = -1$, we can group the real and imaginary terms:

$$ x_c[n] + jx_s[n] = [\cos(\omega_0)x_c[n-1] - \sin(\omega_0)x_s[n-1]] + j[\sin(\omega_0)x_c[n-1] + \cos(\omega_0)x_s[n-1]] $$

Equating the real parts and the imaginary parts yields the coupled difference equations:

$$ x_c[n] = \cos(\omega_0)x_c[n-1] - \sin(\omega_0)x_s[n-1] $$

$$ x_s[n] = \sin(\omega_0)x_c[n-1] + \cos(\omega_0)x_s[n-1] $$

**Matrix Form:**
This can be elegantly written in matrix notation:

$$ \begin{bmatrix} x_c[n] \\ x_s[n] \end{bmatrix} = \begin{bmatrix} \cos(\omega_0) & -\sin(\omega_0) \\ \sin(\omega_0) & \cos(\omega_0) \end{bmatrix} \begin{bmatrix} x_c[n-1] \\ x_s[n-1] \end{bmatrix} $$

This matrix is the standard 2D Euclidean rotation matrix. Geometrically, the state vector is simply rotated by $\omega_0$ radians at every clock cycle in the complex plane. 

While this system is still marginally stable (BIBO marginally stable) and susceptible to round-off noise, the noise properties are more symmetric, and it provides both quadrature signals natively. It requires 4 real multiplications and 2 additions per sample, which is a manageable trade-off for the increased stability and functionality compared to the direct form.

### 4.5 Numerically Controlled Oscillator (NCO/DDS)

Because all recursive IIR oscillators eventually suffer from amplitude drift in finite-precision arithmetic, modern telecommunications and signal synthesis rely almost exclusively on the Numerically Controlled Oscillator (NCO), which forms the core of Direct Digital Synthesis (DDS).

The NCO entirely abandons the recursive IIR approach. Instead, it tracks the instantaneous phase of the waveform explicitly and maps that phase to an amplitude using a memory lookup. This guarantees unconditional stability because there is no feedback loop involving the amplitude.

**Core Architecture of an NCO:**

1. **Phase Accumulator:** An $N$-bit digital register that holds the current phase state $\theta[n]$. It acts as a digital integrator for frequency.
2. **Phase Increment (Tuning Word, $W$):** An $N$-bit unsigned integer that determines the frequency. It is added to the accumulator on every clock cycle.
3. **Phase-to-Amplitude Converter:** Typically a Read-Only Memory (ROM) Lookup Table (LUT) containing pre-computed sine and/or cosine values.

**Mathematical Model:**

At each rising edge of the system clock $f_{clk}$ (period $T_s = 1/f_{clk}$):

$$ \theta[n] = (\theta[n-1] + W) \pmod{2^N} $$

The phase $\theta[n]$ increments linearly. When the sum exceeds $2^N - 1$, the modulo arithmetic causes it to overflow naturally back to near zero. This exactly mimics the behavior of a physical phase angle wrapping from $2\pi$ back to $0$. The accumulator generates a perfect digital sawtooth wave representing the phase.

To find the true phase in radians:

$$ \Phi[n] = 2\pi \frac{\theta[n]}{2^N} $$

The frequency of the generated sinusoid is defined as the rate of change of phase. In discrete time, the phase changes by $W$ units every clock period $T_s$. The proportion of a full cycle completed per clock is $W / 2^N$.
Therefore, the absolute output frequency in Hertz is:

$$ f_{out} = \frac{W}{2^N} f_{clk} $$

**Frequency Resolution:**

The most powerful advantage of an NCO is its extreme frequency resolution. The smallest possible change in output frequency occurs when the tuning word $W$ is incremented by exactly 1:

$$ \Delta f = \frac{f_{clk}}{2^N} $$

By simply widening the accumulator (e.g., to $N = 32, 48$, or even $64$ bits), we can achieve micro-Hertz or nano-Hertz frequency resolution, far surpassing what is possible with analog PLLs, all while using a fixed master clock.

### 4.6 Phase Truncation and Dithering

While the phase accumulator can be very wide (e.g., $N=32$ bits), mapping a 32-bit phase to an amplitude requires a ROM LUT with $2^{32}$ entries. Assuming 16-bit amplitude resolution, this requires 8 Gigabytes of memory, which is completely unfeasible for on-chip cache or FPGA block RAM.
Therefore, we must **truncate** the phase word, using only the most significant $P$ bits (e.g., $P=12$) to address the LUT, while ignoring the remaining $K$ lower bits (where $N = P + K$).

**The Consequence of Phase Truncation:**

By dropping the lower $K$ bits, we introduce a phase error $\epsilon[n]$.

$$ \hat{\theta}[n] = \theta[n] - \epsilon[n] $$

Because the accumulator increases linearly, the truncated portion $\epsilon[n]$ forms a periodic sawtooth pattern. A periodic error in the time domain fundamentally transforms into concentrated, spurious tones (spurs) in the frequency domain. These spurs degrade the spectral purity of the oscillator.

The Spurious-Free Dynamic Range (SFDR) is the ratio (in dB) between the power of the desired fundamental frequency and the power of the strongest spurious tone. As a rule of thumb derived from the error energy, every bit of phase used to address the LUT provides approximately 6 dB of SFDR:

$$ SFDR \approx 6.02 \cdot P \text{ dB} $$

(Thus, a 12-bit LUT address yields an SFDR of ~72 dB. Note that this assumes the amplitude quantization in the LUT itself is not the limiting factor).

**Phase Dithering:**

To improve the SFDR without exponentially increasing the LUT size, we employ Phase Dithering. We add a small, pseudo-random noise sequence to the full $N$-bit phase word immediately before truncation.

$$ \theta_{dithered}[n] = \theta[n] + \text{noise}[n] $$

This randomness breaks up the periodic nature of the truncation error $\epsilon[n]$. In the frequency domain, the concentrated spurious tones are smeared out and transformed into broadband white noise. 

While the *total integrated noise power* remains exactly the same, the peak power of any single tone is drastically reduced. The noise floor rises slightly, but the prominent spurs are eliminated, greatly increasing the SFDR. This is a brilliant example of trading an undesirable deterministic error for a much more benign random error.

### 4.7 Chirp Generation

A chirp signal (used heavily in RADAR pulse compression and acoustic sonar) is a signal whose frequency increases or decreases linearly with time.

**Linear Frequency Modulation (LFM):**

The continuous-time phase of a chirp is the integral of its linear frequency. Let $f(t) = f_0 + kt$:

$$ \Phi(t) = 2\pi \int_0^t (f_0 + k\tau) d\tau = 2\pi \left( f_0 t + \frac{k}{2} t^2 \right) $$

Because the phase is a quadratic function of time, a simple NCO with a constant tuning word $W$ cannot generate it directly.

**Dual-Accumulator NCO Implementation:**

To generate a digital chirp, we make the tuning word $W$ time-dependent.

$$ W[n] = W_0 + k_{step} \cdot n $$

This requires a modified NCO architecture with two cascaded accumulators:

1. **Frequency Accumulator:** A register that holds the dynamic tuning word $W[n]$. On every clock cycle, a constant frequency step $k_{step}$ is added to it.
2. **Phase Accumulator:** The standard phase register $\theta[n]$. However, instead of adding a constant, it adds the dynamically changing $W[n]$ from the first accumulator.

The double integration perfectly yields the required quadratic phase, producing an impeccably linear digital chirp that sweeps smoothly across the spectrum.

---
## 5. COMPLETE PROOFS AND DERIVATIONS

**Derivation of SFDR Limit due to Phase Truncation:**

We wish to prove mathematically why phase truncation causes spurs and estimate their magnitude.

Let the true phase be $\Phi[n]$. The truncated phase is $\hat{\Phi}[n] = \Phi[n] - \epsilon[n]$, where $\epsilon[n]$ is the phase error sequence in radians.

The output of the perfect LUT is:

$$ y[n] = \cos(\hat{\Phi}[n]) = \cos(\Phi[n] - \epsilon[n]) $$

Using the trigonometric identity for the cosine of a difference:

$$ y[n] = \cos(\Phi[n])\cos(\epsilon[n]) + \sin(\Phi[n])\sin(\epsilon[n]) $$

Because the phase error is small (bounded by the truncation threshold $2\pi/2^P$), we can apply the small angle approximations: $\cos(\epsilon) \approx 1$ and $\sin(\epsilon) \approx \epsilon$.

$$ y[n] \approx \cos(\Phi[n]) \cdot 1 + \sin(\Phi[n]) \cdot \epsilon[n] $$

$$ y[n] = \cos(\Phi[n]) + \epsilon[n]\sin(\Phi[n]) $$

The output consists of the ideal desired carrier $\cos(\Phi[n])$ plus an error term $\epsilon[n]\sin(\Phi[n])$. This error term represents the carrier multiplied by (mixed with) the phase error sequence.

The phase error $\epsilon[n]$ is exactly the fractional part dropped during truncation. It forms a periodic sawtooth waveform bounded by the weight of the LSB of the truncated word, which is $2\pi/2^P$.

The peak error amplitude is $E_{max} = \frac{2\pi}{2^P}$.

When this periodic error mixes with the carrier, it generates sidebands (spurs). The power of the worst-case spur is directly related to the fundamental by the ratio of their amplitudes. In decibels, this ratio is approximately bounded by:

$$ 20 \log_{10}(2^P) = 20 \cdot P \cdot \log_{10}(2) \approx 20 \cdot P \cdot 0.301 = 6.02 \cdot P \text{ dB} $$

This elegantly proves that every bit of phase address yields ~6 dB of SFDR, providing a direct design rule for sizing ROMs in hardware synthesis.

---
## 6. WORKED EXAMPLES (MINIMUM 5 — fully solved)

### Example 1: Recursive Oscillator Design
**Problem statement:** 
Design a recursive digital oscillator to generate a 2 kHz sine wave at a sampling frequency of 10 kHz. Derive the exact difference equation and specify the necessary initial conditions to start the oscillation perfectly.

**Solution:**
1. Determine the normalized angular frequency $\omega_0$:
$$ \omega_0 = 2\pi \frac{f_{out}}{f_s} = 2\pi \frac{2000}{10000} = 2\pi (0.2) = 0.4\pi \text{ radians/sample} $$
2. Calculate the multiplier coefficient $a_1$:
$$ a_1 = 2\cos(\omega_0) = 2\cos(0.4\pi) $$
Evaluating $\cos(72^\circ) = 0.309016...$
$$ a_1 = 2 \times 0.3090169 = 0.6180339 $$
3. Write the standard difference equation:
$$ y[n] = 0.618034 y[n-1] - y[n-2] $$
4. Determine initial conditions to generate $y[n] = \sin(\omega_0 n)$:
We need $y[-1]$ and $y[-2]$.
$$ y[-1] = \sin(-\omega_0) = -\sin(0.4\pi) = -0.951056 $$
$$ y[-2] = \sin(-2\omega_0) = -\sin(0.8\pi) = -0.587785 $$

**Physical interpretation:** The system is an IIR filter. Providing it with the history of a sine wave (the initial conditions) injects exactly the right amount of energy and phase momentum to sustain the sine wave forever.

**Common mistakes to avoid:** Students often plug degrees into the cosine function instead of radians, resulting in drastically wrong coefficients. Always ensure calculators are in radian mode.

---

### Example 2: Amplitude Drift Calculation in Fixed Point
**Problem statement:** 
For the oscillator designed in Example 1, assume the coefficient $a_1$ must be implemented in a cheap microcontroller using only 3 fractional bits (Q3 format). Find the exact implemented coefficient, calculate the new pole locations, and determine the new frequency of oscillation.

**Solution:**
1. Exact coefficient calculated: $a_1 = 0.618034$.
2. To convert to Q3 format, multiply by $2^3 = 8$:
$$ 0.618034 \times 8 = 4.94427 $$
3. Round to the nearest integer:
$$ \text{Round}(4.94427) = 5 $$
4. The quantized coefficient in decimal is therefore:
$$ \hat{a}_1 = 5 / 8 = 0.625 $$
5. The implemented characteristic equation is:
$$ z^2 - 0.625z + 1 = 0 $$
6. Solve for the roots (poles):
$$ z_{1,2} = \frac{0.625 \pm \sqrt{0.625^2 - 4(1)(1)}}{2} $$
$$ z_{1,2} = \frac{0.625 \pm \sqrt{0.390625 - 4}}{2} $$
$$ z_{1,2} = \frac{0.625 \pm \sqrt{-3.609375}}{2} = 0.3125 \pm j 0.949917 $$
7. Verify magnitude:
$$ |z| = \sqrt{0.3125^2 + 0.949917^2} = \sqrt{0.097656 + 0.902343} = \sqrt{1.0} = 1 $$
The poles are strictly on the unit circle.
8. Calculate the new frequency. The angle of the pole is the new $\omega_{new}$:
$$ \omega_{new} = \arccos(0.3125) = 1.2532 \text{ radians/sample} $$
Converting back to Hz:
$$ f_{new} = \frac{1.2532}{2\pi} \times 10000 = 1994.5 \text{ Hz} $$

**Physical interpretation:** Coefficient quantization shifts the frequency from 2000 Hz to 1994.5 Hz. While the poles remain on the unit circle (ensuring it is still an oscillator), any roundoff errors during the multiplication $0.625 \cdot y[n-1]$ will cause the amplitude to drift unpredictably.

---

### Example 3: Coupled Oscillator Matrix Formulation
**Problem statement:** 
Derive the exact state matrix for generating a complex sinusoid at a frequency of 1.25 MHz with a sampling rate of 5 MHz. Show the first two iterations assuming initial conditions $x_c[0]=1, x_s[0]=0$.

**Solution:**
1. Determine the normalized frequency:
$$ \omega_0 = 2\pi \frac{1.25 \text{ MHz}}{5 \text{ MHz}} = 2\pi (0.25) = 0.5\pi = \frac{\pi}{2} $$
2. Calculate the matrix entries:
$$ \cos(\pi/2) = 0 $$
$$ \sin(\pi/2) = 1 $$
3. The state update rotation matrix is:
$$ \begin{bmatrix} x_c[n] \\ x_s[n] \end{bmatrix} = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} x_c[n-1] \\ x_s[n-1] \end{bmatrix} $$
4. Iteration 1 ($n=1$):
$$ \begin{bmatrix} x_c[1] \\ x_s[1] \end{bmatrix} = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} (0)(1) + (-1)(0) \\ (1)(1) + (0)(0) \end{bmatrix} = \begin{bmatrix} 0 \\ 1 \end{bmatrix} $$
5. Iteration 2 ($n=2$):
$$ \begin{bmatrix} x_c[2] \\ x_s[2] \end{bmatrix} = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} 0 \\ 1 \end{bmatrix} = \begin{bmatrix} -1 \\ 0 \end{bmatrix} $$

**Physical interpretation:** The state vector perfectly rotates by 90 degrees at each step. The sequence is $(1,0) \rightarrow (0,1) \rightarrow (-1,0) \rightarrow (0,-1)$, which perfectly represents samples of $\cos(\pi n / 2)$ and $\sin(\pi n / 2)$.

---

### Example 4: NCO Tuning Word and Frequency Resolution
**Problem statement:** 
A Direct Digital Synthesizer (DDS) features a 32-bit phase accumulator and is clocked by a highly stable $f_{clk} = 100 \text{ MHz}$ reference. 
a) Calculate the absolute frequency resolution of the synthesizer.
b) Calculate the exact integer tuning word $W$ required to generate an output frequency of 10.5 MHz.
c) Calculate the actual exact frequency generated by the NCO using this integer tuning word.

**Solution:**
a) Frequency resolution $\Delta f$:
$$ \Delta f = \frac{f_{clk}}{2^N} = \frac{100 \times 10^6}{2^{32}} = \frac{100,000,000}{4,294,967,296} \approx 0.023283 \text{ Hz} $$
This is an incredibly fine resolution of roughly 23 mHz!

b) Output frequency formula solved for $W$:
$$ f_{out} = \frac{W \cdot f_{clk}}{2^N} \implies W = \frac{f_{out} \cdot 2^N}{f_{clk}} $$
Substitute the values:
$$ W = \frac{10.5 \times 10^6 \cdot 4,294,967,296}{100 \times 10^6} $$
$$ W = 0.105 \times 4,294,967,296 = 450,971,566.08 $$
Since the tuning word must be an exact integer loaded into the digital register, we must round to the nearest whole number:
$$ W = 450,971,566 $$

c) The actual frequency generated by this integer word:
$$ f_{actual} = \frac{450,971,566 \cdot 100 \times 10^6}{4,294,967,296} $$
$$ f_{actual} = 10,499,999.998 \text{ Hz} $$

**Physical interpretation:** The difference between the desired 10.5 MHz and the actual frequency is a minuscule 0.002 Hz. This frequency error is negligible for almost all applications, demonstrating the massive power of the 32-bit NCO architecture.

**Common mistakes:** Forgetting that $W$ is strictly an integer. Leaving it as a float implies infinite precision, which physical hardware cannot achieve.

---

### Example 5: SFDR Estimation and Phase Truncation
**Problem statement:** 
An NCO architecture uses a massive 48-bit accumulator for extreme frequency resolution. However, the block RAM on the FPGA is limited, so the phase word is truncated to address a $1024 \times 16$-bit sine look-up table. Estimate the Spurious-Free Dynamic Range (SFDR) caused solely by phase truncation.

**Solution:**
1. Determine the phase address width $P$:
The LUT has 1024 entries. Therefore, the number of address bits $P$ is:
$$ P = \log_2(1024) = 10 \text{ bits} $$
2. The number of discarded phase bits $K$:
$$ K = N - P = 48 - 10 = 38 \text{ bits} $$
3. Apply the SFDR approximation formula:
$$ SFDR \approx 6.02 \cdot P \text{ dB} $$
$$ SFDR \approx 6.02 \times 10 = 60.2 \text{ dB} $$

**Physical interpretation:** The highest spurious tone caused by dropping the lower 38 bits of the phase will be roughly 60.2 dB below the main carrier signal power. This means the spur has roughly $1/1,000,000$ the power of the fundamental. If this is insufficient for a critical RF application, phase dithering must be employed, or a larger LUT must be used.

---
## 7. ENGINEERING APPLICATIONS AND CASE STUDIES

**Case Study 1: Software-Defined Radio (SDR) Up-Conversion**

In a modern 5G base station using FPGA-based SDR transmitters, baseband I/Q signals sampled at 1 MSPS must be upconverted to an intermediate frequency (IF) of 30 MHz before being fed to an RF DAC. The FPGA's digital signal processing slice runs at a clock rate of 120 MHz. The system employs an NCO to generate the 30 MHz local oscillator digitally. 

Using a 32-bit accumulator, the tuning word is precisely $W = (30/120) \times 2^{32} = (1/4) \times 2^{32} = 2^{30} = 1,073,741,824$. A digital complex mixer multiplies the baseband signals with the exact quadrature outputs of the NCO, producing perfectly continuous upconverted spectra with zero I/Q mismatch—a massive improvement over analog quadrature modulators.

**Case Study 2: Professional Digital Audio Synthesizers**

A high-end professional digital audio synthesizer keyboard uses DDS techniques to generate multiple polyphonic notes simultaneously. A standard digital audio clock of 48 kHz is used throughout the DSP pipeline. 

To generate the specific musical pitch of Middle C (261.6256 Hz), an NCO with a 24-bit accumulator computes $W = (261.6256 / 48000) \times 2^{24} = 91461.7 \approx 91462$. Because human hearing is extremely sensitive to harmonic distortion, phase dithering is employed heavily to ensure that all truncation spurs fall well below the 96 dB dynamic range of the 16-bit audio DACs, rendering the synthesis mathematically perfect to the human ear.

**Case Study 3: FMCW Automotive RADAR**

Self-driving cars rely on Frequency Modulated Continuous Wave (FMCW) RADAR to detect objects. This requires a chirp signal sweeping from 76 GHz to 77 GHz linearly over 1 millisecond. 

An NCO operating at a baseband frequency generates the digital chirp using dual accumulators (as derived in Section 4.7). The precise control of the $k_{step}$ variable guarantees perfect linearity of the sweep, which directly translates to accurate range resolution in the RADAR processing chain—an impossible feat with thermal-drift-prone analog VCOs.

---
## 8. COMMON STUDENT MISCONCEPTIONS AND ERRORS

1. **Misconception:** NCOs inherently output continuous analog voltage signals.
   **Correction:** An NCO is purely a digital state machine. It outputs a stream of binary numbers representing discrete samples of a waveform. A completely separate hardware component (the Digital-to-Analog Converter, or DAC) and an analog low-pass reconstruction filter are required to produce the continuous analog voltage.
2. **Misconception:** The frequency resolution of an NCO is determined by the size (number of entries) of the ROM/LUT.
   **Correction:** Frequency resolution is determined entirely by the width of the Phase Accumulator ($N$) and the clock frequency $f_{clk}$. The size of the LUT ($P$ bits) only affects the magnitude of phase truncation spurs and the resulting SFDR, not the fundamental frequency resolution.
3. **Misconception:** In a recursive IIR oscillator, quantizing the coefficients moves the poles inside the unit circle, causing the oscillation to immediately die out.
   **Correction:** It depends entirely on the specific quantized value. For the standard form $y[n] = a_1 y[n-1] - y[n-2]$, the $z^{-2}$ coefficient remains 1 exactly (if it is hardcoded). This forces the magnitude of the poles to remain exactly $|z|=1$, meaning the frequency shifts but marginal stability is retained. However, the subsequent round-off noise during the accumulation phase is what acts as a disturbance, causing amplitude drift.
4. **Misconception:** Phase dithering removes the noise from the system to improve the signal.
   **Correction:** Dithering actually *adds* artificial noise to the system. However, it converts coherent, deterministic spurious tones (which are highly objectionable and can interfere with specific frequency bands) into broad-band white noise. The total integrated noise power remains the same, but the peak power of any single spur is drastically reduced, thus significantly improving the Spurious-Free Dynamic Range (SFDR).
5. **Misconception:** A chirp NCO simply changes the tuning word inside a loop without requiring integration.
   **Correction:** A linear chirp requires a linearly increasing frequency. Because phase is mathematically the integral of frequency, a linearly increasing frequency requires a quadratic phase progression. Thus, two cascaded accumulators (one integrating frequency steps to form the tuning word, and the other integrating the tuning word to form the phase) are absolutely necessary.
6. **Misconception:** The direct form recursive oscillator is always inferior and never used.
   **Correction:** While NCOs are standard for frequency synthesis, the direct form oscillator is still highly relevant in extremely resource-constrained embedded systems where a large ROM table is unavailable, and the oscillation only needs to be maintained for short bursts (e.g., generating DTMF tones in legacy telephony).
7. **Misconception:** NCOs suffer from frequency drift as the chip heats up.
   **Correction:** The NCO's frequency is entirely deterministic and relies only on integer math. It will never drift. The only source of frequency instability is the physical quartz crystal oscillator driving the clock ($f_{clk}$).

---
## 9. CONNECTIONS TO OTHER LECTURES

**What this builds on:**
* **Lecture 6:** The Z-Transform, regions of convergence, and pole-zero analysis of discrete systems.
* **Lecture 12:** Fixed-point arithmetic, two's complement representation, and the modeling of quantization noise as an additive white noise source.
* **Lecture 18:** Digital filter design, specifically the structures of Infinite Impulse Response (IIR) filters and state-space matrix representations.

**Future dependencies (What future lectures depend on this):**
* **Lecture 28:** Digital Up/Down Conversion (DUC/DDC), where NCOs serve as the digital local oscillators for frequency translation.
* **Lecture 32:** Software Defined Radio (SDR) architectures, tying together ADCs, DACs, NCOs, and digital mixers into complete transceivers.

---
## 10. EXAMINATION QUESTIONS

### 10.1 Short Answer (5 questions with model answers)

**Q1:** Explain in detail why a simple direct-form recursive oscillator cannot sustain a stable, constant amplitude indefinitely when implemented in a standard fixed-point DSP processor.
*Model Answer:* At every time step, the output of the multiplier $a_1 \cdot y[n-1]$ has more bits than the register size and must be rounded. This round-off error acts as additive noise. Because the ideal oscillator has poles exactly on the unit circle, the system acts as an infinite-Q resonator. The quantization noise energy at the resonant frequency is integrated indefinitely, causing the amplitude to perform an unbounded random walk, eventually leading to overflow or decay.

**Q2:** Describe the fundamental mechanism of phase dithering in a Direct Digital Synthesizer (DDS).
*Model Answer:* Phase dithering involves adding a pseudo-random noise sequence to the LSBs of the phase accumulator output immediately before phase truncation. This breaks the periodic, deterministic pattern of the truncation error. In the frequency domain, it spreads the concentrated energy of spurious tones across the entire noise floor, thereby significantly improving the Spurious-Free Dynamic Range (SFDR).

**Q3:** Derive the transfer function $H(z)$ of the ideal digital sinusoidal oscillator starting from its difference equation.
*Model Answer:* Difference eq: $y[n] = 2\cos(\omega_0)y[n-1] - y[n-2] + x[n]$. 
Taking the Z-transform: $Y(z) = 2\cos(\omega_0)z^{-1}Y(z) - z^{-2}Y(z) + X(z)$. 
Grouping $Y(z)$: $Y(z)(1 - 2\cos(\omega_0)z^{-1} + z^{-2}) = X(z)$. 
Result: $H(z) = Y(z)/X(z) = \frac{1}{1 - 2\cos(\omega_0)z^{-1} + z^{-2}} = \frac{z^2}{z^2 - 2\cos(\omega_0)z + 1}$.

**Q4:** If an NCO system clock is strictly 50 MHz and the main phase accumulator is exactly 24 bits wide, calculate the absolute frequency resolution.
*Model Answer:* The frequency resolution is given by $\Delta f = f_{clk} / 2^N$. Therefore, $\Delta f = 50 \times 10^6 / 2^{24} = 50,000,000 / 16,777,216 \approx 2.9802$ Hz.

**Q5:** Why is the coupled oscillator matrix form preferred over the direct form in many digital communication applications (such as QAM)?
*Model Answer:* The coupled form elegantly provides both in-phase (cosine) and quadrature (sine) outputs simultaneously, which are perfectly orthogonal. Furthermore, it exhibits more symmetrical and stable round-off noise properties, and measuring the instantaneous amplitude for periodic renormalization is computationally simpler.

### 10.2 Long Answer / Numerical Problems (4 problems with complete solutions)

**Problem 1:** Design a recursive digital oscillator to generate a precise 1.5 kHz sine wave at an 8 kHz sampling rate. Give the exact difference equation. What is the location of the poles in polar form?
*Solution:* 
1. $\omega_0 = 2\pi(f/f_s) = 2\pi(1500/8000) = 0.375\pi = 1.1781$ radians/sample. 
2. Multiplier $a_1 = 2\cos(0.375\pi) = 2(0.38268) = 0.76536$. 
3. Difference equation: $y[n] = 0.76536y[n-1] - y[n-2]$. 
4. Pole locations: The poles are at $e^{\pm j\omega_0}$. Thus, in polar form, magnitude $r = 1$ and angle $\theta = \pm 0.375\pi$.

**Problem 2:** Rigorously prove that the coupled oscillator state matrix $\mathbf{A} = \begin{bmatrix} \cos(\omega_0) & -\sin(\omega_0) \\ \sin(\omega_0) & \cos(\omega_0) \end{bmatrix}$ yields poles strictly on the unit circle.
*Solution:* 
The poles of a state-space system are the eigenvalues of the state matrix $\mathbf{A}$.
We find the eigenvalues $\lambda$ by solving the characteristic equation $\det(\lambda \mathbf{I} - \mathbf{A}) = 0$.
$\det \begin{bmatrix} \lambda - \cos(\omega_0) & \sin(\omega_0) \\ -\sin(\omega_0) & \lambda - \cos(\omega_0) \end{bmatrix} = 0$.
$(\lambda - \cos(\omega_0))^2 - (-\sin(\omega_0))(\sin(\omega_0)) = 0$.
$(\lambda - \cos(\omega_0))^2 + \sin^2(\omega_0) = 0$.
$(\lambda - \cos(\omega_0))^2 = -\sin^2(\omega_0)$.
Taking the square root of both sides:
$\lambda - \cos(\omega_0) = \pm j\sin(\omega_0)$.
$\lambda = \cos(\omega_0) \pm j\sin(\omega_0) = e^{\pm j\omega_0}$.
The magnitude of the eigenvalues is $\sqrt{\cos^2(\omega_0) + \sin^2(\omega_0)} = 1$. Thus, poles are strictly on the unit circle.

**Problem 3:** Calculate the tuning word $W$ (in hexadecimal format) for an NCO with a 50 MHz clock, generating exactly a 5 MHz signal, using a 32-bit accumulator. Show all intermediate steps.
*Solution:* 
1. Tuning word formula: $W = (f_{out} / f_{clk}) \cdot 2^N$.
2. Substitute values: $W = (5 / 50) \cdot 2^{32} = 0.1 \cdot 4,294,967,296$.
3. Compute exact value: $W = 429,496,729.6$.
4. Round to nearest integer: $W = 429,496,730$.
5. Convert decimal to hexadecimal. $429496730 / 16 = 26843545$ remainder 10 (A).
Continuing division yields the hexadecimal value: $W = \text{0x1999999A}$.

**Problem 4:** A military RADAR NCO must achieve a Spurious-Free Dynamic Range (SFDR) of at least 80 dB to prevent false target detection. How many bits $P$ must be fed to the sine LUT? How many entries will the ROM require?
*Solution:* 
1. Use the SFDR approximation formula: $SFDR \approx 6.02 \cdot P$.
2. Set up inequality: $6.02 \cdot P \ge 80$.
3. Solve for $P$: $P \ge 80 / 6.02 = 13.289$.
4. Since $P$ must be an integer, round up to the next whole bit: $P = 14$ bits.
5. The number of entries in the ROM is $2^P = 2^{14} = 16,384$ entries.

### 10.3 True/False with Justification (6 items)

1. **False:** An NCO with a larger LUT has fundamentally better frequency resolution. 
   *(Justification: Frequency resolution relies entirely on the accumulator width $N$, not the LUT size. The LUT only affects phase truncation spurs).*

2. **True:** Dithering improves SFDR but strictly increases the total integrated noise floor power.
   *(Justification: Dithering adds actual random noise to the signal, raising the broadband noise floor while eliminating concentrated spurs).*

3. **True:** A recursive digital oscillator acts as an infinite-Q bandpass filter at its resonance frequency.
   *(Justification: Because the poles are on the unit circle, the damping factor is zero, giving an infinite Quality factor. Any noise at that frequency is integrated forever).*

4. **False:** Chirp signals are generated using a single phase accumulator with a constantly large tuning word. 
   *(Justification: A chirp requires a linearly sweeping tuning word, which mandates a second cascaded accumulator to integrate the frequency step).*

5. **False:** If coefficient quantization places poles slightly outside the unit circle, the result is a decaying amplitude. 
   *(Justification: Poles outside the unit circle ($|z| > 1$) result in exponentially growing amplitudes, leading to rapid overflow).*

6. **True:** The direct form IIR recursive oscillator only requires one real multiplication per output sample.
   *(Justification: The equation $y[n] = 2\cos(\omega_0)y[n-1] - y[n-2]$ has only one non-trivial coefficient, $2\cos(\omega_0)$, requiring a single multiplier).*

---
## 11. KEY FORMULAS REFERENCE

| Concept | Formula | Comprehensive Description |
| :--- | :--- | :--- |
| **Recursive Oscillator Diff. Eq.** | $y[n] = 2\cos(\omega_0)y[n-1] - y[n-2]$ | The fundamental second-order IIR difference equation for generating a sinusoid autonomously. |
| **Coupled Form (State Matrix)** | $\mathbf{x}[n] = \mathbf{R}(\omega_0) \mathbf{x}[n-1]$ | Quadrature generation where $\mathbf{R}$ is the 2D rotation matrix: $\begin{bmatrix} \cos\omega_0 & -\sin\omega_0 \\ \sin\omega_0 & \cos\omega_0 \end{bmatrix}$. |
| **Z-Domain Transfer Function** | $H(z) = \frac{z^2}{z^2 - 2\cos(\omega_0)z + 1}$ | The ideal continuous oscillator equivalent in the discrete Z-domain. |
| **Poles of the Oscillator** | $z_{1,2} = e^{\pm j\omega_0}$ | Exact location of the complex conjugate poles on the unit circle. |
| **NCO Phase Accumulator Update** | $\theta[n] = (\theta[n-1] + W) \pmod{2^N}$ | The core phase accumulator integer math using an $N$-bit register and tuning word $W$. |
| **NCO Exact Output Frequency** | $f_{out} = \frac{W \cdot f_{clk}}{2^N}$ | The exact mathematical relationship between the tuning word, clock, and generated frequency. |
| **NCO Frequency Resolution** | $\Delta f = \frac{f_{clk}}{2^N}$ | The smallest possible step in frequency (achieved when $W$ changes by exactly 1). |
| **SFDR Limit (Phase Truncation)** | $SFDR \approx 6.02 \cdot P$ dB | Spurious-free dynamic range given $P$ phase bits fed into the LUT address. |
| **Chirp Quadratic Phase** | $\Phi[n] = \omega_0 n + \frac{k_{step}}{2} n^2$ | The required quadratic phase progression for perfect linear frequency modulation. |

---
## 12. FURTHER READING AND REFERENCES

1. Proakis, J. G., & Manolakis, D. K. (2006). *Digital Signal Processing: Principles, Algorithms, and Applications* (4th Ed.). Pearson. Chapter 9 provides extensive coverage of IIR Filter implementation issues and limit cycles.
2. Oppenheim, A. V., & Schafer, R. W. (2009). *Discrete-Time Signal Processing* (3rd Ed.). Prentice Hall. Section 6.8 specifically addresses digital oscillators and their finite word-length effects.
3. Tierney, J., Rader, C. M., & Gold, B. (1971). "A Digital Frequency Synthesizer." *IEEE Transactions on Audio and Electroacoustics*, vol. 19, no. 1, pp. 48-57. (The seminal, original DDS invention paper).
4. Analog Devices MT-085 Tutorial: "Fundamentals of Direct Digital Synthesis (DDS)". An industry-standard practical guide to DDS architecture and phase truncation effects.
5. Haykin, S. (2001). *Communication Systems* (4th Ed.). Wiley. Excellent contextual reading for why phase continuous signals (like those from an NCO) are necessary in modern digital modulation schemes.
</Faculty Notes — Lecture 23: Digital Oscillators & NCO>
