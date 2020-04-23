import { Routes } from '@angular/router';

import { HomeComponent } from '../home/home.component';
import { UploadComponent } from '../upload/upload.component';
import { ListCorpusComponent } from '../corpus/list-corpus.component';
import { CorpusComponent } from '../corpus/corpus.component';
import { ListMethodComponent } from '../method/list-method.component';
import { MethodComponent } from '../method/method.component';
import { LoginComponent } from '../auth/login.component';
import { ProcessComponent } from '../process/process.component';

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
        path: 'corpora/:id',
        component: CorpusComponent
    },
    {
        path: 'process/:id',
        component: ProcessComponent
    },
    {
        path: 'methods',
        component: ListMethodComponent,
    },
    {
        path: 'methods/:id',
        component: MethodComponent
    },
    {
        path: 'login',
        component: LoginComponent
    },
    {
        path: '',
        redirectTo: '/home',
        pathMatch: 'full'
    }
];

export { routes };
