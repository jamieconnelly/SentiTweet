import test from 'tape'
import 'jsdom-global/register';
import React from 'react'
import { shallow, mount } from 'enzyme';

import App from '../src/containers/App';

const state = { 
	'error': false,
	'errorText': 'hello',
	'loaded': true,
	'neg': 0,
	'neut': 0, 
	'pos': 0,
	'results': true, 
	'term': '', 
	'tweets': [] 
}

test('----- React Component Tests: App -----', t => {
  const wrapper = mount(<App />)
  t.equal(wrapper.children().length, 4, 'App children length should equal "4"')
  wrapper.setState({'error': true})
  t.equal(wrapper.children().length, 5, 'App children length should equal "5"')
  t.equal(wrapper.state().error, true, 'App state "error" should equal "true"')
  t.equal(wrapper.state().errorText, 'hello', 'App state "errorText" should equal "hello"')
  t.equal(wrapper.state().loaded, true, 'App state "loaded" should equal "true"')
  t.equal(wrapper.state().neg, 0, 'App state "neg" should equal "0"')
  wrapper.setState({'neg': 10})
  t.equal(wrapper.state().neg, 10, 'App state "neg" should equal "10"')
  t.end()
})