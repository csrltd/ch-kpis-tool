fetch('/measures_data')
    .then(response => response.json())
    .then(data => {

        const labels = [];
        const mortalityRates = [];
        data.forEach(measure => {
            labels.push(measure.hospital__name);
            mortalityRates.push(measure.total_mortality_rate);
        });

        const ctx = document.getElementById('mortality-rate').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Total Mortality Rate',
                    data: mortalityRates,
                    backgroundColor: ['rgb(14, 118, 188)', 'rgb(150, 77, 77)', 'rgb(48, 180, 26)', 'rgb(255, 0, 0)', 'rgb(255, 229, 0)'],
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }],
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    });