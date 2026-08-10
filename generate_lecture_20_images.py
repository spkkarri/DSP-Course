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
# Plot 1: Single stage of an FIR lattice filter
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 3.2))

# Horizontal paths
ax.plot([0.5, 6.0], [2.2, 2.2], color='#e2e8f0', linewidth=1.5)
ax.plot([0.5, 6.0], [0.6, 0.6], color='#e2e8f0', linewidth=1.5)

# Delay block on bottom path
ax.fill_between([1.8, 2.8], 0.3, 0.9, color='#1f2937', edgecolor='#0dd5c5', linewidth=1.5)
ax.text(2.3, 0.6, r"$z^{-1}$", color='white', ha='center', va='center', fontweight='bold')

# Cross paths (lattice)
ax.plot([1.2, 4.4], [2.2, 0.6], color='#e2e8f0', linestyle='--', linewidth=1.2)
ax.plot([3.1, 4.4], [0.6, 2.2], color='#e2e8f0', linestyle='--', linewidth=1.2)

# Multipliers
ax.add_patch(plt.Circle((2.5, 1.5), 0.22, facecolor='#8b5cf6', edgecolor='white', linewidth=1))
ax.text(2.5, 1.5, "Km", color='black', fontsize=8, fontweight='bold', ha='center', va='center')

ax.add_patch(plt.Circle((3.5, 1.2), 0.22, facecolor='#8b5cf6', edgecolor='white', linewidth=1))
ax.text(3.5, 1.2, "Km", color='black', fontsize=8, fontweight='bold', ha='center', va='center')

# Adders
ax.add_patch(plt.Circle((4.7, 2.2), 0.18, facecolor='#10b981', edgecolor='white', linewidth=1))
ax.text(4.7, 2.2, "+", color='black', fontsize=10, fontweight='bold', ha='center', va='center')

ax.add_patch(plt.Circle((4.7, 0.6), 0.18, facecolor='#10b981', edgecolor='white', linewidth=1))
ax.text(4.7, 0.6, "+", color='black', fontsize=10, fontweight='bold', ha='center', va='center')

# Terminals
ax.text(0.3, 2.2, r"$f_{m-1}[n]$", color='white', fontsize=10, ha='right', va='center')
ax.text(0.3, 0.6, r"$b_{m-1}[n]$", color='white', fontsize=10, ha='right', va='center')
ax.text(6.2, 2.2, r"$f_m[n]$", color='white', fontsize=10, ha='left', va='center')
ax.text(6.2, 0.6, r"$b_m[n]$", color='white', fontsize=10, ha='left', va='center')

ax.set_title("Single lattice stage of order $m$", fontsize=13, pad=15)
ax.set_xlim(-0.8, 7.2)
ax.set_ylim(-0.1, 2.7)
ax.axis('off')

plt.tight_layout()
plt.savefig("images/fir_lattice_stage.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Plot 2: Lattice-Ladder IIR Structure
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 3.2))

# Draw blocks
ax.fill_between([1.0, 3.5], 0.5, 2.0, color='#1f2937', edgecolor='#8b5cf6', linewidth=1.5)
ax.text(2.25, 1.25, r"Lattice Section" + "\n" + r"(Feedback: Poles)" + "\n" + r"Reflection $K_m$", color='white', fontsize=9, ha='center', va='center')

ax.fill_between([4.5, 7.0], 0.5, 2.0, color='#1f2937', edgecolor='#10b981', linewidth=1.5)
ax.text(5.75, 1.25, r"Ladder Section" + "\n" + r"(Feedforward: Zeros)" + "\n" + r"Ladder $C_m$", color='white', fontsize=9, ha='center', va='center')

# Paths
ax.plot([0.0, 1.0], [1.25, 1.25], color='#e2e8f0', linewidth=1.5)
ax.plot([3.5, 4.5], [1.25, 1.25], color='#e2e8f0', linewidth=1.5)
ax.plot([7.0, 8.0], [1.25, 1.25], color='#e2e8f0', linewidth=1.5)

# Labels
ax.text(-0.2, 1.25, r"$x[n]$", color='white', fontsize=11, ha='right', va='center')
ax.text(8.2, 1.25, r"$y[n]$", color='white', fontsize=11, ha='left', va='center')

ax.set_title("Lattice-Ladder IIR filter architecture", fontsize=13, pad=15)
ax.set_xlim(-0.8, 9.0)
ax.set_ylim(0.0, 2.5)
ax.axis('off')

plt.tight_layout()
plt.savefig("images/lattice_ladder.png", dpi=300)
plt.close()

print("Lecture 20 images generated successfully.")
