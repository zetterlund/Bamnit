// Chart.js options
export const chartOptions1 = {
  maintainAspectRatio: false,
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
        stepSize: 10
        // callback: function(label, index, labels) {
        //   return Math.round(label*100)+'%';
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
    text: 'Total Teacher Absences in Austin',
    fontSize: 16,
  }
};



// Functions for colorizing the bars in the chart
export function getDayRelation(someDate) {
  someDate = new Date(someDate);
  const today = new Date();
  if (
    someDate.getUTCDate() == today.getUTCDate() &&
    someDate.getUTCMonth() == today.getUTCMonth() &&
    someDate.getUTCFullYear() == today.getUTCFullYear()
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
        backgroundColor.push("rgba(67,137,187,0.38)");
        hoverBackgroundColor.push("rgba(67,137,187,0.34)");
        borderWidth.push({
          top: 0,
          right: 2,
          bottom: 0,
          left: 0
        });        
        break;
      case "afterToday":
        backgroundColor.push("rgba(67,137,187,0.18)");
        hoverBackgroundColor.push("rgba(67,137,187,0.14)");
        borderWidth.push(0);
        break;
      case "beforeToday":
        backgroundColor.push("rgba(67,137,187,0.38)");
        hoverBackgroundColor.push("rgba(67,137,187,0.34)");
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
