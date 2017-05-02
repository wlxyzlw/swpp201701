import React, { PropTypes } from 'react'
import styled from 'styled-components'
import { font, palette } from 'styled-theme'

const StatusLabel = ({login_entered, login_iswaiting, turn, win}) => (
    <h4>
        <div id='status_label' style={{border:'solid'}}>
            { !login_entered ? "":
                (login_iswaiting ? "WAITING" : 
                    (win == 0 ? (turn == '1' ? 'Next O' : 'Next X') : 
                        (win == 1 ? 'O win' : 'X win'))) }
        </div>
    </h4>
)

StatusLabel.propTypes = {
  login_entered: PropTypes.bool,
  login_iswaiting: PropTypes.bool,
  turn: PropTypes.number,
  win: PropTypes.number
}

export default StatusLabel
