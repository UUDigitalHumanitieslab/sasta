import { Component, OnInit } from '@angular/core';
import { MethodService } from '../services/method.service'
import { Method } from '../models/method';


@Component({
  selector: 'sas-list-method',
  templateUrl: './list-method.component.html',
  styleUrls: ['./list-method.component.scss']
})
export class ListMethodComponent implements OnInit {
  methods: Method[];

  constructor(private methodService: MethodService) { }

  ngOnInit() {
    this.methodService
      .list()
      .subscribe(res => this.methods = res);
  }

}
