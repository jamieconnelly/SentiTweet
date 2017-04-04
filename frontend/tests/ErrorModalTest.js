import test from 'tape'
import React from 'react'
import { shallow, mount } from 'enzyme';

import ErrorModal from '../src/components/ErrorModal';

const cb = () => false
const error = { error: true, errorText: 'error' }

test('----- React Component Tests: ErrorModal -----', t => {
  const wrapper = shallow(<ErrorModal handleClose={cb} error={error} />)
  t.equal(wrapper.unrendered.props.error.errorText, 'error', 'errorText props of component should equal "error"')
  t.equal(wrapper.unrendered.props.error.error, true, 'error props of component should equal "true"')
  t.end()
})