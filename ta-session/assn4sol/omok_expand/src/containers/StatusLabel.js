import { connect } from 'react-redux'
import StatusLabel from '../components/atoms/StatusLabel'

const mapStateToProps = (state) => {
    return {
        turn : state.omok.turn,
        win : state.omok.win,
        login_entered : state.omok.login_entered,
        login_iswaiting : state.omok.login_iswaiting
    }
}
const mapDispatchToProps = (dispatch) => {
    return { }
}

export default connect(mapStateToProps, mapDispatchToProps)(StatusLabel)
