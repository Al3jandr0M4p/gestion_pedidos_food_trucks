document.addEventListener("DOMContentLoaded", () => {
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

    window.addEventListener("resize", updateIsMobile);
});