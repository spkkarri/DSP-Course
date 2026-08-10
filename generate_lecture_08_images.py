import os
import numpy as np
import matplotlib.pyplot as plt

os.makedirs("images", exist_ok=True)

# Dark mode styling parameters
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.2
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['figure.facecolor'] = '#0d121f'
plt.rcParams['axes.facecolor'] = '#0d121f'
plt.rcParams['savefig.facecolor'] = '#0d121f'

# -------------------------------------------------------------
# Plot 1: Linear vs. Circular Shift Comparison
# -------------------------------------------------------------
x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
N = len(x)
shift = 3

# Linear shift (with zero padding)
x_linear = np.zeros(N)
x_linear[shift:] = x[:-shift]

# Circular shift
x_circular = np.roll(x, shift)

fig, axs = plt.subplots(3, 1, figsize=(8, 7), sharex=True)

# Original
axs[0].stem(np.arange(N), x, linefmt='#6366f1', markerfmt='o', basefmt='white')
axs[0].set_title("Original Sequence $x[n]$")
axs[0].set_ylabel("Amplitude")
axs[0].set_ylim(-0.5, 9)

# Linear Shift
axs[1].stem(np.arange(N), x_linear, linefmt='#ef4444', markerfmt='o', basefmt='white')
axs[1].set_title(f"Linear Shift by {shift} samples (Last values lost, zeros appended)")
axs[1].set_ylabel("Amplitude")
axs[1].set_ylim(-0.5, 9)

# Circular Shift
axs[2].stem(np.arange(N), x_circular, linefmt='#10b981', markerfmt='o', basefmt='white')
axs[2].set_title(r"Circular Shift $x[((n - 3))_8]$ (Values wrap around)")
axs[2].set_xlabel("Time Index n")
axs[2].set_ylabel("Amplitude")
axs[2].set_ylim(-0.5, 9)

plt.tight_layout()
plt.savefig("images/circular_shift_comparison.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Plot 2: Circular vs. Linear Convolution (with Time Aliasing)
# -------------------------------------------------------------
x1 = np.array([1, 1, 1, 1])
x2 = np.array([1, 1, 1, 1])

# Linear convolution
y_linear = np.convolve(x1, x2)
n_lin = np.arange(len(y_linear))

# 8-point circular convolution (no aliasing since N >= 7)
y_circ8 = np.convolve(x1, x2)
# circular convolution of length 8 is just linear padded
y_circ8 = np.pad(y_circ8, (0, 8 - len(y_circ8)))

# 5-point circular convolution (aliasing since N = 5 < 7)
# y_c5[n] = y_l[n] + y_l[n+5]
y_circ5 = np.zeros(5)
for n in range(5):
    val = y_linear[n]
    if n + 5 < len(y_linear):
        val += y_linear[n + 5]
    y_circ5[n] = val

fig, axs = plt.subplots(3, 1, figsize=(8, 8))

# Linear Convolution
axs[0].stem(n_lin, y_linear, linefmt='#8b5cf6', markerfmt='o', basefmt='white')
axs[0].set_title("Linear Convolution $y_{linear}[n] = x_1[n] * x_2[n]$ (Length = 7)")
axs[0].set_xlim(-0.5, 10)
axs[0].set_ylim(-0.2, 4.5)

# Circular Convolution N=8
axs[1].stem(np.arange(8), y_circ8, linefmt='#0dd5c5', markerfmt='o', basefmt='white')
axs[1].set_title("8-Point Circular Convolution $y_{circ8}[n]$ (No Aliasing, $N \geq 7$)")
axs[1].set_xlim(-0.5, 10)
axs[1].set_ylim(-0.2, 4.5)

# Circular Convolution N=5
axs[2].stem(np.arange(5), y_circ5, linefmt='#ef4444', markerfmt='o', basefmt='white')
axs[2].set_title("5-Point Circular Convolution $y_{circ5}[n]$ (Aliasing occurs: tail wraps around)")
axs[2].set_xlim(-0.5, 10)
axs[2].set_ylim(-0.2, 4.5)
axs[2].set_xlabel("Time Index n")

plt.tight_layout()
plt.savefig("images/circular_vs_linear_convolution.png", dpi=300)
plt.close()

print("Lecture 8 images generated successfully.")
