async function viewUser(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        const user = await response.json();
        
        // Создаем модальное окно с информацией о пользователе
        const modal = new bootstrap.Modal(document.getElementById('userDetailsModal'));
        document.getElementById('userDetails').innerHTML = `
            <p><strong>ID:</strong> ${user.id}</p>
            <p><strong>Telegram ID:</strong> ${user.telegram_id}</p>
            <p><strong>Рост:</strong> ${user.height} см</p>
            <p><strong>Вес:</strong> ${user.weight} кг</p>
            <p><strong>Пол:</strong> ${user.gender}</p>
            <p><strong>Возраст:</strong> ${user.age}</p>
            <p><strong>Цель:</strong> ${user.goal}</p>
            <p><strong>Дата регистрации:</strong> ${new Date(user.registration_date).toLocaleDateString()}</p>
        `;
        modal.show();
    } catch (error) {
        console.error('Error fetching user details:', error);
    }
}

async function sendBroadcastMessage() {
    const messageText = document.getElementById('messageText').value;
    if (!messageText) {
        alert('Введите текст сообщения');
        return;
    }
    
    try {
        const response = await fetch('/api/broadcast', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: messageText })
        });
        
        const result = await response.json();
        alert(result.message);
        
        // Закрываем модальное окно
        const modal = bootstrap.Modal.getInstance(document.getElementById('sendMessageModal'));
        modal.hide();
    } catch (error) {
        console.error('Error sending broadcast:', error);
        alert('Ошибка при отправке сообщения');
    }
}

async function exportUsers() {
    try {
        const response = await fetch('/api/users/export');
        const blob = await response.blob();
        
        // Создаем ссылку для скачивания
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'users.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error exporting users:', error);
        alert('Ошибка при экспорте пользователей');
    }
} 