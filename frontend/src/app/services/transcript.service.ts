import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Transcript } from '../models/transcript';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TranscriptService {

  constructor(private httpClient: HttpClient) { }

  docxToTxt() {
    return null
  }

  txtToCHAT(): Observable<Transcript> {

  }

  parse(transcript: Transcript): Observable<Transcript> {

  }




}
