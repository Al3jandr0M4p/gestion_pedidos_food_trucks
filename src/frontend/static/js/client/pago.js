let openModal = (id) => {
    document.getElementById(id).style.display = 'flex';

    if (id == "modalEfectivo") {
        setTimeout(() => {
            const total = localStorage.getItem("total") || "0.00";
            console.log("Monto obtenido del localStorage:", total);
            
            // Buscar elementos dentro del modal de efectivo
            const montoAPagar = document.querySelector("#modalEfectivo #monto-a-pagar");
            const montoHidden = document.querySelector("#modalEfectivo #monto-hidden");

            if (montoAPagar && montoHidden) {
                montoAPagar.textContent = `$${total}`;
                montoHidden.value = total;
            } else {
                console.error("No se encontraron los elementos para actualizar el monto en efectivo.");
            }
        }, 100);
    } else if (id == "modalTarjeta") {
        // Actualizar también el monto en el modal de tarjeta
        setTimeout(() => {
            const total = localStorage.getItem("total") || "0.00";
            const montoAPagar = document.querySelector("#modalTarjeta #monto-a-pagar");
            const montoHidden = document.querySelector("#modalTarjeta #monto-hidden");
            
            if (montoAPagar && montoHidden) {
                montoAPagar.textContent = `$${total}`;
                montoHidden.value = total;
            }
        }, 100);
    } else if (id == "modalTransferencia") {
        // Actualizar el monto en el modal de transferencia
        setTimeout(() => {
            const total = localStorage.getItem("total") || "0.00";
            const montoInput = document.querySelector("#modalTransferencia #monto");
            
            if (montoInput) {
                montoInput.value = total;
            }
        }, 100);
    }
}

let closeModal = (id) => {
    document.getElementById(id).style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    const stripeFormElement = document.getElementById('payment-form');
    const transferenciaFormElement = document.getElementById('transferencia-payment-form');

    const showLoadingIndicator = () => {
        document.getElementById('loading-indicator').style.display = 'block';
    };

    const hideLoadingIndicator = () => {
        document.getElementById('loading-indicator').style.display = 'none';
    };
    
    const handleResponse = (data) => {
        if (data.success) {
            window.location.href = data.redirect_url;
        } else {
            hideLoadingIndicator();
            console.log(data.message || 'Ocurrió un error al procesar el pago');
        }
    };
    
    const handleError = (error, metodo) => {
        hideLoadingIndicator();
        console.error(`Error en ${metodo}:`, error);
        console.log(`Ocurrió un error al procesar el pago por ${metodo}`);
    };
    
    if (stripeFormElement) {
        stripeFormElement.addEventListener('submit', function(event) {
            event.preventDefault();
            showLoadingIndicator();
            
            stripeFormElement.submit();
        });

    }
    
    if (transferenciaFormElement) {
        transferenciaFormElement.addEventListener('submit', function(event) {
            event.preventDefault();
            showLoadingIndicator();
            
            const carritoInput = document.getElementById('carrito-input');
            if (carritoInput) {
                carritoInput.value = localStorage.getItem('carrito') || '[]';
            }
            
            transferenciaFormElement.submit();
        });
    }
    
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            const activeModal = document.querySelector('.modal[style*="flex"]');
            if (activeModal) {
                const form = activeModal.querySelector('form');
                if (form) {
                    event.preventDefault();
                    form.dispatchEvent(new Event('submit'));
                }
            }
        }
    });
});