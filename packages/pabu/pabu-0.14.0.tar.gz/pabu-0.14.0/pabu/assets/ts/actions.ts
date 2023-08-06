import client from "./client";
import { pabuLocalStorage } from "./tools";
import { PaymentSubmitData, ServerIssueData, StateGetter, ThunkDispatcher, TickingStat } from "./types";

export enum Action {
    CLOSE_ISSUE_DIALOG = 'CLOSE_ADD_ISSUE_DIALOG',
    CLOSE_ADD_TIME_DIALOG = 'CLOSE_ADD_TIME_DIALOG',
    CLOSE_PROJECT_DIALOG = 'CLOSE_PROJECT_DIALOG',
    CLOSE_PAYMENT_DIALOG = 'CLOSE_PAYMENT_DIALOG',
    CLOSE_PROJECT = 'CLOSE_PROJECT',
    CLOSE_INVITE_DIALOG = 'CLOSE_INVITE_DIALOG',
    CLOSE_ISSUE_VIEW_DIALOG = 'CLOSE_ISSUE_VIEW_DIALOG',
    DELETE_PROJECT = 'DELETE_PROJECT',
    DELETE_ISSUE = 'DELETE_ISSUE',
    DELETE_TIME_ENTRY = 'DELETE_TIME_ENTRY',
    DELETE_PAYMENT = 'DELETE_PAYMENT',
    DELETE_PROJECT_TOKEN = 'DELETE_PROJECT_TOKEN',
    OPEN_ISSUE_DIALOG = 'OPEN_ISSUE_DIALOG',
    OPEN_INVITE_DIALOG = 'OPEN_INVITE_DIALOG',
    OPEN_PROJECT_DIALOG = 'OPEN_PROJECT_DIALOG',
    OPEN_ADD_TIME_DIALOG = 'OPEN_ADD_TIME_DIALOG',
    OPEN_PAYMENT_DIALOG = 'OPEN_PAYMENT_DIALOG',
    OPEN_PROJECT = 'OPEN_PROJECT',
    OPEN_ISSUE_VIEW_DIALOG = 'OPEN_ISSUE_VIEW_DIALOG',
    RECEIVE_ISSUES = 'RECEIVE_ISSUES',
    RECEIVE_TIME_ENTRIES = 'RECEIVE_TIME_ENTRIES',
    RECEIVE_PROJECTS = 'RECEIVE_PROJECTS',
    RECEIVE_TICKING_STAT = 'RECEIVE_TICKING_STAT',
    RECEIVE_USERS = 'RECEIVE_USERS',
    RECEIVE_PAYMENTS = 'RECEIVE_PAYMENTS',
    RECEIVE_PROJECT_TOKENS = 'RECEIVE_PROJECT_TOKENS',
    SET_DARK_THEME = 'SET_DARK_THEME',
    SET_PROJECT_DATA_AGE = 'SET_PROJECT_DATA_AGE',
    SET_LAST_SEEN_CHANGELOG_VERSION = 'SET_LAST_SEEN_CHANGELOG_VERSION',
}

export function setLastSeenChangelogVersion(version: string) {
    pabuLocalStorage.lastSeenChangelogVersion = version;
    return {
        type: Action.SET_LAST_SEEN_CHANGELOG_VERSION,
        version,
    }
}

export function fetchAllProjectData(id: number) {
    return dispatch =>
        client.getAllProjectData(id).then(data => {
            dispatch(receiveUsers(data.users))
            dispatch(receiveTimeEntries(data.timeEntries))
            dispatch(receiveProjectTokens(data.projectInvitationTokens))
            dispatch(receivePayments(data.payments))
            dispatch(receiveIssues(data.issues))
            dispatch(receiveProjects(data.projects))
            dispatch({
                type: Action.SET_PROJECT_DATA_AGE,
                id,
                time: new Date().getTime(),
            })
            return Promise.resolve(data)
        });
}

export function fetchAllProjectDataIfNeeded(id: number) {
    return (dispatch: ThunkDispatcher, getState: StateGetter) => {
        if (id in getState().projectDataAge)
            return;
        return dispatch(fetchAllProjectData(id));
    }
}

export function openProject(id: number) {
    return (dispatch: ThunkDispatcher) => {
        pabuLocalStorage.openedProjectId = id;
        dispatch({type: Action.OPEN_PROJECT,id});
        dispatch(fetchAllProjectDataIfNeeded(id));
    }
}

export function openIssueViewDialog(id: number) {
    return {
        type: Action.OPEN_ISSUE_VIEW_DIALOG,
        id,
    }
}

export function closeIssueViewDialog() {
    return {
        type: Action.CLOSE_ISSUE_VIEW_DIALOG,
    }
}

export function closeProject() {
    return {
        type: Action.CLOSE_PROJECT,
    }
}

export function openInviteDialog() {
    return {
        type: Action.OPEN_INVITE_DIALOG,
    }
}

export function closeInviteDialog() {
    return {
        type: Action.CLOSE_INVITE_DIALOG,
    }
}

export function joinToProject(token: string) {
    return dispatch => client.joinToProject(token);
}

export function kickUserFromProject(projectId: number, userId: number) {
    return dispatch => client.kickUserFromProject(projectId, userId);
}

export function leaveProject(projectId: number) {
    return dispatch => client.leaveProject(projectId).then(() => {
        dispatch({
            type: Action.DELETE_PROJECT,
            id: projectId,
        })
        return new Promise((resolve, reject) => resolve())
    });
}

export function openProjectDialog(id: number = null) {
    return {
        type: Action.OPEN_PROJECT_DIALOG,
        context: {id},
    }
}

export function closeProjectDialog() {
    return {
        type: Action.CLOSE_PROJECT_DIALOG,
    }
}

export function openIssueDialog(projectId: number, id: number = null){
    return {
        type: Action.OPEN_ISSUE_DIALOG,
        context: {projectId, id},
    }
}

export function closeIssueDialog() {
    return {
        type: Action.CLOSE_ISSUE_DIALOG,
    }
}

export function openPaymentDialog(projectId: number){
    return dispatch => {
        dispatch({
            type: Action.OPEN_PAYMENT_DIALOG,
            projectId,
        })
        return client.getProjectUsers(projectId).then(data => {
            dispatch(receiveUsers(data))
        })
    }
}

export function closePaymentDialog(){
    return {
        type: Action.CLOSE_PAYMENT_DIALOG,
    }
}

export function openAddTimeDialog(projectId: number, issueId: number = null){
    return {
        type: Action.OPEN_ADD_TIME_DIALOG,
        projectId,
        issueId,
    }
}

export function closeAddTimeDialog(){
    return {
        type: Action.CLOSE_ADD_TIME_DIALOG,
    }
}

export function fetchProjects(id: number = null, ) {
    return dispatch => {
        return client.getProjects(id).then(data => {
            dispatch(receiveProjects(data))
        })
    }
}

export function fetchProjectUsers(projectId: number) {
    return dispatch => {
        return client.getProjectUsers(projectId).then(data => {
            dispatch(receiveUsers(data))
        })
    }
}

export function fetchIssues(projectId: number) {
    return dispatch => {
        return client.getIssues(projectId).then(data => {
            dispatch(receiveIssues(data))
        })
    }
}
export function fetchProjectTokens(projectId: number) {
    return dispatch => {
        return client.getProjectTokens(projectId).then(data => {
            dispatch(receiveProjectTokens(data))
        })
    }
}

export function fetchTimeEntries(projectId: number) {
    return dispatch => client.getTimeEntries(projectId).then(data => dispatch(receiveTimeEntries(data)))
}

export function fetchPayments(projectId: number) {
    return dispatch => client.getPayments(projectId).then(data => dispatch(receivePayments(data)))
}

export function receiveProjectTokens(data) {
    return  {
        type: Action.RECEIVE_PROJECT_TOKENS,
        data,
    }
}

export function receiveUsers(data) {
    return  {
        type: Action.RECEIVE_USERS,
        data,
    }
}

export function receiveProjects(data) {
    return  {
        type: Action.RECEIVE_PROJECTS,
        data,
    }
}

export function receiveIssues(data, deepUpdate = false) {
    return  {
        type: Action.RECEIVE_ISSUES,
        data,
        deepUpdate,
    }
}

export function receiveTimeEntries(data) {
    return  {
        type: Action.RECEIVE_TIME_ENTRIES,
        data,
    }
}

export function receivePayments(data) {
    return  {
        type: Action.RECEIVE_PAYMENTS,
        data,
    }
}

export function sendProject(name: string, description: string, id: number = null) {
    return () => id ? client.updateProject(id, name, description) : client.createProject(name, description);
}

export function processIssues(issues: Array<ServerIssueData>) {
    return dispatch => client.processIssues(issues);
}

export function sendTime(projectId: number, time: string, amount: string, issueId: number = null) {
    return dispatch => {
        return client.addTime(projectId, amount, time, issueId).then(() => {
            dispatch(closeAddTimeDialog())
            dispatch(fetchAllProjectData(projectId));
        })
    }
}

export function createProjectToken(projectId: number) {
    return dispatch => client.createProjectToken(projectId).then(t => dispatch(receiveProjectTokens({[t.id]: t})));
}

export function deleteProjectToken(id: number) {
    return dispatch => client.deleteProjectToken(id).then(() => {
        dispatch({
            type: Action.DELETE_PROJECT_TOKEN,
            id,
        })
    });
}

export function receiveTickingStat(data: TickingStat) {
    return {
        type: Action.RECEIVE_TICKING_STAT,
        data,
    }
}

export function fetchTickingStat() {
    return dispatch => {
        return client.getTickingStat().then(data => {
            dispatch(receiveTickingStat(data))
        })
    }
}

export function startTime(projectId: number, issueId: number = null) {
    return dispatch => {
        return client.startTime(projectId, issueId).then(() => {
            dispatch(fetchTickingStat())
            dispatch(fetchTimeEntries(projectId))
        })
    }
}

export function stopTime() {
    return dispatch => {
        return client.stopTime().then(te => {
            dispatch(fetchTickingStat())
            dispatch(fetchProjects(te.projectId))
            dispatch(fetchTimeEntries(te.projectId))
            dispatch(fetchIssues(te.projectId))
        })
    }
}

export function sendPayment(projectId: number, data: PaymentSubmitData) {
    return dispatch => {
        return client.addPayment(projectId, data.amount, data.user_id, data.time, data.note).then(res => {
            dispatch(closePaymentDialog())
            dispatch(fetchAllProjectData(projectId));
        })
    }
}

export function deleteProject(id: number) {
    return dispatch => {
        return client.deleteProject(id).then(() => {
            dispatch(fetchProjects())
            dispatch({
                type: Action.DELETE_PROJECT,
                id,
            })
        })
    }
}

export function deletePayment(id: number) {
    return dispatch => client.deletePayment(id).then(() => {
        dispatch({
            type: Action.DELETE_PAYMENT,
            id,
        })
        return Promise.resolve()
    })
}

export function deleteTimeEntry(id: number) {
    return dispatch => client.deleteTimeEntry(id).then(() => {
        dispatch({
            type: Action.DELETE_TIME_ENTRY,
            id,
        })
        return Promise.resolve();
    })
}

export function deleteIssue(id: number, openedProjectId: number) {
    return dispatch => {
        return client.deleteIssue(id).then(() => {
            dispatch({
                type: Action.DELETE_ISSUE,
                id,
            })
            dispatch(fetchProjects(openedProjectId))
        })
    }
}

export function setDarkTheme(isSet: boolean) {
    pabuLocalStorage.isDarkTheme = isSet;
    return {
        type: Action.SET_DARK_THEME,
        isSet,
    }
}
