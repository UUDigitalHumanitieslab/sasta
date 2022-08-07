import { TestBed } from '@angular/core/testing';

import { XmlParseService } from './xml-parse.service';
import { ExtractinatorService } from 'lassy-xpath';

describe('XmlParseService', () => {
    let service: XmlParseService;

    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [ExtractinatorService],
        });
        service = TestBed.inject(XmlParseService);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });
});
