#!/bin/bash
# Instala la plantilla brain/msg/Kick dentro del contenedor del robot virtual.
# Uso (en la Terminal-B1 de Booster Studio, después de copiar esta carpeta al contenedor):
#   bash instalar_plantilla_kick.sh
# Equivale al paso 4 del Nivel 1 de PROCEDIMIENTO.md.
set -e
mkdir -p ~/kick_ws/src
cp -r "$(dirname "$0")/src/brain" ~/kick_ws/src/
cd ~/kick_ws && source /opt/ros/humble/setup.bash && colcon build --packages-select brain
source ~/kick_ws/install/setup.bash
ros2 interface show brain/msg/Kick
