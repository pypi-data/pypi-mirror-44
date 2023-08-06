
import { connect } from 'react-redux';
import { closeAddTimeDialog, closeIssueDialog, closePaymentDialog, closeProject, fetchProjects, openProject, receiveIssues, sendPayment, sendTime, processIssues, fetchAllProjectDataIfNeeded } from '../actions';
import ProjectList, {StateProps, DispatchProps} from '../components/ProjectList';
import { PaymentSubmitData, Project, State, ThunkDispatcher, IssueStatus, Issue } from '../types';

function mapStateToProps(state: State) {
    const { issueDialogContext, openedProjectId, addTimeDialogContext, paymentDialogProjectId, users, issues, projects } = state;
    let issueData = {name: '', desc: '', status: IssueStatus.TODO};
    if (issueDialogContext && issueDialogContext.id) {
        issueData = issues[issueDialogContext.id];
    }

    return {
        issueDialogContext,
        addTimeDialogContext,
        openedProjectId,
        paymentDialogProjectId,
        projects: Object.values(projects).sort((a: Project, b: Project) => b.timeStat.lastEntry - a.timeStat.lastEntry),
        users,
        issueData: issueData as Issue,
    }
}

const mapDispatchToProps = (dispatch: ThunkDispatcher) => {
    return {
        onIssueSubmit: (name: string, desc: string, status: IssueStatus, projectId: number, id: number) => {
            dispatch(processIssues([{name, desc, status, projectId, id}])).then(issues => {
                dispatch(closeIssueDialog())
                dispatch(fetchProjects(projectId))
                dispatch(receiveIssues(issues))
            })
        },
        onPaymentSubmit: (projectId: number, data: PaymentSubmitData) => {
            dispatch(sendPayment(projectId, data));
        },
        hideAddIssueDialog: () => {
            dispatch(closeIssueDialog())
        },
        hidePaymentDialog: () => {
            dispatch(closePaymentDialog())
        },
        hideAddTimeDialog: () => {
            dispatch(closeAddTimeDialog())
        },
        onTimeSubmit: (amount: string, time: string, projectId: number, issueId: number = null) => {
            dispatch(sendTime(projectId, time, amount, issueId));
        },
        openProject: (projectId: number) => {
            dispatch(openProject(projectId))
        },
        closeProject: () => {
            dispatch(closeProject());
        },
        onHoverTitle: (projectId: number) => {
            dispatch(fetchAllProjectDataIfNeeded(projectId));
        }
    }
}

export default connect<StateProps, DispatchProps>(mapStateToProps, mapDispatchToProps)(ProjectList);
