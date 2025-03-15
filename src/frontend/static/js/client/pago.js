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
        }, 100)
    }
}

let closeModal = (id) => {
    document.getElementById(id).style.display = 'none';
}