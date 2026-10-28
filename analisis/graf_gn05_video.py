import subprocess, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from PIL import Image
V='../videos/B1_-_Simulator_2026-10-18_00-30-50.mp4'
vt=[34,38,42,46,50,54]; st=[84.63,86.33,88.86,90.59,92.36,94.44]
s0=88.91
F=[(42.4,'Inicio: robot frente\nal balón'),(44.4,'Gira ~40° a su derecha\ny se acerca'),(46.0,'Toca el balón:\nlo empuja'),(48.4,'Swing pierna derecha\n(golpe débil)'),(50.0,'Swing pierna izquierda'),(52.6,'Final: balón a 0.38 D,\n~12° a la izquierda')]
fig,ax=plt.subplots(1,6,figsize=(16,3.2))
for a,(v,lab) in zip(ax,F):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(v),'-i',V,'-frames:v','1','-vf','crop=200:140:413:198','/tmp/_f.png'],check=True)
    a.imshow(Image.open('/tmp/_f.png')); a.axis('off')
    s=np.interp(v,vt,st)
    a.set_title('t = %.1f s (sim)\n%s'%(s-s0,lab),fontsize=10)
fig.suptitle('goal_y = −0.5 m (goal_n05_1): fotogramas del video. t = tiempo simulado desde el primer mensaje en /kick_ball',fontsize=11)
plt.tight_layout(); plt.savefig('../figuras/goal_n05_1_video.png',dpi=110,bbox_inches='tight')
