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
# Plot 1: S-plane to Z-plane Mapping (Strips mapping to Circle)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 4.2))

# Left: S-plane showing strip
ax1.axhline(0, color=(1.0, 1.0, 1.0, 0.15), linewidth=1)
ax1.axvline(0, color=(1.0, 1.0, 1.0, 0.15), linewidth=1)

# Draw horizontal lines for the Nyquist limits: -pi/T to +pi/T
ax1.axhline(np.pi, color='#ef4444', linestyle='--', linewidth=1.2, label=r"Nyquist Limit ($\pi/T$)")
ax1.axhline(-np.pi, color='#ef4444', linestyle='--', linewidth=1.2)

# Fill primary strip in LHP
ax1.fill_between([-3.0, 0], [-np.pi, -np.pi], [np.pi, np.pi], color='#3b82f6', alpha=0.1, label="Primary LHP Strip")
ax1.fill_between([-3.0, 0], [np.pi, np.pi], [3*np.pi, 3*np.pi], color='#a78bfa', alpha=0.05, label="Aliasing Strips")
ax1.fill_between([-3.0, 0], [-3*np.pi, -3*np.pi], [-np.pi, -np.pi], color='#a78bfa', alpha=0.05)

ax1.set_title("s-Plane Poles", fontsize=11, pad=10)
ax1.set_xlabel(r"$\sigma$ (Real)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax1.set_ylabel(r"$j\Omega$ (Imaginary)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax1.set_xlim(-3.0, 1.5)
ax1.set_ylim(-3.5*np.pi, 3.5*np.pi)
ax1.set_yticks([-3*np.pi, -np.pi, 0, np.pi, 3*np.pi])
ax1.set_yticklabels([r"$-3\pi/T$", r"$-\pi/T$", "0", r"$\pi/T$", r"$3\pi/T$"])
ax1.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
ax1.legend(loc='lower left', frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=8)

# Right: Z-plane showing unit circle
theta = np.linspace(0, 2*np.pi, 200)
ax2.plot(np.cos(theta), np.sin(theta), color=(1.0, 1.0, 1.0, 0.25), linestyle='-')
ax2.fill(0.95*np.cos(theta), 0.95*np.sin(theta), color='#3b82f6', alpha=0.1, label="Inside Circle (|z|<1)")
ax2.axhline(0, color=(1.0, 1.0, 1.0, 0.15), linewidth=1)
ax2.axvline(0, color=(1.0, 1.0, 1.0, 0.15), linewidth=1)

ax2.set_title(r"z-Plane Poles ($z = e^{s T}$)", fontsize=11, pad=10)
ax2.set_xlabel("Real(z)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax2.set_ylabel("Imag(z)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax2.set_xlim(-1.3, 1.3)
ax2.set_ylim(-1.3, 1.3)
ax2.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
ax2.legend(loc='lower left', frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=8.5)

plt.tight_layout()
plt.savefig("images/impulse_invariance_mapping.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Plot 2: Aliasing Demonstration
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 3.5))

w = np.linspace(-3*np.pi, 3*np.pi, 1000)
# Original analog filter response: lowpass with slow roll-off
Omega_c = 1.0
H_a = 1 / np.sqrt(1 + (w / Omega_c)**2)

# Digital filter response: periodic summation of H_a
H_shift1 = 1 / np.sqrt(1 + ((w - 2*np.pi) / Omega_c)**2)
H_shift2 = 1 / np.sqrt(1 + ((w + 2*np.pi) / Omega_c)**2)
H_sum = H_a + H_shift1 + H_shift2

ax.plot(w, H_a, color=(1.0, 1.0, 1.0, 0.4), linestyle='--', label=r"Analog Response $|H_a(j\Omega)|$")
ax.plot(w, H_shift1, color='#fb7185', linestyle=':', alpha=0.4, label=r"Replicas $|H_a(j(\Omega \pm 2\pi/T))|$")
ax.plot(w, H_shift2, color='#fb7185', linestyle=':', alpha=0.4)
ax.plot(w, H_sum, color='#10b981', linewidth=1.8, label="Resulting Digital Response (Aliased)")

ax.axvline(np.pi, color='#ef4444', linestyle=':')
ax.axvline(-np.pi, color='#ef4444', linestyle=':')
ax.text(np.pi + 0.1, 0.5, r"Nyquist Frequency $\pi/T$", color='#ef4444', rotation=90, fontsize=8)

ax.set_xlabel("Frequency \u03c9 (radians)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_ylabel("Amplitude Magnitude", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_title("Spectral Aliasing in Impulse Invariance Method", fontsize=11, pad=12)
ax.set_xlim(-2*np.pi, 2*np.pi)
ax.set_ylim(-0.05, 1.35)
ax.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
ax.legend(frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=8.5)

plt.tight_layout()
plt.savefig("images/aliasing_demonstration.png", dpi=300)
plt.close()

print("Lecture 27 images generated successfully.")
