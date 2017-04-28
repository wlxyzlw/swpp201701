import { connect } from 'react-redux'
import { RoomInfo } from '../components/atoms/RoomInfo'
import { postEnterRoomRequest } from '../store/omok/actions'

const mapStateToProps = (state) => {
    console.log("mapStateToProps: state=" + state.omok)
    return state.omok
}
const mapDispatchToProps = (dispatch) => {
    return { 
        onEnter : (uname, upwd, rid) => {
            dispatch(postEnterRoomRequest(uname, upwd, rid))
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(RoomInfo)
