

// set chart global parameters
Chart.defaults.global.legend.display = false;
Chart.defaults.global.animation.duration = 750;
Chart.defaults.global.animation.easing = 'easeOutQuart';
Chart.defaults.global.defaultFontFamily = "Roboto, sans-serif";


Chart.Tooltip.positioners.custom = function(elements, position) {
    const x = elements[0]._model.x + 0;
    const y = elements[0]._model.y - 15;
    return {
        x: x,
        y: y
    };
};


// add helper functions
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

function getData(target, lookupType) {
  let labels = [];
  let totalValues = [];
  let totalData = populateDateRange(total_counts)
  for (const i of Object.entries(totalData)) {
    labels.push(i[0]);
    totalValues.push(i[1]);
  }

  let jobValues = [];
  let lookupDict = {
    'subject': subject_counts,
    'grade': grade_counts
  };
  let jobData = populateDateRange(lookupDict[lookupType][target]);
  for (const i of Object.entries(jobData)) {
    jobValues.push(i[1]);
  }

  let data = {
    labels: labels,
    totalValues: totalValues,
    jobValues: jobValues
  };

  return data;
}



let subjectList = Object.keys(subject_counts).map(function(subject) {
  return ({"name": subject});
});

let gradeList = Object.keys(grade_counts).map(function(grade) {
  return ({"name": grade});
})











// set chart options
var chartOptions1 = {
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
        //     return tooltipItem.datasetIndex === 0;
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
        text: 'Total Teacher Absences in Austin',
        fontSize: 16,
    }
};






// functions for colorizing the "Today" bar in the chart
function getDayRelation(someDate) {
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

function colorizeBars(labels) {
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



class BarChart extends React.Component {
  constructor(props) {
    super(props);
    this.canvasRef = React.createRef();
    this.state = {
      'colorizedBars': colorizeBars(this.props.data.labels)
    }
  }

  componentDidUpdate() {
    this.myChart.data.labels = this.props.data.labels;
    this.myChart.data.datasets[1].data = this.props.data.totalValues;
    this.myChart.data.datasets[0].data = this.props.data.jobValues;
    this.myChart.data.classType = this.props.classType
    // this.myChart.data.datasets[1].backgroundColor = this.props.backgroundColor;
    this.myChart.update();
  }

  componentDidMount() {
    this.myChart = new Chart(this.canvasRef.current, {
      type: 'bar',
      options: chartOptions1,
      data: {
        classType: this.props.classType,
        labels: this.props.data.labels,
        datasets: [{
          label: "My Job Data",
          fill: true,
          backgroundColor: "rgba(30,60,100,0.45)",
          hoverBackgroundColor: "rgba(30,60,100,0.7)",                
          data: this.props.data.jobValues,
          xAxisID: "bar-x-axis2",
          // yAxisID: "bar-y-axis2",
          // stack: 2
        }, {
          label: this.props.title,
          fill: true,
          backgroundColor: this.state.colorizedBars['backgroundColor'],
          hoverBackgroundColor: this.state.colorizedBars['hoverBackgroundColor'],
          borderColor: "rgba(137,0,0,0.5)",
          borderWidth: this.state.colorizedBars['borderWidth'],
          data: this.props.data.totalValues,
          xAxisID: "bar-x-axis1",
          // yAxisID: "bar-y-axis1",
          spanGaps: false,
          // stack: 1
        }]
      }
    });
  }

  render() {
    return (
        <canvas ref={this.canvasRef} height="540" />
    );
  }
}



// Get the total number of jobs for each classType
function getClassTypeCounts() {
  const gradeCounts = {};
  const subjectCounts = {};

  const counts = {
    'grade': gradeCounts,
    'subject': subjectCounts
  };

  Object.entries(grade_counts).map(function(x) {
    gradeCounts[x[0]] = (x[1].map((y) => y[1]).reduce((a,b) => a + b, 0));
  });
  Object.entries(subject_counts).map(function(x) {
    subjectCounts[x[0]] = (x[1].map((y) => y[1]).reduce((a,b) => a + b, 0));
  });  

  return counts;
}
const classTypeCounts = getClassTypeCounts();






function DisplayCurrentClass(props) {
  const courseCount = classTypeCounts[props.lookupType][props.classType];
  return (
    <div id="display-current-class">
      <p><span class="class-type">{props.classType}</span></p>
      <p><span class="course-count">{courseCount}</span> total openings</p>
    </div>
  )
}





// functional components rendered by the DynamicSearch component
function TypeButton(props) {
  return(
    <li className={props['data-buttonClass']}>
      <div>
        <span>({props['data-count']})</span>
        <a onClick={props.onClick}>{props['data-target']}</a>
      </div>
    </li>
  )
}

function TypeList(props) {
  const courses = props.targets.map(x => x.name)
  courses.sort(function(a,b) {
    return classTypeCounts[props.lookupType][a] - classTypeCounts[props.lookupType][b];
  }).reverse();

  return (
    courses.map(function(course) {
      return(
        <TypeButton
          data-buttonClass={"list-item" + (props.currentClassType == course && props.currentLookupType == props.lookupType ? " selected" : "")}
          data-target={course}
          data-count={classTypeCounts[props.lookupType][course]}
          data-lookupType={props.lookupType}
          onClick={function() {
            return (props.handleClick(course, props.lookupType));
          }}
        />        
      )
    })

  )
}



class DynamicSearch extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      searchString: ''
    };
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange() {
    this.setState(function(prevState) {return {searchString: event.target.value}});
    console.log("Scope updated!");
  }

  render() {
    var subjects = this.props.subjects;
    var grades = this.props.grades;
    var searchString = this.state.searchString.trim().toLowerCase();

    if (searchString.length > 0) {
      subjects = subjects.filter(subject => subject.name.toLowerCase().match(searchString));
      grades = grades.filter(grade => grade.name.toLowerCase().match(searchString));
    }

    return (      
      <div>
        <div class="row">
          <div class="col-xs-12">
            <DisplayCurrentClass classType={this.props.currentClassType} lookupType={this.props.currentLookupType} />
          </div>
        </div>
        <div class="row">
          <div class="col-xs-12 col-md-4">
            <div id="classes-filter">
              <label>Filter classes</label>
              <br />
              <input type="text" value={this.state.searchString} onChange={this.handleChange} placeholder="Search!" />
            </div>
          </div>
          <div class="col-xs-12 col-sm-6 col-md-3">
            <h3>Grades</h3>
            <ul className="courses-list">
              <TypeList
                targets={grades}
                lookupType="grade"
                handleClick={(a, b) => this.props.handleClick(a, b)}
                currentClassType={this.props.currentClassType}
                currentLookupType={this.props.currentLookupType}
              />
            </ul>
          </div>
          <div class="col-xs-12 col-sm-6 col-md-5">
            <h3>Subjects</h3>
            <ul className="courses-list">
              <TypeList
                targets={subjects}
                lookupType="subject"
                handleClick={(a, b) => this.props.handleClick(a, b)}
                currentClassType={this.props.currentClassType}
                currentLookupType={this.props.currentLookupType}
              />
            </ul>
          </div>
        </div>
      </div>
    )
  }
}



class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      classType: 'FIFTH GRADE',
      lookupType: 'grade',
      data: getData('FIFTH GRADE', 'grade'),
    };
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(target, lookupType) {
    this.setState(function(prevState) {
      let state = prevState;
      state.data = getData(target, lookupType);
      state.classType = target;
      state.lookupType = lookupType;
      return state;
    })
  }

  render() {
    return (
      <div>
        <div class="row chart-row">
          <div class="col-xs-12">
            <div className="App">
              <div className="sub chart-wrapper">
                <BarChart
                  data={this.state.data}
                  // title="My awesome title"
                  classType={this.state.classType}
                  height="500"
                />
              </div>
            </div>
          </div>
        </div>
        <DynamicSearch
          currentClassType={this.state.classType}
          currentLookupType={this.state.lookupType}
          handleClick={(a, b) => this.handleClick(a, b)}
          subjects={subjectList}
          grades={gradeList}
        />
      </div>
    );
  }
}



ReactDOM.render(<App />, document.getElementById('graph-root'));
