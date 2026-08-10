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
# Plot 1: DTFT vs. DFT (Spectral Sampling)
# -------------------------------------------------------------
# Let's take a rectangular pulse sequence x[n] = 1 for n=0..4, N_dft = 8
N_dft = 8
x = np.ones(5)

# Calculate continuous DTFT
omega = np.linspace(0, 2*np.pi, 500)
X_dtft = np.zeros_like(omega, dtype=complex)
for n_idx, val in enumerate(x):
    X_dtft += val * np.exp(-1j * omega * n_idx)
mag_dtft = np.abs(X_dtft)

# Calculate 8-point DFT
X_dft = np.fft.fft(x, n=N_dft)
omega_dft = np.linspace(0, 2*np.pi, N_dft, endpoint=False)
mag_dft = np.abs(X_dft)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(omega, mag_dtft, color='#8b5cf6', linewidth=2.0, label='Continuous DTFT $|X(e^{j\omega})|$')
ax.stem(omega_dft, mag_dft, linefmt='#0dd5c5', markerfmt='o', basefmt='white', label='8-point DFT samples $X[k]$')

ax.set_title("DFT as Samples of the DTFT Spectrum")
ax.set_xlabel(r"Normalized Frequency $\omega$ (rad/sample)")
ax.set_ylabel("Magnitude")
ax.set_xlim(-0.1, 2*np.pi + 0.1)
ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
ax.set_xticklabels(['0', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$'])
ax.legend(loc='upper right')

plt.tight_layout()
plt.savefig("images/dtft_vs_dft.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Plot 2: DFT Basis Functions (N = 8)
# -------------------------------------------------------------
# We'll plot the basis functions for k = 0, 1, 2, 3
N = 8
n = np.arange(N)

fig, axs = plt.subplots(4, 2, figsize=(10, 8), sharex=True)

for k in range(4):
    basis = np.exp(-1j * 2 * np.pi * k * n / N)
    
    # Real part (Cosine)
    axs[k, 0].stem(n, np.real(basis), linefmt='#10b981', markerfmt='o', basefmt='white')
    axs[k, 0].set_ylabel(f"k = {k}")
    axs[k, 0].set_ylim(-1.2, 1.2)
    if k == 0:
        axs[k, 0].set_title(r"Real Part: $\cos(2\pi k n / 8)$")
    
    # Imaginary part (Sine)
    axs[k, 1].stem(n, np.imag(basis), linefmt='#ef4444', markerfmt='o', basefmt='white')
    axs[k, 1].set_ylim(-1.2, 1.2)
    if k == 0:
        axs[k, 1].set_title(r"Imaginary Part: $-\sin(2\pi k n / 8)$")

# Add x labels to bottom plots
axs[3, 0].set_xlabel("Time Index n")
axs[3, 1].set_xlabel("Time Index n")

plt.suptitle("DFT Basis Complex Exponentials (N=8)", fontsize=14, y=0.98, color='white')
plt.tight_layout()
plt.savefig("images/dft_basis_functions.png", dpi=300)
plt.close()

print("Lecture 7 images generated successfully.")
