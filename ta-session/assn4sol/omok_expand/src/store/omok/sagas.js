import {spawn, take, put, call, fork} from 'redux-saga/effects'
import {delay} from 'redux-saga'
import api from 'services/api'
import {enterRoomSuccess, enterRoomFail, getAcceptEnemyRequest,
    startGame, getStateRequest, updateState, postPlaceStone } from './actions'

const user_url = (uid) => {
    return "http://35.161.17.183:8000/users/" + uid + "/";
}
const players_url = (rid) => {
    return "http://35.161.17.183:8000/rooms/" + rid + "/players/";
}
const history_url = (rid) => {
    return "http://35.161.17.183:8000/rooms/" + rid + "/history/";
}
const room_url = (rid) => {
    return "http://35.161.17.183:8000/rooms/" + rid + "/";
}


/*
 * Functions that watch
 * 1. 'POST_ENTER_ROOM_REQUEST' action.
 * - Function "watchLogin" observes it.
 *    * This function calls "postEnterRoom", which
 *      tries to do login by sending data to backend.
 *      If it succeeds, it creates a new action 'ENTER_ROOM_SUCCESS'.
 *     Otherwise, it creates 'ENTER_ROOM_FAIL'.
 * 
 * 2. 'ENTER_ROOM_SUCCESS' action.
 * - Function "createEnemyWait" observes it.
 *    * This function creates action 'GET_ACCEPT_ENEMY_REQUEST'.
 *
 * 3. 'GET_ACCEPT_ENEMY_REQUEST' action.
 * - Function "waitEnemy" observes it.
 *     * This function calls another function 'acceptEnemy'.
 *     * 'acceptEnemy' checks whether a new user is entered to the room.
 *     * If a new user is entered, actions 'START_GAME' and
 *       'GET_STATE_REQUEST' are fired.
 *     * Otherwise, it sleeps for 300 msec, then creates
 *       'GET_ACCEPT_ENEMY_REQUEST' again.
 */

export function* postEnterRoom(data) {
    let uname = data.uname
    let upwd = data.upwd
    let rid = data.rid // Room id
    console.log("Logging in..");
    // Django REST uses HTTP Basic Auth mechanism by default.
    const hash = new Buffer(`${uname}:${upwd}`).toString('base64')
    // Join to the room
    const response = yield call(fetch, players_url(rid), {
        method: 'POST',
        headers: {
            'Authorization': `Basic ${hash}`
        }
    })
    console.log(response)
    if (!response.ok) {
        // Calls ENTER_ROOM_FAIL action.
        yield put(enterRoomFail());
    } else {
        // Calls ENTER_ROOM_SUCCESS action.
        yield put(enterRoomSuccess(rid, uname, hash));
    }
}

export function* createNewAction(data) {
    const rid = data.rid
    const uname = data.uname
    yield delay(300)
    yield put(getAcceptEnemyRequest(rid, uname))
}
export function* acceptEnemy(data) {
    let rid = data.rid // Room id
    let uname = data.uname

    console.log("Getting current player list..");
    const res = yield call(api.get, players_url(rid))
    
    // Check whether room is now full..!
    
    let usernames = []
    for (var i = 0; i < res.length; i++) {
        const ires = yield call(api.get, user_url(res[i]))
        usernames.push(ires["username"])
    }
    console.log(usernames)

    if (usernames.length == 2) {
        // Room is full!
        let enemyname = ""
        let mystone = 0
        if (usernames[0] == uname) {
            // I am first!
            enemyname = usernames[1]
            mystone = 1
        } else {
            enemyname = usernames[0]
            mystone = 2
        }
        // Now start game!
        yield put(startGame(enemyname, mystone));
        // Now start periodic fetch from backend.
        yield put(getStateRequest(data.rid))
    } else {
        // Get enemy info again after 0.3 second (300 msecs)
        yield spawn(createNewAction, {rid, uname})
    }
}

export function* watchLogin() {
    // After clicking "Connect" button
    // To deal with login failure, use infinite loop. :p
    while (true) {
        const data = yield take('POST_ENTER_ROOM_REQUEST')
        yield call(postEnterRoom, data)
    }
}
export function* createEnemyWait() {
    const data = yield take('ENTER_ROOM_SUCCESS')
    // Now at this point I successfully logged in
    // Create 'GET_ACCEPT_ENEMY_REQUEST'
    yield put(getAcceptEnemyRequest(data.rid, data.uname))
}
export function* waitEnemy() {
    while (true) {
        console.log("Waiting GET_ACCEPT_ENEMY_REQUEST..")
        const data = yield take('GET_ACCEPT_ENEMY_REQUEST')
        yield call(acceptEnemy, data)
        // acceptEnemy() will create 'GET_ACCEPT_ENEMY_REQUEST' again.
    }
}

/*
 * Functions that watch
 * 4. 'GET_STATE_REQUEST' action.
 * - Function 'updateStatePeriodically' is responsible for it.
 * - 'updateStatePeriodically' calls 'getState', which fetches data
 *      from backend, and creates a new action 'UPDATE_STATE'
 *    * 'UPDATE_STATE' goes to redux's reducer, which updates React components.
 * - It creates another 'GET_STATE_REQUEST' action after 300 msec.
 *    * This makes periodic update of React components.
 */

export function* updateStatePeriodically() {
    while (true) {
        const data = yield take('GET_STATE_REQUEST')
        yield call(getState, data)
    }
}

export function* createNewStateUpdate(data) {
    const res = data.res
    const rid = data.rid
    yield delay(300)
    yield put(updateState(res))
    yield put(getStateRequest(rid))
}
export function* getState(data) {
    let rid = data.rid // Room id

    const res = yield call(api.get, room_url(rid))
    
    yield spawn(createNewStateUpdate, {res, rid})
}

/*
 * Functions that watch
 * 5. 'POST_PLACE_STONE' action.
 * - Function 'watchPostPlaceStone' is responsible for it.
 */
export function* watchPostPlaceStone() {
    while(true) {
        const data = yield take('POST_PLACE_STONE')
        let hash = data.ubase64
        let rid = data.rid // Room id
        let y = data.y
        let x = data.x
        console.log("POST_PLACE_STONE : x : " + x + " , y : " + y
            + " , roomid : " + rid + " , hash : " + hash)
        // Post it
        const response = yield call(fetch, history_url(rid), {
            method: 'POST',
            headers: {
                'Content-Type':'application/json',
                'Authorization': `Basic ${hash}`
            },
            body: JSON.stringify(
                {
                    'place_j': `${x}`,
                    'place_i': `${y}`
                }
            )
        })
        console.log(response)
    }
}



export default function* () {
    yield fork(watchLogin)
    yield fork(createEnemyWait)
    yield fork(waitEnemy)

    yield fork(updateStatePeriodically)

    yield fork(watchPostPlaceStone)
}
