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
  interval$: Observable<number>;
  corpora: Corpus[];

  constructor(private corpusService: CorpusService) { }

  ngOnInit() {
    this.interval$ = interval(UPDATE_INTERVAL);
    this.subscription$ = this.interval$
      .pipe(
        startWith(0),
        flatMap(() => this.corpusService.list())
      )
      .subscribe(
        res => {
          this.corpora = res;
        },
        err => console.error(err)
      );
  }

  ngOnDestroy() {
    this.subscription$.unsubscribe();
  }

}
