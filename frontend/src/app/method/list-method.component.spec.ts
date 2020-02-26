import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ListMethodComponent } from './list-method.component';

describe('ListMethodComponent', () => {
  let component: ListMethodComponent;
  let fixture: ComponentFixture<ListMethodComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ListMethodComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ListMethodComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
