import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { faFile, faFileCode, faTrash, faArrowLeft, faDownload, faUpload } from '@fortawesome/free-solid-svg-icons';
import { saveAs } from 'file-saver';
import { MessageService } from 'primeng/api';
import { Transcript } from '../models/transcript';
import { Corpus } from '../models/corpus';
import { Method } from '../models/method';
import { TranscriptService } from '../services/transcript.service';
import { CorpusService } from '../services/corpus.service';
import { MethodService } from '../services/method.service';
import { SelectItemGroup } from 'primeng/api';
import * as _ from 'lodash';

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

  queryAction: 'annotate' | 'query' | 'generateForm';
  onlyInform = true;
  querying = false;

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

  ngOnInit() {
    this.get_transcript();
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

  get_transcript() {
    this.transcriptService
      .get_by_id(this.id)
      .subscribe(res => {
        this.transcript = res;
        this.get_corpus(res.corpus)
      });
  }

  get_corpus(corpus_id) {
    this.corpusService
      .get_by_id(corpus_id)
      .subscribe(res => {
        this.corpus = res;
        // retrieve default method
        if (res.default_method) {
          this.methodService
            .get_by_id(res.default_method)
            .subscribe(res => {
              this.currentTam = res
            });
          }
      })
  }

  performQuerying(method: Method) {
    switch (this.queryAction) {
      case 'annotate':
        this.annotateTranscript(method);
        break;
      case 'query':
        this.queryTranscript(method);
        break;
      case 'generateForm':
        this.generateFormTranscript(method);
        break;
      default:
        break;
    }

  }

  downloadFile(data: any, filename: string) {
    const blob = new Blob([data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    saveAs(blob, filename);
  }

  annotateTranscript(method: Method) {
    this.querying = true;
    this.corpusService
      .annotate_transcript(this.id, method.id, this.onlyInform)
      .subscribe(
        response => {
          this.downloadFile(response.body, `${this.transcript.name}_SAF.xlsx`);
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

  queryTranscript(method: Method) {
    this.querying = true;
    this.corpusService
      .query_transcript(this.id, method.id)
      .subscribe(
        response => {
          this.downloadFile(response.body, `${this.transcript.name}_matches.xlsx`);
          this.messageService.add({ severity: 'success', summary: 'Querying success', detail: '' });
          this.querying = false;
        },
        err => {
          console.log(err);
          this.messageService.add({ severity: 'error', summary: 'Error querying', detail: err.message, sticky: true });
          this.querying = false;
        });
  }

  generateFormTranscript(method: Method) {
    this.querying = true;
    this.corpusService
      .generate_form_transcript(this.id, method.id)
      .subscribe(
        response => {
          this.downloadFile(response.body, `${this.transcript.name}_${method.category.name}_form.xlsx`);
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
    var corpus_id = this.corpus.id;
    this.transcriptService
      .delete(this.id)
      .subscribe(
        () => {
          this.router.navigate([`/corpora/${corpus_id}`])
          this.messageService.add({ severity: 'success', summary: 'Removed transcript', detail: '' });
        },
        err => {
          console.log(err);
          this.messageService.add({ severity: 'error', summary: 'Error removing transcript', detail: err.message, sticky: true });
        });
  }

  chatFileAvailable(transcript) {
    return ['converted', 'parsed'].includes(transcript.status);
  }

  lassyFileAvailable(transcript) {
    return transcript.status === 'parsed';
  }
  
  showChat() {
    window.open(this.transcript.content, '_blank');
  }

  showLassy() {
    window.open(this.transcript.parsed_content, '_blank');
  }


}
