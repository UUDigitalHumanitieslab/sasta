import { Component, Input, OnInit } from '@angular/core';
import {
    faCheck,
    faMinus,
    faProjectDiagram,
    faSearch,
    IconDefinition,
} from '@fortawesome/free-solid-svg-icons';
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
    faSearch = faSearch;
    faProjectDiagram = faProjectDiagram;

    _: any = _; // Lodash
    sortedUtterances: Utterance[];
    loadingTree = false;

    treeSentence?: string;
    treeXml?: string;

    constructor() {}

    ngOnInit(): void {}

    analysisIcon(u: Utterance): IconDefinition {
        return u.for_analysis ? faCheck : faMinus;
    }

    showTree(utterance: Utterance) {
        this.loadingTree = true;
        this.treeSentence = utterance.sentence;
        this.treeXml = utterance.parse_tree;
        this.loadingTree = false;
    }

    onCloseTree() {
        this.loadingTree = false;
        this.treeSentence = undefined;
        this.treeXml = undefined;
    }
}
