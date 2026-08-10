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
# Plot 1: Discrete Frequency Sampling Grid
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 3.2))

w_c = np.pi / 3
M = 15
k = np.arange(M // 2 + 1)
w_k = 2 * np.pi * k / M

# Ideal Lowpass
w_ideal = np.linspace(0, np.pi, 200)
H_ideal = np.where(w_ideal <= w_c, 1.0, 0.0)
ax.plot(w_ideal, H_ideal, color=(1.0, 1.0, 1.0, 0.3), linestyle='--', label="Ideal Brickwall")

# Samples
H_k = np.where(w_k <= w_c, 1.0, 0.0)
ax.stem(w_k, H_k, linefmt='#3b82f6', markerfmt='o', label="DFT Samples H[k]", basefmt=" ")

ax.set_xlabel("Frequency \u03c9 (radians)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_ylabel("Amplitude |H[k]|", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_title("Frequency Sampling Grid (M=15)", fontsize=12, pad=12)
ax.set_xlim(-0.1, np.pi + 0.1)
ax.set_ylim(-0.1, 1.2)
ax.set_xticks(w_k)
ax.set_xticklabels([f"{k_val}" for k_val in k], fontsize=8)
ax.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
ax.legend(loc='upper right', frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=8.5)

plt.tight_layout()
plt.savefig("images/freq_sampling_discrete.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Plot 2: Transition Band Sample Optimization
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 3.8))

w = np.linspace(0, np.pi, 500)

M_filt = 15
alpha = (M_filt - 1) / 2

def idft_filter(H_samples):
    h = np.zeros(M_filt)
    for n in range(M_filt):
        val = H_samples[0]
        for k in range(1, (M_filt - 1) // 2 + 1):
            val += 2 * H_samples[k] * np.cos(2 * np.pi * k * (n - alpha) / M_filt)
        h[n] = val / M_filt
    return h

def get_response(h):
    H = np.zeros_like(w, dtype=complex)
    for idx, wi in enumerate(w):
        H[idx] = np.sum(h * np.exp(-1j * wi * np.arange(M_filt)))
    return 20 * np.log10(np.abs(H) + 1e-5)

# Case A coefficients
H_samples_A = [1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
h_A = idft_filter(H_samples_A)
resp_A = get_response(h_A)

# Case B coefficients
H_samples_B = [1.0, 1.0, 0.38, 0.0, 0.0, 0.0, 0.0, 0.0]
h_B = idft_filter(H_samples_B)
resp_B = get_response(h_B)

ax.plot(w, resp_A, color='#ef4444', linewidth=1.5, label="Direct Sampling (Stopband ~ -20 dB)")
ax.plot(w, resp_B, color='#10b981', linewidth=1.8, label="Optimized Transition Sample T1=0.38 (Stopband ~ -45 dB)")

ax.set_xlabel("Frequency \u03c9 (radians)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_ylabel("Gain (dB)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_title("Transition Band Optimization Comparison (M=15)", fontsize=12, pad=12)
ax.set_xlim(0, np.pi)
ax.set_ylim(-70, 5)
ax.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
ax.legend(loc='upper right', frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=8.5)

plt.tight_layout()
plt.savefig("images/transition_samples.png", dpi=300)
plt.close()

print("Lecture 24 images generated successfully.")
