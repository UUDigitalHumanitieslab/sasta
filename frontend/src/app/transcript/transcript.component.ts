import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import {
    faArrowLeft,
    faDownload,
    faFile,
    faFileCode,
    faTrash,
    faUpload,
} from '@fortawesome/free-solid-svg-icons';
import { saveAs } from 'file-saver';
import * as _ from 'lodash';
import { MessageService, SelectItemGroup } from 'primeng/api';
import { Subject } from 'rxjs';
import { switchMap, takeUntil } from 'rxjs/operators';
import { Corpus } from '../models/corpus';
import { Method } from '../models/method';
import { Transcript, TranscriptStatus } from '../models/transcript';
import {
    AnalysisService,
    AnnotationOutputFormat,
} from '../services/analysis.service';
import { AuthService } from '../services/auth.service';
import { CorpusService } from '../services/corpus.service';
import { MethodService } from '../services/method.service';
import { TranscriptService } from '../services/transcript.service';

const XLSX_MIME =
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
const TXT_MIME = 'text/plain';

@Component({
    selector: 'sas-transcript',
    templateUrl: './transcript.component.html',
    styleUrls: ['./transcript.component.scss'],
})
export class TranscriptComponent implements OnInit, OnDestroy {
    _: any = _; // Lodash

    id: number;
    transcript: Transcript;
    corpus: Corpus;

    tams: Method[];
    currentTam: Method;
    groupedTams: SelectItemGroup[];

    faTrash = faTrash;
    faFile = faFile;
    faFileCode = faFileCode;
    faArrowLeft = faArrowLeft;
    faDownload = faDownload;
    faUpload = faUpload;

    querying = false;

    displayCorrUpload = false;

    onDestroy$ = new Subject<boolean>();

    readonly TranscriptStatus = TranscriptStatus;

    constructor(
        private transcriptService: TranscriptService,
        private corpusService: CorpusService,
        private methodService: MethodService,
        private analysisService: AnalysisService,
        private router: Router,
        private route: ActivatedRoute,
        private messageService: MessageService,
        public authService: AuthService
    ) {
        this.route.paramMap.subscribe(
            (params) => (this.id = +params.get('id'))
        );
    }

    allowCorrectionUpload() {
        return (
            this.transcript.status === TranscriptStatus.PARSED &&
            this.transcript.latest_run
        );
    }

    allowCorrectionReset() {
        return this.transcript.latest_run;
    }

    allowScoring() {
        return this.transcript.status === TranscriptStatus.PARSED;
    }

    ngOnInit() {
        this.loadData();
    }

    ngOnDestroy() {
        this.onDestroy$.next();
    }

    loadData() {
        this.transcriptService
            .get_by_id(this.id)
            .pipe(
                takeUntil(this.onDestroy$),
                // get transcript
                switchMap((t: Transcript) => {
                    this.transcript = t;
                    return this.corpusService.get_by_id(t.corpus); // get corpus
                }),
                switchMap((c: Corpus) => {
                    this.corpus = c;
                    return this.methodService.get_by_id(c.default_method); // get default method
                }),
                switchMap((m: Method) => {
                    this.currentTam = m;
                    return this.methodService.list(); // get all methods
                })
            )
            .subscribe((tams: Method[]) => {
                this.tams = tams;
                this.groupedTams = this.methodService.groupMethods(
                    tams,
                    this.corpus.method_category
                ); // group methods
            });
    }

    downloadFile(data: any, filename: string, mimetype: string) {
        const blob = new Blob([data], { type: mimetype });
        saveAs(blob, filename);
    }

    downloadLatestAnnotations() {
        this.transcriptService
            .latest_annotations(this.id)
            .pipe(takeUntil(this.onDestroy$))
            .subscribe((res) => {
                this.downloadFile(
                    res.body,
                    `${this.transcript.name}_latest_SAF.xlsx`,
                    XLSX_MIME
                );
            });
    }

    resetAnnotations() {
        this.transcriptService
            .reset_annotations(this.id)
            .pipe(takeUntil(this.onDestroy$))
            .subscribe(() => this.loadData());
    }

    annotateTranscript(outputFormat: AnnotationOutputFormat) {
        this.querying = true;
        this.analysisService
            .annotate(this.id, this.currentTam.id, outputFormat)
            .pipe(takeUntil(this.onDestroy$))
            .subscribe(
                (response) => {
                    switch (outputFormat) {
                        case 'xlsx':
                            this.downloadFile(
                                response.body,
                                `${this.transcript.name}_SAF.xlsx`,
                                XLSX_MIME
                            );
                            break;
                        case 'cha':
                            this.downloadFile(
                                response.body,
                                `${this.transcript.name}_annotated.cha`,
                                TXT_MIME
                            );
                            break;
                        default:
                            break;
                    }
                    this.messageService.add({
                        severity: 'success',
                        summary: 'Annotation success',
                        detail: '',
                    });
                    this.querying = false;
                    this.loadData();
                },
                (err) => {
                    console.log(err);
                    this.messageService.add({
                        severity: 'error',
                        summary: 'Error querying',
                        detail: err.message,
                        sticky: true,
                    });
                    this.querying = false;
                }
            );
    }

    queryTranscript() {
        this.querying = true;
        this.analysisService
            .query(this.id, this.currentTam.id)
            .pipe(takeUntil(this.onDestroy$))
            .subscribe(
                (response) => {
                    this.downloadFile(
                        response.body,
                        `${this.transcript.name}_matches.xlsx`,
                        XLSX_MIME
                    );
                    this.messageService.add({
                        severity: 'success',
                        summary: 'Querying success',
                        detail: '',
                    });
                    this.querying = false;
                },
                (err) => {
                    console.log(err);
                    this.messageService.add({
                        severity: 'error',
                        summary: 'Error querying',
                        detail: err.message,
                        sticky: true,
                    });
                    this.querying = false;
                }
            );
    }

    generateForm() {
        this.querying = true;
        this.analysisService
            .generateForm(this.id, this.currentTam.id)
            .pipe(takeUntil(this.onDestroy$))
            .subscribe(
                (response) => {
                    this.downloadFile(
                        response.body,
                        `${this.transcript.name}_${this.currentTam.category.name}_form.xlsx`,
                        XLSX_MIME
                    );
                    this.messageService.add({
                        severity: 'success',
                        summary: 'Generated form',
                        detail: '',
                    });
                    this.querying = false;
                },
                (err) => {
                    console.log(err);
                    this.messageService.add({
                        severity: 'error',
                        summary: 'Error generating form',
                        detail: err.message,
                        sticky: true,
                    });
                    this.querying = false;
                }
            );
    }

    deleteTranscript() {
        const corpusId = this.corpus.id;
        this.transcriptService
            .delete(this.id)
            .pipe(takeUntil(this.onDestroy$))
            .subscribe(
                () => {
                    this.router.navigate([`/corpora/${corpusId}`]);
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

    chatFileAvailable(transcript): boolean {
        return [TranscriptStatus.CONVERTED, TranscriptStatus.PARSED].includes(
            transcript.status
        );
    }

    lassyFileAvailable(transcript): boolean {
        return transcript.status === TranscriptStatus.PARSED;
    }

    showChat() {
        window.open(this.transcript.content, '_blank');
    }

    showLassy() {
        window.open(this.transcript.parsed_content, '_blank');
    }

    showCorrectedLassy() {
        window.open(this.transcript.corrected_content, '_blank');
    }

    showCorrectionsUpload() {
        this.displayCorrUpload = true;
    }

    onCorrectionsUploadClose(event) {
        this.displayCorrUpload = event;
        this.loadData();
    }

    numUtterancesAnalysed() {
        // Count the number of utterances that will be analysed
        // Uses reduce to efficiently find the number
        return this.transcript.utterances.reduce(
            (total, utt) => (utt.for_analysis ? ++total : total),
            0
        );
    }
}
