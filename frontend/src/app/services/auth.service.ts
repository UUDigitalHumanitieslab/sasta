import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { map, switchMap } from 'rxjs/operators';
import { User } from '../models/user';

@Injectable({
    providedIn: 'root',
})
export class AuthService {
    authAPI = 'rest-auth';
    isAuthenticated$ = new BehaviorSubject<boolean>(false);
    currentUser$ = new BehaviorSubject<User>(null);

    constructor(private httpClient: HttpClient) {
        this.setUser();
    }

    setUser() {
        this.getCompleteUser().subscribe(
            (res) => {
                this.isAuthenticated$.next(true);
                this.currentUser$.next(res);
            },
            (err) => {
                this.isAuthenticated$.next(false);
                this.currentUser$.next(null);
            }
        );
    }

    login(username: string, password: string): Observable<string> {
        return this.httpClient.post<string>(`${this.authAPI}/login/`, {
            username,
            password,
        });
    }

    logout(): Observable<any> {
        return this.httpClient.post(`${this.authAPI}/logout/`, {});
    }

    register(
        username: string,
        password1: string,
        password2: string,
        email: string
    ): Observable<any> {
        return this.httpClient.post(`${this.authAPI}/registration/`, {
            username,
            password1,
            password2,
            email,
        });
    }

    getCompleteUser() {
        return this.httpClient.get<User>(`${this.authAPI}/user/`).pipe(
            switchMap((user) => {
                return this.isAdmin().pipe(
                    map((adminStatus) => {
                        user.isAdmin = adminStatus;
                        return user;
                    })
                );
            })
        );
    }

    isAdmin(): Observable<boolean> {
        return this.httpClient
            .get(`${this.authAPI}/has_admin_access/`)
            .pipe(map((response) => response[`has_admin_access`] as boolean));
    }

    infoFromConfirmKey(key: string): Observable<any> {
        return this.httpClient.get(`${this.authAPI}/infofromkey/${key}/`);
    }

    confirmEmail(key: string): Observable<any> {
        return this.httpClient.post(
            `${this.authAPI}/registration/verify-email/`,
            { key }
        );
    }
}
