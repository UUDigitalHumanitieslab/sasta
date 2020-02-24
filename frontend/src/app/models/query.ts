import { Method } from './method'

export interface Query {
    method: Method;
    query_id: string;
    category?: string;
    subcat?: string;
    level?: string;
    item?: string;
    altitems?: string;
    implies?: string;
    original?: boolean;
    pages?: string;
    phase?: string;
    query?: string;
    screening?: boolean;
    comments?: string;
}