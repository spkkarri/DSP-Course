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

omega = np.linspace(-np.pi, np.pi, 500)

# -------------------------------------------------------------
# Plot 1: Magnitude & Phase of Low-Pass vs. High-Pass Filter
# -------------------------------------------------------------
# LPF: H_LP(e^jw) = 1 / (1 - 0.7 e^-jw)
# HPF: H_HP(e^jw) = 1 / (1 + 0.7 e^-jw)
r = 0.7
H_LP = 1 / (1 - r * np.exp(-1j * omega))
H_HP = 1 / (1 + r * np.exp(-1j * omega))

fig, axs = plt.subplots(2, 2, figsize=(10, 7))

# LPF Magnitude
axs[0, 0].plot(omega, np.abs(H_LP), color='#0dd5c5', linewidth=2)
axs[0, 0].set_title(r"LPF Magnitude $|H(e^{j\omega})|$ ($r=0.7$)")
axs[0, 0].set_ylabel("Gain")
axs[0, 0].set_xticks([-np.pi, 0, np.pi])
axs[0, 0].set_xticklabels([r'$-\pi$', '0', r'$\pi$'])

# LPF Phase
axs[1, 0].plot(omega, np.angle(H_LP), color='#0dd5c5', linewidth=2)
axs[1, 0].set_title(r"LPF Phase $\angle H(e^{j\omega})$")
axs[1, 0].set_xlabel(r"$\omega$ (rad/sample)")
axs[1, 0].set_ylabel("Phase (rad)")
axs[1, 0].set_xticks([-np.pi, 0, np.pi])
axs[1, 0].set_xticklabels([r'$-\pi$', '0', r'$\pi$'])

# HPF Magnitude
axs[0, 1].plot(omega, np.abs(H_HP), color='#ef4444', linewidth=2)
axs[0, 1].set_title(r"HPF Magnitude $|H(e^{j\omega})|$ ($r=-0.7$)")
axs[0, 1].set_xticks([-np.pi, 0, np.pi])
axs[0, 1].set_xticklabels([r'$-\pi$', '0', r'$\pi$'])

# HPF Phase
axs[1, 1].plot(omega, np.angle(H_HP), color='#ef4444', linewidth=2)
axs[1, 1].set_title(r"HPF Phase $\angle H(e^{j\omega})$")
axs[1, 1].set_xlabel(r"$\omega$ (rad/sample)")
axs[1, 1].set_xticks([-np.pi, 0, np.pi])
axs[1, 1].set_xticklabels([r'$-\pi$', '0', r'$\pi$'])

plt.tight_layout()
plt.savefig("images/frequency_response_lpf_hpf.png", dpi=300)
plt.close()


# -------------------------------------------------------------
# Plot 2: Group Delay Analysis
# -------------------------------------------------------------
# Group delay tau_g(w) = (r*cos(w) - r^2) / (1 + r^2 - 2r*cos(w))
# Let's plot for r = 0.5 (moderate decay) and r = 0.85 (steep peak)
r1 = 0.5
r2 = 0.85

tau_g1 = (r1 * np.cos(omega) - r1**2) / (1 + r1**2 - 2 * r1 * np.cos(omega))
tau_g2 = (r2 * np.cos(omega) - r2**2) / (1 + r2**2 - 2 * r2 * np.cos(omega))

# Wait, let's use the correct negative derivative of phase.
# The derivative of phase dtheta/dw is:
# dtheta/dw = - (r*cos(w) - r^2) / (1 + r^2 - 2r*cos(w))
# So group delay is:
# tau_g = - dtheta/dw = (r*cos(w) - r^2) / (1 + r^2 - 2r*cos(w))
# Wait, let's double check if tau_g(0) is positive.
# For r=0.85: tau_g(0) = (0.85 - 0.85^2) / (1 + 0.85^2 - 1.7) = 0.1275 / 0.0225 = 5.67 samples.
# Yes, it is positive.

fig, axs = plt.subplots(2, 1, figsize=(9, 7))

# Magnitude responses for comparison
axs[0].plot(omega, 1 / np.sqrt(1 + r1**2 - 2 * r1 * np.cos(omega)), color='#6366f1', linewidth=2, label=r'$r=0.5$')
axs[0].plot(omega, 1 / np.sqrt(1 + r2**2 - 2 * r2 * np.cos(omega)), color='#0dd5c5', linewidth=2, label=r'$r=0.85$')
axs[0].set_title(r"Filter Magnitude response $|H(e^{j\omega})|$ comparison")
axs[0].set_ylabel("Gain")
axs[0].set_xticks([-np.pi, 0, np.pi])
axs[0].set_xticklabels([r'$-\pi$', '0', r'$\pi$'])
axs[0].legend()

# Group delay
axs[1].plot(omega, tau_g1, color='#6366f1', linewidth=2, label=r'$r=0.5$')
axs[1].plot(omega, tau_g2, color='#0dd5c5', linewidth=2, label=r'$r=0.85$')
axs[1].set_title(r"Group Delay $\tau_g(\omega)$ (High poles delay frequencies longer near cutoff)")
axs[1].set_xlabel(r"$\omega$ (rad/sample)")
axs[1].set_ylabel("Delay (samples)")
axs[1].set_xticks([-np.pi, 0, np.pi])
axs[1].set_xticklabels([r'$-\pi$', '0', r'$\pi$'])
axs[1].legend()

plt.tight_layout()
plt.savefig("images/group_delay_analysis.png", dpi=300)
plt.close()

print("Lecture 4 images generated successfully.")
