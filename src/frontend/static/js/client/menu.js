const notificationTime = 15000;

function showNotificationBot(message) {
    const notification = document.getElementById('notification');
    const msg = document.getElementById('notification-message');

    msg.textContent = message;
    notification.classList.remove('hidden');
    notification.classList.add('show');

    console.log('Notificación mostrada: ', message);

    setTimeout(() => {
        notification.classList.remove('show');
        notification.classList.add('hidden');
    }, notificationTime);
}

let isNotifying = false;

function showBotNotification(mensajes) {
    if (isNotifying || mensajes.length === 0) return;

    isNotifying = true;
    let i = 0;

    const mostrarSiguiente = () => {
        if (i < mensajes.length) {
            showNotificationBot(mensajes[i]);
            console.log('Notificación enviada: ', mensajes[i]);
            i++;
            setTimeout(mostrarSiguiente, notificationTime + 2000);
        } else {
            isNotifying = false;
        }
    };
    mostrarSiguiente();
}

let notificacionesRecientes = [];

function obtenerYMostrarNotificaciones() {
    fetch('/notificaciones')
        .then(res => res.json())
        .then(mensajes => {
            const nuevos = mensajes.filter(msg => !notificacionesRecientes.includes(msg));

            if (nuevos.length > 0) {
                showBotNotification(mensajes);
                notificacionesRecientes = [...notificacionesRecientes, ...nuevos].slice(-80);
            }
        })
        .catch(err => console.log("Error al obtener notificaciones del bot:", err));
}

setInterval(obtenerYMostrarNotificaciones, 25000);

document.addEventListener("DOMContentLoaded", () => {
    obtenerYMostrarNotificaciones();

    const chatHeader = document.getElementById('chat-header');
    const chatBody = document.getElementById('chat-body');
    const chatInput = document.getElementById('chat-input');
    const chatToggle = document.getElementById('chat-toggle');
    const userMessageInput = document.getElementById('user-message');
    const sendMessageButton = document.getElementById('send-message');
    const slider = document.querySelector(".slider__wrapper");
    let isDown = false;
    let startX = 0;
    let scrollLeft = 0;
    let autoScroll = null;
    let isMobile = window.innerWidth <= 768;

    const updateIsMobile = () => {
        isMobile = window.innerWidth <= 768;
        if (isMobile) stopAutoScroll();
        else startAutoScroll();
    }

    const startAutoScroll = () => {
        stopAutoScroll(); // por si ya hay uno corriendo
        if (!isMobile && slider) {
            autoScroll = setInterval(() => {
                if (slider.scrollLeft + slider.clientWidth >= slider.scrollWidth) {
                    slider.scrollLeft = 0;
                } else {
                    slider.scrollBy({ left: 120, behavior: "smooth" });
                }
            }, 3000);
        }
    }

    const stopAutoScroll = () => {
        if (autoScroll) {
            clearInterval(autoScroll);
            autoScroll = null;
        }
    }

    if (slider) {
        slider.addEventListener("touchstart", (e) => {
            stopAutoScroll();
            isDown = true;
            startX = e.touches[0].pageX - slider.offsetLeft;
            scrollLeft = slider.scrollLeft;
        });

        slider.addEventListener("touchmove", (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.touches[0].pageX - slider.offsetLeft;
            const walk = (x - startX) * 1.1;
            slider.scrollLeft = scrollLeft - walk;
        });

        slider.addEventListener("touchend", () => {
            isDown = false;
            if (!isMobile) setTimeout(startAutoScroll, 5000);
        });

        slider.addEventListener("mousedown", (e) => {
            stopAutoScroll();
            isDown = true;
            startX = e.pageX - slider.offsetLeft;
            scrollLeft = slider.scrollLeft;
        });

        slider.addEventListener("mouseup", () => {
            isDown = false;
            if (!isMobile) setTimeout(startAutoScroll, 5000);
        });

        slider.addEventListener("mouseleave", () => {
            isDown = false;
        });

        slider.addEventListener("mousemove", (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - slider.offsetLeft;
            const walk = (x - startX) * 1.1;
            slider.scrollLeft = scrollLeft - walk;
        });

        startAutoScroll();
    }

    // Toggle chat open/close
    chatHeader.addEventListener('click', () => {
        chatBody.classList.toggle('active');
        chatInput.classList.toggle('active');

        // Update toggle icon
        if (chatBody.classList.contains('active')) {
            chatToggle.textContent = '👆';
        } else {
            chatToggle.textContent = '👇';
        }
    });

    // Function to add messages to chat
    function addMessage(message, isUser = false) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(isUser ? 'user-message' : 'bot-message');
        messageElement.textContent = message;

        chatBody.appendChild(messageElement);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // Send message on button click
    sendMessageButton.addEventListener('click', sendMessage);

    // Send message on Enter key
    userMessageInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Send message function
    function sendMessage() {
        const message = userMessageInput.value.trim();
        if (!message) return;

        // Display user message
        addMessage(message, true);
        userMessageInput.value = '';

        // Send to chatbot API
        fetch('/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mensaje: message
            })
        })
            .then(response => response.json())
            .then(data => {
                // Display bot response
                addMessage(data.respuesta);
            })
            .catch(error => {
                console.error('Error comunicándose con el chatbot:', error);
                addMessage('Lo siento, tuve un problema al procesar tu mensaje. Por favor intenta de nuevo.');
            });
    }

    // Automatically show sample response on first load
    setTimeout(() => {
        fetch('/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mensaje: "¿Qué me recomiendas hoy?"
            })
        })
            .then(response => response.json())
            .then(data => {
                // Save this for future display if user opens chat
                window.recommendationResponse = data.respuesta;
            })
            .catch(err => console.log("Error al obtener recomendación inicial:", err));
    }, 3000);

    window.addEventListener("resize", updateIsMobile);
});