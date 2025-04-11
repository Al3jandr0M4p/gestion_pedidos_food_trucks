let currentPage = 1;
let pageSize = 10;
let totalPages = 1;
let rows = [];

document.addEventListener('DOMContentLoaded', function () {
    rows = document.querySelectorAll('#pedidosTable tbody tr');
    initPagination();

    displayPage(currentPage);
});

function initPagination() {
    totalPages = Math.ceil(rows.length / pageSize);
    document.getElementById('total-items').textContent = rows.length;

    updatePaginationControls();

    updateNavButtons();
}

function displayPage(page) {
    rows.forEach(row => {
        row.classList.remove('active');
    });

    const startIndex = (page - 1) * pageSize;
    const endIndex = Math.min(startIndex + pageSize, rows.length);

    for (let i = startIndex; i < endIndex; i++) {
        if (rows[i]) {
            rows[i].classList.add('active');
        }
    }

    document.getElementById('page-start').textContent = startIndex + 1;
    document.getElementById('page-end').textContent = endIndex;

    currentPage = page;

    updatePaginationControls();
    updateNavButtons();
}

function updatePaginationControls() {
    const pageNumbers = document.getElementById('page-numbers');
    pageNumbers.innerHTML = '';

    const maxVisibleButtons = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxVisibleButtons / 2));
    let endPage = Math.min(totalPages, startPage + maxVisibleButtons - 1);

    if (endPage - startPage + 1 < maxVisibleButtons) {
        startPage = Math.max(1, endPage - maxVisibleButtons + 1);
    }

    if (startPage > 1) {
        const firstPageBtn = createPageButton(1);
        pageNumbers.appendChild(firstPageBtn);

        if (startPage > 2) {
            const ellipsis = document.createElement('span');
            ellipsis.textContent = '...';
            ellipsis.className = 'pagination-ellipsis';
            ellipsis.style.margin = '0 5px';
            pageNumbers.appendChild(ellipsis);
        }
    }

    for (let i = startPage; i <= endPage; i++) {
        const pageBtn = createPageButton(i);
        if (i === currentPage) {
            pageBtn.classList.add('active');
        }
        pageNumbers.appendChild(pageBtn);
    }

    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            const ellipsis = document.createElement('span');
            ellipsis.textContent = '...';
            ellipsis.className = 'pagination-ellipsis';
            ellipsis.style.margin = '0 5px';
            pageNumbers.appendChild(ellipsis);
        }

        const lastPageBtn = createPageButton(totalPages);
        pageNumbers.appendChild(lastPageBtn);
    }
}

function createPageButton(pageNum) {
    const button = document.createElement('button');
    button.className = 'pagination-button';
    button.textContent = pageNum;
    button.onclick = function () {
        displayPage(pageNum);
    };
    return button;
}

function updateNavButtons() {
    const prevBtn = document.getElementById('prev-page');
    const nextBtn = document.getElementById('next-page');

    prevBtn.disabled = currentPage === 1;
    nextBtn.disabled = currentPage === totalPages;
}

function prevPage() {
    if (currentPage > 1) {
        displayPage(currentPage - 1);
    }
}

function nextPage() {
    if (currentPage < totalPages) {
        displayPage(currentPage + 1);
    }
}

function changePageSize(size) {
    pageSize = parseInt(size);
    currentPage = 1;
    initPagination();
    displayPage(1);
}