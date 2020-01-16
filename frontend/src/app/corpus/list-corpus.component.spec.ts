import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ListCorpusComponent } from './list-corpus.component';

describe('ListCorpusComponent', () => {
  let component: ListCorpusComponent;
  let fixture: ComponentFixture<ListCorpusComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ListCorpusComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ListCorpusComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
