import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { faCalculator, faCogs, faFile, faFileCode, faFileExport } from '@fortawesome/free-solid-svg-icons';
import { saveAs } from 'file-saver';
import { MessageService } from 'primeng/api';
import { Dialog } from 'primeng/dialog';
import { Corpus } from '../models/corpus';
import { Method } from '../models/method';
import { Transcript } from '../models/transcript';
import { CorpusService } from '../services/corpus.service';
import { MethodService } from '../services/method.service';




@Component({
  selector: 'sas-corpus',
  templateUrl: './corpus.component.html',
  styleUrls: ['./corpus.component.scss'],
})
export class CorpusComponent implements OnInit {
  @ViewChild(Dialog, { static: false }) dialog;

  id: number;
  corpus: Corpus;

  tams: Method[];
  currentTam: Method;

  faFile = faFile;
  faFileCode = faFileCode;
  faFileExport = faFileExport;
  faCogs = faCogs;
  faCalculator = faCalculator;


  displayScore: boolean = false;
  currentTranscript: Transcript;
  queryAction: "annotate" | "query";
  onlyInform: boolean = true;
  querying: boolean = false;

  constructor(private corpusService: CorpusService, private methodService: MethodService, private route: ActivatedRoute, private messageService: MessageService) {
    this.route.paramMap.subscribe(params => this.id = +params.get('id'));
  }

  ngOnInit() {
    this.corpusService
      .get_by_id(this.id)
      .subscribe(res => this.corpus = res);

    this.methodService
      .list()
      .subscribe(res => this.tams = res);
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
    const blob = new Blob([data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    saveAs(blob, filename);
  }

  performQuerying(transcript: Transcript, method: Method) {
    if (this.queryAction == 'annotate') {
      this.annotateTranscript(transcript, method);
    }
    if (this.queryAction == 'query') {
      this.queryTranscript(transcript, method);
    }
  }

  annotateTranscript(transcript: Transcript, method: Method) {
    this.querying = true;
    this.corpusService
      .annotate_transcript(transcript.id, method.name, this.onlyInform)
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
      .score_transcript(transcript.id, method.name)
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
}
