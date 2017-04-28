import React from 'react'
import { storiesOf } from '@kadira/storybook'
import RestartButton from '.'

storiesOf('RestartButton', module)
  .add('default', () => (
    <RestartButton>Hello</RestartButton>
  ))
  .add('reverse', () => (
    <RestartButton reverse>Hello</RestartButton>
  ))
