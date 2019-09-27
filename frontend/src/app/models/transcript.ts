export interface Transcript {
    name: string;
    content: File;
    status: 'uploading' | 'uploaded';
}
