<Faculty Notes — Lecture 21: FIR Specifications & 4 Linear-Phase Types>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY
Linear phase is the primary reason engineers choose FIR filters over IIR filters. A filter with strictly linear phase introduces a pure constant time delay across all frequency components, completely preventing dispersion and phase distortion.

**Pedagogical Strategy:**
1. Formulate the Generalized Linear Phase (GLP) condition: $H(e^{j\omega}) = A(\omega) e^{-j(\alpha \omega - \beta)}$.
2. Prove that constant group delay requires $\beta = 0$ (symmetry) or $\beta = \pi/2$ (antisymmetry), with group delay $\tau_g = \alpha = \frac{N-1}{2}$.
3. Systematically categorize the **4 Types of Linear-Phase FIR Filters**:
   * Type I: Symmetric, $N$ odd (Universal).
   * Type II: Symmetric, $N$ even ($H(e^{j\pi}) = 0 \implies$ CANNOT be HPF or BSF).
   * Type III: Antisymmetric, $N$ odd ($H(e^{j0}) = H(e^{j\pi}) = 0 \implies$ BPF, Differentiator, Hilbert).
   * Type IV: Antisymmetric, $N$ even ($H(e^{j0}) = 0 \implies$ HPF, Differentiator, Hilbert).
4. Prove that roots of linear-phase FIR filters occur in **Conjugate Reciprocal Quadruplets**: $\{z_0, z_0^*, 1/z_0, 1/z_0^*\}$.

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Derive** linear phase conditions for symmetric and antisymmetric FIR impulse responses.
2. **Classify** FIR filters into Types I, II, III, and IV based on length $N$ and symmetry.
3. **Determine** boundary zero constraints at $\omega = 0$ and $\omega = \pi$ for each FIR type.
4. **Select** the appropriate FIR type for specific filter applications (LPF, HPF, BPF, BSF, Differentiators, Hilbert Transformers).
5. **Analyze** zero locations in the complex $z$-plane.

---
## 2. MATHEMATICAL FOUNDATIONS

### 2.1 The 4 Types of Linear-Phase FIR Filters

| Type | Symmetry | Length $N$ (Order $M=N-1$) | Amplitude Function $A(\omega)$ | Mandatory Boundary Zeros | Suitable Applications |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **Type I** | Symmetric ($h[n] = h[N-1-n]$) | $N$ Odd ($M$ Even) | $\sum a[k] \cos(\omega k)$ | None | LPF, HPF, BPF, BSF (Universal) |
| **Type II** | Symmetric ($h[n] = h[N-1-n]$) | $N$ Even ($M$ Odd) | $\sum b[k] \cos(\omega(k-1/2))$ | Zero at $\omega = \pi$ ($z = -1$) | LPF, BPF only |
| **Type III** | Antisymmetric ($h[n] = -h[N-1-n]$) | $N$ Odd ($M$ Even) | $\sum c[k] \sin(\omega k)$ | Zeros at $\omega = 0$ ($z=1$) & $\omega = \pi$ ($z=-1$) | BPF, Differentiator, Hilbert |
| **Type IV** | Antisymmetric ($h[n] = -h[N-1-n]$) | $N$ Even ($M$ Odd) | $\sum d[k] \sin(\omega(k-1/2))$ | Zero at $\omega = 0$ ($z = 1$) | HPF, BPF, Differentiator, Hilbert |

### 2.2 Proof of Mandatory Zeros
* **Type II at $\omega = \pi$ ($z = -1$):**
  $$ H(-1) = \sum_{n=0}^{N-1} h[n] (-1)^{-n} = \sum_{n=0}^{N/2-1} h[n] [(-1)^{-n} + (-1)^{-(N-1-n)}] $$
  Since $N$ is even, $N-1$ is odd $\implies (-1)^{-(N-1-n)} = -(-1)^{-n} \implies H(-1) = 0$.
  Therefore, a Type II filter always has a zero at $\omega = \pi$ and can **never** be used as a Highpass or Bandstop filter.

### 2.3 Zero Quadruplet Locations
Because $h[n]$ is real and symmetric/antisymmetric:
$$ H(z) = \pm z^{-(N-1)} H(z^{-1}) $$
If $z_0 = r e^{j\theta}$ is a zero, then:
1. $z_0^* = r e^{-j\theta}$ is a zero (conjugate symmetry for real coefficients).
2. $1/z_0 = \frac{1}{r} e^{-j\theta}$ is a zero (linear phase symmetry).
3. $1/z_0^* = \frac{1}{r} e^{j\theta}$ is a zero.
Zeros off the unit circle always occur in groups of 4 (quadruplets).

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 21.1: FIR Type Identification & Zero Locations
**Problem:** An FIR filter has transfer function $H(z) = 1 + 2z^{-1} + 3z^{-2} + 2z^{-3} + z^{-4}$.
(a) Determine its FIR Type, filter length $N$, and group delay $\tau_g$.
(b) Can this filter be used as a Highpass filter?

**Solution:**
**(a)** Coefficients: $h = [1, 2, 3, 2, 1]$.
* Length $N = 5$ (Odd), Order $M = 4$ (Even).
* Symmetry: $h[0]=h[4]=1, \; h[1]=h[3]=2, \; h[2]=3 \implies$ **Symmetric**.
* Therefore, it is a **Type I FIR Filter**.
* Group delay: $\tau_g = \frac{N-1}{2} = \frac{5-1}{2} = 2 \text{ samples}$.

**(b)** Highpass Feasibility:
Check $H(e^{j\pi}) = H(-1) = 1 - 2 + 3 - 2 + 1 = 1 \ne 0$.
Since Type I has no mandatory zeros at $\omega = \pi$, it can theoretically operate as a Highpass filter (though this specific impulse response has $H(e^{j0}) = 9$ and $H(e^{j\pi}) = 1$, making it a Lowpass filter).

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
**(a)** State the four types of linear-phase FIR filters and derive the mandatory boundary zeros for Type II, Type III, and Type IV filters. *(9 Marks)*
**(b)** Prove that the roots of a linear-phase FIR filter occur in conjugate reciprocal quadruplets. *(6 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Part (a):**
  * Table of 4 Types with symmetry and length definitions *(3 Marks)*
  * Mathematical proofs showing $H(e^{j\pi})=0$ for Type II, $H(1)=H(-1)=0$ for Type III, and $H(1)=0$ for Type IV *(6 Marks)*
* **Part (b):**
  * Step-by-step proof using $H(z) = \pm z^{-(N-1)} H(z^{-1})$ and complex conjugation $H^*(z) = H(z^*)$ *(6 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import numpy as np

h = np.array([1, 2, 3, 2, 1])
w = np.linspace(0, np.pi, 500)
H = np.polyval(h[::-1], np.exp(-1j * w))

# Phase should be exactly -2*w
phase = np.unwrap(np.angle(H))
group_delay = -np.diff(phase) / np.diff(w)
print(f"Mean Group Delay: {np.mean(group_delay):.4f} samples (Theoretical = 2.0)")
```
