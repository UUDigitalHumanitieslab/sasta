import { Method } from './method';

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
    fase?: string;
    query?: string;
    inform?: string;
    screening?: boolean;
    process?: number;
    special1?: string;
    special2?: string;
    comments?: string;
}
