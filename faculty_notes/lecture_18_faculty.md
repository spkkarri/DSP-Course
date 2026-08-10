<Faculty Notes — Lecture 18: Wavelet Transform & Multiresolution Analysis>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY

Teaching the Wavelet Transform is notoriously difficult in an undergraduate DSP course because it requires students to shift their fundamental perspective from stationary analysis (Fourier) to multiresolution analysis. Up to this point, students are comfortable with frequency analysis where sinusoids of infinite duration are the basis functions. The STFT (Short-Time Fourier Transform) provides a bridge, but it retains the fixed-resolution problem. Wavelets fix the fixed-resolution limitation of STFT, but the mathematics can appear daunting.

The key to teaching this lecture is to ground the abstract mathematics in intuitive concepts:
1. **The Windowing Problem:** Start with the STFT. Show how a fixed window size restricts the time-frequency resolution trade-off. 
2. **Constant-Q Analysis:** Explain how wavelets adapt their width to the frequency being analyzed (short windows for high frequencies, long windows for low frequencies).
3. **MRA and the Filter Bank Connection:** This is the most crucial insight for EEE students. The Continuous Wavelet Transform (CWT) is mathematically elegant, but the Discrete Wavelet Transform (DWT) via Multiresolution Analysis (MRA) connects directly to their existing knowledge of digital filters. Show them that Mallat's algorithm is just an iterated filter bank (a cascade of lowpass and highpass filters with decimation).
4. **The Haar Wavelet:** Use the Haar wavelet as the simplest example to build intuition. Because its coefficients are simple averages and differences, students can manually compute a 1-level DWT easily and see the energy compaction.

**Suggested Demos:**
* Use MATLAB or Python to plot a signal with a sudden spike and a slow drift. Show its STFT (spectrogram) and point out the blurring. Then show its Continuous Wavelet Transform (scalogram) to highlight the sharp time localization at high frequencies and good frequency localization at low frequencies.
* Perform a live 1-level DWT of a simple 8-point vector using the Haar wavelet on the board. This demystifies the process.
* Demonstrate the effect of thresholding on a noisy signal. This shows a very practical application of the DWT that is easy for students to visually grasp.
* Show the decomposition tree dynamically.

**Prerequisite Checks:**
* Ensure students understand the uncertainty principle in signal processing (time-bandwidth product).
* Review decimation (downsampling) and its effect in the frequency domain (aliasing).
* Review the concept of orthogonal basis functions and inner products.

---
## 1. LEARNING OBJECTIVES

By the end of this lecture, students will be able to:
1. **Analyze** the limitations of the Short-Time Fourier Transform (STFT) concerning time-frequency resolution and the fixed-window problem.
2. **Formulate** the Continuous Wavelet Transform (CWT) and explain the physical significance of the scale and translation parameters.
3. **Evaluate** the Admissibility Condition for mother wavelets and prove that it necessitates a zero-mean property.
4. **Construct** the nested subspaces of Multiresolution Analysis (MRA) and derive the two-scale relations for scaling and wavelet functions.
5. **Execute** Mallat's pyramid algorithm to compute the Discrete Wavelet Transform (DWT) of discrete-time signals using iterated filter banks.
6. **Design** Quadrature Mirror Filters (QMF) that satisfy perfect reconstruction conditions and verify them for the Haar wavelet.
7. **Apply** wavelet transforms to solve engineering problems such as image compression (JPEG 2000), ECG baseline wander removal, and signal denoising.
8. **Differentiate** between various wavelet families (Haar, Daubechies, Biorthogonal) based on their properties like compact support, orthogonality, and linear phase.

---
## 2. PREREQUISITE KNOWLEDGE REVIEW

Before diving into wavelets, students must recall the following concepts:

**1. The Fourier Transform (FT) and Short-Time Fourier Transform (STFT):**
The FT decomposes a signal into infinite-duration complex exponentials:
$$ X(\omega) = \int_{-\infty}^{\infty} x(t) e^{-j\omega t} dt $$
While FT gives exact frequency information, it provides zero time resolution.
The STFT introduces a sliding window $w(t)$ to gain time-localization:
$$ X(t, \omega) = \int_{-\infty}^{\infty} x(\tau) w(\tau - t) e^{-j\omega \tau} d\tau $$
*Crucial limitation:* The width of $w(t)$ is fixed. By Heisenberg's Uncertainty Principle ($\Delta t \Delta \omega \ge 1/2$), a narrow window gives good time resolution but poor frequency resolution, and vice-versa. For a given STFT analysis, once the window is chosen, the resolution tiling in the time-frequency plane is rigidly fixed across all frequencies. If you choose a window of 20 ms, you can resolve fast transients lasting 20 ms, but you cannot resolve frequency components closer than $\approx 50$ Hz. If you choose a 2-second window to resolve 0.5 Hz frequency differences, you smear any transient shorter than 2 seconds.

**2. Inner Products and Basis Functions:**
The projection of a signal $x(t)$ onto a basis function $\phi(t)$ is given by the inner product:
$$ \langle x, \phi \rangle = \int_{-\infty}^{\infty} x(t) \phi^*(t) dt $$
This measures "how much" of the basis function is present in the signal. If the basis functions form an orthonormal set, Parseval's theorem guarantees energy conservation.

**3. Digital Filters and Decimation:**
Passing a signal $x[n]$ through a filter $h[n]$ gives convolution: $y[n] = x[n] * h[n]$.
Downsampling by 2 (decimation) means keeping only even-indexed samples: $y_d[n] = y[2n]$. This will introduce aliasing (overlapping spectra) unless the signal is properly low-pass filtered (anti-aliasing) prior to decimation. Upsampling by 2 (interpolation) involves inserting a zero between every sample, creating spectral images that must be removed via an anti-imaging filter. These concepts are foundational for understanding the filter bank implementation of the DWT.

---
## 3. HISTORICAL AND MOTIVATIONAL CONTEXT

**Who discovered this?**
The mathematical foundations of wavelets were laid by Alfred Haar (1909), who described the simplest wavelet (a step function). For decades, it remained a mathematical curiosity. In the 1980s, the modern unified theory was developed by geophysicist Jean Morlet and theoretical physicist Alex Grossmann (who coined the term "wavelet"), and mathematicians Yves Meyer and Ingrid Daubechies (who constructed compactly supported orthogonal wavelets). Finally, Stephane Mallat later connected wavelets to filter banks via MRA in 1989, making them practically computable for engineers.

**Real Engineering Applications:**
Why do electrical engineers need wavelets? Standard Fourier analysis fails for non-stationary signals—signals whose frequency content changes over time. 
* In **seismology**, determining the exact time a high-frequency acoustic wave hits a rock boundary is critical for oil exploration. Fourier methods fail because they smear this sudden event over all frequencies.
* In **biomedical engineering**, an ECG signal contains a slow baseline wander (respiration artifacts, $< 0.5$ Hz) and very sharp, sudden spikes (the QRS complex). STFT blurs these spikes, whereas wavelets cleanly isolate them.
* In **image processing**, sharp edges in images (sudden transitions) require excellent spatial (time) resolution, which DCT (used in standard JPEG) struggles with, leading to blocky artifacts. Wavelets natively handle this, leading to their adoption in the JPEG 2000 standard and the FBI fingerprint compression standard.
* In **power systems**, detecting sub-cycle power quality disturbances (like transients and voltage sags) relies heavily on wavelet analysis to pinpoint the exact start and end times of the fault.

**Motivation for Wavelets:**
The core motivation is to achieve **logarithmically scaled resolution** (Constant-Q analysis). We want a flexible window:
* For high frequencies: short time windows (to catch rapid transients).
* For low frequencies: long time windows (to resolve slow drifts accurately).
By having logarithmically scaled frequency bands, wavelets provide a much more natural analysis tool for signals that have both fine transient features and long slow trends. The time-bandwidth product is constant, allowing for optimal time-frequency tiling.

---
## 4. THEORETICAL FOUNDATIONS

### 4.1 The Continuous Wavelet Transform (CWT)

The Continuous Wavelet Transform projects a signal $x(t)$ onto a set of basis functions that are all derived from a single prototype function, the **mother wavelet**, $\psi(t)$. 

**The Definition:**
The CWT of a continuous-time signal $x(t) \in L^2(\mathbb{R})$ is defined as:
$$ W_x(a,b) = \frac{1}{\sqrt{|a|}} \int_{-\infty}^{\infty} x(t)\psi^*\left(\frac{t-b}{a}\right)dt $$

**Parameters and Physical Interpretation:**
1. **$a$ (Scale Parameter):** The parameter $a \in \mathbb{R}^+$ controls the dilation or compression of the wavelet. 
   * If $a < 1$, the wavelet is compressed in time. This makes it oscillate faster, thereby capturing high-frequency content. The time window is narrow, giving precise time localization.
   * If $a > 1$, the wavelet is stretched. It oscillates slower, capturing low-frequency content. The time window is wide, giving precise frequency localization.
   * *Relation to frequency:* Scale $a$ is inversely proportional to frequency $f$. Specifically, $f \approx \frac{f_c}{a}$, where $f_c$ is the center frequency of the mother wavelet.
2. **$b$ (Translation Parameter):** The parameter $b \in \mathbb{R}$ shifts the wavelet along the time axis, allowing us to analyze the signal at different moments in time. 
3. **$\frac{1}{\sqrt{|a|}}$ (Normalization):** This factor ensures that the wavelet energy is conserved across all scales. The energy of the mother wavelet is $E = \int |\psi(t)|^2 dt$. The energy of the scaled wavelet $\psi_{a,b}(t) = \frac{1}{\sqrt{|a|}}\psi(\frac{t-b}{a})$ is:
   $$ \int_{-\infty}^{\infty} \left| \frac{1}{\sqrt{|a|}}\psi\left(\frac{t-b}{a}\right) \right|^2 dt = \frac{1}{|a|} \int_{-\infty}^{\infty} \left| \psi\left(\frac{t-b}{a}\right) \right|^2 dt $$
   Let $u = \frac{t-b}{a}$, then $dt = a du$. 
   $$ \frac{1}{|a|} \int_{-\infty}^{\infty} |\psi(u)|^2 a du = \int_{-\infty}^{\infty} |\psi(u)|^2 du = E $$
   Thus, all scaled wavelets have the same energy.

### 4.2 The Admissibility Condition

For the CWT to be invertible (i.e., we can recover $x(t)$ from $W_x(a,b)$), the mother wavelet must satisfy the admissibility condition:
$$ C_\psi = \int_0^\infty \frac{|\Psi(\omega)|^2}{\omega} d\omega < \infty $$
where $\Psi(\omega)$ is the Fourier transform of $\psi(t)$.

**Physical Interpretation:**
This condition ensures that the inverse transform integral converges. More importantly, it implies a fundamental property of the wavelet in the time domain: it must have a zero mean. (See complete proof in Section 5). 
$$ \int_{-\infty}^{\infty} \psi(t) dt = 0 $$
Because the mean is zero, the function must go above and below the x-axis, creating a "small wave" or "wavelet". Without this property, the basis function would just be a DC offset, not an oscillating wave.

### 4.3 Multiresolution Analysis (MRA)

While the CWT uses continuous parameters $a$ and $b$, computing it is highly redundant and numerically intensive. We transition to the Discrete Wavelet Transform (DWT) by discretizing the scale and translation parameters on a **dyadic grid**:
$$ a = 2^j, \quad b = k \cdot 2^j $$
where $j, k \in \mathbb{Z}$. The basis functions become:
$$ \psi_{j,k}(t) = 2^{-j/2} \psi(2^{-j}t - k) $$

The foundation for this discrete framework is Multiresolution Analysis (MRA). MRA defines a sequence of nested closed subspaces $V_j$ in $L^2(\mathbb{R})$ that represent signals at different resolutions.

**The Ladder of Spaces:**
$$ \dots \subset V_2 \subset V_1 \subset V_0 \subset V_{-1} \subset V_{-2} \subset \dots $$
* Note on notation: In this convention, lower indices mean finer resolution. $V_0$ is a reference resolution. $V_{-1}$ has twice the resolution (contains more high-frequency detail). $V_1$ has half the resolution (coarser).
* Property 1: The union of all spaces spans $L^2(\mathbb{R})$: $\overline{\bigcup_{j \in \mathbb{Z}} V_j} = L^2(\mathbb{R})$.
* Property 2: The intersection of all spaces contains only the zero signal: $\bigcap_{j \in \mathbb{Z}} V_j = \{0\}$.
* Property 3: Scale invariance: $x(t) \in V_j \iff x(2t) \in V_{j-1}$.
* Property 4: Shift invariance: $x(t) \in V_0 \iff x(t-k) \in V_0$ for $k \in \mathbb{Z}$.

**Scaling Function:**
There exists a scaling function $\phi(t)$ whose integer translates $\{\phi(t-k)\}_{k\in\mathbb{Z}}$ form an orthonormal basis for $V_0$.

**Wavelet Spaces (The Details):**
Since $V_0$ is a subspace of $V_{-1}$, there is some "missing information" when we go from the finer resolution $V_{-1}$ to the coarser resolution $V_0$. This missing information lives in the orthogonal complement space, $W_0$, such that:
$$ V_{-1} = V_0 \oplus W_0 $$
In general:
$$ V_{j-1} = V_j \oplus W_j $$
The **wavelet function** $\psi(t)$ is designed such that its integer translates $\{\psi(t-k)\}_{k\in\mathbb{Z}}$ form an orthonormal basis for $W_0$. 
Thus, a signal in $V_{-1}$ can be perfectly represented by its coarse approximation in $V_0$ plus its high-frequency details in $W_0$.

### 4.4 The Two-Scale Relations and Filter Banks

Since $V_0 \subset V_{-1}$ and $\phi(2t)$ spans $V_{-1}$, the scaling function $\phi(t) \in V_0$ can be written as a linear combination of the basis functions of $V_{-1}$. This gives the **two-scale relation for the scaling function**:
$$ \phi(t) = \sqrt{2} \sum_{n} h_0[n] \phi(2t - n) $$
Here, $h_0[n]$ are discrete coefficients that form a **lowpass filter**.

Similarly, since $W_0 \subset V_{-1}$, the wavelet function $\psi(t) \in W_0$ can be written in terms of the basis of $V_{-1}$:
$$ \psi(t) = \sqrt{2} \sum_{n} h_1[n] \phi(2t - n) $$
Here, $h_1[n]$ form a **highpass filter**.

This is the Eureka moment of wavelets! The continuous functions $\phi(t)$ and $\psi(t)$ are entirely defined by the discrete filter coefficients $h_0[n]$ and $h_1[n]$. The design of wavelets boils down entirely to the design of perfect discrete filters.

### 4.5 Mallat's Pyramid Algorithm (Iterated Filter Banks)

Because of the two-scale relation, we don't need to compute complicated continuous integrals to find the DWT of a discrete signal $x[n]$. We can use Mallat's Algorithm, which uses standard digital filters and decimators.

**Analysis (Decomposition):**
At level 1, the signal $x[n]$ is passed through the lowpass filter $h_0[-n]$ and highpass filter $h_1[-n]$, followed by downsampling by 2.
* Approximation coefficients (lowpass): $cA_1[k] = \sum_{n} x[n] h_0[2k - n]$
* Detail coefficients (highpass): $cD_1[k] = \sum_{n} x[n] h_1[2k - n]$

At level 2, the algorithm iterates *only on the approximation coefficients* $cA_1$:
* $cA_2[k] = \sum_{n} cA_1[n] h_0[2k - n]$
* $cD_2[k] = \sum_{n} cA_1[n] h_1[2k - n]$

This creates a logarithmic tree structure (Constant-Q). At each successive level, the frequency band is halved, providing finer and finer frequency resolution for lower frequencies.

**Synthesis (Reconstruction):**
To reconstruct the signal, we reverse the process. We upsample the coefficients (insert zeros between samples) and pass them through synthesis filters $g_0[n]$ (lowpass) and $g_1[n]$ (highpass), and add them together.
$$ cA_{j-1}[n] = \sum_{k} cA_j[k] g_0[n - 2k] + \sum_{k} cD_j[k] g_1[n - 2k] $$

### 4.6 Perfect Reconstruction and QMF

For the DWT to be useful, we must be able to perfectly reconstruct the original signal without aliasing or distortion. This imposes strict conditions on the filters $h_0, h_1, g_0, g_1$.

For orthogonal wavelets (like Haar and Daubechies), the filters are related by the **Quadrature Mirror Filter (QMF)** relation. The highpass filter is an alternating-sign, time-reversed version of the lowpass filter:
$$ h_1[n] = (-1)^n h_0[N - 1 - n] $$
where $N$ is the filter length.
The synthesis filters are simply time-reversed versions of the analysis filters:
$$ g_0[n] = h_0[-n] $$
$$ g_1[n] = h_1[-n] $$

### 4.7 Wavelet Families

1. **Haar Wavelet:** 
   * Simplest wavelet. Step function in time domain. 
   * Filter coefficients: $h_0 = [1/\sqrt{2}, 1/\sqrt{2}]$, $h_1 = [1/\sqrt{2}, -1/\sqrt{2}]$.
   * Excellent time resolution, terrible frequency resolution (filters roll off very slowly).
2. **Daubechies Wavelets (dbN):**
   * Designed for maximal flatness in the frequency domain. 
   * Compactly supported and orthogonal. As $N$ increases, they become smoother and frequency localization improves, but time support increases. db1 is identical to Haar.
   * No analytical expression for the continuous wavelet; they are defined strictly by the filter coefficients.
   * Widely used for denoising due to smooth structure mimicking natural signals.
3. **Biorthogonal Wavelets:**
   * Orthogonal wavelets (except Haar) cannot have linear phase (they are asymmetrical). Linear phase is critical in image processing to prevent edge distortion.
   * Biorthogonal wavelets relax the orthogonality constraint, allowing two different scaling/wavelet functions (one for analysis, one for synthesis). 
   * This allows the filters to have linear phase. The CDF 9/7 wavelet is the standard for JPEG 2000.
4. **Symlets:**
   * A modified version of Daubechies wavelets designed to have the least asymmetry possible while remaining compactly supported and orthogonal. Used when phase distortion must be minimized without switching fully to biorthogonal wavelets.

---
## 5. COMPLETE PROOFS AND DERIVATIONS

### Proof 1: The Admissibility Condition implies Zero Mean
**Theorem:** If a mother wavelet $\psi(t)$ satisfies the admissibility condition $C_\psi = \int_0^\infty \frac{|\Psi(\omega)|^2}{\omega}d\omega < \infty$, and its Fourier Transform $\Psi(\omega)$ is continuous at $\omega=0$, then the wavelet has a zero mean: $\int_{-\infty}^{\infty} \psi(t) dt = 0$.

**Proof:**
1. By definition of the Fourier Transform:
   $$ \Psi(\omega) = \int_{-\infty}^{\infty} \psi(t) e^{-j\omega t} dt $$
2. Evaluate at $\omega = 0$:
   $$ \Psi(0) = \int_{-\infty}^{\infty} \psi(t) dt $$
   This is exactly the mean of the wavelet. Let's assume this mean is non-zero, say $\Psi(0) = c \neq 0$.
3. Since $\Psi(\omega)$ is continuous at $\omega=0$, there exists a small region $[0, \epsilon]$ around zero where $|\Psi(\omega)|^2 \approx |c|^2 > 0$.
4. Substitute this into the admissibility integral over the interval $[0, \epsilon]$:
   $$ \int_0^\epsilon \frac{|\Psi(\omega)|^2}{\omega} d\omega \approx \int_0^\epsilon \frac{|c|^2}{\omega} d\omega $$
5. Evaluate the integral:
   $$ |c|^2 \int_0^\epsilon \frac{1}{\omega} d\omega = |c|^2 \left[ \ln(\omega) \right]_0^\epsilon $$
6. As the lower limit approaches $0$, $\ln(\omega) \to -\infty$. Therefore, the integral diverges to infinity.
7. But the admissibility condition explicitly states that the integral from $0$ to $\infty$ must be finite ($< \infty$).
8. Thus, our assumption that $\Psi(0) \neq 0$ must be false. Therefore, $\Psi(0) = 0$, which implies:
   $$ \int_{-\infty}^{\infty} \psi(t) dt = 0 $$
*(Q.E.D.)*

### Proof 2: Perfect Reconstruction Condition in Filter Banks
**Theorem:** In a 2-channel filter bank with analysis filters $H_0(z), H_1(z)$ and synthesis filters $G_0(z), G_1(z)$, perfect reconstruction is achieved if the aliasing term is zero and the distortion term is a pure delay.

**Proof:**
1. Let the input be $X(z)$.
2. After analysis filtering, the signals are $X(z)H_0(z)$ and $X(z)H_1(z)$.
3. Downsampling by 2 (decimation) maps $V(z) \to \frac{1}{2}[V(z^{1/2}) + V(-z^{1/2})]$. So the decimated signals in the Z-domain are:
   $$ Y_0(z) = \frac{1}{2}[X(z^{1/2})H_0(z^{1/2}) + X(-z^{1/2})H_0(-z^{1/2})] $$
   $$ Y_1(z) = \frac{1}{2}[X(z^{1/2})H_1(z^{1/2}) + X(-z^{1/2})H_1(-z^{1/2})] $$
4. Upsampling by 2 (interpolation) maps $Y(z) \to Y(z^2)$. So after upsampling, the signals become:
   $$ U_0(z) = Y_0(z^2) = \frac{1}{2}[X(z)H_0(z) + X(-z)H_0(-z)] $$
   $$ U_1(z) = Y_1(z^2) = \frac{1}{2}[X(z)H_1(z) + X(-z)H_1(-z)] $$
5. The reconstructed output $\hat{X}(z)$ is formed by passing these through the synthesis filters and adding:
   $$ \hat{X}(z) = U_0(z)G_0(z) + U_1(z)G_1(z) $$
6. Substituting the expressions for $U_0$ and $U_1$:
   $$ \hat{X}(z) = \frac{1}{2}[X(z)H_0(z) + X(-z)H_0(-z)]G_0(z) + \frac{1}{2}[X(z)H_1(z) + X(-z)H_1(-z)]G_1(z) $$
7. Rearranging to group the $X(z)$ (desired signal) and $X(-z)$ (aliasing artifact) terms:
   $$ \hat{X}(z) = \frac{1}{2}[H_0(z)G_0(z) + H_1(z)G_1(z)]X(z) + \frac{1}{2}[H_0(-z)G_0(z) + H_1(-z)G_1(z)]X(-z) $$
8. For Perfect Reconstruction, we require $\hat{X}(z) = z^{-L}X(z)$ (the output is exactly the input, possibly delayed by $L$ samples).
9. Therefore, we must satisfy two conditions simultaneously:
   **Condition 1: Alias Cancellation:** The coefficient of $X(-z)$ must be zero.
   $$ H_0(-z)G_0(z) + H_1(-z)G_1(z) = 0 $$
   **Condition 2: No Distortion:** The coefficient of $X(z)$ must be a pure delay.
   $$ H_0(z)G_0(z) + H_1(z)G_1(z) = 2z^{-L} $$
*(Q.E.D.)*

---
## 6. WORKED EXAMPLES (MINIMUM 5 — fully solved)

### Example 1: 1-Level Haar DWT
**Problem statement:** Compute the 1-level Discrete Wavelet Transform of the signal $x = [4, 6, 8, 2]$ using the Haar wavelet. Then, demonstrate perfect reconstruction.
**Solution:**
The Haar analysis filters are:
Lowpass: $h_0 = [\frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}}]$
Highpass: $h_1 = [\frac{1}{\sqrt{2}}, -\frac{1}{\sqrt{2}}]$

**Decomposition:**
We filter and downsample. Let's compute the dot product for each non-overlapping pair.
* Approximation coefficients $cA$:
  $cA[0] = x[0]h_0[0] + x[1]h_0[1] = 4(1/\sqrt{2}) + 6(1/\sqrt{2}) = 10/\sqrt{2} = 5\sqrt{2}$
  $cA[1] = x[2]h_0[0] + x[3]h_0[1] = 8(1/\sqrt{2}) + 2(1/\sqrt{2}) = 10/\sqrt{2} = 5\sqrt{2}$
  $cA = [5\sqrt{2}, 5\sqrt{2}]$
* Detail coefficients $cD$:
  $cD[0] = x[0]h_1[0] + x[1]h_1[1] = 4(1/\sqrt{2}) - 6(1/\sqrt{2}) = -2/\sqrt{2} = -\sqrt{2}$
  $cD[1] = x[2]h_1[0] + x[3]h_1[1] = 8(1/\sqrt{2}) - 2(1/\sqrt{2}) = 6/\sqrt{2} = 3\sqrt{2}$
  $cD = [-\sqrt{2}, 3\sqrt{2}]$

**Reconstruction:**
Synthesis filters for Haar are $g_0 = [\frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}}]$ and $g_1 = [\frac{1}{\sqrt{2}}, -\frac{1}{\sqrt{2}}]$.
Upsample $cA \to cA_{up} = [5\sqrt{2}, 0, 5\sqrt{2}, 0]$
Upsample $cD \to cD_{up} = [-\sqrt{2}, 0, 3\sqrt{2}, 0]$
Convolve $cA_{up}$ with $g_0$:
$y_0[0] = 5\sqrt{2} \cdot \frac{1}{\sqrt{2}} = 5$
$y_0[1] = 5\sqrt{2} \cdot \frac{1}{\sqrt{2}} = 5$
$y_0[2] = 5\sqrt{2} \cdot \frac{1}{\sqrt{2}} = 5$
$y_0[3] = 5\sqrt{2} \cdot \frac{1}{\sqrt{2}} = 5$
$y_0 = [5, 5, 5, 5]$
Convolve $cD_{up}$ with $g_1$:
$y_1[0] = -\sqrt{2} \cdot \frac{1}{\sqrt{2}} = -1$
$y_1[1] = -\sqrt{2} \cdot -\frac{1}{\sqrt{2}} = 1$
$y_1[2] = 3\sqrt{2} \cdot \frac{1}{\sqrt{2}} = 3$
$y_1[3] = 3\sqrt{2} \cdot -\frac{1}{\sqrt{2}} = -3$
$y_1 = [-1, 1, 3, -3]$
Add them together:
$\hat{x} = y_0 + y_1 = [5-1, 5+1, 5+3, 5-3] = [4, 6, 8, 2]$.
This perfectly matches the original signal $x$.
**Physical interpretation:** The approximation coefficients capture the average value of each pair, while the detail coefficients capture the difference. The scaling by $\sqrt{2}$ guarantees that the transformed signal has the exact same energy as the original signal.
**Common mistakes to avoid:** Forgetting to divide/multiply by $\sqrt{2}$. This normalization ensures energy is conserved between domains.

### Example 2: 2-Level Haar DWT and Decomposition Tree
**Problem statement:** Given $x = [4, 6, 8, 2, 10, 12, 2, 6]$, calculate the 2-level Haar DWT and draw the decomposition tree.
**Solution:**
Level 1 Decomposition:
$cA_1[0] = (4+6)/\sqrt{2} = 10/\sqrt{2}$
$cA_1[1] = (8+2)/\sqrt{2} = 10/\sqrt{2}$
$cA_1[2] = (10+12)/\sqrt{2} = 22/\sqrt{2}$
$cA_1[3] = (2+6)/\sqrt{2} = 8/\sqrt{2}$
$cD_1[0] = (4-6)/\sqrt{2} = -2/\sqrt{2}$
$cD_1[1] = (8-2)/\sqrt{2} = 6/\sqrt{2}$
$cD_1[2] = (10-12)/\sqrt{2} = -2/\sqrt{2}$
$cD_1[3] = (2-6)/\sqrt{2} = -4/\sqrt{2}$

Level 2 Decomposition (applied *only* to $cA_1$):
$cA_2[0] = (10/\sqrt{2} + 10/\sqrt{2})/\sqrt{2} = 20/2 = 10$
$cA_2[1] = (22/\sqrt{2} + 8/\sqrt{2})/\sqrt{2} = 30/2 = 15$
$cD_2[0] = (10/\sqrt{2} - 10/\sqrt{2})/\sqrt{2} = 0/2 = 0$
$cD_2[1] = (22/\sqrt{2} - 8/\sqrt{2})/\sqrt{2} = 14/2 = 7$

The final 2-level DWT coefficients are the concatenation of $cA_2, cD_2, cD_1$:
$[10, 15, 0, 7, -\sqrt{2}, 3\sqrt{2}, -\sqrt{2}, -2\sqrt{2}]$

Decomposition Tree:
```
           x (8 points)
           /         \
    cA1 (4 pts)   cD1 (4 pts) -> Final DWT
       /     \
 cA2(2pts) cD2(2pts)
   |         |
Final DWT  Final DWT
```
**Physical interpretation:** The vector $[10, 15]$ represents the very coarse macro-trend of the 8-point signal. $cD_2=[0, 7]$ represents mid-level changes. The coefficients clearly identify where the signal changes happen across scales.
**Common mistakes to avoid:** Students often try to decompose $cD_1$. In standard DWT (Mallat's algorithm), we only decompose the approximation coefficients. Decomposing both branches leads to Wavelet Packets, which is a different transform.

### Example 3: Verifying the QMF Condition for Haar Filters
**Problem statement:** Prove that the Haar wavelet filters satisfy the Quadrature Mirror Filter (QMF) magnitude condition: $|H_0(e^{j\omega})|^2 + |H_1(e^{j\omega})|^2 = 2$.
**Solution:**
The Haar lowpass filter is $h_0 = [\frac{1}{\sqrt{2}}, \frac{1}{\sqrt{2}}]$.
Taking the DTFT:
$H_0(e^{j\omega}) = \frac{1}{\sqrt{2}}(1 + e^{-j\omega})$
Find the magnitude squared:
$|H_0(e^{j\omega})|^2 = H_0(e^{j\omega})H_0^*(e^{j\omega}) = \frac{1}{2}(1 + e^{-j\omega})(1 + e^{j\omega})$
$= \frac{1}{2}(1 + e^{j\omega} + e^{-j\omega} + 1) = \frac{1}{2}(2 + 2\cos(\omega)) = 1 + \cos(\omega)$

The Haar highpass filter is $h_1 = [\frac{1}{\sqrt{2}}, -\frac{1}{\sqrt{2}}]$.
Taking the DTFT:
$H_1(e^{j\omega}) = \frac{1}{\sqrt{2}}(1 - e^{-j\omega})$
Find the magnitude squared:
$|H_1(e^{j\omega})|^2 = H_1(e^{j\omega})H_1^*(e^{j\omega}) = \frac{1}{2}(1 - e^{-j\omega})(1 - e^{j\omega})$
$= \frac{1}{2}(1 - e^{j\omega} - e^{-j\omega} + 1) = \frac{1}{2}(2 - 2\cos(\omega)) = 1 - \cos(\omega)$

Adding them together:
$|H_0(e^{j\omega})|^2 + |H_1(e^{j\omega})|^2 = (1 + \cos(\omega)) + (1 - \cos(\omega)) = 2$.
This condition is perfectly satisfied.
**Physical interpretation:** This proves that the filters are power-complementary. The energy lost by the lowpass filter is exactly captured by the highpass filter, ensuring no information is lost, which is essential for perfect reconstruction. Without this, signal reconstruction would suffer from amplitude distortion.

### Example 4: Energy Compaction
**Problem statement:** Consider a signal that is mostly constant but has one sudden spike: $x = [2, 2, 2, 2, 2, 2, 2, 10]$. Compute its 1-level Haar DWT and compare its energy distribution to the original signal.
**Solution:**
Energy of original signal:
$E_x = 2^2 \times 7 + 10^2 = 28 + 100 = 128$.
Now, compute 1-level Haar DWT:
$cA[0] = (2+2)/\sqrt{2} = 2\sqrt{2}$
$cA[1] = (2+2)/\sqrt{2} = 2\sqrt{2}$
$cA[2] = (2+2)/\sqrt{2} = 2\sqrt{2}$
$cA[3] = (2+10)/\sqrt{2} = 6\sqrt{2}$
$cD[0] = (2-2)/\sqrt{2} = 0$
$cD[1] = (2-2)/\sqrt{2} = 0$
$cD[2] = (2-2)/\sqrt{2} = 0$
$cD[3] = (2-10)/\sqrt{2} = -4\sqrt{2}$
The transformed signal is $X_{DWT} = [2\sqrt{2}, 2\sqrt{2}, 2\sqrt{2}, 6\sqrt{2}, 0, 0, 0, -4\sqrt{2}]$.
Calculate energy of DWT coefficients:
$E_{DWT} = (2\sqrt{2})^2 \times 3 + (6\sqrt{2})^2 + (-4\sqrt{2})^2$
$E_{DWT} = (8) \times 3 + (72) + (32) = 24 + 72 + 32 = 128$.
Energy is perfectly conserved (Parseval's theorem).
Notice that in the detail coefficients, 3 out of 4 values are exactly zero. All the high-frequency energy is compacted into a single coefficient $cD[3]$.
**Physical interpretation:** This is why wavelets are excellent for compression. A sparse representation is achieved because wavelets perfectly isolate the transient. If we used a Fourier transform, the sudden spike would require non-zero coefficients at *all* frequencies, leading to poor energy compaction.

### Example 5: Wavelet Denoising using Thresholding
**Problem statement:** An ECG signal $x$ is contaminated with zero-mean additive white Gaussian noise with variance $\sigma^2 = 1$. The signal length is $N = 256$. A 1-level DWT yields detail coefficients $cD$. Suppose one of the detail coefficients is $cD[15] = 2.5$ and another is $cD[42] = 4.8$. Determine the universal threshold and state whether these coefficients are kept or zeroed under Hard Thresholding. Also explain the difference for Soft Thresholding.
**Solution:**
The universal threshold (Donoho-Johnstone) for wavelet denoising is given by:
$T = \sigma \sqrt{2 \ln(N)}$
Given $\sigma = 1$ and $N = 256$:
$T = 1 \cdot \sqrt{2 \ln(256)}$
$\ln(256) \approx 5.545$
$T = \sqrt{2 \times 5.545} = \sqrt{11.09} \approx 3.33$

Hard Thresholding rule:
If $|cD[k]| < T$, set it to 0.
If $|cD[k]| \ge T$, keep it as is.
For $cD[15] = 2.5$: Since $2.5 < 3.33$, this coefficient is assumed to be noise and is zeroed out: $\hat{cD}[15] = 0$.
For $cD[42] = 4.8$: Since $4.8 \ge 3.33$, this coefficient is assumed to contain a true signal transient and is kept: $\hat{cD}[42] = 4.8$.

Soft Thresholding rule:
If $|cD[k]| < T$, set it to 0.
If $|cD[k]| \ge T$, set it to $\text{sgn}(cD[k])(|cD[k]| - T)$.
For $cD[42] = 4.8$: $\hat{cD}[42] = 4.8 - 3.33 = 1.47$.

**Physical interpretation:** Noise is spread evenly across all wavelet coefficients, but the true signal features are usually compacted into a few large coefficients. The universal threshold is set just high enough to eliminate the vast majority of pure noise coefficients.
**Common mistakes to avoid:** Confusing Hard Thresholding with Soft Thresholding. In Soft Thresholding, the retained coefficients are also shrunk toward zero, which creates smoother reconstructed signals but degrades sharp edges slightly compared to hard thresholding.

---
## 7. ENGINEERING APPLICATIONS AND CASE STUDIES

**1. Image Compression (JPEG 2000 vs standard JPEG):**
Standard JPEG divides an image into 8x8 blocks and applies the DCT (Discrete Cosine Transform). At high compression ratios, the block boundaries do not match up perfectly, resulting in severe "blocking artifacts" (the image looks like a mosaic).
JPEG 2000 does not block the image. Instead, it applies the 2D Discrete Wavelet Transform over the entire image using the CDF 9/7 biorthogonal wavelet. The image is decomposed into LL, LH, HL, and HH subbands recursively. Because wavelets localize smoothly in space, JPEG 2000 degrades smoothly at high compression (blurring instead of blocking) and provides typically 20% better compression ratios. It also allows inherently for progressive decoding (loading lower-resolution approximations first). This scalability is massive for web delivery.

**2. ECG Signal Denoising (Baseline Wander Removal):**
An electrocardiogram (ECG) typically suffers from two types of noise:
a) High-frequency muscle noise or 50/60 Hz powerline interference.
b) Low-frequency baseline wander due to patient respiration (the entire signal slowly drifts up and down).
Using MRA, a 9-level DWT is applied. The level 9 approximation coefficients ($cA_9$) contain frequencies roughly between 0 and 0.5 Hz. By simply setting $cA_9 = 0$ and applying the inverse DWT, the baseline wander is completely removed without distorting the critical low-frequency ST-segments of the cardiac cycle, which standard highpass filtering often destroys due to phase non-linearity. This demonstrates how subband isolation solves major biomedical engineering issues.

**3. FBI Fingerprint Image Compression:**
The FBI digitized 200 million fingerprint cards. Standard JPEG destroyed the high-frequency ridges and minutiae (bifurcations) necessary for matching due to block boundaries acting as false edges. They adopted a wavelet-scalar quantization (WSQ) standard using a specialized biorthogonal wavelet. By adaptively allocating bits to the high-frequency detail subbands containing the ridge lines, they achieved 15:1 compression with zero loss of matching accuracy, a monumental success for wavelets.

**4. Seismic Signal Analysis:**
In seismic exploration, a source sends acoustic waves underground, and reflections are recorded. The subsurface layers are mapped by detecting the exact arrival time of these wavelets. The Continuous Wavelet Transform (CWT) is heavily utilized because it allows geophysicists to precisely locate high-frequency pulse arrivals in time, while also isolating low-frequency rumble artifacts that mask the true data. The time-frequency tiling is ideal for this application.

---
## 8. COMMON STUDENT MISCONCEPTIONS AND ERRORS

1. **Misconception:** The Discrete Wavelet Transform (DWT) is just a sampled version of the Continuous Wavelet Transform (CWT).
   * **Correction:** No. The CWT is evaluated by calculating continuous integrals across heavily redundant, finely spaced scales. The DWT is a strictly non-redundant, orthogonal decomposition evaluated using digital filter banks and decimation (Mallat's algorithm) built upon Multiresolution Analysis.
2. **Misconception:** DWT is exactly the same concept as STFT.
   * **Correction:** STFT uses a fixed window size for all frequencies. DWT uses a variable window size—scaling the mother wavelet—resulting in a dyadic (logarithmic) time-frequency tiling.
3. **Misconception:** The Wavelet Transform is always vastly superior to the Fast Fourier Transform (FFT).
   * **Correction:** It depends heavily on the signal. If the signal is perfectly stationary (e.g., a pure sine wave, or steady-state motor vibration), the FFT is optimal and provides perfect frequency resolution. Wavelets excel specifically when signals are non-stationary, transient, or possess features at multiple vastly different scales.
4. **Misconception:** Any highpass and lowpass filter pair can be used to compute a DWT.
   * **Correction:** To perform a valid DWT and allow for perfect reconstruction, the filters must satisfy stringent QMF conditions (alias cancellation and distortion-free). Arbitrary Butterworth or FIR filters will completely destroy the signal upon reconstruction due to decimation aliasing.
5. **Misconception:** The "Approximation" coefficients are the high frequencies.
   * **Correction:** Students often mix up the outputs. "Approximation" ($cA$) comes from the *Lowpass* filter, representing the slow, coarse trends. "Detail" ($cD$) comes from the *Highpass* filter, representing the fast, fine details.
6. **Misconception:** Orthogonal wavelets can have linear phase.
   * **Correction:** A mathematically proven limitation states that except for the Haar wavelet (which is discontinuous), no real orthogonal wavelet can have generalized linear phase. If linear phase is required (e.g., image processing), we must abandon strict orthogonality and use Biorthogonal wavelets.
7. **Misconception:** The scaling function $\phi(t)$ itself acts as a high-pass filter.
   * **Correction:** The scaling function $\phi(t)$ is associated with the approximation spaces $V_j$ and essentially corresponds to a low-pass filter $h_0[n]$, while the wavelet function $\psi(t)$ corresponds to the high-pass filter $h_1[n]$.

---
## 9. CONNECTIONS TO OTHER LECTURES

* **Builds on Lecture 3 & 4 (Fourier Analysis):** Directly addresses the limitations of the STFT and Heisenberg's uncertainty principle introduced in those lectures.
* **Builds on Lecture 11 (Multirate Signal Processing):** The entire DWT algorithm relies entirely on the decimation and interpolation theory taught in multirate DSP, especially the mathematical handling of aliasing.
* **Builds on Lecture 14 (Filter Design):** The concepts of linear phase and filter constraints are utilized to explain why we use specific wavelets (e.g., why Biorthogonal filters are designed).
* **Connects to Future Courses:** This forms the bedrock for advanced electives like Digital Image Processing, Biomedical Signal Processing, and Speech Processing.

---
## 10. EXAMINATION QUESTIONS

### 10.1 Short Answer

**Q1:** Explain the primary limitation of the Short-Time Fourier Transform (STFT) and how the Wavelet Transform overcomes it.
**Model Answer:** The STFT uses a fixed window size, forcing a compromise: a short window provides good time resolution but poor frequency resolution, while a long window provides good frequency resolution but poor time resolution. The Wavelet Transform overcomes this by using Constant-Q analysis—scaling the window such that high frequencies are analyzed with short windows (good time resolution for transients) and low frequencies with long windows (good frequency resolution).

**Q2:** What does the admissibility condition require of a mother wavelet, and what does this mathematically imply about its mean value?
**Model Answer:** The admissibility condition $C_\psi = \int_0^\infty \frac{|\Psi(\omega)|^2}{\omega}d\omega < \infty$ ensures the transform is invertible. This condition requires that the Fourier transform of the wavelet at zero frequency, $\Psi(0)$, must be exactly zero to prevent the integral from diverging. Since $\Psi(0) = \int \psi(t) dt$, this proves the wavelet must have a zero mean value.

**Q3:** Differentiate between Approximation coefficients and Detail coefficients in a DWT.
**Model Answer:** Approximation coefficients are generated by passing the signal through the lowpass filter branch of the filter bank, representing the coarse, low-frequency trend of the signal. Detail coefficients are generated by the highpass filter branch, capturing the fine, high-frequency transients and edges.

**Q4:** Why is the Haar wavelet not used for advanced audio compression, despite being orthogonal and compactly supported?
**Model Answer:** The Haar wavelet is a step function, meaning it is not continuous or smooth. In the frequency domain, its filter response rolls off very slowly (resembling a sinc function), leading to poor frequency localization. This causes severe spectral leakage, making it unsuitable for high-quality audio compression.

**Q5:** In Mallat's algorithm, why do we decimate by a factor of 2 at each level?
**Model Answer:** Decimation ensures the transform is non-redundant. When a signal is split into lowpass and highpass halves, the bandwidth of each is halved. By Nyquist theorem, we can reduce the sampling rate by a factor of 2 without losing information, keeping the total number of coefficients equal to the length of the original signal.

### 10.2 Long Answer / Numerical Problems

**Problem 1:** Given the input sequence $x[n] = [8, 4, 1, 5]$.
a) Compute the 2-level Haar DWT. Show all filter convolutions and downsampling steps explicitly.
b) Demonstrate the perfect reconstruction of the signal from the 2-level DWT coefficients.
**Solution:**
a) **Level 1:**
$cA_1[0] = (8+4)/\sqrt{2} = 12/\sqrt{2} = 6\sqrt{2}$
$cA_1[1] = (1+5)/\sqrt{2} = 6/\sqrt{2} = 3\sqrt{2}$
$cD_1[0] = (8-4)/\sqrt{2} = 4/\sqrt{2} = 2\sqrt{2}$
$cD_1[1] = (1-5)/\sqrt{2} = -4/\sqrt{2} = -2\sqrt{2}$
**Level 2:** (Apply to $cA_1$)
$cA_2[0] = (6\sqrt{2} + 3\sqrt{2})/\sqrt{2} = 9$
$cD_2[0] = (6\sqrt{2} - 3\sqrt{2})/\sqrt{2} = 3$
Final DWT vector: $[cA_2[0], cD_2[0], cD_1[0], cD_1[1]] = [9, 3, 2\sqrt{2}, -2\sqrt{2}]$.

b) **Reconstruction Level 2 to 1:**
Upsample $cA_2 \to [9, 0]$ and $cD_2 \to [3, 0]$.
Apply $g_0 = [1/\sqrt{2}, 1/\sqrt{2}]$ to $cA_{2,up}$: $[9/\sqrt{2}, 9/\sqrt{2}]$.
Apply $g_1 = [1/\sqrt{2}, -1/\sqrt{2}]$ to $cD_{2,up}$: $[3/\sqrt{2}, -3/\sqrt{2}]$.
Add: $cA_1 = [12/\sqrt{2}, 6/\sqrt{2}]$. (Matches intermediate step!)
**Reconstruction Level 1 to 0:**
Upsample $cA_1 \to [12/\sqrt{2}, 0, 6/\sqrt{2}, 0]$.
Upsample $cD_1 \to [2\sqrt{2}, 0, -2\sqrt{2}, 0]$.
Apply $g_0$ to $cA_{1,up}$: $[12/2, 12/2, 6/2, 6/2] = [6, 6, 3, 3]$.
Apply $g_1$ to $cD_{1,up}$: $[2, -2, -2, 2]$.
Add: $\hat{x} = [6+2, 6-2, 3-2, 3+2] = [8, 4, 1, 5]$. Signal perfectly reconstructed.

**Problem 2:** Prove mathematically that the alias cancellation condition $G_0(z)H_0(-z) + G_1(z)H_1(-z) = 0$ is satisfied by the Quadrature Mirror Filter (QMF) definitions where $H_1(z) = H_0(-z)$ and the synthesis filters are $G_0(z) = H_0(z)$ and $G_1(z) = -H_1(z)$. (Note: This is a specific QMF structure variant).
**Solution:**
Substitute the definitions into the alias cancellation equation:
Term 1: $G_0(z)H_0(-z) = H_0(z)H_0(-z)$
Term 2: $G_1(z)H_1(-z) = [-H_1(z)][H_1(-z)]$
Since $H_1(z) = H_0(-z)$, then $H_1(-z) = H_0(-(-z)) = H_0(z)$.
Substitute these back into Term 2:
Term 2 = $[-H_0(-z)][H_0(z)] = -H_0(z)H_0(-z)$
Add Term 1 and Term 2:
$H_0(z)H_0(-z) - H_0(z)H_0(-z) = 0$.
The aliasing terms completely cancel out. Q.E.D.

**Problem 3:** In Multiresolution Analysis, state the two-scale relations for the scaling function $\phi(t)$ and the wavelet function $\psi(t)$. Explain how these continuous equations justify the discrete Mallat filtering algorithm.
**Solution:**
Scaling equation: $\phi(t) = \sqrt{2} \sum h_0[n] \phi(2t-n)$
Wavelet equation: $\psi(t) = \sqrt{2} \sum h_1[n] \phi(2t-n)$
These equations demonstrate that the continuous basis functions at a lower resolution ($V_0, W_0$) are purely linear combinations of the basis functions at a higher resolution ($V_{-1}$), scaled by discrete coefficients $h_0[n]$ and $h_1[n]$. Because the functions are nested, taking the inner product of a signal with these basis functions (which defines the wavelet transform) reduces to a discrete convolution of the signal samples with the filters $h_0$ and $h_1$. This bridges the continuous function spaces with discrete digital filters, making it computable via Mallat's algorithm.

**Problem 4:** An engineer applies a 4-level DWT to a 1024-point signal. 
a) State the lengths of all resulting coefficient vectors ($cA_4, cD_4, cD_3, cD_2, cD_1$). 
b) Verify that the total number of coefficients equals 1024.
**Solution:**
a) Because of decimation by 2 at each stage:
Level 1 outputs: $cA_1$ (512 points), $cD_1$ (512 points)
Level 2 outputs (from $cA_1$): $cA_2$ (256 points), $cD_2$ (256 points)
Level 3 outputs (from $cA_2$): $cA_3$ (128 points), $cD_3$ (128 points)
Level 4 outputs (from $cA_3$): $cA_4$ (64 points), $cD_4$ (64 points)
The final subbands are $cA_4, cD_4, cD_3, cD_2, cD_1$.
Their lengths are 64, 64, 128, 256, and 512, respectively.
b) Sum of lengths: $64 + 64 + 128 + 256 + 512 = 1024$. The total number of coefficients is conserved.

**Problem 5:** Suppose you are given a 1D signal representing an image scanline. Explain conceptually how the Haar DWT acts as a simple edge detector. Provide a 4-point numerical example to justify your answer.
**Solution:**
Conceptually, the Haar wavelet highpass filter $h_1 = [1/\sqrt{2}, -1/\sqrt{2}]$ computes the difference between adjacent samples. When a signal is flat (constant), the difference is zero. When there is a sudden change (an edge), the difference is non-zero, resulting in a large detail coefficient.
Example: Consider a signal with a step edge: $x = [2, 2, 8, 8]$.
Apply the Haar level 1 detail filter:
$cD[0] = (x[0] \cdot 1/\sqrt{2}) + (x[1] \cdot -1/\sqrt{2}) = (2-2)/\sqrt{2} = 0$.
$cD[1] = (x[2] \cdot 1/\sqrt{2}) + (x[3] \cdot -1/\sqrt{2}) = (8-8)/\sqrt{2} = 0$.
Wait, the downsampling means we shift by 2.
Let's re-evaluate without downsampling (stationary wavelet transform style) to find the exact edge location.
Convolution with $h_1 = [1/\sqrt{2}, -1/\sqrt{2}]$:
$y[0] = 2(1/\sqrt{2})$ (boundary)
$y[1] = 2(1/\sqrt{2}) - 2(1/\sqrt{2}) = 0$
$y[2] = 8(1/\sqrt{2}) - 2(1/\sqrt{2}) = 6/\sqrt{2}$
$y[3] = 8(1/\sqrt{2}) - 8(1/\sqrt{2}) = 0$
The output $y$ clearly has a peak of $6/\sqrt{2}$ exactly at the index where the edge occurs (transition from 2 to 8). The flat regions yield exactly 0. This demonstrates how the wavelet coefficients directly isolate the high-frequency edge information in the spatial domain.

### 10.3 True/False with Justification

1. **True/False:** The continuous wavelet transform $W_x(a,b)$ evaluates frequency by varying the translation parameter $b$.
   * **False.** The parameter $b$ controls time localization (translation). The scale parameter $a$ controls frequency localization by dilating or compressing the wavelet.
2. **True/False:** Daubechies wavelets have a closed-form analytical mathematical expression in the continuous time domain.
   * **False.** Daubechies wavelets are defined strictly through their discrete filter coefficients. They do not have an explicit analytical formula in continuous time.
3. **True/False:** For image processing applications, biorthogonal wavelets are preferred over orthogonal wavelets because they can have linear phase.
   * **True.** Non-linear phase introduces severe phase distortion (edge blurring) in images. Only biorthogonal wavelets (and the Haar orthogonal wavelet) offer linear phase filters.
4. **True/False:** In Mallat's algorithm, decimation is applied to both the approximation and detail coefficients before iterating the next level on the detail coefficients.
   * **False.** Mallat's standard DWT algorithm iterates *only* on the approximation coefficients, leaving the detail coefficients untouched after generation.
5. **True/False:** Hard thresholding a wavelet coefficient sets it to zero if its magnitude is below a certain threshold.
   * **True.** Hard thresholding acts as an absolute gate: coefficients below $T$ become zero, and those above $T$ remain completely unchanged.
6. **True/False:** Wavelet analysis uses a constant-Q windowing approach, meaning the ratio of center frequency to bandwidth is constant across all scales.
   * **True.** This is the defining characteristic of wavelet time-frequency tiling, making it superior for analyzing non-stationary signals with transient high frequencies and slow low frequencies.
7. **True/False:** The Haar wavelet is the only real-valued orthogonal wavelet with compact support that is symmetric (linear phase).
   * **True.** A famous theorem by Daubechies proves that no other real, compactly supported, orthogonal wavelets can be symmetric. This is why biorthogonal wavelets were invented for image compression.
8. **True/False:** In Mallat's synthesis algorithm, we only upsample the approximation coefficients, not the detail coefficients.
   * **False.** Both the approximation coefficients from level $j$ and the detail coefficients from level $j$ must be upsampled by 2 and passed through their respective synthesis filters to perfectly reconstruct the approximation coefficients at level $j-1$.
9. **True/False:** The CWT uses a fixed number of scales, while the DWT analyzes over continuous scales.
   * **False.** The exact opposite is true. The CWT computes the transform over a continuous range of scales and translations (highly redundant). The DWT evaluates scales and translations only on a discrete dyadic grid ($a=2^j, b=k2^j$), making it non-redundant and computationally efficient via filter banks.
10. **True/False:** An ECG signal sampled at 500 Hz decomposed with an 8-level DWT will have its level 8 approximation coefficients ($cA_8$) representing a frequency band starting from exactly 0 Hz.
    * **True.** The lowpass branch repeatedly halves the frequency range, keeping the DC component. After $j$ levels, the $cA_j$ subband spans roughly $[0, F_s / 2^{j+1}]$.

### 10.4 Conceptual Essay Questions

**Q1:** Compare and contrast the Short-Time Fourier Transform (STFT) and the Discrete Wavelet Transform (DWT) regarding their resolution in the time-frequency plane. Use diagrams (in words) to support your answer.
**Model Answer:** The STFT divides the time-frequency plane into uniform rectangular tiles of equal area and equal aspect ratio. A high-frequency bin has the same time duration as a low-frequency bin, leading to poor time resolution for fast transients if the window is long. In contrast, the DWT divides the plane into variable-sized tiles (though still of equal area due to the uncertainty principle). At high frequencies, the tiles are tall and narrow (wide bandwidth, short time duration), providing excellent time resolution for transients. At low frequencies, the tiles are short and wide (narrow bandwidth, long time duration), providing precise frequency resolution for slow trends.

**Q2:** Explain the role of the orthogonal complement space $W_j$ in Multiresolution Analysis. Why is it necessary alongside $V_j$?
**Model Answer:** The approximation space $V_j$ captures the signal at a specific resolution scale. When moving to a coarser resolution $V_{j+1}$, some fine details are lost. MRA formally captures this lost information by defining $W_{j+1}$ as the orthogonal complement of $V_{j+1}$ inside $V_j$, meaning $V_j = V_{j+1} \oplus W_{j+1}$. The space $V_j$ is spanned by the scaling function $\phi$, while the "detail space" $W_j$ is spanned by the wavelet function $\psi$. Without $W_j$, we would only be smoothing the signal recursively (low-pass filtering) without retaining the information needed to reconstruct the original signal perfectly.

---
## 11. KEY FORMULAS REFERENCE

| Concept | Mathematical Equation |
|---------|-----------------------|
| Continuous Wavelet Transform (CWT) | $W_x(a,b) = \frac{1}{\sqrt{\|a\|}} \int_{-\infty}^{\infty} x(t)\psi^*\left(\frac{t-b}{a}\right)dt$ |
| Inverse CWT | $x(t) = \frac{1}{C_\psi} \int_0^\infty \int_{-\infty}^\infty W_x(a,b) \frac{1}{\sqrt{\|a\|}} \psi\left(\frac{t-b}{a}\right) db \frac{da}{a^2}$ |
| Admissibility Condition | $C_\psi = \int_0^\infty \frac{\|\Psi(\omega)\|^2}{\omega}d\omega < \infty$ |
| Wavelet Mean Value Property | $\int_{-\infty}^{\infty} \psi(t) dt = 0$ |
| Two-Scale Scaling Equation | $\phi(t) = \sqrt{2}\sum_{k} h_0[k]\phi(2t-k)$ |
| Two-Scale Wavelet Equation | $\psi(t) = \sqrt{2}\sum_{k} h_1[k]\phi(2t-k)$ |
| Approximation Coefficients ($cA$) | $cA_j[k] = \sum_{n} cA_{j-1}[n] h_0[2k-n]$ |
| Detail Coefficients ($cD$) | $cD_j[k] = \sum_{n} cA_{j-1}[n] h_1[2k-n]$ |
| QMF Filter Relation (Orthogonal) | $h_1[n] = (-1)^n h_0[N-1-n]$ |
| Alias Cancellation Condition | $G_0(z)H_0(-z) + G_1(z)H_1(-z) = 0$ |
| Distortion-Free Condition | $G_0(z)H_0(z) + G_1(z)H_1(z) = 2z^{-L}$ |
| Universal Denoising Threshold | $T = \sigma \sqrt{2 \ln(N)}$ |

---
## 12. FURTHER READING AND REFERENCES

For faculty preparing exams or students requiring deep mathematical rigor, refer to the following canonical texts:

1. **Proakis, J. G., & Manolakis, D. G. (2006).** *Digital Signal Processing: Principles, Algorithms, and Applications (4th Ed.)*. 
   * *Reference:* Section on Filter Banks and Multiresolution. Excellent for QMF condition proofs.
2. **Oppenheim, A. V., & Schafer, R. W. (2009).** *Discrete-Time Signal Processing (3rd Ed.)*. 
   * *Reference:* Chapter 11 (Multirate Signal Processing).
3. **Mallat, S. (1999).** *A Wavelet Tour of Signal Processing (3rd Ed.)*. 
   * *Reference:* The absolute bible of wavelet theory. Chapters 6 and 7 cover MRA and orthogonal filter banks in exhaustive detail. Highly recommended for understanding the transition from continuous $L^2(\mathbb{R})$ spaces to discrete filters.
4. **Vetterli, M., & Kovačević, J. (1995).** *Wavelets and Subband Coding*. 
   * *Reference:* Excellent resource for the connection between engineering filter banks and mathematical wavelets.
5. **Strang, G., & Nguyen, T. (1996).** *Wavelets and Filter Banks*. 
   * *Reference:* Provides incredible intuition into the linear algebra of wavelets and its connection to filter banks, perfect for EEE students wanting to bridge matrix theory and signal processing.
6. **Burrus, C. S., Gopinath, R. A., & Guo, H. (1998).** *Introduction to Wavelets and Wavelet Transforms: A Primer*. 
   * *Reference:* A great introductory text for DSP students finding Mallat too dense. Explains the transition from Fourier to Wavelets extremely clearly.
7. **Daubechies, I. (1992).** *Ten Lectures on Wavelets*. 
   * *Reference:* The original mathematical text that introduced compactly supported orthogonal wavelets. Required reading for students doing advanced mathematical DSP research.
8. **Vaidyanathan, P. P. (1993).** *Multirate Systems and Filter Banks*. 
   * *Reference:* The definitive guide to multirate filter banks. Provides rigorous proofs for QMF and PR conditions.
9. **Cohen, A., Daubechies, I., & Feauveau, J.-C. (1992).** *Biorthogonal bases of compactly supported wavelets*. 
   * *Reference:* The seminal paper introducing the biorthogonal wavelets used in JPEG 2000. Excellent for showing students how original research transitions into global engineering standards.
10. **Rioul, O., & Vetterli, M. (1991).** *Wavelets and Signal Processing*. 
    * *Reference:* IEEE Signal Processing Magazine. A fantastic tutorial paper that visually and intuitively explains the constant-Q time-frequency tiling. Perfect supplementary reading to assign to students before the lecture.
</Faculty Notes — Lecture 18: Wavelet Transform & Multiresolution Analysis>
