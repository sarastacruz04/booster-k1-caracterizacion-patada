# Datos

## `dataset_D03.csv` — dataset de las 41 pruebas (entregable D0.3)

Separador `;`, decimales con coma, codificación UTF-8 con BOM (se abre directo en Excel). Una fila por prueba con su configuración (versión de la patada y campos del mensaje `/kick_ball`) y su resultado (pierna, instante del golpe, velocidad de rodilla, pitch del torso, si golpeó, distancia y dirección del balón, validez y notas).

- **Instante del golpe:** máximo de la velocidad de extensión de la rodilla que golpea, en segundos de simulación desde el primer mensaje publicado. Confirmado con el video.
- **Distancia del balón:** en **D** = diámetro del círculo central de la cancha, medido en las capturas cenitales.
- **Dirección del balón:** grados respecto al frente inicial del robot, **+ = izquierda**.

### Nombres de las pruebas

| Prefijo | Fase | Qué se probó |
|---|---|---|
| `P4`–`P9` | F1 | Baseline y serie de repetibilidad (observación visual, sin grabación) |
| `patada_01`–`03` | F2 | Patada base grabada (03 con video) |
| `dir_p05`, `dir_n05` | F3 | `dir` = +0.5 / −0.5 rad |
| `goal_n3`, `goal_p3`, `goal_n05` | F3 | `goal_y` = −3 / +3 / −0.5 m |
| `power_6`, `power_05` | F3 | `power` = 6.0 / 0.5 |
| `B_2`, `B_3`, `C_2`, `C_3` | F4 | Repetibilidad de los comportamientos B (power 0.5) y C (goal_y −0.5) |
| `S_1` | F4 | `Shoot()` (error 501) |
| `O_izq_1`, `O_der_1` | F4 | Órbita en lazo abierto |
| `R_1`–`R_3` | F4 | Patada recta automática (control v1–v3) |
| `L_izq_*`, `L_der_*` | F4 | Órbita en lazo cerrado (control v1–v3) |
| `G_izq_1`, `G_der_1` | F4 | Giro de 30° + mensaje corregido (control v4) |
| `P15_izq_1`, `P15_der_1` | F4 | Giro de 15° (control v5) |
| `DEMO_recto`, `DEMO_retardo`, `DEMO_suave` | F4 | Demo final (D0.5) |

El sufijo `_1`, `_2`… es el número de repetición.

## `procesados/*.npz` — grabaciones convertidas

Cada `.npz` es una grabación de `ros2 bag` convertida con `analisis/leer_db3.py` (o `leer_bag2.py`). Se leen con:

```python
import numpy as np
d = np.load("procesados/R_3.npz", allow_pickle=True)
print(d.files)
```

| Clave | Forma | Contenido |
|---|---|---|
| `names` | (22,) | Nombres de las 22 articulaciones |
| `t` | (N,) | Marca de tiempo de grabación (s) de cada mensaje de `/joint_states` |
| `P` | (N, 22) | Posición de cada articulación (rad) |
| `V` | (N, 22) | Velocidad de cada articulación (rad/s) |
| `E` | (N, 22) | Esfuerzo de cada articulación |
| `I` | (M, 11) | `/imu/data`: t, cuaternión (x, y, z, w), velocidad angular (x, y, z), aceleración lineal (x, y, z) |
| `O` | (K, 10) | `/odom`: t, posición (x, y, z), cuaternión (x, y, z, w), velocidad lineal (x, y) |
| `K` | (n, 8) | `/kick_ball`: t, x, y, dir, power, goal_x, goal_y, robot_theta_to_field |
| `CL` | (c, 2) | `/clock`: t de grabación, tiempo de simulación (s) |

- Para pasar cualquier tiempo a **tiempo de simulación**, interpolar con `CL`: `np.interp(t, CL[:,0], CL[:,1])`.
- `prueba.npz` es la grabación de prueba con el robot quieto (Figura 1); `ficha.npz` son los datos de la ficha de articulaciones (Figura 4).
- `goal_n3_2` y `goal_p3_1` se recuperaron de grabaciones copiadas sin cerrar (sin `metadata.yaml`), leyendo la base de datos fila por fila con `leer_db3.py`.
- Diferencias entre grabaciones (por cómo evolucionó el procedimiento):
  - `prueba.npz` usa el primer lector (otras columnas en `I` y `O`, sin `K` ni `CL`).
  - `patada_01.npz` no tiene `/clock` (se añadió a la grabación desde `patada_02`); sus tiempos son de reloj de pared.
  - En `patada_01`–`03`, `dir_p05_*` y `goal_n3_1`, `K` tiene 5 columnas: t, x, y, dir, power.
  - `dir_n05_1` y `S_1` no tienen mensajes de `/kick_ball` grabados (`S_1` usa `Shoot()`, que no publica).

## `metricas.json` y `dataset.json`

Resultados intermedios de `analisis/metricas.py` y `analisis/dataset.py` (las métricas por prueba de las Fases 2 y 3, antes de juntarlas en el CSV).
