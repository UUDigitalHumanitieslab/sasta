import { Transcript } from './transcript';

export interface Corpus {
    id?: number;
    name: string;
    status: 'created';
    files?: File | { name: string }[];
    transcripts?: Transcript[];
}
