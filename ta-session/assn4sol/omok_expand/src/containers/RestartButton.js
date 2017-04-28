import { connect } from 'react-redux'
import { RestartButton } from '../components/atoms/RestartButton'
import { restart } from '../store/omok/actions'

const mapStateToProps = (state) => {
    return {
    }
}
const mapDispatchToProps = (dispatch) => {
    return {
        onClick : () => {
            dispatch(restart())
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(RestartButton)
