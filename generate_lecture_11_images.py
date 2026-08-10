import os
import matplotlib.pyplot as plt

os.makedirs("images", exist_ok=True)

# Dark mode styling parameters
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 9
plt.rcParams['axes.grid'] = False
plt.rcParams['figure.facecolor'] = '#0d121f'
plt.rcParams['axes.facecolor'] = '#0d121f'
plt.rcParams['savefig.facecolor'] = '#0d121f'

# -------------------------------------------------------------
# Plot: DIT vs. DIF Butterfly Structures Side-by-Side
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

# --- Ax1: Decimation in Time (DIT) ---
ax1.plot([0, 3], [2, 2], color='#e2e8f0', linewidth=1.5)
ax1.plot([0, 3], [0, 0], color='#e2e8f0', linewidth=1.5)
ax1.plot([0.5, 2.5], [2, 0], color='#8b5cf6', linewidth=1.5)
ax1.plot([0.5, 2.5], [0, 2], color='#0dd5c5', linewidth=1.5)

# Annotation for DIT
ax1.plot([0.5], [0], 'o', color='#f59e0b', markersize=8) # Twiddle multiplier
ax1.plot([2.5, 2.5], [2, 0], 'o', color='#3b82f6', markersize=10) # Adders

ax1.text(-0.1, 2, "$A$", fontsize=10, color='#e2e8f0', ha='right', va='center')
ax1.text(-0.1, 0, "$B$", fontsize=10, color='#e2e8f0', ha='right', va='center')
ax1.text(0.5, -0.25, r"$\times W_N^r$", color='#f59e0b', ha='center')

ax1.text(3.1, 2, r"$A + W_N^r B$", fontsize=10, color='#10b981', ha='left', va='center')
ax1.text(3.1, 0, r"$A - W_N^r B$", fontsize=10, color='#ef4444', ha='left', va='center')
ax1.text(2.35, 1.8, "+1", fontsize=8, color='#e2e8f0')
ax1.text(2.35, 0.2, "-1", fontsize=8, color='#e2e8f0')
ax1.set_title("Decimation-in-Time (DIT)\nMultiplication before Add/Sub", fontsize=11, color='#e2e8f0', pad=10)
ax1.set_xlim(-0.8, 4.2)
ax1.set_ylim(-0.6, 2.6)
ax1.axis('off')

# --- Ax2: Decimation in Frequency (DIF) ---
ax2.plot([0, 3], [2, 2], color='#e2e8f0', linewidth=1.5)
ax2.plot([0, 3], [0, 0], color='#e2e8f0', linewidth=1.5)
ax2.plot([0.5, 2.5], [2, 0], color='#8b5cf6', linewidth=1.5)
ax2.plot([0.5, 2.5], [0, 2], color='#0dd5c5', linewidth=1.5)

# Annotation for DIF
ax2.plot([0.5, 0.5], [2, 0], 'o', color='#3b82f6', markersize=10) # Adders
ax2.plot([2.5], [0], 'o', color='#f59e0b', markersize=8) # Twiddle multiplier

ax2.text(-0.1, 2, "$A$", fontsize=10, color='#e2e8f0', ha='right', va='center')
ax2.text(-0.1, 0, "$B$", fontsize=10, color='#e2e8f0', ha='right', va='center')
ax2.text(2.5, -0.25, r"$\times W_N^r$", color='#f59e0b', ha='center')

ax2.text(3.1, 2, r"$A + B$", fontsize=10, color='#10b981', ha='left', va='center')
ax2.text(3.1, 0, r"$(A - B) W_N^r$", fontsize=10, color='#ef4444', ha='left', va='center')
ax2.text(0.35, 1.8, "+1", fontsize=8, color='#e2e8f0')
ax2.text(0.35, 0.2, "-1", fontsize=8, color='#e2e8f0')
ax2.set_title("Decimation-in-Frequency (DIF)\nMultiplication after Add/Sub", fontsize=11, color='#e2e8f0', pad=10)
ax2.set_xlim(-0.8, 4.2)
ax2.set_ylim(-0.6, 2.6)
ax2.axis('off')

plt.tight_layout()
plt.savefig("images/dif_butterfly.png", dpi=300)
plt.close()

print("Lecture 11 images generated successfully.")
