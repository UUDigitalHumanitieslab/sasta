import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { UploadSafComponent } from './upload-saf.component';

describe('UploadSafComponent', () => {
    let component: UploadSafComponent;
    let fixture: ComponentFixture<UploadSafComponent>;

    beforeEach(waitForAsync(() => {
        TestBed.configureTestingModule({
            declarations: [UploadSafComponent],
        }).compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(UploadSafComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
