import sys, sqlite3, numpy as np
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
con=sqlite3.connect(sys.argv[1])
topics={i:(n,t) for i,n,t in con.execute('select id,name,type from topics')}
J,V,T,I,O,K,E,CL=[],[],[],[],[],[],[],[]; names=None
rows=[]
mx=int(sys.argv[3]) if len(sys.argv)>3 else 80000
print('max rowid',mx)
bad=0
for a in range(0,mx+1,200):
    try: rows+=con.execute('select rowid,topic_id,timestamp,data from messages where rowid>=? and rowid<?',(a,a+200)).fetchall()
    except Exception:
        for r in range(a,a+200):
            try: rows+=con.execute('select rowid,topic_id,timestamp,data from messages where rowid=?',(r,)).fetchall()
            except Exception: bad+=1
print('rows',len(rows),'bad',bad)
rows=list({r[0]:r for r in rows}.values()); print('unique',len(rows)); rows=[r[1:] for r in rows]; rows.sort(key=lambda r:r[1])
for tid,stamp,data in rows:
    name,typ=topics[tid]; tt=stamp*1e-9
    m=ts.deserialize_cdr(data,typ)
    if name=='/joint_states':
        names=list(m.name); T.append(tt); J.append(np.array(m.position)); V.append(np.array(m.velocity)); E.append(np.array(m.effort))
    elif name=='/imu/data':
        q=m.orientation; I.append((tt,q.x,q.y,q.z,q.w,m.angular_velocity.x,m.angular_velocity.y,m.angular_velocity.z,m.linear_acceleration.x,m.linear_acceleration.y,m.linear_acceleration.z))
    elif name=='/odom':
        p=m.pose.pose.position; q=m.pose.pose.orientation; v=m.twist.twist.linear
        O.append((tt,p.x,p.y,p.z,q.x,q.y,q.z,q.w,v.x,v.y))
    elif name=='/clock':
        CL.append((tt, m.clock.sec+m.clock.nanosec*1e-9))
    elif name=='/kick_ball':
        K.append((tt,m.x,m.y,m.dir,m.power,m.goal_x,m.goal_y,m.robot_theta_to_field))
np.savez(sys.argv[2], t=np.array(T), P=np.array(J), V=np.array(V), names=np.array(names), I=np.array(I), O=np.array(O), K=np.array(K), E=np.array(E), CL=np.array(CL))
print('saved', len(T), len(I), len(O), len(K), len(CL))
if K: print('kick first', K[0][1:], 'n', len(K))
