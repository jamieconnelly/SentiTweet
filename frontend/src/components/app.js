import React from 'react'
import styles from './style.css';

class App extends React.Component {

	constructor() {
    	super();
        this.state = {
        	term: '',
        	resp: false,
        	results: [],
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
      	.then((res) => 
          this.setState({ resp: true,
                          results: res.results,
                        }))
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
	  		{this.state.resp ? 
          <div>
            No of tweets is: {this.state.results.length}
            {this.state.results.map(x => <ul><li>{x[0]}, {x[1] === 0 ? 'neg' : 'pos'}</li></ul>)}
          </div>
        : null}
		 </div>
		);
   };
}

export default App;