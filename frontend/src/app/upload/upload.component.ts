import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { faUpload } from '@fortawesome/free-solid-svg-icons';
import { Subscription } from 'rxjs';
import { Corpus } from '../models/corpus';
import { CorpusService } from '../services/corpus.service';
import { UploadFileService } from '../services/upload-file.service';



@Component({
    selector: 'sas-upload',
    templateUrl: './upload.component.html',
    styleUrls: ['./upload.component.scss']
})
export class UploadComponent implements OnDestroy, OnInit {
    content: File;
    newCorpusName: string;

    fileName: string;
    faUpload = faUpload;

    uploading: boolean;

    corpora: Corpus[];
    selectedCorpus: Corpus;

    constructor(private router: Router, private corpusService: CorpusService, private uploadFileService: UploadFileService) { }

    ngOnInit() {
        this.corpusService.list()
            .then(response => { this.corpora = response; });
    }

    ngOnDestroy() {
    }

    fileChange(fileInput: HTMLInputElement) {
        this.content = fileInput.files[0];
        this.fileName = this.content.name;
    }

    fullyFilled() {
        return (this.newCorpusName || this.selectedCorpus) && this.content;
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
                    this.router.navigate([`/process/${response.corpus_id}`]);
                },
                error => {
                    this.uploading = false;
                    console.log(error);
                }
            );

    }
}
