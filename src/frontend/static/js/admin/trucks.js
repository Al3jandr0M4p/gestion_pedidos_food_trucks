function openModalById (modalId, url=null) {
    const modal = document.getElementById(modalId);
    if (!modal) return;

    console.log("URL: ", url);

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
                showNotification("Error al cargar el contenido del modal de trucks", "error")
                console.error(err);
            });
    } else {
        modal.style.display = 'block';
    }
}

const closeModalById = (modalId) => {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = 'none';
}

const openFoodTruckModal = (id) => {
    openModalById('foodtrucksModal', `/admin/foodtrucks/update_trucks/${id}`);
}

const openCreateFoodTruckModal = () => {
    openModalById('foodtrucksModal', `/admin/foodtrucks/create_trucks`);
}

const closeFoodTruckModal = () => {
    closeModalById('foodtrucksModal');
}

window.onclick = (event) => {
    const modal = document.getElementById('foodtrucksModal');
    if (event.target === modal) {
        closeFoodTruckModal();
    }
}
