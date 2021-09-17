import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { faUpload } from '@fortawesome/free-solid-svg-icons';
import * as _ from 'lodash';
import { Observable } from 'rxjs';
import { concatMap } from 'rxjs/operators';
import { Corpus } from '../models/corpus';
import { MethodCategory } from '../models/methodcategory';
import { UploadFile } from '../models/upload-file';
import { CorpusService } from '../services/corpus.service';
import { MethodService } from '../services/method.service';
import { UploadFileService } from '../services/upload-file.service';


@Component({
    selector: 'sas-upload',
    templateUrl: './upload.component.html',
    styleUrls: ['./upload.component.scss']
})
export class UploadComponent implements OnInit {
    content: File;
    newCorpusName: string;

    fileName: string;
    faUpload = faUpload;

    uploading: boolean;

    corpora: Corpus[];
    selectedCorpus: Corpus;

    categories: MethodCategory[];
    selectedCategory: MethodCategory;

    _: any = _;

    constructor(
        private router: Router, private corpusService: CorpusService,
        private uploadFileService: UploadFileService, private methodService: MethodService) { }

    ngOnInit() {
        this.corpusService.list()
            .subscribe(res => this.corpora = res);
        this.methodService.listCategories()
            .subscribe(res => {
                this.categories = res;
            });
    }

    fileChange(fileInput: HTMLInputElement) {
        this.content = fileInput.files[0];
        this.fileName = this.content.name;
    }

    fullyFilled() {
        return (this.newCorpusName || this.selectedCorpus) && this.content && this.selectedCategory && !this.corpusNameInUse();
    }

    onSelectCorpus() {
        if (this.selectedCorpus) {
            this.selectedCategory = this.categories.find(c => c.id === this.selectedCorpus.method_category);
            this.newCorpusName = undefined;
        } else {
            this.selectedCategory = undefined;
        }

    }

    corpusNameInUse() {
        return _.some(this.corpora, ['name', this.newCorpusName]);
    }

    createCorpus$() {
        const newCorpus: Corpus = {
            name: this.newCorpusName,
            status: 'created',
            method_category: this.selectedCategory.id
        };
        return this.corpusService.create(newCorpus);
    }

    upload$(toCorpus: Corpus) {
        const newUploadFile: UploadFile = {
            name: this.fileName,
            content: this.content,
            status: 'uploading',
            corpus: toCorpus
        };
        return this.uploadFileService.upload(newUploadFile);
    }

    startUpload() {
        this.uploading = true;
        let uploadSteps$: Observable<any>;

        // If a new corpus is defined, first create it
        if (!this.selectedCorpus) {
            uploadSteps$ = this.createCorpus$()
                .pipe(
                    concatMap(corpus => this.upload$(corpus)));
        } else {
            uploadSteps$ = this.upload$(this.selectedCorpus);
        }

        uploadSteps$.subscribe(
            response => {
                this.uploading = false;
                this.router.navigate([`/process/${response.corpus}`]);
            },
            error => {
                console.error(error);
                this.uploading = false;
            }
        );
    }
}
