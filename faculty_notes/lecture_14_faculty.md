<Faculty Notes — Lecture 14: Linear Filtering: Overlap-Save (OLS) Method>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY
The **Overlap-Save (OLS)** method (also called Overlap-Discard) is an alternative block-filtering method where input blocks overlap by $M-1$ samples. Rather than adding output tails as in OLA, the corrupted aliased samples are simply discarded from the circular convolution output.

**Pedagogical Strategy:**
1. Formulate input block partitioning with $M-1$ sample overlap: $x_m[n] = x[mL + n - (M-1)]$.
2. Explain why the first $M-1$ points of circular convolution represent wrap-around aliasing.
3. Demonstrate that the remaining $L$ points exactly equal the linear convolution.
4. Compare Overlap-Add and Overlap-Save:
   * OLA: Disjoint inputs $\to$ Overlapping output additions.
   * OLS: Overlapping inputs $\to$ Discard aliased output prefix; direct concatenation.
5. Explain why OLS is preferred in SIMD/GPU architectures because it requires zero output additions (pure memory copy).

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Formulate** overlapping input blocks for the Overlap-Save algorithm.
2. **Execute** numerical filtering via Overlap-Save and identify aliased regions.
3. **Compare** OLA and OLS in terms of memory access, register operations, and arithmetic complexity.
4. **Select** optimal block sizes for real-time DSP implementation.

---
## 2. MATHEMATICAL FOUNDATIONS

### 2.1 Overlap-Save Block Formulation
Let FIR filter $h[n]$ have length $M$. Choose block length $L$ such that total FFT length is $N = L + M - 1$.
Construct input blocks $x_m[n]$ of length $N$ by prepending the last $M-1$ points from block $m-1$:
$$ x_m[n] = x[mL + n - (M-1)], \quad 0 \le n \le N-1 $$
For the first block ($m=0$), prepend $M-1$ zeros:
$$ x_0[n] = \{ \underbrace{0, 0, \dots, 0}_{M-1 \text{ zeros}}, x[0], x[1], \dots, x[L-1] \} $$

### 2.2 Circular Convolution & Discard Mechanism
Zero-pad $h[n]$ to length $N$. Compute the $N$-point circular convolution:
$$ \tilde{y}_m[n] = x_m[n] \circledast_N h[n] = \text{IDFT}_N\{\text{DFT}_N\{x_m\} \cdot \text{DFT}_N\{h\}\} $$
The output contains:
* Samples $n = 0, 1, \dots, M-2$: **Corrupted by circular wrap-around aliasing $\implies$ DISCARD**.
* Samples $n = M-1, M, \dots, N-1$: **Valid linear convolution samples $\implies$ SAVE**.

### 2.3 Synthesis of Output
The total linear convolution $y[n]$ is formed by direct concatenation of the saved portions:
$$ y[mL + r] = \tilde{y}_m[r + M - 1], \quad 0 \le r \le L-1 $$

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 14.1: Complete Overlap-Save Filtering
**Problem:** Filter the input sequence $x[n] = \{ \underset{\uparrow}{1}, 2, -1, 2, 3, -2, 0, 1, 2, 1 \}$ of length $L_x = 10$ with the FIR impulse response $h[n] = \{ \underset{\uparrow}{1}, 2, 1 \}$ of length $M = 3$ using the Overlap-Save method with circular FFT length $N = 6$ ($L = 4$).

**Solution:**

#### Step 1: Filter and Block Parameter Formulation
* Filter length: $M = 3$
* Number of overlap samples: $M - 1 = 2$
* Circular convolution / FFT block length: $N = 6$
* New input samples processed per block: $L = N - M + 1 = 6 - 3 + 1 = 4$
* Zero-pad the filter $h[n]$ to length $N = 6$:
  $$ h[n] = \{ 1, 2, 1, 0, 0, 0 \} $$

#### Step 2: Construct Input Blocks of Length $N = 6$
Each block is formed by taking $M - 1 = 2$ overlap samples from the preceding block followed by $L = 4$ new input samples:
$$ x_m[n] = x[mL + n - (M - 1)], \quad 0 \le n \le N - 1 $$

* **Block 0 ($m = 0$):** Prepend $M - 1 = 2$ zeros:
  $$ x_0[n] = \{ 0, 0, x[0], x[1], x[2], x[3] \} = \{ 0, 0, 1, 2, -1, 2 \} $$
* **Block 1 ($m = 1$):** Overlap the last 2 samples of block 0 ($x[2] = -1, x[3] = 2$):
  $$ x_1[n] = \{ x[2], x[3], x[4], x[5], x[6], x[7] \} = \{ -1, 2, 3, -2, 0, 1 \} $$
* **Block 2 ($m = 2$):** Overlap the last 2 samples of block 1 ($x[6] = 0, x[7] = 1$), zero-pad at end:
  $$ x_2[n] = \{ x[6], x[7], x[8], x[9], 0, 0 \} = \{ 0, 1, 2, 1, 0, 0 \} $$

#### Step 3: Circular Convolution Formula & Mathematical Formulation
The circular convolution of two $N$-point sequences $x_m[n]$ and $h[n]$ is defined by:
$$ \tilde{y}_m[n] = x_m[n] \circledast_N h[n] = \sum_{k=0}^{N-1} h[k] \, x_m[((n - k))_N], \quad 0 \le n \le N - 1 $$
where the double-parentheses index $((n - k))_N = (n - k) \bmod N$ represents the modulo-$N$ periodic circular time-shift.

Since $h[n] = \{1, 2, 1, 0, 0, 0\}$ with $N = 6$, only $h[0] = 1$, $h[1] = 2$, and $h[2] = 1$ are non-zero. Substituting these into the formula yields the 3-tap circular difference equation:
$$ \tilde{y}_m[n] = 1 \cdot x_m[((n))_6] + 2 \cdot x_m[((n - 1))_6] + 1 \cdot x_m[((n - 2))_6], \quad 0 \le n \le 5 $$

In matrix form, this circular convolution corresponds to multiplying the input vector by the $6 \times 6$ circulant matrix $H_c$:
$$ \begin{bmatrix} \tilde{y}_m[0] \\ \tilde{y}_m[1] \\ \tilde{y}_m[2] \\ \tilde{y}_m[3] \\ \tilde{y}_m[4] \\ \tilde{y}_m[5] \end{bmatrix} = \begin{bmatrix} 1 & 0 & 0 & 0 & 1 & 2 \\ 2 & 1 & 0 & 0 & 0 & 1 \\ 1 & 2 & 1 & 0 & 0 & 0 \\ 0 & 1 & 2 & 1 & 0 & 0 \\ 0 & 0 & 1 & 2 & 1 & 0 \\ 0 & 0 & 0 & 1 & 2 & 1 \end{bmatrix} \begin{bmatrix} x_m[0] \\ x_m[1] \\ x_m[2] \\ x_m[3] \\ x_m[4] \\ x_m[5] \end{bmatrix} $$

Notice that for $n = 0$ and $n = 1$, terms wrap around from the end of the block ($x_m[4]$ and $x_m[5]$), causing **time-domain circular aliasing**. For $n = 2, 3, 4, 5$, no wrap-around occurs, so the output matches the exact **linear convolution**.

#### Step 4: Detailed Step-by-Step Block Computations

**1. Block 0 ($m = 0$):** $x_0[n] = \{ 0, 0, 1, 2, -1, 2 \}$
* $n = 0$: $\tilde{y}_0[0] = x_0[0] + 2x_0[5] + x_0[4] = 0 + 2(2) + (-1) = 3$ $\implies$ **DISCARD (Aliased)**
* $n = 1$: $\tilde{y}_0[1] = x_0[1] + 2x_0[0] + x_0[5] = 0 + 2(0) + 2 = 2$ $\implies$ **DISCARD (Aliased)**
* $n = 2$: $\tilde{y}_0[2] = x_0[2] + 2x_0[1] + x_0[0] = 1 + 2(0) + 0 = 1$ $\implies$ **SAVE ($y[0] = 1$)**
* $n = 3$: $\tilde{y}_0[3] = x_0[3] + 2x_0[2] + x_0[1] = 2 + 2(1) + 0 = 4$ $\implies$ **SAVE ($y[1] = 4$)**
* $n = 4$: $\tilde{y}_0[4] = x_0[4] + 2x_0[3] + x_0[2] = -1 + 2(2) + 1 = 4$ $\implies$ **SAVE ($y[2] = 4$)**
* $n = 5$: $\tilde{y}_0[5] = x_0[5] + 2x_0[4] + x_0[3] = 2 + 2(-1) + 2 = 2$ $\implies$ **SAVE ($y[3] = 2$)**

Output for Block 0:
$$ \tilde{y}_0[n] = \{ \underbrace{3, 2}_{\text{Discard (Aliased)}}, \quad \underbrace{\mathbf{1, 4, 4, 2}}_{\text{Save (Linear Conv)}} \} $$

**2. Block 1 ($m = 1$):** $x_1[n] = \{ -1, 2, 3, -2, 0, 1 \}$
* $n = 0$: $\tilde{y}_1[0] = x_1[0] + 2x_1[5] + x_1[4] = -1 + 2(1) + 0 = 1$ $\implies$ **DISCARD (Aliased)**
* $n = 1$: $\tilde{y}_1[1] = x_1[1] + 2x_1[0] + x_1[5] = 2 + 2(-1) + 1 = 1$ $\implies$ **DISCARD (Aliased)**
* $n = 2$: $\tilde{y}_1[2] = x_1[2] + 2x_1[1] + x_1[0] = 3 + 2(2) + (-1) = 6$ $\implies$ **SAVE ($y[4] = 6$)**
* $n = 3$: $\tilde{y}_1[3] = x_1[3] + 2x_1[2] + x_1[1] = -2 + 2(3) + 2 = 6$ $\implies$ **SAVE ($y[5] = 6$)**
* $n = 4$: $\tilde{y}_1[4] = x_1[4] + 2x_1[3] + x_1[2] = 0 + 2(-2) + 3 = -1$ $\implies$ **SAVE ($y[6] = -1$)**
* $n = 5$: $\tilde{y}_1[5] = x_1[5] + 2x_1[4] + x_1[3] = 1 + 2(0) + (-2) = -1$ $\implies$ **SAVE ($y[7] = -1$)**

Output for Block 1:
$$ \tilde{y}_1[n] = \{ \underbrace{1, 1}_{\text{Discard (Aliased)}}, \quad \underbrace{\mathbf{6, 6, -1, -1}}_{\text{Save (Linear Conv)}} \} $$

**3. Block 2 ($m = 2$):** $x_2[n] = \{ 0, 1, 2, 1, 0, 0 \}$
* $n = 0$: $\tilde{y}_2[0] = x_2[0] + 2x_2[5] + x_2[4] = 0 + 2(0) + 0 = 0$ $\implies$ **DISCARD (Aliased)**
* $n = 1$: $\tilde{y}_2[1] = x_2[1] + 2x_2[0] + x_2[5] = 1 + 2(0) + 0 = 1$ $\implies$ **DISCARD (Aliased)**
* $n = 2$: $\tilde{y}_2[2] = x_2[2] + 2x_2[1] + x_2[0] = 2 + 2(1) + 0 = 4$ $\implies$ **SAVE ($y[8] = 4$)**
* $n = 3$: $\tilde{y}_2[3] = x_2[3] + 2x_2[2] + x_2[1] = 1 + 2(2) + 1 = 6$ $\implies$ **SAVE ($y[9] = 6$)**
* $n = 4$: $\tilde{y}_2[4] = x_2[4] + 2x_2[3] + x_2[2] = 0 + 2(1) + 2 = 4$ $\implies$ **SAVE ($y[10] = 4$)**
* $n = 5$: $\tilde{y}_2[5] = x_2[5] + 2x_2[4] + x_2[3] = 0 + 2(0) + 1 = 1$ $\implies$ **SAVE ($y[11] = 1$)**

Output for Block 2:
$$ \tilde{y}_2[n] = \{ \underbrace{0, 1}_{\text{Discard (Aliased)}}, \quad \underbrace{\mathbf{4, 6, 4, 1}}_{\text{Save (Linear Conv)}} \} $$

#### Step 5: Output Assembly by Direct Concatenation
In Overlap-Save, the total linear convolution output requires **zero arithmetic additions**; the saved segments are concatenated directly:
$$ y[n] = \{ \mathbf{1, 4, 4, 2}, \quad \mathbf{6, 6, -1, -1}, \quad \mathbf{4, 6, 4, 1} \} $$
$$ y[n] = \{ \underset{\uparrow}{1}, 4, 4, 2, 6, 6, -1, -1, 4, 6, 4, 1 \} $$

#### Step 6: Analytical Verification via Direct Linear Convolution
The length of linear convolution is $L_{\text{total}} = L_x + M - 1 = 10 + 3 - 1 = 12$:
$$ y_{\text{lin}}[n] = x[n] * h[n] = \sum_{k=0}^{2} h[k] \, x[n - k] $$
* $y[0] = 1(1) = 1$
* $y[1] = 2(1) + 1(2) = 4$
* $y[2] = -1(1) + 2(2) + 1(1) = 4$
* $y[3] = 2(1) - 1(2) + 2(1) = 2$
* $y[4] = 3(1) + 2(2) - 1(1) = 6$
* $y[5] = -2(1) + 3(2) + 2(1) = 6$
* $y[6] = 0(1) - 2(2) + 3(1) = -1$
* $y[7] = 1(1) + 0(2) - 2(1) = -1$
* $y[8] = 2(1) + 1(2) + 0(1) = 4$
* $y[9] = 1(1) + 2(2) + 1(1) = 6$
* $y[10] = 0(1) + 1(2) + 2(1) = 4$
* $y[11] = 0(1) + 0(2) + 1(1) = 1$

$$ y_{\text{lin}}[n] = \{ \underset{\uparrow}{1}, 4, 4, 2, 6, 6, -1, -1, 4, 6, 4, 1 \} $$
The Overlap-Save reconstruction matches the direct linear convolution exactly across all 12 points.

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
**(a)** Compare the Overlap-Add and Overlap-Save methods in detail. Under what conditions is Overlap-Save preferred? *(7 Marks)*
**(b)** Filter $x[n] = \{ \underset{\uparrow}{2}, -1, 3, 1, 2, 0, 1, 4 \}$ with $h[n] = \{ \underset{\uparrow}{1}, -1 \}$ using the Overlap-Save method with $N = 4$ ($L = 3$). *(8 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Part (a):**
  * Detailed structural comparison covering input buffering, convolution, and output synthesis *(4 Marks)*
  * Explanation: OLS avoids output additions, making it ideal for DMA streaming and parallel SIMD/GPU memory copy pipelines *(3 Marks)*
* **Part (b):**
  * $M=2 \implies M-1=1$ overlap sample. $N=4, L=3$.
  * Block partitioning:
    $x_0 = \{0, 2, -1, 3\}$
    $x_1 = \{3, 1, 2, 0\}$
    $x_2 = \{0, 1, 4, 0\}$ *(2 Marks)*
  * Circular convolution with $h = \{1, -1, 0, 0\}$:
    $\tilde{y}_0 = \{0, 2, -1, 3\} \circledast_4 \{1, -1, 0, 0\} = \{-3, \mathbf{2, -3, 4}\}$ (Discard index 0)
    $\tilde{y}_1 = \{3, 1, 2, 0\} \circledast_4 \{1, -1, 0, 0\} = \{3, \mathbf{-2, 1, -2}\}$ (Discard index 0)
    $\tilde{y}_2 = \{0, 1, 4, 0\} \circledast_4 \{1, -1, 0, 0\} = \{0, \mathbf{1, 3, -4}\}$ (Discard index 0) *(4 Marks)*
  * Concatenation of saved parts:
    $y[n] = \{2, -3, 4, -2, 1, -2, 1, 3, -4\}$ *(2 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import numpy as np

x = np.array([2, -1, 3, 1, 2, 0, 1, 4])
h = np.array([1, -1])
y = np.convolve(x, h)
print("Direct Linear Convolution:", y)
```
