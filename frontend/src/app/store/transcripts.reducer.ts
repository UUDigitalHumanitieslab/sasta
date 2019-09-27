import { Action, createReducer, on } from '@ngrx/store';
import { upload, uploadSucceeded } from './transcripts.actions';
import { Transcript } from '../models/transcript';

const reducer = createReducer<Transcript[]>([],
    on(upload, (state, action) => [...state, action]),
    on(uploadSucceeded, (state, action) => {
        const index = state.findIndex(x => x.name === action.name);
        state[index].status = 'uploaded';
        return [...state];
    }));

export function transcriptsReducer(state: Transcript[], action: Action) {
    return reducer(state, action);
}
