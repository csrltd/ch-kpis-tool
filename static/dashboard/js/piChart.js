fetch("/measures_data")
  .then((response) => response.json())
  .then((data) => {
    const labels = [];
    const mortalityRates = [];
    data.forEach((measure) => {
      labels.push(measure.hospital__name);
      mortalityRates.push(measure.total_mortality_rate);
    });

    const ctx = document.getElementById("mortality-rate").getContext("2d");
    const chart = new Chart(ctx, {
      type: "pie",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Total Mortality Rate",
            data: mortalityRates,
            backgroundColor: [
              "rgb(14, 118, 188)",
              "rgb(150, 77, 77)",
              "rgb(48, 180, 26)",
              "rgb(255, 0, 0)",
              "rgb(255, 229, 0)",
            ],
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
              },
            },
          ],
        },
      },
    });
  });

let lineData = {
  labels: [],
  datasets: [
    {
      label: [],
      data: [],
      borderWidth: 1,
      backgroundColor: "rgba(255, 99, 132, 0.2)",
      borderColor: "rgba(255, 99, 132, 1)",
      hoverBackgroundColor: "rgba(255, 99, 132, 0.4)",
      hoverBorderColor: "rgba(255, 99, 132, 1)",
    },
    {
      label: [],
      data: [],
      borderWidth: 1,
      backgroundColor: "rgba(54, 162, 235, 0.2)",
      borderColor: "rgba(54, 162, 235, 1)",
      hoverBackgroundColor: "rgba(54, 162, 235, 0.4)",
      hoverBorderColor: "rgba(54, 162, 235, 1)",
    },
  ],
};
$.ajax({
  url: "/filter_patients_by_month/",
  type: "GET",
  dataType: "json",
  success: function (response) {
    // create an array of objects for each hospital
    const datasets = Object.keys(response).flatMap((hospital, index) => [
      {
        label: `${hospital} - Inpatient`,
        data: response[hospital]["inpatient_totals"],
        borderWidth: 1,
        backgroundColor: [
          `rgba(255, 99, 132, ${
            (index + 1) / (Object.keys(response).length + 1)
          })`,
        ],
        borderColor: [`rgba(255, 99, 132, 1)`],
        fill: false,
      },
      {
        label: `${hospital} - Outpatient`,
        data: response[hospital]["outpatient_totals"],
        borderWidth: 1,
        backgroundColor: [
          `rgba(54, 162, 235, ${
            (index + 1) / (Object.keys(response).length + 1)
          })`,
        ],
        borderColor: [`rgba(54, 162, 235, 1)`],
        fill: false,
      },
    ]);
    const months = response[Object.keys(response)[0]]["months"];
    lineData.labels = months;
    lineData.datasets = datasets;
    const ctx = document.getElementById("earning");
    new Chart(ctx, {
      type: "line",
      data: lineData,
      options: {
        responsive: true,
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
              },
            },
          ],
        },
        legend: {
          display: true,
          position: "bottom",
          labels: {
            usePointStyle: true,
          },
        },
      },
    });
  },
});
