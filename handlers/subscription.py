from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from datetime import datetime, timedelta
from database.models import User
from database import get_db
from config.config import SUBSCRIPTION_PRICE, FREE_TRIAL_DAYS

async def check_subscription(message: types.Message):
    db = next(get_db())
    user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
    
    if not user:
        await message.answer("Пожалуйста, сначала пройдите регистрацию /start")
        return False
        
    if user.is_subscribed:
        days_left = (user.subscription_end_date - datetime.utcnow()).days
        if days_left > 0:
            return True
            
    registration_days = (datetime.utcnow() - user.registration_date).days
    if registration_days <= FREE_TRIAL_DAYS:
        return True
        
    await message.answer(
        f"Для доступа к этой функции необходима подписка.\n"
        f"Стоимость: {SUBSCRIPTION_PRICE} руб/месяц\n"
        f"Для оформления используйте команду /subscribe"
    )
    return False

async def subscribe(message: types.Message):
    # Здесь должна быть интеграция с платежной системой
    # В данном примере просто имитируем успешную оплату
    
    db = next(get_db())
    user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
    
    if user.is_subscribed:
        await message.answer("У вас уже есть активная подписка!")
        return
        
    user.is_subscribed = True
    user.subscription_end_date = datetime.utcnow() + timedelta(days=30)
    db.commit()
    
    await message.answer(
        "Подписка успешно оформлена! 🎉\n"
        "Теперь вам доступны все функции бота на 30 дней."
    )

def register_subscription_handlers(dp: Dispatcher):
    dp.register_message_handler(subscribe, commands=["subscribe"]) 