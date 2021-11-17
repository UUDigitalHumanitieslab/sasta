import { Component, Input, OnInit } from '@angular/core';
import { faCheck, faMinus } from '@fortawesome/free-solid-svg-icons';
import { Transcript, Utterance } from '../models/transcript';

@Component({
    selector: 'sas-utterances-list',
    templateUrl: './utterances-list.component.html',
    styleUrls: ['./utterances-list.component.scss'],
})
export class UtterancesListComponent implements OnInit {
    @Input() transcript: Transcript;

    faCheck = faCheck;
    faMinus = faMinus;

    constructor() {}

    ngOnInit(): void {}

    analysisIcon(u: Utterance) {
        return u.for_analysis ? faCheck : faMinus;
    }
}
