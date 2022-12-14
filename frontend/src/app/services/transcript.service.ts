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
     *
     * @param id transcript id
     * @returns parse task id
     */
    parse(id: number): Observable<string> {
        return this.httpClient.get<string>(`api/transcripts/${id}/parse/`);
    }

    delete(id): Observable<{}> {
        return this.httpClient.delete(`api/transcripts/${id}/`);
    }

}
