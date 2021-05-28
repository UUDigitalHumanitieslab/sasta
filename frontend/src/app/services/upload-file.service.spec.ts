import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { UploadFileService } from './upload-file.service';

describe('UploadFileService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [HttpClientTestingModule],
  }));

  it('should be created', () => {
    const service: UploadFileService = TestBed.get(UploadFileService);
    expect(service).toBeTruthy();
  });
});
