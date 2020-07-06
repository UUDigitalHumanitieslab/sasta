import { Component, OnInit } from '@angular/core';
import { faLock, faUser, faEnvelope } from '@fortawesome/free-solid-svg-icons';

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
  password1: string;
  password2: string;

  processing: boolean = false;

  constructor() { }

  ngOnInit() {
  }

  register() {
  }

  passwordSame() {
    return this.password1 && this.password2 && (this.password1 == this.password2);
  }

}
