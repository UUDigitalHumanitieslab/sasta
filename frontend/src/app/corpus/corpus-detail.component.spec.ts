import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

import { CorpusComponent } from './corpus-detail.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { RouterTestingModule } from '@angular/router/testing';
import { MessageService } from 'primeng/api';

describe('CorpusComponent', () => {
    let component: CorpusComponent;
    let fixture: ComponentFixture<CorpusComponent>;

    beforeEach(waitForAsync(() => {
        TestBed.configureTestingModule({
            schemas: [NO_ERRORS_SCHEMA],
            declarations: [CorpusComponent],
            imports: [FontAwesomeModule, HttpClientTestingModule, RouterTestingModule],
            providers: [MessageService]
        })
            .compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(CorpusComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
