import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Corpus } from '../models/corpus';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CorpusService {

  constructor(private httpClient: HttpClient) { }

  async list(): Promise<Corpus[]> {
    return await this.httpClient.get<Corpus[]>('api/corpora/').toPromise();
  }

  get_by_id(id): Observable<Corpus> {
    return this.httpClient.get<Corpus>(`api/corpora/${id}/`);
  }

  score_transcript(id, phase?, phase_exact?, group_by?): Observable<any> {
    const formData: FormData = new FormData();
    if (phase) { formData.append('phase', phase) };
    if (phase_exact) { formData.append('phase_exact', phase_exact) };
    if (group_by) { formData.append('group_by', group_by) };

    return this.httpClient.post<any>(`api/transcripts/${id}/score/`, formData)
  }

}

