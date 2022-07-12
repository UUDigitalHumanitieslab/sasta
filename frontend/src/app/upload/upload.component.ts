import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { faUpload } from '@fortawesome/free-solid-svg-icons';
import * as _ from 'lodash';
import { FileUpload } from 'primeng/fileupload';
import { forkJoin, Observable } from 'rxjs';
import { concatMap, switchMap } from 'rxjs/operators';
import { Corpus } from '../models/corpus';
import { MethodCategory } from '../models/methodcategory';
import { UploadFile } from '../models/upload-file';
import { CorpusService } from '../services/corpus.service';
import { MethodService } from '../services/method.service';
import { UploadFileService } from '../services/upload-file.service';

@Component({
    selector: 'sas-upload',
    templateUrl: './upload.component.html',
    styleUrls: ['./upload.component.scss'],
})
export class UploadComponent implements OnInit {
    @ViewChild('fileInput') fileInput: FileUpload;

    files: File[];
    fileAccept =
        '.cha,.txt,.docx,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,.zip,application/zip,application/x-zip-compressed,multipart/x-zip';

    newCorpusName: string;

    faUpload = faUpload;

    uploading: boolean;

    corpora: Corpus[];
    selectedCorpus: Corpus;

    categories: MethodCategory[];
    selectedCategory: MethodCategory;

    _: any = _;

    constructor(
        private router: Router,
        private corpusService: CorpusService,
        private uploadFileService: UploadFileService,
        private methodService: MethodService,
        private route: ActivatedRoute
    ) {}

    ngOnInit() {
        this.corpusService.list().subscribe((res) => {
            this.corpora = res;
        });

        this.corpusService
            .list()
            .pipe(
                switchMap((response: Corpus[]) => {
                    this.corpora = response;
                    return this.route.queryParams;
                })
            )
            .subscribe((params: Params) => {
                if (params.corpus) {
                    this.selectedCorpus = this.corpora.find(
                        (c) => c.id === +params.corpus
                    );
                    this.onSelectCorpus();
                }
            });
        this.methodService.listCategories().subscribe((res) => {
            this.categories = res;
        });
    }

    fullyFilled() {
        return (
            (this.newCorpusName || this.selectedCorpus) &&
            this.selectedCategory &&
            !this.corpusNameInUse() &&
            this.fileInput.files.length > 0
        );
    }

    onSelectCorpus() {
        if (this.selectedCorpus) {
            this.selectedCategory = this.categories.find(
                (c) => c.id === this.selectedCorpus.method_category
            );
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
            method_category: this.selectedCategory.id,
        };
        return this.corpusService.create(newCorpus);
    }

    onUpload(event) {
        // Triggered by PrimeNG file upload component
        this.files = event.files;
    }

    upload$(toCorpus: Corpus, file: File) {
        const newUploadFile: UploadFile = {
            name: file.name,
            content: file,
            status: 'uploading',
            corpus: toCorpus,
        };
        return this.uploadFileService.upload(newUploadFile);
    }

    uploadFiles$(toCorpus: Corpus) {
        const uploadFiles: UploadFile[] = this.files.map((f: File) => {
            return {
                name: f.name,
                content: f,
                status: 'uploading',
                corpus: toCorpus,
            };
        });
        return forkJoin(
            uploadFiles.map((file) => this.uploadFileService.upload(file))
        );
    }

    startUpload() {
        this.uploading = true;
        let uploadSteps$: Observable<any>;

        this.fileInput.upload();

        if (!this.selectedCorpus && this.newCorpusName) {
            uploadSteps$ = this.createCorpus$().pipe(
                concatMap((corpus) => this.uploadFiles$(corpus))
            );
        } else {
            uploadSteps$ = this.uploadFiles$(this.selectedCorpus);
        }

        uploadSteps$.subscribe(
            (response) => {
                this.uploading = false;
                this.router.navigate([`/process/${response[0].corpus}`]);
            },
            (error) => {
                console.error(error);
                this.uploading = false;
            }
        );
    }
}
