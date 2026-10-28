import json, math, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow
D=json.load(open('../datos/dataset.json')); R={r[0]:r for r in D['rows']}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.edgecolor':'#bdbcb6','axes.labelcolor':'#52514e','xtick.color':'#52514e','ytick.color':'#52514e'})
BLUE,ORANGE,AQUA,GRAY,INK,MUTED='#2a78d6','#eb6834','#1baf7a','#8a8984','#0b0b0b','#52514e'
# ---------- Fig 11: ball landing map ----------
groups=[
 ('Pierna derecha · power 1.5, goal_y 0 (baseline y dir)',BLUE,'o',['P6','P7','P8','P9','dir_p05_2','dir_n05_1']),
 ('Pierna izquierda · power 0.5',ORANGE,'s',['power_05_2','power_05_1']),
 ('goal_y ≠ 0 · power 1.5 (empujones)',AQUA,'^',['goal_n3_1','goal_n3_2','goal_n05_1']),
]
lab={'P6':'P6','P7':'P7','P8':'P8','P9':'P9','dir_p05_2':'dir +0.5','dir_n05_1':'dir −0.5','power_05_2':'power 0.5','power_05_1':'power 0.5\n(goal_y −0.5)','goal_n3_1':'goal_y −3 (1)','goal_n3_2':'goal_y −3 (2)','goal_n05_1':'goal_y −0.5'}
off={'P6':(6,-12),'P7':(6,4),'P8':(-24,-14),'P9':(8,-4),'dir_p05_2':(-52,-3),'dir_n05_1':(-58,-4),'power_05_2':(8,-4),'power_05_1':(8,-6),'goal_n3_1':(8,-4),'goal_n3_2':(8,-10),'goal_n05_1':(-70,4)}
fig,ax=plt.subplots(figsize=(7.2,6.2))
for rr in [0.5,1,1.5,2,2.5]:
    ax.add_patch(Circle((0,0),rr,fill=False,ec='#e4e3df',lw=0.8,zorder=0))
    ax.text(rr*0.17+0.02,rr*0.985+0.02,'%g D'%rr,fontsize=8,color=GRAY)
ax.axhline(0,color='#e4e3df',lw=0.8,zorder=0); ax.axvline(0,color='#e4e3df',lw=0.8,zorder=0)
for name,col,mk,ids in groups:
    first=True
    for i in ids:
        r=R[i]; d,a=r[19],r[20]
        lx=-d*math.sin(math.radians(a)); fy=d*math.cos(math.radians(a))
        ax.scatter(lx,fy,s=70,c=col,marker=mk,edgecolors='white',linewidths=2,zorder=3,label=name if first else None); first=False
        ax.annotate(lab[i],(lx,fy),xytext=off[i],textcoords='offset points',fontsize=8.5,color=MUTED)
ax.scatter(0,0,s=110,marker='X',c=GRAY,edgecolors='white',linewidths=2,zorder=4,label='Balón sin mover: patada al aire')
ax.annotate('power 6.0 (×2), goal_y +3',(0,0),xytext=(10,-16),textcoords='offset points',fontsize=8.5,color=MUTED)
ax.add_patch(FancyArrow(0,-0.42,0,0.22,width=0.04,head_width=0.14,head_length=0.1,color=INK,zorder=5))
ax.text(0,-0.55,'Robot (mira hacia arriba)',ha='center',fontsize=8.5,color=INK)
ax.set_xlim(-2.6,2.6); ax.set_ylim(-0.75,2.6); ax.set_aspect('equal')
ax.set_xticks([-2,-1,0,1,2]); ax.set_xticklabels(['2 D\nizquierda','1 D','0','1 D','2 D\nderecha'])
ax.set_yticks([0,1,2]); ax.set_yticklabels(['0','1 D','2 D\nal frente'])
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.set_title('Dónde terminó el balón en cada prueba\n(posición final respecto al punto de partida, en diámetros del círculo central)',fontsize=11,color=INK)
ax.legend(loc='upper center',bbox_to_anchor=(0.5,-0.13),ncol=2,frameon=False,fontsize=8.5)
plt.tight_layout(); plt.savefig('../figuras/f3_mapa_balon.png',dpi=150,bbox_inches='tight'); plt.close()
# ---------- Fig 12: small multiples by configuration ----------
cfg=[('power 0.5',['power_05_2']),('Baseline\n(power 1.5)',['patada_02','patada_03','dir_p05_2']),('power 6.0',['power_6_1','power_6_2']),
     ('goal_y −0.5',['goal_n05_1']),('goal_y −3',['goal_n3_1','goal_n3_2']),('goal_y +3',['goal_p3_1'])]
metr=[(16,'Velocidad de extensión de la rodilla\nen el golpe (°/s)  · intensidad'),(15,'Instante del golpe\n(s simulados desde el 1.er mensaje)  · tiempo'),(17,'Inclinación máx. del torso\n(pitch, °)  · estabilidad')]
fig,axs=plt.subplots(1,3,figsize=(12,3.9),sharey=True)
y=np.arange(len(cfg))[::-1]
for ax,(col,title) in zip(axs,metr):
    for yi,(name,ids) in zip(y,cfg):
        vals=[R[i][col] for i in ids if R[i][col] is not None]
        m=np.mean(vals)
        ax.barh(yi,m,height=0.55,color=BLUE,zorder=2)
        if len(vals)>1: ax.scatter(vals,[yi]*len(vals),s=22,c='white',edgecolors=INK,linewidths=1,zorder=3)
        ax.text(max(vals),yi,'   %s'%(('%.0f'%m) if col!=15 else ('%.1f'%m)),va='center',fontsize=8.5,color=MUTED)
    ax.set_title(title,fontsize=9.5,color=INK,loc='left',pad=16)
    ax.grid(axis='x',color='#ecebe7',zorder=0); 
    for s in ['top','right','left']: ax.spines[s].set_visible(False)
    ax.tick_params(axis='y',length=0)
axs[0].set_yticks(y); axs[0].set_yticklabels([c[0] for c in cfg])
axs[0].set_xlim(0,1000); axs[1].set_xlim(0,7); axs[2].set_xlim(0,22)
for ax,col in zip(axs,[16,15,17]):
    b=np.mean([R[i][col] for i in ['patada_02','patada_03','dir_p05_2']])
    ax.axvline(b,color=INK,lw=1,ls=(0,(3,3)),zorder=4)
    ax.text(b,y[0]+0.55,' baseline',fontsize=8,color=INK,va='bottom')
fig.text(0.01,-0.04,'Barra = media de las repeticiones; puntos blancos = pruebas individuales cuando hay más de una. Golpe al aire en power 6.0 y goal_y ±3.',fontsize=8.5,color=MUTED)
plt.tight_layout(); plt.savefig('../figuras/f3_metricas.png',dpi=150,bbox_inches='tight'); plt.close()
print('ok')
