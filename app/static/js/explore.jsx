import {BarChart} from './components/BarChart'
import {DynamicSearch} from './components/DynamicSearch'
import {getClassTypeCounts, getData, loadCourseList} from './functions/App_functions'



class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      classType: 'FIFTH GRADE',
      lookupType: 'grade',
      data: getData('FIFTH GRADE', 'grade'),
      classTypeCounts: getClassTypeCounts(),
      subjectList: loadCourseList('subject'),
      gradeList: loadCourseList('grade')
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
                  classType={this.state.classType}
                  // height="500"
                />
              </div>
            </div>
          </div>
        </div>
        <DynamicSearch
          classTypeCounts={this.state.classTypeCounts}
          currentClassType={this.state.classType}
          currentLookupType={this.state.lookupType}
          handleClick={(a, b) => this.handleClick(a, b)}
          subjects={this.state.subjectList}
          grades={this.state.gradeList}
        />
      </div>
    );
  }
}



ReactDOM.render(<App />, document.getElementById('graph-root'));