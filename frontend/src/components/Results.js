import React from 'react'

class Results extends React.Component {
  
  render() {
    return (
      <div>
        <p className="muted" style={{ marginBottom: 10 }}> 
        No of tweets is: {this.props.tweets.length} 
        Neg: {this.props.neg}%
        Pos: {this.props.pos}% 
        </p>
      </div>
    );
  }
}

export default Results;