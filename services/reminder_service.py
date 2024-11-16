from datetime import datetime, timedelta
from aiogram import Bot
from database.models import User
from database import get_db

class ReminderService:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_weight_reminder(self):
        """Отправка напоминаний о необходимости взвешивания"""
        db = next(get_db())
        users = db.query(User).all()
        
        for user in users:
            last_weight = (
                db.query(WeightRecord)
                .filter(WeightRecord.user_id == user.id)
                .order_by(WeightRecord.date.desc())
                .first()
            )
            
            if not last_weight or (datetime.utcnow() - last_weight.date).days >= 7:
                await self.bot.send_message(
                    user.telegram_id,
                    "Не забудьте записать свой текущий вес! 📊\n"
                    "Используйте команду /weight для внесения данных."
                )

    async def send_workout_reminder(self):
        """Отправка напоминаний о тренировках"""
        db = next(get_db())
        users = db.query(User).all()
        
        for user in users:
            last_workout = (
                db.query(WorkoutPlan)
                .filter(WorkoutPlan.user_id == user.id)
                .order_by(WorkoutPlan.date.desc())
                .first()
            )
            
            if last_workout:
                await self.bot.send_message(
                    user.telegram_id,
                    "Не пропустите сегодняшнюю тренировку! 💪\n"
                    "Используйте команду /workout_today для просмотра программы."
                ) 