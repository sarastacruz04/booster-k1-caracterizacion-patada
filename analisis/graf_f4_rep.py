import math, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.edgecolor':'#bdbcb6','xtick.color':'#52514e','ytick.color':'#52514e'})
BLUE,ORANGE,AQUA,GRAY,INK,MUTED='#2a78d6','#eb6834','#1baf7a','#8a8984','#0b0b0b','#52514e'
A=[('P6',1.38,32),('P7',2.28,40),('P8',1.34,47),('P9',1.28,44),('dir +0.5',2.34,43.5),('dir −0.5',2.35,33.6)]
B=[('power_05_2',0.95,-40),('B_2',0.0,0),('B_3',0.86,32)]
C=[('goal_n05_1',0.38,12),('C_2',2.31,-45),('C_3',1.10,5)]
off={'P6':(6,-12),'P7':(6,4),'P8':(-24,-14),'P9':(8,-4),'dir +0.5':(-52,-3),'dir −0.5':(-58,-4),'power_05_2':(8,-4),'B_2':(10,10),'B_3':(8,-12),'goal_n05_1':(8,-2),'C_2':(-30,8),'C_3':(8,-4)}
fig,ax=plt.subplots(figsize=(7.2,6.0))
for rr in [0.5,1,1.5,2,2.5]:
    ax.add_patch(Circle((0,0),rr,fill=False,ec='#e4e3df',lw=0.8,zorder=0)); ax.text(rr*0.17+0.02,rr*0.985+0.02,'%g D'%rr,fontsize=8,color=GRAY)
ax.axhline(0,color='#e4e3df',lw=0.8,zorder=0); ax.axvline(0,color='#e4e3df',lw=0.8,zorder=0)
for name,col,mk,pts in [('A · power 1.5, goal_y 0 (10 pruebas; 6 con captura)',BLUE,'o',A),('B · power 0.5, goal_y 0 (3 pruebas)',ORANGE,'s',B),('C · power 1.5, goal_y −0.5 (3 pruebas)',AQUA,'^',C)]:
    first=True
    for lab,d,a in pts:
        x=-d*math.sin(math.radians(a)); y=d*math.cos(math.radians(a))
        ax.scatter(x,y,s=75,c=col,marker=mk,edgecolors='white',linewidths=2,zorder=3,label=name if first else None); first=False
        ax.annotate(lab,(x,y),xytext=off[lab],textcoords='offset points',fontsize=8.5,color=MUTED)
ax.add_patch(FancyArrow(0,-0.42,0,0.22,width=0.04,head_width=0.14,head_length=0.1,color=INK,zorder=5))
ax.text(0,-0.55,'Robot (mira hacia arriba)',ha='center',fontsize=8.5,color=INK)
ax.set_xlim(-2.6,2.6); ax.set_ylim(-0.75,2.6); ax.set_aspect('equal')
ax.set_xticks([-2,-1,0,1,2]); ax.set_xticklabels(['2 D\nizquierda','1 D','0','1 D','2 D\nderecha']); ax.set_yticks([0,1,2]); ax.set_yticklabels(['0','1 D','2 D\nal frente'])
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.set_title('Repetibilidad de los comportamientos A, B y C\n(posición final del balón, en diámetros del círculo central)',fontsize=11,color=INK)
ax.legend(loc='upper center',bbox_to_anchor=(0.5,-0.13),ncol=1,frameon=False,fontsize=8.5)
plt.tight_layout(); plt.savefig('../figuras/f4_repetibilidad.png',dpi=150,bbox_inches='tight')
