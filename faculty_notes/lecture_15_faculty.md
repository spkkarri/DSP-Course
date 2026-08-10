<Faculty Notes — Lecture 15: Power Spectral Density & Wiener Filter>
## EE3621: Digital Signal Processing | III B.Tech EEE
### Faculty Reference Document — Textbook Replacement

---
## PREFACE FOR FACULTY
(How to teach this lecture, common student difficulties, prerequisite checks, suggested demos)

This lecture introduces the foundational concepts of statistical signal processing, specifically Power Spectral Density (PSD) and the Wiener Filter. 
**How to teach this lecture:**
Start by reminding students that in the real world, signals like speech, noise, and communication symbols are not deterministic; they are inherently random. The tools of Fourier analysis still apply, but we must use them on statistical measures like autocorrelation rather than the signals directly.
Emphasize that we assume Wide-Sense Stationary (WSS) random processes throughout this lecture. Without stationarity, these basic tools fall apart and we must move to adaptive filters.
The core of the lecture is the **Orthogonality Principle**. This is *the* key insight in estimation theory. Stress that to minimize error, the estimation error must be orthogonal to the data. It is a concept they will see again and again in machine learning, communications, and advanced signal processing.
Take your time going through the derivations. Do not skip steps. When deriving the Wiener-Khinchin theorem, be sure to explain why we use a truncated sequence $x_N[n]$ and then take the limit as $N \to \infty$.

**Common student difficulties:**
1. Students often struggle with the leap from deterministic to random signals. The interchange of expectation and summation/integration in derivations often confuses them.
2. The concept of an "ensemble" average vs. a "time" average can be confusing. Remind them of ergodicity, although we won't mathematically prove it here.
3. Students often confuse the cross-correlation $R_{xy}[m]$ being non-symmetric, assuming $R_{xy}[m] = R_{xy}[-m]$. Emphasize the conjugate symmetry $R_{xy}[m] = R_{yx}^*[-m]$.

**Prerequisite checks:**
Before beginning the new material, ensure students are familiar with:
- Expectation operator $E\{\cdot\}$
- Discrete-Time Fourier Transform (DTFT)
- Convolution sum
- Matrix multiplication and inversion (for solving Wiener-Hopf)

**Suggested demos:**
Show a noisy sine wave or a noisy speech signal in MATLAB. 
1. Calculate its periodogram using `pwelch`.
2. Filter it using a simple 2-tap Wiener filter designed via the autocorrelation matrix.
3. Compare the time-domain plots before and after filtering, and play the audio to visually and audibly demonstrate noise reduction.

---
## 1. LEARNING OBJECTIVES
By the end of this comprehensive lecture, students will be able to:
1. **Define** Wide-Sense Stationary (WSS) processes and their key statistical properties, including mean and autocorrelation.
2. **Explain** the physical significance of the autocorrelation sequence and its relation to signal power.
3. **Prove** the Wiener-Khinchin theorem rigorously, connecting the autocorrelation sequence to the Power Spectral Density (PSD).
4. **Derive** the complete output autocorrelation and PSD expressions for a Linear Time-Invariant (LTI) system excited by a WSS input.
5. **Formulate** the optimal linear estimation problem and mathematically apply the Orthogonality Principle to minimize the Mean Square Error (MSE).
6. **Construct** and solve the Wiener-Hopf equations for a finite impulse response (FIR) filter using matrix algebra.
7. **Calculate** the Minimum Mean Square Error (MMSE) for a given Wiener filter implementation and interpret its physical meaning.
8. **Analyze** practical applications of Wiener filtering, including channel equalization, noise reduction, and echo cancellation.

---
## 2. PREREQUISITE KNOWLEDGE REVIEW
(What students must know before this lecture; brief review with formulas)

Before delving into PSD and Wiener filters, we must review the prerequisite mathematical tools.

**1. Probability and Expected Value (Mean):**
The expected value $E\{X\}$ of a random variable is its statistical average over an infinite ensemble.
For linear operations, expectation distributes:
$$E\{aX + bY\} = aE\{X\} + bE\{Y\}$$
Variance is defined as:
$$\text{Var}(X) = E\{(X - E\{X\})^2\} = E\{X^2\} - (E\{X\})^2$$

**2. Discrete-Time Fourier Transform (DTFT):**
The DTFT of a deterministic, finite-energy sequence $x[n]$ is given by:
$$X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n}$$
This transforms a discrete-time signal into a continuous function of normalized frequency $\omega$ in radians/sample.

**3. Inverse DTFT:**
The original time-domain sequence can be recovered via the integral over one period ($2\pi$):
$$x[n] = \frac{1}{2\pi} \int_{-\pi}^{\pi} X(e^{j\omega}) e^{j\omega n} d\omega$$

**4. LTI Systems and Convolution:**
For a Linear Time-Invariant (LTI) system characterized by its impulse response $h[n]$ and excited by an input $x[n]$, the output $y[n]$ is given by the discrete convolution sum:
$$y[n] = h[n] * x[n] = \sum_{k=-\infty}^{\infty} h[k] x[n-k]$$

**5. Parseval's Theorem for DTFT:**
The energy of a deterministic signal can be computed in either domain:
$$\sum_{n=-\infty}^{\infty} |x[n]|^2 = \frac{1}{2\pi} \int_{-\pi}^{\pi} |X(e^{j\omega})|^2 d\omega$$

---
## 3. HISTORICAL AND MOTIVATIONAL CONTEXT
(Who discovered this? Real engineering applications. Why does EEE need this?)

**Who discovered this?**
The theoretical foundation of the Wiener filter was formulated by the brilliant American mathematician Norbert Wiener during the tumultuous years of World War II (circa 1942). Originally, it was a classified military project. The goal was to develop an automatic fire-control system that could predict the future position of evasive enemy aircraft based on noisy, jittery radar measurements, thereby directing anti-aircraft artillery with high precision. At almost the exact same time, but on the other side of the world, Andrey Kolmogorov in the Soviet Union independently developed the discrete-time equivalent of this theory. Thus, in many advanced texts, it is referred to as the Wiener-Kolmogorov filter.

**Why does Electrical and Electronics Engineering (EEE) need this?**
In EEE, whether we are designing communication systems, audio processing hardware, or biomedical devices, we are constantly battling noise. 
- A cellular antenna receives a signal that is heavily distorted by multipath fading and thermal noise.
- An EEG machine picks up faint brainwaves corrupted by 50/60 Hz powerline interference and muscle artifact noise.
- A hearing aid must amplify the speech of a conversational partner while suppressing the clatter of a busy restaurant.

In all these cases, the desired signal is hidden within noise. If we know something about the statistical properties of the signal and the noise (specifically, their autocorrelations), the Wiener filter provides the mathematically *optimal* linear framework for separating them. It minimizes the mean square error between the estimated signal and the true (but hidden) signal. 

Furthermore, the Wiener filter forms the conceptual foundation for almost all modern adaptive algorithms. When statistics change over time, we use Adaptive Filters (like the Least Mean Squares or LMS algorithm, invented by Widrow and Hoff). The LMS algorithm is simply a stochastic gradient descent method aimed at finding the very Wiener-Hopf solution we will derive today!

---
## 4. THEORETICAL FOUNDATIONS

### 4.1 Wide-Sense Stationary (WSS) Random Processes
(Complete mathematical treatment — every step shown, no "it can be shown that")

A random process $x[n]$ represents an ensemble (a collection) of possible signals, where each specific signal is one "realization" of the process. Because we cannot predict the exact value of $x[n]$ at any time, we characterize the process using statistical averages.

A random process is called **Strict-Sense Stationary (SSS)** if its entire probability density function (PDF) is invariant to shifts in time. This is an extremely strong condition and is often impossible to verify in practical engineering scenarios.

Instead, we rely on a weaker, more practical condition known as **Wide-Sense Stationarity (WSS)**. A random process $x[n]$ is WSS if and only if it satisfies two conditions:

1. **Constant Mean:**
   The expected value of the signal is constant for all time indices $n$.
   $$E\{x[n]\} = \mu_x \quad \text{for all } n$$

2. **Shift-Invariant Autocorrelation:**
   The autocorrelation function, which measures the correlation between the signal at time $n$ and the signal at time $n-m$, depends *only* on the time difference (the lag, $m$) and not on the absolute time $n$.
   $$E\{x[n] x^*[n-m]\} = R_{xx}[m] \quad \text{for all } n$$

*(Note: The asterisk $*$ denotes complex conjugation, which is necessary when dealing with complex-valued baseband signals in communications. For real-valued signals, $x^*[n-m] = x[n-m]$).*

**Physical Meaning of Autocorrelation:**
- $R_{xx}[m]$ quantifies the similarity or "memory" of the signal over a delay of $m$ samples. If $R_{xx}[m]$ is large and decays slowly, the signal is highly predictable and smooth. If it drops to zero immediately for $m \neq 0$, the signal has no memory (it is purely random white noise).
- At lag $m = 0$, the autocorrelation evaluates to the second moment:
  $$R_{xx}[0] = E\{x[n]x^*[n]\} = E\{|x[n]|^2\}$$
  This represents the **Total Average Power** of the random signal.

**Properties of Autocorrelation for WSS Processes:**
1. **Total Power is Non-Negative:** $R_{xx}[0] \geq 0$
2. **Conjugate Symmetry (Hermitian Property):** 
   Let's prove that $R_{xx}[-m] = R_{xx}^*[m]$.
   Start with the definition:
   $$R_{xx}[-m] = E\{x[n] x^*[n - (-m)]\} = E\{x[n] x^*[n+m]\}$$
   Let $k = n+m$. Then $n = k-m$. Substitute this into the expectation:
   $$R_{xx}[-m] = E\{x[k-m] x^*[k]\}$$
   Because scalar multiplication is commutative, $x[k-m] x^*[k] = x^*[k] x[k-m]$.
   Taking the complex conjugate of the entire expression:
   $$R_{xx}[-m] = (E\{x[k] x^*[k-m]\})^* = R_{xx}^*[m]$$
   For purely real signals, this implies that $R_{xx}[m]$ is an even function: $R_{xx}[-m] = R_{xx}[m]$.
3. **Maximum at Zero Lag:** 
   The magnitude of the autocorrelation at any lag is bounded by the total power.
   $$|R_{xx}[m]| \leq R_{xx}[0]$$
   This is a direct consequence of the Cauchy-Schwarz inequality for expectations: $E\{|XY|\}^2 \leq E\{|X|^2\}E\{|Y|^2\}$. Setting $X = x[n]$ and $Y = x^*[n-m]$ immediately yields the result.
4. **Positive Semi-Definite:** 
   We will prove this later using quadratic forms. It means that the Fourier transform of the autocorrelation sequence is always non-negative.

### 4.2 Cross-Correlation
When we have two jointly WSS processes, $x[n]$ and $y[n]$, we describe their relationship using the cross-correlation function.

Definition:
$$R_{xy}[m] = E\{x[n+m] y^*[n]\}$$
*(Note: Some textbooks define this as $E\{x[n]y^*[n-m]\}$. Because of stationarity, $E\{x[n+m]y^*[n]\} = E\{x[k]y^*[k-m]\}$ by substituting $k = n+m$. Both definitions are equivalent).*

**Symmetry Property of Cross-Correlation:**
Unlike autocorrelation, cross-correlation is NOT symmetric. 
$$R_{xy}[m] \neq R_{xy}[-m]$$
Instead, we can prove the following relationship:
$$R_{xy}[m] = E\{x[n+m] y^*[n]\}$$
Consider the cross-correlation with swapped variables at negative lag:
$$R_{yx}[-m] = E\{y[n-m] x^*[n]\}$$
Conjugate this expression:
$$R_{yx}^*[-m] = (E\{y[n-m] x^*[n]\})^* = E\{y^*[n-m] x[n]\}$$
Let $k = n-m$, so $n = k+m$.
$$R_{yx}^*[-m] = E\{y^*[k] x[k+m]\} = E\{x[k+m] y^*[k]\} = R_{xy}[m]$$
Thus, **$R_{xy}[m] = R_{yx}^*[-m]$**.

### 4.3 Power Spectral Density (PSD)
Deterministic finite-energy signals have well-defined Discrete-Time Fourier Transforms (DTFT). However, WSS random signals (like thermal noise) persist forever. They have infinite energy, meaning their DTFT $X(e^{j\omega})$ does not converge.

Instead of talking about the "energy spectrum," we talk about the **Power Spectral Density (PSD)**, denoted $S_{xx}(e^{j\omega})$. The PSD describes how the finite average power of the signal is distributed across frequency.

**Wiener-Khinchin Theorem:**
The fundamental theorem of statistical signal processing states that the PSD of a WSS process is simply the DTFT of its autocorrelation sequence.
$$S_{xx}(e^{j\omega}) = \sum_{m=-\infty}^{\infty} R_{xx}[m] e^{-j\omega m}$$
*(We will prove this rigorously in Section 5).*

**Properties of PSD:**
1. **Real-Valued:** Because $R_{xx}[m]$ is conjugate symmetric, its Fourier transform is purely real.
2. **Non-Negative:** The PSD represents power, so $S_{xx}(e^{j\omega}) \geq 0$ for all $\omega$.
3. **Total Average Power:** The total power can be found by integrating the PSD over one full frequency period ($-\pi$ to $\pi$), divided by $2\pi$. This is exactly the inverse DTFT evaluated at $m=0$:
   $$R_{xx}[0] = \frac{1}{2\pi} \int_{-\pi}^{\pi} S_{xx}(e^{j\omega}) d\omega$$

### 4.4 LTI Systems with WSS Inputs
When a random signal is passed through a system, we need to know how its statistics change.
Let a WSS signal $x[n]$ with mean $\mu_x$ and autocorrelation $R_{xx}[m]$ be the input to an LTI filter with impulse response $h[n]$. The output is $y[n] = h[n] * x[n]$.

**Mean of Output:**
$$E\{y[n]\} = E\left\{ \sum_{k=-\infty}^{\infty} h[k] x[n-k] \right\}$$
Because expectation is a linear operator, we can swap it with the infinite summation (assuming stability of the filter):
$$E\{y[n]\} = \sum_{k=-\infty}^{\infty} h[k] E\{x[n-k]\}$$
Since $x[n]$ is WSS, $E\{x[n-k]\} = \mu_x$:
$$E\{y[n]\} = \mu_x \sum_{k=-\infty}^{\infty} h[k]$$
The sum of the impulse response is simply the DTFT evaluated at $\omega = 0$ (the DC gain):
$$E\{y[n]\} = \mu_x H(e^{j0})$$

**Output Autocorrelation and PSD:**
The output autocorrelation is given by:
$$R_{yy}[m] = h[m] * h^*[-m] * R_{xx}[m]$$
And the output PSD is given by:
$$S_{yy}(e^{j\omega}) = |H(e^{j\omega})|^2 S_{xx}(e^{j\omega})$$
*(We will prove both of these rigorously in Section 5).*

**Physical Insight:** The filter shapes the input power spectrum strictly by the squared magnitude of its frequency response. The phase response of the filter, $\angle H(e^{j\omega})$, has absolutely zero effect on the output PSD!

### 4.5 The Optimal Linear Estimation Problem Formulation
Now we move to the core of the lecture: the Wiener Filter.

**The Setup:**
We have a desired signal $d[n]$ that we cannot observe directly. 
Instead, we observe a corrupted signal $x[n]$. A very common model is additive noise:
$$x[n] = d[n] + v[n]$$
where $v[n]$ is a zero-mean random noise process.

We want to design a linear Finite Impulse Response (FIR) filter with coefficients $w[k]$ to process the observation $x[n]$ and produce an estimate $\hat{d}[n]$ that is as close to $d[n]$ as possible.
$$\hat{d}[n] = \sum_{k=0}^{M-1} w[k] x[n-k]$$

**Vector Notation:**
For convenience, let's represent the $M$ filter weights as a column vector:
$$\mathbf{w} = \begin{bmatrix} w[0] \\ w[1] \\ \vdots \\ w[M-1] \end{bmatrix}$$
And let the $M$ most recent observations be a data vector:
$$\mathbf{x}_n = \begin{bmatrix} x[n] \\ x[n-1] \\ \vdots \\ x[n-M+1] \end{bmatrix}$$
Then the estimate is a simple dot product:
$$\hat{d}[n] = \mathbf{w}^T \mathbf{x}_n$$

**The Error:**
The estimation error is the difference between the true desired signal and our estimate:
$$e[n] = d[n] - \hat{d}[n] = d[n] - \mathbf{w}^T \mathbf{x}_n$$

**The Objective Function:**
We wish to find the specific vector $\mathbf{w}$ that minimizes the Mean Square Error (MSE), which we define as $J$:
$$J = E\{|e[n]|^2\} = E\{e[n] e^*[n]\}$$
The Wiener filter is the unique set of weights $\mathbf{w}_{opt}$ that achieves this minimum.

### 4.6 The Orthogonality Principle
To minimize the MSE, what condition must the error $e[n]$ satisfy?
The answer is the **Orthogonality Principle**:
*The optimal filter is achieved when the estimation error $e[n]$ is statistically orthogonal to every single piece of data $x[n-k]$ used to form the estimate.*
Mathematically:
$$E\{e[n] x^*[n-k]\} = 0 \quad \text{for all } k = 0, 1, \dots, M-1$$
*(The rigorous calculus-based derivation of this is in Section 5).*

**Geometric Intuition:**
Think of the desired signal $d[n]$ as a vector in a high-dimensional space. The filter can only construct an estimate $\hat{d}[n]$ that lies in the subspace spanned by the observed data vectors $\{x[n], x[n-1], \dots, x[n-M+1]\}$. The shortest distance (minimum error) between the true vector $d[n]$ and this subspace occurs when the error vector $e[n]$ is dropped perpendicularly (orthogonally) onto the subspace. If it weren't perpendicular, we could find a better estimate!

### 4.7 Wiener-Hopf Equations
Let's apply the Orthogonality Principle to find the actual filter weights.
Substitute the definition of the error $e[n] = d[n] - \sum_{l=0}^{M-1} w[l] x[n-l]$ into the orthogonality condition:
$$E\left\{ \left( d[n] - \sum_{l=0}^{M-1} w[l] x[n-l] \right) x^*[n-k] \right\} = 0 \quad \text{for } k=0, \dots, M-1$$

Distribute the expectation:
$$E\{d[n] x^*[n-k]\} - E\left\{ \sum_{l=0}^{M-1} w[l] x[n-l] x^*[n-k] \right\} = 0$$

Move the summation outside the expectation (linearity):
$$E\{d[n] x^*[n-k]\} - \sum_{l=0}^{M-1} w[l] E\{ x[n-l] x^*[n-k] \} = 0$$

Now, recognize the terms:
1. $E\{d[n] x^*[n-k]\}$ is the cross-correlation between the desired signal and the input, evaluated at lag $k$. We denote this $R_{dx}[k]$.
2. $E\{x[n-l] x^*[n-k]\}$ is the autocorrelation of the input, evaluated at lag $(n-l) - (n-k) = k - l$. We denote this $R_{xx}[k-l]$.

Substitute these back:
$$R_{dx}[k] - \sum_{l=0}^{M-1} w[l] R_{xx}[k-l] = 0$$
$$\sum_{l=0}^{M-1} w[l] R_{xx}[k-l] = R_{dx}[k] \quad \text{for } k = 0, 1, \dots, M-1$$

This is a system of $M$ linear equations known as the **Wiener-Hopf Equations**.

We can express this elegantly in matrix form:
$$\mathbf{R}_{xx} \mathbf{w}_{opt} = \mathbf{r}_{dx}$$

Where:
- $\mathbf{R}_{xx}$ is the $M \times M$ autocorrelation matrix of the input data. It is a Toeplitz matrix (constant along diagonals).
- $\mathbf{w}_{opt}$ is the $M \times 1$ vector of optimal filter weights.
- $\mathbf{r}_{dx}$ is the $M \times 1$ cross-correlation vector.

Solving for the optimal weights simply requires matrix inversion:
$$\mathbf{w}_{opt} = \mathbf{R}_{xx}^{-1} \mathbf{r}_{dx}$$

### 4.8 Minimum Mean Square Error (MMSE)
Once we deploy the optimal Wiener filter, the resulting error variance is called the Minimum Mean Square Error (MMSE), denoted $\xi_{min}$.
$$\xi_{min} = R_{dd}[0] - \mathbf{w}_{opt}^T \mathbf{r}_{dx}$$
*(Derived fully in Section 5).*
This tells us that the initial error power (which is just the power of the desired signal if we did no filtering at all) is reduced by the projection of the filter weights onto the cross-correlation vector.

### 4.9 Non-Causal Wiener Filter (Frequency Domain)
If we remove the restriction that the filter must be FIR (finite length), and instead allow it to be infinite and non-causal (i.e., $k$ goes from $-\infty$ to $\infty$), the Wiener-Hopf equations become:
$$\sum_{l=-\infty}^{\infty} w[l] R_{xx}[k-l] = R_{dx}[k] \quad \text{for all } k$$
Notice that the left side is now exactly a convolution: $w[k] * R_{xx}[k]$.
Taking the DTFT of both sides turns convolution into multiplication:
$$W_{opt}(e^{j\omega}) \cdot S_{xx}(e^{j\omega}) = S_{dx}(e^{j\omega})$$
Solving for the filter frequency response gives the **Non-Causal Wiener Filter**:
$$W_{opt}(e^{j\omega}) = \frac{S_{dx}(e^{j\omega})}{S_{xx}(e^{j\omega})}$$

**Important Caveat:** This filter is non-causal. It requires knowledge of future samples of $x[n]$ to compute the current output. It provides an absolute theoretical upper bound on performance but cannot be implemented in real-time. To make it causal requires spectral factorization (a much more advanced topic).

---
## 5. COMPLETE PROOFS AND DERIVATIONS
(All theorems proved rigorously from first principles)

### 5.1 Rigorous Proof of the Wiener-Khinchin Theorem
**Theorem:** The PSD is the DTFT of the autocorrelation: $S_{xx}(e^{j\omega}) = \sum_{m=-\infty}^{\infty} R_{xx}[m] e^{-j\omega m}$.

**Proof:**
A WSS process $x[n]$ does not have finite energy, so its direct DTFT does not exist. We begin by defining a truncated version of the signal, $x_N[n]$:
$x_N[n] = x[n]$ for $-N \leq n \leq N$
$x_N[n] = 0$ otherwise.

Because $x_N[n]$ is finite in length, its DTFT exists:
$$X_N(e^{j\omega}) = \sum_{n=-N}^{N} x[n] e^{-j\omega n}$$

The periodogram (an estimate of the power spectrum) for this truncated signal is defined as the scaled squared magnitude of its Fourier transform:
$$P_N(e^{j\omega}) = \frac{1}{2N+1} |X_N(e^{j\omega})|^2$$

The true Power Spectral Density is defined as the ensemble average (expectation) of the periodogram as the truncation window grows to infinity:
$$S_{xx}(e^{j\omega}) = \lim_{N \to \infty} E\{ P_N(e^{j\omega}) \}$$

Let's compute the expected value of the periodogram for a finite $N$:
$$E\{P_N(e^{j\omega})\} = E\left\{ \frac{1}{2N+1} \left( \sum_{n=-N}^{N} x[n] e^{-j\omega n} \right) \left( \sum_{k=-N}^{N} x^*[k] e^{j\omega k} \right) \right\}$$

Because expectation is linear, we can move it inside the summations:
$$E\{P_N(e^{j\omega})\} = \frac{1}{2N+1} \sum_{n=-N}^{N} \sum_{k=-N}^{N} E\{x[n]x^*[k]\} e^{-j\omega (n-k)}$$

Recognize that $E\{x[n]x^*[k]\}$ is the autocorrelation $R_{xx}[n-k]$. Let us perform a change of variables, defining the lag as $m = n-k$.
The double summation represents adding up elements in a $(2N+1) \times (2N+1)$ grid. 
For a given constant difference $m$, how many pairs of $(n,k)$ satisfy $n-k=m$?
If you draw the grid, you will see it forms diagonal lines. The main diagonal ($m=0$) has $2N+1$ elements. The next diagonal ($m=1$) has $2N$ elements, and so on. In general, for a lag $m$, there are exactly $(2N+1 - |m|)$ terms.
The maximum possible lag is $2N$ and the minimum is $-2N$.

Thus, we can collapse the double sum into a single sum over $m$:
$$E\{P_N(e^{j\omega})\} = \frac{1}{2N+1} \sum_{m=-2N}^{2N} (2N+1 - |m|) R_{xx}[m] e^{-j\omega m}$$
$$E\{P_N(e^{j\omega})\} = \sum_{m=-2N}^{2N} \left( 1 - \frac{|m|}{2N+1} \right) R_{xx}[m] e^{-j\omega m}$$

Notice the term $\left( 1 - \frac{|m|}{2N+1} \right)$. This is a triangular window function (a Bartlett window).
Now, we apply the limit as $N \to \infty$. For any fixed lag $m$, as $N$ approaches infinity, the fraction $\frac{|m|}{2N+1}$ approaches 0. Thus, the triangular window approaches 1 everywhere.
$$S_{xx}(e^{j\omega}) = \lim_{N \to \infty} E\{P_N(e^{j\omega})\} = \sum_{m=-\infty}^{\infty} R_{xx}[m] e^{-j\omega m}$$
This completes the proof. $\blacksquare$

### 5.2 Proof of LTI System Output Autocorrelation and PSD
**Theorem:** $R_{yy}[m] = h[m] * h^*[-m] * R_{xx}[m]$ and $S_{yy}(e^{j\omega}) = |H(e^{j\omega})|^2 S_{xx}(e^{j\omega})$.

**Proof:**
By definition, the output autocorrelation is:
$$R_{yy}[m] = E\{y[n] y^*[n-m]\}$$
Substitute the convolution sum definition for $y[n]$:
$$R_{yy}[m] = E\left\{ \left( \sum_{k=-\infty}^{\infty} h[k] x[n-k] \right) \left( \sum_{l=-\infty}^{\infty} h^*[l] x^*[n-m-l] \right) \right\}$$
Move the expectation operator inside:
$$R_{yy}[m] = \sum_{k=-\infty}^{\infty} \sum_{l=-\infty}^{\infty} h[k] h^*[l] E\{x[n-k] x^*[n-m-l]\}$$
The expected value is the input autocorrelation evaluated at the difference of the indices:
$$E\{x[n-k] x^*[n-m-l]\} = R_{xx}[ (n-k) - (n-m-l) ] = R_{xx}[m + l - k]$$
Substitute this back:
$$R_{yy}[m] = \sum_{k=-\infty}^{\infty} h[k] \left( \sum_{l=-\infty}^{\infty} h^*[l] R_{xx}[m - k + l] \right)$$
Let us define a time-reversed and conjugated version of the impulse response: $h_{rev}[n] = h^*[-n]$.
Then $h^*[l] = h_{rev}[-l]$.
The inner sum becomes:
$$\sum_{l=-\infty}^{\infty} h_{rev}[-l] R_{xx}[(m-k) - (-l)]$$
This is exactly the definition of the convolution between $h_{rev}$ and $R_{xx}$, evaluated at $(m-k)$.
So the equation simplifies to:
$$R_{yy}[m] = \sum_{k=-\infty}^{\infty} h[k] [ h_{rev} * R_{xx} ]_{m-k}$$
This outer sum is exactly the definition of a convolution with $h[k]$.
Therefore:
$$R_{yy}[m] = h[m] * h_{rev}[m] * R_{xx}[m] = h[m] * h^*[-m] * R_{xx}[m]$$

Now, to find the PSD, take the DTFT of both sides. We know that convolution in the time domain corresponds to multiplication in the frequency domain.
$$S_{yy}(e^{j\omega}) = \text{DTFT}\{h[m]\} \cdot \text{DTFT}\{h^*[-m]\} \cdot \text{DTFT}\{R_{xx}[m]\}$$
The DTFT of $h[m]$ is $H(e^{j\omega})$.
The DTFT of a time-reversed conjugated signal $h^*[-m]$ is $H^*(e^{j\omega})$.
The DTFT of $R_{xx}[m]$ is $S_{xx}(e^{j\omega})$.
Therefore:
$$S_{yy}(e^{j\omega}) = H(e^{j\omega}) H^*(e^{j\omega}) S_{xx}(e^{j\omega}) = |H(e^{j\omega})|^2 S_{xx}(e^{j\omega})$$
This completes the proof. $\blacksquare$

### 5.3 Proof of the Orthogonality Principle
**Theorem:** The optimal weights that minimize the MSE $J = E\{|e[n]|^2\}$ must satisfy $E\{e[n] x^*[n-k]\} = 0$.

**Proof using Calculus:**
We want to minimize $J = E\{e[n] e^*[n]\}$.
To find the minimum, we must take the partial derivative of $J$ with respect to each filter weight $w_k$, and set it to zero. Because we are dealing with complex variables, we use Wirtinger calculus, which allows us to treat $w$ and $w^*$ as independent variables and differentiate with respect to $w^*$.

$$\frac{\partial J}{\partial w^*[k]} = \frac{\partial}{\partial w^*[k]} E\{e[n] e^*[n]\}$$
Swap derivative and expectation:
$$\frac{\partial J}{\partial w^*[k]} = E\left\{ e[n] \frac{\partial e^*[n]}{\partial w^*[k]} + e^*[n] \frac{\partial e[n]}{\partial w^*[k]} \right\}$$

Recall that $e[n] = d[n] - \sum_m w[m] x[n-m]$.
This expression depends on $w$, but not on $w^*$. Thus, $\frac{\partial e[n]}{\partial w^*[k]} = 0$.

The conjugate error is $e^*[n] = d^*[n] - \sum_m w^*[m] x^*[n-m]$.
The derivative of $e^*[n]$ with respect to $w^*[k]$ is simply the coefficient of $w^*[k]$:
$$\frac{\partial e^*[n]}{\partial w^*[k]} = -x^*[n-k]$$

Substitute these back into the expectation:
$$\frac{\partial J}{\partial w^*[k]} = E\{ e[n] (-x^*[n-k]) + 0 \}$$
For a minimum, we set the derivative to zero:
$$-E\{ e[n] x^*[n-k] \} = 0 \implies E\{e[n] x^*[n-k]\} = 0$$
This must hold for all $k = 0, 1, \dots, M-1$, completing the proof. $\blacksquare$

### 5.4 Proof of the Minimum Mean Square Error (MMSE) Formula
**Theorem:** $\xi_{min} = R_{dd}[0] - \mathbf{w}_{opt}^T \mathbf{r}_{dx}$.

**Proof:**
The mean square error is:
$$\xi = E\{e[n] e^*[n]\}$$
Substitute the definition of the conjugate error $e^*[n] = d^*[n] - \hat{d}^*[n]$ into the equation:
$$\xi = E\{e[n] (d[n] - \hat{d}[n])^*\} = E\{e[n] d^*[n]\} - E\{e[n] \hat{d}^*[n]\}$$

Now, let's analyze the second term: $E\{e[n] \hat{d}^*[n]\}$.
The estimate is $\hat{d}[n] = \sum_k w[k] x[n-k]$. So the conjugate is $\hat{d}^*[n] = \sum_k w^*[k] x^*[n-k]$.
$$E\{e[n] \hat{d}^*[n]\} = E\left\{ e[n] \sum_{k} w^*[k] x^*[n-k] \right\} = \sum_k w^*[k] E\{ e[n] x^*[n-k] \}$$
By the Orthogonality Principle, we proved that $E\{e[n] x^*[n-k]\} = 0$ for all $k$ when using the optimal weights.
Therefore, the entire sum collapses to zero!
$$E\{e[n] \hat{d}^*[n]\} = 0$$

This leaves us with a greatly simplified expression for the minimum error:
$$\xi_{min} = E\{e[n] d^*[n]\}$$
Now substitute the definition of $e[n]$:
$$\xi_{min} = E\left\{ \left( d[n] - \sum_k w_{opt}[k] x[n-k] \right) d^*[n] \right\}$$
$$\xi_{min} = E\{d[n] d^*[n]\} - \sum_k w_{opt}[k] E\{x[n-k] d^*[n]\}$$

The first term is the autocorrelation of the desired signal at lag 0: $R_{dd}[0]$.
The expected value in the second term is the cross-correlation: $E\{x[n-k] d^*[n]\} = R_{xd}[-k]$.
For real-valued signals, $R_{xd}[-k] = R_{dx}[k]$.
$$\xi_{min} = R_{dd}[0] - \sum_k w_{opt}[k] R_{dx}[k]$$
In vector matrix notation, this summation is a dot product:
$$\xi_{min} = R_{dd}[0] - \mathbf{w}_{opt}^T \mathbf{r}_{dx}$$
This completes the proof. $\blacksquare$

---
## 6. WORKED EXAMPLES (MINIMUM 5 — fully solved)

### Example 1: PSD of an Exponentially Decaying Autocorrelation
**Problem statement:** Given a WSS signal with autocorrelation sequence $R_{xx}[m] = (0.5)^{|m|}$, find its Power Spectral Density $S_{xx}(e^{j\omega})$ and verify mathematically that it is real and strictly non-negative.

**Solution:**
We use the Wiener-Khinchin theorem:
$$S_{xx}(e^{j\omega}) = \sum_{m=-\infty}^{\infty} (0.5)^{|m|} e^{-j\omega m}$$
We must split this summation to handle the absolute value correctly. We split it into negative indices, zero, and positive indices:
$$S_{xx}(e^{j\omega}) = \sum_{m=-\infty}^{-1} (0.5)^{-m} e^{-j\omega m} + (0.5)^0 e^0 + \sum_{m=1}^{\infty} (0.5)^{m} e^{-j\omega m}$$
For the first summation, let $k = -m$. As $m$ goes from $-1$ down to $-\infty$, $k$ goes from $1$ up to $\infty$:
$$S_{xx}(e^{j\omega}) = \sum_{k=1}^{\infty} (0.5)^{k} e^{j\omega k} + 1 + \sum_{m=1}^{\infty} (0.5)^{m} e^{-j\omega m}$$
Group the terms into exponential bases:
$$S_{xx}(e^{j\omega}) = \sum_{k=1}^{\infty} (0.5 e^{j\omega})^k + 1 + \sum_{m=1}^{\infty} (0.5 e^{-j\omega})^m$$
Recall the infinite geometric series formula: $\sum_{n=1}^\infty a^n = \frac{a}{1-a}$, provided $|a| < 1$. Here $|0.5 e^{\pm j\omega}| = 0.5 < 1$, so it converges.
$$S_{xx}(e^{j\omega}) = \frac{0.5e^{j\omega}}{1-0.5e^{j\omega}} + 1 + \frac{0.5e^{-j\omega}}{1-0.5e^{-j\omega}}$$
Let's find a common denominator for the two fractions:
$$S_{xx}(e^{j\omega}) = 1 + \frac{0.5e^{j\omega}(1-0.5e^{-j\omega}) + 0.5e^{-j\omega}(1-0.5e^{j\omega})}{(1-0.5e^{j\omega})(1-0.5e^{-j\omega})}$$
Expand the numerator:
$0.5e^{j\omega} - 0.25 + 0.5e^{-j\omega} - 0.25 = 0.5(e^{j\omega}+e^{-j\omega}) - 0.5$
Expand the denominator:
$1 - 0.5e^{j\omega} - 0.5e^{-j\omega} + 0.25 = 1.25 - 0.5(e^{j\omega}+e^{-j\omega})$
Substitute Euler's formula: $e^{j\omega}+e^{-j\omega} = 2\cos(\omega)$:
$$S_{xx}(e^{j\omega}) = 1 + \frac{0.5(2\cos(\omega)) - 0.5}{1.25 - 0.5(2\cos(\omega))} = 1 + \frac{\cos(\omega) - 0.5}{1.25 - \cos(\omega)}$$
Get a common denominator for the $1$:
$$S_{xx}(e^{j\omega}) = \frac{1.25 - \cos(\omega) + \cos(\omega) - 0.5}{1.25 - \cos(\omega)} = \frac{0.75}{1.25 - \cos(\omega)}$$

**Verification:** 
The function $\cos(\omega)$ is purely real, so the expression is purely real. 
Furthermore, $\cos(\omega)$ is bounded between $-1$ and $1$. 
The maximum value of the denominator is $1.25 - (-1) = 2.25$. 
The minimum value of the denominator is $1.25 - (1) = 0.25$. 
Since the denominator is always between 0.25 and 2.25, it is strictly positive. A positive numerator divided by a positive denominator is strictly positive. Therefore, $S_{xx}(e^{j\omega}) > 0$ for all $\omega$.

**Physical interpretation:** The PSD is largest when the denominator is smallest (at $\omega = 0$), where it peaks at $0.75/0.25 = 3$. It is smallest at $\omega = \pi$, where it dips to $0.75/2.25 = 0.33$. This implies the signal is mostly composed of low frequencies (it's a "low-pass" signal), which aligns with the fact that consecutive samples are positively correlated ($0.5$).

### Example 2: Filtering White Noise
**Problem statement:** White noise $v[n]$ with variance $\sigma_v^2 = 2$ is passed through a first-order IIR filter with system function $H(z) = \frac{1}{1 - 0.8z^{-1}}$. Find the output autocorrelation sequence $R_{yy}[m]$ and the output PSD $S_{yy}(e^{j\omega})$.

**Solution:**
**Step 1: Find the Output PSD.**
The input is white noise, meaning samples are completely uncorrelated. 
Its autocorrelation is $R_{vv}[m] = 2\delta[m]$.
Its PSD is flat: $S_{vv}(e^{j\omega}) = 2$.
The frequency response of the filter is found by substituting $z = e^{j\omega}$:
$H(e^{j\omega}) = \frac{1}{1 - 0.8e^{-j\omega}}$
The output PSD is given by the product:
$$S_{yy}(e^{j\omega}) = |H(e^{j\omega})|^2 S_{vv}(e^{j\omega})$$
Calculate the squared magnitude response:
$$|H(e^{j\omega})|^2 = H(e^{j\omega}) H^*(e^{j\omega}) = \left(\frac{1}{1 - 0.8e^{-j\omega}}\right) \left(\frac{1}{1 - 0.8e^{j\omega}}\right)$$
$$|H(e^{j\omega})|^2 = \frac{1}{1 - 0.8e^{j\omega} - 0.8e^{-j\omega} + 0.64} = \frac{1}{1.64 - 1.6\cos(\omega)}$$
Therefore, the output PSD is:
$$S_{yy}(e^{j\omega}) = \frac{2}{1.64 - 1.6\cos(\omega)}$$

**Step 2: Find the Output Autocorrelation.**
We could find the inverse DTFT of the PSD, but it is often easier to use the time-domain formula:
$$R_{yy}[m] = h[m] * h[-m] * R_{vv}[m]$$
Since $R_{vv}[m] = 2\delta[m]$, convolution with it just scales the result by 2:
$$R_{yy}[m] = 2 (h[m] * h[-m])$$
The impulse response of the filter (from $H(z)$) is $h[m] = (0.8)^m u[m]$.
Let's compute the deterministic autocorrelation of the impulse response, $r_{hh}[m] = \sum_{k=-\infty}^{\infty} h[k] h[k-m]$.
Assume $m \geq 0$:
$$r_{hh}[m] = \sum_{k=m}^{\infty} (0.8)^k (0.8)^{k-m} = \sum_{k=m}^{\infty} (0.8)^{2k-m} = (0.8)^{-m} \sum_{k=m}^{\infty} (0.64)^k$$
To solve the sum, change variables: let $l = k - m$. When $k=m$, $l=0$.
$$r_{hh}[m] = (0.8)^{-m} \sum_{l=0}^{\infty} (0.64)^{l+m} = (0.8)^{-m} (0.64)^m \sum_{l=0}^{\infty} (0.64)^l$$
Since $(0.64)^m = (0.8)^{2m}$, the term outside is $(0.8)^{-m} (0.8)^{2m} = (0.8)^m$.
The infinite sum evaluates to $\frac{1}{1 - 0.64} = \frac{1}{0.36} = 2.778$.
$$r_{hh}[m] = 2.778 (0.8)^m \quad \text{for } m \geq 0$$
Since autocorrelation is symmetric, we can generalize to all $m$ by using absolute value:
$$r_{hh}[m] = 2.778 (0.8)^{|m|}$$
Finally, the output autocorrelation is scaled by 2:
$$R_{yy}[m] = 2 \cdot r_{hh}[m] = 5.556 (0.8)^{|m|}$$

**Physical interpretation:** The LTI filter introduces "memory" to the white noise. The output samples are no longer independent; they are now correlated, which is why the PSD is no longer flat (it's "colored noise").

### Example 3: Designing a 2-Tap Wiener Filter
**Problem statement:** You are given the task of estimating a desired signal $d[n]$ using a 2-tap FIR Wiener filter $\mathbf{w} = [w[0], w[1]]^T$ applied to the observed data $x[n]$. 
The input signal has an autocorrelation matrix $\mathbf{R}_{xx} = \begin{bmatrix} 1 & 0.5 \\ 0.5 & 1 \end{bmatrix}$. 
The cross-correlation vector between the desired and input signal is $\mathbf{r}_{dx} = \begin{bmatrix} 0.8 \\ 0.5 \end{bmatrix}$. 
The total power of the desired signal is $R_{dd}[0] = 1$.
Solve for the optimal weights $\mathbf{w}_{opt}$ and calculate the resulting Minimum Mean Square Error (MMSE).

**Solution:**
**Step 1: Set up the Wiener-Hopf equations.**
The matrix equation is $\mathbf{R}_{xx} \mathbf{w}_{opt} = \mathbf{r}_{dx}$.
$$\begin{bmatrix} 1 & 0.5 \\ 0.5 & 1 \end{bmatrix} \begin{bmatrix} w[0] \\ w[1] \end{bmatrix} = \begin{bmatrix} 0.8 \\ 0.5 \end{bmatrix}$$

**Step 2: Solve the linear system.**
This expands into two equations:
1) $1\cdot w[0] + 0.5\cdot w[1] = 0.8$
2) $0.5\cdot w[0] + 1\cdot w[1] = 0.5$

From equation 1, express $w[0]$ in terms of $w[1]$:
$w[0] = 0.8 - 0.5w[1]$

Substitute this into equation 2:
$0.5(0.8 - 0.5w[1]) + w[1] = 0.5$
$0.4 - 0.25w[1] + w[1] = 0.5$
$0.75w[1] = 0.1$
$w[1] = \frac{0.1}{0.75} = \frac{2}{15} \approx 0.1333$

Now plug $w[1]$ back to find $w[0]$:
$w[0] = 0.8 - 0.5\left(\frac{2}{15}\right) = \frac{8}{10} - \frac{1}{15} = \frac{24}{30} - \frac{2}{30} = \frac{22}{30} = \frac{11}{15} \approx 0.7333$

The optimal filter weights are $\mathbf{w}_{opt} = [0.7333, 0.1333]^T$.

**Step 3: Calculate the MMSE.**
The formula for the minimum error variance is:
$$\xi_{min} = R_{dd}[0] - \mathbf{w}_{opt}^T \mathbf{r}_{dx}$$
$$\xi_{min} = 1 - (w[0]r_{dx}[0] + w[1]r_{dx}[1])$$
$$\xi_{min} = 1 - \left( \frac{11}{15}(0.8) + \frac{2}{15}(0.5) \right)$$
$$\xi_{min} = 1 - \left( \frac{11}{15}\cdot\frac{4}{5} + \frac{2}{15}\cdot\frac{1}{2} \right)$$
$$\xi_{min} = 1 - \left( \frac{44}{75} + \frac{1}{15} \right) = 1 - \left( \frac{44}{75} + \frac{5}{75} \right) = 1 - \frac{49}{75} = \frac{26}{75} \approx 0.3467$$

**Physical interpretation:** If we did no filtering and just guessed 0, our mean square error would be $R_{dd}[0] = 1$. By leveraging the correlation with the observation using just 2 filter taps, we reduced the error power dramatically to roughly $0.347$.

### Example 4: Non-Causal Wiener Filter in Frequency Domain
**Problem statement:** A clean speech signal $s[n]$ has a power spectral density given by $S_{ss}(e^{j\omega}) = \frac{1}{|1-0.8e^{-j\omega}|^2}$. It is sent over a channel that adds white noise $v[n]$ with variance $\sigma_v^2 = 1$. The signal and noise are statistically independent. The received signal is $x[n] = s[n] + v[n]$. 
Derive the frequency response of the optimal non-causal Wiener filter $W_{opt}(e^{j\omega})$ designed to estimate $s[n]$.

**Solution:**
The optimal non-causal filter is given by $W_{opt}(e^{j\omega}) = \frac{S_{dx}(e^{j\omega})}{S_{xx}(e^{j\omega})}$.
Here, our desired signal is $d[n] = s[n]$.
First, compute the input PSD $S_{xx}(e^{j\omega})$. Because $s[n]$ and $v[n]$ are independent, their cross-correlation is zero. Thus, the PSD of their sum is the sum of their PSDs:
$$S_{xx}(e^{j\omega}) = S_{ss}(e^{j\omega}) + S_{vv}(e^{j\omega})$$
Second, compute the cross-PSD $S_{dx}(e^{j\omega})$.
$R_{dx}[m] = E\{s[n+m] x^*[n]\} = E\{s[n+m] (s^*[n] + v^*[n])\} = E\{s[n+m]s^*[n]\} + 0 = R_{ss}[m]$.
Therefore, $S_{dx}(e^{j\omega}) = S_{ss}(e^{j\omega})$.

Substituting these into the filter equation:
$$W_{opt}(e^{j\omega}) = \frac{S_{ss}(e^{j\omega})}{S_{ss}(e^{j\omega}) + S_{vv}(e^{j\omega})}$$
Plug in the known spectra (knowing $S_{vv}(e^{j\omega}) = 1$ for white noise):
$$W_{opt}(e^{j\omega}) = \frac{ \frac{1}{|1-0.8e^{-j\omega}|^2} }{ \frac{1}{|1-0.8e^{-j\omega}|^2} + 1 }$$
Multiply numerator and denominator by $|1-0.8e^{-j\omega}|^2$:
$$W_{opt}(e^{j\omega}) = \frac{1}{1 + |1-0.8e^{-j\omega}|^2}$$
Expand the magnitude squared term:
$|1-0.8e^{-j\omega}|^2 = (1-0.8e^{-j\omega})(1-0.8e^{j\omega}) = 1 - 0.8e^{j\omega} - 0.8e^{-j\omega} + 0.64 = 1.64 - 1.6\cos(\omega)$
Therefore:
$$W_{opt}(e^{j\omega}) = \frac{1}{1 + 1.64 - 1.6\cos(\omega)} = \frac{1}{2.64 - 1.6\cos(\omega)}$$

**Physical interpretation:** Look at the behavior of the filter. At $\omega = 0$ (where signal power is highest), the gain is $\frac{1}{2.64 - 1.6} = \frac{1}{1.04} \approx 0.96$. It passes the signal through almost untouched. At $\omega = \pi$ (where signal power is very low, but noise power is still 1), the gain is $\frac{1}{2.64 + 1.6} = \frac{1}{4.24} \approx 0.236$. The filter heavily attenuates high frequencies because it "knows" that anything at those frequencies is primarily noise. The Wiener filter optimally balances signal distortion vs noise attenuation.

### Example 5: Autocorrelation of a Moving Average Process
**Problem statement:** A random process is generated by adding the current and previous sample of a white noise process $x[n]$ with variance $\sigma^2$: $y[n] = x[n] + x[n-1]$. Derive the autocorrelation sequence $R_{yy}[m]$ directly using the expectation operator.

**Solution:**
By definition:
$$R_{yy}[m] = E\{y[n] y[n-m]\}$$
Substitute the definition of $y[n]$ and $y[n-m]$:
$$R_{yy}[m] = E\{(x[n] + x[n-1])(x[n-m] + x[n-1-m])\}$$
Expand the product into four terms:
$$R_{yy}[m] = E\{x[n]x[n-m]\} + E\{x[n]x[n-1-m]\} + E\{x[n-1]x[n-m]\} + E\{x[n-1]x[n-1-m]\}$$
Because $x[n]$ is white noise, $E\{x[k]x[l]\} = \sigma^2$ if $k=l$, and $0$ otherwise. This can be written as $E\{x[k]x[l]\} = \sigma^2 \delta[k-l]$.
Let's apply this to each term:
1. $E\{x[n]x[n-m]\} = \sigma^2 \delta[m]$
2. $E\{x[n]x[n-1-m]\} = \sigma^2 \delta[m+1]$ (since $n = n-1-m \implies m = -1$)
3. $E\{x[n-1]x[n-m]\} = \sigma^2 \delta[m-1]$ (since $n-1 = n-m \implies m = 1$)
4. $E\{x[n-1]x[n-1-m]\} = \sigma^2 \delta[m]$

Summing them together:
$$R_{yy}[m] = \sigma^2 \delta[m] + \sigma^2 \delta[m+1] + \sigma^2 \delta[m-1] + \sigma^2 \delta[m]$$
$$R_{yy}[m] = 2\sigma^2 \delta[m] + \sigma^2 \delta[m-1] + \sigma^2 \delta[m+1]$$

Evaluating for specific lags:
- $R_{yy}[0] = 2\sigma^2$ (The total power is twice the input power)
- $R_{yy}[1] = R_{yy}[-1] = \sigma^2$
- $R_{yy}[m] = 0$ for $|m| > 1$

**Physical interpretation:** This is an MA(1) (Moving Average of order 1) process. Because the filter only looks back 1 sample, the "memory" of the process is strictly limited to 1 lag. Any samples separated by 2 or more steps are completely uncorrelated.

---
## 7. ENGINEERING APPLICATIONS AND CASE STUDIES

**1. Channel Equalization in Modems and Wireless Communications**
In digital communications, a transmitted signal $s[n]$ (e.g., QAM symbols) travels through a physical channel $c[n]$ (like a coaxial cable or a multipath wireless environment). The channel causes Inter-Symbol Interference (ISI) by smearing the pulses, and adds thermal noise $v[n]$. The received signal is $x[n] = s[n]*c[n] + v[n]$. 
A Wiener filter is placed at the receiver to act as an "equalizer". Its goal is to estimate a delayed version of the transmitted symbol, $d[n] = s[n-\Delta]$. By estimating the channel statistics to build the autocorrelation matrix of the received signal and the cross-correlation vector, the Wiener-Hopf equations yield the optimal tap weights to simultaneously undo the channel smear while suppressing the noise.

**2. Noise Reduction in Hearing Aids**
Modern hearing aids must separate human speech from background babble in real-time. A common approach uses a two-microphone array. The primary microphone captures the desired speech heavily corrupted by noise ($d[n] + v_1[n]$). A secondary microphone, placed slightly further away or pointing in a different direction, captures a reference signal that is mostly just correlated noise ($v_2[n]$). 
The Wiener filter takes the reference noise $v_2[n]$ as its input and attempts to estimate the noise component $v_1[n]$ at the primary microphone. This estimate is then subtracted from the primary signal. The filter dynamically adjusts to minimize the noise output, vastly improving speech intelligibility for the user.

**3. Acoustic Echo Cancellation in VoIP (Voice over IP)**
When a user speaks on a Skype or Zoom call, their voice travels to the far end, plays on a laptop speaker, and bounces around the room back into the far-end microphone. This creates an annoying delay echo for the speaker. 
An adaptive Wiener filter at the far end uses the incoming speaker signal as the reference input to predict what the microphone will pick up based on the room's acoustic impulse response. It continuously synthesizes a replica of the echo and subtracts it from the microphone return signal. Because room acoustics change, the filter taps are continuously updated using LMS algorithms aiming for the Wiener solution.

---
## 8. COMMON STUDENT MISCONCEPTIONS AND ERRORS
(List misconceptions with correct explanations)

1. **Misconception: WSS is exactly the same as Strict-Sense Stationary.**
   *Correction:* WSS is a relaxed condition. It only guarantees that the first moment (mean) and second central moment (autocorrelation) are time-invariant. Strict-sense stationarity requires the entire Probability Density Function to be invariant. We use WSS because linear systems only process the first two moments predictably.
2. **Misconception: Autocorrelation is a 2D function $R_{xx}[n_1, n_2]$.**
   *Correction:* While it starts as a 2D function of two time points, the very definition of WSS means it collapses into a 1D sequence that depends solely on the time difference $m = n_1 - n_2$. Thus we write it as $R_{xx}[m]$.
3. **Misconception: The Wiener filter completely eliminates the noise.**
   *Correction:* The Wiener filter mathematically minimizes the mean *square* error. It is a statistical compromise. It balances noise suppression against signal distortion. The output still contains some residual error; the MMSE $\xi_{min}$ is strictly greater than 0 unless the signal and noise occupy completely distinct, non-overlapping frequency bands.
4. **Misconception: The general Wiener filter is always implementable.**
   *Correction:* The elegant frequency domain formula $W_{opt}(e^{j\omega}) = S_{dx}/S_{xx}$ yields a non-causal IIR filter. It requires future samples. For real-time implementation, we *must* either solve the Wiener-Hopf matrix equations for an FIR filter, or perform complex spectral factorization to find a causal IIR filter.
5. **Misconception: The MMSE can be greater than the original signal power.**
   *Correction:* Look at the MMSE formula: $\xi_{min} = R_{dd}[0] - \mathbf{w}^T\mathbf{r}_{dx}$. Because the autocorrelation matrix $\mathbf{R}_{xx}$ is positive semi-definite, the quadratic form that represents the reduction in error is always non-negative. Therefore, the filter can never make things worse than doing nothing; the error is bounded: $0 \leq \xi_{min} \leq R_{dd}[0]$.
6. **Misconception: The phase response of a filter alters the output PSD.**
   *Correction:* Absolutely not. The relationship is $S_{yy}(e^{j\omega}) = |H(e^{j\omega})|^2 S_{xx}(e^{j\omega})$. The phase term $e^{j\angle H(e^{j\omega})}$ is annihilated by the magnitude squaring operation. The PSD destroys all phase information.
7. **Misconception: Cross-correlation is symmetric.**
   *Correction:* Many students falsely assume $R_{xy}[m] = R_{xy}[-m]$. This is incorrect. The correct property is conjugate symmetry flipped: $R_{xy}[m] = R_{yx}^*[-m]$.

---
## 9. CONNECTIONS TO OTHER LECTURES
- **What this builds on:** This lecture relies heavily on DTFT properties, LTI system analysis, and basic probability theory (Random variables, expectation, variance).
- **What future lectures depend on this:** This is the bedrock for Linear Predictive Coding (LPC) used in speech processing, Adaptive Filters (the LMS algorithm is literally a stochastic gradient descent approach to finding the Wiener-Hopf solution), and Kalman Filtering (which is essentially a recursive, time-varying extension of the Wiener filter).

---
## 10. EXAMINATION QUESTIONS

### 10.1 Short Answer (5 questions with model answers)
**Q1: What two specific mathematical conditions must a random process satisfy to be considered Wide-Sense Stationary (WSS)?**
*Model Answer:* 
1) The mean must be constant over time: $E\{x[n]\} = \mu_x$. 
2) The autocorrelation must depend only on the time lag $m$, not absolute time $n$: $E\{x[n]x^*[n-m]\} = R_{xx}[m]$.

**Q2: State the Wiener-Khinchin theorem and describe its physical significance.**
*Model Answer:* The theorem states that the Power Spectral Density (PSD) of a WSS process is the DTFT of its autocorrelation sequence: $S_{xx}(e^{j\omega}) = \sum R_{xx}[m] e^{-j\omega m}$. It physically links a signal's time-domain memory (correlation) directly to its frequency-domain power distribution.

**Q3: State the Orthogonality Principle in the context of linear estimation.**
*Model Answer:* To achieve minimum mean square error, the estimation error $e[n]$ must be statistically orthogonal to every observed data point $x[n-k]$ used to form the estimate. Mathematically: $E\{e[n]x^*[n-k]\} = 0$ for all $k$ in the filter span.

**Q4: Given the PSD $S_{xx}(e^{j\omega})$ of a signal, how do you compute its total average power?**
*Model Answer:* The total average power is found by integrating the PSD over one fundamental period ($-\pi$ to $\pi$) and dividing by $2\pi$. This is equivalent to evaluating the inverse DTFT at lag zero: $P_{avg} = R_{xx}[0] = \frac{1}{2\pi} \int_{-\pi}^{\pi} S_{xx}(e^{j\omega}) d\omega$.

**Q5: Why is the theoretically optimal filter $W(e^{j\omega}) = S_{dx}/S_{xx}$ usually not implemented in real-time hardware?**
*Model Answer:* The division in the frequency domain generally results in a two-sided, non-causal infinite impulse response (IIR) in the time domain. A non-causal filter requires knowledge of future samples, which introduces infinite delay in real-time systems.

### 10.2 Long Answer / Numerical Problems (4 problems with complete solutions)
*(Note: See Section 6 for full worked step-by-step solutions to similar numerical problems. Use these variants for exams.)*

**Problem 1:** Given a real WSS random process with autocorrelation $R_{xx}[m] = (0.8)^{|m|}$, mathematically derive the Power Spectral Density $S_{xx}(e^{j\omega})$ and prove that the PSD is always positive.

**Problem 2:** White noise with a variance of 3 is passed through an FIR filter with impulse response $h[n] = \delta[n] - 0.5\delta[n-1] + 0.25\delta[n-2]$. Calculate the exact output autocorrelation matrix of size 3x3.

**Problem 3:** Design an optimal 2-tap Wiener filter. The input autocorrelation matrix is $R_{xx} = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$ and the cross-correlation vector is $r_{dx} = \begin{bmatrix} 1 \\ -0.5 \end{bmatrix}$. Find the optimal filter weights and calculate the MMSE given that the desired signal power is $R_{dd}[0] = 3$.

**Problem 4:** An LTI system has a magnitude response $|H(e^{j\omega})| = 2$ for $|\omega| < \pi/2$ and $0$ otherwise. If the input to this system is purely white noise with a variance of 1, calculate the exact total average power of the output signal.

### 10.3 True/False with Justification (6 items)
1. **T/F: The autocorrelation matrix is always symmetric for real WSS processes.**
   *True.* For real signals, conjugate symmetry reduces to even symmetry: $R_{xx}[m] = R_{xx}[-m]$. Thus, the Toeplitz matrix is symmetric.
2. **T/F: The Wiener filter perfectly reconstructs the desired signal, eliminating all noise.**
   *False.* It only minimizes the mean square error. A residual error $\xi_{min} > 0$ always exists unless the signal and noise spectra do not overlap at all.
3. **T/F: The phase of an LTI filter significantly alters the power spectral density of its output.**
   *False.* The output PSD depends entirely on the squared magnitude $|H(e^{j\omega})|^2$. Phase information is completely lost in the PSD.
4. **T/F: Cross-correlation is an even function: $R_{xy}[m] = R_{xy}[-m]$.**
   *False.* Cross-correlation is generally not symmetric. The true relationship is $R_{xy}[m] = R_{yx}^*[-m]$.
5. **T/F: The Orthogonality Principle states that the estimated signal must be orthogonal to the data.**
   *False.* The principle states that the *error* between the true signal and the estimate must be orthogonal to the data, not the estimate itself.
6. **T/F: For ideal white noise, the Power Spectral Density is a constant value across all frequencies.**
   *True.* The autocorrelation of white noise is an impulse $R_{vv}[m] = \sigma^2 \delta[m]$. Its DTFT is the constant $\sigma^2$, indicating equal power at all frequencies.

---
## 11. KEY FORMULAS REFERENCE
(Comprehensive table — every formula needed for this topic)

| Concept | Mathematical Formula | Description |
| :--- | :--- | :--- |
| **Mean of WSS Process** | $\mu_x = E\{x[n]\}$ | Must be constant over time. |
| **Autocorrelation** | $R_{xx}[m] = E\{x[n]x^*[n-m]\}$ | Measures signal memory over lag $m$. |
| **Total Average Power** | $P_{avg} = R_{xx}[0] = E\{\|x[n]\|^2\}$ | Power is the zero-lag autocorrelation. |
| **Cross-Correlation** | $R_{xy}[m] = E\{x[n+m]y^*[n]\}$ | Relates two jointly WSS processes. |
| **Wiener-Khinchin Theorem** | $S_{xx}(e^{j\omega}) = \sum_{m=-\infty}^{\infty} R_{xx}[m] e^{-j\omega m}$ | Links autocorrelation to PSD via DTFT. |
| **Inverse PSD** | $R_{xx}[m] = \frac{1}{2\pi} \int_{-\pi}^{\pi} S_{xx}(e^{j\omega}) e^{j\omega m} d\omega$ | Recovers correlation from spectrum. |
| **LTI Output Autocorrelation**| $R_{yy}[m] = h[m] * h^*[-m] * R_{xx}[m]$ | Autocorrelation transformed by system. |
| **LTI Output PSD** | $S_{yy}(e^{j\omega}) = \|H(e^{j\omega})\|^2 S_{xx}(e^{j\omega})$ | Spectrum shaped by squared magnitude. |
| **Orthogonality Principle**| $E\{e[n] x^*[n-k]\} = 0$ | Error must be orthogonal to data used. |
| **Wiener-Hopf Equations** | $\mathbf{R}_{xx} \mathbf{w}_{opt} = \mathbf{r}_{dx}$ | Matrix system for optimal FIR weights. |
| **Minimum MSE (MMSE)** | $\xi_{min} = R_{dd}[0] - \mathbf{w}_{opt}^T \mathbf{r}_{dx}$ | Minimum achievable error variance. |
| **Non-Causal Wiener Filter** | $W_{opt}(e^{j\omega}) = \frac{S_{dx}(e^{j\omega})}{S_{xx}(e^{j\omega})}$ | Unconstrained optimal frequency response. |

---
## 12. FURTHER READING AND REFERENCES
To deepen understanding, direct students to the following classic texts:
- **Proakis, J. G., & Manolakis, D. G.** (2006). *Digital Signal Processing: Principles, Algorithms, and Applications* (4th ed.). Pearson. (Specifically, Chapter 12 on Statistical Signal Processing provides excellent foundational reading).
- **Oppenheim, A. V., & Schafer, R. W.** (2010). *Discrete-Time Signal Processing* (3rd ed.). Pearson. (Review the detailed sections on Random Signals and introduction to Wiener Filtering).
- **Haykin, S.** (2013). *Adaptive Filter Theory* (5th ed.). Pearson. (Chapters 1 & 2 are highly recommended for a mathematically rigorous treatment of the Wiener-Hopf equations and the geometric interpretation of the orthogonality principle).
- **Hayes, M. H.** (1996). *Statistical Digital Signal Processing and Modeling*. Wiley. (A gold standard text entirely dedicated to this topic, with extensive MATLAB examples).
</Faculty Notes — Lecture 15: Power Spectral Density & Wiener Filter>
