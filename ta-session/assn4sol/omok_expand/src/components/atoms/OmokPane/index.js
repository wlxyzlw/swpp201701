import React, { PropTypes } from 'react'
import styled from 'styled-components'
import { font, palette } from 'styled-theme'

/*const OmokPane = styled.span`
  font-family: ${font('primary')};
  color: ${palette({ grayscale: 0 }, 1)};
`*/
export const OmokPane = ({ login_entered, pane, turn, win, rid, ubase64, postPlaceStone }) => {
    if (!login_entered) {
        // Empty space
        return <div></div>
    }
    var rows = [];
    for (var i = 0 ; i < 19; i++) {
        for (var j = 0; j < 19; j++) {
            var t = i + j;
            const ii = i;
            const jj = j;
            const onClick = () => {
                postPlaceStone(ii, jj, rid, ubase64);
            };
            const onClickAlert = () => {
                alert("The game has ended!")
            };
            rows.push(<div style={{display:"inline-block", 
                    width:30,
                    height:30,
                    textAlign:"center",
                    backgroundColor:((t % 2 == 0 ) ? "lightgray" : "white")}} 
                onClick={win == 0 ? onClick : onClickAlert}
                id={i + "_" + j}>
            {pane[i][j] == '0' ? '-' : (pane[i][j] == '1' ? 'O' : 'X')}
            </div>);
        }
        rows.push(<br />);
    }
    return (<div>{rows}</div>);
}

/*OmokPane.propTypes = {
  pane:
  palette: PropTypes.string,
  reverse: PropTypes.bool,
}*/

/*OmokPane.defaultProps = {
  palette: 'grayscale',
}*/

export default OmokPane
