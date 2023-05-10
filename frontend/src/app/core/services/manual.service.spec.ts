import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { ManualService } from './manual.service';

describe('ManualService', () => {
    let service: ManualService;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [HttpClientTestingModule],
        });
        service = TestBed.inject(ManualService);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });
});
