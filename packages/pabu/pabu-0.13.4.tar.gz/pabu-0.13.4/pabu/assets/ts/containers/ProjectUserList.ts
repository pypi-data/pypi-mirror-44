
import { connect } from 'react-redux';
import { fetchProjects, kickUserFromProject } from '../actions';
import PabuTable, { TableColDesriptor } from '../components/PabuTable';
import { State, ThunkDispatcher, User } from '../types';

type Props = {
    id: number,
}

function mapStateToProps(state: State, props: Props) {
    const {users, projects} = state;

    const project = projects[props.id];

    const colDescriptors = [
        new TableColDesriptor('name', 'Name'),
    ]

    return {
        rows: Object.values(users).filter(u => project.users.indexOf(u.id) != -1),
        colDescriptors,
        context: project.id,
    }
}

const mapDispatchToProps = (dispatch: ThunkDispatcher) => {
    return {
        onDelete: (user: User, context: any) => {
            if (confirm('Do you really want to kick this user from this project?')) {
                dispatch(kickUserFromProject(context, user.id));
                dispatch(fetchProjects(context))
            }
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(PabuTable);
