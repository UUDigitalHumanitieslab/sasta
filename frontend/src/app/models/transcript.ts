import { Corpus } from './corpus';

export interface Transcript {
    id?: number;
    name: string;
    content: string;
    parsed_content: string;
    status: 'created' | 'converting' | 'converted' | 'conversion-failed';
    corpus: number;
    utterances?: any[];
}
