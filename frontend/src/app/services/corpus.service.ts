import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Corpus } from '../models/corpus';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
    providedIn: 'root',
})
export class CorpusService {
    public corpora$: BehaviorSubject<Corpus[]> = new BehaviorSubject([] as any);

    constructor(private httpClient: HttpClient) {}

    updateCorpora() {
        this.httpClient
            .get<Corpus[]>('api/corpora/')
            .subscribe((res) => this.corpora$.next(res));
    }

    create(corpus: Corpus): Observable<any> {
        return this.httpClient.post('/api/corpora/', corpus);
    }

    delete(corpus: Corpus): Observable<any> {
        return this.httpClient.delete(`/api/corpora/${corpus.id}/`);
    }

    list(): Observable<Corpus[]> {
        return this.httpClient.get<Corpus[]>('api/corpora/');
    }

    get_by_id(id): Observable<Corpus> {
        return this.httpClient.get<Corpus>(`api/corpora/${id}/`);
    }

    query_transcript(transcriptID, methodID): Observable<any> {
        const formData: FormData = new FormData();
        formData.append('method', methodID);
        return this.httpClient.post(
            `api/transcripts/${transcriptID}/query/`,
            formData,
            { observe: 'response', responseType: 'blob' }
        );
    }

    annotate_transcript(transcriptID, methodID, outputFormat): Observable<any> {
        const formData: FormData = new FormData();
        formData.append('method', methodID);
        formData.append('format', outputFormat);
        return this.httpClient.post(
            `api/transcripts/${transcriptID}/annotate/`,
            formData,
            { observe: 'response', responseType: 'blob' }
        );
    }

    generate_form_transcript(transcriptID, methodID): Observable<any> {
        const formData: FormData = new FormData();
        formData.append('method', methodID);
        return this.httpClient.post(
            `api/transcripts/${transcriptID}/generateform/`,
            formData,
            { observe: 'response', responseType: 'blob' }
        );
    }

    convert_all(id): Observable<Corpus> {
        return this.httpClient.get<Corpus>(`api/corpora/${id}/convert_all/`);
    }

    parse_all(id): Observable<Corpus> {
        return this.httpClient.get<Corpus>(`api/corpora/${id}/parse_all/`);
    }

    parse_all_async(id): Observable<string> {
        // returns task id
        return this.httpClient.get<string>(
            `api/corpora/${id}/parse_all_async/`
        );
    }

    download_zip(id): Observable<any> {
        const formData: FormData = new FormData();
        return this.httpClient.post(`api/corpora/${id}/download/`, formData, {
            observe: 'response',
            responseType: 'blob',
        });
    }

    set_default_method(id, methodID): Observable<any> {
        const formData: FormData = new FormData();
        formData.append('method', methodID);
        return this.httpClient.post(
            `api/corpora/${id}/defaultmethod/`,
            formData
        );
    }
}
