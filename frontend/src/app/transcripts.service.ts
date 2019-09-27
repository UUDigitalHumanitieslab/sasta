import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Transcript } from './models/transcript';

@Injectable({
    providedIn: 'root'
})
export class TranscriptsService {
    constructor(private httpClient: HttpClient) { }

    async upload(transcript: Transcript) {
        const formData: FormData = new FormData();
        formData.append('content', transcript.content, transcript.content.name);
        formData.append('filename', transcript.content.name);
        formData.append('name', transcript.name);
        await this.httpClient.post('/api/analysis/upload', formData).toPromise();
        return { name: transcript.name };
    }
}
