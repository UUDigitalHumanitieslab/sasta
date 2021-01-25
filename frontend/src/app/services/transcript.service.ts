import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Transcript } from '../models/transcript';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TranscriptService {

  constructor(private httpClient: HttpClient) { }

  get_by_id(id): Observable<Transcript> {
    return this.httpClient.get<Transcript>(`api/transcripts/${id}/`);
  }

  toCHAT(id): Promise<Transcript> {
    return this.httpClient.get<Transcript>(`api/transcripts/${id}/toCHAT/`).toPromise();
  }

  parse(id): Promise<Transcript> {
    return this.httpClient.get<Transcript>(`api/transcripts/${id}/parse/`).toPromise();
  }

  delete(id): Observable<{}> {
    return this.httpClient.delete(`api/transcripts/${id}/`);
  }
}
