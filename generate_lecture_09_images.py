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
# Plot: DFT vs. FFT Multiplications Complexity
# -------------------------------------------------------------
N_values = np.array([4, 8, 16, 32, 64, 128, 256, 512, 1024])
dft_mults = N_values ** 2
fft_mults = (N_values / 2) * np.log2(N_values)

fig, ax = plt.subplots(figsize=(8, 5))
ax.loglog(N_values, dft_mults, color='#ef4444', marker='o', linestyle='-', linewidth=2, label='Direct DFT ($N^2$)')
ax.loglog(N_values, fft_mults, color='#10b981', marker='s', linestyle='-', linewidth=2, label='Radix-2 FFT ($(N/2)\log_2 N$)')

# Annotate values for N=1024
ax.annotate(f'DFT: {dft_mults[-1]:,}', xy=(1024, dft_mults[-1]), xytext=(300, dft_mults[-1]*0.7),
            arrowprops=dict(facecolor='#ef4444', shrink=0.08, width=1, headwidth=6))
ax.annotate(f'FFT: {int(fft_mults[-1]):,}', xy=(1024, fft_circ := fft_mults[-1]), xytext=(350, fft_circ*5.0),
            arrowprops=dict(facecolor='#10b981', shrink=0.08, width=1, headwidth=6))

ax.set_title("Computational Complexity: Direct DFT vs. Radix-2 FFT")
ax.set_xlabel("Signal Length N")
ax.set_ylabel("Number of Complex Multiplications")
ax.set_xticks(N_values)
ax.set_xticklabels(N_values.astype(str))
ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
ax.legend(loc='upper left')

plt.tight_layout()
plt.savefig("images/dft_vs_fft_complexity.png", dpi=300)
plt.close()

print("Lecture 9 images generated successfully.")
