import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { faArrowLeft, faDownload, faFile, faFileCode, faTrash, faUpload } from '@fortawesome/free-solid-svg-icons';
import { saveAs } from 'file-saver';
import * as _ from 'lodash';
import { MessageService, SelectItemGroup } from 'primeng/api';
import { switchMap } from 'rxjs/operators';
import { Corpus } from '../models/corpus';
import { Method } from '../models/method';
import { Transcript, TranscriptStatus } from '../models/transcript';
import { CorpusService } from '../services/corpus.service';
import { MethodService } from '../services/method.service';
import { TranscriptService } from '../services/transcript.service';

const XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
const TXT_MIME = 'text/plain';

@Component({
  selector: 'sas-transcript',
  templateUrl: './transcript.component.html',
  styleUrls: ['./transcript.component.scss']
})
export class TranscriptComponent implements OnInit {

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

  constructor(
    private transcriptService: TranscriptService,
    private corpusService: CorpusService,
    private methodService: MethodService,
    private router: Router,
    private route: ActivatedRoute,
    private messageService: MessageService
  ) {
    this.route.paramMap.subscribe(params => this.id = +params.get('id'));
  }

  allowCorrectionUpload() {
    return this.transcript.status === TranscriptStatus.PARSED && this.transcript.latest_run;
  }

  allowCorrectionReset() {
    return this.transcript.latest_run;
  }

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.transcriptService.get_by_id(this.id).pipe( // get transcript
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
      }),
    ).subscribe(
      (tams: Method[]) => {
        this.tams = tams;
        this.groupedTams = this.methodService.groupMethods(tams, this.corpus.method_category); // group methods
      }
    );
  }

  downloadFile(data: any, filename: string, mimetype: string) {
    const blob = new Blob([data], { type: mimetype });
    saveAs(blob, filename);
  }

  downloadLatestAnnotations() {
    this.transcriptService
      .latest_annotations(this.id)
      .subscribe(
        res => {
          this.downloadFile(res.body, `${this.transcript.name}_latest_SAF.xlsx`, XLSX_MIME);
        }
      );
  }

  resetAnnotations() {
    this.transcriptService
      .reset_annotations(this.id)
      .subscribe(() => this.loadData());
  }

  annotateTranscript(outputFormat: 'xlsx' | 'cha') {
    this.querying = true;
    this.corpusService
      .annotate_transcript(this.id, this.currentTam.id, outputFormat)
      .subscribe(
        response => {
          switch (outputFormat) {
            case 'xlsx':
              this.downloadFile(response.body, `${this.transcript.name}_SAF.xlsx`, XLSX_MIME);
              break;
            case 'cha':
              this.downloadFile(response.body, `${this.transcript.name}_annotated.cha`, TXT_MIME);
              break;
            default:
              break;
          }
          this.messageService.add({ severity: 'success', summary: 'Annotation success', detail: '' });
          this.querying = false;
          this.loadData();
        },
        err => {
          console.log(err);
          this.messageService.add({ severity: 'error', summary: 'Error querying', detail: err.message, sticky: true });
          this.querying = false;
        }
      );
  }

  queryTranscript() {
    this.querying = true;
    this.corpusService
      .query_transcript(this.id, this.currentTam.id)
      .subscribe(
        response => {
          this.downloadFile(response.body, `${this.transcript.name}_matches.xlsx`, XLSX_MIME);
          this.messageService.add({ severity: 'success', summary: 'Querying success', detail: '' });
          this.querying = false;
        },
        err => {
          console.log(err);
          this.messageService.add({ severity: 'error', summary: 'Error querying', detail: err.message, sticky: true });
          this.querying = false;
        });
  }

  generateForm() {
    this.querying = true;
    this.corpusService
      .generate_form_transcript(this.id, this.currentTam.id)
      .subscribe(
        response => {
          this.downloadFile(response.body, `${this.transcript.name}_${this.currentTam.category.name}_form.xlsx`, XLSX_MIME);
          this.messageService.add({ severity: 'success', summary: 'Generated form', detail: '' });
          this.querying = false;
        },
        err => {
          console.log(err);
          this.messageService.add({ severity: 'error', summary: 'Error generating form', detail: err.message, sticky: true });
          this.querying = false;
        });
  }

  deleteTranscript() {
    const corpusId = this.corpus.id;
    this.transcriptService
      .delete(this.id)
      .subscribe(
        () => {
          this.router.navigate([`/corpora/${corpusId}`]);
          this.messageService.add({ severity: 'success', summary: 'Removed transcript', detail: '' });
        },
        err => {
          console.log(err);
          this.messageService.add({ severity: 'error', summary: 'Error removing transcript', detail: err.message, sticky: true });
        });
  }

  chatFileAvailable(transcript): boolean {
    return [TranscriptStatus.CONVERTED, TranscriptStatus.PARSED].includes(transcript.status);
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

  showCorrectionsUpload() {
    this.displayCorrUpload = true;
  }

  onCorrectionsUploadClose(event) {
    this.displayCorrUpload = event;
  }



}
