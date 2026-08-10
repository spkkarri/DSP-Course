</Agent System Instructions>
<Faculty Notes — Lecture 22: Sampling Theorem & A/D D/A Conversion>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY
This lecture represents the essential bridge between the continuous-time world (analog signals) and the discrete-time world (digital signals). The concepts taught here form the absolute bedrock of modern digital signal processing. Students frequently struggle with the frequency-domain interpretation of sampling—specifically, the concept of periodic spectrum repetition and the physical reality of aliasing. 

### How to teach this lecture:
- **Pacing:** Do not rush the Poisson Sum Formula. It is the mathematical heart of the lecture. 
- **Visuals:** Draw the spectra on the board multiple times. Show the baseband spectrum $X(f)$, and then physically draw the shifted copies at $f_s, 2f_s, -f_s$, etc. 
- **Engagement:** Ask students what happens when the shifted copies start moving closer together (as $f_s$ decreases). This naturally leads them to discover aliasing on their own before you define it mathematically.

### Common student difficulties:
- Students often mix up time-domain and frequency-domain representations. Emphasize that sampling in time (multiplication by impulses) equals convolution in frequency (replication of spectra).
- The transition from an ideal DAC (producing impulses) to a practical DAC (producing Zero-Order Hold steps) is a conceptual hurdle. They may not understand why a "flat step" in time alters the frequency content.
- The concept of quantization noise being modeled as an additive white noise source is non-intuitive because quantization is actually a deterministic, non-linear operation.

### Prerequisite checks:
Ensure students are comfortable with the following before starting the core material:
- The Continuous-Time Fourier Transform (CTFT) and its inverse.
- Convolution properties (both time and frequency domain).
- The Dirac delta function $\delta(t)$ and its sifting property.
- The concept of power spectral density (PSD) and variance for noise calculations.

### Suggested demos:
1. **Stroboscope Demo:** Show a video of a helicopter where the camera frame rate perfectly matches the rotor RPM, making the blades appear completely stationary. Explain how this is extreme aliasing.
2. **Audio Demo:** Play a high-quality audio file. Then, use software to downsample it without an anti-aliasing filter to let them explicitly hear the harsh, non-harmonic aliasing artifacts folding back into the audio band. 
3. **ZOH Demo:** Show a high-frequency sine wave reconstructed with a low sample rate ZOH DAC to visually demonstrate the staircase effect and the resulting loss of amplitude (droop).

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Derive** the spectrum of an ideally sampled continuous-time signal from first principles using the Poisson sum formula.
2. **State and prove** the Nyquist-Shannon sampling theorem rigorously, detailing both the sampling and exact reconstruction phases.
3. **Analyze** the aliasing phenomenon mathematically, calculate exact folded frequencies given a signal and sampling rate, and construct frequency folding diagrams.
4. **Design** practical Analog-to-Digital Converter (ADC) pipelines, including calculating exact specifications for the anti-aliasing analog filter to achieve a desired stopband attenuation.
5. **Evaluate** the effect of Zero-Order Hold (ZOH) on signal reconstruction mathematically, formulate the exact droop compensation needed, and explain the aperture effect.
6. **Calculate** critical ADC metrics including dynamic range, Signal-to-Quantization-Noise Ratio (SQNR), and Equivalent Number of Bits (ENOB) given specific hardware parameters.
7. **Explain** the principles of oversampling and first-order noise shaping in Sigma-Delta ADCs, and quantify the resulting SNR improvements mathematically.

---
## 2. PREREQUISITE KNOWLEDGE REVIEW
Before proceeding into the new material, students must firmly recall the following foundational concepts and mathematical tools:

### 2.1 The Continuous-Time Fourier Transform (CTFT)
The CTFT translates a continuous-time signal into its continuous-frequency spectrum.
- **Definition:** $X(f) = \int_{-\infty}^{\infty} x(t) e^{-j2\pi ft} dt$
- **Inverse CTFT:** $x(t) = \int_{-\infty}^{\infty} X(f) e^{j2\pi ft} df$
We use $f$ in Hertz rather than $\omega$ in rad/s to make the sampling frequency $f_s$ more intuitive, though $\omega = 2\pi f$ is equally valid.

### 2.2 The Dirac Delta Function
The delta function $\delta(t)$ is an generalized function (distribution) that is zero everywhere except at $t=0$, where it is infinite, such that its integral over all time is 1.
- **Sifting property:** $\int_{-\infty}^{\infty} x(t) \delta(t - t_0) dt = x(t_0)$
- **Multiplication property:** $x(t) \cdot \delta(t - t_0) = x(t_0) \delta(t - t_0)$
- **Convolution property:** $x(t) * \delta(t - t_0) = x(t - t_0)$

### 2.3 The Convolution Theorem
The most critical theorem for understanding sampling. Multiplication in one domain corresponds to convolution in the other domain.
- **Time Multiplication:** If $y(t) = x(t) \cdot p(t)$, then $Y(f) = X(f) * P(f)$
- **Time Convolution:** If $y(t) = x(t) * h(t)$, then $Y(f) = X(f) \cdot H(f)$

### 2.4 Fourier Transform of an Impulse Train
An infinite sequence of impulses (a Dirac comb) in time transforms into an infinite sequence of impulses in frequency.
Let $p(t) = \sum_{n=-\infty}^{\infty} \delta(t - nT)$. 
The CTFT of $p(t)$ is $P(f) = \frac{1}{T} \sum_{k=-\infty}^{\infty} \delta\left(f - \frac{k}{T}\right)$.
Letting $f_s = 1/T$, we have $P(f) = f_s \sum_{k=-\infty}^{\infty} \delta(f - kf_s)$.

---
## 3. HISTORICAL AND MOTIVATIONAL CONTEXT

### Who discovered this?
While universally known in engineering as the Nyquist-Shannon sampling theorem, the history of this mathematical truth is rich and multi-national.
- **Harry Nyquist (1928):** While working at Bell Labs, Nyquist published "Certain Topics in Telegraph Transmission Theory," detailing that 2W independent pulses could be transmitted per second over a channel of bandwidth W.
- **Vladimir Kotelnikov (1933):** A Soviet engineer who independently proved the theorem in the context of radio transmission, making it known in Russian literature as Kotelnikov's theorem.
- **E.T. Whittaker (1915):** A British mathematician who published the mathematical interpolation formula utilizing the sinc function long before it was applied to communications.
- **Claude Shannon (1949):** Formalized the theorem explicitly for information theory in "Communication in the Presence of Noise," cementing the absolute link between continuous and discrete representations.

### Real Engineering Applications (Why does EEE need this?)
In modern Electrical and Electronics Engineering, almost all signal processing, control, and communication algorithms are executed digitally on microprocessors, DSP chips, or FPGAs. However, the physical universe remains steadfastly analog.
- **Telecommunications:** 5G and LTE base stations receive continuous RF waveforms from the antenna. These must be sampled exactly at specific rates (often hundreds of MSPS) without aliasing adjacent frequency bands.
- **Biomedical Engineering:** EEG (brain) and ECG (heart) signals are microvolt-level analog potentials. An engineer designing a patient monitor must understand sampling to prevent 60 Hz powerline interference from aliasing into the critical biological frequency bands (0.1 Hz to 40 Hz).
- **Audio Engineering:** The entire digital music industry relies on the sampling theorem. The choice of $44.1$ kHz for CDs was specifically engineered to satisfy the Nyquist criterion for human hearing (20 kHz) while allowing practical, low-cost analog anti-aliasing filters to be manufactured in the 1980s.
- **Power Systems:** Digital protective relays sample continuous voltage and current waveforms from the grid at specific rates (e.g., 64 samples per cycle) to rapidly detect faults and trip circuit breakers. If high-frequency switching transients alias into the fundamental 60 Hz measurement, the relay could falsely trip, plunging a city into darkness.

---
## 4. THEORETICAL FOUNDATIONS

### 4.1 Ideal Sampling: Multiplication by Dirac Comb
We model the sampling process mathematically to understand its exact effect on the signal's frequency content.
Consider a continuous-time signal $x(t)$. We want to sample this signal instantaneously every $T$ seconds.
We define an ideal sampling function, known as a Dirac comb or impulse train, $p(t)$:
$$p(t) = \sum_{n=-\infty}^{\infty} \delta(t - nT)$$
where:
- $T$ is the sampling period (in seconds).
- $f_s = 1/T$ is the sampling frequency (in Hertz).

The ideal sampled signal, denoted as $x_s(t)$, is the mathematical product of the continuous signal and the impulse train:
$$x_s(t) = x(t) \cdot p(t) = x(t) \sum_{n=-\infty}^{\infty} \delta(t - nT)$$
Because the delta function is zero everywhere except when its argument is zero (i.e., at $t = nT$), we can apply the multiplication property $x(t)\delta(t - t_0) = x(t_0)\delta(t - t_0)$:
$$x_s(t) = \sum_{n=-\infty}^{\infty} x(nT) \delta(t - nT)$$
This equation states that the sampled signal $x_s(t)$ is a train of impulses, occurring at integer multiples of $T$, where the area (weight) of each impulse is exactly equal to the value of the continuous signal $x(t)$ at that specific instant $nT$.

### 4.2 Frequency Domain Analysis of Sampling (Poisson Sum Formula)
To understand what sampling does to the signal, we must look at the frequency domain. We take the Fourier transform of the sampled signal $x_s(t)$.
$$X_s(f) = \mathcal{F}\{x_s(t)\} = \mathcal{F}\{x(t) \cdot p(t)\}$$
Using the convolution theorem, time-domain multiplication becomes frequency-domain convolution:
$$X_s(f) = X(f) * P(f)$$
where $X(f)$ is the spectrum of the original analog signal, and $P(f)$ is the spectrum of the impulse train.
To find $P(f)$, we expand the periodic impulse train $p(t)$ into a continuous-time Fourier series:
$$p(t) = \sum_{k=-\infty}^{\infty} C_k e^{j 2\pi k f_s t}$$
The Fourier coefficients $C_k$ are calculated over one period (from $-T/2$ to $T/2$):
$$C_k = \frac{1}{T} \int_{-T/2}^{T/2} p(t) e^{-j 2\pi k f_s t} dt$$
Since the only impulse in the interval $[-T/2, T/2]$ is $\delta(t)$ at $t=0$:
$$C_k = \frac{1}{T} \int_{-T/2}^{T/2} \delta(t) e^{-j 2\pi k f_s t} dt = \frac{1}{T} e^0 = \frac{1}{T} = f_s$$
Thus, the Fourier series representation of the impulse train is:
$$p(t) = f_s \sum_{k=-\infty}^{\infty} e^{j 2\pi k f_s t}$$
Now, taking the Fourier transform of $p(t)$ by transforming each complex exponential into a frequency-shifted delta function:
$$P(f) = \mathcal{F}\{p(t)\} = f_s \sum_{k=-\infty}^{\infty} \delta(f - kf_s)$$
Substitute $P(f)$ back into the convolution equation for $X_s(f)$:
$$X_s(f) = X(f) * \left( f_s \sum_{k=-\infty}^{\infty} \delta(f - kf_s) \right)$$
Because convolution is a linear operator, we can bring the summation and scaling factor outside:
$$X_s(f) = f_s \sum_{k=-\infty}^{\infty} [X(f) * \delta(f - kf_s)]$$
Using the property that convolution with a shifted impulse simply shifts the function ($X(f) * \delta(f - f_0) = X(f - f_0)$):
$$X_s(f) = f_s \sum_{k=-\infty}^{\infty} X(f - kf_s)$$
**This is the fundamental equation of sampling.** It reveals that sampling a signal in the time domain creates an infinite number of exact replicas (images or aliases) of the signal's original spectrum $X(f)$, shifted by every integer multiple of the sampling frequency $f_s$, and scaled by $f_s$.

### 4.3 The Nyquist-Shannon Theorem and the Baseband
For a signal to be practically useful, it must have a finite bandwidth. Let us define a strictly bandlimited signal $x(t)$ such that its spectrum $X(f) = 0$ for all $|f| > f_{max}$. The frequency $f_{max}$ is the highest frequency component present in the signal.

Looking at the sampled spectrum $X_s(f) = f_s \sum_{k=-\infty}^{\infty} X(f - kf_s)$, we see:
- The baseband copy ($k=0$) is centered at $f = 0$ and spans from $-f_{max}$ to $f_{max}$.
- The first upper copy ($k=1$) is centered at $f = f_s$ and spans from $f_s - f_{max}$ to $f_s + f_{max}$.
- The first lower copy ($k=-1$) is centered at $f = -f_s$ and spans from $-f_s - f_{max}$ to $-f_s + f_{max}$.

To be able to perfectly isolate the original baseband spectrum $X(f)$ from $X_s(f)$, the shifted copies must not overlap. 
The top edge of the baseband copy is $f_{max}$. 
The bottom edge of the first upper copy is $f_s - f_{max}$.
To prevent overlap, we require:
$$f_{max} < f_s - f_{max}$$
$$2f_{max} < f_s$$
This is the **Nyquist criterion**. The sampling frequency $f_s$ must be strictly greater than twice the maximum frequency present in the signal. The minimum sampling rate $2f_{max}$ is called the **Nyquist rate**.

### 4.4 Aliasing and the Anti-Aliasing Filter
If the Nyquist criterion is violated ($f_s < 2f_{max}$), the lower edge of the $k=1$ copy ($f_s - f_{max}$) will fall below the upper edge of the $k=0$ baseband copy ($f_{max}$). 
The spectra will overlap. In the regions of overlap, the frequencies add together destructively. High-frequency components from the original signal will slide down into the lower frequency ranges. This irreversible corruption is called **aliasing**.

Once a signal is sampled and aliased, it is mathematically impossible to separate the true low-frequency components from the folded high-frequency components. Therefore, aliasing must be prevented *before* sampling occurs.

**The Anti-Aliasing Filter (AAF):**
To guarantee that no frequencies above $f_s/2$ enter the sampler, an analog low-pass filter is placed immediately before the ADC. 
- Ideal AAF: A "brick-wall" filter with a cutoff exactly at $f_s/2$. This is physically impossible to build.
- Practical AAF: Has a passband up to $f_{pass}$, a transition band, and a stopband starting at $f_{stop}$. 
To prevent aliasing into the passband, we must ensure that any frequency that could alias back into $f_{pass}$ is attenuated by the stopband. 
The critical aliasing boundary is $f_{stop} = f_s - f_{pass}$.

### 4.5 Ideal Reconstruction
If $f_s > 2f_{max}$, the copies in $X_s(f)$ do not overlap. To recover $x(t)$, we simply need to extract the baseband copy $k=0$ and discard all other copies ($k = \pm 1, \pm 2, ...$).
We do this by passing the sampled signal $x_s(t)$ through an ideal continuous-time low-pass filter $h_r(t)$, with frequency response $H_r(f)$.
The reconstruction filter $H_r(f)$ must:
1. Have a gain of $T$ (to cancel the $f_s = 1/T$ scaling factor introduced by sampling).
2. Have a cutoff frequency $f_c$ such that $f_{max} \leq f_c \leq f_s - f_{max}$. (Usually $f_c = f_s/2$ is chosen).
3. Have zero gain outside this passband.

Mathematically:
$$H_r(f) = \begin{cases} T, & |f| \leq f_s/2 \\ 0, & |f| > f_s/2 \end{cases}$$
The recovered spectrum is:
$$X_r(f) = X_s(f) \cdot H_r(f) = X(f)$$
To find the time-domain reconstructed signal, we take the inverse CTFT of $H_r(f)$ to find the impulse response $h_r(t)$:
$$h_r(t) = \int_{-\infty}^{\infty} H_r(f) e^{j2\pi ft} df = \int_{-f_s/2}^{f_s/2} T e^{j2\pi ft} df$$
$$h_r(t) = T \left[ \frac{e^{j2\pi ft}}{j2\pi t} \right]_{-f_s/2}^{f_s/2} = T \frac{e^{j\pi f_s t} - e^{-j\pi f_s t}}{j2\pi t} = T \frac{2j \sin(\pi f_s t)}{j2\pi t} = \frac{\sin(\pi f_s t)}{\pi f_s t} = \text{sinc}(f_s t)$$
The reconstructed signal is the convolution of the sampled signal and the reconstruction filter:
$$x_r(t) = x_s(t) * h_r(t) = \left( \sum_{n=-\infty}^{\infty} x(nT) \delta(t - nT) \right) * \text{sinc}(f_s t)$$
Because convolution is linear and shift-invariant:
$$x_r(t) = \sum_{n=-\infty}^{\infty} x(nT) \text{sinc}(f_s(t - nT))$$
This exact mathematical reconstruction is known as Whittaker-Shannon interpolation. It states that the continuous signal can be perfectly rebuilt by placing a continuous sinc function at every sample point, scaled by the sample value, and summing them all up.

### 4.6 Practical Reconstruction: Zero-Order Hold (ZOH)
Ideal reconstruction requires generating perfect Dirac impulses and passing them through an ideal brick-wall filter (which requires an infinite, non-causal sinc impulse response). Real hardware cannot do this.
Practical Digital-to-Analog Converters (DACs) use a Zero-Order Hold (ZOH) circuit. When a digital sample arrives, the DAC outputs a constant voltage corresponding to that sample, and holds it steady for the entire sampling period $T$ until the next sample arrives.
This creates a staircase waveform.

Mathematically, the ZOH operation can be modeled as passing the ideal impulse train $x_s(t)$ through a filter with a rectangular impulse response:
$$h_{zoh}(t) = \begin{cases} 1, & 0 \leq t < T \\ 0, & \text{otherwise} \end{cases}$$
To understand the effect on the frequency spectrum, we take the CTFT of $h_{zoh}(t)$:
$$H_{zoh}(f) = \int_{-\infty}^{\infty} h_{zoh}(t) e^{-j2\pi ft} dt = \int_{0}^{T} 1 \cdot e^{-j2\pi ft} dt$$
$$H_{zoh}(f) = \left[ \frac{e^{-j2\pi ft}}{-j2\pi f} \right]_0^T = \frac{1 - e^{-j2\pi fT}}{j2\pi f}$$
We factor out $e^{-j\pi fT}$:
$$H_{zoh}(f) = e^{-j\pi fT} \frac{e^{j\pi fT} - e^{-j\pi fT}}{j2\pi f} = e^{-j\pi fT} \frac{2j \sin(\pi fT)}{j2\pi f} = T e^{-j\pi fT} \frac{\sin(\pi fT)}{\pi fT}$$
$$H_{zoh}(f) = T \text{sinc}(fT) e^{-j\pi fT}$$

**Interpretation of the ZOH effect (The Aperture Effect):**
1. **Magnitude Droop:** The magnitude $|H_{zoh}(f)| = T |\text{sinc}(f/f_s)|$. Unlike the ideal reconstruction filter which is perfectly flat in the passband, the ZOH acts as a low-pass filter that heavily attenuates higher frequencies within the baseband. At the Nyquist frequency $f = f_s/2$, the attenuation is $\text{sinc}(0.5) = 2/\pi \approx 0.636$, which is nearly -4 dB. This causes an audible "muffling" of high frequencies in audio.
2. **Phase Shift:** The $e^{-j\pi fT}$ term represents a linear phase shift, which corresponds to a constant time delay of $T/2$ seconds. This is usually harmless in open-loop systems but must be accounted for in tight feedback control loops.
3. **Incomplete Image Rejection:** The ideal filter cuts off completely at $f_s/2$. The ZOH sinc function has a slow roll-off and contains sidelobes. High-frequency spectral images (at $f_s, 2f_s$, etc.) are partially allowed through. 
To fix these issues, practical DACs are followed by an analog **reconstruction filter** (or smoothing filter) to remove the remaining high-frequency images, and often employ a digital **inverse-sinc filter** before the DAC to pre-emphasize the high frequencies and exactly cancel the ZOH droop.

### 4.7 Quantization, Dynamic Range, and SNR
Sampling discretizes time. Quantization discretizes amplitude. 
A practical ADC has a finite number of bits, $B$. It divides the continuous input voltage range, $V_{FS}$ (Full Scale), into $2^B$ discrete levels.
The distance between adjacent levels is the resolution or step size, denoted by $\Delta$:
$$\Delta = \frac{V_{FS}}{2^B}$$
When a continuous sample $x(nT)$ is quantized to the nearest level $x_q(nT)$, an error is introduced:
$$e[n] = x(nT) - x_q(nT)$$
To analyze quantization noise, we make several standard statistical assumptions (which hold true for rapidly varying, complex signals):
1. The error $e[n]$ is uniformly distributed between $-\Delta/2$ and $\Delta/2$.
2. The error sequence is a wide-sense stationary white noise process.
3. The error is uncorrelated with the input signal.

**Quantization Noise Power:**
The probability density function (PDF) of the error is $p(e) = 1/\Delta$ for $-\Delta/2 \leq e \leq \Delta/2$, and 0 elsewhere.
The expected value (mean) is 0.
The variance (which equals the noise power, $\sigma_e^2$) is:
$$\sigma_e^2 = \int_{-\infty}^{\infty} e^2 p(e) de = \int_{-\Delta/2}^{\Delta/2} e^2 \left(\frac{1}{\Delta}\right) de = \frac{1}{\Delta} \left[ \frac{e^3}{3} \right]_{-\Delta/2}^{\Delta/2} = \frac{1}{3\Delta} \left( \frac{\Delta^3}{8} - \left(-\frac{\Delta^3}{8}\right) \right) = \frac{\Delta^2}{12}$$

**Signal-to-Quantization-Noise Ratio (SQNR):**
To evaluate the performance of an ADC, we calculate the SQNR for a worst-case scenario: a full-scale sinusoidal input.
Let $x(t) = \frac{V_{FS}}{2} \sin(2\pi f t)$. The peak-to-peak amplitude is $V_{FS}$.
The power of this sinusoidal signal is:
$$P_x = \frac{A^2}{2} = \frac{(V_{FS}/2)^2}{2} = \frac{V_{FS}^2}{8}$$
The SQNR is the ratio of signal power to noise power:
$$SQNR = \frac{P_x}{\sigma_e^2} = \frac{V_{FS}^2 / 8}{\Delta^2 / 12} = \frac{V_{FS}^2 / 8}{(V_{FS} / 2^B)^2 / 12} = \frac{12}{8} \cdot \frac{V_{FS}^2}{V_{FS}^2 / 2^{2B}} = \frac{3}{2} 2^{2B}$$
Expressing this in decibels (dB):
$$SQNR_{dB} = 10 \log_{10}\left(1.5 \cdot 2^{2B}\right) = 10 \log_{10}(1.5) + 10 \log_{10}(2^{2B}) = 1.76 + 20 B \log_{10}(2) \approx 1.76 + 6.02 B \text{ dB}$$
**Fundamental Rule of Thumb:** Every additional bit of resolution provides an extra ~6 dB of dynamic range and SNR. A 16-bit ADC gives ~98 dB. A 24-bit ADC gives ~146 dB.

**Equivalent Number of Bits (ENOB):**
In real hardware, ADCs suffer from thermal noise, clock jitter, and non-linearities, meaning the true measured SNR is always less than the theoretical maximum.
We define ENOB to describe the actual performance of the ADC:
$$ENOB = \frac{SNR_{measured} - 1.76}{6.02}$$

### 4.8 Oversampling and Sigma-Delta ($\Sigma\Delta$) ADCs
**Traditional Oversampling:**
If an ADC samples at the exact Nyquist rate ($f_s = 2f_{max}$), the quantization noise power $\Delta^2/12$ is spread uniformly across the frequency band from $-f_{max}$ to $f_{max}$. 
If we oversample by a ratio $M$, such that $f_s = M \cdot 2f_{max}$, the total quantization noise power $\Delta^2/12$ remains exactly the same, but it is now spread evenly over a much wider frequency band, from $-M f_{max}$ to $M f_{max}$.
The Noise Power Spectral Density (PSD) drops from $\frac{\Delta^2/12}{2f_{max}}$ to $\frac{\Delta^2/12}{2M f_{max}}$.
By passing this oversampled digital signal through a strict digital low-pass filter with a cutoff at $f_{max}$, we filter out all the noise above the signal bandwidth. The remaining in-band noise power is reduced by a factor of $M$.
The new SNR improvement is:
$$\Delta SNR = 10 \log_{10}(M) \text{ dB}$$
For every doubling of the sampling rate ($M \times 2$), we gain 3 dB of SNR, which is equivalent to 0.5 bits of extra resolution.

**Sigma-Delta ($\Sigma\Delta$) Modulator (First-Order Noise Shaping):**
Traditional oversampling is inefficient (doubling the speed only gets 0.5 bits). $\Sigma\Delta$ ADCs use feedback to completely alter the frequency distribution of the quantization noise.
A 1st-order $\Sigma\Delta$ modulator consists of an integrator (an accumulator in discrete time), a 1-bit quantizer (a comparator), and a feedback loop.
In the z-domain, the output $Y(z)$ can be expressed as a function of the input signal $X(z)$ and the quantization noise $E(z)$:
$$Y(z) = z^{-1}X(z) + (1 - z^{-1})E(z)$$
- The **Signal Transfer Function (STF)** is $z^{-1}$, which is just a single sample delay. The signal passes through perfectly.
- The **Noise Transfer Function (NTF)** is $1 - z^{-1}$. This is a discrete-time differentiator, which acts as a high-pass filter.
To see the frequency response of the NTF, substitute $z = e^{j2\pi f / f_s}$:
$$NTF(f) = 1 - e^{-j2\pi f / f_s} = e^{-j\pi f / f_s} \left( e^{j\pi f / f_s} - e^{-j\pi f / f_s} \right) = e^{-j\pi f / f_s} \cdot 2j \sin(\pi f / f_s)$$
The magnitude squared is:
$$|NTF(f)|^2 = 4 \sin^2\left(\frac{\pi f}{f_s}\right)$$
At low frequencies (the signal band, $f \ll f_s$), $\sin(x) \approx x$, so the noise power is proportional to $f^2$. The noise is virtually eliminated in the baseband and pushed massively to high frequencies!
A digital decimation filter then easily removes this high-frequency noise. 
For a 1st-order $\Sigma\Delta$ ADC, every doubling of the oversampling ratio $M$ yields a **9 dB** improvement (1.5 bits of resolution). A 2nd-order loop gives **15 dB** (2.5 bits) per octave! This allows incredibly precise audio converters (24-bit) to be built using only 1-bit quantizers running at multi-MHz speeds.

---
## 5. COMPLETE PROOFS AND DERIVATIONS
The complete, rigorous proofs for the Poisson Sum Formula, the ideal reconstruction via Whittaker-Shannon interpolation, the Zero-Order Hold frequency response, and the quantization noise power variance have all been integrated directly into Section 4 to maintain logical flow and context for the student.

---
## 6. WORKED EXAMPLES (MINIMUM 5)

### Example 1: Detailed Aliasing Frequency Computation
**Problem statement:** 
A continuous-time signal $x(t) = 8\cos(2\pi \cdot 2500 t) + 4\sin(2\pi \cdot 6000 t) + 2\cos(2\pi \cdot 11000 t)$ is sampled at a frequency $f_s = 8000$ Hz. The sampled signal is then passed through an ideal low-pass reconstruction filter with a cutoff frequency of $f_c = 4000$ Hz and a passband gain of $T$. 
Determine the exact mathematical expression of the reconstructed continuous-time signal $x_r(t)$.

**Solution:**
1. Identify the frequencies present in the original signal:
   - $f_1 = 2500$ Hz (Amplitude 8, Cosine)
   - $f_2 = 6000$ Hz (Amplitude 4, Sine)
   - $f_3 = 11000$ Hz (Amplitude 2, Cosine)
2. Identify the sampling parameters:
   - $f_s = 8000$ Hz
   - Nyquist folding frequency = $f_s/2 = 4000$ Hz.
   - Any frequency component greater than 4000 Hz will suffer aliasing.
3. Analyze $f_1 = 2500$ Hz:
   - $f_1 < 4000$ Hz. This frequency satisfies the Nyquist criterion. It is reconstructed perfectly without aliasing.
   - Reconstructed component: $8\cos(2\pi \cdot 2500 t)$.
4. Analyze $f_2 = 6000$ Hz:
   - $f_2 > 4000$ Hz. Aliasing occurs.
   - The aliased frequency is given by $f_a = |f_2 - k f_s|$. 
   - We must find integer $k$ such that $0 \leq f_a \leq f_s/2$.
   - Try $k=1$: $f_a = |6000 - 1(8000)| = |-2000| = 2000$ Hz.
   - The 6000 Hz sine wave folds down and appears as a 2000 Hz signal. 
   - Because the argument inside the absolute value was negative ($6000 - 8000 = -2000$), the phase of a sine wave is inverted (since $\sin(-\theta) = -\sin(\theta)$). 
   - Reconstructed component: $-4\sin(2\pi \cdot 2000 t)$.
5. Analyze $f_3 = 11000$ Hz:
   - $f_3 > 4000$ Hz. Aliasing occurs.
   - Try $k=1$: $f_a = |11000 - 8000| = 3000$ Hz.
   - This falls in the range $0$ to $4000$ Hz, so $k=1$ is correct.
   - The argument was positive, and cosine is an even function anyway ($\cos(-\theta) = \cos(\theta)$), so there is no phase inversion.
   - Reconstructed component: $2\cos(2\pi \cdot 3000 t)$.
6. Construct the final signal $x_r(t)$ by summing the reconstructed components:
   $$x_r(t) = 8\cos(2\pi \cdot 2500 t) - 4\sin(2\pi \cdot 2000 t) + 2\cos(2\pi \cdot 3000 t)$$

**Physical interpretation:** 
The sampler cannot distinguish between a low frequency signal and a higher frequency signal that hits the exact same points at the exact same times. The 6 kHz and 11 kHz signals masquerade as 2 kHz and 3 kHz signals in the digital domain. The ideal filter just outputs the lowest frequency alias.
**Common mistakes to avoid:** 
Forgetting the phase inversion that occurs with sine waves when the alias calculation results in a negative inner argument.

### Example 2: Anti-Aliasing Filter Specification and Roll-off
**Problem statement:** 
An industrial sensor produces a baseband signal with a maximum useful frequency of $f_{pass} = 2.5$ kHz. The system engineer selects a sampling frequency of $f_s = 10$ kHz. The ADC has 12 bits of resolution, giving a dynamic range of approximately 74 dB. 
To ensure aliasing noise does not corrupt the 12-bit accuracy, the anti-aliasing filter must provide at least 74 dB of attenuation for any frequency that could alias into the passband.
If a simple first-order RC low-pass filter (which provides 6 dB/octave roll-off) is used, and the -3 dB cutoff is placed at 2.5 kHz, will this filter meet the requirements? If not, what order Butterworth filter (which provides $6n$ dB/octave roll-off, where $n$ is the order) is required?

**Solution:**
1. Determine the critical stopband frequency $f_{stop}$:
   - Frequencies that alias into the passband ($0$ to $2.5$ kHz) originate from the first spectral copy centered at $f_s = 10$ kHz.
   - The lowest frequency from the first copy that folds back into the passband is $f_s - f_{pass} = 10 - 2.5 = 7.5$ kHz.
   - Therefore, the filter must provide $\geq 74$ dB of attenuation at $f_{stop} = 7.5$ kHz.
2. Evaluate the first-order RC filter:
   - The cutoff frequency is $f_c = 2.5$ kHz (where attenuation is ~3 dB).
   - How many octaves between $f_c$ and $f_{stop}$? 
   - An octave is a doubling of frequency. $\log_2(f_{stop} / f_c) = \log_2(7.5 / 2.5) = \log_2(3) \approx 1.58$ octaves.
   - Attenuation of a 1st-order filter at 7.5 kHz $\approx 1.58 \text{ octaves} \times 6 \text{ dB/octave} = 9.48 \text{ dB}$.
   - 9.48 dB is massively short of the required 74 dB. The first-order filter fails completely.
3. Calculate the required filter order $n$:
   - Required attenuation = 74 dB.
   - Number of octaves = 1.58.
   - Required roll-off rate = $74 / 1.58 \approx 46.8$ dB/octave.
   - Since a Butterworth filter provides $6n$ dB/octave, we set $6n \geq 46.8$.
   - $n \geq 46.8 / 6 = 7.8$.
   - Filter orders must be integers, so we must round up to the next highest integer.
   - Required order $n = 8$.

**Physical interpretation:** 
A transition band of 5 kHz (from 2.5 to 7.5) is very narrow. Forcing a purely analog circuit to drop 74 dB in just 1.5 octaves requires complex, multi-stage active filter topologies (an 8th order filter requires 4 op-amps). This demonstrates why oversampling is so popular—it widens the transition band drastically, allowing simple 1st-order filters to work.

### Example 3: Zero-Order Hold Droop Compensation
**Problem statement:** 
A CD audio player utilizes a DAC operating at $f_s = 44.1$ kHz. The signal passes through a Zero-Order Hold (ZOH) output stage. 
Calculate the exact amplitude attenuation (in dB) experienced by a $15$ kHz cymbal crash due to the aperture effect of the ZOH. 
If a digital pre-compensation (inverse-sinc) filter is used, what specific gain must it apply at 15 kHz to perfectly flatten the frequency response?

**Solution:**
1. Identify parameters:
   - Signal frequency $f = 15000$ Hz.
   - Sampling frequency $f_s = 44100$ Hz.
2. The ZOH magnitude response is $|H_{zoh}(f)| = T |\text{sinc}(f/f_s)|$. We will normalize $T=1$ since we only care about relative attenuation.
   $$|H_{zoh}(f)|_{normalized} = \frac{\sin(\pi f / f_s)}{\pi f / f_s}$$
3. Calculate the argument $x = f/f_s$:
   $$x = \frac{15000}{44100} \approx 0.340136$$
4. Calculate the sinc function value:
   $$|H_{zoh}(15000)| = \frac{\sin(\pi \cdot 0.340136)}{\pi \cdot 0.340136} = \frac{\sin(1.06857)}{1.06857} \text{ rad}$$
   $$|H_{zoh}(15000)| = \frac{0.8767}{1.06857} \approx 0.8204$$
5. Convert the attenuation to decibels (dB):
   $$\text{Attenuation}_{dB} = 20 \log_{10}(0.8204) \approx -1.72 \text{ dB}$$
6. Calculate the compensation gain:
   To perfectly flatten the response, the digital filter must apply the exact inverse of this attenuation.
   $$Gain_{linear} = \frac{1}{0.8204} \approx 1.218$$
   $$Gain_{dB} = +1.72 \text{ dB}$$

**Physical interpretation:** 
The stair-step nature of the DAC output intrinsically acts as a low-pass filter, dulling high frequencies. A 1.72 dB drop is noticeably audible to a trained ear. The DSP chip inside the CD player artificially boosts the 15 kHz digital signals by 1.72 dB *before* sending them to the DAC, so the physical ZOH droop exactly cancels the boost, resulting in a perfectly flat analog output.

### Example 4: SNR, Quantization Noise, and ENOB
**Problem statement:** 
A precision digital multimeter uses a 16-bit ADC with an input range of $0$ to $5$ V. 
a) Calculate the quantization step size (resolution).
b) Calculate the theoretical maximum SQNR for a full-scale AC sine wave.
c) During testing, a 1 kHz full-scale sine wave is applied, and the measured SNR is found to be 86 dB. The degradation is due to thermal noise in the analog front-end. Calculate the Equivalent Number of Bits (ENOB).

**Solution:**
a) Quantization step size $\Delta$:
   - $V_{FS} = 5$ V.
   - $B = 16$.
   - $\Delta = \frac{V_{FS}}{2^B} = \frac{5}{2^{16}} = \frac{5}{65536} \approx 76.29 \mu\text{V}$.
b) Theoretical Maximum SQNR:
   - Use the formula: $SQNR = 6.02 B + 1.76 \text{ dB}$.
   - $SQNR = 6.02(16) + 1.76 = 96.32 + 1.76 = 98.08 \text{ dB}$.
c) Equivalent Number of Bits (ENOB):
   - Measured SNR = 86 dB.
   - $ENOB = \frac{SNR_{measured} - 1.76}{6.02}$
   - $ENOB = \frac{86 - 1.76}{6.02} = \frac{84.24}{6.02} \approx 13.99 \text{ bits}$.

**Physical interpretation:** 
While the digital readout might show 16 bits of numbers, the bottom 2 bits are essentially random noise generated by the thermal agitation of electrons in the analog circuits preceding the ADC. The true, usable accuracy of the instrument is only 14 bits.

### Example 5: Sigma-Delta Oversampling and Noise Shaping Gain
**Problem statement:** 
An audio system requires an SNR of at least 110 dB in the audio band ($0$ to $20$ kHz). 
A design utilizes a 1st-order Sigma-Delta modulator with a 1-bit internal quantizer (comparator). 
If the base Nyquist rate is $f_N = 40$ kHz, calculate the required Oversampling Ratio (OSR) and the corresponding sampling frequency $f_s$ required to achieve this 110 dB SNR.
Assume the 1-bit quantizer alone provides an initial baseband SQNR of 7.78 dB (using the 6.02(1) + 1.76 formula).

**Solution:**
1. Determine the required SNR improvement:
   - Target SNR = 110 dB.
   - Base SNR = 7.78 dB.
   - Required Improvement = $110 - 7.78 = 102.22$ dB.
2. Relate OSR to SNR improvement for a 1st-order $\Sigma\Delta$:
   - A 1st-order loop provides an SNR improvement of roughly 9 dB per octave of oversampling.
   - Let $N_{octaves}$ be the number of octaves.
   - $9 \times N_{octaves} = 102.22 \implies N_{octaves} = 102.22 / 9 \approx 11.36$ octaves.
3. Calculate the Oversampling Ratio (OSR):
   - An octave is a power of 2. 
   - $OSR = 2^{N_{octaves}} = 2^{11.36}$.
   - $2^{11} = 2048$. $2^{11.36} \approx 2631$.
   - We must round up to the nearest integer, or practically, the nearest power of 2 for easy digital filtering. Let's use $OSR = 4096$ (which is 12 octaves).
4. Calculate the required sampling frequency $f_s$:
   - $f_s = OSR \times f_N = 4096 \times 40000$ Hz.
   - $f_s = 163.84$ MHz.

**Physical interpretation:** 
By running a simple, cheap 1-bit comparator at 163 MHz, the system pushes almost all of its quantization noise out into the MHz range. A digital decimation filter then deletes everything above 20 kHz. The remaining signal has 110 dB of purity—better than CD quality—achieved entirely without the need for precisely matched resistor ladders (which multi-bit ADCs require).

### Example 6: Impact of Clock Jitter on ADC Performance
**Problem statement:** 
Consider a sinusoidal input signal $x(t) = A \sin(2\pi f_{in} t)$ sampled by an ADC. The sampling clock has a small timing uncertainty (jitter) with an rms value of $\Delta t_{rms}$. Show mathematically how this limits the maximum achievable SNR, and calculate the maximum allowable jitter for a 14-bit ADC sampling a 100 kHz signal if the jitter noise must not exceed the theoretical quantization noise.

**Solution:**
1. The error in voltage due to a timing error $\Delta t$ is approximately:
   $$\Delta v pprox rac{dx(t)}{dt} \Delta t$$
2. The derivative of the input is:
   $$rac{dx(t)}{dt} = A (2\pi f_{in}) \cos(2\pi f_{in} t)$$
3. The maximum slew rate (worst-case derivative) occurs when $\cos=1$:
   $$	ext{Max Slew Rate} = A (2\pi f_{in})$$
4. The rms voltage error due to rms clock jitter is:
   $$\Delta v_{rms} = rac{A}{\sqrt{2}} (2\pi f_{in}) \Delta t_{rms}$$
5. The signal rms voltage is $A/\sqrt{2}$. The SNR limited purely by jitter is:
   $$SNR_{jitter} = 20 \log_{10}\left( rac{V_{sig,rms}}{\Delta v_{rms}} ight) = 20 \log_{10}\left( rac{A/\sqrt{2}}{(A/\sqrt{2}) 2\pi f_{in} \Delta t_{rms}} ight)$$
   $$SNR_{jitter} = -20 \log_{10}(2\pi f_{in} \Delta t_{rms})$$
6. For a 14-bit ADC, the theoretical quantization SNR is:
   $$SQNR pprox 6.02(14) + 1.76 = 86.04 	ext{ dB}$$
7. To ensure jitter doesn't degrade this, we need $SNR_{jitter} \geq 86.04$ dB:
   $$-20 \log_{10}(2\pi (100,000) \Delta t_{rms}) = 86.04$$
   $$\log_{10}(2\pi (100,000) \Delta t_{rms}) = -4.302$$
   $$2\pi (100,000) \Delta t_{rms} = 10^{-4.302} pprox 4.98 	imes 10^{-5}$$
   $$\Delta t_{rms} = rac{4.98 	imes 10^{-5}}{2\pi 	imes 100,000} pprox 79 	ext{ picoseconds (ps)}$$

**Physical interpretation:** 
Even if you buy a perfect 14-bit ADC chip, if your clock generator has more than 79 picoseconds of jitter, your overall system performance will drop below 14 bits because the ADC is capturing the signal slightly too early or too late during fast-moving parts of the sine wave! High-speed sampling requires incredibly stable oscillators.

---
## 7. ENGINEERING APPLICATIONS AND CASE STUDIES

### Case Study 1: The Compact Disc (CD) Audio Standard
The specifications of the CD are a masterclass in engineering trade-offs utilizing the sampling theorem.
- **Why 44.1 kHz?** Human hearing is generally accepted to span $20$ Hz to $20$ kHz. The strict Nyquist rate is therefore 40 kHz. Early digital recorders utilized modified analog video tape recorders (U-matic format). These recorders operated at $525$ lines/frame at $30$ frames/sec (NTSC) or $625$ lines/frame at $25$ frames/sec (PAL). Both formats allowed exactly 3 samples per video line. Math: $525 \times 30 = 15750$ lines/sec; $15750 \times 3 \text{ samples/line} = 47250$ samples/sec. After reserving lines for blanking intervals, the usable rate worked out to exactly 44100 samples/sec for both formats. 
- **Transition Band:** With $f_s = 44.1$ kHz and a $20$ kHz signal band, the folding frequency is $22.05$ kHz. The anti-aliasing filter has a transition band from $20$ kHz to $22.05$ kHz (a 10% width). This required very steep, expensive 9th-order elliptic analog filters in early CD players.
- **Oversampling DACs:** Modern CD players don't use steep analog filters on the output. Instead, they digitally oversample the 44.1 kHz signal to 352.8 kHz (8x oversampling), apply a sharp digital FIR interpolation filter, and then output via a DAC. The first image is now pushed up to $352.8 - 20 = 332.8$ kHz. A simple, cheap 1st-order analog RC filter easily removes this.

### Case Study 2: Software-Defined Radio (SDR) and IF Sampling
Traditional AM/FM radios use complex analog heterodyne circuits (mixers, local oscillators, IF filters) to tune to a specific station and bring it down to audio frequencies before the listener hears it.
Modern SDRs (like those in cell phones or military radios) push the ADC closer to the antenna. 
- **Direct RF Sampling:** A wideband antenna captures the entire FM band (88 MHz to 108 MHz). The ADC samples the raw RF at 250 MSPS. The entire radio spectrum up to 125 MHz is perfectly preserved in the digital domain.
- **Digital Tuning:** Selecting a station is just a mathematical operation—multiplying the digital signal by a digital complex exponential (a numerical oscillator) to shift the station down to 0 Hz, followed by a digital low-pass filter to reject all other stations. This allows one piece of hardware to demodulate AM, FM, Bluetooth, or GPS simply by loading different software.

---
## 8. COMMON STUDENT MISCONCEPTIONS AND ERRORS

1. **Misconception:** "Sampling exactly at the Nyquist rate ($f_s = 2f_{max}$) is perfectly fine in practice."
   - **Explanation:** Mathematically, it only works if the signal has infinite duration and you use a non-causal ideal sinc filter. Physically, it fails entirely. If $x(t) = \sin(2\pi f_{max} t)$, and you sample at $t = 0, \frac{1}{2f_{max}}, \frac{2}{2f_{max}}$, all your samples will fall exactly on the zero-crossings. The ADC will output a flat line of zeros! The signal is lost. You must sample *strictly greater* than $2f_{max}$, and practically, much higher to allow for filter transition bands.

2. **Misconception:** "If aliasing occurs, we can just use a DSP algorithm to filter out the false frequencies."
   - **Explanation:** Absolutely false. Once aliasing has occurred during the sampling process, the folded high frequencies sum together with the true baseband frequencies. $X_s(f)$ at a given frequency is a single number representing the sum of all aliases. You cannot untangle a summed number (if I tell you the sum is 10, you don't know if it was 5+5 or 7+3). Anti-aliasing *must* be done in the analog domain before the ADC.

3. **Misconception:** "Higher sampling rates always result in higher fidelity signals."
   - **Explanation:** Only true up to a point. Once you satisfy the Nyquist criterion for the highest frequency of *interest* (plus transition band), sampling faster does not add any new information to the signal band. It just captures higher-frequency noise, drastically increases memory storage requirements, and burns more power. 

4. **Misconception:** "Zero-Order Hold (ZOH) droop is a mathematical flaw in discrete-time signals."
   - **Explanation:** Discrete-time math is perfect. The droop is purely a physical artifact of the Analog-to-Digital hardware. The discrete samples $x[n]$ inside the computer do not have droop. The droop is injected at the exact moment the DAC circuit "holds" the voltage constant over time $T$.

5. **Misconception:** "Adding more bits to an ADC guarantees a higher quality measurement."
   - **Explanation:** An ADC's performance is bottlenecked by the analog circuitry driving it. If your sensor amplifier has 1 millivolt of thermal noise, and you use a 24-bit ADC with a 1 microvolt resolution, the bottom 10 bits of your ADC are just perfectly, faithfully digitizing random thermal noise. The Effective Number of Bits (ENOB) will still be low.

6. **Misconception:** "The Fourier transform of a sampled signal repeats just once at $f_s$."
   - **Explanation:** Students often draw just the baseband and one copy. The Poisson Sum formula has summation limits from $k = -\infty$ to $\infty$. There are an infinite number of spectral copies extending out to infinite frequency.

---
## 9. CONNECTIONS TO OTHER LECTURES
- **Builds heavily upon:** Lecture 6 (Continuous-Time Fourier Transform), Lecture 8 (Convolution and LTI Systems), and Lecture 15 (Fourier Series).
- **Critical foundation for:** 
  - Lecture 23 (The Discrete-Time Fourier Transform - DTFT): The DTFT is simply the continuous spectrum of the sampled signal $X_s(f)$ with the frequency axis normalized to $\omega = 2\pi f/f_s$. The infinite periodicity of $X_s(f)$ perfectly explains why the DTFT is always periodic with period $2\pi$.
  - Lecture 25 (The Discrete Fourier Transform - DFT): Understanding how sampling in time causes periodicity in frequency is the key to understanding why sampling in frequency (the DFT) causes periodicity in time (circular convolution).
  - Lecture 30 (FIR Filter Design): Designing digital anti-aliasing and interpolation filters requires the windowing methods taught later.

---
## 10. EXAMINATION QUESTIONS

### 10.1 Short Answer (Assessments of Basic Recall and Concept)
**Q1.** State the Nyquist-Shannon sampling theorem precisely.
*Model Answer:* A continuous-time signal $x(t)$ strictly bandlimited to $f_{max}$ Hz can be perfectly reconstructed from its discrete samples if and only if the sampling frequency $f_s$ is strictly greater than $2f_{max}$.

**Q2.** Explain the function and necessity of an Anti-Aliasing Filter (AAF).
*Model Answer:* An AAF is an analog low-pass filter placed before an ADC. Its function is to strictly bandlimit the analog signal, ensuring no frequency components above the Nyquist folding frequency ($f_s/2$) enter the sampler. This prevents high frequencies from folding into the baseband and irreversibly corrupting the digital signal.

**Q3.** Describe the "Aperture Effect" in Digital-to-Analog Converters.
*Model Answer:* The Aperture Effect is the frequency distortion caused by the DAC's Zero-Order Hold (ZOH) circuit, which holds the output voltage constant for the sample period $T$. In the frequency domain, this acts as a sinc-shaped low-pass filter, causing amplitude attenuation (droop) at higher frequencies within the passband, particularly near $f_s/2$.

**Q4.** What is the theoretical Signal-to-Quantization-Noise Ratio (SQNR) of a 14-bit ADC for a full-scale sine wave?
*Model Answer:* Using the formula $SQNR = 6.02B + 1.76$, we get $SQNR = 6.02(14) + 1.76 = 84.28 + 1.76 = 86.04$ dB.

**Q5.** Briefly explain the core mechanism by which a Sigma-Delta ADC achieves high resolution.
*Model Answer:* It uses massive oversampling combined with a feedback loop containing an integrator. This architecture performs "noise shaping," which mathematically pushes the quantization noise out of the low-frequency signal band and into high frequencies, where it is subsequently removed by a digital low-pass decimation filter.

### 10.2 Long Answer / Numerical Problems
**Problem 1: Complex Aliasing Scenario**
A signal $x(t) = 4\cos(3000\pi t) + 2\sin(10000\pi t) + \cos(14000\pi t)$ is sampled at a rate of 6000 samples per second. The resulting discrete-time signal is passed through an ideal continuous-time low-pass filter with a cutoff frequency of 3000 Hz and a passband gain of $1/f_s$. 
Determine the exact mathematical expression for the output signal $y(t)$.
*Solution Outline:*
- Convert $\omega$ to $f$: $f_1 = 1500$ Hz, $f_2 = 5000$ Hz, $f_3 = 7000$ Hz.
- $f_s = 6000$ Hz, folding frequency = 3000 Hz.
- $f_1$ (1500 Hz): $< 3000$. Unaliased. Output: $4\cos(3000\pi t)$.
- $f_2$ (5000 Hz): $> 3000$. Alias $f_a = |5000 - 6000| = 1000$ Hz. The argument is negative, so phase inverts for sine. Output: $-2\sin(2000\pi t)$.
- $f_3$ (7000 Hz): $> 3000$. Alias $f_a = |7000 - 6000| = 1000$ Hz. Cosine is even, no inversion. Output: $\cos(2000\pi t)$.
- Total signal: $y(t) = 4\cos(3000\pi t) - 2\sin(2000\pi t) + \cos(2000\pi t)$.

**Problem 2: Anti-Aliasing Filter Design**
An ADC samples at $f_s = 48$ kHz. The signal of interest is bandlimited to 15 kHz. We require that any potential aliasing noise be suppressed by at least 60 dB. 
If we use an analog Butterworth filter, what is the minimum required filter order $N$?
*Solution Outline:*
- Passband edge $f_{pass} = 15$ kHz.
- Lowest aliasing frequency $f_{stop} = f_s - f_{pass} = 48 - 15 = 33$ kHz.
- Filter must transition from 0 dB at 15 kHz to -60 dB at 33 kHz.
- Octaves = $\log_2(33/15) = \log_2(2.2) \approx 1.137$ octaves.
- Required roll-off = $60 / 1.137 \approx 52.7$ dB/octave.
- Butterworth provides $6N$ dB/octave. $6N \geq 52.7 \implies N \geq 8.78$.
- Minimum order is $N = 9$.

**Problem 3: Quantization Noise Derivation**
Derive the expression for the variance of quantization noise, $\sigma_e^2 = \Delta^2/12$, starting from the assumption that the quantization error $e$ is uniformly distributed.
*Solution Outline:* Show PDF graph. Setup integral $\int e^2 (1/\Delta) de$ from $-\Delta/2$ to $\Delta/2$. Execute integration steps clearly as shown in Section 4.7.

**Problem 4: Oversampling Gain**
A baseband signal has a maximum frequency of $1$ MHz. A standard ADC sampling at 2 MHz yields an SNR of 40 dB. If we replace this with an oversampling ADC running at 32 MHz followed by an ideal digital low-pass filter, what is the new theoretical SNR?
*Solution Outline:*
- Base Nyquist rate = 2 MHz.
- New rate = 32 MHz.
- OSR $M = 32 / 2 = 16$.
- SNR improvement = $10 \log_{10}(M) = 10 \log_{10}(16) = 10 \times 1.204 \approx 12.04$ dB.
- New SNR = $40 + 12.04 = 52.04$ dB.

### 10.3 True/False with Justification
1. **T/F:** If a signal is undersampled, applying a sharper digital low-pass filter after the ADC can eliminate the aliasing. 
   *False. Once sampled, aliased frequencies overlap identically with real baseband frequencies. They are mathematically indistinguishable. Aliasing must be prevented by analog filters before the ADC.*
2. **T/F:** The impulse response of an ideal DAC reconstruction filter is non-causal.
   *True. The ideal brick-wall LPF transforms to a sinc function in the time domain, which extends to negative infinity in time, making it physically impossible to build in real time.*
3. **T/F:** Zero-Order Hold circuits perfectly reconstruct the digital samples into a continuous waveform without distorting the frequency content.
   *False. ZOH holds the voltage constant, which acts as a low-pass filter (sinc-shaped magnitude response), attenuating high frequencies and failing to completely reject higher-order image spectra.*
4. **T/F:** Sigma-Delta ADCs require highly precise, laser-trimmed resistor ladders to achieve 24-bit accuracy.
   *False. The beauty of a 1st-order Sigma Delta is that it uses a 1-bit quantizer (a simple comparator), which is inherently perfectly linear and requires no precision matching.*
5. **T/F:** Every octave (doubling) of oversampling in a standard (non-noise-shaping) ADC improves the SQNR by 3 dB.
   *True. The noise power density drops by a factor of 2, and the digital filter cuts away half the noise, giving a $10 \log_{10}(2) \approx 3$ dB improvement.*
6. **T/F:** A 16-bit ADC always provides exactly 96.32 dB of signal-to-noise ratio in practice.
   *False. This is the theoretical maximum SQNR based purely on quantization. Real hardware adds thermal noise and jitter, leading to a lower Effective Number of Bits (ENOB).*

---
## 11. KEY FORMULAS REFERENCE

| Concept | Formula | Notes |
| :--- | :--- | :--- |
| **Dirac Comb / Impulse Train** | $p(t) = \sum_{n=-\infty}^{\infty} \delta(t - nT)$ | Used to model ideal instantaneous sampling. |
| **Sampled Signal (Time)** | $x_s(t) = \sum_{n=-\infty}^{\infty} x(nT) \delta(t - nT)$ | Sequence of weighted impulses. |
| **Poisson Sum Formula (Freq)** | $X_s(f) = f_s \sum_{k=-\infty}^{\infty} X(f - kf_s)$ | Shows infinite periodic repetition of spectrum. |
| **Nyquist Criterion** | $f_s > 2f_{max}$ | Minimum condition to avoid aliasing. |
| **Aliased Frequency Calculation** | $f_a = \|f - kf_s\|$ | $k$ is integer chosen such that $0 \leq f_a \leq f_s/2$. |
| **Whittaker-Shannon Interpolation** | $x(t) = \sum_{n=-\infty}^{\infty} x(nT) \text{sinc}(f_s(t - nT))$ | Exact mathematical reconstruction using ideal LPF. |
| **Zero-Order Hold Response** | $H_{zoh}(f) = T e^{-j\pi fT} \text{sinc}(fT)$ | Note the low-pass droop and linear phase shift. |
| **Quantization Step Size** | $\Delta = \frac{V_{FS}}{2^B}$ | Resolution of a B-bit ADC. |
| **Quantization Noise Variance** | $\sigma_e^2 = \frac{\Delta^2}{12}$ | Assumes uniform white noise distribution. |
| **Theoretical ADC SQNR** | $SQNR \approx 6.02B + 1.76 \text{ dB}$ | For a full-scale sinusoidal input. |
| **Effective Number of Bits** | $ENOB = \frac{SNR_{measured} - 1.76}{6.02}$ | Represents true hardware performance. |
| **Standard Oversampling Gain** | $\Delta SNR = 10 \log_{10}(M)$ | $M$ is the oversampling ratio $f_s / f_{Nyquist}$. |
| **1st-Order $\Sigma\Delta$ Noise Transfer**| $NTF(z) = 1 - z^{-1}$ | Acts as a high-pass filter to quantization noise. |

---
## 12. GLOSSARY OF TERMS
- **Aliasing:** The effect that causes different signals to become indistinguishable (or aliases of one another) when sampled.
- **Anti-Aliasing Filter (AAF):** A low-pass filter used before an ADC to restrict the bandwidth of a signal to approximately satisfy the Nyquist–Shannon sampling theorem.
- **Aperture Effect:** The attenuation of high frequencies in the passband due to the Zero-Order Hold property of practical DACs.
- **Baseband:** The original band of frequencies of a signal before it is modulated or sampled.
- **Dirac Comb:** An infinite series of Dirac delta functions spaced at regular intervals.
- **ENOB (Effective Number of Bits):** A measure of the dynamic performance of an ADC, reflecting its real-world resolution after accounting for noise and distortion.
- **Nyquist Rate:** The minimum rate at which a continuous-time signal needs to be sampled to allow for perfect reconstruction, equal to twice the maximum frequency in the signal.
- **Oversampling:** Sampling a signal at a frequency significantly higher than the Nyquist rate.
- **Quantization:** The process of mapping continuous infinite values to a smaller set of discrete finite values.
- **Sigma-Delta Modulation:** A method for encoding analog signals into digital signals as found in an ADC, heavily utilizing oversampling and noise shaping.
- **Whittaker-Shannon Interpolation:** A method to construct a continuous-time bandlimited signal from a sequence of real numbers using sinc functions.
- **Zero-Order Hold (ZOH):** A mathematical model of the practical signal reconstruction done by a conventional digital-to-analog converter (DAC).

---
## 13. FURTHER READING AND REFERENCES
To provide students with diverse explanations or to prepare advanced exam problems, faculty should consult the following standard texts:

1. **Oppenheim, A. V., & Schafer, R. W. (2010).** *Discrete-Time Signal Processing (3rd Ed.)*. Prentice Hall.
   - *Target Chapter:* Chapter 4 (Sampling of Continuous-Time Signals). This is the gold standard for the mathematical rigor of sampling and polyphase reconstruction.
2. **Proakis, J. G., & Manolakis, D. G. (2006).** *Digital Signal Processing: Principles, Algorithms, and Applications (4th Ed.)*. Pearson.
   - *Target Chapter:* Chapter 1 (Introduction) and Chapter 6 (Sampling and Reconstruction). Excellent treatment of practical ADC/DAC hardware considerations and AAF design.
3. **Haykin, S. (2014).** *Communication Systems (5th Ed.)*. Wiley.
   - *Target Chapter:* Excellent for tying sampling theory directly into Information Theory, Pulse Code Modulation (PCM), and rigorous noise analysis.
4. **Texas Instruments Application Notes:**
   - *Understanding Delta-Sigma Data Converters (SBAA066)*. This is highly recommended for faculty who want to bring real-world hardware schematic examples of oversampling circuits into the classroom.

</Faculty Notes — Lecture 22: Sampling Theorem & A/D D/A Conversion>
