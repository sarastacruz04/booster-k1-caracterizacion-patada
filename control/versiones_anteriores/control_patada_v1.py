# ============================================================
#  CONTROL DE LA PATADA — Fase 4 (Booster K1, Booster Studio)
#  Ejecutar UNA vez por sesión, después de la celda de arranque
#  (necesita `client` y la plantilla brain/msg/Kick instalada).
# ============================================================
import subprocess, threading, math, time

ROS = "source /opt/ros/humble/setup.bash && source ~/kick_ws/install/setup.bash && "

# ---------- 1. Lector de odometría y reloj simulado (en segundo plano) ----------
LECTOR = r'''
import rclpy, math
from rclpy.node import Node
from nav_msgs.msg import Odometry
from rosgraph_msgs.msg import Clock
class Lector(Node):
    def __init__(self):
        super().__init__("lector_control")
        self.create_subscription(Odometry, "/odom", self.odom, 10)
        self.create_subscription(Clock, "/clock", self.reloj, 10)
        self.t = 0.0
    def reloj(self, m):
        self.t = m.clock.sec + m.clock.nanosec * 1e-9
    def odom(self, m):
        q = m.pose.pose.orientation
        yaw = math.atan2(2*(q.w*q.z + q.x*q.y), 1 - 2*(q.y*q.y + q.z*q.z))
        p = m.pose.pose.position
        print(f"{self.t:.3f},{p.x:.4f},{p.y:.4f},{yaw:.5f}", flush=True)
rclpy.init(); rclpy.spin(Lector())
'''
with open("/root/lector_control.py", "w") as f:
    f.write(LECTOR)

estado = {"t": None, "x": None, "y": None, "yaw": None}

def _leer(proc):
    for linea in proc.stdout:
        try:
            t, x, y, yaw = map(float, linea.strip().split(","))
            estado.update(t=t, x=x, y=y, yaw=yaw)
        except ValueError:
            pass

def iniciar_lector():
    global _lector
    _lector = subprocess.Popen(["bash", "-c", ROS + "exec python3 /root/lector_control.py"],
                               stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    threading.Thread(target=_leer, args=(_lector,), daemon=True).start()
    for _ in range(100):
        if estado["yaw"] is not None:
            print(f"Lector listo: x={estado['x']:.2f} m, y={estado['y']:.2f} m, "
                  f"orientación={math.degrees(estado['yaw']):.1f}°")
            return
        time.sleep(0.1)
    print("⚠️ El lector no recibe /odom. ¿Está el robot en modo Walking?")

def _ang(a):                      # normaliza un ángulo a [-pi, pi]
    return math.atan2(math.sin(a), math.cos(a))

def _parar():
    client.Move(0.0, 0.0, 0.0)

# ---------- 2. Movimientos en lazo cerrado ----------
def girar_hasta(yaw_obj, w=0.3, tol_grados=2.0, t_max=30):
    """Gira sobre sí mismo hasta la orientación yaw_obj (rad), midiendo con /odom."""
    inicio = time.time()
    while time.time() - inicio < t_max:
        err = _ang(yaw_obj - estado["yaw"])
        if abs(math.degrees(err)) <= tol_grados:
            break
        client.Move(0.0, 0.0, w if err > 0 else -w)
        time.sleep(0.05)
    _parar(); time.sleep(1.0)

def ir_hasta(x_obj, y_obj, v=0.25, tol=0.04, t_max=40):
    """Camina (sin girar) hasta el punto (x_obj, y_obj) del marco de /odom."""
    inicio = time.time()
    while time.time() - inicio < t_max:
        dx, dy = x_obj - estado["x"], y_obj - estado["y"]
        dist = math.hypot(dx, dy)
        if dist <= tol:
            break
        c, s = math.cos(estado["yaw"]), math.sin(estado["yaw"])
        ex, ey = c*dx + s*dy, -s*dx + c*dy           # error en el marco del robot
        client.Move(v*ex/dist, v*ey/dist, 0.0)        # velocidad fija hacia el objetivo
        time.sleep(0.05)
    _parar(); time.sleep(1.0)

def orbitar(grados, d=0.45):
    """Rodea el balón (a d metros delante del robot) y termina mirándolo,
    con la orientación girada `grados` (positivo = más a la izquierda)."""
    x0, y0, yaw0 = estado["x"], estado["y"], estado["yaw"]
    bx, by = x0 + d*math.cos(yaw0), y0 + d*math.sin(yaw0)       # balón estimado
    yaw1 = yaw0 + math.radians(grados)
    x1, y1 = bx - d*math.cos(yaw1), by - d*math.sin(yaw1)       # nuevo punto de patada
    girar_hasta(yaw1)
    ir_hasta(x1, y1)
    girar_hasta(yaw1, tol_grados=1.5)                           # corrección final
    giro = math.degrees(_ang(estado["yaw"] - yaw0))
    err = math.hypot(estado["x"] - x1, estado["y"] - y1)
    print(f"Órbita: giro real {giro:.1f}° (pedido {grados}°), error de posición {100*err:.0f} cm")
    return giro

# ---------- 3. Patada A con publicación automática ----------
def patada_A(segundos_sim=2.5, power=1.5):
    """Activa la patada visual, publica el mensaje del baseline durante `segundos_sim`
    segundos SIMULADOS y la detiene sola (sin Ctrl + C)."""
    msg = ("{x: 0.6, y: 0.0, dir: 0.0, goal_x: 4.5, goal_y: 0.0, "
           f"robot_theta_to_field: 0.0, power: {power}}}")
    client.VisualKick(True, VisualKickVersion.kV1)
    time.sleep(1.0)
    pub = subprocess.Popen(["bash", "-c", ROS + f'exec ros2 topic pub -r 10 /kick_ball brain/msg/Kick "{msg}"'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    t0, inicio = estado["t"], time.time()
    while estado["t"] - t0 < segundos_sim and time.time() - inicio < segundos_sim / 0.3:
        time.sleep(0.05)
    pub.terminate(); pub.wait(timeout=10)
    print(f"Publicación detenida tras {estado['t'] - t0:.2f} s simulados")
    time.sleep(4.0)                                  # deja terminar el golpe y la recuperación
    client.VisualKick(False)
    print("Patada visual desactivada")

# ---------- 4. Comandos de alto nivel ----------
COMPORTAMIENTOS = {
    "recto":     0,     # sin órbita: el balón sale ~40° a la izquierda del frente inicial
    "izquierda": 40,    # el robot mira 40° más a la izquierda antes de patear
    "derecha":  -40,    # el robot mira 40° más a la derecha antes de patear
}
def patear(comportamiento):
    grados = COMPORTAMIENTOS[comportamiento]
    print(f"== Comportamiento: {comportamiento} (órbita {grados}°) ==")
    if grados != 0:
        orbitar(grados)
    patada_A()
