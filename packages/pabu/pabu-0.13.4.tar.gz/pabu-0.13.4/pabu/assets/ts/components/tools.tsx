import * as React from 'react';
import Grow from '@material-ui/core/Grow';
import { Theme, createStyles, withStyles, Avatar, Typography } from '@material-ui/core';
import { User, Issue, State, UserMap } from '../types';
import AccountCircle from '@material-ui/icons/AccountCircle';
import { connect } from 'react-redux';

export const dialogTransition = p => <Grow {...p} />

const userAvatarStyles = ({ palette, shape, typography }: Theme) => createStyles({
    avatar: {
        color: typography.caption.color,
        width: 24,
        height: 24,
    },
});

const UserAvatarComponent = withStyles(userAvatarStyles)(React.memo((props: {userId: number, users: UserMap, classes: any}) => {
    const {users, userId, classes} = props;
    const user = users[userId];
    return user.avatar ? <Avatar data-tip={user.name} className={classes.avatar} src={user.avatar}/> :
        <AccountCircle className={classes.avatar} data-tip={user.name}/>
}));

export const UserAvatar = connect((state: State) => ({users: state.users}))(UserAvatarComponent);

const UserLabelComponent = React.memo((props: {userId: number, users: UserMap}) => {
    const {users, userId} = props;
    const user = users[userId];
    return <div style={{display: 'flex', alignItems: 'center'}}>
        <UserAvatar userId={userId} />
        <Typography style={{paddingLeft: 5}}>{user.name}</Typography>
    </div>
});

export const UserLabel = connect((state: State) => ({users: state.users}))(UserLabelComponent);

export const IssueUserIcon = React.memo((props: {issue: Issue}) => {
    const {issue} = props;
    return <UserAvatar userId={issue.assigneeId || issue.reporterId} />
});

const badgeStyles = ({ palette, shape, typography }: Theme) => createStyles({
    root: {
        color: typography.caption.color,
        backgroundColor: palette.background.default,
        fontSize: typography.caption.fontSize,
        padding: '5px 7px',
        borderRadius: shape.borderRadius,
        textTransform: 'uppercase',
        userSelect: 'none',
    },
});

export const Badge = withStyles(badgeStyles)(React.memo((props: {text: string, classes: any, style?: React.CSSProperties}) => {
    const {text, classes, style} = props;
    return <span className={classes.root} style={style}>{text}</span>
}));

export const NoDataLabel = React.memo((props: {text: string}) => {
    return <Typography style={{opacity: 0.6, fontStyle: 'italic'}}>{props.text}</Typography>
});
