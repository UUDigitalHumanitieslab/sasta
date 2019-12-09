import { TestBed } from '@angular/core/testing';

import { TranscriptsService } from './transcripts.service';

describe('TranscriptsService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: TranscriptsService = TestBed.get(TranscriptsService);
    expect(service).toBeTruthy();
  });
});
