import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Transcript } from '../models/transcript';

@Injectable({
    providedIn: 'root',
})
export class AnnotationsService {
    constructor(private http: HttpClient) {}

    annoBaseRoute(id: number): string {
        return `api/transcripts/${id}/annotations/`;
    }

    latest(transcriptID: number): Observable<any> {
        return this.http.get(this.annoBaseRoute(transcriptID) + 'latest/', {
            observe: 'response',
            responseType: 'blob',
        });
    }

    reset(transcriptID: number): Observable<any> {
        return this.http.get(this.annoBaseRoute(transcriptID) + 'reset/');
    }

    upload(
        filename: string,
        filecontent: File,
        transcript: Transcript
    ): Observable<any> {
        const formData = new FormData();
        formData.append('filename', filename);
        formData.append('content', filecontent);
        return this.http.post(
            this.annoBaseRoute(transcript.id) + 'upload/',
            formData
        );
    }
}
