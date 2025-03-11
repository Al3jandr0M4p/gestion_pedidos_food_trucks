document.addEventListener("DOMContentLoaded", () => {
    const listaCarrito = document.getElementById("lista-carrito");
    const totalPrecio = document.getElementById("total-precio");
    const btnVaciar = document.getElementById("vaciar-carrito");
    const btnFinalizar = document.getElementById("finalizar-compra");

    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

    function actualizarCarrito() {
        listaCarrito.innerHTML = "";
        let total = 0;

        if (carrito.length === 0) {
            listaCarrito.innerHTML = "<p style='text-align: center;'>El carrito está vacío.</p>";
            totalPrecio.textContent = "$0.00";
            return;
        }

        carrito.forEach((producto, index) => {
            total += producto.precio * producto.cantidad;

            const item = document.createElement("div");
            item.classList.add("carrito-item");
            item.innerHTML = `
                <h2>${producto.nombre}</h2>
                <p>Precio: $${producto.precio.toFixed(2)}</p>
                <p>Cantidad: ${producto.cantidad}</p>
                <button class="eliminar" data-index="${index}">Eliminar</button>
            `;
            listaCarrito.appendChild(item);
        });

        totalPrecio.textContent = `$${total.toFixed(2)}`;

        document.querySelectorAll(".eliminar").forEach(boton => {
            boton.addEventListener("click", (e) => {
                const index = e.target.getAttribute("data-index");
                carrito.splice(index, 1);
                localStorage.setItem("carrito", JSON.stringify(carrito));
                actualizarCarrito();
            });
        });
    }

    btnVaciar.addEventListener("click", () => {
        carrito = [];
        localStorage.setItem("carrito", JSON.stringify(carrito));
        actualizarCarrito();
    });

    btnFinalizar.addEventListener("click", () => {
        if (carrito.length === 0) {
            alert("El carrito está vacío.");
            return;
        }

        let total = 0;
        carrito.forEach(function(producto) {
            total += (producto.precio * producto.cantidad);
        })

        let itbis = total * 0.18;
        let totalConItbis = total + itbis;

        localStorage.setItem("total", totalConItbis.toFixed(2));
        localStorage.setItem("itbis", itbis.toFixed(2));

        window.location.href = "/seleccionar-pago";
    });

    actualizarCarrito();
});