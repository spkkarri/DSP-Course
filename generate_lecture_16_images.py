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
# Plot 1: Linear Phase FIR folding structure (M=4, symmetric)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 3.5))

# Main horizontal path
ax.plot([0, 6], [2, 2], color='#e2e8f0', linewidth=1.5)
# Folded horizontal path
ax.plot([1.5, 6], [0, 0], color='#e2e8f0', linewidth=1.5)

# Delay blocks (registers)
ax.fill_between([1.1, 1.9], 1.7, 2.3, color='#1f2937', edgecolor='#4b5563', linewidth=1.5)
ax.text(1.5, 2, r"$z^{-1}$", color='white', ha='center', va='center', fontweight='bold')

ax.fill_between([3.6, 4.4], 1.7, 2.3, color='#1f2937', edgecolor='#4b5563', linewidth=1.5)
ax.text(4.0, 2, r"$z^{-1}$", color='white', ha='center', va='center', fontweight='bold')

# Folding path down and left
ax.plot([5.2, 5.2], [2, 0], color='#e2e8f0', linewidth=1.5)
ax.plot([5.2, 3.6], [0, 0], color='#e2e8f0', linewidth=1.5)

# Another register on bottom path
ax.fill_between([2.6, 3.4], -0.3, 0.3, color='#1f2937', edgecolor='#4b5563', linewidth=1.5)
ax.text(3.0, 0, r"$z^{-1}$", color='white', ha='center', va='center', fontweight='bold')

# Summing node (left folding addition)
ax.add_patch(plt.Circle((0.8, 1.0), 0.18, facecolor='#10b981', edgecolor='white', linewidth=1))
ax.text(0.8, 1.0, "+", color='black', fontsize=10, fontweight='bold', ha='center', va='center')
ax.plot([0.8, 0.8], [2, 0], color='#e2e8f0', linestyle='--', linewidth=1.2)
ax.plot([0.8, 1.8], [0, 0], color='#e2e8f0', linewidth=1.5)

# Stems and multipliers
ax.add_patch(plt.Circle((0.8, 0.5), 0.22, facecolor='#6366f1', edgecolor='white', linewidth=1))
ax.text(0.8, 0.5, "h[0]", color='black', fontsize=8, fontweight='bold', ha='center', va='center')

ax.add_patch(plt.Circle((2.2, 0.5), 0.22, facecolor='#8b5cf6', edgecolor='white', linewidth=1))
ax.text(2.2, 0.5, "h[1]", color='black', fontsize=8, fontweight='bold', ha='center', va='center')

# Summing node at the bottom right
ax.add_patch(plt.Circle((5.7, 0.5), 0.18, facecolor='#10b981', edgecolor='white', linewidth=1))
ax.text(5.7, 0.5, "+", color='black', fontsize=10, fontweight='bold', ha='center', va='center')

# Path arrows and connections
ax.text(-0.2, 2, r"$x[n]$", color='white', fontsize=11, ha='right', va='center')
ax.text(6.4, 0.5, r"$y[n]$", color='white', fontsize=11, ha='left', va='center')

ax.set_title("Symmetric Linear-Phase FIR folding structure ($M=4$)", fontsize=13, pad=15)
ax.set_xlim(-1.0, 7.5)
ax.set_ylim(-0.8, 2.8)
ax.axis('off')

plt.tight_layout()
plt.savefig("images/linear_phase_fir.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Plot 2: Frequency Sampling Filter Structure
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 3.2))

# Horizontal feed path
ax.plot([0, 8.5], [1, 1], color='#e2e8f0', linewidth=1.5)

# Comb filter box
ax.fill_between([1.2, 2.8], 0.4, 1.6, color='#1f2937', edgecolor='#0dd5c5', linewidth=1.5)
ax.text(2, 1, r"$H_c(z) = 1 - z^{-N}$" + "\n" + r"(Comb Filter)", color='white', fontsize=9, ha='center', va='center')

# Resonator Bank Box
ax.fill_between([4.5, 7.5], 0.3, 1.7, color='#1f2937', edgecolor='#8b5cf6', linewidth=1.5)
ax.text(6.0, 1, r"Parallel Resonators" + "\n" + r"$H_p(z) = \sum_{k=0}^{N-1} \frac{H[k]/N}{1 - e^{j2\pi k/N}z^{-1}}$", color='white', fontsize=9, ha='center', va='center')

# Path labels
ax.text(-0.2, 1, r"$x[n]$", color='white', fontsize=11, ha='right', va='center')
ax.text(3.65, 1.2, r"$w[n]$", color='#0dd5c5', fontsize=10, ha='center', va='center')
ax.text(8.7, 1, r"$y[n]$", color='white', fontsize=11, ha='left', va='center')

ax.set_title("Frequency-Sampling FIR realization", fontsize=13, pad=15)
ax.set_xlim(-1.0, 9.5)
ax.set_ylim(-0.2, 2.2)
ax.axis('off')

plt.tight_layout()
plt.savefig("images/frequency_sampling_structure.png", dpi=300)
plt.close()

print("Lecture 16 images generated successfully.")
