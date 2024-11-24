fetch('/libros-mas-prestados/')
.then(response => response.json())
.then(data => {
    const ctx = document.getElementById('prestamosChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels, // Nombres de los libros
            datasets: [{
                label: 'Préstamos',
                data: data.values, // Cantidad de préstamos
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true, // Hacer el gráfico responsive
            maintainAspectRatio: false, // Permitir que cambie de proporción
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    position: 'top', // Ajustar la posición de la leyenda
                }
            }
        }
    });
});