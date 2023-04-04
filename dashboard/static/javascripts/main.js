
  const ctx = document.getElementById('myChart');
  const earning = document.getElementById('earning');
  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Inpatient', 'Swing Bed', 'Observetion', 'Emergency Room', 'Outpatient', 'Rural Health Clinic'],
      datasets: [{
        label: '# of Votes',
        data: [12, 19, 3, 5, 2, 3],
        backgroundColor:[
            'rgba(14, 118, 188, 1)',
            'rgba(48, 180, 26, 1)',
            'rgba(0, 174, 239, 1)',
            'rgba(150, 77, 77, 1)',
            'rgba(255, 0, 0, 1)',
            'rgba(48, 180, 26, 1)',
        ],
        
        borderWidth: 1
      }]
    },
    options: {
        responsive: true,
    //   scales: {
    //     y: {
    //       beginAtZero: true
    //     }
    //   }
    }
  });

  new Chart(earning, {
    type: 'line',
    data: {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange', 'Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
      datasets: [{
        label: 'Earning',
        data: [12, 19, 3, 5, 2, 3,12, 19, 3, 5, 2, 3],
       
        backgroundColor: [
            'rgba(226, 190, 69, 1)',
            'rgba(244, 90, 110, 1)',
            'rgba(226, 190, 69, 1)',
            'rgba(226, 190, 69, 1)',
            'rgba(22, 6, 185, 1)',
        ],
        // borderWidth: 1
      }]
    },
    options: {
      responsive:true,
      scales: {
            x: {
              beginAtoZero: true
            }
          }
    }
  });
