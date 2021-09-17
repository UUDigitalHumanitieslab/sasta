import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UploadSafComponent } from './upload-saf.component';

describe('UploadSafComponent', () => {
  let component: UploadSafComponent;
  let fixture: ComponentFixture<UploadSafComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UploadSafComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UploadSafComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
