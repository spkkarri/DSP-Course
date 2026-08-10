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
# Plot 1: Cascade IIR realization
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 3.0))

# Horizontal flow line
ax.plot([0, 8], [1, 1], color='#e2e8f0', linewidth=1.5)

# First block (SOS 1)
ax.fill_between([1.2, 3.2], 0.4, 1.6, color='#1f2937', edgecolor='#6366f1', linewidth=1.5)
ax.text(2.2, 1, r"$H_1(z) = \frac{b_{01} + b_{11}z^{-1} + b_{21}z^{-2}}{1 + a_{11}z^{-1} + a_{21}z^{-2}}$", color='white', fontsize=9, ha='center', va='center')

# Second block (SOS 2)
ax.fill_between([4.5, 6.5], 0.4, 1.6, color='#1f2937', edgecolor='#10b981', linewidth=1.5)
ax.text(5.5, 1, r"$H_2(z) = \frac{b_{02} + b_{12}z^{-1} + b_{22}z^{-2}}{1 + a_{12}z^{-1} + a_{22}z^{-2}}$", color='white', fontsize=9, ha='center', va='center')

# Direction arrows and labels
ax.text(-0.2, 1, r"$x[n]$", color='white', fontsize=11, ha='right', va='center')
ax.text(3.85, 1.2, r"$y_1[n]$", color='#6366f1', fontsize=9, ha='center', va='center')
ax.text(8.2, 1, r"$y[n]$", color='white', fontsize=11, ha='left', va='center')

ax.set_title("Cascade (Serial) IIR realization (SOS 1 followed by SOS 2)", fontsize=13, pad=15)
ax.set_xlim(-1.0, 9.0)
ax.set_ylim(-0.2, 2.0)
ax.axis('off')

plt.tight_layout()
plt.savefig("images/iir_cascade.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Plot 2: Parallel IIR realization
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 3.5))

# Input branches
ax.plot([0, 1.5], [1.5, 1.5], color='#e2e8f0', linewidth=1.5)
ax.plot([1.5, 1.5], [0.5, 2.5], color='#e2e8f0', linewidth=1.5)
ax.plot([1.5, 2.2], [2.5, 2.5], color='#e2e8f0', linewidth=1.5)
ax.plot([1.5, 2.2], [1.5, 1.5], color='#e2e8f0', linewidth=1.5)
ax.plot([1.5, 2.2], [0.5, 0.5], color='#e2e8f0', linewidth=1.5)

# Parallel blocks
ax.fill_between([2.2, 4.8], 2.1, 2.9, color='#1f2937', edgecolor='#8b5cf6', linewidth=1.5)
ax.text(3.5, 2.5, r"$H_1(z) = \frac{\beta_{01} + \beta_{11}z^{-1}}{1 + a_{11}z^{-1} + a_{21}z^{-2}}$", color='white', fontsize=8.5, ha='center', va='center')

ax.fill_between([2.2, 4.8], 1.1, 1.9, color='#1f2937', edgecolor='#3b82f6', linewidth=1.5)
ax.text(3.5, 1.5, r"$H_2(z) = \frac{\beta_{02} + \beta_{12}z^{-1}}{1 + a_{12}z^{-1} + a_{22}z^{-2}}$", color='white', fontsize=8.5, ha='center', va='center')

ax.fill_between([2.2, 4.8], 0.1, 0.9, color='#1f2937', edgecolor='#f59e0b', linewidth=1.5)
ax.text(3.5, 0.5, r"Direct Term: $C$", color='white', fontsize=8.5, ha='center', va='center')

# Output branches and summing node
ax.plot([4.8, 5.8], [2.5, 2.5], color='#e2e8f0', linewidth=1.5)
ax.plot([4.8, 5.8], [1.5, 1.5], color='#e2e8f0', linewidth=1.5)
ax.plot([4.8, 5.8], [0.5, 0.5], color='#e2e8f0', linewidth=1.5)
ax.plot([5.8, 5.8], [0.5, 2.5], color='#e2e8f0', linewidth=1.5)

# Sum junction
ax.add_patch(plt.Circle((5.8, 1.5), 0.22, facecolor='#10b981', edgecolor='white', linewidth=1))
ax.text(5.8, 1.5, "+", color='black', fontsize=12, fontweight='bold', ha='center', va='center')

# Final output path
ax.plot([6.0, 7.5], [1.5, 1.5], color='#e2e8f0', linewidth=1.5)

# Input/Output labels
ax.text(-0.2, 1.5, r"$x[n]$", color='white', fontsize=11, ha='right', va='center')
ax.text(7.7, 1.5, r"$y[n]$", color='white', fontsize=11, ha='left', va='center')

ax.set_title("Parallel IIR realization (SOS channels added in parallel)", fontsize=13, pad=15)
ax.set_xlim(-1.0, 8.5)
ax.set_ylim(-0.2, 3.2)
ax.axis('off')

plt.tight_layout()
plt.savefig("images/iir_parallel.png", dpi=300)
plt.close()

print("Lecture 18 images generated successfully.")
