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

}

