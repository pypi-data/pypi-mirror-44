
import { connect } from 'react-redux';
import { createProjectToken, deleteProjectToken, fetchProjects, openConfirmDialog } from '../actions';
import ProjectInviteTokenList, { DispatchProps, OwnProps, StateProps } from '../components/ProjectInviteTokenList';
import { ProjectInvitationToken, State, ThunkDispatcher } from '../types';

function mapStateToProps(state: State, props: OwnProps) {
    const {projectInvitationTokens} = state;

    return {
        rows: Object.values(projectInvitationTokens).filter(t => t.projectId == props.id),
    }
}

const mapDispatchToProps = (dispatch: ThunkDispatcher) => {
    return {
        onDelete: (prjToken: ProjectInvitationToken) => {
            dispatch(openConfirmDialog({
                message: 'Do you really want to delete this token?',
                callback: () => dispatch(deleteProjectToken(prjToken.id)).then(() => dispatch(fetchProjects(prjToken.projectId))),
            }))
        },
        onCreateProjectToken: (projectId: number) => {
            dispatch(createProjectToken(projectId))
        }
    }
}

export default connect<StateProps, DispatchProps, OwnProps>(mapStateToProps, mapDispatchToProps)(ProjectInviteTokenList);
