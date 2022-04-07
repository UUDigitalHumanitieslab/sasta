import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { NgxJsonViewerModule } from 'ngx-json-viewer';
import { AccordionModule } from 'primeng/accordion';
import { ConfirmationService, MessageService } from 'primeng/api';
import { CheckboxModule } from 'primeng/checkbox';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { DialogModule } from 'primeng/dialog';
import { DropdownModule } from 'primeng/dropdown';
import { FieldsetModule } from 'primeng/fieldset';
import { FileUploadModule } from 'primeng/fileupload';
import { MessageModule } from 'primeng/message';
import { MessagesModule } from 'primeng/messages';
import { PanelModule } from 'primeng/panel';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { StepsModule } from 'primeng/steps';
import { ToastModule } from 'primeng/toast';
import { TooltipModule } from 'primeng/tooltip';
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
import { TranscriptProgressCellComponent } from './process/transcript-progress-cell.component';
import { TranscriptProgressComponent } from './process/transcript-progress.component';
import { TranscriptComponent } from './transcript/transcript.component';
import { UploadSafComponent } from './transcript/upload-saf.component';
import { UploadComponent } from './upload/upload.component';
import { UtterancesListComponent } from './utterances/utterances-list.component';

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
        UploadSafComponent,
        TranscriptProgressComponent,
        TranscriptProgressCellComponent,
        UtterancesListComponent,
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
            headerName: 'X-CSRFToken',
        }),
        NgxJsonViewerModule,
        // PrimeNG
        AccordionModule,
        CheckboxModule,
        ConfirmDialogModule,
        DialogModule,
        DropdownModule,
        FieldsetModule,
        FileUploadModule,
        MessageModule,
        MessagesModule,
        ToastModule,
        TooltipModule,
        PanelModule,
        ProgressSpinnerModule,
        StepsModule,
    ],
    providers: [ConfirmationService, MessageService],
    bootstrap: [AppComponent],
})
export class AppModule {}
