import { connect } from 'react-redux'
import { OmokPane } from '../components/atoms/OmokPane'
import { postPlaceStone } from '../store/omok/actions'

const mapStateToProps = (state) => {
    return state.omok
}
const mapDispatchToProps = (dispatch) => {
    return { 
        postPlaceStone : (i, j, rid, ubase64) => {
            dispatch(postPlaceStone(i, j, rid, ubase64))
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(OmokPane)
