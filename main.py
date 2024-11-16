from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config.config import BOT_TOKEN
from services.reminder_service import ReminderService
from database import init_db
import asyncio
import logging
import aioschedule

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
reminder_service = ReminderService(bot)

async def scheduler():
    aioschedule.every().day.at("10:00").do(reminder_service.send_weight_reminder)
    aioschedule.every().day.at("08:00").do(reminder_service.send_workout_reminder)
    
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(3600)

async def on_startup(dp):
    logging.info('Инициализация базы данных...')
    init_db()
    logging.info('База данных инициализирована')
    
    logging.info('Запуск планировщика задач...')
    asyncio.create_task(scheduler())
    logging.info('Планировщик задач запущен')
    
    logging.info('Бот успешно запущен!')

if __name__ == '__main__':
    from handlers import register_all_handlers
    register_all_handlers(dp)
    
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True) 