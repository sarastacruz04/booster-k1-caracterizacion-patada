import sys, numpy as np
from pathlib import Path
from rosbags.highlevel import AnyReader
from rosbags.typesys import Stores, get_typestore
ts = get_typestore(Stores.ROS2_HUMBLE)
bag = Path(sys.argv[1])
J, I, O = [], [], []
names = None
with AnyReader([bag], default_typestore=ts) as r:
    for c, t, raw in r.messages():
        m = r.deserialize(raw, c.msgtype)
        st = m.header.stamp.sec + m.header.stamp.nanosec*1e-9
        if c.topic == '/joint_states':
            names = list(m.name)
            J.append((t*1e-9, st, np.array(m.position), np.array(m.velocity) if len(m.velocity) else None, np.array(m.effort) if len(m.effort) else None))
        elif c.topic == '/imu/data':
            q = m.orientation
            I.append((t*1e-9, st, q.x, q.y, q.z, q.w, m.angular_velocity.x, m.angular_velocity.y, m.angular_velocity.z, m.linear_acceleration.x, m.linear_acceleration.y, m.linear_acceleration.z))
        elif c.topic == '/odom':
            p = m.pose.pose.position; q = m.pose.pose.orientation
            O.append((t*1e-9, st, p.x, p.y, p.z, q.x, q.y, q.z, q.w))
print('joints', len(J), 'names', names)
print('vel?', J[0][3] is not None, 'effort?', J[0][4] is not None, 'npos', len(J[0][2]))
t = np.array([j[0] for j in J]); s = np.array([j[1] for j in J])
print('wall span', t[-1]-t[0], 'stamp span', s[-1]-s[0], 'stamp first', s[0])
P = np.array([j[2] for j in J])
for n, a, b, sd in zip(names, P.min(0), P.max(0), P.std(0)):
    print(f'{n:22s} min {a:+.3f} max {b:+.3f} std {sd:.4f}')
I = np.array(I); O = np.array(O)
def rpy(x,y,z,w):
    roll=np.arctan2(2*(w*x+y*z),1-2*(x*x+y*y)); pitch=np.arcsin(np.clip(2*(w*y-z*x),-1,1)); yaw=np.arctan2(2*(w*z+x*y),1-2*(y*y+z*z)); return roll,pitch,yaw
r,p,y = rpy(I[:,2],I[:,3],I[:,4],I[:,5])
print('imu stamp span', I[-1,1]-I[0,1], 'roll', r.mean(), r.std(), 'pitch', p.mean(), p.std(), 'yaw', y.mean(), y.std())
print('acc mean', I[:,9:12].mean(0))
print('odom first', O[0,2:5], 'last', O[-1,2:5], 'stamp span', O[-1,1]-O[0,1])
np.savez(sys.argv[2], t=t, s=s, P=P, names=np.array(names), V=np.array([j[3] for j in J]) if J[0][3] is not None else np.array([]), I=I, O=O)
