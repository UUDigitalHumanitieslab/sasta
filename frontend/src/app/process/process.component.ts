import { Component, OnInit } from '@angular/core';
import { MenuItem } from 'primeng/api';
import { Transcript } from '../models/transcript';

@Component({
  selector: 'sas-process',
  templateUrl: './process.component.html',
  styleUrls: ['./process.component.scss']
})
export class ProcessComponent implements OnInit {

  stepsItems: MenuItem[] = [
    { label: 'Convert .docx' },
    { label: 'Convert to CHAT' },
    { label: 'Parse' },
    { label: 'Done' }
  ]
  stepsIndex: number = 0;

  constructor() { }

  ngOnInit() {
    // this.curProgress = 0;
    // this.curMax = 4;
  }

  docxToTxt() {
    // Converts .docx input
    // Returns ??
  }

  txtToChat() {
    // Converts to CHAT
    // Returns transcript
  }

  parse() {
    // Parses with Alpino
    // Returns transcript (including parse)
  }

}
