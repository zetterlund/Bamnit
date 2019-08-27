

// set chart global parameters
Chart.defaults.global.legend.display = false;
Chart.defaults.global.animation.duration = 1000;
Chart.defaults.global.animation.easing = 'easeOutQuart';
Chart.defaults.global.defaultFontFamily = "Roboto, sans-serif";



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
        callbacks: {
            label: function(tooltipItem) {
                return tooltipItem.yLabel;
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



class BarChart extends React.Component {
  constructor(props) {
    super(props);
    this.canvasRef = React.createRef();
  }

  componentDidUpdate() {
    this.myChart.data.labels = this.props.data.labels;
    this.myChart.data.datasets[0].data = this.props.data.totalValues;
    this.myChart.data.datasets[1].data = this.props.data.jobValues;
    this.myChart.data.datasets[0].backgroundColor = this.props.backgroundColor;
    this.myChart.update();
  }

  componentDidMount() {
    this.myChart = new Chart(this.canvasRef.current, {
      type: 'bar',
      options: chartOptions1,
      data: {
        labels: this.props.data.labels,
        datasets: [{
          label: this.props.title,
          fill: true,
          backgroundColor: this.props.backgroundColor,
          hoverBackgroundColor: "rgba(67,137,187,0.6)",
          data: this.props.data.totalValues,
          xAxisID: "bar-x-axis1",
          // yAxisID: "bar-y-axis1",
          spanGaps: false,
          // stack: 1
        }, {
          label: "My Job Data",
          fill: true,
          backgroundColor: "rgba(30,60,100,0.38)",
          hoverBackgroundColor: "rgba(30,60,100,0.6)",                
          data: this.props.data.jobValues,
          xAxisID: "bar-x-axis2",
          // yAxisID: "bar-y-axis2",
          // stack: 2
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



function TypeButton(props) {
  return(
    <li><a onClick={props.onClick}>{props['data-target']}</a></li>
  )
}

function TypeList(props) {
  return (
    props.targets.map(function(target) {
      return(
        <TypeButton
          data-target={target.name}
          data-lookupType={props.lookupType}
          onClick={function() {
            return (props.handleClick(target.name, props.lookupType));
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
        <input type="text" value={this.state.searchString} onChange={this.handleChange} placeholder="Search!" />
        <h2>Grades</h2>
        <ul>
          <TypeList targets={grades} lookupType="grade" handleClick={(a, b) => this.props.handleClick(a, b)} />
        </ul>
        <h2>Subjects</h2>
        <ul>
          <TypeList targets={subjects} lookupType="subject" handleClick={(a, b) => this.props.handleClick(a, b)} />
        </ul>        
      </div>
    )
  }
}



class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: getData('TCHR ASST HIGH SCHOOL ONE TO O', 'subject'),
      backgroundColor: "rgba(67,137,187,0.38)"
    };
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(target, lookupType) {
    this.setState(function(prevState) {
      let state = prevState;
      state.data = getData(target, lookupType)
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
                  title="My awesome title"
                  backgroundColor={this.state.backgroundColor}
                  height="500"
                />
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-xs-12">
            <DynamicSearch handleClick={(a, b) => this.handleClick(a, b)} subjects={subjectList} grades={gradeList} />
          </div>
        </div>
      </div>
    );
  }
}



ReactDOM.render(<App />, document.getElementById('root'));
