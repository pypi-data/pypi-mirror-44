import { Project, Issue, TimeEntryMap, ProjectInvitationToken, ProjectInvitationTokenMap, IssueStatus, ServerIssueData, IssueMap, AllProjectData, TimeEntry } from "./types";
import { convertKeysToSnakeCase, convertKeysToCamelCase } from "./tools";

class PabuClient {

    private _path: string;

    constructor() {
        this._path = '/api/'
    }

    private async _send(method: string, params: Array<any> = []) {
        let payload = {
            method: method,
            id : new Date().getTime(),
            jsonrpc : "2.0",
            params: params
        }

        const resp = await fetch(this._path, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });
        const data = await resp.json();
        if (data.error) {
            console.error(data.error)
            throw new Error('server error');
        }
        return convertKeysToCamelCase(data.result);
    }

    async getProjects(id: number = null) {
        return this._send('get_projects', [id]);
    }

    async getIssues(project_id: number) {
        return this._send('get_issues', [project_id]);
    }

    async getPayments(project_id: number) {
        return this._send('get_payments', [project_id]);
    }

    async getTimeEntries(project_id: number): Promise<TimeEntryMap> {
        return this._send('get_time_entries', [project_id]);
    }

    async getProjectUsers(project_id: number) {
        return this._send('get_project_users', [project_id]);
    }

    async createProject(name: string, description: string): Promise<Project> {
        return this._send('create_project', [name, description]);
    }

    async updateProject(id: number, name: string, description: string): Promise<Project> {
        return this._send('update_project', [id, name, description]);
    }

    async processIssues(issues: Array<ServerIssueData>): Promise<IssueMap> {
        return this._send('process_issues', [issues.map(convertKeysToSnakeCase)]);
    }

    async addTime(projectId: number, amount: string, time: string, issueId: number = null) {
        return this._send('add_time', [projectId, amount, time, issueId]);
    }

    async startTime(projectId: number, issueId: number = null) {
        return this._send('start_time', [projectId, issueId]);
    }

    async addPayment(projectId: number, amount: string, paidUserId: number, time: string, note: string) {
        return this._send('add_payment', [projectId, amount, paidUserId, time, note]);
    }

    async stopTime(): Promise<TimeEntry> {
        return this._send('stop_time');
    }

    async deleteProject(id: number) {
        return this._send('delete_project', [id]);
    }

    async deleteTimeEntry(id: number) {
        return this._send('delete_time_entry', [id]);
    }

    async deletePayment(id: number) {
        return this._send('delete_payment', [id]);
    }

    async deleteIssue(id: number) {
        return this._send('delete_issue', [id]);
    }

    async getTickingStat() {
        return this._send('get_ticking_stat');
    }

    async getProjectTokens(project_id: number): Promise<ProjectInvitationTokenMap> {
        return this._send('get_project_tokens', [project_id]);
    }

    async createProjectToken(project_id: number): Promise<ProjectInvitationToken> {
        return this._send('create_project_token', [project_id]);
    }

    async deleteProjectToken(id: number) {
        return this._send('delete_project_token', [id]);
    }

    async joinToProject(token: string) {
        return this._send('join_to_project', [token]);
    }

    async kickUserFromProject(projectId: number, userId: number) {
        return this._send('kick_user_from_project', [projectId, userId]);
    }

    async leaveProject(projectId: number) {
        return this._send('leave_project', [projectId]);
    }

    async getAllProjectData(projectId: number): Promise<AllProjectData> {
        return this._send('get_all_project_data', [projectId]);
    }
}

export default new PabuClient();
