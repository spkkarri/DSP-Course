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
# Plot: Radix-2 DIT FFT Butterfly Flow Graph
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.5))

# Draw horizontal lines for channels
ax.plot([0, 4], [2, 2], color='#e2e8f0', linewidth=2)
ax.plot([0, 4], [0, 0], color='#e2e8f0', linewidth=2)

# Draw cross paths
ax.plot([1, 3], [2, 0], color='#8b5cf6', linestyle='-', linewidth=2, label='Cross Addition/Subtraction')
ax.plot([1, 3], [0, 2], color='#0dd5c5', linestyle='-', linewidth=2)

# Draw arrow heads
ax.annotate('', xy=(3, 2), xytext=(1, 0), arrowprops=dict(arrowstyle="->", color='#0dd5c5', lw=2))
ax.annotate('', xy=(3, 0), xytext=(1, 2), arrowprops=dict(arrowstyle="->", color='#8b5cf6', lw=2))
ax.annotate('', xy=(4, 2), xytext=(3, 2), arrowprops=dict(arrowstyle="->", color='#e2e8f0', lw=2))
ax.annotate('', xy=(4, 0), xytext=(3, 0), arrowprops=dict(arrowstyle="->", color='#e2e8f0', lw=2))

# Draw multiplication/addition nodes
ax.plot([3, 3], [2, 0], 'o', color='#3b82f6', markersize=12)
ax.plot([1], [0], 'o', color='#f59e0b', markersize=10, label='Twiddle Multiplication')

# Add text labels
ax.text(-0.1, 2, r"$A = X_{m-1}[p]$", fontsize=11, color='#e2e8f0', ha='right', va='center')
ax.text(-0.1, 0, r"$B = X_{m-1}[q]$", fontsize=11, color='#e2e8f0', ha='right', va='center')

ax.text(1, -0.3, r"$\times W_N^r$", fontsize=11, color='#f59e0b', ha='center', va='center')

# Summation results
ax.text(4.1, 2, r"$X_m[p] = A + W_N^r B$", fontsize=11, color='#10b981', ha='left', va='center')
ax.text(4.1, 0, r"$X_m[q] = A - W_N^r B$", fontsize=11, color='#ef4444', ha='left', va='center')

# Add path multiplier signs
ax.text(2.8, 1.8, r"$+1$", fontsize=10, color='#e2e8f0')
ax.text(2.8, 0.2, r"$-1$", fontsize=10, color='#e2e8f0')

ax.set_title("Radix-2 Decimation-in-Time (DIT) Butterfly Computations", fontsize=13, pad=15)
ax.set_xlim(-1.5, 6.5)
ax.set_ylim(-0.8, 2.8)
ax.axis('off')

plt.tight_layout()
plt.savefig("images/fft_butterfly.png", dpi=300)
plt.close()

print("Lecture 10 images generated successfully.")
