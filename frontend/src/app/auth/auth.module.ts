import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './login.component';
import { RegisterComponent } from './register.component';
import { VerifyComponent } from './verify.component';
import { SharedModule } from '../shared/shared.module';

@NgModule({
    declarations: [LoginComponent, RegisterComponent, VerifyComponent],
    imports: [CommonModule, SharedModule],
    exports: [LoginComponent, RegisterComponent, VerifyComponent],
})
export class AuthModule {}
