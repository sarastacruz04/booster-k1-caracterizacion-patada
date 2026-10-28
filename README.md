# Caracterización física y control de la patada del Booster K1 (Booster Studio)

**Autora:** Sara Santacruz Corredor · Universidad de La Sabana · octubre 2026

Fase previa al proyecto de aprendizaje por refuerzo (RL): entender experimentalmente cómo funciona la patada visual del robot humanoide **Booster K1** en el simulador **Booster Studio**, medir qué parámetros la modifican y construir un sistema que permita pedir distintas patadas de forma intencional y repetible.

El trabajo siguió un roadmap de dos semanas en cuatro fases y registró **41 pruebas** (grabaciones de sensores con `ros2 bag`, capturas cenitales y videos).

| Fase | Qué se hizo | Entregable |
|---|---|---|
| F1 · Familiarización y baseline | Interfaz del SDK, descubrimiento de `/kick_ball`, serie de repetibilidad (pruebas 5–9) | D0.1 Guía de operación · baseline |
| F2 · Descomposición | Grabación de la patada base, 6 etapas, ficha de articulaciones, diagrama temporal | D0.2 Caracterización de la patada base |
| F3 · Sensibilidad | Un parámetro a la vez: `dir`, `goal_y`, `power` | D0.3 Dataset · D0.4 Mapa de sensibilidad |
| F4 · Control integrado | Sistema `control_patada.py` (5 versiones), 6 métodos de dirección, demo | D0.5 Demo de control |

La explicación completa, con todas las tablas y figuras, está en **[`docs/Caracterizacion_bitacora.docx`](docs/Caracterizacion_bitacora.docx)**.
El procedimiento paso a paso para reproducirlo está en **[`PROCEDIMIENTO.md`](PROCEDIMIENTO.md)**.

---

## Hallazgos principales

1. **La patada visual no busca el balón en el simulador.** Solo patea cuando alguien publica la posición del balón en el tópico `/kick_ball` (tipo `brain/msg/Kick`). En el robot real eso lo hace el programa de visión; en Booster Studio el tópico tiene 2 suscriptores y 0 publicadores. Hay que instalar la plantilla del mensaje (`ros2_ws/`) y publicarla uno mismo.
2. **El núcleo del golpe es un patrón fijo** (±0.01 s, ±1° entre repeticiones): carga → swing 0.34 s, swing → contacto 0.16 s. Lo que varía es la aproximación.
3. **Baseline** (V1, x 0.6, y 0, dir 0, goal_x 4.5, goal_y 0, power 1.5): pierna derecha, balón 32°–48° a la izquierda del frente del robot (media ~41°), 1.1–2.4 D, rodilla ~400–440 °/s, pitch del torso ~12°.
4. **Sensibilidad:**
   - `dir`: sin efecto apreciable.
   - `goal_y`: decide el sentido de un giro del robot, pero en lazo abierto el robot sigue girando mientras se publica (hasta +596°) y el golpe empeora.
   - `power`: 0.5 → toque/conducción sin golpe fuerte; 1.5 → pase; 6.0 → swing de ~865 °/s que golpea al aire.
5. **El golpe llega ~0.9 s después del último mensaje** publicado, y la pierna que golpea decide el lado (derecha → balón a la izquierda).
6. **La dirección del balón no es controlable de forma fiable** con las interfaces disponibles: se probaron 6 métodos (órbita en lazo abierto, órbita en lazo cerrado, giro + mensaje corregido, giro de ±15°, `goal_y`, `power`). La odometría se equivoca 10–25 cm en pasos laterales y no hay medida real del balón.
7. `Shoot()` devuelve error 501 en el simulador.

### Qué se puede controlar con `control_patada.py`

| Variable | ¿Controlable? | Cómo |
|---|---|---|
| Momento de la patada (timing) | Sí | `patear("recto", retardo=5)` |
| Intensidad | Sí, por niveles | `patear("recto")` (power 1.5) vs `patear("suave")` (power 0.5) |
| Orientación del robot | Sí, ±1.5° | `girar(grados)`, `girar_hasta(yaw)` (lazo cerrado con IMU) |
| Posición del robot | Imprecisa | `ir_hasta(x, y)`, `orbitar(grados)` (odometría, error 10–25 cm) |
| Dirección del balón | No fiable | `patear("izquierda"/"derecha")` existen pero son experimentales |

---

## Estructura del repositorio

```
├── README.md                  ← este archivo
├── PROCEDIMIENTO.md           ← procedimiento de operación (niveles 0–3) y resultado esperado
├── docs/
│   ├── Caracterizacion_bitacora.docx   ← bitácora completa (hallazgos, pruebas, figuras, informe final)
│   └── D0.1_Guia_de_operacion.docx
├── notebook/
│   └── operacion_patada.ipynb ← celdas listas: arranque, grabación, control, prueba
├── control/
│   ├── control_patada.py      ← sistema de control, versión 5 (final)
│   ├── versiones_anteriores/  ← v1–v4, para seguir la evolución descrita en la bitácora
│   └── pruebas_sin_robot/     ← pruebas con un robot simulado de mentira (no necesitan Booster Studio)
├── ros2_ws/
│   ├── src/brain/             ← paquete ROS 2 con la plantilla brain/msg/Kick
│   └── instalar_plantilla_kick.sh
├── datos/
│   ├── dataset_D03.csv        ← dataset de las 41 pruebas (separador ';', se abre en Excel)
│   ├── metricas.json, dataset.json
│   ├── procesados/*.npz       ← grabaciones de cada prueba convertidas a NumPy
│   └── README.md              ← qué contiene cada archivo y cómo leerlo
├── analisis/                  ← scripts que generan métricas, dataset y figuras
│   └── README.md
└── figuras/                   ← figuras de la bitácora; capturas/ = capturas cenitales antes/después
```

## Entorno

| Elemento | Valor |
|---|---|
| Simulador | Booster Studio, robot virtual K1 (22 grados de libertad) |
| Contenedor | Docker Desktop (Windows), imagen `virtual-robot:0.8.4-beta-humble`, contenedor `sj3yg-k1` |
| ROS | ROS 2 Humble |
| SDK | `booster_robotics_sdk_python` (`B1LocoClient`), robot en `127.0.0.1` |
| Notebook | Kernel “Booster Jupyter”, Python 3.10, dentro del contenedor (`/root`) |
| Firmware | v1.5.2.1 o superior (requisito de la patada visual) |
| Velocidad de simulación | Variable, 0.43x–0.7x → **todos los tiempos se miden con `/clock`** |

## Cómo reproducir

1. Seguir [`PROCEDIMIENTO.md`](PROCEDIMIENTO.md) niveles 0 y 1 (incluye instalar la plantilla Kick).
2. Abrir `notebook/operacion_patada.ipynb` como panel en Booster Studio y ejecutar las secciones 1–4.
3. Colocar el robot (sección 5.1) y ejecutar `patear("recto")`.
4. Comparar con la tabla **“Resultado esperado al validar”** al final de `PROCEDIMIENTO.md`.

Para revisar los análisis sin el robot (en cualquier computador con Python):
```bash
pip install -r requirements.txt
cd analisis
python metricas.py      # recalcula datos/metricas.json desde datos/procesados/
python graf_f3.py       # regenera figuras/f3_mapa_balon.png y f3_metricas.png
```

## Qué no está en el repositorio

- **Grabaciones crudas de `ros2 bag`** (`.db3`, ~1 GB): superan el límite de GitHub. Están convertidas a `.npz` en `datos/procesados/` sin pérdida de los tópicos usados. Las originales están disponibles a petición.
- **Videos de pantalla** (`.mp4`): disponibles a petición. Serie de repetibilidad (pruebas 5–9): https://youtu.be/ZSQiHGStv5E

## Limitaciones conocidas

- La colocación del robot antes de cada patada es en lazo abierto (velocidad × tiempo); es la principal fuente de variación.
- La distancia del balón se mide en diámetros del círculo central (D), no en metros, porque no se conocen las medidas exactas de la cancha simulada.
- Las pruebas P4–P9 de la Fase 1 son observaciones visuales sin grabación de sensores.

## Recomendaciones para el proyecto de RL

1. Dar a la política la **posición real del balón** (del simulador al entrenar; de la visión en el robot real).
2. **No usar la odometría como verdad**; usar la pose real del simulador.
3. Reutilizar las métricas de este trabajo para la recompensa: dirección y distancia del balón, momento del golpe, velocidad de la rodilla, inclinación del torso (~15° como límite de estabilidad).
4. Usar la patada visual como **referencia**, no como trayectoria a copiar.
5. Medir los tiempos con el **reloj de la simulación**.
6. **Aleatorizar la posición inicial del balón** al entrenar.
