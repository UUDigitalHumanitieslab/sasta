import { Component, Input, OnInit } from '@angular/core';
import { Transcript, TranscriptStatus } from '../models/transcript';

@Component({
  selector: '[sas-transcript-progress]',
  templateUrl: './transcript-progress.component.html',
  styleUrls: ['./transcript-progress.component.scss']
})
export class TranscriptProgressComponent implements OnInit {
  @Input() transcript: Transcript;

  constructor() { }

  ngOnInit() {
  }

  parseProgress(): number {
    if (this.transcript.status < 5) {
      return 0;
    }
    switch (this.transcript.status) {
      case TranscriptStatus.PARSING_FAILED:
        return -1;
      case TranscriptStatus.PARSING:
        return 1;
      case TranscriptStatus.PARSED:
        return 2;
    }
  }

  convertProgress(): number {
    if (this.transcript.status > 4) {
      return 2;
    }
    switch (this.transcript.status) {
      case TranscriptStatus.CONVERSION_FAILED:
        return -1;
      case TranscriptStatus.CREATED:
        return 0;
      case TranscriptStatus.CONVERTING:
        return 1;
      case TranscriptStatus.CONVERTED:
        return 2;
    }
  }

}
