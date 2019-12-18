import { Component, OnInit, Input } from '@angular/core';
import { Corpus } from '../models/corpus';
import { CorpusService } from '../services/corpus.service';
import { ActivatedRoute } from '@angular/router';
import { faFileCode, faFileExport, faCogs, faCalculator } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'sas-corpus',
  templateUrl: './corpus.component.html',
  styleUrls: ['./corpus.component.scss']
})
export class CorpusComponent implements OnInit {
  id: number;
  corpus: Corpus;
  faFileCode = faFileCode;
  faFileExport = faFileExport;
  faCogs = faCogs;
  faCalculator = faCalculator;

  constructor(private corpusService: CorpusService, private route: ActivatedRoute) {
    this.route.paramMap.subscribe(params => this.id = +params.get('id'));
  }

  ngOnInit() {
    this.corpusService
      .get_by_id(this.id)
      .subscribe(res => this.corpus = res);
  }

}
