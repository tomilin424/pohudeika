from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import sys
from pathlib import Path

# Добавляем корневую директорию в путь для импортов
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from webapp import app as webapp
from database import init_db

# Инициализируем базу данных
init_db()

# Настраиваем статические файлы и шаблоны для Vercel
webapp.mount("/static", StaticFiles(directory=str(root_dir / "web/static")), name="static")
templates = Jinja2Templates(directory=str(root_dir / "web/templates"))

# Экспортируем приложение для Vercel
app = webapp 