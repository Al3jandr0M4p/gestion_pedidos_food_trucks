document.addEventListener("DOMContentLoaded", function () {
    const slider = document.querySelector(".slider__wrapper");
    let isDown = false;
    let startX;
    let scrollLeft;
    let autoScroll;
    let isMobile = window.innerWidth <= 768;

    // modal feedback
    const modal = document.getElementById('feedbackModal');

    // Verificar si debe mostrarse el modal (usando URLSearchParams)
    const urlParams = new URLSearchParams(window.location.search);
    const mostrarFeedback = urlParams.get('mostrar_feedback');
    const transaccionId = urlParams.get('transaccion_id');

    const feedbackFlag = localStorage.getItem('mostrar_feedback');

    if (mostrarFeedback === 'true' || feedbackFlag === 'true') {
        // si tenemos la transaccionId, lo asignamos al campo oculto
        if (transaccionId) {
            const transaccionInput = document.getElementById('transaccion_id');
            if (transaccionInput) {
                transaccionId.value = transaccionId;
            }
        }

        if (modal) {
            modal.style.display = 'flex';

            // limpiar el flag de localStorage despues de mostrar
            localStorage.removeItem('mostrar_feedback');
        }
    }

    // manejo del modal
    const closeButton = document.querySelector('#feedbackModal .close');
    if (closeButton) {
        closeButton.onclick = () => {
            modal.style.display = 'none';
        }
    }

    // cerrar modal al hacer clic fuera del contenido
    window.onclick = (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }

    // resto del codigo para el slider
    function startAutoScroll() {
        if (!isMobile) {
            autoScroll = setInterval(() => {
                if (slider.scrollLeft + slider.clientWidth >= slider.scrollWidth) {
                    slider.scrollLeft = 0;
                } else {
                    slider.scrollBy({ left: 120, behavior: "smooth" });
                }
            }, 3000);
        }
    }

    function stopAutoScroll() {
        clearInterval(autoScroll);
    }

    if (slider) {
        slider.addEventListener("touchstart", (e) => {
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

        slider.addEventListener("mousemove", (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - slider.offsetLeft;
            const walk = (x - startX) * 1.1;
            slider.scrollLeft = scrollLeft - walk;
        });
    
        startAutoScroll();
    }
});