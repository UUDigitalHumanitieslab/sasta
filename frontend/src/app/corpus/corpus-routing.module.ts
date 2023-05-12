import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from '../auth/auth.guard';
import { CorpusComponent } from './corpus-detail.component';
import { ListCorpusComponent } from './list-corpus.component';

const routes: Routes = [
    {
        path: '',
        component: ListCorpusComponent,
        canActivate: [AuthGuard],
    },
    {
        path: ':id',
        component: CorpusComponent,
        canActivate: [AuthGuard],
    },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule],
})
export class CorpusRoutingModule {}
