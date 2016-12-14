import React from 'react';

export default class Greeting extends React.Component {
  constructor() {
    super();
  }

  render() {
    return (  
      <div className='greeting'>
        H!, {this.props.name}!
      </div>
    );
  }
}