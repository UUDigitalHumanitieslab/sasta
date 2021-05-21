import { HttpClientTestingModule } from '@angular/common/http/testing';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';

import { ListMethodComponent } from './list-method.component';

describe('ListMethodComponent', () => {
  let component: ListMethodComponent;
  let fixture: ComponentFixture<ListMethodComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ListMethodComponent],
      imports: [RouterTestingModule, HttpClientTestingModule]
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
