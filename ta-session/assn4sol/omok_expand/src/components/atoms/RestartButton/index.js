import React, { PropTypes } from 'react'
import styled from 'styled-components'
import { font, palette } from 'styled-theme'

export const RestartButton = ({ onClick }) => (
    <button id='restart' onClick={onClick}>RESTART</button>
)

RestartButton.propTypes = {
    onClick : PropTypes.func.isRequired
}

export default RestartButton
