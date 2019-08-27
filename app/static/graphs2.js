
    	// set chart global parameters
        Chart.defaults.global.legend.display = false;
        Chart.defaults.global.animation.duration = 1500;
        Chart.defaults.global.animation.easing = 'easeOutQuart';


        // get chart canvases
        var ctx1 = document.getElementById("myChart1").getContext("2d");



        

        function addDays(date, days) {
            var newDate = new Date(date.valueOf());
            newDate.setDate(newDate.getDate() + days);
            return newDate;
        }

        function getDates(startDate, stopDate) {
            var dateArray = new Array();
            var currentDate = startDate;
            while (currentDate <= stopDate) {
                dateArray.push(new Date (currentDate));
                currentDate = addDays(currentDate, 1);
            }
            return dateArray;
        }

        function dateToString(date) {
            date = date.toISOString();
            date = date.slice(0, 10);
            return date;
        }



        function generateEmptyDateRange() {
            var today = new Date();
            var beginDate = addDays(today, -28);
            var endDate = addDays(today, 7);

            var dateRange = getDates(beginDate, endDate);
            for (var i = 0; i < dateRange.length; i++) {
                dateRange[i] = dateRange[i].toISOString().slice(0, 10);
            }

            var dates = {};
            for (const d of dateRange) {
                dates[d] = 0;
            }

            return dates;
        }

        function populateDateRange(data) {
            var dates = generateEmptyDateRange();
            for (const d of data) {
                dates[d[0]] = d[1];
            }
            return dates;
        }




        


        var c1_legend = "My Legend";
        var c1_labels = [];

        var c1_totalValues = [];
        var totalData = populateDateRange(total_counts);
        for (const i of Object.entries(totalData)) {
            c1_labels.push(i[0]);
            c1_totalValues.push(i[1]);
        }

        var c1_jobValues = [];
        var jobData = populateDateRange(subject_counts['TCHR ASST']);
        for (const i of Object.entries(jobData)) {
            c1_jobValues.push(i[1]);
        }




        // define the chart data
        var chartData1 = {
            labels: c1_labels,
            datasets: [{
                label: c1_legend,
                fill: true,
                backgroundColor: "rgba(67,137,187,0.38)",
                hoverBackgroundColor: "rgba(67,137,187,0.6)",
                data: c1_totalValues,
                xAxisID: "bar-x-axis1",
                // yAxisID: "bar-y-axis1",
                spanGaps: false,
                // stack: 1
            }, {
                label: "My Job Data",
                fill: true,
                backgroundColor: "rgba(30,60,100,0.38)",
                hoverBackgroundColor: "rgba(30,60,100,0.6)",                
                data: c1_jobValues,
                xAxisID: "bar-x-axis2",
                // yAxisID: "bar-y-axis2",
                // stack: 2
            }]
        };
        

        // set chart options
        var chartOptions1 = {
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
                    id: "bar-y-axis1",
                    stacked: false,
                    type: 'linear',
                    ticks: {
                        beginAtZero: true,
                        min: 0,
                        // max: 100,
                        stepSize: 5
                        // callback: function(label, index, labels) {
                        //     return Math.round(label*100)+'%';
                        // }
                    },
                    scaleLabel: {
                        display: true,
                    }
                }],
                xAxes: [{
                    id: "bar-x-axis1",
                    stacked: true,
                    categoryPercentage: 1,
                    barPercentage: 1,
                    barThickness: 'flex',
                    ticks: {
                        autoSkip: false,
                    }
                }, {
                    id: "bar-x-axis2",
                    display: false,
                    offset: true,
                    stacked: true,
                    type: 'category',
                    categoryPercentage: 1,
                    barPercentage: 0.7,
                    barThickness: 'flex',
                    gridLines: {
                        offsetGridLines: true
                    }
                }]
            },
            title: {
                display: true,
                text: 'Distribution of teacher absences',
                fontSize: 14,
            }
        };






        // create the charts using the chart canvas
        var myChart1 = new Chart(ctx1, {
            type: 'bar',
            data: chartData1,
            options: chartOptions1,
        });
