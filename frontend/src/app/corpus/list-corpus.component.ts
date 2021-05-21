import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { Corpus } from '../models/corpus';
import { CorpusService } from '../services/corpus.service';

// check every 10 seconds
const UPDATE_INTERVAL = 10000;

@Component({
  selector: 'sas-list-corpus',
  templateUrl: './list-corpus.component.html',
  styleUrls: ['./list-corpus.component.scss']
})
export class ListCorpusComponent implements OnInit {
  subscriptions: Subscription[];
  corpora: Corpus[];

  constructor(private corpusService: CorpusService) {
  }

  ngOnInit() {
    this.corpusService
      .list_obs()
      .subscribe(
        res => this.corpora = res,
        err => console.log(err)
      );
  }

}
