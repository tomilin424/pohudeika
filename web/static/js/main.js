async function updateBotStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        document.getElementById('bot-status').textContent = data.status;
        document.getElementById('uptime').textContent = data.uptime;
        document.getElementById('active-users').textContent = data.active_users;
    } catch (error) {
        console.error('Error updating status:', error);
    }
}

async function restartBot() {
    if (confirm('Вы уверены, что хотите перезапустить бота?')) {
        try {
            const response = await fetch('/api/restart', { method: 'POST' });
            const data = await response.json();
            alert(data.message);
        } catch (error) {
            console.error('Error restarting bot:', error);
        }
    }
}

// Обновляем статус каждые 30 секунд
setInterval(updateBotStatus, 30000);
updateBotStatus(); 