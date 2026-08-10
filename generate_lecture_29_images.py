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
# Plot 1: Mapped Poles and Zeros using MZT
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 4.2))

# Analog filter poles at s = -1 \pm j3, zero at s = -4 (for LHP)
ax1.axhline(0, color=(1.0, 1.0, 1.0, 0.15), linewidth=1)
ax1.axvline(0, color=(1.0, 1.0, 1.0, 0.15), linewidth=1)
ax1.scatter([-1, -1], [3, -3], s=60, color='#3b82f6', marker='x', label="Poles")
ax1.scatter([-4], [0], s=60, color='#10b981', marker='o', label="Zeros")
ax1.set_title("Analog s-Plane Poles/Zeros", fontsize=11, pad=10)
ax1.set_xlabel(r"$\sigma$", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax1.set_ylabel(r"$j\Omega$", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax1.set_xlim(-5.0, 1.5)
ax1.set_ylim(-4.0, 4.0)
ax1.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
ax1.legend(loc='lower right', frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=8.5)

# Digital filter poles under MZT (z = e^(s * T), T=0.2)
# Poles: e^(-0.2 \pm j0.6) = 0.8187 * (cos(0.6) \pm j sin(0.6))
# Zeros: e^(-0.8) = 0.4493
T = 0.2
p_r = np.exp(-1 * T)
p_theta = 3 * T
poles_z_real = [p_r * np.cos(p_theta), p_r * np.cos(-p_theta)]
poles_z_imag = [p_r * np.sin(p_theta), p_r * np.sin(-p_theta)]
zeros_z_real = [np.exp(-4 * T)]
zeros_z_imag = [0]

theta = np.linspace(0, 2*np.pi, 200)
ax2.plot(np.cos(theta), np.sin(theta), color=(1.0, 1.0, 1.0, 0.25), linestyle='-')
ax2.axhline(0, color=(1.0, 1.0, 1.0, 0.15), linewidth=1)
ax2.axvline(0, color=(1.0, 1.0, 1.0, 0.15), linewidth=1)
ax2.scatter(poles_z_real, poles_z_imag, s=60, color='#3b82f6', marker='x', label="Mapped Poles")
ax2.scatter(zeros_z_real, zeros_z_imag, s=60, color='#10b981', marker='o', label="Mapped Zeros")
# MZT adds zero at z = -1 to match high-frequency roll-off (since N_poles > N_zeros)
ax2.scatter([-1], [0], s=60, color='#8b5cf6', marker='o', facecolors='none', edgecolors='#8b5cf6', linewidth=1.5, label="Added Zeros at z=-1")

ax2.set_title("Digital z-Plane Poles/Zeros (MZT)", fontsize=11, pad=10)
ax2.set_xlabel("Real(z)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax2.set_ylabel("Imag(z)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax2.set_xlim(-1.3, 1.3)
ax2.set_ylim(-1.3, 1.3)
ax2.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
ax2.legend(loc='lower right', frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=8.5)

plt.tight_layout()
plt.savefig("images/matched_zplane.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Plot 2: Spectral Transformations
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 3.8))

# Let's plot digital response transformations
omega = np.linspace(0, np.pi, 300)

# Prototype LPF cutoff at 0.3*pi (2nd-order Butterworth LPF)
wc = 0.3 * np.pi
H_lpf = 1.0 / np.sqrt(1 + (omega / wc)**6)

# HPF response: invert frequency (omega -> pi - omega)
H_hpf = 1.0 / np.sqrt(1 + ((np.pi - omega) / wc)**6)

# BPF response: peak at 0.5*pi, passband width 0.2*pi
H_bpf = np.exp(-((omega - 0.5*np.pi) / (0.15*np.pi))**4)

# BSF response: notch at 0.5*pi
H_bsf = 1.0 - np.exp(-((omega - 0.5*np.pi) / (0.15*np.pi))**4)

ax.plot(omega, H_lpf, color='#3b82f6', linewidth=1.8, label="Lowpass Prototype")
ax.plot(omega, H_hpf, color='#ef4444', linewidth=1.8, label="Transformed Highpass")
ax.plot(omega, H_bpf, color='#10b981', linewidth=1.8, label="Transformed Bandpass")
ax.plot(omega, H_bsf, color='#fb7185', linewidth=1.8, label="Transformed Bandstop")

ax.set_xlabel("Discrete Frequency \u03c9 (radians)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_ylabel("Magnitude |H(e^{j\u03c9})|", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_title("Frequency Transformations in Digital Domain", fontsize=11, pad=12)
ax.set_xlim(0, np.pi)
ax.set_ylim(-0.05, 1.05)
ax.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
ax.set_xticklabels(["0", r"$\pi/4$", r"$\pi/2$", r"$3\pi/4$", r"$\pi$"])
ax.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
ax.legend(frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=8.5)

plt.tight_layout()
plt.savefig("images/spectral_transformation_mappings.png", dpi=300)
plt.close()

print("Lecture 29 images generated successfully.")
