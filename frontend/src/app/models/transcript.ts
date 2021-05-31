import { Corpus } from './corpus';

interface AnalysisRun {
    id: number;
    created: Date;
    annotation_file: string;
}

export interface Transcript {
    id?: number;
    name: string;
    content: string;
    parsed_content: string;
    status: 'created' | 'converting' | 'converted' | 'conversion-failed';
    date_added?: Date;
    corpus: number;
    utterances?: any[];
    latest_run?: AnalysisRun;
}
