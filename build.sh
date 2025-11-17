#!/usr/bin/env bash
# build.sh
set -o errexit  # Detener si ocurre un error

# Actualizar pip
python -m pip install --upgrade pip

# Preparar Django
python manage.py collectstatic --noinput
python manage.py migrate --noinput
