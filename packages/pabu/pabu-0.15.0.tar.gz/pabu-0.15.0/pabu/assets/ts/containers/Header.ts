
import { connect } from 'react-redux';
import Header, {StateProps, DispatchProps, OwnProps} from '../components/Header';
import { State, ThunkDispatcher } from '../types';
import { stopTime, setDarkTheme } from '../actions';

const mapStateToProps = (state: State) => {
    const {tickingStat, isDarkTheme, projects, issues } = state;

    return {
        tickingStat,
        isDarkTheme,
        projects,
        issues,
    }
}

const mapDispatchToProps = (dispatch: ThunkDispatcher) => {
    return {
        onStopTime: () => {
            dispatch(stopTime())
        },
        onThemeClick: (isDark: boolean) => {
            dispatch(setDarkTheme(isDark))
        },
    }
}

export default connect<StateProps, DispatchProps, OwnProps>(mapStateToProps, mapDispatchToProps)(Header)
