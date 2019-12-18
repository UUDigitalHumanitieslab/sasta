import { Transcript } from './transcript'

export interface Corpus {
    id?: number;
    name: string;
    status: 'pending' | 'created';
    files?: File | { name: string }[];
    transcripts?: Transcript[];
}