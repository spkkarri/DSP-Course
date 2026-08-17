import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch

os.makedirs("images", exist_ok=True)

plt.style.use('dark_background')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.2
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['figure.facecolor'] = '#0d121f'
plt.rcParams['axes.facecolor'] = '#0d121f'
plt.rcParams['savefig.facecolor'] = '#0d121f'

def draw_zplane(ax, xlim=2.0, ylim=2.0, title="Z-Plane"):
    ax.axhline(0, color='white', linewidth=0.8, alpha=0.3)
    ax.axvline(0, color='white', linewidth=0.8, alpha=0.3)
    uc = Circle((0, 0), 1.0, color='#6366f1', fill=False, linestyle='--', linewidth=1.5, label=r'Unit Circle ($|z|=1$)')
    ax.add_patch(uc)
    ax.set_aspect('equal')
    ax.set_xlim(-xlim, xlim)
    ax.set_ylim(-ylim, ylim)
    ax.set_xlabel('Real Part (Re)')
    ax.set_ylabel('Imag Part (Im)')
    ax.set_title(title, fontsize=11, color='#38bdf8', fontweight='bold')

# ==============================================================================
# LECTURE 6: Inverse Z-Transform & Stability Analysis
# ==============================================================================
print("1/25. Generating Lecture 6 images...")
fig, ax = plt.subplots(figsize=(7, 7))
draw_zplane(ax, xlim=1.8, ylim=1.8, title="Z-Plane Stability Regions & Pole Dynamics")
stable_disk = Circle((0, 0), 1.0, color='#10b981', alpha=0.15, label=r'Stable Region ($|z| < 1$)')
ax.add_patch(stable_disk)
ax.plot(0.6, 0, 'x', color='#10b981', markersize=10, markeredgewidth=2.5, label=r'Stable Real Pole ($z=0.6$)')
ax.plot([0.5, 0.5], [0.6, -0.6], 'x', color='#38bdf8', markersize=10, markeredgewidth=2.5, label=r'Stable Complex ($0.5 \pm j0.6$)')
ax.plot([0, 0], [1.0, -1.0], 'x', color='#f59e0b', markersize=10, markeredgewidth=2.5, label=r'Marginally Stable ($z=\pm j$)')
ax.plot(1.3, 0.4, 'x', color='#ef4444', markersize=10, markeredgewidth=2.5, label=r'Unstable Pole ($|z|>1$)')
ax.annotate("BIBO STABLE:\nPoles inside $|z|<1$\nDecaying Impulse Response", xy=(0.6, 0.0), xytext=(-1.7, 1.3),
            arrowprops=dict(facecolor='#10b981', shrink=0.05, width=1.5, headwidth=6),
            fontsize=8.5, color='#10b981', fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#1e293b', edgecolor='#10b981'))
ax.annotate("MARGINALLY STABLE:\nPoles ON $|z|=1$\nSustained Oscillation", xy=(0, 1.0), xytext=(-1.7, -1.5),
            arrowprops=dict(facecolor='#f59e0b', shrink=0.05, width=1.5, headwidth=6),
            fontsize=8.5, color='#f59e0b', fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#1e293b', edgecolor='#f59e0b'))
ax.annotate("UNSTABLE:\nPoles outside $|z|>1$\nExplosive Growth", xy=(1.3, 0.4), xytext=(0.6, 1.4),
            arrowprops=dict(facecolor='#ef4444', shrink=0.05, width=1.5, headwidth=6),
            fontsize=8.5, color='#ef4444', fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#1e293b', edgecolor='#ef4444'))
ax.legend(loc='lower right', fontsize=8)
plt.tight_layout()
plt.savefig("images/pole_zero_stability_l6.png", dpi=300)
plt.close()

fig, axs = plt.subplots(2, 2, figsize=(11, 7))
n = np.arange(0, 20)
h1 = (0.7)**n
axs[0, 0].stem(n, h1, linefmt='#10b981', markerfmt='C2o', basefmt='white')
axs[0, 0].set_title(r"Pole at $z=0.7$ (Positive Real) $\rightarrow h[n]=0.7^n u[n]$ (Monotonic Decay)", fontsize=9.5, color='#10b981')
axs[0, 0].set_xlabel('n (samples)'); axs[0, 0].set_ylabel('Amplitude')

h2 = (-0.7)**n
axs[0, 1].stem(n, h2, linefmt='#38bdf8', markerfmt='C0o', basefmt='white')
axs[0, 1].set_title(r"Pole at $z=-0.7$ (Negative Real) $\rightarrow h[n]=(-0.7)^n u[n]$ (Alternating Decay)", fontsize=9.5, color='#38bdf8')
axs[0, 1].set_xlabel('n (samples)'); axs[0, 1].set_ylabel('Amplitude')

r = 0.8; w0 = np.pi/4
h3 = (r**n) * np.cos(w0 * n)
axs[1, 0].stem(n, h3, linefmt='#a855f7', markerfmt='C4o', basefmt='white')
axs[1, 0].set_title(r"Poles at $0.8 e^{\pm j\pi/4}$ $\rightarrow h[n]=0.8^n \cos(\pi n/4) u[n]$ (Damped Sinusoid)", fontsize=9.5, color='#a855f7')
axs[1, 0].set_xlabel('n (samples)'); axs[1, 0].set_ylabel('Amplitude')

h4 = np.cos(w0 * n)
axs[1, 1].stem(n, h4, linefmt='#f59e0b', markerfmt='C1o', basefmt='white')
axs[1, 1].set_title(r"Poles at $e^{\pm j\pi/4}$ $\rightarrow h[n]=\cos(\pi n/4) u[n]$ (Sustained Oscillation)", fontsize=9.5, color='#f59e0b')
axs[1, 1].set_xlabel('n (samples)'); axs[1, 1].set_ylabel('Amplitude')
plt.tight_layout()
plt.savefig("images/impulse_response_modes.png", dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(10, 4.5))
n_pfe = np.arange(0, 15)
mode_a = 2.0 * (0.8**n_pfe); mode_b = -1.0 * (0.4**n_pfe); total_h = mode_a + mode_b
ax.plot(n_pfe, mode_a, '--', color='#38bdf8', label=r'Mode A: $2(0.8)^n u[n]$ (Slow Decay)', alpha=0.8)
ax.plot(n_pfe, mode_b, '--', color='#ef4444', label=r'Mode B: $-1(0.4)^n u[n]$ (Fast Decay)', alpha=0.8)
markerline, stemlines, baseline = ax.stem(n_pfe, total_h, linefmt='#10b981', markerfmt='go', basefmt='white', label=r'Total $h[n] = 2(0.8)^n - (0.4)^n$')
plt.setp(stemlines, 'linewidth', 2)
ax.set_title("Partial Fraction Expansion: Total Impulse Response as Superposition of Modes", fontsize=11, color='#10b981', fontweight='bold')
ax.set_xlabel("Sample index $n$"); ax.set_ylabel("Amplitude $h[n]$")
ax.legend(loc='upper right', fontsize=9)
plt.tight_layout()
plt.savefig("images/pfe_decomposition_modes.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 7: Discrete Fourier Transform (DFT) & Matrix Formulation
# ==============================================================================
print("2/25. Generating Lecture 7 images...")
omega = np.linspace(-np.pi, np.pi, 500)
X_dtft = np.sin(4 * omega / 2 + 1e-12) / np.sin(omega / 2 + 1e-12)
k_indices = np.arange(0, 8)
omega_k = 2 * np.pi * k_indices / 8
omega_k_disp = np.where(omega_k > np.pi, omega_k - 2*np.pi, omega_k)
sorted_idx = np.argsort(omega_k_disp)
omega_k_disp = omega_k_disp[sorted_idx]
X_dft_samples = np.sin(4 * omega_k_disp / 2 + 1e-12) / np.sin(omega_k_disp / 2 + 1e-12)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(omega, np.abs(X_dtft), color='#38bdf8', linewidth=2, label=r'Continuous DTFT $|X(e^{j\omega})|$', alpha=0.8)
markerline, stemlines, baseline = ax.stem(omega_k_disp, np.abs(X_dft_samples), linefmt='#f59e0b', markerfmt='D', basefmt='white', label=r'Sampled 8-point DFT $|X[k]|$ ($\omega_k = \frac{2\pi k}{8}$)')
plt.setp(stemlines, 'linewidth', 2)
plt.setp(markerline, 'markersize', 8, 'color', '#f59e0b')
ax.set_title(r"DTFT vs. DFT: Sampling the Continuous Spectrum at $N=8$ Uniform Angles", fontsize=11, color='#38bdf8', fontweight='bold')
ax.set_xlabel(r"Normalized Frequency $\omega$ (rad/sample)"); ax.set_ylabel("Magnitude $|X|$")
ax.set_xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
ax.set_xticklabels([r'$-\pi$', r'$-\pi/2$', '$0$', r'$\pi/2$', r'$\pi$'])
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig("images/dtft_vs_dft.png", dpi=300)
plt.close()

N = 8; n = np.arange(N)
fig, axs = plt.subplots(4, 2, figsize=(11, 8), sharex=True)
for k in range(4):
    basis_cos = np.cos(2 * np.pi * k * n / N); basis_sin = -np.sin(2 * np.pi * k * n / N)
    axs[k, 0].stem(n, basis_cos, linefmt='#0dd5c5', markerfmt='o', basefmt='white')
    axs[k, 0].set_ylabel(f"k = {k}", color='#0dd5c5', fontweight='bold')
    axs[k, 0].set_ylim(-1.3, 1.3)
    if k == 0:
        axs[k, 0].set_title(r"Real Basis: $\mathrm{Re}\{W_N^{kn}\} = \cos(2\pi kn / N)$", fontsize=10, color='#0dd5c5', fontweight='bold')
    axs[k, 1].stem(n, basis_sin, linefmt='#ef4444', markerfmt='s', basefmt='white')
    axs[k, 1].set_ylim(-1.3, 1.3)
    if k == 0:
        axs[k, 1].set_title(r"Imag Basis: $\mathrm{Im}\{W_N^{kn}\} = -\sin(2\pi kn / N)$", fontsize=10, color='#ef4444', fontweight='bold')
axs[3, 0].set_xlabel("Time sample index $n$"); axs[3, 1].set_xlabel("Time sample index $n$")
plt.suptitle(r"Orthogonal DFT Basis Functions ($N=8$, Harmonic Bins $k=0,1,2,3$)", fontsize=12, color='white', fontweight='bold', y=0.99)
plt.tight_layout()
plt.savefig("images/dft_basis_functions.png", dpi=300)
plt.close()

W = np.zeros((8, 8), dtype=complex)
for r in range(8):
    for c in range(8):
        W[r, c] = np.exp(-1j * 2 * np.pi * r * c / 8)
fig, axs = plt.subplots(1, 2, figsize=(11, 5))
im1 = axs[0].imshow(np.real(W), cmap='coolwarm', vmin=-1, vmax=1)
axs[0].set_title(r"$\mathrm{Re}\{W_8\}$ (Cosine Coefficients Matrix)", color='#38bdf8', fontweight='bold')
axs[0].set_xlabel("Column $n$ (0 to 7)"); axs[0].set_ylabel("Row $k$ (0 to 7)")
fig.colorbar(im1, ax=axs[0], fraction=0.046, pad=0.04)
im2 = axs[1].imshow(np.imag(W), cmap='coolwarm', vmin=-1, vmax=1)
axs[1].set_title(r"$\mathrm{Im}\{W_8\}$ (Sine Coefficients Matrix)", color='#ef4444', fontweight='bold')
axs[1].set_xlabel("Column $n$ (0 to 7)"); axs[1].set_ylabel("Row $k$ (0 to 7)")
fig.colorbar(im2, ax=axs[1], fraction=0.046, pad=0.04)
plt.suptitle(r"Vandermonde DFT Matrix $W_8$: Orthogonal Row Vectors ($W W^H = 8 I$)", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/dft_matrix_heatmaps.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 8: Properties of DFT & Circular Convolution
# ==============================================================================
print("3/25. Generating Lecture 8 images...")
x_orig_short = np.array([4, 3, 2, 1, 0, 0])
x_circ = np.roll(x_orig_short, 2)
fig, axs = plt.subplots(3, 1, figsize=(10, 6.5), sharex=True)
n_idx = np.arange(6)
axs[0].stem(n_idx, x_orig_short, linefmt='#38bdf8', markerfmt='o', basefmt='white')
axs[0].set_title(r"Original Sequence $x[n] = [4, 3, 2, 1, 0, 0]$ ($N=6$)", fontsize=10, color='#38bdf8', fontweight='bold')
axs[0].set_ylabel("Amplitude")
axs[1].stem(n_idx, [0, 0, 4, 3, 2, 1], linefmt='#10b981', markerfmt='s', basefmt='white')
axs[1].set_title("Linear Time Delay $x[n-2]$: Samples fall off edge without wrapping", fontsize=10, color='#10b981', fontweight='bold')
axs[1].set_ylabel("Amplitude")
axs[2].stem(n_idx, x_circ, linefmt='#f59e0b', markerfmt='D', basefmt='white')
axs[2].set_title(r"Circular Shift $x[((n-2))_6]$: Samples pushed past $N-1$ wrap around to beginning!", fontsize=10, color='#f59e0b', fontweight='bold')
axs[2].set_ylabel("Amplitude"); axs[2].set_xlabel("Index $n$")
plt.tight_layout()
plt.savefig("images/circular_shift_comparison.png", dpi=300)
plt.close()

x1 = np.array([1, 2, 3, 1]); x2 = np.array([2, 1, 4])
y_lin = np.convolve(x1, x2)
y_circ_4 = np.array([15, 9, 12, 11])
y_circ_6 = y_lin

fig, axs = plt.subplots(3, 1, figsize=(10, 7.5))
axs[0].stem(np.arange(len(y_lin)), y_lin, linefmt='#10b981', markerfmt='o', basefmt='white')
axs[0].set_title(r"1. True Linear Convolution: $y_{lin}[n] = x_1[n] * x_2[n]$ (Length $L_1+L_2-1 = 6$)", fontsize=10, color='#10b981', fontweight='bold')
axs[0].set_ylabel("Amplitude")
axs[1].stem(np.arange(len(y_circ_4)), y_circ_4, linefmt='#ef4444', markerfmt='s', basefmt='white')
axs[1].set_title(r"2. Unpadded Circular Conv ($N=4 < 6$): Time-Aliasing! ($y[0]=15, y[1]=9$)", fontsize=10, color='#ef4444', fontweight='bold')
axs[1].set_ylabel("Amplitude")
axs[2].stem(np.arange(len(y_circ_6)), y_circ_6, linefmt='#38bdf8', markerfmt='D', basefmt='white')
axs[2].set_title(r"3. Zero-Padded Circular Conv ($N=6 \geq L_1+L_2-1$): Matches Linear Conv Exactly!", fontsize=10, color='#38bdf8', fontweight='bold')
axs[2].set_ylabel("Amplitude"); axs[2].set_xlabel("Sample index $n$")
plt.tight_layout()
plt.savefig("images/circular_vs_linear_convolution.png", dpi=300)
plt.close()

N = 16
x_sym = np.array([1, 2, 3, 4, 3, 2, 1, 0, -1, -2, -1, 0, 1, 2, 3, 2])
X_sym = np.fft.fft(x_sym)
k = np.arange(N)
fig, axs = plt.subplots(1, 2, figsize=(11, 4.5))
axs[0].stem(k, np.abs(X_sym), linefmt='#38bdf8', markerfmt='o', basefmt='white')
axs[0].set_title(r"Magnitude $|X[k]|$: Even Symmetric ($|X[k]| = |X[N-k]|$)", fontsize=10, color='#38bdf8', fontweight='bold')
axs[0].set_xlabel("DFT Bin index $k$"); axs[0].set_ylabel("Magnitude")
axs[1].stem(k, np.angle(X_sym), linefmt='#ef4444', markerfmt='s', basefmt='white')
axs[1].set_title(r"Phase $\angle X[k]$: Odd Symmetric ($\angle X[k] = -\angle X[N-k]$)", fontsize=10, color='#ef4444', fontweight='bold')
axs[1].set_xlabel("DFT Bin index $k$"); axs[1].set_ylabel("Phase (rad)")
plt.suptitle("Hermitian Symmetry Property for Real Signals in DFT", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/dft_symmetry_and_parseval.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 9: Fast Fourier Transform (FFT) — Decimation in Time (DIT)
# ==============================================================================
print("4/25. Generating Lecture 9 images...")
N_vals = 2**np.arange(1, 13)
dft_mults = N_vals**2
fft_mults = (N_vals / 2) * np.log2(N_vals)
savings_pct = (1 - (fft_mults / dft_mults)) * 100

fig, axs = plt.subplots(1, 2, figsize=(12, 5))
axs[0].plot(N_vals, dft_mults, 'o-', color='#ef4444', linewidth=2, label=r'Direct DFT: $N^2$ Multiplications')
axs[0].plot(N_vals, fft_mults, 's-', color='#10b981', linewidth=2, label=r'Radix-2 FFT: $\frac{N}{2} \log_2 N$ Multiplications')
axs[0].set_xscale('log', base=2); axs[0].set_yscale('log')
axs[0].set_title("Computational Multiplications: DFT vs FFT (Log-Log Scale)", fontsize=10, color='#38bdf8', fontweight='bold')
axs[0].set_xlabel("Transform Length $N$"); axs[0].set_ylabel("Complex Multiplications")
axs[0].legend(loc='upper left')

axs[1].plot(N_vals, savings_pct, 'D-', color='#f59e0b', linewidth=2)
axs[1].set_xscale('log', base=2)
axs[1].set_title("Percentage Computational Savings of FFT over Direct DFT", fontsize=10, color='#f59e0b', fontweight='bold')
axs[1].set_xlabel("Transform Length $N$"); axs[1].set_ylabel("Savings (%)"); axs[1].set_ylim(0, 105)
axs[1].annotate('At $N=1024$:\nDirect DFT: 1,048,576 mults\nFFT: 5,120 mults\n> 99.5% SAVINGS!',
                xy=(1024, 99.5), xytext=(32, 45),
                arrowprops=dict(facecolor='#10b981', shrink=0.05, width=1.5, headwidth=6),
                fontsize=9, color='#10b981', fontweight='bold', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#10b981'))
plt.tight_layout()
plt.savefig("images/dft_vs_fft_complexity.png", dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(10, 5))
ax.set_facecolor('#0d121f'); ax.axis('off')
ax.text(0.1, 0.85, "n (Decimal)\n0 = 000_2\n1 = 001_2\n2 = 010_2\n3 = 011_2\n4 = 100_2\n5 = 101_2\n6 = 110_2\n7 = 111_2",
        fontsize=9.5, color='#38bdf8', bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor='#38bdf8'))
ax.text(0.48, 0.85, "Bit-Reversal Mapping\n000_2 -> 000_2 = 0\n001_2 -> 100_2 = 4\n010_2 -> 010_2 = 2\n011_2 -> 110_2 = 6\n100_2 -> 001_2 = 1\n101_2 -> 101_2 = 5\n110_2 -> 011_2 = 3\n111_2 -> 111_2 = 7",
        fontsize=9.5, color='#f59e0b', bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor='#f59e0b'))
ax.text(0.85, 0.85, "DIT Input Sequence\nx[0]\nx[4]\nx[2]\nx[6]\nx[1]\nx[5]\nx[3]\nx[7]",
        fontsize=9.5, color='#10b981', fontweight='bold', bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor='#10b981'))
ax.annotate('', xy=(0.42, 0.85), xytext=(0.32, 0.85), arrowprops=dict(facecolor='#38bdf8', shrink=0.05, width=2, headwidth=8))
ax.annotate('', xy=(0.80, 0.85), xytext=(0.70, 0.85), arrowprops=dict(facecolor='#f59e0b', shrink=0.05, width=2, headwidth=8))
ax.text(0.5, 0.25, "Physical Meaning in Radix-2 DIT-FFT:\nBy addressing inputs in bit-reversed order, the FFT algorithm can compute butterflies in-place,\noverwriting old values with new outputs at every stage, requiring zero additional memory!",
        ha='center', fontsize=10, color='white', bbox=dict(boxstyle='round,pad=0.6', facecolor='#111827', edgecolor='#10b981', linewidth=1.5))
ax.set_title(r"Radix-2 Decimation-In-Time (DIT) Bit-Reversal Mechanism ($N=8$)", fontsize=11, color='#38bdf8', fontweight='bold')
plt.tight_layout()
plt.savefig("images/dit_bit_reversal_tree.png", dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(9, 5))
ax.set_facecolor('#0d121f'); ax.axis('off')
ax.text(0.1, 0.75, "$A$ (Upper Input)", fontsize=12, color='#38bdf8', fontweight='bold')
ax.text(0.1, 0.25, "$B$ (Lower Input)", fontsize=12, color='#38bdf8', fontweight='bold')
ax.plot([0.3, 0.7], [0.75, 0.75], color='#38bdf8', linewidth=2.5)
ax.plot([0.3, 0.7], [0.25, 0.25], color='#38bdf8', linewidth=2.5)
ax.plot([0.3, 0.7], [0.75, 0.25], color='#ef4444', linewidth=2, linestyle='--')
ax.plot([0.3, 0.7], [0.25, 0.75], color='#10b981', linewidth=2, linestyle='--')
ax.plot(0.48, 0.25, 'o', color='#f59e0b', markersize=12)
ax.text(0.48, 0.15, r"$\times W_N^r$", fontsize=11, color='#f59e0b', fontweight='bold', ha='center')
ax.text(0.65, 0.35, "$-1$", fontsize=11, color='#ef4444', fontweight='bold')
ax.text(0.73, 0.75, r"$X = A + B \cdot W_N^r$", fontsize=12, color='#10b981', fontweight='bold')
ax.text(0.73, 0.25, r"$Y = A - B \cdot W_N^r$", fontsize=12, color='#ef4444', fontweight='bold')
ax.set_title("Fundamental 2-Point Butterfly Computation Unit (Radix-2 DIT)", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/fft_butterfly.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 10: FIR Filter Design — Window Method
# ==============================================================================
print("5/25. Generating Lecture 10 images...")
M = 31; n = np.arange(M)
w_rect = np.ones(M); w_hann = np.hanning(M); w_hamm = np.hamming(M); w_black = np.blackman(M)
N_fft = 1024; omega_w = np.linspace(-np.pi, np.pi, N_fft)
W_rect_db = 20 * np.log10(np.abs(np.fft.fftshift(np.fft.fft(w_rect, N_fft))) / np.sum(w_rect) + 1e-6)
W_hann_db = 20 * np.log10(np.abs(np.fft.fftshift(np.fft.fft(w_hann, N_fft))) / np.sum(w_hann) + 1e-6)
W_hamm_db = 20 * np.log10(np.abs(np.fft.fftshift(np.fft.fft(w_hamm, N_fft))) / np.sum(w_hamm) + 1e-6)
W_black_db = 20 * np.log10(np.abs(np.fft.fftshift(np.fft.fft(w_black, N_fft))) / np.sum(w_black) + 1e-6)

fig, axs = plt.subplots(1, 2, figsize=(12, 5))
axs[0].plot(n, w_rect, 'o-', label='Rectangular', color='#ef4444', alpha=0.8)
axs[0].plot(n, w_hann, 's-', label='Hann (Hanning)', color='#38bdf8', alpha=0.8)
axs[0].plot(n, w_hamm, '^-', label='Hamming', color='#10b981', alpha=0.8)
axs[0].plot(n, w_black, 'D-', label='Blackman', color='#f59e0b', alpha=0.8)
axs[0].set_title(r"Window Functions in Time Domain ($M=31$ Taps)", fontsize=10, color='#38bdf8', fontweight='bold')
axs[0].set_xlabel("Sample index $n$"); axs[0].set_ylabel("Amplitude $w[n]$")
axs[0].legend(loc='upper right', fontsize=8.5)

axs[1].plot(omega_w, W_rect_db, label='Rectangular (Sidelobe: -13 dB)', color='#ef4444', alpha=0.8)
axs[1].plot(omega_w, W_hann_db, label='Hann (Sidelobe: -31 dB)', color='#38bdf8', alpha=0.8)
axs[1].plot(omega_w, W_hamm_db, label='Hamming (Sidelobe: -43 dB)', color='#10b981', alpha=0.8)
axs[1].plot(omega_w, W_black_db, label='Blackman (Sidelobe: -58 dB)', color='#f59e0b', alpha=0.8)
axs[1].set_title("Window Spectra: Mainlobe Width vs Sidelobe Attenuation", fontsize=10, color='#f59e0b', fontweight='bold')
axs[1].set_xlabel(r"Normalized Frequency $\omega$ (rad/sample)"); axs[1].set_ylabel("Magnitude (dB)")
axs[1].set_ylim(-90, 5); axs[1].set_xlim(0, np.pi)
axs[1].set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
axs[1].set_xticklabels(['$0$', r'$\pi/4$', r'$\pi/2$', r'$3\pi/4$', r'$\pi$'])
axs[1].legend(loc='upper right', fontsize=8.5)
plt.tight_layout()
plt.savefig("images/fir_window_functions_time_freq.png", dpi=300)
plt.close()

n_ideal = np.arange(-30, 31); wc = np.pi / 3
h_ideal = np.sinc(wc * n_ideal / np.pi) * (wc / np.pi)
M = 21
idx_trunc = (n_ideal >= -(M-1)//2) & (n_ideal <= (M-1)//2)
h_rect = np.zeros_like(h_ideal); h_rect[idx_trunc] = h_ideal[idx_trunc]
h_hamm = np.zeros_like(h_ideal); h_hamm[idx_trunc] = h_ideal[idx_trunc] * np.hamming(M)

w_axis, H_rect_spec = np.linspace(0, np.pi, 500), np.zeros(500, dtype=complex)
H_hamm_spec = np.zeros(500, dtype=complex)
for i, w in enumerate(w_axis):
    H_rect_spec[i] = np.sum(h_rect * np.exp(-1j * w * n_ideal))
    H_hamm_spec[i] = np.sum(h_hamm * np.exp(-1j * w * n_ideal))

fig, axs = plt.subplots(1, 2, figsize=(12, 5))
axs[0].stem(n_ideal, h_ideal, linefmt='#64748b', markerfmt='o', basefmt='white', label=r'Infinite Ideal Sinc $h_d[n]$')
axs[0].stem(n_ideal[idx_trunc], h_rect[idx_trunc], linefmt='#ef4444', markerfmt='s', basefmt='white', label=r'Rectangular Truncation ($M=21$)')
axs[0].set_title(r"Ideal Sinc Truncation in Time Domain ($M=21$)", fontsize=10, color='#38bdf8', fontweight='bold')
axs[0].set_xlabel("Sample index $n$"); axs[0].set_ylabel("Amplitude")
axs[0].legend(loc='upper right', fontsize=8.5)

axs[1].axvline(wc, color='white', linestyle='--', alpha=0.5, label=r'Cutoff $\omega_c = \pi/3$')
axs[1].plot(w_axis, np.abs(H_rect_spec), color='#ef4444', linewidth=2, label='Rect Window: 8.9% Gibbs Overshoot & Ripple')
axs[1].plot(w_axis, np.abs(H_hamm_spec), color='#10b981', linewidth=2, label='Hamming Window: Smooth Passband, No Ripple')
axs[1].set_title("Gibbs Phenomenon in Frequency Response", fontsize=10, color='#ef4444', fontweight='bold')
axs[1].set_xlabel(r"Frequency $\omega$ (rad/sample)"); axs[1].set_ylabel(r"Magnitude $|H(e^{j\omega})|$")
axs[1].set_xticks([0, np.pi/6, np.pi/3, np.pi/2, 2*np.pi/3, np.pi])
axs[1].set_xticklabels(['$0$', r'$\pi/6$', r'$\omega_c=\pi/3$', r'$\pi/2$', r'$2\pi/3$', r'$\pi$'])
axs[1].legend(loc='upper right', fontsize=8.5)
plt.tight_layout()
plt.savefig("images/gibbs_phenomenon_truncation.png", dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(10, 4.5))
ax.set_facecolor('#0d121f'); ax.axis('off')
steps = [
    "Step 1: Specify Ideal Filter\nH_d(e^jw) = 1 for |w| <= w_c\nCompute h_d[n] = sin(w_c n) / (pi n)",
    "Step 2: Choose Window Type\nSelect window w[n] based on\nrequired stopband attenuation A_s\n(e.g., Hamming for 53 dB)",
    "Step 3: Determine Length M\nCalculate filter order from\ntransition width Delta_w:\nM ~ c / Delta_w + 1",
    "Step 4: Truncate & Shift\nh[n] = h_d[n - (M-1)/2] * w[n]\nfor 0 <= n <= M-1\n(Guarantees Causal Linear Phase)"
]
colors = ['#38bdf8', '#f59e0b', '#10b981', '#a855f7']
for idx, (step, col) in enumerate(zip(steps, colors)):
    x_pos = 0.05 + idx * 0.24
    ax.text(x_pos + 0.1, 0.5, step, ha='center', va='center', fontsize=8.8, color=col, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor=col, linewidth=1.5))
    if idx < 3:
        ax.annotate('', xy=(x_pos + 0.23, 0.5), xytext=(x_pos + 0.20, 0.5),
                    arrowprops=dict(facecolor='white', shrink=0.05, width=1.5, headwidth=6))
ax.set_title("Step-by-Step FIR Filter Design Procedure (Window Method)", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/fir_filter_design_workflow.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 11: FIR Filter Design — Frequency Sampling & Optimal Methods
# ==============================================================================
print("6/25. Generating Lecture 11 images...")
N = 16; k = np.arange(N); omega_k = 2 * np.pi * k / N
H_k = np.zeros(N); H_k[0:4] = 1.0; H_k[13:] = 1.0
omega_cont = np.linspace(0, 2*np.pi, 500)
H_interpolated = np.zeros_like(omega_cont, dtype=complex)
for idx, w in enumerate(omega_cont):
    for ki in range(N):
        if np.abs(w - omega_k[ki]) < 1e-6:
            H_interpolated[idx] += H_k[ki]
        else:
            term = (1 - np.exp(-1j * N * (w - omega_k[ki]))) / (1 - np.exp(-1j * (w - omega_k[ki])))
            H_interpolated[idx] += (H_k[ki] / N) * term

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(omega_cont, np.abs(H_interpolated), color='#38bdf8', linewidth=2, label=r'Continuous Interpolated $|H(e^{j\omega})|$')
markerline, stemlines, baseline = ax.stem(omega_k, H_k, linefmt='#f59e0b', markerfmt='s', basefmt='white', label=r'Specified Discrete Samples $H[k]$')
plt.setp(stemlines, 'linewidth', 2)
plt.setp(markerline, 'markersize', 8, 'color', '#f59e0b')
ax.set_title(r"FIR Frequency Sampling Method: Exact at Samples $H[k]$, Ripple in Between", fontsize=11, color='#38bdf8', fontweight='bold')
ax.set_xlabel(r"Normalized Frequency $\omega$ (rad/sample)"); ax.set_ylabel(r"Magnitude $|H(e^{j\omega})|$")
ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
ax.set_xticklabels(['$0$', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$'])
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig("images/freq_sampling_discrete_grid.png", dpi=300)
plt.close()

w_axis = np.linspace(0, np.pi, 500)
H_unopt = np.where(w_axis <= np.pi/3, 1.0 + 0.15*np.sin(3*w_axis*3), 0.15*np.abs(np.sinc((w_axis-np.pi/3)*4)))
H_opt = np.where(w_axis <= np.pi/3, 1.0 + 0.02*np.sin(3*w_axis*3), 0.02*np.abs(np.sinc((w_axis-np.pi/3)*4)))

fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(w_axis, 20*np.log10(H_unopt + 1e-4), color='#ef4444', linewidth=2, label='Without Transition Sample (Sidelobe: -16 dB)')
ax.plot(w_axis, 20*np.log10(H_opt + 1e-4), color='#10b981', linewidth=2, label='With 1 Optimized Transition Sample (Sidelobe: -45 dB)')
ax.set_title("Drastic Sidelobe Suppression by Adding 1 Optimized Transition Sample", fontsize=11, color='#10b981', fontweight='bold')
ax.set_xlabel(r"Frequency $\omega$ (rad/sample)"); ax.set_ylabel("Magnitude (dB)")
ax.set_ylim(-70, 5)
ax.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
ax.set_xticklabels(['$0$', r'$\pi/4$', r'$\pi/2$', r'$3\pi/4$', r'$\pi$'])
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig("images/transition_band_optimization.png", dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(9, 5))
ax.set_facecolor('#0d121f'); ax.axis('off')
ax.text(0.1, 0.75, "$x_0$", fontsize=12, color='#38bdf8', fontweight='bold')
ax.text(0.1, 0.25, "$x_1$", fontsize=12, color='#38bdf8', fontweight='bold')
ax.plot([0.25, 0.65], [0.75, 0.75], color='#38bdf8', linewidth=2.5)
ax.plot([0.25, 0.65], [0.25, 0.25], color='#38bdf8', linewidth=2.5)
ax.plot([0.25, 0.65], [0.75, 0.25], color='#ef4444', linewidth=2, linestyle='--')
ax.plot([0.25, 0.65], [0.25, 0.75], color='#10b981', linewidth=2, linestyle='--')
ax.plot(0.65, 0.25, 'o', color='#f59e0b', markersize=12)
ax.text(0.65, 0.15, r"$\times W_N^r$", fontsize=11, color='#f59e0b', fontweight='bold', ha='center')
ax.text(0.45, 0.35, "$-1$", fontsize=11, color='#ef4444', fontweight='bold')
ax.text(0.72, 0.75, r"$X_{even} = x_0 + x_1$", fontsize=12, color='#10b981', fontweight='bold')
ax.text(0.72, 0.25, r"$X_{odd} = (x_0 - x_1) \cdot W_N^r$", fontsize=12, color='#ef4444', fontweight='bold')
ax.set_title("Radix-2 DIF Butterfly: Twiddle Factor Multiplication Placed at the OUTPUT", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/dif_butterfly.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 12: IIR Filter Design — Analog Prototype & Bilinear Transform
# ==============================================================================
print("7/25. Generating Lecture 12 images...")
Omega = np.linspace(0, 3, 500)
H_butter = 1 / np.sqrt(1 + (Omega/1.0)**8)
T4 = np.where(Omega <= 1.0, 8*Omega**4 - 8*Omega**2 + 1, np.cosh(4 * np.arccosh(Omega + 1e-12)))
H_cheb1 = 1 / np.sqrt(1 + (0.5 * T4)**2)

fig, axs = plt.subplots(1, 2, figsize=(12, 5))
axs[0].plot(Omega, H_butter, color='#10b981', linewidth=2.2, label='Butterworth (Maximally Flat, No Ripple)')
axs[0].plot(Omega, H_cheb1, color='#38bdf8', linewidth=2.2, label='Chebyshev Type I (Equiripple Passband)')
axs[0].axvline(1.0, color='white', linestyle='--', alpha=0.4, label=r'Cutoff $\Omega_c = 1.0$')
axs[0].set_title(r"Analog Filter Magnitude Profiles ($N=4$)", fontsize=10, color='#38bdf8', fontweight='bold')
axs[0].set_xlabel(r"Normalized Analog Frequency $\Omega / \Omega_c$")
axs[0].set_ylabel(r"Gain $|H_a(j\Omega)|$")
axs[0].legend(loc='upper right', fontsize=8.5)

draw_s_plane = axs[1]
draw_s_plane.axhline(0, color='white', linewidth=0.8, alpha=0.3)
draw_s_plane.axvline(0, color='white', linewidth=0.8, alpha=0.3)
s_circle = Circle((0, 0), 1.0, color='#10b981', fill=False, linestyle='--', label='Butterworth S-Plane Circle (R=1)')
draw_s_plane.add_patch(s_circle)
angles = np.array([5*np.pi/8, 7*np.pi/8, 9*np.pi/8, 11*np.pi/8])
s_poles = np.exp(1j * angles)
draw_s_plane.plot(np.real(s_poles), np.imag(s_poles), 'x', color='#10b981', markersize=10, markeredgewidth=2.5, label='Butterworth Poles (LHP)')
draw_s_plane.set_xlim(-1.5, 1.5); draw_s_plane.set_ylim(-1.5, 1.5); draw_s_plane.set_aspect('equal')
draw_s_plane.set_title("S-Plane Pole Placement (Strict Left-Half Plane for Stability)", fontsize=10, color='#10b981', fontweight='bold')
draw_s_plane.set_xlabel(r"Real $(\sigma)$"); draw_s_plane.set_ylabel(r"Imag $(j\Omega)$")
draw_s_plane.legend(loc='upper right', fontsize=8.5)
plt.tight_layout()
plt.savefig("images/analog_filter_prototypes.png", dpi=300)
plt.close()

fig, axs = plt.subplots(1, 2, figsize=(11, 5.5))
axs[0].axhline(0, color='white', linewidth=0.8, alpha=0.3)
axs[0].axvline(0, color='#ef4444', linewidth=2.0, label=r'Imag Axis $j\Omega$')
axs[0].fill_between([-2, 0], [-2, -2], [2, 2], color='#10b981', alpha=0.2, label='Stable Left-Half Plane (LHP)')
axs[0].set_xlim(-2, 1.5); axs[0].set_ylim(-2, 2)
axs[0].set_title(r"Analog S-Plane ($s = \sigma + j\Omega$)", color='#38bdf8', fontweight='bold')
axs[0].set_xlabel(r"$\sigma$ (Real)"); axs[0].set_ylabel(r"$j\Omega$ (Imaginary)")
axs[0].legend(loc='lower left', fontsize=8.5)

axs[1].axhline(0, color='white', linewidth=0.8, alpha=0.3)
axs[1].axvline(0, color='white', linewidth=0.8, alpha=0.3)
uc = Circle((0, 0), 1.0, color='#ef4444', fill=False, linewidth=2.0, label=r'Unit Circle ($|z|=1$)')
axs[1].add_patch(uc)
stable_z = Circle((0, 0), 1.0, color='#10b981', alpha=0.2, label=r'Stable Interior ($|z|<1$)')
axs[1].add_patch(stable_z)
axs[1].set_xlim(-1.8, 1.8); axs[1].set_ylim(-1.8, 1.8); axs[1].set_aspect('equal')
axs[1].set_title(r"Digital Z-Plane ($z = e^{s T}$ Conformal Map)", color='#10b981', fontweight='bold')
axs[1].set_xlabel("Re(z)"); axs[1].set_ylabel("Im(z)")
axs[1].legend(loc='lower left', fontsize=8.5)
plt.suptitle(r"Bilinear Transformation Conformal Mapping: $s = \frac{2}{T} \frac{1 - z^{-1}}{1 + z^{-1}}$", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/bilinear_s_to_z_mapping.png", dpi=300)
plt.close()

omega_d = np.linspace(0, np.pi - 0.05, 500); T_samp = 1.0
Omega_a = (2 / T_samp) * np.tan(omega_d / 2)
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(omega_d, Omega_a, color='#f59e0b', linewidth=2.5, label=r'Bilinear Warping: $\Omega = \frac{2}{T} \tan(\frac{\omega}{2})$')
ax.plot(omega_d, omega_d / (T_samp/2), '--', color='#64748b', label='Ideal Linear Mapping (No Warping)')
ax.set_title("Frequency Warping Phenomenon in Bilinear Transformation", fontsize=11, color='#f59e0b', fontweight='bold')
ax.set_xlabel(r"Digital Frequency $\omega$ (rad/sample)"); ax.set_ylabel(r"Analog Frequency $\Omega$ (rad/sec)")
ax.set_xlim(0, np.pi); ax.set_ylim(0, 10)
ax.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
ax.set_xticklabels(['$0$', r'$\pi/4$', r'$\pi/2$', r'$3\pi/4$', r'$\pi$ (Compressed to $\infty$)'])
ax.legend(loc='upper left')
ax.annotate("PRE-WARPING FORMULA:\n$\\Omega_c = \\frac{2}{T} \\tan(\\omega_c / 2)$\nEnsures digital cutoff hits exact target!",
            xy=(np.pi/2, 2.0), xytext=(0.3, 5.5),
            arrowprops=dict(facecolor='#10b981', shrink=0.05, width=1.5, headwidth=6),
            fontsize=9, color='#10b981', fontweight='bold', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#10b981'))
plt.tight_layout()
plt.savefig("images/frequency_warping_prewarping.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 13: IIR Filter Structures
# ==============================================================================
print("8/25. Generating Lecture 13 images...")
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_facecolor('#0d121f'); ax.axis('off')
ax.text(0.25, 0.75, "Direct Form I (Non-Canonical)\n- Separate Delay Lines for Feedforward & Feedback\n- Total Delays required: M + N\n- Higher Memory Footprint",
        ha='center', fontsize=9.5, color='#38bdf8', bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor='#38bdf8', linewidth=1.5))
ax.text(0.75, 0.75, "Direct Form II (Canonical)\n- Merged / Shared Single Delay Line w[n]\n- Total Delays required: max(M, N)\n- Minimal Memory Hardware Footprint",
        ha='center', fontsize=9.5, color='#10b981', bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor='#10b981', linewidth=1.5))
ax.text(0.5, 0.25, "Engineering Insight: Direct Form II achieves identical mathematical transfer function H(z)\nwhile reducing hardware register count by 50% compared to Direct Form I!",
        ha='center', fontsize=10, color='white', bbox=dict(boxstyle='round,pad=0.6', facecolor='#111827', edgecolor='#f59e0b', linewidth=1.5))
ax.set_title("Direct Form I vs. Canonical Direct Form II IIR Architectures", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/iir_direct_form_i_ii_comparison.png", dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(10, 5))
ax.set_facecolor('#0d121f'); ax.axis('off')
ax.text(0.25, 0.75, "Cascade (Series) Biquad Realization\nH(z) = H_1(z) * H_2(z) * H_3(z)\n- Factored into 2nd-order sections\n- Robust against pole-zero coefficient quantization",
        ha='center', fontsize=9.5, color='#a855f7', bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor='#a855f7', linewidth=1.5))
ax.text(0.75, 0.75, "Parallel Biquad Realization\nH(z) = C + H_1(z) + H_2(z) + H_3(z)\n- Partial Fraction Expansion\n- Independent sections prevent round-off noise buildup",
        ha='center', fontsize=9.5, color='#f59e0b', bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor='#f59e0b', linewidth=1.5))
ax.text(0.5, 0.25, "Why High-Order Direct Forms are Avoided in Practice:\nFor orders N > 4, tiny rounding errors in polynomial coefficients push poles outside |z|>1,\nresulting in catastrophic filter instability!",
        ha='center', fontsize=9.5, color='#ef4444', bbox=dict(boxstyle='round,pad=0.6', facecolor='#111827', edgecolor='#ef4444', linewidth=1.5))
ax.set_title("Cascade vs. Parallel IIR Modular Architectures", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/iir_cascade_parallel_architectures.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 14: Multirate DSP
# ==============================================================================
print("9/25. Generating Lecture 14 images...")
omega_mr = np.linspace(-np.pi, np.pi, 500)
X_orig = np.maximum(0, 1 - np.abs(omega_mr)/(np.pi/3))
X_down2 = np.maximum(0, 1 - np.abs(omega_mr)/(2*np.pi/3))

fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
axs[0].plot(omega_mr, X_orig, color='#38bdf8', linewidth=2.2)
axs[0].set_title(r"1. Original Spectrum $X(e^{j\omega})$ (Bandwidth $B = \pi/3$)", fontsize=10, color='#38bdf8', fontweight='bold')
axs[0].set_ylabel("Magnitude")
axs[1].plot(omega_mr, X_down2, color='#ef4444', linewidth=2.2)
axs[1].set_title(r"2. Downsampled Spectrum ($M=2$): Frequency axis stretches by factor of 2!", fontsize=10, color='#ef4444', fontweight='bold')
axs[1].set_ylabel("Magnitude"); axs[1].set_xlabel(r"$\omega$ (rad/sample)")
axs[1].set_xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
axs[1].set_xticklabels([r'$-\pi$', r'$-\pi/2$', '$0$', r'$\pi/2$', r'$\pi$'])
plt.tight_layout()
plt.savefig("images/downsampling_decimation_spectrum.png", dpi=300)
plt.close()

fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
axs[0].plot(omega_mr, X_orig, color='#38bdf8', linewidth=2.2)
axs[0].set_title(r"1. Original Input Spectrum $X(e^{j\omega})$", fontsize=10, color='#38bdf8', fontweight='bold')
axs[0].set_ylabel("Magnitude")
X_up2 = np.maximum(0, 1 - np.abs((omega_mr + np.pi/2) % np.pi - np.pi/2)/(np.pi/6))
axs[1].plot(omega_mr, X_up2, color='#10b981', linewidth=2.2)
axs[1].set_title(r"2. Upsampled Spectrum ($L=2$): Frequency axis compresses, creating unwanted Images!", fontsize=10, color='#10b981', fontweight='bold')
axs[1].set_ylabel("Magnitude"); axs[1].set_xlabel(r"$\omega$ (rad/sample)")
axs[1].set_xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
axs[1].set_xticklabels([r'$-\pi$', r'$-\pi/2$', '$0$', r'$\pi/2$', r'$\pi$'])
plt.tight_layout()
plt.savefig("images/upsampling_interpolation_spectrum.png", dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(10, 4.5))
ax.set_facecolor('#0d121f'); ax.axis('off')
ax.text(0.5, 0.75, "Noble Identity for Decimation: Filtering AFTER Downsampler operates at M-times lower clock rate!",
        ha='center', fontsize=10, color='#38bdf8', bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor='#38bdf8', linewidth=1.5))
ax.text(0.5, 0.25, "Polyphase Commutator Model:\nDecomposes high-rate filter H(z) into M parallel branches operating at low rate\nReduces required arithmetic operations per second by a factor of M!",
        ha='center', fontsize=9.5, color='#10b981', bbox=dict(boxstyle='round,pad=0.6', facecolor='#111827', edgecolor='#10b981', linewidth=1.5))
ax.set_title("Multirate Polyphase Decomposition & Computational Savings", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/polyphase_decomposition_noble.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 15: Power Spectral Density & Wiener Filter
# ==============================================================================
print("10/25. Generating Lecture 15 images...")
tau = np.arange(-20, 21)
R_xx = 0.5 * np.cos(np.pi * tau / 4) + (tau == 0) * 0.8
fig, axs = plt.subplots(1, 2, figsize=(11, 4.8))
axs[0].stem(tau, R_xx, linefmt='#38bdf8', markerfmt='o', basefmt='white')
axs[0].set_title(r"Autocorrelation Sequence $R_{xx}[m]$", fontsize=10, color='#38bdf8', fontweight='bold')
axs[0].set_xlabel("Lag index $m$"); axs[0].set_ylabel(r"Correlation $R_{xx}[m]$")

w_psd = np.linspace(-np.pi, np.pi, 500)
S_xx = np.zeros_like(w_psd)
for i, w in enumerate(w_psd):
    S_xx[i] = np.sum(R_xx * np.exp(-1j * w * tau)).real
axs[1].plot(w_psd, S_xx, color='#10b981', linewidth=2.2)
axs[1].set_title(r"Power Spectral Density $S_{xx}(e^{j\omega}) = \mathcal{F}\{R_{xx}[m]\}$", fontsize=10, color='#10b981', fontweight='bold')
axs[1].set_xlabel(r"$\omega$ (rad/sample)"); axs[1].set_ylabel("Power Density")
axs[1].set_xticks([-np.pi, -np.pi/4, 0, np.pi/4, np.pi])
axs[1].set_xticklabels([r'$-\pi$', r'$-\pi/4$', '$0$', r'$\pi/4$', r'$\pi$'])
plt.suptitle("Wiener-Khinchin Theorem: Fourier Transform of Autocorrelation yields PSD", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/psd_wiener_khinchin_concept.png", dpi=300)
plt.close()

w_wf = np.linspace(0, np.pi, 500)
S_ss = 1.0 / (1 + (w_wf / (np.pi/4))**6)
S_vv = 0.2 * np.ones_like(w_wf)
H_wiener = S_ss / (S_ss + S_vv)
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(w_wf, S_ss, color='#38bdf8', linewidth=2, label=r'Clean Signal PSD $S_{ss}(\omega)$')
ax.plot(w_wf, S_vv, '--', color='#ef4444', linewidth=2, label=r'Noise PSD $S_{vv}(\omega)$')
ax.plot(w_wf, H_wiener, color='#10b981', linewidth=2.5, label=r'Optimal Wiener Filter Gain: $H(e^{j\omega}) = \frac{S_{ss}}{S_{ss} + S_{vv}}$')
ax.set_title("Optimal Wiener Filter: High Gain where SNR is High, Near-Zero Gain where Noise Dominates", fontsize=11, color='#10b981', fontweight='bold')
ax.set_xlabel(r"Frequency $\omega$ (rad/sample)"); ax.set_ylabel("Power / Transfer Gain")
ax.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
ax.set_xticklabels(['$0$', r'$\pi/4$', r'$\pi/2$', r'$3\pi/4$', r'$\pi$'])
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig("images/wiener_filter_noise_cancellation.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 16: Adaptive Filtering — LMS Algorithm
# ==============================================================================
print("11/25. Generating Lecture 16 images...")
w0 = np.linspace(-2, 4, 100); w1 = np.linspace(-2, 4, 100); W0, W1 = np.meshgrid(w0, w1)
J = (W0 - 1.0)**2 + 1.5*(W1 - 1.5)**2 + 0.2
fig, ax = plt.subplots(figsize=(8, 6.5))
cs = ax.contourf(W0, W1, J, levels=20, cmap='viridis', alpha=0.85)
cbar = fig.colorbar(cs, ax=ax); cbar.set_label(r'Mean Square Error $J(\mathbf{w}) = E[e^2[n]]$', color='white')
ax.plot(1.0, 1.5, 'r*', markersize=14, label=r'Wiener Optimal Weights $\mathbf{w}^* = (1.0, 1.5)$')
traj_w0 = [-1.5, -0.5, 0.3, 0.7, 0.9, 0.98, 1.0]; traj_w1 = [3.5, 2.7, 2.1, 1.7, 1.55, 1.51, 1.5]
ax.plot(traj_w0, traj_w1, 'o-', color='#10b981', linewidth=2.2, label=r'Stable LMS Trajectory (Optimal $\mu$)')
traj_w0_bad = [-1.5, 3.2, -1.0, 2.8, -0.4, 2.2]; traj_w1_bad = [3.5, 0.2, 3.1, 0.5, 2.7, 0.8]
ax.plot(traj_w0_bad, traj_w1_bad, 's--', color='#ef4444', linewidth=1.5, alpha=0.7, label=r'Overshooting Trajectory (Too Large $\mu$)')
ax.set_title("Quadratic Error Performance Surface & Gradient Descent Trajectory", fontsize=11, color='#38bdf8', fontweight='bold')
ax.set_xlabel("Filter Weight $w_0$"); ax.set_ylabel("Filter Weight $w_1$")
ax.legend(loc='lower left', fontsize=8.5)
plt.tight_layout()
plt.savefig("images/lms_error_performance_surface.png", dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(10, 4.8))
ax.set_facecolor('#0d121f'); ax.axis('off')
ax.text(0.12, 0.75, "Input Signal\n$x[n]$", ha='center', fontsize=10, color='#38bdf8', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#38bdf8'))
ax.text(0.48, 0.75, "Adaptive FIR Filter\n$y[n] = \\sum w_k x[n-k]$", ha='center', fontsize=10, color='#10b981', bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor='#10b981', linewidth=1.5))
ax.text(0.85, 0.75, "Summing Junction\n$e[n] = d[n] - y[n]$", ha='center', fontsize=10, color='#f59e0b', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#f59e0b'))
ax.text(0.85, 0.25, "Desired Signal\n$d[n]$", ha='center', fontsize=10, color='white', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='white'))
ax.text(0.48, 0.25, "LMS Weight Update Engine\n$\\mathbf{w}[n+1] = \\mathbf{w}[n] + 2\\mu e[n] \\mathbf{x}[n]$", ha='center', fontsize=10, color='#a855f7', bbox=dict(boxstyle='round,pad=0.5', facecolor='#111827', edgecolor='#a855f7', linewidth=1.5))
ax.annotate('', xy=(0.33, 0.75), xytext=(0.20, 0.75), arrowprops=dict(facecolor='#38bdf8', shrink=0.05, width=1.5, headwidth=6))
ax.annotate('', xy=(0.74, 0.75), xytext=(0.63, 0.75), arrowprops=dict(facecolor='#10b981', shrink=0.05, width=1.5, headwidth=6))
ax.annotate('', xy=(0.85, 0.63), xytext=(0.85, 0.37), arrowprops=dict(facecolor='white', shrink=0.05, width=1.5, headwidth=6))
ax.annotate('', xy=(0.64, 0.25), xytext=(0.76, 0.70), arrowprops=dict(facecolor='#f59e0b', shrink=0.05, width=1.5, headwidth=6))
ax.annotate('', xy=(0.48, 0.63), xytext=(0.48, 0.37), arrowprops=dict(facecolor='#a855f7', shrink=0.05, width=1.5, headwidth=6))
ax.set_title("Canonical Adaptive Closed-Loop FIR Filter Architecture", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/adaptive_filter_block_diagram.png", dpi=300)
plt.close()

n_iter = np.arange(0, 300); noise_floor = 0.05
learning_curve_opt = 2.5 * np.exp(-n_iter / 35.0) + noise_floor + 0.02*np.random.randn(len(n_iter))
learning_curve_slow = 2.5 * np.exp(-n_iter / 120.0) + noise_floor + 0.01*np.random.randn(len(n_iter))
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(n_iter, 10*np.log10(np.maximum(1e-4, learning_curve_opt)), color='#10b981', linewidth=2, label=r'Optimal Step Size $\mu_{opt}$: Fast convergence')
ax.plot(n_iter, 10*np.log10(np.maximum(1e-4, learning_curve_slow)), color='#38bdf8', linewidth=2, label=r'Small Step Size $\mu_{small}$: Slow adaptation')
ax.axhline(10*np.log10(noise_floor), color='#f59e0b', linestyle='--', label=r'Minimum MSE Noise Floor $J_{min}$')
ax.set_title("LMS Learning Curve: Exponential Error Convergence Over Time", fontsize=11, color='#10b981', fontweight='bold')
ax.set_xlabel("Iteration index $n$"); ax.set_ylabel("Mean Square Error (dB)")
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig("images/lms_learning_curve_weights.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 17: STFT & Spectrogram
# ==============================================================================
print("12/25. Generating Lecture 17 images...")
t_stft = np.linspace(0, 1.0, 1000)
sig_nonstat = np.sin(2 * np.pi * (20 + 80 * t_stft) * t_stft) + (t_stft > 0.6) * np.sin(2 * np.pi * 180 * t_stft)

fig, axs = plt.subplots(2, 1, figsize=(11, 6), sharex=True)
axs[0].plot(t_stft, sig_nonstat, color='#38bdf8', linewidth=1.2)
axs[0].set_title("Non-Stationary Signal: Time-Varying Frequency (Chirp + High-Frequency Burst)", fontsize=10, color='#38bdf8', fontweight='bold')
axs[0].set_ylabel("Amplitude")

w_center = 0.45; w_width = 0.15
window_shape = np.exp(-((t_stft - w_center)/(w_width/3))**2)
axs[1].plot(t_stft, sig_nonstat * window_shape, color='#10b981', linewidth=1.2, label=r'Windowed Segment $x(\tau) w(\tau - t)$')
axs[1].plot(t_stft, window_shape, '--', color='#f59e0b', linewidth=2.0, label=f'Analysis Window centered at t={w_center}s')
axs[1].set_title("Sliding Analysis Window Localizing Signal in Time", fontsize=10, color='#10b981', fontweight='bold')
axs[1].set_xlabel("Time (seconds)"); axs[1].set_ylabel("Amplitude")
axs[1].legend(loc='upper right')
plt.tight_layout()
plt.savefig("images/stft_windowing_concept.png", dpi=300)
plt.close()

# Mock spectrograms using numpy
t_grid = np.linspace(0, 1, 60); f_grid = np.linspace(0, 300, 60); T_g, F_g = np.meshgrid(t_grid, f_grid)
# True frequency curve: f(t) = 20 + 160*t, plus 180Hz for t>0.6
Sxx_true = np.exp(-((F_g - (20 + 160*T_g))/15)**2) + (T_g > 0.6) * np.exp(-((F_g - 180)/12)**2)
Sxx_narrow = np.exp(-((F_g - (20 + 160*T_g))/8)**2) + (T_g > 0.6) * np.exp(-((F_g - 180)/8)**2)
Sxx_wide = np.exp(-((F_g - (20 + 160*T_g))/35)**2) + (T_g > 0.6) * np.exp(-((F_g - 180)/30)**2)

fig, axs = plt.subplots(1, 2, figsize=(12, 5))
im1 = axs[0].pcolormesh(t_grid, f_grid, 10*np.log10(Sxx_narrow + 1e-4), shading='gouraud', cmap='magma')
axs[0].set_title("Narrowband Spectrogram (Long Window)\nFine Frequency Resolution, Poor Time Resolution", fontsize=10, color='#38bdf8', fontweight='bold')
axs[0].set_xlabel("Time (s)"); axs[0].set_ylabel("Frequency (Hz)")
fig.colorbar(im1, ax=axs[0], label='Power (dB)')

im2 = axs[1].pcolormesh(t_grid, f_grid, 10*np.log10(Sxx_wide + 1e-4), shading='gouraud', cmap='magma')
axs[1].set_title("Wideband Spectrogram (Short Window)\nFine Time Resolution, Smeared Frequencies", fontsize=10, color='#f59e0b', fontweight='bold')
axs[1].set_xlabel("Time (s)"); axs[1].set_ylabel("Frequency (Hz)")
fig.colorbar(im2, ax=axs[1], label='Power (dB)')

plt.suptitle("Heisenberg Uncertainty: Time vs. Frequency Resolution Trade-off in STFT", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/spectrogram_narrowband_vs_wideband.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 18: Wavelet Transform & Multiresolution Analysis
# ==============================================================================
print("13/25. Generating Lecture 18 images...")
fig, axs = plt.subplots(1, 2, figsize=(11, 5))
axs[0].set_title("STFT Time-Frequency Tiling\n(Fixed Window Size: Rigid Aspect Ratio)", color='#38bdf8', fontweight='bold', fontsize=10)
for t in range(5):
    for f in range(5):
        rect = Rectangle((t*0.2, f*0.2), 0.2, 0.2, fill=False, edgecolor='#38bdf8', linewidth=1.5)
        axs[0].add_patch(rect)
axs[0].set_xlim(0, 1.0); axs[0].set_ylim(0, 1.0); axs[0].set_xlabel("Time (t)"); axs[0].set_ylabel("Frequency (f)")

axs[1].set_title("Wavelet Multiresolution Tiling\n(Narrow time at high freq, fine freq at low freq)", color='#10b981', fontweight='bold', fontsize=10)
for t in range(2):
    rect = Rectangle((t*0.5, 0.0), 0.5, 0.25, fill=False, edgecolor='#10b981', linewidth=1.5)
    axs[1].add_patch(rect)
for t in range(4):
    rect = Rectangle((t*0.25, 0.25), 0.25, 0.25, fill=False, edgecolor='#10b981', linewidth=1.5)
    axs[1].add_patch(rect)
for t in range(8):
    rect = Rectangle((t*0.125, 0.50), 0.125, 0.50, fill=False, edgecolor='#10b981', linewidth=1.5)
    axs[1].add_patch(rect)
axs[1].set_xlim(0, 1.0); axs[1].set_ylim(0, 1.0); axs[1].set_xlabel("Time (t)"); axs[1].set_ylabel("Frequency / Scale (f)")
plt.tight_layout()
plt.savefig("images/stft_vs_wavelet_tiling.png", dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(10, 4.8))
ax.set_facecolor('#0d121f'); ax.axis('off')
ax.text(0.1, 0.5, "Input x[n]", fontsize=10, color='white', ha='center', bbox=dict(boxstyle='round,pad=0.3', facecolor='#1e293b', edgecolor='white'))
ax.text(0.35, 0.75, "Lowpass Filter h_0[n]\n-> [Down 2] -> A_1[n] (Approx 1)", fontsize=9, color='#10b981', ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#10b981'))
ax.text(0.35, 0.25, "Highpass Filter h_1[n]\n-> [Down 2] -> D_1[n] (Detail 1)", fontsize=9, color='#ef4444', ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#ef4444'))
ax.text(0.75, 0.85, "LPF -> [Down 2] -> A_2[n]", fontsize=9, color='#10b981', ha='center', bbox=dict(boxstyle='round,pad=0.3', facecolor='#1e293b', edgecolor='#10b981'))
ax.text(0.75, 0.60, "HPF -> [Down 2] -> D_2[n]", fontsize=9, color='#ef4444', ha='center', bbox=dict(boxstyle='round,pad=0.3', facecolor='#1e293b', edgecolor='#ef4444'))
ax.annotate('', xy=(0.24, 0.75), xytext=(0.17, 0.55), arrowprops=dict(facecolor='#10b981', shrink=0.05, width=1.5, headwidth=6))
ax.annotate('', xy=(0.24, 0.25), xytext=(0.17, 0.45), arrowprops=dict(facecolor='#ef4444', shrink=0.05, width=1.5, headwidth=6))
ax.annotate('', xy=(0.65, 0.85), xytext=(0.47, 0.75), arrowprops=dict(facecolor='#10b981', shrink=0.05, width=1.5, headwidth=6))
ax.annotate('', xy=(0.65, 0.60), xytext=(0.47, 0.75), arrowprops=dict(facecolor='#ef4444', shrink=0.05, width=1.5, headwidth=6))
ax.set_title("Mallat's Pyramidal Multiresolution Discrete Wavelet Transform (DWT) Tree", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/dwt_filterbank_mallat.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 19: FIR Structures & Lattice Filters
# ==============================================================================
print("14/25. Generating Lecture 19 images...")
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.set_facecolor('#0d121f'); ax.axis('off')
ax.text(0.5, 0.75, "Standard Transversal FIR (M Taps):\nRequires M full Multipliers and M-1 Adders",
        ha='center', fontsize=9.5, color='#ef4444', bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor='#ef4444', linewidth=1.5))
ax.text(0.5, 0.25, "Exploiting Coefficient Symmetry: h[n] = h[M-1-n]\nPre-adds symmetric samples: y[n] = sum h[k] (x[n-k] + x[n-M+1+k])\n50% Multiplier Savings in Hardware!",
        ha='center', fontsize=10, color='#10b981', bbox=dict(boxstyle='round,pad=0.6', facecolor='#111827', edgecolor='#10b981', linewidth=1.5))
ax.set_title("Linear Phase FIR Hardware Optimization (50% Multiplier Reduction)", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/fir_linear_phase_efficient_structure.png", dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(10, 4.8))
ax.set_facecolor('#0d121f'); ax.axis('off')
ax.text(0.12, 0.5, "Input x[n]\nf_0[n]=g_0[n]", ha='center', fontsize=9.5, color='#38bdf8', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#38bdf8'))
ax.text(0.5, 0.5, "Lattice Stage m Equations:\nf_m[n] = f_{m-1}[n] + k_m * g_{m-1}[n-1]\ng_m[n] = k_m * f_{m-1}[n] + g_{m-1}[n-1]", ha='center', fontsize=10, color='#f59e0b', bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor='#f59e0b', linewidth=1.5))
ax.text(0.88, 0.5, "Reflection Coeffs\n|k_m| < 1 <==>\nStrict Stability!", ha='center', fontsize=9.5, color='#10b981', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#10b981', linewidth=1.5))
ax.annotate('', xy=(0.33, 0.5), xytext=(0.22, 0.5), arrowprops=dict(facecolor='#38bdf8', shrink=0.05, width=1.5, headwidth=6))
ax.annotate('', xy=(0.77, 0.5), xytext=(0.67, 0.5), arrowprops=dict(facecolor='#f59e0b', shrink=0.05, width=1.5, headwidth=6))
ax.set_title("Lattice Stage Dynamics: Forward/Backward Residuals & Stability Criterion", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/fir_lattice_filter_architecture.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 20: Spectral Estimation — Periodogram & Parametric Methods
# ==============================================================================
print("15/25. Generating Lecture 20 images...")
N_sig = 512; t_pe = np.arange(N_sig)
sig_pe = np.sin(2 * np.pi * 0.18 * t_pe) + 0.8 * np.sin(2 * np.pi * 0.22 * t_pe) + 1.2 * np.random.randn(N_sig)
P_raw = (np.abs(np.fft.fft(sig_pe, 1024))**2) / N_sig
# Segment averaging mock
P_welch = np.convolve(P_raw[:512], np.ones(15)/15, mode='same')

fig, axs = plt.subplots(1, 2, figsize=(12, 5))
f_raw = np.linspace(0, 0.5, 512)
axs[0].plot(f_raw, 10*np.log10(P_raw[:512]), color='#ef4444', linewidth=1.2)
axs[0].set_title("Raw Periodogram (Non-Parametric)\nHigh Variance, Erratic Spurious Fluctuations", color='#ef4444', fontweight='bold', fontsize=10)
axs[0].set_xlabel("Normalized Frequency ($f / f_s$)"); axs[0].set_ylabel("Power / Frequency (dB/Hz)")

axs[1].plot(f_raw, 10*np.log10(P_welch), color='#10b981', linewidth=2.0)
axs[1].set_title("Welch Overlapped Segment Averaging\nSmooth Spectrum with Reduced Variance", color='#10b981', fontweight='bold', fontsize=10)
axs[1].set_xlabel("Normalized Frequency ($f / f_s$)"); axs[1].set_ylabel("Power / Frequency (dB/Hz)")
plt.suptitle("Spectral Estimation: Inconsistency of Raw Periodogram vs. Variance Reduction in Welch", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/periodogram_vs_bartlett_welch.png", dpi=300)
plt.close()

w_eval = np.linspace(0, np.pi, 500)
a_ar = np.poly([0.95*np.exp(1j*0.4*np.pi), 0.95*np.exp(-1j*0.4*np.pi)])
H_ar = 1.0 / np.abs(np.polyval(a_ar, np.exp(1j*w_eval)))

fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(w_eval / np.pi, 20*np.log10(H_ar), color='#38bdf8', linewidth=2.5, label='AR(2) Parametric All-Pole Model (Sharp Resonant Peak)')
ax.plot(f_raw*2, 10*np.log10(P_welch*15), '--', color='#f59e0b', linewidth=1.8, label='Welch Non-Parametric Estimate')
ax.set_title("Parametric (AR Model) vs Non-Parametric Spectral Estimation for Short Data", fontsize=11, color='#38bdf8', fontweight='bold')
ax.set_xlabel(r"Normalized Frequency ($\omega / \pi$)"); ax.set_ylabel("Magnitude Spectrum (dB)")
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig("images/ar_parametric_vs_nonparametric.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 21: Quantization Effects
# ==============================================================================
print("16/25. Generating Lecture 21 images...")
x_cont = np.linspace(-1.5, 1.5, 500)
q_levels = 8; Delta = 2.0 / q_levels
x_quant = np.floor(x_cont / Delta + 0.5) * Delta
x_quant = np.clip(x_quant, -1.0 + Delta/2, 1.0 - Delta/2)

fig, axs = plt.subplots(1, 2, figsize=(11, 4.8))
axs[0].plot(x_cont, x_cont, '--', color='#64748b', label='Ideal Analog Input')
axs[0].step(x_cont, x_quant, color='#38bdf8', linewidth=2.0, label=r'Quantized Output $Q(x)$ ($B=3$ bits)')
axs[0].set_title(r"Uniform Mid-Tread Quantizer Staircase ($\Delta = 2^{-B}$)", fontsize=10, color='#38bdf8', fontweight='bold')
axs[0].set_xlabel("Analog Input $x$"); axs[0].set_ylabel("Quantized Level $Q(x)$")
axs[0].legend(loc='upper left', fontsize=8.5)

e_axis = np.linspace(-Delta, Delta, 200)
pdf_e = np.where(np.abs(e_axis) <= Delta/2, 1.0 / Delta, 0.0)
axs[1].plot(e_axis, pdf_e, color='#10b981', linewidth=2.2)
axs[1].fill_between(e_axis, 0, pdf_e, color='#10b981', alpha=0.25)
axs[1].set_title(r"Uniform Error PDF: $p(e) = \frac{1}{\Delta}, \quad \sigma_e^2 = \frac{\Delta^2}{12}$", fontsize=10, color='#10b981', fontweight='bold')
axs[1].set_xlabel("Quantization Error $e = Q(x) - x$"); axs[1].set_ylabel("Probability Density $p(e)$")
axs[1].set_xticks([-Delta/2, 0, Delta/2]); axs[1].set_xticklabels([r'$-\Delta/2$', '$0$', r'$+\Delta/2$'])
plt.suptitle("Statistical Model of Quantization Error in Fixed-Point Systems", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/uniform_quantization_error_pdf.png", dpi=300)
plt.close()

bits = np.arange(4, 25); sqnr = 6.02 * bits + 1.76
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(bits, sqnr, 'o-', color='#f59e0b', linewidth=2.5, label=r'$\mathrm{SQNR} = 6.02 B + 1.76\text{ dB}$')
ax.plot([16, 16], [0, 6.02*16+1.76], 'g--', label='16-bit Audio Standard (SQNR = 98.08 dB)')
ax.plot([24, 24], [0, 6.02*24+1.76], 'c--', label='24-bit Studio Master (SQNR = 146.24 dB)')
ax.set_title("The 6.02 dB/bit Rule: Linear Increase of SQNR with Wordlength", fontsize=11, color='#f59e0b', fontweight='bold')
ax.set_xlabel("ADC Wordlength / Number of Bits ($B$)"); ax.set_ylabel("Signal-to-Quantization-Noise Ratio (dB)")
ax.set_ylim(20, 160); ax.legend(loc='lower right', fontsize=8.5)
ax.annotate('Each additional bit adds ~6.02 dB of dynamic range,\ncutting the noise power by a factor of 4!',
            xy=(8, 50), xytext=(5, 100),
            arrowprops=dict(facecolor='#10b981', shrink=0.05, width=1.5, headwidth=6),
            fontsize=9, color='#10b981', fontweight='bold', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#10b981'))
plt.tight_layout()
plt.savefig("images/sqnr_vs_bitdepth_rule.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 22: Sampling Theorem, Aliasing & ADC/DAC
# ==============================================================================
print("17/25. Generating Lecture 22 images...")
Omega = np.linspace(-30, 30, 1000)
def baseband(w, w_max=6): return np.maximum(0, 1 - np.abs(w)/w_max)
Xs_nyq = (baseband(Omega) + baseband(Omega - 16) + baseband(Omega + 16))
Xs_alias = (baseband(Omega) + baseband(Omega - 8) + baseband(Omega + 8))

fig, axs = plt.subplots(2, 1, figsize=(11, 6), sharex=True)
axs[0].plot(Omega, Xs_nyq, color='#10b981', linewidth=2.2)
axs[0].set_title(r"1. Nyquist Sampling ($\Omega_s \geq 2\Omega_{max}$): Spectral Replicas are Disjoint $\rightarrow$ Perfect Reconstruction!", fontsize=10, color='#10b981', fontweight='bold')
axs[0].set_ylabel(r"Magnitude $|X_s(j\Omega)|$")
axs[1].plot(Omega, Xs_alias, color='#ef4444', linewidth=2.2)
axs[1].set_title(r"2. Undersampling ($\Omega_s < 2\Omega_{max}$): Spectral Aliasing Overlap $\rightarrow$ Irreversible Distortion!", fontsize=10, color='#ef4444', fontweight='bold')
axs[1].set_ylabel(r"Magnitude $|X_s(j\Omega)|$"); axs[1].set_xlabel(r"Analog Frequency $\Omega$ (rad/s)")
plt.tight_layout()
plt.savefig("images/sampling_frequency_replication.png", dpi=300)
plt.close()

t_cont = np.linspace(0, 1.0, 1000)
f_high = 9.0; f_low = 1.0; fs = 10.0
x_high = np.cos(2 * np.pi * f_high * t_cont)
x_low = np.cos(2 * np.pi * f_low * t_cont)
n_samp = np.arange(0, 1.05, 1.0/fs)
x_sampled = np.cos(2 * np.pi * f_high * n_samp)

fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(t_cont, x_high, '--', color='#ef4444', alpha=0.7, label=r'High-Frequency True Signal ($9\text{ Hz}$)')
ax.plot(t_cont, x_low, color='#10b981', linewidth=2.2, label=r'Apparent Low-Frequency Alias ($1\text{ Hz} = |9 - 10|\text{ Hz}$)')
ax.plot(n_samp, x_sampled, 'o', color='#f59e0b', markersize=8, label=r'Sampled Points ($f_s = 10\text{ Hz}$)')
ax.set_title("Time-Domain Aliasing: High Frequency Masquerades Identically as Low Frequency", fontsize=11, color='#f59e0b', fontweight='bold')
ax.set_xlabel("Time (seconds)"); ax.set_ylabel("Amplitude")
ax.legend(loc='upper right', fontsize=8.5)
plt.tight_layout()
plt.savefig("images/aliasing_time_domain_masquerade.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 23: Digital Oscillators & NCO
# ==============================================================================
print("18/25. Generating Lecture 23 images...")
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.set_facecolor('#0d121f'); ax.axis('off')
ax.text(0.15, 0.75, "Frequency Control Word\nFCW = M = (f_out / f_clk) * 2^N", ha='center', fontsize=9.5, color='#38bdf8', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#38bdf8'))
ax.text(0.45, 0.75, "N-bit Phase Accumulator\ntheta[n] = (theta[n-1] + M) mod 2^N", ha='center', fontsize=9.5, color='#f59e0b', bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor='#f59e0b', linewidth=1.5))
ax.text(0.80, 0.75, "Phase-to-Amplitude LUT\ns[n] = sin(2 pi theta[n] / 2^N)", ha='center', fontsize=9.5, color='#10b981', bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor='#10b981', linewidth=1.5))
ax.text(0.5, 0.25, "Key Advantages of NCO / DDS over Recursive IIR Oscillators:\n- Instantaneous, Phase-Continuous Frequency Switching\n- Exact Zero Amplitude Drift over infinite runtime (LUT bounded)\n- Sub-Hertz frequency tuning resolution: Delta f = f_clk / 2^N",
        ha='center', fontsize=9.5, color='white', bbox=dict(boxstyle='round,pad=0.6', facecolor='#111827', edgecolor='#10b981', linewidth=1.5))
ax.annotate('', xy=(0.33, 0.75), xytext=(0.25, 0.75), arrowprops=dict(facecolor='#38bdf8', shrink=0.05, width=1.5, headwidth=6))
ax.annotate('', xy=(0.68, 0.75), xytext=(0.58, 0.75), arrowprops=dict(facecolor='#f59e0b', shrink=0.05, width=1.5, headwidth=6))
ax.set_title("Direct Digital Synthesis (DDS) / Numerically Controlled Oscillator Architecture", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/dds_nco_architecture_operation.png", dpi=300)
plt.close()

n_osc = np.arange(0, 300); w_osc = 0.1 * np.pi
osc_ideal = np.cos(w_osc * n_osc); osc_decay = (0.995**n_osc) * np.cos(w_osc * n_osc)

fig, axs = plt.subplots(1, 2, figsize=(11, 4.8))
axs[0].plot(n_osc, osc_ideal, color='#10b981', label='Ideal Float (Poles |z|=1.0)')
axs[0].plot(n_osc, osc_decay, '--', color='#ef4444', label='Quantized Inward Drift (|z|=0.995)')
axs[0].set_title("Recursive Oscillator Amplitude Drift in Fixed-Point Arithmetic", fontsize=10, color='#38bdf8', fontweight='bold')
axs[0].set_xlabel("Sample index $n$"); axs[0].set_ylabel("Amplitude")
axs[0].legend(loc='lower left', fontsize=8.5)

draw_zplane(axs[1], xlim=1.5, ylim=1.5, title="Unit Circle Pole Sensitivity")
axs[1].plot(np.cos(w_osc), np.sin(w_osc), 'x', color='#10b981', markersize=10, markeredgewidth=2.5, label='Ideal Pole on |z|=1')
axs[1].plot(0.995*np.cos(w_osc), 0.995*np.sin(w_osc), 'x', color='#ef4444', markersize=10, markeredgewidth=2.5, label='Drifted Pole inside |z|<1')
axs[1].legend(loc='lower left', fontsize=8)
plt.tight_layout()
plt.savefig("images/recursive_oscillator_zplane_drift.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 24: Linear Prediction & Speech Processing
# ==============================================================================
print("19/25. Generating Lecture 24 images...")
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.set_facecolor('#0d121f'); ax.axis('off')
ax.text(0.15, 0.75, "Voiced Source\n(Glottal Pulse Train p(t))", ha='center', fontsize=9, color='#38bdf8', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#38bdf8'))
ax.text(0.15, 0.25, "Unvoiced Source\n(Turbulent White Noise)", ha='center', fontsize=9, color='#f59e0b', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#f59e0b'))
ax.text(0.52, 0.5, "Vocal Tract All-Pole Filter\nH(z) = G / (1 - sum a_k z^-k)\nFormants F_1, F_2, F_3", ha='center', fontsize=10, color='#10b981', bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor='#10b981', linewidth=1.5))
ax.text(0.88, 0.5, "Synthesized\nSpeech Signal\ns[n]", ha='center', fontsize=9.5, color='white', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='white'))
ax.annotate('', xy=(0.38, 0.55), xytext=(0.28, 0.75), arrowprops=dict(facecolor='#38bdf8', shrink=0.05, width=1.5, headwidth=6))
ax.annotate('', xy=(0.38, 0.45), xytext=(0.28, 0.25), arrowprops=dict(facecolor='#f59e0b', shrink=0.05, width=1.5, headwidth=6))
ax.annotate('', xy=(0.80, 0.5), xytext=(0.67, 0.5), arrowprops=dict(facecolor='#10b981', shrink=0.05, width=1.5, headwidth=6))
ax.set_title("Source-Filter Acoustic Speech Production & LPC Synthesis Framework", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/speech_production_source_filter.png", dpi=300)
plt.close()

w_speech = np.linspace(0, np.pi, 500); pitch_spikes = np.zeros_like(w_speech); pitch_spikes[::15] = 1.0
H_vocal = 1.0 / (np.abs(1 - 0.9*np.exp(-1j*(w_speech-0.3))) * np.abs(1 - 0.88*np.exp(-1j*(w_speech-0.8))) * np.abs(1 - 0.85*np.exp(-1j*(w_speech-1.5))))
speech_spec = 20*np.log10(H_vocal) + 15 * pitch_spikes

fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(w_speech / np.pi, speech_spec, color='#64748b', alpha=0.7, label='Raw Speech DFT Spectrum (Harmonic Pitch Lines)')
ax.plot(w_speech / np.pi, 20*np.log10(H_vocal), color='#ef4444', linewidth=2.5, label=r'LPC All-Pole Spectral Envelope (Formant Resonances $F_1, F_2, F_3$)')
ax.set_title("LPC Spectral Envelope Tracking Vocal Tract Formant Peaks", fontsize=11, color='#ef4444', fontweight='bold')
ax.set_xlabel(r"Normalized Frequency ($\omega / \pi$)"); ax.set_ylabel("Magnitude Spectrum (dB)")
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig("images/lpc_spectral_envelope_tracking.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 25: DSP in Communications
# ==============================================================================
print("20/25. Generating Lecture 25 images...")
t_rc = np.linspace(-4, 4, 500)
def raised_cosine(t, alpha):
    denom = 1 - (2*alpha*t)**2
    denom = np.where(np.abs(denom) < 1e-5, 1e-5, denom)
    return np.sinc(t) * np.cos(np.pi * alpha * t) / denom

fig, axs = plt.subplots(1, 2, figsize=(12, 4.8))
axs[0].plot(t_rc, raised_cosine(t_rc, 0.0), label=r'$\alpha=0.0$ (Ideal Sinc, Infinite Taps)', color='#ef4444')
axs[0].plot(t_rc, raised_cosine(t_rc, 0.5), label=r'$\alpha=0.5$ (Standard RC Pulse)', color='#38bdf8', linewidth=2.0)
axs[0].plot(t_rc, raised_cosine(t_rc, 1.0), label=r'$\alpha=1.0$ (Full Roll-off)', color='#10b981')
axs[0].set_title(r"Nyquist Raised-Cosine Pulses: Zero-Crossings at $t = \pm 1, \pm 2, \pm 3$", fontsize=10, color='#38bdf8', fontweight='bold')
axs[0].set_xlabel("Time normalized to Symbol Period ($t / T$)"); axs[0].set_ylabel("Amplitude")
axs[0].axvline(1.0, color='white', linestyle='--', alpha=0.3); axs[0].axvline(-1.0, color='white', linestyle='--', alpha=0.3)
axs[0].legend(loc='upper right', fontsize=8.5)

t_mf = np.linspace(0, 2, 400); pulse = (t_mf >= 0.2) & (t_mf <= 0.8)
mf_out = np.convolve(pulse + 0.6*np.random.randn(len(t_mf)), pulse[::-1], mode='same') / np.sum(pulse)
axs[1].plot(t_mf, pulse + 0.6*np.random.randn(len(t_mf)), color='#64748b', alpha=0.6, label=r'Noisy Received Signal $r[n] = s[n] + w[n]$')
axs[1].plot(t_mf, mf_out, color='#f59e0b', linewidth=2.2, label=r'Matched Filter Output $y[n]$ (Peak at $t=T$)')
axs[1].set_title("Matched Filter: Maximum Instantaneous SNR at Sampling Instant", fontsize=10, color='#f59e0b', fontweight='bold')
axs[1].set_xlabel("Time (s)"); axs[1].set_ylabel("Amplitude")
axs[1].legend(loc='upper right', fontsize=8.5)
plt.tight_layout()
plt.savefig("images/raised_cosine_pulse_and_isi.png", dpi=300)
plt.close()

np.random.seed(42)
qpsk_symbols = np.array([1+1j, 1-1j, -1+1j, -1-1j]) / np.sqrt(2)
tx_data = np.random.choice(qpsk_symbols, 800)
rx_data = tx_data + 0.18*(np.random.randn(800) + 1j*np.random.randn(800))
fig, ax = plt.subplots(figsize=(6.5, 6.5))
ax.axhline(0, color='white', linewidth=0.8, alpha=0.3); ax.axvline(0, color='white', linewidth=0.8, alpha=0.3)
ax.scatter(np.real(rx_data), np.imag(rx_data), color='#38bdf8', alpha=0.5, s=15, label='Received Noisy Symbols')
ax.scatter(np.real(qpsk_symbols), np.imag(qpsk_symbols), color='#ef4444', s=80, marker='x', linewidths=3, label='Ideal Constellation Points')
ax.set_title("QPSK Complex Constellation Scatter & Decision Boundaries", fontsize=11, color='#38bdf8', fontweight='bold')
ax.set_xlabel("In-Phase Component (I)"); ax.set_ylabel("Quadrature Component (Q)")
ax.set_xlim(-1.8, 1.8); ax.set_ylim(-1.8, 1.8); ax.set_aspect('equal')
ax.legend(loc='upper right', fontsize=8.5)
plt.tight_layout()
plt.savefig("images/qpsk_constellation_and_eye_diagram.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 26: DSP for Power Systems
# ==============================================================================
print("21/25. Generating Lecture 26 images...")
t_grid = np.linspace(0, 0.04, 500)
v_fund = np.sin(2 * np.pi * 50 * t_grid)
v_3rd = 0.15 * np.sin(2 * np.pi * 150 * t_grid)
v_5th = 0.08 * np.sin(2 * np.pi * 250 * t_grid)
v_distorted = v_fund + v_3rd + v_5th

fig, axs = plt.subplots(1, 2, figsize=(12, 4.8))
axs[0].plot(t_grid * 1000, v_distorted, color='#ef4444', linewidth=2.2, label=r'Distorted Grid Voltage $v(t)$')
axs[0].plot(t_grid * 1000, v_fund, '--', color='#10b981', label='Pure 50 Hz Fundamental')
axs[0].set_title("Power Grid Waveform with Harmonic Distortion", fontsize=10, color='#ef4444', fontweight='bold')
axs[0].set_xlabel("Time (ms)"); axs[0].set_ylabel("Voltage (p.u.)")
axs[0].legend(loc='upper right', fontsize=8.5)

harmonics = [50, 150, 250, 350]; amplitudes = [100.0, 15.0, 8.0, 2.0]
axs[1].stem(harmonics, amplitudes, linefmt='#38bdf8', markerfmt='o', basefmt='white')
axs[1].set_title(r"Harmonic Spectrum: $\mathrm{THD} = \frac{\sqrt{V_3^2 + V_5^2 + V_7^2}}{V_1} = 17.1\%$", fontsize=10, color='#38bdf8', fontweight='bold')
axs[1].set_xlabel("Frequency (Hz)"); axs[1].set_ylabel("Amplitude (% of Fundamental)")
axs[1].set_xticks([50, 100, 150, 200, 250, 300, 350])
plt.tight_layout()
plt.savefig("images/power_harmonics_waveform_thd.png", dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(10, 4.5))
ax.set_facecolor('#0d121f'); ax.axis('off')
ax.text(0.5, 0.75, "Recursive Sliding DFT Update Formula:\nX_n[k] = (X_{n-1}[k] + x[n] - x[n-N]) * W_N^-k\nComputes full new spectrum in only O(1) complex operations per sample!",
        ha='center', fontsize=10, color='#10b981', bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor='#10b981', linewidth=1.5))
ax.text(0.5, 0.25, "Phasor Measurement Unit (PMU) Operation in Smart Grids:\nProvides sub-cycle voltage magnitude |V| and phase angle phi updates synchronized to GPS clock\nCritical for instantaneous fault detection and wide-area power system stability monitoring!",
        ha='center', fontsize=9.5, color='#38bdf8', bbox=dict(boxstyle='round,pad=0.6', facecolor='#111827', edgecolor='#38bdf8', linewidth=1.5))
ax.set_title("Sliding Recursive DFT Architecture for Real-Time Grid Phasor Estimation", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/sliding_dft_phasor_tracking.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 27: DSP for Image Processing
# ==============================================================================
print("22/25. Generating Lecture 27 images...")
x_grid = np.linspace(0, 1, 128); y_grid = np.linspace(0, 1, 128); X_g, Y_g = np.meshgrid(x_grid, y_grid)
pattern_2d = np.sin(2 * np.pi * 4 * X_g) + np.sin(2 * np.pi * 8 * Y_g)
dft_2d = np.fft.fftshift(np.fft.fft2(pattern_2d))

fig, axs = plt.subplots(1, 2, figsize=(11, 5))
axs[0].imshow(pattern_2d, cmap='gray')
axs[0].set_title(r"2D Spatial Signal $f[m,n]$ (Horizontal + Vertical Waves)", fontsize=10, color='#38bdf8', fontweight='bold')
axs[0].axis('off')
axs[1].imshow(np.log(np.abs(dft_2d) + 1), cmap='magma')
axs[1].set_title(r"Centered 2D DFT Spectrum $|F(u,v)|$ (DC at Center $(0,0)$)", fontsize=10, color='#f59e0b', fontweight='bold')
axs[1].axis('off')
plt.suptitle("2D Discrete Fourier Transform: Spatial Patterns to Frequency Domain Bins", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/image_2d_dft_spatial_frequencies.png", dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(7, 6))
dct_matrix = np.array([
    [120, 45, 18, 8, 3, 1, 0, 0],
    [52, 28, 12, 5, 2, 0, 0, 0],
    [22, 14, 7, 3, 1, 0, 0, 0],
    [9, 6, 3, 1, 0, 0, 0, 0],
    [4, 2, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
])
im_dct = ax.imshow(dct_matrix, cmap='coolwarm')
fig.colorbar(im_dct, ax=ax, label='DCT Coefficient Energy')
ax.set_title("2D Discrete Cosine Transform (DCT) Energy Compaction (8x8 Block)", fontsize=10.5, color='#10b981', fontweight='bold')
ax.set_xlabel("Horizontal Frequency $u$"); ax.set_ylabel("Vertical Frequency $v$")
ax.annotate('DC & Low Frequencies\n(Contains > 95% Image Energy)', xy=(0.5, 0.5), xytext=(2.5, 2.5),
            arrowprops=dict(facecolor='#10b981', shrink=0.05, width=1.5, headwidth=6),
            fontsize=8.5, color='#10b981', fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#1e293b', edgecolor='#10b981'))
ax.annotate('High Frequencies\n(Quantized to Zero for Compression)', xy=(6.5, 6.5), xytext=(3.5, 5.5),
            arrowprops=dict(facecolor='#ef4444', shrink=0.05, width=1.5, headwidth=6),
            fontsize=8.5, color='#ef4444', fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#1e293b', edgecolor='#ef4444'))
plt.tight_layout()
plt.savefig("images/jpeg_2d_dct_energy_compaction.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 28: DSP for Biomedical Signals — ECG, EEG & EMG Processing
# ==============================================================================
print("23/25. Generating Lecture 28 images...")
t_ecg = np.linspace(0, 1.5, 600)
p_wave = 0.25 * np.exp(-((t_ecg - 0.2) / 0.03)**2); q_wave = -0.15 * np.exp(-((t_ecg - 0.28) / 0.015)**2)
r_wave = 1.2 * np.exp(-((t_ecg - 0.3) / 0.02)**2); s_wave = -0.35 * np.exp(-((t_ecg - 0.33) / 0.02)**2)
t_wave = 0.35 * np.exp(-((t_ecg - 0.5) / 0.06)**2)
ecg_clean = p_wave + q_wave + r_wave + s_wave + t_wave
ecg_noisy = ecg_clean + 0.15 * np.sin(2 * np.pi * 50 * t_ecg) + 0.3 * np.sin(2 * np.pi * 0.8 * t_ecg)

fig, axs = plt.subplots(2, 1, figsize=(11, 6), sharex=True)
axs[0].plot(t_ecg, ecg_noisy, color='#ef4444', linewidth=1.2)
axs[0].set_title(r"1. Raw Noisy ECG: Corrupted by $50\text{ Hz}$ Powerline Hum + Baseline Wander", fontsize=10, color='#ef4444', fontweight='bold')
axs[0].set_ylabel("Amplitude (mV)")
axs[1].plot(t_ecg, ecg_clean, color='#10b981', linewidth=2.0)
axs[1].set_title("2. Clean Processed ECG: P-QRS-T Morphology Preserved", fontsize=10, color='#10b981', fontweight='bold')
axs[1].set_ylabel("Amplitude (mV)"); axs[1].set_xlabel("Time (seconds)")
axs[1].annotate('P Wave', xy=(0.2, 0.25), xytext=(0.1, 0.6), arrowprops=dict(facecolor='#38bdf8', shrink=0.05, width=1, headwidth=4), fontsize=8.5, color='#38bdf8')
axs[1].annotate('R Peak', xy=(0.3, 1.2), xytext=(0.35, 1.3), arrowprops=dict(facecolor='#10b981', shrink=0.05, width=1, headwidth=4), fontsize=8.5, color='#10b981', fontweight='bold')
axs[1].annotate('T Wave', xy=(0.5, 0.35), xytext=(0.6, 0.7), arrowprops=dict(facecolor='#f59e0b', shrink=0.05, width=1, headwidth=4), fontsize=8.5, color='#f59e0b')
plt.tight_layout()
plt.savefig("images/ecg_morphology_and_noise_artifacts.png", dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(10, 4.5))
ax.set_facecolor('#0d121f'); ax.axis('off')
steps_pt = [
    "1. Bandpass Filter\n(5 - 15 Hz)\nRemoves 50Hz hum\n& baseline wander",
    "2. Derivative\ny[n] = 2x[n] + x[n-1]\n- x[n-3] - 2x[n-4]\nHighlights QRS slope",
    "3. Squaring\ny[n] = x^2[n]\nMakes all values positive\n& amplifies peaks",
    "4. Moving Window\nIntegration (150ms)\nSmooths QRS waveform\nfor peak detection"
]
colors_pt = ['#38bdf8', '#f59e0b', '#ef4444', '#10b981']
for idx, (st, col) in enumerate(zip(steps_pt, colors_pt)):
    x_pos = 0.05 + idx * 0.24
    ax.text(x_pos + 0.1, 0.5, st, ha='center', va='center', fontsize=9, color=col, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor=col, linewidth=1.5))
    if idx < 3:
        ax.annotate('', xy=(x_pos + 0.23, 0.5), xytext=(x_pos + 0.20, 0.5),
                    arrowprops=dict(facecolor='white', shrink=0.05, width=1.5, headwidth=6))
ax.set_title("Pan-Tompkins Real-Time QRS / R-Peak Detection Signal Processing Pipeline", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/pan_tompkins_qrs_detection_pipeline.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 29: DSP for Radar — Pulse Compression, Doppler & CFAR
# ==============================================================================
print("24/25. Generating Lecture 29 images...")
t_chirp = np.linspace(-1, 1, 1000); f0 = 2.0; k_rate = 15.0
chirp_sig = np.cos(2 * np.pi * (f0 * t_chirp + 0.5 * k_rate * t_chirp**2))
mf_radar = np.sinc(k_rate * t_chirp * 2)

fig, axs = plt.subplots(1, 2, figsize=(12, 4.8))
axs[0].plot(t_chirp, chirp_sig, color='#38bdf8', linewidth=1.2)
axs[0].set_title(r"Transmitted LFM Chirp Pulse (Wide Duration $T$, High Energy)", fontsize=10, color='#38bdf8', fontweight='bold')
axs[0].set_xlabel(r"Time ($\mu$s)"); axs[0].set_ylabel("Amplitude")
axs[1].plot(t_chirp, np.abs(mf_radar), color='#10b981', linewidth=2.2)
axs[1].set_title(r"Compressed Output Pulse: Narrow Resolution ($\Delta \tau \approx 1/B$)", fontsize=10, color='#10b981', fontweight='bold')
axs[1].set_xlabel(r"Time Delay ($\mu$s)"); axs[1].set_ylabel("Compressed Amplitude")
plt.suptitle("Radar Pulse Compression: Overcomes Peak Power Limit while achieving High Range Resolution", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/radar_pulse_compression_chirp.png", dpi=300)
plt.close()

fig, ax = plt.subplots(figsize=(10, 4.8))
ax.set_facecolor('#0d121f'); ax.axis('off')
ax.text(0.18, 0.75, "Leading Reference Cells\n(Estimate Background Noise Clutter)", ha='center', fontsize=9, color='#38bdf8', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#38bdf8'))
ax.text(0.50, 0.75, "Guard Cells + CUT\n(Cell Under Test)", ha='center', fontsize=9, color='#ef4444', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#ef4444', linewidth=1.5))
ax.text(0.82, 0.75, "Lagging Reference Cells\n(Estimate Background Noise Clutter)", ha='center', fontsize=9, color='#38bdf8', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#38bdf8'))
ax.text(0.5, 0.25, "Cell-Averaging Constant False Alarm Rate (CA-CFAR) Principle:\nAdaptive Threshold T_thresh = alpha * (1/N) sum P_ref[i]\nDynamically scales with clutter intensity to maintain constant false alarm probability P_FA!",
        ha='center', fontsize=9.5, color='#10b981', bbox=dict(boxstyle='round,pad=0.6', facecolor='#111827', edgecolor='#10b981', linewidth=1.5))
ax.set_title("CA-CFAR Dynamic Adaptive Target Detection Architecture", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/ca_cfar_detection_threshold.png", dpi=300)
plt.close()

# ==============================================================================
# LECTURE 30: DSP Capstone — System Design & Applications
# ==============================================================================
print("25/25. Generating Lecture 30 images...")
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_facecolor('#0d121f'); ax.axis('off')
ax.text(0.15, 0.75, "Primary Mic\nSignal + Noise\n$d[n] = s[n] + n_0[n]$", ha='center', fontsize=9.5, color='#38bdf8', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#38bdf8'))
ax.text(0.15, 0.25, "Reference Mic\nNoise Source\n$x[n] = n_1[n]$", ha='center', fontsize=9.5, color='#f59e0b', bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#f59e0b'))
ax.text(0.52, 0.25, "Adaptive LMS Filter\nModels Acoustic Transfer Path H(z)\nn_hat[n] = w^T[n] x[n]", ha='center', fontsize=9.5, color='#10b981', bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor='#10b981', linewidth=1.5))
ax.text(0.85, 0.75, "Error Output (Clean Audio)\n$e[n] = d[n] - \\hat{n}_0[n] \\approx s[n]$", ha='center', fontsize=9.5, color='#10b981', fontweight='bold', bbox=dict(boxstyle='round,pad=0.5', facecolor='#111827', edgecolor='#10b981', linewidth=1.5))
ax.annotate('', xy=(0.70, 0.75), xytext=(0.30, 0.75), arrowprops=dict(facecolor='#38bdf8', shrink=0.05, width=1.5, headwidth=6))
ax.annotate('', xy=(0.37, 0.25), xytext=(0.28, 0.25), arrowprops=dict(facecolor='#f59e0b', shrink=0.05, width=1.5, headwidth=6))
ax.annotate('', xy=(0.85, 0.63), xytext=(0.67, 0.25), arrowprops=dict(facecolor='#10b981', shrink=0.05, width=1.5, headwidth=6))
ax.set_title("Adaptive Noise Cancellation (ANC) Dual-Microphone DSP System", fontsize=11, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig("images/adaptive_noise_cancellation_system.png", dpi=300)
plt.close()

omega_eq = np.linspace(0, np.pi, 500)
H_channel = np.abs(1 - 0.7 * np.exp(-1j * omega_eq) + 0.4 * np.exp(-2j * omega_eq))
H_equalizer = 1.0 / (H_channel + 1e-4)
H_combined = H_channel * H_equalizer

fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(omega_eq / np.pi, 20*np.log10(H_channel), color='#ef4444', linewidth=2.0, label=r'Distorted Dispersive Channel $H_{ch}(e^{j\omega})$')
ax.plot(omega_eq / np.pi, 20*np.log10(H_equalizer), '--', color='#38bdf8', linewidth=2.0, label=r'Zero-Forcing Equalizer $H_{eq}(e^{j\omega}) = 1/H_{ch}$')
ax.plot(omega_eq / np.pi, 20*np.log10(H_combined), color='#10b981', linewidth=2.5, label='Equalized Total Response: Flat 0 dB (ISI Eliminated!)')
ax.set_title("Channel Equalization: Inverting Multipath Distortion to Restore Flat Frequency Response", fontsize=11, color='#10b981', fontweight='bold')
ax.set_xlabel(r"Normalized Frequency ($\omega / \pi$)"); ax.set_ylabel("Gain (dB)")
ax.legend(loc='lower right')
plt.tight_layout()
plt.savefig("images/channel_equalizer_frequency_response.png", dpi=300)
plt.close()

print("ALL 25 LECTURES (L6 TO L30) GENERATED SUCCESSFULLY!")
