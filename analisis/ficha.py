import numpy as np
from scipy.signal import find_peaks
J=['Right_Hip_Pitch','Right_Hip_Roll','Right_Hip_Yaw','Right_Knee_Pitch','Right_Ankle_Pitch','Right_Ankle_Roll',
   'Left_Hip_Pitch','Left_Hip_Roll','Left_Hip_Yaw','Left_Knee_Pitch','Left_Ankle_Pitch','Left_Ankle_Roll',
   'ARight_Shoulder_Pitch','Right_Shoulder_Roll','ALeft_Shoulder_Pitch','Left_Shoulder_Roll','Head_Pitch','AAHead_Yaw']
F=['Aproximación','Carga','Swing','Seguimiento','Recuperación']
ROM=[]; VEL=[]; DUR=[]
for name in ['patada_02','patada_03']:
    d=np.load(f'../datos/procesados/{name}.npz'); tc=d['K'][0,0]; CL=d['CL']; ct=CL[:,0]-tc; cs=CL[:,1]-np.interp(0,CL[:,0]-tc,CL[:,1])
    t=np.interp(d['t']-tc,ct,cs)   # sim time rel
    P=np.degrees(d['P']); V=np.degrees(d['V']); n=list(d['names'])
    m=(t>-0.2)&(t<6); tt=t[m]
    rk=P[m,n.index('Right_Knee_Pitch')]; lk=P[m,n.index('Left_Knee_Pitch')]
    pkL,_=find_peaks(lk,prominence=8); c=tt[pkL[np.argmax(lk[pkL])]]
    k=tt[np.argmin(V[m,n.index('Right_Knee_Pitch')])]
    legs=[i for i,x in enumerate(n) if any(s in x for s in ['Hip','Knee','Ankle'])]
    act=np.convolve(np.abs(V[:,legs]).sum(1),np.ones(40)/40,'same')
    e=t[np.where((t>k)&(t<k+6)&(act<15))[0][0]]
    b=[0,c-0.19,k-0.28,k,k+0.47,e]
    DUR.append(np.diff(b))
    rom=np.zeros((len(J),5)); vel=np.zeros((len(J),5))
    for f in range(5):
        mm=(t>=b[f])&(t<b[f+1])
        for i,j in enumerate(J):
            x=P[mm,n.index(j)]; rom[i,f]=x.max()-x.min(); vel[i,f]=np.abs(V[mm,n.index(j)]).max()
    ROM.append(rom); VEL.append(vel)
    print(name,'bounds',np.round(b,2))
ROM=np.mean(ROM,0); VEL=np.mean(VEL,0); DUR=np.mean(DUR,0)
np.savez('../datos/procesados/ficha.npz',ROM=ROM,VEL=VEL,J=np.array(J),F=np.array(F),DUR=DUR)
print('dur',np.round(DUR,2))
for i,j in enumerate(J): print(f'{j:22s}', ' '.join(f'{ROM[i,f]:5.1f}/{VEL[i,f]:4.0f}' for f in range(5)))
