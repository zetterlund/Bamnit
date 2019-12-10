import {
  chartOptions1,
  chartOptions2,
  setChartHeight,
  getDayRelation,  
  colorizeBars,
} from './../functions/BarChart_functions.js'



// Chart.js global parameters
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



export class BarChart extends React.Component {
  constructor(props) {
    super(props);
    this.canvasRef = React.createRef();
    this.state = {
      'colorizedBars': colorizeBars(this.props.data.labels),
    };
  }

  componentDidUpdate() {
    this.myChart.data.labels = this.props.data.labels;
    this.myChart.data.datasets[1].data = this.props.data.totalValues;
    this.myChart.data.datasets[0].data = this.props.data.jobValues;
    this.myChart.data.classType = this.props.classType;
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
          backgroundColor: "rgba(30,60,100,0.55)",
          hoverBackgroundColor: "rgba(30,60,100,0.85)",
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
        }]
      },
    });      
  }

  render() {
    return (
      <canvas id="myCanvas" ref={this.canvasRef}
      />
    );
  }
}