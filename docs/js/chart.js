document.addEventListener('DOMContentLoaded', function () {
    fetch('data/line_chart_data.json')
        .then(response => response.json())
        .then(data => {
            const lnc = document.getElementById('line-chart');
            console.log(data[0].data)
            let chartlength = data[0].data.length
            new Chart(lnc, {
                type: 'line',
                data: {
                    labels: [...Array(chartlength).keys()],
                    datasets: data
                },
                options: {
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Spiele'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Punkte'
                            }
                        }
                    }
                }
            })

        })
        .catch(error => console.error('Fehler beim Laden der Daten:', error));
});