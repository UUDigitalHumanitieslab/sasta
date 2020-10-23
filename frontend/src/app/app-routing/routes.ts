import { Routes } from '@angular/router';
import { LoginComponent } from '../auth/login.component';
import { RegisterComponent } from '../auth/register.component';
import { VerifyComponent } from '../auth/verify.component';
import { CorpusComponent } from '../corpus/corpus.component';
import { ListCorpusComponent } from '../corpus/list-corpus.component';
import { HomeComponent } from '../home/home.component';
import { ListMethodComponent } from '../method/list-method.component';
import { MethodComponent } from '../method/method.component';
import { ProcessComponent } from '../process/process.component';
import { UploadComponent } from '../upload/upload.component';


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
        path: 'register',
        component: RegisterComponent
    },
    {
        path: 'confirm-email/:key',
        component: VerifyComponent
    },
    {
        path: '',
        redirectTo: '/home',
        pathMatch: 'full'
    }
];

export { routes };
