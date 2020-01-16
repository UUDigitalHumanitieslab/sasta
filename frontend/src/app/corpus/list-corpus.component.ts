import { Component, OnInit } from '@angular/core';
import { Store, select, State } from '@ngrx/store';
import { Subscription, interval } from 'rxjs';
import { storeStructure } from '../store';
import { Corpus } from '../models/corpus';
import { refreshList } from '../store/corpus.actions';
import { startWith } from 'rxjs/operators';

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

  constructor(private store: Store<storeStructure>) {
    this.subscriptions = [
      this.store.pipe(select('corpora')).subscribe((corpora: Corpus[]) => {
        this.corpora = corpora;
      }),
      interval(UPDATE_INTERVAL).pipe(startWith(0)).subscribe(() => {
        store.dispatch(refreshList({}));
      })
    ];
  }



  ngOnInit() {
  }

}
