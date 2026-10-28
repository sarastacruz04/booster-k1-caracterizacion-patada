# Procedimiento de operación

Cómo arrancar el robot virtual, hacer una prueba de patada y guardar los datos. Está dividido en cuatro niveles según con qué frecuencia se hace cada cosa:

| Nivel | Cuándo | Qué incluye |
|---|---|---|
| 0 | Una sola vez en el computador | Instalación, carpetas, notebook, `control_patada.py` |
| 1 | Al empezar **cada sesión** | Plantilla Kick, conexión al SDK, funciones, modo Walking |
| 2 | En **cada prueba** | Colocar el robot, grabar, patear, copiar la grabación |
| 3 | Al terminar la sesión | Detener todo y copiar grabaciones |

**Por qué hay niveles:** lo que está en el computador se conserva (notebook, código, grabaciones copiadas), pero el contenedor del robot puede recrearse entre sesiones y la memoria del kernel de Python se pierde siempre. Por eso la plantilla Kick se comprueba en cada sesión y la celda de arranque se ejecuta en cada kernel.

Dónde se ejecuta cada cosa:
- **Notebook:** el notebook abierto como panel en Booster Studio (kernel dentro del contenedor, carpeta `/root`).
- **Terminal-B1:** la terminal del robot dentro de Booster Studio (también dentro del contenedor).
- **PowerShell:** una terminal de Windows en el computador (fuera del contenedor).

---

## Nivel 0 — Primera vez (una sola vez)

1. Instalar Booster Studio con el instalador oficial de Booster. El robot virtual necesita Docker Desktop.
2. Abrir Booster Studio, arrancar el robot virtual (pestaña B1) y comprobar que el indicador `127.0.0.1` está en verde.
3. Cargar la escena de cancha con balón.
4. Crear las carpetas del proyecto en el computador:
   - Carpeta del proyecto (donde va el notebook).
   - Carpeta de grabaciones: `Documents\Booster_grabaciones`.
5. Copiar `notebook/operacion_patada.ipynb` a la carpeta del proyecto (nunca dentro del contenedor).
6. Tener a mano `control/control_patada.py` (el notebook ya trae una copia exacta en su sección 3).

---

## Nivel 1 — Arranque de cada sesión (siempre, en este orden)

1. **Abrir Booster Studio** y arrancar el robot virtual. Esperar a que aparezca la cancha con el balón y el indicador `127.0.0.1` en verde.

2. **Abrir el notebook como panel** dentro de la vista del robot: pestaña B1 → *Open Notebook* → el archivo del proyecto.
   - No abrirlo a la vez como pestaña aparte: así el kernel no ejecuta.
   - Guardar con Ctrl + S y comprobar que desaparece la marca de cambios sin guardar.

3. **Terminal-B1: comprobar la plantilla del mensaje Kick.**
   ```bash
   source /opt/ros/humble/setup.bash && source ~/kick_ws/install/setup.bash && ros2 interface show brain/msg/Kick
   ```
   - Si aparecen estas 8 líneas, ir al paso 5:
     ```
     std_msgs/Header header
     float64 x
     float64 y
     float64 dir
     float64 goal_x
     float64 goal_y
     float64 robot_theta_to_field
     float64 power
     ```
   - Si sale un error (`No such file` o `Unknown package 'brain'`), hacer el paso 4.

4. **Terminal-B1: instalar la plantilla Kick** (solo si el paso 3 falló). Pegar el bloque completo (los mismos archivos están en `ros2_ws/src/brain/`):
   ```bash
   mkdir -p ~/kick_ws/src/brain/msg
   cat << 'EOF' > ~/kick_ws/src/brain/msg/Kick.msg
   std_msgs/Header header
   float64 x
   float64 y
   float64 dir
   float64 goal_x
   float64 goal_y
   float64 robot_theta_to_field
   float64 power
   EOF
   cat << 'EOF' > ~/kick_ws/src/brain/CMakeLists.txt
   cmake_minimum_required(VERSION 3.8)
   project(brain)
   find_package(ament_cmake REQUIRED)
   find_package(rosidl_default_generators REQUIRED)
   find_package(std_msgs REQUIRED)
   rosidl_generate_interfaces(${PROJECT_NAME} "msg/Kick.msg" DEPENDENCIES std_msgs)
   ament_export_dependencies(rosidl_default_runtime)
   ament_package()
   EOF
   cat << 'EOF' > ~/kick_ws/src/brain/package.xml
   <?xml version="1.0"?>
   <package format="3">
     <name>brain</name>
     <version>0.0.1</version>
     <description>Plantilla del mensaje Kick</description>
     <maintainer email="sara@example.com">sara</maintainer>
     <license>MIT</license>
     <buildtool_depend>ament_cmake</buildtool_depend>
     <buildtool_depend>rosidl_default_generators</buildtool_depend>
     <depend>std_msgs</depend>
     <exec_depend>rosidl_default_runtime</exec_depend>
     <member_of_group>rosidl_interface_packages</member_of_group>
     <export><build_type>ament_cmake</build_type></export>
   </package>
   EOF
   cd ~/kick_ws && source /opt/ros/humble/setup.bash && colcon build --packages-select brain
   source ~/kick_ws/install/setup.bash
   ros2 interface show brain/msg/Kick
   ```
   Al final deben aparecer las 8 líneas de la plantilla. En cada terminal nueva hay que repetir `source ~/kick_ws/install/setup.bash`.

5. **Terminal-B1: cerrar grabaciones viejas.**
   ```bash
   ps aux | grep "bag record" | grep -v grep
   ```
   Si sale alguna línea:
   ```bash
   pkill -INT -f "ros2 bag record"
   ```

6. **Notebook: celda de arranque** (sección 1 del notebook). Debe imprimir el estado del robot sin errores. Se ejecuta una sola vez por kernel; si da error de canal, *Restart* del kernel y ejecutarla de nuevo. El mensaje `ChannelSubscriber::InitChannel...` es informativo.

7. **Notebook: funciones de grabación** (sección 2).

8. **Notebook: sistema de control** (sección 3, copia de `control/control_patada.py`). No imprime nada.

9. **Preparar el robot:**
   1. Simulador: reiniciar la escena.
   2. Notebook (sección 4):
      ```python
      client.ChangeMode(RobotMode.kWalking)
      time.sleep(3)
      iniciar_lector()
      ```
      Debe aparecer `Lector listo: x=..., y=..., orientación=...°`.

---

## Nivel 2 — Cada prueba o patada

1. **Simulador:** reiniciar la escena. El robot vuelve a su posición de partida, junto a la banda, y el balón al punto central.

2. **Notebook:** modo Walking.
   ```python
   client.ChangeMode(RobotMode.kWalking)
   time.sleep(3)
   ```

3. **Notebook: llevar el robot a la posición de patada.** Ejecutar cada línea en una celda separada:
   ```python
   client.Move(0.0, 0.30, 0.0); time.sleep(25); client.Move(0.0, 0.0, 0.0)   # lateral a la izquierda
   client.Move(0.0, 0.0, 0.25); time.sleep(1); client.Move(0.0, 0.0, 0.0)    # giro a la izquierda
   client.Move(0.30, 0.0, 0.0); time.sleep(4); client.Move(0.0, 0.0, 0.0)    # avance
   client.Move(0.0, 0.22, 0.0); time.sleep(3); client.Move(0.0, 0.0, 0.0)    # ajuste lateral
   ```
   - **Posición objetivo:** el robot queda a la derecha del balón (vista cenital), mirándolo, a unos 0.45 m.
   - Los tiempos pueden necesitar ajuste porque la velocidad de simulación varía (0.43x–0.7x). Si el robot no llega, repetir la celda con más o menos tiempo.
   - No usar velocidades menores de 0.2 m/s: el robot hace el gesto pero no da pasos (zona muerta).
   - ⚠️ Esta colocación es en **lazo abierto** (velocidad × tiempo, ajustada a ojo). Es la principal fuente de variación entre pruebas.

4. **Pantalla:** empezar a grabar el video (opcional, recomendado). El video muestra el *Simulation time*, que es el mismo reloj que `/clock`.

5. **Notebook: iniciar la grabación de datos.**
   ```python
   p = iniciar_grabacion("NOMBRE")
   ```
   Esperar a ver `Grabando: NOMBRE` y sacar la captura cenital “antes”.

6. **Notebook: pedir la patada.**

   | Orden | Qué hace |
   |---|---|
   | `patear("recto")` | Pase estándar: golpe con la pierna derecha y balón ~40° a la izquierda del frente del robot |
   | `patear("recto", retardo=5)` | El mismo pase, 5 s después de pedirlo |
   | `patear("suave")` | Toque o conducción del balón sin golpe fuerte (power 0.5) |

   Esperar a que aparezca `Patada visual desactivada`. No tocar la terminal mientras tanto.

7. **Notebook: detener la grabación.**
   ```python
   detener_grabacion(p)
   ```
   Esperar a ver `Grabación detenida`. Sacar la captura “después” y parar el video.

8. **Terminal-B1: comprobar que la grabación se cerró bien.**
   ```bash
   ls -la /root/NOMBRE
   ```
   Deben aparecer `NOMBRE_0.db3` y `metadata.yaml`. **Nunca copiar una grabación que sigue abierta** (queda corrupta y sin `metadata.yaml`).

9. **PowerShell: copiar la grabación al computador.**
   ```powershell
   docker cp sj3yg-k1:/root/NOMBRE "$HOME\Documents\Booster_grabaciones\NOMBRE"
   ```
   (`sj3yg-k1` es el nombre del contenedor en este equipo; se consulta con `docker ps`.)

### Patada manual (sin el sistema de control)

1. Notebook: `client.VisualKick(True, VisualKickVersion.kV1)`
2. Terminal-B1: publicar la posición del balón:
   ```bash
   ros2 topic pub -r 10 /kick_ball brain/msg/Kick "{x: 0.6, y: 0.0, dir: 0.0, goal_x: 4.5, goal_y: 0.0, robot_theta_to_field: 0.0, power: 1.5}"
   ```
3. Ctrl + C justo después del golpe. Si no, el robot sigue pateando.
4. Notebook: `client.VisualKick(False)`

---

## Nivel 3 — Al terminar la sesión

1. Notebook: si quedó algo activo, detenerlo:
   ```python
   client.VisualKick(False)
   client.Move(0.0, 0.0, 0.0)
   ```
   Si quedó una grabación abierta: `detener_grabacion(p)`.
2. PowerShell: copiar con `docker cp` todas las grabaciones que falten. Lo que queda en `/root` puede perderse al cerrar.
3. Notebook: guardar con Ctrl + S.
4. Cerrar Booster Studio.

---

## Resultado esperado al validar (patada base `patear("recto")`)

Si el procedimiento está bien ejecutado, una patada base debería dar valores dentro de estos rangos (medidos en las pruebas 5–9, R_1, R_3 y DEMO_recto):

| Qué mirar | Valor esperado |
|---|---|
| Salida del notebook | `golpe a ~3.1–3.6 s simulados de activar la patada (−380 a −440 °/s)` |
| Pierna que golpea | Derecha |
| Dirección del balón | 32°–48° a la izquierda del frente inicial del robot (media ~41°) |
| Distancia del balón | 1.1–2.4 D (D = diámetro del círculo central) |
| Inclinación máx. del torso (pitch) | ~12° |
| Caída del robot | No |

Cómo se mide el balón: en las capturas cenitales “antes” y “después” se ajusta una circunferencia a las líneas del círculo central y se expresa la posición del balón en diámetros de ese círculo (D). Script: `analisis/medir_balon.py`.
