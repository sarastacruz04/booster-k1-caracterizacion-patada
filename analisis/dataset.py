import json, csv, math
M=json.load(open('../datos/metricas.json'))
# Manual: contact swing per test (leg, t, knee ext vel), ball outcome (dist D, angle +izq), validity, notes
rows=[
 # id, fecha, fase, grabacion, serie, version, x,y,dir,goal_x,goal_y,power, pub, giro, pierna, t_swing, v_rod, pitch, golpea, dist, ang, validez, notas
 ['P4','15/10','F1','—','Baseline (preparación no estándar)','V1',0.6,0,0,4.5,0,1.5,None,None,'Izquierda',None,None,None,'Sí',None,None,'Válida (cualitativa)','Sin reinicio de escena; balón al frente-izquierda; ~5 s sim hasta el contacto'],
 ['P5','15/10','F1','—','Baseline','V1',0.6,0,0,4.5,0,1.5,None,None,'Derecha',6.0,None,None,'Sí',None,None,'Válida (sin captura cenital)','Frente-izquierda; tiempo medido con Simulation time'],
 ['P6','15/10','F1','—','Baseline','V1',0.6,0,0,4.5,0,1.5,None,None,'Derecha',6.0,None,None,'Sí',1.38,32,'Válida',''],
 ['P7','15/10','F1','—','Baseline','V1',0.6,0,0,4.5,0,1.5,None,None,'Derecha',3.0,None,None,'Sí',2.28,40,'Válida',''],
 ['P8','15/10','F1','—','Baseline','V1',0.6,0,0,4.5,0,1.5,None,None,'Derecha',2.0,None,None,'Sí',1.34,47,'Válida',''],
 ['P9','15/10','F1','—','Baseline','V1',0.6,0,0,4.5,0,1.5,None,None,'Derecha',2.0,None,None,'Sí',1.28,44,'Válida',''],
 ['patada_01','17/10','F2','patada_01','Baseline (datos del cuerpo)','V1',0.6,0,0,4.5,0,1.5,'patada_01',None,'Derecha',3.18,422,None,'Sí',None,None,'Válida (sin /clock: tiempos de reloj)','Sin captura cenital'],
 ['patada_02','17/10','F2','patada_02','Baseline (datos del cuerpo)','V1',0.6,0,0,4.5,0,1.5,'patada_02',None,'Derecha',1.56,407,None,'Sí',None,None,'Válida','Sin captura cenital'],
 ['patada_03','17/10','F2','patada_03','Baseline (datos del cuerpo + video)','V1',0.6,0,0,4.5,0,1.5,'patada_03',None,'Derecha',1.90,427,None,'Sí',None,None,'Válida','Video sincronizado con /clock'],
 ['dir_p05_1','17/10','F3','dir_p05_1','dir','V1',0.6,0,0.5,4.5,0,1.5,None,None,'Derecha',None,None,None,'Sí',None,None,'Descartada','Publicación 21.6 s, dos patadas, reinicio de escena; sin capturas'],
 ['dir_p05_2','17/10','F3','dir_p05_2','dir','V1',0.6,0,0.5,4.5,0,1.5,'dir_p05_2',None,'Derecha',1.52,441,None,'Sí',2.34,43.5,'Válida',''],
 ['dir_n05_1','17/10','F3','dir_n05_1','dir','V1',0.6,0,-0.5,4.5,0,1.5,None,None,'Derecha',None,None,None,'Sí',2.35,33.6,'Válida para dirección','Grabación terminó antes de la patada; balón llegó a la valla'],
 ['goal_n3_1','17/10','F3','goal_n3_1','goal_y','V1',0.6,0,0,4.5,-3,1.5,'goal_n3_1',None,'Derecha',2.95,625,None,'No (empujón)',0.71,-57,'Válida','Sin video'],
 ['goal_n3_2','18/10','F3','goal_n3_2','goal_y','V1',0.6,0,0,4.5,-3,1.5,'goal_n3_2',None,'Derecha',2.99,766,None,'No (empujón; swing al aire)',0.26,-60,'Válida (grabación recuperada)','Video'],
 ['goal_p3_1','18/10','F3','goal_p3_1','goal_y','V1',0.6,0,0,4.5,3,1.5,'goal_p3_1',None,'Derecha',6.05,687,None,'No (al aire)',0.0,None,'Válida (grabación recuperada)','Video; ~1.65 vueltas'],
 ['goal_n05_1','18/10','F3','goal_n05_1','goal_y','V1',0.6,0,0,4.5,-0.5,1.5,'goal_n05_1',None,'Derecha + izquierda',2.73,503,None,'Débil (empujón)',0.38,12,'Válida','Video; segundo swing izquierdo 600°/s a 3.27 s'],
 ['power_6_1','18/10','F3','power_6_1','power','V1',0.6,0,0,4.5,0,6.0,'power_6_1',None,'Izquierda',1.74,874,None,'No (al aire)',0.0,None,'Válida','Video'],
 ['power_05_1','18/10','F3','power_05_1','power + goal_y (error)','V1',0.6,0,0,4.5,-0.5,0.5,'power_05_1',None,'Izquierda',2.40,330,None,'Sí',2.1,-44,'Válida (2 parámetros cambiados)','Video; comparar con goal_n05_1'],
 ['power_05_2','18/10','F3','power_05_2','power','V1',0.6,0,0,4.5,0,0.5,'power_05_2',None,'Izquierda',3.31,323,None,'Sí',0.95,-40,'Válida','Video'],
 ['power_6_2','18/10','F3','power_6_2','power','V1',0.6,0,0,4.5,0,6.0,'power_6_2',None,'Izquierda',1.71,856,None,'No (al aire)',0.0,None,'Válida','Video; repetición de power_6_1'],
]
H=['ID','Fecha','Fase','Grabación','Serie / parámetro variado','Versión','x (m)','y (m)','dir (rad)','goal_x (m)','goal_y (m)','power','Duración publicación (s sim)','Giro antes del golpe (°, + izq.)','Pierna de golpeo','Instante del golpe (s sim desde 1er mensaje)','Vel. máx. extensión rodilla (°/s)','Pitch máx. torso (°)','¿Golpea el balón?','Distancia del balón (D)','Dirección del balón (°, + izq. del frente inicial)','Validez','Notas']
out=[]
for r in rows:
    r=list(r); g=r[12]
    pub=giro=pitch=None
    if g and g in M and 'pub' in M[g]:
        m=M[g]; pub=m['pub']; giro=m['giro_swing']; pitch=m['pitch_max']
    # replace col 12 (bag key) with pub
    r[12]=pub; r[13]=giro; r[17]=pitch
    out.append(r)
# manual overrides: goal_n3_1 giro at swing 2.95 -> -177 measured before; goal_p3_1 ~589
with open('../datos/dataset_D03.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f,delimiter=';'); w.writerow(H)
    for r in out: w.writerow(['' if v is None else (str(v).replace('.',',') if isinstance(v,float) else v) for v in r])
json.dump({'H':H,'rows':out},open('../datos/dataset.json','w'),ensure_ascii=False,indent=0)
for r in out: print(r[0],r[12],r[13],r[14],r[15],r[16],r[17],r[19],r[20])

# recompute giro at manual swing time
import numpy as np
def yaw(q): x,y,z,w=q; return math.degrees(math.atan2(2*(w*z+x*y),1-2*(y*y+z*z)))
for r in out:
    g=r[3]
    if r[12] is None or r[15] is None: continue
    d=np.load('../datos/procesados/'+g+'.npz',allow_pickle=True); I,K,CL=d['I'],d['K'],d['CL']
    sim=(lambda tt: np.interp(tt, CL[:,0], CL[:,1])) if len(CL)>10 else (lambda tt: tt)
    s0=sim(K[0,0]); ti=sim(I[:,0])-s0
    y=np.degrees(np.unwrap(np.radians([yaw(q[1:5]) for q in I]))); y=y-y[np.argmin(abs(ti))]
    r[13]=int(round(y[np.argmin(abs(ti-r[15]))]))
with open('../datos/dataset_D03.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f,delimiter=';'); w.writerow(H)
    for r in out: w.writerow(['' if v is None else (str(v).replace('.',',') if isinstance(v,float) else v) for v in r])
json.dump({'H':H,'rows':out},open('../datos/dataset.json','w'),ensure_ascii=False,indent=0)
print('giros:',[(r[0],r[13]) for r in out if r[13] is not None])
