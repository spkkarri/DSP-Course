import os
import numpy as np
import matplotlib.pyplot as plt

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
# Plot: Radix-4 FFT Butterfly Schematic
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))

# Draw horizontal lines for channels
y_vals = [3, 2, 1, 0]
colors = ['#6366f1', '#8b5cf6', '#0dd5c5', '#10b981']

for y, c in zip(y_vals, colors):
    ax.plot([0, 4], [y, y], color='#e2e8f0', linewidth=1.5)

# Butterfly crossing box
ax.fill_between([1.2, 2.8], -0.4, 3.4, color='#1f2937', alpha=0.9, edgecolor='#4b5563', linewidth=1.5)
ax.text(2, 1.5, "4-Point DFT\n(Radix-4 Butterfly)", color='white', fontsize=12, fontweight='bold', ha='center', va='center')

# Inputs
ax.text(-0.2, 3, r"$x[n]$", color=colors[0], fontsize=11, ha='right', va='center')
ax.text(-0.2, 2, r"$x[n + N/4] \cdot W_N^{k}$", color=colors[1], fontsize=11, ha='right', va='center')
ax.text(-0.2, 1, r"$x[n + N/2] \cdot W_N^{2k}$", color=colors[2], fontsize=11, ha='right', va='center')
ax.text(-0.2, 0, r"$x[n + 3N/4] \cdot W_N^{3k}$", color=colors[3], fontsize=11, ha='right', va='center')

# Outputs
ax.text(4.2, 3, r"$X[k]$", color=colors[0], fontsize=11, ha='left', va='center')
ax.text(4.2, 2, r"$X[k + N/4]$", color=colors[1], fontsize=11, ha='left', va='center')
ax.text(4.2, 1, r"$X[k + N/2]$", color=colors[2], fontsize=11, ha='left', va='center')
ax.text(4.2, 0, r"$X[k + 3N/4]$", color=colors[3], fontsize=11, ha='left', va='center')

# Draw labels inside the box for matrix elements (columns)
ax.text(1.3, 3, "1", color='#e2e8f0', fontsize=8, ha='left', va='center')
ax.text(1.3, 2, "1", color='#e2e8f0', fontsize=8, ha='left', va='center')
ax.text(1.3, 1, "1", color='#e2e8f0', fontsize=8, ha='left', va='center')
ax.text(1.3, 0, "1", color='#e2e8f0', fontsize=8, ha='left', va='center')

ax.text(2.7, 3, "1", color='#e2e8f0', fontsize=8, ha='right', va='center')
ax.text(2.7, 2, "-j", color='#0dd5c5', fontsize=8, ha='right', va='center')
ax.text(2.7, 1, "-1", color='#8b5cf6', fontsize=8, ha='right', va='center')
ax.text(2.7, 0, "j", color='#10b981', fontsize=8, ha='right', va='center')

ax.set_title("Radix-4 Decimation-in-Time Butterfly structure", fontsize=13, pad=15)
ax.set_xlim(-1.8, 5.8)
ax.set_ylim(-0.8, 3.8)
ax.axis('off')

plt.tight_layout()
plt.savefig("images/radix4_butterfly.png", dpi=300)
plt.close()

print("Lecture 12 images generated successfully.")
