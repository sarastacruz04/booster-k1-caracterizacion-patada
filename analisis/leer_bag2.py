import sys, numpy as np
from pathlib import Path
from rosbags.highlevel import AnyReader
from rosbags.typesys import Stores, get_typestore, get_types_from_msg
ts = get_typestore(Stores.ROS2_HUMBLE)
ts.register(get_types_from_msg("""std_msgs/Header header
float64 x
float64 y
float64 dir
float64 goal_x
float64 goal_y
float64 robot_theta_to_field
float64 power""", 'brain/msg/Kick'))
bag = Path(sys.argv[1])
J, V, T, I, O, K, E, CL = [], [], [], [], [], [], [], []
names=None
with AnyReader([bag], default_typestore=ts) as r:
    for c, t, raw in r.messages():
        m = r.deserialize(raw, c.msgtype); tt=t*1e-9
        if c.topic == '/joint_states':
            names = list(m.name); T.append(tt); J.append(np.array(m.position)); V.append(np.array(m.velocity)); E.append(np.array(m.effort))
        elif c.topic == '/imu/data':
            q=m.orientation; I.append((tt,q.x,q.y,q.z,q.w,m.angular_velocity.x,m.angular_velocity.y,m.angular_velocity.z,m.linear_acceleration.x,m.linear_acceleration.y,m.linear_acceleration.z))
        elif c.topic == '/odom':
            p=m.pose.pose.position; q=m.pose.pose.orientation; v=m.twist.twist.linear
            O.append((tt,p.x,p.y,p.z,q.x,q.y,q.z,q.w,v.x,v.y))
        elif c.topic == '/clock':
            CL.append((tt, m.clock.sec + m.clock.nanosec*1e-9))
        elif c.topic == '/kick_ball':
            K.append((tt, m.x, m.y, m.dir, m.power))
T=np.array(T); np.savez(sys.argv[2], t=T, P=np.array(J), V=np.array(V), names=np.array(names), I=np.array(I), O=np.array(O), K=np.array(K), E=np.array(E), CL=np.array(CL))
print('saved', len(T), len(I), len(O), len(K))
