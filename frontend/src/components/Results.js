import React from 'react'

class Results extends React.Component {
  
  render() {
    return (
      <div>
        No of tweets is: {this.props.tweets.length}
        {this.props.tweets.map(x => <ul><li>{x}</li></ul>)}
      </div>
    );
  }
}

export default Results;