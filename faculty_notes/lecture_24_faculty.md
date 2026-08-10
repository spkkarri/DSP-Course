<Faculty Notes — Lecture 24: Linear Prediction & Speech Processing>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY

This lecture introduces Linear Prediction (LP), a cornerstone of modern speech processing, and its applications such as vocoders, speech recognition (MFCCs), and pitch detection. Students often find the transition from abstract $z$-domain filtering to real-world speech production somewhat abrupt. The mathematical leap into Yule-Walker equations and the Levinson-Durbin algorithm can be intimidating due to matrix algebra and recursive definitions.

**How to teach this lecture:**
1. Begin with the biological intuition: lungs (source), vocal cords (periodic or noise excitation), vocal tract (filter). Connect this physically to the math $H(z)$. Draw analogies to electrical circuits (source/load) and acoustic tubes (lossless tube models).
2. When discussing LP, explain the core idea conceptually before diving into the mean squared error minimization. The idea is simple: the next sample is a linear combination of previous samples. Show how this relates to Taylor series expansion in continuous time, but adapted for discrete samples.
3. The Yule-Walker derivation is a straightforward optimization problem (setting derivatives to zero). Emphasize that the resulting matrix is Toeplitz, which is why we don't just use standard matrix inversion. Distinguish between the Autocorrelation method (which yields a Toeplitz matrix and guarantees stability) and the Covariance method (which does not).
4. The Levinson-Durbin algorithm should be taught primarily conceptually for large $p$, but work through a $p=2$ or $p=3$ case fully by hand so they see how the reflection coefficients $k_m$ evolve. Relate the reflection coefficients to physical reflections at the boundaries of cylindrical tube sections in the vocal tract.
5. Emphasize Line Spectral Frequencies (LSFs) as the modern replacement for reflection coefficients in quantization.
6. In Cepstrum analysis, emphasize the "deconvolution via logarithm" trick. It’s a very elegant mathematical solution to an otherwise difficult separation problem. Walk through the math of transforming convolution to addition step-by-step.
7. When discussing MFCCs, connect the Mel scale to the non-linear frequency resolution of the human basilar membrane.

**Prerequisite checks:**
- Basic understanding of $z$-transforms, regions of convergence, and LTI systems.
- Familiarity with autocorrelation of deterministic and random signals, and power spectral density.
- Basic matrix algebra (multiplication, solving systems of linear equations, positive definite matrices).
- Orthogonality principle from basic probability and random variables.

**Suggested demos:**
- Play a synthesized speech signal using only the vocal tract filter and a pulse train, then change the pitch by changing the pulse train period without changing the filter. (This proves the source and filter are independent).
- Show a spectrogram of a speech signal and overlay the LPC spectral envelope to demonstrate how LPC captures formants.
- Demonstrate pitch tracking using autocorrelation or AMDF in a Python/MATLAB live script, showing how frame size affects tracking accuracy.
- Show the effect of varying the LPC order $p$. Start at $p=2$ (underfitting) up to $p=50$ (overfitting the harmonics).

---
## 1. LEARNING OBJECTIVES

By the end of this comprehensive lecture and corresponding assignments, students will be able to:
1. **Explain** the source-filter model of speech production in detail, distinguishing between voiced and unvoiced excitation, and mathematically model the vocal tract as a time-varying all-pole filter $1/A(z)$.
2. **Formulate** the linear prediction problem and rigorously derive the normal equations (Yule-Walker equations) by minimizing the mean squared prediction error, clearly differentiating between the Autocorrelation and Covariance formulations.
3. **Analyze** the Levinson-Durbin recursive algorithm for solving Toeplitz systems in $O(p^2)$ time, and mathematically evaluate the stability of the resulting synthesis filter using PARCOR (reflection) coefficients.
4. **Compare** Direct Form I/II filter realizations with Lattice Filter structures, explaining why lattice structures based on reflection coefficients are highly preferred in speech applications due to quantization robustness.
5. **Design** the architecture of an LPC vocoder (e.g., LPC-10), specifying the exact parameters extracted during analysis (pitch, gain, reflection coefficients/LSFs, voicing flag) and synthesizing speech from these quantized parameters.
6. **Apply** homomorphic signal processing (Cepstrum) to mathematically deconvolve the excitation source from the vocal tract filter, and interpret the quefrency domain to identify pitch and formant structure.
7. **Calculate** Mel-Frequency Cepstral Coefficients (MFCCs) step-by-step from a speech signal frame, justifying the use of the Mel scale filterbank and the Discrete Cosine Transform (DCT) for decorrelation.
8. **Evaluate** and compare various pitch detection algorithms (Autocorrelation, AMDF, Cepstral peak picking), analyzing their algorithmic complexity, robustness to noise, and susceptibility to common failure modes such as octave errors.

---
## 2. PREREQUISITE KNOWLEDGE REVIEW

Before diving into speech processing, students must be perfectly fluent with the following foundational concepts:

### 2.1 Autocorrelation Function and Stationarity
For a discrete-time wide-sense stationary (WSS) random process $x[n]$, the true autocorrelation sequence $R_{xx}[m]$ is defined as an expectation:
$$ R_{xx}[m] = E\{ x[n]x[n-m] \} $$
For a deterministic, finite-energy signal, the time-average (deterministic) autocorrelation is:
$$ R_{xx}[m] = \sum_{n=-\infty}^{\infty} x[n]x[n-m] $$
**Key properties:**
1. Autocorrelation is an even function: $R_{xx}[-m] = R_{xx}[m]$.
2. It achieves its absolute maximum at the origin: $|R_{xx}[m]| \le R_{xx}[0]$.
3. $R_{xx}[0]$ represents the average power (for WSS signals) or total energy (for finite-energy signals) of the signal.
4. The Fourier transform of the autocorrelation sequence is the Power Spectral Density (PSD), $S_{xx}(\omega)$, which is always real and non-negative.

### 2.2 All-Pole Filters (Autoregressive Models)
An LTI system described by a difference equation with no feedforward terms (other than the current input) is an all-pole filter (also known as an Autoregressive or AR model in statistics):
$$ y[n] = G \cdot x[n] - \sum_{k=1}^{p} a_k y[n-k] $$
Applying the $z$-transform, its transfer function is:
$$ H(z) = \frac{Y(z)}{X(z)} = \frac{G}{1 + \sum_{k=1}^{p} a_k z^{-k}} $$
For this system to be bounded-input bounded-output (BIBO) stable, all roots of the denominator polynomial $A(z) = 1 + \sum_{k=1}^{p} a_k z^{-k}$ (the poles) must lie strictly inside the unit circle ($|z| < 1$).

### 2.3 Optimization by Differentiation (Calculus Review)
To find the minimum of a quadratic cost function $J$ with respect to a set of parameters $a_k$, we compute the partial derivatives and set them to zero:
$$ \frac{\partial J}{\partial a_k} = 0 \quad \text{for } k=1, 2, \dots, p $$
Since the mean squared error surface in linear prediction is a multi-dimensional paraboloid (a quadratic form with a positive definite Hessian matrix), the critical point found by setting the gradient to zero is guaranteed to be the unique global minimum.

### 2.4 The Orthogonality Principle
From estimation theory, the optimal linear estimator (which minimizes the mean squared error) yields an error vector that is orthogonal to the data space used for the estimation.
If $\hat{x}[n]$ is estimated using data $x[n-1], \dots, x[n-p]$, then the optimal error $e[n] = x[n] - \hat{x}[n]$ satisfies:
$$ E\{ e[n] x[n-k] \} = 0 \quad \text{for } k = 1, 2, \dots, p $$
This principle will provide a highly elegant shortcut for deriving the normal equations.

---
## 3. HISTORICAL AND MOTIVATIONAL CONTEXT

**Who discovered this?**
The dream of synthesizing human speech began with Homer Dudley's VODER (Voice Operating Demonstrator), a massive analog machine demonstrated at the 1939 New York World's Fair. The operator used a keyboard to manually control resonant filters and a pitch pedal, effectively becoming the first human-operated "vocoder".
The rigorous mathematical foundations of linear prediction date back to the work of Norbert Wiener and Andrey Kolmogorov in the 1940s, who developed Wiener filter theory for continuous-time signals (primarily for anti-aircraft fire control systems during WWII).
In the late 1960s and early 1970s, the transition to digital signal processing allowed researchers like Fumitada Itakura, Shuzo Saito (NTT in Japan), and Bishnu S. Atal (Bell Labs in the US) to adapt these techniques specifically for digital speech processing. This led to the creation of the LPC (Linear Predictive Coding) algorithm.
The highly efficient Levinson-Durbin algorithm is named after Norman Levinson, who published the $O(p^2)$ algorithm in 1947, and James Durbin, who generalized it in 1960.
The concept of the Cepstrum was coined by Bogert, Healy, and Tukey in 1963 to detect echoes in seismic signals, and later adapted for speech by Alan Oppenheim.

**Real Engineering Applications:**
- **Telecommunications and Mobile Networks:** LPC is the absolute foundation of digital cellular voice compression. The GSM full-rate codec (13 kbps) uses RPE-LTP (Regular Pulse Excitation - Long Term Prediction), an extension of basic LPC. The US Department of Defense standard LPC-10 achieves highly intelligible (though synthetic-sounding) speech at just 2.4 kbps, enabling secure encrypted voice over very narrow tactical radio channels.
- **Automatic Speech Recognition (ASR):** MFCCs, developed in the 1980s by Davis and Mermelstein, remain the standard acoustic feature representation for speech recognition systems. From early Hidden Markov Models (HMMs) to modern deep learning architectures (like Whisper or Wav2Vec), transforming the raw waveform into MFCCs or Mel-filterbanks is step zero.
- **Voice Biometrics and Forensics:** Speaker identification systems rely heavily on the spectral envelope modeled by LPC and MFCCs, as the physiological dimensions of the vocal tract (which dictate the formant frequencies) are physically unique to each individual.

**Why does an EEE student need this?**
Electrical and Electronics Engineers design the physical layer communication systems, IoT devices, and embedded systems that process voice. Understanding how to compress a 64 kbps raw PCM audio stream down to 2.4 kbps without losing intelligibility is a masterclass in information theory and signal processing. It requires a deep understanding of what information is actually necessary for the human brain to perceive speech (the formants and pitch) and throwing away the redundant waveform details.

---
## 4. THEORETICAL FOUNDATIONS

### 4.1 The Complete Source-Filter Model of Speech Production
Human speech is mechanically generated by expelling air from the lungs, modulating it at the glottis (vocal cords), and filtering it through the vocal tract (throat, mouth, nose). The source-filter model assumes these two operations (modulation and filtering) are linearly independent and separable.

**The Source (Excitation Model):**
- **Voiced Speech:** For sounds like vowels (/a/, /i/, /u/) and voiced consonants (/z/, /v/), the vocal cords are tensed. As air is forced through, the Bernoulli effect causes them to rapidly open and close, generating a quasi-periodic train of air pulses.
  The fundamental frequency of this vibration is the **pitch** ($F_0$). Typical pitch ranges are 80-150 Hz for adult males and 150-250 Hz for adult females.
  In a rigorous model (like the Rosenberg glottal pulse model), the excitation is not a perfect impulse train, but a sequence of asymmetric pulses (gradual opening, rapid closure). The rapid closure is what generates the high-frequency harmonics that excite the vocal tract.
- **Unvoiced Speech:** For sounds like fricatives (/s/, /f/, /sh/), the vocal cords are fully open and relaxed (no periodic vibration). Instead, air is forced through a narrow constriction in the mouth (e.g., teeth or lips). This turbulent airflow is modeled as a random white noise source.
- **Mixed Excitation:** Some sounds, like voiced fricatives (/v/, /z/), involve both periodic vocal cord vibration and turbulent noise simultaneously. Standard LPC struggles with this, forcing a hard Voiced OR Unvoiced decision.

**The Filter (Vocal Tract Model):**
The vocal tract from the glottis to the lips acts as an acoustic tube with a varying cross-sectional area. It has specific resonant frequencies called **formants** (denoted F1, F2, F3, etc.). The vocal tract shapes the broad, flat spectrum of the excitation source, amplifying frequencies near the formants and attenuating others.
Using acoustic tube modeling (modeling the tract as a concatenation of discrete cylindrical segments), it can be shown that if the tube is completely unconstricted at the lips and closed at the glottis, its transfer function is exclusively comprised of poles.
We model the vocal tract as a time-varying, all-pole digital filter $H(z)$:
$$ H(z) = \frac{G}{A(z)} = \frac{G}{1 + \sum_{k=1}^{p} a_k z^{-k}} $$
where $G$ is a gain factor representing signal energy, and $a_k$ are the linear prediction coefficients. $p$ is the predictor order.
*Rule of thumb for order $p$:* The human vocal tract has roughly one formant (one complex conjugate pole pair, requiring 2 poles) per 1000 Hz of bandwidth. For an 8 kHz sampled speech signal, the Nyquist frequency is 4 kHz, so there are ~4 formants. This requires 8 poles. We add 2-4 extra poles to model the radiation characteristics of the lips and the glottal pulse shape, resulting in an optimal order of $p = 10$ to $12$.

### 4.2 Acoustic Tube Modeling: The Physics of LPC
To truly appreciate the coefficients $a_k$, one must look at the lossless tube model of the vocal tract. Imagine the vocal tract approximated by $p$ concatenated cylindrical tubes, each of length $l = c \cdot T / 2$, where $c$ is the speed of sound and $T$ is the sampling period. 
Each junction between tube $m$ and tube $m+1$ has a change in cross-sectional area, from $A_m$ to $A_{m+1}$. 
According to acoustic physics, an acoustic wave traveling through this tube will experience partial reflection and partial transmission at every boundary. The reflection coefficient at boundary $m$ is given by:
$$ k_m = \frac{A_{m+1} - A_m}{A_{m+1} + A_m} $$
Because cross-sectional areas must be positive ($A_m > 0$), it mathematically follows that $-1 < k_m < 1$.
The Levinson-Durbin algorithm magically extracts these exact physical reflection coefficients directly from the time-domain speech signal. Thus, LPC is not just a mathematical curve-fitting tool; it is actively deducing the physical shape of the speaker's throat in real-time.

### 4.3 Linear Prediction Analysis Formulation
Speech is non-stationary over long periods, but for very short intervals (10 to 30 ms), the vocal tract shape remains relatively constant. We divide the signal into overlapping frames and perform LP analysis on each frame independently.

**The Prediction Equation:**
The foundational premise of LP is that the current speech sample $x[n]$ is highly correlated with its immediate past. We can predict $x[n]$ using a linear combination of the past $p$ samples:
$$ \hat{x}[n] = -\sum_{k=1}^{p} a_k x[n-k] $$
*(Note: The negative sign is a strictly mathematical convention used in DSP to ensure the filter polynomial is written as $A(z) = 1 + a_1 z^{-1} + a_2 z^{-2} \dots$ instead of $1 - a_1 z^{-1} \dots$. Both conventions exist in literature, but Proakis/Manolakis use the negative sign).*

**The Prediction Error (Residual):**
The difference between the actual sample $x[n]$ and our predicted sample $\hat{x}[n]$ is the prediction error (or residual), $e[n]$:
$$ e[n] = x[n] - \hat{x}[n] = x[n] + \sum_{k=1}^{p} a_k x[n-k] $$
Taking the $z$-transform of both sides gives:
$$ E(z) = X(z) + \sum_{k=1}^{p} a_k z^{-k} X(z) = X(z)\left( 1 + \sum_{k=1}^{p} a_k z^{-k} \right) $$
$$ E(z) = X(z)A(z) $$
The polynomial $A(z)$ is known as the **inverse filter** or **analysis filter**. It takes the highly correlated speech signal $X(z)$ and flattens its spectrum, outputting the uncorrelated residual $E(z)$. If the LP model perfectly matched the vocal tract, $E(z)$ would be exactly equal to the original excitation source (a pure impulse train or pure white noise).

### 4.4 The Two Formulations: Autocorrelation vs. Covariance Method
To find the optimal coefficients $a_k$, we minimize the total squared error $E$.
$$ E = \sum_{n} e^2[n] = \sum_{n} \left( x[n] + \sum_{k=1}^{p} a_k x[n-k] \right)^2 $$
The limits of the summation over $n$ determine the specific method used.

**1. The Autocorrelation Method:**
We assume the speech frame $x[n]$ is multiplied by a window function $w[n]$ (like a Hamming window) of length $N$, so $x[n]$ is identically zero outside $0 \le n \le N-1$.
The summation is taken from $n = -\infty$ to $\infty$ (though it is only non-zero for $0 \le n \le N-1+p$).
This formulation leads to the classic Yule-Walker equations with a Toeplitz autocorrelation matrix.
*Advantage:* Guarantees the resulting filter $1/A(z)$ is stable.
*Disadvantage:* Windowing distorts the spectral envelope slightly (widens the formants).

**2. The Covariance Method:**
We do not apply a window that forces the signal to zero at the boundaries. Instead, we minimize the error strictly over a finite interval $n = 0$ to $N-1$. Because the prediction filter requires $p$ past samples, we must have access to unwindowed samples from $n = -p$ to $N-1$.
This leads to a system of equations involving the covariance matrix, which is symmetric but NOT Toeplitz.
*Advantage:* Higher spectral resolution, no windowing distortion.
*Disadvantage:* Does NOT guarantee filter stability (poles can be outside the unit circle), and cannot use Levinson-Durbin (must use Cholesky decomposition, $O(p^3)$).
For this lecture, we focus entirely on the Autocorrelation method.

### 4.5 The Levinson-Durbin Algorithm Details
Solving $\mathbf{R}\mathbf{a} = -\mathbf{r}$ directly takes $O(p^3)$ operations. The Levinson-Durbin algorithm leverages the fact that a Toeplitz matrix contains massive redundancy. It solves the system recursively, generating optimal predictors of order $m=1$, then $m=2$, all the way up to $m=p$.

For each step $m$, we compute a **reflection coefficient** (or PARCOR coefficient) $k_m$.
The physical interpretation of $k_m$ is fascinating: if we model the vocal tract as a series of $p$ interconnected cylindrical tubes of different cross-sectional areas, $k_m$ represents the acoustic reflection coefficient at the boundary between the $m$-th and $(m+1)$-th tube.

**Strict Stability Criterion:**
A profound theorem in signal processing states that the all-pole filter $H(z) = 1/A(z)$ is strictly stable (all poles inside the unit circle) if and only if:
$$ |k_m| < 1 \quad \text{for all } m=1, 2, \dots, p $$
If even a single $k_m$ is $\ge 1$, the vocal tract model is unstable (implying an acoustic tube that adds energy rather than just resonating). This makes $k_m$ ideal for quantization and transmission, because as long as we constrain the quantized values to strictly lie between -1 and 1, we guarantee stability at the receiver.

### 4.6 Filter Realization: Lattice Structures and LSFs
Instead of implementing the synthesis filter $H(z)$ using a standard Direct Form I or II structure with the $a_k$ coefficients, modern DSPs use a **Lattice Filter** structure using the $k_m$ reflection coefficients directly.
Why? Because the Direct Form structure is hypersensitive to coefficient quantization. Small changes in $a_k$ (due to limited bit depth) can easily push a pole outside the unit circle, causing the filter to explode. Lattice filters are robust: as long as the quantized $k_m$ values remain within $(-1, 1)$, stability is absolutely guaranteed.
In modern cellular standards (like AMR and EVRC), an even more robust parameter set called **Line Spectral Frequencies (LSFs)** or Line Spectral Pairs (LSPs) is used. They represent the $A(z)$ polynomial as the sum of a symmetric and anti-symmetric polynomial. They map the poles to angles on the unit circle, making quantization and interpolation between frames extremely stable and natural-sounding.

### 4.7 Homomorphic Analysis and the Cepstrum
Linear filtering is mathematically represented by convolution: $x[n] = e[n] * h[n]$.
We often want to completely separate the excitation source $e[n]$ (to find the pitch) from the vocal tract filter $h[n]$ (to find the formants). Convolution mixes them inextricably in the time domain.
**Homomorphic processing** is a mathematical framework for transforming non-linear combinations (like multiplication or convolution) into linear combinations (addition).
1. **Fourier Transform:** Convolution in time becomes multiplication in frequency.
   $$ X(e^{j\omega}) = E(e^{j\omega})H(e^{j\omega}) $$
2. **Magnitude & Complex Logarithm:** The logarithm transforms multiplication into addition!
   $$ \log |X(e^{j\omega})| = \log |E(e^{j\omega})| + \log |H(e^{j\omega})| $$
3. **Inverse Fourier Transform (IDTFT):** The IDTFT is a linear operator, so the addition is preserved in the new domain.
   $$ c[n] = c_e[n] + c_h[n] $$
The resulting sequence $c[n]$ is called the **real cepstrum**. The independent variable $n$ is no longer time, but is called **quefrency**.
Because the vocal tract frequency response $H(e^{j\omega})$ is a smooth, slowly varying spectral envelope, its cepstrum $c_h[n]$ is concentrated at low quefrencies (low $n$).
Because the periodic excitation $E(e^{j\omega})$ has a rapid, comb-like harmonic structure in the frequency domain, its cepstrum $c_e[n]$ is manifested as a sharp peak at high quefrency, specifically at $n = T_0$ (the pitch period).
We can perfectly separate them by applying a simple rectangular window in the cepstral domain, a process called **liftering**.

### 4.8 Mel-Frequency Cepstral Coefficients (MFCC)
While LPC models the physical vocal tract, MFCCs model human perception. The human basilar membrane inside the cochlea does not have linear frequency resolution. We can easily distinguish a 100 Hz tone from a 200 Hz tone, but we cannot distinguish a 10,000 Hz tone from a 10,100 Hz tone. The Mel scale approximates this perceptual characteristic.
$$ f_{\text{mel}} = 2595 \log_{10} \left( 1 + \frac{f}{700} \right) $$
**Detailed MFCC extraction pipeline:**
1. **Pre-emphasis:** Apply a high-pass filter $H(z) = 1 - 0.97z^{-1}$ to boost high frequencies, compensating for the natural $-20$ dB/decade spectral roll-off of human speech.
2. **Frame & Window:** Divide speech into overlapping 25 ms frames. Apply a Hamming window to prevent spectral leakage at the edges.
3. **FFT:** Compute the magnitude spectrum $|X[k]|$.
4. **Mel Filterbank:** Multiply the spectrum by a bank of 20-40 overlapping triangular filters. The center frequencies of these triangles are linearly spaced on the Mel scale (meaning they get wider and further apart on the linear Hz scale). Sum the energy in each band.
5. **Logarithm:** Take the log of the filterbank energies, simulating human logarithmic loudness perception.
6. **DCT (Discrete Cosine Transform):** The overlapping triangular filters cause the log energies to be highly correlated. We apply a DCT to decorrelate the features. We keep only the first 12-13 coefficients, which represent the broad spectral shape (formants) while discarding the pitch harmonics (which would appear in the higher coefficients).

### 4.9 Pitch Detection Algorithms (PDA)
Accurate pitch detection (finding $F_0 = 1/T_0$) is notoriously difficult but essential for vocoders.
**1. Autocorrelation Method:**
$$ R_{xx}[k] = \sum_{n} x[n]x[n+k] $$
For a periodic signal with period $T_0$, $x[n]$ will closely match $x[n+T_0]$. Therefore, $R_{xx}[k]$ will have a strong local maximum at lag $k = T_0$.
*Weakness:* The vocal tract formants can cause spurious peaks in the autocorrelation. To fix this, we often apply "center clipping" to the signal before autocorrelation to remove formants and leave only the high-amplitude glottal pulses.

**2. Average Magnitude Difference Function (AMDF):**
$$ D[k] = \sum_{n} |x[n] - x[n+k]| $$
Instead of multiplying, AMDF subtracts. At $k = T_0$, $x[n] \approx x[n+T_0]$, so the difference approaches zero. We look for a deep global minimum.
*Advantage:* Computationally incredibly cheap because it uses absolute differences instead of hardware multipliers.

**3. Cepstral Pitch Determination:**
As discussed, the real cepstrum $c[n]$ will have a distinct peak at quefrency $n = T_0$.
*Advantage:* Highly accurate because the logarithm flattens the formants, preventing them from interfering with the pitch peak.
*Disadvantage:* Computationally expensive (requires FFT, log, IFFT).

**Common Failure Modes:**
- **Octave Errors:** The algorithm detects $2T_0$ (pitch halving) or $T_0/2$ (pitch doubling) instead of the true fundamental period.
- **Voiced/Unvoiced Confusion:** Attempting to find a pitch in random noise, or classifying a weak voiced segment as unvoiced.

---
## 5. COMPLETE PROOFS AND DERIVATIONS

### 5.1 Rigorous Derivation of the Yule-Walker Equations (Calculus Method)
**Objective:** Minimize the Mean Squared Error over an infinite window (Autocorrelation method):
$$ J = E = \sum_{n=-\infty}^{\infty} e^2[n] = \sum_{n=-\infty}^{\infty} \left( x[n] + \sum_{k=1}^{p} a_k x[n-k] \right)^2 $$

**Step 1: Differentiate with respect to $a_m$**
To find the global minimum of this quadratic surface, set the partial derivative $\frac{\partial J}{\partial a_m} = 0$ for each $m \in \{1, 2, \dots, p\}$.
Using the chain rule:
$$ \frac{\partial J}{\partial a_m} = \sum_{n=-\infty}^{\infty} 2 \left( x[n] + \sum_{k=1}^{p} a_k x[n-k] \right) \cdot \frac{\partial}{\partial a_m} \left( x[n] + \sum_{k=1}^{p} a_k x[n-k] \right) = 0 $$

**Step 2: Evaluate the inner derivative**
Since $x[n]$ is treated as constant with respect to the filter coefficients, its derivative is 0. In the inner summation, the only term that depends on $a_m$ is when $k=m$. The derivative of $a_m x[n-m]$ with respect to $a_m$ is exactly $x[n-m]$.
$$ \frac{\partial J}{\partial a_m} = 2 \sum_{n=-\infty}^{\infty} \left( x[n] + \sum_{k=1}^{p} a_k x[n-k] \right) x[n-m] = 0 $$

**Step 3: Distribute the summation**
Divide by 2 to simplify:
$$ \sum_{n=-\infty}^{\infty} x[n]x[n-m] + \sum_{n=-\infty}^{\infty} \sum_{k=1}^{p} a_k x[n-k]x[n-m] = 0 $$
Swap the order of summations in the second term:
$$ \sum_{n=-\infty}^{\infty} x[n]x[n-m] + \sum_{k=1}^{p} a_k \left( \sum_{n=-\infty}^{\infty} x[n-k]x[n-m] \right) = 0 $$

**Step 4: Express in terms of Autocorrelation**
Recall the definition of deterministic autocorrelation: $R_{xx}[m] = \sum_{n=-\infty}^{\infty} x[n]x[n-m]$.
In the second term, we have $\sum_{n=-\infty}^{\infty} x[n-k]x[n-m]$. Let $l = n-k$. Then $n-m = l + k - m$. The summation becomes $\sum_{l=-\infty}^{\infty} x[l]x[l - (m-k)] = R_{xx}[m-k]$.
Substituting these definitions:
$$ R_{xx}[m] + \sum_{k=1}^{p} a_k R_{xx}[m-k] = 0 $$
Rearranging yields the famous Yule-Walker normal equations:
$$ \sum_{k=1}^{p} a_k R_{xx}[m-k] = -R_{xx}[m] \quad \text{for } m = 1, 2, \dots, p $$

### 5.2 Derivation using the Orthogonality Principle (Elegant Method)
By the orthogonality principle, the optimal error $e[n]$ must be orthogonal to the data used to form the prediction, which are the past samples $x[n-m]$ for $m=1 \dots p$.
$$ \sum_{n=-\infty}^{\infty} e[n] x[n-m] = 0 \quad \text{for } m = 1 \dots p $$
Substitute the definition of $e[n]$:
$$ \sum_{n=-\infty}^{\infty} \left( x[n] + \sum_{k=1}^{p} a_k x[n-k] \right) x[n-m] = 0 $$
$$ \sum_{n} x[n]x[n-m] + \sum_{k=1}^{p} a_k \sum_{n} x[n-k]x[n-m] = 0 $$
$$ R_{xx}[m] + \sum_{k=1}^{p} a_k R_{xx}[m-k] = 0 $$
This yields the exact same normal equations in three lines of math!

### 5.3 Derivation of the Minimum Prediction Error ($E_p$)
What is the absolute minimum value of the error variance $E_p$?
$$ E_p = \sum_{n} e^2[n] = \sum_{n} e[n] \left( x[n] + \sum_{k=1}^{p} a_k x[n-k] \right) $$
Distribute $e[n]$:
$$ E_p = \sum_{n} e[n]x[n] + \sum_{k=1}^{p} a_k \sum_{n} e[n]x[n-k] $$
By the orthogonality principle, $\sum_{n} e[n]x[n-k] = 0$ for all $k=1 \dots p$. Thus, the entire right summation vanishes!
$$ E_p = \sum_{n} e[n]x[n] = \sum_{n} \left( x[n] + \sum_{k=1}^{p} a_k x[n-k] \right) x[n] $$
$$ E_p = \sum_{n} x^2[n] + \sum_{k=1}^{p} a_k \sum_{n} x[n-k]x[n] $$
$$ E_p = R_{xx}[0] + \sum_{k=1}^{p} a_k R_{xx}[k] $$

---
## 6. WORKED EXAMPLES (FULLY SOLVED)

### Example 1: Order-1 Linear Predictor (p=1)
**Problem statement:**
Given a windowed speech signal frame with autocorrelation values $R_{xx}[0] = 5.0$ and $R_{xx}[1] = 4.0$. Find the optimal order-1 predictor coefficient $a_1$, write the inverse filter transfer function $A(z)$, and calculate the minimum prediction error $E_1$.

**Solution:**
For $p=1$, the Yule-Walker normal equation system reduces to a single equation:
$a_1 R_{xx}[0] = -R_{xx}[1]$
Substituting the given autocorrelation values:
$a_1 (5.0) = -4.0$
$a_1 = -4.0 / 5.0 = -0.8$

The optimal linear prediction filter is:
$\hat{x}[n] = -a_1 x[n-1] = -(-0.8) x[n-1] = 0.8 x[n-1]$

The inverse filter (analysis filter) $A(z)$ is:
$A(z) = 1 + a_1 z^{-1} = 1 - 0.8z^{-1}$

The minimum prediction error variance $E_1$ is:
$E_1 = R_{xx}[0] + a_1 R_{xx}[1]$
$E_1 = 5.0 + (-0.8)(4.0) = 5.0 - 3.2 = 1.8$

**Physical interpretation:**
The signal is highly correlated at lag 1 ($R[1]$ is close to $R[0]$), meaning adjacent samples are very similar. Predicting the next sample as simply 80% of the previous sample reduces the signal variance (error) from 5.0 down to 1.8, removing significant redundancy.
The synthesis filter has a single pole at $z = 0.8$, meaning it is a low-pass filter, which is characteristic of highly correlated signals.

**Common mistakes to avoid:**
Students often confuse the sign of $a_1$ in the prediction equation $\hat{x}[n] = -a_1 x[n-1]$ versus the filter equation $A(z) = 1 + a_1 z^{-1}$. Remember the negative convention.

### Example 2: Full Levinson-Durbin Recursion (p=2)
**Problem statement:**
A speech frame has the following autocorrelation sequence: $R_{xx}[0] = 10, R_{xx}[1] = 8, R_{xx}[2] = 4$. Use the Levinson-Durbin recursive algorithm to find the reflection coefficients $k_1, k_2$, the final LPC coefficients $a_1, a_2$, and the final error $E_2$.

**Solution:**
**Initialization (m=0):**
$E_0 = R_{xx}[0] = 10$

**Iteration 1 (Order m=1):**
Calculate reflection coefficient $k_1$:
$k_1 = -R_{xx}[1] / E_0 = -8 / 10 = -0.8$
Update filter coefficients for order 1:
$a_1^{(1)} = k_1 = -0.8$
Update the error for order 1:
$E_1 = (1 - k_1^2) E_0 = (1 - (-0.8)^2) \times 10 = (1 - 0.64) \times 10 = 0.36 \times 10 = 3.6$

**Iteration 2 (Order m=2):**
Calculate reflection coefficient $k_2$:
$k_2 = -\frac{R_{xx}[2] + a_1^{(1)} R_{xx}[1]}{E_1}$
$k_2 = -\frac{4 + (-0.8)(8)}{3.6} = -\frac{4 - 6.4}{3.6} = -\frac{-2.4}{3.6} = \frac{2.4}{3.6} = \frac{2}{3} \approx 0.6667$
Update filter coefficients for order 2:
The highest order coefficient is just the reflection coefficient:
$a_2^{(2)} = k_2 = 0.6667$
The lower order coefficients are updated using the previous order's coefficients (reversed):
$a_1^{(2)} = a_1^{(1)} + k_2 \cdot a_1^{(1)}$  *(since m=2, the reversed index m-i is 2-1=1)*
$a_1^{(2)} = -0.8 + (0.6667)(-0.8) = -0.8 - 0.5333 = -1.3333$
Update the error for order 2:
$E_2 = (1 - k_2^2) E_1 = (1 - (2/3)^2) \times 3.6 = (1 - 4/9) \times 3.6 = (5/9) \times 3.6 = 2.0$

**Final Result:**
Inverse filter: $A(z) = 1 - 1.3333 z^{-1} + 0.6667 z^{-2}$
Reflection coefficients: $k_1 = -0.8, k_2 = 0.6667$
Final minimum Error: $2.0$

**Physical interpretation:**
The error dropped from 10 to 3.6 using one coefficient, and then dropped further to 2.0 using the second coefficient. Both reflection coefficients satisfy $|k_1| < 1$ and $|k_2| < 1$, mathematically guaranteeing that the roots of $A(z)$ lie strictly inside the unit circle, ensuring synthesis filter stability.

### Example 3: Filter Stability Check via PARCOR
**Problem statement:**
During transmission over a noisy channel, an LPC vocoder receives a set of corrupted PARCOR (reflection) coefficients for a $p=3$ model: $k_1 = 0.95, k_2 = -0.6, k_3 = -1.1$. Should the receiver synthesize speech using these parameters?

**Solution:**
The necessary and sufficient stability criterion for an all-pole synthesis filter $H(z) = 1/A(z)$ derived via Levinson-Durbin is that ALL reflection coefficients must satisfy strictly $|k_m| < 1$.
Checking the received coefficients:
$|k_1| = 0.95 < 1$ (Pass)
$|k_2| = |-0.6| = 0.6 < 1$ (Pass)
$|k_3| = |-1.1| = 1.1 \ge 1$ (Fail)
Because $k_3$ exceeds 1 in magnitude, the resulting synthesis filter is unconditionally unstable. If the receiver attempts to synthesize speech, the output will grow exponentially to infinity (creating loud, dangerous digital artifacts). The receiver should discard this frame and either interpolate from the previous frame or mute the audio (frame concealment).

### Example 4: Cepstral Computation from Z-Transform
**Problem statement:**
A simplified vocal tract can be modeled as a single-pole system with z-transform $X(z) = \frac{1}{1 - 0.5z^{-1}}$ for $|z| > 0.5$. Calculate its complex cepstrum $c[n]$ for $n > 0$.

**Solution:**
1. **Take the natural logarithm of the transfer function:**
$C(z) = \log X(z) = \log \left( \frac{1}{1 - 0.5z^{-1}} \right) = -\log(1 - 0.5z^{-1})$
2. **Apply Maclaurin series expansion:**
Recall the standard Taylor/Maclaurin series for $\log(1-x) = -x - x^2/2 - x^3/3 - x^4/4 - \dots$ (valid for $|x|<1$).
Let $x = 0.5z^{-1}$. This expansion is strictly valid since we are given $|z| > 0.5$, meaning $|0.5z^{-1}| < 1$.
Substituting this into our equation:
$C(z) = -\left( - (0.5z^{-1}) - \frac{(0.5z^{-1})^2}{2} - \frac{(0.5z^{-1})^3}{3} - \dots \right)$
$C(z) = (0.5z^{-1}) + \frac{0.25}{2}z^{-2} + \frac{0.125}{3}z^{-3} + \dots$
3. **Take the Inverse Z-Transform (by inspection):**
The inverse Z-transform simply extracts the coefficients of $z^{-n}$. Therefore, $c[n]$ is the coefficient of the $n$-th term.
$c[1] = 0.5$
$c[2] = 0.25 / 2 = 0.125$
$c[3] = 0.125 / 3 \approx 0.0417$
In general, for any $n \ge 1$, the closed-form expression for the complex cepstrum is:
$c[n] = \frac{(0.5)^n}{n}$ for $n \ge 1$.
$c[n] = 0$ for $n \le 0$.

**Physical interpretation:**
The single pole represents a smooth resonance. Notice how rapidly the cepstrum sequence $c[n]$ decays towards zero as $n$ increases. This mathematically proves our earlier assertion that vocal tract information (formants/poles) is heavily concentrated at very low quefrencies (small values of $n$).

### Example 5: MFCC Mel Frequency Conversion
**Problem statement:**
An ASR system uses a Mel filterbank. Calculate the Mel frequency corresponding to a linear frequency of $f = 1400$ Hz. Conversely, calculate the exact linear frequency corresponding to a Mel value of 2000 Mels.

**Solution:**
**Part 1: Linear to Mel Conversion**
Using the standard formula: $f_{mel} = 2595 \log_{10} \left( 1 + \frac{f}{700} \right)$
Substitute $f = 1400$:
$f_{mel} = 2595 \log_{10} \left( 1 + \frac{1400}{700} \right)$
$f_{mel} = 2595 \log_{10}(1 + 2) = 2595 \log_{10}(3)$
Using $\log_{10}(3) \approx 0.47712$:
$f_{mel} = 2595 \times 0.47712 \approx 1238.1$ Mels.

**Part 2: Mel to Linear Conversion**
Set $f_{mel} = 2000$ and solve for $f$:
$2000 = 2595 \log_{10} \left( 1 + \frac{f}{700} \right)$
Divide by 2595:
$\log_{10} \left( 1 + \frac{f}{700} \right) = \frac{2000}{2595} \approx 0.77071$
Exponentiate both sides (base 10):
$1 + \frac{f}{700} = 10^{0.77071} \approx 5.8981$
Subtract 1:
$\frac{f}{700} = 4.8981$
Multiply by 700:
$f = 700 \times 4.8981 \approx 3428.7$ Hz.

### Example 6: Pitch Period from Autocorrelation
**Problem statement:**
A 30 ms speech frame sampled at $8000\text{ Hz}$ is analyzed. Its autocorrelation function $R_{xx}[k]$ has a strong global maximum at $k=0$, and the next strongest local maximum occurs at a lag of $k=64$ samples. Determine the pitch period in milliseconds and the fundamental frequency ($F_0$) in Hz.

**Solution:**
1. **Find Pitch Period in seconds:**
The peak at lag $k=64$ indicates the signal repeats every 64 samples.
$T_0 = \frac{k}{F_s} = \frac{64}{8000} = 0.008\text{ seconds} = 8\text{ ms}$.
2. **Find Fundamental Frequency:**
$F_0 = \frac{1}{T_0} = \frac{1}{0.008} = 125\text{ Hz}$.

**Physical Interpretation:**
A fundamental frequency of $125\text{ Hz}$ is typical for an adult male speaker. The pitch period of $8\text{ ms}$ fits comfortably inside the $30\text{ ms}$ analysis frame, guaranteeing that at least 3 full pitch cycles were captured, ensuring the autocorrelation peak is well-defined.

---
## 7. ENGINEERING APPLICATIONS AND CASE STUDIES

### 7.1 Linear Predictive Vocoder (LPC-10) Standard
In secure military and tactical communications (e.g., VHF radios), available bandwidth is severely limited. The US Department of Defense standardized LPC-10 (FS-1015) to encode speech at just 2400 bits per second (bps) — a massive 96% reduction from standard 64 kbps PCM telephony.
**System Parameters & Extraction:**
- Sample rate: 8000 Hz.
- Frame size: 22.5 ms (180 samples per frame).
- Predictor order: $p=10$.
**Analysis Process:**
Every 22.5 ms, the encoder analyzes the frame and extracts:
1. 10 reflection coefficients ($k_1 \dots k_{10}$). These are uniquely non-linearly quantized, assigning more bits to lower-order coefficients (e.g., $k_1$ and $k_2$ get 5 bits each, while $k_9, k_{10}$ might only get 2 bits) because the lower-order coefficients have a far more drastic impact on the spectral envelope.
2. 1 Pitch period parameter.
3. 1 Voiced/Unvoiced binary flag.
4. 1 RMS Gain parameter.
**Total data:** 54 bits per frame.
**Data rate:** 54 bits / 22.5 ms = 2400 bps.
**Synthesis result:** The speech is perfectly intelligible but sounds distinctly robotic or "buzzy". The rigid Voiced/Unvoiced binary decision causes catastrophic failures when encountering mixed-excitation sounds (like the voiced fricative 'z'), resulting in unnatural artifacts.

### 7.2 GSM Full Rate Codec (RPE-LTP)
Early 2G cell phones required better audio quality than LPC-10 but still needed high compression. The European GSM standard utilized Regular Pulse Excitation - Long Term Prediction (RPE-LTP), running at 13 kbps.
It improved upon pure LPC by using a two-stage filter model:
1. **Short-Term Predictor (Standard LPC):** An order $p=8$ filter removes the vocal tract envelope redundancy.
2. **Long-Term Predictor (LTP or Pitch Filter):** Removes the fine harmonic structure redundancy caused by the vibrating vocal cords.
Instead of forcing a rigid voiced/unvoiced decision and using artificial noise or impulse trains, the residual signal (after both filters) is simply downsampled and transmitted as a sequence of "regular pulses." This preserved the natural phase and mixed-excitation characteristics, dramatically improving naturalness over LPC-10 while remaining computationally feasible for 1990s mobile processors.

### 7.3 Modern Era: Neural Vocoders (LPCNet)
While classic LPC vocoders sound robotic, modern deep learning has resurrected linear prediction. **LPCNet** (developed by Mozilla) is a modern neural vocoder that combines traditional DSP with artificial intelligence.
Instead of relying on a simplistic pulse/noise excitation, LPCNet uses a highly efficient Recurrent Neural Network (RNN) to artificially synthesize the complex excitation signal $e[n]$ sample-by-sample. This neural excitation is then passed through a traditional, mathematical LPC all-pole synthesis filter $1/A(z)$.
By offloading the spectral envelope modeling to traditional mathematically-proven LPC, the neural network only has to learn the flat excitation, allowing LPCNet to synthesize indistinguishable-from-human voice on basic smartphone CPUs in real-time.

---
## 8. COMMON STUDENT MISCONCEPTIONS AND ERRORS

1. **Misconception:** The estimated LPC polynomial $A(z)$ is the vocal tract filter.
   *Correction:* $A(z)$ is the *inverse* filter (the analysis filter). It flattens the spectrum to extract the residual. The actual vocal tract synthesis filter that produces speech is $H(z) = 1/A(z)$.
2. **Misconception:** Human speech is purely voiced (periodic) or purely unvoiced (noise).
   *Correction:* Human speech frequently contains mixed excitation. Voiced fricatives like 'v', 'z', or the French 'j' involve vocal cords vibrating simultaneously with turbulent noise generated at the teeth/lips. Simple LPC vocoders struggle severely with these sounds.
3. **Misconception:** The Toeplitz matrix $\mathbf{R}$ in the Yule-Walker equations is inverted directly using standard matrix inverse $[\mathbf{R}]^{-1}$.
   *Correction:* While mathematically possible, directly inverting a $10\times10$ matrix using Gaussian elimination takes $O(p^3)$ operations, which was computationally impossible in real-time on early DSP chips. We use the Levinson-Durbin algorithm to bypass direct inversion, solving it in $O(p^2)$ while simultaneously guaranteeing stability.
4. **Misconception:** Higher order predictors (e.g., $p=50$) will always produce a more accurate model and sound better.
   *Correction:* A predictor order that is too high will overfit the data. Instead of just modeling the smooth vocal tract formants (the envelope), a $p=50$ filter will start modeling the individual pitch harmonics (the fine structure). This destroys the source-filter separation paradigm. For 8 kHz speech, $p=10$ to $12$ is optimal.
5. **Misconception:** Homomorphic Cepstrum analysis separates signals in the time domain.
   *Correction:* The Cepstrum separates signals that were *convolved* in the time domain by transforming them into an additive linear representation in an entirely new domain called the *quefrency* domain.
6. **Misconception:** The AMDF algorithm is slower than Autocorrelation because it uses absolute values.
   *Correction:* AMDF is significantly faster in hardware because it entirely avoids multiplications, relying strictly on addition and subtraction. Historically, DSP multipliers were expensive in silicon area and clock cycles.

---
## 9. CONNECTIONS TO OTHER LECTURES

*   **Builds on Lecture 18 (FIR/IIR Filter Structures):** The LPC synthesis filter is an IIR all-pole filter. The lattice filter structures discussed in Lecture 18 are the direct physical implementation of the Levinson-Durbin reflection coefficients $k_m$.
*   **Builds on Lecture 14 (DFT/FFT):** Cepstrum and MFCC calculations heavily rely on the Fast Fourier Transform to jump between the time and frequency domains efficiently.
*   **Feeds into Next Course (Machine Learning / ASR):** The MFCCs generated in this lecture are not just historical artifacts; they remain the foundational raw input features for Neural Networks, Support Vector Machines, or Hidden Markov Models in modern speech recognition and NLP pipelines.

---
## 10. EXAMINATION QUESTIONS

### 10.1 Short Answer

**Q1: Explain the physical biological equivalent of the source and filter in the source-filter model.**
**Model Answer:** The source corresponds to the lungs expelling air and the glottis (vocal cords) modulating it into either periodic pulses (voiced) or turbulent noise (unvoiced). The filter corresponds to the vocal tract (throat, mouth, nasal cavity) acting as a resonant acoustic tube that shapes the spectrum.

**Q2: Why is the autocorrelation matrix $\mathbf{R}$ in the normal equations structured as a Toeplitz matrix?**
**Model Answer:** Because we assume the signal frame is wide-sense stationary, the autocorrelation $E\{x[n]x[n-m]\}$ depends only on the lag difference $m$, not on absolute time $n$. Thus, all elements along any given diagonal of the matrix share the same lag difference, making them constant.

**Q3: State the exact mathematical stability condition for the LPC synthesis filter in terms of the Levinson-Durbin algorithm outputs.**
**Model Answer:** The synthesis filter $H(z) = 1/A(z)$ is strictly stable (all poles inside the unit circle) if and only if the magnitude of all intermediate reflection (PARCOR) coefficients $k_m$ is strictly less than 1 ($|k_m| < 1$ for all $m \in 1 \dots p$).

**Q4: Explain the physiological and perceptual purpose of applying the Mel scale in computing MFCCs.**
**Model Answer:** The human cochlea's basilar membrane does not perceive frequency linearly. It acts as a filterbank with high frequency resolution at low frequencies and poor resolution at high frequencies. The Mel scale mathematically warps the linear frequency axis to mimic this non-linear perceptual resolution.

**Q5: Define "liftering" in the context of homomorphic signal processing.**
**Model Answer:** Liftering is the cepstral-domain equivalent of filtering. It involves multiplying the real cepstrum $c[n]$ by a window function to separate the low-quefrency components (vocal tract envelope) from the high-quefrency components (pitch excitation).

### 10.2 Long Answer / Numerical Problems

**Problem 1: Levinson-Durbin Recursion Complete Walkthrough**
Given a windowed speech frame with autocorrelation sequence $R_{xx}[0]=1, R_{xx}[1]=0.5, R_{xx}[2]=0.2, R_{xx}[3]=0.1$. Compute the complete set of LPC coefficients for a 3rd order predictor using the Levinson-Durbin recursive algorithm. Ensure you show all intermediate reflection coefficients and error terms.
**Solution Step-by-Step:**
*Initialization:* $E_0 = R_{xx}[0] = 1$
*Order 1:*
$k_1 = -R_{xx}[1]/E_0 = -0.5/1 = -0.5$.
$a_1^{(1)} = k_1 = -0.5$.
$E_1 = (1 - k_1^2) E_0 = (1 - (-0.5)^2) \times 1 = 1 - 0.25 = 0.75$.
*Order 2:*
$k_2 = -(R_{xx}[2] + a_1^{(1)}R_{xx}[1])/E_1 = -(0.2 + (-0.5)(0.5))/0.75 = -(0.2 - 0.25)/0.75 = -(-0.05)/0.75 = 0.05/0.75 = 1/15 \approx 0.0667$.
$a_2^{(2)} = k_2 = 0.0667$.
$a_1^{(2)} = a_1^{(1)} + k_2 a_1^{(1)} = -0.5 + (0.0667)(-0.5) = -0.5 - 0.03335 = -0.5333$.
$E_2 = (1 - k_2^2) E_1 = (1 - (0.0667)^2) \times 0.75 = (1 - 0.00444) \times 0.75 \approx 0.7467$.
*Order 3:*
$k_3 = -(R_{xx}[3] + a_1^{(2)}R_{xx}[2] + a_2^{(2)}R_{xx}[1])/E_2 = -(0.1 + (-0.5333)(0.2) + (0.0667)(0.5))/0.7467$
Numerator calculation: $0.1 - 0.10666 + 0.03335 = 0.02669$.
$k_3 = -(0.02669)/0.7467 \approx -0.0357$.
$a_3^{(3)} = k_3 = -0.0357$.
$a_1^{(3)} = a_1^{(2)} + k_3 a_2^{(2)} = -0.5333 + (-0.0357)(0.0667) = -0.5333 - 0.00238 = -0.5357$.
$a_2^{(3)} = a_2^{(2)} + k_3 a_1^{(2)} = 0.0667 + (-0.0357)(-0.5333) = 0.0667 + 0.0190 = 0.0857$.
**Final Answer:** The 3rd order predictor coefficients are $a_1 = -0.5357, a_2 = 0.0857, a_3 = -0.0357$.

### 10.3 True/False with Justification

1. **True/False:** The prediction error filter (analysis filter) $A(z)$ is always a stable FIR filter.
   *Answer:* True. $A(z) = 1 + \sum a_k z^{-k}$ is an FIR filter. Its transfer function has all of its poles located exactly at the origin $z=0$, which is trivially strictly inside the unit circle, making it unconditionally stable.
2. **True/False:** The AMDF pitch detection algorithm requires significantly more multiplications than the standard Autocorrelation algorithm.
   *Answer:* False. AMDF stands for Average Magnitude Difference Function. It uses absolute differences (subtraction) instead of mathematical products, requiring exactly zero multiplications.
3. **True/False:** In the real cepstrum of a voiced speech frame, the pitch period manifests as a strong, distinct peak at very low quefrencies.
   *Answer:* False. The pitch period creates rapid harmonic variations in the frequency domain. Rapid variations in frequency map to *high* quefrencies in the cepstral domain. Low quefrencies are dominated by the slow-varying vocal tract formants.
4. **True/False:** If the first reflection coefficient $k_1 = 1.2$, the resulting synthesis filter generated by the Levinson-Durbin algorithm will be unstable.
   *Answer:* True. The necessary and sufficient condition for mathematical stability of the all-pole filter is $|k_m| < 1$ for all $m$. Since $|1.2| \ge 1$, the filter is unstable.
5. **True/False:** Unvoiced speech is biologically modeled as a periodic impulse train passing through an all-pole filter.
   *Answer:* False. Unvoiced speech (like 's' or 'f') is modeled using a random white noise excitation source, not a periodic impulse train.
6. **True/False:** Directly solving the Yule-Walker normal equations using standard Gaussian elimination matrix inversion takes $O(p^2)$ computational operations.
   *Answer:* False. Standard Gaussian elimination takes $O(p^3)$ operations. It is the specialized Levinson-Durbin algorithm that exploits the Toeplitz structure to solve the system in $O(p^2)$ operations.
7. **True/False:** For an $8\text{ kHz}$ sampled speech signal, an LPC filter order of $p = 50$ would perfectly capture the formants without any drawbacks.
   *Answer:* False. An order of $50$ would heavily overfit the data, attempting to model the individual pitch harmonics rather than just the smooth formant envelope, ruining the source-filter separation.
8. **True/False:** Line Spectral Frequencies (LSFs) are preferred over direct $a_k$ coefficients for transmission because they ensure filter stability after quantization.
   *Answer:* True. LSFs map the filter poles to the unit circle and inherently guarantee stability as long as the frequencies remain correctly ordered, making them highly robust for quantization.

---
## 11. KEY FORMULAS REFERENCE

| Concept | Formula |
| :--- | :--- |
| **Linear Prediction Equation** | $\hat{x}[n] = -\sum_{k=1}^{p} a_k x[n-k]$ |
| **Inverse (Analysis) Filter $A(z)$** | $A(z) = 1 + \sum_{k=1}^{p} a_k z^{-k}$ |
| **Vocal Tract (Synthesis) Filter $H(z)$** | $H(z) = \frac{G}{A(z)}$ |
| **Mean Squared Prediction Error** | $J = E\{ (x[n] - \hat{x}[n])^2 \} = \sum e^2[n]$ |
| **Yule-Walker Normal Equations** | $\sum_{k=1}^{p} a_k R_{xx}[m-k] = -R_{xx}[m] \quad \text{for } m=1 \dots p$ |
| **Levinson Reflection Coeff $k_m$** | $k_{m} = -\frac{R_{xx}[m] + \sum_{i=1}^{m-1} a_i^{(m-1)} R_{xx}[m-i]}{E_{m-1}}$ |
| **Levinson Filter Update $a_i$** | $a_i^{(m)} = a_i^{(m-1)} + k_m a_{m-i}^{(m-1)}$ |
| **Levinson Minimum Error $E_m$** | $E_m = (1 - k_m^2) E_{m-1}$ |
| **Real Cepstrum Transformation** | $c[n] = \mathcal{F}^{-1}\{ \log \|X(e^{j\omega})\| \}$ |
| **Mel Scale Frequency Conversion** | $f_{\text{mel}} = 2595 \log_{10} \left( 1 + \frac{f}{700} \right)$ |
| **Autocorrelation Pitch Detection** | $R_{xx}[k] = \sum_{n} x[n]x[n+k]$ |
| **AMDF Pitch Detection** | $D[k] = \sum_{n} \|x[n] - x[n+k]\|$ |

---
## 12. FURTHER READING AND REFERENCES

*   **Proakis, J. G., & Manolakis, D. G.** *Digital Signal Processing: Principles, Algorithms, and Applications (4th Edition)*. Chapter 11 (Linear Prediction and Optimum Linear Filters). This is the definitive mathematical reference for the Yule-Walker derivation.
*   **Rabiner, L. R., & Schafer, R. W.** *Theory and Applications of Digital Speech Processing*. Highly recommended for deep, practical dives into pitch detection algorithms, LPC-10 vocoder implementation, and the physical acoustics of the vocal tract.
*   **Oppenheim, A. V., & Schafer, R. W.** *Discrete-Time Signal Processing (3rd Edition)*. Chapter 13 provides the most rigorous treatment of Cepstrum Analysis and Homomorphic Deconvolution available in standard textbooks.
*   **Haykin, S.** *Adaptive Filter Theory*. Chapter 6 provides an advanced, statistical signal processing approach to the Levinson-Durbin recursion and lattice filter structures.

</Faculty Notes — Lecture 24: Linear Prediction & Speech Processing>





























































