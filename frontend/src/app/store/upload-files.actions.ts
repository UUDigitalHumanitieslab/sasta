import { createAction, props } from '@ngrx/store';
import { UploadFile } from '../models/upload-file';

export const upload = createAction(
    '[UploadFiles] Upload',
    props<UploadFile>());

export const uploadSucceeded = createAction(
    '[UploadFiles] Upload success',
    props<{ name: string }>());
