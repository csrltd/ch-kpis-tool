

const ctx = document.getElementById('myChart').getContext('2d');

new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: bed_labels,
    datasets: [{
      label: 'patient',
      data: swing_bed,
      backgroundColor: [
        
        'rgba(48, 180, 255)'
        
      ],

      borderWidth: 1
    }]
  },
  data: {
    labels: bed_labels,
    datasets: [{
      label: 'beds',
      data: acute_bed,
      backgroundColor: [
        'rgba(14, 188, 1)'
        
      ],

      borderWidth: 1
    }]
  },
  
  options: {
    responsive: true,

  }
});







// for (var view in chartData) {
//   if (chartData.hasOwnProperty(view)) {
//     var data = chartData[view].data;
    
//     // Add the view's data to the chartDataSets array
//     chartDataSets.push({
//       label: view,
//       data: data,
//     });
//   }
// }

// // Create an array of unique label values
// chartLabels = Object.keys(chartData);

// // Create the chart

// console.log(chartData);
// var ctx = document.getElementById('myChart').getContext('2d');
// var myChart = new Chart(ctx, {
//   type: 'doughnut',
//   data: {
//     labels: chartLabels,
//     datasets:[{
//       label:'my dataset',
//       data: chartDataSets[0].data,
//       backgroundColor: [
//         'rgba(255, 99, 132, 1)',
//         'rgba(54, 162, 235, 1)',
//         'rgba(255, 206, 86, 1)',
//         'rgba(75, 192, 192, 1)',
//         'rgba(153, 102, 255, 1)',
//         'rgba(255, 159, 64, 1)'
//       ],
//       borderColor: [
//         'rgba(255, 99, 132, 1)',
//         'rgba(54, 162, 235, 1)',
//         'rgba(255, 206, 86, 1)',
//         'rgba(75, 192, 192, 1)',
//         'rgba(153, 102, 255, 1)',
//         'rgba(255, 159, 64, 1)'
//       ],
//     }] 
//   },
// }
