import { Action, createReducer, on } from '@ngrx/store';
import { listRetrieved } from './corpus.actions';
import { Corpus } from '../models/corpus';

const reducer = createReducer<Corpus[]>([],
    on(listRetrieved, (_, action) => {
        return action.corpora;
    }));

export function corpusReducer(state: Corpus[], action: Action) {
    return reducer(state, action);
}
