
import { State,  ThunkDispatcher } from '../types';
import { connect } from 'react-redux';
import IssueViewDialog, {StateProps, DispatchProps} from '../components/IssueViewDialog';
import { closeIssueViewDialog, openAddTimeDialog, startTime, stopTime, deleteIssue, openIssueDialog } from '../actions';

function mapStateToProps(state: State): StateProps {
    let {issues, issueViewDialogContext, tickingStat, projects} = state;
    return {
        issue: issueViewDialogContext.id ? issues[issueViewDialogContext.id] : null,
        show: issueViewDialogContext.show,
        tickingStat,
        project: issueViewDialogContext.id ? projects[issues[issueViewDialogContext.id].projectId] : null
    }
}

const mapDispatchToProps = (dispatch: ThunkDispatcher): DispatchProps => {
    return {
        onClose: () => dispatch(closeIssueViewDialog()),
        // TODO: this is copypaste from IssueList.ts ...
        onAddNewTime: (projectId: number, issueId: number) => dispatch(openAddTimeDialog(projectId, issueId)),
        startTime: (projectId: number, issueId: number) => dispatch(startTime(projectId, issueId)),
        stopTime: () => dispatch(stopTime()),
        onDeleteIssue: (projectId: number, issueId: number) => {
            if(confirm('Do you really want to delete this task?'))
                dispatch(deleteIssue(issueId, projectId));
        },
        onUpdateIssue: (projectId: number, id: number) => dispatch(openIssueDialog(projectId, id)),
    }
}

export default connect<StateProps, DispatchProps>(mapStateToProps, mapDispatchToProps)(IssueViewDialog);
