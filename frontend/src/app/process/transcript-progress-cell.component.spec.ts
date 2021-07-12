import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { Transcript } from '../models/transcript';

import { TranscriptProgressCellComponent } from './transcript-progress-cell.component';

describe('TranscriptProgressCellComponent', () => {
  let component: TranscriptProgressCellComponent;
  let fixture: ComponentFixture<TranscriptProgressCellComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [TranscriptProgressCellComponent],
      schemas: [CUSTOM_ELEMENTS_SCHEMA]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TranscriptProgressCellComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});