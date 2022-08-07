import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { ConfirmationService, MessageService } from 'primeng/api';

import { ListCorpusComponent } from './list-corpus.component';

describe('ListCorpusComponent', () => {
    let component: ListCorpusComponent;
    let fixture: ComponentFixture<ListCorpusComponent>;

    beforeEach(waitForAsync(() => {
        TestBed.configureTestingModule({
            declarations: [ListCorpusComponent],
            imports: [RouterTestingModule, HttpClientTestingModule],
            providers: [ConfirmationService, MessageService],
        }).compileComponents();
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
