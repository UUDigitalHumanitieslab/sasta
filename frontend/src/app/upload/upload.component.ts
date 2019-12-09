import { Component, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';

import { Store, select } from '@ngrx/store';
import { faUpload } from '@fortawesome/free-solid-svg-icons';

import { storeStructure } from '../store';
import { upload } from '../store/transcripts.actions';
import { Transcript } from '../models/transcript';
import { Corpus } from '../models/corpus'
import { Subscription } from 'rxjs';
import { CorpusService } from '../services/corpus.service';

@Component({
    selector: 'sas-upload',
    templateUrl: './upload.component.html',
    styleUrls: ['./upload.component.scss']
})
export class UploadComponent implements OnDestroy {
    content: File;
    name: string;

    fileName: string;
    faUpload = faUpload;

    uploading: boolean;
    subscriptions: Subscription[];

    corpora: Corpus[];
    selectedCorpus: Corpus;

    constructor(private store: Store<storeStructure>, router: Router, private corpusService: CorpusService) {
        this.subscriptions = [
            this.store.pipe(select('transcripts')).subscribe((transcripts: Transcript[]) => {
                // information about the transcript is available
                if (this.uploading) {
                    const transcript = transcripts.find(x => x.name === this.name);
                    if (transcript.status === 'uploaded') {
                        router.navigate(['/transcripts']);
                    }
                }
            })
        ];
    }

    ngOnInit() {
        this.corpusService.list()
            .then(response => { this.corpora = response; })
    }

    ngOnDestroy() {
        this.subscriptions.forEach(subscription => subscription.unsubscribe());
    }

    fileChange(fileInput: HTMLInputElement) {
        this.content = fileInput.files[0];
        this.fileName = this.content.name;
    }

    upload() {
        this.uploading = true;
        this.store.dispatch(upload({
            content: this.content,
            name: this.name,
            status: 'uploading'
        }));
    }
}
