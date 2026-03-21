document.addEventListener('DOMContentLoaded', function () {
    fetch('data/line_chart_data.json')
        .then(response => response.json())
        .then(data => {
            const lnc = document.getElementById('line-chart');

            new Chart(lnc, {
                type: 'line',
                data: {
                    labels: [...Array(42).keys()],
                    datasets: data
                }
            })

        })
        .catch(error => console.error('Fehler beim Laden der Daten:', error));
});