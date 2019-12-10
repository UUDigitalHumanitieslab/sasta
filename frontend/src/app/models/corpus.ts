import { Transcript } from './transcript'

export interface Corpus {
    name: string;
    status: 'pending' | 'created';
    files?: File | { name: string }[];
    transcripts?: Transcript[];
}