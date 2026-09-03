# Lecture 29: Matched Z-Transform & Spectral Transformations
## EE3621: Digital Signal Processing | III B.Tech EEE

---
## 1. LEARNING OBJECTIVES
By the end of this lecture, students will be able to:
1. **Apply** the Matched Z-Transform to convert analog transfer functions to discrete transfer functions.
2. **Transform** lowpass digital filter prototypes into highpass, bandpass, and bandstop filters using Constantinides formulas.
3. **Calculate** the mapping parameter $\alpha$ from prototype and target cutoff frequencies.

---
## 2. MATHEMATICAL FOUNDATIONS

### 2.1 The Matched Z-Transform (MZT)
Given analog factored transfer function:
$$ H_a(s) = K \frac{\prod_{i=1}^{M} (s - z_i)}{\prod_{k=1}^{N} (s - p_k)} $$
The discrete transfer function is formed by mapping each factor:
$$ H(z) = K_d \frac{\prod_{i=1}^{M} (1 - e^{z_i T_d} z^{-1})}{\prod_{k=1}^{N} (1 - e^{p_k T_d} z^{-1})} (1 + z^{-1})^{N - M} $$
Where $K_d$ is chosen to match the DC gain or passband peak.

### 2.2 Constantinides Digital Spectral Transformations
Substitute $z^{-1} \to g(z^{-1})$ into prototype lowpass filter $H_{\text{LP}}(z)$ with cutoff $\theta_p$:

1. **Lowpass to Highpass (Target Cutoff $\omega_p$):**
   $$ z^{-1} \to -\frac{z^{-1} + \alpha}{1 + \alpha z^{-1}}, \qquad \alpha = -\frac{\cos\left( \frac{\theta_p + \omega_p}{2} \right)}{\cos\left( \frac{\theta_p - \omega_p}{2} \right)} $$
2. **Lowpass to Lowpass (New Cutoff $\omega_p$):**
   $$ z^{-1} \to \frac{z^{-1} - \alpha}{1 - \alpha z^{-1}}, \qquad \alpha = \frac{\sin\left( \frac{\theta_p - \omega_p}{2} \right)}{\sin\left( \frac{\theta_p + \omega_p}{2} \right)} $$

---
## 3. WORKED NUMERICAL EXAMPLES

### Example 29.1: Lowpass to Highpass Spectral Transformation
**Problem:** A first-order digital lowpass filter prototype has transfer function:
$$ H_{\text{LP}}(z) = \frac{0.2452(1 + z^{-1})}{1 - 0.5095 z^{-1}} $$
with cutoff $\theta_p = 0.2\pi$. Transform it into a digital Highpass filter with cutoff $\omega_p = 0.6\pi$.

**Solution:**
1. **Compute Transformation Parameter $\alpha$:**
   $$ \alpha = -\frac{\cos\left( \frac{0.2\pi + 0.6\pi}{2} \right)}{\cos\left( \frac{0.2\pi - 0.6\pi}{2} \right)} = -\frac{\cos(0.4\pi)}{\cos(-0.2\pi)} = -\frac{\cos(72^\circ)}{\cos(36^\circ)} = -\frac{0.3090}{0.8090} = -0.3820 $$
2. **Substitute $z^{-1} \to -\frac{z^{-1} - 0.3820}{1 - 0.3820 z^{-1}}$:**
   $$ H_{\text{HP}}(z) = \frac{0.2452 \left( 1 - \frac{z^{-1} - 0.3820}{1 - 0.3820 z^{-1}} \right)}{1 - 0.5095 \left( -\frac{z^{-1} - 0.3820}{1 - 0.3820 z^{-1}} \right)} = \frac{0.2452 [(1 - 0.3820 z^{-1}) - (z^{-1} - 0.3820)]}{(1 - 0.3820 z^{-1}) + 0.5095(z^{-1} - 0.3820)} $$
   $$ H_{\text{HP}}(z) = \frac{0.2452 [1.3820 - 1.3820 z^{-1}]}{(1 - 0.1946) + (-0.3820 + 0.5095) z^{-1}} = \frac{0.3389(1 - z^{-1})}{0.8054 + 0.1275 z^{-1}} = \frac{0.4208(1 - z^{-1})}{1 + 0.1583 z^{-1}} $$
3. **Verification:**
   * At DC ($z = 1$): $H(1) = 0$ (Zero transmission at DC).
   * At $\omega = \pi$ ($z = -1$): $H(-1) = \frac{0.4208(2)}{1 - 0.1583} = \frac{0.8416}{0.8417} \approx 1.0$ (0 dB passband gain).

---
## 4. UNIVERSITY EXAMINATION QUESTIONS & MARKING RUBRIC

### Question 1 (15 Marks)
**(a)** State the formulas for digital-to-digital spectral transformations from Lowpass to Highpass and Lowpass to Bandpass. Explain why these transformations preserve system stability. *(8 Marks)*
**(b)** Given a 1st-order lowpass filter $H(z) = \frac{1 - a}{2} \frac{1 + z^{-1}}{1 - a z^{-1}}$ with 3-dB cutoff $\theta_p = \pi/2$, find $a$ and transform it into a Highpass filter with cutoff $\omega_p = 3\pi/4$. *(7 Marks)*

**Model Answer & Step-by-Step Marking Rubric:**
* **Part (a):**
  * Transformation equations for LP $\to$ HP and LP $\to$ BP *(4 Marks)*
  * Stability proof: The mapping $g(z^{-1})$ is an all-pass function ($|g(e^{j\omega})|=1$), mapping $|z|<1$ strictly to $|z|<1$ *(4 Marks)*
* **Part (b):**
  * Find $a$: At $\theta_p = \pi/2$, $|H(j)|^2 = 0.5 \implies a = 0 \implies H_{\text{LP}}(z) = \frac{1 + z^{-1}}{2}$ *(3 Marks)*
  * $\alpha = -\frac{\cos(5\pi/8)}{\cos(-\pi/8)} = -\frac{-0.3827}{0.9239} = 0.4142$ *(2 Marks)*
  * Substitute to find $H_{\text{HP}}(z) = \frac{1 - 0.4142}{2} \frac{1 - z^{-1}}{1 + 0.4142 z^{-1}} = 0.2929 \frac{1 - z^{-1}}{1 + 0.4142 z^{-1}}$ *(2 Marks)*

---
## 5. PYTHON VERIFICATION SCRIPT
```python
import numpy as np

# Verify HP transformation
w = np.array([0, np.pi])
H_hp = lambda z: 0.4208 * (1 - z**-1) / (1 + 0.1583 * z**-1)
print("Gain at w=0 (DC):", np.abs(H_hp(np.exp(1j * 0))))
print("Gain at w=pi:", np.abs(H_hp(np.exp(1j * np.pi))))
```
