import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { combineLatest, Observable } from 'rxjs';
import { map, switchMap, tap } from 'rxjs/operators';
import { ManualPage, ManualService } from '../services/manual.service';

@Component({
    selector: 'sas-manual',
    templateUrl: './manual.component.html',
    styleUrls: ['./manual.component.scss'],
})
export class ManualComponent implements OnInit {
    manifest$ = this.manualService.manifest$.asObservable();

    currentPage: Observable<ManualPage>;

    constructor(
        private manualService: ManualService,
        private activatedRoute: ActivatedRoute
    ) {}

    ngOnInit(): void {
        this.currentPage = combineLatest([
            this.manifest$,
            this.activatedRoute.paramMap,
        ]).pipe(
            switchMap(([manifest, params]) => {
                const identifier = params.get('identifier');
                const meta = manifest.find((m) => m.id === identifier);
                return this.manualService.getPage(meta);
            })
        );
    }
}
