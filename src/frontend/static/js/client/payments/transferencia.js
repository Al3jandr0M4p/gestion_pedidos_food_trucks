document.addEventListener('DOMContentLoaded', () => {
    const total = localStorage.getItem('total') || "0.00";
    document.getElementById("monto").value = total;

    document.getElementById("carrito-input").value = localStorage.getItem("carrito") || "[]";
});