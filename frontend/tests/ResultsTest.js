import test from 'tape'
import React from 'react'
import { shallow, mount } from 'enzyme';

import Results from '../src/components/Results';

const results = true
const tweets = ['tweet 1', 'tweet 2']
const neut = 15
const neg = 50
const pos = 35

test('----- React Component Tests: Results -----', t => {
  const wrapper = shallow(<Results results={results}
  						   		   tweets={tweets} 
  						   		   neut={neut}
  						   		   neg={neg}
  						   		   pos={pos}
  						  />)
  const resultsArray = wrapper.props().children.props.children
  t.equal(resultsArray[1], 2, '<p> should display correct number of tweets "2"')
  t.equal(resultsArray[3], 15, '<p> should display correct number of neutral tweets "15"')
  t.equal(resultsArray[5], 50, '<p> should display correct number of negative tweets "50"')
  t.equal(resultsArray[7], 35, '<p> should display correct number of positive tweets "35"')
  t.end()
})