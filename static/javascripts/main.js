
//census chart

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
     
      chartData.datasets[0].data = [chart_data.swing_bed, chart_data.acute_bed, chart_data.inpatient, chart_data.outpatient];

       
      var ctx = document.getElementById('myChart').getContext('2d');
      new Chart(ctx, {
          type: 'doughnut',
          data: chartData,
          options: {
            display: true,
              legend:{
                position: 'right',
                align : 'center'
              }
             
          }
      });
  }
});

//Measures chart

var lineData = {
  labels: ['Mangum', 'Prague', 'Carnegie', 'Pawhuska'],
  
  datasets: [{
    
    data: [0],
    borderWidth: 1
  }],
  backgroundColor: [
    'rgba(255, 99, 132, 0.2)',
    'rgba(255, 159, 64, 0.2)',
    'rgba(255, 205, 86, 0.2)',
    'rgba(201, 203, 207, 0.2)'
  ],
};
$.ajax({
  url: 'linechart/',
  type: 'GET',
  dataType: 'json',
  success: function (linechart_data) {
     
    lineData.datasets[0].data = [linechart_data.hospital];

const ctx = document.getElementById('earning');

  new Chart(ctx, {
    type: 'line',
    data: lineData,

    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}
});
