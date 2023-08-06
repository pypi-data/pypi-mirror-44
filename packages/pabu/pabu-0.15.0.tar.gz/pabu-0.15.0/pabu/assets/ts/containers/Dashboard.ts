
import { connect } from 'react-redux';
import { closeInviteDialog, closeProjectDialog, fetchProjects, joinToProject, openInviteDialog, openProjectDialog, receiveProjects, sendProject, setDarkTheme, stopTime } from '../actions';
import Dashboard from '../components/Dashboard';
import { State, ThunkDispatcher } from '../types';

const mapStateToProps = (state: State) => {
    const { projectDialogContext, tickingStat, projects, isDarkTheme, inviteDialogIsOpen } = state;
    let projectData = {name: '', desc: ''};
    if (projectDialogContext && projectDialogContext.id) {
        projectData = projects[projectDialogContext.id];
    }
    return {
        projectDialogContext,
        tickingStat,
        projectData,
        isDarkTheme,
        inviteDialogIsOpen,
    }
}

const mapDispatchToProps = (dispatch: ThunkDispatcher) => {
    return {
        onProjectSubmit: (id: number, name: string, desc: string) => {
            dispatch(sendProject(name, desc, id)).then(project => {
                dispatch(closeProjectDialog())
                dispatch(receiveProjects({[project.id]: project}))
            })
        },
        onInviteSubmit: (token: string) => {
            dispatch(joinToProject(token)).then(() => {
                dispatch(closeInviteDialog())
                dispatch(fetchProjects())
            })
        },
        showInviteDialog: () => {
            dispatch(openInviteDialog())
        },
        hideInviteDialog: () => {
            dispatch(closeInviteDialog())
        },
        showDialog: () => {
            dispatch(openProjectDialog())
        },
        hideDialog: () => {
            dispatch(closeProjectDialog())
        },
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Dashboard)
