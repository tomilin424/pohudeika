from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn
from datetime import datetime
import subprocess
import psutil
import os
import io
import csv

app = FastAPI()

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# Настраиваем шаблоны
templates = Jinja2Templates(directory="web/templates")

# Время запуска приложения
START_TIME = datetime.now()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/users")
async def users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request})

@app.get("/stats")
async def stats(request: Request):
    return templates.TemplateResponse("stats.html", {"request": request})

@app.get("/api/status")
async def get_status():
    # Получаем информацию о процессе бота
    bot_process = None
    for proc in psutil.process_iter(['pid', 'name']):
        if 'python' in proc.info['name'] and 'main.py' in proc.cmdline():
            bot_process = proc
            break

    uptime = str(datetime.now() - START_TIME).split('.')[0]
    
    return {
        "status": "Работает" if bot_process else "Остановлен",
        "uptime": uptime,
        "active_users": "42"  # Здесь нужно получить реальное количество из базы данных
    }

@app.post("/api/restart")
async def restart_bot():
    try:
        # Останавливаем текущий процесс бота
        for proc in psutil.process_iter(['pid', 'name']):
            if 'python' in proc.info['name'] and 'main.py' in proc.cmdline():
                proc.kill()
        
        # Запускаем бота заново
        subprocess.Popen(["python", "main.py"])
        
        return {"message": "Бот успешно перезапущен"}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Ошибка при перезапуске бота: {str(e)}"}
        )

@app.get("/api/users")
async def get_users():
    db = next(get_db())
    users = db.query(User).all()
    return users

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/api/broadcast")
async def broadcast_message(message: dict):
    try:
        db = next(get_db())
        users = db.query(User).all()
        
        for user in users:
            try:
                await bot.send_message(user.telegram_id, message["message"])
            except Exception as e:
                logging.error(f"Error sending message to user {user.telegram_id}: {e}")
        
        return {"message": "Сообщение успешно отправлено всем пользователям"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/users/export")
async def export_users():
    db = next(get_db())
    users = db.query(User).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Записываем заголовки
    writer.writerow(["ID", "Telegram ID", "Рост", "Вес", "Пол", "Возраст", 
                    "Цель", "Дата регистрации", "Подписка"])
    
    # Записываем данные пользователей
    for user in users:
        writer.writerow([
            user.id,
            user.telegram_id,
            user.height,
            user.weight,
            user.gender,
            user.age,
            user.goal,
            user.registration_date,
            "Активна" if user.is_subscribed else "Неактивна"
        ])
    
    output.seek(0)
    return StreamingResponse(
        io.StringIO(output.getvalue()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=users.csv"}
    )

@app.get("/webapp")
async def webapp(request: Request):
    return templates.TemplateResponse("webapp.html", {"request": request})

@app.get("/api/user/progress")
async def get_user_progress(request: Request):
    user_id = request.headers.get('X-Telegram-User-Id')
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    db = next(get_db())
    weight_records = (
        db.query(WeightRecord)
        .join(User)
        .filter(User.telegram_id == user_id)
        .order_by(WeightRecord.date)
        .all()
    )
    
    if not weight_records:
        return {
            "current_weight": 0,
            "weight_change": 0,
            "weight_history": {
                "dates": [],
                "weights": []
            }
        }
    
    return {
        "current_weight": weight_records[-1].weight,
        "weight_change": weight_records[-1].weight - weight_records[0].weight,
        "weight_history": {
            "dates": [record.date.strftime("%d.%m") for record in weight_records],
            "weights": [record.weight for record in weight_records]
        }
    }

@app.get("/api/user/nutrition")
async def get_nutrition_plan(request: Request):
    user_id = request.headers.get('X-Telegram-User-Id')
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    db = next(get_db())
    user = db.query(User).filter(User.telegram_id == user_id).first()
    
    today_plan = (
        db.query(NutritionPlan)
        .filter(NutritionPlan.user_id == user.id)
        .filter(NutritionPlan.date >= datetime.now().date())
        .first()
    )
    
    if not today_plan:
        return {"description": "План питания еще не сгенерирован"}
    
    return {
        "description": today_plan.meal_plan,
        "calories": today_plan.calories
    }

@app.get("/api/user/workout")
async def get_workout_plan(request: Request):
    user_id = request.headers.get('X-Telegram-User-Id')
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    db = next(get_db())
    user = db.query(User).filter(User.telegram_id == user_id).first()
    
    today_workout = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == user.id)
        .filter(WorkoutPlan.date >= datetime.now().date())
        .first()
    )
    
    if not today_workout:
        return {"description": "План тренировок еще не сгенерирован"}
    
    return {
        "description": today_workout.program,
        "difficulty": today_workout.difficulty
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 