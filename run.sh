#!/bin/bash

# Активируем виртуальное окружение
source venv/bin/activate

# Проверяем наличие необходимых пакетов
if ! pip freeze | grep -q "aiogram"; then
    echo "Установка зависимостей..."
    pip install -r requirements.txt
fi

# Запускаем бота в фоновом режиме
python main.py &
BOT_PID=$!

# Запускаем веб-интерфейс
python webapp.py

# При завершении скрипта останавливаем бота
kill $BOT_PID

# Деактивируем виртуальное окружение
deactivate 