import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Utterance } from '../models/transcript';

import { UtterancesListComponent } from './utterances-list.component';

describe('UtterancesListComponent', () => {
    let component: UtterancesListComponent;
    let fixture: ComponentFixture<UtterancesListComponent>;
    const testUtterances: Utterance[] = [
        {
            uttno: 1,
            id: 1,
            sentence: 'Hier staat een test zin',
            speaker: 'CHI',
            for_analysis: true,
            parse_tree: '',
        },
        {
            uttno: 2,
            id: 2,
            sentence: 'Hier staat nog een test zin',
            speaker: 'INV',
            for_analysis: false,
            parse_tree: '',
        },
    ];

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [UtterancesListComponent],
        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(UtterancesListComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
    it('should return correct icon', () => {
        expect(component.analysisIcon(testUtterances[0])).toBe(
            component.faCheck
        );
        expect(component.analysisIcon(testUtterances[1])).toBe(
            component.faMinus
        );
    });
});
