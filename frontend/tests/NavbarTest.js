import test from 'tape'
import React from 'react'
import { shallow, mount } from 'enzyme';
import sinon from 'sinon';

import Navbar from '../src/components/Navbar';

const handleKeyPress = () => true
const onChange = () => true

test('----- React Component Tests: Navbar -----', t => {
  const handleSubmit = sinon.spy();
  const wrapper = shallow(<Navbar handleKeyPress={handleKeyPress}
  								  onChange={onChange}
  								  handleSubmit={handleSubmit}
  						  />)
  t.equal(handleSubmit.callCount, 0, 'submit button props call count should equal "0"')
  wrapper.find('.submit').simulate('click');
  t.equal(handleSubmit.callCount, 1, 'submit button props call count should equal "1"')
  t.end()
})