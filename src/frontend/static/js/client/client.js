document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".btn-status").forEach(button => {
        button.addEventListener("click", function () {
            const userId = this.getAttribute("data-id");
            toggleStatus(userId, this);
        });
    });
});

function toggleStatus(userId, button) {
    fetch(`/admin/gestion/employees/toggle_status/${userId}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const row = button.closest("tr");
            const statusElement = row.querySelector(".status");

            if (data.new_status === "activo") {
                statusElement.textContent = "activo";
                statusElement.classList.remove("inactive");
                statusElement.classList.add("active");
                button.innerHTML = "🔴 Desactivar";
            } else {
                statusElement.textContent = "inactivo";
                statusElement.classList.remove("active");
                statusElement.classList.add("inactive");
                button.innerHTML = "🟢 Activar";
            }
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => {
        console.error("Error en la solicitud:", error);
    });
}