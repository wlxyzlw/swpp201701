import React from 'react'
import OmokPane from '../../../containers/OmokPane'
import StatusLabel from '../../../containers/StatusLabel'
import RoomInfo from '../../../containers/RoomInfo'

import { PageTemplate } from 'components'

const HomePage = () => {
  return (
    <div>
        Login with "user1 / user1password", "user2 / user2password"
        and room number 1 ~ 20 <br/> <br/>
        <RoomInfo />
        <OmokPane />
        <StatusLabel />
    </div>
  )
}

export default HomePage
