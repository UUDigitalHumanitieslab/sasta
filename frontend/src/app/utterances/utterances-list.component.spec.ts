import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UtterancesListComponent } from './utterances-list.component';

describe('UtterancesListComponent', () => {
  let component: UtterancesListComponent;
  let fixture: ComponentFixture<UtterancesListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UtterancesListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UtterancesListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
