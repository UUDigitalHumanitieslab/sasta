import { Routes } from '@angular/router';
import { LoginComponent } from '../auth/login.component';
import { RegisterComponent } from '../auth/register.component';
import { VerifyComponent } from '../auth/verify.component';
import { CorpusComponent } from '../corpus/corpus.component';
import { ListCorpusComponent } from '../corpus/list-corpus.component';
import { TranscriptComponent } from '../transcript/transcript.component';
import { ListMethodComponent } from '../method/list-method.component';
import { MethodComponent } from '../method/method.component';
import { ProcessComponent } from '../process/process.component';
import { UploadComponent } from '../upload/upload.component';
import { AuthGuard } from './auth.guard';
import { ManualComponent } from '../manual/manual.component';

const routes: Routes = [
    {
        path: 'upload',
        component: UploadComponent,
        canActivate: [AuthGuard],
    },
    {
        path: 'corpora',
        component: ListCorpusComponent,
        canActivate: [AuthGuard],
    },
    {
        path: 'corpora/:id',
        component: CorpusComponent,
        canActivate: [AuthGuard],
    },
    {
        path: 'transcript/:id',
        component: TranscriptComponent,
        canActivate: [AuthGuard],
    },
    {
        path: 'process/:id',
        component: ProcessComponent,
        canActivate: [AuthGuard],
    },
    {
        path: 'methods',
        component: ListMethodComponent,
        canActivate: [AuthGuard],
    },
    {
        path: 'methods/:id',
        component: MethodComponent,
        canActivate: [AuthGuard],
    },
    {
        path: 'login',
        component: LoginComponent,
    },
    {
        path: 'register',
        component: RegisterComponent,
    },
    {
        path: 'confirm-email/:key',
        component: VerifyComponent,
    },
    {
        path: 'manual',
        component: ManualComponent,
    },
    {
        path: '',
        redirectTo: '/corpora',
        pathMatch: 'full',
    },
];

export { routes };
