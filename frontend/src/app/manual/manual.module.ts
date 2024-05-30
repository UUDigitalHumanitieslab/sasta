import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ManualComponent } from './manual.component';
import { RouterModule } from '@angular/router';
import { ManualNavComponent } from './manual-nav.component';

@NgModule({
    declarations: [ManualComponent, ManualNavComponent],
    imports: [CommonModule, RouterModule],
    exports: [ManualComponent, ManualNavComponent],
})
export class ManualModule {}
