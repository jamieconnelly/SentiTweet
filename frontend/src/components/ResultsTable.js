import React from 'react'
import {Table} from 'react-bootstrap';

class ResultsTable extends React.Component {

  getPolarity(polarity) {
    if (polarity == 0)
      return 'negative'
    else if (polarity == 2)
      return 'nuetral'
    else
      return 'positive'
  }

  getRowColour(polarity) {
    if (polarity == 0)
      return 'rgba(238, 144, 144, 0.35)'
    else if(polarity == 2)
      return 'rgba(144, 219, 238, 0.35)'
    else
      return 'rgba(183, 238, 144, 0.35)'
  }

  constructResults(tweets) {
    let results = []
    for (let i=0; i<tweets.length; i++) {
      results.push({
        'id': i+1,
        'text': tweets[i].text,
        'polarity': this.getPolarity(tweets[i].polarity),
        'colour': this.getRowColour(tweets[i].polarity)
      })
    }
    return results
  }

  getTableHead() {
    return (
      <thead>
        <tr>
          <th style={{'width': '5%'}}>#</th>
          <th style={{'width': '80%'}}>Tweet</th>
          <th style={{'width': '15%'}}>Polarity</th>
        </tr>
      </thead>
    )
  }

  render() {
    const results = this.constructResults(this.props.tweets)

    return (
      <div style={{'marginTop': '20px'}}>
        <Table className="results-table" bordered condensed hover>
          {this.getTableHead()}
          <tbody>
          {results.map(x => (
              <tr style={{'backgroundColor': x.colour}}>
                <td>{x.id}</td>
                <td>{x.text}</td>
                <td>{x.polarity}</td>
              </tr>
            )
          )}
          </tbody>
        </Table>
      </div>
    );
  }
}

export default ResultsTable;
