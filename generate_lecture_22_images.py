import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("images", exist_ok=True)

# Dark mode styling parameters
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.grid'] = False
plt.rcParams['figure.facecolor'] = '#0d121f'
plt.rcParams['axes.facecolor'] = '#0d121f'
plt.rcParams['savefig.facecolor'] = '#0d121f'

# -------------------------------------------------------------
# Plot 1: Window Time-domain Shapes
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 3.2))

M = 31
n = np.arange(M)
w_rect = np.ones(M)
w_hann = 0.5 - 0.5 * np.cos(2 * np.pi * n / (M - 1))

ax.stem(n, w_rect, linefmt='#3b82f6', markerfmt='o', label="Rectangular Window", basefmt=" ")
ax.stem(n, w_hann, linefmt='#10b981', markerfmt='s', label="Hann Window", basefmt=" ")

ax.set_xlabel("Sample index n", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_ylabel("Amplitude w[n]", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_title("Time-Domain Window Shapes (Length M=31)", fontsize=12, pad=12)
ax.legend(loc='lower center', frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=9)
ax.set_ylim(-0.1, 1.2)
ax.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)

plt.tight_layout()
plt.savefig("images/window_shapes.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Plot 2: Gibbs Phenomenon (Lowpass filter spectrum comparison)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 3.8))

w = np.linspace(0, np.pi, 500)
# Ideal filter cutoff
wc = np.pi / 3

# Compute response with Rectangular and Hann window
# hd[n] = sin(wc * n) / (pi * n) for -15 <= n <= 15
n_ideal = np.arange(-15, 16)
hd = np.zeros_like(n_ideal, dtype=float)
for idx, ni in enumerate(n_ideal):
    if ni == 0:
        hd[idx] = wc / np.pi
    else:
        hd[idx] = np.sin(wc * ni) / (np.pi * ni)

# Apply window
h_rect = hd * np.ones_like(n_ideal)
h_hann = hd * (0.5 - 0.5 * np.cos(2 * np.pi * (n_ideal + 15) / 30))

# Frequency responses
H_rect = np.zeros_like(w, dtype=complex)
H_hann = np.zeros_like(w, dtype=complex)

for idx, wi in enumerate(w):
    H_rect[idx] = np.sum(h_rect * np.exp(-1j * wi * n_ideal))
    H_hann[idx] = np.sum(h_hann * np.exp(-1j * wi * n_ideal))

# Convert to magnitude
mag_rect = np.abs(H_rect)
mag_hann = np.abs(H_hann)

# Plot
ax.plot(w, mag_rect, color='#ef4444', linewidth=1.5, label="Truncated via Rectangular Window (Gibbs Overshoot)")
ax.plot(w, mag_hann, color='#10b981', linewidth=1.8, label="Truncated via Hann Window (Smoothed)")
ax.axvline(wc, color='#f59e0b', linestyle=':', label="Ideal Cutoff \u03c9c")

# Ideal lowpass box
w_box = [0, wc, wc, np.pi]
mag_box = [1, 1, 0, 0]
ax.plot(w_box, mag_box, color=(1.0, 1.0, 1.0, 0.4), linestyle='--', label="Ideal Brickwall Response")

ax.set_xlabel("Frequency \u03c9 (radians)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_ylabel("Magnitude $|H(e^{j\omega})|$", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_title("Gibbs Phenomenon & Spectral Windowing Leakage", fontsize=12, pad=12)
ax.set_xlim(0, np.pi)
ax.set_xticks([0, np.pi/3, np.pi/2, 2*np.pi/3, np.pi])
ax.set_xticklabels(["0", r"$\pi/3$", r"$\pi/2$", r"$2\pi/3$", r"$\pi$"])
ax.set_ylim(-0.1, 1.25)
ax.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
ax.legend(loc='upper right', frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=8.5)

# Annotate overshoot
ax.annotate("Gibbs Overshoot (~8.9%)", xy=(0.28, 1.08), xytext=(0.55, 1.18),
            arrowprops=dict(facecolor='#ef4444', arrowstyle="->", color='#ef4444'),
            color='#ef4444', fontsize=8.5)

plt.tight_layout()
plt.savefig("images/gibbs_phenomenon.png", dpi=300)
plt.close()

print("Lecture 22 images generated successfully.")
