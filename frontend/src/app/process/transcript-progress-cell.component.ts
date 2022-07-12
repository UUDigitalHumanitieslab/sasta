import { Component, Input, OnInit } from '@angular/core';
import { faCheck, faExclamationTriangle, faQuestion, faMinus } from '@fortawesome/free-solid-svg-icons';

@Component({
    selector: 'td[sas-transcript-progress-cell]',
    templateUrl: './transcript-progress-cell.component.html',
    styleUrls: ['./transcript-progress-cell.component.scss'],
})
export class TranscriptProgressCellComponent implements OnInit {
    @Input() evalProgress: () => number;
    faQuestion = faQuestion;
    faExclamation = faExclamationTriangle;
    faCheck = faCheck;
    faMinus = faMinus;

    constructor() {}

    ngOnInit() {}
}
