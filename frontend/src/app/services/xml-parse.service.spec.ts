import { TestBed } from '@angular/core/testing';

import { XmlParseService } from './xml-parse.service';

describe('XmlParseService', () => {
  let service: XmlParseService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(XmlParseService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
