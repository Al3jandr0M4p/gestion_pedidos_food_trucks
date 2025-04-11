fetch('/admin/reports', {
    headers: { "X-Requested-With": "XMLHttpRequest" }
})
.then(response => response.json())
.then(data => {
    console.log("Datos recibidos:", data);

    // Gráfico de Métodos de Pago
    const ctx1 = document.getElementById("graficoMetodosPago").getContext("2d");
    new Chart(ctx1, {
        type: 'line',
        data: {
            labels: data.metodo_pago.map(m => m.metodo),
            datasets: [{
                label: "Métodos de Pago",
                data: data.metodo_pago.map(m => m.total),
                backgroundColor: 'rgba(255, 125, 32, 0.3)', // Color con transparencia
                borderColor: '#ff7d20',  // Color de la línea
                borderWidth: 3,
                pointBackgroundColor: '#ff7d20', // Color de los puntos
                pointBorderColor: '#fff', // Color del borde de los puntos
                pointBorderWidth: 2,  // Bordes más gruesos
                pointRadius: 5,  // Aumentar el tamaño de los puntos
                fill: true,  // Rellenar debajo de la línea
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            aspectRatio: 1.5,  // Ajustar relación de aspecto
            plugins: {
                tooltip: {
                    backgroundColor: '#2c3e50',
                    titleColor: '#ecf0f1',
                    bodyColor: '#ecf0f1',
                    callbacks: {
                        label: function(tooltipItem) {
                            return `Total: $${tooltipItem.raw}`;
                        }
                    }
                },
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        font: {
                            family: 'Arial',
                            size: 14,
                            weight: 'bold',
                            color: '#34495e'  // Color de las etiquetas de la leyenda
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Método de Pago',
                        font: {
                            size: 14,
                            weight: 'bold',
                            color: '#34495e'
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Total ($)',
                        font: {
                            size: 14,
                            weight: 'bold',
                            color: '#34495e'
                        }
                    },
                    beginAtZero: true
                }
            }
        }
    });

    // Gráfico de Ingresos por Food Truck
    const ctx2 = document.getElementById("graficoTrucks").getContext("2d");
    new Chart(ctx2, {
        type: 'radar',
        data: {
            labels: data.ventas_trucks.map(t => t.nombre_truck),
            datasets: [{
                label: "Ingresos ($)",
                data: data.ventas_trucks.map(t => t.total),
                backgroundColor: 'rgba(251, 120, 27, 0.4)', // Color con transparencia
                borderColor: '#fb781b',
                borderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            aspectRatio: 2,  // Ajustar relación de aspecto
            plugins: {
                tooltip: {
                    backgroundColor: '#2c3e50',
                    titleColor: '#ecf0f1',
                    bodyColor: '#ecf0f1',
                    callbacks: {
                        label: function(tooltipItem) {
                            return `Ingresos: $${tooltipItem.raw}`;
                        }
                    }
                }
            }
        }
    });

    // Gráfico de Ventas por Producto
    const ctx3 = document.getElementById("graficoVentasProducto").getContext("2d");
    new Chart(ctx3, {
        type: 'bar',
        data: {
            labels: data.ventas_productos.map(p => p.nombre_producto),
            datasets: [{
                label: "Ingresos ($)",
                data: data.ventas_productos.map(p => p.total),
                backgroundColor: 'rgba(231, 76, 60, 0.8)', // Color con transparencia
                borderColor: '#e74c3c',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            aspectRatio: 1.5,  // Ajustar relación de aspecto
            plugins: {
                tooltip: {
                    backgroundColor: '#2c3e50',
                    titleColor: '#ecf0f1',
                    bodyColor: '#ecf0f1',
                    callbacks: {
                        label: function(tooltipItem) {
                            return `Total: $${tooltipItem.raw}`;
                        }
                    }
                },
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        font: {
                            family: 'Arial',
                            size: 14,
                            weight: 'bold',
                            color: '#34495e'  // Color de las etiquetas de la leyenda
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Producto',
                        font: {
                            size: 14,
                            weight: 'bold',
                            color: '#34495e'
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Total ($)',
                        font: {
                            size: 14,
                            weight: 'bold',
                            color: '#34495e'
                        }
                    },
                    beginAtZero: true
                }
            }
        }
    });

    // Gráfico de Número de Transacciones por Food Truck (más pequeño)
    const ctx4 = document.getElementById("graficoTransaccionesTruck").getContext("2d");
    new Chart(ctx4, {
        type: 'pie',
        data: {
            labels: data.transacciones_trucks.map(t => t.nombre_truck),
            datasets: [{
                label: "Transacciones",
                data: data.transacciones_trucks.map(t => t.numero_transacciones),
                backgroundColor: ['#2ecc71', '#9b59b6', '#f39c12', '#3498db']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            aspectRatio: 1,  // Relación de aspecto más pequeña
            plugins: {
                tooltip: {
                    backgroundColor: '#2c3e50',
                    titleColor: '#ecf0f1',
                    bodyColor: '#ecf0f1',
                    callbacks: {
                        label: function(tooltipItem) {
                            return `${tooltipItem.label}: ${tooltipItem.raw} transacciones`;
                        }
                    }
                }
            }
        }
    });

    // Gráfico de Ventas por Hora
    const ctx5 = document.getElementById("graficoVentasHora").getContext("2d");
    new Chart(ctx5, {
        type: 'line',
        data: {
            labels: data.ventas_hora.map(h => h.hora),
            datasets: [{
                label: "Ventas por Hora",
                data: data.ventas_hora.map(h => h.total),
                borderColor: '#34495e',
                fill: false,
                pointRadius: 6  // Aumentar tamaño de los puntos
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            aspectRatio: 2,  // Relación de aspecto ligeramente más grande
            plugins: {
                tooltip: {
                    backgroundColor: '#2c3e50',
                    titleColor: '#ecf0f1',
                    bodyColor: '#ecf0f1',
                    callbacks: {
                        label: function(tooltipItem) {
                            return `Ventas: $${tooltipItem.raw}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Hora del Día',
                        font: {
                            size: 14,
                            weight: 'bold',
                            color: '#34495e'
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Total ($)',
                        font: {
                            size: 14,
                            weight: 'bold',
                            color: '#34495e'
                        }
                    },
                    beginAtZero: true
                }
            }
        }
    });

    // Gráfico de Estado de las Mesas (más pequeño)
    const ctx6 = document.getElementById("graficoEstadoMesas").getContext("2d");
    new Chart(ctx6, {
        type: 'doughnut',
        data: {
            labels: data.estado_mesas.map(m => m.estado),
            datasets: [{
                label: "Estado de las Mesas",
                data: data.estado_mesas.map(m => m.total),
                backgroundColor: ['#f1c40f', '#e74c3c'],
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            aspectRatio: 1,  // Relación de aspecto más pequeña
            plugins: {
                tooltip: {
                    backgroundColor: '#2c3e50',
                    titleColor: '#ecf0f1',
                    bodyColor: '#ecf0f1',
                    callbacks: {
                        label: function(tooltipItem) {
                            return `${tooltipItem.label}: ${tooltipItem.raw} mesas`;
                        }
                    }
                }
            }
        }
    });
})
.catch(error => console.error("Error al obtener datos:", error));