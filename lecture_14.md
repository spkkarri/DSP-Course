# Lecture 14: Linear Filtering of Long Sequences — Overlap-Save (OLS) Method
## EE3621: Digital Signal Processing | III B.Tech EEE

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
  * Parameter formulation: $M = 2 \implies M - 1 = 1$ overlap sample, $N = 4, L = 3$.
  * Block partitioning:
    * $x_0[n] = \{ 0, 2, -1, 3 \}$ (prepend 1 zero)
    * $x_1[n] = \{ 3, 1, 2, 0 \}$ (overlap $x[2]=3$)
    * $x_2[n] = \{ 0, 1, 4, 0 \}$ (overlap $x[5]=0$, pad 1 zero) *(2 Marks)*
  * Circular convolution with $h[n] = \{ 1, -1, 0, 0 \}$ ($N = 4$):
    * $\tilde{y}_0[n] = \{ 0, 2, -1, 3 \} \circledast_4 \{ 1, -1, 0, 0 \} = \{ -3, \mathbf{2, -3, 4} \}$ (Discard index 0)
    * $\tilde{y}_1[n] = \{ 3, 1, 2, 0 \} \circledast_4 \{ 1, -1, 0, 0 \} = \{ 3, \mathbf{-2, 1, -2} \}$ (Discard index 0)
    * $\tilde{y}_2[n] = \{ 0, 1, 4, 0 \} \circledast_4 \{ 1, -1, 0, 0 \} = \{ 0, \mathbf{1, 3, -4} \}$ (Discard index 0) *(4 Marks)*
  * Concatenation of saved parts (zero output additions):
    $$ y[n] = \{ \mathbf{2, -3, 4}, \; \mathbf{-2, 1, -2}, \; \mathbf{1, 3, -4} \} $$
    $$ y[n] = \{ \underset{\uparrow}{2}, -3, 4, -2, 1, -2, 1, 3, -4 \} $$ *(2 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import numpy as np

x = np.array([2, -1, 3, 1, 2, 0, 1, 4])
h = np.array([1, -1])
y = np.convolve(x, h)
print("Direct Linear Convolution:", y)
```


# Pedagogical Guide: Aliasing, Reconstruction, and FFT Filtering

Your intuition is 100% spot on! The standard and most effective way to teach these concepts is by using **"Triangle" Spectral Analysis** to visually demonstrate the **Duality of Aliasing**. 

The "better approach" is to teach these topics not as separate mathematical chores, but as two sides of the exact same coin: **Frequency Aliasing** (when sampling) and **Time Aliasing** (when using the FFT).

Here is a step-by-step pedagogical progression you can use to explain these concepts explicitly in class.

---

## Part 1: Sampling, Reconstruction & Frequency Aliasing
*The problem of making time discrete.*

### 1. The "Triangle" Baseband Spectrum
Don't use complex real-world spectra yet. Represent a generic continuous-time analog signal's spectrum as a **Triangle** in the frequency domain. 
*   **Why a triangle?** It clearly shows the signal has maximum energy at DC ($f=0$), tapers off, and has a strict, hard boundary at a maximum frequency ($f_{max}$). It also makes it visually obvious when two spectra overlap.

### 2. The Act of Sampling (Replication)
Explain that the mathematical act of sampling in the time domain is equivalent to **replicating** that triangle infinitely in the frequency domain, spaced exactly by the sampling frequency ($f_s$).

### 3. Visualizing Aliasing
*   **No Aliasing ($f_s > 2f_{max}$):** The triangles sit side-by-side with empty space (guard bands) between them.
*   **Aliasing ($f_s < 2f_{max}$):** The bases of the triangles overlap. 
*   **The visual payoff:** When the triangles overlap, their amplitudes add together. The sharp corner of the triangle is destroyed, and the shape is permanently warped. This warped triangle proves that high frequencies have folded back and corrupted the low frequencies.

![Sampling Replication](../images/sampling_frequency_replication.png)

### 4. Perfect Reconstruction
How do we get the continuous signal back? We pass it through a DAC (Digital-to-Analog Converter) and an analog low-pass filter. 
*   **Visually:** Draw a rectangular box (an ideal low-pass filter) exactly over the center triangle (from $-f_{max}$ to $+f_{max}$).
*   If the triangles were separated (Nyquist met), the rectangle perfectly isolates the original triangle. Perfect reconstruction!
*   If they overlapped (Aliasing), the rectangle captures the warped, overlapping tails. The original signal is lost forever.

---

## Part 2: FFT Linear Filtering & Time Aliasing
*The problem of making frequency discrete.*

Now, pivot to the FFT. Students often think they can just take the FFT of a signal, multiply it by the FFT of a filter, and take the IFFT to get the filtered signal. 

### 1. The "Circular" Trap
Explain the core rule of DSP duality: Just as making time discrete caused frequency to become periodic (the repeating triangles), **making frequency discrete (which the FFT does) causes time to become periodic!**
*   Because the FFT assumes the time signal loops infinitely, multiplying two FFTs results in **Circular Convolution**, not Linear Convolution.

### 2. Visualizing Time Aliasing
Use rectangular pulses in the time domain as your visual aid here (instead of frequency triangles). Convolving two rectangles in time creates a triangle/trapezoid.
*   If your FFT size ($N$) is too small, the tail of that resulting triangle wraps around the circle and overlaps with the beginning of the signal.
*   **The Aha! Moment:** Tell the students, *"Remember how sampling too slowly caused the frequency triangles to overlap? Using an FFT size that is too small causes the time-domain signals to overlap! This is called **Time Aliasing**."*

### 3. The Solution: Zero-Padding
To prevent frequency aliasing, we increase the sampling rate (add more space between triangles). 
To prevent time aliasing, we **Zero-Pad** the signals (add empty space at the end of the time vectors). 
*   If signal A has length $M$ and filter B has length $N$, the FFT size must be at least $L \ge M + N - 1$. The zeros act as a "buffer" so the tail of the convolution has room to die out before wrapping around.

---

## Part 3: Overlap-Add and Overlap-Save
*Scaling it to infinite streams.*

Finally, address practical streaming. If we have a 1-hour audio file, we can't take a 1-hour FFT. We must chop the signal into blocks. But chopping it up causes boundary issues during convolution.

### 1. Overlap-Add (The "Tail" Method)
*   **Concept:** We take a block of data, zero-pad it, and FFT filter it. The linear convolution creates a "tail" that spills past the original block length.
*   **Action:** We must mathematically **ADD** that overlapping tail to the beginning of the *next* block to get the correct result.
*   **Visual:** Draw blocks with overlapping triangle tails being summed together.

![Overlap Add](../images/overlap_add.png)

### 2. Overlap-Save (The "Trash" Method)
*   **Concept:** Instead of zero-padding, we deliberately allow Time Aliasing to happen!
*   **Action:** We take overlapping blocks of input data. We circular-convolve via FFT. We know the first $M-1$ samples are corrupted by time-aliasing wrap-around. So, we simply throw them in the trash (discard them) and **SAVE** the remaining uncorrupted samples.

![Overlap Save](../images/overlap_save.png)

---

## Summary of the "Better Approach"
By using the **Triangle** concept in frequency to teach Nyquist, and then immediately mirroring that exact same overlapping logic in the time domain to teach FFT Circular Convolution, you unify the two hardest topics in DSP. 

*   **Under-sampling $\rightarrow$ Frequency Overlap (Spectral Aliasing)**
*   **Under-sizing the FFT $\rightarrow$ Time Overlap (Circular/Time Aliasing)**
