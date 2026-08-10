<Faculty Notes — Lecture 6: Inverse Z-Transform & System Analysis>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY

Welcome to Lecture 6 of the EE3621 Digital Signal Processing curriculum. This lecture covers the essential techniques for computing the inverse Z-transform and applying it to system analysis. This is a critical transitional lecture; it moves students from purely theoretical abstract mathematical spaces into practical, time-domain realization of discrete systems.

Three primary methods for computing the inverse Z-transform exist, and each has distinct strengths:
1. **Partial Fraction Expansion (PFE)** is the most common and practical method for rational transfer functions. It is the workhorse of DSP engineering. However, students frequently make algebraic errors (like dropping negative signs) or forget the crucial step of expanding $X(z)/z$ instead of $X(z)$.
2. **Power Series (Long Division)** is straightforward for finding the first few samples of a sequence. It is particularly useful for non-rational functions or when exact closed-form expressions are cumbersome. It reinforces the idea that the Z-transform is fundamentally a polynomial in $z^{-1}$.
3. **Contour Integration (Residue Theorem)** provides the formal definition and works for all cases, but requires a solid foundation in complex analysis. It is essential for advanced students who will pursue graduate studies in signal processing or communications.

Emphasize repeatedly throughout this lecture that the Region of Convergence (ROC) fundamentally determines the solution. The algebraic expression alone does not uniquely specify the time-domain sequence. Make sure to visually draw the ROC in the z-plane to clarify whether a pole corresponds to a causal, anti-causal, or two-sided sequence. Without this visual aid, students often memorize formulas without understanding the underlying geometric implications.

**Common Student Difficulties:**
- **Calculus rusty:** Many students will struggle with the partial fraction expansion of repeated poles because it requires taking derivatives of complex polynomials.
- **ROC confusion:** Students often think the ROC is a property of the equation, not the physical system. Emphasize that the ROC is a choice the engineer makes based on whether the system is causal or stable.
- **Algebra fatigue:** The sheer length of some PFE problems causes sign errors. Encourage step-by-step verification.

**Suggested Demos for the Classroom:**
- Use MATLAB's `residuez` and `impz` on the overhead projector. Show how changing the coefficients of the transfer function physically alters the impulse response in real-time.
- Plot pole locations dynamically and step through the unit circle for stability demonstrations. If possible, show a system "blowing up" (going unstable) when a pole crosses from 0.99 to 1.01.

---
## 1. LEARNING OBJECTIVES

By the end of this comprehensive lecture, students will be able to demonstrate mastery in the following areas:

1. **Apply** Partial Fraction Expansion (PFE) meticulously to compute the inverse Z-transform of rational expressions for systems containing distinct, repeated, and complex conjugate poles.
2. **Execute** polynomial long division systematically to find the early time-domain samples of a sequence for both causal (descending powers of $z$) and anti-causal (ascending powers of $z$) systems.
3. **Analyze** complex integrals using Cauchy's Residue Theorem to formally derive the inverse Z-transform from fundamental mathematical principles.
4. **Evaluate** the stability and causality of a discrete-time Linear Time-Invariant (LTI) system purely based on its pole locations relative to the unit circle in the complex z-plane.
5. **Formulate** and rigorously solve finite difference equations with non-zero initial conditions using the unilateral Z-transform and its shifting properties.
6. **Interpret** the profound connection between the mathematical ROC boundaries (circles in the complex plane) and the physical nature of signals (decaying, growing, causal, non-causal).
7. **Synthesize** multiple mathematical approaches to verify the correctness of an inverse Z-transform calculation (e.g., using long division to check the first few terms of a PFE result).
8. **Diagnose** common algebraic and conceptual errors in system stability analysis and correct them using rigorous mathematical justification.

---
## 2. PREREQUISITE KNOWLEDGE REVIEW

Before diving into the new material, spend the first 5-10 minutes reviewing these fundamental concepts. Do not assume students remember them perfectly from earlier courses.

### 2.1 Partial Fractions from Calculus
Students must remember how to decompose rational algebraic functions. This is arguably the most critical mechanical skill for this lecture.
Given a rational function $F(x) = \frac{N(x)}{D(x)}$, where the degree of the numerator $N(x)$ is strictly less than the degree of the denominator $D(x)$:

**Distinct Roots:**
If $D(x) = (x-a)(x-b)(x-c)$, then:
$$F(x) = \frac{A}{x-a} + \frac{B}{x-b} + \frac{C}{x-c}$$
where $A, B, C$ are constants found via the cover-up method or equating coefficients.

**Repeated Roots:**
If $D(x) = (x-a)^3$, then:
$$F(x) = \frac{A}{(x-a)} + \frac{B}{(x-a)^2} + \frac{C}{(x-a)^3}$$

**Irreducible Quadratic Roots:**
If $D(x) = (x-a)(x^2 + bx + c)$, then:
$$F(x) = \frac{A}{x-a} + \frac{Bx + C}{x^2 + bx + c}$$

### 2.2 Basic Z-Transform Pairs
The fundamental pairs heavily relied upon for synthesis must be memorized. Write these explicitly on the board:
- **Unit Impulse:** $\delta[n] \longleftrightarrow 1$, for all $z$.
- **Unit Step (Causal):** $u[n] \longleftrightarrow \frac{z}{z-1} = \frac{1}{1-z^{-1}}, \quad |z| > 1$.
- **Causal Exponential:** $a^n u[n] \longleftrightarrow \frac{z}{z-a} = \frac{1}{1-a z^{-1}}, \quad |z| > |a|$.
- **Anti-Causal Exponential:** $-a^n u[-n-1] \longleftrightarrow \frac{z}{z-a} = \frac{1}{1-a z^{-1}}, \quad |z| < |a|$.
- **Unit Ramp:** $n u[n] \longleftrightarrow \frac{z}{(z-1)^2}, \quad |z| > 1$.
- **Causal Scaled Ramp:** $n a^n u[n] \longleftrightarrow \frac{a z}{(z-a)^2}, \quad |z| > |a|$.

### 2.3 Poles and Zeros Definitions
- **Zeros:** The roots of the numerator polynomial $N(z)$. These are the values of $z$ for which $X(z) = 0$. They represent frequencies where the system completely attenuates the input.
- **Poles:** The roots of the denominator polynomial $D(z)$. These are the values of $z$ for which $X(z) \to \infty$. They dictate the fundamental modes (frequencies and decay rates) of the system's transient response.

### 2.4 Complex Algebra Review
- **Euler's Formula:** $e^{j\theta} = \cos\theta + j\sin\theta$.
- **Complex Conjugates:** If a polynomial has purely real coefficients, any complex roots MUST appear in conjugate pairs. If $p = \sigma + j\omega$ is a root, then $p^* = \sigma - j\omega$ is also a root.

---
## 3. HISTORICAL AND MOTIVATIONAL CONTEXT

The foundation of the inverse Z-transform traces back to pure complex analysis, specifically the Laurent series expansion and contour integration formalized by the prolific French mathematician Augustin-Louis Cauchy in the 19th century. 

In the realm of continuous-time systems, Pierre-Simon Laplace developed the Laplace transform as an operational calculus tool for solving linear ordinary differential equations. When engineers and physicists moved toward digital control, radar, and discrete-time signal processing in the mid-20th century (driven largely by the demands of WWII and the Cold War), they needed a discrete equivalent to the Laplace transform. The Z-transform emerged as this indispensable tool. Initially called the "generating function" in probability theory, it was adapted by engineers at MIT and Bell Labs into the robust framework we use today.

**Why does an Electrical and Electronics Engineering (EEE) student need this?**
1. **Digital Filter Design:** The transition from continuous analog filters (using bulky R, L, C circuits and operational amplifiers) to discrete digital filters (implemented in microprocessors, DSP chips, or FPGAs) requires mapping from the s-domain to the z-domain. The inverse Z-transform is what allows the engineer to reconstruct the filter's actual impulse response in the time domain, which is the exact sequence of code executed by the processor.
2. **Control Systems:** Modern digital PID controllers act on sampled errors rather than continuous voltages. Predicting the system response—such as determining if a robotic arm will overshoot its target or how long it will take to settle—requires solving complex difference equations. The inverse Z-transform is the primary mathematical engine for this.
3. **Stability Analysis:** Real-world systems can cause catastrophic failure if unstable (e.g., an aircraft autopilot entering uncontrolled oscillations). The Z-transform provides a purely algebraic, guaranteed way to verify system safety without explicitly simulating or solving for every time step.

---
## 4. THEORETICAL FOUNDATIONS

### 4.1 Inverse Z-transform via Contour Integration

The most mathematically rigorous and formal definition of the inverse Z-transform is given by a contour integral over a closed path in the complex plane. 

$$x[n] = \frac{1}{2\pi j} \oint_C X(z) z^{n-1} dz$$

where $C$ is a counterclockwise closed contour that lies entirely within the Region of Convergence (ROC) of $X(z)$ and completely encloses the origin of the z-plane.

#### Cauchy's Residue Theorem Application
According to Cauchy's Residue Theorem, an integral of a complex function over a closed contour equals $2\pi j$ times the sum of the residues of the enclosed singularities (poles).
$$ \oint_C F(z) dz = 2\pi j \sum \text{Residues of } F(z) \text{ inside } C $$
Applying this theorem to our inverse Z-transform definition, let the function be $F(z) = X(z) z^{n-1}$. The inverse Z-transform simplifies dramatically to:
$$ x[n] = \sum \left( \text{Residues of } X(z) z^{n-1} \text{ at poles inside } C \right) $$

#### The General Residue Formula
For any given pole $p_k$ of multiplicity (or order) $m$, the mathematical residue is calculated using the limit derivative formula:
$$ \text{Res}_{z = p_k} = \frac{1}{(m-1)!} \lim_{z \to p_k} \frac{d^{m-1}}{dz^{m-1}} \left[ (z - p_k)^m X(z) z^{n-1} \right] $$

For a simple pole (multiplicity $m=1$), the formula collapses to a simple limit without derivatives:
$$ \text{Res}_{z = p_k} = \lim_{z \to p_k} \left[ (z - p_k) X(z) z^{n-1} \right] $$

**When is this practical?** 
Contour integration is highly rigorous but is often too computationally cumbersome for everyday manual engineering calculations. It is primarily used in pure mathematics contexts, theoretical signal processing derivations, or when dealing with $X(z)$ functions that are non-rational (e.g., functions containing logarithms or exponentials in $z$). For rational functions, PFE is overwhelmingly preferred.

### 4.2 Partial Fraction Expansion (PFE) Method

Partial Fraction Expansion (PFE) is the universally applied, practical method used by engineers in the field. The core concept is to express a complex, high-order rational function $X(z)$ as a linear combination (a sum) of much simpler, first-order fractions. These simple fractions correspond directly to standard Z-transform pairs found in reference tables.

#### The Crucial Trick: Expanding X(z)/z
A common pitfall is attempting to expand $X(z)$ directly. Most standard Z-transform pairs have a $z$ in the numerator, such as $\frac{z}{z-a}$. 
If we directly expand $X(z)$ using standard calculus techniques, we obtain terms of the form $\frac{A}{z-a}$. 
Inverse transforming $\frac{A}{z-a}$ requires recognizing that it is $A z^{-1} \frac{z}{z-a}$, which by the time-shifting property introduces a unit delay: $A a^{n-1} u[n-1]$. This shift makes the final equation unnecessarily messy and prone to off-by-one index errors.
To avoid dealing with time shifts immediately, it is customary and highly recommended to divide by $z$ first, expanding $\frac{X(z)}{z}$.

#### Case 1: Distinct Poles
Consider a system with a rational transfer function $\frac{X(z)}{z} = \frac{N(z)}{D(z)}$ where the denominator has purely distinct roots $D(z) = (z-p_1)(z-p_2)\dots(z-p_N)$.
$$ \frac{X(z)}{z} = \frac{A_1}{z-p_1} + \frac{A_2}{z-p_2} + \dots + \frac{A_N}{z-p_N} $$
To find the unknown coefficient $A_k$ (the residue for pole $p_k$), we multiply both sides of the equation by the factor $(z-p_k)$ and then evaluate the entire expression at the pole location $z = p_k$:
$$ A_k = \left[ (z-p_k) \frac{X(z)}{z} \right]_{z=p_k} $$
After computing all constants $A_1 \dots A_N$, multiply both sides back by $z$:
$$ X(z) = \frac{A_1 z}{z-p_1} + \frac{A_2 z}{z-p_2} + \dots + \frac{A_N z}{z-p_N} $$
Each individual term can now be inverse transformed immediately by consulting the ROC.

#### Case 2: Repeated Poles
If a specific pole $p_i$ is repeated $r$ times (order $r$), the partial fraction expansion must include $r$ distinct terms to account for the multiplicity:
$$ \frac{X(z)}{z} = \frac{A_{i1}}{z-p_i} + \frac{A_{i2}}{(z-p_i)^2} + \dots + \frac{A_{ir}}{(z-p_i)^r} + \sum \text{other distinct poles} $$
The coefficient $A_{ik}$ is computed using derivatives evaluated at the pole:
$$ A_{ik} = \frac{1}{(r-k)!} \left[ \frac{d^{r-k}}{dz^{r-k}} \left( (z-p_i)^r \frac{X(z)}{z} \right) \right]_{z=p_i} $$
For example, if the pole is double ($r=2$):
The coefficient for the highest power fraction ($k=2$) requires zero derivatives ($2-2=0$):
$$ A_{i2} = \left[ (z-p_i)^2 \frac{X(z)}{z} \right]_{z=p_i} $$
The coefficient for the lower power fraction ($k=1$) requires one derivative ($2-1=1$):
$$ A_{i1} = \left[ \frac{d}{dz} \left( (z-p_i)^2 \frac{X(z)}{z} \right) \right]_{z=p_i} $$

#### Case 3: Complex Conjugate Pole Pairs
If the coefficients of the original polynomial polynomials $N(z)$ and $D(z)$ are entirely real numbers (which is true for all physical, real-world systems), then any complex poles must always appear in conjugate pairs. 
If $p = \alpha + j\beta$ is a pole, then $p^* = \alpha - j\beta$ is absolutely guaranteed to be a pole as well. 
Furthermore, the calculated residues $A$ and $A^*$ for these poles will also be perfect complex conjugates of each other. This elegant mathematical symmetry ensures that when the inverse Z-transform is computed, all imaginary components exactly cancel out, yielding a time-domain sequence $x[n]$ that is purely real.

#### Combining with Correct ROC
Once the expansion is complete, the Region of Convergence defines the time direction of each term:
- If the overall ROC is $|z| > |p_k|$, the inverse of that specific term is a Right-sided (Causal) sequence: $A_k (p_k)^n u[n]$.
- If the overall ROC is $|z| < |p_k|$, the inverse of that specific term is a Left-sided (Anti-causal) sequence: $-A_k (p_k)^n u[-n-1]$.

### 4.3 Long Division / Power Series Method

The Z-transform is fundamentally defined as an infinite power series in the variable $z^{-1}$:
$$ X(z) = \sum_{n=-\infty}^{\infty} x[n] z^{-n} = \dots + x[-1]z^1 + x[0] + x[1]z^{-1} + x[2]z^{-2} + x[3]z^{-3} + \dots $$
By performing straightforward polynomial long division on the rational transfer function, the coefficients of the resulting polynomial quotient correspond exactly, one-to-one, with the time samples $x[n]$.

#### Causal Sequence (ROC outside the outermost pole)
To extract a causal sequence, arrange both the numerator polynomial and the denominator polynomial in **descending powers of z** (which is equivalent to **ascending powers of $z^{-1}$**).
Performing long division will yield a quotient power series in the specific form: 
$c_0 + c_1 z^{-1} + c_2 z^{-2} + c_3 z^{-3} + \dots$
By matching terms with the fundamental definition, we can simply read off the sequence values:
$x[0] = c_0$, $x[1] = c_1$, $x[2] = c_2$, etc.

#### Anti-Causal Sequence (ROC inside the innermost pole)
To extract an anti-causal sequence, arrange both the numerator polynomial and the denominator polynomial in **ascending powers of z** (which is equivalent to **descending powers of $z^{-1}$**).
Performing long division in this orientation yields a quotient power series in the specific form: 
$d_1 z^1 + d_2 z^2 + d_3 z^3 + \dots$
By matching terms with the fundamental definition, we read off the negative-time sequence values:
$x[-1] = d_1$, $x[-2] = d_2$, $x[-3] = d_3$, etc.

**When to use this method:** 
Long division does NOT provide a closed-form, generalized analytical formula for $x[n]$. It only provides numerical values. Therefore, it is only used when the first few samples are requested by a problem, when checking the first few terms of a PFE derivation for accuracy, or when the denominator polynomial is of such high degree that factoring it analytically to find the poles is mathematically intractable without a computer.

### 4.4 Stability Analysis using Z-transform

For a discrete-time Linear Time-Invariant (LTI) system characterized by its impulse response $h[n]$, the system is defined as Bounded-Input Bounded-Output (BIBO) stable if and only if the impulse response is absolutely summable:
$$ \sum_{n=-\infty}^{\infty} |h[n]| < \infty $$
In the complex Z-domain, the transfer function is $H(z)$. The convergence of the Z-transform infinite sum requires that the Region of Convergence (ROC) strictly includes the unit circle (the locus of points where $|z| = 1$). 
- **Causality Requirement:** A causal system ($h[n]=0$ for $n<0$) requires the ROC to be the exterior of a circle, specifically $|z| > p_{max}$, where $p_{max}$ is the magnitude of the outermost pole.
- **Stability Requirement:** A stable system requires the ROC to include the unit circle.
- **Causal AND Stable System Intersect:** For a system to be BOTH causal and stable, the outermost pole must be located inside the unit circle. Therefore, the absolute, non-negotiable rule is: **For a causal discrete-time LTI system to be stable, ALL poles of its transfer function must lie strictly inside the unit circle** ($|p_i| < 1$ for all index $i$).

### 4.5 System Analysis with Initial Conditions

The standard (bilateral) Z-transform assumes time ranges from $-\infty$ to $+\infty$. Consequently, it cannot inherently handle systems that start at $t=0$ with pre-existing initial energy (initial conditions like charged capacitors or spinning motors). To handle these, we use the **Unilateral Z-transform**, strictly defined for $n \ge 0$:
$$ X^+(z) = \sum_{n=0}^{\infty} x[n] z^{-n} $$
The most important property of the unilateral transform is the Time-Shifting (Delay) Property, which injects initial conditions into the algebraic equation:
$$ \mathcal{Z}^+ \{ x[n-k] \} = z^{-k} X^+(z) + \sum_{m=1}^{k} x[-m] z^{-k+m} $$
For a single discrete delay step ($k=1$):
$$ \mathcal{Z}^+ \{ x[n-1] \} = z^{-1} X^+(z) + x[-1] $$
For a double discrete delay step ($k=2$):
$$ \mathcal{Z}^+ \{ x[n-2] \} = z^{-2} X^+(z) + z^{-1}x[-1] + x[-2] $$
This profound property seamlessly transforms linear difference equations (which are hard to solve directly with initial conditions) into purely algebraic polynomial equations. Solving for $Y(z)$ and taking the inverse transform yields the complete system response, naturally combining the zero-input response (due to initial energy) and the zero-state response (due to the driving input).

---
## 5. COMPLETE PROOFS AND DERIVATIONS

### Derivation 5.1: Residue Theorem Application to Inverse Z-Transform
**Theorem:** The inverse Z-transform is rigorously given by the integral $x[n] = \frac{1}{2\pi j} \oint_C X(z) z^{n-1} dz$.
**Complete Proof:**
1. We begin with the fundamental definition of the bilateral Z-transform:
   $$ X(z) = \sum_{k=-\infty}^{\infty} x[k] z^{-k} $$
2. Multiply both sides of the equation by the term $z^{n-1}$:
   $$ X(z) z^{n-1} = \left( \sum_{k=-\infty}^{\infty} x[k] z^{-k} \right) z^{n-1} = \sum_{k=-\infty}^{\infty} x[k] z^{n-k-1} $$
3. Integrate both sides over a closed counterclockwise contour $C$ that lies entirely within the Region of Convergence (ROC) of $X(z)$:
   $$ \oint_C X(z) z^{n-1} dz = \oint_C \left( \sum_{k=-\infty}^{\infty} x[k] z^{n-k-1} \right) dz $$
4. Assuming uniform absolute convergence within the specified ROC, we are mathematically permitted to interchange the order of the integral and the infinite sum:
   $$ \oint_C X(z) z^{n-1} dz = \sum_{k=-\infty}^{\infty} x[k] \left( \oint_C z^{n-k-1} dz \right) $$
5. Now, consider the fundamental canonical integral from complex analysis:
   $$ I_m = \oint_C z^{m} dz $$
   Let us parameterize the contour $C$ as a perfect circle of radius $R$ centered at the origin, so $z = R e^{j\theta}$.
   As $z$ traces the circle, the angle $\theta$ goes from $0$ to $2\pi$. 
   The differential is $dz = j R e^{j\theta} d\theta$.
   Substituting these into the integral:
   $$ I_m = \int_{0}^{2\pi} (R e^{j\theta})^m (j R e^{j\theta}) d\theta = j R^{m+1} \int_{0}^{2\pi} e^{j(m+1)\theta} d\theta $$
6. We evaluate this integral for two distinct cases:
   - **Case A: If $m \neq -1$:**
     $$ I_m = j R^{m+1} \left[ \frac{e^{j(m+1)\theta}}{j(m+1)} \right]_0^{2\pi} $$
     Because $e^{j(m+1)2\pi} = 1$ and $e^{0} = 1$, the evaluated bracket is $(1 - 1) = 0$. So $I_m = 0$.
   - **Case B: If $m = -1$:**
     The integral simplifies to:
     $$ I_{-1} = j R^{0} \int_{0}^{2\pi} e^{0} d\theta = j (1) \int_{0}^{2\pi} 1 d\theta = j [\theta]_0^{2\pi} = 2\pi j $$
7. Therefore, we have established the powerful identity:
   $$ \oint_C z^{m} dz = \begin{cases} 2\pi j & m = -1 \\ 0 & m \neq -1 \end{cases} $$
8. Returning to our main derivation in Step 4, the exponent in our integral is $m = n - k - 1$. 
   The only term in the entire infinite sum that does not evaluate to zero is when the exponent equals $-1$.
   Setting $n - k - 1 = -1 \implies k = n$.
   For this specific single term where $k=n$, the integral evaluates to $2\pi j$. All other terms vanish completely.
9. Substituting this result back:
   $$ \oint_C X(z) z^{n-1} dz = x[n] (2\pi j) $$
10. Finally, dividing both sides by $2\pi j$ isolates $x[n]$, yielding the intended proof:
    $$ x[n] = \frac{1}{2\pi j} \oint_C X(z) z^{n-1} dz $$
This concludes the rigorous, step-by-step mathematical proof.

---
## 6. WORKED EXAMPLES (MINIMUM 5 — fully solved)

### Example 1: Full Partial Fraction Expansion for Distinct Poles
**Problem statement:** Compute the inverse Z-transform of the system transfer function $H(z) = \frac{z^2}{(z - 0.5)(z - 0.25)}$, operating under the explicit assumption that the system is causal.

**Complete Solution:**
**Step 1: Analyze the ROC.** 
The problem states the system is strictly causal. By theoretical definition, the ROC for a causal sequence must be the exterior of a circle encompassing the outermost pole. 
The given poles are clearly located at $p_1 = 0.5$ and $p_2 = 0.25$. 
Therefore, the definitive ROC is $|z| > 0.5$.

**Step 2: Prepare the function for PFE.** 
Divide the transfer function by $z$ to avoid time-shift complications later:
$$ \frac{H(z)}{z} = \frac{z}{(z - 0.5)(z - 0.25)} $$
Set up the partial fraction structure with unknown residues $A$ and $B$:
$$ \frac{H(z)}{z} = \frac{A}{z - 0.5} + \frac{B}{z - 0.25} $$

**Step 3: Calculate the residues mathematically using the cover-up method.**
For coefficient $A$ (associated with pole at $0.5$):
$$ A = \left[ (z - 0.5) \frac{z}{(z-0.5)(z-0.25)} \right]_{z=0.5} $$
Cancel the terms:
$$ A = \left[ \frac{z}{z-0.25} \right]_{z=0.5} $$
Substitute $z=0.5$:
$$ A = \frac{0.5}{0.5 - 0.25} = \frac{0.5}{0.25} = 2 $$

For coefficient $B$ (associated with pole at $0.25$):
$$ B = \left[ (z - 0.25) \frac{z}{(z-0.5)(z-0.25)} \right]_{z=0.25} $$
Cancel the terms:
$$ B = \left[ \frac{z}{z-0.5} \right]_{z=0.25} $$
Substitute $z=0.25$:
$$ B = \frac{0.25}{0.25 - 0.5} = \frac{0.25}{-0.25} = -1 $$

**Step 4: Reconstruct the full algebraic expression.**
Substitute the calculated residues $A=2$ and $B=-1$ back into the expansion:
$$ \frac{H(z)}{z} = \frac{2}{z - 0.5} - \frac{1}{z - 0.25} $$
Multiply both sides of the equation entirely by $z$:
$$ H(z) = \frac{2z}{z - 0.5} - \frac{z}{z - 0.25} $$

**Step 5: Apply the inverse Z-transform operation.**
Refer to the standard Z-transform pair library. Since the ROC $|z| > 0.5$ physically encompasses both $|z|>0.5$ and $|z|>0.25$, both individual fractional terms must correspond to causal, right-sided time sequences.
Using the rule $\frac{z}{z-a} \longleftrightarrow a^n u[n]$:
$$ h[n] = 2 (0.5)^n u[n] - 1 (0.25)^n u[n] $$
$$ h[n] = [2(0.5)^n - (0.25)^n] u[n] $$

**Physical interpretation:** The overall system response is a linear superposition of two decaying exponential modes. The dominant mode is $(0.5)^n$ because it decays slower than $(0.25)^n$, dictating the long-term settling behavior of the digital filter.
**Common mistakes to avoid:** Forgetting to divide by $z$ in Step 2. If a student expands $H(z) = \frac{A}{z-0.5} + \frac{B}{z-0.25}$, they require transform pairs for $1/(z-a)$, which introduces an irritating unit delay shift $a^{n-1}u[n-1]$, drastically increasing the likelihood of off-by-one errors in the final index expression.

### Example 2: Partial Fraction Expansion with Repeated Poles
**Problem statement:** Find the exact causal inverse Z-transform of the system $X(z) = \frac{z^2}{(z - 0.5)^2}$.

**Complete Solution:**
**Step 1: Prepare the function.**
Divide by $z$:
$$ \frac{X(z)}{z} = \frac{z}{(z - 0.5)^2} $$

**Step 2: Setup the PFE structure for a repeated pole.**
The pole at $p=0.5$ is of order $r=2$. We must include two terms in the expansion:
$$ \frac{X(z)}{z} = \frac{A_1}{z - 0.5} + \frac{A_2}{(z - 0.5)^2} $$

**Step 3: Rigorously calculate the residues.**
For $A_2$ (the highest power term, $k=2$), no derivative is required:
$$ A_2 = \left[ (z - 0.5)^2 \frac{z}{(z - 0.5)^2} \right]_{z=0.5} $$
$$ A_2 = [z]_{z=0.5} = 0.5 $$

For $A_1$ (the lower power term, $k=1$), one derivative is strictly required:
$$ A_1 = \frac{1}{1!} \left[ \frac{d}{dz} \left( (z - 0.5)^2 \frac{z}{(z - 0.5)^2} \right) \right]_{z=0.5} $$
Cancel the denominator terms inside the derivative FIRST:
$$ A_1 = \left[ \frac{d}{dz} (z) \right]_{z=0.5} $$
Compute the derivative of $z$ with respect to $z$, which is simply $1$:
$$ A_1 = [1]_{z=0.5} = 1 $$

**Step 4: Reconstruct the expression.**
Substitute the calculated residues $A_1=1$ and $A_2=0.5$ back into the expansion:
$$ \frac{X(z)}{z} = \frac{1}{z - 0.5} + \frac{0.5}{(z - 0.5)^2} $$
Multiply the entire equation back by $z$:
$$ X(z) = \frac{z}{z - 0.5} + 0.5 \frac{z}{(z - 0.5)^2} $$

**Step 5: Apply the inverse Z-transform.**
Because the problem specifies a causal system, the ROC is $|z| > 0.5$.
We utilize the two standard pairs:
1. $\frac{z}{z-a} \longleftrightarrow a^n u[n]$
2. $\frac{a z}{(z-a)^2} \longleftrightarrow n a^n u[n]$

Rewrite the second term of our expansion to perfectly match the standard form structure. Notice that $a = 0.5$, and our numerator is $0.5z$. It perfectly matches the required form $\frac{0.5 z}{(z - 0.5)^2}$.
Therefore, inverse transforming term by term:
$$ x[n] = (0.5)^n u[n] + n(0.5)^n u[n] $$
Factoring out common terms for a cleaner final result:
$$ x[n] = (1 + n)(0.5)^n u[n] $$

**Physical interpretation:** A repeated pole mathematically models a critically damped or resonance-like condition within discrete time. It is physically characterized by the linear polynomial multiplication factor $n$ modifying the exponential decay envelope.
**Common mistakes to avoid:** Miscalculating the derivative in Step 3 by attempting to take the derivative of the entire rational function BEFORE cancelling the root factor. The cancellation must always happen first.

### Example 3: Long Division for a Causal Sequence
**Problem statement:** Manually calculate the first five numerical terms of the sequence corresponding to $X(z) = \frac{1}{1 - 0.5 z^{-1} - 0.5 z^{-2}}$, assuming a purely causal sequence.

**Complete Solution:**
**Step 1: Set up the polynomial long division framework.** 
Because the sequence is requested to be causal, we must divide the polynomials exactly as they are currently written (in descending powers of $z$, which structurally manifests as ascending powers of the delay operator $z^{-1}$).
Numerator polynomial: $1$
Denominator polynomial: $1 - 0.5 z^{-1} - 0.5 z^{-2}$

**Step 2: Iteration 1 (finding $x[0]$)**
Divide the leading term of the numerator ($1$) by the leading term of the denominator ($1$): $1 \div 1 = 1$. 
This is the first term of the quotient.
Multiply $1$ by the entire denominator: $1 \times (1 - 0.5 z^{-1} - 0.5 z^{-2})$.
Subtract this result from the current numerator: 
$1 - (1 - 0.5 z^{-1} - 0.5 z^{-2}) = 0.5 z^{-1} + 0.5 z^{-2}$.
Current cumulative quotient: $1$.

**Step 3: Iteration 2 (finding $x[1]$)**
Divide the new leading term ($0.5 z^{-1}$) by the leading term of the denominator ($1$): $(0.5 z^{-1}) \div 1 = 0.5 z^{-1}$. 
This is the second term of the quotient.
Multiply $0.5 z^{-1}$ by the entire denominator:
$(0.5 z^{-1}) \times (1 - 0.5 z^{-1} - 0.5 z^{-2}) = 0.5 z^{-1} - 0.25 z^{-2} - 0.25 z^{-3}$.
Subtract this carefully from the remainder of Step 2: 
$(0.5 z^{-1} + 0.5 z^{-2}) - (0.5 z^{-1} - 0.25 z^{-2} - 0.25 z^{-3}) = 0.75 z^{-2} + 0.25 z^{-3}$.
Current cumulative quotient: $1 + 0.5 z^{-1}$.

**Step 4: Iteration 3 (finding $x[2]$)**
Divide the new leading term ($0.75 z^{-2}$) by $1$: $(0.75 z^{-2}) \div 1 = 0.75 z^{-2}$. 
Multiply by denominator:
$(0.75 z^{-2}) \times (1 - 0.5 z^{-1} - 0.5 z^{-2}) = 0.75 z^{-2} - 0.375 z^{-3} - 0.375 z^{-4}$.
Subtract from previous remainder: 
$(0.75 z^{-2} + 0.25 z^{-3}) - (0.75 z^{-2} - 0.375 z^{-3} - 0.375 z^{-4}) = 0.625 z^{-3} + 0.375 z^{-4}$.
Current cumulative quotient: $1 + 0.5 z^{-1} + 0.75 z^{-2}$.

**Step 5: Iteration 4 (finding $x[3]$)**
Divide leading term: $(0.625 z^{-3}) \div 1 = 0.625 z^{-3}$. 
Multiply by denominator:
$(0.625 z^{-3}) \times (1 - 0.5 z^{-1} - 0.5 z^{-2}) = 0.625 z^{-3} - 0.3125 z^{-4} - 0.3125 z^{-5}$.
Subtract: 
$(0.625 z^{-3} + 0.375 z^{-4}) - (0.625 z^{-3} - 0.3125 z^{-4} - 0.3125 z^{-5}) = 0.6875 z^{-4} + 0.3125 z^{-5}$.
Current cumulative quotient: $1 + 0.5 z^{-1} + 0.75 z^{-2} + 0.625 z^{-3}$.

**Step 6: Iteration 5 (finding $x[4]$)**
Divide leading term: $(0.6875 z^{-4}) \div 1 = 0.6875 z^{-4}$.
Current cumulative quotient: $1 + 0.5 z^{-1} + 0.75 z^{-2} + 0.625 z^{-3} + 0.6875 z^{-4}$.

**Step 7: Final Mapping to Time Domain Samples**
By directly equating the resulting polynomial coefficients to the formal Z-transform definition $X(z) = \sum x[n]z^{-n}$:
$x[0] = 1$
$x[1] = 0.5$
$x[2] = 0.75$
$x[3] = 0.625$
$x[4] = 0.6875$

**Physical interpretation:** The output sequence oscillates slightly up and down but gradually approaches a steady state target value. The long division method provides an immediate numerical "window" into this transient behavior.
**Common mistakes to avoid:** Subtracting incorrectly. Keeping meticulous track of double negative signs during the polynomial subtraction step is historically the #1 source of student error in this specific method.

### Example 4: Verifying Forward and Inverse Relation (The Round Trip)
**Problem statement:** We are given a known time-domain sequence $x[n] = (2^n - 3^n)u[n]$. First, find its forward Z-transform $X(z)$ and rigorously determine its Region of Convergence (ROC). Then, perform a complete Partial Fraction Expansion to verify that we can perfectly mathematically recover the original $x[n]$.

**Complete Solution:**
**Phase 1: Forward Z-transform.**
Expand the given expression:
$x[n] = 2^n u[n] - 3^n u[n]$
Applying the fundamental linearity property of the Z-transform:
$X(z) = \mathcal{Z}\{2^n u[n]\} - \mathcal{Z}\{3^n u[n]\}$
Looking up standard tables:
$X(z) = \frac{z}{z-2} - \frac{z}{z-3}$
Determine the ROC components:
ROC for the component $2^n u[n]$ is $|z| > 2$.
ROC for the component $3^n u[n]$ is $|z| > 3$.
The overall system ROC must be the strict mathematical intersection of the individual component ROCs. The intersection of "greater than 2" and "greater than 3" is strictly $|z| > 3$.

Combine the two fractions into a single rational transfer function for the reverse step:
$X(z) = \frac{z(z-3) - z(z-2)}{(z-2)(z-3)}$
Expand numerators:
$X(z) = \frac{z^2 - 3z - (z^2 - 2z)}{(z-2)(z-3)}$
Simplify numerator completely:
$X(z) = \frac{z^2 - 3z - z^2 + 2z}{(z-2)(z-3)} = \frac{-z}{(z-2)(z-3)}$
Final forward result: $X(z) = \frac{-z}{(z-2)(z-3)}$ with firm ROC: $|z| > 3$.

**Phase 2: Inverse Z-transform via PFE.**
We begin with the rational expression: $X(z) = \frac{-z}{(z-2)(z-3)}$ and ROC $|z| > 3$.
Divide by $z$:
$$ \frac{X(z)}{z} = \frac{-1}{(z-2)(z-3)} $$
Set up PFE format:
$$ \frac{X(z)}{z} = \frac{A}{z-2} + \frac{B}{z-3} $$
Calculate Residues meticulously:
$$ A = \left[ (z-2) \frac{-1}{(z-2)(z-3)} \right]_{z=2} = \frac{-1}{2-3} = \frac{-1}{-1} = 1 $$
$$ B = \left[ (z-3) \frac{-1}{(z-2)(z-3)} \right]_{z=3} = \frac{-1}{3-2} = \frac{-1}{1} = -1 $$
Reconstruct the expansion equation:
$$ \frac{X(z)}{z} = \frac{1}{z-2} - \frac{1}{z-3} $$
Multiply fully by $z$:
$$ X(z) = \frac{z}{z-2} - \frac{z}{z-3} $$
Apply inverse mapping. Since the defined ROC is $|z| > 3$, it physically bounds the exterior of BOTH system poles (at 2 and 3). Therefore, both component sequences are guaranteed to be causal (right-sided).
$$ x[n] = 1 (2^n) u[n] - 1 (3^n) u[n] $$
$$ x[n] = (2^n - 3^n)u[n] $$
The recovered equation perfectly matches the starting equation, proving the integrity of the math.

**Physical interpretation:** A complex system built composed of parallel subsystems combines mathematically algebraically. The overall system's stability boundary and causality boundary is dictated strictly by the "worst" or "dominant" component (in this case, the outermost pole residing at $z=3$).
**Common mistakes to avoid:** Falsely assuming the system ROC is the bounded ring $2 < |z| < 3$. Because the initial sequence is explicitly purely causal (as dictated by the step function multiplication $u[n]$), both underlying components must be causal, forcing the ROC to logically be the absolute exterior of the largest magnitude pole.

### Example 5: Solving Difference Equations with Initial Conditions
**Problem statement:** An engineering system is defined by the discrete difference equation $y[n] - 0.5 y[n-1] = u[n]$, operating with a known pre-existing initial condition $y[-1] = 2$. Find the complete mathematical response $y[n]$ strictly for time indices $n \ge 0$.

**Complete Solution:**
**Step 1: Take Unilateral Z-transform.**
Apply the unilateral transform operator $\mathcal{Z}^+$ to both sides of the linear difference equation.
$$ \mathcal{Z}^+ \{ y[n] \} - 0.5 \mathcal{Z}^+ \{ y[n-1] \} = \mathcal{Z}^+ \{ u[n] \} $$
Let the symbol $Y(z)$ definitively equal $\mathcal{Z}^+ \{ y[n] \}$.
Apply the critical single-delay shifting property formula:
$$ Y(z) - 0.5 \left[ z^{-1} Y(z) + y[-1] \right] = \frac{z}{z-1} $$

**Step 2: Inject the physical initial condition.**
Substitute the given energy state $y[-1] = 2$ directly into the algebraic equation.
$$ Y(z) - 0.5 \left[ z^{-1} Y(z) + 2 \right] = \frac{z}{z-1} $$
Distribute the $-0.5$ constant multiplier:
$$ Y(z) - 0.5 z^{-1} Y(z) - 1 = \frac{z}{z-1} $$
Factor out the common $Y(z)$ term on the left-hand side:
$$ Y(z) (1 - 0.5 z^{-1}) - 1 = \frac{z}{z-1} $$

**Step 3: Solve algebraically for $Y(z)$.**
Move the constant $-1$ to the right side of the equation:
$$ Y(z) (1 - 0.5 z^{-1}) = \frac{z}{z-1} + 1 $$
To prepare for standard form, rewrite the term $(1 - 0.5 z^{-1})$ as a proper fraction $\frac{z - 0.5}{z}$:
$$ Y(z) \left( \frac{z - 0.5}{z} \right) = \frac{z}{z-1} + \frac{z-1}{z-1} $$
Combine the two fractions on the right side:
$$ Y(z) \left( \frac{z - 0.5}{z} \right) = \frac{z + z - 1}{z-1} = \frac{2z - 1}{z-1} $$
Isolate $Y(z)$ completely by cross-multiplying:
$$ Y(z) = \left( \frac{z}{z - 0.5} \right) \left( \frac{2z - 1}{z-1} \right) $$
$$ Y(z) = \frac{z(2z - 1)}{(z-1)(z-0.5)} $$

**Step 4: Perform Partial Fraction Expansion to compute $y[n]$.**
Divide the entire equation by $z$:
$$ \frac{Y(z)}{z} = \frac{2z - 1}{(z-1)(z-0.5)} $$
Establish the partial fraction structure:
$$ \frac{Y(z)}{z} = \frac{A}{z-1} + \frac{B}{z-0.5} $$
Calculate the Residue coefficients:
$$ A = \left[ \frac{2z - 1}{z - 0.5} \right]_{z=1} = \frac{2(1) - 1}{1 - 0.5} = \frac{1}{0.5} = 2 $$
$$ B = \left[ \frac{2z - 1}{z - 1} \right]_{z=0.5} = \frac{2(0.5) - 1}{0.5 - 1} = \frac{0}{-0.5} = 0 $$

**Step 5: Final Equation Reconstruction.**
Substitute the coefficients back:
$$ \frac{Y(z)}{z} = \frac{2}{z-1} + \frac{0}{z-0.5} $$
Multiply back by $z$:
$$ Y(z) = \frac{2z}{z-1} $$

**Step 6: Final Inverse Z-transform.**
The sequence is mathematically guaranteed to be strictly causal by the fundamental defining definition of the unilateral transform framework.
Using standard lookup tables:
$$ y[n] = 2 (1)^n u[n] = 2 u[n] $$

**Physical interpretation:** This is a profoundly interesting specific case. The mathematical zero-input response (the decay caused strictly by the pre-existing initial conditions) precisely and exactly cancelled out the decaying transient component of the zero-state response (caused by the new input). This perfectly balanced cancellation leaves a pure, completely flat step output immediately at $n=0$ with zero transient settling time.
**Common mistakes to avoid:** Completely forgetting the unilateral delay property formula. A frequent, disastrous error is applying the initial condition value to $y[0]$ instead of properly assigning it to $y[-1]$ for a single discrete unit delay shift.

---
## 7. ENGINEERING APPLICATIONS AND CASE STUDIES

### Application 7.1: IIR Digital Filter Impulse Response Realization
In professional digital signal processing hardware engineering, complex filters are frequently mathematically designed in the continuous frequency domain (s-domain) and systematically mapped over to the discrete z-domain utilizing the Bilinear Transform. The resulting function $H(z)$ is almost always a highly complex rational fraction polynomial. Engineers heavily rely on the inverse Z-transform (usually executed via algorithmic PFE) to calculate the explicit closed-form discrete equation for the impulse response $h[n]$. This is computationally crucial for an engineer to physically see if the designed filter exhibits excessive time-domain ringing (caused by complex conjugate poles situated too close to the unit circle perimeter) or suffers from excruciatingly slow decay (caused by real positive poles parked dangerously near $z=1$). 
**Detailed engineering parameters:** Suppose a digital low-pass audio filter contains dominant poles located at $0.9 \pm j0.1$. The physical time-domain envelope will strictly ring for an approximate time constant of $\tau \approx 1/(1-0.9) = 10$ discrete samples before settling into an acceptable steady-state margin.

### Application 7.2: Absolute Stability Testing in Aerospace Control Systems
Consider a highly sensitive digital flight control loop governing a quadcopter. It rapidly processes gyroscopic sensor inputs to generate precise motor thrust commands. The overall physical closed-loop system transfer function is rigorously computed as $T(z) = \frac{G(z)}{1 + G(z)H(z)}$. 
Instead of irresponsibly simulating the entire complex non-linear system for millions of possible random input vectors, control engineers programmatically extract the system characteristic equation denominator $1+G(z)H(z)=0$ and mathematically isolate its polynomial roots (the system poles). If even a single solitary root satisfies $|p_i| \ge 1$, the drone will absolutely crash—either by oscillating violently to destruction or diverging instantly to infinity. The Z-transform provides an elegant, mathematically rigorous, and bulletproof guarantee of flight safety dynamics.

### Application 7.3: Precision Step Response Transient Analysis
An industrial robotic arm motor speed controller defined by $G(z)$ is abruptly given a target reference step input mathematically modeled as $R(z) = \frac{z}{z-1}$. The resulting physical output motion is $Y(z) = G(z)R(z)$. By rigorously applying the inverse Z-transform process to $Y(z)$, systems engineers obtain the precise, exact mathematical curve describing the motor rotational speed $y[n]$ over discrete time steps. This crucial curve allows absolute, exact precision calculation of critical metrics like peak overshoot percentage, system rise time, and total error settling time—completely without the prohibitive cost of building expensive, potentially dangerous physical hardware prototypes first.

---
## 8. COMMON STUDENT MISCONCEPTIONS AND ERRORS

1. **Misconception:** The inverse Z-transform of a given mathematical expression $X(z)$ is absolute and mathematically unique.
   * **Correction:** The ROC absolutely must be specified! Without an explicit ROC definition, a single algebraic equation seamlessly maps to entirely multiple, fundamentally different time-domain physical sequences (e.g., completely causal right-sided versus purely anti-causal left-sided). The ROC uniquely and exclusively selects which physical reality is mathematically correct.
2. **Misconception:** Performing PFE directly on the raw function $X(z)$ instead of modifying it to $X(z)/z$.
   * **Correction:** If a student attempts to blindly expand $X(z)$ directly, they invariably generate fraction terms like $A/(z-p)$. While technically, mathematically solvable, processing this necessitates heavily applying the time delay property, which yields the highly error-prone format $A p^{n-1} u[n-1]$. Pre-expanding $X(z)/z$ first elegantly bypasses this, leading smoothly and directly to the vastly simpler, standard reference formula $A p^n u[n]$.
3. **Misconception:** The polynomial long division trick can completely solve any inverse transform easily and efficiently.
   * **Correction:** Polynomial long division exclusively yields a localized sequence of numerical time data samples $x[n]$. It absolutely does not yield a closed-form, generalized mathematical formula (like a clean exponential $a^n$). It is mathematically impossible to rigorously analyze system stability bounds analytically by merely glancing at the first 5 output numbers.
4. **Misconception:** Repeated system poles are simply expanded normally precisely as if they were distinct poles.
   * **Correction:** Repeated poles containing an order degree $r$ strictly necessitate an ascending expansion spanning all powers up to $r$, such as the form $A/(z-p) + B/(z-p)^2$. Calculating their exact, proper mathematical residues explicitly requires executing advanced calculus derivatives.
5. **Misconception:** The physical Region of Convergence mathematically includes the physical locations of the poles themselves.
   * **Correction:** The defined ROC is strictly an "open" mathematical region (formally defined as strictly greater than or strictly less than). By the fundamental definition of singularity, the Z-transform diverges to sheer infinity precisely at a pole coordinate. Therefore, the singular pole itself can literally never reside inside the stable Region of Convergence.
6. **Misconception:** Any LTI system whatsoever with its mathematical poles safely inside the bounds of the unit circle is inherently stable.
   * **Correction:** This highly dangerous assumption is purely only universally true specifically for **causal** operating systems! Conversely, a completely anti-causal system sequence is classified as stable only if its fundamental poles sit strictly *outside* the perimeter of the unit circle. Students must explicitly, carefully interlink causality definitions and stability definitions together correctly.

---
## 9. CONNECTIONS TO OTHER LECTURES

- **Critically Builds Upon:** Lecture 4 (The Fundamental Formal Definition of the infinite Z-transform and rigorous ROC boundaries) and Lecture 5 (Operational Mathematical Properties of the Z-transform, particularly linearity and discrete time-shifting theorems).
- **Essential Foundation For:** Lecture 8 (Analyzing the Frequency Response Dynamics of LTI Systems — achieved by explicitly substituting the boundary $z = e^{j\omega}$) and Lectures 12-14 (Advanced IIR Digital Filter Design methodologies encompassing advanced concepts like Impulse Invariance mapping).
- **Directly Analogous To:** The Continuous-time Laplace Transform operations (specifically inversion via PFE techniques) derived directly from preliminary foundational Signals and Systems prerequisite courses.

---
## 10. EXAMINATION QUESTIONS

### 10.1 Short Answer Questions
**Q1.** Mathematically and conceptually, why is the specific Region of Convergence absolutely critical and essential when accurately computing an inverse Z-transform?
*Model Answer:* Because a singular rational algebraic equation can correspond mathematically to multiple, entirely different physical time-domain discrete sequences (e.g., a causal decaying sequence versus an anti-causal exploding sequence). The specific, defined ROC uniquely and exclusively selects which exact time-domain sequence is mathematically correct for the physical system in question.

**Q2.** Clearly state the strict mathematical condition required for an LTI discrete-time system to be both simultaneously physically causal and strictly BIBO stable, explicitly defined in terms of system pole coordinates.
*Model Answer:* For dual compliance, absolutely all fundamental poles of the system's global transfer function $H(z)$ must lie entirely and strictly inside the inner boundary of the complex unit circle ($|p_i| < 1$).

**Q3.** Conceptually explain the specific, practical engineering purpose of modifying the function to expand $X(z)/z$ instead of raw $X(z)$ during the PFE manual procedure.
*Model Answer:* Almost all standard textbook Z-transform reference pairs structurally contain a '$z$' variable specifically located in the fractional numerator. Pre-expanding the form $X(z)/z$ cleverly allows the engineer to safely multiply the entire expression back by '$z$' later in the final stage, allowing the terms to exactly match the standard reference forms perfectly and entirely circumventing heavily complex, error-prone time-shift index operations.

**Q4.** How exactly does a mathematically repeated multiple-order pole in the complex z-domain physically manifest structurally within the final resulting time domain sequence response?
*Model Answer:* A repeated system pole possessing an order of $r$ directly introduces linear, ramping polynomial multiplication scaling factors into the time domain equation. For instance, a specific double pole situated at root value $a$ mathematically ensures the final time sequence must include a ramping component strictly of the mathematical form $n a^n u[n]$.

**Q5.** In practical application, under what precise conditions is the numerical polynomial long division algorithm vastly preferred by engineers over the analytical Partial Fraction Expansion technique?
*Model Answer:* The long division algorithm is explicitly vastly preferred specifically when only the very first few immediate time samples of a sequence are actually required for analysis, or physically when the complex denominator polynomial is so overwhelmingly mathematically complex that analytically factoring it to extract the precise singular poles is deemed mathematically intractable for manual calculation.

### 10.2 Long Answer / Numerical Problems
**Problem 1.** Rigorously determine and compute the complete inverse Z-transform equation of the function $X(z) = \frac{3z^2 - 4z}{(z-1)(z-2)}$ operating specifically bound by the finite ROC $1 < |z| < 2$.
*Comprehensive Solution Summary:*
1. Structurally modify the expression: $X(z)/z = \frac{3z - 4}{(z-1)(z-2)}$. Set up PFE: $\frac{A}{z-1} + \frac{B}{z-2}$.
2. Compute Residue A: $A = [(3z-4)/(z-2)]_{z=1} = (3(1)-4)/(1-2) = (-1)/(-1) = 1$.
3. Compute Residue B: $B = [(3z-4)/(z-1)]_{z=2} = (3(2)-4)/(2-1) = (6-4)/(1) = 2$.
4. Reconstruct the algebraic fraction: $X(z)/z = \frac{1}{z-1} + \frac{2}{z-2}$. Multiply by z: $X(z) = \frac{z}{z-1} + \frac{2z}{z-2}$.
5. Carefully analyze the explicit boundary ROC $1 < |z| < 2$. This absolutely implies that the specific pole situated at root $z=1$ operates strictly as a causal entity (because $|z|>1$), while the specific pole situated at root $z=2$ operates entirely as a non-causal, anti-causal entity (because $|z|<2$).
6. Systematically apply inverse mappings: The $z=1$ component maps directly to $1^n u[n] = u[n]$. The $z=2$ component maps directly to an inverted, scaled $-2(2^n) u[-n-1]$.
7. Combine for final, precise equation: $x[n] = u[n] - 2(2^n) u[-n-1]$.

**Problem 2.** You are provided a complex transfer function $H(z) = \frac{z}{z^2 + 0.25}$. Accurately find the physical impulse response $h[n]$ strictly operating under the absolute assumption that it represents a strictly causal physical system.
*Comprehensive Solution Summary:*
1. Factor the complex denominator to extract poles. The roots of $z^2 + 0.25 = 0$ are the purely imaginary coordinates $z = \pm j0.5$.
2. Formulate expansion: $H(z)/z = \frac{1}{(z - j0.5)(z + j0.5)} = \frac{A}{z - j0.5} + \frac{B}{z + j0.5}$.
3. Rigorously compute imaginary Residue A: $A = [1/(z + j0.5)]_{z=j0.5} = 1/(j0.5 + j0.5) = 1/j$. Simplify this explicitly to $-j$.
4. Rigorously compute imaginary Residue B: $B = [1/(z - j0.5)]_{z=-j0.5} = 1/(-j0.5 - j0.5) = -1/j$. Simplify this explicitly to $j$.
5. Reconstruct total complex algebraic sum: $H(z) = -j \frac{z}{z - j0.5} + j \frac{z}{z + j0.5}$.
6. Apply time inverse mappings (causal system selected): $h[n] = -j (j0.5)^n u[n] + j (-j0.5)^n u[n]$.
7. This equation is correct but physically unreadable. Simplify radically using Euler's advanced identities: recognize $j = e^{j\pi/2}$. This mathematical transformation ultimately yields the clean, real-valued trigonometric final function: $h[n] = 2 (0.5)^n \sin(\pi n / 2) u[n]$.

**Problem 3.** Fully and rigorously analytically solve the discrete linear difference equation $y[n] - y[n-1] + 0.25 y[n-2] = x[n]$ assuming a constant driving unit step input $x[n]=u[n]$ operating firmly with an absolute zero state system initial conditions baseline.
*Comprehensive Solution Summary:*
1. Apply the baseline Z-transform comprehensively: $Y(z)(1 - z^{-1} + 0.25 z^{-2}) = X(z)$.
2. Compute the raw transfer function: $H(z) = \frac{Y(z)}{X(z)} = \frac{1}{1 - z^{-1} + 0.25 z^{-2}}$. Algebraically simplify to positive powers to reveal poles: $H(z) = \frac{z^2}{(z-0.5)^2}$.
3. Transform driving input: Since $x[n] = u[n]$, strictly $X(z) = \frac{z}{z-1}$.
4. Compute total output expression: $Y(z) = H(z)X(z) = \frac{z^3}{(z-1)(z-0.5)^2}$.
5. Carefully expand $Y(z)/z = \frac{z^2}{(z-1)(z-0.5)^2}$ heavily utilizing complex PFE repeated pole differentiation derivative rules.
6. Mathematical coefficients calculation yields exactly: $Y(z) = 4\frac{z}{z-1} - 3\frac{z}{z-0.5} - \frac{0.5z}{(z-0.5)^2}$.
7. Inverse mapping term by term precisely produces the final dynamic curve: $y[n] = [4 - 3(0.5)^n - n(0.5)^n] u[n]$.

**Problem 4.** Critically systematically determine total holistic system stability and definitive system causality given only the absolute bare pole locations mapped at $p_1 = 0.8, p_2 = -1.2, p_3 = 0.5+j0.2$. Comprehensively define and explicitly list all mathematically possible valid Region of Convergence (ROC) boundaries.
*Comprehensive Solution Summary:*
1. First, precisely compute absolute radial pole magnitudes from the exact z-plane origin: magnitudes are strictly $0.8$, strictly $1.2$, and the complex vector length $\sqrt{0.5^2+0.2^2} = \sqrt{0.25+0.04} = \sqrt{0.29} = 0.538$.
2. Formally mathematically sequence these boundary magnitudes in strictly ascending order: $0.538$, followed by $0.8$, followed by $1.2$.
3. ROC Condition 1 analysis: Exterior boundary $|z| > 1.2$. Because it is outside the largest pole, it strictly maps to a Causal system. Because it fails to envelop the unit circle ($|z|=1$), it physically operates as Unstable.
4. ROC Condition 2 analysis: Inner ring boundary $0.8 < |z| < 1.2$. It fundamentally maps as Two-sided. Because the inner bound is less than 1 and outer is greater than 1, it encompasses the unit circle, making it entirely Stable.
5. ROC Condition 3 analysis: Deep inner ring $0.538 < |z| < 0.8$. It structurally maps as Two-sided. Because the absolute outer boundary is strictly less than 1, it fails to cover the unit circle, making it highly Unstable.
6. ROC Condition 4 analysis: Absolute interior core boundary $|z| < 0.538$. Because it is completely inside the smallest pole, it maps identically as Anti-causal. Failing to envelop the unit circle dictates it is entirely Unstable.

### 10.3 True/False with Justification
1. **False:** The complex inverse Z-transform mathematical formula heavily utilizing Cauchy's formal Integral theorem is fundamentally and regularly heavily used directly for daily practical engineering filter design calculations. (Justification: PFE is overwhelmingly preferred due to sheer practicality; the contour integration method is largely relegated strictly to purely theoretical abstract math).
2. **True:** For completely purely real physical time sequences, any complex system poles discovered must always, unconditionally appear exclusively in mathematically perfect conjugate pairs.
3. **False:** The Region of Convergence strictly boundaries inherently physically include the exact coordinate position of the outermost pole. (Justification: ROC by definition strictly heavily bounds the safe region and never physically includes the infinitely blowing up pole coordinate itself).
4. **True:** The specific unilateral variant of the formal Z-transform mathematical framework can elegantly, easily, and rigorously account directly for absolutely non-zero pre-existing physical initial conditions.
5. **True:** A strictly perfectly causal discrete LTI physical system discovered possessing a singular dominant pole sitting precisely at coordinate boundary $z=1.01$ is undeniably totally fundamentally physically unstable. (Justification: $|p| = 1.01$, which is rigidly $> 1$. This unequivocally violates the foundational causality-stability condition law).
6. **False:** The numerical polynomial long division mathematical algorithm provides an exact, completely closed-form globally generalized rigorous mathematical algebraic equation for the final sequence $x[n]$. (Justification: It exclusively strictly only yields a completely finite, disjointed sequential list of raw numerical static values).

---
## 11. KEY FORMULAS REFERENCE

| Fundamental Concept | Explicit Exact Mathematical Formula |
|---------------------|---------------------------------------|
| Absolute Formal Inverse Z-transform (Complex Contour Integral) | $x[n] = \frac{1}{2\pi j} \oint_C X(z) z^{n-1} dz$ |
| PFE (Distinct Singular Poles Exact Residue Formula) | $A_k = \left[ (z-p_k) \frac{X(z)}{z} \right]_{z=p_k}$ |
| PFE (Repeated Multiple Poles Exact Residue Derivation) | $A_{ik} = \frac{1}{(r-k)!} \left[ \frac{d^{r-k}}{dz^{r-k}} \left( (z-p_i)^r \frac{X(z)}{z} \right) \right]_{z=p_i}$ |
| Standard Causal Exponential Sequence Mapping Pair | $a^n u[n] \longleftrightarrow \frac{z}{z-a}, \quad \|z\| > \|a\|$ |
| Standard Anti-Causal Exponential Sequence Mapping Pair | $-a^n u[-n-1] \longleftrightarrow \frac{z}{z-a}, \quad \|z\| < \|a\|$ |
| Standard Repeated Pole Sequence Mapping Pair | $n a^n u[n] \longleftrightarrow \frac{a z}{(z-a)^2}, \quad \|z\| > \|a\|$ |
| Unilateral Formal Discrete Shift Property (1 step singular delay) | $\mathcal{Z}^+ \{ x[n-1] \} = z^{-1} X^+(z) + x[-1]$ |
| Unilateral Formal Discrete Shift Property (2 step complex delay) | $\mathcal{Z}^+ \{ x[n-2] \} = z^{-2} X^+(z) + z^{-1}x[-1] + x[-2]$ |

---
## 12. FURTHER READING AND REFERENCES
- **John G. Proakis & Dimitris K. Manolakis, *Digital Signal Processing: Principles, Algorithms, and Applications***: Specifically heavily target Chapter 3 (The Z-Transform), paying rigorous attention specifically to Sections 3.3 (Detailed Inverse Z-transform procedures) and 3.4 (Deep Properties of LTI Discrete Systems).
- **Alan V. Oppenheim & Ronald W. Schafer, *Discrete-Time Signal Processing***: A fundamentally more mathematically advanced text. See specifically Chapter 3, which provides highly rigorous abstract proofs directly connecting the complex Cauchy residue theorem formally to the engineering unilateral transform.
- **Simon Haykin & Barry Van Veen, *Signals and Systems***: See strictly Chapter 7. This is an absolutely excellent transitional reference text explicitly tailored for seamlessly comparing continuous Laplace mechanics directly to discrete Z-transform intuition and heavily unpacking complex partial fraction expansion algebraic tricks.
</Faculty Notes — Lecture 6: Inverse Z-Transform & System Analysis>
