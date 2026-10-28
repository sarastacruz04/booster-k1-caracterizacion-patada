import sys, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
d = np.load(sys.argv[1]); out = sys.argv[2]; titulo = sys.argv[3] if len(sys.argv) > 3 else ''
names = list(d['names']); P = d['P']; t = d['t'] - d['t'][0]; I = d['I']; ti = I[:,0] - d['t'][0]
x,y,z,w = I[:,2],I[:,3],I[:,4],I[:,5]
roll = np.degrees(np.arctan2(2*(w*x+y*z),1-2*(x*x+y*y))); pitch = np.degrees(np.arcsin(np.clip(2*(w*y-z*x),-1,1)))
C = ['#2a78d6', '#eb6834', '#1baf7a']
INK, INK2, GRID, SURF = '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9})
fig, axs = plt.subplots(3, 1, figsize=(8.2, 7.2), sharex=True, facecolor=SURF)
paneles = [
  ('Pierna derecha (ángulo, °)', [('Right_Hip_Pitch','Cadera pitch'), ('Right_Knee_Pitch','Rodilla pitch'), ('Right_Ankle_Pitch','Tobillo pitch')]),
  ('Pierna izquierda (ángulo, °)', [('Left_Hip_Pitch','Cadera pitch'), ('Left_Knee_Pitch','Rodilla pitch'), ('Left_Ankle_Pitch','Tobillo pitch')]),
]
for ax, (tt, ser) in zip(axs[:2], paneles):
    for k, (n, lab) in enumerate(ser):
        v = np.degrees(P[:, names.index(n)])
        ax.plot(t, v, color=C[k], lw=2, label=lab)
    ax.set_title(tt, loc='left', color=INK, fontsize=10, fontweight='bold')
ax = axs[2]
ax.plot(ti, pitch, color=C[0], lw=2, label='Pitch del torso (adelante +)')
ax.plot(ti, roll, color=C[1], lw=2, label='Roll del torso (lateral)')
ax.set_title('Inclinación del torso, IMU (°)', loc='left', color=INK, fontsize=10, fontweight='bold')
ax.set_xlabel('Tiempo desde el inicio de la grabación (s)', color=INK2)
for ax in axs:
    ax.set_facecolor(SURF); ax.grid(axis='y', color=GRID, lw=0.8); ax.set_axisbelow(True)
    for s in ('top','right'): ax.spines[s].set_visible(False)
    for s in ('left','bottom'): ax.spines[s].set_color(GRID)
    ax.tick_params(colors=INK2)
    ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1), frameon=False, labelcolor=INK)
if titulo: fig.suptitle(titulo, x=0.02, ha='left', color=INK, fontsize=11, fontweight='bold')
fig.tight_layout(); fig.savefig(out, dpi=150, facecolor=SURF)
print('ok', out)
