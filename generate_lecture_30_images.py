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
# Plot 1: Adaptive Noise Cancellation Diagram (Flowchart style)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 3.5))

# Draw blocks
# Signal source
ax.text(0.1, 0.8, "Signal s[n]\n+ Noise v0[n]", bbox=dict(facecolor='#1e293b', edgecolor='#3b82f6', boxstyle='round,pad=0.5'), ha='center', fontsize=9.5)
# Reference noise source
ax.text(0.1, 0.2, "Reference\nNoise v1[n]", bbox=dict(facecolor='#1e293b', edgecolor='#10b981', boxstyle='round,pad=0.5'), ha='center', fontsize=9.5)
# Adaptive filter block
ax.text(0.55, 0.2, "Adaptive FIR Filter\nW(z)", bbox=dict(facecolor='#1e293b', edgecolor='#8b5cf6', boxstyle='round,pad=0.6'), ha='center', fontsize=10)
# Summing junction
ax.text(0.55, 0.8, "  +  \n( \u03a3 )\n  -  ", bbox=dict(facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.3), boxstyle='circle'), ha='center', fontsize=10)
# Output
ax.text(0.9, 0.8, "Error e[n]\n(Clean s[n])", bbox=dict(facecolor='#1e293b', edgecolor='#f59e0b', boxstyle='round,pad=0.5'), ha='center', fontsize=9.5)

# Arrows
ax.annotate("", xy=(0.47, 0.8), xytext=(0.22, 0.8), arrowprops=dict(arrowstyle="->", color='#3b82f6', lw=1.5))
ax.annotate("", xy=(0.42, 0.2), xytext=(0.21, 0.2), arrowprops=dict(arrowstyle="->", color='#10b981', lw=1.5))
ax.annotate("", xy=(0.55, 0.70), xytext=(0.55, 0.32), arrowprops=dict(arrowstyle="->", color='#8b5cf6', lw=1.5))
ax.annotate("", xy=(0.80, 0.8), xytext=(0.63, 0.8), arrowprops=dict(arrowstyle="->", color='#f59e0b', lw=1.5))

# Feedback loop for LMS algorithm adjustment
# From output line back to filter block
ax.annotate("", xy=(0.55, 0.34), xytext=(0.75, 0.34), arrowprops=dict(arrowstyle="->", color='#fb7185', lw=1.2, linestyle=':'))
ax.plot([0.75, 0.75], [0.34, 0.8], color='#fb7185', linestyle=':', linewidth=1.2)

# Text labels on arrows
ax.text(0.57, 0.5, "y[n]\n(Noise Est)", color='#8b5cf6', fontsize=8.5, ha='left')
ax.text(0.72, 0.5, "LMS Adaptation Loop", color='#fb7185', fontsize=8, rotation=90, va='center')

ax.set_xlim(0, 1.0)
ax.set_ylim(0, 1.0)
ax.axis('off')
ax.set_title("Adaptive Noise Cancellation (ANC) Architecture", fontsize=11, pad=10)

plt.tight_layout()
plt.savefig("images/adaptive_noise_cancellation.png", dpi=300)
plt.close()

# -------------------------------------------------------------
# Plot 2: Channel Equalizer Frequency Responses
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 3.5))

f = np.linspace(0, 1.0, 300)
# Channel response: lowpass roll-off with a dip
H_channel = 1.0 / (1.0 + 3.0*f**2) * (1.0 - 0.4*np.exp(-((f-0.5)/0.1)**2))

# Equalizer response: exact inverse of channel
H_equalizer = 1.0 / H_channel

# Combined response: flat line
H_combined = H_channel * H_equalizer

ax.plot(f, 20*np.log10(H_channel), color='#ef4444', linewidth=1.8, label="Distorted Channel C(z)")
ax.plot(f, 20*np.log10(H_equalizer), color='#3b82f6', linewidth=1.8, label="Channel Equalizer E(z)")
ax.plot(f, 20*np.log10(H_combined), color='#10b981', linewidth=2.0, linestyle='--', label="Combined System C(z)E(z)")

ax.set_xlabel("Normalized Frequency (f / f_nyquist)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_ylabel("Gain (dB)", color=(1.0, 1.0, 1.0, 0.6), fontsize=9)
ax.set_title("Channel Equalization Frequency Responses", fontsize=11, pad=12)
ax.set_xlim(0, 1.0)
ax.set_ylim(-20, 20)
ax.tick_params(colors=(1.0, 1.0, 1.0, 0.4), labelsize=8)
ax.legend(frameon=True, facecolor='#111827', edgecolor=(1.0, 1.0, 1.0, 0.1), fontsize=8.5)

plt.tight_layout()
plt.savefig("images/equalizer_response.png", dpi=300)
plt.close()

print("Lecture 30 images generated successfully.")
