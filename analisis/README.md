# Scripts de análisis

Se ejecutan **desde esta carpeta** (`cd analisis`) en un computador con Python 3.10+ y `pip install -r ../requirements.txt`. No necesitan Booster Studio.

| Script | Qué hace | Entrada → salida |
|---|---|---|
| `leer_bag2.py` | Convierte una grabación de `ros2 bag` a `.npz` | `python leer_bag2.py <carpeta_bag> <salida.npz>` |
| `leer_db3.py` | Igual, pero lee el `.db3` fila por fila (recupera grabaciones sin `metadata.yaml` o dañadas) | `python leer_db3.py <archivo.db3> <salida.npz> [max_rowid]` |
| `leer_bag.py` | Primera versión del lector (Fase 2) | — |
| `metricas.py` | Métricas por prueba: pierna, golpe, velocidad de rodilla, giro, pitch/roll | `../datos/procesados/` → `../datos/metricas.json` |
| `dataset.py` | Construye el dataset | `metricas.json` → `../datos/dataset_D03.csv`, `dataset.json` |
| `resumen_goal.py` | Resumen de giro y golpe para las pruebas de `goal_y` | `python resumen_goal.py goal_n3_1 goal_p3_1 …` |
| `medir_balon.py` | Ajusta el círculo central en una captura cenital y mide el balón en D y grados | `../figuras/capturas/<nombre>_capturas.png` |
| `ficha.py`, `graf_ficha.py` | Ficha de articulaciones por etapa (Figura 4) | → `../figuras/ficha_articulaciones.png` |
| `graf_patada.py` | Línea de tiempo de la patada base (Figura 2) | → `../figuras/patada01_timeline.png` |
| `graf_postura.py` | Postura de pie / grabación de prueba (Figura 1) | `python graf_postura.py <npz> <png> [título]` |
| `graf_diagrama.py` | Diagrama temporal con fotogramas del video (Figura 3) | necesita `../videos/fotogramas_patada_03/` (no incluido) |
| `graf_f3.py` | Mapa del balón y métricas de la Fase 3 (Figuras 11 y 12) | `dataset.json` → `../figuras/f3_*.png` |
| `graf_f4_rep.py` | Repetibilidad de A, B y C (Figura 13) | → `../figuras/f4_repetibilidad.png` |
| `graf_*_video.py` | Fotogramas de los videos de pilotos | necesitan `../videos/*.mp4` (no incluidos) y `ffmpeg` |

Comprobación rápida de que todo cuadra: `python metricas.py` debe regenerar `../datos/metricas.json` idéntico al del repositorio.
