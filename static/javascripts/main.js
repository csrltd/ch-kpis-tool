
//census chart

var chartData = {
  labels: ['Swing Bed', 'Acute Bed', 'inpatient', 'outpatient'],
  datasets: [{
    data: [0, 0, 0, 0],
    backgroundColor: ['#FF6384', '#36A2EB', '#FF456', '#23A2AB'],
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
        display: true,

      }
    });
  }
});


let lineData = {
  labels: ['Mangum', 'Prague', 'Carnegie', 'Pawhuska'],
  datasets: [{
    label:["Hospitals"],
    data: [0, 0, 0, 0],
    borderWidth: 1,
  }],
  backgroundColor: ['#FF6384', '#36A2EB', '#FF456', '#23A2AB']
};

$.ajax({
  url: '/linechart_data/',
  type: 'GET',
  dataType: 'json',
  success: function (response) {
    lineData.labels = response.hospital_names;
    lineData.datasets[0].data = response.mortality_rates;
    const ctx = document.getElementById('earning');
    new Chart(ctx, {
      type: 'bar',
      data: lineData,
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
          }
        }
      }
    });
  }
});




