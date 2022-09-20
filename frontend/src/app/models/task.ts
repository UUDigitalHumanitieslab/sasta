export type TaskStatus =
    | 'PENDING'
    | 'STARTED'
    | 'RETRY'
    | 'FAILURE'
    | 'SUCCESS';

export interface TaskResult {
    id: string;
    status: TaskStatus;
    result: string;
}
