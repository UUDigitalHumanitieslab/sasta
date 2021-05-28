import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { CorpusService } from './corpus.service';

describe('CorpusService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [HttpClientTestingModule],
  }));

  it('should be created', () => {
    const service: CorpusService = TestBed.get(CorpusService);
    expect(service).toBeTruthy();
  });
});
