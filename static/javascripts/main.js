
//census chart

var chartData = {
  labels: ['Swing Bed', 'Acute Bed', 'inpatient', 'outpatient'],
  datasets: [{
    data: [0, 0, 0, 0],
    backgroundColor: ['#FF6384', '#36A2EB', '#463333', '#23A2AB'],
    borderWidth: 1,
  }]
};

$.ajax({
  url: '/charts-data/',
  type: 'GET',
  dataType: 'json',
  success: function (chart_data) {

    chartData.datasets[0].data = [chart_data.swing_bed, chart_data.acute_bed, chart_data.inpatient, chart_data.outpatient];


    var ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
      type: 'doughnut',
      data: chartData,
      options: {
        Plugins: {
          legend: {
            labels: {
              usePointStyle : true
            }
          }
        },

      }
    });
  }
});



let lineData = {
  labels: [],
  datasets: [{
    label: [],
    data: [],
    borderWidth: 1,
    backgroundColor: 'rgba(255, 99, 132, 0.2)',
    borderColor: 'rgba(255, 99, 132, 1)',
    hoverBackgroundColor: 'rgba(255, 99, 132, 0.4)',
    hoverBorderColor: 'rgba(255, 99, 132, 1)',
  }, {
    label: [],
    data: [],
    borderWidth: 1,
    backgroundColor: 'rgba(54, 162, 235, 0.2)',
    borderColor: 'rgba(54, 162, 235, 1)',
    hoverBackgroundColor: 'rgba(54, 162, 235, 0.4)',
    hoverBorderColor: 'rgba(54, 162, 235, 1)',
  }],
};
$.ajax({
  url: '/linechart_data/',
  type: 'GET',
  dataType: 'json',
  success: function (response) {
    // create an array of objects for each hospital
    const datasets = Object.keys(response).map((hospital) => ({
      label: hospital,
      data: response[hospital]['totals'],
      borderColor: getRandomColor(),
      fill: false
    }));
    const months = response[Object.keys(response)[0]]['months'];
    lineData.labels = months;
    lineData.datasets = datasets;
    const ctx = document.getElementById('earning');
    new Chart(ctx, {
      type: 'line',
      data: lineData,
      options: {
        responsive: true,
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        },
        legend: {
          display: true,
          position: 'bottom',
          labels: {
            usePointStyle: true
          }
        }
      }
    });
  }
});

function getRandomColor() {
  // generate a random color for each hospital
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}
