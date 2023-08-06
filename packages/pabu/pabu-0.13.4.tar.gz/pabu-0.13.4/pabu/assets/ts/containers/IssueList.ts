
import { connect } from 'react-redux';
import { deleteIssue, openAddTimeDialog, openIssueDialog, openIssueViewDialog, startTime, stopTime } from '../actions';
import IssueList, { DispatchProps, OwnProps, StateProps } from '../components/IssueList';
import { State, ThunkDispatcher } from '../types';

function mapStateToProps(state: State, props: OwnProps): StateProps {
    let {issues, tickingStat} = state;
    return {
        issues: Object.values(issues).filter(i => i.projectId == props.id),
        tickingStat,
    }
}

const mapDispatchToProps = (dispatch: ThunkDispatcher): DispatchProps => {
    return {
        onAddNewTime: (projectId: number, issueId: number) => dispatch(openAddTimeDialog(projectId, issueId)),
        startTime: (projectId: number, issueId: number) => dispatch(startTime(projectId, issueId)),
        stopTime: () => dispatch(stopTime()),
        onDeleteIssue: (projectId: number, issueId: number) => {
            if(confirm('Do you really want to delete this task?'))
                dispatch(deleteIssue(issueId, projectId));
        },
        onUpdateIssue: (projectId: number, id: number) => dispatch(openIssueDialog(projectId, id)),
        onAddNewIssue: (projectId: number) => dispatch(openIssueDialog(projectId)),
        showIssue: (id: number) => dispatch(openIssueViewDialog(id)),
    }
}

export default connect<StateProps, DispatchProps, OwnProps>(mapStateToProps, mapDispatchToProps)(IssueList);
