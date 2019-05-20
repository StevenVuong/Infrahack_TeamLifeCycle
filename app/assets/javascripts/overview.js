var createDoughnutChart = function(identifier, charging, discharging, callback){
    
    var ctx = document.getElementById(identifier).getContext('2d');
    var myDoughnutChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [
                {
                    data: [charging,discharging,0],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                },
            ],
        
            // These labels appear in the legend and in the tooltips when hovering different arcs
            labels: [
                'Charging',
                'Discharging'
            ]
        },
        options: {
            circumference: Math.PI,
            rotation: Math.PI
        }
    });
    if(typeof(callback) !== 'function') return;
    callback(myDoughnutChart);
}



var createLineChart2 = function(identifier, xAxis, values, values2, callback){
    var ctx = document.getElementById(identifier).getContext('2d');

    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: xAxis,
            datasets: [{
                label: 'Dumb',
                data: values,
                borderColor: [
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            },
            {
                label: 'Smart',
                data: values2,
                borderColor: [
                    'rgba(54, 162, 235, 0.2)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            title: {
                display: true,
                text: "Real Time Demand Chart"
            }
        }
    });
    if(typeof(callback) !== 'function') return;
    callback(chart);
}

var createLineChart = function(identifier, xAxis, values, callback){
    var ctx = document.getElementById(identifier).getContext('2d');

    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: xAxis,
            datasets: [{
                label: 'Demand',
                data: values,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
    if(typeof(callback) !== 'function') return;
    callback(chart);
}


