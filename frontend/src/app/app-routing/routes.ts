import { Routes } from '@angular/router';

import { HomeComponent } from '../home/home.component';
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
        path: '',
        redirectTo: '/home',
        pathMatch: 'full'
    }
];

export { routes };
