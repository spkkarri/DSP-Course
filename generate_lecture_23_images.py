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
# Plot 1: Window Time-domain Shapes
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 3.2))

M = 31
n = np.arange(M)
w_hamming = 0.54 - 0.46 * np.cos(2 * np.pi * n / (M - 1))
w_blackman = 0.42 - 0.5 * np.cos(2 * np.pi * n / (M - 1)) + 0.08 * np.cos(4 * np.pi * n / (M - 1))

ax.stem(n, w_hamming, linefmt='#a78bfa', markerfmt='o', label="Hamming Window", basefmt=" ")
ax.stem(n, w_blackman, linefmt='#fb7185', markerfmt='s', label="Blackman Window", basefmt=" ")

ax.set_xlabel("Sample index n", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_ylabel("Amplitude w[n]", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_title("Time-Domain Window Shapes (Length M=31)", fontsize=12, pad=12)
ax.legend(loc='lower center', frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=9)
ax.set_ylim(-0.1, 1.2)
ax.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)

plt.tight_layout()
plt.savefig("images/window_comparison_shapes.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Plot 2: Spectral Sidelobe comparison
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 3.8))

w = np.linspace(0, np.pi, 1000)

# Ideal LPF coefficients with wc = pi/4
wc = np.pi / 4
M_large = 51
alpha = (M_large - 1) / 2
n_ideal = np.arange(M_large)
hd = np.zeros_like(n_ideal, dtype=float)
for idx, ni in enumerate(n_ideal):
    diff = ni - alpha
    if diff == 0:
        hd[idx] = wc / np.pi
    else:
        hd[idx] = np.sin(wc * diff) / (np.pi * diff)

# Apply 4 windows
w_rect = np.ones(M_large)
w_hann = 0.5 - 0.5 * np.cos(2 * np.pi * n_ideal / (M_large - 1))
w_hamming = 0.54 - 0.46 * np.cos(2 * np.pi * n_ideal / (M_large - 1))
w_blackman = 0.42 - 0.5 * np.cos(2 * np.pi * n_ideal / (M_large - 1)) + 0.08 * np.cos(4 * np.pi * n_ideal / (M_large - 1))

h_rect = hd * w_rect
h_hann = hd * w_hann
h_ham = hd * w_hamming
h_blk = hd * w_blackman

# Frequency responses (dB)
def get_db_response(h):
    H = np.zeros_like(w, dtype=complex)
    for idx, wi in enumerate(w):
        H[idx] = np.sum(h * np.exp(-1j * wi * np.arange(len(h))))
    mag = np.abs(H)
    # Normalize by passband gain
    mag = mag / mag[0]
    return 20 * np.log10(np.max([np.ones_like(mag)*1e-5, mag], axis=0))

resp_rect = get_db_response(h_rect)
resp_hann = get_db_response(h_hann)
resp_ham = get_db_response(h_ham)
resp_blk = get_db_response(h_blk)

# Plot spectra
ax.plot(w, resp_rect, color='#ef4444', linewidth=1.2, label="Rectangular (-21 dB Stopband)")
ax.plot(w, resp_hann, color='#10b981', linewidth=1.2, label="Hann (-44 dB Stopband)")
ax.plot(w, resp_ham, color='#a78bfa', linewidth=1.5, label="Hamming (-53 dB Stopband)")
ax.plot(w, resp_blk, color='#fb7185', linewidth=1.8, label="Blackman (-74 dB Stopband)")

ax.set_xlabel("Frequency \u03c0 (radians)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_ylabel("Normalized Gain (dB)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_title("Window Spectra Stopband Attenuation Comparison (Length M=51)", fontsize=12, pad=12)
ax.set_xlim(0, np.pi)
ax.set_ylim(-90, 5)
ax.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
ax.legend(loc='upper right', frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=8.5)

plt.tight_layout()
plt.savefig("images/sidelobe_suppression.png", dpi=300)
plt.close()

print("Lecture 23 images generated successfully.")
