let myChart;
// const hospitalId = `{{ hospital_id }}`;

fetch(`/single-hospital-turnover-data/${hospitalId}/`)
    .then((response) => response.json())
    .then((data) => {
        const labels = data.labels;
        const datasets = data.datasets;

        // create chart
        const ctx = document.getElementById("turnOvers").getContext("2d");
        myChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: datasets,
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: true,
                    position: "bottom",
                },
                scales: {
                    xAxes: [
                        {
                            display: true,
                            scaleLabel: {
                                display: true,
                                labelString: "Month-Year",
                            },
                        },
                    ],
                    yAxes: [
                        {
                            display: true,
                            scaleLabel: {
                                display: true,
                                labelString: "Values",
                            },
                            ticks: {
                                beginAtZero: true,
                                stepSize: 10,
                            },
                        },
                    ],
                },
            },
        });
    })
    .catch((error) => console.error(error));


document.getElementById("year").addEventListener("change", function () {
    var selectedYear = this.value;

    fetch(`/single-hospital-turnover-data/${hospitalId}/?year=${selectedYear}`)
        .then((response) => response.json())
        .then((data) => {

            updateChart(data);
        })
        .catch((error) => console.error(error));
});

function updateChart(data) {
    myChart.data.labels = data.labels;
    myChart.data.datasets = data.datasets;
    myChart.update();
}