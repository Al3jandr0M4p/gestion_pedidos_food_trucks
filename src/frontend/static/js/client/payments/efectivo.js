document.addEventListener("DOMContentLoaded", () => {
    const formEfectivo = document.getElementById("form-efectivo");
    const alertaPendiente = document.getElementById("alerta-pendiente");
    const btnConfirmar = document.getElementById("confirmar-pago");
    const inputComprobante = document.getElementById("comprobante");

    formEfectivo.addEventListener("submit", (e) => {
        e.preventDefault();
        alertaPendiente.style.display = "block";
        btnConfirmar.style.display = "block";
    });

    btnConfirmar.addEventListener("click", async () => {
        const comprobante = inputComprobante.files[0];

        if (!comprobante) {
            Swal.fire({
                icon: "warning",
                title: "¡Comprobante necesario!",
                text: "Por favor sube el comprobante de pago para confirmar.",
                confirmButtonColor: "#3085d6"
            });
            return;
        }

        // Crear FormData para enviar el archivo
        const formData = new FormData();
        formData.append("comprobante", comprobante);
        formData.append("monto", document.getElementById("monto-hidden").value);
        formData.append("nombre", document.getElementById("nombre").value);

        // Enviar los datos al backend (ajustar la URL según corresponda)
        try {
            const response = await fetch("/confirmar-pago", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                localStorage.setItem("pago_confirmado", "true");
                localStorage.removeItem("carrito");

                Swal.fire({
                    title: "Pago confirmado",
                    text: "Pago en efectivo confirmado. Procesando pedido...",
                    icon: "success",
                    confirmButtonColor: "#3085d6",
                    confirmButtonText: "OK"
                }).then(() => {
                    window.location.href = "/ver-carrito"; // Redirigir a la página deseada
                });
            } else {
                throw new Error("Error al procesar el pago");
            }
        } catch (error) {
            Swal.fire({
                title: "Error",
                text: "Hubo un problema al procesar el pago. Intenta nuevamente.",
                icon: "error",
                confirmButtonColor: "#3085d6"
            });
        }
    });

    const montoAPagar = document.getElementById("monto-a-pagar");
    const montoHidden = document.getElementById("monto-hidden");

    setTimeout(() => {
        const total = localStorage.getItem("total") || "0.00";
        montoAPagar.textContent = `$${total}`;
        montoHidden.value = total;
    }, 500);
});