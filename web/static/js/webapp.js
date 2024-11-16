let tg = window.Telegram.WebApp;
tg.expand();

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', async () => {
    // Настраиваем основную кнопку Telegram
    tg.MainButton.setText('Обновить данные');
    tg.MainButton.onClick(loadUserProgress);
    
    // Устанавливаем цвета в соответствии с темой Telegram
    document.documentElement.style.setProperty('--tg-theme-bg-color', tg.backgroundColor);
    document.documentElement.style.setProperty('--tg-theme-text-color', tg.textColor);
    document.documentElement.style.setProperty('--tg-theme-button-color', tg.buttonColor);
    document.documentElement.style.setProperty('--tg-theme-button-text-color', tg.buttonTextColor);

    await loadUserProgress();
});

async function loadUserProgress() {
    try {
        const response = await fetch('/api/user/progress', {
            headers: {
                'X-Telegram-User-Id': tg.initDataUnsafe.user.id
            }
        });
        const data = await response.json();
        
        // Обновляем статистику
        updateStats(data);
        
        // Создаем график прогресса
        createProgressChart(data.weight_history);
        
        // Показываем основную кнопку
        tg.MainButton.show();
        
    } catch (error) {
        console.error('Error loading progress:', error);
        tg.showPopup({
            title: 'Ошибка',
            message: 'Не удалось загрузить данные о прогрессе',
            buttons: [{type: 'ok'}]
        });
    }
}

function updateStats(data) {
    document.getElementById('current-weight').textContent = 
        `${data.current_weight.toFixed(1)} кг`;
    
    const change = data.weight_change;
    const changeElement = document.getElementById('weight-change');
    changeElement.textContent = `${change > 0 ? '+' : ''}${change.toFixed(1)} кг`;
    changeElement.style.color = change > 0 ? '#ff4444' : '#00C851';
}

function createProgressChart(weightHistory) {
    const ctx = document.getElementById('progress-chart').getContext('2d');
    
    // Уничтожаем предыдущий график, если он существует
    if (window.progressChart) {
        window.progressChart.destroy();
    }
    
    window.progressChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: weightHistory.dates,
            datasets: [{
                label: 'Вес',
                data: weightHistory.weights,
                borderColor: tg.buttonColor || '#2481cc',
                backgroundColor: 'rgba(36, 129, 204, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            },
            interaction: {
                mode: 'index',
                intersect: false
            }
        }
    });
}

async function showNutritionPlan() {
    try {
        const response = await fetch('/api/user/nutrition', {
            headers: {
                'X-Telegram-User-Id': tg.initDataUnsafe.user.id
            }
        });
        const plan = await response.json();
        
        tg.showPopup({
            title: 'План питания на сегодня',
            message: plan.description,
            buttons: [{
                type: 'default',
                text: 'Понятно'
            }]
        });
    } catch (error) {
        console.error('Error loading nutrition plan:', error);
    }
}

async function showWorkoutPlan() {
    try {
        const response = await fetch('/api/user/workout', {
            headers: {
                'X-Telegram-User-Id': tg.initDataUnsafe.user.id
            }
        });
        const plan = await response.json();
        
        tg.showPopup({
            title: 'План тренировок на сегодня',
            message: plan.description,
            buttons: [{
                type: 'default',
                text: 'Понятно'
            }]
        });
    } catch (error) {
        console.error('Error loading workout plan:', error);
    }
}

function recordWeight() {
    tg.showPopup({
        title: 'Запись веса',
        message: 'Введите ваш текущий вес:',
        buttons: [
            {type: 'default', text: 'Отмена'},
            {type: 'ok', text: 'Сохранить'}
        ]
    }, async (buttonId) => {
        if (buttonId === 'ok') {
            // Здесь будет логика сохранения веса
            await loadUserProgress(); // Обновляем данные
        }
    });
}

function showProfile() {
    tg.showPopup({
        title: 'Мой профиль',
        message: 'Здесь будет информация о вашем профиле',
        buttons: [{type: 'ok'}]
    });
} 