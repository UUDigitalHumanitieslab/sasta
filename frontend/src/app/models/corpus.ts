import { Transcript } from './transcript';

export interface Corpus {
    id?: number;
    name: string;
    status: 'created';
    date_added?: Date;
    date_modified?: Date;
    files?: File | { name: string }[];
    transcripts?: Transcript[];
}
