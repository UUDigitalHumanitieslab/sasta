import { Component, OnInit } from '@angular/core';
import { Store, select } from '@ngrx/store';
import { Subscription, interval } from 'rxjs';
import { storeStructure } from '../store';
import { Transcript } from '../models/transcript';
import { refreshList } from '../store/transcripts.actions';
import { startWith } from 'rxjs/operators';
import { TranscriptsService } from '../transcripts.service'

// check every 10 seconds
const UPDATE_INTERVAL = 10000;

@Component({
    selector: 'sas-transcripts',
    templateUrl: './transcripts.component.html',
    styleUrls: ['./transcripts.component.scss']
})
export class TranscriptsComponent implements OnInit {
    subscriptions: Subscription[];
    transcripts: Transcript[];

    constructor(private store: Store<storeStructure>, private transcriptsService: TranscriptsService) {
        this.subscriptions = [
            this.store.pipe(select('transcripts')).subscribe((transcripts: Transcript[]) => {
                this.transcripts = transcripts;
            }),
            interval(UPDATE_INTERVAL).pipe(startWith(0)).subscribe(() => {
                store.dispatch(refreshList({}));
            })
        ];
    }

    ngOnInit() {
    }

    convertTranscript(transcript: Transcript) {
        this.transcriptsService.convert(transcript);
    }

    deleteTranscript(transcript: Transcript) {
        this.transcriptsService.delete(transcript);
    }
}
