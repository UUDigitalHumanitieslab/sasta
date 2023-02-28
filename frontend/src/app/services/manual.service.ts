import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { map } from 'rxjs/operators';

export interface ManualPageMetaData {
    title: string;
    id: string;
}

export interface ManualPage extends ManualPageMetaData {
    content: string;
}

@Injectable({
    providedIn: 'root',
})
export class ManualService {
    manifest$ = new Subject<ManualPageMetaData[]>();
    page$ = new Subject<ManualPage[]>();

    constructor(private http: HttpClient) {
        this.getManifest().subscribe(
            (man) => this.manifest$.next(man),
            (error) => console.error(error)
        );
    }

    getPage(meta: ManualPageMetaData): Observable<ManualPage> {
        const file = meta.id + '.md';
        const url = this.docsPath(file);
        return this.http
            .get(url, { responseType: 'text' })
            .pipe(map((text) => ({ ...meta, content: text })));
    }

    private getManifest(): Observable<ManualPageMetaData[]> {
        return this.http.get<ManualPageMetaData[]>(
            this.docsPath('manifest.json')
        );
    }

    private docsPath = (file: string): string => `assets/manual/${file}`;
}
