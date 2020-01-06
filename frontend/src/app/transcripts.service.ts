import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Transcript } from './models/transcript';

interface UploadResponse {
    name: string;
}
interface ListResponse {
    files: {
        name: string,
        file_name: string,
        status: string
    }[];
}
interface ConvertResponse {
    msg: string;
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
        const response = await this.httpClient.get<ListResponse>('/api/analysis/list').toPromise();
        return response.files.map(file => ({
            name: file.name,
            content: { name: file.file_name },
            status: file.status as Transcript['status']
        }));
    }

    async convert(transcript: Transcript) {
        const formData: FormData = new FormData();
        formData.append('filename', transcript.content.name);
        formData.append('name', transcript.name);
        return await this.httpClient.post<ConvertResponse>('api/analysis/convert', formData).toPromise();
    }

    async delete(transcript: Transcript) {
        const formData: FormData = new FormData();
        formData.append('filename', transcript.content.name);
        formData.append('name', transcript.name);
        return await this.httpClient.post<ConvertResponse>('api/analysis/delete', formData).toPromise();
    }
}
