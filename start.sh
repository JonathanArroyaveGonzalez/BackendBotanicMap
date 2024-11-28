#!/bin/bash

# Activar el entorno virtual
source /opt/render/project/src/.venv/bin/activate

# Asigna el puerto especificado por Render o usa el puerto 8000 por defecto
PORT=${PORT:-8000}

# Ejecuta la aplicación FastAPI con uvicorn
uvicorn main:app --host 0.0.0.0 --port $PORT