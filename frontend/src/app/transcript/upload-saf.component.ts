import { Component, EventEmitter, Input, OnDestroy, OnInit, Output } from '@angular/core';
import { Transcript } from '../models/transcript';
import { faUpload } from '@fortawesome/free-solid-svg-icons';
import { TranscriptService } from '../services/transcript.service';
import { MessageService } from 'primeng/api';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'sas-upload-saf',
  templateUrl: './upload-saf.component.html',
  styleUrls: ['./upload-saf.component.scss']
})
export class UploadSafComponent implements OnInit, OnDestroy {

  @Input() transcript: Transcript;
  @Input() display: boolean;

  @Output() displayChange = new EventEmitter();

  content: File;
  fileName: string;
  uploading: boolean;
  faUpload = faUpload;

  parseErrors: string[];

  constructor(private transcriptService: TranscriptService, private messageService: MessageService) { }

  ngOnInit() {
  }

  ngOnDestroy() {
    this.displayChange.unsubscribe();
  }

  onClose() {
    this.parseErrors = null;
    this.displayChange.emit(false);
  }

  header() {
    return `Upload corrections for ${this.transcript.name}`;
  }

  onFileChange(fileInput: HTMLInputElement) {
    this.parseErrors = null;
    this.content = fileInput.files[0];
    this.fileName = this.content.name;
  }

  upload() {
    this.parseErrors = null;
    this.uploading = true;
    this.transcriptService
      .upload_annotations(this.fileName, this.content, this.transcript)
      .subscribe(
        () => {
          this.uploading = false;
          this.messageService.add({
            severity: 'success',
            summary: `Annotations uploaded for ${this.transcript.name}`,
          });
        },
        error => this.handleErrors(error)
      );
  }

  handleErrors(httpError: HttpErrorResponse) {
    this.uploading = false;
    if (Array.isArray(httpError.error)) {
      this.parseErrors = httpError.error;
    } else {
      this.parseErrors = [httpError.error];
    }
  }

}
