import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { EffectsModule } from '@ngrx/effects';
import { StoreModule } from '@ngrx/store';
import { NgxJsonViewerModule } from 'ngx-json-viewer';
import { AccordionModule } from 'primeng/accordion';
import { MessageService } from 'primeng/api';
import { CheckboxModule } from 'primeng/checkbox';
import { DialogModule } from 'primeng/dialog';
import { DropdownModule } from 'primeng/dropdown';
import { MessageModule } from 'primeng/message';
import { MessagesModule } from 'primeng/messages';
import { StepsModule } from 'primeng/steps';
import { ToastModule } from 'primeng/toast';
import { TooltipModule } from 'primeng/tooltip';
import {PanelModule} from 'primeng/panel';
import { AppRoutingModule } from './app-routing/app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './auth/login.component';
import { RegisterComponent } from './auth/register.component';
import { VerifyComponent } from './auth/verify.component';
import { CorpusComponent } from './corpus/corpus.component';
import { ListCorpusComponent } from './corpus/list-corpus.component';
import { FooterComponent } from './footer/footer.component';
import { HomeComponent } from './home/home.component';
import { MenuComponent } from './menu/menu.component';
import { ListMethodComponent } from './method/list-method.component';
import { MethodComponent } from './method/method.component';
import { ProcessComponent } from './process/process.component';
import { effects, reducers } from './store';
import { UploadComponent } from './upload/upload.component';
import { TranscriptComponent } from './transcript/transcript.component';

@NgModule({
    declarations: [
        AppComponent,
        FooterComponent,
        MenuComponent,
        HomeComponent,
        UploadComponent,
        ListCorpusComponent,
        CorpusComponent,
        ListMethodComponent,
        MethodComponent,
        LoginComponent,
        ProcessComponent,
        RegisterComponent,
        VerifyComponent,
        TranscriptComponent,
    ],
    imports: [
        AppRoutingModule,
        BrowserModule,
        BrowserAnimationsModule,
        FontAwesomeModule,
        FormsModule,
        HttpClientModule,
        HttpClientXsrfModule.withOptions({
            cookieName: 'csrftoken',
            headerName: 'X-CSRFToken'
        }),
        EffectsModule.forRoot(effects),
        StoreModule.forRoot(reducers),
        NgxJsonViewerModule,
        // PrimeNG
        AccordionModule,
        CheckboxModule,
        DialogModule,
        DropdownModule,
        MessageModule,
        MessagesModule,
        ToastModule,
        TooltipModule,
        PanelModule,
        StepsModule,
    ],
    providers: [MessageService],
    bootstrap: [AppComponent]
})
export class AppModule { }
