#!/bin/bash
set -e

cd /home/cultivai/pycultivai

echo "[setup_venv] Borrando entorno .venv (si existe)..."
rm -rf .venv

echo "[setup_venv] Creando entorno .venv nuevo..."
python3 -m venv .venv

echo "[setup_venv] Instalando paquetes..."
. .venv/bin/activate
pip install --upgrade pip
pip install supabase pyserial

echo "[setup_venv] Entorno listo."
exit 0
