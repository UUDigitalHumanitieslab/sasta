import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import * as _ from 'lodash';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Method } from '../models/method';
import { MethodCategory } from '../models/methodcategory';

@Injectable({
    providedIn: 'root',
})
export class MethodService {
    private methods$ = new BehaviorSubject<Method[]>([]);
    private categories$ = new BehaviorSubject<MethodCategory[]>([]);

    constructor(private http: HttpClient) {
        this.initCategories();
        this.initMethods();
    }

    public initCategories() {
        this.http
            .get<MethodCategory[]>('api/method_categories/')
            .subscribe((categories) => this.categories$.next(categories));
    }

    public initMethods() {
        this.http
            .get<Method[]>('api/assessment_methods/')
            .subscribe((methods) => this.methods$.next(methods));
    }

    public getMethods(): Observable<Method[]> {
        return this.methods$;
    }

    public getMethodsForCategory(c: MethodCategory): Observable<Method[]> {
        return this.methods$.pipe(
            map((methods) =>
                methods.filter((method) => method.category.id === c.id)
            )
        );
    }

    public getCategories(): Observable<MethodCategory[]> {
        return this.categories$;
    }

    public getCategory(id): Observable<MethodCategory> {
        return this.categories$.pipe(
            map((cats) => cats.filter((cat) => cat.id === id)),
            map((cats) => cats[0])
        );
    }

    public getMethod(id): Observable<Method> {
        return this.methods$.pipe(
            map((methods) => methods.filter((method) => method.id === id)),
            map((methods) => methods[0])
        );
    }

    async upload(method: Method) {
        const formData: FormData = new FormData();
        formData.append('content', method.content as File, method.content.name);
        formData.append('name', method.name);
        const response = await this.http
            .post<Method>('api/assessment_methods/', formData)
            .toPromise();
        return response;
    }

    groupMethods(methods: Method[], categoryID: number) {
        return _(methods)
            .filter((m) => m.category.id === categoryID)
            .groupBy('category.name')
            .map((groupedMethods, methodCat) => ({
                label: methodCat,
                items: _.map(groupedMethods, (m: Method) => ({
                    label: m.name,
                    value: m,
                })),
            }))
            .value();
    }
}
