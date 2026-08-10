<Faculty Notes — Lecture 28: Biomedical Signal Processing>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY

This lecture, "Biomedical Signal Processing," introduces students to the real-world application of DSP techniques on physiological signals. Unlike traditional communications or control signals, biomedical signals are characterized by extremely low amplitudes and severe contamination by various noise sources that often share the same frequency bands as the signals of interest.

**How to teach this lecture:**
Start by emphasizing the fragility of physiological signals. Students must understand that capturing an ECG or EEG is fundamentally an exercise in extracting a weak signal from overwhelming noise. Introduce the signal characteristics before diving into the processing pipeline. When discussing the Pan-Tompkins algorithm, write out the block diagram on the board and step through the transformation of the signal at each stage physically. The concept of filtering, differentiation, squaring, and integration should be mapped visually to how a typical ECG QRS complex evolves through the pipeline. 

**Common student difficulties:**
- Differentiating between different types of biological signals (ECG vs EEG vs EMG).
- Understanding the mathematical reasoning behind the Pan-Tompkins steps (especially why squaring and moving window integration are both necessary).
- Grasping the physical meaning of pole-zero placement for the notch filter. Many can memorize the transfer function but fail to understand why $r < 1$ prevents instability while controlling the notch bandwidth.
- Interpreting frequency bands in HRV and EEG analysis. Students often confuse the significance of LF vs HF in HRV.

**Suggested demos:**
- Bring a basic AD8232 ECG sensor module and an Arduino. Plot the raw signal on a serial plotter, then apply a simple moving average or digital notch filter in real-time.
- Show an animation of the Pan-Tompkins algorithm stages, highlighting the signal shape after each step.
- Demonstrate HRV using a smartphone camera app that measures PPG, showing how breathing deeply increases the high-frequency variation.
- Use a digital stethoscope (like Eko) to visualize a phonocardiogram live, showing the separation of S1 and S2.

---
## 1. LEARNING OBJECTIVES

By the end of this comprehensive lecture, students will be able to:
1. **Identify and characterize** the amplitude ranges, frequency bandwidths, and physiological origins of primary biomedical signals, including ECG, EEG, EMG, and PPG.
2. **Design and analyze** digital notch filters for powerline interference removal using precise pole-zero placement techniques.
3. **Derive and mathematically justify** each stage of the Pan-Tompkins QRS detection algorithm.
4. **Compute and interpret** Time-Domain and Frequency-Domain Heart Rate Variability (HRV) metrics and relate them to autonomic nervous system balance.
5. **Categorize** EEG frequency bands according to their cognitive correlates and explain the principles of spatial filtering and Independent Component Analysis (ICA) for artifact removal.
6. **Formulate** signal processing pipelines for EMG signals to assess muscle fatigue and for digital phonocardiograms to detect pathological heart sounds.
7. **Evaluate** real-time processing constraints in biomedical embedded systems.
8. **Analyze** non-stationary signals using time-frequency methods conceptually to detect evolving features like muscle fatigue.

---
## 2. PREREQUISITE KNOWLEDGE REVIEW

Before embarking on this lecture, students must be fluent in the following DSP concepts:

**Z-Transform and System Functions:**
Students must know how to relate poles and zeros in the Z-plane to the magnitude and phase response of a filter.
$$ H(z) = \frac{Y(z)}{X(z)} = \frac{\sum_{k=0}^{M} b_k z^{-k}}{1 + \sum_{k=1}^{N} a_k z^{-k}} $$

**Pole-Zero Placement on the Z-Plane:**
- A zero on the unit circle at angle $\theta$ completely completely nulls the frequency response at $\omega = \theta$.
- A pole near the unit circle at angle $\theta$ causes a sharp peak in the frequency response at $\omega = \theta$.
- Stability requires all poles to be strictly inside the unit circle ($|p| < 1$).

**Digital Differentiators:**
Approximations of continuous-time derivatives in discrete time using backward differences:
$$ y[n] = x[n] - x[n-1] $$
or more complex central differences.

**Moving Average Filters:**
The concept of smoothing as a low-pass filtering operation:
$$ y[n] = \frac{1}{N} \sum_{k=0}^{N-1} x[n-k] $$

**Power Spectral Density (PSD):**
Understanding how Welch's method or the periodogram estimates the distribution of signal power over frequency.

---
## 3. HISTORICAL AND MOTIVATIONAL CONTEXT

**Historical Context:**
The marriage of signal processing and medicine dates back to the early 20th century. Willem Einthoven invented the first practical electrocardiogram (ECG) in 1903 using a string galvanometer, for which he won the Nobel Prize. However, early ECGs were purely analog and prone to massive interference. The digital revolution in the 1960s and 70s allowed for robust, computerized analysis. In 1985, J. Pan and W. J. Tompkins published their seminal paper on a real-time QRS detection algorithm, which remains the gold standard today. Similarly, Hans Berger recorded the first human EEG in 1924, but it wasn't until the advent of the Fast Fourier Transform (FFT) and Independent Component Analysis (ICA) in the late 20th century that meaningful, real-time brain-computer interfaces (BCIs) became feasible.

**Real Engineering Applications:**
For EEE students, biomedical signal processing is the core technology behind:
- **Wearable Health Tech:** Apple Watches, Fitbits, and Garmin devices use photoplethysmography (PPG) and single-lead ECGs to detect atrial fibrillation and track HRV.
- **Brain-Computer Interfaces (BCI):** Allowing paralyzed patients to control robotic limbs or cursors via real-time EEG processing.
- **Smart Prosthetics:** Using surface EMG signals to decode patient intent and actuate robotic hands with proportional force.
- **Intensive Care Unit (ICU) Monitors:** Continuously processing multi-parameter data to trigger life-saving alarms while ignoring false artifacts.

**Why EEE needs this:**
Biomedical instrumentation is fundamentally an electrical engineering discipline. The body is an electrical generator (the heart, the brain, the muscles). Capturing these microvolt-level signals in an environment saturated with 50/60 Hz electromagnetic interference requires masterful analog front-end design coupled with advanced digital signal processing. Without DSP, raw biomedical signals are virtually useless due to the overwhelming noise floor.

---
## 4. THEORETICAL FOUNDATIONS

### 4.1 Biomedical Signal Characteristics

Biomedical signals are incredibly diverse. We must understand their intrinsic properties to design effective DSP pipelines.

#### 4.1.1 Electrocardiogram (ECG)
- **Origin:** Electrical activity of the heart muscles (myocardium) during depolarization and repolarization.
- **Amplitude Range:** $0.5 \text{ mV}$ to $5 \text{ mV}$ (typically analyzed in the $1 \text{ mV}$ range).
- **Frequency Band:** $0.05 \text{ Hz}$ to $150 \text{ Hz}$ for diagnostic quality; $0.5 \text{ Hz}$ to $40 \text{ Hz}$ for standard patient monitoring.
- **Key Features:** P wave (atrial depolarization), QRS complex (ventricular depolarization), T wave (ventricular repolarization).
- **Challenges:** Baseline wander (due to respiration), powerline interference, and muscle tremor (EMG noise).

#### 4.1.2 Electroencephalogram (EEG)
- **Origin:** Summated excitatory and inhibitory post-synaptic potentials from cortical neurons in the brain.
- **Amplitude Range:** $10 \mu\text{V}$ to $100 \mu\text{V}$ (extremely weak, heavily attenuated by the skull).
- **Frequency Band:** $0.5 \text{ Hz}$ to $100 \text{ Hz}$.
- **Key Features:** Rhythmic oscillatory bands (Delta, Theta, Alpha, Beta, Gamma).
- **Challenges:** Eye blinks (Electrooculogram or EOG artifacts), scalp muscle contractions (EMG artifacts), and severe baseline drift.

#### 4.1.3 Electromyogram (EMG)
- **Origin:** Electrical activity produced by skeletal muscles during contraction (motor unit action potentials).
- **Amplitude Range:** $0.1 \text{ mV}$ to $10 \text{ mV}$.
- **Frequency Band:** $10 \text{ Hz}$ to $500 \text{ Hz}$ (bulk of energy between 50-150 Hz).
- **Key Features:** Looks like stochastic, amplitude-modulated noise; analyzed via envelopes and spectral properties.
- **Challenges:** Crosstalk from adjacent muscles, movement artifacts.

#### 4.1.4 Photoplethysmogram (PPG)
- **Origin:** Optical measurement of volumetric changes in blood circulation at the skin surface.
- **Amplitude Range:** Arbitrary optical units (depends on sensor).
- **Frequency Band:** $0.5 \text{ Hz}$ to $5 \text{ Hz}$.
- **Key Features:** AC component corresponding to heart rate, DC component corresponding to respiration and thermoregulation.
- **Challenges:** Extremely susceptible to motion artifacts (ambient light changes, sensor movement).

### 4.2 ECG Processing Pipeline and Anatomy

A diagnostic ECG trace consists of the P-wave, QRS complex, and T-wave. Extracting these requires addressing specific noise sources.

#### 4.2.1 Baseline Wander Removal
Baseline wander is a low-frequency drift primarily caused by the patient's breathing (respiration modulates the impedance of the chest cavity). The typical frequency of human respiration is 0.15 to 0.3 Hz.
- **Filter Design:** We use a High-Pass Filter (HPF) with a cutoff frequency ($f_c$) of $0.5 \text{ Hz}$.
- **Phase constraint:** It is critical to use a linear phase FIR filter or apply zero-phase forward-backward IIR filtering (`filtfilt` in software) so that the relative timing of the P, QRS, and T waves is not distorted. Phase distortion can lead to misdiagnosis of ST-segment elevation.

#### 4.2.2 Powerline Interference Removal
Mains electricity radiates 50 Hz (or 60 Hz in the US) electromagnetic fields that couple into the human body and the electrode cables.
- **Filter Design:** A narrow Notch filter centered exactly at $50 \text{ Hz}$. The design involves placing zeros precisely on the unit circle at the 50 Hz digital frequency, and poles slightly inside the unit circle to narrow the notch bandwidth, minimizing damage to the ECG spectrum (since the QRS complex has significant energy around 10-20 Hz, but ECG extends up to 150 Hz).

### 4.3 Pan-Tompkins QRS Detection Algorithm

The Pan-Tompkins algorithm reliably detects the QRS complex (the heartbeat) under heavy noise. It consists of five sequential stages.

#### Stage 1: Bandpass Filtering
The purpose is to isolate the energy of the QRS complex and attenuate the P and T waves, baseline wander, and high-frequency muscle noise.
- The optimal bandpass range for the QRS complex is roughly **5 Hz to 15 Hz**.
- This maximizes the Signal-to-Noise Ratio (SNR) for the QRS complex.

#### Stage 2: Differentiation
The QRS complex is characterized by the steepest slopes in the ECG signal. The differentiator highlights these steep slopes.
$$ y[n] = \frac{1}{8T} \left( 2x[n] + x[n-1] - x[n-3] - 2x[n-4] \right) $$
- This is a 5-point derivative approximation that suppresses high-frequency noise amplification compared to a simple $x[n]-x[n-1]$ difference.

#### Stage 3: Squaring
The differentiated signal has both positive and negative peaks (due to the rising and falling edges of the QRS).
$$ y[n] = (x[n])^2 $$
- **Why?** It makes all data points positive (point-by-point rectification) and non-linearly amplifies the larger slopes (the QRS) while suppressing smaller slopes (P and T waves or noise).

#### Stage 4: Moving-Window Integration
The squaring operation often results in multiple fragmented peaks for a single QRS complex.
$$ y[n] = \frac{1}{N} \sum_{k=0}^{N-1} x[n-k] $$
- The window width $N$ is chosen to be roughly the width of the widest possible normal QRS complex (approximately 150 ms).
- This operation "smears" or "lumps" the fragmented peaks into a single, smooth, unified hump representing the entire QRS complex.

#### Stage 5: Adaptive Thresholding
A static threshold fails because ECG amplitudes vary significantly over time and between patients.
- The algorithm maintains two running estimates: the **Signal Peak** level ($SPK$) and the **Noise Peak** level ($NPK$).
- When a new peak is found, the threshold is dynamically calculated, e.g., $Threshold = NPK + 0.25(SPK - NPK)$.
- If a peak exceeds the threshold, it is classified as a QRS complex, and $SPK$ is updated. Otherwise, it is classified as noise, and $NPK$ is updated.

### 4.4 Heart Rate Variability (HRV) Analysis

Extracting the time intervals between successive QRS peaks (RR intervals) allows us to analyze HRV. HRV is a powerful non-invasive tool to assess the Autonomic Nervous System (ANS).

#### 4.4.1 Time-Domain Metrics
- **SDNN (Standard Deviation of NN intervals):** Reflects overall variability. Lower SDNN indicates higher stress or cardiac risk.
- **RMSSD (Root Mean Square of Successive Differences):**
  $$ RMSSD = \sqrt{\frac{1}{N-1} \sum_{i=1}^{N-1} (RR_{i+1} - RR_i)^2} $$
  Primarily reflects parasympathetic (vagal) tone.
- **pNN50:** The percentage of successive RR intervals that differ by more than 50 ms.
- **NN50:** The number of pairs of successive NNs that differ by more than 50 ms.

#### 4.4.2 Frequency-Domain Metrics (Welch PSD)
The RR interval time series is unevenly sampled. We interpolate it to a uniform grid (e.g., 4 Hz) and compute the Power Spectral Density (PSD).
- **VLF (Very Low Frequency):** $< 0.04 \text{ Hz}$. Related to thermoregulation and hormonal factors.
- **LF (Low Frequency):** $0.04 \text{ Hz}$ to $0.15 \text{ Hz}$. Reflects both sympathetic and parasympathetic activity (often tied to blood pressure regulation/baroreceptors).
- **HF (High Frequency):** $0.15 \text{ Hz}$ to $0.4 \text{ Hz}$. Reflects purely parasympathetic (vagal) activity, largely driven by respiration (Respiratory Sinus Arrhythmia).
- **LF/HF Ratio:** A crucial metric representing the "Sympathovagal Balance" (balance between the fight-or-flight and rest-and-digest systems).

**Clinical Significance:** High HRV indicates a healthy, adaptable heart. Low HRV is a predictor of mortality post-myocardial infarction and is associated with chronic stress. Erratic, completely irregular RR intervals are the primary diagnostic marker for Atrial Fibrillation (AFib).

### 4.5 EEG Signal Processing

The EEG signal is a superposition of millions of neuronal firings. We decompose it into frequency bands.

#### 4.5.1 Frequency Bands and Cognitive Correlates
- **Delta ($\delta$, $0.5-4 \text{ Hz}$):** Dominant in deep, restorative sleep.
- **Theta ($\theta$, $4-8 \text{ Hz}$):** Drowsiness, meditation, light sleep.
- **Alpha ($\alpha$, $8-13 \text{ Hz}$):** Relaxed wakefulness. Prominent over the occipital lobe when eyes are closed. Attenuates when eyes open.
- **Beta ($\beta$, $13-30 \text{ Hz}$):** Active, busy, or anxious thinking and active concentration.
- **Gamma ($\gamma$, $>30 \text{ Hz}$):** High-level cognitive processing, sensory binding.

#### 4.5.2 Artifact Removal
- **EOG and EMG Contamination:** Eye movements generate massive electrical potentials (EOG) that bleed into frontal EEG channels. Jaw clenching generates massive EMG noise across all channels.
- **Independent Component Analysis (ICA):** A blind source separation technique. It assumes the EEG signals are linear mixtures of statistically independent brain sources and artifact sources. ICA decomposes the multi-channel EEG into independent components. Components representing eye blinks (typically characterized by distinct topographical maps and low-frequency pulses) can be manually or automatically zeroed out before reconstructing the clean EEG.

#### 4.5.3 Common Spatial Patterns (CSP) for BCI
In Brain-Computer Interfaces (like motor imagery, where a user imagines moving their left vs. right hand), we use CSP. CSP finds spatial filters (linear combinations of electrodes) that maximize the variance of the signal for one class (left hand) while minimizing it for the other (right hand), making classification highly accurate.

### 4.6 EMG Signal Processing

EMG reflects muscle recruitment. It is highly stochastic.

#### 4.6.1 Time-Domain Features
- **RMS (Root Mean Square):** Represents the power of the muscle contraction.
- **MAV (Mean Absolute Value):** Used heavily in prosthetic control.
- **ZC (Zero Crossings) & SSC (Slope Sign Changes):** Provide a rough estimate of frequency content and muscle motor unit firing rates without needing heavy FFT calculations.

#### 4.6.2 Frequency-Domain and Muscle Fatigue
- **Median Frequency (MDF) and Mean Power Frequency (MNF).**
- **Muscle Fatigue Principle (Spectral Compression):** As a muscle fatigues during sustained isometric contraction, the conduction velocity of action potentials along the muscle fibers decreases. Furthermore, different motor unit types recruit differently. This causes the entire power spectrum to compress and shift towards lower frequencies.
- **DSP Application:** Tracking the continuous decline of the Median Frequency over time is the standard non-invasive method for quantifying localized muscle fatigue.

#### 4.6.3 EMG-Controlled Prosthetics
Pattern recognition algorithms (like SVMs or Neural Networks) take windows of EMG (e.g., 200 ms), extract features (RMS, ZC, AR coefficients), and classify the intended movement (grasp, pinch, wrist extension) to drive a bionic hand.

### 4.7 Digital Stethoscope and Phonocardiogram (PCG)

The PCG records acoustic heart sounds.
- **S1 ("Lub"):** Closure of mitral and tricuspid valves. Occurs at the onset of ventricular systole (aligns with the QRS complex). Frequency range: 10-140 Hz.
- **S2 ("Dub"):** Closure of aortic and pulmonary valves. End of systole. Frequency range: 10-400 Hz.
- **S3 & S4:** Pathological heart sounds (gallops). Very low frequency (20-70 Hz). Indicate heart failure or stiff ventricles.
- **Filtering Requirements:** A digital stethoscope must selectively amplify these specific bands. A bell mode (low frequency) focuses on S3/S4, while a diaphragm mode (higher frequency) listens for murmurs.

---
## 5. COMPLETE PROOFS AND DERIVATIONS

### 5.1 Design and Derivation of the IIR Notch Filter

To remove a specific noise frequency $f_0$ (e.g., 50 Hz) given a sampling rate $f_s$, we map this to the digital frequency domain:
$$ \omega_0 = 2\pi \frac{f_0}{f_s} $$

**Step 1: Pole-Zero Placement**
To completely eliminate the frequency $\omega_0$, we place a pair of complex conjugate zeros exactly on the unit circle at angles $\pm \omega_0$:
$$ z_1 = e^{j\omega_0}, \quad z_2 = e^{-j\omega_0} $$
This ensures the magnitude response $H(e^{j\omega_0}) = 0$.

However, a filter with only zeros (an FIR filter) will have a very wide notch, severely attenuating neighboring frequencies. To narrow the notch, we place a pair of complex conjugate poles at the exact same angles, but slightly inside the unit circle, at a radius $r < 1$:
$$ p_1 = r e^{j\omega_0}, \quad p_2 = r e^{-j\omega_0} $$

**Step 2: Deriving the Transfer Function**
The transfer function $H(z)$ is formed by the ratio of the zero polynomials to the pole polynomials. To ensure unity gain at DC ($\omega = 0, z = 1$), a normalization constant $K$ is sometimes added, but we'll focus on the core structure:
$$ H(z) = \frac{(z - z_1)(z - z_2)}{(z - p_1)(z - p_2)} $$
$$ H(z) = \frac{(z - e^{j\omega_0})(z - e^{-j\omega_0})}{(z - r e^{j\omega_0})(z - r e^{-j\omega_0})} $$
Expanding the numerator:
$$ (z - e^{j\omega_0})(z - e^{-j\omega_0}) = z^2 - z(e^{j\omega_0} + e^{-j\omega_0}) + 1 $$
Using Euler's identity: $e^{j\omega_0} + e^{-j\omega_0} = 2\cos(\omega_0)$:
$$ \text{Numerator} = z^2 - 2\cos(\omega_0)z + 1 $$
Expanding the denominator similarly:
$$ (z - r e^{j\omega_0})(z - r e^{-j\omega_0}) = z^2 - r z(e^{j\omega_0} + e^{-j\omega_0}) + r^2 $$
$$ \text{Denominator} = z^2 - 2r\cos(\omega_0)z + r^2 $$

Dividing numerator and denominator by $z^2$ to express in terms of delays ($z^{-1}$):
$$ H(z) = \frac{1 - 2\cos(\omega_0)z^{-1} + z^{-2}}{1 - 2r\cos(\omega_0)z^{-1} + r^2 z^{-2}} $$

**Step 3: Relationship between Pole Radius and Notch Width**
We evaluate the frequency response by setting $z = e^{j\omega}$. For frequencies close to the notch $\omega \approx \omega_0$, let $\omega = \omega_0 \pm \Delta\omega / 2$, where $\Delta\omega$ is the 3-dB bandwidth.
The distance from the unit circle to the pole is approximately $1 - r$.
Geometrically, the 3-dB point occurs when the distance to the zero is $\sqrt{2}$ times the distance to the pole.
For high-Q filters (where $r$ is close to 1), it can be shown that the 3-dB bandwidth (in radians/sample) is heavily dominated by the pole distance:
$$ \Delta\omega \approx 2(1 - r) $$
Alternatively, expressed in Hertz:
$$ BW_{-3\text{dB}} \approx \frac{1 - r}{\pi} f_s $$
**Proof conclusion:** As $r \rightarrow 1$, the bandwidth $\Delta\omega \rightarrow 0$. The notch becomes infinitely sharp. However, if $r=1$, the poles cancel the zeros, and the filter does nothing. If $r>1$, the filter is unstable. Furthermore, a sharper notch (larger $r$) results in a longer impulse response, leading to severe ringing artifacts in the time domain when impulsive signals (like a QRS complex) pass through.

---
## 6. WORKED EXAMPLES (MINIMUM 5 — fully solved)

### Example 1: IIR Notch Filter Design for 50 Hz Powerline Interference
**Problem statement:** 
Design a second-order IIR digital notch filter to eliminate 50 Hz interference from an ECG signal sampled at $f_s = 500 \text{ Hz}$. Choose a pole radius of $r = 0.9$ to provide a balance between notch width and transient ringing. Determine the difference equation.

**Solution:**
1. **Find Digital Frequency:**
   $$ \omega_0 = 2\pi \frac{f_0}{f_s} = 2\pi \frac{50}{500} = 0.2\pi \text{ rad/sample} $$
2. **Calculate Trigonometric Coefficient:**
   $$ \cos(\omega_0) = \cos(0.2\pi) = 0.8090 $$
3. **Determine Numerator Coefficients ($b_k$):**
   $$ b_0 = 1 $$
   $$ b_1 = -2\cos(\omega_0) = -2(0.8090) = -1.6180 $$
   $$ b_2 = 1 $$
4. **Determine Denominator Coefficients ($a_k$):**
   $$ a_0 = 1 $$
   $$ a_1 = -2r\cos(\omega_0) = -2(0.9)(0.8090) = -1.4562 $$
   $$ a_2 = r^2 = (0.9)^2 = 0.81 $$
5. **Construct Transfer Function:**
   $$ H(z) = \frac{1 - 1.6180z^{-1} + z^{-2}}{1 - 1.4562z^{-1} + 0.81z^{-2}} $$
6. **Formulate Difference Equation:**
   $$ Y(z)(1 - 1.4562z^{-1} + 0.81z^{-2}) = X(z)(1 - 1.6180z^{-1} + z^{-2}) $$
   Taking the Inverse Z-Transform:
   $$ y[n] - 1.4562y[n-1] + 0.81y[n-2] = x[n] - 1.6180x[n-1] + x[n-2] $$
   $$ y[n] = 1.4562y[n-1] - 0.81y[n-2] + x[n] - 1.6180x[n-1] + x[n-2] $$

**Physical interpretation:** The output relies heavily on past outputs (IIR nature), allowing an infinite impulse response that sharply cancels the 50 Hz oscillation without significantly dampening the 15 Hz QRS components.
**Common mistakes to avoid:** Forgetting that $\omega_0$ must be in radians (not degrees) when calculating cosine in programming languages (C/Python/MATLAB).

### Example 2: Analyzing the Pan-Tompkins Moving Window Integrator
**Problem statement:** 
An ECG signal is sampled at $200 \text{ Hz}$. According to the Pan-Tompkins algorithm, the moving window integrator should be roughly 150 ms wide. Calculate the number of samples $N$ required for the window and write the difference equation in its recursive, computationally efficient form.

**Solution:**
1. **Determine Window Size $N$:**
   $$ \text{Time width} = 150 \text{ ms} = 0.15 \text{ seconds} $$
   $$ N = \text{Time width} \times f_s = 0.15 \times 200 = 30 \text{ samples} $$
2. **Standard Moving Average Equation:**
   $$ y[n] = \frac{1}{30} \sum_{k=0}^{29} x[n-k] $$
3. **Derive Recursive Form for Efficiency:**
   $$ y[n] = \frac{1}{30} (x[n] + x[n-1] + \dots + x[n-29]) $$
   $$ y[n-1] = \frac{1}{30} (x[n-1] + x[n-2] + \dots + x[n-30]) $$
   Subtracting $y[n-1]$ from $y[n]$:
   $$ y[n] - y[n-1] = \frac{1}{30} (x[n] - x[n-30]) $$
   $$ y[n] = y[n-1] + \frac{1}{30} (x[n] - x[n-30]) $$

**Physical interpretation:** This is a low-pass filter. The recursive form drastically reduces the number of additions from 29 per sample to just 2, making it ideal for low-power microcontrollers in wearable ECG patches.
**Common mistakes to avoid:** Implementing the summation naively in a loop inside an interrupt service routine, which causes massive latency.

### Example 3: HRV Frequency Domain Analysis - LF/HF Ratio
**Problem statement:** 
A patient undergoes a stress test. Welch's PSD estimate of their RR interval time series yields the following absolute power values: VLF = $400 \text{ ms}^2$, LF = $800 \text{ ms}^2$, HF = $200 \text{ ms}^2$. Calculate the LF/HF ratio and interpret the sympathovagal balance. What physiological state does this suggest?

**Solution:**
1. **Identify Relevant Bands:**
   LF power = $800 \text{ ms}^2$
   HF power = $200 \text{ ms}^2$
2. **Calculate Ratio:**
   $$ \text{LF/HF Ratio} = \frac{\text{LF}}{\text{HF}} = \frac{800}{200} = 4.0 $$

**Physical interpretation:** A normal resting LF/HF ratio is typically between 1.0 and 2.0. An LF/HF ratio of 4.0 implies profound sympathetic dominance. This perfectly aligns with a patient undergoing a stress test, as the "fight or flight" response is activated, increasing heart rate and shifting variability power into the low-frequency band.
**Common mistakes to avoid:** Including the VLF power when calculating the ratio, or failing to realize that these powers are often expressed in normalized units (nu) to account for total variance.

### Example 4: EMG Median Frequency Shift during Fatigue
**Problem statement:** 
During a 60-second sustained bicep curl, the power spectrum of the surface EMG signal is analyzed in 2-second windows. In the first window, the spectrum $P(f)$ is uniform between 50 Hz and 150 Hz and zero elsewhere. In the final window, due to fatigue, the spectrum compresses and is uniform between 30 Hz and 90 Hz. Calculate the Median Frequency (MDF) for both windows and prove it has decreased.

**Solution:**
1. **Understand Median Frequency:**
   The MDF is the frequency that divides the power spectrum into two regions of equal area:
   $$ \int_{0}^{\text{MDF}} P(f) df = \int_{\text{MDF}}^{\infty} P(f) df $$
2. **Window 1 (Initial State):**
   Uniform spectrum from 50 to 150 Hz. Since it's a rectangle, the median is exactly in the middle.
   $$ \text{MDF}_1 = \frac{50 + 150}{2} = 100 \text{ Hz} $$
3. **Window 2 (Fatigued State):**
   Uniform spectrum from 30 to 90 Hz.
   $$ \text{MDF}_2 = \frac{30 + 90}{2} = 60 \text{ Hz} $$
4. **Conclusion:**
   The MDF shifted from 100 Hz down to 60 Hz. 

**Physical interpretation:** The decrease in median frequency quantitatively proves the physiological onset of localized muscle fatigue, caused by a decrease in muscle fiber conduction velocity as lactic acid builds up.
**Common mistakes to avoid:** Confusing Median Frequency with Mean Frequency. For skewed real-world EMG spectra, MDF is generally preferred as it is less sensitive to high-frequency noise tails.

### Example 5: 60 Hz Notch Filter Bandwidth Calculation
**Problem statement:** 
An EEG system in the USA suffers from 60 Hz interference. The sampling rate is 256 Hz. A notch filter is designed with pole radius $r = 0.98$. Calculate the 3-dB bandwidth of the resulting notch in Hertz.

**Solution:**
1. **Use the Bandwidth Approximation Formula:**
   $$ \Delta\omega \approx 2(1 - r) \text{ radians/sample} $$
2. **Substitute $r$:**
   $$ \Delta\omega = 2(1 - 0.98) = 2(0.02) = 0.04 \text{ radians/sample} $$
3. **Convert radians/sample to Hertz:**
   $$ \Delta f = \frac{\Delta\omega}{2\pi} \times f_s $$
   $$ \Delta f = \frac{0.04}{2\pi} \times 256 = \frac{10.24}{2\pi} \approx \frac{10.24}{6.283} \approx 1.63 \text{ Hz} $$

**Physical interpretation:** The notch rejects frequencies strictly between approximately 59.18 Hz and 60.82 Hz. This is a very sharp, surgical filter, leaving the critical Gamma band EEG activity (which can span 30-100 Hz) largely intact.
**Common mistakes to avoid:** Using the formula blindly for low $r$ values. The approximation $\Delta\omega \approx 2(1 - r)$ only holds true for high-Q filters where $r \rightarrow 1$.

### Example 6: QRS Detection Trace Through PT Algorithm
**Problem statement:**
Consider a synthetic sampled signal representing a raw QRS spike contaminated with high-frequency noise: $x[n] = [0.1, -0.2, 2.0, -1.8, 0.3]$. Trace this signal through the Pan-Tompkins differentiator and squaring steps. Assume a sampling time $T=1$ for simplicity and ignore previous states.
**Solution:**
1. **Differentiation (simplified as $x[n] - x[n-1]$ to illustrate the point):**
   $y_{diff}[0] = 0.1$
   $y_{diff}[1] = -0.2 - 0.1 = -0.3$
   $y_{diff}[2] = 2.0 - (-0.2) = 2.2$
   $y_{diff}[3] = -1.8 - 2.0 = -3.8$
   $y_{diff}[4] = 0.3 - (-1.8) = 2.1$
2. **Squaring:**
   $y_{sq}[n] = (y_{diff}[n])^2$
   $y_{sq}[0] = (0.1)^2 = 0.01$
   $y_{sq}[1] = (-0.3)^2 = 0.09$
   $y_{sq}[2] = (2.2)^2 = 4.84$
   $y_{sq}[3] = (-3.8)^2 = 14.44$
   $y_{sq}[4] = (2.1)^2 = 4.41$
**Physical Interpretation:** The small noisy variations (0.1, -0.2) yield extremely small squared outputs (0.01, 0.09), while the large steep slope of the QRS (-3.8) yields a massive peak (14.44). The signal-to-noise ratio has been drastically improved.

### Example 7: Signal-to-Noise Ratio (SNR) in ECG
**Problem statement:**
An ECG signal has a peak QRS amplitude of 1.5 mV. It is corrupted by a 50 Hz powerline interference with a peak amplitude of 0.15 mV. Calculate the SNR in decibels (dB) before filtering, assuming both are roughly sinusoidal for power calculations.
**Solution:**
1. **Signal Power:**
   $P_{sig} = \frac{(A_{sig} / \sqrt{2})^2}{R} \propto A_{sig}^2 = (1.5)^2 = 2.25$
2. **Noise Power:**
   $P_{noise} = \frac{(A_{noise} / \sqrt{2})^2}{R} \propto A_{noise}^2 = (0.15)^2 = 0.0225$
3. **SNR (dB):**
   $SNR = 10 \log_{10} \left( \frac{P_{sig}}{P_{noise}} \right)$
   $SNR = 10 \log_{10} \left( \frac{2.25}{0.0225} \right) = 10 \log_{10}(100)$
   $SNR = 10 \times 2 = 20 \text{ dB}$
**Physical Interpretation:** A 20 dB SNR means the signal power is 100 times stronger than the noise power. While this sounds good, in clinical diagnostics where tiny variations matter, 20 dB is often insufficient and requires filtering.

---
## 7. ENGINEERING APPLICATIONS AND CASE STUDIES

**Case Study 1: Smartwatch Atrial Fibrillation Detection**
Modern smartwatches utilize PPG sensors on the wrist. Because PPG is heavily corrupted by arm swinging (motion artifacts in the 1-2 Hz range, which perfectly overlaps the heart rate), DSP is critical. 
*Implementation:* The watch uses a 3-axis accelerometer as a noise reference. An Adaptive Filter (like the LMS or RLS algorithm) dynamically subtracts the motion frequencies from the PPG signal. The cleaned PPG is then processed to extract peak-to-peak intervals. If the Poincare plot of these intervals exhibits high dispersion (irregular irregularity), the device flags potential Atrial Fibrillation.

**Case Study 2: Bionic Prosthetics via Surface EMG**
Targeted Muscle Reinnervation (TMR) patients have residual nerves grafted to chest muscles. Surface EMG electrodes record the signals.
*Implementation:* The embedded DSP samples 8 channels at 1000 Hz. Every 50 ms, it extracts the Mean Absolute Value (MAV) and 4th-order Autoregressive (AR) coefficients. These features are fed into a Linear Discriminant Analysis (LDA) classifier to determine if the patient wants to open or close the robotic hand. The processing pipeline must have a total latency of $< 200 \text{ ms}$ to avoid the user perceiving a lag.

**Case Study 3: Fetal ECG Extraction**
Extracting fetal ECG from maternal abdominal sensors is a classic DSP problem.
*Implementation:* The maternal ECG is roughly 10 times stronger than the fetal ECG. DSP engineers use spatial filtering or Adaptive Interference Cancellation. The maternal ECG is recorded clearly on the chest (reference signal). Abdominal signals contain a mix of maternal and fetal ECGs. An adaptive filter estimates the maternal component in the abdomen and subtracts it, leaving only the tiny fetal QRS complexes, which are then passed through a Pan-Tompkins algorithm to monitor fetal distress.

**Case Study 4: Automated Sleep Staging from EEG**
Polysomnography requires classifying patient sleep stages (N1, N2, N3, REM) using EEG. 
*Implementation:* The EEG is analyzed in 30-second epochs. A filter bank decomposes the signal into Delta, Theta, Alpha, and Beta bands. The relative band power is calculated. High Delta power triggers an N3 (deep sleep) classification, while high Theta and random eye movements (via EOG) trigger REM sleep classification. 

**Case Study 5: Hearing Aids and Cochlear Implants**
DSP is the heart of modern audiological devices.
*Implementation:* A cochlear implant takes environmental audio, runs it through a 22-channel digital filter bank (mimicking the basilar membrane), extracts the envelope of each channel using a rectifier and LPF, and uses those envelopes to stimulate the auditory nerve with biphasic electrical pulses.

---
## 8. COMMON STUDENT MISCONCEPTIONS AND ERRORS

1. **Misconception: "An FIR filter is always better for biomedical signals because it is always stable."**
   *Correction:* While FIR filters are unconditionally stable and can be designed with exactly linear phase (crucial for preserving ECG wave shapes), they require extremely high orders (hundreds of taps) to achieve narrow transition bands (like for a 50 Hz notch). This creates unacceptable computational delay and memory usage in real-time embedded systems. IIR filters are often necessary for low-latency narrow notches, despite their non-linear phase.

2. **Misconception: "High Frequency (HF) in HRV means the heart is beating faster."**
   *Correction:* HRV frequencies describe the oscillation of the *intervals* between beats, not the heart rate itself. High Frequency (HF) power actually corresponds to the parasympathetic nervous system (Vagal tone), which generally *slows down* the average heart rate. High HF power implies the heart is highly responsive to respiration (Respiratory Sinus Arrhythmia), a sign of health.

3. **Misconception: "Squaring the signal in Pan-Tompkins is just to make the values positive (absolute value)."**
   *Correction:* If the goal was merely to make values positive, we would just use the absolute value $|x[n]|$. Squaring $x[n]^2$ is a *non-linear amplification*. It aggressively amplifies the large values (the steep slopes of the QRS complex) while severely attenuating the small values (the slopes of P and T waves, and random noise). This expands the dynamic range between signal and noise, making thresholding much easier.

4. **Misconception: "A notch filter removes powerline noise without any side effects."**
   *Correction:* A causal IIR notch filter introduces phase distortion around the notch frequency. Furthermore, if the notch is too sharp ($r$ very close to 1), it behaves like an oscillator. When a sharp transient (like a QRS peak) hits the filter, it causes "ringing" or "ringing artifacts" at the notch frequency, which can distort the ST-segment—a critical diagnostic marker for heart attacks.

5. **Misconception: "EMG signals are deterministic and can be analyzed looking at individual spikes."**
   *Correction:* Unlike the ECG, which is highly deterministic and repeating, surface EMG is a stochastic, interference pattern resulting from the asynchronous firing of hundreds of motor units. It must be treated as a random signal. Information is extracted by looking at its variance (power), envelope, or spectral moments, not by tracking individual peaks.

6. **Misconception: "Zero-phase filtering can be used in real-time patient monitors."**
   *Correction:* Zero-phase filtering (like MATLAB's `filtfilt`) requires passing the signal forward, then reversing the entire signal in time and passing it backward. This is non-causal. It requires the entire signal to be recorded first, making it impossible to use in strict real-time monitoring where the system must react instantly to a heartbeat.

7. **Misconception: "All artifacts in EEG can simply be filtered out."**
   *Correction:* Artifacts like eye blinks (EOG) and muscle movements (EMG) often span a wide frequency range (0-100 Hz), completely overlapping with the signal of interest (Delta to Gamma waves). Simple frequency filtering will destroy the underlying EEG. Advanced spatial filtering (like ICA) is required to separate the statistically independent sources without destroying frequency content.

---
## 9. CONNECTIONS TO OTHER LECTURES

* **Builds upon:** 
  * Lecture 12 (Z-transform and Pole-Zero Analysis): Essential for notch filter design.
  * Lecture 18 (FIR vs IIR Filter Design): Understanding the trade-offs between phase linearity and computational efficiency.
  * Lecture 22 (Power Spectral Density Estimation): Required for understanding HRV and EMG frequency domain features.
* **Sets up for:**
  * Lecture 32 (Adaptive Filtering): How to remove noise when the noise frequency is unknown or changing (e.g., motion artifacts in wearable PPG).
  * Lecture 35 (DSP in Machine Learning): How features extracted via these pipelines (like EMG RMS or EEG Band Power) are fed into classifiers for BCI and prosthetics.

---
## 10. EXAMINATION QUESTIONS

### 10.1 Short Answer (5 questions with model answers)
**Q1: What is the primary purpose of the moving-window integration step in the Pan-Tompkins algorithm?**
*Answer:* The squaring and differentiation steps often produce multiple fragmented peaks for a single QRS complex. The moving-window integrator acts as a smoothing low-pass filter that "lumps" these fragments together into a single, unified waveform, allowing a simple threshold to detect exactly one peak per heartbeat.

**Q2: List the standard EEG frequency bands from lowest to highest frequency and state one cognitive state associated with the Alpha band.**
*Answer:* Delta, Theta, Alpha, Beta, Gamma. The Alpha band (8-13 Hz) is associated with a state of relaxed wakefulness, typically with the eyes closed.

**Q3: Explain the concept of "spectral compression" in the context of EMG analysis.**
*Answer:* During sustained muscle contraction, muscle fatigue occurs. This causes a decrease in the conduction velocity of muscle fiber action potentials. In the frequency domain, this manifests as spectral compression, where the entire power spectrum shifts toward lower frequencies, measurable as a drop in the median frequency.

**Q4: Why is the LF/HF ratio calculated in HRV analysis?**
*Answer:* The LF (Low Frequency) band reflects both sympathetic and parasympathetic activity, while the HF (High Frequency) band reflects purely parasympathetic activity. The LF/HF ratio serves as an index of the "sympathovagal balance" or the overall balance of the autonomic nervous system.

**Q5: What is the difference between S1 and S3 heart sounds in a phonocardiogram?**
*Answer:* S1 is a normal, relatively high-frequency sound caused by the closure of the mitral and tricuspid valves during systole. S3 is a pathological, very low-frequency "gallop" sound occurring early in diastole, often indicating congestive heart failure.

### 10.2 Long Answer / Numerical Problems (6 problems with complete solutions)
**Problem 1: Notch Filter Difference Equation**
Derive the complete difference equation for a digital notch filter designed to remove 60 Hz noise at a sampling rate of 600 Hz, with a pole radius $r=0.95$.
*Solution:*
$\omega_0 = 2\pi(60)/600 = 0.2\pi$.
$\cos(0.2\pi) = 0.8090$.
$b_0 = 1, b_1 = -2(0.8090) = -1.618, b_2 = 1$.
$a_0 = 1, a_1 = -2(0.95)(0.8090) = -1.5371, a_2 = 0.95^2 = 0.9025$.
Transfer function: $H(z) = \frac{1 - 1.618z^{-1} + z^{-2}}{1 - 1.5371z^{-1} + 0.9025z^{-2}}$.
Difference Eq: $y[n] = 1.5371y[n-1] - 0.9025y[n-2] + x[n] - 1.618x[n-1] + x[n-2]$.

**Problem 2: QRS Integrator Window Sizing**
An embedded ECG monitor samples at $f_s = 250 \text{ Hz}$. A patient has an abnormally wide QRS complex due to a bundle branch block, lasting 180 ms. Calculate the optimal number of taps $N$ for the moving-window integrator in the Pan-Tompkins algorithm to accommodate this.
*Solution:*
Time width $T = 0.180 \text{ seconds}$.
Number of samples $N = T \times f_s = 0.180 \times 250$.
$N = 45 \text{ samples}$.
The filter requires a 45-tap moving average.

**Problem 3: Differentiator Frequency Response**
The Pan-Tompkins derivative is $y[n] = \frac{1}{8T}(2x[n] + x[n-1] - x[n-3] - 2x[n-4])$. Find its Z-transform and prove it acts as a high-pass filter by evaluating the DC gain.
*Solution:*
Taking Z-transform: $Y(z) = \frac{1}{8T}(2 + z^{-1} - z^{-3} - 2z^{-4})X(z)$.
$H(z) = \frac{1}{8T}(2 + z^{-1} - z^{-3} - 2z^{-4})$.
Evaluate DC gain by setting $\omega = 0$, thus $z = e^{j0} = 1$.
$H(1) = \frac{1}{8T}(2 + 1 - 1 - 2) = \frac{1}{8T}(0) = 0$.
Because the gain at DC ($0 \text{ Hz}$) is exactly zero, it acts as a high-pass (or band-pass) filter, rejecting baseline wander.

**Problem 4: HRV Analysis Calculation**
Given the following successive RR intervals in seconds: [0.8, 0.9, 1.0, 0.8]. Calculate the mean RR, SDNN, and RMSSD.
*Solution:*
Mean RR = $(0.8 + 0.9 + 1.0 + 0.8) / 4 = 3.5 / 4 = 0.875 \text{ s}$.
Differences ($RR_{i+1} - RR_i$): $0.1, 0.1, -0.2$.
Squared diffs: $0.01, 0.01, 0.04$.
Sum of squared diffs = $0.06$.
RMSSD = $\sqrt{0.06 / 3} = \sqrt{0.02} \approx 0.141 \text{ s}$.
SDNN requires standard deviation of intervals. Variance = $[(0.8-0.875)^2 + (0.9-0.875)^2 + (1.0-0.875)^2 + (0.8-0.875)^2] / 3$.
Variance = $[0.005625 + 0.000625 + 0.015625 + 0.005625] / 3 = 0.0275 / 3 = 0.00916$.
SDNN = $\sqrt{0.00916} \approx 0.0957 \text{ s}$.

**Problem 5: Zero Placement for 50Hz and 100Hz Rejection**
Design the numerator of an FIR filter that perfectly rejects both 50 Hz and 100 Hz interference for an ECG sampled at 400 Hz.
*Solution:*
1. Frequencies in rad/sample:
   $\omega_1 = 2\pi(50)/400 = 0.25\pi$
   $\omega_2 = 2\pi(100)/400 = 0.5\pi$
2. Zeros required on unit circle:
   $z_1, z_2 = e^{\pm j0.25\pi}$
   $z_3, z_4 = e^{\pm j0.5\pi} = \pm j$
3. First pair polynomial:
   $(z - e^{j0.25\pi})(z - e^{-j0.25\pi}) = z^2 - 2\cos(0.25\pi)z + 1 = z^2 - \sqrt{2}z + 1$
4. Second pair polynomial:
   $(z - j)(z + j) = z^2 + 1$
5. Combined Numerator:
   $N(z) = (z^2 - \sqrt{2}z + 1)(z^2 + 1) = z^4 - \sqrt{2}z^3 + 2z^2 - \sqrt{2}z + 1$

**Problem 6: pNN50 Calculation**
A 10-second ECG recording yields the following 9 RR intervals (in ms): [800, 820, 890, 840, 810, 810, 870, 930, 900]. Calculate the pNN50 metric.
*Solution:*
1. Calculate differences between adjacent intervals:
   $820-800 = 20$
   $890-820 = 70$
   $840-890 = -50$
   $810-840 = -30$
   $810-810 = 0$
   $870-810 = 60$
   $930-870 = 60$
   $900-930 = -30$
2. Find absolute differences:
   [20, 70, 50, 30, 0, 60, 60, 30]
3. Count differences strictly > 50 ms (NN50):
   70, 60, 60. Total NN50 = 3.
4. Calculate total number of differences: 8.
5. Calculate percentage (pNN50):
   $pNN50 = (3 / 8) \times 100\% = 37.5\%$

### 10.3 True/False with Justification (6 items)
1. **T/F: An IIR notch filter with $r=0.99$ will have less time-domain ringing than one with $r=0.90$.**
   *False.* A higher $r$ means the poles are closer to the unit circle, resulting in a higher Q-factor, sharper notch, and inherently longer impulse response, which causes *more* ringing.
2. **T/F: In Pan-Tompkins, the differentiation step removes the P and T waves.**
   *False.* It attenuates them relative to the QRS complex because P and T waves have lower slopes (lower frequencies), but it does not completely remove them; the thresholding step does the final isolation.
3. **T/F: LF/HF ratio increases during physical exercise.**
   *True.* Exercise activates the sympathetic nervous system (fight or flight), increasing LF power relative to HF power.
4. **T/F: EEG Beta waves are predominantly seen during deep sleep.**
   *False.* Delta waves are seen in deep sleep. Beta waves indicate active, alert thinking.
5. **T/F: The Median Frequency of an EMG signal decreases as the muscle fatigues.**
   *True.* Due to spectral compression and lowered conduction velocity of action potentials.
6. **T/F: A digital High-Pass Filter with a cutoff of 0.5 Hz is used to remove powerline interference in ECG.**
   *False.* A 0.5 Hz HPF is used to remove baseline wander (respiration artifacts). A notch filter at 50/60 Hz removes powerline interference.

---
## 11. KEY FORMULAS REFERENCE

| Concept | Formula | Notes |
|---------|---------|-------|
| Digital Frequency | $\omega_0 = 2\pi \frac{f_0}{f_s}$ | Radians per sample |
| Notch Filter Zeros | $z_{1,2} = e^{\pm j\omega_0}$ | Placed on unit circle |
| Notch Filter Poles | $p_{1,2} = r e^{\pm j\omega_0}$ | $r < 1$ defines bandwidth |
| Notch Transfer Fn. | $H(z) = \frac{1 - 2\cos(\omega_0)z^{-1} + z^{-2}}{1 - 2r\cos(\omega_0)z^{-1} + r^2 z^{-2}}$ | Canonical form |
| Notch 3-dB BW | $\Delta\omega \approx 2(1 - r)$ | Valid for $r \rightarrow 1$ |
| PT Differentiator | $y[n] = \frac{1}{8T} (2x[n] + x[n-1] - x[n-3] - 2x[n-4])$ | Pan-Tompkins 5-point |
| Moving Window Int. | $y[n] = \frac{1}{N} \sum_{k=0}^{N-1} x[n-k]$ | Smoothes squared signal |
| Recursive Int. | $y[n] = y[n-1] + \frac{1}{N}(x[n] - x[n-N])$ | Efficient implementation |
| RMSSD (HRV) | $\sqrt{\frac{1}{N-1} \sum_{i=1}^{N-1} (RR_{i+1} - RR_i)^2}$ | Time domain parasympathetic index |

---
## 12. FURTHER READING AND REFERENCES

1. **Rangayyan, R. M. (2015).** *Biomedical Signal Analysis: A Case-Study Approach.* IEEE Press. (Primary text for this module, particularly Chapters 3 and 4 on filtering and QRS detection. Highly recommended for students pursuing capstone projects in this area).
2. **Pan, J., & Tompkins, W. J. (1985).** *A Real-Time QRS Detection Algorithm.* IEEE Transactions on Biomedical Engineering, BME-32(3), 230-236. (The foundational paper - mandatory reading for embedded DSP projects. Shows the original empirical justification for the filter choices).
3. **Proakis, J. G., & Manolakis, D. K. (2006).** *Digital Signal Processing: Principles, Algorithms, and Applications.* 4th Ed. Pearson. (Chapter 10 for IIR filter design specifics, particularly the pole-zero placement method).
4. **Task Force of the European Society of Cardiology and the North American Society of Pacing and Electrophysiology (1996).** *Heart rate variability: standards of measurement, physiological interpretation and clinical use.* Circulation, 93(5), 1043-1065. (The definitive guide to HRV metrics, standardization of VLF, LF, HF bands).
5. **Oppenheim, A. V., & Schafer, R. W. (2010).** *Discrete-Time Signal Processing.* 3rd Ed. Pearson. (Reference for moving average filter frequency response and phase properties).
6. **Sörnmo, L., & Laguna, P. (2005).** *Bioelectrical Signal Processing in Cardiac and Neurological Applications.* Academic Press. (Advanced text covering EEG artifact removal via ICA and detailed EMG spectral analysis).
7. **Haykin, S. (2013).** *Adaptive Filter Theory.* 5th Ed. Pearson. (Useful for the upcoming adaptive filtering lectures related to fetal ECG extraction and wearable PPG motion artifact cancellation).

**End of Faculty Reference Notes.**

---
## 13. APPENDIX: LABORATORY EXPERIMENT IDEAS
- **Lab 1: ECG Filter Design:** Students capture raw ECG data, implement the 50/60 Hz notch and 0.5 Hz HPF in MATLAB, and observe the ST segment distortion with different Q-factors.
- **Lab 2: Real-time Pan-Tompkins:** Students implement the Pan-Tompkins algorithm on a microcontroller (e.g., STM32) and verify QRS detection accuracy against a known database (like MIT-BIH).
- **Lab 3: EMG Fatigue Analysis:** Using an AD8226 INA, students record their own bicep EMG during a prolonged hold, compute the spectrogram, and write a script to track the falling Median Frequency over time.

---
## 14. GLOSSARY OF TERMS
- **ANS:** Autonomic Nervous System, regulating involuntary bodily functions.
- **BCI:** Brain-Computer Interface, a direct communication pathway between a brain and an external device.
- **EOG:** Electrooculogram, a measurement of the resting potential of the retina.
- **Q-Factor:** Quality factor of a filter, describing how under-damped an oscillator or resonator is.
- **Sympathovagal Balance:** The relative level of activity of the sympathetic and parasympathetic branches of the ANS.
</Faculty Notes — Lecture 28: Biomedical Signal Processing>
