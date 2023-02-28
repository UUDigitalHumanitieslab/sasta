import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface ManualPageMetaData {
    title: string;
    id: string;
}

@Injectable({
    providedIn: 'root',
})
export class ManualService {
    constructor(private http: HttpClient) {}

    getManifest(): Observable<ManualPageMetaData[]> {
        return this.http.get<ManualPageMetaData[]>(
            this.docsPath('manifest.json')
        );
    }

    private docsPath = (file: string): string => `assets/manual/${file}`;
}
