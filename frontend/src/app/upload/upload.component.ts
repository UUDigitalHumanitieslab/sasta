import { Component, OnInit } from '@angular/core';
import { faUpload } from '@fortawesome/free-solid-svg-icons';
@Component({
    selector: 'sas-upload',
    templateUrl: './upload.component.html',
    styleUrls: ['./upload.component.scss']
})
export class UploadComponent implements OnInit {
    fileName: string;
    faUpload = faUpload;

    constructor() { }

    ngOnInit() {
    }

    fileChange(fileInput: HTMLInputElement) {
        this.fileName = fileInput.files[0].name;
    }
}
