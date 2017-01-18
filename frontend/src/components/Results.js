import React from 'react'

class Results extends React.Component {
  
  render() {
    return (
      <div>
        <p style={{ marginLeft: '10%', marginBottom: 15 }}>
        Neutral: {this.props.neg}%,
        Negative: {this.props.neg}%,
        Positive: {this.props.pos}% 
        </p>
      </div>
    );
  }
}

export default Results;