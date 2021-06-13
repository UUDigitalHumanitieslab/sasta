import { HttpClientTestingModule } from '@angular/common/http/testing';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { StepsModule } from 'primeng/steps';

import { ProcessComponent } from './process.component';
import { TranscriptProgressCellComponent } from './transcript-progress-cell.component';
import { TranscriptProgressComponent } from './transcript-progress.component';

describe('ProcessComponent', () => {
  let component: ProcessComponent;
  let fixture: ComponentFixture<ProcessComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ProcessComponent, TranscriptProgressComponent, TranscriptProgressCellComponent],
      imports: [StepsModule, RouterTestingModule, HttpClientTestingModule],
      schemas: [CUSTOM_ELEMENTS_SCHEMA]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProcessComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
