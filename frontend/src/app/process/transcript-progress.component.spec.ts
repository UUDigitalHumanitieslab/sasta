import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { Transcript } from '@models';
import { TranscriptProgressCellComponent } from './transcript-progress-cell.component';

import { TranscriptProgressComponent } from './transcript-progress.component';

describe('TranscriptProgressComponent', () => {
    let component: TranscriptProgressComponent;
    let fixture: ComponentFixture<TranscriptProgressComponent>;

    const mockTranscript: Transcript = {
        id: 99,
        name: 'Tarsp_01',
        content: 'some/path/1.cha',
        parsed_content: 'some/path/1.xml',
        corrected_content: 'some/corrected/1.xml',
        status: 6,
        status_name: 'parsed',
        date_added: new Date(2021, 6, 3),
        corpus: 1,
        utterances: [
            {
                id: 1,
                for_analysis: true,
                sentence: 'hee',
                parse_tree: '',
                speaker: 'CHI',
                uttno: 1,
            },
            {
                id: 2,
                for_analysis: true,
                sentence: 'joe',
                parse_tree: '',
                speaker: 'INV',
                uttno: 2,
            },
        ],
    };

    beforeEach(waitForAsync(() => {
        TestBed.configureTestingModule({
            declarations: [
                TranscriptProgressComponent,
                TranscriptProgressCellComponent,
            ],
            schemas: [CUSTOM_ELEMENTS_SCHEMA],
        }).compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(TranscriptProgressComponent);
        component = fixture.componentInstance;
        component.transcript = mockTranscript;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
