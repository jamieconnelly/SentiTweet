import React from 'react'
import NavbarInstance from '../components/Navbar.js'
import Results from '../components/Results.js'
import HeatMap from '../components/HeatMap.js'

class App extends React.Component {

	constructor() {
    	super();
        this.state = {
        	term: '',
        	resp: false,
        	tweets: []
        };
        this.onChange = this.onChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
    };

    onChange(e) {
    	this.setState({term: e.target.value});
  	};

    handleSubmit() {
  		fetch(`/search?term=${this.state.term}`, {method: "GET"})
  		  .then((res) => res.json())
        .then((res) => this.setState({ resp: true, tweets: res.tweets}))
        .catch((err) => console.error(err));
    };

   	render() {
  		return (
        <div>
          <NavbarInstance onChange={this.onChange} handleSubmit={this.handleSubmit} />
          {this.state.resp ? <Results tweets={this.state.tweets}/> : null}
          <HeatMap />
        </div>
  		);
   };
}

export default App;