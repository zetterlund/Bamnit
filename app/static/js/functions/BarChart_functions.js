

// Chart.js options
export const chartOptions1 = {
  maintainAspectRatio: false,
  onResize: function(chart, size) {
    resizeChartHelper(chart, size);
  },
  tooltips: {
    yAlign: 'bottom',
    xAlign: 'center',
    position: 'custom',
    displayColors: false,
    mode: 'index',
    animationDuration: 0,
    bodyFontSize: 14,
    cornerRadius: 5,
    caretSize: 10,
    caretPadding: 0,
    backgroundColor: 'rgba(255, 255, 255, 0.7)',
    bodyFontColor: '#000000',
    bodySpacing: 4,
    xPadding: 10,
    yPadding: 10,
    borderColor: "rgba(0, 0, 0, 0.6)",
    borderWidth: 2,
    // filter: function (tooltipItem) {
    //   return tooltipItem.datasetIndex === 0;
    // },    
    callbacks: {
      title: function(tooltipItem) {
        return;
      },
      label: function(tooltipItem, data) {
        if (tooltipItem.datasetIndex == 0) {
          return ([
            data.classType,
            tooltipItem.yLabel + " opening" + (tooltipItem.yLabel == 1 ? "" : "s") + " on " + tooltipItem.label
          ]);          
        } else {
          return;
        }
      },
      labelColor: function(tooltipItem, data) {
        return {
          borderColor: 'rgb(255, 0, 0)',
          backgroundColor: 'rgb(255, 0, 0)'
        };
      },
    },
  },
  scales: {
    yAxes: [{
      id: "bar-y-axis1",
      gridLines: {
        drawTicks: false,
      },
      stacked: false,
      type: 'linear',
      ticks: {
        beginAtZero: true,
        min: 0,
        padding: 10,
        stepSize: (function(){
          if (window.innerWidth < 768) {
            return 30;
          } else if (window.innerWidth < 992) {
            return 20;
          } else {
            return 10;
          }  
        })(),
      },
      scaleLabel: {
        display: true,
      }
    }],
    xAxes: [{
      afterTickToLabelConversion: function(data) {
        var xLabels = data.ticks;
        var factor;
        if (window.innerWidth < 992) {
          factor = 7;
        } else {
          factor = 1;
        }
        xLabels.forEach(function (label, i) {
          if (factor == 1) {
            xLabels[i] = getDateString(label);
          } else if (factor == 7) {
            var date = new Date(label);
            if (date.getUTCDay() == 1) {
              xLabels[i] = getDateString(label);
            } else {
              xLabels[i] = '';
            }
          }
        });
      },
      id: "bar-x-axis1",
      stacked: true,
      categoryPercentage: 1,
      barPercentage: 1,
      barThickness: 'flex',
      gridLines: getXGridLines(),
      ticks: {
        autoSkip: false,
        padding: 10,
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
        // display: false,
        offsetGridLines: true
      },
    }]
  },
  title: {
    display: true,
    text: 'Total Teacher Absences in Austin',
    fontSize: 16,
  }
};



function getXGridLines() {
  var utcDate = new Date().getUTCDate();
  var today = new Date().getDate();
  var lookback;
  if (utcDate == today) {
    lookback = 7;
  } else {
    lookback = 8;
  }

  var result = {}

  result['display'] = true;
  result['drawTicks'] = false;

  result['color'] = (function() {
    var colors = new Array(36).fill('#E5E5E5');
    colors[colors.length - lookback] = 'rgba(0,62,105,0.7)';
    return colors;
  })();

  result['lineWidth'] = (function() {
    var lines = new Array(36).fill(1);
    lines[lines.length - lookback] = 2;
    return lines;
  })();

  return result;
}



function getDateString(date) {
  var monthList = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'];
  var dateString = '';
  date = new Date(date);
  dateString += monthList[date.getUTCMonth()];
  dateString += ' ';
  dateString += date.getUTCDate();
  return dateString;
}



// Function to help re-render more responsive Chart design
function resizeChartHelper(chart, size) {
  var yStepSize;
  if (window.innerWidth < 576) {
    yStepSize = 50;
  } else if (window.innerWidth < 768) {
    yStepSize = 30;
  } else if (window.innerWidth < 992) {
    yStepSize = 20;
  } else {
    yStepSize = 10;
  }
  chart.options.scales.yAxes[0].ticks.stepSize = yStepSize;
  chart.update();
}



// Functions for colorizing the bars in the chart
export function getDayRelation(someDate) {
  someDate = new Date(someDate);
  someDate = new Date(
    someDate.getUTCFullYear().toString() + '-' +
    (someDate.getUTCMonth()+1).toString() + '-' +
    someDate.getUTCDate().toString()
  );

  var today = new Date();

  if (
    someDate.getUTCDate() == today.getDate() &&
    someDate.getUTCMonth() == today.getMonth() &&
    someDate.getUTCFullYear() == today.getFullYear()
  ) {
    return "today";
  } else if (someDate > today) {
    return "afterToday";
  } else {
    return "beforeToday";
  }
}



// export function getTestDate(labels) {
//   var result = [];
//   for (var i=0; i<labels.length; i++) {
//     result.push([labels[i], getDayRelation(labels[i])]);
//   }
//   return result;
// }



export function colorizeBars(labels) {
  const backgroundColor = [];
  const hoverBackgroundColor = [];
  const borderWidth = [];
  for (var i=0; i<labels.length; i++) {
    switch (getDayRelation(labels[i])) {
      case "today":
        backgroundColor.push("rgba(67,137,187,0.45)");
        hoverBackgroundColor.push("rgba(67,137,187,0.32)");
        borderWidth.push(
          0
        // {
        //   top: 0,
        //   right: 2,
        //   bottom: 0,
        //   left: 0
        // }
        );        
        break;
      case "afterToday":
        backgroundColor.push("rgba(67,137,187,0.25)");
        hoverBackgroundColor.push("rgba(67,137,187,0.14)");
        borderWidth.push(0);
        break;
      case "beforeToday":
        backgroundColor.push("rgba(67,137,187,0.45)");
        hoverBackgroundColor.push("rgba(67,137,187,0.32)");
        borderWidth.push(0);
        break;
    }
  }

  const colorizedBars = {
    'backgroundColor': backgroundColor,
    'hoverBackgroundColor': hoverBackgroundColor,
    'borderWidth': borderWidth,
  };
  return colorizedBars;
}

