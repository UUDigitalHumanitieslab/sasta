import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CorpusRoutingModule } from './corpus-routing.module';
import { CorpusComponent } from './corpus-detail.component';
import { SharedModule } from '../shared/shared.module';
import { ListCorpusComponent } from './list-corpus.component';

@NgModule({
    declarations: [CorpusComponent, ListCorpusComponent],
    imports: [CommonModule, CorpusRoutingModule, SharedModule],
    exports: [CorpusComponent, ListCorpusComponent],
})
export class CorpusModule {}
