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

# Helper function to draw a complex plane axis
def draw_zplane_axes(ax):
    ax.axhline(0, color='white', linewidth=0.8, alpha=0.3)
    ax.axvline(0, color='white', linewidth=0.8, alpha=0.3)
    # Draw unit circle
    uc = plt.Circle((0, 0), 1.0, color='#6366f1', fill=False, linestyle='--', linewidth=1.2, label='Unit Circle')
    ax.add_patch(uc)
    ax.set_aspect('equal')
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)
    ax.set_xlabel('Real (Re)')
    ax.set_ylabel('Imaginary (Im)')

# -------------------------------------------------------------
# Plot 1: Pole Locations vs. Stability Regions
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6, 6))
draw_zplane_axes(ax)

# Draw a stable shaded region inside the unit circle
stable_region = plt.Circle((0, 0), 1.0, color='#10b981', alpha=0.08, label='Stable Region (|z| < 1)')
ax.add_patch(stable_region)

# Draw poles inside and outside the unit circle
ax.plot(0.5, 0.5, 'x', color='#10b981', markersize=10, markeredgewidth=2, label='Stable Pole (z = 0.5 + 0.5j)')
ax.plot(0.5, -0.5, 'x', color='#10b981', markersize=10, markeredgewidth=2)
ax.plot(1.3, 0.8, 'x', color='#ef4444', markersize=10, markeredgewidth=2, label='Unstable Pole (z = 1.3 + 0.8j)')
ax.plot(1.3, -0.8, 'x', color='#ef4444', markersize=10, markeredgewidth=2)

ax.set_title("Pole Locations & BIBO Stability Region")
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig("images/pole_zero_stability_l6.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Plot 2: Impulse Response Modes h[n]
# -------------------------------------------------------------
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# 1. Causal Stable: h[n] = 0.7^n u[n]
n_causal = np.arange(0, 15)
h_causal_stable = 0.7 ** n_causal
axs[0, 0].stem(n_causal, h_causal_stable, linefmt='#10b981', markerfmt='o', basefmt='white')
axs[0, 0].set_title(r"Causal Stable: $0.7^n u[n]$ (Decays)")
axs[0, 0].set_xlabel("n")
axs[0, 0].set_ylabel("h[n]")
axs[0, 0].set_xlim(-1, 15)
axs[0, 0].set_ylim(-0.2, 1.2)

# 2. Causal Unstable: h[n] = 1.3^n u[n]
h_causal_unstable = 1.3 ** n_causal
axs[0, 1].stem(n_causal, h_causal_unstable, linefmt='#ef4444', markerfmt='o', basefmt='white')
axs[0, 1].set_title(r"Causal Unstable: $1.3^n u[n]$ (Explodes)")
axs[0, 1].set_xlabel("n")
axs[0, 1].set_ylabel("h[n]")
axs[0, 1].set_xlim(-1, 15)
axs[0, 1].set_ylim(-0.5, 30)

# 3. Anti-Causal Stable: h[n] = -1.3^n u[-n-1]
n_anticausal = np.arange(-15, 0)
h_anticausal_stable = -(1.3 ** n_anticausal)
axs[1, 0].stem(n_anticausal, h_anticausal_stable, linefmt='#10b981', markerfmt='o', basefmt='white')
axs[1, 0].set_title(r"Anti-Causal Stable: $-1.3^n u[-n-1]$ (Decays for $n \to -\infty$)")
axs[1, 0].set_xlabel("n")
axs[1, 0].set_ylabel("h[n]")
axs[1, 0].set_xlim(-15, 1)
axs[1, 0].set_ylim(-1.2, 0.2)

# 4. Anti-Causal Unstable: h[n] = -0.7^n u[-n-1]
h_anticausal_unstable = -(0.7 ** n_anticausal)
axs[1, 1].stem(n_anticausal, h_anticausal_unstable, linefmt='#ef4444', markerfmt='o', basefmt='white')
axs[1, 1].set_title(r"Anti-Causal Unstable: $-0.7^n u[-n-1]$ (Explodes for $n \to -\infty$)")
axs[1, 1].set_xlabel("n")
axs[1, 1].set_ylabel("h[n]")
axs[1, 1].set_xlim(-15, 1)
axs[1, 1].set_ylim(-30, 0.5)

plt.tight_layout()
plt.savefig("images/impulse_response_modes.png", dpi=300)
plt.close()

print("Lecture 6 images generated successfully.")
