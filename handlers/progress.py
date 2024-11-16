from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.models import WeightRecord, User
from database import get_db
from utils.helpers import generate_progress_graph
from datetime import datetime

class WeightState(StatesGroup):
    waiting_for_weight = State()

async def start_weight_record(message: types.Message):
    await WeightState.waiting_for_weight.set()
    await message.answer(
        "Введите ваш текущий вес в килограммах (например: 70.5):"
    )

async def process_weight(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text)
        if not 30 <= weight <= 250:
            await message.answer("Пожалуйста, введите корректный вес (от 30 до 250 кг)")
            return

        db = next(get_db())
        user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
        
        # Записываем новый вес
        new_weight = WeightRecord(
            user_id=user.id,
            weight=weight
        )
        db.add(new_weight)
        db.commit()

        # Получаем историю веса для построения графика
        weight_records = (
            db.query(WeightRecord)
            .filter(WeightRecord.user_id == user.id)
            .order_by(WeightRecord.date)
            .all()
        )

        if len(weight_records) > 1:
            # Генерируем график прогресса
            graph_buf = await generate_progress_graph(weight_records)
            
            # Вычисляем изменение веса
            total_change = weight_records[-1].weight - weight_records[0].weight
            
            await message.answer_photo(
                graph_buf,
                caption=f"Вес успешно записан! 📊\n"
                        f"Общее изменение веса: {total_change:+.1f} кг"
            )
        else:
            await message.answer(
                "Вес успешно записан! 📊\n"
                "График прогресса будет доступен после нескольких записей."
            )

        await state.finish()

    except ValueError:
        await message.answer("Пожалуйста, введите число (например: 70.5)")

async def show_progress(message: types.Message):
    db = next(get_db())
    user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
    
    weight_records = (
        db.query(WeightRecord)
        .filter(WeightRecord.user_id == user.id)
        .order_by(WeightRecord.date)
        .all()
    )
    
    if len(weight_records) < 2:
        await message.answer(
            "Для отображения прогресса необходимо минимум две записи веса.\n"
            "Используйте команду /weight для внесения данных."
        )
        return

    graph_buf = await generate_progress_graph(weight_records)
    total_change = weight_records[-1].weight - weight_records[0].weight
    days = (weight_records[-1].date - weight_records[0].date).days
    
    await message.answer_photo(
        graph_buf,
        caption=f"📊 Ваш прогресс за {days} дней:\n"
                f"Начальный вес: {weight_records[0].weight:.1f} кг\n"
                f"Текущий вес: {weight_records[-1].weight:.1f} кг\n"
                f"Общее изменение: {total_change:+.1f} кг"
    )

def register_progress_handlers(dp: Dispatcher):
    dp.register_message_handler(start_weight_record, commands=["weight"])
    dp.register_message_handler(process_weight, state=WeightState.waiting_for_weight)
    dp.register_message_handler(show_progress, commands=["progress"]) 