
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


// let lineData = {
//   labels: ['Mangum', 'Prague', 'Carnegie', 'Pawhuska'],
//   datasets: [{
//     label:["Hospitals"],
//     data: [0, 0, 0, 0],
//     borderWidth: 1,
//   }],
//   backgroundColor: ['#FF6384', '#36A2EB', '#FF456', '#23A2AB']
// };

// $.ajax({
//   url: '/linechart_data/',
//   type: 'GET',
//   dataType: 'json',
//   success: function (response) {
//     lineData.labels = response.hospital_names;
//     lineData.datasets[0].data = response.mortality_rates;
//     const ctx = document.getElementById('earning');
//     new Chart(ctx, {
//       type: 'bar',
//       data: lineData,
//       options: {
//         responsive: true,
//         scales: {
//           y: {
//             beginAtZero: true,
//           }
//         }
//       }
//     });
//   }
// });


let lineData = {
  labels: [],
  datasets: [{
    label: 'Inpatients',
    data: [],
    borderWidth: 1,
    backgroundColor: 'rgba(255, 99, 132, 0.2)',
    borderColor: 'rgba(255, 99, 132, 1)',
    hoverBackgroundColor: 'rgba(255, 99, 132, 0.4)',
    hoverBorderColor: 'rgba(255, 99, 132, 1)',
  }, {
    label: 'Outpatients',
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
    lineData.labels = response.hospital_names;
    lineData.datasets[0].data = response.inpatient_data;
    lineData.datasets[1].data = response.outpatient_data;
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
        }
      }
    });
  }
});





