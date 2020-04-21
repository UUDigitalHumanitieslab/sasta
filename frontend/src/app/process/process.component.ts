import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'sas-process',
  templateUrl: './process.component.html',
  styleUrls: ['./process.component.scss']
})
export class ProcessComponent implements OnInit {
  extractProgress: number;
  docxConvertProgress: number;
  chatConvertProgress: number;
  parseProgress: number;


  constructor() { }

  ngOnInit() {
    this.extractProgress = 0;
    this.docxConvertProgress = 0;
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  go() {
    this.extractProgress += 1;
    this.docxConvertProgress += 1;
  }



}
