document.addEventListener('DOMContentLoaded', function() {
    // Selectores - Añade verificaciones
    const notificationDropdown = document.getElementById('notifDropdown');
    const notificationCount = document.querySelector('.notification');
    const notificationCenter = document.querySelector('.notif-center');
    const markAllReadLink = document.querySelector('.see-all');

    // Verificar que los elementos existan
    if (!notificationCount || !notificationCenter) {
        console.error('No se encontraron elementos de notificación');
        return;
    }

    // Escape HTML para prevenir XSS
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // Fetch notifications
    function fetchNotifications() {
        // IMPORTANTE: URL EXACTA de tu vista de notificaciones
        const notificationsUrl = "{% url 'notifications' %}";  // Usar template tag de Django

        fetch(notificationsUrl, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => {
            if (!response.ok) {
                if (response.status === 403) {
                    throw new Error('No autorizado. Por favor inicie sesión.');
                }
                throw new Error('Error al cargar notificaciones');
            }
            return response.json();
        })
        .then(data => {
            // Actualizar contador de notificaciones
            notificationCount.textContent = data.count || '0';
            
            // Limpiar notificaciones existentes
            notificationCenter.innerHTML = '';

            // Mostrar notificaciones
            if (!data.notifications || data.notifications.length === 0) {
                notificationCenter.innerHTML = `
                    <div class="text-center py-3 text-muted">
                        No hay notificaciones nuevas
                    </div>
                `;
            } else {
                data.notifications.forEach(notification => {
                    const notificationItem = document.createElement('div');
                    notificationItem.classList.add('notif-item');
                    notificationItem.innerHTML = `
                        <div class="notif-icon">
                            <i class="fa ${escapeHtml(notification.icon || 'fa-bell')}"></i>
                        </div>
                        <div class="notif-content">
                            <span class="subject">${escapeHtml(notification.message)}</span>
                            <span class="time">${escapeHtml(notification.created_at || '')}</span>
                        </div>
                    `;
                    notificationCenter.appendChild(notificationItem);
                });
            }
        })
        .catch(error => {
            console.error('Error fetching notifications:', error);
            notificationCenter.innerHTML = `
                <div class="text-center py-3 text-danger">
                    ${error.message}
                </div>
            `;
        });
    }

    // Marcar todas las notificaciones como leídas
    function markAllNotificationsRead() {
        const notificationsUrl = "{% url 'notifications' %}";

        fetch(notificationsUrl, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                notificationCount.textContent = '0';
                notificationCenter.innerHTML = `
                    <div class="text-center py-3 text-muted">
                        Todas las notificaciones marcadas como leídas
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('Error marcando notificaciones:', error);
        });
    }

    // Fetch notifications on page load
    fetchNotifications();

    // Periodically refresh notifications (every 2 minutes)
    setInterval(fetchNotifications, 120000);

    // Add event listener to mark all as read
    if (markAllReadLink) {
        markAllReadLink.addEventListener('click', markAllNotificationsRead);
    }
});