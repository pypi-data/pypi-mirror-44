
import { connect } from 'react-redux';
import { createProjectToken, deleteProjectToken, fetchProjects } from '../actions';
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
            const projectId = prjToken.projectId;
            if (confirm('Do you really want to delete this token?'))
                dispatch(deleteProjectToken(prjToken.id)).then(() => {
                    dispatch(fetchProjects(projectId))
                })
        },
        onCreateProjectToken: (projectId: number) => {
            dispatch(createProjectToken(projectId))
        }
    }
}

export default connect<StateProps, DispatchProps, OwnProps>(mapStateToProps, mapDispatchToProps)(ProjectInviteTokenList);
