/**
 * For usage, visit Chart.js docs https://www.chartjs.org/docs/latest/
 */
const lineConfig = {
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'],
    datasets: [
      {
        label: 'Mangum',
        /**
         * These colors come from Tailwind CSS palette
         * https://tailwindcss.com/docs/customizing-colors/#default-color-palette
         */
        backgroundColor: '#bef264',
        borderColor: '#bef264',
        data: [3, 8, 40, 4, 67, 3, 70, 4, 0, 46, 70, 20],
        fill: false,
      },
      {
        label: 'Prague',
        /**
         * These colors come from Tailwind CSS palette
         * https://tailwindcss.com/docs/customizing-colors/#default-color-palette
         */
        backgroundColor: '#60a5fa',
        borderColor: '#60a5fa',
        data: [48, 38, 30, 4, 7, 23, 20, 73, 10, 4, 20, 300],
        fill: false,
      },
      {
        label: 'Pawhuska',
        /**
         * These colors come from Tailwind CSS palette
         * https://tailwindcss.com/docs/customizing-colors/#default-color-palette
         */
        backgroundColor: '#0d9488',
        borderColor: '#0d9488',
        data: [43, 48, 40, 54, 67, 73, 70, -3, 0, 40, 40, -200],
        fill: false,
      },
      {
        label: 'Seiling',
        /**
         * These colors come from Tailwind CSS palette
         * https://tailwindcss.com/docs/customizing-colors/#default-color-palette
         */
        backgroundColor: '#9333ea',
        borderColor: '#9333ea',
        data: [43, 48, 50, 64, 77, 83, 90, -30, 10, 30, 20, -100],
        fill: false,
      },
      {
        label: 'Carnegie',
        fill: false,
        /**
         * These colors come from Tailwind CSS palette
         * https://tailwindcss.com/docs/customizing-colors/#default-color-palette
         */
        backgroundColor: '#ca8a04',
        borderColor: '#ca8a04',
        data: [-3, 0, 40, 40, -200, 24, 50, 64, 74, 52, 51, 65],
      },
    ],
  },
  options: {
    responsive: true,
    /**
     * Default legends are ugly and impossible to style.
     * See examples in charts.html to add your own legends
     *  */
    legend: {
      display: false,
    },
    tooltips: {
      mode: 'index',
      intersect: false,
    },
    hover: {
      mode: 'nearest',
      intersect: true,
    },
    scales: {
      x: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Month',
        },
      },
      y: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Value',
        },
      },
    },
  },
}

// change this to the id of your chart element in HMTL
const lineCtx = document.getElementById('line')
window.myLine = new Chart(lineCtx, lineConfig)
