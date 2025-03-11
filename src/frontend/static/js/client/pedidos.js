document.addEventListener("DOMContentLoaded", () => {
    const carrito = JSON.parse(localStorage.getItem("carrito")) || [];

    document.querySelectorAll(".agregar__carrito").forEach(boton => {
        boton.addEventListener("click", (e) => {
            const id = e.target.getAttribute("data-id");
            const nombre = e.target.getAttribute("data-nombre");
            const precio = parseFloat(e.target.getAttribute("data-precio"));

            const producto = { id, nombre, precio, cantidad: 1 };

            const index = carrito.findIndex(p => p.id === id);
            if (index !== -1) {
                carrito[index].cantidad++;
            } else {
                carrito.push(producto);
            }

            // Guardar carrito en localStorage
            localStorage.setItem("carrito", JSON.stringify(carrito));

            // Actualizar el contador del carrito
            actualizarCarrito();

            // Mostrar alerta
            const alert = document.getElementById('cartAlert');
            alert.classList.add('show');

            setTimeout(() => {
                alert.classList.remove('show');
                document.querySelector('.fa-cart-shopping').parentElement.classList.remove('cart-pulse');
            }, 2000);
        });
    });

    // Función para actualizar el contador del carrito
    function actualizarCarrito() {
        const carrito = JSON.parse(localStorage.getItem("carrito")) || [];
        const totalItems = carrito.reduce((acc, producto) => acc + producto.cantidad, 0);

        const carritoIcon = document.querySelector(".fa-cart-shopping");
        carritoIcon.setAttribute("data-count", totalItems);
    }

    // Inicializar el contador del carrito al cargar la página
    actualizarCarrito();
});
