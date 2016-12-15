import React from 'react'

class App extends React.Component {

	constructor() {
    	super();
        this.state = { 
        	data: [],
        	value: '',
        	showResults: false,
        	results: {}
        };
        this.onChange = this.onChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
    };

    componentDidMount() {
        fetch('/api')
        .then((res) => res.json())
        .then((res) => {
        	console.log('first get', res.loaded)
        	return res;
        })
        .then((json) => this.setState({data: json.error}));
    };

    onChange(e) {
    	this.setState({value: e.target.value});
  	};

    handleSubmit() {
    	let formData = new FormData()
    	formData.append('term', this.state.value)
		
		fetch('/api', { method: 'POST', body: formData })
		.then((res) => res.json())
      	.then((resJson) => {
			this.setState({results: resJson.test, showResults: true});
      	})
      	.catch((error) => console.error(error));
    }

   	render() {
		return (
		 <div>
		  		Search terms:
		  		<input type="text" name="term" onChange={this.onChange} /><br/>
		  		<input type="submit" value="Submit" onClick={this.handleSubmit} />
			{this.state.showResults ? this.state.results : 'no'}
		 </div>
		);
   }
}

export default App;