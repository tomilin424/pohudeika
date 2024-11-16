let tg = window.Telegram.WebApp;
tg.expand();

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', async () => {
    await loadUserProgress();
});

async function loadUserProgress() {
    try {
        const response = await fetch('/api/user/progress');
        const data = await response.json();
        
        // Обновляем текущий вес и изменение
        document.getElementById('current-weight').textContent = data.current_weight;
        document.getElementById('weight-change').textContent = 
            (data.weight_change > 0 ? '+' : '') + data.weight_change;
        
        // Создаем график прогресса
        createProgressChart(data.weight_history);
    } catch (error) {
        console.error('Error loading progress:', error);
    }
}

function createProgressChart(weightHistory) {
    const ctx = document.getElementById('progress-chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: weightHistory.dates,
            datasets: [{
                label: 'Вес',
                data: weightHistory.weights,
                borderColor: '#4CAF50',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

async function showNutritionPlan() {
    try {
        const response = await fetch('/api/user/nutrition');
        const plan = await response.json();
        tg.showPopup({
            title: 'План питания на сегодня',
            message: plan.description,
            buttons: [{
                type: 'default',
                text: 'Закрыть'
            }]
        });
    } catch (error) {
        console.error('Error loading nutrition plan:', error);
    }
}

async function showWorkoutPlan() {
    try {
        const response = await fetch('/api/user/workout');
        const plan = await response.json();
        tg.showPopup({
            title: 'План тренировок на сегодня',
            message: plan.description,
            buttons: [{
                type: 'default',
                text: 'Закрыть'
            }]
        });
    } catch (error) {
        console.error('Error loading workout plan:', error);
    }
} 