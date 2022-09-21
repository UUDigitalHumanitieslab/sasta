import { HttpClientTestingModule } from '@angular/common/http/testing';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { MessageService } from 'primeng/api';
import { StepsModule } from 'primeng/steps';
import { ParseService } from '../services/parse.service';

import { ProcessComponent } from './process.component';
import { TranscriptProgressCellComponent } from './transcript-progress-cell.component';
import { TranscriptProgressComponent } from './transcript-progress.component';

describe('ProcessComponent', () => {
    let component: ProcessComponent;
    let fixture: ComponentFixture<ProcessComponent>;

    beforeEach(waitForAsync(() => {
        TestBed.configureTestingModule({
            declarations: [
                ProcessComponent,
                TranscriptProgressComponent,
                TranscriptProgressCellComponent,
            ],
            providers: [ParseService, MessageService],
            imports: [
                StepsModule,
                RouterTestingModule,
                HttpClientTestingModule,
            ],
            schemas: [CUSTOM_ELEMENTS_SCHEMA],
        }).compileComponents();
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
