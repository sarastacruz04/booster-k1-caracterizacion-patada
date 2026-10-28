# ============================================================
#  CONTROL DE LA PATADA — Fase 4 (Booster K1, Booster Studio)
#  Versión 3. Ejecutar UNA vez por sesión, después de la celda de
#  arranque (necesita `client` y la plantilla brain/msg/Kick).
# ============================================================
import subprocess, threading, math, time

ROS = "source /opt/ros/humble/setup.bash && source ~/kick_ws/install/setup.bash && "
D_BALON = 0.45      # distancia robot–balón en la posición de patada (m) ≈ 0.3 D
X_BASE = 0.6        # x publicado en el baseline (con el balón a D_BALON)

# ---------- 1. Lector en segundo plano: /odom, /clock y /kick_ball ----------
LECTOR = r'''
import rclpy, math
from rclpy.node import Node
from nav_msgs.msg import Odometry
from rosgraph_msgs.msg import Clock
from brain.msg import Kick
from sensor_msgs.msg import JointState
class Lector(Node):
    def __init__(self):
        super().__init__("lector_control")
        self.t = 0.0
        self.create_subscription(Clock, "/clock", self.reloj, 10)
        self.create_subscription(Odometry, "/odom", self.odom, 10)
        self.create_subscription(Kick, "/kick_ball", self.kick, 10)
        self.create_subscription(JointState, "/joint_states", self.articulaciones, 10)
        self.idx = None
    def reloj(self, m):
        self.t = m.clock.sec + m.clock.nanosec * 1e-9
    def odom(self, m):
        q = m.pose.pose.orientation
        yaw = math.atan2(2*(q.w*q.z + q.x*q.y), 1 - 2*(q.y*q.y + q.z*q.z))
        p = m.pose.pose.position
        print(f"O,{self.t:.3f},{p.x:.4f},{p.y:.4f},{yaw:.5f}", flush=True)
    def kick(self, m):
        print(f"K,{self.t:.3f}", flush=True)
    def articulaciones(self, m):
        if self.idx is None:
            self.idx = [i for i, n in enumerate(m.name) if n in ("Left_Knee_Pitch", "Right_Knee_Pitch")]
        v = min(m.velocity[i] for i in self.idx)          # extensión de rodilla = velocidad negativa
        if v < -6.6:                                      # < -380 °/s: golpe
            print(f"G,{self.t:.3f},{math.degrees(v):.0f}", flush=True)
rclpy.init(); rclpy.spin(Lector())
'''
with open("/root/lector_control.py", "w") as f:
    f.write(LECTOR)

estado = {"t": None, "x": None, "y": None, "yaw": None, "n_kick": 0, "t_kick0": None, "t_golpe": None, "v_golpe": None}

def _leer(proc):
    for linea in proc.stdout:
        partes = linea.strip().split(",")
        try:
            if partes[0] == "O":
                t, x, y, yaw = map(float, partes[1:])
                estado.update(t=t, x=x, y=y, yaw=yaw)
            elif partes[0] == "K":
                if estado["n_kick"] == 0:
                    estado["t_kick0"] = float(partes[1])
                estado["n_kick"] += 1
            elif partes[0] == "G":
                estado["t_golpe"], estado["v_golpe"] = float(partes[1]), float(partes[2])
        except (ValueError, IndexError):
            pass

def iniciar_lector():
    global _lector
    _lector = subprocess.Popen(["bash", "-c", ROS + "exec python3 /root/lector_control.py"],
                               stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    threading.Thread(target=_leer, args=(_lector,), daemon=True).start()
    for _ in range(150):
        if estado["yaw"] is not None:
            print(f"Lector listo: x={estado['x']:.2f} m, y={estado['y']:.2f} m, "
                  f"orientación={math.degrees(estado['yaw']):.1f}°")
            return
        time.sleep(0.1)
    print("⚠️ El lector no recibe /odom. ¿Está el robot en modo Walking?")

def _ang(a):
    return math.atan2(math.sin(a), math.cos(a))

def _parar():
    client.Move(0.0, 0.0, 0.0)

# ---------- 2. Movimientos en lazo cerrado ----------
def girar_hasta(yaw_obj, w=0.3, tol_grados=1.5, t_max=30):
    inicio = time.time()
    while time.time() - inicio < t_max:
        err = _ang(yaw_obj - estado["yaw"])
        if abs(math.degrees(err)) <= tol_grados:
            break
        vel = w if abs(math.degrees(err)) > 12 else 0.12     # más lento cerca del objetivo
        client.Move(0.0, 0.0, vel if err > 0 else -vel)
        time.sleep(0.05)
    _parar(); time.sleep(1.0)

def ir_hasta(x_obj, y_obj, v=0.25, tol=0.03, t_max=40):
    inicio = time.time()
    while time.time() - inicio < t_max:
        dx, dy = x_obj - estado["x"], y_obj - estado["y"]
        dist = math.hypot(dx, dy)
        if dist <= tol:
            break
        c, s = math.cos(estado["yaw"]), math.sin(estado["yaw"])
        ex, ey = c*dx + s*dy, -s*dx + c*dy
        client.Move(v*ex/dist, v*ey/dist, 0.0)
        time.sleep(0.05)
    _parar(); time.sleep(1.0)

def balon_relativo(bx, by):
    """Posición estimada del balón en el marco del robot (x adelante, y izquierda)."""
    dx, dy = bx - estado["x"], by - estado["y"]
    c, s = math.cos(estado["yaw"]), math.sin(estado["yaw"])
    return c*dx + s*dy, -s*dx + c*dy

def orbitar(grados, d=D_BALON, rondas=4):
    """Rodea el balón (d m delante del robot) y termina mirándolo con la orientación
    girada `grados` (positivo = más a la izquierda). Corrige hasta `rondas` veces.
    Devuelve la posición estimada del balón en el marco del robot al terminar."""
    x0, y0, yaw0 = estado["x"], estado["y"], estado["yaw"]
    bx, by = x0 + d*math.cos(yaw0), y0 + d*math.sin(yaw0)
    yaw1 = yaw0 + math.radians(grados)
    x1, y1 = bx - d*math.cos(yaw1), by - d*math.sin(yaw1)
    for r in range(rondas):
        girar_hasta(yaw1)
        ir_hasta(x1, y1)
        err_pos = math.hypot(estado["x"] - x1, estado["y"] - y1)
        err_ang = math.degrees(_ang(estado["yaw"] - yaw1))
        if err_pos <= 0.04 and abs(err_ang) <= 2.0:
            break
    giro = math.degrees(_ang(estado["yaw"] - yaw0))
    xb, yb = balon_relativo(bx, by)
    print(f"Órbita: giro real {giro:.1f}° (pedido {grados}°), error de posición "
          f"{100*err_pos:.0f} cm tras {r+1} ronda(s); balón estimado en x={xb:.2f} m, y={yb:+.2f} m")
    return xb, yb

# ---------- 3. Patada A con publicación automática ----------
def patada_A(x=X_BASE, y=0.0, power=1.5, max_sim=8.0):
    """Publica (x, y) en /kick_ball, activa la patada visual y detiene la publicación
    sola en cuanto detecta el golpe (rodilla extendiéndose a más de 380 °/s)."""
    msg = (f"{{x: {x:.3f}, y: {y:.3f}, dir: 0.0, goal_x: 4.5, goal_y: 0.0, "
           f"robot_theta_to_field: 0.0, power: {power}}}")
    n0 = estado["n_kick"]
    pub = subprocess.Popen(["bash", "-c", ROS + f'exec ros2 topic pub -r 10 /kick_ball brain/msg/Kick "{msg}"'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    inicio = time.time()
    while estado["n_kick"] == n0 and time.time() - inicio < 30:   # espera a que el publicador arranque
        time.sleep(0.05)
    client.VisualKick(True, VisualKickVersion.kV1)
    t0 = estado["t"]
    estado["t_golpe"] = None
    while time.time() - inicio < 90:
        if estado["t_golpe"] is not None and estado["t_golpe"] > t0 + 0.5:
            break                                                  # golpe detectado
        if estado["t"] - t0 > max_sim:
            break                                                  # no hubo golpe: se rinde
        time.sleep(0.02)
    golpe = estado["t_golpe"] is not None and estado["t_golpe"] > t0 + 0.5
    t_fin = estado["t"]
    while estado["t"] - t_fin < 0.3:                               # margen tras el golpe
        time.sleep(0.02)
    pub.terminate(); pub.wait(timeout=10)
    if golpe:
        print(f"Mensaje x={x:.2f}, y={y:+.2f}: golpe a {estado['t_golpe'] - t0:.2f} s simulados "
              f"de activar la patada ({estado['v_golpe']:.0f} °/s); publicación detenida")
    else:
        print(f"⚠️ Mensaje x={x:.2f}, y={y:+.2f}: no se detectó golpe en {max_sim:.0f} s simulados")
    time.sleep(3.0)
    client.VisualKick(False)
    print("Patada visual desactivada")

# ---------- 4. Comandos de alto nivel ----------
COMPORTAMIENTOS = {"recto": 0, "izquierda": 40, "derecha": -40}

def patear(comportamiento):
    grados = COMPORTAMIENTOS[comportamiento]
    print(f"== Comportamiento: {comportamiento} (órbita {grados}°) ==")
    if grados == 0:
        patada_A()
        return
    xb, yb = orbitar(grados)
    # el mensaje describe dónde quedó el balón respecto a la posición del baseline
    patada_A(x=X_BASE + (xb - D_BALON), y=yb)
