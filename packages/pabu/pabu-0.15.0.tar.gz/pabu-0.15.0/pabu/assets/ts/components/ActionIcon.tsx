import * as React from 'react';
import { withStyles, IconButton, Theme, createStyles } from '@material-ui/core';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { IconProp } from '@fortawesome/fontawesome-svg-core';
import { filterDataProps } from '../tools';

type ActionIconProps = {
    icon: IconProp,
    classes: any,
    onClick?: () => void,
    disabled?: boolean,
    className?: string,
}

const styles = ({ palette }: Theme) => createStyles({
    iconButton: {
        width: 35,
        height: 35,
        padding: 5,
    },
    icon: {
        fontSize: 17,
    },
});

export default withStyles(styles)(React.memo((props: ActionIconProps) => {
    const {icon, classes, onClick, disabled} = props;
    return (
        <IconButton {...filterDataProps(props)} className={classes.iconButton} onClick={onClick} disabled={disabled}>
            <FontAwesomeIcon icon={icon} className={classes.icon + (props.className ? (' ' + props.className) : '')} />
        </IconButton>
    )
}));
