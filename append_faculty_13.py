import os

extra_content = r"""
### 10.4 Advanced Design Problem (Take-Home Assignment)
**Problem:** Design a digital lowpass filter with a Chebyshev Type 1 response, passband ripple of 1 dB, cutoff frequency of $\pi/4$, and order $N=4$. Implement this filter strictly in Cascade Biquad form using Transposed Direct Form II sections. Ensure your coefficients are scaled such that the maximum gain of any intermediate node does not exceed 1.0. 
*Solution Guide:*
1. **Analog Prototype:** Start with analog Chebyshev Type I.
2. **Bilinear Transform:** Convert to discrete time.
3. **Roots:** Find the 4 poles and 4 zeros of the Z-domain transfer function.
4. **Pairing:** Group the pole pair closest to the unit circle with the zeros closest to them (likely at $z=-1$). Group the second pole pair with the remaining zeros.
5. **Ordering:** Place the low-Q biquad first, high-Q biquad second.
6. **Scaling:** Calculate the $L_\infty$ norm of the first biquad and scale its input coefficients so it cannot overflow. Apply the inverse scaling to the second biquad.
7. **Implementation:** Write the 6 state-variable equations for the two Transposed DF2 sections.

---
## 13. ADDITIONAL SOFTWARE IMPLEMENTATION NOTES

**MATLAB `filter` vs `sosfilt`:**
When teaching this material, a very common question from students is how MATLAB implements these filters.
- `filter(b, a, x)`: Implements the filter exactly as a single Direct Form II Transposed structure. For high orders ($N>6$), this function will suffer from severe numerical instability if the poles are tight.
- `sosfilt(sos, x)`: Implements the filter as a cascade of Second-Order Sections (biquads). The `sos` matrix is an $K \times 6$ matrix where each row contains the $b$ and $a$ coefficients for one biquad. This is the **strongly recommended** function for IIR filtering in MATLAB.

**Python `scipy.signal.lfilter` vs `scipy.signal.sosfilt`:**
The exact same dichotomy exists in Python's SciPy library. 
- `lfilter` computes the direct form difference equation.
- `sosfilt` computes the cascade form.
Always advise students to use `scipy.signal.butter(..., output='sos')` instead of `output='ba'` to extract the biquad coefficients directly.

**C/C++ Implementation Example (Biquad):**
```c
typedef struct {
    float b0, b1, b2, a1, a2;
    float z1, z2; // State variables (delay line)
} Biquad;

float processBiquad(Biquad* filter, float x) {
    // Transposed Direct Form II Implementation
    float out = filter->b0 * x + filter->z1;
    filter->z1 = filter->b1 * x - filter->a1 * out + filter->z2;
    filter->z2 = filter->b2 * x - filter->a2 * out;
    return out;
}
```
This C code perfectly illustrates the hardware efficiency. It requires exactly 5 multiplies, 4 additions, and 2 memory reads/writes per sample. This executes in just a few nanoseconds on a modern ARM Cortex microcontroller, making it suitable for high-resolution audio (192 kHz sample rates).

---
## 14. SUPPLEMENTARY PROOFS

**Proof of Lattice AR Stability Condition ($|K_m| < 1$):**
The stability of the all-pole lattice filter relies on the properties of polynomials orthogonal on the unit circle (Szegő polynomials).
Let $A_m(z)$ be the prediction error filter polynomial of order $m$.
The Levinson step-up recursion is:
$$ A_m(z) = A_{m-1}(z) + K_m z^{-m} A_{m-1}(z^{-1}) $$
We need to prove that if $A_{m-1}(z)$ has all roots strictly inside the unit circle, then $A_m(z)$ also has all roots inside the unit circle if and only if $|K_m| < 1$.
According to Rouché's Theorem from complex analysis, if two functions $f(z)$ and $g(z)$ are analytic inside and on a closed contour $C$, and $|g(z)| < |f(z)|$ on $C$, then $f(z)$ and $f(z) + g(z)$ have the same number of zeros inside $C$.
Let $C$ be the unit circle $|z|=1$.
On the unit circle, $|z^{-m} A_{m-1}(z^{-1})| = |A_{m-1}(z)|$.
Let $f(z) = A_{m-1}(z)$ and $g(z) = K_m z^{-m} A_{m-1}(z^{-1})$.
Then on the unit circle, $|g(z)| = |K_m| |A_{m-1}(z)| = |K_m| |f(z)|$.
If $|K_m| < 1$, then $|g(z)| < |f(z)|$ strictly on the unit circle.
Therefore, $A_m(z) = f(z) + g(z)$ has the exact same number of zeros inside the unit circle as $f(z) = A_{m-1}(z)$.
By mathematical induction, if the 0th order polynomial $A_0(z) = 1$ has no roots outside (trivially stable), then all subsequent orders $A_m(z)$ are strictly stable as long as every $|K_m| < 1$. This completes the proof and demonstrates the immense power of the lattice structure constraint!

---
## 15. FREQUENTLY ASKED QUESTIONS BY STUDENTS

**FAQ 1: Why do we use $z^{-1}$ instead of $z$ in the transfer function?**
We use negative powers of $z$ ($z^{-1}$) because they correspond to *delays* in the time domain, which are physically realizable (causal). A positive power $z^1$ would represent an advance in time, requiring us to look into the future, which is impossible in a real-time DSP system.

**FAQ 2: Can an IIR filter be implemented on an FPGA? Isn't it just for CPUs?**
Yes, IIR filters are regularly implemented on FPGAs. However, the feedback loop inherent in IIR filters means that the next output cannot be completely calculated until the previous output is known. This creates a bottleneck that limits the maximum clock frequency (the "iteration bound"). Pipelining inside the feedback loop is impossible without altering the transfer function. Therefore, FIR filters are more common on FPGAs for ultra-high-speed applications, while IIR filters are used when sharp cutoffs are needed with minimal hardware resources.

**FAQ 3: How do you choose between Cascade and Parallel forms?**
Cascade form is almost universally preferred for frequency-selective filters (like audio EQs or bandpass filters) because the overall transfer function is the *product* of the sections. It's easy to design the stopband by placing zeros on the unit circle, which completely zeroes out the gain in that biquad and thus the entire cascade. Parallel forms are harder to tune for deep stopbands because you rely on destructive interference (subtraction) between the parallel branches, which is sensitive to quantization. However, Parallel forms are preferred when latency and parallel computing speed are the absolute top priority.

---
## END OF DOCUMENT
"""

with open(r"C:\Users\sriph\Downloads\DSP\faculty_notes\lecture_13_faculty.md", "a", encoding="utf-8") as f:
    f.write(extra_content)
    # also add 50 newlines just to be perfectly safe
    f.write("\n" * 50)
