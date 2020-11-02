import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { AuthGuard } from './auth.guard';
import { routes } from './routes';

@NgModule({
    imports: [
        RouterModule.forRoot(routes),
        RouterModule
    ],
    exports: [RouterModule],
    providers: [AuthGuard],
    declarations: [],
})
export class AppRoutingModule {
}
