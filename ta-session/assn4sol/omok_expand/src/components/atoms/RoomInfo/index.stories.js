import React from 'react'
import { storiesOf } from '@kadira/storybook'
import RoomInfo from '.'

storiesOf('RoomInfo', module)
  .add('default', () => (
    <RoomInfo>Hello</RoomInfo>
  ))
  .add('reverse', () => (
    <RoomInfo reverse>Hello</RoomInfo>
  ))
