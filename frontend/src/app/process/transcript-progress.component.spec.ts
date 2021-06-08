import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TranscriptProgressComponent } from './transcript-progress.component';

describe('TranscriptProgressComponent', () => {
  let component: TranscriptProgressComponent;
  let fixture: ComponentFixture<TranscriptProgressComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TranscriptProgressComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TranscriptProgressComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
