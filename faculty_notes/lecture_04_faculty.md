<Faculty Notes — Lecture 4: Frequency Response & Group Delay>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY
This lecture establishes how discrete LTI systems modify the magnitude and phase of input signals. A major conceptual pillar in DSP is the **Eigenfunction Property**: When a complex exponential $e^{j\omega n}$ passes through an LTI system, the output is the same complex exponential scaled by the complex frequency response $H(e^{j\omega})$.

**Pedagogical Strategy:**
1. Derive the eigenfunction property: $\mathcal{T}\{e^{j\omega n}\} = H(e^{j\omega}) e^{j\omega n}$.
2. Decompose $H(e^{j\omega}) = |H(e^{j\omega})| e^{j\angle H(e^{j\omega})}$.
3. Differentiate between **Phase Delay** $\tau_p(\omega) = -\frac{\angle H(e^{j\omega})}{\omega}$ and **Group Delay** $\tau_g(\omega) = -\frac{d}{d\omega} \angle H(e^{j\omega})$.
4. Explain the physical consequence of non-constant group delay: **Dispersion (phase distortion)**, which spreads wave packets in time.
5. Define the condition for strictly linear phase: $\angle H(e^{j\omega}) = -\alpha \omega \implies \tau_g(\omega) = \alpha = \text{constant}$.

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Derive** the steady-state response of an LTI system to sinusoidal and multi-tone inputs.
2. **Calculate** the magnitude response $|H(e^{j\omega})|$, phase response $\theta(\omega)$, phase delay $\tau_p(\omega)$, and group delay $\tau_g(\omega)$.
3. **Analyze** the distortion introduced by non-linear phase filters on broadband and modulated communication signals.
4. **Determine** the conditions under which a digital filter provides generalized linear phase.

---
## 2. MATHEMATICAL FOUNDATIONS

### 2.1 The Eigenfunction Property
Let input $x[n] = e^{j\omega n}$ for all $-\infty < n < \infty$. The system output is:
$$ y[n] = \sum_{k=-\infty}^{\infty} h[k] x[n-k] = \sum_{k=-\infty}^{\infty} h[k] e^{j\omega(n-k)} = \left( \sum_{k=-\infty}^{\infty} h[k] e^{-j\omega k} \right) e^{j\omega n} = H(e^{j\omega}) e^{j\omega n} $$
Where $H(e^{j\omega}) = \mathcal{F}\{h[n]\}$ is the **Frequency Response** of the system.

For a real sinusoidal input $x[n] = A \cos(\omega_0 n + \phi)$:
$$ y[n] = A |H(e^{j\omega_0})| \cos(\omega_0 n + \phi + \angle H(e^{j\omega_0})) $$

### 2.2 Phase Delay vs. Group Delay
* **Phase Delay $\tau_p(\omega)$:** The time delay experienced by individual sinusoidal carrier frequencies:
  $$ \tau_p(\omega) = -\frac{\angle H(e^{j\omega})}{\omega} = -\frac{\theta(\omega)}{\omega} $$
* **Group Delay $\tau_g(\omega)$:** The time delay experienced by the envelope/information of a narrowband wave packet (derivative of phase):
  $$ \tau_g(\omega) = -\frac{d \theta(\omega)}{d\omega} = -\frac{d}{d\omega} \left[ \angle H(e^{j\omega}) \right] $$

### 2.3 Condition for Distortionless Transmission
For a system to transmit a signal without wave shape distortion:
$$ y[n] = A x[n - n_d] $$
In the frequency domain:
$$ Y(e^{j\omega}) = A e^{-j\omega n_d} X(e^{j\omega}) \implies H(e^{j\omega}) = A e^{-j\omega n_d} $$
1. **Magnitude Response:** $|H(e^{j\omega})| = A = \text{constant}$ (No amplitude distortion).
2. **Phase Response:** $\theta(\omega) = -\omega n_d$ (Strictly linear phase).
3. **Group Delay:** $\tau_g(\omega) = n_d = \text{constant}$ (All frequencies delayed equally).

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 4.1: Frequency Response & Delay of a Moving-Average Filter
**Problem:** A 3-point moving average filter has impulse response $h[n] = \frac{1}{3} \{ \underset{\uparrow}{1}, 1, 1 \}$.
(a) Find $H(e^{j\omega})$.
(b) Determine the magnitude response $|H(e^{j\omega})|$ and phase response $\theta(\omega)$.
(c) Compute the phase delay $\tau_p(\omega)$ and group delay $\tau_g(\omega)$.

**Solution:**
**(a)**
$$ H(e^{j\omega}) = \frac{1}{3} \left( 1 + e^{-j\omega} + e^{-j 2\omega} \right) = \frac{1}{3} e^{-j\omega} \left( e^{j\omega} + 1 + e^{-j\omega} \right) = \frac{1}{3} e^{-j\omega} (1 + 2\cos\omega) $$

**(b)**
* Amplitude function: $A(\omega) = \frac{1 + 2\cos\omega}{3}$.
* Magnitude: $|H(e^{j\omega})| = \frac{|1 + 2\cos\omega|}{3}$.
* Phase: $\theta(\omega) = -\omega$ (for $1 + 2\cos\omega > 0$).

**(c)**
* Phase Delay: $\tau_p(\omega) = -\frac{\theta(\omega)}{\omega} = -\frac{-\omega}{\omega} = 1 \text{ sample}$.
* Group Delay: $\tau_g(\omega) = -\frac{d\theta(\omega)}{d\omega} = -\frac{d(-\omega)}{d\omega} = 1 \text{ sample}$.
Since $\tau_g(\omega) = 1$ is constant for all frequencies where $A(\omega) > 0$, the filter has **strictly linear phase**.

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
**(a)** Define Phase Delay and Group Delay. Explain why constant group delay is critical in digital communications and biomedical instrumentation. *(6 Marks)*
**(b)** An LTI system has frequency response:
$$ H(e^{j\omega}) = \frac{1 - 0.5 e^{-j\omega}}{1 - 0.8 e^{-j\omega}} $$
1. Find the steady-state output $y[n]$ for $x[n] = 2 + 4\cos\left( \frac{\pi}{2} n + \frac{\pi}{6} \right)$. *(6 Marks)*
2. Find the group delay $\tau_g(\omega)$ at $\omega = 0$ and $\omega = \pi$. *(3 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Part (a):**
  * Mathematical definitions of $\tau_p$ and $\tau_g$ *(2 Marks)*
  * Explanation: Variable group delay causes dispersion/pulse broadening leading to Intersymbol Interference (ISI) in comms, and waveform distortion in ECG/EEG *(4 Marks)*
* **Part (b.1):**
  * At DC ($\omega = 0$): $H(e^{j0}) = \frac{1 - 0.5}{1 - 0.8} = \frac{0.5}{0.2} = 2.5$.
    DC output: $y_{DC}[n] = 2 \times 2.5 = 5$. *(2 Marks)*
  * At $\omega = \pi/2$: $e^{-j\pi/2} = -j$.
    $$ H(e^{j\pi/2}) = \frac{1 + 0.5j}{1 + 0.8j} = \frac{\sqrt{1 + 0.25} e^{j\arctan(0.5)}}{\sqrt{1 + 0.64} e^{j\arctan(0.8)}} = \frac{1.1180 e^{j 0.4636}}{1.2806 e^{j 0.6747}} = 0.8730 e^{-j 0.2111} \text{ rad} $$ *(2 Marks)*
  * Total output:
    $$ y[n] = 5 + 4(0.8730) \cos\left( \frac{\pi}{2} n + \frac{\pi}{6} - 0.2111 \right) = 5 + 3.492 \cos\left( \frac{\pi}{2} n + 0.3125 \right) $$ *(2 Marks)*
* **Part (b.2):**
  * Group delay formula for single-pole single-zero sections:
    $\tau_g(\omega) = \frac{0.8(0.8 - \cos\omega)}{1 - 1.6\cos\omega + 0.64} - \frac{0.5(0.5 - \cos\omega)}{1 - \cos\omega + 0.25}$
    * At $\omega = 0$: $\tau_g(0) = \frac{0.8(-0.2)}{0.04} - \frac{0.5(-0.5)}{0.25} = -4.0 - (-1.0) = -3.0 \to \text{delay } +3.0$. *(1.5 Marks)*
    * At $\omega = \pi$: $\tau_g(\pi) = \frac{0.8(1.8)}{3.24} - \frac{0.5(1.5)}{2.25} = 0.444 - 0.333 = 0.111 \text{ samples}$. *(1.5 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import numpy as np

# Verify frequency response at w = pi/2
w = np.pi / 2
H = (1 - 0.5 * np.exp(-1j * w)) / (1 - 0.8 * np.exp(-1j * w))
print(f"|H(e^j(pi/2))| = {np.abs(H):.4f}, Angle = {np.angle(H):.4f} rad")
```
