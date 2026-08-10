<Faculty Notes — Lecture 3: Discrete-Time Fourier Transform (DTFT)>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY

The Discrete-Time Fourier Transform (DTFT) is often the most conceptually challenging topic for students early in the DSP curriculum. While they may have seen the continuous-time Fourier Transform (CTFT), the shift to discrete-time introduces nuances like the $2\pi$ periodicity of the spectrum that frequently trip up even the best students. 

**How to teach this lecture:**
Begin by emphasizing the core philosophy of Fourier analysis: we are decomposing complicated signals into fundamental building blocks. In DSP, these building blocks are complex exponentials $e^{j\omega n}$. Crucially, highlight that complex exponentials are *eigenfunctions* of Linear Time-Invariant (LTI) systems. This is the entire reason we bother transforming to the frequency domain—convolution in the time domain becomes multiplication in the frequency domain, drastically simplifying analysis and filter design.

**Common student difficulties:**
1. Confusing the DTFT (continuous frequency) with the DFT (discrete frequency). It is imperative to hammer home that the DTFT takes a discrete-time signal and produces a *continuous* frequency function $X(e^{j\omega})$.
2. The concept of digital frequency $\omega$ in radians/sample versus physical frequency $\Omega$ in radians/second. 
3. The $2\pi$ periodicity of the spectrum. Students often ask why we only care about the interval $[-\pi, \pi]$. You must physically demonstrate that $e^{j(\omega + 2\pi)n} = e^{j\omega n}$. 
4. Dealing with distributions like the Dirac delta function when finding the DTFT of $u[n]$ or a constant.

**Suggested demos:**
Use a MATLAB or Python script in class to plot a simple discrete signal, like a decaying exponential, and then plot its DTFT magnitude and phase. Show what happens as the signal gets longer in time (the spectrum gets narrower)—this physically grounds the time-frequency uncertainty principle. 

---
## 1. LEARNING OBJECTIVES

By the end of this lecture and the associated assignments, students will be able to:
1. **Define** the forward and inverse Discrete-Time Fourier Transform equations and explain the continuous, periodic nature of the resulting frequency spectrum.
2. **Derive** the DTFT from the Discrete Fourier Series (DFS) by taking the limit as the period $N \to \infty$.
3. **Evaluate** the convergence of the DTFT for given discrete-time sequences using the criteria of absolute summability and finite energy (Dirichlet conditions).
4. **Calculate** the DTFT for fundamental sequences, including impulses, unit steps, finite rectangular pulses, and one/two-sided decaying exponentials, from first principles.
5. **Apply** the mathematical properties of the DTFT (linearity, time shift, frequency shift, time reversal, differentiation, conjugation, convolution, and multiplication) to analyze complex signals without re-evaluating the summation formula.
6. **Construct** rigorous mathematical proofs for major DTFT theorems, including Parseval's theorem and the Convolution theorem.
7. **Interpret** magnitude and phase spectra to understand the physical and frequency-domain characteristics of linear time-invariant systems.
8. **Solve** complex numerical and algebraic problems involving forward/inverse DTFT transformations, leveraging duality and symmetry properties.

---
## 2. PREREQUISITE KNOWLEDGE REVIEW

Before embarking on the DTFT, ensure students have a firm grasp of the following mathematical tools. A quick 5-minute review is highly recommended.

**1. The Geometric Series Formula (Critical!)**
The majority of DTFT derivations for infinite duration signals rely on the infinite geometric series.
Given a common ratio $r$ where $|r| < 1$, the sum to infinity is:
$$\sum_{n=0}^{\infty} r^n = \frac{1}{1 - r}$$
For a finite geometric series:
$$\sum_{n=0}^{M-1} r^n = \frac{1 - r^M}{1 - r}$$
*Note for faculty: Write this on the board and leave it there. You will use it constantly.*

**2. Euler's Identity and Complex Exponentials**
Euler's formula is the bridge between real sinusoids and complex exponentials:
$$e^{j\theta} = \cos(\theta) + j\sin(\theta)$$
And the inverse relations:
$$\cos(\theta) = \frac{e^{j\theta} + e^{-j\theta}}{2}, \quad \sin(\theta) = \frac{e^{j\theta} - e^{-j\theta}}{2j}$$

**3. LTI Systems and Convolution**
Recall that for an LTI system with impulse response $h[n]$ and input $x[n]$, the output $y[n]$ is given by the linear convolution sum:
$$y[n] = x[n] * h[n] = \sum_{k=-\infty}^{\infty} x[k] h[n-k]$$

**4. Absolute Summability**
A sequence $x[n]$ is absolutely summable if:
$$\sum_{n=-\infty}^{\infty} |x[n]| < \infty$$
This is the primary sufficient condition for the existence of the DTFT.

---
## 3. HISTORICAL AND MOTIVATIONAL CONTEXT

**Who discovered this?**
The theoretical foundation dates back to Jean-Baptiste Joseph Fourier's 1807 work on heat transfer, where he posited that any periodic function could be represented as an infinite sum of sines and cosines. This eventually evolved into the Fourier Transform for aperiodic continuous signals. The Discrete-Time Fourier Transform is the natural extension of this theory applied to sampled sequences, heavily formalized in the mid-20th century alongside the rise of digital computers and sampled-data control systems.

**Why does EEE need this?**
In Electrical and Electronics Engineering (EEE), signals are no longer continuous voltages on an oscilloscope screen; they are arrays of numbers residing in memory (e.g., from an ADC). To design digital filters (FIR, IIR), equalize communication channels, or compress audio (MP3), we must understand the frequency content of these digital sequences. 
The DTFT bridges the gap between a discrete time-domain sequence and its continuous frequency-domain representation. Without the DTFT, the design of frequency-selective digital filters (lowpass, highpass, bandpass) would be mathematically intractable, as we would be forced to solve massive systems of difference equations rather than simple algebraic multiplications.

**Convergence and Gibbs Phenomenon**
Historically, mathematicians struggled with the convergence of Fourier series for functions with discontinuities (Dirichlet conditions). In DSP, this manifests as the Gibbs phenomenon—an inescapable oscillatory overshoot near discontinuities (like a rectangular window) that does not vanish even as the number of terms increases.

---
## 4. THEORETICAL FOUNDATIONS

### 4.1 Derivation of DTFT from DFS as $N \to \infty$
*Faculty note: Show every step. Do not skip directly to the formula.*

Consider a periodic sequence $\tilde{x}[n]$ with fundamental period $N$. It can be represented by the Discrete Fourier Series (DFS):
$$\tilde{X}[k] = \sum_{n=0}^{N-1} \tilde{x}[n] e^{-j \frac{2\pi}{N} k n}$$
The synthesis equation is:
$$\tilde{x}[n] = \frac{1}{N} \sum_{k=0}^{N-1} \tilde{X}[k] e^{j \frac{2\pi}{N} k n}$$

To extend this to an aperiodic finite-energy signal $x[n]$, we can view $x[n]$ as one period of $\tilde{x}[n]$ where the period $N$ is stretched to infinity ($N \to \infty$).
Let:
$$x[n] = \lim_{N \to \infty} \tilde{x}[n]$$

As $N \to \infty$:
1. The discrete frequency spacing $\Delta \omega = \frac{2\pi}{N}$ becomes infinitesimally small, denoted as $d\omega$.
2. The discrete frequency variable $\frac{2\pi k}{N}$ becomes a continuous variable $\omega$.
3. The summation over $N$ samples stretches from $-\infty$ to $\infty$.

Substitute $\tilde{X}[k]$ into the synthesis equation:
$$\tilde{x}[n] = \frac{1}{2\pi} \sum_{k=0}^{N-1} \tilde{X}[k] e^{j \left(\frac{2\pi}{N}\right) k n} \left( \frac{2\pi}{N} \right)$$
Let $\omega_k = \frac{2\pi}{N}k$ and $\Delta \omega = \frac{2\pi}{N}$. Then:
$$\tilde{x}[n] = \frac{1}{2\pi} \sum_{k=0}^{N-1} \tilde{X}[k] e^{j \omega_k n} \Delta \omega$$

Taking the limit as $N \to \infty$ ($\Delta \omega \to 0$):
The summation turns into an integral over a contiguous $2\pi$ interval (since the original sum covers $N$ samples, and $N \cdot \frac{2\pi}{N} = 2\pi$):
$$x[n] = \frac{1}{2\pi} \int_{-\pi}^{\pi} X(e^{j\omega}) e^{j\omega n} d\omega$$
Where the spectrum function is defined as:
$$X(e^{j\omega}) = \lim_{N \to \infty} \tilde{X}[k] = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n}$$
This establishes the standard Analysis and Synthesis equations.

### 4.2 Existence and Convergence Conditions
For the DTFT sum $X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n}$ to exist, the infinite series must converge.
**1. Absolute Summability (Uniform Convergence):**
If a sequence satisfies $\sum_{n=-\infty}^{\infty} |x[n]| < \infty$, the DTFT converges uniformly to a continuous function of $\omega$.
*Proof:* 
$$|X(e^{j\omega})| = \left| \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n} \right| \le \sum_{n=-\infty}^{\infty} |x[n] e^{-j\omega n}|$$
Since $|e^{-j\omega n}| = 1$:
$$|X(e^{j\omega})| \le \sum_{n=-\infty}^{\infty} |x[n]| < \infty$$

**2. Finite Energy (Mean-Square Convergence):**
Some signals are not absolutely summable but have finite energy (e.g., $x[n] = \frac{\sin(\omega_c n)}{\pi n}$).
$$\sum_{n=-\infty}^{\infty} |x[n]|^2 < \infty$$
In this case, the DTFT converges in the mean-square sense, meaning the energy of the error between the finite sum and the infinite sum goes to zero, even though point-wise convergence (like at discontinuities) may not hold (Gibbs phenomenon).

**3. Dirichlet Conditions:**
For absolute convergence, the signal must also have a finite number of maxima/minima and discontinuities within any finite interval, though this is inherently satisfied for bounded discrete sequences.

### 4.3 Inverse DTFT (IDTFT) Derivation
To prove the synthesis equation:
$$x[m] = \frac{1}{2\pi} \int_{-\pi}^{\pi} X(e^{j\omega}) e^{j\omega m} d\omega$$
Start with the right-hand side and substitute the definition of $X(e^{j\omega})$:
$$\text{RHS} = \frac{1}{2\pi} \int_{-\pi}^{\pi} \left( \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n} \right) e^{j\omega m} d\omega$$
Assuming uniform convergence allows swapping the integral and summation:
$$\text{RHS} = \sum_{n=-\infty}^{\infty} x[n] \left( \frac{1}{2\pi} \int_{-\pi}^{\pi} e^{j\omega(m-n)} d\omega \right)$$
Evaluate the inner integral. Let $k = m-n$.
If $k \neq 0$ ($m \neq n$):
$$\int_{-\pi}^{\pi} e^{j\omega k} d\omega = \left[ \frac{e^{j\omega k}}{jk} \right]_{-\pi}^{\pi} = \frac{e^{j\pi k} - e^{-j\pi k}}{jk} = \frac{2j\sin(\pi k)}{jk} = 0$$
(Since $\sin(\pi \times \text{integer}) = 0$).

If $k = 0$ ($m = n$):
$$\int_{-\pi}^{\pi} e^{j\omega(0)} d\omega = \int_{-\pi}^{\pi} 1 d\omega = 2\pi$$
Thus, the integral acts as a sifting property, defining the discrete Kronecker delta function:
$$\frac{1}{2\pi} \int_{-\pi}^{\pi} e^{j\omega(m-n)} d\omega = \delta[m-n]$$
Substituting back:
$$\text{RHS} = \sum_{n=-\infty}^{\infty} x[n] \delta[m-n] = x[m]$$
This completes the proof.

### 4.4 Frequency-Domain Interpretation
The complex function $X(e^{j\omega})$ is evaluated for real frequencies $\omega$.
* **Magnitude Spectrum:** $|X(e^{j\omega})|$ represents the amplitude of the frequency components present in the signal.
* **Phase Spectrum:** $\angle X(e^{j\omega})$ represents the phase shift of these components.
* **Periodicity:** 
  $$X(e^{j(\omega + 2\pi)}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j(\omega + 2\pi)n} = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n} e^{-j2\pi n}$$
  Since $e^{-j2\pi n} = \cos(2\pi n) - j\sin(2\pi n) = 1$ for all integer $n$, we have:
  $$X(e^{j(\omega + 2\pi)}) = X(e^{j\omega})$$
  Because of this, digital frequencies only have unique physical meaning within a $2\pi$ interval, usually taken as $[-\pi, \pi]$. $\omega = 0$ is DC, and $\omega = \pm \pi$ is the highest possible digital oscillation (Nyquist rate).

### 4.5 Key DTFT Pairs with Derivations

**1. Unit Impulse $\delta[n]$**
$$X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} \delta[n] e^{-j\omega n}$$
By the sifting property of the impulse, the only non-zero term is at $n=0$:
$$X(e^{j\omega}) = 1 \cdot e^{-j\omega(0)} = 1$$
*Intuition:* An impulse in time contains equal amounts of all frequencies.

**2. Unit Step $u[n]$**
The unit step is not absolutely summable, so its DTFT involves generalized functions (Dirac delta).
$$u[n] = \frac{1}{2} + \frac{1}{2}\text{sgn}[n]$$
Alternatively, we can derive it as the limit of $a^n u[n]$ as $a \to 1$.
The complete expression is:
$$X(e^{j\omega}) = \frac{1}{1 - e^{-j\omega}} + \pi \sum_{k=-\infty}^{\infty} \delta(\omega - 2\pi k)$$
*Faculty Note: Emphasize the presence of the infinite delta train, which accounts for the DC offset of the step function.*

**3. Right-Sided Exponential $a^n u[n]$ for $|a| < 1$**
$$X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} a^n u[n] e^{-j\omega n} = \sum_{n=0}^{\infty} (ae^{-j\omega})^n$$
Using infinite geometric series with ratio $r = ae^{-j\omega}$ where $|r| = |a| < 1$:
$$X(e^{j\omega}) = \frac{1}{1 - ae^{-j\omega}}$$

**4. Rectangular Window**
$$w[n] = 1 \text{ for } -M \le n \le M$$
$$W(e^{j\omega}) = \sum_{n=-M}^{M} 1 \cdot e^{-j\omega n}$$
Change variables: let $m = n + M \Rightarrow n = m - M$:
$$W(e^{j\omega}) = \sum_{m=0}^{2M} e^{-j\omega(m-M)} = e^{j\omega M} \sum_{m=0}^{2M} (e^{-j\omega})^m$$
Using the finite geometric series sum with $N_{terms} = 2M + 1$:
$$W(e^{j\omega}) = e^{j\omega M} \frac{1 - e^{-j\omega(2M+1)}}{1 - e^{-j\omega}}$$
Factor out half-angles from numerator and denominator:
$$W(e^{j\omega}) = e^{j\omega M} \frac{e^{-j\omega(2M+1)/2} \left( e^{j\omega(2M+1)/2} - e^{-j\omega(2M+1)/2} \right)}{e^{-j\omega/2} \left( e^{j\omega/2} - e^{-j\omega/2} \right)}$$
$$W(e^{j\omega}) = e^{j\omega M} \cdot e^{-j\omega M} \cdot e^{-j\omega/2} \cdot e^{j\omega/2} \frac{2j \sin\left(\omega(2M+1)/2\right)}{2j \sin(\omega/2)}$$
$$W(e^{j\omega}) = \frac{\sin\left(\omega(2M+1)/2\right)}{\sin(\omega/2)}$$
This is the discrete Dirichlet kernel. It is purely real because the original sequence is real and even.

### 4.6 DTFT Properties with Proofs

**1. Linearity**
$$a x_1[n] + b x_2[n] \xrightarrow{\text{DTFT}} a X_1(e^{j\omega}) + b X_2(e^{j\omega})$$
*Proof is trivial via the linearity of the summation operator.*

**2. Time Shifting**
$$x[n - n_0] \xrightarrow{\text{DTFT}} X(e^{j\omega}) e^{-j\omega n_0}$$
*Proof:*
$$\sum_{n=-\infty}^{\infty} x[n-n_0] e^{-j\omega n}$$
Let $m = n - n_0$, so $n = m + n_0$:
$$= \sum_{m=-\infty}^{\infty} x[m] e^{-j\omega(m + n_0)} = e^{-j\omega n_0} \sum_{m=-\infty}^{\infty} x[m] e^{-j\omega m} = e^{-j\omega n_0} X(e^{j\omega})$$
*Physical interpretation:* Delaying a signal in time does not change its frequency content (magnitude), but it adds a linear phase shift proportional to the delay $n_0$ and frequency $\omega$.

**3. Frequency Shifting (Modulation)**
$$e^{j\omega_0 n} x[n] \xrightarrow{\text{DTFT}} X(e^{j(\omega - \omega_0)})$$
*Proof:*
$$\sum_{n=-\infty}^{\infty} (x[n] e^{j\omega_0 n}) e^{-j\omega n} = \sum_{n=-\infty}^{\infty} x[n] e^{-j(\omega - \omega_0)n} = X(e^{j(\omega - \omega_0)})$$
*Physical interpretation:* Multiplying by a complex exponential shifts the entire spectrum in the frequency domain. This is the fundamental basis of AM radio and modern digital communications (upconversion to a carrier frequency).

**4. Conjugation**
$$x^*[n] \xrightarrow{\text{DTFT}} X^*(e^{-j\omega})$$
*Proof:*
$$\text{DTFT}\{x^*[n]\} = \sum_{n=-\infty}^{\infty} x^*[n] e^{-j\omega n}$$
Take the conjugate of the entire expression:
$$= \left( \sum_{n=-\infty}^{\infty} x[n] e^{j\omega n} \right)^* = \left( \sum_{n=-\infty}^{\infty} x[n] e^{-j(-\omega) n} \right)^* = X^*(e^{-j\omega})$$

**5. Time Reversal**
$$x[-n] \xrightarrow{\text{DTFT}} X(e^{-j\omega})$$
*Proof:*
$$\sum_{n=-\infty}^{\infty} x[-n] e^{-j\omega n}$$
Let $m = -n$:
$$= \sum_{m=-\infty}^{\infty} x[m] e^{-j\omega(-m)} = \sum_{m=-\infty}^{\infty} x[m] e^{-j(-\omega)m} = X(e^{-j\omega})$$
*If $x[n]$ is real, $X(e^{-j\omega}) = X^*(e^{j\omega})$.*

**6. Differentiation in Frequency**
$$n x[n] \xrightarrow{\text{DTFT}} j \frac{d X(e^{j\omega})}{d\omega}$$
*Proof:*
Take the derivative of the defining sum with respect to $\omega$:
$$\frac{d}{d\omega} X(e^{j\omega}) = \frac{d}{d\omega} \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n}$$
$$= \sum_{n=-\infty}^{\infty} x[n] \frac{d}{d\omega} (e^{-j\omega n}) = \sum_{n=-\infty}^{\infty} x[n] (-jn) e^{-j\omega n}$$
$$= -j \sum_{n=-\infty}^{\infty} (n x[n]) e^{-j\omega n} = -j \text{DTFT}\{n x[n]\}$$
Multiply both sides by $j$:
$$j \frac{d X(e^{j\omega})}{d\omega} = \text{DTFT}\{n x[n]\}$$

**7. Multiplication in Time (Windowing)**
$$x[n] \cdot y[n] \xrightarrow{\text{DTFT}} \frac{1}{2\pi} \int_{-\pi}^{\pi} X(e^{j\theta}) Y(e^{j(\omega-\theta)}) d\theta$$
This states that multiplication in the time domain corresponds to periodic (circular) convolution in the frequency domain, scaled by $1/2\pi$.

---
## 5. COMPLETE PROOFS AND DERIVATIONS

### 5.1 The Convolution Theorem
**Theorem:** If $y[n] = x[n] * h[n]$, then $Y(e^{j\omega}) = X(e^{j\omega}) \cdot H(e^{j\omega})$.

**Rigorous Proof:**
By definition, the output of an LTI system is:
$$y[n] = \sum_{k=-\infty}^{\infty} x[k] h[n-k]$$
Take the DTFT of both sides:
$$Y(e^{j\omega}) = \sum_{n=-\infty}^{\infty} \left[ \sum_{k=-\infty}^{\infty} x[k] h[n-k] \right] e^{-j\omega n}$$
Assuming absolutely summable sequences, we can invoke Fubini's theorem to interchange the order of summation:
$$Y(e^{j\omega}) = \sum_{k=-\infty}^{\infty} x[k] \left[ \sum_{n=-\infty}^{\infty} h[n-k] e^{-j\omega n} \right]$$
Focus on the inner sum. Let $m = n - k$, so $n = m + k$. The limits remain $-\infty$ to $\infty$.
$$\sum_{m=-\infty}^{\infty} h[m] e^{-j\omega (m+k)} = e^{-j\omega k} \sum_{m=-\infty}^{\infty} h[m] e^{-j\omega m} = e^{-j\omega k} H(e^{j\omega})$$
Substitute this back into the outer sum:
$$Y(e^{j\omega}) = \sum_{k=-\infty}^{\infty} x[k] \left[ e^{-j\omega k} H(e^{j\omega}) \right]$$
Since $H(e^{j\omega})$ is independent of $k$, pull it out:
$$Y(e^{j\omega}) = H(e^{j\omega}) \sum_{k=-\infty}^{\infty} x[k] e^{-j\omega k} = H(e^{j\omega}) X(e^{j\omega})$$
*Physical interpretation:* An LTI system acts as a frequency-dependent multiplier. It shapes the spectrum of the input signal by amplifying, attenuating, or phase-shifting specific frequencies according to $H(e^{j\omega})$.

### 5.2 Parseval's Theorem
**Theorem:** Energy computed in the time domain equals the energy computed in the frequency domain.
$$\sum_{n=-\infty}^{\infty} |x[n]|^2 = \frac{1}{2\pi} \int_{-\pi}^{\pi} |X(e^{j\omega})|^2 d\omega$$

**Rigorous Proof Using Convolution Theorem:**
Consider a sequence $x[n]$ and its time-reversed, conjugated version $y[n] = x^*[-n]$.
From properties, the DTFT of $y[n]$ is:
$$Y(e^{j\omega}) = X^*(e^{j\omega})$$
Let's define a new signal $z[n]$ as the convolution of $x[n]$ and $y[n]$:
$$z[n] = x[n] * y[n] = \sum_{k=-\infty}^{\infty} x[k] y[n-k]$$
By the Convolution Theorem, the DTFT of $z[n]$ is:
$$Z(e^{j\omega}) = X(e^{j\omega}) Y(e^{j\omega}) = X(e^{j\omega}) X^*(e^{j\omega}) = |X(e^{j\omega})|^2$$
Now, let's evaluate $z[n]$ at a specific time index $n=0$:
Using the convolution sum:
$$z[0] = \sum_{k=-\infty}^{\infty} x[k] y[0-k] = \sum_{k=-\infty}^{\infty} x[k] x^*[-(-k)] = \sum_{k=-\infty}^{\infty} x[k] x^*[k]$$
Since a complex number multiplied by its conjugate gives the magnitude squared ($x \cdot x^* = |x|^2$):
$$z[0] = \sum_{k=-\infty}^{\infty} |x[k]|^2$$
This is the total energy of the signal $x[n]$, which represents the left side of Parseval's relation.
Next, let's express $z[0]$ using the Inverse DTFT equation:
$$z[n] = \frac{1}{2\pi} \int_{-\pi}^{\pi} Z(e^{j\omega}) e^{j\omega n} d\omega$$
Evaluate at $n=0$:
$$z[0] = \frac{1}{2\pi} \int_{-\pi}^{\pi} Z(e^{j\omega}) e^0 d\omega = \frac{1}{2\pi} \int_{-\pi}^{\pi} |X(e^{j\omega})|^2 d\omega$$
Equating the two expressions for $z[0]$ yields Parseval's Theorem:
$$\sum_{n=-\infty}^{\infty} |x[n]|^2 = \frac{1}{2\pi} \int_{-\pi}^{\pi} |X(e^{j\omega})|^2 d\omega$$

---
## 6. WORKED EXAMPLES (MINIMUM 5)

*Faculty Note: Work these out fully on the board. Do not skip steps. State properties used.*

### Example 1: Right-Sided Decaying Exponential
**Problem statement:** Find the DTFT of the signal $x[n] = (0.8)^n u[n]$ and sketch its magnitude and phase spectra.
**Solution:**
Using the definition:
$$X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} (0.8)^n u[n] e^{-j\omega n}$$
Because $u[n] = 0$ for $n<0$, the summation bounds change to $0 \to \infty$:
$$X(e^{j\omega}) = \sum_{n=0}^{\infty} (0.8 e^{-j\omega})^n$$
This is a geometric series with ratio $r = 0.8 e^{-j\omega}$. Since $|0.8 e^{-j\omega}| = 0.8 < 1$, it converges:
$$X(e^{j\omega}) = \frac{1}{1 - 0.8 e^{-j\omega}}$$
To find magnitude and phase, convert to rectangular form:
$$X(e^{j\omega}) = \frac{1}{1 - 0.8(\cos\omega - j\sin\omega)} = \frac{1}{(1 - 0.8\cos\omega) + j(0.8\sin\omega)}$$
Magnitude:
$$|X(e^{j\omega})| = \frac{1}{\sqrt{(1 - 0.8\cos\omega)^2 + (0.8\sin\omega)^2}}$$
$$|X(e^{j\omega})| = \frac{1}{\sqrt{1 - 1.6\cos\omega + 0.64\cos^2\omega + 0.64\sin^2\omega}} = \frac{1}{\sqrt{1.64 - 1.6\cos\omega}}$$
Phase:
$$\angle X(e^{j\omega}) = -\arctan\left( \frac{0.8\sin\omega}{1 - 0.8\cos\omega} \right)$$
**Physical interpretation:** This is a low-pass filter characteristic. The maximum magnitude occurs at $\omega = 0$ ($|X(e^{j0})| = 1/(1-0.8) = 5$). The minimum is at $\omega = \pm \pi$ ($|X(e^{j\pi})| = 1/(1+0.8) \approx 0.55$).
**Common mistakes to avoid:** Students often forget to change the summation limits when $u[n]$ is present, trying to sum from $-\infty$.

### Example 2: Double-Sided Decaying Exponential
**Problem statement:** Find the DTFT of $x[n] = (0.8)^{|n|}$. Show that the result is purely real and non-negative.
**Solution:**
Split the sequence into two parts based on the absolute value:
$$x[n] = (0.8)^{-n} u[-n-1] + (0.8)^n u[n]$$
Using the sum definition:
$$X(e^{j\omega}) = \sum_{n=-\infty}^{-1} (0.8)^{-n} e^{-j\omega n} + \sum_{n=0}^{\infty} (0.8)^n e^{-j\omega n}$$
First sum: let $m = -n$:
$$S_1 = \sum_{m=1}^{\infty} (0.8)^m e^{j\omega m} = \sum_{m=1}^{\infty} (0.8 e^{j\omega})^m$$
$$S_1 = \frac{0.8 e^{j\omega}}{1 - 0.8 e^{j\omega}}$$
Second sum:
$$S_2 = \frac{1}{1 - 0.8 e^{-j\omega}}$$
Total DTFT:
$$X(e^{j\omega}) = \frac{0.8 e^{j\omega}}{1 - 0.8 e^{j\omega}} + \frac{1}{1 - 0.8 e^{-j\omega}}$$
Find a common denominator:
$$X(e^{j\omega}) = \frac{0.8 e^{j\omega} (1 - 0.8 e^{-j\omega}) + 1 (1 - 0.8 e^{j\omega})}{(1 - 0.8 e^{j\omega})(1 - 0.8 e^{-j\omega})}$$
Numerator:
$$0.8 e^{j\omega} - 0.64 + 1 - 0.8 e^{j\omega} = 0.36$$
Denominator:
$$1 - 0.8 e^{-j\omega} - 0.8 e^{j\omega} + 0.64 = 1.64 - 0.8(e^{j\omega} + e^{-j\omega}) = 1.64 - 1.6\cos\omega$$
Final Result:
$$X(e^{j\omega}) = \frac{0.36}{1.64 - 1.6\cos\omega}$$
**Physical interpretation:** Since $x[n]$ is real and even ($x[n] = x[-n]$), its transform must be purely real and even. We confirmed this because there is no imaginary part ($j$) in the final expression, and $\cos(\omega) = \cos(-\omega)$.
**Common mistakes to avoid:** Mismanaging the bounds of the first summation. Summing from $m=0$ instead of $m=1$ incorrectly adds an extra term of 1 to the result.

### Example 3: Symmetrical Rectangular Window
**Problem statement:** Find the DTFT of $w[n] = 1$ for $|n| \le M$ and $w[n]=0$ otherwise. Show it results in a Dirichlet kernel.
**Solution:**
$$W(e^{j\omega}) = \sum_{n=-M}^{M} 1 \cdot e^{-j\omega n}$$
Let $m = n + M$. The limits become $m = 0$ to $2M$.
$$W(e^{j\omega}) = \sum_{m=0}^{2M} e^{-j\omega (m-M)} = e^{j\omega M} \sum_{m=0}^{2M} (e^{-j\omega})^m$$
Apply finite geometric series:
$$W(e^{j\omega}) = e^{j\omega M} \frac{1 - e^{-j\omega(2M+1)}}{1 - e^{-j\omega}}$$
Factor half-angle exponentials:
Numerator: $1 - e^{-j\omega(2M+1)} = e^{-j\omega(2M+1)/2} \left[ e^{j\omega(2M+1)/2} - e^{-j\omega(2M+1)/2} \right]$
Denominator: $1 - e^{-j\omega} = e^{-j\omega/2} \left[ e^{j\omega/2} - e^{-j\omega/2} \right]$
Substitute back:
$$W(e^{j\omega}) = e^{j\omega M} \frac{e^{-j\omega M} e^{-j\omega/2}}{e^{-j\omega/2}} \frac{2j\sin(\omega(2M+1)/2)}{2j\sin(\omega/2)}$$
The exponentials cancel perfectly: $e^{j\omega M} e^{-j\omega M} = 1$.
$$W(e^{j\omega}) = \frac{\sin\left(\omega \frac{2M+1}{2}\right)}{\sin\left(\frac{\omega}{2}\right)}$$
**Physical interpretation:** This function is a digital sinc function. It has a main lobe centered at DC ($\omega=0$) and side lobes that decay. The wider the window in time (larger $M$), the narrower the main lobe in frequency.
**Common mistakes to avoid:** Messing up the half-angle factoring is extremely common. Tell students to write out the exponents carefully.

### Example 4: Applying Time Shift Property
**Problem statement:** Use properties to find the DTFT of $y[n] = (0.5)^{n-3} u[n-3]$.
**Solution:**
Recognize that this is a delayed version of a base sequence.
Let $x[n] = (0.5)^n u[n]$.
We know from our standard pairs that:
$$X(e^{j\omega}) = \frac{1}{1 - 0.5 e^{-j\omega}}$$
The given signal is exactly $y[n] = x[n-3]$.
According to the Time Shifting property:
$x[n-n_0] \xrightarrow{\text{DTFT}} e^{-j\omega n_0} X(e^{j\omega})$
Here, $n_0 = 3$. Therefore:
$$Y(e^{j\omega}) = e^{-j3\omega} \cdot \frac{1}{1 - 0.5 e^{-j\omega}} = \frac{e^{-j3\omega}}{1 - 0.5 e^{-j\omega}}$$
**Verification:**
Calculate directly using definition:
$$Y(e^{j\omega}) = \sum_{n=-\infty}^{\infty} (0.5)^{n-3} u[n-3] e^{-j\omega n}$$
Sum bounds change to $n=3$ to $\infty$:
$$Y(e^{j\omega}) = \sum_{n=3}^{\infty} (0.5)^{n-3} e^{-j\omega n}$$
Let $m = n - 3$. When $n=3$, $m=0$. $n = m+3$.
$$Y(e^{j\omega}) = \sum_{m=0}^{\infty} (0.5)^m e^{-j\omega (m+3)} = e^{-j3\omega} \sum_{m=0}^{\infty} (0.5 e^{-j\omega})^m$$
$$= e^{-j3\omega} \frac{1}{1 - 0.5 e^{-j\omega}}$$
**Physical interpretation:** The shape of the frequency magnitude spectrum is identical to the un-delayed exponential. However, all frequency components are phase-shifted by an amount proportional to their frequency ($\Delta \theta = -3\omega$).

### Example 5: Parseval's Theorem Application
**Problem statement:** Evaluate the infinite sum $E = \sum_{n=0}^{\infty} (0.9)^{2n}$ using Parseval's Theorem, without summing it directly. Then verify directly.
**Solution:**
Define a signal $x[n] = (0.9)^n u[n]$.
The energy of this signal in the time domain is:
$$E = \sum_{n=-\infty}^{\infty} |x[n]|^2 = \sum_{n=0}^{\infty} ((0.9)^n)^2 = \sum_{n=0}^{\infty} (0.9)^{2n}$$
Parseval's theorem states this equals the frequency domain energy:
$$E = \frac{1}{2\pi} \int_{-\pi}^{\pi} |X(e^{j\omega})|^2 d\omega$$
First, find $X(e^{j\omega})$:
$$X(e^{j\omega}) = \frac{1}{1 - 0.9 e^{-j\omega}}$$
Magnitude squared:
$$|X(e^{j\omega})|^2 = \frac{1}{(1 - 0.9 e^{-j\omega})(1 - 0.9 e^{j\omega})} = \frac{1}{1 - 0.9e^{j\omega} - 0.9e^{-j\omega} + 0.81} = \frac{1}{1.81 - 1.8\cos\omega}$$
So we must evaluate:
$$E = \frac{1}{2\pi} \int_{-\pi}^{\pi} \frac{1}{1.81 - 1.8\cos\omega} d\omega$$
Using standard complex integration (contour integral over unit circle $z = e^{j\omega}$):
$$E = \frac{1}{2\pi j} \oint_C \frac{1}{(1-0.9z^{-1})(1-0.9z)} \frac{dz}{z}$$
Poles are at $z = 0.9$ (inside) and $z = 1/0.9 \approx 1.11$ (outside).
Using Cauchy Residue Theorem for pole at $z=0.9$:
$$\text{Res}(0.9) = \lim_{z \to 0.9} (z-0.9) \frac{1}{(z-0.9)(0.9-z^{-1})} = \dots = \frac{1}{1 - 0.9^2} = \frac{1}{1 - 0.81} = \frac{1}{0.19} \approx 5.263$$
Verify by direct time-domain geometric series sum:
$$E = \sum_{n=0}^{\infty} (0.81)^n = \frac{1}{1 - 0.81} = \frac{1}{0.19} \approx 5.263$$
**Physical interpretation:** Shows the immense power of moving between domains. Sometimes an integral is easier than a sum, or vice versa.

### Example 6: Inverse DTFT using Partial Fraction Expansion
**Problem statement:** Find the inverse DTFT of $X(e^{j\omega}) = \frac{1}{(1 - 0.5e^{-j\omega})(1 - 0.25e^{-j\omega})}$.
**Solution:**
This requires finding the sequence $x[n]$ that produces this spectrum. The most robust method for rational spectra is partial fraction expansion.
First, perform the substitution $z = e^{j\omega}$ to simplify the algebra:
$$X(z) = \frac{1}{(1 - 0.5z^{-1})(1 - 0.25z^{-1})}$$
We want to decompose this into the form:
$$X(z) = \frac{A}{1 - 0.5z^{-1}} + \frac{B}{1 - 0.25z^{-1}}$$
To find $A$, multiply both sides by $(1 - 0.5z^{-1})$ and evaluate at $z^{-1} = 2$:
$$A = \left. \frac{1}{1 - 0.25z^{-1}} \right|_{z^{-1}=2} = \frac{1}{1 - 0.25(2)} = \frac{1}{1 - 0.5} = \frac{1}{0.5} = 2$$
To find $B$, multiply both sides by $(1 - 0.25z^{-1})$ and evaluate at $z^{-1} = 4$:
$$B = \left. \frac{1}{1 - 0.5z^{-1}} \right|_{z^{-1}=4} = \frac{1}{1 - 0.5(4)} = \frac{1}{1 - 2} = \frac{1}{-1} = -1$$
Substitute $A$ and $B$ back into the expansion:
$$X(e^{j\omega}) = \frac{2}{1 - 0.5e^{-j\omega}} - \frac{1}{1 - 0.25e^{-j\omega}}$$
Now, use the linearity property and the standard transform pair $a^n u[n] \leftrightarrow \frac{1}{1 - a e^{-j\omega}}$:
For the first term: $2(0.5)^n u[n]$
For the second term: $-(0.25)^n u[n]$
Combine the results in the time domain:
$$x[n] = 2(0.5)^n u[n] - (0.25)^n u[n]$$
**Physical interpretation:** The multiplication of two terms in the frequency domain corresponds to the convolution of two sequences in the time domain. Here, the system behaves as a cascade of two first-order low-pass filters. The resulting time-domain sequence is the sum of two decaying exponentials, which is typical for a second-order LTI system.
**Common mistakes to avoid:** Students often make algebraic errors when dealing with negative exponents in $z^{-1}$. Encourage them to treat $z^{-1}$ as a single variable when performing partial fraction expansion.

---
## 7. ENGINEERING APPLICATIONS AND CASE STUDIES

**1. Spectrum Analysis of Sampled Signals (Audio Engineering)**
When a continuous voltage signal (e.g., from a microphone capturing a musical performance) is sampled by an ADC at $F_s$ Hz (typically 44.1 kHz for CD quality audio), the resulting discrete sequence $x[n]$ contains frequency information that scales relative to the sampling rate. The DTFT allows us to rigorously analyze this spectrum. A digital frequency of $\omega = \pi$ radians/sample corresponds to the analog Nyquist frequency $F_s/2$ (22.05 kHz). By plotting the magnitude spectrum $|X(e^{j\omega})|$, audio engineers can visually identify noise floors, harmonic distortion, or unwanted resonances present in the digital signal. This analysis forms the foundation of all digital spectrum analyzers used in modern recording studios.

**2. Frequency Response and Design of Digital Filters (Telecommunications)**
If we design an FIR filter with coefficients $h[0], h[1], \dots, h[N]$, the DTFT of $h[n]$ gives us $H(e^{j\omega})$, the continuous frequency response. 
*Example:* A simple moving average filter is given by $y[n] = 0.5x[n] + 0.5x[n-1]$.
The impulse response is $h[n] = 0.5\delta[n] + 0.5\delta[n-1]$.
Using the DTFT pairs and linearity: 
$$H(e^{j\omega}) = 0.5 + 0.5e^{-j\omega} = 0.5 e^{-j\omega/2} (e^{j\omega/2} + e^{-j\omega/2}) = e^{-j\omega/2} \cos(\omega/2)$$
Magnitude response: $|H(e^{j\omega})| = |\cos(\omega/2)|$.
At DC ($\omega=0$), the gain is 1. At the highest frequency ($\omega=\pi$), the gain is 0. This mathematically proves that the moving average acts as a Low-Pass Filter. In telecommunications, similar but much higher-order filters are designed using the DTFT to isolate specific frequency bands (e.g., extracting a single radio channel from a wideband signal).

**3. Audio Equalization Curves (Consumer Electronics)**
Parametric Equalizers (EQs) in digital audio workstations (DAWs) or consumer stereos use Infinite Impulse Response (IIR) filters governed by difference equations. The DTFT of these equations maps exactly to the graphical curves shown on the user interface, allowing a producer or consumer to boost or cut specific frequencies (e.g., adding a "bass boost" at a specific low digital frequency $\omega_c$). The DTFT provides the exact mathematical mapping from the filter's multiplier coefficients to the perceived change in audio tonality.

**4. Radar and Sonar Signal Processing**
In radar systems, a chirp signal is transmitted and its reflection is recorded as a discrete sequence. The DTFT of the received sequence is computed (often efficiently via the FFT) to determine the Doppler shift caused by the moving target. By observing how the spectrum shifts in the frequency domain (utilizing the frequency shifting property of the DTFT), engineers can accurately calculate the velocity of aircraft or weather patterns. This is a direct real-world application of the theoretical property $x[n] e^{j\omega_0 n} \leftrightarrow X(e^{j(\omega - \omega_0)})$.

---
## 8. COMMON STUDENT MISCONCEPTIONS AND ERRORS

1. **"The DTFT is the same as the DFT."**
   *Correction:* The DTFT produces a continuous spectrum $X(e^{j\omega})$ for all real $\omega$, representing the true analytical spectrum. The DFT (Discrete Fourier Transform) produces a finite discrete array of numbers $X[k]$ meant for computers. The DFT is essentially sampled versions of the DTFT, and without understanding the DTFT, one cannot properly understand DFT zero-padding or spectral leakage.
2. **"The spectrum goes from $-\infty$ to $\infty$."**
   *Correction:* While it technically does extend from $-\infty$ to $\infty$, it is perfectly periodic with period $2\pi$. Frequencies beyond $\pi$ do not represent "higher" physical oscillations; they are aliases of lower frequencies. A digital frequency of $1.1\pi$ is physically identical to $-0.9\pi$.
3. **"DTFT doesn't exist for $u[n]$ because it's not absolutely summable."**
   *Correction:* While the standard infinite sum diverges, the DTFT exists in the sense of generalized functions (distributions). By utilizing the Dirac delta function to handle the infinite energy at DC ($\omega=0$), we preserve the analytical utility of the transform for signals with non-zero average values.
4. **"Negative digital frequencies have no physical meaning."**
   *Correction:* Negative frequencies are mathematically essential. A real cosine wave is formed by the addition of a positive and a negative complex exponential ($e^{j\omega n} + e^{-j\omega n}$). Without negative frequencies, real signals cannot exist in the Fourier domain, and phase cancellation cannot occur.
5. **"Phase spectrum discontinuity means the signal is broken."**
   *Correction:* The phase angle is mathematically computed using $\arctan(\text{Im}/\text{Re})$, which is wrapped to the principal range $[-\pi, \pi]$. The visual discontinuities (vertical jumps from $-\pi$ to $\pi$ on a plot) are just artifacts of phase wrapping, not physical discontinuities in the signal. Instruct students to use the `unwrap()` function in MATLAB/Python.
6. **"If a signal is causal, its DTFT must be real."**
   *Correction:* A causal signal ($x[n] = 0$ for $n < 0$) almost always has a complex DTFT with both magnitude and phase variations. For a DTFT to be purely real, the signal must be purely even (symmetric around $n=0$). A strictly causal signal (except a simple impulse at origin) cannot be even, so its DTFT cannot be purely real.

---
## 9. CONNECTIONS TO OTHER LECTURES

* **Builds on:** Lecture 1 (Discrete-Time Signals, Delta functions), Lecture 2 (LTI Systems, Convolution, Stability). 
* **Prerequisite for:** Lecture 4 (The Z-Transform). The DTFT is simply the Z-transform evaluated on the unit circle ($z = e^{j\omega}$). If students do not understand the DTFT, the region of convergence (ROC) concept in Z-transforms will make zero sense.
* **Prerequisite for:** Lecture 6 (The Discrete Fourier Transform - DFT). We derive the DFT by sampling the DTFT in the frequency domain.

---
## 10. EXAMINATION QUESTIONS

### 10.1 Short Answer Questions
**Q1:** What is the physical significance of evaluating the DTFT at $\omega = 0$?
*Model Answer:* It yields the DC component of the signal, which is simply the sum of all sample values: $X(e^{j0}) = \sum x[n]$.

**Q2:** Why is the DTFT periodic with period $2\pi$?
*Model Answer:* Because the basis functions, $e^{-j\omega n}$, are periodic in $\omega$ with period $2\pi$ for any integer sample index $n$.

**Q3:** State the sufficient condition for the uniform convergence of the DTFT.
*Model Answer:* The sequence $x[n]$ must be absolutely summable: $\sum |x[n]| < \infty$.

**Q4:** If $x[n]$ is a real and even sequence, what are the properties of its DTFT $X(e^{j\omega})$?
*Model Answer:* The DTFT will be purely real and even.

**Q5:** What happens to the DTFT magnitude spectrum if a signal is compressed in time (made shorter)?
*Model Answer:* The spectrum broadens in frequency, demonstrating the time-frequency uncertainty principle.

### 10.2 Long Answer / Numerical Problems

**Problem 1:** Let $x[n] = (0.4)^n u[n]$ and $y[n] = (0.2)^n u[n]$. Find the DTFT of $z[n] = x[n] * y[n]$.
*Solution:*
By Convolution Theorem, $Z(e^{j\omega}) = X(e^{j\omega}) Y(e^{j\omega})$.
$X(e^{j\omega}) = \frac{1}{1 - 0.4 e^{-j\omega}}$
$Y(e^{j\omega}) = \frac{1}{1 - 0.2 e^{-j\omega}}$
$Z(e^{j\omega}) = \frac{1}{(1 - 0.4 e^{-j\omega})(1 - 0.2 e^{-j\omega})} = \frac{1}{1 - 0.6 e^{-j\omega} + 0.08 e^{-j2\omega}}$

**Problem 2:** Find the inverse DTFT of $X(e^{j\omega}) = 2 + 3e^{-j\omega} - 4e^{-j3\omega}$.
*Solution:*
Recognize the definition $X(e^{j\omega}) = \sum x[n] e^{-j\omega n}$.
By inspection:
At $n=0$, $x[0] = 2$
At $n=1$, $x[1] = 3$
At $n=3$, $x[3] = -4$
For all other $n$, $x[n] = 0$.
So, $x[n] = 2\delta[n] + 3\delta[n-1] - 4\delta[n-3]$.

**Problem 3:** Use properties to find the DTFT of $x[n] = n (0.5)^n u[n-1]$.
*Solution:*
Rewrite: $x[n] = n (0.5)^n u[n-1]$. Wait, note that $u[n-1]$ means $n \ge 1$.
Let $v[n] = (0.5)^n u[n]$. $V(e^{j\omega}) = \frac{1}{1 - 0.5e^{-j\omega}}$.
Since $(0.5)^n u[n-1] = (0.5)^n u[n] - \delta[n]$, let $w[n] = (0.5)^n u[n-1]$.
$W(e^{j\omega}) = \frac{1}{1 - 0.5e^{-j\omega}} - 1 = \frac{0.5e^{-j\omega}}{1 - 0.5e^{-j\omega}}$.
Now use differentiation property: $x[n] = n \cdot w[n] \Rightarrow j \frac{d}{d\omega} W(e^{j\omega})$.
$j \frac{d}{d\omega} \left( \frac{0.5e^{-j\omega}}{1 - 0.5e^{-j\omega}} \right) = \dots = \frac{0.5e^{-j\omega}}{(1 - 0.5e^{-j\omega})^2}$.

**Problem 4:** Evaluate $\int_{-\pi}^{\pi} | \frac{1}{1 - 0.5 e^{-j\omega}} |^2 d\omega$ using Parseval's theorem.
*Solution:*
This integral matches the right side of Parseval's theorem scaled by $2\pi$.
Let $X(e^{j\omega}) = \frac{1}{1 - 0.5e^{-j\omega}}$.
The corresponding time signal is $x[n] = (0.5)^n u[n]$.
Energy $E = \sum_{n=0}^{\infty} (0.5)^{2n} = \sum (0.25)^n = \frac{1}{1 - 0.25} = \frac{1}{0.75} = \frac{4}{3}$.
By Parseval, $E = \frac{1}{2\pi} \int_{-\pi}^{\pi} |X|^2 d\omega$.
Therefore, $\int_{-\pi}^{\pi} |X|^2 d\omega = 2\pi E = 2\pi (4/3) = \frac{8\pi}{3}$.

**Problem 5 (Bonus):** Prove that if $x[n]$ is real, then $|X(e^{j\omega})|$ is an even function of $\omega$.
*Solution:*
Start with the definition of the DTFT:
$$X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n}$$
Now evaluate the DTFT at $-\omega$:
$$X(e^{-j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{j\omega n}$$
Take the complex conjugate of $X(e^{j\omega})$:
$$X^*(e^{j\omega}) = \left( \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n} \right)^* = \sum_{n=-\infty}^{\infty} x^*[n] e^{j\omega n}$$
Since $x[n]$ is real, $x^*[n] = x[n]$. Thus:
$$X^*(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{j\omega n}$$
Comparing the two expressions, we see that:
$$X(e^{-j\omega}) = X^*(e^{j\omega})$$
Taking the magnitude of both sides:
$$|X(e^{-j\omega})| = |X^*(e^{j\omega})|$$
Since the magnitude of a complex number is equal to the magnitude of its conjugate ($|z| = |z^*|$):
$$|X(e^{-j\omega})| = |X(e^{j\omega})|$$
This proves that the magnitude spectrum is an even function of $\omega$.

### 10.3 True/False with Justification
1. **T/F:** The DTFT of a finite length sequence always exists.
   *True.* A finite sum of bounded values is always absolutely summable.
2. **T/F:** Digital frequencies $\omega = \pi/2$ and $\omega = 5\pi/2$ represent fundamentally different oscillation rates.
   *False.* They differ by $2\pi$, therefore due to periodicity, they map to the exact same physical oscillation.
3. **T/F:** If a signal is anti-symmetric ($x[n] = -x[-n]$), its DTFT is purely imaginary.
   *True.* Euler's identity shows that the odd part of a signal corresponds exclusively to the sine (imaginary) terms.
4. **T/F:** Multiplication in the frequency domain is equivalent to multiplication in the time domain.
   *False.* Multiplication in frequency corresponds to convolution in time.
5. **T/F:** Parseval's Theorem proves that energy is lost when converting to the frequency domain.
   *False.* It proves energy is strictly conserved.
6. **T/F:** The DTFT of a real signal always has an even magnitude spectrum.
   *True.* By conjugate symmetry $X(e^{-j\omega}) = X^*(e^{j\omega})$, leading to $|X(e^{-j\omega})| = |X(e^{j\omega})|$.

---
## 11. KEY FORMULAS REFERENCE

| Concept / Property | Formula |
| :--- | :--- |
| **Forward DTFT** | $X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n}$ |
| **Inverse DTFT** | $x[n] = \frac{1}{2\pi} \int_{-\pi}^{\pi} X(e^{j\omega}) e^{j\omega n} d\omega$ |
| **Linearity** | $a x_1[n] + b x_2[n] \leftrightarrow a X_1(e^{j\omega}) + b X_2(e^{j\omega})$ |
| **Time Shifting** | $x[n-n_0] \leftrightarrow e^{-j\omega n_0} X(e^{j\omega})$ |
| **Frequency Shifting** | $e^{j\omega_0 n} x[n] \leftrightarrow X(e^{j(\omega - \omega_0)})$ |
| **Time Reversal** | $x[-n] \leftrightarrow X(e^{-j\omega})$ |
| **Conjugation** | $x^*[n] \leftrightarrow X^*(e^{-j\omega})$ |
| **Frequency Differentiation**| $n x[n] \leftrightarrow j \frac{d X(e^{j\omega})}{d\omega}$ |
| **Convolution in Time** | $x[n] * h[n] \leftrightarrow X(e^{j\omega}) H(e^{j\omega})$ |
| **Multiplication in Time** | $x[n] y[n] \leftrightarrow \frac{1}{2\pi} \int_{-\pi}^{\pi} X(e^{j\theta}) Y(e^{j(\omega-\theta)}) d\theta$ |
| **Parseval's Theorem** | $\sum_{n=-\infty}^{\infty} \|x[n]\|^2 = \frac{1}{2\pi} \int_{-\pi}^{\pi} \|X(e^{j\omega})\|^2 d\omega$ |
| **Unit Impulse $\delta[n]$** | $1$ |
| **Shifted Impulse $\delta[n-k]$**| $e^{-j\omega k}$ |
| **Unit Step $u[n]$** | $\frac{1}{1 - e^{-j\omega}} + \pi \sum_{k=-\infty}^{\infty} \delta(\omega - 2\pi k)$ |
| **Exponential $a^n u[n]$** | $\frac{1}{1 - a e^{-j\omega}}$ ($|a| < 1$) |
| **Rect Window $[-M, M]$** | $\frac{\sin(\omega(2M+1)/2)}{\sin(\omega/2)}$ |

---
## 12. FURTHER READING AND REFERENCES

* **Proakis, J. G., & Manolakis, D. G. (2006).** *Digital Signal Processing: Principles, Algorithms, and Applications* (4th Ed.). Chapter 3: The Discrete-Time Fourier Transform. Highly recommended for rigorous math.
* **Oppenheim, A. V., & Schafer, R. W. (2009).** *Discrete-Time Signal Processing* (3rd Ed.). Chapter 2: Discrete-Time Signals and Systems. Best resource for deep theoretical insights and complex edge cases.
* **Haykin, S., & Van Veen, B. (2002).** *Signals and Systems* (2nd Ed.). Excellent for linking CTFT concepts to DTFT.
* **Mitra, S. K. (2006).** *Digital Signal Processing: A Computer-Based Approach* (3rd Ed.). Chapter 3: Provides excellent MATLAB-based examples for evaluating the DTFT numerically.

---
## 13. COMPUTATIONAL CONSIDERATIONS (FOR LAB INTEGRATION)

While the DTFT is an analytical tool returning a continuous function, students will invariably ask how to compute it in software (MATLAB, Python). 
* **The `freqz` Function:** In MATLAB, the `freqz(b, a)` function is the workhorse for evaluating the DTFT of an LTI system defined by difference equation coefficients `b` and `a`. It evaluates the DTFT at a dense, discrete grid of frequencies.
* **Evaluating via FFT:** To numerically approximate the DTFT of a finite sequence $x[n]$, we pad the sequence with zeros (zero-padding) and take a long N-point Fast Fourier Transform (FFT). If we pad to $N=1024$, the FFT returns samples of the DTFT at frequencies $\omega_k = \frac{2\pi k}{1024}$.
* **Visualization:** Remind students to always plot frequency on the x-axis normalized to $\pi$ (e.g., using `plot(w/pi, abs(X))`) so the axis ranges from 0 to 1, representing the fraction of the Nyquist rate.
</Faculty Notes — Lecture 3: Discrete-Time Fourier Transform (DTFT)>























