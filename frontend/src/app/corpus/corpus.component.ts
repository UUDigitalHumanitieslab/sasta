import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { faCogs, faDownload, faPlus, faTrash } from '@fortawesome/free-solid-svg-icons';
import { saveAs } from 'file-saver';
import * as _ from 'lodash';
import { MessageService, SelectItemGroup } from 'primeng/api';
import { interval, Observable } from 'rxjs';
import { startWith, switchMap } from 'rxjs/operators';
import { Corpus } from '../models/corpus';
import { Method } from '../models/method';
import { Transcript } from '../models/transcript';
import { CorpusService } from '../services/corpus.service';
import { MethodService } from '../services/method.service';
import { TranscriptService } from '../services/transcript.service';

@Component({
    selector: 'sas-corpus',
    templateUrl: './corpus.component.html',
    styleUrls: ['./corpus.component.scss'],
})
export class CorpusComponent implements OnInit, OnDestroy {
    _: any = _; // Lodash

    id: number;
    corpus: Corpus;

    tams: Method[];
    defaultTam: Method;
    groupedTams: SelectItemGroup[];

    faDownload = faDownload;
    faTrash = faTrash;
    faCogs = faCogs;
    faPlus = faPlus;

    interval$: Observable<number> = interval(5000);

    constructor(
        private corpusService: CorpusService,
        private transcriptService: TranscriptService,
        private methodService: MethodService,
        private route: ActivatedRoute,
        private messageService: MessageService
    ) {
        this.route.paramMap.subscribe(
            (params) => (this.id = +params.get('id'))
        );
    }

    ngOnInit() {
        this.methodService
            .list()
            .pipe(
                switchMap((methods) => {
                    this.tams = methods;
                    return this.corpusService.get_by_id(this.id);
                }),
                switchMap((c: Corpus) => {
                    this.groupedTams = this.methodService.groupMethods(
                        this.tams,
                        c.method_category
                    );
                    return this.interval$;
                }),
                startWith(0)
            )
            .subscribe(() => {
                this.getCorpus();
            });
    }

    ngOnDestroy() {}

    getCorpus() {
        this.corpusService.get_by_id(this.id).subscribe((res) => {
            this.corpus = res;
            // retrieve default method
            if (res.default_method) {
                this.methodService
                    .get_by_id(res.default_method)
                    .subscribe((tam) => (this.defaultTam = tam));
            }
        });
    }

    downloadFile(data: any, filename: string, mimetype: string) {
        const blob = new Blob([data], { type: mimetype });
        saveAs(blob, filename);
    }

    deleteTranscript(transcript: Transcript) {
        this.transcriptService.delete(transcript.id).subscribe(
            () => {
                this.getCorpus();
                this.messageService.add({
                    severity: 'success',
                    summary: 'Removed transcript',
                    detail: '',
                });
            },
            (err) => {
                console.log(err);
                this.messageService.add({
                    severity: 'error',
                    summary: 'Error removing transcript',
                    detail: err.message,
                    sticky: true,
                });
            }
        );
    }

    changeDefaultMethod() {
        this.corpusService
            .set_default_method(
                this.corpus.id,
                this.defaultTam ? this.defaultTam.id : null
            )
            .subscribe(
                () => {},
                (err) => {
                    console.log(err);
                    this.messageService.add({
                        severity: 'error',
                        summary: 'Error changing default method',
                        detail: err.message,
                        sticky: true,
                    });
                }
            );
    }

    downloadZip() {
        this.corpusService.download_zip(this.corpus.id).subscribe(
            (response) => {
                this.downloadFile(
                    response.body,
                    `${this.corpus.name}.zip`,
                    'application/zip'
                );
                this.messageService.add({
                    severity: 'success',
                    summary: 'Downloaded corpus',
                    detail: '',
                });
            },
            (err) => {
                console.error(err);
                this.messageService.add({
                    severity: 'error',
                    summary: 'Error downloading',
                    detail: err.message,
                    sticky: true,
                });
            }
        );
    }
}
