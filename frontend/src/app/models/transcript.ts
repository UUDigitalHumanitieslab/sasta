interface AnalysisRun {
    id: number;
    created: Date;
    annotation_file: string;
    method: number;
    is_manual_correction: boolean;
}

export interface Utterance {
    id: number;
    sentence: string;
    speaker: string;
    utt_id: number;
    xsid?: number;
    for_analysis: boolean;
}

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
    utterances?: Utterance[];
    latest_run?: AnalysisRun;
    latest_corrections?: AnalysisRun;
    target_speakers?: string;
}

