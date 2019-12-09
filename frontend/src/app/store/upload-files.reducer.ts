import { Action, createReducer, on } from '@ngrx/store';
import { upload, uploadSucceeded } from './upload-files.actions';
import { UploadFile } from '../models/upload-file';

const reducer = createReducer<UploadFile[]>([],
    on(upload, (state, action) => [...state, action]),
    on(uploadSucceeded, (state, action) => {
        const index = state.findIndex(x => x.content.name === action.name);
        state[index].status = 'uploaded';
        return [...state];
    }));
export function uploadFilesReducer(state: UploadFile[], action: Action) {
    return reducer(state, action);
}
