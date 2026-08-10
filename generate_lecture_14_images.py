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
# Plot: Overlap-Save Method Visualization
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 4.5))

# Draw blocks
L = 6
M_minus_1 = 2
N = L + M_minus_1

# Block 1
x1 = np.arange(0, N)
y1 = np.zeros(N)
y1[0:M_minus_1] = 0.5 # Aliased/Discarded
y1[M_minus_1:N] = 1.0 - (np.arange(L)/L)

# Plot block stems
markerline, stemlines, baseline = ax.stem(x1, y1, linefmt='#8b5cf6', markerfmt='o', label='Block 1 Output')
plt.setp(markerline, color='#8b5cf6', markersize=6)
plt.setp(stemlines, color='#8b5cf6', linewidth=1.5)

# Highlight discarded region
ax.axvspan(0, M_minus_1, color=(239/255, 68/255, 68/255, 0.15), label='Discarded Region (Aliased)')
ax.text(M_minus_1/2, 0.8, "Discard\nAliased", color='#ef4444', fontweight='bold', ha='center', fontsize=9)

# Highlight saved region
ax.axvspan(M_minus_1, N, color=(16/255, 185/255, 129/255, 0.1), label='Saved Region (Valid)')
ax.text((M_minus_1 + N)/2, 0.8, "Save/Keep\nLinear Output", color='#10b981', fontweight='bold', ha='center', fontsize=9)

ax.set_title("Overlap-Save Method: Discarding Circular Aliasing", fontsize=13, pad=15)
ax.set_xlabel("Time Index n")
ax.set_ylabel("Amplitude")
ax.set_xticks(np.arange(0, 9))
ax.set_ylim(-0.2, 1.4)
ax.legend(loc='upper right')

plt.tight_layout()
plt.savefig("images/overlap_save.png", dpi=300)
plt.close()

print("Lecture 14 images generated successfully.")
