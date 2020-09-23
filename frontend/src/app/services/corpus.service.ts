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
    return this.httpClient.get<Corpus[]>('api/corpora/');
  }


  get_by_id(id): Observable<Corpus> {
    return this.httpClient.get<Corpus>(`api/corpora/${id}/`);
  }

  query_transcript(transcriptID, methodID): Observable<any> {
    const formData: FormData = new FormData();
    formData.append('method', methodID);
    return this.httpClient.post(`api/transcripts/${transcriptID}/query/`, formData, { observe: 'response', responseType: 'blob' });
  }

  annotate_transcript(transcriptID, methodID, onlyInform): Observable<any> {
    const formData: FormData = new FormData();
    formData.append('method', methodID);
    formData.append('only_inform', onlyInform);
    return this.httpClient.post(`api/transcripts/${transcriptID}/annotate/`, formData, { observe: 'response', responseType: 'blob' });
  }

  convert_all(id): Observable<Corpus> {
    return this.httpClient.get<Corpus>(`api/corpora/${id}/convert_all/`);
  }

  parse_all(id): Observable<Corpus> {
    return this.httpClient.get<Corpus>(`api/corpora/${id}/parse_all/`);
  }

  download_zip(id): Observable<any> {
    const formData: FormData = new FormData();
    return this.httpClient.post(`api/corpora/${id}/download/`, formData, { observe: 'response', responseType: 'blob' });
  }

}

