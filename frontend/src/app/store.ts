import { ActionReducer } from '@ngrx/store';

import { transcriptsReducer } from './store/transcripts.reducer';
import { TranscriptsEffects } from './store/transcripts.effects';

export const reducers = {
    transcripts: transcriptsReducer
};

type ActionType<Type> = Type extends ActionReducer<infer T> ? T : never;

export type storeStructure = {
    [K in keyof typeof reducers]: ActionType<(typeof reducers)[K]>;
};

export const effects = [TranscriptsEffects];
