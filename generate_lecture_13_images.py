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
# Plot: Overlap-Add Method Visualization
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 4.5))

# Draw blocks
# Block 1 (length L=6, M-1=2 overlap)
L = 6
M_minus_1 = 2
N = L + M_minus_1

# Timeline offsets
x1 = np.arange(0, N)
y1 = np.zeros(N)
y1[0:L] = 1.0 - (np.arange(L)/L)
y1[L:N] = y1[L-1] * np.exp(-np.arange(1, M_minus_1+1))

x2 = np.arange(L, L + N)
y2 = np.zeros(N)
y2[0:L] = 0.8 * np.sin(np.arange(L) * np.pi / L)
y2[L:N] = y2[L-1] * np.exp(-np.arange(1, M_minus_1+1))

# Plot block stems
markerline, stemlines, baseline = ax.stem(x1, y1, linefmt='#0dd5c5', markerfmt='o', label='Block 1 Output ($y_1[n]$)')
plt.setp(markerline, color='#0dd5c5', markersize=6)
plt.setp(stemlines, color='#0dd5c5', linewidth=1.5)

markerline, stemlines, baseline = ax.stem(x2, y2 + 1.2, linefmt='#8b5cf6', markerfmt='s', label='Block 2 Output ($y_2[n]$)')
plt.setp(markerline, color='#8b5cf6', markersize=6)
plt.setp(stemlines, color='#8b5cf6', linewidth=1.5)

# Highlight overlap region with valid tuple color
ax.axvspan(L, L + M_minus_1, color=(245/255, 158/255, 11/255, 0.15), label='Overlap Region ($M-1$ samples)')
ax.text((L + L + M_minus_1)/2, 0.6, "Overlap & Add\n($y_1[n] + y_2[n]$)", color='#f59e0b', fontweight='bold', ha='center', fontsize=9)

# Draw arrows showing addition
ax.annotate('', xy=(6.5, 0.35), xytext=(6.5, 1.2), arrowprops=dict(arrowstyle="->", color='#f59e0b', lw=1.5))
ax.annotate('', xy=(7.5, 0.25), xytext=(7.5, 1.3), arrowprops=dict(arrowstyle="->", color='#f59e0b', lw=1.5))

ax.set_title("Overlap-Add Method: Reconstructing Filtered Output", fontsize=13, pad=15)
ax.set_xlabel("Time Index n")
ax.set_ylabel("Amplitude")
ax.set_xticks(np.arange(0, 16))
ax.set_ylim(-0.2, 2.5)
ax.legend(loc='upper right')

plt.tight_layout()
plt.savefig("images/overlap_add.png", dpi=300)
plt.close()

print("Lecture 13 images generated successfully.")
