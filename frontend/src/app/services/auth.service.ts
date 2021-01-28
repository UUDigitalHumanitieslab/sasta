import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { User } from '../models/user';
import { map } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  isAuthenticated$ = new BehaviorSubject<boolean>(false);
  authAPI = 'rest-auth';

  constructor(private httpClient: HttpClient) {
    this.checkAuthenticated();
  }

  checkAuthenticated() {
    this.getUser()
      .subscribe(
        (res) => {
          this.isAuthenticated$.next(true);
        },
        (err) => {
          this.isAuthenticated$.next(false);
        }
      );
  }

  isLoggedIn(): Observable<boolean> {
    return this.getUser().pipe(map(Boolean));
  }

  login(username: string, password: string): Observable<string> {
    return this.httpClient.post<string>(`${this.authAPI}/login/`, { username, password });
  }

  logout(): Observable<any> {
    return this.httpClient.post(`${this.authAPI}/logout/`, {});
  }

  register(username: string, password1: string, password2: string, email: string): Observable<any> {
    return this.httpClient.post(`${this.authAPI}/registration/`,
      { username, password1, password2, email });
  }

  getUser(): Observable<User> {
    return this.httpClient.get<User>(`${this.authAPI}/user/`);
  }

  infoFromConfirmKey(key: string): Observable<any> {
    return this.httpClient.get(`${this.authAPI}/infofromkey/${key}/`);
  }

  confirmEmail(key: string): Observable<any> {
    return this.httpClient.post(`${this.authAPI}/registration/verify-email/`, { key });
  }

}
