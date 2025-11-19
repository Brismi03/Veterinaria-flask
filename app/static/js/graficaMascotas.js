document.addEventListener("DOMContentLoaded", function() {
    try {
        const ctx = document.getElementById('barChart')?.getContext('2d');
        if (ctx) {
            const mascotasData = {
                labels: tipos_mascotas,
                datasets: [{
                    label: 'Cantidad de mascotas',
                    data: cantidades_mascotas,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            };

            const mascotasConfig = {
                type: 'bar',
                data: mascotasData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            };

            new Chart(ctx, mascotasConfig);
        } else {
            console.error('Elemento canvas no encontrado.');
        }
    } catch (e) {
        console.error('Error al crear la gráfica:', e);
    }
});
