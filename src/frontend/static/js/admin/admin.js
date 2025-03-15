document.addEventListener("DOMContentLoaded", () => {
    // Botón de menú responsivo
    const menuButton = document.createElement('button');
    menuButton.className = 'menu-toggle';
    menuButton.textContent = '☰';

    menuButton.onclick = () => {
        const menu = document.querySelector('.container__admin__configuration');
        menu?.classList.toggle('show');
    };

    document.body.appendChild(menuButton);

    const links = document.querySelectorAll('.links__admin a[data-url]');
    const mainContent = document.querySelector('.container__admin__content');

    links.forEach(link => {
        link.addEventListener("click", async (event) => {
            event.preventDefault();
            const url = link.getAttribute("data-url");

            try {
                const response = await fetch(url, {
                    headers: { "X-Requested-With": "XMLHttpRequest" }
                });
            
                if (!response.ok) {
                    throw new Error(`Error en la respuesta del servidor: ${response.statusText}`);
                }
            
                const contentType = response.headers.get("content-type");
                if (!contentType || !contentType.includes("text/html")) {
                    throw new Error(`Esperaba HTML, pero recibí ${contentType}`);
                }
            
                const content = await response.text();
                mainContent.innerHTML = content;
                history.pushState({ path: url }, "", url);
            } catch (error) {
                console.error("Error al cargar la sección:", error);
                mainContent.innerHTML = "<p>Error al cargar la sección.</p>";
            }
            
        });
    });

    window.addEventListener("popstate", async () => {
        const url = window.location.pathname;

        try {
            const response = await fetch(url, {
                headers: { "X-Requested-With": "XMLHttpRequest" }
            });

            if (!response.ok) throw new Error("Error al recargar la sección");

            const content = await response.text();
            mainContent.innerHTML = content;
        } catch (error) {
            console.error(error);
            mainContent.innerHTML = "<p>Error al recargar la sección.</p>";
        }
    });
});