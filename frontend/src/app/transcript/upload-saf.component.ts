import { Component, EventEmitter, Input, OnDestroy, OnInit, Output } from '@angular/core';
import { Transcript } from '../models/transcript';

@Component({
  selector: 'sas-upload-saf',
  templateUrl: './upload-saf.component.html',
  styleUrls: ['./upload-saf.component.scss']
})
export class UploadSafComponent implements OnInit, OnDestroy {

  @Input() transcript: Transcript;
  @Input() display: boolean;

  @Output() displayChange = new EventEmitter();

  constructor() { }

  ngOnInit() {
  }

  ngOnDestroy() {
    this.displayChange.unsubscribe();
  }

  onClose() {
    this.displayChange.emit(false);
  }

}
