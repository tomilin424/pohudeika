#!/bin/bash

# Устанавливаем зависимости из vercel_requirements.txt
pip install -r vercel_requirements.txt

# Запускаем приложение
uvicorn api.index:app --host 0.0.0.0 --port $PORT 