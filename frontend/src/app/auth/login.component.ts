import { Component, OnDestroy, OnInit } from '@angular/core';
import { faLock, faUser } from '@fortawesome/free-solid-svg-icons';
import { AuthService } from '../services/auth.service';
import { User } from '../models/user';
import { Router } from '@angular/router';
import { takeUntil } from 'rxjs/operators';
import { Subject } from 'rxjs';

@Component({
    selector: 'sas-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnDestroy, OnInit {
    faLock = faLock;
    faUser = faUser;

    username: string;
    password: string;

    processing = false;

    messages: { severity: string; summary: string; detail: string }[] = [];

    onDestroy$: Subject<boolean> = new Subject<boolean>();

    constructor(private authService: AuthService, private router: Router) {}

    ngOnInit() {}

    ngOnDestroy() {
        this.onDestroy$.next();
    }

    login() {
        this.processing = true;
        this.messages = [];
        this.authService
            .login(this.username, this.password)
            .pipe(takeUntil(this.onDestroy$))
            .subscribe(
                (res) => {
                    this.authService.isAuthenticated$.next(true);
                    this.router.navigate(['/corpora']);
                },
                (err) => {
                    this.messages.push({
                        severity: 'error',
                        summary: 'Login failed.',
                        detail: err.error.non_field_errors,
                    });
                    console.log('Http Error', err);
                    this.authService.isAuthenticated$.next(false);
                    this.processing = false;
                }
            );
    }
}
