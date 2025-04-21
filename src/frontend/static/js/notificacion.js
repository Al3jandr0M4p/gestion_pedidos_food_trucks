const notificationContainer = document.createElement('div');
notificationContainer.className = "notification-container";
document.body.appendChild(notificationContainer);

function showNotification(icon, message, className) {
    const notification = document.createElement('div');
    notification.className = className;
    notification.innerHTML = `<span class="icon">${icon}</span> <span>${message}</span>`;

    notificationContainer.appendChild(notification);

    setTimeout(() => {
        notification.style.opacity = "0";
        setTimeout(() => notification.remove(), 550);
    }, 3000);
}

document.addEventListener("DOMContentLoaded", function () {
    const messages = document.querySelectorAll('#flash-messages li');
    const currentLocation = document.querySelector('meta[name="current-location"]').getAttribute('content');

    messages.forEach((msg) => {
        const messageText = msg.innerText;
        const category = msg.dataset.category;
        const messageLocation = msg.dataset.location;

        if (messageLocation !== currentLocation) return;

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
})