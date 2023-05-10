import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { MessageService } from 'primeng/api';

import { ParseService } from './parse.service';

describe('ParseService', () => {
    let service: ParseService;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [HttpClientTestingModule],
            providers: [MessageService],
        });
        service = TestBed.inject(ParseService);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });
});
