import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { mergeMap } from 'rxjs/operators';
import * as TranscriptsActions from './transcripts.actions';
import { TranscriptsService } from '../transcripts.service';

@Injectable()
export class TranscriptsEffects {
    uploadTranscripts$ = createEffect(() =>
        this.actions$.pipe(
            ofType(TranscriptsActions.upload),
            mergeMap(async (props) => {
                const response = await this.transcriptsService.upload(props);
                return TranscriptsActions.uploadSucceeded({ name: response.name });
            })));

    listTranscripts$ = createEffect(() =>
        this.actions$.pipe(
            ofType(TranscriptsActions.refreshList),
            mergeMap(async () => {
                const transcripts = await this.transcriptsService.list();
                return TranscriptsActions.listRetrieved({ transcripts });
            })
        ));

    constructor(
        private actions$: Actions,
        private transcriptsService: TranscriptsService
    ) { }
}
