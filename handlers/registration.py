from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.models import User
from services.calculator import calculate_bmr, calculate_daily_calories

class RegistrationStates(StatesGroup):
    waiting_for_height = State()
    waiting_for_weight = State()
    waiting_for_gender = State()
    waiting_for_age = State()
    waiting_for_goal = State()

async def start_registration(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Начать регистрацию")
    
    await message.answer(
        "Добро пожаловать в фитнес-бот! 🏃‍♂️\n"
        "Для начала работы необходимо пройти регистрацию.",
        reply_markup=keyboard
    )

async def request_height(message: types.Message):
    await RegistrationStates.waiting_for_height.set()
    await message.answer(
        "Введите ваш рост в сантиметрах (например: 175):",
        reply_markup=types.ReplyKeyboardRemove()
    )

async def process_height(message: types.Message, state: FSMContext):
    try:
        height = float(message.text)
        if 100 <= height <= 250:
            await state.update_data(height=height)
            await RegistrationStates.waiting_for_weight.set()
            await message.answer("Введите ваш вес в килограммах (например: 70):")
        else:
            await message.answer("Пожалуйста, введите корректный рост (от 100 до 250 см):")
    except ValueError:
        await message.answer("Пожалуйста, введите число:")

async def process_gender(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Мужской", "Женский")
    
    await RegistrationStates.waiting_for_gender.set()
    await message.answer(
        "Укажите ваш пол:",
        reply_markup=keyboard
    )

async def process_goal(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Похудение", "Поддержание веса", "Набор массы")
    
    await RegistrationStates.waiting_for_goal.set()
    await message.answer(
        "Выберите вашу цель:",
        reply_markup=keyboard
    )

def register_registration_handlers(dp: Dispatcher):
    dp.register_message_handler(start_registration, commands=["start"])
    dp.register_message_handler(request_height, text="Начать регистрацию", state="*")
    dp.register_message_handler(process_height, state=RegistrationStates.waiting_for_height)
    dp.register_message_handler(process_gender, state=RegistrationStates.waiting_for_gender)
    dp.register_message_handler(process_goal, state=RegistrationStates.waiting_for_goal) 