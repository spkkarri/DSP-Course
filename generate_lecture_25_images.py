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
# Plot 1: Z-plane for N=8 Moving Average Filter
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(4.5, 4.5))

# Draw unit circle
theta = np.linspace(0, 2*np.pi, 200)
ax.plot(np.cos(theta), np.sin(theta), color=(1.0, 1.0, 1.0, 0.2), linestyle='--')

# Zeros of N=8 (except z=1)
N = 8
k = np.arange(1, N)
zeros = np.exp(1j * 2 * np.pi * k / N)

ax.scatter(np.real(zeros), np.imag(zeros), s=60, facecolors='none', edgecolors='#10b981', linewidth=1.5, marker='o', label="Zeros")

# Canceled Pole/Zero at z=1
ax.scatter([1.0], [0.0], s=60, color='#6b7280', marker='x', label="Canceled Pole/Zero")

# Poles at z=0 (N-1 poles)
ax.scatter([0.0], [0.0], s=80, color='#ef4444', marker='x', label="Poles at Origin")

# Axis lines
ax.axhline(0, color=(1.0, 1.0, 1.0, 0.1), linewidth=1)
ax.axvline(0, color=(1.0, 1.0, 1.0, 0.1), linewidth=1)

ax.set_title("Z-Plane of 8-Point Moving Average Filter", fontsize=11, pad=12)
ax.set_xlabel("Real Part", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_ylabel("Imaginary Part", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_xlim(-1.3, 1.3)
ax.set_ylim(-1.3, 1.3)
ax.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
ax.legend(loc='upper left', frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=8.5)

plt.tight_layout()
plt.savefig("images/moving_average_zplane.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Plot 2: Magnitude Response
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 3.2))

w = np.linspace(0, np.pi, 500)
H = np.zeros_like(w)
for idx, wi in enumerate(w):
    if wi == 0:
        H[idx] = 1.0
    else:
        H[idx] = np.sin(wi * N / 2) / (N * np.sin(wi / 2))

H_mag = np.abs(H)

ax.plot(w, H_mag, color='#3b82f6', linewidth=1.8, label=r"$|H(e^{j\omega})|$ (Dirichlet)")
ax.axhline(0, color=(1.0, 1.0, 1.0, 0.1), linewidth=1)

# Draw vertical lines for nulls
nulls = [2*np.pi/N, 4*np.pi/N, 6*np.pi/N]
for null in nulls:
    if null <= np.pi:
        ax.axvline(null, color='#ef4444', linestyle=':', alpha=0.6)

ax.set_xlabel("Frequency \u03c9 (radians)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_ylabel("Magnitude", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_title("Magnitude Response of 8-Point Moving Average Filter", fontsize=11, pad=12)
ax.set_xlim(0, np.pi)
ax.set_ylim(-0.05, 1.05)
ax.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
ax.legend(frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=8.5)

plt.tight_layout()
plt.savefig("images/moving_average_frequency.png", dpi=300)
plt.close()

print("Lecture 25 images generated successfully.")
