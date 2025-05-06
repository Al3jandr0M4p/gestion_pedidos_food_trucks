// Función para abrir modales
let openModal = (id) => {
    document.getElementById(id).style.display = 'flex';

    // Asegurarse de que el monto se establece correctamente en cada modal
    setTimeout(() => {
        const total = localStorage.getItem("total") || "0.00";
        console.log(`Actualizando monto en modal ${id}: ${total}`);
        
        if (id === "modalEfectivo") {
            const montoAPagar = document.querySelector("#modalEfectivo #monto-a-pagar");
            const montoHidden = document.querySelector("#modalEfectivo #monto-hidden");

            if (montoAPagar && montoHidden) {
                montoAPagar.textContent = `$${total}`;
                montoHidden.value = total;
            } else {
                console.error("No se encontraron los elementos para actualizar el monto en efectivo.");
            }
        } else if (id === "modalTarjeta") {
            const montoAPagar = document.querySelector("#modalTarjeta #monto-a-pagar");
            const montoHidden = document.querySelector("#modalTarjeta #monto-hidden");
            
            if (montoAPagar && montoHidden) {
                montoAPagar.textContent = `$${total}`;
                montoHidden.value = total;
            } else {
                console.error("No se encontraron los elementos para actualizar el monto en tarjeta.");
            }
        } else if (id === "modalTransferencia") {
            const montoInput = document.querySelector("#modalTransferencia #monto");
            
            if (montoInput) {
                montoInput.value = total;
            } else {
                console.error("No se encontró el elemento para actualizar el monto en transferencia.");
            }
        }
    }, 100);
}

// Función para cerrar modales
let closeModal = (id) => {
    document.getElementById(id).style.display = 'none';
}

// Variable global para el elemento de tarjeta
let cardElement = null;
// Variable global para stripe
let stripeInstance = null;
// Flag para evitar envíos múltiples
let isSubmitting = false;
// Variable para elementos de Stripe
let elements = null;

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM cargado completamente");
    
    // Inicializar Stripe una sola vez
    try {
        stripeInstance = Stripe('pk_test_51R1rahC8mDrO4oITEAe4lbHFYbySRp025uY4iwDXuNktd98M5UEZcFuNtFeahByR3NXLuYc0FWB0s5mFyFpsSYcL00VmEPiwKY');
        console.log("Stripe inicializado correctamente");
    } catch (error) {
        console.error("Error al inicializar Stripe:", error);
    }
    
    // Configurar los formularios primero antes de instanciar el elemento de tarjeta
    setupForms();
    
    // Verificar si estamos en la página de tarjetas y configurar Stripe
    const cardContainer = document.getElementById('card-element');
    if (cardContainer && stripeInstance) {
        console.log("Configurando Stripe Elements...");
        try {
            // Crear elementos una sola vez
            elements = stripeInstance.elements();
            
            // Almacenar el elemento de tarjeta en la variable global
            cardElement = elements.create('card');
            cardElement.mount('#card-element');

            cardElement.addEventListener('change', function(e) {
                const displayError = document.getElementById('card-errors');
                if (displayError) {
                    if (e.error) {
                        displayError.textContent = e.error.message;
                    } else {
                        displayError.textContent = '';
                    }
                }
            });
            console.log("Stripe Elements configurado correctamente");
        } catch (error) {
            console.error("Error al configurar Stripe Elements:", error);
        }
    }
    
    // Función para configurar los formularios
    function setupForms() {
        // Referencias a los formularios
        const stripeFormElement = document.getElementById('payment-form');
        const transferenciaFormElement = document.getElementById('transferencia-payment-form');

        // Manejar el formulario de tarjeta
        if (stripeFormElement) {
            console.log("Formulario de pago con tarjeta encontrado");
            
            // NO clonar el formulario para no perder la referencia al elemento card-element
            // Simplemente añadir el event listener
            stripeFormElement.addEventListener('submit', function(event) {
                console.log("Formulario de tarjeta enviado");
                event.preventDefault();
                
                // Evitar múltiples envíos
                if (isSubmitting) {
                    console.log("Envío ya en proceso, ignorando clic adicional");
                    return;
                }
                
                submitCardPayment(stripeFormElement);
            });
        } else {
            console.warn("No se encontró el formulario de pago con tarjeta");
        }
        
        // Manejar el formulario de transferencia
        if (transferenciaFormElement) {
            transferenciaFormElement.addEventListener('submit', function(event) {
                event.preventDefault();
                
                // Evitar múltiples envíos
                if (isSubmitting) {
                    console.log("Envío ya en proceso, ignorando clic adicional");
                    return;
                }
                
                submitTransferPayment(transferenciaFormElement);
            });
        }
        
        // Manejar la tecla Enter en cualquier modal activo con protección contra envíos múltiples
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' && !isSubmitting) {
                const activeModal = document.querySelector('.modal[style*="flex"]');
                if (activeModal) {
                    const form = activeModal.querySelector('form');
                    if (form) {
                        console.log("Tecla Enter detectada en modal, enviando formulario");
                        event.preventDefault();
                        form.dispatchEvent(new Event('submit'));
                    }
                }
            }
        });
    }
});

// Funciones de indicador de carga
const showLoadingIndicator = () => {
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.style.display = 'block';
    }
};

const hideLoadingIndicator = () => {
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.style.display = 'none';
    }
};

// Función para procesar el pago con tarjeta
function submitCardPayment(formElement) {
    // Establecer flag para evitar envíos múltiples
    isSubmitting = true;
    showLoadingIndicator();
    
    // Desactivar el botón para evitar múltiples envíos
    const submitButton = formElement.querySelector('button[type="submit"]');
    if (submitButton) submitButton.disabled = true;
    
    console.log("Procesando pago con tarjeta...");
    
    try {
        // Verificar si Stripe está disponible
        if (!stripeInstance) {
            console.error("Error: Stripe no está inicializado");
            alert("Error: El procesador de pagos no está disponible. Por favor, recarga la página.");
            hideLoadingIndicator();
            if (submitButton) submitButton.disabled = false;
            isSubmitting = false;
            return;
        }
        
        // Usar la variable global cardElement
        if (!cardElement) {
            console.error("Error: No se encontró el elemento de tarjeta");
            alert("Error: Información de tarjeta no inicializada. Por favor, recarga la página.");
            hideLoadingIndicator();
            if (submitButton) submitButton.disabled = false;
            isSubmitting = false;
            return;
        }
        
        // Obtener datos adicionales del formulario que puedan ser necesarios
        const nombreInput = document.getElementById('nombre');
        const emailInput = document.getElementById('email');
        
        // Preparar datos de facturación (opcional)
        let billingDetails = {};
        
        if (nombreInput && nombreInput.value) {
            billingDetails.name = nombreInput.value;
        }
        
        if (emailInput && emailInput.value) {
            billingDetails.email = emailInput.value;
        }
        
        // Generar el token de Stripe con detalles adicionales si están disponibles
        let tokenOptions = {};
        if (Object.keys(billingDetails).length > 0) {
            tokenOptions.billing_details = billingDetails;
        }
        
        console.log("Generando token con estos detalles:", tokenOptions);
        
        // Verificar que el elemento de tarjeta aún está montado
        const cardElementContainer = document.getElementById('card-element');
        if (!cardElementContainer) {
            console.error("Error: El contenedor del elemento de tarjeta ya no existe en el DOM");
            alert("Error: La información de la tarjeta no está disponible. Por favor, recarga la página.");
            hideLoadingIndicator();
            if (submitButton) submitButton.disabled = false;
            isSubmitting = false;
            return;
        }
        
        // Generar el token de Stripe
        stripeInstance.createToken(cardElement, tokenOptions).then(function(result) {
            console.log("Respuesta de Stripe:", result);
            
            if (result.error) {
                // Mostrar el error al usuario
                const errorElement = document.getElementById('card-errors');
                if (errorElement) {
                    errorElement.textContent = result.error.message;
                }
                console.error("Error al crear token:", result.error.message);
                hideLoadingIndicator();
                if (submitButton) submitButton.disabled = false;
                isSubmitting = false;
            } else {
                console.log("Token generado exitosamente:", result.token.id);
                
                // Preparar los datos para el envío
                const formData = new FormData(formElement);
                formData.append('stripeToken', result.token.id);
                formData.append('carrito', localStorage.getItem('carrito') || '[]');
                formData.append('monto', localStorage.getItem('total') || '0.00');
                
                // Opcional: Agregar estos datos para debugging en el backend
                formData.append('device_info', navigator.userAgent);
                
                console.log("Enviando datos al servidor...");
                
                // Enviar los datos mediante fetch en lugar de enviar el formulario directamente
                fetch(formElement.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Error HTTP: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Respuesta del servidor:", data);
                    if (data.success) {
                        // Limpiar localStorage después del pago exitoso
                        localStorage.removeItem('carrito');
                        localStorage.removeItem('total');
                        
                        // Redirigir a la página de éxito o mostrar mensaje
                        window.location.href = data.redirect || '/pago-exitoso';
                    } else {
                        // Mostrar error
                        alert(data.message || "Error al procesar el pago. Por favor, intenta nuevamente.");
                        hideLoadingIndicator();
                        if (submitButton) submitButton.disabled = false;
                        isSubmitting = false;
                    }
                })
                .catch(error => {
                    console.error("Error en la petición fetch:", error);
                    
                    // En caso de error de red, intentar enviar el formulario tradicional
                    console.log("Intentando método alternativo de envío...");
                    
                    // Limpiar cualquier token anterior que pudiera existir
                    const existingToken = formElement.querySelector('input[name="stripeToken"]');
                    if (existingToken) {
                        existingToken.remove();
                    }
                    
                    // Añadir el token al formulario
                    const hiddenInput = document.createElement('input');
                    hiddenInput.setAttribute('type', 'hidden');
                    hiddenInput.setAttribute('name', 'stripeToken');
                    hiddenInput.setAttribute('value', result.token.id);
                    formElement.appendChild(hiddenInput);
                    
                    // Añadir el carrito al formulario
                    const carritoInput = document.createElement('input');
                    carritoInput.setAttribute('type', 'hidden');
                    carritoInput.setAttribute('name', 'carrito');
                    carritoInput.setAttribute('value', localStorage.getItem('carrito') || '[]');
                    formElement.appendChild(carritoInput);
                    
                    // Limpiar localStorage antes de enviar para evitar doble procesamiento
                    localStorage.removeItem('carrito');
                    localStorage.removeItem('total');
                    
                    // Enviar el formulario de manera tradicional
                    formElement.submit();
                });
            }
        }).catch(function(error) {
            console.error("Error al generar token:", error);
            alert("Error al procesar el pago. Por favor, verifica la información de tu tarjeta e intenta nuevamente.");
            hideLoadingIndicator();
            if (submitButton) submitButton.disabled = false;
            isSubmitting = false;
        });
    } catch (error) {
        console.error("Error general en el proceso de pago:", error);
        alert("Error en el sistema de pagos. Por favor, intenta nuevamente o contacta a soporte.");
        hideLoadingIndicator();
        if (submitButton) submitButton.disabled = false;
        isSubmitting = false;
    }
}

// Función para procesar el pago por transferencia
function submitTransferPayment(formElement) {
    isSubmitting = true;
    showLoadingIndicator();
    
    // Desactivar el botón para evitar múltiples envíos
    const submitButton = formElement.querySelector('button[type="submit"]');
    if (submitButton) submitButton.disabled = true;
    
    console.log("Procesando pago por transferencia...");
    
    // Asegurar que el carrito se incluye en el formulario
    const carritoInput = document.getElementById('carrito-input');
    if (carritoInput) {
        carritoInput.value = localStorage.getItem('carrito') || '[]';
        console.log("Carrito incluido en transferencia:", carritoInput.value);
    } else {
        // Si no existe el input, crearlo
        const newCarritoInput = document.createElement('input');
        newCarritoInput.setAttribute('type', 'hidden');
        newCarritoInput.setAttribute('name', 'carrito');
        newCarritoInput.setAttribute('id', 'carrito-input');
        newCarritoInput.setAttribute('value', localStorage.getItem('carrito') || '[]');
        formElement.appendChild(newCarritoInput);
        console.log("Carrito creado y añadido:", newCarritoInput.value);
    }
    
    // Usar fetch para enviar el formulario
    try {
        const formData = new FormData(formElement);
        
        fetch(formElement.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Respuesta del servidor:", data);
            if (data.success) {
                // Limpiar localStorage después del pago exitoso
                localStorage.removeItem('carrito');
                localStorage.removeItem('total');
                
                // Redirigir a la página de éxito o mostrar mensaje
                window.location.href = data.redirect || '/pago-exitoso';
            } else {
                // Mostrar error
                alert(data.message || "Error al procesar la transferencia. Por favor, intenta nuevamente.");
                hideLoadingIndicator();
                if (submitButton) submitButton.disabled = false;
                isSubmitting = false;
            }
        })
        .catch(error => {
            console.error("Error en la petición fetch:", error);
            
            // Limpiar localStorage antes de enviar para evitar doble procesamiento
            localStorage.removeItem('carrito');
            localStorage.removeItem('total');
            
            // Enviar el formulario de manera tradicional como fallback
            formElement.submit();
        });
    } catch (error) {
        console.error("Error general al enviar datos de transferencia:", error);
        
        // Limpiar localStorage antes de enviar para evitar doble procesamiento
        localStorage.removeItem('carrito');
        localStorage.removeItem('total');
        
        // Enviar el formulario de manera tradicional como último recurso
        formElement.submit();
    }
}