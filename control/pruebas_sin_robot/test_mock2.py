import math, time, threading, random
src=open('../control_patada.py').read().replace('with open("/root/lector_control.py", "w") as f:\n    f.write(LECTOR)','')
ns={}; exec(src, ns)
cmd={'v':(0,0,0)}
class C:
    def Move(self,vx,vy,w): cmd['v']=(vx,vy,w)
    def VisualKick(self,*a): pass
ns['client']=C(); ns['VisualKickVersion']=type('V',(),{'kV1':1})
st=ns['estado']; st.update(t=0.0,x=1.0,y=2.0,yaw=math.radians(170))
lag=[]
def sim():
    dt=0.01; buf=[(0,0,0)]*15   # 0.15 s actuation lag -> overshoot
    while True:
        buf.append(cmd['v']); vx,vy,w=buf.pop(0)
        if math.hypot(vx,vy)<0.15: vx=vy=0
        k=3.0; c,s=math.cos(st['yaw']),math.sin(st['yaw'])
        st['x']+=k*dt*(c*vx-s*vy); st['y']+=k*dt*(s*vx+c*vy); st['yaw']+=k*dt*1.9*w; st['t']+=k*dt*0.5
        time.sleep(dt)
threading.Thread(target=sim,daemon=True).start()
for g in [40,-40]:
    st.update(x=1.0,y=2.0,yaw=math.radians(170)); time.sleep(0.3)
    print(ns['orbitar'](g))
