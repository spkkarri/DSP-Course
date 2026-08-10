# Lecture 11: FIR Filter Design — Frequency Sampling & Optimal Methods

**Course:** EE3621 — Digital Signal Processing  
**Target Audience:** III B.Tech EEE Students  
**Duration:** 40 Minutes  

* **Available Formats:** [LaTeX Source File](file:///C:/Users/sriph/Downloads/DSP/lecture_11.tex) | [Compiled PDF Notes](file:///C:/Users/sriph/Downloads/DSP/lecture_11.pdf)

---

## 1. Lecture Plan (40 Minutes Breakdown)

* **00:00 – 05:00 (5 mins):** Introduction to Frequency Sampling Design.
* **05:00 – 12:00 (7 mins):** Transition Sample Optimization.
* **12:00 – 20:00 (8 mins):** Parks-McClellan (Remez Exchange) Algorithm and Alternation Theorem.
* **20:00 – 25:00 (5 mins):** Design Formulas (Kaiser, Herrmann-Rabiner).
* **25:00 – 30:00 (5 mins):** FIR Filter Types (I, II, III, IV) and their constraints.
* **30:00 – 35:00 (5 mins):** Worked Example: 15-tap Equiripple Bandpass Filter.
* **35:00 – 40:00 (5 mins):** FIR vs IIR Comparison and Checkpoint Questions.

---

## 2. Frequency Sampling Method

The frequency sampling method is a direct way to design FIR filters. Instead of manipulating the impulse response in the time domain, we specify the desired frequency response exactly at $N$ equally spaced points in the frequency domain.

### 2.1 Concept and Formulation

Let the desired continuous frequency response be $H_d(\omega)$. We sample this response at $N$ equally spaced frequencies in the range $0 \le \omega < 2\pi$:

$$
\omega_k = \frac{2\pi k}{N}, \quad k = 0, 1, \dots, N-1
$$

The sampled frequency response is defined as:

$$
H[k] = H_d\left(\frac{2\pi k}{N}\right)
$$

The impulse response $h[n]$ of the FIR filter is obtained by taking the $N$-point Inverse Discrete Fourier Transform (IDFT) of $H[k]$.

### 2.2 Derivation of Impulse Response

We start with the IDFT definition:

$$
h[n] = \frac{1}{N} \sum_{k=0}^{N-1} H[k] e^{j \frac{2\pi}{N} kn}
$$

$$
h[n] = \frac{1}{N} \sum_{k=0}^{N-1} H[k] W_N^{-kn}
$$

where $W_N = e^{-j 2\pi / N}$ is the twiddle factor.

Let's expand the summation carefully to show the symmetry properties. Assuming $H[k]$ is conjugate symmetric (since $h[n]$ must be real):

$$
H[N-k] = H^*[k]
$$

We can split the summation into the DC component, the Nyquist component (if $N$ is even), and the conjugate symmetric pairs.

For $N$ odd:

$$
h[n] = \frac{1}{N} H[0] + \frac{1}{N} \sum_{k=1}^{(N-1)/2} \left[ H[k] e^{j \frac{2\pi}{N} kn} + H[N-k] e^{j \frac{2\pi}{N} (N-k)n} \right]
$$

$$
h[n] = \frac{1}{N} H[0] + \frac{1}{N} \sum_{k=1}^{(N-1)/2} \left[ H[k] e^{j \frac{2\pi}{N} kn} + H^*[k] e^{-j \frac{2\pi}{N} kn} \right]
$$

Let $H[k] = |H[k]| e^{j \angle H[k]}$. Then:

$$
h[n] = \frac{1}{N} H[0] + \frac{2}{N} \sum_{k=1}^{(N-1)/2} |H[k]| \cos\left(\frac{2\pi}{N} kn + \angle H[k]\right)
$$

For a linear phase FIR filter, we must impose constraints on $\angle H[k]$. Specifically, for a Type I filter (symmetric, odd $N$), the phase must be:

$$
\angle H[k] = - \alpha \frac{2\pi k}{N}
$$

where $\alpha = \frac{N-1}{2}$.

Substituting this back into the equation:

$$
h[n] = \frac{1}{N} H[0] + \frac{2}{N} \sum_{k=1}^{(N-1)/2} |H[k]| \cos\left(\frac{2\pi k}{N} (n - \alpha)\right)
$$

**KEY RESULT:** The filter exactly interpolates the specified points at $\omega_k$. However, between the sample points, the frequency response may exhibit significant ripple, especially near the transition band.

---

## 3. Transition Sample Optimization

The basic frequency sampling method can lead to large ripples between the sample points in the passband and stopband (similar to the Gibbs phenomenon). To mitigate this, we can introduce one or more "transition samples" in the transition band.

### 3.1 Intuition

Instead of forcing the frequency response to jump abruptly from 1 to 0 between two adjacent frequency samples, we introduce an intermediate value (e.g., $T_1 = 0.39$).

### 3.2 Effect of Transition Samples

By allowing the transition band to have a non-zero sample, we increase the transition width, but we gain an additional degree of freedom. This degree of freedom can be optimized to minimize the maximum sidelobe level in the stopband.

Example:
For a lowpass filter with $N = 33$, suppose we specify:
* Passband: $H[0] = H[1] = H[2] = H[3] = 1$
* Transition: $H[4] = T_1$
* Stopband: $H[5] = \dots = H[16] = 0$

Without $T_1$ (i.e., $T_1 = 0$), the stopband attenuation might only be -20 dB.
By optimizing $T_1$, we can push the stopband attenuation to -40 dB or better. A common optimal value found via linear programming is $T_1 \approx 0.39$.
If we use two transition samples, $T_1$ and $T_2$, we can achieve even higher stopband attenuation (e.g., -60 dB) at the cost of a wider transition band.

---

## 4. Parks-McClellan (Remez Exchange) Algorithm

While frequency sampling is simple, it is not optimal. The window method is also sub-optimal because it minimizes the mean squared error rather than the maximum absolute error. The **Parks-McClellan algorithm** designs optimal equiripple FIR filters by minimizing the Chebyshev (minimax) error.

### 4.1 Chebyshev Approximation Problem Formulation

Let $H(\omega)$ be the zero-phase frequency response of an FIR filter.
Let $H_d(\omega)$ be the desired frequency response.
Let $W(\omega)$ be a positive weighting function that allows us to specify different error tolerances for different frequency bands (e.g., tighter tolerance in the stopband).

The weighted error function is defined as:

$$
E(\omega) = W(\omega) [H_d(\omega) - H(\omega)]
$$

The goal is to find the filter coefficients that minimize the maximum absolute error over the closed subset of frequencies $A \subset [0, \pi]$ (which includes the passband and stopband, but excludes the transition band).

Mathematically, we want to minimize:

$$
\max_{\omega \in A} |E(\omega)|
$$

This is the minimax or Chebyshev approximation problem:

$$
\min_{h[n]} \max_{\omega \in A} W(\omega) |H_d(\omega) - H(\omega)|
$$

### 4.2 Alternation Theorem

The solution to the Chebyshev approximation problem is characterized by the **Alternation Theorem**.

**Theorem:** If $H(\omega)$ is a linear combination of $L$ independent cosine functions (i.e., $H(\omega)$ has $L$ free parameters), then $H(\omega)$ is the unique optimal min-max approximation if and only if the error function $E(\omega)$ exhibits at least $L+1$ extremal frequencies (alternations) in $A$.

At these extremal frequencies $\omega_i$, the error reaches the maximum magnitude but alternates in sign:

$$
E(\omega_i) = -E(\omega_{i+1}) = \pm \max_{\omega \in A} |E(\omega)|
$$

For a Type I FIR filter of length $N$, the number of free parameters is $L = \frac{N+1}{2}$. Thus, the optimal filter must have at least $L+1$ alternations. Because the error touches the maximum bound and bounces back, the resulting magnitude response is "equiripple."

### 4.3 Remez Algorithm Outline

The Parks-McClellan algorithm uses the Remez exchange algorithm, which is an iterative procedure to find the optimal polynomial.

1. **(a) Guess extremal frequencies:** Initialize a set of $L+1$ guess frequencies $\omega_i$ in the bands of interest.
2. **(b) Solve for polynomial:** Calculate the optimal maximum error $\delta$ and the polynomial $H(\omega)$ that exactly satisfies $E(\omega_i) = (-1)^i \delta$ at the current guess frequencies.
3. **(c) Find actual maximum error location:** Evaluate $E(\omega)$ on a dense grid over the entire set $A$ to find the actual local maxima of $|E(\omega)|$.
4. **(d) Update extremal set:** If the maximum error on the dense grid is greater than $\delta$, update the set of extremal frequencies with the new peak locations, ensuring the alternating sign property is maintained.
5. **(e) Iterate:** Repeat steps (b) through (d) until the extremal frequencies converge (i.e., they do not change between iterations).

### 4.4 Comparison with Window Method

* **Optimality:** The equiripple filter has the minimum possible order for a given set of specifications (passband ripple, stopband attenuation, transition width).
* **Error Distribution:** The window method produces larger ripples near the band edges (Gibbs phenomenon). The equiripple method spreads the error evenly across the band.
* **Complexity:** The window method is computationally trivial (analytical formula). Parks-McClellan requires an iterative numerical algorithm.

---

## 5. Design Formulas

To estimate the required filter length $N$ for given specifications, we use empirical formulas.

Let:
* $\delta_p$ = passband ripple
* $\delta_s$ = stopband ripple
* $\Delta f = \frac{\omega_s - \omega_p}{2\pi}$ = normalized transition width

### 5.1 Kaiser Formula

Kaiser proposed a simple formula to estimate $N$:

$$
N \approx \frac{-20 \log_{10}(\sqrt{\delta_p \delta_s}) - 13}{14.6 \Delta f} + 1
$$

### 5.2 Herrmann-Rabiner Formula

A more accurate empirical formula was developed by Herrmann, Rabiner, and Chan:

$$
N \approx \frac{D_{\infty}(\delta_p, \delta_s) - F(\delta_p, \delta_s) (\Delta f)^2}{\Delta f} + 1
$$

where $D_{\infty}$ and $F$ are complex polynomial functions of $\log_{10}(\delta_p)$ and $\log_{10}(\delta_s)$. For most engineering purposes, the Kaiser formula provides a very good starting point.

---

## 6. Type I, II, III, IV FIR Filters

Linear phase FIR filters are classified into four types based on symmetry and filter length.

Let $h[n]$ be the impulse response of length $N$.
Symmetry condition: $h[n] = \pm h[N-1-n]$.

### 6.1 Type I: Symmetric, Odd Length
* $h[n] = h[N-1-n]$
* $N$ is odd.
* Center of symmetry is an integer: $\alpha = (N-1)/2$.
* **Constraints:** No constraints at $\omega = 0$ or $\omega = \pi$.
* **Applications:** Can be used for any filter type (Lowpass, Highpass, Bandpass, Bandstop).

### 6.2 Type II: Symmetric, Even Length
* $h[n] = h[N-1-n]$
* $N$ is even.
* Center of symmetry is a half-integer.
* **Constraints:** $H(e^{j\pi}) = 0$. (Must have a zero at $\omega = \pi$).
* **Applications:** Cannot be used for Highpass or Bandstop filters. Good for Lowpass.

### 6.3 Type III: Anti-Symmetric, Odd Length
* $h[n] = -h[N-1-n]$
* $N$ is odd.
* **Constraints:** $h[\alpha] = 0$. $H(e^{j0}) = 0$ and $H(e^{j\pi}) = 0$. (Zeros at both $\omega = 0$ and $\omega = \pi$).
* **Applications:** Differentiators, Hilbert transformers, Bandpass filters. Cannot be Lowpass or Highpass.

### 6.4 Type IV: Anti-Symmetric, Even Length
* $h[n] = -h[N-1-n]$
* $N$ is even.
* **Constraints:** $H(e^{j0}) = 0$. (Zero at $\omega = 0$).
* **Applications:** Highpass filters, Differentiators, Hilbert transformers. Cannot be Lowpass.

---

## 7. FIR vs IIR Comparison Table

| Feature | FIR Filters | IIR Filters |
| :--- | :--- | :--- |
| **Stability** | Always stable (all poles at origin) | Conditionally stable (poles must be inside unit circle) |
| **Phase Linearity** | Can have exact linear phase | Cannot have exact linear phase (phase is non-linear) |
| **Filter Order (N)** | High (typically 20 to 200+) | Low (typically 2 to 10) |
| **Design Complexity** | High (Parks-McClellan is iterative) | Low (Bilinear transform from analog prototypes) |
| **Computational Load** | High (many multiply-accumulate ops) | Low (fewer operations per sample) |
| **Feedback** | No (Non-recursive) | Yes (Recursive) |
| **Implementation** | Efficient via FFT (see image below) | Standard difference equations |
| **Applications** | Audio processing, phase-sensitive comms | Equalizers, systems where phase distortion is acceptable |

*Note on implementation:* Large FIR filters can be implemented very efficiently using block convolution methods (Overlap-Add / Overlap-Save) which rely on the Fast Fourier Transform (FFT). The butterfly structure of the FFT (e.g., Decimation-in-Frequency) is crucial for this speedup.

![DIT vs DIF Butterfly Structures](images/dif_butterfly.png)

---

## 8. Worked Example: 15-Tap Equiripple Bandpass Filter

**Problem:** Design a 15-tap ($N=15$) optimal equiripple bandpass filter. 
Desired passband: $\omega \in [0.4\pi, 0.6\pi]$.
Stopbands: $\omega \in [0, 0.2\pi]$ and $\omega \in [0.8\pi, \pi]$.
Equal weighting: $W(\omega) = 1$ in all bands.

**Step-by-step setup:**

1. **Filter Type:** Since $N=15$ (odd) and we want a bandpass filter, we must use a Type I FIR filter.

2. **Number of Free Parameters:**
$$
L = \frac{N+1}{2} = \frac{15+1}{2} = 8
$$

3. **Alternation Theorem Requirement:**
The optimal error curve must have at least $L+1 = 9$ alternating extrema.

4. **Parks-McClellan Execution (Conceptual):**
   * **Initialization:** The algorithm picks 9 initial guess frequencies spread across the two stopbands and one passband.
   * **Iteration 1:** It solves for the optimal error $\delta$ and the coefficients of the cosine series.
   * **Update:** It evaluates the actual frequency response on a dense grid of roughly $15 \times 16 = 240$ points. It locates the peaks of the error curve.
   * **Convergence:** The peak locations are updated. After a few iterations, the maximum error in all three bands equalizes to exactly $\pm \delta$.

**Output:**
The PM algorithm returns the 8 independent coefficients $h[0], h[1], \dots, h[7]$.
The remaining coefficients are found via symmetry:
$$
h[8] = h[6], \quad h[9] = h[5], \quad \dots \quad h[14] = h[0]
$$
The resulting frequency response will have an equiripple behavior in both stopbands and the passband, bounded exactly by $\pm \delta$.

---

## 9. Checkpoint Questions

1. **Q1:** Why can't a Type II FIR filter be used to design a highpass filter?
   * *Detailed Answer:* A Type II FIR filter has an even number of taps ($N$ is even) and symmetric coefficients ($h[n] = h[N-1-n]$). The frequency response of a symmetric filter can be written as $H(\omega) = e^{-j\omega(N-1)/2} \sum_{n=1}^{N/2} 2h[N/2-n] \cos(\omega(n-0.5))$. If we evaluate this at $\omega = \pi$ (the highest frequency in discrete time), the argument of the cosine becomes $\pi(n-0.5) = n\pi - \pi/2$. The cosine of any odd multiple of $\pi/2$ is identically zero. Therefore, $H(e^{j\pi}) = 0$ always. A highpass filter must pass the frequency $\omega = \pi$ (i.e., $H(e^{j\pi}) \neq 0$). Since a Type II filter strictly forces the response to be zero at $\pi$, it is physically impossible to use it as a highpass filter.

2. **Q2:** In the frequency sampling method, if we specify the desired response exactly, why isn't the resulting filter perfect?
   * *Detailed Answer:* The frequency sampling method forces the filter's frequency response to perfectly match the desired response *only at the specific sample points* $\omega_k = 2\pi k / N$. However, between these sample points, the frequency response is determined by the interpolation formula (a sum of shifted sinc-like functions, specifically the Dirichlet kernel). Because the desired response often has abrupt discontinuities (like an ideal brick-wall filter), interpolating it with a finite number of points leads to severe overshoot and ringing between the samples (the discrete-time equivalent of the Gibbs phenomenon). Thus, while the error is exactly zero at the sampled frequencies, it can be unacceptably large between them.

3. **Q3:** According to the Alternation Theorem, a length-21 Type I equiripple lowpass filter must have how many alternations, and what does this mean physically?
   * *Detailed Answer:* For a Type I filter, the length $N$ is odd, so $N = 21$. The number of independent coefficients (free parameters) is $L = (N+1)/2 = (21+1)/2 = 11$. The Alternation Theorem states that the optimal Chebyshev filter must have at least $L+1$ extremal frequencies. Therefore, there must be at least $11+1 = 12$ alternations. Physically, this means that if we plot the error function $E(\omega)$ over the passband and stopband, it will hit its maximum allowable magnitude and bounce back in the opposite direction at least 12 times. This creates the characteristic "equiripple" pattern where the frequency response ripples uniformly between the upper and lower tolerance bounds.

---

## 10. Summary of Key Formulas

| Concept | Formula |
| :--- | :--- |
| **Frequency Sample IDFT** | $h[n] = \frac{1}{N}\sum_{k=0}^{N-1} H[k] W_N^{-kn}$ |
| **Chebyshev Error** | $E(\omega) = W(\omega) [H_d(\omega) - H(\omega)]$ |
| **Kaiser N Estimate** | $N \approx \frac{-20 \log_{10}(\sqrt{\delta_p \delta_s}) - 13}{14.6 \Delta f} + 1$ |
| **Free Parameters (Type I)** | $L = \frac{N+1}{2}$ |

<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
