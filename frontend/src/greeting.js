import React from 'react';

export default class Greeting extends React.Component {
  constructor() {
    super();
  }

  render() {
    return (  
      <div className='greeting'>
        Hi!, {this.props.name}!
      </div>
    );
  }
}