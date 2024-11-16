import matplotlib.pyplot as plt
import io
from datetime import datetime, timedelta

async def generate_progress_graph(weight_records):
    """
    Генерация графика прогресса на основе записей веса
    """
    dates = [record.date for record in weight_records]
    weights = [record.weight for record in weight_records]
    
    plt.figure(figsize=(10, 6))
    plt.plot(dates, weights, marker='o')
    plt.title('График изменения веса')
    plt.xlabel('Дата')
    plt.ylabel('Вес (кг)')
    plt.grid(True)
    
    # Сохраняем график в байтовый буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    
    return buf 