import React from 'react'
import NavbarInstance from '../components/Navbar.js'
import Results from '../components/Results.js'
import HeatMap from '../components/HeatMap.js'
import ResultsTable from '../components/ResultsTable.js'
import ErrorModal from '../components/ErrorModal.js'

class App extends React.Component {

	constructor() {
    	super();
        this.state = {
        	term: '',
          error: false,
          errorText: 'hello',
          loaded: true,
          results: true,
        	tweets: [],
          pos: 0,
          neg: 0,
          neut: 0
        };
        this.onChange = this.onChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
        this.handleKeyPress = this.handleKeyPress.bind(this)
        this.handleModalClose = this.handleModalClose.bind(this)
    };

    handleModalClose() {
      this.setState({error: false});
    }

    onChange(e) {
    	this.setState({term: e.target.value});
  	};

    handleKeyPress(target) {
      if(target.charCode == 13) {
        this.handleSubmit();
      }
    };

    handleErrors(res) {
      if (!res.ok) {
        console.log(res)
        throw Error(res.error)
      }
      return res;
    }

    handleResponse(res) {
      res.tweets.length ? this.setState({results: true}) : this.setState({results: false})
      this.setState({tweets: res.tweets,
                     loaded: true,
                     pos: res.pos || 0,
                     neg: res.neg || 0,
                     neut: res.neut || 0})
    }

    handleSubmit() {
      this.setState({loaded: false})
  		fetch(`/search?term=${this.state.term}`, {method: "GET"})
        .then(this.handleErrors)
        .then(res => res.json())
        .then(res => this.handleResponse(res))
        .catch(err => this.setState({error: true, errorText: err}))
    };

   	render() {
  		return (
        <div>
          <NavbarInstance handleKeyPress={this.handleKeyPress}
                          onChange={this.onChange}
                          handleSubmit={this.handleSubmit} />
          <Results {...this.state} />
          <HeatMap tweets={this.state.tweets} loaded={this.state.loaded}/>
          <ResultsTable tweets={this.state.tweets} loaded={this.state.loaded} />
          {this.state.error ? <ErrorModal handleClose={this.handleModalClose} 
                                          error={this.state.errorText} /> 
          : null}
        </div>
  		);
   };
}

export default App;