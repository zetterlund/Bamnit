
// Functional component to display currently selected item
function DisplayCurrentClass(props) {
  const courseCount = props.classTypeCounts[props.lookupType][props.classType];
  return (
    <div id="display-current-class">
      <p><span class="class-type">{props.classType}</span></p>
      <p><span class="course-count">{courseCount}</span> total openings</p>
    </div>
  )
}



function ExpandButton(props) {
  return(
    <div class="expand-course-list">
      <a onClick={props.onClick}>
        ({props.expanded ? ("Hide additional jobs") : ("Show " + props.additionalCount + " more")})
      </a>
    </div>
  )
}



// Functional components to display available courses in a list
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



class TypeList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      expanded: false,
      displayLimit: 15
    };
    this.expandList = this.expandList.bind(this);
  }

  expandList() {
    this.setState((prevState) => ({expanded: !prevState.expanded}));
  }

  render() {
    let courses = this.props.targets.map(x => x.name);
    const sort1 = this.props.classTypeCounts;
    const sort2 = this.props.lookupType;
    courses.sort(function(a,b) {
      return sort1[sort2][a] - sort1[sort2][b];
    }).reverse();

    let additionalCount = 0
    let showExpandButton = false;
    if (courses.length > this.state.displayLimit) {
      additionalCount = courses.length - this.state.displayLimit;
      showExpandButton = true;
    }

    if (showExpandButton == true && this.state.expanded == false) {
      courses = courses.slice(0, this.state.displayLimit);
    }

    return (
      <div>
        <ul className="courses-list">
          {courses.map(function(course) {
            return(
              <TypeButton
                data-buttonClass={"list-item" + (this.props.currentClassType == course && this.props.currentLookupType == this.props.lookupType ? " selected" : "")}
                data-target={course}
                data-count={this.props['classTypeCounts'][this.props.lookupType][course]}
                data-lookupType={this.props.lookupType}
                onClick={() => this.props.handleClick(course, this.props.lookupType)}
              />
            )
          }, this)}
        </ul>
        {showExpandButton == true &&
          <ExpandButton
            onClick={() => this.expandList()}
            additionalCount={additionalCount}
            expanded={this.state.expanded}
          />
        }
      </div>
    )
  }
}



// Component to search and filter available courses
export class DynamicSearch extends React.Component {
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
            <DisplayCurrentClass
            	classTypeCounts={this.props.classTypeCounts}
            	classType={this.props.currentClassType}
            	lookupType={this.props.currentLookupType} />
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
            <TypeList
              targets={grades}
              lookupType="grade"
              handleClick={(a, b) => this.props.handleClick(a, b)}
              classTypeCounts={this.props.classTypeCounts}
              currentClassType={this.props.currentClassType}
              currentLookupType={this.props.currentLookupType}
            />
          </div>
          <div class="col-xs-12 col-sm-6 col-md-5">
            <h3>Subjects</h3>
            <TypeList
              targets={subjects}
              lookupType="subject"
              handleClick={(a, b) => this.props.handleClick(a, b)}
              classTypeCounts={this.props.classTypeCounts}
              currentClassType={this.props.currentClassType}
              currentLookupType={this.props.currentLookupType}
            />
          </div>
        </div>
      </div>
    )
  }
}