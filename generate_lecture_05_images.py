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

# Helper function to draw a complex plane axis
def draw_zplane_axes(ax, xlim=2.2, ylim=2.2):
    ax.axhline(0, color='white', linewidth=0.8, alpha=0.3)
    ax.axvline(0, color='white', linewidth=0.8, alpha=0.3)
    # Draw unit circle
    uc = plt.Circle((0, 0), 1.0, color='#6366f1', fill=False, linestyle='--', linewidth=1.5, label='Unit Circle ($|z|=1$)')
    ax.add_patch(uc)
    ax.set_aspect('equal')
    ax.set_xlim(-xlim, xlim)
    ax.set_ylim(-ylim, ylim)
    ax.set_xlabel('Real (Re)')
    ax.set_ylabel('Imaginary (Im)')

# -------------------------------------------------------------
# Plot 1: ROC of Causal vs. Anti-Causal Exponential with Stability Callouts
# -------------------------------------------------------------
fig, axs = plt.subplots(1, 2, figsize=(11, 5.5))

# 1. Causal ROC: x[n] = 0.7^n u[n] -> ROC: |z| > 0.7
draw_zplane_axes(axs[0])
ring = plt.Circle((0,0), 3.0, color='#0dd5c5', alpha=0.15)
axs[0].add_patch(ring)
inner_disk = plt.Circle((0,0), 0.7, color='#0d121f', fill=True)
axs[0].add_patch(inner_disk)
boundary = plt.Circle((0,0), 0.7, color='#0dd5c5', fill=False, linestyle='-', linewidth=1.5)
axs[0].add_patch(boundary)
axs[0].plot(0.7, 0, 'x', color='#ef4444', markersize=10, markeredgewidth=2.5, label='Pole ($z=0.7$)')
axs[0].plot(0, 0, 'o', color='#10b981', markersize=8, fillstyle='none', markeredgewidth=2, label='Zero ($z=0$)')
axs[0].set_title(r"Causal $0.7^n u[n]$ (ROC: $|z| > 0.7$, Exterior)")
axs[0].legend(loc='upper right', fontsize=8)

axs[0].annotate('STABILITY COMMENT:\nROC includes Unit Circle ($|z|=1$)\n' + r'$\Rightarrow$ SYSTEM IS BIBO STABLE',
                xy=(1.0, 0.0), xytext=(0.8, 1.4),
                arrowprops=dict(facecolor='#10b981', shrink=0.05, width=1.5, headwidth=7),
                fontsize=8.5, color='#10b981', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#10b981', alpha=0.9))

# 2. Anti-Causal ROC: x[n] = -0.7^n u[-n-1] -> ROC: |z| < 0.7 (INSIDE Unit Circle)
draw_zplane_axes(axs[1])
inner_disk_shaded = plt.Circle((0,0), 0.7, color='#0dd5c5', alpha=0.25)
axs[1].add_patch(inner_disk_shaded)
boundary2 = plt.Circle((0,0), 0.7, color='#0dd5c5', fill=False, linestyle='-', linewidth=1.5)
axs[1].add_patch(boundary2)
axs[1].plot(0.7, 0, 'x', color='#ef4444', markersize=10, markeredgewidth=2.5, label='Pole ($z=0.7$)')
axs[1].plot(0, 0, 'o', color='#10b981', markersize=8, fillstyle='none', markeredgewidth=2, label='Zero ($z=0$)')
axs[1].set_title(r"Anti-Causal $-0.7^n u[-n-1]$ (ROC: $|z| < 0.7$, Interior Disk)")
axs[1].legend(loc='upper right', fontsize=8)

axs[1].annotate('STABILITY COMMENT:\nROC excludes Unit Circle ($|z|=1$)\n' + r'$\Rightarrow$ SYSTEM IS UNSTABLE',
                xy=(0.7, 0.7), xytext=(0.8, 1.4),
                arrowprops=dict(facecolor='#ef4444', shrink=0.05, width=1.5, headwidth=7),
                fontsize=8.5, color='#ef4444', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#ef4444', alpha=0.9))

plt.tight_layout()
plt.savefig("images/roc_causal_anticausal.png", dpi=300)
plt.close()


# -------------------------------------------------------------
# Plot 2: ROC of Two-Sided Signal (Annular Ring)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 6.5))
draw_zplane_axes(ax, xlim=2.2, ylim=2.2)

outer_ring = plt.Circle((0,0), 1.5, color='#0dd5c5', alpha=0.20)
ax.add_patch(outer_ring)
inner_disk_mask = plt.Circle((0,0), 0.5, color='#0d121f', fill=True)
ax.add_patch(inner_disk_mask)

b_inner = plt.Circle((0,0), 0.5, color='#0dd5c5', fill=False, linestyle='-', linewidth=1.5)
b_outer = plt.Circle((0,0), 1.5, color='#0dd5c5', fill=False, linestyle='-', linewidth=1.5)
ax.add_patch(b_inner)
ax.add_patch(b_outer)

ax.plot(0.5, 0, 'x', color='#ef4444', markersize=10, markeredgewidth=2.5, label='Pole Causal ($z=0.5$)')
ax.plot(1.5, 0, 'x', color='#ef4444', markersize=10, markeredgewidth=2.5, label='Pole Anti-Causal ($z=1.5$)')

ax.annotate('STABILITY COMMENT:\nROC Ring ($0.5 < |z| < 1.5$) contains Unit Circle ($|z|=1$)\n' + r'$\Rightarrow$ SYSTEM IS BIBO STABLE',
            xy=(0, 1.0), xytext=(-2.1, 1.6),
            arrowprops=dict(facecolor='#10b981', shrink=0.05, width=1.5, headwidth=7),
            fontsize=8.5, color='#10b981', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#10b981', alpha=0.9))

ax.set_title(r"Two-Sided Signal Annular Ring ROC ($0.5 < |z| < 1.5$)")
ax.legend(loc='lower right', fontsize=8)

plt.tight_layout()
plt.savefig("images/zplane_common_pairs.png", dpi=300)
plt.close()


# -------------------------------------------------------------
# Plot 3: Worked Examples of Poles, Zeros, ROC & Stability (Exp, Sin, Cos, Delta)
# -------------------------------------------------------------
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

# Ex 1: Causal Cosine: x[n] = cos(pi/3 n) u[n] -> Poles on unit circle z = e^(+- j pi/3), ROC |z| > 1
draw_zplane_axes(axs[0], xlim=1.5, ylim=1.5)
ring1 = plt.Circle((0,0), 2.5, color='#0dd5c5', alpha=0.15)
axs[0].add_patch(ring1)
disk1 = plt.Circle((0,0), 1.0, color='#0d121f', fill=True)
axs[0].add_patch(disk1)
b1 = plt.Circle((0,0), 1.0, color='#0dd5c5', fill=False, linestyle='-', linewidth=1.5)
axs[0].add_patch(b1)
# Poles at e^(+- j pi/3) = 0.5 +- j 0.866
axs[0].plot(0.5, np.sin(np.pi/3), 'x', color='#ef4444', markersize=9, markeredgewidth=2.5, label=r'Poles $z=e^{\pm j\pi/3}$')
axs[0].plot(0.5, -np.sin(np.pi/3), 'x', color='#ef4444', markersize=9, markeredgewidth=2.5)
axs[0].plot(0, 0, 'o', color='#10b981', markersize=8, fillstyle='none', markeredgewidth=2, label='Zero $z=0$')
axs[0].plot(0.5, 0, 'o', color='#10b981', markersize=8, fillstyle='none', markeredgewidth=2, label=r'Zero $z=\cos(\pi/3)$')
axs[0].set_title(r"Causal $\cos(\frac{\pi}{3}n) u[n]$" + "\nPoles on Unit Circle | ROC: $|z|>1$\n(Marginally Stable)")
axs[0].legend(loc='lower right', fontsize=7.5)

# Ex 2: Damped Sinusoid: x[n] = 0.7^n sin(pi/4 n) u[n] -> Poles at 0.7 e^(+- j pi/4), ROC |z| > 0.7
draw_zplane_axes(axs[1], xlim=1.5, ylim=1.5)
ring2 = plt.Circle((0,0), 2.5, color='#0dd5c5', alpha=0.15)
axs[1].add_patch(ring2)
disk2 = plt.Circle((0,0), 0.7, color='#0d121f', fill=True)
axs[1].add_patch(disk2)
b2 = plt.Circle((0,0), 0.7, color='#0dd5c5', fill=False, linestyle='-', linewidth=1.5)
axs[1].add_patch(b2)
p_re = 0.7 * np.cos(np.pi/4)
p_im = 0.7 * np.sin(np.pi/4)
axs[1].plot(p_re, p_im, 'x', color='#ef4444', markersize=9, markeredgewidth=2.5, label=r'Poles $z=0.7e^{\pm j\pi/4}$')
axs[1].plot(p_re, -p_im, 'x', color='#ef4444', markersize=9, markeredgewidth=2.5)
axs[1].plot(0, 0, 'o', color='#10b981', markersize=8, fillstyle='none', markeredgewidth=2, label='Zero $z=0$')
axs[1].set_title(r"Damped Sinusoid $0.7^n \sin(\frac{\pi}{4}n)u[n]$" + "\nPoles inside Unit Circle | ROC: $|z|>0.7$\n(BIBO STABLE)")
axs[1].legend(loc='lower right', fontsize=7.5)

# Ex 3: Anti-Causal Exponential: x[n] = -(0.8)^n u[-n-1] -> Pole at z=0.8, ROC |z| < 0.8
draw_zplane_axes(axs[2], xlim=1.5, ylim=1.5)
disk3 = plt.Circle((0,0), 0.8, color='#0dd5c5', alpha=0.25)
axs[2].add_patch(disk3)
b3 = plt.Circle((0,0), 0.8, color='#0dd5c5', fill=False, linestyle='-', linewidth=1.5)
axs[2].add_patch(b3)
axs[2].plot(0.8, 0, 'x', color='#ef4444', markersize=9, markeredgewidth=2.5, label='Pole $z=0.8$')
axs[2].plot(0, 0, 'o', color='#10b981', markersize=8, fillstyle='none', markeredgewidth=2, label='Zero $z=0$')
axs[2].set_title(r"Anti-Causal Exponential $-(0.8)^n u[-n-1]$" + "\nROC $|z|<0.8$ (Inside Unit Circle)\n(UNSTABLE)")
axs[2].legend(loc='lower right', fontsize=7.5)

plt.tight_layout()
plt.savefig("images/pole_zero_roc_examples.png", dpi=300)
plt.close()


# -------------------------------------------------------------
# Plot 4 (NEW): Multi-Pole Multi-Zero System: ROC, Pole-Zero Plot, Magnitude & Phase
# -------------------------------------------------------------
# System: H(z) = (z - 0.5) / (z^2 - 0.8 z + 0.25)
# Zero at z = 0.5
# Poles at z = 0.4 +- j 0.3 (magnitude r = sqrt(0.16 + 0.09) = 0.5)
# Causal ROC: |z| > 0.5

fig, axs = plt.subplots(1, 3, figsize=(15, 5))

# 1. Pole-Zero Plot & ROC in Z-Plane
draw_zplane_axes(axs[0], xlim=1.5, ylim=1.5)
ring4 = plt.Circle((0,0), 2.5, color='#0dd5c5', alpha=0.15)
axs[0].add_patch(ring4)
disk4 = plt.Circle((0,0), 0.5, color='#0d121f', fill=True)
axs[0].add_patch(disk4)
b4 = plt.Circle((0,0), 0.5, color='#0dd5c5', fill=False, linestyle='-', linewidth=1.5)
axs[0].add_patch(b4)

# Poles & Zeros
p1_re, p1_im = 0.4, 0.3
axs[0].plot(p1_re, p1_im, 'x', color='#ef4444', markersize=9, markeredgewidth=2.5, label=r'Poles $p_{1,2} = 0.4 \pm j0.3$ ($|p|=0.5$)')
axs[0].plot(p1_re, -p1_im, 'x', color='#ef4444', markersize=9, markeredgewidth=2.5)
axs[0].plot(0.5, 0, 'o', color='#10b981', markersize=8, fillstyle='none', markeredgewidth=2, label=r'Zero $z_1 = 0.5$')

axs[0].set_title(r"Multi-Pole Multi-Zero $H(z) = \frac{z - 0.5}{z^2 - 0.8z + 0.25}$" + "\nROC: $|z| > 0.5$ (BIBO STABLE)")
axs[0].legend(loc='lower right', fontsize=7.5)

# 2. Magnitude Response |H(e^jw)|
w = np.linspace(0, np.pi, 500)
ejw = np.exp(1j * w)
H_w = (ejw - 0.5) / (ejw**2 - 0.8 * ejw + 0.25)
mag_H = np.abs(H_w)
phase_H = np.angle(H_w)

axs[1].plot(w, mag_H, color='#0dd5c5', linewidth=2)
axs[1].set_title(r"Magnitude Response $|H(e^{j\omega})|$ (Resonance near $\omega = \arctan(0.75) \approx 0.64$ rad)")
axs[1].set_xlabel(r"Frequency $\omega$ (rad/sample)")
axs[1].set_ylabel(r"Gain $|H(e^{j\omega})|$")
axs[1].set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
axs[1].set_xticklabels(['0', r'$\pi/4$', r'$\pi/2$', r'$3\pi/4$', r'$\pi$'])

# 3. Phase Response angle H(e^jw)
axs[2].plot(w, phase_H, color='#8b5cf6', linewidth=2)
axs[2].set_title(r"Phase Response $\angle H(e^{j\omega})$ (radians)")
axs[2].set_xlabel(r"Frequency $\omega$ (rad/sample)")
axs[2].set_ylabel(r"Phase $\theta(\omega)$ (rad)")
axs[2].set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
axs[2].set_xticklabels(['0', r'$\pi/4$', r'$\pi/2$', r'$3\pi/4$', r'$\pi$'])

plt.tight_layout()
plt.savefig("images/multipole_multizero_mag_phase.png", dpi=300)
plt.close()

print("All Lecture 5 images generated successfully.")
