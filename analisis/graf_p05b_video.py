import subprocess, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from PIL import Image
V='../videos/B1_-_Simulator_2026-10-18_00-55-28.mp4'
F=[(24.0,'Inicio de la publicación'),(28.8,'Espera sin girar'),(30.4,'Golpe con la\npierna izquierda'),(31.8,'El balón sale hacia\nla derecha del robot'),(37.7,'Final: balón a ≈0.95 D')]
fig,ax=plt.subplots(1,5,figsize=(15,3.0))
for a,(v,lab) in zip(ax,F):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(v),'-i',V,'-frames:v','1','-vf','crop=320:200:330:130','/tmp/_f.png'],check=True)
    a.imshow(Image.open('/tmp/_f.png')); a.axis('off'); a.set_title(lab,fontsize=10)
fig.suptitle('power = 0.5, goal_y = 0 (power_05_2): fotogramas del video',fontsize=11)
plt.tight_layout(); plt.savefig('../figuras/power_05_2_video.png',dpi=110,bbox_inches='tight')
