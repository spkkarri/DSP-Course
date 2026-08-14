import os
import numpy as np
import matplotlib.pyplot as plt

os.makedirs("images", exist_ok=True)

# Dark mode styling parameters
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 9.5
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.2
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['figure.facecolor'] = '#0d121f'
plt.rcParams['axes.facecolor'] = '#0d121f'
plt.rcParams['savefig.facecolor'] = '#0d121f'

def draw_zplane_axes(ax, title=""):
    ax.axhline(0, color='white', linewidth=0.8, alpha=0.3)
    ax.axvline(0, color='white', linewidth=0.8, alpha=0.3)
    uc = plt.Circle((0, 0), 1.0, color='#6366f1', fill=False, linestyle='--', linewidth=1.5, label='Unit Circle ($|z|=1$)')
    ax.add_patch(uc)
    ax.set_aspect('equal')
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_xlabel('Real (Re)')
    ax.set_ylabel('Imaginary (Im)')
    ax.set_title(title, fontsize=10, fontweight='bold', color='#38bdf8')

# Frequency vector from 0 to 2*pi
w_eval = np.linspace(0, 2 * np.pi, 800)
ejw_eval = np.exp(1j * w_eval)

cardinal_w = np.array([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
cardinal_labels = ['0', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$']
cardinal_ejw = np.exp(1j * cardinal_w)


# =============================================================
# CASE 1: Single Zero System H(z) = z - 0.6
# =============================================================
z1 = 0.6 + 0.0j
H1 = ejw_eval - z1
mag1 = np.abs(H1)
phase1 = np.angle(H1)

mag1_cardinal = np.abs(cardinal_ejw - z1)
phase1_cardinal = np.angle(cardinal_ejw - z1)

fig, axs = plt.subplots(1, 3, figsize=(15, 4.5))

draw_zplane_axes(axs[0], title=r"1. Single Zero: $H(z) = z - 0.6$")
axs[0].plot(np.real(z1), np.imag(z1), 'o', color='#10b981', markersize=9, fillstyle='none', markeredgewidth=2.5, label='Zero $z_1 = 0.6$')

colors = ['#ef4444', '#f59e0b', '#38bdf8', '#ec4899', '#ef4444']
for idx, (w_c, label_c) in enumerate(zip(cardinal_w[:4], cardinal_labels[:4])):
    zc = np.exp(1j * w_c)
    axs[0].plot(np.real(zc), np.imag(zc), 'o', color=colors[idx], markersize=5)
    axs[0].annotate(label_c, (np.real(zc)*1.18, np.imag(zc)*1.18), color=colors[idx], fontsize=9, fontweight='bold')

text_box1 = (
    "CARDINAL EVALUATION (0 to 2pi):\n"
    " w=0: |H|=0.40, theta=0 deg\n"
    " w=pi/2: |H|=1.17, theta=120.96 deg\n"
    " w=pi: |H|=1.60, theta=180 deg\n"
    " w=3pi/2: |H|=1.17, theta=-120.96 deg"
)
axs[0].text(0.02, 0.05, text_box1, transform=axs[0].transAxes, fontsize=7.5,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#0dd5c5', alpha=0.9))
axs[0].legend(loc='upper left', fontsize=7.5)

# Magnitude
axs[1].plot(w_eval, mag1, color='#0dd5c5', linewidth=2)
axs[1].plot(cardinal_w, mag1_cardinal, 'ro', markersize=6, label='Cardinal Points')
axs[1].set_title(r"Magnitude $|H(e^{j\omega})|$")
axs[1].set_xlabel(r"Frequency $\omega$ (rad)")
axs[1].set_ylabel("Magnitude")
axs[1].set_xticks(cardinal_w)
axs[1].set_xticklabels(cardinal_labels)
axs[1].legend(fontsize=7.5)

# Phase
axs[2].plot(w_eval, phase1, color='#8b5cf6', linewidth=2)
axs[2].plot(cardinal_w, phase1_cardinal, 'ro', markersize=6, label='Cardinal Points')
axs[2].set_title(r"Phase $\angle H(e^{j\omega})$")
axs[2].set_xlabel(r"Frequency $\omega$ (rad)")
axs[2].set_ylabel("Phase (rad)")
axs[2].set_xticks(cardinal_w)
axs[2].set_xticklabels(cardinal_labels)
axs[2].legend(fontsize=7.5)

plt.tight_layout()
plt.savefig("images/vector_geometric_single_zero.png", dpi=300)
plt.close()


# =============================================================
# CASE 2: Single Pole System H(z) = 1 / (z - 0.7)
# =============================================================
p1 = 0.7 + 0.0j
H2 = 1.0 / (ejw_eval - p1)
mag2 = np.abs(H2)
phase2 = np.angle(H2)

mag2_cardinal = np.abs(1.0 / (cardinal_ejw - p1))
phase2_cardinal = np.angle(1.0 / (cardinal_ejw - p1))

fig, axs = plt.subplots(1, 3, figsize=(15, 4.5))

draw_zplane_axes(axs[0], title=r"2. Single Pole: $H(z) = \frac{1}{z - 0.7}$")
axs[0].plot(np.real(p1), np.imag(p1), 'x', color='#ef4444', markersize=10, markeredgewidth=2.5, label='Pole $p_1 = 0.7$')

for idx, (w_c, label_c) in enumerate(zip(cardinal_w[:4], cardinal_labels[:4])):
    zc = np.exp(1j * w_c)
    axs[0].plot(np.real(zc), np.imag(zc), 'o', color=colors[idx], markersize=5)
    axs[0].annotate(label_c, (np.real(zc)*1.18, np.imag(zc)*1.18), color=colors[idx], fontsize=9, fontweight='bold')

text_box2 = (
    "CARDINAL EVALUATION (0 to 2pi):\n"
    " w=0: |H|=3.33, theta=0 deg (Peak)\n"
    " w=pi/2: |H|=0.82, theta=-125.00 deg\n"
    " w=pi: |H|=0.59, theta=-180 deg\n"
    " w=3pi/2: |H|=0.82, theta=125.00 deg\n"
    " STABILITY: |0.7|<1 => BIBO STABLE"
)
axs[0].text(0.02, 0.05, text_box2, transform=axs[0].transAxes, fontsize=7.5,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#ef4444', alpha=0.9))
axs[0].legend(loc='upper left', fontsize=7.5)

# Magnitude
axs[1].plot(w_eval, mag2, color='#0dd5c5', linewidth=2)
axs[1].plot(cardinal_w, mag2_cardinal, 'ro', markersize=6, label='Cardinal Points')
axs[1].set_title(r"Magnitude $|H(e^{j\omega})|$")
axs[1].set_xlabel(r"Frequency $\omega$ (rad)")
axs[1].set_ylabel("Magnitude")
axs[1].set_xticks(cardinal_w)
axs[1].set_xticklabels(cardinal_labels)
axs[1].legend(fontsize=7.5)

# Phase
axs[2].plot(w_eval, phase2, color='#8b5cf6', linewidth=2)
axs[2].plot(cardinal_w, phase2_cardinal, 'ro', markersize=6, label='Cardinal Points')
axs[2].set_title(r"Phase $\angle H(e^{j\omega})$")
axs[2].set_xlabel(r"Frequency $\omega$ (rad)")
axs[2].set_ylabel("Phase (rad)")
axs[2].set_xticks(cardinal_w)
axs[2].set_xticklabels(cardinal_labels)
axs[2].legend(fontsize=7.5)

plt.tight_layout()
plt.savefig("images/vector_geometric_single_pole.png", dpi=300)
plt.close()


# =============================================================
# CASE 3: One Pole + One Zero System H(z) = (z - 0.8) / (z - 0.5)
# =============================================================
z3 = 0.8 + 0.0j
p3 = 0.5 + 0.0j
H3 = (ejw_eval - z3) / (ejw_eval - p3)
mag3 = np.abs(H3)
phase3 = np.angle(H3)

mag3_cardinal = np.abs((cardinal_ejw - z3) / (cardinal_ejw - p3))
phase3_cardinal = np.angle((cardinal_ejw - z3) / (cardinal_ejw - p3))

fig, axs = plt.subplots(1, 3, figsize=(15, 4.5))

draw_zplane_axes(axs[0], title=r"3. One Pole + One Zero: $H(z) = \frac{z - 0.8}{z - 0.5}$")
axs[0].plot(np.real(z3), np.imag(z3), 'o', color='#10b981', markersize=9, fillstyle='none', markeredgewidth=2.5, label='Zero $z_1 = 0.8$')
axs[0].plot(np.real(p3), np.imag(p3), 'x', color='#ef4444', markersize=10, markeredgewidth=2.5, label='Pole $p_1 = 0.5$')

for idx, (w_c, label_c) in enumerate(zip(cardinal_w[:4], cardinal_labels[:4])):
    zc = np.exp(1j * w_c)
    axs[0].plot(np.real(zc), np.imag(zc), 'o', color=colors[idx], markersize=5)
    axs[0].annotate(label_c, (np.real(zc)*1.18, np.imag(zc)*1.18), color=colors[idx], fontsize=9, fontweight='bold')

text_box3 = (
    "CARDINAL EVALUATION (0 to 2pi):\n"
    " w=0: |H|=0.40, theta=0 deg\n"
    " w=pi/2: |H|=1.15, theta=+12.09 deg\n"
    " w=pi: |H|=1.20, theta=0 deg\n"
    " w=3pi/2: |H|=1.15, theta=-12.09 deg\n"
    " STABILITY: |0.5|<1 => BIBO STABLE"
)
axs[0].text(0.02, 0.05, text_box3, transform=axs[0].transAxes, fontsize=7.5,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#38bdf8', alpha=0.9))
axs[0].legend(loc='upper left', fontsize=7.5)

# Magnitude
axs[1].plot(w_eval, mag3, color='#0dd5c5', linewidth=2)
axs[1].plot(cardinal_w, mag3_cardinal, 'ro', markersize=6, label='Cardinal Points')
axs[1].set_title(r"Magnitude $|H(e^{j\omega})|$")
axs[1].set_xlabel(r"Frequency $\omega$ (rad)")
axs[1].set_ylabel("Magnitude")
axs[1].set_xticks(cardinal_w)
axs[1].set_xticklabels(cardinal_labels)
axs[1].legend(fontsize=7.5)

# Phase
axs[2].plot(w_eval, phase3, color='#8b5cf6', linewidth=2)
axs[2].plot(cardinal_w, phase3_cardinal, 'ro', markersize=6, label='Cardinal Points')
axs[2].set_title(r"Phase $\angle H(e^{j\omega})$")
axs[2].set_xlabel(r"Frequency $\omega$ (rad)")
axs[2].set_ylabel("Phase (rad)")
axs[2].set_xticks(cardinal_w)
axs[2].set_xticklabels(cardinal_labels)
axs[2].legend(fontsize=7.5)

plt.tight_layout()
plt.savefig("images/vector_geometric_one_pole_one_zero.png", dpi=300)
plt.close()


# =============================================================
# CASE 4: Two Poles + Two Zeros System H(z) = (z^2 - 1) / (z^2 - 0.8 z + 0.25)
# =============================================================
z4_1 = 1.0 + 0.0j
z4_2 = -1.0 + 0.0j
p4_1 = 0.4 + 0.3j
p4_2 = 0.4 - 0.3j

H4 = ((ejw_eval - z4_1) * (ejw_eval - z4_2)) / ((ejw_eval - p4_1) * (ejw_eval - p4_2))
mag4 = np.abs(H4)
phase4 = np.angle(H4)

H4_cardinal = ((cardinal_ejw - z4_1) * (cardinal_ejw - z4_2)) / ((cardinal_ejw - p4_1) * (cardinal_ejw - p4_2))
mag4_cardinal = np.abs(H4_cardinal)
phase4_cardinal = np.angle(H4_cardinal)

fig, axs = plt.subplots(1, 3, figsize=(15, 4.5))

draw_zplane_axes(axs[0], title=r"4. Two Poles + Two Zeros")
axs[0].plot(np.real(z4_1), np.imag(z4_1), 'o', color='#10b981', markersize=8, fillstyle='none', markeredgewidth=2.5, label=r'Zeros $z_{1,2} = \pm 1$')
axs[0].plot(np.real(z4_2), np.imag(z4_2), 'o', color='#10b981', markersize=8, fillstyle='none', markeredgewidth=2.5)
axs[0].plot(np.real(p4_1), np.imag(p4_1), 'x', color='#ef4444', markersize=9, markeredgewidth=2.5, label=r'Poles $p_{1,2} = 0.4 \pm j0.3$')
axs[0].plot(np.real(p4_2), np.imag(p4_2), 'x', color='#ef4444', markersize=9, markeredgewidth=2.5)

for idx, (w_c, label_c) in enumerate(zip(cardinal_w[:4], cardinal_labels[:4])):
    zc = np.exp(1j * w_c)
    axs[0].plot(np.real(zc), np.imag(zc), 'o', color=colors[idx], markersize=5)
    axs[0].annotate(label_c, (np.real(zc)*1.18, np.imag(zc)*1.18), color=colors[idx], fontsize=9, fontweight='bold')

text_box4 = (
    "CARDINAL EVALUATION (0 to 2pi):\n"
    " w=0: |H|=0.00 (Notch)\n"
    " w=pi/2: |H|=1.82, theta=133.15 deg\n"
    " w=pi: |H|=0.00 (Notch)\n"
    " w=3pi/2: |H|=1.82, theta=-133.15 deg\n"
    " STABILITY: |p|=0.5<1 => BIBO STABLE"
)
axs[0].text(0.02, 0.05, text_box4, transform=axs[0].transAxes, fontsize=7.5,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#38bdf8', alpha=0.9))
axs[0].legend(loc='upper left', fontsize=7.5)

# Magnitude
axs[1].plot(w_eval, mag4, color='#0dd5c5', linewidth=2)
axs[1].plot(cardinal_w, mag4_cardinal, 'ro', markersize=6, label='Cardinal Points')
axs[1].set_title(r"Magnitude $|H(e^{j\omega})|$")
axs[1].set_xlabel(r"Frequency $\omega$ (rad)")
axs[1].set_ylabel("Magnitude")
axs[1].set_xticks(cardinal_w)
axs[1].set_xticklabels(cardinal_labels)
axs[1].legend(fontsize=7.5)

# Phase
axs[2].plot(w_eval, phase4, color='#8b5cf6', linewidth=2)
axs[2].plot(cardinal_w, phase4_cardinal, 'ro', markersize=6, label='Cardinal Points')
axs[2].set_title(r"Phase $\angle H(e^{j\omega})$")
axs[2].set_xlabel(r"Frequency $\omega$ (rad)")
axs[2].set_ylabel("Phase (rad)")
axs[2].set_xticks(cardinal_w)
axs[2].set_xticklabels(cardinal_labels)
axs[2].legend(fontsize=7.5)

plt.tight_layout()
plt.savefig("images/vector_geometric_two_poles_two_zeros.png", dpi=300)
plt.close()

print("All 4 geometric vector demonstration plots successfully regenerated with cardinal points.")
