import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { MethodService } from './method.service';

describe('TamService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [HttpClientTestingModule],
  }));

  it('should be created', () => {
    const service: MethodService = TestBed.get(MethodService);
    expect(service).toBeTruthy();
  });
});
