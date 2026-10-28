import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
d=np.load('../datos/procesados/ficha.npz'); VEL=d['VEL']; F=list(d['F']); DUR=d['DUR']
lab=['Cadera pitch','Cadera roll','Cadera yaw','Rodilla pitch','Tobillo pitch','Tobillo roll']
rows=[f'D · {l}' for l in lab]+[f'I · {l}' for l in lab]+['Hombro der. pitch','Hombro der. roll','Hombro izq. pitch','Hombro izq. roll','Cabeza pitch','Cabeza yaw']
cmap=LinearSegmentedColormap.from_list('b',['#f4f8fd','#cde2fb','#9ec5f4','#6da7ec','#3987e5','#256abf','#184f95','#0d366b'])
INK,INK2,SURF='#0b0b0b','#52514e','#fcfcfb'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9})
fig,ax=plt.subplots(figsize=(8.2,7.4),facecolor=SURF)
im=ax.imshow(VEL,cmap=cmap,vmin=0,vmax=560,aspect='auto')
for i in range(VEL.shape[0]):
    for j in range(VEL.shape[1]):
        v=VEL[i,j]; ax.text(j,i,f'{v:.0f}',ha='center',va='center',fontsize=8,color='#ffffff' if v>330 else INK)
ax.set_xticks(range(5)); ax.set_xticklabels([f'{f}\n({dd:.2f} s)' for f,dd in zip(F,DUR)],color=INK)
ax.set_yticks(range(len(rows))); ax.set_yticklabels(rows,color=INK)
ax.xaxis.tick_top()
for y in (5.5,11.5,15.5): ax.axhline(y,color=SURF,lw=3)
ax.set_xticks(np.arange(-.5,5,1),minor=True); ax.set_yticks(np.arange(-.5,18,1),minor=True)
ax.grid(which='minor',color=SURF,lw=1.5); ax.tick_params(which='both',length=0)
for s in ax.spines.values(): s.set_visible(False)
cb=fig.colorbar(im,ax=ax,fraction=0.035,pad=0.02); cb.set_label('Velocidad máxima de la articulación (°/s)',color=INK2); cb.outline.set_visible(False); cb.ax.tick_params(colors=INK2)
fig.suptitle('Qué articulaciones trabajan en cada etapa',x=0.02,ha='left',color=INK,fontsize=11,fontweight='bold')
fig.text(0.02,0.918,'Velocidad máxima por etapa, media de patada_02 y patada_03 (tiempo simulado).\nD = pierna derecha (patea) · I = pierna izquierda (apoyo)',fontsize=8.3,color=INK2)
fig.tight_layout(rect=(0,0,1,0.91)); fig.savefig('../figuras/ficha_articulaciones.png',dpi=150,facecolor=SURF); print('ok')
