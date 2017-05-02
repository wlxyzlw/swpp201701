import React from 'react'
import { storiesOf } from '@kadira/storybook'
import OmokPane from '.'

storiesOf('OmokPane', module)
  .add('default', () => (
    <OmokPane>Hello</OmokPane>
  ))
  .add('reverse', () => (
    <OmokPane reverse>Hello</OmokPane>
  ))
