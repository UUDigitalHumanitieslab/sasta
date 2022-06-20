import { Component, NgZone, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import {
    faFileUpload, faFolder,
    faListAlt, faUser, faUserShield
} from '@fortawesome/free-solid-svg-icons';
import { environment } from '../../environments/environment';
import { animations, showState } from '../animations';
import { User } from '../models/user';
import { AuthService } from '../services/auth.service';


@Component({
    animations,
    selector: 'sas-menu',
    templateUrl: './menu.component.html',
    styleUrls: ['./menu.component.scss'],
})
export class MenuComponent implements OnInit {
    burgerShow: showState;
    burgerActive = false;
    public activeUser: User;
    public isAuthenticated$ = this.authService.isAuthenticated$;
    public isAdmin: boolean;

    faUser = faUser;
    faFolder = faFolder;
    faListAlt = faListAlt;
    faFileUpload = faFileUpload;
    faUserShield = faUserShield;
    version = environment.appVersion;

    constructor(
        private ngZone: NgZone,
        private authService: AuthService,
        private router: Router
    ) {}

    ngOnInit() {
        this.isAuthenticated$.subscribe((authenticated) => {
            if (authenticated) {
                this.authService.getUser().subscribe(
                    async (res) => {
                        this.activeUser = res;
                        this.isAdmin = await this.authService.isAdmin();
                    },
                    (err) => console.log('Http Error', err)
                );
            } else {
                this.activeUser = null;
            }
        });
    }

    isAuthenticated() {
        return this.authService.isAuthenticated$.getValue();
    }

    logout() {
        this.authService.logout().subscribe(
            (res) => {
                this.router.navigate(['/login']);
                this.authService.isAuthenticated$.next(false);
                this.activeUser = null;
            },
            (err) => console.log('Http Error', err)
        );
    }

    toggleBurger() {
        if (!this.burgerActive) {
            // make it active to make it visible (add a class to
            // override it being hidden for smaller screens)
            this.burgerActive = true;
            // immediately hide it
            this.burgerShow = 'hide';
            setTimeout(() => {
                this.ngZone.run(() => {
                    // trigger the transition
                    this.burgerShow = 'show';
                });
            });
            return;
        }

        this.burgerShow = this.burgerShow === 'show' ? 'hide' : 'show';
    }
}
