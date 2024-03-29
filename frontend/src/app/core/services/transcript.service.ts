import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Transcript } from '@models';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root',
})
export class TranscriptService {
    constructor(private httpClient: HttpClient) {}

    getByID(id: number): Observable<Transcript> {
        return this.httpClient.get<Transcript>(`/api/transcripts/${id}/`);
    }

    toCHAT(id: number): Promise<Transcript> {
        return this.httpClient
            .get<Transcript>(`/api/transcripts/${id}/toCHAT/`)
            .toPromise();
    }

    /**
     * Parses a single trancript asychronously
     *
     * @param id transcript id
     * @returns parse task id
     */
    parse(id: number): Observable<string> {
        return this.httpClient.get<string>(`/api/transcripts/${id}/parse/`);
    }

    delete(id: number): Observable<null> {
        return this.httpClient.delete<null>(`/api/transcripts/${id}/`);
    }
}
