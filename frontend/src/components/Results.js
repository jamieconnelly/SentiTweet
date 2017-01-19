import React from 'react'

class Results extends React.Component {
  
  render() {
    return (
      <div>
        {this.props.tweets.length ? 
          this.props.tweets.map(x => <ul><li>{x.location},</li></ul>)
        : null}
        <p style={{ marginLeft: '10%', marginBottom: 15 }}>
        Neutral: {this.props.neut}%,
        Negative: {this.props.neg}%,
        Positive: {this.props.pos}% 
        </p>
      </div>
    );
  }
}

export default Results;