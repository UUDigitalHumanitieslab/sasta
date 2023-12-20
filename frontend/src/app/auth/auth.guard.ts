import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, Router } from '@angular/router';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { AuthService } from '@services';

@Injectable({
    providedIn: 'root',
})
export class AuthGuard  {
    constructor(private authService: AuthService, private router: Router) {}

    canActivate(
        next: ActivatedRouteSnapshot,
        state: RouterStateSnapshot
    ):
        | Observable<boolean | UrlTree>
        | Promise<boolean | UrlTree>
        | boolean
        | UrlTree {
        if (this.authService.currentUser$.getValue()) {
            // if there is already a logged in user, no need to recheck
            return of(true);
        }

        return this.authService.getCompleteUser().pipe(
            map((userData) => {
                if (!!userData) {
                    return true;
                }
            }),
            catchError(() => {
                this.router.navigate(['/login']);
                return of(false);
            })
        );
    }
}
