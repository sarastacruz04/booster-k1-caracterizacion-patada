import math, time, threading, types
src=open('../control_patada.py').read()
src=src.replace('with open("/root/lector_control.py", "w") as f:\n    f.write(LECTOR)','')
ns={}
exec(src, ns)
cmd={'v':(0,0,0)}
class C:
    def Move(self,vx,vy,w): cmd['v']=(vx,vy,w)
ns['client']=C()
st=ns['estado']; st.update(t=0.0,x=1.0,y=2.0,yaw=math.radians(170))
def sim():
    dt=0.01
    while True:
        vx,vy,w=cmd['v']
        # deadband 0.15 m/s on linear speed, yaw gain 1.9, speed 3x for test
        sp=math.hypot(vx,vy)
        if sp<0.15: vx=vy=0
        k=3.0
        c,s=math.cos(st['yaw']),math.sin(st['yaw'])
        st['x']+=k*dt*(c*vx-s*vy); st['y']+=k*dt*(s*vx+c*vy); st['yaw']+=k*dt*1.9*w; st['t']+=k*dt*0.5
        time.sleep(dt)
threading.Thread(target=sim,daemon=True).start()
for g in [40,-40]:
    st.update(x=1.0,y=2.0,yaw=math.radians(170))
    x0,y0,yaw0=1.0,2.0,math.radians(170); bx,by=x0+0.45*math.cos(yaw0),y0+0.45*math.sin(yaw0)
    ns['orbitar'](g)
    # ball relative to robot
    dx,dy=bx-st['x'],by-st['y']; c,s=math.cos(st['yaw']),math.sin(st['yaw'])
    print('ball in robot frame: x %.3f y %.3f'%(c*dx+s*dy,-s*dx+c*dy))
