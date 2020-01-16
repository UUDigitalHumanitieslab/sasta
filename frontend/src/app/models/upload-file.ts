import { Corpus } from './corpus';

export interface UploadFile {
    name: string;
    content: File | { name: string };
    status: 'uploading' | 'uploaded' | 'extracting' | 'extracted' | 'extraction-failed';
    corpus?: Corpus;
}