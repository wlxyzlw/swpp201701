// Room enter
export const postEnterRoomRequest = (uname, upwd, rid) => {
    return {
        type: 'POST_ENTER_ROOM_REQUEST',
        uname, // user name
        upwd, // password
        rid // room id
    }
}
export const enterRoomSuccess = (rid, uname, ubase64) => {
    return {
        type: 'ENTER_ROOM_SUCCESS',
        rid, // room id
        uname, // my user name
        ubase64 // base64 value of "uname:passwd"
    }
}
export const enterRoomFail = () => {
    return { type: 'ENTER_ROOM_FAIL' }
}
// Accept enemy's request
export const getAcceptEnemyRequest = (rid, uname) => {
    return {
        type: 'GET_ACCEPT_ENEMY_REQUEST',
        rid, // room id
        uname // my user name
    }
}
// Start game
export const startGame = (enemyname, mystone) => {
    return {
        type: 'START_GAME',
        enemyname,
        mystone
    }
}

// Get state from backend & update redux's state
export const getStateRequest = (rid) => {
    return {
        type: 'GET_STATE_REQUEST',
        rid
    }
}
export const updateState = (roominfo) => {
    return {
        type: 'UPDATE_STATE',
        roominfo
    }
}

// place stone
export const postPlaceStone = (y, x, rid, ubase64) => {
    return {
        type: 'POST_PLACE_STONE',
        y,
        x,
        rid,
        ubase64
    }
}


