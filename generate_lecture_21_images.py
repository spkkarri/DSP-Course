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
# Plot 1: Zeros Location (Reciprocal Conjugate Quadruplets)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(4.5, 4.5))

# Draw axes
ax.axhline(0, color=(1.0, 1.0, 1.0, 0.15), linewidth=1)
ax.axvline(0, color=(1.0, 1.0, 1.0, 0.15), linewidth=1)

# Draw unit circle
theta = np.linspace(0, 2*np.pi, 200)
ax.plot(np.cos(theta), np.sin(theta), color=(1.0, 1.0, 1.0, 0.3), linestyle='--', label="Unit Circle")

# Define a base complex zero inside unit circle: z0 = r * e^(j * phi)
r = 0.65
phi = np.pi / 5
z0 = r * np.exp(1j * phi)

# Compute the quadruplet
z_quad = [z0, np.conj(z0), 1/z0, np.conj(1/z0)]

# Colors and labels
colors = ['#8b5cf6', '#a78bfa', '#10b981', '#34d399']
labels = [
    r"$z_0 = re^{j\phi}$",
    r"$z_0^* = re^{-j\phi}$",
    r"$1/z_0 = \frac{1}{r}e^{-j\phi}$",
    r"$1/z_0^* = \frac{1}{r}e^{j\phi}$"
]

# Plot each zero
for z, c, label in zip(z_quad, colors, labels):
    ax.plot(z.real, z.imag, marker='o', markersize=7, color=c, label=label, linestyle='')
    # draw connection line to origin/unit circle
    ax.plot([0, z.real], [0, z.imag], color=c, linestyle=':', alpha=0.5)

# Label axes
ax.set_xlabel("Real", fontsize=9, color=(1.0, 1.0, 1.0, 0.6))
ax.set_ylabel("Imaginary", fontsize=9, color=(1.0, 1.0, 1.0, 0.6))
ax.set_title("Zeros Complex Quadruplet Symmetry", fontsize=12, pad=12)

# Adjust plot boundaries
ax.set_xlim(-2.0, 2.0)
ax.set_ylim(-2.0, 2.0)
ax.set_aspect('equal')
ax.legend(loc='upper right', frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=8)

plt.tight_layout()
plt.savefig("images/zero_quadruplet.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Plot 2: FIR Type constraints (Magnitude envelopes)
# -------------------------------------------------------------
fig, axs = plt.subplots(2, 2, figsize=(8.5, 5.0))

w = np.linspace(0, np.pi, 200)

# Type I: No constraints
axs[0, 0].plot(w, np.cos(w/2)**2, color='#3b82f6', linewidth=2)
axs[0, 0].set_title("Type I (Symmetric, Odd): All filters", fontsize=10)
axs[0, 0].set_xticks([0, np.pi])
axs[0, 0].set_xticklabels(["0", r"$\pi$"])
axs[0, 0].set_ylim(-0.1, 1.1)

# Type II: Zero at pi
axs[0, 1].plot(w, np.cos(w/2), color='#0dd5c5', linewidth=2)
axs[0, 1].plot([np.pi], [0], marker='o', color='red', markersize=6)
axs[0, 1].text(np.pi-0.4, 0.15, r"$H(\pi)=0$", color='red', fontsize=8)
axs[0, 1].set_title("Type II (Symmetric, Even): LPF/BPF only", fontsize=10)
axs[0, 1].set_xticks([0, np.pi])
axs[0, 1].set_xticklabels(["0", r"$\pi$"])
axs[0, 1].set_ylim(-0.1, 1.1)

# Type III: Zeros at 0 and pi
axs[1, 0].plot(w, np.sin(w), color='#8b5cf6', linewidth=2)
axs[1, 0].plot([0, np.pi], [0, 0], marker='o', color='red', markersize=6, linestyle='')
axs[1, 0].text(0.1, 0.15, r"$H(0)=0$", color='red', fontsize=8)
axs[1, 0].text(np.pi-0.5, 0.15, r"$H(\pi)=0$", color='red', fontsize=8)
axs[1, 0].set_title("Type III (Antisymmetric, Odd): BPF only", fontsize=10)
axs[1, 0].set_xticks([0, np.pi])
axs[1, 0].set_xticklabels(["0", r"$\pi$"])
axs[1, 0].set_ylim(-0.1, 1.1)

# Type IV: Zero at 0
axs[1, 1].plot(w, np.sin(w/2), color='#10b981', linewidth=2)
axs[1, 1].plot([0], [0], marker='o', color='red', markersize=6)
axs[1, 1].text(0.1, 0.15, r"$H(0)=0$", color='red', fontsize=8)
axs[1, 1].set_title("Type IV (Antisymmetric, Even): HPF/BPF only", fontsize=10)
axs[1, 1].set_xticks([0, np.pi])
axs[1, 1].set_xticklabels(["0", r"$\pi$"])
axs[1, 1].set_ylim(-0.1, 1.1)

for ax in axs.flat:
    ax.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
    ax.set_ylabel(r"Mag $|H(e^{j\omega})|$", fontsize=8, color=(1.0, 1.0, 1.0, 0.4))
    ax.plot([0, np.pi], [0, 0], color=(1.0, 1.0, 1.0, 0.1), linewidth=1)

plt.suptitle("Frequency Constraints of Linear-Phase FIR Types", fontsize=12, y=0.98)
plt.tight_layout()
plt.savefig("images/fir_types.png", dpi=300)
plt.close()

print("Lecture 21 images generated successfully.")
