<Faculty Notes — Lecture 7: Discrete Fourier Transform (DFT) & Matrix Formulation>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY
The Discrete Fourier Transform (DFT) is the cornerstone of practical digital signal processing. Unlike the DTFT (which produces a continuous spectrum) or the Z-Transform, the DFT operates on a finite sequence of $N$ numbers and yields $N$ discrete frequency coefficients, making it directly implementable in digital hardware and computers.

**Pedagogical Strategy:**
1. Derive the DFT by uniformly sampling the continuous DTFT spectrum $X(e^{j\omega})$ at $N$ points $\omega_k = \frac{2\pi k}{N}$.
2. Introduce the twiddle factor notation $W_N = e^{-j 2\pi / N}$ and prove its periodicity, symmetry, and orthogonality properties.
3. Formulate the DFT as a linear matrix transformation $\mathbf{X} = \mathbf{W}_N \mathbf{x}$.
4. Demonstrate the unitary matrix properties $\mathbf{W}_N^{-1} = \frac{1}{N} \mathbf{W}_N^*$.
5. Connect time-domain discrete resolution ($\Delta t = T_s$) to frequency-domain bin resolution ($\Delta f = F_s / N$).

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Derive** the forward $N$-point DFT and Inverse DFT (IDFT) analysis/synthesis equations.
2. **Construct** the $N \times N$ DFT twiddle factor matrix $\mathbf{W}_N$ for $N = 4$ and $N = 8$.
3. **Compute** the DFT of basic sequences analytically and via matrix-vector multiplication.
4. **Determine** frequency resolution $\Delta f$ and bin frequencies $f_k = k \frac{F_s}{N}$.
5. **Relate** the DFT to the continuous DTFT and Discrete Fourier Series (DFS).

---
## 2. MATHEMATICAL FOUNDATIONS

### 2.1 The DFT Definition
For a finite-duration sequence $x[n]$ of length $N$ ($0 \le n \le N-1$):
* **Forward $N$-point DFT:**
  $$ X[k] = \sum_{n=0}^{N-1} x[n] W_N^{nk}, \quad k = 0, 1, \dots, N-1 $$
* **Inverse $N$-point IDFT:**
  $$ x[n] = \frac{1}{N} \sum_{k=0}^{N-1} X[k] W_N^{-nk}, \quad n = 0, 1, \dots, N-1 $$
Where the **Twiddle Factor** is defined as:
$$ W_N = e^{-j \frac{2\pi}{N}} = \cos\left( \frac{2\pi}{N} \right) - j \sin\left( \frac{2\pi}{N} \right) $$

### 2.2 Fundamental Properties of the Twiddle Factor $W_N$
1. **Periodicity in $n$ and $k$:**
   $$ W_N^{k + N} = W_N^k, \quad W_N^{nk + N} = W_N^{nk} $$
2. **Symmetry Property (Half-Period Inversion):**
   $$ W_N^{k + N/2} = -W_N^k \quad (\text{for even } N) $$
3. **Phase Reduction:**
   $$ W_N^{nk} = W_N^{(nk) \bmod N} $$
4. **Orthogonality of Basis Functions:**
   $$ \sum_{n=0}^{N-1} W_N^{n(k - m)} = \begin{cases} N, & k = m \pmod N \\ 0, & k \ne m \pmod N \end{cases} $$

### 2.3 Matrix Formulation of the DFT
In vector-matrix form:
$$ \mathbf{X} = \mathbf{W}_N \mathbf{x} $$
$$ \begin{bmatrix} X[0] \\ X[1] \\ X[2] \\ \vdots \\ X[N-1] \end{bmatrix} = \begin{bmatrix} W_N^0 & W_N^0 & W_N^0 & \dots & W_N^0 \\ W_N^0 & W_N^1 & W_N^2 & \dots & W_N^{N-1} \\ W_N^0 & W_N^2 & W_N^4 & \dots & W_N^{2(N-1)} \\ \vdots & \vdots & \vdots & \ddots & \vdots \\ W_N^0 & W_N^{N-1} & W_N^{2(N-1)} & \dots & W_N^{(N-1)(N-1)} \end{bmatrix} \begin{bmatrix} x[0] \\ x[1] \\ x[2] \\ \vdots \\ x[N-1] \end{bmatrix} $$
The Inverse DFT is:
$$ \mathbf{x} = \mathbf{W}_N^{-1} \mathbf{X} = \frac{1}{N} \mathbf{W}_N^* \mathbf{X} $$
Where $\mathbf{W}_N^*$ is the complex conjugate of the twiddle matrix.

For $N=4$ ($W_4 = e^{-j 2\pi/4} = e^{-j\pi/2} = -j$):
$$ \mathbf{W}_4 = \begin{bmatrix} 1 & 1 & 1 & 1 \\ 1 & -j & -1 & j \\ 1 & -1 & 1 & -1 \\ 1 & j & -1 & -j \end{bmatrix} $$

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 7.1: 4-Point DFT Matrix Computation
**Problem:** Compute the 4-point DFT of $x[n] = \{ \underset{\uparrow}{1}, 2, 0, 1 \}$.

**Solution:**
Using $\mathbf{X} = \mathbf{W}_4 \mathbf{x}$:
$$ \begin{bmatrix} X[0] \\ X[1] \\ X[2] \\ X[3] \end{bmatrix} = \begin{bmatrix} 1 & 1 & 1 & 1 \\ 1 & -j & -1 & j \\ 1 & -1 & 1 & -1 \\ 1 & j & -1 & -j \end{bmatrix} \begin{bmatrix} 1 \\ 2 \\ 0 \\ 1 \end{bmatrix} $$
* $X[0] = 1(1) + 1(2) + 1(0) + 1(1) = 4$
* $X[1] = 1(1) - j(2) - 1(0) + j(1) = 1 - 2j + j = 1 - j$
* $X[2] = 1(1) - 1(2) + 1(0) - 1(1) = 1 - 2 - 1 = -2$
* $X[3] = 1(1) + j(2) - 1(0) - j(1) = 1 + 2j - j = 1 + j$
Result:
$$ X[k] = \{ 4, \; 1 - j, \; -2, \; 1 + j \} $$
Notice Hermitian symmetry: $X[0] = 4 \in \mathbb{R}$, $X[2] = -2 \in \mathbb{R}$, and $X[3] = X[1]^* = 1 + j$.

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
**(a)** State and prove the twiddle factor properties: Periodicity, Symmetry, and Orthogonality. *(6 Marks)*
**(b)** Given an 8-point sequence $x[n] = \delta[n] + 2\delta[n-2] + \delta[n-4]$.
1. Compute its 8-point DFT $X[k]$ analytically. *(5 Marks)*
2. If sampling rate $F_s = 8000 \text{ Hz}$, find the frequency in $\text{Hz}$ corresponding to bin $k = 3$. *(2 Marks)*
3. Verify Parseval's relation for this sequence. *(2 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Part (a):**
  * Periodicity proof: $W_N^{k+N} = e^{-j \frac{2\pi(k+N)}{N}} = e^{-j\frac{2\pi k}{N}} e^{-j 2\pi} = W_N^k \cdot 1 = W_N^k$ *(2 Marks)*
  * Symmetry proof: $W_N^{k+N/2} = e^{-j\frac{2\pi(k+N/2)}{N}} = W_N^k e^{-j\pi} = -W_N^k$ *(2 Marks)*
  * Orthogonality proof: Geometric series $\sum_{n=0}^{N-1} [W_N^{k-m}]^n = \frac{1 - W_N^{N(k-m)}}{1 - W_N^{k-m}} = \frac{1-1}{1-W_N^{k-m}} = 0$ for $k \ne m$ *(2 Marks)*
* **Part (b.1):**
  * $X[k] = \sum_{n=0}^7 x[n] W_8^{nk} = 1 \cdot W_8^0 + 2 W_8^{2k} + 1 \cdot W_8^{4k}$
  * Since $W_8^2 = W_4 = e^{-j\pi/2} = -j$ and $W_8^4 = W_2 = e^{-j\pi} = -1$:
    $$ X[k] = 1 + 2(-j)^k + (-1)^k $$
    * $X[0] = 1 + 2(1) + 1 = 4$
    * $X[1] = 1 + 2(-j) - 1 = -2j$
    * $X[2] = 1 + 2(-1) + 1 = 0$
    * $X[3] = 1 + 2(j) - 1 = 2j$
    * $X[4] = 1 + 2(1) + 1 = 4$
    * $X[5] = 1 + 2(-j) - 1 = -2j$
    * $X[6] = 1 + 2(-1) + 1 = 0$
    * $X[7] = 1 + 2(j) - 1 = 2j$
    $$ X[k] = \{ 4, -2j, 0, 2j, 4, -2j, 0, 2j \} $$ *(5 Marks)*
* **Part (b.2):**
  * Bin frequency: $f_k = k \frac{F_s}{N} = 3 \times \frac{8000}{8} = 3000 \text{ Hz}$. *(2 Marks)*
* **Part (b.3):**
  * Time energy: $\sum_{n=0}^7 |x[n]|^2 = 1^2 + 2^2 + 1^2 = 1 + 4 + 1 = 6$.
  * Frequency energy: $\frac{1}{8} \sum_{k=0}^7 |X[k]|^2 = \frac{1}{8} [4^2 + 2^2 + 0 + 2^2 + 4^2 + 2^2 + 0 + 2^2] = \frac{1}{8} [16 + 4 + 4 + 16 + 4 + 4] = \frac{48}{8} = 6$.
  * Parseval's holds exactly ($6 = 6$). *(2 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import numpy as np

x = np.array([1, 0, 2, 0, 1, 0, 0, 0])
X = np.fft.fft(x)
print("Computed 8-pt DFT:", np.round(X, 4))
```
