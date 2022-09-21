import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export type AnnotationOutputFormat = 'xlsx' | 'cha';

@Injectable({
    providedIn: 'root',
})
export class AnalysisService {
    constructor(private http: HttpClient) {}

    query(transcriptID, methodID): Observable<any> {
        const formData: FormData = new FormData();
        formData.append('method', methodID);
        return this.http.post(
            `api/transcripts/${transcriptID}/query/`,
            formData,
            { observe: 'response', responseType: 'blob' }
        );
    }

    annotate(
        transcriptID,
        methodID,
        outputFormat: AnnotationOutputFormat
    ): Observable<any> {
        const formData: FormData = new FormData();
        formData.append('method', methodID);
        formData.append('format', outputFormat);
        return this.http.post(
            `api/transcripts/${transcriptID}/annotate/`,
            formData,
            { observe: 'response', responseType: 'blob' }
        );
    }

    generateForm(transcriptID, methodID): Observable<any> {
        const formData: FormData = new FormData();
        formData.append('method', methodID);
        return this.http.post(
            `api/transcripts/${transcriptID}/generateform/`,
            formData,
            { observe: 'response', responseType: 'blob' }
        );
    }
}
