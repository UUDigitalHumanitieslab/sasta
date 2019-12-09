import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Transcript } from '../models/transcript';

interface UploadResponse {
    name: string;
}

@Injectable({
    providedIn: 'root'
})
export class TranscriptsService {
    constructor(private httpClient: HttpClient) { }

    async upload(transcript: Transcript) {
        const formData: FormData = new FormData();
        formData.append('content', transcript.content as File, transcript.content.name);
        formData.append('filename', transcript.content.name);
        formData.append('name', transcript.name);
        return await this.httpClient.post<UploadResponse>('/api/analysis/upload', formData).toPromise();
    }

    async list(): Promise<Transcript[]> {
        return await this.httpClient.get<Transcript[]>('api/upload-files/').toPromise();
    }
}