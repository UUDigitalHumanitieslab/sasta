import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UploadComponent } from './upload.component';
import { SharedModule } from '../shared/shared.module';

@NgModule({
    declarations: [UploadComponent],
    imports: [CommonModule, SharedModule],
    exports: [UploadComponent],
})
export class UploadModule {}
