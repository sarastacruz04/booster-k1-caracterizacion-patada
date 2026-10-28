import numpy as np, math, sys
def yaw(q): x,y,z,w=q; return math.degrees(math.atan2(2*(w*z+x*y),1-2*(y*y+z*z)))
def pitch(q):
    x,y,z,w=q; return math.degrees(math.asin(max(-1,min(1,2*(w*y-z*x)))))
for n in sys.argv[1:]:
    d=np.load('../datos/procesados/'+n+'.npz',allow_pickle=True); I,K,CL,t,P,V=d['I'],d['K'],d['CL'],d['t'],d['P'],d['V']; names=list(d['names'])
    sim=lambda tt: np.interp(tt, CL[:,0], CL[:,1])
    print('==',n,'clock %.2f-%.2f'%(CL[0,1],CL[-1,1]),'kick sim %.2f-%.2f'%(sim(K[0,0]),sim(K[-1,0])), 'n',len(K))
    dt=np.diff(t); print(' max gap joint %.3f s at sim %.2f'%(dt.max(), sim(t[np.argmax(dt)])))
    print(' clock jumps back:', np.sum(np.diff(CL[:,1])<-0.5))
    s0=sim(K[0,0])
    y=np.degrees(np.unwrap(np.radians([yaw(r[1:5]) for r in I]))); y-=y[np.argmin(abs(sim(I[:,0])-s0))]
    pt=np.array([pitch(r[1:5]) for r in I])
    ts=sim(I[:,0])-s0
    print(' yaw', ' '.join('%.1f:%.0f'%(T,y[np.argmin(abs(ts-T))]) for T in np.arange(0,ts[-1],0.5)))
    m=ts>0; print(' pitch max %.1f at %.2f'%(pt[m].max(), ts[m][np.argmax(pt[m])]))
    tj=sim(t)-s0
    for j in ['Right_Knee_Pitch','Left_Knee_Pitch']:
        k=names.index(j); mm=(tj>0)
        v=np.degrees(V[:,k]); 
        # list strong extension events < -400 deg/s
        ev=np.where(mm&(v<-400))[0]
        groups=[]; 
        for i in ev:
            if not groups or tj[i]-tj[groups[-1][-1]]>0.3: groups.append([i])
            else: groups[-1].append(i)
        print(' %s extension events:'%j, ['%.2fs %.0f'%(tj[g[np.argmin(v[g])]], v[g].min()) for g in groups])
