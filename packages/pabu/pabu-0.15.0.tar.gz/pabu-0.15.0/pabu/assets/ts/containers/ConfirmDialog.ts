
import { connect } from 'react-redux';
import { State, ThunkDispatcher } from '../types';
import ConfirmDialog, {StateProps, DispatchProps} from '../components/ConfirmDialog';
import { closeConfirmDialog } from '../actions';

const mapStateToProps = (state: State): StateProps => {
    const { confirmDialogContex } = state;
    return {
        confirmDialogContex
    }
}

const mapDispatchToProps = (dispatch: ThunkDispatcher): DispatchProps => {
    return {
        closeDialog: (callback: () => any) => {
            if (callback)
                callback()
            dispatch(closeConfirmDialog())
        }
    }
}

export default connect<StateProps, DispatchProps>(mapStateToProps, mapDispatchToProps)(ConfirmDialog)
