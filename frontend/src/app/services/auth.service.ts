import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { User } from '../models/user';


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  isAuthenticated$ = new BehaviorSubject<boolean>(false);

  constructor(private httpClient: HttpClient) {
    this.getUser()
      .toPromise()
      .then(
        _res => this.isAuthenticated$.next(true),
        _err => this.isAuthenticated$.next(false)
      );
  }

  login(username: string, password: string): Observable<String> {
    return this.httpClient.post<String>('rest-auth/login/', { username: username, password: password });
  }

  logout(): Observable<any> {
    return this.httpClient.post('rest-auth/logout/', {});
  }

  register(username: string, password1: string, password2: string, email: string): Observable<any> {
    return this.httpClient.post('rest-auth/register/',
      { username: username, password1: password1, password2: password2, email: email });
  }

  getUser(): Observable<User> {
    return this.httpClient.get<User>('rest-auth/user/');
  }

}