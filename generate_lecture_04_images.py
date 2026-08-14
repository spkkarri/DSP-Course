import os
import numpy as np
import matplotlib.pyplot as plt

os.makedirs("images", exist_ok=True)

# Dark mode styling parameters
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.2
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['figure.facecolor'] = '#0d121f'
plt.rcParams['axes.facecolor'] = '#0d121f'
plt.rcParams['savefig.facecolor'] = '#0d121f'

omega = np.linspace(-np.pi, np.pi, 500)

# -------------------------------------------------------------
# Plot 1: Magnitude & Phase of Low-Pass vs. High-Pass Filter
# -------------------------------------------------------------
r = 0.7
H_LP = 1 / (1 - r * np.exp(-1j * omega))
H_HP = 1 / (1 + r * np.exp(-1j * omega))

fig, axs = plt.subplots(2, 2, figsize=(10, 7))

# LPF Magnitude
axs[0, 0].plot(omega, np.abs(H_LP), color='#0dd5c5', linewidth=2)
axs[0, 0].set_title(r"LPF Magnitude $|H(e^{j\omega})|$ ($r=0.7$)")
axs[0, 0].set_ylabel("Gain")
axs[0, 0].set_xticks([-np.pi, 0, np.pi])
axs[0, 0].set_xticklabels([r'$-\pi$', '0', r'$\pi$'])

# LPF Phase
axs[1, 0].plot(omega, np.angle(H_LP), color='#0dd5c5', linewidth=2)
axs[1, 0].set_title(r"LPF Phase $\angle H(e^{j\omega})$")
axs[1, 0].set_xlabel(r"$\omega$ (rad/sample)")
axs[1, 0].set_ylabel("Phase (rad)")
axs[1, 0].set_xticks([-np.pi, 0, np.pi])
axs[1, 0].set_xticklabels([r'$-\pi$', '0', r'$\pi$'])

# HPF Magnitude
axs[0, 1].plot(omega, np.abs(H_HP), color='#ef4444', linewidth=2)
axs[0, 1].set_title(r"HPF Magnitude $|H(e^{j\omega})|$ ($r=-0.7$)")
axs[0, 1].set_xticks([-np.pi, 0, np.pi])
axs[0, 1].set_xticklabels([r'$-\pi$', '0', r'$\pi$'])

# HPF Phase
axs[1, 1].plot(omega, np.angle(H_HP), color='#ef4444', linewidth=2)
axs[1, 1].set_title(r"HPF Phase $\angle H(e^{j\omega})$")
axs[1, 1].set_xlabel(r"$\omega$ (rad/sample)")
axs[1, 1].set_xticks([-np.pi, 0, np.pi])
axs[1, 1].set_xticklabels([r'$-\pi$', '0', r'$\pi$'])

plt.tight_layout()
plt.savefig("images/frequency_response_lpf_hpf.png", dpi=300)
plt.close()


# -------------------------------------------------------------
# Plot 2: Group Delay Analysis
# -------------------------------------------------------------
r1 = 0.5
r2 = 0.85

tau_g1 = (r1 * np.cos(omega) - r1**2) / (1 + r1**2 - 2 * r1 * np.cos(omega))
tau_g2 = (r2 * np.cos(omega) - r2**2) / (1 + r2**2 - 2 * r2 * np.cos(omega))

fig, axs = plt.subplots(2, 1, figsize=(9, 7))

# Magnitude responses for comparison
axs[0].plot(omega, 1 / np.sqrt(1 + r1**2 - 2 * r1 * np.cos(omega)), color='#6366f1', linewidth=2, label=r'$r=0.5$')
axs[0].plot(omega, 1 / np.sqrt(1 + r2**2 - 2 * r2 * np.cos(omega)), color='#0dd5c5', linewidth=2, label=r'$r=0.85$')
axs[0].set_title(r"Filter Magnitude response $|H(e^{j\omega})|$ comparison")
axs[0].set_ylabel("Gain")
axs[0].set_xticks([-np.pi, 0, np.pi])
axs[0].set_xticklabels([r'$-\pi$', '0', r'$\pi$'])
axs[0].legend()

# Group delay
axs[1].plot(omega, tau_g1, color='#6366f1', linewidth=2, label=r'$r=0.5$')
axs[1].plot(omega, tau_g2, color='#0dd5c5', linewidth=2, label=r'$r=0.85$')
axs[1].set_title(r"Group Delay $\tau_g(\omega)$ (High poles delay frequencies longer near cutoff)")
axs[1].set_xlabel(r"$\omega$ (rad/sample)")
axs[1].set_ylabel("Delay (samples)")
axs[1].set_xticks([-np.pi, 0, np.pi])
axs[1].set_xticklabels([r'$-\pi$', '0', r'$\pi$'])
axs[1].legend()

plt.tight_layout()
plt.savefig("images/group_delay_analysis.png", dpi=300)
plt.close()


# -------------------------------------------------------------
# Plot 3 (NEW): Intuitive Concept Comparison Diagram (Phase Delay vs Group Delay)
# -------------------------------------------------------------
fig, axs = plt.subplots(2, 1, figsize=(10, 7))

t_int = np.linspace(-2, 4, 1000)

# Panel A: Phase Delay (Single Pure Sine Wave)
f0 = 1.0
w0 = 2 * np.pi * f0
tau_p_ex = 0.5

sin_in = np.sin(w0 * t_int)
sin_out = np.sin(w0 * (t_int - tau_p_ex))

axs[0].plot(t_int, sin_in, color='#38bdf8', linestyle='--', label='Original Pure Sine Wave $x(t) = \sin(\omega_0 t)$')
axs[0].plot(t_int, sin_out, color='#0dd5c5', linewidth=2.5, label='Phase Delayed Sine Wave $y(t) = \sin(\omega_0(t - \\tau_p))$')
axs[0].annotate('', xy=(0.25, 1.0), xytext=(0.25 + tau_p_ex, 1.0),
             arrowprops=dict(arrowstyle='<->', color='#f59e0b', lw=2))
axs[0].text(0.25 + tau_p_ex/2, 1.12, r'Phase Delay $\tau_p = -\frac{\theta(\omega)}{\omega}$', color='#f59e0b',
             fontsize=10, fontweight='bold', ha='center')

# Callout box for Phase Delay Intuition
text_box_pd = (
    "PHASE DELAY INTUITION:\n"
    "• Single Tone / Carrier Delay\n"
    "• Analogy: Delay of a runner's stride rhythm\n"
    "• Formula: tau_p = -theta(w) / w"
)
axs[0].text(0.98, 0.20, text_box_pd, transform=axs[0].transAxes, fontsize=8.5,
             verticalalignment='center', horizontalalignment='right',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor='#38bdf8', alpha=0.9))

axs[0].set_title('1. PHASE DELAY (\\tau_p): Delay experienced by a SINGLE pure frequency tone', fontsize=11, fontweight='bold', color='#38bdf8')
axs[0].set_ylabel('Amplitude')
axs[0].set_ylim(-1.4, 1.4)
axs[0].legend(loc='upper left', fontsize=8)


# Panel B: Group Delay (Group of Frequencies / Beat Wave Packet Envelope)
w1 = 2 * np.pi * 3.5
w2 = 2 * np.pi * 4.5
w_center = 2 * np.pi * 4.0
w_beat = 2 * np.pi * 0.5

tau_p_grp = 0.3
tau_g_grp = 1.0

# Input beat packet
env_beat_in = np.cos(w_beat * t_int)
carrier_beat_in = np.cos(w_center * t_int)
packet_in = env_beat_in * carrier_beat_in

# Output beat packet: envelope delayed by tau_g, carrier delayed by tau_p
env_beat_out = np.cos(w_beat * (t_int - tau_g_grp))
carrier_beat_out = np.cos(w_center * (t_int - tau_p_grp))
packet_out = env_beat_out * carrier_beat_out

axs[1].plot(t_int, packet_in, color='#a855f7', linestyle='--', alpha=0.5, label='Input Frequency Group (Wave Packet)')
axs[1].plot(t_int, env_beat_in, color='#f59e0b', linestyle=':', label='Original Envelope')
axs[1].plot(t_int, packet_out, color='#ec4899', linewidth=1.5, label='Output Wave Packet')
axs[1].plot(t_int, env_beat_out, color='#ec4899', linestyle='--', linewidth=2.5, label='Delayed Envelope (Group Delay $\\tau_g$)')

# Envelope shift annotation
axs[1].annotate('', xy=(0.0, 1.0), xytext=(tau_g_grp, 1.0),
             arrowprops=dict(arrowstyle='<->', color='#ec4899', lw=2.5))
axs[1].text(tau_g_grp/2, 1.15, r'Group Delay $\tau_g = -\frac{d\theta(\omega)}{d\omega}$', color='#ec4899',
             fontsize=10, fontweight='bold', ha='center')

# Callout box for Group Delay Intuition
text_box_gd = (
    "GROUP DELAY INTUITION:\n"
    "• Wave Packet / Envelope Burst Delay\n"
    "• Analogy: Delay of the entire runner pack\n"
    "• Formula: tau_g = -d[theta(w)] / dw"
)
axs[1].text(0.98, 0.20, text_box_gd, transform=axs[1].transAxes, fontsize=8.5,
             verticalalignment='center', horizontalalignment='right',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#1e293b', edgecolor='#ec4899', alpha=0.9))

axs[1].set_title('2. GROUP DELAY (\\tau_g): Delay experienced by the OVERALL ENVELOPE / PACKET of a group of frequencies', fontsize=11, fontweight='bold', color='#ec4899')
axs[1].set_xlabel('Time (seconds)')
axs[1].set_ylabel('Amplitude')
axs[1].set_ylim(-1.4, 1.4)
axs[1].legend(loc='upper left', fontsize=8)

plt.tight_layout()
plt.savefig("images/phase_vs_group_delay_intuition.png", dpi=300)
plt.close()


# -------------------------------------------------------------
# Plot 4: Impact of Constant vs Non-Constant Group Delay on Voltage Waveform
# -------------------------------------------------------------
t = np.linspace(0, 4, 1000)
w0 = 2 * np.pi * 1.0

v_in = 100 * np.sin(w0 * t) + 35 * np.sin(3 * w0 * t) + 15 * np.sin(5 * w0 * t)

# Case A: Linear Phase (Constant Group Delay tau = 0.3 s for all frequencies)
tau_const = 0.3
v_out_linear = 100 * np.sin(w0 * (t - tau_const)) + 35 * np.sin(3 * w0 * (t - tau_const)) + 15 * np.sin(5 * w0 * (t - tau_const))

# Case B: Non-Linear Phase (Dispersive Group Delay: fundamental tau=0.3s, 3rd harmonic tau=0.55s, 5th harmonic tau=0.85s)
tau_1 = 0.30
tau_3 = 0.55
tau_5 = 0.85
v_out_dispersive = 100 * np.sin(w0 * (t - tau_1)) + 35 * np.sin(3 * w0 * (t - tau_3)) + 15 * np.sin(5 * w0 * (t - tau_5))

fig, axs = plt.subplots(2, 1, figsize=(10, 7))

# Time Domain Voltage Signals
axs[0].plot(t, v_in, color='#e2e8f0', linestyle='--', alpha=0.6, label='Input Voltage $V_{in}(t)$ ($V_{peak} = 150V$)')
axs[0].plot(t, v_out_linear, color='#0dd5c5', linewidth=2, label='Linear Phase Output (Constant $\\tau_g$: Waveform Preserved, $V_{peak}=150V$)')
axs[0].plot(t, v_out_dispersive, color='#ef4444', linewidth=2, label='Non-Linear Phase Output (Dispersive $\\tau_g$: Shape Distortion, $V_{peak}=118V$)')

# Callout annotation for voltage peak drop & dispersion
axs[0].annotate('Harmonics misaligned!\n$V_{peak}$ reduced & edges smeared',
                xy=(1.5, 118), xytext=(1.9, 140),
                arrowprops=dict(facecolor='#ef4444', shrink=0.05, width=1.5, headwidth=7),
                fontsize=8.5, color='#ef4444', fontweight='bold')

axs[0].set_title('Time Domain Impact on Composite Voltage Signal (Harmonic Distortion & Peak Attenuation)', fontsize=11)
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Voltage (V)')
axs[0].legend(loc='upper right', fontsize=8)

# Frequency Domain / Group Delay Characteristics
freqs = np.array([1, 3, 5])
gd_linear = np.array([tau_const, tau_const, tau_const])
gd_dispersive = np.array([tau_1, tau_3, tau_5])

axs[1].stem(freqs - 0.1, gd_linear, linefmt='C0-', markerfmt='C0o', basefmt=" ", label='Linear Phase System ($\tau_g(\omega) = const$)')
axs[1].stem(freqs + 0.1, gd_dispersive, linefmt='r-', markerfmt='ro', basefmt=" ", label='Dispersive System ($\tau_g(\omega)$ varies with $\omega$)')
axs[1].set_title('Frequency Domain Group Delay Profile $\tau_g(\omega)$ at Harmonics ($f_0, 3f_0, 5f_0$)', fontsize=11)
axs[1].set_xlabel('Frequency Multiplier ($f / f_0$)')
axs[1].set_ylabel('Group Delay $\tau_g$ (seconds)')
axs[1].set_xticks([1, 3, 5])
axs[1].set_xticklabels(['$f_0$ (Fundamental)', '$3f_0$ (3rd Harmonic)', '$5f_0$ (5th Harmonic)'])
axs[1].legend(loc='upper left', fontsize=8)

plt.tight_layout()
plt.savefig("images/voltage_signal_dispersion.png", dpi=300)
plt.close()


# -------------------------------------------------------------
# Plot 5: Carrier Delay (Phase Delay) vs Envelope Delay (Group Delay)
# -------------------------------------------------------------
t2 = np.linspace(-3, 5, 1200)
w_c = 2 * np.pi * 4.0  # Carrier frequency
sigma = 0.8            # Gaussian envelope width

# Input envelope & carrier
env_in = np.exp(-t2**2 / (2 * sigma**2))
carrier_in = np.cos(w_c * t2)
v_rf_in = env_in * carrier_in

# Phase delay and Group delay values
tau_p_val = 0.45  # Carrier shift
tau_g_val = 1.20  # Envelope shift

env_out = np.exp(-(t2 - tau_g_val)**2 / (2 * sigma**2))
carrier_out = np.cos(w_c * (t2 - tau_p_val))
v_rf_out = env_out * carrier_out

fig, axs = plt.subplots(2, 1, figsize=(10, 7))

# Input Narrowband Pulse
axs[0].plot(t2, v_rf_in, color='#8b5cf6', label='Input Pulsed RF Voltage $V_{in}(t)$')
axs[0].plot(t2, env_in, color='#f59e0b', linestyle='--', label='Input Envelope $s(t)$')
axs[0].plot(t2, -env_in, color='#f59e0b', linestyle='--')
axs[0].set_title('Narrowband Modulated Input Voltage Signal $V_{in}(t) = s(t) \cos(\omega_0 t)$')
axs[0].set_ylabel('Voltage (V)')
axs[0].legend(loc='upper right', fontsize=8)

# Output Narrowband Pulse showing Tau_p vs Tau_g
axs[1].plot(t2, v_rf_out, color='#0dd5c5', label='Output Voltage $V_{out}(t)$')
axs[1].plot(t2, env_out, color='#ec4899', linestyle='--', linewidth=2, label=f'Output Envelope $s(t - \\tau_g)$, $\\tau_g = {tau_g_val}s$')
axs[1].plot(t2, -env_out, color='#ec4899', linestyle='--', linewidth=2)

# Annotations
axs[1].annotate(f'Group Delay $\\tau_g = {tau_g_val}s$\n(Envelope / Wave Packet Shift)',
                xy=(tau_g_val, 1.0), xytext=(tau_g_val + 0.8, 1.1),
                arrowprops=dict(facecolor='#ec4899', shrink=0.05, width=1.5, headwidth=8),
                fontsize=9, color='#ec4899', fontweight='bold')

axs[1].annotate(f'Phase Delay $\\tau_p = {tau_p_val}s$\n(Carrier Oscillation Shift)',
                xy=(tau_p_val, 0.4), xytext=(tau_p_val - 1.8, 0.7),
                arrowprops=dict(facecolor='#0dd5c5', shrink=0.05, width=1.5, headwidth=8),
                fontsize=9, color='#0dd5c5', fontweight='bold')

axs[1].set_title('Output Signal: Carrier shifted by Phase Delay $\\tau_p$, Envelope shifted by Group Delay $\\tau_g$')
axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Voltage (V)')
axs[1].legend(loc='upper right', fontsize=8)

plt.tight_layout()
plt.savefig("images/narrowband_carrier_envelope_delay.png", dpi=300)
plt.close()

print("All Lecture 4 images generated successfully.")
