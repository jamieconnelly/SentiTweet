import React from 'react'
import {BootstrapTable, TableHeaderColumn} from 'react-bootstrap-table';

class ResultsTable extends React.Component {

  get_polarity(polarity) {
    if (polarity == 0)
      return 'negative'
    else if (polarity == 2)
      return 'nuetral'
    else
      return 'positive'
  }

  render() {
    const tweets = this.props.tweets
    const results = []
    const style = {'marginTop': '20px'}
    const styleId = {'width': '10%'}
    const styleText = {'width': '80%'}
    const stylePolarity = {'width': '10%'}

    for (let i=0; i<tweets.length; i++) {
      results.push({
        'id': i+1,
        'text': tweets[i].text,
        'polarity': this.get_polarity(tweets[i].polarity)
      })
    }

    return (
      
      <div style={style}>
        <BootstrapTable striped hover data={results}>
          <TableHeaderColumn dataField='id' isKey={ true } >#</TableHeaderColumn>
          <TableHeaderColumn dataField='text' dataSort={ true }>Tweet</TableHeaderColumn>
          <TableHeaderColumn dataField='polarity' dataSort={true}>Polarity</TableHeaderColumn>
        </BootstrapTable>
      </div>
    );
  }
}

export default ResultsTable;
