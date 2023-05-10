
//census chart

let chartData = {
  labels: ['Mangum', 'Pawhuska', 'Prague', 'Carnegie', 'Seilling'],
  datasets: [{
    data: [0, 0, 0, 0],
    backgroundColor: ['rgba(255, 99, 132, 0.8)',
    'rgba(54, 162, 235, 0.8)',
    'rgba(255, 206, 86, 0.8)',
    'rgba(75, 192, 192, 0.8)',
    'rgba(153, 102, 255, 0.8)'],
    borderWidth: 1,
  }]
};

$.ajax({
  url: '/charts-data/',
  type: 'GET',
  dataType: 'json',
  success: function (chart_data) {

    chartData.datasets[0].data = [chart_data.swing_bed, chart_data.acute_bed, chart_data.inpatient, chart_data.outpatient];


    let ctx = document.getElementById('motalityRate').getContext('2d');
    new Chart(ctx, {
      type: 'doughnut',
      data: chartData,
      options: {
        plugins:{
            legend: {
                rtl: true,
                
                display: true,
                position: 'right',
                labels: {
                    usePointStyle: true
                    
                }
                
            },
           
        } ,
       
       layout: {
            padding: {
                left : 0,
            }
          }   
      },

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
