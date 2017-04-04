import React from 'react'
import {Modal, Button} from 'react-bootstrap';

class ErrorModal extends React.Component {

  render() {
    return (
      <div className="static-modal">
        <Modal.Dialog style={{margin: '2% auto'}}>
          <Modal.Header>
            <Modal.Title>An error has occurred...</Modal.Title>
          </Modal.Header>
          <Modal.Body className='error-message'>
            {`${this.props.error.name}: ${this.props.error.message}`}
          </Modal.Body>
          <Modal.Footer>
            <Button onClick={this.props.handleClose}>Close</Button>
          </Modal.Footer>
        </Modal.Dialog>
      </div>
    )
  }
}

export default ErrorModal;