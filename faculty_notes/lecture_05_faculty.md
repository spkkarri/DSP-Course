</Agent System Instructions>
<Faculty Notes — Lecture 5: Z-Transform & ROC>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY
The Z-transform is arguably the most critical mathematical tool introduced in the first half of a DSP course. It serves as the discrete-time analogue of the Laplace transform from continuous-time signal analysis. The conceptual leap from the continuous-time domain to discrete-time sequences often trips students up. 

When teaching this lecture, it is imperative to spend extra time on the Region of Convergence (ROC). The ROC is the most commonly misunderstood concept in this topic. Students tend to treat the Z-transform formula merely as an algebraic exercise without considering where the series actually converges. Ensure that you consistently connect stability to the ROC containing the unit circle.

Suggested demos:
- Use MATLAB or a Python script to plot 3D surfaces of $|X(z)|$ for simple sequences like $a^n u[n]$. Show how the surface blows up at the poles and how the ROC defines the "safe" regions where the sum is finite. For example, plotting the magnitude of $1/(1-0.9z^{-1})$ over the complex plane clearly visualizes the pole at $0.9$.
- Visually demonstrate the mapping from the $s$-plane to the $z$-plane ($z = e^{sT}$). Show how the left half-plane maps to the interior of the unit circle, the $j\Omega$ axis maps to the unit circle itself, and the right half-plane maps to the exterior. This is a crucial preview of filter design.
- Common student difficulties include confusing left-sided vs right-sided ROCs, failing to understand why the intersection of ROCs is necessary for linearity, and struggling with the geometric series formulation for negative indices. Walk through negative index summation extremely slowly.

---
## 1. LEARNING OBJECTIVES
By the end of this comprehensive lecture, students will be able to:
1. Define the bilateral Z-transform mathematically and explain its relationship to the Discrete-Time Fourier Transform (DTFT) using polar coordinates.
2. Determine and sketch the Region of Convergence (ROC) for finite-length, right-sided, left-sided, and two-sided sequences on the complex z-plane.
3. Derive the Z-transforms and corresponding ROCs from first principles for fundamental discrete-time signals including the impulse, unit step, decaying/growing exponentials, and sinusoidal sequences.
4. Apply the mathematical properties of the Z-transform (linearity, time shift, scaling, time reversal, differentiation, conjugation, and convolution) to simplify the analysis of complex, composite signals.
5. Prove the Initial Value Theorem and Final Value Theorem, and apply them correctly to determine steady-state and transient behaviors with rigorous consideration of their convergence conditions.
6. Evaluate the Bounded-Input Bounded-Output (BIBO) stability and causality of a discrete-time Linear Time-Invariant (LTI) system by exhaustively analyzing its pole-zero locations and the corresponding ROC.
7. Synthesize inverse Z-transform concepts conceptually by determining which time-domain signal corresponds to a given rational algebraic expression based solely on the specified ROC.
8. Model real-world engineering problems (such as digital motor control stability or audio equalization) using rational Z-transforms and pole-zero placements.

---
## 2. PREREQUISITE KNOWLEDGE REVIEW
Students must be comfortable with the following mathematical concepts before beginning this lecture. Briefly review these on the whiteboard at the start of class:

**A. Geometric Series:**
The infinite geometric series is the foundation of almost all Z-transform derivations. Write this on the board and leave it there for the entire lecture.
Formula:
$$\sum_{n=0}^{\infty} \alpha^n = 1 + \alpha + \alpha^2 + \alpha^3 + \dots = \frac{1}{1 - \alpha}, \quad \text{for } |\alpha| < 1$$
Finite sum formula (for finite duration sequences):
$$\sum_{n=0}^{N-1} \alpha^n = 1 + \alpha + \dots + \alpha^{N-1} = \frac{1 - \alpha^N}{1 - \alpha}, \quad \text{for } \alpha \neq 1$$
Emphasize that the condition $|\alpha| < 1$ is non-negotiable for convergence of the infinite series. This inequality is where the ROC originates.

**B. Discrete-Time Fourier Transform (DTFT):**
Recall the definition of the DTFT:
$$X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n}$$
Remind students that the DTFT only converges if the signal is absolutely summable ($\sum |x[n]| < \infty$). Ask the class: "What happens if we try to take the DTFT of $u[n]$?" (Answer: It doesn't converge in the strict sense, requiring Dirac delta distributions).

**C. Complex Analysis Basics:**
- Polar representation of complex numbers: $z = r e^{j\theta}$
- Euler's formula: $e^{j\theta} = \cos(\theta) + j\sin(\theta)$
- Magnitude and phase: $|z| = r$, $\angle z = \theta$
- Complex conjugate: $z^* = r e^{-j\theta}$

**D. Pole-Zero Diagrams:**
Review the concept of roots of polynomials. For a rational function $H(z) = \frac{N(z)}{D(z)}$:
Roots of the numerator polynomial $N(z)$ are zeros (where the function evaluates to 0).
Roots of the denominator polynomial $D(z)$ are poles (where the function goes to infinity).

---
## 3. HISTORICAL AND MOTIVATIONAL CONTEXT

**Historical Context:**
The fundamental mathematics of the Z-transform date back to 1730 with Abraham de Moivre introduced the concept of generating functions in probability theory. In 1843, Pierre-Alphonse Laurent formalized Laurent series expansions, which the Z-transform relies upon algebraically. 
However, its formal introduction into modern engineering, and its current name, are attributed to Witold Hurewicz and John R. Ragazzini in 1947. Working during and shortly after World War II, they needed mathematical tools to solve linear difference equations in sampled-data control systems for radar tracking and anti-aircraft fire control. 
The letter "Z" originally stood for the "Z-transform" simply as a letter choice to represent the discrete counterpart to the "S" used in the Laplace transform. During the 1960s, with the advent of digital computers and the Cooley-Tukey Fast Fourier Transform (FFT) algorithm, discrete methods exploded in popularity. The Z-transform became the mathematical backbone of digital filter analysis and design, completely revolutionizing telecommunications.

**Motivational Context:**
Why do EEE students need this? The DTFT is powerful for analyzing the frequency content of stable signals. However, the DTFT fails to converge for many practical, real-world signals, such as the unit step function $u[n]$ or growing exponentials $2^n u[n]$. Furthermore, analyzing transient behaviors, system stability, and feedback loops using linear constant-coefficient difference equations directly in the time domain is mathematically cumbersome and prone to error. 
The Z-transform converts these difficult discrete-time difference equations into straightforward algebraic polynomial equations in the complex variable $z$. It allows engineers to use algebra rather than calculus or convolution sums. It is the fundamental tool that allows engineers to design digital controllers for power electronics (inverters, DC-DC converters), motor drives (FOC control), and audio/image processing algorithms (digital equalizers, noise reduction filters). Without the Z-transform, modern digital engineering would not exist.

---
## 4. THEORETICAL FOUNDATIONS

### 4.1 Bilateral Z-Transform Definition
The bilateral (or two-sided) Z-transform of a discrete-time signal $x[n]$ is mathematically defined as a Laurent series:
$$X(z) = \sum_{n=-\infty}^{\infty} x[n] z^{-n}$$
where $z$ is a complex variable in the general complex plane.

To deeply understand its relation to the DTFT and why it solves the convergence problem, let us express $z$ in polar form:
$$z = r e^{j\omega}$$
where $r = |z|$ is the magnitude (radius) and $\omega = \angle z$ is the angle (frequency).
Substitute this polar representation into the fundamental definition:
$$X(r e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] (r e^{j\omega})^{-n}$$
By distributing the negative exponent:
$$X(r e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] r^{-n} e^{-j\omega n}$$
Rearranging the terms to group the magnitude components:
$$X(r e^{j\omega}) = \sum_{n=-\infty}^{\infty} \left[ x[n] r^{-n} \right] e^{-j\omega n}$$

**Physical and Mathematical Insight:** 
This equation is a revelation. It proves that the Z-transform of $x[n]$ evaluated at a specific complex point $z = r e^{j\omega}$ is exactly identically to the DTFT of a modified sequence $y[n] = x[n] r^{-n}$. 
The factor $r^{-n}$ acts as an exponential weighting function. 
- If $x[n]$ is a growing exponential that doesn't have a DTFT, we can choose a large radius $r$ such that $r^{-n}$ forces the product $x[n] r^{-n}$ to decay to zero as $n \to \infty$, thereby forcing the DTFT to converge.
- If we set $r=1$ (i.e., we evaluate the Z-transform strictly on the unit circle in the $z$-plane), the weighting factor becomes $1^{-n} = 1$, and we perfectly recover the DTFT:
$$X(z) \Big|_{z = e^{j\omega}} = X(e^{j\omega})$$

### 4.2 Region of Convergence (ROC) — Complete Analysis
The infinite series defining $X(z)$ does not magically converge for all complex values of $z$. The set of all values of $z$ for which $X(z)$ attains a finite analytical value is called the Region of Convergence (ROC).
Mathematically, convergence of the Laurent series requires absolute summability of the modified sequence:
$$\sum_{n=-\infty}^{\infty} |x[n] z^{-n}| = \sum_{n=-\infty}^{\infty} |x[n]| |z|^{-n} = \sum_{n=-\infty}^{\infty} |x[n]| r^{-n} < \infty$$
The geometric shape and extent of the ROC are entirely dictated by the temporal duration and sidedness of the sequence $x[n]$.

**(a) Finite-Length Sequences:**
Assume $x[n]$ is non-zero only for a finite interval $N_1 \le n \le N_2$.
$$X(z) = \sum_{n=N_1}^{N_2} x[n] z^{-n}$$
This is a finite sum of finite terms, which mathematically must always yield a finite result. The only potential mathematical singularities occur at the boundaries of the $z$-plane:
- If $N_2 > 0$, the sum includes negative powers of $z$ (e.g., $z^{-1}, z^{-2}$). If $z=0$, these terms evaluate to $1/0 \to \infty$. Thus, $z=0$ must be excluded.
- If $N_1 < 0$, the sum includes positive powers of $z$ (e.g., $z^1, z^2$). If $z=\infty$, these terms blow up. Thus, $z=\infty$ must be excluded.
**Conclusion:** The ROC is the entire $z$-plane, except possibly $z=0$ and/or $z=\infty$.

**(b) Right-Sided Sequences (Causal):**
A sequence is right-sided if $x[n] = 0$ for $n < N_1$. It extends infinitely in the positive $n$ direction.
For the sum $\sum_{n=N_1}^{\infty} x[n] r^{-n}$ to converge, the decaying factor $r^{-n}$ must overpower any growth in $x[n]$. This requires a large radius $r$. 
**Conclusion:** The ROC extends outward from the outermost pole to infinity. It is of the form $|z| > r_{max}$. If $N_1 \ge 0$ (a strictly causal sequence), the sum has no positive powers of $z$, so the ROC includes $z=\infty$.

**(c) Left-Sided Sequences (Anti-causal):**
A sequence is left-sided if $x[n] = 0$ for $n > N_2$. It extends infinitely in the negative $n$ direction.
For the sum $\sum_{n=-\infty}^{N_2} x[n] r^{-n}$ to converge, we are looking at terms like $r^{+|n|}$. To prevent this from blowing up as $n \to -\infty$, $r$ must be small.
**Conclusion:** The ROC extends inward from the innermost pole to zero. It is of the form $|z| < r_{min}$. If $N_2 \le 0$, the sum has no negative powers of $z$, so the ROC includes $z=0$.

**(d) Two-Sided Sequences:**
If the sequence extends to both $+\infty$ and $-\infty$, we must analytically split it into a right-sided part (requiring $|z| > r_1$) and a left-sided part (requiring $|z| < r_2$). The overall ROC must satisfy BOTH conditions simultaneously, meaning it is the intersection of the two ROCs.
**Conclusion:** The ROC is an annular ring defined by $r_1 < |z| < r_2$. If $r_1 > r_2$, the intersection is the empty set, and the Z-transform simply does not exist for that sequence.

**(e) DTFT Existence and Stability connection:**
If the ROC includes the unit circle ($|z|=1$), then the DTFT $X(e^{j\omega})$ exists and converges. For a system impulse response $h[n]$, if the ROC includes the unit circle, the system is Bounded-Input Bounded-Output (BIBO) stable.

### 4.3 Common Z-Transform Pairs with FULL Derivations

**1. Unit Impulse: $\delta[n]$**
Definition: $\delta[n] = 1$ for $n=0$ and $0$ otherwise.
$$X(z) = \sum_{n=-\infty}^{\infty} \delta[n] z^{-n} = \delta[0] z^0 = 1 \cdot 1 = 1$$
ROC: All $z$.

**2. Unit Step: $u[n]$**
Definition: $u[n] = 1$ for $n \ge 0$ and $0$ otherwise.
$$X(z) = \sum_{n=-\infty}^{\infty} u[n] z^{-n} = \sum_{n=0}^{\infty} 1 \cdot z^{-n} = \sum_{n=0}^{\infty} (z^{-1})^n$$
This is a geometric series with common ratio $\alpha = z^{-1}$.
Using the geometric series formula, this converges strictly if and only if $|\alpha| < 1 \implies |z^{-1}| < 1 \implies |z| > 1$.
$$X(z) = \frac{1}{1 - z^{-1}} = \frac{z}{z - 1}$$
ROC: $|z| > 1$. (A causal sequence, exterior ROC).

**3. Right-Sided Exponential: $a^n u[n]$**
$$X(z) = \sum_{n=-\infty}^{\infty} a^n u[n] z^{-n} = \sum_{n=0}^{\infty} a^n z^{-n} = \sum_{n=0}^{\infty} (a z^{-1})^n$$
This is a geometric series with common ratio $\alpha = a z^{-1}$.
Converges if $|\alpha| < 1 \implies |a z^{-1}| < 1 \implies |a| / |z| < 1 \implies |z| > |a|$.
$$X(z) = \frac{1}{1 - a z^{-1}} = \frac{z}{z - a}$$
ROC: $|z| > |a|$. 

**4. Left-Sided Exponential: $-a^n u[-n-1]$**
This is a notoriously tricky derivation. Pay close attention.
The sequence is non-zero only for $n \le -1$.
$$X(z) = \sum_{n=-\infty}^{\infty} -a^n u[-n-1] z^{-n} = -\sum_{n=-\infty}^{-1} a^n z^{-n}$$
Introduce a change of variables to make indices positive: let $m = -n$. As $n$ goes from $-1$ down to $-\infty$, $m$ goes from $1$ up to $\infty$.
$$X(z) = -\sum_{m=1}^{\infty} a^{-m} z^m = -\sum_{m=1}^{\infty} (a^{-1} z)^m$$
This is a geometric series starting at $m=1$. To use the standard formula, add and subtract the $m=0$ term:
$$X(z) = - \left( \sum_{m=0}^{\infty} (a^{-1} z)^m - 1 \right)$$
Converges strictly if $|a^{-1} z| < 1 \implies |z| / |a| < 1 \implies |z| < |a|$.
Assuming convergence, apply the sum formula:
$$X(z) = - \left( \frac{1}{1 - a^{-1} z} - 1 \right) = - \left( \frac{1 - (1 - a^{-1} z)}{1 - a^{-1} z} \right) = - \left( \frac{a^{-1} z}{1 - a^{-1} z} \right)$$
Multiply the numerator and denominator by $a z^{-1}$ to clear the complex fraction:
$$X(z) = \frac{- (a^{-1} z)(a z^{-1})}{(1 - a^{-1} z)(a z^{-1})} = \frac{-1}{a z^{-1} - 1} = \frac{1}{1 - a z^{-1}} = \frac{z}{z - a}$$
ROC: $|z| < |a|$.
*Crucial Observation:* The algebraic expression $\frac{z}{z-a}$ is IDENTICAL to the right-sided exponential. Only the ROC distinguishes them!

**5. Polynomial-Exponential Sequence: $n a^n u[n]$**
This will be rigorously derived using the differentiation property in Section 4.4.

**6. Cosine Sequence: $\cos(\omega_0 n) u[n]$**
Using Euler's identity: $\cos(\omega_0 n) = \frac{e^{j\omega_0 n} + e^{-j\omega_0 n}}{2}$
The sequence can be expressed as a sum of two complex exponentials:
$$x[n] = \frac{1}{2}(e^{j\omega_0})^n u[n] + \frac{1}{2}(e^{-j\omega_0})^n u[n]$$
Using the standard $a^n u[n]$ pair derived above, with $a_1 = e^{j\omega_0}$ and $a_2 = e^{-j\omega_0}$:
$$X(z) = \frac{1}{2} \left[ \frac{1}{1 - e^{j\omega_0}z^{-1}} \right] + \frac{1}{2} \left[ \frac{1}{1 - e^{-j\omega_0}z^{-1}} \right]$$
The ROC for the first term requires $|z| > |e^{j\omega_0}| = 1$. The ROC for the second term requires $|z| > |e^{-j\omega_0}| = 1$. Therefore, the overall ROC is $|z| > 1$.
Now, combine the fractions over a common denominator:
$$X(z) = \frac{1}{2} \left[ \frac{(1 - e^{-j\omega_0}z^{-1}) + (1 - e^{j\omega_0}z^{-1})}{(1 - e^{j\omega_0}z^{-1})(1 - e^{-j\omega_0}z^{-1})} \right]$$
Expand the numerator: $2 - (e^{j\omega_0} + e^{-j\omega_0})z^{-1}$
Expand the denominator: $1 - e^{-j\omega_0}z^{-1} - e^{j\omega_0}z^{-1} + e^{j\omega_0}e^{-j\omega_0}z^{-2} = 1 - (e^{j\omega_0} + e^{-j\omega_0})z^{-1} + z^{-2}$
Substitute Euler's inverse identity: $e^{j\omega_0} + e^{-j\omega_0} = 2\cos(\omega_0)$:
$$X(z) = \frac{1}{2} \left[ \frac{2 - 2\cos(\omega_0)z^{-1}}{1 - 2\cos(\omega_0)z^{-1} + z^{-2}} \right]$$
Cancel the factor of 2:
$$X(z) = \frac{1 - \cos(\omega_0)z^{-1}}{1 - 2\cos(\omega_0)z^{-1} + z^{-2}}$$
ROC: $|z| > 1$.

**7. Sine Sequence: $\sin(\omega_0 n) u[n]$**
Using Euler's identity: $\sin(\omega_0 n) = \frac{e^{j\omega_0 n} - e^{-j\omega_0 n}}{2j}$
Follow identical algebraic steps to the cosine derivation:
$$X(z) = \frac{1}{2j} \left[ \frac{(1 - e^{-j\omega_0}z^{-1}) - (1 - e^{j\omega_0}z^{-1})}{(1 - e^{j\omega_0}z^{-1})(1 - e^{-j\omega_0}z^{-1})} \right]$$
Numerator: $e^{j\omega_0}z^{-1} - e^{-j\omega_0}z^{-1} = z^{-1}(e^{j\omega_0} - e^{-j\omega_0}) = z^{-1}(2j\sin(\omega_0))$
Cancel the $2j$:
$$X(z) = \frac{\sin(\omega_0)z^{-1}}{1 - 2\cos(\omega_0)z^{-1} + z^{-2}}$$
ROC: $|z| > 1$.

### 4.4 ALL Z-Transform Properties (With Proofs)

**1. Linearity**
If $x_1[n] \leftrightarrow X_1(z)$ with ROC $R_1$, and $x_2[n] \leftrightarrow X_2(z)$ with ROC $R_2$:
$$a x_1[n] + b x_2[n] \leftrightarrow a X_1(z) + b X_2(z)$$
ROC contains the intersection $R_1 \cap R_2$.
*Proof:* Trivial by substituting into the sum definition. The sum of two converging series converges in the region where both individual series converge.

**2. Time Shift**
$$x[n - k] \leftrightarrow z^{-k} X(z)$$
ROC is $R_x$ (except possibly $z=0$ if $k>0$, or $z=\infty$ if $k<0$).
*Proof:* See Section 5 for full rigorous derivation.

**3. Z-Domain Scaling (Multiplication by an exponential sequence)**
$$a^n x[n] \leftrightarrow X\left(\frac{z}{a}\right)$$
ROC is $|a|R_x$.
*Proof:*
$$Z\{a^n x[n]\} = \sum_{n=-\infty}^{\infty} a^n x[n] z^{-n} = \sum_{n=-\infty}^{\infty} x[n] (a^{-1}z)^{-n}$$
By definition, the right side is simply the Z-transform evaluated at $a^{-1}z$:
$$= X(a^{-1}z) = X\left(\frac{z}{a}\right)$$
If the original ROC was defined by $r_1 < |z| < r_2$, the new ROC requires substituting $z$ with $z/a$:
$r_1 < \left|\frac{z}{a}\right| < r_2 \implies |a|r_1 < |z| < |a|r_2$. The ROC is scaled by the magnitude of $a$.

**4. Time Reversal**
$$x[-n] \leftrightarrow X(z^{-1})$$
ROC is $1/R_x$.
*Proof:*
$$Z\{x[-n]\} = \sum_{n=-\infty}^{\infty} x[-n] z^{-n}$$
Introduce a change of variables: Let $m = -n$. As $n$ ranges from $-\infty$ to $\infty$, $m$ ranges from $\infty$ to $-\infty$.
$$\sum_{m=-\infty}^{\infty} x[m] z^{m} = \sum_{m=-\infty}^{\infty} x[m] (z^{-1})^{-m} = X(z^{-1})$$
If the original ROC was $r_1 < |z| < r_2$, the new ROC requires $r_1 < |z^{-1}| < r_2$, which inverts to $\frac{1}{r_2} < |z| < \frac{1}{r_1}$. An outward ROC becomes an inward ROC.

**5. Conjugation**
$$x^*[n] \leftrightarrow X^*(z^*)$$
ROC is identically $R_x$.
*Proof:*
$$Z\{x^*[n]\} = \sum_{n=-\infty}^{\infty} x^*[n] z^{-n}$$
Take the complex conjugate of the entire expression, compensating by conjugating the inside terms:
$$= \left[ \sum_{n=-\infty}^{\infty} \left( x^*[n] z^{-n} \right)^* \right]^* = \left[ \sum_{n=-\infty}^{\infty} x[n] (z^*)^{-n} \right]^* = X^*(z^*)$$

**6. Differentiation in Z-Domain (Multiplication by n)**
$$n x[n] \leftrightarrow -z \frac{dX(z)}{dz}$$
ROC is exactly $R_x$.
*Proof:*
Start with the definition:
$$X(z) = \sum_{n=-\infty}^{\infty} x[n] z^{-n}$$
Differentiate both sides with respect to the complex variable $z$:
$$\frac{dX(z)}{dz} = \sum_{n=-\infty}^{\infty} x[n] \frac{d}{dz}(z^{-n}) = \sum_{n=-\infty}^{\infty} x[n] (-n) z^{-n-1}$$
Factor out a $-z^{-1}$ from the summation:
$$\frac{dX(z)}{dz} = -z^{-1} \sum_{n=-\infty}^{\infty} (n x[n]) z^{-n}$$
Multiply both sides by $-z$ to isolate the summation:
$$-z \frac{dX(z)}{dz} = \sum_{n=-\infty}^{\infty} (n x[n]) z^{-n}$$
By definition, the right side is the Z-transform of $n x[n]$. Thus:
$$Z\{n x[n]\} = -z \frac{dX(z)}{dz}$$

*Application to pair #5:*
Find $Z\{n a^n u[n]\}$. Let $x[n] = a^n u[n] \leftrightarrow X(z) = \frac{1}{1 - a z^{-1}}$.
$$Z\{n a^n u[n]\} = -z \frac{d}{dz} (1 - a z^{-1})^{-1}$$
Use the chain rule for derivatives:
$$= -z \left[ -1 (1 - a z^{-1})^{-2} \cdot \frac{d}{dz}(1 - a z^{-1}) \right]$$
$$= -z \left[ -1 (1 - a z^{-1})^{-2} \cdot (a z^{-2}) \right]$$
$$= -z \left[ -a z^{-2} (1 - a z^{-1})^{-2} \right]$$
$$= \frac{a z^{-1}}{(1 - a z^{-1})^2}$$
Multiply numerator and denominator by $z^2$:
$$= \frac{a z}{(z-a)^2}$$
ROC remains $|z| > |a|$.

**7. Convolution Theorem**
$$x_1[n] * x_2[n] \leftrightarrow X_1(z) X_2(z)$$
ROC contains the intersection $R_1 \cap R_2$.
*Proof:* See Section 5 for exhaustive proof.

**8. Initial Value Theorem**
If $x[n]$ is strictly causal ($x[n] = 0$ for $n < 0$), then $x[0] = \lim_{z \to \infty} X(z)$.
*Proof:* See Section 5.

**9. Final Value Theorem**
If $x[n]$ is causal ($x[n] = 0$ for $n < 0$) and all the poles of $(z-1)X(z)$ lie strictly inside the unit circle, then:
$$\lim_{n \to \infty} x[n] = \lim_{z \to 1} (z-1) X(z)$$
*Conditions explained:* The sequence $x[n]$ must settle to a constant, steady-state DC value. If it oscillates indefinitely (poles on the unit circle) or grows without bound (poles outside), the limit does not mathematically exist. The mathematical condition $(z-1)X(z)$ ensures that any single pole at $z=1$ (which corresponds to a step-function steady state) is canceled out, leaving only poles inside the unit circle, which represent decaying transients that vanish as $n \to \infty$.

### 4.5 Rational Z-Transforms and Pole-Zero Representation
In almost all practical DSP applications, discrete sequences have Z-transforms that can be expressed as rational functions (ratios of polynomials):
$$X(z) = \frac{B(z)}{A(z)} = \frac{b_0 + b_1 z^{-1} + b_2 z^{-2} + \dots + b_M z^{-M}}{a_0 + a_1 z^{-1} + a_2 z^{-2} + \dots + a_N z^{-N}}$$
- Multiply top and bottom by $z^{\max(M,N)}$ to express in positive powers of $z$, which makes finding roots easier.
- The roots of the numerator polynomial $B(z) = 0$ are the **zeros** of the system.
- The roots of the denominator polynomial $A(z) = 0$ are the **poles** of the system.
- **System Order:** The maximum of integers $M$ and $N$.
- **All-pole system (Autoregressive):** $B(z)$ is a simple constant. These model resonant systems and Infinite Impulse Response (IIR) filters.
- **All-zero system (Moving Average):** $A(z)$ is a simple constant. These represent finite-duration sequences and Finite Impulse Response (FIR) filters. FIR filters are always inherently stable because they have no poles (except trivially at $z=0$).

### 4.6 Strict Relationship Between ROC and Signal Type
Summarize this clearly on the board, as it is the most vital conceptual takeaway:
- **Causal Signal:** The ROC is the mathematical exterior of a circle, extending to complex infinity. It inherently includes the point $z=\infty$.
- **Anti-causal Signal:** The ROC is the mathematical interior of a circle, extending down to zero. It inherently includes the point $z=0$.
- **Two-sided Signal:** The ROC is an annular ring bounded by poles on both the inner and outer circumferences.
- **Stable System (BIBO):** For bounded-input bounded-output (BIBO) stability, the system's impulse response $h[n]$ must be absolutely summable ($\sum |h[n]| < \infty$). This is the exact mathematical definition of the DTFT existing! Therefore, stability mathematically implies that the ROC must include the unit circle ($|z|=1$).
- **Stable AND Causal System:** If a system is causal, its ROC is $|z| > r_{max}$. For it to also be simultaneously stable, the unit circle must be inside the ROC. This means the boundary $r_{max}$ must be strictly less than 1 ($1 > r_{max}$). Therefore, **all poles must lie strictly inside the unit circle.** A pole exactly on the unit circle causes marginal stability (sustained oscillations).

---
## 5. COMPLETE PROOFS AND DERIVATIONS

### Proof 1: Time Shift Property and ROC Change Analysis
**Theorem:** $Z\{x[n - k]\} = z^{-k} X(z)$.
**Rigorous Proof:**
Start with the fundamental definition of the Z-transform applied to the shifted sequence:
$$Y(z) = Z\{x[n - k]\} = \sum_{n=-\infty}^{\infty} x[n - k] z^{-n}$$
Introduce a change of index variables. Let $m = n - k$. This implies $n = m + k$.
Determine the new limits of summation: When $n \to -\infty$, $m \to -\infty$. When $n \to \infty$, $m \to \infty$.
Substitute the new variable into the summation:
$$Y(z) = \sum_{m=-\infty}^{\infty} x[m] z^{-(m + k)}$$
Use exponential algebra to split the $z$ term:
$$Y(z) = \sum_{m=-\infty}^{\infty} x[m] z^{-m} z^{-k}$$
Since the factor $z^{-k}$ is entirely independent of the summation index $m$, it can be factored out of the infinite sum:
$$Y(z) = z^{-k} \left( \sum_{m=-\infty}^{\infty} x[m] z^{-m} \right)$$
Recognize that the term inside the parentheses is the exact definition of $X(z)$:
$$Y(z) = z^{-k} X(z)$$

**ROC Change Analysis:**
The absolute convergence of the shifted series depends on $\sum |x[m] z^{-m}| < \infty$, which is exactly the exact same condition required for the original $X(z)$ to converge. Thus, the core ROC remains identical to $R_x$.
However, the multiplicative $z^{-k}$ term introduces a new potential singularity:
- If $k > 0$ (a time delay), $z^{-k} = 1/z^k$. If evaluated at $z=0$, this term becomes $1/0 \to \infty$, which is undefined. Thus, the specific point $z=0$ must be explicitly excluded from the new ROC.
- If $k < 0$ (a time advance), let $k = -p$ where $p>0$. Then $z^{-k} = z^p$. If evaluated as $z \to \infty$, this term diverges to infinity. Thus, the specific point $z=\infty$ must be explicitly excluded from the new ROC.

### Proof 2: Convolution Theorem
**Theorem:** $Z\{x_1[n] * x_2[n]\} = X_1(z) X_2(z)$.
**Rigorous Proof:**
Let the convolution output be $y[n] = x_1[n] * x_2[n]$. By the definition of discrete convolution:
$$y[n] = \sum_{k=-\infty}^{\infty} x_1[k] x_2[n - k]$$
Take the bilateral Z-transform of $y[n]$:
$$Y(z) = \sum_{n=-\infty}^{\infty} y[n] z^{-n} = \sum_{n=-\infty}^{\infty} \left[ \sum_{k=-\infty}^{\infty} x_1[k] x_2[n - k] \right] z^{-n}$$
Assuming absolute convergence within the common ROC intersection, we are mathematically permitted to interchange the order of the infinite summations (Fubini's Theorem):
$$Y(z) = \sum_{k=-\infty}^{\infty} \sum_{n=-\infty}^{\infty} x_1[k] x_2[n - k] z^{-n}$$
Group the terms depending on $n$:
$$Y(z) = \sum_{k=-\infty}^{\infty} x_1[k] \left[ \sum_{n=-\infty}^{\infty} x_2[n - k] z^{-n} \right]$$
The bracketed inner sum is exactly the Z-transform of the shifted sequence $x_2[n-k]$. Applying the time shift property proven above, this equals $z^{-k} X_2(z)$:
$$Y(z) = \sum_{k=-\infty}^{\infty} x_1[k] \left[ z^{-k} X_2(z) \right]$$
Since $X_2(z)$ is independent of the summation index $k$, pull it out of the summation:
$$Y(z) = X_2(z) \left[ \sum_{k=-\infty}^{\infty} x_1[k] z^{-k} \right]$$
The remaining summation is exactly the definition of $X_1(z)$:
$$Y(z) = X_2(z) X_1(z) = X_1(z) X_2(z)$$
The overall ROC must be at least the intersection $R_1 \cap R_2$. It can occasionally be larger if a pole of one function is exactly algebraically canceled by a zero of the other function.

### Proof 3: Initial Value Theorem
**Theorem:** For a strictly causal sequence where $x[n]=0$ for $n<0$, the initial value is $x[0] = \lim_{z \to \infty} X(z)$.
**Rigorous Proof:**
Expand the definition of the Z-transform explicitly for a causal sequence, starting from $n=0$:
$$X(z) = \sum_{n=0}^{\infty} x[n] z^{-n} = x[0] z^0 + x[1]z^{-1} + x[2]z^{-2} + x[3]z^{-3} + \dots$$
$$X(z) = x[0] + \frac{x[1]}{z} + \frac{x[2]}{z^2} + \frac{x[3]}{z^3} + \dots$$
Take the limit of both sides as the magnitude of $z$ approaches infinity:
$$\lim_{z \to \infty} X(z) = \lim_{z \to \infty} \left( x[0] + \frac{x[1]}{z} + \frac{x[2]}{z^2} + \frac{x[3]}{z^3} + \dots \right)$$
Since $x[n]$ are finite values, and $z$ is in the denominator of every term for $n \ge 1$, all terms from $n=1$ to infinity evaluate to $\frac{\text{finite}}{\infty} = 0$.
The only term that does not depend on $z$ is $x[0]$.
Therefore:
$$\lim_{z \to \infty} X(z) = x[0] + 0 + 0 + 0 \dots = x[0]$$

---
## 6. WORKED EXAMPLES (MINIMUM 5)

### Example 1: Sum of Two Right-Sided Sequences (Linearity and ROC Intersection)
**Problem statement:** Find the Z-transform, identify the poles, and explicitly state the ROC of the composite sequence $x[n] = (0.5)^n u[n] + (-0.3)^n u[n]$. Discuss the stability.
**Step-by-Step Solution:**
1. We recognize this as a linear combination of two right-sided exponential sequences. We use the standard derived pair $a^n u[n] \leftrightarrow \frac{z}{z-a}$ with ROC $|z| > |a|$.
2. Analyze the first term: $x_1[n] = (0.5)^n u[n]$
   $$X_1(z) = \frac{1}{1 - 0.5z^{-1}} = \frac{z}{z - 0.5}, \quad \text{ROC}_1: |z| > 0.5$$
3. Analyze the second term: $x_2[n] = (-0.3)^n u[n]$
   $$X_2(z) = \frac{1}{1 - (-0.3)z^{-1}} = \frac{z}{z + 0.3}, \quad \text{ROC}_2: |z| > |-0.3| \implies |z| > 0.3$$
4. Apply the linearity property: $X(z) = X_1(z) + X_2(z)$:
   $$X(z) = \frac{z}{z - 0.5} + \frac{z}{z + 0.3}$$
   Find a common denominator to express it as a single rational function:
   $$X(z) = \frac{z(z + 0.3) + z(z - 0.5)}{(z - 0.5)(z + 0.3)} = \frac{z^2 + 0.3z + z^2 - 0.5z}{z^2 - 0.5z + 0.3z - 0.15} = \frac{2z^2 - 0.2z}{z^2 - 0.2z - 0.15}$$
   Factor out $z$ in numerator: $X(z) = \frac{z(2z - 0.2)}{(z-0.5)(z+0.3)}$
5. Identify poles and zeros:
   Zeros (numerator roots): $z=0$ and $2z - 0.2 = 0 \implies z=0.1$.
   Poles (denominator roots): $z=0.5$ and $z=-0.3$.
6. Determine the composite ROC: The overall ROC must be the mathematical intersection of $\text{ROC}_1$ and $\text{ROC}_2$.
   We need the region where BOTH $|z| > 0.5$ AND $|z| > 0.3$ are simultaneously true.
   The more restrictive condition is $|z| > 0.5$. Therefore, the intersection is $|z| > 0.5$.
**Physical interpretation:** Since the ROC is $|z| > 0.5$, the region extends outwards to infinity, confirming it is a causal sequence. Furthermore, the region $|z| > 0.5$ physically encompasses the unit circle ($|z|=1$). Therefore, if this represented a system's impulse response, the system would be strictly BIBO stable.
**Common mistakes to avoid:** Students often mistakenly state the ROC is $|z| > 0.3$ because visually it represents a "larger" area on the plane. Emphasize that intersection means satisfying ALL constraints. If $|z| = 0.4$, $X_2(z)$ converges but $X_1(z)$ blows up to infinity, meaning the sum blows up.

### Example 2: The Non-Existent Z-Transform
**Problem statement:** Determine $X(z)$ and its ROC for the two-sided sequence $x[n] = (0.5)^n u[n] - (0.5)^n u[-n-1]$.
**Step-by-Step Solution:**
1. Break the sequence into its right-sided and left-sided components.
2. First component (right-sided): $x_1[n] = (0.5)^n u[n]$
   Using the standard pair:
   $$X_1(z) = \frac{z}{z - 0.5}, \quad \text{ROC}_1: |z| > 0.5$$
3. Second component (left-sided): $x_2[n] = -(0.5)^n u[-n-1]$
   Recall the left-sided standard pair derived earlier: $-a^n u[-n-1] \leftrightarrow \frac{z}{z-a}$ with ROC $|z| < |a|$.
   Here $a = 0.5$:
   $$X_2(z) = \frac{z}{z - 0.5}, \quad \text{ROC}_2: |z| < 0.5$$
4. Determine the composite ROC by finding the intersection of $\text{ROC}_1$ and $\text{ROC}_2$.
   We are looking for a complex number $z$ such that its magnitude $|z|$ is STRICTLY GREATER than $0.5$ AND STRICTLY LESS than $0.5$ simultaneously.
   Mathematically, there is no number that satisfies $|z| > 0.5$ and $|z| < 0.5$. The intersection is the empty set ($\emptyset$).
5. **Conclusion:** Because the ROC is empty, the infinite series does not converge anywhere in the complex plane. Therefore, the Z-transform for this specific sequence DOES NOT EXIST.
**Physical interpretation:** Look at the time-domain signal. As $n \to \infty$, $(0.5)^n$ decays to 0 nicely. But for negative $n$, consider $n = -100$. The term is $-(0.5)^{-100} = -2^{100}$, an astronomically large number. The sequence grows exponentially as time goes backwards to $-\infty$. There is no single exponential weighting factor $r^{-n}$ that can suppress the growth in both directions simultaneously.
**Common mistakes to avoid:** Blindly algebraically adding the expressions to get $X_1(z) + X_2(z) = \frac{2z}{z-0.5}$ without checking the ROC intersection. Always check the ROC intersection before doing any algebra!

### Example 3: Inverse Problem - Determining Sequence Type from ROC
**Problem statement:** An LTI system is described by the transfer function $H(z) = \frac{1}{1 - 1.5z^{-1} + 0.5z^{-2}}$. Determine the poles of the system. Then, define the possible ROCs and state whether the corresponding impulse response $h[n]$ is causal, anticausal, or two-sided, and whether the system is stable in each scenario.
**Step-by-Step Solution:**
1. Express $H(z)$ in positive powers of $z$ by multiplying numerator and denominator by $z^2$:
   $$H(z) = \frac{z^2}{z^2 - 1.5z + 0.5}$$
2. Factor the denominator polynomial to find the poles. We need two numbers that multiply to $0.5$ and add to $-1.5$. These are $-1$ and $-0.5$.
   Denominator: $(z - 1)(z - 0.5)$
   Poles are located at $z_1 = 1$ and $z_2 = 0.5$.
3. The complex $z$-plane is divided into three distinct possible regions separated by circular boundaries at the pole magnitudes $|z|=0.5$ and $|z|=1$.
   The three possible ROCs are:
   - Region A: The exterior region, $|z| > 1$
   - Region B: The annular region, $0.5 < |z| < 1$
   - Region C: The interior region, $|z| < 0.5$
4. Analyze each ROC scenario:
   **(a) Scenario 1: ROC is $|z| > 1$.**
   - Signal type: Because the ROC is outside the outermost pole, the sequence $h[n]$ is strictly **causal** (right-sided).
   - Stability: The ROC is $|z| > 1$. Does this region include the unit circle $|z|=1$? No, the unit circle is the boundary, but it is not *inside* the region. Therefore, the system is **unstable** (technically, marginally stable, which will oscillate indefinitely).
   **(b) Scenario 2: ROC is $0.5 < |z| < 1$.**
   - Signal type: Because the ROC is bounded between two poles, the sequence $h[n]$ must be **two-sided** (non-causal). It extends to both $+\infty$ and $-\infty$.
   - Stability: Does this annular ring include $|z|=1$? No. Therefore, the system is **unstable**.
   **(c) Scenario 3: ROC is $|z| < 0.5$.**
   - Signal type: Because the ROC is inside the innermost pole, extending to zero, the sequence $h[n]$ is **anticausal** (left-sided).
   - Stability: Does $|z| < 0.5$ include $|z|=1$? No. Therefore, the system is **unstable**.
**Physical interpretation:** The physical locations of the poles strictly dictate the possible convergence regions. Because one pole is exactly on the unit circle ($z=1$), it is physically impossible to define an ROC that completely encompasses the unit circle without intersecting a pole. Therefore, this specific transfer function cannot represent a strictly stable system under any circumstances.

### Example 4: Repeated Differentiation Property Application
**Problem statement:** Find the bilateral Z-transform of the sequence $x[n] = n^2 a^n u[n]$.
**Step-by-Step Solution:**
1. We cannot solve this directly with a basic table pair. We must build it up using properties.
   Start with the foundational known pair: Let $x_0[n] = a^n u[n]$. 
   $$X_0(z) = \frac{1}{1 - a z^{-1}}, \quad \text{ROC}: |z| > |a|$$
2. Define an intermediate sequence $x_1[n] = n \cdot a^n u[n]$.
   Apply the differentiation property: $Z\{n x_0[n]\} = -z \frac{dX_0(z)}{dz}$
   $$X_1(z) = -z \frac{d}{dz} (1 - a z^{-1})^{-1} = -z \left[ -1(1 - a z^{-1})^{-2}(a z^{-2}) \right] = \frac{a z^{-1}}{(1 - a z^{-1})^2}$$
   ROC remains $|z| > |a|$.
3. Now, recognize that the target sequence is $x[n] = n^2 a^n u[n] = n \cdot (n a^n u[n]) = n \cdot x_1[n]$.
   Apply the differentiation property a SECOND time:
   $$X(z) = -z \frac{dX_1(z)}{dz}$$
4. We must compute the derivative of $X_1(z) = a z^{-1} (1 - a z^{-1})^{-2}$.
   Use the product rule: $\frac{d}{dz}(uv) = u'v + uv'$. Let $u = a z^{-1}$ and $v = (1 - a z^{-1})^{-2}$.
   $u' = -a z^{-2}$
   $v' = -2(1 - a z^{-1})^{-3}(a z^{-2}) = -2a z^{-2} (1 - a z^{-1})^{-3}$
   $$\frac{dX_1(z)}{dz} = \left[ -a z^{-2} \right] (1 - a z^{-1})^{-2} + \left[ a z^{-1} \right] \left[ -2a z^{-2} (1 - a z^{-1})^{-3} \right]$$
   $$\frac{dX_1(z)}{dz} = \frac{-a z^{-2}}{(1 - a z^{-1})^2} - \frac{2a^2 z^{-3}}{(1 - a z^{-1})^3}$$
5. Substitute this back into the property equation:
   $$X(z) = -z \left[ \frac{-a z^{-2}}{(1 - a z^{-1})^2} - \frac{2a^2 z^{-3}}{(1 - a z^{-1})^3} \right]$$
   Distribute the $-z$:
   $$X(z) = \frac{a z^{-1}}{(1 - a z^{-1})^2} + \frac{2a^2 z^{-2}}{(1 - a z^{-1})^3}$$
6. To simplify, get a common denominator of $(1 - a z^{-1})^3$. Multiply the first term by $\frac{1 - a z^{-1}}{1 - a z^{-1}}$:
   $$X(z) = \frac{a z^{-1}(1 - a z^{-1})}{(1 - a z^{-1})^3} + \frac{2a^2 z^{-2}}{(1 - a z^{-1})^3} = \frac{a z^{-1} - a^2 z^{-2} + 2a^2 z^{-2}}{(1 - a z^{-1})^3}$$
   $$X(z) = \frac{a z^{-1} + a^2 z^{-2}}{(1 - a z^{-1})^3}$$
   Multiply numerator and denominator by $z^3$ for positive powers:
   $$X(z) = \frac{a z^2 + a^2 z}{(z - a)^3}$$
   ROC remains $|z| > |a|$.
**Physical interpretation:** Multiplying by $n$ in the time domain corresponds to increasing the multiplicity (order) of the poles in the Z-domain. A single pole $(z-a)^1$ gives an exponential. A double pole $(z-a)^2$ leads to linear growth $n a^n$. A triple pole $(z-a)^3$ leads to quadratic growth $n^2 a^n$.

### Example 5: Final Value Theorem Application
**Problem statement:** An engineering system's output is characterized by $X(z) = \frac{z^2 - 0.5z}{z^2 - 1.8z + 0.8}$. Apply the final value theorem to find the steady-state value $x[\infty]$. Rigorously verify if the theorem's mathematical conditions are met first.
**Step-by-Step Solution:**
1. **Factor the expression:**
   Numerator: $z(z - 0.5)$
   Denominator: Need roots that multiply to $0.8$ and add to $-1.8$. Roots are $-1$ and $-0.8$.
   So, $X(z) = \frac{z(z - 0.5)}{(z - 1)(z - 0.8)}$.
2. **Check Conditions:** The Final Value Theorem requires that $x[n]$ is causal (we assume this is a causal system output) and that ALL poles of the modified function $(z-1)X(z)$ lie STRICTLY inside the unit circle.
   Calculate the modified function:
   $$(z-1)X(z) = (z-1) \frac{z(z - 0.5)}{(z - 1)(z - 0.8)} = \frac{z(z - 0.5)}{z - 0.8}$$
   Identify the poles of this new expression. The only pole is located at $z = 0.8$.
   Check magnitude: $|0.8| < 1$. The pole lies strictly inside the unit circle.
   Therefore, the conditions are satisfied, and the limit will converge to a finite value!
3. **Apply Theorem:**
   $$x[\infty] = \lim_{z \to 1} (z-1)X(z) = \lim_{z \to 1} \frac{z(z - 0.5)}{z - 0.8}$$
   Substitute $z=1$ directly into the expression:
   $$x[\infty] = \frac{1(1 - 0.5)}{1 - 0.8} = \frac{0.5}{0.2} = 2.5$$
**Physical interpretation:** The presence of the pole exactly at $z=1$ in the original $X(z)$ implies the system contains an ideal integrator or that a step input was applied. This forces the system output to settle to a non-zero DC constant. The pole at $z=0.8$ represents a transient response that decays exponentially as $(0.8)^n$. The final value theorem elegantly extracts the steady-state DC value of $2.5$ bypassing the need to perform a complete, tedious partial fraction expansion to find the exact time-domain equation.

---
## 7. ENGINEERING APPLICATIONS AND CASE STUDIES

**Application 1: System Stability Analysis in Digital Motor Control**
In modern electric vehicles, the traction inverter uses a digital microcontroller to run Field Oriented Control (FOC) algorithms. The closed-loop transfer function $H(z)$ of the motor speed controller relies on accurate PI (Proportional-Integral) tuning. 
By calculating the poles of the overall $H(z)$, control engineers verify stability. If a poorly tuned PI gain causes any pole to wander outside the unit circle (e.g., $z = 1.05$), the mathematical model predicts an unstable, exponentially growing sequence. In physical reality, this means the motor speed will oscillate violently until the inverter saturates or a mechanical component shears. 
*Real-world parameters:* For a BLDC motor sampled at $T_s = 100 \mu s$, a closed-loop pole at $z = 1.02$ indicates an unstable growing exponential with a very fast time constant, causing catastrophic failure within milliseconds. Engineers use the Z-plane to graphically ensure all poles remain safely inside a radius of $r=0.9$ to guarantee robustness against temperature variations in the silicon.

**Application 2: IIR Filter Design in Digital Audio Equalization**
High-fidelity digital audio equalizers utilize Infinite Impulse Response (IIR) filters, which are defined purely by rational Z-transforms. To boost bass frequencies without affecting treble, engineers place poles near the unit circle at low frequencies (angles near $0$ in the complex z-plane).
*Real-world parameters:* To create a resonant bass-boost filter centered at 100 Hz for CD-quality audio ($f_s = 44.1$ kHz), the pole angle is calculated as $\theta = 2\pi(f/f_s) = 2\pi(100/44100) \approx 0.0142$ radians. To ensure stability and prevent the audio from endlessly "ringing" (self-oscillation), the pole radius must be strictly less than 1. A typical choice is $r = 0.99$. The poles would be located at $z = 0.99 e^{\pm j 0.0142}$.

**Application 3: Radar Signal Processing and Clutter Rejection**
In pulsed Doppler radar systems (used in air traffic control), ground clutter (reflections from stationary buildings or mountains) creates a massive DC component in the received signal, masking small moving aircraft. 
Engineers design a digital Moving Target Indicator (MTI) filter. The simplest MTI filter is a two-pulse canceler, represented by the difference equation $y[n] = x[n] - x[n-1]$. Taking the Z-transform yields $H(z) = 1 - z^{-1} = \frac{z-1}{z}$. 
This system has a zero at exactly $z=1$ (DC frequency). The zero completely annihilates the stationary clutter while allowing the Doppler-shifted frequencies of moving aircraft to pass through.

---
## 8. COMMON STUDENT MISCONCEPTIONS AND ERRORS

1. **Misconception:** "The ROC is just the boundary circle itself."
   *Correction:* The ROC is a 2D geometric area (a region) on the complex plane. It is defined by strict inequalities like $|z| > r$, which represents the entire infinite area outside a circle, not merely the circumference of the circle.
2. **Misconception:** "If two functions have the exact same algebraic rational expression for $X(z)$, they must automatically correspond to the identical time-domain signal $x[n]$."
   *Correction:* $X(z)$ without an explicitly stated ROC is fundamentally incomplete! As proven in Section 4.3, the expression $\frac{z}{z-0.5}$ corresponds to $(0.5)^n u[n]$ (if the ROC is $|z|>0.5$) OR it corresponds to $-(0.5)^n u[-n-1]$ (if the ROC is $|z|<0.5$).
3. **Misconception:** "The unit circle defines stability, therefore to be stable, the poles must be located ON the unit circle."
   *Correction:* Poles located exactly on the unit circle result in a marginally stable system, which behaves as an oscillator (like a sine wave). For absolute BIBO stability (where transients eventually die out), poles must be strictly, unequivocally INSIDE the unit circle ($|p_i| < 1$).
4. **Misconception:** "The Z-transform is a universal mathematical tool and always exists for every sequence."
   *Correction:* The Z-transform only exists mathematically if there is a valid, non-empty ROC. As rigorously demonstrated in Example 2, some sequences (like $2^n u[n] + 3^{-n} u[-n-1]$) grow too rapidly in both the positive and negative directions, leaving no ROC at all.
5. **Misconception:** "Bilateral and unilateral Z-transforms are mathematically identical; the names just refer to different applications."
   *Correction:* The bilateral transform includes summation limits from $-\infty$ to $\infty$. The unilateral explicitly forces the summation limits from $0$ to $\infty$, effectively discarding any past data. This lecture focuses purely on the bilateral. The unilateral transform is a specialized variant used later primarily for solving difference equations with non-zero initial conditions.
6. **Error:** Confusing the time-advance and time-delay shift properties.
   *Correction:* Delaying a signal by $k$ samples (moving it right, into the future) multiplies the transform by $z^{-k}$. Advancing a signal by $k$ samples (moving it left) multiplies by $z^{+k}$. Students often invert these signs.
7. **Error:** Applying the Final Value Theorem without checking the pole locations first.
   *Correction:* If a system has poles outside the unit circle, the output grows to infinity. If you blindly apply the Final Value Theorem formula $\lim_{z \to 1}(z-1)X(z)$, you will calculate a finite, completely wrong mathematical number, completely missing the fact that the physical system has exploded.

---
## 9. CONNECTIONS TO OTHER LECTURES

**What this lecture builds upon:**
- *Lecture 3 (LTI Systems & Convolution):* The conceptual understanding of the impulse response $h[n]$ and discrete convolution directly leads to the algebraic $H(z) = Y(z)/X(z)$ transfer function relationship.
- *Lecture 4 (Discrete-Time Fourier Transform):* The Z-transform is presented as a natural, required mathematical extension of the DTFT, specifically formulated to overcome the DTFT's severe convergence limitations.

**What future lectures critically depend on this material:**
- *Lecture 6 (The Inverse Z-Transform):* Students must know pole locations and ROC definitions intimately to correctly perform partial fraction expansions and select the correct time-domain sequences.
- *Lecture 9 (IIR Digital Filter Design):* The entire methodology of placing poles and zeros in the complex Z-plane to physically shape the frequency response of a filter relies 100% on the theoretical foundations established today.

---
## 10. EXAMINATION QUESTIONS

### 10.1 Short Answer (10 questions)
**Q1.** State the precise mathematical relationship between the bilateral Z-transform and the DTFT.
*Model Answer:* The Z-transform evaluated exactly on the unit circle ($z = e^{j\omega}$) is identically the DTFT. Alternatively, the Z-transform is a generalized DTFT where the original sequence is multiplied by an exponential weighting factor $r^{-n}$.

**Q2.** State the specific ROC property that mathematically guarantees LTI system stability.
*Model Answer:* For a discrete-time LTI system to be Bounded-Input Bounded-Output (BIBO) stable, the ROC of its transfer function $H(z)$ must strictly include the unit circle ($|z|=1$).

**Q3.** Can a pole of $X(z)$ logically lie within the Region of Convergence? Explain why or why not.
*Model Answer:* No. A pole is defined as a complex value of $z$ where the function $X(z)$ diverges to infinity. The ROC is defined as the specific region where the infinite series converges to a finite value. Therefore, poles inherently form the boundaries of the ROC but can never exist inside it.

**Q4.** What is the Z-transform and ROC of a delayed unit impulse $\delta[n-3]$?
*Model Answer:* Using the time-shift property on $\delta[n] \leftrightarrow 1$, we get $X(z) = 1 \cdot z^{-3} = z^{-3}$. The ROC is the entire z-plane except $z=0$ (because $1/0^3$ is undefined).

**Q5.** If a rational transfer function $X(z)$ has poles at $z=2$ and $z=-3$, list all possible theoretically valid ROCs.
*Model Answer:* The poles have magnitudes 2 and 3. There are three possible regions bounded by these magnitudes: 
(1) $|z| > 3$ (exterior, causal signal)
(2) $2 < |z| < 3$ (annular, two-sided signal)
(3) $|z| < 2$ (interior, anticausal signal).

**Q6.** What is the ROC of the sum of two sequences with individual ROCs $R_1$ and $R_2$?
*Model Answer:* The ROC of the sum must at least contain the intersection of the two regions: $R_1 \cap R_2$.

**Q7.** Why are FIR filters inherently always stable?
*Model Answer:* FIR filters have finite-duration impulse responses. Their Z-transform is a polynomial in $z^{-1}$ (all-zero system). Therefore, they have no poles other than at $z=0$. Because there are no poles, the ROC extends to infinity and always includes the unit circle, guaranteeing stability.

**Q8.** A signal $x[n]$ is known to be left-sided (anti-causal). Its Z-transform has poles at $0.5$ and $0.8$. What is its ROC?
*Model Answer:* For a left-sided signal, the ROC must be the interior of a circle bounded by the innermost pole. The innermost pole is at $0.5$. Thus, the ROC is $|z| < 0.5$.

**Q9.** State the conditions under which the Final Value Theorem is valid.
*Model Answer:* The signal $x[n]$ must be causal ($x[n]=0$ for $n<0$), and all poles of the expression $(z-1)X(z)$ must lie strictly inside the unit circle ($|z|<1$).

**Q10.** How does time-reversing a signal affect its Z-transform poles?
*Model Answer:* By the time-reversal property $X(z^{-1})$, a pole originally at $z=p$ will move to $z=1/p$. Magnitudes invert, so poles inside the unit circle move outside, and vice versa.

### 10.2 Long Answer / Numerical Problems (8 problems)
*(Provide full solutions based on techniques in Section 6)*

**P1.** Find the Z-transform and ROC of $x[n] = 3^n u[n] - 4(0.2)^n u[n]$.
*Solution:* 
$X_1(z) = \frac{z}{z-3}$ with ROC $|z| > 3$.
$X_2(z) = \frac{4z}{z-0.2}$ with ROC $|z| > 0.2$.
$X(z) = \frac{z}{z-3} - \frac{4z}{z-0.2} = \frac{z(z-0.2) - 4z(z-3)}{(z-3)(z-0.2)} = \frac{z^2 - 0.2z - 4z^2 + 12z}{(z-3)(z-0.2)} = \frac{-3z^2 + 11.8z}{(z-3)(z-0.2)}$.
The composite ROC is the intersection: $|z| > 3$.

**P2.** Find the Z-transform of $x[n] = (1/3)^n u[-n-1]$. Determine if it is stable.
*Solution:* This is a left-sided exponential. Using the standard pair $-a^n u[-n-1] \leftrightarrow \frac{z}{z-a}$ with ROC $|z|<|a|$.
Here, the sign is positive, so $X(z) = -\frac{z}{z - 1/3}$.
The ROC is $|z| < 1/3$.
Since the ROC $|z| < 1/3$ does NOT include the unit circle ($|z|=1$), the sequence is unstable (it diverges as $n \to -\infty$).

**P3.** Prove the time reversal property $Z\{x[-n]\} = X(z^{-1})$ from the definition.
*Solution:* See rigorous proof in Section 4.4.

**P4.** Apply the Final Value theorem to $X(z) = \frac{3z^2 - 1.5z}{(z-1)(z-0.4)}$. Check conditions first.
*Solution:* 
Conditions check: Find poles of $(z-1)X(z) = \frac{3z^2 - 1.5z}{z-0.4}$. The only pole is at $z=0.4$. Since $|0.4|<1$, conditions are met.
Apply limit: $x[\infty] = \lim_{z \to 1} \frac{3(1)^2 - 1.5(1)}{1 - 0.4} = \frac{1.5}{0.6} = 2.5$.

**P5.** A system has impulse response $h[n] = \delta[n] - \delta[n-1]$. Find $H(z)$, its zeros, and sketch the pole-zero plot.
*Solution:*
$H(z) = 1 - z^{-1} = \frac{z-1}{z}$.
Zeros: $z=1$. Poles: $z=0$.
The plot has an 'o' at $(1,0)$ and an 'x' at $(0,0)$ on the complex plane. ROC is entire z-plane except $z=0$.

**P6.** Use the differentiation property to find the Z-transform of $x[n] = n \cdot 2^n u[n]$.
*Solution:*
Let $g[n] = 2^n u[n] \leftrightarrow G(z) = \frac{1}{1-2z^{-1}}$.
$X(z) = -z \frac{dG}{dz} = -z \left[ -(1-2z^{-1})^{-2} (2z^{-2}) \right] = \frac{2z^{-1}}{(1-2z^{-1})^2} = \frac{2z}{(z-2)^2}$.
ROC is $|z|>2$.

**P7.** Given $X(z) = \frac{1}{1-2z^{-1}}$ and $Y(z) = \frac{1}{1+3z^{-1}}$. If $w[n] = x[n]*y[n]$, find $W(z)$ and its possible ROCs.
*Solution:* By convolution property, $W(z) = X(z)Y(z) = \frac{1}{(1-2z^{-1})(1+3z^{-1})}$.
Poles at $z=2$ and $z=-3$.
Possible ROCs: $|z|>3$ (causal), $2<|z|<3$ (two-sided), $|z|<2$ (anticausal).

**P8.** An engineer claims a system with $H(z) = \frac{z}{z-1.5}$ is stable. Prove them wrong.
*Solution:* The pole is at $z=1.5$. If the system is causal, the ROC is $|z|>1.5$. This does not include the unit circle $|z|=1$, so it is unstable (it is a growing exponential $(1.5)^n u[n]$). If the system is anticausal, the ROC is $|z|<1.5$. This DOES include the unit circle, making it stable. However, a causal implementation is unstable.

### 10.3 True/False with Justification (10 items)
1. **T/F:** A finite duration sequence has an ROC that is always the entire mathematical z-plane, without exception.
   *False.* It may exclude $z=0$ or $z=\infty$ depending on if it has non-zero values at positive or negative time indices.
2. **T/F:** If $x[n]$ is a stable sequence, its poles must unconditionally be inside the unit circle.
   *False.* This is strictly true only if $x[n]$ is BOTH stable AND causal. If the signal is anti-causal, stable means the poles are strictly OUTSIDE the unit circle.
3. **T/F:** The transfer function $X(z) = \frac{z}{z-2}$ represents a stable system if it is known to be causal.
   *False.* If causal, the ROC is defined as $|z|>2$. This region does not include the unit circle $|z|=1$, therefore it represents an unstable growing sequence.
4. **T/F:** The ROC of a two-sided sequence physically forms an annular ring on the complex plane.
   *True.* It is mathematically the intersection of a right-sided outward-pointing ROC and a left-sided inward-pointing ROC.
5. **T/F:** Multiplying $x[n]$ by $n$ simply differentiates $X(z)$ with respect to $z$.
   *False.* According to the property, it differentiates $X(z)$ AND then multiplies the result by $-z$.
6. **T/F:** The Initial Value Theorem is only valid for causal signals.
   *True.* If the signal has non-zero values for $n<0$, there will be positive powers of $z$ in the expansion that will blow up to infinity as $z \to \infty$, rendering the limit undefined.
7. **T/F:** The Z-transform is a linear operator.
   *True.* The transform of a sum of signals is the sum of their individual transforms, provided the intersection of their ROCs is non-empty.
8. **T/F:** An FIR filter can have poles located at $z=0.5$.
   *False.* FIR filters (Finite Impulse Response) have transfer functions that are polynomials in $z^{-1}$. They only have poles at the origin $z=0$.
9. **T/F:** The Z-transform of $u[n]$ and $u[n-1]$ have the exact same ROC.
   *False.* $u[n]$ has ROC $|z|>1$. $u[n-1]$ has ROC $|z|>1$ AND $z \neq 0$. They differ at the origin.
10. **T/F:** If the ROC is $|z| < 0.9$, the system is stable.
    *False.* To be stable, the ROC must include the unit circle $|z|=1$. A radius of $0.9$ means the unit circle is excluded, thus it is unstable.

---
## 11. KEY FORMULAS REFERENCE

| Conceptual Domain | Formula / Property | ROC Restrictions |
| :--- | :--- | :--- |
| **Bilateral Z-Transform Definition** | $X(z) = \sum_{n=-\infty}^{\infty} x[n] z^{-n}$ | $\sum \|x[n] z^{-n}\| < \infty$ |
| **Unit Impulse Sequence** | $\delta[n] \leftrightarrow 1$ | All $z$ |
| **Unit Step Sequence** | $u[n] \leftrightarrow \frac{z}{z-1}$ | $\|z\| > 1$ |
| **Right-Sided Exponential** | $a^n u[n] \leftrightarrow \frac{z}{z-a}$ | $\|z\| > \|a\|$ |
| **Left-Sided Exponential** | $-a^n u[-n-1] \leftrightarrow \frac{z}{z-a}$ | $\|z\| < \|a\|$ |
| **Multiplication by time index n** | $n x[n] \leftrightarrow -z \frac{dX(z)}{dz}$ | Same as $X(z)$ |
| **Time Shift (Delay/Advance)** | $x[n-k] \leftrightarrow z^{-k} X(z)$ | Same (except 0, $\infty$) |
| **Convolution in Time Domain** | $x_1[n] * x_2[n] \leftrightarrow X_1(z) X_2(z)$ | At least $R_1 \cap R_2$ |
| **Z-Domain Scaling (Exponential)**| $a^n x[n] \leftrightarrow X\left(\frac{z}{a}\right)$ | Scaled ROC: $\|a\|R_x$ |
| **Initial Value Theorem** | $x[0] = \lim_{z \to \infty} X(z)$ | $x[n]$ must be strictly causal |
| **Final Value Theorem** | $x[\infty] = \lim_{z \to 1} (z-1)X(z)$ | Poles strictly inside $\|z\|=1$ |

---
## 12. FURTHER READING AND REFERENCES
- **Proakis, J. G., & Manolakis, D. G.** (2006). *Digital Signal Processing: Principles, Algorithms, and Applications* (4th Ed.). Chapter 3: The Z-Transform and Its Application to the Analysis of LTI Systems. (Excellent resource for engineering applications).
- **Oppenheim, A. V., & Schafer, R. W.** (2010). *Discrete-Time Signal Processing* (3rd Ed.). Chapter 3: The z-Transform. (The definitive, most mathematically rigorous text on the subject).
- **Haykin, S., & Van Veen, B.** (2002). *Signals and Systems* (2nd Ed.). Chapter 7: Discrete-Time LTI Systems and the Z-Transform. (Good for mapping continuous-time Laplace concepts to discrete Z-transform concepts).
</Faculty Notes — Lecture 5: Z-Transform & ROC>
