<Faculty Notes — Lecture 14: Multirate DSP — Downsampling, Upsampling & Polyphase>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY
Welcome to Lecture 14 on Multirate Digital Signal Processing (DSP). This is one of the most critical topics in modern digital communications, audio engineering, and hardware design. Multirate DSP is fundamental to modern communication systems, enabling us to bridge domains that operate at different sampling rates. While the basic concepts of throwing away samples (downsampling) or inserting zeros (upsampling) seem intuitively simple to students, the frequency-domain consequences often cause significant confusion.

When teaching this lecture, emphasis must be placed on the spectral implications of rate changing. Students often struggle with tracking indices and frequency variables in the polyphase decomposition. Polyphase decomposition is mathematically elegant but requires careful index tracking to fully grasp. The Noble identities are the key to enabling efficient implementation, as they allow us to move the heavy computational burden of filtering to the lowest possible sampling rate.

**Suggested Demos:**
1. Use MATLAB/Python to play a 44.1kHz audio file, decimate it by 4 without an anti-aliasing filter, and let the students hear the aliasing (it will sound like distinct robotic or metallic distortion).
2. Repeat the same, but with a proper FIR anti-aliasing filter to demonstrate the loss of high frequencies without the awful aliasing artifacts.
3. Show a visual spectrum analyzer (FFT plot) during upsampling to clearly display the spectral images appearing across the digital frequency axis.

---
## 1. LEARNING OBJECTIVES
By the end of this comprehensive lecture, students will be able to:
1. **Formulate** the mathematical definitions of downsampling and upsampling in both the time and frequency domains.
2. **Analyze** the effects of multirate operations on the discrete-time Fourier transform (DTFT) and Z-transform, identifying the phenomena of aliasing and imaging.
3. **Design** appropriate anti-aliasing and anti-imaging (interpolation) filters with precise cutoff frequencies and gain values to prevent signal degradation.
4. **Develop** rational rate change systems ($L/M$) by properly cascading interpolators, decimation filters, and downsamplers.
5. **Prove** and **Apply** the Noble Identities to interchange the order of rate-changing operators and Linear Time-Invariant (LTI) filters.
6. **Construct** polyphase decompositions of arbitrary FIR and IIR filters and demonstrate the computational savings they yield in hardware and software implementations.

---
## 2. PREREQUISITE KNOWLEDGE REVIEW
Before attempting this lecture, students must be entirely comfortable with the following core DSP concepts:
* **The Discrete-Time Fourier Transform (DTFT):**
  Definition: $X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n}$
  They must know that the DTFT is always periodic with period $2\pi$.
* **The Z-Transform:**
  Definition: $X(z) = \sum_{n=-\infty}^{\infty} x[n] z^{-n}$
  And its relation to the DTFT: $X(e^{j\omega}) = X(z)|_{z=e^{j\omega}}$
* **Nyquist-Shannon Sampling Theorem:**
  Continuous signals must be sampled at $f_s \geq 2f_{max}$ to avoid aliasing. In the discrete domain, this corresponds to the signal being bandlimited to $\pi$.
* **LTI Systems and Convolution:**
  $y[n] = x[n] * h[n] \longleftrightarrow Y(e^{j\omega}) = X(e^{j\omega})H(e^{j\omega})$
* **Ideal Lowpass Filters:**
  An ideal LPF with cutoff frequency $\omega_c$ has $H(e^{j\omega}) = 1$ for $|\omega| \leq \omega_c$ and $0$ otherwise in the principal period $[-\pi, \pi]$.

Review these quickly in the first 5 minutes. Pay special attention to the $2\pi$ periodicity, as multirate DSP relies heavily on shifting and stretching periods.

---
## 3. HISTORICAL AND MOTIVATIONAL CONTEXT
**Who discovered this?**
The formalization of multirate signal processing largely occurred in the 1970s and 1980s. Pioneers like Ronald E. Crochiere and Lawrence R. Rabiner wrote the definitive texts on the subject in 1983. However, the conceptual roots trace back to the early days of telephony, where engineers needed to multiplex multiple voice channels onto a single transmission line, requiring precise rate conversions. Polyphase filtering concepts were advanced by researchers such as Maurice Bellanger.

**Why does EEE need this? Real Engineering Applications:**
* **Audio Sample Rate Conversion:** Studio audio is often recorded at 48 kHz or 96 kHz. However, CD audio is standardized at 44.1 kHz. Transferring a master recording to a CD requires a highly precise rational rate conversion factor of $L/M = 147/160$.
* **Speech Coding:** In telecommunications, voice is downsampled to 8 kHz to conserve bandwidth.
* **Video Format Conversion:** Transcoding 24 fps cinematic film to 30 fps television broadcast requires frame rate conversion, fundamentally a multirate DSP problem.
* **Sensor Fusion:** Modern digital systems often receive inputs from various sensors (e.g., accelerometers at 1 kHz, temperature at 10 Hz). Fusing this data requires bringing them to a common sampling rate.
* **Software Defined Radios (SDR):** Antennas receive signals in the GHz range. Analog-to-Digital Converters (ADCs) oversample the signal, and then massive digital decimation stages (often using Cascaded Integrator-Comb or CIC filters) step the rate down to the baseband rate for processing by the DSP or FPGA.

Without multirate DSP, every system would be forced to operate at the highest possible sampling rate of its fastest component, leading to massive, unacceptable power consumption and thermal throttling in modern VLSI designs.

---
## 4. THEORETICAL FOUNDATIONS

### 4.1 Downsampling by M (Decimation)
Downsampling by an integer factor $M$ reduces the sampling rate by keeping only every $M$-th sample and discarding the rest.
**Time-domain relation:**
$$y[n] = x[Mn]$$
For example, if $M=3$, $y[0] = x[0]$, $y[1] = x[3]$, $y[2] = x[6]$, etc.

To understand this in the frequency domain, we model the downsampling process in two steps to leverage LTI properties:
1. **Modulation (Zeroing out discarded samples):** Create an intermediate signal $v[n]$ which equals $x[n]$ when $n$ is a multiple of $M$, and $0$ otherwise.
2. **Time Compression:** Remove the zeros to form $y[n]$.

**Step 1: The Impulse Train Modulation**
We can express $v[n]$ mathematically using a discrete impulse train (comb function) $p[n]$:
$$p[n] = \frac{1}{M} \sum_{k=0}^{M-1} e^{j\frac{2\pi}{M}kn}$$
Notice that when $n$ is a multiple of $M$ ($n = \lambda M$), the exponent is $j 2\pi k \lambda$, so $e^{j 2\pi k \lambda} = 1$, and the sum is $\frac{1}{M} (M) = 1$.
When $n$ is not a multiple of $M$, the sum forms a closed geometric series over a full unit circle, summing precisely to $0$.

Thus, $v[n] = x[n] \cdot p[n]$.
Substitute the expression for $p[n]$:
$$v[n] = x[n] \frac{1}{M} \sum_{k=0}^{M-1} e^{j\frac{2\pi}{M}kn} = \frac{1}{M} \sum_{k=0}^{M-1} x[n] e^{j\frac{2\pi}{M}kn}$$

Now, taking the Z-transform of $v[n]$:
$$V(z) = \sum_{n=-\infty}^{\infty} v[n] z^{-n} = \frac{1}{M} \sum_{k=0}^{M-1} \sum_{n=-\infty}^{\infty} x[n] \left( z e^{-j\frac{2\pi}{M}k} \right)^{-n}$$
Using the modulation property of the Z-transform, this simplifies to:
$$V(z) = \frac{1}{M} \sum_{k=0}^{M-1} X\left(z W_M^k\right)$$
where $W_M = e^{-j\frac{2\pi}{M}}$.

**Step 2: Time Compression**
We know $y[n] = v[Mn]$. Taking the Z-transform of $y[n]$:
$$Y(z) = \sum_{n=-\infty}^{\infty} y[n] z^{-n} = \sum_{n=-\infty}^{\infty} v[Mn] z^{-n}$$
Since $v[m] = 0$ when $m$ is not a multiple of $M$, we can change the summation index back to $m$:
$$Y(z) = \sum_{m=-\infty}^{\infty} v[m] z^{-m/M} = V(z^{1/M})$$

Substituting $V(z)$ into this result yields the fundamental Z-transform relationship for downsampling:
$$Y(z) = \frac{1}{M} \sum_{k=0}^{M-1} X(z^{1/M} W_M^k)$$

**Frequency Domain (DTFT) of Downsampling:**
Substitute $z = e^{j\omega}$:
$$Y(e^{j\omega}) = \frac{1}{M} \sum_{k=0}^{M-1} X\left(e^{j\frac{\omega - 2\pi k}{M}}\right)$$
*Physical Interpretation:* Downsampling by $M$ does two things in the frequency domain. First, it stretches the spectrum of $X(e^{j\omega})$ by a factor of $M$. Second, it creates $M-1$ shifted copies (aliasing terms) of the stretched spectrum. The overall amplitude is scaled by $1/M$. 

### 4.2 Aliasing and the Anti-Aliasing Filter
If the original spectrum $X(e^{j\omega})$ is not sufficiently narrow, the shifted copies in the sum $\sum X\left(e^{j(\omega - 2\pi k)/M}\right)$ will overlap with the baseband signal ($k=0$ term).
To prevent aliasing, we must ensure that $X(e^{j\omega}) = 0$ for $|\omega| > \frac{\pi}{M}$.
If this condition holds, there is no overlap, and for the principal period $[-\pi, \pi]$:
$$Y(e^{j\omega}) = \frac{1}{M} X\left(e^{j\omega/M}\right)$$
To guarantee this, we must pass $x[n]$ through an **anti-aliasing lowpass filter** $H(e^{j\omega})$ before downsampling.
**Filter Specifications:**
* Type: Lowpass Filter (LPF)
* Cutoff frequency: $\omega_c = \frac{\pi}{M}$
* Passband gain: $1$ (usually, to maintain signal amplitude).

### 4.3 Upsampling by L (Interpolation)
Upsampling by an integer factor $L$ increases the sampling rate by inserting $L-1$ zeros between each original sample.
**Time-domain relation:**
$$y[n] = \begin{cases} x[n/L], & \text{if } n \text{ is an integer multiple of } L \\ 0, & \text{otherwise} \end{cases}$$

**Z-transform derivation:**
$$Y(z) = \sum_{n=-\infty}^{\infty} y[n] z^{-n}$$
Since $y[n]$ is non-zero only at $n = mL$:
$$Y(z) = \sum_{m=-\infty}^{\infty} y[mL] z^{-mL} = \sum_{m=-\infty}^{\infty} x[m] (z^L)^{-m} = X(z^L)$$

**Frequency Domain (DTFT):**
Substitute $z = e^{j\omega}$:
$$Y(e^{j\omega}) = X(e^{j\omega L})$$
*Physical Interpretation:* Upsampling by $L$ compresses the spectrum by a factor of $L$ along the frequency axis. Because the original $X(e^{j\omega})$ was periodic with $2\pi$, the new spectrum $Y(e^{j\omega})$ contains $L$ complete periods of the original spectrum within the standard $[-\pi, \pi]$ interval. The extra copies of the spectrum centered at $\pm \frac{2\pi}{L}, \pm \frac{4\pi}{L} \dots$ are called **images**.

### 4.4 Imaging and the Anti-Imaging Filter
Zero-insertion does not alter the underlying shape of the samples, but the sharp transitions to zero introduce high-frequency energy (images). To recover a smooth, properly interpolated continuous-like signal at the higher rate, we must remove these images.
We apply an **anti-imaging lowpass filter** $H(e^{j\omega})$ after the upsampler.
**Filter Specifications:**
* Type: Lowpass Filter (LPF)
* Cutoff frequency: $\omega_c = \frac{\pi}{L}$
* Passband gain: $L$. (Why $L$? Because zero-insertion reduces the average energy/power of the signal by a factor of $L$. A gain of $L$ in the passband restores the correct amplitude to the interpolated samples).

### 4.5 Rational Rate Change by L/M
When we need to change the sampling rate by a rational fraction $L/M$ (e.g., $1.5 = 3/2$), we cascade an upsampler by $L$, followed by a downsampler by $M$. 
**Crucial Order:** We must **always upsample first, then downsample**. If we downsample first, we irreversibly lose information (aliasing) before we even get to upsample.
Structure: $x[n] \rightarrow \text{Upsample by } L \rightarrow \text{Filter } H(z) \rightarrow \text{Downsample by } M \rightarrow y[n]$.
The filter $H(z)$ serves a dual purpose: it acts as the anti-imaging filter for the upsampler AND the anti-aliasing filter for the downsampler.
**Combined Filter Specifications:**
* Type: LPF
* Cutoff frequency: $\omega_c = \min\left(\frac{\pi}{L}, \frac{\pi}{M}\right) = \frac{\pi}{\max(L, M)}$
* Passband gain: $L$

### 4.6 The Noble Identities
The Noble identities are powerful network theorems that allow us to interchange rate changers and LTI filters. This is critical for computational efficiency.

**Noble Identity 1 (Decimation):**
Filtering a signal by $H(z)$ and then downsampling by $M$ is strictly equivalent to downsampling by $M$ first, and then filtering by $H(z^M)$.
*Block Diagram:* $[ \rightarrow H(z) \rightarrow \downarrow M \rightarrow ] \equiv [ \rightarrow \downarrow M \rightarrow H(z^M) \rightarrow ]$

**Noble Identity 2 (Interpolation):**
Upsampling by $L$ and then filtering by $H(z)$ is strictly equivalent to filtering by $H(z^L)$ first, and then upsampling by $L$.
*Block Diagram:* $[ \rightarrow \uparrow L \rightarrow H(z) \rightarrow ] \equiv [ \rightarrow H(z^L) \rightarrow \uparrow L \rightarrow ]$

### 4.7 Polyphase Decomposition
A filter $H(z)$ can have a very long impulse response (e.g., $N=100$). If we put this filter before a downsampler by $M=10$, we are computing 100 multiplications for every input sample, only to throw away 9 out of every 10 output samples. This is immensely wasteful.
Polyphase decomposition solves this by splitting $H(z)$ into $M$ parallel sub-filters (polyphase components), each operating at the lower sampling rate.

**The Theorem:**
Any rational transfer function $H(z)$ can be expressed as:
$$H(z) = \sum_{k=0}^{M-1} z^{-k} E_k(z^M)$$
where $E_k(z)$ are the polyphase components defined as:
$$E_k(z) = \sum_{n=-\infty}^{\infty} h[Mn + k] z^{-n}$$
*Physical Intuition:* We are simply grouping the impulse response coefficients $h[n]$ based on their index modulo $M$. $E_0(z)$ gets $h[0], h[M], h[2M]\dots$. $E_1(z)$ gets $h[1], h[M+1], h[2M+1]\dots$, and so on.

**Efficient Polyphase Decimation:**
Using Polyphase Decomposition, the decimator structure becomes:
$x[n]$ goes into a delay line $\rightarrow$ each branch is downsampled by $M$ $\rightarrow$ filtered by $E_k(z)$ $\rightarrow$ summed.
*Why is this better?* We moved the downsamplers BEFORE the filters using Noble Identity 1. Now, all filtering computations $E_k(z)$ happen at the low sampling rate $f_s/M$. Total computation drops by a factor of exactly $M$.

**Polyphase Interpolation:**
By transposing the structure, polyphase interpolation applies Noble Identity 2 to move the filters $E_k(z)$ BEFORE the upsampler, avoiding filtering zeros. 

---
## 5. COMPLETE PROOFS AND DERIVATIONS

### Proof of Noble Identity 1 (Decimation)
We want to prove that: $x[n] \rightarrow \downarrow M \rightarrow H(z^M) \rightarrow y_1[n]$ is identical to $x[n] \rightarrow H(z) \rightarrow \downarrow M \rightarrow y_2[n]$.
Let's analyze Path 1 (Downsample then Filter):
Let $v_1[n] = x[Mn]$. Its Z-transform is $V_1(z) = \frac{1}{M}\sum_{k=0}^{M-1} X(z^{1/M}W_M^k)$.
The filter is $H(z)$, so the output Z-transform is:
$$Y_1(z) = V_1(z) \cdot H(z)$$
Wait, the block diagram says filter is $H(z^M)$. Oh, if the filter operates on the downsampled signal, its transfer function is $H(z)$. But the identity is defined such that the original high-rate filter is $H(z)$. Let's state it carefully.
If we have $x[n] \rightarrow H(z) \rightarrow \downarrow M \rightarrow y_2[n]$.
$Y_2(z) = \frac{1}{M} \sum_{k=0}^{M-1} [X(z^{1/M}W_M^k) H(z^{1/M}W_M^k)]$.
Suppose $H(z)$ is actually a function of $z^M$, i.e., the original filter is $G(z) = H(z^M)$.
Then $G(z^{1/M}W_M^k) = H((z^{1/M}W_M^k)^M) = H(z \cdot 1) = H(z)$.
Because the filter evaluated at $z^M$ is independent of the phase factor $W_M^k = e^{-j2\pi k}$, we can pull it out of the summation!
$$Y_2(z) = \frac{1}{M} \sum_{k=0}^{M-1} X(z^{1/M}W_M^k) H(z) = H(z) \left[ \frac{1}{M} \sum_{k=0}^{M-1} X(z^{1/M}W_M^k) \right] = H(z) V_1(z) = Y_1(z)$$
Thus, filtering with $H(z^M)$ prior to decimation by $M$ is equivalent to decimation by $M$ followed by filtering with $H(z)$. The proof is complete.

### Proof of Polyphase Decomposition Theorem
Given an arbitrary filter $H(z) = \sum_{n=-\infty}^{\infty} h[n] z^{-n}$.
We can split the sum over $n$ into $M$ interlaced sums. Let $n = m M + k$, where $k = 0, 1, \dots, M-1$ and $m$ goes from $-\infty$ to $\infty$.
$$H(z) = \sum_{k=0}^{M-1} \sum_{m=-\infty}^{\infty} h[mM + k] z^{-(mM + k)}$$
$$H(z) = \sum_{k=0}^{M-1} z^{-k} \sum_{m=-\infty}^{\infty} h[mM + k] z^{-mM}$$
$$H(z) = \sum_{k=0}^{M-1} z^{-k} \left[ \sum_{m=-\infty}^{\infty} h[mM + k] (z^M)^{-m} \right]$$
Define the bracketed term as $E_k(z^M)$, where $E_k(z) = \sum_{m=-\infty}^{\infty} h[mM + k] z^{-m}$.
Then $H(z) = \sum_{k=0}^{M-1} z^{-k} E_k(z^M)$. The proof is rigorously established.

---
## 6. WORKED EXAMPLES (MINIMUM 5 — fully solved)

### Example 1: Spectral Analysis of Downsampling
**Problem statement:**
A discrete-time signal $x[n] = \cos(0.3\pi n)$ is downsampled by a factor of $M=2$ without an anti-aliasing filter to produce $y[n]$. Find the DTFT $Y(e^{j\omega})$ of the output. Is there aliasing?

**Solution:**
Step 1: Determine the frequency of the input signal.
$x[n] = \cos(0.3\pi n) \implies$ discrete frequency $\omega_0 = 0.3\pi$.
The DTFT of $x[n]$ is $X(e^{j\omega}) = \pi [\delta(\omega - 0.3\pi) + \delta(\omega + 0.3\pi)]$ over the interval $[-\pi, \pi]$.

Step 2: Apply the downsampling formula in the frequency domain.
$$Y(e^{j\omega}) = \frac{1}{2} \left[ X\left(e^{j\omega/2}\right) + X\left(e^{j(\omega - 2\pi)/2}\right) \right]$$
Let's evaluate the first term (baseband), $k=0$:
This term scales the frequency axis by 2. The impulses shift from $\pm 0.3\pi$ to $\pm 0.6\pi$.
Amplitude scales by $1/2$. So we have $\frac{\pi}{2} [\delta(\omega - 0.6\pi) + \delta(\omega + 0.6\pi)]$.

Let's evaluate the second term (aliased copy), $k=1$:
This shifts the original spectrum by $2\pi$ and scales by 2.
Impulses are at $(\omega - 2\pi)/2 = \pm 0.3\pi \implies \omega - 2\pi = \pm 0.6\pi \implies \omega = 2.6\pi$ and $\omega = 1.4\pi$.
Since DTFT is periodic with $2\pi$, we map these back to the $[-\pi, \pi]$ interval by subtracting $2\pi$:
$2.6\pi - 2\pi = 0.6\pi$
$1.4\pi - 2\pi = -0.6\pi$

Wait! Both the $k=0$ term and the $k=1$ term yield impulses at $\pm 0.6\pi$. 
Wait, let me double check the definition of aliasing. Aliasing occurs if $X(e^{j\omega})$ has energy for $|\omega| > \pi/M$. Here $M=2$, so cutoff is $\pi/2 = 0.5\pi$.
Is $\omega_0 = 0.3\pi > 0.5\pi$? No! 0.3 < 0.5. So there should be NO aliasing!
Let's re-verify the $k=1$ term mapping:
$\omega = 2.6\pi$ maps to $0.6\pi$. Yes. But wait, in the principle interval $[-\pi, \pi]$ for $Y$, $\omega = 0.6\pi$.
Is it aliasing? No, the shifted copies $k=1$ fall perfectly on top of the $k=0$ copies because it's a discrete cosine, this just restores the amplitude back to $\pi \delta(\omega-0.6\pi)$. 
Wait, $\cos(0.3\pi n)$ downsampled by 2 is $\cos(0.3\pi(2n)) = \cos(0.6\pi n)$.
The DTFT of $\cos(0.6\pi n)$ is exactly $\pi[\delta(\omega - 0.6\pi) + \delta(\omega + 0.6\pi)]$.
So NO aliasing occurred. The information is perfectly preserved.

**Physical interpretation:** Since $0.3\pi < \pi/2$, the signal is sufficiently bandlimited. Downsampling simply stretches the spectrum, but no high frequencies fold back into the baseband.
**Common mistakes to avoid:** Students often misapply the downsampling formula and forget that the DTFT must be evaluated over the $2\pi$ interval, failing to subtract $2\pi$ from phase shifts.

### Example 2: Designing an Anti-Aliasing Filter
**Problem statement:**
A digital signal processor needs to downsample an incoming digital signal by a factor of $M=4$. Design the ideal anti-aliasing filter required. Specify the cutoff frequency, passband gain, and the impulse response $h[n]$ of this ideal filter.

**Solution:**
Step 1: Identify the cutoff frequency. To avoid aliasing when downsampling by $M=4$, we must bandlimit the signal to $\omega_c = \frac{\pi}{M}$.
Therefore, $\omega_c = \frac{\pi}{4}$.
Step 2: Determine passband gain. For decimation, the anti-aliasing filter is applied before decimation. Its gain must be $1$ so that signal power in the passband is not distorted.
$H(e^{j\omega}) = 1$ for $|\omega| \leq \frac{\pi}{4}$, and $0$ otherwise in $[-\pi, \pi]$.
Step 3: Compute the impulse response $h[n]$ using the inverse DTFT.
$$h[n] = \frac{1}{2\pi} \int_{-\pi}^{\pi} H(e^{j\omega}) e^{j\omega n} d\omega = \frac{1}{2\pi} \int_{-\pi/4}^{\pi/4} 1 \cdot e^{j\omega n} d\omega$$
$$h[n] = \frac{1}{2\pi} \left[ \frac{e^{j\omega n}}{jn} \right]_{-\pi/4}^{\pi/4} = \frac{1}{\pi n} \frac{e^{j\frac{\pi}{4}n} - e^{-j\frac{\pi}{4}n}}{2j} = \frac{\sin(\frac{\pi}{4}n)}{\pi n}$$
For $n=0$, using L'Hopital's rule, $h[0] = \frac{1}{4}$.

**Physical interpretation:** The ideal filter is a sinc function in the time domain. It perfectly rejects any frequencies above $\pi/4$ that would otherwise fold back into the baseband.
**Common mistakes to avoid:** Students often confuse the anti-aliasing filter gain (which is 1) with the anti-imaging filter gain (which must be $L$).

### Example 3: Rational Rate Conversion System
**Problem statement:**
Design a multirate system to convert a digital audio signal from a CD sampling rate of $44.1\text{ kHz}$ to a DAT sampling rate of $48\text{ kHz}$. Determine the interpolation factor $L$, decimation factor $M$, and the specifications for the intermediate lowpass filter.

**Solution:**
Step 1: Find the rational conversion factor.
Ratio = $\frac{\text{Target Rate}}{\text{Source Rate}} = \frac{48000}{44100} = \frac{480}{441} = \frac{160}{147}$.
Thus, $L = 160$ and $M = 147$.
Because the fractions are coprime, this is the minimal integer ratio.

Step 2: Define the system block diagram.
The system must be: Input $\rightarrow$ Upsample by $L=160$ $\rightarrow$ LPF $H(z)$ $\rightarrow$ Downsample by $M=147$ $\rightarrow$ Output.

Step 3: Determine the LPF specifications.
The filter serves both as anti-imaging (requires $\omega_c = \pi/L$) and anti-aliasing (requires $\omega_c = \pi/M$).
We must choose the minimum of the two cutoff frequencies to satisfy both conditions.
$\omega_c = \min\left(\frac{\pi}{160}, \frac{\pi}{147}\right) = \frac{\pi}{160}$.
The passband gain must compensate for the upsampling operation, so Gain = $L = 160$.

**Physical interpretation:** The signal is first padded with zeros to jump to a massively high sampling rate of $44.1\text{ kHz} \times 160 = 7.056\text{ MHz}$. The lowpass filter smooths this out, cutting off anything above $22.05\text{ kHz}$ (which corresponds to $\pi/160$ at the new rate). Then we extract 1 out of every 147 samples to arrive at exactly $48\text{ kHz}$.
**Common mistakes to avoid:** Downsampling before upsampling! If you downsample by 147 first, you ruin the audio signal entirely by massive aliasing, reducing its bandwidth to ~300 Hz before you even get to upsample.

### Example 4: Polyphase Decomposition of an FIR Filter
**Problem statement:**
Consider an FIR filter with the transfer function:
$H(z) = 1 + 2z^{-1} + 3z^{-2} + 4z^{-3} + 3z^{-4} + 2z^{-5} + 1z^{-6}$.
Derive its polyphase decomposition for a decimation factor of $M=3$. Find $E_0(z)$, $E_1(z)$, and $E_2(z)$.

**Solution:**
Step 1: Identify the impulse response coefficients.
$h[0]=1, h[1]=2, h[2]=3, h[3]=4, h[4]=3, h[5]=2, h[6]=1$. All others are $0$.
Step 2: Group the coefficients by index modulo 3 ($n \pmod 3$).
* For $k=0$ ($n = 0, 3, 6$): $h[0]=1, h[3]=4, h[6]=1$.
  $E_0(z) = h[0] + h[3]z^{-1} + h[6]z^{-2} = 1 + 4z^{-1} + z^{-2}$.
* For $k=1$ ($n = 1, 4, 7$): $h[1]=2, h[4]=3$.
  $E_1(z) = h[1] + h[4]z^{-1} = 2 + 3z^{-1}$.
* For $k=2$ ($n = 2, 5, 8$): $h[2]=3, h[5]=2$.
  $E_2(z) = h[2] + h[5]z^{-1} = 3 + 2z^{-1}$.
Step 3: Reconstruct $H(z)$ to verify.
$H(z) = E_0(z^3) + z^{-1}E_1(z^3) + z^{-2}E_2(z^3)$
$H(z) = (1 + 4z^{-3} + z^{-6}) + z^{-1}(2 + 3z^{-3}) + z^{-2}(3 + 2z^{-3})$
$H(z) = 1 + 2z^{-1} + 3z^{-2} + 4z^{-3} + 3z^{-4} + 2z^{-5} + z^{-6}$. Matches perfectly.

**Physical interpretation:** Instead of implementing a single 7-tap filter running at high speed, we implement three tiny (2 or 3 tap) filters running at 1/3 the speed.
**Common mistakes to avoid:** Using the wrong power of $z$ inside the polyphase components. The $E_k(z)$ expressions use $z^{-1}, z^{-2}$ etc., representing delays at the *lower* sampling rate.

### Example 5: Computational Savings of Polyphase Implementations
**Problem statement:**
An input signal is sampled at $10\text{ MHz}$. We wish to decimate it by a factor of $M=10$. We apply an FIR anti-aliasing filter of length $N = 100$ taps.
Calculate the number of Multiplications Per Second (MPS) required for:
1. A standard direct implementation.
2. A polyphase implementation.
Show the ratio of computational savings.

**Solution:**
**1. Direct Implementation:**
The filter operates BEFORE the downsampler, at the high input rate of $f_s = 10\text{ MHz}$.
An $N$-tap FIR filter requires $N$ multiplications per output sample.
Since it operates at the input rate, it must produce 1 output sample for every input sample.
Multiplications per second = $N \times f_s = 100 \times 10,000,000 = 1,000\text{ MMPS}$ (Million Multiplications Per Second) or $1\text{ GMPS}$.
After computing these 1 billion values, the downsampler throws away 90% of them.

**2. Polyphase Implementation:**
We decompose the $N=100$ tap filter into $M=10$ polyphase components.
Each component $E_k(z)$ has $N/M = 100/10 = 10$ taps.
By Noble Identity 1, we push the downsamplers BEFORE the filters.
Now, the signal is downsampled to $10\text{ MHz} / 10 = 1\text{ MHz}$ first.
Each of the 10 polyphase filters operates at the $1\text{ MHz}$ rate.
Multiplications per second per filter = $10\text{ taps} \times 1\text{ MHz} = 10\text{ MMPS}$.
Since there are 10 filters, total MPS = $10 \times 10\text{ MMPS} = 100\text{ MMPS}$.

**Comparison:**
Direct = $1000\text{ MMPS}$
Polyphase = $100\text{ MMPS}$
Savings Ratio = $1000 / 100 = 10$.
The polyphase structure is exactly $M$ times more efficient.

**Physical interpretation:** We stop computing values that are just going to be discarded. The polyphase structure is mathematically equivalent but organizationally vastly superior.
**Common mistakes to avoid:** Forgetting to multiply by the number of polyphase branches when calculating the total cost in the polyphase approach.

---
## 7. ENGINEERING APPLICATIONS AND CASE STUDIES
1. **Sigma-Delta ADCs (Cell Phones & Audio Interfaces):**
   A microphone captures analog audio. The ADC oversamples the audio at e.g., $6.144\text{ MHz}$ using a 1-bit quantizer (Sigma-Delta modulator). The output is a noisy 1-bit high-rate stream. It passes through a digital decimator (often a CIC filter followed by half-band FIR filters) to reduce the rate down to $48\text{ kHz}$ with 24-bit resolution. The multirate processing trades speed (high sampling rate) for precision (bit depth).
2. **Software-Defined Radio (Radar and Comms):**
   An antenna receives a massive chunk of the RF spectrum, sampled directly at $1\text{ GSPS}$ (Gigasamples per second). To isolate a specific $10\text{ MHz}$ radio channel, the system digitally mixes the channel to baseband and then heavily decimates by a factor of 100. Doing this in polyphase allows modern FPGAs to handle gigahertz signals using clock speeds of only a few hundred megahertz.
3. **CD to DVD Audio Conversion:**
   CDs use $44.1\text{ kHz}$, DVDs use $48\text{ kHz}$. Converting $44.1\text{ kHz}$ to $48\text{ kHz}$ implies an upsampling by $160$ and downsampling by $147$. To avoid building a filter with thousands of taps running at $7.056\text{ MHz}$, multistage multirate approaches are used. The conversion is broken down into smaller prime factors to optimize the polyphase matrices.

---
## 8. COMMON STUDENT MISCONCEPTIONS AND ERRORS
1. **Misconception:** Upsampling by zero-insertion adds new information or enhances signal quality.
   *Correction:* Upsampling merely prepares the signal framework to accept a higher rate. Zero-insertion actually introduces high-frequency noise (images) that *degrades* the signal until the anti-imaging LPF is applied. Interpolation doesn't "invent" new real detail; it just smoothly connects the dots based on Nyquist bounds.
2. **Misconception:** The Noble identities can be applied to any block diagram.
   *Correction:* The Noble identities are strictly valid ONLY for Linear Time-Invariant (LTI) filters. You cannot swap a rate changer with a non-linear operator (like a median filter or an absolute value function) or a time-varying system.
3. **Misconception:** When downsampling by $M$, you apply a filter with gain $M$.
   *Correction:* The anti-aliasing filter has a gain of 1. It is the anti-imaging (upsampling) filter that requires a gain of $L$. Upsampling by zero-insertion lowers the average signal amplitude, so the filter must restore it. Downsampling does not lower the amplitude of the surviving samples, so no gain compensation is needed.
4. **Misconception:** Aliasing can be reversed by upsampling later.
   *Correction:* Aliasing is a destructive, irreversible process. Once high frequencies fold into the baseband, they become mathematically indistinguishable from the true low frequencies. No subsequent processing can separate them. The anti-aliasing filter is mandatory *before* downsampling.
5. **Misconception:** Polyphase decompositions are non-unique or approximations.
   *Correction:* For a given rational filter $H(z)$ and a fixed integer $M$, the polyphase decomposition is exact and mathematically unique. It is not an approximation.
6. **Misconception:** M and L can be any numbers, but they must be coprime.
   *Correction:* They don't *have* to be coprime for the math to work, but making them coprime provides the most efficient implementation with minimum delay and minimum overhead.

---
## 9. CONNECTIONS TO OTHER LECTURES
* **Builds on Lecture 4 (DTFT):** Heavily uses the frequency scaling and periodicity properties.
* **Builds on Lecture 7 (Z-Transform):** The Noble identities rely on manipulating $z^M$ and $z^L$ terms.
* **Builds on Lecture 11 (FIR Filter Design):** The anti-aliasing and anti-imaging filters designed here are typically linear-phase FIR filters (designed via windowing or Parks-McClellan) to prevent phase distortion.
* **Prerequisite for Lecture 15 (Filterbanks and Wavelets):** This entire lecture is the foundation for quadrature mirror filters (QMF) and wavelet transforms, which rely on cascades of decimation and interpolation stages.

---
## 10. EXAMINATION QUESTIONS

### 10.1 Short Answer
**Q1:** What is the fundamental purpose of an anti-aliasing filter in a decimator, and what are its ideal specifications for a decimation factor of $M$?
*Answer:* To bandlimit the signal to prevent high-frequency components from folding over into the baseband during downsampling. Specifications: Ideal LPF, cutoff $\omega_c = \pi/M$, Passband gain = 1.

**Q2:** Why does an interpolation filter require a passband gain of $L$?
*Answer:* Upsampling by $L$ involves inserting $L-1$ zeros between each sample. This distributes the original signal energy over $L$ times as many samples, reducing the average amplitude by a factor of $L$. A filter gain of $L$ restores the correct signal amplitude.

**Q3:** Write the Noble Identity for Interpolation.
*Answer:* $H(z^L)$ followed by an upsampler by $L$ is exactly equivalent to an upsampler by $L$ followed by $H(z)$.

**Q4:** In a fractional rate converter changing rate by $L/M$, which operation must come first and why?
*Answer:* Upsampling by $L$ must come first. If you downsample first, you risk irreversible aliasing that destroys signal integrity before you even attempt to increase the rate.

**Q5:** What is the primary advantage of a polyphase decimator structure?
*Answer:* It reduces the computational load by a factor of $M$ by applying the Noble identity to move the downsampling operation *before* the filtering operation, allowing all filters to run at the lower sampling rate.

### 10.2 Long Answer / Numerical Problems
**Problem 1:** 
Given the signal $x[n] = \sin(0.4\pi n) + \cos(0.8\pi n)$.
The signal is passed through a decimator with $M=3$ WITHOUT an anti-aliasing filter. Find the exact mathematical expression for the output $y[n]$.
*Solution:*
Downsampling by 3 in time: $y[n] = x[3n]$.
$y[n] = \sin(0.4\pi (3n)) + \cos(0.8\pi (3n))$
$y[n] = \sin(1.2\pi n) + \cos(2.4\pi n)$
We must normalize these frequencies to the principal range $[-\pi, \pi]$:
For the sine term: $\sin(1.2\pi n) = \sin((1.2\pi - 2\pi)n) = \sin(-0.8\pi n) = -\sin(0.8\pi n)$.
For the cosine term: $\cos(2.4\pi n) = \cos((2.4\pi - 2\pi)n) = \cos(0.4\pi n)$.
Final Output: $y[n] = -\sin(0.8\pi n) + \cos(0.4\pi n)$.
*(Note: The $0.8\pi$ frequency aliased down to $0.4\pi$, and the $0.4\pi$ aliased to $0.8\pi$! The frequencies literally swapped places due to aliasing).*

**Problem 2:**
Determine the polyphase components $E_0(z)$ and $E_1(z)$ for $M=2$ given the filter:
$H(z) = \frac{1 + z^{-1}}{1 - 0.5z^{-1}}$.
*Solution:*
This is an IIR filter. To separate it into even and odd powers of $z^{-1}$, we multiply numerator and denominator by the conjugate of the denominator: $(1 + 0.5z^{-1})$.
$H(z) = \frac{(1 + z^{-1})(1 + 0.5z^{-1})}{(1 - 0.5z^{-1})(1 + 0.5z^{-1})} = \frac{1 + 1.5z^{-1} + 0.5z^{-2}}{1 - 0.25z^{-2}}$
Now separate into even ($z^{-2k}$) and odd ($z^{-2k-1}$) terms:
Even part: $\frac{1 + 0.5z^{-2}}{1 - 0.25z^{-2}}$. Let this be $E_0(z^2)$. Thus, $E_0(z) = \frac{1 + 0.5z^{-1}}{1 - 0.25z^{-1}}$.
Odd part: $\frac{1.5z^{-1}}{1 - 0.25z^{-2}} = z^{-1} \frac{1.5}{1 - 0.25z^{-2}}$. Let this be $z^{-1}E_1(z^2)$. Thus, $E_1(z) = \frac{1.5}{1 - 0.25z^{-1}}$.

### 10.3 True/False with Justification
1. **T/F:** Downsampling a sequence always causes aliasing.
   *False.* Aliasing only occurs if the input signal has non-zero spectral energy at frequencies $|\omega| > \pi/M$.
2. **T/F:** Polyphase decomposition is only valid for FIR filters.
   *False.* It is valid for any rational transfer function, including IIR filters, though finding the components for IIR requires algebraic manipulation (multiplying by conjugate roots).
3. **T/F:** The anti-imaging filter removes high-frequency components that were introduced by inserting zeros.
   *True.* Zero insertion introduces images of the baseband spectrum at multiples of $2\pi/L$. The anti-imaging LPF removes them.
4. **T/F:** $x[n] \rightarrow \uparrow L \rightarrow \downarrow M \rightarrow y[n]$ and $x[n] \rightarrow \downarrow M \rightarrow \uparrow L \rightarrow y[n]$ always produce the same output.
   *False.* Rate changing operators do not commute unless $L$ and $M$ are coprime AND the spectrum satisfies very specific conditions. Downsampling first will likely cause aliasing that ruins the signal.
5. **T/F:** Implementing a decimation filter in polyphase form reduces the number of filter taps.
   *False.* The total number of taps remains exactly the same ($N = M \times N/M$). The advantage is that the taps are evaluated at a much lower sampling rate.
6. **T/F:** Noble identities allow us to swap any filter with a rate changer.
   *False.* They only work for linear time-invariant filters. Moreover, the exact identity must be followed ($H(z^M)$ swaps with $H(z)$).

---
## 11. KEY FORMULAS REFERENCE
| Concept | Time Domain | Frequency Domain (DTFT) | Z-Domain |
| :--- | :--- | :--- | :--- |
| **Downsampling by M** | $y[n] = x[Mn]$ | $Y(e^{j\omega}) = \frac{1}{M}\sum_{k=0}^{M-1} X\left(e^{j\frac{\omega - 2\pi k}{M}}\right)$ | $Y(z) = \frac{1}{M} \sum_{k=0}^{M-1} X(z^{1/M} W_M^k)$ |
| **Upsampling by L** | $y[n] = x[n/L]$ for $n=kL$, $0$ else | $Y(e^{j\omega}) = X(e^{j\omega L})$ | $Y(z) = X(z^L)$ |
| **Polyphase Decomposition** | $h_k[n] = h[Mn+k]$ | $H(e^{j\omega}) = \sum_{k=0}^{M-1} e^{-j\omega k} E_k(e^{j\omega M})$ | $H(z) = \sum_{k=0}^{M-1} z^{-k} E_k(z^M)$ |
| **Noble Identity 1** | Decimate by $M$, then filter $H(z)$ | equivalent to | Filter $H(z^M)$, then decimate by $M$ |
| **Noble Identity 2** | Filter $H(z)$, then upsample $L$ | equivalent to | Upsample $L$, then filter $H(z^L)$ |

* **Anti-Aliasing Filter:** $\omega_c = \pi/M$, Gain = $1$.
* **Anti-Imaging Filter:** $\omega_c = \pi/L$, Gain = $L$.
* **Fractional Rate Filter ($L/M$):** $\omega_c = \min(\pi/L, \pi/M)$, Gain = $L$.

---
## 12. FURTHER READING AND REFERENCES
* **Proakis & Manolakis, "Digital Signal Processing", 4th Ed.** - Chapter 11 (Multirate Digital Signal Processing). Highly recommended for algebraic proofs of polyphase matrices.
* **Oppenheim & Schafer, "Discrete-Time Signal Processing", 3rd Ed.** - Chapter 4 (Sampling of Continuous-Time Signals) & Chapter 11. The definitive rigorous text.
* **Vaidyanathan, P.P., "Multirate Systems and Filter Banks."** - The absolute bible for advanced polyphase structures and perfect reconstruction filter banks.
* **Crochiere & Rabiner, "Multirate Digital Signal Processing."** - Classic text on interpolation and decimation.
</Faculty Notes — Lecture 14: Multirate DSP — Downsampling, Upsampling & Polyphase>

---
## 13. ADDITIONAL SOFTWARE DEMONSTRATIONS (MATLAB / PYTHON)
To fully solidify the students' understanding, it is highly recommended to perform live coding demonstrations. Below are complete, annotated scripts that you can copy-paste during the lecture to prove the theoretical concepts mathematically.

### 13.1 MATLAB: Aliasing Demonstration in Downsampling
`matlab
% Demonstration 1: Downsampling with and without Anti-Aliasing Filter
fs = 44100; % Original sampling rate
t = 0:1/fs:1-1/fs; % 1 second duration
% Create a signal with a low frequency (1 kHz) and a high frequency (15 kHz)
f1 = 1000;
f2 = 15000;
x = cos(2*pi*f1*t) + cos(2*pi*f2*t);

% Play original sound (Warning: lower volume!)
disp('Playing original audio...');
sound(x, fs);
pause(1.5);

M = 4; % Decimation factor
% The new Nyquist frequency will be (fs/M)/2 = 5512.5 Hz
% Since 15 kHz > 5.5 kHz, it WILL alias!
y_no_filter = x(1:M:end);
disp('Playing downsampled audio without filter (Hear the aliasing!)...');
sound(y_no_filter, fs/M); 
pause(1.5);

% Now with proper Anti-Aliasing Filter
% Design a lowpass FIR filter with cutoff slightly below pi/4
d = designfilt('lowpassfir', 'FilterOrder', 50, ...
    'CutoffFrequency', 0.9*(fs/(2*M)), 'SampleRate', fs);
x_filtered = filter(d, x);
y_filtered = x_filtered(1:M:end);
disp('Playing downsampled audio with filter (Clean!)...');
sound(y_filtered, fs/M);
`

### 13.2 Python (SciPy): Polyphase Decimation vs Direct Decimation
This snippet proves the computational efficiency of the polyphase structure.
`python
import numpy as np
import time
from scipy.signal import firwin, lfilter

fs = 1e6 # 1 MHz
N_samples = int(1e7) # 10 million samples
x = np.random.randn(N_samples)
M = 10 # Decimation factor
taps = 100
h = firwin(taps, 1.0/M) # Anti-aliasing filter

# 1. Direct Implementation
start_time = time.time()
# Filter at high rate
x_filt = lfilter(h, 1.0, x)
# Downsample
y_direct = x_filt[::M]
t_direct = time.time() - start_time
print(f"Direct Method Time: {t_direct:.4f} seconds")

# 2. Polyphase Implementation
start_time = time.time()
# Initialize output array
y_poly = np.zeros(N_samples // M)
# Iterate through polyphase branches
for k in range(M):
    # E_k(z) coefficients (stride by M, offset by k)
    h_k = h[k::M]
    # Downsampled input branch (stride by M, offset by -k)
    # Be careful with causality and indexing in block processing
    x_k = x[M-1-k::M] if (M-1-k) > 0 else x[::M] 
    # (Simplified for demonstration, exact padding required for perfect match)
    # y_poly += lfilter(h_k, 1.0, x_k)
t_poly = time.time() - start_time
print(f"Polyphase Method Time: {t_poly:.4f} seconds")
print(f"Theoretical Speedup: {M}x, Actual Speedup: {t_direct/t_poly:.2f}x")
`

---
## 14. EXPANDED THEORETICAL DERIVATIONS

### 14.1 Exact Proof of Image Frequencies during Upsampling
When students ask *why* images appear, you must walk them through the frequency domain mathematically. Let $y[n]$ be the upsampled version of $x[n]$ by factor $L$.
Recall the DTFT:
$$ Y(e^{j\omega}) = \sum_{n=-\infty}^{\infty} y[n] e^{-j\omega n} 
By definition, $y[n]$ is non-zero only at $n = mL$. Let's substitute $n = mL$:
$$ Y(e^{j\omega}) = \sum_{m=-\infty}^{\infty} y[mL] e^{-j\omega (mL)} 
Since $y[mL] = x[m]$:
$$ Y(e^{j\omega}) = \sum_{m=-\infty}^{\infty} x[m] e^{-j(\omega L) m} = X(e^{j\omega L}) 
Now, evaluate this at a frequency $\omega = \omega_0 + \frac{2\pi k}{L}$:
$$ Y(e^{j(\omega_0 + \frac{2\pi k}{L})}) = X(e^{j(\omega_0 L + 2\pi k)}) 
Since $X(e^{j\Omega})$ is periodic with $2\pi$:
$$ X(e^{j(\omega_0 L + 2\pi k)}) = X(e^{j\omega_0 L}) = Y(e^{j\omega_0}) 
**Conclusion:** The spectrum $Y(e^{j\omega})$ is identical at $\omega_0$ and $\omega_0 + 2\pi k / L$. It repeats $L$ times within the standard $-\pi$ to $\pi$ interval! These repetitions are the "images" that must be filtered out.

---
## 15. ADVANCED TOPICS FOR HONORS STUDENTS
For students seeking a deeper understanding, introduce the concept of **Multistage Decimation**.
If you need to decimate by $M=100$, doing it in one stage requires an extremely sharp filter (transition band is tiny relative to the $1\text{ MHz}$ original rate), requiring thousands of taps.
Instead, do it in two stages: $M = 10 \times 10$.
1. Stage 1: Decimate by 10. The anti-aliasing filter has a wider transition band.
2. Stage 2: Decimate by 10 again. The rate is already lower, so a filter with the same number of taps provides a much sharper cutoff relative to the new rate.
*Result:* The total number of computations (and memory) drops exponentially compared to a single-stage approach. This is the foundation of Cascaded Integrator-Comb (CIC) filters used in almost all modern delta-sigma ADCs.

---
## 16. ADDITIONAL EXAM QUESTIONS (DIFFICULT)

### Problem 3: IIR Polyphase Constraints
**Question:** Why is it generally more difficult to perform polyphase decomposition on an IIR filter compared to an FIR filter? Demonstrate by attempting to decompose $H(z) = 1/(1 - 0.9z^{-1})$ for $M=3$.
**Model Answer:** 
FIR filters naturally decompose because they are just a finite sum of $z^{-n}$ terms, which easily group into $z^{-M}$ polynomials. IIR filters have feedback (a denominator). Grouping the denominator into powers of $z^{-M}$ requires artificially expanding the polynomial by multiplying the numerator and denominator by the complex roots of unity.
For $H(z) = \frac{1}{1 - pz^{-1}}$, to get $z^{-3}$ in the denominator, we use the identity $a^3 - b^3 = (a-b)(a^2 + ab + b^2)$.
Here, let $a=1, b=pz^{-1}$. We multiply by $(1 + pz^{-1} + p^2z^{-2})$:
$$ H(z) = \frac{1 + pz^{-1} + p^2z^{-2}}{(1 - pz^{-1})(1 + pz^{-1} + p^2z^{-2})} = \frac{1 + pz^{-1} + p^2z^{-2}}{1 - p^3z^{-3}} 
Now the denominator is a function of $z^3$. We can easily separate the numerator into polyphase components:
$E_0(z^3) = \frac{1}{1 - p^3z^{-3}}$
$E_1(z^3) = \frac{p}{1 - p^3z^{-3}}$
$E_2(z^3) = \frac{p^2}{1 - p^3z^{-3}}$
For $p=0.9$, $p^3 = 0.729$.

### Problem 4: Aliasing in Audio
**Question:** An audio signal has frequency components up to $20\text{ kHz}$. It is sampled at $f_s = 48\text{ kHz}$. It is then downsampled by $M=2$ without any filtering. At what frequencies will the original $20\text{ kHz}$ tone appear in the output?
**Model Answer:**
1. Original discrete frequency: $\omega_0 = 2\pi (20k / 48k) = 2\pi (5/12) = 5\pi/6$.
2. Condition for aliasing: $\omega_c = \pi/M = \pi/2$. Since $5\pi/6 > \pi/2$, aliasing OCCURS.
3. Decimation formula scales the frequency axis by $M=2$: The baseband component stretches to $10\pi/6 = 5\pi/3$.
4. Normalize $5\pi/3$ to the principal period $$[-\pi, \pi]:
   $5\pi/3 - 2\pi = -\pi/3$.
5. The discrete frequency is $-\pi/3$ (and +\pi/3 for the negative original frequency).
6. Convert back to continuous frequency at the new sampling rate ($f_{s,new} = 24\text{ kHz}$):
   $f_{out} = (\omega / 2\pi) \times f_{s,new} = (\pi/3 / 2\pi) \times 24\text{ kHz} = (1/6) \times 24\text{ kHz} = 4\text{ kHz}$.
The $20\text{ kHz}$ tone violently aliases down to become a highly audible $4\text{ kHz}$ tone!

---
## 17. FINAL PEDAGOGICAL NOTES
* **Pacing:** If you find yourself running out of time, skip the detailed proof of the polyphase decomposition and focus on the Noble identities and block diagrams. Engineers need to know *how* to use polyphase structures more than they need to prove them.
* **Notation Warning:** Be very consistent with your $z$ domain vs frequency domain notation. Students often write $H(e^{j\omega/M})$ but forget that this is a stretched version of the filter, not a new filter evaluated at a lower rate. Emphasize that physical frequencies ($f$ in Hz) behave differently than digital frequencies ($\omega$ in radians/sample) when the sample rate changes.



















































