<Faculty Notes — Lecture 29: Radar DSP>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY

This lecture introduces students to the digital signal processing techniques that make modern radar systems possible. 
Radar represents one of the most compelling applications of DSP.
It synthesizes concepts from system theory.
It utilizes Fourier analysis.
It requires detection theory.
It involves probability theory.
It implements discrete-time filtering.

**How to teach this lecture:**
Start by grounding the students in the physical reality of the problem.
The problem is distinguishing a tiny, noise-corrupted electromagnetic echo from a target amidst massive amounts of thermal noise.
It also involves environmental clutter.
The mathematical transition from continuous-time electromagnetic waves propagating in free space to discrete-time baseband signals residing in a digital memory buffer can be jarring for many students. 
It is critical to emphasize that all modern digital processing happens at baseband. 
The RF front-end merely serves to translate the spectrum down to a frequency where our analog-to-digital converters (ADCs) can effectively operate. 

Spend significant time on the concept of Pulse Compression. 
It is mathematically beautiful.
It is practically vital. 
Use the "time-bandwidth product" as a recurring theme. 
The idea that we can decouple range resolution from transmit energy is one of the greatest triumphs of signal processing. 

When moving to range-Doppler processing, draw a physical 2D matrix on the board. 
Make sure they understand that rows are range bins.
These are sampled in fast time.
They are sampled at tens or hundreds of megahertz.
Columns are pulses.
These are sampled in slow time.
They are sampled at the PRF.
This is typically in kilohertz.
The transition from a 1D time series to a 2D matrix is a conceptual leap.

**Common student difficulties:**
1. **Fast Time vs. Slow Time:** 
This is notoriously confusing. 
Students struggle to understand that we are sampling a continuous signal (fast time).
We are also organizing those samples across multiple pulse repetition intervals (slow time). 
The dual time-scales must be explicitly defined.
They must be repeatedly referenced.

2. **Phase as Velocity:** 
The idea that a microscopic change in range manifests as a measurable phase shift across pulses is non-intuitive. 
Students often think of velocity as $v = d/t$.
They think in terms of macroscopic distance measurements. 
In Doppler radar, velocity is measured via phase rotation.
This is given by $\Delta \phi = 4\pi v T_r / \lambda$.

3. **Ambiguity Function:** 
The mathematics of the 2D correlation function often overwhelms the physical interpretation. 
It defines resolution limits.

4. **CFAR Statistics:** 
The derivation of the CFAR threshold relies on probability theory.
It uses exponential distributions.
It uses chi-squared distributions.
Students who are weak in probability will struggle with the CA-CFAR derivation.

**Suggested Demos:**
- **Audio chirp demonstration:** 
Play an audio chirp.
Show its spectrogram.
Show the cross-correlation of the chirp with a delayed version of itself. 
This makes pulse compression audible and visible.

- **Visualizing the Range-Doppler matrix:** 
Use MATLAB or Python to plot a raw Range-Slow Time matrix.
This looks like noise initially.
Then apply a 2D FFT.
This reveals a sharp peak corresponding to a target.

- **FMCW Audio Demo:** 
Mix an audio chirp with a delayed version of itself.
You will hear a constant tone. 
The pitch of this tone corresponds to the delay. 
This perfectly illustrates the FMCW beat frequency concept.

---
## 1. LEARNING OBJECTIVES

By the end of this comprehensive lecture and corresponding study session, students will be able to:

1. **Derive and apply** the fundamental radar equations relating range, time delay, Doppler shift, velocity, and basic electromagnetic propagation.
2. **Analyze** the matched filter output for a Linear Frequency Modulated (LFM) chirp.
3. **Prove** its mathematically optimal SNR properties in Additive White Gaussian Noise (AWGN).
4. **Calculate** the processing gain (Time-Bandwidth Product).
5. **Construct** a 2D Range-Doppler data matrix from sequential radar pulses.
6. **Explain** the sequential discrete Fourier processing required to simultaneously extract target range and velocity.
7. **Evaluate** the ambiguity function mathematically and graphically for different transmit waveforms (LFM, continuous wave, Barker codes).
8. **Interpret** the range-Doppler coupling phenomenon.
9. **Formulate** the threshold for Cell-Averaging Constant False Alarm Rate (CA-CFAR) detection from first probabilistic principles.
10. **Differentiate** between CA, SO, GO, and OS CFAR variants in heterogeneous clutter environments.
11. **Design** digital Moving Target Indicator (MTI) filters using Z-domain analysis.
12. **Plot** their frequency responses.
13. **Calculate** radar blind speeds given a specific Pulse Repetition Frequency (PRF).
14. **Explain** the physical and mathematical mechanics of FMCW and SAR radar systems.
15. **Compute** key parameters like the FMCW beat frequency and the SAR theoretical azimuth resolution limit.

---
## 2. PREREQUISITE KNOWLEDGE REVIEW

Before starting this lecture, students must be extremely comfortable with the following mathematical and DSP concepts. 
A brief 5-minute review is highly recommended.

- **Complex Baseband Representation:** 
Real passband signals $x(t) = A(t)\cos(2\pi f_c t + \phi(t))$ are universally processed as complex baseband signals.
The representation is $\tilde{x}(t) = A(t)e^{j\phi(t)}$. 
This complex notation simplifies the math of frequency shifts.
It simplifies phase modulations.

- **Matched Filtering Theorem:** 
To maximize the Signal-to-Noise Ratio (SNR) of a known signal in Additive White Gaussian Noise (AWGN).
The optimal receiver filter impulse response must be the time-reversed, complex-conjugated version of the transmitted signal.
The impulse response is $h(t) = s^*(-t)$. 
The output is the autocorrelation of $s(t)$.

- **Fourier Transform Properties:** 
Specifically, the time-shifting property is essential.
It is given by $\mathcal{F}\{x(t-\tau)\} = X(f)e^{-j2\pi f \tau}$. 
A delay in time is a linear phase shift in frequency.

- **Discrete Fourier Transform (DFT) and FFT:** 
Used to transition from the discrete-time domain to the discrete-frequency domain efficiently. 

- **Z-Transforms for Filter Design:** 
Difference equations and transfer functions $H(z)$. 
Specifically, placing zeros on the unit circle to create notch filters.

- **Random Variables and Probability:** 
Basic understanding of probability density functions (PDFs). 
The square-law detector output (power) of complex Gaussian noise follows an exponential distribution.
This is a special case of the Chi-squared distribution.

---
## 3. HISTORICAL AND MOTIVATIONAL CONTEXT

The origins of radar trace back to the late 19th century.
Heinrich Hertz demonstrated that radio waves could be reflected by metallic objects. 
However, operational radar was developed just before and during World War II. 
Sir Robert Watson-Watt's pivotal work in the United Kingdom led to the Chain Home early warning system.
This was absolutely critical in securing air superiority during the Battle of Britain.

**Why does an Electrical and Electronics Engineering (EEE) student need to study radar?**
Originally, radar was exclusively the domain of microwave engineers.
It involved electromagnetics specialists.
It relied on analog hardware designers. 
Processing was done using analog delay lines.
It used cathode ray tubes.
It used immense physical filters. 

However, the modern radar paradigm has shifted entirely. 
Today's radar is fundamentally a Digital Signal Processing system. 
The antennas, amplifiers, and RF front-ends merely exist to down-convert the electromagnetic waves.
They convert them into a stream of complex numbers (I and Q samples). 
The core functionality is implemented entirely in software.
This includes detecting targets.
It includes measuring velocity.
It includes filtering clutter.
It includes tracking and imaging.
This is done in software (C/C++, Python) or firmware (FPGAs/ASICs) using discrete-time DSP algorithms.

**Real Engineering Applications and Industry Relevance:**

1. **Automotive Advanced Driver Assistance Systems (ADAS):** 
77 GHz FMCW radars are standard equipment in modern vehicles.
They are used for adaptive cruise control.
They are used for blind-spot monitoring.
They are used for automatic emergency braking. 
Understanding this is crucial for the automotive sector.

2. **Air Traffic Control (ATC):** 
Heavy-duty Pulse-Doppler radars track commercial aircraft across the globe.
They ensure safe separation.

3. **Meteorology and Weather Monitoring:** 
Doppler weather radars map precipitation intensity.
They detect tornadic wind signatures.
They measure the Doppler shift of falling rain droplets.

4. **Earth Observation (SAR):** 
Satellites utilize Synthetic Aperture Radar to map terrain topographies.
They track deforestation.
They measure soil moisture.
They monitor polar ice sheets. 
SAR provides high-resolution imaging regardless of cloud cover, weather, or time of day.

5. **Defense and Aerospace:** 
Phased array radars on fighter jets and naval vessels perform simultaneous target tracking.
They guide missiles.
They conduct electronic warfare.

---
## 4. THEORETICAL FOUNDATIONS

### 4.1 Radar Fundamentals and the Core Radar Equations

The fundamental principle of radar operation involves the transmission of an electromagnetic wave pulse.
It involves the reception of its echo from a distant object.

**The Monostatic Radar Range Equation:**

The power received $P_r$ from a target is derived directly from the geometry of spherical electromagnetic wave propagation.
It depends on the target's physical reflectivity (Radar Cross Section, denoted as $\sigma$).

- The transmitter outputs power $P_t$.
- This power is concentrated by a directional antenna with gain $G$. 
- Assuming free-space propagation, the power density at a range $R$ spreads out over the surface area of a sphere $4\pi R^2$. 
- Thus, power density at the target is $\frac{P_t G}{4\pi R^2}$.
- The target intercepts a portion of this power and re-radiates it. 
- This is quantified by the target's Radar Cross Section (RCS), $\sigma$. 
- The target acts as a secondary isotropic radiator.
- The reflected power density returning to the radar at range $R$ is $\frac{P_t G \sigma}{(4\pi R^2)(4\pi R^2)}$.
- The receiving antenna collects this power.
- It uses an effective aperture area $A_e = \frac{G \lambda^2}{4\pi}$.
- Combining all these terms yields the fundamental monostatic radar equation:
$$ P_r = \frac{P_t G^2 \lambda^2 \sigma}{(4\pi)^3 R^4} $$

This equation shows the extreme $1/R^4$ penalty for range. 
To double the detection range, the transmitted power must be increased by a factor of 16!

**Range Measurement and Range Resolution:**

The time delay $\tau$ of the received echo is directly proportional to the round-trip distance $2R$ traversed by the pulse:
$$ R = \frac{c\tau}{2} $$
where $c$ is the speed of light in a vacuum ($3 \times 10^8$ m/s).

Range resolution, denoted $\delta R$, dictates the radar's ability to distinguish two closely spaced targets on the same bearing. 
Two targets can be independently resolved only if their echoes do not overlap in time. 
For a simple rectangular pulse of duration $\tau_p$, the echoes will overlap if the targets are closer than $c\tau_p/2$. 

Since the bandwidth $B$ of a simple unmodulated rectangular pulse is approximately $1/\tau_p$, we arrive at the critical relationship:
$$ \delta R = \frac{c}{2B} $$
This shows that finer range resolution strictly requires wider signal bandwidth.

**Maximum Unambiguous Range ($R_{max}$):**

A pulsed radar transmits a continuous sequence of pulses at a specific rate called the Pulse Repetition Frequency (PRF), denoted $f_r$. 
The time interval between consecutive pulses is the Pulse Repetition Interval (PRI), $T_r = 1/f_r$. 

If an echo from an extremely distant target arrives after the *next* pulse has already been transmitted, the radar processor cannot inherently tell which transmitted pulse generated the echo. 
This creates a severe range ambiguity. 
The maximum distance a target can be located to ensure its echo arrives before the next pulse transmission is:
$$ R_{max} = \frac{c T_r}{2} = \frac{c}{2 \text{PRF}} $$

**Doppler Frequency Shift:**

For a target moving with absolute velocity $v$ at an angle $\theta$ relative to the radar's line-of-sight, the radial velocity component is $v_r = v \cos(\theta)$. 

This relative motion changes the round-trip path length continuously. 
Over a short time interval $t$, the path length changes by $2v_r t$. 
This microscopic change in distance causes a macroscopic shift in the phase of the received carrier wave. 
The rate of change of this phase is the Doppler frequency shift:
$$ f_d = -\frac{1}{2\pi} \frac{d\phi}{dt} = \frac{2v_r}{\lambda} $$
A target moving towards the radar (positive closing velocity) produces a positive Doppler shift.
A target moving away produces a negative Doppler shift.

### 4.2 Pulse Compression and the Linear Frequency Modulated (LFM) Chirp

A fundamental conflict exists in basic radar design:
1. To achieve long detection ranges, we need high transmitted energy. 
Since peak power is limited by hardware (amplifiers will arc or burn out), we must use a long pulse duration $T$.
2. To achieve fine range resolution, we need high bandwidth $B$. 
For an unmodulated pulse, $B \approx 1/T$, requiring a very short pulse.

Pulse compression solves this dilemma.
It modulates the phase or frequency of a long pulse. 
This increases its bandwidth independently of its duration.

**The LFM Chirp Waveform:**

The most common pulse compression waveform is the Linear Frequency Modulated (LFM) chirp. 
The complex baseband equation is:
$$ s(t) = \text{rect}\left(\frac{t}{T}\right) \exp(j\pi\mu t^2) $$
where $\mu = B/T$ is the chirp rate (Hz/sec). 

The instantaneous frequency of a signal is the time derivative of its phase divided by $2\pi$:
$$ f_{inst}(t) = \frac{1}{2\pi} \frac{d}{dt}(\pi \mu t^2) = \mu t = \frac{B}{T} t $$
This demonstrates that the frequency sweeps linearly over a total bandwidth $B$ during the pulse duration $T$.

**Matched Filtering and Processing Gain:**

To maximize the SNR, the received echo is passed through a matched filter. 
The filter's impulse response is $h(t) = s^*(-t)$. 
The output $y(t) = s(t) * h(t)$ is the deterministic autocorrelation of the signal.

For an LFM chirp, the matched filter output is a highly compressed sinc-like pulse. 
The width of this compressed main lobe (null-to-null) is approximately $2/B$.

The processing gain achieved by this compression is called the Time-Bandwidth Product (TBP):
$$ \text{TBP} = B \cdot T $$
This effectively improves the SNR by a factor equal to the TBP.
It allows long-range detection while simultaneously maintaining a fine resolution of $\delta R = c/(2B)$. 

### 4.3 Range-Doppler Processing (The 2D Matrix)

A modern radar operates by transmitting a coherent burst of $N$ pulses. 
The received analog signal is continuously sampled by an ADC.
It is organized in memory into a 2-Dimensional data matrix.

- **Fast Time (Rows):** The high-speed ADC samples taken within a single PRI. 
These correspond to individual range bins. 
Let there be $M$ samples per pulse, indexed by $m = 0, 1, \dots, M-1$.
- **Slow Time (Columns):** The pulse index. 
Each new pulse forms a new column in the matrix. 
Let there be $N$ pulses in the burst, indexed by $n = 0, 1, \dots, N-1$.

To extract target information, a 2D sequence of DSP operations is performed:
1. **Range Processing (Pulse Compression):** For each column (pulse), the fast-time samples are passed through a digital matched filter. 
This is almost always implemented using Fast Convolution via the FFT.
2. **Doppler Processing:** After pulse compression, if a target is present at range bin $m_0$, its complex amplitude will fluctuate across the $N$ slow-time samples (pulses) due to its Doppler phase shift. 
We extract this velocity by computing an $N$-point FFT across the slow-time dimension (along the row $m_0$).

Performing this slow-time FFT across every single range bin results in a comprehensive **Range-Doppler map**. 
In this 2D image, sharp peaks indicate the presence of targets.
They simultaneously reveal their absolute range and radial velocity.

### 4.4 The Ambiguity Function

The ambiguity function is an analytical tool.
It characterizes the output of the matched filter when there is a simultaneous mismatch in both time delay $\tau$ and Doppler frequency $f_d$. 
It defines the inherent resolution limits.
It defines self-interference properties of a specific waveform.
$$ |\chi(\tau, f_d)|^2 = \left| \int_{-\infty}^{\infty} s(t) s^*(t-\tau) e^{j2\pi f_d t} dt \right|^2 $$

- **Ideal Waveform (The "Thumbtack"):** 
The ideal ambiguity function would be an infinitely sharp spike at the origin $(0,0)$ and zero everywhere else. 
This would mean perfect range and Doppler resolution with zero interference. 
Pseudo-random noise (PRN) codes closely approximate this thumbtack shape.

- **LFM Chirp (The "Ridge" or "Sheared Knife-Edge"):** 
The LFM ambiguity function is heavily skewed along a diagonal. 
This means a target with a true Doppler shift will produce a peak that is offset in time delay. 
The radar will measure an incorrect range! 
This phenomenon is known as range-Doppler coupling.

- **Continuous Wave (CW) (The "Fan"):** 
An unmodulated CW signal has infinite duration. 
Its ambiguity function is an infinitely thin line along the Doppler axis. 
It has perfect Doppler resolution but absolute zero range resolution (infinite ambiguity).

### 4.5 Constant False Alarm Rate (CFAR) Detection

In a real radar system, the background interference is constantly changing.
This includes thermal noise.
It includes environmental clutter reflections.
If a simple fixed threshold is used for target detection, a slight increase in the noise floor will cause millions of false alarms.
This will crash the tracking computer. 
If the threshold is set too high, real targets will be missed.
CFAR dynamically and continuously adjusts the detection threshold based on an estimate of the local background power.

**Cell-Averaging CFAR (CA-CFAR):**

To decide if a target is present in a specific range bin (the Cell Under Test, or CUT), we estimate the local noise power.
We do this by averaging the power in $N$ surrounding reference cells. 
Guard cells are placed immediately adjacent to the CUT.
They are ignored to prevent a strong target's energy from leaking into the noise estimate.
This prevents raising the threshold against itself.

The CA-CFAR test statistic is:
$$ T_{stat} = \alpha \frac{1}{N} \sum_{i=1}^{N} x_i $$
where $x_i$ are the power samples in the reference cells.
$\alpha$ is a multiplier threshold factor strictly dependent on the desired probability of false alarm ($P_{fa}$):
$$ \alpha = N \left( P_{fa}^{-1/N} - 1 \right) $$
If the power in the CUT exceeds $T_{stat}$, a target detection is declared.

**CFAR Architectural Variants:**

- **SO-CFAR (Smallest-Of):** 
Calculates separate averages for the leading and lagging reference windows.
It uses the minimum of the two. 
This helps resolve two closely spaced targets that might otherwise mask each other.

- **GO-CFAR (Greatest-Of):** 
Uses the maximum of the leading and lagging windows. 
This performs very well at sudden clutter edges (e.g., transition from land to sea).
It prevents false alarms at the boundary.

- **OS-CFAR (Ordered-Statistic):** 
Sorts all $N$ reference cells by magnitude.
It selects the $k$-th largest value as the noise estimate. 
It does not average. 
This is highly robust in dense multi-target environments.
Interfering targets in the reference window simply occupy the highest sorted ranks.
They are ignored if $k$ is chosen correctly.

### 4.6 Moving Target Indicator (MTI) Clutter Filtering

MTI is a time-domain filtering technique.
It is used to remove massive, stationary clutter (mountains, buildings, ground) from the radar return.
This ensures that small moving targets (aircraft) can be seen.
Since stationary targets have zero Doppler shift (DC in the frequency domain), an MTI filter is essentially a digital high-pass filter applied across the slow-time samples.

**Basic MTI Implementations:**

- **2-pulse canceller:** 
Subtracts the current pulse from the previous pulse: 
$y[n] = x[n] - x[n-1]$. 
The Z-domain transfer function is $H(z) = 1 - z^{-1}$. 
This places a single zero at $z=1$ (DC, or zero velocity).

- **3-pulse canceller:** 
Cascades two 2-pulse cancellers to create a broader, deeper notch at DC: 
$y[n] = x[n] - 2x[n-1] + x[n-2]$. 
The transfer function is $H(z) = (1 - z^{-1})^2$.

**The Blind Speed Problem:**

Because the radar samples the environment discretely at the PRF, the slow-time signal is subject to the Nyquist sampling theorem. 
Frequencies above PRF/2 will alias. 
If a target is moving at a specific high velocity such that its Doppler shift is exactly equal to the PRF (or a multiple of it), it will alias down to exactly 0 Hz (DC). 
The MTI filter will assume it is stationary clutter.
It will completely cancel it!

These critical velocities are called blind speeds:
$$ v_{blind} = \frac{n \lambda \text{PRF}}{2}, \quad n = \pm 1, \pm 2, \pm 3, \dots $$

To mitigate blind speeds, advanced radars use staggered PRFs (transmitting pulses with alternating PRIs). 
This shifts the blind speeds dynamically so a target is never invisible on consecutive pulse bursts.

### 4.7 Frequency Modulated Continuous Wave (FMCW) Radar

FMCW radar breaks from the traditional pulsed model. 
It transmits continuously while simultaneously receiving.
To measure range, it transmits a continuously sweeping frequency waveform (a very long chirp). 
The received signal (delayed by $\tau$) is routed into an analog mixer alongside a copy of the currently transmitting signal. 
The mixer outputs the difference in frequency between the two, known as the **beat frequency** ($f_b$).

For a stationary target at range $R$, the time delay is $\tau = 2R/c$. 
Because the frequency sweeps linearly at a rate of $B/T$, the frequency difference at the mixer is exactly proportional to the time delay:
$$ f_b = \frac{B}{T} \tau = \frac{2 R B}{c T} $$

This maps the physical range of the target directly to a low-frequency audio tone. 
An ADC can sample this low-frequency beat signal very cheaply.
An FFT easily extracts the range peaks. 
This is the foundation of modern automotive radar.

### 4.8 Synthetic Aperture Radar (SAR) Principles

SAR is an imaging technique that exploits the physical motion of the radar platform (an aircraft or satellite).
It synthesizes an extraordinarily large antenna aperture mathematically.

The real azimuth (cross-range) resolution of a physical antenna of length $D$ is limited by diffraction: 
$\delta a_{real} = \frac{\lambda R}{D}$. 
For a satellite at 800km altitude, a 10m antenna gives an abysmal resolution of several kilometers.

However, as the platform flies, it continuously transmits and receives pulses.
It stores them in memory. 
By coherently integrating all the pulses collected over a flight distance $L$, the signal processor synthesizes a virtual antenna of length $L$.

The maximum distance $L$ over which a target remains illuminated by the physical antenna beam is $L_{max} = \frac{\lambda R}{D}$.
Substituting this maximum synthetic aperture length $L_{max}$ into the resolution equation yields the miraculous theoretical limit for SAR azimuth resolution:
$$ \delta a_{SAR} = \frac{D}{2} $$

This result is astonishing. 
The resolution is independent of range $R$ and wavelength $\lambda$. 
Furthermore, a *smaller* physical antenna yields *better* SAR resolution.
This is because a smaller antenna has a wider beam.
It illuminates the target for a longer time.
This allows the formation of a longer synthetic aperture!

---
## 5. COMPLETE PROOFS AND DERIVATIONS

### 5.1 Rigorous Derivation: Matched Filter Output for the LFM Chirp

Let the transmitted LFM signal be $s(t) = \text{rect}\left(\frac{t}{T}\right) \exp(j\pi\mu t^2)$. 
The matched filter output $y(t)$ is the autocorrelation of $s(t)$:
$$ y(t) = \int_{-\infty}^{\infty} s(\tau) s^*(\tau - t) d\tau $$

Assume for this derivation that $t > 0$ (the analysis for $t < 0$ is symmetric). 
The rectangular envelope $\text{rect}(t/T)$ restricts the signal to the interval $[-T/2, T/2]$. 
When multiplying $s(\tau)$ and $s^*(\tau - t)$, the limits of integration are defined by the overlapping region of the two rect functions, which is from $-T/2 + t$ to $T/2$.

Substituting the exponential phase terms:
$$ y(t) = \int_{-T/2+t}^{T/2} \exp(j\pi\mu \tau^2) \exp(-j\pi\mu (\tau - t)^2) d\tau $$

Expand the quadratic term in the second exponential:
$$ y(t) = \int_{-T/2+t}^{T/2} \exp(j\pi\mu \tau^2) \exp(-j\pi\mu (\tau^2 - 2\tau t + t^2)) d\tau $$

Notice that the $\tau^2$ terms perfectly cancel out:
$$ \exp(j\pi\mu \tau^2) \exp(-j\pi\mu \tau^2) = 1 $$

This leaves:
$$ y(t) = \int_{-T/2+t}^{T/2} \exp(j 2\pi\mu \tau t) \exp(-j\pi\mu t^2) d\tau $$

The term $\exp(-j\pi\mu t^2)$ is independent of the integration variable $\tau$ and can be pulled out:
$$ y(t) = \exp(-j\pi\mu t^2) \int_{-T/2+t}^{T/2} \exp(j 2\pi\mu \tau t) d\tau $$

This is a straightforward exponential integral:
$$ \int e^{a \tau} d\tau = \frac{e^{a \tau}}{a} $$
Where $a = j 2\pi\mu t$. 

Evaluating the definite integral:
$$ y(t) = \exp(-j\pi\mu t^2) \left[ \frac{\exp(j 2\pi\mu (T/2) t) - \exp(j 2\pi\mu (-T/2 + t) t)}{j 2\pi\mu t} \right] $$

For values of $t$ close to the peak (where $t \ll T$), we can approximate the lower limit $-T/2 + t \approx -T/2$. 
This simplifies the expression to:
$$ y(t) \approx \exp(-j\pi\mu t^2) \left[ \frac{\exp(j \pi\mu T t) - \exp(-j \pi\mu T t)}{j 2\pi\mu t} \right] $$

Applying Euler's identity, $\sin(x) = \frac{e^{jx}-e^{-jx}}{2j}$:
$$ y(t) \approx \exp(-j\pi\mu t^2) \frac{2j \sin(\pi \mu T t)}{j 2\pi\mu t} $$

Cancel the $2j$ terms and multiply numerator and denominator by $T$:
$$ y(t) = \exp(-j\pi\mu t^2) T \frac{\sin(\pi \mu T t)}{\pi \mu T t} $$

Since the chirp rate $\mu = B/T$, we substitute $\mu T = B$:
$$ y(t) = \exp(-j\pi\mu t^2) T \text{sinc}(B t) $$

Taking the magnitude, the phase term disappears:
$$ |y(t)| = T |\text{sinc}(B t)| $$

**Conclusion:** 
The peak magnitude of the compressed pulse is proportional to $T$. 
The shape is a sinc function. 
The first null of the sinc function occurs when the argument is $\pi$, so $\pi B t_{null} = \pi$, meaning $t_{null} = 1/B$. 
The total null-to-null width of the compressed main lobe is exactly $2/B$.

### 5.2 Rigorous Derivation: CA-CFAR Threshold Multiplier

Assume the receiver noise is complex Additive White Gaussian Noise (AWGN). 
After square-law detection (taking the magnitude squared), the noise power $x$ in each resolution cell follows an exponential probability density function:
$$ p(x) = \frac{1}{\mu_{noise}} \exp\left(-\frac{x}{\mu_{noise}}\right), \quad x \ge 0 $$
where $\mu_{noise}$ is the true mean noise power.

In CA-CFAR, we sum the power of $N$ independent reference cells: $Z = \sum_{i=1}^N x_i$. 
The sum of $N$ independent exponential random variables follows an Erlang distribution:
$$ p(Z) = \frac{Z^{N-1} \exp(-Z/\mu_{noise})}{\mu_{noise}^N (N-1)!} $$

The dynamic threshold is computed as $T_{th} = \alpha \frac{Z}{N}$. 
A false alarm occurs if the noise power in the Cell Under Test ($X_{CUT}$) randomly exceeds this dynamic threshold. 
The probability of false alarm $P_{fa}$ is the expected value of this occurring over all possible values of the random variable $Z$:
$$ P_{fa} = P(X_{CUT} > T_{th}) = \int_{0}^{\infty} p(Z) \left[ \int_{\alpha Z / N}^{\infty} p(x_{cut}) dx_{cut} \right] dZ $$

First, evaluate the inner integral (the probability that $X_{CUT}$ exceeds a specific threshold $\alpha Z / N$):
$$ \int_{\alpha Z / N}^{\infty} \frac{1}{\mu_{noise}} \exp\left(-\frac{x}{\mu_{noise}}\right) dx = \exp\left(-\frac{\alpha Z}{N \mu_{noise}}\right) $$

Now, substitute this back into the outer integral:
$$ P_{fa} = \int_{0}^{\infty} \frac{Z^{N-1} \exp(-Z/\mu_{noise})}{\mu_{noise}^N (N-1)!} \exp\left(-\frac{\alpha Z}{N \mu_{noise}}\right) dZ $$

Combine the exponential terms:
$$ P_{fa} = \int_{0}^{\infty} \frac{Z^{N-1}}{\mu_{noise}^N (N-1)!} \exp\left[-Z \left(\frac{1}{\mu_{noise}} + \frac{\alpha}{N\mu_{noise}}\right)\right] dZ $$

Let $c = \frac{1}{\mu_{noise}}\left(1 + \frac{\alpha}{N}\right)$. 
The integral of $Z^{N-1} e^{-cZ}$ from 0 to infinity is a known standard integral evaluating to $\frac{(N-1)!}{c^N}$.

Substituting this result:
$$ P_{fa} = \frac{1}{\mu_{noise}^N (N-1)!} \frac{(N-1)!}{\left[ \frac{1}{\mu_{noise}}\left(1 + \frac{\alpha}{N}\right) \right]^N} $$

The $\mu_{noise}^N$ and $(N-1)!$ terms perfectly cancel out, leaving a remarkably simple, noise-independent equation:
$$ P_{fa} = \frac{1}{\left(1 + \frac{\alpha}{N}\right)^N} $$

To find the required multiplier $\alpha$, we solve this algebraic equation:
$$ \left(1 + \frac{\alpha}{N}\right)^N = \frac{1}{P_{fa}} = P_{fa}^{-1} $$
$$ 1 + \frac{\alpha}{N} = P_{fa}^{-1/N} $$
$$ \alpha = N \left( P_{fa}^{-1/N} - 1 \right) $$

**Conclusion:** 
The threshold multiplier $\alpha$ depends ONLY on the number of reference cells $N$ and the desired $P_{fa}$. 
It is completely independent of the actual noise power $\mu_{noise}$. 
This is why it is called a *Constant* False Alarm Rate detector!

---
## 6. WORKED EXAMPLES (FULLY SOLVED)

### Example 1: Basic Radar Range and Resolution Geometry
**Problem statement:** 
A civilian air traffic control radar transmits a short unmodulated pulse with a bandwidth of 2 MHz and operates at a PRF of 1200 Hz. 
Calculate the inherent range resolution and the absolute maximum unambiguous detection range.

**Solution:**
1. Range Resolution calculation:
$$ \delta R = \frac{c}{2B} = \frac{3 \times 10^8 \text{ m/s}}{2 \times 2 \times 10^6 \text{ Hz}} = \frac{3 \times 10^8}{4 \times 10^6} = \frac{300}{4} = 75 \text{ meters} $$
2. Maximum Unambiguous Range calculation:
$$ R_{max} = \frac{c}{2 \text{PRF}} = \frac{3 \times 10^8 \text{ m/s}}{2 \times 1200 \text{ Hz}} = \frac{3 \times 10^8}{2400} = 125,000 \text{ meters} = 125 \text{ km} $$

**Physical interpretation:** 
The radar can distinguish two distinct aircraft only if they are separated by at least 75 meters in radial distance. 
It can track planes up to 125 km away without range folding/ambiguity.

**Common mistakes to avoid:** 
Forgetting the factor of 2 in the denominator, which accounts for the round-trip travel time of the electromagnetic wave.

### Example 2: Pulse Compression and Time-Bandwidth Product Gain
**Problem statement:** 
An advanced military tracking radar utilizes an LFM chirp waveform with a long pulse duration of $150 \mu s$ and a swept bandwidth of 100 MHz. 
Calculate the Time-Bandwidth Product (compression ratio) in dB, and the effective spatial length of the compressed pulse in meters.

**Solution:**
1. Time-Bandwidth Product:
$$ \text{TBP} = B \cdot T = (100 \times 10^6 \text{ Hz}) \cdot (150 \times 10^{-6} \text{ s}) = 15000 $$
2. TBP in Decibels:
$$ \text{Gain}_{dB} = 10 \log_{10}(15000) \approx 41.76 \text{ dB} $$
3. Effective compressed pulse length (null-to-null width in time):
$$ \tau_{comp} = \frac{2}{B} = \frac{2}{100 \times 10^6} = 20 \text{ ns} $$
4. Effective spatial length:
$$ L_{comp} = c \cdot \tau_{comp} = (3 \times 10^8) \cdot (20 \times 10^{-9}) = 6 \text{ meters} $$

**Physical interpretation:** 
The digital matched filter provides a massive processing gain of nearly 42 dB.
This drastically improves SNR and detection capability. 
The uncompressed $150 \mu s$ pulse stretches for 45 kilometers in free space! 
After processing, it is compressed down to an equivalent resolution cell of just 6 meters.

**Common mistakes to avoid:** 
Mixing up microseconds ($10^{-6}$) and milliseconds ($10^{-3}$), which leads to wildly incorrect TBP calculations.

### Example 3: FMCW Beat Frequency Mapping for Automotive Radar
**Problem statement:** 
A vehicle's adaptive cruise control employs a 77 GHz FMCW radar. 
It continuously sweeps a bandwidth of 500 MHz over a very short duration of $30 \mu s$. 
If the radar processor detects a strong beat frequency of $2.5$ MHz, what is the precise distance to the vehicle ahead?

**Solution:**
The beat frequency formula relates range to frequency:
$$ f_b = \frac{2 R B}{c T} $$
Rearrange to solve for Range $R$:
$$ R = \frac{f_b \cdot c \cdot T}{2 B} $$
Substitute the given values:
$$ R = \frac{(2.5 \times 10^6) \cdot (3 \times 10^8) \cdot (30 \times 10^{-6})}{2 \cdot (500 \times 10^6)} $$
$$ R = \frac{22500 \times 10^8}{1000 \times 10^6} = \frac{2.25 \times 10^{12}}{10^{9}} = 22.5 \text{ meters} $$

**Physical interpretation:** 
The vehicle ahead is exactly 22.5 meters away. 
A target at 22.5m produces a clean 2.5 MHz sine wave at the analog mixer output. 
An inexpensive ADC sampling at just a few MSPS can easily digitize this signal.
This entirely avoids the need for multi-GHz ADCs!

**Common mistakes to avoid:** 
Incorrectly using the carrier frequency (77 GHz) instead of the chirp sweep bandwidth (500 MHz) in the primary calculation.

### Example 4: MTI Filter Blind Speeds and PRF Selection
**Problem statement:** 
A pulse-Doppler weather radar operating at 2.8 GHz (S-band) utilizes a PRF of 1000 Hz. 
Calculate the lowest non-zero blind speed in km/h. 
If a storm cell is moving at exactly this speed, what will the radar operator see?

**Solution:**
1. Calculate the operating wavelength:
$$ \lambda = \frac{c}{f} = \frac{3 \times 10^8 \text{ m/s}}{2.8 \times 10^9 \text{ Hz}} \approx 0.107 \text{ meters} $$
2. Calculate the first blind speed ($n=1$):
$$ v_{blind} = \frac{1 \cdot \lambda \cdot \text{PRF}}{2} = \frac{0.107 \cdot 1000}{2} = 53.5 \text{ m/s} $$
3. Convert to km/h:
$$ v_{blind(km/h)} = 53.5 \cdot 3.6 = 192.6 \text{ km/h} $$

**Physical interpretation:** 
A severe storm system moving radially towards or away from the radar at exactly 192.6 km/h will produce a Doppler frequency shift of exactly 1000 Hz. 
Because the radar samples the signal at a PRF of 1000 Hz, this Doppler shift aliases perfectly down to 0 Hz (DC). 
The MTI filter will assume the storm is a stationary mountain and completely cancel it from the display! 
The operator will see nothing.

**Common mistakes to avoid:** 
Confusing the RF carrier frequency (2.8 GHz) with the PRF sampling rate (1000 Hz). 

### Example 5: CA-CFAR Threshold Determination
**Problem statement:** 
A naval radar receiver employs a Cell-Averaging CFAR detector utilizing 24 reference cells (12 leading, 12 lagging) to maintain a strict false alarm probability of $P_{fa} = 10^{-6}$. 
In a particular processing window, the mean noise power computed across the 24 reference cells is measured at 1.8 mW. 
What is the absolute detection threshold in mW for the Cell Under Test?

**Solution:**
1. Calculate the multiplier $\alpha$:
$$ \alpha = N \left( P_{fa}^{-1/N} - 1 \right) = 24 \left( (10^{-6})^{-1/24} - 1 \right) $$
$$ \alpha = 24 \left( 10^{6/24} - 1 \right) = 24 \left( 10^{0.25} - 1 \right) $$
Using a calculator, $10^{0.25} \approx 1.778$:
$$ \alpha \approx 24 \left( 1.778 - 1 \right) = 24 \cdot 0.778 = 18.672 $$
2. Calculate the absolute Threshold:
$$ T_{th} = \alpha \cdot \bar{P}_{noise} = 18.672 \cdot 1.8 \text{ mW} = 33.61 \text{ mW} $$

**Physical interpretation:** 
To guarantee that only one in a million noise samples triggers a false alarm, the required detection threshold must be dynamically set to nearly 19 times the local average noise power. 
In this specific instant, any target return in the CUT exceeding 33.61 mW is officially declared a valid detection.

**Common mistakes to avoid:** 
A frequent student error is assuming $\alpha$ multiplies the *sum* of the reference cells, rather than the *mean average* power of the reference cells.

---
## 7. ENGINEERING APPLICATIONS AND CASE STUDIES

**Case Study 1: The Automotive Radar Revolution (ADAS)**
Modern autonomous and semi-autonomous cars rely heavily on 77 GHz FMCW radars. 
- *System Parameters:* Bandwidth = 1 GHz, Sweep time = $20 \mu s$, Output Power = 10 mW. 
- *Engineering Rationale:* Why not use pulsed radar? 
At 77 GHz, a pulsed radar would require unfeasibly high peak transmitter power.
It would need this to overcome the immense free-space path loss and provide sufficient SNR. 
FMCW solves this by transmitting continuously.
This allows the use of very low-power, cheap solid-state amplifiers. 
Furthermore, digitizing a 1 GHz bandwidth pulsed signal requires multi-Gigasample-per-second (GSPS) ADCs.
These are prohibitively expensive and power-hungry for a car battery. 
FMCW maps this enormous 1 GHz bandwidth down to a beat frequency of a few MHz.
This can be digitized by incredibly cheap, low-power audio-grade ADCs. 
This DSP architecture made mass-market radar a reality.

**Case Study 2: Spaceborne Synthetic Aperture Radar (Sentinel-1 Satellite)**
The European Space Agency's Sentinel-1 satellite carries an advanced C-band SAR system for continuous global Earth observation.
- *System Parameters:* Orbital Altitude $\approx 700$ km, Velocity $\approx 7.5$ km/s, Physical Antenna length $D = 12$ meters.
- *DSP Analysis:* If this satellite operated as a standard real-aperture radar, the beam footprint on the ground would be determined by diffraction: $\approx \lambda R / D$. 
At C-band ($\lambda = 5.5$ cm) and 700km range, the resolution would be roughly 3.2 kilometers! 
This is useless for detailed mapping. 
However, by storing hundreds of thousands of pulses in a massive memory buffer and applying heavy 2D complex DSP filtering, the satellite synthesizes a virtual antenna kilometers long. 
The theoretical azimuth resolution limit plunges to exactly $D/2 = 6$ meters. 
This miraculous DSP reduction allows high-resolution imaging of urban environments, ship tracking, and agricultural monitoring from the vacuum of space, regardless of cloud cover.

---
## 8. COMMON STUDENT MISCONCEPTIONS AND ERRORS

1. **Misconception:** "A longer transmitted pulse provides better range resolution because it inherently contains more total energy to reflect off the target."
   *Correct Explanation:* Total energy determines the maximum detection range and the Signal-to-Noise Ratio (SNR). 
   However, *bandwidth* strictly dictates range resolution. 
   A longer unmodulated pulse actually *worsens* resolution because its bandwidth is inversely proportional to its length. 
   Pulse compression via DSP is absolutely required to decouple these two parameters.

2. **Misconception:** "The Doppler frequency shift is caused by a change in the physical propagation speed of the electromagnetic wave."
   *Correct Explanation:* Electromagnetic waves *always* travel at the speed of light $c$, regardless of target motion. 
   The Doppler shift is a change in the *frequency* (and phase) of the received wave.
   It is caused by the continuously changing path distance compressing or stretching the wave cycles over time.

3. **Misconception:** "Taking an FFT of the received radar pulse directly tells us the target's range."
   *Correct Explanation:* This is highly context-dependent! 
   For standard pulsed radar, applying an FFT over fast-time is simply an efficient way to implement convolution for the matched filter. 
   To get velocity, you must FFT over slow-time. 
   Only in FMCW radar systems does an FFT directly extract absolute range by isolating beat frequencies.

4. **Misconception:** "Implementing a CFAR algorithm magically increases the radar's Signal-to-Noise Ratio (SNR)."
   *Correct Explanation:* CFAR processing does not improve SNR in any way. 
   In fact, due to the statistical variance in estimating the noise floor from a limited number of reference cells, CFAR actually suffers a small performance penalty called "CFAR Loss." 
   Its true purpose is to dynamically adapt the threshold to maintain a constant false alarm rate when facing heterogeneous, wildly changing environmental clutter, preventing the tracking computer from freezing.

5. **Misconception:** "In SAR imaging, building a physically larger satellite antenna will provide sharper image resolution."
   *Correct Explanation:* This intuition is true for optical telescopes and real-aperture radars, but completely backward for SAR! 
   In SAR, a *smaller* physical antenna yields a wider beamwidth. 
   A wider beam illuminates a target on the ground for a much longer period of time as the satellite flies over. 
   This allows the DSP to collect more pulses and synthesize a much *larger* virtual aperture, ultimately resulting in *better* resolution!

6. **Misconception:** "An MTI filter effectively cancels all stationary objects and perfectly preserves all moving targets."
   *Correct Explanation:* While an MTI filter places a deep notch at 0 Hz (DC) to cancel stationary objects, Nyquist sampling ensures this notch repeats at every multiple of the PRF. 
   Targets moving at these "blind speeds" will perfectly alias to DC and be completely canceled by the filter, disappearing from the radar screen entirely.

7. **Misconception:** "The Ambiguity Function measures how confused the radar operator gets."
   *Correct Explanation:* The Ambiguity Function is a strict mathematical property of the chosen transmit waveform. 
   It defines the absolute theoretical limits of how well the matched filter can simultaneously resolve a target's range and velocity, and how much interference a target will cause to adjacent bins.

---
## 9. CONNECTIONS TO OTHER LECTURES

- **Builds on Lecture 14 (Z-Transforms and Difference Equations):** 
Z-domain analysis is used extensively in analyzing, plotting, and designing MTI clutter filter responses.
It gives insight into blind speed suppression.

- **Builds on Lecture 19 (DFT/FFT and Fast Convolution):** 
The computationally intensive FFT is the absolute backbone of 2D Range-Doppler matrix processing.
It is required for digital matched filtering. 
Without fast convolution, modern radar would not exist in real-time.

- **Sets up future courses:** 
This lecture provides the critical foundation for senior-level and graduate courses in Statistical Signal Processing.
It prepares students for Detection and Estimation Theory.
It is required for advanced Adaptive Array Processing (such as Space-Time Adaptive Processing, STAP).

---
## 10. EXAMINATION QUESTIONS

### 10.1 Short Answer (Model Answers Provided)
**Q1:** Explain the fundamental engineering dilemma that necessitates the use of pulse compression waveforms in modern radar.
*Model Answer:* There is a strict conflict between maximum detection range (which requires long, high-energy pulses to maximize SNR) and fine range resolution (which requires short, wide-bandwidth pulses). 
Pulse compression resolves this by phase/frequency modulating a long pulse, thereby decoupling the signal's bandwidth from its time duration.

**Q2:** Clearly differentiate between the concepts of "fast time" and "slow time" in a coherent radar data matrix.
*Model Answer:* Fast time refers to the high-speed ADC sampling that occurs within a single pulse repetition interval (PRI); it directly corresponds to target range. 
Slow time refers to the sampling across successive pulses (at the PRF rate); it is used to observe pulse-to-pulse phase changes to determine target velocity (Doppler).

**Q3:** Describe the phenomenon of range-Doppler coupling in a Linear Frequency Modulated (LFM) waveform.
*Model Answer:* Because the frequency of an LFM chirp sweeps linearly over time, a Doppler frequency shift caused by a moving target is mathematically indistinguishable from a simple time delay. 
Consequently, the matched filter will output a peak at an incorrect time delay, causing the radar to report an erroneous range for the moving target.

**Q4:** In a dense clutter environment, why might a Cell-Averaging CFAR (CA-CFAR) detector fail at abrupt clutter edges (e.g., a coastline)?
*Model Answer:* At a clutter edge, the reference window will be partially filled with high-power clutter (land) and partially with low-power noise (sea). 
If the CUT is in the low-power region, the average will be artificially raised by the high-power cells, masking real targets. 
Conversely, if the CUT is in the high-power region, the average is dragged down, causing massive false alarms. 
GO-CFAR or OS-CFAR must be used instead.

**Q5:** Why do modern Pulse-Doppler MTI radars utilize staggered Pulse Repetition Frequencies (PRFs)?
*Model Answer:* To mitigate the severe problem of blind speeds. 
By systematically varying the PRI between pulse bursts, the radar changes its sampling rate. 
This shifts the velocity at which aliasing occurs. 
A target velocity that is "blind" and canceled during one PRF burst will likely be visible and detected during the next burst.

### 10.2 Long Answer / Numerical Problems (Fully Solved)
**Problem 1:** A sophisticated LFM pulsed radar operates at an X-band frequency of 10 GHz with a steady PRF of 2 kHz. 
The transmitted pulse width is $50 \mu s$ and the LFM chirp bandwidth is 10 MHz. 
a) Calculate the absolute maximum unambiguous range of the system.
b) Calculate the inherent range resolution provided by the chirp.
c) Calculate the DSP time-bandwidth product.

*Model Solution:* 
a) $R_{max} = \frac{c}{2\text{PRF}} = \frac{3\times 10^8}{2 \times 2000} = \frac{3\times 10^8}{4000} = 75,000 \text{ m} = 75 \text{ km}$. 
b) $\delta R = \frac{c}{2B} = \frac{3\times 10^8}{2 \times (10 \times 10^6)} = \frac{3\times 10^8}{20 \times 10^6} = 15 \text{ meters}$.
c) $TBP = B \times T = (10\times 10^6 \text{ Hz}) \times (50\times 10^{-6} \text{ s}) = 500$.

**Problem 2:** Derive the first non-zero blind speed for a 5 GHz C-band radar operating with a PRF of 1500 Hz. 
Following this, design the Z-domain transfer function for a standard 3-pulse MTI canceller and write its corresponding time-domain difference equation.

*Model Solution:*
First, find the wavelength: $\lambda = \frac{c}{f} = \frac{3\times 10^8}{5\times 10^9} = 0.06 \text{ meters}$.
First blind speed ($n=1$): $v_{blind} = \frac{\lambda \cdot \text{PRF}}{2} = \frac{0.06 \cdot 1500}{2} = 45 \text{ m/s}$.
A 3-pulse canceller cascades two basic 2-pulse cancellers. The single canceller is $(1 - z^{-1})$.
Transfer function: $H(z) = (1 - z^{-1})^2 = 1 - 2z^{-1} + z^{-2}$. 
Taking the Inverse Z-Transform yields the difference equation: $y[n] = x[n] - 2x[n-1] + x[n-2]$.

**Problem 3:** In an advanced DSP CA-CFAR architecture utilizing $N=16$ reference cells, compute the precise threshold multiplier $\alpha$ required to maintain a probability of false alarm $P_{fa} = 10^{-5}$.

*Model Solution:*
Formula: $\alpha = N\left( P_{fa}^{-1/N} - 1 \right)$
Substitute values: $\alpha = 16\left( (10^{-5})^{-1/16} - 1 \right) = 16\left( 10^{5/16} - 1 \right)$
Calculate exponent: $5/16 = 0.3125$.
$\alpha = 16\left( 10^{0.3125} - 1 \right) = 16(2.0535 - 1) = 16(1.0535) \approx 16.856$.

**Problem 4:** A continuous-wave FMCW radar transmits a $500$ MHz linear frequency sweep over a duration of $100 \mu s$. 
A target echo is received and mixed, producing a steady beat frequency of 1.5 MHz. 
Calculate the exact range to the target.

*Model Solution:*
FMCW beat equation: $f_b = \frac{2RB}{cT}$.
Rearrange for Range $R$: $R = \frac{f_b \cdot c \cdot T}{2B}$
$R = \frac{(1.5\times 10^6) \cdot (3\times 10^8) \cdot (100\times 10^{-6})}{2 \cdot (500\times 10^6)}$
$R = \frac{4.5\times 10^{10}}{10^9} = 45 \text{ meters}$.

### 10.3 True/False with Justification
1. **True/False:** In a pulsed radar system, dynamically increasing the PRF will directly increase the maximum unambiguous detection range.
   *False.* Increasing the PRF decreases the time between pulses ($T_r$). This directly leads to a *smaller* unambiguous range, governed by the equation $R_{max} = c / (2\text{PRF})$.

2. **True/False:** The mathematical matched filter guarantees the maximization of the signal-to-noise ratio for any given known received signal in AWGN.
   *True.* This is the fundamental definition and singular purpose of the matched filter, rigorously derived via the Cauchy-Schwarz inequality in functional analysis.

3. **True/False:** For a satellite SAR imaging system, utilizing a physically massive 10m antenna will provide significantly sharper azimuth resolution than a small 2m antenna.
   *False.* SAR theoretical azimuth resolution is exactly $D/2$. Therefore, the 2m antenna yields a stunning 1m resolution, while the massive 10m antenna yields a blurry 5m resolution. Smaller is better in SAR!

4. **True/False:** Implementing FMCW radar architectures requires extremely high-speed, expensive ADCs compared to traditional wideband pulsed radar.
   *False.* FMCW completely avoids high-speed ADCs because the analog mixer hardware down-converts the massive RF sweep into a very low-frequency audio beat signal, which can be digitized by incredibly cheap components.

5. **True/False:** Utilizing CFAR logic consistently improves the absolute probability of detecting a target in noise.
   *False.* CFAR logic actually lowers the probability of detection slightly compared to a theoretical (but impossible) perfectly known optimal fixed threshold. This penalty is called "CFAR loss." Its benefit is ensuring the false alarm rate remains strictly bounded.

6. **True/False:** The observed Doppler shift is directly proportional to the target's radial velocity and inversely proportional to the operating wavelength of the radar.
   *True.* This is mathematically evident from the fundamental Doppler equation $f_d = \frac{2v_r}{\lambda}$.

---
## 11. KEY FORMULAS REFERENCE

| Conceptual Topic | Mathematical Formula | Parameter Description |
| :--- | :--- | :--- |
| Monostatic Radar Equation | $P_r = \frac{P_t G^2 \lambda^2 \sigma}{(4\pi)^3 R^4}$ | Relates received power ($P_r$) to range and system params |
| Target Absolute Range | $R = \frac{c\tau}{2}$ | $\tau$ is the measured round-trip delay time |
| Fundamental Range Resolution | $\delta R = \frac{c}{2B}$ | $B$ is the effective signal bandwidth |
| Maximum Unambiguous Range | $R_{max} = \frac{c}{2 \text{PRF}}$ | The physical limit before range folding occurs |
| Target Doppler Frequency Shift | $f_d = \frac{2v_r}{\lambda}$ | $v_r$ is the radial component of target velocity |
| LFM Chirp Waveform Definition | $s(t) = \text{rect}(\frac{t}{T}) \exp(j\pi\frac{B}{T}t^2)$ | Complex baseband linear frequency modulation |
| Processing Gain | $\text{TBP} = B \cdot T$ | Time-bandwidth product of the pulse |
| Waveform Ambiguity Function | $|\chi(\tau, f_d)|^2 = \left\| \int s(t) s^*(t-\tau) e^{j2\pi f_d t} dt \right\|^2$ | Defines theoretical resolution and interference limits |
| CA-CFAR Dynamic Threshold| $T_{th} = \alpha \cdot \bar{P}_{noise}$, $\alpha = N(P_{fa}^{-1/N} - 1)$ | $N$ is the number of local reference cells |
| Basic MTI Filter Transfer Function| $H(z) = (1 - z^{-1})^k$ | $k=1$ for 2-pulse canceller, $k=2$ for 3-pulse |
| MTI Aliasing Blind Speed | $v_{blind} = \frac{n \lambda \text{PRF}}{2}$ | Speeds entirely invisible to the filter ($n \in \mathbb{Z}$) |
| FMCW Down-mixed Beat Freq | $f_b = \frac{2R}{c}\frac{B}{T}$ | Directly linearly relates target range to frequency |
| Ultimate SAR Azimuth Resolution | $\delta a = \frac{D}{2}$ | $D$ is the physical antenna aperture length |

---
## 12. FURTHER READING AND COMPREHENSIVE REFERENCES
- **Richards, M. A. (2014).** *Fundamentals of Radar Signal Processing, Second Edition.* McGraw-Hill Education. (This is considered the definitive modern textbook focusing entirely on the DSP aspects of radar systems).
- **Skolnik, M. I. (2008).** *Introduction to Radar Systems, Third Edition.* McGraw-Hill. (An excellent resource for grounding DSP concepts in physical hardware and system-level overviews).
- **Oppenheim, A. V., & Schafer, R. W. (2010).** *Discrete-Time Signal Processing, Third Edition.* Pearson. (Refer strictly to Chapters 4 and 10 for rigorous treatments of sampling, DSP fundamentals, and FFT algorithmic implementations).
- **Haykin, S. (2001).** *Adaptive Filter Theory, Fourth Edition.* Prentice Hall. (Highly recommended for students pursuing advanced research in Space-Time Adaptive Processing (STAP) and adaptive CFAR concepts).

---
## APPENDIX: ADVANCED TOPICS FOR INSTRUCTORS

### A.1 CFAR Loss Detailed Explanation
While CFAR is absolutely necessary, it is vital to teach students that it does not come for free. 
If the noise variance was perfectly known *a priori*, the optimal detector would be a fixed threshold derived from the Neyman-Pearson lemma. 
Because CFAR must *estimate* this noise variance from a finite set of $N$ reference cells, the estimate itself is a random variable. 
This statistical uncertainty means the CFAR threshold will randomly fluctuate above and below the theoretical optimal fixed threshold.

- When it fluctuates *low*, the false alarm rate temporarily spikes.
- To maintain the average desired $P_{fa}$, the CFAR multiplier $\alpha$ must be set *higher* than the equivalent fixed threshold multiplier.
- Because the threshold is higher on average, the probability of detecting a real target ($P_d$) drops.

This drop in $P_d$ (or equivalently, the extra SNR required to maintain the same $P_d$) is known as **CFAR Loss**. 
As $N \to \infty$, the estimate becomes perfect, and CFAR loss approaches 0 dB.

### A.2 The Straddle Loss Phenomenon
Another practical DSP issue is Straddle Loss. 
When we digitize the fast-time signal, we sample it into discrete range bins. 
It is highly unlikely that a target's true analog peak falls exactly in the center of a digital sample bin. 
Usually, the energy is split (straddled) between two adjacent bins.
This causes a reduction in the measured peak amplitude, leading to a loss in effective SNR. 

In the frequency domain (Doppler processing), the exact same thing happens if a target's true Doppler frequency falls between two FFT bins.
*Mitigation:* This is typically solved by applying zero-padding before the FFT, which interpolates the spectrum, recovering the peak amplitude and reducing straddle loss.

### A.3 Advanced Waveforms: Phase Coding
LFM is not the only way to achieve pulse compression. 
Discrete phase coding (e.g., Barker codes, Polyphase codes) is extensively used in modern digital radars. 
Instead of sweeping frequency continuously, the pulse is divided into $N_c$ smaller sub-pulses (chips).
The phase of each chip is abruptly switched (e.g., 0 or 180 degrees).

The matched filter is then implemented as a digital FIR filter.
The tap weights are the time-reversed, complex-conjugated code sequence. 
The compression ratio (TBP) for a phase-coded pulse is simply equal to the number of chips $N_c$. 
Barker codes are highly prized because their ambiguity function has perfectly flat, minimum-level sidelobes in the zero-Doppler cut, making target detection in clutter much cleaner than with LFM.

</Faculty Notes — Lecture 29: Radar DSP>
