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

  list_obs(): Observable<Corpus[]> {
    return this.httpClient.get<Corpus[]>('api/corpora/')
  }


  get_by_id(id): Observable<Corpus> {
    return this.httpClient.get<Corpus>(`api/corpora/${id}/`);
  }

  score_transcript(id, method): Observable<any> {
    const formData: FormData = new FormData();
    formData.append('method', method)
    return this.httpClient.post(`api/transcripts/${id}/score/`, formData, { observe: 'response', responseType: 'blob' })
  }

  annotate_transcript(id, method): Observable<any> {
    const formData: FormData = new FormData();
    formData.append('method', method);
    return this.httpClient.post(`api/transcripts/${id}/annotate/`, formData, { observe: 'response', responseType: 'blob' });
  }

}

