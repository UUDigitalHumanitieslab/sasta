import { Corpus } from './corpus';

export interface Transcript {
    name: string;
    content: string;
    status: 'created' | 'converting' | 'converted' | 'conversion-failed';
    corpus: Corpus;
}
