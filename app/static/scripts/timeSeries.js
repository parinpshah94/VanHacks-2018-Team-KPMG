window.chartColors = {
  red: 'rgb(255, 99, 132)',
  orange: 'rgb(255, 159, 64)',
  yellow: 'rgb(255, 205, 86)',
  green: 'rgb(75, 192, 192)',
  blue: 'rgb(54, 162, 235)',
  purple: 'rgb(153, 102, 255)',
  grey: 'rgb(231,233,237)'
};

var randomScalingFactor = function() {
  return (Math.random() > 0.5 ? 1.0 : 1.0) * Math.round(Math.random() * 100);
};

var line1 = [randomScalingFactor()*10, randomScalingFactor()*10, randomScalingFactor()*10, randomScalingFactor()*10, randomScalingFactor()*10, randomScalingFactor()*10, randomScalingFactor()*10, randomScalingFactor()*10, randomScalingFactor()*10, randomScalingFactor()*10, randomScalingFactor()*10,randomScalingFactor()*10, ];

var line2 = [randomScalingFactor()*10, randomScalingFactor()*10, randomScalingFactor()*10, randomScalingFactor()*10, randomScalingFactor()*10, randomScalingFactor()*10, randomScalingFactor()*10, randomScalingFactor()*10, randomScalingFactor()*10, randomScalingFactor()*10, randomScalingFactor()*10, 660, ];

var MONTHS = ["Oct, 2017", "Nov, 2017", "Dec, 2017", "Jan, 2018", "Feb, 2018", "Mar, 2018", "Apr, 2018", "May, 2018", "Jun, 2018", "Jul, 2018", "Aug, 2018", "Sep, 2018"];
var config = {
  type: 'line',
  data: {
    labels: MONTHS,
    display: false,
    datasets: [{
      label: "Collected",
      backgroundColor: window.chartColors.red,
      borderColor: window.chartColors.red,
      data: line1,
      fill: false,
    }, {
      label: "Redeemed",
      fill: false,
      backgroundColor: window.chartColors.blue,
      borderColor: window.chartColors.blue,
      data: line2,
    }]
  },
  options: {
    responsive: true,
    title:{
      display: false,
      text:'Chart.js Line Chart'
    },
    tooltips: {
      mode: 'index',
      intersect: false,
    },
   hover: {
      mode: 'nearest',
      intersect: true
    },
    scales: {
      xAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Month'
        }
      }],
      yAxes: [{
        display: true,
        scaleLabel: {
          display: true,
        },
      }]
    }
  }
};

var ctx = document.getElementById("canvas").getContext("2d");
var myLine = new Chart(ctx, config);