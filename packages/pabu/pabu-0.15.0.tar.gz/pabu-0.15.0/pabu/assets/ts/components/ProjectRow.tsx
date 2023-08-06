import { Tab, Tabs, ExpansionPanel, ExpansionPanelSummary, Typography, ExpansionPanelDetails, Theme, createStyles, withStyles } from '@material-ui/core';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import * as React from 'react';
import IssueList from '../containers/IssueList';
import PaymentList from '../containers/PaymentList';
import ProjectInviteTokenList from '../containers/ProjectInviteTokenList';
import ProjectSummary from '../containers/ProjectSummary';
import TimeEntryList from '../containers/TimeEntryList';
import { Project } from '../types';
import ProjectUserList from '../containers/ProjectUserList';
import StopWatch from '../containers/StopWatch';
import { pabuLocalStorage } from '../tools';


const styles = ({ palette, typography }: Theme) => createStyles({
    root: {
        width: '100%',
    },
    heading: {
        fontSize: typography.pxToRem(15),
        flexBasis: '33.33%',
        flexShrink: 0,
    },
    secondaryHeading: {
        fontSize: typography.pxToRem(15),
        color: palette.text.secondary,
    },
    tabLabel: {
        color: palette.text.primary,
    },
    tabHeader: {
        backgroundColor: palette.background.default,
        marginTop: 10,
    },
});

type Props = {
    classes: any,
    handleChange: (id: number) => void,
    project: Project,
    expanded: boolean,
    onHoverTitle: () => void,
}

type State = {
    currentTab: number,
}

class ProjectRow extends React.Component<Props, State> {

    constructor(props: Props) {
        super(props)
        this.state = {currentTab: pabuLocalStorage.openedProjectTab};
    }

    handleTabChange = (ev, val:number) => {
        this.setState({currentTab: val});
        pabuLocalStorage.openedProjectTab = val;
    }

    render() {
        const {classes, handleChange, project, expanded, onHoverTitle} = this.props

        const id = project.id;

        let spent = (project.timeStat.spent/3600).toFixed(1);
        let paid = Math.ceil(project.paid/3600);

        return  <ExpansionPanel
                    className={classes.root}
                    expanded={expanded}
                    key={id}
                    onChange={handleChange.bind(this, id)}
                >
                    <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />} onMouseOver={onHoverTitle}>
                        <Typography className={classes.heading}>{project.name}</Typography>
                        <Typography className={classes.secondaryHeading}>
                            Spent <StopWatch projectId={id} initialValue={project.timeStat.spent} /> in {project.issues.length} tasks ({paid} hours paid)
                        </Typography>
                    </ExpansionPanelSummary>
                    <ExpansionPanelDetails style={{display: 'block'}}>
                        <Tabs
                            value={this.state.currentTab}
                            onChange={this.handleTabChange}
                            className={classes.tabHeader}
                            indicatorColor="primary"
                            variant="fullWidth"
                        >
                            <Tab label="Summary" className={classes.tabLabel} />
                            <Tab label={`Time entries (${project.timeStat.count})`} className={classes.tabLabel} />
                            <Tab label={`Tasks (${project.issues.length})`} className={classes.tabLabel} />
                            <Tab label={`Payments (${project.payments.length})`} className={classes.tabLabel} />
                            <Tab label={`Invite tokens (${project.tokens.length})`} className={classes.tabLabel} />
                            <Tab label={`Users (${project.users.length})`} className={classes.tabLabel} />
                        </Tabs>
                        {this.state.currentTab == 0 && <ProjectSummary id={id} />}
                        {this.state.currentTab == 1 && <TimeEntryList id={id} />}
                        {this.state.currentTab == 2 && <IssueList id={id} />}
                        {this.state.currentTab == 3 && <PaymentList id={id} /> }
                        {this.state.currentTab == 4 && <ProjectInviteTokenList id={id} /> }
                        {this.state.currentTab == 5 && <ProjectUserList id={id} /> }
                    </ExpansionPanelDetails>
                </ExpansionPanel>
    }
};

export default withStyles(styles)(ProjectRow);
