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
# Plot 1: ROC of Causal vs. Anti-Causal Exponential
# -------------------------------------------------------------
fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# 1. Causal ROC: x[n] = 0.7^n u[n] -> ROC: |z| > 0.7
draw_zplane_axes(axs[0])
# Shading ROC (|z| > 0.7)
# To shade the outer region, we draw a huge ring
ring = plt.Circle((0,0), 3.0, color='#0dd5c5', alpha=0.15)
axs[0].add_patch(ring)
# Mask the inner disk of radius 0.7 with dark color
inner_disk = plt.Circle((0,0), 0.7, color='#0d121f', fill=True)
axs[0].add_patch(inner_disk)
# Draw boundary circle at r = 0.7
boundary = plt.Circle((0,0), 0.7, color='#0dd5c5', fill=False, linestyle='-', linewidth=1.5)
axs[0].add_patch(boundary)
# Draw pole at z = 0.7
axs[0].plot(0.7, 0, 'x', color='#ef4444', markersize=10, markeredgewidth=2, label='Pole (z=0.7)')
# Draw zero at z = 0
axs[0].plot(0, 0, 'o', color='#10b981', markersize=8, fillstyle='none', markeredgewidth=2, label='Zero (z=0)')
axs[0].set_title(r"Causal $0.7^n u[n]$ (ROC: $|z| > 0.7$)")
axs[0].legend(loc='upper right')

# 2. Anti-Causal ROC: x[n] = -0.7^n u[-n-1] -> ROC: |z| < 0.7
draw_zplane_axes(axs[1])
# Shading ROC (|z| < 0.7)
inner_disk_shaded = plt.Circle((0,0), 0.7, color='#0dd5c5', alpha=0.15)
axs[1].add_patch(inner_disk_shaded)
# Draw boundary circle at r = 0.7
boundary2 = plt.Circle((0,0), 0.7, color='#0dd5c5', fill=False, linestyle='-', linewidth=1.5)
axs[1].add_patch(boundary2)
# Draw pole at z = 0.7
axs[1].plot(0.7, 0, 'x', color='#ef4444', markersize=10, markeredgewidth=2, label='Pole (z=0.7)')
# Draw zero at z = 0
axs[1].plot(0, 0, 'o', color='#10b981', markersize=8, fillstyle='none', markeredgewidth=2, label='Zero (z=0)')
axs[1].set_title(r"Anti-Causal $-0.7^n u[-n-1]$ (ROC: $|z| < 0.7$)")
axs[1].legend(loc='upper right')

plt.tight_layout()
plt.savefig("images/roc_causal_anticausal.png", dpi=300)
plt.close()


# -------------------------------------------------------------
# Plot 2: ROC of Two-Sided Signal (Annular Ring)
# -------------------------------------------------------------
# x[n] = 0.5^n u[n] + 1.5^n u[-n-1]
# Pole at z=0.5 (causal part -> ROC: |z| > 0.5)
# Pole at z=1.5 (anticausal part -> ROC: |z| < 1.5)
# Overlap ROC: 0.5 < |z| < 1.5
fig, ax = plt.subplots(figsize=(6, 6))
draw_zplane_axes(ax)

# Shading outer ring at 1.5, mask inner ring at 0.5
outer_ring = plt.Circle((0,0), 1.5, color='#0dd5c5', alpha=0.15)
ax.add_patch(outer_ring)
inner_disk_mask = plt.Circle((0,0), 0.5, color='#0d121f', fill=True)
ax.add_patch(inner_disk_mask)

# Boundaries
b_inner = plt.Circle((0,0), 0.5, color='#0dd5c5', fill=False, linestyle='-', linewidth=1.5)
b_outer = plt.Circle((0,0), 1.5, color='#0dd5c5', fill=False, linestyle='-', linewidth=1.5)
ax.add_patch(b_inner)
ax.add_patch(b_outer)

# Poles
ax.plot(0.5, 0, 'x', color='#ef4444', markersize=10, markeredgewidth=2, label='Pole Causal (z=0.5)')
ax.plot(1.5, 0, 'x', color='#ef4444', markersize=10, markeredgewidth=2, label='Pole Anti-Causal (z=1.5)')

ax.set_title(r"Two-Sided Signal (ROC: $0.5 < |z| < 1.5$, Stable)")
ax.legend(loc='upper right')

plt.tight_layout()
plt.savefig("images/zplane_common_pairs.png", dpi=300)
plt.close()

print("Lecture 5 images generated successfully.")
