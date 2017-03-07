import React from 'react'

class Results extends React.Component {

  render() {
    const style = { marginLeft: '10%', marginBottom: 15 }
    return (
      <div>
        {!this.props.results ?
          <p style={style}>No results found with that search term... &#9757;</p>
          :
          <p style={style}>
            Tweets collected: {this.props.tweets.length},
            Neutral: {this.props.neut}%,
            Negative: {this.props.neg}%,
            Positive: {this.props.pos}% 
          </p>
        }
      </div>
    );
  }
}

export default Results;