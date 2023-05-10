import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from '../auth/auth.guard';
import { ListMethodComponent } from './list-method.component';
import { MethodComponent } from './method.component';

const routes: Routes = [
    {
        path: '',
        component: ListMethodComponent,
        canActivate: [AuthGuard],
    },
    {
        path: ':id',
        component: MethodComponent,
        canActivate: [AuthGuard],
    },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule],
})
export class MethodRoutingModule {}
