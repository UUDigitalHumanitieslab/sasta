import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { faDownload, faTrash } from '@fortawesome/free-solid-svg-icons';
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
import { interval, Observable, Subscription } from 'rxjs';
import { startWith } from 'rxjs/operators';

@Component({
  selector: 'sas-corpus',
  templateUrl: './corpus.component.html',
  styleUrls: ['./corpus.component.scss'],
})
export class CorpusComponent implements OnInit, OnDestroy {
  @ViewChild(Dialog, { static: false }) dialog;

  _: any = _; // Lodash

  id: number;
  corpus: Corpus;

  tams: Method[];
  defaultTam: Method;
  groupedTams: SelectItemGroup[];

  faDownload = faDownload;
  faTrash = faTrash;

  interval$: Observable<number> = interval(5000);
  private subscription$: Subscription;

  constructor(
    private corpusService: CorpusService,
    private transcriptService: TranscriptService,
    private methodService: MethodService,
    private route: ActivatedRoute,
    private messageService: MessageService) {
    this.route.paramMap.subscribe(params => this.id = +params.get('id'));
  }

  ngOnInit() {
    this.subscription$ = this.interval$
      .pipe(startWith(0))
      .subscribe(() => this.get_corpus());


    this.methodService
      .list()
      .subscribe(res => {
        this.tams = res;
        this.groupTams(res);
      });
  }

  ngOnDestroy() {
    this.subscription$.unsubscribe();
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
      .subscribe(res => {
        this.corpus = res;
        // retrieve default method
        if (res.default_method) {
          this.methodService
            .get_by_id(res.default_method)
            .subscribe(tam => this.defaultTam = tam);
        }
      });
  }

  downloadFile(data: any, filename: string, mimetype: string) {
    const blob = new Blob([data], { type: mimetype });
    saveAs(blob, filename);
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

  changeDefaultMethod() {
    this.corpusService
      .set_default_method(this.corpus.id, this.defaultTam ? this.defaultTam.id : null)
      .subscribe(
        reponse => {},
        err => {
          console.log(err);
          this.messageService.add({severity: 'error', summary: 'Error changing default method', detail: err.message, sticky: true })
        }
      )
  }

  downloadZip() {
    this.corpusService
      .download_zip(this.corpus.id)
      .subscribe(
        response => {
          this.downloadFile(response.body, `${this.corpus.name}.zip`, 'application/zip');
          this.messageService.add({ severity: 'success', summary: 'Downloaded corpus', detail: '' });
        },
        err => {
          console.log(err);
          this.messageService.add({ severity: 'error', summary: 'Error downloading', detail: err.message, sticky: true });
        });
  }

}
