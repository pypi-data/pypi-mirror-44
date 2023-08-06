import { createStyles, Theme, withStyles } from "@material-ui/core";
import * as React from 'react';
import { connect } from 'react-redux';
import { formatDuration, formatStopwatchDuration } from '../tools';
import { State, TickingStat } from '../types';


const styles = ({ palette, typography }: Theme) => createStyles({

});

type Props = {
    classes: any,
    tickingStat: TickingStat,
    initialValue: number,
    projectId: number,
    issueId?: number,
}

type StopWatchState = {
    value: number,
    timerId: NodeJS.Timeout,
    started: number,
}

class StopWatch extends React.Component<Props, StopWatchState> {

    constructor(props: Props) {
        super(props);
        this.state = {
            value: this.props.initialValue,
            timerId: null,
            started: 0,
        }
    }

    componentWillReceiveProps(props: Props) {
        if (this.isTicking(props))
            this.startTicking()
        else {
            this.stopTicking()
            this.setState({value: props.initialValue})
        }
    }

    private isTicking(props: Props = this.props): boolean {
        const {projectId, issueId, tickingStat} = props;

        if (!tickingStat.ticking)
            return false;

        if (!tickingStat.entry)
            return false;

        if (tickingStat.entry.projectId != projectId)
            return false;

        if (issueId && tickingStat.entry.issueId != issueId)
            return false;

        return true;
    }

    private stopTicking = () => {
        clearInterval(this.state.timerId)
    }

    private startTicking = () => {
        this.stopTicking();
        const timerId = setInterval(() => {
            const now = new Date().getTime()/1000;
            const elapsed = now - this.state.started;
            this.setState({value: this.state.value + elapsed, started: now});
        }, 1000);
        this.setState({timerId, started: new Date().getTime()/1000})
    }

    componentDidMount() {
        if (this.isTicking())
            this.startTicking()
    }

    componentWillUnmount() {
        this.stopTicking()
    }

    render() {
        const value = this.state.value;
        return <span>{this.isTicking() ? formatStopwatchDuration(value) : formatDuration(value)}</span>
    }
}

function mapStateToProps(state: State) {
    const { tickingStat } = state;
    return {
        tickingStat
    }
}

export default withStyles(styles)(connect(mapStateToProps)(StopWatch));
