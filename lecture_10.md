# Lecture 10: FIR Filter Design — Window Method

**Course:** EE3621 — Digital Signal Processing  
**Target Audience:** III B.Tech EEE Students  
**Duration:** 40 Minutes  

* **Available Formats:** [LaTeX Source File](file:///C:/Users/sriph/Downloads/DSP/lecture_10.tex) | [Compiled PDF Notes](file:///C:/Users/sriph/Downloads/DSP/lecture_10.pdf)

---

## 1. Lecture Plan (40 Minutes Breakdown)

* **00:00 – 05:00 (5 mins):** Introduction to FIR vs IIR trade-offs and the concept of linear phase.
* **05:00 – 12:00 (7 mins):** Linear phase conditions for FIR filters and group delay.
* **12:00 – 20:00 (8 mins):** Ideal frequency responses and derivation of the ideal impulse response (LPF).
* **20:00 – 25:00 (5 mins):** The problem of truncation and introduction of the Window Method.
* **25:00 – 32:00 (7 mins):** Common window types and their specifications (Rectangular, Hanning, Hamming, Blackman, Kaiser).
* **32:00 – 36:00 (4 mins):** Step-by-step design procedure.
* **36:00 – 40:00 (4 mins):** Worked Example: 21-tap Hamming-windowed LPF and Checkpoint Questions.

---

## 2. FIR vs IIR Trade-offs

When designing digital filters, we primarily choose between Infinite Impulse Response (IIR) and Finite Impulse Response (FIR) filters. Understanding the trade-offs is crucial for practical engineering applications.

### 2.1. FIR Filter Advantages
* **Strictly Linear Phase:** FIR filters can be designed to have exact linear phase. This is impossible for stable, causal IIR filters. Linear phase means that all frequency components experience the same time delay (group delay), which prevents phase distortion. This is essential in applications like audio processing, data transmission, and biomedical signal processing (e.g., ECG).
* **Inherent Stability:** Because the impulse response is finite, the output is a finite sum of past and present inputs. There is no feedback loop. The poles of the transfer function are always located at the origin ($z=0$) in the z-plane, guaranteeing bounded-input bounded-output (BIBO) stability.
* **Implementation Simplicity:** FIR filters can be implemented efficiently using fast convolution (FFT) or specialized DSP multiply-accumulate (MAC) hardware, even taking advantage of coefficient symmetry.

### 2.2. FIR Filter Disadvantages
* **Higher Order Requirement:** To achieve the same magnitude specifications (selectivity, narrow transition band) as an IIR filter, an FIR filter typically requires a much higher order (sometimes $5$ to $10$ times higher). This implies more memory for coefficients and more computations per output sample.

---

## 3. Linear Phase Condition in FIR Filters

An FIR filter has a transfer function:
$$ H(z) = \sum_{n=0}^{M-1} h[n] z^{-n} $$
where $M$ is the filter length (number of taps), and the order is $N = M - 1$.

### 3.1. Symmetry and Antisymmetry
A causal FIR filter possesses exact linear phase if its impulse response $h[n]$ satisfies one of the following conditions:
* **Symmetric:** $h[n] = h[M - 1 - n]$
* **Antisymmetric:** $h[n] = -h[M - 1 - n]$

When these conditions are met, the frequency response $H(e^{j\omega})$ can be expressed as:
$$ H(e^{j\omega}) = A(\omega) e^{-j\alpha \omega} e^{j\beta} $$
where $A(\omega)$ is a real-valued amplitude function, $\alpha = \frac{M-1}{2}$ is the group delay, and $\beta$ is a phase offset (either $0$ or $\pi/2$).

### 3.2. Four Types of Linear Phase FIR Filters
Depending on the symmetry and whether the length $M$ is odd or even, there are four types:
1. **Type I:** Symmetric, $M$ odd. Can design any filter type (LPF, HPF, BPF, BSF).
2. **Type II:** Symmetric, $M$ even. Has a zero at $\omega = \pi$. Cannot be used for Highpass or Bandstop filters.
3. **Type III:** Antisymmetric, $M$ odd. Has zeros at $\omega = 0$ and $\omega = \pi$. Only suitable for Bandpass and Differentiators.
4. **Type IV:** Antisymmetric, $M$ even. Has a zero at $\omega = 0$. Suitable for Highpass and Differentiators.

---

## 4. Ideal Frequency Responses

Before designing a practical filter, we must define the mathematical goal: the ideal filter.

### 4.1. Mathematical Definitions
An ideal filter perfectly passes a specified range of frequencies and completely blocks others. The four basic types are defined over one period $-\pi \le \omega \le \pi$:

**1. Ideal Lowpass Filter (LPF):**
$$ H_d(e^{j\omega}) = \begin{cases} 1, & |\omega| \le \omega_c \\ 0, & \omega_c < |\omega| \le \pi \end{cases} $$

**2. Ideal Highpass Filter (HPF):**
$$ H_d(e^{j\omega}) = \begin{cases} 0, & |\omega| < \omega_c \\ 1, & \omega_c \le |\omega| \le \pi \end{cases} $$

**3. Ideal Bandpass Filter (BPF):**
$$ H_d(e^{j\omega}) = \begin{cases} 1, & \omega_{c1} \le |\omega| \le \omega_{c2} \\ 0, & \text{otherwise} \end{cases} $$

**4. Ideal Bandstop Filter (BSF):**
$$ H_d(e^{j\omega}) = \begin{cases} 0, & \omega_{c1} < |\omega| < \omega_{c2} \\ 1, & \text{otherwise} \end{cases} $$

---

## 5. Ideal Impulse Response (Ideal LPF)

Let's derive the impulse response $h_d[n]$ of the ideal Lowpass Filter using the Inverse Discrete-Time Fourier Transform (IDTFT).

### 5.1. IDTFT Derivation
The IDTFT formula is:
$$ h_d[n] = \frac{1}{2\pi} \int_{-\pi}^{\pi} H_d(e^{j\omega}) e^{j\omega n} d\omega $$

Substitute the ideal LPF definition:
$$ h_d[n] = \frac{1}{2\pi} \int_{-\omega_c}^{\omega_c} 1 \cdot e^{j\omega n} d\omega $$
$$ h_d[n] = \frac{1}{2\pi} \left[ \frac{e^{j\omega n}}{jn} \right]_{-\omega_c}^{\omega_c} $$
$$ h_d[n] = \frac{1}{2\pi j n} \left( e^{j\omega_c n} - e^{-j\omega_c n} \right) $$

Using Euler's identity $\sin(\theta) = \frac{e^{j\theta} - e^{-j\theta}}{2j}$:
$$ h_d[n] = \frac{\sin(\omega_c n)}{\pi n}, \quad \text{for } n \neq 0 $$

For $n = 0$, applying L'Hôpital's rule or direct integration yields:
$$ h_d[0] = \frac{\omega_c}{\pi} $$

### 5.2. Causality and Realizability
The derived impulse response $h_d[n] = \frac{\sin(\omega_c n)}{\pi n}$ extends from $n = -\infty$ to $n = \infty$. 
* **Non-causal:** It has non-zero values for $n < 0$, which means the system would need to look into the future to process real-time data.
* **Infinite length:** It cannot be computed in finite time or stored in finite memory.

Therefore, the ideal LPF is physically unrealizable. 

---

## 6. Truncation and the Windowing Method

To make the filter physically realizable, we must truncate $h_d[n]$ to a finite length $M$. Simple abrupt truncation (setting $h_d[n] = 0$ outside a range) is equivalent to multiplying by a rectangular window, which causes severe oscillations in the frequency response, known as the **Gibbs Phenomenon**.

### 6.1. The Windowing Concept
Instead of abrupt truncation, we multiply the infinite impulse response $h_d[n]$ by a finite-duration window function $w[n]$ that smoothly tapers to zero at both ends.

To ensure causality, we first shift the ideal impulse response to the right by $\alpha = \frac{M-1}{2}$ samples, so that it is centered at $\alpha$ rather than $0$.

The final causal FIR filter coefficients are:
$$ h[n] = h_d\left[n - \frac{M-1}{2}\right] \cdot w[n], \quad 0 \le n \le M-1 $$
where $h_d[n - \alpha]$ is the delayed ideal impulse response.

---

## 7. Window Types with Specifications

Different window functions offer different trade-offs between the mainlobe width (which determines the transition bandwidth) and the sidelobe level (which determines stopband attenuation). Let $N = M - 1$ be the filter order.

### 7.1. Rectangular Window
* $w[n] = 1, \quad 0 \le n \le M-1$
* **Mainlobe width:** $\frac{4\pi}{M}$ (or approximately $\frac{4\pi}{N}$)
* **Peak Sidelobe:** $-13$ dB
* **Characteristics:** Sharpest transition, but worst stopband attenuation.

### 7.2. Hanning Window
* $w[n] = 0.5 - 0.5 \cos\left(\frac{2\pi n}{M-1}\right), \quad 0 \le n \le M-1$
* **Mainlobe width:** $\frac{8\pi}{M}$
* **Peak Sidelobe:** $-31$ dB

### 7.3. Hamming Window
* $w[n] = 0.54 - 0.46 \cos\left(\frac{2\pi n}{M-1}\right), \quad 0 \le n \le M-1$
* **Mainlobe width:** $\frac{8\pi}{M}$
* **Peak Sidelobe:** $-41$ dB
* **Characteristics:** Optimized coefficients to cancel the first sidelobe of the Hanning window.

### 7.4. Blackman Window
* $w[n] = 0.42 - 0.5 \cos\left(\frac{2\pi n}{M-1}\right) + 0.08 \cos\left(\frac{4\pi n}{M-1}\right)$
* **Mainlobe width:** $\frac{12\pi}{M}$
* **Peak Sidelobe:** $-57$ dB
* **Characteristics:** Excellent stopband attenuation, but wide transition band.

### 7.5. Kaiser Window
The Kaiser window allows a continuous trade-off between mainlobe width and sidelobe level via a parameter $\beta$.
* $w[n] = \frac{I_0\left(\beta \sqrt{1 - \left(\frac{n - \alpha}{\alpha}\right)^2}\right)}{I_0(\beta)}$
where $I_0$ is the zeroth-order modified Bessel function of the first kind.

Given a required stopband attenuation $A_s$ (in positive dB) and a transition bandwidth $\Delta\omega = \omega_s - \omega_p$:
**1. Compute $\beta$:**
$$ \beta = \begin{cases} 0.1102(A_s - 8.7), & A_s > 50 \\ 0.5842(A_s - 21)^{0.4} + 0.07886(A_s - 21), & 21 \le A_s \le 50 \\ 0.0, & A_s < 21 \end{cases} $$

**2. Compute Filter Length $M$:**
$$ M \ge \frac{A_s - 7.95}{2.285 \Delta\omega} + 1 $$

---

## 8. Design Procedure Step-by-Step

**Step 1: Determine specifications**
Identify passband frequency $\omega_p$, stopband frequency $\omega_s$, passband ripple $\delta_p$, and stopband attenuation $\delta_s$ (or $A_s$ in dB).

**Step 2: Select the appropriate window**
Convert $\delta_s$ to dB: $A_s = -20 \log_{10}(\delta_s)$. Choose a window that guarantees peak sidelobe level $< -A_s$.

**Step 3: Compute the required filter length $M$**
Calculate the transition bandwidth $\Delta\omega = \omega_s - \omega_p$. Use the mainlobe width formula of the chosen window to find $M$. For example, for Hamming: $\frac{8\pi}{M} \le \Delta\omega \implies M \ge \frac{8\pi}{\Delta\omega}$. Round up to an integer (often making $M$ odd for a Type I filter).

**Step 4: Compute the ideal impulse response**
Define the cutoff frequency $\omega_c = \frac{\omega_p + \omega_s}{2}$.
Write the formula for $h_d[n]$ shifted by $\alpha = \frac{M-1}{2}$:
$$ h_d[n - \alpha] = \frac{\sin(\omega_c (n - \alpha))}{\pi (n - \alpha)} $$

**Step 5: Compute the window function $w[n]$**
Evaluate the chosen window equation for $0 \le n \le M-1$.

**Step 6: Multiply and finalize**
Multiply the delayed ideal impulse response by the window:
$$ h[n] = h_d[n - \alpha] \cdot w[n] $$

**Step 7: Verify symmetry**
Check that $h[n] = h[M - 1 - n]$ to confirm linear phase.

---

## 9. Worked Example: 21-tap Hamming-windowed LPF

**Problem:** Design a 21-tap causal FIR Lowpass Filter with cutoff frequency $\omega_c = 0.4\pi$ using a Hamming window.

**Solution:**

**1. Given parameters:**
* $M = 21$
* $\omega_c = 0.4\pi$
* Delay $\alpha = \frac{M - 1}{2} = \frac{21 - 1}{2} = 10$.

**2. Delayed ideal impulse response:**
$$ h_d[n - 10] = \frac{\sin(0.4\pi (n - 10))}{\pi (n - 10)} \quad \text{for } n \neq 10 $$
For $n = 10$, using L'Hôpital's rule:
$$ h_d[0] = \frac{0.4\pi}{\pi} = 0.4 $$

**3. Hamming window function:**
$$ w[n] = 0.54 - 0.46 \cos\left(\frac{2\pi n}{20}\right), \quad 0 \le n \le 20 $$

**4. Compute the filter coefficients $h[n]$:**
$$ h[n] = h_d[n - 10] \cdot w[n] $$

Let's compute a few specific coefficients:

* **For $n = 10$ (Center tap):**
  $w[10] = 0.54 - 0.46 \cos\left(\frac{20\pi}{20}\right) = 0.54 - 0.46(-1) = 1.0$
  $h[10] = 0.4 \times 1.0 = 0.4$

* **For $n = 9$ and $n = 11$ (Symmetry check):**
  $h_d[-1] = \frac{\sin(-0.4\pi)}{-\pi} = \frac{\sin(0.4\pi)}{\pi} \approx 0.3027$
  $w[9] = 0.54 - 0.46 \cos\left(\frac{18\pi}{20}\right) \approx 0.54 - 0.46(-0.951) \approx 0.9775$
  $h[9] = 0.3027 \times 0.9775 \approx 0.2959$
  By symmetry, $h[11] = h[9] \approx 0.2959$.

* **For $n = 0$ (Edge tap):**
  $h_d[-10] = \frac{\sin(-4\pi)}{-10\pi} = 0$
  $h[0] = 0$ (Since the sine term evaluates to zero).

This confirms the symmetry $h[n] = h[20-n]$, ensuring strictly linear phase.

---

## 10. Table of Key Formulas

| Concept | Formula | Notes |
| :--- | :--- | :--- |
| Ideal LPF $h_d[n]$ | $\frac{\sin(\omega_c n)}{\pi n}$ | Non-causal, infinite length |
| Group Delay $\alpha$ | $\frac{M-1}{2}$ | Center of symmetry |
| Causal FIR $h[n]$ | $h_d[n-\alpha] \cdot w[n]$ | Windowed and shifted |
| Transition Band $\Delta\omega$ | $\omega_s - \omega_p$ | Determines required $M$ |
| Linear Phase Cond. | $h[n] = \pm h[M-1-n]$ | Symmetric or Antisymmetric |

---

## 11. Checkpoint Questions

1. **Q1: Why is an ideal Lowpass filter physically unrealizable?**
   * *Answer:* 
     * The impulse response of an ideal LPF is a sinc function $h_d[n] = \frac{\sin(\omega_c n)}{\pi n}$.
     * This function extends to $-\infty$, meaning it has non-zero values for $n < 0$. A system is causal (and thus physically realizable in real-time) only if $h[n] = 0$ for $n < 0$.
     * Furthermore, the impulse response extends to $+\infty$, meaning it requires infinite memory and infinite summation to compute each output sample.
     * To make it realizable, we must truncate it and shift it to the right (introducing delay).

2. **Q2: Given a requirement for a stopband attenuation of 50 dB and a transition bandwidth of $0.05\pi$, which fixed window would you choose and what is the minimum required length $M$?**
   * *Answer:* 
     * The required stopband attenuation is $A_s = 50$ dB.
     * Rectangular (-13 dB), Hanning (-31 dB), and Hamming (-41 dB) all fail to meet the 50 dB requirement.
     * The Blackman window provides -57 dB of attenuation, which is sufficient.
     * The mainlobe width for Blackman is $\frac{12\pi}{M}$.
     * Setting $\frac{12\pi}{M} \le \Delta\omega = 0.05\pi$:
       $$ M \ge \frac{12\pi}{0.05\pi} = \frac{12}{0.05} = 240 $$
     * Therefore, we choose the Blackman window with a minimum length of $M = 240$. (Often we use $M = 241$ to get a Type I filter).

3. **Q3: Prove that an FIR filter with a symmetric impulse response $h[n] = h[M-1-n]$ has linear phase.**
   * *Answer:* 
     * The frequency response is $H(e^{j\omega}) = \sum_{n=0}^{M-1} h[n] e^{-j\omega n}$.
     * We can pull out a phase factor corresponding to the group delay $\alpha = \frac{M-1}{2}$:
       $$ H(e^{j\omega}) = e^{-j\omega \alpha} \sum_{n=0}^{M-1} h[n] e^{-j\omega (n - \alpha)} $$
     * Let $k = n - \alpha$. The summation limits go from $-\alpha$ to $\alpha$:
       $$ \sum_{k=-\alpha}^{\alpha} h[k + \alpha] e^{-j\omega k} $$
     * Due to the symmetry condition $h[n] = h[M-1-n]$, we have $h[k + \alpha] = h[-k + \alpha]$.
     * Thus, terms for $k$ and $-k$ can be paired: $h[k+\alpha] (e^{-j\omega k} + e^{j\omega k}) = 2 h[k+\alpha] \cos(\omega k)$.
     * Since cosine is purely real, the entire summation becomes a purely real amplitude function $A(\omega)$.
     * Therefore, $H(e^{j\omega}) = A(\omega) e^{-j\omega \alpha}$, which has a strictly linear phase of $-\alpha \omega$.
