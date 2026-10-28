import numpy as np, math, json
def yaw(q): x,y,z,w=q; return math.degrees(math.atan2(2*(w*z+x*y),1-2*(y*y+z*z)))
def pitch(q): x,y,z,w=q; return math.degrees(math.asin(max(-1,min(1,2*(w*y-z*x)))))
def roll(q): x,y,z,w=q; return math.degrees(math.atan2(2*(w*x+y*z),1-2*(x*x+y*y)))
names_=['patada_01','patada_02','patada_03','dir_p05_1','dir_p05_2','dir_n05_1','goal_n3_1','goal_n3_2','goal_p3_1','goal_n05_1','power_6_1','power_05_1','power_05_2','power_6_2']
out={}
for n in names_:
    d=np.load('../datos/procesados/'+n+'.npz',allow_pickle=True); t,P,V,I,K,CL=d['t'],d['P'],d['V'],d['I'],d['K'],d['CL']; nm=list(d['names'])
    r={'n_msgs':int(len(K))}
    if len(CL)>10:
        sim=lambda tt: np.interp(tt, CL[:,0], CL[:,1]); r['reloj']='sim'
    else:
        sim=lambda tt: tt; r['reloj']='pared'
    if len(K)==0: out[n]=r; print(n,r); continue
    s0=sim(K[0,0]); r['pub']=round(float(sim(K[-1,0])-s0),2)
    if K.shape[1]>=8: r['msg']=[float(v) for v in K[0,1:]]
    else: r['msg']=[float(v) for v in K[0,1:]]
    tj=sim(t)-s0; ti=sim(I[:,0])-s0
    win=(tj>0)&(tj<r['pub']+2.5)
    best=None
    for leg in ['Right','Left']:
        k=nm.index(leg+'_Knee_Pitch'); v=np.degrees(V[:,k]); vv=np.where(win,v,1e9); i=np.argmin(vv)
        if best is None or v[i]<best[1]: best=(leg,v[i],tj[i])
    r['pierna']='Derecha' if best[0]=='Right' else 'Izquierda'; r['v_rodilla']=round(float(-best[1])); r['t_swing']=round(float(best[2]),2)
    y=np.degrees(np.unwrap(np.radians([yaw(q[1:5]) for q in I]))); y=y-y[np.argmin(abs(ti))]
    r['giro_swing']=round(float(y[np.argmin(abs(ti-best[2]))])); r['giro_final']=round(float(y[-1]))
    m=ti>0
    pt=np.array([pitch(q[1:5]) for q in I]); rl=np.array([roll(q[1:5]) for q in I])
    r['pitch_max']=round(float(abs(pt[m]).max()),1); r['roll_max']=round(float(abs(rl[m]).max()),1)
    r['dur_grab']=round(float(ti[-1]),1)
    out[n]=r; print(n,r)
json.dump(out,open('../datos/metricas.json','w'),indent=1)
