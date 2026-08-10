# Lecture 4: Frequency Response, Magnitude/Phase & Group Delay of LTI Systems

**Course:** EE3621 — Digital Signal Processing  
**Target Audience:** III B.Tech EEE Students  
**Duration:** 40 Minutes  

* **Available Formats:** [LaTeX Source File](file:///C:/Users/sriph/Downloads/DSP/lecture_04.tex) | [Compiled PDF Notes](file:///C:/Users/sriph/Downloads/DSP/lecture_04.pdf)

---

## 1. Lecture Plan (40 Minutes Breakdown)
* **00:00 – 08:00 (8 mins):** LTI Eigenfunctions: Why complex exponentials are unique. Derivation of $H(e^{j\omega})$.
* **08:00 – 15:00 (7 mins):** Magnitude \& Phase responses, Rectangular vs. Polar forms.
* **15:00 – 25:00 (10 mins):** Phase Delay vs. Group Delay. Narrowband input derivation (Carrier vs. Envelope delay).
* **25:00 – 35:00 (10 mins):** First-order IIR Filter Example: Detailed algebraic derivation of Group Delay.
* **35:00 – 40:00 (5 mins):** Checkpoints \& Concept Recap.

---

## 2. Eigenfunctions \& The Frequency Response

In linear system analysis, **complex exponentials are eigenfunctions of LTI systems**. An eigenfunction of an operator is a function that, when applied to the operator, yields the same function scaled by a constant (the eigenvalue).

### Derivation
Let the input to a discrete-time LTI system be a complex exponential:
$$x[n] = e^{j\omega n} \quad \forall n$$
The system output $y[n]$ is computed via the convolution sum:
$$y[n] = \sum_{k=-\infty}^{\infty} h[k] x[n-k] = \sum_{k=-\infty}^{\infty} h[k] e^{j\omega(n-k)}$$
We can factor out the term $e^{j\omega n}$ since the summation index is $k$:
$$y[n] = e^{j\omega n} \sum_{k=-\infty}^{\infty} h[k] e^{-j\omega k}$$
Notice that the output $y[n]$ is the original input $e^{j\omega n}$ multiplied by a complex scalar factor. Let's denote this complex scalar factor (eigenvalue) as the **Frequency Response** $H(e^{j\omega})$:
$$y[n] = H(e^{j\omega}) e^{j\omega n}$$
where:
$$H(e^{j\omega}) = \sum_{k=-\infty}^{\infty} h[k] e^{-j\omega k}$$
* **Significance:** This derivation shows that LTI systems do not alter the frequency $\omega$ of a complex exponential input. They only scale its magnitude and shift its phase.

---

## 3. Magnitude \& Phase Responses

Since $H(e^{j\omega})$ is a complex-valued function of $\omega$, it can be represented in either rectangular or polar coordinates:

### A. Rectangular Form
$$H(e^{j\omega}) = H_R(e^{j\omega}) + j H_I(e^{j\omega})$$
where $H_R(e^{j\omega})$ and $H_I(e^{j\omega})$ are the real and imaginary parts of the frequency response.

### B. Polar Form
$$H(e^{j\omega}) = \left| H(e^{j\omega}) \right| e^{j \theta(\omega)}$$
* **Magnitude Response $|H(e^{j\omega})|$**: Represents the frequency-dependent gain of the system:
  $$\left| H(e^{j\omega}) \right| = \sqrt{H_R^2(e^{j\omega}) + H_I^2(e^{j\omega})}$$
* **Phase Response $\theta(\omega) = \angle H(e^{j\omega})$**: Represents the phase shift introduced by the system:
  $$\theta(\omega) = \arctan\left( \frac{H_I(e^{j\omega})}{H_R(e^{j\omega})} \right)$$

If the input is a real sinusoid $x[n] = A \cos(\omega_0 n + \phi)$, the output is:
$$y[n] = A \left| H(e^{j\omega_0}) \right| \cos\left( \omega_0 n + \phi + \theta(\omega_0) \right)$$

Below is a visualization showing the frequency response of a 1st-order low-pass filter vs. a high-pass filter:

![Frequency Response LPF vs HPF](images/frequency_response_lpf_hpf.png)

---

## 4. Phase Delay vs. Group Delay

When a multi-frequency signal passes through an LTI system, different frequency components experience different delays. We categorize these delays into **Phase Delay** and **Group Delay**.

### A. Mathematical Definitions
* **Phase Delay ($\tau_p(\omega)$)**: The time delay experienced by an individual sinusoidal carrier component:
  $$\tau_p(\omega) = -\frac{\theta(\omega)}{\omega}$$
* **Group Delay ($\tau_g(\omega)$)**: The time delay experienced by the envelope of a narrowband signal (wave packet):
  $$\tau_g(\omega) = -\frac{d\theta(\omega)}{d\omega}$$

### B. Narrowband Signal Propagation (Physical Interpretation)
To see why $\tau_p(\omega)$ and $\tau_g(\omega)$ represent carrier and envelope delay respectively, consider a narrowband input signal:
$$x[n] = s[n] \cos(\omega_0 n)$$
where $s[n]$ is a slowly varying envelope (low bandwidth) modulating a carrier at frequency $\omega_0$.
Assuming the system phase response is approximately linear around $\omega_0$, we expand $\theta(\omega)$ using a first-order Taylor series:
$$\theta(\omega) \approx \theta(\omega_0) + \theta'(\omega_0)(\omega - \omega_0)$$
Substituting the definitions of $\tau_p(\omega_0)$ and $\tau_g(\omega_0)$:
$$\theta(\omega) \approx -\omega_0 \tau_p(\omega_0) - \tau_g(\omega_0)(\omega - \omega_0)$$
When $x[n]$ passes through the system, the output envelope is delayed by the group delay, and the carrier is delayed by the phase delay:
$$y[n] \approx \left| H(e^{j\omega_0}) \right| s[n - \tau_g(\omega_0)] \cos\left( \omega_0(n - \tau_p(\omega_0)) \right)$$
* **Linear Phase and Distortionless Transmission**:
  If the phase response is exactly linear: $\theta(\omega) = -\alpha \omega$, then:
  $$\tau_p(\omega) = \alpha \quad \text{and} \quad \tau_g(\omega) = \alpha \text{ samples}$$
  This constant delay across all frequencies ensures that the entire signal waveform (carrier and envelope) is delayed by the same amount, resulting in **distortionless transmission**.

Below is a comparison of group delay for two different pole values:

![Group Delay Analysis](images/group_delay_analysis.png)

---

## 5. Group Delay Derivation for First-Order Filter

Consider a first-order filter described by the difference equation:
$$y[n] - r y[n-1] = x[n] \quad \text{with } |r| < 1$$
We derive its group delay $\tau_g(\omega)$:
1. **Frequency Response:**
   $$H(e^{j\omega}) = \frac{1}{1 - r e^{-j\omega}} = \frac{1}{1 - r\cos\omega + j r\sin\omega}$$
2. **Phase Response:**
   $$\theta(\omega) = -\arctan\left( \frac{r\sin\omega}{1 - r\cos\omega} \right)$$
3. **Calculating Group Delay $\tau_g(\omega) = -\frac{d\theta(\omega)}{d\omega}$:**
   Let $u(\omega) = \frac{r\sin\omega}{1 - r\cos\omega}$. Recall that $\frac{d}{d\omega} \arctan(u) = \frac{1}{1 + u^2} \frac{du}{d\omega}$.
   * Step 3.1: Calculate $\frac{du}{d\omega}$ using the quotient rule:
     $$\frac{du}{d\omega} = \frac{(r\cos\omega)(1-r\cos\omega) - (r\sin\omega)(r\sin\omega)}{(1-r\cos\omega)^2} = \frac{r\cos\omega - r^2(\cos^2\omega + \sin^2\omega)}{(1-r\cos\omega)^2} = \frac{r\cos\omega - r^2}{(1-r\cos\omega)^2}$$
   * Step 3.2: Calculate $1 + u^2$:
     $$1 + u^2 = 1 + \frac{r^2\sin^2\omega}{(1-r\cos\omega)^2} = \frac{(1-r\cos\omega)^2 + r^2\sin^2\omega}{(1-r\cos\omega)^2} = \frac{1 + r^2\cos^2\omega - 2r\cos\omega + r^2\sin^2\omega}{(1-r\cos\omega)^2} = \frac{1 + r^2 - 2r\cos\omega}{(1-r\cos\omega)^2}$$
   * Step 3.3: Combine steps:
     $$\frac{d\theta(\omega)}{d\omega} = - \frac{1}{1+u^2} \frac{du}{d\omega} = - \left[ \frac{(1-r\cos\omega)^2}{1 + r^2 - 2r\cos\omega} \right] \cdot \left[ \frac{r\cos\omega - r^2}{(1-r\cos\omega)^2} \right] = -\frac{r\cos\omega - r^2}{1 + r^2 - 2r\cos\omega}$$
   * Step 3.4: Since $\tau_g(\omega) = -\frac{d\theta(\omega)}{d\omega}$:
     $$\tau_g(\omega) = \frac{r\cos\omega - r^2}{1 + r^2 - 2r\cos\omega}$$

---

## 6. Checkpoint \& Quick Review Questions

1. **Q1:** Find the group delay of a system with impulse response $h[n] = \delta[n - N_0]$.
   * *Answer:* 
     Frequency response is $H(e^{j\omega}) = e^{-j\omega N_0}$.
     The phase response is $\theta(\omega) = -N_0\omega$.
     The group delay is $\tau_g(\omega) = -\frac{d\theta(\omega)}{d\omega} = -\frac{d}{d\omega}(-N_0\omega) = N_0$ samples.
     This constant delay represents a distortionless phase shift.

2. **Q2:** For a first-order system with pole $r = 0.9$, calculate the group delay at $\omega = 0$.
   * *Answer:* 
     Evaluate $\tau_g(\omega)$ at $\omega = 0$:
     $$\tau_g(0) = \frac{r\cos(0) - r^2}{1 + r^2 - 2r\cos(0)} = \frac{r - r^2}{1 + r^2 - 2r} = \frac{r(1-r)}{(1-r)^2} = \frac{r}{1 - r}$$
     For $r = 0.9$:
     $$\tau_g(0) = \frac{0.9}{1 - 0.9} = \frac{0.9}{0.1} = 9\text{ samples}$$
     This filter delays low frequencies near the pole frequency by exactly 9 samples.
