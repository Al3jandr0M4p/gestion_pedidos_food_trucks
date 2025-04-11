document.addEventListener('DOMContentLoaded', function() {
    console.log("JS de notificacion cargado");
    const messages = document.querySelectorAll('#flash-messages li');
    const notificationContainer = document.createElement('div');
    notificationContainer.className = "notification-container";
    document.body.appendChild(notificationContainer);

    let showNotification = (icon, message, className) => {
        const notification = document.createElement('div');
        notification.className = className;
        notification.innerHTML = `<span class="icon">${icon}</span> <span>${message}</span>`;

        notificationContainer.appendChild(notification);

        setTimeout(() => {
            notification.style.opacity = "0";
            setTimeout(() => notification.remove(), 500);
        }, 3000);
    }

    messages.forEach((msg) => {
        const messageText = msg.innerText;
        const category = msg.dataset.category;

        let icon = "";
        let className = "notification";

        if (category === "success") {
            icon = "✔️";
            className += " success";
        } else if (category === "error") {
            icon = "❌";
            className += " error";
        }

        showNotification(icon, messageText, className);
    });
});