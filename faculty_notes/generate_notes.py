import os

content = r'''<Faculty Notes — Lecture 12: IIR Filter Design — Analog Prototypes & Bilinear Transform>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY
Teaching Infinite Impulse Response (IIR) filter design using analog prototypes is a cornerstone of Digital Signal Processing. For III B.Tech EEE students, this topic bridges their foundational knowledge in analog circuits (typically from their Network Theory and Linear Integrated Circuits courses) with discrete-time systems. The primary challenge students face is understanding *why* we must design an analog filter first to obtain a digital filter. They often find this indirect approach counter-intuitive and cumbersome. As an instructor, emphasize that we are leveraging decades of robust, closed-form analog filter theory rather than reinventing the wheel in the discrete domain. Direct digital design is possible for IIR, but it relies heavily on numerical optimization, whereas the analog-to-digital mapping approach is purely algebraic and yields guaranteed optimal results.

A common student difficulty is grasping the concept of **frequency warping** in the Bilinear Transform (BLT). If they do not pre-warp the specifications, they will end up with incorrect cutoff frequencies in the final digital filter. They tend to just plug the given digital cutoff into the analog design equations. A suggested demonstration is to use MATLAB or Python in class to show the magnitude response of a filter designed with and without pre-warping, highlighting the shift in the critical frequencies. 

Furthermore, students often confuse the Impulse Invariance Method (IIM) with the BLT. Clearly distinguish that IIM causes aliasing (and is thus unsuitable for high-pass and band-stop filters), whereas BLT maps the entire imaginary axis to the unit circle without any aliasing. The price we pay for no aliasing in BLT is the non-linear compression of the frequency axis (warping). 

This lecture should ideally be taught on a chalkboard for the mathematical derivations, as seeing the steps unfold helps students follow the complex algebra. Be prepared to spend significant time on the pole derivation for the Butterworth filter.

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Explain** the philosophy of indirect IIR filter design using analog prototypes and justify its necessity over direct digital design methods.
2. **Derive** the squared magnitude response and explicitly locate the poles for an $N$-th order Butterworth analog filter on the $s$-plane.
3. **Calculate** the minimum continuous-time filter order $N$ required to meet specific passband and stopband attenuation specifications for a Butterworth filter.
4. **Compare and contrast** the detailed mathematical characteristics (ripple, roll-off, phase linearity, required order) of Butterworth, Chebyshev (Type I & II), and Elliptic (Cauer) filters.
5. **Formulate** the mathematical mapping between the continuous-time $s$-plane and the discrete-time $z$-plane using both the Impulse Invariance Method and the Bilinear Transform.
6. **Evaluate** the phenomenon of frequency warping inherent in the Bilinear Transform and apply the necessary pre-warping to discrete-time specifications.
7. **Design** a complete, fully functioning digital IIR filter from given discrete-time specifications by successfully performing pre-warping, deriving the analog prototype transfer function, and applying the Bilinear Transform.

---
## 2. PREREQUISITE KNOWLEDGE REVIEW
Before starting this lecture, students must be extremely comfortable with the following mathematical and engineering concepts:

* **The Laplace Transform and $s$-plane:** 
  - The complex frequency variable $s = \sigma + j\Omega$.
  - The requirement for bounded-input bounded-output (BIBO) stability: For causal continuous-time systems, all poles of the transfer function $H_a(s)$ must lie strictly in the Left Half Plane (LHP), meaning the real part $\sigma < 0$.
* **The $z$-Transform and $z$-plane:** 
  - The discrete-time complex variable $z = r e^{j\omega}$.
  - The requirement for discrete-time BIBO stability: All poles of $H(z)$ must lie strictly inside the unit circle, meaning magnitude $|z| < 1$.
* **Frequency Responses:** 
  - Obtaining the analog frequency response by evaluating $H_a(s)$ strictly on the imaginary axis: $s = j\Omega$.
  - Obtaining the digital frequency response by evaluating $H(z)$ strictly on the unit circle: $z = e^{j\omega}$.
* **Filter Specifications (Attenuation vs. Gain):** 
  - Passband ripple $A_p$ (or maximum attenuation), typically in dB.
  - Stopband attenuation $A_s$ (or minimum attenuation), typically in dB.
  - Cutoff frequencies: Analog frequency $\Omega$ is strictly in rad/s, while discrete frequency $\omega$ is strictly in radians/sample.
* **Euler's Identity:** 
  - $e^{j\theta} = \cos\theta + j\sin\theta$. This will be heavily used in calculating pole locations.
  - $(-1) = e^{j\pi}$, $j = e^{j\pi/2}$.

---
## 3. HISTORICAL AND MOTIVATIONAL CONTEXT
The foundation of analog filter design was laid in the early 20th century to solve crucial problems in telecommunications, telegraphy, and early radio transmission. The Butterworth filter, characterized by its "maximally flat" passband, was first described by the British engineer and physicist Stephen Butterworth in his seminal 1930 paper "On the Theory of Filter Amplifiers". His goal was to create a filter that did not distort the amplitude of signals within the desired frequency band, overcoming the uneven frequency responses of earlier designs.

Following Butterworth, mathematicians and engineers utilized advanced polynomials to achieve better performance. The Chebyshev filters utilized polynomials named after Pafnuty Chebyshev, a Russian mathematician. These allowed for a steeper roll-off at the expense of introducing ripples in either the passband or stopband. Wilhelm Cauer subsequently developed the Elliptic filter (often called the Cauer filter), utilizing Jacobian elliptic functions to provide equiripple behavior in both bands, resulting in the absolute minimum possible filter order for any given set of specifications.

For modern EEE engineers, IIR digital filters are absolutely essential. Why do we need this theoretical background today? In real-time DSP applications—such as audio channel equalization, biomedical signal processing (like removing 50/60 Hz powerline noise from an ECG), and digital control systems—we often require filters with extremely sharp cutoffs. While FIR (Finite Impulse Response) filters can achieve this with linear phase, they often require hundreds or thousands of taps (coefficients). This means high computational cost (MAC operations) and unacceptable latency. IIR filters, by utilizing feedback (poles), can achieve the exact same magnitude specifications as FIR filters but with a significantly lower order (e.g., an 8th order IIR instead of a 200th order FIR). This drastically reduces the number of multiplications per sample and minimizes processing latency, which is critical in closed-loop control and real-time audio.

---
## 4. THEORETICAL FOUNDATIONS

### 4.1 The Butterworth Filter: Maximally Flat Response
The Butterworth filter is designed to have a frequency response that is as flat as mathematically possible in the passband. This means the first $2N-1$ derivatives of the squared magnitude response are exactly zero at $\Omega = 0$. It has absolutely no ripple in either the passband or the stopband, and the response is strictly monotonically decreasing as frequency increases.

The squared magnitude response of an $N$-th order Butterworth low-pass filter is defined completely by the equation:
$$ |H_a(j\Omega)|^2 = \frac{1}{1 + \left(\frac{\Omega}{\Omega_c}\right)^{2N}} $$
Where:
* $N$ is the filter order (must be an integer).
* $\Omega_c$ is the $-3$ dB cutoff frequency (the half-power frequency).
* $\Omega$ is the continuous-time analog frequency variable.

Let us evaluate this at key frequencies to build physical intuition:
* When $\Omega = 0$ (DC): $|H_a(j0)|^2 = \frac{1}{1 + 0} = 1$. The DC gain is unity.
* When $\Omega = \Omega_c$ (Cutoff): $|H_a(j\Omega_c)|^2 = \frac{1}{1 + 1^{2N}} = \frac{1}{2}$. In decibels, this is $10 \log_{10}(0.5) \approx -3.01$ dB. This holds true regardless of the filter order $N$.
* When $\Omega \to \infty$: $|H_a(j\Omega)|^2 \to 0$ monotonically.

**Detailed Derivation of Pole Locations:**
To find the actual transfer function $H_a(s)$ that we can implement, we must extend the frequency variable to the complex $s$-plane. We know that the frequency response is evaluated on the imaginary axis, so we substitute $j\Omega = s$. This algebraically implies that $\Omega = \frac{s}{j} = -js$.

We also know from complex variable theory that for a real-coefficient rational transfer function, $|H_a(j\Omega)|^2 = H_a(j\Omega) H_a^*(j\Omega) = H_a(j\Omega) H_a(-j\Omega)$.
Substituting $\Omega = -js$:
$$ H_a(s) H_a(-s) = \frac{1}{1 + \left(\frac{s/j}{\Omega_c}\right)^{2N}} $$
$$ H_a(s) H_a(-s) = \frac{1}{1 + \frac{s^{2N}}{j^{2N} \Omega_c^{2N}}} $$
We must evaluate $j^{2N}$. We know that $j^2 = -1$. Therefore, $j^{2N} = (j^2)^N = (-1)^N$.
$$ H_a(s) H_a(-s) = \frac{1}{1 + \frac{s^{2N}}{(-1)^N \Omega_c^{2N}}} = \frac{1}{1 + (-1)^{-N} \left(\frac{s}{\Omega_c}\right)^{2N}} $$
Since $(-1)^{-N} = (-1)^N$, we have:
$$ H_a(s) H_a(-s) = \frac{1}{1 + (-1)^N \left(\frac{s}{\Omega_c}\right)^{2N}} $$

To find the poles of this combined system $H_a(s)H_a(-s)$, we equate the denominator to zero:
$$ 1 + (-1)^N \left(\frac{s}{\Omega_c}\right)^{2N} = 0 $$
$$ \left(\frac{s}{\Omega_c}\right)^{2N} = - \frac{1}{(-1)^N} = -(-1)^{-N} = (-1)^{1-N} = (-1)^{N-1} $$
We now express the real number $(-1)^{N-1}$ in complex polar form using Euler's identity. Any real number 1 can be written as $e^{j2\pi k}$, and $-1$ can be written as $e^{j\pi(2k+1)}$ for integer $k$.
Thus, $(-1)^{N-1} = e^{j\pi(N-1)} \cdot e^{j2\pi k} = e^{j\pi(2k + N - 1)}$.
$$ \left(\frac{s}{\Omega_c}\right)^{2N} = e^{j\pi(2k + N - 1)} $$
To solve for $s$, we take the $2N$-th root of both sides. In the complex plane, taking a root divides the angle by the root value.
$$ \frac{s_k}{\Omega_c} = e^{j \frac{\pi(2k + N - 1)}{2N}} $$
$$ s_k = \Omega_c e^{j \frac{\pi(2k + N - 1)}{2N}} \quad \text{for } k = 0, 1, 2, \dots, 2N-1 $$

This gives us $2N$ poles. These poles lie exactly on a circle of radius $\Omega_c$ in the $s$-plane. 
However, $H_a(s)H_a(-s)$ contains the poles of the causal, stable filter $H_a(s)$ AND the anti-causal, unstable filter $H_a(-s)$. 
For a physically realizable, stable continuous-time filter, all poles must lie in the Left Half Plane (LHP). We therefore must select the $N$ poles out of the $2N$ total poles that have a negative real part.
Mathematically, the stable poles correspond to indices $k = 1, 2, \dots, N$.
The selected stable transfer function is then constructed as:
$$ H_a(s) = \frac{\Omega_c^N}{\prod_{k=1}^N (s - s_k)} $$

### 4.2 Chebyshev Filters: Equiripple Response
When the requirement for a maximally flat passband is relaxed, we can allow small, bounded fluctuations (ripples) in the frequency response. By allowing ripple, Chebyshev filters achieve a significantly steeper transition from passband to stopband (roll-off) for the exact same filter order $N$ compared to a Butterworth filter.

**Chebyshev Type I (Passband Ripple):**
Type I filters feature equiripple behavior strictly in the passband and monotonic roll-off in the stopband.
The squared magnitude response is defined as:
$$ |H_a(j\Omega)|^2 = \frac{1}{1 + \epsilon^2 C_N^2\left(\frac{\Omega}{\Omega_p}\right)} $$
Here, $\Omega_p$ is specifically the passband edge frequency, not the -3dB cutoff.
The parameter $\epsilon$ (epsilon) is a real constant that strictly controls the maximum passband ripple amplitude. The ripple in dB is given by $R_p = 10 \log_{10}(1 + \epsilon^2)$.
The function $C_N(x)$ is the Chebyshev polynomial of the first kind of order $N$. It is defined piece-wise:
$$ C_N(x) = \begin{cases} \cos(N \cos^{-1} x) & \text{for } |x| \leq 1 \text{ (Passband)} \\ \cosh(N \cosh^{-1} x) & \text{for } |x| > 1 \text{ (Stopband)} \end{cases} $$
Properties of the Chebyshev polynomials:
- $C_0(x) = 1$
- $C_1(x) = x$
- $C_2(x) = 2x^2 - 1$
- Recursion relation: $C_N(x) = 2x C_{N-1}(x) - C_{N-2}(x)$
In the passband ($|x| \le 1$), the polynomial evaluates to a cosine function, bounding its value strictly between -1 and +1. This causes the $|H_a(j\Omega)|^2$ term to oscillate precisely between $1$ and $\frac{1}{1+\epsilon^2}$, creating the equiripple effect.
In the stopband ($|x| > 1$), it evaluates to a hyperbolic cosine, which grows extremely rapidly, much faster than the simple polynomial $x^{2N}$ in the Butterworth filter. This rapid growth in the denominator creates the steep roll-off.
The poles of a Chebyshev Type I filter do not lie on a circle; they lie on an **ellipse** in the left half of the $s$-plane.

**Chebyshev Type II (Stopband Ripple):**
Type II filters, also called inverse Chebyshev filters, feature strictly monotonic behavior in the passband and equiripple behavior in the stopband. 
The squared magnitude response is:
$$ |H_a(j\Omega)|^2 = \frac{1}{1 + \left[ \epsilon^2 C_N^2\left(\frac{\Omega_s}{\Omega}\right) \right]^{-1}} $$
Notice the inversion of the frequency ratio $\frac{\Omega_s}{\Omega}$. This inversion maps the oscillating passband of the polynomial to the high frequencies of the filter's stopband.
Unlike Butterworth and Chebyshev Type I (which are all-pole filters), Chebyshev Type II filters contain both poles and zeros. The zeros lie directly on the $j\Omega$ imaginary axis. When evaluated at these zeros, the transfer function drops exactly to zero, creating the deep, repeating nulls (equiripple behavior) in the stopband.

### 4.3 Elliptic (Cauer) Filters
Elliptic filters provide equiripple behavior in **both** the passband and the stopband. 
By distributing the error evenly across both bands, the Elliptic filter achieves the absolute sharpest transition band possible for any given filter order. For a strict set of specifications, an Elliptic filter will always yield the **minimum possible order $N$** compared to Butterworth or Chebyshev.
The magnitude response is mathematically defined using Jacobian elliptic functions $U_N(x)$:
$$ |H_a(j\Omega)|^2 = \frac{1}{1 + \epsilon^2 U_N^2\left(\frac{\Omega}{\Omega_p}\right)} $$
Because the mathematics involves complex elliptic integrals and is highly non-trivial to solve by hand, practical engineering designs rely exclusively on software tools (like MATLAB's `ellip` or Python's `scipy.signal.ellip`) to compute the pole and zero locations. The resulting transfer function contains both poles and zeros, with zeros on the $j\Omega$ axis.

### 4.4 The Impulse Invariance Method (IIM)
The IIM is a time-domain approach. It creates a digital filter by directly sampling the impulse response of the continuous-time analog filter:
$$ h[n] = T_s \, h_a(nT_s) $$
The scaling factor $T_s$ (sampling period) is included to maintain the proper DC gain of the filter.
If the analog transfer function has distinct poles, it can be expanded via partial fractions:
$$ H_a(s) = \sum_{k=1}^N \frac{A_k}{s - s_k} $$
The inverse Laplace transform gives the continuous impulse response:
$$ h_a(t) = \sum_{k=1}^N A_k e^{s_k t} u(t) $$
Sampling this at discrete intervals $t = nT_s$:
$$ h[n] = T_s \sum_{k=1}^N A_k e^{s_k n T_s} u[n] = \sum_{k=1}^N (T_s A_k) (e^{s_k T_s})^n u[n] $$
Taking the standard Z-transform of this discrete sequence yields:
$$ H(z) = \sum_{k=1}^N \frac{T_s A_k}{1 - e^{s_k T_s} z^{-1}} $$
**Fundamental Mapping:** 
By comparing the analog partial fraction to the digital one, we see that every analog pole $s_k$ maps directly and exactly to a digital pole $z_k$ via the relation:
$$ z_k = e^{s_k T_s} $$
**The Critical Drawback (Aliasing):**
Because the IIM is fundamentally based on time-domain sampling, it is governed by the Nyquist-Shannon sampling theorem. Sampling in the time domain causes periodic replication of the spectrum in the frequency domain. If the analog filter is not strictly bandlimited (which no practical finite-order filter is), the high-frequency tails of the analog filter's spectrum will fold back into the baseband (aliasing). 
This severe aliasing distortion makes the IIM entirely unsuitable for high-pass or band-stop filters, as they inherently contain infinite high-frequency energy. It is only marginally acceptable for low-pass or narrow band-pass filters where the attenuation at the Nyquist frequency is extremely high.

### 4.5 The Bilinear Transform (BLT)
The Bilinear Transform is a frequency-domain approach designed specifically to solve the aliasing problem of the IIM. It achieves this by mapping the entire infinite analog imaginary axis $j\Omega$ (from $-\infty$ to $+\infty$) exactly once around the digital unit circle ($-\pi$ to $+\pi$).
It is derived from approximating the continuous-time integration operation using the numerical Trapezoidal Rule.
The resulting algebraic substitution to map from $s$-domain to $z$-domain is:
$$ s = \frac{2}{T_s} \frac{1 - z^{-1}}{1 + z^{-1}} = \frac{2}{T_s} \frac{z - 1}{z + 1} $$

**Detailed Derivation of Frequency Warping:**
To understand how frequencies map between the two domains, we substitute the frequency boundaries. We set $s = j\Omega$ (the analog frequency axis) and $z = e^{j\omega}$ (the digital frequency axis).
$$ j\Omega = \frac{2}{T_s} \frac{e^{j\omega} - 1}{e^{j\omega} + 1} $$
To simplify this complex exponential fraction, we factor out the half-angle $e^{j\omega/2}$ from both the numerator and the denominator:
$$ j\Omega = \frac{2}{T_s} \frac{e^{j\omega/2}(e^{j\omega/2} - e^{-j\omega/2})}{e^{j\omega/2}(e^{j\omega/2} + e^{-j\omega/2})} $$
The $e^{j\omega/2}$ terms cancel out. We now apply Euler's identities for sine and cosine:
$\sin(\theta) = \frac{e^{j\theta} - e^{-j\theta}}{2j} \implies e^{j\theta} - e^{-j\theta} = 2j\sin(\theta)$
$\cos(\theta) = \frac{e^{j\theta} + e^{-j\theta}}{2} \implies e^{j\theta} + e^{-j\theta} = 2\cos(\theta)$
Applying these with $\theta = \omega/2$:
$$ j\Omega = \frac{2}{T_s} \frac{2j \sin(\omega/2)}{2 \cos(\omega/2)} = j \frac{2}{T_s} \tan\left(\frac{\omega}{2}\right) $$
Dividing both sides by $j$, we arrive at the pivotal **Warping Equation**:
$$ \Omega = \frac{2}{T_s} \tan\left(\frac{\omega}{2}\right) $$
This mapping is highly non-linear. While small frequencies map approximately linearly ($\tan(x) \approx x$ for small $x$), high analog frequencies are severely compressed. The entire analog range $\Omega \to \infty$ is compressed into the digital frequency $\omega = \pi$.
To compensate for this compression in our final digital filter, we must **pre-warp** our desired discrete-time critical frequencies (like cutoff or stopband edge) into corresponding analog frequencies *before* we design the analog prototype filter.

---
## 5. COMPLETE PROOFS AND DERIVATIONS

### Proof 1: Comprehensive Derivation of Butterworth Order Formula
Given strict filter specifications:
- $A_p$ is the maximum passband attenuation at the passband edge frequency $\Omega_p$.
- $A_s$ is the minimum stopband attenuation at the stopband edge frequency $\Omega_s$.
*Note: Ensure $A_p$ and $A_s$ are strictly in linear (magnitude) scale, not decibels.*

From the exact definition of the squared magnitude response:
1. At the passband edge $\Omega_p$:
   $A_p^2 = 1 + \left(\frac{\Omega_p}{\Omega_c}\right)^{2N}$
2. At the stopband edge $\Omega_s$:
   $A_s^2 = 1 + \left(\frac{\Omega_s}{\Omega_c}\right)^{2N}$

We have a system of two equations with two unknowns ($N$ and $\Omega_c$). We will solve for $N$ by eliminating the unknown $\Omega_c$.
Rearranging equation 1:
$$ A_p^2 - 1 = \left(\frac{\Omega_p}{\Omega_c}\right)^{2N} $$
$$ (A_p^2 - 1)^{1/2N} = \frac{\Omega_p}{\Omega_c} $$
$$ \Omega_c = \frac{\Omega_p}{(A_p^2 - 1)^{1/2N}} $$

Rearranging equation 2:
$$ A_s^2 - 1 = \left(\frac{\Omega_s}{\Omega_c}\right)^{2N} $$
$$ (A_s^2 - 1)^{1/2N} = \frac{\Omega_s}{\Omega_c} $$
$$ \Omega_c = \frac{\Omega_s}{(A_s^2 - 1)^{1/2N}} $$

Equating the two expressions for $\Omega_c$:
$$ \frac{\Omega_p}{(A_p^2 - 1)^{1/2N}} = \frac{\Omega_s}{(A_s^2 - 1)^{1/2N}} $$
Cross-multiplying and grouping terms to the power of $1/2N$:
$$ \frac{(A_s^2 - 1)^{1/2N}}{(A_p^2 - 1)^{1/2N}} = \frac{\Omega_s}{\Omega_p} $$
$$ \left( \frac{A_s^2 - 1}{A_p^2 - 1} \right)^{1/2N} = \frac{\Omega_s}{\Omega_p} $$
Raise both sides to the power of $2N$:
$$ \frac{A_s^2 - 1}{A_p^2 - 1} = \left(\frac{\Omega_s}{\Omega_p}\right)^{2N} $$
To solve for the exponent $2N$, take the base-10 logarithm on both sides:
$$ \log_{10}\left( \frac{A_s^2 - 1}{A_p^2 - 1} \right) = \log_{10}\left( \left(\frac{\Omega_s}{\Omega_p}\right)^{2N} \right) $$
Using logarithmic properties, bring down the exponent:
$$ \log_{10}\left( \frac{A_s^2 - 1}{A_p^2 - 1} \right) = 2N \log_{10}\left(\frac{\Omega_s}{\Omega_p}\right) $$
Divide to isolate $N$:
$$ N = \frac{\log_{10}\left(\frac{A_s^2 - 1}{A_p^2 - 1}\right)}{2 \log_{10}\left(\frac{\Omega_s}{\Omega_p}\right)} $$
Because a physical filter must have an integer number of components (or delays), the order $N$ must be an integer. Since we must strictly meet or exceed the attenuation specifications, we must round up to the next highest integer:
$$ N_{final} = \lceil N_{calc} \rceil $$

### Proof 2: Stability Preservation in Bilinear Transform
It is crucial to prove that applying the Bilinear Transform to a stable analog filter guarantees a stable digital filter.
Let the analog complex frequency be $s = \sigma + j\Omega$. 
The inverse Bilinear mapping (from $s$ to $z$) is given by rearranging $s = \frac{2}{T_s}\frac{z-1}{z+1}$ to solve for $z$:
$$ z = \frac{1 + (T_s/2)s}{1 - (T_s/2)s} $$
Substituting $s = \sigma + j\Omega$:
$$ z = \frac{1 + \frac{T_s}{2}(\sigma + j\Omega)}{1 - \frac{T_s}{2}(\sigma + j\Omega)} = \frac{(1 + \frac{T_s}{2}\sigma) + j\left(\frac{T_s}{2}\Omega\right)}{(1 - \frac{T_s}{2}\sigma) - j\left(\frac{T_s}{2}\Omega\right)} $$
To analyze stability, we must find the magnitude of $z$. The magnitude squared $|z|^2$ of a complex fraction is the magnitude squared of the numerator divided by the magnitude squared of the denominator ($|a+jb|^2 = a^2 + b^2$):
$$ |z|^2 = \frac{\left(1 + \frac{T_s}{2}\sigma\right)^2 + \left(\frac{T_s}{2}\Omega\right)^2}{\left(1 - \frac{T_s}{2}\sigma\right)^2 + \left(\frac{T_s}{2}\Omega\right)^2} $$
We analyze three distinct regions of the $s$-plane:
* **Case 1: Left Half Plane (LHP).** For a stable analog filter, all poles have $\sigma < 0$.
  If $\sigma$ is a negative number, then $(1 + \frac{T_s}{2}\sigma)$ is smaller in magnitude than $(1 - \frac{T_s}{2}\sigma)$.
  Since the imaginary parts $(\frac{T_s}{2}\Omega)^2$ are identical, the entire numerator is strictly smaller than the denominator.
  Therefore, $|z|^2 < 1 \implies |z| < 1$. 
  *Conclusion:* All LHP poles map strictly strictly to the inside of the unit circle. Stability is unconditionally preserved.
* **Case 2: Imaginary Axis.** Here, $\sigma = 0$.
  The real parts become identical: $1^2 = 1^2$.
  The numerator exactly equals the denominator.
  Therefore, $|z|^2 = 1 \implies |z| = 1$.
  *Conclusion:* The $j\Omega$ axis maps perfectly to the unit circle boundary.
* **Case 3: Right Half Plane (RHP).** For unstable poles, $\sigma > 0$.
  If $\sigma$ is positive, $(1 + \frac{T_s}{2}\sigma)$ is larger than $(1 - \frac{T_s}{2}\sigma)$.
  The numerator is strictly greater than the denominator.
  Therefore, $|z|^2 > 1 \implies |z| > 1$.
  *Conclusion:* Unstable poles map outside the unit circle.

---
## 6. WORKED EXAMPLES (MINIMUM 5 — fully solved)

### Example 1: Full Butterworth Order Calculation
**Problem statement:** Calculate the required minimum integer order $N$ for an analog Butterworth low-pass filter satisfying the following strict specifications:
- Maximum passband attenuation of $1.5$ dB at frequency $\Omega_p = 20$ rad/s.
- Minimum stopband attenuation of $45$ dB at frequency $\Omega_s = 60$ rad/s.
**Solution:**
**Step 1:** Convert attenuation given in decibels (dB) to absolute linear squared ratios.
Our formula utilizes $A_p^2$ and $A_s^2$. The conversion is $A^2 = 10^{\text{dB}/10}$.
$A_p^2 = 10^{1.5/10} = 10^{0.15} \approx 1.4125$
$A_s^2 = 10^{45/10} = 10^{4.5} \approx 31622.77$
**Step 2:** Apply the Butterworth exact order formula derived previously.
$$ N \geq \frac{\log_{10}\left(\frac{A_s^2 - 1}{A_p^2 - 1}\right)}{2 \log_{10}\left(\frac{\Omega_s}{\Omega_p}\right)} $$
Substitute the computed values:
$$ N \geq \frac{\log_{10}\left(\frac{31622.77 - 1}{1.4125 - 1}\right)}{2 \log_{10}\left(\frac{60}{20}\right)} $$
$$ N \geq \frac{\log_{10}\left(\frac{31621.77}{0.4125}\right)}{2 \log_{10}(3)} $$
Calculate the ratio inside the logarithm:
$\frac{31621.77}{0.4125} \approx 76658.83$
Calculate logarithms:
$\log_{10}(76658.83) \approx 4.8845$
$\log_{10}(3) \approx 0.4771$
$$ N \geq \frac{4.8845}{2 \times 0.4771} = \frac{4.8845}{0.9542} \approx 5.118 $$
**Step 3:** Round to integer.
Since $N$ must be an integer, and an order of 5 would fail to meet the $45$ dB stopband requirement (it would provide slightly less attenuation), we must round up.
$N = \lceil 5.118 \rceil = 6$.
**Physical interpretation:** The designed continuous-time filter will require a 6th-order differential equation to model. In physical circuit synthesis, this will translate to 6 reactive energy-storage components (inductors and capacitors in a ladder network).
**Common mistakes to avoid:** The most frequent student error is calculating $20 \log_{10}(A)$ instead of $10 \log_{10}(A^2)$. Ensure students know the formula intrinsically requires squared magnitude ratios.

### Example 2: Complete Analog Prototype Derivation for N=2
**Problem statement:** Derive the exact transfer function $H_a(s)$ for a 2nd-order ($N=2$) analog Butterworth low-pass filter with a 3-dB cutoff frequency $\Omega_c = 100$ rad/s.
**Solution:**
**Step 1:** Determine the total number of poles and the stable pole condition.
For $N=2$, the squared magnitude response equation has $2N=4$ total poles lying on a circle of radius $\Omega_c = 100$. We require the $N=2$ stable poles located in the Left Half Plane.
**Step 2:** Calculate pole angles using the general formula.
$$ s_k = \Omega_c e^{j \frac{\pi(2k + N - 1)}{2N}} \quad \text{for } k=1, 2 $$
For $k=1$:
$$ \theta_1 = \frac{\pi(2(1) + 2 - 1)}{4} = \frac{3\pi}{4} \text{ radians} (135^\circ) $$
$$ s_1 = 100 e^{j \frac{3\pi}{4}} = 100 \left( \cos(135^\circ) + j\sin(135^\circ) \right) = 100 \left( -\frac{\sqrt{2}}{2} + j\frac{\sqrt{2}}{2} \right) \approx -70.71 + j70.71 $$
For $k=2$:
$$ \theta_2 = \frac{\pi(2(2) + 2 - 1)}{4} = \frac{5\pi}{4} \text{ radians} (225^\circ) $$
$$ s_2 = 100 e^{j \frac{5\pi}{4}} = 100 \left( \cos(225^\circ) + j\sin(225^\circ) \right) = 100 \left( -\frac{\sqrt{2}}{2} - j\frac{\sqrt{2}}{2} \right) \approx -70.71 - j70.71 $$
Notice that $s_1$ and $s_2$ form a complex conjugate pair, which is strictly required for the final transfer function to have real coefficients.
**Step 3:** Formulate the transfer function.
$$ H_a(s) = \frac{\Omega_c^N}{(s-s_1)(s-s_2)} $$
Substitute the exact radical forms for precision:
$$ H_a(s) = \frac{100^2}{\left(s - 100(-\frac{\sqrt{2}}{2} + j\frac{\sqrt{2}}{2})\right) \left(s - 100(-\frac{\sqrt{2}}{2} - j\frac{\sqrt{2}}{2})\right)} $$
Let $a = 100\frac{\sqrt{2}}{2} = 50\sqrt{2}$. The poles are $-a + ja$ and $-a - ja$.
$$ (s - (-a + ja))(s - (-a - ja)) = ((s+a) - ja)((s+a) + ja) $$
Using difference of squares: $(x-y)(x+y) = x^2 - y^2$.
$$ = (s+a)^2 - (ja)^2 = (s^2 + 2as + a^2) - (-a^2) = s^2 + 2as + 2a^2 $$
Substitute $a = 50\sqrt{2}$:
$2a = 100\sqrt{2} \approx 141.42$
$2a^2 = 2(50\sqrt{2})^2 = 2(2500 \cdot 2) = 10000 = \Omega_c^2$
Therefore, the denominator is $s^2 + 100\sqrt{2}s + 10000$.
$$ H_a(s) = \frac{10000}{s^2 + 141.42s + 10000} $$
**Physical interpretation:** This is the classic 2nd-order system characteristic equation $s^2 + 2\zeta\omega_n s + \omega_n^2$. By pattern matching, the natural frequency $\omega_n = \Omega_c = 100$, and the damping ratio $2\zeta\omega_n = 100\sqrt{2} \implies 2\zeta(100) = 141.4 \implies \zeta = \frac{\sqrt{2}}{2} \approx 0.707$. A damping ratio of 0.707 defines the maximally flat Butterworth response.

### Example 3: Applying Bilinear Transform to a 1st-Order Prototype
**Problem statement:** Given the simple 1st-order analog low-pass filter $H_a(s) = \frac{\Omega_c}{s + \Omega_c}$ with an analog cutoff of $\Omega_c = 2$ rad/s, apply the Bilinear Transform to find the digital transfer function $H(z)$. Assume a sampling period $T_s = 0.5$ seconds. Calculate the resulting digital cutoff frequency $\omega_c$.
**Solution:**
**Step 1:** Formulate the specific BLT substitution equation.
$$ s = \frac{2}{T_s} \frac{z-1}{z+1} = \frac{2}{0.5} \frac{z-1}{z+1} = 4 \frac{z-1}{z+1} $$
**Step 2:** Substitute into $H_a(s)$.
Given $\Omega_c = 2$:
$$ H(z) = \frac{2}{\left(4 \frac{z-1}{z+1}\right) + 2} $$
**Step 3:** Simplify the algebraic fraction.
Multiply the numerator and the denominator entirely by $(z+1)$ to clear the complex fraction:
$$ H(z) = \frac{2(z+1)}{4(z-1) + 2(z+1)} $$
Expand the denominator:
$$ = \frac{2z + 2}{4z - 4 + 2z + 2} = \frac{2z + 2}{6z - 2} $$
Divide numerator and denominator by 2 to simplify:
$$ H(z) = \frac{z + 1}{3z - 1} $$
Express in negative powers of $z$ (standard DSP format) by dividing numerator and denominator by $z$:
$$ H(z) = \frac{1 + z^{-1}}{3 - z^{-1}} $$
Normalize the leading denominator coefficient to 1 by dividing everything by 3:
$$ H(z) = \frac{\frac{1}{3} + \frac{1}{3}z^{-1}}{1 - \frac{1}{3}z^{-1}} = \frac{0.3333(1 + z^{-1})}{1 - 0.3333z^{-1}} $$
**Step 4:** Determine the actual digital cutoff frequency.
The analog filter was designed at $\Omega_c = 2$. We must use the warping equation to find where this frequency landed in the digital domain.
$$ \Omega_c = \frac{2}{T_s} \tan\left(\frac{\omega_c}{2}\right) $$
$$ 2 = \frac{2}{0.5} \tan\left(\frac{\omega_c}{2}\right) \implies 2 = 4 \tan\left(\frac{\omega_c}{2}\right) $$
$$ \tan\left(\frac{\omega_c}{2}\right) = 0.5 $$
$$ \frac{\omega_c}{2} = \tan^{-1}(0.5) \approx 0.4636 \text{ radians} $$
$$ \omega_c = 2 \times 0.4636 = 0.9272 \text{ radians/sample} $$
**Physical interpretation:** If we intended to build a digital filter with a cutoff of $1.0$ rad/sample, this process would have failed because the cutoff warped to $0.9272$. This explicitly demonstrates why **pre-warping** is a mandatory first step.

### Example 4: The Complete Digital Design Procedure (A to Z)
**Problem statement:** Design a 3rd-order digital Butterworth low-pass filter with a discrete-time cutoff frequency $\omega_c = 0.4\pi$ radians/sample using the Bilinear Transform method. Show every mathematical step.
**Solution:**
**Step 1: Prewarping.**
We must warp the desired digital cutoff into a target analog cutoff.
We are allowed to choose any dummy value for $T_s$ because it will cancel out during the BLT step. The standard convention to simplify algebra is to choose $T_s = 2$.
$$ \Omega_c = \frac{2}{T_s} \tan\left(\frac{\omega_c}{2}\right) = \frac{2}{2} \tan\left(\frac{0.4\pi}{2}\right) = \tan(0.2\pi) $$
Evaluating $\tan(0.2\pi) = \tan(36^\circ) \approx 0.7265$ rad/s.
This is our target continuous-time design frequency.

**Step 2: Analog Prototype Design (N=3).**
We need a 3rd-order continuous Butterworth filter.
The stable poles for $N=3$ are:
$$ s_k = \Omega_c e^{j\frac{\pi}{6}(2k + 2)} \quad \text{for } k = 1, 2, 3 $$
Calculate the specific poles:
- $k=1: s_1 = 0.7265 e^{j\frac{4\pi}{6}} = 0.7265(-0.5 + j0.866) = -0.3633 + j0.6292$
- $k=2: s_2 = 0.7265 e^{j\pi} = 0.7265(-1) = -0.7265$
- $k=3: s_3 = 0.7265 e^{j\frac{8\pi}{6}} = 0.7265(-0.5 - j0.866) = -0.3633 - j0.6292$

Construct the analog transfer function. Group the complex conjugate pair $(s_1, s_3)$:
$(s - s_1)(s - s_3) = (s - (-0.3633 + j0.6292))(s - (-0.3633 - j0.6292))$
$= (s + 0.3633)^2 + (0.6292)^2 = s^2 + 0.7266s + 0.1320 + 0.3959 = s^2 + 0.7266s + 0.5279$
Now multiply by the real pole $(s - s_2) = (s + 0.7265)$:
$(s + 0.7265)(s^2 + 0.7266s + 0.5279) = s^3 + 0.7266s^2 + 0.5279s + 0.7265s^2 + 0.5279s + 0.3835$
$= s^3 + 1.4531s^2 + 1.0558s + 0.3835$
The numerator is $\Omega_c^3 = (0.7265)^3 \approx 0.3835$.
$$ H_a(s) = \frac{0.3835}{s^3 + 1.4531s^2 + 1.0558s + 0.3835} $$

**Step 3: Apply Bilinear Transform.**
Since we chose $T_s = 2$, the substitution is simply $s = \frac{z-1}{z+1}$.
$$ H(z) = \frac{0.3835}{\left(\frac{z-1}{z+1}\right)^3 + 1.4531\left(\frac{z-1}{z+1}\right)^2 + 1.0558\left(\frac{z-1}{z+1}\right) + 0.3835} $$
Multiply the entire expression (numerator and denominator) by $(z+1)^3$:
Numerator: $0.3835(z+1)^3 = 0.3835(z^3 + 3z^2 + 3z + 1)$
Denominator terms expansion:
1. $(z-1)^3 = z^3 - 3z^2 + 3z - 1$
2. $1.4531(z-1)^2(z+1) = 1.4531(z^2 - 2z + 1)(z+1) = 1.4531(z^3 - z^2 - z + 1)$
3. $1.0558(z-1)(z+1)^2 = 1.0558(z-1)(z^2 + 2z + 1) = 1.0558(z^3 + z^2 - z - 1)$
4. $0.3835(z+1)^3 = 0.3835(z^3 + 3z^2 + 3z + 1)$

Sum the coefficients for each power of $z$ in the denominator:
- For $z^3$: $1 + 1.4531 + 1.0558 + 0.3835 = 3.8924$
- For $z^2$: $-3 - 1.4531 + 1.0558 + 1.1505 = -2.2468$
- For $z^1$: $3 - 1.4531 - 1.0558 + 1.1505 = 1.6416$
- For $z^0$: $-1 + 1.4531 - 1.0558 + 0.3835 = -0.2192$

$$ H(z) = \frac{0.3835(z^3 + 3z^2 + 3z + 1)}{3.8924z^3 - 2.2468z^2 + 1.6416z - 0.2192} $$
Normalize by dividing all coefficients by the leading denominator coefficient ($3.8924$) and convert to negative powers by factoring out $z^3/z^3$:
$$ H(z) = \frac{0.0985 (1 + 3z^{-1} + 3z^{-2} + z^{-3})}{1 - 0.5772z^{-1} + 0.4217z^{-2} - 0.0563z^{-3}} $$
**Physical interpretation:** We have completely synthesized a discrete-time difference equation. The coefficients in the numerator (feedforward) dictate the zeros, while the denominator (feedback) dictates the poles. This digital filter will perfectly exhibit a $-3$ dB cutoff exactly at the digital frequency of $\omega = 0.4\pi$.

### Example 5: Comparative Analysis - Butterworth vs Chebyshev Order
**Problem statement:** For a highly stringent filter application with the following specifications:
- Passband maximum ripple: $A_p = 1$ dB
- Stopband minimum attenuation: $A_s = 50$ dB
- Passband edge frequency: $\Omega_p = 1000$ rad/s
- Stopband edge frequency: $\Omega_s = 1500$ rad/s
Calculate and compare the required order for a Butterworth filter versus a Chebyshev Type I filter.
**Solution:**
**Part A: Butterworth Order:**
Convert specifications: $A_p^2 = 10^{0.1} = 1.2589$. $A_s^2 = 10^5 = 100000$.
$$ N_{butt} \geq \frac{\log_{10}((100000-1)/(1.2589-1))}{2 \log_{10}(1500/1000)} $$
$$ N_{butt} \geq \frac{\log_{10}(99999 / 0.2589)}{2 \log_{10}(1.5)} = \frac{\log_{10}(386245.6)}{2(0.1761)} = \frac{5.5868}{0.3522} = 15.86 $$
Rounding up, the required Butterworth order is **$N = 16$**.

**Part B: Chebyshev Type I Order:**
The order formula for Chebyshev relies on inverse hyperbolic cosines (arcosh):
$$ N_{cheb} \geq \frac{\cosh^{-1}\left(\sqrt{\frac{10^{0.1 A_s} - 1}{10^{0.1 A_p} - 1}}\right)}{\cosh^{-1}(\Omega_s/\Omega_p)} $$
Numerator: $\cosh^{-1}\left(\sqrt{\frac{100000 - 1}{1.2589 - 1}}\right) = \cosh^{-1}(\sqrt{386245.6}) = \cosh^{-1}(621.48)$
Using identity $\cosh^{-1}(x) = \ln(x + \sqrt{x^2 - 1})$:
$\ln(621.48 + \sqrt{621.48^2 - 1}) \approx \ln(1242.96) \approx 7.125$
Denominator: $\cosh^{-1}(1500/1000) = \cosh^{-1}(1.5) = \ln(1.5 + \sqrt{1.5^2 - 1}) = \ln(1.5 + \sqrt{1.25}) \approx 0.962$
$$ N_{cheb} \geq \frac{7.125}{0.962} = 7.40 $$
Rounding up, the required Chebyshev order is **$N = 8$**.

**Physical interpretation & Discussion:** The Butterworth filter requires a massive order of 16 to meet these steep transition requirements because its monotonic polynomial grows slowly. Implementing a 16th-order IIR filter is highly problematic due to extreme sensitivity to coefficient quantization errors, risking instability. 
The Chebyshev filter perfectly meets the exact same strict amplitude specifications but with an order of only 8. By merely allowing a $1$ dB ripple in the passband, we cut the computational complexity exactly in half. This is why Chebyshev and Elliptic filters are heavily favored in DSP hardware implementations.

---
## 7. ENGINEERING APPLICATIONS AND CASE STUDIES
1. **Audio Anti-Aliasing & DAC Reconstruction Filters:**
   When digitizing high-fidelity analog audio (e.g., at 44.1 kHz for CD quality), a strict low-pass filter must be applied before the Analog-to-Digital Converter (ADC) to strictly enforce the Nyquist theorem and prevent aliasing. Often, an analog Elliptic filter is used because it provides the steepest possible roll-off, allowing the filter cutoff to be placed very close to the Nyquist frequency (e.g., flat passband up to 20 kHz while heavily attenuating everything above 22.05 kHz). On the digital playback side (Digital-to-Analog Converter), when oversampling or upsampling, digital IIR filters based on Elliptic or Chebyshev designs provide extremely sharp transition bands at remarkably low computational costs compared to long FIR alternatives.
2. **Biomedical Signal Processing (ECG Filters):**
   Electrocardiogram (ECG) signals operate at very low physiological frequencies (typically 0.05 Hz to 150 Hz). They are highly prone to baseline wander (ultra-low frequency noise from breathing) and high-frequency powerline interference (50/60 Hz). Digital Butterworth bandpass filters are exceptionally useful here because of their completely flat passband. A Chebyshev filter's ripple might severely distort the crucial morphological diagnostic features of the ECG waveform (like the QRS complex or the ST segment). The BLT method is used extensively in biomedical embedded systems (like patient monitors) to design these precise IIR filters.
3. **Digital Control Systems & Channel Equalization:**
   In closed-loop digital control systems, processing delay (latency) directly degrades phase margin and can cause catastrophic system instability. IIR filters inherently provide much lower latency than FIR filters for a given magnitude specification because they require far fewer taps. Thus, PID controllers often integrate IIR low-pass filters to suppress high-frequency sensor noise. Similarly, in digital communications, channels introduce severe phase and amplitude distortion. Inverse filters are used as equalizers. Often, these equalizers are modeled using pole-zero IIR structures derived from robust analog network equivalents using the BLT.

---
## 8. COMMON STUDENT MISCONCEPTIONS AND ERRORS
1. **Misconception:** "The Bilinear Transform introduces aliasing, just like the Impulse Invariance Method."
   * **Instructor Correction:** This is fundamentally false. The BLT was mathematically invented specifically to completely avoid aliasing. It compresses the entire infinite continuous frequency domain $(-\infty, \infty)$ entirely into the finite discrete unit circle domain $(-\pi, \pi)$. There is frequency warping, absolutely, but absolutely no aliasing.
2. **Misconception:** "Pre-warping is an optional fine-tuning step, or is done *after* the digital filter is completely designed to correct its frequencies."
   * **Instructor Correction:** Pre-warping must be the very first mathematical step executed. You mathematically warp the given digital specifications into analog specifications, design the entire analog prototype in that warped domain, and then the final BLT substitution naturally "un-warps" it back into the correct, precise digital frequencies.
3. **Misconception:** "The value of the sampling period $T_s$ in the Bilinear Transform design equations must perfectly match the actual physical sampling time of the hardware."
   * **Instructor Correction:** When using the BLT for indirect design, $T_s$ is merely a mathematical dummy variable. If you use the pre-warping formula with a specific $T_s$ value and then apply the BLT substitution with the exact same $T_s$ value, the variable completely cancels itself out algebraically. Choosing $T_s = 2$ is a common DSP convention simply because it removes the fraction from the substitution $s = \frac{2}{T_s} \frac{z-1}{z+1}$, yielding $s = \frac{z-1}{z+1}$.
4. **Misconception:** "Higher order filters are universally better because they have sharper cutoffs."
   * **Instructor Correction:** While higher orders undeniably provide steeper roll-offs, they introduce severe phase non-linearities, higher group delay, and are highly susceptible to finite-word-length quantization errors (coefficient truncation). In fixed-point DSP processors, high-order IIR filters can easily become unstable.
5. **Misconception:** "Chebyshev and Elliptic filters have linear phase."
   * **Instructor Correction:** Only strictly symmetric FIR filters can achieve perfectly linear phase. All causal IIR filters inherently have non-linear phase. Butterworth is the most linear of the IIR family in the passband, while Elliptic has highly non-linear, distorted phase, especially near the cutoff transition.
6. **Misconception:** "The poles of an analog Butterworth filter lie exactly on the $j\Omega$ imaginary axis."
   * **Instructor Correction:** The stable Butterworth poles lie specifically on a semi-circle strictly within the Left Half Plane (LHP). The transfer function has absolutely no finite zeros on the $j\Omega$ axis. Only Chebyshev Type II and Elliptic filters possess zeros on the $j\Omega$ axis to create stopband nulls.
7. **Misconception:** "The Impulse Invariance Method can be used effectively to design highpass digital filters if the sampling rate is high enough."
   * **Instructor Correction:** IIM fundamentally maps analog spectra by aliasing. Ideal highpass analog filters inherently have infinite bandwidth (passing all frequencies up to infinity), which guarantees infinite aliasing regardless of the sampling rate. IIM is strictly reserved for bandlimited lowpass or narrow bandpass filters.

---
## 9. CONNECTIONS TO OTHER LECTURES
* **Builds on:** 
  - Lecture 4 (The $z$-Transform and Region of Convergence): Essential for understanding stability inside the unit circle.
  - Lecture 6 (Frequency Response of LTI Systems): Needed to comprehend magnitude squared evaluations.
  - Lecture 8 (Analog Filter Basics): Prerequisite knowledge of Laplace transforms and continuous-time differential equations.
* **Prepares for:** 
  - Lecture 13 (Realization Structures for IIR Filters): We will learn how to implement the difference equations derived here into Direct Form I, Direct Form II, Cascade, and Parallel block structures.
  - Lecture 15 (FIR Filter Design using Windowing): Will provide a contrast to IIR, showing how to achieve perfectly linear phase at the cost of high filter order.
  - Lecture 18 (Finite Word Length Effects): Understanding the precise pole locations derived in this lecture is absolutely critical for analyzing how coefficient quantization in hardware might push a pole outside the unit circle, causing catastrophic instability.

---
## 10. EXAMINATION QUESTIONS

### 10.1 Short Answer Questions
**Q1.** Why is pre-warping mathematically necessary when designing digital filters using the Bilinear Transform approach?
**Model Answer:** The BLT employs a highly non-linear mapping (specifically, an arctangent function) between continuous analog and discrete digital frequencies. High analog frequencies are severely compressed into a finite digital band. Pre-warping mathematically stretches the initial digital specifications in the exact opposite proportion so that the subsequent BLT step will map them perfectly back to the desired target digital frequencies.

**Q2.** State the primary mathematical difference in the magnitude response characteristics between Butterworth and Chebyshev Type I filters.
**Model Answer:** Butterworth filters are defined to be "maximally flat," possessing absolutely no ripples in either the passband or the stopband, with a monotonic transition. Chebyshev Type I filters purposefully introduce bounded, equiripple fluctuations strictly within the passband in order to achieve a much steeper, sharper transition band for an identical filter order.

**Q3.** Why is the Impulse Invariance Method inherently prohibited for high-pass digital filter design?
**Model Answer:** The IIM maps analog poles to digital poles through direct time-domain sampling of the impulse response, which inherently causes spectral folding (aliasing) in the frequency domain. High-pass continuous analog filters contain infinite high-frequency energy. Under time sampling, all of this infinite energy would severely alias down into the digital baseband, completely destroying the intended high-pass filter characteristics.

**Q4.** Describe the exact geometric location of the roots (poles) of the squared magnitude response of an analog Butterworth filter on the complex $s$-plane.
**Model Answer:** The full $2N$ poles of the theoretical squared magnitude response lie symmetrically evenly spaced on a full circle of radius $\Omega_c$ centered at the origin in the complex $s$-plane. To form a stable, causal filter, only the $N$ poles located strictly in the Left Half Plane (LHP, negative real part) are selected.

**Q5.** In the Bilinear Transform, what specific continuous-time domain mathematically maps to the digital unit circle ($|z|=1$)?
**Model Answer:** The entire continuous imaginary axis ($j\Omega$ from $-\infty$ to $+\infty$) in the $s$-plane maps exactly and uniquely to the continuous boundary of the unit circle in the $z$-plane.

### 10.2 Long Answer / Numerical Problems
**Problem 1.** Calculate the required integer filter order $N$ for an analog Butterworth filter given the following specifications: Passband maximum attenuation of $2$ dB at a frequency of $20$ rad/s. Stopband minimum attenuation of $50$ dB at a frequency of $60$ rad/s. Show all conversion steps.
**Solution Highlights:** 
First, convert dB to linear squared ratios: $A_p^2 = 10^{2/10} = 10^{0.2} = 1.5849$. $A_s^2 = 10^{50/10} = 10^5 = 100000$.
Apply the formula:
$$ N \geq \frac{\log_{10}((100000-1)/(1.5849-1))}{2 \log_{10}(60/20)} $$
Numerator: $\log_{10}(99999 / 0.5849) = \log_{10}(170967.6) \approx 5.2329$
Denominator: $2 \log_{10}(3) \approx 2(0.4771) = 0.9542$
$N \geq 5.2329 / 0.9542 = 5.484$. 
Because the order must be an integer, round up to $N = 6$.

**Problem 2.** Design a first-order discrete-time digital high-pass filter with a cutoff frequency of $\omega_c = \pi/4$ using the Bilinear Transform method. The normalized prototype analog highpass filter is given as $H_a(s) = \frac{s}{s + \Omega_c}$. Use $T_s = 2$.
**Solution Highlights:**
Prewarp the digital cutoff frequency: $\Omega_c = \frac{2}{2}\tan((\pi/4)/2) = \tan(\pi/8) \approx 0.4142$ rad/s.
Substitute into prototype: $H_a(s) = \frac{s}{s + 0.4142}$. 
Apply BLT substitution $s = \frac{z-1}{z+1}$ (since $T_s = 2$).
$$ H(z) = \frac{\frac{z-1}{z+1}}{\frac{z-1}{z+1} + 0.4142} $$
Multiply numerator and denominator by $(z+1)$:
$$ H(z) = \frac{z-1}{(z-1) + 0.4142(z+1)} = \frac{z-1}{1.4142z - 0.5858} $$
Normalize denominator leading coefficient to 1:
$$ H(z) = \frac{0.7071 - 0.7071z^{-1}}{1 - 0.4142z^{-1}} $$

**Problem 3.** Derive the crucial frequency warping relationship $\Omega = \frac{2}{T_s}\tan(\frac{\omega}{2})$ starting fundamentally from the Bilinear Transform algebraic definition.
**Solution Highlights:** 
Start strictly with the BLT mapping: $s = \frac{2}{T_s}\frac{z-1}{z+1}$. 
Substitute the frequency axis definitions $s=j\Omega$ and $z=e^{j\omega}$.
$$ j\Omega = \frac{2}{T_s}\frac{e^{j\omega}-1}{e^{j\omega}+1} $$
Factor out half-angles $e^{j\omega/2}$ in both numerator and denominator.
$$ = \frac{2}{T_s} \frac{e^{j\omega/2}(e^{j\omega/2} - e^{-j\omega/2})}{e^{j\omega/2}(e^{j\omega/2} + e^{-j\omega/2})} $$
Apply Euler's sine and cosine identities. The numerator term becomes $2j\sin(\omega/2)$ and the denominator term becomes $2\cos(\omega/2)$.
Resulting expression: $j\Omega = \frac{2}{T_s} \frac{2j\sin(\omega/2)}{2\cos(\omega/2)} = j\frac{2}{T_s}\tan(\omega/2)$.
Divide by $j$ to yield the final warping equation.

**Problem 4.** Determine the exact algebraic locations of the stable poles for a 3rd-order ($N=3$) analog Butterworth filter with a cutoff frequency $\Omega_c = 2$ rad/s.
**Solution Highlights:** 
The general formula is $s_k = \Omega_c e^{j\frac{\pi}{2N}(2k+N-1)}$ for $k=1,2,3$.
Substitute $\Omega_c=2$, $N=3$: $s_k = 2 e^{j\frac{\pi}{6}(2k+2)}$.
For $k=1$: $\theta = 4\pi/6 = 120^\circ$. $s_1 = 2(\cos 120^\circ + j\sin 120^\circ) = 2(-0.5 + j0.866) = -1 + j1.732$.
For $k=2$: $\theta = 6\pi/6 = 180^\circ$. $s_2 = 2(\cos 180^\circ + j\sin 180^\circ) = 2(-1) = -2$.
For $k=3$: $\theta = 8\pi/6 = 240^\circ$. $s_3 = 2(\cos 240^\circ + j\sin 240^\circ) = 2(-0.5 - j0.866) = -1 - j1.732$.

### 10.3 True/False with Detailed Justification
1. **True/False:** The Bilinear Transform inherently introduces frequency aliasing into the designed digital filter.
   * **Answer:** False. The BLT utilizes a continuous conformal mapping that maps the entire infinite analog frequency range directly to the finite unit circle boundary without any overlap or folding.
2. **True/False:** For a precisely identical set of magnitude specifications, an Elliptic filter will consistently yield a lower or equal order compared to a Butterworth filter.
   * **Answer:** True. By mathematically permitting and distributing equiripple errors into both the passband and stopband simultaneously, the Elliptic polynomial achieves the absolute sharpest theoretical transition roll-off.
3. **True/False:** In the Impulse Invariance Method, the mapping of the complex poles is defined by $z = e^{s T_s}$.
   * **Answer:** True. This is the fundamental, derived mathematical mapping resulting from discretely sampling the continuous time-domain exponential functions of the impulse response.
4. **True/False:** High-order analog Butterworth filters exhibit a perfectly linear phase response within their designated passband.
   * **Answer:** False. It is mathematically impossible for any causal IIR filter (continuous or digital) to exhibit perfectly linear phase. Butterworth is merely the most linear among IIR types, but it is still non-linear.
5. **True/False:** The specific numerical choice of the parameter $T_s$ alters the final coefficient values of a digital filter designed via the Bilinear Transform.
   * **Answer:** False. As long as the identical $T_s$ value is utilized in both the initial pre-warping phase and the subsequent mapping substitution phase, it will algebraically cancel out entirely, leaving the final transfer function invariant.
6. **True/False:** Under the Bilinear Transform, all stable continuous-time analog poles located in the Left Half Plane will map strictly to locations inside the unit circle.
   * **Answer:** True. The mathematical mapping ensures that for any $s = \sigma + j\Omega$ where $\sigma < 0$, the resulting magnitude $|z|$ is rigorously strictly less than 1.

---
## 11. KEY FORMULAS REFERENCE

| DSP Concept / Technique | Rigorous Mathematical Formula |
| :--- | :--- |
| **Butterworth Squared Magnitude Response** | $|H_a(j\Omega)|^2 = \frac{1}{1 + (\Omega/\Omega_c)^{2N}}$ |
| **Butterworth Stable Pole Locations** | $s_k = \Omega_c e^{j\frac{\pi}{2N}(2k + N - 1)} \quad \text{for } k=1, 2, \dots, N$ |
| **Exact Order Calculation (Butterworth)**| $N \geq \frac{\log_{10}((A_s^2 - 1)/(A_p^2 - 1))}{2 \log_{10}(\Omega_s/\Omega_p)}$ |
| **Chebyshev Type I Magnitude Response** | $|H(j\Omega)|^2 = \frac{1}{1 + \epsilon^2 C_N^2\left(\frac{\Omega}{\Omega_p}\right)}$ |
| **Chebyshev Polynomial Recursion** | $C_N(x) = 2x C_{N-1}(x) - C_{N-2}(x)$ |
| **Impulse Invariance Time-Domain Mapping** | $h[n] = T_s h_a(nT_s)$ |
| **Impulse Invariance Pole Mapping** | $z_k = e^{s_k T_s}$ |
| **Bilinear Transform Substitution (BLT)** | $s = \frac{2}{T_s} \frac{1 - z^{-1}}{1 + z^{-1}} = \frac{2}{T_s} \frac{z - 1}{z + 1}$ |
| **Inverse BLT Mapping (z to s)** | $z = \frac{1 + (T_s/2)s}{1 - (T_s/2)s}$ |
| **Non-Linear Frequency Warping Equation** | $\Omega = \frac{2}{T_s} \tan\left(\frac{\omega}{2}\right)$ |

---
## 12. FURTHER READING AND REFERENCES
* **Proakis, J. G., & Manolakis, D. G.** (2006). *Digital Signal Processing: Principles, Algorithms, and Applications* (4th Ed.). Pearson Education. (Refer strictly to Chapter 10: Design of Digital Filters for rigorous IIR proofs).
* **Oppenheim, A. V., & Schafer, R. W.** (2009). *Discrete-Time Signal Processing* (3rd Ed.). Prentice Hall. (Chapter 7 provides an unparalleled, exhaustive mathematical treatment of Filter Design Techniques).
* **Haykin, S., & Van Veen, B.** (2002). *Signals and Systems* (2nd Ed.). John Wiley & Sons. (This text provides deep physical and mathematical insight into the continuous-time analog prototypes).
* **MATLAB DSP Toolbox Documentation:** Instructors and students are highly encouraged to review the official documentation for the `butter`, `cheby1`, `cheby2`, `ellip`, and `bilinear` software functions for practical implementation examples and syntax.
</Faculty Notes — Lecture 12: IIR Filter Design — Analog Prototypes & Bilinear Transform>'''

import os
import pathlib

# Ensure directory exists
directory = r'C:\Users\sriph\Downloads\DSP\faculty_notes'
pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

file_path = os.path.join(directory, 'lecture_12_faculty.md')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Successfully wrote {len(content.splitlines())} lines to {file_path}")
