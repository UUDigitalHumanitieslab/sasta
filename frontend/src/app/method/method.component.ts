import { Component, OnInit } from '@angular/core';
import { MethodService } from '../services/method.service';
import { ActivatedRoute } from '@angular/router';
import { Method } from '../models/method';
import { faCheck, faSearch } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'sas-method',
  templateUrl: './method.component.html',
  styleUrls: ['./method.component.scss']
})
export class MethodComponent implements OnInit {
  id: number;
  method: Method;
  faCheck = faCheck;
  faSearch = faSearch;
  constructor(private methodService: MethodService, private route: ActivatedRoute) {
    this.route.paramMap.subscribe(params => this.id = +params.get('id'));
  }

  ngOnInit() {
    this.methodService
      .get_by_id(this.id)
      .subscribe(res => {
        this.method = res
        console.log(res);
      }
      );
  }

}
