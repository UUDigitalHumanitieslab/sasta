import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { mergeMap } from 'rxjs/operators';
import * as CorpusActions from './corpus.actions';
import { CorpusService } from '../services/corpus.service';

@Injectable()
export class CorpusEffects {
    listCorpora$ = createEffect(() =>
        this.actions$.pipe(
            ofType(CorpusActions.refreshList),
            mergeMap(async () => {
                const corpora = await this.corpusService.list();
                return CorpusActions.listRetrieved({ corpora });
            })
        ));

    constructor(
        private actions$: Actions,
        private corpusService: CorpusService
    ) { }
}
