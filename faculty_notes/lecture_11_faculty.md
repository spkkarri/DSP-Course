<Faculty Notes — Lecture 11: FIR Design — Parks-McClellan & Frequency Sampling>

## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---

## PREFACE FOR FACULTY

The Parks-McClellan (PM) algorithm is arguably the crown jewel of FIR filter design. As instructors, it is essential to convey not just the algorithmic mechanics but the profound beauty of optimal filter design in the Chebyshev (minimax) sense. While the frequency sampling method is conceptually simpler and easier to implement directly via the IDFT, it is significantly less flexible and often sub-optimal in terms of filter order compared to PM. 


**How to teach this lecture:**

Start by grounding the students in the intuitive Frequency Sampling method. They already know the DFT/IDFT, so this will build confidence. Then, demonstrate its flaw: the severe rippling between sample points (analogous to the Gibbs phenomenon). This perfectly motivates the need for an optimal approach. Introduce the Chebyshev approximation problem and build up to the Alternation Theorem. Spend ample time on the Alternation Theorem; it is a profound result that requires intuition before math. Finally, bring it all together by comparing the Window Method, Frequency Sampling, and Parks-McClellan.


**Common student difficulties:**

- Grasping the minimax criterion: Students are used to least-squares error minimization (like in the Window method). The concept of minimizing the *maximum* error (Chebyshev norm) is often new.

- The Alternation Theorem: The idea of "free parameters" ($L$) and "alternating error extrema" ($L+1$ or $L+2$) is abstract. Draw many pictures of equiripple responses.

- Filter Types: Remembering the constraints for Type I, II, III, and IV filters. Emphasize *why* these constraints exist based on symmetry and zeros at $\omega = 0$ or $\omega = \pi$.

- Understanding why the frequency response has ripples between sampled points in the Frequency Sampling method.

- Realizing that Parks-McClellan is iterative and doesn't produce an explicit formula for the coefficients.


**Suggested demos:**

- Run a live MATLAB or Python script comparing a 31-tap filter designed using `fir1` (window) vs `firls` (least squares) vs `firpm` (Parks-McClellan). Show how PM achieves tighter specs for the same order, or requires a lower order for the same specs.

- Show the Frequency Sampling method on screen and visually adjust the transition sample to see the sidelobes change dynamically.


---

## 1. LEARNING OBJECTIVES

By the end of this lecture, students will be able to:

1. **Apply** the frequency sampling method to design linear-phase FIR filters by specifying desired frequency domain samples and computing the IDFT.

2. **Optimize** transition band samples in the frequency sampling method to minimize stopband sidelobes.

3. **Differentiate** between Type I, II, III, and IV linear-phase FIR filters, and **justify** their inherent zero constraints at DC and Nyquist frequencies.

4. **Formulate** the FIR filter design problem as a Chebyshev (minimax) approximation problem using a weighted error function.

5. **Analyze** the optimality of a given FIR filter response using the Alternation Theorem, determining if it satisfies the required number of error alternations.

6. **Estimate** the required filter order for a Parks-McClellan design using Kaiser's empirical formula based on passband/stopband ripple and transition width.

7. **Compare** and **contrast** FIR and IIR filters across multiple dimensions including stability, phase linearity, and computational complexity.

8. **Synthesize** a holistic understanding of how different FIR design methodologies balance trade-offs.


---

## 2. PREREQUISITE KNOWLEDGE REVIEW

Before embarking on this lecture, students must be comfortable with the following concepts:


**1. Linear Phase Conditions:**

An FIR filter with impulse response $h[n]$ of length $N$ has strictly linear phase if it is either symmetric:

$h[n] = h[N - 1 - n]$

or anti-symmetric:

$h[n] = -h[N - 1 - n]$

The phase response takes the form $\angle H(e^{j\omega}) = -\alpha \omega + \beta$, where $\alpha = \frac{N-1}{2}$.


**2. The Discrete Fourier Transform (DFT) and IDFT:**

The relationship between a finite-duration discrete-time signal and its frequency-domain samples.

$H[k] = \sum_{n=0}^{N-1} h[n] e^{-j \frac{2\pi}{N} k n}$

$h[n] = \frac{1}{N} \sum_{k=0}^{N-1} H[k] e^{j \frac{2\pi}{N} k n}$


**3. The Window Method for FIR Design:**

Students should know that simply truncating an ideal impulse response $h_d[n]$ leads to the Gibbs phenomenon (large ripples near the band edges). The window method mitigates this but does not minimize the maximum error.


**4. Frequency Response of Discrete-Time Systems:**

$H(e^{j\omega}) = \sum_{n=-\infty}^{\infty} h[n] e^{-j\omega n}$

Understanding how this continuous function of $\omega$ behaves for discrete sequences.


**5. Polynomial Roots and the Fundamental Theorem of Algebra:**

A polynomial of degree $N$ has exactly $N$ roots (some of which may be complex or repeated). A non-zero polynomial of degree $N$ cannot have more than $N$ roots. This fact is crucial for the proof of uniqueness in the Alternation Theorem.


---

## 3. HISTORICAL AND MOTIVATIONAL CONTEXT

**Historical Context:**

In the early 1970s, as digital signal processing was emerging from its infancy, designing filters that strictly met required specifications was a tedious, trial-and-error process. James McClellan, a graduate student at Rice University, and his advisor Thomas Parks, revolutionized the field in 1972. They recognized that FIR filter design could be mapped perfectly to the Chebyshev polynomial approximation problem, a well-known mathematical problem in approximation theory. By adapting the Remez exchange algorithm (a numerical technique from the 1930s by Evgeny Remez) to this specific problem, they created the Parks-McClellan algorithm. This algorithm became an instant classic, widely implemented in IEEE signal processing libraries.


**Why does EEE need this?**

Electrical and Electronics Engineers design systems that require precise spectral separation without phase distortion. For example:

- **Audio Crossover Networks:** Require perfect phase linearity so that low and high frequencies recombine without destructive interference at the crossover point.

- **Data Communication (Modems/SDRs):** Pulse shaping filters (like Root-Raised Cosine) must be strictly linear phase to prevent intersymbol interference (ISI).

- **Biomedical Instrumentation:** ECG and EEG signal processing require filters that do not distort the morphological shape of the pulses (e.g., the QRS complex), mandating exact linear phase FIR filters.

- **Radar Systems:** Precise delay matching is required, which relies on the constant group delay offered by optimal FIR filters.


---

## 4. THEORETICAL FOUNDATIONS

### 4.1 Frequency Sampling Method

The frequency sampling method takes a direct approach: if we want a specific frequency response, let's just sample that desired response at discrete frequencies and use the Inverse DFT to find the filter coefficients.


Let the desired continuous frequency response be $H_d(e^{j\omega})$. We sample this at $N$ evenly spaced points in the interval $[0, 2\pi)$:

$\omega_k = \frac{2\pi k}{N} \quad \text{for } k = 0, 1, \dots, N-1$


The sampled frequency response is:

$H[k] = H_d\left(e^{j\frac{2\pi k}{N}}\right)$


To find the time-domain impulse response $h[n]$, we compute the $N$-point IDFT of $H[k]$:

$h[n] = \frac{1}{N} \sum_{k=0}^{N-1} H[k] e^{j \frac{2\pi}{N} k n} \quad \text{for } n = 0, 1, \dots, N-1$


**Interpolation Formula:**

While the filter exactly matches $H_d(e^{j\omega})$ at the sample frequencies $\omega_k$, what happens *between* the samples? The actual continuous frequency response of the designed filter is given by the interpolation formula:


$H(e^{j\omega}) = \sum_{n=0}^{N-1} h[n] e^{-j\omega n}$

Substituting the IDFT expression for $h[n]$:

$H(e^{j\omega}) = \sum_{n=0}^{N-1} \left( \frac{1}{N} \sum_{k=0}^{N-1} H[k] e^{j \frac{2\pi}{N} k n} \right) e^{-j\omega n}$

Interchanging the summations:

$H(e^{j\omega}) = \frac{1}{N} \sum_{k=0}^{N-1} H[k] \sum_{n=0}^{N-1} e^{-j\left(\omega - \frac{2\pi k}{N}\right) n}$


The inner sum is a finite geometric series:

$\sum_{n=0}^{N-1} e^{-j\theta n} = \frac{1 - e^{-j\theta N}}{1 - e^{-j\theta}} = e^{-j\theta \frac{N-1}{2}} \frac{\sin(\theta N / 2)}{\sin(\theta / 2)}$

where $\theta = \omega - \frac{2\pi k}{N}$.


Thus, the continuous frequency response is:

$H(e^{j\omega}) = \frac{1}{N} \sum_{k=0}^{N-1} H[k] e^{-j\left(\omega - \frac{2\pi k}{N}\right) \frac{N-1}{2}} \frac{\sin\left(\frac{N}{2}(\omega - \frac{2\pi k}{N})\right)}{\sin\left(\frac{1}{2}(\omega - \frac{2\pi k}{N})\right)}$


This shows that $H(e^{j\omega})$ is a linear combination of shifted Dirichlet kernels (periodic sinc functions). Because the Dirichlet kernel has large sidelobes, $H(e^{j\omega})$ can exhibit significant rippling between the sample points, especially near discontinuities in $H[k]$ (i.e., the transition band).


### 4.2 Transition Sample Optimization

To reduce the large ripples (sidelobes) caused by abrupt changes in $H[k]$, we can introduce transition samples. Instead of jumping directly from a passband value of 1 to a stopband value of 0, we insert an intermediate value, say $T_1$, in the transition band.


For example, a lowpass filter specification might look like:

$H[k] = \{1, 1, 1, T_1, 0, 0, \dots, 0, T_1, 1, 1\}$


By treating $T_1$ as a variable, we gain a degree of freedom. We can use numerical optimization (often linear programming) to find the value of $T_1$ that minimizes the maximum sidelobe level in the stopband.

- No transition sample: Stopband attenuation might be $\approx -21$ dB.

- 1 optimized transition sample (e.g., $T_1 = 0.39$): Attenuation improves to $\approx -40$ dB.

- 2 optimized transition samples (e.g., $T_1 = 0.59, T_2 = 0.11$): Attenuation improves to $\approx -60$ dB.

The tradeoff is a wider transition band.


### 4.3 Type I, II, III, and IV FIR Filters

Linear phase FIR filters are categorized based on their symmetry and length $N$. Let $h[n]$ be defined for $n = 0, 1, \dots, N-1$. The center of symmetry is $\alpha = (N-1)/2$.


**Type I:** Symmetric ($h[n] = h[N-1-n]$), Odd $N$.

- $\alpha$ is an integer.

- The frequency response can be written as:

  $H(e^{j\omega}) = e^{-j\omega\alpha} \sum_{k=0}^{(N-1)/2} a[k] \cos(\omega k)$

- **Constraints:** None. Can be used for any filter type (LP, HP, BP, BS).


**Type II:** Symmetric ($h[n] = h[N-1-n]$), Even $N$.

- $\alpha$ is a half-integer.

- The frequency response is:

  $H(e^{j\omega}) = e^{-j\omega\alpha} \sum_{k=1}^{N/2} b[k] \cos\left(\omega (k - 1/2)\right)$

- **Constraint at $\omega=\pi$:** If we evaluate the sum at $\omega=\pi$, every term is $\cos(\pi(k-0.5)) = \cos((k-0.5)\pi)$, which is zero for all integers $k$. Thus, $H(e^{j\pi}) = 0$.

- **Implication:** A Type II filter **cannot** be used to design a Highpass or Bandstop filter, as it forces a zero at the Nyquist frequency.


**Type III:** Anti-symmetric ($h[n] = -h[N-1-n]$), Odd $N$.

- $\alpha$ is an integer. Furthermore, $h[\alpha] = -h[\alpha] \implies h[\alpha] = 0$.

- The frequency response is:

  $H(e^{j\omega}) = e^{-j\omega\alpha} e^{j\pi/2} \sum_{k=1}^{(N-1)/2} c[k] \sin(\omega k)$

- **Constraints:** At $\omega=0$, $\sin(0)=0 \implies H(e^{j0}) = 0$. At $\omega=\pi$, $\sin(\pi k)=0 \implies H(e^{j\pi}) = 0$.

- **Implication:** Must have zeros at both DC and Nyquist. Can only be used for Bandpass filters or differentiators/Hilbert transformers.


**Type IV:** Anti-symmetric ($h[n] = -h[N-1-n]$), Even $N$.

- $\alpha$ is a half-integer.

- The frequency response is:

  $H(e^{j\omega}) = e^{-j\omega\alpha} e^{j\pi/2} \sum_{k=1}^{N/2} d[k] \sin\left(\omega (k - 1/2)\right)$

- **Constraint at $\omega=0$:** $\sin(0) = 0 \implies H(e^{j0}) = 0$.

- **Implication:** Cannot be used for Lowpass filters. Good for Highpass or differentiators.


### 4.4 The Chebyshev Approximation Problem

The Parks-McClellan algorithm formulates FIR design as a minimax optimization. Let the amplitude response of a zero-phase FIR filter be $A(\omega)$. We desire it to approximate an ideal response $H_d(\omega)$ over a set of frequency bands $F$ (passbands and stopbands, excluding transition bands).


We define a weighted error function:

$E(\omega) = W(\omega) [H_d(\omega) - A(\omega)]$

where $W(\omega) > 0$ is a weighting function that allows us to specify relative error tolerances. For example, making $W(\omega)$ larger in the stopband forces the algorithm to achieve smaller ripples there.


The Chebyshev (minimax) problem is to find the filter coefficients that minimize the maximum absolute error:

$\min_{h[n]} \max_{\omega \in F} |E(\omega)|$


### 4.5 The Alternation Theorem

This is the mathematical cornerstone of the PM algorithm.


**Theorem Statement:**

Let $A(\omega)$ be expressed as a linear combination of $L$ basis functions (e.g., $L$ cosine terms). $A(\omega)$ is the unique, optimal, minimax approximation to $H_d(\omega)$ on $F$ if and only if the error function $E(\omega)$ exhibits at least $L+1$ alternating extremal frequencies in $F$.


That is, there must exist $L+1$ frequencies $\omega_1 < \omega_2 < \dots < \omega_{L+1}$ such that:

1. $E(\omega_i) = -E(\omega_{i+1})$

2. $|E(\omega_i)| = \max_{\omega \in F} |E(\omega)| = \delta$


For a Type I filter, the amplitude response is $A(\omega) = \sum_{k=0}^{(N-1)/2} a[k] \cos(\omega k)$.

Here, the number of free parameters (basis functions) is $L = \frac{N-1}{2} + 1 = \frac{N+1}{2}$.

Therefore, an optimal Type I filter must have at least $L+1 = \frac{N+3}{2}$ alternations.


**Physical Meaning:** The optimal filter is "equiripple." The error bounces between $+\delta$ and $-\delta$ the maximum possible number of times.


### 4.6 The Remez Exchange Algorithm

How do we find this optimal filter? We use the iterative Remez Exchange Algorithm:

1. **Guess:** Pick $L+1$ initial extremal frequencies $\omega_i$.

2. **Solve:** Set up a system of equations: $W(\omega_i) [H_d(\omega_i) - A(\omega_i)] = (-1)^i \delta$ for $i=1, \dots, L+1$. Solve this linear system for the unknown coefficients $a[k]$ and the error magnitude $\delta$.

3. **Evaluate:** Use the calculated $a[k]$ to evaluate $E(\omega)$ on a very dense grid over $F$.

4. **Exchange:** Find the actual local maxima of $|E(\omega)|$. If the largest error on the grid exceeds $\delta$, replace the old guess frequencies $\omega_i$ with the new peak locations, maintaining the alternating sign property.

5. **Iterate:** Repeat steps 2-4 until the extremal frequencies stop changing. The algorithm is guaranteed to converge to the unique optimal solution.


### 4.7 Filter Order Estimation Formulas

Before running the PM algorithm, we must provide the filter order $N$. How do we know what $N$ is required to meet our specs (passband ripple $\delta_p$, stopband ripple $\delta_s$, transition width $\Delta f = \frac{f_s - f_p}{f_{samp}}$)?


**Kaiser's Formula:**

$N \approx \frac{-20 \log_{10}(\sqrt{\delta_p \delta_s}) - 13}{14.6 \Delta f} + 1$

(Note: $\delta_p$ and $\delta_s$ must be in linear scale, not dB).


### 4.8 FIR vs IIR Comparison

| Feature | FIR Filters | IIR Filters |

| :--- | :--- | :--- |

| **Phase Linearity** | Can be exactly linear (constant group delay) | Highly non-linear, especially near band edges |

| **Stability** | Inherently stable (all poles at $z=0$) | Conditionally stable (poles must be inside $|z|=1$) |

| **Filter Order** | High (often 50-200) | Low (often 4-10) for same magnitude specs |

| **Implementation** | Efficiently realized via FFT/overlap-add | Direct form structures, prone to limit cycles |

| **Memory/Delay** | High memory requirement, high latency | Low memory, low latency |

| **Design Complexity** | Iterative algorithms (PM) required for optimal | Closed-form formulas via analog prototypes (Butterworth) |

| **Finite Word Length** | Very robust to coefficient quantization | Highly sensitive; poles can move outside unit circle |


---

## 5. COMPLETE PROOFS AND DERIVATIONS

### Proof: Necessity of Zero Constraints in FIR Types

**Theorem:** A Type II FIR filter must have a zero at $\omega = \pi$.

**Proof:**

By definition, a Type II filter has even length $N$ and symmetric coefficients $h[n] = h[N-1-n]$.

The frequency response is $H(e^{j\omega}) = \sum_{n=0}^{N-1} h[n] e^{-j\omega n}$.

Evaluate at $\omega = \pi$:

$H(e^{j\pi}) = \sum_{n=0}^{N-1} h[n] e^{-j\pi n} = \sum_{n=0}^{N-1} h[n] (-1)^n$

Let $N = 2M$ where $M$ is an integer. We split the sum into the first half and the second half:

$H(e^{j\pi}) = \sum_{n=0}^{M-1} h[n] (-1)^n + \sum_{n=M}^{2M-1} h[n] (-1)^n$

In the second sum, let $m = 2M - 1 - n$. As $n$ goes from $M$ to $2M-1$, $m$ goes from $M-1$ down to $0$.

$H(e^{j\pi}) = \sum_{n=0}^{M-1} h[n] (-1)^n + \sum_{m=0}^{M-1} h[2M-1-m] (-1)^{2M-1-m}$

Using the symmetry property $h[2M-1-m] = h[m]$:

$H(e^{j\pi}) = \sum_{n=0}^{M-1} h[n] (-1)^n + \sum_{m=0}^{M-1} h[m] (-1)^{2M-1} (-1)^{-m}$

Since $2M-1$ is odd, $(-1)^{2M-1} = -1$.

Also, $(-1)^{-m} = (-1)^m$.

Therefore:

$H(e^{j\pi}) = \sum_{n=0}^{M-1} h[n] (-1)^n - \sum_{m=0}^{M-1} h[m] (-1)^m = 0$

Thus, $H(e^{j\pi}) = 0$ is mathematically guaranteed. $\blacksquare$


### Proof Concept: Why Optimal Equiripple implies Minimum Order

Suppose we have an equiripple filter $H_1$ of order $N$ that exactly meets the specifications with maximum error $\delta$. Suppose there exists another filter $H_2$ of order $N-1$ that also meets the specifications with error $\le \delta$.

If we construct the difference polynomial $D(\omega) = H_1(\omega) - H_2(\omega)$, it is a polynomial of degree $N$.

Because $H_1$ alternates $L+1$ times between $+\delta$ and $-\delta$, and $H_2$ is strictly bounded by $\delta$, the difference $D(\omega)$ must cross zero at least $L$ times.

However, a trigonometric polynomial of degree $N-1$ (which determines the order of $H_2$) cannot have $L$ zeros unless it is identically zero (Fundamental Theorem of Algebra for polynomials). This creates a contradiction, proving that no filter of lower order can achieve the same or better maximum error. Thus, the equiripple filter is the unique minimum-order filter. $\blacksquare$


### Proof: Derivation of Interpolation Formula for Frequency Sampling
**Theorem:** The continuous frequency response $H(e^{j\omega})$ is an interpolation of the sampled points $H[k]$.

**Proof:**

$H(e^{j\omega}) = \sum_{n=0}^{N-1} h[n] e^{-j\omega n}$

Substitute $h[n] = \frac{1}{N} \sum_{k=0}^{N-1} H[k] e^{j \frac{2\pi k n}{N}}$:

$H(e^{j\omega}) = \sum_{n=0}^{N-1} \left( \frac{1}{N} \sum_{k=0}^{N-1} H[k] e^{j \frac{2\pi k n}{N}} \right) e^{-j\omega n}$

$H(e^{j\omega}) = \frac{1}{N} \sum_{k=0}^{N-1} H[k] \sum_{n=0}^{N-1} e^{-j(\omega - \frac{2\pi k}{N})n}$

The inner sum is a geometric progression. Let $\theta = \omega - \frac{2\pi k}{N}$:

$\sum_{n=0}^{N-1} e^{-j\theta n} = \frac{1 - e^{-j\theta N}}{1 - e^{-j\theta}} = \frac{e^{-j\theta N/2}(e^{j\theta N/2} - e^{-j\theta N/2})}{e^{-j\theta/2}(e^{j\theta/2} - e^{-j\theta/2})}$

$= e^{-j\theta \frac{N-1}{2}} \frac{\sin(\theta N/2)}{\sin(\theta/2)}$

Substitute $\theta$ back in:

$H(e^{j\omega}) = \frac{1}{N} \sum_{k=0}^{N-1} H[k] e^{-j(\omega - \frac{2\pi k}{N})\frac{N-1}{2}} \frac{\sin(\frac{N}{2}(\omega - \frac{2\pi k}{N}))}{\sin(\frac{1}{2}(\omega - \frac{2\pi k}{N}))}$

This formula demonstrates that $H(e^{j\omega})$ perfectly equals $H[k]$ when $\omega = 2\pi k / N$, but ripples between these points according to the Dirichlet kernel. $\blacksquare$


---

## 6. WORKED EXAMPLES (MINIMUM 5 — fully solved)

### Example 1: Basic Frequency Sampling Design
**Problem statement:** Design a 7-point ($N=7$) FIR lowpass filter using the frequency sampling method. The desired frequency samples are: $H[0]=1, H[1]=1, H[2]=0, H[3]=0, H[4]=0, H[5]=0, H[6]=1$.

Compute the impulse response $h[n]$ for $n=0,1,2,3$.


**Solution:**

We use the IDFT formula: $h[n] = \frac{1}{N} \sum_{k=0}^{N-1} H[k] e^{j \frac{2\pi}{N} k n}$.

Here $N=7$. The non-zero values of $H[k]$ are at $k=0, 1, 6$.

Notice that $H[6] = H[N-1] = H[-1]$, which ensures conjugate symmetry.

$h[n] = \frac{1}{7} \left( H[0] + H[1] e^{j \frac{2\pi}{7} (1) n} + H[6] e^{j \frac{2\pi}{7} (6) n} \right)$

Since $e^{j \frac{2\pi}{7} 6 n} = e^{-j \frac{2\pi}{7} n}$:

$h[n] = \frac{1}{7} \left( 1 + e^{j \frac{2\pi}{7} n} + e^{-j \frac{2\pi}{7} n} \right)$

$h[n] = \frac{1}{7} \left( 1 + 2 \cos\left(\frac{2\pi}{7} n\right) \right)$


Now, evaluate for specific $n$:

- $h[0] = \frac{1}{7} (1 + 2 \cos(0)) = \frac{3}{7} \approx 0.4286$

- $h[1] = \frac{1}{7} (1 + 2 \cos(2\pi/7)) = \frac{1}{7} (1 + 2(0.6235)) = \frac{2.247}{7} \approx 0.3210$

- $h[2] = \frac{1}{7} (1 + 2 \cos(4\pi/7)) = \frac{1}{7} (1 + 2(-0.2225)) = \frac{0.555}{7} \approx 0.0793$

- $h[3] = \frac{1}{7} (1 + 2 \cos(6\pi/7)) = \frac{1}{7} (1 + 2(-0.9009)) = \frac{-0.8018}{7} \approx -0.1145$


By symmetry (since this is a zero-phase filter centered at $n=0$, we must shift it to make it causal, but the values remain the same).


**Physical interpretation:** The impulse response is essentially a sampled sinc function. The negative value at $h[3]$ indicates ringing, characteristic of sharp frequency cutoffs.

**Common mistakes to avoid:** Forgetting that $H[N-k]$ must equal $H^*[k]$ for $h[n]$ to be real.


### Example 2: Transition Sample Optimization
**Problem statement:** For a frequency sampled lowpass filter with $N=15$, the samples are defined as $H[0]=H[1]=1$, $H[2]=T_1$, and $H[k]=0$ for $k=3,4,5,6,7$. Symmetric for $k>7$.

Derive the expression for the zero-phase continuous frequency response $H(\omega)$ at $\omega = \frac{5\pi}{7}$ (midpoint of the stopband) in terms of $T_1$.


**Solution:**

For a zero-phase symmetric filter with odd $N$, the continuous response is:

$H(\omega) = H[0] + 2 \sum_{k=1}^{(N-1)/2} H[k] \cos(k\omega)$

Substitute the known values ($N=15$, $(N-1)/2 = 7$):

$H(\omega) = 1 + 2(1)\cos(\omega) + 2(T_1)\cos(2\omega) + 2(0)\cos(3\omega) + \dots$

$H(\omega) = 1 + 2\cos(\omega) + 2T_1\cos(2\omega)$


Evaluate at $\omega = \frac{5\pi}{7}$:

$H(5\pi/7) = 1 + 2\cos(5\pi/7) + 2T_1\cos(10\pi/7)$

$\cos(5\pi/7) \approx -0.6235$

$\cos(10\pi/7) = \cos(2\pi - 4\pi/7) = \cos(4\pi/7) \approx -0.2225$

$H(5\pi/7) = 1 + 2(-0.6235) + 2T_1(-0.2225)$

$H(5\pi/7) = 1 - 1.247 - 0.445 T_1 = -0.247 - 0.445 T_1$


**Physical interpretation:** The amplitude in the stopband at this specific frequency is a linear function of $T_1$. By choosing $T_1$ such that $-0.247 - 0.445 T_1 \approx 0$ (which gives $T_1 \approx -0.55$, though practical global optimization yields $T_1 \approx 0.39$ to minimize all sidelobes), we can theoretically force a zero at this frequency.

**Common mistakes to avoid:** Confusing the discrete indices $k$ with the continuous frequency variable $\omega$.


### Example 3: Verifying Type II Zero Constraint
**Problem statement:** Let $h[n] = \{1, 2, 3, 3, 2, 1\}$. Verify that this Type II filter has a null at $\omega = \pi$.

**Solution:**

This is an even-length ($N=6$), symmetric filter.

The frequency response evaluated at $\omega = \pi$ is given by the DTFT:

$H(e^{j\pi}) = \sum_{n=0}^{5} h[n] e^{-j\pi n} = \sum_{n=0}^{5} h[n] (-1)^n$

$H(e^{j\pi}) = h[0](-1)^0 + h[1](-1)^1 + h[2](-1)^2 + h[3](-1)^3 + h[4](-1)^4 + h[5](-1)^5$

$H(e^{j\pi}) = 1(1) + 2(-1) + 3(1) + 3(-1) + 2(1) + 1(-1)$

$H(e^{j\pi}) = 1 - 2 + 3 - 3 + 2 - 1 = 0$

**Physical interpretation:** The alternating sum of the coefficients of a symmetric even-length filter perfectly cancels out. It is physically incapable of passing a $1/2$ sampling rate frequency (Nyquist).

**Common mistakes to avoid:** Assuming that just because a filter is lowpass, it automatically has $H(\pi)=0$. Only Type II strictly forces it to exactly zero structurally.


### Example 4: Estimating Filter Order with Kaiser Formula
**Problem statement:** A digital audio system requires a lowpass filter with the following specifications:

Sampling frequency $f_s = 48$ kHz. Passband edge $f_p = 18$ kHz. Stopband edge $f_{stop} = 21$ kHz.

Passband ripple $R_p \le 0.1$ dB. Stopband attenuation $A_s \ge 60$ dB.

Estimate the required filter order $N$ for a Parks-McClellan design.


**Solution:**

1. Convert ripples to linear scale ($\delta_p, \delta_s$):

   $R_p = -20 \log_{10}(1 - \delta_p) \approx 8.686 \delta_p \implies \delta_p \approx \frac{0.1}{8.686} \approx 0.0115$

   $A_s = -20 \log_{10}(\delta_s) = 60 \implies \delta_s = 10^{-60/20} = 10^{-3} = 0.001$

2. Calculate normalized transition width:

   $\Delta f = \frac{f_{stop} - f_p}{f_s} = \frac{21 - 18}{48} = \frac{3}{48} = 0.0625$

3. Apply Kaiser's Formula:

   Numerator: $-20 \log_{10}(\sqrt{\delta_p \delta_s}) - 13$

   $\sqrt{\delta_p \delta_s} = \sqrt{0.0115 \times 0.001} = \sqrt{0.0000115} \approx 0.00339$

   $-20 \log_{10}(0.00339) \approx -20(-2.47) = 49.4$

   Numerator $= 49.4 - 13 = 36.4$

   Denominator: $14.6 \times \Delta f = 14.6 \times 0.0625 = 0.9125$

   $N \approx \frac{36.4}{0.9125} + 1 \approx 39.89 + 1 = 40.89$

4. Round up to the next integer. If a specific filter type is required (e.g., Type I), make $N$ odd. Let's choose $N=41$.


**Physical interpretation:** The narrow transition band (3 kHz relative to 48 kHz) dominates the requirement, pushing the order up to 41.

**Common mistakes to avoid:** Plugging dB values directly into the Kaiser formula instead of linear $\delta$ values.


### Example 5: Comparing Window vs PM Order
**Problem statement:** For the specifications in Example 4 ($A_s = 60$ dB, $\Delta f = 0.0625$), what would be the required order if we used the Window method (specifically a Blackman window)?


**Solution:**

1. Determine the appropriate window: A Blackman window provides a stopband attenuation of 74 dB, which exceeds the required 60 dB. (Hamming provides only 53 dB, which is insufficient).

2. Use the transition width formula for Blackman window:

   $\Delta \omega = \frac{5.56 \pi}{M}$ where $M = N-1$ is the filter order (some texts use $N$ directly; let's use $N$).

   In terms of normalized frequency $f$: $\Delta f = \frac{5.56}{2N}$ (since $\Delta \omega = 2\pi \Delta f$).

   Wait, a standard approximation is $\Delta f \approx \frac{5.5}{N}$.

   Let's use $\Delta f = \frac{5.56}{N} \implies N = \frac{5.56}{\Delta f}$.

3. Calculate $N$:

   $N = \frac{5.56}{0.0625} = 88.96 \implies N = 89$.


**Physical interpretation:** The Window method requires an order of 89, whereas Parks-McClellan requires an order of only 41 to meet the *exact same* specifications. This proves that PM is optimal and dramatically more efficient.

**Common mistakes to avoid:** Assuming all design methods yield similar filter orders.


---

## 7. ENGINEERING APPLICATIONS AND CASE STUDIES

**1. Digital Audio Anti-aliasing / Reconstruction Filters:**

In CD audio (44.1 kHz sampling), the audio band extends up to 20 kHz. The transition band from 20 kHz to 22.05 kHz (Nyquist) is incredibly narrow ($\Delta f \approx 0.046$). An equiripple filter designed via PM is the only way to achieve the required 90+ dB attenuation in the stopband without requiring a filter with thousands of taps (which would introduce unacceptable latency). The computational savings are immense.


**2. Matched Filters in Digital Communications:**

In QAM or QPSK transceivers, Root-Raised Cosine (RRC) filters are used to shape pulses. These filters must have strictly linear phase to ensure zero Intersymbol Interference (ISI) at the sampling instants. PM is used to design these equiripple FIR filters, often implemented efficiently in FPGA hardware using polyphase structures.


**3. Hilbert Transformers for Single Sideband (SSB) Modulation:**

A Type III or Type IV FIR filter designed with the PM algorithm can perfectly approximate an ideal 90-degree phase shift (Hilbert transform). This is heavily used in Software Defined Radios (SDR) to generate analytic signals for SSB modulation or phase demodulation. The zero at DC ensures that any DC offset in the baseband signal does not propagate through the phase shifter.


---

## 8. COMMON STUDENT MISCONCEPTIONS AND ERRORS

1. **Misconception:** "Parks-McClellan gives the filter with the absolute minimum number of taps for ANY specification."

   *Correction:* It gives the minimum order for a *minimax* (Chebyshev) error criterion. If your goal is to minimize total noise power, a Least-Squares FIR design might require a lower order for that specific metric.

2. **Misconception:** "The Alternation Theorem means the ripple is equal everywhere."

   *Correction:* It means the ripple is equal *in magnitude* at the extremal frequencies *within each band*. The ripple in the passband ($\delta_p$) and stopband ($\delta_s$) can be completely different if the weighting function $W(\omega)$ is not uniform.

3. **Misconception:** "Frequency sampling simply interpolates linearly between the sample points."

   *Correction:* It interpolates using the Dirichlet kernel (sinc-like function). This causes severe oscillations (Gibbs phenomenon) between the sample points, not straight lines.

4. **Misconception:** "Type II filters are the best general-purpose FIR filters because even lengths are easier for FFTs."

   *Correction:* Type II filters have a forced zero at $\omega = \pi$. They are completely useless for Highpass or Bandstop designs. Type I (odd length) is the true general-purpose filter.

5. **Misconception:** "More taps (larger N) in frequency sampling always reduces the error everywhere."

   *Correction:* Just like the continuous Gibbs phenomenon, increasing N makes the transition band steeper, but the *peak amplitude of the overshoot* (ripple) remains at roughly 9%, regardless of how large N gets, unless transition samples are optimized.

6. **Misconception:** "IIR filters are always better because they have lower order."

   *Correction:* While IIR filters have lower order, they do not have strictly linear phase and can be unstable, which makes FIR filters preferable for applications sensitive to phase distortion (e.g. data communications, images).

7. **Misconception:** "Parks-McClellan can perfectly design any filter."

   *Correction:* The algorithm can fail to converge if the specifications are not physically realizable or if the extremal frequency grid is too sparse. 


---

## 9. CONNECTIONS TO OTHER LECTURES

- **Builds on (Lectures 6-8):** DFT and IDFT concepts, zero-phase and linear-phase properties, z-transform symmetry conditions.

- **Builds on (Lecture 10):** The Window Method for FIR design (used as a sub-optimal baseline for comparison).

- **Supports (Future Lectures):** Polyphase implementations of FIR filters, multi-rate signal processing (decimation/interpolation filters heavily rely on equiripple designs), and eventually IIR filter design (where non-linear phase will be contrasted).


---

## 10. EXAMINATION QUESTIONS

### 10.1 Short Answer

**Q1:** State the mathematical condition required for an FIR filter to possess strictly linear phase.

*Answer:* The impulse response must be either symmetric ($h[n] = h[N-1-n]$) or anti-symmetric ($h[n] = -h[N-1-n]$).


**Q2:** Why is the frequency sampling method generally considered inferior to the Parks-McClellan algorithm for sharp cutoff filters?

*Answer:* Frequency sampling only guarantees exact matching at the discrete sample points. Between points, Dirichlet interpolation causes large ripples (Gibbs phenomenon) near cutoffs. PM optimizes the response over the entire continuous band.


**Q3:** How does a weighting function $W(\omega)$ provide flexibility in the PM algorithm?

*Answer:* It allows the designer to trade off passband ripple against stopband attenuation. By setting $W(\omega)$ higher in the stopband, the algorithm will force tighter constraints (smaller $\delta$) there.


**Q4:** A student designs a highpass filter and gets an output of all zeros. They used an FIR filter of length 64 with symmetric coefficients. What went wrong?

*Answer:* A symmetric filter with even length ($N=64$) is a Type II filter. Type II filters inherently have a zero at $\omega = \pi$ (the highest frequency), making them impossible to use as highpass filters.


**Q5:** Define the term "Alternation" in the context of the Chebyshev approximation problem.

*Answer:* An alternation is a frequency point where the error function $E(\omega)$ reaches its maximum absolute magnitude $\delta$ and alternates sign relative to the adjacent extremal frequency point.


### 10.2 Long Answer / Numerical Problems

**Problem 1:** Design a 5-tap linear phase FIR lowpass filter using frequency sampling. The desired frequency response is $H[0] = 1, H[1] = 0.5, H[2] = 0, H[3] = 0, H[4] = 0.5$. Calculate the impulse response $h[n]$. Is this a Type I, II, III, or IV filter? Prove it.

*Solution:* 

$N=5$ (odd length). Since $H[k]$ is purely real and symmetric ($H[1]=H[4], H[2]=H[3]$), $h[n]$ will be symmetric. Thus, Type I.

$h[n] = \frac{1}{5} \sum_{k=0}^{4} H[k] e^{j \frac{2\pi}{5} kn}$

$h[n] = \frac{1}{5} (1 + 0.5 e^{j \frac{2\pi}{5} n} + 0.5 e^{j \frac{2\pi}{5} 4n})$

Since $e^{j \frac{2\pi}{5} 4n} = e^{-j \frac{2\pi}{5} n}$:

$h[n] = \frac{1}{5} (1 + \cos(\frac{2\pi}{5} n))$

Evaluating for $n=0,1,2,3,4$:

$h[0] = 0.4$

$h[1] = 0.2(1 + \cos(72^\circ)) \approx 0.2(1 + 0.309) = 0.2618$

$h[2] = 0.2(1 + \cos(144^\circ)) \approx 0.2(1 - 0.809) = 0.0382$

By symmetry (circular), $h[3] = h[2] = 0.0382$, $h[4] = h[1] = 0.2618$.


**Problem 2:** An equiripple lowpass filter is designed with $N=25$. How many alternating error extrema must it have at a minimum, assuming it is a Type I filter? If the algorithm converges with exactly this number of extrema, how many are in the passband and how many in the stopband?

*Solution:* 

$N=25$, Type I. Number of free parameters $L = (N+1)/2 = 13$.

Minimum alternations required = $L+1 = 14$.

The distribution of the 14 extrema between passband and stopband depends on the specifications ($\delta_p, \delta_s, \Delta f$) and cannot be determined purely a priori without running the algorithm, though they generally split proportionally to the band widths.


**Problem 3:** Compare the estimated filter lengths required to meet the following specs using (a) Kaiser's formula for PM, and (b) a Hamming window. Specs: $f_s=10$ kHz, $f_p=2$ kHz, $f_{stop}=2.5$ kHz, Stopband attenuation = 50 dB, Passband ripple = 0.05 dB.

*Solution:*

(a) Kaiser: $\Delta f = 0.5/10 = 0.05$. $A_s = 50$ dB $\implies \delta_s = 0.00316$. $R_p = 0.05 \implies \delta_p \approx 0.0057$.

$\sqrt{\delta_p \delta_s} \approx 0.0042$. $-20 \log_{10}(0.0042) \approx 47.5$.

$N \approx \frac{47.5 - 13}{14.6(0.05)} + 1 = \frac{34.5}{0.73} + 1 \approx 48.2 \implies 49$.

(b) Hamming: The transition width is roughly $\Delta f \approx 3.3/N \implies N \approx 3.3/0.05 = 66$. (Note: Hamming max attenuation is 53 dB, so it just barely meets the 50 dB spec). PM is much more efficient.


**Problem 4:** Derive the symmetry conditions for $H[k]$ to ensure that $h[n]$ is purely real in the frequency sampling method.

*Solution:*

$h[n] = \frac{1}{N} \sum_{k=0}^{N-1} H[k] e^{j \frac{2\pi}{N} kn}$

For $h[n]$ to be real, $h[n] = h^*[n]$.

$h^*[n] = \frac{1}{N} \sum_{k=0}^{N-1} H^*[k] e^{-j \frac{2\pi}{N} kn}$

Let $m = N-k$. As $k$ goes from $1$ to $N-1$, $m$ goes from $N-1$ down to $1$. The $k=0$ term is isolated.

$h^*[n] = \frac{1}{N} H^*[0] + \frac{1}{N} \sum_{m=1}^{N-1} H^*[N-m] e^{-j \frac{2\pi}{N} (N-m)n}$

$e^{-j \frac{2\pi}{N} N n} e^{j \frac{2\pi}{N} mn} = (1) e^{j \frac{2\pi}{N} mn}$

$h^*[n] = \frac{1}{N} H^*[0] + \frac{1}{N} \sum_{m=1}^{N-1} H^*[N-m] e^{j \frac{2\pi}{N} mn}$

Equating coefficients of the basis functions $e^{j \frac{2\pi}{N} kn}$ in $h[n]$ and $h^*[n]$:

$H[0] = H^*[0] \implies H[0]$ must be real.

$H[k] = H^*[N-k]$ for $k = 1, 2, \dots, N-1$. This is the conjugate symmetry condition.


### 10.3 True/False with Justification

1. **T/F:** A Type III filter can be used as a lowpass filter.

   *False.* Type III filters have $H(e^{j0}) = 0$, meaning they completely reject DC. A lowpass filter must pass DC.

2. **T/F:** The Remez exchange algorithm is used to find the minimum least-squares error of a filter.

   *False.* It is used to minimize the maximum absolute error (Chebyshev norm), not the sum of squared errors.

3. **T/F:** Increasing the number of transition samples in the frequency sampling method narrows the transition band.

   *False.* Introducing transition samples *widens* the transition band. The benefit is that it reduces the peak stopband sidelobe level.

4. **T/F:** FIR filters can guarantee absolute stability.

   *True.* Because they have no feedback (all poles at the origin of the z-plane), they can never become unstable.

5. **T/F:** The Alternation Theorem applies only to IIR filters.

   *False.* It is specifically the foundation for optimal FIR filter design using polynomials.

6. **T/F:** Kaiser's formula estimates that filter length $N$ is inversely proportional to transition width $\Delta f$.

   *True.* The denominator of the formula is $14.6 \Delta f$, showing a clear inverse relationship: tighter transition bands require significantly higher order filters.


---

## 11. KEY FORMULAS REFERENCE

| Description | Formula |

| :--- | :--- |

| **DFT** | $H[k] = \sum_{n=0}^{N-1} h[n] e^{-j \frac{2\pi}{N} k n}$ |

| **IDFT (Freq Sampling)** | $h[n] = \frac{1}{N} \sum_{k=0}^{N-1} H[k] e^{j \frac{2\pi}{N} k n}$ |

| **Weighted Error** | $E(\omega) = W(\omega) [H_d(\omega) - A(\omega)]$ |

| **Free Params (Type I)** | $L = \frac{N+1}{2}$ |

| **Free Params (Type II)** | $L = \frac{N}{2}$ |

| **Kaiser Estimate for N** | $N \approx \frac{-20 \log_{10}(\sqrt{\delta_p \delta_s}) - 13}{14.6 \Delta f} + 1$ |

| **Type I Phase** | $\angle H(e^{j\omega}) = -\left(\frac{N-1}{2}\right)\omega$ |

| **Linear Phase Center** | $\alpha = \frac{N-1}{2}$ |


---

## 12. FURTHER READING AND REFERENCES

1. **Proakis, J. G., & Manolakis, D. K.** (2006). *Digital Signal Processing: Principles, Algorithms, and Applications* (4th ed.). Pearson. (Chapter 10: FIR Filter Design).

2. **Oppenheim, A. V., & Schafer, R. W.** (2009). *Discrete-Time Signal Processing* (3rd ed.). Prentice Hall. (Chapter 7: Filter Design Techniques).

3. **Parks, T. W., & McClellan, J. H.** (1972). *Chebyshev Approximation for Nonrecursive Digital Filters with Linear Phase*. IEEE Transactions on Circuit Theory. (The original paper — excellent for advanced reading).

4. **Haykin, S., & Van Veen, B.** (2002). *Signals and Systems* (2nd ed.). Wiley. (Good for reviewing the basic Fourier Transform properties used in the proofs).

</Faculty Notes — Lecture 11: FIR Design — Parks-McClellan & Frequency Sampling>

