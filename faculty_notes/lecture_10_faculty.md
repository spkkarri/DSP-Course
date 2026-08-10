<Faculty Notes — Lecture 10: FIR Filter Design — Window Method>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY

The window method is often the first FIR design technique introduced to undergraduate students. While it is highly intuitive—conceptually starting from an ideal filter and physically forcing it into reality—it is fundamentally sub-optimal compared to advanced numerical methods like the Parks-McClellan (Remez exchange) algorithm, which yields equiripple optimal designs.

However, we must teach the window method first precisely for its intuition. It provides a tangible bridge between the continuous/ideal mathematical world and discrete/practical engineering reality. It is crucial to emphasize that this method represents a mathematical compromise. The Gibbs phenomenon should be highlighted not just as a mathematical artifact of truncation, but as a fundamental limitation of Fourier series convergence at discontinuities. 

**Teaching Strategy:**
1. Begin with the concept of the ideal frequency response. Show the brick-wall behavior.
2. Mathematically derive the ideal impulse response. Ensure students see the limits of integration.
3. Prove its unrealizability. Specifically point out that it is infinite in both directions (non-causal).
4. Introduce truncation and demonstrate the resulting Gibbs ringing visually. 
5. Explain how tapering the edges (windowing) mitigates this ringing, but at the cost of a wider transition band. 
6. Emphasize that the window method is an analytical approach, not an optimization approach. The coefficients are computed via formula, not iterative refinement.

**Suggested Demos:**
* Use MATLAB/Python to show the time-domain and frequency-domain effects of abrupt truncation vs. a Hamming window.
* Demonstrate the Gibbs phenomenon by plotting the frequency response for $M = 21, 51, 101$. Show that while the ripples get "squished" near the cutoff edge, the 9% overshoot amplitude never vanishes.
* Use audio files (like a drum beat) to demonstrate phase distortion. Pass it through an IIR filter vs. an FIR linear-phase filter and let students hear the "smearing" of the transient.

**Common Student Difficulties:**
* Students often forget to apply the shift $(M-1)/2$. Remind them that without the shift, the filter remains non-causal.
* Confusion between filter length $M$ and filter order $N = M-1$. Always clarify which one is being used in formulas.
* Misunderstanding the difference between phase delay and group delay.

---
## 1. LEARNING OBJECTIVES

By the end of this comprehensive lecture, students will be able to:
1. **Derive** the ideal impulse response $h_d[n]$ for a lowpass filter using the Inverse Discrete-Time Fourier Transform (IDTFT) directly from the frequency domain definition.
2. **Explain** the origins, mathematical properties, and physical implications of the Gibbs phenomenon in the context of filter design.
3. **Analyze** the strict trade-offs between mainlobe width (transition bandwidth) and peak sidelobe level (stopband attenuation) across different window functions (Rectangular, Bartlett, Hanning, Hamming, Blackman, Kaiser).
4. **Design** a causal, strictly linear-phase FIR filter from given specifications ($\omega_p, \omega_s, A_s$) by selecting the appropriate window function and determining the exact filter length $M$.
5. **Prove** mathematically that a symmetric or antisymmetric FIR filter impulse response guarantees strictly linear phase and constant group delay.
6. **Apply** spectral transformation techniques to derive Highpass, Bandpass, and Bandstop filters from a prototype Lowpass filter.
7. **Evaluate** the hardware complexity (number of delay elements, multipliers, adders) required to implement the designed FIR filters.
8. **Interpret** the practical impact of linear phase in specific engineering systems, such as biomedical signal analysis and audio reproduction.

---
## 2. PREREQUISITE KNOWLEDGE REVIEW

Before embarking on FIR filter design, students must be extremely comfortable with the following foundational concepts from prior lectures:

**1. Discrete-Time Fourier Transform (DTFT):**
The DTFT relates a discrete-time sequence $x[n]$ to its continuous frequency spectrum $X(e^{j\omega})$.
The synthesis and analysis equations are:
$$ X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n} $$
$$ x[n] = rac{1}{2\pi} \int_{-\pi}^{\pi} X(e^{j\omega}) e^{j\omega n} d\omega $$
(Ensure students know how to integrate complex exponentials.)

**2. Convolution in Time = Multiplication in Frequency:**
If $y[n] = x[n] * h[n]$, then $Y(e^{j\omega}) = X(e^{j\omega})H(e^{j\omega})$.
Conversely, multiplication in time equals circular convolution in frequency. This is the bedrock of the window method:
If $h[n] = h_d[n] \cdot w[n]$, then:
$$ H(e^{j\omega}) = rac{1}{2\pi} \int_{-\pi}^{\pi} H_d(e^{j	heta}) W(e^{j(\omega-	heta)}) d	heta $$
This convolution in the frequency domain is what causes the "smearing" (transition band) and ripples (sidelobes).

**3. Concept of Causality and Stability:**
A system is causal if the output depends only on present and past inputs. For an impulse response, this requires:
$$ h[n] = 0 	ext{ for all } n < 0 $$
A system is BIBO stable if its impulse response is absolutely summable:
$$ \sum_{n=-\infty}^{\infty} |h[n]| < \infty $$
FIR filters are inherently stable because they have a finite number of finite-valued coefficients.

**4. Linear Phase and Group Delay:**
Phase response: $\phi(\omega) = ngle H(e^{j\omega})$
Phase delay is defined as:
$$ 	au_p(\omega) = -rac{\phi(\omega)}{\omega} $$
Group delay is defined as the negative derivative of the phase:
$$ 	au_g(\omega) = -rac{d\phi(\omega)}{d\omega} $$
Strictly linear phase implies that $\phi(\omega) = -c\omega$ for some constant $c$. Consequently, the group delay $	au_g(\omega) = c$ is constant for all frequencies. This means all frequency components are delayed by the exact same amount of time, preserving the waveform shape.

---
## 3. HISTORICAL AND MOTIVATIONAL CONTEXT

The mathematical foundations of this topic date back to Joseph Fourier (1822) and the study of Fourier series. However, the specific artifact of ringing at discontinuities was formalized by J. Willard Gibbs in 1899. Albert Michelson, who built an early mechanical harmonic analyzer, noticed ringing when synthesizing square waves. He wrote to Gibbs, who mathematically proved that when synthesizing a discontinuous function (like an ideal brick-wall filter) using a finite number of sinusoidal basis functions, an overshoot always occurs at the discontinuity.

In the realm of Electrical and Electronics Engineering (EEE), FIR filters are indispensable. While analog circuits naturally yield IIR (Infinite Impulse Response) filters with non-linear phase, digital systems allow for FIR filters which can have strictly linear phase. 

**Why does EEE need this?** 
1. **Digital Communications:** In data transmission, symbols are transmitted as pulses. If the channel or the receiver filter has non-linear phase, different frequency components of the pulse travel at different speeds. This causes the pulse to spread out in time and bleed into adjacent symbol slots, causing Intersymbol Interference (ISI). This heavily degrades the Bit Error Rate (BER).
2. **Audio Processing:** In high-fidelity audio, phase distortion smears transients (e.g., drum hits or guitar plucks), reducing clarity and punch. Linear-phase FIR filters prevent this.
3. **Biomedical Engineering:** When filtering an Electrocardiogram (ECG), non-linear phase can distort the shape of the QRS complex. Since doctors diagnose heart conditions based on the exact shape and timing of these waves, phase distortion could lead to fatal misdiagnoses. FIR filters designed via the window method provide a straightforward way to achieve the required linear phase characteristics while controlling the frequency magnitude response.

---
## 4. THEORETICAL FOUNDATIONS

### 4.1 The Ideal Lowpass Filter
An ideal Lowpass Filter (LPF) completely passes frequencies up to a cutoff $\omega_c$ and completely attenuates frequencies above it. Its frequency response is defined over one period $[-\pi, \pi]$ as:
$$
H_d(e^{j\omega}) = 
egin{cases} 
1, & |\omega| \le \omega_c \ 
0, & \omega_c < |\omega| \le \pi 
\end{cases}
$$

To find the time-domain representation, we apply the IDTFT. We must show every single step:
$$
h_d[n] = rac{1}{2\pi} \int_{-\pi}^{\pi} H_d(e^{j\omega}) e^{j\omega n} d\omega
$$
Since $H_d(e^{j\omega})$ is zero outside $[-\omega_c, \omega_c]$, we change the limits of integration:
$$
h_d[n] = rac{1}{2\pi} \int_{-\omega_c}^{\omega_c} 1 \cdot e^{j\omega n} d\omega
$$
Now, integrate $e^{j\omega n}$ with respect to $\omega$:
$$
h_d[n] = rac{1}{2\pi} \left[ rac{e^{j\omega n}}{jn} ight]_{-\omega_c}^{\omega_c}
$$
Evaluate at the upper and lower limits:
$$
h_d[n] = rac{1}{2\pi j n} (e^{j\omega_c n} - e^{-j\omega_c n})
$$
Using Euler's identity $\sin(	heta) = rac{e^{j	heta} - e^{-j	heta}}{2j}$, we can multiply the numerator and denominator by 2:
$$
h_d[n] = rac{1}{\pi n} \left( rac{e^{j\omega_c n} - e^{-j\omega_c n}}{2j} ight)
$$
$$
h_d[n] = rac{\sin(\omega_c n)}{\pi n} \quad 	ext{for } n 
eq 0
$$
For $n = 0$, we cannot divide by zero. We can either use L'Hôpital's rule on the result, or integrate directly from the start:
$$
h_d[0] = rac{1}{2\pi} \int_{-\omega_c}^{\omega_c} 1 \cdot e^{0} d\omega = rac{1}{2\pi} [\omega]_{-\omega_c}^{\omega_c} = rac{2\omega_c}{2\pi} = rac{\omega_c}{\pi}
$$

**Physical interpretation:** 
The ideal filter requires an infinite number of samples extending from $n = -\infty$ to $n = \infty$. 
It is non-causal because it requires future knowledge (samples for $n < 0$). 
It is technically unstable because the sinc function is not absolutely summable (the sum of $|h_d[n]|$ diverges). 
Therefore, the ideal LPF cannot be built in reality. It serves purely as a mathematical target.

### 4.2 The Gibbs Phenomenon and Truncation
To make the filter practical, we must truncate $h_d[n]$ to a finite number of terms $N$. Simple truncation is mathematically equivalent to multiplying $h_d[n]$ by a rectangular window.
$$ w_{rect}[n] = 1 	ext{ for } -M/2 \le n \le M/2, 	ext{ else } 0 $$
In the frequency domain, this is the convolution of the ideal brick-wall response $H_d(e^{j\omega})$ with the Fourier transform of the rectangular window (the Dirichlet kernel).
Because the Dirichlet kernel has significant side-lobes, this convolution produces ripples in the passband and stopband of the resulting filter. 
As the number of terms $M$ increases, the main lobe of the Dirichlet kernel gets narrower. This causes the ripples in the frequency response to get compressed closer to the cutoff frequency $\omega_c$. 
However, the area under the sidelobes remains constant. Thus, the peak amplitude of the overshoot remains constant at approximately 9% (or 0.0895) of the step size, regardless of how large $M$ gets. This is the **Gibbs Phenomenon**.

### 4.3 The Windowing Operation
To reduce Gibbs ringing, we must smooth out the abrupt truncation. We multiply the ideal impulse response by a window function $w[n]$ that smoothly tapers to zero at its boundaries.
Furthermore, to ensure causality, we must shift the entire impulse response to the right by half the window length. Let $M$ be the total number of taps. The delay is:
$$ lpha = rac{M-1}{2} $$
The final causal FIR filter coefficients are computed as:
$$
h[n] = h_d\left[n - lphaight] \cdot w[n], \quad 0 \le n \le M-1
$$
This shift ensures that the filter starts at $n=0$ and ends at $n=M-1$, making it fully causal and realizable in hardware or software.

### 4.4 Standard Window Specifications
Here are the complete mathematical definitions and specifications for standard windows of length $M$. (Note: $N = M-1$ is the filter order).

**1. Rectangular Window:**
$$ w[n] = 1, \quad 0 \le n \le M-1 $$
* Peak Sidelobe Level: -13 dB
* Mainlobe Width: $4\pi/M$
* Transition Bandwidth: $0.9\pi/M$
* Characteristics: Sharpest transition, but terrible stopband attenuation. Rarely used in practice.

**2. Bartlett (Triangular) Window:**
$$ w[n] = egin{cases} rac{2n}{M-1}, & 0 \le n \le rac{M-1}{2} \ 2 - rac{2n}{M-1}, & rac{M-1}{2} < n \le M-1 \end{cases} $$
(Can also be written as $1 - rac{|2n - (M-1)|}{M-1}$)
* Peak Sidelobe Level: -27 dB
* Mainlobe Width: $8\pi/M$
* Characteristics: Simple linear taper. Better than rectangular but inferior to raised-cosine windows.

**3. Hanning (Hann) Window:**
$$ w[n] = 0.5 - 0.5\cos\left(rac{2\pi n}{M-1}ight), \quad 0 \le n \le M-1 $$
* Peak Sidelobe Level: -32 dB (Note: often taught as -31dB or -32dB depending on textbook)
* Mainlobe Width: $8\pi/M$
* Transition Bandwidth: $3.1\pi/M$
* Characteristics: Smooth to zero at the edges. Good general-purpose window.

**4. Hamming Window:**
$$ w[n] = 0.54 - 0.46\cos\left(rac{2\pi n}{M-1}ight), \quad 0 \le n \le M-1 $$
* Peak Sidelobe Level: -41 dB
* Mainlobe Width: $8\pi/M$
* Transition Bandwidth: $3.3\pi/M$
* Characteristics: The coefficients (0.54, 0.46) were specifically optimized by Richard Hamming to cancel the first sidelobe of the Hanning window. It does not go to zero at the edges.

**5. Blackman Window:**
$$ w[n] = 0.42 - 0.5\cos\left(rac{2\pi n}{M-1}ight) + 0.08\cos\left(rac{4\pi n}{M-1}ight), \quad 0 \le n \le M-1 $$
* Peak Sidelobe Level: -57 dB (Sometimes cited as -74 dB in asymptotic texts, but the practical first sidelobe is -57dB)
* Mainlobe Width: $12\pi/M$
* Transition Bandwidth: $5.5\pi/M$
* Characteristics: Adds a second harmonic cosine term. Excellent stopband attenuation, but wide transition band.

### 4.5 The Kaiser Window
Unlike the fixed windows above, the Kaiser window is tunable. It uses the zeroth-order modified Bessel function of the first kind $I_0(\cdot)$ and a tuning parameter $eta$ to control the trade-off between mainlobe width and sidelobe level.

$$
w[n] = rac{I_0\left(eta \sqrt{1 - \left(rac{n - lpha}{lpha}ight)^2}ight)}{I_0(eta)}, \quad 0 \le n \le M-1
$$
where $lpha = rac{M-1}{2}$.
The Bessel function $I_0(x)$ is defined by the power series:
$$ I_0(x) = 1 + \sum_{k=1}^{\infty} \left[ rac{(x/2)^k}{k!} ight]^2 $$

**Design Equations for Kaiser:**
Given a desired Stopband Attenuation $A_s$ (in positive dB) and a transition width $\Delta\omega = \omega_s - \omega_p$:
1. Determine the shape parameter $eta$:
   $$
   eta = 
   egin{cases} 
   0.1102(A_s - 8.7), & A_s > 50 \ 
   0.5842(A_s - 21)^{0.4} + 0.07886(A_s - 21), & 21 \le A_s \le 50 \ 
   0.0, & A_s < 21 
   \end{cases}
   $$
2. Determine the minimum Filter Length $M$:
   $$
   M \ge rac{A_s - 7.95}{2.285 \Delta\omega} + 1
   $$
This allows exact, optimal satisfaction of filter specifications without over-designing.

---
## 5. COMPLETE PROOFS AND DERIVATIONS

### Proof: Symmetry Implies Strictly Linear Phase
**Theorem:** An FIR filter of length $M$ with a symmetric impulse response $h[n] = h[M-1-n]$ exhibits strictly linear phase.

**Proof:**
Let the transfer function be evaluated on the unit circle to find the frequency response:
$$
H(e^{j\omega}) = \sum_{n=0}^{M-1} h[n] e^{-j\omega n}
$$
Factor out the exponential delay corresponding to the exact midpoint of the filter, $lpha = rac{M-1}{2}$:
$$
H(e^{j\omega}) = e^{-j\omega lpha} \sum_{n=0}^{M-1} h[n] e^{-j\omega (n - lpha)}
$$
Let's make a change of variables to shift the origin to the center. Let $k = n - lpha$. 
When $n = 0$, $k = -lpha$. 
When $n = M-1$, $k = (M-1) - lpha = 2lpha - lpha = lpha$.
So the summation limits become $k = -lpha$ to $lpha$:
$$
H(e^{j\omega}) = e^{-j\omega lpha} \sum_{k=-lpha}^{lpha} h[k + lpha] e^{-j\omega k}
$$
Because of the symmetry condition $h[n] = h[M-1-n]$, let's substitute $n = k+lpha$:
$$ h[k+lpha] = h[M-1-(k+lpha)] $$
Recall that $lpha = rac{M-1}{2}$, which implies $M-1 = 2lpha$. Substituting this in:
$$ h[k+lpha] = h[2lpha - k - lpha] = h[lpha - k] = h[-k + lpha] $$
This means the shifted sequence $h[k+lpha]$ is perfectly even (symmetric) with respect to $k=0$.

We can now expand the summation by isolating the $k=0$ term and pairing the positive and negative $k$ terms:
$$
\sum_{k=-lpha}^{lpha} h[k+lpha] e^{-j\omega k} = h[lpha] + \sum_{k=1}^{lpha} \left( h[k+lpha]e^{-j\omega k} + h[-k+lpha]e^{j\omega k} ight)
$$
Since we proved $h[k+lpha] = h[-k+lpha]$, we can factor it out:
$$
\sum_{k=-lpha}^{lpha} h[k+lpha] e^{-j\omega k} = h[lpha] + \sum_{k=1}^{lpha} h[k+lpha] \left( e^{-j\omega k} + e^{j\omega k} ight)
$$
Using Euler's identity $e^{j	heta} + e^{-j	heta} = 2\cos(	heta)$:
$$
\sum_{k=-lpha}^{lpha} h[k+lpha] e^{-j\omega k} = h[lpha] + \sum_{k=1}^{lpha} 2 h[k+lpha] \cos(\omega k)
$$
Notice that this entire summation term consists only of real coefficients multiplying cosine functions, which are purely real. There are no imaginary $j$ terms left. Let's define this entire real-valued expression as the amplitude function $A(\omega)$:
$$
A(\omega) = h[lpha] + \sum_{k=1}^{lpha} 2 h[k+lpha] \cos(\omega k)
$$
Therefore, the total frequency response can be written as:
$$
H(e^{j\omega}) = A(\omega) e^{-j\omega lpha}
$$
The phase response is the angle of this complex quantity:
$$
ngle H(e^{j\omega}) = -lpha \omega \quad 	ext{(plus } \pi 	ext{ if } A(\omega) < 0 	ext{)}
$$
The phase is a strictly linear function of frequency $\omega$ (with a slope of $-lpha$). 
The group delay is the negative derivative of the phase:
$$
	au_g = -rac{d}{d\omega}(-lpha \omega) = lpha = rac{M-1}{2}
$$
This mathematically proves that impulse response symmetry guarantees exactly constant group delay, which is the definition of strictly linear phase. $lacksquare$

---
## 6. WORKED EXAMPLES (MINIMUM 5 — fully solved)

### Example 1: Basic Lowpass Filter Design (Hamming Window)
**Problem statement:** 
Design a causal FIR lowpass filter to meet the following specifications:
Passband edge frequency: $\omega_p = 0.4\pi$ rad/sample
Stopband edge frequency: $\omega_s = 0.6\pi$ rad/sample
Minimum stopband attenuation: $A_s = 40$ dB
Use the appropriate fixed window. Determine the filter length $M$, the delay $lpha$, and write the expression for the impulse response $h[n]$. Evaluate $h[0]$ and the center tap.

**Solution:**
1. **Choose the Window:**
   The required stopband attenuation is $A_s = 40$ dB. 
   Rectangular (-13dB) and Hanning (-32dB) are insufficient. 
   The Hamming window provides -41 dB, which satisfies the $A_s \ge 40$ dB requirement.
2. **Determine Filter Length $M$:**
   Transition bandwidth $\Delta\omega = \omega_s - \omega_p = 0.6\pi - 0.4\pi = 0.2\pi$.
   For a Hamming window, the design rule relates mainlobe width to transition band as:
   $$ \Delta\omega = rac{3.3\pi}{M} \implies M = rac{3.3\pi}{0.2\pi} = 16.5 $$
   However, using the more conservative full mainlobe width equation: $rac{8\pi}{M} \le \Delta\omega \implies M \ge rac{8\pi}{0.2\pi} = 40$.
   We choose to design a Type I filter, so we need an odd integer. Let's choose $M = 41$.
   The delay is $lpha = (41-1)/2 = 20$ samples.
3. **Determine Ideal Cutoff Frequency:**
   The cutoff frequency is placed precisely in the middle of the transition band:
   $$ \omega_c = rac{\omega_p + \omega_s}{2} = rac{0.4\pi + 0.6\pi}{2} = 0.5\pi $$
4. **Compute Ideal Shifted Impulse Response:**
   $$ h_d[n-20] = rac{\sin(0.5\pi(n-20))}{\pi(n-20)} \quad 	ext{for } n 
eq 20 $$
   At the center, $n=20$:
   $$ h_d[0] = rac{\omega_c}{\pi} = 0.5 $$
5. **Compute Window Function:**
   $$ w[n] = 0.54 - 0.46\cos\left(rac{2\pi n}{40}ight), \quad 0 \le n \le 40 $$
6. **Final Filter Coefficients Equation:**
   $$ h[n] = rac{\sin(0.5\pi(n-20))}{\pi(n-20)} \left[ 0.54 - 0.46\cos\left(rac{2\pi n}{40}ight) ight] $$
7. **Evaluate Specific Taps:**
   Center tap $h[20]$:
   $$ w[20] = 0.54 - 0.46\cos(\pi) = 0.54 - 0.46(-1) = 1.0 $$
   $$ h[20] = h_d[0] \cdot w[20] = 0.5 \cdot 1.0 = 0.5 $$
   Edge tap $h[0]$:
   $$ h_d[-20] = rac{\sin(0.5\pi(-20))}{\pi(-20)} = rac{\sin(-10\pi)}{-20\pi} = 0 $$
   $$ w[0] = 0.54 - 0.46\cos(0) = 0.08 $$
   $$ h[0] = 0 \cdot 0.08 = 0 $$

**Physical interpretation:** The filter delays the signal by exactly 20 samples. Frequencies above half the Nyquist rate are attenuated by at least 41 dB.

---

### Example 2: Comparing Hamming vs Blackman for Given Specifications
**Problem statement:** 
For a desired transition bandwidth of $\Delta\omega = 0.05\pi$, compare the required filter lengths when using a Hamming window versus a Blackman window. Discuss the engineering trade-offs.

**Solution:**
1. **Hamming Window Length Calculation:**
   Using the conservative design rule $M = rac{8\pi}{\Delta\omega}$:
   $$ M_{Hamming} \ge rac{8\pi}{0.05\pi} = rac{8}{0.05} = 160 $$
   Rounding to the next odd integer: $M = 161$.
   Stopband attenuation achieved: ~41 dB.
   Group delay: $	au_g = 160 / 2 = 80$ samples.
2. **Blackman Window Length Calculation:**
   Using the design rule $M = rac{12\pi}{\Delta\omega}$:
   $$ M_{Blackman} \ge rac{12\pi}{0.05\pi} = rac{12}{0.05} = 240 $$
   Rounding to the next odd integer: $M = 241$.
   Stopband attenuation achieved: ~57 dB.
   Group delay: $	au_g = 240 / 2 = 120$ samples.

**Physical interpretation and Trade-offs:** 
To get better stopband attenuation (improving from 41 dB to 57 dB), the Blackman window requires a significantly longer filter (241 taps vs 161 taps) to achieve the exact same transition sharpness. 
* **Computational Cost:** Implementing the Blackman filter requires 241 MAC (Multiply-Accumulate) operations per input sample, compared to 161 for the Hamming filter. This consumes more power and processing time.
* **Latency:** The Blackman filter introduces a group delay of 120 samples versus 80 samples. If the sampling rate is 44.1 kHz, 120 samples is about 2.7 ms of delay. In some real-time feedback control systems, this extra delay could destabilize the system.

---

### Example 3: Optimal Kaiser Window Design
**Problem statement:**
Design a lowpass filter with transition bandwidth $\Delta\omega = 0.1\pi$ and an extremely strict stopband attenuation requirement of $A_s = 80$ dB. Find the optimal Kaiser window parameters $eta$ and $M$.

**Solution:**
1. **Determine the Shape Parameter $eta$:**
   Since $A_s = 80 > 50$, we use the first condition of the empirical Kaiser formula:
   $$ eta = 0.1102(A_s - 8.7) $$
   $$ eta = 0.1102(80 - 8.7) $$
   $$ eta = 0.1102(71.3) $$
   $$ eta = 7.857 $$
2. **Determine Filter Length $M$:**
   Using the empirical length formula for Kaiser windows:
   $$ M \ge rac{A_s - 7.95}{2.285 \Delta\omega} + 1 $$
   Substitute the given values:
   $$ M \ge rac{80 - 7.95}{2.285 (0.1\pi)} + 1 $$
   $$ M \ge rac{72.05}{2.285 	imes 0.314159} + 1 $$
   $$ M \ge rac{72.05}{0.7178} + 1 $$
   $$ M \ge 100.37 + 1 = 101.37 $$
   Rounding up to the nearest odd integer to maintain Type I linear phase symmetry, we set $M = 103$.
3. **Write the Kaiser Window Equation:**
   The required delay is $lpha = rac{103-1}{2} = 51$.
   $$ w[n] = rac{I_0\left(7.857 \sqrt{1 - \left(rac{n - 51}{51}ight)^2}ight)}{I_0(7.857)}, \quad 0 \le n \le 102 $$

**Physical interpretation:** The Kaiser window provides a mathematically optimal parameterization. If we used a fixed window, we would have to guess or use an overly large window. Blackman only gives -57 dB. The exact required parameters ($eta=7.857, M=103$) allow us to precisely hit -80 dB without wasting computational resources on unnecessary filter taps.

---

### Example 4: Highpass Filter Design via Spectral Transformation
**Problem statement:**
Design an 11-tap Highpass Filter (HPF) with cutoff $\omega_c = 0.6\pi$ using a Rectangular window. Use the time-domain spectral transformation method rather than integrating the HPF frequency response directly. Compute $h[5]$ and $h[6]$.

**Solution:**
1. **Ideal LPF to HPF Transformation Concept:**
   An ideal HPF can be formed by subtracting an ideal LPF from an all-pass filter. An all-pass filter passes all frequencies with gain 1, and its impulse response is the unit impulse $\delta[n]$.
   $$ H_{HPF}(e^{j\omega}) = 1 - H_{LPF}(e^{j\omega}) $$
   Taking the IDTFT, we get the time domain relationship:
   $$ h_{d, HPF}[n] = \delta[n] - h_{d, LPF}[n] $$
2. **Shift for Causality:**
   For length $M=11$, the delay is $lpha = (11-1)/2 = 5$.
   We must shift the ideal impulse response:
   $$ h_{d, HPF}[n-5] = \delta[n-5] - rac{\sin(0.6\pi(n-5))}{\pi(n-5)} $$
3. **Apply Rectangular Window:**
   The rectangular window $w[n] = 1$ for $0 \le n \le 10$.
   So the final causal FIR coefficients are simply the truncated shifted ideal response.
   For any $n 
eq 5$:
   $$ h[n] = -rac{\sin(0.6\pi(n-5))}{\pi(n-5)} $$
   For the center tap $n = 5$:
   $$ h[5] = 1 - rac{0.6\pi}{\pi} = 1 - 0.6 = 0.4 $$
4. **Evaluate $h[6]$:**
   $$ h[6] = -rac{\sin(0.6\pi(1))}{\pi(1)} = -rac{\sin(0.6\pi)}{\pi} = -rac{0.951}{\pi} pprox -0.3027 $$

**Physical interpretation:** The filter operates by passing the original delayed signal (represented by the impulse $\delta[n-5]$) and subtracting the low-frequency components (the LPF part), leaving only the high-frequency components intact. 

---

### Example 5: Effect of Window Length on the Frequency Response
**Problem statement:**
Evaluate the quantitative effect of changing the window length from $M=11$ to $M=51$ for a Hamming-windowed LPF with $\omega_c = 0.5\pi$. What happens to the transition bandwidth, the peak sidelobe level, and the group delay?

**Solution:**
1. **Analysis for $M=11$:**
   Transition bandwidth formula for Hamming: $\Delta\omega pprox rac{3.3\pi}{M}$.
   $$ \Delta\omega pprox rac{3.3\pi}{11} = 0.3\pi $$
   Peak sidelobe level remains mathematically fixed by the Hamming shape at -41 dB.
   Group delay is $	au_g = (11-1)/2 = 5$ samples.
2. **Analysis for $M=51$:**
   Transition bandwidth: 
   $$ \Delta\omega pprox rac{3.3\pi}{51} = 0.0647\pi $$
   Peak sidelobe level remains strictly at -41 dB.
   Group delay is $	au_g = (51-1)/2 = 25$ samples.

**Physical interpretation:** Increasing the window length $M$ from 11 to 51 drastically sharpens the filter, narrowing the transition band from a wide $0.3\pi$ to a very steep $0.0647\pi$. This makes it closer to a true brick-wall filter. However, it does *not* improve the stopband attenuation at all (it remains stuck at -41 dB). Furthermore, it heavily penalizes latency, increasing the signal delay from 5 samples to 25 samples. 

---
## 7. ENGINEERING APPLICATIONS AND CASE STUDIES

**1. Anti-Aliasing Filters in ADCs (Sigma-Delta Architecture):**
Before analog-to-digital conversion, continuous signals must be strictly bandlimited to half the Nyquist rate to prevent aliasing. While a simple analog IIR filter is used at the front end, modern architectures (like Sigma-Delta ADCs) vastly oversample the signal, apply a very sharp, high-order digital FIR lowpass filter, and then downsample (decimate) to the desired rate. The strict linear phase of the FIR filter ensures that the time-domain waveform of the sampled signal is fundamentally undistorted, which is highly critical for accurate instrumentation and measurement.

**2. Audio Graphic Equalizers in High-Fidelity Systems:**
In digital audio processing, a graphic equalizer breaks the audio spectrum into multiple distinct frequency bands, allowing the user to boost or cut specific frequencies. Doing this with IIR filters distorts the phase relationship between the fundamental frequency and the harmonics of a musical note. FIR filters designed via windowing provide exact linear phase across all bands. This prevents the "smearing" of percussive transients (like a snare drum hit or a piano hammer strike), maintaining the tight, punchy sound of the original recording.

**3. ECG Baseline Wander Removal in Biomedical Devices:**
Electrocardiogram (ECG) signals often suffer from low-frequency baseline wander (drifting up and down) due to patient respiration and patient movement. A linear-phase FIR highpass filter (with a very low cutoff, e.g., 0.5 Hz) is used to remove this wander. If a standard IIR filter (like a Butterworth or Chebyshev) were used, the non-linear phase response at low frequencies would warp and distort the shape of the Q-wave, R-wave, and S-wave (the QRS complex). Since cardiologists diagnose ischemic heart conditions based on the exact morphological shape and timing of these waves, IIR phase distortion could lead to fatal misdiagnoses. The constant group delay of FIR filters preserves the exact morphological shape of the heartbeat.

---
## 8. COMMON STUDENT MISCONCEPTIONS AND ERRORS

1. **Misconception:** "Increasing the window length $M$ will continuously improve the stopband attenuation, making the filter better."
   **Correction:** This is the most common error. Increasing $M$ *only* narrows the transition band, making the filter sharper. However, the peak sidelobe level (which dictates stopband attenuation) is entirely determined by the mathematical *shape* of the window (e.g., Hamming vs Blackman), not its length. A length-1000 Hamming window still only has -41 dB of stopband attenuation, just like a length-11 Hamming window.
   
2. **Misconception:** "Linear phase is exactly the same concept as zero phase."
   **Correction:** Zero phase literally means $ngle H(e^{j\omega}) = 0$ everywhere across all frequencies, implying absolutely zero delay. This is physically impossible for real-time (causal) filters, as it requires the impulse response to be centered at $n=0$ with data extending into the future. Causal linear phase filters have a phase of $-lpha \omega$, meaning they impart a strictly constant group delay of $lpha$ samples to all frequencies.

3. **Misconception:** "The Gibbs phenomenon can be completely eliminated by just using a large enough $N$."
   **Correction:** The Gibbs phenomenon (the ~9% overshoot at the cutoff edge) is a permanent, indestructible mathematical artifact of Fourier series convergence at a discontinuity. As $N 	o \infty$, the width of the ripple gets infinitely thin and moves infinitely close to the cutoff frequency, but its peak amplitude never vanishes.

4. **Misconception:** "A Type II FIR filter (even length, symmetric) is perfectly fine for designing a Highpass filter."
   **Correction:** By evaluating the transfer function of any Type II filter at the Nyquist frequency $\omega = \pi$ ($z=-1$), it can be algebraically proven that it always has a zero at Nyquist ($H(e^{j\pi}) = 0$). Therefore, it absolutely cannot pass high frequencies and is useless for Highpass or Bandstop designs.

5. **Misconception:** "The window method provides the optimal FIR filter for a given order."
   **Correction:** The window method is fundamentally analytical and intuitive, but completely sub-optimal. Advanced optimization algorithms, like the Parks-McClellan (Remez Exchange) algorithm, distribute the error evenly across the passband and stopband (equiripple). Parks-McClellan yields filters that meet the exact same specifications with a significantly lower filter order $N$ than the window method.

6. **Misconception:** "The ideal highpass impulse response is just the ideal lowpass impulse response inverted."
   **Correction:** Simply negating the lowpass response $-h_{LPF}[n]$ creates a filter that flips the sign of the low frequencies, it doesn't pass the high frequencies. The correct transformation is $\delta[n] - h_{LPF}[n]$, which subtracts the low frequencies from the original all-pass signal.

---
## 9. CONNECTIONS TO OTHER LECTURES

* **Builds upon:** 
  * **Lecture 3:** Properties of the DTFT, specifically the convolution-in-time and multiplication-in-frequency properties.
  * **Lecture 5:** Z-Transform and System Stability. (Confirming that FIR filters are inherently stable because all poles are at $z=0$).
  * **Lecture 8:** Digital Filter Structures (Direct Form, Cascade Form). Students should visualize the tapped delay line required to implement the $M$ taps they just calculated.
* **Prerequisite for:** 
  * **Lecture 12:** Optimal FIR Design (Parks-McClellan Algorithm) – this future lecture directly highlights and solves the numerical shortcomings and sub-optimality of the window method.
  * **Lecture 15:** Multirate Signal Processing (Decimation and Interpolation) – which heavily rely on extremely sharp, strictly linear-phase FIR filters to prevent aliasing during rate conversion.

---
## 10. EXAMINATION QUESTIONS

### 10.1 Short Answer (5 questions with model answers)
**Q1: Why is a delay of $lpha = rac{M-1}{2}$ explicitly added to the ideal impulse response during window method design?**
*Answer:* The original ideal impulse response $h_d[n]$ is symmetrically centered around $n=0$ and extends backwards to time $t = -\infty$. Adding the delay shifts the entire center of the impulse response to the right. When combined with truncation by the finite window, this delay ensures that all filter coefficients $h[n] = 0$ for $n < 0$. This makes the system mathematically causal and physically realizable in hardware.

**Q2: Which standard window type offers the sharpest transition band, and what is the severe engineering trade-off?**
*Answer:* The Rectangular window offers the sharpest possible transition band (mainlobe width of $4\pi/M$). The severe trade-off is that it yields the worst stopband attenuation (a peak sidelobe level of only -13 dB) due to massive, unmitigated Gibbs ringing.

**Q3: State the exact mathematical condition required for a causal FIR filter to exhibit strictly linear phase.**
*Answer:* The filter's impulse response must be either completely symmetric ($h[n] = h[M-1-n]$) or completely antisymmetric ($h[n] = -h[M-1-n]$).

**Q4: Define the Group Delay of a linear phase FIR filter of length $M$, and explain its physical significance.**
*Answer:* The group delay is $	au_g = rac{M-1}{2}$ samples. Its physical significance is that every single frequency component passing through the filter experiences this exact same constant time delay. This preserves the time-domain waveform shape and prevents phase distortion or smearing.

**Q5: Why is the Kaiser window highly preferred over the Hamming or Blackman windows in professional engineering practice?**
*Answer:* Fixed windows (like Hamming and Blackman) offer rigid, discrete choices for stopband attenuation (-41 dB or -57 dB). If an engineer needs exactly 48 dB, Blackman is overkill and wastes processing power, while Hamming fails. The Kaiser window provides a continuous tuning parameter $eta$ that allows the designer to exactly trade off transition bandwidth against stopband attenuation, optimizing hardware usage.

### 10.2 Long Answer / Numerical Problems 
**Problem 1:** 
Design a Bandpass FIR filter using a Hanning window with the following specifications:
Lower cutoff frequency: $\omega_{c1} = 0.3\pi$
Upper cutoff frequency: $\omega_{c2} = 0.7\pi$
Total filter length: $M = 9$
Show all calculation steps.
*Solution Steps:*
1. Calculate the required delay shift: $lpha = (9-1)/2 = 4$.
2. Write the analytical ideal BPF impulse response. It is the subtraction of two LPFs:
   $h_d[n-4] = rac{\sin(0.7\pi(n-4))}{\pi(n-4)} - rac{\sin(0.3\pi(n-4))}{\pi(n-4)}$ for $n 
eq 4$.
   For the center tap $n=4$, apply L'Hôpital's rule:
   $h_d[0] = rac{0.7\pi - 0.3\pi}{\pi} = 0.4$.
3. Compute the discrete Hanning window values:
   $w[n] = 0.5 - 0.5\cos\left(rac{2\pi n}{8}ight)$ for integer values $n=0$ to $8$.
4. Multiply term by term to find final 9 coefficients: $h[n] = h_d[n-4] \cdot w[n]$.
   For instance, at $n=4$: $w[4] = 0.5 - 0.5(-1) = 1.0$. So $h[4] = 0.4 	imes 1.0 = 0.4$.
   At $n=0$: $w[0] = 0$. So $h[0] = 0$.

**Problem 2:** 
An FIR lowpass filter is required to have a narrow transition band of $0.02\pi$ and a stopband attenuation of at least $50$ dB. Choose an appropriate standard window (excluding Kaiser) and determine the exact required filter order $N$.
*Solution:*
1. Evaluate $50$ dB requirement against standard windows: Rectangular(-13), Hanning(-32), and Hamming(-41) all fail. Blackman(-57) successfully meets the criterion.
2. Select Blackman window. The Blackman mainlobe width equation is: $\Delta\omega \ge rac{12\pi}{M}$.
3. Solve for $M$: $M \ge rac{12\pi}{0.02\pi} = 600$.
4. Filter length must be an odd integer for Type I, so $M = 601$.
5. The filter order $N$ is defined as $M - 1$. Therefore, $N = 601 - 1 = 600$.

**Problem 3:** 
Using the time-domain spectral transformation method, analytically derive the ideal impulse response for a Bandstop filter (which rejects frequencies from $\omega_{c1}$ to $\omega_{c2}$) in terms of the ideal Lowpass filter response.
*Solution:*
An ideal Bandstop filter passes low frequencies (up to $\omega_{c1}$) and high frequencies (above $\omega_{c2}$). Conceptually, it can be constructed by summing a lowpass filter and a highpass filter:
$H_{BSF}(e^{j\omega}) = H_{LPF,\omega_{c1}}(e^{j\omega}) + H_{HPF,\omega_{c2}}(e^{j\omega})$
Since an ideal highpass filter is an all-pass minus a lowpass, $H_{HPF,\omega_{c2}} = 1 - H_{LPF,\omega_{c2}}$.
Substitute this into the equation:
$H_{BSF} = 1 - H_{LPF,\omega_{c2}} + H_{LPF,\omega_{c1}}$
Apply the IDTFT to convert back to the time domain:
$h_{d,BSF}[n] = \delta[n] - rac{\sin(\omega_{c2} n)}{\pi n} + rac{\sin(\omega_{c1} n)}{\pi n}$

**Problem 4:**
A causal FIR filter has the following finite impulse response: $h[0]=1, h[1]=2, h[2]=3, h[3]=2, h[4]=1$. Prove mathematically that this specific filter has strictly linear phase, and compute its group delay.
*Solution:*
1. Observe the length $M=5$. The sequence is perfectly symmetric: $h[n] = h[4-n]$.
2. Write the DTFT:
   $H(e^{j\omega}) = 1 + 2e^{-j\omega} + 3e^{-j2\omega} + 2e^{-j3\omega} + e^{-j4\omega}$
3. Factor out the center delay term $e^{-j2\omega}$:
   $H(e^{j\omega}) = e^{-j2\omega} (e^{j2\omega} + 2e^{j\omega} + 3 + 2e^{-j\omega} + e^{-j2\omega})$
4. Group the complex conjugate pairs:
   $H(e^{j\omega}) = e^{-j2\omega} [ 3 + 2(e^{j\omega} + e^{-j\omega}) + (e^{j2\omega} + e^{-j2\omega}) ]$
5. Apply Euler's formula $e^{j	heta} + e^{-j	heta} = 2\cos(	heta)$:
   $H(e^{j\omega}) = e^{-j2\omega} [ 3 + 4\cos(\omega) + 2\cos(2\omega) ]$
6. The bracketed term is purely real (no imaginary $j$ components). Therefore, the phase is entirely determined by the $e^{-j2\omega}$ term, which is exactly $-2\omega$. 
7. Group delay is the negative derivative: $	au_g = -rac{d}{d\omega}(-2\omega) = 2$ samples.

### 10.3 True/False with Justification
1. **T/F:** A Type II FIR filter can be effectively used to design an ideal highpass filter.
   *False.* Type II filters (which have an even length and symmetric coefficients) intrinsically possess a zero at $\omega = \pi$. This strictly prevents them from passing high frequencies.
2. **T/F:** The Gibbs phenomenon overshoot disappears completely if we make the filter length $M$ infinitely large.
   *False.* As $M$ increases, the width of the ripple approaches zero, but the peak amplitude of the overshoot remains mathematically fixed at approximately 9%.
3. **T/F:** A rectangular window has the narrowest mainlobe width of all standard classical windows.
   *True.* Its mainlobe width is $4\pi/M$, which provides the sharpest transition band possible, though severely at the cost of poor stopband attenuation.
4. **T/F:** IIR filters can easily achieve strict linear phase if designed properly.
   *False.* IIR filters absolutely cannot achieve strict linear phase if they are required to be both stable and causal. Only FIR filters possess this capability.
5. **T/F:** The group delay of a linear phase FIR filter of length 15 is exactly 7 samples.
   *True.* Group delay is given by $lpha = (M-1)/2 = (15-1)/2 = 7$ samples.
6. **T/F:** The Kaiser window uses Bessel functions primarily to adjust the filter length.
   *False.* The Bessel function parameter $eta$ adjusts the continuous trade-off between mainlobe width and sidelobe level. The total filter length $M$ is calculated via a completely separate algebraic equation based on the transition width requirement.

---
## 11. KEY FORMULAS REFERENCE

This table serves as a comprehensive reference for all mathematical formulas required for this topic.

| Description | Formula |
| :--- | :--- |
| **DTFT Analysis** | $X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n}$ |
| **IDTFT Synthesis** | $x[n] = rac{1}{2\pi} \int_{-\pi}^{\pi} X(e^{j\omega}) e^{j\omega n} d\omega$ |
| **Ideal LPF Impulse Response** | $h_d[n] = rac{\sin(\omega_c n)}{\pi n}$ |
| **Ideal HPF Impulse Response** | $h_d[n] = \delta[n] - rac{\sin(\omega_c n)}{\pi n}$ |
| **Linear Phase Symmetry** | $h[n] = h[M-1-n]$ |
| **Linear Phase Antisymmetry** | $h[n] = -h[M-1-n]$ |
| **Group Delay** | $	au_g = lpha = rac{M-1}{2}$ |
| **Final Windowed Coefficients** | $h[n] = h_d[n - lpha] \cdot w[n]$ |
| **Rectangular Window** | $w[n] = 1$ |
| **Bartlett Window** | $w[n] = 1 - rac{\|2n - (M-1)\|}{M-1}$ |
| **Hanning Window** | $w[n] = 0.5 - 0.5\cos(rac{2\pi n}{M-1})$ |
| **Hamming Window** | $w[n] = 0.54 - 0.46\cos(rac{2\pi n}{M-1})$ |
| **Blackman Window** | $w[n] = 0.42 - 0.5\cos(rac{2\pi n}{M-1}) + 0.08\cos(rac{4\pi n}{M-1})$ |
| **Kaiser Window Equation** | $w[n] = rac{I_0\left(eta \sqrt{1 - \left(rac{n - lpha}{lpha}ight)^2}ight)}{I_0(eta)}$ |
| **Kaiser Parameter $eta$ (for $A_s > 50$)**| $eta = 0.1102(A_s - 8.7)$ |
| **Kaiser Length Formula** | $M \ge rac{A_s - 7.95}{2.285 \Delta\omega} + 1$ |

---
## 12. FURTHER READING AND REFERENCES

For deeper dives into the numerical analysis and mathematical proofs omitted here, students and faculty are encouraged to consult the following foundational texts:

1. Proakis, J. G., & Manolakis, D. G. (2006). *Digital Signal Processing: Principles, Algorithms, and Applications* (4th ed.). Pearson. (Specifically Chapter 10: FIR Filter Design, which covers the window method in extensive detail).
2. Oppenheim, A. V., & Schafer, R. W. (2010). *Discrete-Time Signal Processing* (3rd ed.). Pearson. (Chapter 7: Filter Design Techniques, widely considered the most mathematically rigorous treatment of the subject).
3. Haykin, S., & Van Veen, B. (2002). *Signals and Systems* (2nd ed.). Wiley. (Good for reviewing the foundational Fourier Series concepts and Gibbs phenomenon).
4. Rabiner, L. R., & Gold, B. (1975). *Theory and Application of Digital Signal Processing*. Prentice-Hall. (A classic, historical text detailing the original engineering applications of these filters).
5. Hamming, R. W. (1989). *Digital Filters* (3rd ed.). Dover Publications. (Written by the inventor of the Hamming window, offering unique insights into the philosophy of filter design).
