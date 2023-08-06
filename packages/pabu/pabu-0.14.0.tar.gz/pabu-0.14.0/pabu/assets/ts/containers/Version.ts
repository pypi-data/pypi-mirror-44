
import { connect } from 'react-redux';
import Version, { StateProps, DispatchProps } from '../components/Version';
import { State, ThunkDispatcher } from '../types';
import { setLastSeenChangelogVersion } from '../actions';

function mapStateToProps(state: State): StateProps {
    const {lastSeenChangelogVersion} = state;

    return {
        lastSeenChangelogVersion
    }
}

const mapDispatchToProps = (dispatch: ThunkDispatcher): DispatchProps => {
    return {
        setLastSeenVersion: version => dispatch(setLastSeenChangelogVersion(version)),
    }
}

export default connect<StateProps, DispatchProps>(mapStateToProps, mapDispatchToProps)(Version);
