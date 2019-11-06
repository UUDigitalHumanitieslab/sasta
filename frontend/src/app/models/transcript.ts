export interface Transcript {
    name: string;
    content: File | { name: string };
    status: 'uploading' | 'uploaded' | 'extracting' | 'extracted' | 'extraction-failed';
}
