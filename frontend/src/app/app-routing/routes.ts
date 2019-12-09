import { Routes } from '@angular/router';

import { HomeComponent } from '../home/home.component';
import { UploadComponent } from '../upload/upload.component';
import { TranscriptsComponent } from '../transcripts/transcripts.component';
import { ListCorpusComponent } from '../corpus/list-corpus.component';

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
        path: 'transcripts',
        component: TranscriptsComponent,
    },
    {
        path: 'corpora',
        component: ListCorpusComponent,
    },
    {
        path: '',
        redirectTo: '/home',
        pathMatch: 'full'
    }
];

export { routes };
