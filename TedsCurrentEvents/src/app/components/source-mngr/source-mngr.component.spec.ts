import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SourceMngrComponent } from './source-mngr.component';

describe('SourceMngrComponent', () => {
  let component: SourceMngrComponent;
  let fixture: ComponentFixture<SourceMngrComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SourceMngrComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SourceMngrComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
