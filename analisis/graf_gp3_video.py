import subprocess, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from PIL import Image
V='../videos/B1_-_Simulator_2026-10-18_00-15-35.mp4'
vt=[22,25,28,31,34,37,40,44]; st=[61.04,63.34,64.62,65.95,67.26,68.55,69.76,71.98]
s0=63.57
F=[(25.6,'Empieza a girar\nhacia su izquierda'),(29.2,'≈ media vuelta;\nel balón no se mueve'),(33.0,'≈ una vuelta completa'),(37.4,'Último mensaje:\n≈ 1.5 vueltas'),(39.7,'Swing de la pierna\nderecha: patada al aire'),(42.0,'Final: balón en\nel punto central')]
fig,ax=plt.subplots(1,6,figsize=(16,3.2))
for a,(v,lab) in zip(ax,F):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(v),'-i',V,'-frames:v','1','-vf','crop=200:140:470:215','/tmp/_f.png'],check=True)
    a.imshow(Image.open('/tmp/_f.png')); a.axis('off')
    s=np.interp(v,vt,st)
    a.set_title('t = %.1f s (sim)\n%s'%(s-s0,lab),fontsize=10)
fig.suptitle('goal_y = +3.0 m (goal_p3_1): fotogramas del video. t = tiempo simulado desde el primer mensaje en /kick_ball',fontsize=11)
plt.tight_layout(); plt.savefig('../figuras/goal_p3_1_video.png',dpi=110,bbox_inches='tight')
