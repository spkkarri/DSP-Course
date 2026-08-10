<Faculty Notes — Lecture 17: Short-Time Fourier Transform (STFT) & Spectrogram>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY

The Short-Time Fourier Transform (STFT) represents a fundamental paradigm shift for undergraduate students. Until this point, their training has conditioned them to view time and frequency as mutually exclusive domains—a signal is either analyzed as a function of time or as a function of frequency. STFT is the gateway to time-frequency analysis. 

When delivering this lecture, it is imperative to establish the concept of non-stationarity early. The primary pedagogical challenge is conveying the Heisenberg-Gabor Uncertainty Principle intuitively before diving into the mathematics. The uncertainty principle is a fundamental mathematical limit of the Fourier Transform itself, not a technological limitation of computers or sensors. 

**Suggested Demos:** 
1. Use a live spectrogram tool (such as Praat or an online WebAudio spectrogram) and whistle a rising chirp. Show the students how the line moves in the time-frequency plane. 
2. Play a complex, non-stationary signal like a musical chord progression or speech, and show how the global DFT completely fails to capture the temporal order of events, while the spectrogram captures it beautifully.
3. Switch between a very short window and a very long window on the live spectrogram to visually demonstrate the time-frequency resolution trade-off.
4. Demonstrate the Gibbs phenomenon using MATLAB/Python by abruptly truncating a sine wave and showing the resulting frequency spectrum with severe spectral leakage.
5. Provide a visualization of 50% overlapping Hann windows adding up to a constant line of 1.

**Prerequisite Checks:**
Ensure students are comfortable with discrete convolution, the DFT formula, and basic concepts of spectral leakage before starting.

---
## 1. LEARNING OBJECTIVES

By the end of this comprehensive lecture, students will be able to:
1. **Explain** the limitations of the Discrete-Time Fourier Transform (DTFT) and Discrete Fourier Transform (DFT) when applied to non-stationary signals.
2. **Define** the Short-Time Fourier Transform (STFT) mathematically and interpret its variables in both time and frequency domains.
3. **Analyze** the role of various window functions (Rectangular, Hann, Hamming, Blackman, Kaiser) and their impact on spectral leakage and frequency resolution.
4. **Formulate** the theoretical trade-offs between time resolution and frequency resolution using the formal Heisenberg-Gabor Uncertainty Principle.
5. **Calculate** exact parameter combinations (window length, hop size, FFT size) to design spectrograms for specific engineering constraints, such as radar and speech processing.
6. **Prove** the Constant Overlap-Add (COLA) condition for perfect signal reconstruction from STFT frames.
7. **Interpret** the STFT as a uniform bank of modulated bandpass filters.
8. **Evaluate** STFT techniques in real-world contexts such as speech recognition (Mel-spectrograms), radar Doppler processing, and music transcription.
9. **Contrast** the STFT with more advanced time-frequency representations such as the Wigner-Ville Distribution and the Continuous Wavelet Transform.

---
## 2. PREREQUISITE KNOWLEDGE REVIEW

Before initiating this lecture, students must have a firm grasp of the following concepts:

**A. Discrete-Time Fourier Transform (DTFT):**
The DTFT of a discrete-time signal $x[n]$ is given by:
$$ X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n} $$
This transform provides a continuous frequency spectrum, periodic with $2\pi$. It assumes the signal $x[n]$ is stationary and defined from $n = -\infty$ to $\infty$.

**B. Discrete Fourier Transform (DFT):**
For an $N$-point sequence, the DFT is:
$$ X[k] = \sum_{n=0}^{N-1} x[n] e^{-j\frac{2\pi}{N}kn}, \quad k = 0, 1, \dots, N-1 $$
The DFT provides a discrete frequency spectrum.

**C. Inverse Discrete Fourier Transform (IDFT):**
The inverse operation to recover the time-domain signal is:
$$ x[n] = \frac{1}{N} \sum_{k=0}^{N-1} X[k] e^{j\frac{2\pi}{N}kn} $$

**D. Convolution in Time vs. Multiplication in Frequency:**
If $y[n] = x[n] \cdot w[n]$, then the DTFT is the periodic convolution:
$$ Y(e^{j\omega}) = \frac{1}{2\pi} \int_{-\pi}^{\pi} X(e^{j\theta}) W(e^{j(\omega-\theta)}) d\theta $$
Windowing a signal in the time domain corresponds to smearing or convolving its spectrum in the frequency domain.

**E. Gibbs Phenomenon & Spectral Leakage:**
Truncating a signal abruptly (multiplying by a rectangular window) leads to ringing artifacts in the frequency domain (sidelobes), which cause spectral leakage.

---
## 3. HISTORICAL AND MOTIVATIONAL CONTEXT

The roots of time-frequency analysis can be traced back to the invention of the Sound Spectrograph in the 1940s at Bell Labs, originally developed for military communications and cryptography (e.g., Project SIGSALY) during World War II. Researchers needed a way to visualize the changing frequencies of the human voice to design better vocoders.

In classical Fourier analysis, dating back to Joseph Fourier's work in the 1800s, basis functions are infinite-duration complex exponentials. While mathematically elegant for solving heat equations or analyzing steady-state AC circuits (where properties don't change), this approach falls apart for real-world signals that carry information. Information, by definition, implies change. 

Speech, music, and radar returns are inherently **non-stationary**. If a musician plays a C major chord followed by a G major chord, the global Fourier transform will indicate that frequencies corresponding to both C major and G major exist. However, it will not tell you *when* they were played, nor in what order. 

For an EEE engineer, dealing with non-stationary signals is unavoidable. From tracking the Doppler shift of a moving aircraft to analyzing faults in rotating machinery, the ability to pinpoint both *which* frequencies are present and *when* they occur is essential. The STFT provides this vital bridge between the time domain and frequency domain.

---
## 4. THEORETICAL FOUNDATIONS

### 4.1 Limitations of DTFT and DFT for Non-Stationary Signals

The DTFT integrates over all time:
$$ X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n} $$
The complex exponential $e^{-j\omega n}$ extends from $t=-\infty$ to $t=\infty$. Thus, the summation kernel has infinite time support. Any transient change in $x[n]$ at a specific instant $n=n_0$ is completely averaged into the global spectrum $X(e^{j\omega})$.

Consider a signal composed of two sequential tones:
$$ x[n] = \begin{cases} \cos(\omega_1 n), & 0 \leq n < 1000 \\ \cos(\omega_2 n), & 1000 \leq n < 2000 \end{cases} $$
The magnitude spectrum $|X(e^{j\omega})|$ will show prominent peaks at both $\omega_1$ and $\omega_2$. But looking at the magnitude spectrum alone, one cannot distinguish this signal from a signal where both tones are played simultaneously for the entire 2000 samples. 

While the timing information is technically preserved in the phase spectrum, unwrapping and interpreting global phase to recover timing is practically impossible for complex, noisy real-world signals.

### 4.2 Definition of the Short-Time Fourier Transform (STFT)

To recover time localization, we modify the Fourier transform by applying a sliding "window" function $w[m]$. The STFT of a sequence $x[m]$ is a two-dimensional function of time index $n$ and discrete frequency bin $k$.

The discrete STFT formula is formally defined as:
$$ X[n, k] = \sum_{m=-\infty}^{\infty} x[m] w[m-n] e^{-j\frac{2\pi}{N}km} $$

Let's dissect this equation rigorously:
1. $x[m]$ is the input signal (potentially of infinite length).
2. $w[m-n]$ is the window function centered (or starting) around the time index $n$. It is non-zero only for a short duration $M$, effectively isolating a localized region of $x[m]$.
3. The term $x_n[m] = x[m] w[m-n]$ is the short-term windowed signal.
4. We then compute the $N$-point DFT of $x_n[m]$ with respect to the running variable $m$.
5. The result $X[n, k]$ represents the frequency content at frequency index $k$ localized around time index $n$.

By shifting the window (varying $n$ by a hop size $H$) and computing the DFT at each step, we generate a 2D matrix representing the time-varying spectrum.

### 4.3 The Role of the Window Function

The choice of window function $w[m]$ is critical. The frequency response of the window, $W(e^{j\omega})$, defines how the true spectrum is distorted via convolution. Let's analyze the common windows.

**The Rectangular Window:**
$$ w_{rect}[m] = \begin{cases} 1, & 0 \leq m \leq M-1 \\ 0, & \text{otherwise} \end{cases} $$
Its DTFT is a Dirichlet function (digital sinc):
$$ W_{rect}(e^{j\omega}) = e^{-j\omega\frac{M-1}{2}} \frac{\sin(\omega M / 2)}{\sin(\omega / 2)} $$
This spectrum has a very narrow mainlobe (width $4\pi/M$) but very high sidelobes. The first sidelobe is only 13 dB below the mainlobe. When this window is multiplied with the signal in time, it causes **spectral leakage**. Energy from a strong frequency bin bleeds into adjacent bins, masking weaker signals.

**The Hann Window:**
To suppress sidelobes, we taper the window at the edges.
$$ w_{hann}[m] = 0.5 - 0.5 \cos\left(\frac{2\pi m}{M-1}\right), \quad 0 \leq m \leq M-1 $$
The Hann window first sidelobe is at -31.5 dB, drastically reducing leakage. However, the trade-off is a widening of the mainlobe (width $8\pi/M$), which reduces frequency resolution.

**The Hamming Window:**
$$ w_{hamming}[m] = 0.54 - 0.46 \cos\left(\frac{2\pi m}{M-1}\right), \quad 0 \leq m \leq M-1 $$
The Hamming window is optimized to cancel the largest sidelobe, pushing the first sidelobe down to -41 dB.

**The Blackman Window:**
$$ w_{blackman}[m] = 0.42 - 0.5 \cos\left(\frac{2\pi m}{M-1}\right) + 0.08 \cos\left(\frac{4\pi m}{M-1}\right) $$
Further reduces sidelobes to -58 dB, but the mainlobe is even wider ($12\pi/M$).

### 4.4 The Spectrogram and Parameter Selection

Since $X[n, k]$ is complex, we usually visualize its squared magnitude, known as the **Spectrogram**:
$$ S(n, k) = |X[n, k]|^2 $$
The spectrogram is plotted as a heatmap, with time on the x-axis, frequency on the y-axis, and intensity/color representing energy. It is almost always plotted on a logarithmic scale (dB): $10 \log_{10}(|X[n, k]|^2)$.

**Key Parameters for Implementation:**
1. **Window Length ($M$):** Determines the fundamental trade-off between time and frequency resolution. $M$ is chosen based on the assumed duration of stationarity (e.g., 20-30 ms for speech).
2. **Hop Size ($H$):** The step size by which the window is shifted. The overlap is $M - H$. Typical overlaps are 50% or 75%.
3. **FFT Size ($N$):** Must be $N \geq M$. If $N > M$, the signal is zero-padded. Zero-padding interpolates the spectrum, providing a smoother visual representation without increasing fundamental frequency resolution.

### 4.5 Time-Frequency Resolution Trade-off and Uncertainty Principle

Let $\Delta t$ be the time resolution (effective duration of the window) and $\Delta f$ be the frequency resolution (effective bandwidth of the window's mainlobe).
For a window of length $M$ and sampling frequency $f_s$:
* $\Delta t = M / f_s$
* $\Delta f \approx f_s / M$ (for rectangular window)

Notice that their product is constant:
$$ \Delta t \cdot \Delta f \approx \left(\frac{M}{f_s}\right) \left(\frac{f_s}{M}\right) = 1 $$

**The Formal Heisenberg-Gabor Uncertainty Principle:**
Formally, it can be proven that for any continuous-time signal $x(t)$, the product of its time variance $\sigma_t^2$ and frequency variance $\sigma_f^2$ is strictly bounded:
$$ \sigma_t \cdot \sigma_f \geq \frac{1}{4\pi} $$
Where:
$$ \sigma_t^2 = \frac{\int_{-\infty}^{\infty} t^2 |x(t)|^2 dt}{\int_{-\infty}^{\infty} |x(t)|^2 dt} \quad \text{and} \quad \sigma_f^2 = \frac{\int_{-\infty}^{\infty} f^2 |X(f)|^2 df}{\int_{-\infty}^{\infty} |X(f)|^2 df} $$
You cannot simultaneously achieve infinite precision in both time and frequency. 
* A narrow window yields excellent time resolution but poor frequency resolution (wide horizontal smearing in the spectrogram).
* A wide window yields excellent frequency resolution but poor time resolution (wide vertical smearing in the spectrogram).

This leads to the motivation for the **Continuous Wavelet Transform (CWT)**, which uses variable-length windows (short windows for high frequencies, long windows for low frequencies) to achieve multiresolution analysis, bypassing the fixed-grid limitation of the STFT.

### 4.6 Overlap-Add (OLA) Method and Perfect Reconstruction

When processing signals in the STFT domain (e.g., for noise suppression or pitch shifting), we must eventually reconstruct a time-domain signal $x[n]$ from modified STFT frames $\hat{X}[n, k]$.
This is done using the Inverse DFT on each frame, producing overlapping time-domain segments, which are then added together. This is the **Overlap-Add (OLA)** method.

Let $y_r[n]$ be the IDFT of the $r$-th frame, shifted to its correct position $rH$:
$$ y_r[n] = x[n] w[n-rH] $$
The reconstructed signal is:
$$ \hat{x}[n] = \frac{\sum_{r=-\infty}^{\infty} y_r[n]}{\sum_{r=-\infty}^{\infty} w[n-rH]} $$

For perfect reconstruction without needing point-by-point division, we require the denominator to be a constant. This is the **Constant Overlap-Add (COLA)** condition.

### 4.7 Overlap-Save (OLS) Method

While OLA adds overlapping segments, an alternative is **Overlap-Save (OLS)**. OLS is typically used for fast convolution. In the context of STFT filterbanks, if the modification in the frequency domain corresponds to a linear filter of length $L$, circular convolution artifacts will occur. In OLS, we discard the first $L-1$ samples of the IDFT output of each frame and only keep the "valid" linear convolution samples, concatenating them without addition.

### 4.8 DFT-Bank Interpretation

The STFT can be equivalently viewed from the frequency domain. Consider the definition:
$$ X[n, k] = \sum_{m} x[m] w[m-n] e^{-j\frac{2\pi}{N}km} $$
Let $l = n-m \implies m = n-l$. Substituting this:
$$ X[n, k] = \sum_{l} x[n-l] w[-l] e^{-j\frac{2\pi}{N}k(n-l)} $$
$$ X[n, k] = e^{-j\frac{2\pi}{N}kn} \sum_{l} x[n-l] \left( w[-l] e^{j\frac{2\pi}{N}kl} \right) $$

Let $h_k[l] = w[-l] e^{j\frac{2\pi}{N}kl}$. The summation is exactly the convolution of $x[n]$ with the filter impulse response $h_k[n]$.
Since $w[-l]$ is a lowpass prototype filter, $h_k[l]$ is a bandpass filter centered at $\omega_k = \frac{2\pi k}{N}$.
Therefore, the STFT is mathematically equivalent to passing the signal through a **uniform bank of $N$ bandpass filters**, and then demodulating the output (the phase term outside the sum).

---
## 5. COMPLETE PROOFS AND DERIVATIONS

### 5.1 Proof of the Constant Overlap-Add (COLA) Condition

**Theorem:** A signal $x[n]$ can be perfectly reconstructed from its unmodified STFT frames simply by summing them (Overlap-Add) if and only if the window function $w[n]$ and hop size $H$ satisfy:
$$ \sum_{r=-\infty}^{\infty} w[n-rH] = C \quad \forall n $$
where $C$ is a non-zero constant.

**Proof:**
1. Let the STFT be computed at discrete time frames $n_r = rH$, where $r \in \mathbb{Z}$ is the frame index and $H$ is the hop size.
2. The $r$-th STFT frame is:
   $$ X_r[k] = \sum_{m} x[m] w[m-rH] e^{-j\frac{2\pi}{N}km} $$
3. To reconstruct, we take the $N$-point Inverse DFT of $X_r[k]$ with respect to $k$. Assuming $N \geq M$ (no time aliasing), the IDFT yields the windowed segment exactly:
   $$ y_r[m] = \text{IDFT}\{ X_r[k] \} = x[m] w[m-rH] $$
4. The overlap-add reconstruction sums these individual windowed frames over all frame indices $r$:
   $$ \hat{x}[m] = \sum_{r=-\infty}^{\infty} y_r[m] = \sum_{r=-\infty}^{\infty} x[m] w[m-rH] $$
5. Since $x[m]$ is independent of $r$ (it's the global time sequence), we can factor it out of the summation:
   $$ \hat{x}[m] = x[m] \left( \sum_{r=-\infty}^{\infty} w[m-rH] \right) $$
6. For perfect reconstruction, we require the reconstructed signal $\hat{x}[m]$ to be a scaled version of the original $x[m]$, meaning $\hat{x}[m] = C \cdot x[m]$. Therefore, we must have:
   $$ \sum_{r=-\infty}^{\infty} w[m-rH] = C \quad \forall m $$
7. If $C=1$, the sum perfectly reproduces $x[m]$ without any scaling. If $C \neq 1$, we simply divide the final sum by $C$.
8. **Q.E.D.**

### 5.2 Derivation of the DFT-Bank Equivalence

We have already sketched this, but let's formalize the derivation of the STFT as a filter bank.
Let the input signal be $x[n]$. We wish to find a linear time-invariant (LTI) filter interpretation.
Define a prototype low-pass filter with impulse response $h_0[n] = w[-n]$.
The frequency response of this low-pass filter is $H_0(e^{j\omega}) = W^*(e^{j\omega})$.

We modulate this low-pass filter to $N$ different center frequencies $\omega_k = \frac{2\pi k}{N}$:
$$ h_k[n] = h_0[n] e^{j\frac{2\pi k}{N}n} = w[-n] e^{j\frac{2\pi k}{N}n} $$
When we pass $x[n]$ through this $k$-th filter, the output $y_k[n]$ is given by convolution:
$$ y_k[n] = \sum_{l=-\infty}^{\infty} x[l] h_k[n-l] = \sum_{l} x[l] w[-(n-l)] e^{j\frac{2\pi k}{N}(n-l)} $$
$$ y_k[n] = e^{j\frac{2\pi k}{N}n} \sum_{l} x[l] w[l-n] e^{-j\frac{2\pi k}{N}l} $$
Comparing this to the STFT definition:
$$ X[n, k] = \sum_{l} x[l] w[l-n] e^{-j\frac{2\pi k}{N}l} $$
We clearly see that:
$$ y_k[n] = e^{j\frac{2\pi k}{N}n} X[n, k] $$
$$ \implies X[n, k] = y_k[n] e^{-j\frac{2\pi k}{N}n} $$
**Conclusion:** The STFT bin $X[n, k]$ is the result of passing $x[n]$ through the bandpass filter $h_k[n]$, followed by a complex demodulation (multiplication by $e^{-j\frac{2\pi k}{N}n}$) to shift the bandpass signal back down to baseband.

### 5.3 Proof of the Wigner-Ville Distribution (WVD) Interference Term

The Wigner-Ville Distribution is defined as:
$$ W(t, \omega) = \int_{-\infty}^{\infty} x(t + \frac{\tau}{2}) x^*(t - \frac{\tau}{2}) e^{-j\omega \tau} d\tau $$
To demonstrate why WVD is not always preferred despite its high resolution, let $x(t) = s_1(t) + s_2(t)$.
$$ W_x(t, \omega) = \int (s_1(t+\frac{\tau}{2}) + s_2(t+\frac{\tau}{2})) (s_1^*(t-\frac{\tau}{2}) + s_2^*(t-\frac{\tau}{2})) e^{-j\omega \tau} d\tau $$
Expanding the product yields four terms:
1. $s_1 s_1^*$ which gives $W_{s1}(t, \omega)$
2. $s_2 s_2^*$ which gives $W_{s2}(t, \omega)$
3. Cross term $s_1 s_2^*$
4. Cross term $s_2 s_1^*$

The cross terms $2 \text{Re}\{W_{s1, s2}(t, \omega)\}$ oscillate precisely midway between the auto-terms $W_{s1}$ and $W_{s2}$ in both time and frequency. For complex multicomponent signals (like speech), these interference terms completely obscure the true signal features, explaining why the STFT (a linear transform with no cross-terms) remains the industry standard.

---
## 6. WORKED EXAMPLES (MINIMUM 5 — fully solved)

### Example 1: STFT of a Piecewise Sinusoid
**Problem statement:** 
A discrete-time signal is defined as:
$$ x[n] = \begin{cases} \cos(0.2\pi n), & 0 \leq n < 32 \\ \cos(0.6\pi n), & 32 \leq n < 64 \\ 0, & \text{otherwise} \end{cases} $$
Describe the expected output of an STFT with a rectangular window of length $M=16$, hop size $H=8$, and FFT size $N=16$. Compute the dominant bins $k$ for each frame.

**Solution:**
1. **Frame 1 ($n=0$, covers $m \in [0, 15]$):** 
   The windowed signal is purely $\cos(0.2\pi n)$.
   Frequency $\omega = 0.2\pi$. The corresponding FFT bin is $k = \frac{\omega}{2\pi/N} = \frac{0.2\pi}{2\pi/16} = 1.6$.
   Since $k=1.6$ is not an integer, energy will be split primarily between bin $k=1$ and $k=2$ due to spectral leakage.
2. **Frame 2 ($n=8$, covers $m \in [8, 23]$):**
   Signal is still purely $\cos(0.2\pi n)$. Same frequency content. Bins $k=1, 2$ dominate.
3. **Frame 3 ($n=16$, covers $m \in [16, 31]$):**
   Signal is still purely $\cos(0.2\pi n)$. Bins $k=1, 2$ dominate.
4. **Frame 4 ($n=24$, covers $m \in [24, 39]$):**
   The window covers $24 \leq m \leq 31$ (where freq is $0.2\pi$) and $32 \leq m \leq 39$ (where freq is $0.6\pi$).
   The STFT will show energy at both $0.2\pi$ and $0.6\pi$ during this transitional frame. Bins $k=1,2$ and $k=4,5$ will have energy.
5. **Frame 5 ($n=32$, covers $m \in [32, 47]$):**
   The windowed signal is purely $\cos(0.6\pi n)$.
   Frequency $\omega = 0.6\pi \implies k = \frac{0.6\pi}{2\pi/16} = 4.8$.
   Energy will be clustered heavily around bins $k=4$ and $k=5$.

**Physical interpretation:** 
The STFT clearly tracks the frequency shift from low to high over time, unlike a global DFT which would just show peaks indiscriminately. The transitional frame shows spectral mixing because the window length is long enough to straddle the boundary.

### Example 2: Resolution Calculation and System Design
**Problem statement:** 
An STFT is applied to a signal sampled at $f_s = 8000$ Hz. A rectangular window of length $M = 256$ is used.
a) Compute the time resolution $\Delta t$ and frequency resolution $\Delta f$.
b) Can this setup resolve two sinusoidal components at 1000 Hz and 1030 Hz?
c) What must $M$ be to achieve a frequency resolution of 10 Hz?

**Solution:**
a) **Time and Frequency Resolution:**
   $$ \Delta t = \frac{M}{f_s} = \frac{256}{8000} = 0.032 \text{ seconds} = 32 \text{ ms} $$
   For a rectangular window, the mainlobe width is approximately $\frac{f_s}{M}$.
   $$ \Delta f = \frac{f_s}{M} = \frac{8000}{256} = 31.25 \text{ Hz} $$
b) **Resolvability:**
   The frequency separation between the two tones is $\Delta F = 1030 - 1000 = 30 \text{ Hz}$.
   Since $\Delta F < \Delta f$ ($30 \text{ Hz} < 31.25 \text{ Hz}$), the two mainlobes will heavily overlap. 
   **Conclusion:** No, the system cannot easily resolve these two frequencies. They will merge into a single broad peak.
c) **Designing for 10 Hz Resolution:**
   Set $\Delta f = 10 \text{ Hz}$.
   $$ 10 = \frac{8000}{M} \implies M = 800 \text{ samples} $$

**Physical interpretation:** 
To resolve frequencies close together, we must observe the signal for a longer duration. Increasing $M$ to 800 means our time resolution worsens to $100$ ms.

### Example 3: Narrowband vs. Wideband Spectrograms for Speech Analysis
**Problem statement:** 
For a speech signal sampled at $f_s = 16000$ Hz, you are tasked with creating two spectrograms:
1) A "Wideband" spectrogram to resolve rapid transient events (like formants and glottal pulses).
2) A "Narrowband" spectrogram to track the exact pitch (fundamental frequency) harmonics.
Determine suitable window lengths $M$ in samples and milliseconds for both cases. Assume average male pitch is 100 Hz.

**Solution:**
1. **Wideband Spectrogram (High Time Resolution):**
   We need a short window to capture rapid events. Standard is $3 \text{ ms} - 5 \text{ ms}$.
   Let's choose $T_w = 4 \text{ ms}$.
   $$ M = T_w \times f_s = 0.004 \times 16000 = 64 \text{ samples} $$
   Frequency resolution is $\Delta f \approx 16000 / 64 = 250 \text{ Hz}$.
   Since $\Delta f = 250 \text{ Hz}$, individual pitch harmonics (spaced by 100 Hz) will blur together, highlighting the broader formant envelopes of the vocal tract.
2. **Narrowband Spectrogram (High Frequency Resolution):**
   We need a long window to resolve the 100 Hz harmonics. We need $\Delta f \ll 100 \text{ Hz}$. Let's target $\Delta f = 40 \text{ Hz}$.
   $$ M = \frac{f_s}{\Delta f} = \frac{16000}{40} = 400 \text{ samples} $$
   Time resolution is $\Delta t = M / f_s = 400 / 16000 = 25 \text{ ms}$.
   Individual harmonics will be clearly visible as thin horizontal lines, but rapid time transients will be smeared.

**Physical interpretation:** Wideband spectrograms emphasize the vocal tract transfer function (formants), while narrowband spectrograms emphasize the glottal source (pitch harmonics). This demonstrates the source-filter model of speech production visually.

### Example 4: Verifying the COLA Condition for Hann Window
**Problem statement:** 
Show mathematically that the Hann window satisfies the Constant Overlap-Add (COLA) condition for an overlap of 50%.

**Solution:**
1. The Hann window is defined as:
   $$ w[n] = 0.5 - 0.5 \cos\left(\frac{2\pi n}{M-1}\right) $$
   for $0 \leq n \leq M-1$. For mathematical convenience, let's use the symmetric version $w[n] = 0.5 - 0.5 \cos(2\pi n / M)$ defined for $-M/2 \leq n < M/2$.
2. An overlap of 50% means the hop size is $H = M/2$.
3. We need to evaluate the sum:
   $$ S[n] = \sum_{r=-\infty}^{\infty} w[n-rH] $$
4. At any specific time index $n$, exactly two windows will overlap significantly.
   Let's consider a point $n$ within the first window $w_0[n] = w[n]$.
   The overlapping window at this time is the previous window $w_{-1}[n] = w[n+M/2]$.
5. The sum is:
   $$ S[n] = w[n] + w[n+M/2] $$
6. Substituting the Hann equation:
   $$ S[n] = \left( 0.5 - 0.5 \cos\left(\frac{2\pi n}{M}\right) \right) + \left( 0.5 - 0.5 \cos\left(\frac{2\pi (n + M/2)}{M}\right) \right) $$
7. Expanding the cosine term:
   $$ \cos\left(\frac{2\pi (n + M/2)}{M}\right) = \cos\left(\frac{2\pi n}{M} + \pi\right) = -\cos\left(\frac{2\pi n}{M}\right) $$
8. Therefore:
   $$ S[n] = 0.5 - 0.5 \cos\left(\frac{2\pi n}{M}\right) + 0.5 - 0.5\left(-\cos\left(\frac{2\pi n}{M}\right)\right) = 0.5 + 0.5 = 1 $$
9. Since $S[n] = 1$ (a constant), the COLA condition is perfectly satisfied.

**Physical interpretation:** A 50% overlapped Hann window adds perfectly to a flat line of amplitude 1, meaning an unmodified signal passed through this STFT and reconstructed will have zero amplitude distortion.

### Example 5: Magnitude vs Power Spectrogram dB Conversion
**Problem statement:** 
In an STFT bin, the complex value is $X[n,k] = 3 + j4$. 
Calculate the magnitude, the power, and the representation in decibels (dB) for a power spectrogram.

**Solution:**
1. **Magnitude:**
   $$ |X[n,k]| = \sqrt{3^2 + 4^2} = \sqrt{9+16} = 5 $$
2. **Power:**
   The power spectrogram is the squared magnitude:
   $$ P[n,k] = |X[n,k]|^2 = 5^2 = 25 $$
3. **Decibels (dB):**
   Using the power rule for dB:
   $$ P_{dB} = 10 \log_{10}(P[n,k]) = 10 \log_{10}(25) $$
   $$ \log_{10}(25) = \log_{10}(100/4) = 2 - \log_{10}(4) \approx 2 - 0.602 = 1.398 $$
   $$ P_{dB} = 10 \times 1.398 = 13.98 \text{ dB} $$
   Alternatively, using magnitude:
   $$ 20 \log_{10}(|X[n,k]|) = 20 \log_{10}(5) = 20 \times 0.699 = 13.98 \text{ dB} $$

**Physical interpretation:** Logarithmic scaling mimics human perception (Weber-Fechner law) and allows massive dynamic ranges (from strong formants to faint background noise) to be visualized on the same colormap.

### Example 6: COLA with Hamming Window
**Problem statement:**
Does a Hamming window $w[n] = 0.54 - 0.46\cos(2\pi n/M)$ satisfy COLA at 50% overlap?
**Solution:**
1. At 50% overlap ($H = M/2$), we sum $w[n] + w[n+M/2]$.
2. $S[n] = 0.54 - 0.46\cos(2\pi n/M) + 0.54 - 0.46\cos(2\pi n/M + \pi)$.
3. $S[n] = 1.08 - 0.46\cos(2\pi n/M) + 0.46\cos(2\pi n/M) = 1.08$.
4. Yes, the sum is a constant 1.08. We must simply divide the reconstructed signal by 1.08 to retrieve the exact original signal.

### Example 7: Frequency Bin Calculation
**Problem statement:**
An STFT uses $N = 1024$ and $f_s = 44.1$ kHz. What is the physical frequency in Hz of the bin $k = 120$?
**Solution:**
1. The bin resolution (width of one FFT bin) is $f_s / N$.
2. $\Delta f = 44100 / 1024 = 43.066$ Hz/bin.
3. Frequency of bin $k$ is $f_k = k \times \Delta f$.
4. $f_{120} = 120 \times 43.066 = 5168$ Hz.

---
## 7. ENGINEERING APPLICATIONS AND CASE STUDIES

### 7.1 Speech Recognition and Mel-Spectrograms
Modern Automatic Speech Recognition (ASR) systems (like Siri, Alexa) do not process raw audio waveforms directly. They compute the STFT, extract the magnitude spectrogram, and then map the linear frequency bins to the **Mel scale**. 
The Mel scale relates perceived frequency, or pitch, of a pure tone to its actual measured frequency, allocating more bins to lower frequencies where human ears are more sensitive.
The formula for Mel frequency is:
$$ m = 2595 \log_{10}\left(1 + \frac{f}{700}\right) $$
The resulting Mel-Spectrogram is treated as a 2D image and fed into Convolutional Neural Networks (CNNs).
* **Typical System Parameters:** $f_s = 16$ kHz, Window length = 25 ms (400 samples), Hop size = 10 ms (160 samples), NFFT = 512, Number of Mel bands = 80.

### 7.2 Radar Doppler Processing
In Pulse-Doppler radar, the transmitted pulse hits a moving target and returns with a Doppler shift proportional to the target's radial velocity $v_r$.
The Doppler frequency $f_d$ is:
$$ f_d = \frac{2 v_r f_0}{c} $$
where $f_0$ is the transmission frequency and $c$ is the speed of light.
Because the target is accelerating/decelerating (e.g., a turning fighter jet), the velocity $v_r$ and thus the Doppler shift $f_d$ is non-stationary. The STFT is used to generate a Time-Doppler map, tracking the acceleration of objects over time. 

### 7.3 Vibration Monitoring and Machine Diagnostics
In mechanical engineering and EEE, large rotating machines (turbines, generators) are monitored using accelerometers. A bearing fault will create specific frequency signatures (harmonics) that change in amplitude and frequency as the machine speeds up or slows down. An STFT-based condition monitoring system can detect these transient fault signatures before catastrophic failure occurs, allowing for predictive maintenance.

---
## 8. COMMON STUDENT MISCONCEPTIONS AND ERRORS

1. **Misconception:** The STFT provides perfect time-frequency localization.
   **Correction:** Impossible due to the Heisenberg-Gabor uncertainty principle. You must compromise between $\Delta t$ and $\Delta f$. No algorithmic trick can bypass this fundamental mathematical limit.
   
2. **Misconception:** Zero-padding the FFT increases the frequency resolution of the spectrogram.
   **Correction:** Zero-padding only increases the *density* of frequency bins (interpolation in the frequency domain). It does not increase the true resolution (the ability to separate two close frequencies). Only increasing the physical window length $M$ improves true resolution.

3. **Misconception:** You always need exactly 50% overlap for Overlap-Add.
   **Correction:** While 50% is standard for Hann windows, a rectangular window can use 0% overlap, and a Hamming window typically uses 75% overlap. The only strict requirement is the COLA condition $\sum w[n-rH] = C$.

4. **Misconception:** The spectrogram contains all the information needed to perfectly reconstruct the audio.
   **Correction:** The spectrogram $S(n,k) = |X[n,k]|^2$ inherently discards all phase information. If you try to invert a magnitude spectrogram back to audio without phase, it will sound robotic, artifact-heavy, or completely unintelligible. (Iterative techniques like Griffin-Lim exist to estimate the lost phase).

5. **Misconception:** A larger window length is always better because it gives a "cleaner, higher-resolution" spectrum.
   **Correction:** A larger window heavily smears transient events in time. For signals with sharp attacks (like drum beats or plosive consonants), a large window causes "pre-echo" artifacts in processing, where the transient's energy is smeared backward in time before the event actually occurs.

6. **Misconception:** The STFT is computationally identical to the Wigner-Ville Distribution (WVD).
   **Correction:** The STFT is a linear transform using a window. The WVD is a bilinear transform that achieves theoretically higher resolution but suffers from severe cross-term interference for multi-component signals, making visual interpretation very difficult for complex signals.

7. **Misconception:** Changing the hop size $H$ changes the frequency resolution.
   **Correction:** The hop size $H$ only affects the time-density of the frames (how often we sample the spectrum over time). It has absolutely zero effect on the frequency resolution $\Delta f$, which is determined entirely by the window length $M$.

---
## 9. CONNECTIONS TO OTHER LECTURES

* **Builds on:** 
  * Lecture 5 (DFT and IDFT formulas and properties).
  * Lecture 7 (Window Functions, Gibbs phenomenon, and Spectral Leakage).
  * Lecture 11 (Fast Fourier Transform radix-2 algorithms).
* **Foundation for:** 
  * Lecture 18 (Filter Banks and Polyphase representations).
  * Lecture 19 (Continuous and Discrete Wavelet Transforms). The intuition of constant bandwidth filterbanks developed here is crucial for understanding how Wavelets solve the fixed-resolution problem by using constant-$Q$ (logarithmic) filterbanks.
  * Lecture 22 (Speech Processing and MFCC extraction).

---
## 10. EXAMINATION QUESTIONS

### 10.1 Short Answer (5 questions with model answers)

**Q1:** Explain why the Discrete Fourier Transform (DFT) is unsuitable for analyzing a chirp signal.
**Model Answer:** A chirp signal's frequency changes over time (non-stationary). The DFT integrates over all time, discarding temporal information. The resulting magnitude spectrum shows a broad band of all frequencies present but gives no indication of the time order in which they occurred.

**Q2:** State the formal uncertainty principle as applied to STFT.
**Model Answer:** The product of time resolution (variance) $\sigma_t$ and frequency resolution (variance) $\sigma_f$ is strictly lower bounded by $\sigma_t \cdot \sigma_f \geq 1/4\pi$. Consequently, one cannot simultaneously achieve perfect time and frequency resolution; any window design is a trade-off.

**Q3:** What is the fundamental difference between the spectrogram and the STFT?
**Model Answer:** The STFT $X[n,k]$ is a complex-valued linear transform containing both magnitude and phase, preserving all signal information. The spectrogram is a real-valued, non-linear representation defined as the squared magnitude $|X[n,k]|^2$, which discards phase and represents signal power.

**Q4:** Describe the physical meaning of the hop size $H$.
**Model Answer:** The hop size $H$ is the number of time samples by which the analysis window is shifted forward for each successive frame. It dictates the time-density of the STFT and the percentage of overlap ($1 - H/M$).

**Q5:** Why is a Hann window typically preferred over a rectangular window for STFT applications?
**Model Answer:** The rectangular window has abrupt edges causing high sidelobes, leading to severe spectral leakage that obscures weak frequencies. The Hann window tapers smoothly to zero at the edges, drastically reducing sidelobe levels and leakage, at the cost of a slightly wider mainlobe.

### 10.2 Long Answer / Numerical Problems (4 problems with complete solutions)

**Problem 1:** 
Given a signal $x[n]$ sampled at 10 kHz, an STFT is computed using a Hann window of length 512 samples and an overlap of 75%.
a) Calculate the exact time duration of one window in milliseconds.
b) Calculate the approximate frequency resolution in Hz (assume mainlobe width).
c) Calculate the hop size $H$ in samples.
**Solution:**
a) Duration = $M / f_s = 512 / 10000 = 0.0512$ s = 51.2 ms.
b) For a Hann window, the mainlobe width is approx $2 \times f_s / M$. 
   $\Delta f \approx 2 \times 10000 / 512 = 39.06$ Hz. 
c) Overlap is 75%, meaning the window steps forward by 25%. 
   $H = 0.25 \times 512 = 128$ samples.

**Problem 2:**
Prove that if the STFT is viewed as a bank of bandpass filters, the frequency response of the $k$-th filter is simply a frequency-shifted version of the time-reversed window function's spectrum.
**Solution:**
Start with the STFT equation: $X[n, k] = \sum_{m} x[m] w[m-n] e^{-j\frac{2\pi}{N}km}$.
Substitute the index $l = n - m$. This gives $m = n - l$.
$X[n, k] = \sum_{l} x[n-l] w[-l] e^{-j\frac{2\pi}{N}k(n-l)}$.
Factor out the term dependent on $n$ but not $l$:
$X[n, k] = e^{-j\frac{2\pi}{N}kn} \sum_{l} x[n-l] \left( w[-l] e^{j\frac{2\pi}{N}kl} \right)$.
The inner summation is a standard discrete convolution $x[n] * h_k[n]$, where the impulse response is $h_k[n] = w[-n] e^{j\frac{2\pi}{N}kn}$.
By the frequency modulation property of the DTFT, multiplying a time sequence $w[-n]$ by the complex exponential $e^{j\omega_k n}$ shifts its frequency spectrum to center exactly at $\omega_k = \frac{2\pi k}{N}$. Thus, $H_k(e^{j\omega}) = W^*(e^{j(\omega - \omega_k)})$.

**Problem 3:**
A radar system needs to track a fast-moving drone with a strict Doppler resolution of 5 Hz. The system sampling rate is 4 kHz. 
a) What is the minimum required STFT rectangular window length $M$? 
b) If the drone performs rapid evasive maneuvers accelerating significantly within 100 ms, why might this chosen $M$ fail to capture the drone's true velocity trajectory?
**Solution:**
a) We need $\Delta f = 5 \text{ Hz}$. Given $f_s = 4000 \text{ Hz}$.
   $M \approx f_s / \Delta f = 4000 / 5 = 800$ samples.
b) The time duration of this window is $T_w = M / f_s = 800 / 4000 = 0.2$ seconds = 200 ms.
   If the drone accelerates significantly within 100 ms, its velocity (and thus its Doppler frequency) changes dramatically *during the span of a single window*. The STFT stationarity assumption over 200 ms is severely violated. The resulting spectrum will show a broad, smeared frequency band rather than a sharp peak, failing to resolve the exact velocity at any given millisecond.

**Problem 4:**
Evaluate the COLA condition for a rectangular window of length $M=100$. Find three distinct values of hop size $H > 0$ that satisfy the condition perfectly.
**Solution:**
The rectangular window is $w_{rect}[n] = 1$ for $0 \leq n < 100$, and 0 otherwise.
The COLA condition requires $\sum w_{rect}[n - rH] = C$ for all $n$.
Since the window is perfectly flat with an amplitude of 1, the shifted copies must tile the time axis perfectly or overlap such that their sum remains constant everywhere. This occurs whenever $H$ is a factor of $M$.
Value 1: $H = 100$ (0% overlap, sum $C=1$ everywhere).
Value 2: $H = 50$ (50% overlap, sum $C=2$ everywhere).
Value 3: $H = 25$ (75% overlap, sum $C=4$ everywhere).
Any of these hop sizes will allow for perfect Overlap-Add reconstruction.

### 10.3 True/False with Justification (6 items)

1. **True/False:** Increasing the FFT size $N$ (e.g., from 512 to 1024) for a fixed window size $M=256$ improves the system's fundamental ability to distinguish two closely spaced frequencies.
   **False:** Increasing $N$ past $M$ is simply zero-padding. It interpolates the spectrum, creating more bins, but the physical width of the mainlobe (which dictates true resolution) is fixed by $M$.
2. **True/False:** The STFT magnitude of a purely stationary infinite sine wave is mathematically identical for all time frames $n$.
   **True:** For a stationary sine wave, the amplitude and frequency content do not change. The magnitude $|X[n,k]|$ is identical across all frames. (The phase, however, will rotate depending on $n$ and the hop size).
3. **True/False:** The Hamming window eliminates spectral leakage entirely.
   **False:** The Hamming window significantly reduces sidelobes (down to -41 dB) compared to the rectangular window, but it does not eliminate leakage. Infinite time-domain signals are required for zero leakage (a delta function in frequency).
4. **True/False:** Perfect Overlap-Add reconstruction requires the window function to be an even (symmetric) function.
   **False:** The OLA method only requires the COLA summation condition ($\sum w[n-rH] = C$) to be met. While symmetric windows are universally used in practice, mathematical symmetry is not a strict requirement for COLA.
5. **True/False:** A wideband spectrogram uses a very short time window.
   **True:** Short time windows yield wide frequency mainlobes (hence "wideband"), heavily smearing frequency but resolving rapid time events very finely.
6. **True/False:** The Continuous Wavelet Transform offers superior frequency resolution at low frequencies compared to an STFT with a fixed window size.
   **True:** The CWT uses multiresolution analysis. It uses long windows for low frequencies (yielding high frequency resolution) and short windows for high frequencies, overcoming the fixed-resolution trade-off of the STFT.

---
## 11. KEY FORMULAS REFERENCE

| Concept | Formula | Notation & Variables |
|---------|---------|----------------------|
| **DTFT Equation** | $X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n}$ | $\omega$ is continuous freq in rad/sample |
| **STFT Definition** | $X[n, k] = \sum_{m} x[m] w[m-n] e^{-j\frac{2\pi}{N}km}$ | $n$ is time frame, $k$ is freq bin |
| **Spectrogram** | $S(n, k) = \|X[n, k]\|^2$ | Real-valued energy density |
| **Uncertainty Principle** | $\sigma_t \cdot \sigma_f \geq \frac{1}{4\pi}$ | Theoretical lower bound for variance |
| **Time Resolution** | $\Delta t \approx \frac{M}{f_s}$ | $M$ is window length, $f_s$ is sampling rate |
| **Freq Resolution** | $\Delta f \approx \frac{f_s}{M}$ | For rectangular window (in Hertz) |
| **OLA Reconstruction** | $\hat{x}[n] = \frac{\sum_r y_r[n]}{\sum_r w[n-rH]}$ | $y_r[n]$ is IDFT of the $r$-th frame |
| **COLA Condition** | $\sum_{r=-\infty}^{\infty} w[n-rH] = C$ | Required for perfect OLA reconstruction |
| **Hann Window** | $w[n] = 0.5 - 0.5 \cos(\frac{2\pi n}{M-1})$ | Tapered window to reduce leakage |
| **Mel Frequency** | $m = 2595 \log_{10}(1 + \frac{f}{700})$ | Perceptual frequency scale mapping |

---
## 12. FURTHER READING AND REFERENCES

1. **Proakis, J. G., & Manolakis, D. G.** (2006). *Digital Signal Processing: Principles, Algorithms, and Applications* (4th ed.). Pearson. (Refer to Chapter 10 for Multirate processing, filter banks, and time-frequency transformations).
2. **Oppenheim, A. V., & Schafer, R. W.** (2010). *Discrete-Time Signal Processing* (3rd ed.). Pearson. (Refer to Chapter 11 on Fourier Analysis of Signals Using the DFT, with deep sections on windowing effects).
3. **Haykin, S.** (2001). *Adaptive Filter Theory* (4th ed.). Prentice Hall. (Excellent background on non-stationary signal statistics and optimal filtering).
4. **Allen, J. B., & Rabiner, L. R.** (1977). "A unified approach to short-time Fourier analysis and synthesis." *Proceedings of the IEEE*, 65(11), 1558-1564. (The seminal, must-read foundational paper formalizing the STFT and OLA mathematically).
5. **Smith, J. O.** (2011). *Spectral Audio Signal Processing*. W3K Publishing. (Highly recommended for practical implementations of STFT in audio contexts).

---
## 13. APPENDIX: MATLAB & PYTHON IMPLEMENTATION GUIDE

### MATLAB Implementation
In MATLAB, the spectrogram function is the primary tool for computing and visualizing the STFT.

`matlab
% Define signal parameters
fs = 16000; % 16 kHz sampling rate
t = 0:1/fs:2-1/fs; % 2 seconds duration
% Create a chirp signal that goes from 100 Hz to 2000 Hz
x = chirp(t, 100, 2, 2000); 

% STFT Parameters
M = 512; % Window length (samples)
H = 256; % Hop size (50% overlap)
NFFT = 1024; % FFT size (zero-padded)
window = hann(M);

% Compute and plot spectrogram
figure;
spectrogram(x, window, M-H, NFFT, fs, 'yaxis');
title('Spectrogram of a Chirp Signal');
`

**Common MATLAB pitfalls for students:**
1. Confusing 'overlap' with 'hop size'. MATLAB's spectrogram takes 
overlap as an argument, which is  - H$, not $.
2. The 'yaxis' flag is crucial; without it, MATLAB plots frequency on the x-axis and time on the y-axis, which goes against standard engineering convention.

### Python (SciPy) Implementation
In Python, the scipy.signal module provides equivalent functionality.

`python
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Define signal parameters
fs = 16000
t = np.arange(0, 2, 1/fs)
# Create a chirp signal
x = signal.chirp(t, f0=100, t1=2, f1=2000)

# STFT Parameters
M = 512
H = 256
NFFT = 1024

# Compute spectrogram
frequencies, times, Sxx = signal.spectrogram(x, fs=fs, window='hann', 
                                             nperseg=M, noverlap=M-H, nfft=NFFT)

# Plot
plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.title('Spectrogram (dB)')
plt.colorbar(label='Intensity [dB]')
plt.show()
`

---
## 14. GLOSSARY OF TERMS

* **Stationary Signal:** A signal whose frequency content and statistical properties do not change over time.
* **Non-Stationary Signal:** A signal whose frequency content changes over time (e.g., speech, music).
* **Windowing:** The process of multiplying a signal by a finite-duration function to isolate a specific segment in time.
* **Spectral Leakage:** The phenomenon where energy from a specific frequency spreads into adjacent frequencies due to the abrupt truncation of a signal (windowing).
* **Mainlobe:** The central, highest-amplitude portion of a window's frequency response, determining frequency resolution.
* **Sidelobes:** The secondary, lower-amplitude peaks in a window's frequency response, causing spectral leakage.
* **Spectrogram:** A visual representation of the spectrum of frequencies of a signal as it varies with time.
* **Hop Size:** The number of samples by which the analysis window is shifted for each successive STFT frame.
* **Overlap:** The number of samples shared between two adjacent windowed segments.
* **Zero-Padding:** Appending zeros to a signal before computing the FFT to interpolate the frequency spectrum.
* **Formants:** The resonant frequencies of the human vocal tract, visible as dark bands in a speech spectrogram.
