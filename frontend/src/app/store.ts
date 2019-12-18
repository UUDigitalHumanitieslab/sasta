import { ActionReducer } from '@ngrx/store';
import { CorpusEffects } from './store/corpus.effects';
import { corpusReducer } from './store/corpus.reducer';
import { uploadFilesReducer } from './store/upload-files.reducer';
import { UploadFilesEffects } from './store/upload-files.effects';


export const reducers = {
    corpora: corpusReducer,
    uploadFiles: uploadFilesReducer
};

type ActionType<Type> = Type extends ActionReducer<infer T> ? T : never;

export type storeStructure = {
    [K in keyof typeof reducers]: ActionType<(typeof reducers)[K]>;
};

export const effects = [CorpusEffects, UploadFilesEffects];
