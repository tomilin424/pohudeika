from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from services.workout_service import WorkoutService
from database.models import WorkoutPlan
from database import get_db

class WorkoutStates(StatesGroup):
    waiting_for_level = State()
    waiting_for_days = State()

async def start_workout_planning(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Новичок", "Средний", "Продвинутый")
    
    await WorkoutStates.waiting_for_level.set()
    await message.answer(
        "Выберите ваш уровень подготовки:",
        reply_markup=keyboard
    )

async def process_level(message: types.Message, state: FSMContext):
    levels = {"Новичок": "начинающий", "Средний": "средний", "Продвинутый": "продвинутый"}
    if message.text not in levels:
        await message.answer("Пожалуйста, выберите уровень из предложенных вариантов")
        return

    await state.update_data(level=levels[message.text])
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("2", "3", "4", "5")
    
    await WorkoutStates.waiting_for_days.set()
    await message.answer(
        "Сколько дней в неделю вы готовы тренироваться?",
        reply_markup=keyboard
    )

async def process_days(message: types.Message, state: FSMContext):
    try:
        days = int(message.text)
        if not 2 <= days <= 5:
            await message.answer("Пожалуйста, выберите от 2 до 5 дней")
            return

        data = await state.get_data()
        workout_service = WorkoutService()
        
        # Получаем цель пользователя из базы данных
        db = next(get_db())
        user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
        
        workout_plan = await workout_service.generate_workout_plan(
            goal=user.goal,
            level=data['level'],
            days_per_week=days
        )

        # Сохраняем план тренировок в базу данных
        new_plan = WorkoutPlan(
            user_id=user.id,
            program=workout_plan,
            difficulty=data['level']
        )
        db.add(new_plan)
        db.commit()

        await message.answer(
            "Ваш план тренировок готов!\n\n" + workout_plan,
            reply_markup=types.ReplyKeyboardRemove()
        )
        await state.finish()

    except ValueError:
        await message.answer("Пожалуйста, введите число от 2 до 5")

def register_workout_handlers(dp: Dispatcher):
    dp.register_message_handler(start_workout_planning, commands=["workout"])
    dp.register_message_handler(process_level, state=WorkoutStates.waiting_for_level)
    dp.register_message_handler(process_days, state=WorkoutStates.waiting_for_days) 