import { TestBed } from '@angular/core/testing';

import { TamService } from './method.service';

describe('TamService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: TamService = TestBed.get(TamService);
    expect(service).toBeTruthy();
  });
});
