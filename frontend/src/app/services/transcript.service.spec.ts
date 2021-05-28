import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { TranscriptService } from './transcript.service';

describe('TranscriptService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [HttpClientTestingModule],
  }));

  it('should be created', () => {
    const service: TranscriptService = TestBed.get(TranscriptService);
    expect(service).toBeTruthy();
  });
});
