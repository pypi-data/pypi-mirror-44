import { ThunkDispatch } from "redux-thunk";
import { Action } from "redux";

export interface UserInfo {
    name: string,
    email: string,
    providerName: string,
    picture?: string,
}

export interface ApplicationData {
    isLoggedIn: boolean,
    userInfo: UserInfo,
    authBackendNames: Array<string>,
}

export interface User {
    id: number,
}

export interface TimeSummary {
    spent: number,
    lastEntry: number,
    count: number,
}

export interface ServerIssueData {
    id?: number,
    name?: string,
    desc?: string,
    projectId?: number,
    userId?: number,
    status?: string,
    rank?: number,
}

export interface PabuModel {
    id: number,
}

export interface Project extends PabuModel {
    name: string,
    desc: string,
    issues: Array<number>,
    users: Array<number>,
    payments: Array<number>,
    tokens: Array<number>,
    timeStat: TimeSummary,
    paid: number,
}

export enum IssueStatus {
    TODO = 'todo',
    IN_PROGRESS = 'in progress',
    DONE = 'done',
}

export interface Issue extends PabuModel {
    name: string,
    desc: string,
    projectId: number,
    reporterId: number,
    assigneeId: number,
    timeEntries: Array<number>,
    timeStat: TimeSummary,
    status: IssueStatus,
    rank: number,
    statusDate: number,
}

export interface TimeEntry extends PabuModel {
    issueId: number,
    projectId: number,
    start: number,
    end: number,
    userId: number,
}

export interface ExpandedTimeEntry extends TimeEntry {
    issueName: string,
    issueStatus: IssueStatus,
    userName: string,
    spentHours: number,
}

export interface User {
    id: number,
    name: string,
    avatar: string,
}

export interface PaymentSubmitData {
    user_id: number,
    amount: string,
    note: string,
    time: string,
}

export interface Payment extends PabuModel {
    projectId: number,
    createdUserId: number,
    paidUserId: number,
    amount: number,
    time: number,
    note: string,
}

export interface ProjectInvitationToken extends PabuModel {
    projectId: number,
    token: string,
}

export interface ExpandedPayment extends Payment {
    createdUserName: string,
    paidUserName: string,
}


export interface TickingStat {
    ticking: boolean,
    entry?: TimeEntry,
}

export type ProjectSubmitCallback = (id: number, name: string, desc: string) => void;
export type NameDescSubmitCallback = (name: string, desc: string) => void;
export type TimeEntrySubmitCallback = (projectId: number, start: Date, issueId?: number, end?: Date) => void;

export type ProjectMap = { [n: number]: Project };
export type IssueMap = { [n: number]: Issue };
export type TimeEntryMap = { [n: number]: TimeEntry };
export type UserMap = { [n: number]: User };
export type PaymentMap = { [n: number]: Payment };
export type ProjectInvitationTokenMap = { [n: number]: ProjectInvitationToken };

export type ProjectDialogContext = {id?: number};
export type IssueDialogContext = {projectId: number, id?: number};
export type TimeDialogContext = {projectId: number, issueId: number};
export type IssueByStatusMap = { [s: string ]: Array<Issue> };
export type ProjectDataAgeMap = { [s: number]: number }
export type IssueViewDialogContext = {id: number, show: boolean}

export type AllProjectData = {
    projects: ProjectMap,
    issues: IssueMap,
    timeEntries: TimeEntryMap,
    users: UserMap,
    payments: PaymentMap,
    projectInvitationTokens: ProjectInvitationTokenMap,
}

export interface State extends AllProjectData {
    addTimeDialogContext: TimeDialogContext,
    isDarkTheme: boolean,
    issueDialogContext: IssueDialogContext,
    openedProjectId: number,
    paymentDialogProjectId: number,
    projectDialogContext: ProjectDialogContext,
    tickingStat: TickingStat,
    projectInvitationTokens: ProjectInvitationTokenMap,
    inviteDialogIsOpen: boolean,
    projectDataAge: ProjectDataAgeMap,
    issueViewDialogContext: IssueViewDialogContext,
    lastSeenChangelogVersion: string,
}

export type ThunkDispatcher = ThunkDispatch<{}, undefined, Action>;

export type IssueListLayout = 'list' | 'card';

export type IssueStatusFilterStatusMap = {
    [IssueStatus.TODO]: boolean,
    [IssueStatus.IN_PROGRESS]: boolean,
    [IssueStatus.DONE]: boolean,
}

export class LocalStorageSchema {
    openedProjectId: number = 0;
    isDarkTheme: boolean = false;
    openedProjectTab: number = 0;
    issueListLayout: IssueListLayout = 'list';
    issueDoneDateFilter: number = 0;
    issueTableFilters: IssueStatusFilterStatusMap = {
        [IssueStatus.TODO]: true,
        [IssueStatus.IN_PROGRESS]: true,
        [IssueStatus.DONE]: false,
    };
    lastSeenChangelogVersion: string = 'v0.0.0';
}

export type StateGetter = () => State;

export interface VersionChangeLog {
    name: string,
    enh: Array<string>,
    fix: Array<string>,
    date: number,
}

export type Changelog = Array<VersionChangeLog>;

export interface AppData {
    changelog: Changelog,
    userInfo: UserInfo,
    isLoggedIn: boolean
    authBackendNames: Array<string>,
    version: string,
    initialData: AllProjectData,
}
