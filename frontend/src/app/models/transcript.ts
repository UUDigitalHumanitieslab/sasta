import { Corpus } from './corpus';

export interface Transcript {
    name: string;
    content: string;
    parsed_content: string;
    status: 'created' | 'converting' | 'converted' | 'conversion-failed';
    corpus: Corpus;
}
