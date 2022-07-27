import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TreeVisualizerComponent } from './tree-visualizer.component';
import { ExtractinatorService } from 'lassy-xpath';

describe('TreeVisualizerComponent', () => {
    let component: TreeVisualizerComponent;
    let fixture: ComponentFixture<TreeVisualizerComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [TreeVisualizerComponent],
            providers: [ExtractinatorService],
        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(TreeVisualizerComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
