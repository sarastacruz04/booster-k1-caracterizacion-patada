# Sistema de control de la patada

`control_patada.py` (versión 5, final) corre **dentro del notebook de Booster Studio**, después de la celda de arranque (necesita `client` y la plantilla `brain/msg/Kick`). El notebook `notebook/operacion_patada.ipynb` ya trae una copia exacta.

## Funciones

| Función | Qué hace |
|---|---|
| `iniciar_lector()` | Lanza en segundo plano un nodo ROS 2 que lee `/odom`, `/clock`, `/kick_ball` y `/joint_states` |
| `girar_hasta(yaw)` / `girar(grados)` | Gira sobre sí mismo en lazo cerrado (±1.5°) |
| `ir_hasta(x, y)` | Camina a un punto en lazo cerrado con la odometría (imprecisa en pasos laterales) |
| `orbitar(grados)` | Rodea el balón (experimental) |
| `patada_A(x, y, power)` | Publica `/kick_ball` a 10 Hz, activa `VisualKick`, detecta el golpe (extensión de rodilla > 380 °/s), deja de publicar 0.3 s simulados después y desactiva la patada. Si no hay golpe en 8 s simulados, se detiene y avisa |
| `patear(comportamiento, retardo)` | Orden de alto nivel: `"recto"`, `"suave"`, `"izquierda"`, `"derecha"` (las dos últimas no fiables) |

## Evolución (`versiones_anteriores/`)

| Versión | Cambio | Resultado (pruebas) |
|---|---|---|
| v1 | Órbita en lazo cerrado + patada automática: activa `VisualKick` y publica durante 2.5 s simulados fijos | R_1 bien; L_izq_1 / L_der_1 giro correcto, patada fallida (balón 10–20 cm fuera) |
| v2 | Publica primero y activa la patada al llegar los mensajes; acepta `x`, `y` corregidos; sigue cortando a 2.5 s fijos | R_2 falla: con el nuevo orden, cortaba antes del golpe |
| v3 | **Detecta el golpe en las rodillas** y entonces corta | R_3 bien; órbitas siguen fallando (odometría) |
| v4 | Gira 30° sin caminar y corrige el mensaje con geometría | G_izq_1 / G_der_1 fallan |
| v5 | Giros de ±15°; comportamientos para la demo | P15 fallan; DEMO_recto, DEMO_retardo, DEMO_suave cumplen |

## `pruebas_sin_robot/`

Simulan un robot de mentira (con retardo de actuación y zona muerta) para comprobar la lógica de lazo cerrado y de detección del golpe sin abrir Booster Studio:
```bash
cd control/pruebas_sin_robot
python test_mock.py
```
