import { Component, OnInit } from '@angular/core';
import { faLock, faUser } from '@fortawesome/free-solid-svg-icons'
import { AuthService } from '../services/auth.service';
import { User } from '../models/user';
import { Router } from '@angular/router';


@Component({
  selector: 'sas-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  faLock = faLock;
  faUser = faUser;

  username: string;
  password: string;

  processing: boolean = false;

  messages: { severity: string, summary: string, detail: string }[] = [];

  constructor(private authService: AuthService, private router: Router) { }

  ngOnInit() {
  }

  login() {
    this.processing = true;
    this.authService
      .login(this.username, this.password)
      .subscribe(
        res => {
          this.messages = [];
          this.authService.isAuthenticated$.next(true);
          this.router.navigate(['/corpora']);
        },
        err => {
          this.messages.push({ severity: 'error', summary: 'Login failed.', detail: err.error.non_field_errors })
          console.log('Http Error', err);
          this.authService.isAuthenticated$.next(false);
          this.processing = false;
        })
  }

}
