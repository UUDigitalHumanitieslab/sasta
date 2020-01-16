import { createAction, props } from '@ngrx/store';
import { Corpus } from '../models/corpus';

export const create = createAction(
    '[Corpora] Create',
    props<Corpus>());

export const createSucces = createAction(
    '[Corpora] Create success',
    props<{ name: string }>());

export const refreshList = createAction(
    '[Corpora] List',
    props<{}>());

export const listRetrieved = createAction(
    '[Corpora] List retrieved',
    props<{ corpora: Corpus[] }>());
