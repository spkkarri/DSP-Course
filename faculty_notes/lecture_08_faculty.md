<Faculty Notes — Lecture 8: Properties of the DFT & Circular Convolution>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY
Understanding the mathematical properties of the Discrete Fourier Transform (DFT) is essential for spectral analysis, circular filtering, and fast algorithm design. Because the DFT inherently assumes periodic extension of sequences, operations in time correspond to modulo-$N$ circular shifts and circular convolutions.

**Pedagogical Strategy:**
1. Define the circular index notation $((n - m))_N = (n - m) \bmod N$.
2. Prove the Circular Time-Shifting property: $\text{DFT}_N\{x[((n - m))_N]\} = W_N^{km} X[k]$.
3. Rigorously derive the **Circular Convolution Theorem**: Multiplication in the discrete frequency domain corresponds to circular convolution in the time domain: $x_1[n] \circledast_N x_2[n] \leftrightarrow X_1[k] X_2[k]$.
4. Teach the Graphical Concentric Circle method and Matrix Multiplication method for circular convolution.
5. Derive Parseval's energy theorem for the DFT: $\sum_{n=0}^{N-1} |x[n]|^2 = \frac{1}{N} \sum_{k=0}^{N-1} |X[k]|^2$.

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Apply** DFT properties including Circular Shifting, Modulation, and Conjugate Symmetry.
2. **Compute** circular convolution $x_1[n] \circledast_N x_2[n]$ using the formula, tabular/concentric-circle method, and the DFT-IDFT method.
3. **Analyze** the periodic and circular symmetry of real-valued sequences.
4. **Evaluate** signal energy and circular cross-correlation via the DFT.

---
## 2. MATHEMATICAL FOUNDATIONS

### 2.1 Circular Time Shift
A circular shift of a sequence $x[n]$ by $m$ samples is defined on the finite support $0 \le n \le N-1$ as:
$$ x_c[n] = x[((n - m))_N] = x[(n - m) \bmod N] $$
Applying the forward DFT:
$$ X_c[k] = \sum_{n=0}^{N-1} x[((n - m))_N] W_N^{nk} = W_N^{km} X[k] = e^{-j \frac{2\pi km}{N}} X[k] $$

### 2.2 Circular Convolution Theorem
Let $x_1[n]$ and $x_2[n]$ be two $N$-point sequences with DFTs $X_1[k]$ and $X_2[k]$. The circular convolution $y_c[n] = x_1[n] \circledast_N x_2[n]$ is:
$$ y_c[n] = \sum_{m=0}^{N-1} x_1[m] x_2[((n - m))_N], \quad 0 \le n \le N-1 $$
Taking the DFT of $y_c[n]$:
$$ Y_c[k] = \sum_{n=0}^{N-1} \left( \sum_{m=0}^{N-1} x_1[m] x_2[((n - m))_N] \right) W_N^{nk} = \sum_{m=0}^{N-1} x_1[m] \left( \sum_{n=0}^{N-1} x_2[((n - m))_N] W_N^{nk} \right) $$
Using the circular shift property, the inner sum equals $W_N^{mk} X_2[k]$:
$$ Y_c[k] = \sum_{m=0}^{N-1} x_1[m] W_N^{mk} X_2[k] = \left( \sum_{m=0}^{N-1} x_1[m] W_N^{mk} \right) X_2[k] = X_1[k] \cdot X_2[k] $$
$$ \mathbf{x_1[n] \circledast_N x_2[n] \iff X_1[k] \cdot X_2[k]} $$

### 2.3 Matrix Formulation of Circular Convolution
Circular convolution can be written as a matrix-vector product with a **Circulant Matrix**:
$$ \begin{bmatrix} y_c[0] \\ y_c[1] \\ y_c[2] \\ \vdots \\ y_c[N-1] \end{bmatrix} = \begin{bmatrix} x_2[0] & x_2[N-1] & x_2[N-2] & \dots & x_2[1] \\ x_2[1] & x_2[0] & x_2[N-1] & \dots & x_2[2] \\ x_2[2] & x_2[1] & x_2[0] & \dots & x_2[3] \\ \vdots & \vdots & \vdots & \ddots & \vdots \\ x_2[N-1] & x_2[N-2] & x_2[N-3] & \dots & x_2[0] \end{bmatrix} \begin{bmatrix} x_1[0] \\ x_1[1] \\ x_1[2] \\ \vdots \\ x_1[N-1] \end{bmatrix} $$

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 8.1: Circular Convolution via Matrix Method
**Problem:** Compute the 4-point circular convolution $y_c[n] = x_1[n] \circledast_4 x_2[n]$ for:
$$ x_1[n] = \{ \underset{\uparrow}{1}, 2, 3, 1 \}, \quad x_2[n] = \{ \underset{\uparrow}{4}, 3, 2, 1 \} $$

**Solution:**
Construct the circulant matrix for $x_2[n]$:
$$ \begin{bmatrix} y_c[0] \\ y_c[1] \\ y_c[2] \\ y_c[3] \end{bmatrix} = \begin{bmatrix} 4 & 1 & 2 & 3 \\ 3 & 4 & 1 & 2 \\ 2 & 3 & 4 & 1 \\ 1 & 2 & 3 & 4 \end{bmatrix} \begin{bmatrix} 1 \\ 2 \\ 3 \\ 1 \end{bmatrix} $$
* $y_c[0] = 4(1) + 1(2) + 2(3) + 3(1) = 4 + 2 + 6 + 3 = 15$
* $y_c[1] = 3(1) + 4(2) + 1(3) + 2(1) = 3 + 8 + 3 + 2 = 16$
* $y_c[2] = 2(1) + 3(2) + 4(3) + 1(1) = 2 + 6 + 12 + 1 = 21$
* $y_c[3] = 1(1) + 2(2) + 3(3) + 4(1) = 1 + 4 + 9 + 4 = 18$
Result:
$$ y_c[n] = \{ \underset{\uparrow}{15}, 16, 21, 18 \} $$

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
**(a)** State and prove the Circular Convolution Theorem of the DFT. *(6 Marks)*
**(b)** Given two sequences $x_1[n] = \{ \underset{\uparrow}{2}, 1, 2, 1 \}$ and $x_2[n] = \{ \underset{\uparrow}{1}, 2, 3, 4 \}$:
1. Compute the 4-point DFT of $x_1[n]$ and $x_2[n]$. *(4 Marks)*
2. Find $Y[k] = X_1[k] X_2[k]$. *(2 Marks)*
3. Compute the 4-point IDFT to find $y_c[n] = x_1[n] \circledast_4 x_2[n]$. *(3 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Part (a):** Complete derivation shown in Section 2.2 *(6 Marks)*
* **Part (b.1):**
  * $X_1[k] = \mathbf{W}_4 x_1$:
    $X_1[0] = 2+1+2+1 = 6$
    $X_1[1] = 2 - j(1) - 2 + j(1) = 0$
    $X_1[2] = 2 - 1 + 2 - 1 = 2$
    $X_1[3] = 2 + j(1) - 2 - j(1) = 0$
    $X_1[k] = \{ 6, 0, 2, 0 \}$ *(2 Marks)*
  * $X_2[k] = \mathbf{W}_4 x_2$:
    $X_2[0] = 1+2+3+4 = 10$
    $X_2[1] = 1 - 2j - 3 + 4j = -2 + 2j$
    $X_2[2] = 1 - 2 + 3 - 4 = -2$
    $X_2[3] = 1 + 2j - 3 - 4j = -2 - 2j$
    $X_2[k] = \{ 10, -2+2j, -2, -2-2j \}$ *(2 Marks)*
* **Part (b.2):**
  * $Y[0] = 6 \times 10 = 60$
  * $Y[1] = 0 \times (-2+2j) = 0$
  * $Y[2] = 2 \times (-2) = -4$
  * $Y[3] = 0 \times (-2-2j) = 0$
  * $Y[k] = \{ 60, 0, -4, 0 \}$ *(2 Marks)*
* **Part (b.3):**
  * $y_c[n] = \frac{1}{4} \mathbf{W}_4^* Y$:
    * $y_c[0] = \frac{1}{4}(60 + 0 - 4 + 0) = \frac{56}{4} = 14$
    * $y_c[1] = \frac{1}{4}(60 + 0 - (-4) + 0) = \frac{64}{4} = 16$
    * $y_c[2] = \frac{1}{4}(60 + 0 - 4 + 0) = \frac{56}{4} = 14$
    * $y_c[3] = \frac{1}{4}(60 + 0 - (-4) + 0) = \frac{64}{4} = 16$
    $$ y_c[n] = \{ \underset{\uparrow}{14}, 16, 14, 16 \} $$ *(3 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import numpy as np

x1 = np.array([2, 1, 2, 1])
x2 = np.array([1, 2, 3, 4])

X1 = np.fft.fft(x1)
X2 = np.fft.fft(x2)
Y = X1 * X2
yc = np.fft.ifft(Y).real

print("Circular Convolution Output:", np.round(yc))
# Expected: [14, 16, 14, 16]
```
