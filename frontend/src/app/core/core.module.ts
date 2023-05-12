import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MenuComponent } from './menu/menu.component';
import { HomeComponent } from './home/home.component';
import { FooterComponent } from './footer/footer.component';
import { SharedModule } from '../shared/shared.module';

@NgModule({
    declarations: [MenuComponent, HomeComponent, FooterComponent],
    imports: [CommonModule, SharedModule],
    exports: [MenuComponent, HomeComponent, FooterComponent],
})
export class CoreModule {}
