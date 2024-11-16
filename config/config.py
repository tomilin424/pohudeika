from dotenv import load_dotenv
import os

load_dotenv()

# Telegram Bot конфигурация
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBAPP_URL = os.getenv('VERCEL_URL', 'https://your-app.vercel.app')

# OpenAI конфигурация
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# База данных
DATABASE_URL = os.getenv('DATABASE_URL')

# Настройки подписки
SUBSCRIPTION_PRICE = 1000  # в рублях
FREE_TRIAL_DAYS = 7 