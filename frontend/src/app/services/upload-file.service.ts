import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { UploadFile } from '../models/upload-file';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UploadFileService {

  constructor(private httpClient: HttpClient) { }

  async upload(uploadFile: UploadFile) {
    const formData: FormData = new FormData();
    formData.append('content', uploadFile.content as File, uploadFile.content.name);
    formData.append('name', uploadFile.name);
    formData.append('corpus', uploadFile.corpus.name);
    formData.append('status', 'pending');
    const response = await this.httpClient.post<UploadFile>('api/upload_files/', formData).toPromise()
    return response;
  }

  upload_obs(uploadFile: UploadFile): Observable<UploadFile> {
    const formData: FormData = new FormData();
    formData.append('content', uploadFile.content as File, uploadFile.content.name);
    formData.append('name', uploadFile.name);
    formData.append('corpus', uploadFile.corpus.name);
    formData.append('status', 'pending');
    return this.httpClient.post<UploadFile>('api/upload_files/', formData)
  }



}
