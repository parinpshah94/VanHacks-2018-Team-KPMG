      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Year', 'Collected', 'Redeemed'],
          ['2004',  1000,      400],
          ['2005',  1170,      460],
          ['2006',  660,       1120],
          ['2007',  1030,      540]
        ]);

        var options = {
          //title: 'Company Performance',
          //curveType: 'function',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart'));

        chart.draw(data, options);
      }

var chPage = document.getElementsByClassName('chPage');
for(let i = 0; i < chPage.length; i++) {
  chPage[i].addEventListener('click', changePage);
}
var nowActive = chPage[0];
function changePage(e) {
  if (nowActive != this) {
    nowActive.classList.remove('active');
    nowActive = this;
    nowActive.classList.add('active');
  }
  if (nowActive.innerHTML == "HOME") {
    document.getElementById('main').style.display = "inline-block";
    document.getElementById('orders').style.display = "none";
    document.getElementById('product').style.display = "none";
  }
  if (nowActive.innerHTML == "ORDERS") {
    document.getElementById('main').style.display = "none";
    document.getElementById('orders').style.display = "inline-block";
    document.getElementById('product').style.display = "none";
  }
  if (nowActive.innerHTML == "PRODUCT") {
    document.getElementById('main').style.display = "none";
    document.getElementById('orders').style.display = "none";
    document.getElementById('product').style.display = "inline-block";
  }
}
