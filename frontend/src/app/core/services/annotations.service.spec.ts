import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { AnnotationsService } from './annotations.service';

describe('AnnotationsService', () => {
    let service: AnnotationsService;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [HttpClientTestingModule],
        });
        service = TestBed.inject(AnnotationsService);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });
});
