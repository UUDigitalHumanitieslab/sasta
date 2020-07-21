import { Component, OnInit } from '@angular/core';
import { MenuItem } from 'primeng/api';
import { Corpus } from '../models/corpus';
import { Router, ActivatedRoute } from '@angular/router';
import { CorpusService } from '../services/corpus.service';
import { concat } from 'rxjs/operators';

@Component({
  selector: 'sas-process',
  templateUrl: './process.component.html',
  styleUrls: ['./process.component.scss']
})
export class ProcessComponent implements OnInit {
  corpus: Corpus;
  id: number;

  stepsItems: MenuItem[] = [
    { label: 'Convert to CHAT' },
    { label: 'Parse' },
    { label: 'Done' }
  ];
  stepsIndex: number;
  processing = false;

  constructor(private route: ActivatedRoute, private corpusService: CorpusService, private router: Router) {
    this.route.paramMap.subscribe(params => this.id = +params.get('id'));
  }

  ngOnInit() {
    this.corpusService
      .get_by_id(this.id)
      .subscribe(
        res => {
          this.corpus = res;
        },
        err => console.log(err));
  }

  async full_process() {
    this.processing = true;
    this.stepsIndex = 0;
    this.corpusService.convert_all(this.corpus.id)
      .pipe(
        // tslint:disable-next-line: deprecation
        concat(this.corpusService.parse_all(this.corpus.id)))
      .subscribe(
        res => {
          console.log(res.transcripts);
          this.stepsIndex += 1;
        },
        err => {
          console.log(err);
          this.stepsIndex += 1;
        },
        () => {
          this.processing = false;
          this.router.navigate([`/corpora/${this.corpus.id}`]);
        }
      );

  }

}

