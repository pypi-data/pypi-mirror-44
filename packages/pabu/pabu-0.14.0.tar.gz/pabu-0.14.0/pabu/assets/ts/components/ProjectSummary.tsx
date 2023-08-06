import * as React from 'react';
import { withStyles, Theme, createStyles, Table, TableHead, TableRow, TableCell, TableBody, TableFooter, Button } from '@material-ui/core';
import { User, Project } from '../types';
import { formatDuration } from '../tools';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

export interface UserPaymentStat {
    spent: number,
    paid: number,
    user: User,
    ticking: boolean,
}

export type OwnProps = {
    id: number,
}

export type StateProps = {
    userStat: Array<UserPaymentStat>,
    project: Project,
}

export type DispatchProps = {
    onUpdateProject: (projectId: number) => void,
    onDeleteProject: (projectId: number) => void,
    onLeaveProject: (projectId: number) => void,
}

const styles = ({ palette }: Theme) => createStyles({
    buttonBar: {
        margin: '10px 0',
    }
});

export default withStyles(styles)(React.memo((props: OwnProps & StateProps & DispatchProps & {classes: any}) => {
    let {id, userStat, onUpdateProject, onDeleteProject, classes, onLeaveProject, project} = props;

    const sum = {spent: 0, paid: 0, ticking: false};
    for (let stat of userStat) {
        sum.spent += stat.spent;
        sum.paid += stat.paid;
        if (stat.ticking)
            sum.ticking = true;
    }

    return <div>
        <Table>
            <TableHead>
                <TableRow>
                    <TableCell>User</TableCell>
                    <TableCell>Spent</TableCell>
                    <TableCell>Paid</TableCell>
                    <TableCell>Balance</TableCell>
                    <TableCell>Working now?</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {userStat.filter(s => s.user).map(stat => <TableRow key={stat.user.id}>
                    <TableCell>{stat.user.name}</TableCell>
                    <TableCell>{formatDuration(stat.spent)}</TableCell>
                    <TableCell>{formatDuration(stat.paid)}</TableCell>
                    <TableCell>{formatDuration(stat.paid - stat.spent)}</TableCell>
                    <TableCell><FontAwesomeIcon icon={stat.ticking ? 'check' : 'times'}/></TableCell>
                </TableRow>)}
            </TableBody>
            <TableFooter>
                <TableRow>
                    <TableCell></TableCell>
                    <TableCell>{formatDuration(sum.spent)}</TableCell>
                    <TableCell>{formatDuration(sum.paid)}</TableCell>
                    <TableCell>{formatDuration(sum.paid - sum.spent)}</TableCell>
                    <TableCell><FontAwesomeIcon icon={sum.ticking ? 'check' : 'times'}/></TableCell>
                </TableRow>
            </TableFooter>
        </Table>
        <div className={classes.buttonBar}>
            <Button size="small" color="primary" disabled={project.users.length == 1}
                    onClick={onLeaveProject.bind(this, id)}>Leave</Button>
            <Button size="small" color="primary" onClick={onUpdateProject.bind(this, id)}>Update</Button>
            <Button size="small" color="secondary" onClick={onDeleteProject.bind(this, id)}>Delete</Button>
        </div>
    </div>
}))
