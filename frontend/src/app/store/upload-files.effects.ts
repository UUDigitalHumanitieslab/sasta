import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { mergeMap } from 'rxjs/operators';
import * as UploadFilesActions from './upload-files.actions';
import { UploadFileService } from '../services/upload-file.service';

@Injectable()
export class UploadFilesEffects {
    uploadFile$ = createEffect(() =>
        this.actions$.pipe(
            ofType(UploadFilesActions.upload),
            mergeMap(async (props) => {
                const response = await this.UploadFilesService.upload(props);
                return UploadFilesActions.uploadSucceeded({ name: response.content.name });
            })));


    constructor(
        private actions$: Actions,
        private UploadFilesService: UploadFileService
    ) { }
}
