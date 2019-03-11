
    	// set chart global parameters
        Chart.defaults.global.legend.display = false;
        Chart.defaults.global.animation.duration = 1500;
        Chart.defaults.global.animation.easing = 'easeOutQuart';


        // get chart canvases
        var ctx1 = document.getElementById("myChart1").getContext("2d");
        var ctx2 = document.getElementById("myChart2").getContext("2d");


        // define the chart data
        var chartData1 = {
            labels : c1_labels,
            datasets : [{
                label: c1_legend,
                fill: true,
                backgroundColor: "rgba(67,137,187,0.38)",
                hoverBackgroundColor: "rgba(67,137,187,0.6)",
                data : c1_values,
            }]
        };

        var chartData2 = {
            labels : c2_labels,
            datasets : [{
                label: c2_legend,
                fill: true,
                backgroundColor: "rgba(67,137,187,0.38)",
                hoverBackgroundColor: "rgba(67,137,187,0.6)",
                data : c2_values,
                spanGaps: false
            }]
        }


        // set chart options
        var chartOptions1 = {
            tooltips: {
                callbacks: {
                    label: function(tooltipItem) {
                        return Math.round(tooltipItem.yLabel*100)+'%';
                    }
                }
            },
            scales: {
                yAxes: [{
                    type: 'linear',
                    ticks: {
                        beginAtZero: true,
                        max: 0.4,
                        callback: function(label, index, labels) {
                            return Math.round(label*100)+'%';
                        }
                    },
                    scaleLabel: {
                        display: true,
                    }
                }],
                xAxes: [{
                    ticks: {
                        autoSkip: false,
                    },
                }]
            },
            title: {
                display: true,
                text: 'Distribution of teacher absences',
                fontSize: 14,
            }
        };

        var chartOptions2 = {
            tooltips: {
                callbacks: {
                    label: function(tooltipItem) {
                        var foo = tooltipItem.yLabel;
                        return computeTime(foo);
                    }
                },
            },
            scales: {
                yAxes: [{
                    type: 'linear',
                    ticks: {
                        beginAtZero: true,
                        min: 0,
                        stepSize: 14400,
                        callback: function(label, index, labels) {
                            return computeTime(label, true);
                        }
                    },
                    scaleLabel: {
                        display: true,
                    }
                }],
                xAxes: [{
                    ticks: {
                        autoSkip: false,
                    },
                }]
            },
            title: {
                display: true,
                text: 'Average time it takes to fill an absence',
                fontSize: 14,
            }
        };


        // create the charts using the chart canvas
        var myChart1 = new Chart(ctx1, {
            type: 'bar',
            data: chartData1,
            options: chartOptions1,
        });

        var myChart2 = new Chart(ctx2, {
            type: 'bar',
            data: chartData2,
            options: chartOptions2,
        });


        // a helper function for properly displaying time formats in graphs
        function computeTime(secs, hours_only) {
            var t = moment.utc(secs*1000);
            var h = t.format('H');
            var m = t.format('m');
            if (secs >= 86400) {
                h = (parseInt(h, 10) + 24).toString();
            };
            if (hours_only == true) {
                return h + ' hours'              
            };
            return h + ' hours, ' + m + ' min';
        }
