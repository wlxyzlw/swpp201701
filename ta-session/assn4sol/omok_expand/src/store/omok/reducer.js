import initialState from './selectors'

const omok_reducer = (state = initialState, action) => {
    switch(action.type) {
        case 'ENTER_ROOM_SUCCESS':
            console.log("Login success!")
            return {
                ...state,
                login_entered:true,
                login_iswaiting:true,
                login_failed:false,
                rid:action.rid,
                uname:action.uname,
                ubase64:action.ubase64
            }
        case 'ENTER_ROOM_FAIL':
            return { ...state, login_entered:false, login_iswaiting:false, login_failed:true}
        case 'START_GAME':
            return {
                ...state,
                login_entered:true,
                login_iswaiting:false,
                login_failed:false,
                mystone:action.mystone,
                enemyname:action.enemyname
            }
        case 'UPDATE_STATE':
            const roominfo = action.roominfo
            return {
                ...state,
                pane:roominfo.pane,
                turn:roominfo.turn,
                win:roominfo.win
            }
        default:
            return state
    }
}

export default omok_reducer
