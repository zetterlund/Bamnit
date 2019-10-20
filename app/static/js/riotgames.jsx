
function LoadingBox(props) {
  return (
    <div>
      <div id="loading-box">
        <p>Loading...</p>
      </div>
    </div>
  )
}

function ErrorBox(props) {
  if (props.error) {
    return (
      <div id="error-box">
        <span>{props.error}</span>
      </div>      
    )
  } else {
    return (
      <div></div>
    )
  }
}



class RiotGamesForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      champions: {
        champion0: '',
        champion1: '',
        champion2: '',
        champion3: '',
        champion4: '',
        champion5: '',
        champion6: '',
        champion7: '',
        champion8: '',
        champion9: '',
      },
      availableChamps: ['empty'],
      error: null
    }
    this.fetchChamps = this.fetchChamps.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.checkFormErrors = this.checkFormErrors.bind(this);
  }


  componentDidMount() {
    this.fetchChamps();
  }


  fetchChamps() {
    fetch("https://bamnit.com/static/riotgames/champ_list.json")
      .then(response => response.json())
      .then(result => {
        let champs = result.filter(i => {
          return i != null;
        });
        champs.unshift(['0', 'SELECT CHAMP']);
        this.setState({availableChamps: champs})
      });        
  }


  handleChange(event) {
    let name = event.target.name;
    let value = event.target.value;
    this.setState((prevState) => {
      prevState.champions[name] = value;
      return prevState;
    });
  }


  handleSubmit(event) {
    event.preventDefault();

    // Clear previous requests
    this.props.clearPrediction();
    this.setState({error: null});

    // Check for form errors
    let errorFound = this.checkFormErrors();

    // Call prediction function
    if (!errorFound) {
      this.props.onSubmit(this.state.champions);
    }
  }


  checkFormErrors() {
    
    // // Check for missing champions
    // for (let i in this.state.champions) {
    //   if (this.state.champions[i] == 0) {
    //     this.setState({error: 'Some champion is set to zero.'});
    //     return true;
    //   }
    // }

    // // Check for duplicate champions
    // let championSet = new Set();
    // for (let i of Object.values(this.state.champions)) {
    //   championSet.add(i);
    // }
    // if (championSet.size < 5) {
    //   this.setState({error: 'Duplicate champions selected.'});
    //   return true;
    // }

    return false;
  }


  render() {
    let champs = this.state.availableChamps;

    let champRow = (begin, end) => {
      return (
        Object.entries(this.state.champions).splice(begin, end).map(x => {
          return(
            <div class="col-xs-12 col-sm-6 col-md-5ths">
              <select value={x[1]} name={x[0]} onChange={this.handleChange}>
                {champs.map(champ => <option value={champ[0]}>{champ[1]}</option>)}
              </select>
            </div>
          )
        })
      )
    }

    return (
      <div>
        <ErrorBox error={this.state.error} />
        <form onSubmit={this.handleSubmit}>
          <div class="team-box" id="team-1-box">
            <div class="row">
              <div class="col-xs-12">
                <p class="team-label">Team 1</p>
              </div>
            </div>
            <div class="row">
              {champRow(0, 5)}
            </div>
          </div>
          <div class="team-box" id="team-2-box">
            <div class="row">
              <div class="col-xs-12">
                <p class="team-label">Team 2</p>
              </div>
            </div>
            <div class="row">
              {champRow(5, 10)}
            </div>
          </div>
          <div class="row">
            <div class="col-xs-12">
              <button>Submit</button>
            </div>
          </div>
        </form>
      </div>
    );
  }
}



class PredictionResults extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      winningTeam: '',
      confidence: ''
    }

    this.componentDidUpdate = this.componentDidUpdate.bind(this);
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    if (this.props.predictionResults['winningTeam'] != prevProps.predictionResults['winningTeam']) {
      let teamLookup;
      switch (this.props.predictionResults['winningTeam']) {
        case '100':
          teamLookup = '1';
          break;
        case '200':
          teamLookup = '2';
          break;
      }
      this.setState({
        winningTeam: teamLookup,
        confidence: this.props.predictionResults['confidence']
      });
    }
  }

  render() {

    let predictionStatement;
    if (this.state.winningTeam != '' && this.state.confidence != '') {
      predictionStatement = (
          <div>
            <p id="prediction-label">Prediction:</p>
            <div>
              <span class="prediction-statement" id={"team" + this.state.winningTeam}>
                <span class="prediction-statistic">Team {this.state.winningTeam}</span> has a <span class="prediction-statistic">{this.state.confidence}%</span> chance of winning!
              </span>
            </div>
          </div>
      );
    }

    return (
      <div class="row">
        <div class="col-xs-12">
          <div id="prediction-box">
            {predictionStatement}
            {this.props.loading && <LoadingBox />}
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
      predictionResults: {
        winningTeam: '',
        confidence: ''
      },
      loading: false
    }
    this.handleSubmit = this.handleSubmit.bind(this);
    this.clearPrediction = this.clearPrediction.bind(this);
  }

  handleSubmit(data) {
    this.setState({loading: true})
    let postResponse;
    $.post("https://bamnit.com/riot/get_prediction", data, function(response) {
      postResponse = response;
    }).then(() => {
      this.setState({predictionResults: postResponse});
      this.setState({loading: false})
    });
  }

  clearPrediction() {
    this.setState({predictionResults: {
      winningTeam: '',
      confidence: ''
    }});
  }  

  render() {
    return(
      <div>
        <RiotGamesForm
          onSubmit={(a) => this.handleSubmit(a)}
          clearPrediction={() => this.clearPrediction()}
        />
        <PredictionResults
          predictionResults={this.state.predictionResults}
          loading={this.state.loading}
        />
        <div id="match-results"></div>
      </div>
    )
  }
}



ReactDOM.render(<App />, document.getElementById('riot-games-root'));