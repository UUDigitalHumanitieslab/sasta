import { Component, OnInit } from '@angular/core';
import { faLock, faUser, faEnvelope } from '@fortawesome/free-solid-svg-icons';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'sas-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {
  faLock = faLock;
  faUser = faUser;
  faEnvelope = faEnvelope;

  username: string;
  emailAddress: string;
  password1: string = '';
  password2: string;

  processing = false;

  constructor(private authService: AuthService, private router: Router, private messageService: MessageService) { }

  ngOnInit() {
  }

  passwordSame() {
    return this.password1 && this.password2 && (this.password1 === this.password2);
  }

  passwordMinLength() {
    return this.password1.length >= 8;
  }

  containsSpace(str: string) {
    return str.indexOf(' ') >= 0;
  }

  usernameValid() {
    return !this.containsSpace(this.username);
  }

  onError(err) {
    this.authService.isAuthenticated$.next(false);
    this.processing = false;
    let detailMsg;

    if (err.error.username) {
    } else if (err.error.email) {
      detailMsg = err.error.email[0];
    } else if (err.error.password1) {
      detailMsg = err.error.password1[0];
    } else {
      detailMsg = err.error;
    }
    const msg = { severity: 'error', summary: 'Registration failed.', detail: detailMsg, sticky: true };
    this.messageService.add(msg);
  }

  register() {
    this.processing = true;
    this.authService
      .register(this.username, this.password1, this.password2, this.emailAddress)
      .subscribe(
        () => {
          this.messageService.add({
            severity: 'success',
            summary: 'Registration success',
            detail: `E-mail confirmation request sent to ${this.emailAddress}.`,
            life: 6000
          });
          this.router.navigate(['/login']);
        },
        err => {
          this.onError(err);
        });
  }

}
