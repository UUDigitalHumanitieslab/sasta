import { createAction, props } from '@ngrx/store';
import { Transcript } from '../models/transcript';

export const upload = createAction(
    '[Transcripts] Upload',
    props<Transcript>());

export const uploadSucceeded = createAction(
    '[Transcripts] Upload success',
    props<{ name: string }>());
