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
# Plot 1: IIR Direct Form I Realization Schematic
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 3.5))

# Draw blocks
# Input feedforward delay line (left)
ax.plot([0, 3], [2.2, 2.2], color='#e2e8f0', linewidth=1.5)
ax.plot([3, 7], [2.2, 2.2], color='#e2e8f0', linewidth=1.5)

# Delay blocks (feedforward)
ax.fill_between([1.1, 1.9], 1.9, 2.5, color='#1f2937', edgecolor='#6366f1', linewidth=1.5)
ax.text(1.5, 2.2, r"$z^{-1}$", color='white', ha='center', va='center', fontweight='bold')

# Delay blocks (feedback)
ax.fill_between([5.1, 5.9], 1.9, 2.5, color='#1f2937', edgecolor='#8b5cf6', linewidth=1.5)
ax.text(5.5, 2.2, r"$z^{-1}$", color='white', ha='center', va='center', fontweight='bold')

# Coefficient paths
ax.plot([0.8, 0.8], [2.2, 0.8], color='#e2e8f0', linestyle='--', linewidth=1.2)
ax.plot([2.2, 2.2], [2.2, 0.8], color='#e2e8f0', linestyle='--', linewidth=1.2)

ax.plot([4.8, 4.8], [2.2, 0.8], color='#e2e8f0', linestyle='--', linewidth=1.2)
ax.plot([6.2, 6.2], [2.2, 0.8], color='#e2e8f0', linestyle='--', linewidth=1.2)

# Multipliers
ax.add_patch(plt.Circle((0.8, 0.8), 0.22, facecolor='#6366f1', edgecolor='white', linewidth=1))
ax.text(0.8, 0.8, "b0", color='black', fontsize=8, fontweight='bold', ha='center', va='center')

ax.add_patch(plt.Circle((2.2, 0.8), 0.22, facecolor='#6366f1', edgecolor='white', linewidth=1))
ax.text(2.2, 0.8, "b1", color='black', fontsize=8, fontweight='bold', ha='center', va='center')

ax.add_patch(plt.Circle((4.8, 0.8), 0.22, facecolor='#8b5cf6', edgecolor='white', linewidth=1))
ax.text(4.8, 0.8, "-a1", color='black', fontsize=8, fontweight='bold', ha='center', va='center')

ax.add_patch(plt.Circle((6.2, 0.8), 0.22, facecolor='#8b5cf6', edgecolor='white', linewidth=1))
ax.text(6.2, 0.8, "-a2", color='black', fontsize=8, fontweight='bold', ha='center', va='center')

# Summing junction
ax.add_patch(plt.Circle((3.5, 0.8), 0.2, facecolor='#10b981', edgecolor='white', linewidth=1))
ax.text(3.5, 0.8, "+", color='black', fontsize=11, fontweight='bold', ha='center', va='center')

# Connecting multiplier outputs to sum node
ax.plot([0.8, 3.3], [0.8, 0.8], color='#e2e8f0', linewidth=1.2)
ax.plot([2.2, 3.3], [0.8, 0.8], color='#e2e8f0', linewidth=1.2)
ax.plot([4.8, 3.7], [0.8, 0.8], color='#e2e8f0', linewidth=1.2)
ax.plot([6.2, 3.7], [0.8, 0.8], color='#e2e8f0', linewidth=1.2)

# Input/Output labels
ax.text(-0.2, 2.2, r"$x[n]$", color='white', fontsize=11, ha='right', va='center')
ax.text(7.2, 2.2, r"$y[n]$", color='white', fontsize=11, ha='left', va='center')

ax.set_title("IIR Direct Form I realization (Separated Zeros & Poles)", fontsize=13, pad=15)
ax.set_xlim(-1.0, 8.0)
ax.set_ylim(0.0, 3.0)
ax.axis('off')

plt.tight_layout()
plt.savefig("images/iir_direct_form_i.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Plot 2: IIR Direct Form II Realization Schematic
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 3.5))

# Draw shared middle delay line
ax.plot([3.5, 3.5], [2.2, 0.2], color='#e2e8f0', linewidth=1.5)

# Delay blocks in the center
ax.fill_between([3.1, 3.9], 1.7, 2.3, color='#1f2937', edgecolor='#0dd5c5', linewidth=1.5)
ax.text(3.5, 2.0, r"$z^{-1}$", color='white', ha='center', va='center', fontweight='bold')

ax.fill_between([3.1, 3.9], 0.7, 1.3, color='#1f2937', edgecolor='#0dd5c5', linewidth=1.5)
ax.text(3.5, 1.0, r"$z^{-1}$", color='white', ha='center', va='center', fontweight='bold')

# Sum node on left (feedback summation)
ax.add_patch(plt.Circle((1.5, 2.0), 0.2, facecolor='#10b981', edgecolor='white', linewidth=1))
ax.text(1.5, 2.0, "+", color='black', fontsize=11, fontweight='bold', ha='center', va='center')
ax.plot([0.5, 1.3], [2.0, 2.0], color='#e2e8f0', linewidth=1.5)
ax.plot([1.7, 3.1], [2.0, 2.0], color='#e2e8f0', linewidth=1.5)

# Sum node on right (feedforward summation)
ax.add_patch(plt.Circle((5.5, 2.0), 0.2, facecolor='#10b981', edgecolor='white', linewidth=1))
ax.text(5.5, 2.0, "+", color='black', fontsize=11, fontweight='bold', ha='center', va='center')
ax.plot([3.9, 5.3], [2.0, 2.0], color='#e2e8f0', linewidth=1.5)
ax.plot([5.7, 6.5], [2.0, 2.0], color='#e2e8f0', linewidth=1.5)

# Coefficient multiplier nodes
ax.add_patch(plt.Circle((2.5, 1.0), 0.2, facecolor='#8b5cf6', edgecolor='white', linewidth=1))
ax.text(2.5, 1.0, "-a1", color='black', fontsize=8, fontweight='bold', ha='center', va='center')
ax.plot([3.1, 2.7], [1.0, 1.0], color='#e2e8f0', linewidth=1.2)
ax.plot([2.3, 1.5], [1.0, 2.0], color='#e2e8f0', linestyle='--', linewidth=1.2)

ax.add_patch(plt.Circle((4.5, 1.0), 0.2, facecolor='#6366f1', edgecolor='white', linewidth=1))
ax.text(4.5, 1.0, "b1", color='black', fontsize=8, fontweight='bold', ha='center', va='center')
ax.plot([3.9, 4.3], [1.0, 1.0], color='#e2e8f0', linewidth=1.2)
ax.plot([4.7, 5.5], [1.0, 2.0], color='#e2e8f0', linestyle='--', linewidth=1.2)

# Input/Output labels
ax.text(0.2, 2.0, r"$x[n]$", color='white', fontsize=11, ha='right', va='center')
ax.text(6.8, 2.0, r"$y[n]$", color='white', fontsize=11, ha='left', va='center')

ax.set_title("IIR Direct Form II realization (Shared Delay Line)", fontsize=13, pad=15)
ax.set_xlim(0.0, 7.0)
ax.set_ylim(-0.2, 2.8)
ax.axis('off')

plt.tight_layout()
plt.savefig("images/iir_direct_form_ii.png", dpi=300)
plt.close()

print("Lecture 17 images generated successfully.")
