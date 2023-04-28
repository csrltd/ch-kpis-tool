var chartData = {
  labels: ['Swing Bed', 'Acute Bed','inpatient','outpatient'],
  datasets: [{
      data: [0, 0, 0, 0],
      backgroundColor: ['#FF6384', '#36A2EB','#FF456','#23A2AB'],
      borderWidth: 1
  }]
};

$.ajax({
  url: '/charts-data/',
  type: 'GET',
  dataType: 'json',
  success: function (chart_data) {
      // Update the chart data with the received data
      chartData.datasets[0].data = [chart_data.swing_bed, chart_data.acute_bed, chart_data.inpatient, chart_data.outpatient];

      // Create the chart
      var ctx = document.getElementById('myChart').getContext('2d');
      var myChart = new Chart(ctx, {
          type: 'doughnut',
          data: chartData,
          options: {
              responsive: false
          }
      });
  }
});



const ctx = document.getElementById('earning');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Mangum', 'Prague', 'Carnegie', 'Pawhuska'],
      datasets: [{
        label: 'Hospitals',
        data: [12, 19, 3, 5],
        borderWidth: 1
      }],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(255, 205, 86, 0.2)',
        'rgba(201, 203, 207, 0.2)'
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
