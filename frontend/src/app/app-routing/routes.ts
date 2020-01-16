import { Routes } from '@angular/router';

import { HomeComponent } from '../home/home.component';
import { UploadComponent } from '../upload/upload.component';
import { ListCorpusComponent } from '../corpus/list-corpus.component';
import { CorpusComponent } from '../corpus/corpus.component';

const routes: Routes = [
    {
        path: 'home',
        component: HomeComponent,
    },
    {
        path: 'upload',
        component: UploadComponent,
    },
    {
        path: 'corpora',
        component: ListCorpusComponent,
    },
    {
        path: 'corpus/:id',
        component: CorpusComponent
    },
    {
        path: '',
        redirectTo: '/home',
        pathMatch: 'full'
    }
];

export { routes };
