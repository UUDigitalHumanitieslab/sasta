import { Corpus } from './corpus';

export enum TranscriptStatus {
    UNKNOWN, CREATED,
    CONVERTING, CONVERTED, CONVERSION_FAILED,
    PARSING, PARSED, PARSING_FAILED
}

export interface Transcript {
    id?: number;
    name: string;
    content: string;
    parsed_content: string;
    status: number;
    status_name: 'unknown' | 'created' | 'converting' | 'converted' | 'conversion-failed' | 'parsing' | 'parsed' | 'parsing-failed';
    date_added?: Date;
    corpus: number;
    utterances?: any[];
}

