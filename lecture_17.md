# Lecture 17: Short-Time Fourier Transform (STFT) & Spectrogram

**Course:** EE3621 — Digital Signal Processing  
**Target Audience:** III B.Tech EEE Students  
**Duration:** 40 Minutes  

* **Available Formats:** [LaTeX Source File](lecture_17.tex) | [Compiled PDF Notes](lecture_17.pdf)

---

## 1. Lecture Plan (40 Minutes Breakdown)

* **00:00 – 05:00 (5 mins):** **Motivation: Non-stationary signals**. Why DFT/DTFT fail for signals whose frequency content changes over time (speech, EEG).
* **05:00 – 12:00 (7 mins):** **STFT Definition & Physical Intuition**. Mathematical formulation, shifting windows, and local spectrum interpretation.
* **12:00 – 17:00 (5 mins):** **Window Function Role**. Rectangular vs. Hanning/Hamming windows, spectral leakage, and Gibbs phenomenon.
* **17:00 – 25:00 (8 mins):** **Time-Frequency Resolution Trade-off**. Heisenberg uncertainty principle for discrete signals. The bandwidth-duration product.
* **25:00 – 30:00 (5 mins):** **Spectrogram**. Definition, practical parameters (window length, hop size, FFT size), and speech formants example.
* **30:00 – 34:00 (4 mins):** **Overlap-Add (OLA) Method & Reconstruction**. Perfect reconstruction condition and proof.
* **34:00 – 37:00 (3 mins):** **Advanced & Alternative Views**. Wigner-Ville Distribution (cross-terms) and DFT-bank interpretation of STFT.
* **37:00 – 40:00 (3 mins):** **Applications & Checkpoints**. Radar, ECG, Audio compression. 3 Checkpoint questions.

---

## 2. Motivation: Non-stationary Signals

The Discrete-Time Fourier Transform (DTFT) and the Discrete Fourier Transform (DFT) are powerful tools for analyzing the frequency content of a signal. The DTFT is defined as:
$$ X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n} $$

**The Stationarity Assumption:**
The underlying assumption of the DFT and DTFT is that the signal $x[n]$ is **stationary**. This means its statistical properties and frequency content do not change over time. When we compute the standard Fourier transform, we sum over all time from $-\infty$ to $\infty$. The resulting spectrum $X(e^{j\omega})$ tells us *what* frequencies exist in the signal, but it completely destroys any information about *when* those frequencies occurred.

**Real-world Non-stationary Signals:**
* **Speech:** As you speak, your vocal tract changes shape. A vowel sound like "ah" has completely different harmonics than a consonant like "s". The frequencies change rapidly over time.
* **EEG (Brainwaves):** The electrical activity in the brain changes depending on the state of the subject (e.g., awake, sleeping, seizing).
* **Music/Audio:** A piano playing a melody produces different notes (frequencies) at different times.

If we take the DFT of an entire 3-minute song, the output will just show all the notes that were played in the song, jumbled together. We need a method to analyze frequency content as it evolves over time: **Time-Frequency Analysis**.

**Physical Intuition:** 
Imagine looking through a narrow slit that slides across a long scroll of paper. At any given moment, you only see a small portion of the scroll. The STFT applies this exact concept to signals using a "window" function.

---

## 3. STFT Definition

To analyze a signal at a specific time $n$, we multiply the signal by a window function $w[m-n]$ centered at time $n$. This window is typically non-zero only for a short duration (length $M$). This isolates a short segment of the signal around time $n$. We then take the Fourier transform of this isolated segment.

The Short-Time Fourier Transform (STFT) is defined as:
$$ X[n, k] = \sum_{m=-\infty}^{\infty} x[m] w[m-n] e^{-j\frac{2\pi}{N}km} $$

### Step-by-Step Breakdown of the Formula:
1. $x[m]$ is our infinite-length or long duration signal.
2. $w[m-n]$ is the **analysis window** of length $M$, shifted so its reference point (usually the center or start) is at time $n$.
3. The product $x_n[m] = x[m] w[m-n]$ is the "windowed" signal, which only contains the values of $x[m]$ near time $n$.
4. The summation over $m$ with the exponential term $e^{-j\frac{2\pi}{N}km}$ is simply the $N$-point DFT of the windowed signal $x_n[m]$.
5. The result $X[n, k]$ is a two-dimensional function: $n$ represents the time index, and $k$ represents the frequency bin.

**KEY RESULT:** The STFT gives us the "local spectrum" of the signal at time $n$.

---

## 4. The Role of the Window Function

The choice of the window function $w[m]$ is crucial. In time, multiplying the signal by $w[m]$ corresponds to convolution in the frequency domain.

### The Rectangular Window
A rectangular window simply cuts off the signal abruptly:
$$ w_{rect}[m] = \begin{cases} 1, & 0 \leq m \leq M-1 \\ 0, & \text{otherwise} \end{cases} $$

**Spectral Leakage and Gibbs Phenomenon:**
Because the rectangular window has sharp transitions (edges) in the time domain, its frequency response (a sinc function) has a narrow mainlobe but very high sidelobes. When we convolve the signal's spectrum with these sidelobes, energy from one frequency bin "leaks" into adjacent bins. This is known as **spectral leakage**. If the signal contains a strong frequency component, it will obscure weaker, nearby frequency components because of these high sidelobes.

### Hanning and Hamming Windows
To reduce spectral leakage, we use windows that taper off smoothly at the edges, avoiding sharp discontinuities.

The Hamming window is defined as:
$$ w_{hamming}[m] = 0.54 - 0.46 \cos\left(\frac{2\pi m}{M-1}\right) \quad \text{for } 0 \leq m \leq M-1 $$

The Hanning window is defined as:
$$ w_{hanning}[m] = 0.5 - 0.5 \cos\left(\frac{2\pi m}{M-1}\right) \quad \text{for } 0 \leq m \leq M-1 $$

**Trade-offs in Window Design:**
* Tapering the ends reduces the height of the sidelobes (less spectral leakage).
* However, tapering reduces the effective length of the window, which widens the mainlobe in the frequency domain.
* A wider mainlobe means decreased frequency resolution (inability to distinguish two closely spaced frequencies).

---

## 5. Time-Frequency Resolution Trade-off

One of the most fundamental principles in signal processing is the **Heisenberg Uncertainty Principle** applied to time-frequency analysis.

For continuous signals, the product of the time duration $\Delta t$ and the frequency bandwidth $\Delta f$ is lower bounded:
$$ \Delta t \cdot \Delta f \geq \frac{1}{4\pi} $$

For discrete signals, a similar bound exists. Let's explore the physical intuition:

* **Wide Window (Large $M$):** 
  * A long time window captures many cycles of a low-frequency wave. 
  * The DFT of this long segment has very fine frequency bins.
  * **Result:** Excellent frequency resolution, but poor time resolution (we don't know exactly *when* within that wide window a short event occurred).
* **Narrow Window (Small $M$):**
  * A short time window captures rapid transient events accurately in time.
  * The DFT of a short segment has very wide frequency bins.
  * **Result:** Excellent time resolution, but poor frequency resolution.

**The Bandwidth-Duration Product:**
You cannot simultaneously achieve arbitrarily high resolution in both time and frequency. If you want to know exactly what frequency is present, you must observe it over a long time. If you want to know exactly when an event happened, you must look at a very short time slice, thereby losing frequency precision.

---

## 6. Spectrogram

The **Spectrogram** is the most common way to visualize the STFT. Because $X[n,k]$ is complex, we typically plot its magnitude squared.
$$ \text{Spectrogram}(n, k) = |X[n, k]|^2 $$

This is a 2D plot (usually visualized as a heatmap or image):
* **X-axis:** Time index $n$
* **Y-axis:** Frequency bin $k$
* **Color/Intensity:** Magnitude $|X[n, k]|^2$ (often plotted in dB: $10 \log_{10}(|X[n, k]|^2)$)

### Practical Parameters for Computing a Spectrogram:
1. **Window Length ($M$):** Dictates the time-frequency resolution trade-off. For speech, 20-30 ms is standard to assume short-term stationarity.
2. **Hop Size ($H$):** The number of samples we advance the window for the next STFT frame. If $M=1000$ and $H=250$, the overlap is 75%. High overlap produces a smoother spectrogram at the cost of more computation.
3. **FFT Size ($N$):** Must be $N \geq M$. If $N > M$, we zero-pad the windowed signal before the FFT. This does not increase true frequency resolution, but it interpolates the spectrum, resulting in a smoother curve.

**Example: Speech Spectrogram:**
In a speech spectrogram, vowels appear as horizontal, dark bands of high energy. These are the resonant frequencies of the vocal tract, called **formants**. Plosive consonants (like 'p' or 't') appear as sudden, wide-band vertical lines (impulse-like events).

---

## 7. Overlap-Add (OLA) Method

Once we modify the signal in the STFT domain (e.g., for noise reduction), we need to convert it back to the time domain. Because the windows overlap, we cannot just inverse-FFT each frame and concatenate them. We must use the **Overlap-Add (OLA)** method.

Let $y_r[m]$ be the inverse DFT of the modified STFT frame $Y[rH, k]$, where $r$ is the frame index and $H$ is the hop size. The frames are placed at their correct time positions and summed.

The reconstructed signal $x[n]$ is given by:
$$ x[n] = \frac{\sum_{r=-\infty}^{\infty} y_r[n]}{\sum_{r=-\infty}^{\infty} w[n-rH]} $$

### Perfect Reconstruction Condition
For the unmodified STFT to perfectly reconstruct the original signal, the sum of the window functions shifted by the hop size $H$ must be a constant for all $n$.

**Theorem:** Perfect reconstruction requires:
$$ \sum_{r=-\infty}^{\infty} w[n-rH] = C \quad \text{for all } n $$
where $C$ is a constant greater than zero. 

**Proof:**
1. Let $X[r, k]$ be the STFT using window $w$. The time-domain frame before FFT is $x[m] w[m-rH]$.
2. The inverse FFT of $X[r, k]$ gives back the windowed segment: $y_r[n] = x[n] w[n-rH]$.
3. Summing these overlapping frames:
   $$ \sum_r y_r[n] = \sum_r x[n] w[n-rH] = x[n] \sum_r w[n-rH] $$
4. If $\sum_r w[n-rH] = C$, then:
   $$ \sum_r y_r[n] = x[n] \cdot C \implies x[n] = \frac{1}{C} \sum_r y_r[n] $$
5. Thus, perfect reconstruction is achieved. Often, $w^2$ is used if the window is applied twice (analysis and synthesis). The Constant Overlap-Add (COLA) condition is crucial in filterbank design.

---

## 8. Alternative Views: Wigner-Ville & DFT-Bank

### Wigner-Ville Distribution (WVD)
The WVD is an alternative time-frequency representation defined as:
$$ WVD(n, \omega) = \sum_{m} x[n+m] x^*[n-m] e^{-j2\omega m} $$
**Advantage:** It offers theoretically optimal time-frequency resolution, bypassing the STFT window trade-off.
**Disadvantage:** It is a bilinear transform. If a signal has two distinct frequency components, the WVD will show artificial "cross-terms" oscillating halfway between them, which makes interpretation very difficult for complex signals.

### DFT-Bank Interpretation of STFT
Instead of thinking of the STFT as shifting a window across time, we can view it from the frequency dimension. 
For a fixed frequency index $k$, $X[n, k]$ as a function of time index $n$ represents the output of passing the signal $x[n]$ through a bandpass filter centered at frequency $\frac{2\pi}{N}k$.
The STFT acts as a **uniform bank of modulated bandpass filters**. The window function $w[n]$ serves as the impulse response of the prototype lowpass filter. This perspective is vital in audio compression.

---

## 9. Numerical Worked Example

**Problem:** 
Consider a signal sampled at $f_s = 8000$ Hz. We want to compute an STFT to analyze a bird chirp. We need a frequency resolution of at least $50$ Hz. What is the minimum window length in samples, and what is the corresponding time resolution?

**Calculations:**
1. **Frequency Resolution ($\Delta f$):** The frequency resolution is roughly the width of the mainlobe, which for a rectangular window is inversely proportional to the window duration $T_w$.
   $$ \Delta f \approx \frac{f_s}{M} $$
2. **Find $M$:**
   $$ 50 \text{ Hz} = \frac{8000}{M} \implies M = \frac{8000}{50} = 160 \text{ samples} $$
3. **Time Resolution ($\Delta t$):** The time resolution is simply the duration of the window in seconds.
   $$ \Delta t = \frac{M}{f_s} = \frac{160}{8000} = 0.02 \text{ seconds} = 20 \text{ ms} $$

If we needed better frequency resolution (e.g., 25 Hz), $M$ would double to 320, and the time resolution would worsen to 40 ms.

---

## 10. Applications

1. **Speech Processing:** The spectrogram is used to identify formants, pitch tracking, and voice activity detection. It is the basis for most speech recognition feature extraction (MFCCs).
2. **Audio Compression (MP3):** MP3 compression uses a Modified Discrete Cosine Transform (MDCT), which is deeply related to the STFT and the OLA method, acting as a filterbank to split audio into frequency subbands and quantize them based on psychoacoustic models.
3. **Radar Doppler Processing:** Analyzing the time-varying Doppler shift of a moving target requires STFT.
4. **ECG Analysis:** Detecting arrhythmias by observing how the heart's electrical frequencies change during abnormal beats.

---

## 11. Key Formulas

| Concept | Formula | Description |
|---------|---------|-------------|
| **DTFT** | $X(e^{j\omega}) = \sum_{n} x[n] e^{-j\omega n}$ | Standard Fourier Transform, infinite time |
| **STFT Definition** | $X[n, k] = \sum_{m} x[m] w[m-n] e^{-j\frac{2\pi}{N}km}$ | Local spectrum at time $n$ |
| **Spectrogram** | $S(n, k) = \|X[n, k]\|^2$ | Energy visualization in time-frequency |
| **Uncertainty Principle** | $\Delta t \cdot \Delta f \geq \frac{1}{4\pi}$ | Bandwidth-duration trade-off |
| **OLA Reconstruction** | $x[n] = \frac{\sum_r y_r[n]}{\sum_r w[n-rH]}$ | Rebuilding signal from overlapping frames |

---

## 12. Checkpoint & Quick Review Questions

1. **Q1:** If you increase the length of the window $M$ in an STFT, what happens to the time resolution and the frequency resolution?
   * *Answer:* 
     * Increasing the window length $M$ means the window spans a longer duration of time.
     * This **worsens (decreases) the time resolution**, because short transient events within that long window cannot be precisely localized in time.
     * However, this **improves (increases) the frequency resolution**, because a longer observation time allows for finer separation of closely spaced frequencies (narrower mainlobe).

2. **Q2:** Why is a Hamming window often preferred over a rectangular window for computing spectrograms of audio signals?
   * *Answer:* 
     * A rectangular window abruptly cuts off the signal at the edges, which causes severe **spectral leakage** (high sidelobes in the frequency domain).
     * This leakage can cause strong frequency components to mask nearby weaker components.
     * A Hamming window tapers smoothly at the edges, greatly reducing the sidelobe levels and minimizing spectral leakage, allowing weaker frequencies to be observed, at the slight cost of widening the mainlobe.

3. **Q3:** For a window function $w[n] = 1$ for $0 \leq n \leq 99$, what is the maximum hop size $H$ that satisfies the Constant Overlap-Add (COLA) perfect reconstruction condition, assuming we simply sum the frames without dividing by a constant?
   * *Answer:* 
     * The COLA condition requires $\sum_r w[n-rH] = C$.
     * Since $w[n]$ is a rectangular window of length $M=100$, to maintain a constant sum of 1 everywhere across the time axis (so no division is needed), the windows must tile perfectly without gaps or overlapping accumulations.
     * Therefore, the hop size must be exactly $H = 100$. If $H > 100$, there will be gaps. If $H < 100$, the sum will fluctuate depending on the overlap alignment unless $H$ is a perfect divisor of $M$.
