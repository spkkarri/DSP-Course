# Lecture 28: Bilinear Transformation (BLT) Method
## EE3621: Digital Signal Processing | III B.Tech EEE

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Derive** the Bilinear Transformation algebraic mapping and frequency warping relation.
2. **Prewarp** digital filter specifications into continuous analog frequencies.
3. **Design** Butterworth and Chebyshev IIR digital filters using the Bilinear Transformation.
4. **Compare** the Bilinear Transformation with the Impulse Invariance method.

---
## 2. MATHEMATICAL FOUNDATIONS

### 2.1 Derivation via Trapezoidal Integration
Consider the first-order differential equation $\frac{dy(t)}{dt} = x(t)$. Integrating over $[(n-1)T_d, n T_d]$ using the trapezoidal rule:
$$ y(n T_d) - y((n-1)T_d) = \int_{(n-1)T_d}^{n T_d} x(t) dt \approx \frac{T_d}{2} [x(n T_d) + x((n-1)T_d)] $$
In discrete notation:
$$ y[n] - y[n-1] = \frac{T_d}{2} [x[n] + x[n-1]] $$
Taking the Z-Transform:
$$ Y(z)(1 - z^{-1}) = \frac{T_d}{2} X(z)(1 + z^{-1}) \implies H(z) = \frac{Y(z)}{X(z)} = \frac{T_d}{2} \frac{1 + z^{-1}}{1 - z^{-1}} $$
Since the analog integrator transfer function is $H_a(s) = \frac{1}{s}$, equating $H_a(s) = H(z)$ yields:
$$ \mathbf{s = \frac{2}{T_d} \frac{1 - z^{-1}}{1 + z^{-1}} = \frac{2}{T_d} \frac{z - 1}{z + 1}} $$

### 2.2 Frequency Warping and Prewarping
Substitute $s = j\Omega$ and $z = e^{j\omega}$:
$$ j\Omega = \frac{2}{T_d} \frac{1 - e^{-j\omega}}{1 + e^{-j\omega}} = \frac{2}{T_d} \frac{e^{j\omega/2} - e^{-j\omega/2}}{e^{j\omega/2} + e^{-j\omega/2}} = j \frac{2}{T_d} \tan\left( \frac{\omega}{2} \right) $$
$$ \mathbf{\Omega = \frac{2}{T_d} \tan\left( \frac{\omega}{2} \right)} $$
* **Prewarping Formulas:**
  $$ \Omega_p = \frac{2}{T_d} \tan\left( \frac{\omega_p}{2} \right), \qquad \Omega_s = \frac{2}{T_d} \tan\left( \frac{\omega_s}{2} \right) $$

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 28.1: 1st-Order Lowpass Filter via BLT
**Problem:** Design a digital lowpass filter with a 3-dB cutoff frequency $\omega_c = 0.2\pi \text{ rad/sample}$ from an analog prototype $H_a(s) = \frac{\Omega_c}{s + \Omega_c}$ using the Bilinear Transformation ($T_d = 1\text{ s}$).

**Solution:**
1. **Prewarp the Cutoff Frequency:**
   $$ \Omega_c = \frac{2}{T_d} \tan\left( \frac{\omega_c}{2} \right) = \frac{2}{1} \tan(0.1\pi) = 2 \times 0.3249 = 0.6498 \text{ rad/s} $$
2. **Analog Transfer Function:**
   $$ H_a(s) = \frac{0.6498}{s + 0.6498} $$
3. **Apply Bilinear Transformation ($s = 2 \frac{1 - z^{-1}}{1 + z^{-1}}$):**
   $$ H(z) = \left. \frac{0.6498}{s + 0.6498} \right|_{s = 2 \frac{1 - z^{-1}}{1 + z^{-1}}} = \frac{0.6498}{2 \frac{1 - z^{-1}}{1 + z^{-1}} + 0.6498} = \frac{0.6498(1 + z^{-1})}{2(1 - z^{-1}) + 0.6498(1 + z^{-1})} $$
   $$ H(z) = \frac{0.6498 + 0.6498 z^{-1}}{(2 + 0.6498) + (-2 + 0.6498) z^{-1}} = \frac{0.6498(1 + z^{-1})}{2.6498 - 1.3502 z^{-1}} = \frac{0.2452(1 + z^{-1})}{1 - 0.5095 z^{-1}} $$
4. **Verification:**
   * At DC ($\omega = 0, z = 1$): $H(1) = \frac{0.2452(2)}{1 - 0.5095} = \frac{0.4904}{0.4905} \approx 1.0$ (0 dB).
   * At half-sampling ($\omega = \pi, z = -1$): $H(-1) = \frac{0.2452(0)}{1 + 0.5095} = 0$ ($-\infty$ dB).

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
**(a)** Derive the Bilinear Transformation and the frequency warping equation. Explain the necessity of prewarping. *(8 Marks)*
**(b)** Design a digital Butterworth lowpass filter satisfying:
* $0.8 \le |H(e^{j\omega})| \le 1.0$ for $0 \le \omega \le 0.2\pi$
* $|H(e^{j\omega})| \le 0.2$ for $0.6\pi \le \omega \le \pi$
Use Bilinear Transformation with $T_d = 1\text{ s}$. *(7 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Part (a):**
  * Trapezoidal derivation of $s = \frac{2}{T_d}\frac{1-z^{-1}}{1+z^{-1}}$ *(4 Marks)*
  * Warping derivation $\Omega = \frac{2}{T_d}\tan(\omega/2)$ and prewarping explanation *(4 Marks)*
* **Part (b):**
  * Prewarp: $\Omega_p = 2\tan(0.1\pi) = 0.6498, \; \Omega_s = 2\tan(0.3\pi) = 2.7528$ *(2 Marks)*
  * Specs: $A_p = -20\log_{10}(0.8) = 1.9382\text{ dB}, \; A_s = -20\log_{10}(0.2) = 13.9794\text{ dB}$ *(1 Mark)*
  * Order calculation: $N \ge \frac{\log_{10}[(10^{1.398}-1)/(10^{0.1938}-1)]}{2\log_{10}(2.7528/0.6498)} = \frac{\log_{10}(24/0.5623)}{2\log_{10}(4.236) } = \frac{1.6303}{1.254} = 1.30 \implies \mathbf{N = 2}$ *(2 Marks)*
  * Synthesize 2nd-order Butterworth $H_a(s)$ and substitute $s \to 2\frac{1-z^{-1}}{1+z^{-1}}$ *(2 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import scipy.signal as signal

# Butterworth BLT design
b, a = signal.butter(2, 0.2, btype='low', analog=False)
print("Digital Filter b:", np.round(b, 4))
print("Digital Filter a:", np.round(a, 4))
```
