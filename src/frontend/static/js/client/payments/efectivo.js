document.addEventListener("DOMContentLoaded", () => {
    const formEfectivo = document.getElementById("form-efectivo");
    const alertaPendiente = document.getElementById("alerta-pendiente");
    const btnConfirmar = document.getElementById("confirmar-pago");

    formEfectivo.addEventListener("submit", (e) => {
        e.preventDefault();
        alertaPendiente.style.display = "block";
        btnConfirmar.style.display = "block";
    });

    btnConfirmar.addEventListener("click", () => {
        localStorage.setItem("pago_confirmado", "true");
        localStorage.removeItem("carrito");
        alert("Pago en efectivo confirmado. Procesando pedido...");
        window.location.href = "/ver-carrito";
    });

    const montoAPagar = document.getElementById("monto-a-pagar");
    const montoHidden = document.getElementById("monto-hidden");

    setTimeout(() => {
        // Obtener total del localStorage
        const total = localStorage.getItem("total") || "0.00";
        console.log("Monto obtenido del localStorage:", total);
        // Mostrar el monto correctamente
        montoAPagar.textContent = `$${total}`;
        montoHidden.value = total;
    }, 500)
})