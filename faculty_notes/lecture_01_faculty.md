<Faculty Notes — Lecture 1: Discrete-Time Signals & Systems>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY

When introducing Digital Signal Processing (DSP) to III B.Tech EEE students, it is essential to build a solid bridge from their previous coursework in Continuous-Time (CT) Signals and Systems. A highly effective pedagogical strategy is to draw continuous-time and discrete-time (DT) signals side-by-side on the blackboard. 

Showing a physical continuous waveform, such as $x(t) = \cos(2\pi t)$, alongside its sampled sequence $x[n] = \cos(2\pi n T_s)$, instantly visualizes the discretization process. The act of explicitly drawing the stem plot helps students internalize that the independent variable is now an integer index $n$, rather than time $t$. 

A common and critical point of confusion at this stage is that students frequently equate "discrete" with "digital." You must explicitly clarify this terminology early and often:
* **Discrete-Time (DT):** The signal is discretized only in the time domain, meaning it is defined only at integer multiples of the sampling period. However, it still possesses continuous amplitude values. This is a purely mathematical construct used for analysis.
* **Digital:** A true "digital" signal must be discretized in both time (sampled) and amplitude (quantized). Emphasize that while analytical DSP math typically deals with discrete-time unquantized signals (treating amplitude with infinite precision), real-world hardware DSP always deals with digital signals subject to quantization noise.

### Suggested Demos for Lecture 1:
1. **Audio Sampling Demo:** Play an audio clip sampled at a high rate (e.g., 44.1 kHz, CD quality). Then, play the same clip downsampled to 8 kHz (telephone quality), and finally down to 2 kHz. This practically demonstrates the perceptual effects of discrete time intervals and aliasing if not properly filtered.
2. **Visual Python/MATLAB Script:** Show a continuous sine wave and overlay stem plots of it sampled at various rates (over-sampled, critically sampled, and under-sampled) to visually introduce the concept of the Nyquist limit before formally proving it later in the course.

---
## 1. LEARNING OBJECTIVES

By the end of this comprehensive lecture, students will be able to:
1. **Differentiate** explicitly between continuous-time, discrete-time, and true digital signals based on their properties in the time and amplitude domains.
2. **Decompose** any arbitrary discrete-time signal into its even (symmetric) and odd (anti-symmetric) components using formal mathematical definitions.
3. **Calculate** the total energy and average power of discrete-time signals using infinite series summations, and classify them strictly as energy signals, power signals, or neither.
4. **Determine** the periodicity condition for discrete-time sinusoidal and complex exponential sequences, and calculate the fundamental period $N$.
5. **Construct** and represent complex discrete-time signals using foundational elementary sequences such as the unit impulse, unit step, ramp, and real/complex exponentials.
6. **Perform** elementary signal operations including time shifting, time reversal, amplitude scaling, and integer time scaling (decimation/downsampling and interpolation/upsampling).
7. **Classify** discrete-time systems based on strict mathematical properties: linearity, time-invariance, causality, memory (dynamic/static), and stability properties using formal proofs.
8. **Analyze** and formally prove the Bounded-Input Bounded-Output (BIBO) stability of an LTI system based on the absolute summability condition of its impulse response.

---
## 2. PREREQUISITE KNOWLEDGE REVIEW

Before proceeding with the core DSP material in this lecture, ensure that students are comfortable with the following mathematical and engineering concepts. A brief 5-minute review on the board is highly recommended.

**1. Continuous-Time Signals and Systems:**
* Definition of the CT Dirac delta impulse $\delta(t)$ and the Heaviside step function $u(t)$.
* Superposition and the Convolution integral concepts from their second-year Signals and Systems courses.

**2. Complex Exponentials and Euler's Formula:**
* Students must fluently use Euler's formula to decompose complex sinusoids into real orthogonal components:
  $$ e^{j\theta} = \cos(\theta) + j\sin(\theta) $$
* And conversely, express real sinusoids as sums of complex exponentials:
  $$ \cos(\theta) = \frac{e^{j\theta} + e^{-j\theta}}{2} $$
  $$ \sin(\theta) = \frac{e^{j\theta} - e^{-j\theta}}{2j} $$

**3. Geometric Series Summation Formulas:**
These are absolutely critical. Without memorizing these, students will fail to compute signal energy, power, and later, the Z-Transform.
* **Finite geometric series sum:**
  $$ \sum_{n=0}^{N-1} a^n = \frac{1 - a^N}{1 - a}, \quad \text{for } a \neq 1 $$
* **Infinite geometric series sum:**
  $$ \sum_{n=0}^{\infty} a^n = \frac{1}{1 - a}, \quad \text{strictly for } |a| < 1 $$
* *Review these formulas explicitly on the board, as they are the primary mathematical tool for energy and power classification calculations.*

**4. Basic Linear Algebra & Complex Calculus:**
* Familiarity with limits at infinity.
* Understanding absolute values and magnitudes of complex numbers, specifically that the magnitude of any purely complex exponential is unity: $|e^{j\theta}| = 1$.

---
## 3. HISTORICAL AND MOTIVATIONAL CONTEXT

Why does an Electrical Engineering student need to study Digital Signal Processing? The transition from analog circuits to digital algorithms has revolutionized communication, control, power systems, and instrumentation over the last few decades.

**Historical Milestones:**
* **1948 - Shannon's Sampling Theorem:** Claude Shannon formalized the Nyquist-Shannon sampling theorem, proving that a continuous, bandlimited signal can be perfectly and exactly reconstructed from its discrete samples provided the sampling frequency is strictly greater than twice the maximum frequency present in the signal.
* **1965 - Cooley-Tukey FFT Algorithm:** James Cooley and John Tukey published an algorithm for the Fast Fourier Transform (FFT), reducing the computational complexity of calculating the Discrete Fourier Transform (DFT) from $O(N^2)$ to $O(N \log_2 N)$. This algorithmic breakthrough is what made real-time DSP practical on early computers.
* **Early Digital Audio (1970s-80s):** The invention of the Compact Disc (CD) using a 44.1 kHz sampling rate and 16-bit Pulse Code Modulation (PCM) audio was the first mass-market, consumer-level application of complex DSP theory.

**Modern Applications in Electrical Engineering:**
* **5G & Wireless Communications:** The entire baseband signal processing chain, OFDM (Orthogonal Frequency-Division Multiplexing) modulation, channel equalization, and error correction coding are executed purely via DSP algorithms on dedicated ASICs or FPGAs.
* **Smart Grids & Power Quality Analysis:** Phasor Measurement Units (PMUs) sample power grid voltages and currents at very high rates. They use DSP algorithms to compute harmonic distortion, active/reactive power, and detect transient faults in real-time.
* **Biomedical Instrumentation:** ECG and EEG machines sample extremely faint biological signals (often in the microvolt range). They rely heavily on DSP filtering (like digital notch filters) to remove 50 Hz or 60 Hz power-line interference without distorting the underlying medical data.

---
## 4. THEORETICAL FOUNDATIONS

### 4.1 Classification of DT Signals

#### Energy vs. Power Signals
A physical signal carries energy. In DSP, we evaluate the normalized energy (assuming a 1 Ohm reference resistance for simplicity).

The **total energy** $E$ of a discrete-time signal $x[n]$ is defined over all of time (from negative infinity to positive infinity) as the sum of the squared magnitudes:
$$ E = \sum_{n=-\infty}^{\infty} |x[n]|^2 $$

The **average power** $P$ is the average rate of energy delivery over time. It is defined via a symmetric limit as the observation window $N$ approaches infinity:
$$ P = \lim_{N \to \infty} \frac{1}{2N + 1} \sum_{n=-N}^{N} |x[n]|^2 $$
Note that the denominator $2N+1$ represents the total number of samples in the symmetric interval $[-N, N]$.

**Strict Classification Conditions:**
* **Energy Signal:** A signal is classified as an energy signal if and only if its total energy is finite and non-zero: $0 < E < \infty$. 
  * *Consequence:* If the total energy is finite, the average power spread over infinite time must logically be zero ($P = 0$). 
  * *Examples:* Finite duration sequences, transient pulses, and exponentially decaying sequences.
* **Power Signal:** A signal is classified as a power signal if and only if its average power is finite and non-zero: $0 < P < \infty$. 
  * *Consequence:* If a signal maintains non-zero average power over infinite time, its total accumulated energy must logically be infinite ($E = \infty$). 
  * *Examples:* Periodic sequences, continuous sinusoids, and the unit step function $u[n]$.
* **Neither:** Signals like $x[n] = 2^n u[n]$ (an exponentially growing sequence) have both infinite energy and infinite average power, thus falling into neither category.

#### Periodic vs. Aperiodic Signals
A discrete-time sequence $x[n]$ is periodic if there exists an integer $N > 0$ such that the sequence repeats exactly:
$$ x[n + N] = x[n] \quad \text{for all } n $$
The smallest such strictly positive integer $N$ is called the **fundamental period**.
If absolutely no such integer exists, the sequence is termed **aperiodic**.

**Complete Proof of Periodicity Condition for Complex Exponentials:**
Consider the complex exponential sequence $x[n] = e^{j\omega_0 n}$.
For this sequence to be periodic with period $N$, it must satisfy the definition:
$$ e^{j\omega_0 (n + N)} = e^{j\omega_0 n} $$
By expanding the exponent:
$$ e^{j\omega_0 n} \cdot e^{j\omega_0 N} = e^{j\omega_0 n} $$
Dividing both sides by the non-zero term $e^{j\omega_0 n}$, we require:
$$ e^{j\omega_0 N} = 1 $$
From Euler's identity, we know that $e^{j \theta} = 1$ if and only if $\theta$ is an integer multiple of $2\pi$. Therefore:
$$ \omega_0 N = 2\pi m \quad \text{for some integer } m $$
Rearranging this to solve for the relationship between the frequency $\omega_0$ and the period $N$:
$$ \frac{\omega_0}{2\pi} = \frac{m}{N} $$
This is a profound result in DSP. It states that for a discrete-time sinusoid or complex exponential to be periodic, its normalized frequency $f_0 = \omega_0 / (2\pi)$ **must be a rational number** (a ratio of two integers $m$ and $N$). 
If, for example, $\omega_0 = 1$ rad/sample, then $\omega_0/(2\pi) = 1/(2\pi)$, which is an irrational number. Thus, the sequence $\cos(n)$ is **aperiodic**, which is a stark contrast to the continuous-time domain where $\cos(t)$ is always periodic.

#### Even and Odd Symmetry (Decomposition Theorem)
Every arbitrary discrete-time signal $x[n]$ can be uniquely decomposed into an Even (symmetric) part $x_e[n]$ and an Odd (anti-symmetric) part $x_o[n]$.
* **Even Signal Definition:** $x[-n] = x[n]$ for all $n$.
* **Odd Signal Definition:** $x[-n] = -x[n]$ for all $n$. (Note a critical implication: at $n=0$, $x_o[0] = -x_o[0]$, which mandates that $x_o[0] = 0$).

**Complete Proof of the Decomposition Theorem:**
Let us assume that any signal $x[n]$ can be written as the sum of an even and an odd component:
$$ x[n] = x_e[n] + x_o[n] \quad \text{--- (Equation 1)} $$
Now, let's substitute $-n$ for $n$ to evaluate the time-reversed signal:
$$ x[-n] = x_e[-n] + x_o[-n] $$
Apply the fundamental definitions of even and odd signals ($x_e[-n] = x_e[n]$ and $x_o[-n] = -x_o[n]$):
$$ x[-n] = x_e[n] - x_o[n] \quad \text{--- (Equation 2)} $$
We now possess a simple linear system of two equations. 
Adding (Equation 1) and (Equation 2) together cancels the odd component:
$$ x[n] + x[-n] = 2 x_e[n] \implies x_e[n] = \frac{1}{2}(x[n] + x[-n]) $$
Subtracting (Equation 2) from (Equation 1) cancels the even component:
$$ x[n] - x[-n] = 2 x_o[n] \implies x_o[n] = \frac{1}{2}(x[n] - x[-n]) $$
This formally proves that any signal can be constructed from these derived even and odd components.

### 4.2 Elementary DT Signals
These mathematical sequences are the foundational primitive building blocks of all DSP theory.

**1. Unit Impulse Sequence $\delta[n]$:**
This is the most important signal in DSP, analogous to the Dirac delta in CT, but much simpler because it is finite and well-behaved.
$$ \delta[n] = \begin{cases} 1, & n = 0 \\ 0, & n \neq 0 \end{cases} $$

*Complete Proof of the Sifting Property:*
We wish to evaluate the infinite summation: $\sum_{k=-\infty}^{\infty} x[k] \delta[n-k]$.
Examine the term $\delta[n-k]$. Based on its definition, this shifted impulse is exactly zero everywhere EXCEPT when its argument is zero, i.e., when $n - k = 0$, which implies $k = n$.
Therefore, as the summation index $k$ sweeps from $-\infty$ to $\infty$, every single term in the sum is multiplied by $0$, and thus vanishes, EXCEPT the single specific term where $k=n$.
At $k=n$, the term becomes $x[n] \delta[n-n] = x[n] \delta[0] = x[n] \times 1 = x[n]$.
Therefore:
$$ \sum_{k=-\infty}^{\infty} x[k] \delta[n-k] = x[n] $$
This profound result proves that any arbitrary discrete sequence can be viewed simply as a weighted sum of shifted unit impulses.

**2. Unit Step Sequence $u[n]$:**
The discrete counterpart to the Heaviside step function.
$$ u[n] = \begin{cases} 1, & n \ge 0 \\ 0, & n < 0 \end{cases} $$
*Relationship to the Impulse:* 
The impulse is the first difference (discrete derivative) of the step: $\delta[n] = u[n] - u[n-1]$.
The step is the running sum (discrete integral) of the impulse: $u[n] = \sum_{k=-\infty}^{n} \delta[k] = \sum_{k=0}^{\infty} \delta[n-k]$.

**3. Real Exponential Sequence $x[n] = a^n u[n]$:**
Where $a$ is a real number. The system's behavior is dictated entirely by $a$:
* $0 < a < 1$: A smoothly decaying exponential (stable).
* $-1 < a < 0$: A decaying sequence that oscillates in sign every single sample (stable).
* $|a| > 1$: An unbounded growing sequence (unstable).

**4. Complex Exponential Sequence $x[n] = e^{j\omega_0 n}$:**
By Euler's identity: $e^{j\omega_0 n} = \cos(\omega_0 n) + j\sin(\omega_0 n)$.
As rigorously proven in the previous section, this sequence is periodic if and only if $\frac{\omega_0}{2\pi}$ is a rational number.

### 4.3 Signal Operations
Transformations manipulating the independent integer variable $n$.

**1. Time Shifting:**
Defined as $y[n] = x[n - k]$, where $k$ is an integer.
* If $k > 0$, the signal is **delayed**. The waveform shifts to the right on the time axis.
* If $k < 0$, the signal is **advanced**. The waveform shifts to the left on the time axis.

**2. Time Reversal (Folding):**
Defined as $y[n] = x[-n]$. The signal is mirrored symmetrically across the y-axis (the origin $n=0$).

**3. Time Scaling:**
In continuous time, scaling by any real factor $c$ is possible ($x(ct)$). In discrete time, because $n$ must remain an integer, we can only scale time by an integer factor $M$ or $L$.
* **Decimation (Subsampling/Downsampling):** $y[n] = x[Mn]$, where $M$ is a positive integer. We extract and keep only every $M$-th sample, permanently discarding all the intermediate samples. This compresses the signal in the time domain, but inherently loses information and can cause frequency aliasing if the signal is not low-pass filtered beforehand.
* **Interpolation (Upsampling):** 
  $$ y[n] = \begin{cases} x[n/L], & \text{if } n \text{ is an integer multiple of } L \\ 0, & \text{otherwise} \end{cases} $$
  This operation expands the signal in time by inserting exactly $L-1$ zeros between every pair of original samples.

**4. Amplitude Scaling:**
$y[n] = A \cdot x[n]$. This simply amplifies ($|A|>1$) or attenuates ($|A|<1$) the signal magnitude.

### 4.4 System Classification
A discrete-time system, denoted by the operator $T\{\cdot\}$, is a mathematical algorithm that maps an input sequence $x[n]$ to an output sequence $y[n]$: $y[n] = T\{x[n]\}$.

**1. Linearity:**
A system is strictly linear if and only if it satisfies the Principle of Superposition, which encompasses both Additivity and Homogeneity (scaling).
For any two inputs $x_1[n]$ and $x_2[n]$, and any two complex constants $a$ and $b$:
$$ T\{a x_1[n] + b x_2[n]\} = a T\{x_1[n]\} + b T\{x_2[n]\} $$

**2. Time-Invariance (Shift-Invariance):**
A system is time-invariant if introducing a delay in the input sequence causes an identical delay in the output sequence, without altering the shape or characteristics of the output in any way.
Formal test method (Shift-and-Test):
* Step 1: Apply a shifted input $x_1[n] = x[n - k]$. Calculate the intermediate response $y_1[n] = T\{x_1[n]\}$.
* Step 2: Take the standard output $y[n]$ and explicitly delay its index by $k$ to yield $y[n - k]$.
* Step 3: Check for equality. If $y_1[n] = y[n - k]$ for all valid $n$ and $k$, the system is strictly Time-Invariant (TI).

**3. Causality:**
A system is causal if the output $y[n_0]$ at any given instant $n_0$ depends exclusively on present and past inputs (i.e., $x[n]$ where $n \le n_0$). It cannot look into the future.
For a Linear Time-Invariant (LTI) system characterized entirely by its impulse response $h[n]$, causality strictly requires:
$$ h[n] = 0 \quad \text{for all } n < 0 $$

**4. Memory (Dynamic vs. Static):**
A system is memoryless (static) if the output $y[n_0]$ at time $n_0$ depends strictly and exclusively on the input $x[n_0]$ at that exact same instant. It cannot use past or future values.
For an LTI system, it is memoryless if and only if its impulse response is merely a scaled impulse: $h[n] = c \cdot \delta[n]$, where $c$ is a constant.

**5. BIBO Stability:**
Bounded-Input Bounded-Output (BIBO) stability requires that for any input sequence that is bounded in magnitude (there exists a finite $M_x$ such that $|x[n]| \le M_x < \infty$ for all $n$), the resulting output sequence must also be strictly bounded in magnitude (there exists a finite $M_y$ such that $|y[n]| \le M_y < \infty$).
For an LTI system, this requires the impulse response to be absolutely summable.

---
## 5. COMPLETE PROOFS AND DERIVATIONS

### 5.1 Proof of Parseval's Theorem for Energy Signals in Time Domain
While Parseval's relation is often used to connect the time domain and frequency domain (Fourier Transform), purely within the time domain, we must prove that the total energy of a sequence is fundamentally invariant to simple time shifts.
Let an original signal $x[n]$ have energy $E_x$.
Let a delayed signal be $y[n] = x[n - N_0]$. We wish to find its energy $E_y$.
$$ E_y = \sum_{n=-\infty}^{\infty} |y[n]|^2 = \sum_{n=-\infty}^{\infty} |x[n - N_0]|^2 $$
To solve this, we perform a change of variables on the summation index. 
Let $m = n - N_0$. 
Determine the new summation limits: As $n \to \infty$, the new index $m \to \infty$. As $n \to -\infty$, the new index $m \to -\infty$.
Substituting $m$ into the summation:
$$ E_y = \sum_{m=-\infty}^{\infty} |x[m]|^2 $$
By definition, this expression is exactly the energy of the original signal $E_x$.
$$ E_y = E_x $$
Therefore, shifting a signal in time does not create or destroy energy. Energy is time-shift invariant.

### 5.2 Complete BIBO Stability Proof for LTI Systems
This is a critical proof for EEE students, as stability is paramount in control systems and filter design.
**Theorem:** A Linear Time-Invariant (LTI) system, characterized by its impulse response sequence $h[n]$, is Bounded-Input Bounded-Output (BIBO) stable if and only if the impulse response is absolutely summable: $\sum_{k=-\infty}^{\infty} |h[k]| < \infty$.

**Proof of Sufficiency (The "If" part):**
We must prove that if the condition holds, the system is stable.
Assume the condition is met: $\sum_{k=-\infty}^{\infty} |h[k]| = S < \infty$.
Let the input sequence $x[n]$ be bounded by some finite maximum value $M_x$, such that $|x[n]| \le M_x < \infty$ for all $n$.
The output of an LTI system is given by the convolution sum formula:
$$ y[n] = \sum_{k=-\infty}^{\infty} h[k] x[n-k] $$
To analyze stability, we take the absolute magnitude of both sides:
$$ |y[n]| = \left| \sum_{k=-\infty}^{\infty} h[k] x[n-k] \right| $$
Apply the generalized triangle inequality (the absolute value of a sum is always less than or equal to the sum of absolute values):
$$ |y[n]| \le \sum_{k=-\infty}^{\infty} |h[k] x[n-k]| = \sum_{k=-\infty}^{\infty} |h[k]| \cdot |x[n-k]| $$
Since we established that the input is globally bounded by $M_x$, we can replace $|x[n-k]|$ with its maximum possible value $M_x$ to create a strict upper bound:
$$ |y[n]| \le \sum_{k=-\infty}^{\infty} |h[k]| \cdot M_x $$
We can factor $M_x$ outside the summation since it is a constant independent of $k$:
$$ |y[n]| \le M_x \sum_{k=-\infty}^{\infty} |h[k]| $$
Substituting our initial assumption that the sum equals $S$:
$$ |y[n]| \le M_x \cdot S $$
Since $M_x$ is a finite number, and $S$ is a finite number, their product $M_x \cdot S$ is also finite. 
Thus, $|y[n]| < \infty$. We have proven that the output is bounded. The condition is sufficient for stability.

**Proof of Necessity (The "Only If" part):**
We must now prove the converse: that if the sum is infinite, the system is fundamentally unstable. We do this by contradiction/construction.
Assume the condition is violated: $\sum_{k=-\infty}^{\infty} |h[k]| = \infty$.
We must construct a specific, malicious bounded input sequence that forces the output to blow up to infinity.
Let us define our input sequence precisely as:
$$ x[n] = \begin{cases} \frac{h^*[-n]}{|h[-n]|}, & \text{if } h[-n] \neq 0 \\ 0, & \text{if } h[-n] = 0 \end{cases} $$
*(Note: $h^*$ denotes the complex conjugate).*
First, verify this input is bounded. The magnitude $|x[n]|$ is the magnitude of a complex number divided by itself, which is exactly $1$. Thus, $|x[n]| \le 1$ for all valid $n$. The input is bounded ($M_x = 1$).
Now, evaluate the system output exactly at the specific time instant $n=0$:
$$ y[0] = \sum_{k=-\infty}^{\infty} h[k] x[0-k] = \sum_{k=-\infty}^{\infty} h[k] x[-k] $$
Substitute our carefully constructed definition of $x[-k]$ into the sum:
$$ y[0] = \sum_{k=-\infty}^{\infty} h[k] \left( \frac{h^*[k]}{|h[k]|} \right) $$
Recall the property of complex numbers that a number multiplied by its conjugate equals its magnitude squared: $h[k] h^*[k] = |h[k]|^2$.
Substituting this in:
$$ y[0] = \sum_{k=-\infty}^{\infty} \frac{|h[k]|^2}{|h[k]|} = \sum_{k=-\infty}^{\infty} |h[k]| $$
According to our initial assumption, this summation evaluates to infinity.
Therefore, $y[0] = \infty$.
Even though we fed the system a perfectly bounded input (maximum amplitude of 1), the system produced an infinite, unbounded output. 
Hence, finite absolute summability is strictly necessary for BIBO stability. The proof is complete.

---
## 6. WORKED EXAMPLES (MINIMUM 5 — fully solved)

### Example 1: Comprehensive Energy and Power Calculation
**Problem statement:** Classify the sequence $x[n] = (0.8)^{|n|}$ as an energy signal or a power signal. Compute its corresponding valid metric (energy or power) in Joules or Watts.
**Solution:**
First, visually inspect the signal. Since the magnitude of the exponential base is $0.8 < 1$, the signal decays exponentially towards zero as $n$ approaches both $+\infty$ and $-\infty$. Signals that decay to zero generally possess finite energy. We will test it as an energy signal.
The total energy formula is:
$$ E = \sum_{n=-\infty}^{\infty} |x[n]|^2 $$
Substitute the signal definition:
$$ E = \sum_{n=-\infty}^{\infty} \left((0.8)^{|n|}\right)^2 = \sum_{n=-\infty}^{\infty} (0.64)^{|n|} $$
Because of the absolute value $|n|$ in the exponent, the function is symmetric around $n=0$. We must split this infinite summation into three distinct parts: strictly negative indices, the origin, and strictly positive indices.
$$ E = \sum_{n=-\infty}^{-1} (0.64)^{-n} + (0.64)^0 + \sum_{n=1}^{\infty} (0.64)^n $$
Evaluate the origin term: $(0.64)^0 = 1$.
For the negative summation, perform a change of variable. Let $m = -n$. The bounds change from $n=-\infty \to -1$ to $m=\infty \to 1$.
$$ \sum_{n=-\infty}^{-1} (0.64)^{-n} = \sum_{m=1}^{\infty} (0.64)^m $$
Since $m$ is just a dummy index, we can rename it back to $n$. Notice that the negative sum is exactly identical to the positive sum.
$$ E = \left( \sum_{n=1}^{\infty} (0.64)^n \right) + 1 + \left( \sum_{n=1}^{\infty} (0.64)^n \right) = 1 + 2 \sum_{n=1}^{\infty} (0.64)^n $$
Now, we must evaluate the infinite geometric series. The standard formula $\sum_{n=0}^{\infty} a^n = \frac{1}{1-a}$ starts at $n=0$. Our series starts at $n=1$. 
We can adapt the formula by factoring out one term of $a$: 
$$ \sum_{n=1}^{\infty} a^n = a \sum_{n=0}^{\infty} a^n = \frac{a}{1-a} $$
Let $a = 0.64$.
$$ \sum_{n=1}^{\infty} (0.64)^n = \frac{0.64}{1 - 0.64} = \frac{0.64}{0.36} $$
Simplify the fraction by dividing numerator and denominator by 4:
$$ \frac{64}{36} = \frac{16}{9} $$
Substitute this back into the total energy equation:
$$ E = 1 + 2\left(\frac{16}{9}\right) = 1 + \frac{32}{9} = \frac{9}{9} + \frac{32}{9} = \frac{41}{9} \text{ Joules}. $$
Since the calculated energy is a finite, non-zero number ($0 < E < \infty$), the sequence is formally classified as an **Energy Signal**.
By definition, its average power over infinite time is $P = 0$.
**Physical interpretation:** This mathematical sequence represents a two-sided exponentially decaying transient, similar to the voltage across a capacitor discharging in both forward and reverse time analysis.
**Common mistakes to avoid:** Students frequently forget that $|n|$ requires splitting the sum and accidentally apply the geometric sum formula blindly from $-\infty$, which leads to divergent, incorrect answers. Another common error is using the standard geometric series formula starting from $n=0$ when the isolated sum actually starts at $n=1$.

### Example 2: Determining Periodicity of a Composite Signal
**Problem statement:** Determine whether the composite sequence $x[n] = \cos(0.2\pi n) + \sin(0.3\pi n)$ is periodic. If it is periodic, calculate its fundamental period $N$.
**Solution:**
A linear combination of periodic signals is periodic if and only if the ratio of their individual periods is a rational number.
Step 1: Analyze the first component, $x_1[n] = \cos(0.2\pi n)$.
The angular frequency is $\omega_1 = 0.2\pi$.
Check the periodicity condition $f_1 = \omega_1 / (2\pi)$:
$$ f_1 = \frac{0.2\pi}{2\pi} = \frac{0.2}{2} = \frac{1}{10} $$
Because $1/10$ is a rational fraction of integers ($m_1=1, N_1=10$), the sequence $x_1[n]$ is periodic with an individual fundamental period of $N_1 = 10$ samples.

Step 2: Analyze the second component, $x_2[n] = \sin(0.3\pi n)$.
The angular frequency is $\omega_2 = 0.3\pi$.
Check the periodicity condition $f_2 = \omega_2 / (2\pi)$:
$$ f_2 = \frac{0.3\pi}{2\pi} = \frac{0.3}{2} = \frac{3}{20} $$
Because $3/20$ is a rational fraction of integers ($m_2=3, N_2=20$), the sequence $x_2[n]$ is periodic with an individual fundamental period of $N_2 = 20$ samples.

Step 3: Check the ratio of the periods.
Ratio = $N_1 / N_2 = 10 / 20 = 1 / 2$.
Since this ratio is a rational number, the sum of the two signals is indeed periodic.

Step 4: Calculate the composite fundamental period.
The overall fundamental period $N$ is the Least Common Multiple (LCM) of the individual periods $N_1$ and $N_2$.
$$ N = \text{LCM}(10, 20) $$
The smallest integer that is perfectly divisible by both 10 and 20 is 20.
$$ N = 20 \text{ samples}. $$
**Physical interpretation:** The first waveform completes exactly 2 full cycles in 20 samples. The second waveform completes exactly 3 full cycles in 20 samples. Therefore, every 20 samples, both waveforms return precisely to their initial starting phases simultaneously, causing the composite sum waveform to repeat exactly.

### Example 3: The Aperiodic Discrete Sinusoid
**Problem statement:** Prove whether the sequence $x[n] = \cos(n)$ is periodic or aperiodic.
**Solution:**
Identify the angular frequency from the argument. The sequence is of the form $\cos(\omega_0 n)$. Therefore, $\omega_0 = 1$ radian/sample.
Apply the strict discrete-time periodicity condition. For a sinusoid to be periodic, the normalized frequency must be a rational number.
$$ \frac{\omega_0}{2\pi} = \frac{1}{2\pi} $$
We know that $\pi$ is a transcendental irrational number ($\approx 3.14159...$). Therefore, the fraction $1/(2\pi)$ is fundamentally irrational.
It is impossible to find two integers $m$ and $N$ such that $1/(2\pi) = m/N$.
Therefore, no integer period $N$ exists.
The signal is formally classified as **Aperiodic**.
**Physical interpretation:** Imagine a continuous 1 Hz sine wave. If you sample it at exactly 1 sample per second, you get a DC flat line (aliasing). If you sample it at a rate that is not a rational multiple of $\pi$, the discrete sample points will slide slightly along the sine wave on every cycle. They will never perfectly align with the exact same phase angles in any future cycle, meaning the discrete sequence of numbers never repeats identically.

### Example 4: Even and Odd Decomposition of a Non-Symmetric Signal
**Problem statement:** Mathematically decompose the unit step sequence $x[n] = u[n]$ into its even ($x_e[n]$) and odd ($x_o[n]$) symmetric parts. Detail the values for all $n$ and provide a mathematical expression.
**Solution:**
First, establish the definitions of the original sequence and its time-reversed version.
* Original sequence $u[n]$: Evaluates to $1$ for $n \ge 0$, and $0$ for $n < 0$.
* Time-reversed sequence $u[-n]$: Evaluates to $1$ for $n \le 0$, and $0$ for $n > 0$.
*(Crucial observation: Both sequences equal 1 at the origin, $n=0$. They overlap).*

**Step 1: Calculate the Even part $x_e[n]$**
Formula: $x_e[n] = \frac{1}{2}(u[n] + u[-n])$
We evaluate this piecewise for three regions:
* For strictly positive time ($n > 0$): $u[n] = 1, u[-n] = 0$.
  $$ x_e[n] = \frac{1 + 0}{2} = 0.5 $$
* For strictly negative time ($n < 0$): $u[n] = 0, u[-n] = 1$.
  $$ x_e[n] = \frac{0 + 1}{2} = 0.5 $$
* Exactly at the origin ($n = 0$): $u[0] = 1, u[-0] = u[0] = 1$.
  $$ x_e[0] = \frac{1 + 1}{2} = \frac{2}{2} = 1.0 $$
Summary for Even Part: The sequence equals $0.5$ everywhere from $-\infty$ to $\infty$, except at the origin where it peaks at $1.0$.
Mathematical representation: A constant DC level of $0.5$ plus an impulse of height $0.5$ at the origin.
$$ x_e[n] = 0.5 + 0.5\delta[n] $$

**Step 2: Calculate the Odd part $x_o[n]$**
Formula: $x_o[n] = \frac{1}{2}(u[n] - u[-n])$
Evaluate piecewise:
* For strictly positive time ($n > 0$): $u[n] = 1, u[-n] = 0$.
  $$ x_o[n] = \frac{1 - 0}{2} = 0.5 $$
* For strictly negative time ($n < 0$): $u[n] = 0, u[-n] = 1$.
  $$ x_o[n] = \frac{0 - 1}{2} = -0.5 $$
* Exactly at the origin ($n = 0$): $u[0] = 1, u[-0] = 1$.
  $$ x_o[0] = \frac{1 - 1}{2} = 0 $$
Summary for Odd Part: The sequence is $-0.5$ for negative time, $0$ at the origin, and $0.5$ for positive time.
Mathematical representation: This is half the signum function.
$$ x_o[n] = 0.5 \text{ sgn}(n) $$
**Verification:** Does $x_e[n] + x_o[n] = u[n]$?
At $n > 0$: $0.5 + 0.5 = 1$. Correct.
At $n < 0$: $0.5 + (-0.5) = 0$. Correct.
At $n = 0$: $1.0 + 0 = 1$. Correct.
**Common mistakes:** Students frequently assume that $u[-n]$ is 0 at the origin, incorrectly assuming it perfectly mirrors the positive side without overlapping. Emphasize that $u[0]$ and $u[-0]$ are the exact same sample.

### Example 5: Rigorous Testing of System Linearity and Time-Invariance
**Problem statement:** A discrete-time system is defined by the input-output relationship $y[n] = x[n^2]$. Conduct formal mathematical tests to determine if the system is strictly linear, and if it is strictly time-invariant.
**Solution:**
**1. Linearity Test:**
We must prove that $T\{a x_1[n] + b x_2[n]\} = a T\{x_1[n]\} + b T\{x_2[n]\}$.
* Step A: Apply a scaled composite input to the system.
  Let $x_3[n] = a x_1[n] + b x_2[n]$.
  The system squares the time index of whatever is passed into it. Therefore, the output is:
  $$ y_3[n] = T\{x_3[n]\} = x_3[n^2] $$
  Substitute the definition of $x_3$ evaluated at $n^2$:
  $$ y_3[n] = a x_1[n^2] + b x_2[n^2] \quad \text{--- (Result A)} $$
* Step B: Calculate the weighted sum of the individual system responses.
  The individual responses are $y_1[n] = x_1[n^2]$ and $y_2[n] = x_2[n^2]$.
  The weighted sum is:
  $$ a y_1[n] + b y_2[n] = a x_1[n^2] + b x_2[n^2] \quad \text{--- (Result B)} $$
* Step C: Compare. Since Result A equals Result B for all inputs and constants, Superposition holds.
The system is **Linear**.

**2. Time-Invariance Test (Shift-and-Test):**
We must prove that $T\{x[n-k]\} = y[n-k]$.
* Step A: Shift the input signal before applying it to the system.
  Define an intermediate delayed signal $x_1[n] = x[n - k]$.
  Apply this to the system. The system replaces the index 'n' with '$n^2$'.
  $$ y_1[n] = T\{x_1[n]\} = x_1[n^2] $$
  Substitute the definition of $x_1$ evaluated at $n^2$:
  $$ y_1[n] = x[n^2 - k] \quad \text{--- (Result A)} $$
* Step B: Apply the system first, then shift the final output.
  The normal output is $y[n] = x[n^2]$.
  Now, replace every instance of the independent variable $n$ with $(n - k)$ to explicitly delay the output sequence.
  $$ y[n - k] = x[(n - k)^2] $$
  Expand the algebraic square:
  $$ y[n - k] = x[n^2 - 2nk + k^2] \quad \text{--- (Result B)} $$
* Step C: Compare.
  $x[n^2 - k]$ is clearly mathematically distinct from $x[n^2 - 2nk + k^2]$. They are not equal.
Therefore, the system is **Time-Varying**.
**Physical interpretation:** The time-warping effect of squaring the index means that a signal entering the system at $n=0$ behaves very differently than a signal entering the system at $n=5$. The delay experienced at the input is subjected to severe non-linear distortion at the output depending on absolute time, utterly breaking shift-invariance.

---
## 7. ENGINEERING APPLICATIONS AND CASE STUDIES

To keep EEE students engaged, DSP must be tied to physical hardware and real-world systems.

**1. Speech Coding in GSM Telecommunications**
In classic digital telephony (like GSM 2G networks), human speech must be transmitted efficiently. The raw vocal frequencies range up to about 4 kHz. 
* **Analog Pre-filtering:** The microphone analog signal is first strictly bandlimited to 3.4 kHz using an active analog low-pass filter (anti-aliasing). 
* **Sampling:** It is then sampled at exactly 8 kHz, which perfectly satisfies the Nyquist rate ($8 \text{ kHz} > 2 \times 3.4 \text{ kHz}$). 
* **Quantization:** The discrete-time samples are quantized using a logarithmic 8-bit non-linear ADC algorithm (such as A-law in Europe or $\mu$-law in the US) to compress dynamic range. 
* **DSP:** Digital signal processing algorithms then compress these samples using Linear Predictive Coding (LPC). LPC models the human vocal tract mathematically as a digital IIR filter, sending only the filter coefficients rather than the raw audio data, massively reducing the required radio bandwidth.

**2. ECG Monitoring and Power-Line Interference Rejection**
An electrocardiogram (ECG) measures the heart's electrical polarization. The raw analog signal is extremely weak, typically in the range of 1 to 5 millivolts. When long electrode wires are attached to a patient's chest, they act as large antennas, readily coupling with the 50 Hz (or 60 Hz) electromagnetic field radiated by the hospital's AC power mains lighting and equipment.
* **Sampling:** The analog signal is amplified and sampled using a high-precision 12-bit ADC at a rate of 250 Hz. 
* **Filtering:** An analog filter cannot easily remove exactly 50 Hz without destroying the 40-60 Hz biomedical data. Instead, a discrete-time infinite impulse response (IIR) notch filter is implemented via a DSP microprocessor. The algorithm is designed to place a sharp zero exactly on the unit circle at the digital frequency corresponding to 50 Hz, perfectly nullifying the power-line interference without distorting the crucial low-frequency P-Q-R-S-T heart wave data.

**3. Digital Control Systems (Grid-Tied Inverters)**
In modern EEE applications, a solar power inverter converting DC battery power to AC grid power uses a microcontroller or DSP chip to generate a Pulse Width Modulated (PWM) signal. 
* **Reference Generation:** The perfect reference sine wave is generated entirely in software as a discrete-time sequence: $x[n] = \sin(2\pi f_{grid} n / f_s)$. 
* **Control Loop:** A discrete-time Proportional-Integral (PI) control algorithm continuously evaluates the error sequence $e[n]$ between the mathematically generated reference voltage and the physically measured output voltage via an ADC. The DSP calculates the exact required PWM duty cycle $d[n]$ at each sample interval (often at 20 kHz). This requires absolute algorithmic causality (you cannot use future error states) and extremely fast real-time execution.

---
## 8. COMMON STUDENT MISCONCEPTIONS AND ERRORS

1. **"Discrete-Time implies Digital."**
   * *The Misconception:* Students use the terms interchangeably, assuming any sequence written as $x[n]$ is ready for a computer.
   * *The Correction:* Emphasize that a discrete-time signal $x[n]$ is a mathematical abstraction with infinite precision amplitude. It becomes "digital" only after passing through a quantizer which maps the continuous amplitude to discrete binary levels, introducing quantization noise.
2. **"Complex exponentials $e^{j\omega_0 n}$ are unconditionally periodic."**
   * *The Misconception:* Students blindly carry over Continuous-Time logic, where $e^{j\omega_0 t}$ is always periodic for absolutely any real value of $\omega_0$.
   * *The Correction:* Reinforce the derivation. In DT, the normalized frequency $f = \omega_0 / (2\pi)$ must be a perfectly rational fraction. If it is irrational, the discrete samples walk continuously along the phase angle and never identically repeat a full period.
3. **"The total energy of the unit step $u[n]$ is simply 1 Joule."**
   * *The Misconception:* Looking at a plot of $u[n]$ and mistaking its amplitude of 1 for its total accumulated energy.
   * *The Correction:* Total energy is an infinite sum of squared magnitudes. $\sum_{n=0}^{\infty} 1^2 = 1 + 1 + 1 + \dots = \infty$. Thus $u[n]$ is mathematically an infinite-energy power signal, not an energy signal.
4. **"Discrete Decimation (Downsampling) by $M$ is identical to Continuous Time Scaling."**
   * *The Misconception:* Thinking $x[2n]$ merely plays the digital audio file twice as fast, just like speeding up an analog tape, with no side effects.
   * *The Correction:* In DT, decimation brutally discards samples. $x[2n]$ deletes all odd-indexed samples. This permanently destroys information and causes severe frequency aliasing if the signal is not subjected to an anti-aliasing low-pass filter prior to decimation.
5. **"Time-shifting a time-reversed signal $x[-n]$ by $k$ yields $x[-n-k]$."**
   * *The Misconception:* Careless algebraic substitution without thinking about the independent variable.
   * *The Correction:* When dealing with operations on mirrored signals, you must explicitly replace the fundamental independent variable $n$ with $(n-k)$. This results in $x[-(n-k)] = x[-n+k]$. This mathematically shifts the signal in the opposite direction than intuition would suggest.

---
## 9. CONNECTIONS TO OTHER LECTURES
* **Builds upon prior knowledge from:** Continuous-time Signals and Systems courses, specifically Fourier Series properties, continuous Convolution integrals, and Laplace Transforms.
* **Prepares the foundation for:**
  * **Lecture 2 & 3 (The Z-Transform):** The Z-Transform is the discrete-time equivalent of the Laplace transform. It fundamentally requires absolute mastery of the infinite geometric series summations and causality concepts introduced today to calculate Regions of Convergence (ROC).
  * **Lecture 4 & 5 (Discrete Fourier Transform):** The concept of periodicity of complex exponentials and rational frequency relationships discussed today is the absolute mathematical cornerstone of the DFT and FFT.
  * **Future Lectures (Digital Filter Design):** The design of FIR and IIR filters directly utilizes the LTI system classification concepts established today (Linearity, Time-Invariance, Causality, and BIBO Stability).

---
## 10. EXAMINATION QUESTIONS

### 10.1 Short Answer (5 questions)
**Q1.** Provide the formal mathematical definition of a linear system in DSP.
*Model Answer:* A system is linear if and only if it satisfies the principle of superposition (both additivity and homogeneity). Mathematically, the system operator $T\{\cdot\}$ must satisfy $T\{ax_1[n] + bx_2[n]\} = aT\{x_1[n]\} + bT\{x_2[n]\}$ for any arbitrary input sequences and complex constants.

**Q2.** State the necessary and sufficient condition for a Linear Time-Invariant (LTI) system to be BIBO stable.
*Model Answer:* The impulse response sequence $h[n]$ must be absolutely summable. Mathematically: $\sum_{n=-\infty}^{\infty} |h[n]| < \infty$.

**Q3.** Clearly differentiate between an energy signal and a power signal.
*Model Answer:* An energy signal has finite, non-zero total energy ($0 < E < \infty$) and consequently zero average power. A power signal has finite, non-zero average power ($0 < P < \infty$) and consequently infinite total energy. A signal cannot be both simultaneously.

**Q4.** Explain mathematically why the sequence $x[n] = \cos(\pi n / 3)$ is periodic, whereas $x[n] = \cos(3n)$ is aperiodic.
*Model Answer:* For a DT sinusoid to be periodic, its normalized frequency $f_0 = \omega_0/(2\pi)$ must be rational. For $\cos(\pi n / 3)$, $f_0 = (\pi/3)/(2\pi) = 1/6$, which is a rational fraction, thus it is periodic. For $\cos(3n)$, $f_0 = 3/(2\pi)$, which is an irrational number because $\pi$ is irrational, thus it is aperiodic.

**Q5.** Express the unit step sequence $u[n]$ mathematically in terms of the fundamental unit impulse sequence $\delta[n]$.
*Model Answer:* The unit step is the running infinite sum (discrete integral) of the impulse sequence: $u[n] = \sum_{k=-\infty}^{n} \delta[k]$, which can also be written as $u[n] = \sum_{k=0}^{\infty} \delta[n-k]$.

### 10.2 Long Answer / Numerical Problems (4 problems)
**Problem 1.** Analyze the system defined by the input-output relationship $y[n] = n \cdot x[n]$. Conduct formal tests to determine if the system is (a) Linear, and (b) Time-Invariant.
*Full Solution:*
(a) Linearity Test:
Define a composite input: $x_3[n] = a x_1[n] + b x_2[n]$.
Apply to system: $y_3[n] = n \cdot x_3[n] = n(a x_1[n] + b x_2[n]) = a(n x_1[n]) + b(n x_2[n])$.
Since $y_1[n] = n x_1[n]$ and $y_2[n] = n x_2[n]$, we have $y_3[n] = a y_1[n] + b y_2[n]$.
Superposition holds. The system is strictly **Linear**.
(b) Time-Invariance Test:
Step 1 - Shift input: Let $x_1[n] = x[n-k]$. Apply to system: $y_1[n] = n \cdot x_1[n] = n \cdot x[n-k]$.
Step 2 - Shift output: Take $y[n] = n \cdot x[n]$ and replace $n$ with $n-k$. This yields $y[n-k] = (n-k) x[n-k]$.
Step 3 - Compare: $y_1[n] \neq y[n-k]$ because $n \cdot x[n-k]$ is not equal to $(n-k) x[n-k]$.
The system is **Time-Varying**.

**Problem 2.** Calculate the total energy in Joules of the sequence $x[n] = \left(\frac{1}{3}\right)^n u[n]$.
*Full Solution:*
Total energy formula: $E = \sum_{n=-\infty}^{\infty} |x[n]|^2$.
Because of the unit step $u[n]$, the sequence is strictly zero for $n < 0$. We adjust the lower summation bound to zero.
$E = \sum_{n=0}^{\infty} \left| \left(\frac{1}{3}\right)^n \right|^2$
Apply exponent rules: $(x^a)^b = x^{ab} = (x^b)^a$.
$E = \sum_{n=0}^{\infty} \left( \left(\frac{1}{3}\right)^2 \right)^n = \sum_{n=0}^{\infty} \left(\frac{1}{9}\right)^n$
This is a standard infinite geometric series $\sum_{n=0}^{\infty} a^n = \frac{1}{1-a}$, where $a = 1/9$. Since $|1/9| < 1$, the sum converges.
$E = \frac{1}{1 - 1/9} = \frac{1}{8/9} = \frac{9}{8} = 1.125 \text{ Joules}.$

**Problem 3.** Find the explicit even and odd symmetric components of the finite sequence $x[n] = \{1, 2, \underline{3}, 4\}$, where the underline indicates the origin $n=0$.
*Full Solution:*
Define the original sequence indices:
$x[-2]=1, \quad x[-1]=2, \quad x[0]=3, \quad x[1]=4$.
Construct the time-reversed sequence $x[-n]$:
$x[-n]$ maps the value at $n=1$ to $n=-1$, $n=-1$ to $n=1$, etc.
$x[-n] = \{4, \underline{3}, 2, 1\}$ defined from $n=-1$ to $n=2$.
To add/subtract, we must align them over the common valid range $n \in [-2, 2]$, padding with zeros where undefined:
$x[n] = \{1, 2, \underline{3}, 4, 0\}$
$x[-n] = \{0, 4, \underline{3}, 2, 1\}$
Calculate Even part $x_e[n] = \frac{1}{2}(x[n] + x[-n])$:
$x_e[-2] = (1+0)/2 = 0.5$
$x_e[-1] = (2+4)/2 = 3.0$
$x_e[0] = (3+3)/2 = 3.0$
$x_e[1] = (4+2)/2 = 3.0$
$x_e[2] = (0+1)/2 = 0.5$
Result: $x_e[n] = \{0.5, 3, \underline{3}, 3, 0.5\}$
Calculate Odd part $x_o[n] = \frac{1}{2}(x[n] - x[-n])$:
$x_o[-2] = (1-0)/2 = 0.5$
$x_o[-1] = (2-4)/2 = -1.0$
$x_o[0] = (3-3)/2 = 0.0$
$x_o[1] = (4-2)/2 = 1.0$
$x_o[2] = (0-1)/2 = -0.5$
Result: $x_o[n] = \{0.5, -1, \underline{0}, 1, -0.5\}$

**Problem 4.** An LTI system is characterized by the impulse response $h[n] = \alpha^n u[n]$. Using rigorous mathematics, derive the exact range of values for $\alpha$ (which may be complex) for which the system is BIBO stable.
*Full Solution:*
According to the BIBO stability theorem, the impulse response must be absolutely summable.
We require: $\sum_{n=-\infty}^{\infty} |h[n]| < \infty$
Substitute the given impulse response:
$\sum_{n=-\infty}^{\infty} |\alpha^n u[n]| < \infty$
The unit step restricts the summation to non-negative indices:
$\sum_{n=0}^{\infty} |\alpha|^n < \infty$
This is an infinite geometric series. The mathematical rule for the convergence of an infinite geometric series $\sum x^n$ is that it evaluates to a finite value $\frac{1}{1 - x}$ strictly if and only if the magnitude of the base is strictly less than 1 ($|x| < 1$). If $|x| \ge 1$, the series diverges to infinity.
Therefore, the summation converges to a finite value if and only if:
$|\alpha| < 1$.
The system is BIBO stable exclusively for all real or complex values of $\alpha$ whose magnitude is strictly less than 1 (i.e., inside the unit circle on the complex plane).

### 10.3 True/False with Justification (6 items)
1. **T/F:** The addition of two discrete-time periodic signals guarantees that the resulting composite signal will also be periodic.
   * *True.* Since both are DT periodic signals, their individual fundamental periods $N_1$ and $N_2$ must inherently be integers. Therefore, the ratio $N_1/N_2$ is fundamentally a ratio of two integers, which is the definition of a rational number. Because the ratio is always rational, a Least Common Multiple (LCM) always exists, ensuring the sum is periodic.
2. **T/F:** A discrete-time system governed by the equation $y[n] = x[n+1]$ is a causal system.
   * *False.* Causality requires that the output depends only on present or past inputs. To calculate $y[n]$ at time $n$, the system requires the input value at $x[n+1]$, which lies one step in the future. The system is non-causal (specifically, anti-causal).
3. **T/F:** Quantization noise can theoretically be completely eliminated in digital processing systems if the sampling rate is high enough.
   * *False.* Sampling rate (time domain) has absolutely nothing to do with quantization noise (amplitude domain). Quantization is a permanent, lossy many-to-one mapping. Noise is structurally inherent unless the bit-depth of the ADC is literally infinite, which is physically impossible.
4. **T/F:** A discrete-time exponential sequence $a^n$ is bounded and stable only if the base $a$ is a purely real number.
   * *False.* The stability and boundedness depend entirely on the geometric magnitude $|a|$, not the phase. It is stable if the magnitude $|a| < 1$. If $a$ is complex (e.g., $a = 0.5j$), its magnitude is $0.5 < 1$, and it will decay stably.
5. **T/F:** The standard unit impulse sequence $\delta[n]$ is formally classified as an energy signal.
   * *True.* By definition, its total energy is $E = \sum_{n=-\infty}^{\infty} |\delta[n]|^2$. Since $\delta[n]$ is 1 only at $n=0$ and 0 everywhere else, the sum evaluates to exactly $1^2 = 1$ Joule. This is a finite, non-zero energy, satisfying the condition for an energy signal.
6. **T/F:** Applying a time-reversal operation to an energy signal fundamentally alters its total accumulated energy.
   * *False.* Energy is calculated via absolute magnitude squared, summed globally over all time from $n = -\infty$ to $\infty$. Reversing the signal simply changes the order of summation, which does not affect the final scalar sum. $E_x = \sum |x[n]|^2 = \sum |x[-n]|^2 = E_{reversed}$.

---
## 11. KEY FORMULAS REFERENCE

This comprehensive table summarizes the critical mathematical relationships required for the first module.

| DSP Concept / Metric | Formal Mathematical Definition |
| :--- | :--- |
| **Total Signal Energy** | $E = \sum_{n=-\infty}^{\infty} \|x[n]\|^2$ |
| **Average Signal Power** | $P = \lim_{N \to \infty} \frac{1}{2N+1} \sum_{n=-N}^{N} \|x[n]\|^2$ |
| **Periodic Frequency Condition**| $\frac{\omega_0}{2\pi} = \frac{m}{N}$ (where both $m$ and $N$ are integers) |
| **Symmetric (Even) Component** | $x_e[n] = \frac{x[n] + x[-n]}{2}$ |
| **Anti-Symmetric (Odd) Component**| $x_o[n] = \frac{x[n] - x[-n]}{2}$ |
| **Impulse Sifting Property** | $x[n] = \sum_{k=-\infty}^{\infty} x[k] \delta[n-k]$ |
| **LTI BIBO Stability Condition**| $\sum_{k=-\infty}^{\infty} \|h[k]\| < \infty$ (Absolute summability) |
| **Finite Geometric Series Sum** | $\sum_{n=0}^{N-1} a^n = \frac{1 - a^N}{1 - a}$ (Valid for $a \neq 1$) |
| **Infinite Geometric Series Sum**| $\sum_{n=0}^{\infty} a^n = \frac{1}{1 - a}$ (Strictly valid for $\|a\| < 1$) |

---
## 12. FURTHER READING AND REFERENCES

For deeper exploration of these foundational topics, faculty and advanced students should consult the following definitive texts:

* **Proakis, J. G., & Manolakis, D. G. (2006).** *Digital Signal Processing: Principles, Algorithms, and Applications (4th ed.).* Pearson.
  * *Focus:* Chapter 1 (Introduction) and Chapter 2 (Discrete-Time Signals and Systems). This is the primary referenced textbook for signal classification rules and rigorous energy/power worked examples.
* **Oppenheim, A. V., & Schafer, R. W. (2010).** *Discrete-Time Signal Processing (3rd ed.).* Pearson.
  * *Focus:* Chapter 2. This text is highly recommended for its extremely rigorous mathematical treatment of LTI system properties, convolutions, and formal stability proofs.
* **Haykin, S., & Van Veen, B. (2002).** *Signals and Systems (2nd ed.).* Wiley.
  * *Focus:* Chapter 1. Excellent pedagogical resource for bridging the gap and brushing up on Continuous-Time to Discrete-Time transitions, sampling foundations, and basic signal transformation operations.
</Faculty Notes — Lecture 1: Discrete-Time Signals & Systems>
