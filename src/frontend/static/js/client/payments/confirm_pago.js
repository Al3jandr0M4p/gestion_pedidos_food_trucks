document.addEventListener("DOMContentLoaded", () => {
    localStorage.removeItem("carrito");
    localStorage.removeItem("total");
    localStorage.removeItem("itbis");
    sessionStorage.removeItem("carrito");
    alert("Productos comprados exitosamente.")
});