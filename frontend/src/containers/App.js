import React from 'react'
import NavbarInstance from '../components/Navbar.js'
import Results from '../components/Results.js'
import HeatMap from '../components/HeatMap.js'
import ResultsTable from '../components/ResultsTable.js'

class App extends React.Component {

	constructor() {
    	super();
        this.state = {
        	term: '',
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
    };

    onChange(e) {
    	this.setState({term: e.target.value});
  	};

    handleKeyPress(target) {
      if(target.charCode == 13) {
        this.handleSubmit();
      }
    };

    handleSubmit() {
      this.setState({loaded: false})
  		fetch(`/search?term=${this.state.term}`, {method: "GET"})
  		  .then((res) => res.json())
        .then((res) => {
          res.tweets.length ? 
            this.setState({results: true}) :
            this.setState({results: false})
          this.setState({tweets: res.tweets,
                         loaded: true,
                         pos: res.pos || 0,
                         neg: res.neg || 0,
                         neut: res.neut || 0 })
        })
        .catch((err) => console.error(err));
    };
    // {this.state.tweets.length ? 
   	render() {
  		return (
        <div>
          <NavbarInstance handleKeyPress={this.handleKeyPress}
                          onChange={this.onChange}
                          handleSubmit={this.handleSubmit} />
          <Results {...this.state} />
          <HeatMap tweets={this.state.tweets} loaded={this.state.loaded}/>
          <ResultsTable tweets={this.state.tweets} />
        </div>
  		);
   };
}

export default App;