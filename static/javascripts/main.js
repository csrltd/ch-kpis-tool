
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



// let lineData = {
//   labels: [],
//   datasets: [{
//     label: [],
//     data: [],
//     borderWidth: 1,
//     backgroundColor: 'rgba(255, 99, 132, 0.2)',
//     borderColor: 'rgba(255, 99, 132, 1)',
//     hoverBackgroundColor: 'rgba(255, 99, 132, 0.4)',
//     hoverBorderColor: 'rgba(255, 99, 132, 1)',
//   }, {
//     label: [],
//     data: [],
//     borderWidth: 1,
//     backgroundColor: 'rgba(54, 162, 235, 0.2)',
//     borderColor: 'rgba(54, 162, 235, 1)',
//     hoverBackgroundColor: 'rgba(54, 162, 235, 0.4)',
//     hoverBorderColor: 'rgba(54, 162, 235, 1)',
//   }],
// };



// $.ajax({
//   url: '/filter_patients_by_month/',
//   type: 'GET',
//   dataType: 'json',
//   success: function (response) {
//     // create an array of objects for each hospital
//     const datasets = Object.keys(response).map((hospital) => ({
//       label: hospital + ' - Inpatient',
//       data: response[hospital]['inpatient_totals'],
//       borderWidth: 1,
//       backgroundColor: ['#FF6384', '#36A2EB', '#463333', '#23A2AB'],
//       borderColor: ['#FF6384', '#36A2EB', '#463333', '#23A2AB'],
      
//       fill: false
//     }), Object.keys(response).map((hospital) => ({
//       label: hospital + ' - Outpatient',
//       data: response[hospital]['outpatient_totals'],
//       borderWidth: 1,
//       backgroundColor: ['#F96384', '#F6A2EB', '#4A3333', '#2FA2AB'],
//       borderColor: ['#F36384', '#36A5EB', '#463F33', '#2332AB'],
      
//       fill: false
//     }))).flat();
//     const months = response[Object.keys(response)[0]]['months'];
//     lineData.labels = months;
//     lineData.datasets = datasets;
//     const ctx = document.getElementById('earning');
//     new Chart(ctx, {
//       type: 'line',
//       data: lineData,
//       options: {
//         responsive: true,
//         scales: {
//           yAxes: [{
//             ticks: {
//               beginAtZero: true
//             }
//           }]
//         },
//         legend: {
//           display: true,
//           position: 'bottom',
//           labels: {
//             usePointStyle: true
//           }
//         }
//       }
//     });
//   }
// });

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
  url: '/filter_patients_by_month/',
  type: 'GET',
  dataType: 'json',
  success: function (response) {
    // create an array of objects for each hospital
    const datasets = Object.keys(response).flatMap((hospital, index) => [{
      label: `${hospital} - Inpatient`,
      data: response[hospital]['inpatient_totals'],
      borderWidth: 1,
      backgroundColor: [`rgba(255, 99, 132, ${(index + 1) / (Object.keys(response).length + 1)})`],
      borderColor: [`rgba(255, 99, 132, 1)`],
      fill: false
    }, {
      label: `${hospital} - Outpatient`,
      data: response[hospital]['outpatient_totals'],
      borderWidth: 1,
      backgroundColor: [`rgba(54, 162, 235, ${(index + 1) / (Object.keys(response).length + 1)})`],
      borderColor: [`rgba(54, 162, 235, 1)`],
      fill: false
    }]);
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
