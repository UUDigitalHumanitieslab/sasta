import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { faArrowRight, faCogs } from '@fortawesome/free-solid-svg-icons';
import { MenuItem } from 'primeng/api';
import { interval, Observable, of, Subscription } from 'rxjs';
import { catchError, concatMap, startWith } from 'rxjs/operators';
import { Corpus } from '../models/corpus';
import { CorpusService } from '../services/corpus.service';
import { ParseService } from '../services/parse.service';

@Component({
    selector: 'sas-process',
    templateUrl: './process.component.html',
    styleUrls: ['./process.component.scss'],
})
export class ProcessComponent implements OnInit, OnDestroy {
    corpus: Corpus;
    id: number;

    stepsItems: MenuItem[] = [
        { label: 'Convert to CHAT' },
        { label: 'Parse' },
        { label: 'Done' },
    ];
    stepsIndex: number;
    processing = false;

    subscription$: Subscription;
    interval$: Observable<number> = interval(2000);

    faCogs = faCogs;
    faArrowRight = faArrowRight;

    constructor(
        private route: ActivatedRoute,
        private corpusService: CorpusService,
        private parseService: ParseService
    ) {
        this.route.paramMap.subscribe(
            (params) => (this.id = +params.get('id'))
        );
    }

    ngOnInit() {
        this.subscription$ = this.interval$
            .pipe(startWith(0))
            .subscribe(() => this.getCorpus());
    }

    ngOnDestroy() {
        this.subscription$.unsubscribe();
    }

    getCorpus() {
        this.corpusService.get_by_id(this.id).subscribe(
            (res) => {
                this.corpus = res;
            },
            (err) => console.log(err)
        );
    }

    async full_process() {
        this.processing = true;
        this.stepsIndex = 0;
        this.corpusService
            .convert_all(this.corpus.id)
            .pipe(
                // tslint:disable-next-line: deprecation
                // concat(this.corpusService.parse_all(this.corpus.id)))
                concatMap((_) =>
                    this.corpusService.parse_all_async(this.corpus.id)
                ),
                catchError((err) => of('error', err))
            )
            .subscribe(
                (res) => {
                    console.log(res);
                    this.stepsIndex += 1;
                },
                (err) => {
                    console.log(err);
                    this.stepsIndex += 1;
                },
                () => {
                    this.processing = false;
                    // this.router.navigate([`/corpora/${this.corpus.id}`]);
                }
            );
    }

    fullSingle(transcript) {
        this.parseService.fullProcess(transcript).subscribe(
            (next) => console.log(next),
            (err) => console.error(err)
        );
    }
}
