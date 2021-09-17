import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import * as _ from 'lodash';
import { Observable } from 'rxjs';
import { Method } from '../models/method';
import { MethodCategory } from '../models/methodcategory';

@Injectable({
  providedIn: 'root'
})
export class MethodService {

  constructor(private httpClient: HttpClient) { }

  list(): Observable<Method[]> {
    return this.httpClient.get<Method[]>('api/assessment_methods/');
  }

  get_by_id(id): Observable<Method> {
    return this.httpClient.get<Method>(`api/assessment_methods/${id}/`);
  }

  async upload(method: Method) {
    const formData: FormData = new FormData();
    formData.append('content', method.content as File, method.content.name);
    formData.append('name', method.name);
    const response = await this.httpClient.post<Method>('api/assessment_methods/', formData).toPromise();
    return response;
  }

  listCategories(): Observable<MethodCategory[]> {
    return this.httpClient.get<MethodCategory[]>('api/method_categories/');
  }

  groupMethods(methods: Method[], categoryID: number) {
    return _(methods)
      .filter(m => m.category.id === categoryID)
      .groupBy('category.name')
      .map((groupedMethods, methodCat) =>
      ({
        label: methodCat, items: _.map(groupedMethods, (m: Method) =>
          ({ label: m.name, value: m }))
      })
      )
      .value();
  }
}
