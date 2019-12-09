import { ActionReducer } from '@ngrx/store';
import { CorpusEffects } from './store/corpus.effects';
import { corpusReducer } from './store/corpus.reducer';
import { TranscriptsEffects } from './store/transcripts.effects';
import { transcriptsReducer } from './store/transcripts.reducer';


export const reducers = {
    transcripts: transcriptsReducer,
    corpus: corpusReducer
};

type ActionType<Type> = Type extends ActionReducer<infer T> ? T : never;

export type storeStructure = {
    [K in keyof typeof reducers]: ActionType<(typeof reducers)[K]>;
};

export const effects = [TranscriptsEffects, CorpusEffects];
