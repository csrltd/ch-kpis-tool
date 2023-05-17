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


const urlParts = window.location.pathname.split('/');
const hospitalId = urlParts[urlParts.length - 1];

// Single Hospital
fetch(`/single-hospital-data/${hospitalId}`)
  .then((response) => response.json())
  .then((data) => {
    const labels = data.labels;
    const datasets = data.datasets;

    // create chart
    const ctx = document.getElementById("singleturnOvers").getContext("2d");
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
