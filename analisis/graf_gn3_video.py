import subprocess, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from PIL import Image
V='../videos/B1_-_Simulator_2026-10-18_00-03-22.mp4'
vt=[26,27.5,28.4,28.8,29.2,30,32,34]; st=[95.94,96.55,96.93,97.10,97.27,97.65,98.56,99.62]
s0=95.52
F=[(26.0,'Empieza a girar\nhacia su derecha'),(28.4,'Se acerca al balón\nmientras gira'),(29.6,'Empuja el balón\nmientras gira'),(31.9,'Swing de la pierna\nderecha: patada al aire'),(34.0,'Final: balón a 0.26 D')]
fig,ax=plt.subplots(1,5,figsize=(15,3.4))
for a,(v,lab) in zip(ax,F):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(v),'-i',V,'-frames:v','1','-vf','crop=200:140:480:195','/tmp/_f.png'],check=True)
    a.imshow(Image.open('/tmp/_f.png')); a.axis('off')
    s=np.interp(v,vt,st)
    a.set_title('t = %.1f s (sim)\n%s'%(s-s0,lab),fontsize=10)
fig.suptitle('goal_y = −3.0 m (goal_n3_2): fotogramas del video. t = tiempo simulado desde el primer mensaje en /kick_ball',fontsize=11)
plt.tight_layout(); plt.savefig('../figuras/goal_n3_2_video.png',dpi=110,bbox_inches='tight')
