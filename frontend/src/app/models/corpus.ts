import { Method } from './method';
import { Transcript } from './transcript';

export interface Corpus {
    id?: number;
    name: string;
    status: 'created';
    files?: File | { name: string }[];
    default_method?: Method;
    transcripts?: Transcript[];
}
