<Faculty Notes — Lecture 4: Frequency Response & Group Delay>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---

## PREFACE FOR FACULTY
This lecture is a critical bridge in the Digital Signal Processing curriculum. It transitions students from the abstract mathematical concept of the Discrete-Time Fourier Transform (DTFT) to the practical engineering domain of filter design and frequency-selective signal processing. 

The eigenfunction concept is crucial here. If a student does not understand why complex exponentials are eigenfunctions of LTI systems, they will struggle with everything that follows in filter design, including spectral analysis, Fourier Series, and the Fast Fourier Transform (FFT). 

Many students confuse phase delay and group delay. The standard textbook definitions (minus phase divided by frequency vs. negative derivative of phase) are mathematically straightforward but physically opaque. Use the narrowband envelope analogy carefully. Show them visually how a carrier wave shifts (phase delay) versus how the envelope or "packet" of energy shifts (group delay). 

When introducing these concepts, emphasize that we are dealing with systems that are Linear and Time-Invariant. Non-linear systems do not possess these eigenfunctions, and time-varying systems will shift frequencies (creating new frequency components).

**Suggested Demos:** 
1. **MATLAB/Python Live Script:** Show a sum of two sinusoids (e.g., 100 Hz and 1000 Hz) passing through a filter with non-linear phase. Show the input waveform and output waveform in the time domain. The distortion in the time domain will be obvious to the students, even if the magnitude response is flat.
2. **Audio Demo:** Pass a sharp percussion sound (broadband, containing many frequencies) through an all-pass filter with severe group delay distortion. The sound will become "smeared" or "chirped" (like a laser sound), demonstrating that even if the magnitude response is perfectly flat, phase deeply affects the time-domain waveform.
3. **Phasor Animation:** An animated GIF showing phasors at different frequencies rotating and being scaled/shifted by $H(e^{j\omega})$.

---

## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Derive** the eigenfunction property of Linear Time-Invariant (LTI) systems for complex exponential inputs, demonstrating rigorous mathematical steps.
2. **Calculate** the frequency response (magnitude and phase) for arbitrary discrete-time LTI systems given their impulse response or linear constant-coefficient difference equation.
3. **Differentiate** between phase delay and group delay mathematically and conceptually, utilizing the narrowband signal approximation.
4. **Evaluate** the group delay of given systems, applying first-order Taylor series approximations for narrowband signal analysis and finding the exact group delay using analytical differentiation.
5. **Prove** rigorously that a symmetric or anti-symmetric Finite Impulse Response (FIR) filter exhibits exactly linear (or generalized linear) phase and constant group delay.
6. **Interpret** pole-zero plots geometrically in the complex Z-plane to sketch the magnitude and phase responses without relying on computational tools.
7. **Analyze** why ideal frequency-selective filters (LPF, HPF, BPF, BSF) are physically unrealizable and non-causal due to their infinite and two-sided impulse responses.
8. **Solve** engineering design problems involving group delay requirements for distortionless transmission in digital communication systems.

---

## 2. PREREQUISITE KNOWLEDGE REVIEW

Before embarking on this lecture, ensure students are comfortable with the following prior concepts:

### A. The Discrete-Time Fourier Transform (DTFT)
Students must recall the definition of the DTFT for a discrete-time sequence $x[n]$:
$$
X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n}
$$
And the inverse DTFT:
$$
x[n] = \frac{1}{2\pi} \int_{-\pi}^{\pi} X(e^{j\omega}) e^{j\omega n} d\omega
$$
They should remember that the DTFT is continuous and periodic in $\omega$ with period $2\pi$.

### B. Convolution Sum
The fundamental input-output relationship for a discrete-time LTI system with impulse response $h[n]$:
$$
y[n] = x[n] * h[n] = \sum_{k=-\infty}^{\infty} h[k] x[n-k] = \sum_{k=-\infty}^{\infty} x[k] h[n-k]
$$

### C. Z-Transform and System Function
The relation between the Z-transform of the impulse response and the system function:
$$
H(z) = \sum_{n=-\infty}^{\infty} h[n] z^{-n}
$$
Poles (values of $z$ where $H(z) \rightarrow \infty$) and zeros (values of $z$ where $H(z) = 0$). 
The frequency response is the system function evaluated strictly on the unit circle (Region of Convergence must include $|z|=1$ for stable systems):
$$
H(e^{j\omega}) = H(z) \Big|_{z = e^{j\omega}}
$$

### D. Complex Arithmetic and Euler's Formula
Euler's fundamental relation linking trigonometry and complex exponentials:
$$
e^{j\theta} = \cos(\theta) + j\sin(\theta)
$$
Magnitude and phase representation of a complex number $z = x + jy$:
$$
|z| = \sqrt{x^2 + y^2}, \quad \angle z = \arctan\left(\frac{y}{x}\right)
$$
Conversion between rectangular and polar forms is essential for computing magnitude and phase responses.

---

## 3. HISTORICAL AND MOTIVATIONAL CONTEXT

**Historical Context:**
The concepts of frequency response and graphical representations (like Bode plots) were formalized in the 1930s by Hendrik Wade Bode at Bell Labs. Bode was working on the stability of feedback amplifiers for long-distance telephone networks across the United States. The necessity to understand how magnitude and phase behaved across different frequencies was paramount for preventing amplifier oscillations.
The concept of group delay was deeply explored later as communication systems moved to higher bandwidths. When transmitting radar pulses during World War II or digital data packets in early modems, engineers noticed that waveforms arrived smeared over time. This smearing was traced back to the non-linear phase of transmission lines, waveguides, and analog filters. The mathematical formalization of group delay allowed engineers to quantify and compensate for this dispersion.

**Why does an EEE student need this?**
Electrical and Electronics Engineers deal with signals constantly—whether it's audio, video, sensor data, telecommunications, or power grid frequencies. 
1. **Digital Communications:** In 4G/5G networks, Wi-Fi, and fiber optics, non-constant group delay causes Intersymbol Interference (ISI). A delayed high-frequency component of one pulse might bleed into the time slot of the next pulse, scrambling the digital data (1s and 0s become unreadable).
2. **Audio Engineering:** When designing a crossover network for loudspeakers, non-linear phase will cause destructive interference between the woofer and tweeter exactly at the crossover frequency, creating a "hole" in the sound.
3. **Biomedical Engineering:** When filtering an ECG signal to remove 50/60 Hz powerline noise, a filter with severe phase distortion can alter the shape of the QRS complex, potentially leading a cardiologist to misdiagnose a heart condition.
4. **Radar Systems:** Radar relies on the exact timing of returned pulses to measure distance. If the receiver filters have significant group delay distortion, the pulse timing becomes ambiguous, degrading range resolution.

---

## 4. THEORETICAL FOUNDATIONS

### 4.1 Eigenfunction Property of LTI Systems

An **eigenfunction** of a linear operator or system is a function that, when passed through the system, emerges as the same function, modified only by a scalar constant multiplier (the eigenvalue).
For Linear Time-Invariant (LTI) systems, eternal complex exponentials of the form $x[n] = e^{j\omega n}$ are the unique eigenfunctions.

**Complete Mathematical Treatment:**
Let the input sequence be a complex exponential:
$$
x[n] = e^{j\omega n}, \quad -\infty < n < \infty
$$
The output $y[n]$ of the LTI system is given precisely by the convolution sum:
$$
y[n] = \sum_{k=-\infty}^{\infty} h[k] x[n-k]
$$
Substitute the input sequence into the convolution formula:
$$
y[n] = \sum_{k=-\infty}^{\infty} h[k] e^{j\omega (n-k)}
$$
Using the basic algebraic properties of exponents ($a^{b-c} = a^b a^{-c}$):
$$
y[n] = \sum_{k=-\infty}^{\infty} h[k] e^{j\omega n} e^{-j\omega k}
$$
Notice that the term $e^{j\omega n}$ does not depend on the summation index $k$. Because the system is linear, we can factor this term completely out of the infinite sum:
$$
y[n] = e^{j\omega n} \left( \sum_{k=-\infty}^{\infty} h[k] e^{-j\omega k} \right)
$$
Look closely at the term in the parentheses. For a specific chosen frequency $\omega$, the sum $\sum h[k] e^{-j\omega k}$ evaluates to a single complex number. We define this complex constant as the frequency response $H(e^{j\omega})$:
$$
H(e^{j\omega}) = \sum_{k=-\infty}^{\infty} h[k] e^{-j\omega k}
$$
Thus, the final output equation is elegantly simple:
$$
y[n] = H(e^{j\omega}) e^{j\omega n}
$$
This rigorous derivation proves unequivocally that the complex exponential is an eigenfunction, and $H(e^{j\omega})$ is the corresponding complex eigenvalue. 

**Physical Intuition:** A pure, eternal sine wave fed into a linear, time-invariant system will ALWAYS exit as a pure sine wave of the exact same frequency. Only its amplitude may be scaled up or down, and its phase may be shifted. The system absolutely cannot create new frequencies.

### 4.2 Frequency Response $H(e^{j\omega})$

The frequency response $H(e^{j\omega})$ is generally a continuous complex-valued function of the real variable $\omega$. Since it is evaluated on the unit circle $z = e^{j\omega}$, it is always periodic with a period of $2\pi$.

It can be expressed in polar form:
$$
H(e^{j\omega}) = |H(e^{j\omega})| e^{j \theta(\omega)}
$$
Where:
- $|H(e^{j\omega})|$ is the **Magnitude Response** (or gain). It dictates how much a particular frequency is amplified or attenuated.
- $\theta(\omega) = \angle H(e^{j\omega})$ is the **Phase Response**. It dictates how much a particular frequency is shifted in time.

By Euler's formula, if the input is a real cosine wave:
$$
x[n] = A \cos(\omega_0 n + \phi) = \frac{A}{2} e^{j(\omega_0 n + \phi)} + \frac{A}{2} e^{-j(\omega_0 n + \phi)}
$$
Because the system is linear and real (assuming the impulse response $h[n]$ is real-valued), the system possesses conjugate symmetry: $H(e^{-j\omega_0}) = H^*(e^{j\omega_0})$. The output becomes:
$$
y[n] = \frac{A}{2} H(e^{j\omega_0}) e^{j(\omega_0 n + \phi)} + \frac{A}{2} H^*(e^{j\omega_0}) e^{-j(\omega_0 n + \phi)}
$$
Letting $H(e^{j\omega_0}) = |H|e^{j\theta}$:
$$
y[n] = \frac{A|H|}{2} e^{j(\omega_0 n + \phi + \theta)} + \frac{A|H|}{2} e^{-j(\omega_0 n + \phi + \theta)}
$$
$$
y[n] = A |H(e^{j\omega_0})| \cos(\omega_0 n + \phi + \theta(\omega_0))
$$

### 4.3 Phase Delay $\tau_p(\omega)$

Phase delay is the effective time delay experienced by a pure sinusoidal carrier wave at a specific frequency $\omega$.
The phase shift $\theta(\omega)$ can be mathematically interpreted as a time shift in the time domain. 
Consider a cosine wave that has been delayed by $\tau_p$ samples:
$$
y[n] = \cos(\omega (n - \tau_p)) = \cos(\omega n - \omega \tau_p)
$$
We equate the phase term from our frequency response derivation with this delayed term:
$$
-\omega \tau_p = \theta(\omega)
$$
Solving for $\tau_p$:
$$
\tau_p(\omega) = -\frac{\theta(\omega)}{\omega}
$$
**Physical Intuition:** It tells us how many samples a steady-state continuous sine wave is shifted to the right. However, since a pure, eternal sine wave carries zero information (it looks identically the same everywhere from $t=-\infty$ to $t=\infty$), phase delay is often less meaningful for communication signals than group delay. 

### 4.4 Group Delay $\tau_g(\omega)$

Group delay represents the time delay of the **envelope** of a signal, or the time it takes for a "group" of frequencies or a wave packet (which carries the actual information) to travel through the system.
$$
\tau_g(\omega) = -\frac{d\theta(\omega)}{d\omega}
$$

**Derivation from narrowband signal envelope delay:**
Consider a narrowband signal centered around a high-frequency carrier $\omega_c$:
$$
X(e^{j\omega}) \approx 0 \text{ for } |\omega - \omega_c| > \Delta\omega
$$
In the close vicinity of $\omega_c$, we can approximate the system's phase response $\theta(\omega)$ using a first-order Taylor series expansion:
$$
\theta(\omega) \approx \theta(\omega_c) + \frac{d\theta(\omega)}{d\omega}\bigg|_{\omega=\omega_c} (\omega - \omega_c)
$$
Let us define our two delay metrics at the carrier frequency:
$$
\tau_g = -\frac{d\theta(\omega)}{d\omega}\bigg|_{\omega=\omega_c}, \quad \tau_p = -\frac{\theta(\omega_c)}{\omega_c}
$$
Substituting these back into the Taylor expansion gives:
$$
\theta(\omega) \approx -\omega_c \tau_p - \tau_g (\omega - \omega_c)
$$
The output spectrum $Y(e^{j\omega})$ is the input spectrum multiplied by the frequency response:
$$
Y(e^{j\omega}) = X(e^{j\omega}) |H(e^{j\omega})| e^{j\theta(\omega)}
$$
Assuming the magnitude response is relatively flat across this narrow band ($|H(e^{j\omega})| \approx G$):
$$
Y(e^{j\omega}) \approx G \cdot X(e^{j\omega}) e^{j(-\omega_c \tau_p - \tau_g (\omega - \omega_c))}
$$
Taking the inverse DTFT:
$$
y[n] \approx G \cdot s[n - \tau_g] \cos(\omega_c (n - \tau_p))
$$
Where $s[n]$ is the low-frequency envelope modulating the carrier.
**Physical Intuition:** The envelope (the pulse shape, the data bits) is delayed exactly by $\tau_g$, while the rapid oscillations inside the envelope are delayed by $\tau_p$. If $\tau_g$ is not constant across the entire bandwidth of a wideband signal, different parts of the spectrum travel at different speeds, causing **dispersion**. The pulse spreads out, gets distorted, and causes ISI.

### 4.5 Linear Phase Systems

A system possesses **Linear Phase** if its phase response is a strictly linear function of frequency passing through the origin:
$$
\theta(\omega) = -\alpha \omega
$$
In this case, let us evaluate the delays:
- Phase Delay: $\tau_p(\omega) = -\frac{-\alpha \omega}{\omega} = \alpha$
- Group Delay: $\tau_g(\omega) = -\frac{d}{d\omega}(-\alpha \omega) = \alpha$
Both delays are constant and equal to $\alpha$ for all frequencies. A signal passing through a linear phase system will have all its frequency components delayed by the exact same amount in time. Because every harmonic component maintains its relative time alignment, the signal shape is perfectly preserved in the time domain (no phase distortion).

### 4.6 Computing Frequency Response from Poles/Zeros

The rational Z-transform of a system is given by:
$$
H(z) = G \frac{\prod_{k=1}^{M} (1 - z_k z^{-1})}{\prod_{k=1}^{N} (1 - p_k z^{-1})}
$$
To find the continuous frequency response, we restrict our evaluation to the unit circle by setting $z = e^{j\omega}$:
$$
H(e^{j\omega}) = G \frac{\prod_{k=1}^{M} (1 - z_k e^{-j\omega})}{\prod_{k=1}^{N} (1 - p_k e^{-j\omega})} = G \frac{\prod_{k=1}^{M} (e^{j\omega} - z_k) e^{-j\omega M}}{\prod_{k=1}^{N} (e^{j\omega} - p_k) e^{-j\omega N}}
$$
Geometrically, the term $(e^{j\omega} - z_k)$ represents a vector in the complex Z-plane pointing from the zero location $z_k$ to the current frequency point $e^{j\omega}$ on the unit circle. 
- **Magnitude:** The overall magnitude $|H(e^{j\omega})|$ is proportional to the product of the lengths of all vectors from the zeros, divided by the product of the lengths of all vectors from the poles.
- **Phase:** The overall phase is the sum of the angles of the zero vectors minus the sum of the angles of the pole vectors (plus a linear phase term from the delay $e^{-j\omega(M-N)}$).
**Physical Intuition:** As $\omega$ sweeps from $0$ to $\pi$ around the top half of the unit circle, moving physically close to a pole causes the denominator to shrink, making the magnitude spike (resonance). Moving physically close to a zero causes the numerator to shrink, making the magnitude drop (attenuation or notch).

### 4.7 Ideal Filters

Ideal filters possess a magnitude response of exactly 1 in their passband and exactly 0 in their stopband, combined with exactly linear phase in the passband to ensure distortionless transmission.
For an ideal Low-Pass Filter (LPF) with cutoff frequency $\omega_c$ and delay $\alpha$:
$$
H_{ideal}(e^{j\omega}) = \begin{cases} 
1 \cdot e^{-j\alpha \omega}, & |\omega| \le \omega_c \\
0, & \omega_c < |\omega| \le \pi 
\end{cases}
$$
Taking the inverse DTFT to find the time-domain impulse response $h[n]$:
$$
h_{ideal}[n] = \frac{1}{2\pi} \int_{-\omega_c}^{\omega_c} e^{-j\alpha \omega} e^{j\omega n} d\omega = \frac{1}{2\pi} \int_{-\omega_c}^{\omega_c} e^{j\omega (n-\alpha)} d\omega
$$
Evaluating the integral:
$$
h_{ideal}[n] = \frac{1}{2\pi j(n-\alpha)} \left[ e^{j\omega_c(n-\alpha)} - e^{-j\omega_c(n-\alpha)} \right]
$$
$$
h_{ideal}[n] = \frac{\sin(\omega_c (n-\alpha))}{\pi (n-\alpha)}
$$
This is a standard sinc function, shifted by $\alpha$.
**The fundamental physical issue:** A sinc function extends infinitely from $n = -\infty$ to $n = \infty$. No matter how large we make the delay $\alpha$, the function is non-zero for $n < 0$. Therefore, a true ideal filter is strictly **non-causal**—it requires looking into the infinite future to compute the current output. Furthermore, the sequence is not absolutely summable ($\sum |h[n]| = \infty$), meaning it is only marginally stable. Ideal filters are mathematical abstractions and cannot be built in the physical world.

---

## 5. COMPLETE PROOFS AND DERIVATIONS

### Proof: Linear Phase from Symmetric FIR Filters
**Theorem:** A Finite Impulse Response (FIR) filter with an impulse response that is symmetric around its midpoint (i.e., $h[n] = h[N-1-n]$) exhibits exactly linear phase (or generalized linear phase with constant group delay).

**Rigorous Proof:**
Let the FIR filter have a finite length $N$. The frequency response by definition is:
$$
H(e^{j\omega}) = \sum_{n=0}^{N-1} h[n] e^{-j\omega n}
$$
Assume $N$ is odd for mathematical simplicity in this derivation. Let the center point index be $M = \frac{N-1}{2}$. The symmetry condition is $h[n] = h[N-1-n] = h[2M - n]$.
We rewrite the summation by explicitly splitting it into three parts: the terms before the midpoint, the midpoint term itself, and the terms after the midpoint:
$$
H(e^{j\omega}) = \sum_{n=0}^{M-1} h[n] e^{-j\omega n} + h[M]e^{-j\omega M} + \sum_{n=M+1}^{2M} h[n] e^{-j\omega n}
$$
In the third sum (the right-hand side), we introduce a change of variables to reverse the indexing. Let $m = 2M - n$. 
When $n = M+1$, the new index $m = 2M - (M+1) = M-1$. 
When $n = 2M$, the new index $m = 2M - 2M = 0$. 
The third sum becomes:
$$
\sum_{n=M+1}^{2M} h[n] e^{-j\omega n} = \sum_{m=0}^{M-1} h[2M-m] e^{-j\omega (2M-m)}
$$
Now we apply the critical symmetry condition $h[2M-m] = h[m]$:
$$
= \sum_{m=0}^{M-1} h[m] e^{-j\omega 2M} e^{j\omega m}
$$
Substitute this transformed sum back into the main frequency response equation:
$$
H(e^{j\omega}) = \sum_{n=0}^{M-1} h[n] e^{-j\omega n} + h[M]e^{-j\omega M} + \sum_{n=0}^{M-1} h[n] e^{-j\omega 2M} e^{j\omega n}
$$
Factor out the midpoint delay term $e^{-j\omega M}$ from the entire mathematical expression:
$$
H(e^{j\omega}) = e^{-j\omega M} \left[ h[M] + \sum_{n=0}^{M-1} h[n] \left( e^{j\omega(M-n)} + e^{-j\omega(M-n)} \right) \right]
$$
By using Euler's identity $e^{j\theta} + e^{-j\theta} = 2\cos(\theta)$, we can combine the exponentials into a pure real cosine term:
$$
H(e^{j\omega}) = e^{-j\omega M} \left[ h[M] + \sum_{n=0}^{M-1} 2h[n] \cos(\omega(M-n)) \right]
$$
Let the term enclosed in the brackets be designated as a real-valued amplitude function $A(\omega)$:
$$
A(\omega) = h[M] + \sum_{n=0}^{M-1} 2h[n] \cos(\omega(M-n))
$$
$$
H(e^{j\omega}) = A(\omega) e^{-j\omega M}
$$
Because $A(\omega)$ is constructed entirely from real coefficients and real cosine functions, it is purely real-valued. The phase of $H(e^{j\omega})$ is determined entirely by the complex exponential term $e^{-j\omega M}$ (plus any abrupt $180^\circ$ flips if $A(\omega)$ crosses zero and becomes negative).
Ignoring the discrete phase flips for the continuous delay calculation, the phase response is:
$$
\theta(\omega) = -M\omega = -\left(\frac{N-1}{2}\right)\omega
$$
This is an exactly linear equation of the form $y = mx$, passing straight through the origin. The group delay is mathematically defined as the negative derivative:
$$
\tau_g(\omega) = -\frac{d}{d\omega} (-M\omega) = M = \frac{N-1}{2}
$$
This result is independent of $\omega$, meaning it is a strict constant. The theorem is proved. $\blacksquare$

---

## 6. WORKED EXAMPLES (MINIMUM 5)

### Example 1: Moving Average Filter Frequency Response
**Problem statement:** Compute the frequency response $H(e^{j\omega})$ for a 3-point weighted moving average filter with impulse response $h[n] = \{\frac{1}{4}, \frac{1}{2}, \frac{1}{4}\}$ for $n=0, 1, 2$. Plot or describe the magnitude and phase. Prove it has linear phase.

**Solution:**
1. The impulse response values are $h[0]=0.25$, $h[1]=0.5$, $h[2]=0.25$.
2. The frequency response via DTFT is:
   $$
   H(e^{j\omega}) = \sum_{n=0}^{2} h[n] e^{-j\omega n} = 0.25 + 0.5 e^{-j\omega} + 0.25 e^{-j2\omega}
   $$
3. To reveal the phase properties, mathematically factor out the mid-point phase delay term $e^{-j\omega}$:
   $$
   H(e^{j\omega}) = e^{-j\omega} \left( 0.25 e^{j\omega} + 0.5 + 0.25 e^{-j\omega} \right)
   $$
4. Group the symmetric terms together:
   $$
   H(e^{j\omega}) = e^{-j\omega} \left( 0.5 + 0.25(e^{j\omega} + e^{-j\omega}) \right)
   $$
5. Apply Euler's cosine identity:
   $$
   H(e^{j\omega}) = e^{-j\omega} (0.5 + 0.5 \cos(\omega))
   $$
6. The magnitude is simply the absolute value: $|H(e^{j\omega})| = |0.5 + 0.5 \cos(\omega)|$. Note that because $-1 \le \cos(\omega) \le 1$, the term $0.5 + 0.5 \cos(\omega)$ is always $\ge 0$ for all $\omega$. We don't need absolute value bars.
7. The phase is explicitly $\angle H(e^{j\omega}) = -\omega$.

**Physical interpretation:** This is a gentle low-pass filter. At DC ($\omega=0$), the magnitude is $1$. At the Nyquist frequency ($\omega=\pi$), the magnitude is exactly $0$. The phase is perfectly linear, so it delays all frequencies identically by exactly 1 sample (constant group delay = 1).
**Common mistakes to avoid:** Forgetting to factor out the central delay term. If a student simply takes the real and imaginary parts of the original polynomial expression, the math gets extremely messy with complex arctangents, obscuring the beautiful simple linear phase property.

### Example 2: First-Order IIR Group Delay Evaluation
**Problem statement:** Find the maximum and minimum group delay of the causal, stable first-order IIR system defined by the transfer function $H(z) = \frac{1}{1 - 0.8z^{-1}}$.

**Solution:**
1. The system has a single real pole at $r = 0.8$.
2. From the rigorous derivation of the phase derivative (which can be derived using the quotient rule on the arctangent function), the exact group delay formula for a generic one-pole filter $H(z) = \frac{1}{1 - r z^{-1}}$ is:
   $$
   \tau_g(\omega) = \frac{r\cos\omega - r^2}{1 + r^2 - 2r\cos\omega}
   $$
3. Maximum group delay for a positive real pole occurs at $\omega = 0$ (the frequency closest to the pole location on the unit circle):
   $$
   \tau_g(0) = \frac{0.8(1) - 0.8^2}{1 + 0.8^2 - 2(0.8)(1)} = \frac{0.8 - 0.64}{1 + 0.64 - 1.6} = \frac{0.16}{0.04} = 4 \text{ samples}
   $$
4. Minimum group delay occurs at $\omega = \pi$ (the frequency furthest from the pole):
   $$
   \tau_g(\pi) = \frac{0.8(-1) - 0.8^2}{1 + 0.8^2 - 2(0.8)(-1)} = \frac{-0.8 - 0.64}{1 + 0.64 + 1.6} = \frac{-1.44}{3.24} \approx -0.444 \text{ samples}
   $$

**Physical interpretation:** At DC ($\omega=0$), the signal envelope is significantly delayed by exactly 4 samples. At the Nyquist rate ($\omega=\pi$), the envelope is actually advanced slightly (negative group delay), though the magnitude is heavily attenuated at this frequency. This extreme variation (4 to -0.44) causes severe dispersion for wideband signals.
**Common mistakes to avoid:** Evaluating group delay without first verifying that the filter is stable. If $r \ge 1$, the Z-transform does not converge on the unit circle, making DTFT evaluation and group delay analysis fundamentally invalid.

### Example 3: Notch Filter Geometric Evaluation
**Problem statement:** A biomedical notch filter is designed to eliminate a severe powerline interference frequency of $\omega_0 = \pi/2$. It has discrete zeros exactly on the unit circle at $e^{j\pi/2}$ and $e^{-j\pi/2}$, and stabilizing poles slightly inside at $0.9e^{j\pi/2}$ and $0.9e^{-j\pi/2}$. Plot the pole-zero diagram and compute the exact magnitude response at $\omega = 0$, $\omega = \pi/2$, and $\omega = \pi$.

**Solution:**
1. Zeros in Cartesian form: $z_1 = j, z_2 = -j$. Poles: $p_1 = 0.9j, p_2 = -0.9j$.
2. Formulate the System function:
   $$
   H(z) = \frac{(1 - j z^{-1})(1 + j z^{-1})}{(1 - 0.9j z^{-1})(1 + 0.9j z^{-1})} = \frac{1 + z^{-2}}{1 + 0.81 z^{-2}}
   $$
3. Convert to Frequency response by setting $z = e^{j\omega}$:
   $$
   H(e^{j\omega}) = \frac{1 + e^{-j2\omega}}{1 + 0.81 e^{-j2\omega}}
   $$
4. Evaluate Magnitude at $\omega = 0$:
   $$
   H(e^{j0}) = \frac{1 + e^0}{1 + 0.81 e^0} = \frac{1 + 1}{1 + 0.81} = \frac{2}{1.81} \approx 1.105
   $$
5. Evaluate Magnitude at $\omega = \pi/2$:
   $$
   H(e^{j\pi/2}) = \frac{1 + e^{-j\pi}}{1 + 0.81 e^{-j\pi}} = \frac{1 - 1}{1 - 0.81} = \frac{0}{0.19} = 0
   $$
6. Evaluate Magnitude at $\omega = \pi$:
   $$
   H(e^{j\pi}) = \frac{1 + e^{-j2\pi}}{1 + 0.81 e^{-j2\pi}} = \frac{1 + 1}{1 + 0.81} = \frac{2}{1.81} \approx 1.105
   $$

**Physical interpretation:** The filter allows DC and Nyquist frequencies to pass almost entirely unaffected (with a slight gain of ~1.1), but completely obliterates the signal exactly at $\pi/2$ (gain is precisely 0). The close proximity of the poles to the zeros ensures the notch is very sharp and narrow, minimizing damage to adjacent frequencies.
**Common mistakes to avoid:** Failing to pair complex conjugate poles and zeros. If a real-valued medical signal is processed, the filter coefficients must be entirely real. This mathematically necessitates complex conjugate symmetry in all pole and zero locations.

### Example 4: Designing an Ideal LPF
**Problem statement:** Formulate the exact impulse response for an ideal Low-Pass Filter with a sharp cutoff frequency $\omega_c = \pi/4$ and zero phase delay ($\alpha = 0$). Write out the first five analytical terms of $h[n]$ and explain technically why it cannot be realized in real-time hardware.

**Solution:**
1. The desired ideal response is mathematically defined as $H(e^{j\omega}) = 1$ for $|\omega| \le \pi/4$, and $0$ everywhere else in $[-\pi, \pi]$.
2. The impulse response is derived via the inverse DTFT integral:
   $$
   h[n] = \frac{1}{2\pi} \int_{-\pi/4}^{\pi/4} 1 \cdot e^{j\omega n} d\omega
   $$
3. For the specific case of $n=0$, L'Hopital's rule or direct integration yields:
   $$
   h[0] = \frac{1}{2\pi} [\omega]_{-\pi/4}^{\pi/4} = \frac{1}{2\pi} \left(\frac{\pi}{4} - \left(-\frac{\pi}{4}\right)\right) = \frac{1}{2\pi} \frac{2\pi}{4} = 0.25
   $$
4. For all other $n \neq 0$:
   $$
   h[n] = \frac{1}{2\pi} \left[ \frac{e^{j\omega n}}{jn} \right]_{-\pi/4}^{\pi/4} = \frac{1}{2\pi j n} (e^{j\pi n / 4} - e^{-j\pi n / 4}) = \frac{1}{\pi n} \sin\left(\frac{\pi n}{4}\right)
   $$
5. Computing the first few terms analytically:
   - $h[0] = 0.25$
   - $h[1] = \frac{\sin(\pi/4)}{\pi} \approx 0.225 = h[-1]$
   - $h[2] = \frac{\sin(\pi/2)}{2\pi} = \frac{1}{2\pi} \approx 0.159 = h[-2]$
   - $h[3] = \frac{\sin(3\pi/4)}{3\pi} \approx 0.075 = h[-3]$
   - $h[4] = \frac{\sin(\pi)}{4\pi} = 0 = h[-4]$

**Physical interpretation:** This theoretical filter requires knowledge of the infinite future. To compute the output sample $y[0]$, it requires multiplying $x[1], x[2], x[3]$ going out to infinity. 
**Common mistakes to avoid:** Believing that simple truncation makes the filter ideal. If you abruptly truncate this $h[n]$ to make it causal and finite, it immediately suffers from the Gibbs Phenomenon (severe ringing in the frequency domain) and entirely loses its ideal "brick-wall" characteristics.

### Example 5: Group Delay Specification in Communications
**Problem statement:** A high-speed digital data transmission system uses a carrier frequency $\omega_c = \pi/3$. To avoid severe intersymbol interference (ISI), the engineering spec demands that group delay variation must be strictly less than 0.5 samples over the signal bandwidth. An engineer proposes a filter with phase response $\theta(\omega) = -2\omega - 0.5 \sin(\omega)$. Verify if the filter definitively meets the ISI requirement.

**Solution:**
1. First, mathematically calculate the group delay function by taking the negative derivative:
   $$
   \tau_g(\omega) = -\frac{d\theta(\omega)}{d\omega} = -\frac{d}{d\omega} (-2\omega - 0.5\sin(\omega)) = 2 + 0.5\cos(\omega)
   $$
2. Determine the maximum group delay. This occurs when $\cos(\omega) = 1$ (at $\omega = 0$), resulting in $\tau_{g,max} = 2 + 0.5 = 2.5$ samples.
3. Determine the minimum group delay. This occurs when $\cos(\omega) = -1$ (at $\omega = \pi$), resulting in $\tau_{g,min} = 2 - 0.5 = 1.5$ samples.
4. Calculate the maximum possible variation (peak-to-peak ripple) in group delay across the ENTIRE frequency spectrum: $\Delta\tau_g = 2.5 - 1.5 = 1.0$ sample.
5. In the absolute worst-case scenario over the whole band, the variation is 1.0, which violates the $< 0.5$ limit. However, the problem specifies the requirement over the *signal bandwidth*. If the bandwidth is extremely small and tightly clustered around $\omega_c = \pi/3$, the local variation might be acceptable. 
   - Let's evaluate exactly at the carrier: $\tau_g(\pi/3) = 2 + 0.5\cos(\pi/3) = 2 + 0.5(0.5) = 2.25$.
   - Unless the bandwidth is explicitly provided, we cannot guarantee the filter meets the spec, because the global variation of 1.0 exceeds the 0.5 threshold. The engineer's proposal is risky.

**Physical interpretation:** Non-linear terms in the phase equation (like the sinusoidal $\sin(\omega)$ ripple) cause oscillations in the group delay. This ripple means different frequencies within the signal packet travel at different speeds, stretching the packet out.
**Common mistakes to avoid:** Missing the negative sign when differentiating the phase to find group delay, leading to inverted results and incorrect maximum/minimum analyses.

---

## 7. ENGINEERING APPLICATIONS AND CASE STUDIES

**Application 1: Audio Phase Equalization in Studio Mastering**
When multiple microphones record a complex instrument like a drum kit, distance variations cause time-of-flight delays. When mixed together electronically, these microscopic delays manifest as severe non-linear phase, causing "comb filtering" (a hollow, thin sound). An all-pass filter is designed mathematically with $H(e^{j\omega}) = e^{j\theta(\omega)}$ (the magnitude is exactly 1 everywhere). By cascading this specific all-pass filter into the signal chain, the audio engineer can introduce a compensatory group delay curve that precisely cancels the acoustic group delay, restoring the sharp transient attacks of the snare drum without altering the frequency balance (magnitude).

**Application 2: Dispersion Compensation in Transoceanic Fiber Optics**
In fiber optic communications, the refractive index of glass depends slightly on the wavelength of light (chromatic dispersion). Since $c = f\lambda$, different frequency components of a laser pulse travel at marginally different speeds—this is a macroscopic physical manifestation of non-constant group delay. Over a 10,000 km transatlantic cable, a square digital pulse will smear heavily into adjacent bit slots, causing catastrophic ISI. Engineers use "Dispersion Compensating Fiber" (DCF) or complex digital DSP equalizers at the receiver to apply an inverse group delay profile. If the main fiber exhibits $\tau_g \propto \omega$, the compensator applies a reverse profile $\tau_g \propto -\omega$, summing to a perfectly constant total delay.

**Application 3: Zero-Phase Filtering in Medical ECG Processing**
When filtering to remove 50/60 Hz powerline noise from an Electrocardiogram (ECG), a standard IIR notch filter can severely distort the delicate QRS complex due to non-linear group delay near the notch frequency. In non-real-time software processing (such as MATLAB's `filtfilt` function), a trick is used: the data is filtered forwards in time, the array is mathematically reversed, and it is filtered backwards.
Let the filter transfer function be $H(e^{j\omega})$. The effective overall frequency response is:
$$
H_{eff}(e^{j\omega}) = H(e^{j\omega}) H^*(e^{j\omega}) = |H(e^{j\omega})|^2 e^{j\theta(\omega)} e^{-j\theta(\omega)} = |H(e^{j\omega})|^2
$$
The phase terms cancel out exactly to zero, meaning group delay is strictly zero across all frequencies. This ensures the P, QRS, and T waves remain in their exact original time positions relative to each other, preventing fatal diagnostic errors.

---

## 8. COMMON STUDENT MISCONCEPTIONS AND ERRORS

1. **Misconception:** "Phase delay is the time it takes for a real signal to pass completely through a system."
   * **Correction:** Phase delay only applies to steady-state continuous sinusoids. An actual information-bearing signal has an envelope, and its travel time (and distortion) is determined strictly by the Group Delay. 
2. **Misconception:** "An ideal filter is the best possible filter to use in engineering practice."
   * **Correction:** Ideal filters are strictly non-causal (require future inputs forever) and their infinite sinc impulse responses must be mathematically truncated in reality. This truncation leads to severe ringing (Gibbs phenomenon) which is highly undesirable and destructive in time-domain signals.
3. **Misconception:** "A filter with flat magnitude response (Gain = 1 everywhere) does absolutely nothing to the signal."
   * **Correction:** This describes an All-Pass Filter. While it doesn't attenuate or amplify frequencies, it can have wild phase distortions. A sharp square pulse sent into a high-order all-pass filter can come out looking like a completely unrecognizable smeared chirp.
4. **Misconception:** "Group delay is always positive because a causal system cannot output a signal before it receives it."
   * **Correction:** While the total overall system delay is necessarily positive, the local group delay at specific isolated frequencies *can* be mathematically negative in IIR filters. This doesn't violate causality; it just means the envelope of that specific narrow frequency band appears shifted forward relative to the carrier. This usually occurs only in regions of extreme attenuation where the "envelope" concept becomes mathematically murky anyway.
5. **Misconception:** "All FIR filters automatically have linear phase."
   * **Correction:** Only FIR filters with symmetric (or anti-symmetric) impulse responses have linear phase. Asymmetric FIR filters (e.g., minimum-phase FIR filters) will have non-linear phase.
6. **Misconception:** "If $H(z)$ has poles and zeros, I can just evaluate it at $z = 1$ to find the maximum frequency response."
   * **Correction:** The point $z = 1$ corresponds to $\omega = 0$ (DC frequency). The highest frequency in discrete time is $\omega = \pi$, which corresponds to evaluating at $z = e^{j\pi} = -1$.

---

## 9. CONNECTIONS TO OTHER LECTURES

**Builds upon:**
- **Lecture 1-2 (LTI Systems & Convolution):** Relies entirely on the strict assumption of system linearity and time-invariance. Without LTI properties, complex exponentials aren't eigenfunctions.
- **Lecture 3 (Z-Transform):** Evaluating the algebraic $H(z)$ exclusively on the unit circle is the mathematical foundation for analyzing continuous frequency responses.

**Prerequisite for:**
- **Lecture 5 (FIR Filter Design):** The rigorous proof that a symmetric $h[n]$ yields linear phase is the entire foundational basis for Window-based and Parks-McClellan FIR design methods.
- **Lecture 7 (IIR Filter Design):** When mapping analog Butterworth/Chebyshev filters to the digital domain via the Bilinear Transform, students will see exactly how the phase becomes non-linear (warping), requiring the group delay analysis taught here.
- **Lecture 10 (Fast Fourier Transform):** Understanding the spacing and meaning of discrete frequency bins requires a rock-solid grasp of magnitude and phase on the continuous unit circle.

---

## 10. EXAMINATION QUESTIONS

### 10.1 Short Answer Questions (Model Answers Provided)
**Q1:** Define precisely what an eigenfunction is in the context of an LTI system and state the specific eigenfunction for discrete-time LTI systems.
**Model Answer:** An eigenfunction is a specific input signal that produces a system output of the exact same functional shape, differing only by a complex scalar multiplying factor (eigenvalue). For discrete-time LTI systems, eternal complex exponentials $e^{j\omega n}$ are the unique eigenfunctions.

**Q2:** Distinguish clearly between phase delay and group delay mathematically and conceptually.
**Model Answer:** Phase delay is defined as $\tau_p(\omega) = -\theta(\omega)/\omega$, representing the simple time shift of a steady continuous carrier sine wave. Group delay is defined as the negative derivative $\tau_g(\omega) = -d\theta(\omega)/d\omega$, representing the time shift of the envelope (the information-bearing wave packet) of a narrowband signal.

**Q3:** Why is linear phase considered highly desirable or even mandatory in digital data transmission systems?
**Model Answer:** Linear phase guarantees that the group delay is mathematically constant across all frequencies. This ensures that all harmonic frequency components of a digital signal pulse travel at the exact same speed, preventing the pulse from dispersing or smearing into adjacent time slots (eliminating phase distortion and ISI).

**Q4:** A given FIR filter has an impulse response $h[n] = \{1, -2, 4, -2, 1\}$. Without calculating the DTFT, determine if it has linear phase and justify your answer.
**Model Answer:** Yes, it unequivocally has linear phase. The impulse response is perfectly symmetric around its center value of 4 ($h[n] = h[4-n]$). The mathematical theorem states that all symmetric FIR filters inherently exhibit linear phase.

**Q5:** What physically happens to the magnitude response of a discrete system if a pole is placed exactly on the unit circle?
**Model Answer:** The magnitude response will mathematically go to infinity at the precise frequency $\omega$ corresponding to the pole's angle. Physically, this implies the system is marginally unstable and will oscillate infinitely at that resonant frequency, acting as an oscillator rather than a filter.

### 10.2 Long Answer / Numerical Problems

**Problem 1:** A discrete-time LTI system is described by the following linear difference equation:
$y[n] = x[n] + 2x[n-1] + x[n-2]$.
a) Find the complex frequency response $H(e^{j\omega})$.
b) Express the response cleanly in polar form (Magnitude and Phase).
c) Calculate both the phase delay and group delay.

**Solution:**
a) Take the Z-transform of both sides: $Y(z) = X(z) (1 + 2z^{-1} + z^{-2})$. 
The transfer function is $H(z) = 1 + 2z^{-1} + z^{-2} = (1+z^{-1})^2$.
Substitute $z = e^{j\omega}$ to find the frequency response: $H(e^{j\omega}) = 1 + 2e^{-j\omega} + e^{-j2\omega}$.
b) Factor out the middle delay term $e^{-j\omega}$ to reveal the symmetry:
$H(e^{j\omega}) = e^{-j\omega} (e^{j\omega} + 2 + e^{-j\omega}) = e^{-j\omega} (2 + 2\cos(\omega))$.
Magnitude: $|H(e^{j\omega})| = 2 + 2\cos(\omega)$ (Note: $2+2\cos(\omega) \ge 0$ always).
Phase: $\theta(\omega) = -\omega$.
c) Phase delay $\tau_p(\omega) = -(-\omega)/\omega = 1$.
Group delay $\tau_g(\omega) = -d(-\omega)/d\omega = 1$. Both are mathematically constant at exactly 1 sample for all frequencies.

**Problem 2:** Find the precise group delay of a first-order all-pass filter given by $H(z) = \frac{z^{-1} - a^*}{1 - a z^{-1}}$ where the parameter $a = 0.5$. Evaluate it specifically at $\omega = 0$ and $\omega = \pi$.

**Solution:**
Substitute $z = e^{j\omega}$ and $a = 0.5$:
$H(e^{j\omega}) = \frac{e^{-j\omega} - 0.5}{1 - 0.5 e^{-j\omega}}$.
The standard derived formula for the group delay of a real first-order all-pass section is:
$\tau_g(\omega) = \frac{1 - a^2}{1 + a^2 - 2a\cos\omega}$.
For $a=0.5$, substitute into the formula: 
$\tau_g(\omega) = \frac{1 - 0.25}{1 + 0.25 - \cos\omega} = \frac{0.75}{1.25 - \cos\omega}$.
Evaluate at DC ($\omega = 0$): $\tau_g(0) = \frac{0.75}{1.25 - 1} = \frac{0.75}{0.25} = 3$ samples.
Evaluate at Nyquist ($\omega = \pi$): $\tau_g(\pi) = \frac{0.75}{1.25 - (-1)} = \frac{0.75}{2.25} = \frac{1}{3} \approx 0.333$ samples.
Note the severe variation in delay (from 3 down to 0.33), demonstrating why all-pass filters cause massive phase distortion.

**Problem 3:** Design considerations for a system dictate a phase response of $\theta(\omega) = -3\omega + 0.2\sin(2\omega)$. Calculate the group delay. Find the maximum and minimum group delay values and state whether the system exhibits linear phase.

**Solution:**
Group delay $\tau_g(\omega) = -d\theta/d\omega$.
$\tau_g(\omega) = -\frac{d}{d\omega}(-3\omega + 0.2\sin(2\omega)) = 3 - 0.4\cos(2\omega)$.
Max group delay occurs when $\cos(2\omega) = -1$, so $\tau_{max} = 3 - 0.4(-1) = 3.4$ samples.
Min group delay occurs when $\cos(2\omega) = 1$, so $\tau_{min} = 3 - 0.4(1) = 2.6$ samples.
The system does NOT have linear phase because the phase response contains a non-linear sinusoidal term, and consequently, the group delay is not a constant value.

**Problem 4:** A continuous signal is sampled, processed by an ideal low-pass filter, and reconstructed. The filter has cutoff $\pi/3$ and phase $\theta(\omega) = -5\omega$. If the input is $x[n] = \cos(\pi n / 4) + \cos(3\pi n / 4)$, determine the output $y[n]$ analytically.

**Solution:**
The filter is an LPF. It passes frequencies up to $\pi/3 \approx 1.047$ rad/sample.
Input has two components:
$\omega_1 = \pi/4 \approx 0.785$ rad/sample. This is $<\pi/3$, so it passes.
$\omega_2 = 3\pi/4 \approx 2.356$ rad/sample. This is $>\pi/3$, so it is entirely blocked.
The system response at $\omega_1 = \pi/4$:
Magnitude is 1 (passband). Phase is $\theta(\pi/4) = -5(\pi/4)$.
The output is just the passed component, modified by the magnitude and phase:
$y[n] = 1 \cdot \cos(\pi n/4 - 5\pi/4) = \cos(\pi(n-5)/4)$.
The signal is perfectly delayed by exactly 5 samples.

### 10.3 True/False with Justification (6 items)

1. **True/False:** The discrete-time unit step complex exponential $e^{j\omega n} u[n]$ is a valid eigenfunction of an LTI system.
   * **FALSE:** Only two-sided, eternal complex exponentials $e^{j\omega n}$ existing for all time $-\infty < n < \infty$ are true eigenfunctions. The step function $u[n]$ acts as a switch, introducing broadband transient effects that violate the pure steady-state requirement of an eigenfunction.
2. **True/False:** All systems with exactly zero phase ($\theta(\omega) = 0$ for all $\omega$) are strictly non-causal.
   * **TRUE:** A zero-phase system implies the impulse response is perfectly symmetric around the origin ($h[n] = h[-n]$). For it to have any meaningful non-zero values for $n > 0$, it must identically have non-zero values for $n < 0$, making it fundamentally non-causal.
3. **True/False:** Group delay is mathematically defined as the derivative of the magnitude response.
   * **FALSE:** It is mathematically defined as the negative derivative of the *phase* response with respect to frequency, entirely unrelated to the magnitude derivative.
4. **True/False:** A filter demanding a constant group delay of exactly 5.5 samples cannot be physically implemented using a causal FIR filter with integer coefficients.
   * **FALSE:** A causal symmetric FIR filter of length $N$ has a constant group delay of $(N-1)/2$. Setting $(N-1)/2 = 5.5$ yields $N=12$. An even-length symmetric FIR filter naturally has a fractional group delay of 5.5 samples.
5. **True/False:** Stable, causal IIR filters can never exhibit exactly linear phase over the entire continuous frequency range $[-\pi, \pi]$.
   * **TRUE:** Exact linear phase requires perfect symmetry in the impulse response. A stable, causal IIR filter's impulse response decays exponentially to infinity in the positive direction and is zero in the negative direction, so it physically cannot be symmetric around any finite point in time. 
6. **True/False:** The complex magnitude response evaluated at $z=1$ always gives the DC gain of the discrete system.
   * **TRUE:** On the unit circle, $z = e^{j\omega}$. When the frequency $\omega = 0$ (which corresponds to DC), $z = e^{j0} = 1$. Thus, evaluating the algebraic $H(z)$ at $z=1$ yields the DC gain directly.

---

## 11. KEY FORMULAS REFERENCE

| Conceptual Topic | Mathematical Formula | Important Notes & Context |
| :--- | :--- | :--- |
| **Frequency Response Definition** | $H(e^{j\omega}) = \sum_{k=-\infty}^{\infty} h[k] e^{-j\omega k}$ | Direct evaluation of the DTFT of the impulse response sequence. |
| **LTI Eigenfunction Output** | $y[n] = H(e^{j\omega_0}) e^{j\omega_0 n}$ | Strictly for an eternal complex exponential input $x[n] = e^{j\omega_0 n}$. |
| **Magnitude Response** | $\|H(e^{j\omega})\| = \sqrt{H_R^2 + H_I^2}$ | Represents the frequency-dependent gain at frequency $\omega$. |
| **Phase Response** | $\theta(\omega) = \arctan\left(\frac{H_I}{H_R}\right)$ | Represents the phase shift (time alignment) at frequency $\omega$. |
| **Phase Delay Calculation** | $\tau_p(\omega) = -\frac{\theta(\omega)}{\omega}$ | Represents the effective time delay of a continuous carrier wave. |
| **Group Delay Calculation** | $\tau_g(\omega) = -\frac{d\theta(\omega)}{d\omega}$ | Represents the time delay of the signal envelope (wave packet). |
| **Constant Group Delay** | $\tau_g = \alpha$ | Occurs strictly if the phase response is linear: $\theta(\omega) = -\alpha\omega$. |
| **FIR Symmetry Delay** | $\tau_g = \frac{N-1}{2}$ | Valid only for symmetric/anti-symmetric FIR filters of length $N$. |
| **First-Order IIR Delay** | $\tau_g(\omega) = \frac{r\cos\omega - r^2}{1 + r^2 - 2r\cos\omega}$ | Derived for a single-pole lowpass/highpass $H(z) = \frac{1}{1 - rz^{-1}}$. |
| **All-Pass Filter Property** | $\|H(e^{j\omega})\| = 1 \quad \forall \omega$ | Severely distorts phase and group delay while preserving magnitude. |

---

## 12. FURTHER READING AND REFERENCES

1. **Alan V. Oppenheim and Ronald W. Schafer**, *Discrete-Time Signal Processing*, 3rd Ed., Pearson.
   - Chapter 5: Transform Analysis of Linear Time-Invariant Systems. (This is the absolute gold standard for rigorous mathematical treatment of group delay, phase delay, and linear phase conditions).
2. **John G. Proakis and Dimitris K. Manolakis**, *Digital Signal Processing: Principles, Algorithms, and Applications*, 4th Ed., Pearson.
   - Chapter 4: Frequency Analysis of Signals and Systems. (Excellent practical examples and geometric pole-zero interpretations).
3. **Simon Haykin and Barry Van Veen**, *Signals and Systems*, 2nd Ed., Wiley.
   - Focus on the continuous-to-discrete parallels of frequency response and foundational system theory.
4. **MIT OpenCourseWare:** EE 6.011 Introduction to Communication, Control, and Signal Processing.
   - Specifically the video lectures covering Group Delay and Dispersion in communication channels.
