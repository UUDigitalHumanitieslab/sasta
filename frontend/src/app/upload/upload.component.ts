import { Component, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';

import { Store, select } from '@ngrx/store';
import { faUpload } from '@fortawesome/free-solid-svg-icons';

import { storeStructure } from '../store';
import { upload } from '../store/upload-files.actions';
import { create } from '../store/corpus.actions';
import { Corpus } from '../models/corpus'
import { Subscription } from 'rxjs';
import { CorpusService } from '../services/corpus.service';
import { UploadFile } from '../models/upload-file';
import { UploadFileService } from '../services/upload-file.service';

@Component({
    selector: 'sas-upload',
    templateUrl: './upload.component.html',
    styleUrls: ['./upload.component.scss']
})
export class UploadComponent implements OnDestroy {
    content: File;
    newCorpusName: string;

    fileName: string;
    faUpload = faUpload;

    uploading: boolean;
    subscriptions: Subscription[];

    corpora: Corpus[];
    selectedCorpus: Corpus;

    constructor(private store: Store<storeStructure>, private router: Router, private corpusService: CorpusService, private uploadFileService: UploadFileService) {
        this.subscriptions = [
            this.store.pipe(select('uploadFiles')).subscribe((uploadFiles: UploadFile[]) => {
                // information about the file is available
                if (this.uploading) {
                    const file = uploadFiles.find(x => x.content.name === this.content.name);
                    if (file.status === 'uploaded') {
                        router.navigate(['/corpora']);
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
        this.uploadFileService.upload_obs({
            name: this.fileName,
            content: this.content,
            status: 'uploading',
            corpus: this.selectedCorpus || { name: this.newCorpusName, status: 'created' }
        })
            .subscribe(
                response => {
                    this.uploading = false;
                    this.router.navigate([`/process/${response.corpus_id}`])
                },
                error => {
                    this.uploading = false;
                    console.log(error);
                }
            )

    }
}
