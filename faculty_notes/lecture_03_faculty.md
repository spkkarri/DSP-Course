<Faculty Notes — Lecture 3: Discrete-Time Fourier Transform (DTFT)>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY
The Discrete-Time Fourier Transform (DTFT) represents discrete sequences in the continuous frequency domain $\omega \in [-\pi, \pi]$. It provides the frequency analysis tool for aperiodic discrete-time signals and forms the theoretical bridge to filter frequency response and the DFT.

**Pedagogical Strategy:**
1. Derive the DTFT from continuous-time Fourier analysis of sampled impulse trains.
2. Emphasize the inherent $2\pi$-periodicity of the DTFT: $X(e^{j(\omega + 2\pi)}) = X(e^{j\omega})$.
3. Rigorously define existence/convergence: The DTFT converges uniformly if $x[n]$ is absolutely summable ($\sum |x[n]| < \infty$).
4. Systematically derive the fundamental theorems: Linearity, Time-Shifting, Frequency-Shifting (Modulation), Differentiation in Frequency, Time Convolution, and Parseval's Energy Theorem.
5. Highlight Hermitian symmetry for real sequences: Magnitude is an even function ($|X(e^{-j\omega})| = |X(e^{j\omega})|$), phase is an odd function ($\angle X(e^{-j\omega}) = -\angle X(e^{j\omega})$).

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Compute** the forward DTFT $X(e^{j\omega})$ and Inverse DTFT (IDTFT) $x[n]$ for standard and composite signals.
2. **Apply** DTFT transform properties to evaluate complex frequency responses without direct integration.
3. **Analyze** symmetry properties of $X(e^{j\omega})$ for real, imaginary, even, and odd sequences.
4. **Use** Parseval's Theorem to compute total energy in both time and frequency domains.
5. **Differentiate** between the DTFT (continuous frequency) and the DFT (sampled discrete frequency).

---
## 2. MATHEMATICAL FOUNDATIONS

### 2.1 The DTFT Analysis and Synthesis Equations
* **Forward DTFT (Analysis Equation):**
  $$ X(e^{j\omega}) = \mathcal{F}\{x[n]\} = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n} $$
* **Inverse DTFT (Synthesis Equation):**
  $$ x[n] = \mathcal{F}^{-1}\{X(e^{j\omega})\} = \frac{1}{2\pi} \int_{-\pi}^{\pi} X(e^{j\omega}) e^{j\omega n} d\omega = \frac{1}{2\pi} \int_{2\pi} X(e^{j\omega}) e^{j\omega n} d\omega $$

### 2.2 Convergence Condition
The infinite series converges uniformly to a continuous function of $\omega$ if $x[n]$ is absolutely summable (sufficient condition):
$$ \sum_{n=-\infty}^{\infty} |x[n]| < \infty $$
If $x[n]$ is square-summable ($\sum |x[n]|^2 < \infty$), the DTFT converges in the mean-square sense.

### 2.3 Comprehensive Table of DTFT Properties
Let $x[n] \leftrightarrow X(e^{j\omega})$ and $y[n] \leftrightarrow Y(e^{j\omega})$:

| Property | Time Domain | Frequency Domain |
| :--- | :--- | :--- |
| **Periodicity** | $x[n]$ | $X(e^{j(\omega + 2\pi)}) = X(e^{j\omega})$ |
| **Linearity** | $a x[n] + b y[n]$ | $a X(e^{j\omega}) + b Y(e^{j\omega})$ |
| **Time Shifting** | $x[n - n_0]$ | $e^{-j\omega n_0} X(e^{j\omega})$ |
| **Frequency Shifting** | $e^{j\omega_0 n} x[n]$ | $X(e^{j(\omega - \omega_0)})$ |
| **Time Reversal** | $x[-n]$ | $X(e^{-j\omega})$ |
| **Differentiation in Freq** | $n x[n]$ | $j \frac{d X(e^{j\omega})}{d\omega}$ |
| **Convolution in Time** | $x[n] * y[n]$ | $X(e^{j\omega}) Y(e^{j\omega})$ |
| **Multiplication in Time** | $x[n] \cdot y[n]$ | $\frac{1}{2\pi} \int_{-\pi}^\pi X(e^{j\theta}) Y(e^{j(\omega - \theta)}) d\theta$ |
| **Parseval's Relation** | $\sum_{n=-\infty}^\infty |x[n]|^2$ | $\frac{1}{2\pi} \int_{-\pi}^\pi |X(e^{j\omega})|^2 d\omega$ |

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 3.1: DTFT of Exponential Decaying Sequence
**Problem:** Find the DTFT of $x[n] = a^n u[n]$ where $|a| < 1$. Find magnitude and phase.

**Solution:**
$$ X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} a^n u[n] e^{-j\omega n} = \sum_{n=0}^{\infty} (a e^{-j\omega})^n $$
Since $|a e^{-j\omega}| = |a| < 1$, using geometric series $\sum_{n=0}^\infty r^n = \frac{1}{1-r}$:
$$ X(e^{j\omega}) = \frac{1}{1 - a e^{-j\omega}} = \frac{1}{1 - a\cos\omega + j a\sin\omega} $$
* **Magnitude Response:**
  $$ |X(e^{j\omega})| = \frac{1}{\sqrt{(1 - a\cos\omega)^2 + (a\sin\omega)^2}} = \frac{1}{\sqrt{1 - 2a\cos\omega + a^2}} $$
* **Phase Response:**
  $$ \angle X(e^{j\omega}) = -\arctan\left( \frac{a\sin\omega}{1 - a\cos\omega} \right) $$

---
### Example 3.2: Inverse DTFT of an Ideal Lowpass Filter
**Problem:** Find the impulse response $h_d[n]$ of an ideal Lowpass filter with cutoff $\omega_c$:
$$ H_d(e^{j\omega}) = \begin{cases} 1, & |\omega| \le \omega_c \\ 0, & \omega_c < |\omega| \le \pi \end{cases} $$

**Solution:**
Using the IDTFT synthesis integral:
$$ h_d[n] = \frac{1}{2\pi} \int_{-\omega_c}^{\omega_c} 1 \cdot e^{j\omega n} d\omega = \left. \frac{1}{2\pi j n} e^{j\omega n} \right|_{-\omega_c}^{\omega_c} = \frac{e^{j\omega_c n} - e^{-j\omega_c n}}{2\pi j n} = \frac{\sin(\omega_c n)}{\pi n} $$
For $n = 0$, applying L'Hôpital's rule: $h_d[0] = \frac{\omega_c}{\pi}$.
Thus:
$$ h_d[n] = \frac{\sin(\omega_c n)}{\pi n} = \frac{\omega_c}{\pi} \text{sinc}\left( \frac{\omega_c n}{\pi} \right) $$
*Note:* $h_d[n]$ is infinite in duration and non-causal (since $h_d[n] \ne 0$ for $n < 0$), making ideal brick-wall filters physically unrealizable.

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
**(a)** State and prove the Time-Shifting and Convolution properties of the DTFT. *(6 Marks)*
**(b)** Using DTFT properties, find the frequency response $X(e^{j\omega})$ of $x[n] = (n+1) a^n u[n]$ for $|a| < 1$. *(5 Marks)*
**(c)** Evaluate the total energy $E$ of the sequence $x[n] = \frac{\sin(\pi n / 3)}{\pi n}$ using Parseval's Theorem. *(4 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Part (a):**
  * Time Shift proof: $\mathcal{F}\{x[n-n_0]\} = \sum x[n-n_0] e^{-j\omega n}$. Let $m = n-n_0 \implies e^{-j\omega(m+n_0)} = e^{-j\omega n_0} X(e^{j\omega})$ *(3 Marks)*
  * Convolution proof: $\mathcal{F}\{x*y\} = \sum_n [\sum_k x[k] y[n-k]] e^{-j\omega n} = \sum_k x[k] e^{-j\omega k} \sum_m y[m] e^{-j\omega m} = X(e^{j\omega}) Y(e^{j\omega})$ *(3 Marks)*
* **Part (b):**
  * Let $v[n] = a^n u[n] \leftrightarrow V(e^{j\omega}) = \frac{1}{1 - a e^{-j\omega}}$.
  * $x[n] = n v[n] + v[n]$.
  * Applying differentiation in frequency: $\mathcal{F}\{n v[n]\} = j \frac{d}{d\omega} \left( \frac{1}{1 - a e^{-j\omega}} \right) = j \frac{-(-j a e^{-j\omega})}{(1 - a e^{-j\omega})^2} = \frac{a e^{-j\omega}}{(1 - a e^{-j\omega})^2}$.
  * $X(e^{j\omega}) = \frac{a e^{-j\omega}}{(1 - a e^{-j\omega})^2} + \frac{1}{1 - a e^{-j\omega}} = \frac{1}{(1 - a e^{-j\omega})^2}$ *(5 Marks)*
* **Part (c):**
  * By Parseval's theorem: $E = \sum |x[n]|^2 = \frac{1}{2\pi} \int_{-\pi}^\pi |X(e^{j\omega})|^2 d\omega$.
  * Here $X(e^{j\omega})$ is an ideal pulse of height $1$ over $[-\pi/3, \pi/3]$.
  * $E = \frac{1}{2\pi} \int_{-\pi/3}^{\pi/3} 1^2 d\omega = \frac{1}{2\pi} \left( \frac{2\pi}{3} \right) = \frac{1}{3} \text{ Joules}$. *(4 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import numpy as np

# Energy verification via Parseval's
n = np.arange(-1000, 1001)
# Handle n=0 limit
x = np.zeros_like(n, dtype=float)
x[n != 0] = np.sin(np.pi * n[n != 0] / 3) / (np.pi * n[n != 0])
x[n == 0] = 1.0 / 3.0

E_time = np.sum(x**2)
E_freq = 1.0 / 3.0
print(f"Time-domain Energy = {E_time:.6f}, Theoretical = {E_freq:.6f}")
```
