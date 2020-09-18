import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { faCalculator, faCogs, faDownload, faFile, faFileCode, faFileExport, faTrash } from '@fortawesome/free-solid-svg-icons';
import { saveAs } from 'file-saver';
import { MessageService } from 'primeng/api';
import { Dialog } from 'primeng/dialog';
import { Corpus } from '../models/corpus';
import { Method } from '../models/method';
import { Transcript } from '../models/transcript';
import { CorpusService } from '../services/corpus.service';
import { MethodService } from '../services/method.service';
import { TranscriptService } from '../services/transcript.service';
import { SelectItemGroup } from 'primeng/api';
import * as _ from 'lodash';

@Component({
  selector: 'sas-corpus',
  templateUrl: './corpus.component.html',
  styleUrls: ['./corpus.component.scss'],
})
export class CorpusComponent implements OnInit {
  @ViewChild(Dialog, { static: false }) dialog;

  _: any = _; // Lodash

  id: number;
  corpus: Corpus;

  tams: Method[];
  currentTam: Method;
  groupedTams: SelectItemGroup[];

  faFile = faFile;
  faFileCode = faFileCode;
  faFileExport = faFileExport;
  faCogs = faCogs;
  faCalculator = faCalculator;
  faDownload = faDownload;
  faTrash = faTrash;


  displayScore = false;
  currentTranscript: Transcript;
  queryAction: 'annotate' | 'query';
  onlyInform = true;
  querying = false;

  constructor(
    private corpusService: CorpusService,
    private transcriptService: TranscriptService,
    private methodService: MethodService,
    private route: ActivatedRoute,
    private messageService: MessageService) {
    this.route.paramMap.subscribe(params => this.id = +params.get('id'));
  }

  ngOnInit() {
    this.get_corpus();
    this.methodService
      .list()
      .subscribe(res => {
        this.tams = res;
        this.groupTams(res);
      });
  }

  groupTams(tams) {
    this.groupedTams = _(tams)
      .groupBy('category.name')
      .map((methods, methodCat) =>
        ({
          label: methodCat, items: _.map(methods, (m) =>
            ({ label: m.name, value: m }))
        })
      )
      .value();
  }

  get_corpus() {
    this.corpusService
      .get_by_id(this.id)
      .subscribe(res => this.corpus = res);
  }

  showChat(transcript: Transcript) {
    window.open(transcript.content, '_blank');
  }

  showLassy(transcript: Transcript) {
    window.open(transcript.parsed_content, '_blank');
  }

  showDialog(transcript: Transcript) {
    this.currentTranscript = transcript;
    this.displayScore = true;
  }

  closeDialog() {
    this.currentTranscript = null;
  }

  downloadFile(data: any, filename: string) {
    const blob = new Blob([data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    saveAs(blob, filename);
  }

  performQuerying(transcript: Transcript, method: Method) {
    if (this.queryAction === 'annotate') {
      this.annotateTranscript(transcript, method);
    }
    if (this.queryAction === 'query') {
      this.queryTranscript(transcript, method);
    }
  }

  annotateTranscript(transcript: Transcript, method: Method) {
    this.querying = true;
    this.corpusService
      .annotate_transcript(transcript.id, method.id, this.onlyInform)
      .subscribe(
        response => {
          this.downloadFile(response.body, `${transcript.name}_SAF.xlsx`);
          this.messageService.add({ severity: 'success', summary: 'Annotation success', detail: '' });
          this.querying = false;
        },
        err => {
          console.log(err);
          this.messageService.add({ severity: 'error', summary: 'Error querying', detail: err.message, sticky: true });
          this.querying = false;
        }
      );
  }

  queryTranscript(transcript: Transcript, method: Method) {
    this.querying = true;
    this.corpusService
      .score_transcript(transcript.id, method.id)
      .subscribe(
        response => {
          this.downloadFile(response.body, `${transcript.name}_matches.xlsx`);
          this.messageService.add({ severity: 'success', summary: 'Querying success', detail: '' });
          this.querying = false;
        },
        err => {
          console.log(err);
          this.messageService.add({ severity: 'error', summary: 'Error querying', detail: err.message, sticky: true });
          this.querying = false;
        });
  }

  deleteTranscript(transcript: Transcript) {
    this.transcriptService
      .delete(transcript.id)
      .subscribe(
        () => {
          this.get_corpus();
          this.messageService.add({ severity: 'success', summary: 'Removed transcript', detail: '' });
        },
        err => {
          console.log(err);
          this.messageService.add({ severity: 'error', summary: 'Error removing transcript', detail: err.message, sticky: true });
        });
  }

  downloadZip() {
    this.corpusService
      .download_zip(this.corpus.id)
      .subscribe(
        response => {
          this.downloadFile(response.body, `${this.corpus.name}.zip`);
          this.messageService.add({ severity: 'success', summary: 'Downloaded corpus', detail: '' });
        },
        err => {
          console.log(err);
          this.messageService.add({ severity: 'error', summary: 'Error downloading', detail: err.message, sticky: true });
        });
  }

}
