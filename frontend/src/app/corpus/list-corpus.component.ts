import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription, interval, Observable } from 'rxjs';
import { flatMap, startWith } from 'rxjs/operators';
import { Corpus } from '../models/corpus';
import { CorpusService } from '../services/corpus.service';

// check every 10 seconds
const UPDATE_INTERVAL = 10000;

@Component({
  selector: 'sas-list-corpus',
  templateUrl: './list-corpus.component.html',
  styleUrls: ['./list-corpus.component.scss']
})
export class ListCorpusComponent implements OnInit, OnDestroy {
  private subscription$: Subscription;
  interval$: Observable<number> = interval(UPDATE_INTERVAL);
  corpora: Corpus[];

  constructor(private corpusService: CorpusService) { }

  ngOnDestroy() {
    this.subscription$.unsubscribe();
  }

  ngOnInit() {
    this.corpusService.corpora$.subscribe(res => this.corpora = res);
    this.subscription$ = this.interval$
      .pipe(startWith(0))
      .subscribe(() => this.refreshCorpora());
  }

  refreshCorpora() {
    this.corpusService.updateCorpora();
  }

}
