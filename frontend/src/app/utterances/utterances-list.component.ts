import { Component, Input, OnInit } from '@angular/core';
import { faCheck, faMinus } from '@fortawesome/free-solid-svg-icons';
import { Transcript, Utterance } from '../models/transcript';
import * as _ from 'lodash';

@Component({
    selector: 'sas-utterances-list',
    templateUrl: './utterances-list.component.html',
    styleUrls: ['./utterances-list.component.scss'],
})
export class UtterancesListComponent implements OnInit {
    @Input()
    set transcript(transcript: Transcript) {
        this.sortedUtterances = _.sortBy(transcript.utterances, (t) => t.uttno);
    }
    faCheck = faCheck;
    faMinus = faMinus;

    _: any = _; // Lodash
    sortedUtterances: Utterance[];

    constructor() {}

    ngOnInit(): void {}

    analysisIcon(u: Utterance) {
        return u.for_analysis ? faCheck : faMinus;
    }
}
