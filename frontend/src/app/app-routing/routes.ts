import { Routes } from '@angular/router';

import { HomeComponent } from '../home/home.component';
import { UploadComponent } from '../upload/upload.component';
import { ListCorpusComponent } from '../corpus/list-corpus.component';
import { CorpusComponent } from '../corpus/corpus.component';
import { ListMethodComponent } from '../method/list-method.component';

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
        path: 'methods',
        component: ListMethodComponent,
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
