from aiogram import types, Dispatcher
from services.nutrition_service import NutritionService
from database import get_db
from database.models import User, NutritionPlan
from datetime import datetime

async def show_nutrition_plan(message: types.Message):
    db = next(get_db())
    user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
    
    # Получаем или генерируем план питания
    today_plan = (
        db.query(NutritionPlan)
        .filter(NutritionPlan.user_id == user.id)
        .filter(NutritionPlan.date >= datetime.now().date())
        .first()
    )
    
    if not today_plan:
        nutrition_service = NutritionService()
        plan = await nutrition_service.generate_meal_plan(
            calories=user.daily_calories,
            goal=user.goal
        )
        
        today_plan = NutritionPlan(
            user_id=user.id,
            calories=user.daily_calories,
            meal_plan=plan
        )
        db.add(today_plan)
        db.commit()
    
    # Отправляем план пользователю
    await message.answer(
        f"🍽 Ваш план питания на сегодня:\n\n"
        f"Целевые калории: {today_plan.calories} ккал\n\n"
        f"{today_plan.meal_plan}"
    )

def register_nutrition_handlers(dp: Dispatcher):
    dp.register_message_handler(show_nutrition_plan, text="🍽 Питание") 