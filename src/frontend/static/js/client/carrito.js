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

        // Obtener la data carrito
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

    // vaciar el carrito
    btnVaciar.addEventListener("click", () => {
        Swal.fire({
            title: "Estas seguro?",
            text: "Se eliminaran todos los productos del carrito",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#d33",
            cancelButtonColor: "#3085d6",
            confirmButtonText: "si, vaciar",
            cancelButtonText: "no, cancelar"
        }).then((result) => {
            if (result.isConfirmed) {
                carrito = [];
                localStorage.setItem("carrito", JSON.stringify(carrito));
                actualizarCarrito();
                Swal.fire(
                    'Carrito vaciado!',
                    '',
                    'success'
                )
            }
        })
    });

    btnFinalizar.addEventListener("click", () => {
        if (carrito.length === 0) {
            Swal.fire({
                icon: "warning",
                title: "Carrito vacio",
                text: "Agrega productos antes de finalizar la compra.",
                confirmButtonColor: "#3085d6"
            })
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
        localStorage.setItem("carrito", JSON.stringify(carrito));
        sessionStorage.carrito = JSON.stringify(carrito);

        // redirijir a los metodos de pagos
        Swal.fire({
            title: "Procesando compra...",
            text: "Redirigiendo a metodos de pagos",
            icon: "success",
            timer: 2000,
            showConformButton: false
        }).then(() => {
            window.location.href = "/seleccionar-pago";
        });
    });

    // Actualizar el carrito
    actualizarCarrito();
});