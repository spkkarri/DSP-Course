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
# Plot 1: Pole Locations (Butterworth vs Chebyshev) in S-Plane
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 4.2))

# 4th-order Butterworth poles (radius = 1.0)
N = 4
theta_b = np.pi * (0.5 + (2*np.arange(1, N+1) - 1)/(2*N))
poles_b = np.exp(1j * theta_b)

# Draw circle
circ = np.linspace(0, 2*np.pi, 100)
ax1.plot(np.cos(circ), np.sin(circ), color=(1.0, 1.0, 1.0, 0.15), linestyle='--')
ax1.axhline(0, color=(1.0, 1.0, 1.0, 0.1), linewidth=1)
ax1.axvline(0, color=(1.0, 1.0, 1.0, 0.1), linewidth=1)
ax1.scatter(np.real(poles_b), np.imag(poles_b), s=60, color='#3b82f6', marker='x', label="Poles")
ax1.set_title("Butterworth Poles (Order N=4)", fontsize=11, pad=10)
ax1.set_xlabel("\u03c3 (Real Axis)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax1.set_ylabel("j\u03a9 (Imag Axis)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax1.set_xlim(-1.3, 1.3)
ax1.set_ylim(-1.3, 1.3)
ax1.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
ax1.legend(frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=8.5)

# 4th-order Chebyshev poles (ellipse parameters: major=1.0, minor=0.5)
epsilon = 0.5088 # for 0.5dB ripple
phi = (1/N) * np.arcsinh(1/epsilon)
theta_c = np.pi * (2*np.arange(1, N+1) - 1) / (2*N)
poles_c_real = -np.sinh(phi) * np.sin(theta_c)
poles_c_imag = np.cosh(phi) * np.cos(theta_c)

# Draw ellipse
ell = np.linspace(0, 2*np.pi, 100)
ax2.plot(np.sinh(phi)*np.cos(ell), np.cosh(phi)*np.sin(ell), color=(1.0, 1.0, 1.0, 0.15), linestyle='--')
ax2.axhline(0, color=(1.0, 1.0, 1.0, 0.1), linewidth=1)
ax2.axvline(0, color=(1.0, 1.0, 1.0, 0.1), linewidth=1)
ax2.scatter(poles_c_real, poles_c_imag, s=60, color='#10b981', marker='x', label="Poles")
ax2.set_title("Chebyshev Type I Poles (Order N=4)", fontsize=11, pad=10)
ax2.set_xlabel("\u03c3 (Real Axis)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax2.set_xlim(-1.3, 1.3)
ax2.set_ylim(-1.3, 1.3)
ax2.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
ax2.legend(frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=8.5)

plt.tight_layout()
plt.savefig("images/analog_poles.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Plot 2: Magnitude Responses
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 3.5))

Omega = np.linspace(0, 3.0, 300)
# Butterworth N=4, wc=1
H_butter = 1 / np.sqrt(1 + Omega**(2*N))

# Chebyshev Type I N=4, wp=1, epsilon=0.5088 (0.5 dB ripple)
eps = 0.5088
C4 = np.zeros_like(Omega)
for idx, x in enumerate(Omega):
    if x <= 1.0:
        C4[idx] = np.cos(4 * np.arccos(x))
    else:
        C4[idx] = np.cosh(4 * np.arccosh(x))
H_cheby = 1 / np.sqrt(1 + (eps**2) * (C4**2))

ax.plot(Omega, H_butter, color='#3b82f6', linewidth=1.5, label="Butterworth (Maximally Flat)")
ax.plot(Omega, H_cheby, color='#10b981', linewidth=1.8, label="Chebyshev Type I (0.5 dB Passband Ripple)")

ax.axvline(1.0, color=(1.0, 1.0, 1.0, 0.2), linestyle=':')
ax.set_xlabel("Normalized Analog Frequency \u03a9 / \u03a9_p", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_ylabel("Magnitude |H_a(j\u03a9)|", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_title("Analog Lowpass Prototypes (N=4)", fontsize=12, pad=12)
ax.set_xlim(0, 2.5)
ax.set_ylim(-0.05, 1.05)
ax.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
ax.legend(frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=8.5)

plt.tight_layout()
plt.savefig("images/analog_responses.png", dpi=300)
plt.close()

print("Lecture 26 images generated successfully.")
