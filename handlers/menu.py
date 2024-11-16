from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from handlers.subscription import check_subscription
from aiogram.types import WebAppInfo
from config.config import WEBAPP_URL

async def show_main_menu(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    # Добавляем кнопку для мини-приложения
    webapp_button = types.KeyboardButton(
        text="📱 Открыть приложение",
        web_app=WebAppInfo(url=f"{WEBAPP_URL}/webapp")
    )
    
    buttons = [
        "📊 Мой прогресс",
        "⚖️ Записать вес",
        "🏋️ Тренировки",
        "🍽 Питание",
        webapp_button,
        "ℹ️ Помощь"
    ]
    keyboard.add(*buttons)
    
    await message.answer(
        "Главное меню:\n"
        "Выберите нужный раздел или откройте приложение 👇",
        reply_markup=keyboard
    )

async def show_profile(message: types.Message):
    db = next(get_db())
    user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
    
    subscription_status = "Активна" if user.is_subscribed else "Неактивна"
    if user.is_subscribed:
        days_left = (user.subscription_end_date - datetime.utcnow()).days
        subscription_status += f" (осталось {days_left} дней)"
    
    profile_text = (
        f"👤 Ваш профиль:\n\n"
        f"Рост: {user.height} см\n"
        f"Текущий вес: {user.weight} кг\n"
        f"Пол: {user.gender}\n"
        f"Возраст: {user.age} лет\n"
        f"Цель: {user.goal}\n\n"
        f"Подписка: {subscription_status}"
    )
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("Изменить данные", callback_data="edit_profile"),
        types.InlineKeyboardButton("Продлить подписку", callback_data="extend_subscription")
    )
    
    await message.answer(profile_text, reply_markup=keyboard)

async def show_help(message: types.Message):
    help_text = (
        "🤖 Доступные команды:\n\n"
        "/start - Начать работу с ботом\n"
        "/menu - Главное меню\n"
        "/weight - Записать текущий вес\n"
        "/progress - Посмотреть прогресс\n"
        "/workout - Получить план тренировок\n"
        "/nutrition - Получить план питания\n"
        "/profile - Мой профиль\n"
        "/subscribe - Оформить подписку\n\n"
        "По всем вопросам обращайтесь к @admin"
    )
    await message.answer(help_text)

def register_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(show_main_menu, commands=["menu"])
    dp.register_message_handler(show_main_menu, text="🔙 Главное меню")
    dp.register_message_handler(show_profile, commands=["profile"])
    dp.register_message_handler(show_profile, text="👤 Мой профиль")
    dp.register_message_handler(show_help, commands=["help"])
    dp.register_message_handler(show_help, text="ℹ️ Помощь") 