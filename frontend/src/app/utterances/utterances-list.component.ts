import { Component, Input, OnInit } from '@angular/core';
import { Transcript } from '../models/transcript';

@Component({
    selector: 'sas-utterances-list',
    templateUrl: './utterances-list.component.html',
    styleUrls: ['./utterances-list.component.scss'],
})
export class UtterancesListComponent implements OnInit {
    @Input() transcript: Transcript;

    constructor() {}

    ngOnInit(): void {}
}
