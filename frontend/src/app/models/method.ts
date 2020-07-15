import { Query } from './query';

export interface Method {
    name: string;
    content: File | { name: string };
    dateAdded?: Date;
    queries?: Query[];
}
