import { createStyles, Theme, Typography, withStyles, Avatar, Tooltip, Link } from "@material-ui/core";
import * as React from 'react';
import { DragDropContext, Draggable, Droppable, DroppableStateSnapshot, DropResult } from "react-beautiful-dnd";
import { IssueByStatusMap, IssueStatus, UserMap, TickingStat, Issue, User } from "../types";
import classNames = require("classnames");
import AccountCircle from '@material-ui/icons/AccountCircle';
import StopWatch from "../containers/StopWatch";
import IssueActionIcons from "./IssueActionIcons";
import { removeKeys } from "../tools";
import { IssueUserIcon } from "./tools";

const styles = ({ palette, shape, typography }: Theme) => createStyles({
    card: {
        borderRadius: shape.borderRadius,
        backgroundColor: palette.background.default,
        '&:hover': {
            opacity: 0.8,
        },
        boxShadow: '0px 0px 5px rgba(0,0,0,.3)',
    },
    avatar: {
        color: typography.caption.color,
        width: 24,
        height: 24,
    },
});

export type StateProps = {
    issues: IssueByStatusMap,
}

export type DispatchProps = {
    onDragEnd: (result: DropResult, issues: IssueByStatusMap) => void,
    showIssue: (id: number) => void,
}

export type OwnProps = {
    projectId: number,
    tickingStat: TickingStat,
    onAddNewIssue: (projectId: number) => void,
    onAddNewTime: (projectId: number, issueId: number) => void,
    onDeleteIssue: (projectId: number, issueId: number) => void,
    onUpdateIssue: (projectId: number, issueId: number) => void,
    startTime: (projectId: number, issueId: number) => void,
    stopTime: () => void,
    doneDateFilter: number,
}

type MuiProps = {
    classes: any,
}

type Props = OwnProps & StateProps & DispatchProps & MuiProps;

type CardContentProps = {
    showIssue: (id: number) => void,
    tickingStat: TickingStat,
    onAddNewTime: (projectId: number, issueId: number) => void,
    onDeleteIssue: (projectId: number, issueId: number) => void,
    onUpdateIssue: (projectId: number, issueId: number) => void,
    startTime: (projectId: number, issueId: number) => void,
    stopTime: () => void,
    issue: Issue,
}

const CardContent = withStyles(styles)(React.memo((props: CardContentProps & MuiProps) => {

    const {showIssue, issue} = props;

    return <React.Fragment>
        <div className="header">
            <Typography className="title" variant="subtitle1">
                <Link onClick={() => showIssue(issue.id)}>#{issue.id}</Link> {issue.name}
            </Typography>
            <IssueUserIcon issue={issue}/>
        </div>
        <div className="footer">
            <Typography style={{opacity: 0.6, flexGrow: 1}}>
                <StopWatch projectId={issue.projectId} issueId={issue.id} initialValue={issue.timeStat.spent} />
            </Typography>
            <IssueActionIcons issue={issue} {...removeKeys<CardContentProps>(props, 'classes')} />
        </div>
    </React.Fragment>
}))

export default withStyles(styles)(React.memo((props: Props) => {

    let {issues, onDragEnd, classes} = props;

    const isDifferentStatus = (status: string, {isDraggingOver, draggingOverWith}: DroppableStateSnapshot): boolean => {
        return isDraggingOver && draggingOverWith && !issues[status].filter(i => i.id == parseInt(draggingOverWith)).length;
    }

    return <div className="card-container">
        <DragDropContext onDragEnd={result => onDragEnd(result, issues)}>{Object.values(IssueStatus).map(s =>
            <div className="card-column" key={s}>
                <Typography variant="h6" className="card-column-header">{s}</Typography>
                <Droppable droppableId={s} >{({innerRef, droppableProps, placeholder}, snapshot) => (
                    <div key={s} ref={innerRef} {...droppableProps} className={classNames('droppable', {hovering: isDifferentStatus(s, snapshot)})}>
                        {issues[s].map((i, idx) =>
                        <Draggable draggableId={i.id.toString()} index={idx} key={i.id}>
                            {({innerRef, dragHandleProps, draggableProps}) => (
                                <div className={classes.card + ' card'} ref={innerRef} {...draggableProps} {...dragHandleProps}>
                                    <CardContent issue={i} {...removeKeys<Props>(props, 'classes')} />
                                </div>
                            )}
                        </Draggable>)}
                        {placeholder}
                    </div>
                )}</Droppable>
            </div>
        )}</DragDropContext>
    </div>
}))
