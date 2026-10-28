import glob, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
INK,INK2,GRID,SURF='#0b0b0b','#52514e','#e4e3df','#fcfcfb'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9})
fs=sorted(glob.glob('../videos/fotogramas_patada_03/e_*.png'))[:7]
labs=['Orden\n0.00 s','Aproximación\n0.55 s','Carga\n1.40 s','Swing\n1.74 s','Contacto\n1.90 s','Seguimiento\n2.31 s','Recuperación\n2.70 s']
fig=plt.figure(figsize=(10,3.6),facecolor=SURF)
gs=fig.add_gridspec(2,7,height_ratios=[2.2,0.9],hspace=0.08,wspace=0.05)
for j,(f,l) in enumerate(zip(fs,labs)):
    ax=fig.add_subplot(gs[0,j]); im=Image.open(f).convert('RGB').crop((405,100,585,260))
    ax.imshow(im); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_color('#0b0b0b' if 'Contacto' in l else GRID); s.set_linewidth(1.6 if 'Contacto' in l else 0.8)
    ax.set_title(l,fontsize=8.5,color=INK)
ax=fig.add_subplot(gs[1,:]); ax.set_facecolor(SURF)
fases=[(0,1.05,'Aproximación'),(1.05,1.45,'Carga'),(1.45,1.73,'Swing'),(1.73,2.2,'Seguimiento'),(2.2,4.0,'Recuperación')]
cols=['#cfe0f5','#9fc2ec','#5d9ae0','#9fc2ec','#cfe0f5']
for (a,b,l),c in zip(fases,cols):
    ax.barh(0,b-a,left=a,height=0.55,color=c,edgecolor=SURF,linewidth=2)
    ax.text((a+b)/2,0,l,ha='center',va='center',fontsize=8 if b-a<0.45 else 9,color=INK)
ax.axvline(1.73,color=INK,lw=1.2,ls=(0,(3,3))); ax.text(1.76,0.42,'contacto ≈ 1.73 s',ha='left',va='bottom',fontsize=8,color=INK)
ax.set_xlim(0,4.1); ax.set_ylim(-0.45,0.75); ax.set_yticks([])
for s in ('top','right','left'): ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color(GRID); ax.tick_params(colors=INK2)
ax.set_xlabel('Tiempo simulado desde la orden en /kick_ball (s) — promedio de patada_02 y patada_03',color=INK2)
fig.suptitle('Diagrama temporal de la patada base',x=0.02,ha='left',color=INK,fontsize=11,fontweight='bold')
fig.text(0.02,0.905,'Arriba: fotogramas del video de patada_03 (tiempo simulado desde la orden). Abajo: duración media de cada etapa.',fontsize=8.5,color=INK2)
fig.savefig('../figuras/diagrama_temporal.png',dpi=150,facecolor=SURF,bbox_inches='tight'); print('ok')
