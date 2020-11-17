import { Corpus } from './corpus';

export interface Transcript {
    id?: number;
    name: string;
    content: string;
    parsed_content: string;
    status: number;
    status_name: 'unknown' | 'created' | 'converting' | 'converted' | 'conversion-failed' | 'parsing' | 'parsed' | 'parsing-failed';
    corpus: Corpus;
    utterances?: any[];
}

