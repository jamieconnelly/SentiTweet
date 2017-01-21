import React from 'react'
import NavbarInstance from '../components/Navbar.js'
import Results from '../components/Results.js'
import HeatMap from '../components/HeatMap.js'

class App extends React.Component {

	constructor() {
    	super();
        this.state = {
        	term: '',
          loaded: true,
        	tweets: [],
          pos: 0,
          neg: 0,
          neut: 0
        };
        this.onChange = this.onChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
    };

    onChange(e) {
    	this.setState({term: e.target.value});
  	};

    handleSubmit() {
      this.setState({loaded: false})
  		fetch(`/search?term=${this.state.term}`, {method: "GET"})
  		  .then((res) => res.json())
        .then((res) => this.setState({ tweets: res.tweets,
                                       loaded: true,
                                       pos: res.pos || 0,
                                       neg: res.neg || 0,
                                       neut: res.neut || 0 }))
        .catch((err) => console.error(err));
    };

   	render() {
  		return (
        <div>
          <NavbarInstance onChange={this.onChange} handleSubmit={this.handleSubmit} />
          <Results {...this.state} />
          <HeatMap tweets={this.state.tweets} loaded={this.state.loaded}/>
        </div>
  		);
   };
}

export default App;