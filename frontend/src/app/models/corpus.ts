import { Transcript } from './transcript'

export interface Corpus {
    name: string;
    status: 'created';
    files?: File | { name: string }[];
    transcripts?: Transcript[];
}