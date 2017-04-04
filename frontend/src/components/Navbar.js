import React from 'react'
import { Navbar, FormGroup, FormControl, Button } from 'react-bootstrap';

class NavbarInstance extends React.Component {

  render() {
    return (
      <Navbar>
        <Navbar.Header>
          <Navbar.Brand>SentiVis</Navbar.Brand>
          <Navbar.Toggle />
        </Navbar.Header>
        <Navbar.Collapse>
          <Navbar.Form pullLeft>
            <FormControl onChange={this.props.onChange}
                         onKeyPress={this.props.handleKeyPress}
                         type="text"
                         placeholder="Enter search term..." />
            <Button className='submit' onClick={this.props.handleSubmit} type="submit">Submit</Button>
          </Navbar.Form>
        </Navbar.Collapse>
      </Navbar>
    );
  }
}

export default NavbarInstance;