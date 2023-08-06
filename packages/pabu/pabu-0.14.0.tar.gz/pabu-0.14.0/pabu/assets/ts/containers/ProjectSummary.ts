
import { connect } from 'react-redux';
import { deleteProject, openProjectDialog, leaveProject, fetchProjects } from '../actions';
import ProjectSummary, { DispatchProps, OwnProps, StateProps, UserPaymentStat } from '../components/ProjectSummary';
import { State, ThunkDispatcher } from '../types';

function mapStateToProps(state: State, props: OwnProps): StateProps {
    const projectId = props.id;

    const project = state.projects[projectId];
    const payments = Object.values(state.payments).filter(r => r.projectId == projectId);
    const timeEntries = Object.values(state.timeEntries).filter(r => r.projectId == projectId);

    let userPaymentStat: {[n: number]: UserPaymentStat} = {};

    for (let userId of project.users) {
        userPaymentStat[userId] = {spent: 0, paid: 0, user: state.users[userId], ticking: false};
    }

    for (const payment of payments) {
        userPaymentStat[payment.paidUserId].paid += payment.amount;
    }

    for (const entry of timeEntries) {
        if (!(entry.userId in userPaymentStat))
            continue

        const len = (entry.end || (new Date().getTime()/1000)) - entry.start;
        userPaymentStat[entry.userId].spent += len;
        if (entry.end == null)
            userPaymentStat[entry.userId].ticking = true;
    }

    return {
        userStat: Object.values(userPaymentStat),
        project,
    }
}

const mapDispatchToProps = (dispatch: ThunkDispatcher) => {
    return {
        onDeleteProject: (projectId: number) => {
            if (confirm('Do you really want to delete this project?'))
                dispatch(deleteProject(projectId));
        },
        onUpdateProject: (projectId: number) => {
            dispatch(openProjectDialog(projectId))
        },
        onLeaveProject: (projectId: number) => {
            if (confirm('Do you really want to leave this project?'))
                dispatch(leaveProject(projectId))
        },
    }
}

export default connect<StateProps, DispatchProps, OwnProps>(mapStateToProps, mapDispatchToProps)(ProjectSummary);
