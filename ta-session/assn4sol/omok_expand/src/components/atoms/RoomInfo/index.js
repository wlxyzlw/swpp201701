import React, { PropTypes } from 'react'
import styled from 'styled-components'
import { font, palette } from 'styled-theme'

export const RoomInfo = ({ enemyname, mystone, uname,
        rid, login_iswaiting, login_entered, login_failed, onEnter }) => {
    let newuname, newpwd, newrid;
    const onSubmit = () => {
        if (newuname != undefined && newpwd != undefined && newrid != undefined) {
            onEnter(newuname.value, newpwd.value, newrid.value);
        }
    }
    const mystonelbl = mystone == 0 ? "":
                (mystone == 1 ? "O" :
                    (mystone == 2 ? "X" :
                    ""/*unreachable*/))
    var block = (<button onClick={onSubmit} disabled={login_entered}>CONNECT</button>)
    var block2 = 
        login_failed? (<span>Login failed!</span>):
            (login_iswaiting ?
                (<span>Waiting enemy..</span>):
                (login_entered ? 
                    // Game started.
                    (<span>Game started! You are {mystonelbl}</span>):
                    (<span>Please login.</span>)))

    const spanstyle = {
        // Make <span> 300-pixel width
        display:'inline-block',
        width:'200px'
    }
    return (
    <div>
        <div>
            <span style={spanstyle}>
                Login:
                {login_entered?
                    (<span id="username_field">{uname}</span>):
                    (<input id="username_field" size="10" ref={n => {newuname = n; }} />)
                }
            </span>
            <span style={spanstyle}>
                PW:
                {login_entered?
                    "****":
                    (<input id="password_field" size="10" type="password" ref={n => {newpwd = n; }} />)
                }
            </span>
            <span style={spanstyle}>
                Room Number:
                {login_entered?
                    (<span id="room_field">{rid}</span>):
                    (<input id="room_field" size="5" ref={n => {newrid = n;}} />)
                }
            </span>
        </div>
        <div>
            <span style={spanstyle}>
                Enemy:
                <span id="enemy_field">
                    {enemyname}
                </span>
            </span>
            <span style={spanstyle}>
                {block2}
            </span>
            <span style={spanstyle}>
                {block}
            </span>
        </div>
    </div>
    );
}


RoomInfo.propTypes = {
  enemyname : PropTypes.string.isRequired,
  login_iswaiting : PropTypes.bool.isRequired,
  login_failed : PropTypes.bool.isRequired,
  onEnter : PropTypes.func.isRequired
}

export default RoomInfo
