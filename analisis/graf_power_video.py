import subprocess, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from PIL import Image
U='../videos/'
rows=[
 ('power = 6.0, goal_y = 0 (power_6_1)', U+'B1_-_Simulator_2026-10-18_00-40-25.mp4', [28,32,36],[87.25,89.58,91.34], 88.96, 'crop=300:200:350:120',
  [(31.0,'Inicio'),(32.6,'Gira a su derecha'),(33.9,'Swing fuerte de la\npierna izquierda, al aire'),(35.2,'Se aleja del balón'),(37.4,'Final: balón sin mover')]),
 ('power = 0.5, goal_y = −0.5 (power_05_1)', U+'B1_-_Simulator_2026-10-18_00-45-01.mp4', [28,32,36],[83.90,85.64,87.48], 83.36, 'crop=300:200:350:120',
  [(27.0,'Inicio'),(30.4,'Gira a su derecha\ny se acerca'),(32.4,'Contacto'),(33.4,'El balón sale hacia\nla derecha del robot'),(34.2,'Balón lejos (≈2.1 D al final)')]),
]
fig,ax=plt.subplots(2,5,figsize=(15,6.4))
for r,(title,V,vt,st,s0,crop,F) in enumerate(rows):
    for a,(v,lab) in zip(ax[r],F):
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(v),'-i',V,'-frames:v','1','-vf',crop,'/tmp/_f.png'],check=True)
        a.imshow(Image.open('/tmp/_f.png')); a.axis('off')
        a.set_title('t = %.1f s\n%s'%(np.interp(v,vt,st)-s0,lab),fontsize=9.5)
    ax[r][0].text(-0.08,0.5,title,transform=ax[r][0].transAxes,rotation=90,va='center',ha='right',fontsize=10,fontweight='bold')
fig.suptitle('Pilotos de power: fotogramas del video (t = tiempo simulado desde el primer mensaje en /kick_ball)',fontsize=11)
plt.tight_layout(); plt.savefig('../figuras/power_video.png',dpi=110,bbox_inches='tight')
