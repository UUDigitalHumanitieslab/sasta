import { createAction, props } from '@ngrx/store';
import { Corpus } from '../models/corpus';

export const refreshList = createAction(
    '[Corpora] List',
    props<{}>());

export const listRetrieved = createAction(
    '[Corpora] List retrieved',
    props<{ corpora: Corpus[] }>());
