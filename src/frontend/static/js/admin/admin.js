document.addEventListener("DOMContentLoaded", () => {
    // Botón de menú responsivo
    const menuButton = document.createElement('button');
    menuButton.className = 'menu-toggle';
    menuButton.textContent = '☰';

    menuButton.onclick = () => {
        const menu = document.querySelector('.container__admin__configuration');
        menu.classList.toggle('show');
    };

    document.body.appendChild(menuButton);
});