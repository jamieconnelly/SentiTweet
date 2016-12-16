import React from 'react'
import styles from './style.css';

class App extends React.Component {

	constructor() {
    	super();
        this.state = {
        	term: '',
        	resp: false,
        	results: ''
        };
        this.onChange = this.onChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
    };

    onChange(e) {
    	this.setState({term: e.target.value});
  	};

    handleSubmit() {
		fetch(`/api?term=${this.state.term}`, {method: "GET"})
		.then((res) => res.json())
      	.then((res) => this.setState({ resp: true, results: res.result }))
      	.catch((err) => console.error(err));
    };

   	render() {
		return (
		 <div>
	  		<input className={styles.form}
	  			   placeholder="Enter search term..." 
	  			   type="text"
	  			   onChange={this.onChange} />
	  		<input className={`${styles.primaryButton} ${styles.btndefault}`} 
	  			   type="submit"
	  			   value="Submit"
	  			   onClick={this.handleSubmit} />
	  		{this.state.resp ? <p>Results are: {this.state.results}</p> : null}
		 </div>
		);
   };
}

export default App;