import { Button, Dialog, DialogActions, DialogContent, DialogTitle, Divider, IconButton, Typography } from '@material-ui/core';
import CloseIcon from '@material-ui/icons/Close';
import * as React from 'react';
import { Issue, TickingStat, Project } from '../types';
import { dialogTransition, UserLabel, Badge, NoDataLabel } from './tools';
import StopWatch from '../containers/StopWatch';
import moment = require('moment');
import Tooltip from './Tooltip';

export type StateProps = {
    issue: Issue,
    show: boolean,  // needed for nice hide effect
    tickingStat: TickingStat,
    project: Project,
}

export type DispatchProps = {
    onClose: () => void,
    onAddNewTime: (projectId: number, issueId: number) => void,
    onDeleteIssue: (projectId: number, issueId: number) => void,
    onUpdateIssue: (projectId: number, issueId: number) => void,
    startTime: (projectId: number, issueId: number) => void,
    stopTime: () => void,
}

export default React.memo((props: StateProps & DispatchProps) => {
    const {issue, onClose, show, tickingStat, startTime, stopTime, onDeleteIssue, onAddNewTime, onUpdateIssue, project} = props;
    if (!issue) return <div></div>;

    function getTickingIcon() {
        if (tickingStat.ticking) {
            if (tickingStat.entry.issueId == issue.id)
                return <Button variant="contained" color="secondary" onClick={stopTime}>Stop time</Button>
            else
                return <Button variant="contained" color="primary" disabled>Start time</Button>
        } else
            return <Button variant="contained" color="primary" onClick={startTime.bind(this, issue.projectId, issue.id)}>Start time</Button>
    }

    return  <Dialog
                TransitionComponent={dialogTransition}
                onClose={onClose}
                open={show}
                className="issue-view-dialog"
                PaperProps={{style: {minWidth: 400}}
            }>
                <DialogTitle className="title" disableTypography>
                    <Typography variant="h6" style={{flexGrow: 1}}>#{issue.id} {issue.name}</Typography>
                    <IconButton aria-label="Close" onClick={onClose}>
                        <CloseIcon />
                    </IconButton>
                </DialogTitle>
                <Divider/>
                <div className="controls">
                    <Button variant="contained" color="primary" onClick={()=>onAddNewTime(issue.projectId, issue.id)}>Add time</Button>
                    {getTickingIcon()}
                    <Button variant="contained" color="primary" onClick={()=>onUpdateIssue(issue.projectId, issue.id)}>Update</Button>
                </div>
                <Divider/>
                <table className="details">
                    <tbody>
                        <tr><td><Typography>Project</Typography></td><td><Typography>{project.name}</Typography></td></tr>
                        <tr><td><Typography>Reporter</Typography></td><td><UserLabel userId={issue.reporterId}/></td></tr>
                        <tr><td><Typography>Assignee</Typography></td><td>{
                            issue.assigneeId ? <UserLabel userId={issue.assigneeId}/> : <NoDataLabel text="unassigned" />
                        }</td></tr>
                        <tr>
                            <td><Typography>Time spent</Typography></td>
                            <td>
                                <Typography>
                                    <StopWatch projectId={issue.projectId} issueId={issue.id} initialValue={issue.timeStat.spent} />
                                </Typography>
                            </td>
                        </tr>
                        <tr>
                            <td><Typography>Status</Typography></td>
                            <td>
                                <div style={{display: 'flex', alignItems: 'center'}}>
                                    <Badge text={issue.status} style={{marginRight: 5}}></Badge>
                                    <Tooltip placement="top" title={moment.unix(issue.statusDate).format('YYYY-MM-DD HH:mm:ss')}>
                                        <Typography component="span">
                                            ({moment.duration(issue.statusDate*1000 - new Date().getTime()).humanize(true)})
                                        </Typography>
                                    </Tooltip>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td style={{verticalAlign: 'top'}}><Typography>Description</Typography></td>
                            <td>{issue.desc ? <Typography>{issue.desc}</Typography> : <NoDataLabel text="There is no description" />}</td>
                        </tr>
                    </tbody>
                </table>
                <Divider/>
                <DialogActions>
                    <Button variant="contained" color="secondary" onClick={()=>onDeleteIssue(issue.projectId, issue.id)}>Delete</Button>
                </DialogActions>
            </Dialog>
});
