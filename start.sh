#!/bin/bash

# Активируем виртуальное окружение
source venv/bin/activate

# Проверяем установлен ли ngrok
if ! command -v ngrok &> /dev/null; then
    echo "Установка ngrok..."
    sudo snap install ngrok
fi

# Проверяем наличие jq
if ! command -v jq &> /dev/null; then
    echo "Установка jq..."
    sudo apt-get install -y jq
fi

# Запускаем ngrok напрямую (без фонового режима для отладки)
echo "Запуск ngrok..."
ngrok http 8000 &
NGROK_PID=$!

# Ждем немного дольше, чтобы ngrok точно запустился
echo "Ожидание запуска ngrok..."
sleep 10

# Проверяем API ngrok
echo "Проверка API ngrok..."
TUNNELS_INFO=$(curl -s http://localhost:4040/api/tunnels)
echo "Информация о туннелях: $TUNNELS_INFO"

# Получаем URL от ngrok
NGROK_URL=$(echo $TUNNELS_INFO | jq -r '.tunnels[0].public_url')

if [ -z "$NGROK_URL" ] || [ "$NGROK_URL" = "null" ]; then
    echo "Ошибка: Не удалось получить URL от ngrok"
    echo "Проверьте, что:"
    echo "1. Вы установили authtoken командой: ngrok config add-authtoken ВАШ_ТОКЕН"
    echo "2. Порт 8000 не занят другими процессами"
    echo "3. У вас есть доступ к localhost:4040"
    
    # Показываем статус ngrok
    echo "Статус ngrok:"
    ps aux | grep ngrok
    
    # Убиваем процесс ngrok
    kill $NGROK_PID 2>/dev/null
    exit 1
fi

echo "Ngrok URL: $NGROK_URL"

# Обновляем URL в конфигурации бота
echo "WEBAPP_URL=$NGROK_URL" > .env
echo "BOT_TOKEN=5381880934:AAHOtgPW1S4cjs9PudZXmNHitMxmH-u0Jwk" >> .env
echo "OPENAI_API_KEY=your_openai_api_key" >> .env
echo "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fitness_bot" >> .env

# Запускаем бота в фоновом режиме
echo "Запуск бота..."
python main.py &
BOT_PID=$!

# Запускаем веб-интерфейс
echo "Запуск веб-интерфейса..."
python webapp.py

# При завершении останавливаем все процессы
trap 'kill $NGROK_PID; kill $BOT_PID' EXIT

# Деактивируем виртуальное окружение при выходе
trap 'deactivate' EXIT 