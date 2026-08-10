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
# Plot: Parallel IIR SFG Detailed
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 3.8))

# Input distribution line
ax.plot([0, 1.5], [2.0, 2.0], color='#e2e8f0', linewidth=1.5)
ax.plot([1.5, 1.5], [0.5, 3.5], color='#e2e8f0', linewidth=1.5)
ax.plot([1.5, 2.2], [3.5, 3.5], color='#e2e8f0', linewidth=1.5)
ax.plot([1.5, 2.2], [2.0, 2.0], color='#e2e8f0', linewidth=1.5)
ax.plot([1.5, 2.2], [0.5, 0.5], color='#e2e8f0', linewidth=1.5)

# Branch arrows
ax.annotate("", xy=(2.0, 3.5), xytext=(1.5, 3.5), arrowprops=dict(arrowstyle="->", color='#e2e8f0'))
ax.annotate("", xy=(2.0, 2.0), xytext=(1.5, 2.0), arrowprops=dict(arrowstyle="->", color='#e2e8f0'))
ax.annotate("", xy=(2.0, 0.5), xytext=(1.5, 0.5), arrowprops=dict(arrowstyle="->", color='#e2e8f0'))

# Stage blocks
ax.fill_between([2.2, 5.0], 3.1, 3.9, color='#1f2937', edgecolor='#8b5cf6', linewidth=1.5)
ax.text(3.6, 3.5, r"Section 1: $H_1(z)$", color='white', fontsize=9.5, ha='center', va='center')

ax.fill_between([2.2, 5.0], 1.6, 2.4, color='#1f2937', edgecolor='#3b82f6', linewidth=1.5)
ax.text(3.6, 2.0, r"Section 2: $H_2(z)$", color='white', fontsize=9.5, ha='center', va='center')

ax.fill_between([2.2, 5.0], 0.1, 0.9, color='#1f2937', edgecolor='#10b981', linewidth=1.5)
ax.text(3.6, 0.5, r"Direct Term: $C$", color='white', fontsize=9.5, ha='center', va='center')

# Output collection line
ax.plot([5.0, 5.8], [3.5, 3.5], color='#e2e8f0', linewidth=1.5)
ax.plot([5.0, 5.8], [2.0, 2.0], color='#e2e8f0', linewidth=1.5)
ax.plot([5.0, 5.8], [0.5, 0.5], color='#e2e8f0', linewidth=1.5)
ax.plot([5.8, 5.8], [0.5, 3.5], color='#e2e8f0', linewidth=1.5)

# Output sum node
ax.add_patch(plt.Circle((5.8, 2.0), 0.22, facecolor='#10b981', edgecolor='white', linewidth=1))
ax.text(5.8, 2.0, "+", color='black', fontsize=12, fontweight='bold', ha='center', va='center')

# Final output line
ax.plot([6.0, 7.8], [2.0, 2.0], color='#e2e8f0', linewidth=1.5)
ax.annotate("", xy=(7.4, 2.0), xytext=(6.0, 2.0), arrowprops=dict(arrowstyle="->", color='#e2e8f0'))

# Labels
ax.text(-0.2, 2.0, r"$x[n]$", color='white', fontsize=11, ha='right', va='center')
ax.text(8.0, 2.0, r"$y[n]$", color='white', fontsize=11, ha='left', va='center')

ax.set_title("Parallel IIR Realization detailed SFG", fontsize=13, pad=15)
ax.set_xlim(-1.0, 9.0)
ax.set_ylim(-0.2, 4.2)
ax.axis('off')

plt.tight_layout()
plt.savefig("images/iir_parallel_sfg.png", dpi=300)
plt.close()

print("Lecture 19 images generated successfully.")
