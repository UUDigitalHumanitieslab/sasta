import { Injectable } from '@angular/core';
import { Method } from '../models/method';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class MethodService {

  constructor(private httpClient: HttpClient) { }

  async list(): Promise<Method[]> {
    return await this.httpClient.get<Method[]>('api/assessment_methods/').toPromise();
  }

  async upload(method: Method) {
    const formData: FormData = new FormData();
    formData.append('content', method.content as File, method.content.name);
    formData.append('name', method.name);
    const response = await this.httpClient.post<Method>('api/assessment_methods/', formData).toPromise()
    return response;
  }
}
