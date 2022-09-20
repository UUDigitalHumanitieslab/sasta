import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Transcript } from '../models/transcript';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root',
})
export class TranscriptService {
    constructor(private httpClient: HttpClient) {}

    get_by_id(id): Observable<Transcript> {
        return this.httpClient.get<Transcript>(`api/transcripts/${id}/`);
    }

    toCHAT(id): Promise<Transcript> {
        return this.httpClient
            .get<Transcript>(`api/transcripts/${id}/toCHAT/`)
            .toPromise();
    }

    /**
     * Parses a single trancript asychronously
     * @param id transcript id
     * @returns parse task id
     */
    parse(id: number): Observable<string> {
        return this.httpClient.get<string>(`api/transcripts/${id}/parse/`);
    }

    delete(id): Observable<{}> {
        return this.httpClient.delete(`api/transcripts/${id}/`);
    }

    latest_annotations(id): Observable<any> {
        return this.httpClient.get(
            `api/transcripts/${id}/annotations/latest/`,
            { observe: 'response', responseType: 'blob' }
        );
    }

    reset_annotations(id): Observable<any> {
        return this.httpClient.get(`api/transcripts/${id}/annotations/reset/`);
    }

    upload_annotations(
        filename: string,
        filecontent: File,
        transcript: Transcript
    ): Observable<any> {
        const formData = new FormData();
        formData.append('filename', filename);
        formData.append('content', filecontent);
        return this.httpClient.post(
            `api/transcripts/${transcript.id}/annotations/upload/`,
            formData
        );
    }
}
