document.addEventListener("DOMContentLoaded", () => {
    const montoAPagar = document.getElementById("monto-a-pagar");
    const montoHidden = document.getElementById("monto-hidden");

    // Cargar el total desde localStorage
    const total = localStorage.getItem("total") || "0.00";
    montoAPagar.textContent = `$${total}`;
    montoHidden.value = total;

    // Configurar Stripe
    const stripe = Stripe('pk_test_51R1rahC8mDrO4oITEAe4lbHFYbySRp025uY4iwDXuNktd98M5UEZcFuNtFeahByR3NXLuYc0FWB0s5mFyFpsSYcL00VmEPiwKY');
    const elements = stripe.elements();
    const card = elements.create('card');
    card.mount('#card-element');

    card.addEventListener('change', function(e) {
        const displayError = document.getElementById('card-errors');
        if (e.error) {
            displayError.textContent = e.error.message;
        } else {
            displayError.textContent = '';
        }
    });

    const form = document.getElementById('payment-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // Desactivar el botón para evitar múltiples envíos
        const submitButton = document.querySelector('#payment-form button[type="submit"]');
        submitButton.disabled = true;

        stripe.createToken(card).then(function(result) {
            console.log("Stripe token creado: ", result);

            if (result.error) {
                // Reactivar el botón si hay error
                submitButton.disabled = false;
                const errorElement = document.getElementById('card-errors');
                errorElement.textContent = result.error.message;
            } else {
                console.log("Token generado:", result.token.id);
                // Agregar token a la forma
                const hiddenInput = document.createElement('input');
                hiddenInput.setAttribute('type', 'hidden');
                hiddenInput.setAttribute('name', 'stripeToken');
                hiddenInput.setAttribute('value', result.token.id);
                form.appendChild(hiddenInput);

                const carritoInput = document.createElement('input');
                carritoInput.setAttribute('type', 'hidden');
                carritoInput.setAttribute('name', 'carrito');
                carritoInput.setAttribute('value', localStorage.getItem('carrito'));
                form.appendChild(carritoInput);

                console.log("Token que se va a enviar:", hiddenInput.value);

                // Enviar el formulario
                console.log('Enviando formulario de pago con tarjeta');
                form.submit();
            }
        }).catch(function(error) {
            console.log("Stripe token error en la creacion: ", error);
            submitButton.disabled = false;
        });
    });
});