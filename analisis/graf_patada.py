import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
d=np.load('../datos/procesados/patada_01.npz'); T0=d['t'][0]; K=d['K']; tc=K[0,0]
t=d['t']-tc; P=np.degrees(d['P']); n=list(d['names']); I=d['I']; ti=I[:,0]-tc
x,y,z,w=I[:,1],I[:,2],I[:,3],I[:,4]
roll=np.degrees(np.arctan2(2*(w*x+y*z),1-2*(x*x+y*y))); pitch=np.degrees(np.arcsin(np.clip(2*(w*y-z*x),-1,1)))
yaw=np.degrees(np.unwrap(np.arctan2(2*(w*z+x*y),1-2*(y*y+z*z)))); yaw=yaw-yaw[(ti>-3)&(ti<0)].mean()
C=['#2a78d6','#eb6834','#1baf7a']; INK,INK2,GRID,SURF='#0b0b0b','#52514e','#e4e3df','#fcfcfb'
fases=[(0,1.8,'Aproximación'),(1.8,2.6,'Carga'),(2.6,3.15,'Swing'),(3.15,4.1,'Seguimiento'),(4.1,7.8,'Recuperación')]
bands=['#efeeea','#dddcd6']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9})
fig,axall=plt.subplots(4,1,figsize=(9,8.2),sharex=True,facecolor=SURF,gridspec_kw={'height_ratios':[0.35,1,1,1]})
strip=axall[0]; axs=axall[1:]
L=[('Pierna derecha (pierna que patea), °',[('Right_Hip_Pitch','Cadera pitch'),('Right_Knee_Pitch','Rodilla pitch'),('Right_Ankle_Pitch','Tobillo pitch')]),
   ('Pierna izquierda (apoyo durante el golpe), °',[('Left_Hip_Pitch','Cadera pitch'),('Left_Knee_Pitch','Rodilla pitch'),('Left_Ankle_Pitch','Tobillo pitch')])]
m=(t>-0.7)&(t<8.3); mi=(ti>-0.7)&(ti<8.3)
for ax,(tt,ser) in zip(axs[:2],L):
    for k,(j,lab) in enumerate(ser): ax.plot(t[m],P[m,n.index(j)],color=C[k],lw=2,label=lab)
    ax.set_title(tt,loc='left',color=INK,fontsize=10,fontweight='bold')
ax=axs[2]
ax.plot(ti[mi],pitch[mi],color=C[0],lw=2,label='Pitch (adelante +)')
ax.plot(ti[mi],roll[mi],color=C[1],lw=2,label='Roll (lateral)')
ax.plot(ti[mi],yaw[mi],color=C[2],lw=2,label='Giro (yaw) respecto\nal inicio')
ax.set_title('Torso (IMU), °',loc='left',color=INK,fontsize=10,fontweight='bold')
ax.set_xlabel('Tiempo desde la primera orden en /kick_ball (s, reloj)',color=INK2)
for ax in axs:
    for k,(a,b,lab) in enumerate(fases): ax.axvspan(a,b,color=bands[k%2],lw=0,zorder=0)
    ax.axvline(0,color=INK2,lw=1,ls=(0,(3,3)),zorder=1); ax.axvline(3.15,color=INK,lw=1.2,ls=(0,(3,3)),zorder=1)
    ax.set_facecolor(SURF); ax.grid(axis='y',color=GRID,lw=0.8); ax.set_axisbelow(True)
    for s in ('top','right'): ax.spines[s].set_visible(False)
    for s in ('left','bottom'): ax.spines[s].set_color(GRID)
    ax.tick_params(colors=INK2); ax.set_xlim(-0.7,8.3)
    ax.legend(loc='upper left',bbox_to_anchor=(1.01,1),frameon=False,labelcolor=INK)
for k,(a,b,lab) in enumerate(fases):
    strip.axvspan(a,b,color=bands[k%2],lw=0)
    strip.text(((a+b)/2+0.08) if lab=='Seguimiento' else (a+b)/2,0.5,lab,ha='center',va='center',fontsize=8.5 if b-a>0.7 else 7.5,color=INK,rotation=0 if b-a>0.7 else 0)
strip.axvline(0,color=INK2,lw=1,ls=(0,(3,3))); strip.axvline(3.15,color=INK,lw=1.2,ls=(0,(3,3)))
strip.text(0,1.05,'orden',ha='center',va='bottom',fontsize=8,color=INK2,transform=strip.get_xaxis_transform())
strip.text(3.15,1.05,'contacto',ha='center',va='bottom',fontsize=8,color=INK,transform=strip.get_xaxis_transform())
strip.set_yticks([]); strip.set_facecolor(SURF)
for sp in strip.spines.values(): sp.set_visible(False)
strip.tick_params(bottom=False)
fig.suptitle('Patada base (patada_01): articulaciones y torso a lo largo del tiempo',x=0.02,ha='left',color=INK,fontsize=11,fontweight='bold')
fig.tight_layout(rect=(0,0,1,0.965)); fig.savefig('../figuras/patada01_timeline.png',dpi=150,facecolor=SURF); print('ok')
