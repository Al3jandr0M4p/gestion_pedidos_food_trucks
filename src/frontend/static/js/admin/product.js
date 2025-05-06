function openModalById(modalId, url=null) {
    const modal = document.getElementById(modalId);
    if (!modal) return;

    if (url) {
        fetch(url)
            .then(response => {
                if (!response.ok) throw new Error("No se pudo cargar el modal");
                return response.text();
            })
            .then(html => {
                const modalBody = modal.querySelector('.modal-body') || modal.querySelector('#modal-body');

                if (modalBody) modalBody.innerHTML = html;
                modal.style.display = 'block';
            })
            .catch(err => {
                showNotification("Error al cargar el modal de productos", "error");
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

const openProductModal = (id) => openModalById('productModal', `/admin/products/update_product/${id}`);

const openCreateProductModal = (id) => openModalById('productModal', `/admin/products/create_product/${id}`);

const closeProductModal = () => closeModalById('productModal');

window.onclick = event => {
    const modal = document.getElementById('productModal');
    if (event.target == modal) closeProductModal();
}