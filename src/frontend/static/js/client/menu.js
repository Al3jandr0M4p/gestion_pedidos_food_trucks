document.addEventListener("DOMContentLoaded", () => {
    const slider = document.querySelector(".slider__wrapper");
    let isDown = false;
    let startX;
    let scrollLeft;
    let autoScroll;
    let isMobile = window.innerWidth <= 768;

    // resto del codigo para el slider
    let startAutoScroll = () => {
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

    let stopAutoScroll = () => {
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