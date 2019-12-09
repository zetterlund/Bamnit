

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
      stacked: false,
      type: 'linear',
      ticks: {
        beginAtZero: true,
        min: 0,
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
        if (window.innerWidth < 768) {
          factor = 7;
        } else if (window.innerWidth < 992) {
          factor = 2;
        } else {
          factor = 1;
        }



        // xLabels.forEach(function (label, i) {
        //   if (factor == 1) {

        //     var d = new Date(label);
        //     xLabels[i] = d.toLocaleDateString('en-US', {
        //       day: 'numeric',
        //       month: 'short'
        //     });

        //   } else if (factor == 2) {

        //     var d = new Date(label);
        //     xLabels[i] = d.toLocaleDateString('en-US', {
        //       day: 'numeric',
        //       month: 'short'
        //     });     
        //     if (i % factor != 0) {
        //         xLabels[i] = '';
        //     }            

        //   } else if (factor == 7) {

        //     var d = new Date(label);
        //     if (d.getDay() == 1) {
        //       xLabels[i] = d.toLocaleDateString('en-US', {
        //         day: 'numeric',
        //         month: 'short'
        //       });
        //     } else {
        //       xLabels[i] = '';
        //     }

        //   }




        });




        xLabels.forEach(function (labels, i) {

          if (i % factor != 0) {
              xLabels[i] = '';
          }
        });
      },

      id: "bar-x-axis1",
      stacked: true,
      categoryPercentage: 1,
      barPercentage: 1,
      barThickness: 'flex',
      gridLines: {
        display: true,
        color: (function(){
          var colors = new Array(36).fill('#E5E5E5');
          colors[colors.length - 7] = 'rgba(0,62,105,0.7)';
          return colors;
        })(),
        lineWidth: (function(){
          var lines = new Array(36).fill(1);
          lines[lines.length - 7] = 2;
          return lines;
        })(),
      },
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





// Function to help re-render more responsive Chart design
function resizeChartHelper(chart, size) {
  var yStepSize;
  if (window.innerWidth < 768) {
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


  // const today = new Date();

  // var today = new Date(Date().toLocaleString('en-US', {
  //     timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
  //   }));

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

