import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { UploadFile } from '../models/upload-file';

@Injectable({
  providedIn: 'root'
})
export class UploadFileService {

  constructor(private httpClient: HttpClient) { }

  // async upload(uploadFile: UploadFile) {
  //   const formData: FormData = new FormData();
  //   formData.append('content', transcript.content as File, transcript.content.name);
  //   formData.append('filename', transcript.content.name);
  //   formData.append('name', transcript.name);
  //   return await this.httpClient.post<UploadResponse>('/api/analysis/upload', formData).toPromise();
  // }

  async upload(uploadFile: UploadFile, corpusname?: string) {
    const formData: FormData = new FormData();
    formData.append('content', uploadFile.content as File, uploadFile.content.name);
    formData.append('filename', uploadFile.content.name);
    formData.append('name', uploadFile.content.name);
    formData.append('corpus', uploadFile.corpus.name);
    return await this.httpClient.post<UploadFile>('api/upload_file', formData).toPromise();
  }

}
