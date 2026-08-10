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
# Plot 1: FIR Direct Form Realization Schematic
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 3.5))

# Draw paths
# x[n] input line
ax.plot([0, 7], [2, 2], color='#e2e8f0', linewidth=1.5)

# Delay blocks
delays = [2, 4.5]
for dx in delays:
    # Delay box
    ax.fill_between([dx - 0.4, dx + 0.4], 1.7, 2.3, color='#1f2937', edgecolor='#4b5563', linewidth=1.5)
    ax.text(dx, 2, r"$z^{-1}$", color='white', fontsize=11, ha='center', va='center', fontweight='bold')

# Coefficient paths and multiplier circles
coef_x = [0.8, 3.25, 5.75]
coef_labels = [r"$h[0]$", r"$h[1]$", r"$h[2]$"]
colors = ['#6366f1', '#8b5cf6', '#0dd5c5']

# Accumulation sum path
ax.plot([0.8, 7], [0, 0], color='#e2e8f0', linewidth=1.5)

for cx, label, col in zip(coef_x, coef_labels, colors):
    # Vertical line down
    ax.plot([cx, cx], [2, 0], color='#e2e8f0', linestyle='--', linewidth=1.2)
    # Multiplier circle
    circle_mult = plt.Circle((cx, 1.0), 0.25, facecolor=col, edgecolor='white', linewidth=1, alpha=0.9)
    ax.add_patch(circle_mult)
    ax.text(cx, 1.0, label, color='black', fontsize=9, fontweight='bold', ha='center', va='center')
    # Sum nodes on the bottom line
    if cx > 0.8:
        circle_sum = plt.Circle((cx, 0), 0.18, facecolor='#10b981', edgecolor='white', linewidth=1)
        ax.add_patch(circle_sum)
        ax.text(cx, 0, "+", color='black', fontsize=10, fontweight='bold', ha='center', va='center')

# Inputs/Outputs
ax.text(-0.2, 2, r"$x[n]$", color='white', fontsize=11, ha='right', va='center')
ax.text(7.2, 0, r"$y[n]$", color='white', fontsize=11, ha='left', va='center')

ax.set_title("FIR Direct-Form realization (3-tap Transversal Filter)", fontsize=13, pad=15)
ax.set_xlim(-1.0, 8.0)
ax.set_ylim(-0.8, 2.8)
ax.axis('off')

plt.tight_layout()
plt.savefig("images/fir_direct_form.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Plot 2: FIR Cascade Form Realization Schematic
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 3.0))

# Blocks
ax.plot([0, 8], [1, 1], color='#e2e8f0', linewidth=1.5)

# Cascade stages boxes
ax.fill_between([1.5, 3.5], 0.4, 1.6, color='#1f2937', edgecolor='#6366f1', linewidth=1.5)
ax.text(2.5, 1, r"Second-Order" + "\n" + r"Section $H_1(z)$", color='white', fontsize=10, ha='center', va='center')

ax.fill_between([4.5, 6.5], 0.4, 1.6, color='#1f2937', edgecolor='#8b5cf6', linewidth=1.5)
ax.text(5.5, 1, r"Second-Order" + "\n" + r"Section $H_2(z)$", color='white', fontsize=10, ha='center', va='center')

# Labels
ax.text(-0.2, 1, r"$x[n]$", color='white', fontsize=11, ha='right', va='center')
ax.text(0.7, 1.2, r"Input", color=(1.0, 1.0, 1.0, 0.4), fontsize=8, ha='center')

ax.text(4.0, 1.2, r"$y_1[n]$", color='#0dd5c5', fontsize=10, ha='center', va='center')

ax.text(8.2, 1, r"$y[n]$", color='white', fontsize=11, ha='left', va='center')

ax.set_title(r"FIR Cascade-Form realization ($H(z) = H_1(z) \cdot H_2(z)$)", fontsize=13, pad=15)
ax.set_xlim(-1.0, 9.0)
ax.set_ylim(-0.2, 2.2)
ax.axis('off')

plt.tight_layout()
plt.savefig("images/fir_cascade_form.png", dpi=300)
plt.close()

print("Lecture 15 images generated successfully.")
