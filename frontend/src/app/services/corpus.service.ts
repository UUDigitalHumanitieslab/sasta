import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Corpus } from '../models/corpus';
import { BehaviorSubject, Observable, Subject } from 'rxjs';

@Injectable({
    providedIn: 'root',
})
export class CorpusService {
    private corpora$: Subject<Corpus[]> = new Subject();

    constructor(private httpClient: HttpClient) {}

    public getCorpora(): Observable<Corpus[]> {
        return this.corpora$;
    }

    public init() {
        this.httpClient
            .get<Corpus[]>('api/corpora/')
            .subscribe((corpora) => this.corpora$.next(corpora));
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
