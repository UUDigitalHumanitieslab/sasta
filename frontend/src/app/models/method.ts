import { Query } from './query';
import { MethodCategory } from './methodcategory';

export interface Method {
    name: string;
    category: MethodCategory;
    content: File | { name: string };
    date_added?: Date;
    queries: Query[];
}
