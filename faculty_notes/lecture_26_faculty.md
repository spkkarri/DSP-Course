<Faculty Notes — Lecture 26: DSP for Power Systems — Harmonic Analysis & Phasor Estimation>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY

This lecture transitions students from pure signal processing theory into practical, high-stakes electrical engineering applications: Power Systems. 

Students often struggle to see how the abstract Discrete Fourier Transform (DFT) connects to physical grid infrastructure and power quality phenomena. 

The goal here is to ground the mathematics by constantly referring to physical parameters—specifically voltage, current, frequency, and real-time execution constraints. 

Common student difficulties include understanding exactly why DFT spectral leakage matters in a physical sense. 
They often treat it as a mathematical artifact, failing to see that in a digital relay, leakage causes false harmonics, which in turn can cause a false trip, bringing down a substation. 

Furthermore, the mathematical derivation of the Sliding (Recursive) DFT is notoriously confusing because of the time-shifting property. 
Faculty must emphasize how the sliding window functions conceptually before diving into the complex exponentials.

**Suggested Demos for the Lecture:** 

1. **Hardware-in-the-Loop:** 
   Use a signal generator to create a pure 50 Hz sine wave and a separately distorted wave (e.g., inject 3rd and 5th harmonics). 
   Run both signals through an oscilloscope with a real-time FFT analyzer to visually demonstrate the harmonic peaks. 

2. **Leakage Visualization:** 
   Program a simple Python or MATLAB script to show a slight frequency drift (e.g., grid droops to 49.5 Hz). 
   Run a standard rectangular window DFT to visually demonstrate spectral leakage spilling energy into adjacent bins.

3. **Sliding DFT Simulation:** 
   Show an animated sliding window moving across a sampled sine wave.
   Plot the magnitude and phase of the fundamental bin $X[1]$ at each time step.
   This proves that the magnitude remains constant while the phase continually rotates in the complex plane.

---
## 1. LEARNING OBJECTIVES

By the end of this comprehensive lecture, students will be able to:

1. **Define** Total Harmonic Distortion (THD) accurately and calculate it for given voltage and current harmonic profiles, understanding its physical implications on grid equipment.

2. **Derive** the 1-cycle Discrete Fourier Transform (DFT) completely from first principles, specifically tuned for extracting fundamental and harmonic complex phasors.

3. **Analyze** the effect of spectral leakage caused by off-nominal grid frequencies (frequency drift) on phasor estimation and propose mitigation strategies.

4. **Formulate** and rigorously prove the recursive (sliding) DFT algorithm for real-time, sample-by-sample phasor updates, computing its Big-O algorithmic complexity.

5. **Evaluate** the operational compliance of Phasor Measurement Units (PMUs) utilizing the exact Total Vector Error (TVE) metric mandated by the IEEE C37.118 standard.

6. **Design** a Kalman filter state-space model for optimal dynamic phasor tracking under transient grid fault conditions, contrasting it with the static DFT.

7. **Calculate** and interpret both active and reactive power components considering comprehensive harmonic content using standard DFT outputs and the Budeanu framework.

---
## 2. PREREQUISITE KNOWLEDGE REVIEW

Before introducing this specialized topic, faculty must ensure students are highly comfortable with the following mathematical prerequisites. 
A 5-minute review is strongly recommended:

* **Complex Phasors in AC Circuits:** 
  The representation of a time-domain continuous sinusoid $v(t) = V_{peak} \cos(\omega t + \phi)$ as a complex number (phasor). 
  The standard power systems convention uses the RMS phasor: 
  $$ V = \frac{V_{peak}}{\sqrt{2}} e^{j\phi} = \frac{V_{peak}}{\sqrt{2}} (\cos\phi + j\sin\phi) $$

* **Discrete Fourier Transform (DFT) Fundamentals:** 
  The standard $N$-point DFT formula defining the transformation from the discrete time-domain sequence $x[n]$ to the discrete frequency-domain sequence $X[k]$: 
  $$ X[k] = \sum_{n=0}^{N-1} x[n] e^{-j \frac{2\pi}{N} k n} $$
  Remind students of the orthogonality of discrete complex exponentials over exactly $N$ samples.

* **Active, Reactive, and Apparent Power (Fundamental Only):** 
  The classical definitions for purely sinusoidal systems:
  $$ P = V_{RMS} I_{RMS} \cos(\theta) $$
  $$ Q = V_{RMS} I_{RMS} \sin(\theta) $$
  $$ S = V_{RMS} I_{RMS}^* = P + jQ $$
  where $\theta = \phi_v - \phi_i$ is the power factor angle.

* **State-Space System Representation (Basic Control Theory):** 
  The discrete-time linear time-invariant system model:
  $$ \mathbf{x}_{k+1} = \mathbf{A}\mathbf{x}_k + \mathbf{B}\mathbf{u}_k + \mathbf{w}_k $$
  $$ \mathbf{y}_k = \mathbf{C}\mathbf{x}_k + \mathbf{v}_k $$
  where $\mathbf{w}_k$ and $\mathbf{v}_k$ are process and measurement noise respectively.

---
## 3. HISTORICAL AND MOTIVATIONAL CONTEXT

The application of Digital Signal Processing to power systems represents one of the most critical leaps in electrical infrastructure modernization. 
It began in earnest in the late 1970s and 1980s with the advent of microprocessor-based numerical relays. 

Prior to this era, electromechanical relays utilized physical moving coils, magnetic induction disks, and purely analog circuitry to detect overcurrents and faults. 
These older devices were incredibly slow, mechanically inflexible, prone to calibration drift, and required significant physical maintenance. 

The digitization of the grid allowed engineers to convert analog voltage and current signals into discrete samples. 
Suddenly, complex algorithms—like the Fourier Transform—could be executed in software to compute voltage and current phasors in real-time. 
This allowed numerical relays to distinguish between a harmless temporary overload and a catastrophic short circuit within milliseconds.

The concept of the **Phasor Measurement Unit (PMU)** was pioneered by Dr. Arun G. Phadke and Dr. James S. Thorp at Virginia Tech around 1988. 
They hypothesized that by synchronizing the analog-to-digital sampling clocks across the entire continental power grid using the 1-Pulse-Per-Second (1-PPS) signal from GPS satellites, they could measure the absolute phase angle of grid buses simultaneously. 

This single innovation birthed the field of Wide-Area Monitoring Systems (WAMS). 
It gave grid operators unprecedented, time-synchronized visibility into dynamic grid stability, directly preventing widespread cascading blackouts by identifying power oscillations before they caused system collapse.

**Why does an EEE student need this knowledge today?**

Modern electrical grids are experiencing a paradigm shift. 
They are becoming highly polluted with harmonics generated by nonlinear power electronics: 
electric vehicle (EV) fast chargers, solar photovoltaic grid-tied inverters, variable frequency drives (VFDs) in factories, and even standard switch-mode power supplies in consumer electronics. 

Accurately measuring these distortions, extracting the fundamental 50/60Hz components amidst severe noise, and rapidly isolating system faults using DSP algorithms is no longer optional. 
It is the baseline requirement for modern power system stability, microgrid control, and critical equipment protection.

---
## 4. THEORETICAL FOUNDATIONS

### 4.1 Power Quality: Ideal vs. Distorted Sinusoids and Harmonics

The ideal utility power grid provides a perfectly pure sinusoidal voltage. 
If a linear load (like a pure resistor or inductor) is connected, it draws a purely sinusoidal current. 
However, nonlinear loads draw current in abrupt, non-sinusoidal pulses. 

According to Fourier's fundamental theorem, any periodic but distorted waveform can be mathematically decomposed into the sum of a fundamental sinusoid (the grid frequency, 50Hz or 60Hz) and infinite harmonic sinusoids whose frequencies are strictly integer multiples of the fundamental.

Let the instantaneous periodic voltage waveform be $v(t)$ with a period $T = 1/f_1$. 
We represent this as a Fourier series:
$$ v(t) = V_{dc} + \sum_{k=1}^{\infty} V_k \sqrt{2} \cos(k \omega_1 t + \phi_k) $$

Where:
* $V_{dc}$ is the DC offset (ideally zero in AC grids).
* $V_k$ is the Root Mean Square (RMS) magnitude of the $k$-th harmonic component.
* $\omega_1 = 2\pi f_1$ is the fundamental angular frequency.
* $\phi_k$ is the phase angle of the $k$-th harmonic.
* The term $\sqrt{2}$ converts the RMS value $V_k$ to the peak amplitude required for the time-domain cosine function.

The fundamental is $k=1$ (e.g., 50 Hz). 
The 2nd harmonic is $k=2$ (100 Hz), the 3rd is $k=3$ (150 Hz), and so on.

**Inter-harmonics and Sub-harmonics:**
It is critical to distinguish integer harmonics from other spectral phenomena:
* **Inter-harmonics:** These are frequency components that are strictly *not* integer multiples of the fundamental frequency (e.g., 75 Hz, 182 Hz). They are primarily generated by asynchronous switching devices like Cycloconverters or Variable Frequency Drives operating at non-integer ratios of the grid frequency. They cause severe light flickering and sub-synchronous torsional interactions in generator shafts.
* **Sub-harmonics:** A specific subset of inter-harmonics where the frequency is strictly *less* than the fundamental grid frequency (e.g., 10 Hz, 25 Hz). Arc furnaces are a primary source of sub-harmonic pollution. In DSP analysis, standard 1-cycle window DFTs cannot correctly resolve sub-harmonics; analyzing them requires significantly longer observation windows (e.g., 10-12 cycles) to achieve the necessary frequency resolution.

### 4.2 Total Harmonic Distortion (THD) Formulation

The severity of harmonic distortion in a signal is quantified by a single metric: the Total Harmonic Distortion (THD). 
It is defined strictly as the ratio of the equivalent RMS value of all the harmonic components combined to the RMS value of the fundamental component alone.

Mathematically, for a voltage signal:
$$ THD_V = \frac{\sqrt{\sum_{k=2}^{\infty} V_k^2}}{V_1} \times 100\% $$

This ratio directly compares the RMS energy of the unwanted harmonic "pollution" to the RMS energy of the desired fundamental. 

**Physical Consequences of High THD:**

* **Transformers:** 
  High-frequency harmonic currents drastically increase skin effect and proximity effect in transformer windings. 
  This massively increases $I^2R$ copper losses. 
  Furthermore, higher frequencies increase core hysteresis and eddy current losses. 
  Transformers heavily loaded with harmonics must be severely derated to prevent thermal destruction.

* **Induction Motors:** 
  Negative sequence harmonics (specifically the 5th harmonic, e.g., 250 Hz) create a reverse-rotating magnetic field in the stator. 
  This produces an opposing "braking" torque against the rotor's primary rotation, reducing motor efficiency, causing severe overheating, and inducing mechanical shaft vibrations that destroy bearings.

* **Capacitor Banks:** 
  The reactance of a capacitor is inversely proportional to frequency ($X_c = 1 / (2\pi f C)$). 
  Therefore, capacitors present a very low impedance path to high-frequency harmonics. 
  This causes massive harmonic currents to sink into power factor correction capacitors, leading to dielectric breakdown and catastrophic explosive failures.

### 4.3 Power Quality Monitoring: Sags, Swells, and Unbalance

Aside from harmonics, numerical DSP relays and power quality monitors track several critical transient and steady-state voltage phenomena defined by standard IEC/IEEE metrics:

* **Voltage Sag (Dip):**
  A temporary decrease in the RMS voltage magnitude to between 0.1 pu and 0.9 pu (per unit) of the nominal voltage. 
  Sags typically last from 0.5 cycles to 1 minute. They are most commonly caused by faults on parallel feeder lines or the massive inrush currents of starting large induction motors. DSP relays detect this by calculating the 1-cycle RMS voltage continuously and comparing it against the 0.9 pu threshold.

* **Voltage Swell:**
  A temporary increase in the RMS voltage magnitude to between 1.1 pu and 1.8 pu of the nominal voltage. 
  Like sags, swells last from 0.5 cycles to 1 minute. They occur when heavy loads are abruptly switched off or due to single-line-to-ground faults causing the healthy phases to swell. The DSP detects a swell when the 1-cycle RMS exceeds 1.1 pu.

* **Voltage Unbalance:**
  In a perfectly balanced 3-phase system, all phase voltages are equal in magnitude and exactly 120° apart. 
  Unbalance occurs when single-phase loads (like residential lighting or traction systems) are unevenly distributed. 
  DSP algorithms calculate unbalance using the method of Symmetrical Components, specifically analyzing the ratio of the Negative Sequence Voltage ($V_2$) to the Positive Sequence Voltage ($V_1$).

* **Harmonic Limits (IEEE 519):**
  Monitors also check THD against strict utility codes. IEEE 519 limits are designed to restrict the harmonic injection from a consumer into the utility grid. Typical voltage THD limits are 5% for systems under 69kV, with individual harmonic limits strictly bounded to 3%.

### 4.4 Fourier Analysis for Grid Phasor Extraction

In a numerical protection relay, power quality meter, or PMU, the continuous analog signals ($v(t)$ and $i(t)$) are passed through an analog anti-aliasing lowpass filter and then sampled by an Analog-to-Digital Converter (ADC) at a constant sampling frequency $f_s$. 
This yields a discrete sequence $x[n]$.

To analyze exactly one fundamental cycle of the grid, we choose our window length $N$ such that:
$$ N = \frac{f_s}{f_1} $$
where $f_1$ is the nominal fundamental grid frequency.

The standard DFT formula at frequency bin $k$ is:
$$ X[k] = \sum_{n=0}^{N-1} x[n] e^{-j \frac{2\pi}{N} k n} $$

To extract the fundamental complex phasor, we evaluate the DFT specifically at bin $k=1$. 
Expanding the complex exponential using Euler's formula:
$$ X[1] = \sum_{n=0}^{N-1} x[n] \left( \cos\left(\frac{2\pi}{N} n\right) - j \sin\left(\frac{2\pi}{N} n\right) \right) $$

Because the standard DFT of a real sinusoid yields two peaks (at $k=1$ and $k=N-1$, representing positive and negative frequencies), the magnitude of the bin $X[1]$ is exactly half of the actual signal amplitude multiplied by $N$. 
Therefore, to extract the true time-domain peak amplitude phasor $V_{1, peak}$, we must scale the DFT output:
$$ V_{1, peak} = \frac{2}{N} X[1] $$

And to obtain the standard RMS phasor used in all power system load flow and fault calculations:
$$ V_{1, RMS} = \frac{V_{1, peak}}{\sqrt{2}} = \frac{\sqrt{2}}{N} X[1] $$

This resulting complex number intrinsically contains both the magnitude and the absolute phase angle of the fundamental component relative to the start of the sampling window ($n=0$).

### 4.4 The Problem of Spectral Leakage in Power Systems

The DFT's mathematical elegance relies entirely on the assumption that the signal is perfectly periodic over the exact window length $N$. 
If the grid frequency deviates from its nominal value—a common occurrence during generation-load imbalances—the sampling window no longer aligns with an integer number of cycles.

**Example Scenario:**
* Nominal Frequency: 50.0 Hz. Cycle duration: 20.00 ms.
* ADC samples at 1600 Hz. Samples per cycle $N = 32$.
* The grid undergoes a heavy load spike, causing the generators to slow down. The actual grid frequency droops to 49.5 Hz.
* The true cycle duration is now $1 / 49.5 \approx 20.20$ ms.
* However, our ADC still captures $N=32$ samples over exactly 20.00 ms.
* The data window truncates the waveform prematurely, leaving off the final 0.20 ms of the cycle.

When the DFT is applied, it implicitly assumes this truncated, 20.00 ms segment repeats infinitely. 
The truncation creates a sharp mathematical discontinuity at the boundary between one assumed period and the next. 

In the frequency domain, this discontinuity manifests as **Spectral Leakage**. 
The massive energy of the fundamental 49.5 Hz signal "leaks" or smears into the adjacent harmonic bins (e.g., $k=2, k=3$, etc.).

**Consequence:** 
A digital relay monitoring THD will suddenly report high harmonic levels, even if the voltage is a perfectly pure (but off-frequency) sine wave. 
This false harmonic reading can cause the relay to incorrectly trip a breaker, exacerbating the grid disturbance.

**Mitigation Strategies:** 

1. **Windowing Functions:** 
   Multiply the time-domain samples by a tapering function (e.g., Hanning or Blackman window) that smoothly forces the boundary samples to zero, eliminating the discontinuity. 

2. **Frequency Tracking (PLL):** 
   Implement a software Phase-Locked Loop that continuously estimates the true instantaneous grid frequency and dynamically adjusts the ADC sampling rate $f_s$ to ensure $N$ samples always perfectly span one actual cycle.

### 4.5 Phasor Measurement Units (PMUs) and Synchrophasors

A PMU computes the **synchrophasor**, which is defined as a complex phasor referenced to an absolute, universal time timestamp provided by GPS UTC.

The performance and compliance of a PMU are governed by the rigorous IEEE C37.118-2011 standard. 
The primary performance metric is the Total Vector Error (TVE).

Let the theoretical, mathematically true phasor be $X = X_r + j X_i$.
Let the PMU's digitally measured and computed phasor be $\hat{X} = \hat{X}_r + j \hat{X}_i$.

The TVE is defined as:
$$ TVE = \sqrt{ \frac{(\hat{X}_r - X_r)^2 + (\hat{X}_i - X_i)^2}{X_r^2 + X_i^2} } \times 100\% $$

The TVE encapsulates amplitude errors, phase angle errors, and GPS timing synchronization errors into one single scalar metric. 
The IEEE standard unequivocally demands that under steady-state conditions, the TVE must strictly remain $< 1\%$. 
Achieving this requires exceptional hardware and advanced DSP algorithms that can compensate for instrument transformer errors and ADC jitter.

---
## 5. COMPLETE PROOFS AND DERIVATIONS

### 5.1 Rigorous Derivation of the Recursive (Sliding) DFT

In numerical protection relays, tripping decisions must be made in less than a quarter of a cycle (e.g., 5 milliseconds). 
Recomputing an entire $N$-point Fast Fourier Transform (FFT) every time a new sample arrives is computationally prohibitive for microcontroller-based relays. 
The FFT requires $O(N \log N)$ operations. We require an algorithm that can update the phasor estimate in $O(1)$ operations per sample.

Let $X_k[n]$ represent the $k$-th DFT frequency bin computed over a data window of length $N$ that strictly ends at the current sample index $n$.
$$ X_k[n] = \sum_{m=0}^{N-1} x[n-m] e^{-j \frac{2\pi}{N} k (N-1-m)} $$

Let us fully expand this summation for clarity:
$$ X_k[n] = x[n]e^{-j \frac{2\pi}{N} k (N-1)} + x[n-1]e^{-j \frac{2\pi}{N} k (N-2)} + \dots + x[n-N+1]e^{-j \frac{2\pi}{N} k (0)} $$

Now, consider the DFT computed at the previous time step, $n-1$. 
This window covers samples from $n-N$ up to $n-1$:
$$ X_k[n-1] = \sum_{m=0}^{N-1} x[n-1-m] e^{-j \frac{2\pi}{N} k (N-1-m)} $$

Expanding this previous DFT:
$$ X_k[n-1] = x[n-1]e^{-j \frac{2\pi}{N} k (N-1)} + x[n-2]e^{-j \frac{2\pi}{N} k (N-2)} + \dots + x[n-N]e^{0} $$

Our objective is to algebraically express the new state $X_k[n]$ explicitly in terms of the previous state $X_k[n-1]$.

To align the exponential terms, let us multiply $X_k[n]$ by $e^{-j \frac{2\pi}{N} k}$:
$$ X_k[n] e^{-j \frac{2\pi}{N} k} = x[n]e^{-j \frac{2\pi}{N} k N} + x[n-1]e^{-j \frac{2\pi}{N} k (N-1)} + \dots + x[n-N+1]e^{-j \frac{2\pi}{N} k} $$

We must recognize a critical property of complex exponentials. 
The term $e^{-j \frac{2\pi}{N} k N}$ simplifies directly to $e^{-j 2\pi k}$. 
Because $k$ is strictly an integer representing the harmonic index, $e^{-j 2\pi k} = \cos(2\pi k) - j\sin(2\pi k) = 1 - j0 = 1$.

Substituting this identity yields:
$$ X_k[n] e^{-j \frac{2\pi}{N} k} = x[n] + x[n-1]e^{-j \frac{2\pi}{N} k (N-1)} + \dots + x[n-N+1]e^{-j \frac{2\pi}{N} k} $$

Now, we compare this resulting expression closely with the expanded form of $X_k[n-1]$:
$$ X_k[n-1] = x[n-1]e^{-j \frac{2\pi}{N} k (N-1)} + \dots + x[n-N+1]e^{-j \frac{2\pi}{N} k} + x[n-N] $$

Observe that the large middle block of terms is perfectly identical. 
We can therefore substitute the terms from $n-1$ down to $n-N+1$:
$$ \text{Middle Terms} = X_k[n-1] - x[n-N] $$

Substituting this back into our modified $X_k[n]$ equation:
$$ X_k[n] e^{-j \frac{2\pi}{N} k} = x[n] + \left( X_k[n-1] - x[n-N] \right) $$

Finally, we isolate $X_k[n]$ by multiplying both sides by $e^{+j \frac{2\pi}{N} k}$:
$$ X_k[n] = \left( X_k[n-1] + x[n] - x[n-N] \right) e^{j \frac{2\pi}{N} k} $$

**Q.E.D.**

**Algorithmic Complexity and Physical Interpretation:**

This update requires exactly:
1. One real subtraction: $(x[n] - x[n-N])$
2. One complex addition: adding the result to $X_k[n-1]$
3. One complex multiplication: multiplying by the constant rotation factor $e^{j \frac{2\pi}{N} k}$.

The complexity is definitively $O(1)$ per sample.

Physically, this means: Drop the oldest sample, add the newest sample, and phase-rotate the resulting complex vector forward by exactly one sample's angular width to account for the advancement of the observation window.

### 5.2 Power Formulation under Harmonics

Active power ($P$) is defined as the average power over a fundamental cycle $T$.
$$ P = \frac{1}{T} \int_0^T v(t)i(t) dt $$

If both voltage and current contain harmonics, we represent them by their Fourier series.
$$ v(t) = \sum_{k=1}^{\infty} V_k \sqrt{2} \cos(k\omega_1 t + \phi_{vk}) $$
$$ i(t) = \sum_{m=1}^{\infty} I_m \sqrt{2} \cos(m\omega_1 t + \phi_{im}) $$

When multiplying the series and integrating over the period $T$, all cross-frequency products (where $k \neq m$) integrate exactly to zero due to the orthogonal nature of sinusoids of different harmonic frequencies.

Therefore, real power transfer only occurs between voltage and current components of the identical frequency:
$$ P = \sum_{k=1}^{\infty} V_k I_k \cos(\phi_{vk} - \phi_{ik}) $$

This mathematically proves that harmonic currents drawn by a nonlinear load interacting with a pure fundamental voltage source produce exactly zero useful active power, yet they still heavily inflate the RMS current, causing catastrophic thermal losses.

---
## 6. WORKED EXAMPLES (MINIMUM 5 — fully solved)

### Example 1: Total Harmonic Distortion (THD) Calculation

**Problem statement:** 
An industrial facility utilizes massive 6-pulse Variable Frequency Drives. A power quality analyzer measures the phase current and reports the following RMS harmonic profile: 
Fundamental ($I_1$) = 150 A, 5th Harmonic ($I_5$) = 30 A, 7th Harmonic ($I_7$) = 15 A, 11th Harmonic ($I_{11}$) = 10 A, 13th Harmonic ($I_{13}$) = 5 A. 
All other harmonics are practically zero. Calculate the Total Harmonic Distortion of the current ($THD_I$). Determine if this exceeds standard IEEE 519 limits (assume limit is 5%).

**Solution:**
1. Identify the fundamental component magnitude: 
   $$ I_1 = 150 \text{ A} $$
2. Sum the squares of all the harmonic components ($k \ge 2$):
   $$ \sum_{k=2}^{\infty} I_k^2 = I_5^2 + I_7^2 + I_{11}^2 + I_{13}^2 $$
   $$ \sum I_k^2 = 30^2 + 15^2 + 10^2 + 5^2 $$
   $$ \sum I_k^2 = 900 + 225 + 100 + 25 = 1250 \text{ A}^2 $$
3. Compute the total RMS harmonic current by taking the square root:
   $$ I_H = \sqrt{1250} \approx 35.355 \text{ A} $$
4. Compute the final $THD_I$ ratio:
   $$ THD_I = \frac{I_H}{I_1} = \frac{35.355}{150} = 0.2357 $$
   
**Answer:** 
$THD_I = 23.57\%$. This wildly exceeds the typical 5% IEEE 519 limit.

**Physical interpretation:** 
The facility is injecting massive harmonic pollution back into the grid, drawing 35.3 Amps of entirely useless harmonic current that only serves to overheat the utility's supply transformers.

**Common mistakes to avoid:** 
Students routinely include the fundamental $I_1$ in the numerator sum. The numerator sum must strictly begin at $k=2$.

### Example 2: Extracting the Physical Phasor from Raw DFT Bins

**Problem statement:** 
A microprocessor-based distance relay protects a 50 Hz transmission line. It samples the voltage at 1000 Hz. Following a severe fault, a 1-cycle DFT is computed on the voltage samples. 
The fundamental DFT bin ($k=1$) evaluates to the complex value $X[1] = -5000 - j2000$. 
Calculate the true RMS voltage phasor (magnitude and phase) that the relay will use for its distance calculation.

**Solution:**
1. Determine the sample window size $N$:
   $$ N = \frac{f_s}{f_1} = \frac{1000}{50} = 20 \text{ samples per cycle.} $$
2. Convert the raw DFT bin to the peak time-domain phasor using the $2/N$ scale factor:
   $$ V_{1, peak} = \frac{2}{20} (-5000 - j2000) = 0.1 (-5000 - j2000) = -500 - j200 \text{ V.} $$
3. Convert the peak phasor to the standard RMS phasor:
   $$ V_{1, RMS} = \frac{-500 - j200}{\sqrt{2}} \approx -353.55 - j141.42 \text{ V.} $$
4. Calculate the magnitude of the RMS phasor:
   $$ |V_{1, RMS}| = \sqrt{(-353.55)^2 + (-141.42)^2} $$
   $$ |V_{1, RMS}| = \sqrt{125000 + 20000} = \sqrt{145000} \approx 380.79 \text{ V.} $$
5. Calculate the absolute phase angle. Because both the real and imaginary components are negative, the phasor lies strictly in the third quadrant of the complex plane:
   $$ \phi_1 = \text{atan2}(-141.42, -353.55) = -158.2^\circ \ (\text{or } +201.8^\circ). $$
   
**Answer:** 
The true RMS phasor is $380.79 \angle -158.2^\circ$ V.

**Physical interpretation:** 
The voltage magnitude has collapsed to just 380V RMS, and the phase angle has shifted drastically, highly indicative of a bolted fault condition on the line.

**Common mistakes to avoid:** 
Forgetting to scale by $2/N$ to get the physical amplitude, forgetting to divide by $\sqrt{2}$ to get RMS (standard in power systems), and using standard $\arctan(y/x)$ which cannot distinguish between quadrants 1/3 and 2/4.

### Example 3: Executing the Recursive DFT Update Step

**Problem statement:** 
A protective relay executes the recursive (sliding) DFT algorithm for a 60 Hz electrical system. The ADC sampling rate is 480 Hz. Let $N$ be the 1-cycle window size. 
For the fundamental frequency bin ($k=1$), the previously calculated unscaled DFT value was $X_1[n-1] = 200 + j150$. 
At the current time step, the new incoming sample is $x[n] = 40$, and the oldest sample dropping out of the window is $x[n-N] = -10$. 
Calculate the exact new unscaled DFT bin value $X_1[n]$.

**Solution:**
1. Determine the window length $N$:
   $$ N = \frac{480}{60} = 8 \text{ samples.} $$
2. Determine the constant complex phase rotation factor $e^{j \frac{2\pi}{N} k}$:
   For $N=8, k=1$: The rotation angle is $\theta = \frac{2\pi(1)}{8} = \frac{\pi}{4}$ radians ($45^\circ$).
   $$ e^{j \pi/4} = \cos(45^\circ) + j\sin(45^\circ) = 0.7071 + j0.7071 $$
3. Execute the inner addition step of the recursive formula:
   $$ \text{Inner} = X_1[n-1] + x[n] - x[n-N] $$
   $$ \text{Inner} = (200 + j150) + 40 - (-10) $$
   $$ \text{Inner} = (200 + j150) + 50 = 250 + j150 $$
4. Execute the complex multiplication with the rotation factor:
   $$ X_1[n] = (250 + j150)(0.7071 + j0.7071) $$
   Calculate the Real part: 
   $$ (250 \times 0.7071) - (150 \times 0.7071) = 176.775 - 106.065 = 70.71 $$
   Calculate the Imaginary part: 
   $$ (250 \times 0.7071) + (150 \times 0.7071) = 176.775 + 106.065 = 282.84 $$
   
**Answer:** 
The updated unscaled bin value is $X_1[n] = 70.71 + j282.84$.

**Physical interpretation:** 
The sliding window advanced by one sample time (1/480th of a second), causing the measured fundamental phasor vector to physically rotate by exactly $45^\circ$ in the complex plane.

### Example 4: Evaluating PMU Compliance via Total Vector Error (TVE)

**Problem statement:** 
A manufacturer is seeking IEEE C37.118 certification for their new Phasor Measurement Unit. 
During a steady-state compliance test, the highly accurate laboratory reference reports a true fundamental voltage phasor of $120.00 \angle 0.00^\circ$ V. 
The PMU under test reports a measured phasor of $119.50 \angle 0.50^\circ$ V. 
1. Calculate the TVE.
2. Determine if the PMU passes the standard steady-state requirement of $< 1\%$.

**Solution:**
1. Convert the laboratory reference phasor to rectangular form:
   $$ X_{true} = 120.00 \cos(0^\circ) + j120.00 \sin(0^\circ) = 120.00 + j0.00 $$
2. Convert the PMU's measured phasor to rectangular form:
   $$ \hat{X} = 119.50 \cos(0.50^\circ) + j119.50 \sin(0.50^\circ) $$
   $$ \cos(0.50^\circ) \approx 0.99996, \quad \sin(0.50^\circ) \approx 0.008726 $$
   $$ \hat{X}_r = 119.50 \times 0.99996 = 119.495 $$
   $$ \hat{X}_i = 119.50 \times 0.008726 = 1.0428 $$
   So, $\hat{X} = 119.495 + j1.0428$.
3. Apply the TVE formula rigorously:
   $$ TVE = \sqrt{ \frac{(\hat{X}_r - X_r)^2 + (\hat{X}_i - X_i)^2}{X_r^2 + X_i^2} } \times 100\% $$
   Calculate numerator terms:
   $$ (\hat{X}_r - X_r) = 119.495 - 120.00 = -0.505 $$
   $$ (\hat{X}_i - X_i) = 1.0428 - 0.00 = 1.0428 $$
   Numerator sum of squares: 
   $$ (-0.505)^2 + (1.0428)^2 = 0.255 + 1.0874 = 1.3424 $$
   Denominator sum of squares: 
   $$ 120.00^2 + 0^2 = 14400 $$
   $$ TVE = \sqrt{\frac{1.3424}{14400}} \times 100\% $$
   $$ TVE = \sqrt{0.00009322} \times 100\% $$
   $$ TVE = 0.00965 \times 100\% = 0.965\% $$
   
**Answer:** 
The TVE is $0.965\%$. Because $0.965\% < 1.0\%$, the PMU mathematically passes the steady-state certification.

**Physical interpretation:** 
The TVE is extremely sensitive to phase errors. Even though the magnitude was off by less than $0.5\%$, the mere $0.5^\circ$ phase error almost caused the unit to fail the strict $1\%$ standard limit.

### Example 5: Active and Reactive Power Computation with Severe Harmonics

**Problem statement:** 
An arc furnace draws highly distorted single-phase power. A DSP-based meter computes the following RMS phasors using an FFT:
Fundamental ($k=1$): $V_1 = 200 \angle 0^\circ$ V, $I_1 = 50 \angle -45^\circ$ A
Third Harmonic ($k=3$): $V_3 = 40 \angle 30^\circ$ V, $I_3 = 20 \angle -15^\circ$ A
Fifth Harmonic ($k=5$): $V_5 = 10 \angle 90^\circ$ V, $I_5 = 15 \angle 0^\circ$ A
Calculate the total Active Power ($P$) and total Budeanu Reactive Power ($Q$) consumed by the furnace.

**Solution:**
We evaluate $P$ and $Q$ harmonic by harmonic.
1. **Fundamental Component ($k=1$):**
   $$ P_1 = V_1 I_1 \cos(\phi_{v1} - \phi_{i1}) $$
   $$ P_1 = (200)(50) \cos(0^\circ - (-45^\circ)) = 10000 \cos(45^\circ) = 10000(0.707) = 7071 \text{ W} $$
   $$ Q_1 = V_1 I_1 \sin(\phi_{v1} - \phi_{i1}) $$
   $$ Q_1 = (200)(50) \sin(45^\circ) = 10000(0.707) = 7071 \text{ VAR} $$
2. **Third Harmonic Component ($k=3$):**
   $$ P_3 = V_3 I_3 \cos(\phi_{v3} - \phi_{i3}) $$
   $$ P_3 = (40)(20) \cos(30^\circ - (-15^\circ)) = 800 \cos(45^\circ) = 800(0.707) = 565.6 \text{ W} $$
   $$ Q_3 = V_3 I_3 \sin(45^\circ) = 800(0.707) = 565.6 \text{ VAR} $$
3. **Fifth Harmonic Component ($k=5$):**
   $$ P_5 = V_5 I_5 \cos(\phi_{v5} - \phi_{i5}) $$
   $$ P_5 = (10)(15) \cos(90^\circ - 0^\circ) = 150 \cos(90^\circ) = 150(0) = 0 \text{ W} $$
   $$ Q_5 = V_5 I_5 \sin(90^\circ) = 150(1) = 150 \text{ VAR} $$
4. **Total Active Power ($P$):**
   $$ P = P_1 + P_3 + P_5 = 7071 + 565.6 + 0 = 7636.6 \text{ W} $$
5. **Total Reactive Power ($Q$):**
   $$ Q = Q_1 + Q_3 + Q_5 = 7071 + 565.6 + 150 = 7786.6 \text{ VAR} $$
   
**Answer:** 
Total P = 7636.6 W, Total Q = 7786.6 VAR.

**Physical interpretation:** 
The 3rd harmonic actually contributes to real power flow, but often this harmonic active power ends up dissipated entirely as core-loss heat in downstream transformers rather than doing useful mechanical work. The 5th harmonic voltage and current are exactly orthogonal ($90^\circ$ apart), thus they shuttle energy back and forth without doing net work.

---
## 7. ENGINEERING APPLICATIONS AND CASE STUDIES

### 7.1 Active Power Filters (APF) and Shunt Compensation

An Active Power Filter is a sophisticated power electronics inverter installed in parallel (shunt) with a polluting nonlinear load (like an arc furnace). 
It continuously measures the load current harmonics and injects equal but opposite (180° out of phase) harmonic currents into the grid. 
The result is that the utility grid sees a perfectly pure sine wave load.

* **The DSP Role:** 
  A high-speed DSP microcontroller (such as the Texas Instruments C2000 series) samples the load current at rates exceeding 20 kHz. 
  It utilizes highly optimized recursive DFT or instantaneous reactive power theory (p-q theory) algorithms to rapidly extract the harmonic profile.
* **Latency Constraint:** 
  To maintain closed-loop control stability and accurately cancel out high-order harmonics, the DSP must sample, run the DFT, calculate the corrective current reference, and generate the PWM gate drive signals for the IGBTs all within a tight real-time deadline of less than $50 \mu\text{s}$. 
  Standard FFT approaches are utterly incapable of meeting this deadline, necessitating the recursive algorithms taught in this lecture.

### 7.2 Numerical Distance Protection Relays (ANSI 21)

Distance relays protect critical high-voltage transmission lines. 
They operate on the principle of computing the apparent impedance of the transmission line, $Z = V_1 / I_1$, calculated strictly from the fundamental frequency phasors.

* **The DSP Role:** 
  When a fault (like a lightning strike causing a short circuit to the tower) occurs, the voltage instantly collapses and the current spikes massively. 
  The resulting waveforms are violently distorted, containing high-frequency traveling wave transients and slowly decaying exponential DC offsets.
* The relay's DSP first applies a digital mimic filter (differentiator) to aggressively strip away the DC offset. 
  It then processes the filtered signal through the 1-cycle Recursive DFT. 
  Because a fault requires isolation within 2 to 3 cycles (40-60 ms) to prevent grid instability, the DSP must yield a stable impedance calculation within less than 1 cycle. 
  If the calculated complex $Z$ falls inside a predefined protective geometric zone (like a Mho circle) on the R-X plane, the DSP immediately fires an interrupt to open the massive high-voltage circuit breakers.

### 7.3 Kalman Filter for Dynamic Phasor Tracking

The static DFT formulation assumes the voltage signal amplitude and phase are perfectly constant over the $N$-sample observation window. 
During dynamic system events (generator swings, power oscillations, faults), this assumption fails completely. 

* **State-Space Paradigm:** 
  The Kalman Filter models the fundamental phasor dynamically. The state vector is $\mathbf{x}_k = [X_{real}, X_{imag}]^T$. 
* The state transition matrix predicts how the phasor will rotate to the next sample based on the nominal frequency. 
* As each new ADC measurement $z_k$ arrives, the filter optimally updates the state estimate by blending the prediction with the new measurement, weighted by the Kalman Gain. 
* **Advantage:** 
  Unlike the DFT which is bounded by a 1-cycle sliding window that "smears" transient events, a well-tuned Kalman Filter can track rapidly changing amplitudes and step-changes in phase angles in just a fraction of a cycle. 
  It provides optimal phasor estimation even amidst severe measurement noise.

---
## 8. COMMON STUDENT MISCONCEPTIONS AND ERRORS

1. **Misconception:** 
   The full FFT algorithm must be re-executed for every single incoming sample to generate a continuous phasor stream.
   * **Correction:** 
     Re-running an FFT every sample is wildly inefficient ($O(N \log N)$). The Recursive (Sliding) DFT updates the harmonic bin based solely on the incoming and exiting samples in strict $O(1)$ time, making full FFTs entirely unnecessary for tracking a few specific bins.

2. **Misconception:** 
   The Total Harmonic Distortion (THD) metric can never mathematically exceed 100%.
   * **Correction:** 
     This is factually incorrect. If the total RMS sum of the harmonics is larger than the RMS of the fundamental, the THD is absolutely $>100\%$. This scenario is incredibly common in highly distorted power electronics applications, such as the input current waveform of an unfiltered single-phase diode bridge rectifier.

3. **Misconception:** 
   Applying a windowing function (like Hanning or Hamming) is universally beneficial and should always be used before a DFT.
   * **Correction:** 
     Windowing intrinsically broadens the main frequency lobe, reducing frequency resolution. In a power system, if the grid frequency is exactly nominal (e.g., 50.00 Hz), a standard rectangular window provides perfect, zero-leakage orthogonal results. Applying a Hanning window to this perfect scenario actually degrades the fundamental amplitude estimate. Windowing is solely a necessary evil to mitigate leakage when the frequency drifts off-nominal.

4. **Misconception:** 
   The 1-cycle DFT accurately captures the instantaneous dynamics of a fault transient.
   * **Correction:** 
     The DFT explicitly assumes the signal is stationary and periodic over the entire data window. During a violent step change (a fault), the DFT output takes exactly one full cycle to transition smoothly from the pre-fault steady state to the post-fault steady state. The 1-cycle DFT output during this transition is a mathematical artifact, a blur, and does not represent true instantaneous physical reality.

5. **Misconception:** 
   The scale factor $2/N$ must be applied to all DFT bins to get peak physical amplitude.
   * **Correction:** 
     The scale factor for the DC component bin ($k=0$) is $1/N$, not $2/N$.

---
## 9. CONNECTIONS TO OTHER LECTURES

* **Builds intensely upon:** 
  Lecture 15 (Discrete Fourier Transform Fundamentals), Lecture 20 (Windowing Techniques and Spectral Leakage Analysis), Lecture 22 (FFT Algorithms).
* **Prepares students for:** 
  Lecture 28 (Kalman Filtering - Deep Dive into State Estimation), Lecture 30 (Advanced DSP Processors and FPGA Architectures). 
  This specific lecture serves as the primary "bridge" proving to EEE students that highly abstract DSP mathematical transforms possess concrete, mission-critical safety implications in high-voltage engineering.

---
## 10. EXAMINATION QUESTIONS

### 10.1 Short Answer (5 questions with model answers)

**Q1:** Explain physically why an off-nominal grid frequency induces spectral leakage in a standard DFT phasor estimation algorithm.
**Model Answer:** The mathematical foundation of the DFT relies on the strict assumption that the discrete sample window encapsulates exactly an integer number of fundamental cycles. When the grid frequency drifts off-nominal, this periodicity assumption breaks. The data window prematurely truncates the cycle, creating a sharp mathematical discontinuity at the window edges. In the frequency domain, the concentrated energy of the fundamental frequency smears or "leaks" outward into adjacent harmonic frequency bins.

**Q2:** State the primary algorithmic advantage of deploying the recursive DFT over a standard radix-2 FFT for digital distance protection relays.
**Model Answer:** The recursive (sliding) DFT requires only a constant $O(1)$ number of arithmetic operations (2 additions, 1 complex multiplication) per sample to update a specific frequency bin. Conversely, the FFT requires $O(N \log N)$ operations per sample. Because relays only need to track a few specific frequencies (fundamental, DC, 2nd, 3rd, 5th), the recursive approach is immensely more computationally efficient, meeting strict real-time deadlines.

**Q3:** Provide the precise technical definition of a synchrophasor in the context of WAMS.
**Model Answer:** A synchrophasor is the complex phasor representation of a fundamental power system voltage or current signal that has been rigidly timestamped and synchronized against an absolute, highly accurate universal time reference (typically the UTC 1-PPS signal from the GPS constellation).

**Q4:** What is the maximum acceptable Total Vector Error (TVE) for a PMU per the IEEE C37.118-2011 steady-state compliance requirements?
**Model Answer:** The TVE must strictly remain less than 1.0%.

**Q5:** Why is an analog anti-aliasing lowpass filter fundamentally required before the ADC stage in a digital protection relay?
**Model Answer:** The power grid is heavily polluted with high-frequency noise and high-energy transients (e.g., lightning strikes, switching surges). If these high-frequency components exceed the ADC's Nyquist frequency ($f_s / 2$), they will mathematically fold back (alias) into the lower fundamental frequency band during sampling. This corrupted fundamental measurement could easily trigger a false and catastrophic relay trip. The analog filter blocks these frequencies before sampling occurs.

### 10.2 Long Answer / Numerical Problems (4 problems with complete solutions)

**Problem 1:** 
An intelligent electronic device (IED) samples a voltage signal at a high rate of 2400 Hz. The nominal power grid frequency is exactly 60 Hz. 
a) Determine the exact 1-cycle DFT observation window size $N$. 
b) Utilizing the recursive DFT methodology, derive the precise complex update equation specifically for the 5th harmonic frequency bin, $X_5[n]$. What is the numerical value of the complex phase rotation factor?

**Solution:**
a) $N = \frac{f_s}{f_1} = \frac{2400}{60} = 40$ discrete samples per fundamental cycle.
b) The generalized recursive formula is: 
   $$ X_k[n] = (X_k[n-1] + x[n] - x[n-N]) e^{j \frac{2\pi}{N} k} $$
   For the 5th harmonic, $k=5$, and we established $N=40$. 
   The phase rotation exponent is: 
   $$ \theta = \frac{2\pi(5)}{40} = \frac{10\pi}{40} = \frac{\pi}{4} \text{ radians } (45^\circ) $$
   The complex rotation factor evaluated is: 
   $$ e^{j \pi/4} = \cos(45^\circ) + j\sin(45^\circ) = 0.7071 + j0.7071 $$
   The final precise update equation is:
   $$ X_5[n] = (X_5[n-1] + x[n] - x[n-40]) (0.7071 + j0.7071) $$

**Problem 2:**
During a rigorous factory acceptance test (FAT), a PMU measures and reports a fundamental voltage phasor of $102.5 \angle -1.5^\circ$ V. 
Concurrently, the highly precise laboratory calibration standard reports the true, absolute reference phasor as $100.0 \angle 0.0^\circ$ V. 
Calculate the Total Vector Error (TVE) percentage.

**Solution:**
1. Convert true reference to rectangular:
   $$ X_{true} = 100.0 + j0.0 $$
2. Convert PMU measurement to rectangular:
   $$ \hat{X} = 102.5 \cos(-1.5^\circ) + j102.5 \sin(-1.5^\circ) $$
   $$ \hat{X}_r = 102.5 \times 0.999657 = 102.4648 $$
   $$ \hat{X}_i = 102.5 \times (-0.026176) = -2.683 $$
3. Compute TVE:
   $$ TVE = \sqrt{ \frac{(102.4648 - 100.0)^2 + (-2.683 - 0)^2}{100.0^2} } \times 100\% $$
   $$ TVE = \sqrt{ \frac{(2.4648)^2 + (-2.683)^2}{10000} } \times 100\% $$
   $$ TVE = \sqrt{ \frac{6.075 + 7.198}{10000} } \times 100\% $$
   $$ TVE = \sqrt{ \frac{13.273}{10000} } \times 100\% $$
   $$ TVE = \sqrt{0.0013273} \times 100\% $$
   $$ TVE = 0.03643 \times 100\% = 3.64\% $$

**Problem 3:** 
A highly nonlinear 3-phase rectifier load draws the following current harmonic profile: $I_1=45$ A, $I_3=12$ A, $I_5=8$ A, $I_7=6$ A, $I_{11}=2$ A. 
Determine the $THD_I$ percentage.

**Solution:**
1. Compute the RMS sum of all harmonic components ($k \ge 2$):
   $$ I_H = \sqrt{12^2 + 8^2 + 6^2 + 2^2} $$
   $$ I_H = \sqrt{144 + 64 + 36 + 4} = \sqrt{248} $$
   $$ I_H \approx 15.748 \text{ A} $$
2. Compute THD:
   $$ THD_I = \frac{15.748}{45} \times 100\% = 34.99\% $$

**Problem 4:**
A numerical impedance protection relay continuously computes the apparent line impedance $Z = V_1 / I_1$. 
At a specific time step, a 1-cycle unscaled DFT processes a 32-sample window. 
The outputs are $X_{V1} = 4000 - j3000$ and $X_{I1} = 200 - j100$. 
Compute the apparent physical impedance $Z$ in polar form. (Note: demonstrate that the $2/N$ scale factors gracefully cancel out in the ratio).

**Solution:**
The physical phasors are $V_1 = \frac{2}{N} X_{V1}$ and $I_1 = \frac{2}{N} X_{I1}$.
$$ Z = \frac{V_1}{I_1} = \frac{\frac{2}{N} (4000 - j3000)}{\frac{2}{N} (200 - j100)} = \frac{4000 - j3000}{200 - j100} $$
1. Compute Magnitude:
   $$ |X_{V1}| = \sqrt{4000^2 + (-3000)^2} = 5000 $$
   $$ |X_{I1}| = \sqrt{200^2 + (-100)^2} = \sqrt{40000 + 10000} = \sqrt{50000} = 223.6 $$
   $$ |Z| = \frac{5000}{223.6} = 22.36 \ \Omega $$
2. Compute Phase Angles:
   $$ \text{Angle of } V_1 = \text{atan2}(-3000, 4000) = -36.87^\circ $$
   $$ \text{Angle of } I_1 = \text{atan2}(-100, 200) = -26.56^\circ $$
   $$ \text{Angle of } Z = \text{Angle of } V_1 - \text{Angle of } I_1 = -36.87^\circ - (-26.56^\circ) = -10.31^\circ $$
   
Final Answer: $Z = 22.36 \angle -10.31^\circ \ \Omega$.

### 10.3 True/False with Justification (6 items)

1. **T/F:** A perfectly pure sine wave from a laboratory signal generator possesses a THD of 100%. 
   **Answer:** False. A pure sine wave contains absolutely zero harmonic content. Therefore, the numerator of the THD equation is zero, yielding a THD of exactly 0%.

2. **T/F:** The algorithmic complexity of the recursive sliding DFT is strictly O(1) operations per sample update.
   **Answer:** True. The algorithm executes a fixed number of arithmetic operations (2 additions, 1 complex multiplication) for any given bin update, completely irrespective of the window size $N$.

3. **T/F:** The IEEE C37.118-2011 standard mandates that a PMU's TVE must be mathematically zero.
   **Answer:** False. Achieving absolute zero measurement error in physical analog systems is impossible due to ADC quantization noise and clock jitter. The standard specifies a rigorous, but achievable, tolerance of TVE < 1% under steady-state conditions.

4. **T/F:** Harmonic currents fundamentally contribute to useful mechanical active power transfer in three-phase induction motors.
   **Answer:** False. Harmonic active power primarily manifests purely as core and copper heat loss. Furthermore, certain harmonics (like the 5th) produce opposing torque that actually hinders mechanical work.

5. **T/F:** A well-tuned state-space Kalman filter is capable of tracking dynamic phasor changes faster and more accurately than a 1-cycle DFT.
   **Answer:** True. The DFT is locked to an averaging time window of one full cycle, which naturally blurs fast transients. The Kalman filter leverages dynamic transition models to recursively update the state estimate instantaneously with every new sample.

6. **T/F:** When computing Total Harmonic Distortion (THD), the DC offset component ($k=0$) is included in the numerator summation.
   **Answer:** False. THD is strictly a metric for AC waveform distortion, evaluating harmonic frequencies ($k \ge 2$). DC injection is an entirely separate power quality metric.

---
## 11. KEY FORMULAS REFERENCE

| Conceptual Parameter | Rigorous Formula | Technical Notes |
| :--- | :--- | :--- |
| **Total Harmonic Distortion (THD)** | $THD = \frac{\sqrt{\sum_{k=2}^\infty V_k^2}}{V_1} \times 100\%$ | Numerator strictly evaluates $k \ge 2$ using RMS values. |
| **1-Cycle DFT ($k$-th frequency bin)** | $X[k] = \sum_{n=0}^{N-1} x[n] e^{-j \frac{2\pi}{N} k n}$ | Evaluates raw, unscaled complex sum over window $N$. |
| **Peak Phasor Extraction** | $V_{k, peak} = \frac{2}{N} X[k]$ | Scale factor specifically for AC bins ($k \neq 0$). |
| **RMS Phasor Extraction** | $V_{k, RMS} = \frac{\sqrt{2}}{N} X[k]$ | Standard phasor definition in power systems analysis. |
| **Recursive (Sliding) DFT Update** | $X_k[n] = \left( X_k[n-1] + x[n] - x[n-N] \right) e^{j \frac{2\pi}{N} k}$ | Executes in strict $O(1)$ complexity. |
| **Total Vector Error (TVE)** | $TVE = \sqrt{ \frac{(\hat{X}_r - X_r)^2 + (\hat{X}_i - X_i)^2}{X_r^2 + X_i^2} } \times 100\%$ | Mandatory compliance metric for PMUs. |
| **Active Power (Harmonics Included)** | $P = \sum_{k=1}^N V_{k,RMS} I_{k,RMS} \cos(\phi_{Vk} - \phi_{Ik})$ | Proves cross-frequency real power is mathematically zero. |
| **Reactive Power (Harmonics Included)** | $Q = \sum_{k=1}^N V_{k,RMS} I_{k,RMS} \sin(\phi_{Vk} - \phi_{Ik})$ | Based strictly on the classical Budeanu definition framework. |

---
## 12. FURTHER READING AND REFERENCES

1. **Phadke, A. G., & Thorp, J. S. (2008).** *Synchronized Phasor Measurements and Their Applications*. Springer. 
   (The absolute definitive historical and technical text on the invention and deployment of PMUs).

2. **Proakis, J. G., & Manolakis, D. K. (2006).** *Digital Signal Processing: Principles, Algorithms, and Applications*. Pearson. 
   (Refer strictly to Chapter 7 for foundational theory on standard DFT leakage and frequency resolution).

3. **IEEE Standard C37.118.1-2011.** *IEEE Standard for Synchrophasor Measurements for Power Systems*. 
   (Mandatory reading for understanding exact TVE compliance bounds).

4. **IEEE Standard 519-2014.** *IEEE Recommended Practice and Requirements for Harmonic Control in Electric Power Systems*. 
   (Details acceptable THD limits for various grid voltage levels).

5. **IEC 61000-4-30.** *Testing and measurement techniques - Power quality measurement methods*. 
   (Global standard for implementing power quality monitoring algorithms in hardware).
</Faculty Notes — Lecture 26: DSP for Power Systems — Harmonic Analysis & Phasor Estimation>
