# Lecture 2: LTI Systems, Convolution, Stability & Difference Equations

**Course:** EE3621 — Digital Signal Processing  
**Target Audience:** III B.Tech EEE Students  
**Duration:** 40 Minutes  

* **Available Formats:** [LaTeX Source File](file:///C:/Users/sriph/Downloads/DSP/lecture_02.tex) | [Compiled PDF Notes](file:///C:/Users/sriph/Downloads/DSP/lecture_02.pdf)

---

## 1. Lecture Plan (40 Minutes Breakdown)
* **00:00 – 05:00 (5 mins):** Review of System Properties & Introduction to Linear Time-Invariant (LTI) Systems.
* **05:00 – 15:00 (10 mins):** Complete Derivation of the Convolution Sum & Graphical Steps (Folding, Shifting, Multiplying, Summing).
* **15:00 – 22:00 (7 mins):** Properties of Discrete-Time Convolution (Commutativity, Associativity, Distributivity, and Shifting) with rigorous algebraic proofs.
* **22:00 – 30:00 (8 mins):** LTI System Properties: Causality condition ($h[n]=0$ for $n<0$) and BIBO Stability (proof of absolute summability condition in both directions).
* **30:00 – 38:00 (8 mins):** Linear Constant-Coefficient Difference Equations (LCCDE): Homogeneous & Particular Solutions, Initial Rest Condition, and Step Response.
* **38:00 – 40:00 (2 mins):** Interactive Checkpoints & Summary Q&A.

---

## 2. Derivation of the Convolution Sum

A **Linear Time-Invariant (LTI)** system is a system that simultaneously satisfies the properties of **linearity** and **time-invariance**. Such a system is uniquely and completely characterized by its **impulse response** $h[n]$, defined as the output of the system when the input is a unit impulse sequence $\delta[n]$:
$$h[n] = \mathcal{T}\{\delta[n]\}$$

### The Step-by-Step Mathematical Derivation
We can derive the response of an LTI system to any arbitrary input signal $x[n]$ using the following steps:

1. **Sifting Property representation:** Recall from Lecture 1 that any discrete-time sequence $x[n]$ can be written as a weighted sum of shifted unit impulses:
   $$x[n] = \sum_{k=-\infty}^{\infty} x[k] \delta[n-k]$$
   Here, $x[k]$ acts as the scaling coefficient for the impulse centered at index $k$.

2. **Applying the system operator:** Let $\mathcal{T}$ represent the transformation operator of the system. The output $y[n]$ is given by:
   $$y[n] = \mathcal{T}\{x[n]\} = \mathcal{T}\left\{ \sum_{k=-\infty}^{\infty} x[k] \delta[n-k] \right\}$$

3. **Exploiting Linearity:** Since the system is linear, it satisfies the principles of superposition (additivity and scaling). Assuming the system is stable, we can move the system operator inside the summation:
   $$y[n] = \sum_{k=-\infty}^{\infty} x[k] \mathcal{T}\{\delta[n-k]\}$$
   *Note: The scaling coefficients $x[k]$ are treated as constants with respect to the system operator.*

4. **Exploiting Time-Invariance:** By definition, if the system's response to a unit impulse $\delta[n]$ is $h[n]$, then the response to a time-shifted impulse $\delta[n-k]$ must be a time-shifted impulse response $h[n-k]$:
   $$\mathcal{T}\{\delta[n-k]\} = h[n-k]$$

5. **Resulting Convolution Sum:** Substituting this relation back into step 3 yields the fundamental equation of LTI systems, the **Discrete-Time Convolution Sum**:
   $$y[n] = \sum_{k=-\infty}^{\infty} x[k] h[n-k] = x[n] * h[n]$$

### Graphical Steps for Computing Convolution
To calculate the convolution sum graphically for any index $n$, follow these four operations:
1. **Folding (Time Reversal):** Plot the impulse response sequence as a function of the dummy variable $k$ to get $h[k]$. Flip this sequence about the vertical axis ($k=0$) to obtain the time-reversed sequence $h[-k]$.
2. **Shifting:** Shift the folded sequence $h[-k]$ by $n$ units to the right (if $n > 0$) or to the left (if $n < 0$) to obtain $h[n-k]$.
3. **Multiplication:** Multiply the input sequence $x[k]$ with the shifted and folded sequence $h[n-k]$ point-by-point to obtain a product sequence:
   $$v_n[k] = x[k] \cdot h[n-k]$$
4. **Summation:** Sum all the values of the product sequence $v_n[k]$ over all $k$ to find the single output value $y[n]$:
   $$y[n] = \sum_{k=-\infty}^{\infty} v_n[k]$$

Repeat this process for every index $n$ where the sequences overlap.

---

## 3. Properties of Discrete-Time Convolution

### A. Commutativity
The order of signals in a convolution operation does not affect the final output:
$$x[n] * h[n] = h[n] * x[n]$$
* **Proof:** Let $m = n - k$, which implies $k = n - m$. As $k \to \infty$, $m \to -\infty$, and as $k \to -\infty$, $m \to \infty$:
  $$x[n] * h[n] = \sum_{k=-\infty}^{\infty} x[k] h[n-k] = \sum_{m=\infty}^{-\infty} x[n-m] h[m] = \sum_{m=-\infty}^{\infty} h[m] x[n-m] = h[n] * x[n]$$
* **Physical Interpretation:** Feeding an input $x[n]$ into a filter with impulse response $h[n]$ yields the exact same output as feeding $h[n]$ into a system with impulse response $x[n]$.

### B. Associativity
Convolution is associative, allowing cascaded LTI systems to be simplified:
$$\left(x[n] * h_1[n]\right) * h_2[n] = x[n] * \left(h_1[n] * h_2[n]\right)$$
* **Physical Interpretation:** If a signal passes through two LTI systems in series (cascade connection), the equivalent single-block system has an impulse response $h_{eq}[n] = h_1[n] * h_2[n]$. The order of the cascaded systems does not matter.

### C. Distributivity
Convolution distributes over addition:
$$x[n] * \left(h_1[n] + h_2[n]\right) = x[n] * h_1[n] + x[n] * h_2[n]$$
* **Physical Interpretation:** If an input signal is split and processed in parallel by two separate LTI systems, and their outputs are summed, the equivalent single system has an impulse response equal to the sum of the individual responses: $h_{eq}[n] = h_1[n] + h_2[n]$.

### D. Time-Shifting Property
If $y[n] = x[n] * h[n]$, then shifting either input shifts the output by the corresponding sum of shifts:
$$x[n-n_1] * h[n-n_2] = y[n - n_1 - n_2]$$
* **Proof:**
  Let $x_s[n] = x[n-n_1]$. Then:
  $$x_s[n] * h[n-n_2] = \sum_{k=-\infty}^{\infty} x[k-n_1] h[n - n_2 - k]$$
  Let $m = k - n_1 \Rightarrow k = m + n_1$.
  $$\sum_{m=-\infty}^{\infty} x[m] h[n - n_2 - m - n_1] = \sum_{m=-\infty}^{\infty} x[m] h[(n - n_1 - n_2) - m] = y[n - n_1 - n_2]$$

---

## 4. Causality & BIBO Stability of LTI Systems

### A. Causality
A system is causal if the output at any time depends only on present and past values of the input.
* **LTI Causality Condition:** An LTI system is causal if and only if its impulse response is zero for all negative time indices:
  $$h[n] = 0 \quad \forall n < 0$$
* **Proof:** The convolution sum is $y[n] = \sum_{k=-\infty}^{\infty} x[k] h[n-k]$. For the system to be causal, $y[n]$ must not depend on future inputs $x[k]$ (i.e., inputs where $k > n$). This requires the coefficients multiplying $x[k]$ for $k > n$ to be zero. The coefficient multiplying $x[k]$ is $h[n-k]$. For $k > n$, the index $n-k$ is negative. Thus, we must have $h[m] = 0$ for all $m < 0$.
* **Simplified Causal Convolution:** If both the system and the input signal are causal ($x[n] = 0$ for $n < 0$), the convolution limits simplify to:
  $$y[n] = \sum_{k=0}^{n} x[k] h[n-k]$$

### B. BIBO Stability
A system is Bounded-Input Bounded-Output (BIBO) stable if any bounded input $|x[n]| \le M_x < \infty$ produces a bounded output $|y[n]| \le M_y < \infty$.
* **LTI Stability Condition:** An LTI system is stable if and only if its impulse response is **absolutely summable**:
  $$S = \sum_{n=-\infty}^{\infty} |h[n]| < \infty$$

#### Mathematical Proof:
1. **Sufficiency (Absolute summability implies stability):**
   Assume the impulse response is absolutely summable: $\sum_{k=-\infty}^{\infty} |h[k]| = S < \infty$. Given a bounded input $|x[n]| \le M_x < \infty$, we evaluate the magnitude of the output:
   $$|y[n]| = \left| \sum_{k=-\infty}^{\infty} x[n-k] h[k] \right|$$
   Applying the triangle inequality:
   $$|y[n]| \le \sum_{k=-\infty}^{\infty} |x[n-k]| |h[k]|$$
   Since $|x[n-k]| \le M_x$ for all $n-k$:
   $$|y[n]| \le M_x \sum_{k=-\infty}^{\infty} |h[k]| = M_x S < \infty$$
   Thus, the output is bounded, proving the system is BIBO stable.

2. **Necessity (Stability implies absolute summability):**
   Assume the system is stable. We prove that $S < \infty$ by contradiction. Suppose $S = \sum |h[k]| = \infty$.
   Let us construct a bounded input sequence $x[n]$ designed specifically to cause the output to grow infinitely at $n=0$. Define:
   $$x[-k] = \text{sgn}(h[k]) = \begin{cases} 1, & h[k] \ge 0 \\ -1, & h[k] < 0 \end{cases}$$
   This input is bounded because $|x[n]| \le 1$ for all $n$. Now, evaluate the output at $n=0$:
   $$y[0] = \sum_{k=-\infty}^{\infty} x[-k] h[k] = \sum_{k=-\infty}^{\infty} \text{sgn}(h[k]) h[k] = \sum_{k=-\infty}^{\infty} |h[k]| = S = \infty$$
   This contradicts the assumption that any bounded input produces a bounded output. Therefore, $S$ must be finite, proving that absolute summability is a necessary condition.

---

## 5. Linear Constant-Coefficient Difference Equations (LCCDE)

In practice, recursive discrete-time systems (IIR filters) and non-recursive systems (FIR filters) are implemented using difference equations of the form:
$$\sum_{k=0}^{N} a_k y[n-k] = \sum_{m=0}^{M} b_m x[n-m]$$
where $N$ is the order of the system. Typically, we normalize by setting $a_0 = 1$ and solve for $y[n]$:
$$y[n] = -\sum_{k=1}^{N} a_k y[n-k] + \sum_{m=0}^{M} b_m x[n-m]$$

### The Initial Rest Condition
A difference equation by itself does not uniquely define an LTI system; it requires auxiliary boundary conditions.
* To represent a **linear and time-invariant** system, we must apply the **Initial Rest Condition**:
  $$\text{If } x[n] = 0 \quad \forall n < n_0, \quad \text{then } y[n] = 0 \quad \forall n < n_0$$
* If the system is at initial rest, it is guaranteed to be linear, time-invariant, and causal.

### Analytical Solution Components
The complete solution to a difference equation consists of two parts:
$$y[n] = y_h[n] + y_p[n]$$
1. **Homogeneous Solution ($y_h[n]$):** The solution to the equation when the input is set to zero ($\sum_{k=0}^{N} a_k y[n-k] = 0$). We assume a solution of the form $y_h[n] = C \lambda^n$, leading to the characteristic equation:
   $$\sum_{k=0}^{N} a_k \lambda^{N-k} = 0$$
   The roots $\lambda_i$ determine the natural response terms $C_i \lambda_i^n$.
2. **Particular Solution ($y_p[n]$):** The response of the system to the specific input excitation $x[n]$. We assume a form similar to the input (e.g., constant for step inputs, exponential for exponential inputs).

---

## 6. Step Response vs. Impulse Response

* The **Step Response** $s[n]$ of a system is its output when the input is a unit step sequence $u[n]$:
  $$s[n] = h[n] * u[n] = \sum_{k=-\infty}^{\infty} h[k] u[n-k] = \sum_{k=-\infty}^{n} h[k]$$
* The **Impulse Response** $h[n]$ can be recovered from the step response by taking the first backward difference:
  $$h[n] = s[n] - s[n-1]$$
  This behaves as the discrete-time analogue to differentiation.

---

## 7. Detailed Worked Examples

### Example 1: Causal Convolution of Two Finite Sequences
**Problem:** Compute the convolution $y[n] = x[n] * h[n]$ of the following finite sequences:
$$x[n] = \{1, \underset{\uparrow}{2}, 1\}, \quad h[n] = \{\underset{\uparrow}{1}, 1\}$$
*(The arrow indicates the index $n=0$.)*

**Solution:**
1. **Determine the ranges:**
   * $x[n]$ is non-zero for $n \in [-1, 1]$. Let $N_x = [-1, 1]$, length $L_x = 3$.
   * $h[n]$ is non-zero for $n \in [0, 1]$. Let $N_h = [0, 1]$, length $L_h = 2$.
   * The output range starts at $n_{start} = -1 + 0 = -1$ and ends at $n_{end} = 1 + 1 = 2$. The total length is $L_y = L_x + L_h - 1 = 3 + 2 - 1 = 4$.

2. **Evaluate the sum $y[n] = \sum_{k=-\infty}^{\infty} x[k] h[n-k]$ for each $n \in [-1, 2]$:**
   * **For $n = -1$:**
     $$y[-1] = x[-1]h[0] + x[0]h[-1] + x[1]h[-2] = (1)(1) + (2)(0) + (1)(0) = 1$$
   * **For $n = 0$:**
     $$y[0] = x[-1]h[1] + x[0]h[0] + x[1]h[-1] = (1)(1) + (2)(1) + (1)(0) = 3$$
   * **For $n = 1$:**
     $$y[1] = x[-1]h[2] + x[0]h[1] + x[1]h[0] = (1)(0) + (2)(1) + (1)(1) = 3$$
   * **For $n = 2$:**
     $$y[2] = x[-1]h[3] + x[0]h[2] + x[1]h[1] = (1)(0) + (2)(0) + (1)(1) = 1$$

3. **Result:**
   $$y[n] = \{1, \underset{\uparrow}{3}, 3, 1\}$$

---

### Example 2: Convolution of Causal Exponential Sequences
**Problem:** Compute the convolution of $x[n] = a^n u[n]$ and $h[n] = b^n u[n]$ for both the case where $a \neq b$ and the case where $a = b$.

**Solution:**
The convolution sum is:
$$y[n] = \sum_{k=-\infty}^{\infty} x[k] h[n-k] = \sum_{k=-\infty}^{\infty} a^k u[k] b^{n-k} u[n-k]$$

1. **Analyze unit step constraints:**
   * $u[k] = 1$ for $k \ge 0$.
   * $u[n-k] = 1$ for $n-k \ge 0 \Rightarrow k \le n$.
   * For $n < 0$, there is no value of $k$ satisfying $0 \le k \le n$, so $y[n] = 0$.
   * For $n \ge 0$, the limits of the summation are from $k=0$ to $k=n$:
     $$y[n] = \sum_{k=0}^{n} a^k b^{n-k} = b^n \sum_{k=0}^{n} \left(\frac{a}{b}\right)^k$$

2. **Case A: $a \neq b$**
   Using the finite geometric series formula $\sum_{k=0}^{n} q^k = \frac{1-q^{n+1}}{1-q}$:
   $$y[n] = b^n \frac{1 - (a/b)^{n+1}}{1 - (a/b)} = b^n \frac{\frac{b^{n+1} - a^{n+1}}{b^{n+1}}}{\frac{b-a}{b}} = \frac{b^{n+1} - a^{n+1}}{b - a} u[n] = \frac{a^{n+1} - b^{n+1}}{a - b} u[n]$$

3. **Case B: $a = b$**
   The summation simplifies because the ratio is $1$:
   $$y[n] = a^n \sum_{k=0}^{n} (1)^k = a^n (n + 1) u[n]$$

---

### Example 3: Finding the Impulse Response from a Difference Equation
**Problem:** Find the impulse response $h[n]$ of the causal system described by:
$$y[n] - 0.7 y[n-1] = x[n]$$

**Solution:**
The impulse response $h[n]$ is the output when $x[n] = \delta[n]$. Thus:
$$h[n] - 0.7 h[n-1] = \delta[n]$$
Since the system is causal, we apply the initial rest condition: $h[n] = 0$ for $n < 0$. Let's compute the first few terms recursively:
* **For $n = 0$:** $h[0] - 0.7 h[-1] = \delta[0] \Rightarrow h[0] - 0.7(0) = 1 \Rightarrow h[0] = 1$
* **For $n = 1$:** $h[1] - 0.7 h[0] = \delta[1] \Rightarrow h[1] - 0.7(1) = 0 \Rightarrow h[1] = 0.7$
* **For $n = 2$:** $h[2] - 0.7 h[1] = \delta[2] \Rightarrow h[2] - 0.7(0.7) = 0 \Rightarrow h[2] = (0.7)^2 = 0.49$
* **For general $n \ge 0$:** We observe the pattern:
  $$h[n] = (0.7)^n u[n]$$

---

### Example 4: Testing LTI Stability
**Problem:** An LTI system has an impulse response $h[n] = a^n u[n]$. Prove under what conditions of $a$ the system is stable.

**Solution:**
To check stability, we evaluate the absolute sum $S = \sum_{n=-\infty}^{\infty} |h[n]|$:
$$S = \sum_{n=0}^{\infty} |a^n| = \sum_{n=0}^{\infty} |a|^n$$
This is an infinite geometric series with ratio $q = |a|$.
* **Case 1: $|a| < 1$**
  The series converges:
  $$S = \frac{1}{1 - |a|} < \infty$$
  Since $S$ is finite, the system is **stable**.
* **Case 2: $|a| \ge 1$**
  The terms of the series do not decay to zero. The summation diverges:
  $$S = \infty$$
  The system is **unstable**.

---

### Example 5: Step Response of a First-Order Causal Filter
**Problem:** Find the step response $s[n]$ of the causal system described by the impulse response $h[n] = 0.5^n u[n]$.

**Solution:**
The step response is:
$$s[n] = \sum_{k=0}^{n} h[k] = \sum_{k=0}^{n} (0.5)^k$$
For $n \ge 0$, applying the finite geometric series sum formula:
$$s[n] = \frac{1 - 0.5^{n+1}}{1 - 0.5} = \frac{1 - 0.5 \cdot 0.5^n}{0.5} = 2(1 - 0.5^{n+1}) = 2 - 0.5^n$$
For $n < 0$, $s[n] = 0$. Thus:
$$s[n] = (2 - 0.5^n) u[n]$$
At steady state ($n \to \infty$), the step response converges to a value of $2$.

---

### Example 6: Solving a Difference Equation with Step Input
**Problem:** Solve the difference equation $y[n] - 0.5 y[n-1] = u[n]$ under initial rest conditions.

**Solution:**
1. **Find the homogeneous solution $y_h[n]$:**
   Set the input to zero: $y_h[n] - 0.5 y_h[n-1] = 0$.
   Substitute $y_h[n] = C \lambda^n$:
   $$C \lambda^n - 0.5 C \lambda^{n-1} = 0 \Rightarrow \lambda - 0.5 = 0 \Rightarrow \lambda = 0.5$$
   So:
   $$y_h[n] = C (0.5)^n$$

2. **Find the particular solution $y_p[n]$:**
   Since the input $x[n] = u[n]$ is a constant ($1$) for $n \ge 0$, we assume a constant particular solution: $y_p[n] = K$.
   Substitute into the difference equation:
   $$K - 0.5 K = 1 \Rightarrow 0.5 K = 1 \Rightarrow K = 2$$
   So:
   $$y_p[n] = 2 \quad (n \ge 0)$$

3. **Form the complete solution:**
   $$y[n] = y_h[n] + y_p[n] = C (0.5)^n + 2 \quad (n \ge 0)$$

4. **Apply initial boundary conditions to find $C$:**
   Under initial rest, $y[-1] = 0$. Use the difference equation at $n=0$:
   $$y[0] = 0.5 y[-1] + u[0] = 0.5(0) + 1 = 1$$
   Substitute $n=0$ into the complete solution equation:
   $$y[0] = C (0.5)^0 + 2 = C + 2$$
   Equating the two:
   $$C + 2 = 1 \Rightarrow C = -1$$

5. **Final Solution:**
   $$y[n] = (2 - 0.5^n) u[n]$$

---

## 8. Interactive Lecture Checkpoints

* **Checkpoint 1: Why is an unstable LTI system dangerous in engineering applications?**
  * **Answer:** An unstable system has poles outside the unit circle, causing the impulse response to grow exponentially. If a bounded input (like a step voltage or sensor signal) is applied, the output will quickly grow toward infinity, saturating the amplifier circuits or physically damaging the hardware.

* **Checkpoint 2: Show that $x[n] * \delta[n] = x[n]$ using the convolution sum.**
  * **Answer:** By definition:
    $$x[n] * \delta[n] = \sum_{k=-\infty}^{\infty} x[k] \delta[n-k]$$
    Since $\delta[n-k]$ is non-zero (equal to 1) only when $n-k = 0 \Rightarrow k = n$, the infinite sum collapses to a single term evaluated at $k = n$:
    $$x[n] * \delta[n] = x[n] \cdot 1 = x[n]$$

* **Checkpoint 3: Explain the difference between homogeneous response and transient response.**
  * **Answer:** The homogeneous response describes the natural, unexcited behavior of the system based solely on its internal feedback configuration (determined by the characteristic roots). The transient response is the temporary part of the complete response that decays to zero as $n \to \infty$. For stable systems, the homogeneous response corresponds directly to the transient response.

* **Checkpoint 4: Prove that the cascade connection order of two stable causal LTI systems does not change the overall system response.**
  * **Answer:** Let the systems have impulse responses $h_1[n]$ and $h_2[n]$. If they are connected in series, the equivalent impulse response is $h_{eq}[n] = h_1[n] * h_2[n]$. By the commutative property of convolution, $h_1[n] * h_2[n] = h_2[n] * h_1[n]$. Thus, the equivalent impulse response is identical regardless of the order, meaning the overall response remains unchanged.
