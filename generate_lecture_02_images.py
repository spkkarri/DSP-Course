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
# Plot 1: Convolution Steps Illustration
# -------------------------------------------------------------
# x[n] = 1 for 0 <= n <= 4, 0 otherwise
# h[n] = 0.8^n for 0 <= n <= 4, 0 otherwise
n = np.arange(-3, 10)
x = np.where((n >= 0) & (n <= 4), 1.0, 0.0)
h = np.where((n >= 0) & (n <= 4), 0.8**n, 0.0)

fig, axs = plt.subplots(4, 1, figsize=(8, 10), sharex=True)

# 1. x[k] and h[k]
markerline, stemlines, baseline = axs[0].stem(n, x)
plt.setp(markerline, color='#6366f1', marker='o')
plt.setp(stemlines, color='#6366f1')
plt.setp(baseline, color='k', linewidth=1)
axs[0].set_title(r"Input Sequence $x[k]$")
axs[0].set_ylabel("Amplitude")

markerline, stemlines, baseline = axs[1].stem(n, h)
plt.setp(markerline, color='#10b981', marker='o')
plt.setp(stemlines, color='#10b981')
plt.setp(baseline, color='k', linewidth=1)
axs[1].set_title(r"Impulse Response $h[k]$")
axs[1].set_ylabel("Amplitude")

# 2. Folded impulse response h[-k]
h_folded = np.zeros_like(n, dtype=float)
for i, val_n in enumerate(n):
    neg_n = -val_n
    if neg_n in n:
        h_folded[i] = h[n == neg_n][0]

markerline, stemlines, baseline = axs[2].stem(n, h_folded)
plt.setp(markerline, color='#8b5cf6', marker='o')
plt.setp(stemlines, color='#8b5cf6')
plt.setp(baseline, color='k', linewidth=1)
axs[2].set_title(r"Time-Reversed Impulse Response $h[-k]$ (Folding)")
axs[2].set_ylabel("Amplitude")

# 3. Output y[n] = x[n] * h[n]
y = np.convolve(x[n>=0], h[n>=0])
n_y = np.arange(0, len(y))

markerline, stemlines, baseline = axs[3].stem(n_y, y)
plt.setp(markerline, color='#ef4444', marker='o')
plt.setp(stemlines, color='#ef4444')
plt.setp(baseline, color='k', linewidth=1)
axs[3].set_title(r"Convolution Output $y[n] = x[n] * h[n]$")
axs[3].set_xlabel("n")
axs[3].set_ylabel("Amplitude")
axs[3].set_xlim(-3, 10)

plt.tight_layout()
plt.savefig("images/convolution_steps.png", dpi=300)
plt.close()


# -------------------------------------------------------------
# Plot 2: LTI Stability (Impulse Response Growth/Decay)
# -------------------------------------------------------------
n_stab = np.arange(0, 16)
h_stable = 0.8**n_stab
h_unstable = 1.15**n_stab

fig, axs = plt.subplots(2, 1, figsize=(9, 7))

# Stable
markerline, stemlines, baseline = axs[0].stem(n_stab, h_stable)
plt.setp(markerline, color='#10b981', marker='o')
plt.setp(stemlines, color='#10b981')
plt.setp(baseline, color='k', linewidth=1)
axs[0].set_title(r"BIBO Stable LTI System: Decaying Impulse Response $h[n] = 0.8^n u[n]$ (Absolutely Summable $\sum |h[n]| < \infty$)")
axs[0].set_ylabel("Amplitude")
axs[0].set_xticks(n_stab)
axs[0].set_ylim(-0.1, 1.1)

# Unstable
markerline, stemlines, baseline = axs[1].stem(n_stab, h_unstable)
plt.setp(markerline, color='#ef4444', marker='o')
plt.setp(stemlines, color='#ef4444')
plt.setp(baseline, color='k', linewidth=1)
axs[1].set_title(r"BIBO Unstable LTI System: Growing Impulse Response $h[n] = 1.15^n u[n]$ (Sum diverges to $\infty$)")
axs[1].set_ylabel("Amplitude")
axs[1].set_xlabel("n")
axs[1].set_xticks(n_stab)

plt.tight_layout()
plt.savefig("images/lti_stability.png", dpi=300)
plt.close()

print("Lecture 2 images generated successfully.")
