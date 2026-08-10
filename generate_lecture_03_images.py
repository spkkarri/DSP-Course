import os
import numpy as np
import matplotlib.pyplot as plt

os.makedirs("images", exist_ok=True)

# Dark mode styling parameters
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
# Plot 1: DTFT of Rectangular Pulse (Time-Frequency Duality)
# -------------------------------------------------------------
omega = np.linspace(-np.pi, np.pi, 500)

fig, axs = plt.subplots(2, 2, figsize=(10, 7))

# Pulse 1: Short (M = 4)
M1 = 4
n1 = np.arange(-2, 8)
x1 = np.where((n1 >= 0) & (n1 < M1), 1.0, 0.0)
X1 = np.sin(omega * M1 / 2) / (np.sin(omega / 2) + 1e-12) * np.exp(-1j * omega * (M1 - 1) / 2)

# Pulse 2: Long (M = 8)
M2 = 8
n2 = np.arange(-2, 10)
x2 = np.where((n2 >= 0) & (n2 < M2), 1.0, 0.0)
X2 = np.sin(omega * M2 / 2) / (np.sin(omega / 2) + 1e-12) * np.exp(-1j * omega * (M2 - 1) / 2)

# Time 1
markerline, stemlines, baseline = axs[0, 0].stem(n1, x1)
plt.setp(markerline, color='#0dd5c5')
plt.setp(stemlines, color='#0dd5c5')
axs[0, 0].set_title(r"Short Pulse $x_1[n]$ ($M = 4$)")
axs[0, 0].set_ylabel("Amplitude")

# Freq 1 (Magnitude)
axs[0, 1].plot(omega, np.abs(X1), color='#0dd5c5', linewidth=2)
axs[0, 1].set_title(r"Magnitude $|X_1(e^{j\omega})|$ (Wide Lobe)")
axs[0, 1].set_ylabel("Magnitude")
axs[0, 1].set_xticks([-np.pi, 0, np.pi])
axs[0, 1].set_xticklabels([r'$-\pi$', '0', r'$\pi$'])

# Time 2
markerline, stemlines, baseline = axs[1, 0].stem(n2, x2)
plt.setp(markerline, color='#8b5cf6')
plt.setp(stemlines, color='#8b5cf6')
axs[1, 0].set_title(r"Longer Pulse $x_2[n]$ ($M = 8$)")
axs[1, 0].set_xlabel("n")
axs[1, 0].set_ylabel("Amplitude")

# Freq 2 (Magnitude)
axs[1, 1].plot(omega, np.abs(X2), color='#8b5cf6', linewidth=2)
axs[1, 1].set_title(r"Magnitude $|X_2(e^{j\omega})|$ (Narrow Lobe)")
axs[1, 1].set_xlabel(r"$\omega$ (rad/sample)")
axs[1, 1].set_ylabel("Magnitude")
axs[1, 1].set_xticks([-np.pi, 0, np.pi])
axs[1, 1].set_xticklabels([r'$-\pi$', '0', r'$\pi$'])

plt.tight_layout()
plt.savefig("images/dtft_rect_sinc.png", dpi=300)
plt.close()


# -------------------------------------------------------------
# Plot 2: Time Shifting Property & Phase Spectrum
# -------------------------------------------------------------
# x[n] = 0.7^n u[n] vs x[n - 2]
n = np.arange(-2, 10)
x_orig = np.where(n >= 0, 0.7**n, 0.0)
x_shifted = np.where(n >= 2, 0.7**(n-2), 0.0)

# DTFT
X_orig = 1 / (1 - 0.7 * np.exp(-1j * omega))
# Shifted DTFT: X_shifted = X_orig * e^(-j * 2 * omega)
X_shifted = X_orig * np.exp(-1j * 2 * omega)

fig, axs = plt.subplots(2, 2, figsize=(10, 7))

# Stems Orig
markerline, stemlines, baseline = axs[0, 0].stem(n, x_orig)
plt.setp(markerline, color='#10b981')
plt.setp(stemlines, color='#10b981')
axs[0, 0].set_title(r"Original $x[n] = 0.7^n u[n]$")
axs[0, 0].set_ylabel("Amplitude")

# Magnitude (both are equal)
axs[0, 1].plot(omega, np.abs(X_orig), color='#10b981', linewidth=2, label='Original')
axs[0, 1].plot(omega, np.abs(X_shifted), color='#ef4444', linestyle='--', linewidth=2, label='Shifted')
axs[0, 1].set_title(r"Magnitude spectrum is identical: $|X(e^{j\omega})|$")
axs[0, 1].set_ylabel("Magnitude")
axs[0, 1].set_xticks([-np.pi, 0, np.pi])
axs[0, 1].set_xticklabels([r'$-\pi$', '0', r'$\pi$'])
axs[0, 1].legend()

# Stems Shifted
markerline, stemlines, baseline = axs[1, 0].stem(n, x_shifted)
plt.setp(markerline, color='#ef4444')
plt.setp(stemlines, color='#ef4444')
axs[1, 0].set_title(r"Shifted $y[n] = x[n - 2]$")
axs[1, 0].set_xlabel("n")
axs[1, 0].set_ylabel("Amplitude")

# Phase comparison
axs[1, 1].plot(omega, np.angle(X_orig), color='#10b981', linewidth=2, label='Original')
axs[1, 1].plot(omega, np.angle(X_shifted), color='#ef4444', linewidth=2, label='Shifted (Linear Phase)')
axs[1, 1].set_title(r"Phase Spectrum $\angle X(e^{j\omega})$ (Slope changes)")
axs[1, 1].set_xlabel(r"$\omega$ (rad/sample)")
axs[1, 1].set_ylabel("Phase (radians)")
axs[1, 1].set_xticks([-np.pi, 0, np.pi])
axs[1, 1].set_xticklabels([r'$-\pi$', '0', r'$\pi$'])
axs[1, 1].legend()

plt.tight_layout()
plt.savefig("images/dtft_shifting_property.png", dpi=300)
plt.close()

print("Lecture 3 images generated successfully.")
