// fetch data from the server
fetch("/turnover_data/")
  .then((response) => response.json())
  .then((data) => {
    const labels = data.labels;
    const datasets = data.datasets;

    // create chart
    const ctx = document.getElementById("turnOvers").getContext("2d");
    const myChart = new Chart(ctx, {
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
                labelString: "Months",
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
