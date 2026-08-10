import os
import numpy as np
import matplotlib.pyplot as plt

# Create images directory if it doesn't exist
os.makedirs("images", exist_ok=True)

# Set plotting style for clean academic dark mode look
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.2
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['figure.facecolor'] = '#0d121f'
plt.rcParams['axes.facecolor'] = '#0d121f'
plt.rcParams['savefig.facecolor'] = '#0d121f'

# -------------------------------------------------------------
# Plot 1: Analog vs. Sampled vs. Digital (Quantized)
# -------------------------------------------------------------
t = np.linspace(0, 2, 500)
x_t = 1.5 * np.sin(2 * np.pi * 1.0 * t) + 0.5 * np.cos(2 * np.pi * 2.5 * t)

# Sampling parameters
fs = 12
t_s = np.arange(0, 2, 1/fs)
x_ts = 1.5 * np.sin(2 * np.pi * 1.0 * t_s) + 0.5 * np.cos(2 * np.pi * 2.5 * t_s)

# Quantization (e.g., 3-bit, 8 levels between -2.0 and 2.0)
levels = np.linspace(-2.0, 2.0, 8)
x_tq = np.array([levels[np.argmin(np.abs(val - levels))] for val in x_ts])

fig, axs = plt.subplots(3, 1, figsize=(8, 7), sharex=True)

# 1. Analog
axs[0].plot(t, x_t, color='#1f77b4', lw=2)
axs[0].set_title("Analog Signal $x(t)$ (Continuous-Time, Continuous-Amplitude)")
axs[0].set_ylabel("Amplitude")
axs[0].set_ylim(-2.2, 2.2)

# 2. Sampled
markerline, stemlines, baseline = axs[1].stem(t_s, x_ts)
plt.setp(markerline, color='#d62728', marker='o')
plt.setp(stemlines, color='#d62728')
plt.setp(baseline, color='k', linewidth=1)
axs[1].plot(t, x_t, color='#1f77b4', alpha=0.3, linestyle='--')
axs[1].set_title(r"Sampled Signal $x(nT_s)$ / $x[n]$ (Discrete-Time, Continuous-Amplitude)")
axs[1].set_ylabel("Amplitude")
axs[1].set_ylim(-2.2, 2.2)

# 3. Quantized
markerline, stemlines, baseline = axs[2].stem(t_s, x_tq)
plt.setp(markerline, color='#2ca02c', marker='o')
plt.setp(stemlines, color='#2ca02c')
plt.setp(baseline, color='k', linewidth=1)
# Draw quantization levels as horizontal guide lines
for lvl in levels:
    axs[2].axhline(lvl, color='gray', alpha=0.2, linestyle=':')
axs[2].set_title(r"Quantized Digital Signal $x_q[n]$ (Discrete-Time, Discrete-Amplitude)")
axs[2].set_xlabel("Time (seconds)")
axs[2].set_ylabel("Amplitude")
axs[2].set_ylim(-2.2, 2.2)

plt.tight_layout()
plt.savefig("images/analog_vs_digital.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Plot 2: Elementary Sequences
# -------------------------------------------------------------
fig, axs = plt.subplots(3, 2, figsize=(10, 8))
n = np.arange(-5, 11)

# 1. Unit Impulse delta[n]
delta = np.zeros_like(n)
delta[n == 0] = 1
markerline, stemlines, baseline = axs[0, 0].stem(n, delta)
plt.setp(markerline, color='blue', marker='o')
plt.setp(stemlines, color='blue')
plt.setp(baseline, color='k', linewidth=1)
axs[0, 0].set_title(r"Unit Impulse Sequence $\delta[n]$")
axs[0, 0].set_xlabel("n")
axs[0, 0].set_ylabel("Amplitude")
axs[0, 0].set_xticks(np.arange(-5, 11, 2))
axs[0, 0].set_ylim(-0.2, 1.2)

# 2. Unit Step u[n]
step = np.where(n >= 0, 1, 0)
markerline, stemlines, baseline = axs[0, 1].stem(n, step)
plt.setp(markerline, color='blue', marker='o')
plt.setp(stemlines, color='blue')
plt.setp(baseline, color='k', linewidth=1)
axs[0, 1].set_title(r"Unit Step Sequence $u[n]$")
axs[0, 1].set_xlabel("n")
axs[0, 1].set_ylabel("Amplitude")
axs[0, 1].set_xticks(np.arange(-5, 11, 2))
axs[0, 1].set_ylim(-0.2, 1.2)

# 3. Unit Ramp r[n]
ramp = np.where(n >= 0, n, 0)
markerline, stemlines, baseline = axs[1, 0].stem(n, ramp)
plt.setp(markerline, color='blue', marker='o')
plt.setp(stemlines, color='blue')
plt.setp(baseline, color='k', linewidth=1)
axs[1, 0].set_title(r"Unit Ramp Sequence $r[n]$")
axs[1, 0].set_xlabel("n")
axs[1, 0].set_ylabel("Amplitude")
axs[1, 0].set_xticks(np.arange(-5, 11, 2))
axs[1, 0].set_ylim(-1, 11)

# 4. Decaying Exponential (a = 0.8)
exp1 = np.where(n >= 0, 0.8**n, 0)
markerline, stemlines, baseline = axs[1, 1].stem(n, exp1)
plt.setp(markerline, color='blue', marker='o')
plt.setp(stemlines, color='blue')
plt.setp(baseline, color='k', linewidth=1)
axs[1, 1].set_title(r"Decaying Exponential Sequence $0.8^n u[n]$")
axs[1, 1].set_xlabel("n")
axs[1, 1].set_ylabel("Amplitude")
axs[1, 1].set_xticks(np.arange(-5, 11, 2))
axs[1, 1].set_ylim(-0.2, 1.2)

# 5. Alternating Exponential (a = -0.7)
exp2 = np.where(n >= 0, (-0.7)**n, 0)
markerline, stemlines, baseline = axs[2, 0].stem(n, exp2)
plt.setp(markerline, color='blue', marker='o')
plt.setp(stemlines, color='blue')
plt.setp(baseline, color='k', linewidth=1)
axs[2, 0].set_title(r"Alternating Exponential Sequence $(-0.7)^n u[n]$")
axs[2, 0].set_xlabel("n")
axs[2, 0].set_ylabel("Amplitude")
axs[2, 0].set_xticks(np.arange(-5, 11, 2))
axs[2, 0].set_ylim(-1.2, 1.2)

# 6. Discrete-Time Sinusoid cos(2*pi*n/8)
sinusoid = np.cos(2 * np.pi * n / 8)
markerline, stemlines, baseline = axs[2, 1].stem(n, sinusoid)
plt.setp(markerline, color='blue', marker='o')
plt.setp(stemlines, color='blue')
plt.setp(baseline, color='k', linewidth=1)
axs[2, 1].set_title(r"Sinusoidal Sequence $\cos(\frac{\pi}{4} n)$ (Period N = 8)")
axs[2, 1].set_xlabel("n")
axs[2, 1].set_ylabel("Amplitude")
axs[2, 1].set_xticks(np.arange(-5, 11, 2))
axs[2, 1].set_ylim(-1.2, 1.2)

plt.tight_layout()
plt.savefig("images/elementary_sequences.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Plot 3: Even & Odd Decomposition
# -------------------------------------------------------------
n_eo = np.arange(-6, 7)
# x[n] = 2 at n=0, 3 at n=1, 1 at n=2, 0 otherwise
x_n = np.zeros_like(n_eo, dtype=float)
x_n[n_eo == 0] = 2.0
x_n[n_eo == 1] = 3.0
x_n[n_eo == 2] = 1.0

# x[-n]
x_minus_n = x_n[::-1]

# Even part: x_e[n] = (x[n] + x[-n]) / 2
x_e = (x_n + x_minus_n) / 2.0

# Odd part: x_o[n] = (x[n] - x[-n]) / 2
x_o = (x_n - x_minus_n) / 2.0

fig, axs = plt.subplots(2, 2, figsize=(10, 8), sharex=True, sharey=True)

# x[n]
markerline, stemlines, baseline = axs[0, 0].stem(n_eo, x_n)
plt.setp(markerline, color='#6366f1', marker='o')
plt.setp(stemlines, color='#6366f1')
plt.setp(baseline, color='k', linewidth=1)
axs[0, 0].set_title(r"Original Signal $x[n]$")
axs[0, 0].set_ylabel("Amplitude")

# x[-n]
markerline, stemlines, baseline = axs[0, 1].stem(n_eo, x_minus_n)
plt.setp(markerline, color='#8b5cf6', marker='o')
plt.setp(stemlines, color='#8b5cf6')
plt.setp(baseline, color='k', linewidth=1)
axs[0, 1].set_title(r"Time-Reversed Signal $x[-n]$")

# x_e[n]
markerline, stemlines, baseline = axs[1, 0].stem(n_eo, x_e)
plt.setp(markerline, color='#10b981', marker='o')
plt.setp(stemlines, color='#10b981')
plt.setp(baseline, color='k', linewidth=1)
axs[1, 0].set_title(r"Even Component $x_e[n] = \frac{x[n] + x[-n]}{2}$")
axs[1, 0].set_xlabel("n")
axs[1, 0].set_ylabel("Amplitude")

# x_o[n]
markerline, stemlines, baseline = axs[1, 1].stem(n_eo, x_o)
plt.setp(markerline, color='#ef4444', marker='o')
plt.setp(stemlines, color='#ef4444')
plt.setp(baseline, color='k', linewidth=1)
axs[1, 1].set_title(r"Odd Component $x_o[n] = \frac{x[n] - x[-n]}{2}$")
axs[1, 1].set_xlabel("n")

plt.tight_layout()
plt.savefig("images/even_odd_decomposition.png", dpi=300)
plt.close()


# -------------------------------------------------------------
# Plot 4: Energy vs. Power Signals
# -------------------------------------------------------------
fig, axs = plt.subplots(2, 1, figsize=(9, 7))

# Energy Signal: x[n] = 2 * (0.7)^n * u[n]
n_e = np.arange(-2, 11)
x_energy = np.where(n_e >= 0, 2.0 * (0.7**n_e), 0.0)
markerline, stemlines, baseline = axs[0].stem(n_e, x_energy)
plt.setp(markerline, color='#10b981', marker='o')
plt.setp(stemlines, color='#10b981')
plt.setp(baseline, color='k', linewidth=1)
axs[0].set_title(r"Energy Signal: $x[n] = 2(0.7)^n u[n]$ (Finite Energy $E \approx 7.84$, Power $P = 0$)")
axs[0].set_ylabel("Amplitude")
axs[0].set_xticks(np.arange(-2, 11))
axs[0].set_ylim(-0.2, 2.3)

# Power Signal: x[n] = 1.5 * cos(0.2 * pi * n)
n_p = np.arange(-2, 16)
x_power = 1.5 * np.cos(0.2 * np.pi * n_p)
markerline, stemlines, baseline = axs[1].stem(n_p, x_power)
plt.setp(markerline, color='#6366f1', marker='o')
plt.setp(stemlines, color='#6366f1')
plt.setp(baseline, color='k', linewidth=1)
axs[1].set_title(r"Power Signal: $x[n] = 1.5\cos(0.2\pi n)$ (Infinite Energy $E = \infty$, Avg Power $P = 1.125$)")
axs[1].set_ylabel("Amplitude")
axs[1].set_xlabel("n")
axs[1].set_xticks(np.arange(-2, 16))
axs[1].set_ylim(-1.8, 1.8)

plt.tight_layout()
plt.savefig("images/energy_vs_power.png", dpi=300)
plt.close()

print("Images generated successfully in 'images/' folder.")
