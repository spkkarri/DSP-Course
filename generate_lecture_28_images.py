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
# Plot 1: Bilinear s-plane to z-plane region mapping
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 4.2))

# Left: S-plane
ax1.axhline(0, color=(1.0, 1.0, 1.0, 0.15), linewidth=1)
# Draw imaginary axis in green to show it maps to unit circle
ax1.axvline(0, color='#10b981', linewidth=2.0, label="Imag Axis (s = j\u03a9)")
# Fill Left-Half Plane (LHP)
ax1.fill_between([-4.0, 0], [-4.0, -4.0], [4.0, 4.0], color='#3b82f6', alpha=0.1, label="Left Half Plane")
ax1.fill_between([0, 4.0], [-4.0, -4.0], [4.0, 4.0], color='#ef4444', alpha=0.03, label="Right Half Plane")

ax1.set_title("s-Plane Domains", fontsize=11, pad=10)
ax1.set_xlabel(r"$\sigma$ (Real)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax1.set_ylabel(r"$j\Omega$ (Imaginary)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax1.set_xlim(-3.0, 3.0)
ax1.set_ylim(-3.0, 3.0)
ax1.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
ax1.legend(loc='lower left', frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=8.5)

# Right: Z-plane
theta = np.linspace(0, 2*np.pi, 200)
# Draw unit circle in green to match the mapped imaginary axis
ax2.plot(np.cos(theta), np.sin(theta), color='#10b981', linewidth=2.0, label="Unit Circle (|z| = 1)")
ax2.fill(0.98*np.cos(theta), 0.98*np.sin(theta), color='#3b82f6', alpha=0.1, label="Inside Circle (|z|<1)")
ax2.axhline(0, color=(1.0, 1.0, 1.0, 0.15), linewidth=1)
ax2.axvline(0, color=(1.0, 1.0, 1.0, 0.15), linewidth=1)

ax2.set_title("z-Plane Domains", fontsize=11, pad=10)
ax2.set_xlabel("Real(z)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax2.set_ylabel("Imag(z)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax2.set_xlim(-1.3, 1.3)
ax2.set_ylim(-1.3, 1.3)
ax2.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
ax2.legend(loc='lower left', frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=8.5)

plt.tight_layout()
plt.savefig("images/bilinear_s_to_z.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Plot 2: Frequency Warping
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 3.8))

# Omega goes from 0 to 12
Omega = np.linspace(0, 15, 500)
# w = 2 * arctan(Omega * T / 2)
# Let T = 1
T = 1.0
w = 2 * np.arctan(Omega * T / 2)

# Linear tangent line at origin
w_linear = Omega * T

ax.plot(Omega, w, color='#8b5cf6', linewidth=2.0, label=r"Warped Frequency: $\omega = 2 \arctan(\Omega T_d / 2)$")
ax.plot(Omega, w_linear, color=(1.0, 1.0, 1.0, 0.3), linestyle='--', label=r"Linear Mapping: $\omega = \Omega T_d$")
ax.axhline(np.pi, color='#ef4444', linestyle=':', label=r"Digital Nyquist \omega = \pi")

ax.set_xlabel("Analog Frequency \u03a9 (rad/s)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_ylabel("Digital Frequency \u03c9 (rad)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_title("Frequency Warping in Bilinear Transformation", fontsize=11, pad=12)
ax.set_xlim(0, 12)
ax.set_ylim(0, np.pi * 1.1)
ax.set_yticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
ax.set_yticklabels(["0", r"$\pi/4$", r"$\pi/2$", r"$3\pi/4$", r"$\pi$"])
ax.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
ax.legend(frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=8.5)

plt.tight_layout()
plt.savefig("images/bilinear_frequency_warping.png", dpi=300)
plt.close()

print("Lecture 28 images generated successfully.")
