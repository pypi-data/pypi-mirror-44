
import * as React from 'react';
import { Typography, Popover, Theme, createStyles, withStyles } from '@material-ui/core';
import { appData } from '../tools';
import moment = require('moment');
import * as semver from 'semver';

const LogBlock = React.memo((props: { title: string, items: Array<string> }) => {
    return <div className="logblock">
        <Typography variant="subtitle2" className="title">{props.title}:</Typography>
        {props.items.map((i, idx) =>
            <Typography key={idx} className="item">- {i}</Typography>
        )}
    </div>
});

const styles = (theme: Theme) => createStyles({
    new: {
        textTransform: 'uppercase',
        padding: '2px 4px',
        marginLeft: 5,
        backgroundColor: theme.palette.text.primary,
        color: theme.palette.background.default,
        borderRadius: theme.shape.borderRadius,
        fontWeight: 'bold',
        fontSize: '0.8em',
    }
});

export type StateProps = {
    lastSeenChangelogVersion: string,
}

export type DispatchProps = {
    setLastSeenVersion: (version: string) => void,
}

class Version extends React.Component<StateProps & DispatchProps & { classes: any }, { anchorEl: HTMLElement }> {
    state = {
        anchorEl: null,
    };

    handleClick = event => {
        this.setState({
            anchorEl: event.currentTarget,
        });
    };

    handleClose = () => {
        this.setState({
            anchorEl: null,
        });
        this.props.setLastSeenVersion(appData.changelog[0].name)
    };

    render() {
        const { lastSeenChangelogVersion, classes } = this.props;
        const { version } = appData;
        const { anchorEl } = this.state;
        const open = Boolean(anchorEl);
        return <React.Fragment>
            <Typography onClick={this.handleClick} variant="subtitle2" color="inherit" className="version">
                v{version}{semver.gt(appData.changelog[0].name, lastSeenChangelogVersion) ? <span className={classes.new}>new!</span> : ''}
            </Typography>
            <Popover
                open={open}
                anchorEl={anchorEl}
                onClose={this.handleClose}
                anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'center',
                }}
                transformOrigin={{
                    vertical: 'top',
                    horizontal: 'center',
                }}
            >
                <div className="changelog-container">
                    {appData.changelog.map(ch => <Typography key={ch.name} component="div" className="logblock-container">
                        <span className="title">{ch.name}</span>
                        <span className="date">({moment.unix(ch.date).format('YYYY-MM-DD HH:mm')})</span>
                        {semver.lt(lastSeenChangelogVersion, ch.name) ? <span className={classes.new}>new!</span> : ''}
                        {ch.fix.length ? <LogBlock title="Fixes" items={ch.fix} /> : null}
                        {ch.enh.length ? <LogBlock title="Enhancements" items={ch.enh} /> : null}
                    </Typography>)}
                </div>
            </Popover>
        </React.Fragment>
    }
}

export default withStyles(styles)(Version);
