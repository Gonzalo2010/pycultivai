#!/bin/bash
set -e

cd /home/cultivai/pycultivai

# Si no existe el venv, lo creamos e instalamos paquetes
if [ ! -d ".venv" ]; then
  echo "[setup_venv] Creando entorno .venv..."
  python3 -m venv .venv
  . .venv/bin/activate
  pip install --upgrade pip
  pip install supabase pyserial
else
  echo "[setup_venv] .venv ya existe, no hago nada."
fi

exit 0
