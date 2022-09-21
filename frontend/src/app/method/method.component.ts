import { Component, OnInit } from '@angular/core';
import { MethodService } from '../services/method.service';
import { ActivatedRoute } from '@angular/router';
import { Method } from '../models/method';
import { faCheck, faSearch } from '@fortawesome/free-solid-svg-icons';
import { Query } from '@angular/compiler/src/core';

import * as _ from 'lodash';
import { Observable } from 'rxjs';

@Component({
    selector: 'sas-method',
    templateUrl: './method.component.html',
    styleUrls: ['./method.component.scss'],
})
export class MethodComponent implements OnInit {
    id: number;
    method$: Observable<Method>;
    selectedQuery: any;
    showDialog = false;
    _: any = _; // Lodash

    faCheck = faCheck;
    faSearch = faSearch;
    constructor(
        private methodService: MethodService,
        private route: ActivatedRoute
    ) {
        this.route.paramMap.subscribe(
            (params) => (this.id = +params.get('id'))
        );
    }

    ngOnInit() {
        this.method$ = this.methodService.getMethod(this.id);
    }

    showQuery(query: Query) {
        this.selectedQuery = query;
        this.showDialog = true;
    }
}
