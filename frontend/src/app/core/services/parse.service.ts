import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { MessageService } from 'primeng/api';
import { Observable, timer } from 'rxjs';
import {
    catchError,
    concatMap,
    filter,
    switchMap,
    take,
    tap,
} from 'rxjs/operators';
import { TaskResult } from '@models';
import { Transcript } from '@models';
import { TranscriptService } from './transcript.service';

@Injectable({
    providedIn: 'root',
})
export class ParseService {
    apiRoot = 'api';
    parseRoot = this.apiRoot + '/parse';
    transcriptRoot = this.apiRoot + '/transcripts';

    constructor(
        private http: HttpClient,
        private msgService: MessageService,
        private transcriptService: TranscriptService
    ) {}

    msgTaskComplete = (response: TaskResult): void => {
        this.msgService.add({
            severity: 'success',
            summary: 'Task complete',
            detail: response.result,
            sticky: false,
        });
    };

    msgConvertComplete = (transcript: Transcript): void => {
        this.msgService.add({
            severity: 'success',
            summary: 'Task complete',
            detail: `Converted ${transcript.name}`,
            sticky: false,
        });
    };

    taskSuccess = (response: TaskResult): boolean =>
        response.status === 'SUCCESS';

    /**
     * Converts a single transcript, depending on input
     * .doc -> .txt
     * .txt -> .cha
     * .cha -> .cha (preprocessing)
     *
     * @param transcriptID transcript id
     * @returns converted transcript
     */
    convert(transcriptID: number): Observable<Transcript> {
        return this.http
            .get<Transcript>(`${this.transcriptRoot}/${transcriptID}/convert/`)
            .pipe(tap(this.msgConvertComplete));
    }

    /**
     * Creates asynchronous parse job
     *
     * @param transcriptID transcript id
     * @returns observable of parse task id
     */
    createParseTask(transcriptID: number): Observable<string> {
        return this.http.get<string>(
            `${this.transcriptRoot}/${transcriptID}/parse_async/`
        );
    }

    getParseTask(taskID: string): Observable<TaskResult> {
        return this.http.get<TaskResult>(`${this.parseRoot}/task/${taskID}/`);
    }

    pollParseTask(taskID: string): Observable<TaskResult> {
        return timer(0, 5000).pipe(
            switchMap((_) => this.getParseTask(taskID)),
            filter(this.taskSuccess),
            take(1)
        );
    }

    parse(transcript: Transcript): Observable<TaskResult> {
        return this.createParseTask(transcript.id).pipe(
            switchMap((taskID) => this.pollParseTask(taskID)),
            tap(this.msgTaskComplete)
        );
    }

    fullProcess(transcript: Transcript): Observable<Transcript> {
        return this.convert(transcript.id).pipe(
            concatMap((t) => this.parse(t)),
            concatMap(() => this.transcriptService.getByID(transcript.id)),
            catchError((err) => {
                throw new Error(err);
            })
        );
    }
}
