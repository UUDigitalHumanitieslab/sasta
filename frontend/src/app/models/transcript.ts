import { Corpus } from './corpus';

export interface Transcript {
    name: string;
    content: File | { name: string };
    status: 'created' | 'converting' | 'converted';
    corpus: Corpus;
}
