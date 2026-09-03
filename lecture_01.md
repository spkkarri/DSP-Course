# Lecture 1: Course Introduction & Discrete-Time Signals
## EE3621: Digital Signal Processing | III B.Tech EEE

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Differentiate** between continuous-time, discrete-time, and digital signals across time-domain and amplitude-domain representations.
2. **Compute** the fundamental period $N_0$ of discrete-time sinusoids and verify periodicity conditions.
3. **Decompose** an arbitrary discrete-time sequence into its even symmetric $x_e[n]$ and odd symmetric $x_o[n]$ components.
4. **Evaluate** the total signal energy $E$ and average power $P$ of elementary and composite discrete-time sequences.
5. **Formulate** elementary signal operations including time-shifting, time-reversal, amplitude scaling, and downsampling/upsampling.

---
## 2. MATHEMATICAL FOUNDATIONS & DEFINITIONS

### 2.1 Continuous to Discrete Sampling
A discrete-time signal $x[n]$ is obtained by sampling a continuous-time signal $x_a(t)$ at uniform intervals of $T_s$ seconds:
$$ x[n] = x_a(n T_s) = \left. x_a(t) \right|_{t = n T_s}, \quad n \in \mathbb{Z} $$
Where:
* $T_s = 1/F_s$ is the sampling period in seconds.
* $F_s$ is the sampling frequency in Hertz ($\text{Hz}$ or samples/sec).
* $\Omega$ denotes continuous-time angular frequency ($\text{rad/s}$), and $\omega = \Omega T_s = \Omega / F_s$ denotes normalized discrete-time angular frequency ($\text{rad/sample}$).

### 2.2 Elementary Discrete-Time Sequences
1. **Unit Impulse (Kronecker Delta):**
   $$ \delta[n] = \begin{cases} 1, & n = 0 \\ 0, & n \ne 0 \end{cases} $$
   *Sifting Property:* $\sum_{n=-\infty}^{\infty} x[n] \delta[n - n_0] = x[n_0]$.

2. **Unit Step Sequence:**
   $$ u[n] = \begin{cases} 1, & n \ge 0 \\ 0, & n < 0 \end{cases} = \sum_{k=0}^{\infty} \delta[n - k] = \sum_{m=-\infty}^{n} \delta[m] $$
   Relation to impulse: $\delta[n] = u[n] - u[n-1]$.

3. **Unit Ramp Sequence:**
   $$ r[n] = n \cdot u[n] = \begin{cases} n, & n \ge 0 \\ 0, & n < 0 \end{cases} $$

4. **Real Exponential Sequence:**
   $$ x[n] = a^n u[n] = \begin{cases} a^n, & n \ge 0 \\ 0, & n < 0 \end{cases} $$
   * For $0 < a < 1$: decaying monotonic sequence.
   * For $-1 < a < 0$: alternating decaying sequence.
   * For $|a| > 1$: exponentially growing sequence (unstable).

5. **Complex Exponential and Sinusoidal Sequences:**
   $$ x[n] = A e^{j(\omega_0 n + \phi)} = A \cos(\omega_0 n + \phi) + j A \sin(\omega_0 n + \phi) $$

### 2.3 Periodicity Condition in Discrete Time
A discrete-time sequence $x[n]$ is periodic with fundamental period $N \in \mathbb{Z}^+$ if and only if $x[n + N] = x[n]$ for all $n$.
For a sinusoid $x[n] = \cos(\omega_0 n)$:
$$ \cos(\omega_0 (n + N)) = \cos(\omega_0 n + \omega_0 N) = \cos(\omega_0 n) \iff \omega_0 N = 2\pi k, \quad k \in \mathbb{Z}^+ $$
$$ \frac{\omega_0}{2\pi} = \frac{k}{N} \in \mathbb{Q} \quad (\text{Ratio of frequency to } 2\pi \text{ must be a rational number}) $$
The fundamental period is $N_0 = \frac{2\pi k}{\omega_0}$, where $k$ is the smallest positive integer such that $N_0$ is an integer.

### 2.4 Energy and Power Classification
* **Total Signal Energy $E$:**
  $$ E = \sum_{n=-\infty}^{\infty} |x[n]|^2 $$
* **Average Signal Power $P$:**
  $$ P = \lim_{K \to \infty} \frac{1}{2K + 1} \sum_{n=-K}^{K} |x[n]|^2 $$
  For a periodic sequence with fundamental period $N_0$:
  $$ P = \frac{1}{N_0} \sum_{n=0}^{N_0 - 1} |x[n]|^2 $$
* **Classification:**
  1. *Energy Signal:* $0 < E < \infty \implies P = 0$.
  2. *Power Signal:* $0 < P < \infty \implies E = \infty$.
  3. *Neither:* $E = \infty$ and $P = \infty$ or $P = 0$.

### 2.5 Even and Odd Symmetry Decomposition
Any arbitrary sequence $x[n]$ can be uniquely decomposed into even and odd components:
$$ x[n] = x_e[n] + x_o[n] $$
$$ x_e[n] = \frac{1}{2} \left( x[n] + x[-n] \right) \quad (\text{Even Component: } x_e[-n] = x_e[n]) $$
$$ x_o[n] = \frac{1}{2} \left( x[n] - x[-n] \right) \quad (\text{Odd Component: } x_o[-n] = -x_o[n], \; x_o[0] = 0) $$

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 1.1: Periodicity Analysis of Composite Discrete Sinusoids
**Problem:** Determine if the following signals are periodic. If periodic, find the fundamental period $N_0$:
(a) $x_1[n] = \cos\left( \frac{3\pi}{7} n + \frac{\pi}{4} \right)$
(b) $x_2[n] = \cos(0.8 n)$
(c) $x_3[n] = \cos\left( \frac{\pi}{6} n \right) + \sin\left( \frac{\pi}{8} n \right)$

**Solution:**
**(a)** $\omega_1 = \frac{3\pi}{7}$.
$$ \frac{\omega_1}{2\pi} = \frac{3\pi/7}{2\pi} = \frac{3}{14} \in \mathbb{Q} $$
Since the ratio is rational, $x_1[n]$ is periodic.
Fundamental period: $N_1 = \frac{2\pi \cdot k}{\omega_1} = \frac{2\pi \cdot 3}{3\pi/7} = 14$ samples (with $k=3$).

**(b)** $\omega_2 = 0.8 = \frac{4}{5}$.
$$ \frac{\omega_2}{2\pi} = \frac{0.8}{2\pi} = \frac{0.4}{\pi} \notin \mathbb{Q} $$
Because $\pi$ is irrational, $\frac{\omega_2}{2\pi}$ is irrational. Therefore, $x_2[n]$ is **aperiodic (non-periodic)**.

**(c)** For composite signal $x_3[n]$:
* For $\cos\left( \frac{\pi}{6} n \right)$: $\omega_a = \pi/6 \implies \frac{\omega_a}{2\pi} = \frac{1}{12} \implies N_a = 12$.
* For $\sin\left( \frac{\pi}{8} n \right)$: $\omega_b = \pi/8 \implies \frac{\omega_b}{2\pi} = \frac{1}{16} \implies N_b = 16$.
Both terms are periodic. The overall fundamental period is the Least Common Multiple (LCM):
$$ N_0 = \text{LCM}(N_a, N_b) = \text{LCM}(12, 16) = 48 \text{ samples} $$

---
### Example 1.2: Energy and Power Calculation
**Problem:** Classify the following signals as Energy, Power, or Neither, and compute the corresponding $E$ or $P$:
(a) $x[n] = (0.6)^n u[n]$
(b) $x[n] = e^{j(\frac{\pi}{4} n + \frac{\pi}{3})}$

**Solution:**
**(a)** Total Energy:
$$ E = \sum_{n=-\infty}^{\infty} |x[n]|^2 = \sum_{n=0}^{\infty} |(0.6)^n|^2 = \sum_{n=0}^{\infty} (0.36)^n $$
Using the infinite geometric series formula $\sum_{n=0}^{\infty} r^n = \frac{1}{1-r}$ for $|r| < 1$:
$$ E = \frac{1}{1 - 0.36} = \frac{1}{0.64} = \frac{25}{16} = 1.5625 \text{ Joules} $$
Since $0 < E < \infty$, $x[n]$ is an **Energy Signal** with average power $P = 0$.

**(b)** The signal has $|x[n]| = \left| e^{j(\frac{\pi}{4} n + \frac{\pi}{3})} \right| = 1$ for all $n$.
Fundamental period: $\omega_0 = \pi/4 \implies N_0 = \frac{2\pi}{\pi/4} = 8$.
Average Power:
$$ P = \frac{1}{N_0} \sum_{n=0}^{N_0-1} |x[n]|^2 = \frac{1}{8} \sum_{n=0}^{7} 1^2 = \frac{8}{8} = 1 \text{ Watt} $$
Total energy $E = \sum_{n=-\infty}^{\infty} 1 = \infty$.
Therefore, $x[n]$ is a **Power Signal** with $P = 1\text{ W}$ and $E = \infty$.

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
**(a)** Define elementary discrete-time sequences: $\delta[n]$, $u[n]$, and $r[n]$. Express $u[n]$ in terms of $\delta[n]$ and vice-versa. *(5 Marks)*
**(b)** A continuous-time signal $x_a(t) = 3\cos(100\pi t) + 2\sin(250\pi t)$ is sampled at $F_s = 200 \text{ Hz}$.
1. Find the discrete-time sequence $x[n]$. *(3 Marks)*
2. Determine whether $x[n]$ is periodic. If periodic, find the fundamental period $N_0$. *(4 Marks)*
3. Calculate the average power $P$ of $x[n]$. *(3 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Part (a):**
  * Definitions of $\delta[n], u[n], r[n]$ with equations and sketches *(3 Marks)*
  * $u[n] = \sum_{k=-\infty}^n \delta[k] = \sum_{m=0}^\infty \delta[n-m]$ and $\delta[n] = u[n] - u[n-1]$ *(2 Marks)*
* **Part (b.1):**
  * Substitute $t = n/F_s = n/200$:
    $$ x[n] = 3\cos\left( 100\pi \frac{n}{200} \right) + 2\sin\left( 250\pi \frac{n}{200} \right) = 3\cos\left( \frac{\pi}{2} n \right) + 2\sin\left( \frac{5\pi}{4} n \right) $$
    Since $\frac{5\pi}{4} = 2\pi - \frac{3\pi}{4}$, the principal alias is:
    $$ x[n] = 3\cos(0.5\pi n) - 2\sin(0.75\pi n) $$ *(3 Marks)*
* **Part (b.2):**
  * $\omega_1 = 0.5\pi \implies \frac{\omega_1}{2\pi} = \frac{1}{4} \implies N_1 = 4$.
  * $\omega_2 = 0.75\pi \implies \frac{\omega_2}{2\pi} = \frac{3}{8} \implies N_2 = 8$.
  * $N_0 = \text{LCM}(4, 8) = 8$ samples. *(4 Marks)*
* **Part (b.3):**
  * Average power:
    $$ P = \frac{3^2}{2} + \frac{2^2}{2} = 4.5 + 2.0 = 6.5 \text{ Watts} $$ *(3 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import numpy as np

# Sampling verification
Fs = 200
n = np.arange(0, 16)
xn = 3 * np.cos(np.pi / 2 * n) + 2 * np.sin(5 * np.pi / 4 * n)

# Compute fundamental period power
N0 = 8
P = np.mean(xn[:N0]**2)
print(f"Discrete Signal Power P = {P:.4f} W (Theoretical = 6.5 W)")
```
