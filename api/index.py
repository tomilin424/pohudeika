from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from pathlib import Path

# Создаем FastAPI приложение
app = FastAPI()

# Получаем путь к корневой директории
root_dir = Path(__file__).resolve().parent.parent

# Настраиваем статические файлы и шаблоны
app.mount("/static", StaticFiles(directory=str(root_dir / "web/static")), name="static")
templates = Jinja2Templates(directory=str(root_dir / "web/templates"))

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/webapp")
async def webapp(request: Request):
    return templates.TemplateResponse("webapp.html", {"request": request})

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "bot_token": os.getenv("BOT_TOKEN", "Not set")
    } 