function openModalById (modalId, url=null) {
    const modal = document.getElementById(modalId);
    if (!modal) return;

    if (url) {
        fetch(url)
            .then(response => {
                if (!response.ok) throw new Error("No se pudo cargar el contenido");
                return response.text();
            })
            .then(html => {
                const modalBody = modal.querySelector('.modal-body') || modal.querySelector('#modal-body');
                
                if (modalBody) modalBody.innerHTML = html;
                modal.style.display = 'block';
            })
            .catch(err => {
                showNotification("Error al cargar el contenido del modal", "error");
                console.log(err);
            });
    } else {
        modal.style.display = 'block';
    }
}

const closeModalById = (modalId) => {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = 'none';
}

const openEmployeeModal = (id) => {
    openModalById('employeeModal', `/admin/employees/update_employee/${id}`);
}

const openCreateEmployeeModal = () => {
    openModalById('employeeModal', '/admin/employees/create_employee');
}

const closeEmployeeModal = () => {
    closeModalById('employeeModal');
}

window.onclick = event => {
    const modal = document.getElementById('employeeModal');
    if (event.target === modal) {
        closeEmployeeModal();
    }
}