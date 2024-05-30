import { Component, OnInit } from '@angular/core';
import { ManualService } from '../services/manual.service';

@Component({
    selector: 'sas-manual-nav',
    templateUrl: './manual-nav.component.html',
    styleUrls: ['./manual-nav.component.scss'],
})
export class ManualNavComponent implements OnInit {
    manifest$ = this.manualService.manifest$.asObservable();
    constructor(private manualService: ManualService) {}

    ngOnInit(): void {}
}
