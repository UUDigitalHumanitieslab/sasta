import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ListMethodComponent } from './list-method.component';
import { MethodComponent } from './method.component';
import { SharedModule } from '../shared/shared.module';
import { MethodRoutingModule } from './method-routing.module';

@NgModule({
    declarations: [ListMethodComponent, MethodComponent],
    imports: [CommonModule, MethodRoutingModule, SharedModule],
    exports: [ListMethodComponent, MethodComponent],
})
export class MethodModule {}
