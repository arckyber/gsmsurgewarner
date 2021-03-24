$(document).ready(function(){
    Chart.defaults.global.responsive = false;

		// var times = {{times|safe}};

		// var data = {{water_distance|safe}};

    var times = ['jan', 'feb', 'mar', 'apr'];

    var data = [4, 3, 5, 2];

		var legend = "Water distance from sensor";

		var chartData = {
			labels : times,
			datasets: [
				{
					label: legend,
					fill: true,
					lineTension: 0.1,
					backgroundColor: "rgba(75,192,192,0.4)",
					borderColor: "rgba(75,192,192,1)",
					borderCapStyle: 'butt',
					borderDash: [],
					borderDashOffset: 0.0,
					borderJoinStyle: 'miter',
					pointBorderColor: "rgba(75,192,192,1)",
					pointBackgroundColor: "#fff",
					pointBorderWidth: 1,
					pointHoverRadius: 5,
					pointHoverBackgroundColor: "rgba(75,192,192,1)",
					pointHoverBorderColor: "rgba(220,220,220,1)",
					pointHoverBorderWidth: 2,
					pointRadius: 1,
					pointHitRadius: 10,
					data: data,
					spanGaps: false,
					options: {
						scales: {
							yAxes: [{
								ticks: {
									reverse: true,
									beginAtZero:true,
									start: 0,
									callback: function(value, index, values) {
										return value + "m";
									},
								}
							}],
							xAxes: [{
									ticks: {
									reverse: true,
									beginAtZero: true,
									start: 0,
								}
							}]
						},
						rotation: (0.5 * Math.PI)
					}
				}
			]
		};

		var holder = document.getElementById("myChart");
		var ctx = document.getElementById("myChart").getContext("2d");

		// create the chart using the chart canvas
		var myChart = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
          tooltips: {
            enabled: true,
            mode: 'single',
            callbacks: {
              label: function(tooltipItems, data) {
					return tooltipItems.yLabel + ' degrees';
				}
            }
          },
        }
      });

      // get the text element below the chart
      var pointSelected = document.getElementById("pointSelected");

      // create a callback function for updating the selected index on the chart
      holder.onclick = function(evt){
        var activePoint = myChart.getElementAtEvent(evt);
        console.log(activePoint);
        console.log('x:' + activePoint[0]._view.x);
        console.log('maxWidth: ' + activePoint[0]._xScale.maxWidth);
        console.log('y: ' + activePoint[0]._view.y);
        console.log('index: ' + activePoint[0]._index);
        pointSelected.innerHTML = 'Point selected... index: ' + activePoint[0]._index;
      };

	//   $('#datePicker1').val(new Date().toDateInputValue());
  })